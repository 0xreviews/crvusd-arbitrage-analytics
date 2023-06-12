import requests
from config.constance import EIGEN_ANALYTICS_TX, EIGEN_TX_URL, EIGEN_SUMMARY_TX


def query_eigenphi_txtrace(tx, network_id="1"):
    return requests.get(EIGEN_TX_URL + tx).json()


def query_eigenphi_analytics_tx(tx):
    resp = requests.get(EIGEN_ANALYTICS_TX + tx).json()
    if resp["status"] == "ok" and len(resp["result"]) > 0:
        return resp["result"][0]
    return None


def query_eigenphi_summary_tx(tx):
    return requests.get(EIGEN_SUMMARY_TX + tx).json()
