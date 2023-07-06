from datetime import datetime, timedelta
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config.filename_config import DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR
from utils.date import str_to_timestamp, timestamp_to_date

plt.style.use(
    os.path.join(os.path.dirname(__file__), "../config/pitayasmoothie-dark.mplstyle")
)
default_chart_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


def load_detailed_trades_df(token_symbol):
    with open("data/detailed_trades_tokenflow_data_%s.json" % (token_symbol)) as f:
        raws = json.load(f)
        begin_date = ""
        data = []

        for i in range(len(raws)):
            row = raws[i]

            timestamp = row["timestamp"]
            address_tags = row["address_tags"]
            summary = row["summary"]
            liquidate_volume = float(row["liquidate_volume"])

            if summary is not None:
                profit = float(summary["profit"])
                revenue = float(summary["revenue"])
                cost = float(summary["cost"])

                if begin_date == "":
                    begin_date = get_date_from_timestamp(timestamp)

                data.append(
                    {
                        "timestamp": timestamp,
                        "date": get_date_from_timestamp(timestamp),
                        "tx_from": address_tags["tx_from"],
                        "arbitrage_contract": address_tags["arbitrage_contract"],
                        "profit": profit,
                        "revenue": revenue,
                        "cost": cost,
                        "liquidate_volume": liquidate_volume,
                    }
                )

        df = pd.DataFrame(data)

        return df


def detailed_trades_stat_daily(token_symbol):
    df = load_detailed_trades_df(token_symbol)
    end_ts = int(df["timestamp"].sort_index().to_list()[-1])

    # counts
    counts = df["date"].value_counts().sort_index()
    counts_dates = [
        timestamp_to_date(str_to_timestamp(item, fmt="%Y-%m-%d"))
        for item in list(counts.index)
    ]
    counts_values = counts.to_list()

    # profits, volume(crvusd), gas cost (usd)
    profits = []
    revenues = []
    volumes = []
    gas_costs = []
    for d in counts_dates:
        profits.append(
            np.sum([float(n) for n in df[df["date"] == str(d.date())]["profit"].values])
        )
        revenues.append(
            np.sum(
                [float(n) for n in df[df["date"] == str(d.date())]["revenue"].values]
            )
        )
        volumes.append(
            np.sum(
                [
                    float(n)
                    for n in df[df["date"] == str(d.date())]["liquidate_volume"].values
                ]
            )
        )
        gas_costs.append(
            np.sum([float(n) for n in df[df["date"] == str(d.date())]["cost"].values])
        )

    return end_ts, counts_dates, counts_values, profits, revenues, volumes, gas_costs


def draw_daily_stat(symbol, data_dir=DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR):
    with open(data_dir.replace(".json", "_%s.json" % (symbol)), "r") as f:
        raws = json.load(f)
        (
            end_ts,
            counts_dates,
            counts_values,
            profits,
            revenues,
            volumes,
            gas_costs,
        ) = detailed_trades_stat_daily(token_symbol=symbol)

        x_ticks = []
        begin_xtick = counts_dates[0]
        end_xtick = counts_dates[-1]
        cur_xtick = begin_xtick
        while cur_xtick <= end_xtick:
            x_ticks.append(cur_xtick)
            cur_xtick += timedelta(days=1)
        x_ticks = [str(d.date()) for d in x_ticks]

        prices_date = []
        prices = []
        for i in range(len(raws)):
            if int(raws[i][0]) / 1000 >= end_ts:
                prices_date = [
                    timestamp_to_date(int(item[0]) / 1000) for item in raws[: i + 1]
                ]
                prices = [item[1] for item in raws[: i + 1]]
                break

        # counts
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=counts_values,
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation count daily" % (symbol),
            y_axis_label="tx count",
            save_dir="data/img/stat_count_%s.png" % (symbol),
        )

        # volumes
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=volumes,
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation volume daily" % (symbol),
            y_axis_label="volume(crvusd)",
            save_dir="data/img/stat_volume_%s.png" % (symbol),
        )

        # profits
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=profits,
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation profit daily" % (symbol),
            y_axis_label="profit($)",
            save_dir="data/img/stat_profit_%s.png" % (symbol),
        )

        # gas cost
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=gas_costs,
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation gas cost daily" % (symbol),
            y_axis_label="gas cost($)",
            save_dir="data/img/stat_gascost_%s.png" % (symbol),
        )

        bar_datas = {
            "gas costs": [g for g in gas_costs],
            "revenue": revenues,
            # "tx counts": counts_values,
            # "volumes": volumes,
        }

        _draw_daily_bars_multi(
            bar_x=counts_dates,
            bar_datas=bar_datas,
            x1_list=prices_date,
            y1_list=prices,
            y0_axis_label="gas cost and revenue($)",
            y1_axis_label="collateral price($)",
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation gas cost and revenue daily" % (symbol),
            save_dir="data/img/stat_daily_revenue_gascost_%s.png" % (symbol),
        )


