# get market distances

# PLZ data from https://www.suche-postleitzahl.org/downloads
# summarize into landkreise as only 126 remain -> should be reasonable to model market
import csv
import sys
from Utility.Drawing import *
from geopy.geocoders import Nominatim
import pickle
import os
import googlemaps
from pathlib import Path


def get_distributor_locations() -> list():
    geolocator = Nominatim(user_agent="example app")
    plz_dict = get_plz_city_district()
    locations = []
    stepsize = 5000
    buckets = range(stepsize,100001,stepsize)
    locations = dict.fromkeys(buckets)
    for i in locations.keys():
        locations[i] = {}

    counter = 0
    total = len(plz_dict.keys())
    step = round(total / 100,0)
    done_percentage = 0
    for i in plz_dict.keys():
        for j in locations.keys():
            if int(i) < j:
                search = i + ", Deutschland"
                output = geolocator.geocode(search).raw
                locations[j][int(i)] = {"lat":output['lat'], "lon":output['lon'], 'name':output['display_name']}
                break
        counter = counter + 1
        if counter % step == 0:
            done_percentage = done_percentage + 1
            print("Collected " + str(done_percentage) + "%h so far")



    print(locations)

    pickle.dump(locations, open("locations.p", "wb"))









def get_population_by_district() -> dict():
    plz_dict = get_plz_city_district()

    # retrieve all plz and area names

    with open('zuordnung_plz_ort_landkreis.csv', newline='') as csvfile:
        zip_code_city = csv.DictReader(csvfile, delimiter=',')
        for row in zip_code_city:
            plz_dict[row['plz']] = {'landkreis':row['landkreis'], 'population':0}

    # get citizens per zip code
    get_plz_einwohner(plz_dict)

    # sort population to area
    district_population = {}
    for zipcode in plz_dict.values():
        if zipcode['landkreis'] in district_population.keys():
            district_population[zipcode['landkreis']] = district_population[zipcode['landkreis']] + zipcode['population']
        else:
            district_population[zipcode['landkreis']] = zipcode['population']

    quick_test = 0
    for i in district_population.values():
        quick_test = quick_test + i

    print(quick_test)

    return district_population


def get_plz_einwohner(plz_dict:dict()) -> dict():
    # get citizens per zip code
    with open ('plz_einwohner.csv', newline='') as csvfile:
        plz_einwohner = csv.DictReader(csvfile, delimiter= ',')
        for row in plz_einwohner:
            if row['plz'] in plz_dict.keys():
                plz_dict[row['plz']]['population'] = plz_dict[row['plz']]['population'] + int(row['einwohner'])
            else:
                print('Left out:')
                print(row['plz'] + ' with a population of '+  row['einwohner'])

def get_plz_city_district() -> dict():
    plz_dict = {}
    with open('zuordnung_plz_ort_landkreis.csv', newline='') as csvfile:
        zip_code_city = csv.DictReader(csvfile, delimiter=',')
        for row in zip_code_city:
            plz_dict[row['plz']] = {'landkreis':row['landkreis'], 'population':0}

    return plz_dict


def get_distributor_locations() -> dict():
    filePath = "distributor_locations.p"
    if os.path.exists(filePath):
        distributor_locations = pickle.load(open(filePath, "rb"))
    else:
        distributor_locations = {}
        locations = pickle.load(open("locations.p", "rb"))

        for i in locations.keys():
            sum_lat = sum(float(locations[i][j]["lat"]) for j in locations[i].keys())
            sum_lon = sum(float(locations[i][j]["lon"]) for j in locations[i].keys())
            number_coordinates = len(locations[i].keys())
            distributor_locations[i] = {"lat": sum_lat / number_coordinates, "lon": sum_lon / number_coordinates}

        pickle.dump(distributor_locations, open("distributor_locations.p", "wb"))

    return distributor_locations


def get_distance_distributor_customer() -> dict():

    filePath = "distanceMatrix.p"

    if os.path.exists(filePath):
        distanceMatrix = pickle.load(open(filePath, "rb"))


    else:

        # get customer locations
        customer_dict = get_population_by_district()
        print(len(customer_dict.keys()))

        key = ''
        if key == '':
            print('Enter the Google API Idiot!')
            raise ValueError
        gmaps = googlemaps.Client(key)

        # assume Munich for distributor
        distanceMatrix = {}
        distanceMatrix['Augsburg'] = {}
        counter = 1

        distributor_location = get_distributor_locations()

        total = len(distributor_location.keys())*len(customer_dict.keys())
        for distributor in distributor_location.keys():
            distributor_coordinates = str(distributor_location[distributor]['lat'])+", "+str(distributor_location[distributor]['lon'])
            distanceMatrix[distributor_coordinates] = {}
            for customer in customer_dict.keys():
                customer_coordinates = customer + ', Germany'
                distance = gmaps.distance_matrix(origins=distributor_coordinates, destinations=customer_coordinates,
                                 mode='driving')
                distanceMatrix[distributor_coordinates][customer] = distance
                print(str(counter)+ " / " + str(total)+ " with a distance of " + str(distance))
                counter = counter + 1

        pickle.dump(distanceMatrix, open("distanceMatrix.p", "wb"))

    return distanceMatrix



distanceMatrix = get_distance_distributor_customer()
distributor_locations = get_distributor_locations()
print(distributor_locations)

create_folium_with_distributors(distributor_locations,'Results/Plots/DistributorNetwork.html')











