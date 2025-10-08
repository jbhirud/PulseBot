from flask import Flask, render_template, jsonify

from ..backtesting.enhanced_engine import EnhancedBacktestingEngine
from ..strategies.micro_scalping import MicroScalpingStrategy
from ..exchanges.binance_manager import BinanceManager

app = Flask(__name__)


@app.route('/')
def dashboard():
    return "PulseBot dashboard placeholder"


@app.route('/api/backtest/results')
def get_backtest_results():
    engine = EnhancedBacktestingEngine()
    strategy = MicroScalpingStrategy({'profit_target': 0.005})
    results = engine.run_comprehensive_backtest(strategy, 'BTC/USDT', 100)
    return jsonify(results)


@app.route('/api/balance')
def get_balance():
    exchange = BinanceManager()
    balance = exchange.fetch_balance()
    return jsonify(balance)


if __name__ == '__main__':
    app.run(debug=True)
