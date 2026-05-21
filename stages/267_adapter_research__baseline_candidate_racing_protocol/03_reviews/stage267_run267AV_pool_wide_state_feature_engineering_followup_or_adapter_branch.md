# Stage267 Run267AV Pool-wide State Feature Engineering Follow-up/Adapter Branch Design(267단계 267AV 후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계)

- action(행동): run267AU(267AU 실행)의 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)를 candidate role decision(후보 역할 결정), next experiment queue(다음 실험 큐), failure memory(실패 기억)로 바꿨다.
- effect(효과): 대표 KPI(headline KPI, 대표 핵심 성과 지표)가 좋아 보여도 바로 고르지 않고, 2024-12(2024년 12월), Monday(월요일), Tier A+B duplicate boundary(Tier A+B 중복 경계)를 다음 검증 조건으로 고정한다.
- status(상태): `run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch_design_completed`
- judgment(판정): `followup_adapter_branch_design_completed_no_candidate_selection`
- profile_decisions(프로필 결정): `8`
- candidate_decisions(후보 결정): `5`
- next_queue_rows(다음 큐 행): `5`
- failure_memory(실패 기억): `5`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

Stage58(58단계)부터 이전 연구를 충분히 활용했느냐는 질문에는 아직 `아니오, 일부만 충분히 활용했다`가 맞다.
Effect(효과): 이전 연구가 버려진 것은 아니지만, 지금 목표가 요구하는 후보군 전체 R&D racing(연구개발 경주), feature ablation(피처 제거), similar replacement(유사 피처 대체), balance/equity curve(잔액/평가금 곡선) 검증까지는 아직 더 펼쳐야 한다.

다만 Stage267(267단계) 안에서는 보완이 진행됐다. run267V/W/X/Y/Z(267V/W/X/Y/Z 실행)는 실제 feature order(피처 순서) 기반 ablation(제거)을 다시 열었고, run267AB부터 run267AU(267AB-AU 실행)는 weak slice(약한 구간), noncalendar state feature(비달력 상태 피처), MT5(MetaTrader 5, 메타트레이더5) 거래 검토까지 이어졌다.
Effect(효과): 이제 문제는 `이전 연구를 썼는가`가 아니라 `아직 깊은 구멍을 통과할 만큼 썼는가`이고, 답은 아직 아니다.

run267AU(267AU 실행)의 핵심 판독은 단순하다. 모든 후보가 순손익과 PF(profit factor, 수익 팩터)는 좋아 보였지만, 모든 후보가 깊은 구간 구멍을 남겼다.
Effect(효과): run267AV(267AV 실행)는 후보 선택이 아니라 다음 압박 설계다.

## Candidate Decisions(후보 결정)

