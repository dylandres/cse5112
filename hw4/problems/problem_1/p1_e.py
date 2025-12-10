# Problem 1e

from collections import defaultdict, deque

class Graph:
    def __init__(self):
        self._nodes = set()
        self._adj = {}

    def add_node(self, n):
        if n not in self._nodes:
            self._nodes.add(n)
            self._adj.setdefault(n, {})

    def add_nodes_from(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_edge(self, u, v, **attrs):
        self.add_node(u)
        self.add_node(v)
        self._adj[u][v] = dict(attrs)

    def nodes(self):
        return list(self._nodes)

    def edges(self, data=False):
        for u in self._adj:
            for v, attrs in self._adj[u].items():
                if data:
                    yield (u, v, attrs)
                else:
                    yield (u, v)

    def has_edge(self, u, v):
        return u in self._adj and v in self._adj[u]

    def remove_edge(self, u, v):
        if u in self._adj and v in self._adj[u]:
            del self._adj[u][v]

    def __getitem__(self, u):
        return self._adj[u]


def plan_city_e(num_data_hubs,
                num_service_providers,
                connections,
                provider_capacities,
                preliminary_assignment):
    graph, residual, source, sink, flow = _build_graph_and_residual(
        num_data_hubs,
        num_service_providers,
        connections,
        provider_capacities,
        preliminary_assignment,
    )

    # Run Ford–Fulkerson
    while True:
        found, parent = _bfs(residual, source, sink)
        if not found:
            break
        _augment_flow(graph, residual, flow, parent, source, sink)

    assigned_hubs = 0
    for h in range(num_data_hubs):
        if flow[(source, h)] > 0:
            assigned_hubs += 1

    offset = num_data_hubs

    # feasible
    if assigned_hubs == num_data_hubs:
        assignments = []
        for h in range(num_data_hubs):
            assigned_provider = 0
            for p in connections.get(h, []):
                if flow[(h, p)] > 0:
                    assigned_provider = p
                    break
            assignments.append(assigned_provider)
        return assignments

    # not feasible
    assignments = [0] * num_data_hubs
    reachable = set([source])
    q = deque([source])
    while q:
        u = q.popleft()
        for v, data in residual[u].items():
            if data["capacity"] > 0 and v not in reachable:
                reachable.add(v)
                q.append(v)

    # find which providers need +1 capacity
    provider_increments = [0] * num_service_providers
    for j in range(num_service_providers):
        p = offset + j
        if p in reachable and graph.has_edge(p, sink):
            cap = graph[p][sink]["capacity"]
            used = flow[(p, sink)]
            if used == cap:
                provider_increments[j] = 1

    return assignments + provider_increments


def _build_graph_and_residual(num_data_hubs,
                              num_service_providers,
                              connections,
                              provider_capacities,
                              preliminary_assignment):
    graph = Graph()

    # nodes
    source = "source"
    sink = "sink"
    graph.add_node(source)

    # hubs
    for h in range(num_data_hubs):
        graph.add_node(h)

    # providers
    offset = num_data_hubs
    for j in range(num_service_providers):
        p = offset + j
        graph.add_node(p)

    # source -> hub edges
    for h in range(num_data_hubs):
        graph.add_edge(source, h)

    # hub -> provider edges
    for h, provs in connections.items():
        for p in provs:
            graph.add_edge(h, p)

    # provider -> sink edges
    graph.add_node(sink)
    for j in range(num_service_providers):
        p = offset + j
        cap = provider_capacities[p]
        graph.add_edge(p, sink, capacity=cap)

    flow = defaultdict(int)
    for hub, prov in preliminary_assignment.items():
        flow[(source, hub)] += 1
        flow[(hub, prov)] += 1
        flow[(prov, sink)] += 1

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

    return graph, residual, source, sink, flow


def _bfs(residual, source, sink):
    parent = {source: None}
    q = deque([source])
    while q:
        u = q.popleft()
        for v, data in residual[u].items():
            cap = data["capacity"]
            if cap > 0 and v not in parent:
                parent[v] = u
                if v == sink:
                    return True, parent
                q.append(v)

    return False, parent


def _augment_flow(graph, residual, flow, parent, source, sink):
    # find bottleneck capacity
    bottleneck = float("inf")
    v = sink
    while v != source:
        u = parent[v]
        cap = residual[u][v]["capacity"]
        bottleneck = min(bottleneck, cap)
        v = u

    # update residual and flow
    v = sink
    while v != source:
        u = parent[v]

        # update forward edge
        residual[u][v]["capacity"] -= bottleneck
        if residual[u][v]["capacity"] == 0:
            residual.remove_edge(u, v)

        # update backward edge
        if residual.has_edge(v, u):
            residual[v][u]["capacity"] += bottleneck
        else:
            residual.add_edge(v, u, capacity=bottleneck)

        # update flow
        if graph.has_edge(u, v):
            flow[(u, v)] += bottleneck
        else:
            # path uses a backward residual edge, reduce flow
            flow[(v, u)] -= bottleneck

        v = u
