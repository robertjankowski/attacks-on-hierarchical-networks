from graph_tool.all import *
import numpy as np
import sys
from tqdm import tqdm
import pandas as pd

sys.path.append('..')
from scripts.hrg import load_dendrogram, generate_hrg
from scripts.giant_connected_component import size_gcc
from scripts.generate_network import erdos_renyi_v2, barabasi_albert


def get_vertices(g):
    return np.array(list(g.vertices()))


def get_edges(g):
    return np.array(list(g.edges()))


def simulate_attack_erdos_renyi(N, p_er, ps, random_attack=True, type='node', ntimes=1):
    mean_sizes = []
    std_sizes = []
    for p in tqdm(ps):
        sizes_per_p = []
        for _ in range(ntimes):
            g = erdos_renyi_v2(N, p_er)
            if random_attack:
                sizes_per_p.append(get_rescaled_gcc_size_after_random_attack(g, p, type=type))
            else:
                sizes_per_p.append(get_rescaled_gcc_size_after_intentional_attack(g, p))
        mean_sizes.append(np.mean(sizes_per_p))
        std_sizes.append(np.std(sizes_per_p))
    return mean_sizes, std_sizes


def simulate_attack_barabasi_albert(N, ps, m=3, random_attack=True, type='node', ntimes=1):
    mean_sizes = []
    std_sizes = []
    for p in tqdm(ps):
        sizes_per_p = []
        for _ in range(ntimes):
            g = barabasi_albert(N, m)
            if random_attack:
                sizes_per_p.append(get_rescaled_gcc_size_after_random_attack(g, p, type))
            else:
                sizes_per_p.append(get_rescaled_gcc_size_after_intentional_attack(g, p))
        mean_sizes.append(np.mean(sizes_per_p))
        std_sizes.append(np.std(sizes_per_p))
    return mean_sizes, std_sizes


def simulate_attack_hrg(dendrogram_path: str, ps, random_attack=True, type='node', ntimes=1):
    mean_sizes = []
    std_sizes = []
    dendrogram = load_dendrogram(dendrogram_path)
    for p in tqdm(ps):
        sizes_per_p = []
        for _ in range(ntimes):
            g = generate_hrg(dendrogram)
            if random_attack:
                sizes_per_p.append(get_rescaled_gcc_size_after_random_attack(g, p, type))
            else:
                sizes_per_p.append(get_rescaled_gcc_size_after_intentional_attack(g, p))
        mean_sizes.append(np.mean(sizes_per_p))
        std_sizes.append(np.std(sizes_per_p))
    return mean_sizes, std_sizes


def get_rescaled_gcc_size_after_random_attack(g, p, type='node'):
    if type == 'node':
        return get_rescaled_gcc_size_after_random_attack_node(g, p)
    elif type == 'edge':
        return get_rescaled_gcc_size_after_random_attack_edge(g, p)


def get_rescaled_gcc_size_after_random_attack_node(g, p):
    all_vertices = get_vertices(g)
    vertices = np.random.choice(all_vertices, int(g.num_vertices() * p), replace=False)
    # [g.clear_vertex(v) for v in vertices]
    g.remove_vertex(vertices)
    return size_gcc(g) / len(all_vertices)


def get_rescaled_gcc_size_after_random_attack_edge(g, p):
    all_edges = get_edges(g)
    edges = np.random.choice(all_edges, int(len(all_edges) * p), replace=False)
    # set_fast_edge_removal()
    [g.remove_edge(e) for e in edges]
    # g.remove_edge(edges)
    N = g.num_vertices() if g.num_vertices() != 0 else 1
    return size_gcc(g) / N


def get_rescaled_gcc_size_after_intentional_attack(g, p):
    all_vertices = get_vertices(g)
    vertices = get_vertices_highest_degree(g, p)
    g.remove_vertex(vertices)
    return size_gcc(g) / len(all_vertices)


def get_vertices_highest_degree(g, p):
    deg_vert = []
    for d, v in zip(g.degree_property_map("total").a, g.get_vertices()):
        deg_vert.append((d, v))
    return sorted(deg_vert, key=lambda x: x[0], reverse=True)[:int((g.num_vertices() * p))]


def save_output(mean_sizes, std_sizes, path: str):
    df = pd.DataFrame(data=zip(mean_sizes, std_sizes))
    df.columns = ['mean', 'std']
    df.to_csv(path, index=False)
