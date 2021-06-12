from Data.DataManipulation import *

def initialize_sets(I,J,M,A,B,C,R,P,W,S,F):
    # Primary Supplier
    I = ['PS_1','PS_2','PS_3']

    # Backup Supplier
    J = ['PS_1', 'PS_2', 'PS_3']

    # Manufacturer
    M = ["M 1, Hannover, Germany", "M 2, Korbach, Germany", "M 3, Otrokovice, Tschechien", "M 4, Puchov, Slowakai"]

    # Distributors
    distributor_locations = get_distributor_locations()
    counter = 1
    D = []
    for i in distributor_locations.keys():
        D.append("D-" + str(counter) + '-PLZ-' + str(i))
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

initialize_sets(I,J,M,A,B,C,R,P,W,S,F)