# Frontier75B Proxy Scout Report(전선75B 프록시 탐색 보고서)

Run id(실행 ID): `frontier75B_volatility_compression_liquidity_release_proxy_scout_v1`

Stage id(단계 ID): `stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density`

Created(생성): 2026-06-17T04:36:39Z

Status(상태): `proxy_scout_no_meaningful_signal_repair_required_no_authority`

Judgment(판정): `proxy_scout_no_meaningful_signal_repair_required_no_authority`

Claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Hypothesis(가설)

Volatility compression plus liquidity release(변동성 압축 + 유동성 방출)가 F74보다 더 나은 tradeable-density proxy surface(거래 가능한 밀도 프록시 표면)를 만들 수 있는지 시험했다.

## Proxy Expectation(프록시 예상)

Action(행동): compression gate(압축 조건), session gate(세션 조건), feature bundle(피처 묶음), model family(모델 계열), first-touch risk label(선도달 위험 라벨)을 넓게 바꿨다.

Effect(효과): F74처럼 density/parity(밀도/동등성)만 보는 반복을 피하고, net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래)를 함께 본다.

## Proxy KPI(프록시 KPI)

- candidates(후보): `594`
- scout clues(탐색 단서): `11`
- meaningful signals(의미 있는 신호): `0`
- final-like reference only(최종형 참고 전용): `0`
- Best candidate(최선 후보): `f75b_0551` validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래) `2292.5432/1.8815/2.6469/0.9016`, OOS(표본외) `514.0273/1.1963/5.6023/1.0000`.

## Data and Model Boundary(데이터/모델 경계)

- data source(데이터 원천): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`, `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`
- feature-label boundary(피처-라벨 경계): entry features(진입 피처)는 현재 58개 feature(피처)만 사용했고 future OHLC(미래 시고저종)는 label/proxy outcome(라벨/프록시 결과)에만 사용했다.
- model scores(모델 점수): calibrated probabilities(보정 확률)가 아니라 rank scores(순위 점수)다.
- validation threshold(검증 임계값): target trades/day(목표 일거래 수)에 맞춰 validation split(검증 분할)에서 선택했다.

## Runtime Probe Status(런타임 탐침 상태)

MT5 Runtime Probe(MT5 런타임 탐침)는 아직 실행하지 않았다. Effect(효과): 이 결과는 proxy scout(프록시 탐색)이며 runtime authority(런타임 권위)가 아니다. 의미 있는 signal(신호)이 있으면 다음 run(실행)에서 pre-MT5 Grok review(MT5 전 Grok 검토)와 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.

## Next Action(다음 행동)

`frontier75C_volatility_compression_label_risk_repair_proxy_v1`
