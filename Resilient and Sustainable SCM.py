import gurobipy as gurobi
import numpy as np


# Data import
''' Index '''
i = 0   # i Primary Supplier
j = 0   # j Backup Supplier
m = 0   # m manufacturers
a = 0   # a distributors
b = 0   # b markets
c = 0   # c collectors
r = 0   # r recyclers
p = 0   # p tire index
w = 0   # w raw material
s = 0   # s distribution scenario
f = 0   # f information shared

''' Parameters '''
RawMaterial_Cost_PrimarySupplier = np.ndarray(shape=(w,i), dtype=float)
RawMaterial_Cost_BackupSupplier = np.ndarray(shape=(w,j),dtype=float)
Contracting_Cost_PrimarySupplier = np.ndarray(shape=(i),dtype=float)
Contracting_Cost_BackupSupplier = np.ndarray(shape=(j),dtype=float)
Production_Cost_Manufacturer = np.ndarray(shape=(p,m), dtype=float)
Disruption_probability = np.ndarray(shape=(s), dtype=float)                     # disruption probability in scenario s
Disrupted_Capacity_PrimarySupplier = np.ndarray(shape=(i,s), dtype=float)       # disrupted capacity of manufactuer
RawMaterial_for_Tire = np.ndarray(shape=(i,s), dtype=float)                     # quantity for producing one final product
T_w_ij_m_s = np.ndarray(shape=(i,s), dtype=float)                               # transportation cost of material w to supplier manufacturer m in scenario s
T_p_m_a_s = np.ndarray(shape=(i,s), dtype=float)                                # manufacturer to distributor
T_p_a_b_s = np.ndarray(shape=(i,s), dtype=float)                                # distributor to market
T_p_b_c_s = np.ndarray(shape=(i,s), dtype=float)                                # market to collector
T_p_c_r_s = np.ndarray(shape=(i,s), dtype=float)                                # collector to recycler
T_r_m_s = np.ndarray(shape=(i,s), dtype=float)                                  # recycler manufacturer
Fixed_cost= np.ndarray(shape=(i,s), dtype=float)                                # for manufacturer, distributor, collector, recycler
Capacity_s = np.ndarray(shape=(i,s), dtype=float)                               # for primary supplier, backup supplier, manufacturer, distributor, collecotr, recyler
Purchasing_Price= np.ndarray(shape=(i,s), dtype=float)
Demand= np.ndarray(shape=(i,s), dtype=float)
Percentage_Scrapped= np.ndarray(shape=(i,s), dtype=float)
Pollution_Emitted= np.ndarray(shape=(i,s), dtype=float)
Water_Consumption= np.ndarray(shape=(i,s), dtype=float)                         # manufactuer, recycler
Electricity_Consumption= np.ndarray(shape=(i,s), dtype=float)                   # manufactuer, recycler
Pollution= np.ndarray(shape=(i,s), dtype=float)                                 # manufacturer, recycler
Fixed_Job_Opportunities= np.ndarray(shape=(i,s), dtype=float)                   # supplier, manufacturer, distributor, collector, recycler
Variable_Job_Opportunities= np.ndarray(shape=(i,s), dtype=float)                # supplier, manufacturer, distributor, collector, recycler
Security_System_s = np.ndarray(shape=(i,s), dtype=float)                        #
information_sharing_f_s= np.ndarray(shape=(i,s), dtype=float)                   # cost information sharing of kind f
percentage_of_information_exchange= np.ndarray(shape=(i,s), dtype=float)

'''Optimization Model'''
SCM_Model = gurobi.Model('Resilient and Sustainable SCM')

'''Decision Variables'''

'''Objective Functions'''

'''Constraints'''

'''Optimization'''
