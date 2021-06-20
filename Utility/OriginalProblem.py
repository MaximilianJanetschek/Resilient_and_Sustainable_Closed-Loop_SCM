import gurobipy as gb
import Utility.OptimizationModel as ModelP
import numpy as np


def create_payoff_table (P,objectives)-> list():
    number_obj_functions = len(objectives)
    payoff_table = [[0 for i in range(number_obj_functions) ] for j in range(number_obj_functions)]
    #P.setParam('LogToConsole',0)

    '''Fixing First Objective'''
    # Solve for first objective Economic
    P.setObjective(objectives[0], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[0][0] = P.objVal

    # Solve for the second objective
    P.addConstr(objectives[0] == payoff_table[0][0], 'additional constraint objective 1')
    P.setObjective(objectives[1], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[0][1] = P.objVal

    # Solve for the third objective
    P.setObjective(objectives[2], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[0][2] = P.objVal

    P.remove(P.getConstrByName('additional constraint objective 1'))

    '''Fixing Second Objective'''
    # Solve for first objective Economic
    P.setObjective(objectives[1], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[1][1] = P.objVal

    # Solve for the second objective
    P.addConstr(objectives[1] == payoff_table[1][1], 'additional constraint objective 2')
    P.setObjective(objectives[0], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[1][0] = P.objVal

    # Solve for the third objective
    P.setObjective(objectives[2], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[1][2] = P.objVal

    P.remove(P.getConstrByName('additional constraint objective 2'))

    '''Fixing Third Objective'''
    # Solve for first objective Economic
    P.setObjective(objectives[2], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[2][2] = P.objVal

    # Solve for the second objective
    P.addConstr(objectives[2] == payoff_table[2][2], 'additional constraint objective 3')
    P.setObjective(objectives[0], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[2][0] = P.objVal

    # Solve for the third objective
    P.setObjective(objectives[1], gb.GRB.MAXIMIZE)
    P.update()
    P.optimize()
    payoff_table[2][1] = P.objVal

    P.remove(P.getConstrByName('additional constraint objective 3'))


    print(payoff_table)



    return payoff_table

def get_ranges(payoff_table) -> list():
    ranges = []

    for i in range(len(payoff_table)):
        solution_vector = np.array(payoff_table)

        # get min
        lb_range = min(solution_vector[:,i])


        # get max
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


def solveProblemP (P, objectives, ranges, grid_point_obj_1, grid_point_obj_2, number_of_obj_functions, Variable) -> list():
    obj = gb.LinExpr(objectives[0])
    obj_help = gb.LinExpr()
    S = P.addVars([2,3],vtype=gb.GRB.CONTINUOUS, name="S")
    for i in range(1,number_of_obj_functions):
        superscript = -(i-1)
        obj_help += (10**superscript)*(S[i+1]/ranges[i]['range'])
    obj += obj_help
    constraint_1 = gb.LinExpr(objectives[1])
    constraint_1 -= S[2]
    P.addConstr(constraint_1 == grid_point_obj_1, 'additional constraint to fix constraint 1')

    constraint_2 = gb.LinExpr(objectives[2])
    constraint_2 -= S[3]
    P.addConstr(constraint_2 == grid_point_obj_2, 'additional constraint to fix constraint 2')

    P.setObjective(obj, gb.GRB.MAXIMIZE)
    P.setParam('LogToConsole',0)
    P.update()
    P.optimize()

    solved_model = (P.status == gb.GRB.Status.OPTIMAL)
    S_values = []
    solutions = []
    established_locations = []
    supply_links = []
    if solved_model:
        S_values = [0,0,S[2].x, S[3].x]
        solutions = [objectives[i].getValue() for i in range(len(objectives))]
        # get opened locations

        for e in Variable['E indices']:
            if Variable['E'][e].x >= 0.8:
                established_locations.append(e)

        for q in Variable['Q indices']:
            if Variable['Q'][q].x >= 0.5:
                supply_links.append(q)







    P.remove(P.getConstrByName('additional constraint to fix constraint 1'))
    P.remove(P.getConstrByName('additional constraint to fix constraint 2'))
    P.update()


    return solutions, S_values, solved_model, established_locations, supply_links











