import pandas as pd
import rasterio

# Load landslide dataset
df = pd.read_csv("meghalaya_ml_dataset.csv")

# Open DEM
with rasterio.open("data/N25E092.hgt") as src:

    print("DEM Bounds:")
    print("Left   :", src.bounds.left)
    print("Right  :", src.bounds.right)
    print("Bottom :", src.bounds.bottom)
    print("Top    :", src.bounds.top)

    print("\nLandslide Coordinate Range:")
    print("Latitude min :", df["Latitude"].min())
    print("Latitude max :", df["Latitude"].max())
    print("Longitude min:", df["Longitude"].min())
    print("Longitude max:", df["Longitude"].max())

    # Check which points are inside DEM
    inside = (
        (df["Longitude"] >= src.bounds.left) &
        (df["Longitude"] <= src.bounds.right) &
        (df["Latitude"] >= src.bounds.bottom) &
        (df["Latitude"] <= src.bounds.top)
    )

    print("\nCoverage:")
    print("Total records :", len(df))
    print("Inside DEM    :", inside.sum())
    print("Outside DEM   :", (~inside).sum())