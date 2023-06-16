import csv
import json
from analytics.detailed_trades import fetch_analytics_data_batch, get_trades_data
from config.filename_config import DEFAULT_EIGENPHI_TX_RAW_DIR, DEFAUT_TRADES_DATA_DIR


if __name__ == "__main__":
    use_local_data = False
    gql_alltrades_dir = DEFAUT_TRADES_DATA_DIR
    eigenphi_tx_raw_dir = DEFAULT_EIGENPHI_TX_RAW_DIR

    if not use_local_data:
        all_trades = get_trades_data(
            save=True, save_csv=True, save_dir=gql_alltrades_dir
        )
    else:
        with open(gql_alltrades_dir, encoding="utf-8") as f:
            all_trades = json.load(f)

    batch_size = 60 if not use_local_data else len(all_trades) + 1
    data_lines = []
    json_data = []
    raws_data = []

    for i in range(len(all_trades) // batch_size + 1):
        begin_index = i * batch_size
        end_index = min(len(all_trades), (i + 1) * batch_size)
        print("process txs %d to %d" % (begin_index, end_index))
        txs = all_trades[begin_index:end_index]
        lines, json_lines, raws = fetch_analytics_data_batch(
            txs,
            begin_index,
            original_data_dir=eigenphi_tx_raw_dir if use_local_data else "",
        )
        data_lines += lines
        json_data += json_lines
        raws_data += raws

    with open(
        "data/detailed_trades_tokenflow_data.csv", "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerows(data_lines)

    with open("data/detailed_trades_tokenflow_data.json", "w") as f:
        f.write(json.dumps(json_data, indent=4))

    if not use_local_data:
        with open(eigenphi_tx_raw_dir, "w") as f:
            f.write(json.dumps(raws_data, indent=4))
