# subgraph
from string import Template


SUBGRAPH_ENDPOINT_0XREVIEWS = (
    "https://api.thegraph.com/subgraphs/name/0x-stan/curve-stablecoin"
)
SUBGRAPH_ENDPOINT_VOLUME = (
    "https://api.thegraph.com/subgraphs/name/convex-community/crvusd"
)
SUBGRAPH_QUERY_SIZE = 1000

# eigenPhi
EIGEN_TX_URL = "https://eigenphi.io/mev/eigentx/"
EIGEN_ANALYTICS_TX = (
    "https://eigenphi.io/api/v1/analyseTransaction?chain=ALL&enableCallStack=on&tx="
)
EIGEN_SUMMARY_TX = "https://storage.googleapis.com/eigenphi-ethereum-tx/"

# Tenderly
TENDERLY_TX_TRACE = Template(
    "https://api.tenderly.co/api/v1/public-contract/$networkId/trace/$tx"
)

# Coingecko api
COINGECKO_PRICE_HISTORICAL = "https://api.coingecko.com/api/v3/coins/{id}/market_chart/range"


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

SYMBOL_TO_ID = {
    "sfrxeth": "staked-frax-ether",
    "wsteth": "wrapped-steth",
}
