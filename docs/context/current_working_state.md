# Current Working State

- updated_on: `2026-04-29`
- project_mode: `clean_stage_restart`
- active_stage: `12_model_family_challenge__extratrees_training_effect(12단계 모델 계열 도전)`
- active_branch: `main(메인 브랜치)`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 clean stage restart(깨끗한 단계 재시작) 이후 Stage 02~09(2~9단계)를 닫았다.

효과(effect, 효과): Stage 10(10단계)은 `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)` 200~220 closeout(마감) runtime_probe(런타임 탐침)로 닫혔다. Stage 11(11단계)은 `RUN02A~RUN02S(실행 02A~02S)` LGBM(`LightGBM`, 라이트GBM) training/threshold/divergent/idea burst/salvage extension scouts(학습/임계값/발산형/아이디어 무더기/회수 확장 탐색)를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 실행했고, `RUN02T~RUN02V(실행 02T~02V)` priority structural probe(우선순위 구조 탐침)로 다음 방향을 좁혔다. `RUN02W(실행 02W)`는 fwd18(90분) 재학습을 MT5 runtime_probe(런타임 탐침)까지 확인했고, `RUN02X~RUN02Z(실행 02X~02Z)`는 fwd18 rank/inverse/context(90분 순위/역방향/문맥) 축을 판 결과다. `RUN02AA~RUN02AK(실행 02AA~02AK)`는 그 중심 표면의 ADX/routing/session stress(ADX/라우팅/세션 압박)를 완료했다. `run01Y(실행 01Y)`는 비교 점수판(comparison scoreboard, 비교 점수판)으로만 둔다.

Stage 11(11단계)은 `stage11_alpha_robustness_closeout_packet_v1`로 닫혔다. Stage 12(12단계)는 ExtraTrees(`ExtraTrees`, 엑스트라 트리) standalone experiment(단독 실험)로 열렸다. `RUN03A(실행 03A)`는 Stage 10/11(10/11단계) 표면을 끌고 와서 `invalid_for_standalone_scope(단독 범위 무효)`로 낮췄고, `RUN03B(실행 03B)`는 단독 Python scout(파이썬 탐침) 원천 모델이며, `RUN03D(실행 03D)`는 standalone batch20 Python package(단독 20개 묶음 파이썬 패키지), 현재 기준은 `RUN03F(실행 03F)` Tier A/B/routed MT5 tier-balance supplement(Tier A/B/라우팅 MT5 티어 균형 보강)다.

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

`12_model_family_challenge__extratrees_training_effect`

Stage 12(12단계)의 질문(question, 질문)은 Stage 10/11(10/11단계)을 계승하지 않고 ExtraTrees(엑스트라 트리) model family(모델 계열)를 standalone(단독)으로 학습하면 어떤 구조 신호가 나오는가다.

효과(effect, 효과): Stage 12(12단계)는 Stage 10(10단계)의 threshold/session(임계값/세션), Stage 11(11단계)의 LightGBM/context surface(라이트GBM/문맥 표면)를 쓰지 않고 새 모델 자체의 학습 효과(training effect, 학습 효과)를 분리해서 본다.

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

- status(상태): `reviewed_closed_no_next_stage_opened`
- current run packet(현재 실행 묶음): `run02AA_run02AK_fwd18_rank_stress_packet_v1`
- model family(모델 계열): `lightgbm_lgbmclassifier_multiclass`
- comparison reference(비교 기준): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- selected slice(선택 구간): `200 < minutes_from_cash_open <= 220`
- selected hold(선택 보유): `9`
- selected threshold(선택 임계값): `a_tier_a_rankq0.960_short0.571_long0.654_margin0.120__b_tier_b_rankq0.960_short0.413_long0.457_margin0.080__hold9__slice_mid_second_overlap_200_220__model_lgbm_rank_target_inverse__ctx_di_spread_abs_lte8_adx_lte25`
- threshold method(임계값 방식): `rank-target quantile(순위 기반 분위수)`
- external verification status(외부 검증 상태): `completed(완료)`

