import os
from unittest.mock import patch, MagicMock

from pulsebot.core.bot_manager import BotManager


def test_run_testnet_places_order(monkeypatch):
    # Mock BinanceManager methods to avoid real network calls
    mock_order = {'id': 'testorder', 'status': 'open'}

    class FakeExchange:
        def create_order(self, symbol, order_type, side, amount, price=None):
            return mock_order

    class FakeManager:
        def __init__(self):
            self.exchange = FakeExchange()

        def connect_testnet(self, apiKey=None, secret=None):
            self.exchange = FakeExchange()
            return self.exchange

        def place_test_order(self, symbol, side, amount, price=None):
            return mock_order

    with patch('pulsebot.core.bot_manager.BinanceManager', return_value=FakeManager()):
        manager = BotManager()
        result = manager.run_testnet(None, 'BTC/USDT', balance=100)
        assert result['status'] == 'ok'
        assert result['order'] == mock_order
