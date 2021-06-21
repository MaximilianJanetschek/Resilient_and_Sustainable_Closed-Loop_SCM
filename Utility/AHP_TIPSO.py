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

    print(Distance_Euclidean)
    preferred_solution = -1
    best_found_RC_value = -1
    for solution in Distance_Euclidean:
        if solution["Relative Closeness"] > best_found_RC_value:
            preferred_solution = solution["Counter"]
            best_found_RC_value = solution["Relative Closeness"]

    print(Distance_Euclidean[preferred_solution-1])


# cfo
pareto_set = [[-1031147094.2531995, -1471760194.3539302, 15955.804241407026], [-1031124653.2317389, -1472237753.3324683, 15892.272483877929], [-1032610152.9177637, -1461691279.1546457, 15979.927984645741], [-1034923512.0343275, -1331561596.1586206, 15474.825866441586], [-1037761447.6689869, -1317521194.0377414, 15470.010504740569], [-1042436549.5367744, -1296925467.5924695, 15472.391077906183], [-1047465498.786174, -1276329741.147197, 15455.878369970596], [-1052605574.8318354, -1255734014.7019255, 15448.809377627045], [-1057878712.6541154, -1235138288.256653, 15441.61861832049], [-1063154660.0928957, -1214542561.811381, 15387.130537981719], [-1068483420.004726, -1193946835.3661091, 15389.458853216369], [-1073846039.8079803, -1173351108.9208372, 15382.330641586694], [-1079251081.1396842, -1152755382.4755652, 15375.200654328602], [-1084693412.5498056, -1132159656.0302932, 15368.051451111123], [-1090170215.9456043, -1111563929.5850213, 15351.485785009709], [-1095679068.166676, -1090968203.1397493, 15337.539132800157], [-1101215330.176362, -1070372476.6944784, 15346.675500987312], [-1106764163.369764, -1049776750.2492063, 15339.52539373361], [-1112331732.0676916, -1029181023.8039342, 15332.35981234503], [-1117933158.9057448, -1008585297.3586624, 15315.763811405792], [-1123553505.5475118, -987989570.9133904, 15318.065422039157], [-1129189025.9613345, -967393844.4681184, 15310.912851489069], [-1134853445.2717853, -946798118.0228463, 15303.675461089437], [-1140534800.167304, -926202391.5775745, 15296.378832399243], [-1146221701.2783895, -905606665.1323024, 15207.78321845769], [-1151978307.985715, -885010938.6870307, 15210.680880865562], [-1157743829.5307007, -864415212.2417587, 15204.11262862101], [-1163530375.611176, -843819485.7964866, 15197.537123899283], [-1169335370.5969405, -823223759.3512148, 15190.959950556127], [-1175156756.8668053, -802628032.9059426, 15174.943686405955], [-1181000762.2506788, -782032306.4606707, 15168.360224637463], [-1186866874.681157, -761436580.0153987, 15161.786723646062], [-1192750668.00684, -740840853.5701267, 15155.20573161243], [-1198647614.9016898, -720245127.1248547, 15148.619438008507], [-1204569439.6920533, -699649400.6795828, 15142.023464432907], [-1210523714.1092634, -679053674.2343107, 15144.88131343437], [-1216491244.9376733, -658457947.7890387, 15138.284923767893], [-1222494527.009997, -637862221.3437667, 15131.684692122717], [-1228527228.4513493, -617266494.8984947, 15125.080713487054], [-1234596956.0558372, -596670768.4532228, 15118.473315475843], [-1240722333.8727207, -576075042.0079508, 15111.845033127984], [-1242284373.6229281, -454278247.0433262, 14642.389572994396], [-1244506809.9101875, -452500683.33604413, 15168.489683198051]]
working_directory = str(os.getcwd()).replace('/Utility', '')

os.chdir(working_directory)
pareto_set = pickle.load(open("non_dominated_solutions.p", "rb"))
print(len(pareto_set))
test_matrix = np.matrix([[1,4,6],[1/4,1,3],[1/6,1/3,1]])
weights = get_weights(test_matrix)
pareto_set = np.array(pareto_set)
print(pareto_set[1,:])
get_topsis_ranking(pareto_set, weights)

# government
test_matrix = np.matrix([[1,1/5,1/8],[5,1,1/4],[8,4,1]])
weights = get_weights(test_matrix)
print(pareto_set[1,:])
get_topsis_ranking(pareto_set, weights)

# ceo
test_matrix = np.matrix([[1,1/3,1/2],[3,1,2],[2,1/2,1]])
weights = get_weights(test_matrix)
print(pareto_set[1,:])
get_topsis_ranking(pareto_set, weights)
