import pytest

from pulsebot.risk.advanced_risk import AdvancedRiskManager


def test_get_max_drawdown_limit():
    rm = AdvancedRiskManager()
    assert rm.get_max_drawdown_limit(10) == 0.03
    assert rm.get_max_drawdown_limit(100) == 0.05
    assert rm.get_max_drawdown_limit(1000) == 0.08
    assert rm.get_max_drawdown_limit(10000) == 0.10


def test_trigger_circuit_breaker():
    rm = AdvancedRiskManager()
    rm.circuit_breakers['acct1'] = {'balance': 100}
    rm.check_circuit_breaker('acct1', 0.1)  # 10% drawdown; should trip for small accounts
    assert rm.circuit_breakers['acct1'].get('tripped', False) is True
