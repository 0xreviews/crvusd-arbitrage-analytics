import json
import sys
import asyncio

from analytics.detailed_trades import fetch_analytics_data_batch, wash_analytics_data
from config.filename_config import DEFAULT_EIGENPHI_TX_RAW_DIR
from flowchart.generate_flowchart import draw_graph_from_string, generate_flowchart
from network.http import HTTP


async def main():
    (_, tx, save_dot_dir) = sys.argv
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
