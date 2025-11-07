# Problem 1b

def _get_tree_root(values, adjacency):
    child_nodes = set()
    for children in adjacency.values():
        for c in children:
            child_nodes.add(c)
    for node in values.keys():
        if not node in child_nodes:
            return node

def _maxsum_helper(root, values, adjacency):
    take_root_sum = values[root]
    skip_root_sum = 0

    for child in adjacency.get(root, []):
        include_child_sum, skip_child_sum = _maxsum_helper(child, values, adjacency)
        take_root_sum += skip_child_sum
        skip_root_sum += max(include_child_sum, skip_child_sum)

    return take_root_sum, skip_root_sum

def maxsum_tree(values, adjacency):
    if len(values) == 0:
        return 0
    if len(values) == 1:
        return values.get(list(values.keys())[0])
    
    root = _get_tree_root(values, adjacency)

    take_root_sum, skip_root_sum = _maxsum_helper(root, values, adjacency)
    return max(take_root_sum, skip_root_sum)
