# Negative Result Register

| result_id | idea_id | hypothesis | why_failed | salvage_value | reopen_condition |
|---|---|---|---|---|---|
| `NR-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT` | `IDEA-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT` | four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색)가 같은 직접 로지스틱 ONNX(온엑스) 표면 계열 안에서 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 함께 고칠 수 있다 | frontier02E(전선02E) go_rule_rows(진행 규칙 행)가 `0`이고 OOS PF/DD(표본외 수익 팩터/손실폭)가 `1.05433` / `10.3356%`라 네 축 동시 목표에 부족했다 | frontier02C(전선02C) seed surface(씨앗 표면) `frontier02c_logreg_teacher__trend_follow_joint__mid_cash__both__q70__cd6__p34__m0__cd6`와 proxy->teacher->ONNX->decision replay(프록시-교사-온엑스-결정 재생) 측정 사슬을 보존한다 | new source/label/model family/regime split/runtime representation(새 원천/라벨/모델군/레짐 분할/런타임 표현)이 있을 때만 재개 |
| `NR-001` | `time_semantics_direct_utc` | 원천 `time_open_unix`를 직접 UTC(direct UTC, 직접 협정세계시)로 보고 미국 정규장 피처(US cash-session features, 미국 정규장 피처)를 계산할 수 있다 | `20260424_time_semantics_probe`에서 직접 UTC 일치율(direct UTC match ratio, 직접 UTC 일치율)이 `0.0`이었다 | 원천 timestamp(타임스탬프)는 브로커 시계 정렬 키(broker-clock alignment key, 브로커 시계 정렬 키)로는 쓸 수 있다 | 새 export(내보내기) 또는 브로커 문서(broker documentation, 브로커 문서)가 UTC 의미를 명확히 증명할 때 |
| `NR-002` | `IDEA-ST11-LGBM-DIRECTION-SHORT-ONLY` | LGBM(`LightGBM`, 라이트GBM) short-only(숏만) 방향 분리가 RUN02A/RUN02B(실행 02A/02B)의 약함을 회복할 수 있다 | RUN02D(실행 02D) OOS(표본외) net/PF(순수익/수익 팩터)가 `-211.48 / 0.31`로 크게 약했다 | validation(검증)은 `-18.33 / 0.89`라서 short-specific label(숏 전용 라벨)의 필요성을 알려준다 | 새 short-specific label(숏 전용 라벨) 또는 short-side model(숏 전용 모델)이 생길 때 |
| `NR-003` | `IDEA-ST11-LGBM-CALM-TREND-GATE` | `adx_14 >= 25`와 `historical_vol_5_over_20 <= 1.25` calm trend gate(차분한 추세 문맥 제한)가 LGBM(라이트GBM) 신호를 정화할 수 있다 | RUN02F(실행 02F) validation/OOS(검증/표본외) net/PF(순수익/수익 팩터)가 `-234.03 / 0.46`, `-163.22 / 0.41`로 둘 다 약했다 | context gating(문맥 제한)은 필요할 수 있지만 이 조건 조합은 약하다 | 다른 context feature(문맥 피처) 조합이나 regime label(국면 라벨)이 생길 때 |
| `NR-004` | `IDEA-ST11-LGBM-LOW-VOL-EXTREME-CONFIDENCE` | low volatility(저변동성) 문맥과 extreme confidence(극단 확신)를 결합하면 RUN02E(실행 02E)의 손실이 줄 수 있다 | RUN02I(실행 02I) validation/OOS(검증/표본외) net/PF(순수익/수익 팩터)가 `-509.12 / 0.00`, `-231.42 / 0.00`이었다 | low volatility(저변동성) 필터만으로는 LGBM(라이트GBM) 극단 확신을 살리지 못한다 | 새 calibration(보정) 또는 다른 volatility regime(변동성 국면) 라벨이 있을 때 |
| `NR-005` | `IDEA-ST11-LGBM-QUIET-RETURN-ZSCORE` | quiet return z-score(조용한 수익률 z점수) 문맥에서 LGBM(라이트GBM) 확률 순위가 안정될 수 있다 | RUN02K(실행 02K) validation/OOS(검증/표본외) net/PF(순수익/수익 팩터)가 `-496.54 / 0.02`, `-494.23 / 0.19`로 둘 다 크게 약했다 | 조용한 즉시 수익률 조건은 손실 구조를 줄이지 못했다 | 다른 mean-reversion label(평균회귀 라벨)이 생길 때 |
| `NR-006` | `IDEA-ST11-LGBM-RANGE-COMPRESSION` | DI spread/ADX(DI 차이/ADX) 압축 문맥에서 LGBM(라이트GBM)이 추격 손상을 피할 수 있다 | RUN02L(실행 02L) validation/OOS(검증/표본외) net/PF(순수익/수익 팩터)가 `-352.49 / 0.34`, `-250.36 / 0.05`였다 | range compression(횡보 압축) 조건은 현재 LGBM(라이트GBM) 확률을 정화하지 못했다 | 압축 후 breakout label(돌파 라벨)이 생길 때 |
| `NR-007` | `IDEA-ST11-LGBM-HIGH-VOL-MOMENTUM-ALIGN` | high-vol momentum alignment(고변동성 모멘텀 정렬)가 있어야 LGBM(라이트GBM)이 살아날 수 있다 | RUN02M(실행 02M) validation/OOS(검증/표본외) net/PF(순수익/수익 팩터)가 `-496.38 / 0.25`, `-305.93 / 0.31`이었다 | 변동성 확장과 모멘텀 정렬만으로는 손실을 줄이지 못했다 | 새 momentum-specific model(모멘텀 전용 모델)이나 label(라벨)이 있을 때 |
| `NR-008` | `IDEA-ST11-LGBM-BULL-TREND-LONG` | bullish trend confirmation(상승 추세 확인)이 long-only(롱만) LGBM(라이트GBM)을 살릴 수 있다 | RUN02H(실행 02H) OOS(표본외)는 `11.52 / 1.21`로 작게 양수였지만 validation(검증)이 `-210.68 / 0.19`로 약했다 | bullish trend(상승 추세) 필터는 RUN02G(실행 02G)보다 회수 가치가 작다 | long pullback(롱 되돌림)과 결합하거나 새 추세 라벨이 있을 때 |
| `NR-009` | `IDEA-ST11-LGBM-BULL-VORTEX-LONG` | bullish vortex(상승 보텍스) 문맥이 long-only(롱만) 회수 가치를 집중시킬 수 있다 | RUN02O(실행 02O) OOS(표본외)는 `6.04 / 1.20`로 작게 양수였지만 validation(검증)이 `-86.88 / 0.55`였다 | 단독 bullish vortex(상승 보텍스) 조건은 회수 가치가 작다 | RUN02G(실행 02G) pullback(되돌림) 조건과 결합할 때 |
| `NR-010` | `IDEA-ST11-LGBM-BEAR-VORTEX-SHORT-DENSITY` | RUN02P(실행 02P)의 작은 dual-positive(양쪽 양수) 판독은 looser bearish vortex short density(느슨한 하락 보텍스 숏 밀도)로 커질 수 있다 | RUN02Q(실행 02Q) validation/OOS(검증/표본외) net/PF(순수익/수익 팩터)가 `-139.28 / 0.62`, `-140.58 / 0.54`로 둘 다 약했다 | bear-vortex short(하락 보텍스 숏)을 느슨하게 넓히면 거래 수는 늘지만 품질이 무너진다 | short-specific label(숏 전용 라벨) 또는 short-side model(숏 전용 모델)이 생길 때 |
| `NR-011` | `IDEA-ST11-LGBM-LONG-PULLBACK-ADX-REPAIR` | RUN02G(실행 02G)의 OOS(표본외) 회수 가치는 deeper pullback plus ADX gate(더 깊은 되돌림과 ADX 제한)로 validation(검증)을 복구할 수 있다 | RUN02R(실행 02R) validation(검증)은 `275.78 / 2.44`로 좋았지만 OOS(표본외)가 `-82.01 / 0.74`로 실패했다 | validation-only repair(검증만 복구)라서 regime sensitivity(국면 민감도)를 보여준다 | WFO(워크포워드 최적화) 또는 새 pullback label(되돌림 라벨)이 생길 때 |
| `NR-012` | `IDEA-ST11-WFO-LITE-PRIORITY` | RUN02S(실행 02S)를 현재 표면 그대로 full WFO(전체 워크포워드 최적화)에 올릴 수 있다 | RUN02U(실행 02U)에서 OOS(표본외) 신호가 `10`개뿐이라 window(구간)별 학습/검증 판단이 너무 얇다 | WFO(워크포워드 최적화)는 버리지 않지만, 현재 RUN02S(실행 02S) 표면 그대로는 우선순위가 낮다 | fwd18 retraining probe(fwd18 재학습 탐침)나 더 조밀한 surface(표면)가 생길 때 |
| `NR-013` | `IDEA-ST11-LABEL-HORIZON-FWD18-RETRAIN` | fwd18-only retrain(fwd18 단독 재학습)과 RUN01Y(실행 01Y) 200~220 threshold(임계값) 구조가 LGBM(`LightGBM`, 라이트GBM)을 MT5(`MetaTrader 5`, 메타트레이더5)에서 회복할 수 있다 | RUN02W(실행 02W) routed validation/OOS(라우팅 검증/표본외) net/PF(순수익/수익 팩터)가 `-496.25 / 0.28`, `-216.12 / 0.67`로 둘 다 약했다 | fwd18 label horizon(90분 라벨 예측수평선)은 단독 반복보다 context gate/rank threshold(문맥 제한/순위 임계값)와 결합할 때만 다시 볼 가치가 있다 | fwd18(90분)과 context gate/rank threshold(문맥 제한/순위 임계값)를 결합한 새 표면이 생길 때 |
| `NR-014` | `IDEA-ST11-LABEL-HORIZON-FWD18-RANK-DIRECT` | fwd18(90분) LGBM(`LightGBM`, 라이트GBM) 고순위 확률 신호를 direct decision(직접 판정)으로 쓰면 RUN02W(실행 02W)를 회복할 수 있다 | RUN02X(실행 02X) Tier A q96 validation/OOS hit rate(Tier A q96 검증/표본외 적중률)가 `0.25 / 0.15625`로 약했다 | fwd18(90분) rank signal(순위 신호)은 direct(직접)보다 inverse/context(역방향/문맥)와 결합할 때만 다시 볼 가치가 있다 | inverse decision(역방향 판정)과 context gate(문맥 제한)를 결합한 표면이 생길 때 |
| `NR-015` | `IDEA-ST11-LABEL-HORIZON-FWD18-INVERSE-RANK-CONTEXT-STRESS` | RUN02Z(실행 02Z)의 문맥을 `ADX<=20`으로 더 좁히면 품질이 더 좋아질 수 있다 | RUN02AA(실행 02AA)는 validation(검증) `480.75 / 446.14`였지만 OOS(표본외)가 `31.62 / 2.80 / 2 trades(거래)`로 너무 얇았다 | 너무 좁은 ADX cutoff(ADX 절단값)는 validation-heavy(검증 치우침)를 만든다 | 다른 rank quantile/margin(순위 분위수/마진)에서 OOS(표본외) 거래 수가 늘 때 |
| `NR-016` | `IDEA-ST11-LABEL-HORIZON-FWD18-INVERSE-RANK-CONTEXT-STRESS` | Tier B fallback(Tier B 대체)을 끄면 RUN02Z(실행 02Z)의 OOS(표본외) 품질이 더 좋아질 수 있다 | RUN02AD/RUN02AE(실행 02AD/02AE)는 OOS(표본외)가 양수였지만 거래가 `2`개뿐이고, routed(라우팅)보다 순수익과 밀도가 낮았다 | Tier B fallback(티어 B 대체)은 현재 중심 표면에서 OOS(표본외) 밀도와 순수익을 보탠다 | Tier B fallback(티어 B 대체) 구성 손익이 반복적으로 음수로 바뀔 때 |

Negative results are preserved because they prevent repeated dead ends.
| `NR-017` | `IDEA-ST12-ET-BATCH20-V20` | ExtraTrees(엑스트라트리스) fwd12(12봉 전방) 확률 방향을 inverse(역방향)로 쓰면 구조적 역방향성이 드러날 수 있다 | `run03G_et_variant_stability_probe_v1`에서 validation hit(검증 적중)는 높지만 OOS hit(표본외 적중)가 약해 inverse-only(역방향 단독)는 실패 경계로 남겼다 | inverse(역방향)는 단독 반복하지 말고 context gate(문맥 제한)나 다른 label horizon(라벨 수평선)과 결합할 때만 회수한다 | inverse+context(역방향+문맥) 또는 다른 horizon(수평선)에서 OOS 월별 안정성이 회복될 때 |
| `NR-019` | `IDEA-ST12-ET-SESSION-AGE-REGIME` | session age(세션 경과 시간)만으로 ExtraTrees(엑스트라 트리) 신호가 안정될 수 있다 | RUN03M(실행 03M) best bucket(최상위 구간)도 both-positive fold(양쪽 양수 접힘)가 `0`라 반복성이 약했다 | session bucket(세션 구간)은 보조 설명 축으로 남긴다 | 특정 bucket(구간)이 다른 label/model(라벨/모델)에서 반복될 때 |
| `NR-020` | `IDEA-ST12-ET-VOLATILITY-REGIME` | volatility regime(변동성 국면)만으로 ExtraTrees(엑스트라 트리) 신호가 안정될 수 있다 | RUN03N(실행 03N) best bucket(최상위 구간)의 both-positive fold(양쪽 양수 접힘)는 `0`다 | volatility bucket(변동성 구간)은 보조 설명 축으로 남긴다 | 특정 bucket(구간)이 다른 label/model(라벨/모델)에서 반복될 때 |
| `NR-021` | `IDEA-ST12-ET-TREND-CHOP-REGIME` | trend/chop regime(추세/횡보 국면)만으로 ExtraTrees(엑스트라 트리) 신호가 안정될 수 있다 | RUN03O(실행 03O) best bucket(최상위 구간)의 both-positive fold(양쪽 양수 접힘)는 `0`다 | trend/chop bucket(추세/횡보 구간)은 보조 설명 축으로 남긴다 | 특정 bucket(구간)이 다른 label/model(라벨/모델)에서 반복될 때 |
| `NR-022` | `IDEA-ST12-ET-MEGA-CAP-DIVERGENCE` | mega-cap divergence regime(대형주 괴리 국면)만으로 ExtraTrees(엑스트라 트리) 신호가 안정될 수 있다 | RUN03P(실행 03P) best bucket(최상위 구간)의 both-positive fold(양쪽 양수 접힘)는 `0`다 | mega-cap divergence bucket(대형주 괴리 구간)은 보조 설명 축으로 남긴다 | 특정 bucket(구간)이 다른 label/model(라벨/모델)에서 반복될 때 |
| `NR-023` | `IDEA-ST12-ET-MACRO-PROXY-REGIME` | macro proxy regime regime(거시 대리 국면 국면)만으로 ExtraTrees(엑스트라 트리) 신호가 안정될 수 있다 | RUN03Q(실행 03Q) best bucket(최상위 구간)의 both-positive fold(양쪽 양수 접힘)는 `0`다 | macro proxy regime bucket(거시 대리 국면 구간)은 보조 설명 축으로 남긴다 | 특정 bucket(구간)이 다른 label/model(라벨/모델)에서 반복될 때 |
| `NR-024` | `IDEA-ST12-ET-GAP-OVERNIGHT-CONTEXT` | gap/overnight context regime(갭/야간 문맥 국면)만으로 ExtraTrees(엑스트라 트리) 신호가 안정될 수 있다 | RUN03R(실행 03R) best bucket(최상위 구간)의 both-positive fold(양쪽 양수 접힘)는 `0`다 | gap/overnight context bucket(갭/야간 문맥 구간)은 보조 설명 축으로 남긴다 | 특정 bucket(구간)이 다른 label/model(라벨/모델)에서 반복될 때 |
| `NR-025` | `IDEA-ST12-ET-PROBABILITY-SHAPE-ATTRIBUTION` | probability-shape attribution regime(확률 모양 귀속 국면)만으로 ExtraTrees(엑스트라 트리) 신호가 안정될 수 있다 | RUN03S(실행 03S) best bucket(최상위 구간)의 both-positive fold(양쪽 양수 접힘)는 `0`다 | probability-shape attribution bucket(확률 모양 귀속 구간)은 보조 설명 축으로 남긴다 | 특정 bucket(구간)이 다른 label/model(라벨/모델)에서 반복될 때 |
| `NR-026` | `IDEA-ST16-QDA-CLASS-COVARIANCE` | QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) full58(전체 58개 피처) reg0.18(정규화 0.18) 주변과 drop_mega10(대형주 10개 제거) 변형을 single split(단일 분할)에서 더 미세 조정하면 안정 edge(거래 우위)가 생길 수 있다 | Stage16(16단계) run10(실행10)에서 best OOS(최고 표본외) `run10B`는 validation(검증)이 음수였고, strong survivor(강한 생존 표면)는 `run10I` 하나뿐이었다 | QDA(이차 판별 분석) class-specific covariance(클래스별 공분산)는 보존 단서로 남기되 같은 reg/coverage(정규화/커버리지) 미세 반복은 멈춘다 | 새 label/horizon(라벨/예측수평선), WFO(`walk-forward optimization`, 워크포워드 최적화), 또는 다른 model/context(모델/문맥)에서 인접 설정 두 개 이상이 validation/OOS(검증/표본외) 동시 생존할 때 |
| `NR-027` | `IDEA-ST40-CANDLE-MORPHOLOGY-SIGNAL-QUALITY` | candle morphology(캔들 형태)를 closed US100 M5 OHLC(확정 US100 5분봉 시가/고가/저가/종가)에서 새로 계산하면 signal quality(신호 품질)를 안정적으로 분리할 수 있다 | Stage40(40단계) run34A(실행34A) MT5(`MetaTrader 5`, 메타트레이더5) broad sweep(넓은 훑기)에서 best validation(최고 검증) `c07_rejection_tail_directional`은 validation(검증) net/PF(순수익/수익 팩터) `29.36/1.07`이나 OOS(표본외) `-113.55/0.67`로 실패했고, best OOS(최고 표본외) `c15_morphology_score_low_complexity`는 OOS(표본외) `195.55/1.10`이나 validation(검증) `-142.46/0.95`로 실패했다 | outside/rejection(외부봉/꼬리 반전) 조합 `c13`은 양쪽 양수였지만 thin trade count(얇은 거래 수)라 seed clue(씨앗 단서)로만 보존한다. wide_range_doji(넓은 범위 도지) negative control(음성 대조군)은 약하고 얇았다 | 새 label/horizon(라벨/예측수평선) 또는 별도 candle-specific model(캔들 전용 모델)에서 validation/OOS(검증/표본외) 양쪽 PF(`profit factor`, 수익 팩터)와 거래 수가 동시에 살아날 때 |
| `NR-028` | `IDEA-ST95-V41-OOS-EARLY-ENTRY-GATE` | Stage93 best(93단계 최선안)의 OOS early flatline risk(표본외 초반 평탄화 위험)는 entry gate/confidence threshold(진입 게이트/신뢰도 문턱)를 조이면 고쳐질 수 있다 | Stage95/Stage96(95/96단계)에서 Gate09/Gate10(게이트09/게이트10)은 OOS early(표본외 초반)를 `-20.13 / PF 0.925`, `-5.25 / PF 0.977`로 악화했고, Thr056(문턱 0.56)은 Stage93 best(93단계 최선안)를 보존했지만 `13.02 / PF 1.046` 약점을 고치지 못했다 | Entry gate(진입 게이트)는 현재 축에서 더 조이지 않는다. 보존 가치는 Stage93 best(93단계 최선안)의 full split(전체 분할) 균형과 Stage95의 실패 기억이다 | lifecycle/hold/re-entry(생명주기/보유/재진입) 또는 side/session attribution(방향/세션 귀속)에서 OOS early(표본외 초반) 약점 원인이 분리될 때 |
| `NR-029` | `IDEA-ST97-V41-OOS-EARLY-LIFECYCLE` | Stage93 best(93단계 최선안)의 OOS early flatline risk(표본외 초반 평탄화 위험)는 max_hold_bars(최대 보유 봉수) 또는 same-direction cooldown(동방향 쿨다운)만 바꾸면 고쳐질 수 있다 | Stage97(97단계)에서 H2(2봉 보유)는 validation(검증)을 `213.26 / PF 1.22`로 훼손했고, H4(4봉 보유)는 OOS early(표본외 초반) `-6.53 / PF 0.980`과 OOS DD(표본외 손실률) `26.49%`를 만들었고, CD8(8봉 쿨다운)은 validation(검증)은 강했지만 OOS(표본외) `495.51 / PF 1.44`와 OOS early(표본외 초반) `-1.95 / PF 0.994`로 약했다 | H2는 OOS early(표본외 초반) 작은 개선 단서, CD8은 validation density(검증 밀도) 단서로만 보존한다 | Stage98(98단계) 검토 뒤 side/session/market context(방향/세션/시장 문맥) 또는 separate branch(별도 분기)가 OOS early(표본외 초반)를 validation 훼손 없이 분리할 때 |
| `NR-030` | `IDEA-ST135-STAGE122-SURVIVOR-AUDIT` | Stage122 survivor(Stage122 생존 후보)는 34D(레거시 기준) 이상 KPI(핵심 성과 지표)에 바로 도달할 수 있다 | Stage135(135단계)에서 PF/net(수익 팩터/순손익)은 강했지만 validation late concentration(검증 후반 집중), OOS drawdown(외부 표본 손실폭), trade count gap(거래 수 격차)이 남았다 | 후보는 보존하고 Stage136(136단계)에서 trade count/concentration(거래 수/집중)만 좁게 수리한다 | 거래 수가 늘고 집중이 낮아져도 validation/OOS PF/net(검증/외부 표본 수익 팩터/순손익)과 risk/ATR(위험/ATR)이 유지될 때 |
| `NR-031` | `IDEA-ST267-PROXY-ABLATION-CANDIDATE-DISTINGUISHABILITY` | proxy score ablation/replacement(대체 점수 제거/대체) 변형이 다섯 Baseline candidates(기준 후보)를 구분할 수 있다 | run267T(267T 실행)에서 34개 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)가 2개 signature(서명)로 접혀 후보 구분성이 약했다 | volatility/ATR(변동성/평균진폭), trend/ADX(추세/평균방향지수), rank/gate(순위/게이트)는 단서로 보존하되 proxy(대체) 경계는 반복하지 않는다 | raw/upstream feature surface(원천/상류 피처 표면)와 실제 feature order/model hash(피처 순서/모델 해시) 변경을 증명할 때 |
| `NR-032` | `IDEA-ST267-S264-AIH-STATE-ACCELERATION-INTERACTION` | state_acceleration_interaction(상태 가속 상호작용)이 2025H1 cross-period(확장 기간) 대조군에서 trade activation(거래 활성화)을 만들 수 있다 | run267BP(267BP 실행)에서 tester report(테스터 보고서)는 completed(완료)였지만 trade count(거래 수)가 `0`이고 runtime CSV(런타임 CSV)가 없어서 inactive surface(비활성 표면)로 분류했다 | state acceleration(상태 가속) 아이디어는 버리지 않지만 같은 threshold/surface(임계값/표면) 그대로 재실행하지 않는다 | feature surface(피처 표면), threshold(임계값), 또는 routing density(라우팅 밀도)를 바꿔 trade activation(거래 활성화)이 먼저 증명될 때 |
| `NR-033` | `IDEA-ST267-S264-AIH-ANTI-OVERCONSTRAINT-PRUNE` | anti_overconstraint_prune(과제약 제거)를 standalone research baseline candidate(독립 연구 기준 후보)로 밀 수 있다 | run267BQ/run267BR(267BQ/267BR 실행)에서 2023H2는 강했지만 2025H1/2025H2 PF(수익 팩터)가 얇고 DD(drawdown, 손실폭)와 sell/hour/late 약점이 남아 독립 선택에는 실패했다 | 2023H2 강세와 late net(후반 순수익)은 directional asymmetry(방향 비대칭)와 impulse replacement(임펄스 대체) seed clue(씨앗 단서)로 보존한다 | pool-wide side/impulse replacement(후보군 전체 방향/임펄스 대체)가 2024, 2025H1, 2025H2에서 거래 수와 PF/DD를 동시에 살릴 때 |
| `NR-034` | `IDEA-ST267-DIRECTIONAL-ASYMMETRY-STANDALONE` | directional_asymmetry(방향 비대칭)를 후보군 전체 standalone profile(독립 프로필)로 밀 수 있다 | run267BU(267BU 실행)에서 다섯 Baseline candidates(기준 후보) 모두 순수익 또는 PF(수익 팩터)가 약했고, DD(drawdown, 손실폭)가 높았다 | 방향 축은 버리지 않고 side-pressure diagnostic(방향 압박 진단)과 weak-slice explanation(약한 구간 설명)으로만 보존한다 | 새 side-specific model/source feature(방향별 모델/원천 피처)가 생겨 독립 신호가 아니라 구조 진단으로 재정의될 때 |

