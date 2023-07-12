# swap pool pattern
CURVE_ROUTER_PATTERN = "CurveSwapRouter"
CURVE_SWAP_PATTERN = "^(CurveStableSwap|Curve3Pool|CurveCryptoSwap|CurveTriCrypto|CurveTriCryptoNG)(-[0-9a-zA-Z]+)+$"
UNISWAP_V3_SWAP_PATTERN = "^UniswapV3Pool(-[0-9a-zA-Z]+)+(:fee_[0-9]+)?$"
LLAMMA_SWAP_PATTERN = "^LLAMMA(-[0-9a-zA-Z]+)+$"
PANCAKE_SWAP_PATTERN = "^PancakeV3Pool(-[0-9a-zA-Z]+)+"
BALANCER_VAULT_PATTERN = "^BalancerVault"
SOLIDLY_SWAP_PATTERN = "^SolidlySwap(-[0-9a-zA-Z]+)+"
MAVERICK_SWAP_PATTERN = "^MaverickPool(-[0-9a-zA-Z]+)+"

# Token flow
WETH_FLOW = [
    "WETH_deposit:eth_in",
    "WETH_deposit:weth_out",
    "WETH_withdraw:weth_in",
    "WETH_withdraw:eth_out",
    "WETH_transfer",
]
RETH_FLOW = [
    "rETH_deposit:eth_in",
    "rETH_deposit:reth_out",
    "rETH_withdraw:reth_in",
    "rETH_withdraw:eth_out",
    "rETH_transfer",
]
FRXETH_FLOW = [
    "frxETH_mint:eth_in",
    "frxETH_mint:frxETH_out",
    "frxETH_stake:frxETH_in",
    "frxETH_stake:sFrxETH_out",
    "frxETH_unstake:sFrxETH_in",
    "frxETH_unstake:frxETH_out",
    "frxETH_transfer",
    "sfrxETH_transfer",
]
CURVE_ROUTER_FLOW = [
    "CurveRouter:token_in",
    "CurveRouter:token_out",
    "CurveRouter:token_from_pool",
    "CurveRouter:token_to_pool",
]
CURVE_SWAP_FLOW = [
    "CurveSwap:token_in",
    "CurveSwap:token_out",
]
CURVE_SWAP_WETH_FLOW = [
    "CurveSwapWETH_Deposit:eth_out",
    "CurveSwapWETH_Deposit:weth_in",
    "CurveSwapWETH_Withdraw:weth_out",
    "CurveSwapWETH_Withdraw:eth_in",
]
CURVE_META_SWAP_FLOW = [
    "CurveMetaPool_Swap:token_in",
    "CurveMetaPool_Swap:token_out",
    "CurveMetaPool_LP:LP_in",
    "CurveMetaPool_LP:LP_out",
    "CurveMetaPool_LP:LP_mint",
    "CurveMetaPool_LP:LP_burn",
]
LLAMMA_SWAP_FLOW = [
    "LLAMMA:token_in",
    "LLAMMA:token_out",
]
UNISWAP_SWAP_FLOW = [
    "UniswapSwap:token_in",
    "UniswapSwap:token_out",
]
PANCAKE_SWAP_FLOW = [
    "PancakeSwap:token_in",
    "PancakeSwap:token_out",
]
SOLIDLY_SWAP_FLOW = [
    "SolidlySwap:token_in",
    "SolidlySwap:token_out",
]
BALANCER_VAULT_FLOW = ["BalancerVault:token_out", "BalancerVault:token_in"]
MAVERRICK_SWAP_FLOW = [
    "MaverickSwap:token_in",
    "MaverickSwap:token_out",
]

ACTION_GROUP_TYPE = [
    CURVE_ROUTER_FLOW,
    CURVE_SWAP_FLOW,
    CURVE_SWAP_WETH_FLOW,
    CURVE_META_SWAP_FLOW,
    LLAMMA_SWAP_FLOW,
    UNISWAP_SWAP_FLOW,
    PANCAKE_SWAP_FLOW,
    SOLIDLY_SWAP_FLOW,
    BALANCER_VAULT_FLOW,
    MAVERRICK_SWAP_FLOW,
    WETH_FLOW,
    RETH_FLOW,
    FRXETH_FLOW,
]

ACTION_GROUP_TAG = ["begin", "doing", "end"]

ACTION_GROUP_SWAP_TYPE = [
    "CurveSwap",
    "CurveMetaPool_Swap",
    # "LLAMMA",
    "UniswapSwap",
    "PancakeSwap",
    "SolidlySwap",
    "MaverickSwap",
]


SWAPPOOL_TYPE = [
    "CurveRouter",
    "CurveSwapPool",
    "LLAMMAPool",
    "UniswapPool",
    "PancakePool",
    "SolidlySwapPool",
    "BalancerVault",
    "MaverickPool",
]
FLASH_POOL_TYPE = [
    "UniswapSwap",
    "PancakeSwap",
    "SolidlySwap",
    "BalancerVault",
]


# Take profit flow
TAKE_PROFIT_FLOW = ["miner_take_profit", "beneficiary_take_profit"]

CALL_ARBI_CONTRACT_FLOW = ["call_arbi_contract", "call_arbi_contract_with_token"]
