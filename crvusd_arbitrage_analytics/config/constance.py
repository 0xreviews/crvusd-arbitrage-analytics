# subgraph
from string import Template


SUBGRAPH_ENDPOINT = "https://api.thegraph.com/subgraphs/name/0x-stan/curve-stablecoin"
SUBGRAPH_QUERY_SIZE = 1000

# eigenPhi
EIGEN_TX_URL = "https://eigenphi.io/mev/eigentx/"
EIGEN_ANALYTICS_TX = "https://eigenphi.io/api/v1/analyseTransaction?chain=ALL&tx="
EIGEN_SUMMARY_TX = "https://storage.googleapis.com/eigenphi-ethereum-tx/"

# Tenderly
TENDERLY_TX_TRACE = Template(
    "https://api.tenderly.co/api/v1/public-contract/$networkId/trace/$tx"
)

# Address
ADDRESS_PATTERN = "^0x[a-fA-F0-9]{40}$"
ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"

ADDRESS_ALIAS = {
    "0x0000000000000000000000000000000000000000": "ADDRESS_ZERO",
    "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": "eth",
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "weth",
    "0xf939e0a03fb07f59a73314e73794be0e57ac1b4e": "crvUSD",
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
    "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
    "0x5e8422345238f34275888049021821e8e08caa1f": "frxETH",
    "0xac3e018457b222d93114458476f3e3416abbe38f": "sFrxETH",
    "0x8472a9a7632b173c8cf3a86d3afec50c35548e76": "Controller-sFrxETH",
    "0x136e783846ef68c8bd00a3369f787df8d683a696": "LLAMMA-sFrxETH-crvUSD",
    "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640": "UniswapV3Pool-WETH-USDC",
    "0x11b815efb8f581194ae79006d24e0d814b7697f6": "UniswapV3Pool-WETH-USDT",
    "0xa1f8a6807c402e4a15ef4eba36528a3fed24e577": "CurveStableSwap-ETH-FRXETH",
    "0x4dece678ceceb27446b35c672dc7d61f30bad69e": "CurveStableSwap-crvUSD-USDC",
    "0x390f3595bca2df7d23783dfd126427cceb997bf4": "CurveStableSwap-crvUSD-USDT",
    "0xca978a0528116dda3cba9acd3e68bc6191ca53d0": "CurveStableSwap-crvUSD-USDP",
    "0x34d655069f4cac1547e4c8ca284ffff5ad4a8db0": "CurveStableSwap-crvUSD-TUSD",
    "0xba12222222228d8ba445958a75a0704d566bf2c8": "BalancerVault",
}

ALIAS_TO_ADDRESS = {
    "ADDRESS_ZERO": "0x0000000000000000000000000000000000000000",
    "eth": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "weth": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "crvUSD": "0xf939e0a03fb07f59a73314e73794be0e57ac1b4e",
    "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "frxETH": "0x5e8422345238f34275888049021821e8e08caa1f",
    "sFrxETH": "0xac3e018457b222d93114458476f3e3416abbe38f",
    "Controller-sFrxETH": "0x8472a9a7632b173c8cf3a86d3afec50c35548e76",
    "LLAMMA-sFrxETH-crvUSD": "0x136e783846ef68c8bd00a3369f787df8d683a696",
    "UniswapV3Pool-WETH-USDC": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
    "UniswapV3Pool-WETH-USDT": "0x11b815efb8f581194ae79006d24e0d814b7697f6",
    "CurveStableSwap-ETH-FRXETH": "0xa1f8a6807c402e4a15ef4eba36528a3fed24e577",
    "CurveStableSwap-crvUSD-USDC": "0x4dece678ceceb27446b35c672dc7d61f30bad69e",
    "CurveStableSwap-crvUSD-USDT": "0x390f3595bca2df7d23783dfd126427cceb997bf4",
    "CurveStableSwap-crvUSD-USDP": "0xca978a0528116dda3cba9acd3e68bc6191ca53d0",
    "CurveStableSwap-crvUSD-TUSD": "0x34d655069f4cac1547e4c8ca284ffff5ad4a8db0",
    "BalancerVault": "0xba12222222228d8ba445958a75a0704d566bf2c8",
}

TOKEN_DECIMALS = {
    "eth": 18,
    "weth": 18,
    "frxeth": 18,
    "sfrxeth": 18,
    "steth": 18,
    "wsteth": 18,
    "crvusd": 18,
    "usdc": 6,
    "usdt": 6,
}

ETH_SWAP_POOLS_ALIAS = ["CurveStableSwap-ETH-FRXETH", "UniswapV3Pool-WETH-USDC"]



