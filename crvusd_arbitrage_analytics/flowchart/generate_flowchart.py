import pygraphviz as pgv
from config.diagram_config import DIAGRAM_COLORS, DIAGRAM_LINE_COLOR
from flowchart.node import (
    generate_flow_cell,
    modify_edge,
    modify_special_nodes,
    process_shape,
    process_subgraphs,
    remove_duplicate_nodes,
)


def generate_flowchart(token_flow_list):
    
    G = pgv.AGraph(
        name="root",
        label="LLAMMA soft liquidation flow chart\n\n",
        directed="true",
        # layout="dot",
        cluster="true",
        rankdir="TB",
        compound="true",
        fontsize="44",
        labelloc="t",
        bgcolor="#212946",
        fontcolor="white",
        pad=2,
    )

    # default settings
    G.node_attr["fixedsize"] = False
    G.node_attr["fontsize"] = 38
    G.node_attr["fontcolor"] = "white"
    G.node_attr["height"] = 1
    G.node_attr["margin"] = 0.4
    G.node_attr["shape"] = "ellipse"
    G.node_attr["style"] = "filled,setlinewidth(4)"
    G.node_attr["width"] = 2
    G.node_attr["color"] = DIAGRAM_LINE_COLOR
    G.node_attr["fillcolor"] = "transparent"

    G.edge_attr["color"] = DIAGRAM_COLORS[4]
    G.edge_attr["arrowsize"] = 0.5
    G.edge_attr["style"] = "filled,setlinewidth(4)"
    G.edge_attr["penwidth"] = 8
    G.edge_attr["minlen"] = 3
    G.edge_attr["fontsize"] = 38
    G.edge_attr["fontcolor"] = DIAGRAM_LINE_COLOR

    cells, sub_graphs_data = generate_flow_cell(token_flow_list)

    for i in range(len(cells)):
        cell = cells[i]
        G.add_node(cell["n"], label=cell["n_label"])

        if i > 0:
            prev_cell = cells[i - 1]
            l = prev_cell["next_edge_label"]
            if l == "":
                l = cell["prev_edge_label"]
            if not G.has_edge(prev_cell["n"], cell["n"]):
                G.add_edge(prev_cell["n"], cell["n"], label=l)


    process_subgraphs(G, "", sub_graphs_data)

    remove_duplicate_nodes(G, sub_graphs_data, token_flow_list)

    modify_special_nodes(G, token_flow_list)

    modify_edge(G, token_flow_list)

    process_shape(G, token_flow_list)

    G.layout()
    return G
