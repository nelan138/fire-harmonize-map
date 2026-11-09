"""
FireHarmonize - Member A Orchestrator
Master CLI pipeline script for:
1. Fetching active fire data (NASA FIRMS)
2. Quality filtering
3. Extracting 13:30 coincident overpasses (Aqua MODIS & Suomi-NPP VIIRS)
4. Training EQM Quantile Mapping and FRP scaling across 4 biomes
5. Exporting 'calibration_lookup.parquet'
6. Fetching GIBS WMS satellite images for visual ground truth
"""

import sys
from pathlib import Path
import argparse
import logging
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    HOTSPOT_REGIONS,
    FIRMS_MAP_KEY,
    RAW_FIRMS_DIR,
    PROCESSED_CALIBRATED_DIR,
)
from downloaders.firms_downloader import FIRMSDownloader
from downloaders.gibs_downloader import GIBSDownloader
from downloaders.s3_viirs_crawler import S3VIIRSCrawler
from filters.quality_filter import filter_active_fires
from filters.coincident_filter import extract_coincident_pairs, save_coincident_pairs
from calibration.eqm_model import CalibrationModel, apply_eqm_to_modis

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PipelineOrchestrator")


def run_full_pipeline(
    region_key: str = "INDOCHINA",
    map_key: str = None,
    day_range: int = 1,
    date_str: str = "2023-03-15",
    download_imagery: bool = True,
    sample_s3: bool = False,
):
    print("\n" + "=" * 70)
    print(f"🔥 FIREHARMONIZE - MEMBER A PIPELINE EXECUTION ({region_key})")
    print(f"📅 Target Date: {date_str or 'recent'} | Day Range: {day_range}")
    print("=" * 70 + "\n")

    region_cfg = HOTSPOT_REGIONS.get(region_key, HOTSPOT_REGIONS["INDOCHINA"])
    bbox = region_cfg["bbox"]
    biome_id = region_cfg["default_biome"]
    key = map_key or FIRMS_MAP_KEY

    # -------------------------------------------------------------
    # STEP 1: Download Real NASA Active Fire Data
    # -------------------------------------------------------------
    logger.info(f"[STEP 1/5] Acquiring real active fire observations for {region_key} from NASA FIRMS...")
    firms = FIRMSDownloader(map_key=key)

    # Choose source stream based on date (SP for historical <= 2026-08, NRT for recent)
    is_historical = bool(date_str and date_str <= "2026-08-31")
    viirs_src = "VIIRS_SNPP_SP" if is_historical else "VIIRS_NOAA20_NRT"
    modis_src = "MODIS_SP" if is_historical else "MODIS_NRT"

    logger.info(f"Querying {viirs_src} and {modis_src}...")
    v_df = firms.download_area_hotspots(viirs_src, bbox=bbox, day_range=day_range, date_str=date_str)
    m_df = firms.download_area_hotspots(modis_src, bbox=bbox, day_range=day_range, date_str=date_str)
    raw_df = pd.concat([v_df, m_df], ignore_index=True)
    firms.save_to_disk(raw_df, region_key, f"REAL_{date_str or 'NRT'}")

    # -------------------------------------------------------------
    # STEP 2: Quality Filtering
    # -------------------------------------------------------------
    logger.info("[STEP 2/5] Applying confidence and sensor quality thresholds...")
    clean_df = filter_active_fires(raw_df)
    clean_path = RAW_FIRMS_DIR / f"{region_key}_clean_fire_events.parquet"
    clean_df.to_parquet(clean_path, index=False)
    logger.info(f"Saved clean events to {clean_path}")

    # -------------------------------------------------------------
    # STEP 3: Coincident Overpass Extraction (13:30 Local Solar Time)
    # -------------------------------------------------------------
    logger.info("[STEP 3/5] Extracting coincident overpasses (Δt <= 30m, Δd <= 1000m)...")
    pairs_df = extract_coincident_pairs(clean_df)
    pairs_df["biome_id"] = biome_id
    save_coincident_pairs(pairs_df, region_key)

    # -------------------------------------------------------------
    # STEP 4: Calibration Model (EQM + FRP Scaling)
    # -------------------------------------------------------------
    logger.info("[STEP 4/5] Training Empirical Quantile Mapping & FRP Power Scaling...")
    cal_model = CalibrationModel()
    lookup_df = cal_model.train_biome_calibration(pairs_df, default_biome_id=biome_id)
    lookup_path = cal_model.save_calibration_lookup(lookup_df)

    # Quick test demonstration of EQM conversion:
    test_modis_count = 10
    converted_viirs = apply_eqm_to_modis(test_modis_count, biome_id=biome_id, lookup_df=lookup_df)
    logger.info(f">> Test EQM Harmonization: {test_modis_count} MODIS fires in Biome {biome_id} -> {round(converted_viirs, 1)} VIIRS-equivalent fires")

    # -------------------------------------------------------------
    # STEP 5: NASA GIBS TrueColor Satellite Imagery
    # -------------------------------------------------------------
    if download_imagery:
        logger.info("[STEP 5/5] Downloading NASA GIBS WMS true-color satellite imagery...")
        gibs = GIBSDownloader()
        try:
            # 15 March 2023 dry season in Indochina
            date_str = "2023-03-15"
            m_img, v_img = gibs.download_comparison_pair(
                bbox=bbox,
                date_str=date_str,
                prefix=f"{region_key.lower()}",
                width=1000,
                height=750,
            )
            logger.info(f">> Downloaded Aqua MODIS: {m_img}")
            logger.info(f">> Downloaded Suomi-NPP VIIRS: {v_img}")
        except Exception as e:
            logger.error(f"GIBS imagery download skipped: {e}")

    # -------------------------------------------------------------
    # Optional STEP 6: AWS S3 Inspection
    # -------------------------------------------------------------
    if sample_s3:
        logger.info("[OPTIONAL] Inspecting NOAA-21 VIIRS AWS S3 public bucket...")
        s3 = S3VIIRSCrawler()
        items = s3.list_objects(prefix="VIIRS-", max_keys=5)
        for item in items:
            logger.info(f"S3 Object: {item['key']} ({item['size_mb']} MB)")

    print("\n" + "=" * 70)
    print("✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"📦 Calibration Lookup Table: {lookup_path}")
    print(f"📦 Filtered Fire Events:     {clean_path}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FireHarmonize Member A Pipeline")
    parser.add_argument("--region", default="INDOCHINA", choices=list(HOTSPOT_REGIONS.keys()))
    parser.add_argument("--map-key", default=None, help="NASA FIRMS MAP_KEY")
    parser.add_argument("--date", default="2023-03-15", help="Observation date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=1, help="Day range (1 to 5)")
    parser.add_argument("--no-images", action="store_true", help="Skip GIBS WMS imagery download")
    parser.add_argument("--check-s3", action="store_true", help="Inspect AWS S3 bucket")
    
    args = parser.parse_args()
    run_full_pipeline(
        region_key=args.region,
        map_key=args.map_key,
        date_str=args.date,
        day_range=args.days,
        download_imagery=not args.no_images,
        sample_s3=args.check_s3,
    )

