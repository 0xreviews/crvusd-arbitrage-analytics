# swap pool pattern
CURVE_STABLE_SWAP_PATTERN = "^CurveStableSwap-[a-zA-Z]+-[a-zA-Z]+$"
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
    "CurveStableSwapPool",
    "CurveCryptoSwapPool",
    "LLAMMAPool",
    "UniswapV3Pool",
    "UniswapV2Pool",
    "BalancerVault",
]
CURVE_STABLE_SWAP_FLOW = [
    "CurveStableSwap:token_in",
    "CurveStableSwap:token_out",
    "CurveStableSwap:token_in:flash_swap",
    "CurveStableSwap:token_out:flash_swap",
]
LLAMMA_SWAP_FLOW = [
    "LLAMMA:token_in",
    "LLAMMA:token_out",
    "LLAMMA:token_in:flash_swap",
    "LLAMMA:token_out:flash_swap",
]
UNISWAP_V3_SWAP_FLOW = [
    "UniswapV3Pool:token_in",
    "UniswapV3Pool:token_out",
    "UniswapV3Pool:token_in:flash_swap",
    "UniswapV3Pool:token_out:flash_swap",
]

FLASH_POOL_TYPE = ["BalancerVault"]
BALANCER_VAULT_FLOW = ["BalancerVault:FLASH_borrow", "BalancerVault:FLASH_repay"]

# Take profit flow
TAKE_PROFIT_FLOW = ["miner_take_profit", "beneficiary_take_profit"]
