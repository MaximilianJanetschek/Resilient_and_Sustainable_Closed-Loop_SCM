import gurobipy as gb


class OptimizationModel:
    decision_x = [1,2]
    decision_S = [2]
    number_of_obj_functions = 2
    eps = (10 ** -3)

    SingleObjectiveModel = gb.Model('Payoff-Table')

    # add decision variables
    x = SingleObjectiveModel.addVars(decision_x, vtype=gb.GRB.INTEGER, name="x")


    # add objective function
    obj1 = gb.LinExpr()
    obj2 = gb.LinExpr()





    def __init__(self, eps):

        self.decision_x = [1, 2]
        self.decision_S = [1, 2]  # as much as objective functions
        self.eps = eps

        number_of_obj_functions = 2

        self.SingleObjectiveModel = gb.Model('Single Objective Model')
        self.SingleObjectiveModel.setParam('LogToConsole', 0)
        # add decision variables
        self.x = self.SingleObjectiveModel.addVars(self.decision_x, vtype=gb.GRB.INTEGER, name="x")
        self.S = self.SingleObjectiveModel.addVars(self.decision_S, vtype=gb.GRB.CONTINUOUS,name='S')

        # add constrains
        self.SingleObjectiveModel.addConstr(self.x[1] <= 20, name='first')
        self.SingleObjectiveModel.addConstr(self.x[2] <= 40, name='second')
        self.SingleObjectiveModel.addConstr(5 * self.x[1] + 4 * self.x[2] <= 200, name='third')

        # add objective function
        number_of_obj_functions = 2

        self.obj1 = gb.LinExpr()
        self.obj1 += 1 * self.x[1]

        self.obj2 = gb.LinExpr()
        self.obj2 += 3 * self.x[1] + 4 * self.x[2]

        print('start procedure')
        self.SingleObjectiveModel.setObjective(self.obj1, gb.GRB.MAXIMIZE)
        self.SingleObjectiveModel.update()
        self.SingleObjectiveModel.optimize()



    def get_obj_value(self):
        return_values = []
        if self.SingleObjectiveModel.status == gb.GRB.Status.OPTIMAL:
            return_values = {'obj1':self.x[1].x,'obj2': self.x[1].x * 3 + self.x[2].x, 'x1': self.x[1].x, 'x2':self.x[2].x}
        return return_values

