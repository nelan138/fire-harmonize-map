"""
FireHarmonize - Member A
Coincident Overpass Extraction (Aqua MODIS vs Suomi-NPP VIIRS)
Matches thermal anomalies observed during the daytime 13:30 local solar time window
satisfying:
1. Δt <= 30 minutes
2. Δd <= 1,000 meters (Haversine spatial distance, matching MODIS 1km nadir pixel)
3. Daytime observations only (daynight == 'D')
4. Voronoi 1-to-1 nearest-neighbor partitioning to strictly prevent multi-counting
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


def extract_coincident_pairs(
    df: pd.DataFrame,
    max_dist_m: float = None,
    max_time_diff_min: float = None,
    require_daytime: bool = True,
) -> pd.DataFrame:
    """
    Extract coincident observation pairs between Aqua MODIS and Suomi-NPP VIIRS
    using strict 1-to-1 Voronoi spatial assignment to guarantee zero multi-counting.
    """
    if df.empty:
        return pd.DataFrame()

    max_dist_m = max_dist_m or FILTER_CONFIG["coincident_max_distance_m"]
    max_time_diff_min = max_time_diff_min or FILTER_CONFIG["coincident_max_time_diff_min"]

    # 1. Enforce strict Daytime filter (13:30 afternoon overpass window)
    if require_daytime and "daynight" in df.columns:
        initial_count = len(df)
        df = df[df["daynight"].astype(str).str.upper() == "D"].copy()
        logger.info(f"Filtered for daytime overpasses (daynight == 'D'): {len(df):,} of {initial_count:,} events kept.")

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
    total_assigned_viirs = 0

    # Match within the same acquisition date
    common_dates = sorted(set(modis_df["acq_date"].unique()).intersection(set(viirs_df["acq_date"].unique())))
    logger.info(f"Finding coincident overpasses across {len(common_dates)} shared observation dates (radius={max_dist_m}m, dt<={max_time_diff_min}m)...")

    for date in common_dates:
        m_day = modis_df[modis_df["acq_date"] == date].reset_index(drop=True)
        v_day = viirs_df[viirs_df["acq_date"] == date].reset_index(drop=True)

        if m_day.empty or v_day.empty:
            continue

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

        # Voronoi 1-to-1 Partitioning:
        # Build KDTree on MODIS centroids, then query for each VIIRS point.
        # This guarantees each VIIRS point is assigned to AT MOST ONE nearest MODIS centroid!
        tree_modis = cKDTree(m_xyz)
        chord_radius = 2.0 * np.sin(max_dist_m / (2.0 * EARTH_RADIUS_METERS))
        dists, nearest_m_indices = tree_modis.query(v_xyz, distance_upper_bound=chord_radius)

        assigned_clusters = {}
        for v_idx, (dist, m_idx) in enumerate(zip(dists, nearest_m_indices)):
            if dist <= chord_radius and m_idx < len(m_day):
                # Check acquisition time difference
                dt = abs(v_day.loc[v_idx, "time_min"] - m_day.loc[m_idx, "time_min"])
                if dt <= max_time_diff_min:
                    assigned_clusters.setdefault(m_idx, []).append(v_idx)

        for m_idx, v_indices in assigned_clusters.items():
            v_sub = v_day.loc[v_indices]
            m_pt = m_day.loc[m_idx]
            
            total_viirs_frp = float(v_sub["frp"].sum())
            viirs_count = int(len(v_indices))
            total_assigned_viirs += viirs_count

            matched_pairs.append({
                "acq_date": str(date),
                "modis_lat": float(m_pt["latitude"]),
                "modis_lon": float(m_pt["longitude"]),
                "modis_time": int(m_pt["acq_time"]),
                "modis_frp": float(m_pt["frp"]),
                "modis_confidence": str(m_pt["confidence"]),
                "viirs_count": viirs_count,
                "viirs_frp_sum": total_viirs_frp,
                "viirs_mean_lat": float(v_sub["latitude"].mean()),
                "viirs_mean_lon": float(v_sub["longitude"].mean()),
                "count_ratio": float(viirs_count),
                "frp_ratio": float(total_viirs_frp / max(float(m_pt["frp"]), 1e-3)),
                "region_id": str(m_pt.get("region_id", "UNKNOWN")),
                "biome_id": int(m_pt.get("biome_id", 1)),
            })

    pairs_df = pd.DataFrame(matched_pairs)
    logger.info(f"Extracted {len(pairs_df):,} clean 1-to-1 coincident clusters grouping {total_assigned_viirs:,} VIIRS detections.")
    return pairs_df


def save_coincident_pairs(df: pd.DataFrame, region_key: str) -> Path:
    """Save coincident pairs to parquet"""
    PROCESSED_COINCIDENT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PROCESSED_COINCIDENT_DIR / f"{region_key}_coincident_pairs.parquet"
    df.to_parquet(out_file, index=False)
    logger.info(f"Saved coincident pairs to {out_file}")
    return out_file
