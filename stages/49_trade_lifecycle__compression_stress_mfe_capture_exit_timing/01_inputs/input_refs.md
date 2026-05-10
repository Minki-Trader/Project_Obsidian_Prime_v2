# Input References(입력 참조)

- Stage45 handoff(45단계 인계): `stages/45_volatility_mechanism__compression_expansion_signal_rebuild/02_runs/run39A_volatility_compression_expansion_broad_mt5_probe_v1/mt5/handoff_manifest.json`
- Stage45 candidate signal table(45단계 후보 신호표): `stages/45_volatility_mechanism__compression_expansion_signal_rebuild/02_runs/run39A_volatility_compression_expansion_broad_mt5_probe_v1/tables/candidate_signal_table.parquet`
- Stage45 score table(45단계 점수표): `stages/45_volatility_mechanism__compression_expansion_signal_rebuild/02_runs/run39A_volatility_compression_expansion_broad_mt5_probe_v1/models/stage45_discrete_signal_score_table.csv`
- Stage48 trade-level records(48단계 거래 단위 기록): `stages/48_robustness_attribution__survivor_cluster_concentration_scout/02_runs/run42B/results/trade_level_records.csv`
- Source candidate(원천 후보): `c08_extreme_compression_stress`
- Rule(규칙): `skip short entries when 20 <= adx_14 <= 25`
