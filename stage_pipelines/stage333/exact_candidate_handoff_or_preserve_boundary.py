from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-26"
FORWARD_START_ISO = "2026-04-14T00:00:00Z"

STAGE_ID = "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
NEXT_STAGE_ID = "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN_NUMBER = "run333G"
RUN_ID = "run333G_exact_candidate_runtime_handoff_or_preserve_boundary_v1"
PARENT_RUN_ID = "run333F_signal_replay_mt5_forensics_and_packaging_boundary_v1"
NEXT_RUN_ID = "run334A_design_forward_usable_onnx_handoff_contract_after_cp322a_boundary_v1"

STATUS = "completed_exact_candidate_handoff_audit_boundary_preserved_stage333_closed"
JUDGMENT = "cp322a_exact_handoff_still_missing_boundary_preserved_no_goal_achieve"
DECISION = "stage333G_cp322a_exact_handoff_missing_preserve_boundary_open_stage334_contract_hardening"
CLAIM_BOUNDARY = (
    "research_development_only_cp322a_exact_handoff_not_materialized_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
NEXT_STAGE_BOUNDARY = (
    "research_development_only_forward_usable_onnx_handoff_contract_hardening_"
    "separate_cp322a_preserved_artifact_from_new_research_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUTS_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_REVIEWS_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage333G_exact_candidate_handoff_boundary_stage334_open.md"

STAGE322_RUN_B = ROOT / "stages" / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure" / "02_runs" / "run322B"
STAGE325_RUN = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
)
STAGE323_ADAPTER = (
    ROOT
    / "stages"
    / "323_onnx_candidate_campaign__selected_curve_adapter_package"
    / "02_runs"
    / "run323A"
    / "adapter_package"
)
RUN333E_DIR = STAGE_DIR / "02_runs" / "run333E"
RUN333F_DIR = STAGE_DIR / "02_runs" / "run333F"

ONNX_EXPORT_REPORT = STAGE325_RUN / "onnx_export_report.json"
ONNX_MODEL = STAGE325_RUN / "models" / "cp322a_route_signal_identity.onnx"
FEATURE_ORDER_PARITY = STAGE325_RUN / "feature_order_parity_receipt.json"
ADAPTER_MANIFEST = STAGE323_ADAPTER / "adapter_package_manifest.json"
RUN333E_HANDOFF = RUN333E_DIR / "runtime_probe_handoff_manifest.csv"
RUN333E_BRIDGE_FEATURES = RUN333E_DIR / "signal_replay_bridge" / "m48_breadth_soft_veto_probability_bridge_features.csv"
RUN333E_BRIDGE_ONNX = RUN333E_DIR / "onnx" / "signal_payload_identity_probability_bridge.onnx"
RUN333F_DECISION = RUN333F_DIR / "final_forward_decision.json"

ROUTE_SIGNAL_FILES = [
    STAGE322_RUN_B / "features" / "run322A_cp322A_cp321b_exact_replay_control_tier_a_val_route_signal.csv",
    STAGE322_RUN_B / "features" / "run322A_cp322A_cp321b_exact_replay_control_tier_a_oos_route_signal.csv",
    STAGE322_RUN_B / "features" / "run322A_cp322A_cp321b_exact_replay_control_tier_b_val_route_signal.csv",
    STAGE322_RUN_B / "features" / "run322A_cp322A_cp321b_exact_replay_control_tier_b_oos_route_signal.csv",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
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


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
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
    index_by_key = {
        tuple(str(row.get(column, "")) for column in key_columns): index
        for index, row in enumerate(existing)
    }
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in index_by_key:
            existing[index_by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def first_csv_header(path: Path) -> list[str]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            return next(reader)
        except StopIteration:
            return []


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line_once(text: str, marker: str, insertion: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == marker:
            lines[index + 1:index + 1] = insertion.strip("\n").splitlines()
            return "\n".join(lines) + "\n"
    return insertion + "\n" + text


def append_section_once(path: Path, heading: str, body: str) -> Path:
    if path_exists(path):
        text, had_bom = read_text_lossless(path)
    else:
        text, had_bom = "", True
    if heading in text:
        return path
    new_text = text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n"
    return write_text_lossless(path, new_text, had_bom)


def scan_route_signal(path: Path) -> dict[str, Any]:
    row_count = 0
    active_count = 0
    rows_after_forward = 0
    active_after_forward = 0
    first_ts = ""
    last_ts = ""
    split = ""
    tier = ""
    package_id = ""
    branch = ""
    max_signal_abs = 0.0
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                row_count += 1
                ts = row.get("timestamp_utc", "")
                if ts:
                    first_ts = first_ts or ts
                    last_ts = ts
                split = split or row.get("split", "")
                tier = tier or row.get("tier_scope", "")
                package_id = package_id or row.get("package_id", "")
                branch = branch or row.get("materialized_branch_id", "")
                try:
                    signal = float(row.get("run322b_route_signal", "0") or 0)
                except ValueError:
                    signal = 0.0
                if abs(signal) > 0:
                    active_count += 1
                max_signal_abs = max(max_signal_abs, abs(signal))
                if ts >= FORWARD_START_ISO:
                    rows_after_forward += 1
                    if abs(signal) > 0:
                        active_after_forward += 1
    return {
        "file": rel(path),
        "exists": path_exists(path),
        "split": split,
        "tier": tier,
        "rows": row_count,
        "active_rows": active_count,
        "first_timestamp": first_ts,
        "last_timestamp": last_ts,
        "rows_after_2026_04_14": rows_after_forward,
        "active_after_2026_04_14": active_after_forward,
        "max_abs_signal": max_signal_abs,
        "package_id": package_id,
        "materialized_branch_id": branch,
        "sha256": sha256_file(path),
    }


def build_audit() -> dict[str, Any]:
    onnx_report = read_json(ONNX_EXPORT_REPORT)
    feature_receipt = read_json(FEATURE_ORDER_PARITY)
    run333f_decision = read_json(RUN333F_DECISION)
    handoff_rows = read_csv_rows(RUN333E_HANDOFF) if path_exists(RUN333E_HANDOFF) else []
    handoff_row = handoff_rows[0] if handoff_rows else {}
    route_rows = [scan_route_signal(path) for path in ROUTE_SIGNAL_FILES]
    total_forward_rows = sum(int(row["rows_after_2026_04_14"]) for row in route_rows)
    total_forward_active = sum(int(row["active_after_2026_04_14"]) for row in route_rows)
    latest_route_ts = max([row["last_timestamp"] for row in route_rows if row["last_timestamp"]] or [""])
    bridge_header = first_csv_header(RUN333E_BRIDGE_FEATURES)
    bridge_features = [column for column in bridge_header if column not in {"bar_time_server", "timestamp_utc", "row_index"}]
    cp322a_features = onnx_report.get("feature_order", [])
    exact_handoff_materializable = (
        path_exists(ONNX_MODEL)
        and cp322a_features == ["run322b_route_signal"]
        and total_forward_rows > 0
        and total_forward_active > 0
    )
    return {
        "onnx_report": onnx_report,
        "feature_receipt": feature_receipt,
        "run333f_decision": run333f_decision,
        "handoff_row": handoff_row,
        "route_rows": route_rows,
        "total_forward_rows": total_forward_rows,
        "total_forward_active": total_forward_active,
        "latest_route_ts": latest_route_ts,
        "bridge_header": bridge_header,
        "bridge_features": bridge_features,
        "cp322a_features": cp322a_features,
        "exact_handoff_materializable": exact_handoff_materializable,
    }


def write_run_artifacts(audit: Mapping[str, Any], now: str) -> list[Path]:
    route_rows = list(audit["route_rows"])
    route_path = write_csv(
        RUN_DIR / "source_route_signal_coverage.csv",
        [
            "file",
            "exists",
            "split",
            "tier",
            "rows",
            "active_rows",
            "first_timestamp",
            "last_timestamp",
            "rows_after_2026_04_14",
            "active_after_2026_04_14",
            "max_abs_signal",
            "package_id",
            "materialized_branch_id",
            "sha256",
        ],
        route_rows,
    )

    feasibility_rows = [
        {
            "check": "cp322a_candidate_onnx_exists",
            "status": "passed" if path_exists(ONNX_MODEL) else "missing",
            "evidence": rel(ONNX_MODEL),
            "effect": "cp322A ONNX(온엑스) artifact(산출물)는 남아 있지만 forward handoff(전진 인계)를 만들려면 run322b_route_signal(322B 경로 신호)이 필요하다.",
        },
        {
            "check": "cp322a_required_feature_order",
            "status": "passed" if audit["cp322a_features"] == ["run322b_route_signal"] else "failed",
            "evidence": audit["cp322a_features"],
            "effect": "identity surface(정체성 표면)는 시장 피처가 아니라 route signal(경로 신호) 하나만 소비한다.",
        },
        {
            "check": "route_signal_forward_coverage_after_2026_04_14",
            "status": "failed_missing_forward_rows" if audit["total_forward_rows"] == 0 else "passed",
            "evidence": {
                "latest_route_signal_timestamp": audit["latest_route_ts"],
                "total_forward_rows": audit["total_forward_rows"],
                "total_forward_active": audit["total_forward_active"],
            },
            "effect": "2026-04-14 이후 exact route signal(정확 경로 신호)이 없으면 cp322A exact MT5 forward(정확 MT5 전진)를 만들 수 없다.",
        },
        {
            "check": "run333e_bridge_subject_identity",
            "status": "failed_not_cp322a_exact_subject",
            "evidence": {
                "bridge_features": audit["bridge_features"],
                "bridge_type": audit["handoff_row"].get("bridge_type", ""),
                "bridge_rows": audit["handoff_row"].get("rows", ""),
            },
            "effect": "run333E bridge(333E 연결기)는 probability replay(확률 재생) 3열이며 cp322A의 run322b_route_signal(322B 경로 신호) 1열과 다르다.",
        },
        {
            "check": "exact_candidate_runtime_handoff_materialized",
            "status": "not_materialized_boundary_preserved",
            "evidence": {
                "exact_handoff_materializable": audit["exact_handoff_materializable"],
                "reason": "missing exact route signal rows after 2026-04-14",
            },
            "effect": "positive signal replay(긍정 신호 재생)는 연구 근거로 보존하지만 cp322A Forward Passed(전진 통과)로 승격하지 않는다.",
        },
    ]
    feasibility_path = write_csv(
        RUN_DIR / "exact_handoff_feasibility_report.csv",
        ["check", "status", "evidence", "effect"],
        feasibility_rows,
    )

    mismatch_rows = [
        {
            "subject": "cp322A_exact_onnx",
            "model_path": rel(ONNX_MODEL),
            "feature_count": len(audit["cp322a_features"]),
            "feature_order": audit["cp322a_features"],
            "feature_order_hash": audit["onnx_report"].get("feature_order_hash"),
            "source_kind": "route_signal_identity_surface",
            "forward_authority": "blocked_missing_forward_route_signal",
        },
        {
            "subject": "run333E_signal_payload_bridge",
            "model_path": rel(RUN333E_BRIDGE_ONNX),
            "feature_count": len(audit["bridge_features"]),
            "feature_order": audit["bridge_features"],
            "feature_order_hash": audit["handoff_row"].get("feature_order_hash", ""),
            "source_kind": audit["handoff_row"].get("bridge_type", ""),
            "forward_authority": "research_only_not_candidate_onnx",
        },
    ]
    mismatch_path = write_csv(
        RUN_DIR / "bridge_subject_mismatch_report.csv",
        ["subject", "model_path", "feature_count", "feature_order", "feature_order_hash", "source_kind", "forward_authority"],
        mismatch_rows,
    )

    option_rows = [
        {
            "option": "reuse_stage322_route_signal_files",
            "verdict": "not_feasible_for_forward",
            "changes_cp322a": "no",
            "evidence": f"latest_route_signal_timestamp={audit['latest_route_ts']}; rows_after_2026_04_14={audit['total_forward_rows']}",
            "effect": "old-window exact replay(과거창 정확 재생)는 새 forward MT5 input(전진 MT5 입력)을 만들지 못한다.",
        },
        {
            "option": "promote_run333E_identity_bridge_to_cp322a",
            "verdict": "forbidden_wrong_subject",
            "changes_cp322a": "yes_wrong_input_surface",
            "evidence": f"cp322A_features={audit['cp322a_features']}; run333E_features={audit['bridge_features']}",
            "effect": "positive MT5(양수 MT5)를 exact cp322A(정확 cp322A) 근거로 바꾸는 subject swap(주체 바꿔치기)이 된다.",
        },
        {
            "option": "derive_run322b_route_signal_from_run333E_probabilities",
            "verdict": "forbidden_not_exact_repair",
            "changes_cp322a": "yes_new_generator",
            "evidence": "run333E payload contains p_short/p_flat/p_long, not frozen run322b_route_signal source.",
            "effect": "새 generator(생성기)를 만드는 것이며 frozen cp322A(고정 cp322A) replay(재생)가 아니다.",
        },
        {
            "option": "use_run333F_positive_kpi_as_forward_pass",
            "verdict": "forbidden_claim_boundary",
            "changes_cp322a": "yes_wrong_claim",
            "evidence": audit["run333f_decision"].get("claim_boundary", ""),
            "effect": "KPI(핵심지표) 양수만으로 runtime authority(런타임 권위)나 Goal Achieve(목표 달성)를 만들 수 없다.",
        },
        {
            "option": "open_forward_usable_onnx_contract_hardening_stage",
            "verdict": "allowed_research_next_stage",
            "changes_cp322a": "no_cp322a_preserved",
            "evidence": NEXT_STAGE_ID,
            "effect": "cp322A(322A 후보)는 보존하고, forward-usable ONNX(전진 사용 가능 온엑스) handoff(인계) 계약을 별도 연구로 다룬다.",
        },
    ]
    option_path = write_csv(
        RUN_DIR / "repair_option_matrix.csv",
        ["option", "verdict", "changes_cp322a", "evidence", "effect"],
        option_rows,
    )

    final_decision = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "cp322a_exact_forward_blocked": "confirmed_exact_handoff_missing_after_2026_04_13",
        "goal_achieve": "not_claimed",
        "selected_candidate": "none",
        "exact_candidate_runtime_handoff_materialized": False,
        "stage333_closed": True,
        "stage334_opened": True,
        "next_stage": NEXT_STAGE_ID,
        "next_action": NEXT_RUN_ID,
        "reason": "cp322A ONNX is an identity surface over run322b_route_signal; the exact route-signal files stop at 2026-04-13 22:00:00 and run333E is a different probability bridge, so exact forward handoff is not materialized under frozen rules.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    decision_path = write_json(RUN_DIR / "final_forward_decision.json", final_decision)

    runtime_parity = {
        "research_path": rel(Path(__file__)),
        "runtime_path": rel(ONNX_MODEL),
        "shared_contract": {
            "candidate": "cp322A_cp321b_exact_replay_control_surface",
            "required_feature_order": audit["cp322a_features"],
            "required_forward_input": "run322b_route_signal after 2026-04-13",
        },
        "known_differences": [
            "run333E uses p_short/p_flat/p_long probability bridge(확률 연결기) and is not the cp322A route-signal identity input(경로 신호 정체성 입력).",
            "Stage322 route-signal files(경로 신호 파일)은 2026-04-13 22:00:00에서 끝나며 2026-04-14 이후 행이 없다.",
        ],
        "parity_check": "artifact_hash_and_forward_coverage_audit_no_new_mt5_run",
        "parity_identity": {
            "cp322a_onnx_sha256": sha256_file(ONNX_MODEL),
            "onnx_feature_order_hash": audit["onnx_report"].get("feature_order_hash"),
            "run333e_bridge_onnx_sha256": sha256_file(RUN333E_BRIDGE_ONNX),
            "run333e_bridge_feature_order_hash": audit["handoff_row"].get("feature_order_hash", ""),
        },
        "runtime_claim_boundary": "research_only_exact_cp322a_runtime_handoff_not_materialized",
    }
    runtime_path = write_json(RUN_DIR / "runtime_parity_receipt.json", runtime_parity)

    model_validation = {
        "model_subject": "cp322A_cp321b_exact_replay_control_surface",
        "frozen_model_unchanged": True,
        "threshold_retuned": False,
        "lot_optimized": False,
        "feature_order_changed": False,
        "exact_forward_input_available": audit["total_forward_rows"] > 0,
        "judgment": "model_artifact_preserved_forward_input_missing",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_path = write_json(RUN_DIR / "model_validation_receipt.json", model_validation)

    data_integrity = {
        "forward_start": FORWARD_START_ISO,
        "route_signal_latest_timestamp": audit["latest_route_ts"],
        "route_signal_forward_rows": audit["total_forward_rows"],
        "run333e_bridge_rows": audit["handoff_row"].get("rows", ""),
        "data_judgment": "forward_market_data_exists_for_signal_replay_but_exact_cp322a_route_signal_handoff_missing",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_path = write_json(RUN_DIR / "data_integrity_receipt.json", data_integrity)

    result_path = write_csv(
        RUN_DIR / "result_judgment.csv",
        ["run_id", "status", "judgment", "decision", "forward_passed", "forward_failed", "goal_achieve", "next_action", "claim_boundary"],
        [
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )

    gate_path = write_csv(
        RUN_DIR / "required_gate_coverage_audit.csv",
        ["gate", "status", "evidence_path", "effect"],
        [
            {
                "gate": "runtime_evidence_gate(런타임 근거 게이트)",
                "status": "passed_with_boundary",
                "evidence_path": rel(runtime_path),
                "effect": "exact cp322A runtime handoff(정확 cp322A 런타임 인계)는 만들지 않았고, 왜 못 만드는지 기록했다.",
            },
            {
                "gate": "source_authority_audit(원천 권위 감사)",
                "status": "passed_boundary_preserved",
                "evidence_path": rel(mismatch_path),
                "effect": "run333E bridge(333E 연결기)를 cp322A exact ONNX(정확 온엑스)로 승격하지 않는다.",
            },
            {
                "gate": "result_judgment(결과 판정)",
                "status": "passed_no_goal_achieve",
                "evidence_path": rel(result_path),
                "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다.",
            },
            {
                "gate": "stage_closeout(단계 종료)",
                "status": "passed_stage334_opened",
                "evidence_path": rel(DECISION_DOC),
                "effect": "Stage333(333단계)는 no selection(선택 없음)으로 닫고 Stage334(334단계)를 연다.",
            },
        ],
    )

    lineage = {
        "source_inputs": [
            rel(ONNX_EXPORT_REPORT),
            rel(ONNX_MODEL),
            rel(RUN333E_HANDOFF),
            rel(RUN333F_DECISION),
            *[rel(Path(row["file"])) for row in route_rows],
        ],
        "producer": rel(Path(__file__)),
        "consumer": [rel(DECISION_DOC), rel(NEXT_SPEC_DIR / "stage_brief.md"), rel(NEXT_SELECTED_DIR / "selection_status.md")],
        "artifact_paths": [
            rel(route_path),
            rel(feasibility_path),
            rel(mismatch_path),
            rel(option_path),
            rel(decision_path),
            rel(runtime_path),
            rel(model_path),
            rel(data_path),
            rel(result_path),
            rel(gate_path),
        ],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "availability": "tracked_after_stage_closeout_push",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_path = write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage)

    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "stage333_closed": True,
        "stage334_opened": True,
        "next_action": NEXT_RUN_ID,
        "outputs": [rel(path) for path in [route_path, feasibility_path, mismatch_path, option_path, decision_path, runtime_path, model_path, data_path, result_path, gate_path, lineage_path]],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = write_json(RUN_DIR / "run_manifest.json", manifest)

    written = [
        route_path,
        feasibility_path,
        mismatch_path,
        option_path,
        decision_path,
        runtime_path,
        model_path,
        data_path,
        result_path,
        gate_path,
        lineage_path,
        manifest_path,
    ]
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in written}
    write_json(lineage_path, lineage)
    return written


def write_reports(audit: Mapping[str, Any], now: str) -> list[Path]:
    review = write_md(
        REVIEWS_DIR / "run333G_exact_candidate_handoff_boundary.md",
        f"""
# run333G Exact Candidate Handoff Boundary(333G 정확 후보 인계 경계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- cp322A exact forward blocked(cp322A 정확 전진 차단): `confirmed_exact_handoff_missing_after_2026_04_13`
- Goal Achieve(목표 달성): `not_claimed`

## Finding(발견)

cp322A(322A 후보) ONNX(온엑스)는 `run322b_route_signal` 1개 feature(피처)를 소비하는 identity surface(정체성 표면)이다. Stage322(322단계) route signal(경로 신호) 파일의 latest timestamp(최신 시각)는 `{audit['latest_route_ts']}`이고, 2026-04-14 이후 exact route signal rows(정확 경로 신호 행)는 `{audit['total_forward_rows']}`개다.

run333E(333E 실행)의 positive MT5(양수 MT5) 근거는 `{audit['bridge_features']}` probability bridge(확률 연결기)에서 왔다. Effect(효과): 이 근거는 useful research evidence(유용한 연구 근거)이지만 exact cp322A ONNX runtime handoff(정확 cp322A 온엑스 런타임 인계)가 아니다.

## Closeout(종료)

Stage333(333단계)는 no selection(선택 없음)으로 닫고 Stage334(334단계) `{NEXT_STAGE_ID}`를 연다.

Effect(효과): cp322A(322A 후보)는 research artifact(연구 산출물)로 보존하고, 다음 단계는 forward-usable ONNX handoff contract(전진 사용 가능 온엑스 인계 계약)를 overfit(과적합) 없이 분리해서 다룬다.

Next(다음): `{NEXT_RUN_ID}`
""",
    )

    final_stage = write_md(
        REVIEWS_DIR / "final_stage333_decision_report.md",
        f"""
# Final Stage333 Decision(333단계 최종 결정)

- stage_id(단계 ID): `{STAGE_ID}`
- closed_by(종료 실행): `{RUN_ID}`
- status(상태): `closed_no_selection`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`

Stage333(333단계)는 timestamp-safe pocket veto(타임스탬프 안전 포켓 거부) materialization(물질화), guarded scoring(방어 점수화), signal replay MT5 forensics(신호 재생 MT5 포렌식), exact handoff boundary audit(정확 인계 경계 감사)를 완료했다.

Effect(효과): run333E/F(333E/F 실행)의 양수 MT5(메타트레이더5) 근거는 보존하지만, cp322A exact ONNX(정확 온엑스)의 forward authority(전진 권위)는 만들지 않는다.
""",
    )

    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage333G Exact Candidate Handoff Boundary Decision(333G 정확 후보 인계 경계 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- cp322A exact forward blocked(cp322A 정확 전진 차단): `confirmed_exact_handoff_missing_after_2026_04_13`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cp322A exact handoff(정확 인계)는 여전히 materialize(물질화)하지 않고, forward-usable ONNX handoff contract(전진 사용 가능 온엑스 인계 계약)를 새 연구 단계로 분리한다.
""",
    )
    return [review, final_stage, decision]


def write_stage_docs(audit: Mapping[str, Any]) -> list[Path]:
    stage333_status = write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage333 Selection Status(333단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_missing`
- latest_runtime_probe(최신 런타임 탐침): `run333E_runtime_probe_queue_or_failure_memory_from_screen_v1`
- latest_forensics_review(최신 포렌식 검토): `run333F_signal_replay_mt5_forensics_and_packaging_boundary_v1`
- latest_exact_handoff_audit(최신 정확 인계 감사): `{RUN_ID}`
- supportive_signal_evidence_not_selection(선택이 아닌 신호 근거): `m48_breadth_soft_veto_replay`
- stage_status(단계 상태): `closed_no_selection`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run333E/F(333E/F 실행) MT5(메타트레이더5) signal replay(신호 재생)는 연구 근거로 보존하되 cp322A exact ONNX handoff(정확 온엑스 인계) 판정과 분리한다.
""",
    )

    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `closed_no_selection`")
        if "closed_by(종료 실행)" not in text:
            text = text.rstrip() + f"\n- closed_by(종료 실행): `{RUN_ID}`\n"
        write_text_lossless(STAGE_BRIEF, text, had_bom)

    NEXT_SPEC_DIR.mkdir(parents=True, exist_ok=True)
    NEXT_INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    NEXT_REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    NEXT_SELECTED_DIR.mkdir(parents=True, exist_ok=True)

    next_brief = write_md(
        NEXT_SPEC_DIR / "stage_brief.md",
        f"""
# Stage334 Forward-Usable ONNX Handoff Contract Hardening(334단계 전진 사용 가능 온엑스 인계 계약 경화)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- status(상태): `open_planned`
- opened_by(개방 실행): `{RUN_ID}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- active_question(활성 질문): cp322A exact handoff(정확 인계)가 없는 상태에서 positive signal replay evidence(긍정 신호 재생 근거)를 과적합 없이 forward-usable ONNX handoff contract(전진 사용 가능 온엑스 인계 계약)로 분리할 수 있는가?
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`

Effect(효과): cp322A(322A 후보)는 preserved research artifact(보존 연구 산출물)로 두고, 다음 연구는 exact replay(정확 재생), non-identity ONNX(비정체성 온엑스), runtime handoff(런타임 인계), cost/curve/parity guard(비용/곡선/동등성 방어)를 같은 계약으로 묶는다.
""",
    )

    input_refs = write_md(
        NEXT_INPUTS_DIR / "input_refs.md",
        f"""
# Stage334 Input References(334단계 입력 참조)

- Stage333G exact handoff boundary(정확 인계 경계): `stages/{STAGE_ID}/02_runs/run333G/final_forward_decision.json`
- Stage333F signal replay forensics(신호 재생 포렌식): `stages/{STAGE_ID}/02_runs/run333F/final_forward_decision.json`
- Stage333E MT5 report/telemetry(MT5 보고서/실행기록): `stages/{STAGE_ID}/02_runs/run333E/`
- Stage325 cp322A ONNX package(cp322A 온엑스 패키지): `stages/325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a/02_runs/run325A/`
- Stage329H exact handoff blocker(정확 인계 차단 사유): `stages/329_onnx_rebuild__live_feature_control/03_reviews/run329H_cp322a_exact_handoff_repair_feasibility.md`

Effect(효과): 다음 단계는 positive KPI(긍정 핵심지표)를 바로 후보로 삼지 않고, handoff identity(인계 정체성)와 overfit guard(과적합 방어)를 먼저 계약화한다.
""",
    )

    next_selection = write_md(
        NEXT_SELECTED_DIR / "selection_status.md",
        f"""
# Stage334 Selection Status(334단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_missing`
- active_question(활성 질문): `forward_usable_onnx_handoff_contract_hardening_without_overfit`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 새 단계는 ONNX(온엑스)를 바로 고르지 않고, exact subject boundary(정확 주체 경계), handoff contract(인계 계약), parity evidence(동등성 근거)를 먼저 닫는다.
""",
    )

    next_ledger = write_csv(
        NEXT_REVIEWS_DIR / "stage_run_ledger.csv",
        ["ledger_row_id", "stage_id", "run_id", "work_family", "evidence_scope", "kpi_scope", "status", "judgment", "claim_boundary", "path", "notes", "decision"],
        [],
    )
    return [stage333_status, STAGE_BRIEF, next_brief, input_refs, next_selection, next_ledger]


def update_state_docs() -> list[Path]:
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
    else:
        text, had_bom = "", False
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
    text = replace_prefix_line(text, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    focus_insert = f"""- >-
  Stage334(334단계) `{NEXT_STAGE_ID}`를 open_planned(열림 계획)로 열었다. Effect(효과): cp322A exact handoff(정확 인계)가 없는 상태에서 forward-usable ONNX handoff contract(전진 사용 가능 온엑스 인계 계약)를 overfit(과적합) 없이 분리해 검증한다.
- >-
  Stage333(333단계) run333G(333G 실행)는 `{STATUS}`로 exact candidate handoff audit(정확 후보 인계 감사)를 닫았다. Effect(효과): route signal(경로 신호)은 2026-04-13 22:00:00에서 끝나며 run333E bridge(333E 연결기)는 cp322A exact ONNX(정확 온엑스)가 아니므로 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 없다."""
    text = insert_after_line_once(text, "current_focus:", focus_insert, "run333G(333G 실행)")
    write_text_lossless(WORKSPACE_STATE, text, had_bom)

    text, had_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(활성 단계):": f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`",
        "- source_stage(원천 단계):": f"- source_stage(원천 단계): `{STAGE_ID}`",
        "- target_surface(목표 표면):": "- target_surface(목표 표면): `forward_usable_onnx_handoff_contract_hardening`",
        "- status(상태):": "- status(상태): `open_planned_stage334_after_stage333_closeout`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = f"- run333G_summary(333G 요약): exact candidate handoff audit(정확 후보 인계 감사)를 `{STATUS}`로 닫았다. Effect(효과): cp322A route signal(경로 신호)은 2026-04-14 이후 없고 run333E bridge(333E 연결기)는 다른 주체라서 Stage333(333단계)는 no selection(선택 없음)으로 닫고 Stage334(334단계)를 연다."
    text = insert_after_line_once(text, "- decision(판정): `" + DECISION + "`", summary, "run333G_summary")
    text = replace_prefix_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`")
    write_text_lossless(CURRENT_STATE, text, had_bom)

    append_section_once(
        CHANGELOG,
        "## 2026-05-26 - Stage333G Exact Candidate Handoff Boundary and Stage334 Open(333G 정확 후보 인계 경계 및 334단계 개방)",
        f"""
- run333G(333G 실행): cp322A exact candidate runtime handoff(정확 후보 런타임 인계) 가능성을 다시 감사했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): exact route signal(정확 경로 신호)은 2026-04-14 이후 없고 run333E bridge(333E 연결기)는 다른 주체라서 cp322A Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    return [WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def write_stage333_ledger() -> None:
    columns = [
        "row_id",
        "stage_id",
        "run_id",
        "view",
        "tier_scope",
        "scoreboard",
        "status",
        "judgment",
        "evidence_boundary",
        "report_path",
        "notes",
        "decision",
    ]
    rows: list[dict[str, Any]] = []
    if path_exists(STAGE_LEDGER):
        with io_path(STAGE_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                if row.get("run_id") == RUN_ID or row.get("row_id") == f"{RUN_ID}__exact_handoff_boundary":
                    continue
                rows.append({column: row.get(column, "") for column in columns})
    rows.append(
        {
            "row_id": f"{RUN_ID}__exact_handoff_boundary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "exact_candidate_runtime_handoff_boundary(정확 후보 런타임 인계 경계)",
            "tier_scope": "cp322a_exact_route_signal_subject(cp322A 정확 경로 신호 주체)",
            "scoreboard": "runtime_handoff_feasibility_no_new_mt5(런타임 인계 가능성 새 MT5 없음)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "evidence_boundary": CLAIM_BOUNDARY,
            "report_path": f"stages/{STAGE_ID}/03_reviews/run333G_exact_candidate_handoff_boundary.md",
            "notes": "stage333_closed_no_selection;stage334_opened;goal_achieve_not_claimed.",
            "decision": DECISION,
        }
    )
    write_csv(STAGE_LEDGER, columns, rows)


def update_registries(artifacts: Sequence[Path], now: str) -> None:
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
                "path": f"stages/{STAGE_ID}/03_reviews/run333G_exact_candidate_handoff_boundary.md",
                "notes": "exact_handoff_missing;stage333_closed;stage334_opened;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__exact_handoff_boundary",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "exact_candidate_runtime_handoff_boundary",
                "tier_scope": "cp322a_exact_route_signal_subject",
                "kpi_scope": "runtime_handoff_feasibility_no_new_mt5",
                "scoreboard_lane": "runtime_parity",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run333G_exact_candidate_handoff_boundary.md",
                "primary_kpi": "exact_route_signal_forward_rows=0",
                "guardrail_kpi": "run333E_identity_bridge_not_candidate_onnx;goal_achieve_not_claimed",
                "external_verification_status": "artifact_hash_and_forward_coverage_audit_no_new_mt5_run",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    write_stage333_ledger()
    artifact_rows = []
    for path in artifacts:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage333G_exact_handoff_boundary_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID if STAGE_ID in rel(path) else NEXT_STAGE_ID if NEXT_STAGE_ID in rel(path) else STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "exact handoff boundary and stage transition artifact; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    now = utc_now()
    audit = build_audit()
    run_artifacts = write_run_artifacts(audit, now)
    report_artifacts = write_reports(audit, now)
    stage_artifacts = write_stage_docs(audit)
    state_artifacts = update_state_docs()
    all_artifacts = [Path(__file__), *run_artifacts, *report_artifacts, *stage_artifacts, *state_artifacts]
    update_registries(all_artifacts, now)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "exact_handoff_materialized": False,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "stage333_closed": True,
                "stage334_opened": True,
                "next_action": NEXT_RUN_ID,
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
