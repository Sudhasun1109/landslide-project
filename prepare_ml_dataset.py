import pandas as pd

INPUT_FILE = "meghalaya_complete_dataset.csv"
OUTPUT_FILE = "meghalaya_ml_dataset.csv"

# Load data
df = pd.read_csv(INPUT_FILE)

print("Original records:", len(df))

# Keep only useful ML columns
ml_columns = [
    "Latitude",
    "Longitude",
    "Material Involved",
    "Movement Type",
    "Elevation_m",
    "Slope_deg",
    "Rainfall_mm"
]

ml_df = df[ml_columns].copy()

# Remove rows where important numeric features are missing
ml_df = ml_df.dropna(
    subset=[
        "Elevation_m",
        "Slope_deg",
        "Rainfall_mm"
    ]
)

# Fill missing categorical values
ml_df["Material Involved"] = (
    ml_df["Material Involved"]
    .fillna("Unknown")
)

ml_df["Movement Type"] = (
    ml_df["Movement Type"]
    .fillna("Unknown")
)

# Save
ml_df.to_csv(OUTPUT_FILE, index=False)

print("\nSUCCESS!")
print("Output:", OUTPUT_FILE)
print("Records:", len(ml_df))

print("\nMissing values:")
print(ml_df.isnull().sum())

print("\nSample:")
print(ml_df.head())