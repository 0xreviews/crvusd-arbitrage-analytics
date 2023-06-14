# swap pool pattern
CURVE_ROUTER_PATTERN = "CurveSwapRouter"
CURVE_SWAP_PATTERN = "^(CurveStableSwap|Curve3Pool|CurveCryptoSwap|CurveTriCrypto|CurveTriCryptoNG)(-[a-zA-Z]+)+$"
UNISWAP_V3_SWAP_PATTERN = "^UniswapV3Pool-[a-zA-Z]+-[a-zA-Z]+$"
LLAMMA_SWAP_PATTERN = "^LLAMMA-[a-zA-Z]+-[a-zA-Z]+$"
BALANCER_VAULT_PATTERN = "^BalancerVault"

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
    "frxETH_stake:frxETH_in",
    "frxETH_stake:sFrxETH_out",
    "frxETH_unstake:sFrxETH_in",
    "frxETH_unstake:frxETH_out",
    "frxETH_transfer",
    "sfrxETH_transfer",
    "frxETH_mint:eth_in",
    "frxETH_mint:frxETH_out",
]
SWAPPOOL_TYPE = [
    "CurveRouter",
    "CurveSwapPool",
    "LLAMMAPool",
    "UniswapV3Pool",
    "UniswapV2Pool",
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
LLAMMA_SWAP_FLOW = [
    "LLAMMA:token_in",
    "LLAMMA:token_out",
]
UNISWAP_V3_SWAP_FLOW = [
    "UniswapV3Pool:token_in",
    "UniswapV3Pool:token_out",
]

FLASH_POOL_TYPE = ["BalancerVault"]
BALANCER_VAULT_FLOW = ["BalancerVault:FLASH_borrow", "BalancerVault:FLASH_repay"]

ACTION_GROUP_TYPE = [
    "CurveRouterSwap"
]

ACTION_GROUP_TAG = ["begin", "doing", "end"]

# Take profit flow
TAKE_PROFIT_FLOW = ["miner_take_profit", "beneficiary_take_profit"]
