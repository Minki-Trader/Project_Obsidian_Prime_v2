# Alpha Exploration Report Template(알파 탐색 보고서 틀)

이 틀(template, 틀)은 future alpha report(향후 알파 보고서)가 tier label(티어 라벨), split/window(분할/창), metrics(지표), judgment boundary(판정 경계), failure memory(실패 기억), no-promotion boundary(승격 아님 경계)를 빠뜨리지 않게 한다.

작성 행동(action, 행동)의 효과(effect, 효과)는 alpha exploration(알파 탐색)을 빠르게 기록하면서도 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 섞지 않게 하는 것이다.

## 1. Report Identity(보고서 정체성)

- report_id(보고서 ID): ``
- idea_id(아이디어 ID): ``
- run_id(실행 ID): ``
- stage_id(단계 ID): ``
- created_on(작성일): ``
- status(상태): `draft/reviewed/invalid(초안/검토됨/무효)`
- report lane(보고 레인): `single_split_scout/WFO/other(단일 분할 탐색 판독/워크포워드 최적화/기타)`
- scoreboard lane(점수판 레인): `structural_scout/regular_risk_execution/not_applicable(구조 탐색/정규 위험 실행/해당 없음)`
- primary KPI(`key performance indicator`, 핵심 성과 지표):
- guardrail KPI(보호 지표):
- disqualifier(탈락 조건):

## 2. Hypothesis(가설)

- hypothesis(가설):
- expected effect(기대 효과):
- tested action(시험한 행동):
- action effect(행동 효과):

## 3. Tier Label And Sample Scope(티어 라벨과 표본 범위)

| field(항목) | value(값) |
|---|---|
| tier label(티어 라벨) | `Tier A/Tier B/Tier C(티어 A/티어 B/티어 C)` |
| sample description(표본 설명) |  |
| data scope(데이터 범위) |  |
| missing context(빠진 문맥) |  |
| interpretation risk(해석 위험) |  |

Tier label(티어 라벨)은 sample label(표본 라벨)이다. exploration gate(탐색 제한문)가 아니다.

### 3.1 Tier Pair Records(티어 쌍 기록)

Stage 10(10단계) 이후 alpha exploration(알파 탐색)은 Tier A(티어 A), Tier B(티어 B), Tier A+B combined(Tier A+B 합산)를 모두 기록한다.

| record view(기록 보기) | tier scope(티어 범위) | status(상태) | path(경로) | read(판독) |
|---|---|---|---|---|
| `tier_a_separate(티어 A 분리)` | `Tier A(티어 A)` |  |  |  |
| `tier_b_separate(티어 B 분리)` | `Tier B(티어 B)` |  |  |  |
| `tier_ab_combined(티어 A+B 합산)` | `Tier A+B(티어 A+B)` |  |  |  |

기록 행동(action, 행동)의 효과(effect, 효과)는 Tier A(티어 A)만 본 판독을 전체 alpha read(알파 판독)처럼 과장하지 않고, Tier B(티어 B)와 합산 기록(combined record, 합산 기록)을 같은 실행(run, 실행) 안에서 비교하게 하는 것이다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서는 `tier_a_separate(티어 A 분리)`를 Tier A used(Tier A 사용), `tier_b_separate(티어 B 분리)`를 Tier B fallback used(Tier B 대체 사용), `tier_ab_combined(티어 A+B 합산)`를 actual routed total(실제 라우팅 전체)로 적는다.

효과(effect, 효과): combined record(합산 기록)가 separate tester run(분리 테스터 실행)의 synthetic sum(합성 합산)인지, 한 계좌 경로(account path, 계좌 경로)의 actual routed total(실제 라우팅 전체)인지 분명해진다.

## 4. Allowed Evidence Used(사용한 허용 근거)

| evidence item(근거 항목) | id/path(식별자/경로) | use(사용) | boundary(경계) |
|---|---|---|---|
| model input dataset(모델 입력 데이터셋) |  |  |  |
| label/split contract(라벨/분할 계약) |  |  |  |
| feature integrity audit(피처 무결성 감사) |  |  | not model quality(모델 품질 아님) |
| runtime parity evidence(런타임 동등성 근거) |  |  | not alpha quality(알파 품질 아님) |
| Stage 07 smoke(7단계 스모크) |  | preprocessing/training pipeline evidence(전처리/학습 파이프라인 근거) | not alpha quality(알파 품질 아님) |

Disallowed evidence check(금지 근거 확인):

