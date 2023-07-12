from utils.match import (
    get_address_alias,
    get_token_by_swap_name,
    is_balancer_vault,
    is_curve_router,
    is_curve_swap,
    is_llamma_swap,
    is_maverick_swap,
    is_pancake_swap,
    is_solidly_swap,
    is_uniswap_swap,
)
from config.tokenflow_category import (
    BALANCER_VAULT_FLOW,
    CALL_ARBI_CONTRACT_FLOW,
    CURVE_META_SWAP_FLOW,
    CURVE_ROUTER_FLOW,
    CURVE_SWAP_FLOW,
    CURVE_SWAP_WETH_FLOW,
    FRXETH_FLOW,
    LLAMMA_SWAP_FLOW,
    MAVERRICK_SWAP_FLOW,
    PANCAKE_SWAP_FLOW,
    SOLIDLY_SWAP_FLOW,
    SWAPPOOL_TYPE,
    TAKE_PROFIT_FLOW,
    UNISWAP_SWAP_FLOW,
    WETH_FLOW,
    RETH_FLOW,
)


def match_weth_action(row_step, transfers, target_symbol="weth"):
    row = transfers[row_step]
    token_symbol = row["token_symbol"]
    f_alias = get_address_alias(row["from"]).lower()
    t_alias = get_address_alias(row["to"]).lower()
    type_index = -1

    target_token_flow = WETH_FLOW
    if target_symbol == "reth":
        target_token_flow = RETH_FLOW

    # WETH_contract in
    if t_alias == target_symbol:
        # WETH_deposit:eth_in
        if token_symbol.lower() == "eth" and float(row["amount"]) > 0:
            # next transfer is WETH_deposit:weth_out
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == target_symbol
                    and get_address_alias(next_row["from"]).lower() == target_symbol
                    and float(next_row["amount"]) > 0
                ):
                    type_index = 0

        # WETH_withdraw:weth_in
        elif token_symbol.lower() == target_symbol and float(row["amount"]) > 0:
            # next transfer is WETH_withdraw:eth_out
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "eth"
                    and get_address_alias(prev_row["from"]).lower() == target_symbol
                    and float(prev_row["amount"]) > 0
                ):
                    type_index = 2

    # WETH_contract out
    elif f_alias == target_symbol:
        # WETH_withdraw:eth_out
        if token_symbol.lower() == "eth" and float(row["amount"]) > 0:
            # next transfer is WETH_withdraw:weth_in
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == target_symbol
                    and get_address_alias(next_row["to"]).lower() == target_symbol
                    and float(next_row["amount"]) > 0
                ):
                    type_index = 3
        # WETH_deposit:weth_out
        elif token_symbol.lower() == target_symbol and float(row["amount"]) > 0:
            # prev transfer is WETH_deposit:eth_in
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "eth"
                    and get_address_alias(prev_row["to"]).lower() == target_symbol
                    and float(prev_row["amount"]) > 0
                ):
                    type_index = 1

    elif row["category"].lower() == "transfer":
        if token_symbol == target_symbol:
            type_index = 4

    if type_index > -1:
        return (type_index, target_token_flow[type_index], token_symbol)
    else:
        return (-1, "", "")