stress packet(압박 묶음): `run02AA_run02AK_fwd18_rank_stress_packet_v1`
closeout packet(마감 묶음): `stage11_alpha_robustness_closeout_packet_v1`

효과(effect, 효과): RUN02Z(실행 02Z)의 중심 조건 `ADX<=25`, `200-220`, routed fallback(라우팅 대체)이 ADX/routing/session stress(ADX/라우팅/세션 압박)에서 가장 균형적으로 남았다. 하지만 거래 수가 작아서 alpha quality(알파 품질)나 promotion_candidate(승격 후보)는 아니다.

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

RUN02G~RUN02P(실행 02G~02P)는 RUN02C/RUN02E(실행 02C/02E)의 회수 가치를 바로 세부 탐색하지 않고, context/direction/confidence(문맥/방향/확신) 아이디어 10개로 더 넓게 발산시킨 묶음이다.

| run(실행) | idea(아이디어) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---|
| RUN02G(실행 02G) | long pullback(롱 되돌림) | `-138.39 / 0.54` | `238.68 / 3.44` | OOS(표본외) 회수 가치는 큼, validation(검증)은 약함 |
| RUN02H(실행 02H) | bull trend long(상승 추세 롱) | `-210.68 / 0.19` | `11.52 / 1.21` | 작은 OOS(표본외) 양수, validation(검증) 약함 |
| RUN02I(실행 02I) | low-vol extreme confidence(저변동성 극단 확신) | `-509.12 / 0.00` | `-231.42 / 0.00` | 실패 |
| RUN02J(실행 02J) | balanced midband(균형 중간대) | `70.10 / 1.29` | `-121.32 / 0.55` | validation(검증)만 양수 |
| RUN02K(실행 02K) | quiet return z-score(조용한 수익률 z점수) | `-496.54 / 0.02` | `-494.23 / 0.19` | 실패 |
| RUN02L(실행 02L) | range compression(횡보 압축) | `-352.49 / 0.34` | `-250.36 / 0.05` | 실패 |
| RUN02M(실행 02M) | high-vol momentum alignment(고변동성 모멘텀 정렬) | `-496.38 / 0.25` | `-305.93 / 0.31` | 실패 |
| RUN02N(실행 02N) | squeeze breakout(압축 돌파) | `-125.51 / 0.62` | `107.14 / 55.11` | OOS(표본외) 회수 가치는 있으나 거래 수 3개 |
| RUN02O(실행 02O) | bull vortex long(상승 보텍스 롱) | `-86.88 / 0.55` | `6.04 / 1.20` | 작은 OOS(표본외) 양수, validation(검증) 약함 |
| RUN02P(실행 02P) | bear vortex short(하락 보텍스 숏) | `1.78 / 1.02` | `24.33 / 1.37` | 양쪽 모두 양수지만 규모가 작아 불충분 |

효과(effect, 효과): RUN02G/RUN02N/RUN02P(실행 02G/02N/02P)는 회수 가치(salvage value, 회수 가치)를 남겼다. 하지만 RUN02G/RUN02N(실행 02G/02N)은 validation(검증)이 약하고, RUN02P(실행 02P)는 순수익(net profit, 순수익)과 거래 수가 작아서 아직 세부 탐색 후보일 뿐이다.

RUN02Q~RUN02S(실행 02Q~02S)는 위 세 가지 회수 후보를 동시에 더 파본 salvage extension(회수 확장) 묶음이다.

| run(실행) | idea(아이디어) | signals A/B/AB(신호 A/B/합산) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---|
| RUN02Q(실행 02Q) | bear vortex short density(하락 보텍스 숏 밀도 확대) | `83/5/88` | `-139.28 / 0.62` | `-140.58 / 0.54` | 신호 밀도는 늘었지만 validation/OOS(검증/표본외)가 모두 음수 |
| RUN02R(실행 02R) | long pullback ADX repair(롱 되돌림 ADX 복구) | `51/3/54` | `275.78 / 2.44` | `-82.01 / 0.74` | validation(검증)은 복구됐지만 OOS(표본외)가 실패 |
| RUN02S(실행 02S) | squeeze density(압축 밀도 확대) | `19/7/26` | `-2.50 / 0.99` | `32.56 / 1.69` | 가장 가까운 생존 신호지만 거래 수가 작음 |