- legacy winner(과거 승자): `not used(사용 안 함)`
- legacy promotion history(과거 승격 이력): `not used(사용 안 함)`
- Stage 07 smoke as alpha quality(7단계 스모크를 알파 품질로 사용): `not used(사용 안 함)`
- MT5 price-proxy as actual NDX/QQQ weights(MT5 가격 대리를 실제 NDX/QQQ 가중치로 사용): `not used(사용 안 함)`

## 5. Split/Window(분할/창)

### 5.1 Single Split Scout(단일 분할 탐색 판독)

- split_id(분할 ID): ``
- train window(학습 창): ``
- validation window(검증 창): ``
- OOS window(표본외 창): ``
- train rows(학습 행 수): ``
- validation rows(검증 행 수): ``
- OOS rows(표본외 행 수): ``
- scout boundary(탐색 판독 경계): `single split only(단일 분할만)`

### 5.2 WFO(walk-forward optimization, 워크포워드 최적화)

| window_id(창 ID) | train window(학습 창) | validation window(검증 창) | OOS window(표본외 창) | tuning rule(튜닝 규칙) | locked rule(고정 규칙) |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

WFO action(워크포워드 최적화 행동):

- window plan fixed before run(실행 전 창 계획 고정): `yes/no(예/아니오)`
- aggregate method(집계 방법):
- expected effect(기대 효과):

## 6. Method(방법)

- model family(모델 계열):
- feature set(피처 세트):
- preprocessing policy(전처리 정책):
- threshold rule(임계값 규칙):
- probability use(확률 사용):
- cost/slippage assumption(비용/슬리피지 가정):
- reproducibility notes(재현성 메모):

## 7. Metrics(지표)

### 7.0 Scoreboard And Trial Accounting(점수판과 실험 회계)

여러 후보(candidate, 후보), 파라미터(parameter, 파라미터), 창(window, 창)을 비교했다면 반드시 채운다.

| field(항목) | value(값) |
|---|---|
| scoreboard lane(점수판 레인) | `structural_scout/regular_risk_execution(구조 탐색/정규 위험 실행)` |
| run count(실행 수) |  |
| trial count(실험 횟수) |  |
| completed trial count(완료 실험 수) |  |
| failed trial count(실패 실험 수) |  |
| failed reason summary(실패 사유 요약) |  |
| candidate family count(후보 계열 수) |  |
| parameter grid/range(파라미터 격자/범위) |  |
| selected rank(선택 순위) |  |
| search breadth note(탐색 폭 메모) |  |

| KPI role(지표 역할) | metric(지표) | pass/fail read(통과/실패 판독) | note(메모) |
|---|---|---|---|
| primary KPI(핵심 성과 지표) |  |  |  |
| guardrail KPI(보호 지표) |  |  |  |
| disqualifier(탈락 조건) |  |  |  |

효과(effect, 효과): 가장 좋아 보이는 한 결과가 search breadth(탐색 폭), failed trials(실패 실험), selection bias(선택 편향)를 숨기지 못하게 한다.

### 7.0.1 Tier-Paired KPI(티어 쌍 KPI)

| record view(기록 보기) | KPI scope(KPI 범위) | primary KPI(핵심 성과 지표) | guardrail KPI(보호 지표) | judgment read(판정 판독) |
|---|---|---|---|---|
| `tier_a_separate(티어 A 분리)` |  |  |  |  |
| `tier_b_separate(티어 B 분리)` |  |  |  |  |
| `tier_ab_combined(티어 A+B 합산)` |  |  |  |  |

효과(effect, 효과): KPI(`key performance indicator`, 핵심 성과 지표)가 좋은 한 티어(tier, 티어)만 골라 보이는 일을 막고, 분리 기록(separate record, 분리 기록)과 합산 기록(combined record, 합산 기록)의 차이를 남긴다.

Routed run(라우팅 실행)의 component row(구성 행)가 per-tier PnL(티어별 손익)을 직접 추적하지 못하면, 그 행은 수익(profit, 수익)을 주장하지 않고 route count(경로 수), signal count(신호 수), fill/reject/skip(체결/거부/스킵)만 적는다. 수익·위험 KPI(핵심 성과 지표)는 actual routed total(실제 라우팅 전체)에 적는다.

### 7.1 Identity And Coverage(정체성과 커버리지)

| field(항목) | value(값) |
|---|---|
| dataset id(데이터셋 ID) |  |
| label id(라벨 ID) |  |
| split id(분할 ID) |  |
| feature count(피처 수) |  |
| feature order hash(피처 순서 해시) |  |
| missing/invalid rows(누락/무효 행 수) |  |
| prediction coverage(예측 커버리지) |  |
| no-prediction/no-trade rate(무예측/무거래 비율) |  |

