# Problem 1a,b,c 
# NOTE: Problem B and C are to be implemented in this file as well

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from collections import defaultdict


class Graph:
    def __init__(self):
        self._nodes = set()
        self._edges = {}

    def add_node(self, n):
        self._nodes.add(n)

    def add_nodes_from(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_edge(self, u, v, **attrs):
        self._nodes.add(u)
        self._nodes.add(v)
        self._edges[(u, v)] = attrs

    def nodes(self):
        return list(self._nodes)

    def edges(self, data=False):
        if data:
            for (u, v), attrs in self._edges.items():
                yield (u, v, attrs)
        else:
            for (u, v) in self._edges.keys():
                yield (u, v)


def _draw_graph(graph, pos, labels, title):
    plt.figure(figsize=(6, 4))
    ax = plt.gca()

    # draw nodes
    xs = []
    ys = []
    for n in graph.nodes():
        x, y = pos[n]
        xs.append(x)
        ys.append(y)
    ax.scatter(xs, ys, s=1200, color="lightblue", zorder=2)

    # draw labels
    for n in graph.nodes():
        x, y = pos[n]
        ax.text(x, y, labels.get(n, str(n)), ha="center", va="center",
                fontsize=8, zorder=3)

    # draw edges
    for (u, v) in graph.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="->",
            mutation_scale=20,
            linewidth=1.0,
            color="black",
            zorder=1,
        )
        ax.add_patch(arrow)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def plan_city_a(num_data_hubs, num_service_providers,
                connections, provider_capacities,
                preliminary_assignment):
    graph = Graph()

    # add source
    source = "source"
    graph.add_node(source)

    # hubs
    for h in range(num_data_hubs):
        graph.add_node(h)

    # providers
    offset = num_data_hubs
    for j in range(num_data_hubs, num_data_hubs + num_service_providers):
        p = j
        graph.add_node(p)

    # add source to hub edges
    for h in range(num_data_hubs):
        graph.add_edge(source, h)

    # add hub to provider edges
    for h, provs in connections.items():
        for p in provs:
            graph.add_edge(h, p)

    # positions
    pos = {}
    pos[source] = (0, 0)
    for i, h in enumerate(range(num_data_hubs)):
        pos[h] = (1, i - (num_data_hubs - 1) / 2)

    for j in range(num_service_providers):
        p = offset + j
        pos[p] = (2, j - (num_service_providers - 1) / 2)

    # labels
    labels = {source: "s"}
    for h in range(num_data_hubs):
        labels[h] = f"hub{h}"
    for j in range(num_service_providers):
        p = offset + j
        labels[p] = f"prov{p}"

    # draw A
    _draw_graph(graph, pos, labels, "Problem 1(a)")

    # add sink
    sink = "sink"
    graph.add_node(sink)

    # add provider to sink edges with capacities
    for j in range(num_service_providers):
        p = offset + j
        cap = provider_capacities[p]
        graph.add_edge(p, sink, capacity=cap)

    pos_b = dict(pos)
    pos_b[sink] = (3, 0)

    labels_b = dict(labels)
    labels_b[sink] = "t"

    # draw B
    _draw_graph(graph, pos_b, labels_b, "Problem 1(b)")

    # build flow from preliminary_assignment
    flow = defaultdict(int)

    for hub, prov in preliminary_assignment.items():
        flow[(source, hub)] += 1
        flow[(hub, prov)] += 1
        flow[(prov, sink)] += 1

    # residual graph
    residual = Graph()
    residual.add_nodes_from(graph.nodes())

    for u, v, data in graph.edges(data=True):
        cap = data.get("capacity", 1)
        f = flow[(u, v)]

        # forward capacity
        forward_cap = cap - f
        if forward_cap > 0:
            residual.add_edge(u, v, capacity=forward_cap)

        # backward capacity
        if f > 0:
            residual.add_edge(v, u, capacity=f)

    # draw C
    _draw_graph(residual, pos_b, labels_b, "Problem 1(c) - Residual Graph")


if __name__ == "__main__":
    plan_city_a(
        num_data_hubs=5,
        num_service_providers=5,
        connections={
            0: [5, 7, 8],
            1: [5, 8],
            2: [7, 8, 9],
            3: [5, 6, 8, 9],
            4: [5, 6, 7, 8],
        },
        provider_capacities=[0] * 5 + [0, 1, 0, 2, 2],
        preliminary_assignment={0: 8, 1: 8, 2: 9, 3: 9},
    )
