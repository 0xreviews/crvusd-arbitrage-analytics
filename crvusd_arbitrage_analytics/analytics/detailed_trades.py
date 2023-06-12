import csv
from analytics.match_action import (
    match_frxeth_action,
    match_swap_pool_action,
    match_take_profit,
    match_weth_action,
)
from utils import format_decimals, get_address_alias
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

            print("trades data write to %s successfully.")

    return all_trades


TOKEN_FLOW_HEADER = [
    "transfer_step",
    "token_symbol",
    "from",
    "to",
    "amount",
    "action_type",
    "swap_pool",
]


def generate_token_flow(
    transfers, address_tags, save=False, save_dir=DEFAUT_TRADES_TOKENFLOW_DATA_DIR
):
    token_flow_list = []
    for i in range(len(transfers)):
        item = transfers[i]

        token_flow = [
            i,
            item["token_symbol"],
            item["from_alias"],
            item["to_alias"],
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
            # check flash swap
            use_flash = True
            if i > 0:
                (
                    _,
                    _,
                    prev_swap_pool,
                    prev_swap_type_index,
                    _,
                    _,
                    _,
                ) = match_swap_pool_action(i - 1, transfers)
                if prev_swap_pool == swap_pool:
                    use_flash = prev_swap_type_index == swap_type_index
            if len(transfers) > i + 2:
                (
                    _,
                    _,
                    next_swap_pool,
                    next_swap_type_index,
                    _,
                    _,
                    _,
                ) = match_swap_pool_action(i + 1, transfers)
                if next_swap_pool == swap_pool:
                    use_flash = next_swap_type_index == swap_type_index

            if use_flash:
                swap_type_index += 2

            action_row = [swap_flow_list[swap_type_index], swap_pool]

        token_flow += action_row

        token_flow_list.append(token_flow)

    if save:
        with open(save_dir, "w") as f:
            writer = csv.writer(f)
            writer.writerow(TOKEN_FLOW_HEADER)
            writer.writerows(token_flow_list)

    return token_flow_list
