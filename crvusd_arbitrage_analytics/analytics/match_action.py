from utils import (
    get_address_alias,
    get_token_by_swap_name,
    is_balancer_vault,
    is_curve_router,
    is_curve_swap,
    is_llamma_swap,
    is_uniswapv3_swap,
)
from config.tokenflow_category import (
    BALANCER_VAULT_FLOW,
    CURVE_ROUTER_FLOW,
    CURVE_SWAP_FLOW,
    FRXETH_FLOW,
    LLAMMA_SWAP_FLOW,
    SWAPPOOL_TYPE,
    TAKE_PROFIT_FLOW,
    UNISWAP_V3_SWAP_FLOW,
    WETH_FLOW,
)


def match_weth_action(row_step, transfers):
    row = transfers[row_step]
    token_symbol = row["token_symbol"]
    type_index = -1

    # WETH_contract in
    if get_address_alias(row["to"]).lower() == "weth":
        # WETH_deposit:eth_in
        if token_symbol.lower() == "eth" and float(row["amount"]) > 0:
            # prev transfer is WETH_deposit:weth_out
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "weth"
                    and get_address_alias(prev_row["from"]).lower() == "weth"
                    and float(prev_row["amount"]) > 0
                ):
                    type_index = 0

        # WETH_withdraw:weth_in
        elif token_symbol.lower() == "weth" and float(row["amount"]) > 0:
            # prev transfer is WETH_withdraw:eth_out
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "eth"
                    and get_address_alias(prev_row["from"]).lower() == "weth"
                    and float(prev_row["amount"]) > 0
                ):
                    type_index = 2

    # WETH_contract out
    elif get_address_alias(row["from"]).lower() == "weth":
        # WETH_deposit:weth_out
        if token_symbol.lower() == "weth" and float(row["amount"]) > 0:
            # next transfer is WETH_deposit:eth_in
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == "eth"
                    and get_address_alias(next_row["to"]).lower() == "weth"
                    and float(next_row["amount"]) > 0
                ):
                    type_index = 1

        # WETH_withdraw:eth_out
        elif token_symbol.lower() == "eth" and float(row["amount"]) > 0:
            # next transfer is WETH_withdraw:weth_in
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == "weth"
                    and get_address_alias(next_row["to"]).lower() == "weth"
                    and float(next_row["amount"]) > 0
                ):
                    type_index = 3

    elif row["category"].lower() == "transfer":
        if token_symbol == "weth":
            type_index = 4

    if type_index > -1:
        return (type_index, WETH_FLOW[type_index], token_symbol)
    else:
        return (-1, "", "")


def match_frxeth_action(row_step, transfers):
    row = transfers[row_step]
    token_symbol = row["token_symbol"]
    action_type_index = -1

    # sFrxETH_contract token in
    if get_address_alias(row["to"]).lower() == "sfrxeth":
        # frxETH_stake:frxETH_in
        # 0. frxETH in sFrxETH_contract
        if token_symbol.lower() == "frxeth":
            # next transfer is frxETH_stake:sFrxETH_out
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == "sfrxeth"
                    and get_address_alias(next_row["from"]).lower() == "sfrxeth"
                    and float(next_row["amount"]) > 0
                ):
                    action_type_index = 0

        # frxETH_unstake:sFrxETH_in
        # 3. transfer sFrxETH_in to sFrxETH_contract
        elif token_symbol.lower() == "sfrxeth":
            # next transfer is frxETH_unstake:frxETH_out
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == "frxeth"
                    and get_address_alias(next_row["from"]).lower() == "sfrxeth"
                    and float(next_row["amount"]) > 0
                ):
                    action_type_index = 2

    # sFrxETH_contract token out
    elif get_address_alias(row["from"]).lower() == "sfrxeth":
        # frxETH_stake:sFrxETH_out
        #   2. transfer sFrxETH from sFrxETH_contract
        if row["token_symbol"].lower() == "sfrxeth":
            # prev transfer is frxETH_stake:frxETH_in
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "frxeth"
                    and get_address_alias(prev_row["to"]).lower() == "sfrxeth"
                ):
                    action_type_index = 1

        # frxETH_unstake:frxETH_out
        #   3. transfer srxETH from sFrxETH_contract
        elif row["token_symbol"].lower() == "frxeth" and float(row["amount"]) > 0:
            # prev transfer is frxETH_unstake:sFrxETH_in
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "sfrxeth"
                    and get_address_alias(prev_row["to"]).lower() == "sfrxeth"
                    and float(prev_row["amount"]) > 0
                ):
                    action_type_index = 3
    # transfer
    elif row["category"].lower() == "transfer":
        if token_symbol == "frxETH":
            action_type_index = 4
        elif token_symbol == "frxETH":
            action_type_index = 5

    if action_type_index > -1:
        return (action_type_index, FRXETH_FLOW[action_type_index], token_symbol)
    else:
        return (-1, "", "")


