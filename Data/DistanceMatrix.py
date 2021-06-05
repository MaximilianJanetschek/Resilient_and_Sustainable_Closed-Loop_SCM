import pandas as pd
import googlemaps
import Data.DataManipulation as DM

# get customer locations
customer_dict = DM.get_population_by_district()
print(len(customer_dict.keys()))

key = ''
gmaps = googlemaps.Client(key)

# assume Munich for distributor
distanceMatrix = {}
distanceMatrix['Augsburg'] = {}
counter = 1
percentage_counter = 1
for district in customer_dict.keys():
    district_origin = district + ', Germany'
    distance = gmaps.distance_matrix(origins=district_origin, destinations='Augsburg, Germany',
                     mode='driving')
    distanceMatrix['Augsburg'][district] = distance
    if counter % int((len(customer_dict.keys())/10)) == 0:
        print(percentage_counter)
        percentage_counter = percentage_counter + 1

    counter = counter + 1


