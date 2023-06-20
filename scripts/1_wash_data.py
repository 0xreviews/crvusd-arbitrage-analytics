import csv
import json
from analytics.detailed_trades import wash_analytics_data
from config.filename_config import (
    DEFAULT_EIGENPHI_TX_RAW_DIR,
    DEFAUT_TRADES_TOKENFLOW_DATA_DIR,
)


if __name__ == "__main__":
    for collateral in ["sFrxETH", "wstETH"]:
        json_data, csv_lines = wash_analytics_data(
            original_raw_data_dir=DEFAULT_EIGENPHI_TX_RAW_DIR.replace(
                ".json", "_%s.json" % (collateral)
            )
        )

        with open(
            DEFAUT_TRADES_TOKENFLOW_DATA_DIR.replace(".csv", "_%s.csv" % (collateral)),
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.writer(f)
            writer.writerows(csv_lines)

        with open(
            "data/detailed_trades_tokenflow_data_%s.json" % (collateral), "w"
        ) as f:
            f.write(json.dumps(json_data, indent=4))
