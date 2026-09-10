import pandas as pd

# Input files
LANDSLIDE_FILE = "meghalaya_final_base.csv"
BACKGROUND_FILE = "background_features.csv"

# Output
OUTPUT_FILE = "landslide_training_data.csv"

# Load datasets
landslides = pd.read_csv(LANDSLIDE_FILE)
background = pd.read_csv(BACKGROUND_FILE)

# Add label to landslide records
landslides["Label"] = 1

# Keep only required columns
landslides = landslides[
    ["Latitude", "Longitude", "Elevation_m", "Slope_deg", "Label"]
]

background = background[
    ["Latitude", "Longitude", "Elevation_m", "Slope_deg", "Label"]
]

# Combine
training_data = pd.concat(
    [landslides, background],
    ignore_index=True
)

# Shuffle
training_data = training_data.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save
training_data.to_csv(
    OUTPUT_FILE,
    index=False
)

print("SUCCESS!")
print("Output:", OUTPUT_FILE)
print("Total records:", len(training_data))

print("\nLabel distribution:")
print(training_data["Label"].value_counts())

print("\nMissing values:")
print(training_data.isna().sum())

print("\nSample:")
print(training_data.head(10).to_string(index=False))