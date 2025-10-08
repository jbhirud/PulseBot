import ccxt
import os
import time
import random
from typing import Optional
import logging


class BinanceManager:
    def __init__(self):
        self.exchange = None
        self.is_testnet = True
        self.fee_config = {
            'spot': 0.001,
            'future': 0.0004,
        }

    def initialize(self, config=None):
        # config may include api keys and testnet flag
        self.config = config or {}

    def connect_testnet(self, apiKey=None, secret=None):
        """Connect to Binance testnet (sandbox)"""
        params = {}
        params.update({'sandbox': True})
        # prefer explicit args, fall back to env vars
        apiKey = apiKey or self.config.get('apiKey') or os.environ.get('BINANCE_API_KEY')
        secret = secret or self.config.get('secret') or os.environ.get('BINANCE_SECRET')

        if apiKey and secret:
            params.update({'apiKey': apiKey, 'secret': secret})

        try:
            self.exchange = ccxt.binance(params)
        except Exception:
            self.exchange = None
        self.is_testnet = True
        return self.exchange

    def fetch_balance(self):
        if self.exchange:
            try:
                return self.exchange.fetch_balance()
            except Exception:
                return None
        return None

    def place_test_order(self, symbol, side, amount, price=None):
        order_type = 'limit' if price else 'market'
        if not self.exchange:
            raise RuntimeError('Exchange not connected')
        return self._safe_create_order(symbol, order_type, side, amount, price)

    def _safe_create_order(self, symbol: str, order_type: str, side: str, amount: float, price: Optional[float] = None, *,
                           max_retries: int = 3, base_backoff: float = 0.5, idempotency_key: Optional[str] = None):
        """Create an order with retries, exponential backoff, and optional idempotency.

        - Retries transient exceptions up to max_retries.
        - Adds a simple jitter to backoff to avoid thundering herd.
        - If idempotency_key is provided and the exchange driver supports passing headers, it will attach it.
        """
        attempt = 0
        logger = logging.getLogger(__name__)
        # metrics hook (callable) - can be monkeypatched in tests or replaced by a real hook
        metrics_hook = getattr(self, 'metrics_hook', None)
        while True:
            attempt += 1
            try:
                params = {}
                # Map idempotency into headers if requested; many exchange SDKs accept a 'headers' dict in params
                if idempotency_key:
                    params['headers'] = {'Idempotency-Key': idempotency_key}

                if price is not None:
                    res = self.exchange.create_order(symbol, order_type, side, amount, price, params)
                else:
                    res = self.exchange.create_order(symbol, order_type, side, amount, params)

                # Report success to metrics hook
                if callable(metrics_hook):
                    try:
                        metrics_hook(event='order_success', exchange=getattr(self.exchange, 'id', None) or 'unknown')
                    except Exception:
                        logger.debug('metrics_hook failed', exc_info=True)

                return res
            except Exception as e:
                # Consider all exceptions transient for now; in production inspect type/messages
                logger.warning('order attempt %d failed: %s', attempt, str(e))
                if callable(metrics_hook):
                    try:
                        metrics_hook(event='order_retry', exchange=getattr(self.exchange, 'id', None) or 'unknown', attempt=attempt)
                    except Exception:
                        logger.debug('metrics_hook failed', exc_info=True)

                if attempt > max_retries:
                    logger.error('order failed after %d attempts', attempt)
                    if callable(metrics_hook):
                        try:
                            metrics_hook(event='order_failed', exchange=getattr(self.exchange, 'id', None) or 'unknown', attempt=attempt)
                        except Exception:
                            logger.debug('metrics_hook failed', exc_info=True)
                    raise
                backoff = base_backoff * (2 ** (attempt - 1))
                # jitter +/- 20%
                jitter = backoff * 0.2 * (random.random() * 2 - 1)
                sleep_time = max(0.0, backoff + jitter)
                time.sleep(sleep_time)
