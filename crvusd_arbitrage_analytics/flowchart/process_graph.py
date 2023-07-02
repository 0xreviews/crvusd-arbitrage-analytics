from config.diagram_config import (
    DIAGRAM_COINS,
    DIAGRAM_LAYOUT_NAME,
    DIAGRAM_LINE_COLOR,
    DIAGRAM_NODE_CONFIG,
    DIAGRAM_SUBGRAPH_CONFIG,
    DIAGRAM_SUBGRAPH_SWAP,
    DIAGRAM_SUBGRAPH_WRAPPED_ETH,
)
from config.tokenflow_category import (
    ACTION_GROUP_SWAP_TYPE,
    CALL_ARBI_CONTRACT_FLOW,
    CURVE_ROUTER_FLOW,
    FLASH_POOL_TYPE,
    SWAPPOOL_TYPE,
)
from utils.match import is_curve_swap, is_llamma_swap, is_uniswap_swap


def generate_flow_cell(token_flow_list):
    cells = []
    sub_graphs = {
        DIAGRAM_LAYOUT_NAME[0]: {"children": []},
        DIAGRAM_LAYOUT_NAME[1]: {"children": []},
        DIAGRAM_LAYOUT_NAME[2]: {"children": []},
    }
    tmp_action_group = ""
    for i in range(len(token_flow_list)):
        row = token_flow_list[i]

        if row["from"] == "tx_miner" or row["to"] == "tx_miner":
            continue

        _cells = []
        if row["action_group"] == "":
            if row["from"] not in ["tx_from", "arbitrage_contract"]:
                _cells += [
                    {
                        "n": "%s_%s" % (i, row["from"]),
                        "n_label": row["from"],
                        "prev_edge_label": "",
                        "next_edge_label": row["token_symbol"],
                    }
                ]
            if row["to"] not in ["tx_from", "arbitrage_contract"]:
                _cells += [
                    {
                        "n": "%s_%s" % (i, row["to"]),
                        "n_label": row["to"],
                        "prev_edge_label": row["token_symbol"],
                        "next_edge_label": row["token_symbol"] if i == 0 else "",
                    },
                ]
        else:
            if tmp_action_group == row["action_group"]:
                cells[-1]["next_edge_label"] = row["token_symbol"]
                continue

            # if i == 0 and row["from"] in ["tx_from", "arbitrage_contract"]:
            #     _cells += [
            #         {
            #             "n": "%s_%s" % (i, row["from"]),
            #             "n_label": row["from"],
            #             "next_edge_label": row["token_symbol"],
            #         }
            #     ]

            label = row["action_group"].split(",")
            label = label[-1]
            label = label.split(":")

            if len(label) > 1:
                label.pop()
                label = ":".join(label)
            else:
                label = label[0]

            if label in ACTION_GROUP_SWAP_TYPE:
                label = row["swap_pool"].split(",")[-1]

            _cells += [
                {
                    "n": "%s_%s" % (i, row["action_group"]),
                    "n_label": label,
                    "prev_edge_label": row["token_symbol"] if i > 0 else "",
                    "next_edge_label": "" if i > 0 else row["token_symbol"],
                }
            ]

            # flash_repay: pool_B token_out repay to pool_A, then pool_B token_in (swap)
            if i > 0:
                prev_row = token_flow_list[i-1]
                if ":flash_repay" in prev_row["action_group"] and len(prev_row["swap_pool"].split(",")) == 2:
                    _cells += [cells.pop()]


            # if i == len(token_flow_list) - 1 and row["to"] in [
            #     "tx_from",
            #     "arbitrage_contract",
            # ]:
            #     _cells += [
            #         {
            #             "n": "%s_%s" % (i, row["to"]),
            #             "n_label": row["to"],
            #             "prev_edge_label": row["token_symbol"],
            #         }
            #     ]

            tmp_action_group = row["action_group"]

        cells += _cells

        tmp_graphs = sub_graphs[DIAGRAM_LAYOUT_NAME[0]]
        if row["action_type"] in ["LLAMMA:token_in", "LLAMMA:token_out"]:
            tmp_graphs = sub_graphs[DIAGRAM_LAYOUT_NAME[1]]
        elif (
            len(sub_graphs[DIAGRAM_LAYOUT_NAME[1]]["children"])
            + len(sub_graphs[DIAGRAM_LAYOUT_NAME[1]].keys())
            > 1
        ):
            tmp_graphs = sub_graphs[DIAGRAM_LAYOUT_NAME[2]]

        tmp_graphs["children"] += [c["n"] for c in _cells]

    return cells, sub_graphs


