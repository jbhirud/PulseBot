from ..backtesting.enhanced_engine import EnhancedBacktestingEngine
from ..exchanges.binance_manager import BinanceManager
import os


class BotManager:
    def __init__(self):
        self.backends = {}

    def run_backtest(self, strategy, symbol, initial_balance=100):
        engine = EnhancedBacktestingEngine()
        return engine.run_comprehensive_backtest(strategy, symbol, initial_balance)

    def run_testnet(self, strategy, symbol, balance=100):
        """Connect to Binance testnet using env vars BINANCE_API_KEY and BINANCE_SECRET and place a sample order."""
        api_key = os.environ.get('BINANCE_API_KEY')
        api_secret = os.environ.get('BINANCE_SECRET')
        manager = BinanceManager()
        manager.connect_testnet(apiKey=api_key, secret=api_secret)

        # simple example: place a very small market order (this is a demo; in practice add checks)
        try:
            order = manager.place_test_order(symbol, 'buy', 0.0001)
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

        return {'status': 'ok', 'order': order}
