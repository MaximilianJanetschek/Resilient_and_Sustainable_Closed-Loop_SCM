import gurobipy as gurobi
import numpy as np


# Data import
''' Index ''' # do not use 1,..,n rahter some unique such that parameters are hashable
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

# get Set lengths
len_I = len(I)
len_J = len(J)
len_M = len(M)
len_A = len(A)
len_B = len(B)
len_C = len(C)
len_R = len(R)
len_P = len(P)
len_W = len(W)
len_S = len(S)
len_F = len(F)



''' Parameters '''
RawMaterial_Cost_PrimarySupplier = np.ndarray(shape=(W,I), dtype=float)
RawMaterial_Cost_BackupSupplier = np.ndarray(shape=(W,J),dtype=float)
Contracting_Cost_PrimarySupplier = np.ndarray(shape=(I),dtype=float)
Contracting_Cost_BackupSupplier = np.ndarray(shape=(J),dtype=float)
Production_Cost_Manufacturer = np.ndarray(shape=(P,M), dtype=float)
Disruption_probability = np.ndarray(shape=(S), dtype=float)                     # disruption probability in scenario s
Disrupted_Capacity_PrimarySupplier = np.ndarray(shape=(I,S), dtype=float)       # disrupted capacity of manufactuer
RawMaterial_for_Tire = np.ndarray(shape=(I,S), dtype=float)                     # quantity for producing one final product
T_w_ij_m_s = np.ndarray(shape=(I,s), dtype=float)                               # transportation cost of material w to supplier manufacturer m in scenario s
T_p_m_a_s = np.ndarray(shape=(i,s), dtype=float)                                # manufacturer to distributor
T_p_a_b_s = np.ndarray(shape=(i,s), dtype=float)                                # distributor to market
T_p_b_c_s = np.ndarray(shape=(i,s), dtype=float)                                # market to collector
T_p_c_r_s = np.ndarray(shape=(i,s), dtype=float)                                # collector to recycler
T_r_m_s = np.ndarray(shape=(i,s), dtype=float)                                  # recycler manufacturer
Fixed_cost= np.ndarray(shape=(i,s), dtype=float)                                # for manufacturer, distributor, collector, recycler
Capacity_s = np.ndarray(shape=(i,s), dtype=float)                               # for primary supplier, backup supplier, manufacturer, distributor, collecotr, recyler
Purchasing_Price= np.ndarray(shape=(i,s), dtype=float)
Demand= np.ndarray(shape=(i,s), dtype=float)
Percentage_Scrapped = np.ndarray(shape=(i,s), dtype=float)
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
Production_Quantity = SCM_Model.addVars(p,m,s,vtype=gurobi.GRB.continuous, name="Production_Quantity")
RawMaterial_Transferred_PrimarySupplier = SCM_Model.addVars(w,i,m,s,vtype=gurobi.GRB.continuous, name="RawMaterial_Transferred_PrimarySupplier")
RawMaterial_Transferred_BackupSupplier = SCM_Model.addVars(w,j,m,s,vtype=gurobi.GRB.continuous, name="RawMaterial_Transferred_BackupSupplier")
Product_Transferred_Manufacturer = SCM_Model.addVars(p,m,a,s,vtype=gurobi.GRB.continuous, name="Product_Transferred_Manufacturer")
Product_Transferred_Distributor = SCM_Model.addVars(p,a,b,s,vtype=gurobi.GRB.continuous, name="Product_Transferred_Distributor")
Product_Transferred_Distributor = SCM_Model.addVars(p,b,c,s,vtype=gurobi.GRB.continuous, name="Product_Transferred_Distributor")
Product_Transferred_Collector = SCM_Model.addVars(p,c,r,s,vtype=gurobi.GRB.continuous, name="Product_Transferred_Collector")
Product_Transferred_Recycler = SCM_Model.addVars(r,m,s,vtype=gurobi.GRB.continuous, name="Product_Transferred_Recycler")
Information_Visible = SCM_Model.addVars(f,s,vtype=gurobi.GRB.continuous, name="Information_Visible")
PrimarySupplier = SCM_Model.addVars(i,vtype=gurobi.GRB.continuous, name="PrimarySupplie")
BackupSupplier = SCM_Model.addVars(j,vtype=gurobi.GRB.continuous, name="BackupSupplier")
Manufacturer = SCM_Model.addVars(m,vtype=gurobi.GRB.continuous, name="Manufacturer")
Distributor = SCM_Model.addVars(a,vtype=gurobi.GRB.continuous, name="Distributor")
Collector = SCM_Model.addVars(c,vtype=gurobi.GRB.continuous, name="Collector")
Recycler = SCM_Model.addVars(r,vtype=gurobi.GRB.continuous, name="Recycler")
Information_Sharing_Center = SCM_Model.addVars(f,vtype=gurobi.GRB.continuous, name="Information_Sharing_Center")
Information_Security_Center = SCM_Model.addVars(f,vtype=gurobi.GRB.continuous, name="Information_Security_Center")



'''Objective Functions'''

'''Economic'''
obj_Economic = gurobi.LinExpr()

# Fixed Cost
obj_Economic_Fixed = gurobi.LinExpr()
obj_Economic_Fixed += gurobi.quicksum(FC[m] * E[m] for m in M) + gurobi.quicksum(FC[a] * E[a] for a in A) +
                gurobi.quicksum(FC[c] * E[c] for c in C) + gurobi.quicksum(FC[r] * E[r] for r in R) +
                gurobi.quicksum(CC[i] * PS[i] for i in I) + gurobi.quicksum(CC[i] * BS[i] for j in J) +
                gurobi.quicksum(gurobi.quicksum(RC[w][i] * PS[i] for i in I) + gurobi.quicksum(RC[w][j] * BS[j] for j in J) for w in W)

