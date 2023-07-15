import csv
import json
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from utils.date import timestamp_to_date

plt.style.use(
    os.path.join(os.path.dirname(__file__), "../config/pitayasmoothie-dark.mplstyle")
)
default_chart_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

SPLIT_SYMBOL = ","


def sort_arbitrage_data(trades_data):
    arbi_type_data = []
    sort_type_count = {}

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

            if (
                re.compile("(call_arbi_contract|miner|beneficiary)").match(
                    item["action_type"]
                )
                or item["action_type"] == ""
                or "_transfer" in item["action_type"]
            ):
                continue
            
            token_path.append(item["token_symbol"])
            action_types.append(item["action_type"])
            swap_pools.append(item["swap_pool"])
            action_groups.append(item["action_group"])
            flash_pairs.append(
                str(item["flash_pair"]) if "flash_pair" in item.keys() else ""
            )

        sort_type_value = SPLIT_SYMBOL.join(action_types + token_path)

        arbi_type_data.append(
            {
                "tx": tx,
                "timestamp": timestamp,
                "token_path": SPLIT_SYMBOL.join(token_path),
                "action_types": SPLIT_SYMBOL.join(action_types),
                "swap_pools": SPLIT_SYMBOL.join(swap_pools),
                "action_groups": SPLIT_SYMBOL.join(action_groups),
                "flash_pairs": SPLIT_SYMBOL.join(flash_pairs),
                "sort_type_value": sort_type_value,
            }
        )

        if sort_type_value not in sort_type_count:
            sort_type_count[sort_type_value] = 0
        sort_type_count[sort_type_value] += 1

    return arbi_type_data, sort_type_count


def sort_arbi_type(df, save_csv_dir, save_json_dir):
    group = df.groupby(by=["action_types", "token_path"])

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
                "sort_type_value": g[1]["sort_type_value"].values[0],
            }
        )
        i += 1

    action_types_sort.sort(key=lambda x: x["count"], reverse=True)

    with open(save_csv_dir, "w") as action_types_file:
        writer = csv.writer(action_types_file)
        csv_rows = []
        for row in action_types_sort:
            v = {}
            v["index"] = row["index"]
            v["count"] = row["count"]
            v["tx_0"] = row["tx_0"]
            v["action_types"] = replace_split_symbol(
                row["action_types"], SPLIT_SYMBOL, "\n"
            )
            v["swap_pools"] = replace_split_symbol(
                row["swap_pools"], SPLIT_SYMBOL, "\n"
            )
            v["token_path"] = replace_split_symbol(
                row["token_path"], SPLIT_SYMBOL, "\n"
            )
            v["action_groups"] = replace_split_symbol(
                row["action_groups"], SPLIT_SYMBOL, "\n"
            )
            v["flash_pairs"] = replace_split_symbol(
                row["flash_pairs"], SPLIT_SYMBOL, "\n"
            )
            v["sort_type_value"] = replace_split_symbol(
                row["sort_type_value"], SPLIT_SYMBOL, "\n"
            )
            csv_rows.append(v.values())

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
            + csv_rows
        )

    with open(save_json_dir, "w") as action_types_file:
        json_data = [
            {
                "index": item["index"],
                "count": int(item["count"]),
                "tx_0": item["tx_0"],
                "action_types": item["action_types"],
                "swap_pools": item["swap_pools"],
                "token_path": item["token_path"],
                "action_groups": item["action_groups"],
                "flash_pairs": item["flash_pairs"],
            }
            for item in action_types_sort
        ]
        action_types_file.write(json.dumps(json_data, indent=4))

    return json_data

STACK_TYPE_LABELS_LEN = 10
def sort_arbi_type_stack(collateral, df, sort_type_count, save_dir):
    # sort by date
    df_dates = [timestamp_to_date(int(item)).date() for item in list(df["timestamp"])]
    df["date"] = df_dates

    type_rank = list(sort_type_count.items())
    type_rank.sort(key=lambda x: x[1], reverse=True)
    type_rank = [x[0] for x in type_rank]

    df_arbi_type = []
    for i in df.index:
        row = df.loc[i]
        _arbi_type = row["sort_type_value"]
        df_arbi_type.append(type_rank.index(_arbi_type))
    df["arbi_type"] = df_arbi_type

    x_labes = []
    y_data = {}

    group = df.groupby(by="date")

    STACK_TYPE_LABELS = ["No.%d" % (i + 1) for i in range(STACK_TYPE_LABELS_LEN)] + ["others"]

    for g in group:
        x_labes.append(g[0])
        _y = {}
        s = 0
        for index in g[1]["arbi_type"].to_list():
            index = int(index)
            if index < STACK_TYPE_LABELS_LEN:
                _type = STACK_TYPE_LABELS[index]
            else:
                _type = "others"
            if _type not in _y:
                _y[_type] = 0
            _y[_type] += 1
            s += 1

        for label in STACK_TYPE_LABELS:
            if label not in y_data:
                y_data[label] = []
            if label in _y:
                y_data[label].append(_y[label] / s)
            else:
                y_data[label].append(0)

    stack_colors = plt.get_cmap("plasma")(np.linspace(0.8, 0.4, len(y_data.keys())))

    fig, ax = plt.subplots()
    ax.stackplot(x_labes, y_data.values(), labels=y_data.keys(), colors=stack_colors, alpha=1)
    ax.legend(loc="upper left")
    ax.set_title("Arbitrage Type (%s)" % (collateral), font={"size": 28}, pad=16)
    ax.set_xlabel("Date")
    ax.set_ylabel("count")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

    plt.subplots_adjust(left=0.1, right=1)
    plt.margins(0.1)
    fig.set_size_inches(18, 12)
    fig.savefig(save_dir, dpi=100)


def replace_split_symbol(string, old_symbol, new_symbol):
    return new_symbol.join(string.split(old_symbol))
