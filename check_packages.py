print("Checking packages...\n")

try:
    import geopandas
    print("GeoPandas:", geopandas.__version__)
except Exception as e:
    print("GeoPandas ERROR:")
    print(e)

try:
    import shapely
    print("Shapely:", shapely.__version__)
except Exception as e:
    print("Shapely ERROR:")
    print(e)

try:
    import sklearn
    print("Scikit-learn:", sklearn.__version__)
except Exception as e:
    print("Scikit-learn ERROR:")
    print(e)