효과(effect, 효과): 다른 입력 표면(input surface, 입력 표면)을 같은 결과처럼 비교하지 않는다.

### 7.2 Signal Quality(신호 품질)

| split/window(분할/창) | rows(행 수) | class balance(클래스 균형) | accuracy(정확도) | balanced accuracy(균형 정확도) | macro F1(매크로 F1) | per-class precision/recall/F1(클래스별 정밀도/재현율/F1) | directional hit rate(방향 적중률) |
|---|---:|---|---:|---:|---:|---|---:|
| train(학습) |  |  |  |  |  |  |  |
| validation(검증) |  |  |  |  |  |  |  |
| OOS(표본외) |  |  |  |  |  |  |  |

- confusion matrix(혼동 행렬):
- baseline comparison(기준선 비교):
- lift by confidence bucket(확신도 구간별 리프트):

### 7.3 Probability Quality(확률 품질)

확률(probability, 확률)을 쓰지 않으면 `not_applicable(해당 없음)`로 적는다.

| split/window(분할/창) | log loss(로그 손실) | Brier score(브라이어 점수) | ECE(기대 보정 오차) | confidence distribution(확신도 분포) | entropy/margin(엔트로피/확률 차이) | row-sum check(행 합 검사) |
|---|---:|---:|---:|---|---|---|
| train(학습) |  |  |  |  |  |  |
| validation(검증) |  |  |  |  |  |  |
| OOS(표본외) |  |  |  |  |  |  |

- calibration by probability bucket(확률 구간별 보정):

### 7.4 Threshold And Decision Shape(임계값과 판정 형태)

| threshold id(임계값 ID) | decision threshold(판정 임계값) | signal count by class(클래스별 신호 수) | precision/coverage read(정밀도/커버리지 판독) | no-trade rate(무거래 비율) | turnover estimate(회전율 추정) | long/short mix(롱/숏 비율) |
|---|---|---|---|---:|---:|---|
|  |  |  |  |  |  |  |

- threshold sweep(임계값 스윕):

| rule/context item(규칙/문맥 항목) | pass/hit rate(통과/적중률) | rows/trades affected(영향 행/거래 수) | interpretation(해석) |
|---|---:|---:|---|
| rule_pass_rate(규칙 통과율) |  |  |  |
| context hit-rate(문맥 적중률) |  |  |  |

효과(effect, 효과): 필터(filter, 필터)가 표본을 줄여서 만든 착시와 실제 문맥 우위(context edge, 문맥 우위)를 나눠 본다.

### 7.5 Stability And Slice Quality(안정성과 조각 품질)

positive(긍정)나 promotion_candidate(승격 후보)로 말하려면 채운다.

| slice type(조각 유형) | slice id(조각 ID) | metric read(지표 판독) | degradation/gap(악화/격차) | interpretation(해석) |
|---|---|---|---|---|
| month/quarter(월/분기) |  |  |  |  |
| session/time-of-day(세션/시간대) |  |  |  |  |
| volatility regime(변동성 국면) |  |  |  |  |
| long vs short(롱/숏) |  |  |  |  |
| WFO window(WFO 창) |  |  |  |  |

- train/validation/OOS gap(학습/검증/표본외 격차):
- parameter neighborhood robustness(파라미터 주변 견고성):
- parameter cliff/plateau read(파라미터 절벽/평탄 구간 판독):
- bridge non-regression(브리지 비퇴행):

### 7.6 Overfit And Multiple Testing Controls(과최적화와 다중 검정 통제)

여러 trial(실험) 중 좋은 결과를 골랐다면 채운다. 계산할 수 없으면 `not_calculated(계산 안 됨)`와 이유를 적는다.

| field(항목) | value(값) |
|---|---|
| PBO(`Probability of Backtest Overfitting`, 백테스트 과최적화 확률) |  |
| PBO method(백테스트 과최적화 확률 산식/방법) |  |
| DSR(`Deflated Sharpe Ratio`, 보정 샤프 비율) |  |
| Sharpe-like metric used(샤프 유사 지표) |  |
| trial count used for deflation(보정에 쓴 실험 횟수) |  |
| multiple testing adjustment(다중 검정 보정) |  |
| performance degradation IS/OOS(표본내/표본외 성과 악화) |  |
| probability of loss OOS(표본외 손실 확률) |  |
| stochastic dominance read(확률 지배 판독) |  |
| parameter neighborhood robustness(파라미터 주변 견고성) |  |
| parameter cliff/plateau read(파라미터 절벽/평탄 구간 판독) |  |

