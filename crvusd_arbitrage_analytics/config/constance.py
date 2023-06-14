# subgraph
from string import Template


SUBGRAPH_ENDPOINT = "https://api.thegraph.com/subgraphs/name/0x-stan/curve-stablecoin"
SUBGRAPH_QUERY_SIZE = 1000

# eigenPhi
EIGEN_TX_URL = "https://eigenphi.io/mev/eigentx/"
EIGEN_ANALYTICS_TX = "https://eigenphi.io/api/v1/analyseTransaction?chain=ALL&enableCallStack=on&tx="
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
    # LLAMMA and Controller
    "0x8472a9a7632b173c8cf3a86d3afec50c35548e76": "Controller-sFrxETH",
    "0x136e783846ef68c8bd00a3369f787df8d683a696": "LLAMMA-sFrxETH-crvUSD",
    "0x37417b2238aa52d0dd2d6252d989e728e8f706e4": "LLAMMA-wstETH-crvUSD",
    # token
    "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": "eth",
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "weth",
    "0xf939e0a03fb07f59a73314e73794be0e57ac1b4e": "crvUSD",
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
    "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
    "0x0ab87046fbb341d058f17cbc4c1133f25a20a52f": "gOHM",
    # frxETH
    "0x5e8422345238f34275888049021821e8e08caa1f": "frxETH",
    "0xac3e018457b222d93114458476f3e3416abbe38f": "sFrxETH",
    "0xbafa44efe7901e04e39dad13167d089c559c1138": "frxETHMinter",
    # rETH
    "0xae78736cd615f374d3085123a210448e74fc6393": "rETH",
    # UniswapPool
    "0x11b815efb8f581194ae79006d24e0d814b7697f6": "UniswapV3Pool-WETH-USDT:fee_500",
    "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36": "UniswapV3Pool-WETH-USDT:fee_3000",
    "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640": "UniswapV3Pool-WETH-USDC:fee_500",
    "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8": "UniswapV3Pool-WETH-USDC:fee_3000",
    "0x8a15b2dc9c4f295dcebb0e7887dd25980088fdcb": "UniswapV3Pool-WETH-frxETH:fee_500",
    "0xa4e0faa58465a2d369aa21b3e42d43374c6f9613": "UniswapV3Pool-WETH-rETH:fee_500",
    "0xd340b57aacdd10f96fc1cf10e15921936f41e29c": "UniswapV3Pool-WETH-wstETH:fee_500",
    "0x08f68110f1e0ca67c80a24b4bd206675610f445d": "UniswapV3Pool-USDC-gOHM:fee_3000",
    # CurveSwapPool
    "0xa1f8a6807c402e4a15ef4eba36528a3fed24e577": "CurveStableSwap-ETH-FRXETH",
    "0x4dece678ceceb27446b35c672dc7d61f30bad69e": "CurveStableSwap-crvUSD-USDC",
    "0x390f3595bca2df7d23783dfd126427cceb997bf4": "CurveStableSwap-crvUSD-USDT",
    "0xca978a0528116dda3cba9acd3e68bc6191ca53d0": "CurveStableSwap-crvUSD-USDP",
    "0x34d655069f4cac1547e4c8ca284ffff5ad4a8db0": "CurveStableSwap-crvUSD-TUSD",
    "0xecd5e75afb02efa118af914515d6521aabd189f1": "CurveStableSwap-TUSD-3POOL",
    "0xdcef968d416a41cdac0ed8702fac8128a64241a2": "CurveStableSwap-FRAX-USDC",
    "0x497ce58f34605b9944e6b15ecafe6b001206fd25": "CurveStableSwap-LUSD-crvFRAX",  # crvFRAX is FRAX/USDC LP token
    "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7": "Curve3Pool-DAI-USDC-USDT",
    "0x0f3159811670c117c372428d4e69ac32325e4d0f": "CurveCryptoSwap-ETH-rETH",
    "0x47d5e1679fe5f0d9f0a657c6715924e33ce05093": "CurveCryptoSwap-frxETH-CVX",
    "0xbec570d92afb7ffc553bdd9d4b4638121000b10d": "CurveCryptoSwap-CVX-crvFRAX",
    "0xd51a44d3fae010294c616388b506acda1bfaae46": "CurveTriCrypto-WBTC-ETH-USDT",
    "0x7f86bf177dd4f3494b841a37e810a34dd56c829b": "CurveTriCryptoNG-WBTC-USDC",
    "0xecb456ea5365865ebab8a2661b0c503410e9b347": "CurveStablePoolOwner",
    "0x99a58482bd75cbab83b27ec03ca68ff489b5788f": "CurveSwapRouter",
    # CurvePool LP token
    "0x3175df0976dfa876431c2e9ee6bc45b65d3473cc": "CurveStableSwapLP-USDC-FRAX",
    "0x6e52cce4eafdf77091dd1c82183b2d97b776b397": "CurveStableSwapLP-frxETH-CVX",
    "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490": "CurveStableSwapLP-DAI-USDC-USDT",
    # PancakeSwapPool
    "0x6ca298d2983ab03aa1da7679389d955a4efee15c": "PancakeV3Pool-WETH-USDT",
    "0x5c9c6f39ce25cc6d0f39410f890933a1476fb1b0": "PancakeV3Pool-WETH-frxETH",
    # SolidlySwapPool
    "0x4e30fc7ccd2df3ddca39a69d2085334ee63b9c96": "SolidlySwap-WETH-frxETH",
    "0x8362b08718a09f1902e00f34039923a2262a6fcf": "SolidlySwap-WETH-frxETH",
    # Other swap pool
    "0xba12222222228d8ba445958a75a0704d566bf2c8": "BalancerVault",
    "0x1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e": "dYdXSoloMargin",
    "0xb63cac384247597756545b500253ff8e607a8020": "OlympusStaking",
}

ALIAS_TO_ADDRESS = {}
for addr, alias in ADDRESS_ALIAS.items():
    ALIAS_TO_ADDRESS[alias] = addr

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
