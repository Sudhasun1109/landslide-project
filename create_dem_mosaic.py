import rasterio
from rasterio.merge import merge
import glob
import os

# Find all DEM tiles
dem_files = glob.glob("data/*.hgt")

print("DEM tiles found:")
for file in dem_files:
    print(file)

# Open all DEM files
src_files = [rasterio.open(file) for file in dem_files]

# Merge
mosaic, transform = merge(src_files)

# Copy metadata from first file
out_meta = src_files[0].meta.copy()

out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": transform,
    "compress": "lzw"
})

# Save combined DEM
output_file = "data/meghalaya_dem.tif"

with rasterio.open(output_file, "w", **out_meta) as dest:
    dest.write(mosaic)

# Close files
for src in src_files:
    src.close()

print("\nSUCCESS!")
print("Combined DEM:", output_file)
print("Width:", mosaic.shape[2])
print("Height:", mosaic.shape[1])
print("Bands:", mosaic.shape[0])