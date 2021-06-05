import pandas as pd
import googlemaps


locations = pd.DataFrame({"origin_city": ["Hamburg", "Toronto", "Sucre",
                                          "Jaipur", "Wellington"],
                          "origin_country": ["Germany", "Canada", "Bolivia",
                                      "India", "New Zealand"],
                          "destination_city": ["Zurich", "New York", "Santiago",
                                              "Bengaluru", "Auckland"],
                          "destination_country": ["Switzerland", "USA", "Chile",
                                                 "India", "New Zealand"]
                         },
                        columns = ["origin_city", "origin_country",
                                  "destination_city", "destination_country"])

key = ''
gmaps = googlemaps.Client(key)
import numpy as np
import re

def concat_cities(x, y):
    name = x + "+" + y
    return(re.sub(" ", "+", name))

locations['origin'] = np.vectorize(concat_cities)(
    locations['origin_city'], locations['origin_country'])
locations['destination'] = np.vectorize(concat_cities)(
    locations['destination_city'], locations['destination_country'])
print(locations)


ham_zur = gmaps.distance_matrix(origins=locations.origin[0], destinations=locations.destination[0],
                     mode='driving')
print('test')
print(ham_zur)
ham_zur['rows']
ham_zur['rows'][0]
ham_zur['rows'][0]['elements']
map_data = pd.Series(np.vectorize(gmaps.distance_matrix)(locations['origin'],
                                                      locations['destination'],
                                                      mode='driving')).map(
    lambda x: x['rows'][0]['elements'][0])
map_data
locations['distance_m'] = [x['distance']['value'] for x in map_data]
locations['durations_min'] = [x['duration']['value'] for x in map_data]
locations.drop(['origin', 'destination'], axis=1, inplace=True)
locations

'''
import requests

response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA')

resp_json_payload = response.json()

print(resp_json_payload['results'][0]['geometry']['location'])
'''

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="example app")
output = geolocator.geocode("86368 Deutschland").raw
print(output['lat'], output['lon'], output['display_name'])