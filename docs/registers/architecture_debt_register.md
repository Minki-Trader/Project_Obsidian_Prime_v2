# Architecture Debt Register (구조 부채 등록부)

This register tracks known architecture debt (알려진 구조 부채) so future stages do not copy it as normal project style.

Registering a debt means: known, bounded, and not safe to repeat. It does not mean accepted as a healthy pattern.

| debt_id | scope (범위) | symptom (증상) | why_it_matters (중요한 이유) | allowed_until (허용 조건) | must_not_repeat (반복 금지 조건) |
|---|---|---|---|---|---|
| `AD-001` | reusable feature layer (재사용 피처 계층) | `foundation/features` has only `README.md`, while reusable Python feature logic currently lives in `foundation/pipelines/materialize_fpmarkets_v2_dataset.py`. | Future agents may mistake pipeline-local feature calculation (파이프라인 로컬 피처 계산) for the intended architecture. | Existing Stage 01 to Stage 07 evidence may remain readable as historical materialized evidence until a dedicated feature-layer migration is approved. | Do not add new reusable feature calculation to `foundation/pipelines` when it belongs in `foundation/features`. |
| `AD-002` | model artifact identity (모델 산출물 정체성) | Stage 06 reduced-context model reads produced probability tables and summaries, but no tracked `.joblib`, `.pkl`, `.onnx`, or frozen parameter/spec bundle. | Calling this a materialized model (물질화된 모델) can overstate reproducibility and handoff readiness. | Existing Stage 06/07 docs may keep their historical wording only when paired with claim discipline that distinguishes probability-output evidence from frozen model artifacts. | Do not describe a future model as materialized unless a reproducible artifact or frozen parameter/spec bundle exists. |
| `AD-003` | alpha search boundary (알파 탐색 경계) | Stage 07 opening narrowed toward a Tier B dual-verdict source-boundary packet even though the current keep42 surface is weight-neutral on direct inputs. | Alpha search (알파 탐색) can drift into validation debt closure (검증 부채 정리) while looking like search progress. | Treat this as an existing Stage 07 framing debt until a later Stage 07 realignment packet is approved. | Do not let future alpha stages become source cleanup only without an explicit decision and separate alpha-search question. |
| `AD-004` | Korean encoding (한국어 인코딩) | Some Korean `.md` files lacked UTF-8 BOM, and `obsidian-task-packet` contained mojibake in Korean trigger phrases. | Windows-facing workflows can display broken Korean text and agents may copy corrupted triggers. | Existing files must be normalized during the agent-settings hardening pass. | Do not edit Korean `.md` or `.txt` docs without preserving UTF-8 with BOM and checking for mojibake. |

## Use Rule (사용 규칙)

- Before feature/model/pipeline/stage/claim work, check whether the task touches any debt above.
- If it does, state whether the pass reduces the debt (부채 감소), leaves it unchanged (부채 유지), or would deepen it (부채 심화).
- Debt-deepening changes require an explicit decision memo or task packet.