def match_frxeth_action(row_step, transfers):
    row = transfers[row_step]
    token_symbol = row["token_symbol"].lower()
    action_type_index = -1

    f_alias = get_address_alias(row["from"]).lower()
    t_alias = get_address_alias(row["to"]).lower()

    # eth/frxETH to frxETHMinter_contract
    if t_alias == "frxethminter":
        if f_alias == "" and token_symbol == "eth":
            action_type_index = 0
        if f_alias == "frxeth" and token_symbol == "frxeth":
            action_type_index = 1

    # sFrxETH_contract token in
    elif t_alias == "sfrxeth":
        # frxETH_stake:frxETH_in
        #   frxETH in sFrxETH_contract
        if token_symbol == "frxeth":
            # next transfer is frxETH_stake:sFrxETH_out
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == "sfrxeth"
                    and get_address_alias(next_row["from"]).lower() == "sfrxeth"
                ):
                    action_type_index = 2

        # frxETH_unstake:sFrxETH_in
        #   transfer sFrxETH_in to sFrxETH_contract
        elif token_symbol == "sfrxeth":
            # prev transfer is frxETH_unstake:frxETH_out
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "frxeth"
                    and get_address_alias(prev_row["from"]).lower() == "sfrxeth"
                ):
                    action_type_index = 4

    # sFrxETH_contract token out
    elif f_alias == "sfrxeth":
        # frxETH_stake:sFrxETH_out
        #   transfer sFrxETH from sFrxETH_contract
        if token_symbol == "sfrxeth":
            # prev transfer is frxETH_stake:frxETH_in
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "frxeth"
                    and get_address_alias(prev_row["to"]).lower() == "sfrxeth"
                ):
                    action_type_index = 3

        # frxETH_unstake:frxETH_out
        #   transfer srxETH from sFrxETH_contract
        elif token_symbol == "frxeth":
            # next transfer is frxETH_unstake:sFrxETH_in
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == "sfrxeth"
                    and get_address_alias(next_row["to"]).lower() == "sfrxeth"
                ):
                    action_type_index = 5
    # transfer
    elif row["category"].lower() == "transfer":
        if token_symbol == "frxeth":
            action_type_index = 6
        elif token_symbol == "sfrxeth":
            action_type_index = 7

    if action_type_index > -1:
        return (action_type_index, FRXETH_FLOW[action_type_index], token_symbol)
    else:
        return (-1, "", "")