효과(effect, 효과): 여러 번 시도한 뒤 제일 좋은 결과만 보고 alpha strength(알파 강도)를 과대평가하지 않는다.

### 7.7 Trade Shape Metrics(거래 형태 지표)

거래 해석(trading interpretation, 거래 해석)을 주장하지 않으면 `not_applicable(해당 없음)`로 적는다.

| split/window(분할/창) | trade count(거래 수) | exposure(노출) | avg/median hold(평균/중앙 보유) | win rate(승률) | avg win/loss(평균 승/패) | payoff ratio(손익비) | expectancy/trade(거래당 기대값) | profit factor(수익 팩터) | gross/net profit(총/순수익) |
|---|---:|---:|---|---:|---|---:|---:|---:|---|
| train(학습) |  |  |  |  |  |  |  |  |  |
| validation(검증) |  |  |  |  |  |  |  |  |  |
| OOS(표본외) |  |  |  |  |  |  |  |  |  |

- long expectancy/short expectancy(롱 기대값/숏 기대값):
- MFE/MAE summary(최대 유리/불리 이동 요약):
- participation vs quality delta(참여율 변화와 품질 변화 분해):

| comparison(비교) | participation delta(참여율 변화) | quality delta(품질 변화) | read(판독) |
|---|---:|---:|---|
| candidate vs baseline(후보 대 기준선) |  |  |  |

### 7.8 Risk And Drawdown(위험과 손실 곡선)

수익성(profitability, 수익성)이나 거래 가능성(tradability, 거래 가능성)을 말하지 않으면 `not_applicable(해당 없음)`로 적는다.

| split/window(분할/창) | max DD pct/amount(최대 손실률/금액) | equity DD pct/amount(자기자본 손실률/금액) | time under water(회복 전 체류 시간) | longest recovery(최장 회복) | worst day/week(최악 일/주) | consecutive losses(연속 손실) | ulcer index(울서 지수) | tail loss/worst trade(꼬리 손실/최악 거래) |
|---|---|---|---|---|---|---:|---:|---|
| train(학습) |  |  |  |  |  |  |  |  |
| validation(검증) |  |  |  |  |  |  |  |  |
| OOS(표본외) |  |  |  |  |  |  |  |  |

- recovery_factor(회복 계수):
- min_free_margin(최소 여유 증거금):

### 7.9 Execution Quality(실행 품질)

MT5(`MetaTrader 5`, 메타트레이더5), strategy tester(전략 테스터), live-like runtime(실거래 유사 런타임)을 말하지 않으면 `not_applicable(해당 없음)`로 적는다.

| field(항목) | value(값) |
|---|---|
| tester model(테스터 모델) |  |
| spread/slippage summary(스프레드/슬리피지 요약) |  |
| fill rate(체결률) |  |
| reject count(거부 수) |  |
| skip rate/reasons(스킵 비율/이유) |  |
| entry delay stats(진입 지연 통계) |  |
| external mismatch count(외부 입력 불일치 수) |  |
| data readiness failures(데이터 준비 실패) |  |
| broker constraint events(브로커 제약 이벤트) |  |
| ready row gap(준비 행 격차) |  |
| external skip mean/latest(외부 스킵 평균/최신) |  |
| argmax mean/p90(최대 확률 집중도 평균/90분위) |  |
| entropy mean/p10(엔트로피 평균/10분위) |  |
| overlay mean/latest(오버레이 평균/최신) |  |
| top skip reasons(상위 스킵 사유) |  |
| governance reason(거버넌스 사유) |  |

### 7.10 Parity And Runtime Drift(동등성과 런타임 드리프트)

Python/MT5(파이썬/메타트레이더5) 또는 runtime handoff(런타임 인계)를 말하지 않으면 `not_applicable(해당 없음)`로 적는다.

| field(항목) | value(값) |
|---|---|
| exact timestamp drift mean/p90/max(정확 타임스탬프 드리프트 평균/90분위/최대) |  |
| best-neighbor drift mean/p90/max(최인접 드리프트 평균/90분위/최대) |  |
| zero-shift share(무이동 비율) |  |
| checksum parity(체크섬 동등성) |  |
| decision flip count/rate(판정 반전 수/비율) |  |
| decision flip attribution(판정 반전 원인 분해) |  |
| high-diff cluster read(고차이 군집 판독) |  |
| session concentration(세션 집중) |  |

### 7.11 Event Attribution And Bridge Read(이벤트 기여와 연결 판독)

특정 이벤트(event, 이벤트), 보호 장치(protection, 보호 장치), 브리지(bridge, 연결)를 주장하지 않으면 `not_applicable(해당 없음)`로 적는다.

