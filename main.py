# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import matplotlib.pyplot as plt
import networkx
import osmnx as ox
from typing import Dict, Tuple
import numpy as np
import time
import random

from dijkstras import dijkstra, reconstruct_path
from a_star import a_star 


# H E L P E R   F U N C T I O N S ----------------------------------
def create_node_positions(graph) -> Dict[int, Tuple[float, float]]:
    """Create a dictionary of node positions using latitude and longitude"""
    return {node: (data['x'], data['y'])
            for node, data in graph.nodes(data=True)}


def euclidean_heuristic(pos1, pos2, positions):
    """Calculate Euclidean distance between two nodes using their positions"""
    x1, y1 = positions[pos1]
    x2, y2 = positions[pos2]
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def manhattan_heuristic(pos1, pos2, positions) -> float:
    x1, y1 = positions[pos1]
    x2, y2 = positions[pos2]
    return abs(x1 - x2) + abs(y1 - y2)


def relaxed_manhattan_heuristic(pos1, pos2, positions, factor=0.8) -> float:
    x1, y1 = positions[pos1]
    x2, y2 = positions[pos2]
    return factor * (abs(x1 - x2) + abs(y1 - y2))


# M A I N   P R O G R A M ------------------------------------------
def main():
    # Location and map settings
    location = "Orange County, Florida, USA"
    graph = ox.graph_from_place(location, network_type='drive')


    # Get data points for verification
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

    # Use two random nodes for TESTING
    nodes = list(graph.nodes())
   
    # Ensure we don't pick the same start and end nodes
    while True:
        start_node = nodes[random.randint(0, len(nodes) - 1)]
        end_node = nodes[random.randint(0, len(nodes) - 1)]
        if start_node != end_node:
            break

    print(f"Start Node: {start_node}")
    print(f"End Node: {end_node}")

    # Create positions dictionary for heuristic
    positions = create_node_positions(graph)

    # Create heuristic function closure
    heuristic = lambda n1, n2: relaxed_manhattan_heuristic(n1, n2, positions)


    # Run Dijkstra's Algorithm
    dijkstra_start_time = time.time()
    dijkstra_distances, dijkstra_previous = dijkstra(graph, start_node, end_node)
    dijkstra_end_time = time.time()
    dijkstra_elapsed_time = dijkstra_end_time - dijkstra_start_time

    # Run A* Algorithm
    astar_start_time = time.time()
    astar_distances, astar_previous = a_star(graph, start_node, end_node, heuristic)
    astar_end_time = time.time()
    astar_elapsed_time = astar_end_time - astar_start_time

    # Get the shortest paths
    dijkstra_path = reconstruct_path(dijkstra_previous, start_node, end_node)
    astar_path = reconstruct_path(astar_previous, start_node, end_node)

    # Print Performance Comparison
    print("\n--- Performance Comparison ---")
    print(f"Dijkstra's Algorithm:")
    print(f"  Time taken: {dijkstra_elapsed_time:.6f} seconds")
    print(f"  Total distance: {dijkstra_distances[end_node]:.2f} meters")
    print(f"  Nodes in path: {len(dijkstra_path)}")

    print("\nA* Algorithm:")
    print(f"  Time taken: {astar_elapsed_time:.6f} seconds")
    print(f"  Total distance: {astar_distances[end_node]:.2f} meters")
    print(f"  Nodes in path: {len(astar_path)}")

    # Verify path consistency
    print("\n--- Path Verification ---")
    if dijkstra_distances[end_node] == astar_distances[end_node]:
        print("Path distances match ✓")
    else:
        print("Path distances do NOT match! ✗")
        print(f"Dijkstra distance: {dijkstra_distances[end_node]}")
        print(f"A* distance: {astar_distances[end_node]}")

    # Visualize both paths
    # Alternate between Dijkstra and A* paths with multiple calls to plt.show()
   
    # Dijkstra Path
    fig1, ax1 = ox.plot_graph_route(
        graph,
        dijkstra_path,
        route_color='red',
        route_linewidth=6,
        route_alpha=0.5,
        node_size=0,
        edge_color='blue',
        edge_linewidth=1,
        edge_alpha=0.5,
        bgcolor='white'
    )
    plt.title("Shortest Path using Dijkstra's Algorithm")
    plt.show()


    # A* Path
    fig2, ax2 = ox.plot_graph_route(
        graph,
        astar_path,
        route_color='green',
        route_linewidth=6,
        route_alpha=0.5,
        node_size=0,
        edge_color='blue',
        edge_linewidth=1,
        edge_alpha=0.5,
        bgcolor='white'
    )
    plt.title("Shortest Path using A* Algorithm")
    plt.show()

if __name__ == "__main__":
    main()
