import json
import os
import pandas as pd

from analytics.sort_trades import (
    sort_arbi_type,
    sort_arbitrage_data,
)


def sort_data():
    for collateral in ["sFrxETH", "wstETH", "WETH", "WBTC"]:
        with open("data/json/tokenflow_data_%s.json" % (collateral), "r") as f:
            trades_data = json.load(f)
            arbi_type_data, sort_type_count = sort_arbitrage_data(trades_data)

            df = pd.DataFrame(arbi_type_data)

            # sort by arbitrage type
            arbi_type_data = sort_arbi_type(
                df,
                save_csv_dir="data/csv/arbi_types_%s.csv" % (collateral),
                save_json_dir="data/json/arbi_types_%s.json" % (collateral),
            )


if __name__ == "__main__":
    sort_data()
