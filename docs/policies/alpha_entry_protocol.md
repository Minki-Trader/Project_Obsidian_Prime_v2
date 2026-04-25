# Alpha Entry Protocol(알파 진입 규칙)

- 갱신일(updated_on, 갱신일): `2026-04-25`
- 소유 단계(owner stage, 소유 단계): `08_alpha_entry_protocol__tier_reporting_search_rules`
- 상태(status, 상태): `defined_for_pre_alpha_handoff(알파 전 인계용 정의됨)`

## 목적(Purpose, 목적)

이 문서는 model-backed alpha exploration(모델 근거 알파 탐색)을 시작할 때 쓸 근거(evidence, 근거), 보고(reporting, 보고), 실패 기억(failure memory, 실패 기억), 승격 아님 경계(no-promotion boundary, 승격 아님 경계)를 정한다.

효과(effect, 효과)는 alpha idea(알파 아이디어)를 자유롭게 탐색하면서도, alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 섞어 말하지 않게 하는 것이다.

## 현재 경계(Current Boundary, 현재 경계)

이 규칙(protocol, 규칙)은 alpha result(알파 결과)가 아니다.

Stage 07(7단계) baseline training smoke(기준선 학습 스모크)는 Python-side training pipeline evidence(파이썬 측 학습 파이프라인 근거)다. 이것은 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 뜻하지 않는다.

Stage 08(8단계)의 행동(action, 행동)은 alpha entry rule(알파 진입 규칙)을 문서화하는 것이다. 그 효과(effect, 효과)는 Stage 09(9단계)가 registry/current truth/publish packet(등록부/현재 진실/게시 묶음)을 정리할 수 있게 하는 것이다.

## Allowed Evidence(허용 근거)

alpha exploration(알파 탐색)은 아래 근거(evidence, 근거)를 사용할 수 있다.

| evidence surface(근거 표면) | allowed use(허용 사용) | effect(효과) |
|---|---|---|
| Stage 02/04(2/4단계) materialized dataset(물질화 데이터셋)과 Stage 04(4단계) 58 feature model input(58개 피처 모델 입력) | 첫 model-backed alpha input surface(모델 근거 알파 입력 표면)로 쓴다 | 입력 표면(input surface, 입력 표면)을 고정해서 조용한 데이터 변경(silent data change, 조용한 데이터 변경)을 막는다 |
| Stage 03/04(3/4단계) label/split contract(라벨/분할 계약) | 첫 default label(기본 라벨)과 split(분할)으로 쓴다 | horizon(예측 수평선), class threshold(클래스 임계값), train/validation/OOS(학습/검증/표본외) 해석을 고정한다 |
| Stage 05(5단계) feature integrity audit(피처 무결성 감사) | feature formula/time/external alignment/label leakage(피처 수식/시간/외부 정렬/라벨 누수) 근거로 쓴다 | 계산과 정렬의 기본 신뢰를 제공하지만 model quality(모델 품질)를 주장하지 않는다 |
| Stage 06(6단계) runtime parity closed evidence(런타임 동등성 폐쇄 근거) | minimum fixture set(최소 표본 묶음)의 Python/MT5 parity(파이썬/MT5 동등성) 근거로 쓴다 | 런타임 계산 표면(runtime calculation surface, 런타임 계산 표면)을 좁게 고정하지만 alpha quality(알파 품질)를 주장하지 않는다 |
| Stage 07(7단계) baseline training smoke(기준선 학습 스모크) | preprocessing policy/training run contract/model artifact identity(전처리 정책/학습 실행 계약/모델 산출물 정체성) 근거로 쓴다 | 학습 파이프라인(training pipeline, 학습 파이프라인)이 실행된다는 근거를 주지만 alpha quality(알파 품질)가 아니다 |
| future alpha run report(향후 알파 실행 보고서) | report identity(보고서 정체성), split/window(분할/창), metrics(지표), judgment(판정)을 갖춘 뒤 참고한다 | 같은 아이디어를 비교하고 실패를 반복하지 않게 한다 |

다음은 허용 근거(allowed evidence, 허용 근거)가 아니다.

