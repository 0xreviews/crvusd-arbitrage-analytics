import csv
import json
from collector.tenderly.utils import tenderly_tokenflow
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


# def process_tx_tokenflow(tx):
#     resp = query_tenderly_txtrace(tx)
#     asset_changes, token_balance_diff = tenderly_tokenflow(resp)
    
#     return asset_changes, token_balance_diff

# def process_trades_tokenflow_data(
#     trades_data_dir=DEFAUT_TRADES_DATA_DIR,
#     save=False,
#     save_dir=DEFAUT_TRADES_TOKENFLOW_DATA_DIR,
# ):
#     with open(trades_data_dir, newline="") as csvfile:
#         tx_header_index = 0
#         data = {}
#         spamreader = csv.reader(csvfile, delimiter=",")
#         for row in spamreader:
#             # header
#             if row[0] == "id":
#                 for i in range(len(row)):
#                     if row[i] == "tx":
#                         tx_header_index = i
#                         break
#                 # skip header
#                 continue

#             _id = row[0]
#             tx = row[tx_header_index]
#             asset_changes, balance_diff = query_tx_tokenflow(tx)
#             data[_id] = {
#                 "asset_changes": asset_changes,
#                 "balance_diff": balance_diff,
#             }

#         if save:
#             with open(save_dir, "w") as f:
#                 f.write(json.dumps(data))

#     return data

