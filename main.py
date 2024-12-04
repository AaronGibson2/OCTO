# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import matplotlib.pyplot as plt
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
    return {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)}

def euclidean_heuristic(pos1, pos2, positions):
    """Calculate Euclidean distance between two nodes using their positions"""
    x1, y1 = positions[pos1]
    x2, y2 = positions[pos2]
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def manhattan_heuristic(pos1, pos2, positions) -> float:
    """Caclualte Manhattan distance between two nodes using grid positions"""
    x1, y1 = positions[pos1]
    x2, y2 = positions[pos2]
    return abs(x1 - x2) + abs(y1 - y2)

def haversine_distance(pos1, pos2, positions):
    """More accurate distance calculation using Haversine formula - Accounts for Earth's curvature"""
    R = 6371000  # Earth's radius in meters
    lat1, lon1 = positions[pos1]
    lat2, lon2 = positions[pos2]
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c

def improved_heuristic(node1, node2, positions):
    """Combine haversine distance and euclidean distance"""
    # Straight-line Haversine distance
    haversine_dist = haversine_distance(node1, node2, positions)
    
    # Euclidean distance as fallback
    euclidean_dist = euclidean_heuristic(node1, node2, positions)
    
    # Weighted combination
    return 0.7 * haversine_dist + 0.3 * euclidean_dist


# M A I N   P R O G R A M ------------------------------------------
def main():
    # Set location and map settings
    location = "Jacksonville, Florida, USA"
    graph = ox.graph_from_place(location, network_type='drive')


    # Get data points for display
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

    # Use two random nodes
    nodes = list(graph.nodes())
   
    # Ensure we don't pick the same start and end nodes
    while True:
        start_node = nodes[random.randint(0, len(nodes) - 1)]
        end_node = nodes[random.randint(0, len(nodes) - 1)]
        
        # Change for manual node selection

        # start_node = nodes[0]
        # end_node = nodes[11137]
        if start_node != end_node:
            break

    print(f"Start Coordinate: {start_node}")
    print(f"End Coordinate: {end_node}")

    # Create positions dictionary for heuristic
    positions = create_node_positions(graph)

    # Create heuristic function closure
    heuristic = lambda n1, n2: improved_heuristic(n1, n2, positions)

    # Run Dijkstra's Algorithm
    # Calculate time taken to completely run Dijkstra's algorithm from start node to end node
    dijkstra_start_time = time.time()
    dijkstra_distances, dijkstra_previous, dijkstra_visited = dijkstra(graph, start_node, end_node)
    dijkstra_end_time = time.time()
    dijkstra_elapsed_time = dijkstra_end_time - dijkstra_start_time

    # Run A* Algorithm
    # Calculate time taken to completely run A* algorithm from start node to end node
    astar_start_time = time.time()
    astar_distances, astar_previous, astar_visited = a_star(graph, start_node, end_node, heuristic, positions)
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
    print(f"  Nodes visited: {len(dijkstra_visited)}")

    print("\nA* Algorithm:")
    print(f"  Time taken: {astar_elapsed_time:.6f} seconds")
    print(f"  Total distance: {astar_distances[end_node]:.2f} meters")
    print(f"  Nodes in path: {len(astar_path)}")
    print(f"  Nodes visited: {len(astar_visited)}")

    # Verify path consistency between algorithms
    print("\n--- Path Verification ---")
    if dijkstra_distances[end_node] == astar_distances[end_node]:
        print("Path distances match ✓")
    else:
        print("Path distances do NOT match! ✗")
        print(f"Dijkstra distance: {dijkstra_distances[end_node]}")
        print(f"A* distance: {astar_distances[end_node]}")

    # Visualize both paths
   
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
    plt.show()

if __name__ == "__main__":
    main()
