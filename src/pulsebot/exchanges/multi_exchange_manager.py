import ccxt
import os


class APIKeyManager:
    def __init__(self):
        # Placeholder for secure key storage integration
        self.keys = {}

    def set_key(self, exchange_name, api_key, secret):
        self.keys[exchange_name] = {'apiKey': api_key, 'secret': secret}

    def get_key(self, exchange_name):
        return self.keys.get(exchange_name) or {
            'apiKey': os.environ.get(f'{exchange_name.upper()}_API_KEY'),
            'secret': os.environ.get(f'{exchange_name.upper()}_SECRET')
        }


class MultiExchangeManager:
    def __init__(self):
        self.exchanges = {}
        self.api_key_manager = APIKeyManager()

    def add_exchange(self, exchange_name, api_key=None, secret=None, testnet=False):
        exchange_config = {'sandbox': testnet}
        key = api_key or secret and {'apiKey': api_key, 'secret': secret} or self.api_key_manager.get_key(exchange_name)

        if key and key.get('apiKey') and key.get('secret'):
            exchange_config.update({'apiKey': key.get('apiKey'), 'secret': key.get('secret')})

        if exchange_name == 'binance':
            self.exchanges[exchange_name] = ccxt.binance(exchange_config)
        elif exchange_name == 'pionex':
            self.exchanges[exchange_name] = ccxt.pionex(exchange_config)
        elif exchange_name == 'delta':
            self.exchanges[exchange_name] = ccxt.delta(exchange_config)

    def calculate_total_usd(self, balance):
        # Convert asset balances to USD using tickers where possible
        total = 0.0
        # balance typically contains keys like 'free', 'used', 'total' or asset symbols
        for asset, info in balance.items():
            try:
                # if asset looks like a fiat USD entry
                if asset in ('USD', 'USDT', 'USDC'):
                    total += float(info.get('total', 0))
                else:
                    # try to fetch ticker for asset/USD or asset/USDT
                    symbol_usd = f"{asset}/USD"
                    symbol_usdt = f"{asset}/USDT"
                    price = None
                    try:
                        ticker = self._last_ticker_cache.get(symbol_usd)
                        if ticker is None:
                            ticker = self._fetch_ticker_from_exchanges(symbol_usd)
                        price = ticker
                    except Exception:
                        pass

                    if price is None:
                        try:
                            ticker = self._last_ticker_cache.get(symbol_usdt)
                            if ticker is None:
                                ticker = self._fetch_ticker_from_exchanges(symbol_usdt)
                            price = ticker
                        except Exception:
                            pass

                    asset_total = float(info.get('total', 0))
                    if price is not None:
                        total += asset_total * float(price)
            except Exception:
                continue

        return total

    def _fetch_ticker_from_exchanges(self, symbol):
        # Try each exchange to fetch a ticker for symbol and cache it
        if not hasattr(self, '_last_ticker_cache'):
            self._last_ticker_cache = {}

        for ex in self.exchanges.values():
            try:
                t = ex.fetch_ticker(symbol)
                price = t.get('last') or t.get('close')
                if price:
                    self._last_ticker_cache[symbol] = price
                    return price
            except Exception:
                continue

        return None

    def get_aggregated_balance(self):
        total_balance = 0
        balances = {}

        for name, exchange in self.exchanges.items():
            try:
                balance = exchange.fetch_balance()
                total_usd = self.calculate_total_usd(balance)
                total_balance += total_usd
                balances[name] = {'balance': balance, 'total_usd': total_usd}
            except Exception as e:
                balances[name] = {'error': str(e)}

        return {'total_balance': total_balance, 'exchange_balances': balances}
