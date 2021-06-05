import os

import networkx as nx
import matplotlib.pyplot as plt
import folium



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