| `NR-035` | `IDEA-ST270-AGGRESSIVE-NONFILTER-REWARD-SKEW` | aggressive non-filter reward skew(공격형 비필터 보상 기울기)가 ONNX-worthy candidate(온엑스화 가치 후보)로 이어질 수 있다 | run270D(270D 실행)에서 active probe(활성 탐침) 4개가 OOS(표본외) 순수익 또는 DD(drawdown, 손실폭) 기준을 넘지 못했고 survivor(생존 후보)가 `0`개였다 | q03 supply expansion(공급 확장)은 near-breakeven OOS(근본전 표본외) 단서와 weak-slice map(약한 구간 지도)로만 보존한다 | loss-asymmetry/time-risk state(손실 비대칭/시간 위험 상태)를 새 feature/decision surface(피처/판단 표면)로 재구성할 때 |

| `NR-036` | `IDEA-ST271-FRESH-EDGE-REBUILD-AFTER-NONFILTER-FAILURE` | cp271A damage-first loss asymmetry(손상 우선 손실 비대칭)와 cp271C recovery-tail payoff rebalance(회복 꼬리 보상 재균형)가 Stage272(272단계) 탐침 씨앗이 될 수 있다 | run271E(271E 실행)에서 cp271A는 validation/OOS(검증/표본외) alignment(정렬률)가 약하고 route bias(경로 편향)가 있었으며, cp271C는 Tier A/Tier B(티어 A/티어 B) decision rate(판단 비율)가 크게 갈라졌다 | 손실 비대칭과 회복 보상 축은 버리지 않지만 같은 score surface(점수 표면) 그대로 반복하지 않는다 | partial-context adapter(부분 문맥 어댑터) 또는 새 decision surface(판단 표면)가 생길 때 |

| `NEG-ST273-Q04-STABILITY-FAILURE-RUN273B` | `273_onnx_candidate_campaign__time_risk_router_stability_validation` | q04 weak-clock throttle router(q04 약한 시계 제한 라우터) | valid_negative(유효한 부정) | month/hour loss concentration(월/시간 손실 집중) and curve fragility(곡선 취약성) | reopen only with fresh decision/risk surface(새 판단/위험 표면이 있을 때만 재개) | `stages/273_onnx_candidate_campaign__time_risk_router_stability_validation/03_reviews/run273B_report.md` |

| `NEG-ST274-RUN274E-cp274A` | `IDEA-ST274-POST-Q04-FILTER-LIKE-SCORE-SURFACE` | Post-q04 score surface(q04 이후 점수 표면)가 fresh decision surface(새 판단 표면)가 될 수 있다. | q04 control(q04 대조)과 entry signal(진입 신호)이 거의 같아 fresh decision surface(새 판단 표면)가 아니다. | Risk telemetry(위험 기록) 차이는 보존하지만 candidate package(후보 패키지)로 부르지 않는다. | 새 entry creation(진입 생성)이나 direction change(방향 변경)가 생길 때만 재개한다. |
| `NEG-ST274-RUN274E-cp274B` | `IDEA-ST274-POST-Q04-FILTER-LIKE-SCORE-SURFACE` | Post-q04 score surface(q04 이후 점수 표면)가 fresh decision surface(새 판단 표면)가 될 수 있다. | 새 active trade(활성 거래)를 만들지 않고 q04 trade(q04 거래)를 줄이기만 한다. | Removed pocket(제거 구간)은 failure memory(실패 기억)로 남겨 Stage275(275단계)에서 금지 반복을 막는다. | Non-filter reward creation(비필터 보상 생성) 또는 direction switch(방향 전환)가 생길 때만 재개한다. |
| `NEG-ST274-RUN274E-cp274C` | `IDEA-ST274-POST-Q04-FILTER-LIKE-SCORE-SURFACE` | Post-q04 score surface(q04 이후 점수 표면)가 fresh decision surface(새 판단 표면)가 될 수 있다. | q04 control(q04 대조)과 entry signal(진입 신호)이 거의 같아 fresh decision surface(새 판단 표면)가 아니다. | Risk telemetry(위험 기록) 차이는 보존하지만 candidate package(후보 패키지)로 부르지 않는다. | 새 entry creation(진입 생성)이나 direction change(방향 변경)가 생길 때만 재개한다. |

## 2026-05-23 run275E_screen_fresh_candidate_score_surfaces_v1

