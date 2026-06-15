# Frontier61 Stage Closeout Review(전선61 단계 마감 검토)

Codex local truth(코덱스 로컬 진실):

- stage(단계): `stage_frontier_61__non_long_axis_pf_source_after_friction_memory`
- run(실행): `frontier61Z_runtime_probe_backfill_v1`
- hypothesis(가설): after F53-F60 friction memory(F53-F60 마찰 기억) failed, test non-long-axis side allocation(비롱 축 방향 배분) while keeping feature contract(피처 계약) unchanged.
- selected seed surface(선택 씨앗 표면): `f61b_side_alloc_t38_m2_h4`
- model(모델): ExtraTrees 3-class ONNX(온엑스), class order(클래스 순서) `0=short(숏)`, `1=flat(관망)`, `2=long(롱)`
- proxy(프록시): validation PF(검증 수익 팩터) `0.9798`, OOS PF(OOS 수익 팩터) `1.1169`, validation DD(검증 손실폭) `5.7556`, OOS DD(OOS 손실폭) `3.0752`, trades/day(일 거래) about `4.79`.
- ONNX parity(온엑스 동등성): max_abs_diff(최대 절대 차이) `1.4164e-07`, feature hash(피처 해시) `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`.

MT5 runtime probe observation(MT5 런타임 탐침 관찰):

| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---|---|---:|---:|---:|---:|---:|
| validation_is | completed(완료) | completed(완료) | 0.43 | 53.18 | 12.3115 | 0 | 0 |
| oos | completed(완료) | completed(완료) | 0.71 | 15.16 | 11.4427 | 0 | 0 |

Proxy-runtime gap(프록시-런타임 차이):

- validation PF gap(MT5 minus proxy, MT5-프록시): `-0.5498`; DD gap(손실폭 차이): `+47.4244`; trade count gap(거래 수 차이): `+1376`.
- OOS PF gap(MT5 minus proxy, MT5-프록시): `-0.4069`; DD gap(손실폭 차이): `+12.0848`; trade count gap(거래 수 차이): `+873`.
- signal_count_diff(신호 수 차이) and feature_ready_diff(피처 준비 차이) are both `0`, so local read(로컬 판독) treats this as economics/exit-shape failure(경제성/청산 모양 실패), not handoff failure(인계 실패).

Proposed Codex closeout(코덱스 제안 마감):

- classification(분류): `runtime_probe_observation_no_authority`
- judgment(판정): `negative_memory_side_allocation_failed_runtime_pf(부정 기억, 방향 배분 런타임 PF 실패)`
- claim boundary(주장 경계): observation only(관찰만), no completion(완성 아님), no baseline(기준선 아님), no promotion(승격 아님), no runtime authority(런타임 권위 아님), no live readiness(실거래 준비 아님), no Goal Achieve(목표 달성 아님).
- preserved clue(보존 단서): side allocation preserved proxy DD under 10(방향 배분은 프록시 손실폭 10 미만을 보존했으나), runtime overtraded and degraded PF(런타임에서 과거래와 PF 저하가 발생했다).
- negative memory(부정 기억): side allocation without exit/friction control(청산/마찰 제어 없는 방향 배분)은 runtime PF/DD(런타임 수익 팩터/손실폭)를 망가뜨렸다.

Review request(검토 요청):

Return exactly one of `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)` as the verdict(판정).

Focus only on whether this closeout(마감) is honest under the bounded evidence(제한 근거). Do not suggest promotion(승격) or runtime authority(런타임 권위). If rejected(거절), say the missing local check(빠진 로컬 점검) that must happen before closeout(마감).