효과(effect, 효과): RUN02S(실행 02S)는 약한 회수 가치(weak salvage value, 약한 회수 가치)로 보존한다. RUN02Q(실행 02Q)는 bear-vortex short(하락 보텍스 숏)을 느슨하게 넓히면 손상이 커진다는 부정 기억(negative memory, 부정 기억)이고, RUN02R(실행 02R)는 validation-only repair(검증만 복구)로 남긴다.

RUN02T~RUN02V(실행 02T~02V)는 우선순위(priority, 우선순위) 1/2/3을 구조 탐침(structural probe, 구조 탐침)으로 정리한 묶음이다.

| run(실행) | priority(우선순위) | source(원천) | primary read(핵심 판독) | judgment(판정) |
|---|---:|---|---|---|
| RUN02T(실행 02T) | 1 | RUN02S(실행 02S) | fwd18(90분) OOS hit rate(표본외 적중률) `0.714286`, fwd12(60분)는 `0.285714`, 비교 가능 OOS 신호 `7`개 | `horizon_shift_worth_retraining_probe` |
| RUN02U(실행 02U) | 2 | RUN02S(실행 02S) | OOS(표본외) window(구간) 3개 모두 신호는 있지만 총 신호 `10`개뿐 | `wfo_lite_density_insufficient_for_full_wfo` |
| RUN02V(실행 02V) | 3 | RUN02P/RUN02Q(실행 02P/02Q) | RUN02Q(실행 02Q)는 RUN02P(실행 02P)보다 숏 신호가 `2.1x`지만 OOS 숏 hit rate(표본외 숏 적중률)는 `0.190476`로 낮음 | `short_specific_probe_inconclusive` |

효과(effect, 효과): 당시 판독은 full WFO(전체 워크포워드 최적화)보다 fwd18 label horizon(90분 라벨 예측수평선) 재학습 탐침의 정보량이 컸다는 것이다. 이 질문은 RUN02W~RUN02AK(실행 02W~02AK) 안에서 닫혔다.

RUN02W(실행 02W)는 그 1순위 질문을 MT5(메타트레이더5)까지 연결한 fwd18 retrain runtime_probe(fwd18 재학습 런타임 탐침)이다.

| view(보기) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---:|---:|---|
| Tier A only(Tier A 단독) | `-495.84 / 0.28` | `-132.97 / 0.75` | negative(부정) |
| Tier B fallback-only(Tier B 대체 단독) | `197.17 / 8.31` | `-105.73 / 0.70` | validation-only(검증만 양수) |
| Routed total(라우팅 전체) | `-496.25 / 0.28` | `-216.12 / 0.67` | negative(부정) |

효과(effect, 효과): fwd18(90분) 라벨만 바꾸는 단순 재학습은 MT5 거래 품질을 회복하지 못했다. 하지만 invalid(무효)는 아니며, fwd18 + context/rank threshold(문맥/순위 임계값) 확인으로 이어진 Stage 11(11단계) 내부 근거다.

RUN02X~RUN02Z(실행 02X~02Z)는 fwd18 + context/rank threshold(fwd18 + 문맥/순위 임계값)를 실제로 더 판 묶음이다.

| run(실행) | method(방식) | validation read(검증 판독) | OOS read(표본외 판독) | meaning(의미) |
|---|---|---:|---:|---|
| RUN02X(실행 02X) | direct fwd18 rank threshold(직접 fwd18 순위 임계값) | Tier A q96 hit(적중률) `0.25` | Tier A q96 hit(적중률) `0.15625` | direct(직접) 방향은 약함 |
| RUN02Y(실행 02Y) | inverse fwd18 rank threshold(역방향 fwd18 순위 임계값) | Tier A q96 hit(적중률) `0.604167` | Tier A q96 hit(적중률) `0.34375` | inverse(역방향)만으로는 부족 |
| RUN02Z(실행 02Z) | inverse rank + DI/ADX context(역방향 순위 + DI/ADX 문맥) | MT5 routed(라우팅) `386.06 / 7.25 / 9 trades(거래)` | MT5 routed(라우팅) `352.63 / 52.03 / 5 trades(거래)` | 작은 표본 양수 런타임 탐침 |

