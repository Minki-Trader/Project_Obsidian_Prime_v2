# Stage270 Run270D Balance/Time-Slice/Trade-Quality Review(270단계 270D 잔액/시간구간/거래품질 검토)

- status(상태): `completed_aggressive_probe_balance_timeslice_trade_quality_review_no_survivor_selection`
- judgment(판정): `valid_negative_active_aggressive_probe_no_candidate_selection`
- source_run(원천 실행): `run270C_aggressive_probe_mt5_signal_replay_v1`
- trade_records(거래 기록): `7628`
- parser_mismatch(파서 불일치): `0`
- active_probe_failures(활성 탐침 실패): `4`
- survivors(생존 후보): `0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run270E_stage270_closeout_and_stage271_fresh_thesis_handoff`

## Plain Result(쉬운 결과)

run270D(270D 실행)는 run270C(270C 실행)의 20개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 거래 단위로 다시 읽었다.
효과(effect, 효과): headline KPI(대표 핵심 성과 지표) 뒤에 있는 balance/equity curve(잔액/평가금 곡선), month/session/chron slice(월/세션/순서 구간), trade quality(거래 품질)를 드러낸다.

활성 aggressive probe(공격형 탐침)는 선택 후보로 올라가지 못했다.
효과(effect, 효과): Stage270(270단계)의 aggressive non-filter upside(공격형 비필터 상방) 질문은 failure memory(실패 기억)로 닫을 준비가 됐고, 다음은 새 thesis(논제)로 넘어가는 쪽이다.

## Variant Summary(변형 요약)

| variant(변형) | role(역할) | val net(검증 순수익) | oos net(표본외 순수익) | val PF(검증 수익 팩터) | oos PF(표본외 수익 팩터) | worst DD%(최악 손실폭) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `run270A_q03_supply_expansion_watch` | `active_probe` | 223.03 | -11.74 | 1.09 | 0.99 | 82.14 | `near_breakeven_oos_but_negative_and_dd_fragile_not_survivor` |
| `run270A_q05_cost_relaxed_probe` | `active_probe` | 117.90 | -85.39 | 1.05 | 0.95 | 92.16 | `oos_negative_not_survivor` |
| `run270A_q04_tail_reward_extreme` | `active_probe` | 176.35 | -94.25 | 1.12 | 0.92 | 93.97 | `oos_negative_not_survivor` |
| `run270A_q02_reward_skew_tilt` | `active_probe` | 15.33 | -151.87 | 1.01 | 0.88 | 88.02 | `oos_negative_not_survivor` |
| `run270A_q01_base_materialized_decision` | `control_reference` | 154.17 | 42.56 | 1.09 | 1.03 | 82.26 | `control_reference_positive_but_high_dd_not_candidate` |

## Worst Tier A Slices(최악 Tier A 구간)

| variant(변형) | split(분할) | axis(축) | bucket(구간) | net(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `run270A_q05_cost_relaxed_probe` | `oos` | `weekday` | `Thursday` | -354.53 | 81 | `deep_negative_or_dd_slice` |
| `run270A_q01_base_materialized_decision` | `oos` | `weekday` | `Thursday` | -353.70 | 54 | `deep_negative_or_dd_slice` |
| `run270A_q03_supply_expansion_watch` | `oos` | `month` | `2025-11` | -312.67 | 64 | `deep_negative_or_dd_slice` |
| `run270A_q02_reward_skew_tilt` | `validation_is` | `chron_segment` | `chron_early` | -268.22 | 135 | `deep_negative_or_dd_slice` |
| `run270A_q01_base_materialized_decision` | `validation_is` | `chron_segment` | `chron_early` | -266.52 | 125 | `deep_negative_or_dd_slice` |
| `run270A_q04_tail_reward_extreme` | `oos` | `weekday` | `Thursday` | -250.18 | 47 | `deep_negative_or_dd_slice` |
| `run270A_q02_reward_skew_tilt` | `oos` | `weekday` | `Thursday` | -243.83 | 50 | `deep_negative_or_dd_slice` |
| `run270A_q03_supply_expansion_watch` | `oos` | `chron_segment` | `chron_early` | -239.03 | 147 | `deep_negative_or_dd_slice` |
| `run270A_q04_tail_reward_extreme` | `validation_is` | `chron_segment` | `chron_early` | -229.53 | 103 | `deep_negative_or_dd_slice` |
| `run270A_q03_supply_expansion_watch` | `oos` | `weekday` | `Thursday` | -224.13 | 81 | `deep_negative_or_dd_slice` |
| `run270A_q05_cost_relaxed_probe` | `validation_is` | `chron_segment` | `chron_early` | -199.16 | 182 | `deep_negative_or_dd_slice` |
| `run270A_q01_base_materialized_decision` | `validation_is` | `month` | `2025-03` | -195.22 | 49 | `deep_negative_or_dd_slice` |

## Tier Boundary(티어 경계)

- duplicate_audit_rows(중복 감사 행): `10`
- interpretation(해석): Tier B(Tier B)는 이번 run270C(270C 실행)에서 별도 structural replay(구조 재생)로 Tier A(Tier A)와 mirror duplicate(거울 중복)를 만들었다.
- effect(효과): 이 결과는 Tier B fallback authority(Tier B 대체 권위)나 actual routed total(실제 라우팅 전체)이 아니다.

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): symbol(심볼) `US100`, timeframe(시간봉) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`.
- date_ranges(날짜 범위): `oos 2025.10.01 to 2026.04.14; validation_is 2025.01.02 to 2025.10.01`.
- trade_evidence(거래 근거): parser checks(파서 점검) `20`, mismatch(불일치) `0`.
- cost_assumptions(비용 가정): `strategy_tester_report_costs_only_no_cost_edge_claim`.
- backtest_judgment(백테스트 판정): `usable_with_boundary`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/02_runs/run270C/execution_result.json`, `stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/02_runs/run270C/mt5_kpi_summary.csv`, `stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/02_runs/run270C/backtest_forensics.csv`, `stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/02_runs/run270A/aggressive_probe_variant_plan.csv`.
- producer(생산자): `stage_pipelines/stage270/review_aggressive_probe_balance_timeslice_trade_quality.py`.
- consumer(소비자): `run270E_stage270_closeout_and_stage271_fresh_thesis_handoff`.
- artifact_paths(산출물 경로): `stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/02_runs/run270D/trade_records.csv`, `stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/02_runs/run270D/time_slice_kpi.csv`, `stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/02_runs/run270D/curve_diagnostics.csv`, `stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/02_runs/run270D/variant_summary.csv`.
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Required Gate Coverage(필수 게이트 커버리지)

- kpi_contract_audit(KPI 계약 감사): `passed`
- row_grain_audit(행 단위 감사): `passed`
- source_authority_audit(원천 권위 감사): `passed`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): `passed`
- final_claim_guard(최종 주장 가드): `passed_no_selected_candidate_no_onnx_no_goal_achieve`

## Boundary(경계)

- positive_claim(긍정 주장): `none`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(온엑스 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- operating_promotion(운영 승격), runtime_authority(런타임 권위), deployment(배포): `not_claimed`.
