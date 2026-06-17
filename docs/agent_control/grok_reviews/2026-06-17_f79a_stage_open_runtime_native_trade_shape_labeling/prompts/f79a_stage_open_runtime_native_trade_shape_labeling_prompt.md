# F79A Stage-Open Grok Prompt(F79A 단계 개방 그록 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

Open Frontier79(전선79) as `runtime_native_trade_shape_labeling_from_fill_path(체결 경로 기반 런타임 네이티브 거래 형태 라벨링)`.
This is a topic pivot(주제 전환), not F78 inheritance(F78 상속 아님).
The point is to vary feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), and regime/session split(장세/세션 분할), not only repair one F78 threshold(임계값).

## Current Truth(현재 진실)

- F78 status(상태): `closed_negative_memory_no_authority`
- F78 judgment(판정): `negative_memory_with_preserved_clue_no_authority`
- F78 closeout report(마감 보고서): `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/stage_closeout_report.md` sha256 `b499ff9460de22b9a1f35a02eb6ed65dbbdeaa85de1f650ba76ffae30f2e897e`
- five-stage retrospective status(5단계 회고 상태): `not_due_after_f78_closeout_3_of_5`, closeouts since last(이전 회고 이후 마감 수): `3`
- dataset rows(데이터 행): `46650`, split counts(분할 수): `{'train': 29222, 'validation': 9844, 'oos': 7584}`
- claim boundary(주장 경계): `stage_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## F78 Preserved Clue(F78 보존 단서)

- ONNX/EA feature and signal parity(ONNX/EA 피처와 신호 동등성)는 정확히 맞출 수 있었다.
- Selected-entry veto tape(선택 진입 거부 테이프)는 proxy selected count(프록시 선택 수)와 runtime signal count(런타임 신호 수)를 맞추는 도구로 보존한다.
- Entry timing(진입 시각)과 DD denominator(손실폭 분모)는 proxy label(프록시 라벨) 설계 시작부터 명시해야 한다.

## F78 Negative Memory(F78 부정 기억)

- Next-bar proxy(다음 봉 프록시)는 양수여도 MT5 same-bar execution(MT5 동일 봉 실행)에서는 음수가 될 수 있다.
- Runtime-aligned entry(런타임 정렬 진입)와 tester-deposit DD(테스터 예치금 손실폭) 수리 뒤 F78F는 scout clue(탐색 단서) 0, meaningful signal(의미 신호) 0이었다.
- F78은 threshold-only(임계값 단독)나 model-only(모델 단독) 수리로 계속 밀면 반복 수리가 된다.

## F79 Axis Contract(F79 축 계약)

| axis(축) | action(행동) | effect(효과) | broad sweep(넓은 탐색) |
|---|---|---|---|
| feature_set(피처 묶음) | test full58, contract_core, price_vol_session, runtime_fill_context, and ablated no_external/no_session sets(전체58, 계약 핵심, 가격/변동성/세션, 런타임 체결 문맥, 외부/세션 제거 묶음 시험) | separates actual source value(원천 가치) from F78 parity-only repair(동등성 단독 수리) | full58, contract_core, price_vol_session, runtime_fill_context, no_external, no_session |
| label_target(라벨/목표) | build same-bar/next-tick fill-path labels with first-touch order, MAE/MFE, net utility, DD-normalized utility, and density quota(동일 봉/다음 틱 체결 경로, 선도달 순서, MAE/MFE, 순효용, 손실폭 정규화 효용, 밀도 할당) | moves entry timing(진입 시각), fill ordering(체결 순서), and tester-deposit DD(테스터 예치금 손실폭)를 proxy expectation(프록시 예상)에 처음부터 넣는다 | fill_path_net, first_touch_utility, mae_mfe_asymmetry, dd_normalized_utility, density_quota |
| model_family(모델 계열) | compare LGBM-like HistGBM, linear/logistic, ExtraTrees, EBM-style shallow additive proxy, and small NN when exportable(히스토그램 GBM, 선형/로지스틱, ExtraTrees, EBM식 얕은 가산 프록시, 내보내기 가능한 작은 신경망) | tests whether runtime-native labels(런타임 네이티브 라벨)이 특정 model bias(모델 편향)에만 걸리는지 분리한다 | logistic, ridge, HistGradientBoosting, ExtraTrees, shallow additive bins, small MLP proxy |
| trade_shape(거래 형태) | vary long/short/both, entry delay, SL/TP first-touch, max hold, opposite exit, cooldown, and one-position occupancy(롱/숏/양방향, 진입 지연, 손절/익절 선도달, 최대 보유, 반대 신호 청산, 쿨다운, 단일 포지션 점유) | treats trade count(거래 수) as realized lifecycle(실현 생명주기), not independent signal count(독립 신호 수) | short, long, both, hold 6/12/18/24, cooldown 0/3/6, SLTP grids |
| risk_logic(위험 로직) | score with Deposit=500 DD, fixed 0.1 lot, spread-aware cost, MAE gate, loss streak guard, and daily DD guard proxies(예치금 500 손실폭, 고정 0.1랏, 스프레드 비용, MAE 게이트, 연속 손실 보호, 일 손실 보호 프록시) | brings drawdown control(손실폭 제어) before MT5 materialization(MT5 물질화) | DD penalty, MAE gate, loss streak cap, daily stop proxy, recovery factor filter |
| regime_session_split(장세/세션 분할) | rotate all/cash_open/cash_mid/cash_late/high_vol/low_vol/trend/chop/day-of-week slices(전체, 현금장 초반/중반/후반, 고변동/저변동, 추세/횡보, 요일 구간) | changes topic surface(주제 표면) without hiding overfit(과적합)를 tiny slice(작은 구간)에 숨기지 않는다 | all, cash_open, cash_mid, cash_late, high_vol, low_vol, trend, chop, dow |

## Question(질문)

Is this F79 stage-open direction(단계 개방 방향) broad and novel enough to address the user's concern that experiments must keep changing feature sets(피처 묶음), labels(라벨), model families(모델 계열), trade shapes(거래 형태), risk logic(위험 로직), and regimes/sessions(장세/세션)?

Also check whether it is properly scoped for proxy scout(프록시 탐색) -> mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) if signal exists(신호가 있으면).

Classify your advice(조언 분류) as accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), or rejected(거절).
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
