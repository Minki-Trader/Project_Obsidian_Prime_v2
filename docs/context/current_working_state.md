# Current Working State

- updated_on: `2026-04-26`
- project_mode: `clean_stage_restart`
- active_stage: `10_alpha_scout__default_split_model_threshold_scan`
- active_branch: `main`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 clean stage restart(깨끗한 단계 재시작) 이후 Stage 02~09(2~9단계)를 닫았다.

효과(effect, 효과): 이제 현재 작업은 Stage 10(10단계)의 첫 alpha scout(알파 탐색 판독)인 `run01A(실행 01A)`를 runtime_probe(런타임 탐침)로 완료한 상태다.

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

`10_alpha_scout__default_split_model_threshold_scan`

Stage 10(10단계)의 질문(question, 질문)은 default split(기본 분할) 위에서 첫 model-backed alpha scout(모델 근거 알파 탐색 판독)를 어떤 model/threshold candidate(모델/임계값 후보)로 시작할 것인가다.

효과(effect, 효과): Stage 10(10단계)은 Stage 08(8단계) protocol(규칙)과 Stage 09(9단계) handoff(인계)를 바탕으로 첫 `single_split_scout(단일 분할 탐색 판독)`을 실행했고, 그 실행을 runtime_probe(런타임 탐침) 경계로 읽는다.

## 탐색 원칙(Exploration Rule, 탐색 원칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 탐색 게이트(exploration gate, 탐색 제한문)가 아니다.

둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 sample label(표본 라벨)이다.

효과(effect, 효과): 보고서(report, 보고서)는 무엇을 탐색했는지 정직하게 라벨링(labeling, 라벨링)하되, 티어(tier, 티어)를 아이디어 승인이나 거절로 쓰지 않는다.

Stage 10(10단계) 이후 alpha exploration run(알파 탐색 실행)은 Tier A(티어 A), Tier B(티어 B), Tier A+B combined(Tier A+B 합산)를 함께 남긴다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서는 이 뜻이 `Tier A primary(티어 A 우선)`, `Tier B fallback(티어 B 대체)`, `actual routed total(실제 라우팅 전체)`이다.

효과(effect, 효과): Tier A(티어 A)만 본 결과가 전체 alpha read(알파 판독)처럼 남지 않고, Tier B(티어 B)가 실제로 메운 구간과 전체 라우팅 결과를 같은 실행(run, 실행)에서 비교한다.

Stage 10(10단계)의 기본 레인(lane, 레인)은 `exploration(탐색)`이고 첫 경계(boundary, 경계)는 `single_split_scout(단일 분할 탐색 판독)`다.

## 현재 실행(Current Run, 현재 실행)

`run01A_logreg_threshold_mt5_scout_v1`

- label(라벨): `stage10_Model__LogReg_MT5Scout`
- external verification status(외부 검증 상태): `completed(완료)`
- judgment(판정): `inconclusive_single_split_scout_mt5_routed_completed`
- routing mode(라우팅 방식): `tier_a_primary_tier_b_partial_context_fallback`
- boundary(경계): `runtime_probe(런타임 탐침)`
- key artifacts(핵심 산출물): `run_manifest.json`, `kpi_record.json`, MT5 Strategy Tester report(MT5 전략 테스터 리포트)

효과(effect, 효과): Python(파이썬) threshold sweep(임계값 스윕), ONNX(`Open Neural Network Exchange`, 온닉스) parity(동등성), MT5(`MetaTrader 5`, 메타트레이더5) Tier A only/Tier B fallback-only/A+B routed(Tier A 단독/Tier B 대체 구간 단독/A+B 라우팅) validation/OOS(검증/표본외) 수익·위험·실행 KPI(핵심 성과 지표)를 한 실행 근거(run evidence, 실행 근거)로 묶었다.

run01A(실행 01A)의 routing coverage(라우팅 커버리지)는 Tier A primary(Tier A 우선) `46650`행, Tier B partial-context fallback(Tier B 부분 문맥 대체) `12398`행, no_tier labelable(티어 없음 라벨 가능) `1053`행이다.

