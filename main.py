# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import matplotlib.pyplot as plt
import networkx
import osmnx as ox

# M A P   S E T U P ------------------------------------------------

# Location and map settings
location = "Orange County, Florida, USA"
graph = ox.graph_from_place(location, network_type='drive')


# Visualization set up
fig, ax = ox.plot_graph(
    graph,
    node_size=0,
    node_color='#66cc66',
    edge_color='blue',
    edge_linewidth=1,
    edge_alpha=0.5,
    bgcolor='white'
)

plt.show()

# Get data points
num_nodes = len(graph.nodes())
num_edges = len(graph.edges())

print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")

# Save the graph to a file for later reuse
ox.save_graphml(graph, filepath="data/gainesville.graphml")
