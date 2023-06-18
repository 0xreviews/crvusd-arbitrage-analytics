from collector.TokenBalanceDiff import TokenBalanceDiff
from utils import get_address_alias, is_address_zero


def get_eigenphi_tokenflow(resp):
    table_rows = resp["transferTable"]["rows"]

    address_tags = {
        "tx_from": "",
        "tx_to": "",
        "tx_beneficiary": "",
        "tx_miner": "",
        "arbitrage_contract": "",
    }
    for i in range(len(resp["addressTags"])):
        addr = resp["addressTags"][i]["address"]
        tags = resp["addressTags"][i]["tags"]
        for j in range(len(tags)):
            if tags[j]["categoryName"] == "TransactionField":
                if tags[j]["value"] == "from":
                    address_tags["tx_from"] = addr
                elif tags[j]["value"] == "to":
                    address_tags["tx_to"] = addr
                elif tags[j]["value"] == "miner":
                    address_tags["tx_miner"] = addr
            elif tags[j]["categoryName"] == "AddressType":
                if tags[j]["value"] == "EOA" and address_tags["tx_from"] == addr:
                    address_tags["tx_beneficiary"] = addr
                elif (
                    tags[j]["value"] == "Contract"
                    and address_tags["tx_to"] == addr
                    and address_tags["tx_beneficiary"] != addr
                    and get_address_alias(addr) == ""
                ):
                    address_tags["arbitrage_contract"] = addr

    transfers = []
    for i in range(len(resp["transfers"])):
        item = resp["transfers"][i]
        item["token_address"] = item["token"]["address"]
        item["token_symbol"] = item["token"]["symbol"].lower()
        item["from_alias"] = eigenphi_address_alias(item["from"], address_tags)
        item["to_alias"] = eigenphi_address_alias(item["to"], address_tags)
        transfers.append(item)

    transfers.sort(key=lambda x: x["transferStep"])

    token_balance_diff = TokenBalanceDiff()

    for i in range(len(table_rows)):
        row = table_rows[i]
        cell = row["cells"][0]
        token_balance_diff.update_diff(
            row["address"].lower(),
            symbol=cell["token"]["symbol"].lower(),
            diff=float(cell["amount"]),
        )

    return token_balance_diff, address_tags, transfers


def eigenphi_address_alias(addr, address_tags):
    _alias = get_address_alias(addr)
    if _alias == "":
        for key in [
            "tx_from",
            "tx_to",
            # "tx_beneficiary",
            "tx_miner",
            "arbitrage_contract",
        ]:
            value = address_tags[key]
            if value.lower() == addr.lower():
                _alias = key
    return _alias if _alias else addr
