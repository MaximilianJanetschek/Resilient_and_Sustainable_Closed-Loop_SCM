import gurobipy as gb

class NonDominated_Solutions:
    x = {}
    objVal = []

    def __init__(self, SolvedModel, objValues):
        for i in range(len(SolvedModel.x)):
            self.x[i] = SolvedModel.x[i]
        self.objVal = objValues




