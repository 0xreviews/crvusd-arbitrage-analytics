# swap pool pattern
CURVE_STABLE_SWAP_PATTERN = "^CurveStableSwap-[a-zA-Z]+-[a-zA-Z]+$"
UNISWAP_V3_SWAP_PATTERN = "^UniswapV3Pool-[a-zA-Z]+-[a-zA-Z]+$"
LLAMMA_SWAP_PATTERN = "^LLAMMA-[a-zA-Z]+-[a-zA-Z]+$"

# Token flow
WETH_FLOW = ["WETH_deposit", "WETH_withdraw", "WETH_transfer"]
FRXETH_FLOW = [
    "frxETH_stake:frxETH_in",
    "frxETH_stake:sFrxETH_out",
    "frxETH_unstake:sFrxETH_in",
    "frxETH_unstake:frxETH_out",
    "frxETH_transfer",
]
SWAPPOOL_TYPE = [
    "CurveStableSwapPool",
    "CurveCryptoSwapPool",
    "LLAMMAPool",
    "UniswapV3Pool",
    "UniswapV2Pool",
]
CURVE_STABLE_SWAP_FLOW = ["CurveStableSwap_token_in", "CurveStableSwap_token_out"]
LLAMMA_SWAP_FLOW = ["LLAMMA_token_in", "LLAMMA_token_out"]
UNISWAP_V3_SWAP_FLOW = ["UniswapV3Pool_token_in", "UniswapV3Pool_token_out"]
