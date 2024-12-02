# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import heapq
from typing import Dict, List, Set, Tuple


# F U N C T I O N S ------------------------------------------------

def dijkstra(graph, start_node: int, end_node: int) -> Tuple[Dict[int, float], Dict[int,int]]:

    # Set all unknown node distances to infinity
    distances = {node: float('infinity') for node in graph.nodes()}

    # Set distance from starting_node to starting_node to 0
    distances[start_node] = 0;
