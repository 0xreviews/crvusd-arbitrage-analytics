import asyncio
import csv
import json
from analytics.detailed_trades import (
    generate_token_flow,
    generate_tx_summary,
    generate_txs_analytics,
    process_trades_data,
)
from collector.eigenphi.query import (
    query_eigenphi_analytics_tx,
    query_eigenphi_summary_tx,
)
from collector.eigenphi.utils import get_eigenphi_tokenflow
from utils import get_address_alias


# txs = [
#     "0x6c1424586ea485da35ca689a10bc811633773b847c7fd3a5adb2c9ca32e7abeb",
#     # "0xb8b798e09a6060852fa23f8fd5034de1f54c15716c18300a17bf50c1bb114979",
#     # "0xec221a9468969b56c77ccc8ec7b4deb05af3a678bff3797f20c37ef1cda16cfa",
#     # "0x57d2caf101319139edb554c8a998a7fe3895c8ea15eea8852ce75befc6811bdf",
# ]


def process_batch(txs, begin_index, original_data_dir=""):
    if original_data_dir == "":
        tasks = []
        for i in range(len(txs)):
            target_tx = txs[i]
            tasks.append(asyncio.ensure_future(query_eigenphi_summary_tx(target_tx)))
            tasks.append(asyncio.ensure_future(query_eigenphi_analytics_tx(target_tx)))

        results = loop.run_until_complete(asyncio.gather(*tasks))
        print("results len:", len(results))
    else:
        with open(original_data_dir, encoding="utf-8") as f:
            original_data = json.load(f)
            results = []
            for i in range(len(txs)):
                index = begin_index + i
                index = min(len(original_data)-1, index)
                item = original_data[index]
                results.append(item["summary_original"])
                results.append(item["analytics_tx_original"])

    raws = []
    lines = []
    json_lines = []
    for i in range(len(txs)):
        if results[i * 2] is None:
            summary = None
            token_prices = None
            tx_meta = None
        else:
            summary, token_prices, tx_meta = generate_tx_summary(results[i * 2])

        # save original data
        if original_data_dir == "":
            raws.append(
                {
                    "tx": txs[i],
                    "summary_original": results[i * 2],
                    "analytics_tx_original": results[i * 2 + 1],
                }
            )

        token_balance_diff, address_tags, transfers = get_eigenphi_tokenflow(
            results[i * 2 + 1]
        )

        token_flow_list = generate_token_flow(
            transfers,
            address_tags,
        )

        tokenflow_lines = generate_txs_analytics(
            summary,
            token_prices,
            tx_meta,
            token_flow_list,
        )

        lines += [[str(i + begin_index)]] + tokenflow_lines + [[], []]
        json_lines.append(
            {
                "summary": summary,
                "token_prices": token_prices,
                "tx_meta": tx_meta,
                "token_flow_list": token_flow_list,
            }
        )

    return lines, json_lines, raws


if __name__ == "__main__":
    use_original_data = True
    gql_alltrades_dir = "data/detailed_trades_data.csv"
    eigenphi_original_dir = "data/original/eigenphi_raw_data.json"

    if not use_original_data:
        loop = asyncio.get_event_loop()

        all_trades = process_trades_data(
            save=True, save_dir=gql_alltrades_dir
        )
        all_txs = [row["tx"] for row in all_trades]
    else:
        all_txs = []
        with open(gql_alltrades_dir, encoding="utf-8") as f:
            spamreader = csv.reader(f)
            for row in spamreader:
                all_txs.append(row[13])
            
            

    batch_size = 100
    data_lines = []
    json_data = []
    raws_data = []

    for i in range(len(all_txs) // batch_size + 1):
        begin_index = i * batch_size
        end_index = min(len(all_txs), (i + 1) * batch_size)
        print("process txs %d to %d" % (begin_index, end_index))
        txs = all_txs[begin_index:end_index]
        lines, json_lines, raws = process_batch(
            txs,
            begin_index,
            original_data_dir=eigenphi_original_dir if use_original_data else "",
        )
        data_lines += lines
        json_data += json_lines
        raws_data += raws

    with open(
        "data/detailed_trades_tokenflow_data.csv", "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerows(data_lines)

    with open("data/detailed_trades_tokenflow_data.json", "w") as f:
        f.write(json.dumps(json_data, indent=4))

    if not use_original_data:
        with open(eigenphi_original_dir, "w") as f:
            f.write(json.dumps(raws_data, indent=4))
