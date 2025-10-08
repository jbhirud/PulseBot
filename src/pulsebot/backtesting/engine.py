import ccxt
import pandas as pd


class BacktestingEngine:
    def __init__(self):
        # using ccxt exchange instance for data fetching
        try:
            self.exchange = ccxt.binance()
        except Exception:
            self.exchange = None
        self.historical_data = {}

    def fetch_historical_data(self, symbol, timeframe='1d', days=365):
        """Fetch historical OHLCV data."""
        if not self.exchange:
            raise RuntimeError('Exchange instance not available')

        since = self.exchange.parse8601(
            (pd.Timestamp.now() - pd.Timedelta(days=days)).isoformat()
        )
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def calculate_equity_curve(self, results):
        # placeholder
        return []

    def run_backtest(self, strategy, symbol, initial_balance=100):
        data = self.fetch_historical_data(symbol)
        results = strategy.execute(data, initial_balance)

        periods = {
            '1y': data,
            '3m': data.tail(90),
            '1m': data.tail(30),
            '7d': data.tail(7)
        }

        period_results = {}
        for period_name, period_data in periods.items():
            period_results[period_name] = strategy.execute(period_data, initial_balance)

        return {
            'full_results': results,
            'period_breakdown': period_results,
            'equity_curve': self.calculate_equity_curve(results)
        }
