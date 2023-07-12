import re
from config.tokenflow_category import (
    ACTION_GROUP_TAG,
    ACTION_GROUP_TYPE,
    CURVE_META_SWAP_FLOW,
    CURVE_ROUTER_FLOW,
    CURVE_SWAP_FLOW,
    CURVE_SWAP_WETH_FLOW,
    FLASH_POOL_TYPE,
)
from utils.match import get_token_by_swap_name, is_balancer_vault, is_swap_pool


def match_action_group(token_flow_list):
    tmp_begin = -1
    tmp_end = -1
    tmp_group_index = -1

    group_count = {}

    for i in range(len(token_flow_list)):
        # clear prev group if it end
        if tmp_end > -1:
            tmp_begin = -1
            tmp_end = -1
            tmp_group_index = -1

        row = token_flow_list[i]
        action_group_item = []

        # group begin
        if tmp_begin < 0:
            tmp_begin = i
            tmp_group_index = check_action_group_type_index(row)
            if tmp_group_index not in group_count:
                group_count[tmp_group_index] = 0
            group_count[tmp_group_index] += 1

        # group end
        if tmp_end < 0:
            if i == len(token_flow_list) - 1:
                tmp_end = i
            elif i < len(token_flow_list) - 1:
                next_row = token_flow_list[i + 1]
                next_group_index = check_action_group_type_index(next_row)
                if next_group_index != tmp_group_index:
                    tmp_end = i
                else:
                    # if swap action, check swap pool are same
                    if tmp_group_index in [1, 2, 3, 4, 5, 6, 7]:
                        if row["swap_pool"] != next_row["swap_pool"]:
                            tmp_end = i

                # @remind some exceptions， not the end of group

                # CurveRouter pool deposit/withdraw WETH
                if tmp_group_index == 0:
                    if next_row["action_type"] in CURVE_SWAP_WETH_FLOW:
                        tmp_end = -1
                    elif next_row["action_type"] in CURVE_META_SWAP_FLOW:
                        tmp_end = -1

        if tmp_group_index > -1:
            group_name = row["action_type"].split(":")[0]
            action_group_item.append(
                "%s:%d" % (group_name, group_count[tmp_group_index])
            )

        token_flow_list[i]["action_group"] = ",".join(action_group_item)

    token_flow_list = match_curve_swap_special_group(
        token_flow_list,
        special_type="CurveSwapWETH_(Deposit|Withdraw)",
        exclude_pools=["CurveSwapRouter"],
        special_type_flow_list=[
            CURVE_SWAP_FLOW,
            CURVE_SWAP_WETH_FLOW,
            CURVE_SWAP_WETH_FLOW,
            CURVE_SWAP_FLOW,
        ],
    )

    token_flow_list = match_curve_swap_special_group(
        token_flow_list,
        special_type="CurveMetaPool_(Swap|LP)",
        exclude_pools=["CurveSwapRouter", "Curve3Pool-DAI-USDC-USDT"],
        special_type_flow_list=[
            CURVE_SWAP_FLOW,
            CURVE_META_SWAP_FLOW,
            CURVE_META_SWAP_FLOW,
            CURVE_SWAP_FLOW,
        ],
    )

    token_flow_list = match_flash_action_group(token_flow_list)

    token_flow_list = match_curve_router_group(token_flow_list)

    return token_flow_list


def check_action_group_type_index(row):
    action_type = row["action_type"]
    group_index = -1

    for i in range(len(ACTION_GROUP_TYPE)):
        if action_type in ACTION_GROUP_TYPE[i]:
            group_index = i
            break

    return group_index