효과(effect, 효과): RUN02Z(실행 02Z)는 fwd18(90분) 모델이 고확신으로 말한 방향을 그대로 믿는 게 아니라, DI spread/ADX(DI 차이/ADX)가 낮은 문맥에서 inverse(역방향)로 쓰면 거래 품질이 살아날 수 있다는 첫 MT5(메타트레이더5) 단서를 남겼다. 다만 validation(검증) `9`거래, OOS(표본외) `5`거래라 아직 promotion_candidate(승격 후보)나 alpha quality(알파 품질)가 아니다.

RUN02AA~RUN02AK(실행 02AA~02AK)는 RUN02Z(실행 02Z)를 압박한 묶음이다.

| axis(축) | best read(최고 판독) | weak read(약한 판독) | meaning(의미) |
|---|---|---|---|
| ADX cutoff(ADX 절단값) | `ADX<=25` RUN02Z(실행 02Z) OOS `352.63 / 52.03 / 5 trades(거래)` | `ADX<=20` RUN02AA(실행 02AA) OOS `31.62 / 2.80 / 2 trades(거래)` | 너무 좁히면 OOS(표본외)가 마른다 |
| routing(라우팅) | routed(라우팅) RUN02Z(실행 02Z) OOS `352.63 / 5 trades(거래)` | Tier A-only(Tier A 단독) RUN02AD(실행 02AD) OOS `241.95 / 2 trades(거래)` | Tier B fallback(Tier B 대체)이 밀도와 순수익을 보탠다 |
| session slice(세션 구간) | `200-220` RUN02Z(실행 02Z) OOS `352.63 / 52.03` | `190-210` RUN02AI(실행 02AI)는 validation-heavy(검증 치우침) | 중심 구간 유지가 낫다 |

효과(effect, 효과): Stage 11(11단계) 안에서는 `ADX<=25`, routed(라우팅), `200-220` 중심이 가장 값진 닫힌 단서로 남는다. 표본이 작아서 운영 의미(operational meaning, 운영 의미)는 없다.

## 현재 Stage 12 상태(Current Stage 12 State, 현재 Stage 12 상태)

- 활성 단계(active stage, 활성 단계): `12_model_family_challenge__extratrees_training_effect`.
- 현재 실행(current run, 현재 실행): `run03F_et_v11_tier_balance_mt5_v1`.
- 독립 경계(standalone boundary, 독립 경계): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력은 사용하지 않는다.
- 최신 Python 패키지(latest Python package, 최신 파이썬 패키지): `run03D_et_standalone_batch20_v1`.
- 이전 MT5 런타임 탐침(previous MT5 runtime probe, 이전 MT5 런타임 탐침): `run03E_et_batch20_top_v11_mt5_probe_v1`.
- 최신 MT5 런타임 탐침(latest MT5 runtime probe, 최신 MT5 런타임 탐침): `run03F_et_v11_tier_balance_mt5_v1`.
- 검증 대상(target, 대상): `v11_base_leaf20_q85`.
- Python 검증/표본외 적중(Python validation/OOS hit, 파이썬 검증/표본외 적중): `0.392688` / `0.457317`.
- MT5 검증 routed net/PF/trades(MT5 검증 라우팅 순손익/수익팩터/거래): `-194.48` / `0.90` / `444`.
- MT5 표본외 routed net/PF/trades(MT5 표본외 라우팅 순손익/수익팩터/거래): `546.79` / `1.47` / `368`.
- Tier A/B 단독 표본외 net(Tier A/B only OOS net, 티어 A/B 단독 표본외 순손익): `399.59` / `88.69`.
- 판정(judgment, 판정): `inconclusive_runtime_probe_tier_balance_supplement_completed`.
- 효과(effect, 효과): RUN03F는 RUN03D 대표 변형의 Tier A 단독, Tier B 단독, A+B 라우팅을 MT5까지 보강했다. 그래도 runtime_probe(런타임 탐침)일 뿐 alpha quality(알파 품질)나 operating promotion(운영 승격)은 아니다.

