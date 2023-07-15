import os
import json
from flowchart.generate_flowchart import draw_graph_from_string, generate_flowchart


def main():
    for symbol in ["sFrxETH", "wstETH", "WETH", "WBTC"]:
        dot_dir = "data/img/%s/dot/" % (symbol)
        png_dir = "data/img/%s/" % (symbol)

        if not os.path.exists(dot_dir):
            os.mkdir(dot_dir)
        if not os.path.exists(png_dir):
            os.mkdir(png_dir)

        # clean data
        old_dot_list = os.listdir(dot_dir)
        old_png_list = os.listdir(png_dir)

        for old_dot in old_dot_list:
            remove_dir = dot_dir + old_dot
            if os.path.exists(remove_dir) and not os.path.isdir(remove_dir):
                os.remove(remove_dir)
        for old_png in old_png_list:
            remove_dir = png_dir + old_png
            if os.path.exists(remove_dir) and not os.path.isdir(remove_dir):
                os.remove(remove_dir)

        with open(
            "data/detailed_trades_tokenflow_data_%s.json" % (symbol), "r"
        ) as trades_data_file:
            trades_data = json.load(trades_data_file)
            trades_data_len = len(trades_data)

            with open("data/action_types_%s.json" % (symbol)) as action_types_file:
                action_types = json.load(action_types_file)[:10]
                action_types_txs = {}
                for i in range(len(action_types)):
                    item = action_types[i]
                    action_types_txs[item["tx_0"]] = {
                        "index": i,
                        "count": item["count"],
                        "tx_0": item["tx_0"],
                    }

            for row in trades_data:
                # # @follow-up
                # if (
                #     row["tx"]
                #     != "0x0aca86ee49f770a199881150e27933d2ec34674b6eadca3d1de7bb99036bf6a7"
                # ):
                #     continue

                if row["tx"] in action_types_txs.keys():
                    action_tx_data = action_types_txs[row["tx"]]
                    index = action_tx_data["index"]
                    count = action_tx_data["count"]
                    tx_0 = action_tx_data["tx_0"]

                    G_string = generate_flowchart(
                        row,
                        title="LLAMMA(%s) Soft-Liquidation Tokenflow No.%d Proportion %.2f%% \n\n" % (
                            symbol, index + 1, count / trades_data_len * 100
                        ),
                    )
                    draw_graph_from_string(
                        G_string,
                        save_dot_dir="data/img/%s/dot/%s_%s_%s.dot"
                        % (symbol, index, count, tx_0),
                        save_png_dir="data/img/%s/%s_%s_%s.png"
                        % (symbol, index, count, tx_0),
                    )


if __name__ == "__main__":
    main()
