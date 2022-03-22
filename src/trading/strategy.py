from dataclasses import dataclass

from broker import Broker
from rule import *

##
#   Listing strategies for bots.
#   1 - End of Day strategy
#   2 - Swing strategy
#   3 - Day strategy
#   4 - Trend (rule based) strategy
#   5 - Scalping strategy
#   6 - Position (long term) strategy
##

@dataclass
class RuleBasedStrategy:
    """Trading bot that connects to a crypto broker and performs trades."""

    broker: Broker
    buy_strategy: TradingStrategyRule
    sell_strategy: TradingStrategyRule

    def run(self, symbol: str) -> None:
        prices = self.broker.get_market_data(symbol)
        if self.buy_strategy(prices):
            self.broker.buy(symbol, 10)
        elif self.sell_strategy(prices):
            self.broker.sell(symbol, 10)
        else:
            print(f"No action needed for {symbol}.")