- failure_memory_rows(실패 기억 행): `1`
- evidence(근거): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275E/failure.csv`
- effect(효과): route bias(경로 편향)나 filter-like(필터형) 반복을 다음 candidate construction(후보 구성)에서 금지한다.

| `NEG-ST276-RUN276D-AGGRESSIVE-FRESH-SURFACE-FAILURE` | `IDEA-ST276-AGGRESSIVE-FRESH-SURFACE-PROBE` | aggressive fresh surface(공격형 새 표면)가 ONNX-worthy candidate(온엑스화 가치 후보)로 이어질 수 있다 | run276D(276D 실행)에서 survivor watch(생존 관찰)가 `0`개였고 cp275A/cp275B/cp275D(275A/275B/275D 패키지)는 pf_too_thin/OOS negative/deep slice hole(수익 팩터 과소/표본외 음수/깊은 구간 구멍)로 실패했다 | weak session/month/chron late(약한 세션/월/시간 후반) 실패 기억은 Stage277(277단계) fresh thesis seed(새 논제 씨앗)로 보존한다 | 새 feature/decision/risk surface(피처/판단/위험 표면)가 생기고 Tier A/Tier B(티어 A/티어 B) paired evidence(쌍 근거)가 닫힐 때만 재개한다 | `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/03_reviews/stage276_closeout_stage277_handoff.md` |

| `NEG-ST277-RUN277E-SCORE-SCREEN-NONPROBE` | `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277E` | `cp277A/cp277B` score surface(점수 표면)는 Stage278(278단계) MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침)로 넘기지 않는다 | run277E(277E 실행) screen_score(선별 점수)가 probe queue(탐침 대기열) 기준에 못 미쳤다 | score shape clue(점수 형태 단서)만 보존한다 | new feature/decision/risk surface(새 피처/판단/위험 표면) 또는 stronger score screen(더 강한 점수 선별)이 있을 때만 재개한다 | `stages/277_onnx_candidate_campaign__fresh_thesis_rebuild/02_runs/run277E/failure_memory.csv` |

| `NEG-ST278-DIRECTION-MAPPING-GAP` | `278_onnx_candidate_campaign__fresh_thesis_mt5_probe` | active/flat(활성/관망) signal payload(신호 페이로드)는 supported direction mapping(지원되는 방향 매핑) 없이 MT5 tester(MT5 테스터)로 갈 수 없다. | valid blocker(유효 차단) | reopen only through Stage279(279단계) direction source audit(방향 원천 감사) |

| `NEG-ST279-DIRECTIONAL-MAPPING-RUN279D` | `279_onnx_candidate_campaign__directional_runtime_mapping_rebuild` | runtime probe failure memory(런타임 탐침 실패 기억) `8`개 | Reopen only with new decision/risk surface(새 판단/위험 표면일 때만 재개) | `stages/279_onnx_candidate_campaign__directional_runtime_mapping_rebuild/02_runs/run279D/runtime_probe_failure_memory.csv` |

| `NEG-ST280-DIRECTIONAL-STABILITY` | `280_onnx_candidate_campaign__directional_mapping_stability_validation` | 생존 씨앗 `3`개가 안정성 검증에서 선택 후보가 되지 못함 | 새 손실폭 정규화 판단/위험 표면일 때만 재개 | `stages/280_onnx_candidate_campaign__directional_mapping_stability_validation/02_runs/run280A/stability_failure_memory.csv` |

| `NEG-ST281-DRAWDOWN-NORMALIZED-DIRECTION` | `281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild` | drawdown-normalized directional rebuild(손실폭 정규화 방향 재구성)이 validation(검증) 회복력 기준을 통과하지 못함 | OOS(표본외) 상방은 후보 선택 근거가 아니라 Stage282(282단계) 새 논제 입력으로만 사용 | `stages/281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild/02_runs/run281C/failure_memory.csv` |

| `NEG-ST286-CURVE-QUALITY-FAIL` | `286_onnx_candidate_campaign__trade_density_curve_quality_rebuild` | `run286C_review_trade_density_curve_quality_mt5_probe_v1` | density/scale clue(밀도/규모 단서)는 있으나 curve pocket(곡선 포켓)과 underwater ratio(수중 비율)가 ONNX-worthy candidate(온엑스 가치 후보) 기준 미달 | Stage287(287단계)에서 새 구조로만 재개 | threshold-only repair(임계값만 고치는 수리) 금지 |

| `NEG-ST287-DENSITY-SCALE-CURVE-POCKET` | `287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild` | `run287C_review_density_scale_curve_pocket_mt5_probe_v1` | density/profit seed found but no candidate(밀도/수익 씨앗은 있으나 후보 없음) | efficiency/curve gate failed(효율/곡선 게이트 실패) | reopen only with risk/reward/exit surface(위험/보상/청산 표면으로만 재개) |

| `NEG-ST288-RISK-REWARD-EXIT` | `288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild` | `run288C_review_risk_reward_exit_asymmetry_mt5_probe_v1` | risk/reward/exit-only failed(위험/보상/청산 단독 실패) | OOS and curve did not survive(표본외와 곡선 생존 실패) | reopen only with regime-conditioned edge surface(국면 조건부 엣지 표면으로만 재개) |

| `NEG-ST289-REGIME-CONDITIONED-EDGE` | `289_onnx_candidate_campaign__regime_conditioned_edge_surface_rebuild` | `run289C_review_regime_conditioned_edge_mt5_probe_v1` | regime-conditioned inherited signal filtering failed(국면 조건부 계승 신호 필터링 실패) | validation net/PF/recovery(검증 순수익/수익 팩터/회복)가 후보 기준 미달 | reopen only with payoff-weighted fresh model surface(수익 가중 새 모델 표면으로만 재개) |

| `NEG-ST290-PAYOFF-WEIGHTED-EDGE` | `IDEA-ST290-PAYOFF-WEIGHTED-EDGE-MODEL` | payoff-weighted edge model(손익가중 엣지 모델)이 ONNX-worthy candidate(온엑스화 가치 후보)로 이어질 수 있다 | run290C(290C 실행)에서 MT5 KPI/곡선/거래품질 gate(게이트)를 통과한 candidate package(후보 패키지)가 없었다 | inverse orientation(역방향) 공통성과 density construction(밀도 구성)은 Stage291(291단계) seed clue(씨앗 단서)로 보존한다 | walk-forward payoff generalization(워크포워드 손익 일반화), side relabel(방향 재라벨), native cost/curve objective(비용/곡선 내장 목적함수)가 생길 때 |

| `NEG-ST291-WFO-PAYOFF-GENERALIZATION` | `IDEA-ST291-WFO-PAYOFF-GENERALIZATION` | walk-forward payoff generalization(워크포워드 손익 일반화)이 ONNX-worthy candidate(온엑스 가치 후보)로 이어질 수 있다 | run291C(291C 실행)에서 6개 후보 모두 actual routed total(실제 라우팅 전체) 기준 순손실 또는 낮은 PF/회복/곡선 실패로 candidate package(후보 패키지)가 없었다 | broad WFO signal(넓은 워크포워드 신호)은 실패 기억으로 남기고, invert/skip/meta-label(반전/회피/메타라벨) 단서만 Stage292(292단계)로 넘긴다 | anti-direction meta-label(역방향 메타라벨), trade simulator objective(거래 시뮬레이터 목적함수), density/profit two-head router(밀도/수익 이중 헤드 라우터)처럼 구조가 바뀔 때만 재개 |

| `NEG-ST292-ANTI-DIRECTION-META-TRADE-SIM` | `IDEA-ST292-ANTI-DIRECTION-META-LABEL-TRADE-SIM` | anti-direction/meta trade simulator(반대방향/메타 거래 시뮬레이터)가 ONNX-worthy candidate(ONNX화 가치 후보)로 닫히지 않음 | run292C(292C 실행)에서 최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 곡선 포켓을 함께 통과한 패키지가 없음 | proxy(대리값)와 MT5 runtime(MT5 런타임)의 공백을 실패 기억으로 보존 | 새 runtime-aware simulator calibration(런타임 인식 시뮬레이터 보정)이나 curve objective(곡선 목적함수)일 때만 재개 |

| `NEG-ST293-PROFIT-SCALE-DENSITY-CALIBRATION` | `IDEA-ST293-PROFIT-SCALE-DENSITY-CALIBRATION` | profit-scale density calibration(순수익 규모/거래 밀도 보정)이 ONNX-worthy candidate(ONNX화 가치 후보)로 닫히지 않음 | run293C(293C 실행)에서 모든 actual routed total(실제 라우팅 전체)이 검증 또는 표본외 순손실이고 PF(수익 팩터), 회복, 기대값, 곡선 포켓을 함께 통과한 패키지가 없음 | cp293A/cp293F의 근본전 고밀도 손실은 outcome relabel(결과 재라벨)과 direction flip(방향 반전) 입력으로 보존 | MT5 filled trade outcome(체결 거래 결과) 기반 새 label/decision/risk surface(라벨/판단/위험 표면)일 때만 재개 |

| `NEG-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP` | `IDEA-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP` | MT5 outcome relabel directional flip(MT5 결과 재라벨 방향 반전)이 ONNX-worthy candidate(ONNX화 가치 후보)로 닫히지 않음 | run294C(294C 실행)에서 OOS(표본외)는 일부 양수였지만 모든 validation(검증)이 음수라 후보 게이트를 통과하지 못함 | flip(반전)이 OOS 단서를 만들 수 있다는 점은 보존하되, validation damage(검증 손상)를 새 구조로 다뤄야 함 | split-consistent outcome distillation(분할 일관 결과 증류) 또는 validation damage veto(검증 손상 거부)일 때만 재개 |

| `NEG-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION` | `IDEA-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION` | split-consistent outcome distillation(분할 일관 결과 증류)이 ONNX-worthy candidate(온엑스화 가치 후보)로 닫히지 않음 | 모든 actual routed total(실제 라우팅 전체)이 4-10 trades/day(일 4-10거래), split-positive 수익, 곡선 proxy(대리 지표)를 동시에 통과하지 못함 | cp295D는 저밀도 수익 단서, cp295B/E는 OOS 상방 단서로만 보존 | fresh density-floor profit expansion(새 거래 밀도 하한 수익 확장)에서만 재개 |

| `NEG-ST296-DENSITY-FLOOR-PROFIT-EXPANSION` | `IDEA-ST296-DENSITY-FLOOR-PROFIT-EXPANSION` | density-floor profit expansion(거래 밀도 하한 수익 확장)이 ONNX-worthy candidate(ONNX화 가치 후보)로 닫히지 않음 | run296C(296C 실행)에서 최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 곡선 포켓을 함께 통과한 패키지가 없음 | cp296 proxy(대리) 상방은 보존하되 MT5 runtime(메타트레이더5 런타임)에서 수익 규모와 곡선 품질을 같이 만족해야 함 | 새 curve-monotonic profit objective(곡선 단조 수익 목적함수) 또는 entry/risk surface(진입/위험 표면)일 때만 재개 |

## run297C_review_bilevel_curve_monotonic_profit_mt5_probe_v1 Stage297 low profit-scale negative memory(297단계 낮은 수익 규모 부정 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 4-10 trades/day(일 4-10거래)는 대체로 유지됐지만 순수익 규모, OOS PF(표본외 수익 팩터), recovery(회복), curve pocket(곡선 포켓)이 동시에 부족했다.
- do_not_repeat(반복 금지): Stage297 robust bucket(강건 구간) agree/soft flip/veto 임계값만 좁게 바꾸는 repair(수리)는 하지 않는다.
- reopen_condition(재개 조건): 실제 MT5 routed total(라우팅 전체)에서 validation/OOS 각각 net profit(순수익) 300 이상과 combined(합산) 800 이상을 먼저 보여야 한다.

## run298C_review_profit_scale_edge_amplification_mt5_probe_v1 Stage298 payoff-rank validation damage negative memory(298단계 보상 순위 검증 손상 부정 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): OOS(표본외) 양수 단서는 있었지만 validation(검증)이 음수로 돌아서고 DD(손실폭)가 커졌다.
- do_not_repeat(반복 금지): payoff rank(보상 순위), hold widening(보유 확장), density8 control(밀도 8 대조)을 같은 임계값만 바꿔 반복하지 않는다.
- reopen_condition(재개 조건): 런타임 실제 거래 형태가 validation/OOS 모두 순수익 300 이상과 깊은 포켓 제거를 보여야 한다.

## run299C_review_runtime_realized_trade_shape_mt5_probe_v1 Stage299 validation-positive OOS-negative memory(299단계 검증 양수 표본외 음수 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 일부 후보는 validation(검증) 순수익/PF(수익 팩터)를 회복했지만 OOS(표본외)가 음수라 ONNX-worthy(온엑스 가치) 조건을 만족하지 못했다.
- do_not_repeat(반복 금지): 같은 trade-shape quantile(거래 형태 분위) 또는 loss-cluster veto(손실 군집 거부) 조정만 반복하지 않는다.
- reopen_condition(재개 조건): split-forward(분할 전진) 구조에서 validation/OOS 모두 순수익 300 이상과 곡선 포켓 제거를 먼저 보여야 한다.

## run300C_review_split_forward_trade_shape_generalization_mt5_probe_v1 Stage300 split-forward profit scale failure memory(300단계 검증 양수 표본외 음수 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 일부 후보는 validation(검증) 순수익/PF(수익 팩터)를 회복했지만 OOS(표본외)가 음수라 ONNX-worthy(온엑스 가치) 조건을 만족하지 못했다.
- do_not_repeat(반복 금지): 같은 trade-shape quantile(거래 형태 분위) 또는 loss-cluster veto(손실 군집 거부) 조정만 반복하지 않는다.
- reopen_condition(재개 조건): split-forward(분할 전진) 구조에서 validation/OOS 모두 순수익 300 이상과 곡선 포켓 제거를 먼저 보여야 한다.

## run301C_review_orthogonal_profit_source_mt5_probe_v1 Stage301 positive-small failure memory(301단계 양수-소규모 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 일부 profile(프로필)은 validation/OOS(검증/표본외) 모두 양수였지만 수익 규모, 회복계수, 곡선 포켓 조건을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): HGB inverse-return(HGB 역방향 수익률) density(밀도)만 좁게 조정하지 않는다.
- reopen_condition(재개 조건): 실제 MT5(메타트레이더5)에서 충분한 OOS(표본외) 순수익과 매끄러운 확대 곡선을 먼저 보여야 한다.

## run302C_review_payoff_convexity_profit_scale_mt5_probe_v1 Stage302 OOS-scale validation-damage failure memory(302단계 표본외 규모/검증 손상 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 일부 profile(프로필)은 OOS(표본외) 수익 규모가 컸지만 validation(검증) 손익/회복/곡선 포켓 조건을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): ATR/risk(ATR/위험) 배수만 좁게 조정하지 않는다.
- reopen_condition(재개 조건): 실제 MT5(메타트레이더5)에서 충분한 OOS(표본외) 순수익과 매끄러운 확대 곡선을 먼저 보여야 한다.

## run303C_review_regime_balanced_profit_scale_router_mt5_probe_v1 Stage303 OOS-scale validation-damage failure memory(302단계 표본외 규모/검증 손상 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 일부 profile(프로필)은 OOS(표본외) 수익 규모가 컸지만 validation(검증) 손익/회복/곡선 포켓 조건을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): ATR/risk(ATR/위험) 배수만 좁게 조정하지 않는다.
- reopen_condition(재개 조건): 실제 MT5(메타트레이더5)에서 충분한 OOS(표본외) 순수익과 매끄러운 확대 곡선을 먼저 보여야 한다.

## run304C_review_curve_pocket_aware_profit_source_mt5_probe_v1 Stage304 curve-pocket-aware failure memory(304단계 곡선 포켓 인식 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 실제 MT5(메타트레이더5) routed total(라우팅 전체)에서 수익 규모, 효율, 밀도, 곡선 포켓을 동시에 만족하지 못한 분기.
- do_not_repeat(반복 금지): 같은 Stage304 표면에서 lot(랏), ATR(평균진폭), density(밀도)만 미세 조정하지 않는다.
- reopen_condition(재개 조건): runtime-realized trade attribution(런타임 실제 거래 기여도)으로 새 수익 원천을 만들 때만 재사용한다.

## run305C_review_runtime_realized_curve_attribution_mt5_probe_v1 Stage306 curve-pocket-aware failure memory(304?④퀎 怨≪꽑 ?ъ폆 ?몄떇 ?ㅽ뙣 湲곗뼲)

- failed_profiles(?ㅽ뙣 ?꾨줈??: `6`
- failure_boundary(?ㅽ뙣 寃쎄퀎): ?ㅼ젣 MT5(硫뷀??몃젅?대뜑5) routed total(?쇱슦???꾩껜)?먯꽌 ?섏씡 洹쒕え, ?⑥쑉, 諛?? 怨≪꽑 ?ъ폆???숈떆??留뚯”?섏? 紐삵븳 遺꾧린.
- do_not_repeat(諛섎났 湲덉?): 媛숈? Stage306 ?쒕㈃?먯꽌 lot(??, ATR(?됯퇏吏꾪룺), density(諛??留?誘몄꽭 議곗젙?섏? ?딅뒗??
- reopen_condition(?ш컻 議곌굔): runtime-realized trade attribution(?고????ㅼ젣 嫄곕옒 湲곗뿬???쇰줈 ???섏씡 ?먯쿇??留뚮뱾 ?뚮쭔 ?ъ궗?⑺븳??

## run306C_review_anti_surface_trade_shape_mt5_probe_v1 Stage306 anti-surface trade-shape failure memory(306단계 반표면 거래 형태 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 실제 MT5(메타트레이더5) routed total(라우팅 전체)에서 수익 규모, 효율, 밀도, 곡선 포켓을 동시에 만족하지 못한 분기다.
- do_not_repeat(반복 금지): 같은 Stage306 표면에서 lot(랏), ATR(평균진폭), density(밀도)만 미세 조정하지 않는다.
- reopen_condition(재개 조건): 새 수익 원천이나 새 구조가 validation/OOS(검증/표본외) 규모와 곡선을 함께 개선할 때만 재사용한다.

## run307C_review_post_trade_shape_scale_mt5_probe_v1 Stage307 post-trade-shape scale failure memory(307단계 거래 형태 이후 수익 규모 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): 실제 MT5(메타트레이더5) routed total(라우팅 전체)에서 수익 규모, 효율, 밀도, 곡선 포켓을 동시에 만족하지 못한 분기다.
- do_not_repeat(반복 금지): 같은 Stage307 return-rank(수익 순위) 표면에서 lot(랏), ATR(평균진폭), density(밀도)만 미세 조정하지 않는다.
- reopen_condition(재개 조건): 새 수익 원천이나 새 구조가 validation/OOS(검증/표본외) 규모와 곡선을 함께 개선할 때만 재사용한다.

## run308C_review_non_return_rank_profit_source_mt5_probe_v1 Stage308 non-return-rank source failure memory(308단계 비수익순위 원천 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5) routed total(라우팅 전체)에서 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.
- preserved_clue(보존 단서): cp308E(308E 후보)는 OOS(표본외) 수익 단서가 있으나 validation(검증) 수익과 DD(drawdown, 손실폭)가 약하다.
- do_not_repeat(반복 금지): Stage308(308단계) 표면에서 density/hold/ATR(밀도/보유/평균진폭)만 좁게 조정하지 않는다.
- reopen_condition(재개 조건): split-coherent(분할 일관) validation/OOS(검증/표본외) 수익과 곡선 포켓이 같이 개선될 때만 재사용한다.

## run309C_review_split_coherent_profit_curve_source_mt5_probe_v1 Stage309 split-coherent source failure memory(309단계 분할 일관 원천 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5) routed total(라우팅 전체)에서 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.
- preserved_clue(보존 단서): cp309A/cp309E(309A/309E 후보)는 양수 조각이 있으나 각각 규모/거래수/곡선이 부족하다.
- do_not_repeat(반복 금지): Stage309(309단계) 표면에서 density/hold/lot(밀도/보유/랏)만 좁게 조정하지 않는다.
- reopen_condition(재개 조건): runtime positive fragments(런타임 양수 조각)를 새 allocation layer(배분 계층)로 결합할 때만 재사용한다.

## run310C_review_runtime_positive_fragment_allocation_mt5_probe_v1 Stage310 allocation failure memory(310단계 배분 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 수익 규모, 효율, 거래수, 곡선 포켓을 동시에 만족하지 못했다.
- preserved_clue(보존 단서): 양수 조각이 있더라도 배분만으로는 ONNX-worthy(온엑스 가치 있음) 후보가 되지 않을 수 있다.
- do_not_repeat(반복 금지): Stage310 allocation(310단계 배분)을 lot/hold/density(수량/보유/밀도)만 좁게 바꿔 반복하지 않는다.
- reopen_condition(재개 조건): 새 feature/model/risk surface(피처/모델/위험 표면)가 함께 바뀔 때만 재사용한다.

## run311C_review_post_allocation_fresh_edge_mt5_probe_v1 Stage311 fresh edge failure memory(311단계 새 엣지 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 수익 규모, 효율, 거래수, 곡선 포켓을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): hour mirror(시간 반전)만 좁게 반복하지 않는다.
- reopen_condition(재개 조건): 모델/피처 비대칭 표면이 함께 바뀔 때만 재사용한다.

## run312C_review_fresh_model_asymmetry_mt5_probe_v1 Stage312 fresh model asymmetry failure memory(312단계 새 모델 비대칭 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 최소 거래 수, 밀도, 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): 시간-방향 표만 좁게 다시 보정하지 않는다.
- reopen_condition(재개 조건): runtime outcome source(런타임 결과 원천) 자체를 바꿀 때만 재사용한다.

## run313C_review_runtime_outcome_source_pivot_mt5_probe_v1 Stage313 runtime outcome source pivot failure memory(313단계 런타임 결과 원천 전환 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 최소 거래 수, 밀도, 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): 시간-방향 표만 좁게 다시 보정하지 않는다.
- reopen_condition(재개 조건): runtime outcome source(런타임 결과 원천) 자체를 바꿀 때만 재사용한다.

## run314C_review_runtime_outcome_feature_source_mt5_probe_v1 Stage314 runtime outcome feature source failure memory(314단계 런타임 결과 피처 원천 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 최소 거래 수, 밀도, 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): 시간-방향 표만 좁게 다시 보정하지 않는다.
- reopen_condition(재개 조건): runtime outcome source(런타임 결과 원천) 자체를 바꿀 때만 재사용한다.

## run315C_review_runtime_outcome_feature_interaction_mt5_probe_v1 Stage315 runtime outcome feature interaction failure memory(315단계 런타임 결과 피처 상호작용 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 최소 거래수, 4-10 trades/day(일 4-10거래), 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): hour-only repair(시간만 고치는 수리)나 lot-only scale(랏만 키우는 규모화)을 반복하지 않는다.
- reopen_condition(재개 조건): feature/model/risk surface(피처/모델/위험 표면)를 새로 바꿀 때만 재사용한다.

## run316C_review_post_interaction_profit_scale_curve_mt5_probe_v1 Stage316 post interaction profit scale/curve failure memory(316단계 상호작용 이후 수익 규모/곡선 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 최소 거래수, 4-10 trades/day(일 4-10거래), 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): hour-only repair(시간만 고치는 수리)를 더 반복하지 않는다.
- reopen_condition(재개 조건): non-time profit source(비시간 수익 원천)나 새 model surface(모델 표면)를 만들 때만 재사용한다.

## run317C_review_fresh_non_time_profit_source_mt5_probe_v1 Stage317 fresh non-time profit source failure memory(317단계 새 비시간 수익 원천 실패 기억)

- failed_profiles(실패 프로필): `6`
- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 최소 거래수, 4-10 trades/day(일 4-10거래), 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.
- do_not_repeat(반복 금지): 한 표면의 lot/hold(랏/보유) 좁은 수리를 반복하지 않는다.
- reopen_condition(재개 조건): 새 feature surface(피처 표면)나 curve stability(곡선 안정성) 구조를 만들 때만 재사용한다.

## run318C_review_post_non_time_curve_stability_mt5_probe_v1 Stage318 curve-pocket failure memory(318단계 곡선 포켓 실패 기억)

- failed_profiles(실패 프로필): `4` direct failures plus survivor seeds still not selected.
- failure_boundary(실패 경계): 큰 순수익만으로 ONNX-worthy(온엑스 가치 있음) 후보가 되지 않는다. DD%(드로다운 비율), 양수 월 비율, 긴 underwater stretch(수중 구간)가 같이 통과해야 한다.
- preserved_clue(보존 단서): cp318A/cp318D(318A/318D 후보)는 수익 규모와 거래 밀도 단서로 Stage319(319단계)에 넘긴다.
- do_not_repeat(반복 금지): Stage318(318단계) score threshold(점수 임계값)만 좁게 올리고 내리는 repair(수리)를 반복하지 않는다.
- reopen_condition(재개 조건): curve-pocket risk asymmetry(곡선 포켓 위험 비대칭)나 새 feature/risk surface(피처/위험 표면)가 있을 때만 다시 쓴다.

## run319C_review_curve_pocket_risk_asymmetry_mt5_probe_v1 Stage319 validation pocket memory(319단계 검증 포켓 기억)

- failure_boundary(실패 경계): 수익 규모가 커도 validation DD%(검증 드로다운 비율)와 underwater stretch(수중 구간)가 깊으면 ONNX-worthy(온엑스 가치 있음) 후보가 아니다.
- preserved_clue(보존 단서): cp319D/cp319B/cp319F(319D/319B/319F 후보)는 Stage320(320단계) validation pocket controller(검증 포켓 제어기) 씨앗으로 쓴다.
- do_not_repeat(반복 금지): volatility cap(변동성 상한)만 다시 조절하는 좁은 수리를 반복하지 않는다.

## run320C_review_validation_pocket_drawdown_controller_mt5_probe_v1 Stage320 controller failure(320단계 제어기 실패)

- failure_boundary(실패 경계): VIX/quality controller(VIX/품질 제어기)는 검증 DD%(드로다운 비율)와 PF(수익 팩터)를 악화시켰다.
- do_not_repeat(반복 금지): 같은 controller(제어기) 변형 반복 금지.

## run321C_review_post_controller_profit_curve_mt5_probe_v1 Stage321 review failure memory(321단계 검토 실패 기억)

- cp321C(321C 후보): highest profit scale(최대 수익 규모)이지만 OOS(표본외) 확대 구간 포켓 때문에 Stage322(322단계) 씨앗에서 제외.
- cp321A/cp321D/cp321E/cp321F: DD/PF/zoom gate(드로다운/수익 팩터/확대 관문) 중 하나 이상 실패.
## run322C_review_cp321b_curve_stability_pressure_mt5_probe_v1 Stage322 pressure memory(322단계 압박 기억)

- selected_candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface`
- boundary(경계): Adapter(어댑터)와 ONNX(온엑스)는 not_started(미시작).
- do_not_repeat(반복 금지): exact replay(정확 재생)만 통과한 경우에는 후보로 포장하지 않는다.

## run330G_raw_forward_failure_fragility_memory_and_overfit_followup_v1 Stage330 failure memory(330단계 실패 기억)

- failed_or_high_pressure_profiles(실패 또는 높은 압력 프로필): `c56_bal_rf, m48_bal_rf, u42_bal_rf, u42_plain_rf`
- preserved_clues_not_selection(선택 아닌 보존 단서): `c56_plain_rf, m48_plain_rf`
- memory_rows(기억 행): `6`
- failure_boundary(실패 경계): raw-forward MT5(원본 전진 MT5) 양수 결과만으로는 cost stress(비용 압박), curve pocket(곡선 포켓), direction attribution(방향 귀속), D/B source(D/B 원천) 공백을 닫지 못했다.
- do_not_repeat(반복 금지): forward(전진) 양수 후보에 threshold(임계값), lot(수량), balanced/plain(균형/일반)만 좁게 맞추는 수리를 반복하지 않는다.
- reopen_condition(재개 조건): cross-horizon(교차 기간), cost stress(비용 압박), curve pocket(곡선 포켓), runtime parity(런타임 동등성)가 같은 no-retune(무재튜닝) 기준에서 동시에 약해질 때만 재개한다.

## run337AF_failure_memory_and_no_overfit_rebuild_queue_v1 Stage337 cost/direction/curve negative memory(337단계 비용/방향/곡선 부정 기억)

- failed_or_boundary_profiles(실패 또는 경계 프로필): `7`
- failure_boundary(실패 경계): completed-day positive net(완성일 양수 순수익)은 cost stress(비용 압박), recovery/DD(회복/손실폭), direction asymmetry(방향 비대칭), curve pocket(곡선 포켓), D/B source gap(D/B 원천 공백), economic regime gap(경제 국면 공백), full current-day visibility gap(현재일 전체 가시성 공백)을 닫지 못했다.
- do_not_repeat(반복 금지): forward data(전진 데이터)에 threshold/lot/short/risk(임계값/랏/숏/위험)를 좁게 맞추지 않는다.
- preserved_clue(보존 단서): cost ladder(비용 사다리), rolling pocket(이동 포켓), side-specific payoff(방향별 손익), as-of regime source(시점 기준 국면 원천), proxy/MT5 role lock(프록시/MT5 역할 고정)을 run337AG(337AG 실행)로 넘긴다.
- reopen_condition(재개 조건): predeclared split/WFO(사전 선언 분할/워크포워드)와 MT5 runtime probe(MT5 런타임 탐침)에서 비용/곡선/방향/데이터/동등성 gate(게이트)가 동시에 닫힐 때만 재개한다.

