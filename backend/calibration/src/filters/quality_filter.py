"""
FireHarmonize - Member A
Quality and Confidence Filter
Applies NASA FIRMS science-quality filtering:
- MODIS: drop confidence < 30%
- VIIRS: drop confidence == 'low'
- Outlier filtering (valid lat/lon ranges, non-negative FRP)
"""

import sys
from pathlib import Path
import logging
import pandas as pd

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import FILTER_CONFIG

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("QualityFilter")


def filter_active_fires(df: pd.DataFrame) -> pd.DataFrame:
    """Filter fire events according to project quality thresholds"""
    if df.empty:
        return df
    
    initial_count = len(df)
    
    # 1. Geographic bounds check
    valid_coords = (
        (df["latitude"] >= -90.0) & (df["latitude"] <= 90.0) &
        (df["longitude"] >= -180.0) & (df["longitude"] <= 180.0)
    )
    df = df[valid_coords].copy()

    # 2. Confidence filter
    # For MODIS: confidence is usually numeric (0-100)
    modis_mask = df["instrument"].str.upper() == "MODIS"
    if "confidence" in df.columns:
        modis_conf_numeric = pd.to_numeric(df.loc[modis_mask, "confidence"], errors="coerce").fillna(0)
        keep_modis = modis_conf_numeric >= FILTER_CONFIG["modis_min_confidence"]
        
        # For VIIRS: confidence is categorical ('l', 'n', 'h' or 'low', 'nominal', 'high')
        viirs_mask = df["instrument"].str.upper() == "VIIRS"
        viirs_conf_str = df.loc[viirs_mask, "confidence"].astype(str).str.lower()
        drop_vals = [v.lower() for v in FILTER_CONFIG["viirs_drop_confidence"]] + ["l"]
        keep_viirs = ~viirs_conf_str.isin(drop_vals)

        # Combine
        keep_indices = df.index[
            (modis_mask & keep_modis) | (viirs_mask & keep_viirs) | (~modis_mask & ~viirs_mask)
        ]
        df = df.loc[keep_indices].copy()

    # 3. FRP validity (FRP >= 0)
    if "frp" in df.columns:
        df["frp"] = pd.to_numeric(df["frp"], errors="coerce").fillna(0.0)
        df = df[df["frp"] >= 0.0]

    logger.info(f"Quality filter: kept {len(df)}/{initial_count} records ({round(len(df)/initial_count*100, 1)}%)")
    return df