## 현재 KPI 재구축/운영 포맷 상태(Current KPI Rebuild / Operating Format State, 현재 KPI 재구축 / 운영 포맷 상태)

- 운영 포맷(operating format, 운영 포맷): `work_packet(작업 묶음)`, `run_plan(실행 계획)`, `skill_receipt(스킬 영수증)`, `KPI source authority(KPI 원천 권위)`, `n/a reason(해당없음 사유)` 계약이 물질화됐다.
- 목록 묶음(inventory packet, 목록 묶음): `kpi_rebuild_inventory_v1`, 대상 실행(target runs, 대상 실행) `70`.
- MT5 기록 묶음(MT5 recording packet, MT5 기록 묶음): `kpi_rebuild_mt5_recording_v1`, MT5 보고서 확인 실행 `65 / 70`, normalized KPI rows(정규화 KPI 행) `448`.
- MT5 실행 묶음(MT5 execution packet, MT5 실행 묶음): `kpi_rebuild_mt5_execution_v1`, 추가 테스터 실행 `22 / 22` 완료, 차단 실행(blocked runs, 차단 실행) `5`.
- 거래 귀속 묶음(trade attribution packet, 거래 귀속 묶음): `kpi_trade_attribution_v1`, 거래 귀속 필요 행 `266`, 채운 행 `241`, zero-trade rows(거래 0개 행) `25`, trade-level rows(거래 단위 행) `15,803`, parser errors(파서 오류) `0`.
- 티어 균형 보강 묶음(tier-balance completion packet, 티어 균형 보강 묶음): `kpi_tier_balance_completion_v1`, 보강 실행 `6 / 6`, MT5 시도 `36 / 36`, normalized KPI rows(정규화 KPI 행) `60`, trade attribution rows(거래 귀속 행) `35`, trade-level rows(거래 단위 행) `1,837`, parser errors(파서 오류) `0`.
- GitHub 동기화(GitHub sync, 깃허브 동기화): KPI 재구축 산출물은 `1b557a463f49005bcf5e8bac5b128037b653fa0e`에 반영됐고, 이 문서 동기화 이후 최신 푸시 상태는 git HEAD(깃 HEAD)를 기준으로 읽는다.
- 효과(effect, 효과): KPI 재구축은 Stage 10~12(10~12단계) 증거를 같은 7-layer KPI(7층 KPI) 형식으로 읽게 하지만, Stage 12 알파 품질(alpha quality, 알파 품질)이나 운영 승격(operating promotion, 운영 승격)을 만들지는 않는다.

## 현재 코드 표면/모듈화 상태(Current Code Surface / Modularization State, 현재 코드 표면 / 모듈화 상태)

- 코드 표면 감사(code-surface audit, 코드 표면 감사): `python -m foundation.control_plane.code_surface_audit --root .`가 `pass(통과)`한다.
- 기준선(baseline, 기준선): `docs/agent_control/code_surface_baseline.yaml`이 큰 파일(line budget, 줄 예산)과 직접 import(가져오기) 금지 규칙을 가진다.
- 실제 수정(actual refactor, 실제 리팩터): MT5 Strategy Tester report parser(MT5 전략 테스터 보고서 파서)를 `foundation/mt5/strategy_report.py`로 옮겼고, `foundation/control_plane(제어면)`의 직접 Stage10 pipeline import(10단계 파이프라인 직접 가져오기)를 끊었다.
- 남은 부채(remaining debt, 남은 부채): `foundation/mt5/runtime_support.py`는 아직 Stage10 orchestration(10단계 조율 파일)에 일부 MT5 runtime helper(런타임 도구)를 위임하는 compatibility shim(호환 어댑터)이다.
- 효과(effect, 효과): 앞으로 큰 pipeline/EA(파이프라인/EA)를 더 키우거나 제어면에서 단계 파일을 직접 재사용하면 audit(감사)이 먼저 잡는다.

