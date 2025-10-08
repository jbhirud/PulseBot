import ccxt
import requests


def fetch_price_usd(symbol, exchange=None, fallback_api=None):
    """Fetch latest price for symbol in USD using ccxt fetch_ticker, with optional fallback API.

    symbol: 'BTC/USDT' or 'BTC/USD' etc.
    exchange: ccxt exchange instance (optional)
    fallback_api: URL template expecting {symbol} (optional)
    """
    # Try ccxt first
    try:
        ex = exchange or ccxt.binance()
        ticker = ex.fetch_ticker(symbol)
        # ccxt ticker may have 'last' price
        price = ticker.get('last') or ticker.get('close') or ticker.get('price')
        if price:
            return float(price)
    except Exception:
        pass

    # Fallback to requests if provided
    try:
        if fallback_api:
            url = fallback_api.format(symbol=symbol.replace('/', ''))
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            # expect data to contain 'price' or similar
            if isinstance(data, dict):
                for key in ('price', 'last', 'ticker'):
                    if key in data:
                        return float(data[key])
            # if list-like, try first element
            if isinstance(data, list) and len(data) > 0:
                try:
                    return float(data[0].get('price'))
                except Exception:
                    pass
    except Exception:
        pass

    raise RuntimeError('Unable to fetch price')
