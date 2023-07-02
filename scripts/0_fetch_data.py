import json
import os
import time
import asyncio
from analytics.detailed_trades import fetch_analytics_data_batch, get_trades_data
from config.filename_config import DEFAULT_EIGENPHI_TX_RAW_DIR, DEFAUT_TRADES_DATA_DIR
from collector.coingecko.query import query_prices_historical


async def get_prices_data():
    results = []
    for symbol in ["sfrxeth", "wsteth"]:
        raws = await query_prices_historical(token_symbol=symbol, save=True)
        results.append(raws)
    return results

async def main():
    for collateral in ["sFrxETH", "wstETH"]:
        raw_save_dir = DEFAULT_EIGENPHI_TX_RAW_DIR.replace(
            ".json", "_%s.json" % (collateral)
        )

        all_trades = get_trades_data(
            llamma_collateral=collateral,
            save=True,
            save_csv=True,
            save_dir=DEFAUT_TRADES_DATA_DIR,
        )

        batch_size = 50
        data_lines = []
        json_data = []
        raws_data = []

        exists_data = None
        all_txs = []
        if os.path.exists(raw_save_dir):
            with open(raw_save_dir, "r") as exists_data_file:
                exists_data = json.load(exists_data_file)
                raws_data = [] + exists_data
                exists_txs = [item["tx"] for item in exists_data]
                for _trade in all_trades:
                    if _trade["transactionHash"] not in exists_txs:
                        all_txs.append(_trade)
                print(
                    "exists_txs len %d, fetch data len %d"
                    % (len(exists_txs), len(all_txs))
                )
        else:
            all_txs = all_trades

        for i in range(len(all_txs) // batch_size + 1):
            begin_index = i * batch_size
            end_index = min(len(all_txs), (i + 1) * batch_size)
            print("process txs %d to %d" % (begin_index, end_index))
            txs = all_txs[begin_index:end_index]
            raws = await fetch_analytics_data_batch(txs)
            raws_data += raws
            time.sleep(0.1)

        with open(raw_save_dir, "w") as f:
            f.write(json.dumps(raws_data, indent=4))

if __name__ == "__main__":
    asyncio.run(get_prices_data())
    asyncio.run(main())