## 2026-06-01 run338A Stage Branch Negative Memory(부정 기억)

- subject(대상): Stage337 proxy-positive MT5-negative runtime probe(프록시 양수 MT5 음수 런타임 탐침)
- judgment(판정): `valid_negative(유효한 부정)`
- carried_to(이월 대상): `338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair`
- evidence(근거): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/final_decision.json`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/jr_mt5_runtime_probe_review_scorecard.csv`, `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338A/stage338_negative_memory_seed.csv`
- effect(효과): 신호 재현 문제로 오해하지 않고 거래 생명주기 수리 제약으로 사용한다.

## 2026-06-01 Stage339B Lifecycle Exit Failure Memory(생명주기 청산 실패 기억)

- subject(대상): close_on_flat(평탄 청산) and aggressive long relief(공격적 롱 완화)
- evidence(근거): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339B/failure_memory.csv`
- judgment(판정): `negative_clue_with_salvage(회수 가치 있는 부정 단서)`
- effect(효과): 실패 변형을 버리지 않고 run339C(339C 실행)의 제약으로 바꾼다.

## 2026-06-01 Stage339B Lifecycle Exit Failure Memory(생명주기 청산 실패 기억)

- subject(대상): close_on_flat(평탄 청산) and aggressive long relief(공격적 롱 완화)
- evidence(근거): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339B/failure_memory.csv`
- judgment(판정): `negative_clue_with_salvage(회수 가치 있는 부정 단서)`
- effect(효과): 실패 변형을 버리지 않고 run339C(339C 실행)의 제약으로 바꾼다.

## 2026-06-01 Stage339E Side Balance Failure Memory(방향 균형 실패 기억)

- subject(대상): strict_short_overprune(엄격한 숏 과삭감) and raw_long_relief_profit_tax(무제약 롱 완화 수익세)
- evidence(근거): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339E/failure_memory.csv`
- judgment(판정): `negative_clue_with_salvage(회수 가치 있는 부정 단서)`
- effect(효과): short_threshold(숏 임계값) 0.57+ 단독 수리와 long_threshold(롱 임계값) 0.44~0.46 단독 완화를 반복하지 않고, min_margin(최소 마진)을 다음 제약으로 쓴다.

## 2026-06-01 Stage340B Balance Failure Memory(340B 균형 실패 기억)

- subject(대상): over-relieved long balance(과완화 롱 균형) and short_threshold_056(숏 임계값 0.56)
- evidence(근거): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340B/failure_memory.csv`
- judgment(판정): `negative_clue_with_salvage(회수 가치가 있는 부정 단서)`
- effect(효과): 균형만 보고 threshold(임계값)를 완화하는 반복을 막고 f01(에프01) 주변 압박으로 좁힌다.

## 2026-06-01 Stage340E Close-On-Flat Control Mismatch(평탄 청산 대조 불일치)

- subject(대상): `run340D_close_on_flat_true_pressure_surface`
- evidence(근거): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/control_semantics_audit.csv`, `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/failure_memory.csv`
- judgment(판정): `negative_surface_with_invalid_exact_control(무효 정확 대조를 가진 부정 표면)`
- effect(효과): run340D(340D 실행)를 원본 f01 실패로 과장하지 않고, close_on_flat=True(평탄 청산 켬) 재사용을 막는다.

## 2026-06-01 Stage340E Close-On-Flat Control Mismatch(평탄 청산 대조 불일치)

- subject(대상): `run340D_close_on_flat_true_pressure_surface`
- evidence(근거): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/control_semantics_audit.csv`, `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/failure_memory.csv`
- judgment(판정): `negative_surface_with_invalid_exact_control(무효 정확 대조를 가진 부정 표면)`
- effect(효과): run340D(340D 실행)를 원본 f01 실패로 과장하지 않고, close_on_flat=True(평탄 청산 켬) 재사용을 막는다.

## 2026-06-01 Stage340H Hold-Only Recovery Tax(보유 단독 회복 손상)

- subject(대상): `q07_h10` and `q08_h14`
- evidence(근거): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/failure_memory.csv`
- judgment(판정): `negative_clue_with_constraint(제약으로 남기는 부정 단서)`
- effect(효과): hold-only(보유만 변경) 반복을 줄이고 session/regime(세션/국면) 조건과 결합할 때만 다시 연다.

## 2026-06-01 Stage342D Hard Firewall Failure Memory(342D 강한 방화벽 실패 기억)

- subject(대상): `hard_early_long_0_110_trade_shape_tax`
- evidence(근거): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342D/failure_memory.csv`
- judgment(판정): `positive_clue_with_selection_blocker(선정 차단이 있는 긍정 단서)`
- effect(효과): hard block(강한 차단)을 반복 선정하지 않고 soft window(부드러운 구간)로 이동한다.

## 2026-06-01 Stage342G Soft Window Failure Memory(342G 부드러운 구간 실패 기억)

- subject(대상): `soft_window_0_45_0_75_trade_shape_no_recovery`
- evidence(근거): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342G/failure_memory.csv`
- judgment(판정): `negative_boundary_with_preserved_profit_clue(수익 단서를 보존한 부정 경계)`
- effect(효과): time-window only(시간 구간만) 변형을 반복하지 않고 quality/margin(품질/마진) 축으로 이동한다.

## run344E Exit Overlay Failure Memory(청산 오버레이 실패 기억)

- failure(실패): s09/s10/s12 exit lifecycle overlay(청산 생명주기 오버레이)는 net/PF/expectancy(순수익/수익 팩터/기대값)를 훼손했다.
- effect(효과): 다음 작업에서 전역 청산 수리(global exit repair, 전역 청산 수리)를 기본 해법으로 반복하지 않는다.

## run344E Exit Overlay Failure Memory(청산 오버레이 실패 기억)

- failure(실패): s09/s10/s12 exit lifecycle overlay(청산 생명주기 오버레이)는 net/PF/expectancy(순수익/수익 팩터/기대값)를 훼손했다.
- effect(효과): 다음 작업에서 전역 청산 수리(global exit repair, 전역 청산 수리)를 기본 해법으로 반복하지 않는다.

## 2026-06-01 run344L Failure Memory(실패 기억)

- source_run(원천 실행): `run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- failure(실패): heavy cost recovery breaks(강한 비용 회복 실패), cash-open concentration(현금장 초반 집중), short carry majority(숏 기여 과반)
- effect(효과): 다음 run344M은 이 조건을 완화하지 않고 설계 제약으로 가져간다.

## 2026-06-01 run344L Failure Memory(실패 기억)

- source_run(원천 실행): `run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- failure(실패): heavy cost recovery breaks(강한 비용 회복 실패), cash-open concentration(현금장 초반 집중), short carry majority(숏 기여 과반)
- effect(효과): 다음 run344M은 이 조건을 완화하지 않고 설계 제약으로 가져간다.

## 2026-06-01 run346B Cash-Open Side-Filter Failure Memory(현금장 방향 필터 실패 기억)

- source_run(원천 실행): `run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1`
- failure(실패): single side-filter variants(단일 방향 필터 변형)는 balance(균형) 또는 trade count(거래수)를 일부 바꿨지만 net/PF/recovery(순수익/수익 팩터/회복)를 함께 개선하지 못했다.
- evidence(근거): `stages/346_cash_open_runtime_review__asymmetric_source_pivot/02_runs/run346B/failure_memory.csv`
- salvage_value(회수 가치): long-quality fragment(롱 품질 조각)와 short-carry fragment(숏 기여 조각)를 separate source/head(분리 원천/헤드)로 넘긴다.
- do_not_repeat(반복 금지): cash-open short block(현금장 초반 숏 차단), late-long firewall(후반 롱 방화벽), short-only(숏 전용)를 운영 후보처럼 반복하지 않는다.

| `NR-ST347C-LONG-OOS-MISSING` | `IDEA-ST347-RUN347C-ASYMMETRIC-SOURCE-PROXY-TRAINING` | long quality teacher label(롱 품질 교사 라벨)이 validation/test(검증/테스트)에 없다 | run347C split audit(347C 분할 감사) | long head(롱 헤드)는 OOS 검증 불충분으로 낮춰 말한다 | richer long source label(더 풍부한 롱 원천 라벨) 또는 MT5 probe(런타임 탐침) 비교 시 재개 |

## 2026-06-01 run348A Proxy Review Constraint Memory(프록시 검토 제약 기억)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- constraint(제약): long OOS positive labels(롱 표본외 양성 라벨)이 `0`이라 long quality(롱 품질)를 OOS(`out-of-sample`, 표본외) 근거로 주장할 수 없다.
- proxy_boundary(프록시 경계): proxy expected value(프록시 예상값)는 signal sanity check(신호 점검)이고 MT5 KPI(MT5 핵심 성과 지표)가 아니다.
- effect(효과): run348B(348B 실행)는 선정(selection, 선정)이 아니라 review/triage(검토/분류)로만 닫아야 한다.
- evidence(근거): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348A/stage348_negative_memory_seed.csv`

## 2026-06-01 run348B Proxy Review Negative Memory(프록시 검토 부정 기억)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- negative_memory(부정 기억): long OOS positive labels(롱 표본외 양성 라벨) `0`; default short OOS head(기본 숏 표본외 헤드) 약함.
- salvage_value(회수 가치): ONNX deployable short threshold seeds(온엑스 배포 가능 숏 임계값 씨앗) `4`개.
- do_not_repeat(반복 금지): all-split proxy queue(전체 분할 프록시 대기열)를 candidate selection(후보 선정)이나 MT5 KPI(MT5 핵심 성과 지표)처럼 쓰지 않는다.
- reopen_condition(재개 조건): run348C/MT5 probe(348C/MT5 탐침)에서 실제 거래 KPI(거래 핵심 성과 지표)가 확인되거나 long OOS label source(롱 표본외 라벨 원천)가 보강될 때.
- evidence(근거): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348B/review_findings.csv`

## 2026-06-01 run348B Proxy Review Negative Memory(프록시 검토 부정 기억)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- negative_memory(부정 기억): long OOS positive labels(롱 표본외 양성 라벨) `0`; default short OOS head(기본 숏 표본외 헤드) 약함.
- salvage_value(회수 가치): ONNX deployable short threshold seeds(온엑스 배포 가능 숏 임계값 씨앗) `4`개.
- do_not_repeat(반복 금지): all-split proxy queue(전체 분할 프록시 대기열)를 candidate selection(후보 선정)이나 MT5 KPI(MT5 핵심 성과 지표)처럼 쓰지 않는다.
- reopen_condition(재개 조건): run348C/MT5 probe(348C/MT5 탐침)에서 실제 거래 KPI(거래 핵심 성과 지표)가 확인되거나 long OOS label source(롱 표본외 라벨 원천)가 보강될 때.
- evidence(근거): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348B/review_findings.csv`

## 2026-06-01 run348C Runtime Boundary Memory(런타임 경계 기억)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- constraint(제약): feature count(피처 수) `53` vs MT5 v2 contract(MT5 v2 계약) `58`.
- constraint(제약): cash_open_regime_allocator(현금장 국면 배분기)는 현재 EA(`Expert Advisor`, 전문가 자문)에서 partial mapping(부분 매핑)이다.
- effect(효과): run348D(348D 실행)의 MT5 result(MT5 결과)는 반드시 이 경계를 감안해 proxy-MT5 diff(프록시-MT5 차이)로 읽어야 한다.
- evidence(근거): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/feature_order_contract.csv`, `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/runtime_mapping_audit.csv`

## 2026-06-01 run348C Runtime Boundary Memory(런타임 경계 기억)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- constraint(제약): feature count(피처 수) `53` vs MT5 v2 contract(MT5 v2 계약) `58`.
- constraint(제약): cash_open_regime_allocator(현금장 국면 배분기)는 현재 EA(`Expert Advisor`, 전문가 자문)에서 partial mapping(부분 매핑)이다.
- effect(효과): run348D(348D 실행)의 MT5 result(MT5 결과)는 반드시 이 경계를 감안해 proxy-MT5 diff(프록시-MT5 차이)로 읽어야 한다.
- evidence(근거): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/feature_order_contract.csv`, `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/runtime_mapping_audit.csv`

## stage351B_proxy_weak_trade_surface

- result(결과): proxy(프록시)는 약하지만 MT5 probe(MT5 탐침) 인계는 가능하다.
- reopen_condition(재개 조건): MT5 runtime probe(MT5 런타임 탐침)가 proxy(프록시)와 다른 수익 구조를 보이거나 새 threshold/rule stack(임계값/규칙 묶음)이 생길 때 재개한다.

## 2026-06-02 run354C Existing Surface Density-Edge Failure(기존 표면 밀도-엣지 실패)

- source_run(원천 실행): `run354C_expand_proxy_filter_sweep_without_db_v1`
- failure(실패): existing probability surface(기존 확률 표면)는 hold/filter/threshold(보유기간/필터/임계값) 확장에서도 validation/OOS(검증/표본외) 순수익, 비용 압박, trade/day(일별 거래수) `3+`를 동시에 만족하지 못했다.
- evidence(근거): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/failure_memory.csv`
- salvage_value(회수 가치): best near miss(최상 근접 실패)를 다음 label/source/model family(라벨/원천/모델 계열) 설계 제약으로 사용한다.
- do_not_repeat(반복 금지): 같은 surface(표면)의 threshold-only search(임계값 전용 탐색)를 운영 후보처럼 반복하지 않는다.
- reopen_condition(재개 조건): 새 label/source/model family(라벨/원천/모델 계열) 또는 MT5 runtime diff(MT5 런타임 차이)가 생길 때.

## 2026-06-02 run356B_train_density_recovery_proxy_models_without_db_v1

- hypothesis(가설): density recovery labels(밀도 회복 라벨)이 proxy training(프록시 학습)에서 trade/day(일별 거래수) 3+와 stress net(압박 순수익)을 동시에 회복한다.
- variants_tried(시도 변형): 4 label variants(라벨 변형) x 3 model families(모델 계열) x threshold/margin/session/ADX grid(임계값/마진/세션/ADX 격자).
- failed_boundary(실패 경계): `proxy_scout_queue(프록시 탐색 대기열)`.
- why_failed(실패 이유): validation/OOS stress net, PF, density, balance(검증/표본외 압박 순수익, PF, 밀도, 균형) 동시 통과 행이 없다.
- salvage_value(회수 가치): best proxy rows(최선 프록시 행)와 ONNX parity(온엑스 동등성) 행을 다음 확장 탐색 씨앗으로 보존한다.
- reopen_condition(재개 조건): new feature/source/model or relaxed-but-recorded scout surface(새 피처/원천/모델 또는 기록된 완화 탐색 표면).
- do_not_repeat(반복 금지): 같은 label/table(라벨/표)에서 동일 grid(격자)만 반복하지 않는다.

## 2026-06-02 run356C_expand_density_recovery_proxy_training_search_without_db_v1

- hypothesis(가설): raw return regression and union heads(원시 수익률 회귀와 합집합 헤드)가 trade/day(일별 거래수) 3+와 stress net(압박 순수익)을 동시에 회복한다.
- variants_tried(시도 변형): Ridge/ExtraTrees regression(릿지/엑스트라트리 회귀), quantile/cost/ADX/session grid(분위수/비용/ADX/세션 격자), union non-overlap(합집합 비중첩).
- failed_boundary(실패 경계): proxy scout candidate queue(프록시 탐색 후보 대기열).
- why_failed(실패 이유): validation/oos(검증/표본외)에서 3+ trade/day(일별 거래수)와 positive stress KPI(양수 압박 KPI)를 동시에 만족하지 못했다.
- salvage_value(회수 가치): positive edge(양수 단서)는 trade/day(일별 거래수) 약 2 근처까지 올라왔고, dense rows(고밀도 행)는 validation(검증) 양수와 OOS(표본외) 음수 괴리를 드러냈다.
- reopen_condition(재개 조건): high-density label pivot(고밀도 라벨 전환), cost/session aware target(비용/세션 인식 타깃), 또는 MT5-aligned lifecycle label(MT5 정렬 생명주기 라벨)이 생길 때.
- do_not_repeat(반복 금지): 같은 label(라벨)에서 score threshold(점수 임계값)만 더 조이는 미세 탐색.

## 2026-06-02 run357A_branch_stage356_to_high_density_label_pivot_without_db_v1

- subject(대상): Stage356C density recovery expansion(356C 밀도 회복 확장)
- result_label(결과 라벨): `negative_memory_for_stage357_seed(357단계 씨앗용 부정 기억)`
- failure_boundary(실패 경계): validation trade/day(검증 일별 거래수) `2.4451219512195124`와 validation PF(검증 수익 팩터) `1.013945130731893`가 후보 조건을 넘지 못했다.
- salvage_value(회수 가치): OOS PF(표본외 수익 팩터) `1.0744976620172675`와 OOS net(표본외 순수익) `0.031124279379026655`는 high-density label pivot(고밀도 라벨 전환)의 seed surface(씨앗 표면)로 보존한다.
- reopen_condition(재개 조건): Stage357B(357B 실행)에서 timestamp-safe(시점 안전) label(라벨), ONNX parity(온엑스 동등성), non-overlap proxy(비중첩 프록시)로 trade/day(일별 거래수) 3+를 회복할 때.
- claim_boundary(주장 경계): `state_sync_stage_branch_user_requested_high_density_label_pivot_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-02 run359D Stage359C Runtime Probe Failure Memory(359D Stage359C 런타임 탐침 실패 기억)

- source_run(원천 실행): `run359C_review_high_density_label_pivot_mt5_probe_without_db_v1`
- failure(실패): validation positive rows(검증 양수 행) `0/2`, q05 validation net(q05 검증 순수익) `-222.41`, q05 validation max DD%(q05 검증 최대 낙폭 비율) `94.77`, q05 OOS monthly positive(q05 표본외 월별 양수) `2/7`, cost drag +0.30 survivors(추가 비용 0.30 생존 행) `0`.
- salvage_value(회수 가치): q05 OOS net(q05 표본외 순수익) `262.85`, PF(수익 팩터) `1.09`, trades(거래수) `936`, long/cash contribution(롱/현금장 기여), proxy-MT5 mismatch(프록시-MT5 불일치) `0`.
- do_not_repeat(반복 금지): OOS-only positive(표본외만 긍정)를 candidate selection(후보 선택)이나 operating promotion(운영 승격)처럼 반복하지 않는다.
- reopen_condition(재개 조건): Stage360(360단계) WFO/broad sweep(WFO/넓은 탐색)가 validation/OOS stability(검증/표본외 안정성), trade/day(일별 거래수) 3+, cost buffer(비용 완충)를 함께 회복할 때.
- claim_boundary(주장 경계): `state_sync_stage_branch_stage359_to_stage360_regime_stability_pivot_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-02 run359D Stage359C Runtime Probe Failure Memory(359D Stage359C 런타임 탐침 실패 기억)

- source_run(원천 실행): `run359C_review_high_density_label_pivot_mt5_probe_without_db_v1`
- failure(실패): validation positive rows(검증 양수 행) `0/2`, q05 validation net(q05 검증 순수익) `-222.41`, q05 validation max DD%(q05 검증 최대 낙폭 비율) `94.77`, q05 OOS monthly positive(q05 표본외 월별 양수) `2/7`, cost drag +0.30 survivors(추가 비용 0.30 생존 행) `0`.
- salvage_value(회수 가치): q05 OOS net(q05 표본외 순수익) `262.85`, PF(수익 팩터) `1.09`, trades(거래수) `936`, long/cash contribution(롱/현금장 기여), proxy-MT5 mismatch(프록시-MT5 불일치) `0`.
- do_not_repeat(반복 금지): OOS-only positive(표본외만 긍정)를 candidate selection(후보 선택)이나 operating promotion(운영 승격)처럼 반복하지 않는다.
- reopen_condition(재개 조건): Stage360(360단계) WFO/broad sweep(WFO/넓은 탐색)가 validation/OOS stability(검증/표본외 안정성), trade/day(일별 거래수) 3+, cost buffer(비용 완충)를 함께 회복할 때.
- claim_boundary(주장 경계): `state_sync_stage_branch_stage359_to_stage360_regime_stability_pivot_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-02 run359D Stage359C Runtime Probe Failure Memory(359D Stage359C 런타임 탐침 실패 기억)

