# Development Guide

This document outlines the recommended git branching model, tagging strategy, and release phases for PulseBot.

Branching model

- `main`: production-ready releases only.
- `develop`: integration branch for completed features and QA.
- Feature branches: `feature/<name>` off `develop`.
- Hotfix branches: `hotfix/<name>` off `main`, merged back to `main` and `develop`.

Initial setup commands

```bash
git init
git add .
git commit -m "feat: PulseBot initial commit - project structure"
git tag v0.1.0-alpha
git checkout -b develop
git checkout -b feature/core-engine
git checkout -b feature/exchange-integration
git checkout -b feature/ai-adaptation
```

Versioning & tags

- `v0.1.0-alpha` → Phase 1 complete
- `v0.2.0-beta`  → Phase 2 complete
- `v0.3.0-rc1`   → Phase 3 complete
- `v1.0.0`       → Production ready

Release checklist (example)

1. Ensure tests pass (`pytest`).
2. Bump version in `src/pulsebot/__init__.py`.
3. Tag the release: `git tag -a vX.Y.Z -m "release vX.Y.Z"`.
4. Merge to `main` and push tags.

Next-phase implementation roadmap

- Phase 1 (v0.1.0-alpha): project skeleton, core engine interfaces, simple strategy scaffold, exchange mock adapters, basic docs.
- Phase 2 (v0.2.0-beta): implement exchange integrations, live market data adapters, strategy execution loop, basic backtester.
- Phase 3 (v0.3.0-rc1): AI-driven signal adapter, robust backtesting with metrics, CI, and deployment pipelines.

Notes

- Keep commits small and focused; use Conventional Commits for readability.


