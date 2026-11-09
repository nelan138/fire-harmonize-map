"""
FireHarmonize - Member A
NASA FIRMS Country Yearly Summary Downloader
Fetches full historical time series (2000-2025) for target study countries
Directly from NASA FIRMS Open Data Archive:
https://firms.modaps.eosdis.nasa.gov/data/country/
"""

import sys
from pathlib import Path
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import io
import requests
import pandas as pd

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DATA_DIR, RAW_FIRMS_DIR
from filters.quality_filter import filter_active_fires

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CountryDownloader")

FIRMS_COUNTRY_BASE = "https://firms.modaps.eosdis.nasa.gov/data/country"
COUNTRY_ARCHIVE_DIR = RAW_FIRMS_DIR / "country_archive"
COUNTRY_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def download_single_year(instrument: str, year: int, country: str, dest_dir: Path) -> Path | None:
    """Download a single yearly CSV file for a given instrument and country."""
    # NASA FIRMS naming convention:
    # modis_{year}_{country}.csv
    # viirs-snpp_{year}_{country}.csv
    # viirs-jpss1_{year}_{country}.csv
    filename = f"{instrument}_{year}_{country}.csv"
    url = f"{FIRMS_COUNTRY_BASE}/{filename}"
    out_path = dest_dir / filename

    if out_path.exists() and out_path.stat().st_size > 1000:
        logger.info(f"Already downloaded: {filename}")
        return out_path

    try:
        resp = requests.get(url, timeout=45)
        if resp.status_code == 200 and len(resp.content) > 200:
            out_path.write_bytes(resp.content)
            logger.info(f"Downloaded {filename} ({round(len(resp.content)/1024, 1)} KB)")
            return out_path
        elif resp.status_code == 404:
            logger.warning(f"File not found on FIRMS: {filename}")
            return None
        else:
            logger.warning(f"Failed {filename} with HTTP {resp.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error downloading {filename}: {e}")
        return None


def download_country_history(country: str = "Vietnam", start_year: int = 2000, end_year: int = 2024) -> Path:
    """
    Downloads complete MODIS (2000-2024) and VIIRS S-NPP (2012-2024) for a country,
    applies quality filter, and consolidates into a single Parquet file.
    """
    dest_dir = COUNTRY_ARCHIVE_DIR / country.lower()
    dest_dir.mkdir(parents=True, exist_ok=True)

    tasks = []
    # 1. MODIS: 2000 to end_year
    for yr in range(start_year, end_year + 1):
        tasks.append(("modis", yr))

    # 2. VIIRS S-NPP: 2012 to end_year
    for yr in range(2012, end_year + 1):
        tasks.append(("viirs-snpp", yr))

    logger.info(f"Initiating batch download for {country}: {len(tasks)} yearly archives...")
    downloaded_files = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_map = {
            executor.submit(download_single_year, inst, yr, country, dest_dir): (inst, yr)
            for inst, yr in tasks
        }
        for future in as_completed(future_map):
            res = future.result()
            if res:
                downloaded_files.append(res)

    logger.info(f"Successfully retrieved {len(downloaded_files)}/{len(tasks)} files for {country}.")

    # Consolidate into clean master dataframe
    logger.info("Consolidating and filtering active fire records...")
    dfs = []
    for f in sorted(downloaded_files):
        try:
            temp_df = pd.read_csv(f)
            # Add instrument identification if needed
            inst_str = "MODIS" if "modis" in f.name else "VIIRS"
            sat_str = "Terra/Aqua" if "modis" in f.name else "Suomi-NPP"
            if "instrument" not in temp_df.columns:
                temp_df["instrument"] = inst_str
            if "satellite" not in temp_df.columns:
                temp_df["satellite"] = sat_str
            dfs.append(temp_df)
        except Exception as e:
            logger.error(f"Error reading {f}: {e}")

    if not dfs:
        raise RuntimeError("No data was parsed!")

    full_df = pd.concat(dfs, ignore_index=True)
    logger.info(f"Total raw records loaded: {len(full_df):,}")

    # Standardize column names
    full_df.columns = [c.lower() for c in full_df.columns]

    # Type casting
    full_df["latitude"] = pd.to_numeric(full_df["latitude"], errors="coerce")
    full_df["longitude"] = pd.to_numeric(full_df["longitude"], errors="coerce")
    if "frp" in full_df.columns:
        full_df["frp"] = pd.to_numeric(full_df["frp"], errors="coerce").fillna(0.0)
    # Type casting
    full_df["latitude"] = pd.to_numeric(full_df["latitude"], errors="coerce")
    full_df["longitude"] = pd.to_numeric(full_df["longitude"], errors="coerce")
    full_df["confidence"] = full_df["confidence"].astype(str)
    if "frp" in full_df.columns:
        full_df["frp"] = pd.to_numeric(full_df["frp"], errors="coerce").fillna(0.0)
    else:
        full_df["frp"] = 0.0

    clean_df = filter_active_fires(full_df)
    clean_df["confidence"] = clean_df["confidence"].astype(str)
    clean_df["country"] = country
    clean_df["region_id"] = "INDOCHINA"
    clean_df["biome_id"] = 1  # Forest & Agro-forestry complex

    out_parquet = RAW_FIRMS_DIR / f"{country.upper()}_25YR_clean_fire_events.parquet"
    clean_df.to_parquet(out_parquet, index=False)
    logger.info(f"Saved {len(clean_df):,} clean 25-year fire events to: {out_parquet}")
    return out_parquet


if __name__ == "__main__":
    download_country_history("Vietnam", 2000, 2024)
