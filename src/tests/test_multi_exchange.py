from unittest.mock import MagicMock

from pulsebot.exchanges.multi_exchange_manager import MultiExchangeManager


def test_aggregated_balance_multiple_exchanges():
    mgr = MultiExchangeManager()

    # Mock exchanges
    e1 = MagicMock()
    e1.fetch_balance.return_value = {'BTC': {'total': 1}, 'USD': {'total': 100}}

    e2 = MagicMock()
    e2.fetch_balance.return_value = {'ETH': {'total': 2}, 'USD': {'total': 50}}

    mgr.exchanges = {'binance': e1, 'pionex': e2}
    agg = mgr.get_aggregated_balance()
    assert 'total_balance' in agg
    assert 'exchange_balances' in agg
