"""
FireHarmonize - Member A
AWS S3 NOAA-21 VIIRS Open Data Crawler
Connects to the public AWS S3 bucket: 'noaa-nesdis-n21-pds' without credentials (anonymous access).
Allows listing and downloading NOAA-21 granules and products as referenced in VIIRS/links.txt.
"""

import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import logging
import requests

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("S3VIIRSCrawler")

S3_BUCKET_URL = "https://noaa-nesdis-n21-pds.s3.amazonaws.com"
RAW_S3_DIR = DATA_DIR / "raw" / "s3_granules"
RAW_S3_DIR.mkdir(parents=True, exist_ok=True)


class S3VIIRSCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "FireHarmonize-Crawler/1.0"})

    def list_objects(self, prefix: str = "", max_keys: int = 50) -> list[dict]:
        """
        List objects in the noaa-nesdis-n21-pds S3 bucket under a prefix.
        Uses S3 REST ListObjectsV2 API without authentication.
        """
        url = f"{S3_BUCKET_URL}/?list-type=2&prefix={prefix}&max-keys={max_keys}"
        logger.info(f"Listing S3 objects with prefix: '{prefix}'")
        resp = self.session.get(url, timeout=30)
        
        if resp.status_code != 200:
            raise RuntimeError(f"S3 request failed ({resp.status_code}): {resp.text[:200]}")

        # Parse S3 XML response
        root = ET.fromstring(resp.content)
        # S3 namespace
        ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        
        items = []
        for content in root.findall("s3:Contents", ns):
            key = content.find("s3:Key", ns).text
            size = int(content.find("s3:Size", ns).text)
            modified = content.find("s3:LastModified", ns).text
            items.append({
                "key": key,
                "size_mb": round(size / (1024 * 1024), 2),
                "last_modified": modified,
                "url": f"{S3_BUCKET_URL}/{key}",
            })
            
        logger.info(f"Found {len(items)} items under prefix '{prefix}'")
        return items

    def download_granule(self, s3_key: str, dest_dir: Path = RAW_S3_DIR) -> Path:
        """Download a specific .nc granule from S3"""
        url = f"{S3_BUCKET_URL}/{s3_key}"
        filename = Path(s3_key).name
        dest_path = dest_dir / filename

        logger.info(f"Downloading granule from S3: {url}")
        resp = self.session.get(url, stream=True, timeout=60)
        resp.raise_for_status()

        total_bytes = 0
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    total_bytes += len(chunk)

        logger.info(f"Successfully saved {round(total_bytes / (1024*1024), 2)} MB to {dest_path}")
        return dest_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Query and download NOAA-21 VIIRS from AWS S3")
    parser.add_argument("--prefix", default="VIIRS-", help="S3 prefix to search (e.g. 'VIIRS-I-BAND' or 'VIIRS-M-BAND')")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of files to list")
    parser.add_argument("--download-first", action="store_true", help="Download the first file found")
    args = parser.parse_args()

    crawler = S3VIIRSCrawler()
    items = crawler.list_objects(prefix=args.prefix, max_keys=args.limit)
    
    print("\n--- NOAA-21 S3 Bucket Contents ---")
    for idx, item in enumerate(items):
        print(f"[{idx+1}] {item['key']} ({item['size_mb']} MB) - {item['last_modified']}")

    if args.download_first and items:
        first_key = items[0]["key"]
        print(f"\nDownloading first granule: {first_key}")
        crawler.download_granule(first_key)

