"""
FireHarmonize - Member A
Batch Multi-Region Harvester (5 Global Hotspots)
Downloads real multi-day active fire observations from NASA FIRMS for all 5 study regions,
extracts coincident overpasses, and trains the multi-biome calibration model.
Strictly 100% Real NASA Satellite Data.
"""

import sys
from pathlib import Path
import time
import logging
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    HOTSPOT_REGIONS,
    FIRMS_MAP_KEY,
    RAW_FIRMS_DIR,
    PROCESSED_COINCIDENT_DIR,
    PROCESSED_CALIBRATED_DIR,
)
from downloaders.firms_downloader import FIRMSDownloader
from filters.quality_filter import filter_active_fires
from filters.coincident_filter import extract_coincident_pairs, save_coincident_pairs
from calibration.eqm_model import CalibrationModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BatchHarvester")

# High-fire historic observation windows for the 5 regions:
TARGET_HARVEST_CAMPAIGNS = {
    "INDOCHINA": {
        "date_str": "2023-03-15",
        "days": 5,
        "biome": 1,
        "desc": "Peak dry season in SE Asia (Laos/Cambodia/Vietnam)",
    },
    "AMAZON": {
        "date_str": "2023-08-15",
        "days": 5,
        "biome": 1,
        "desc": "Peak deforestation & burning season in Amazon Basin",
    },
    "CALIFORNIA": {
        "date_str": "2020-09-08",
        "days": 5,
        "biome": 4,
        "desc": "Creek Fire & August Complex fire season",
    },
    "PANTANAL": {
        "date_str": "2020-10-01",
        "days": 5,
        "biome": 2,
        "desc": "Historic wetland drought & savanna fires in Brazil",
    },
    "SE_AUSTRALIA": {
        "date_str": "2020-01-01",
        "days": 5,
        "biome": 2,
        "desc": "Black Summer mega-fires peak",
    },
}


def harvest_all_regions(map_key: str = None):
    key = map_key or FIRMS_MAP_KEY
    firms = FIRMSDownloader(map_key=key)
    cal_model = CalibrationModel()

    all_clean_events = []
    all_coincident_pairs = []

    print("\n" + "=" * 75)
    print("🌍 FIREHARMONIZE - 5 GLOBAL HOTSPOTS BATCH HARVEST (100% REAL NASA DATA)")
    print("=" * 75 + "\n")

    for region_key, campaign in TARGET_HARVEST_CAMPAIGNS.items():
        region_cfg = HOTSPOT_REGIONS[region_key]
        bbox = region_cfg["bbox"]
        date_str = campaign["date_str"]
        days = campaign["days"]
        biome_id = campaign["biome"]

        print(f"\n--- Harvesting {region_key} ({region_cfg['name']}) ---")
        print(f"    Date window: {date_str} (+{days} days) | Biome: {biome_id} ({campaign['desc']})")

        # 1. Download VIIRS (VNP14IMGTDL Standard Quality)
        logger.info(f"Downloading VIIRS_SNPP_SP for {region_key}...")
        v_df = firms.download_area_hotspots("VIIRS_SNPP_SP", bbox=bbox, day_range=days, date_str=date_str)
        time.sleep(1.0) # Polite pause between API calls

        # 2. Download MODIS (MCD14ML Standard Quality)
        logger.info(f"Downloading MODIS_SP for {region_key}...")
        m_df = firms.download_area_hotspots("MODIS_SP", bbox=bbox, day_range=days, date_str=date_str)
        time.sleep(1.0)

        # 3. Combine & save raw
        combined = pd.concat([v_df, m_df], ignore_index=True)
        raw_path = firms.save_to_disk(combined, region_key, f"CAMPAIGN_{date_str}")

        # 4. Filter Quality
        clean_df = filter_active_fires(combined)
        clean_df["region_id"] = region_key
        clean_df["biome_id"] = biome_id
        all_clean_events.append(clean_df)

        # 5. Extract coincident pairs
        logger.info(f"Extracting coincident pairs for {region_key}...")
        pairs = extract_coincident_pairs(clean_df)
        if not pairs.empty:
            pairs["region_id"] = region_key
            pairs["biome_id"] = biome_id
            save_coincident_pairs(pairs, region_key)
            all_coincident_pairs.append(pairs)
            logger.info(f"-> {region_key}: {len(pairs)} coincident overpass clusters extracted.")
        else:
            logger.warning(f"-> {region_key}: No coincident overpasses found in this window.")

    # -------------------------------------------------------------
    # Consolidate Global Dataset & Train Final Multi-Biome Calibration
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print("📈 CONSOLIDATING GLOBAL MULTI-BIOME CALIBRATION DATASET")
    print("=" * 75)

    if all_clean_events:
        total_clean = pd.concat(all_clean_events, ignore_index=True)
        total_clean_path = RAW_FIRMS_DIR / "GLOBAL_5_REGIONS_clean_fire_events.parquet"
        total_clean.to_parquet(total_clean_path, index=False)
        print(f"📦 Total Real Active Fire Events: {len(total_clean):,} saved to {total_clean_path.name}")

    if all_coincident_pairs:
        total_pairs = pd.concat(all_coincident_pairs, ignore_index=True)
        total_pairs_path = PROCESSED_COINCIDENT_DIR / "GLOBAL_coincident_pairs_multi_biome.parquet"
        total_pairs.to_parquet(total_pairs_path, index=False)
        print(f"📦 Total Real Coincident Clusters: {len(total_pairs):,} saved to {total_pairs_path.name}")

        # Train EQM Model
        print("\nTraining Empirical Quantile Mapping across 4 Biomes...")
        lookup_df = cal_model.train_biome_calibration(total_pairs)
        lookup_path = cal_model.save_calibration_lookup(lookup_df)
        print(f"✅ Final Calibration Table: {lookup_path}")

    print("\n" + "=" * 75)
    print("🎉 BATCH HARVEST COMPLETED SUCCESSFULLY WITH 100% REAL SATELLITE DATA!")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    harvest_all_regions()