- source_run(원천 실행): `run359C_review_high_density_label_pivot_mt5_probe_without_db_v1`
- failure(실패): validation positive rows(검증 양수 행) `0/2`, q05 validation net(q05 검증 순수익) `-222.41`, q05 validation max DD%(q05 검증 최대 낙폭 비율) `94.77`, q05 OOS monthly positive(q05 표본외 월별 양수) `2/7`, cost drag +0.30 survivors(추가 비용 0.30 생존 행) `0`.
- salvage_value(회수 가치): q05 OOS net(q05 표본외 순수익) `262.85`, PF(수익 팩터) `1.09`, trades(거래수) `936`, long/cash contribution(롱/현금장 기여), proxy-MT5 mismatch(프록시-MT5 불일치) `0`.
- do_not_repeat(반복 금지): OOS-only positive(표본외만 긍정)를 candidate selection(후보 선택)이나 operating promotion(운영 승격)처럼 반복하지 않는다.
- reopen_condition(재개 조건): Stage360(360단계) WFO/broad sweep(WFO/넓은 탐색)가 validation/OOS stability(검증/표본외 안정성), trade/day(일별 거래수) 3+, cost buffer(비용 완충)를 함께 회복할 때.
- claim_boundary(주장 경계): `state_sync_stage_branch_stage359_to_stage360_regime_stability_pivot_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## FM-ST360C-SIMPLE-LATE-VETO

- subject(대상): simple late veto(단순 후반 제외)
- evidence(근거): q05 no-late(후반 제외)는 OOS(표본외) net(순수익) `305.66`이지만 validation(검증) net(순수익) `-449.38`이다.
- judgment(판정): negative_report_derived_control(부정, 보고서 파생 대조)
- reopen_condition(재개 조건): WFO regime router(WFO 국면 라우터)가 validation non-negative(검증 비음수), OOS positive(표본외 양수), density >= 3(밀도 3 이상)을 만족해야 한다.

## 2026-06-02 FM-ST362C-Q05-MARGIN-GRID-DENSITY-COLLAPSE

- source_run(원천 실행): `run362C_review_q05_long_only_margin_grid_without_db_v1`
- failure(실패): p_long_floor>=0.40 margin-only tightening(p_long 하한 0.40 이상 마진 단독 조임)은 validation/OOS cost positive(검증/표본외 비용 양수)와 density >= 3(밀도 3 이상)를 동시에 회복하지 못했다.
- salvage_value(회수 가치): validation-derived margin rank near miss(검증 파생 마진 순위 근접 실패)는 Stage363(363단계) lower-floor/rank surface(낮은 하한/순위 표면)의 씨앗이다.
- do_not_repeat(반복 금지): sparse cost-positive pocket(희소 비용 양수 구간)을 candidate selection(후보 선택)으로 올리지 않는다.
- reopen_condition(재개 조건): Stage363B(363B 실행)가 validation/OOS cost positive(검증/표본외 비용 양수)와 density >= 3(밀도 3 이상)를 동시에 만들 때.
- evidence(근거): `stages/362_long_only_margin_grid__cost_buffer_first_branch/02_runs/run362C/review_findings.csv`

## 2026-06-02 FM-ST363B-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF

- source_run(원천 실행): `run363B_materialize_q05_lower_floor_rank_surface_without_db_v1`
- failure(실패): lower-floor/rank surface(낮은 하한/순위 표면)는 비용 양수 구간을 만들었지만 validation/OOS(검증/표본외) density >= 3(밀도 3 이상)을 동시에 만족하지 못했다.
- salvage_value(회수 가치): sparse cost-positive variants(희소 비용 양수 변형)는 regime/label/source pivot(국면/라벨/원천 전환)의 설명 변수로 보존한다.
- do_not_repeat(반복 금지): lower-floor/rank threshold(낮은 하한/순위 임계값)만 더 조이는 미세 탐색을 후보 선택처럼 반복하지 않는다.
- reopen_condition(재개 조건): 새 regime/label/source(국면/라벨/원천)가 density(밀도)와 cost stress(비용 압박)를 같이 회복할 때.
- evidence(근거): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363B/lower_floor_rank_failure_attribution.csv`

## 2026-06-02 FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF

- source_run(원천 실행): `run363C_review_q05_lower_floor_rank_surface_without_db_v1`
- failure(실패): lower-floor/rank surface(낮은 하한/순위 표면)는 cost-positive sparse rows(비용 양수 희소 행)를 만들었지만 density >= 3(밀도 3 이상)을 동시에 만족하지 못했다.
- salvage_value(회수 가치): sparse cost-positive variants(희소 비용 양수 변형), open-hour clue(진입 시간 단서), dense control failure(고밀도 대조 실패).
- do_not_repeat(반복 금지): lower-floor/rank threshold micro-tuning(낮은 하한/순위 임계값 미세조정)을 후보 선택처럼 반복하지 않는다.
- reopen_condition(재개 조건): timestamp-safe context/regime/label source(시점 안전 문맥/국면/라벨 원천)가 density >= 3(밀도 3 이상)과 cost positive(비용 양수)를 같이 만든다.
- evidence(근거): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363C/review_findings.csv`.

## 2026-06-02 FM-ST364C-TIMESTAMP-CONTEXT-MONTH-FRAGILITY

- source_run(원천 실행): `run364C_review_timestamp_context_cost_surface_without_db_v1`
- failure_memory(실패 기억): timestamp context pass rows(시점 문맥 통과 행)는 split net(분할 순수익)은 양수지만 monthly positive coverage(월별 양수 커버리지)가 약하다.
- best_seed_status(최선 씨앗 상태): validation positive months(검증 양수 월) `3/9`, OOS positive months(표본외 양수 월) `3/7`.
- do_not_repeat(반복 금지): 이 상태를 promotion candidate(승격 후보)나 runtime authority(런타임 권위)로 과장하지 않는다.
- reopen_condition(재개 조건): `run364D_materialize_timestamp_context_training_seed_without_db_v1`가 WFO/month stability(WFO/월 안정성)를 개선하고 MT5 runtime probe(MT5 런타임 탐침)로 재확인한다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364C/monthly_stability.csv`.

## 2026-06-02 FM-ST364H-SPARSE-RUNTIME-TAPE-NEGATIVE-MT5-KPI

- source_run(원천 실행): `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- failure(실패): MT5 net_profit(순수익) `-230.65`, PF(수익 팩터) `0.78`, trade_count(거래수) `66`, closed_trades_per_business_day(영업일당 종료 거래) `0.47482`.
- salvage_value(회수 가치): proxy-MT5 parity(프록시-MT5 동등성)는 matched_rows(일치 행) `472`, mismatch_rows(불일치 행) `0`로 좋다.
- do_not_repeat(반복 금지): 같은 sparse event tape(희소 이벤트 테이프)의 threshold-only search(임계값 전용 탐색)를 반복하지 않는다.
- reopen_condition(재개 조건): dense M5 source(고밀도 M5 원천), calendar exit semantics(캘린더 청산 의미), session/regime router(세션/국면 라우터)가 trade/day 3+와 MT5 순수익 양수를 동시에 만들 때.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/failure_memory.csv`.

## FM-ST364I-COST-FILTER-DENSE-OOS-WEAK

- run_id(실행 ID): `run364I_design_dense_m5_runtime_repair_proxy_without_db_v1`
- failed_boundary(실패 경계): `proxy_prefilter_strict_cross_split_success(프록시 선별 엄격 교차 분할 성공)`
- why_failed(실패 이유): dense source(고밀도 원천)는 회복됐지만 run364E cost filter(비용 필터)의 OOS profit factor(표본외 수익 팩터)가 약했다.
- salvage_value(회수 가치): dense M5 source(고밀도 M5 원천), calendar exit semantics(캘린더 청산 의미), no-split simulator(비분할 시뮬레이터)는 다음 탐색에 재사용한다.
- reopen_condition(재개 조건): direct dense M5 ONNX scout(직접 고밀도 M5 ONNX 탐색) 또는 MT5 dense flat tape(고밀도 flat 테이프)에서 PF>=1.05와 trade/day>=3이 같이 나온다.
- do_not_repeat(반복 금지): sparse long trade table(희소 롱 거래표)에만 cost filter(비용 필터)를 얹어 운영 후보처럼 말하지 않는다.

## run364J Direct Dense M5 ONNX Scout No Strict Candidate(364J 직접 고밀도 5분봉 온엑스 탐색 엄격 후보 없음)

Action(행동): direct dense M5 ONNX scout(직접 고밀도 5분봉 온엑스 탐색)를 strict cost-density gate(엄격 비용-밀도 게이트)로 닫았다.

Effect(효과): 다음 작업은 failure memory(실패 기억)를 이용해 새 offensive seed(공격 씨앗)를 고른다. 아이디어 사망(idea dead, 아이디어 사망)은 아니다.

## run364K Direct Dense M5 Density Bottleneck Failure Memory(364K 직접 고밀도 5분봉 밀도 병목 실패 기억)

Action(행동): run364J(364J 실행)의 strict_candidate_rows(엄격 후보 행) `0`개를 확인하고 failure memory(실패 기억)를 남겼다.

Effect(효과): h24 fixed-hold(24봉 고정 보유)는 high-density claim(고밀도 주장)에 반복 사용하지 않고, h6 density row(6봉 밀도 행)는 validation stability repair(검증 안정성 수리) 조건으로 재개한다.

## run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1

- failed_boundary(실패 경계): PF>=1.30 and density>=3/day without trade splitting(PF 1.30 이상과 하루 3회 이상, 거래 쪼개기 없음).
- why_failed(실패 이유): density-safe(밀도 안전) 행은 PF/DD(수익 팩터/낙폭)가 약하고 PF-pass(PF 통과) 행은 density(밀도)가 부족했다.
- salvage_value(회수 가치): hold6 density(6봉 보유 밀도), sparse PF-pass(희소 PF 통과), threshold edge DD(임계값 경계 DD)를 다음 입력으로 보존한다.
- reopen_condition(재개 조건): PF>=1.30과 density>=3/day가 같은 row grain(행 단위)에서 동시 통과한다.

## run364AQ_review_hold6_pf_dd_repair_offensive_scout_without_db_v1

- negative_result(부정 결과): strict_pass_rows(엄격 통과 행) 0, package_candidate_rows(패키지 후보 행) 0.
- effect(효과): MT5 runtime probe(MT5 런타임 탐침)로 승격하지 않고 PF gap(PF 간극) 수리 queue(대기열)로 낮춘다.

## run364AS_train_threshold_edge_pf_gap_repair_scout_without_db_v1

- status(상태): pending_review(검토 대기).
- action(행동): AS scout(정찰) 표면을 만들었다.
- effect(효과): strict_pass_rows(엄격 통과 행)와 selected KPI(선택 KPI)는 다음 review(검토)에서 negative/positive(부정/긍정)로 분리한다.

## run364AT_review_threshold_edge_pf_gap_repair_scout_without_db_v1

- status(상태): positive_proxy_with_runtime_missing(런타임 누락이 있는 긍정 프록시).
- failure_memory(실패 기억): month-side negative rows(월/방향 음수 행) `10`개와 MT5 runtime evidence(MT5 런타임 근거) 부재.
- effect(효과): 다음 run(실행)은 runtime probe(런타임 탐침)와 비용 압박 검토를 반드시 수행해야 한다.

## run364AW_review_threshold_edge_floor001_mt5_runtime_probe_without_db_v1

- status(상태): mixed_positive_runtime_probe_promotion_ineligible(혼합 긍정 런타임 탐침, 승격 부적격).
- blocker(차단 사유): actual trade density(실제 거래 밀도) `2.9159159159` < 3/day(일 3회), long/short(롱/숏) `887/84`, equity DD(수익곡선 낙폭) `17.51%`.
- effect(효과): positive clue(긍정 단서)는 폐기하지 않고 `run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1` 수리 입력으로 넘긴다.

## run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1

- status(상태): materialized_repair_inputs_no_authority(수리 입력 물질화, 권위 없음).
- failure memory(실패 기억): AW actual MT5 density(AW 실제 MT5 밀도) `2.9159159159` < 3/day(일 3회), long share(롱 비중) `0.9134912461`, DD(낙폭) `17.51`%.
- effect(효과): 같은 blocker(차단 원인)를 반복하지 않고, AY scout(스카우트)의 제약과 비교축으로 바꾼다.

## run364AY_train_threshold_edge_density_restore_cost_session_scout_without_db_v1

- status(상태): pending_review(검토 대기).
- action(행동): AY proxy surface(AY 프록시 표면)를 만들었다.
- effect(효과): negative/positive(부정/긍정) 판정은 `run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1`에서 MT5 package(MT5 패키지) 가능성과 분리해 결정한다.

## run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1

- status(상태): no_package_eligible_rows(패키지 가능 행 0).
- action(행동): MT5 package(MT5 패키지)를 열지 않았다.
- effect(효과): 운영 주장을 막고 BA materialization(BA 물질화)로 수익 원천 탐색을 계속한다.

## run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1

- status(상태): materialization_only(물질화만).
- action(행동): BB scout(BB 스카우트) 입력을 만들었다.
- effect(효과): 아직 MT5 package(MT5 패키지)나 operating promotion(운영 승격)은 없다.

## run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1

- status(상태): pending_review(검토 대기).
- action(행동): BB proxy surface(BB 프록시 표면)를 만들었다.
- effect(효과): negative/positive(부정/긍정) 판정은 `run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1` review(검토)에서 package eligibility(패키지 가능성)와 분리해 결정한다.

## run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1

- status(상태): package_opened_no_authority(패키지 열림, 권위 없음).
- action(행동): package candidate(패키지 후보) 외 실패/구현 필요 행을 failure memory(실패 기억)로 남겼다.
- effect(효과): 좋은 후보만 기억하지 않고 실패 제약도 다음 패키지에 같이 넘긴다.

- run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1: package_only_no_authority(패키지 전용, 권위 없음). Effect(효과): 실행 전 operating claim(운영 주장)을 막는다.

## run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1

- status(상태): materialized_forward_regime_stress_inputs_no_authority(전진/국면 압박 입력 물질화, 권위 없음).
- failure_memory(실패 기억): forward pass(전진 통과) 없음, long share(롱 비중) `0.9025590551`, drawdown(낙폭) `18.3`%.
- effect(효과): 같은 차단 원인을 반복 보고하지 않고 BH scout(BH 스카우트)의 비교축으로 바꾼다.

## run364BH_train_density_restore_forward_regime_stress_scout_without_db_v1

- status(상태): density-breaking repairs rejected(밀도 붕괴 수리 거절).
- failure_memory(실패 기억): month/hour hard delete(월/시간 강한 삭제)는 PF를 올려도 trade density(거래 밀도)를 3/day 아래로 깎는다.
- effect(효과): 다음 작업은 hard delete(강한 삭제)보다 micro margin guard(미세 margin 가드)나 new short source(새 숏 원천)에 집중한다.

<!-- run364BI_density_breaking_repairs -->
- Negative memory(부정 기억): exact month/hour hard filters(정확 월/시간 강한 필터)는 density(밀도) < 3/day로 이번 경로에서 rejected(거절). Effect(효과): 같은 삭제식 수리를 운영 후보로 끌고 가지 않는다.

## run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1

- status(상태): materialization_only_no_authority(물질화 전용, 권위 없음).
- failure memory(실패 기억): long deletion(롱 삭제)만으로 short target(숏 목표)을 맞추려면 `181`건 제거가 필요하지만 density removable budget(삭제 가능 밀도 여유)은 `7`건뿐이다.
- effect(효과): 같은 blocker(차단 원인)를 반복하지 않고 new short source(새 숏 원천) 탐색 제약으로 바꾼다.

## run364BM_train_h19_stress_short_balance_proxy_scout_without_db_v1

- status(상태): proxy_only_review_required(프록시 전용, 검토 필요).
- failure_memory(실패 기억): synthetic fixed6 label(합성 고정6봉 라벨)과 same-tape threshold(동일 테이프 임계값)는 MT5 runtime evidence(MT5 런타임 근거)를 대체하지 못한다.
- effect(효과): BN review(BN 검토)에서 packageability(패키지 가능성)와 MT5 reprobe(MT5 재탐침)를 먼저 확인한다.

## run364BN_review_h19_stress_short_balance_proxy_scout_without_db_v1

- status(상태): BM package candidate rejected(BM 패키지 후보 거절).
- failure_memory(실패 기억): BM selected synthetic short PF(합성 숏 수익 팩터) `0.8733691583`라서 combined proxy(합산 프록시)만으로 패키지하면 안 된다.
- effect(효과): next run(다음 실행)은 standalone short source quality(숏 원천 단독 품질)를 먼저 수리한다.

## run364BO_train_short_source_quality_repair_scout_without_db_v1

- status(상태): package not opened(패키지 열지 않음).
- failure_memory(실패 기억): broad pool negative control(넓은 풀 부정 대조)은 hard pass(하드 통과)를 만들지 못했고, selected proxy(선택 프록시)는 month stress(월 압박)가 남았다.
- effect(효과): 다음 검토는 프록시 단서를 보존하되 MT5 package(MT5 패키지)로 바로 올리지 않는다.

## run364BP_review_short_source_quality_repair_scout_without_db_v1

- status(상태): BO package rejected(BO 패키지 거절).
- failure_memory(실패 기억): selected proxy(선택 프록시)는 month_bad_count(월 나쁨 수) `2`이고 MT5 reprobe(MT5 재탐침)가 없다.
- effect(효과): package(패키지)가 아니라 broad clean short-share lift(넓은 클린 숏 비중 보강) 제약으로 넘긴다.

## run364BQ_train_broad_clean_short_share_lift_scout_without_db_v1

- status(상태): package not opened(패키지 열지 않음).
- failure_memory(실패 기억): selected proxy(선택 프록시)는 month_bad_count(월 나쁨 수) `1`이고 MT5 reprobe(MT5 재탐침)가 없다.
- salvage_value(회수 가치): short share(숏 비중) 목표와 PF(수익 팩터) 목표는 동시에 통과했다.
- reopen_condition(재개 조건): `run364BR_review_broad_clean_short_share_lift_scout_without_db_v1`에서 월 압박 원인과 proxy/MT5 diff(프록시/MT5 차이)를 닫는다.

## run364BS_train_late_year_short_share_stress_repair_scout_without_db_v1

- status(상태): package not opened(패키지 열지 않음).
- failure_memory(실패 기억): proxy stress clear(프록시 압박 해소)가 있어도 MT5 reprobe(MT5 재탐침)와 BT review(BT 검토)가 없으면 operating claim(운영 주장)이 아니다.
- salvage_value(회수 가치): `bs02_late_year_parent_session_suppress__moy12__h21__side_long`는 late-year/session repair(연말/세션 수리) 후보로 검토 가치가 있다.
- reopen_condition(재개 조건): `run364BT_review_late_year_short_share_stress_repair_scout_without_db_v1`에서 overfit watch(과적합 관찰)와 proxy/MT5 diff(프록시/MT5 차이)를 닫는다.

