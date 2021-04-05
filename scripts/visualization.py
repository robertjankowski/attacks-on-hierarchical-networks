import matplotlib.pyplot as plt
import networkx as nx


def load_matplotlib():
    plt.rc('figure', figsize=(8, 6))
    plt.rcParams['font.size'] = 17
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Coolvetica'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'


def add_legend(loc='best', ncol=1, frameon=False, fontsize=14, labelspacing=0.02):
    plt.legend(fontsize=fontsize, loc=loc, handlelength=1, frameon=frameon,
               borderpad=0.1, ncol=ncol, labelspacing=labelspacing, fancybox=False,
               columnspacing=0.3)


def save_figure(filename: str):
    """
    Save matplotlib figure in correct extension
    :param filename: Name of output plot
    """
    extension = filename.split('.')[-1]
    if extension == "png":
        plt.savefig(filename, bbox_inches='tight', dpi=300)
    elif extension == "pdf" or extension == "svg":
        plt.savefig(filename, bbox_inches='tight')
    else:
        print('Error. Cannot save figure, unsupported extension: [{}]'.format(extension))


def draw_network(g: nx.Graph, ax=None, pos=None, node_size_list=None, node_size_scale=10,
                 edge_alpha=0.1, node_border_color='black', node_border_width=0.5):
    """
    Draw nx.Graph on matplotlib axis
    :param g: nx.Graph
    :param ax: matplotlib canvas
    :param pos: position of nodes (e.g. from nx.spring_layout(g))
    :param node_size_list: list of node sizes
    :param edge_alpha: float
    :param node_border_color: float
    :param node_border_width: float
    """
    if pos is None:
        pos = nx.spring_layout(g)
    if node_size_list is None:
        node_size_list = degree_node_size(g, node_size_scale)
    nx.draw_networkx_edges(g, ax=ax, alpha=edge_alpha, pos=pos, connectionstyle='arc3, rad = 0.1')
    nx.draw_networkx_nodes(g, node_size=node_size_list, ax=ax, pos=pos,
                           edgecolors=node_border_color, linewidths=node_border_width)


def degree_node_size(g: nx.Graph, scale=10):
    return [scale * v for v in dict(g.degree).values()]
