# Current Working State

- updated_on: `2026-04-25`
- project_mode: `clean_stage_restart`
- active_stage: `06_runtime_parity__python_mt5_runtime_authority`
- active_branch: `main`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 깨끗한 단계 구조(clean stage structure, 깨끗한 단계 구조)로 다시 시작한 뒤, shared feature frame freeze(공유 피처 프레임 동결 산출물), training label/split(학습 라벨/분할), Stage 04(4단계) model input(모델 입력), Stage 05(5단계) feature integrity audit(피처 무결성 감사)까지 닫았다.

이전 `Stage 00`부터 `Stage 07`까지의 흐름(flow, 흐름)은 현재 진실(current truth, 현재 진실)이 아니다. 저장소 바깥 압축 스냅샷(zip snapshot, 압축 스냅샷)으로 남겨 둔 과거 이력(prior history, 과거 이력)일 뿐이다.

보존한 것(preserved assets, 보존 자산):

- 에이전트 스킬(agent skills, 에이전트 스킬)
- 계약 문서(contract documents, 계약 문서)
- 개념 노트(concept notes, 개념 노트)
- 데이터 루트(data roots, 데이터 루트)
- 재사용 foundation 도구(reusable foundation tools, 재사용 기반 도구)

## 탐색 원칙(Exploration Rule, 탐색 원칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 탐색 게이트(exploration gate, 탐색 제한문)가 아니다.

둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 어떤 표본(sample, 표본)을 공부했는지 알려주는 라벨(label, 라벨)이다.

## 닫힌 기반 단계(Closed Foundation Stages, 닫힌 기반 단계)

`02_feature_frame__practical_full_cash_freeze`

Stage 02(2단계)는 Stage 01(1단계)에서 고른 목표를 실제 shared freeze(공유 동결 산출물)로 물질화했다.

