from Data.DataManipulation import *
import random
import Data.DataManipulation
import os

def get_coordinates_of_all_sites(indices):
    [I, J, M, A, B, C, R, P, W, S, F] = indices
    filePath = 'Data/locations_of_all_sites.p'
    if os.path.exists(filePath):
        locations = pickle.load(open(filePath, "rb"))

    else:
        geolocator = Nominatim(user_agent="example app")


        locations = {}
        # suppliers
        primary_supplier = {'PS_1': "Leipzig, Germany", 'PS_2': "Kassel, Germany", 'PS_3': "Düsseldorf, Germany"}
        backup_supplier = {'BS_1': "Leipzig, Germany", 'BS_2': "Münster, Germany", 'BS_3': "Nürnberg, Germany"}
        manufacturer = {"M 1, Hannover, Germany": "Hannover, Germany", "M 2, Korbach, Germany": "Korbach, Germany",
                        "M 3, Otrokovice, Tschechien": "Otrokovice, Tschechien",
                        "M 4, Puchov, Slowakai": "Puchov, Slowakai"}


        for i in I:
            output = geolocator.geocode(primary_supplier[i]).raw
            locations[i] ={"lat": output['lat'], "lon": output['lon'], 'name': output['display_name'], 'category':'suppliers'}

        for j in J:
            output = geolocator.geocode(backup_supplier[j]).raw
            locations[j] ={"lat": output['lat'], "lon": output['lon'], 'name': output['display_name'], 'category':'suppliers'}

        print(locations)

        # manufacturers
        for m in M:
            output = geolocator.geocode(manufacturer[m]).raw
            locations[m] ={"lat": output['lat'], "lon": output['lon'], 'name': output['display_name'], 'category':'manufacturer'}

        # distributors
        distributors = get_distributor_locations()
        print(distributors)
        for a in A:
            dis = int(a.split('-')[3])
            locations[a] = {"lat": distributors[dis]['lat'], "lon": distributors[dis]['lon'], 'category':'distributor'}

        customer_dict = get_population_by_district()
        for b in B:
            print(b)
            if b != '':
                output = geolocator.geocode(b).raw
                locations[b] ={"lat": output['lat'], "lon": output['lon'], 'name': output['display_name'], 'category':'customer'}

        # collectors
        for c in C:
            dis = int(c.split('-')[3])
            locations[c] = {"lat": distributors[dis]['lat'], "lon": distributors[dis]['lon'], 'category':'collectors'}


        # recyclers
        for r in R:
            recycler = r.split('-')[2] +  ', Germany'
            output = geolocator.geocode(recycler).raw
            locations[r] ={"lat": output['lat'], "lon": output['lon'], 'name': output['display_name'], 'category':'recyclers'}

        pickle.dump(locations, open(filePath, "wb"))

    return locations


def initialize_sets():

    # Primary Supplier
    I = ['PS_1','PS_2','PS_3']

    # Backup Supplier
    J = ['BS_1', 'BS_2', 'BS_3']

    # Manufacturer
    M = ["M 1, Hannover, Germany", "M 2, Korbach, Germany", "M 3, Otrokovice, Tschechien", "M 4, Puchov, Slowakai"]

    # Distributors
    distributor_locations = get_distributor_locations()
    counter = 1
    A = []
    for i in distributor_locations.keys():
        A.append("D-" + str(counter) + '-PLZ-' + str(i))
        counter += 1

    # Markets
    customer_dict = get_population_by_district()
    B = []
    for i in customer_dict.keys():
        B.append(i)

    # collectors
    counter = 1
    C = []
    for i in distributor_locations.keys():
        C.append("C-" + str(counter) + '-PLZ-' + str(i))
        counter += 1

    # Recyclers
    R = ["R-1-Brenz", "R-2-Wernigerode", "R-3-Bochum", "R-4-Bad Bibra", "R-5-Mülsen", "R-6-Löhneberg", "R-7-Neckarsulm", "R-8-Friedberg", "R-9-Fürstenzell"]

    # Tire Index
    P = ['Light-Vehicle']

    # Raw Material
    W = ["Natrual Rubber", "Syntetic Polymere", "Fillers"]

    # Distribution Scenario
    S = ["Trend"]

    # Information Shared
    F = ["Normal"]

    return [I,J,M,A,B,C,R,P,W,S,F]

