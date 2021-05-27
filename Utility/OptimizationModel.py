import gurobipy as gb


class OptimizationModel:
    decision_x = [1,2]
    decision_S = [1,2] # as much as objective functions
    eps = 10^-3

    SingleObjectiveModel = gb.Model('Single Objective Model')

    # add decision variables
    x = SingleObjectiveModel.addVars(decision_x)
    S = SingleObjectiveModel.addVars(decision_S)

    # add constrains
    SingleObjectiveModel.addConstr(x[1] <= 20, '1')
    SingleObjectiveModel.addConstr(x[2] <= 40, '2')
    SingleObjectiveModel.addConstr(5*x[1] + 4*x[2] <= 200, '3')

    # add objective function
    obj1 = gb.LinExpr()
    obj1 = 1*x[1]

    obj2 = gb.LinExpr()
    obj2 = 3*x[1] + 4*x[2]

