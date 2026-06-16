# F69B Event-First First-Hit Proxy Sweep(F69B 이벤트 우선 선도달 프록시 스윕)

Updated(갱신): 2026-06-16T20:05:21Z

## Hypothesis(가설)

Sparse event-first first-hit opportunity labels(희소 이벤트 우선 선도달 기회 라벨)이 F68 risk-only repair loop(F68 위험 단독 수리 반복)와 다른 PF source(수익 팩터 원천)를 만들 수 있는지 시험했다.

## Action And Effect(행동 및 효과)

Action(행동): compact feature set(압축 피처 묶음), first-hit target(선도달 목표), interpretable model family(해석 가능 모델 계열), event admission(이벤트 진입)을 함께 바꾼 proxy sweep(프록시 탐색)을 실행했다.

Effect(효과): 위험 폭만 고치는 반복을 피하고, 신호 원천이 feature/label/model/event(피처/라벨/모델/이벤트) 축에서 생기는지 확인한다.

## KPI Summary(KPI 핵심 성과 요약)

- candidate rows(후보 행): `3240` summary(요약), `6480` split KPI(분할 KPI).
- scout candidates(탐색 단서 후보): `0`.
- meaningful proxy candidates after control(대조군 후 의미 있는 프록시 후보): `0`.
- top candidate(상위 후보): `f69b_c059a1429316`.
- top validation net/PF/DD/trades_day(상위 검증 순수익/수익 팩터/손실폭/일거래): `771.326973` / `2.653945` / `0.818416` / `0.132731`.
- top OOS net/PF/DD/trades_day(상위 표본외 순수익/수익 팩터/손실폭/일거래): `655.919283` / `3.561207` / `0.761477` / `0.144162`.

## Required Records(필수 기록)

- test period(테스트 기간): validation(검증) 2025-01-01 to 2025-09-30, OOS(표본외) 2025-10-01 to 2026-04-13.
- proxy expectation(프록시 예상): PF movement(수익 팩터 움직임)이 event/label/model axis(이벤트/라벨/모델 축)에서 생기면 pre-MT5 Grok review(사전 MT5 그록 검토)로 간다.
- proxy KPI(프록시 KPI): see(참조) `stages/stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory/02_runs/frontier69B_event_first_first_hit_proxy_sweep_v1/f69b_proxy_candidate_summary.csv` and `stages/stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory/02_runs/frontier69B_event_first_first_hit_proxy_sweep_v1/f69b_proxy_kpi_by_split.csv`.
- runtime probe KPI(런타임 탐침 KPI): pending(대기), proxy-only claim boundary(프록시 전용 주장 경계).
- signal count parity(신호 수 동등성): not_applicable_before_runtime(런타임 전 해당 없음).
- feature readiness parity(피처 준비 동등성): not_applicable_before_runtime(런타임 전 해당 없음).
- proxy/runtime gap cause(프록시/런타임 간극 원인): pending_runtime_probe(런타임 탐침 대기).
- next action(다음 행동): `frontier69C_repair_event_first_label_or_feature_surface_v1`.

## Tier Pair Boundary(티어 쌍 경계)

Tier A separate(Tier A 분리)는 물질화했다. Tier B separate(Tier B 분리)는 `missing_required(필수 누락)`이고, Tier A+B combined(Tier A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`이다.

Effect(효과): Tier A 결과를 전체 알파 판독처럼 과장하지 않고, 다음 repair action(수리 행동)에 Tier B partial-context materialization(Tier B 부분 문맥 물질화)을 남긴다.

## Judgment(판정)

- status(상태): `completed_proxy_scout_repair_required_no_authority`.
- judgment(판정): `proxy_signal_inconclusive_repair_required_no_authority`.
- claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`.