- legacy winner(과거 승자), legacy promotion history(과거 승격 이력), old Stage pressure(과거 단계 압력)
- Tier A only anchor(Tier A만 기준선이라는 주장)
- Tier B pre-validation gate(Tier B 사전검증 제한문)
- Stage 07 smoke(7단계 스모크)를 alpha quality(알파 품질)로 읽는 주장
- MT5 price-proxy weights(MT5 가격 대리 가중치)를 actual NDX/QQQ weights(실제 NDX/QQQ 가중치)로 읽는 주장

## Tier A/B Reporting(티어 A/B 보고)

Tier label(티어 라벨)은 sample label(표본 라벨)이다. exploration permission(탐색 허가)이 아니다.

- Tier A(티어 A): full-context sample(전체 문맥 표본)
- Tier B(티어 B): partial-context sample(부분 문맥 표본)
- Tier C(티어 C): weak sample(약한 표본) 또는 명시적으로 허용된 local research(로컬 연구)

보고서(report, 보고서)는 Tier label(티어 라벨), data scope(데이터 범위), missing context(빠진 문맥), interpretation risk(해석 위험)를 적는다. 이 행동(action, 행동)의 효과(effect, 효과)는 Tier A/B(티어 A/B)를 비교 가능하게 하면서도, 티어(tier, 티어)를 탐색 제한문(gate, 제한문)으로 만들지 않는 것이다.

Tier A(티어 A)와 Tier B(티어 B)를 한 표에 같이 보일 수 있다. 다만 각 행(row, 행)은 자신의 tier label(티어 라벨)과 split/window(분할/창)를 유지한다.

## Single Split Scout(단일 분할 탐색 판독)

single split scout(단일 분할 탐색 판독)는 빠른 구조 판독(structural scout, 구조 스카우트)이다.

허용 행동(action, 행동):

- 첫 default split(기본 분할)의 train/validation/OOS(학습/검증/표본외)를 그대로 쓴다.
- model family(모델 계열), feature subset(피처 부분집합), threshold idea(임계값 아이디어), probability use(확률 사용)를 빠르게 비교한다.
- report status(보고 상태)에 `single_split_scout(단일 분할 탐색 판독)`를 적는다.

효과(effect, 효과)는 많은 alpha idea(알파 아이디어)를 빠르게 걸러 보되, robustness(견고성)나 operating promotion(운영 승격)을 주장하지 않는 것이다.

single split scout(단일 분할 탐색 판독) 결과는 `positive(긍정)`, `negative(부정)`, `inconclusive(불충분)`, `invalid(무효)`로 판정할 수 있다. 하지만 그 판정은 scout boundary(탐색 판독 경계) 안에서만 유효하다.

## Main Alpha Scope(메인 알파 범위)

Stage 10(10단계)부터 알파 탐색(alpha exploration, 알파 탐색)이 닫히는 단계(stage, 단계)까지는 다음 축(axis, 축)을 기본 main alpha scope(메인 알파 범위)로 연다.

- label(라벨)
- feature(피처)
- model(모델)
- decision surface(의사결정 표면)
- entry(진입)
- exit(청산)
- sizing/overlay(사이징/오버레이)
- retrain/carry(재학습/유지)
- combination mainline(조합형 메인라인)

이 축(axis, 축)은 edge exploration(엣지 탐색, 가장자리 탐색)이 아니라 기본 알파 탐색(alpha exploration, 알파 탐색)이다. 효과(effect, 효과)는 모델 점수(model score, 모델 점수)만 보지 않고, MT5(`MetaTrader 5`, 메타트레이더5) 실행 표면(execution surface, 실행 표면)에서 실제 거래 구조(trade structure, 거래 구조)가 살아남는지 보게 하는 것이다.

## Mainline Run Discipline(메인라인 실행 규율)

각 알파 탐색 단계(alpha exploration stage, 알파 탐색 단계)는 하나의 핵심 주제(core topic, 핵심 주제)를 끝까지 학습(training, 학습), 최적화(optimization, 최적화), 압박 시험(stress test, 압박 시험)한다.

