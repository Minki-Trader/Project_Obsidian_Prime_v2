# Current Working State

- updated_on: `2026-04-25`
- project_mode: `clean_stage_restart`
- active_stage: `09_pre_alpha_handoff__registry_publish_packet`
- active_branch: `main`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 clean stage restart(깨끗한 단계 재시작) 이후 Stage 02~08(2~8단계)을 닫았다.

효과(effect, 효과): 이제 현재 작업은 alpha exploration(알파 탐색) 자체가 아니라, Stage 09(9단계)의 registry/current truth/publish handoff(등록부/현재 진실/게시 인계) 정리다.

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

## 최근 닫힌 Stage 08(최근 닫힌 8단계)

`08_alpha_entry_protocol__tier_reporting_search_rules`

Stage 08(8단계)는 alpha entry protocol(알파 진입 규칙)과 Tier A/B reporting rule(티어 A/B 보고 규칙)을 닫았다.

- packet_id(묶음 ID): `stage08_alpha_entry_protocol_v1`
- status(상태): `reviewed_closed_handoff_to_stage09_complete_with_alpha_entry_protocol`
- judgment(판정): `positive_alpha_entry_protocol_defined`
- policy(정책): `docs/policies/alpha_entry_protocol.md`
- report template(보고 틀): `docs/templates/alpha_exploration_report_template.md`
- review(검토): `stages/08_alpha_entry_protocol__tier_reporting_search_rules/03_reviews/alpha_entry_protocol_review.md`

효과(effect, 효과): allowed evidence(허용 근거), metric/report format(지표/보고 형식), overfit/trial accounting(과최적화/실험 회계), selected legacy-derived metrics(선택된 레거시 유래 지표), Tier A/B reporting(티어 A/B 보고), failure memory rule(실패 기억 규칙), no-promotion boundary(승격 아님 경계)가 공식 규칙으로 고정됐다.

경계(boundary, 경계): Stage 08(8단계)은 official alpha result(공식 알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 만들지 않았다.

## 현재 단계(Current Stage, 현재 단계)

`09_pre_alpha_handoff__registry_publish_packet`

Stage 09(9단계)의 질문(question, 질문)은 alpha exploration(알파 탐색)을 열기 전에 registry(등록부), current truth(현재 진실), changelog(변경기록), commit/PR boundary(커밋/PR 경계), alpha entry packet(알파 진입 묶음)을 깔끔하게 묶었는가다.

효과(effect, 효과): Stage 09(9단계)가 닫히면 model-backed alpha exploration(모델 근거 알파 탐색)을 공식 결과로 남길 수 있는 진입 묶음(entry packet, 진입 묶음)이 생긴다.

## 탐색 원칙(Exploration Rule, 탐색 원칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 탐색 게이트(exploration gate, 탐색 제한문)가 아니다.

둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 sample label(표본 라벨)이다.

효과(effect, 효과): 보고서(report, 보고서)는 무엇을 탐색했는지 정직하게 라벨링(labeling, 라벨링)하되, 티어(tier, 티어)를 아이디어 승인이나 거절로 쓰지 않는다.

## 현재 경계(Current Boundary, 현재 경계)

현재 상태는 아직 alpha-ready(알파 준비 완료), official alpha result(공식 알파 결과), live readiness(실거래 준비), operating promotion(운영 승격)이 아니다.

지금 닫힌 주장은 Stage 08(8단계)의 alpha entry protocol(알파 진입 규칙)이 정의됐고 Stage 09(9단계)로 인계됐다는 것이다.

## 남은 작업(Open Items, 남은 작업)

- Stage 09(9단계): registry/current truth/publish packet(등록부/현재 진실/게시 묶음) 정리
- artifact registry(산출물 등록부)와 run registry(실행 등록부) 정합성 확인
- changelog(변경기록)와 current truth docs(현재 진실 문서) 최종 동기화
- alpha entry packet(알파 진입 묶음) 작성
- Stage 09(9단계) 폐쇄 전에는 official alpha result(공식 알파 결과)를 만들지 않기

## 현재 진실이 아닌 것(Not Current Truth, 현재 진실 아님)

- 오래된 Stage 06 `Tier B(티어 B)` 점수판(scorecard, 점수판) 결론
- 오래된 Stage 07 이중 판정 팩(dual-verdict packet, 이중 판정 팩)
- `Tier A(티어 A)`만 탐색의 기준선(anchor, 기준선)이라는 주장
- `Tier B(티어 B)`가 model study(모델 연구) 전에 끝없는 pre-validation(사전검증)을 받아야 한다는 주장
- MT5 price-proxy weights(MT5 가격 대리 가중치)를 actual index weights(실제 지수 가중치)로 읽는 주장
- Stage 07(7단계) baseline training smoke(기준선 학습 스모크)를 alpha quality(알파 품질)나 live readiness(실거래 준비)로 읽는 주장
- Stage 08(8단계) protocol(규칙)을 alpha result(알파 결과)로 읽는 주장
