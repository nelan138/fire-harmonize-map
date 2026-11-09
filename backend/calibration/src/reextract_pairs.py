import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from config import RAW_FIRMS_DIR, PROCESSED_COINCIDENT_DIR, HOTSPOT_REGIONS
from filters.coincident_filter import extract_coincident_pairs, save_coincident_pairs

# Load clean fire events
clean_global_path = RAW_FIRMS_DIR / "GLOBAL_5_REGIONS_clean_fire_events.parquet"
df_global = pd.read_parquet(clean_global_path)

all_pairs = []
for reg_key in HOTSPOT_REGIONS.keys():
    df_reg = df_global[df_global["region_id"] == reg_key].copy()
    print(f"\nProcessing {reg_key}: {len(df_reg):,} events...")
    pairs = extract_coincident_pairs(df_reg, max_dist_m=1000.0, max_time_diff_min=30.0, require_daytime=True)
    if not pairs.empty:
        save_coincident_pairs(pairs, reg_key)
        all_pairs.append(pairs)

if all_pairs:
    global_df = pd.concat(all_pairs, ignore_index=True)
    global_path = PROCESSED_COINCIDENT_DIR / "GLOBAL_coincident_pairs_multi_biome.parquet"
    global_df.to_parquet(global_path, index=False)
    print(f"\nSuccessfully updated GLOBAL coincident pairs:")
    print(f"  Clusters: {len(global_df):,}")
    print(f"  Total matched VIIRS points: {global_df['viirs_count'].sum():,}")
    print(f"  Biomes represented:\n{global_df['biome_id'].value_counts()}")