def process_subgraphs(G, sub_graphs_data):
    if G is None:
        return

    # init subgraphs
    for i in range(len(DIAGRAM_LAYOUT_NAME)):
        sg_name = DIAGRAM_LAYOUT_NAME[i]
        is_cluster = "true"
        if i == 1:
            is_cluster = "false"
        G.add_subgraph(
            name=sg_name,
            label=sg_name,
            cluster=is_cluster,
            rank="" if is_cluster == "true" else "same",
            nbunch=sub_graphs_data[sg_name]["children"],
            color=DIAGRAM_LINE_COLOR,
            fontcolor="white",
            fillcolor="transparent",
            margin=24,
            fontsize=32,
            penwidth=2,
        )


def remove_duplicate_nodes(G, sub_graphs_data, token_flow_list):
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

        _g = G
        for sg in G.subgraphs():
            if (
                sg.has_node(prev_node)
                and sg.has_node(node)
                and sg.get_edge(prev_node, node) is not None
            ):
                _g = sg

        _g.remove_edge(prev_node, node)
        _g.add_edge(prev_node, next_node, label=l)

        # cache label if next_node will be delete either
        if next_node in nodes_to_del:
            tmp_l = l
        else:
            tmp_l = ""

    for dn in nodes_to_del:
        G.remove_node(dn)


def modify_special_nodes(G, token_flow_list):
    edge_to_modify = []

    for p in G.subgraphs():
        for n in p.nodes():
            label = n.attr["label"]
            if "frxETH_unstake" in label:
                edge_to_modify.append(
                    {
                        "n": n,
                        "prev_edge": "sfrxeth",
                        "next_edge": "frxeth",
                    }
                )

            elif "frxETH_stake" in label:
                edge_to_modify.append(
                    {
                        "n": n,
                        "prev_edge": "frxeth",
                        "next_edge": "sfrxeth",
                    }
                )
            elif "WETH_withdraw" in label:
                edge_to_modify.append(
                    {
                        "n": n,
                        "prev_edge": "weth",
                        "next_edge": "eth",
                    }
                )
            elif "WETH_deposit" in label:
                edge_to_modify.append(
                    {
                        "n": n,
                        "prev_edge": "eth",
                        "next_edge": "weth",
                    }
                )

    for em in edge_to_modify:
        n = em["n"]
        node = G.get_node(n)
        if len(G.predecessors(node)) > 0:
            prev_node = G.predecessors(node)[-1]
            if "prev_edge" in em:
                G.get_edge(prev_node, node).attr["label"] = em["prev_edge"]

        if len(G.out_neighbors(node)) > 0:
            next_node = G.out_neighbors(node)[0]
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

    # add llamma left arrow and right arrow
    llamma_subgraph = G.get_subgraph(DIAGRAM_LAYOUT_NAME[1])
    llamma_subgraph.add_node(
        "llamma_left_arrow",
        fixedsize="true",
        height=0,
        shape="point",
        style="invis",
    )
    llamma_subgraph.add_node(
        "llamma_right_arrow",
        fixedsize="true",
        height=0,
        shape="point",
        style="invis",
    )

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

        if (
            node0_subgraph == DIAGRAM_LAYOUT_NAME[0]
            and node1_subgraph == DIAGRAM_LAYOUT_NAME[1]
        ):
            llamma_subgraph.add_edge(
                "llamma_left_arrow",
                e[1],
                label=e.attr["label"],
            )
            G.remove_edge(e)
        elif (
            node0_subgraph == DIAGRAM_LAYOUT_NAME[1]
            and node1_subgraph == DIAGRAM_LAYOUT_NAME[2]
        ):
            llamma_subgraph.add_edge(
                e[0],
                "llamma_right_arrow",
                label=e.attr["label"],
            )
            G.remove_edge(e)


def process_shape(G, token_flow_list):
    nodes = G.nodes()

    for n in nodes:
        _process_node_attr(G, n)

    # subgraphs = G.subgraphs()

    # for s in subgraphs:
    #     _process_subgraph_attr(G, s)

    #     for cs in s.subgraphs():
    #         _process_subgraph_attr(G, cs)


def _process_node_attr(G, n):
    label = n.attr["label"]

    if label in DIAGRAM_COINS:
        label = "coin"
    elif is_llamma_swap(label):
        label = "LLAMMA"
    elif is_curve_swap(label):
        if "-crvUSD" in label:
            label = "CurveStable_crvUSD"
        else:
            label = "CurveSwapPool"
    elif is_uniswap_swap(label):
        label = "UniswapPool"
    elif label.split("_")[0] in DIAGRAM_SUBGRAPH_WRAPPED_ETH:
        label = "wrapped_eth"

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
