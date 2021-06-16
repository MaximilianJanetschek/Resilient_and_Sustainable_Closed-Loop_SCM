import Utility.OriginalProblem as OP
import Utility.OptimizationModel as OM
import Utility.Resilient_and_Sustainable_SCM as Math_Model
from Utility.AHP_TIPSO import *
from Data.Data_Retrieval import *
import pickle
import gurobipy as gurobi
import pandas as pd
import os
import numpy as np
import time


# Data import
''' Index '''  # do not use 1,..,n rahter some unique such that parameters are hashable
indices = initialize_sets()

''' Parameters '''
parameters = get_parameters(indices)

''' Initialize Model and Objectives'''
ModelSCM, objectives = Math_Model.get_multi_objective_model(indices,parameters)

number_of_obj_functions = len(objectives)


# Start

# Create payoff table (lexmax f_k(X), k=1..p)
payoff_table = OP.create_payoff_table(ModelSCM,objectives)

# Calculate ranges r_k for k = 2..p (ranges of respective objective function)
ranges = OP.get_ranges(payoff_table)
print(ranges)

# set number of grid points
number_of_grid_points = {}
for i in range(len(ranges)):
    if ranges[i]['range'] > 100:
        number_of_grid_points[i] = ranges[i]['range'] / (0.01*ranges[i]['range'] )
    else:
        number_of_grid_points[i] = ranges[i]['range']

# Divide r_k into g_k intervals (set number of gridpoints = g_k + 1)
grid_points = OP.get_grid_points(ranges,number_of_grid_points)

print('Grid points')
for i in grid_points:
    print(len(i))

# Initialize counters: i_k = 0 for k = 2...p, n_p = 0
i_counter = [0 for i in range(number_of_obj_functions)]
number_of_runs = 0
counter_pareto_solutions = 0
nonDominatedSolutions = []

print('enter multi objective solution procedure')
seconds = time.time()
time_and_solution_count = []


while i_counter[2] < number_of_grid_points[2]:
    while i_counter[1] < number_of_grid_points[1]:
        # Solve problem P
        solution, S, feasible_status = OP.solveProblemP(ModelSCM, objectives, ranges, grid_points[1][i_counter[1]], grid_points[2 ][i_counter[2]], len(objectives))

        # If feasible
        if feasible_status:
            # Safe Solution
            nonDominatedSolutions.append(solution)

            # Then
            counter_pareto_solutions += 1  # n_p = p_p + 1
            b = int(S[2] / (ranges[1]['range'] / number_of_grid_points[1]))  # Calculate b, b = int(S_2/step_2)
            i_counter[1] += b  # i_2 = i_2 +b
            if b >= 2:
                print('found jump with ' + str(b) + ' steps.')

        else:
            i_counter[1] = number_of_grid_points[1]  # i_2 = g_2
            print('solution is infeasible')

        number_of_runs += 1

        i_counter[1] += 1

    i_counter[1] = 0
    i_counter[2] += 1
    print("finishied " + str(i_counter[2]))
    time_and_solution_count.append(((time.time()-seconds), counter_pareto_solutions))

    print("Seconds since multi objective starting procedure =", (seconds-time.time()))


print('Found ' + str(counter_pareto_solutions) + " non-dominated solutions in " + str(number_of_runs) + ' runs.')
print(nonDominatedSolutions)

pickle.dump(nonDominatedSolutions, open("non_dominated_solutions.p ", "wb"))
pickle.dump(nonDominatedSolutions, open("time_and_solution_count.p ", "wb"))


test_matrix = np.matrix([[1,1/3,1/9],[3,1,1],[9,1,1]])
weights = get_weights(test_matrix)

get_topsis_ranking(np.array(nonDominatedSolutions), weights)