- `run01A`, `run01B`, `run01C`는 미리 정한 단계별 역할(role, 역할)이 아니다.
- 각 실행(run, 실행)은 같은 핵심 주제(core topic, 핵심 주제)를 계속 미는 순서 번호(sequence number, 순서 번호)다.
- 실행 목적(run purpose, 실행 목적)은 각 `run_manifest.json(실행 목록)`에 따로 적는다. 예시는 base learning(기본 학습), neighborhood shake(주변 흔들기), extreme sweep(극단값 탐색), boundary check(경계값 확인), MT5(`MetaTrader 5`, 메타트레이더5) rerun(MT5 재실행), recovery run(복구 실행)이다.
- `run02A`는 새 핵심 주제(new core topic, 새 핵심 주제)나 새 stage(새 단계)를 뜻하지 않는다. 같은 단계(stage, 단계) 안에서 탐색 묶음(exploration packet, 탐색 묶음)을 새로 나눌 필요가 있을 때 쓴다.
- 실행 개수(run count, 실행 개수), 후보 수(candidate count, 후보 수), 탐색 폭(search width, 탐색 폭)은 미리 닫지 않는다.

다음 단계(next stage, 다음 단계)는 현재 단계(stage, 단계)의 핵심 주제(core topic, 핵심 주제)가 충분히 밀렸고, 남은 갈래(branches, 갈래)가 positive handoff(긍정 인계), negative memory(부정 기억), inconclusive boundary(불충분 경계), invalid setup(무효 설정), blocked retry condition(차단 재시도 조건) 중 하나로 정리됐을 때만 연다.

효과(effect, 효과)는 한 단계(stage, 단계) 안에서 label(라벨), feature(피처), model(모델), decision surface(의사결정 표면), entry(진입), exit(청산), sizing/overlay(사이징/오버레이), retrain/carry(재학습/유지)를 충분히 밀어붙이되, 실행마다 무엇을 흔들었는지 잃지 않게 하는 것이다.

탐색 라벨(exploration label, 탐색 라벨)과 실행 번호(run number, 실행 번호)는 `docs/policies/stage_structure.md`의 알파 탐색 이름 규칙(Alpha Exploration Naming, 알파 탐색 이름 규칙)과 알파 탐색 실행 번호 규칙(Alpha Run Numbering, 알파 실행 번호 규칙)을 따른다.

## WFO(walk-forward optimization, 워크포워드 최적화)

WFO(walk-forward optimization, 워크포워드 최적화)는 serious optimization(진지한 최적화)의 기본 방식이다.

필수 행동(action, 행동):

- window plan(창 계획)을 먼저 적는다.
- 각 window(창)의 train/validation/OOS(학습/검증/표본외)를 적는다.
- window별 metrics(창별 지표)와 aggregate metrics(집계 지표)를 분리한다.
- tuning rule(튜닝 규칙)과 locked rule(고정 규칙)을 분리한다.

효과(effect, 효과)는 alpha idea(알파 아이디어)가 한 구간에만 맞는지, 시간 이동(time shift, 시간 이동)에도 버티는지 확인하는 것이다.

WFO(walk-forward optimization, 워크포워드 최적화) 통과는 operating promotion(운영 승격)이 아니다. WFO(워크포워드 최적화)는 promotion_candidate(승격 후보)를 논의할 수 있는 근거가 될 수 있지만, 별도 operating promotion decision(운영 승격 결정)을 대신하지 않는다.

## Metrics(지표)

보고서(report, 보고서)는 실행 목적(run purpose, 실행 목적)에 맞는 metrics(지표)를 층(layer, 층)으로 나눠 적는다.

효과(effect, 효과)는 accuracy(정확도) 하나나 profit number(수익 숫자) 하나가 alpha quality(알파 품질)처럼 보이는 일을 막는 것이다.

### 0. Scoreboard And Trial Accounting(점수판과 실험 회계)

탐색이 여러 후보(candidate, 후보), 여러 파라미터(parameter, 파라미터), 여러 창(window, 창)을 비교했다면 먼저 적는다.

