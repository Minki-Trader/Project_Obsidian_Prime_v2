# Architecture Invariants

코드 소유권(code ownership, 코드 소유권)을 단순하게 유지한다.

## 소유권(Ownership, 소유권)

- `foundation/features`: 재사용 피처 로직(reusable feature logic, 재사용 피처 로직)
- `foundation/pipelines`: 공통 데이터 물질화(materialization, 물질화)와 legacy 호환 shim(호환 진입점)
- `stage_pipelines/stageXX`: 해당 Stage에만 고유한 실행 어댑터(stage-specific execution adapter, 단계 전용 실행 어댑터)
- `foundation/mt5`: MT5 실행(execution, 실행) 또는 검증(verification, 검증) 도구
- `foundation/parity`: Python과 MT5 비교(comparison, 비교) 도구
- `stages/*`: 단계 로컬 산출물(stage-local artifacts, 단계 로컬 산출물), 보고서(reports, 보고서), 결정(decisions, 결정)

`foundation/pipelines`와 `stage_pipelines`가 피처 정의(feature definition, 피처 정의)나 모델 로직(model logic, 모델 로직)의 숨은 진실 원천(source of truth, 진실 원천)이 되면 안 된다. `stage_pipelines/stageXX`는 각 stage의 실행 지휘실(execution room, 실행 지휘실)이지 공통 도구 창고(shared toolbox, 공통 도구 창고)가 아니다. 다른 stage에서 재사용할 로직은 `foundation/*` owner module(소유 모듈)로 끌어올린 뒤 사용한다.

## EA 모듈 경계(EA Module Boundary, EA 모듈 경계)

MT5 EA(`Expert Advisor`, 전문가 자문)는 얇은 진입점(thin entrypoint, 얇은 진입점)과 재사용 모듈(reusable module, 재사용 모듈)로 나눈다.

- `.mq5` 진입점(entrypoint, 진입점)은 `OnInit`, `OnTick`, `OnDeinit`, 입력값(input, 입력값), 파일 경로(file path, 파일 경로) 연결만 담당한다.
- 재사용 MQL5 모듈(reusable MQL5 module, 재사용 MQL5 모듈)은 `foundation/mt5/include/ObsidianPrime/` 아래에 둔다.
- 피처 입력(feature input, 피처 입력), 모델 런타임(model runtime, 모델 런타임), 의사결정 표면(decision surface, 의사결정 표면), 주문 연결(execution bridge, 실행 연결), 런타임 기록(runtime telemetry, 런타임 기록)은 서로 다른 모듈 경계(module boundary, 모듈 경계)를 가진다.
- 단계 로컬 EA(stage-local EA, 단계 로컬 EA)는 실험(probe, 탐침)에만 쓰고, 두 번 이상 재사용할 로직(logic, 로직)은 모듈로 끌어올린다.
- run별 차이(run-specific difference, 실행별 차이)가 파라미터(parameter, 파라미터)뿐이면 `.mq5`를 복제하지 않고 `.set` file(설정 파일), `run_manifest.json(실행 목록)`, KPI record(KPI 기록)에 남긴다.
- run별 차이(run-specific difference, 실행별 차이)가 decision surface(의사결정 표면), execution bridge(실행 연결), telemetry(기록), feature input(피처 입력)을 바꾸면 해당 `.mqh` 모듈(module, 모듈)의 버전(version, 버전)과 sha256 hash(해시)를 남긴다.
- `#property(프로그램 속성)`처럼 main `.mq5`에 있어야 하는 항목은 entrypoint(진입점)에 둔다. include file(포함 파일)에 숨기지 않는다.

효과(effect, 효과): EA 파일 하나가 계속 커지면서 입력 계약(input contract, 입력 계약), 실행 계약(execution contract, 실행 계약), 기록 계약(telemetry contract, 기록 계약)을 섞는 일을 막는다.

## EA 실행 변형 트리거(EA Run Variant Trigger, EA 실행 변형 트리거)

EA(`Expert Advisor`, 전문가 자문), Strategy Tester(전략 테스터), `.set` 설정(set file, 설정 파일), optimization pass(최적화 회차), runtime package(런타임 패키지), model bundle(모델 번들)을 건드리는 작업은 시작 전에 run variant boundary(실행 변형 경계)를 정한다.

필수 판정(required decision, 필수 판정):

- entrypoint unchanged + parameter change(진입점 유지 + 파라미터 변경): `.set`과 manifest(목록)만 새로 만든다.
- module change(모듈 변경): `.mqh` 모듈 버전(module version, 모듈 버전)을 올리고 module hash(모듈 해시)를 남긴다.
- entrypoint change(진입점 변경): lifecycle(생명주기), tester property(테스터 속성), file handoff(파일 인계)가 바뀌는 이유를 기록한다.
- new EA file(새 EA 파일): 기존 runner(실행기)와 모듈(module, 모듈)로 표현할 수 없는 이유가 있을 때만 만든다.

효과(effect, 효과): run01A/run01B 같은 실행(run, 실행)이 조금씩 달라도 code identity(코드 정체성), input identity(입력 정체성), tester identity(테스터 정체성)가 끊기지 않는다.

## 모델 산출물(Model Artifacts, 모델 산출물)

모델(model, 모델)은 재현 가능한 산출물(reproducible artifact, 재현 가능한 산출물)이나 동결된 파라미터/규격 묶음(frozen parameter/spec bundle, 동결 파라미터/규격 묶음)이 있을 때만 물질화(materialized, 물질화)되었다고 말한다.

확률표(probability table, 확률표)와 보고서(report, 보고서)는 근거(evidence, 근거)이지 모델 산출물(model artifact, 모델 산출물) 자체는 아니다.

## 경로 규칙(Path Rules, 경로 규칙)

문서(docs, 문서), 매니페스트(manifest, 목록), 등록부(register, 등록부), 테스트(test, 테스트) 안에서는 저장소 상대경로(repo-relative path, 저장소 상대경로)를 쓴다.

절대경로(absolute path, 절대경로)는 로컬 진단(local diagnostic, 로컬 진단), 사용자용 클릭 링크(clickable link, 클릭 링크), 외부 도구(external tool, 외부 도구), MT5 인계(MT5 handoff, MT5 인계)에만 쓴다.

## 인코딩(Encoding, 인코딩)

한국어 `.md`와 `.txt` 문서는 UTF-8 with BOM(UTF-8 BOM 포함)을 쓴다.