## 현재 Codex 제어면 상태(Current Codex Control Plane State, 현재 코덱스 제어면 상태)

- control packet(제어 묶음): `codex_control_plane_v2_incremental_v1`
- 핵심 구조(core structure, 핵심 구조): prompt(프롬프트)를 work family(작업군), surface(작업 표면), risk vector(위험축), decision lock(결정 고정), evidence gate(근거 제한문), final claim(최종 주장)으로 나눈다.
- 상태 감사(state sync audit, 상태 동기화 감사): RUN03E/RUN03F 충돌을 먼저 `blocked(차단)`로 잡았고, RUN03F 기준 동기화 후 `pass(통과)`했다.
- 마감 제한문(closeout gate, 마감 제한문): work packet schema(작업 묶음 스키마), skill receipt lint(스킬 영수증 존재 검사), skill receipt schema(스킬 영수증 내용 검사), state sync audit(상태 동기화 감사)를 묶어 `completed(완료)` 주장을 제한한다.
- 효과(effect, 효과): Codex가 작업을 축소하거나 근거 없이 완료라고 말하면, 사람이 눈치채기 전에 기계 gate(제한문)가 먼저 막는 구조로 바뀌었다.

## 현재 경계(Current Boundary, 현재 경계)

현재 상태는 아직 alpha-ready(알파 준비 완료), official alpha result(공식 알파 결과), live readiness(실거래 준비), operating promotion(운영 승격)이 아니다.

Stage 10(10단계) `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)`를 실행했다는 뜻은 200~220 closeout runtime_probe(마감 런타임 탐침)를 완료했다는 뜻이다. Stage 11(11단계) `RUN02A~RUN02S(실행 02A~02S)`는 LightGBM(라이트GBM) 학습방법, LGBM-specific threshold(LGBM 전용 임계값), 발산형/아이디어 무더기/회수 확장 runtime_probe(런타임 탐침)를 완료했다는 뜻이다. `RUN02T~RUN02V(실행 02T~02V)`와 `RUN02X~RUN02Y(실행 02X~02Y)`는 Python structural probe(파이썬 구조 탐침)이고, `RUN02W/RUN02Z/RUN02AA~RUN02AK(실행 02W/02Z/02AA~02AK)`는 MT5 runtime_probe(MT5 런타임 탐침) 또는 그 인계물이다. `RUN02AL~RUN02AP(실행 02AL~02AP)`는 빠진 Tier A/B/routed(Tier A/B/라우팅) 보강 실행이다. Stage 12(12단계) `RUN03D(실행 03D)`는 standalone batch20 Python structural scout(단독 20개 묶음 파이썬 구조 탐색), `RUN03E(실행 03E)`는 이전 Tier A 단독 MT5 runtime_probe(이전 Tier A 단독 MT5 런타임 탐침), `RUN03F(실행 03F)`는 Tier A/B/routed MT5 tier-balance supplement(티어 균형 보강)다. 아직 full WFO(전체 워크포워드 최적화) 결과, alpha quality(알파 품질), operating_promotion(운영 승격)은 없다.

KPI 재구축 묶음(KPI rebuild packets, KPI 재구축 묶음)은 evidence management(근거 관리) 산출물이다. 현재 판정을 더 정확히 읽게 하지만, 새 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 만들지 않는다.

코드 표면 감사(code-surface audit, 코드 표면 감사)는 운영 가드(operating guard, 운영 제한문)다. 큰 파일이 존재한다는 사실을 숨기지 않고, 새 코드가 그 부채를 더 키우는 일을 막는다.

Codex 제어면 v2(Control Plane v2, 제어면 v2)는 코덱스 작업 운영 가드다. 이것은 거래 alpha quality(알파 품질), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격)을 만들지 않는다.

## 닫힌 기억(Closed Memory, 닫힌 기억)

