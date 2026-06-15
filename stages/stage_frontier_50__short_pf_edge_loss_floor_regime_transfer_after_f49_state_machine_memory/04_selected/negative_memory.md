# Negative Memory(부정 기억)

F50 negative memory(부정 기억)는 train-only loss-floor regime transfer(학습 전용 손실 하한 체제 전이)이 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): 3
- seed_surface_count(씨앗 표면 수): 0
- runtime_probe_candidate_count(런타임 탐침 후보 수): 0
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_observation_no_authority`
- runtime_probe_run(런타임 탐침 실행): `frontier50Z_runtime_probe_backfill_v1`
- runtime_probe_candidate(런타임 탐침 후보): `f50c_0064`
- runtime_negative_memory(런타임 부정 기억): proxy scout(프록시 탐색)였던 `f50c_0064`는 validation/OOS proxy PF(검증/표본외 프록시 수익 팩터) 1.134967/1.057828에서 MT5 PF(MT5 수익 팩터) 0.81/0.99로 내려갔다. DD(손실폭)는 9.4888/15.6379에서 76.21%/31.52%로 악화됐고 trades(거래)는 1282/912에서 99/71로 압축됐다.
- runtime_interpretation(런타임 해석): signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0이므로 handoff parity(인계 동등성) 문제라기보다 Python first-hit proxy(파이썬 첫 터치 프록시)가 MT5 single-position/order path(MT5 단일 포지션/주문 경로)의 DD/trade-count compression(손실폭/거래수 압축)을 과소평가한 문제다.
- next_do_not_skip(다음 생략 금지): F51부터 scout->MT5 handoff(탐색에서 MT5 인계) 전에 explicit order-path layer(명시적 주문 경로 층) 또는 narrow order-path simulator(좁은 주문 경로 시뮬레이터)를 proxy(프록시)에 넣어야 한다.
- eligibility_rule(적격 규칙): weak positive PF(약한 양수 PF)는 scout threshold(탐색 임계값)을 넘지 못하면 near-miss alpha(근접 알파)가 아니라 negative_memory(부정 기억)로 남긴다.
- do_not_repeat(반복 금지): F49 floor-state gate relabeling(F49 하한 상태 게이트 재라벨링), F48 static state gate(전선48 정적 상태 게이트), F47 percentile risk-budget sweep(전선47 분위수 위험 예산 훑기), F46 sequence-context score-only repair(순서 문맥 점수 전용 수리), F45 same-bar threshold-only repair(동일 봉 임계값 전용 수리), F44 continuous regression(연속 회귀), F42 timing gate(타이밍 게이트), F43 trade-shape source(거래 형태 원천), F38 shallow score quantile repair(얕은 점수 분위수 수리), F39 regime bucket overlay(체제 버킷 덧씌움)를 primary lever(주 레버)로 반복하지 않는다.
