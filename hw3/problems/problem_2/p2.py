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
    pass