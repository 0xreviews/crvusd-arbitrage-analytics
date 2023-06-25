from datetime import datetime
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config.filename_config import DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR
from utils.date import str_to_timestamp, timestamp_to_date


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
    volumes = []
    gas_costs = []
    for d in counts_dates:
        profits.append(
            np.mean(
                [float(n) for n in df[df["date"] == str(d.date())]["profit"].values]
            )
        )
        volumes.append(
            np.mean(
                [
                    float(n)
                    for n in df[df["date"] == str(d.date())]["liquidate_volume"].values
                ]
            )
        )
        gas_costs.append(
            np.mean([float(n) for n in df[df["date"] == str(d.date())]["cost"].values])
        )

    return end_ts, counts_dates, counts_values, profits, volumes, gas_costs


def draw_daily_stat(symbol, data_dir=DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR):
    with open(data_dir.replace(".json", "_%s.json" % (symbol)), "r") as f:
        raws = json.load(f)
        (
            end_ts,
            counts_dates,
            counts_values,
            profits,
            volumes,
            gas_costs,
        ) = detailed_trades_stat_daily(token_symbol=symbol)

        x_ticks = []
        ticks_len = len(counts_dates)
        ticks_interval = ticks_len // 4
        for i in range(ticks_len):
            if i % ticks_interval == 0 and i < ticks_len - 1.2 * ticks_interval:
                x_ticks.append(counts_dates[i])
        x_ticks.append(counts_dates[-1])

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
            title="%s LLAMMA soft-liquidation count" % (symbol),
            y_axis_label="tx count",
            save_dir="data/original/stat_count_%s.png" % (symbol),
        )

        # profits
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=profits,
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation averange profit" % (symbol),
            y_axis_label="profit(usd)",
            save_dir="data/original/stat_profit_%s.png" % (symbol),
        )

        # volumes
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=volumes,
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation averange volume" % (symbol),
            y_axis_label="volume(crvusd)",
            save_dir="data/original/stat_volume_%s.png" % (symbol),
        )

        # gas cost
        _draw_daily_stat(
            x0_list=prices_date,
            y0_list=prices,
            x1_list=counts_dates,
            y1_list=gas_costs,
            x_ticks=x_ticks,
            title="%s LLAMMA soft-liquidation averange gas cost" % (symbol),
            y_axis_label="gas cost(usd)",
            save_dir="data/original/stat_gascost_%s.png" % (symbol),
        )


def _draw_daily_stat(
    x0_list, y0_list, x1_list, y1_list, x_ticks, title, y_axis_label, save_dir
):
    fig, ax1 = plt.subplots()

    ax1.set_title(title)
    ax1.set_xlabel(
        "date",
    )
    ax1.set_ylabel("collateral price")
    line1 = ax1.plot(
        x0_list,
        y0_list,
        alpha=0.6,
        label="collateral price",
    )

    ax2 = ax1.twinx()
    ax2.set_ylabel(y_axis_label)
    bar1 = ax2.bar(
        x1_list,
        y1_list,
        color="orange",
        alpha=0.6,
        label=y_axis_label,
    )

    plt.xticks(x_ticks)
    chart_elements = line1 + [bar1]
    ax1.legend(
        chart_elements, [l.get_label() for l in chart_elements], loc="upper left"
    )

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(18, 10)

    fig.savefig(save_dir, dpi=72)


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

    profit_data = df_profit.to_list()[:3] + [sum(df_profit.to_list()[3:])]
    profit_label = df_profit.index.to_list()[:3] + ["others"]
    profit_colors = plt.get_cmap("Blues")(np.linspace(0.7, 0.2, len(profit_data)))

    volume_data = df_volume.to_list()[:3] + [sum(df_volume.to_list()[3:])]
    volume_label = df_volume.index.to_list()[:3] + ["others"]
    volume_colors = plt.get_cmap("Blues")(np.linspace(0.7, 0.2, len(volume_data)))

    gascost_data = df_gascost.to_list()[:3] + [sum(df_gascost.to_list()[3:])]
    gascost_label = df_gascost.index.to_list()[:3] + ["others"]
    gascost_colors = plt.get_cmap("Blues")(np.linspace(0.7, 0.2, len(gascost_data)))

    plt.style.use("_mpl-gallery-nogrid")
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    patches, text, _ = ax1.pie(
        counts_data,
        colors=counts_colors,
        autopct="%.2f",
        radius=3,
        center=(4, 4),
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        frame=True,
    )
    ax1.legend(patches, labels=counts_label, loc="best")
    ax1.set_title("Tx Count Dominance")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.margins(x=0.1, y=0.3)

    patches, text, _ = ax2.pie(
        profit_data,
        colors=profit_colors,
        autopct="%.2f",
        radius=3,
        center=(4, 4),
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        frame=True,
    )
    ax2.legend(patches, labels=profit_label, loc="best")
    ax2.set_title("Profits Dominance")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.margins(x=0.1, y=0.3)

    patches, text, _ = ax3.pie(
        volume_data,
        colors=volume_colors,
        autopct="%.2f",
        radius=3,
        center=(4, 4),
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        frame=True,
    )
    ax3.legend(patches, labels=volume_label, loc="best")
    ax3.set_title("Volume Dominance")
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.margins(x=0.1, y=0.3)

    patches, text, _ = ax4.pie(
        gascost_data,
        colors=gascost_colors,
        autopct="%.2f",
        radius=3,
        center=(4, 4),
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        frame=True,
    )
    ax4.legend(patches, labels=gascost_label, loc="best")
    ax4.set_title("Gas cost Dominance")
    ax4.set_xticks([])
    ax4.set_yticks([])
    ax4.margins(x=0.1, y=0.3)

    fig.set_size_inches(18, 20)
    fig.tight_layout(pad=2)
    fig.savefig("data/original/dominance_count_%s.png" % (token_symbol), dpi=72)


def get_date_from_timestamp(ts):
    return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
