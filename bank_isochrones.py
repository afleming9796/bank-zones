import pandas as pd
import os
import requests
from dotenv import load_dotenv
import geopandas as gpd
from shapely.geometry import shape

load_dotenv()
MAPBOX_KEY = os.getenv('MAPBOX_TOKEN')

#read in bank locations
bank_locs = pd.read_csv("bank_locs_philly.csv")

#loop through bank locations and get isochrones for each
#set up base url
iso_url = "https://api.mapbox.com/isochrone/v1/mapbox/"

#set up params
params = {
    "contours_minutes": 15,
    "polygons": "true",
    "access_token": MAPBOX_KEY
}

for index, row in bank_locs.iterrows():
    response = requests.get(iso_url + "walking/" + str(row['long']) + "," + str(row['lat']), params=params).json()
    geometry = shape(response['features'][0]['geometry'])
    bank_locs.loc[index, 'isochrone'] = geometry

gdf = gpd.GeoDataFrame(bank_locs, geometry='isochrone')

#save gdf
gdf.to_file("data/output/bank_isochrones.geojson", driver='GeoJSON')