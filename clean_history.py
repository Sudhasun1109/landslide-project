import pandas as pd
import re

df = pd.read_csv("meghalaya_ml_base.csv")

def extract_year(value):
    if pd.isna(value):
        return None

    text = str(value)

    # Find a 4-digit year
    match = re.search(r"\b(19|20)\d{2}\b", text)

    if match:
        return int(match.group())

    return None


df["History_Year"] = df["History"].apply(extract_year)

df.to_csv("meghalaya_ml_base_clean.csv", index=False)

print("================================")
print("HISTORY CLEANING COMPLETE")
print("================================")

print("Total records:", len(df))
print("Valid years:", df["History_Year"].notna().sum())
print("Missing years:", df["History_Year"].isna().sum())

print("\nYear distribution:")
print(df["History_Year"].value_counts().sort_index())

print("\nSample:")
print(df[["History", "History_Year"]].head(20).to_string(index=False))

print("\nCreated: meghalaya_ml_base_clean.csv")