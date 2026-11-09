"""
FireHarmonize - Member A
Coincident Overpass Extraction (Aqua MODIS vs Suomi-NPP VIIRS)
Matches thermal anomalies observed during the 13:30 local solar time window
satisfying:
1. Δt <= 30 minutes
2. Δd <= 1,000 meters (Haversine spatial distance)
"""

import sys
from pathlib import Path
import logging
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import FILTER_CONFIG, PROCESSED_COINCIDENT_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CoincidentFilter")

EARTH_RADIUS_METERS = 6371000.0


def time_to_minutes(acq_time_val) -> int:
    """Convert 'HHMM' or integer HHMM to minutes from midnight"""
    val_str = str(acq_time_val).zfill(4)
    try:
        hours = int(val_str[:2])
        mins = int(val_str[2:4])
        return hours * 60 + mins
    except Exception:
        return 0


def haversine_distance_matrix(lat1, lon1, lat2, lon2):
    """Compute Haversine distance in meters between two points or arrays"""
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return EARTH_RADIUS_METERS * c


def extract_coincident_pairs(
    df: pd.DataFrame,
    max_dist_m: float = None,
    max_time_diff_min: float = None,
) -> pd.DataFrame:
    """
    Extract coincident observation pairs between Aqua MODIS and Suomi-NPP/NOAA-20 VIIRS.
    """
    if df.empty:
        return pd.DataFrame()

    max_dist_m = max_dist_m or FILTER_CONFIG["coincident_max_distance_m"]
    max_time_diff_min = max_time_diff_min or FILTER_CONFIG["coincident_max_time_diff_min"]

    # Normalize instrument names
    df["instrument_norm"] = df["instrument"].astype(str).str.upper()
    
    # Split into MODIS and VIIRS subsets
    modis_df = df[df["instrument_norm"].str.contains("MODIS")].copy()
    viirs_df = df[df["instrument_norm"].str.contains("VIIRS")].copy()

    if modis_df.empty or viirs_df.empty:
        logger.warning(f"Cannot extract pairs: MODIS has {len(modis_df)} points, VIIRS has {len(viirs_df)} points.")
        return pd.DataFrame()

    # Precalculate time in minutes
    modis_df["time_min"] = modis_df["acq_time"].apply(time_to_minutes)
    viirs_df["time_min"] = viirs_df["acq_time"].apply(time_to_minutes)

    matched_pairs = []

    # Match within the same acquisition date
    common_dates = set(modis_df["acq_date"].unique()).intersection(set(viirs_df["acq_date"].unique()))
    logger.info(f"Finding coincident overpasses across {len(common_dates)} shared observation dates...")

    for date in common_dates:
        m_day = modis_df[modis_df["acq_date"] == date].reset_index(drop=True)
        v_day = viirs_df[viirs_df["acq_date"] == date].reset_index(drop=True)

        # Convert lat/lon to 3D Cartesian coordinates on unit sphere for fast spatial KDTree search
        m_lats, m_lons = np.radians(m_day["latitude"]), np.radians(m_day["longitude"])
        v_lats, v_lons = np.radians(v_day["latitude"]), np.radians(v_day["longitude"])

        m_xyz = np.column_stack([
            np.cos(m_lats) * np.cos(m_lons),
            np.cos(m_lats) * np.sin(m_lons),
            np.sin(m_lats)
        ])
        v_xyz = np.column_stack([
            np.cos(v_lats) * np.cos(v_lons),
            np.cos(v_lats) * np.sin(v_lons),
            np.sin(v_lats)
        ])

        tree = cKDTree(v_xyz)
        # Search radius in chord distance: 2 * sin(d / (2 * R))
        chord_radius = 2.0 * np.sin(max_dist_m / (2.0 * EARTH_RADIUS_METERS))
        indices_list = tree.query_ball_point(m_xyz, r=chord_radius)

        for m_idx, v_indices in enumerate(indices_list):
            if not v_indices:
                continue
            
            m_time = m_day.loc[m_idx, "time_min"]
            m_frp = m_day.loc[m_idx, "frp"]
            m_lat = m_day.loc[m_idx, "latitude"]
            m_lon = m_day.loc[m_idx, "longitude"]

            # Filter by time difference
            valid_v_indices = []
            for v_idx in v_indices:
                v_time = v_day.loc[v_idx, "time_min"]
                if abs(m_time - v_time) <= max_time_diff_min:
                    valid_v_indices.append(v_idx)

            if valid_v_indices:
                # Sum FRP of all collocated VIIRS sub-pixels within the 1km MODIS footprint
                v_sub = v_day.loc[valid_v_indices]
                total_viirs_frp = v_sub["frp"].sum()
                viirs_count = len(valid_v_indices)

                matched_pairs.append({
                    "acq_date": date,
                    "modis_lat": m_lat,
                    "modis_lon": m_lon,
                    "modis_time": m_day.loc[m_idx, "acq_time"],
                    "modis_frp": m_frp,
                    "modis_confidence": m_day.loc[m_idx, "confidence"],
                    "viirs_count": viirs_count,
                    "viirs_frp_sum": total_viirs_frp,
                    "viirs_mean_lat": v_sub["latitude"].mean(),
                    "viirs_mean_lon": v_sub["longitude"].mean(),
                    "count_ratio": viirs_count / 1.0,
                    "frp_ratio": total_viirs_frp / max(m_frp, 1e-3),
                })

    pairs_df = pd.DataFrame(matched_pairs)
    if "modis_confidence" in pairs_df.columns:
        pairs_df["modis_confidence"] = pairs_df["modis_confidence"].astype(str)
    logger.info(f"Extracted {len(pairs_df)} coincident overpass clusters!")
    return pairs_df


def save_coincident_pairs(df: pd.DataFrame, region_key: str) -> Path:
    """Save coincident pairs to parquet"""
    out_file = PROCESSED_COINCIDENT_DIR / f"{region_key}_coincident_pairs.parquet"
    df.to_parquet(out_file, index=False)
    logger.info(f"Saved coincident pairs to {out_file}")
    return out_file
