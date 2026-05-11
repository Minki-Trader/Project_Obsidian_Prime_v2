# Run50C LogReg Bracket Micro-Grid(50C 실행 로지스틱 회귀 구간 미세 격자)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50C_logreg_bracket_micro_grid_v1`
- model_family(모델군): `LogReg(로지스틱 회귀)` Stage07 full-context Tier A model(Stage07 전체 문맥 Tier A 모델) plus Tier B fallback model(Tier B 대체 모델)
- mt5_attempted(MT5 시도): `True`
- routed_fallback_enabled(라우팅 대체 활성): `True`
- best_current_read(현재 최선 판독): `d38h10` / `weak_routed_dense_engine_candidate_runtime_probe_only`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

- hypothesis(가설): run50B(50B 실행)의 d34h06 density frontier(밀도 경계)와 d40h12 quality frontier(품질 경계) 사이에 실제 A+B routed total(A+B 라우팅 전체) 약한 기준선 후보가 있을 수 있다.
- decision_use(결정 용도): selected_research_baseline(선택 연구 기준선), baseline_candidate_only(기준선 후보 전용), no_dense_engine_found(두꺼운 엔진 없음) 중 최종 판정으로 갈 수 있는지 좁힌다.
- controls(통제): 같은 split(분할), 같은 Stage07 LogReg(로지스틱 회귀), 같은 Tier B partial-context(부분 문맥), 같은 MT5 EA(전문가 자문), 같은 US100 M5 계약을 쓴다.
- changed_variables(변경 변수): short/long threshold(숏/롱 임계값)와 max_hold_bars(최대 보유 봉 수)만 바꾼다.

## Results(결과)

| variant(변형) | A val/day(A 검증/일) | A OOS/day(A 표본외/일) | routed val/day(라우팅 검증/일) | routed OOS/day(라우팅 표본외/일) | routed val PF(라우팅 검증 수익 팩터) | routed OOS PF(라우팅 표본외 수익 팩터) | B val bars(B 검증 봉) | B OOS bars(B 표본외 봉) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| d35h07 | 5.901639 | 4.415385 | 6.387978 | 4.856410 | 0.99 | 1.0 | 2366 | 1062 | `routed_quality_failed_runtime_probe_only` |
| d36h08 | 5.322404 | 4.010256 | 5.754098 | 4.379487 | 1.01 | 0.94 | 2366 | 1062 | `routed_quality_failed_runtime_probe_only` |
| d37h09 | 4.775956 | 3.497436 | 5.147541 | 3.841026 | 1.03 | 1.0 | 2366 | 1062 | `routed_density_or_quality_inconclusive_runtime_probe_only` |
| d38h10 | 4.103825 | 3.097436 | 4.464481 | 3.446154 | 1.07 | 1.13 | 2366 | 1062 | `weak_routed_dense_engine_candidate_runtime_probe_only` |
| d39h11 | 3.628415 | 2.687179 | 3.874317 | 2.953846 | 1.08 | 1.12 | 2366 | 1062 | `routed_density_or_quality_inconclusive_runtime_probe_only` |

## Read(판독)

- 이 실행은 actual routed total(실제 라우팅 전체)을 synthetic sum(합성 합산)으로 만들지 않고, MT5 strategy tester(전략 테스터) 단일 계좌 경로에서 읽는다.
- Tier B fallback(Tier B 대체)은 라우팅에서 실제 사용된 봉 수를 따로 기록한다. 효과는 Tier B 단독 성과와 라우팅 기여를 섞지 않게 하는 것이다.
- live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조)는 주장하지 않는다.
