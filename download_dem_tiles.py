import pandas as pd
import math
import os
import requests

# Load landslide coordinates
df = pd.read_csv("meghalaya_ml_dataset.csv")

# Find required 1-degree SRTM tiles
tiles = set()

for _, row in df.iterrows():
    lat = math.floor(row["Latitude"])
    lon = math.floor(row["Longitude"])

    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"

    tile = f"{ns}{abs(lat):02d}{ew}{abs(lon):03d}"
    tiles.add(tile)

print("Required DEM tiles:")
for tile in sorted(tiles):
    print(tile)

# Create data folder
os.makedirs("data", exist_ok=True)

# Download tiles
for tile in sorted(tiles):

    # Example:
    # N25E092 -> N25/N25E092.hgt.gz
    lat_part = tile[:3]

    url = f"https://s3.amazonaws.com/elevation-tiles-prod/skadi/{lat_part}/{tile}.hgt.gz"

    output_gz = f"data/{tile}.hgt.gz"
    output_hgt = f"data/{tile}.hgt"

    print(f"\nDownloading {tile}...")

    try:
        response = requests.get(url, timeout=60)

        if response.status_code == 200:

            with open(output_gz, "wb") as f:
                f.write(response.content)

            print(f"Downloaded: {tile}.hgt.gz")

            # Extract gzip
            import gzip
            with gzip.open(output_gz, "rb") as f_in:
                with open(output_hgt, "wb") as f_out:
                    f_out.write(f_in.read())

            os.remove(output_gz)

            print(f"Extracted: {tile}.hgt")

        else:
            print(f"FAILED: {tile}")
            print("HTTP Status:", response.status_code)

    except Exception as e:
        print(f"ERROR downloading {tile}: {e}")

print("\nDONE!")