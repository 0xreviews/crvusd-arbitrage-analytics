from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from config.address import ALIAS_TO_ADDRESS
from config.constance import (
    SUBGRAPH_ENDPOINT_0XREVIEWS,
    SUBGRAPH_ENDPOINT_VOLUME,
    SUBGRAPH_QUERY_SIZE,
)
from .gql_queries import (
    detialed_trades_query,
    token_exchanges_query,
    liquidations_query,
)

tp = RequestsHTTPTransport(url=SUBGRAPH_ENDPOINT_VOLUME)

# Create a GraphQL client using the defined transport
client = Client(transport=tp, fetch_schema_from_transport=True)


def query_gql(q, variables={}):
    """
    function to query subgraph.

    Parameters
    ----------
    q : str
        A GraphQL query.
    variables: dict
        query vaiables

    Returns
    -------
    str
        The returned results.

    """
    r = client.execute(q, variable_values=variables)
    return r


def data_iteration(
    key_name, query_func, llamma_collateral="sfrxETH", size=SUBGRAPH_QUERY_SIZE
):
    count = 0
    data = []
    while True:
        res = query_func(llamma_collateral, count * size, size)
        if key_name in res:
            _data = res[key_name]
            if len(_data) == 0:
                print(
                    "query %s done, total res len %d" % (key_name, len(data))
                )
                break
            data = data + _data
            print(
                "query %s, from %d to %d res len: %d"
                % (key_name, count * size, (count + 1) * size, len(_data))
            )
        else:
            break

        count += 1

    return data


def query_detailed_trades(skip=0, size=SUBGRAPH_QUERY_SIZE):
    return query_gql(
        detialed_trades_query,
        variables={"skip": int(skip), "size": int(size)},
    )


def query_token_exchanges(llamma_collateral, skip=0, size=SUBGRAPH_QUERY_SIZE):
    # llamma_name: LLAMMA-sfrxETH-crvUSD / LLAMMA-wstETH-crvUSD / LLAMMA-WETH-crvUSD / LLAMMA-WBTC-crvUSD
    llamma_address = ALIAS_TO_ADDRESS["LLAMMA-%s-crvUSD" % (llamma_collateral)]
    return query_gql(
        token_exchanges_query,
        variables={"llamma": llamma_address, "skip": int(skip), "size": int(size)},
    )


def query_detailed_trades_all(llamma_collateral="sfrxETH"):
    res = data_iteration(
        "tokenExchanges",
        query_token_exchanges,
        size=SUBGRAPH_QUERY_SIZE,
        llamma_collateral=llamma_collateral,
    )
    return res


def query_liquidations(llamma_collateral, skip=0, size=SUBGRAPH_QUERY_SIZE):
    # llamma_name: Controller-sfrxETH / Controller-wstETH / Controller-WETH / Controller-WBTC
    llamma_address = ALIAS_TO_ADDRESS["Controller-%s" % (llamma_collateral)]
    return query_gql(
        liquidations_query,
        variables={"llamma": llamma_address, "skip": int(skip), "size": int(size)},
    )


def query_liquidations_all(llamma_collateral="sfrxETH"):
    res = data_iteration(
        "liquidations",
        query_liquidations,
        size=SUBGRAPH_QUERY_SIZE,
        llamma_collateral=llamma_collateral,
    )
    return res