# CurveSwap[WETH/METAPOOL]
def match_curve_swap_special_group(
    token_flow_list, special_type, exclude_pools, special_type_flow_list
):
    # CurveSwap:0 CurveSwap:token_in
    # CurveSwap:1 CurveSwap[WETH/METAPOOL]:...
    # CurveSwap:2 CurveSwap[WETH/METAPOOL]:...
    # CurveSwap:3 CurveSwap:token_out
    length = len(token_flow_list)
    for i in range(length):
        tmp_group = ""
        row = token_flow_list[i]
        if re.compile(special_type).match(row["action_group"]) is not None:
            if i > 0 and i < length - 3:
                row_0 = token_flow_list[i - 1]
                row_1 = row
                row_2 = token_flow_list[i + 1]
                row_3 = token_flow_list[i + 2]

                tmp_swap_pool = ""

                for p in row["swap_pool"].split(","):
                    if p not in exclude_pools:
                        tmp_swap_pool = p
                        break

                # check action_type and swap pool
                if (
                    row_0["action_type"] in special_type_flow_list[0]
                    and row_1["action_type"] in special_type_flow_list[1]
                    and row_2["action_type"] in special_type_flow_list[2]
                    and row_3["action_type"] in special_type_flow_list[3]
                    and tmp_swap_pool in row_0["swap_pool"].split(",")
                    and tmp_swap_pool in row_2["swap_pool"].split(",")
                    and tmp_swap_pool in row_3["swap_pool"].split(",")
                ):
                    tmp_group = row_0["action_group"]
                    row_1["action_group"] = tmp_group + "," + row_1["action_group"]
                    row_2["action_group"] = tmp_group + "," + row_2["action_group"]
                    row_3["action_group"] = modify_match_group_type(
                        tmp_group.split(":")[0], tmp_group, row_3["action_group"]
                    )

    return token_flow_list


def match_curve_router_group(token_flow_list):
    length = len(token_flow_list)
    tmp_router_group_name = ""
    tmp_target_group = ""
    add_router_group_list = []
    for i in range(length):
        row = token_flow_list[i]
        groups = row["action_group"].split(",")
        if "CurveRouter:" in groups[0] and row["action_type"] == CURVE_ROUTER_FLOW[0]:
            tmp_router_group_name = groups[0]
            continue
        if "CurveRouter:" in groups[0] and row["action_type"] == CURVE_ROUTER_FLOW[1]:
            row["action_group"] = modify_match_group_type(
                "CurveRouter:[0-9]+", tmp_router_group_name, row["action_group"]
            )
            continue
        if "CurveSwapRouter" in row["swap_pool"] and tmp_target_group != groups[0]:
            tmp_target_group = groups[0]
        if tmp_target_group not in add_router_group_list:
            add_router_group_list.append(tmp_target_group)
        if tmp_router_group_name != "" and groups[0] in add_router_group_list:
            row["action_group"] = tmp_router_group_name + "," + row["action_group"]

    return token_flow_list