<!-- run364BU_synthetic_short_source_blocker -->
- Blocker memory(차단 기억): `run364BU_prepare_late_year_session_gate_mt5_precheck_without_db_v1` could not run exact MT5 precheck(정확 MT5 사전점검) because synthetic short source runtime support(합성 숏 원천 런타임 지원)가 missing(누락)이다. Effect(효과): 다음 작업은 같은 외부 검증 누락을 말로만 반복하지 않고 source materialization(원천 물질화) 또는 rejection(거절)을 해야 한다.

## run364CG_train_cost_stable_h17_source_guard_offensive_scout_without_db_v1

- status(상태): no operating package yet(아직 운영 패키지 없음).
- failure_memory(실패 기억): h17 floor tightening(17시 하한 강화), overlay-only stress(오버레이 전용 압박), and short-floor variants(숏 하한 변형)는 net/PF or short balance(순수익/PF 또는 숏 균형)를 흔들었다.
- salvage_value(회수 가치): `cg09_best_open_hour_overlay_focus`는 small lift(작은 우위)와 short floor(숏 하한)를 같이 보존한다.
- reopen_condition(재개 조건): CH review(CH 검토)가 month/source/cost stress(월/원천/비용 압박)를 통과하고 MT5 reprobe(MT5 재탐침)가 열릴 때.

## run364CH_review_cost_stable_h17_source_guard_offensive_scout_without_db_v1

- status(상태): CG h17 focus package rejected(CG 17시 집중 패키지 거절).
- failure_memory(실패 기억): bad months(나쁜 월) `['2025-08', '2025-12']`, cost stress delta(비용 압박 차이) `-1.13`, MT5 reprobe missing(MT5 재탐침 없음).
- salvage_value(회수 가치): h17 focus(17시 집중)와 synthetic_short_overlay(합성 숏 오버레이)는 CI repair seed(CI 수리 씨앗)로 남긴다.
- reopen_condition(재개 조건): `run364CI_materialize_h17_focus_month_cost_stress_repair_inputs_without_db_v1`가 stress_adjusted_net_delta>=0(압박 조정 순수익 차이 0 이상), density>=3(밀도 3 이상), short_count>=100(숏 100개 이상)을 동시에 만든다.

<!-- run364CJ__boundary__run364CJ_train_h17_focus_month_cost_stress_repair_scout_without_db_v1 -->
- `run364CJ_train_h17_focus_month_cost_stress_repair_scout_without_db_v1` boundary note(경계 메모): proxy scout(프록시 정찰) did not run new MT5(새 MT5 미실행), so runtime authority(런타임 권위) and operating promotion(운영 승격) remain not claimed(주장 안 함).

<!-- run364CK__run364CK_review_h17_focus_month_cost_stress_repair_scout_without_db_v1 -->
- `run364CK_review_h17_focus_month_cost_stress_repair_scout_without_db_v1` package rejection(패키지 거절): bad months(손실 월) `2025-08;2025-12` remain despite positive proxy KPI(긍정 프록시 KPI). Reopen condition(재개 조건): `run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1` creates bad_month_count_zero(손실 월 0) without exact-date filtering(정확 날짜 필터 없음).

<!-- run364CL__run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1 -->
- `run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1` preserves CK package rejection(CK 패키지 거절 보존): bad months(손실 월) `2025-08;2025-12` remain unresolved until `run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1` replay(재생). Reopen condition(재개 조건): bad_month_count==0 and stress_delta>=0 without top_n/trade splitting/exact-year date filter(top_n/거래 쪼개기/정확 연도 날짜 필터 없이 손실 월 0 및 압박 차이 0 이상).

<!-- run364CM__boundary__run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1 -->
- `run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1` boundary note(경계 메모): proxy scout(프록시 정찰) produced bad_month_count_zero(손실 월 0) but did not run new MT5(새 MT5 미실행), so runtime authority(런타임 권위) and operating promotion(운영 승격) remain not claimed(주장 안 함). Reopen condition(재개 조건): `run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1` reviews package gate(패키지 게이트) and MT5 reprobe boundary(MT5 재탐침 경계).

<!-- run364CN__run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1 -->
- `run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1` residual risk(잔여 위험): weakest months(약한 월) `2025-12` net `2.66` and synthetic overlay(합성 오버레이) thin sample(얇은 표본). Reopen condition(재개 조건): `run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1` or later MT5 probe(MT5 탐침)가 proxy/MT5 diff(프록시/MT5 차이)를 불리하게 보이면 source/month guard(원천/월 가드)를 다시 연다.

<!-- run364CQ__run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1 -->
- `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`: Not invalid(무효 아님), but zero bad month(손실 월 0) claim failed in MT5 because `2025-12` net `-3.97`. Reopen condition(재개 조건): MT5 month attribution(월 귀속) non-negative with density >= 3 and short floor >= 100.

<!-- run364CS__boundary__run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1 -->
- `run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1` boundary note(경계 메모): proxy scout(프록시 정찰)는 긍정 단서를 만들었지만 MT5 equity DD(MT5 수익곡선 낙폭)를 직접 증명하지 못합니다. Effect(효과): `run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1`에서 runtime probe boundary(런타임 탐침 경계)를 먼저 판단합니다.

<!-- run364CT__runtime_gap__run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1 -->
- `run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1` runtime gap(런타임 간극): cr04 proxy(프록시)는 긍정이지만 현재 EA(전문가 자문)는 piecewise month12 margin guard(구간별 12월 마진 가드)를 정확히 표현하지 못합니다. Effect(효과): cr04를 버리지 않고 `run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1`에서 도구를 먼저 수리합니다.

<!-- run364CW__run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1 -->
- `run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`: Not invalid(무효 아님), but operating claim(운영 주장)은 equity DD `130.11`, long share `0.896090535`, proxy net diff `-56.18` 때문에 닫지 않습니다. Reopen condition(재개 조건): MT5 density >= 3, short floor >= 100, month attribution non-negative(월 귀속 비음수)를 유지하며 equity DD와 side balance(방향 균형)를 개선합니다.

<!-- run364CX__run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1 -->
- `run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1`: Not invalid(무효 아님). Materialization only(구체화 전용)라 성능 개선을 주장하지 않는다. Reopen condition(재개 조건): `run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`가 density >= 3, short_count >= 100, month12 net >= 0을 보존하며 equity-risk proxy(수익곡선 위험 프록시)나 long share(롱 비중)를 개선해야 한다.

<!-- run364CY__run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1 -->
- `run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`: Not invalid(무효 아님). Proxy positive(프록시 긍정)이지만 MT5 equity DD(MT5 수익곡선 낙폭)와 EA risk-scale representation(EA 위험비율 표현)이 없어 operating claim(운영 주장)은 금지.

<!-- run364CZ__runtime_gap__run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1 -->
- `run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1` runtime gap(런타임 간극): cx05 proxy(프록시)는 긍정이지만 현재 EA(전문가 자문)는 side/hour/margin risk-scale overlay(방향/시간/마진 위험비율 오버레이)를 정확히 표현하지 못합니다. Effect(효과): 직접 MT5 package(MT5 패키지)를 막고 `run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1`에서 도구를 먼저 수리합니다.

<!-- run364DC__side_balance__run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1 -->
- `run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`: pure exposure scaling(순수 노출 증폭)은 net profit(순수익)을 올렸지만 long/short balance(롱/숏 균형)를 해결하지 못함. Effect(효과): 같은 수리만 반복하지 않고 short-source expansion(숏 원천 확장)을 다음 제약으로 둠.

<!-- run364DD__run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1 -->
- `run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1`: Not invalid(무효 아님). Proxy scout(프록시 탐색) only(전용)이므로 MT5 runtime probe(MT5 런타임 탐침) 전까지 operating claim(운영 주장) 금지.

<!-- run364DE__run364DE_review_h17_short_source_expansion_runtime_positive_scout_without_db_v1 -->
- `run364DE_review_h17_short_source_expansion_runtime_positive_scout_without_db_v1`: Not invalid(무효 아님). Existing EA lacked exact flat-margin guard(기존 EA에 정확한 flat 마진 조건 없음); operating claim(운영 주장) 금지 until MT5 probe(MT5 탐침) exists.

<!-- run364DF__run364DF_implement_h17_short_source_expansion_runtime_package_without_db_v1 -->
- `run364DF_implement_h17_short_source_expansion_runtime_package_without_db_v1`: Not invalid(무효 아님). Package only(패키지 전용); MT5 runtime output(MT5 런타임 출력) 전까지 operating claim(운영 주장) 금지.
<!-- run364DH__profit_retreat__run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1 -->
- `run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`: short-source expansion(숏 원천 확장)은 거래수 증가만으로는 충분하지 않았습니다. Net delta vs DB(DB 대비 순수익 변화) `-30.9`, PF delta(PF 변화) `-0.03`. Effect(효과): DI는 low-quality added shorts(저품질 추가 숏)를 거르는 방향으로 진행합니다.
<!-- run364DI__month_stress_boundary__run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1 -->
- `run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1`: month-stress variants(月 스트레스 변형)는 높은 proxy score(프록시 점수)를 보였지만 multi-month runtime repair(다중 월 런타임 보정)와 overfit risk(과적합 위험)가 있어 selected package candidate(선택 패키지 후보)로 직접 승격하지 않았습니다. Effect(효과): 월 배제는 운영 필터가 아니라 regime clue(국면 단서)로만 남깁니다.
<!-- run364DJ__month_stress_boundary__run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1 -->
- `run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1`: month-stress(月 스트레스) variants remain regime clues(국면 단서) only; they are not selected package candidates(선택 패키지 후보 아님).
<!-- run364DK__run364DK_implement_h17_short_source_profit_recovery_runtime_package_without_db_v1 -->
- `run364DK_implement_h17_short_source_profit_recovery_runtime_package_without_db_v1`: Not invalid(무효 아님). Package only(패키지 전용); MT5 runtime output(MT5 런타임 출력) 전까지 operating claim(운영 주장) 금지.
<!-- run364DM__db_threshold_not_exceeded__run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1 -->
- `run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`: short-source profit recovery(숏 원천 수익 회복)는 DB를 아직 초과하지 못했습니다. Net delta vs DB(DB 대비 순수익 변화) `-0.67`, PF delta(PF 변화) `-0.01`. Effect(효과): DN은 PF 상승 없는 밀도 추가를 금지하고 품질 다듬기만 탐색합니다.
<!-- run364DN__no_calibrated_pf_pass__run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1 -->
- `run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1`: no parameter-only candidate(파라미터 전용 후보 없음)가 calibrated net>DB and PF>DB(보정 순수익/PF DB 초과)를 동시에 통과했습니다. Effect(효과): DO는 net-only pass(순수익만 통과)를 패키지로 과장하지 않습니다.
<!-- run364DO__parameter_only_pf_fail__run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1 -->
- `run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1`: DN parameter-only polish(DN 파라미터 전용 다듬기)는 strict calibrated DB net/PF exceedance(엄격 보정 DB 순수익/PF 초과)를 달성하지 못했습니다. Effect(효과): runtime package(런타임 패키지)를 열지 않고 새 수익 원천 탐색으로 전환합니다.
<!-- run364DP__strict_candidate_absent__run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1 -->
- `run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1`: short-source model/label reseed(숏 원천 모델/라벨 재시드)는 strict cross-split contract(엄격 교차 분할 계약)를 통과하지 못했습니다. Effect(효과): DQ는 OOS-only clue(표본외 전용 단서)를 package(패키지)로 과장하지 않습니다.
<!-- run364DQ__density_below_min__run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1 -->
- `run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1`: DP ONNX seed(DP ONNX 씨앗)는 density below 3/day(일 3회 미만 밀도)라 runtime package(런타임 패키지)로 열지 않았습니다. Effect(효과): OOS-only low-density clue(OOS 전용 저밀도 단서)를 운영 후보로 과장하지 않습니다.
<!-- run364DR__strict_candidate_absent__run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1 -->
- `run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1`: density/PF bridge(밀도/PF 브리지)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. density_both_count(양쪽 밀도 통과 수)는 `2013`지만 density_and_net_count(양쪽 밀도+순수익 통과 수)는 `0`입니다. Effect(효과): 밀도만 올리는 경로를 반복하지 않습니다.
<!-- run364DS__density_bridge_failed__run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1 -->
- `run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1`: DR density/PF bridge(DR 밀도/PF 브리지)는 package rejected(패키지 거절)입니다. density_both_count(양쪽 밀도 통과 수) `2013` 중 density_and_net_count(양쪽 밀도+순수익 통과 수)는 `0`입니다. Effect(효과): DP score bridge(DP 점수 브리지)만 넓히는 반복을 멈춥니다.
<!-- run364DT__strict_candidate_absent__run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1 -->
- `run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1`: regime/behavior reseed(국면/현상 재시드)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): DU에서 OOS clue(표본외 단서)와 validation failure(검증 실패)를 분리 검토합니다.
<!-- run364DU__validation_failure__run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1 -->
- `run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1`: regime/behavior reseed(국면/현상 재시드)는 validation net/PF(검증 순수익/PF) 실패로 package rejected(패키지 거절)입니다. Effect(효과): OOS-only success(OOS 전용 성공)를 운영 근거로 쓰지 않습니다.
<!-- run364DV__strict_candidate_absent__run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1 -->
- `run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1`: validation-stability reseed(검증 안정성 재시드)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): DW에서 실패 기억과 재사용 단서를 분리 검토합니다.
<!-- run364DW__density_below_objective__run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1 -->
- `run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1`: DV validation-stability model(DV 검증 안정성 모델)은 density below 3/day(일 3회 미만 밀도)로 package rejected(패키지 거절)입니다. Effect(효과): 높은 PF를 낮은 거래수 모델로 과장하지 않습니다.
<!-- run364DX__strict_candidate_absent__run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1 -->
- `run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1`: density recovery reseed(밀도 회복 재시드)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): DY에서 수익/밀도 tradeoff(절충)를 분리 검토합니다.
<!-- run364DY__oos_pf_net_failed__run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1 -->
- `run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1`: DX density recovery(DX 밀도 회복)는 OOS net/PF failure(표본외 순수익/PF 실패)로 package rejected(패키지 거절)입니다. Effect(효과): 검증 전용 밀도 회복을 운영 근거로 쓰지 않습니다.
<!-- run364DZ__strict_candidate_absent__run364DZ_train_h17_density_pf_balance_reseed_without_db_v1 -->
- `run364DZ_train_h17_density_pf_balance_reseed_without_db_v1`: density/PF balance reseed(밀도/PF 균형 재시드)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): EA review(EA 검토)에서 실패 기억과 재사용 단서를 분리합니다.
<!-- run364EA__validation_pf_floor__run364EA_review_h17_density_pf_balance_reseed_without_db_v1 -->
- `run364EA_review_h17_density_pf_balance_reseed_without_db_v1`: DZ는 OOS(표본외)는 회복했지만 validation PF(검증 수익 팩터)가 `1.0038126802`라 package(패키지)로 열 수 없습니다. Effect(효과): EB는 검증 PF 바닥을 직접 제약으로 씁니다.
<!-- run364EB__strict_candidate_absent__run364EB_train_h17_validation_pf_floor_density_recovery_reseed_without_db_v1 -->
- `run364EB_train_h17_validation_pf_floor_density_recovery_reseed_without_db_v1`: validation PF floor density recovery(검증 PF 바닥 밀도 회복)가 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): EC review(EC 검토)에서 salvage value(회수 가치)와 reopen condition(재개 조건)을 분리합니다.
<!-- run364EC__dual_pf_floor__run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1 -->
- `run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1`: EB는 density_net_count(밀도+순수익 후보 수) `144`를 만들었지만 pf110_count(PF 1.10 양쪽 통과 수)는 `0`입니다. Effect(효과): ED는 min_pf(최소 PF)를 직접 보상합니다.
<!-- run364ED__strict_candidate_absent__run364ED_train_h17_dual_pf_floor_bridge_reseed_without_db_v1 -->
- `run364ED_train_h17_dual_pf_floor_bridge_reseed_without_db_v1`: strict dual PF floor(엄격 양쪽 PF 바닥) 후보 수는 `0`입니다. Effect(효과): EE review(EE 검토)에서 scout(스카우트) 가치와 다음 공격 씨앗을 분리합니다.
<!-- run364EE__dual_pf_floor_bridge_failed__run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1 -->
- `run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1`: ED selected min_pf(선택 최소 PF) `1.0219124076`, pf110_count `0`라 package(패키지)를 열지 않습니다. Effect(효과): 직접 min_pf 격자 반복을 피하고 EF 원천 회전으로 넘깁니다.
<!-- run364EF__strict_candidate_absent__run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1 -->
- `run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1`: strict candidate(엄격 후보)는 `0`입니다. Effect(효과): EG review(EG 검토)에서 PF bridge(수익 팩터 연결) 정도와 다음 씨앗을 분리합니다.
<!-- run364EG__pf108_bridge_missing__run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1 -->
- `run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1`: EF pf108_count(PF 1.08 양쪽 통과 수) `0`라 package(패키지)를 열지 않습니다. Effect(효과): EH는 OOS PF 1.08 연결을 밀도 보존과 함께 탐색합니다.
<!-- run364EH__strict_candidate_absent__run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1 -->
- `run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1`: strict candidate(엄격 후보)는 `0`입니다. Effect(효과): EI review(EI 검토)에서 PF bridge(수익 팩터 연결) 정도와 다음 씨앗을 분리합니다.
<!-- run364EI__density_floor_failed__run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1 -->
- `run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1`: EH OOS PF(표본외 PF) `1.2623046122`는 좋지만 density(밀도)가 `2.9344262295` / `2.8320610687`라 package(패키지)를 열지 않습니다. Effect(효과): EJ는 밀도 바닥 회수를 먼저 봅니다.
<!-- run364EJ__oos112_density_absent__run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1 -->
- `run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1`: OOS PF 1.12 density candidate(표본외 PF 1.12 밀도 후보)는 `0`입니다. Effect(효과): EK review(EK 검토)에서 밀도 복구 실패와 남은 PF 단서를 분리합니다.
<!-- run364EK__oos_pf_collapsed__run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1 -->
- `run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1`: selected OOS PF(선택 표본외 PF)는 `1.0183147066`이고 density_oos108_val104_count(밀도 OOS108 검증104 후보 수)는 `0`입니다. Effect(효과): package(패키지)를 열지 않고 EL 수리 조건으로 넘깁니다.
<!-- run364EM__cost_stress_caution__run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1 -->
- `run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1`: cost stress(비용 압박)는 validation cost 0.6(검증 비용 0.6)에서 실패합니다. Effect(효과): EN/MT5 probe(EN/MT5 탐침)는 비용 압박을 별도 판정 조건으로 가져갑니다.
<!-- run364EN__no_authority__run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1 -->
- `run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1`: Not invalid(무효 아님). Package only(패키지 전용); MT5 runtime output(MT5 런타임 출력) 전까지 operating claim(운영 주장) 금지.
<!-- run364EO__no_authority__run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1 -->
- `run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`: runtime probe attempt(런타임 탐침 시도)일 뿐 operating claim(운영 주장)은 없습니다.
<!-- run364EP__cost_side_no_authority__run364EP_review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1 -->
- `run364EP_review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`: positive runtime clue(긍정 런타임 단서)는 있지만 validation cost stress(검증 비용 압박), short-heavy(숏 편중), forward/replay absence(전진/재생 부재) 때문에 authority(권위) 없음. Effect(효과): 운영 주장을 막고 EQ 수리 조건으로 전환합니다.
## stage364EQ_existing_surface_strict_pass_zero

