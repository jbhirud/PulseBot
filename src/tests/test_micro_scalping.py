import pandas as pd

from pulsebot.strategies.micro_scalping import MicroScalpingStrategy


def make_sample_data():
    timestamps = pd.date_range('2025-01-01', periods=5, freq='T')
    prices = [100, 100.2, 100.1, 100.5, 100.3]
    df = pd.DataFrame({'timestamp': timestamps, 'close': prices})
    return df


def test_micro_scalping_trades():
    data = make_sample_data()
    strat = MicroScalpingStrategy({'profit_target': 0.001})
    result = strat.execute(data, 100)
    assert 'final_balance' in result
    assert 'trades' in result
