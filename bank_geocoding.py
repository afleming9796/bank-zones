import pandas as pd
import os
import requests
from dotenv import load_dotenv

load_dotenv()
MAPBOX_KEY = os.getenv('MAPBOX_TOKEN')

#bank location data available at https://banks.data.fdic.gov/docs/#/
#see definitions at https://banks.data.fdic.gov/docs/locations_definitions.csv
locs = pd.read_csv("https://s3-us-gov-west-1.amazonaws.com/cg-2e5c99a6-e282-42bf-9844-35f5430338a5/downloads/locations.csv")

#subset cols 
cols = ['ADDRESS', 'CERT', 'CITY', 'COUNTY', 'NAME', 'OFFNAME', 'SERVTYPE', 'STALP', 'STCNTY', 'STNAME', 'ZIP']
locs = locs.loc[:, cols]

#subset locs to only include banks in Philadelphia and SERVTYPE = 11 (brick and mortar)
locs_ph = locs.loc[(locs['CITY'] == 'Philadelphia') & (locs['SERVTYPE'] == 11), :]

#remove string after # in address. Strip # too. 
locs_ph.loc[:, 'ADDRESS'] = locs_ph['ADDRESS'].str.split("#").str[0].str.strip()

#create col with full address 
locs_ph.loc[:, 'full_address'] = locs_ph['ADDRESS'] + ", " + locs_ph['CITY'] + ", " + locs_ph['STALP'] + " " + locs_ph['ZIP'].astype(str)

#make call to mapbox api to geocode each bank location
geocoding_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

#set up params
payload = {
    "access_token": MAPBOX_KEY
}

#create new boolean col to track missed addresses
locs_ph.loc[:, 'missed_address'] = False

#loop through each bank location and make call to mapbox api
#store each each lat and long as part of bank_locs
for index, row in locs_ph.iterrows():
    try: 
        #make call to mapbox api
        response = requests.get(geocoding_url + row["full_address"] + ".json", params=payload).json()
        #store lat and long
        locs_ph.loc[index, 'lat'] = response['features'][0]['center'][1]
        locs_ph.loc[index, 'long'] = response['features'][0]['center'][0]
    except Exception as e:
        print(e)
        print(index)
        #label row with missed address
        locs_ph.loc[index, 'missed_address'] = True

#check missing addresses
locs_ph[locs_ph['missed_address'] == True]

#save locs_ph without index
locs_ph.to_csv("data/staging/bank_locs_philly.csv", index=False)