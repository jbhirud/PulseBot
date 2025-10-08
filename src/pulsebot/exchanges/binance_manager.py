import ccxt


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
        # ccxt uses 'test' or 'sandbox' depending on exchange; use sandbox for compatibility
        params.update({'sandbox': True})
        if apiKey and secret:
            params.update({'apiKey': apiKey, 'secret': secret})

        self.exchange = ccxt.binance(params)
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
