import gurobipy as gb
import Utility.Solutions as Solution

class OptimizationModel:
    decision_x = [1,2]
    decision_S = [1,2] # as much as objective functions
    eps = 1

    SingleObjectiveModel = gb.Model('Single Objective Model')

    # add decision variables
    x = SingleObjectiveModel.addVars(decision_x, vtype=gb.GRB.INTEGER, name="x")
    S = SingleObjectiveModel.addVars(decision_S)

    # add constrains
    SingleObjectiveModel.addConstr(x[1] <= 20, 'first constraint')
    SingleObjectiveModel.addConstr(x[2] <= 40, '2')
    SingleObjectiveModel.addConstr(5*x[1] + 4*x[2] <= 200, '3')

    # add objective function
    number_of_obj_functions = 2

    obj1 = gb.LinExpr()
    obj1 = 1*x[1]
    obj = {}
    obj[0] = 1*x[1]

    obj2 = gb.LinExpr()
    obj2 = 3*x[1] + 4*x[2]
    obj[1] = 3*x[1] + 4*x[2]

    def saveSolution(self):
        solution = Solution.NonDominated_Solutions(self.SingleObjectiveModel, self.get_obj_value())
        return solution

    def get_obj_value(self):
        return_values = []
        if self.SingleObjectiveModel.status == gb.GRB.Status.OPTIMAL:
            return_values = [self.x[1].x, self.x[1].x * 3 + self.x[2].x]
        return return_values

