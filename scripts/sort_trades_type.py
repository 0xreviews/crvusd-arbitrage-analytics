import csv
import json
import pandas as pd


def main():
    with open("data/detailed_trades_tokenflow_data.json", "r") as f:
        trades_data = json.load(f)

        arbi_type_data = []

        for i in range(len(trades_data)):
            row = trades_data[i]
            tx = row["tx"]
            timestamp = row["timestamp"]
            token_path = [item["token_symbol"] for item in row["token_flow_list"]]
            action_types = [item["action_type"] for item in row["token_flow_list"]]
            swap_pools = [item["swap_pool"] for item in row["token_flow_list"]]
            action_groups = [item["action_group"] for item in row["token_flow_list"]]
            arbi_type_data.append(
                {
                    "tx": tx,
                    "timestamp": timestamp,
                    "token_path": "|".join(token_path),
                    "action_types": "|".join(action_types),
                    "swap_pools": "|".join(swap_pools),
                    "action_groups": "|".join(action_groups),
                }
            )

        df = pd.DataFrame(arbi_type_data)
        # print(df)

        group = df.groupby(by="action_types")

        action_types_sort = []
        i = 0
        for g in group:
            action_types_sort.append(
                {
                    "index": str(i),
                    "count": g[1]["action_types"].count(),
                    "tx_0": g[1]["tx"].values[0],
                    "action_types": g[0].split("|"),
                }
            )
            i += 1
        

        action_types_sort.sort(key=lambda x: x["count"], reverse=True)

        with open("data/action_types.csv", "w") as action_types_file:
            writer = csv.writer(action_types_file)
            writer.writerows(
                [["index", "count", "tx_0", "action_types"]]
                + [item.values() for item in action_types_sort]
            )


if __name__ == "__main__":
    main()