# return pool_type_index, pool_type, swap_pool, swap_type_index, swap_type, token_symbol
def match_swap_pool_action(row_step, transfers):
    row = transfers[row_step]

    f_alias = get_address_alias(row["from"])
    t_alias = get_address_alias(row["to"])
    token_symbol = row["token_symbol"].lower()

    pool_type = -1
    swap_pool = []
    swap_in = False

    # CurveRouter swap
    if is_curve_router(f_alias):
        swap_pool.append(f_alias)
        if not is_curve_swap(t_alias):
            pool_type = 0
            swap_in = False
    elif is_curve_router(t_alias):
        swap_pool.append(t_alias)
        if not is_curve_swap(f_alias):
            pool_type = 0
            swap_in = True

    # CurveSwap without router
    if pool_type == -1:
        if is_curve_swap(f_alias):
            pool_type = 1
            swap_pool.append(f_alias)
            swap_in = False
        if is_curve_swap(t_alias):
            pool_type = 1
            swap_pool.append(t_alias)
            swap_in = True
    # LLAMMA
    if is_llamma_swap(f_alias):
        pool_type = 2
        swap_pool.append(f_alias)
        swap_in = False
    if is_llamma_swap(t_alias):
        pool_type = 2
        swap_pool.append(t_alias)
        swap_in = True
    # UniswapPool
    if is_uniswap_swap(f_alias):
        pool_type = 3
        swap_pool.append(f_alias)
        swap_in = False
    if is_uniswap_swap(t_alias):
        pool_type = 3
        swap_pool.append(t_alias)
        swap_in = True
    # PancakePool = 4
    if is_pancake_swap(f_alias):
        pool_type = 4
        swap_pool.append(f_alias)
        swap_in = False
    if is_pancake_swap(t_alias):
        pool_type = 4
        swap_pool.append(t_alias)
        swap_in = True
    # SolidlySwapPool = 5
    if is_solidly_swap(f_alias):
        pool_type = 5
        swap_pool.append(f_alias)
        swap_in = False
    if is_solidly_swap(t_alias):
        pool_type = 5
        swap_pool.append(t_alias)
        swap_in = True
    # BalancerVault (flash)
    if is_balancer_vault(f_alias):
        pool_type = 6
        swap_pool.append(f_alias)
        swap_in = True
    if is_balancer_vault(t_alias):
        pool_type = 6
        swap_pool.append(t_alias)
        swap_in = False
    # MaverickPool
    if is_maverick_swap(f_alias):
        pool_type = 7
        swap_pool.append(f_alias)
        swap_in = True
    if is_maverick_swap(t_alias):
        pool_type = 7
        swap_pool.append(t_alias)
        swap_in = False

    if pool_type in range(len(SWAPPOOL_TYPE)):
        swap_type_index = 0 if swap_in else 1
        swap_flow_list = CURVE_SWAP_FLOW

        if pool_type == 0:
            swap_flow_list = CURVE_ROUTER_FLOW
            if len(swap_pool) > 1:
                swap_type_index += 2
        if pool_type == 1:
            swap_flow_list = CURVE_SWAP_FLOW
            # CurveSwapPool with weth
            if f_alias == "weth":
                if token_symbol == "weth":
                    swap_flow_list = CURVE_SWAP_WETH_FLOW
                    swap_type_index = 1
                elif token_symbol == "eth":
                    swap_flow_list = CURVE_SWAP_WETH_FLOW
                    swap_type_index = 3
            elif t_alias == "weth":
                if token_symbol == "weth":
                    swap_flow_list = CURVE_SWAP_WETH_FLOW
                    swap_type_index = 2
                elif token_symbol == "eth":
                    swap_flow_list = CURVE_SWAP_WETH_FLOW
                    swap_type_index = 0
            # CurveSwapPool(Meta) with 3crv(3Pool-LP) or 3 usd token
            if f_alias == "Curve3Pool-DAI-USDC-USDT":
                if token_symbol in ["dai", "usdc", "usdt"]:
                    swap_flow_list = CURVE_META_SWAP_FLOW
                    swap_type_index = 1
                elif token_symbol == "3crv":
                    swap_flow_list = CURVE_META_SWAP_FLOW
                    swap_type_index = 3
            elif t_alias == "Curve3Pool-DAI-USDC-USDT":
                if token_symbol in ["dai", "usdc", "usdt"]:
                    swap_flow_list = CURVE_META_SWAP_FLOW
                    swap_type_index = 0
                elif token_symbol == "3crv":
                    swap_flow_list = CURVE_META_SWAP_FLOW
                    swap_type_index = 2
            elif f_alias == "Curve3PoolLP-DAI-USDC-USDT":
                if token_symbol == "3crv":
                    swap_flow_list = CURVE_META_SWAP_FLOW
                    swap_type_index = 4
            elif t_alias == "Curve3PoolLP-DAI-USDC-USDT":
                if token_symbol in ["dai", "usdc", "usdt"]:
                    swap_flow_list = CURVE_META_SWAP_FLOW
                    swap_type_index = 5

        elif pool_type == 2:
            swap_flow_list = LLAMMA_SWAP_FLOW
        elif pool_type == 3:
            swap_flow_list = UNISWAP_SWAP_FLOW
        elif pool_type == 4:
            swap_flow_list = PANCAKE_SWAP_FLOW
        elif pool_type == 5:
            swap_flow_list = SOLIDLY_SWAP_FLOW
        elif pool_type == 6:
            swap_flow_list = BALANCER_VAULT_FLOW
        elif pool_type == 7:
            swap_flow_list = MAVERRICK_SWAP_FLOW

        return (
            pool_type,
            SWAPPOOL_TYPE[pool_type],
            ",".join(swap_pool),
            swap_type_index,
            swap_flow_list[swap_type_index],
            token_symbol,
            swap_flow_list,
        )

    return (-1, "", -1, "", "", "", [])


def match_call_arbitrage_contract(row_step, transfers, address_tags):
    if row_step == 0:
        row = transfers[row_step]
        action_type_index = -1

        if (
            row["from"] == address_tags["tx_beneficiary"]
            and row["to"] == address_tags["arbitrage_contract"]
        ):
            action_type_index = 1

        if action_type_index > -1:
            return (action_type_index, CALL_ARBI_CONTRACT_FLOW[action_type_index])
        else:
            return (-1, "")

    return (-1, "")


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


# @todo CurveStablePoolOwner
