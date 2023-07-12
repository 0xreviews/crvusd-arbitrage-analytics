import json
import os
import pandas as pd

from analytics.sort_trades import (
    sort_arbi_type,
    sort_arbi_type_stack,
    sort_arbitrage_data,
)


def sort_data():
    for collateral in ["sFrxETH", "wstETH", "WETH", "WBTC"]:
        with open(
            "data/detailed_trades_tokenflow_data_%s.json" % (collateral), "r"
        ) as f:
            trades_data = json.load(f)
            arbi_type_data = sort_arbitrage_data(trades_data)

            df = pd.DataFrame(arbi_type_data)

            # sort by arbitrage type
            arbi_type_data = sort_arbi_type(
                df,
                save_csv_dir="data/action_types_%s.csv" % (collateral),
                save_json_dir="data/action_types_%s.json" % (collateral),
            )

            folder_dir = "data/img/%s" % (collateral)
            if not os.path.exists(folder_dir):
                os.mkdir(folder_dir)

            sort_arbi_type_stack(
                df,
                arbi_type_data,
                save_dir=folder_dir + "/arbitrage_types_stack.png",
            )


if __name__ == "__main__":
    sort_data()
