# Architecture Invariants (구조 불변 규칙)

This policy defines stage-agnostic architecture rules (단계 독립 구조 규칙) for `Project_Obsidian_Prime_v2`.

Use this file when work touches feature calculation (피처 계산), model training or export (모델 학습 또는 내보내기), pipeline materialization (파이프라인 물질화), artifact claims (산출물 주장), stage transition (단계 전환), alpha search (알파 탐색), or Korean encoding (한국어 인코딩).

## Ownership Rules (소유권 규칙)

- `foundation/features` owns reusable feature logic (재사용 피처 로직).
- `foundation/pipelines` orchestrates reusable logic (재사용 로직 조율) and must not become the source of truth (진실 원천) for feature definitions, feature order, or reusable feature computation.
- Stage-local scripts (단계 로컬 스크립트) may materialize experiment outputs, but they must not quietly become the long-term owner of reusable feature, model, or runtime contracts.
- `foundation/mt5` may implement MT5 runtime or parity logic (MT5 런타임 또는 동등성 로직), but duplicated calculation surfaces must name their Python owner and parity evidence (파이썬 소유자 및 동등성 근거).

## Code Surface Rules (코드 표면 규칙)

- Reusable feature/model/runtime logic (재사용 피처/모델/런타임 로직) belongs under the correct `foundation` owner module.
- `foundation/pipelines` owns orchestration (조율), stage scripts own materialization and stage-local analysis (물질화 및 단계 로컬 분석), and MT5 EA code owns execution and verification (실행 및 검증).
- New code must name where it is used: caller (호출자), input contract (입력 계약), output contract (출력 계약), and artifact/report effect (산출물/보고 효과).
- Do not concentrate broad feature, model, runtime, and reporting logic in one EA or one pipeline file when smaller owner modules can carry the reusable logic.
- A task packet (작업 패킷) that cannot explain code placement and effect must stop before implementation.

## Model Artifact Rules (모델 산출물 규칙)

- A model is not `materialized` (물질화됨) unless a reproducible model artifact (재현 가능한 모델 산출물) or frozen parameter/spec bundle (동결 파라미터/규격 번들) exists under a tracked stage run path or a registered artifact path.
- Probability tables, evaluation summaries, calibration reads, and reports are materialized evidence (물질화 근거), but they are not by themselves a materialized model artifact.
- If a pipeline can rebuild a model only from current code, describe the result as a code-rebuildable read (코드 재실행 가능 판독), not as a frozen model (동결 모델).
- Any future model handoff must record feature surface (피처 표면), label rule (라벨 규칙), imputation policy (대치 정책), output order (출력 순서), and artifact identity (산출물 정체성).

## Alpha Search Integrity (알파 탐색 무결성)

- Alpha search (알파 탐색) may include source cleanup (소스 정리) or validation debt closure (검증 부채 정리), but it must not be reduced to those tasks alone without an explicit decision.
- A source-boundary packet (소스 경계 팩) must not prune or promote an alpha lane (알파 레인) when the active feature surface (활성 피처 표면) is unaffected by that source.
- Placeholder inputs (임시 입력) may be used only within their stated boundary and must not later become a promotion gate (승격 게이트) without a durable decision explaining why.

## Path Rules (경로 규칙)

- Repo-internal references (저장소 내부 참조) must use repo-relative paths (저장소 상대경로) by default in documents, manifests, registries, tests, and stage artifacts.
- Absolute paths (절대경로) are allowed only for local diagnostics (로컬 진단), user-facing clickable file links (사용자용 클릭 파일 링크), external tool invocation (외부 도구 호출), or MT5 environment handoff (MT5 환경 인계) when a machine path is required.
- Durable artifact identity (지속 산출물 정체성) must not depend on an absolute terminal install path (터미널 설치 절대경로); use repo-relative path plus hash, run id, bundle id, or registry fields instead.
- Stage and run directories (단계 및 실행 디렉터리) already carry context, so filenames should avoid repeating long dataset, stage, run, or project identifiers unless a contract or registry schema explicitly requires them.
- If one tool can enumerate a file but another reports `Cannot find path` or `False`, treat Windows long path handling (윈도우 긴 경로 처리) as a first suspect before declaring the artifact missing.
- Archive snapshots (아카이브 스냅샷) of deep stage trees should prefer ZIP plus manifest (ZIP 및 목록) over nested folder copies, because ZIP preserves internal relative paths while avoiding destination path expansion.
- `\\?\` long-path prefixes (긴 경로 접두사) may be used in local scripts or one-off tooling, but committed docs and registry fields should stay repo-relative.

## Debt Handling (부채 처리)

- Known architecture debt (알려진 구조 부채) belongs in `docs/registers/architecture_debt_register.md`.
- Registering debt does not normalize it. It marks the debt as known, bounded, and not safe to copy as a project pattern.
- New work may leave existing debt unchanged only when the task is unrelated or when the task explicitly records why cleanup is out of scope.
- New work must not deepen existing debt without a decision memo (결정 메모) or task packet (작업 패킷) that names the tradeoff.

## Encoding Rules (인코딩 규칙)

- Korean `.md` and `.txt` documents (한국어 문서)는 UTF-8 with BOM (UTF-8 BOM 포함)을 사용한다.
- If mojibake (문자 깨짐), replacement characters (대체 문자), or suspicious CJK compatibility text (의심스러운 CJK 호환 문자)가 발견되면, 의미 있는 문서 변경 전에 원인을 분리한다.
- Use `Get-Content -Encoding UTF8` or an equivalent explicit UTF-8 read (명시적 UTF-8 읽기) when inspecting Korean docs on Windows.
- Run the architecture guard validator (구조 가드 검증기) when agent settings, repo-scoped skills, or Korean docs are edited.
