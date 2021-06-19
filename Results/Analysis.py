import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.interpolate import interpn
from Data.Data_Retrieval import *
import pickle
import os

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
print(locations)
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

fig.show()

#density_scatter( x, y, bins = [30,30] )

def print_established_locations(locations: list()):

    # get German map and plot all locations
    indices = initialize_sets()
    coordinates_of_all_sites = get_coordinates_of_all_sites(indices)
    MapOfNetwork = folium.Map(location=(52.520008, 13.404954), zoom_start=5.3)
    color_dict = {'suppliers': 'beige','manufacturer': 'orange','distributor': 'green', 'collectors': 'lightblue', 'recyclers': 'blue'}
    # {'suppliers': '#DAD7CB', 'manufacturer': '#E37222', 'distributor': '#A2AD00', 'collectors': '#98C6EA','recyclers': '#64A0C8'}

    for location in locations:
        node = coordinates_of_all_sites[location]
        folium.Marker(location=[node["lat"], node["lon"]], icon=folium.Icon(color=color_dict[node['category']])).add_to(MapOfNetwork)

    MapOfNetwork.save('Results/Plots/DistributorNetworkTest.html')

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
        MapOfNetwork.save('Results/Plots/DistributorNetworkTest.html')
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
        MapOfNetwork.save('Results/Plots/DistributorNetworkTest.html')

locations = pickle.load(open('established_locations_list.p', 'rb'))[0]
print_established_locations(locations)



