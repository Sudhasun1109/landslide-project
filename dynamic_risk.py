import pandas as pd
import rasterio


# =========================
# Files
# =========================

INPUT_FILE = "landslide_risk_predictions.csv"
RAINFALL_FILE = "rainfall/20240713.tif"
OUTPUT_FILE = "dynamic_risk_predictions.csv"


# =========================
# Load predictions
# =========================

df = pd.read_csv(INPUT_FILE)

print("Prediction data loaded!")
print("Records:", len(df))


# =========================
# Read rainfall
# =========================

with rasterio.open(RAINFALL_FILE) as src:

    print("\nRainfall raster loaded!")
    print("CRS:", src.crs)
    print("Resolution:", src.res)

    rainfall_values = []

    for _, row in df.iterrows():

        lat = row["Latitude"]
        lon = row["Longitude"]

        # Check location is inside raster
        if (
            src.bounds.left <= lon <= src.bounds.right
            and src.bounds.bottom <= lat <= src.bounds.top
        ):
            r, c = src.index(lon, lat)

            raw_value = src.read(1)[r, c]

            # IMERG daily GIS product scaling
            rainfall_mm = float(raw_value) / 10

        else:
            rainfall_mm = 0.0

        rainfall_values.append(rainfall_mm)


df["Rainfall_mm"] = rainfall_values


# =========================
# Rainfall trigger
# =========================
#
# Prototype rainfall factor:
#
# 0 mm       -> 0
# 10 mm      -> 20
# 25 mm      -> 50
# 50 mm      -> 75
# 100+ mm    -> 100
#

def rainfall_factor(rainfall):

    if rainfall <= 0:
        return 0

    elif rainfall < 10:
        return 20

    elif rainfall < 25:
        return 50

    elif rainfall < 50:
        return 75

    else:
        return 100


df["Rainfall_Factor"] = df["Rainfall_mm"].apply(
    rainfall_factor
)


# =========================
# Dynamic risk
# =========================

df["Dynamic_Risk_Score"] = (
    df["Risk_Score"] * 0.70
    +
    df["Rainfall_Factor"] * 0.30
)


# =========================
# Risk level
# =========================

def get_risk_level(score):

    if score < 25:
        return "Low"

    elif score < 50:
        return "Medium"

    elif score < 75:
        return "High"

    else:
        return "Very High"


df["Dynamic_Risk_Level"] = df[
    "Dynamic_Risk_Score"
].apply(get_risk_level)


# =========================
# Save
# =========================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================
# Results
# =========================

print("\nSUCCESS!")

print("Output:", OUTPUT_FILE)

print("\nRainfall statistics:")
print(df["Rainfall_mm"].describe())

print("\nDynamic risk distribution:")
print(
    df["Dynamic_Risk_Level"].value_counts()
)

print("\nSample:")
print(
    df[
        [
            "Latitude",
            "Longitude",
            "Risk_Score",
            "Rainfall_mm",
            "Rainfall_Factor",
            "Dynamic_Risk_Score",
            "Dynamic_Risk_Level"
        ]
    ].head(15).to_string(index=False)
)