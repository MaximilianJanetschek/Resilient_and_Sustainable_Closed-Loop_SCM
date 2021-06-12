import gurobipy as gurobi
import numpy as np
from Data.Data_Retrieval import *


# Data import
''' Index ''' # do not use 1,..,n rahter some unique such that parameters are hashable

[I,J,M,A,B,C,R,P,W,S,F] = initialize_sets()



''' Parameters '''
RC = {}
CC = {}
LC = {}
p  = {}     # disruption probability in scenario s
N  = {}
G = {}
T = {}
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







'''Optimization Model'''
SCM_Model = gurobi.Model('Resilient and Sustainable SCM')

'''Decision Variables'''
L = SCM_Model.addVars(P,M,S,vtype=gurobi.GRB.continuous, name="Production_Quantity")

Production_Variable = gurobi.tuplelist()
Production_Variable += [(w,i,m,s) for w in W for i in I for m in M for s in S]
Production_Variable += [(w,j,m,s) for w in W for j in J for m in M for s in S]
Production_Variable += [(p,m,a,s) for p in P for m in M for a in A for s in S]
Production_Variable += [(p,b,c,s) for p in P for b in B for c in C for s in S]
Production_Variable += [(p,c,r,s) for p in P for c in C for r in R for s in S]
Production_Variable += [(r,m,s) for r in R for m in M for s in S]
Q = SCM_Model.addVars(Production_Variable,vtype=gurobi.GRB.continuous, name="RawMaterial_Transferred_PrimarySupplier")


V = SCM_Model.addVars(F,S,vtype=gurobi.GRB.continuous, name="Information_Visible")

PS = SCM_Model.addVars(I,vtype=gurobi.GRB.continuous, name="PrimarySupplie")
BS = SCM_Model.addVars(J,vtype=gurobi.GRB.continuous, name="BackupSupplier")

Established_Variable = gurobi.tuplelist()
Established_Variable += [(m) for m in M]
Established_Variable += [(a) for a in A]
Established_Variable += [(b) for b in B]
Established_Variable += [(c) for c in C]
Established_Variable += [(r) for r in R]
E = SCM_Model.addVars(Established_Variable,vtype=gurobi.GRB.continuous, name="Established")

SCU = SCM_Model.addVars(F,vtype=gurobi.GRB.continuous, name="Information_Sharing_Center")
IS = SCM_Model.addVars(F,vtype=gurobi.GRB.continuous, name="Information_Security_Center")



'''Objective Functions'''

'''Economic'''
obj_Economic = gurobi.LinExpr()

# Fixed Cost
obj_Economic_Fixed = gurobi.LinExpr()
obj_Economic_Fixed += gurobi.quicksum(FC[m] * E[m] for m in M) + gurobi.quicksum(FC[a] * E[a] for a in A)
+ gurobi.quicksum(FC[c] * E[c] for c in C) + gurobi.quicksum(FC[r] * E[r] for r in R)
+gurobi.quicksum(CC[i] * PS[i] for i in I) + gurobi.quicksum(CC[i] * BS[i] for j in J)\
+gurobi.quicksum(gurobi.quicksum(RC[w][i] * PS[i] for i in I)
                 +gurobi.quicksum(RC[w][j] * BS[j] for j in J) for w in W)

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
        + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[p,m,a,s] * Q [p,m,a,s] for a in A)for m in M)for p in P)
        + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[p,a,b,s] * Q[p,a,b,s] for b in B) for a in A) for p in P)
+ gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[p,b,c,s] * Q[p,b,c,s] for c in C) for b in B) for p in P)
+ gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[p,c,r,s] * Q[p,c,r,s] for r in R) for c in C) for p in P)
+ gurobi.quicksum(gurobi.quicksum(T[r,m,s] * Q[r,m,s] for r in R) for m in M)
                                                for s in S)


# summing all up
obj_Economic = obj_Economic_Fixed + obj_Economic_Variable + obj_Economic_Transportation


