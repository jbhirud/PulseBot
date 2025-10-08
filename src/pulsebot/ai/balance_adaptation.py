class BalanceAdaptationAI:
    def __init__(self):
        self.balance_history = []
        self.current_allocation = {}

    def analyze_balance_change(self, new_balance, previous_balance):
        if previous_balance == 0:
            return self.current_allocation

        change_percent = (new_balance - previous_balance) / previous_balance

        if abs(change_percent) > 0.1:
            return self.reallocate_strategies(new_balance)
        return self.current_allocation

    def reallocate_strategies(self, balance):
        if balance < 50:
            allocation = {
                'micro_scalping': 0.6,
                'micro_grid': 0.3,
                'spot_dca': 0.1
            }
        elif balance < 500:
            allocation = {
                'spot_grid': 0.4,
                'micro_scalping': 0.3,
                'futures_scalping': 0.2,
                'spot_dca': 0.1
            }
        else:
            allocation = {
                'spot_grid': 0.3,
                'futures_grid': 0.25,
                'futures_hedge': 0.2,
                'breakout': 0.15,
                'arbitrage': 0.1
            }

        self.current_allocation = allocation
        return allocation
