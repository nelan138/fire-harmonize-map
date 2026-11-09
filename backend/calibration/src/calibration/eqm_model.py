"""
FireHarmonize - Member A
Empirical Quantile Mapping (EQM) & Wooster FRP Scaling Model (Audited & Corrected)

Fixes:
1. Replaces degenerate m_counts=[1,1,1] with authentic spatial grid cell fire count distributions.
2. Fits empirical quantiles F_M(N) and F_V(N) across active cells per biome.
3. Trains Wooster FRP power-law regression on clean 1-to-1 Voronoi coincident pairs with Baskerville retransformation energy conservation.
4. Outputs valid, non-degenerate 'calibration_lookup.parquet'.
"""

import sys
from pathlib import Path
import logging
import numpy as np
import pandas as pd
from scipy import stats

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import BIOMES, PROCESSED_CALIBRATED_DIR, RAW_FIRMS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CalibrationModel")


class CalibrationModel:
    def __init__(self):
        self.quantile_steps = np.round(np.linspace(0.01, 0.99, 99), 3)

    def extract_spatial_grid_counts(self, events_df: pd.DataFrame, grid_size: float = 0.1) -> pd.DataFrame:
        """
        Aggregates daytime fire detections into spatial grid cells (e.g. 0.1 deg ~11km)
        per date to extract true empirical distributions of fire counts for MODIS and VIIRS.
        """
        day_events = events_df[events_df["daynight"].astype(str).str.upper() == "D"].copy()
        day_events["grid_lat"] = np.round(day_events["latitude"] / grid_size) * grid_size
        day_events["grid_lon"] = np.round(day_events["longitude"] / grid_size) * grid_size

        inst_col = "instrument_norm" if "instrument_norm" in day_events.columns else "instrument"
        day_events["inst"] = day_events[inst_col].apply(lambda x: "VIIRS" if "VIIRS" in str(x).upper() else "MODIS")

        grouped = day_events.groupby(
            ["region_id", "acq_date", "grid_lat", "grid_lon", "biome_id", "inst"]
        ).size().unstack(fill_value=0).reset_index()

        if "MODIS" not in grouped.columns:
            grouped["MODIS"] = 0
        if "VIIRS" not in grouped.columns:
            grouped["VIIRS"] = 0

        # Return cells where at least one sensor detected fire
        active_cells = grouped[(grouped["MODIS"] > 0) | (grouped["VIIRS"] > 0)].copy()
        logger.info(f"Aggregated {len(active_cells):,} active spatial grid cells across observation dates.")
        return active_cells

    def train_biome_calibration(
        self,
        pairs_df: pd.DataFrame,
        events_df: pd.DataFrame = None,
        default_biome_id: int = 1
    ) -> pd.DataFrame:
        """
        Train EQM quantiles from spatial grid count distributions and Wooster FRP scaling from 1-to-1 coincident pairs.
        """
        if events_df is None:
            raw_path = RAW_FIRMS_DIR / "GLOBAL_5_REGIONS_clean_fire_events.parquet"
            events_df = pd.read_parquet(raw_path)

        grid_df = self.extract_spatial_grid_counts(events_df)
        lookup_rows = []

        # Baseline literature priors for biomes with limited empirical overpasses (e.g. Croplands Biome 3)
        baseline_params = {
            1: {"alpha": 0.631, "beta": 1.477},
            2: {"alpha": 0.625, "beta": 1.711},
            3: {"alpha": 0.600, "beta": 1.850},
            4: {"alpha": 0.517, "beta": 2.059},
        }

        for biome_id, biome_name in BIOMES.items():
            b_pairs = pairs_df[pairs_df["biome_id"] == biome_id] if "biome_id" in pairs_df.columns else pd.DataFrame()
            b_grid = grid_df[grid_df["biome_id"] == biome_id]
            base = baseline_params[biome_id]

            # 1. Wooster FRP Power-Law Fit
            if len(b_pairs) >= 20:
                valid_frp = (b_pairs["modis_frp"] > 0) & (b_pairs["viirs_frp_sum"] > 0)
                if valid_frp.sum() >= 10:
                    x = np.log(b_pairs.loc[valid_frp, "modis_frp"].values)
                    y = np.log(b_pairs.loc[valid_frp, "viirs_frp_sum"].values)
                    slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
                    frp_alpha = float(slope)
                    frp_beta_raw = float(intercept)

                    # Baskerville / Wooster Retransformation Factor for exact energy conservation
                    m_vals = b_pairs["modis_frp"].values
                    v_true_sum = b_pairs["viirs_frp_sum"].sum()
                    pred_unadj = np.sum([np.exp(frp_beta_raw) * (m ** frp_alpha) if m > 0 else 0.0 for m in m_vals])
                    if pred_unadj > 0 and v_true_sum > 0:
                        retrans_mult = v_true_sum / pred_unadj
                        frp_beta = float(frp_beta_raw + np.log(retrans_mult))
                    else:
                        frp_beta = frp_beta_raw
                else:
                    frp_alpha, frp_beta = base["alpha"], base["beta"]
            else:
                frp_alpha, frp_beta = base["alpha"], base["beta"]

            # 2. Empirical Quantile Mapping from Real Spatial Cell Distributions
            # Use cells where fires were detected by either or both sensors
            if len(b_grid) >= 20 and (b_grid["MODIS"] > 0).sum() >= 10:
                # MODIS active cells in this biome
                m_active_counts = b_grid.loc[b_grid["MODIS"] > 0, "MODIS"].values
                v_active_counts = b_grid.loc[b_grid["VIIRS"] > 0, "VIIRS"].values

                m_quantiles = np.quantile(m_active_counts, self.quantile_steps)
                v_quantiles = np.quantile(v_active_counts, self.quantile_steps)
            else:
                # For Biomes with sparse cells (e.g. Croplands), scale from global empirical distribution
                all_m = grid_df.loc[grid_df["MODIS"] > 0, "MODIS"].values
                all_v = grid_df.loc[grid_df["VIIRS"] > 0, "VIIRS"].values
                m_quantiles = np.quantile(all_m, self.quantile_steps)
                # Agricultural burns have higher sub-pixel fragmentation
                crop_multiplier = 1.35 if biome_id == 3 else 1.0
                v_quantiles = np.quantile(all_v * crop_multiplier, self.quantile_steps)

            # Ensure monotonic non-decreasing quantiles
            m_quantiles = np.maximum.accumulate(m_quantiles)
            v_quantiles = np.maximum.accumulate(v_quantiles)

            logger.info(f"Biome {biome_id} ({biome_name}):")
            logger.info(f"  FRP: alpha={frp_alpha:.3f}, beta={frp_beta:.3f}")
            logger.info(f"  EQM Quantiles range: MODIS=[{m_quantiles[0]:.1f}..{m_quantiles[-1]:.1f}], VIIRS=[{v_quantiles[0]:.1f}..{v_quantiles[-1]:.1f}]")

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
        lookup_df["biome_id"] = lookup_df["biome_id"].astype("int8")
        lookup_df["quantile_step"] = lookup_df["quantile_step"].astype("float32")
        lookup_df["modis_q_val"] = lookup_df["modis_q_val"].astype("float32")
        lookup_df["viirs_q_val"] = lookup_df["viirs_q_val"].astype("float32")
        lookup_df["frp_alpha"] = lookup_df["frp_alpha"].astype("float32")
        lookup_df["frp_beta"] = lookup_df["frp_beta"].astype("float32")

        return lookup_df

    def save_lookup(self, df: pd.DataFrame) -> Path:
        """Save calibration lookup to parquet"""
        PROCESSED_CALIBRATED_DIR.mkdir(parents=True, exist_ok=True)
        out_file = PROCESSED_CALIBRATED_DIR / "calibration_lookup.parquet"
        df.to_parquet(out_file, index=False)
        logger.info(f"Saved non-degenerate calibration lookup table to: {out_file}")
        return out_file


def main():
    pairs_path = Path("D:/Project/NASA/VIIRS/data/processed/coincident_pairs/GLOBAL_coincident_pairs_multi_biome.parquet")
    events_path = Path("D:/Project/NASA/VIIRS/data/raw/firms/GLOBAL_5_REGIONS_clean_fire_events.parquet")

    logger.info("Training audited EQM and Wooster Calibration Model...")
    pairs_df = pd.read_parquet(pairs_path)
    events_df = pd.read_parquet(events_path)

    model = CalibrationModel()
    lookup_df = model.train_biome_calibration(pairs_df, events_df)
    model.save_lookup(lookup_df)
    print("Done generating calibration_lookup.parquet!")


if __name__ == "__main__":
    main()
