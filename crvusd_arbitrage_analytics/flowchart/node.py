import re
import pygraphviz as pgv

from config.tokenflow_category import (
    CALL_ARBI_CONTRACT_FLOW,
    CURVE_META_SWAP_FLOW,
    CURVE_ROUTER_FLOW,
    CURVE_SWAP_WETH_FLOW,
    FRXETH_FLOW,
    LLAMMA_SWAP_FLOW,
    WETH_FLOW,
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
                # "graph_group": row["action_group"].split(","),
            },
            {
                "n": "%s_%s" % (i, row["to"]),
                "n_label": row["to"],
                "prev_edge_label": row["token_symbol"],
                "next_edge_label": "",
                # "graph_group": row["action_group"].split(","),
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

    # # LLAMMA swap
    # elif is_llamma_swap(",".join(swap_pools)):
    #     n_label = get_swap_pool_exclude_router(swap_pools)

    #     edge_label = ""
    #     if ",".join(actions) == ",".join([LLAMMA_SWAP_FLOW[0], LLAMMA_SWAP_FLOW[1]]):
    #         # token out token in
    #         edge_label = "%s out %s in" % (tokens[0], tokens[1])
    #     elif ",".join(actions) == ",".join([LLAMMA_SWAP_FLOW[1], LLAMMA_SWAP_FLOW[0]]):
    #         # token in token out
    #         edge_label = "%s in %s out" % (tokens[0], tokens[1])

    #     cells.append(
    #         {
    #             "n": "%s_%s" % (first_step, n_label),
    #             "n_label": n_label,
    #             "prev_edge_label": edge_label,
    #             "next_edge_label": "",
    #             "graph_group": "LLAMMA soft liquidate",
    #             "children": [],
    #         }
    #     )
    # # CurveRouter
    # elif is_curve_router(",".join(swap_pools)):
    #     # CurveRouter:token_in
    #     if ",".join(actions) == CURVE_ROUTER_FLOW[0]:
    #         cells.append(
    #             {
    #                 "n": "%s_CurveSwapRouter" % (first_step),
    #                 "n_label": "CurveSwapRouter",
    #                 "prev_edge_label": "%s" % (tokens[0]),
    #                 "next_edge_label": "",
    #                 "graph_group": "",
    #                 # "graph_group": "CurveRouter batch swap",
    #                 "children": [],
    #             }
    #         )
    #     # CurveRouter:token_out
    #     elif ",".join(actions) == CURVE_ROUTER_FLOW[1]:
    #         cells.append(
    #             {
    #                 "n": "%s_CurveSwapRouter" % (first_step),
    #                 "n_label": "CurveSwapRouter",
    #                 "prev_edge_label": "%s" % (tokens[0]),
    #                 "next_edge_label": "",
    #                 "graph_group": "",
    #                 # "graph_group": "CurveRouter batch swap",
    #                 "children": [],
    #             }
    #         )
    #     elif is_router_mid_node(",".join(groups)):
    #         n_label = get_swap_pool_exclude_router(swap_pools)

    #         prev_edge_label = ""
    #         next_edge_label = ""
    #         if ",".join(actions) == ",".join(
    #             [CURVE_ROUTER_FLOW[2], CURVE_ROUTER_FLOW[3]]
    #         ):
    #             # token out token in
    #             prev_edge_label = "%s" % (tokens[1])
    #             next_edge_label = "%s" % (tokens[0])
    #         elif ",".join(actions) == ",".join(
    #             [CURVE_ROUTER_FLOW[3], CURVE_ROUTER_FLOW[2]]
    #         ):
    #             # token in token out
    #             prev_edge_label = "%s" % (tokens[0])
    #             next_edge_label = "%s" % (tokens[1])

    #         cells.append(
    #             {
    #                 "n": "%s_%s" % (first_step, n_label),
    #                 "n_label": n_label,
    #                 "prev_edge_label": prev_edge_label,
    #                 "next_edge_label": next_edge_label,
    #                 "graph_group": "",
    #                 # "graph_group": "CurveRouter batch swap",
    #                 "children": [],
    #             }
    #         )
    # # WETH Flow
    # elif re.compile("WETH").match(",".join(groups)):
    #     prev_edge_label = ""
    #     # WETH_deposit
    #     if ",".join(actions) == ",".join([WETH_FLOW[0], WETH_FLOW[1]]):
    #         prev_edge_label = WETH_FLOW[0].split(":")[0]
    #     # WETH_withdraw
    #     if ",".join(actions) == ",".join([WETH_FLOW[3], WETH_FLOW[2]]):
    #         prev_edge_label = WETH_FLOW[0].split(":")[0]

    #     cells.append(
    #         {
    #             "n": "%s_WETH" % (first_step),
    #             "n_label": "WETH",
    #             "prev_edge_label": prev_edge_label,
    #             "next_edge_label": "",
    #             "graph_group": "",
    #             # "graph_group": prev_edge_label,
    #             "children": [],
    #         }
    #     )
    # # frxETH Flow
    # elif re.compile("frxETH").match(",".join(groups)):
    #     prev_edge_label = ""
    #     # frxETH_mint
    #     if ",".join(actions) == ",".join([FRXETH_FLOW[0], FRXETH_FLOW[1]]):
    #         prev_edge_label = FRXETH_FLOW[0].split(":")[0]
    #     # frxETH_stake
    #     elif ",".join(actions) == ",".join([FRXETH_FLOW[2], FRXETH_FLOW[3]]):
    #         prev_edge_label = FRXETH_FLOW[2].split(":")[0]
    #     # frxETH_unstake
    #     elif ",".join(actions) == ",".join([FRXETH_FLOW[5], FRXETH_FLOW[4]]):
    #         prev_edge_label = FRXETH_FLOW[4].split(":")[0]

    #     cells.append(
    #         {
    #             "n": "%s_sFrxETH" % (first_step),
    #             "n_label": "sFrxETH",
    #             "prev_edge_label": prev_edge_label,
    #             "next_edge_label": "",
    #             "graph_group": "",
    #             # "graph_group": prev_edge_label,
    #             "children": [],
    #         }
    #     )
    # # CurveSwap:WETH deposit/withdraw
    # elif re.compile("CurveSwap:WETH").match(",".join(actions)):
    #     prev_edge_label = ""
    #     next_edge_label = ""
    #     n_label = get_swap_pool_exclude_router(swap_pools)
    #     # WETH_deposit
    #     if ",".join(actions) == ",".join(
    #         [CURVE_SWAP_WETH_FLOW[0], CURVE_SWAP_WETH_FLOW[1]]
    #     ):
    #         prev_edge_label = "CurveSwap:WETH_deposit"
    #     # WETH_withdraw
    #     if ",".join(actions) == ",".join(
    #         [CURVE_SWAP_WETH_FLOW[2], CURVE_SWAP_WETH_FLOW[3]]
    #     ):
    #         prev_edge_label = "CurveSwap:WETH_withdraw"

    #     # add cell to a subgraph
    #     if len(cells) > 0:
    #         cells[-1]["children"].append(
    #             {
    #                 "n": "%s_WETH" % (first_step),
    #                 "n_label": "WETH",
    #                 "prev_edge_label": prev_edge_label,
    #                 "next_edge_label": next_edge_label,
    #                 "graph_group": "CurveSwap_WETH",
    #                 "children": [],
    #             }
    #         )
    # # Curve Meta Swap Pool
    # elif re.compile("CurveSwap:MetaPool").match(",".join(actions)):
    #     prev_edge_label = ""
    #     next_edge_label = ""
    #     n_label = "Curve3Pool-DAI-USDC-USDT"
    #     # token in + LP mint
    #     if ",".join(actions) == ",".join(
    #         [CURVE_META_SWAP_FLOW[0], CURVE_META_SWAP_FLOW[4]]
    #     ):
    #         prev_edge_label = "%s" % (CURVE_META_SWAP_FLOW[0].split(":")[1])
    #         next_edge_label = "%s" % (CURVE_META_SWAP_FLOW[4].split(":")[1])
    #     # token out + LP burn
    #     if ",".join(actions) == ",".join(
    #         [CURVE_META_SWAP_FLOW[1], CURVE_META_SWAP_FLOW[5]]
    #     ):
    #         prev_edge_label = "%s" % (CURVE_META_SWAP_FLOW[1].split(":")[1])
    #         next_edge_label = "%s" % (CURVE_META_SWAP_FLOW[5].split(":")[1])

    #     cells.append(
    #         {
    #             "n": "%s_%s" % (first_step, n_label),
    #             "n_label": n_label,
    #             "prev_edge_label": prev_edge_label,
    #             "next_edge_label": next_edge_label,
    #             "graph_group": "CurveMetaPool",
    #             "children": [],
    #         }
    #     )


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
                l = G.get_edge(node, next_node).attr["label"]
                edges_to_del.append((prev_node, node, next_node, l))

    for prev_node, node, next_node, l in edges_to_del:
        G.remove_edge(prev_node, node)
        G.add_edge(prev_node, next_node, label=l)
    for dn in nodes_to_del:
        G.remove_node(dn)


def remove_useless_subgraph(G, token_flow_list):
    graphs = G.subgraphs()
    length = len(graphs)
    graphs_to_del = []
    for i in range(length):
        g = graphs[i]
        print(g.get_name())

        if "_transfer:" in g.get_name():
            graphs_to_del.append(g)

    for g in graphs_to_del:
        G.remove_subgraph(g)
