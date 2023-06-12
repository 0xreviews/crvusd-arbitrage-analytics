import re
from config.constance import ADDRESS_ALIAS, ADDRESS_PATTERN,  ETH_SWAP_POOLS_ALIAS, TOKEN_DECIMALS
from config.tokenflow_category import CURVE_STABLE_SWAP_PATTERN, LLAMMA_SWAP_PATTERN, UNISWAP_V3_SWAP_PATTERN

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


def is_address(string):
    pattern = re.compile(ADDRESS_PATTERN)
    return pattern.match(string) != None

def is_address_zero(address):
    if is_address(address) != True:
        return False
    return get_address_alias(address) == "ADDRESS_ZERO"

def is_weth_or_frxeth(address):
    if is_address(address) != True:
        return False
    return get_address_alias(address) in ["weth", "frxETH"]


def is_eth_swap_pool(address):
    if is_address(address) != True:
        return False
    return get_address_alias(address) in ETH_SWAP_POOLS_ALIAS

def is_curve_stable_swap(string):
    pattern = re.compile(CURVE_STABLE_SWAP_PATTERN)
    return pattern.match(string) != None

def is_uniswapv3_swap(string):
    pattern = re.compile(UNISWAP_V3_SWAP_PATTERN)
    return pattern.match(string) != None

def is_llamma_swap(string):
    pattern = re.compile(LLAMMA_SWAP_PATTERN)
    return pattern.match(string) != None

def get_token_by_swap_name(string):
    if is_curve_stable_swap(string) or is_llamma_swap(string) or is_uniswapv3_swap(string):
        string_list = re.split("-", string)
        if len(string_list) == 3:
            return string_list[1], string_list[2], ""
        if len(string_list) == 4:
            return string_list[1], string_list[2], string_list[3]
    return "", "", ""