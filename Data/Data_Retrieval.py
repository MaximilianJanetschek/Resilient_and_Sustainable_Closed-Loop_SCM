from Data.DataManipulation import *
from random import seed
from random import random


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
    collector_locations = get_distributor_locations()
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

def get_parameters(I,J,M,A,B,C,R,P,W,S,F):
    filePath = "Data/parameters.p"

    if os.path.exists(filePath):
        parameters = pickle.load(open(filePath, "rb"))

    else:
        parameters = initialize_parameters(I,J,M,A,B,C,R,P,W,S,F)
        pickle.dump(parameters, open(filePath, "wb"))

    return parameters


def initialize_parameters(I,J,M,A,B,C,R,P,W,S,F):
    seed(115599)
    RC = {}
    raw_prices = {"Natrual Rubber": 1.96, "Syntetic Polymere":1.5, "Fillers":3.26}

    # natural rubber https://www.statista.com/statistics/727582/price-of-rubber-per-pound/
    # synthetic polymers https://www.ft.com/content/f97d653c-71f4-4b84-90ee-896b7bd5d299
    # Fillers https://wits.worldbank.org/trade/comtrade/en/country/All/year/2019/tradeflow/Exports/partner/MDA/product/400510

    final_tire_price = 100
    # raw data prices
    for w in W:
        for i in I:
            RC[w,i] = raw_prices[w]   # https://www.statista.com/statistics/727582/price-of-rubber-per-pound/
        for j in J:
            RC[w, j] = raw_prices[w] * 1.5

    # Fixed cost of contracting supplier
    CC = {}
    for i in I:
        CC[i] = 17596           # https://blog.iaccm.com/commitment-matters-tim-cummins-blog/the-cost-of-a-contract
    for j in J:
        CC[j] = 17596 * 1.5

    # Production Cost of tire type p
    LC = {}
    for p in P:
        for m in M:
            LC[p,m] = final_tire_price * 0.5

    prob = {}  # disruption probability in scenario s
    for s in S:
        prob[s] = round(random()*0.1,2)


    # disrupted capacitz of PS
    N = {}
    for s in S:
        for i in I:
            N[(i,s)] = round(random()*0.5,2)

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
                T[w,i,m,s] = 0.001 * distanceSupplierManufacturer[i,m] / 1000

    # manufacturer distributor
    distanceManufacturerDistributor=  get_distance_manufacturer_distributors(A)
    for s in S:
        for p in P:
            for (m,a) in distanceManufacturerDistributor:
                T[p,m,a,s] = 0.01 * distanceManufacturerDistributor[m,a] / 1000

    # distributor market
    distanceDistributorMarket = get_distance_distributor_customer(A)
    for s in S:
        for p in P:
            for (a,b) in distanceDistributorMarket:
                T[p,a,b,s] = 0.03*distanceDistributorMarket[a,b] / 1000



    # market collector
    distanceMarketCollector = get_distance_customer_collector(distanceDistributorMarket, C)
    for s in S:
        for p in P:
            for (b,c) in distanceMarketCollector:
                T[p,b,c,s] = 0.03*distanceMarketCollector[b,c] / 1000


    # collector recycling center
    distanceCollectorRecycling = get_distance_collector_recycling(R,C)
    for s in S:
        for p in P:
            for (c,r) in distanceCollectorRecycling:
                T[p,c,r,s] = 0.02 * distanceCollectorRecycling[c,r] / 1000


    # recycling manufacturer
    distanceRecyclingManufacturer = get_distance_recycling_manufacturer(R)
    print(distanceRecyclingManufacturer)
    for s in S:
        for (r,m) in distanceRecyclingManufacturer:
            T[r,m,s] = 0.005*distanceRecyclingManufacturer[r,m]

    # Fixed Cost
    FC = {}
    for m in M:
        FC[m] = 200000
    for a in A:
        FC[a] = 50000

    for c in C:
        FC[c] = 30000
    for r in R:
        FC[r] = 100000

    # capacity
    K = {}
    capacity_raw = {"Natrual Rubber": 4062713, "Syntetic Polymere": 1406324, "Fillers": 5156520}
    for s in S:
        # PS
        for w in W:
            for i in I:
                K[w,i,s] = capacity_raw[w] * 1.7
            for j in J:
                K[w,j,s] = capacity_raw[w] * 1.2
        for p in P:
            for m in M:
                K[p,m,s] = round(1302152,0)
            for a in A:
                K[p, a, s] = 260430*3
            for c in C:
                K[p, c, s] = round(260430*2,0)
        for r in R:
            K[r, s] = 578734*2

    # purchase prices
    U = {}
    for s in S:
        for p in P:
            for m in M:
                U[p,m,s] = final_tire_price*0.8
            for a in A:
                U[p, a, s] = final_tire_price
            for b in B:
                U[p, b, s] = final_tire_price*0.05
            for c in C:
                U[p, c, s] = 0.1*final_tire_price
        for r in R:
            U[r, s] = 0.2*final_tire_price

    # percentage scrapped
    alpha = {}
    for s in S:
        for b in B:
            for p in P:
                alpha[p,b,s] = round(random(),2)

    # demand of market b
    customer = get_population_by_district()
    total_population = sum_population(customer)
    total_demand = 5208606

    D = {}
    for s in S:
        for p in P:
            for b in customer.keys():
                demand = total_demand * (customer[b] / total_population)
                D[p,b,s] = round(demand,0)

    # polution emitted
    H = {}
    for s in S:
        # on transport to manufacturer
        for m in M:
            # from primary supplier
            for i in I:
               H[i,m,s] = T["Natrual Rubber",i,m,s]
            # from backup supplier
            for j in J:
                H[j,m,s] = T["Natrual Rubber",j,m,s]
            # manufacturer to distributor
            for a in A:
                H[m,a,s] = T['Light-Vehicle',m,a,s]

        # distributor to market
        for a in A:
            for b in B:
                H[a,b,s] = T['Light-Vehicle',a,b,s]

        # market to collector
        for b in B:
            for c in C:
                H[b,c,s] = T['Light-Vehicle',b,c,s]

        # collector to recycler
        for c in C:
            for r in R:
                H[c,r,s] = T['Light-Vehicle',c,r,s]

        # recycler to manufacturer
        for r in R:
            for m in M:
                H[r,m,s] = T[r,m,s]

    # water consumption
    WU = {}
    for m in M:
        WU[m] = round(random()*10000000,2)
    for r in R:
        WU[r] = round(random()*2000000,2)

    # electric energy
    EE = {}
    # manufacturer
    for m in M:
        EE[m] = 68.12 * K['Light-Vehicle',m,"Trend"]
    # recycler
    for r in R:
        EE[r] = 100 * K[r, "Trend"]

    # pollution emitted
    PE = {}
    for m in M:
        PE[m] = round(random()*2000000,2)
    for r in R:
        PE[r] = round(random()*200000,2)

    # fixed jobs opportunities
    FJO = {}

    # primary supplier
    for i in I:
        FJO[i] = round(random()*1000,2)
    # backup supplier
    for j in J:
        FJO[j] = round(random()*500,2)
    # manufacturer
    for m in M:
        FJO[m] = round(random()*10000,2)

    # distributor
    for a in A:
        FJO[a] = round(random()*100,2)

    # collector
    for c in C:
        FJO[c] = round(random()*100,2)

    # recycler
    for r in R:
        FJO[r] = round(random()*750,2)


    # variable job opportunities
    VJO = {}
    for s in S:
        # primary supplier
        for i in I:
            VJO[i,s] = round(random()*100,2)

        # backup supplier
        for j in J:
            VJO[j, s] = round(random()*50,2)

        # manufacturer
        for m in M:
            VJO[m, s] = round(random()*300,2)

        # distributor
        for a in A:
            VJO[a, s] = round(random()*200,2)

        # collector
        for c in C:
            VJO[c, s] = round(random()*200,2)

        # recycler
        for r in R:
            VJO[r, s] = round(random()*150,2)

    # establishment cost of information type f and information sharing center
    SC = {}
    IC = {}
    EX = {}
    for s in S:
        for f in F:
            SC[f,s] = round(random()*50,2)
            IC[f,s] = round(random()*30,2)
            EX[f,s] = round(random()*70,2)




    return [RC, CC, LC, prob,N,G,T,FC,K,U,D,alpha, H, WU,EE,PE,FJO,VJO,SC,IC,EX]