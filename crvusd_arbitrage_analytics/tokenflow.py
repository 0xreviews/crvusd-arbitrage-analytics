import sys
import asyncio
from analytics.get_trades import fetch_analytics_data_batch, wash_analytics_data
from flowchart.generate_flowchart import draw_graph_from_string, generate_flowchart


async def main():
    argv_len = len(sys.argv)

    if argv_len <= 1:
        print("Usage:\npython crvusd_arbitrage_analytics/tokenflow.py [transactionHash] [png file save dir]")
        return
    if argv_len > 1:
        tx = sys.argv[1]
    if argv_len > 2:
        save_dot_dir = sys.argv[2]
    else:
        save_dot_dir = "%s.dot" % (tx)
    
    json_data = []

    txs = [
        {
            "transactionHash": tx,
            "blockTimestamp": 0,
        }
    ]

    # 0 fetch data
    row_datas = await fetch_analytics_data_batch(txs)
    # 1 wash data
    json_data, csv_lines = wash_analytics_data(row_datas)

    G_string = generate_flowchart(json_data[0])

    draw_graph_from_string(
        G_string,
        save_dot_dir,
        save_dot_dir.replace(".dot", ".png"),
    )


if __name__ == "__main__":
    asyncio.run(main())
