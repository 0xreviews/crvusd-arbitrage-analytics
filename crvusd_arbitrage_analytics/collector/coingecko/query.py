# import requests
import json
from time import time
from utils.date import str_to_timestamp
from config.constance import BEGIN_DATE, COINGECKO_PRICE_HISTORICAL, SYMBOL_TO_ID
from config.filename_config import DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR

# from network.http import HTTP
import aiohttp
import requests


async def query_prices_historical(
    token_symbol,
    save=False,
    save_dir=DEFAULT_COINGECKO_PRICES_HISTORICAL_RAW_DIR,
):
    from_date = str_to_timestamp(BEGIN_DATE[token_symbol])
    to_date = time()
    token = SYMBOL_TO_ID[token_symbol]
    url = COINGECKO_PRICE_HISTORICAL.format(id=token)
    parameters = {
        "vs_currency": "usd",
        "convert": "USD",
        "from": from_date,
        "to": to_date,
    }
    # @todo
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, params=parameters) as resp:
    resp = requests.get(url, params=parameters).json()

    if "prices" in resp:
        if save:
            save_dir = save_dir.replace(".json", "_%s.json" % (token_symbol))
            with open(save_dir, "w") as json_file:
                json_file.write(json.dumps(resp["prices"], indent=4))
                print("prices data write to %s successfully." % (save_dir))

        return resp["prices"]
    else:
        return None
