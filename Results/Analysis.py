import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.interpolate import interpn
from Data.Data_Retrieval import *
import pickle
import os
import statistics

def density_scatter( x , y, ax = None, sort = True, bins = 20, **kwargs )   :
    """
    Scatter plot colored by 2d histogram
    """
    if ax is None :
        fig , ax = plt.subplots()
    data , x_e, y_e = np.histogram2d( x, y, bins = bins, density = True )
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False)

    #To be sure to plot all data
    z[np.where(np.isnan(z))] = 0.0

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

    ax.scatter( x, y, c=z, **kwargs )

    norm = Normalize(vmin = np.min(z), vmax = np.max(z))
    cbar = fig.colorbar(cm.ScalarMappable(norm = norm), ax=ax)
    cbar.ax.set_ylabel('Density')
    fig.show()

    return ax



x = np.random.normal(size=100000)
y = x * 3 + np.random.normal(size=100000)

working_directory = str(os.getcwd()).replace('/Results', '')

os.chdir(working_directory)
solution = pickle.load(open("non_dominated_solutions.p", "rb"))
locations = pickle.load(open("established_locations_list.p", "rb"))

plot_solution = {'economic':[], 'environmental':[], 'social':[]}
for i in solution:
    plot_solution['economic'].append(-i[0])
    plot_solution['environmental'].append(-i[1])
    plot_solution['social'].append(i[2])

fig , ax = plt.subplots()
ax.scatter( plot_solution['economic'], plot_solution['environmental'], c=plot_solution['social'])
norm = Normalize(vmin = np.min(plot_solution['social']), vmax = np.max(plot_solution['social']))
cbar = fig.colorbar(cm.ScalarMappable(norm = norm), ax=ax)
cbar.ax.set_ylabel('Social')
ax.set_xlabel('Economic Downside')
ax.set_ylabel('Environmental Impact')

fig.savefig("Results/Plots/ParetoSpace.png", dpi=200)

#density_scatter( x, y, bins = [30,30] )

def print_established_locations(locations: list(), links, solution_number):

    # get German map and plot all locations
    indices = initialize_sets()
    coordinates_of_all_sites = get_coordinates_of_all_sites(indices)
    [I, J, M, A, B, C, R, P, W, S, F] = indices
    MapOfNetwork = folium.Map(location=(52.520008, 13.404954), zoom_start=5.3)
    color_dict = {'suppliers': 'beige','manufacturer': 'orange','distributor': 'green', 'collectors': 'lightblue', 'recyclers': 'blue'}
    # {'suppliers': '#DAD7CB', 'manufacturer': '#E37222', 'distributor': '#A2AD00', 'collectors': '#98C6EA','recyclers': '#64A0C8'}

    for location in locations:
        node = coordinates_of_all_sites[location]
        if location.split('-')[0]=='C':
            [node["lat"], node["lon"]] = [node["lat"]+0.1, node["lon"]+0.1]
        folium.Marker(location=[node["lat"], node["lon"]], icon=folium.Icon(color=color_dict[node['category']])).add_to(MapOfNetwork)



    arcs_to_be_plotted = []
    for arc in links:
        (p,a,b,s) = arc
        if b != '':
            start_node = coordinates_of_all_sites[a]
            end_node = coordinates_of_all_sites[b]
            folium.PolyLine([(start_node['lat'], start_node['lon']), (end_node['lat'], end_node['lon'])], color="green", weight=2.5, opacity=1).add_to(MapOfNetwork)



    MapOfNetwork.save('Results/Plots/DistributorNetwork' + str(solution_number)+'.html')

    # supplier #DAD7CB

    # manufacturer #E37222

    # distributors #A2AD00

    # collectors #98C6EA

    # recyclers #64A0C8

def create_folium_with_distributors(nodes_to_be_plotted:dict(), path: str):
    MapOfNetwork = folium.Map(location=(52.520008, 13.404954), zoom_start=5.3)

    for node in nodes_to_be_plotted.values():
        folium.Marker(location=[node["lat"], node["lon"]],icon=folium.Icon(color='red')).add_to(MapOfNetwork)
    if os.path.exists(path):
        MapOfNetwork.save('Results/Plots/DistributorNetwork.html')
    else:
        path = path.split("/")
        counter = -2
        check_path = path[counter]
        while not os.path.exists(check_path):
            counter -= 1
            check_path = path[counter] + "/" + check_path
            if counter == -len(path):
                break
        print(check_path)
        os.makedirs(check_path)
        MapOfNetwork.save('Results/Plots/DistributorNetwork.html')


links = pickle.load(open("supply_links_list.p", "rb"))
selected_solution = 195
print_established_locations(locations[selected_solution], links[selected_solution], selected_solution)


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

plt.bar(plot_x,plot_y)
plt.xlabel('Distributors')
plt.ylabel('Count in pareto set')
plt.savefig("Results/Plots/Distributors.png", dpi=200)
plt.show()



# summary statistics
sum_stats = {'manufacturer': {}, 'distributor': {}, 'collectors': {},
              'recyclers': {}}



solution_count = 1
for solution in locations:
    for cat in sum_stats.keys():
        sum_stats[cat][solution_count] = 0
    for i in solution:
        node = coordinates_of_all_sites[i]
        if node['category'] == 'suppliers':
            print(node)
        sum_stats[node['category']][solution_count] += 1
    solution_count += 1


sum_stats['primary supplier'] = {}
sum_stats['backup supplier'] = {}

suppliers = pickle.load(open('suppliers_oppend.p', 'rb'))
print(suppliers)
solution_count = 1
for i in suppliers:
    sum_stats['primary supplier'][solution_count] = 0
    sum_stats['backup supplier'][solution_count] = 0
    for j in i:
        print(j)
        if j.split('_')[0] =='PS':
                sum_stats['primary supplier'][solution_count] += 1
        else:
            sum_stats['backup supplier'][solution_count] += 1
    solution_count += 1

print(sum_stats)

stats_output = {}
for i in sum_stats.keys():
    stats_output[i] = {}



for category in sum_stats.keys():
    # transform into list
    cat_list=[]
    for i in sum_stats[category].keys():
        cat_list.append(sum_stats[category][i])
    print(cat_list)
    stats_output[category]['mean'] = round(statistics.mean(cat_list),2)
    stats_output[category]['std'] = round(statistics.stdev(cat_list),2)
    stats_output[category]['min'] = min(cat_list)
    stats_output[category]['max'] = max(cat_list)
    stats_output[category]['median'] = statistics.median(cat_list)
print(stats_output)

