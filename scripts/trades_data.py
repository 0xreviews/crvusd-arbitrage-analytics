from collector.eigenphi.query import query_eigenphi_analytics_tx
from collector.eigenphi.utils import get_eigenphi_tokenflow
from utils import get_address_alias


# process_trades_data(save=True, save_dir="data/detailed_trades_data.csv")

target_tx = "0x6c1424586ea485da35ca689a10bc811633773b847c7fd3a5adb2c9ca32e7abeb"


resp = query_eigenphi_analytics_tx(target_tx)
tokenflow = get_eigenphi_tokenflow(resp)

for acc in tokenflow.get_accounts():
    print("")
    print(acc, 'alias', get_address_alias(acc))
    for symbol in tokenflow.get_account_symbols(addr=acc):
        print(symbol, tokenflow.get_diff(acc, symbol=symbol))