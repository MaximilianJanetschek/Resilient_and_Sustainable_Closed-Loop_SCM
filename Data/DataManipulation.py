# get market distances

# PLZ data from https://www.suche-postleitzahl.org/downloads
# summarize into landkreise as only 126 remain -> should be reasonable to model market
import csv










def get_population_by_district() -> dict():
    plz_dict = {}

    # retrieve all plz and area names
    with open('zuordnung_plz_ort_landkreis.csv', newline='') as csvfile:
        zip_code_city = csv.DictReader(csvfile, delimiter=',')
        for row in zip_code_city:
            plz_dict[row['plz']] = {'landkreis':row['landkreis'], 'population':0}

    # get citizens per zip code
    with open ('plz_einwohner.csv', newline='') as csvfile:
        plz_einwohner = csv.DictReader(csvfile, delimiter= ',')
        for row in plz_einwohner:
            if row['plz'] in plz_dict.keys():
                plz_dict[row['plz']]['population'] = plz_dict[row['plz']]['population'] + int(row['einwohner'])
            else:
                print('Left out:')
                print(row['plz'] + ' with a population of '+  row['einwohner'])

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







