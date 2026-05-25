# Negative Result Register

| result_id | idea_id | hypothesis | why_failed | salvage_value | reopen_condition |
|---|---|---|---|---|---|
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
