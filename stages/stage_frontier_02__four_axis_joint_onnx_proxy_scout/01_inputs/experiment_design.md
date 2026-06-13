# Experiment Design(실험 설계)

Packet(작업 묶음): `frontier02A_proxy_score_spec_v1`

## Required Experiment Fields(필수 실험 항목)

- hypothesis(가설): directly trained ONNX(직접 학습 온엑스) surface(표면)를 위한 four-axis joint objective(네 축 동시 목적)는 density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 함께 보아 one-axis repair loop(한 축 수리 반복)를 줄일 수 있다.
- decision_use(결정 용도): first proxy scout(첫 프록시 탐색)를 실행할지, 어떤 score(점수)와 invalid condition(무효 조건)을 쓸지 정한다.
- comparison_baseline(비교 기준): no-trade baseline(무거래 기준)과 Stage364 negative memory(364단계 부정 기억)를 reference only(참조 전용)로 쓴다. selected baseline(선택 기준선)은 없다.
- control_variables(고정 변수): symbol/timeframe(심볼/시간프레임) `US100/M5`, FPMarkets data contract(FPMarkets 데이터 계약), closed-bar only(확정봉 전용), feature order hash(피처 순서 해시) `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`, train/validation/OOS split(학습/검증/표본외 분할).
- changed_variables(변경 변수): proxy score(프록시 점수), joint selection objective(동시 선택 목적), sparse PF penalty(희소 PF 벌점), DD segment penalty(구간 손실폭 벌점), curve smoothness penalty(곡선 매끄러움 벌점).
- sample_scope(표본 범위): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet` and selected model input(선택 모델 입력) `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`; train `2022-09-01` to `2024-12-31`, validation `2025-01-01` to `2025-09-30`, OOS `2025-10-01` to `2026-04-13`.
- success_criteria(성공 기준): scout clue(탐색 단서) exists if at least one surface(표면) improves aspiration_distance_score(목표 거리 점수) without hiding sparse PF(희소 PF), DD(손실폭), or Tier B/combined gap(Tier B/합산 공백).
- failure_criteria(실패 기준): no surface(표면) improves joint distance(동시 거리), or all improvements are one-axis only(한 축 전용), sparse(희소), or proxy-only(프록시 전용) without usable next question(쓸 수 있는 다음 질문).
- invalid_conditions(무효 조건): timestamp leakage(타임스탬프 누수), label leakage(라벨 누수), feature order mismatch(피처 순서 불일치), split contamination(분할 오염), missing source artifact(원천 산출물 누락), non-reproducible score code(재현 불가 점수 코드).
- stop_conditions(중지 조건): capped repair(상한 수리) two same-axis repeats(같은 축 2회 반복), missing required data(필수 데이터 누락), Grok pre-expensive review rejection(비싼 검증 전 그록 거절), or local gate failure(로컬 게이트 실패).
- evidence_plan(근거 계획): proxy_score_plan(프록시 점수 계획), run_manifest(실행 목록), Tier A/B/combined rows(티어 A/B/합산 행), artifact hashes(산출물 해시), run registry(실행 등록부), stage ledger(단계 장부), and no-authority claim guard(권위 없음 주장 가드).

## Exploration Mandate Fields(탐색 규율 항목)

- idea_id(아이디어 ID): `IDEA-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT`
- legacy_relation(레거시 관계): `prior_evidence_only(이전 근거 전용)` for Stage12~364(12~364단계); no legacy code(레거시 코드 없음).
- tier_scope(티어 범위): Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산) required when first proxy validation run(첫 프록시 검증 실행) materializes. Stage-open packet(단계 개방 작업 묶음)은 no trading KPI(거래 KPI 없음).
- broad_sweep(넓은 탐색): compare joint score variants(동시 점수 변형) for density/PF/DD/smoothness weights(밀도/수익 팩터/손실폭/매끄러움 가중치), sparse penalties(희소 벌점), and curve penalties(곡선 벌점).
- extreme_sweep(극단 탐색): include high-density/low-PF(고밀도/낮은 PF), high-PF/sparse(높은 PF/희소), low-DD/flat-curve(낮은 손실폭/평탄 곡선), smooth-but-thin(매끄럽지만 얇은) boundary cases(경계 사례).
- micro_search_gate(미세 탐색 게이트): only after broad sweep(넓은 탐색) has at least one non-sparse joint scout clue(비희소 동시 탐색 단서).
- wfo_plan(WFO 계획): WFO(워크포워드 최적화)는 scout survivor(탐색 생존 표면)가 생긴 뒤, Grok pre-expensive review(비싼 검증 전 그록 검토)와 local verification(로컬 검증) 뒤에만 실행한다.
- failure_memory(실패 기억): negative closeout(부정 마감)은 failed axis(실패 축), variants tried(시도 변형), salvage value(회수 가치), reopen condition(재개 조건), DNR note(반복 금지 메모)를 남긴다.
- evidence_boundary(근거 경계): stage-open design only(단계 개방 설계 전용); no model training(모델 학습 없음), no MT5(메타트레이더5 없음), no authority(권위 없음).

## Data Integrity Boundary(데이터 무결성 경계)

- data_source(데이터 원천): current contracts(현재 계약)에 적힌 training and model input parquet(학습 및 모델 입력 파케이).
- time_axis(시간축): broker-clock alignment key(브로커 시계 정렬 키) and event UTC/session mapper(이벤트 UTC/세션 매퍼) policy(정책)를 따른다.
- feature_label_boundary(피처-라벨 경계): features(피처)는 closed bar(확정봉)까지, label(라벨)은 fwd12(12봉 전방)로 분리한다.
- split_boundary(분할 경계): time-ordered train/validation/OOS(시간순 학습/검증/표본외)만 쓴다.
- leakage_risk(누수 위험): score design(점수 설계)이 OOS(표본외)를 selector training(선택기 학습)에 섞는 경우.
- integrity_judgment(무결성 판정): usable_with_boundary(경계付き 사용 가능) for design(설계); actual run(실제 실행) 전 hash and row count(해시와 행 수) 재확인 필요.

## Model Validation Boundary(모델 검증 경계)

- model_family(모델군): ONNX-ready tabular model family(ONNX 준비 표형 모델군), exact model(정확 모델) not selected(선택 안 됨).
- target_and_label(목표와 라벨): fwd12 3-class direction label(12봉 전방 3분류 방향 라벨) unless later packet(다음 작업 묶음)이 새 label contract(라벨 계약)를 연다.
- split_method(분할 방법): time-ordered train/validation/OOS(시간순 학습/검증/표본외), WFO later(나중).
- selection_metric(선택 지표): aspiration_distance_score(목표 거리 점수) plus joint_pass_count(동시 통과 수), not single PF(단일 PF 아님).
- overfit_risk(과적합 위험): repeated score tuning(반복 점수 조정), OOS-driven selection(OOS 기반 선택), sparse PF(희소 PF).
- calibration_risk(보정 위험): model output(모델 출력)은 probability(확률)로 말하지 않고 calibration evidence(보정 근거)가 생기기 전에는 rank/score(순위/점수)로 둔다.
- validation_judgment(검증 판정): exploratory_design_only(탐색 설계 전용).
