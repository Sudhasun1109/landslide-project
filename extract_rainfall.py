import rasterio

tif_file = "rainfall/20240713.tif"

latitude = 25.033514
longitude = 92.435539

with rasterio.open(tif_file) as src:

    print("Raster opened successfully!")
    print("CRS:", src.crs)
    print("Resolution:", src.res)
    print("Data type:", src.dtypes[0])
    print("NoData:", src.nodata)
    print("Scale:", src.scales)
    print("Offset:", src.offsets)

    raw_value = list(src.sample([(longitude, latitude)]))[0][0]

    print("Raw rainfall value:", raw_value)

    # Apply scale/offset if provided by the GeoTIFF
    scale = src.scales[0]
    offset = src.offsets[0]

    rainfall = raw_value * scale + offset

    print("Converted rainfall:", rainfall)