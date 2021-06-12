from Data.DataManipulation import *

def initialize_sets():
    I = []  # i Primary Supplier
    J = []  # j Backup Supplier
    M = []  # m manufacturers
    A = []  # a distributors
    B = []  # b markets
    C = []  # c collectors
    R = []  # r recyclers
    P = []  # p tire index
    W = []  # w raw material
    S = []  # s distribution scenario
    F = []  # f information shared

    # Primary Supplier
    I = ['PS_1','PS_2','PS_3']

    # Backup Supplier
    J = ['PS_1', 'PS_2', 'PS_3']

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

def initialize_parameters(I,J,M,A,B,C,R,P,W,S,F):
    RC = {}
    # raw data prices
    for w in W:
        for i in I:
            RC[(w,i)] = 0
        for j in J:
            RC[(w, j)] = 0

    # Fixed cost of contracting supplier
    CC = {}
    for i in I:
        CC[i] = 0
    for j in J:
        CC[j] = 0

    # Production Cost of tire type p
    LC = {}
    for p in P:
        LC[p] = 0

    p = {}  # disruption probability in scenario s
    for s in S:
        p[s] = 1/ len(S)

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
    distanceDistributorMarket = get_distance_distributor_customer()
    for s in S:
        for p in P:
            for (a,b) in distanceDistributorMarket:
                T[p,a,b,s] = distanceDistributorMarket[a,b] / 1000



    # market collector
    distanceMarketCollector = get_distance_customer_collector(distanceDistributorMarket)
    for s in S:
        for p in P:
            for (b,c) in distanceMarketCollector:
                T[p,b,c,s] = distanceMarketCollector[b,c] / 1000


    # collector recycling center
    distanceCollectorRecycling = get_distance_collector_recycling(R)
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

    D = {}
    H = {}
    WU = {}
    EE = {}
    PE = {}
    FJO = {}
    VJO = {}
    SC = {}
    IC = {}
    EX = {}

    return [RC, CC, LC, p,N,G,T,FC,K,U,D,alpha, H, WU,EE,PE,FJO,VJO,SC,IC,EX]






I = []   # i Primary Supplier
J = []   # j Backup Supplier
M = []   # m manufacturers
A = []   # a distributors
B = []   # b markets
C = []   # c collectors
R = []   # r recyclers
P = []   # p tire index
W = []   # w raw material
S = []   # s distribution scenario
F = []   # f information shared

[I,J,M,A,B,C,R,P,W,S,F] = initialize_sets()
initialize_parameters(I,J,M,A,B,C,R,P,W,S,F)