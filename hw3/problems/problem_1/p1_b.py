# Problem 1b


def maximal_bipartite_match(g) -> int:

    def has_path(u, visited):
        for v in range(len(g[0])):
            if g[u][v] and not visited[v]:
                visited[v] = True
                if connected_to[v] == -1 or has_path(connected_to[v], visited):
                    connected_to[v] = u
                    return True
        return False

    connected_to = [-1] * len(g[0])
    matches = 0
    for u in range(len(g)):
        visited = [False] * len(g[0])
        if has_path(u, visited):
            matches += 1
    return matches
