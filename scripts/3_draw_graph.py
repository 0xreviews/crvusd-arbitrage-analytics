import os
import json
from flowchart.generate_flowchart import draw_graph_from_string, generate_flowchart

action_types_txs = {}


for symbol in ["sFrxETH", "wstETH"]:
    # clean data
    old_dot_list = os.listdir("data/img/%s/dot/" % (symbol))
    old_png_list = os.listdir("data/img/%s/" % (symbol))

    for old_dot in old_dot_list:
        remove_dir = "data/img/%s/dot/%s" % (symbol, old_dot)
        if os.path.exists(remove_dir) and not os.path.isdir(remove_dir):
            os.remove(remove_dir)
    for old_png in old_png_list:
        remove_dir = "data/img/%s/%s" % (symbol, old_png)
        if os.path.exists(remove_dir) and not os.path.isdir(remove_dir):
            os.remove(remove_dir)

    with open(
        "data/detailed_trades_tokenflow_data_%s.json" % (symbol), "r"
    ) as trades_data_file:
        trades_data = json.load(trades_data_file)

        with open("data/action_types_%s.json" % (symbol)) as action_types_file:
            action_types = json.load(action_types_file)
            for i in range(len(action_types)):
                item = action_types[i]
                action_types_txs[item["tx_0"]] = {
                    "index": i,
                    "count": item["count"],
                    "tx_0": item["tx_0"],
                }

        for row in trades_data:
            if row["tx"] in action_types_txs.keys():
                action_tx_data = action_types_txs[row["tx"]]
                index = action_tx_data["index"]
                count = action_tx_data["count"]
                tx_0 = action_tx_data["tx_0"]

                G_string = generate_flowchart(row)
                draw_graph_from_string(
                    G_string,
                    save_dot_dir="data/img/%s/dot/%s_%s_%s.dot"
                    % (symbol, index, count, tx_0),
                    save_png_dir="data/img/%s/%s_%s_%s.png"
                    % (symbol, index, count, tx_0),
                )
