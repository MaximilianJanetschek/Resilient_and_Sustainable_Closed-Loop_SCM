import Utility.OriginalProblem as OP
import Utility.OptimizationModel as OM
import gurobipy as gb

number_of_obj_functions = 2
number_of_grid_points = 30

ModelP = OM.OptimizationModel()
# Start

# Create payoff table (lexmax f_k(X), k=1..p)
payoff_table = OP.create_payoff_table(number_obj_functions = 2)

# Calculate ranges r_k for k = 2..p (ranges of respective objective function)
ranges = OP.get_ranges(payoff_table)

# Divide r_k into g_k intervals (set number of gridpoints = g_k + 1)
grid_points = OP.get_grid_points(ranges,number_of_grid_points)
print('Grid points')
print(grid_points)

# Initialize counters: i_k = 0 for k = 2...p, n_p = 0
i_counter = [0 for i in range(number_of_obj_functions + 1)]
number_of_runs = 0
print(i_counter)
counter_pareto_solutions = 0

print('enter multi objective solution procedure')

# While i_p < g_p / or entered
while i_counter[2] < number_of_grid_points:

    # i_p = i_p + 1
    # i_counter[2] += 1

    # While i_p-1 < g_p-1 / or entered
    while i_counter[2] < number_of_grid_points:

        # i_p-1 = i_p-1 + 1
        # i_counter[2] += 1

        # While i_2 < g_2 / or entered
        while i_counter[2] < number_of_grid_points:

            # i_2 = i_2 + 1
            i_counter[2] += 1

            # Solve problem P
            OP.solveProblemP(ModelP, ranges, grid_points[1][i_counter[2]-1])

            # If feasible
            if ModelP.SingleObjectiveModel.status == gb.GRB.Status.OPTIMAL:
                # Then
                counter_pareto_solutions += 1                     # n_p = p_p + 1
                b = int(ModelP.S[2].x/(ranges[1]['range']/number_of_grid_points)) # Calculate b, b = int(S_2/step_2)
                i_counter[2] = i_counter[2] + b # i_2 = i_2 +b
                if b >= 2:
                    print('found jump with ' + str(b) + ' steps.')

            else:
                i_counter[2] = number_of_grid_points    # i_2 = g_2
                print('solution is infeasible')

            number_of_runs += 1


print('Found ' + str(counter_pareto_solutions) + " non-dominated solutions in " + str(number_of_runs) + ' runs.')


