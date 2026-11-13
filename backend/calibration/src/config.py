"""
FireHarmonize - Member A (Physics & Calibration)
Configuration module for satellite data download, coincident overpass filtering, and calibration.
"""

from pathlib import Path
import os

# Base paths
SRC_DIR = Path(__file__).resolve().parent
VIIRS_DIR = SRC_DIR.parent
DATA_DIR = VIIRS_DIR / "data"

RAW_FIRMS_DIR = DATA_DIR / "raw" / "firms"
RAW_IMAGERY_DIR = DATA_DIR / "raw" / "imagery"
PROCESSED_COINCIDENT_DIR = DATA_DIR / "processed" / "coincident_pairs"
PROCESSED_CALIBRATED_DIR = DATA_DIR / "processed" / "calibrated"

for p in [RAW_FIRMS_DIR, RAW_IMAGERY_DIR, PROCESSED_COINCIDENT_DIR, PROCESSED_CALIBRATED_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# NASA FIRMS API Key
# Set via environment variable FIRMS_MAP_KEY or update here
FIRMS_MAP_KEY = os.getenv("FIRMS_MAP_KEY", "e89c5ce8ee535299671d20ea5e2dffb6")

# Target Study Hotspots (BBOX format: [min_lon, min_lat, max_lon, max_lat])
HOTSPOT_REGIONS = {
    "INDOCHINA": {
        "name": "Tay Nguyen & Lower Mekong (Vietnam/Laos/Cambodia)",
        "bbox": [100.0, 10.0, 110.0, 22.0],
        "default_biome": 1,  # Tropical moist/dry deciduous forest & agro complex
    },
    "AMAZON": {
        "name": "Amazon Basin (Brazil)",
        "bbox": [-74.0, -15.0, -44.0, 5.0],
        "default_biome": 1,  # Dense Tropical Rainforest
    },
    "CALIFORNIA": {
        "name": "California (USA)",
        "bbox": [-125.0, 32.0, -114.0, 42.5],
        "default_biome": 4,  # Shrubland / Chaparral & Temperate Forest
    },
    "PANTANAL": {
        "name": "Pantanal Wetland (Brazil/Bolivia)",
        "bbox": [-60.0, -22.5, -55.0, -15.5],
        "default_biome": 2,  # Flooded Grasslands & Savanna
    },
    "SE_AUSTRALIA": {
        "name": "South-East Australia",
        "bbox": [140.0, -40.0, 154.0, -28.0],
        "default_biome": 2,  # Temperate Eucalyptus & Savanna
    },
}

# FIRMS Sensor Sources
FIRMS_SOURCES = {
    "MODIS_NRT": "MODIS Near Real Time (1km)",
    "MODIS_SP": "MODIS Standard Quality MCD14ML (1km)",
    "VIIRS_SNPP_NRT": "VIIRS Suomi-NPP Near Real Time (375m)",
    "VIIRS_SNPP_SP": "VIIRS Suomi-NPP Standard Quality VNP14IMGTDL (375m)",
    "VIIRS_NOAA20_NRT": "VIIRS NOAA-20 Near Real Time (375m)",
    "VIIRS_NOAA21_NRT": "VIIRS NOAA-21 Near Real Time (375m)",
}

# Filtering & Quality Thresholds (Standardized: Δd <= 1,000m nadir pixel, Δt <= 30min daytime overpass)
FILTER_CONFIG = {
    "modis_min_confidence": 30,         # Filter out MODIS confidence < 30%
    "viirs_drop_confidence": ["low"],   # Filter out VIIRS confidence = 'low' (keep nominal, high)
    "coincident_max_distance_m": 1000.0, # Max spatial distance between Aqua and VIIRS (meters)
    "coincident_max_time_diff_min": 30.0,# Max acquisition time difference (minutes - Aqua vs S-NPP afternoon pass)
    "require_daytime": True,             # Enforce daytime overpasses (daynight == 'D')
}

# Biome definitions matching MCD12Q1 aggregation in FIREHARMONIZE_7DAYS_PLAN.md
BIOMES = {
    1: "Dense Forests (Tropical & Temperate)",
    2: "Savanna & Grasslands",
    3: "Croplands (Agricultural burning)",
    4: "Shrublands & Chaparral",
}

