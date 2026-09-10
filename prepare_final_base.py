import pandas as pd

INPUT_FILE = "meghalaya_dem_final.csv"
OUTPUT_FILE = "meghalaya_final_base.csv"

df = pd.read_csv(INPUT_FILE)

# Keep reliable features
columns = [
    "Latitude",
    "Longitude",
    "Elevation_m",
    "Slope_deg",
    "Material Involved",
    "Movement Type"
]

final_df = df[columns].copy()

# Fill text missing values
final_df["Material Involved"] = (
    final_df["Material Involved"].fillna("Unknown")
)

final_df["Movement Type"] = (
    final_df["Movement Type"].fillna("Unknown")
)

# Remove invalid numeric values
final_df = final_df.dropna(
    subset=[
        "Latitude",
        "Longitude",
        "Elevation_m",
        "Slope_deg"
    ]
)

final_df.to_csv(OUTPUT_FILE, index=False)

print("SUCCESS!")
print("Output:", OUTPUT_FILE)
print("Records:", len(final_df))

print("\nMissing values:")
print(final_df.isna().sum())

print("\nSample:")
print(final_df.head(10).to_string(index=False))