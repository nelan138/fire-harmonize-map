"""Build monthly H3-6 detection counts for the web density API (no calibration)."""

import argparse
from pathlib import Path

import h3
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"


def aggregate_h3_monthly(events: pd.DataFrame) -> pd.DataFrame:
    events = events.copy()
    valid = events.latitude.between(-90, 90) & events.longitude.between(-180, 180)
    if not valid.all():
        raise ValueError("Input contains missing or invalid coordinates")
    dates = pd.to_datetime(events.acq_date, errors="raise")
    if dates.isna().any() or events[["region_id", "biome_id"]].isna().any().any():
        raise ValueError("Input contains missing dates, regions or biomes")
    events["year"] = dates.dt.year
    events["month"] = dates.dt.month
    events["h3_index"] = [
        h3.latlng_to_cell(lat, lon, 6)
        for lat, lon in zip(events.latitude, events.longitude)
    ]
    monthly = events.groupby(
        ["region_id", "year", "month", "biome_id", "h3_index"], as_index=False
    ).agg(fire_count=("h3_index", "size"), frp_mw=("frp", "sum"))
    centers = {cell: h3.cell_to_latlng(cell) for cell in monthly.h3_index.unique()}
    monthly["lat_centroid"] = monthly.h3_index.map(lambda cell: centers[cell][0])
    monthly["lon_centroid"] = monthly.h3_index.map(lambda cell: centers[cell][1])
    # Average H3-6 hexagon area, not the exact area of each cell.
    monthly["area_km2"] = h3.average_hexagon_area(6, unit="km^2")
    monthly["density_per_km2"] = monthly["fire_count"] / monthly["area_km2"]
    return monthly


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DATA / "raw/firms/VIETNAM_25YR_clean_fire_events.parquet")
    parser.add_argument("--output", type=Path, default=DATA / "processed/calibrated/fire_density_h3_monthly.parquet")
    args = parser.parse_args()
    events = pd.read_parquet(args.input, columns=[
        "latitude", "longitude", "acq_date", "region_id", "biome_id", "frp",
    ])
    monthly = aggregate_h3_monthly(events)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    monthly.to_parquet(args.output, index=False)
    print(f"{len(events):,} detections -> {len(monthly):,} monthly H3-6 rows: {args.output}")


if __name__ == "__main__":
    main()
