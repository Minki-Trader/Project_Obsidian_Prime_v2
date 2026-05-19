# Stage247 Stage246 Soft Guard Follow-up Review(247단계 246단계 부드러운 보호문 후속 검토)

- stage(단계): `247_adapter_research__stage246_soft_guard_followup_review`
- run(실행): `run247A_stage247_stage246_soft_guard_followup_review_v1`
- source_stage(원천 단계): `246_adapter_research__soft_timestamp_guard_repair_after_stage244_overprune`
- source_run(원천 실행): `run246A_stage246_soft_timestamp_guard_repair_after_stage244_overprune_v1`
- source_stage246_evidence_commit(원천 246단계 근거 커밋): `b6a388299dd99e64595d08529ac4462d578297c9`
- source_stage246_hash_record_commit(원천 246단계 해시 기록 커밋): `528a69d866925607e496b4fe7d7b270c822c7392`
- external_verification_status(외부 검증 상태): `review_only_source_stage246_mt5_reports_completed`
- decision(판정): `open_stage248_bounded_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 판독)

- Stage246(246단계)의 soft guard(부드러운 보호문)는 DD(낙폭)를 줄였다.
- 하지만 validation net(검증 순손익)과 mid PF(중간 수익요인)를 같이 깎았다.
- 가장 가까운 행은 여전히 `s246_cap0305_control`이다. 하지만 이 행도 34D(34D 기준) 대비 net(순손익) `-10.93`, DD(낙폭) `-0.033664`, mid PF(중간 수익요인) 부족이 남는다.
- ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율)는 존재한다. 효과는 필수 기능은 통과했지만, 이것만으로 final adapter(최종 어댑터)가 되지 않는다는 점을 분리해 보여준다.
- 결론은 stronger soft guard(더 강한 부드러운 보호문)가 아니라 entry/source quality repair(진입/원천 품질 수리)로 넘어가는 것이다.

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | class(분류) | val net(검증 순손익) | net gap(순손익 차이) | DD%(낙폭) | DD margin(낙폭 여유) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | read(판독) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| s246_cap0305_control | control_near_miss_not_final | 976.67 | -10.93 | 12.9428 | -0.033664 | 1.522877251 | 775.76 | 가장 가까운 reference surface(참고 표면)이지만 34D(34D 기준) net(순손익), DD(낙폭), mid PF(중간 수익요인)를 동시에 넘지 못했다. |
| s246_softlow_flat003 | soft_guard_dd_helped_but_net_midpf_damaged | 921.30 | -66.30 | 12.2261 | 0.683036 | 1.499804924 | 772.80 | soft guard(부드러운 보호문)는 DD(낙폭)를 줄였지만 validation net(검증 순손익)과 mid PF(중간 수익요인)를 깎았다. |
| s246_softlow_flat005 | soft_guard_dd_helped_but_net_midpf_damaged | 905.28 | -82.32 | 11.6296 | 1.279536 | 1.502614300 | 767.37 | soft guard(부드러운 보호문)는 DD(낙폭)를 줄였지만 validation net(검증 순손익)과 mid PF(중간 수익요인)를 깎았다. |
| s246_softlowmid_lite | soft_guard_dd_helped_but_net_midpf_damaged | 905.70 | -81.90 | 12.0496 | 0.859536 | 1.489840910 | 773.15 | soft guard(부드러운 보호문)는 DD(낙폭)를 줄였지만 validation net(검증 순손익)과 mid PF(중간 수익요인)를 깎았다. |
| s246_softlowmid_balanced | soft_guard_dd_helped_but_net_midpf_damaged | 897.16 | -90.44 | 11.6721 | 1.237036 | 1.499664177 | 765.43 | soft guard(부드러운 보호문)는 DD(낙폭)를 줄였지만 validation net(검증 순손익)과 mid PF(중간 수익요인)를 깎았다. |

## Judgment(판정)

- result_subject(판정 대상): `run247A_stage247_stage246_soft_guard_followup_review_v1`
- evidence_available(사용 근거): Stage246(246단계) MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서), quality matrix(품질 행렬), segment KPI(구간 핵심 성과 지표), balance curve audit(잔고 곡선 감사), risk/ATR telemetry(위험/ATR 기록).
- evidence_missing(부족 근거): Stage248(248단계) entry/source repair(진입/원천 수리) 측정, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `soft_guard_tradeoff_negative_not_final(부드러운 보호문 상충 부정, 최종 아님)`
- claim_boundary(주장 경계): research/development only(연구개발 전용). no deployment(배포 없음), no live_readiness(실거래 준비 없음), no runtime_authority(런타임 권위 없음).
- next_condition(다음 조건): `248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff`에서 entry/source quality(진입/원천 품질)를 좁게 수리하고 같은 KPI(핵심 성과 지표)를 다시 잰다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
