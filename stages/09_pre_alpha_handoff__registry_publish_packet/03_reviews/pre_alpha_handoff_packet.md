# Stage 09 Pre-Alpha Handoff Packet

- packet_id(묶음 ID): `stage09_pre_alpha_handoff_packet_v1`
- stage(단계): `09_pre_alpha_handoff__registry_publish_packet`
- status(상태): `reviewed_closed_handoff_to_stage10_complete_with_pre_alpha_handoff_packet`
- judgment(판정): `positive_pre_alpha_handoff_packet_complete`
- external_verification_status(외부 검증 상태): `not_applicable(해당 없음)`

## 쉬운 판독(Plain Read, 쉬운 판독)

Stage 09(9단계)는 pre-alpha foundation(알파 전 기반)의 registry/current truth/publish boundary(등록부/현재 진실/게시 경계)를 한 묶음(packet, 묶음)으로 닫는다.

효과(effect, 효과): 다음 활성 단계(active stage, 활성 단계)인 `10_alpha_scout__default_split_model_threshold_scan`은 첫 alpha scout(알파 탐색 판독)를 준비할 수 있다.

## 닫힌 근거(Closed Evidence, 닫힌 근거)

- Stage 04(4단계) selected model input(선택 모델 입력): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- feature count(피처 수): `58`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- default label(기본 라벨): `label_v1_fwd12_m5_logret_train_q33_3class`
- default split(기본 분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`
- Stage 05(5단계) feature integrity audit(피처 무결성 감사): `20260425_stage05_feature_integrity_audit_v1`
- Stage 06(6단계) runtime parity(런타임 동등성): `20260425_stage06_runtime_parity_closed_v1`
- Stage 07(7단계) baseline training smoke(기준선 학습 스모크): `20260425_stage07_baseline_training_smoke_v1`
- Stage 08(8단계) alpha entry protocol(알파 진입 규칙): `stage08_alpha_entry_protocol_v1`

## 등록부 동기화(Registry Sync, 등록부 동기화)

`docs/registers/artifact_registry.csv`는 Stage 09(9단계) handoff packet(인계 묶음)을 등록한다.

`docs/registers/run_registry.csv`에는 Stage 09(9단계) 행을 추가하지 않는다. 이유(reason, 이유)는 Stage 09(9단계)가 run-producing stage(실행 생성 단계)가 아니라 document handoff stage(문서 인계 단계)이기 때문이다.

효과(effect, 효과): reviewed run(검토된 실행)이라는 말은 measurement(측정), identity(정체성), judgment(판정)을 가진 실행에만 남는다.

## 게시 경계(Publish Boundary, 게시 경계)

- branch(브랜치): `codex/stage09-pre-alpha-handoff`
- commit boundary(커밋 경계): `Close Stage 09 pre-alpha handoff`
- PR(`pull request`, 풀 리퀘스트): 이번 묶음에서는 만들지 않는다.

효과(effect, 효과): Stage 09(9단계) 닫힘은 커밋 단위로 남지만, 원격 게시(remote publish, 원격 게시)나 PR(풀 리퀘스트)은 별도 요청이 있을 때 한다.

## 다음 단계(Next Stage, 다음 단계)

다음 활성 단계(active stage, 활성 단계)는 `10_alpha_scout__default_split_model_threshold_scan`이다.

Stage 10(10단계)의 lane(레인)은 `exploration(탐색)`이고, 첫 경계(boundary, 경계)는 `single_split_scout(단일 분할 탐색 판독)`다.

효과(effect, 효과): 첫 공식 알파 작업은 기본 split(기본 분할) 위에서 model/threshold candidate(모델/임계값 후보)를 빠르게 판독할 수 있다. 하지만 Stage 10(10단계)이 열린 것만으로 alpha result(알파 결과)가 생기지는 않는다.

## 경계(Boundary, 경계)

이 묶음(packet, 묶음)은 alpha-ready(알파 준비 완료), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 만들지 않는다.

Stage 06(6단계)의 runtime authority(런타임 권위)는 minimum fixture set(최소 표본 묶음)에만 닫힌다. Stage 07(7단계)의 baseline smoke(기준선 스모크)는 Python-side training pipeline evidence(파이썬 측 학습 처리 흐름 근거)이지 alpha quality(알파 품질)가 아니다.

MT5 price-proxy weights(MT5 가격 대리 가중치)는 actual NDX/QQQ weights(실제 NDX/QQQ 가중치)가 아니다.

## 구조 가드(Architecture Guard, 구조 가드)

- architecture_risk(구조 위험): stage transition(단계 전환), artifact registry(산출물 등록부), alpha-search framing(알파 탐색 틀짓기)을 바꾼다.
- debt_interaction(부채 상호작용): `AD-003`, `AD-004`, `AD-005`, `AD-006`를 건드리지만 새 debt(부채)를 정상 패턴으로 승격하지 않는다.
- allowed_debt_change(허용 부채 변경): `leave_unchanged(변경 없음)`
- encoding_check(인코딩 검사): Korean `.md` 문서는 UTF-8 with BOM(UTF-8 BOM 포함)을 유지한다.
- path_safety_check(경로 안전 검사): durable identity(지속 정체성)는 repo-relative path(저장소 상대경로)를 쓴다. Windows long path(윈도우 긴 경로)는 검증 때 `rg --files --no-ignore` 같은 열거 기반 확인을 우선한다.
- code_surface_check(코드 표면 검사): 코드 변경 없음. owner module(소유 모듈), caller(호출자), input/output contract(입출력 계약)는 새로 생기지 않는다.