def get_parameters(indices):
    [I,J,M,A,B,C,R,P,W,S,F] = indices
    filePath = os.getcwd() + "/Data/parameters.p"
    if os.path.exists(filePath):
        parameters = pickle.load(open(filePath, "rb"))

    else:
        parameters = initialize_parameters(I,J,M,A,B,C,R,P,W,S,F)
        pickle.dump(parameters, open(filePath, "wb"))

    return parameters


def initialize_parameters(I,J,M,A,B,C,R,P,W,S,F):
    Scenario = {'Worse': {'demand':{'Lower_Limit':60, 'Upper_Limit': 90},'cost':{'Lower_Limit':110, 'Upper_Limit': 140}}, 'Trend':{'demand':{'Lower_Limit':100, 'Upper_Limit': 101},'cost':{'Lower_Limit':100, 'Upper_Limit': 101}}, 'Good':{'demand':{'Lower_Limit':110, 'Upper_Limit': 150},'cost':{'Lower_Limit':70, 'Upper_Limit': 90}}}
    # worse scenario: economy recovers badly, demand goes down and cost up
    # trend as it is
    # good economy recovers, cost go down
    random.seed(115599)
    RC = {}
    raw_prices = {"Natrual Rubber": 1.96, "Syntetic Polymere":1.5, "Fillers":3.26}

    Man_cost = {"M 1, Hannover, Germany":1.4, "M 2, Korbach, Germany":1.2, "M 3, Otrokovice, Tschechien":1, "M 4, Puchov, Slowakai":0.9}

    # natural rubber https://www.statista.com/statistics/727582/price-of-rubber-per-pound/
    # synthetic polymers https://www.ft.com/content/f97d653c-71f4-4b84-90ee-896b7bd5d299
    # Fillers https://wits.worldbank.org/trade/comtrade/en/country/All/year/2019/tradeflow/Exports/partner/MDA/product/400510

    final_tire_price = 100
    # raw data prices
    for w in W:
        for i in I:
            intermediate_result =  raw_prices[w]  * (random.randrange(80, 120, 2)/100) # https://www.statista.com/statistics/727582/price-of-rubber-per-pound/
            RC[w,i] = round(intermediate_result,2)
        for j in J:
            intermediate_result = raw_prices[w] * 1.5 *  (random.randrange(80, 120, 2)/100)
            RC[w, j] = round(intermediate_result,2)
            # Fixed cost of contracting supplier
    CC = {}
    for i in I:
        intermediate_result = 17596  *  (random.randrange(80, 120, 2)/100)      # https://blog.iaccm.com/commitment-matters-tim-cummins-blog/the-cost-of-a-contract
        CC[i] = round(intermediate_result,2)
    for j in J:
        intermediate_result =  17596 * 1.5*  (random.randrange(80, 120, 2)/100)
        CC[j] = round(intermediate_result,2)

    # Production Cost of tire type p
    LC = {}
    for p in P:
        for m in M:
            intermediate_result = final_tire_price * 0.5 * Man_cost[m]
            LC[p, m] =round(intermediate_result,2)

    prob = {}  # disruption probability in scenario s
    for s in S:
        prob[s] = round(1/len(S),4)


    # disrupted capacitz of PS
    N = {}
    for s in S:
        for i in I:
            N[(i,s)] = round(random.random()*0.5,2)

    # quantity of raw material
    raw_material_kg_per_kg = {"Natrual Rubber": 0.09, "Syntetic Polymere": 0.26, "Fillers": 0.33} # https://escholarship.org/uc/item/06r0q71c
    G = {}
    for w in W:
        G[w] = raw_material_kg_per_kg[w] * 9 # average weight of a tire

    # Transportation Cost
    T = {}
    # primary supplier to manufacturer
    distanceSupplierManufacturer = get_distance_supplier_manufacturer()
    for s in S:
        for w in W:
            for (i,m) in distanceSupplierManufacturer.keys():
                intermediate_result = (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)*0.001 * distanceSupplierManufacturer[i,m] / 1000
                T[w, i, m, s] = round(intermediate_result,15)
    # manufacturer distributor
    distanceManufacturerDistributor=  get_distance_manufacturer_distributors(A)
    for s in S:
        for p in P:
            for (m,a) in distanceManufacturerDistributor:
                intermediate_result= (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)*0.002 * distanceManufacturerDistributor[m,a] / 1000
                T[p, m, a, s] = round(intermediate_result,15)
    # distributor market
    distanceDistributorMarket = get_distance_distributor_customer(A)
    for s in S:
        for p in P:
            for (a,b) in distanceDistributorMarket:
                intermediate_result =  (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)*0.03*distanceDistributorMarket[a,b] / 1000
                T[p, a, b, s] = round(intermediate_result,15)


    # market collector
    distanceMarketCollector = get_distance_customer_collector(distanceDistributorMarket, C)
    for s in S:
        for p in P:
            for (b,c) in distanceMarketCollector:
                intermediate_result = (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)*0.04*distanceMarketCollector[b,c] / 1000
                T[p,b,c,s] = round(intermediate_result,15)

    # collector recycling center
    distanceCollectorRecycling = get_distance_collector_recycling(R,C)
    for s in S:
        for p in P:
            for (c,r) in distanceCollectorRecycling:
                intermediate_result= (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)*0.002 * distanceCollectorRecycling[c,r] / 1000
                T[p,c,r,s] = round(intermediate_result,15)

    # recycling manufacturer
    distanceRecyclingManufacturer = get_distance_recycling_manufacturer(R)
    print(distanceRecyclingManufacturer)
    for s in S:
        for (r,m) in distanceRecyclingManufacturer:
            intermediate_result=(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)*0.0005*distanceRecyclingManufacturer[r,m]
            T[r, m, s] = round(intermediate_result,15)

    # Fixed Cost
    FC = {}
    for m in M:
        FC[m] = 20000000*Man_cost[m]
    for a in A:
        FC[a] = 5000000 * (random.randrange(80, 120, 2)/100)

    for c in C:
        FC[c] = 4000000*(random.randrange(80, 120, 2)/100)
    for r in R:
        FC[r] = 1000000*(random.randrange(80, 120, 2)/100)

    # capacity
    K = {}
    capacity_raw = {"Natrual Rubber": 4062713, "Syntetic Polymere": 1406324, "Fillers": 5156520}
    for s in S:
        # PS
        for w in W:
            for i in I:
                intermediate_result = capacity_raw[w] * 2 *1.7 * (random.randrange(80, 120, 2)/100)*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                K[w, i, s] = round(intermediate_result,0)
            for j in J:
                intermediate_result = capacity_raw[w] * 1.2*2* (random.randrange(80, 120, 2)/100)*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                K[w, j, s] = round(intermediate_result,0)
        for p in P:
            for m in M:
                intermediate_result = round(1302152,0)*2 *Man_cost[m]*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                K[p, m, s] = round(intermediate_result,0)
            for a in A:
                intermediate_result = 260430*5 * (random.randrange(80, 120, 2)/100)*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                K[p, a, s] = round(intermediate_result, 0)
            for c in C:
                intermediate_result = round(260430*5,0)*(random.randrange(80, 120, 2)/100)* (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                K[p, c, s] = round(intermediate_result, 0)
        for r in R:
            K[r, s] = 578734*2*(random.randrange(80, 120, 2)/100)

    # purchase prices
    U = {}
    for s in S:
        for p in P:
            for m in M:
                intermediate_result = final_tire_price*0.8*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                U[p, m, s] = round(intermediate_result, 8)
            for a in A:
                intermediate_result = final_tire_price*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                U[p, a, s]= round(intermediate_result, 8)
            for b in B:
                intermediate_result = final_tire_price*-0.05*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                U[p, b, s]= round(intermediate_result, 8)
            for c in C:
                intermediate_result = 0.05*final_tire_price*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                U[p, c, s] = round(intermediate_result, 8)
        for r in R:
            intermediate_result= 0.02*final_tire_price*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
            U[r, s]= round(intermediate_result, 8)

    # percentage scrapped
    alpha = {}
    for s in S:
        for b in B:
            for p in P:
                alpha[p,b,s] = round(random.randrange(70,90,2)/100,2)
    print(alpha)

    # demand of market b
    customer = get_population_by_district()
    total_population = sum_population(customer)
    total_demand = 5208606

    D = {}
    for s in S:
        for p in P:
            for b in customer.keys():
                demand = total_demand * (customer[b] / total_population)* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100)
                D[p,b,s] = round(demand,0)

    # polution emitted
    H = {}
    for s in S:
        # on transport to manufacturer
        for m in M:
            # from primary supplier
            for i in I:
                intermediate_result = T["Natrual Rubber",i,m,s] * (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100) / Man_cost[m]
                H[i, m, s] = round(intermediate_result, 15)
            # from backup supplier
            for j in J:
                intermediate_result = T["Natrual Rubber",j,m,s] *  (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100) / Man_cost[m]
                H[j, m, s] = round(intermediate_result*2, 15)
            # manufacturer to distributor
            for a in A:
                intermediate_result = T['Light-Vehicle',m,a,s] * (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100) / Man_cost[m]
                H[m, a, s] = round(intermediate_result/4, 15)

        # distributor to market
        for a in A:
            for b in B:
                intermediate_result = T['Light-Vehicle',a,b,s] *(random.randrange(80, 120, 2)/100)* (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                H[a, b, s] = round(intermediate_result/20,15)
        # market to collector
        for b in B:
            for c in C:
                intermediate_result = T['Light-Vehicle',b,c,s] * (random.randrange(80, 120, 2)/100)*(random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                H[b, c, s] = round(intermediate_result/20,15)
        # collector to recycler
        for c in C:
            for r in R:
                intermediate_result = T['Light-Vehicle',c,r,s] *(random.randrange(80, 120, 2)/100)* (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                H[c, r, s] = round(intermediate_result/10,15)
        # recycler to manufacturer
        for r in R:
            for m in M:
                intermediate_result = T[r,m,s] *(random.randrange(80, 120, 2)/100)* (random.randrange(Scenario[s]['cost']['Lower_Limit'], Scenario[s]['cost']['Upper_Limit'], 1)/100)
                H[r, m, s] = round(intermediate_result/4,15)

    # water consumption
    WU = {}
    for m in M:
        WU[m] = round( 17300000000* (10.2/37.7) *round(1302152,0)*1.5 *Man_cost[m] / ((Man_cost[m]*2)* total_demand)*(6.8/37.7),2) # sustainability report broken down to german market in liter
    for r in R:
        WU[r] = round(random.random()*2000000,2)

    # electric energy
    EE = {}
    # manufacturer
    for m in M:
        intermediate_result = 68.12 * K['Light-Vehicle',m,"Trend"]/ (Man_cost[m]*2)
        EE[m] = round(intermediate_result,6)
    # recycler
    for r in R:
        intermediate_result = 20 * K[r, "Trend"] *(random.randrange(80, 120, 2)/100)
        EE[r] = round(intermediate_result, 6)

    # pollution emitted
    PE = {}
    for m in M:
        PE[m] = round( 780000000* (10.2/37.7) *round(1302152,0)*1.5 *Man_cost[m] / ((Man_cost[m]*2)* total_demand)*(6.8/37.7),2) # sustainability report broken down to german market, in kg
    for r in R:
        PE[r] = - round(60 *(random.randrange(80, 120, 2)/100),2) # https://www.bundesverband-reifenhandel.de/themen/runderneuerung-von-reifen/runderneuerung-lkw-reifen/umwelt/'

    # fixed jobs opportunities
    FJO = {}

    # primary supplier
    for i in I:
        FJO[i] = random.randrange(500,1000,2)
    # backup supplier
    for j in J:
        FJO[j] = random.randrange(400,800,2)
    # manufacturer
    for m in M:
        FJO[m] = random.randrange(4000,6000,2)

    # distributor
    for a in A:
        FJO[a] = random.randrange(60,120,2)

    # collector
    for c in C:
        FJO[c] = random.randrange(60,120,2)

    # recycler
    for r in R:
        FJO[r] = random.randrange(400,800,2)


    # variable job opportunities
    VJO = {}
    for s in S:
        # primary supplier
        for i in I:
            VJO[i,s] = round(random.randrange(500,1000,2)/2 * (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100),2)

        # backup supplier
        for j in J:
            VJO[j, s] = round(random.randrange(400,800,2)/2* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100),2)

        # manufacturer
        for m in M:
            VJO[m, s] = round(random.randrange(2000,5000,2)/2* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100)/ (Man_cost[m]*2),2)

        # distributor
        for a in A:
            VJO[a, s] = round(random.randrange(100,200,2)/2* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100),2)

        # collector
        for c in C:
            VJO[c, s] = round(random.randrange(100,200,2)/2* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100),2)

        # recycler
        for r in R:
            VJO[r, s] = round(random.randrange(400,800,2)/2* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100),2)

    # establishment cost of information type f and information sharing center
    SC = {}
    IC = {}
    EX = {}
    for s in S:
        for f in F:
            SC[f,s] = round(random.randrange(2000,5000,1)* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100),2)
            IC[f,s] = round(random.randrange(10000,30000,1)* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100),2)
            EX[f,s] = round(random.randrange(2000,70000,1)* (random.randrange(Scenario[s]['demand']['Lower_Limit'], Scenario[s]['demand']['Upper_Limit'], 1)/100),2)




    return [RC, CC, LC, prob,N,G,T,FC,K,U,D,alpha, H, WU,EE,PE,FJO,VJO,SC,IC,EX]


