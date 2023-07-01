import asyncio
from analytics.detailed_trades_statistics import detailed_trades_distribution, detailed_trades_stat_scatter, draw_daily_stat, detialed_trades_stat_dominance
from collector.coingecko.query import query_prices_historical


async def get_prices_data():
    results = []
    for symbol in ["sfrxeth", "wsteth"]:
        raws = await query_prices_historical(token_symbol=symbol, save=True)
        results.append(raws)
    return results


if __name__ == "__main__":
    # asyncio.run(get_prices_data())
    for symbol in ["sfrxeth", "wsteth"]:
        draw_daily_stat(symbol)
        detialed_trades_stat_dominance(symbol)
        detailed_trades_distribution(symbol)
        detailed_trades_stat_scatter(symbol)

