import re
from typing import List
from xmlrpc.client import Boolean
from config.constance import (
    ADDRESS_ALIAS,
    ADDRESS_PATTERN,
    ETH_SWAP_POOLS_ALIAS,
    TOKEN_DECIMALS,
)
from config.tokenflow_category import (
    BALANCER_VAULT_PATTERN,
    CURVE_ROUTER_PATTERN,
    CURVE_SWAP_PATTERN,
    LLAMMA_SWAP_PATTERN,
    PANCAKE_SWAP_PATTERN,
    SOLIDLY_SWAP_PATTERN,
    UNISWAP_V3_SWAP_PATTERN,
)


def get_address_alias(address):
    if address.lower() in ADDRESS_ALIAS:
        return ADDRESS_ALIAS[address.lower()]
    else:
        return ""


def format_decimals(n, symbol="", decimals=18):
    d = decimals
    if symbol != "" and symbol.lower() in TOKEN_DECIMALS:
        d = TOKEN_DECIMALS[symbol.lower()]

    return int(n) / 10**d


def is_address(string) -> Boolean:
    pattern = re.compile(ADDRESS_PATTERN)
    return pattern.match(string) != None


def is_address_zero(address) -> Boolean:
    if is_address(address) != True:
        return False
    return get_address_alias(address) == "ADDRESS_ZERO"


def is_weth_or_frxeth(address) -> Boolean:
    if is_address(address) != True:
        return False
    return get_address_alias(address) in ["weth", "frxETH"]


def is_eth_swap_pool(address) -> Boolean:
    if is_address(address) != True:
        return False
    return get_address_alias(address) in ETH_SWAP_POOLS_ALIAS


def is_curve_router(string) -> Boolean:
    pattern = re.compile(CURVE_ROUTER_PATTERN)
    return pattern.match(string) != None


def is_curve_swap(string) -> Boolean:
    pattern = re.compile(CURVE_SWAP_PATTERN)
    return pattern.match(string) != None


def is_uniswap_swap(string) -> Boolean:
    pattern = re.compile(UNISWAP_V3_SWAP_PATTERN)
    return pattern.match(string) != None


def is_llamma_swap(string) -> Boolean:
    pattern = re.compile(LLAMMA_SWAP_PATTERN)
    return pattern.match(string) != None


def is_pancake_swap(string) -> Boolean:
    pattern = re.compile(PANCAKE_SWAP_PATTERN)
    return pattern.match(string) != None


def is_balancer_vault(string) -> Boolean:
    pattern = re.compile(BALANCER_VAULT_PATTERN)
    return pattern.match(string) != None


def is_solidly_swap(string) -> Boolean:
    pattern = re.compile(SOLIDLY_SWAP_PATTERN)
    return pattern.match(string) != None


def get_token_by_swap_name(string) -> List[str]:
    if (
        is_curve_swap(string)
        or is_llamma_swap(string)
        or is_uniswap_swap(string)
        or is_pancake_swap(string)
        or is_solidly_swap(string)
    ):
        string_list = re.compile("-[0-9a-zA-Z]+").findall(string)
        if len(string_list) >0:
            return [re.sub(r"^-", '', token) for token in string_list]
    return []
