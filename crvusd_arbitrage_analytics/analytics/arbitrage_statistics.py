from datetime import datetime, timedelta, timezone
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from analytics.sort_trades import sort_arbitrage_data
from config.constance import TOKEN_DECIMALS
from config.filename_config import (
    DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR,
    DEFAUT_LIQUIDATIONS_GQL_DIR,
)
from utils.date import str_to_timestamp, timestamp_to_date

plt.style.use(
    os.path.join(os.path.dirname(__file__), "../config/pitayasmoothie-dark.mplstyle")
)
default_chart_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

STACK_TYPE_LEN = 10
IMG_DIR = "data/img/stat"


def load_detailed_trades_df(token_symbol):
    with open("data/json/tokenflow_data_%s.json" % (token_symbol)) as f:
        raws = json.load(f)
        begin_date = ""
        data = []

        for i in range(len(raws)):
            row = raws[i]

            timestamp = row["timestamp"]
            address_tags = row["address_tags"]
            summary = row["summary"]
            sort_type_value = row["sort_type_value"]
            liquidate_volume = float(row["liquidate_volume"])

            if summary is not None:
                profit = float(summary["profit"])
                revenue = float(summary["revenue"])
                cost = float(summary["cost"])
                is_sandwitch_victim = "PartialSandwich" in summary["types"]
            else:
                continue

            if begin_date == "":
                begin_date = get_date_from_timestamp(timestamp)

            data.append(
                {
                    "timestamp": timestamp,
                    "date": get_date_from_timestamp(timestamp),
                    "profit": profit,
                    "revenue": revenue,
                    "cost": cost,
                    "liquidate_volume": liquidate_volume,
                    "is_sandwitch_victim": is_sandwitch_victim,
                    "tx_from": address_tags["tx_from"],
                    # "arbitrage_contract": address_tags["arbitrage_contract"],
                    "sort_type_value": sort_type_value,
                    "tx": row["tx"],
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
        _profits = []
        _revenues = []
        _volumes = []
        _gascost = []
        for index in df[df["date"] == str(d.date())].index:
            # @follow-up exclude unusual losses
            row = df.loc[index]
            if float(row["revenue"]) < 0 and row["is_sandwitch_victim"]:
                _profits.append(0)
                _revenues.append(0)
            else:
                _profits.append(row["profit"])
                _revenues.append(row["revenue"])
            _volumes.append(row["liquidate_volume"])
            _gascost.append(row["cost"])

        profits.append(np.sum(_profits))
        revenues.append(np.sum(_revenues))
        volumes.append(np.sum(_volumes))
        gas_costs.append(np.sum(_gascost))

    return end_ts, counts_dates, counts_values, profits, revenues, volumes, gas_costs


def draw_daily_stat(symbol, data_dir=DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR):
    with open(data_dir.replace(".json", "_%s.json" % (symbol.lower())), "r") as f:
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

        prices_date = []
        prices = []
        end_i = len(raws)
        for i in range(len(raws)):
            if int(raws[i][0]) / 1000 >= end_ts:
                end_i = i + 1
                break
        prices_date = [timestamp_to_date(int(item[0]) / 1000) for item in raws[:end_i]]
        prices = [item[1] for item in raws[:end_i]]

        x_ticks = []
        begin_xtick = prices_date[0].date()
        end_xtick = prices_date[-1].date()
        cur_xtick = begin_xtick
        while cur_xtick <= end_xtick:
            x_ticks.append(cur_xtick)
            cur_xtick += timedelta(days=1)

        # counts
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=counts_values,
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation count daily" % (symbol),
            y_axis_label="tx count",
            save_dir="%s/%s/stat_count_%s.png" % (IMG_DIR, symbol, symbol),
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
            save_dir="%s/%s/stat_volume_%s.png" % (IMG_DIR, symbol, symbol),
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
            save_dir="%s/%s/stat_profit_%s.png" % (IMG_DIR, symbol, symbol),
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
            save_dir="%s/%s/stat_gascost_%s.png" % (IMG_DIR, symbol, symbol),
        )

        bar_datas = {
            "gas costs": [g for g in gas_costs],
            "revenue": revenues,
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
            save_dir="%s/%s/stat_daily_revenue_gascost_%s.png"
            % (IMG_DIR, symbol, symbol),
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

    # rotate the date labels
    fig.autofmt_xdate(ha='center', rotation=90)
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
    fig.savefig(
        "%s/%s/dominance_%s.png" % (IMG_DIR, token_symbol, token_symbol), dpi=100
    )


def detailed_trades_distribution(token_symbol):
    df = load_detailed_trades_df(token_symbol)

    # volume
    # range unit k
    volume_ranges = [5, 10, 20, 30, 40, 50, 100, 200]
    volume_x_labels = (
        ["0-%dk" % (volume_ranges[0])]
        + [
            "%dk-%dk" % (volume_ranges[i], volume_ranges[i + 1])
            for i in range(len(volume_ranges) - 1)
        ]
        + [">%dk" % (volume_ranges[-1])]
    )

    # revenue
    revenue_ranges = [5, 10, 20, 30, 40, 50, 100, 200, 300]
    revenue_x_labels = (
        ["0-%d" % (revenue_ranges[0])]
        + [
            "%d-%d" % (revenue_ranges[i], revenue_ranges[i + 1])
            for i in range(len(revenue_ranges) - 1)
        ]
        + [">%d" % (revenue_ranges[-1])]
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
        x_title="volume range ($)",
        y_title="count",
        x_labels=volume_x_labels,
        y_axis_label="volume distribution",
        title="%s volume distribution" % (token_symbol),
        save_dir="%s/%s/stat_hist_volume_%s.png"
        % (IMG_DIR, token_symbol, token_symbol),
    )

    _draw_distribution(
        df=df,
        df_key="revenue",
        ranges=revenue_ranges,
        x_title="revenue range ($)",
        y_title="count",
        x_labels=revenue_x_labels,
        y_axis_label="revenue distribution",
        title="%s revenue distribution" % (token_symbol),
        save_dir="%s/%s/stat_hist_revenue_%s.png"
        % (IMG_DIR, token_symbol, token_symbol),
    )

    _draw_distribution(
        df=df,
        df_key="cost",
        x_title="gascost range ($)",
        y_title="count",
        ranges=gascost_ranges,
        x_labels=gascost_x_labels,
        y_axis_label="gascost distribution",
        title="%s gascost distribution" % (token_symbol),
        save_dir="%s/%s/stat_hist_gascost_%s.png"
        % (IMG_DIR, token_symbol, token_symbol),
    )


def _draw_distribution(df, df_key, ranges, x_title, y_title, x_labels, y_axis_label, title, save_dir):
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
    ax1.set_xlabel(x_title, font={"size": 20})
    ax1.set_ylabel(y_title, font={"size": 20})
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
    save_dir = "%s/%s/stat_scatter_revenue_volume_%s.png" % (
        IMG_DIR,
        token_symbol,
        token_symbol,
    )

    x_list = df["liquidate_volume"].to_list()
    y_list = [max(y, 1) for y in df["revenue"].to_list()]
    x_max = max(x_list)

    # skip sandwitch victim
    x_list_skip_sandwitch = []
    y_list_skip_sandwitch = []
    sandwitch_victims = df["is_sandwitch_victim"].to_list()
    for i in range(len(sandwitch_victims)):
        if not sandwitch_victims[i]:
            x_list_skip_sandwitch.append(x_list[i])
            y_list_skip_sandwitch.append(y_list[i])
    
    fig, ax1 = plt.subplots()
    ax1.set_title(title, font={"size": 32}, pad=24)
    ax1.set_xlabel("soft-liquidation volume ($)", font={"size": 24})
    ax1.set_ylabel("soft-liquidation revenue ($)", font={"size": 24})

    ax1.scatter(
        x=x_list_skip_sandwitch,
        y=y_list_skip_sandwitch,
        s=[max(10, s / x_max * 3000) for s in x_list_skip_sandwitch],
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


def sort_arbi_type_stack(collateral):
    df = load_detailed_trades_df(collateral)

    # sort by date
    df_dates = [timestamp_to_date(int(item)).date() for item in list(df["timestamp"])]
    df["date"] = df_dates

    with open("data/json/tokenflow_data_%s.json" % (collateral), "r") as f:
        trades_data = json.load(f)
        arbi_type_data, sort_type_count = sort_arbitrage_data(trades_data)

    type_rank = list(sort_type_count.items())
    type_rank.sort(key=lambda x: x[1], reverse=True)
    type_rank = [x[0] for x in type_rank]

    df_arbi_type = []
    for i in df.index:
        row = df.loc[i]
        _arbi_type = row["sort_type_value"]
        df_arbi_type.append(type_rank.index(_arbi_type))
    df["arbi_type"] = df_arbi_type

    x_labes = []
    y_data = {}

    group = df.groupby(by="date")

    stack_labels = ["No.%d" % (i + 1) for i in range(STACK_TYPE_LEN)] + ["others"]

    for g in group:
        x_labes.append(g[0])
        _y = {}
        s = 0
        for index in g[1]["arbi_type"].to_list():
            index = int(index)
            if index < STACK_TYPE_LEN:
                _type = stack_labels[index]
            else:
                _type = "others"
            if _type not in _y:
                _y[_type] = 0
            _y[_type] += 1
            s += 1

        for label in stack_labels:
            if label not in y_data:
                y_data[label] = []
            if label in _y:
                y_data[label].append(_y[label] / s)
            else:
                y_data[label].append(0)

    stack_colors = plt.get_cmap("plasma")(np.linspace(0.8, 0.4, len(y_data.keys())))

    fig, ax = plt.subplots()
    ax.stackplot(
        x_labes, y_data.values(), labels=y_data.keys(), colors=stack_colors, alpha=1
    )
    ax.legend(loc="upper left")
    ax.set_title("Arbitrage Type (%s)" % (collateral), font={"size": 28}, pad=16)
    ax.set_xlabel("Date")
    ax.set_ylabel("count")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

    plt.subplots_adjust(left=0.1, right=1)
    plt.margins(0.1)
    fig.set_size_inches(18, 12)
    fig.savefig(
        "data/img/stat/%s/arbi_types_stack_%s.png" % (collateral, collateral), dpi=100
    )


def load_liquidations_df(token_symbol):
    with open(
        DEFAUT_LIQUIDATIONS_GQL_DIR.replace(".json", "_%s.json" % (token_symbol))
    ) as f:
        raws = json.load(f)
        begin_date = ""
        data = []

        for i in range(len(raws)):
            row = raws[i]

            timestamp = row["blockTimestamp"]
            debt = float(row["debt"]) / 10**TOKEN_DECIMALS["crvusd"]
            collateral_received = float(row["collateralReceived"]) / 10**TOKEN_DECIMALS[token_symbol.lower()]
            stablecoin_received = float(row["stablecoinReceived"]) / 10**TOKEN_DECIMALS["crvusd"]

            user = row["user"]["id"]
            liquidator = row["liquidator"]["id"]

            if begin_date == "":
                begin_date = get_date_from_timestamp(timestamp)

            data.append(
                {
                    "timestamp": timestamp,
                    "date": get_date_from_timestamp(timestamp),
                    "debt": debt,
                    "collateral_received": collateral_received,
                    "stablecoin_received": stablecoin_received,
                    "block_number": row["blockNumber"],
                    "tx": row["transactionHash"],
                }
            )

        df = pd.DataFrame(data)

        return df


def liquidations_stat_daily(token_symbol):
    df = load_liquidations_df(token_symbol)
    end_ts = int(df["timestamp"].sort_index().to_list()[-1])

    # counts
    counts = df["date"].value_counts().sort_index()
    counts_dates = [
        timestamp_to_date(str_to_timestamp(item, fmt="%Y-%m-%d"))
        for item in list(counts.index)
    ]
    counts_values = counts.to_list()

    debts = []
    collateral_receiveds = []
    stablecoin_receiveds = []
    for d in counts_dates:
        _debts = []
        _collateral_receiveds = []
        _stablecoin_receiveds = []
        for index in df[df["date"] == str(d.date())].index:
            row = df.loc[index]
            _debts.append(row["debt"])
            _collateral_receiveds.append(row["collateral_received"])
            _stablecoin_receiveds.append(row["stablecoin_received"])

        debts.append(np.sum(_debts))
        collateral_receiveds.append(np.sum(_collateral_receiveds))
        stablecoin_receiveds.append(np.sum(_stablecoin_receiveds))

    return (
        end_ts,
        counts_dates,
        counts_values,
        debts,
        collateral_receiveds,
        stablecoin_receiveds,
    )


def draw_daily_liquidations(symbol, data_dir=DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR):
    with open(data_dir.replace(".json", "_%s.json" % (symbol.lower())), "r") as f:
        raws = json.load(f)
        (
            end_ts,
            counts_dates,
            counts_values,
            debts,
            collateral_receiveds,
            stablecoin_receiveds,
        ) = liquidations_stat_daily(token_symbol=symbol)

        prices_date = []
        prices = []
        end_i = len(raws)
        for i in range(len(raws)):
            if int(raws[i][0]) / 1000 >= end_ts:
                end_i = i + 1
                break
        prices_date = [timestamp_to_date(int(item[0]) / 1000) for item in raws[:end_i]]
        prices = [item[1] for item in raws[:end_i]]

        x_ticks = []
        begin_xtick = prices_date[0].date()
        end_xtick = prices_date[-1].date()
        cur_xtick = begin_xtick
        while cur_xtick <= end_xtick:
            x_ticks.append(cur_xtick)
            cur_xtick += timedelta(days=1)

        # counts
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=counts_values,
            x_ticks=x_ticks,
            title="%s Controller hard-liquidation count daily" % (symbol),
            y_axis_label="tx count",
            save_dir="%s/%s/liquidations_count_%s.png" % (IMG_DIR, symbol, symbol),
        )

        # calculate debt and collateral received
        received_usds = []
        profit_rates = []
        for i in range(len(counts_dates)):
            for j in range(len(prices_date)):
                if counts_dates[i].date() == prices_date[j].date():
                    _price = prices[j]
                    _received_usd = (
                        stablecoin_receiveds[i] + _price * collateral_receiveds[i]
                    )
                    received_usds.append(_received_usd)
                    profit_rates.append(_received_usd / debts[i] - 1)
                    break

        # # profit_rates
        # _draw_daily_stat(
        #     x0_list=prices_date,
        #     y0_list=prices,
        #     x1_list=counts_dates,
        #     y1_list=profit_rates,
        #     x_ticks=x_ticks,
        #     title="%s Controller hard-liquidation profit rate daily" % (symbol),
        #     y_axis_label="profit rate",
        #     save_dir="%s/%s/liquidations_profitrate_%s.png" % (IMG_DIR, symbol, symbol),
        # )

        bar_datas = {
            "debt": debts,
            "collateral received($)": received_usds,
        }

        _draw_daily_bars_multi(
            bar_x=counts_dates,
            bar_datas=bar_datas,
            x1_list=prices_date,
            y1_list=prices,
            y0_axis_label="debt($)",
            y1_axis_label="%s price" % (symbol),
            x_ticks=x_ticks,
            title="%s Controller hard-liquidation debt and collateral received daily"
            % (symbol),
            save_dir="%s/%s/liquidations_daily_debt_received_%s.png"
            % (IMG_DIR, symbol, symbol),
        )


def get_date_from_timestamp(ts):
    return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d")
