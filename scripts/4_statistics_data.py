from analytics.detailed_trades_statistics import (
    detailed_trades_distribution,
    detailed_trades_stat_scatter,
    draw_daily_stat,
    detialed_trades_stat_dominance,
)


if __name__ == "__main__":
    for symbol in ["sfrxeth", "wsteth"]:
        draw_daily_stat(symbol)
        detialed_trades_stat_dominance(symbol)
        detailed_trades_distribution(symbol)
        detailed_trades_stat_scatter(symbol)
