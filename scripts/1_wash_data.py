import csv
import json
from analytics.get_trades import wash_analytics_data_from_file
from config.filename_config import DEFAULT_EIGENPHI_TX_RAW_DIR
from utils.utils import make_or_clean_dir

CSV_DIR = "data/csv"
JSON_DIR = "data/json"

if __name__ == "__main__":
    make_or_clean_dir(JSON_DIR)
    make_or_clean_dir(CSV_DIR)

    for collateral in ["sfrxETH", "wstETH", "WBTC", "WETH"]:
        json_data, csv_lines = wash_analytics_data_from_file(collateral)

        with open("%s/tokenflow_data_%s.csv" % (CSV_DIR, collateral), "w") as f:
            writer = csv.writer(f)
            writer.writerows(csv_lines)

        with open("%s/tokenflow_data_%s.json" % (JSON_DIR, collateral), "w") as f:
            f.write(json.dumps(json_data, indent=4))
