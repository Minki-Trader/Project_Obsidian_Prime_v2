# Current Working State

- updated_on: `2026-04-27`
- project_mode: `clean_stage_restart`
- active_stage: `11_alpha_robustness__wfo_label_horizon_sensitivity`
- active_branch: `main`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 clean stage restart(깨끗한 단계 재시작) 이후 Stage 02~09(2~9단계)를 닫았다.

효과(effect, 효과): Stage 10(10단계)은 `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)` 200~220 closeout(마감) runtime_probe(런타임 탐침)로 닫혔다. Stage 11(11단계)은 `run01Y(실행 01Y)` 기준선을 WFO(`walk-forward optimization`, 워크포워드 최적화)와 label/horizon sensitivity(라벨/예측수평선 민감도)로 압박하는 단계로 열렸다.

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

Stage 11(11단계)의 질문(question, 질문)은 Stage 10(10단계)의 `run01Y(실행 01Y)` 기준 후보가 WFO(워크포워드 최적화)와 label/horizon sensitivity(라벨/예측수평선 민감도)에서도 구조적으로 버티는가다.

효과(effect, 효과): Stage 11(11단계)은 Stage 10(10단계)의 single_split_scout(단일 분할 탐색 판독)을 alpha quality(알파 품질)처럼 과장하지 않고, robustness scout(견고성 탐색 판독)로 다시 압박한다.

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

- status(상태): `active_scaffolded_no_runs_yet`
- baseline(기준선): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- selected slice(선택 구간): `200 < minutes_from_cash_open <= 220`
- selected hold(선택 보유): `9`
- selected threshold(선택 임계값): `short0.600_long0.450_margin0.000`
- selected routing mode(선택 라우팅 방식): `tier_a_primary_no_fallback`

효과(effect, 효과): Stage 11(11단계)은 열렸지만 아직 Stage 11 run(실행)은 없다.

## 현재 경계(Current Boundary, 현재 경계)

현재 상태는 아직 alpha-ready(알파 준비 완료), official alpha result(공식 알파 결과), live readiness(실거래 준비), operating promotion(운영 승격)이 아니다.

Stage 10(10단계) `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)`를 실행했다는 뜻은 200~220 closeout runtime_probe(마감 런타임 탐침)를 완료했다는 뜻이다. Stage 11(11단계) scaffold(뼈대)는 만들었지만 아직 WFO(워크포워드 최적화) 결과, promotion_candidate(승격 후보), operating_promotion(운영 승격)은 없다.

## 남은 작업(Open Items, 남은 작업)

- Stage 11(11단계): `run01Y(실행 01Y)` 기준선에서 첫 WFO/label-horizon sensitivity(WFO/라벨-예측수평선 민감도) 실행 묶음을 설계하기
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
