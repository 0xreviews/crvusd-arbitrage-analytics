from collector.TokenBalanceDiff import TokenBalanceDiff
from utils.match import get_address_alias, is_address_zero


def get_eigenphi_tokenflow(resp):
    table_rows = resp["transferTable"]["rows"]

    address_tags = {
        "tx_from": "",
        "tx_to": "",
        "tx_beneficiary": "",
        "tx_miner": "",
        "arbitrage_contract": "",
        "EOA_0": "",
        "EOA_1": "",
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
                if tags[j]["value"] == "EOA":
                    if address_tags["tx_from"] == addr:
                        address_tags["tx_beneficiary"] = addr
                    elif (
                        address_tags["tx_beneficiary"] == ""
                        and table_rows[0]["address"] == addr
                    ):
                        address_tags["tx_beneficiary"] = addr

                    if address_tags["EOA_0"] == "":
                        address_tags["EOA_0"] = addr
                    elif address_tags["EOA_1"] == "":
                        address_tags["EOA_1"] = addr

                elif (
                    tags[j]["value"] == "Contract"
                    # and address_tags["tx_to"] == addr
                    and address_tags["tx_beneficiary"] != addr
                    and address_tags["arbitrage_contract"] == ""
                    and get_address_alias(addr) == ""
                ):
                    address_tags["arbitrage_contract"] = addr
            elif tags[j]["categoryName"] == "Others" and tags[j]["value"] == "leaf":
                address_tags["tx_beneficiary"] = addr

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
            "EOA_0",
            "EOA_1",
            "tx_beneficiary",
            "tx_miner",
            "tx_from",
            "tx_to",
            "arbitrage_contract",
        ]:
            value = address_tags[key]
            if value.lower() == addr.lower():
                _alias = key
    return _alias if _alias else addr
