import gurobipy as gurobi


# Data import
''' Index '''
# i Primary Supplier
# j Backup Supplier
# m manufacturers
# a distributors
# b markets
# c collectors
# r recyclers
# p tire index
# w raw material
# s distribution scenario
# f information shared

''' Parameters '''
RC_w_ij
CC_ij
LC_p_m
p_s # disruption probability in scenario s
N_i_s # disrupted capacity of manufactuer
G_w # quantity for producing one final product
T_w_ij_m^s # transportation cost of material w to supplier manufacturer m in scenario s
T_p_m_a^s # manufacturer to distributor
T_p_a_b^s # distributor to market
T_p_b_c^s # market to collector
T_p_c_r^s # collector to recycler
T_r_m^s # recycler manufacturer
Fixed_cost # for manufacturer, distributor, collector, recycler
Capacity^s # for primary supplier, backup supplier, manufacturer, distributor, collecotr, recyler
Purchasing Price
Demand
Percentage Scrapped
Pollution_Emitted
Water_Consumption # manufactuer, recycler
Electricity_Consumption # manufactuer, recycler
Pollution # manufacturer, recycler
Fixed_Job_Opportunities # supplier, manufacturer, distributor, collector, recycler
Variable_Job_Opportunities # supplier, manufacturer, distributor, collector, recycler
Security_System^s #
information_sharing_f^s # cost information sharing of kind f
percentage_of_information_exchange









# Model
SCM_Model = gurobi.Model('Resilient and Sustainable SCM')

# Optimization

# Solution
