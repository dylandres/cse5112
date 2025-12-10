# Problem 3

def hash(a, b, item, p, w, i):
    return ((a[i] * item + b[i]) % p) % w

def count_min_sketch(a, b, p, w, stream):
    """
    Inputs:
    - a, b: vectors with positive entries
    - p, w: a scalar
    Outputs:
    - a sketch matrix, of size d x w
    """
    sketch_matrix = [[0] * w for _ in range(len(a))]

    for item in stream:
        for i in range(len(a)):
            sketch_matrix[i][hash(a, b, item, p, w, i)] += 1

    return sketch_matrix
