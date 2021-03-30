from graph_tool.all import *
import numpy as np
import sys
from tqdm import tqdm

sys.path.append('..')
from scripts.giant_connected_component import size_gcc


def get_vertices(g):
    return np.array(list(g.vertices()))


def simulate_random_attack(g, ps, ntimes=1):
    mean_sizes = []
    std_sizes = []
    N = g.num_vertices()
    all_vertices = get_vertices(g)
    for p in tqdm(ps):
        sizes_per_p = []
        for _ in range(ntimes):
            g_copy = g.copy()
            vertices = np.random.choice(all_vertices, int(N * p), replace=False)
            g_copy.remove_vertex(vertices)
            if g_copy.num_vertices() == 0:
                s = 0
            else:
                s = size_gcc(g_copy)
            sizes_per_p.append(s / N)
        mean_sizes.append(np.mean(sizes_per_p))
        std_sizes.append(np.std(sizes_per_p))

    return mean_sizes, std_sizes