def match_flash_action_group(token_flow_list):
    length = len(token_flow_list)

    borrow_index_stack = []
    repay_index_stack = []
    flash_pool_list = []

    # loop reversed list
    for borrow_ptr in range(length - 1, -1, -1):
        borrow_row = token_flow_list[borrow_ptr]
        borrow_symbol = borrow_row["token_symbol"]
        borrow_action_type = borrow_row["action_type"]
        borrow_swap_pools = borrow_row["swap_pool"].split(",")
        borrower = borrow_row["to"]

        borrow_flash_type_index, if_borrow_token_out = check_flash_group_type(
            borrow_action_type
        )

        if (
            borrow_flash_type_index < 0
            # or not if_borrow_token_out
            or borrow_ptr in borrow_index_stack
        ):
            continue

        for repay_ptr in range(length):
            repay_row = token_flow_list[repay_ptr]
            repay_symbol = repay_row["token_symbol"]
            repay_action_type = repay_row["action_type"]
            repay_swap_pools = repay_row["swap_pool"].split(",")
            repayer = repay_row["from"]


            if len(repay_swap_pools) == 1:
                repay_flash_type_index, if_repay_token_out = check_flash_group_type(
                    repay_action_type
                )

                if (
                    repay_flash_type_index < 0
                    or if_repay_token_out
                    or repay_ptr in repay_index_stack
                ):
                    continue

            is_pair = False
            for repay_swap_pool in repay_swap_pools:
                # borrower == repayer: Normal flash swap
                # swap_pool_B repay to swap_pool_A:
                #   1. borrow from swap_pool_A
                #   2. swap_pool_B token out, repay to swap_pool_A
                #   3. swap_pool_B token in (normal swap)
                if (
                    repay_swap_pool in borrow_swap_pools
                    and repay_ptr - borrow_ptr > 1
                    and (borrower == repayer or is_swap_pool(repayer))
                ):
                    # BalancerVault
                    if (
                        repay_flash_type_index == 3
                        and repay_symbol == borrow_symbol
                        and is_balancer_vault(repay_swap_pool)
                    ):
                        borrow_index_stack.append(borrow_ptr)
                        repay_index_stack.append(repay_ptr)
                        is_pair = True
                        flash_pool_list.append(repay_swap_pool)
                        break
                    
                    else:

                        tokens = get_token_by_swap_name(repay_swap_pool)
                        tokens = [token.lower() for token in tokens]

                        if repay_symbol in tokens and borrow_symbol in tokens:
                            borrow_index_stack.append(borrow_ptr)
                            repay_index_stack.append(repay_ptr)
                            is_pair = True
                            flash_pool_list.append(repay_swap_pool)
                            break
            

            if is_pair:
                break

    flash_action_pair_cout = 0
    while len(borrow_index_stack) > 0:
        borrow_ptr = borrow_index_stack.pop()
        repay_ptr = repay_index_stack.pop()
        flash_pool = flash_pool_list.pop()

        # edit action_group
        borrow_group = "flash_borrow:%s:%d" % (flash_pool, flash_action_pair_cout)
        repay_group = "flash_repay:%s:%d" % (flash_pool, flash_action_pair_cout)

        if isinstance(token_flow_list[borrow_ptr]["action_group"], list):
            token_flow_list[borrow_ptr]["action_group"].append(borrow_group)
        else:
            token_flow_list[borrow_ptr]["action_group"] = [borrow_group]
        if "flash_pair" in token_flow_list[borrow_ptr] and isinstance(token_flow_list[borrow_ptr]["flash_pair"], list):
            token_flow_list[borrow_ptr]["flash_pair"].append(str(flash_action_pair_cout))
        else:
            token_flow_list[borrow_ptr]["flash_pair"] = [str(flash_action_pair_cout)]
   
        if isinstance(token_flow_list[repay_ptr]["action_group"], list):
            token_flow_list[repay_ptr]["action_group"].append(repay_group)
        else:
            token_flow_list[repay_ptr]["action_group"] = [repay_group]
        if "flash_pair" in token_flow_list[repay_ptr] and isinstance(token_flow_list[repay_ptr]["flash_pair"], list):
            token_flow_list[repay_ptr]["flash_pair"].append(str(flash_action_pair_cout))
        else:
            token_flow_list[repay_ptr]["flash_pair"] = [str(flash_action_pair_cout)]

        flash_action_pair_cout += 1
    
    for row in token_flow_list:
        if isinstance(row["action_group"], list):
            row["action_group"] = ",".join(row["action_group"])
        if "flash_pair" in row and isinstance(row["flash_pair"], list):
            row["flash_pair"] = ",".join(row["flash_pair"])

    return token_flow_list


def check_flash_group_type(action_type):
    flash_group_type_index = -1
    if_token_out = False

    for i in range(len(FLASH_POOL_TYPE)):
        if re.compile("^" + FLASH_POOL_TYPE[i]).match(action_type):
            flash_group_type_index = i

            if action_type.replace(FLASH_POOL_TYPE[i] + ":", "") == "token_out":
                if_token_out = True

            break

    return flash_group_type_index, if_token_out


def modify_match_group_type(match_pattern, target_value, group_types):
    new_group_types = []
    for g in group_types.split(","):
        if re.compile(match_pattern).match(g) is not None:
            g = target_value
        new_group_types.append(g)
    return ",".join(new_group_types)
