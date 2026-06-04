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
