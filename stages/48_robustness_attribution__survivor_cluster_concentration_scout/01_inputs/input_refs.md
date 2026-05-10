# Input References

- source stages: `43`, `44`, `45`, `46`, `47`
- source packets: `docs/agent_control/packets/stage43...` through `stage47...`
- source ledgers: `stages/43.../03_reviews/stage_run_ledger.csv` through `stages/47.../03_reviews/stage_run_ledger.csv`
- regenerated signal source: `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier B fallback source: `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`

Effect: Stage48 uses existing reviewed MT5 KPI and regenerated candidate activation rows. It does not reuse missing heavy Stage43-47 run folders as if they were present.
