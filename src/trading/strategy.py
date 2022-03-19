# Listing strategies

# 1 - End of Day strategy
# 2 - Swing strategy
# 3 - Day strategy
# 4 - Trend (rule based) strategy
# 5 - Scalping strategy
# 6 - Position (long term) strategy


class Strategy: pass
class RuleBasedStrategy: pass
class MultiRuleBasedStrategy: pass

#
# Interface
#
class Strategy:
    def __init__(self, market, connector, strategy_settings): pass
    def run(self): pass

    # Should those to be method or run function argument ?
    def backtest(self): pass
    def demo(self): pass

#
# Strategies
#
class RuleBasedStrategy(Strategy):
    # A rule based strategy computes key indicators and take aciton upon the value returned
    # Well known rules include :
    # - Moving Average Threshold (Above 50 days to enter and bellow 200 days to exit)
    # - Bollinger Bands
    # Full list here : https://www.ig.com/en/trading-strategies/10-trading-indicators-every-trader-should-know-190604
    def __init__(self):
        super().__init__()


class MultiRuleBasedStrategy(Strategy):
    def __init__(self):
        super().__init__()