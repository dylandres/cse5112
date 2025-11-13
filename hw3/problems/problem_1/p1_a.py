
def is_bipartite(g_l):
    g_undir = {}
    for u in g_l:
        if u not in g_undir:
            g_undir[u] = []
        for v in g_l[u]:
            if v not in g_undir:
                g_undir[v] = []
            g_undir[u].append(v)
            g_undir[v].append(u)

    color = {}
    for node in g_undir:
        if node not in color:
            queue = [node]
            # assign color
            color[node] = 0
            while queue:
                u = queue.pop(0)
                # look at neighbors
                for v in g_undir[u]:
                    # assigned opposite color
                    if v not in color:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    # colored already with same color
                    elif color[v] == color[u]:
                        return False
    return True
