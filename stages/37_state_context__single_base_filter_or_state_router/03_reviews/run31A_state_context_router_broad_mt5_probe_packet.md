# RUN31A State Context Router Broad MT5 Probe(31A 실행 상태 문맥 라우터 넓은 MT5 탐침)

## Judgment(판정)

- result judgment(결과 판정): `state_context_not_useful_or_inconclusive`
- reason(이유): No state structure had positive validation and OOS routed totals with a minimal trade-count floor.
- external verification(외부 검증): `completed`
- boundary(경계): `stage37_structure_judgment_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness`

효과(effect, 효과): 이번 결과는 model structure(모델 구조) 방향만 정한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 없다.

## Evidence(근거)

- common table(공통 테이블): `stages/37_state_context__single_base_filter_or_state_router/02_runs/run31A_state_context_router_broad_mt5_probe_v1/results/common_state_context_response_table.parquet`
- runtime variants(런타임 변형): `4`
- MT5 attempts(MT5 시도): `8`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `24`

| variant(변형) | split(분할) | net(순손익) | PF(수익계수) | trades(거래 수) |
|---|---:|---:|---:|---:|
| simple_context_control | validation_is | 301.81 | 1.26 | 217 |
| simple_context_control | oos | -51.84 | 0.95 | 151 |
| single_base_state_filter | validation_is | 303.22 | 1.71 | 17 |
| single_base_state_filter | oos | -88.9 | 0.84 | 23 |
| single_base_state_adapter | validation_is | -495.45 | 0.47 | 37 |
| single_base_state_adapter | oos | -92.37 | 0.9 | 75 |
| limited_state_specialist_router | validation_is | -498.92 | 0.55 | 85 |
| limited_state_specialist_router | oos | 118.8 | 1.1 | 193 |

## Claim Boundary(주장 경계)

이 packet(묶음)은 broad runtime probe(넓은 런타임 탐침)다. 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.
