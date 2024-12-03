# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import heapq
from typing import Dict, List, Set, Tuple, Optional, Mapping, Callable


# F U N C T I O N S ------------------------------------------------

# Manhattan Heuristic
def manhattan_heuristic(node1: int, node2: int, node_positions: Dict[int, Tuple[int, int]]) -> float:
    x1, y1 = node_positions[node1]
    x2, y2 = node_positions[node2]
    return abs(x1 - x2) + abs(y1 - y2)

# A* Algorithm Implementation
def a_star(graph, start_node: int, end_node: int, heuristic: Callable[[int, int], float]) -> Tuple[Dict[int, float], Dict[int,Optional[int]]]:
    # Set all unknown node distances to infinity
    distances = {node: float('infinity') for node in graph.nodes()}

    # Set distance from starting_node to starting_node to 0
    distances[start_node] = 0

    # Dictionary to store previous nodes for optimal path
    previous: Dict[int, Optional[int]] = {node: None for node in graph.nodes()}

    # Priority queu to store distance to node pairs as we discover
    # Add one item start_node to start_node distance of 0
    pq = [(0, start_node)]

    # Set to keep track of those visited
    visited: Set[int] = set()

    # While my PQ is not empty
    while pq:

        # Unpack from pq using heapop()
        current_f, current_node = heapq.heappop(pq)

        # Check if we are at end node
        if current_node == end_node:
            break

        # Check if the node we are at has been visited
        if current_node in visited:
            continue    # Skip if it has been visited
        # Add current_node to those visited
        visited.add(current_node)

        # Check all neighbors of the current node
        for neighbor in graph.neighbors(current_node):
            # If we have already seen neighbor then skip
            if neighbor in visited:
                continue

            # Get edge data from current to neighbor
            edge_data = graph.get_edge_data(current_node, neighbor)

            # Get the first edge and get length attribute
            edge_length = edge_data[0]['length']

            # Calculate actual cost to neighbor
            g_cost = distances[current_node] + edge_length
            
            # Calculate heuristic estimate
            h_cost = heuristic(neighbor, end_node)

            # Calculate estimated cost
            f_cost = g_cost + h_cost
            
            # Perform Relaxation
            if f_cost < distances[neighbor]:
                distances[neighbor] = g_cost
                previous[neighbor] = current_node

                # Push new edge into pq
                heapq.heappush(pq, (f_cost, neighbor))


    return distances, previous

# Reconstructs path from start -> end using previous dict
def reconstruct_path(previous: Mapping[int, Optional[int]], start_node: int, end_node: int) -> List[int]:

    # Initialize list path
    path = []
    current_node = end_node

    # Traverse previous dict to get optimal path
    while current_node is not None:
        path.append(current_node)
        current_node = previous[current_node]

    # Return reversed path to get start to end
    return path[::-1]
