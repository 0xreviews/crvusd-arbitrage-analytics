import re
from config.constance import ADDRESS_ALIAS, ADDRESS_PATTERN, ETH_SWAP_POOLS_ALIAS, TOKEN_DECIMALS


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