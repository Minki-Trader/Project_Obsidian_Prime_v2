# Stage 03 MT5 Runtime Snapshot Handoff

## Purpose

- export the first `MT5 feature snapshot audit`(MT5 피처 스냅샷 감사) artifact for `runtime_fpmarkets_v2_mt5_snapshot_0001`
- keep the handoff grounded in the already bound five-window Stage 03 minimum parity pack
- prepare the exact inputs needed for the first evaluated `runtime parity`(런타임 패리티) comparison

## Required Existing Inputs

- `../02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json`
- `../02_runs/runtime_parity_pack_0001/mt5_snapshot_audit_inputs.set`
- `../02_runs/runtime_parity_pack_0001/mt5_tester_runtime_parity_pack_0001.ini`
- `../02_runs/runtime_parity_pack_0001/mt5_target_windows_utc.txt`
- `../02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json`
- `../../../foundation/parity/compare_fpmarkets_v2_runtime_parity.py`
- `../../../foundation/parity/run_fpmarkets_v2_runtime_parity_native.py`

## MT5 Snapshot Audit Inputs

- `Expert = Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeParityAuditEA.ex5`
- `InpOutputPath = Project_Obsidian_Prime_v2/runtime_parity/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl`
- `InpOutputUseCommonFiles = true`
- `InpTargetWindowsUtc = 2022.09.02 17:00:00;2022.09.01 20:00:00;2022.11.09 21:00:00;2022.09.01 19:55:00;2022.09.01 13:35:00`
- `InpMainSymbol = US100`
- `InpTimeframe = 5`
- `InpMainWarmupBars = 300`
- `InpExternalWarmupBars = 25`

## Expected MT5 Output

- one JSONL line per bound fixture window under `MetaQuotes/Terminal/Common/Files/Project_Obsidian_Prime_v2/runtime_parity/runtime_parity_pack_0001/`
- four `ready`(준비 완료) rows for the regular, session-boundary, DST-sensitive, and external-alignment samples
- one `non-ready`(비준비) row for the negative fixture where required external inputs are missing

## Loadable Input Set

- load `../02_runs/runtime_parity_pack_0001/mt5_snapshot_audit_inputs.set` on the MT5 `Inputs` tab so the v2-native audit path, window spec, and warmup settings are copied without retyping

## Native Tester Command

```powershell
python foundation/parity/run_fpmarkets_v2_runtime_parity_native.py `
  --mt5-request stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json
```

## Exclusive Launch Note

- `terminal64.exe /config:...` can be ignored when another MT5 GUI instance is already running
- the native runner above stops early in that situation unless `--force-close-terminal` is passed explicitly
- use `--force-close-terminal` only when it is safe to close the current MT5 GUI instance

## Import Command

```powershell
python foundation/parity/import_fpmarkets_v2_mt5_snapshot_audit.py `
  --mt5-request stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json
```

## One-Shot Command

```powershell
python foundation/parity/run_fpmarkets_v2_runtime_parity_after_mt5.py `
  --mt5-request stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json
```

## Comparison Command

```powershell
python foundation/parity/compare_fpmarkets_v2_runtime_parity.py `
  --python-snapshot stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json `
  --mt5-request stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json `
  --mt5-snapshot stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl `
  --output-json stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json
```

## Report Rendering Command

```powershell
python foundation/parity/render_fpmarkets_v2_runtime_parity_report.py `
  --comparison-json stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json `
  --python-snapshot stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json `
  --mt5-request stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json `
  --mt5-snapshot stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl `
  --report-path stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md
```

## Interpretation Guardrail

- do not claim `model-input parity closure`(모델 입력 패리티 폐쇄) from this handoff note alone
- the comparison output must exist and the Stage 03 report must be updated before any closure claim
- if the MT5 JSONL artifact lacks an explicit `timestamp_utc`(UTC 시각) field, the comparator first infers UTC from `external_inputs[].requested_close_utc`; if that identity is absent too, it falls back to `bar_time_server` text matching and should be treated as `handoff verification`(전달 검증) rather than full closure evidence
- the compare and render defaults still expect the imported repo-local JSONL path under `../02_runs/runtime_parity_pack_0001/`, not the raw Common Files path
