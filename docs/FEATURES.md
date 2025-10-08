# PulseBot Features (Phases 1-3)

This document summarizes implemented features across Phase 1 → Phase 3 (v0.1.0-alpha → v0.3.0-rc1).

Phase 1 — Core Foundation (v0.1.0-alpha)
- Project skeleton and package layout
- Core engine scaffold (`PulseBotCore`)
- Exchange adapter scaffold (`BinanceManager`) with testnet support
- Backtesting engine (`BacktestingEngine`) and enhanced wrapper
- Local authentication (`LocalAuth`) using SQLite (hardened with bcrypt)
- Basic documentation and scripts

Phase 2 — Trading Engine & Basic Strategies (v0.2.0-beta)
- Trading strategies: `MicroScalpingStrategy`, `GridTradingStrategy` (scaffold)
- BotManager and demo CLI to run backtests or testnet placeholders
- AI balance adaptation: `BalanceAdaptationAI`
- Enhanced backtesting and a Flask frontend scaffold
- CI pipeline (unit tests, build wheel, coverage)

Phase 3 — Multi-Exchange & Advanced AI (v0.3.0-rc1)
- Multi-exchange manager (`MultiExchangeManager`) with APIKeyManager placeholder
- Advanced AI modules: `AdvancedAdaptationAI`, `FeeAwareOptimizer`
- Pricing utility (`fetch_price_usd`) using ccxt with requests fallback
- Tests for multi-exchange aggregation, fee optimizer, pricing, and BotManager
- Release automation: draft releases and wheel uploads

Notes & Next Steps
- Replace `APIKeyManager` with secret manager integration (Vault/AWS Secrets)
- Improve USD valuation accuracy (use spot tickers and reliable price oracles)
- Add integration tests with VCR or recorded fixtures to avoid live calls in CI
- Add PyPI publishing credentials (protected via GitHub Secrets) to publish releases automatically
