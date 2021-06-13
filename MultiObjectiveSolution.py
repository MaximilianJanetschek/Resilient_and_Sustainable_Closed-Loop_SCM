import Utility.OriginalProblem as OP
import Utility.OptimizationModel as OM
import gurobipy as gb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

number_of_obj_functions = 2


ModelP = OM.OptimizationModel(2)
number_of_obj_functions = ModelP.number_of_obj_functions

# Start

# Create payoff table (lexmax f_k(X), k=1..p)
payoff_table = OP.create_payoff_table(ModelP, number_obj_functions = number_of_obj_functions)

# Calculate ranges r_k for k = 2..p (ranges of respective objective function)
ranges = OP.get_ranges(payoff_table)

# set number of grid points
number_of_grid_points = {}
for i in range(len(ranges)):
    number_of_grid_points[i] = ranges[i]['range']

# Divide r_k into g_k intervals (set number of gridpoints = g_k + 1)
grid_points = OP.get_grid_points(ranges,number_of_grid_points)
print('Grid points')
print(grid_points)

# Initialize counters: i_k = 0 for k = 2...p, n_p = 0
i_counter = [0 for i in range(number_of_obj_functions - 1)]
number_of_runs = 0
counter_pareto_solutions = 0
nonDominatedSolutions = []

print('enter multi objective solution procedure')


for i in range(0,ModelP.number_of_obj_functions-1):
    while i_counter[i] < number_of_grid_points[i+1]:
        # Solve problem P
        solution = OP.solveProblemP(ModelP, ranges, grid_points[1][i_counter[i]])

        # If feasible
        if ModelP.SingleObjectiveModel.status == gb.GRB.Status.OPTIMAL:
            # Safe Solution
            nonDominatedSolutions.append(solution)

            # Then
            counter_pareto_solutions += 1  # n_p = p_p + 1
            b = int(ModelP.S[2].x / (ranges[i]['range'] / number_of_grid_points[i]))  # Calculate b, b = int(S_2/step_2)
            i_counter[i] += b  # i_2 = i_2 +b
            if b >= 2:
                print('found jump with ' + str(b) + ' steps.')

        else:
            i_counter[i] = number_of_grid_points[i]  # i_2 = g_2
            print('solution is infeasible')

        number_of_runs += 1

        i_counter[i] += 1

    i_counter[i] = 0


print('Found ' + str(counter_pareto_solutions) + " non-dominated solutions in " + str(number_of_runs) + ' runs.')
print(nonDominatedSolutions)

ParetoFrontier = {'x1': [], 'x2': []}
for i in range(len(nonDominatedSolutions)):
    ParetoFrontier['x1'].append(nonDominatedSolutions[i]['x1'])
    ParetoFrontier['x2'].append(nonDominatedSolutions[i]['x2'])




