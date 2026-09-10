import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


# =========================
# 1. Load dataset
# =========================

DATA_FILE = "landslide_training_data.csv"

df = pd.read_csv(DATA_FILE)

print("Dataset loaded!")
print("Total records:", len(df))


# =========================
# 2. Select features
# =========================

X = df[
    [
        "Elevation_m",
        "Slope_deg"
    ]
]

y = df["Label"]


print("\nFeatures:")
print(X.columns.tolist())

print("\nLabels:")
print(y.value_counts())


# =========================
# 3. Split dataset
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# =========================
# 4. Create Random Forest
# =========================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# =========================
# 5. Train model
# =========================

print("\nTraining Random Forest...")

model.fit(X_train, y_train)

print("Training completed!")


# =========================
# 6. Prediction
# =========================

y_pred = model.predict(X_test)


# =========================
# 7. Accuracy
# =========================

accuracy = accuracy_score(y_test, y_pred)

print("\n========================")
print("MODEL RESULTS")
print("========================")

print("Accuracy:", round(accuracy * 100, 2), "%")


# =========================
# 8. Classification report
# =========================

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# =========================
# 9. Feature importance
# =========================

print("\nFeature Importance:")

for feature, importance in zip(
    X.columns,
    model.feature_importances_
):
    print(
        feature,
        ":",
        round(importance, 4)
    )


# =========================
# 10. Save model
# =========================

MODEL_FILE = "landslide_model.pkl"

joblib.dump(model, MODEL_FILE)

print("\nSUCCESS!")
print("Model saved as:", MODEL_FILE)