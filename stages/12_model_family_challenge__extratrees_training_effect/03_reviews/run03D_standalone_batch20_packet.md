# run03D review packet(검토 묶음)

## Result(결과)

`run03D_et_standalone_batch20_v1`는 Stage12 단독 20개 가설 패키지다. Python structural scout(파이썬 구조 탐색)는 완료됐다.

| rank(순위) | variant(변형) | val signals(검증 신호) | val hit(검증 적중) | oos signals(표본외 신호) | oos hit(표본외 적중) | score(점수) | judgment(판정) |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | v11_base_leaf20_q85 | 1477 | 0.392688 | 1148 | 0.457317 | 2.588295 | inconclusive_standalone_structural_scout |
| 2 | v19_context16_features_q90 | 985 | 0.393909 | 627 | 0.430622 | 2.444602 | inconclusive_standalone_structural_scout |
| 3 | v04_log2_features_leaf20_q90 | 985 | 0.385787 | 739 | 0.441137 | 2.407685 | inconclusive_standalone_structural_scout |
| 4 | v10_bootstrap70_leaf20_q90 | 985 | 0.382741 | 750 | 0.442667 | 2.382416 | inconclusive_standalone_structural_scout |
| 5 | v08_depth12_leaf20_q90 | 985 | 0.385787 | 745 | 0.452349 | 2.382016 | inconclusive_standalone_structural_scout |
| 6 | v09_depth8_leaf10_q90 | 985 | 0.392893 | 721 | 0.482663 | 2.353887 | inconclusive_standalone_structural_scout |
| 7 | v17_top30_features_q90 | 985 | 0.381726 | 792 | 0.460859 | 2.346678 | inconclusive_standalone_structural_scout |
| 8 | v13_base_margin002_q90 | 977 | 0.385875 | 768 | 0.472656 | 2.341653 | inconclusive_standalone_structural_scout |

## Evidence(근거)

- manifest(실행 목록): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2\stages\12_model_family_challenge__extratrees_training_effect\02_runs\run03D_et_standalone_batch20_v1\run_manifest.json`
- KPI record(KPI 기록): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2\stages\12_model_family_challenge__extratrees_training_effect\02_runs\run03D_et_standalone_batch20_v1\kpi_record.json`
- variant results(변형 결과): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2\stages\12_model_family_challenge__extratrees_training_effect\02_runs\run03D_et_standalone_batch20_v1\results\variant_results.csv`
- scored predictions(점수 예측): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2\stages\12_model_family_challenge__extratrees_training_effect\02_runs\run03D_et_standalone_batch20_v1\predictions\scored_validation_oos.parquet`
- summary(요약): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2\stages\12_model_family_challenge__extratrees_training_effect\02_runs\run03D_et_standalone_batch20_v1\summary.json`

## Judgment(판정)

- package judgment(패키지 판정): `inconclusive_standalone_batch20_structural_scout`
- MT5 external verification(메타트레이더5 외부 검증): `out_of_scope_by_claim`.
- effect(효과): 좋은 변형이 있어도 운영 의미로 승격하지 않고, 다음 좁은 MT5 runtime probe(런타임 탐침) 후보만 만든다.
