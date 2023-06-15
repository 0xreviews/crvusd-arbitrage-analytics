import re
from config.tokenflow_category import (
    ACTION_GROUP_TAG,
    ACTION_GROUP_TYPE,
    CURVE_META_SWAP_FLOW,
    CURVE_SWAP_WETH_FLOW,
    FLASH_POOL_TYPE,
)
from utils import get_token_by_swap_name


def match_action_group(token_flow_list):
    tmp_begin = -1
    tmp_end = -1
    tmp_group_index = -1

    for i in range(len(token_flow_list)):
        # clear prev group if it end
        if tmp_end > -1:
            tmp_begin = -1
            tmp_end = -1
            tmp_group_index = -1

        row = token_flow_list[i]
        action_group_item = ""

        # group begin
        if tmp_begin < 0:
            tmp_begin = i
            tmp_group_index = check_action_group_type_index(row)

        # group end
        if tmp_end < 0:
            if i == len(token_flow_list) - 1:
                tmp_end = i
            elif i < len(token_flow_list) - 1:
                next_row = token_flow_list[i + 1]
                next_group_index = check_action_group_type_index(next_row)
                if next_group_index != tmp_group_index:
                    tmp_end = i

                # @remind some exceptions， not the end of group

                # CurveRouter pool deposit/withdraw WETH
                if tmp_group_index == 0:
                    if next_row["action_type"] in CURVE_SWAP_WETH_FLOW:
                        tmp_end = -1
                    elif next_row["action_type"] in CURVE_META_SWAP_FLOW:
                        tmp_end = -1

        if tmp_group_index > -1:
            tmp_action_group = ACTION_GROUP_TYPE[tmp_group_index]
            action_group_item = "%s:%d" % (tmp_action_group, i - tmp_begin)

        # add action_group tag

        # CurveRouterSwap group tag
        if tmp_group_index == 0:
            if i == tmp_begin:
                action_group_item += ":%s" % (ACTION_GROUP_TAG[0])
            elif i == tmp_end:
                action_group_item += ":%s" % (ACTION_GROUP_TAG[2])
            else:
                action_group_item += ":%s" % (ACTION_GROUP_TAG[1])

        token_flow_list[i]["action_group"] = action_group_item

    token_flow_list = match_flash_action_group(token_flow_list)

    return token_flow_list


def check_action_group_type_index(row):
    action_type = row["action_type"]
    swap_pool = row["swap_pool"]
    group_index = -1

    for i in range(len(ACTION_GROUP_TYPE)):
        if re.compile("^" + ACTION_GROUP_TYPE[i]).match(action_type):
            group_index = i
            break

    return group_index


def match_flash_action_group(token_flow_list):
    length = len(token_flow_list)

    borrow_index_stake = []
    repay_index_stake = []

    # loop reversed list
    for borrow_ptr in range(length - 1, -1, -1):
        borrow_row = token_flow_list[borrow_ptr]
        borrow_symbol = borrow_row["token_symbol"]
        borrow_action_type = borrow_row["action_type"]
        borrow_swap_pool = borrow_row["swap_pool"]
        borrower = borrow_row["to"]

        borrow_flash_type_index, if_borrow_token_out = check_flash_group_type(
            borrow_action_type
        )

        if (
            borrow_flash_type_index < 0
            or not if_borrow_token_out
            or borrow_ptr in borrow_index_stake
        ):
            continue

        for repay_ptr in range(length):
            repay_row = token_flow_list[repay_ptr]
            repay_symbol = repay_row["token_symbol"]
            repay_action_type = repay_row["action_type"]
            repay_swap_pool = repay_row["swap_pool"]
            repayer = repay_row["from"]

            repay_flash_type_index, if_repay_token_out = check_flash_group_type(
                repay_action_type
            )

            if (
                repay_flash_type_index < 0
                or if_repay_token_out
                or repay_ptr in repay_index_stake
            ):
                continue

            if (
                repay_swap_pool == borrow_swap_pool
                and repay_ptr - borrow_ptr > 1
                and borrower == repayer
            ):
                # BalancerVault
                if repay_flash_type_index == 3 and repay_symbol == borrow_symbol:
                    borrow_index_stake.append(borrow_ptr)
                    repay_index_stake.append(repay_ptr)
                    break

                tokens = get_token_by_swap_name(repay_swap_pool)
                tokens = [token.lower() for token in tokens]

                if repay_symbol in tokens and borrow_symbol in tokens:
                    borrow_index_stake.append(borrow_ptr)
                    repay_index_stake.append(repay_ptr)
                    break

    flash_action_pair_cout = 0
    while len(borrow_index_stake) > 0:
        borrow_ptr = borrow_index_stake.pop()
        repay_ptr = repay_index_stake.pop()

        # edit action_group
        token_flow_list[borrow_ptr]["action_group"] = re.sub(
            r":[0-9]+",
            ":flash_borrow:%d" % (flash_action_pair_cout),
            token_flow_list[borrow_ptr]["action_group"],
        )
        token_flow_list[borrow_ptr]["flash_pair"] = flash_action_pair_cout

        token_flow_list[repay_ptr]["action_group"] = re.sub(
            r":[0-9]+",
            ":flash_repay:%d" % (flash_action_pair_cout),
            token_flow_list[repay_ptr]["action_group"],
        )
        token_flow_list[repay_ptr]["flash_pair"] = flash_action_pair_cout

        flash_action_pair_cout += 1

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
