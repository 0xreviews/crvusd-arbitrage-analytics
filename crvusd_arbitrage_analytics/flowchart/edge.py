import pygraphviz as pgv
from config.tokenflow_category import FRXETH_FLOW

from utils import is_curve_router, is_swap_pool


def get_or_add_edge_in_graph(G, f, t, label=""):
    if not G.has_edge(f, t):
        G.add_edge(f, t, label)
    return G.get_edge(f, t)


def generate_edge_label(actions):
    string = ""
    s0 = ""
    s1 = ""
    for i in range(len(actions)):
        a = actions[i]
        ll = actions[i].split(":")
        if a in FRXETH_FLOW:
            s0 = ll[0]

    if s0 != "":
        string = "%s %s" % (s0, s1)

    return string
