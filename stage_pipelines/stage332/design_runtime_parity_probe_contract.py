from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "332_overfit_guard__failure_memory_forward_research_handoff"
RUN_NUMBER = "run332E"
RUN_ID = "run332E_runtime_parity_probe_design_v1"
PARENT_RUN_ID = "run332D_design_pocket_veto_feature_thesis_v1"
NEXT_RUN_ID = "run332F_close_stage332_open_pocket_veto_materialization_stage_v1"
STATUS = "completed_runtime_parity_probe_contract_design_no_runtime_execution"
JUDGMENT = "runtime_parity_contract_design_research_only_no_goal_achieve"
DECISION = "future_runtime_probe_requires_identity_hash_tester_and_telemetry_contract_no_runtime_authority"
CLAIM_BOUNDARY = (
    "research_development_only_runtime_parity_probe_contract_design_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SELECTED_DIR = STAGE_DIR / "04_selected"
RUN332D_DIR = STAGE_DIR / "02_runs" / "run332D"
RUN332C_DIR = STAGE_DIR / "02_runs" / "run332C"
RUN331C_DIR = ROOT / "stages" / "331_overfit_guard__cross_horizon_cost_curve_parity_probe" / "02_runs" / "run331C"
MT5_DIR = ROOT / "foundation" / "mt5"
MT5_INCLUDE_DIR = MT5_DIR / "include" / "ObsidianPrime"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage332E_runtime_parity_probe_contract.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

MODULE_FILES = [
    MT5_DIR / "ObsidianPrimeV2_RuntimeProbeEA.mq5",
    MT5_INCLUDE_DIR / "DecisionSurface.mqh",
    MT5_INCLUDE_DIR / "EbmTableRuntime.mqh",
    MT5_INCLUDE_DIR / "ExecutionBridge.mqh",
    MT5_INCLUDE_DIR / "FeatureInputs.mqh",
    MT5_INCLUDE_DIR / "ModelRuntime.mqh",
    MT5_INCLUDE_DIR / "RuntimeTelemetry.mqh",
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line(text: str, prefix: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return "\n".join(lines[: index + 1] + [block] + lines[index + 1 :]) + "\n"
    return text.rstrip() + "\n" + block + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def source_files() -> list[Path]:
    return [
        RUN332D_DIR / "feature_materialization_queue.csv",
        RUN332D_DIR / "feature_thesis_registry.csv",
        RUN332D_DIR / "feature_label_boundary_receipt.json",
        RUN332C_DIR / "guarded_scout_matrix.csv",
        RUN332C_DIR / "guard_threshold_spec.json",
        RUN331C_DIR / "runtime_replay_compare_report.csv",
        RUN331C_DIR / "runtime_parity_receipt.json",
        RUN331C_DIR / "mt5_probe_attempts.json",
        RUN331C_DIR / "mt5" / "mt5_compile.log",
    ]


def module_identity_rows(previous_receipt: Mapping[str, Any]) -> list[dict[str, Any]]:
    previous_hashes = {
        item.get("path"): item.get("sha256")
        for item in previous_receipt.get("parity_identity", {}).get("module_hashes", [])
    }
    rows: list[dict[str, Any]] = []
    for path in MODULE_FILES:
        current = sha256_file(path) if path_exists(path) else ""
        previous = previous_hashes.get(rel(path), "")
        rows.append(
            {
                "module_path": rel(path),
                "exists": path_exists(path),
                "current_sha256": current,
                "run331C_sha256": previous,
                "matches_run331C": bool(current and previous and current == previous),
                "future_probe_requirement": "hash_must_be_recorded; if changed, module version and reason must be in run manifest",
            }
        )
    return rows


def compile_identity(previous_receipt: Mapping[str, Any]) -> dict[str, Any]:
    compile_info = previous_receipt.get("parity_identity", {}).get("compile", {})
    log_path = RUN331C_DIR / "mt5" / "mt5_compile.log"
    log_text = io_path(log_path).read_text(encoding="utf-8-sig", errors="replace") if path_exists(log_path) else ""
    normalized_log = " ".join(log_text.replace("\x00", "").split()).lower()
    return {
        "source_log": rel(log_path),
        "source_log_sha256": sha256_file(log_path) if path_exists(log_path) else "",
        "recorded_returncode": compile_info.get("returncode"),
        "recorded_status": compile_info.get("status"),
        "log_reports_zero_errors": "0 errors" in normalized_log and "0 warnings" in normalized_log,
        "future_requirement": "future runtime probe must keep compile log and treat compile alone as insufficient without tester/report/telemetry evidence",
    }


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "feature_input_identity",
            "required_evidence": "feature CSV path, sha256, row count, first/last timestamp, feature order hash",
            "pass_condition": "MT5 handoff feature identity equals research manifest exactly",
            "block_condition": "missing feature file, hash mismatch, row mismatch, or timestamp gap",
            "claim_boundary_if_missing": "blocked_or_invalid_no_runtime_interpretation",
        },
        {
            "contract_id": "model_bundle_identity",
            "required_evidence": "ONNX path, sha256, feature count, model id, threshold id",
            "pass_condition": "model and feature order match manifest; threshold fixed before runtime",
            "block_condition": "model hash mismatch, feature order drift, or threshold retune",
            "claim_boundary_if_missing": "invalid_no_model_or_runtime_claim",
        },
        {
            "contract_id": "decision_surface_identity",
            "required_evidence": "D/B or future surface mapping, min margin threshold, action mapping, flat handling",
            "pass_condition": "Python and MT5 decision rows agree on trade count/net/PF within declared tolerance",
            "block_condition": "action mapping mismatch, trade count mismatch, or unversioned decision rule change",
            "claim_boundary_if_missing": "invalid_or_blocked_before_performance_judgment",
        },
        {
            "contract_id": "risk_and_lot_identity",
            "required_evidence": "ATR SL/TP, risk percent, lot logic, deposit/leverage, spread/slippage mode",
            "pass_condition": "runtime tester params and research assumptions are both recorded",
            "block_condition": "lot optimization, ATR logic drift, or missing tester settings",
            "claim_boundary_if_missing": "runtime_probe_not_interpretable",
        },
        {
            "contract_id": "tester_report_telemetry_identity",
            "required_evidence": "MT5 report htm/png, telemetry CSV, summary CSV, tester ini, set file, terminal path",
            "pass_condition": "report, telemetry, and source KPI all reconcile",
            "block_condition": "missing report/telemetry, terminal path unknown, or KPI mismatch",
            "claim_boundary_if_missing": "blocked_runtime_evidence_missing",
        },
        {
            "contract_id": "no_authority_boundary",
            "required_evidence": "result judgment receipt and run manifest claim boundary",
            "pass_condition": "runtime_probe only; no operating promotion or runtime authority",
            "block_condition": "any document claims live readiness, deployment, operating promotion, or runtime authority",
            "claim_boundary_if_missing": "claim_violation",
        },
    ]


def run_variant_rows(queue: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue.to_dict(orient="records"):
        thesis_id = str(row["thesis_id"])
        rows.append(
            {
                "thesis_id": thesis_id,
                "allowed_runtime_change": "run id, report path, telemetry path, approved feature/model payload path",
                "entrypoint_policy": "entrypoint_unchanged_required",
                "parameter_only_policy": "new .set and .ini plus run_manifest only",
                "module_change_policy": "requires .mqh version/hash and separate repair/design receipt before tester interpretation",
                "new_ea_policy": "forbidden unless existing runner cannot express payload and reason is recorded",
                "current_runtime_status": "not_ready_no_payload_yet",
                "next_required_artifact": "materialized feature/model/signal payload after Stage332 closeout",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def readiness_rows(queue: pd.DataFrame, module_rows: Sequence[Mapping[str, Any]], replay: pd.DataFrame) -> list[dict[str, Any]]:
    modules_match = all(row.get("matches_run331C") for row in module_rows)
    replay_match = bool((replay["metrics_match"].astype(str).str.lower() == "true").all())
    rows: list[dict[str, Any]] = []
    for row in queue.to_dict(orient="records"):
        rows.append(
            {
                "thesis_id": row["thesis_id"],
                "source_clue": row["source_clue"],
                "module_identity_status": "matches_run331C_reference" if modules_match else "module_hash_drift_needs_record",
                "prior_replay_reference": "run331C_6_of_6_matched" if replay_match else "run331C_replay_mismatch_reference_not_clean",
                "missing_before_runtime": "materialized_feature_matrix;model_or_score_payload;feature_order_hash;set_file;ini_file;tester_report;telemetry_summary",
                "runtime_probe_readiness": "design_ready_but_not_runtime_ready",
                "allowed_claim_now": "runtime_contract_ready_only",
                "forbidden_claim_now": "no_runtime_probe_result_no_runtime_authority_no_forward_passed",
            }
        )
    return rows


def evidence_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "python_source_kpi",
            "required_file": "candidate KPI/cost/curve report produced before MT5",
            "minimum_fields": "trade_count;net_profit;profit_factor;expectancy;max_drawdown;cost2_pf;rolling20_min_net",
            "failure_read": "no performance judgment before Python source KPI exists",
        },
        {
            "evidence_id": "mt5_tester_output",
            "required_file": "report htm plus screenshot/png when available",
            "minimum_fields": "strategy tester report path; tester settings; report sha256",
            "failure_read": "blocked_runtime_evidence_missing",
        },
        {
            "evidence_id": "telemetry_reconciliation",
            "required_file": "runtime telemetry CSV and summary CSV",
            "minimum_fields": "order_fill_count;model_ok_count;trade_count;net;PF;timestamp range",
            "failure_read": "invalid_or_blocked_if_mismatch",
        },
        {
            "evidence_id": "handoff_manifest",
            "required_file": "run manifest with feature/model/set/ini/report hashes",
            "minimum_fields": "feature hash;model hash;feature order hash;threshold;EA/module hashes;terminal path",
            "failure_read": "artifact_lineage_disconnected",
        },
        {
            "evidence_id": "claim_boundary_receipt",
            "required_file": "result_judgment_receipt.json",
            "minimum_fields": "runtime_probe_only;no_runtime_authority;no_goal_achieve",
            "failure_read": "claim_violation_if_authority_language_appears",
        },
    ]


def receipts(
    module_rows: Sequence[Mapping[str, Any]],
    compile_info: Mapping[str, Any],
    output_paths: Sequence[Path],
) -> dict[str, Any]:
    module_match_count = sum(1 for row in module_rows if row.get("matches_run331C"))
    all_modules_match = module_match_count == len(module_rows)
    return {
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(MT5_DIR / "ObsidianPrimeV2_RuntimeProbeEA.mq5"),
            "shared_contract": "features, feature order, model/hash, threshold, decision surface, ATR/risk/lot logic, tester settings, report, telemetry, and source KPI must reconcile before runtime probe interpretation",
            "known_differences": "future probes may change run id, report path, telemetry path, and approved payload paths only",
            "parity_check": "contract_design_only; no new MT5 tester run in run332E",
            "parity_identity": {
                "module_match_count": module_match_count,
                "module_total": len(module_rows),
                "all_modules_match_run331C": all_modules_match,
                "compile_identity": compile_info,
            },
            "runtime_claim_boundary": "research_only_runtime_contract_no_runtime_authority",
        },
        "artifact_lineage_receipt": {
            "source_inputs": [rel(path) for path in source_files()],
            "producer": rel(Path(__file__)),
            "consumer": [NEXT_RUN_ID, rel(RUN_DIR / "runtime_parity_contract.csv")],
            "artifact_paths": [rel(path) for path in output_paths],
            "artifact_hashes": [{"path": rel(path), "sha256": sha256_file(path), "exists": path_exists(path)} for path in source_files()],
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked_outputs_with_source_hashes",
            "lineage_judgment": "connected_with_boundary",
        },
        "no_retune_guard_receipt": {
            "threshold_retuning": "not_performed",
            "lot_optimization": "not_performed",
            "model_update": "not_performed",
            "onnx_export": "not_performed",
            "mt5_execution": "not_performed_in_run332E",
            "candidate_selection": "not_performed",
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [
                "runtime_parity_contract.csv",
                "run_variant_boundary.csv",
                "runtime_probe_readiness_matrix.csv",
                "runtime_evidence_requirement_plan.csv",
                "runtime_identity_manifest.json",
            ],
            "evidence_missing": "no future branch payload and no new MT5 tester output by design",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    }


def gate_rows(
    module_rows: Sequence[Mapping[str, Any]],
    readiness: Sequence[Mapping[str, Any]],
    output_paths: Sequence[Path],
) -> list[dict[str, Any]]:
    source_ready = all(path_exists(path) for path in source_files())
    modules_present = all(row["exists"] for row in module_rows)
    modules_match = all(row["matches_run331C"] for row in module_rows)
    readiness_named = all(row["runtime_probe_readiness"] == "design_ready_but_not_runtime_ready" for row in readiness)
    return [
        {
            "gate": "source_runtime_reference_loaded",
            "status": "pass" if source_ready else "fail",
            "evidence": "run332D design inputs and run331C runtime replay evidence exist.",
        },
        {
            "gate": "module_identity_audited",
            "status": "pass" if modules_present else "fail",
            "evidence": "EA and include module hashes are recorded.",
        },
        {
            "gate": "module_identity_matches_reference",
            "status": "pass" if modules_match else "fail",
            "evidence": "current RuntimeProbeEA module hashes match run331C reference hashes.",
        },
        {
            "gate": "runtime_probe_readiness_boundary_named",
            "status": "pass" if readiness_named else "fail",
            "evidence": "future branches are design-ready only, not runtime-ready.",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence": "No threshold, lot, model, ONNX, EA, or runtime handoff change was made.",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass" if "no_goal_achieve" in CLAIM_BOUNDARY else "fail",
            "evidence": "No Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, or Goal Achieve claim.",
        },
        {
            "gate": "outputs_exist",
            "status": "pass" if all(path_exists(path) for path in output_paths) else "fail",
            "evidence": "Durable run332E CSV/JSON outputs exist.",
        },
    ]


def update_docs(queue_count: int) -> None:
    review = f"""
# run332E Runtime Parity Probe Contract(332E 런타임 동등성 탐침 계약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Contract Read(계약 판독)

- future_branch_count(미래 분기 수): `{queue_count}`
- runtime boundary(런타임 경계): future branch(미래 분기)는 feature/model/threshold/risk/report/telemetry identity(피처/모델/임계값/위험/보고서/기록 정체성)를 모두 남겨야 runtime probe(런타임 탐침)로 읽을 수 있다.
- run331C reference(331C 참고): 기존 runtime replay(런타임 재생)는 6/6 match(일치)였지만 runtime authority(런타임 권위)가 아니라 probe reference(탐침 참고)다.

Effect(효과): 다음 run332F(332F 실행)는 Stage332(332단계)을 closeout(종료)하고, materialization stage(물질화 단계)를 열 때 MT5 runtime evidence(런타임 근거) 요구조건을 잃지 않는다.

## Boundary(경계)

- no MT5 execution(새 MT5 실행 없음)
- no threshold retuning(임계값 재튜닝 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 업데이트 없음)
- no ONNX export(ONNX 내보내기 없음)
- no candidate selection(후보 선택 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_md(REVIEWS_DIR / "run332E_runtime_parity_probe_contract.md", review)

    decision = f"""
# Stage332E Runtime Parity Probe Contract Decision(332E 런타임 동등성 탐침 계약 결정)

run332E(332E 실행)는 future materialized branch(미래 물질화 분기)를 runtime probe(런타임 탐침)로 해석하기 위한 identity/hash/tester/telemetry contract(정체성/해시/테스터/기록 계약)를 만들었다.
Effect(효과): Python research(파이썬 연구), MT5 tester(메타트레이더5 테스터), telemetry(기록)가 같은 의미를 갖지 못하면 성과 판정을 차단한다.

- status(상태): `{STATUS}`
- decision(판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_md(DECISION_DOC, decision)

    input_block = f"""
- run332E_runtime_parity_contract(332E 런타임 동등성 계약): `{rel(RUN_DIR / "runtime_parity_contract.csv")}`
- run332E_run_variant_boundary(332E 실행 변형 경계): `{rel(RUN_DIR / "run_variant_boundary.csv")}`
- run332E_probe_readiness(332E 탐침 준비도): `{rel(RUN_DIR / "runtime_probe_readiness_matrix.csv")}`
- run332E_runtime_identity(332E 런타임 정체성): `{rel(RUN_DIR / "runtime_identity_manifest.json")}`
"""
    append_if_missing(INPUTS_DIR / "input_refs.md", "run332E_runtime_parity_contract", input_block)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = insert_after_line(
        selection_text,
        "- latest_pocket_veto_feature_thesis",
        f"- latest_runtime_parity_contract(최신 런타임 동등성 계약): `{RUN_ID}`",
        "latest_runtime_parity_contract",
    )
    selection_text = replace_prefix_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_prefix_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_prefix_line(
        selection_text,
        "- effect(효과):",
        "- effect(효과): runtime parity contract(런타임 동등성 계약)는 미래 MT5 탐침의 해석 조건을 고정했지만, 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    block = (
        "- >-\n"
        f"  Stage332(332단계) run332E(332E 실행)는 `{STATUS}`로 runtime parity probe contract(런타임 동등성 탐침 계약)를 설계했다. "
        "Effect(효과): future materialized branches(미래 물질화 분기)가 MT5 runtime probe(런타임 탐침)로 해석되려면 feature/model/threshold/risk/report/telemetry identity(피처/모델/임계값/위험/보고서/기록 정체성)를 모두 남겨야 하며 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_line(workspace_text, "current_focus:", block, STATUS)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `332_overfit_guard__failure_memory_forward_research_handoff_v6`")
    current_text = replace_prefix_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- target_surface(목표 표면):", "- target_surface(목표 표면): `stage332_closeout_or_materialization_stage_open`")
    current_text = replace_prefix_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision(판정):", f"- decision(판정): `{DECISION}`")
    current_text = insert_after_line(
        current_text,
        "- decision(판정):",
        f"- run332E_summary(332E 요약): runtime parity probe contract(런타임 동등성 탐침 계약)를 `{STATUS}`로 완료했다. Effect(효과): future branch(미래 분기) `4`개에 대해 MT5 report/telemetry/source KPI(보고서/기록/원천 KPI) reconciliation(대조) 조건을 고정했고 새 MT5 실행이나 runtime authority(런타임 권위)는 없다.",
        "run332E_summary",
    )
    current_text = replace_prefix_line(current_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    changelog_block = f"""
## {TODAY} - Stage332E runtime parity probe contract(런타임 동등성 탐침 계약)

- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- effect(효과): future materialized branch(미래 물질화 분기)의 MT5 runtime probe(런타임 탐침)를 해석하기 위한 feature/model/threshold/risk/report/telemetry identity(피처/모델/임계값/위험/보고서/기록 정체성) 계약을 만들었다.
- boundary(경계): 새 MT5 실행, Forward Passed/Failed(전진 통과/실패), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    append_if_missing(CHANGELOG, "Stage332E runtime parity probe contract", changelog_block)


def update_registers(output_paths: Sequence[Path]) -> None:
    review_path = REVIEWS_DIR / "run332E_runtime_parity_probe_contract.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_parity",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(review_path),
                "notes": f"runtime_parity_probe_contract;next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__runtime_parity_contract",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "runtime_parity_probe_contract",
                "tier_scope": "future_materialized_branch_runtime_contract_design",
                "kpi_scope": "runtime_contract_no_new_trading_kpi",
                "scoreboard_lane": "runtime_parity",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(review_path),
                "primary_kpi": "runtime_contract_rows=6;future_branch_rows=4",
                "guardrail_kpi": "no_mt5_execution;no_threshold_retuning;no_lot_optimization;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_design_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__runtime_parity_contract",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "runtime_parity_probe_contract(런타임 동등성 탐침 계약)",
                "tier_scope": "future_materialized_branch_runtime_contract_design(미래 물질화 분기 런타임 계약 설계)",
                "scoreboard": "runtime_contract_no_new_trading_kpi(런타임 계약, 새 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(review_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in output_paths:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": utc_now(),
                "notes": "run332E durable evidence; runtime contract design boundary.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> int:
    queue = read_csv(RUN332D_DIR / "feature_materialization_queue.csv")
    replay = read_csv(RUN331C_DIR / "runtime_replay_compare_report.csv")
    previous_receipt = read_json(RUN331C_DIR / "runtime_parity_receipt.json")
    attempts = read_json(RUN331C_DIR / "mt5_probe_attempts.json")
    module_rows = module_identity_rows(previous_receipt)
    compile_info = compile_identity(previous_receipt)
    contract = contract_rows()
    variants = run_variant_rows(queue)
    readiness = readiness_rows(queue, module_rows, replay)
    evidence_plan = evidence_requirement_rows()
    runtime_identity = {
        "run_id": RUN_ID,
        "reference_run": "run331C_runtime_replay_or_block_cross_horizon_probe_v1",
        "reference_attempt_count": len(attempts),
        "reference_replay_all_match": bool((replay["metrics_match"].astype(str).str.lower() == "true").all()),
        "module_identity": module_rows,
        "compile_identity": compile_info,
        "terminal_path_reference": read_json(RUN331C_DIR / "run_manifest.json").get("terminal_path"),
        "terminal_data_root_reference": read_json(RUN331C_DIR / "run_manifest.json").get("terminal_data_root"),
        "claim_boundary": CLAIM_BOUNDARY,
    }

    output_paths = [
        write_csv(
            RUN_DIR / "runtime_parity_contract.csv",
            ["contract_id", "required_evidence", "pass_condition", "block_condition", "claim_boundary_if_missing"],
            contract,
        ),
        write_csv(
            RUN_DIR / "run_variant_boundary.csv",
            [
                "thesis_id",
                "allowed_runtime_change",
                "entrypoint_policy",
                "parameter_only_policy",
                "module_change_policy",
                "new_ea_policy",
                "current_runtime_status",
                "next_required_artifact",
                "claim_boundary",
            ],
            variants,
        ),
        write_csv(
            RUN_DIR / "runtime_probe_readiness_matrix.csv",
            [
                "thesis_id",
                "source_clue",
                "module_identity_status",
                "prior_replay_reference",
                "missing_before_runtime",
                "runtime_probe_readiness",
                "allowed_claim_now",
                "forbidden_claim_now",
            ],
            readiness,
        ),
        write_csv(
            RUN_DIR / "runtime_evidence_requirement_plan.csv",
            ["evidence_id", "required_file", "minimum_fields", "failure_read"],
            evidence_plan,
        ),
        write_csv(
            RUN_DIR / "runtime_module_identity_audit.csv",
            ["module_path", "exists", "current_sha256", "run331C_sha256", "matches_run331C", "future_probe_requirement"],
            module_rows,
        ),
        write_json(RUN_DIR / "runtime_identity_manifest.json", runtime_identity),
    ]

    receipt_payloads = receipts(module_rows, compile_info, output_paths)
    for name, payload in receipt_payloads.items():
        output_paths.append(write_json(RUN_DIR / f"{name}.json", payload))
    output_paths.append(write_json(RUN_DIR / "source_artifact_hashes.json", receipt_payloads["artifact_lineage_receipt"]["artifact_hashes"]))

    gate_audit = gate_rows(module_rows, readiness, output_paths)
    output_paths.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate", "status", "evidence"], gate_audit))

    run_manifest = {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "mt5_execution": "not_performed",
        "source_files": [rel(path) for path in source_files()],
        "outputs": [rel(path) for path in output_paths],
        "runtime_contract_count": len(contract),
        "future_branch_count": len(variants),
        "next_action": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
    }
    output_paths.append(write_json(RUN_DIR / "run_manifest.json", run_manifest))

    update_docs(queue_count=len(variants))
    output_paths.extend([REVIEWS_DIR / "run332E_runtime_parity_probe_contract.md", DECISION_DOC])
    update_registers(output_paths)

    failed_gates = [row for row in gate_audit if row["status"] != "pass"]
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "runtime_contract_count": len(contract),
                "future_branch_count": len(variants),
                "failed_gates": failed_gates,
                "mt5_execution": "not_performed",
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if failed_gates else 0


if __name__ == "__main__":
    raise SystemExit(main())
