# import requests
import json
from config.constance import EIGEN_ANALYTICS_TX, EIGEN_TX_URL, EIGEN_SUMMARY_TX
from network.http import HTTP


async def query_eigenphi_analytics_tx(tx):
    resp = await HTTP.get(EIGEN_ANALYTICS_TX + tx)
    if resp["status"] == "ok" and len(resp["result"]) > 0:
        return resp["result"][0]
    else:
        return None


async def query_eigenphi_summary_tx(tx):
    try:
        resp = await HTTP.get(EIGEN_SUMMARY_TX + tx)
    except:
        return None
    return resp
