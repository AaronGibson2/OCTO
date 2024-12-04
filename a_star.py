import heapq
from typing import Dict, List, Set, Tuple, Optional, Mapping, Callable, Any




def a_star(
    graph: Any,
    start_node: int,
    end_node: int,
    heuristic: Callable[[int, int], float]
) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Implement A* pathfinding algorithm.
   
    Args:
        graph: Graph object with .nodes(), .neighbors(), .get_edge_data() methods
        start_node: Starting node for path finding
        end_node: Destination node
        heuristic: Function to estimate distance between two nodes
   
    Returns:
        Tuple of (g_scores, previous nodes) dictionaries
   
    Raises:
        ValueError if start or end nodes are not in the graph
    """
    # Validate input nodes
    graph_nodes = set(graph.nodes())
    if start_node not in graph_nodes or end_node not in graph_nodes:
        raise ValueError("Start or end node not in graph")




    # Initialize scores
    g_score = {node: float('infinity') for node in graph_nodes}
    f_score = {node: float('infinity') for node in graph_nodes}




    g_score[start_node] = 0
    f_score[start_node] = heuristic(start_node, end_node)




    # Track previous nodes for path reconstruction
    previous: Dict[int, Optional[int]] = {node: None for node in graph_nodes}




    # Priority queue stores (f_score, node)
    pq = [(f_score[start_node], start_node)]
    visited: Set[int] = set()




    while pq:
        current_f_score, current_node = heapq.heappop(pq)




        # Early exit if we've reached the end node
        if current_node == end_node:
            break




        # Skip already visited nodes
        if current_node in visited:
            continue
        visited.add(current_node)




        # Check all neighbors
        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue




            # Get edge weight (assumes first edge has 'length' attribute)
            edge_data = graph.get_edge_data(current_node, neighbor)
            edge_length = edge_data[0]['length']




            # Calculate tentative g_score
            tentative_g_score = g_score[current_node] + edge_length




            # Relaxation step
            if tentative_g_score < g_score[neighbor]:
                # Update path
                previous[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_node)




                # Add to priority queue
                heapq.heappush(pq, (f_score[neighbor], neighbor))




    # Check if path exists
    if g_score[end_node] == float('infinity'):
        print(f"No path exists between {start_node} and {end_node}")




    return g_score, previous




def reconstruct_path(
    previous: Mapping[int, Optional[int]],
    start_node: int,
    end_node: int
) -> List[int]:
    """
    Reconstruct the shortest path from start to end node.
   
    Args:
        previous: Dictionary mapping nodes to their previous nodes
        start_node: Starting node
        end_node: Destination node
   
    Returns:
        List of nodes representing the shortest path
    """
    path = []
    current_node = end_node




    # Traverse back to start node
    while current_node is not None:
        path.append(current_node)
        current_node = previous[current_node]




    # Reverse to get start to end order
    return path[::-1]
