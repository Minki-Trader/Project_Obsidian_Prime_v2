# F80 Stage Brief(F80 단계 개요)

Created(생성): 2026-06-17T12:05:00Z

Stage id(단계 ID): `stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics`

Run id(실행 ID): `frontier80A_stage_open_multi_axis_surface_rotation_v1`

## Hypothesis(가설)

F80(전선80)은 F79 fill-order repair(F79 체결 순서 수리)를 반복하지 않고, feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할)을 함께 바꿀 때 runtime economics(런타임 경제성), DD(손실폭), density(밀도), order lifecycle(주문 생명주기)이 같이 살아나는지 시험한다.

## Frontier Context(전선 문맥)

Stage364(364단계) 이후 Frontier(전선)는 Stage365 continuation(365단계 연속)이 아니라 independent campaign(독립 캠페인)이다. Stage12-364(12-364단계)는 reference, not inheritance(참조이지 상속 아님)로만 읽는다.

F64-F67(전선64-67) 교훈은 F80의 기본 게이트다. parity(동등성), ONNX handoff(온엑스 인계), signal count(신호 수)는 MT5 economics(MT5 경제성)를 보장하지 않는다.

## Novelty Delta(신규성 차이)

F79(전선79)는 runtime-native trade-shape label(런타임 네이티브 거래 형태 라벨)과 fill-path repair(체결 경로 수리)를 시험했지만 density(밀도)가 붕괴했다. F80(전선80)은 한 축 수리가 아니라 최소 두 개 이상의 independent surface family(독립 표면 계열)를 만들고, 각 family(계열)에서 6축 중 4축 이상을 실제로 바꾼다.

## Axis Contract(축 계약)

- feature_set(피처 묶음): full58, contract core, price/volatility/session, runtime fill context, no-external, no-session, compact runtime-native subsets(전체58, 계약 핵심, 가격/변동성/세션, 런타임 체결 문맥, 외부 제거, 세션 제거, 압축 런타임 네이티브 묶음)
- label_target(라벨/목표): fill-path utility, order-intent utility, cost/DD normalized utility, density-aware survival, regime-conditioned exit value(체결 경로 효용, 주문 의도 효용, 비용/손실폭 정규화 효용, 밀도 인식 생존, 장세 조건 청산 가치)
- model_family(모델 계열): linear/logistic, ExtraTrees, HistGBM, shallow additive proxy, compact neural candidate when exportable(선형/로지스틱, 엑스트라트리스, 히스토그램 GBM, 얕은 가산 프록시, 내보내기 가능한 압축 신경망 후보)
- trade_shape(거래 형태): long/short/both, entry delay, SL/TP first touch, max hold, opposite exit, one-position occupancy, cooldown(롱/숏/양방향, 진입 지연, 손절/익절 선도달, 최대 보유, 반대 청산, 단일 포지션 점유, 쿨다운)
- risk_logic(위험 로직): Deposit=500 DD, fixed 0.1 lot, spread/commission/slippage, MAE/MFE guard, loss streak, daily DD, time-under-water(예치금 500 손실폭, 고정 0.1랏, 스프레드/수수료/슬리피지, MAE/MFE 보호, 연속 손실, 일 손실폭, 회복 전 체류)
- regime_session_split(장세/세션 분할): all/cash_open/cash_mid/cash_late/high_vol/low_vol/trend/chop/day-of-week(전체/현금장 초반/중반/후반/고변동/저변동/추세/횡보/요일)

## Mandatory Lifecycle(필수 생명주기)

`A open(개방)` -> `B broad + extreme sweep(넓은 훑기 + 극단 훑기)` -> `C WFO-aware selection(워크포워드 인식 선택)` -> `D MT5 runtime probe(MT5 런타임 탐침)` -> `E gap attribution(간극 귀속)` -> `F closeout(마감)`.

Codex Task Force review(코덱스 태스크포스 검토)는 Grok role succession(그록 역할 승계)이 아니다. active five-stage Grok retrospective(활성 5단계 그록 회고)는 이 F80 경로에서 비활성이다.

Claim boundary(주장 경계): `stage_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
