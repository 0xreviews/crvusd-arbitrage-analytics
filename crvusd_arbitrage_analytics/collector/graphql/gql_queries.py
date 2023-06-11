from gql import Client, gql

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
