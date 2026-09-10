import pandas as pd
import rasterio

INPUT_FILE = "meghalaya_ml_dataset.csv"
DEM_FILE = "data/meghalaya_dem.tif"
OUTPUT_FILE = "meghalaya_elevation_dataset.csv"

# Load dataset
df = pd.read_csv(INPUT_FILE)

print("Total records:", len(df))

# Open DEM
with rasterio.open(DEM_FILE) as src:

    print("\nDEM information:")
    print("CRS:", src.crs)
    print("Bounds:", src.bounds)
    print("Resolution:", src.res)

    elevations = []

    for _, row in df.iterrows():

        lat = row["Latitude"]
        lon = row["Longitude"]

        # Check if point is inside DEM
        if (
            src.bounds.left <= lon <= src.bounds.right
            and
            src.bounds.bottom <= lat <= src.bounds.top
        ):
            value = list(src.sample([(lon, lat)]))[0][0]

            # Check invalid elevation
            if value <= -100:
                elevations.append(None)
            else:
                elevations.append(float(value))

        else:
            elevations.append(None)

# Add elevation
df["Elevation_m"] = elevations

# Remove records without valid elevation
df = df.dropna(subset=["Elevation_m"])

# Save
df.to_csv(OUTPUT_FILE, index=False)

print("\nSUCCESS!")
print("Output:", OUTPUT_FILE)
print("Valid records:", len(df))
print("Missing elevation:", df["Elevation_m"].isna().sum())

print("\nElevation statistics:")
print(df["Elevation_m"].describe())

print("\nSample:")
print(
    df[
        ["Latitude", "Longitude", "Elevation_m"]
    ].head(10).to_string(index=False)
)