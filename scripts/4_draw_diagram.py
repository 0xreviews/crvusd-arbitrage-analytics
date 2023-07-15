import os
import json
from flowchart.generate_flowchart import draw_graph_from_string, generate_flowchart
from utils.utils import make_or_clean_dir


def main():
    for symbol in ["sFrxETH", "wstETH", "WETH", "WBTC"]:
        dot_dir = "data/img/%s/dot/" % (symbol)
        png_dir = "data/img/%s/" % (symbol)

        make_or_clean_dir(dot_dir)
        make_or_clean_dir(png_dir)

        with open(
            "data/json/tokenflow_data_%s.json" % (symbol), "r"
        ) as trades_data_file:
            trades_data = json.load(trades_data_file)
            trades_data_len = len(trades_data)

            with open("data/json/arbi_types_%s.json" % (symbol)) as arbi_types_file:
                arbi_types = json.load(arbi_types_file)[:10]
                arbi_types_txs = {}
                for i in range(len(arbi_types)):
                    item = arbi_types[i]
                    arbi_types_txs[item["tx_0"]] = {
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

                if row["tx"] in arbi_types_txs.keys():
                    arbi_tx_data = arbi_types_txs[row["tx"]]
                    index = arbi_tx_data["index"]
                    count = arbi_tx_data["count"]
                    tx_0 = arbi_tx_data["tx_0"]

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
