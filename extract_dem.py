import pandas as pd
import rasterio

# Input files
csv_file = "meghalaya_ml_base_clean.csv"
dem_file = "data/N25E092.hgt"

# Load landslide dataset
df = pd.read_csv(csv_file)

print("Landslide records:", len(df))

# Open DEM
with rasterio.open(dem_file) as src:

    elevations = []

    for _, row in df.iterrows():

        latitude = row["Latitude"]
        longitude = row["Longitude"]

        try:
            elevation = list(
                src.sample([(longitude, latitude)])
            )[0][0]

            elevations.append(float(elevation))

        except Exception:
            elevations.append(None)

# Add elevation column
df["Elevation_m"] = elevations

# Save result
output_file = "meghalaya_dem_dataset.csv"
df.to_csv(output_file, index=False)

print("\nSUCCESS!")
print("Output file:", output_file)
print("Records:", len(df))

print("\nElevation sample:")
print(df[["Latitude", "Longitude", "Elevation_m"]].head(10))

print("\nMissing elevation:", df["Elevation_m"].isna().sum())