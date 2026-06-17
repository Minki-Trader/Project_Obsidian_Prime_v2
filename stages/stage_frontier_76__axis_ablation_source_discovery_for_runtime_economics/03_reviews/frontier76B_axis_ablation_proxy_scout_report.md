# Frontier76B Axis Ablation Proxy Scout Report(F76B 축 제거 프록시 탐색 보고서)

Run id(실행 ID): `frontier76B_axis_ablation_proxy_scout_v1`

Status(상태): `proxy_scout_meaningful_signal_pre_mt5_probe_required_no_authority`

Judgment(판정): `meaningful_signal_pre_mt5_probe_required_no_authority`

Claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Hypothesis(가설)

Feature/label/model/trade/risk/session ablation(피처/라벨/모델/거래/위험/세션 제거·교체)이 runtime economics source(런타임 경제성 원천)를 식별하거나 반증할 수 있는지 proxy(프록시)로 탐색했다.

## Proxy KPI(프록시 핵심 성과 지표)

- candidate rows(후보 행): `7680`
- model fits completed(완료된 모델 적합): `80/80`
- scout clue count(탐색 단서 수): `2091`
- meaningful signal count(의미 신호 수): `10`
- dual positive count(양분할 양수 수): `1105`

## Best Candidate(최선 후보)

- candidate(후보): `f76b_06637`
- axes(축): feature/model/target/session/risk/cooldown `mega_cap_removed/extra_trees_d7_l60/long_fwd12_q60/cash_open/trend_aligned/0`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `1760.3101806640625/1.594854315978897/6.4446875%/1.0601092896174864/194`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `1471.7918701171875/1.6893374882536825/7.8916796875%/1.1755725190839694/154`

## Gate Read(게이트 판독)

- scout clue gate(탐색 단서 게이트): `one split net>0 or PF>=1.15, trade_count>=50, density>=0.75/day, fragility recorded`
- meaningful signal gate(의미 신호 게이트): `validation+OOS net>0, PF>=1.30, DD<=10%, trades/day>=1.0, trade_count>=100 per split`
- result(결과): `meaningful_signal_pre_mt5_probe_required_no_authority`

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet` sha256 `5bb44b3c041fccb5ccdbc247899c08aaaba6974cef74a65ee7acbc493930ef43`; `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt` sha256 `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- producer(생산자): `stage_pipelines/stage_frontier_76/frontier76b_axis_ablation_proxy_scout.py`
- consumer(소비자): `frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_v1`
- artifact_paths(산출물 경로): `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/f76b_summary.json`, `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/f76b_candidate_results_ranked_top100.csv`, `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/f76b_axis_summary.csv`, `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/f76b_model_fit_summary.csv`, `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/frontier76B_axis_ablation_proxy_scout_report.md`, `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/required_gate_coverage_audit_f76b.md`
- artifact_hashes(산출물 해시): source input hashes(원천 입력 해시)는 local run_manifest(로컬 실행 목록) `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/02_runs/frontier76B_axis_ablation_proxy_scout_v1/run_manifest.json`에 기록했다.
- registry_links(등록부 연결): `docs/registers/run_registry.csv`, `docs/registers/alpha_run_ledger.csv`, `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/stage_run_ledger.csv`
- availability(가용성): review artifacts(검토 산출물)는 tracked(추적됨) 대상이고, run_manifest(실행 목록)는 `stages/*/02_runs/` ignore rule(무시 규칙) 아래 local generated artifact(로컬 생성 산출물)이다.
- lineage_judgment(계보 판정): `connected_with_boundary`

## Runtime Rule(런타임 규칙)

Action(행동): `frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_v1`로 넘긴다.

Effect(효과): meaningful signal(의미 신호)이 없으면 best nonzero/scout candidate(최선 비영/탐색 후보)를 negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침)로 물질화해 proxy/runtime gap(프록시/런타임 간극)을 기록한다. meaningful signal(의미 신호)이 있으면 pre-MT5 Grok review(MT5 전 Grok 검토) 뒤 MT5 Runtime Probe(런타임 탐침)를 실행한다.