- Stage 12(12단계)는 열려 있고, `RUN03F(실행 03F)` ExtraTrees(엑스트라 트리) v11 Tier A/B/routed MT5 tier-balance supplement(Tier A/B/라우팅 MT5 티어 균형 보강)가 현재 실행이다.
- `RUN03D(실행 03D)` ExtraTrees(엑스트라 트리)는 최신 standalone Python batch package(단독 파이썬 20개 묶음)다.
- `RUN03C(실행 03C)` ExtraTrees(엑스트라 트리)는 이전 standalone MT5 runtime_probe(단독 MT5 런타임 탐침)다.
- `kpi_rebuild_inventory_v1/kpi_rebuild_mt5_recording_v1/kpi_rebuild_mt5_execution_v1/kpi_trade_attribution_v1/kpi_tier_balance_completion_v1(KPI 재구축 목록/MT5 기록/MT5 실행/거래 귀속/티어 균형 보강 묶음)`은 현재 교차 단계 KPI 증거다.
- `code_surface_audit(코드 표면 감사)`은 현재 코드 배치(code placement, 코드 배치)와 모듈화(module split, 모듈 분리)를 지키는 운영 가드다.
- `codex_control_plane_v2_incremental_v1(코덱스 제어면 v2 단계형 묶음)`은 작업군/표면/위험축/결정 고정/마감 제한문을 현재 운영 포맷으로 추가했다.
- `RUN03A(실행 03A)`는 Stage 10/11(10/11단계)을 끌고 와서 standalone evidence(단독 근거)가 아니다.
- Stage 11(11단계)은 `reviewed_closed_no_next_stage_opened(검토 후 닫힘, 다음 단계 미개방)` 상태다.
- `RUN02W(실행 02W)`는 fwd18-only retrain(fwd18 단독 재학습) 부정 런타임 기억이다.
- `RUN02X(실행 02X)` direct rank(직접 순위)는 구조 부정 기억이다.
- `RUN02Y(실행 02Y)` inverse rank alone(역방향 순위 단독)은 혼합 구조 기억이다.
- `RUN02Z/RUN02AA~RUN02AK(실행 02Z/02AA~02AK)`는 작은 표본 양수 중심 단서지만 promotion_candidate(승격 후보)가 아니다.
- `RUN02Q/RUN02R(실행 02Q/02R)`는 각각 느슨한 bear-vortex short density(하락 보텍스 숏 밀도 확대) 부정 기억과 validation-only repair(검증만 복구) 기억이다.
- 이 문서는 새 stage(단계)의 작업 지시를 남기지 않는다.

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
- Stage 11(11단계) `RUN02T~RUN02V(실행 02T~02V)` Python structural probe(파이썬 구조 탐침)를 MT5 runtime result(MT5 런타임 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- Stage 11(11단계) `RUN02A~RUN02S/RUN02W/RUN02Z/RUN02AA~RUN02AK(실행 02A~02S/02W/02Z/02AA~02AK)` LightGBM MT5 runtime_probe(라이트GBM MT5 런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- Stage 11(11단계) `RUN02Z/RUN02AA~RUN02AK(실행 02Z/02AA~02AK)`의 작은 표본 양수를 promotion_candidate(승격 후보), operating_promotion(운영 승격), runtime_authority expansion(런타임 권위 확장)으로 읽는 주장
- Stage 12(12단계) `RUN03A(실행 03A)`를 standalone evidence(단독 근거)로 읽는 주장
- Stage 12(12단계) `RUN03B(실행 03B)` ExtraTrees standalone Python structural scout(엑스트라 트리 단독 파이썬 구조 탐침)를 MT5 runtime evidence(MT5 런타임 근거)로 읽는 주장
- Stage 12(12단계) `RUN03C(실행 03C)` standalone MT5 runtime_probe(단독 MT5 런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- Stage 12(12단계) `RUN03F(실행 03F)` Tier A/B/routed MT5 tier-balance supplement(Tier A/B/라우팅 MT5 티어 균형 보강)를 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- `kpi_trade_attribution_v1(거래 귀속 묶음)`의 MFE/MAE(최대 유리/불리 이동)와 regime/slice attribution(국면/구간 귀속)을 운영 승격(operating promotion, 운영 승격)이나 새 알파 품질(alpha quality, 알파 품질)로 읽는 주장
