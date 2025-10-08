class AdvancedAdaptationAI:
    def __init__(self):
        self.performance_history = []
        self.market_conditions = {}

    def dynamic_strategy_adjustment(self, account_balances, market_volatility):
        total_balance = sum(balances['total_usd'] for balances in account_balances.values())
        volatility_factor = self.calculate_volatility_factor(market_volatility)
        base_allocation = self.get_base_allocation(total_balance)
        adjusted_allocation = self.apply_market_adjustments(base_allocation, volatility_factor)
        return adjusted_allocation

    def calculate_volatility_factor(self, market_volatility):
        # Simple normalization placeholder
        return min(max(market_volatility, 0.0), 2.0)

    def apply_market_adjustments(self, base_allocation, volatility_factor):
        # Decrease aggressive allocations in high volatility
        adjusted = {}
        for k, v in base_allocation.items():
            adjusted[k] = max(0.0, v * (1.0 - 0.5 * (volatility_factor - 1)))
        # Normalize
        total = sum(adjusted.values()) or 1.0
        for k in adjusted:
            adjusted[k] = adjusted[k] / total
        return adjusted

    def get_base_allocation(self, total_balance):
        if total_balance < 20:
            return {'micro_scalping': 0.7, 'micro_grid': 0.3}
        elif total_balance < 100:
            micro_weight = max(0.7 - (total_balance - 20) / 80 * 0.4, 0.3)
            grid_weight = 1 - micro_weight
            return {'micro_scalping': micro_weight, 'spot_grid': grid_weight}
        elif total_balance < 500:
            # Smooth transition example
            return {'micro_scalping': 0.4, 'spot_grid': 0.4, 'breakout': 0.2}
        else:
            return {'spot_grid': 0.3, 'futures_grid': 0.25, 'futures_hedge': 0.2, 'breakout': 0.15, 'arbitrage': 0.1}
