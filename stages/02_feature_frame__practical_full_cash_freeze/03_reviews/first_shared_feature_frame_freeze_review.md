# First Shared Feature Frame Freeze Review

## 판독(Read, 판독)

`20260424_practical_full_cash_freeze_materialization` 실행(run, 실행)은 Stage 02(2단계) 질문에 `yes(예)`로 답한다.

선택된 target(목표)인 `practical_start_full_cash_day_valid_rows_only`는 실제 shared feature frame freeze(공유 피처 프레임 동결 산출물)로 물질화되었다.

## 핵심 수치(Key Numbers, 핵심 수치)

- dataset_id(데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- raw rows(원시 행 수): `255001`
- valid rows(유효행 수): `55408`
- selected rows(선택 행 수): `54439`
- eligible full cash days(사용한 완전 정규장 일수): `890`
- excluded partial cash days(제외된 부분 정규장 일수): `40`
- excluded partial-day valid rows(제외된 부분 정규장 유효행 수): `252`
- feature count(피처 수): `58`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

## 산출물 정체성(Artifact Identity, 산출물 정체성)

- dataset summary(데이터셋 요약): `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01/dataset_summary.json`
- features parquet(피처 파케이): `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01/features.parquet`
- summary SHA256(요약 SHA256): `cfbe306248a029537c4030c742dcf3ffcacc7d58997b81552502f3b76be87dc1`
- features SHA256(피처 SHA256): `0b3feec1f01f0436c908abb7b5b02d740b259c70a1639438de2b2f172a1121d0`

## 코드 배치 판독(Code Placement Read, 코드 배치 판독)

- owner_module(소유 모듈): `foundation/pipelines/materialize_feature_frame_freeze.py`
- caller(호출자): Stage 02 evidence run(근거 실행)
- input_contract(입력 계약): Stage 01 target selection(목표 선택) + dataset freeze contract(데이터셋 동결 계약)
- output_contract(출력 계약): shared feature frame freeze summary(공유 피처 프레임 동결 요약), row validity report(행 유효성 보고서), parser manifest(파서 목록), local dataset files(로컬 데이터셋 파일)
- artifact_or_report_relation(산출물/보고서 관계): 무거운 데이터 파일(heavy data files, 무거운 데이터 파일)은 로컬에 두고, 정체성(identity, 정체성)와 해시(hash, 해시)는 Git 추적 문서에 남긴다.
- monolith_risk(단일파일 위험): 낮음. 재사용 로직(reusable logic, 재사용 로직)은 기존 materializer(물질화기)를 재사용하고, 새 파일은 Stage 02 질문에 맞는 조율(orchestration, 조율)만 맡는다.

## 외부 검증 상태(External Verification Status, 외부 검증 상태)

`not_applicable(해당 없음)`

이 실행(run, 실행)은 pure Python dataset freeze claim(순수 파이썬 데이터셋 동결 주장)만 다룬다. MT5 execution(실행), tester orchestration(테스터 조율), runtime parity(런타임 동등성)를 주장하지 않으므로 이 단계에서는 외부 검증(external verification, 외부 검증)이 필요하지 않다.

## 효과(Effect, 효과)

Stage 02(2단계)는 닫을 수 있다.

남은 일(remaining work, 남은 작업)은 첫 training label(학습 라벨)과 split contract(분할 계약)를 정하는 것이다.
