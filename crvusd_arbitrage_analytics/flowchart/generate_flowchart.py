import pygraphviz as pgv
from flowchart.node import (
    generate_flow_cell,
    modify_edge,
    modify_special_nodes,
    process_sub_graphs,
    remove_duplicate_nodes,
)


def generate_flowchart(token_flow_list):
    
    G = pgv.AGraph(
        name="root",
        label="LLAMMA soft liquidation flow chart",
        directed=True,
        # layout="dot",
        # cluster=True,
        rankdir="TB",
        # newrank=True,
        compound=True,
    )

    # default settings
    G.node_attr["fixedsize"] = False
    G.node_attr["fontsize"] = 24
    G.node_attr["height"] = 1
    G.node_attr["shape"] = "box"
    G.node_attr["style"] = "filled,setlinewidth(3)"
    G.node_attr["width"] = 2.2

    G.edge_attr["arrowsize"] = 0.5
    G.edge_attr["labelfontname"] = "Ubuntu"
    G.edge_attr["weight"] = 10
    G.edge_attr["style"] = "filled,setlinewidth(3)"

    cells, sub_graphs_data = generate_flow_cell(token_flow_list)

    for i in range(len(cells)):
        cell = cells[i]
        G.add_node(cell["n"], label=cell["n_label"])

        if i > 0:
            prev_cell = cells[i - 1]
            l = cell["prev_edge_label"]
            if l == "":
                l = prev_cell["next_edge_label"]
            if not G.has_edge(prev_cell["n"], cell["n"]):
                G.add_edge(prev_cell["n"], cell["n"], label=l)

    process_sub_graphs(G, "", sub_graphs_data)

    remove_duplicate_nodes(G, token_flow_list)

    modify_special_nodes(G, token_flow_list)

    modify_edge(G, token_flow_list)

    G.layout()
    return G
