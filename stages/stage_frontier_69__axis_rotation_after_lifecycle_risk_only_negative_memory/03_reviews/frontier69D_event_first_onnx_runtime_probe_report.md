# F69D Event-First ONNX Runtime Probe(F69D 이벤트 우선 ONNX 런타임 탐침)

Updated(갱신): 2026-06-16T20:48:08Z

## Action And Effect(행동과 효과)

Action(행동): F69B/F69C proxy(프록시)에서 exportable ExtraTrees axes(내보내기 가능한 ExtraTrees 축) 2개를 ONNX(온엑스), RuntimeVetoTape(런타임 차단 테이프), MT5 Strategy Tester(MT5 전략 테스터)로 물질화했다.

Effect(효과): high-PF sparse clue(고PF 희박 단서)와 dense weak-PF clue(촘촘하지만 약한 PF 단서)를 구분해 proxy/runtime KPI gap(프록시/런타임 KPI 간극)을 관찰한다.

- status(상태): `completed_mt5_runtime_probe_observation_no_authority(MT5 런타임 탐침 관찰 완료, 권위 없음)`
- judgment(판정): `runtime_probe_observation_recorded_no_authority(MT5 런타임 탐침 관찰 기록, 권위 없음)`
- Grok advice(그록 조언): `accepted_with_guardrails(보호 장치와 함께 수용)`.
- attempts(시도 수): `4`.

## ONNX And Signal Parity(ONNX와 신호 동등성)

| axis(축) | candidate(후보) | export(내보내기) | probability parity(확률 동등성) | signal parity(신호 동등성) |
|---|---|---|---|---|
| `pf_sparse_export_axis` | `f69b_9dd9ed423f5f` | `exported_onnx_parity_passed` | `True` | `True` |
| `density_weak_export_axis` | `f69b_968cfd55b728` | `exported_onnx_parity_passed` | `True` | `True` |

## Runtime KPI(런타임 핵심 성과 지표)

| axis(축) | split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `pf_sparse_export_axis` | `validation` | `2025-01-02..2025-10-01` | `11.67` | `33.38` | `-21.71` | `1.54` | `2.19` | `17` | `0.0625` | `0` | `0` | `tester_economics_observed(테스터 경제성 관찰)` |
| `pf_sparse_export_axis` | `oos` | `2025-10-01..2026-04-14` | `14.2` | `21.52` | `-7.32` | `2.94` | `1.52` | `7` | `0.035897` | `0` | `0` | `tester_economics_observed(테스터 경제성 관찰)` |
| `density_weak_export_axis` | `validation` | `2025-01-02..2025-10-01` | `25.93` | `409.58` | `-383.65` | `1.07` | `6.45` | `361` | `1.327206` | `0` | `0` | `tester_economics_observed(테스터 경제성 관찰)` |
| `density_weak_export_axis` | `oos` | `2025-10-01..2026-04-14` | `48.38` | `307.32` | `-258.94` | `1.19` | `7.49` | `261` | `1.338462` | `0` | `0` | `tester_economics_observed(테스터 경제성 관찰)` |

## Runtime Parity Boundary(런타임 동등성 경계)

- research_path(연구 경로): `stage_pipelines/stage_frontier_69/frontier69d_event_first_onnx_runtime_probe.py`.
- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` and include modules(포함 모듈).
- shared_contract(공유 계약): feature order hash(피처 순서 해시), ONNX probability output(ONNX 확률 출력), event veto tape(이벤트 차단 테이프), threshold_margin(임계값 마진), ATR SL/TP(ATR 손절/익절), max hold bars(최대 보유 봉).
- known_differences(알려진 차이): proxy first-hit points(프록시 선도달 포인트)와 MT5 account execution(계좌 실행)은 비용/체결/포지션 생명주기가 다르다.

Claim boundary(주장 경계): `runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
