import asyncio
import json
import matplotlib.pyplot as plt
from analytics.detailed_trades_statistics import load_detialed_trades_stat_daily
from collector.coingecko.query import query_prices_historical
from utils.date import str_to_timestamp, timestamp_to_date


BEGIN_DATE = {
    "sfrxeth": "2023-05-14 12:20",
    "wsteth": "2023-06-08 01:05",
}


async def get_prices_data():
    results = []
    for symbol in ["sfrxeth", "wsteth"]:
        raws = await query_prices_historical(
            token_symbol=symbol,
            from_date=BEGIN_DATE[symbol],
            to_date="2023-06-21 23:59",
            save=True,
        )
        results.append(raws)
    return results


def draw_diagram():
    for symbol in ["sfrxeth", "wsteth"]:
        with open(
            "data/original/coingecko_prices_raw_data_%s.json" % (symbol), "r"
        ) as f:
            raws = json.load(f)
            counts = load_detialed_trades_stat_daily(token_symbol=symbol)

            counts_values = counts.to_list()
            counts_dates = list(counts.index)

            print(counts_dates)
            print(counts_values)

            fig, ax1 = plt.subplots()

            ax1.set_title("LLAMMA soft-liquidation statistics (daily count)")

            ax1.set_xlabel(
                "date",
            )
            ax1.set_ylabel("collateral price")
            ax1.plot(
                [timestamp_to_date(item[0] / 1000) for item in raws],
                [item[1] for item in raws],
                alpha=0.6,
            )
            # ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()
            ax2.set_ylabel("soft-liquidation count")
            ax2.bar(
                [
                    timestamp_to_date(str_to_timestamp(item, fmt="%Y-%m-%d"))
                    for item in counts_dates
                ],
                counts_values,
                color="orange",
                alpha=0.6,
            )

            fig.tight_layout()  # otherwise the right y-label is slightly clipped
            fig.set_size_inches(18.5, 10.5)
            # plt.show()

            fig.savefig("data/original/stat_%s.png" % (symbol), dpi=72)


if __name__ == "__main__":
    # asyncio.run(get_prices_data())
    draw_diagram()
