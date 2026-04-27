# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `11_alpha_robustness__wfo_label_horizon_sensitivity`
- status(상태): `reviewed_closed_no_next_stage_opened`
- lane(레인): `exploration(탐색)`
- scout boundary(탐색 판독 경계): `fwd18_inverse_rank_context_mt5_runtime_probe(fwd18 역방향 순위 문맥 MT5 런타임 탐침)`
- current run packet(현재 실행 묶음): `run02AA_run02AK_fwd18_rank_stress_packet_v1`
- current operating reference(현재 운영 기준): `none(없음)`

## 인계 조건(Handoff Condition, 인계 조건)

Stage 10(10단계)이 `stage10_alpha_scout_closeout_packet_v1` 묶음(packet, 묶음)으로 `run01Y(실행 01Y)`를 best balanced baseline(최고 균형 기준선)으로 남기고 닫혔으므로 시작한다.

효과(effect, 효과): Stage 11(11단계)은 Stage 10(10단계)의 단일 분할 판독을 먼저 LightGBM(`LightGBM`, 라이트GBM) model training method(모델 학습방법) 변경으로 압박하고, WFO(`walk-forward optimization`, 워크포워드 최적화)와 label/horizon sensitivity(라벨/예측수평선 민감도)는 뒤에 본다.

## 선택된 입력(Selected Inputs, 선택 입력)

- Stage 10 closeout packet(Stage 10 마감 묶음): `stages/10_alpha_scout__default_split_model_threshold_scan/03_reviews/stage10_closeout_packet.md`
- selected baseline run(선택 기준 실행): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- selected slice(선택 구간): `200 < minutes_from_cash_open <= 220`
- selected hold(선택 보유): `9`
- selected threshold(선택 임계값): `short0.600_long0.450_margin0.000`
- selected routing mode(선택 라우팅 방식): `tier_a_primary_no_fallback`

## 현재 RUN02A(Current RUN02A, 현재 실행 02A)

