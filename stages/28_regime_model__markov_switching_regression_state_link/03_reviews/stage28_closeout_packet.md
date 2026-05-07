# Stage28 Markov Regression Closeout Packet(28단계 마르코프 회귀 마감 묶음)

## Judgment(판정)

- stage(단계): `28_regime_model__markov_switching_regression_state_link`
- run range(실행 범위): `run22A-run22B`
- judgment(판정): `closed_inconclusive_markov_regression_state_characteristics_exhausted`
- selected variant(선택 변형): `v01_return_2state_switchvar`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- boundary(경계): `markov_regression_state_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage28(28단계)는 Markov regression(마르코프 회귀)의 state-link(상태 연결)와 sampled state score-table handoff(표본 상태 점수표 인계)를 보존하고, micro-tuning(미세탐색) 없이 Stage29(29단계) topic pivot(주제 전환)으로 이동한다.

## Evidence(근거)

- Python scout(파이썬 탐색): `run22A_markov_regression_state_link_scout_v1`, judgment(판정) `inconclusive_markov_regression_state_link_scout_completed`
- MT5 runtime_probe(MT5 런타임 탐침): `run22B_markov_regression_state_runtime_probe_v1`, judgment(판정) `inconclusive_markov_regression_state_runtime_probe_completed`
- external verification(외부 검증): `completed`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized records(정규화 기록): `6`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`
- validation routed net/PF/trades(검증 라우팅 순손익/수익 팩터/거래 수): `244.08 / 1.77 / 190`
- OOS routed net/PF/trades(표본외 라우팅 순손익/수익 팩터/거래 수): `111.27 / 1.31 / 118`
- MT5 report folder(MT5 보고서 폴더): `stages/28_regime_model__markov_switching_regression_state_link/02_runs/run22B_markov_regression_state_runtime_probe_v1/mt5/reports`

## Tier Views(티어 보기)

- Tier A separate(Tier A 분리): Python(파이썬)은 mostly long-only(대부분 롱 전용) 상태 신호를 만들었고, runtime routed validation(런타임 검증 라우팅)에서 Tier A used(Tier A 사용) `966`개를 기록했다.
- Tier B separate(Tier B 분리): Python(파이썬)은 short/long mix(숏/롱 혼합)를 보였고, runtime routed validation(런타임 검증 라우팅)에서 Tier B fallback used(Tier B 대체 사용) `598`개를 기록했다.
- Tier A+B routed(Tier A+B 라우팅): validation routed rows(검증 라우팅 행) `12210`, OOS routed rows(표본외 라우팅 행) `8646`.

## Preserved Clues(보존 단서)

- user-accepted preserved seed(사용자 수락 보존 씨앗)는 Markov regression(마르코프 회귀) 전체가 아니라 Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)다.
- Markov regression(마르코프 회귀) state direction(상태 방향)은 Tier A(티어 A)에서 long-biased(롱 편향)로 강하게 나타났다.
- Tier B fallback(티어 B 대체)은 partial-context(부분 문맥) 구간을 실제로 메웠고, routed total(실제 라우팅 전체)에 포함됐다.
- MT5 runtime_probe(MT5 런타임 탐침)는 feature-order repair(피처 순서 수정) 뒤 Python score table(파이썬 점수표)과 같은 확률/임계값 의미로 실행됐다.
- validation/OOS routed(검증/표본외 라우팅)는 모두 positive net(양의 순손익)을 보였지만, 이것은 runtime_probe(런타임 탐침) 관찰일 뿐이다.

## Negative Memory(부정 기억)

- run22B(22B 실행)는 native statsmodels MarkovRegression runtime(원본 스탯스모델 마르코프 회귀 런타임)이 아니라 sampled state table handoff(표본 상태표 인계)다.
- 첫 MT5 attempt(첫 MT5 시도)는 metadata-before-feature CSV(메타데이터 선행 피처 CSV) 때문에 false-flat(거짓 무거래)으로 읽혔고, `foundation/mt5/runtime_artifacts.py`에서 feature columns before optional metadata(선택 메타데이터보다 피처 우선)로 수리했다.
- validation/OOS(검증/표본외) 수익은 promotion(승격)이나 runtime authority(런타임 권위)가 아니다.

## Invalid Or Blocked Branches(무효 또는 차단 갈래)

- invalid setup repaired(수리된 무효 설정): metadata columns(메타데이터 열)이 MQL5 feature scanner(MQL5 피처 스캐너)에 feature(피처)로 잡힌 문제를 수정하고 재실행했다.
- blocked retry condition(차단 재시도 조건): `none(없음)` after completed MT5 runtime_probe(MT5 런타임 탐침 완료)

## Next Stage(다음 단계)

Open Stage29(29단계) `29_adaptive_model__river_online_drift_learning` as open-only(개방만). Next exact action(다음 정확한 행동): `run23A_river_online_drift_learning_scout_v1`.

## RUN22C Supplement(22C 실행 보강)

- run(실행): `run22C_markov_regression_supplement_state_variance_attribution_v1`
- judgment(판정): `inconclusive_markov_regression_supplement_completed`
- report(보고서): `stages/28_regime_model__markov_switching_regression_state_link/03_reviews/run22C_markov_regression_supplement_packet.md`
- packet(묶음): `docs/agent_control/packets/stage28_run22C_markov_regression_supplement_state_variance_attribution_v1/aggregate_summary.json`

효과(effect, 효과): Stage28(28단계) closeout(마감)을 되돌리지 않고, 사용자가 요청한 네 가지 보강 질문만 Stage28(28단계) 보존 근거에 붙였다.
