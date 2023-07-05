import json
import pandas as pd

from analytics.sort_trades import (
    SPLIT_SYMBOL,
    sort_arbi_type,
    sort_arbi_type_stack,
    sort_arbitrage_data,
)
from utils.date import str_to_timestamp, timestamp_to_date


def sort_data():
    for collateral in ["sFrxETH", "wstETH"]:
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

            sort_arbi_type_stack(
                df,
                arbi_type_data,
                save_dir="data/img/%s/arbitrage_types_stack.png" % (collateral),
            )


if __name__ == "__main__":
    sort_data()
