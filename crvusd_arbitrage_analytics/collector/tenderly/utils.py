from ..TokenBalanceDiff import TokenBalanceDiff
from utils.match import (
    format_decimals,
    get_address_alias,
    is_address,
    is_eth_swap_pool,
    is_weth_or_frxeth,
)
from config.address import ALIAS_TO_ADDRESS, ADDRESS_ALIAS, ADDRESS_ZERO


def tenderly_tokenflow(resp):
    # tenderly.asset_chagnes does not include ETH flow
    asset_changes = [
        {
            "type": item["type"],
            "name": item["token_info"]["name"],
            "symbol": item["token_info"]["symbol"],
            "amount": item["amount"],
            "dollar_value": item["dollar_value"],
            "from": item["from"] if "from" in item else ADDRESS_ZERO,
            "from_alias": get_address_alias(item["from"])
            if "from" in item
            else "ADDRESS_ZERO",
            "to": item["to"] if "to" in item else ADDRESS_ZERO,
            "to_alias": get_address_alias(item["to"])
            if "to" in item
            else "ADDRESS_ZERO",
            "contract_address": item["token_info"]["contract_address"],
            "decimals": item["token_info"]["decimals"],
            "standard": item["token_info"]["standard"],
        }
        for item in resp["asset_changes"]
    ]

    # tx caller
    caller = resp["call_trace"]["from"]

    token_balance_diff = TokenBalanceDiff()
    for i in range(len(asset_changes)):
        item = asset_changes[i]
        token_balance_diff.update_diff(
            addr=item["from"].lower(),
            symbol=item["symbol"],
            diff=float(item["amount"]) * -1,
        )
        token_balance_diff.update_diff(
            addr=item["to"].lower(),
            symbol=item["symbol"],
            diff=float(item["amount"]),
        )

    # add some token flow data with tx_logs
    for i in range(len(resp["logs"])):
        item = resp["logs"][i]
        n = item["name"]
        inputs = item["inputs"]
        contract_address = item["raw"]["address"]

        s = (
            get_address_alias(contract_address)
            if get_address_alias(contract_address) != ""
            else contract_address
        )  # symbol
        f = ""  # from
        t = ""  # to
        a = 0  # amount

        # WETH.withdraw(): weth to ADDRESS_ZERO
        if n == "Withdrawal":
            if s.lower() == "weth":
                t = ALIAS_TO_ADDRESS["weth"]
                for _input in inputs:
                    if _input["soltype"]["name"] == "src":
                        f = _input["value"]
                    if _input["soltype"]["name"] == "wad":
                        a = format_decimals(_input["value"], symbol=s)

        if a == 0:
            continue

        token_balance_diff.update_diff(addr=f, symbol=s, diff=-a)
        token_balance_diff.update_diff(addr=t, symbol=s, diff=a)

    # generate ETH flow with tenderly.balance_diff
    for i in range(len(resp["balance_diff"])):
        item = resp["balance_diff"][i]
        if item["is_miner"]:
            continue
        if (
            item["address"].lower() == caller
            or is_weth_or_frxeth(item["address"])
            or is_eth_swap_pool(item["address"])
        ):
            # tenderly.state_diff.dirty/original maybe number string or dict
            amount = int(item["dirty"]) - int(item["original"])
            token_balance_diff.update_diff(
                addr=item["address"].lower(),
                symbol="eth",
                diff=format_decimals(amount, symbol="eth"),
            )

            

    return asset_changes, token_balance_diff


def tenderly_txlog(tx_logs):
    # token_balance_diff:
    #   address:
    #       token symbol: net value
    token_balance_diff = TokenBalanceDiff()

    # Tenderly result.asset_changes won't track sFrxETH.deposit/withdraw
    # We process logs to generate token flow
    for i in range(len(tx_logs)):
        n = tx_logs[i]["name"]
        inputs = tx_logs[i]["inputs"]
        contract_address = tx_logs[i]["raw"]["address"]

        s = (
            get_address_alias(contract_address)
            if get_address_alias(contract_address) != ""
            else contract_address
        )  # symbol
        f = ""  # from
        t = ""  # to
        a = 0  # amount
        v = 0  # dollar_value

        # if call dposit/withdraw function of WETH/stETH/frxETH,
        # need add ETH token flow
        eth_flow_from = ""
        eth_flow_to = ""
        eth_flow_amount = 0
        eth_flow_value = 0

        # @remind use equivalent amount of ETH to accounting,
        # store staked amount in `staked_eth_shares`
        # sFrxETH/stETH shares
        staked_eth_shares = 0

        if n == "Transfer":
            for _input in inputs:
                if _input["soltype"]["name"] in ["from", "src", "sender"]:
                    f = _input["value"]
                if _input["soltype"]["name"] in ["to", "dst", "receiver"]:
                    t = _input["value"]
                if _input["soltype"]["name"] in ["value", "wad"]:
                    a = format_decimals(_input["value"], symbol=s)

                # frxETH burn emit Transfer event
                if s.lower() == "frxeth" and t == ADDRESS_ZERO:
                    eth_flow_from = ADDRESS_ZERO
                    eth_flow_to = f
                    eth_flow_amount = a

        elif n == "Withdrawal":
            if s.lower() == "weth":
                t = ALIAS_TO_ADDRESS["weth"]
                for _input in inputs:
                    if _input["soltype"]["name"] == "src":
                        f = _input["value"]
                    if _input["soltype"]["name"] == "wad":
                        a = format_decimals(_input["value"], symbol=s)
                # eth flow amount
                eth_flow_from = t
                eth_flow_to = f
                eth_flow_amount = a

            # @todo sfrxeth Withdrawal
            # @todo wsteth Withdrawal

        elif n == "Deposit":
            if s.lower() == "sfrxeth":
                # sFrxETH transfer out to owner
                f = ALIAS_TO_ADDRESS["sFrxETH"]
                for _input in inputs:
                    if _input["soltype"]["name"] == "owner":
                        t = _input["value"]
                    if _input["soltype"]["name"] == "shares":
                        staked_eth_shares = format_decimals(_input["value"], symbol=s)
                    if _input["soltype"]["name"] == "assets":
                        a = format_decimals(_input["value"], symbol=s)
                # frxETH transfer in to contract
                token_balance_diff.update_diff(addr=t, symbol=s, diff=-a)
                token_balance_diff.update_diff(addr=f, symbol=s, diff=a)

            # @todo weth Deposit
            # @todo wsteth Deposit

        if a == 0 and eth_flow_amount == 0:
            continue

        token_balance_diff.update_diff(addr=f, symbol=s, diff=-a)
        token_balance_diff.update_diff(addr=t, symbol=s, diff=a)

        # add eth token flow
        if eth_flow_amount != 0:
            token_balance_diff.update_diff(
                addr=eth_flow_from, symbol="eth", diff=-eth_flow_amount
            )
            token_balance_diff.update_diff(
                addr=eth_flow_to, symbol="eth", diff=eth_flow_amount
            )
