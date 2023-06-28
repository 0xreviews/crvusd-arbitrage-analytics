import re
from config.diagram_config import (
    DIAGRAM_COINS,
    DIAGRAM_LINE_COLOR,
    DIAGRAM_NODE_CONFIG,
    DIAGRAM_SUBGRAPH_CONFIG,
    DIAGRAM_SUBGRAPH_SWAP,
    DIAGRAM_SUBGRAPH_WRAPPED_ETH,
)
from config.tokenflow_category import (
    CALL_ARBI_CONTRACT_FLOW,
    CURVE_META_SWAP_FLOW,
    CURVE_ROUTER_FLOW,
)
from utils.match import is_curve_router, is_curve_swap, is_llamma_swap, is_uniswap_swap


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
    sub_graphs = {
        "left": {"children": []},
        "mid": {"children": []},
        "right": {"children": []},
    }
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
        tmp_graphs = sub_graphs["left"]
        if row["action_type"] in ["LLAMMA:token_in", "LLAMMA:token_out"]:
            tmp_graphs = sub_graphs["mid"]
        elif len(sub_graphs["mid"]["children"]) + len(sub_graphs["mid"].keys()) > 1:
            tmp_graphs = sub_graphs["right"]

        if row["action_group"] == "":
            tmp_graphs["children"].append("%s_%s" % (i, row["from"]))
            tmp_graphs["children"].append("%s_%s" % (i, row["to"]))
        else:
            for gn in row["action_group"].split(","):
                if gn == "" or "CurveRouter:" in gn or "_transfer:" in gn:
                    continue

                if gn not in tmp_graphs:
                    tmp_graphs[gn] = {"children": []}
                tmp_graphs[gn]["children"].append("%s_%s" % (i, row["from"]))
                tmp_graphs[gn]["children"].append("%s_%s" % (i, row["to"]))
                tmp_graphs = tmp_graphs[gn]

    for c in sub_graphs:
        print(c)
        print(sub_graphs[c])
    return cells, sub_graphs


def process_subgraphs(G, sub_name, sub_graphs_data):
    if G is None:
        return

    if sub_name == "":
        _g = G
    else:
        _g = G.get_subgraph(sub_name)
        if _g is None:
            is_cluster = "true"
            label = sub_name.split(":")[0]
            if label == "LLAMMA":
                is_cluster = "false"
            _g = G.add_subgraph(
                name=sub_name,
                label=sub_name.split(":")[0],
                cluster=is_cluster,
                rankdir="TB",
                rank="same",
                newrank=True,
                color=DIAGRAM_LINE_COLOR,
                fontcolor="white",
                fillcolor="transparent",
                margin=16,
                fontsize=28,
                penwidth=4,
            )

        for _c in sub_graphs_data["children"]:
            _g.add_node(_c)

    for gn, value in sub_graphs_data.items():
        if gn != "children":
            process_subgraphs(_g, gn, value)


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

    # if it has only one node, remove subgraph
    for s in G.subgraphs():
        nodes = s.nodes()
        if len(nodes) == 1 and s.node_attr["label"] in ["CurveSwap", "UniswapSwap"]:
            G.remove_subgraph(s.get_name())


def modify_special_nodes(G, token_flow_list):
    nodes = G.nodes()
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
        elif "WETH_withdraw:" in gn:
            edge_to_modify.append(
                {
                    "n": sg_nodes[0],
                    "prev_edge": "weth",
                }
            )
            edge_to_modify.append(
                {
                    "n": sg_nodes[-1],
                    "next_edge": "eth",
                }
            )
        elif "WETH_deposit:" in gn:
            edge_to_modify.append(
                {
                    "n": sg_nodes[0],
                    "prev_edge": "eth",
                }
            )
            edge_to_modify.append(
                {
                    "n": sg_nodes[-1],
                    "next_edge": "weth",
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


def modify_edge(G, token_flow_list):
    subgraphs = G.subgraphs()
    edges = G.edges()

    nodes_subgraphs = {}
    for s in subgraphs:
        s_nodes = s.nodes()
        for cs in s.subgraphs():
            cs_nodes = cs.nodes()
            tmp_s_nodes = []
            for i in range(len(s_nodes)):
                tmp_s_node = s_nodes.pop()
                for j in range(len(cs_nodes)):
                    if cs_nodes[j] != tmp_s_node:
                        tmp_s_nodes.append(tmp_s_node)
            s_nodes = tmp_s_nodes
            nodes_subgraphs[cs.get_name()] = cs_nodes

        nodes_subgraphs[s.get_name()] = s_nodes

    for e in edges:
        node0_subgraph = ""
        node1_subgraph = ""

        # margin edge label
        e.attr["label"] = "  " + e.attr["label"] + "  "

        for s in nodes_subgraphs:
            if e[0] in nodes_subgraphs[s]:
                node0_subgraph = s
                break
        for s in nodes_subgraphs:
            if e[1] in nodes_subgraphs[s]:
                node1_subgraph = s
                break

        if node0_subgraph != node1_subgraph:
            if node0_subgraph != "":
                e.attr["ltail"] = node0_subgraph
            if node1_subgraph != "":
                e.attr["lhead"] = node1_subgraph


def process_shape(G, token_flow_list):
    nodes = G.nodes()

    for n in nodes:
        _process_node_attr(G, n)

    subgraphs = G.subgraphs()

    for s in subgraphs:
        _process_subgraph_attr(G, s)

        for cs in s.subgraphs():
            _process_subgraph_attr(G, cs)


def _process_node_attr(G, n):
    label = n.attr["label"]

    if label in DIAGRAM_COINS:
        label = "coin"
    elif is_llamma_swap(label):
        label = "LLAMMA"
    elif is_curve_swap(label):
        label = "CurveSwapPool"
    elif is_uniswap_swap(label):
        label = "UniswapPool"

    if label in DIAGRAM_NODE_CONFIG:
        cf = DIAGRAM_NODE_CONFIG[label]
        for k, v in cf.items():
            n.attr[k] = v


def _process_subgraph_attr(G, s):
    label = s.graph_attr["label"]
    if label.split("_")[0] in DIAGRAM_SUBGRAPH_WRAPPED_ETH:
        label = "wrapped_eth"
    if label in DIAGRAM_SUBGRAPH_SWAP:
        label = "swap"

    if label in DIAGRAM_SUBGRAPH_CONFIG:
        cf = DIAGRAM_SUBGRAPH_CONFIG[label]
        # cluster style "filled" "striped" "rounded"
        for k, v in cf.items():
            s.graph_attr[k] = v
