# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

import numpy as np
import osmnx as ox
import os
import time

from dijkstras import dijkstra, reconstruct_path
from a_star import a_star
from statWindow import create_stat_window

# H E L P E R   F U N C T I O N S ----------------------------------

# Heuristic for A* algorithm using Haversine Formula
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

# M A I N ----------------------------------------------------------

def main(algorithm='Dijkstra\'s & A*', city_map='Gainesville'):
    global fig, ax, graph_proj

    # M A P   S E T U P ------------------------------------------------
    graph_file = f"graphml_files/{city_map}.graphml"

    if not os.path.exists(graph_file):
        print(f"Graph file not found: {graph_file}")
        return

    graph = ox.load_graphml(graph_file)

    # Projects the graph
    graph_proj = ox.project_graph(graph)

    # Print graph info to terminal for testing and verification
    num_nodes = len(graph_proj.nodes())
    num_edges = len(graph_proj.edges())
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

    # Global variables for click handling
    global selected_nodes, route_line, markers, a_route_line
    selected_nodes = []
    route_line = None  # Keep track of the route line
    markers = []  # Keep track of markers

    a_route_line = None

    def clear_map():

        global selected_nodes, route_line, markers, a_route_line
        # Clear routes
        if route_line:
            if isinstance(route_line, list):
                for line in route_line:
                    line.remove()
            else:
                route_line.remove()
            route_line = None

        if a_route_line:
            if isinstance(a_route_line, list):
                for line in a_route_line:
                    line.remove()
            else:
                a_route_line.remove()
            a_route_line = None

        # Clear markers
        for marker in markers:
            marker.remove()
        markers.clear()

        # Clear selected nodes
        selected_nodes.clear()

        # Clear legend
        ax.legend_.remove() if ax.get_legend() else None

        plt.draw()

    def on_key(event):
        global selected_nodes, route_line, a_route_line

        # Space key to trace route
        if event.key == ' ' and len(selected_nodes) == 2:
            start_node, end_node = selected_nodes

            # Get node positions for A* heuristic
            positions = {node: (data['x'], data['y'])
                        for node, data in graph.nodes(data=True)}

            heuristic = lambda n1, n2: haversine_distance(n1, n2, positions)

            # Run Dijkstra's Algorithm
            # Calculate time taken to completely run Dijkstra's algorithm from start node to end node
            dijkstra_start_time = time.time()
            dijkstra_distances, dijkstra_previous, djikstra_visited = dijkstra(graph, start_node, end_node)
            dijkstra_end_time = time.time()
            dijkstra_nodes_visited = len(djikstra_visited)
            dijkstra_elapsed_time = dijkstra_end_time - dijkstra_start_time

            # Run A* Algorithm
            # Calculate time taken to completely run A* algorithm from start node to end node
            astar_start_time = time.time()
            astar_distances, astar_previous, astar_visited = a_star(graph, start_node, end_node, heuristic, positions)
            astar_end_time = time.time()
            astar_nodes_visited = len(astar_visited)
            astar_elapsed_time = astar_end_time - astar_start_time

            # Get the shortest paths
            dijkstra_path = reconstruct_path(dijkstra_previous, start_node, end_node)
            astar_path = reconstruct_path(astar_previous, start_node, end_node)

            stat_window = create_stat_window(
                elapsed_time_dijkstra=dijkstra_elapsed_time,
                elapsed_time_aStar=astar_elapsed_time,
                num_nodes_visited_dijkstra=dijkstra_nodes_visited,
                num_nodes_visited_aStar=astar_nodes_visited,
                distance_dijkstra=dijkstra_distances[end_node],
                distance_aStar=astar_distances[end_node])

            if dijkstra_distances[end_node] != float('inf'):
                # Clear previous route if it exists
                if route_line:
                    route_line.remove()

                # Plot the Dijkstra's route
                route_coords = []
                for node in dijkstra_path:
                    node_data = graph_proj.nodes[node]
                    route_coords.append((node_data['x'], node_data['y']))

                x_coords, y_coords = zip(*route_coords)

                # Bright orange route
                route_line = ax.plot(x_coords, y_coords,
                                   color='#FF8C00',  # Bright orange
                                   linewidth=1,
                                   alpha=0.8)[0]

                # Plot the A* route
                a_route_coords = []
                for node in astar_path:
                    a_node_data = graph_proj.nodes[node]
                    a_route_coords.append((a_node_data['x'], a_node_data['y']))

                a_x_coords, a_y_coords = zip(*a_route_coords)

                # Bright blue route
                a_route_line = ax.plot(a_x_coords, a_y_coords,
                                   color='#0096FF',  # Bright blue
                                   linewidth=1,
                                   alpha=0.8)[0]

                # Print values to terminal for testing
                print(f"Total Dijkstra's distance: {dijkstra_distances[end_node]:.2f} meters")
                print(f"Total A* distance: {astar_distances[end_node]:.2f} meters")
            else:
                print("No valid path found between selected points!")

            plt.draw()

        # X key to clear map
        elif event.key == 'x':
            clear_map()

    def on_click(event):
        global selected_nodes, graph_proj, route_line, markers
        if event.button is MouseButton.LEFT and event.inaxes == ax:
            # Get the clicked coordinates
            x, y = event.xdata, event.ydata

            # Find the nearest node to the clicked point
            nearest_node = ox.nearest_nodes(graph_proj, x, y)

            if len(selected_nodes) < 2:
                selected_nodes.append(nearest_node)
                # Bright orange markers
                marker = plt.plot(x, y, 'o', color='#FF8C00', markersize=5, alpha=0.9)[0]
                markers.append(marker)  # Store marker reference
                plt.draw()

    # Close any existing figures
    plt.close('all')

    # Configure plot settings
    plt.style.use('dark_background')
    plt.rcParams.update({
        'figure.facecolor': 'black',
        'axes.facecolor': 'black',
        'savefig.facecolor': 'black',
    })

    # Set algorithm name
    algorithm_name = "Dijkstra's & A*"

    # Create the plot with background map - with minimal edge width
    fig, ax = ox.plot_graph(
        graph_proj,
        node_size=0,
        edge_color='white',     # White edges
        edge_linewidth=0.3,
        edge_alpha=0.5,
        bgcolor='black',        # Black background
        show=False,
        figsize=(8, 8)        # Square figure size
    )

    fig.canvas.manager.set_window_title(f"{city_map.capitalize()} - {algorithm_name}")

    # Remove the attribution text
    ax.text(0.99, 0.01, '', transform=ax.transAxes, ha='right', va='bottom')

    # Hide all axes text and ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Remove all margins and spacing
    plt.subplots_adjust(left=0, right=1, top=0.98, bottom=0)

    # Connect the events
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Ensure the plot fills the axes
    ax.set_aspect('auto')

    plt.show()

# M A I N ----------------------------------------------------------
if __name__ == "__main__":
    # If run directly, use defaults
    main(algorithm='dijkstra', city_map='Gainesville')
