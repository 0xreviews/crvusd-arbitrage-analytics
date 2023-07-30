import json
import os
import time
import asyncio
from analytics.get_trades import fetch_analytics_data_batch, fetch_summary_data_batch, get_trades_data
from config.filename_config import DEFAULT_EIGENPHI_TX_RAW_DIR, DEFAUT_TRADES_GQL_DIR
from collector.coingecko.query import query_prices_historical


async def get_prices_data():
    results = []
    for symbol in ["sfrxeth", "wsteth", "wbtc", "weth"]:
        raws = await query_prices_historical(token_symbol=symbol, save=True)
        results.append(raws)
    return results


async def refetch_summary_data(exists_data):
    fetch_index_list = []
    fetch_tx_list = []
    for i in range(len(exists_data)):
        if exists_data[i]["summary_original"] is None:
            fetch_index_list.append(i)
            fetch_tx_list.append(exists_data[i]["tx"])
    
    results = await fetch_summary_data_batch(fetch_tx_list)
    for i in range(len(results)):
        exists_data[fetch_index_list[i]]["summary_original"] = results[i]
    
    print("refetch_summary_data res len ", len(results))
    return exists_data


async def main():
    for collateral in ["sfrxETH", "wstETH", "WBTC", "WETH"]:
        raw_save_dir = DEFAULT_EIGENPHI_TX_RAW_DIR.replace(
            ".json", "_%s.json" % (collateral)
        )

        all_trades = get_trades_data(llamma_collateral=collateral)

        batch_size = 30
        raws_data = []

        exists_data = None
        fetch_txs = []
        if os.path.exists(raw_save_dir):
            with open(raw_save_dir, "r") as exists_data_file:
                exists_data = json.load(exists_data_file)
                # refetch summary data
                exists_data = await refetch_summary_data(exists_data)
                raws_data = [] + exists_data
                exists_txs = [item["tx"] for item in exists_data]
                for _trade in all_trades:
                    if _trade["transactionHash"] not in exists_txs:
                        fetch_txs.append(_trade)
                print(
                    "exists_txs len %d, fetch data len %d"
                    % (len(exists_txs), len(fetch_txs))
                )
        else:
            fetch_txs = all_trades

        for i in range(len(fetch_txs) // batch_size + 1):
            begin_index = i * batch_size
            end_index = min(len(fetch_txs), (i + 1) * batch_size)
            print("process txs %d to %d" % (begin_index, end_index))
            txs = fetch_txs[begin_index:end_index]
            raws = await fetch_analytics_data_batch(txs)
            raws_data += raws
            time.sleep(0.3)

        with open(raw_save_dir, "w") as f:
            f.write(json.dumps(raws_data, indent=4))


if __name__ == "__main__":
    asyncio.run(get_prices_data())
    asyncio.run(main())
