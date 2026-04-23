# Run Result Management (실행 결과 관리)

This policy defines how Project Obsidian Prime v2 manages run (`실행`) results. KPI (`key performance indicator`, 핵심 성과 지표) measurement and result judgment live in separate policies.

## Core Rule

Every run must have managed identity (`관리되는 정체성`) before it is treated as reviewed (`검토됨`), selected (`선택됨`), archived (`보관됨`), invalidated (`무효화됨`), or superseded (`대체됨`).

Progressive hardening (`점진적 경화`) applies: `planned`, `running`, and `completed` runs may carry partial records; `reviewed` and `selected` runs need measurement, management, and judgment; `operating_promotion` and `runtime_authority` claims need strict evidence.

Stage-local folders store source artifacts. Git-tracked registers store the map.

## Run Folder Contract

Default run path:

```text
stages/<stage_id>/02_runs/<status>/<run_id>/
```

Recommended files:

- `run_manifest.json` (`실행 명세`): identity, lineage, inputs, code/artifact references, and expected effect.
- `config.json` (`설정`): executable parameters when applicable.
- `kpi_record.json` (`핵심 성과 지표 기록`): machine-readable KPI layers.
- `result_summary.md` (`결과 요약`): human-readable readout and judgment.
- `artifacts/` (`산출물`): model, bundle, schema, or intermediate files.
- `reports/` (`보고서`): detailed review outputs.
- `logs/` (`로그`): execution logs.
- `mt5_attempts/` (`MT5 시도`): tester attempts when MT5 is involved.

If an existing stage already uses a compatible local structure, do not move old artifacts only to satisfy this layout. Apply this contract to new or touched runs.

## Run Status Lifecycle

Allowed `status` (`상태`) values:

- `planned` (`계획됨`)
- `running` (`실행 중`)
- `completed` (`완료됨`)
- `reviewed` (`검토됨`)
- `selected` (`선택됨`)
- `archived` (`보관됨`)
- `failed_execution` (`실행 실패`)
- `invalidated` (`무효화됨`)
- `superseded` (`대체됨`)

Do not use `reviewed` unless `kpi_record.json`, `result_summary.md`, and `docs/registers/run_registry.csv` can point to the run's evidence or explicitly state why a field is `n/a`. Do not force an early scout run into `invalidated` only because its record is partial; label it `completed`, `scout-only`, or `inconclusive` as appropriate.

## Run Registry

`docs/registers/run_registry.csv` is the durable run map (`실행 지도`). It stores summary identity only; detailed KPI values stay in each run's `kpi_record.json`.

Required columns:

```text
run_id,stage_id,idea_id,lane,tier_scope,scoreboard,evidence_boundary,status,result_class,primary_kpi,guardrail_status,parity_level,wfo_status,hard_gate_applicable,operating_truth_claim,artifact_hash,kpi_record_path,summary_path,created_at,reviewed_at
```

Use `n/a` (`해당 없음`) when a column does not apply. Use `pending` (`대기`) only for planned rows that have not produced evidence yet.

## Lineage And Identity

Every reviewed run should record:

- `parent_run_id` (`부모 실행 식별자`) or `n/a`
- `idea_id` (`아이디어 식별자`)
- `variant_of` (`변형 원본`)
- `changed_surface` (`변경 표면`)
- `change_reason` (`변경 이유`)
- `expected_effect` (`기대 효과`)
- `actual_effect` (`실제 효과`) once reviewed

This prevents isolated winner-only notes and keeps negative results reusable.

## Git Boundary

Track small identity artifacts in Git: manifests, KPI records, summaries, configs, hashes, and registry rows. Large local artifacts may stay outside Git, but their role, path, and hash must be represented by Git-tracked evidence before they are described as reusable.
