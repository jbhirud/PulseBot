class FeeAwareOptimizer:
    def __init__(self):
        self.exchange_fees = {
            'binance': {'spot': 0.001, 'future': 0.0004},
            'pionex': {'spot': 0.0005, 'grid': 0.0005},
            'delta': {'spot': 0.001, 'future': 0.0005}
        }

    def calculate_minimum_profit(self, exchange, trade_type, trade_size):
        fee_rate = self.exchange_fees.get(exchange, {}).get(trade_type, 0)
        total_fee = trade_size * fee_rate * 2
        if trade_size == 0:
            return 0
        min_profit_percent = (total_fee / trade_size) * 3
        return min(min_profit_percent, 0.01)

    def optimize_trade_size(self, exchange, strategy, available_balance):
        min_profit = self.calculate_minimum_profit(exchange, strategy.trade_type, available_balance)
        if min_profit > getattr(strategy, 'target_profit', 0):
            return min(available_balance * 0.5, getattr(strategy, 'min_trade_size', available_balance * 0.01))
        else:
            return available_balance * getattr(strategy, 'max_position_size', 0.1)
