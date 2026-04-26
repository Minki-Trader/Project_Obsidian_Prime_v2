# Current Working State

- updated_on: `2026-04-27`
- project_mode: `clean_stage_restart`
- active_stage: `11_alpha_robustness__wfo_label_horizon_sensitivity`
- active_branch: `main`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 clean stage restart(깨끗한 단계 재시작) 이후 Stage 02~09(2~9단계)를 닫았다.

효과(effect, 효과): Stage 10(10단계)은 `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)` 200~220 closeout(마감) runtime_probe(런타임 탐침)로 닫혔다. Stage 11(11단계)은 `RUN02A~RUN02F(실행 02A~02F)` LGBM(`LightGBM`, 라이트GBM) training/threshold/divergent scouts(학습/임계값/발산형 탐색)를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 실행했고, `run01Y(실행 01Y)`는 비교 점수판(comparison scoreboard, 비교 점수판)으로만 둔다.

아직 alpha result(알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 없다.

## 닫힌 기반 진실(Closed Foundation Truth, 닫힌 기반 진실)

Stage 02(2단계)는 첫 shared feature frame freeze(공유 피처 프레임 동결 산출물)를 물질화했다.

- dataset_id(데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- selected rows(선택 행 수): `54439`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

Stage 03(3단계)는 첫 training label/split(학습 라벨/분할)을 물질화했다.

- training_dataset_id(학습 데이터셋 ID): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- train/validation/OOS(학습/검증/표본외): `29222/9844/7584`

Stage 04(4단계)는 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)와 58 feature(58개 피처) model input(모델 입력)을 물질화했다.

- model_input_dataset_id(모델 입력 데이터셋 ID): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- included features(포함 피처): `58`
- boundary(경계): price-proxy weights(가격 대리 가중치)는 actual NDX/QQQ weights(실제 NDX/QQQ 가중치)가 아니다.

Stage 05(5단계)는 feature integrity audit(피처 무결성 감사)를 닫았다.

- run_id(실행 ID): `20260425_stage05_feature_integrity_audit_v1`
- judgment(판정): `positive_feature_integrity_audit_passed`
- boundary(경계): feature integrity evidence(피처 무결성 근거)이지 model quality(모델 품질)가 아니다.

Stage 06(6단계)는 minimum fixture set(최소 표본 묶음) 기준 Python/MT5 runtime parity(파이썬/MT5 런타임 동등성)를 닫았다.

- run_id(실행 ID): `20260425_stage06_runtime_parity_closed_v1`
- judgment(판정): `positive_runtime_parity_passed`
- max abs diff(최대 절대 차이): `0.0000017512503873717833`
- boundary(경계): Stage 06(6단계) 최소 표본 묶음의 runtime authority(런타임 권위)이지 model quality(모델 품질)나 operating promotion(운영 승격)이 아니다.

Stage 07(7단계)는 baseline training smoke(기준선 학습 스모크)를 닫았다.

- run_id(실행 ID): `20260425_stage07_baseline_training_smoke_v1`
- model artifact id(모델 산출물 ID): `model_fpmarkets_v2_stage07_logreg_smoke_v1`
- validation accuracy(검증 정확도): `0.45672490857375053`
- OOS accuracy(표본외 정확도): `0.457542194092827`
- boundary(경계): Python-side training pipeline evidence(파이썬 측 학습 처리 흐름 근거)이지 alpha quality(알파 품질)가 아니다.

Stage 08(8단계)는 alpha entry protocol(알파 진입 규칙)과 Tier A/B reporting rule(티어 A/B 보고 규칙)을 닫았다.

- packet_id(묶음 ID): `stage08_alpha_entry_protocol_v1`
- status(상태): `reviewed_closed_handoff_to_stage09_complete_with_alpha_entry_protocol`
- policy(정책): `docs/policies/alpha_entry_protocol.md`
- report template(보고 틀): `docs/templates/alpha_exploration_report_template.md`
- boundary(경계): Stage 08(8단계)은 alpha result(알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 만들지 않았다.

Stage 09(9단계)는 pre-alpha handoff packet(알파 전 인계 묶음)을 닫았다.

- packet_id(묶음 ID): `stage09_pre_alpha_handoff_packet_v1`
- status(상태): `reviewed_closed_handoff_to_stage10_complete_with_pre_alpha_handoff_packet`
- packet(묶음): `stages/09_pre_alpha_handoff__registry_publish_packet/03_reviews/pre_alpha_handoff_packet.md`
- decision(결정): `docs/decisions/2026-04-25_stage09_pre_alpha_handoff.md`
- boundary(경계): Stage 09(9단계)는 registry/current truth/publish boundary(등록부/현재 진실/게시 경계)를 닫았지만 alpha result(알파 결과)를 만들지 않았다.

## 현재 단계(Current Stage, 현재 단계)

`11_alpha_robustness__wfo_label_horizon_sensitivity`

Stage 11(11단계)의 질문(question, 질문)은 Stage 10(10단계)의 `run01Y(실행 01Y)` 기준 후보와 그 주변 아이디어가 WFO(워크포워드 최적화), label/horizon sensitivity(라벨/예측수평선 민감도), model training method sensitivity(모델 학습방법 민감도)에서도 구조적으로 버티는가다.

효과(effect, 효과): Stage 11(11단계)은 Stage 10(10단계)의 single_split_scout(단일 분할 탐색 판독)을 alpha quality(알파 품질)처럼 과장하지 않고, 먼저 학습방법 변경이 신호 표면(signal surface, 신호 표면)을 바꾸는지 확인한다.

## 탐색 원칙(Exploration Rule, 탐색 원칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 탐색 게이트(exploration gate, 탐색 제한문)가 아니다.

둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 sample label(표본 라벨)이다.

효과(effect, 효과): 보고서(report, 보고서)는 무엇을 탐색했는지 정직하게 라벨링(labeling, 라벨링)하되, 티어(tier, 티어)를 아이디어 승인이나 거절로 쓰지 않는다.

Stage 10(10단계) 이후 alpha exploration run(알파 탐색 실행)은 Tier A(티어 A), Tier B(티어 B), Tier A+B combined(Tier A+B 합산)를 함께 남긴다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서는 이 뜻이 `Tier A primary(티어 A 우선)`, `Tier B fallback(티어 B 대체)`, `actual routed total(실제 라우팅 전체)`이다.

효과(effect, 효과): Tier A(티어 A)만 본 결과가 전체 alpha read(알파 판독)처럼 남지 않고, Tier B(티어 B)가 실제로 메운 구간과 전체 라우팅 결과를 같은 실행(run, 실행)에서 비교한다.

Stage 10(10단계)의 기본 레인(lane, 레인)은 `exploration(탐색)`이고 첫 경계(boundary, 경계)는 `single_split_scout(단일 분할 탐색 판독)`다.

## 닫힌 Stage 10 묶음(Closed Stage 10 Packet, 닫힌 Stage 10 묶음)

`run01Y_run01AC_logreg_a_base_no_fallback_200_220_hold_threshold_closeout_v1`

- included runs(포함 실행): `run01Y hold9 base(9봉 기준)`, `run01Z hold6(6봉)`, `run01AA hold12(12봉)`, `run01AB margin0.025(마진 0.025)`, `run01AC strict probability(엄격 확률)`
- routing mode(라우팅 방식): `tier_a_primary_no_fallback`
- routed fallback enabled(라우팅 대체 사용): `false`
- baseline Tier A rule(기준 Tier A 규칙): `short0.600_long0.450_margin0.000`
- baseline max hold bars(기준 최대 보유 봉 수): `9`
- session slice(시간대 조각): `200 < minutes_from_cash_open <= 220`
- boundary(경계): `runtime_probe(런타임 탐침)`

효과(effect, 효과): run01Y(실행 01Y)의 좋은 점이 hold(보유)나 threshold(임계값) 한 점에만 묶였는지 확인했다.

MT5(`MetaTrader 5`, 메타트레이더5) 결과는 다음과 같다.

| run(실행) | slice/routing(구간/라우팅) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | OOS DD/recovery(표본외 손실/회복) |
|---:|---:|---:|---:|---:|
| run01Y(실행 01Y) | hold9(9봉), base(기준) | `318.48 / 3.88` | `313.14 / 3.99` | `144.65 / 2.16` |
| run01Z(실행 01Z) | hold6(6봉), base(기준) | `264.14 / 2.99` | `109.65 / 1.66` | `161.79 / 0.68` |
| run01AA(실행 01AA) | hold12(12봉), base(기준) | `447.76 / 4.55` | `225.69 / 2.57` | `170.11 / 1.33` |
| run01AB(실행 01AB) | hold9(9봉), margin0.025(마진 0.025) | `318.48 / 3.88` | `313.14 / 3.99` | `144.65 / 2.16` |
| run01AC(실행 01AC) | hold9(9봉), strict probability(엄격 확률) | `143.91 / 2.30` | `219.09 / 5.53` | `147.09 / 1.49` |

효과(effect, 효과): run01Y(실행 01Y)가 현재 순수익(net profit, 순수익)과 recovery(회복계수)의 균형이 가장 좋다. hold6(6봉 보유)은 약하고, hold12(12봉 보유)는 validation(검증)은 좋아지지만 OOS(표본외)가 줄었다. margin0.025(마진 0.025)는 결과가 같아서 실제로 조건을 줄이지 못했고, strict probability(엄격 확률)는 OOS PF(표본외 수익 팩터)는 높지만 net/recovery(순수익/회복)가 낮아졌다.

Tier B fallback-only(Tier B 대체 구간 단독)는 run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)에서 validation/OOS(검증/표본외) 모두 거래가 없었다.

효과(effect, 효과): 이번 closeout(마감)은 `200~220` 구간의 run01Y(실행 01Y)를 Stage 11(11단계)의 기준 후보로 넘긴다. 하지만 아직 single_split runtime_probe(단일 분할 런타임 탐침)라서 alpha quality(알파 품질)나 operating promotion(운영 승격)은 아니다.

## 현재 Stage 11 상태(Current Stage 11 State, 현재 Stage 11 상태)

- status(상태): `active_run02C_run02F_divergent_runtime_probe_completed`
- current run packet(현재 실행 묶음): `run02C_run02F_lgbm_divergent_scout_packet_v1`
- model family(모델 계열): `lightgbm_lgbmclassifier_multiclass`
- comparison reference(비교 기준): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- selected slice(선택 구간): `200 < minutes_from_cash_open <= 220`
- selected hold(선택 보유): `9`
- selected threshold(선택 임계값): `a_tier_a_rankq0.960_short0.578_long0.553_margin0.120__b_tier_b_rankq0.960_short0.379_long0.409_margin0.080__hold9__slice_mid_second_overlap_200_220__model_lgbm_rank_target`
- threshold method(임계값 방식): `rank-target quantile(순위 기반 분위수)`
- external verification status(외부 검증 상태): `completed(완료)`

RUN02A(실행 02A)는 같은 run01Y(실행 01Y) threshold/slice/hold(임계값/구간/보유)를 LightGBM(라이트GBM)에 그대로 적용한 training-method scout(학습방법 탐색)다.

RUN02B(실행 02B)는 RUN01(실행 01)의 absolute grid(절대값 격자)를 반복하지 않고, RUN02A(실행 02A)의 LightGBM(라이트GBM) 확률 분포에서 validation quantile rank(검증 분위수 순위)로 임계값을 다시 정했다.

| view(보기) | rows(행) | signal count(신호 수) | signal coverage(신호 비율) | short/long(숏/롱) |
|---|---:|---:|---:|---:|
| Tier A separate(Tier A 분리) | `2884` | `338` | `0.11719833564493759` | `149/189` |
| Tier B separate(Tier B 분리) | `696` | `123` | `0.17672413793103448` | `38/85` |
| Tier A+B combined(Tier A+B 합산) | `3580` | `461` | `0.12877094972067038` | `187/274` |

효과(effect, 효과): RUN02B(실행 02B)는 RUN02A(실행 02A)보다 combined signal coverage(합산 신호 비율)를 `0.20642458100558658`에서 `0.12877094972067038`로 줄였지만, 거래 KPI(핵심 성과 지표)는 회복하지 못했다.

MT5(`MetaTrader 5`, 메타트레이더5) 결과는 다음과 같다.

| run(실행) | method(방식) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | OOS DD/recovery(표본외 손실/회복) |
|---|---|---:|---:|---:|
| RUN02A(실행 02A) | run01Y absolute threshold(run01Y 절대 임계값) | `-496.88 / 0.25` | `-27.44 / 0.94` | `249.28 / -0.11` |
| RUN02B(실행 02B) | LGBM rank-target threshold(LGBM 순위 기반 임계값) | `-496.45 / 0.23` | `-92.09 / 0.76` | `293.51 / -0.31` |

RUN02C~RUN02F(실행 02C~02F)는 RUN01(실행 01)식 근처 튜닝을 피하고 direction/confidence/context(방향/확신/문맥)으로 발산시킨 묶음이다.

| run(실행) | idea(아이디어) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---|
| RUN02C(실행 02C) | long-only(롱만) | `-154.01 / 0.68` | `82.69 / 1.35` | OOS(표본외) 회수 가치는 있으나 validation(검증)이 약함 |
| RUN02D(실행 02D) | short-only(숏만) | `-18.33 / 0.89` | `-211.48 / 0.31` | short-only(숏만)는 OOS(표본외)에서 약함 |
| RUN02E(실행 02E) | extreme confidence(극단 확신) | `-115.17 / 0.31` | `-6.35 / 0.96` | OOS(표본외)는 거의 본전이나 validation(검증)이 약함 |
| RUN02F(실행 02F) | calm trend context gate(차분한 추세 문맥 제한) | `-234.03 / 0.46` | `-163.22 / 0.41` | 현재 문맥 제한 조건은 실패 |

효과(effect, 효과): RUN02C(실행 02C)와 RUN02E(실행 02E)는 회수 가치(salvage value, 회수 가치)를 남겼지만, 둘 다 validation/OOS(검증/표본외)를 동시에 회복하지 못했다. 그래서 지금은 LGBM(라이트GBM) 세부 조정보다 새 label/model/context(라벨/모델/문맥) 축을 여는 쪽이 낫다.

## 현재 경계(Current Boundary, 현재 경계)

현재 상태는 아직 alpha-ready(알파 준비 완료), official alpha result(공식 알파 결과), live readiness(실거래 준비), operating promotion(운영 승격)이 아니다.

Stage 10(10단계) `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)`를 실행했다는 뜻은 200~220 closeout runtime_probe(마감 런타임 탐침)를 완료했다는 뜻이다. Stage 11(11단계) `RUN02A~RUN02F(실행 02A~02F)`는 LightGBM(라이트GBM) 학습방법, LGBM-specific threshold(LGBM 전용 임계값), 발산형 runtime_probe(런타임 탐침)를 완료했다는 뜻이다. 아직 WFO(워크포워드 최적화) 결과, promotion_candidate(승격 후보), operating_promotion(운영 승격)은 없다.

## 남은 작업(Open Items, 남은 작업)

- Stage 11(11단계): `RUN02C/RUN02E(실행 02C/02E)`의 회수 가치(salvage value, 회수 가치)는 보존하되, 바로 micro search(세부 탐색)로 들어가지 않기
- Stage 11(11단계): 다음 발산 축은 새 label/model/context(라벨/모델/문맥) 중 하나로 열기
- Stage 11(11단계): `run01Y(실행 01Y)` WFO/label-horizon sensitivity(WFO/라벨-예측수평선 민감도)는 LGBM 발산형 판독 뒤에도 아직 승격 검증으로 읽지 않기
- Stage 10(10단계): `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)`는 closed inconclusive runtime probe(닫힌 불충분 런타임 탐침)로 유지하기
- `run01A(실행 01A)`부터 `run01AC(실행 01AC)`까지의 Tier A only/Tier B fallback-only/routed total(Tier A 단독/Tier B 대체 구간 단독/라우팅 전체) 장부와 KPI(핵심 성과 지표)를 다음 실행 비교 기준으로 유지하기
- Tier B partial-context fallback(Tier B 부분 문맥 대체)의 subtype(하위유형)별 신호 품질과 거래 품질을 다음 scout variant(탐색 변형)에서 비교하기
- label/horizon variants(라벨/예측수평선 변형)는 나중 후보로 두고 기본 계약(default contract, 기본 계약)을 조용히 바꾸지 않기
- broader valid-row scope(더 넓은 유효행 범위)나 partial-day scope(부분일 범위)는 나중 후보로 두고 첫 freeze(동결 산출물)를 조용히 넓히지 않기
- MT5 price-proxy top3 weights(MT5 가격 대리 top3 가중치)를 actual NDX/QQQ weights(실제 NDX/QQQ 가중치)로 읽지 않기

## 현재 진실이 아닌 것(Not Current Truth, 현재 진실 아님)

- 오래된 Stage 06 `Tier B(티어 B)` 점수판(scorecard, 점수판) 결론
- 오래된 Stage 07 이중 판정 팩(dual-verdict packet, 이중 판정 팩)
- `Tier A(티어 A)`만 탐색의 기준선(anchor, 기준선)이라는 주장
- `Tier B(티어 B)`가 model study(모델 연구) 전에 끝없는 pre-validation(사전검증)을 받아야 한다는 주장
- MT5 price-proxy weights(MT5 가격 대리 가중치)를 actual index weights(실제 지수 가중치)로 읽는 주장
- Stage 07(7단계) baseline training smoke(기준선 학습 스모크)를 alpha quality(알파 품질)나 live readiness(실거래 준비)로 읽는 주장
- Stage 08(8단계) protocol(규칙)을 alpha result(알파 결과)로 읽는 주장
- Stage 09(9단계) handoff packet(인계 묶음)을 alpha result(알파 결과)로 읽는 주장
- Stage 10(10단계) `run01A(실행 01A)`부터 `run01AC(실행 01AC)`까지의 runtime probe(런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), runtime authority expansion(런타임 권위 확장), operating promotion(운영 승격)으로 읽는 주장
- Stage 11(11단계) scaffold(뼈대)를 Stage 11 run result(실행 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- Stage 11(11단계) `RUN02A~RUN02F(실행 02A~02F)` LightGBM MT5 runtime_probe(라이트GBM MT5 런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
