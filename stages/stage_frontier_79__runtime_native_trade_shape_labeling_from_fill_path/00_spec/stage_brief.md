# F79 Stage Brief(F79 단계 개요)

Created(생성): 2026-06-17T10:04:29Z

Stage id(단계 ID): `stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path`

Run id(실행 ID): `frontier79A_stage_open_runtime_native_trade_shape_labeling_from_fill_path_v1`

## Hypothesis(가설)

Runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨)이 actual fill path(실제 체결 경로), entry timing(진입 시각), tester-deposit risk(테스터 예치금 위험), and lifecycle occupancy(생명주기 점유)를 처음부터 label/target(라벨/목표)에 넣으면 F78의 proxy/runtime gap(프록시/런타임 간극)을 줄일 수 있다.

## Novelty Delta(신규성 차이)

F78은 contract P/L(계약 손익)과 parity(동등성)를 맞춘 뒤 entry/deposit repair(진입/예치금 수리)를 했다. F79는 그 수리를 뒤에서 붙이지 않고, fill path(체결 경로)와 trade shape(거래 형태)를 label/target(라벨/목표)의 원천으로 삼는다.

## Axis Contract(축 계약)

- feature_set(피처 묶음): test full58, contract_core, price_vol_session, runtime_fill_context, and ablated no_external/no_session sets(전체58, 계약 핵심, 가격/변동성/세션, 런타임 체결 문맥, 외부/세션 제거 묶음 시험)
- label_target(라벨/목표): build same-bar/next-tick fill-path labels with first-touch order, MAE/MFE, net utility, DD-normalized utility, and density quota(동일 봉/다음 틱 체결 경로, 선도달 순서, MAE/MFE, 순효용, 손실폭 정규화 효용, 밀도 할당)
- model_family(모델 계열): compare LGBM-like HistGBM, linear/logistic, ExtraTrees, EBM-style shallow additive proxy, and small NN when exportable(히스토그램 GBM, 선형/로지스틱, ExtraTrees, EBM식 얕은 가산 프록시, 내보내기 가능한 작은 신경망)
- trade_shape(거래 형태): vary long/short/both, entry delay, SL/TP first-touch, max hold, opposite exit, cooldown, and one-position occupancy(롱/숏/양방향, 진입 지연, 손절/익절 선도달, 최대 보유, 반대 신호 청산, 쿨다운, 단일 포지션 점유)
- risk_logic(위험 로직): score with Deposit=500 DD, fixed 0.1 lot, spread-aware cost, MAE gate, loss streak guard, and daily DD guard proxies(예치금 500 손실폭, 고정 0.1랏, 스프레드 비용, MAE 게이트, 연속 손실 보호, 일 손실 보호 프록시)
- regime_session_split(장세/세션 분할): rotate all/cash_open/cash_mid/cash_late/high_vol/low_vol/trend/chop/day-of-week slices(전체, 현금장 초반/중반/후반, 고변동/저변동, 추세/횡보, 요일 구간)

## Mandatory Lifecycle(필수 생명주기)

Hypothesis(가설) -> proxy scout(프록시 탐색) -> pre-MT5 Grok review(사전 MT5 그록 검토) -> mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) if signal exists(신호 존재 시) -> gap analysis(간극 분석) -> WFO/stress/repair(워크포워드/스트레스/수리) as needed(필요 시) -> closeout(마감).

Claim boundary(주장 경계): `stage_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
