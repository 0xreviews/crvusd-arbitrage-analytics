

from collections import defaultdict

# diffs:
#   address:
#       token symbol: total diff amount
class TokenBalanceDiff():

    def __init__(self):
        self.diffs = defaultdict(dict)
    
    def get_accounts(self):
        return self.diffs.keys()
    
    def get_account_symbols(self, addr):
        return self.diffs[addr].keys()

    def get_diff(self, addr, symbol):
        if symbol not in self.diffs[addr]:
            return 0
        return self.diffs[addr][symbol]

    def update_diff(self, addr, symbol, diff):
        if addr is None or addr == "":
            raise TypeError("TokenBalanceDiff account should not empty.")
        if symbol not in self.diffs[addr]:
            self.diffs[addr][symbol] = 0
        self.diffs[addr][symbol] += diff

