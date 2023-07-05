import csv
import json
import os
import re
import matplotlib.pyplot as plt

from utils.date import timestamp_to_date

plt.style.use(
    os.path.join(os.path.dirname(__file__), "../config/pitayasmoothie-dark.mplstyle")
)
default_chart_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

SPLIT_SYMBOL = "\n"
GROUP_KEY = "swap_pools"


def sort_arbitrage_data(trades_data):
    arbi_type_data = []

    for i in range(len(trades_data)):
        row = trades_data[i]
        tx = row["tx"]
        timestamp = row["timestamp"]

        token_path = []
        action_types = []
        swap_pools = []
        action_groups = []
        flash_pairs = []

        for j in range(len(row["token_flow_list"])):
            item = row["token_flow_list"][j]

            if re.compile("(call_arbi_contract|miner|beneficiary)").match(
                item["action_type"]
            ):
                continue

            token_path.append(item["token_symbol"])
            action_types.append(item["action_type"])
            swap_pools.append(item["swap_pool"])
            action_groups.append(item["action_group"])
            flash_pairs.append(
                str(item["flash_pair"]) if "flash_pair" in item.keys() else ""
            )

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
    
    return arbi_type_data


def sort_arbi_type(df, save_csv_dir, save_json_dir):
    group = df.groupby(by=GROUP_KEY)

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

    with open(save_csv_dir, "w") as action_types_file:
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

    with open(save_json_dir, "w") as action_types_file:
        json_data = [
            {
                "index": item["index"],
                "count": int(item["count"]),
                "tx_0": item["tx_0"],
                "action_types": item["action_types"].split(SPLIT_SYMBOL),
                "swap_pools": item["swap_pools"].split(SPLIT_SYMBOL),
                "token_path": item["token_path"].split(SPLIT_SYMBOL),
                "action_groups": item["action_groups"].split(SPLIT_SYMBOL),
                "flash_pairs": item["flash_pairs"].split(SPLIT_SYMBOL),
            }
            for item in action_types_sort
        ]
        action_types_file.write(json.dumps(json_data, indent=4))
    
    return json_data

def sort_arbi_type_stack(df, sort_arbi_type_data, save_dir):
    # sort by date
    df_dates = [
        timestamp_to_date(int(item)).date() for item in list(df["timestamp"])
    ]
    df["date"] = df_dates


    arbi_types = {}
    for i in range(len(sort_arbi_type_data)):
        swap_pools = sort_arbi_type_data[i]["swap_pools"]
        arbi_t = SPLIT_SYMBOL.join(swap_pools)
        arbi_types[arbi_t] = i

    df_arbi_type = [int(arbi_types[item]) for item in list(df["swap_pools"])]
    df["arbi_type"] = df_arbi_type

    x_labes = []
    y_data = {}

    group = df.groupby(by="date")

    STACK_TYPE_LABELS = ['A', "B", "C", "D", "E", "others"]

    for g in group:
        x_labes.append(g[0])
        _y = {}
        for index in g[1]["arbi_type"].to_list():
            index = int(index)
            if index < len(STACK_TYPE_LABELS)-1:
                _type = STACK_TYPE_LABELS[index]
            else:
                _type = "others"
            if _type not in _y:
                _y[_type] = 0
            _y[_type] += 1
        
        for label in STACK_TYPE_LABELS[:-1]:
            if label not in y_data:
                y_data[label] = []
            if label in _y:
                y_data[label].append(_y[label])
            else:
                y_data[label].append(0)
    

    fig, ax = plt.subplots()
    ax.stackplot(x_labes, y_data.values(),
                labels=y_data.keys(), alpha=0.8)
    ax.legend(loc='upper left')
    ax.set_title('Arbitrage Type')
    ax.set_xlabel('Date')
    ax.set_ylabel('count')

    plt.subplots_adjust(left=0.1, right=0.9)
    plt.margins(0.2)
    fig.set_size_inches(12, 12)
    fig.savefig(save_dir, dpi=100)