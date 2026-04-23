# Architecture Invariants

코드 소유권(code ownership, 코드 소유권)을 단순하게 유지한다.

## 소유권(Ownership, 소유권)

- `foundation/features`: 재사용 피처 로직(reusable feature logic, 재사용 피처 로직)
- `foundation/pipelines`: 조율(orchestration, 조율)과 물질화(materialization, 물질화)
- `foundation/mt5`: MT5 실행(execution, 실행) 또는 검증(verification, 검증) 도구
- `foundation/parity`: Python과 MT5 비교(comparison, 비교) 도구
- `stages/*`: 단계 로컬 산출물(stage-local artifacts, 단계 로컬 산출물), 보고서(reports, 보고서), 결정(decisions, 결정)

`foundation/pipelines`가 피처 정의(feature definition, 피처 정의)나 모델 로직(model logic, 모델 로직)의 숨은 진실 원천(source of truth, 진실 원천)이 되면 안 된다.

## 모델 산출물(Model Artifacts, 모델 산출물)

모델(model, 모델)은 재현 가능한 산출물(reproducible artifact, 재현 가능한 산출물)이나 동결된 파라미터/규격 묶음(frozen parameter/spec bundle, 동결 파라미터/규격 묶음)이 있을 때만 물질화(materialized, 물질화)되었다고 말한다.

확률표(probability table, 확률표)와 보고서(report, 보고서)는 근거(evidence, 근거)이지 모델 산출물(model artifact, 모델 산출물) 자체는 아니다.

## 경로 규칙(Path Rules, 경로 규칙)

문서(docs, 문서), 매니페스트(manifest, 목록), 등록부(register, 등록부), 테스트(test, 테스트) 안에서는 저장소 상대경로(repo-relative path, 저장소 상대경로)를 쓴다.

절대경로(absolute path, 절대경로)는 로컬 진단(local diagnostic, 로컬 진단), 사용자용 클릭 링크(clickable link, 클릭 링크), 외부 도구(external tool, 외부 도구), MT5 인계(MT5 handoff, MT5 인계)에만 쓴다.

## 인코딩(Encoding, 인코딩)

한국어 `.md`와 `.txt` 문서는 UTF-8 with BOM(UTF-8 BOM 포함)을 쓴다.
