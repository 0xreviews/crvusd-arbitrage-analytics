import requests
from config.address import TENDERLY_TX_TRACE


def query_tenderly_txtrace(tx, network_id="1"):
    return requests.get(
        TENDERLY_TX_TRACE.substitute(networkId=network_id, tx=tx)
    ).json()
