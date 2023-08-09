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
   - Group all tx steps, e.g. flashswap, sfrxETH stake/unstake, WETH deposit/withdraw, token swap in/out
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

Some statistical graphs and token flow charts (statistics date: 2023-08-09):

### Statistics

#### Daily revenue and gascost

![](./results/stat/sfrxETH/stat_daily_revenue_gascost_sfrxETH.png)

![](./results/stat/wstETH/stat_daily_revenue_gascost_wstETH.png)

![](./results/stat/WBTC/stat_daily_revenue_gascost_WBTC.png)

![](./results/stat/WETH/stat_daily_revenue_gascost_WETH.png)

#### revenue volume scatter

![](./results/stat/sfrxETH/stat_scatter_revenue_volume_sfrxETH.png)

![](./results/stat/wstETH/stat_scatter_revenue_volume_wstETH.png)

![](./results/stat/WBTC/stat_scatter_revenue_volume_WBTC.png)

![](./results/stat/WETH/stat_scatter_revenue_volume_WETH.png)


#### sfrxETH Dominance

![](./results/stat/sfrxETH/dominance_sfrxETH.png)

#### wstETH Dominance

![](./results/stat/wstETH/dominance_wstETH.png)

#### WBTC Dominance

![](./results/stat/WBTC/dominance_WBTC.png)

#### WETH Dominance

![](./results/stat/WETH/dominance_WETH.png)


### Tokenflow

#### sfrxETH LLAMMA Pool

![](./results/tokenflow/How-to-Arbitrage-on-LLAMMA_sfrxETH.png)

The three most frequently used arbitrage methods:

![](./results/tokenflow/sfrxETH/type_1.png)

![](./results/tokenflow/sfrxETH/type_2.png)

![](./results/tokenflow/sfrxETH/type_3.png)

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


### Daily classical-liquidations

![](./results/stat/sfrxETH/liquidations_count_sfrxETH.png)

![](./results/stat/wstETH/liquidations_count_wstETH.png)

![](./results/stat/WBTC/liquidations_count_WBTC.png)

![](./results/stat/WETH/liquidations_count_WETH.png)

![](./results/stat/sfrxETH/liquidations_daily_debt_received_sfrxETH.png)

![](./results/stat/wstETH/liquidations_daily_debt_received_wstETH.png)

![](./results/stat/WBTC/liquidations_daily_debt_received_WBTC.png)

![](./results/stat/WETH/liquidations_daily_debt_received_WETH.png)



More data and picture results can be seen in [results folder](./results).
