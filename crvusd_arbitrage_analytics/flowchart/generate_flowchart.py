import token
import pygraphviz as pgv
from flowchart.edge import generate_edge_label
from flowchart.node import (
    generate_flow_cell,
    process_sub_graphs,
    remove_duplicate_nodes,
    remove_useless_subgraph,
)


def generate_flowchart(token_flow_list):
    G = pgv.AGraph(
        name="root",
        label="LLAMMA soft liquidation flow chart",
        directed=True,
        layout="dot",
        cluster=True,
        rankdir="TB",
        newrank=True,
    )

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
    # remove_useless_subgraph(G, token_flow_list)

    # print("")
    # print("nodes")
    # print(G.nodes())
    # print("edges")
    # print(G.edges())
    # print("subgraphs")
    # print(G)

    G.layout()
    return G
