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

    with open('Data/zuordnung_plz_ort_landkreis.csv', newline='') as csvfile:
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

    total_districts = sum_population(district_population)
    print(total_districts)

    return district_population

def sum_population(district_population):
    total_population = 0
    for i in district_population.values():
        total_population = total_population + i


    return total_population


def get_plz_einwohner(plz_dict:dict()) -> dict():
    # get citizens per zip code
    with open ('Data/plz_einwohner.csv', newline='') as csvfile:
        plz_einwohner = csv.DictReader(csvfile, delimiter= ',')
        for row in plz_einwohner:
            if row['plz'] in plz_dict.keys():
                plz_dict[row['plz']]['population'] = plz_dict[row['plz']]['population'] + int(row['einwohner'])
            else:
                print('Left out:')
                print(row['plz'] + ' with a population of '+  row['einwohner'])

def get_plz_city_district() -> dict():
    plz_dict = {}
    with open('Data/zuordnung_plz_ort_landkreis.csv', newline='') as csvfile:
        zip_code_city = csv.DictReader(csvfile, delimiter=',')
        for row in zip_code_city:
            plz_dict[row['plz']] = {'landkreis':row['landkreis'], 'population':0}

    return plz_dict


def get_distributor_locations() -> dict():
    filePath = "Data/distributor_locations.p"
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


def get_distance_distributor_customer(distributors) -> dict():

    filePath = "Data/distanceMatrixDistributorCustomer.p"

    if os.path.exists(filePath):
        distanceMatrix = pickle.load(open(filePath, "rb"))


    else:
        print("retrieve all distributor market data by google maps")

        # get customer locations
        customer_dict = get_population_by_district()
        print(len(customer_dict.keys()))

        gmaps = googlemaps.Client(get_google_maps_key())

        # assume Munich for distributor
        distanceMatrix = {}
        counter = 1

        distributor_location = get_distributor_locations()
        print(distributor_location)

        total = len(distributor_location.keys())*len(customer_dict.keys())

        for d in distributors:
            distributor = int(d.split('-')[3])
            distributor_coordinates = str(distributor_location[distributor]['lat'])+", "+str(distributor_location[distributor]['lon'])
            distanceMatrix[distributor_coordinates] = {}
            for customer in customer_dict.keys():
                customer_coordinates = customer + ', Germany'
                distance = gmaps.distance_matrix(origins=distributor_coordinates, destinations=customer_coordinates,
                                 mode='driving')
                distanceMatrix[distributor_coordinates][customer] = distance
                print(str(counter)+ " / " + str(total)+ " with a distance of " + str(distance))
                counter = counter + 1

        pickle.dump(distanceMatrix, open(filePath, "wb"))
    return_distanceMatrix = {}
    distributor_location = get_distributor_locations()
    for d in distributors:
        distributor = int(d.split("-")[3])
        distributor_coordinates = str(distributor_location[distributor]['lat']) + ", " + str(
            distributor_location[distributor]['lon'])
        for m in distanceMatrix[distributor_coordinates].keys():
            return_distanceMatrix[d,m] = distanceMatrix[distributor_coordinates][m]["rows"][0]['elements'][0]['distance']['value']

    return return_distanceMatrix

def get_distance_supplier_manufacturer():

    filePath = "Data/distanceMatrixSupplierManufacturer.p"

    if os.path.exists(filePath):
        distanceMatrix = pickle.load(open(filePath, "rb"))

    else:
        primary_supplier = {'PS_1':"Leipzig, Germany",'PS_2':"Kassel, Germany",'PS_3': "Düsseldorf, Germany"}
        backup_supplier = {'BS_1':"Leipzig, Germany", 'BS_2':"Münster, Germany", 'BS_3':"Nürnberg, Germany"}
        manufacturer = {"M 1, Hannover, Germany" : "Hannover, Germany", "M 2, Korbach, Germany":"Korbach, Germany", "M 3, Otrokovice, Tschechien":"Otrokovice, Tschechien", "M 4, Puchov, Slowakai":"Puchov, Slowakai"}
        gmaps = googlemaps.Client(get_google_maps_key())
        distanceMatrix = {}

        for m in manufacturer.keys():
            for ps in primary_supplier.keys():
                 distance = gmaps.distance_matrix(origins=primary_supplier[ps], destinations=manufacturer[m],mode='driving')
                 distanceMatrix[ps, m] = distance["rows"][0]['elements'][0]['distance']['value']

            for bs in backup_supplier.keys():
                distance = gmaps.distance_matrix(origins=backup_supplier[bs], destinations=manufacturer[m],
                                         mode='driving')
                distanceMatrix[bs, m] = distance["rows"][0]['elements'][0]['distance']['value']

        pickle.dump(distanceMatrix, open(filePath, "wb"))

    return distanceMatrix

