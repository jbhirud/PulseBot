from ..backtesting.enhanced_engine import EnhancedBacktestingEngine


class BotManager:
    def __init__(self):
        self.backends = {}

    def run_backtest(self, strategy, symbol, initial_balance=100):
        engine = EnhancedBacktestingEngine()
        return engine.run_comprehensive_backtest(strategy, symbol, initial_balance)

    def run_testnet(self, strategy, exchange, symbol, balance=100):
        # Placeholder: orchestrate live/testnet runs
        # For now, just return a message
        return {'status': 'connected', 'symbol': symbol}
