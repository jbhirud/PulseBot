class MicroScalpingStrategy:
    def __init__(self, config):
        self.profit_target = config.get('profit_target', 0.005)
        self.stop_loss = config.get('stop_loss', 0.008)
        self.max_trade_size = config.get('max_trade_size', 0.1)

    def execute(self, data, balance):
        trades = []
        current_balance = balance

        for i in range(1, len(data)):
            current_price = data['close'].iloc[i]
            prev_price = data['close'].iloc[i-1]
            price_change = (current_price - prev_price) / prev_price

            if abs(price_change) > 0.001:
                side = 'buy' if price_change > 0 else 'sell'
                trade_size = min(current_balance * self.max_trade_size, balance * 0.1)

                if trade_size > 0:
                    entry_price = current_price
                    exit_price = entry_price * (1 + self.profit_target) if side == 'buy' else entry_price * (1 - self.profit_target)
                    profit = trade_size * self.profit_target
                    current_balance += profit

                    trades.append({
                        'timestamp': data['timestamp'].iloc[i],
                        'side': side,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'size': trade_size,
                        'profit': profit
                    })

        return {
            'final_balance': current_balance,
            'total_profit': current_balance - balance,
            'trades': trades,
            'total_trades': len(trades)
        }