| field(항목) | value(값) |
|---|---|
| direct event count(직접 이벤트 수) |  |
| direct event net/share(직접 이벤트 순효과/비중) |  |
| trigger reason breakdown(트리거 사유 분해) |  |
| session/ATR bucket breakdown(세션/ATR 구간 분해) |  |
| baseline comparison(기준선 비교) |  |
| return/PF/DD delta(수익률/수익 팩터/손실 곡선 차이) |  |
| continuous bridge read(연속 연결 판독) |  |
| bridge non-regression(브리지 비퇴행) |  |

### 7.12 KPI Judgment Read(지표 판정 판독)

- strongest evidence(가장 강한 근거):
- weakest evidence(가장 약한 근거):
- main failure mode(주요 실패 양상):
- metric conflict(지표 충돌):
- instability note(불안정성 메모):
- salvage value(회수 가치):
- next measurement needed(다음 측정 필요 항목):
- comparison baseline(비교 기준):

## 8. Judgment Boundary(판정 경계)

- judgment(판정): `positive/negative/inconclusive/invalid(긍정/부정/불충분/무효)`
- boundary vocabulary(경계 어휘): `single_split_scout/comparison_candidate/promotion_candidate/runtime_probe(단일 분할 탐색 판독/비교 후보/승격 후보/런타임 탐침)`
- evidence basis(근거 기준):
- missing evidence(빠진 근거):
- external verification status(외부 검증 상태): `not_applicable/completed/blocked/out_of_scope_by_claim(해당 없음/완료/차단/주장 범위 밖)`
- lowered claim if needed(필요 시 낮춘 주장):

판정 행동(action, 행동)의 효과(effect, 효과)는 결과를 쓸 수 있는 범위(scope, 범위)를 분명히 해서, positive(긍정)와 operating promotion(운영 승격)을 섞지 않게 하는 것이다.

## 9. Tier A/B Reporting Read(티어 A/B 보고 판독)

- project alpha run ledger(프로젝트 알파 실행 장부): `docs/registers/alpha_run_ledger.csv`
- stage run ledger(단계 실행 장부): `stages/<stage_id>/03_reviews/stage_run_ledger.csv`
- Tier A separate read(티어 A 분리 판독):
- Tier B separate read(티어 B 분리 판독):
- Tier A+B combined read(티어 A+B 합산 판독):
- routed interpretation if applicable(해당 시 라우팅 해석): `Tier A primary + Tier B fallback / actual routed total(Tier A 우선 + Tier B 대체 / 실제 라우팅 전체)`
- compare allowed(비교 허용): `yes/no(예/아니오)`
- compare boundary(비교 경계):
- sample-label warning(표본 라벨 경고): Tier label(티어 라벨)은 exploration gate(탐색 제한문)가 아니다.
- incomplete record action(미완성 기록 행동): `blocked_tier_pair_incomplete/inconclusive_tier_pair_incomplete/out_of_scope_by_claim/not_applicable(티어 쌍 미완료 차단/티어 쌍 미완료 불충분/주장 범위 밖/해당 없음)`

## 10. Failure Memory(실패 기억)

negative(부정), inconclusive(불충분), invalid(무효) 결과이면 반드시 채운다.

- hypothesis(가설):
- variants tried(시도한 변형):
- failed boundary(실패 경계):
- why failed(실패 이유):
- salvage value(회수 가치):
- reopen condition(재개 조건):
- do-not-repeat note(반복 금지 메모):
- negative result register action(부정 결과 등록부 행동): `none/propose_register_entry(없음/등록 제안)`
- action effect(행동 효과):

## 11. No-Promotion Boundary(승격 아님 경계)

이 보고서(report, 보고서)는 alpha exploration report(알파 탐색 보고서)다.

- operating promotion claimed(운영 승격 주장): `no(아니오)`
- live readiness claimed(실거래 준비 주장): `no(아니오)`
- runtime authority expanded(런타임 권위 확장): `no(아니오)`
- alpha quality proven(알파 품질 증명): `no(아니오)`

경계 효과(boundary effect, 경계 효과): 탐색 결과(exploration result, 탐색 결과)를 운영 의미(operational meaning, 운영 의미)로 과장하지 않는다.

## 12. Attachments And Follow-up(첨부와 후속 작업)

- run manifest(실행 목록):
- output path(출력 경로):
- model artifact manifest(모델 산출물 목록):
- charts/tables(차트/표):
- registry update needed(등록부 갱신 필요):
- next action(다음 행동):
- next action effect(다음 행동 효과):
