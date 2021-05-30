import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import numpy as np
import sys

sys.path.append('..')
from scripts.convert_graphs import nx2gt


def load_dendrogram(path: str) -> nx.Graph:
    """
    Load dendrogram from a give file. The file should follow this structure:

    # Tree structure #
    0 A
    O B
    ... (edgelist)
    # Probabilities #
    O 0.3
    A 0.32
    ... (internal probabilities)
    # Sizes #
    C 400
    D 560
    ... (number of nodes in _i_ community)

    """
    with open(path, 'r') as f:
        f.readline()
        dendrogram = nx.Graph()
        # Edgelist
        for line in f:
            if '#' in line:
                break
            source, target = line.strip().split(' ')
            dendrogram.add_edge(source, target)
        # Probabilities
        for line in f:
            if '#' in line:
                break
            node, prob = line.strip().split(' ')
            dendrogram.nodes[node]['prob'] = float(prob)
        # Sizes
        for line in f:
            node, size = line.strip().split(' ')
            dendrogram.nodes[node]['size'] = int(size)
        return dendrogram


def total_size(dendrogram: nx.Graph) -> int:
    return sum(nx.get_node_attributes(dendrogram, 'size').values())


def avg_degree(dendrogram: nx.Graph) -> float:
    """
    Calculate average degree of a generated network given a dendrogram structure

    :param dendrogram:
    :return: <k>
    """

    def calc_E(p, N):
        return p * N * (N - 1) / 2

    d_g = dendrogram.copy()
    total_E = 0
    sizes = total_size(dendrogram)

    for node in d_g.nodes():
        n = d_g.nodes[node]
        if 'prob' in n and 'size' in n:
            total_E += calc_E(n['prob'], n['size'])

    while True:
        for node in sorted(d_g.nodes()):
            n = d_g.nodes[node]
            if 'size' not in n:
                neighbors = list(d_g.neighbors(node))
                s = []
                for nn_node in neighbors:
                    nn = d_g.nodes[nn_node]
                    if 'size' in nn:
                        s.append(nn['size'])
                if len(s) > 1:
                    d_g.nodes[node]['size'] = sum(s)
                    total_E += n['prob'] * min(s)
        if len(nx.get_node_attributes(d_g, 'size')) == nx.number_of_nodes(d_g):
            break

    return 2 * total_E / sizes


def plot_dendrogram(g, ax=None, node_border_color='black', node_border_width=1):
    pos = graphviz_layout(g, prog='dot')
    nodes_labels = {k: k for k in list(g.nodes())}
    nx.draw_networkx_labels(g, pos=pos, ax=ax, labels=nodes_labels, font_weight='bold', font_size=20,
                            font_color='white')
    nx.draw(g, pos, with_labels=False, arrows=True, node_size=1000, ax=ax,
            edgecolors=node_border_color, linewidths=node_border_width)


def generate_hrg(dendrogram: nx.Graph, to_gt=True):
    initial_community = {}

    start_idx = 0
    for node, size in nx.get_node_attributes(dendrogram, 'size').items():
        er = nx.fast_gnp_random_graph(size, p=dendrogram.nodes[node]['prob'])
        mapping = dict(zip(er, range(start_idx, start_idx + size)))
        er = nx.relabel_nodes(er, mapping)
        initial_community[node] = er
        start_idx += size

    visited = set()
    edges_between_communities = []
    while True:
        next_communities, new_edges_between_communities = combine_communities(initial_community, dendrogram, visited)

        edges_between_communities.extend(new_edges_between_communities)
        if len(next_communities) == 1:
            g = list(next_communities.values())[0]
            if to_gt:
                return nx2gt(g), edges_between_communities
            else:
                return g, edges_between_communities
        initial_community = next_communities


def combine_communities(communities: dict, dendrogram: nx.Graph, visited):
    next_communities = {}
    edges_between_communities = []
    for node1, c1 in communities.items():
        for node2, c2 in communities.items():
            if node1 != node2 and node1 not in visited and node2 not in visited:
                n1 = list(set(list(dendrogram.neighbors(node1))) - visited)
                n2 = list(set(list(dendrogram.neighbors(node2))) - visited)
                if n1 == n2:
                    # combine communities
                    g, new_edges_between_communities = connect_communities(dendrogram, n1[0], c1, c2)
                    next_communities[n1[0]] = g
                    visited.add(node1)
                    visited.add(node2)
                    edges_between_communities.extend(new_edges_between_communities)
                else:
                    continue

    return next_communities, edges_between_communities


def connect_communities(dendrogram: nx.Graph, node, c1, c2) -> (nx.Graph, list):
    p = dendrogram.nodes[node]['prob']
    g = nx.compose(c1, c2)

    # TODO: check if this is correct !
    N1 = nx.number_of_nodes(c1)
    N2 = nx.number_of_nodes(c2)
    c1_subset = np.random.choice(c1.nodes, size=int(p * N1), replace=True)
    c2_subset = np.random.choice(c2.nodes, size=int(p * N2), replace=True)

    new_edges = list(zip(c1_subset, c2_subset))
    g.add_edges_from(new_edges)
    return g, new_edges