- failed boundary(실패 경계): strict operational proxy pass(엄격 운영 프록시 통과) across cost/PF/density/side/net(비용/PF/밀도/방향/순수익).
- why failed(실패 이유): existing EL surface(기존 EL 표면)는 combined net>=523.58(합산 순수익 523.58 이상), cost0.9(비용0.9), density(밀도), short share(숏 비중), PF floor(PF 바닥)를 동시에 만족하지 못했다.
- salvage value(회수 가치): model/label/feature reseed(모델/라벨/피처 재시드)로 이동.
- do-not-repeat note(반복 금지 메모): 같은 surface micro-search(표면 미세탐색)를 운영 후보처럼 반복하지 않는다.
- reopen condition(재개 조건): ER에서 full trade tape(전체 거래 테이프)와 새 cost-aware labels(비용 인식 라벨)를 만든 뒤 재평가.
<!-- run364ER__strict_candidate_absent__run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1 -->
- `run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1`: cost-side reseed(비용/방향 재시드)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): ES에서 OOS clue(표본외 단서)와 validation/cost failure(검증/비용 실패)를 분리 검토합니다.
<!-- run364ES__density_cost_short_failure__run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1 -->
- `run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1`: density>=3 and validation/OOS cost0.6 pass(밀도 3 이상과 검증/표본외 비용0.6 통과)를 동시에 만족한 row(행)가 0개라 package rejected(패키지 거절)입니다. Effect(효과): threshold micro-search(임계값 미세탐색) 반복 대신 ET에서 label/score(라벨/점수)를 다시 엽니다.
<!-- run364ET__strict_candidate_absent__run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1 -->
- `run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1`: density/cost/short balance reseed(밀도/비용/숏 균형 재시드)가 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): EU에서 실패 조건과 salvage segment(회수 구간)를 분리합니다.
<!-- run364EU__cost09_density_edge_failure__run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1 -->
- `run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1`: ET selected candidate(ET 선택 후보)는 combined density(합산 밀도) `2.9936305733`와 combined cost0.9 net(합산 비용0.9 순수익) `-111.709` 때문에 package rejected(패키지 거절)입니다. Effect(효과): OOS-only cost strength(표본외 전용 비용 강점)를 운영 근거로 쓰지 않고 EV 수리 조건으로 넘깁니다.
<!-- run364EV__strict_candidate_absent__run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1 -->
- `run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1`: cost09/density edge recovery(비용0.9/밀도 엣지 회복)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): EW에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364EW__validation_overfit_oos_collapse__run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1 -->
- `run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1`: EV selected candidate(EV 선택 후보)는 OOS net/PF(표본외 순수익/PF) `-17.382` / `0.9763940571`로 package rejected(패키지 거절)입니다. Effect(효과): validation cost09(검증 비용0.9) 단독 보상 반복을 금지합니다.
<!-- run364EX__strict_candidate_absent__run364EX_train_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1 -->
- `run364EX_train_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1`: OOS preserve cost09/short rebalance(표본외 보존 비용0.9/숏 재균형)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): EY에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364EY__pf125_cost09_gap__run364EY_review_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1 -->
- `run364EY_review_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1`: EX selected candidate(EX 선택 후보)는 OOS PF/cost0.9(표본외 수익 팩터/비용0.9) 부족으로 package rejected(패키지 거절)입니다. Effect(효과): PF 1.25와 비용0.9 간격 수리를 다음 조건으로 고정합니다.
<!-- run364EZ__strict_candidate_absent__run364EZ_train_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1 -->
- `run364EZ_train_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1`: OOS PF125 cost09 gap repair(표본외 PF 1.25 비용0.9 간격 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FA에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FA__validation_density_cost_short_collapse__run364FA_review_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1 -->
- `run364FA_review_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1`: EZ selected candidate(EZ 선택 후보)는 validation/density/combined cost/short(검증/밀도/합산 비용/숏) 붕괴로 package rejected(패키지 거절)입니다. Effect(효과): 표본외 PF 전용 선택을 금지하고 밀도 3/day(일 3회) 회복을 다음 조건으로 고정합니다.
<!-- run364FB__strict_candidate_absent__run364FB_train_h17_oos108_pf125_density_bridge_repair_without_db_v1 -->
- `run364FB_train_h17_oos108_pf125_density_bridge_repair_without_db_v1`: PF125 density bridge repair(PF125 밀도 연결 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FC에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FC__pf125_short_cost09_gap__run364FC_review_h17_oos108_pf125_density_bridge_repair_without_db_v1 -->
- `run364FC_review_h17_oos108_pf125_density_bridge_repair_without_db_v1`: FB selected candidate(FB 선택 후보)는 OOS PF/cost0.9/short share(표본외 PF/비용0.9/숏 비중) 간격으로 package rejected(패키지 거절)입니다. Effect(효과): 밀도 3/day(일 3회)를 보존하면서 숏/비용 균형 수리를 다음 조건으로 고정합니다.
<!-- run364FD__strict_candidate_absent__run364FD_train_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1 -->
- `run364FD_train_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1`: PF125 short/cost09 balance repair(PF125 숏/비용0.9 균형 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FE에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FE__density_reloss__run364FE_review_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1 -->
- `run364FE_review_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1`: FD selected candidate(FD 선택 후보)는 validation/combined density(검증/합산 밀도) 재손실로 package rejected(패키지 거절)입니다. Effect(효과): 표본외 PF/비용0.9 보존과 밀도 재결합을 다음 조건으로 고정합니다.
<!-- run364FF__strict_candidate_absent__run364FF_train_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1 -->
- `run364FF_train_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1`: PF125 density rejoin cost09 short guard(PF125 밀도 재결합 비용0.9 숏 가드)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FG에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FG__density_profit_failure__run364FG_review_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1 -->
- `run364FG_review_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1`: FF selected candidate(FF 선택 후보)는 validation/combined density(검증/합산 밀도)와 validation cost(검증 비용)가 부족해 package rejected(패키지 거절)입니다. Effect(효과): 표본외 PF/비용 단서는 보존하고 검증 밀도 수익 실패를 다음 조건으로 고정합니다.
<!-- run364FH__strict_candidate_absent__run364FH_train_h17_oos108_pf125_validation_density_profit_repair_without_db_v1 -->
- `run364FH_train_h17_oos108_pf125_validation_density_profit_repair_without_db_v1`: validation density profit repair(검증 밀도 수익 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FI에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FI__oos_pf_cost_reloss__run364FI_review_h17_oos108_pf125_validation_density_profit_repair_without_db_v1 -->
- `run364FI_review_h17_oos108_pf125_validation_density_profit_repair_without_db_v1`: FH selected candidate(FH 선택 후보)는 OOS PF(표본외 수익 팩터) `1.1853206259`, OOS cost0.9(표본외 비용0.9) `-61.113`, combined cost0.9(합산 비용0.9) `-281.932` 때문에 package rejected(패키지 거절)입니다. Effect(효과): 검증 밀도 회복만으로 운영 후보를 만들지 않습니다.
<!-- run364FJ__strict_candidate_absent__run364FJ_train_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1 -->
- `run364FJ_train_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1`: OOS density preserve repair(표본외 밀도 보존 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FK에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FK__density_reloss__run364FK_review_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1 -->
- `run364FK_review_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1`: FJ selected candidate(FJ 선택 후보)는 OOS PF(표본외 수익 팩터) `1.4709758917`와 OOS cost0.9(표본외 비용0.9) `132.92`를 회복했지만 density(밀도)가 `2.131147541` / `2.5496183206` / `2.3057324841`라 package rejected(패키지 거절)입니다. Effect(효과): PF만 좋은 저밀도 후보를 운영 후보로 올리지 않습니다.
<!-- run364FL__strict_candidate_absent__run364FL_train_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1 -->
- `run364FL_train_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1`: dual density OOS cost bridge(양쪽 밀도 표본외 비용 연결)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FM에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FM__oos_cost_reloss__run364FM_review_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1 -->
- `run364FM_review_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1`: FL selected candidate(FL 선택 후보)는 density3(밀도3)는 회복했지만 OOS PF(표본외 수익 팩터) `1.0477871778`와 OOS cost0.9(표본외 비용0.9) `-198.611` 때문에 package rejected(패키지 거절)입니다. Effect(효과): 밀도만 좋은 저수익 후보를 운영 후보로 올리지 않습니다.
<!-- run364FN__strict_candidate_absent__run364FN_train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1 -->
- `run364FN_train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1`: density cost decoupled bridge(밀도 비용 분리 연결)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FO에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FO__density_pf_overlap_absent__run364FO_review_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1 -->
- `run364FO_review_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1`: strict_candidate_count(엄격 후보 수) `0`, density3_all_splits_oos_pf105_count(전 분할 밀도3과 표본외 PF105 동시 수) `0`, oos_pf125_cost09_density3_count(표본외 PF125/비용0.9/밀도3 동시 수) `0`로 package rejected(패키지 거절)입니다. Effect(효과): 저밀도 수익 후보를 운영 후보로 올리지 않습니다.
<!-- run364FP__strict_candidate_absent__run364FP_train_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1 -->
- `run364FP_train_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1`: positive density floor reseed(양수 밀도 바닥 재시드)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FQ에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FQ__positive_density_absent__run364FQ_review_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1 -->
- `run364FQ_review_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1`: validation_positive_density3_count(검증 양수 밀도3 수) `0`, density3_all_splits_valpos_oospos_count(전 분할 양수 밀도3 수) `0`, strict_candidate_count(엄격 후보 수) `0`로 package rejected(패키지 거절)입니다. Effect(효과): 저밀도 비용 후보를 운영 후보로 올리지 않습니다.
<!-- run364FR__strict_candidate_absent__run364FR_train_h17_oos108_pf125_density3_regime_split_repair_without_db_v1 -->
- `run364FR_train_h17_oos108_pf125_density3_regime_split_repair_without_db_v1`: density3 regime split repair(밀도3 국면 분할 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FS에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FS__profit_salvage_density_lost__run364FS_review_h17_oos108_pf125_density3_regime_split_repair_without_db_v1 -->
- `run364FS_review_h17_oos108_pf125_density3_regime_split_repair_without_db_v1`: selected validation net(선택 검증 순수익) `188.314`, combined net(합산 순수익) `181.752`이지만 density3_all_splits_count(전 분할 밀도3 수) `0`로 package rejected(패키지 거절)입니다. Effect(효과): 낮은 거래수 수익 후보를 운영 후보로 올리지 않습니다.
<!-- run364FT__strict_candidate_absent__run364FT_train_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1 -->
- `run364FT_train_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1`: regime profit density reexpand(국면 수익 밀도 재확장)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FU에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FU__density_recovered_profit_failed__run364FU_review_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1 -->
- `run364FU_review_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1`: density3(밀도3)는 `246`행으로 회복됐지만 OOS profit(표본외 수익)이 실패했습니다. Effect(효과): FV에서 density3를 보존하고 OOS net/PF를 직접 수리합니다.
<!-- run364FV__strict_candidate_absent__run364FV_train_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1 -->
- `run364FV_train_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1`: density3 OOS profit bridge(밀도3 표본외 수익 연결)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FW에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FW__oos_profit_recovered_density_lost__run364FW_review_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1 -->
- `run364FW_review_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1`: OOS profit(표본외 수익)은 회복됐지만 density3(밀도3)가 `0`행으로 사라졌습니다. Effect(효과): FX에서 FT 밀도 앵커와 FV 수익 앵커를 재결합합니다.
<!-- run364FX__strict_candidate_absent__run364FX_train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1 -->
- `run364FX_train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1`: profit density dual anchor rejoin(수익 밀도 이중 앵커 재결합)은 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FY에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364FY__density_recovered_oos_profit_failed__run364FY_review_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1 -->
- `run364FY_review_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1`: density3(밀도3)는 `162`행으로 회복됐지만 OOS profit(표본외 수익)이 실패했습니다. Effect(효과): FZ에서 밀도-수익 충돌을 재혼합합니다.
<!-- run364FZ__strict_candidate_absent__run364FZ_train_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1 -->
- `run364FZ_train_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1`: density profit conflict reblend(밀도 수익 충돌 재혼합)은 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GA에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364GA__conflict_reblend_worse__run364GA_review_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1 -->
- `run364GA_review_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1`: density profit conflict reblend(밀도 수익 충돌 재혼합)는 selected OOS net/PF(선택 표본외 순수익/수익 팩터) `-107.009` / `0.8470401907`와 density(밀도) `2.7103825137/2.786259542/2.7420382166`로 실패했습니다. Effect(효과): GB에서 세션/방향 손실 군집을 차단합니다.
<!-- run364GB__strict_candidate_absent__run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1 -->
- `run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1`: session side loss veto rescue(세션 방향 손실 차단 회수)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GC에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364GC__profit_recovered_density_cost_failed__run364GC_review_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1 -->
- `run364GC_review_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1`: session side loss veto rescue(세션 방향 손실 차단 회수)는 selected OOS net/PF(선택 표본외 순수익/수익 팩터) `60.74` / `1.1268140527`를 회복했지만 density/cost(밀도/비용) `2.5464480874/2.106870229/2.3630573248` / `-334.895`로 실패했습니다. Effect(효과): GD에서 수익 보존 밀도 회복을 실행합니다.
<!-- run364GD__strict_candidate_absent__run364GD_train_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1 -->
- `run364GD_train_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1`: profit preserving density recovery(수익 보존 밀도 회복)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GE에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364GE__oos_profit_improved_validation_density_failed__run364GE_review_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1 -->
- `run364GE_review_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1`: profit preserving density recovery(수익 보존 밀도 회복)는 selected OOS net/PF(선택 표본외 순수익/수익 팩터) `83.737` / `1.184927453`로 개선됐지만 validation/density(검증/밀도) `16.965` / `2.0546448087/2.0458015267/2.050955414`로 실패했습니다. Effect(효과): GF에서 수익 바닥 밀도 상승을 실행합니다.
<!-- run364GF__strict_candidate_absent__run364GF_train_h17_oos108_pf125_profit_floor_density_lift_without_db_v1 -->
- `run364GF_train_h17_oos108_pf125_profit_floor_density_lift_without_db_v1`: profit-floor density lift(수익 바닥 밀도 상승)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GG에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364GG__density3_failed__run364GG_review_h17_oos108_pf125_profit_floor_density_lift_without_db_v1 -->
- `run364GG_review_h17_oos108_pf125_profit_floor_density_lift_without_db_v1`: GF selected(선택) 후보는 validation net/PF(검증 순수익/수익 팩터) `78.008` / `1.101326856`와 OOS PF(표본외 수익 팩터) `1.2040677568`를 만들었지만 density(밀도) `2.2568306011/1.9694656489/2.1369426752`로 실패했습니다. Effect(효과): GH에서 밀도3 수익 바닥 수리를 실행합니다.
<!-- run364GH__strict_candidate_absent__run364GH_train_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1 -->
- `run364GH_train_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1`: density3 profit-floor repair(밀도3 수익 바닥 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GI에서 실패 경계와 회수 단서를 분리합니다.
<!-- run364GI__density_lift_cost_floor_failed__run364GI_review_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1 -->
- `run364GI_review_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1`: GH selected(선택) 후보는 density(밀도) `2.7103825137/2.6870229008/2.7006369427`로 개선됐지만 validation net(검증 순수익) `0.439`, OOS cost0.6(표본외 비용0.6) `-23.483`, combined cost0.9(합산 비용0.9) `-426.244`로 실패했습니다. Effect(효과): GJ에서 밀도-비용 바닥 재결합을 실행합니다.
<!-- run364GK__cost_repaired_density_lost__run364GK_review_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1 -->
- `run364GK_review_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1`: GJ는 OOS cost0.6(표본외 비용0.6) `25.124`와 combined cost0.9(합산 비용0.9) `-18.374`로 개선됐지만 combined density(합산 밀도) `1.6369426752`로 실패했습니다. Effect(효과): GL에서 비용 수리 상태를 보존하며 밀도를 재확장합니다.
<!-- run364GJ__strict_candidate_absent__run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1 -->
- `run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1`: density-cost floor rejoin(밀도-비용 바닥 재결합)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GK에서 비용 회복과 밀도 손실을 분리합니다.
<!-- run364GL__strict_candidate_absent__run364GL_train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1 -->
- `run364GL_train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1`: cost-repaired density reexpand(비용 수리 후 밀도 재확장)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GM에서 밀도 회복과 비용 보존을 분리합니다.
<!-- run364GM__density_recovered_cost_failed__run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1 -->
- `run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1`: GL은 combined density(합산 밀도) `2.4713375796`를 회복했지만 OOS cost0.6(표본외 비용0.6) `-79.072`와 combined cost0.9(합산 비용0.9) `-427.54`로 실패했습니다. Effect(효과): GN에서 비용 앵커와 밀도 앵커를 분리합니다.
<!-- run364GN__strict_candidate_absent__run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1 -->
- `run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GO에서 비용·밀도 균형 후보와 실패 경계를 분리합니다.
<!-- run364GO__sparse_pf999__run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1 -->
- `run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1`: sparse PF999 selector failure(희소 PF999 선택기 실패). Effect(효과): GP에서 PF를 캡하고 최소 밀도/거래수 바닥을 하드 조건으로 둡니다.
<!-- run364GP__strict_candidate_absent__run364GP_train_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1 -->
- `run364GP_train_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GQ에서 PF cap 수리 효과와 남은 비용/밀도 경계를 분리합니다.
<!-- run364GQ__cost_density_incomplete__run364GQ_review_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1 -->
- `run364GQ_review_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1`: selector repaired but cost-density frontier incomplete(선택기 수리 완료, 비용-밀도 경계 미완). Effect(효과): GR에서 비용 근접 경계를 먼저 고정합니다.
<!-- run364GR__strict_candidate_absent__run364GR_train_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1 -->
- `run364GR_train_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GS에서 비용 수리와 밀도 부족을 분리해 다음 재탐색 조건을 정합니다.
<!-- run364GS__partial_cost_repair_oos_cost_density_weak__run364GS_review_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1 -->
- `run364GS_review_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1`: combined cost0.9(합산 비용0.9)는 수리됐지만 OOS cost0.6(표본외 비용0.6)과 density lift(밀도 상승)가 약합니다. Effect(효과): GT 조건은 합산 비용 보존 + 표본외 비용/밀도 상승입니다.
<!-- run364GT__strict_candidate_absent__run364GT_train_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1 -->
- `run364GT_train_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GU에서 비용 보존과 밀도 상승의 어느 쪽이 다시 깨졌는지 분리합니다.
<!-- run364GU__density_lift_without_oos_cost_repair__run364GU_review_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1 -->
- `run364GU_review_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1`: OOS density(표본외 밀도)는 상승했지만 OOS cost0.6(표본외 비용0.6) `-29.212`로 package(패키지) 실패입니다. Effect(효과): density-only lift(밀도만 올리는 선택)를 다음 run(실행)에서 반복하지 않습니다.
<!-- run364GV__strict_candidate_absent__run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1 -->
- `run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GW에서 OOS cost0.6(표본외 비용0.6)과 density(밀도) 중 실패 축을 분리합니다.
<!-- run364GW__cost_repair_density_preserve_fail__run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1 -->
- `run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1`: cost repair(비용 수리)는 됐지만 OOS density(표본외 밀도) `1.2900763359`와 combined density(합산 밀도) `1.3280254777`가 부족합니다. Effect(효과): cost-only repair(비용만 수리)를 package(패키지)로 올리지 않습니다.
<!-- run364GX__strict_candidate_absent__run364GX_train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1 -->
- `run364GX_train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GY에서 cost hold(비용 유지)와 density recovery(밀도 회복)의 실패 축을 분리합니다.
<!-- run364GY__profit_cost_clue_density_fail__run364GY_review_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1 -->
- `run364GY_review_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1`: OOS profit/cost0.6(표본외 수익/비용0.6)은 개선됐지만 OOS density(표본외 밀도) `1.3053435115`, combined density(합산 밀도) `1.2993630573`, combined cost0.9(합산 비용0.9) `-132.105`가 package(패키지) 기준에 부족합니다. Effect(효과): profit-only selection(수익만 보는 선택)을 운영 후보로 올리지 않습니다.
<!-- run364GZ__strict_candidate_absent__run364GZ_train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1 -->
- `run364GZ_train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): HA에서 profit/cost/density(수익/비용/밀도) 중 실패 축을 분리합니다.
<!-- run364HA__density_cost_clue_profit_cost06_fail__run364HA_review_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1 -->
- `run364HA_review_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1`: OOS density(표본외 밀도)와 combined cost0.9(합산 비용0.9)는 회복됐지만 OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6) `45.36`/`1.1193919853`/`-8.94`, combined density(합산 밀도) `1.3057324841`가 부족합니다. Effect(효과): density/cost-only repair(밀도/비용만 수리)를 package(패키지)로 올리지 않습니다.
<!-- run364HB__strict_candidate_absent__run364HB_train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1 -->
- `run364HB_train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): HC에서 profit/PF/cost0.6(수익/수익 팩터/비용0.6), density(밀도), cost floor(비용 바닥) 실패 축을 분리합니다.
<!-- run364HC__hb_cost_improved_density_profit_regressed__run364HC_review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1 -->
- `run364HC_review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1`: HB combined cost0.9(합산 비용0.9)는 `-24.605`로 좋아졌지만 OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6)는 `40.598`/`1.1145199235`/`1.2977099237`/`-10.402`라 package(패키지) 부적격입니다. Effect(효과): HB single-score(HB 단일 점수)를 반복하지 않습니다.
<!-- run364HD__strict_candidate_absent__run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1 -->
- `run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1`: dual-surface switch(이중 표면 전환)가 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): HE에서 수익 복구, 비용, 밀도 실패 축을 분리합니다.
<!-- run364HE__package_rejected__run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1 -->
- `run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1`: HD는 package(패키지)로 열지 않았습니다. 이유(reason, 이유): strict_candidate_count=0, OOS net/PF 목표 미달, MT5 runtime probe(MT5 런타임 탐침) 없음. Effect(효과): 운영 주장을 차단하고 HF 탐색 조건으로 바꿉니다.
<!-- run364HJ__density_boundary__run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1 -->
- `run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1`: Not invalid(무효 아님). Package only(패키지 전용)이며 expected OOS density(예상 표본외 밀도) `1.3740458015`는 3/day(일 3회) 목표보다 낮아 운영 후보로 주장하지 않습니다.
<!-- run364HK__no_authority__run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->
- `run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`: runtime probe attempt(런타임 탐침 시도)일 뿐 operating claim(운영 주장)은 없습니다. Expected density(예상 밀도) `1.3740458015`도 3/day(일 3회) 미만입니다.
<!-- run364HL__density_side_cost_no_authority__run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->
- `run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`: positive runtime clue(긍정 런타임 단서)는 있지만 trade density(거래 밀도) `1.7261146497`가 3/day(일 3회) 미만이고 short-heavy/cost/partial-route(숏 편중/비용/부분 라우트)가 남아 authority(권위) 없음. Effect(효과): 운영 주장을 막고 HM 수리 탐색으로 넘깁니다.
<!-- run364HM__direct_strict_pass_zero__run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1 -->
- `run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`: direct strict pass(직접 엄격 통과)는 `0`개입니다. Effect(효과): scaled density estimate(스케일 밀도 추정)를 MT5 proof(MT5 증명)로 부르지 않고 HN review(HN 검토)로 넘깁니다.
<!-- run364HN__no_authority__run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1 -->
- `run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`: scaled density estimate(스케일 밀도 추정)는 긍정 단서지만 direct density proof(직접 밀도 증명), 새 MT5 runtime probe(새 MT5 런타임 탐침), runtime package(런타임 패키지)가 아직 없어 authority(권위) 없음. Effect(효과): 운영 주장 대신 HO 패키지 물질화로 넘깁니다.
<!-- run364HO__no_authority__run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1 -->
- `run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1`: runtime package(런타임 패키지)는 준비됐지만 MT5 execution(MT5 실행)과 tester output(테스터 출력)이 없어 authority(권위) 없음. Effect(효과): 운영 주장 대신 HP 런타임 탐침으로 넘깁니다.
<!-- run364HP__no_authority__run364HP_execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->
- `run364HP_execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1`: MT5 runtime probe(MT5 런타임 탐침)는 authority(권위) 없음. Effect(효과): 운영 주장 대신 HQ review(HQ 검토)로 넘깁니다.
<!-- run364HQ__profit_quality_density_no_authority__run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->
- `run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1`: MT5 net(순수익)은 양수지만 PF(수익 팩터) `1.05`, RF(회복 계수) `0.4`, density(밀도) `2.9681528662` 때문에 authority(권위) 없음. Effect(효과): 운영 주장을 막고 HR 수리 탐색으로 넘깁니다.
<!-- run364HR__no_strict_joint_pass__run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1 -->
- `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`: strict joint pass(엄격 동시 통과) `0`. Effect(효과): 운영 주장 없이 HS에서 품질/밀도 단서를 분리 검토합니다.
<!-- run364HS__stage364_closeout_no_next_stage -->
- `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`: Stage364(364단계) closeout(마감)은 `run364HR` strict_joint_pass_count(엄격 동시 통과 수) `0` 때문에 operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)를 주장하지 않습니다. Preserved clue(보존 단서)는 `hold4_margin_0.01` net/PF/density(순수익/수익 팩터/밀도) `462.0071630903` / `1.2257899553` / `2.1178343949`입니다. Effect(효과): Stage364(364단계)를 negative memory(부정 기억)로 닫고 next stage(다음 단계)를 열지 않습니다.
<!-- frontier04E_stage_closeout_v1 -->
- `frontier04E_stage_closeout_v1`: path-aware oracle label seed did not transfer into usable ONNX metrics(경로 인식 오라클 라벨 씨앗이 쓸만한 온엑스 지표로 전달되지 않음). Effect(효과): next frontier(다음 전선)는 같은 라벨-전달 가정을 반복하지 않습니다.
<!-- frontier05B_closed_bar_path_precursor_feature_scout_v1 -->
- `frontier05B_closed_bar_path_precursor_feature_scout_v1`: closed-bar precursor augmentation did not pass controlled improvement criteria(확정봉 선행 피처 증강이 통제 개선 기준을 통과하지 못함). Effect(효과): label threshold sweep(라벨 임계값 탐색) 없이 repair/closeout decision(수리/마감 결정)으로 넘깁니다.
<!-- frontier05C_stage_closeout_v1 -->
- `frontier05C_stage_closeout_v1`: Frontier05(전선05) closed as negative_memory(부정 기억): handcrafted closed-bar OHLC precursors did not improve feature_set_v2 path-label transfer(수제 확정봉 OHLC 선행 피처가 피처 세트 v2 경로 라벨 전달을 개선하지 못함). Effect(효과): next frontier(다음 전선)는 feature micro-expansion(피처 미세 확장)이 아니라 새 signal/validation hypothesis(신호/검증 가설)를 열어야 합니다.
<!-- frontier06B_selective_probability_abstention_signal_scout_v1 -->
- `frontier06B_selective_probability_abstention_signal_scout_v1`: selective abstention signal contract did not produce strict validation+OOS scout clue(선택적 기권 신호 계약이 검증+표본밖 엄격 탐색 단서를 만들지 못함). Effect(효과): unbounded threshold micro-search(무제한 임계값 미세탐색)를 막고 closeout decision(마감 결정)으로 넘깁니다.
<!-- frontier06C_stage_closeout_v1 -->
- `frontier06C_stage_closeout_v1`: selective probability abstention signal contract(선택적 확률 기권 신호 계약) did not produce validation+OOS strict scout clue(검증+표본밖 엄격 탐색 단서 없음). Effect(효과): density/PF clue(밀도/수익 팩터 단서)는 보존하되 Frontier06(전선06)은 마감합니다.
<!-- frontier07D_stage_closeout_decision_v1 -->
- `frontier07D_stage_closeout_decision_v1`: Frontier07 risk-shaped labels and capped class-prior repair did not satisfy simultaneous density/PF/DD/smoothness(전선07 위험 라벨과 상한 클래스 수리는 밀도/수익 팩터/손실폭/매끄러움 동시 조건을 만족하지 못함). Effect(효과): 같은 수리 반복을 막고 다음 전선으로 넘깁니다.
<!-- frontier08D_stage_closeout_sample_weight_objective_v1__NR-FR08-SAMPLE-WEIGHTED-OBJECTIVE -->
| `NR-FR08-SAMPLE-WEIGHTED-OBJECTIVE` | `IDEA-FR08-MULTI-OBJECTIVE-SAMPLE-WEIGHTING` | multi-objective sample weighting(다중목적 표본 가중)이 US100 M5 ONNX(온엑스) proxy surface(프록시 표면)를 네 축 동시 개선으로 밀 수 있다 | Frontier08B/C(전선08B/C) strict scout clue rows(엄격 탐색 단서 행)가 `0`이고 best validation DD(최상 검증 손실폭)가 58~60%라 WFO/MT5(WFO/MT5) 전 단계에서 실패했다 | OOS density(표본밖 밀도) 5~6/day를 만드는 adverse/path utility weighting(불리 이동/경로 효용 가중) 단서만 보존한다 | 새 objective(목적함수)가 DD/curve quality(손실폭/곡선 품질)를 직접 다룰 때만 재개 |
<!-- frontier09D_stage_closeout_drawdown_clean_path_labeling_v1 -->
- `frontier09D_stage_closeout_drawdown_clean_path_labeling_v1`: validation DD(검증 손실폭)가 56~64%로 남아 strict scout clue(엄격 탐색 단서)가 없었습니다. Effect(효과): 같은 clean path density bridge repair(깨끗한 경로 밀도 브리지 수리)를 반복하지 않습니다.
<!-- frontier10D_stage_closeout_split_consistent_utility_distillation_v1 -->
- `frontier10D_stage_closeout_split_consistent_utility_distillation_v1`: validation DD(검증 손실폭)가 56~60%로 남고 best preserved repair(최상 보존 수리)도 OOS DD(표본밖 손실폭)를 악화했습니다. Effect(효과): 같은 side-class-weight ladder/density bridge/threshold micro-search(방향 클래스 가중 사다리/밀도 브리지/임계값 미세 탐색)를 Frontier10 안에서 반복하지 않습니다.
<!-- frontier11C_stage_closeout_subperiod_stability_first_onnx_scout_v1 -->
- `frontier11C_stage_closeout_subperiod_stability_first_onnx_scout_v1`: Frontier11(전선11) negative memory(부정 기억). Action(행동): post-fit subperiod stability selector(적합 후 하위기간 안정성 선택기)를 F10C(전선10C) 후보군에 적용했지만 strict/preserved rows(엄격/보존 행)가 0이었습니다. Effect(효과): same-pool selector weight tweak(같은 후보군 선택기 가중 미세조정)은 반복 수리로 보고 다음 전선으로 넘깁니다.
<!-- frontier14D_stage_closeout_daily_session_opportunity_budget_onnx_scout_v1__density_transfer_negative_memory -->
- `frontier14D_stage_closeout_daily_session_opportunity_budget_onnx_scout_v1__density_transfer_negative_memory`: Daily/session opportunity-budget labels(일/세션별 기회 예산 라벨)은 label-side density(라벨 쪽 밀도)를 만들었지만 plain argmax ONNX(평범 최대확률 온엑스)로 model-side density(모델 쪽 밀도)를 전달하지 못했습니다. Effect(효과): 같은 quota/flat subset repair(할당량/평면 부분 표본 수리)를 반복하지 않습니다.
<!-- frontier15C_score_threshold_density_repair_or_closeout_decision_v1__score_threshold_edge_quality_negative_memory -->
- `frontier15C_score_threshold_density_repair_or_closeout_decision_v1__score_threshold_edge_quality_negative_memory`: Probability score threshold(확률 점수 임계값) alone(단독) did not create joint edge quality/PF/DD/subperiod stability(엣지 품질/수익 팩터/손실폭/하위기간 안정성). Effect(효과): 같은 9-cell threshold grid(9칸 임계값 격자) 확장이나 validation-guided filtering(검증 유도 필터링)을 반복하지 않습니다. Reopen condition(재개 조건): 새 edge-quality/risk mechanism(엣지 품질/위험 메커니즘)이 density transfer(빈도 전이)를 입력 단서로만 사용할 때.
<!-- frontier16C_edge_quality_risk_repair_or_closeout_decision_v1__edge_quality_risk_veto_negative_memory -->
<!-- frontier16C_edge_quality_risk_repair_or_closeout_decision_v1__edge_quality_risk_veto_negative_memory -->
## frontier16C_edge_quality_risk_repair_or_closeout_decision_v1 Frontier16 edge-quality risk-veto negative memory(프론티어16 엣지 품질 위험 배제 부정 기억)

- subject(대상): locked edge_margin target8(고정 엣지 마진 목표8) + 3 risk-quality labels(위험 품질 라벨 3개)
- judgment(판정): `negative_memory_no_forward_clue(전진 단서 없는 부정 기억)`
- evidence(근거): best RF validation/OOS PF-density-DD(최고 랜덤포레스트 검증/표본밖 수익 팩터-빈도-손실폭) `1.06795/5.65574/12.9599%` and `0.942216/5.45802/12.8032%`
- do_not_repeat(반복 금지): same 3 labels plus locked edge_margin target8(같은 3개 라벨 + 고정 엣지 마진 목표8), density/DD near miss as preserved clue(빈도/손실폭 근접 실패를 보존 단서로 승격)
- reopen_condition(재개 조건): new hypothesis(새 가설)가 PF and split stability(수익 팩터와 분할 안정성)를 직접 설계할 때만 재개
- report(보고서): `stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/03_reviews/frontier16C_edge_quality_risk_repair_or_closeout_decision_v1_report.md`
<!-- frontier16D_runtime_probe_supplement_v1__runtime_probe_observation -->
<!-- frontier16D_runtime_probe_supplement_v1__runtime_probe_observation -->
## frontier16D_runtime_probe_supplement_v1 Frontier16 runtime probe observation(전선16 런타임 탐침 관찰)

- judgment(판정): `runtime_probe_observation_negative_memory_unchanged(런타임 탐침 관찰, 부정 기억 유지)`
- observation(관찰): validation_is: status=completed/completed, PF=1.37, DD=12.2, trades=229, signal_diff=0 | oos: status=completed/completed, PF=0.87, DD=47.17, trades=164, signal_diff=0
- boundary(경계): F16C negative memory(부정 기억)는 유지. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
- report(보고서): `stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/03_reviews/frontier16D_runtime_probe_supplement_v1_report.md`
<!-- frontier17D_loss_cluster_firewall_repair_or_closeout_decision_v1 -->
<!-- frontier17D_loss_cluster_firewall_repair_or_closeout_decision_v1 -->
## frontier17D_loss_cluster_firewall_repair_or_closeout_decision_v1 Frontier17 Negative Memory(전선17 부정 기억)

- judgment(판정): `negative_memory(부정 기억)`
- negative memory(부정 기억): `loss_cluster_firewall_profit_persistence_failed_native_mt5_economics_and_dd(손실 군집 방화벽 수익 지속 가설은 MT5 실행 경제성과 손실폭에서 실패)`
- preserved clue(보존 단서): `runtime_veto_tape_handoff_preserved_for_future_closed_bar_veto_runtime_probe(종료봉 차단 런타임 탐침을 위한 런타임 차단 테이프 인계 단서 보존)`
- runtime observation(런타임 관찰): validation_is: PF=1.13, DD=35.45%, trades=317, signal_diff=0 | oos: PF=0.92, DD=47.5%, trades=254, signal_diff=0
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
- report(보고서): `stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/03_reviews/frontier17D_loss_cluster_firewall_repair_or_closeout_decision_v1_report.md`
<!-- frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1 -->
<!-- frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1 -->
## frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1 Frontier18 Negative Memory(전선18 부정 기억)

- judgment(판정): `negative_memory(부정 기억)`
- negative memory(부정 기억): `asymmetric_exit_lifecycle_profit_lock_failed_pf_density_smoothness_under_pre_registered_profiles(사전 등록 프로필 아래 비대칭 청산 생명주기 수익 잠금은 PF/빈도/매끄러움에서 실패)`
- preserved clue(보존 단서): `low_dd_lifecycle_shapes_preserved_as_dd_containment_clue_only(낮은 손실폭 생명주기 모양은 손실폭 억제 단서로만 보존)`
- runtime probe blocker(런타임 탐침 차단 사유): `no_forward_clue_rows_0_0_0_and_no_runtime_handoff_candidate_under_pre_registered_profile_lock(전진 단서 0/0/0이고 사전 등록 프로필 고정 아래 런타임 인계 후보 없음)`
- best proxy(최선 프록시): best=f18b_hold6_reverse_atr1p5_tp3p0__lr_plain__lifecycle;val_pf=1.03878;val_density=9.42697;val_dd=8.87262;oos_pf=0.99953;oos_density=10.5873;oos_dd=7.60684;neg_subperiod=0.409091;strict_seed_preserved=0_0_0
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
- report(보고서): `stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/03_reviews/frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1_report.md`
<!-- frontier19B_boosted_backbone_no_repair_stack_proxy_scout_v1 -->
- `frontier19B_boosted_backbone_no_repair_stack_proxy_scout_v1`: no strict/seed surface(엄격/씨앗 표면 없음) under boosted backbone-only locks(부스팅 백본 단독 잠금). Effect(효과): repair/closeout decision(수리/마감 결정)로 넘겨 같은 repair stack(수리 중첩)을 반복하지 않습니다.
<!-- frontier19C_boosted_backbone_repair_or_closeout_decision_v1 -->
- `frontier19C_boosted_backbone_repair_or_closeout_decision_v1`: capped_boosted_tree_backbone_only_valid_onnx_but_no_forward_economic_clue(상한 부스팅 트리 백본 단독은 유효 ONNX를 만들지만 전진 경제 단서 없음). Runtime blocker(런타임 차단): `no_forward_clue_rows_0_0_0_and_no_runtime_handoff_candidate_under_backbone_only_lock(전진 단서 0/0/0이고 백본 단독 잠금 아래 런타임 인계 후보 없음)`. Effect(효과): boosted backbone-only(부스팅 백본 단독)을 repair stack(수리 중첩) 없이 반복하지 않습니다.
<!-- frontier20C_rule_atlas_repair_or_closeout_decision_v1 -->
- `frontier20C_rule_atlas_repair_or_closeout_decision_v1`: train_only_depth2_rule_atlas_alone_does_not_reduce_dd_or_create_runtime_handoff(학습 전용 깊이2 규칙 지도 단독은 손실폭을 충분히 줄이거나 런타임 인계를 만들지 못함). Preserved clue(보존 단서): `low_vix_momentum_price_position_long_feature_state_surface_density_aligned_pf12_seed(낮은 VIX 모멘텀/가격 위치 롱 피처 상태 표면은 빈도 정렬 PF 약 1.2 씨앗 표면)`. Runtime blocker(런타임 차단): `runtime_probe_ineligible_under_f20_locks_no_handoff_candidate(F20 잠금 아래 인계 후보가 없어 런타임 탐침 부적격)`. Effect(효과): same train-only depth-2 rule atlas(같은 학습 전용 깊이2 규칙 지도)를 DD/handoff(손실폭/인계) 해결책처럼 반복하지 않습니다.
