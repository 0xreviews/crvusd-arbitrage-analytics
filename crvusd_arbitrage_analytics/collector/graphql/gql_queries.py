from gql import Client, gql

# https://github.com/0xreviews/curve-stablecoin-subgraph
detialed_trades_query = gql(
    """
    query DetailedTradesQuery ($skip: Int!, $size: Int!) {
        detailedTrades(skip: $skip, first: $size, orderBy: timestamp, orderDirection: asc) {
            id
            buyer
            sold_id
            tokens_sold
            tokens_bought
            avg_price
            oracle_price
            market_price
            profit_rate
            n1
            n2
            ticks_in
            ticks_out
            tx
            timestamp
        }
    }
"""
)

# https://github.com/curvefi/volume-subgraphs/tree/main/subgraphs/crvusd
token_exchanges_query = gql(
    """
    query TokenExchangesQuery ($llamma: String!, $skip: Int!, $size: Int!) {
        tokenExchanges(skip: $skip, first: $size, orderBy: blockTimestamp, orderDirection: asc, where: { 
            llamma: $llamma,
        }) {
            id
            transactionHash
            blockTimestamp
            blockNumber
            soldId
            tokensSold
            boughtId
            tokensBought
            buyer {
                id
            }
        }
    }
"""
)

liquidations_query = gql(
    """
    query Liquidations ($llamma: String!, $skip: Int!, $size: Int!) {
        liquidations(skip: $skip, first: $size, orderBy: blockTimestamp, orderDirection: asc, where: { 
            market: $llamma,
        }) {
            id
            blockNumber
            blockTimestamp
            transactionHash
            debt
            collateralReceived
            stablecoinReceived
            user {
                id
            }
            liquidator {
                id
            }
            # market {
            #     id
            # }
        }
    }
"""
)