def _draw_daily_bars_multi(
    bar_x,
    bar_datas,
    x1_list,
    y1_list,
    x_ticks,
    y0_axis_label,
    y1_axis_label,
    title,
    save_dir,
):
    fig, ax1 = plt.subplots()

    ax1.set_title(title, font={"size": 32}, pad=24)
    ax1.set_xlabel("date", font={"size": 24})
    ax1.set_ylabel(y0_axis_label, font={"size": 18})

    ax2 = ax1.twinx()

    line1 = ax2.plot(
        x1_list,
        y1_list,
        alpha=0.8,
        label=y1_axis_label,
        color=default_chart_colors[2],
    )
    ax2.set_ylabel(y1_axis_label, font={"size": 18})

    multiplier = 0
    bar_width = timedelta(hours=7)
    bars = []

    for attribute, values in bar_datas.items():
        offset = (bar_width) * multiplier - bar_width * 0.5
        _bar = ax1.bar(
            [x + offset for x in bar_x],
            values,
            bar_width,
            label=attribute,
            alpha=0.8,
            # bottom=gas_bottom if attribute == "gas costs" else profits_bottom,
        )
        # ax1.bar_label(
        #     _bar,
        #     padding=5,
        #     font={"size": 10},
        #     fmt="{:,.2f}",
        # )
        bars.append(_bar)
        multiplier += 1

    # plt.xticks(x_ticks, font={"size": 16}, rotation=70)
    plt.xticks(x_ticks, font={"size": 13}, rotation=90)
    ax1.set_xticklabels(x_ticks, rotation=90)
    chart_elements = line1 + bars
    ax1.legend(
        chart_elements,
        [l.get_label() for l in chart_elements],
        loc="upper left",
        prop={"size": 16},
    )
    ax1.grid(False)

    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.subplots_adjust(left=0.06, right=0.94)
    fig.set_size_inches(18, 12)

    fig.savefig(save_dir, dpi=100)


def _draw_daily_stat(
    x0_list,
    y0_list,
    x1_list,
    y1_list,
    x_ticks,
    title,
    y_axis_label,
    save_dir,
):
    bar_width = timedelta(hours=12)
    fig, ax1 = plt.subplots()

    ax1.set_title(title, font={"size": 32}, pad=24)
    ax1.set_xlabel("date", font={"size": 24})
    ax1.set_ylabel("collateral price", font={"size": 24})
    ax1.grid(False)
    ax2 = ax1.twinx()

    line1 = ax2.plot(
        x0_list,
        y0_list,
        color=default_chart_colors[1],
        alpha=0.6,
        label="collateral price",
    )

    bar1 = ax1.bar(
        x1_list,
        y1_list,
        width=bar_width,
        alpha=0.7,
        label=y_axis_label,
    )
    ax1.set_ylabel(y_axis_label, font={"size": 24})

    plt.xticks(x_ticks, font={"size": 12}, rotation=90)
    ax1.set_xticklabels(x_ticks, font={"size": 13}, rotation=90)
    plt.subplots_adjust(left=0.05, right=0.95)
    chart_elements = line1 + [bar1]
    ax1.legend(
        chart_elements,
        [l.get_label() for l in chart_elements],
        loc="upper left",
        prop={"size": 16},
    )

    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(18, 10)

    fig.savefig(save_dir, dpi=100)


