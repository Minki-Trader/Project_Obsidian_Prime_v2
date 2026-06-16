# F69 Stage Brief(F69 단계 개요)

Stage(단계): `stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory`
Opened(개방): 2026-06-16T19:47:04Z

## Hypothesis(가설)

A sparse event-first regime/session and candle-path opportunity model(희소 이벤트 우선 장세/세션 및 캔들 경로 기회 모델)이 F68 risk-only repair loop(F68 위험 단독 수리 반복)와 다른 PF source(수익 팩터 원천)를 만들 수 있는지 시험한다.

## Action And Effect(행동 및 효과)

Action(행동): F69를 event-first axis rotation(이벤트 우선 축 회전) 전선으로 연다.

Effect(효과): F68의 동등성/기록 단서는 보존하지만, 동일 ONNX(온엑스)에 위험 로직만 덧대는 반복을 끊고 새 PF source(수익 팩터 원천)를 찾는다.

## Axis Contract(축 계약)

| axis(축) | F68 surface(F68 표면) | F69 surface(F69 표면) | enforcement(강제 경계) |
|---|---|---|---|
| feature_set(피처 묶음) | full F68F/F68 lifecycle ONNX feature surface(전체 F68F/F68 생명주기 온엑스 피처 표면) | compact event/context feature surface(압축 이벤트/문맥 피처 표면) | write explicit F68F as-is reuse prohibition(F68F 그대로 재사용 금지 명시) |
| label_target(라벨/목표) | lifecycle/cost/DD aggregate label(생명주기/비용/손실폭 집계 라벨) | first-hit opportunity long/short heads(선도달 기회 롱/숏 헤드) | future path starts after entry bar only(미래 경로는 진입봉 이후만 사용) |
| model_family(모델 계열) | F68F ONNX scoring vehicle(F68F 온엑스 점수화 수단) | linear/shallow tree first, optional EBM-like only if local support(선형/얕은 트리 우선, EBM 유사 선택) | interpretable scout before ONNX export(온엑스 내보내기 전 해석 가능 탐색) |
| trade_shape(거래 형태) | dense every-bar scoring with risk repair(촘촘한 매봉 점수와 위험 수리) | event admission, fixed hold, first-hit SLTP(이벤트 진입, 고정 보유, 선도달 손익절) | risk knobs frozen in phase 1(1단계에서 위험 손잡이 고정) |
| risk_logic(위험 로직) | ATR width/capped repair became central(평균진폭 폭/상한 수리가 중심화) | single conservative template until PF movement appears(PF 움직임 전까지 단일 보수 템플릿) | no SLTP-only search until proxy source passes(프록시 원천 통과 전 손익절 단독 탐색 금지) |
| regime_session_split(장세/세션 분할) | not primary attribution axis(주 귀속 축 아님) | open/mid/late, trend/chop/volatility bucket comparisons(초/중/후반, 추세/횡보/변동성 구간 비교) | bucket KPI required in F69B(F69B 구간별 KPI 필수) |

## Required Lifecycle(필수 생명주기)

Hypothesis(가설) -> proxy(프록시) -> mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) -> gap analysis(간극 분석) -> validation/repair/closeout(검증/수리/마감).

F69A is design-only(설계 전용)이다. F69B가 meaningful proxy signal(의미 있는 프록시 신호)을 만들면 pre-MT5 Grok review(사전 MT5 그록 검토)와 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다.

## Grok Stage Open Review(그록 단계 개방 검토)

- prompt_path(프롬프트 경로): `docs/agent_control/grok_reviews/2026-06-17_f69_stage_open_axis_rotation/prompts/f69_stage_open_axis_rotation_prompt.md`
- prompt_hash(프롬프트 해시): `abd3c8b4e4af23528e62ce0dfb51989bc3063f00091f14d6fc3bd1b5a612c9d8`
- clean_output_path(정리 출력 경로): `docs/agent_control/grok_reviews/2026-06-17_f69_stage_open_axis_rotation/outputs/clean_output.md`
- advice_classification(조언 분류): `accepted_with_conditions(조건부 수용)`

## Next Action(다음 행동)

`frontier69B_event_first_first_hit_proxy_sweep_v1`: staged proxy sweep(단계형 프록시 탐색)을 실행한다.

Claim boundary(주장 경계): `stage_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
