import ccxt
import os


class BinanceManager:
    def __init__(self):
        self.exchange = None
        self.is_testnet = True
        self.fee_config = {
            'spot': 0.001,
            'future': 0.0004,
        }

    def initialize(self, config=None):
        # config may include api keys and testnet flag
        self.config = config or {}

    def connect_testnet(self, apiKey=None, secret=None):
        """Connect to Binance testnet (sandbox)"""
        params = {}
        params.update({'sandbox': True})
        # prefer explicit args, fall back to env vars
        apiKey = apiKey or self.config.get('apiKey') or os.environ.get('BINANCE_API_KEY')
        secret = secret or self.config.get('secret') or os.environ.get('BINANCE_SECRET')

        if apiKey and secret:
            params.update({'apiKey': apiKey, 'secret': secret})

        try:
            self.exchange = ccxt.binance(params)
        except Exception:
            self.exchange = None
        self.is_testnet = True
        return self.exchange

    def fetch_balance(self):
        if self.exchange:
            try:
                return self.exchange.fetch_balance()
            except Exception:
                return None
        return None

    def place_test_order(self, symbol, side, amount, price=None):
        order_type = 'limit' if price else 'market'
        if not self.exchange:
            raise RuntimeError('Exchange not connected')
        return self.exchange.create_order(symbol, order_type, side, amount, price)
