from analytics.detailed_trades import generate_token_flow
from collector.eigenphi.query import query_eigenphi_analytics_tx
from collector.eigenphi.utils import get_eigenphi_tokenflow
from utils import get_address_alias


# process_trades_data(save=True, save_dir="data/detailed_trades_data.csv")

target_tx = "0x6c1424586ea485da35ca689a10bc811633773b847c7fd3a5adb2c9ca32e7abeb"


resp = query_eigenphi_analytics_tx(target_tx)
token_balance_diff, address_tags, transfers = get_eigenphi_tokenflow(resp)

# for acc in token_balance_diff.get_accounts():
#     _alias = get_address_alias(acc)
#     if _alias == "":
#         for tag, addr in address_tags.items():
#             if addr.lower() == acc:
#                 _alias = tag

#     print("")
#     print(acc, "alias", _alias)
#     for symbol in token_balance_diff.get_account_symbols(addr=acc):
#         print(symbol, token_balance_diff.get_diff(acc, symbol=symbol))

generate_token_flow(transfers, address_tags, save=True, save_dir="data/detailed_trades_tokenflow_data.csv")