'''Environmental'''
obj_Environmental = gurobi.LinExpr()

# pollution emitted by Value Adding
obj_Environmental_Pol_Value_Adding = gurobi.LinExpr()
obj_Environmental_Pol_Value_Adding += gurobi.quicksum(WU[m] * E[m] for m in M) + gurobi.quicksum(WU[r]*E[r]for r in R)
+ gurobi.quicksum(EE[m]*E[m]for m in M) + gurobi.quicksum(EE[r]*E[r]for r in R) + gurobi.quicksum(PE[m]*E[m]for m in M)
+ gurobi.quicksum(PE[r]*E[r]for r in R)

# pollution emitted by transport
obj_Environmental_Pol_Transport = gurobi.LinExpr()
obj_Environmental_Pol_Transport += gurobi.quicksum(
    gurobi.quicksum(H[i,m,s]*Q[w,i,m,s] for w in W for i in I for m in M)
    + gurobi.quicksum(H[j,m,s]*Q[w,j,m,s] for w in W for j in J for m in M)
    + gurobi.quicksum(H[m,a,s]*Q[p,m,a,s] for p in P for m in M for a in A)
    + gurobi.quicksum(H[a,b,s]*Q[p,a,b,s] for p in P for a in A for b in B)
    + gurobi.quicksum(H[b,c,s]*(Q[p,b,c,s]*alpha[p,b,s]) for p in P for b in B for c in C)
    + gurobi.quicksum(H[c,r,s]*Q[p,c,r,s] for p in P for c in C for r in R)
    + gurobi.quicksum(H[r,m,s]*Q[r,m,s] for r in R for m in M)

    for s in S
)

obj_Environmental = obj_Environmental_Pol_Transport + obj_Environmental_Pol_Value_Adding


'''Social'''
obj_Social = gurobi.LinExpr()

# Fixed job opportunities
obj_Social_Fixed_Ops = gurobi.LinExpr()
obj_Social_Fixed_Ops += gurobi.quicksum(FJO[i] * PS[i] for i in I) + gurobi.quicksum(FJO[j] * BS[j] for j in J) + gurobi.quicksum(FJO[m] * E[m] for m in M) + gurobi.quicksum(FJO[a] * E[a] for a in A) + gurobi.quicksum(FJO[c] * E[c] for c in C)+ gurobi.quicksum(FJO[r] * E[r] for r in R)


# variable job opportunities
obj_Social_Variable_Ops = gurobi.LinExpr()
obj_Social_Variable_Ops += gurobi.quicksum(
    gurobi.quicksum(VJO[i,s] * (Q[w,i,m,s] / (K[w,i,s] * (1 - N[i,s]))) for i in I)
    + gurobi.quicksum(VJO[j,s] * (Q[w,j,m,s] / (K[w,j,s])) for j in J)
    + gurobi.quicksum(VJO[m,s] * (Q[p,m,a,s] / (K[p,m,s])) for m in M)
    + gurobi.quicksum(VJO[a, s] * (Q[p, a, b, s] / (K[p, a, s])) for a in A)
    + gurobi.quicksum(VJO[c, s] * (Q[p, c, r, s] / (K[p, c, s])) for c in C)
    + gurobi.quicksum(VJO[r, s] * (Q[r, m, s] / (K[r, s])) for r in R)
    for s in S
)



obj_Social = obj_Social_Fixed_Ops + obj_Social_Variable_Ops



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
                gurobi.quicksum(Q[p,b,c,s] for c in C) <= D[p,b,s] *  alpha [p,b,s]
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
                gurobi.quicksum(Q[p,a,b,s] for a in A) >= gurobi.quicksum(Q[p,b,c,s] * alpha[p,b,s] for c in C)
            )

        for c in C:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[p,b,c,s] * alpha[p,b,s] for b in B)
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



'''Optimization'''

SCM_Model.setObjective(obj_Environmental,gurobi.GRB.MINIMIZE)
SCM_Model.update()
SCM_Model.optimize()



"""
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
"""