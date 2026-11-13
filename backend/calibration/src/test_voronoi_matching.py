import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

df = pd.read_parquet(r"D:\Project\NASA\VIIRS\data\raw\firms\GLOBAL_5_REGIONS_clean_fire_events.parquet")

# 1. Filter strictly daytime 'D'
df_day = df[df["daynight"] == "D"].copy()
print(f"Total clean events: {len(df):,}")
print(f"Daytime events: {len(df_day):,} (MODIS: {(df_day['instrument']=='MODIS').sum():,}, VIIRS: {(df_day['instrument']=='VIIRS').sum():,})")

# Matching thresholds: 1,000 meters, 30 minutes
EARTH_R = 6371000.0
max_dist = 1000.0
max_time = 30.0
chord_r = 2.0 * np.sin(max_dist / (2.0 * EARTH_R))

def time_to_min(val):
    s = str(val).zfill(4)
    return int(s[:2]) * 60 + int(s[2:4])

df_day["time_min"] = df_day["acq_time"].apply(time_to_min)

modis_df = df_day[df_day["instrument"] == "MODIS"].reset_index(drop=True)
viirs_df = df_day[df_day["instrument"] == "VIIRS"].reset_index(drop=True)

dates = sorted(set(modis_df["acq_date"]).intersection(set(viirs_df["acq_date"])))
print("Shared dates:", len(dates))

clusters = []
matched_viirs_indices = set()

for d in dates:
    m_sub = modis_df[modis_df["acq_date"] == d].reset_index(drop=True)
    v_sub = viirs_df[viirs_df["acq_date"] == d].reset_index(drop=True)
    
    m_rad_lat, m_rad_lon = np.radians(m_sub["latitude"]), np.radians(m_sub["longitude"])
    v_rad_lat, v_rad_lon = np.radians(v_sub["latitude"]), np.radians(v_sub["longitude"])
    
    m_xyz = np.column_stack([np.cos(m_rad_lat)*np.cos(m_rad_lon), np.cos(m_rad_lat)*np.sin(m_rad_lon), np.sin(m_rad_lat)])
    v_xyz = np.column_stack([np.cos(v_rad_lat)*np.cos(v_rad_lon), np.cos(v_rad_lat)*np.sin(v_rad_lon), np.sin(v_rad_lat)])
    
    tree_m = cKDTree(m_xyz)
    dists, nearest_m = tree_m.query(v_xyz, distance_upper_bound=chord_r)
    
    # 1-to-1 Voronoi grouping
    assigned_v = {}
    for v_i, (dist, m_i) in enumerate(zip(dists, nearest_m)):
        if dist <= chord_r and m_i < len(m_sub):
            dt = abs(v_sub.loc[v_i, "time_min"] - m_sub.loc[m_i, "time_min"])
            if dt <= max_time:
                assigned_v.setdefault(m_i, []).append(v_i)
    
    for m_i, v_list in assigned_v.items():
        v_pts = v_sub.loc[v_list]
        m_pt = m_sub.loc[m_i]
        
        clusters.append({
            "acq_date": d,
            "modis_lat": m_pt["latitude"],
            "modis_lon": m_pt["longitude"],
            "modis_time": m_pt["acq_time"],
            "modis_frp": m_pt["frp"],
            "modis_confidence": str(m_pt["confidence"]),
            "viirs_count": len(v_list),
            "viirs_frp_sum": v_pts["frp"].sum(),
            "viirs_mean_lat": v_pts["latitude"].mean(),
            "viirs_mean_lon": v_pts["longitude"].mean(),
            "count_ratio": float(len(v_list)),
            "frp_ratio": float(v_pts["frp"].sum() / max(m_pt["frp"], 1e-3)),
            "region_id": m_pt["region_id"],
            "biome_id": int(m_pt["biome_id"]),
        })

pairs_res = pd.DataFrame(clusters)
print(f"Total clean 1-to-1 clusters: {len(pairs_res):,}")
print(f"Total matched VIIRS points: {pairs_res['viirs_count'].sum():,}")
print(f"Total daytime VIIRS points: {len(viirs_df):,}")
print(f"Strictly leak-free (matched <= total)? {pairs_res['viirs_count'].sum() <= len(viirs_df)}")
print("\nCount ratio percentiles:")
print(pairs_res["viirs_count"].describe())
