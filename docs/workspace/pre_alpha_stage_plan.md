# Pre-Alpha Stage Plan

## 목적(Purpose, 목적)

이 문서는 model-backed alpha exploration(모델 근거 알파 탐색) 전에 끝내야 할 작업을 stage(단계)별로 나눈다.

효과(effect, 효과)는 남은 작업이 한 단계 안에서 섞이거나, 다음 작업 때 drift(드리프트, 방향 이탈)를 일으키지 않게 하는 것이다.

## 현재 원칙(Current Principle, 현재 원칙)

정식 alpha exploration(알파 탐색) 전 경로는 58 feature(58개 피처) 기준이다.

현재 상태(current state, 현재 상태): Stage 04~09(4~9단계)는 `stage09_pre_alpha_handoff_packet_v1`로 닫혔고, Stage 10(10단계)은 `stage10_alpha_scout_closeout_packet_v1`로 닫혔다. 효과(effect, 효과)는 Stage 11(11단계) `11_alpha_robustness__wfo_label_horizon_sensitivity`가 `run01Y(실행 01Y)` 기준선을 WFO(`walk-forward optimization`, 워크포워드 최적화)와 label/horizon sensitivity(라벨/예측수평선 민감도)로 압박할 수 있다는 것이다.

Stage 04(4단계)에서 만든 56 feature(56개 피처) model input(모델 입력)은 `placeholder_equal_weight(임시 동일가중)` 오염을 막기 위한 interim quarantine artifact(임시 격리 산출물)이다. 최종 pre-alpha(알파 전) 경로가 아니다.

Stage 04(4단계)의 정식 58 feature(58개 피처) 경로는 `MT5 price-proxy weights(MT5 가격 대리 가중치)`로 물질화했다. 이것은 actual NDX/QQQ weights(실제 NDX/QQQ 가중치)가 아니다.

## Stage Queue(단계 대기열)

### Stage 04(4단계): `04_model_input_readiness__weights_parity_feature_audit`

소유 질문(owner question, 소유 질문): MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)를 만들고 58 feature(58개 피처) model input(모델 입력)을 다시 고정할 수 있는가?

맡는 작업:

- MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치) 계약
- MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치) 생성
- 58 feature set(58개 피처 세트) 복구
- feature frame(피처 프레임), training dataset(학습 데이터셋), model input(모델 입력) 재물질화
- 56 feature(56개 피처) interim quarantine artifact(임시 격리 산출물)를 최종 경로가 아닌 보조 근거로 표시

### Stage 05(5단계): `05_feature_integrity__formula_time_alignment_leakage_audit`

소유 질문(owner question, 소유 질문): 58 feature(58개 피처), 시간축(time axis, 시간축), 외부 정렬(external alignment, 외부 정렬), label(라벨)에 leakage(누수)나 계산 오류가 없는가?

맡는 작업:

- feature formula audit(피처 공식 감사)
- session/time audit(세션/시간 감사)
- external alignment audit(외부 정렬 감사)
- label leakage audit(라벨 누수 감사)
- Tier A/B(티어 A/B) sample label(표본 라벨) 보존 규칙 확인

### Stage 06(6단계): `06_runtime_parity__python_mt5_runtime_authority`

소유 질문(owner question, 소유 질문): Python/MT5 parity(파이썬/MT5 동등성)와 full MT5 runtime authority(완전 MT5 런타임 권위)를 alpha exploration(알파 탐색) 전 기준으로 닫을 수 있는가?

맡는 작업:

- parity fixture plan(동등성 검사 표본 계획)
- Python snapshot(파이썬 스냅샷), MT5 snapshot(MT5 스냅샷), parity report(동등성 보고서)
- stale MT5 audit tools(낡은 MT5 감사 도구) 폐기 또는 갱신
- 58 feature(58개 피처) input order(입력 순서), hash(해시), model handoff(모델 인계) 확인
- full MT5 runtime authority(완전 MT5 런타임 권위) 차단 사유 또는 완료 근거 기록

### Stage 07(7단계): `07_model_training_baseline__contract_preprocessing_smoke`

소유 질문(owner question, 소유 질문): 첫 baseline model training(기준선 모델 학습)을 재현 가능한 run(실행)으로 만들 수 있는가?

맡는 작업:

- scaler/preprocessing policy(스케일러/전처리 정책)
- model training run contract(모델 학습 실행 계약)
- baseline smoke training(기준선 스모크 학습)
- baseline report template(기준선 보고서 틀)
- model artifact identity(모델 산출물 정체성)와 registry(등록부) 기록

### Stage 08(8단계): `08_alpha_entry_protocol__tier_reporting_search_rules`

소유 질문(owner question, 소유 질문): alpha exploration(알파 탐색)을 어떤 규칙으로 시작하고, Tier A/B(티어 A/B)를 어떻게 보고할 것인가?

맡는 작업:

- alpha search protocol(알파 탐색 규칙)
- single split scout(단일 분할 탐색 판독)와 WFO(walk-forward optimization, 워크포워드 최적화) 경계
- Tier A/B(티어 A/B) result reporting(결과 보고) 규칙
- negative result memory(부정 결과 기억)와 idea registry(아이디어 등록부) 규칙

### Stage 09(9단계): `09_pre_alpha_handoff__registry_publish_packet`

소유 질문(owner question, 소유 질문): alpha exploration(알파 탐색)을 열기 전에 registry(등록부), changelog(변경기록), commit/PR(커밋/PR) 경계를 깔끔하게 묶었는가?

맡는 작업:

- run/artifact registry(실행/산출물 등록부) 최종 정합성
- current truth docs(현재 진실 문서) 동기화
- foundation build commit/PR(기반 구축 커밋/PR) 경계
- alpha entry packet(알파 진입 묶음) 작성

## 금지되는 Drift(금지되는 드리프트)

- Stage 04(4단계)에서 model training(모델 학습)을 시작하지 않는다.
- Stage 05(5단계)에서 alpha selection(알파 선택)을 시작하지 않는다.
- Stage 06(6단계)에서 operating promotion(운영 승격)을 주장하지 않는다.
- Stage 07(7단계)의 smoke training(스모크 학습)을 alpha quality(알파 품질)로 읽지 않는다.
- Stage 08(8단계) 전에는 alpha search result(알파 탐색 결과)를 공식 결과처럼 남기지 않는다.
- Stage 09(9단계) handoff packet(인계 묶음)을 alpha result(알파 결과)로 말하지 않는다.
- Stage 10(10단계)이 active(활성)라고 해서 alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
- Stage 11(11단계) scaffold(뼈대)를 Stage 11 run result(실행 결과), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)으로 말하지 않는다.