- scoreboard lane(점수판 레인): `structural_scout/regular_risk_execution(구조 탐색/정규 위험 실행)`
- run/trial count(실행/실험 횟수)
- completed/failed trial count(완료/실패 실험 수)
- failed reason summary(실패 사유 요약)
- candidate family count(후보 계열 수)
- parameter grid/range(파라미터 격자/범위)
- selected rank(선택 순위)
- primary KPI(`key performance indicator`, 핵심 성과 지표)
- guardrail KPI(보호 지표)
- disqualifier(탈락 조건)
- PBO(`Probability of Backtest Overfitting`, 백테스트 과최적화 확률)
- DSR(`Deflated Sharpe Ratio`, 보정 샤프 비율)
- multiple testing note(다중 검정 메모)
- parameter neighborhood robustness(파라미터 주변 견고성)

이 행동(action, 행동)의 효과(effect, 효과)는 가장 좋아 보이는 한 결과가 넓은 search space(탐색 공간)와 과최적화 위험(overfitting risk, 과최적화 위험)을 숨기지 못하게 하는 것이다.

### 1. Identity And Coverage(정체성과 커버리지)

모든 보고서(report, 보고서)에 적는다.

- dataset id(데이터셋 ID), label id(라벨 ID), split id(분할 ID)
- feature count(피처 수)와 feature order hash(피처 순서 해시)
- rows by split/window(분할/창별 행 수)
- class balance(클래스 균형)
- missing/invalid row count(누락/무효 행 수)
- prediction coverage(예측 커버리지)
- no-prediction/no-trade rate(무예측/무거래 비율)

이 행동(action, 행동)의 효과(effect, 효과)는 서로 다른 표본(sample, 표본)이나 다른 피처 입력(feature input, 피처 입력)을 같은 결과처럼 비교하지 않게 하는 것이다.

### 2. Signal Quality(신호 품질)

분류 모델(classification model, 분류 모델)이나 확률 모델(probability model, 확률 모델)을 말하면 적는다.

- accuracy(정확도)
- balanced accuracy(균형 정확도)
- macro F1(매크로 F1)
- per-class precision/recall/F1(클래스별 정밀도/재현율/F1)
- confusion matrix(혼동 행렬)
- baseline comparison(기준선 비교): majority class(다수 클래스), random baseline(무작위 기준선), Stage 07 smoke(Stage 07 스모크) 중 해당되는 것
- directional hit rate(방향 적중률): flat(중립)을 제외한 방향 신호가 있으면 적는다.
- lift by confidence bucket(확신도 구간별 리프트): 확률이 높을수록 실제 성과가 좋아지는지 본다.

이 행동(action, 행동)의 효과(effect, 효과)는 모델이 단순히 많이 나온 클래스(class, 클래스)를 맞힌 것인지, 실제 방향 신호(signal, 신호)가 있는지 분리하는 것이다.

### 3. Probability Quality(확률 품질)

확률(probability, 확률)을 decision threshold(판정 임계값), position sizing(포지션 크기), filtering(필터링)에 쓰면 적는다.

- log loss(로그 손실)
- Brier score(브라이어 점수)
- calibration by probability bucket(확률 구간별 보정)
- expected calibration error(ECE, 기대 보정 오차)
- confidence distribution(확신도 분포)
- entropy or margin(엔트로피 또는 1위/2위 확률 차이)
- probability row-sum check(확률 행 합 검사)

이 행동(action, 행동)의 효과(effect, 효과)는 높은 확률(high probability, 높은 확률)이 실제로 더 믿을 만한 신호인지 확인하는 것이다.

### 4. Threshold And Decision Shape(임계값과 판정 형태)

threshold rule(임계값 규칙), flat filter(중립 필터), entry filter(진입 필터)를 쓰면 적는다.

- decision threshold(판정 임계값)
- signal count by class(클래스별 신호 수)
- threshold sweep(임계값 스윕)
- precision/coverage curve(정밀도/커버리지 곡선)
- no-trade rate(무거래 비율)
- turnover estimate(회전율 추정)
- long/short mix(롱/숏 비율)
- rule_pass_rate(규칙 통과율): 각 entry/filter/exit rule(진입/필터/청산 규칙)이 표본을 얼마나 통과시키는지 적는다.
- context hit-rate(문맥 적중률): session/regime/day context(세션/국면/요일 문맥)가 실제 유효 신호와 얼마나 맞는지 적는다.

