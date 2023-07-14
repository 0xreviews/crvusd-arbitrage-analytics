import asyncio
import csv
import json
import re
from analytics.match_action import (
    match_call_arbitrage_contract,
    match_frxeth_action,
    match_swap_pool_action,
    match_take_profit,
    match_weth_action,
)
from analytics.match_action_group import match_action_group
from collector.eigenphi.query import (
    query_eigenphi_analytics_tx,
    query_eigenphi_summary_tx,
)
from collector.eigenphi.utils import get_eigenphi_tokenflow

from utils.match import format_decimals, get_address_alias, is_llamma_swap
from collector.graphql.query import query_detailed_trades_all
from config.constance import EIGEN_TX_URL
from config.filename_config import (
    DEFAUT_TRADES_DATA_DIR,
    DEFAUT_TRADES_TOKENFLOW_DATA_DIR,
)


def get_trades_data(
    llamma_collateral, save=False, save_csv=False, save_dir=DEFAUT_TRADES_DATA_DIR
):
    all_trades = query_detailed_trades_all(llamma_collateral)

    if save:
        save_dir = save_dir.replace(".json", "_%s.json" % (llamma_collateral))
        with open(save_dir, "w") as json_file:
            json_file.write(json.dumps(all_trades, indent=4))

        if save_csv:
            csv_dir = save_dir.replace(".json", ".csv")
            with open(csv_dir, "w") as csv_file:
                writer = csv.writer(csv_file)
                header = []
                process_decimals_keys = [
                    "tokensSold",
                    "tokensBought",
                    # "avg_price",
                    # "oracle_price",
                    # "market_price",
                    # "profit_rate",
                ]
                if len(all_trades) > 0:
                    header = [h for h in all_trades[0]] + ["eigenphi_txlink"]
                    writer.writerow(header)

                    for i in range(len(all_trades)):
                        row = all_trades[i]
                        # process decimals
                        for _k in process_decimals_keys:
                            row[_k] = int(row[_k]) / 1e18
                        # ticks_in = []
                        # ticks_out = []
                        # for i in range(len(row["ticks_in"])):
                        #     ticks_in.append(int(row["ticks_in"][i]) / 1e18)
                        # for i in range(len(row["ticks_out"])):
                        #     ticks_out.append(int(row["ticks_out"][i]) / 1e18)
                        # row["ticks_in"] = ticks_in
                        # row["ticks_out"] = ticks_out

                        # add eigenphi link
                        row["eigenphi_txlink"] = EIGEN_TX_URL + row["transactionHash"]
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
    "flash_pair",
]


def generate_token_flow(transfers, address_tags):
    token_flow_list = []
    for i in range(len(transfers)):
        item = transfers[i]

        token_flow = {
            "transferStep": i,
            "from": item["from_alias"],
            "to": item["to_alias"],
            "token_symbol": item["token_symbol"],
            "amount": float(item["amount"]),
        }

        (
            call_arbitrage_contract_type_index,
            call_arbitrage_contract_type,
        ) = match_call_arbitrage_contract(i, transfers, address_tags)
        (take_profit_type_index, take_profit_type) = match_take_profit(
            i, transfers, address_tags
        )
        (weth_match_index, weth_math_type, weth_match_tokensymbol) = match_weth_action(
            i, transfers, target_symbol="weth"
        )
        (reth_match_index, reth_math_type, reth_match_tokensymbol) = match_weth_action(
            i, transfers, target_symbol="reth"
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
        ) = match_swap_pool_action(i, transfers, address_tags)

        action_row = ["", ""]

        if take_profit_type_index > -1:
            action_row = [take_profit_type, ""]
        if weth_match_index > -1:
            action_row = [weth_math_type, ""]
        if reth_match_index > -1:
            action_row = [reth_math_type, ""]
        if frxeth_match_index > -1:
            action_row = [frxeth_math_type, ""]
        if pool_type_index > -1:
            action_row = [swap_flow_list[swap_type_index], swap_pool]
        if call_arbitrage_contract_type_index > -1:
            action_row = [call_arbitrage_contract_type, ""]

        token_flow["action_type"] = action_row[0]
        token_flow["swap_pool"] = action_row[1]

        token_flow_list.append(token_flow)

    return token_flow_list


def generate_tx_summary(resp):
    if resp is None:
        return None, None, None

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


async def fetch_analytics_data_batch(txs):
    tasks = []
    for i in range(len(txs)):
        target_tx = txs[i]["transactionHash"]
        tasks.append(query_eigenphi_summary_tx(target_tx))
        tasks.append(query_eigenphi_analytics_tx(target_tx))

    results = await asyncio.gather(*tasks)
    print("query results:", len(results) // 2)

    raws = []
    for i in range(len(txs)):
        row = txs[i]

        # save original data
        raws.append(
            {
                "tx": row["transactionHash"],
                "timestamp": row["blockTimestamp"],
                # "LLAMMA_avg_price": row["avg_price"],
                # "sfrxETH_oracle_price": row["oracle_price"],
                # "sfrxETH_market_price": row["market_price"],
                "summary_original": results[i * 2],
                "analytics_tx_original": results[i * 2 + 1],
            }
        )

    return raws


def wash_analytics_data_from_file(original_raw_data_dir=DEFAUT_TRADES_TOKENFLOW_DATA_DIR):
    with open(original_raw_data_dir, encoding="utf-8") as f:
        original_data = json.load(f)
        return wash_analytics_data(original_data)

def wash_analytics_data(original_data):
    csv_lines = []
    json_data = []
    for i in range(len(original_data)):
        # # @follow-up
        # if original_data[i]["tx"] != "0xebf1ac9c93f7af806120d15eaee1994fce511ef8ddb71b2c586ede38e6a3dc11":
        #     continue

        row = original_data[i]
        summary, token_prices, tx_meta = generate_tx_summary(row["summary_original"])

        token_balance_diff, address_tags, transfers = get_eigenphi_tokenflow(
            row["analytics_tx_original"]
        )

        token_flow_list = generate_token_flow(
            transfers,
            address_tags,
        )

        token_flow_list = match_action_group(token_flow_list)

        liquidate_volume = 0
        # get LLAMMA trade volume
        for flow in token_flow_list:
            if flow["token_symbol"] == "crvusd" and is_llamma_swap(flow["swap_pool"]):
                liquidate_volume = flow["amount"]
                break

        csv_lines += [[str(i)]]

        csv_lines.append(
            [
                "tiemstamp & tx_hash:",
                row["timestamp"],
                row["tx"],
            ]
        )

        if summary is not None:
            csv_lines += [
                ["summary:"] + [str(key) for key in summary.keys()],
                [""] + [str(value) for value in summary.values()],
            ]

        if token_prices is not None:
            csv_lines += [
                ["price:"] + [item["token_symbol"] for item in token_prices],
                [""] + [str(item["price_usd"]) for item in token_prices],
            ]

        csv_lines += (
            [[], TOKEN_FLOW_HEADER]
            + [item.values() for item in token_flow_list]
            + [[], []]
        )

        json_data.append(
            {
                "tx": row["tx"],
                "timestamp": row["timestamp"],
                # "LLAMMA_avg_price": row["LLAMMA_avg_price"],
                # "sfrxETH_oracle_price": row["sfrxETH_oracle_price"],
                # "sfrxETH_market_price": row["sfrxETH_market_price"],
                "liquidate_volume": liquidate_volume,
                "summary": summary,
                "address_tags": address_tags,
                "token_prices": token_prices,
                "tx_meta": tx_meta,
                "token_flow_list": token_flow_list,
            }
        )

    return json_data, csv_lines
