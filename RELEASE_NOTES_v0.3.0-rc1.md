# Release v0.3.0-rc1 (Release Candidate)

This release focuses on multi-exchange support and advanced AI adaptation features.

### Highlights

- Multi-exchange manager (`MultiExchangeManager`) with API key manager placeholder.
- Advanced AI modules:
  - `AdvancedAdaptationAI` for dynamic strategy allocation based on balances and volatility.
  - `FeeAwareOptimizer` for fee-aware trade sizing.
- Asset pricing utility using `ccxt.fetch_ticker` with a `requests` fallback.
- Unit tests added for multi-exchange aggregation, fee optimizer, pricing, and BotManager order placement (mocked).
- CI: coverage enforcement, wheel build, and release workflows.

### Notes

- `APIKeyManager` is a placeholder; integrate with a secrets manager for production.
- `calculate_total_usd` is a simplified placeholder; for accurate USD valuation, integrate a price oracle or robust price mapping.