# return pool_type_index, pool_type, swap_pool, swap_type_index, swap_type, token_symbol
def match_swap_pool_action(row_step, transfers):
    row = transfers[row_step]

    f_alias = get_address_alias(row["from"])
    t_alias = get_address_alias(row["to"])

    pool_type = -1
    swap_pool = ""
    swap_in = False

    # CurveRouter
    if is_curve_router(f_alias):
        pool_type = 0
        swap_pool = f_alias
        swap_in = False
        if is_curve_swap(t_alias):
            swap_pool += "," + t_alias  
    elif is_curve_router(t_alias):
        pool_type = 0
        swap_pool = t_alias
        swap_in = True
        if is_curve_swap(f_alias):
            swap_pool += "," + f_alias  
    # CurveSwap
    elif is_curve_swap(f_alias):
        pool_type = 1
        swap_pool = f_alias
        swap_in = False
    elif is_curve_swap(t_alias):
        pool_type = 1
        swap_pool = t_alias
        swap_in = True
    # LLAMMA
    elif is_llamma_swap(f_alias):
        pool_type = 2
        swap_pool = f_alias
        swap_in = False
    elif is_llamma_swap(t_alias):
        pool_type = 2
        swap_pool = t_alias
        swap_in = True
    # UniswapV3Pool
    elif is_uniswapv3_swap(f_alias):
        pool_type = 3
        swap_pool = f_alias
        swap_in = False
    elif is_uniswapv3_swap(t_alias):
        pool_type = 3
        swap_pool = t_alias
        swap_in = True
    # BalancerVault (flash)
    elif is_balancer_vault(f_alias):
        pool_type = 5
        swap_pool =f_alias
        swap_in = True
    elif is_balancer_vault(t_alias):
        pool_type = 5
        swap_pool = t_alias
        swap_in = False

    if pool_type in [0, 1, 2, 3, 5]:
        swap_type_index = 0 if swap_in else 1
        swap_flow_list = CURVE_SWAP_FLOW

        if pool_type == 0:
            swap_flow_list = CURVE_ROUTER_FLOW
            if len(swap_pool.split(",")) > 1:
                swap_type_index += 2
        elif pool_type == 2:
            swap_flow_list = LLAMMA_SWAP_FLOW
        elif pool_type == 3:
            swap_flow_list = UNISWAP_V3_SWAP_FLOW
        elif pool_type == 5:
            swap_flow_list = BALANCER_VAULT_FLOW

        return (
            pool_type,
            SWAPPOOL_TYPE[pool_type],
            swap_pool,
            swap_type_index,
            swap_flow_list[swap_type_index],
            row["token_symbol"],
            swap_flow_list,
        )

    return (-1, "", -1, "", "", "", [])


def match_take_profit(row_step, transfers, address_tags):
    row = transfers[row_step]
    action_type_index = -1

    if row["to"] == address_tags["tx_miner"]:
        action_type_index = 0
    # arbitrage_contract transfer profit to tx_from
    elif row["from"] == address_tags["tx_to"] and row["to"] == address_tags["tx_from"]:
        action_type_index = 1

    if action_type_index > -1:
        return (action_type_index, TAKE_PROFIT_FLOW[action_type_index])
    else:
        return (-1, "")


# @todo Curve3Pool

# @todo CurveTriCrypto

# @todo CurveStablePoolOwner

# @todo CurveSwapRouter

# @todo rETH

# @todo frxETHMinter

# @todo frxETHMinter

# @todo BalancerVault

# @todo PancakeV3Pool

# @todo SolidlySwap

