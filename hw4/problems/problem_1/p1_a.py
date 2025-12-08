# Problem 1a,b,c 
# NOTE: Problem B and C are to be implemented in this file as well

import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def plan_city_a(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment):
    graph = nx.DiGraph()

    # add source
    source = "source"
    graph.add_node(source)

    # hubs
    for h in range(num_data_hubs):
        graph.add_node(h)
    # provides
    offset = num_data_hubs
    for j in range(num_service_providers):
        p = offset + j
        graph.add_node(p)

    # add source to hub edges
    for h in range(num_data_hubs):
        graph.add_edge(source, h)

    # add hub to provider edges
    for h, provs in connections.items():
        for p in provs:
            graph.add_edge(h, p)
    pos = {}
    pos[source] = (0, 0)
    for i, h in enumerate(range(num_data_hubs)):
        pos[h] = (1, i - (num_data_hubs - 1) / 2)

    for j in range(num_service_providers):
        p = offset + j
        pos[p] = (2, j - (num_service_providers - 1) / 2)

    # label
    labels = {source: "s"}
    for h in range(num_data_hubs):
        labels[h] = f"hub{h}"
    for j in range(num_service_providers):
        p = offset + j
        labels[p] = f"prov{p}"

    # draw A
    plt.figure(figsize=(6, 4))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        labels=labels,
        node_size=1200,
        node_color="lightblue",
        arrows=True,
        arrowsize=20,
        font_size=8,
    )
    plt.title("Problem 1(a)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    # add sink
    sink = "sink"
    graph.add_node(sink)

    # add provider to sink edges
    for j in range(num_service_providers):
        p = offset + j
        cap = provider_capacities[p]
        graph.add_edge(p, sink, capacity=cap)

    pos_b = dict(pos)
    pos_b[sink] = (3, 0)

    labels_b = dict(labels)
    labels_b[sink] = "t"

    # draw B
    plt.figure(figsize=(6, 4))
    nx.draw(
        graph,
        pos_b,
        with_labels=True,
        labels=labels_b,
        node_size=1200,
        node_color="lightblue",
        arrows=True,
        arrowsize=20,
        font_size=8,
    )
    plt.title("Problem 1(b)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    flow = defaultdict(int)

    for hub, prov in preliminary_assignment.items():
        flow[(source, hub)] += 1
        flow[(hub, prov)] += 1
        flow[(prov, sink)] += 1

    residual = nx.DiGraph()
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

    # reuse labels
    pos_c = pos_b
    labels_c = labels_b

    # draw C
    plt.figure(figsize=(6, 4))
    nx.draw(
        residual,
        pos_c,
        with_labels=True,
        labels=labels_c,
        node_size=1200,
        node_color="lightblue",
        arrows=True,
        arrowsize=20,
        font_size=8,
    )
    plt.title("Problem 1(c) - Residual Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    
if __name__ == "__main__":
    plan_city_a(num_data_hubs=5,
                num_service_providers=5,
                connections={0: [5 ,7 ,8] , 1: [5 , 8] , 2: [7 ,8 ,9] , 3: [5 , 6 , 8 , 9] , 4: [5 ,6 ,7 ,8]},
                provider_capacities=[0] * 5 + [0 ,1 ,0 ,2 ,2],
                preliminary_assignment={0: 8 , 1: 8 , 2: 9 , 3: 9})
