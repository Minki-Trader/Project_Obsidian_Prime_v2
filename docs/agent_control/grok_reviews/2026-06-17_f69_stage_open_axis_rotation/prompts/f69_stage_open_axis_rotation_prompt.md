# F69 Stage Open Review Prompt(F69 단계 개방 검토 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자) for Project Obsidian Prime v2.

Answer only from this prompt(이 프롬프트 안의 근거만 사용). Do not browse(브라우징 금지), inspect files(파일 확인 금지), run tools(도구 실행 금지), or claim local verification(로컬 검증 주장 금지).

## Current Truth(현재 진실)

- Project(프로젝트): FPMarkets US100 M5(US100 5분봉) ONNX(온엑스) research.
- Frontier rule(전선 규칙): Stage12~364(12~364단계)는 reference only(참조 전용)이다. winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)는 상속하지 않는다.
- Current closed stage(현재 마감 단계): `stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout`.
- F68 closeout label(F68 마감 라벨): `preserved_clue_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음)`.
- Five-stage retrospective(5단계 중간 검토): `not_due_after_f68_closeout_3_of_5(아직 아님, F68 마감 후 3/5)`.
- Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).

## F68 Evidence Snapshot(F68 근거 스냅샷)

F68 tested whether lifecycle/cost/DD-aware proxy(생명주기/비용/손실폭 인식 프록시)가 MT5 runtime economics gap(MT5 런타임 경제성 간극)을 줄일 수 있는지.

Key MT5 Strategy Tester(전략 테스터) observations:

| run/view(실행/보기) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실폭) | trades/day(일 거래 수) | parity(동등성) |
|---|---:|---:|---:|---:|---:|---|
| F68F near-four-axis repair(F68F 네 축 근접 수리) | validation(검증) | 8.91 | 1.01 | 25.06% | 3.97 | signal=0, feature=0 |
| F68F near-four-axis repair(F68F 네 축 근접 수리) | OOS(표본외) | 241.18 | 1.18 | 19.57% | 4.78 | signal=0, feature=0 |
| F68J unit-corrected ATR wide(F68J 단위 보정 평균진폭 넓은 변형) | validation(검증) | -141.58 | 0.94 | 38.55% | 5.71 | signal=0, feature=0 |
| F68J unit-corrected ATR wide(F68J 단위 보정 평균진폭 넓은 변형) | OOS(표본외) | 68.24 | 1.04 | 13.76% | 6.69 | signal=0, feature=0 |

Preserved clues(보존 단서):
- F68F exact signal/feature parity(정확한 신호/피처 동등성) survived MT5(메타트레이더5) materialization.
- F68J unit-corrected ATR telemetry(단위 보정 평균진폭 기록)는 variant differentiation(변형 구분성)을 회복했다.
- F68J OOS DD(표본외 손실폭)는 13.76%까지 낮아졌고 density(밀도)는 6.69/day(일 6.69회)로 목표권에 접근했다.

Negative memory(부정 기억):
- Same F68F ONNX(동일 F68F 온엑스) plus risk-only repair(위험 로직 단독 수리)는 four-axis target(네 축 목표)을 동시에 만들지 못했다.
- Capped ATR repair(상한 평균진폭 수리)는 signature collapse(서명 붕괴)를 만들었다.
- SL/TP/ATR width only(손절/익절/평균진폭 폭만 조정)는 PF source(수익 팩터 원천)가 아니었다.

## Proposed F69 Direction(F69 제안 방향)

Open new frontier stage(새 전선 단계 개방):

`stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory`

First run(첫 실행):

`frontier69A_stage_open_axis_rotation_hypothesis_design_v1`

Hypothesis(가설):

A sparse event-first regime/session and candle-path opportunity model(희소 이벤트 우선 장세/세션 및 캔들 경로 기회 모델) may create a new PF source(새 수익 팩터 원천) by changing multiple major axes at once:

- feature set(피처 묶음): build a compact event/context feature surface(압축 이벤트/문맥 피처 표면) from candle morphology(캔들 형태), session age(세션 경과), volatility/trend/chop regime(변동성/추세/횡보 장세), and selected contract-safe core features(계약 안전 핵심 피처). Do not reuse the full F68F feature/model surface as-is(그대로 재사용 금지).
- label/target(라벨/목표): replace lifecycle-cost aggregate label(생명주기 비용 집계 라벨) with first-hit opportunity labels(선도달 기회 라벨): target-before-stop, MAE guard(불리 이동 보호), and side-specific long/short binary heads(롱/숏 방향별 이진 헤드).
- model family(모델 계열): start with interpretable compact families(해석 가능한 압축 계열), such as linear(선형), shallow tree(얕은 트리), and optional EBM-like shape scout(EBM 유사 형태 탐색) if locally supported.
- trade shape(거래 형태): event admission(이벤트 진입 허용), cooldown(쿨다운), fixed maximum hold(고정 최대 보유), and first-hit SL/TP(선도달 손절/익절), instead of dense every-bar scoring(매 봉 촘촘한 점수화).
- regime/session split(장세/세션 분할): explicitly compare session buckets(세션 구간), open/mid/late behavior(초반/중반/후반 행동), and trend/chop/volatility pockets(추세/횡보/변동성 포켓).
- risk logic(위험 로직): risk stays secondary(위험은 보조). Do not let SL/TP width repair become the main PF source(손절/익절 폭 수리를 주요 PF 원천으로 만들지 않음).

Decision use(결정 사용):
- F69A only opens and designs(개방 및 설계만 수행).
- F69B should run a broad proxy sweep(넓은 프록시 탐색) across the changed axes.
- If proxy signal is meaningful(프록시 신호가 의미 있으면), F69 must run pre-MT5 Grok review(사전 MT5 그록 검토) and mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침).

Claim boundary(주장 경계):

`stage_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Review Question(검토 질문)

Please critique this proposed F69 stage open(제안된 F69 단계 개방)을 answer in this structure(이 구조로 답하라):

1. accepted(수용): what direction is sound(타당한 방향).
2. rejected(거절): what would repeat F68 or overclaim(무엇이 F68 반복 또는 과장 주장인지).
3. needs_local_verification(로컬 검증 필요): what Codex must verify locally(코덱스가 로컬에서 확인해야 하는 것).
4. drift_risks(드리프트 위험): how this could accidentally become another F68 risk-only repair loop(다시 F68 위험 단독 수리 반복이 되는 경로).
5. final_direction_advice(최종 방향 조언): a concise recommendation(간단한 권고).

Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

