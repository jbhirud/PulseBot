from types import SimpleNamespace

from pulsebot.ai.fee_optimizer import FeeAwareOptimizer


def test_fee_optimizer_min_profit():
    opt = FeeAwareOptimizer()
    class Strat:
        trade_type = 'spot'
        target_profit = 0.001
        min_trade_size = 1
        max_position_size = 0.1

    strategy = Strat()
    sized = opt.optimize_trade_size('binance', strategy, 100)
    assert sized > 0
