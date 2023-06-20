import csv
import json
import re
import pandas as pd

from utils import process_token_path

SPLIT_SYMBOL = "\n"


def sort_data():
    with open("data/detailed_trades_tokenflow_data.json", "r") as f:
        trades_data = json.load(f)

        arbi_type_data = []

        for i in range(len(trades_data)):
            row = trades_data[i]
            tx = row["transactionHash"]
            timestamp = row["timestamp"]

            token_path = []
            action_types = []
            swap_pools = []
            action_groups = []
            flash_pairs = []

            for j in range(len(row["token_flow_list"])):
                item = row["token_flow_list"][j]

                if re.compile("(call_arbi_contract|miner|beneficiary)").match(item["action_type"]):
                    continue

                token_path.append(item["token_symbol"])
                action_types.append(item["action_type"])
                swap_pools.append(item["swap_pool"])
                action_groups.append(item["action_group"])
                flash_pairs.append(str(item["flash_pair"]) if "flash_pair" in item.keys() else "")

            arbi_type_data.append(
                {
                    "tx": tx,
                    "timestamp": timestamp,
                    "token_path": SPLIT_SYMBOL.join(token_path),
                    "action_types": SPLIT_SYMBOL.join(action_types),
                    "swap_pools": SPLIT_SYMBOL.join(swap_pools),
                    "action_groups": SPLIT_SYMBOL.join(action_groups),
                    "flash_pairs": SPLIT_SYMBOL.join(flash_pairs),
                }
            )

        df = pd.DataFrame(arbi_type_data)

        group = df.groupby(by="swap_pools")

        action_types_sort = []
        i = 0
        for g in group:
            action_types_sort.append(
                {
                    "index": str(i),
                    "count": g[1]["action_types"].count(),
                    "tx_0": g[1]["tx"].values[0],
                    "action_types": g[1]["action_types"].values[0],
                    "swap_pools": g[1]["swap_pools"].values[0],
                    "token_path": g[1]["token_path"].values[0],
                    "action_groups": g[1]["action_groups"].values[0],
                    "flash_pairs": g[1]["flash_pairs"].values[0],
                }
            )
            i += 1

        action_types_sort.sort(key=lambda x: x["count"], reverse=True)

        with open("data/action_types.csv", "w") as action_types_file:
            writer = csv.writer(action_types_file)
            writer.writerows(
                [
                    [
                        "index",
                        "count",
                        "tx_0",
                        "action_types",
                        "swap_pools",
                        "token_path",
                        "action_groups",
                        "flash_pair",
                    ]
                ]
                + [item.values() for item in action_types_sort]
            )


if __name__ == "__main__":
    sort_data()
