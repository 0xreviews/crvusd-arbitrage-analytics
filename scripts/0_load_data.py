import csv
import json
from analytics.detailed_trades import fetch_analytics_data_batch, get_trades_data
from config.filename_config import DEFAULT_EIGENPHI_TX_RAW_DIR, DEFAUT_TRADES_DATA_DIR


if __name__ == "__main__":
    all_trades = get_trades_data(
        save=True, save_csv=True, save_dir=DEFAUT_TRADES_DATA_DIR
    )

    batch_size = 60
    data_lines = []
    json_data = []
    raws_data = []

    for i in range(len(all_trades) // batch_size + 1):
        begin_index = i * batch_size
        end_index = min(len(all_trades), (i + 1) * batch_size)
        print("process txs %d to %d" % (begin_index, end_index))
        txs = all_trades[begin_index:end_index]
        raws = fetch_analytics_data_batch(
            txs,
            begin_index,
        )
        raws_data += raws

    with open(DEFAULT_EIGENPHI_TX_RAW_DIR, "w") as f:
        f.write(json.dumps(raws_data, indent=4))
