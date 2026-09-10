import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
import rasterio

LANDSLIDE_FILE = "meghalaya_final_base.csv"
OUTPUT_FILE = "background_points.csv"
DEM_FILE = "data/meghalaya_dem.tif"

# Load known landslides
landslides = pd.read_csv(LANDSLIDE_FILE)

print("Known landslide points:", len(landslides))

# Convert coordinates to approximate metres
# 1 degree latitude ≈ 111 km
lat_scale = 111320
mean_lat = landslides["Latitude"].mean()
lon_scale = 111320 * np.cos(np.radians(mean_lat))

landslide_xy = np.column_stack([
    landslides["Longitude"] * lon_scale,
    landslides["Latitude"] * lat_scale
])

# Fast spatial index
tree = cKDTree(landslide_xy)

# Get DEM bounds
with rasterio.open(DEM_FILE) as src:
    bounds = src.bounds

print("\nDEM area:")
print("Longitude:", bounds.left, "to", bounds.right)
print("Latitude :", bounds.bottom, "to", bounds.top)

np.random.seed(42)

background = []

print("\nGenerating background points...")

while len(background) < len(landslides):

    # Generate 5000 candidates at once
    lats = np.random.uniform(
        bounds.bottom + 0.01,
        bounds.top - 0.01,
        5000
    )

    lons = np.random.uniform(
        bounds.left + 0.01,
        bounds.right - 0.01,
        5000
    )

    candidate_xy = np.column_stack([
        lons * lon_scale,
        lats * lat_scale
    ])

    # Find nearest landslide
    distances, _ = tree.query(candidate_xy)

    # Keep points at least 1 km away
    valid = distances >= 1000

    for lat, lon in zip(lats[valid], lons[valid]):

        background.append({
            "Latitude": lat,
            "Longitude": lon,
            "Label": 0
        })

        if len(background) >= len(landslides):
            break

    print("Generated:", len(background))

# Create DataFrame
background_df = pd.DataFrame(background)

# Save
background_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nSUCCESS!")
print("Background points:", len(background_df))
print("Output:", OUTPUT_FILE)

print("\nSample:")
print(background_df.head(10).to_string(index=False))