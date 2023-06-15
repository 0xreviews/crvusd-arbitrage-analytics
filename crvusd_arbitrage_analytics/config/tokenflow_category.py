# swap pool pattern
CURVE_ROUTER_PATTERN = "CurveSwapRouter"
CURVE_SWAP_PATTERN = "^(CurveStableSwap|Curve3Pool|CurveCryptoSwap|CurveTriCrypto|CurveTriCryptoNG)(-[0-9a-zA-Z]+)+$"
UNISWAP_V3_SWAP_PATTERN = "^UniswapV3Pool(-[0-9a-zA-Z]+)+(:fee_[0-9]+)?$"
LLAMMA_SWAP_PATTERN = "^LLAMMA(-[0-9a-zA-Z]+)+$"
PANCAKE_SWAP_PATTERN = "^PancakeV3Pool(-[0-9a-zA-Z]+)+"
BALANCER_VAULT_PATTERN = "^BalancerVault"
SOLIDLY_SWAP_PATTERN = "^SolidlySwap(-[0-9a-zA-Z]+)+"

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
SWAPPOOL_TYPE = [
    "CurveRouter",
    "CurveSwapPool",
    "LLAMMAPool",
    "UniswapPool",
    "PancakePool",
    "SolidlySwapPool",
    "BalancerVault",
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
    "CurveSwap:WETH_deposit_eth_out",
    "CurveSwap:WETH_deposit_weth_in",
    "CurveSwap:WETH_withdraw_weth_out",
    "CurveSwap:WETH_withdraw_eth_in",
]
CURVE_META_SWAP_FLOW = [
    "CurveSwap:MetaPool_3Pool_token_in",
    "CurveSwap:MetaPool_3Pool_token_out",
    "CurveSwap:MetaPool_3Pool_LP_in",
    "CurveSwap:MetaPool_3Pool_LP_out",
    "CurveSwap:MetaPool_3Pool_LP_mint",
    "CurveSwap:MetaPool_3Pool_LP_burn",
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

FLASH_POOL_TYPE = [
    "UniswapSwap",
    "PancakeSwap",
    "SolidlySwap",
    "BalancerVault",
]
BALANCER_VAULT_FLOW = ["BalancerVault:token_out", "BalancerVault:token_in"]

ACTION_GROUP_TYPE = [
    "CurveRouter",
    "CurveSwap",
    "UniswapSwap",
    "PancakeSwap",
    "SolidlySwap",
    "BalancerVault",
    "LLAMMA",
    "WETH",
    "stETH",
    "frxETH",
]

ACTION_GROUP_TAG = ["begin", "doing", "end"]

# Take profit flow
TAKE_PROFIT_FLOW = ["miner_take_profit", "beneficiary_take_profit"]