import token
import pygraphviz as pgv
from flowchart.edge import generate_edge_label
from flowchart.node import generate_flow_cell, is_transfers_can_merge


def generate_flowchart(token_flow_list):
    G = pgv.AGraph(directed=True, strict=True, layout="dot")

    # merge token_flow_list
    merged_transfer_list = []
    for i in range(len(token_flow_list)):
        row = token_flow_list[i]

        if i > 0:
            prev_row = token_flow_list[i - 1]
            if is_transfers_can_merge(prev_row, row):
                merged_transfer_list[-1].append(row)
                continue

        merged_transfer_list.append([row])

    print("\nmerged_transfer_list")
    for merged in merged_transfer_list:
        print([item["transferStep"] for item in merged])
        
    cells = []
    for i in range(len(merged_transfer_list)):
        cells += generate_flow_cell(merged_transfer_list[i])

    nodes = []
    node_labels = []
    edges = []
    for i in range(len(cells)):
        cell = cells[i]
        nodes.append(cell["n"])
        node_labels.append(cell["n_label"])

        if i > 0:
            prev_cell = cells[i-1]
            l = cell["prev_edge_label"]
            if l == "":
                l = prev_cell["next_edge_label"]
            if (prev_cell["n"], cell["n"], l) not in edges:
                edges.append((prev_cell["n"], cell["n"], l))

    print("cells")
    for cell in cells:
        print(cell)

    nodes_to_del = []
    for i in range(len(nodes)):
        if i not in nodes_to_del:
            G.add_node(nodes[i], label=node_labels[i])

    nodes_to_del = [nodes[i] for i in nodes_to_del]
    for f, t, label in edges:
        if f not in nodes_to_del and t not in nodes_to_del:
            G.add_edge(f, t, label=label)

    print("")
    print("nodes")
    print(G.nodes())
    print("edges")
    print(G.edges())

    G.layout()
    return G
