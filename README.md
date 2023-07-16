# crvUSD Arbitrage Analystics

This tool visualizes crvUSD LLAMMA pool's arbitraging process and conducts statistical analysis.

## Getting Started

- Install

```sh
poetry install
```

- Generate arbitrage tokenflow chart by transacation hash (dot file and png file)

```sh
poetry shell

python crvusd_arbitrage_analytics/tokenflow.py 0x0806a484daf46bf1948185fac7f13613268da0969d638bc87dc934eefeab6b13
```

## Basic Use

Fetch all arbitrage data and automatically classify, statistics, and generate tokenflow chart.

0. Fetch all arbitrage transacation data, and collateral price data, save raw data in `data/original`
1. Wash raw data, save csv file and json file in `data/csv/tokenflow_data_[collateral]`, `data/json/tokenflow_data_[collateral]`
   - Automatically identify the behavior type of each token transfer
   - Log all swap pools
   - Group all tx steps, e.g. flashswap, sFrxETH stake/unstake, WETH deposit/withdraw, token swap in/out
2. Classify all arbitrage tokenflow
3. Generate statistical graphs
4. Generate tokenflow chart for each arbitrage category

```sh
python scripts/0_fetch_data.py
python scripts/1_wash_data.py
python scripts/2_sort_data.py
python scripts/3_draw_graph.py
python scripts/4_statistics_data.py
```

## Results

Some statistical graphs and token flow charts (statistics date: 2023-07-15):

### Statistics

#### Daily revenue and gascost

![](./results/stat/sFrxETH/stat_daily_revenue_gascost_sfrxeth.png)

![](./results/stat/wstETH/stat_daily_revenue_gascost_wsteth.png)

![](./results/stat/WBTC/stat_daily_revenue_gascost_wbtc.png)

![](./results/stat/WETH/stat_daily_revenue_gascost_weth.png)

#### revenue volume scatter

![](./results/stat/sFrxETH/stat_scatter_revenue_volume_sfrxeth.png)

![](./results/stat/wstETH/stat_scatter_revenue_volume_wsteth.png)

![](./results/stat/WBTC/stat_scatter_revenue_volume_wbtc.png)

![](./results/stat/WETH/stat_scatter_revenue_volume_weth.png)


#### sFrxETH Dominance

![](./results/stat/sFrxETH/dominance_sfrxeth.png)

#### wstETH Dominance

![](./results/stat/wstETH/dominance_wsteth.png)

#### WBTC Dominance

![](./results/stat/WBTC/dominance_wbtc.png)

#### WETH Dominance

![](./results/stat/wstETH/dominance_weth.png)


### Tokenflow

#### sFrxETH LLAMMA Pool

![](./results/tokenflow/How-to-Arbitrage-on-LLAMMA_sFrxETH.png)

The three most frequently used arbitrage methods:

![](./results/tokenflow/sFrxETH/type_1.png)

![](./results/tokenflow/sFrxETH/type_2.png)

![](./results/tokenflow/sFrxETH/type_3.png)

#### wstETH LLAMMA Pool

![](./results/tokenflow/How-to-Arbitrage-on-LLAMMA_wstETH.png)

The three most frequently used arbitrage methods:

![](./results/tokenflow/wstETH/type_1.png)

![](./results/tokenflow/wstETH/type_2.png)

![](./results/tokenflow/wstETH/type_3.png)

#### WBTC LLAMMA Pool

The three most frequently used arbitrage methods:

![](./results/tokenflow/WBTC/type_1.png)

![](./results/tokenflow/WBTC/type_2.png)

![](./results/tokenflow/WBTC/type_3.png)

#### WETH LLAMMA Pool

The three most frequently used arbitrage methods:

![](./results/tokenflow/WETH/type_1.png)

![](./results/tokenflow/WETH/type_2.png)

![](./results/tokenflow/WETH/type_3.png)


More data and picture results can be seen in [results folder](./results).
