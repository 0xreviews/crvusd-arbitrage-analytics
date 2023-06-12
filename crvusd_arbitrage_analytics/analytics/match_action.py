from utils import (
    get_address_alias,
    get_token_by_swap_name,
    is_curve_stable_swap,
    is_llamma_swap,
    is_uniswapv3_swap,
)
from config.tokenflow_category import (
    CURVE_STABLE_SWAP_FLOW,
    FRXETH_FLOW,
    LLAMMA_SWAP_FLOW,
    SWAPPOOL_TYPE,
    UNISWAP_V3_SWAP_FLOW,
    WETH_FLOW,
)


def match_weth_action(row_step, transfers):
    row = transfers[row_step]
    type_index = -1

    if row["token_symbol"].lower() == "weth":
        # deposit
        if (
            get_address_alias(row["from"]).lower() == "weth"
            and float(row["amount"]) > 0
        ):
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    get_address_alias(next_row["to"]).lower() == "weth"
                    and float(next_row["amount"]) > 0
                ):
                    type_index = 0
        # withdraw
        elif (
            get_address_alias(row["to"]).lower() == "weth" and float(row["amount"]) > 0
        ):
            # next transfer user should tansfer ETH to weth contract address
            if row_step > 0:
                prev_row = transfers[row_step - 1]
                if (
                    prev_row["token_symbol"].lower() == "eth"
                    and get_address_alias(prev_row["from"]).lower() == "weth"
                    and float(prev_row["amount"]) > 0
                ):
                    type_index = 1

        # transfer
        elif (
            row["category"].lower() == "transfer"
            and get_address_alias(row["from"]).lower() != "weth"
            and get_address_alias(row["to"]).lower() != "weth"
            and float(row["amount"]) > 0
        ):
            type_index = 2

    if type_index > -1:
        return (type_index, WETH_FLOW[type_index])
    else:
        return (-1, "")


def match_frxeth_action(row_step, transfers):
    row = transfers[row_step]
    type_index = -1

    # sFrxETH_contract token in
    if get_address_alias(row["to"]).lower() == "sfrxeth":
        # frxETH_stake:frxETH_in
        # 0. frxETH in sFrxETH_contract
        if row["token_symbol"].lower() == "frxeth":
            # next transfer is frxETH_stake:sFrxETH_out
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == "sfrxeth"
                    and get_address_alias(next_row["from"]).lower() == "sfrxeth"
                    and float(next_row["amount"]) > 0
                ):
                    type_index = 0

        # frxETH_unstake:sFrxETH_in
        # 3. transfer sFrxETH_in to sFrxETH_contract
        elif row["token_symbol"].lower() == "sfrxeth":
            # next transfer is frxETH_unstake:frxETH_out
            if len(transfers) > row_step + 2:
                next_row = transfers[row_step + 1]
                if (
                    next_row["token_symbol"].lower() == "frxeth"
                    and get_address_alias(next_row["from"]).lower() == "sfrxeth"
                    and float(next_row["amount"]) > 0
                ):
                    type_index = 2

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
                    type_index = 1

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
                    type_index = 3

    if type_index > -1:
        return (type_index, FRXETH_FLOW[type_index])
    else:
        return (-1, "")


# return pool_type_index, pool_type, swap_pool, swap_type_index, swap_type, token_symbol
def match_swap_pool_action(row_step, transfers):
    row = transfers[row_step]

    f_alias = get_address_alias(row["from"])
    t_alias = get_address_alias(row["to"])

    pool_type = -1
    swap_pool = ""
    swap_in = False

    # CurveStableSwap
    if is_curve_stable_swap(f_alias):
        pool_type = 0
        swap_pool = f_alias
        swap_in = False
    elif is_curve_stable_swap(t_alias):
        pool_type = 0
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

    if pool_type in [0, 2, 3]:
        swap_type_index = 0 if swap_in else 1
        swap_flow_list = CURVE_STABLE_SWAP_FLOW
        if pool_type == 2:
            swap_flow_list = LLAMMA_SWAP_FLOW
        elif pool_type == 3:
            swap_flow_list = UNISWAP_V3_SWAP_FLOW
        return (
            pool_type,
            SWAPPOOL_TYPE[pool_type],
            swap_pool,
            swap_type_index,
            swap_flow_list[swap_type_index],
            row["token_symbol"],
        )

    return (-1, "", -1, "", "", "")

