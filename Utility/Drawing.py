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

def easy_case_drawing(ParetoFrontier):
    x = [i for i in range(6, 25)]
    y = [((200 - 5 * x[i]) / 4) for i in range(len(x))]
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.plot([0, 12], [40, 40], 'blue', label='x2 <= 40')
    plt.plot([20, 20], [0, 30], 'green', label='x1 <= 20')
    plt.plot(x, y, 'cyan', label='5*x1 + 4*x2 <= 200')
    plt.arrow(5, 20, 5, 0, head_width=0.5, head_length=0.7, fc='magenta', ec='magenta', label='f1')
    plt.arrow(5, 25, 3, 4, head_width=0.5, head_length=0.7, fc='red', ec='red', label='f2')
    plt.legend()
    plt.savefig('Results/SolutionSpace.png', dpi=500)
    plt.plot(ParetoFrontier['x1'], ParetoFrontier['x2'], 'bo', label='non-dominated Solutions')
    plt.legend()
    plt.savefig('Results/ParetoFrontier.png', dpi=500)
    plt.show()



