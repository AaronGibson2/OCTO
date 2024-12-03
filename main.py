# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import matplotlib.pyplot as plt
import networkx
import osmnx as ox

from dijkstras import dijkstra, reconstruct_path

# M A P   S E T U P ------------------------------------------------

# Location and map settings
location = "Orange County, Florida, USA"
graph = ox.graph_from_place(location, network_type='drive')

# Get data points for verification
num_nodes = len(graph.nodes())
num_edges = len(graph.edges())
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")

# Use two random nodes for TESTING ------------
nodes = list(graph.nodes())

start_node = nodes[0]
end_node = nodes[100]

# Run our implementation
distances, previous = dijkstra(graph, start_node, end_node)

# Get the shortest path
path = reconstruct_path(previous, start_node, end_node)


print(f"Total distance: {distances[end_node]:.2f} meters")

# Set up visualization with that path
fig, ax = ox.plot_graph_route(
    graph,
    path,
    route_color='red',
    route_linewidth=6,
    route_alpha=0.5,
    node_size=0,
    edge_color='blue',
    edge_linewidth=1,
    edge_alpha=0.5,
    bgcolor='white'
)

plt.show()



# Save the graph to a file for later reuse
ox.save_graphml(graph, filepath="data/gainesville.graphml")
