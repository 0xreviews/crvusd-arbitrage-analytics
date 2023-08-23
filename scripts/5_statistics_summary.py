from datetime import datetime, timedelta
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from analytics.get_trades import get_trades_data
from analytics.sort_trades import sort_arbitrage_data
from config.filename_config import DEFAUT_LIQUIDATIONS_GQL_DIR, DEFAUT_TRADES_GQL_DIR

from utils.date import str_to_timestamp, timestamp_to_date

plt.style.use(
    os.path.join(
        os.path.dirname(__file__),
        "../crvusd_arbitrage_analytics/config/pitayasmoothie-dark.mplstyle",
    )
)
default_chart_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


def stat_summary_soft():
    counts = {}
    volumes = {}
    days = {}
    for collateral in ["sfrxETH", "wstETH", "WBTC", "WETH"]:
        gql_data_dir = DEFAUT_TRADES_GQL_DIR.replace(".json", "_%s.json" % (collateral))
        with open(gql_data_dir, "r") as json_file:
            all_trades = json.load(json_file)
            print(collateral, " gql data len:", len(all_trades))
            counts[collateral] = len(all_trades)
            volumes[collateral] = [getTradeVolume(item) for item in all_trades]
            delta_seconds = int(all_trades[-1]["blockTimestamp"]) - int(all_trades[0]["blockTimestamp"])
            dt = timedelta(seconds=delta_seconds)
            days[collateral] = dt.days + dt.seconds / (24 * 60 * 60)

    bar_width = 0.3
    species = counts.keys()
    x = np.arange(len(species))  # the label locations
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    rects1 = ax1.bar(
        x,
        [
            sum(volume) / days[collateral]
            for collateral, volume in volumes.items()
        ],
        width=bar_width,
        label="volume",
        color=default_chart_colors[1],
    )
    ax1.bar_label(rects1, fmt="%.2f", padding=5, font={"size": 12})
    rects2 = ax2.bar(
        x + 0.4,
        [count / days[collateral] for collateral, count in counts.items()],
        width=bar_width,
        label="count",
        color=default_chart_colors[0],
    )
    ax2.bar_label(rects2, fmt="%.2f", label_type="center", padding=5, font={"size": 12})

    ax2.grid(False)

    ax1.set_title(
        "Average Daily Volume and Count (Soft-Liquidation)", font={"size": 16}, pad=16
    )
    ax1.set_xticks(x + bar_width, species)
    chart_elements = [rects1, rects2]
    ax1.legend(
        chart_elements,
        [l.get_label() for l in chart_elements],
        loc="upper right",
        prop={"size": 12},
    )

    # plt.show()
    fig.savefig("data/img/stat/stat_summary_soft.png", dpi=100)


def stat_summary_hard():
    counts = {}
    volumes = {}
    days = {}
    for collateral in ["sfrxETH", "wstETH", "WBTC", "WETH"]:
        gql_data_dir = DEFAUT_LIQUIDATIONS_GQL_DIR.replace(
            ".json", "_%s.json" % (collateral)
        )
        with open(gql_data_dir, "r") as json_file:
            all_trades = json.load(json_file)
            print(collateral, " gql data len:", len(all_trades))
            counts[collateral] = len(all_trades)
            volumes[collateral] = [
                float(item["stablecoinReceived"]) / 1e18 for item in all_trades
            ]
            delta_seconds = int(all_trades[-1]["blockTimestamp"]) - int(all_trades[0]["blockTimestamp"])
            dt = timedelta(seconds=delta_seconds)
            days[collateral] =  dt.days + dt.seconds / (24 * 60 * 60)

    bar_width = 0.3
    species = counts.keys()
    x = np.arange(len(species))  # the label locations
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    rects1 = ax1.bar(
        x,
        [sum(volume) / days[collateral] for collateral, volume in volumes.items()],
        width=bar_width,
        label="volume",
        color=default_chart_colors[1],
    )
    ax1.bar_label(rects1, fmt="%.2f", padding=5, font={"size": 12})
    rects2 = ax2.bar(
        x + 0.4,
        [count / days[collateral] for collateral, count in counts.items()],
        width=bar_width,
        label="count",
        color=default_chart_colors[0],
    )
    ax2.bar_label(rects2, fmt="%.2f", label_type="center", padding=5, font={"size": 12})

    ax2.grid(False)

    ax1.set_title(
        "Average Daily Volume and Count (Hard-Liquidation)", font={"size": 16}, pad=16
    )
    ax1.set_xticks(x + bar_width, species)
    chart_elements = [rects1, rects2]
    ax1.legend(
        chart_elements,
        [l.get_label() for l in chart_elements],
        loc="upper right",
        prop={"size": 12},
    )

    # plt.show()
    fig.savefig("data/img/stat/stat_summary_hard.png", dpi=100)


def getTradeVolume(item):
    if item["soldId"] == "1":
        volume = float(item["tokensBought"]) / 1e18
    else:
        volume = float(item["tokensSold"]) / 1e18
    return volume


if __name__ == "__main__":
    stat_summary_soft()
    stat_summary_hard()