def detialed_trades_stat_dominance(token_symbol):
    df = load_detailed_trades_df(token_symbol)
    df_count = (
        df.groupby(by="tx_from")["timestamp"].count().sort_values(ascending=False)
    )
    df_profit = df.groupby(by="tx_from")["profit"].sum().sort_values(ascending=False)
    df_volume = (
        df.groupby(by="tx_from")["liquidate_volume"].sum().sort_values(ascending=False)
    )
    df_gascost = df.groupby(by="tx_from")["cost"].sum().sort_values(ascending=False)

    counts_data = df_count.to_list()[:3] + [sum(df_count.to_list()[3:])]
    counts_label = df_count.index.to_list()[:3] + ["others"]
    counts_colors = plt.get_cmap("Reds")(np.linspace(0.7, 0.2, len(counts_data)))

    profit_data = df_profit.to_list()[:3] + [
        sum([max(p, 0) for p in df_profit.to_list()[3:]])
    ]
    profit_label = df_profit.index.to_list()[:3] + ["others"]
    profit_colors = plt.get_cmap("Blues")(np.linspace(0.7, 0.2, len(profit_data)))

    volume_data = df_volume.to_list()[:3] + [sum(df_volume.to_list()[3:])]
    volume_label = df_volume.index.to_list()[:3] + ["others"]
    volume_colors = plt.get_cmap("Greens")(np.linspace(0.7, 0.2, len(volume_data)))

    gascost_data = df_gascost.to_list()[:3] + [sum(df_gascost.to_list()[3:])]
    gascost_label = df_gascost.index.to_list()[:3] + ["others"]
    gascost_colors = plt.get_cmap("Purples")(np.linspace(0.7, 0.2, len(gascost_data)))

    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    textprops = {"font": {"size": 16}}
    legend_cf = {
        "loc": "upper center",
        "prop": {"size": 18},
    }

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    patches, text, _ = ax1.pie(
        x=counts_data,
        colors=counts_colors,
        autopct="%.2f%%",
        pctdistance=1.2,
        radius=3,
        center=(4, 4),
        wedgeprops=wedgeprops,
        textprops=textprops,
        frame=True,
    )
    ax1.legend(
        handles=patches,
        labels=counts_label,
        loc=legend_cf["loc"],
        prop=legend_cf["prop"],
    )
    ax1.set_title("%s Tx Count Dominance" % (token_symbol), font={"size": 28}, pad=16)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.margins(x=0.1, y=0.5)

    patches, text, _ = ax2.pie(
        x=profit_data,
        colors=profit_colors,
        autopct="%.2f%%",
        pctdistance=1.2,
        radius=3,
        center=(4, 4),
        wedgeprops=wedgeprops,
        textprops=textprops,
        frame=True,
    )
    ax2.legend(
        handles=patches,
        labels=profit_label,
        loc=legend_cf["loc"],
        prop=legend_cf["prop"],
    )
    ax2.set_title("%s Profits Dominance" % (token_symbol), font={"size": 28}, pad=16)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.margins(x=0.1, y=0.5)

    patches, text, _ = ax3.pie(
        x=volume_data,
        colors=volume_colors,
        autopct="%.2f%%",
        pctdistance=1.2,
        radius=3,
        center=(4, 4),
        wedgeprops=wedgeprops,
        textprops=textprops,
        frame=True,
    )
    ax3.legend(
        handles=patches,
        labels=volume_label,
        loc=legend_cf["loc"],
        prop=legend_cf["prop"],
    )
    ax3.set_title("%s Volume Dominance" % (token_symbol), font={"size": 28}, pad=16)
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.margins(x=0.1, y=0.5)

    patches, text, _ = ax4.pie(
        x=gascost_data,
        colors=gascost_colors,
        autopct="%.2f%%",
        pctdistance=1.2,
        radius=3,
        center=(4, 4),
        wedgeprops=wedgeprops,
        textprops=textprops,
        frame=True,
    )
    ax4.legend(
        handles=patches,
        labels=gascost_label,
        loc=legend_cf["loc"],
        prop=legend_cf["prop"],
    )
    ax4.set_title("%s Gas cost Dominance" % (token_symbol), font={"size": 28}, pad=16)
    ax4.set_xticks([])
    ax4.set_yticks([])
    ax4.margins(x=0.1, y=0.5)

    fig.set_size_inches(18, 22)
    fig.tight_layout(pad=2)
    fig.savefig("data/img/dominance_%s.png" % (token_symbol), dpi=100)


