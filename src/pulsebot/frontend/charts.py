class TradingVisualization:
    def create_live_trading_chart(self, trades, current_prices):
        """Create real-time trading visualization.

        trades: list of trade dicts
        current_prices: dict symbol->price
        Returns a simple dict representing the chart payload (scaffold).
        """
        # Scaffold: return a payload suitable for a frontend renderer
        chart = {
            'series': [],
            'markers': [],
            'prices': current_prices,
        }
        for t in trades:
            chart['markers'].append({
                'symbol': t.get('symbol'),
                'price': t.get('price'),
                'side': t.get('side'),
                'time': t.get('time'),
            })

        return chart

    def create_performance_dashboard(self, backtest_results):
        """Create comprehensive performance dashboard (scaffold).

        backtest_results: dict with period breakdowns and metrics
        """
        dashboard = {
            'periods': backtest_results.get('periods', []),
            'metrics': backtest_results.get('metrics', {}),
        }
        return dashboard

    def create_balance_evolution_chart(self, balance_history):
        """Show balance evolution across accounts.

        balance_history: list of {time, total_balance}
        """
        return {'balance_history': balance_history}
