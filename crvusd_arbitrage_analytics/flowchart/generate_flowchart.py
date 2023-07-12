import subprocess
import pygraphviz as pgv
from config.diagram_config import (
    DIAGRAM_COLORS,
    DIAGRAM_LAYOUT_NAME,
    DIAGRAM_LINE_COLOR,
)
from flowchart.process_graph import (
    generate_flow_cell,
    modify_edge,
    modify_special_nodes,
    process_shape,
    process_subgraphs,
    remove_duplicate_nodes,
)


def generate_flowchart(trade_data, title="soft liquidation flow chart"):
    token_flow_list = trade_data["token_flow_list"]
    G = pgv.AGraph(
        name="root",
        label=title,
        directed="true",
        layout="dot",
        cluster="true",
        rankdir="TB",
        compound="true",
        fontsize="32",
        labelloc="t",
        bgcolor="#212946",
        fontcolor="white",
        pad=1,
    )
    G.layout("dot")

    # default settings
    G.node_attr["fixedsize"] = False
    G.node_attr["fontsize"] = 20
    G.node_attr["fontcolor"] = "white"
    G.node_attr["height"] = 1
    G.node_attr["margin"] = 0.15
    G.node_attr["shape"] = "ellipse"
    G.node_attr["style"] = "filled,setlinewidth(3)"
    G.node_attr["width"] = 1.5
    G.node_attr["pad"] = 10
    G.node_attr["color"] = DIAGRAM_LINE_COLOR
    G.node_attr["penwidth"] = 2
    G.node_attr["fillcolor"] = "transparent"

    G.edge_attr["color"] = DIAGRAM_COLORS[4]
    G.edge_attr["arrowsize"] = 0.5
    G.edge_attr["style"] = "filled,setlinewidth(3)"
    G.edge_attr["penwidth"] = 6
    G.edge_attr["weight"] = 10
    G.edge_attr["minlen"] = 1.5
    G.edge_attr["fontsize"] = 20
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
        

    process_subgraphs(G, sub_graphs_data)

    remove_duplicate_nodes(G, sub_graphs_data, token_flow_list)

    modify_special_nodes(G, token_flow_list)

    modify_edge(G, token_flow_list)

    process_shape(G, token_flow_list)

    # sort subgraphs
    subgraphs = {}
    for sg in G.subgraphs():
        subgraphs[sg.get_name()] = sg.to_string()

    subgraphs_string = "\n".join(
        [
            subgraphs[sg_name].replace("strict digraph", "subgraph")
            for sg_name in DIAGRAM_LAYOUT_NAME
        ]
    )
    for sg in subgraphs.keys():
        n_to_del = G.get_subgraph(sg).nodes()
        for n in n_to_del:
            G.remove_node(n)
        G.remove_subgraph(sg)

    container_g_string = G.to_string()
            
    G_string = container_g_string.replace("}", subgraphs_string + "}")

    return G_string


def draw_graph_from_string(G_string, save_dot_dir, save_png_dir):
    with open(save_dot_dir, "w") as f:
        f.write(G_string)

    subprocess.run(["dot", save_dot_dir, "-Tpng", "-o", save_png_dir])
