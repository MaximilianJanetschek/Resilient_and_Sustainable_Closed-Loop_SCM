import gurobipy as gurobi
import numpy as np
from Data.Data_Retrieval import *



def get_multi_objective_model(indices,parameters):
    [I, J, M, A, B, C, R, P, W, S, F] = indices
    [RC, CC, LC, prob, N, G, T, FC, K, U, D, alpha, H, WU, EE, PE, FJO, VJO, SC, IC, EX] = parameters
    '''Optimization Model'''
    SCM_Model = gurobi.Model('Resilient and Sustainable SCM')

    '''Decision Variables'''
    L = SCM_Model.addVars(P,M,S,vtype=gurobi.GRB.CONTINUOUS, name="Production_Quantity")

    Production_Variable = gurobi.tuplelist()
    Production_Variable += [(w,i,m,s) for w in W for i in I for m in M for s in S]
    Production_Variable += [(w,j,m,s) for w in W for j in J for m in M for s in S]
    Production_Variable += [(p,m,a,s) for p in P for m in M for a in A for s in S]
    Production_Variable += [(p,a,b,s) for p in P for a in A for b in B for s in S]
    Market_Data = [(p, a, b, s) for p in P for a in A for b in B for s in S]
    Production_Variable += [(p,b,c,s) for p in P for b in B for c in C for s in S]
    Production_Variable += [(p,c,r,s) for p in P for c in C for r in R for s in S]
    Production_Variable += [(r,m,s,"dummy") for r in R for m in M for s in S]
    seen = set()
    for key in Production_Variable:
        if key in seen:
            print(key)
        else:
            seen.add(key)

    Q = SCM_Model.addVars(Production_Variable,vtype=gurobi.GRB.CONTINUOUS, name="Flow")


    V = SCM_Model.addVars(F,S,vtype=gurobi.GRB.CONTINUOUS, name="Information_Visible")

    PS = SCM_Model.addVars(I,vtype=gurobi.GRB.BINARY, name="PrimarySupplie")
    BS = SCM_Model.addVars(J,vtype=gurobi.GRB.BINARY, name="BackupSupplier")

    Established_Variable = gurobi.tuplelist()
    Established_Variable += [(m) for m in M]
    Established_Variable += [(a) for a in A]
    Established_Variable += [(c) for c in C]
    Established_Variable += [(r) for r in R]

    E = SCM_Model.addVars(Established_Variable,vtype=gurobi.GRB.BINARY, name="Established")

    Variable = {'E': E, 'E indices': Established_Variable, 'Q':Q, 'Q indices':Market_Data, 'PS':PS,'PS_indices':I ,'BS':BS,'BS_indices':J}
    SCU = SCM_Model.addVars(F,vtype=gurobi.GRB.BINARY, name="Information_Sharing_Center")
    IS = SCM_Model.addVars(F,vtype=gurobi.GRB.BINARY, name="Information_Security_Center")



    '''Objective Functions'''

    '''Economic'''
    obj_Economic = gurobi.LinExpr()

    # Fixed Cost
    obj_Economic_Fixed = gurobi.LinExpr()
    obj_Economic_Fixed += gurobi.quicksum(FC[m] * E[m] for m in M) + gurobi.quicksum(FC[a] * E[a] for a in A)
    obj_Economic_Fixed += gurobi.quicksum(FC[c] * E[c] for c in C) + gurobi.quicksum(FC[r] * E[r] for r in R)+gurobi.quicksum(CC[i] * PS[i] for i in I) + gurobi.quicksum(CC[j] * BS[j] for j in J)
    obj_Economic_Fixed += gurobi.quicksum(gurobi.quicksum(RC[w,i] * PS[i] for i in I) + gurobi.quicksum(RC[w,j] * BS[j] for j in J) for w in W)

    # Variable Cost
    obj_Economic_Variable = gurobi.LinExpr()

    obj_Economic_Variable += gurobi.quicksum(prob[s] * gurobi.quicksum(IS[f]*IC[f,s] for f in F)for s in S)
    obj_Economic_Variable +=  gurobi.quicksum(prob[s] * gurobi.quicksum(SCU[f]*SC[f,s]for f in F) + gurobi.quicksum(gurobi.quicksum(L[p,m,s] *LC[p,m]for m in M)for p in P)
                                             + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(U[p,m,s] * Q [p,m,a,s] for a in A) for m in M)for p in P)
                                             + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(U[p,a,s] * Q [p,a,b,s] for b in B) for a in A)for p in P)
                                             + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(U[p,b,s] * Q [p,b,c,s] for c in C) for b in B)for p in P)
                                             + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(U[p,c,s] * Q [p,c,r,s] for r in R) for c in C)for p in P)
                                             + gurobi.quicksum(gurobi.quicksum(U[r,s] * Q [r,m,s,"dummy"] for m in M) for r in R)
    for s in S)


    # Transportation Cost
    obj_Economic_Transportation = gurobi.LinExpr()
    obj_Economic_Transportation += gurobi.quicksum( prob[s]
            + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[w,i,m,s] * Q [w,i,m,s] for m in M)for i in I)for w in W)
            +  gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[w,j,m,s] * Q [w,j,m,s] for m in M)for j in J)for w in W)
            + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[p,m,a,s] * Q [p,m,a,s] for a in A)for m in M)for p in P)
            + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[p,a,b,s] * Q[p,a,b,s] for b in B) for a in A) for p in P)
    + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[p,b,c,s] * Q[p,b,c,s] for c in C) for b in B) for p in P)
    + gurobi.quicksum(gurobi.quicksum(gurobi.quicksum(T[p,c,r,s] * Q[p,c,r,s] for r in R) for c in C) for p in P)
    + gurobi.quicksum(gurobi.quicksum(T[r,m,s] * Q[r,m,s,"dummy"] for r in R) for m in M)
                                                    for s in S)


    # summing all up
    obj_Economic = obj_Economic_Fixed + obj_Economic_Variable + obj_Economic_Transportation


    '''Environmental'''
    obj_Environmental = gurobi.LinExpr()

    # pollution emitted by Value Adding
    obj_Environmental_Pol_Value_Adding = gurobi.LinExpr()
    obj_Environmental_Pol_Value_Adding += gurobi.quicksum(WU[m] * E[m] for m in M) + gurobi.quicksum(WU[r]*E[r]for r in R) + gurobi.quicksum(EE[m]*E[m]for m in M) + gurobi.quicksum(EE[r]*E[r]for r in R) + gurobi.quicksum(PE[m]*E[m]for m in M)+ gurobi.quicksum(PE[r]*E[r]for r in R)

    # pollution emitted by transport
    obj_Environmental_Pol_Transport = gurobi.LinExpr()
    obj_Environmental_Pol_Transport += gurobi.quicksum(
        gurobi.quicksum(H[i,m,s]*Q[w,i,m,s] for w in W for i in I for m in M)
        + gurobi.quicksum(H[j,m,s]*Q[w,j,m,s] for w in W for j in J for m in M)
        + gurobi.quicksum(H[m,a,s]*Q[p,m,a,s] for p in P for m in M for a in A)
        + gurobi.quicksum(H[a,b,s]*Q[p,a,b,s] for p in P for a in A for b in B)
        + gurobi.quicksum(H[b,c,s]*(Q[p,b,c,s]*alpha[p,b,s]) for p in P for b in B for c in C)
        + gurobi.quicksum(H[c,r,s]*Q[p,c,r,s] for p in P for c in C for r in R)
        + gurobi.quicksum(H[r,m,s]*Q[r,m,s,"dummy"] for r in R for m in M)

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
        gurobi.quicksum(VJO[i,s] * gurobi.quicksum(Q[w,i,m,s] / (K[w,i,s] * (1 - N[i,s])) for m in M for w in W) for i in I)
        + gurobi.quicksum(VJO[j,s] * gurobi.quicksum(Q[w,j,m,s] / K[w,j,s] for w in W for m in M) for j in J)
        + gurobi.quicksum(VJO[m,s] * (Q[p,m,a,s] / K[p,m,s]) for m in M for p in P for a in A)
        + gurobi.quicksum(VJO[a, s] * (Q[p, a, b, s] / K[p, a, s]) for a in A for p in P for b in B)
        + gurobi.quicksum(VJO[c, s] * (Q[p, c, r, s] / K[p, c, s]) for c in C for p in P for r in R)
        + gurobi.quicksum(VJO[r, s] * (Q[r, m, s,"dummy"] / K[r, s]) for r in R for m in M)
        for s in S
    )



    obj_Social = obj_Social_Fixed_Ops + obj_Social_Variable_Ops



    '''Constraints'''
    # Raw Material required for one unit
    for s in S:
        for m in M:

            SCM_Model.addConstr(
                gurobi.quicksum( gurobi.quicksum((1-prob[s]) * Q[w,i,m,s] for i in I) for w in W) +
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
                gurobi.quicksum(L[p,m,s] for p in P) + gurobi.quicksum(Q[r,m,s,"dummy"] for r in R) ==
                gurobi.quicksum(gurobi.quicksum(Q[p,m,a,s]for a in A)for p in P)
            )

        for p in P:
            for a in A:
                SCM_Model.addConstr(
                    gurobi.quicksum(Q[p,m,a,s] for m in M) == gurobi.quicksum(Q[p,a,b,s] for b in B)
                )

            for b in B:
                SCM_Model.addConstr(
                    gurobi.quicksum(Q[p,a,b,s] for a in A) >= D[p,b,s]
                )

                SCM_Model.addConstr(
                    gurobi.quicksum(Q[p,a,b,s] for a in A) >= gurobi.quicksum(Q[p,b,c,s] * alpha[p,b,s] for c in C)
                )



            for c in C:
                SCM_Model.addConstr(
                    gurobi.quicksum(Q[p,b,c,s] * alpha[p,b,s] for b in B) == gurobi.quicksum(Q[p,c,r,s] for r in R)
                )

            for r in R:
                SCM_Model.addConstr(
                    gurobi.quicksum(gurobi.quicksum(Q[p,c,r,s]for c in C)for p in P) ==
                    gurobi.quicksum(Q[r,m,s,"dummy"] for m in M)
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
                    gurobi.quicksum(Q[w,j,m,s] for m in M) <= K[w,j,s]
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
                    gurobi.quicksum(Q[p,c,r,s]for r in R) <= K[p,c,s] * E[c]
                )

        for r in R:
            SCM_Model.addConstr(
                gurobi.quicksum(Q[r,m,s,"dummy"] for m in M) <= K[r,s] * E[r]
            )

    # Visibilitz percent is the informatin shared through an informatioon sharing system
    for s in S:
        for f in F:
            SCM_Model.addConstr(
                IS[f] * EX[f, s] * (1 - prob[s]) <= V[f,s]
            )

    # implementation of the informatin sharing system constraint
    SCM_Model.addConstr(gurobi.quicksum(IS[f] for f in F) == 1 )

    SCM_Model.addConstr(gurobi.quicksum(SCU[f] for f in F) == 1 )

    # SCM_Model.Params.NumericFocus = 2
    #


    '''Optimization'''

    objectives = [-obj_Economic, -obj_Environmental, obj_Social]

    '''
    SCM_Model.setObjective(obj_Economic,gurobi.GRB.MINIMIZE)
    SCM_Model.update()
    SCM_Model.optimize()

    test=0
    for (i) in Established_Variable :
        if E[i].x>= 0.5:
            print(i, E[i].x)
    print()
    print(test)

    SCM_Model.setObjective(obj_Environmental,gurobi.GRB.MINIMIZE)
    SCM_Model.update()
    SCM_Model.optimize()

    SCM_Model.setObjective(obj_Social,gurobi.GRB.MAXIMIZE)
    SCM_Model.update()
    SCM_Model.optimize()
    '''

    return SCM_Model, objectives, Variable


