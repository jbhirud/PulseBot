import pytest
import types

from pulsebot.exchanges.multi_exchange_manager import MultiExchangeManager


class DummyExchangeFactory:
    def __init__(self):
        self.last_config = None

    def __call__(self, config):
        self.last_config = config
        # Return a simple dummy object representing the exchange
        return types.SimpleNamespace(id='dummy', config=config)


def test_multi_exchange_manager_uses_apikeymanager(monkeypatch):
    mgr = MultiExchangeManager()

    # Prepare fake keys returned by APIKeyManager.get_keys (shape {'key','secret'})
    fake_keys = {'key': 'vault-key', 'secret': 'vault-secret'}
    monkeypatch.setattr(mgr.api_key_manager, 'get_keys', lambda name: fake_keys)

    binance_factory = DummyExchangeFactory()
    monkeypatch.setattr('ccxt.binance', binance_factory)

    mgr.add_exchange('binance', api_key=None, secret=None, testnet=True)

    # binance_factory.last_config should contain the apiKey/secret mapped from APIKeyManager
    cfg = binance_factory.last_config
    assert cfg is not None
    assert cfg.get('apiKey') == 'vault-key'
    assert cfg.get('secret') == 'vault-secret'
