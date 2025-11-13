# Problem 3b — 2-opt Local Search
#
# Implement local_search_2opt(c, init) as specified in the HW3 PDF.
# - c: n x n symmetric cost matrix (float('inf') on diagonal)
# - init: a tuple or list representing a permutation of 1..n (1-based labels)
# Return:
# - an improved permutation (as a tuple) obtained by repeatedly applying 2-opt
#   until no improving swap exists.
#
# Notes:
# - cost(s) = sum_{i=1..n-1} c[s[i]][s[i+1]] with 1-based gene labels
# - 2-opt(i,j) reverses the subsequence s[i..j] (0-based positions)
# - Only accept a swap if it strictly improves total path cost.

def local_search_2opt(cost_matrix, init):
    """
    Perform 2-opt local search on a path (not a cycle).

    Args:
        cost_matrix: list[list[float]] of shape n x n, symmetric, c[i][i] = inf
        init: sequence (list/tuple) of 1..n (1-based labels)

    Returns:
        tuple: locally optimal permutation under 2-opt.
    """
    seq = list(init)

    def cost(s):
        return sum([cost_matrix[s[i] - 1][s[i + 1] - 1] for i in range(len(s) - 1)])

    current_cost = cost(seq)

    while True:
        best_delta = 0
        best_i = -1
        best_j = -1
        for i in range(len(seq) - 1):
            for j in range(i + 1, len(seq)):
                seq[i], seq[j] = seq[j], seq[i]
                new_cost = cost(seq)
                seq[i], seq[j] = seq[j], seq[i]
                delta = new_cost - current_cost
                if delta < best_delta:
                    best_delta = delta
                    best_i = i
                    best_j = j

        # best possible delta
        if best_delta >= 0:
            break

        # apply best swap
        seq[best_i], seq[best_j] = seq[best_j], seq[best_i]
        current_cost += best_delta

    return tuple(seq)
