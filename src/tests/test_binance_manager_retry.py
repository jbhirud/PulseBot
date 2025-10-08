import types
import pytest
from pulsebot.exchanges.binance_manager import BinanceManager


class FakeExchange:
    def __init__(self, fail_times=2):
        self._fail_times = fail_times
        self.calls = []

    def create_order(self, symbol, order_type, side, amount, price_or_params=None, params=None):
        # Support both signatures used in manager (price passed or not)
        # Record the call and then fail until counter exhausted
        self.calls.append((symbol, order_type, side, amount, price_or_params, params))
        if self._fail_times > 0:
            self._fail_times -= 1
            raise RuntimeError('transient')
        return {"id": "ok", "symbol": symbol}


def test_safe_create_order_retries_and_succeeds(monkeypatch):
    mgr = BinanceManager()
    fake = FakeExchange(fail_times=2)
    mgr.exchange = fake

    res = mgr._safe_create_order('BTC/USDT', 'market', 'buy', 0.01)
    assert res == {"id": "ok", "symbol": 'BTC/USDT'}
    # The create_order should have been called more than once (2 fails + 1 success)
    assert len(fake.calls) == 3


def test_idempotency_key_passed(monkeypatch):
    mgr = BinanceManager()
    fake = FakeExchange(fail_times=0)
    mgr.exchange = fake
    # Attach a simple metrics hook to capture events
    events = []
    def metrics_hook(**kwargs):
        events.append(kwargs)

    mgr.metrics_hook = metrics_hook

    res = mgr._safe_create_order('ETH/USDT', 'limit', 'sell', 0.1, price=1000, idempotency_key='abc-123')
    assert res == {"id": "ok", "symbol": 'ETH/USDT'}
    # Verify idempotency_key appears in headers of the recorded call
    last_call = fake.calls[-1]
    # params should include 'headers' mapping with our idempotency key
    assert last_call[5] is not None and last_call[5].get('headers', {}).get('Idempotency-Key') == 'abc-123'
    # Verify metrics events were emitted for success
    assert any(e.get('event') == 'order_success' for e in events)