def get_distance_manufacturer_distributors(distributors):


    filePath = "Data/distanceMatrixManufacturerSupplier.p"

    if os.path.exists(filePath):
        distanceMatrix = pickle.load(open(filePath, "rb"))

    else:
        manufacturer = {"M 1, Hannover, Germany": "Hannover, Germany", "M 2, Korbach, Germany": "Korbach, Germany",
                        "M 3, Otrokovice, Tschechien": "Otrokovice, Tschechien",
                        "M 4, Puchov, Slowakai": "Puchov, Slowakai"}
        distributor_location = get_distributor_locations()

        gmaps = googlemaps.Client(get_google_maps_key())
        distanceMatrix = {}
        for distributor in distributors:
            d = int(distributor.split("-")[3])
            distributor_coordinates = str(distributor_location[d]['lat'])+", "+str(distributor_location[d]['lon'])

            for m in manufacturer.keys():
                distance = gmaps.distance_matrix(origins=distributor_coordinates, destinations=manufacturer[m],
                                 mode='driving')
                distanceMatrix[m,distributor] = distance["rows"][0]['elements'][0]['distance']['value']

        pickle.dump(distanceMatrix, open(filePath, "wb"))

    return distanceMatrix

def get_distance_customer_collector(distanceDistributorMarket, collector):
    distanceMatrix = {}

    for (d,cu) in distanceDistributorMarket:
        for co in collector:
            co_split = int(co.split("-")[3])
            d_split = int(co.split("-")[3])
            if d_split == co_split:
                distanceMatrix[cu,co] = distanceDistributorMarket[d,cu]
    return distanceMatrix

def get_distance_collector_recycling(recycling_stations, collectors_index):

    filePath = "Data/distanceMatrixCollectorsRecycling.p"

    if os.path.exists(filePath):
        distanceMatrix = pickle.load(open(filePath, "rb"))

    else:
        collector_locations = get_distributor_locations()

        gmaps = googlemaps.Client(get_google_maps_key())
        distanceMatrix = {}
        for recycling in recycling_stations:
            r = recycling.split("-")[2] + ", Germany"

            for c in collector_locations.keys():
                for co in collectors_index:
                    co_split = int(co.split("-")[3])
                    if c == co_split:
                        print(co)
                        collector_coordinates = str(collector_locations[c]['lat']) + ", " + str(
                            collector_locations[c]['lon'])
                        distance = gmaps.distance_matrix(origins=collector_coordinates, destinations=r,
                                         mode='driving')
                        distanceMatrix[co,recycling] = distance["rows"][0]['elements'][0]['distance']['value']

        pickle.dump(distanceMatrix, open(filePath, "wb"))
    print(distanceMatrix)

    return distanceMatrix

def get_distance_recycling_manufacturer(recycling_stations):
    filePath = "Data/distanceMatrixRecyclingManufacturer.p"
    manufacturer = {"M 1, Hannover, Germany": "Hannover, Germany",
                    "M 2, Korbach, Germany": "Korbach, Germany",
                    "M 3, Otrokovice, Tschechien": "Otrokovice, Tschechien",
                    "M 4, Puchov, Slowakai": "Puchov, Slowakai"}

    if os.path.exists(filePath):
        distanceMatrix = pickle.load(open(filePath, "rb"))

    else:

        gmaps = googlemaps.Client(get_google_maps_key())
        distanceMatrix = {}
        print(recycling_stations)
        for recycling in recycling_stations:
            r = recycling.split("-")[2] + ", Germany"
            for m in manufacturer.keys():
                distance = gmaps.distance_matrix(origins=r, destinations=manufacturer[m],
                                 mode='driving')
                distanceMatrix[recycling,m] = distance["rows"][0]['elements'][0]['distance']['value']

        pickle.dump(distanceMatrix, open(filePath, "wb"))

    return distanceMatrix


def get_google_maps_key():
    key = ''
    if key == '':
        print('Please Enter a Key to use Google Maps plug in')
        raise ValueError
    return key







"""
distanceMatrix = get_distance_distributor_customer()
distributor_locations = get_distributor_locations()
print(distributor_locations)

create_folium_with_distributors(distributor_locations,'Results/Plots/DistributorNetwork.html')
"""










