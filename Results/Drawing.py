import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.interpolate import interpn
from Data.Data_Retrieval import *
import pickle
import os
import statistics

def draw_runtime():
    working_directory = str(os.getcwd()).replace('/Results', '')

    os.chdir(working_directory)


    time_and_solution = pickle.load(open('time_and_solution_count.p', 'rb'))
    print(time_and_solution)
    solution_time_list = []
    solution_count = []
    for i in time_and_solution:
        solution_time_list.append(i[0])
        solution_count.append(i[1])


    plt.plot(solution_time_list, solution_count)
    plt.xlabel('runtime of algorithm in seconds')
    plt.ylabel('number of generated solutions')
    plt.savefig("Results/Plots/Runtime_Solution_Count.png", dpi=200)
    plt.show()

def draw_distributors():
    working_directory = str(os.getcwd()).replace('/Results', '')

    os.chdir(working_directory)
    # opened distributor locations
    indices = initialize_sets()
    [I, J, M, A, B, C, R, P, W, S, F] = indices
    coordinates_of_all_sites = get_coordinates_of_all_sites(indices)
    count_distributor = {}
    locations = pickle.load(open('established_locations_list.p', 'rb'))

    for d in A:
        count_distributor[d] = 0

    for solution in locations:
        for i in solution:
            node = coordinates_of_all_sites[i]
            if node['category'] == 'distributor':
                count_distributor[i] += 1
    plot_x = []
    plot_y = []
    counter = 1
    for i in count_distributor.values():
        plot_x.append(counter)
        plot_y.append(i)
        counter += 1

    plt.bar(plot_x, plot_y)
    plt.xlabel('Distributors')
    plt.ylabel('Count in pareto set')
    plt.savefig("Results/Plots/Distributors.png", dpi=200)
    plt.show()

def draw_pareto_space():
    working_directory = str(os.getcwd()).replace('/Results', '')

    os.chdir(working_directory)
    solution = pickle.load(open("non_dominated_solutions.p", "rb"))
    locations = pickle.load(open("established_locations_list.p", "rb"))

    plot_solution = {'economic': [], 'environmental': [], 'social': []}
    for i in solution:
        plot_solution['economic'].append(-i[0])
        plot_solution['environmental'].append(-i[1])
        plot_solution['social'].append(i[2])

    fig, ax = plt.subplots()
    ax.scatter(plot_solution['economic'], plot_solution['environmental'], c=plot_solution['social'])
    norm = Normalize(vmin=np.min(plot_solution['social']), vmax=np.max(plot_solution['social']))
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm), ax=ax)
    cbar.ax.set_ylabel('Social')
    ax.set_xlabel('Economic Downside')
    ax.set_ylabel('Environmental Impact')
    fig.show()

    fig.savefig("Results/Plots/ParetoSpace.png", dpi=200)

draw_pareto_space()
draw_distributors()