이 행동(action, 행동)의 효과(effect, 효과)는 성과가 모델 자체에서 온 것인지, 임계값이나 필터(filter, 필터)가 표본을 너무 줄여서 생긴 착시인지 확인하는 것이다.

### 5. Stability And Slice Quality(안정성과 조각 품질)

positive(긍정)나 promotion_candidate(승격 후보)로 말하려면 적는다.

- train/validation/OOS gap(학습/검증/표본외 격차)
- month/quarter slice(월/분기 조각)
- session/time-of-day slice(세션/시간대 조각)
- volatility regime slice(변동성 국면 조각)
- long vs short asymmetry(롱/숏 비대칭)
- subperiod consistency(하위 기간 일관성)
- WFO window consistency(WFO 창 일관성)
- parameter neighborhood robustness(파라미터 주변 견고성)
- parameter cliff/plateau read(파라미터 절벽/평탄 구간 판독)
- bridge non-regression(브리지 비퇴행): 긴 연결 구간(bridge, 연결 구간)에서 기준선보다 후퇴하지 않는지 적는다.
- PBO(`Probability of Backtest Overfitting`, 백테스트 과최적화 확률): 여러 후보나 WFO matrix(WFO 행렬)가 있으면 적는다.
- DSR(`Deflated Sharpe Ratio`, 보정 샤프 비율): Sharpe-like claim(샤프 유사 주장)이나 수익률 곡선 우수성을 말하면 적는다.
- trial count and family size(실험 횟수와 후보군 크기): selection bias(선택 편향)를 읽기 위해 적는다.

이 행동(action, 행동)의 효과(effect, 효과)는 한 구간에서만 좋아 보이는 결과를 robust alpha(견고한 알파)처럼 읽지 않게 하는 것이다.

### 6. Trade Shape(거래 형태)

거래 해석(trading interpretation, 거래 해석)을 주장하면 적는다. 거래 해석을 주장하지 않으면 `not_applicable(해당 없음)`로 적는다.

- trade count(거래 수)
- exposure(노출)
- average/median hold time(평균/중앙 보유 시간)
- win rate(승률)
- avg win/avg loss(평균 승/평균 패)
- payoff ratio(손익비)
- expectancy per trade(거래당 기대값)
- profit factor(수익 팩터)
- gross/net profit(총/순수익)
- long expectancy/short expectancy(롱 기대값/숏 기대값)
- participation vs quality delta(참여율 변화와 품질 변화 분해): 거래 수나 커버리지 증가 효과와 거래당 품질 개선 효과를 나눠 적는다.

이 행동(action, 행동)의 효과(effect, 효과)는 classification score(분류 점수)와 trading interpretation(거래 해석)을 섞지 않게 하는 것이다.

### 7. Risk And Drawdown(위험과 손실 곡선)

수익성(profitability, 수익성)이나 거래 가능성(tradability, 거래 가능성)을 말하면 적는다.

- max drawdown pct/amount(최대 손실률/금액)
- equity drawdown pct/amount(자기자본 손실률/금액)
- time under water(회복 전 체류 시간)
- longest recovery duration(최장 회복 기간)
- worst day/worst week(최악 일/최악 주)
- consecutive losses(연속 손실)
- ulcer index(울서 지수)
- tail loss or worst trade(꼬리 손실 또는 최악 거래)
- recovery_factor(회복 계수)
- min_free_margin(최소 여유 증거금)

이 행동(action, 행동)의 효과(effect, 효과)는 수익 숫자(profit number, 수익 숫자)가 큰데 위험(risk, 위험)이 감춰지는 일을 막는 것이다.

### 8. Execution Quality(실행 품질)

MT5(`MetaTrader 5`, 메타트레이더5), strategy tester(전략 테스터), live-like runtime(실거래 유사 런타임)을 근거로 말하면 적는다.

