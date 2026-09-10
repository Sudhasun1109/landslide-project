import pandas as pd
import rasterio
import numpy as np
from pathlib import Path

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

CSV_FILE = "meghalaya_ml_base_clean.csv"
RAINFALL_FOLDER = Path("rainfall_monthly")

# --------------------------------------------------
# LOAD LANDSLIDE DATA
# --------------------------------------------------

df = pd.read_csv(CSV_FILE)

# Keep only records with a valid year
df = df.dropna(subset=["History_Year"]).copy()

df["History_Year"] = df["History_Year"].astype(int)

print("Records with valid year:", len(df))

print("\nYears:")
print(sorted(df["History_Year"].unique()))

# --------------------------------------------------
# FUNCTION TO EXTRACT RAINFALL
# --------------------------------------------------

def get_rainfall(tif_file, latitude, longitude):

    with rasterio.open(tif_file) as src:

        value = list(
            src.sample([(longitude, latitude)])
        )[0][0]

        # Monthly Final IMERG GIS:
        # values are already in approximately 1 mm units
        if src.nodata is not None and value == src.nodata:
            return np.nan

        return float(value)


# --------------------------------------------------
# TEST ONE FILE
# --------------------------------------------------

print("\nChecking rainfall folder...")

files = list(RAINFALL_FOLDER.glob("*.tif"))

print("Monthly TIFF files found:", len(files))

if len(files) == 0:

    print("\nNo monthly rainfall files found!")

    print("Create this folder:")
    print("rainfall_monthly")

    print("\nThen put the monthly IMERG TIFF files inside it.")

    exit()


# --------------------------------------------------
# EXAMPLE EXTRACTION
# --------------------------------------------------

sample_file = files[0]

print("\nTesting file:")
print(sample_file)

sample_lat = df.iloc[0]["Latitude"]
sample_lon = df.iloc[0]["Longitude"]

rainfall = get_rainfall(
    sample_file,
    sample_lat,
    sample_lon
)

print("\nSample coordinate:")
print("Latitude:", sample_lat)
print("Longitude:", sample_lon)

print("Rainfall:", rainfall, "mm")