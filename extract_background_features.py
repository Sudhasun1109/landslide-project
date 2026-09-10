import pandas as pd
import rasterio
import numpy as np

INPUT_FILE = "background_points.csv"
DEM_FILE = "data/meghalaya_dem.tif"
OUTPUT_FILE = "background_features.csv"

# Load background points
df = pd.read_csv(INPUT_FILE)

print("Background points:", len(df))

with rasterio.open(DEM_FILE) as src:

    dem = src.read(1).astype(float)

    # DEM resolution
    xres = src.res[0]
    yres = src.res[1]

    # Approximate metres per pixel
    pixel_size = ((xres + yres) / 2) * 111320

    # Calculate slope
    dy, dx = np.gradient(
        dem,
        pixel_size,
        pixel_size
    )

    slope = np.degrees(
        np.arctan(
            np.sqrt(dx**2 + dy**2)
        )
    )

    elevations = []
    slopes = []

    for _, row in df.iterrows():

        lat = row["Latitude"]
        lon = row["Longitude"]

        # Get raster position
        r, c = src.index(lon, lat)

        elevation = dem[r, c]
        slope_value = slope[r, c]

        elevations.append(float(elevation))
        slopes.append(float(slope_value))

# Add features
df["Elevation_m"] = elevations
df["Slope_deg"] = slopes

# Save
df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nSUCCESS!")
print("Output:", OUTPUT_FILE)
print("Records:", len(df))

print("\nMissing values:")
print(df.isna().sum())

print("\nSample:")
print(df.head(10).to_string(index=False))

print("\nElevation statistics:")
print(df["Elevation_m"].describe())

print("\nSlope statistics:")
print(df["Slope_deg"].describe())