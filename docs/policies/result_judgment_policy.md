# Result Judgment Policy (결과 판정 정책)

This policy defines how Project Obsidian Prime v2 judges run (`실행`) results after measurement (`측정`) and management (`관리`) evidence exists.

## Core Rule

Judgment must be lane-aware (`레인별`) and evidence-bounded (`근거 범위 제한`). A run can be useful evidence without being eligible for promotion (`승격`).

## Result Classes

Allowed `result_class` (`결과 분류`) values:

- `positive` (`긍정`): supports the hypothesis within the declared lane and evidence boundary.
- `negative` (`부정`): weakens or closes the hypothesis but remains reusable evidence.
- `inconclusive` (`불충분`): ran but cannot answer the question because of sample, coverage, or measurement limits.
- `invalid` (`무효`): should not be interpreted because contract, data, parity, or execution assumptions failed.

Never treat `negative` and `invalid` as the same. A negative result teaches something; an invalid result first requires repair or exclusion.

## Lane-Aware Judgment

- `exploration` (`탐색`): judge idea value, search boundary, failure mode, salvage value, and reopen condition.
- `evidence` (`근거`): judge comparability, artifact identity, KPI completeness, and registry completeness.
- `promotion` (`승격`): judge whether operating replacement or confirmation gates are met.
- `runtime` (`런타임`): judge execution, parity, packaging, and environment behavior only.
- `extra` (`추가`): judge against the extra stage charter, not hidden promotion assumptions.

`promotion-ineligible` (`승격 부적격`) does not mean `idea-dead` (`아이디어 사망`). An idea is `idea-dead` only when negative memory records why it failed, what was salvaged, and when it can be reopened.

## Guardrail And Disqualifier Handling

Each reviewed run should state:

- `primary_kpi` (`주요 핵심 성과 지표`) outcome
- `guardrail_status` (`보호 지표 상태`): `pass`, `warn`, `fail`, or `n/a`
- `disqualifier` (`실격 조건`) if any
- `parity_level` (`동등성 레벨`)
- `wfo_status` (`워크포워드 상태`)

A guardrail failure may produce `negative` or `inconclusive` depending on whether the failure answers the question. A contract, data, or parity failure that makes the result uninterpretable must be `invalid`.

## Closure Requirements

Before a run result is called closed (`닫힘`):

- measurement exists in `kpi_record.json` or every unavailable field has an `n/a` reason
- identity exists in `run_manifest.json` or equivalent registered artifacts
- registry row exists in `docs/registers/run_registry.csv`
- judgment is one of the allowed result classes
- negative exploration closure records salvage value and reopen condition

Do not promote from `structural_scout` (`구조 탐색 점수판`) alone. Do not claim `P4_full_runtime_parity_closed` (`전체 런타임 동등성 폐쇄`) from `P2_model_input_parity_closed` (`모델 입력 동등성 폐쇄`) evidence.
