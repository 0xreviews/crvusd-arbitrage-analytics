DIAGRAM_COLORS = ["#18c0c4", "#f62196", "#A267F5", "#f3907e", "#ffe46b", "#428449"]
DIAGRAM_LINE_COLOR = "#fefeff"
DIAGRAM_LAYOUT_NAME = ["Token in", "Soft-Liquidation", "Token out"]
DIAGRAM_COINS = ["crvUSD", "ETH", "WETH", "WBTC", "frxETH", "sfrxETH", "stETH", "wstETH", "rETH", "USDT", "USDC", "TUSD", "USDP", "FRAX"]
DIAGRAM_NODE_CONFIG = {
    "tx_from": {
        "shape": "diamond",
    },
    "arbitrage_contract": {
        "shape": "diamond",
    },
    "arbitrageur": {
        "shape": "diamond",
    },
    "coin": {
        "shape": "hexagon",
        "fillcolor": DIAGRAM_COLORS[0],
        "color": DIAGRAM_LINE_COLOR,
        "fontcolor": "white",
    },
    "flash_borrow": {
        "shape": "house",
        "fillcolor": DIAGRAM_COLORS[2],
        "color": DIAGRAM_LINE_COLOR,
        "fontcolor": "white",
    },
    "flash_repay": {
        "shape": "invhouse",
        "fillcolor": DIAGRAM_COLORS[2],
        "color": DIAGRAM_LINE_COLOR,
        "fontcolor": "white",
    },
    "CurveSwapRouter": {
        "shape": "house",
        "color": DIAGRAM_COLORS[1],
        "fillcolor": "transparent",
    },
    "LLAMMA": {
        "shape": "cylinder",
        "fillcolor": DIAGRAM_COLORS[5],
        "color": DIAGRAM_LINE_COLOR,
        "fontcolor": "white",
    },
    "CurveSwapPool": {
        "shape": "ellipse",
        "fillcolor": DIAGRAM_COLORS[1],
        "color": DIAGRAM_LINE_COLOR,
        "fontcolor": "white",
    },
    "CurveStable_crvUSD": {
        "shape": "cylinder",
        "fillcolor": DIAGRAM_COLORS[1],
        "color": DIAGRAM_LINE_COLOR,
        "fontcolor": "white",
    },
    "UniswapPool": {
        "shape": "ellipse",
        "fillcolor": DIAGRAM_COLORS[2],
        "color": DIAGRAM_LINE_COLOR,
        "fontcolor": "white",
    },
    "wrapped_eth": {
        "shape": "doubleoctagon",
        "fillcolor": DIAGRAM_COLORS[4],
         "color": DIAGRAM_LINE_COLOR,
        "fontcolor": "black",
    },
}

DIAGRAM_SUBGRAPH_WRAPPED_ETH = [
    "frxETH",
    "sfrxETH",
    "stETH",
    "wstETH",
    "WETH",
    "rETH",
    "CurveSwapWETH",
]

DIAGRAM_SUBGRAPH_SWAP = [
    "CurveSwap",
    "CurveMetaPool_Swap",
]

DIAGRAM_SUBGRAPH_CONFIG = {
    "wrapped_eth": {
        "style": "filled, rounded",
        "fillcolor": "transparent",
        "color": DIAGRAM_LINE_COLOR,
    },
    "swap": {"style": "filled, rounded", "fillcolor": "transparent"},
    "LLAMMA": {"style": "filled, rounded", "fillcolor": DIAGRAM_COLORS[0]},
}