# Variable Cost
obj_Economic_Variable = gurobi.LinExpr()
obj_Economic_Variable += gurobi.quicksum(p[s] *  gurobi.quicksum(IS[f]*IC[f,s]for f in F)
                                        + gurobi.quicksum(SCU[f]*SC[f,s]for f in F) + gurobi.quicksum(gurobi.quicksum(L[p,m,s] *LC[p,m]for m in M)for p in P)
                                         + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(U[p,m,s] * Q [p,m,a,s] for a in A) for m in M)for p in P)
                                         + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(U[p,a,s] * Q [p,a,b,s] for b in B) for a in A)for p in P)
                                         + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(U[p,b,s] * Q [p,b,c,s] for c in C) for b in P)for p in P)
                                         + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(U[p,c,s] * Q [p,c,r,s] for r in R) for c in C)for p in P)
                                         + gurobi.quicksum(gurobi.quicksum(U[p,r,s] * Q [r,m,s] for m in M) for r in R)
for s in S)


# Transportation Cost
obj_Economic_Transportation = gurobi.LinExpr()
obj_Economic_Transportation += gurobi.quicksum( p[s]
        + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[w,i,m,s] * Q [w,i,m,s] for m in M)for i in I)for w in W)
        +  gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[w,j,m,s] * Q [w,j,m,s] for m in M)for j in J)for w in W)
        + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[w,i,m,s] * Q [w,i,m,s] for m in M)for i in I)for p in P)
        + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[w, i, m, s] * Q[w, i, m, s] for m in M) for i in I) for w in W)



                                                for s in S)


# summing all up
obj_Economic = obj_Economic_Fixed + obj_Economic_Variable + obj_Economic_Transportation



'''Environmental'''
obj_Environmental = gurobi.LinExpr()

'''Social'''
obj_Social = gurobi.LinExpr()

'''Constraints'''
# Raw Material required for one unit
for s in S:
    for m in M:
        SCM_Model.addConstr(
            gurobi.quicksum( gurobi.quicksum((1-p[s]) * Q[w,i,m,s] for i in I) for w in W) +
            gurobi.quicksum(gurobi.quicksum(Q[w,j,m,s]for j in J)for w in W) == gurobi.quicksum(gurobi.quicksum(L[p,m,s]*G[w] for p in P)for w in W)
        )

# Only part of collected material can be reused
for s in S:
    for p in P:
        for b in B:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,b,c,s] for c in C) <= D[p,b,s] *  Percentage_Scrapped [p,b,s]
            )

# flow constraints
for s in S:
    for m in M:
        SCM_Model.addConstr(
            gurobi.quicksum(L[p,m,s] for p in P) + gurobi.quicksum(Q[r,m,s] for r in R) <=
            gurobi.quicksum(gurobi.quicksum(Q[p,m,a,s]for a in A)for p in P)
        )

    for p in P:
        for a in A:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,m,a,s] for m in M) == gurobi.quicksum(Q[p,a,b,s] for b in B)
            )

        for b in B:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,a,b,s] for a in A) == D[p,b,s]
            )

            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,a,b,s] for a in A) >= gurobi.quicksum(Q[p,b,c,s] * Percentage_Scrapped[p,b,s] for c in C)
            )

        for c in C:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,b,c,s] * Percentage_Scrapped[p,b,s] for b in B)
            )

        for r in R:
            SCM_Model.addConstr(
                gurobi.quicksum(gurobi.quicksum(Q[p,c,r,s]for c in C)for p in P) ==
                gurobi.quicksum(Q[r,m,s] for m in M)
            )

# capacity constraint
for s in S:
    for p in P:
        for m in M:
            SCM_Model.addConstr(
                L[p,m,s] <= K[p,m,s]
            )

# primary and backup supplier capacity constraint
for s in S:
    for w in W:
        for i in I:
            SCM_Model.addConstr(
             gurobi.quicksum(Q[w,i,m,s] for m in M) <= K[w,i,s] * (1 - N[i,s])
            )

        for j in J:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[w,j,m,s]) <= K[w,j,s]
            )



# capacity constraint for manufacturing, dsitributino, collecting, recycling centers
for s in S:
    for p in P:

        for m in M:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,m,a,s] for a in A) <= K[p,m,s] * E[m]
            )

        for a in A:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,a,b,s] for b in B) <= K[p,a,s] * E[a]
            )

        for c in C:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,a,b,s]for r in R) <= K[p,c,s] * E[c]
            )

    for r in R:
        SCM_Model.addConstr(
            gurobi.quicksum(Q[r,m,s] for m in M) <= K[r,s] * E[r]
        )

# Visibilitz percent is the informatin shared through an informatioon sharing system
for s in S:
    for f in F:
        SCM_Model.addConstr(
            IS[f] * EX[f, s] * (1 - p[s]) <= V[f,s]
        )

# implementation of the informatin sharing system constraint
SCM_Model.addConstr(gurobi.quicksum(IS[f] for f in F) == 1 )

SCM_Model.addConstr(gurobi.quicksum(SCU[f] for f in F) == 1 )


'''Constraints'''

'''Optimization'''
