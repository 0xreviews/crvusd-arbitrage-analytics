# swap pool pattern
CURVE_STABLE_SWAP_PATTERN = "^CurveStableSwap-[a-zA-Z]+-[a-zA-Z]+$"
UNISWAP_V3_SWAP_PATTERN = "^UniswapV3Pool-[a-zA-Z]+-[a-zA-Z]+$"
LLAMMA_SWAP_PATTERN = "^LLAMMA-[a-zA-Z]+-[a-zA-Z]+$"

# Token flow
WETH_FLOW = [
    "WETH_deposit:eth_in",
    "WETH_deposit:weth_out",
    "WETH_withdraw:weth_in",
    "WETH_withdraw:eth_out",
    "WETH_transfer",
]
FRXETH_FLOW = [
    "frxETH_stake:frxETH_in",
    "frxETH_stake:sFrxETH_out",
    "frxETH_unstake:sFrxETH_in",
    "frxETH_unstake:frxETH_out",
    "frxETH_transfer",
    "sfrxETH_transfer",
]
SWAPPOOL_TYPE = [
    "CurveStableSwapPool",
    "CurveCryptoSwapPool",
    "LLAMMAPool",
    "UniswapV3Pool",
    "UniswapV2Pool",
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

# Take profit flow
TAKE_PROFIT_FLOW = ["miner_take_profit", "beneficiary_take_profit"]
