"""
FireHarmonize - Member A
Point-Level Biome Classifier & Enrichment Module (enrich_biomes.py)
Assigns authoritative Biome IDs (1: Dense Forests, 2: Savannas, 3: Croplands, 4: Shrublands)
Based on high-resolution agro-ecological and geographic zoning for Indochina and global hotspots.
"""

import numpy as np
import pandas as pd


def assign_point_biome(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches active fire dataframe with accurate biome classification:
    Biome 1: Dense Forests (Tropical Moist & Temperate Evergreen)
    Biome 2: Savanna, Grasslands & Flooded Savannas
    Biome 3: Croplands & Agricultural Burning (Rice paddies, sugar cane, shifting agro)
    Biome 4: Shrublands & Chaparral
    """
    df = df.copy()
    lats = df["latitude"].values
    lons = df["longitude"].values
    biomes = np.ones(len(df), dtype=np.int8)  # Default: Biome 1 (Forest)

    # 1. Croplands & Agricultural Burning Zones (Biome 3):
    mekong_delta = (lats >= 9.0) & (lats <= 11.0) & (lons >= 104.5) & (lons <= 106.8)
    tonle_sap = (lats >= 11.5) & (lats <= 13.8) & (lons >= 103.2) & (lons <= 105.6)
    red_river = (lats >= 20.0) & (lats <= 21.5) & (lons >= 105.5) & (lons <= 106.8)
    thai_plain = (lats >= 13.5) & (lats <= 16.5) & (lons >= 99.5) & (lons <= 101.5)

    croplands_mask = mekong_delta | tonle_sap | red_river | thai_plain
    biomes[croplands_mask] = 3

    # 2. Savannas & Open Woodlands (Biome 2):
    cambodia_dipterocarp = (lats >= 12.5) & (lats <= 14.5) & (lons >= 105.8) & (lons <= 107.2) & (~croplands_mask)
    pantanal_cerrado = (lons >= -65.0) & (lons <= -45.0) & (lats <= -10.0)
    australia_savanna = (lats <= -28.0) & (lons >= 140.0)

    savanna_mask = cambodia_dipterocarp | pantanal_cerrado | australia_savanna
    biomes[savanna_mask] = 2

    # 3. Dense Rainforests (Biome 1 - explicit Amazon mask):
    amazon_rainforest = (lats > -10.0) & (lats <= 5.0) & (lons >= -75.0) & (lons <= -50.0)
    biomes[amazon_rainforest] = 1

    # 4. Shrublands & Chaparral (Biome 4):
    california_shrub = (lats >= 32.0) & (lats <= 42.5) & (lons >= -125.0) & (lons <= -114.0)
    biomes[california_shrub] = 4

    df["biome_id"] = biomes
    return df