| candidate(후보) | role(역할) | mean net(평균 순손익) | min net(최소 순손익) | worst slice(최악 구간) | holes(구멍) | decision(결정) | next use(다음 용도) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s264_aih` | `challenger_core` | 1147.08 | 1021.47 | -270.97 | 2 | `retain_core_challenger_but_not_selection(핵심 도전자는 유지하지만 선택 아님)` | `second pressure branch on volatility/range interaction(변동성/범위 상호작용 2차 압박 분기)` |
| `s264_lc` | `defensive_control` | 1218.34 | 1218.34 | -268.37 | 1 | `defensive_control_retained_no_selection(방어 기준 유지, 선택 아님)` | `control audit for high headline with repeated weak slice(높은 대표 숫자와 반복 약점 구간 감사)` |
| `s262_lih` | `validation_heavy` | 1127.57 | 1127.57 | -272.80 | 1 | `validation_heavy_control_retained_no_selection(검증 중심 기준 유지, 선택 아님)` | `validation stability comparator under second pressure(2차 압박의 검증 안정성 비교 기준)` |
| `s264_aia` | `oos_anchor` | 1063.83 | 1062.17 | -259.92 | 2 | `retain_oos_anchor_adapter_watch_gate_not_selection(표본외 앵커 어댑터 관찰 게이트, 선택 아님)` | `DD-resilience Adapter watch only after slice gate improves(구간 게이트 개선 뒤 손실폭 견고성 어댑터 관찰)` |
| `s258_stc` | `stress_challenger` | 1040.30 | 905.51 | -285.54 | 2 | `stress_challenger_prune_or_rescue(압박 도전자 가지치기 또는 회수)` | `strict stress gate; remove from active challenger lane if PF/trade/DD fails(엄격 압박 게이트, 수익 팩터/거래 수/손실폭 실패 시 활성 도전자에서 제거)` |

## Top Profile Rows(상위 프로필 행)

| candidate(후보) | profile(프로필) | net(순손익) | PF(수익 팩터) | trades(거래 수) | worst slice(최악 구간) | decision(결정) |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `s264_aih` | `core_volatility_resilience_pressure_v2` | 1272.69 | 1.68 | 296 | `month`/`2024-12` -270.97 | `core_challenger_pressure_gate(핵심 도전자 압박 게이트)` |
| `s264_lc` | `defensive_control_volatility_audit_v1` | 1218.34 | 1.69 | 289 | `weekday`/`Monday` -268.37 | `defensive_control_audit_only(방어 기준 감사 전용)` |
| `s258_stc` | `stress_challenger_trend_prune_pressure_v2` | 1175.10 | 1.57 | 303 | `weekday`/`Monday` -267.44 | `stress_challenger_prune_or_rescue_gate(압박 도전자 가지치기 또는 회수 게이트)` |
| `s262_lih` | `validation_control_volatility_audit_v1` | 1127.57 | 1.61 | 288 | `weekday`/`Monday` -272.80 | `validation_heavy_control_audit_only(검증 중심 기준 감사 전용)` |
| `s264_aia` | `oos_anchor_dd_resilience_pressure_v2` | 1065.48 | 1.63 | 296 | `weekday`/`Monday` -259.92 | `oos_anchor_adapter_watch_gate(표본외 앵커 어댑터 관찰 게이트)` |
| `s264_aia` | `oos_anchor_shock_resilience_pressure_v2` | 1062.17 | 1.65 | 293 | `weekday`/`Monday` -227.89 | `oos_anchor_adapter_watch_gate(표본외 앵커 어댑터 관찰 게이트)` |
| `s264_aih` | `core_range_resilience_pressure_v2` | 1021.47 | 1.59 | 301 | `weekday`/`Monday` -231.65 | `core_challenger_pressure_gate(핵심 도전자 압박 게이트)` |
| `s258_stc` | `stress_challenger_volatility_prune_pressure_v2` | 905.51 | 1.50 | 268 | `weekday`/`Monday` -285.54 | `stress_challenger_prune_or_rescue_gate(압박 도전자 가지치기 또는 회수 게이트)` |

## Next Experiment Queue(다음 실험 큐)

| priority(우선순위) | queue(큐) | workstream(작업 흐름) | candidate scope(후보 범위) | decision use(결정 용도) | stop(중단) |
| --- | --- | --- | --- | --- | --- |
| `P0` | `run267AV_q01_core_challenger_second_pressure` | `noncalendar_state_feature_second_pressure(비달력 상태 피처 2차 압박)` | `s264_aih` | `core challenger keep/downgrade decision(핵심 도전자 유지/강등 결정)` | `do not extend this repair beyond two stages without a new hypothesis(새 가설 없이 이 수리를 두 단계 넘게 끌지 않음)` |
| `P0` | `run267AV_q02_oos_anchor_adapter_watch_gate` | `adapter_watch_gate_after_slice_pressure(구간 압박 뒤 어댑터 관찰 게이트)` | `s264_aia` | `Adapter watch or hold decision(어댑터 관찰 또는 보류 결정)` | `hold Adapter work if slice gate fails once more(구간 게이트가 한 번 더 실패하면 어댑터 작업 보류)` |
| `P1` | `run267AV_q03_control_stability_audit` | `defensive_and_validation_control_audit(방어/검증 기준 감사)` | `s264_lc;s262_lih` | `control retention or retirement decision(기준 유지 또는 퇴역 결정)` | `retire control audit lane if it cannot differentiate the next run(다음 실행에서 차이를 못 내면 기준 감사 분기 종료)` |
| `P0` | `run267AV_q04_stress_challenger_prune_or_rescue` | `stress_challenger_prune_or_rescue(압박 도전자 가지치기 또는 회수)` | `s258_stc` | `active stress lane prune/rescue decision(활성 압박 분기 가지치기/회수 결정)` | `if this gate fails, move to failure memory unless a new feature family appears(이 게이트 실패 시 새 피처군이 없으면 실패 기억으로 이동)` |
| `P0` | `run267AV_q05_true_fallback_route_gap` | `true_tier_b_fallback_route_audit(진짜 Tier B 대체 라우팅 감사)` | `all_baseline_candidates(모든 기준 후보)` | `runtime reproduction readiness blocker(런타임 재현 준비 차단 조건)` | `do not open ONNX lane until this route gap is resolved(이 라우팅 공백 해결 전 ONNX 분기 개방 금지)` |

## Result Boundary(결과 경계)

- positive_claim(긍정 주장): `none(없음)`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- missing_required(필수 누락): second pressure MT5 execution(2차 압박 MT5 실행), true Tier B fallback route(진짜 Tier B 대체 라우팅), Adapter implementation(어댑터 구현), broader period survival(더 넓은 기간 생존성), ONNX parity(ONNX 동등성).
- next_action(다음 행동): `run267AW_materialize_pool_wide_state_feature_engineering_second_followup_queue_from_run267AV_design`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AU/pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review/review_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AU/pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review/candidate_followup_profile_review.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AU/pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review/negative_slice_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AU/pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review/tier_duplicate_review.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch.py`.
- consumer(소비자): `run267AW_materialize_pool_wide_state_feature_engineering_second_followup_queue_from_run267AV_design`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AV/pool_wide_state_feature_engineering_followup_or_adapter_branch/profile_decision_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AV/pool_wide_state_feature_engineering_followup_or_adapter_branch/candidate_branch_decision_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AV/pool_wide_state_feature_engineering_followup_or_adapter_branch/next_experiment_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AV/pool_wide_state_feature_engineering_followup_or_adapter_branch/review_result.json`.
