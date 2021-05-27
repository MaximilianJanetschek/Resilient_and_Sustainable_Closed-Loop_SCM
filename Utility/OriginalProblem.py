import gurobipy as gb
import Utility.OptimizationModel as ModelP

def create_payoff_table (number_obj_functions: int)-> list():
    payoff_table = [[0 for i in range(number_obj_functions) ] for j in range(number_obj_functions)]
    decision_x = [1,2]

    SingleObjectiveModel = gb.Model('Single Objective Model')

    # add decision variables
    x = SingleObjectiveModel.addVars(decision_x, vtype=gb.GRB.INTEGER, name="x")

    # add constrains
    SingleObjectiveModel.addConstr(x[1] <= 20)
    SingleObjectiveModel.addConstr(x[2] <= 40)
    SingleObjectiveModel.addConstr(5*x[1] + 4*x[2] <= 200)

    # add objective function
    obj1 = gb.LinExpr()
    obj1 += 1*x[1]




    # Solve for first objective
    SingleObjectiveModel.setObjective(obj1, gb.GRB.MAXIMIZE)
    SingleObjectiveModel.update()
    SingleObjectiveModel.optimize()
    payoff_table[0][0] = SingleObjectiveModel.objVal
    # would have to add constraint and then reoptimize
    limit = SingleObjectiveModel.objVal
    SingleObjectiveModel.addConstr(x[1] == limit, 'additional constraint')
    obj2 = gb.LinExpr()
    obj2 += 3*x[1] + 4*x[2]
    SingleObjectiveModel.setObjective(obj2, gb.GRB.MAXIMIZE)
    SingleObjectiveModel.update()
    SingleObjectiveModel.optimize()
    payoff_table[0][1] = SingleObjectiveModel.objVal

    SingleObjectiveModel.remove(SingleObjectiveModel.getConstrByName('additional constraint'))




    # Solve for second objective
    SingleObjectiveModel.setObjective(obj2, gb.GRB.MAXIMIZE)
    SingleObjectiveModel.update()
    SingleObjectiveModel.optimize()
    payoff_table[1][1] = SingleObjectiveModel.objVal
    limit = SingleObjectiveModel.objVal
    SingleObjectiveModel.addConstr(obj2 == limit, 'additional constraint')
    SingleObjectiveModel.setObjective(obj1, gb.GRB.MAXIMIZE)
    SingleObjectiveModel.update()
    SingleObjectiveModel.optimize()

    SingleObjectiveModel.remove(SingleObjectiveModel.getConstrByName('additional constraint'))

    payoff_table[1][0] = SingleObjectiveModel.objVal


    print(payoff_table)

    return payoff_table

def get_ranges(payoff_table) -> list():
    ranges = []

    for i in range(len(payoff_table)):
        print(i)
        solution_vecotr = payoff_table[i]

        # get min
        lb_range = min(solution_vecotr)

        # get maxy
        ub_range = max(solution_vecotr)

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

    P.SingleObjectiveModel.getConstrByName('first constraint')
    obj = gb.LinExpr()
    obj += P.obj1
    obj_help = gb.LinExpr()
    for i in range(P.number_of_obj_functions):
        superscript = -(i-1)
        obj_help += P.S[i+1]/ranges[i]['range']
    obj += P.eps * obj_help

    P.SingleObjectiveModel.addConstr(3*P.x[1] + 4*P.x[2] - P.S[2] == grid_points, 'additional constraint')

    P.SingleObjectiveModel.setObjective(obj, gb.GRB.MAXIMIZE)
    P.SingleObjectiveModel.setParam('LogToConsole',0)
    P.SingleObjectiveModel.update()
    P.SingleObjectiveModel.optimize()
    print(grid_points)
    #print(P.SingleObjectiveModel.objVal)
    print(P.S[2])
    print(P.x[1])
    print(P.x[2])

    P.SingleObjectiveModel.remove(P.SingleObjectiveModel.getConstrByName('additional constraint'))











