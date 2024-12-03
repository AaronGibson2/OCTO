# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import matplotlib.pyplot as plt
import networkx
import osmnx as ox
import time

from dijkstras import dijkstra, reconstruct_path
from a_star import a_star, manhattan_heuristic

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
end_node = nodes[41999]

# For testing how long the algorithm takes to run
start_time = time.time()

# Run our implementation
# Djikstra's version
distances, previous = dijkstra(graph, start_node, end_node)

# A* version
# node_positions = {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)}
# distances, previous = a_star(graph, start_node, end_node, lambda n1, n2: manhattan_heuristic(n1, n2, node_positions))


# Get the shortest path
path = reconstruct_path(previous, start_node, end_node)

# Calculate how long the algorithm actually took
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to calculate: {elapsed_time:.2f} seconds")

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
