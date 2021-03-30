from graph_tool.all import *

def size_gcc(g):
    u = extract_largest_component(g)
    return u.num_vertices()