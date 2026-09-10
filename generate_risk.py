import pandas as pd
import joblib


# =========================
# 1. Load model
# =========================

MODEL_FILE = "landslide_model.pkl"
DATA_FILE = "landslide_training_data.csv"

model = joblib.load(MODEL_FILE)
df = pd.read_csv(DATA_FILE)

print("Model loaded!")
print("Records:", len(df))


# =========================
# 2. Prepare features
# =========================

X = df[
    [
        "Elevation_m",
        "Slope_deg"
    ]
]


# =========================
# 3. Predict probability
# =========================

probability = model.predict_proba(X)[:, 1]

df["Risk_Score"] = probability * 100


# =========================
# 4. Risk level
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


df["Risk_Level"] = df["Risk_Score"].apply(get_risk_level)


# =========================
# 5. Save result
# =========================

OUTPUT_FILE = "landslide_risk_predictions.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================
# 6. Display results
# =========================

print("\nSUCCESS!")
print("Output:", OUTPUT_FILE)

print("\nRisk level distribution:")
print(df["Risk_Level"].value_counts())

print("\nSample predictions:")

print(
    df[
        [
            "Latitude",
            "Longitude",
            "Elevation_m",
            "Slope_deg",
            "Risk_Score",
            "Risk_Level"
        ]
    ].head(15).to_string(index=False)
)