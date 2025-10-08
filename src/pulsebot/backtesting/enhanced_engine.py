from .engine import BacktestingEngine


class EnhancedBacktestingEngine:
    def __init__(self):
        self.engine = BacktestingEngine()

    def calculate_win_rate(self, trades):
        if not trades:
            return 0.0
        wins = sum(1 for t in trades if t.get('profit', 0) > 0)
        return wins / len(trades)

    def calculate_performance_metrics(self, results):
        # placeholder implementation
        return {}

    def generate_charts(self, results):
        return {}

    def analyze_periods(self, results):
        periods = ['7d', '1m', '3m', '1y']
        analysis = {}

        for period in periods:
            period_data = results['period_breakdown'].get(period, {'total_profit': 0, 'total_trades': 0, 'trades': []})
            analysis[period] = {
                'total_return': period_data.get('total_profit', 0),
                'return_percentage': (period_data.get('total_profit', 0) / 100) * 100,
                'trades_count': period_data.get('total_trades', 0),
                'win_rate': self.calculate_win_rate(period_data.get('trades', []))
            }

        return analysis

    def run_comprehensive_backtest(self, strategy, symbol, initial_balance):
        full_results = self.engine.run_backtest(strategy, symbol, initial_balance)
        period_analysis = self.analyze_periods(full_results)
        performance_metrics = self.calculate_performance_metrics(full_results)

        return {
            **full_results,
            'period_analysis': period_analysis,
            'performance_metrics': performance_metrics,
            'charts': self.generate_charts(full_results)
        }
