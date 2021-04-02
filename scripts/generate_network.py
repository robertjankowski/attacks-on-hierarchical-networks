import numpy as np
from graph_tool.all import *


def erdos_renyi_v1(N, p):
    g = Graph(directed=False)
    for i in range(N):
        for j in range(i):
            if i != j:
                if np.random.rand() < p:
                    g.add_edge(i, j)
    return g


def erdos_renyi_v2(N, p):
    def deg_sample():
        return np.random.poisson((N - 1) * p)

    g = random_graph(N, deg_sampler=deg_sample, directed=False)
    random_rewire(g, "erdos")
    return g


def barabasi_albert(N, m=3):
    return price_network(N, m=m, directed=False)