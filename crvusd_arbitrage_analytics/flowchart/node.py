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


def generate_flow_cell(transfers):
    cells = []

    first_step = -1
    tokens = []
    swap_pools = []
    actions = []
    groups = []

    for i in range(len(transfers)):
        row = transfers[i]

        if first_step < 0:
            first_step = row["transferStep"]

        tokens.append(row["token_symbol"])
        actions.append(row["action_type"])
        groups.append(row["action_group"])
        pools = row["swap_pool"].split(",")
        for _p in pools:
            if _p not in swap_pools:
                swap_pools.append(_p)

    if first_step == 0:
        _action = actions[0]
        if _action == CALL_ARBI_CONTRACT_FLOW[0]:
            _action = ""
        elif _action == CALL_ARBI_CONTRACT_FLOW[1]:
            _action = tokens[0]
        cells += [
            {
                "n": "%s_%s" % (first_step, transfers[0]["from"]),
                "n_label": transfers[0]["from"],
                "prev_edge_label": "",
                "next_edge_label": "",
            },
            {
                "n": "%s_%s" % (first_step, transfers[0]["to"]),
                "n_label": transfers[0]["to"],
                "prev_edge_label": _action,
                "next_edge_label": "",
            },
        ]
    # LLAMMA swap
    elif is_llamma_swap(",".join(swap_pools)):
        n_label = get_swap_pool_exclude_router(swap_pools)

        edge_label = ""
        if ",".join(actions) == ",".join([LLAMMA_SWAP_FLOW[0], LLAMMA_SWAP_FLOW[1]]):
            # token out token in
            edge_label = "%s out %s in" % (tokens[0], tokens[1])
        elif ",".join(actions) == ",".join([LLAMMA_SWAP_FLOW[1], LLAMMA_SWAP_FLOW[0]]):
            # token in token out
            edge_label = "%s in %s out" % (tokens[0], tokens[1])

        cells.append(
            {
                "n": "%s_%s" % (first_step, n_label),
                "n_label": n_label,
                "prev_edge_label": edge_label,
                "next_edge_label": "",
            }
        )
    # CurveRouter
    elif is_curve_router(",".join(swap_pools)):
        # CurveRouter:token_in
        if ",".join(actions) == CURVE_ROUTER_FLOW[0]:
            cells.append(
                {
                    "n": "%s_CurveSwapRouter" % (first_step),
                    "n_label": "CurveSwapRouter",
                    "prev_edge_label": "%s" % (tokens[0]),
                    "next_edge_label": "",
                }
            )
        # CurveRouter:token_out
        elif ",".join(actions) == CURVE_ROUTER_FLOW[1]:
            cells.append(
                {
                    "n": "%s_CurveSwapRouter" % (first_step),
                    "n_label": "CurveSwapRouter",
                    "prev_edge_label": "%s" % (tokens[0]),
                    "next_edge_label": "",
                }
            )
        elif is_router_mid_node(",".join(groups)):
            n_label = get_swap_pool_exclude_router(swap_pools)

            prev_edge_label = ""
            next_edge_label = ""
            if ",".join(actions) == ",".join(
                [CURVE_ROUTER_FLOW[2], CURVE_ROUTER_FLOW[3]]
            ):
                # token out token in
                prev_edge_label = "%s" % (tokens[1])
                next_edge_label = "%s" % (tokens[0])
            elif ",".join(actions) == ",".join(
                [CURVE_ROUTER_FLOW[3], CURVE_ROUTER_FLOW[2]]
            ):
                # token in token out
                prev_edge_label = "%s" % (tokens[0])
                next_edge_label = "%s" % (tokens[1])

            cells.append(
                {
                    "n": "%s_%s" % (first_step, n_label),
                    "n_label": n_label,
                    "prev_edge_label": prev_edge_label,
                    "next_edge_label": next_edge_label,
                }
            )
    # WETH Flow
    elif re.compile("WETH").match(",".join(groups)):
        prev_edge_label = ""
        # WETH_deposit
        if ",".join(actions) == ",".join([WETH_FLOW[0], WETH_FLOW[1]]):
            prev_edge_label = WETH_FLOW[0].split(":")[0]
        # WETH_withdraw
        if ",".join(actions) == ",".join([WETH_FLOW[3], WETH_FLOW[2]]):
            prev_edge_label = WETH_FLOW[0].split(":")[0]

        cells.append(
            {
                "n": "%s_WETH" % (first_step),
                "n_label": "WETH",
                "prev_edge_label": prev_edge_label,
                "next_edge_label": "",
            }
        )
    # frxETH Flow
    elif re.compile("frxETH").match(",".join(groups)):
        prev_edge_label = ""
        # frxETH_mint
        if ",".join(actions) == ",".join([FRXETH_FLOW[0], FRXETH_FLOW[1]]):
            prev_edge_label = FRXETH_FLOW[0].split(":")[0]
        # frxETH_stake
        elif ",".join(actions) == ",".join([FRXETH_FLOW[2], FRXETH_FLOW[3]]):
            prev_edge_label = FRXETH_FLOW[2].split(":")[0]
        # frxETH_unstake
        elif ",".join(actions) == ",".join([FRXETH_FLOW[5], FRXETH_FLOW[4]]):
            prev_edge_label = FRXETH_FLOW[4].split(":")[0]

        cells.append(
            {
                "n": "%s_sFrxETH" % (first_step),
                "n_label": "sFrxETH",
                "prev_edge_label": prev_edge_label,
                "next_edge_label": "",
            }
        )
    # WETH Flow
    elif re.compile("WETH").match(",".join(groups)):
        prev_edge_label = ""
        # WETH_deposit
        if ",".join(actions) == ",".join([WETH_FLOW[0], WETH_FLOW[1]]):
            prev_edge_label = WETH_FLOW[0].split(":")[0]
        # WETH_withdraw
        if ",".join(actions) == ",".join([WETH_FLOW[3], WETH_FLOW[2]]):
            prev_edge_label = WETH_FLOW[0].split(":")[0]

        cells.append(
            {
                "n": "%s_WETH" % (first_step),
                "n_label": "WETH",
                "prev_edge_label": prev_edge_label,
                "next_edge_label": "",
            }
        )
    # CurveSwap:WETH deposit/withdraw
    elif re.compile("CurveSwap:WETH").match(",".join(actions)):
        prev_edge_label = ""
        next_edge_label = ""
        n_label = get_swap_pool_exclude_router(swap_pools)
        # WETH_deposit
        if ",".join(actions) == ",".join(
            [CURVE_SWAP_WETH_FLOW[0], CURVE_SWAP_WETH_FLOW[1]]
        ):
            prev_edge_label = CURVE_SWAP_WETH_FLOW[0].split(":")[1]
            next_edge_label = CURVE_SWAP_WETH_FLOW[1].split(":")[1]
        # WETH_withdraw
        if ",".join(actions) == ",".join(
            [CURVE_SWAP_WETH_FLOW[2], CURVE_SWAP_WETH_FLOW[3]]
        ):
            prev_edge_label = CURVE_SWAP_WETH_FLOW[2].split(":")[1]
            next_edge_label = CURVE_SWAP_WETH_FLOW[3].split(":")[1]

        cells.append(
            {
                "n": "%s_WETH" % (first_step),
                "n_label": "WETH",
                "prev_edge_label": prev_edge_label,
                "next_edge_label": next_edge_label,
            }
        )
    # Curve Meta Swap Pool
    elif re.compile("CurveSwap:MetaPool").match(",".join(actions)):
        prev_edge_label = ""
        next_edge_label = ""
        # n_label = get_swap_pool_exclude_router(swap_pools)
        n_label = "Curve3Pool-DAI-USDC-USDT"
        # token in + LP mint
        if ",".join(actions) == ",".join([CURVE_META_SWAP_FLOW[0], CURVE_META_SWAP_FLOW[4]]):
            prev_edge_label = "%s" % (CURVE_META_SWAP_FLOW[0].split(":")[1])
            next_edge_label = "%s" % (CURVE_META_SWAP_FLOW[4].split(":")[1])
        # token out + LP burn
        if ",".join(actions) == ",".join([CURVE_META_SWAP_FLOW[1], CURVE_META_SWAP_FLOW[5]]):
            prev_edge_label = "%s" % (CURVE_META_SWAP_FLOW[1].split(":")[1])
            next_edge_label = "%s" % (CURVE_META_SWAP_FLOW[5].split(":")[1])

        cells.append(
            {
                "n": "%s_%s" % (first_step, n_label),
                "n_label": n_label,
                "prev_edge_label": prev_edge_label,
                "next_edge_label": next_edge_label,
            }
        )

    return cells