MT5(`MetaTrader 5`, 메타트레이더5) validation_is(검증/표본내)는 Tier A only(Tier A 단독) net profit(순수익) `324.13`, profit factor(수익 팩터) `1.30`, max drawdown(최대 손실) `144.98`, recovery factor(회복 계수) `2.24`; Tier B fallback-only(Tier B 대체 구간 단독) net profit(순수익) `49.48`, profit factor(수익 팩터) `2.76`, max drawdown(최대 손실) `40.59`, recovery factor(회복 계수) `1.22`; A+B routed total(A+B 라우팅 전체) net profit(순수익) `355.65`, profit factor(수익 팩터) `1.33`, max drawdown(최대 손실) `146.24`, recovery factor(회복 계수) `2.43`, fill count(체결 수) `461`이다.

MT5(`MetaTrader 5`, 메타트레이더5) OOS(표본외)는 Tier A only(Tier A 단독) net profit(순수익) `130.01`, profit factor(수익 팩터) `1.15`, max drawdown(최대 손실) `198.17`, recovery factor(회복 계수) `0.66`; Tier B fallback-only(Tier B 대체 구간 단독) net profit(순수익) `-19.15`, profit factor(수익 팩터) `0.87`, max drawdown(최대 손실) `140.92`, recovery factor(회복 계수) `-0.14`; A+B routed total(A+B 라우팅 전체) net profit(순수익) `174.89`, profit factor(수익 팩터) `1.21`, max drawdown(최대 손실) `209.15`, recovery factor(회복 계수) `0.84`, fill count(체결 수) `396`이다.

Tier B fallback subtype(티어 B 대체 하위유형)는 전체 기준 `B_macro_missing(B 거시 결측)` `10740`, `B_mixed_partial_context(B 혼합 부분 문맥)` `1240`, `B_full_context_outside_tier_a_scope(B 전체문맥이나 Tier A 밖)` `217`, `B_core_only(B 핵심만)` `200`, `B_constituent_missing(B 구성종목 결측)` `1`이다.

효과(effect, 효과): Tier A(티어 A)의 all skip(전체 스킵) 구간 중 Tier B(티어 B)가 실제로 메운 부분과 여전히 no_tier(티어 없음)로 남은 부분을 분리하고, A 단독(A only, A 단독)과 B 단독(B fallback-only, B 대체 구간 단독)이 A+B 라우팅(A+B routed, A+B 라우팅)에 무엇을 보탰는지 비교한다. 단, 이는 single_split runtime_probe(단일 분할 런타임 탐침)이지 alpha quality(알파 품질)나 operating promotion(운영 승격)이 아니다.

## 현재 경계(Current Boundary, 현재 경계)

현재 상태는 아직 alpha-ready(알파 준비 완료), official alpha result(공식 알파 결과), live readiness(실거래 준비), operating promotion(운영 승격)이 아니다.

Stage 10(10단계) `run01A(실행 01A)`를 실행했다는 뜻은 first runtime probe(첫 런타임 탐침)를 완료했다는 뜻이다. 아직 WFO(워크포워드 최적화), promotion_candidate(승격 후보), operating_promotion(운영 승격)은 없다.

## 남은 작업(Open Items, 남은 작업)

- Stage 10(10단계): `run01A(실행 01A)`를 inconclusive runtime probe(불충분 런타임 탐침)로 해석하고 다음 scout variant(탐색 변형)를 고르기
- `run01A(실행 01A)`의 Tier A only/Tier B fallback-only/A+B routed(Tier A 단독/Tier B 대체 구간 단독/A+B 라우팅) 장부와 KPI(핵심 성과 지표)를 다음 실행 비교 기준으로 유지하기
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
- Stage 10(10단계) `run01A(실행 01A)` runtime probe(런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), runtime authority expansion(런타임 권위 확장), operating promotion(운영 승격)으로 읽는 주장
