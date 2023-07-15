from analytics.arbitrage_statistics import (
    detailed_trades_distribution,
    detailed_trades_stat_scatter,
    draw_daily_stat,
    detialed_trades_stat_dominance,
    sort_arbi_type_stack,
)
from utils.utils import make_dir, make_or_clean_dir


if __name__ == "__main__":
    make_dir("data/img/stat/")

    for collateral in ["sfrxeth", "wsteth", "weth", "wbtc"]:
        folder_dir = "data/img/stat/%s" % (collateral)
        make_or_clean_dir(folder_dir)

        sort_arbi_type_stack(collateral)
        draw_daily_stat(collateral)
        detialed_trades_stat_dominance(collateral)
        detailed_trades_distribution(collateral)
        detailed_trades_stat_scatter(collateral)
