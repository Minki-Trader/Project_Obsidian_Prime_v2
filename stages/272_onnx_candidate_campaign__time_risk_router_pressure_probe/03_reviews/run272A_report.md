# run272A Time-Risk Router Pressure Probe Packet(272A 시간 위험 라우터 압박 탐침 묶음)

- run_id(실행 ID): `run272A_design_time_risk_router_pressure_probe_packet_v1`
- status(상태): `completed_time_risk_router_pressure_probe_packet_design_no_candidate_selection`
- judgment(판정): `pressure_probe_packet_ready_no_candidate_selection`
- branch_count(분기 수): `6`
- mt5_probe_design_queue_rows(MT5 탐침 설계 대기열 행): `4`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run272B_materialize_time_risk_router_pressure_probe_payloads`

## Plain Result(쉬운 결과)

run272A(272A 실행)는 cp271B(271B 패키지)를 후보로 고르지 않고 압박 분기(branch, 분기)로 나눴다.
효과(effect, 효과): run272B(272B 실행)가 payload parquet(페이로드 parquet), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)를 만들 수 있는 대기열을 갖게 됐다.

## Tier A OOS Pressure Read(Tier A 표본외 압박 판독)

- `run272A_q01_base_router_reference`: decision_rate(판단 비율) `0.47336498`, alignment_rate(정렬률) `0.29192201`, long_share(롱 비율) `0.51866295`
- `run272A_q02_oos_alignment_tight_router`: decision_rate(판단 비율) `0.39200949`, alignment_rate(정렬률) `0.25159771`, long_share(롱 비율) `0.52909519`
- `run272A_q03_route_mix_rebalance_router`: decision_rate(판단 비율) `0.49485759`, alignment_rate(정렬률) `0.24087397`, long_share(롱 비율) `0.52544631`
- `run272A_q04_weak_clock_throttle_router`: decision_rate(판단 비율) `0.28639241`, alignment_rate(정렬률) `0.21086556`, long_share(롱 비율) `0.56077348`
- `run272A_q05_calendar_regime_guard_router`: decision_rate(판단 비율) `0.0`, alignment_rate(정렬률) ``, long_share(롱 비율) ``
- `run272A_q06_failure_boundary_high_risk_router`: decision_rate(판단 비율) `0.32212553`, alignment_rate(정렬률) `0.20384773`, long_share(롱 비율) `0.45886205`

## Gate Coverage(게이트 커버리지)

- work_packet_schema_lint(작업 묶음 스키마 점검): hypothesis/comparison/control/changed variables/evidence plan(가설/비교/고정/변경 변수/근거 계획)을 receipt(영수증)에 기록했다.
- data_integrity(데이터 무결성): timestamp(타임스탬프), split(분할), Tier A/B(티어 A/B), label boundary(라벨 경계)를 기록했다.
- model_validation(모델 검증): 새 모델 학습이 아니라 fixed score surface(고정 점수 표면)의 train-quantile pressure design(학습 분위수 압박 설계)로 제한했다.
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 주장하지 않는다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
