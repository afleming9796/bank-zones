import pandas as pd
import geopandas as gpd
import folium

#read in geojson of bank isochrones
bank_isochrones = gpd.read_file("data/output/bank_isochrones.geojson")

#create a separate gpd with just unioned isochrones
bank_isochrones_union = bank_isochrones.unary_union

#save unioned isochrones as a geojson
gpd.GeoSeries(bank_isochrones_union).to_file("data/output/bank_isochrones_union.geojson", driver='GeoJSON')

# Create a folium map with bank_isochrones_union
m = folium.Map(location=[39.9526, -75.1652], zoom_start=12)

# Add the bank isochrones to the map
folium.GeoJson(bank_isochrones_union).add_to(m)