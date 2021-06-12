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
    R = []

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






    FC = {}
    K = {}
    U = {}
    D = {}
    alpha = {}
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