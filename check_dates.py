import pandas as pd

file = "meghalaya_ml_base_clean.csv"

df = pd.read_csv(file)

print("Total records:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nHistory values:")
print(df["History"].head(20).to_string(index=False))

print("\nValid year records:", df["History_Year"].notna().sum())

print("\nUnique years:")
print(sorted(df["History_Year"].dropna().unique()))