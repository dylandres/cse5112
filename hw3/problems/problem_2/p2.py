# Problem 2

def min_cut(n: int, edge_list: list[tuple[int, int]]) -> int:
    """
    Compute the minimum number of passages (edges) that must be blocked 
    to disconnect Dr. Heinz Doofenshmirtz (at junction 1) from the Tata 
    Innovation Center (at junction n) in a network of junctions.

    The problem is equivalent to finding the minimum cut between node 1 
    and node n in an undirected, unweighted graph.

    Parameters
    ----------
    n : int
        Total number of junctions (1-indexed). 
        Junction 1 represents Doofenshmirtz's studio, and junction n 
        represents the Tata Innovation Center.
        You may assume n ≤ 500.
    
    edge_list : list[tuple[int, int]]
        A list of undirected edges where each tuple (x, y) indicates a 
        two-way passage between junctions x and y. 
        There is at most one passage between any two junctions.

    Returns
    -------
    int
        The minimum number of edges that must be removed to make 
        junction 1 and junction n disconnected.

    Examples
    --------
    >>> min_cut(5, [(1,2), (3,4), (1,5), (2,5)])
    2
    >>> min_cut(12, [(1,4), (1,8), (1,9), (8,9), (9,12), (8,11), (8,12), (3,4), (3,12), (1,5), (2,5)])
    3
    """
    bloomberg = 1
    tata = n
    paths_to_block = 0

    capacities = [[0] * (n + 1) for _ in range(n + 1)]
    for u, v in edge_list:
        capacities[u][v] += 1
        capacities[v][u] += 1

    while True:
        parent = [-1] * (n + 1)
        parent[bloomberg] = bloomberg
        queue = [bloomberg]
        path_cap = [0] * (n + 1)
        path_cap[bloomberg] = float("inf")

        head = 0
        found = False
        while head < len(queue) and not found:
            u = queue[head]
            head += 1
            for v in range(1, n + 1):
                if parent[v] == -1 and capacities[u][v] > 0:
                    parent[v] = u
                    path_cap[v] = min(path_cap[u], capacities[u][v])
                    queue.append(v)
                    if v == tata:
                        found = True
                        break

        # no path
        if parent[tata] == -1:
            break

        f = path_cap[tata]
        paths_to_block += f

        v = tata
        while v != bloomberg:
            u = parent[v]
            capacities[u][v] -= f
            capacities[v][u] += f
            v = u

    return paths_to_block
