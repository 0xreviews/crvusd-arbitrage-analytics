from datetime import datetime
import json
import pandas as pd


def load_detialed_trades_stat_daily(token_symbol="sfrxeth"):
    with open("data/detailed_trades_tokenflow_data_%s.json" % (token_symbol)) as f:
        raws = json.load(f)

        begin_date = ""

        data = []

        for i in range(len(raws)):
            row = raws[i]

            timestamp = row["timestamp"]
            summary = row["summary"]
            if summary is not None:
                profit = summary["profit"]
                revenue = summary["revenue"]
                cost = summary["cost"]

                if begin_date == "":
                    begin_date = get_date_from_timestamp(timestamp)

                data.append(
                    {
                        "timestamp": timestamp,
                        "date": get_date_from_timestamp(timestamp),
                        "profit": profit,
                        "revenue": revenue,
                        "cost": cost,
                    }
                )

        df = pd.DataFrame(data)

        counts = df["date"].value_counts().sort_index()

    return counts


def get_date_from_timestamp(ts):
    return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
