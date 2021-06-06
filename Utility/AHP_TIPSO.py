import numpy as np

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
    decisionMatrixR = np.zeros((number_of_objective_functions, number_of_pareto_solution))

    print(decisionMatrixR)

    for i in range(number_of_objective_functions):
        sum_obj_values = np.sum(np.multiply(pareto_set[i, :])) ^ 0.5

        for j in range(number_of_pareto_solution):
            decisionMatrixR[i, j] = pareto_set[i, j] / sum_obj_values

    # step 2 - weighted normalized matrix V
    matrixV = np.multiply(weights, pareto_set)

    A = {"positive-ideal":[], "negative_ideal":[]}
    # step 3 - positive ideal solution and negative solution
    for i in range(number_of_objective_functions):

        # positive solution
        A["positive-ideal"].append(np.maximum(matrixV[i,:]))
        # negative solution
        A["negative_ideal"].append(np.minimum(matrixV[i, :]))

    Distance_Euclidean = []
    # step 4 - separation distance to positive and negative ideal solution
    for j in range(number_of_pareto_solution):

        # calculate distance to positive ideal solution
        D_pos_inner = matrixV[:,j] - A['positive_ideal'][j]
        D_positive = np.dot(D_pos_inner, D_pos_inner)^0.5

        # calculate distance to negative ideal solution
        D_neg_inner = matrixV[:,j] - A['positive_ideal'][j]
        D_negative = np.dot(D_neg_inner, D_neg_inner)^0.5

        # calculate relative closeness
        relative_closeness = D_negative / (D_positive + D_negative)

        #safe distances to dict
        Distance_Euclidean.append({"D_positive":D_positive, "D_negative":D_negative, "Relative Closeness": relative_closeness})




test_matrix = np.matrix([[1,1/3,1/9,1/5],[3,1,1,1],[9,1,1,3],[5,1,1/3,1]])

get_weights(test_matrix)
check_consistency(test_matrix, get_weights(test_matrix))