


import os
from config.constance import ETHERSCAN_MAINNET_ENDPOINT
from network.http import HTTP


async def query_summary_data_etherscan(tx):
    if os.environ["ETHERSCAN_API_KEY"] is None:
        raise "ETHERSCAN_API_KEY is invalid."

    url = (
        ETHERSCAN_MAINNET_ENDPOINT
        + "?module=proxy&action=eth_getTransactionReceipt&apikey=%s&txhash=%s"
        % (os.environ["ETHERSCAN_API_KEY"], tx)
    )

    try:
        resp = await HTTP.get(url)
    except:
        return None
    
    return resp["result"]