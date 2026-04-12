# Changelog

All notable changes to this project will be documented in this file.

## [0.7.0] - 2026-03-29

### Added
- **Walk-Forward Backtesting** (`walk_forward_backtest_strategy`):
  - Splits data into N folds (train/test) to validate strategy on unseen forward data
  - Per-fold in-sample vs out-of-sample return comparison
  - **Robustness score** (test/train ratio): ROBUST ≥ 0.8 | MODERATE ≥ 0.5 | WEAK ≥ 0.2 | OVERFITTED < 0.2
  - Aggregate out-of-sample metrics: Sharpe, win rate, max drawdown, total return
  - Supports 2–10 splits, configurable train ratio, both 1d and 1h intervals
- **Full Trade Log** (`include_trade_log=True`):
  - Per-trade breakdown: entry/exit date & price, holding days, gross/net return %, cost %
  - Running capital and cumulative return at each trade
- **Equity Curve** (`include_equity_curve=True`):
  - Capital value + drawdown % at each trade exit — ready for charting
  - ⚠️ Note: on long 1h backtests (e.g. 2+ years of hourly data) this list can get large; consider disabling if only reviewing summary stats
- **1h (Hourly) Timeframe** (`interval="1h"`):
  - All strategies and compare now support intraday hourly data
  - Sharpe ratio annualization corrected for 1h bars (252 × 6 trading hours)
  - Works on `backtest_strategy`, `compare_strategies`, and `walk_forward_backtest_strategy`

### Changed
- `backtest_strategy` tool: added `interval`, `include_trade_log`, `include_equity_curve` params
- `compare_strategies` tool: added `interval` param; now documents all 6 strategies (was 4)
- `run_backtest()` now returns last 5 trades always (`recent_trades`) for quick inspection
- Sharpe ratio calculation now uses interval-aware annualization factor

### Notes (personal)
- I changed the default number of walk-forward splits from 5 to 3 in my local config — 5 folds felt like overkill for the shorter crypto datasets I usually test on.
- Changed default `train_ratio` from 0.7 to 0.8 locally — I prefer giving the model more training data, especially on 1h intervals where there's more noise.
- Set default `interval` to `"1h"` in my local copy of `backtest_strategy` — I mostly test crypto intraday and got tired of specifying it every time.
- Bumped default `initial_capital` from 10000 to 1000 locally — easier to mentally track % returns when starting from a round number I actually trade with.
- Bumped `recent_trades` count from 5 to 10 locally — 5 trades wasn't enough context when reviewing 1h backtest results with lots of short-duration trades.
- Set default `include_trade_log` to `True` locally — I always end up enabling it anyway, so saves a step every run.
- Set default `include_equity_curve` to `True` locally — same reasoning as trade log; I always want the curve for visual review.
- Reminder: if running walk-forward on 1h data with equity curve enabled, memory can spike noticeably — may want to flip `include_equity_curve` back to `False` for those runs specifically.
- Lowered default `commission` from 0.1% to 0.075% locally — closer to what I actually pay on Binance with BNB fee discount applied.
