# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `10_alpha_scout__default_split_model_threshold_scan`
- status(상태): `active_run01A_completed_runtime_probe`
- lane(레인): `exploration(탐색)`
- scout boundary(탐색 판독 경계): `single_split_scout(단일 분할 탐색 판독)`
- current run(현재 실행): `run01A_logreg_threshold_mt5_scout_v1`
- current operating reference(현재 운영 기준): `none`

## 인계 조건(Handoff Condition, 인계 조건)

Stage 09(9단계)이 `stage09_pre_alpha_handoff_packet_v1` 묶음(packet, 묶음)으로 registry/current truth/publish boundary(등록부/현재 진실/게시 경계)를 닫고 Stage 10(10단계)로 인계했으므로 시작했다.

효과(effect, 효과): Stage 10(10단계)은 default split(기본 분할) 위에서 model/threshold scout(모델/임계값 탐색 판독)를 실행할 수 있다.

## 선택된 입력(Selected Inputs, 선택 입력)

- Stage 09 handoff packet(Stage 09 인계 묶음): `stages/09_pre_alpha_handoff__registry_publish_packet/03_reviews/pre_alpha_handoff_packet.md`
- Stage 08 protocol(Stage 08 규칙): `docs/policies/alpha_entry_protocol.md`
- Stage 08 report template(Stage 08 보고 틀): `docs/templates/alpha_exploration_report_template.md`
- selected model input(선택 모델 입력): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- default split(기본 분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`

## 현재 실행(Current Run, 현재 실행)

- run_id(실행 ID): `run01A_logreg_threshold_mt5_scout_v1`
- label(라벨): `stage10_Model__LogReg_MT5Scout`
- external verification status(외부 검증 상태): `completed(완료)`
- judgment(판정): `inconclusive_single_split_scout_mt5_routed_completed`
- routing mode(라우팅 방식): `tier_a_primary_tier_b_partial_context_fallback`
- evidence(근거): Python(파이썬) threshold sweep(임계값 스윕), ONNX(`Open Neural Network Exchange`, 온닉스) probability parity(확률 동등성), MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터) Tier A only/Tier B fallback-only/A+B routed validation/OOS(Tier A 단독/Tier B 대체 구간 단독/A+B 라우팅 검증/표본외)

MT5(`MetaTrader 5`, 메타트레이더5) validation_is(검증/표본내)는 Tier A only(Tier A 단독) net profit(순수익) `324.13`, profit factor(수익 팩터) `1.30`; Tier B fallback-only(Tier B 대체 구간 단독) net profit(순수익) `49.48`, profit factor(수익 팩터) `2.76`; A+B routed total(A+B 라우팅 전체) net profit(순수익) `355.65`, profit factor(수익 팩터) `1.33`이다.

MT5(`MetaTrader 5`, 메타트레이더5) OOS(표본외)는 Tier A only(Tier A 단독) net profit(순수익) `130.01`, profit factor(수익 팩터) `1.15`; Tier B fallback-only(Tier B 대체 구간 단독) net profit(순수익) `-19.15`, profit factor(수익 팩터) `0.87`; A+B routed total(A+B 라우팅 전체) net profit(순수익) `174.89`, profit factor(수익 팩터) `1.21`이다.

Tier B partial-context fallback(Tier B 부분 문맥 대체)은 validation_is(검증/표본내)에서 `2366`행, OOS(표본외)에서 `1062`행 사용됐다.

효과(effect, 효과)는 Tier A(티어 A)가 비운 구간을 Tier B(티어 B)가 실제로 메웠다는 사실을 기록하되, 이 결과를 alpha quality(알파 품질)나 operating promotion(운영 승격)으로 과장하지 않는 것이다.

## 경계(Boundary, 경계)

이 문서는 Stage 10(10단계)의 첫 runtime_probe(런타임 탐침)가 완료됐다는 뜻이다. 아직 alpha result(알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority expansion(런타임 권위 확장)을 뜻하지 않는다.
