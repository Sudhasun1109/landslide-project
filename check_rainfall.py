import pandas as pd

df = pd.read_csv("meghalaya_dem_final.csv")

print("Total records:", len(df))

print("\nRainfall information:")
print(df["Rainfall_mm"].describe())

print("\nUnique rainfall values:")
print(sorted(df["Rainfall_mm"].unique()))

print("\nRainfall sample:")
print(
    df[
        ["Latitude", "Longitude", "Rainfall_mm"]
    ].head(10).to_string(index=False)
)