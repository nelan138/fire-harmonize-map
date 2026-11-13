"""
FireHarmonize - Member A
NASA FIRMS Active Fire Downloader (MODIS & VIIRS)
Supports querying the NASA FIRMS Area API and parsing active fire detection CSVs.
"""

import sys
from pathlib import Path
import io
import time
import logging
import requests
import pandas as pd

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import FIRMS_MAP_KEY, HOTSPOT_REGIONS, RAW_FIRMS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("FIRMSDownloader")

FIRMS_API_BASE = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"


class FIRMSDownloader:
    def __init__(self, map_key: str = None):
        self.map_key = map_key or FIRMS_MAP_KEY
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "FireHarmonize-Research/1.0 (NASA Space Apps)"})

    def download_area_hotspots(
        self,
        source: str,
        bbox: list[float],
        day_range: int = 1,
        date_str: str = None,
        timeout: int = 30,
    ) -> pd.DataFrame:
        """
        Download active fire points for a specific bounding box from NASA FIRMS API.
        
        Parameters:
            source: e.g. 'VIIRS_SNPP_NRT', 'MODIS_NRT', 'VIIRS_NOAA20_NRT', 'MODIS_SP'
            bbox: [min_lon, min_lat, max_lon, max_lat]
            day_range: 1 to 10 days
            date_str: 'YYYY-MM-DD' (optional)
        """
        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
        
        # Build URL
        if date_str:
            url = f"{FIRMS_API_BASE}/{self.map_key}/{source}/{bbox_str}/{day_range}/{date_str}"
        else:
            url = f"{FIRMS_API_BASE}/{self.map_key}/{source}/{bbox_str}/{day_range}"

        logger.info(f"Querying FIRMS API: source={source}, bbox={bbox_str}, day_range={day_range}, date={date_str or 'recent'}")
        
        resp = self.session.get(url, timeout=timeout)
        
        if resp.status_code != 200:
            error_msg = resp.text.strip()
            logger.error(f"FIRMS API Error ({resp.status_code}): {error_msg}")
            raise RuntimeError(f"FIRMS API failed with status {resp.status_code}: {error_msg}")

        # The response is CSV text
        csv_text = resp.text.strip()
        if not csv_text or csv_text.startswith("Invalid MAP_KEY"):
            raise ValueError(f"FIRMS API error or invalid response: {csv_text}")

        # Parse CSV into pandas DataFrame
        df = pd.read_csv(io.StringIO(csv_text))
        logger.info(f"Successfully retrieved {len(df)} active fire records from {source}")
        
        # Standardize columns
        df = self._standardize_schema(df, source)
        return df

    def _standardize_schema(self, df: pd.DataFrame, source: str) -> pd.DataFrame:
        """Standardize column names and types across MODIS and VIIRS"""
        if df.empty:
            return df
        
        # Lowercase all column names
        df.columns = [c.lower() for c in df.columns]

        # Ensure required columns exist
        if "latitude" not in df.columns or "longitude" not in df.columns:
            logger.warning("Dataframe missing lat/lon columns!")
            return df

        # Fill sensor info if missing
        if "instrument" not in df.columns:
            df["instrument"] = "MODIS" if "MODIS" in source else "VIIRS"
        if "satellite" not in df.columns:
            if "SNPP" in source:
                df["satellite"] = "Suomi-NPP"
            elif "NOAA20" in source:
                df["satellite"] = "NOAA-20"
            elif "NOAA21" in source:
                df["satellite"] = "NOAA-21"
            elif "MODIS" in source:
                df["satellite"] = "Aqua/Terra"

        # Type casts
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
        if "confidence" in df.columns:
            df["confidence"] = df["confidence"].astype(str)
        if "frp" in df.columns:
            df["frp"] = pd.to_numeric(df["frp"], errors="coerce").fillna(0.0)
        else:
            df["frp"] = 0.0

        return df

    def save_to_disk(self, df: pd.DataFrame, region_key: str, source: str, label: str = "") -> Path:
        """Save raw downloaded dataframe to CSV and Parquet"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename_base = f"{region_key}_{source}_{label}_{timestamp}".strip("_")
        
        csv_path = RAW_FIRMS_DIR / f"{filename_base}.csv"
        parquet_path = RAW_FIRMS_DIR / f"{filename_base}.parquet"
        
        df.to_csv(csv_path, index=False)
        df.to_parquet(parquet_path, index=False)
        logger.info(f"Saved {len(df)} records to:\n  -> {csv_path}\n  -> {parquet_path}")
        return parquet_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download active fire data from NASA FIRMS API")
    parser.add_argument("--region", default="INDOCHINA", choices=list(HOTSPOT_REGIONS.keys()))
    parser.add_argument("--source", default="VIIRS_NOAA20_NRT")
    parser.add_argument("--days", type=int, default=1)
    parser.add_argument("--date", default=None)
    parser.add_argument("--map-key", default=None)
    
    args = parser.parse_args()
    downloader = FIRMSDownloader(map_key=args.map_key)
    bbox = HOTSPOT_REGIONS[args.region]["bbox"]
    
    df = downloader.download_area_hotspots(
        source=args.source,
        bbox=bbox,
        day_range=args.days,
        date_str=args.date,
    )
    downloader.save_to_disk(df, args.region, args.source)
