import re
from config.tokenflow_category import (
    CALL_ARBI_CONTRACT_FLOW,
    CURVE_META_SWAP_FLOW,
    CURVE_ROUTER_FLOW,
)
from utils import is_curve_router, is_llamma_swap


def is_transfers_can_merge(prev_transfer, next_transfer):
    # from to are same
    if (
        prev_transfer["swap_pool"] == next_transfer["swap_pool"]
        and prev_transfer["from"] == next_transfer["to"]
        and prev_transfer["to"] == next_transfer["from"]
    ):
        return True
    # Curve Meta LP mint/burn
    if (
        # 3crv LP mint
        prev_transfer["action_type"] + next_transfer["action_type"]
        == CURVE_META_SWAP_FLOW[0] + CURVE_META_SWAP_FLOW[4]
        # 3crv LP burn
        or prev_transfer["action_type"] + next_transfer["action_type"]
        == CURVE_META_SWAP_FLOW[1] + CURVE_META_SWAP_FLOW[5]
    ):
        return True
    return False


def get_or_add_node_in_graph(G, string, label=""):
    if not G.has_node(string):
        G.add_node(string, label=label)
    return G.get_node(string)


def is_router_mid_node(action_group):
    return re.compile("CurveRouter:[0-9]+:doing").match(action_group) != None


def get_swap_pool_exclude_router(swap_pools):
    pool = ""
    for _p in swap_pools:
        if not is_curve_router(_p):
            pool = _p
            break
    return pool


def generate_flow_cell(token_flow_list):
    cells = []
    sub_graphs = {}
    for i in range(len(token_flow_list)):
        row = token_flow_list[i]
        cells += [
            {
                "n": "%s_%s" % (i, row["from"]),
                "n_label": row["from"],
                "prev_edge_label": "",
                "next_edge_label": row["token_symbol"],
            },
            {
                "n": "%s_%s" % (i, row["to"]),
                "n_label": row["to"],
                "prev_edge_label": row["token_symbol"],
                "next_edge_label": row["token_symbol"] if i == 0 else "",
            },
        ]
        tmp_graphs = sub_graphs
        for gn in row["action_group"].split(","):
            if gn == "" or "CurveRouter:" in gn or "_transfer:" in gn:
                continue

            if gn not in tmp_graphs:
                tmp_graphs[gn] = {"children": []}
            tmp_graphs[gn]["children"].append("%s_%s" % (i, row["from"]))
            tmp_graphs[gn]["children"].append("%s_%s" % (i, row["to"]))
            tmp_graphs = tmp_graphs[gn]

    return cells, sub_graphs


def process_sub_graphs(G, sub_name, sub_graphs_data):
    if G is None:
        return

    if sub_name == "":
        _g = G
    else:
        _g = G.get_subgraph(sub_name)
        if _g is None:
            _g = G.add_subgraph(
                name=sub_name,
                label=sub_name.split(":")[0],
                cluster=True,
                rankdir="LT",
                newrank=True,
                fillcolor="darkgray",
                style="filled",
            )

        for _c in sub_graphs_data["children"]:
            _g.add_node(_c)

    for gn, value in sub_graphs_data.items():
        if gn != "children":
            process_sub_graphs(_g, gn, value)


def remove_duplicate_nodes(G, token_flow_list):
    nodes = G.nodes()
    length = len(nodes)
    nodes_to_del = []
    edges_to_del = []
    for i in range(length):
        node = nodes[i]

        if i > 0 and i < length - 2:
            prev_i = i - 1
            prev_node = nodes[prev_i]
            while prev_node in nodes_to_del:
                prev_i -= 1
                prev_node = nodes[prev_i]
                if prev_i == -1:
                    break

            next_node = nodes[i + 1]

            step = int(node.split("_")[0])
            label = node.attr["label"]

            row = token_flow_list[step]
            remove_flag = False

            if label == "CurveSwapRouter":
                if (
                    row["action_type"] == CURVE_ROUTER_FLOW[0]
                    or row["action_type"] == CURVE_ROUTER_FLOW[1]
                ):
                    remove_flag = False
                else:
                    remove_flag = True
            if label == "arbitrage_contract":
                if row["action_type"] in CALL_ARBI_CONTRACT_FLOW:
                    remove_flag = False
                else:
                    remove_flag = True
            elif prev_node.attr["label"] == label:
                remove_flag = True

            if remove_flag:
                nodes_to_del.append(node)
                prev_l = (
                    G.get_edge(prev_node, node).attr["label"]
                    if G.has_edge(prev_node, node)
                    else ""
                )
                next_l = (
                    G.get_edge(node, next_node).attr["label"]
                    if G.has_edge(node, next_node)
                    else ""
                )
                edges_to_del.append((prev_node, node, next_node, prev_l, next_l))
            else:
                edges_to_del.append(("", "", "", "", ""))

    tmp_l = ""
    for i in range(len(edges_to_del)):
        (prev_node, node, next_node, prev_l, next_l) = edges_to_del[i]

        l = ""
        for string in [tmp_l, prev_l, next_l]:
            if string == l:
                continue
            l += "," + string if l != "" and string != "" else string
        if node == "":
            continue

        G.remove_edge(prev_node, node)
        G.add_edge(prev_node, next_node, label=tmp_l)

        # cache label if next_node will be delete either
        if next_node in nodes_to_del:
            tmp_l = l
        else:
            tmp_l = ""

    for dn in nodes_to_del:
        G.remove_node(dn)


def modify_special_nodes(G, token_flow_list):
    nodes = G.nodes()
    length = len(nodes)
    subgraghs = G.subgraphs()

    edge_to_modify = []

    for sg in subgraghs:
        gn = sg.get_name()
        sg_nodes = sg.nodes()
        if "frxETH_unstake:" in gn:
            edge_to_modify.append(
                {
                    "n": sg_nodes[0],
                    "prev_edge": "sfrxeth",
                }
            )
            edge_to_modify.append(
                {
                    "n": sg_nodes[-1],
                    "next_edge": "frxeth",
                }
            )
        elif "frxETH_stake:" in gn:
            edge_to_modify.append(
                {
                    "n": sg_nodes[0],
                    "prev_edge": "frxeth",
                }
            )
            edge_to_modify.append(
                {
                    "n": sg_nodes[-1],
                    "next_edge": "sfrxeth",
                }
            )

    for em in edge_to_modify:
        n = em["n"]
        node = G.get_node(n)
        prev_node = G.predecessors(node)[-1]
        next_node = G.out_neighbors(node)[0]

        if "prev_edge" in em:
            G.get_edge(prev_node, node).attr["label"] = em["prev_edge"]
        if "next_edge" in em:
            G.get_edge(node, next_node).attr["label"] = em["next_edge"]
