from graph_tool.all import *


def size_gcc(g):
    if g.num_vertices() > 0:
        u = extract_largest_component(g)
        return u.num_vertices()
    else:
        return 0