def detailed_trades_distribution(token_symbol):
    df = load_detailed_trades_df(token_symbol)

    # volume
    # range unit k
    volume_ranges = [5, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
    volume_x_labels = (
        ["0-%dk" % (volume_ranges[0])]
        + [
            "%dk-%dk" % (volume_ranges[i], volume_ranges[i + 1])
            for i in range(len(volume_ranges) - 1)
        ]
        + [">%dk" % (volume_ranges[-1])]
    )

    # volume
    revenue_ranges = [5, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
    revenue_x_labels = (
        ["0-%d" % (revenue_ranges[0])]
        + [
            "%d-%d" % (revenue_ranges[i], revenue_ranges[i + 1])
            for i in range(len(revenue_ranges) - 1)
        ]
        + [">%d" % (volume_ranges[-1])]
    )

    # gascost
    gascost_ranges = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    gascost_x_labels = (
        ["0-%d" % (gascost_ranges[0])]
        + [
            "%d-%d" % (gascost_ranges[i], gascost_ranges[i + 1])
            for i in range(len(gascost_ranges) - 1)
        ]
        + [">%d" % (gascost_ranges[-1])]
    )

    _draw_distribution(
        df=df,
        df_key="liquidate_volume",
        ranges=[r * 1000 for r in volume_ranges],
        x_labels=volume_x_labels,
        y_axis_label="volume distribution",
        title="%s volume distribution" % (token_symbol),
        save_dir="data/img/stat_hist_volume_%s.png" % (token_symbol),
    )

    _draw_distribution(
        df=df,
        df_key="revenue",
        ranges=revenue_ranges,
        x_labels=revenue_x_labels,
        y_axis_label="revenue distribution",
        title="%s revenue distribution" % (token_symbol),
        save_dir="data/img/stat_hist_revenue_%s.png" % (token_symbol),
    )

    _draw_distribution(
        df=df,
        df_key="cost",
        ranges=gascost_ranges,
        x_labels=gascost_x_labels,
        y_axis_label="gascost distribution",
        title="%s gascost distribution" % (token_symbol),
        save_dir="data/img/stat_hist_gascost_%s.png" % (token_symbol),
    )


def _draw_distribution(df, df_key, ranges, x_labels, y_axis_label, title, save_dir):
    # liquidate_volume
    tmp_count = 0
    distributions = []
    for r in ranges:
        count = df[df[df_key] < r][df_key].count()
        count -= tmp_count
        distributions.append(count)
        tmp_count += count

    distributions.append(df[df_key].count() - tmp_count)

    fig, ax1 = plt.subplots()

    ax1.set_title(title, font={"size": 32}, pad=24)
    ax1.set_xlabel("range", font={"size": 24})
    ax1.set_xticklabels(x_labels, font={"size": 16})

    _bar = ax1.bar(
        x_labels,
        distributions,
        alpha=0.7,
        label=y_axis_label,
    )
    ax1.bar_label(
        _bar,
        padding=5,
        font={"size": 12},
    )

    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.subplots_adjust(left=0.05, right=0.95)
    fig.set_size_inches(12, 10)
    fig.savefig(save_dir, dpi=100)


def detailed_trades_stat_scatter(token_symbol):
    df = load_detailed_trades_df(token_symbol)
    title = "%s revenue-volume scatter" % (token_symbol)
    save_dir = "data/img/stat_scatter_revenue_volume_%s.png" % (token_symbol)

    x_list = df["liquidate_volume"].to_list()
    y_list = df["revenue"].to_list()
    x_max = max(x_list)

    fig, ax1 = plt.subplots()
    ax1.set_title(title, font={"size": 32}, pad=24)
    ax1.set_xlabel("soft-liquidation volume", font={"size": 24})
    ax1.set_ylabel("soft-liquidation revenue", font={"size": 24})

    ax1.scatter(
        x=x_list,
        y=y_list,
        s=[max(10, s / x_max * 3000) for s in x_list],
        alpha=0.65,
        color=default_chart_colors[1],
        edgecolors=default_chart_colors[5],
        linewidths=0.7,
    )
    ax1.set_yscale("log")
    ax1.set_xscale("log")

    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.subplots_adjust(left=0.1, right=0.9)
    plt.margins(0.2)
    fig.set_size_inches(12, 12)
    fig.savefig(save_dir, dpi=100)


def get_date_from_timestamp(ts):
    return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
