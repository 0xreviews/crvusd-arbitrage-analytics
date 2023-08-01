import asyncio
import csv
import json
from collector.graphql.query import query_liquidations_all

from config.filename_config import DEFAUT_LIQUIDATIONS_GQL_DIR

def get_liquidations_data(llamma_collateral, save_dir=DEFAUT_LIQUIDATIONS_GQL_DIR, save_csv=False):
    all_liquidations = query_liquidations_all(llamma_collateral)

    save_dir = save_dir.replace(".json", "_%s.json" % (llamma_collateral))
    with open(save_dir, "w") as json_file:
        json_file.write(json.dumps(all_liquidations, indent=4))
    
    # @todo save csv file

    print("liquidations data write to %s successfully." % (save_dir))

    return all_liquidations