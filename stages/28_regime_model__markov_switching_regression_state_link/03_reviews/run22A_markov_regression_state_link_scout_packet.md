# RUN22A Markov Regression State-Link Scout Packet(실행22A 마르코프 회귀 상태 연결 탐색 묶음)

## Judgment(판정)

- run(실행): `run22A_markov_regression_state_link_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_markov_regression_state_link_scout_completed`
- selected variant(선택 변형): `v01_return_2state_switchvar`
- boundary(경계): `markov_regression_state_link_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run22A_next_milestone_run22B_markov_regression_state_runtime_probe_v1(실행22A에서는 미시도, 다음 마일스톤은 run22B_markov_regression_state_runtime_probe_v1)`

효과(effect, 효과): MarkovRegression(마르코프 회귀)이 observable return(관측 가능 수익률)을 상태로 나눌 수 있는지 Python-side evidence(파이썬 근거)로 먼저 확인했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `5`
- statsmodels version(스탯츠모델스 버전): `0.14.6`
- Tier A sampled rows(Tier A 표본 행): `4200`
- Tier B sampled rows(Tier B 표본 행): `2600`
- Tier A validation/oos risk separation(Tier A 검증/표본외 위험 분리): `0.0005349897837731987` / `0.0005274139792845745`
- Tier B validation/oos risk separation(Tier B 검증/표본외 위험 분리): `4.08868364492345e-06` / `0.0007315459454112589`
- Tier A collapsed(Tier A 붕괴): `False`
- Tier B collapsed(Tier B 붕괴): `False`

## Preserved Clues(보존 단서)

- Markov regression(마르코프 회귀)은 supervised label(지도 라벨)을 직접 보지 않고 observable return(관측 가능 수익률)과 optional exog(선택 외생 변수)로 state(상태)를 나눈다.
- selected variant(선택 변형) `v01_return_2state_switchvar`는 Tier A/Tier B(티어 A/티어 B) 모두에서 non-collapsed state read(비붕괴 상태 판독)를 남겼다.
- next runtime_probe(다음 런타임 탐침)는 native statsmodels runtime(원본 스탯츠모델스 런타임)이 아니라 state filter/state table(상태 필터/상태표) handoff(인계)처럼 좁게 검증해야 한다.

## Negative Memory(부정 기억)

- run22A(22A 실행)는 sampled structural scout(표본 구조 탐색)라서 full runtime behavior(전체 런타임 행동)를 주장하지 않는다.
- state separation(상태 분리)은 future return relation(미래 수익률 관계) 읽기일 뿐이며 trading edge(거래 우위)가 아니다.
- convergence warning(수렴 경고)이나 failed variant(실패 변형)는 `variant_summary.csv`와 packet(묶음)에 남긴다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run22B_markov_regression_state_runtime_probe_v1` as a narrow MT5 runtime_probe(좁은 MT5 런타임 탐침) after materializing state handoff(상태 인계) files.
