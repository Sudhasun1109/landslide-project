import pandas as pd
import rasterio

# Input files
csv_file = "meghalaya_dem_features.csv"
tif_file = "rainfall/20240713.tif"

# Load landslide data
df = pd.read_csv(csv_file)

print("Total records:", len(df))

rainfall_values = []

# Open rainfall TIFF
with rasterio.open(tif_file) as src:

    print("Rainfall raster opened!")
    print("CRS:", src.crs)
    print("Resolution:", src.res)

    for _, row in df.iterrows():

        latitude = row["Latitude"]
        longitude = row["Longitude"]

        try:
            value = list(
                src.sample([(longitude, latitude)])
            )[0][0]

            # IMERG 1-day GIS product scaling
            rainfall = float(value) / 10.0

            rainfall_values.append(rainfall)

        except Exception:
            rainfall_values.append(None)

# Add rainfall
df["Rainfall_mm"] = rainfall_values

# Save
output_file = "meghalaya_complete_dataset.csv"
df.to_csv(output_file, index=False)

print("\nSUCCESS!")
print("Output:", output_file)
print("Records:", len(df))

print("\nSample:")
print(
    df[
        [
            "Latitude",
            "Longitude",
            "Elevation_m",
            "Slope_deg",
            "Rainfall_mm"
        ]
    ].head(10)
)

print("\nMissing rainfall:", df["Rainfall_mm"].isna().sum())

print("\nRainfall statistics:")
print(df["Rainfall_mm"].describe())
