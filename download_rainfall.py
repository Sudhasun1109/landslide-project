import requests
from pathlib import Path

url = "https://arthurhouhttps.pps.eosdis.nasa.gov/gpmdata/2024/07/01/gis/3B-MO-GIS.MS.MRG.3IMERG.20240701-S000000-E235959.0000.V07B.tif"

output_folder = Path("rainfall_monthly")
output_folder.mkdir(exist_ok=True)

output_file = output_folder / "202407.tif"

print("Downloading...")
print(url)

response = requests.get(url)

print("Status code:", response.status_code)

if response.status_code == 200:
    output_file.write_bytes(response.content)
    print("Download successful!")
    print("Saved:", output_file)
    print("Size:", len(response.content), "bytes")
else:
    print("Download failed!")
    print(response.text[:500])
    