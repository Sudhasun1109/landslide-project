import pandas as pd

# Load Meghalaya landslide data
df = pd.read_csv("meghalaya_landslide.csv")

# Convert coordinates to numbers
df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

# Remove records without coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Keep useful columns
ml_data = df[
    [
        "Sl.No.",
        "Slide_No",
        "State",
        "District",
        "Slide_Name",
        "Latitude",
        "Longitude",
        "Material Involved",
        "Movement Type",
        "History"
    ]
].copy()

# Save ML base dataset
ml_data.to_csv("meghalaya_ml_base.csv", index=False)

print("================================")
print("ML BASE DATASET CREATED")
print("================================")
print("Records:", len(ml_data))
print("Columns:", ml_data.columns.tolist())
print()
print(ml_data.head())