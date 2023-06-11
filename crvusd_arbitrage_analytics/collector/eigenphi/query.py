import requests
from config.constance import EIGEN_ANALYTICS_TX, EIGEN_TX_URL


def query_eigenphi_txtrace(tx, network_id="1"):
    return requests.get(EIGEN_TX_URL + tx).json()

def query_eigenphi_analytics_tx(tx):
    resp = requests.get(EIGEN_ANALYTICS_TX + tx).json()
    if resp['status'] == 'ok' and len(resp['result']) > 0:
        return resp['result'][0]
    return None