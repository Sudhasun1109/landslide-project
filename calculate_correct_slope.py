import pandas as pd
import rasterio
import numpy as np

INPUT_FILE = "meghalaya_elevation_dataset.csv"
DEM_FILE = "data/meghalaya_dem.tif"
OUTPUT_FILE = "meghalaya_dem_final.csv"

df = pd.read_csv(INPUT_FILE)

print("Total records:", len(df))

with rasterio.open(DEM_FILE) as src:

    dem = src.read(1).astype(float)

    # Pixel size in degrees
    xres = src.res[0]
    yres = src.res[1]

    # Convert approximately to metres
    # 1 degree latitude ≈ 111,320 m
    pixel_size = ((xres + yres) / 2) * 111320

    # Calculate elevation gradients
    dy, dx = np.gradient(dem, pixel_size, pixel_size)

    # Calculate slope in degrees
    slope = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))

    slopes = []

    for _, row in df.iterrows():

        lat = row["Latitude"]
        lon = row["Longitude"]

        # Convert coordinate to raster row/column
        row_idx, col_idx = src.index(lon, lat)

        value = slope[row_idx, col_idx]

        slopes.append(float(value))

df["Slope_deg"] = slopes

# Save final DEM dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nSUCCESS!")
print("Output:", OUTPUT_FILE)
print("Records:", len(df))

print("\nSlope statistics:")
print(df["Slope_deg"].describe())

print("\nSample:")
print(
    df[
        ["Latitude", "Longitude", "Elevation_m", "Slope_deg"]
    ].head(10).to_string(index=False)
)

print("\nMissing slope:", df["Slope_deg"].isna().sum())