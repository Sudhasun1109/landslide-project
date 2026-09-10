import pandas as pd

file = "meghalaya_complete_dataset.csv"

df = pd.read_csv(file)

print("========== DATASET INFO ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
for col in df.columns:
    print("-", col)

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst 5 records:")
print(df.head())

print("\nData types:")
print(df.dtypes)