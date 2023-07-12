# Address
ADDRESS_PATTERN = "^0x[a-fA-F0-9]{40}$"
ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"

ADDRESS_ALIAS = {
    "0x0000000000000000000000000000000000000000": "ADDRESS_ZERO",
    # LLAMMA and Controller
    "0x8472a9a7632b173c8cf3a86d3afec50c35548e76": "Controller-sFrxETH",
    "0x136e783846ef68c8bd00a3369f787df8d683a696": "LLAMMA-sFrxETH-crvUSD",
    "0x37417b2238aa52d0dd2d6252d989e728e8f706e4": "LLAMMA-wstETH-crvUSD",
    "0x1681195c176239ac5e72d9aebacf5b2492e0c4ee": "LLAMMA-WETH-crvUSD",
    "0xe0438eb3703bf871e31ce639bd351109c88666ea": "LLAMMA-WBTC-crvUSD",
    # token
    "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": "eth",
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "weth",
    "0xf939e0a03fb07f59a73314e73794be0e57ac1b4e": "crvUSD",
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
    "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
    "0x6b175474e89094c44da98b954eedeac495271d0f": "DAI",
    "0x0ab87046fbb341d058f17cbc4c1133f25a20a52f": "gOHM",
    # frxETH
    "0x5e8422345238f34275888049021821e8e08caa1f": "frxETH",
    "0xac3e018457b222d93114458476f3e3416abbe38f": "sFrxETH",
    "0xbafa44efe7901e04e39dad13167d089c559c1138": "frxETHMinter",
    # wstETH
    "0xae7ab96520de3a18e5e111b5eaab095312d7fe84": "stETH",
    "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0": "wstETH",
    # rETH
    "0xae78736cd615f374d3085123a210448e74fc6393": "rETH",
    # CurveSwapPool
    "0xa1f8a6807c402e4a15ef4eba36528a3fed24e577": "CurveStableSwap-ETH-FRXETH",
    "0x21e27a5e5513d6e65c4f830167390997aa84843a": "CurveStableSwap-ETH-stETH",
    "0x4dece678ceceb27446b35c672dc7d61f30bad69e": "CurveStableSwap-crvUSD-USDC",
    "0x390f3595bca2df7d23783dfd126427cceb997bf4": "CurveStableSwap-crvUSD-USDT",
    "0xca978a0528116dda3cba9acd3e68bc6191ca53d0": "CurveStableSwap-crvUSD-USDP",
    "0x34d655069f4cac1547e4c8ca284ffff5ad4a8db0": "CurveStableSwap-crvUSD-TUSD",
    "0x0cd6f267b2086bea681e922e19d40512511be538": "CurveStableSwap-crvUSD-FRAX",
    "0xecd5e75afb02efa118af914515d6521aabd189f1": "CurveStableSwap-TUSD-3POOL",
    "0xc270b3b858c335b6ba5d5b10e2da8a09976005ad": "CurveStableSwap-USDP-3POOL",
    "0xdcef968d416a41cdac0ed8702fac8128a64241a2": "CurveStableSwap-FRAX-USDC",
    "0xdc24316b9ae028f1497c275eb9192a3ea0f67022": "CurveStableSwap-stETH-USDT",
    "0x497ce58f34605b9944e6b15ecafe6b001206fd25": "CurveStableSwap-LUSD-crvFRAX",  # crvFRAX is FRAX/USDC LP token
    "0x13b876c26ad6d21cb87ae459eaf6d7a1b788a113": "CurveStableSwap-BADGER-crvFRAX",
    "0x453d92c7d4263201c69aacfaf589ed14202d83a4": "CurveStableSwap-crv-ycrv",
    "0x7b0eff0c991f0aa880481fdfa5624cb0bc9b10e1": "CurveStableSwap-ETH-stETH-frxETH-rETH",
    "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7": "Curve3Pool-DAI-USDC-USDT",
    "0x0f3159811670c117c372428d4e69ac32325e4d0f": "CurveCryptoSwap-ETH-rETH",
    "0x47d5e1679fe5f0d9f0a657c6715924e33ce05093": "CurveCryptoSwap-frxETH-CVX",
    "0xbec570d92afb7ffc553bdd9d4b4638121000b10d": "CurveCryptoSwap-CVX-crvFRAX",
    "0xfc1e8bf3e81383ef07be24c3fd146745719de48d": "CurveCryptoSwap-OHM-crvFRAX",
    "0xd51a44d3fae010294c616388b506acda1bfaae46": "CurveTriCrypto-WBTC-ETH-USDT", # TriCrypto2
    "0x80466c64868e1ab14a1ddf27a676c3fcbe638fe5": "CurveTriCrypto-USDT-WBTC-WETH", # TriCrypto1
    "0x7f86bf177dd4f3494b841a37e810a34dd56c829b": "CurveTriCryptoNG-WBTC-USDC",
    "0xf5f5b97624542d72a9e06f04804bf81baa15e2b4": "CurveTriCryptoNG-WBTC-ETH-USDT",
    "0x50f3752289e1456bfa505afd37b241bca23e685d": "CurveTriCrypto-WBTC-BADGER",
    "0xecb456ea5365865ebab8a2661b0c503410e9b347": "CurveStablePoolOwner",
    "0x99a58482bd75cbab83b27ec03ca68ff489b5788f": "CurveSwapRouter",
    # UniswapPool
    "0x11b815efb8f581194ae79006d24e0d814b7697f6": "UniswapV3Pool-WETH-USDT:fee_500",
    "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36": "UniswapV3Pool-WETH-USDT:fee_3000",
    "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640": "UniswapV3Pool-WETH-USDC:fee_500",
    "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8": "UniswapV3Pool-WETH-USDC:fee_3000",
    "0x8a15b2dc9c4f295dcebb0e7887dd25980088fdcb": "UniswapV3Pool-WETH-frxETH:fee_500",
    "0x109830a1aaad605bbf02a9dfa7b0b92ec2fb7daa": "UniswapV3Pool-WETH-wstETH:fee_100",
    "0xa4e0faa58465a2d369aa21b3e42d43374c6f9613": "UniswapV3Pool-WETH-rETH:fee_500",
    "0x5720eb958685deeeb5aa0b34f677861ce3a8c7f5": "UniswapV3Pool-USDC-USDP:fee_500",
    "0xd340b57aacdd10f96fc1cf10e15921936f41e29c": "UniswapV3Pool-WETH-wstETH:fee_500",
    "0x4622df6fb2d9bee0dcdacf545acdb6a2b2f4f863": "UniswapV3Pool-USDC-wstETH:fee_500",
    "0x9a772018fbd77fcd2d25657e5c547baff3fd7d16": "UniswapV3Pool-WBTC-USDC:fee_500",
    "0x9db9e0e53058c89e5b94e29621a205198648425b": "UniswapV3Pool-WBTC-USDC:fee_3000",
    "0x4585fe77225b41b697c938b018e2ac67ac5a20c0": "UniswapV3Pool-WBTC-WETH:fee_500",
    "0xcbcdf9626bc03e24f779434178a73a0b4bad62ed": "UniswapV3Pool-WBTC-WETH:fee_3000",
    "0x08f68110f1e0ca67c80a24b4bd206675610f445d": "UniswapV3Pool-USDC-gOHM:fee_3000",
    "0x190ed02adaf1ef8039fcd3f006b42553467d5045": "UniswapV3Pool-USDC-RUSDC:fee_500",
    "0xe15e6583425700993bd08f51bf6e7b73cd5da91b": "UniswapV3Pool-WBTC-BADGER:fee_3000",
    "0x2498436a3eb56b9b944d4f8e3704456a86645227": "UniswapV3Pool-WBTC-AUSD:fee_10000",
    # CurvePool LP token
    "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490": "Curve3PoolLP-DAI-USDC-USDT",
    "0x3175df0976dfa876431c2e9ee6bc45b65d3473cc": "CurveStableSwapLP-USDC-FRAX",
    "0x6e52cce4eafdf77091dd1c82183b2d97b776b397": "CurveStableSwapLP-frxETH-CVX",
    "0x09b2e090531228d1b8e3d948c73b990cb6e60720": "CurveStableSwapLP-BADGER-crvFRAX",
    "0x33baeda08b8afacc4d3d07cf31d49fc1f1f3e893": "CurveStableSwapLP-TUSD-crvFRAX",
    # PancakeSwapPool
    "0x6ca298d2983ab03aa1da7679389d955a4efee15c": "PancakeV3Pool-WETH-USDT",
    "0x5c9c6f39ce25cc6d0f39410f890933a1476fb1b0": "PancakeV3Pool-WETH-frxETH",
    "0x4f64951a6583d56004ff6310834c70d182142a07": "PancakeV3Pool-WETH-wstETH",
    "0x9b5699d18dff51fc65fb8ad6f70d93287c36349f": "PancakeV3Pool-WETH-WBTC",
    "0x1ac1a8feaaea1900c4166deeed0c11cc10669d36": "PancakeV3Pool-WETH-USDC",
    # SolidlySwapPool
    "0x4e30fc7ccd2df3ddca39a69d2085334ee63b9c96": "SolidlySwap-WETH-frxETH",
    "0x8362b08718a09f1902e00f34039923a2262a6fcf": "SolidlySwap-WETH-frxETH",
    # 1inch
    "0x1111111254fb6c44bac0bed2854e76f90643097d": "1inchAggregationRouterV4",
    "0x1111111254eeb25477b68fb85ed929f73a960582": "1inchAggregationRouterV5",
    "0xa88800cd213da5ae406ce248380802bd53b47647": "1inchSettlement",
    "0x08b067ad41e45babe5bbb52fc2fe7f692f628b06": "1inchWethUnwrapper",
    "0x92f3f71cef740ed5784874b8c70ff87ecdf33588": "1inchAggregationExecutor:01",
    "0x19ea2e6f21bdfc894abf09fa179d59f6c0e0797b": "1inchAggregationExecutor:02",
    "0xda63a326d2c3c09586676a036e79af2e3c524090": "1inchAggregationExecutor:03",
    # Other swap pool
    "0xba12222222228d8ba445958a75a0704d566bf2c8": "BalancerVault",
    "0x1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e": "dYdXSoloMargin",
    "0xb63cac384247597756545b500253ff8e607a8020": "OlympusStaking",
    "0xef608497df0f4c8bea4dcacf11b712a646f49fba": "MaverickPool-WBTC-WETH:fee_400",
    "0x53dc703b78794b61281812f3a901918253beefee": "MaverickPool-DAI-USDC:fee_500",
    "0xe8d7a52aabe8a0569314f28e90fdb8544860a424": "MaverickPool-USDT-USDC:fee_100",
    "0x11a653ddfbb61e0feff5484919f06d9d254bf65f": "MaverickPool-WETH-USDC:fee_400",
    "0xa86689118d8d940d6ad729c2d7872da3fa20dd40": "KekPool",
    "0x1cf68bbc2b6d3c6cfe1bd3590cf0e10b06a05f17": "KyberPool-WEBTC-WETH",
    "0x74de5d4fcbf63e00296fd95d33236b9794016631": "AirPool",
    # Other
    "0xeb4af8a64070ef0dea6260e0bf2310748f014d88": "MimicSmartVault:01",
    "0xa7ca2c8673bcfa5a26d8ceec2887f2cc2b0db22a": "MimicSmartVault:02",
    "0xe68c1d72340aeefe5be76eda63ae2f4bc7514110": "DeFiPlaza",
}

ALIAS_TO_ADDRESS = {}
for addr, alias in ADDRESS_ALIAS.items():
    ALIAS_TO_ADDRESS[alias] = addr
