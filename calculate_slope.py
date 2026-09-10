import pandas as pd
import rasterio
import numpy as np

# Files
csv_file = "meghalaya_dem_dataset.csv"
dem_file = "data/N25E092.hgt"

# Load dataset
df = pd.read_csv(csv_file)

print("Records:", len(df))

with rasterio.open(dem_file) as src:

    # Read DEM
    elevation = src.read(1).astype(float)

    # Pixel size in degrees
    pixel_size = src.res[0]

    # Convert degrees approximately to meters
    meter_per_degree = 111320
    pixel_size_m = pixel_size * meter_per_degree

    # Calculate elevation gradients
    dz_dy, dz_dx = np.gradient(elevation, pixel_size_m)

    # Calculate slope in degrees
    slope = np.degrees(
        np.arctan(
            np.sqrt(dz_dx**2 + dz_dy**2)
        )
    )

    slopes = []

    for _, row in df.iterrows():

        latitude = row["Latitude"]
        longitude = row["Longitude"]

        try:
            # Convert coordinate to raster row/column
            row_idx, col_idx = src.index(longitude, latitude)

            value = slope[row_idx, col_idx]

            slopes.append(float(value))

        except Exception:
            slopes.append(None)

# Add slope
df["Slope_deg"] = slopes

# Save
output_file = "meghalaya_dem_features.csv"
df.to_csv(output_file, index=False)

print("\nSUCCESS!")
print("Output:", output_file)
print("Records:", len(df))

print("\nSample:")
print(
    df[
        ["Latitude", "Longitude", "Elevation_m", "Slope_deg"]
    ].head(10)
)

print("\nMissing slope:", df["Slope_deg"].isna().sum())

print("\nSlope statistics:")
print(df["Slope_deg"].describe())