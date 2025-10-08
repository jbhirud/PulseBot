from unittest.mock import MagicMock

from pulsebot.exchanges.multi_exchange_manager import MultiExchangeManager


def test_calculate_total_usd_with_tickers():
    mgr = MultiExchangeManager()

    # Mock exchange with balance and ticker
    fake_exchange = MagicMock()
    fake_exchange.fetch_balance.return_value = {'BTC': {'total': 1}, 'USDT': {'total': 100}}
    fake_exchange.fetch_ticker.side_effect = lambda symbol: {'last': 30000} if symbol == 'BTC/USD' or symbol == 'BTC/USDT' else {'last': 1}

    mgr.exchanges = {'binance': fake_exchange}
    agg = mgr.get_aggregated_balance()
    assert agg['total_balance'] > 0