- run_id(실행 ID): `run02A_lgbm_training_method_scout_v1`
- model family(모델 계열): `lightgbm_lgbmclassifier_multiclass`
- comparison reference(비교 기준): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- selected threshold(선택 임계값): `a_short0.600_long0.450_margin0.000__b_short0.600_long0.450_margin0.000__hold9__slice_mid_second_overlap_200_220__model_lgbm`
- Tier A separate(Tier A 분리): `2884 rows(행)`, `659 signals(신호)`, `0.22850208044382803 coverage(커버리지)`
- Tier B-only(Tier B 단독): `696 rows(행)`, `80 signals(신호)`, `0.11494252873563218 coverage(커버리지)`
- Tier A+B combined(Tier A+B 합산): `3580 rows(행)`, `739 signals(신호)`, `0.20642458100558658 coverage(커버리지)`
- external verification status(외부 검증 상태): `completed(완료)`
- ONNX parity(ONNX 온닉스 확률 동등성): `passed(통과)`, Tier A max abs diff(Tier A 최대 절대 차이) `0.007676966073236424`, Tier B max abs diff(Tier B 최대 절대 차이) `0.00000019053892824638652`
- MT5 routed validation net/PF(MT5 라우팅 검증 순수익/수익 팩터): `-496.88 / 0.25`
- MT5 routed OOS net/PF(MT5 라우팅 표본외 순수익/수익 팩터): `-27.44 / 0.94`
- MT5 routed OOS DD/recovery(MT5 라우팅 표본외 손실/회복): `249.28 / -0.11`
- Tier B fallback used(Tier B 대체 사용): validation(검증) `32`, OOS(표본외) `64`
- result summary(결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02A_lgbm_training_method_scout_v1/reports/result_summary.md`

## 현재 RUN02B(Current RUN02B, 현재 실행 02B)

- run_id(실행 ID): `run02B_lgbm_rank_threshold_scout_v1`
- source model run(원천 모델 실행): `run02A_lgbm_training_method_scout_v1`
- model family(모델 계열): `lightgbm_lgbmclassifier_multiclass`
- threshold method(임계값 방식): `rank-target quantile(순위 기반 분위수)`
- selected threshold(선택 임계값): `a_tier_a_rankq0.960_short0.578_long0.553_margin0.120__b_tier_b_rankq0.960_short0.379_long0.409_margin0.080__hold9__slice_mid_second_overlap_200_220__model_lgbm_rank_target`
- Tier A separate(Tier A 분리): `2884 rows(행)`, `338 signals(신호)`, `0.11719833564493759 coverage(커버리지)`
- Tier B separate(Tier B 분리): `696 rows(행)`, `123 signals(신호)`, `0.17672413793103448 coverage(커버리지)`
- Tier A+B combined(Tier A+B 합산): `3580 rows(행)`, `461 signals(신호)`, `0.12877094972067038 coverage(커버리지)`
- external verification status(외부 검증 상태): `completed(완료)`
- MT5 routed validation net/PF(MT5 라우팅 검증 순수익/수익 팩터): `-496.45 / 0.23`
- MT5 routed OOS net/PF(MT5 라우팅 표본외 순수익/수익 팩터): `-92.09 / 0.76`
- MT5 routed OOS DD/recovery(MT5 라우팅 표본외 손실/회복): `293.51 / -0.31`
- Tier B fallback used(Tier B 대체 사용): validation(검증) `32`, OOS(표본외) `64`
- result summary(결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02B_lgbm_rank_threshold_scout_v1/reports/result_summary.md`

효과(effect, 효과): RUN02B(실행 02B)는 RUN01(실행 01)의 absolute grid(절대값 격자)를 반복하지 않고 LGBM(라이트GBM) 확률 분포에 맞춘 임계값을 시험했다. 신호 수는 RUN02A(실행 02A)보다 줄었지만 MT5 trading KPI(MT5 거래 핵심 성과 지표)는 회복하지 못했다.

## 현재 RUN02C~RUN02F(Current RUN02C~RUN02F, 현재 실행 02C~02F)

| run(실행) | idea(아이디어) | signals A/B/AB(신호 A/B/합산) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---|
| RUN02C(실행 02C) | long-only direction isolation(롱 전용 방향 분리) | `294/89/383` | `-154.01 / 0.68` | `82.69 / 1.35` | OOS(표본외)는 양수지만 validation(검증)이 약해 불안정 |
| RUN02D(실행 02D) | short-only direction isolation(숏 전용 방향 분리) | `217/52/269` | `-18.33 / 0.89` | `-211.48 / 0.31` | short-only(숏만)는 OOS(표본외)에서 약함 |
| RUN02E(실행 02E) | extreme confidence rejection(극단 확신만 허용) | `58/86/144` | `-115.17 / 0.31` | `-6.35 / 0.96` | OOS(표본외)는 거의 본전이나 validation(검증)이 약함 |
| RUN02F(실행 02F) | calm trend context gate(차분한 추세 문맥 제한) | `56/6/62` | `-234.03 / 0.46` | `-163.22 / 0.41` | context gate(문맥 제한)는 현재 조건에서 실패 |

효과(effect, 효과): 발산형 탐색(divergent exploration, 발산형 탐색)에서는 RUN02C(실행 02C) long-only(롱만)와 RUN02E(실행 02E) extreme confidence(극단 확신)가 약한 회수 가치(salvage value, 회수 가치)를 남겼다. 하지만 둘 다 validation/OOS(검증/표본외)를 동시에 회복하지 못해서 아직 세부 탐색(micro search, 세부 탐색)으로 들어갈 조건은 아니다.

## 현재 RUN02G~RUN02P(Current RUN02G~RUN02P, 현재 실행 02G~02P)

| run(실행) | idea(아이디어) | signals A/B/AB(신호 A/B/합산) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---|
| RUN02G(실행 02G) | long pullback(롱 되돌림) | `49/3/52` | `-138.39 / 0.54` | `238.68 / 3.44` | OOS(표본외) 회수 가치는 크지만 validation(검증)이 약함 |
| RUN02H(실행 02H) | bull trend long(상승 추세 롱) | `21/3/24` | `-210.68 / 0.19` | `11.52 / 1.21` | 작은 OOS(표본외) 양수, validation(검증) 약함 |
| RUN02I(실행 02I) | low-vol extreme confidence(저변동성 극단 확신) | `14/4/18` | `-509.12 / 0.00` | `-231.42 / 0.00` | 실패 |
| RUN02J(실행 02J) | balanced midband(균형 중간대) | `21/3/24` | `70.10 / 1.29` | `-121.32 / 0.55` | validation(검증)만 양수 |
| RUN02K(실행 02K) | quiet return z-score(조용한 수익률 z점수) | `44/5/49` | `-496.54 / 0.02` | `-494.23 / 0.19` | 실패 |
| RUN02L(실행 02L) | range compression(횡보 압축) | `18/4/22` | `-352.49 / 0.34` | `-250.36 / 0.05` | 실패 |
| RUN02M(실행 02M) | high-vol momentum alignment(고변동성 모멘텀 정렬) | `67/3/70` | `-496.38 / 0.25` | `-305.93 / 0.31` | 실패 |
| RUN02N(실행 02N) | squeeze breakout(압축 돌파) | `13/3/16` | `-125.51 / 0.62` | `107.14 / 55.11` | OOS(표본외) 회수 가치는 있으나 trade count(거래 수) 3개 |
| RUN02O(실행 02O) | bull vortex long(상승 보텍스 롱) | `16/2/18` | `-86.88 / 0.55` | `6.04 / 1.20` | 작은 OOS(표본외) 양수, validation(검증) 약함 |
| RUN02P(실행 02P) | bear vortex short(하락 보텍스 숏) | `34/1/35` | `1.78 / 1.02` | `24.33 / 1.37` | 양쪽 모두 양수지만 규모가 작아 불충분 |

효과(effect, 효과): RUN02G(실행 02G), RUN02N(실행 02N), RUN02P(실행 02P)는 다음 질문을 만들 회수 가치(salvage value, 회수 가치)를 남겼다. 하지만 RUN02G/RUN02N(실행 02G/02N)은 validation(검증)이 약하고, RUN02P(실행 02P)는 순수익(net profit, 순수익)과 거래 수가 작아서 아직 promotion_candidate(승격 후보)도 아니다.

## 현재 RUN02Q~RUN02S(Current RUN02Q~RUN02S, 현재 실행 02Q~02S)

| run(실행) | idea(아이디어) | signals A/B/AB(신호 A/B/합산) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---|
| RUN02Q(실행 02Q) | bear vortex short density(하락 보텍스 숏 밀도 확대) | `83/5/88` | `-139.28 / 0.62` | `-140.58 / 0.54` | density expansion(밀도 확대)은 실패 |
| RUN02R(실행 02R) | long pullback ADX repair(롱 되돌림 ADX 복구) | `51/3/54` | `275.78 / 2.44` | `-82.01 / 0.74` | validation-only positive(검증만 양수) |
| RUN02S(실행 02S) | squeeze density(압축 밀도 확대) | `19/7/26` | `-2.50 / 0.99` | `32.56 / 1.69` | weak salvage(약한 회수)지만 tiny sample(작은 표본) |

효과(effect, 효과): RUN02Q/R/S(실행 02Q/R/S)는 사용자가 물은 세 축을 동시에 판 것이다. 결과는 `RUN02S(실행 02S)`만 약한 생존 신호를 남겼고, `RUN02Q(실행 02Q)`와 `RUN02R(실행 02R)`은 같은 임계값 주변을 더 반복할 이유를 줄였다.

## 현재 RUN02T~RUN02V(Current RUN02T~RUN02V, 현재 실행 02T~02V)

| run(실행) | priority(우선순위) | source(원천) | read(판독) | next meaning(다음 의미) |
|---|---:|---|---|---|
| RUN02T(실행 02T) | 1 | RUN02S(실행 02S) | fwd18(90분) OOS hit rate(표본외 적중률) `0.714286` vs fwd12(60분) `0.285714` | fwd18 retraining probe(fwd18 재학습 탐침)가 1순위 |
| RUN02U(실행 02U) | 2 | RUN02S(실행 02S) | OOS(표본외) signal(신호) `10`, nonzero windows(신호 있는 구간) `3` | full WFO(전체 워크포워드 최적화)는 아직 무거움 |
| RUN02V(실행 02V) | 3 | RUN02P/RUN02Q(실행 02P/02Q) | RUN02Q(실행 02Q) OOS short hit rate(표본외 숏 적중률) `0.190476`, RUN02P(실행 02P) `0.100000` | short-specific(숏 전용)은 보류 가능한 하위 후보 |

효과(effect, 효과): 우선순위는 `1) fwd18 label horizon retraining probe(fwd18 라벨 예측수평선 재학습 탐침)`, `2) WFO-lite after denser surface(더 조밀한 표면 뒤 WFO-lite)`, `3) short-specific label/model(숏 전용 라벨/모델)` 순서로 정리한다.

## 현재 RUN02W(Current RUN02W, 현재 실행 02W)

| view(보기) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---:|---:|---|
| Tier A only(Tier A 단독) | `-495.84 / 0.28` | `-132.97 / 0.75` | negative(부정) |
| Tier B fallback-only(Tier B 대체 단독) | `197.17 / 8.31` | `-105.73 / 0.70` | validation-only(검증만 양수) |
| Routed total(라우팅 전체) | `-496.25 / 0.28` | `-216.12 / 0.67` | negative(부정) |

효과(effect, 효과): fwd18 label horizon(90분 라벨 예측수평선)을 실제 재학습(retraining, 재학습)하고 MT5(`MetaTrader 5`, 메타트레이더5)까지 연결했지만, 기존 run01Y threshold(임계값)를 그대로 쓰는 fwd18-only retrain(fwd18 단독 재학습)은 회복하지 못했다. 이 판독은 이후 fwd18 + context/rank threshold(문맥/순위 임계값) 확인으로 이어졌고 Stage 11(11단계) 근거 안에 닫혔다.

## 현재 RUN02X~RUN02Z(Current RUN02X~RUN02Z, 현재 실행 02X~02Z)

| run(실행) | method(방식) | signal A/B/AB(신호 A/B/합산) | validation read(검증 판독) | OOS read(표본외 판독) | judgment(판정) |
|---|---|---:|---:|---:|---|
| RUN02X(실행 02X) | direct fwd18 rank threshold(직접 fwd18 순위 임계값) | `327/164/491` | Tier A q96 hit(적중률) `0.25` | Tier A q96 hit(적중률) `0.15625` | structural negative(구조 부정) |
| RUN02Y(실행 02Y) | inverse fwd18 rank threshold(역방향 fwd18 순위 임계값) | `327/164/491` | Tier A q96 hit(적중률) `0.604167` | Tier A q96 hit(적중률) `0.34375` | mixed structural(혼합 구조) |
| RUN02Z(실행 02Z) | inverse rank + DI/ADX context(역방향 순위 + DI/ADX 문맥) | `20/9/29` | MT5 routed(라우팅) `386.06 / 7.25 / 9 trades(거래)` | MT5 routed(라우팅) `352.63 / 52.03 / 5 trades(거래)` | positive tiny-sample runtime_probe(작은 표본 긍정 런타임 탐침) |

효과(effect, 효과): RUN02X(실행 02X)는 fwd18(90분) 고순위 신호를 그대로 쓰면 약하다는 것을 남겼다. RUN02Y(실행 02Y)는 단순 inverse(역방향)만으로는 OOS(표본외)를 충분히 회복하지 못한다는 것을 남겼다. RUN02Z(실행 02Z)는 inverse rank(역방향 순위)를 DI spread/ADX(DI 차이/ADX) 압축 문맥으로 제한할 때 validation/OOS(검증/표본외)가 동시에 양수로 바뀐 첫 MT5(메타트레이더5) 판독이다.

하지만 RUN02Z(실행 02Z)는 validation(검증) `9`거래, OOS(표본외) `5`거래라 아직 alpha quality(알파 품질), promotion_candidate(승격 후보), live readiness(실거래 준비), operating promotion(운영 승격)이 아니다. 같은 아이디어의 adjacent context/rank stress test(인접 문맥/순위 압박 시험)와 Tier A-only versus routed check(Tier A 단독 대 라우팅 점검)는 RUN02AA~RUN02AK(실행 02AA~02AK)에서 닫혔다.

## Stage 11 Closeout(Stage 11 마감)

- closeout packet(마감 묶음): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/03_reviews/stage11_closeout_packet.md`
- closeout decision(마감 결정): `docs/decisions/2026-04-27_stage11_alpha_robustness_closeout.md`
- final judgment(최종 판정): `closed_inconclusive_tiny_sample_runtime_probe_evidence`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`

효과(effect, 효과): Stage 11(11단계)은 닫혔고, 이 파일은 새 stage(단계)의 작업 지시를 기록하지 않는다.

## 현재 RUN02AA~RUN02AK(Current RUN02AA~RUN02AK, 현재 실행 02AA~02AK)

| run(실행) | axis(축) | validation net/PF/trades(검증 순수익/수익 팩터/거래) | OOS net/PF/trades(표본외 순수익/수익 팩터/거래) | read(판독) |
|---|---|---:|---:|---|
| RUN02AA(실행 02AA) | `ADX<=20` routed(라우팅) | `480.75 / 446.14 / 7` | `31.62 / 2.80 / 2` | 너무 좁아 OOS(표본외)가 약함 |
| RUN02AB(실행 02AB) | `ADX<=30` routed(라우팅) | `377.02 / 13.47 / 10` | `294.95 / 9.20 / 5` | 생존하지만 RUN02Z(실행 02Z)보다 약함 |
| RUN02AC(실행 02AC) | `ADX<=20` Tier A-only(Tier A 단독) | `253.37 / 3.61 / 4` | `0.00 / 0.00 / 0` | OOS(표본외) 거래 없음 |
| RUN02AD(실행 02AD) | `ADX<=25` Tier A-only(Tier A 단독) | `438.21 / 8.67 / 7` | `241.95 / 0.00 / 2` | 양수지만 routed(라우팅)보다 얇음 |
| RUN02AE(실행 02AE) | `ADX<=30` Tier A-only(Tier A 단독) | `397.54 / 17.29 / 8` | `239.77 / 0.00 / 2` | 양수지만 routed(라우팅)보다 약함 |
| RUN02AI(실행 02AI) | session(세션) `190-210` | `587.28 / 10.61 / 9` | `99.34 / 20.18 / 5` | validation-heavy(검증 치우침) |
| RUN02AJ(실행 02AJ) | session(세션) `195-215` | `460.98 / 9.07 / 9` | `227.12 / 10.91 / 6` | 보조 확인 후보 |
| RUN02AK(실행 02AK) | session(세션) `205-225` | `308.70 / 6.31 / 9` | `233.30 / 31.66 / 4` | 보조 확인 후보 |

효과(effect, 효과): stress(압박) 결과는 RUN02Z(실행 02Z)의 중심 조건 `ADX<=25`, `200-220`, routed fallback(라우팅 대체)을 더 선호하게 만든다. 하지만 표본이 작아서 여전히 promotion_candidate(승격 후보)는 아니다.

## 경계(Boundary, 경계)

RUN02A(실행 02A)는 Python-side scout(파이썬 측 탐색)와 MT5 runtime_probe(MT5 런타임 탐침)를 완료했다. RUN02B(실행 02B)는 LGBM-specific threshold scout(LGBM 전용 임계값 탐색)와 routed-only MT5 runtime_probe(라우팅 전용 MT5 런타임 탐침)를 완료했다. RUN02C~RUN02F(실행 02C~02F)는 direction/confidence/context(방향/확신/문맥) 발산형 runtime_probe(런타임 탐침)를 완료했다. RUN02G~RUN02S(실행 02G~02S)는 idea burst/salvage extension(아이디어 무더기/회수 확장) runtime_probe(런타임 탐침)를 완료했다. RUN02T~RUN02V(실행 02T~02V)는 Python structural probe(파이썬 구조 탐침)를 완료했다. RUN02W(실행 02W)는 fwd18 retrain MT5 runtime_probe(fwd18 재학습 MT5 런타임 탐침)를 완료했다. RUN02X~RUN02Y(실행 02X~02Y)는 fwd18 rank/inverse structural probe(fwd18 순위/역방향 구조 탐침)이고, RUN02Z(실행 02Z)는 fwd18 inverse-rank context MT5 runtime_probe(fwd18 역방향 순위 문맥 MT5 런타임 탐침)를 완료했다.

효과(effect, 효과)는 LightGBM(라이트GBM)이 같은 run01Y(실행 01Y) threshold/slice/hold(임계값/구간/보유)와 fwd18-only retrain(fwd18 단독 재학습)에서는 약하지만, fwd18 inverse-rank + DI/ADX context(fwd18 역방향 순위 + DI/ADX 문맥)에는 작은 양수 런타임 판독이 생겼다는 것을 확인한 것이다.

아직 alpha result(알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority expansion(런타임 권위 확장), full WFO result(전체 워크포워드 최적화 결과)를 뜻하지 않는다.
