import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import numpy as np


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


def plot_dendrogram(g, ax=None, node_border_color='black', node_border_width=1):
    pos = graphviz_layout(g, prog='dot')
    nodes_labels = {k: k for k in list(g.nodes())}
    nx.draw_networkx_labels(g, pos=pos, ax=ax, labels=nodes_labels, font_weight='bold', font_size=20,
                            font_color='white')
    nx.draw(g, pos, with_labels=False, arrows=True, node_size=1000, ax=ax,
            edgecolors=node_border_color, linewidths=node_border_width)


def generate_hrg(dendrogram: nx.Graph):
    initial_community = {}

    start_idx = 0
    for node, size in nx.get_node_attributes(dendrogram, 'size').items():
        er = nx.fast_gnp_random_graph(size, p=dendrogram.nodes[node]['prob'])
        mapping = dict(zip(er, range(start_idx, start_idx + size)))
        er = nx.relabel_nodes(er, mapping)
        initial_community[node] = er
        start_idx += size

    visited = set()
    while True:
        next_communities = combine_communities(initial_community, dendrogram, visited)

        if len(next_communities) == 1:
            return list(next_communities.values())[0]
        initial_community = next_communities


def combine_communities(communities: dict, dendrogram: nx.Graph, visited):
    next_communities = {}
    for node1, c1 in communities.items():
        for node2, c2 in communities.items():
            if node1 != node2 and node1 not in visited and node2 not in visited:
                n1 = list(set(list(dendrogram.neighbors(node1))) - visited)
                n2 = list(set(list(dendrogram.neighbors(node2))) - visited)
                if n1 == n2:
                    # combine communities
                    g = connect_communities(dendrogram, n1[0], c1, c2)
                    next_communities[n1[0]] = g
                    visited.add(node1)
                    visited.add(node2)
                else:
                    continue

    return next_communities


def connect_communities(dendrogram: nx.Graph, node, c1, c2) -> nx.Graph:
    p = dendrogram.nodes[node]['prob']
    g = nx.compose(c1, c2)

    # TODO: check if this is correct !
    N1 = nx.number_of_nodes(c1)
    N2 = nx.number_of_nodes(c2)
    c1_subset = np.random.choice(c1.nodes, size=int(p * N1), replace=True)
    c2_subset = np.random.choice(c2.nodes, size=int(p * N2), replace=True)

    g.add_edges_from(zip(c1_subset, c2_subset))
    return g
