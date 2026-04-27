---
name: obsidian-backtest-forensics
description: Inspect backtest and Strategy Tester evidence, settings, spread, commission, slippage, trade list, deposits, leverage, modeling mode, and report paths before tester results are trusted.
---

# Obsidian Backtest Forensics

Use this skill when work creates, reads, compares, packages, or reports MT5 Strategy Tester, broker terminal, or backtest outputs.

## Required Output

- `tester_identity`: terminal, broker, symbol, timeframe, deposit, leverage, modeling mode, spread, commission, and date range
- `ea_identity`: EA entrypoint, include module hashes, `.set` file, parameter hash, and model or bundle hash
- `report_identity`: report path, snapshot path, terminal output path, and hash when available
- `trade_evidence`: trade count, gross/net result, drawdown, profit factor, and trade list availability
- `cost_assumptions`: spread, commission, slippage, swap, and missing costs
- `forensic_checks`: checks performed against settings drift, missing output, or malformed report
- `backtest_judgment`: usable, usable_with_boundary, inconclusive, invalid, or blocked

## Guardrails

- Do not trust a report if tester identity is unknown.
- Do not compare tester runs with different cost or modeling assumptions as if they are equal.
- Do not call a backtest reviewed when the output path or run identity is missing.
- Do not use tester profit alone as a promotion argument.