- run_id(실행 ID): `20260424_practical_full_cash_freeze_materialization`
- dataset_id(데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- selected rows(선택 행 수): `54439`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

효과(effect, 효과): 학습 데이터셋(training dataset, 학습 데이터셋)을 실제 동결 산출물(frozen artifact, 동결 산출물) 기준으로 말할 수 있다.

`03_training_dataset__label_split_contract`

Stage 03(3단계)는 첫 training label(학습 라벨)과 split contract(분할 계약)를 재현 가능하게 물질화했다.

- run_id(실행 ID): `20260425_label_v1_fwd12_split_v1_materialization`
- training_dataset_id(학습 데이터셋 ID): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- rows(행 수): `46650`
- train/validation/OOS(학습/검증/표본외): `29222/9844/7584`
- artifact path(산출물 경로): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet`

효과(effect, 효과): 첫 model training(모델 학습) 또는 alpha exploration(알파 탐색)에 필요한 기본 정답지와 분할은 있다.

## 최근 닫힌 Stage 04(최근 닫힌 4단계)

`04_model_input_readiness__weights_parity_feature_audit`

Stage 04(4단계)는 실제 지수 가중치(actual index weight, 실제 지수 가중치)를 주장하지 않고, 로컬 MT5 raw bars(원천 봉 데이터)에서 만든 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)로 58 feature(58개 피처) model input(모델 입력)을 재물질화했다.

가중치 실행(weight run, 가중치 실행):

- run_id(실행 ID): `20260425_top3_price_proxy_weights_v1`
- weight_table_id(가중치 표 ID): `top3_monthly_price_proxy_weights_fpmarkets_v2_v1`
- method(방법): `mt5_price_proxy_close_share_v1`
- symbols(심볼): `MSFT`, `NVDA`, `AAPL`
- month coverage(월별 범위): `2022-08`~`2026-04`
- bootstrap month(초기 월): `2022-08`
- weights path(가중치 경로): `foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv`
- weights sha256(가중치 해시): `08531dbf5235a166e5b2e9dc675ec3d41a0cc84066d00592c37f500aa8f89981`

58 feature(58개 피처) 입력 실행(model input run, 모델 입력 실행):

- run_id(실행 ID): `20260425_model_input_feature_set_v2_mt5_price_proxy_58`
- model_input_dataset_id(모델 입력 데이터셋 ID): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- feature_set_id(피처 세트 ID): `feature_set_v2_mt5_price_proxy_top3_weights_58_features`
- rows(행 수): `46650`
- included features(포함 피처): `58`
- restored features(복구 피처): `top3_weighted_return_1`, `us100_minus_top3_weighted_return_1`
- included feature order hash(포함 피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- artifact path(산출물 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`

56 feature(56개 피처) artifact(산출물)는 계속 interim quarantine artifact(임시 격리 산출물)로 보존한다.

효과(effect, 효과): `placeholder_equal_weight(임시 동일가중)` 없이 58개 피처 입력이 생겼고, 동시에 이 가중치가 실제 NDX/QQQ 가중치(actual NDX/QQQ weights, 실제 NDX/QQQ 가중치)가 아니라는 경계도 문서에 남았다.

## 최근 닫힌 Stage 05(최근 닫힌 5단계)

`05_feature_integrity__formula_time_alignment_leakage_audit`

Stage 05(5단계)는 Stage 04(4단계)에서 선택한 58 feature(58개 피처) model input(모델 입력)을 수식(formula, 수식), 시간 정렬(time alignment, 시간 정렬), 외부 정렬(external alignment, 외부 정렬), 라벨 누수(label leakage, 라벨 누수) 관점에서 감사했다.

- run_id(실행 ID): `20260425_stage05_feature_integrity_audit_v1`
- judgment(판정): `positive_feature_integrity_audit_passed`
- feature frame rows(피처 프레임 행): `54439`
- model input rows(모델 입력 행): `46650`
- external alignment missing total(외부 정렬 누락 합계): `0`
- audit summary(감사 요약): `stages/05_feature_integrity__formula_time_alignment_leakage_audit/02_runs/20260425_stage05_feature_integrity_audit_v1/audit_summary.json`

효과(effect, 효과): 첫 학습 전에 “피처가 계산되고 정렬된 방식”은 감사 근거(audit evidence, 감사 근거)를 갖게 됐다. 이 단계는 모델 성능(model quality, 모델 품질)을 아직 주장하지 않는다.

## 현재 단계(Current Stage, 현재 단계)

`06_runtime_parity__python_mt5_runtime_authority`

Stage 06(6단계)의 질문(question, 질문)은 Python/MT5 parity(파이썬/MT5 동등성)와 full MT5 runtime authority(완전 MT5 런타임 권위)를 alpha exploration(알파 탐색) 전 기준으로 닫을 수 있는가다.

Stage 06(6단계)의 입력(input, 입력)은 Stage 05(5단계)가 감사한 58 feature(58개 피처) MT5 price-proxy model input(MT5 가격 대리 모델 입력)이다.

효과(effect, 효과): 이제 같은 피처 표면(feature surface, 피처 표면)을 Python snapshot(파이썬 스냅샷)과 MT5 snapshot(MT5 스냅샷) 비교 대상으로 삼는다.

## Pre-Alpha Stage Queue(알파 전 단계 대기열)

model-backed alpha exploration(모델 근거 알파 탐색) 전에 남은 작업은 Stage 06~09(6~9단계)다.

- Stage 06(6단계): Python/MT5 parity(파이썬/MT5 동등성)와 full MT5 runtime authority(완전 MT5 런타임 권위)
- Stage 07(7단계): preprocessing policy(전처리 정책), model training run contract(모델 학습 실행 계약), baseline smoke training(기준선 스모크 학습)
- Stage 08(8단계): alpha search protocol(알파 탐색 규칙)과 Tier A/B reporting(티어 A/B 보고)
- Stage 09(9단계): registry/current truth/publish handoff(등록부/현재 진실/게시 인계)

효과(effect, 효과): 다음 작업 때 해야 할 일이 한 단계 안에서 섞이지 않는다.

## 현재 경계(Current Boundary, 현재 경계)

이 상태는 아직 model training(모델 학습) 완료도 아니고 runtime authority(런타임 권위)도 아니다.

지금 닫힌 주장은 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치), 58 feature(58개 피처) model input(모델 입력), 그리고 Stage 05(5단계) feature integrity audit(피처 무결성 감사)이 통과했다는 evidence claim(근거 주장)뿐이다.

이 가중치는 NDX 실제 구성비(actual NDX index weights, 실제 NDX 지수 가중치), QQQ 보유비중(QQQ holdings weights, QQQ 보유비중), 시가총액(market cap, 시가총액), 유동주식수(float, 유동주식수)를 반영하지 않는다.

## 현재 진실이 아닌 것(Not Current Truth, 현재 진실 아님)

- 오래된 Stage 06 `Tier B(티어 B)` 점수판(scorecard, 점수판) 결론
- 오래된 Stage 07 이중 판정 팩(dual-verdict packet, 이중 판정 팩)
- `Tier A(티어 A)`만 탐색의 기준선(anchor, 기준선)이라는 주장
- `Tier B(티어 B)`가 모델 연구(model study, 모델 연구) 전에 끝없는 사전검증(pre-validation, 사전검증)을 받아야 한다는 주장
- MT5 price-proxy weights(MT5 가격 대리 가중치)를 actual index weights(실제 지수 가중치)로 읽는 주장
