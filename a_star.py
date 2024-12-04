import heapq
from typing import Dict, List, Set, Tuple, Optional, Mapping, Callable, Any

def a_star(graph, start_node: int, end_node: int, heuristic: Callable[[int, int], float], positions: Dict[int, Tuple[float, float]]) -> Tuple[Dict[int, float], Dict[int, Optional[int]], Set[int]]:
    """
    Implement A* pathfinding algorithm for OSMnx graph
    """
    # Validate input nodes
    graph_nodes = set(graph.nodes())
    if start_node not in graph_nodes or end_node not in graph_nodes:
        raise ValueError("Start or end node not in graph")

    # Initialize data structures
    g_score = {node: float('infinity') for node in graph_nodes}
    f_score = {node: float('infinity') for node in graph_nodes}
    g_score[start_node] = 0
    f_score[start_node] = heuristic(start_node, end_node)

    # Track previous nodes for path reconstruction
    previous: Dict[int, Optional[int]] = {node: None for node in graph_nodes}

    # Priority queue and visited tracking
    open_set = []
    heapq.heappush(open_set, (f_score[start_node], start_node))

    # Keep track of nodes in open set to avoid duplicates
    in_open_set = {start_node}

    # Efficiently track visited nodes
    visited: Set[int] = set()

    while open_set:
        # Get the node with lowest f_score
        _, current_node = heapq.heappop(open_set)
        in_open_set.remove(current_node)

        # if same node don't calculate
        if current_node == end_node:
            break

        # Mark node as visited
        visited.add(current_node)

        # Explore neighbors
        for neighbor in graph.neighbors(current_node):
            # Skip already visited nodes
            if neighbor in visited:
                continue

            # Get edge weight - use length from OSMnx graph
            try:
                edge_data = graph.get_edge_data(current_node, neighbor)[0]
                edge_length = edge_data.get('length', 1)  # in meters
            except Exception as e:
                print(f"Error getting edge data: {e}")
                continue

            # Calculate tentative g_score
            tentative_g_score = g_score[current_node] + edge_length

            # Potentially better path
            if tentative_g_score < g_score[neighbor]:
                # Update tracking
                previous[neighbor] = current_node
                g_score[neighbor] = tentative_g_score

                # Calculate f_score
                f_new = tentative_g_score + heuristic(neighbor, end_node)
                f_score[neighbor] = f_new

                # Add to open set if not already there
                if neighbor not in in_open_set:
                    heapq.heappush(open_set, (f_new, neighbor))
                    in_open_set.add(neighbor)

    return g_score, previous, visited
