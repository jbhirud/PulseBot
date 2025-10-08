import responses
from unittest.mock import MagicMock

from pulsebot.utils.pricing import fetch_price_usd


def test_fetch_price_ccxt_mock(monkeypatch):
    fake_ex = MagicMock()
    fake_ex.fetch_ticker.return_value = {'last': 123.45}
    price = fetch_price_usd('BTC/USDT', exchange=fake_ex)
    assert price == 123.45


@responses.activate
def test_fetch_price_fallback_api():
    api = 'https://api.test/price/{symbol}'
    responses.add(responses.GET, 'https://api.test/price/BTCUSDT', json={'price': 200.0}, status=200)
    price = fetch_price_usd('BTC/USDT', fallback_api=api)
    assert price == 200.0
