# run272B Time-Risk Router Payload Materialization(272B 시간 위험 라우터 페이로드 물질화)

- run_id(실행 ID): `run272B_materialize_time_risk_router_pressure_probe_payloads_v1`
- status(상태): `completed_time_risk_router_pressure_probe_payload_materialization_no_candidate_selection`
- judgment(판정): `pressure_probe_payloads_materialized_no_runtime_or_candidate_claim`
- payload_count(페이로드 수): `4`
- mt5_queue_rows(MT5 탐침 대기열 행): `4`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run272C_execute_or_prepare_time_risk_router_mt5_probe`

## Plain Result(쉬운 결과)

run272B(272B 실행)는 run272A(272A 실행)의 queued pressure branches(대기 중 압박 분기)를 payload parquet(페이로드 파케이), handoff JSON(인계 제이슨), MT5 signal CSV(MT5 신호 CSV)로 물질화했다.
효과(effect, 효과): run272C(272C 실행)가 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)를 준비하거나 실행할 수 있는 파일 단위가 생겼다.

## Materialized Payloads(물질화된 페이로드)

- `run272A_q01_base_router_reference`: role(역할) `reference_control_payload`, Tier A OOS decision_rate(Tier A 표본외 판단 비율) `0.47336498`, judgment(판정) `reference_payload_materialized_no_candidate_claim`
- `run272A_q02_oos_alignment_tight_router`: role(역할) `primary_pressure_payload`, Tier A OOS decision_rate(Tier A 표본외 판단 비율) `0.39200949`, judgment(판정) `primary_pressure_payload_materialized_no_candidate_claim`
- `run272A_q03_route_mix_rebalance_router`: role(역할) `route_mix_payload`, Tier A OOS decision_rate(Tier A 표본외 판단 비율) `0.49485759`, judgment(판정) `route_mix_payload_materialized_no_candidate_claim`
- `run272A_q04_weak_clock_throttle_router`: role(역할) `weak_slice_throttle_payload`, Tier A OOS decision_rate(Tier A 표본외 판단 비율) `0.28639241`, judgment(판정) `weak_slice_throttle_payload_materialized_no_candidate_claim`

## MT5 Probe Queue(MT5 탐침 대기열)

- `run272C_q01` -> `run272A_q01_base_router_reference`: `control_reference`
- `run272C_q02` -> `run272A_q02_oos_alignment_tight_router`: `active_pressure_probe`
- `run272C_q03` -> `run272A_q03_route_mix_rebalance_router`: `active_pressure_probe`
- `run272C_q04` -> `run272A_q04_weak_clock_throttle_router`: `active_pressure_probe`

## Gate Coverage(게이트 커버리지)

- experiment_design(실험 설계): hypothesis/comparison/control/evidence plan(가설/비교/고정/근거 계획)을 receipt(영수증)에 기록했다.
- data_integrity(데이터 무결성): label/future columns(라벨/미래 열)을 payload(페이로드)와 MT5 signal CSV(MT5 신호 CSV)에서 제거했다.
- model_validation(모델 검증): 새 training(학습) 없이 fixed score surface(고정 점수 표면)를 물질화한 범위로 제한했다.
- artifact_lineage(산출물 계보): source inputs(원천 입력), producer(생산자), consumer(소비자), hashes(해시), registry links(등록부 연결)를 기록했다.
- result_judgment(결과 판정): payload materialized(페이로드 물질화)만 말하고 candidate/ONNX/runtime claim(후보/온엑스/런타임 주장)은 열지 않는다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
