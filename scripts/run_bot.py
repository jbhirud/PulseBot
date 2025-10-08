#!/usr/bin/env python3
"""Demo CLI to run a strategy in backtest or testnet mode."""
import argparse
import os

from src.pulsebot.strategies.micro_scalping import MicroScalpingStrategy
from src.pulsebot.core.bot_manager import BotManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['backtest', 'testnet'], default='backtest')
    parser.add_argument('--symbol', default='BTC/USDT')
    parser.add_argument('--balance', type=float, default=100)
    args = parser.parse_args()

    manager = BotManager()
    strategy = MicroScalpingStrategy({'profit_target': 0.005})

    if args.mode == 'backtest':
        result = manager.run_backtest(strategy, args.symbol, args.balance)
        print('Backtest result:')
        print(result)
    else:
        # testnet mode would connect to an exchange; placeholder
        print('Testnet mode is a placeholder; connect exchange keys in config to enable live runs.')


if __name__ == '__main__':
    main()
