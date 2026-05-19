# Stage253 Stage252 Asymmetric Binding Follow-up Review(253단계 252단계 비대칭 결합 후속 검토)

- stage(단계): `253_adapter_research__stage252_asymmetric_binding_followup_review`
- run(실행): `run253A_stage253_stage252_asymmetric_binding_followup_review_v1`
- source_stage(원천 단계): `252_adapter_research__asymmetric_binding_repair_after_stage250_overprune`
- source_run(원천 실행): `run252A_stage252_asymmetric_binding_repair_after_stage250_overprune_v1`
- source_stage252_evidence_commit(원천 252단계 근거 커밋): `53aa5f020f0b7e6d97325d9fc25b2a50a3be5c1d`
- source_stage252_hash_record_commit(원천 252단계 해시 기록 커밋): `1ae463e528189f7d406580aa99923edf0600aa46`
- external_verification_status(외부 검증 상태): `review_only_source_stage252_mt5_reports_completed`
- decision(판정): `open_stage254_bounded_nonbinding_source_repair_after_binding_axis_no_gain_candidate_not_final`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Plain Read(쉬운 해석)

Stage252(252단계)는 valid evidence(유효 근거)를 만들었지만, strong candidate(강한 후보)는 만들지 못했다.
가장 나은 줄은 control(기준)이고 validation net(검증 순수익) `972.15`, PF(수익요인) `1.59`, DD(낙폭) `12.9281`이다.
하지만 legacy 34D lesson-only KPI target(레거시 34D 교훈 전용 핵심 성과 지표 목표)인 net(순수익) `987.60`, DD(낙폭) `12.909136`을 함께 넘지 못했다.

Effect(효과): binding axis(결합 축)를 primary repair(주 수리축)로 계속 밀지 않고, Stage254(254단계)에서 non-binding source/feature/lifecycle repair(비결합 원천/피처/생명주기 수리)로 넘긴다.

## KPI Tradeoff(핵심 성과 지표 절충)

| adapter(어댑터) | validation PF(검증 수익요인) | validation net(검증 순수익) | net delta vs control(기준 대비 순수익 차이) | DD(낙폭) | DD delta(낙폭 차이) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순수익) | read(해석) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s252_binding_control | 1.59 | 972.15 | 0.00 | 12.9281 | 0.0000 | 1.516650878 | 1.78 | 776.02 | reference_only_best_overall_not_34d |
| s252_short_low_score006 | 1.58 | 830.35 | -141.80 | 9.3294 | -3.5987 | 1.485525742 | 1.81 | 710.44 | dd_improved_but_net_midpf_damaged |
| s252_long_low_score006 | 1.57 | 905.08 | -67.07 | 12.3387 | -0.5894 | 1.545646273 | 1.76 | 726.7 | partial_midpf_dd_signal_but_net_oos_below |
| s252_short_low_gate | 1.53 | 336.96 | -635.19 | 12.9535 | 0.0254 | 1.513601222 | 1.87 | 386.49 | gate_axis_overpruned_trade_supply |
| s252_long_low_gate | 1.52 | 611.36 | -360.79 | 8.8768 | -4.0513 | 1.876033803 | 1.7 | 488.04 | gate_axis_overpruned_trade_supply |

## What Worked A Little(조금 먹힌 부분)

- `s252_short_low_score006`: DD(낙폭)는 `9.3294`로 좋아졌지만 validation net(검증 순수익)이 control(기준)보다 `-141.80` 낮고 mid PF(중간 수익요인)도 나빠졌다.
- `s252_long_low_score006`: mid PF(중간 수익요인)는 control(기준)보다 `+0.028995` 좋지만 validation net(검증 순수익)이 `-67.07`, OOS net(표본외 순수익)이 `-49.32` 낮다.
- `s252_long_low_gate`: mid PF(중간 수익요인) `1.876033803`과 DD(낙폭) `8.8768` 단서는 있으나 OOS DD(표본외 낙폭) `14.2071`과 net(순수익) 손상이 크다.

## What Failed(실패한 부분)

- score-only(점수 전용) 변형은 trade count(거래 수)를 보존했지만 net(순수익)을 올리지 못했다.
- gate(게이트) 변형은 거래 공급을 줄여 DD(낙폭) 일부를 낮췄지만 validation/OOS net(검증/표본외 순수익)을 크게 손상했다.
- ATR/risk(ATR/위험)는 telemetry(원격측정)에 존재하지만, 필요조건이지 충분조건이 아니다.
- Stage252(252단계)의 `--resume-partials(부분 재개)` zero-KPI pitfall(0 핵심 성과 지표 함정)은 final KPI closeout(최종 핵심 성과 지표 종료)에 다시 쓰면 안 된다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): `run253A_stage253_stage252_asymmetric_binding_followup_review_v1`
- evidence_available(사용 근거): quality matrix(품질 행렬), KPI summary(핵심 성과 지표 요약), probability binding(확률 결합), risk/ATR telemetry(위험/ATR 원격측정), source report(원천 보고서)
- evidence_missing(부족 근거): Stage254(254단계) 비결합 수리 실행, ONNX(오닉스) parity(동등성), MT5 ONNX/runtime(MT5 오닉스/런타임) reproduction(재현)
- judgment_label(판정 라벨): `negative_valid_binding_axis_no_gain_not_final`
- next_condition(다음 조건): `254_adapter_research__nonbinding_source_repair_after_binding_axis_no_gain`

## Routing(경로)

Stage253(253단계)는 review-only(검토 전용)로 닫는다.
Next action(다음 행동)은 `run254A_stage254_nonbinding_source_repair_after_binding_axis_no_gain_v1`이다.
Effect(효과): binding(결합) 축의 실패 기억을 보존하고, v2-native(브이투 고유) non-binding repair(비결합 수리)로 연구를 계속한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
