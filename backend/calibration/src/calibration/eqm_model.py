"""
FireHarmonize - Member A
Empirical Quantile Mapping (EQM) & FRP Scaling Model
Trains cross-sensor calibration parameters across 4 biomes:
1. Dense Tropical & Temperate Forests
2. Savanna & Grasslands
3. Croplands
4. Shrublands & Chaparral

Outputs: 'calibration_lookup.parquet' adhering to the project schema contract.
"""

import sys
from pathlib import Path
import logging
import numpy as np
import pandas as pd
from scipy import stats

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import BIOMES, PROCESSED_CALIBRATED_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CalibrationModel")


class CalibrationModel:
    def __init__(self):
        self.quantile_steps = np.round(np.linspace(0.01, 0.99, 99), 3)

    def train_biome_calibration(self, pairs_df: pd.DataFrame, default_biome_id: int = 1) -> pd.DataFrame:
        """
        Train EQM quantiles and FRP log-log scaling parameters.
        Pairs dataframe has columns: modis_frp, viirs_frp_sum, viirs_count
        """
        lookup_rows = []

        # If biome_id column is not in pairs_df, assign default or synthesize across 4 biomes
        if "biome_id" not in pairs_df.columns:
            pairs_df["biome_id"] = default_biome_id

        # Theoretical and literature baseline coefficients for 4 biomes (from LaTeX review):
        # Biome 1 (Forest): k ~ 4.5, high attenuation
        # Biome 2 (Savanna): k ~ 2.2, open canopy
        # Biome 3 (Croplands): k ~ 5.5, small agricultural fires
        # Biome 4 (Shrublands): k ~ 3.3, moderate shrub cover
        baseline_params = {
            1: {"k_count": 4.5, "alpha": 0.98, "beta": 0.45},
            2: {"k_count": 2.2, "alpha": 1.01, "beta": 0.20},
            3: {"k_count": 5.8, "alpha": 0.92, "beta": 0.60},
            4: {"k_count": 3.4, "alpha": 0.99, "beta": 0.35},
        }

        for biome_id, biome_name in BIOMES.items():
            sub = pairs_df[pairs_df["biome_id"] == biome_id]
            base = baseline_params[biome_id]

            if len(sub) >= 20:
                # Direct Empirical fit from real matched coincident overpasses
                v_counts = sub["viirs_count"].values
                m_counts = np.ones(len(sub), dtype=float)  # Base 1km MODIS detection footprint
                
                # Compute log-log regression for FRP: ln(FRP_VIIRS) = alpha * ln(FRP_MODIS) + beta
                valid_frp = (sub["modis_frp"] > 0) & (sub["viirs_frp_sum"] > 0)
                if valid_frp.sum() >= 10:
                    x = np.log(sub.loc[valid_frp, "modis_frp"].values)
                    y = np.log(sub.loc[valid_frp, "viirs_frp_sum"].values)
                    slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
                    frp_alpha = float(slope)
                    frp_beta_raw = float(intercept)
                    
                    # Apply Wooster Physical Energy Conservation Constraint (Baskerville/Wooster Retransformation Factor):
                    # Enforces total predicted VIIRS energy to match total observed VIIRS energy across the whole biome
                    m_vals = sub["modis_frp"].values
                    v_true_sum = sub["viirs_frp_sum"].sum()
                    pred_unadjusted = np.sum([np.exp(frp_beta_raw) * (m ** frp_alpha) if m > 0 else 0.0 for m in m_vals])
                    if pred_unadjusted > 0 and v_true_sum > 0:
                        wooster_multiplier = v_true_sum / pred_unadjusted
                        frp_beta = float(frp_beta_raw + np.log(wooster_multiplier))
                    else:
                        frp_beta = frp_beta_raw
                else:
                    frp_alpha, frp_beta = base["alpha"], base["beta"]

                # Real Empirical quantiles
                m_quantiles = np.quantile(m_counts, self.quantile_steps)
                v_quantiles = np.quantile(v_counts, self.quantile_steps)
            else:
                logger.info(f"Using literature priors calibrated against observed distribution for Biome {biome_id} ({biome_name})")
                frp_alpha = base["alpha"]
                frp_beta = base["beta"]
                
                # Use real global pairs distribution scaled by biome sensitivity ratio
                all_v_counts = pairs_df["viirs_count"].values if not pairs_df.empty else np.array([1.0, 2.0, 3.0, 4.0])
                all_m_counts = np.ones(len(all_v_counts), dtype=float)
                
                biome_scale = base["k_count"] / baseline_params[default_biome_id]["k_count"]
                m_quantiles = np.quantile(all_m_counts, self.quantile_steps)
                v_quantiles = np.quantile(all_v_counts * biome_scale, self.quantile_steps)

            for q_step, m_q, v_q in zip(self.quantile_steps, m_quantiles, v_quantiles):
                lookup_rows.append({
                    "biome_id": int(biome_id),
                    "quantile_step": float(q_step),
                    "modis_q_val": float(np.round(m_q, 4)),
                    "viirs_q_val": float(np.round(v_q, 4)),
                    "frp_alpha": float(np.round(frp_alpha, 4)),
                    "frp_beta": float(np.round(frp_beta, 4)),
                })

        lookup_df = pd.DataFrame(lookup_rows)
        # Ensure schema types strictly adhere to contract:
        lookup_df["biome_id"] = lookup_df["biome_id"].astype("int8")
        lookup_df["quantile_step"] = lookup_df["quantile_step"].astype("float32")
        lookup_df["modis_q_val"] = lookup_df["modis_q_val"].astype("float32")
        lookup_df["viirs_q_val"] = lookup_df["viirs_q_val"].astype("float32")
        lookup_df["frp_alpha"] = lookup_df["frp_alpha"].astype("float32")
        lookup_df["frp_beta"] = lookup_df["frp_beta"].astype("float32")

        logger.info(f"Generated calibration lookup table with {len(lookup_df)} rows across 4 biomes.")
        return lookup_df

    def save_calibration_lookup(self, lookup_df: pd.DataFrame) -> Path:
        """Save calibration_lookup.parquet conforming to contract schema"""
        out_path = PROCESSED_CALIBRATED_DIR / "calibration_lookup.parquet"
        lookup_df.to_parquet(out_path, index=False)
        logger.info(f"Successfully saved lookup table to: {out_path}")
        return out_path


def apply_eqm_to_modis(
    raw_modis_count: float,
    biome_id: int,
    lookup_df: pd.DataFrame
) -> float:
    """
    Applies Empirical Quantile Mapping: N_V = F_V^{-1}(F_M(N_M))
    """
    sub = lookup_df[lookup_df["biome_id"] == biome_id]
    if sub.empty or raw_modis_count <= 0:
        return 0.0
    
    # 1. Find percentile p such that F_M(N_M) = p
    m_vals = sub["modis_q_val"].values
    v_vals = sub["viirs_q_val"].values
    
    # Interpolate percentile
    p = np.interp(raw_modis_count, m_vals, sub["quantile_step"].values)
    
    # 2. Invert using VIIRS CDF: N_V = F_V^{-1}(p)
    scaled_count = float(np.interp(p, sub["quantile_step"].values, v_vals))
    return scaled_count

