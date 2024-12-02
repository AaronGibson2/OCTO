import matplotlib.pyplot as plt
import osmnx as ox


# Define location and settings
location = "Gainesville, Florida, USA"
graph = ox.graph_from_place(location, network_type='drive')

# Save the graph to a file for later reuse
ox.save_graphml(graph, filepath="data/gainesville.graphml")


print("working")
