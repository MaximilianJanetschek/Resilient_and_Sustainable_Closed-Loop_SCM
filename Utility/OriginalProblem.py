import gurobipy as gb
import Utility.OptimizationModel as ModelP
import numpy as np


def create_payoff_table (P,number_obj_functions: int)-> list():
    payoff_table = [[0 for i in range(number_obj_functions) ] for j in range(number_obj_functions)]
    P.SingleObjectiveModel.setParam('LogToConsole',0)
    # Solve for first objective
    P.SingleObjectiveModel.setObjective(P.obj1, gb.GRB.MAXIMIZE)
    P.SingleObjectiveModel.update()
    P.SingleObjectiveModel.optimize()

    payoff_table[0][0] = P.SingleObjectiveModel.objVal
    limit = P.SingleObjectiveModel.objVal
    P.SingleObjectiveModel.addConstr(P.x[1] == limit, 'additional constraint')
    P.SingleObjectiveModel.setObjective(P.obj2, gb.GRB.MAXIMIZE)
    P.SingleObjectiveModel.update()
    P.SingleObjectiveModel.optimize()
    payoff_table[0][1] = P.SingleObjectiveModel.objVal

    P.SingleObjectiveModel.remove(P.SingleObjectiveModel.getConstrByName('additional constraint'))
    print(P.SingleObjectiveModel.x[1])
    print(P.SingleObjectiveModel.x[2])




    # Solve for second objective
    P.SingleObjectiveModel.setObjective(P.obj2, gb.GRB.MAXIMIZE)
    P.SingleObjectiveModel.update()
    P.SingleObjectiveModel.optimize()
    payoff_table[1][1] = P.SingleObjectiveModel.objVal
    print(P.SingleObjectiveModel.x[1])
    print(P.SingleObjectiveModel.x[2])

    limit = P.SingleObjectiveModel.objVal
    P.SingleObjectiveModel.addConstr(3*P.x[1] + 4*P.x[2] == limit, 'additional constraint')
    P.SingleObjectiveModel.setObjective(P.obj1, gb.GRB.MAXIMIZE)
    P.SingleObjectiveModel.update()
    P.SingleObjectiveModel.optimize()
    payoff_table[1][0] = P.SingleObjectiveModel.objVal

    P.SingleObjectiveModel.remove(P.SingleObjectiveModel.getConstrByName('additional constraint'))



    return payoff_table

def get_ranges(payoff_table) -> list():
    ranges = []

    for i in range(len(payoff_table)):
        solution_vector = np.array(payoff_table)

        # get min
        lb_range = min(solution_vector[:,i])

        # get maxy
        ub_range = max(solution_vector[:,i])

        ranges.append({'ub':ub_range, 'lb':lb_range, 'range': ub_range - lb_range})

    return ranges

def get_grid_points(ranges, number_of_grid_points) -> list():
    # initialize array for all ojb functions
    grid_points = [[] for i in range(len(ranges))]

    for i in range(len(ranges)):
        obj_range = ranges[i]
        intervall = obj_range['range'] / (number_of_grid_points[i]-1)
        add_point = obj_range['lb']
        for j in range(int(number_of_grid_points[i])):
            grid_points[i].append(add_point)
            add_point += intervall

    return grid_points


def solveProblemP (P:ModelP.OptimizationModel, ranges, grid_points) -> list():

    obj = gb.LinExpr()
    obj += P.obj1
    obj_help = gb.LinExpr()
    for i in range(1,P.number_of_obj_functions):
        superscript = -(i-1)
        obj_help += (10**superscript)*(P.S[i+1]/ranges[i]['range'])
    obj += (0*obj_help)
    P.S = P.SingleObjectiveModel.addVars(P.decision_S, vtype=gb.GRB.CONTINUOUS, name="S")

    P.SingleObjectiveModel.addConstr((3*P.x[1] + 4*P.x[2] - P.S[2] == grid_points) , 'additional constraint')

    P.SingleObjectiveModel.setObjective(obj, gb.GRB.MAXIMIZE)
    P.SingleObjectiveModel.setParam('LogToConsole',0)
    P.SingleObjectiveModel.update()
    P.SingleObjectiveModel.optimize()

    return P.get_obj_value()











