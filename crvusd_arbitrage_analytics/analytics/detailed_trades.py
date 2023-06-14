import csv
import re
from analytics.match_action import (
    match_frxeth_action,
    match_swap_pool_action,
    match_take_profit,
    match_weth_action,
)
from config.tokenflow_category import (
    ACTION_GROUP_TAG,
    ACTION_GROUP_TYPE,
    CURVE_META_SWAP_FLOW,
    CURVE_SWAP_WETH_FLOW,
)
from utils import format_decimals, get_address_alias, is_curve_router
from collector.graphql.query import query_detailed_trades_all
from collector.tenderly.query import query_tenderly_txtrace
from config.constance import ADDRESS_ZERO, ALIAS_TO_ADDRESS, EIGEN_TX_URL
from config.filename_config import (
    DEFAUT_TRADES_DATA_DIR,
    DEFAUT_TRADES_TOKENFLOW_DATA_DIR,
)


def process_trades_data(save=False, save_dir=DEFAUT_TRADES_DATA_DIR):
    all_trades = query_detailed_trades_all()

    if save:
        with open(save_dir, "w") as f:
            writer = csv.writer(f)
            header = []
            process_decimals_keys = [
                "tokens_sold",
                "tokens_bought",
                "avg_price",
                "oracle_price",
                "market_price",
                "profit_rate",
            ]
            if len(all_trades) > 0:
                header = [h for h in all_trades[0]] + ["eigenphi_txlink"]
                writer.writerow(header)

                for i in range(len(all_trades)):
                    row = all_trades[i]
                    # process decimals
                    for _k in process_decimals_keys:
                        row[_k] = int(row[_k]) / 1e18
                    ticks_in = []
                    ticks_out = []
                    for i in range(len(row["ticks_in"])):
                        ticks_in.append(int(row["ticks_in"][i]) / 1e18)
                    for i in range(len(row["ticks_out"])):
                        ticks_out.append(int(row["ticks_out"][i]) / 1e18)
                    row["ticks_in"] = ticks_in
                    row["ticks_out"] = ticks_out

                    # add eigenphi link
                    row["eigenphi_txlink"] = EIGEN_TX_URL + row["tx"]
                    writer.writerow([row[k] for k in row])

            print("trades data write to %s successfully." % (save_dir))

    return all_trades


TOKEN_FLOW_HEADER = [
    "transfer_step",
    "from",
    "to",
    "token_symbol",
    "amount",
    "action_type",
    "swap_pool",
    "action_group",
]


def generate_token_flow(transfers, address_tags):
    token_flow_list = []
    for i in range(len(transfers)):
        item = transfers[i]

        token_flow = [
            i,
            item["from_alias"],
            item["to_alias"],
            item["token_symbol"],
            str(item["amount"]),
        ]

        (take_profit_type_index, take_profit_type) = match_take_profit(
            i, transfers, address_tags
        )
        (weth_match_index, weth_math_type, weth_match_tokensymbol) = match_weth_action(
            i, transfers
        )
        (
            frxeth_match_index,
            frxeth_math_type,
            frxeth_math_tokensymbol,
        ) = match_frxeth_action(i, transfers)
        (
            pool_type_index,
            pool_type,
            swap_pool,
            swap_type_index,
            swap_type,
            token_symbol,
            swap_flow_list,
        ) = match_swap_pool_action(i, transfers)

        action_row = ["", ""]

        if take_profit_type_index > -1:
            action_row = [take_profit_type, ""]
        if weth_match_index > -1:
            action_row = [weth_math_type, ""]
        if frxeth_match_index > -1:
            action_row = [frxeth_math_type, ""]
        if pool_type_index > -1:
            action_row = [swap_flow_list[swap_type_index], swap_pool]

        token_flow += action_row

        token_flow_list.append(token_flow)

    return token_flow_list


def generate_tx_summary(resp):
    summary = resp["summary"]
    tx_meta = resp["txMeta"]
    token_prices = []

    for i in range(len(resp["tokenPrices"])):
        row = resp["tokenPrices"][i]
        # # @remind usdt, usdc price's decimals in result is 12
        # if get_address_alias(row["tokenAddress"]).lower() in ["usdt", "usdc"]:
        #     row["priceInUsd"] = float(row["priceInUsd"]) / 1e12
        token_prices.append(
            {
                "token_address": row["tokenAddress"],
                "token_symbol": get_address_alias(row["tokenAddress"]).lower(),
                "price_usd": row["priceInUsd"],
                "timestamp": tx_meta["blockTimestamp"],
            }
        )

    return summary, token_prices, tx_meta


def generate_txs_analytics(
    summary,
    token_prices,
    tx_meta,
    token_flow_list,
):
    lines = []

    if tx_meta is not None:
        lines.append(
            [
                "tiemstamp & tx_hash:",
                tx_meta["blockTimestamp"],
                tx_meta["transactionHash"],
            ]
        )

    if summary is not None:
        lines += [
            ["summary:"] + [str(key) for key in summary.keys()],
            [""] + [str(value) for value in summary.values()],
        ]

    if token_prices is not None:
        lines += [
            ["price:"] + [item["token_symbol"] for item in token_prices],
            [""] + [str(item["price_usd"]) for item in token_prices],
        ]

    token_flow_list = generate_action_group(token_flow_list)

    lines += [
        [],
        TOKEN_FLOW_HEADER,
    ] + token_flow_list

    return lines


# @todo match flash action group


def generate_action_group(token_flow_list):
    tmp_begin = -1
    tmp_end = -1
    tmp_group_index = -1

    for i in range(len(token_flow_list)):
        # clear prev group if it end
        if tmp_end > -1:
            tmp_begin = -1
            tmp_end = -1
            tmp_group_index = -1

        row = token_flow_list[i]
        action_group_item = ""

        # group begin
        if tmp_begin < 0:
            tmp_begin = i
            tmp_group_index = check_action_group(row)

        # group end
        if tmp_end < 0:
            if i == len(token_flow_list) - 1:
                tmp_end = i
            elif i < len(token_flow_list) - 1:
                next_row = token_flow_list[i + 1]
                next_group_index = check_action_group(next_row)
                if next_group_index != tmp_group_index:
                    tmp_end = i

                # @remind some exceptions， not the end of group

                # CurveRouter pool deposit/withdraw WETH
                if tmp_group_index == 0:
                    if next_row[-2] in CURVE_SWAP_WETH_FLOW:
                        tmp_end = -1
                    elif next_row[-2] in CURVE_META_SWAP_FLOW:
                        tmp_end = -1

        if tmp_group_index > -1:
            tmp_action_group = ACTION_GROUP_TYPE[tmp_group_index]
            action_group_item = "%s:%d" % (tmp_action_group, i - tmp_begin)

        # add action_group tag

        # CurveRouterSwap group tag
        if tmp_group_index == 0:
            if i == tmp_begin:
                action_group_item += ":%s" % (ACTION_GROUP_TAG[0])
            elif i == tmp_end:
                action_group_item += ":%s" % (ACTION_GROUP_TAG[2])
            else:
                action_group_item += ":%s" % (ACTION_GROUP_TAG[1])

        token_flow_list[i].append(action_group_item)

    return token_flow_list


def check_action_group(row):
    action_type = row[-2]
    swap_pool = row[-1]
    group_index = -1

    for i in range(len(ACTION_GROUP_TYPE)):
        if re.compile("^" + ACTION_GROUP_TYPE[i]).match(action_type):
            group_index = i
            break

    return group_index
