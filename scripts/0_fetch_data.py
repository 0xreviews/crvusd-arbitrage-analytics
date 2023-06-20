import json
import time
from analytics.detailed_trades import fetch_analytics_data_batch, get_trades_data
from config.filename_config import DEFAULT_EIGENPHI_TX_RAW_DIR, DEFAUT_TRADES_DATA_DIR


if __name__ == "__main__":
    for collateral in ["sFrxETH", "wstETH"]:
        all_trades = get_trades_data(
            llamma_collateral=collateral,
            save=True,
            save_csv=True,
            save_dir=DEFAUT_TRADES_DATA_DIR,
        )

        batch_size = 10
        data_lines = []
        json_data = []
        raws_data = []

        for i in range(len(all_trades) // batch_size + 1):
            begin_index = i * batch_size
            end_index = min(len(all_trades), (i + 1) * batch_size)
            print("process txs %d to %d" % (begin_index, end_index))
            txs = all_trades[begin_index:end_index]
            raws = fetch_analytics_data_batch(txs)
            raws_data += raws
            time.sleep(3)

        with open(
            DEFAULT_EIGENPHI_TX_RAW_DIR.replace(".json", "_%s.json" % (collateral)), "w"
        ) as f:
            f.write(json.dumps(raws_data, indent=4))
