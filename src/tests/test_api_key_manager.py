import os
import types
import pytest

from pulsebot.exchanges.api_key_manager import APIKeyManager


class FakeKVV2:
    def __init__(self, data):
        self._data = data

    def read_secret_version(self, path):
        return {"data": {"data": self._data}}


class FakeSecrets:
    def __init__(self, data):
        self.kv = types.SimpleNamespace(v2=FakeKVV2(data), read_secret=lambda path: {"data": data})


class FakeClient:
    def __init__(self, data):
        self.secrets = FakeSecrets(data)


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    # Clear variables used by APIKeyManager to avoid leaking from environment
    for k in list(os.environ.keys()):
        if k.endswith("_API_KEY") or k.endswith("_API_SECRET") or k in ("VAULT_ADDR", "VAULT_TOKEN"):
            monkeypatch.delenv(k, raising=False)
    yield


def test_env_fallback(monkeypatch):
    monkeypatch.setenv('BINANCE_API_KEY', 'envkey')
    monkeypatch.setenv('BINANCE_API_SECRET', 'envsecret')
    mgr = APIKeyManager()
    keys = mgr.get_keys('binance')
    assert keys == {"key": "envkey", "secret": "envsecret"}


def test_vault_reads_kv_v2(monkeypatch):
    # Simulate hvac client existing
    fake_data = {"api_key": "vaultkey", "api_secret": "vaultsecret"}
    fake_client = FakeClient(fake_data)

    # Patch hvac module client creation used inside APIKeyManager
    class DummyHVACModule:
        Client = lambda *args, **kwargs: fake_client

    monkeypatch.setitem(__import__('sys').modules, 'hvac', DummyHVACModule())

    # Initialize with a vault addr so it attempts to create a client
    mgr = APIKeyManager(vault_addr='http://localhost:8200')
    # Override internal client with our fake
    mgr._client = fake_client

    keys = mgr.get_keys('binance')
    assert keys == {"key": "vaultkey", "secret": "vaultsecret"}


def test_vault_fallback_to_env_when_vault_missing(monkeypatch):
    # Ensure hvac is missing
    monkeypatch.setitem(__import__('sys').modules, 'hvac', None)
    # Use environment fallback
    monkeypatch.setenv('BINANCE_API_KEY', 'envkey2')
    monkeypatch.setenv('BINANCE_API_SECRET', 'envsecret2')
    mgr = APIKeyManager(vault_addr='http://localhost:8200')
    keys = mgr.get_keys('binance')
    assert keys == {"key": "envkey2", "secret": "envsecret2"}
