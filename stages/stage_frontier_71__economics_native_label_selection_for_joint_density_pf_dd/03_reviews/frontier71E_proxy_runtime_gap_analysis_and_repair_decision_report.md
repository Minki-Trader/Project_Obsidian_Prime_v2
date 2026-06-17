# Frontier71E Proxy/Runtime Gap Analysis and Repair(F71E 프록시/런타임 간극 분석 및 수리)

Updated(갱신): 2026-06-16T23:40:18Z

- candidate(후보): `f71b_1e511d3db9c3`
- repair(수리): `f71e_edge_margin_q40_runtime_semantics_repair` / `runtime_compatible_edge_margin_q40`
- status(상태): `completed_runtime_semantics_repair_observation_no_authority`
- judgment(판정): `runtime_semantics_signal_parity_repaired_economics_gap_remaining_no_authority`
- claim boundary(주장 경계): `runtime_semantics_repair_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Gap Cause(간극 원인)

- F71D ONNX parity(온엑스 동등성) and feature readiness(피처 준비)는 통과했다.
- F71D telemetry(런타임 기록)는 `edge_margin_not_met(엣지 마진 미달)`가 지배했다.
- Local diagnosis(로컬 진단): F71B proxy score(프록시 점수)는 custom score(맞춤 점수)였고 EA decision(전문가 자문 결정)은 edge margin(엣지 마진)이어서 threshold semantics mismatch(임계값 의미 불일치)가 생겼다.

## Grok Review(그록 검토)

- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f71e_pre_runtime_semantics_repair/prompts/f71e_pre_runtime_semantics_repair_prompt.md`
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f71e_pre_runtime_semantics_repair/outputs/clean_output.md`
- classification(분류): `accepted_edge_margin_q40_single_repair_probe_needs_local_verification(엣지 마진 q40 단일 수리 탐침 수용, 로컬 검증 필요)`

## Runtime Repair KPI(런타임 수리 핵심 성과 지표)

| split(분할) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | expected signals(예상 신호) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `validation` | `21.77` | `1.04` | `8.18` | `357` | `1.3125` | `357` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |
| `oos` | `36.35` | `1.09` | `5.92` | `258` | `1.3231` | `258` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |

## Runtime Parity Boundary(런타임 동등성 경계)

- research_path(연구 경로): `stage_pipelines/stage_frontier_71/frontier71e_runtime_semantics_repair_probe.py`
- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` plus generated `.set/.ini` files(생성 설정 파일).
- shared_contract(공유 계약): ONNX output order `[p_short,p_flat,p_long]`, feature order hash(피처 순서 해시), edge_margin decision(엣지 마진 결정), RuntimeVetoTape selected-entry mask(선택 진입 차단 테이프).
- known_differences(알려진 차이): this is a repair probe(수리 탐침), not the original F71B custom-score proxy(맞춤 점수 프록시).
- parity_check(동등성 점검): `signal_parity_repaired`.
- runtime_claim_boundary(런타임 주장 경계): runtime_probe(런타임 탐침), no runtime authority(런타임 권위 없음).

## Next Action(다음 행동)

`frontier71F_stage_closeout_economics_native_label_selection_v1`

## Best Runtime Observation(최선 런타임 관찰)

- net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `36.35` / `1.09` / `5.92` / `1.3231`.
