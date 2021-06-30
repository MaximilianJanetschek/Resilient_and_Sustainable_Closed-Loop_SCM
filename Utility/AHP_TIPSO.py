import numpy as np
import pickle
import os

def get_weights(ranking: np.matrix) -> np.array:
    repeat_step = True
    weights = np.array([])
    ranking_quadratic = ranking
    row_sum = np.array([])
    previous_eigenvector = np.zeros((len(ranking)))
    while repeat_step:
        ranking_quadratic = np.dot(ranking_quadratic, ranking_quadratic)
        row_sum = ranking_quadratic.sum(axis=1)
        norm_eigenvector = row_sum / np.sum(row_sum)
        delta_norm = norm_eigenvector-previous_eigenvector
        if np.sum(delta_norm) <= 0.01:
            repeat_step = False
            weights = norm_eigenvector
        else:
            previous_eigenvector = norm_eigenvector
    check_consistency(ranking, weights)
    return weights

def check_consistency(ranking, weight_matrix) -> float():
    consistency_array = np.sum(np.dot(ranking, weight_matrix), axis=1)
    alpha = np.divide(consistency_array, weight_matrix)
    alpha_max = np.mean(alpha)


    n = len(weight_matrix)
    # sanity check
    if alpha_max < n:
        print("Value for alpha_max is to high, please check AHP procedure")
        raise ValueError

    consistency_index = - (alpha_max - n) / (1 - n)

    RI = [0,0,0.58,0.9,1.12,1.24,1.32,1.41, 1.45, 1.49]

    consistency_ratio = round(consistency_index / RI[n-1],3)

    if consistency_ratio > 0.1:
        print("Ranking Matrix is not consistent! - " + str(consistency_ratio))
    else:
        print("Ranking Matrix is consistent. - "+ str(consistency_ratio))

    return consistency_ratio




def get_topsis_ranking(pareto_set: list(), weights: np.array) -> dict():
    '''
    pareto set of type [[1_obj, 2_obj, 3_obj]]
    '''

    number_of_pareto_solution = len(pareto_set)
    number_of_objective_functions = 3

    # step 1 - normalized decision matrix R
    decisionMatrixR = np.zeros((number_of_pareto_solution,number_of_objective_functions))

    for j in range(number_of_pareto_solution):
        sum_obj_values = np.sum(np.multiply(pareto_set[j, :],pareto_set[j, :]))**0.5

        for i in range(number_of_objective_functions):
            decisionMatrixR[j, i] = pareto_set[j,i] / sum_obj_values

    # step 2 - weighted normalized matrix V
    print(weights)
    matrix_V = np.zeros((number_of_pareto_solution,number_of_objective_functions))
    for j in range(number_of_pareto_solution):
        for i in range(number_of_objective_functions):
            matrix_V[j,i] = decisionMatrixR[j, i] * weights[i]

    A = {"positive_ideal":[], "negative_ideal":[]}
    # step 3 - positive ideal solution and negative solution
    print("test")
    for i in range(number_of_objective_functions):
        # positive solution
        A["positive_ideal"].append(np.amax(matrix_V[:,i]))
        # negative solution
        A["negative_ideal"].append(np.amin(matrix_V[:,i]))

    Distance_Euclidean = []
    # step 4 - separation distance to positive and negative ideal solution
    for j in range(number_of_pareto_solution):

        # calculate distance to positive ideal solution
        D_pos_inner = 0
        D_neg_inner = 0
        for i in range(number_of_objective_functions):
            D_pos_inner += (matrix_V[j,i] - A['positive_ideal'][i])**2
            # calculate distance to negative ideal solution
            D_neg_inner += (matrix_V[j,i] - A['negative_ideal'][i])**2

        D_positive = D_pos_inner**0.5


        D_negative = D_neg_inner**0.5

        # calculate relative closeness
        relative_closeness = D_negative / (D_positive + D_negative)

        #safe distances to dict
        Distance_Euclidean.append({"D_positive":D_positive, "D_negative":D_negative, "Relative Closeness": relative_closeness, "Counter":j+1})


    preferred_solution = -1
    best_found_RC_value = -1
    for solution in Distance_Euclidean:
        if solution["Relative Closeness"] > best_found_RC_value:
            preferred_solution = solution["Counter"]
            best_found_RC_value = solution["Relative Closeness"]

    print(Distance_Euclidean[preferred_solution-1])


# cfo
working_directory = str(os.getcwd()).replace('/Utility', '')

os.chdir(working_directory)
pareto_set = pickle.load(open("non_dominated_solutions.p", "rb"))
print(len(pareto_set))

# CFO
print('shareholder')
test_matrix = np.matrix([[1,4,6],[1/4,1,3],[1/6,1/3,1]])
weights = get_weights(test_matrix)
pareto_set = np.array(pareto_set)

get_topsis_ranking(pareto_set, weights)

# government
print('government')
test_matrix = np.matrix([[1,1/5,1/8],[5,1,1/4],[8,4,1]])
weights = get_weights(test_matrix)
get_topsis_ranking(pareto_set, weights)
5