- tester model(테스터 모델)
- spread/slippage summary(스프레드/슬리피지 요약)
- fill rate(체결률)
- reject count(거부 수)
- skip rate and skip reason(스킵 비율과 이유)
- entry delay stats(진입 지연 통계)
- external mismatch count(외부 입력 불일치 수)
- data readiness failures(데이터 준비 실패)
- broker constraint events(브로커 제약 이벤트)
- ready row gap(준비 행 격차)
- top skip reasons(상위 스킵 사유)
- governance reason(거버넌스 사유)
- argmax concentration(최대 확률 집중도)
- entropy floor(엔트로피 하한)
- overlay rate(오버레이 비율)
- checksum parity(체크섬 동등성)
- decision flip rate(판정 반전 비율)
- decision flip attribution(판정 반전 원인 분해): threshold_cross(임계값 교차), margin_cross(마진 교차), feature_drift(피처 드리프트), data_hole(데이터 구멍)처럼 원인을 나눠 적는다.
- timestamp drift mean/p90/max(타임스탬프 드리프트 평균/90분위/최대)

이 행동(action, 행동)의 효과(effect, 효과)는 백테스트 논리(backtest logic, 백테스트 논리)와 실제 실행 표면(execution surface, 실행 표면)을 분리하는 것이다.

### 9. KPI Judgment Read(지표 판정 판독)

보고서(report, 보고서)는 마지막에 KPI read(지표 판독)를 짧게 적는다.

- strongest evidence(가장 강한 근거)
- weakest evidence(가장 약한 근거)
- main failure mode(주요 실패 양상)
- metric conflict(지표 충돌)
- salvage value(회수 가치)
- next measurement needed(다음 측정 필요 항목)

이 행동(action, 행동)의 효과(effect, 효과)는 많은 숫자를 나열한 뒤 무엇을 배웠는지 잃지 않게 하는 것이다.

## Judgment Boundary(판정 경계)

판정(judgment, 판정)은 다음 중 하나로 적는다.

- `positive(긍정)`: 더 비교할 가치가 있다.
- `negative(부정)`: 가설을 약화하거나 닫는 유효한 결과다.
- `inconclusive(불충분)`: 근거가 부족하다.
- `invalid(무효)`: 설정(setup, 설정), 데이터(data, 데이터), 가정(assumption, 가정)이 깨졌다.

외부 검증(external verification, 외부 검증)이 필요한 claim(주장)은 같은 작업 회차(pass, 회차)에서 좁은 충분 검증(narrow sufficient check, 좁은 충분 검증)을 시도한다. 이 행동(action, 행동)의 효과(effect, 효과)는 검증이 빠진 claim(주장)을 positive(긍정)로 닫지 않게 하는 것이다.

## Failure Memory(실패 기억)

negative(부정), inconclusive(불충분), invalid(무효) 결과는 실패 기억(failure memory, 실패 기억)을 남긴다.

필수 항목(required fields, 필수 항목):

- hypothesis(가설)
- variants tried(시도한 변형)
- failed boundary(실패 경계)
- why failed(실패 이유)
- salvage value(회수 가치)
- reopen condition(재개 조건)
- do-not-repeat note(반복 금지 메모)

이 행동(action, 행동)의 효과(effect, 효과)는 실패를 아이디어 사망(idea-dead, 아이디어 사망)으로 만들지 않고, 다음 탐색(next exploration, 다음 탐색)의 재사용 근거(reusable evidence, 재사용 근거)로 남기는 것이다.

## No-Promotion Boundary(승격 아님 경계)

alpha exploration report(알파 탐색 보고서)는 operating promotion(운영 승격) 문서가 아니다.

허용 표현(allowed wording, 허용 표현):

- scout positive(탐색 판독 긍정)
- comparison candidate(비교 후보)
- promotion_candidate(승격 후보)
- negative reusable evidence(부정 재사용 근거)

금지 표현(forbidden wording, 금지 표현):

- live ready(실거래 준비 완료)
- operating promoted(운영 승격됨)
- runtime authority expanded(런타임 권위 확장됨)
- alpha quality proven(알파 품질 증명됨)

이 경계(boundary, 경계)의 효과(effect, 효과)는 탐색을 빨리 열면서도 운영 의미(operational meaning, 운영 의미)를 과장하지 않는 것이다.
