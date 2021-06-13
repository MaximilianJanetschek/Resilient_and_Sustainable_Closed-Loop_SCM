from Data.DataManipulation import *

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
    RC = {}
    # raw data prices
    for w in W:
        for i in I:
            RC[w,i] = 0
        for j in J:
            RC[w, j] = 0

    # Fixed cost of contracting supplier
    CC = {}
    for i in I:
        CC[i] = 0
    for j in J:
        CC[j] = 0

    # Production Cost of tire type p
    LC = {}
    for p in P:
        for m in M:
            LC[p,m] = 0

    prob = {}  # disruption probability in scenario s
    for s in S:
        prob[s] = round(1 / len(S),4)
        print(prob[s])


    # disrupted capacitz of PS
    N = {}
    for s in S:
        for i in I:
            N[(i,s)] = 0

    # quantity of raw material
    G = {}
    for w in W:
        G[w] = 0

    # Transportation Cost
    T = {}
    # primary supplier to manufacturer
    distanceSupplierManufacturer = get_distance_supplier_manufacturer()
    for s in S:
        for w in W:
            for (i,m) in distanceSupplierManufacturer.keys():
                T[w,i,m,s] = distanceSupplierManufacturer[i,m] / 1000

    # manufacturer distributor
    distanceManufacturerDistributor=  get_distance_manufacturer_distributors(A)
    print(distanceManufacturerDistributor)
    for s in S:
        for p in P:
            for (m,a) in distanceManufacturerDistributor:
                T[p,m,a,s] = distanceManufacturerDistributor[m,a] / 1000

    # distributor market
    distanceDistributorMarket = get_distance_distributor_customer(A)
    for s in S:
        for p in P:
            for (a,b) in distanceDistributorMarket:
                T[p,a,b,s] = distanceDistributorMarket[a,b] / 1000



    # market collector
    distanceMarketCollector = get_distance_customer_collector(distanceDistributorMarket, C)
    for s in S:
        for p in P:
            for (b,c) in distanceMarketCollector:
                T[p,b,c,s] = distanceMarketCollector[b,c] / 1000


    # collector recycling center
    distanceCollectorRecycling = get_distance_collector_recycling(R,C)
    for s in S:
        for p in P:
            for (c,r) in distanceCollectorRecycling:
                T[p,c,r,s] = distanceCollectorRecycling[c,r] / 1000


    # recycling manufacturer
    distanceRecyclingManufacturer = get_distance_recycling_manufacturer(R)
    print(distanceRecyclingManufacturer)
    for s in S:
        for (r,m) in distanceRecyclingManufacturer:
            T[r,m,s] = distanceRecyclingManufacturer[r,m]

    # Fixed Cost
    FC = {}
    for m in M:
        FC[m] = 0
    for a in A:
        FC[a] = 0

    for c in C:
        FC[c] = 0
    for r in R:
        FC[r] = 0

    # capacity
    K = {}

    for s in S:
        # PS
        for w in W:
            for i in I:
                K[w,i,s] = 0
            for j in J:
                K[w,j,s] = 0
        for p in P:
            for m in M:
                K[p,m,s] = 0
            for a in A:
                K[p, a, s] = 0
            for c in C:
                K[p, c, s] = 0
        for r in R:
            K[r, s] = 0

    # purchase prices
    U = {}
    for s in S:
        for p in P:
            for m in M:
                U[p,m,s] = 0
            for a in A:
                U[p, a, s] = 0
            for b in B:
                U[p, b, s] = 0
            for c in C:
                U[p, c, s] = 0
        for r in R:
            U[r, s] = 0

    # percentage scrapped
    alpha = {}
    for s in S:
        for r in R:
            alpha[r,s] = 0

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
               H[i,m,s] = 0
            # from backup supplier
            for j in J:
                H[j,m,s] = 0
            # manufacturer to distributor
            for a in A:
                H[m,a,s] = 0

        # distributor to market
        for a in A:
            for b in B:
                H[a,b,s] = 0

        # market to collector
        for b in B:
            for c in C:
                H[b,c,s] = 0

        # collector to recycler
        for c in C:
            for r in R:
                H[c,r,s] = 0

        # recycler to manufacturer
        for r in R:
            for m in M:
                H[r,m,s] = 0

    # water consumption
    WU = {}
    for m in M:
        WU[m] = 0
    for r in R:
        WU[r] = 0

    # electric energy
    EE = {}
    # manufacturer
    for m in M:
        EE[m] = 0
    # recycler
    for r in R:
        EE[r] = 0

    # pollution emitted
    PE = {}
    for m in M:
        PE[m] = 0
    for r in R:
        PE[r] = 0

    # fixed jobs opportunities
    FJO = {}

    # primary supplier
    for i in I:
        FJO[i] = 0
    # backup supplier
    for j in J:
        FJO[j] = 0
    # manufacturer
    for m in M:
        FJO[m] = 0

    # distributor
    for a in A:
        FJO[a] = 0

    # collector
    for c in C:
        FJO[c] = 0

    # recycler
    for r in R:
        FJO[r] = 0


    # variable job opportunities
    VJO = {}
    for s in S:
        # primary supplier
        for i in I:
            VJO[i,s] = 0

        # backup supplier
        for j in J:
            VJO[j, s] = 0

        # manufacturer
        for m in M:
            VJO[m, s] = 0

        # distributor
        for a in A:
            VJO[a, s] = 0

        # collector
        for c in C:
            VJO[c, s] = 0

        # recycler
        for r in R:
            VJO[r, s] = 0

    # establishment cost of information type f and information sharing center
    SC = {}
    IC = {}
    EX = {}
    for s in S:
        for f in F:
            SC[f,s] = 0
            IC[f,s] = 0
            EX[f,s] = 0




    return [RC, CC, LC, prob,N,G,T,FC,K,U,D,alpha, H, WU,EE,PE,FJO,VJO,SC,IC,EX]