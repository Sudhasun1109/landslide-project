import rasterio

dem_file = "data/N25E092.hgt"

with rasterio.open(dem_file) as src:

    print("DEM opened successfully!")
    print("Driver:", src.driver)
    print("Width:", src.width)
    print("Height:", src.height)
    print("CRS:", src.crs)
    print("Resolution:", src.res)
    print("Bounds:", src.bounds)

    # Our first Meghalaya landslide
    latitude = 25.033514
    longitude = 92.435539

    value = list(src.sample([(longitude, latitude)]))[0][0]

    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Elevation:", value, "meters")