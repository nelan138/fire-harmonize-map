"""
FireHarmonize - Member A
NASA GIBS (Global Imagery Browse Services) WMS Imagery Downloader
Downloads high-resolution TrueColor satellite imagery and active fire thermal overlays.
Does NOT require an API key or NASA Earthdata login!
"""

import sys
from pathlib import Path
import logging
import requests
from urllib.parse import urlencode

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RAW_IMAGERY_DIR, HOTSPOT_REGIONS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GIBSDownloader")

GIBS_WMS_BASE = "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"

# GIBS Layer catalog
GIBS_LAYERS = {
    "modis_truecolor": "MODIS_Aqua_CorrectedReflectance_TrueColor",
    "modis_fires": "MODIS_Combined_Thermal_Anomalies_Day",
    "viirs_truecolor": "VIIRS_SNPP_CorrectedReflectance_TrueColor",
    "viirs_fires": "VIIRS_SNPP_Thermal_Anomalies_375m_All",
    "blue_marble": "BlueMarble_NextGeneration",
    "coastlines": "Coastlines_15m",
}


class GIBSDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "FireHarmonize-Satellite-Crawler/1.0"})

    def fetch_wms_image(
        self,
        layers: list[str],
        bbox: list[float],
        date_str: str,
        width: int = 1200,
        height: int = 800,
        img_format: str = "image/jpeg",
        transparent: bool = False,
    ) -> bytes:
        """
        Fetch composite satellite image from NASA GIBS WMS.
        
        Parameters:
            layers: List of layer names in order of rendering (e.g. ['BlueMarble_NextGeneration', 'VIIRS_SNPP_Thermal_Anomalies_375m_All'])
            bbox: [min_lon, min_lat, max_lon, max_lat] in EPSG:4326
            date_str: 'YYYY-MM-DD'
            width, height: Pixel dimensions of output image
            img_format: 'image/jpeg' or 'image/png'
        """
        # GIBS EPSG:4326 WMS standard: BBOX is min_lon,min_lat,max_lon,max_lat (or min_lat,min_lon in WMS 1.3.0)
        # Using WMS 1.1.1 avoids axis-order ambiguity
        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
        layers_str = ",".join(layers)

        params = {
            "service": "WMS",
            "request": "GetMap",
            "version": "1.1.1",
            "layers": layers_str,
            "styles": "",
            "format": img_format,
            "transparent": "TRUE" if transparent else "FALSE",
            "srs": "EPSG:4326",
            "bbox": bbox_str,
            "width": width,
            "height": height,
            "time": date_str,
        }

        full_url = f"{GIBS_WMS_BASE}?{urlencode(params)}"
        logger.info(f"Requesting GIBS WMS: layers=[{layers_str}], time={date_str}, bbox={bbox_str}")

        resp = self.session.get(full_url, timeout=45)
        if resp.status_code != 200:
            raise RuntimeError(f"GIBS WMS request failed ({resp.status_code}): {resp.text[:200]}")

        # Check if returned content is XML error instead of image
        content_type = resp.headers.get("Content-Type", "")
        if "xml" in content_type.lower():
            raise ValueError(f"GIBS returned XML service exception: {resp.text[:300]}")

        return resp.content

    def download_comparison_pair(
        self,
        bbox: list[float],
        date_str: str,
        prefix: str = "satellite_pair",
        width: int = 1200,
        height: int = 900,
    ) -> tuple[Path, Path]:
        """
        Download both Aqua MODIS and Suomi-NPP VIIRS comparison images for a given date and AOI.
        Matches Figure 1 in the project plan.
        """
        # 1. MODIS Aqua Pair (TrueColor + Fires)
        modis_layers = [GIBS_LAYERS["modis_truecolor"], GIBS_LAYERS["modis_fires"]]
        modis_bytes = self.fetch_wms_image(modis_layers, bbox, date_str, width, height)
        modis_path = RAW_IMAGERY_DIR / f"{prefix}_MODIS_Aqua_{date_str}.jpg"
        modis_path.write_bytes(modis_bytes)
        logger.info(f"Saved Aqua MODIS imagery to {modis_path}")

        # 2. VIIRS Suomi-NPP Pair (TrueColor + Fires 375m)
        viirs_layers = [GIBS_LAYERS["viirs_truecolor"], GIBS_LAYERS["viirs_fires"]]
        viirs_bytes = self.fetch_wms_image(viirs_layers, bbox, date_str, width, height)
        viirs_path = RAW_IMAGERY_DIR / f"{prefix}_VIIRS_SNPP_{date_str}.jpg"
        viirs_path.write_bytes(viirs_bytes)
        logger.info(f"Saved VIIRS Suomi-NPP imagery to {viirs_path}")

        return modis_path, viirs_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download satellite imagery from NASA GIBS WMS")
    parser.add_argument("--region", default="INDOCHINA", choices=list(HOTSPOT_REGIONS.keys()))
    parser.add_argument("--date", default="2023-03-15", help="Observation date (YYYY-MM-DD)")
    parser.add_argument("--width", type=int, default=1000)
    parser.add_argument("--height", type=int, default=800)
    args = parser.parse_args()

    downloader = GIBSDownloader()
    bbox = HOTSPOT_REGIONS[args.region]["bbox"]
    logger.info(f"Fetching GIBS comparison for {args.region} on {args.date}...")
    try:
        modis_file, viirs_file = downloader.download_comparison_pair(
            bbox=bbox,
            date_str=args.date,
            prefix=f"{args.region.lower()}",
            width=args.width,
            height=args.height,
        )
        print(f"\n[SUCCESS] Downloaded satellite comparison images:\n1. {modis_file}\n2. {viirs_file}")
    except Exception as e:
        logger.error(f"Failed to fetch GIBS imagery: {e}")

