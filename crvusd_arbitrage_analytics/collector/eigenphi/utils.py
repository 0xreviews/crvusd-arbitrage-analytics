from collector.TokenBalanceDiff import TokenBalanceDiff
from utils import get_address_alias, is_address_zero


def get_eigenphi_tokenflow(resp):
    table_rows = resp["transferTable"]["rows"]

    address_tags = {
        "tx_from": "",
        "tx_to": "",
        "tx_beneficiary": "",
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
            elif tags[j]["categoryName"] == "AddressType":
                if tags[j]["value"] == "EOA":
                    address_tags["tx_beneficiary"] = addr

    transfers = []
    for i in range(len(resp["transfers"])):
        item = resp["transfers"][i]
        item["token_address"] = item["token"]["address"]
        item["token_symbol"] = item["token"]["symbol"].lower()
        transfers.append(item)

    token_path = []


    token_balance_diff = TokenBalanceDiff()

    for i in range(len(table_rows)):
        row = table_rows[i]
        cell = row["cells"][0]
        token_balance_diff.update_diff(
            row["address"].lower(),
            symbol=cell["token"]["symbol"].lower(),
            diff=float(cell["amount"]),
        )

    return token_path, token_balance_diff, address_tags, transfers
