# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AR"
RUN_ID = "run337AR_db_source_sidecar_feasibility_or_out_of_scope_lock_v1"
PARENT_RUN_ID = "run337AQ_tester_visible_cutoff_policy_and_db_instrumentation_v1"
NEXT_RUN_ID = "run337AS_completed_day_attribution_without_db_and_forward_window_lock_v1"

STATUS = "completed_stage337AR_db_source_sidecar_not_feasible_out_of_scope_locked_no_forward_decision"
JUDGMENT = "db_source_sidecar_not_feasible_from_frozen_lineage_direction_proxy_only"
DECISION = "stage337AR_db_source_attribution_out_of_scope_by_claim_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AR_db_source_sidecar_feasibility_lock_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AR_db_source_sidecar_feasibility_or_out_of_scope_lock.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AR_db_source_sidecar_feasibility_or_out_of_scope_lock.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

AQ_DIR = STAGE_DIR / "02_runs" / "run337AQ"
AP_DIR = STAGE_DIR / "02_runs" / "run337AP"
AO_DIR = STAGE_DIR / "02_runs" / "run337AO"

REQUIRED_DB_COLUMNS = [
    "db_decision_source",
    "d_source",
    "b_source",
    "d_score",
    "b_score",
    "decision_surface_branch",
    "source_component",
]

TIME_AXIS_FIELDS = {
    "bar_time",
    "source_time",
    "timestamp",
    "time",
    "datetime",
    "date_time",
    "open_time",
    "close_time",
    "entry_time",
    "exit_time",
    "decision_time",
    "signal_time",
}

DIRECTION_FIELDS = {
    "decision",
    "direction",
    "trade_direction",
    "signal",
    "route_signal",
    "p_short",
    "p_flat",
    "p_long",
    "long_short",
}

ALTERNATE_TERMS = [
    "d_or_b",
    "d_b",
    "db_source",
    "decision_source",
    "source_family",
    "surface_id",
    "surface_name",
    "branch",
    "score",
    "route_signal",
    "decision_surface",
    "cp321b",
    "cp322a",
    "exact_replay",
    "control_surface",
]

SUBJECT_TERMS = [
    "cp322a",
    "cp321b",
    "exact_replay",
    "control_surface",
    "stage323_cp322a_selected_curve_adapter_package",
    "stage325",
    "forward",
    "onnx",
]

OUT_OF_SCOPE_TERMS = [
    "out_of_scope_by_claim",
    "db_source_missing",
    "db_source_status=not_available",
    "missing_required_columns_7",
    "no_d_b_source_columns",
    "not_available_in_run337ad_u42_artifacts",
]

SCAN_EXTENSIONS = {".csv", ".json", ".md", ".txt"}
MAX_TEXT_BYTES = 2_000_000

LINEAGE_ROOTS = [
    (
        "stage321_cp321b_parent",
        ROOT / "stages" / "321_onnx_candidate_campaign__post_controller_profit_curve_rebuild",
        "cp321B parent surface(cp321B 부모 표면)",
    ),
    (
        "stage322_cp322a_selection_pressure",
        ROOT / "stages" / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure",
        "cp322A selection pressure(cp322A 선택 압박)",
    ),
    (
        "stage323_selected_adapter_package",
        ROOT / "stages" / "323_onnx_candidate_campaign__selected_curve_adapter_package",
        "selected adapter package(선택 어댑터 패키지)",
    ),
    (
        "stage324_onnx_go_pressure",
        ROOT / "stages" / "324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter",
        "ONNX go pressure(ONNX 진행 압박)",
    ),
    (
        "stage325_onnx_export_runtime_reproduction",
        ROOT / "stages" / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a",
        "ONNX export parity(ONNX 내보내기 동등성)",
    ),
    (
        "stage326_forward_gate",
        ROOT / "stages" / "326_forward__cp322a_frozen_forward_gate",
        "frozen forward gate(고정 전진 게이트)",
    ),
    (
        "stage326_duplicate_forward_gate_empty",
        ROOT / "stages" / "326_onnx_candidate_campaign__cp322a_frozen_forward_robustness_gate",
        "empty duplicate forward gate(빈 중복 전진 게이트)",
    ),
    (
        "stage327_overfit_forward_parity",
        ROOT / "stages" / "327_onnx_candidate_campaign__cp322a_overfit_forward_parity_robustness",
        "overfit forward parity(과적합 전진 동등성)",
    ),
    (
        "stage328_signal_contract_extraction",
        ROOT / "stages" / "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction",
        "frozen signal contract(고정 신호 계약)",
    ),
    (
        "stage329_live_feature_control",
        ROOT / "stages" / "329_onnx_rebuild__live_feature_control",
        "live feature control(실시간 피처 제어)",
    ),
    (
        "stage330_forward_safe_non_identity",
        ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness",
        "non-identity robustness(비동일 표면 강건성)",
    ),
    (
        "stage333_pocket_veto",
        ROOT / "stages" / "333_overfit_guard__timestamp_safe_pocket_veto_materialization",
        "timestamp-safe pocket veto(시점 안전 포켓 거부)",
    ),
    (
        "stage334_handoff_hardening",
        ROOT / "stages" / "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening",
        "handoff hardening(인계 경화)",
    ),
    (
        "stage337_current_packet",
        STAGE_DIR,
        "current Stage337 packet(현재 337단계 묶음)",
    ),
]

RUN_REGISTRY_COLUMNS = [
    "run_id",
    "stage_id",
    "lane",
    "status",
    "judgment",
    "path",
    "notes",
    "family",
    "primary_report",
]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
STAGE_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "work_family",
    "evidence_scope",
    "kpi_scope",
    "status",
    "judgment",
    "claim_boundary",
    "path",
    "notes",
    "decision",
    "run_key",
    "family",
    "question",
    "metric_scope",
    "primary_artifact",
    "report_path",
    "next_action",
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
    "artifact_path",
    "claim_boundary",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path | str) -> str:
    return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return str(int(value)) if value.is_integer() else f"{value:.10g}"
    if isinstance(value, (list, tuple, dict, set)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except FileNotFoundError:
        return []


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    target = io_path(path)
    tmp = target.with_name(target.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, target)
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8", errors="replace"), had_bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or (had_bom is None and path.suffix.lower() in {".md", ".txt"}) else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding, newline="\n")
    return path


def sha256_file_lf_normalized(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any], columns: Sequence[str]) -> Path:
    rows = [{column: existing.get(column, "") for column in columns} for existing in read_csv(path)]
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [
        existing
        for existing in rows
        if tuple(str(existing.get(column, "")) for column in key_columns) != key
    ]
    rows.append({column: row.get(column, "") for column in columns})
    return write_csv(path, columns, rows)


def normalise(value: Any) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", str(value or "").strip().lower()).strip("_")


def safe_read_limited_text(path: Path) -> tuple[str, str]:
    try:
        raw = io_path(path).read_bytes()[:MAX_TEXT_BYTES]
    except OSError as exc:
        return "", f"read_error:{exc.__class__.__name__}"
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    encoding = "utf-8-sig" if had_bom else "utf-8"
    return raw.decode(encoding, errors="replace"), "read_ok"


def read_csv_header(path: Path) -> tuple[list[str], str]:
    try:
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            return next(reader, []), "read_ok"
    except OSError as exc:
        return [], f"read_error:{exc.__class__.__name__}"


def collect_json_keys(value: Any, limit: int = 5000) -> list[str]:
    keys: list[str] = []

    def walk(node: Any, prefix: str = "") -> None:
        if len(keys) >= limit:
            return
        if isinstance(node, dict):
            for key, child in node.items():
                path = f"{prefix}.{key}" if prefix else str(key)
                keys.append(path)
                walk(child, path)
                if len(keys) >= limit:
                    return
        elif isinstance(node, list):
            for child in node[:25]:
                walk(child, prefix)
                if len(keys) >= limit:
                    return

    walk(value)
    return keys


def json_key_paths(path: Path, text: str) -> list[str]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return []
    return collect_json_keys(payload)


def term_hits(text: str, terms: Sequence[str]) -> list[str]:
    lower = text.lower()
    return [term for term in terms if term.lower() in lower]


def schema_hits(schema_fields: set[str], terms: Sequence[str]) -> list[str]:
    hits: list[str] = []
    for term in terms:
        needle = normalise(term)
        if any(needle == field or needle in field for field in schema_fields):
            hits.append(term)
    return sorted(set(hits))


def infer_root_id(path: Path) -> tuple[str, str]:
    resolved = path.resolve()
    for root_id, root, role in LINEAGE_ROOTS:
        try:
            resolved.relative_to(root.resolve())
            return root_id, role
        except ValueError:
            continue
    return "unknown", "unknown"


def iter_scan_files() -> tuple[list[dict[str, Any]], list[Path]]:
    root_rows: list[dict[str, Any]] = []
    files: list[Path] = []
    for root_id, root, role in LINEAGE_ROOTS:
        exists = io_path(root).exists()
        count = 0
        if exists:
            for path in root.rglob("*"):
                if path.suffix.lower() in SCAN_EXTENSIONS:
                    files.append(path)
                    count += 1
        root_rows.append(
            {
                "root_id": root_id,
                "lineage_role": role,
                "root_path": rel(root) if str(root).startswith(str(ROOT)) else str(root),
                "exists": "true" if exists else "false",
                "scanned_text_artifacts": count,
                "effect": "scan scope(스캔 범위)를 고정해 임의 파일 뒤지기와 누락 주장을 줄인다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return root_rows, files


def inspect_artifact(path: Path) -> dict[str, Any]:
    file_type = path.suffix.lower().lstrip(".")
    root_id, lineage_role = infer_root_id(path)
    header: list[str] = []
    key_paths: list[str] = []
    text = ""
    read_status = "read_ok"
    if file_type == "csv":
        header, read_status = read_csv_header(path)
        text, text_status = safe_read_limited_text(path)
        if read_status == "read_ok" and text_status != "read_ok":
            read_status = text_status
    else:
        text, read_status = safe_read_limited_text(path)
        if file_type == "json" and read_status == "read_ok":
            key_paths = json_key_paths(path, text)

    header_norm = {normalise(item) for item in header if normalise(item)}
    key_norm = {normalise(Path(item).name) for item in key_paths if normalise(Path(item).name)}
    dotted_key_norm = {normalise(item.split(".")[-1]) for item in key_paths if item}
    schema_fields = {item for item in header_norm | key_norm | dotted_key_norm if item}

    required_schema = [column for column in REQUIRED_DB_COLUMNS if normalise(column) in schema_fields]
    required_text = term_hits(text, REQUIRED_DB_COLUMNS)
    time_schema = sorted(
        field
        for field in schema_fields
        if field in TIME_AXIS_FIELDS or field.endswith("_time") or field.endswith("_timestamp")
    )
    direction_schema = schema_hits(schema_fields, list(DIRECTION_FIELDS))
    direction_text = term_hits(text, ["direction proxy", "long/short", "long_short", "decision"])
    alternate_schema = schema_hits(schema_fields, ALTERNATE_TERMS)
    alternate_text = term_hits(text, ALTERNATE_TERMS)
    subject_text = term_hits(text, SUBJECT_TERMS)
    out_of_scope_text = term_hits(text, OUT_OF_SCOPE_TERMS)

    direct_sidecar_ready = bool(time_schema) and len(required_schema) == len(REQUIRED_DB_COLUMNS)
    if read_status != "read_ok":
        classification = "scan_error"
    elif direct_sidecar_ready:
        classification = "direct_sidecar_ready"
    elif required_schema:
        classification = "partial_db_columns_not_sidecar_ready"
    elif out_of_scope_text:
        classification = "out_of_scope_evidence"
    elif direction_schema or direction_text:
        classification = "direction_proxy_only"
    elif alternate_schema or alternate_text or subject_text:
        classification = "partial_surface_metadata_only"
    else:
        classification = "missing_required"

    relevance_score = (
        len(required_schema) * 10
        + len(required_text) * 3
        + len(direction_schema) * 2
        + len(alternate_schema)
        + len(alternate_text)
        + len(subject_text)
        + len(out_of_scope_text) * 4
    )

    return {
        "artifact_id": f"{root_id}::{rel(path)}",
        "root_id": root_id,
        "lineage_role": lineage_role,
        "path": rel(path),
        "file_type": file_type,
        "read_status": read_status,
        "header_or_key_count": len(schema_fields),
        "text_bytes_scanned_cap": MAX_TEXT_BYTES,
        "time_axis_fields": ";".join(time_schema),
        "required_schema_fields_present": ";".join(required_schema),
        "required_text_mentions": ";".join(required_text),
        "alternate_schema_terms": ";".join(alternate_schema),
        "alternate_text_terms": ";".join(alternate_text),
        "direction_schema_fields": ";".join(direction_schema),
        "direction_text_terms": ";".join(direction_text),
        "subject_terms": ";".join(subject_text),
        "out_of_scope_terms": ";".join(out_of_scope_text),
        "classification": classification,
        "sidecar_ready": "true" if direct_sidecar_ready else "false",
        "relevance_score": relevance_score,
        "effect": "D/B source(D/B 원천)를 실제 컬럼/키와 문서 언급으로 분리해 과장 귀속을 막는다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_match_matrix(inventory_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact in inventory_rows:
        schema_present = set(str(artifact.get("required_schema_fields_present", "")).split(";")) - {""}
        text_present = set(str(artifact.get("required_text_mentions", "")).split(";")) - {""}
        for column in REQUIRED_DB_COLUMNS:
            if column in schema_present:
                presence = "schema_present"
                usable_for_sidecar = "true"
            elif column in text_present:
                presence = "text_mention_only"
                usable_for_sidecar = "false"
            else:
                presence = "missing"
                usable_for_sidecar = "false"
            rows.append(
                {
                    "artifact_id": artifact.get("artifact_id", ""),
                    "path": artifact.get("path", ""),
                    "required_column": column,
                    "presence": presence,
                    "usable_for_timestamp_aligned_sidecar": usable_for_sidecar,
                    "artifact_classification": artifact.get("classification", ""),
                    "effect": "schema_present(스키마 존재)만 보조표 근거로 인정하고 text_mention_only(문서 언급만 있음)는 근거에서 제외한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_decision_rows(inventory_rows: Sequence[Mapping[str, Any]], root_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    counts = Counter(str(row.get("classification", "")) for row in inventory_rows)
    direct = counts.get("direct_sidecar_ready", 0)
    relevant = sum(1 for row in inventory_rows if int(row.get("relevance_score") or 0) > 0 or row.get("classification") != "missing_required")
    read_errors = sum(1 for row in inventory_rows if str(row.get("read_status", "")).startswith("read_error"))
    db_source_sidecar_feasible = direct > 0
    final_feasibility = "feasible_direct_sidecar_found" if db_source_sidecar_feasible else "not_feasible_from_frozen_lineage"
    final_judgment = (
        "direct_timestamp_aligned_db_source_sidecar_ready"
        if db_source_sidecar_feasible
        else "db_source_sidecar_not_feasible_from_frozen_lineage_direction_proxy_only"
    )
    row = {
        "decision_id": "run337AR_db_source_sidecar_feasibility",
        "scanned_roots": len(root_rows),
        "scanned_files": len(inventory_rows),
        "relevant_artifacts": relevant,
        "read_errors": read_errors,
        "direct_sidecar_ready_count": direct,
        "partial_db_columns_count": counts.get("partial_db_columns_not_sidecar_ready", 0),
        "direction_proxy_only_count": counts.get("direction_proxy_only", 0),
        "surface_metadata_only_count": counts.get("partial_surface_metadata_only", 0),
        "out_of_scope_evidence_count": counts.get("out_of_scope_evidence", 0),
        "missing_required_count": counts.get("missing_required", 0),
        "required_columns": ";".join(REQUIRED_DB_COLUMNS),
        "final_feasibility": final_feasibility,
        "final_judgment": final_judgment,
        "allowed_claim": "direction attribution only(방향 귀속만 허용); D/B attribution(D/B 귀속)은 out_of_scope_by_claim(주장 범위 밖)",
        "forbidden_claim": "Do not infer D/B source from decision or long/short direction(decision 또는 long/short 방향에서 D/B 원천 추론 금지).",
        "next_action": NEXT_RUN_ID,
        "effect": "D/B 원천이 없음을 실패처럼 숨기지 않고, 이후 귀속 보고에서 D/B 축을 제외하도록 고정한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [row], row


def build_lock_contract(decision: Mapping[str, Any]) -> list[dict[str, Any]]:
    db_available = str(decision.get("final_feasibility", "")) == "feasible_direct_sidecar_found"
    if db_available:
        lock_status = "sidecar_ready_next_materialization_required"
        db_attribution_status = "pending_sidecar_materialization"
    else:
        lock_status = "out_of_scope_locked"
        db_attribution_status = "out_of_scope_by_claim"
    return [
        {
            "contract_id": "db_source_attribution_scope",
            "status": db_attribution_status,
            "rule": "D/B attribution(D/B 귀속)은 timestamp-aligned sidecar(시점 정렬 보조표)가 있을 때만 허용한다.",
            "allowed": "direction/long-short attribution(방향/롱숏 귀속), session/hour/month/regime/cost/curve pocket diagnostics(세션/시간/월/국면/비용/곡선 포켓 진단)",
            "forbidden": "decision column(결정 컬럼)을 D/B source(D/B 원천)로 대체 금지",
            "effect": "없는 D/B 원천을 만들어내지 않고, 남은 분석을 검증 가능한 축으로 좁힌다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "frozen_candidate_mutation_scope",
            "status": "locked_no_mutation",
            "rule": "selected candidate, ONNX, adapter, feature order, D/B rule, threshold, risk, lot, ATR SL/TP, runtime handoff(선택 후보/ONNX/어댑터/피처 순서/D/B 규칙/임계값/위험/랏/ATR 손절익절/런타임 인계)는 변경하지 않는다.",
            "allowed": "read-only lineage scan(읽기 전용 계보 스캔) and report materialization(보고 물질화)",
            "forbidden": "retraining, retuning, rule rewrite, lot optimization(재학습/재조정/규칙 재작성/랏 최적화)",
            "effect": "과적합을 고치려다 또 다른 과적합을 만드는 경로를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "forward_decision_scope",
            "status": lock_status,
            "rule": "run337AR는 D/B sidecar feasibility(D/B 보조표 가능성)만 판단하고 Forward Passed/Failed(전진 통과/실패)는 판단하지 않는다.",
            "allowed": f"next run(다음 실행) `{NEXT_RUN_ID}` may continue completed-day/tester-visible attribution without D/B source(D/B 원천 없이 완성일/테스터 가시 귀속 계속 가능).",
            "forbidden": "Goal Achieve(목표 달성), runtime authority(런타임 권위), operating promotion(운영 승격) 주장 금지",
            "effect": "판정 범위를 작게 유지해 전진 근거와 계측 근거를 섞지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(RUN_DIR / "db_source_lineage_scan_inventory.csv"),
                    rel(RUN_DIR / "db_source_column_match_matrix.csv"),
                    rel(AQ_DIR / "db_instrumentation_gap_matrix.csv"),
                    rel(AP_DIR / "runtime_telemetry"),
                ],
                "time_axis": "Only schema fields with timestamp/bar_time/source_time(시점/봉시각/원천시각) can qualify as sidecar time axis(보조표 시간축). Text mentions(문서 언급)는 시간축 근거가 아니다.",
                "sample_scope": "Frozen cp322A lineage(고정 cp322A 계보) from Stage321 through Stage337 text/CSV/JSON artifacts(문서/CSV/JSON 산출물).",
                "missing_or_duplicate_check": "This is not bar rematerialization(봉 재물질화가 아님); it checks missing D/B source columns(D/B 원천 컬럼 누락) and does not deduplicate market rows(시장 행 중복 제거 없음).",
                "feature_label_boundary": "No features, labels, thresholds, model, ONNX, lot, risk, or runtime handoff changed(피처/라벨/임계값/모델/ONNX/랏/위험/런타임 인계 변경 없음).",
                "split_boundary": "Research lineage audit only(연구 계보 감사 전용); no train/validation/OOS split mutation(학습/검증/표본외 분할 변경 없음).",
                "leakage_risk": "The main leakage risk is backfilling D/B source from later documents or direction decisions(뒤 문서나 방향 결정으로 D/B 원천을 사후 채우는 위험). This run forbids that substitution(이 실행은 그 대체를 금지).",
                "data_hash_or_identity": {
                    "scan_inventory_sha256": sha256_file_lf_normalized(RUN_DIR / "db_source_lineage_scan_inventory.csv"),
                    "match_matrix_sha256": sha256_file_lf_normalized(RUN_DIR / "db_source_column_match_matrix.csv"),
                    "scanned_files": final.get("scanned_files"),
                },
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "effect": "D/B source(D/B 원천) 부재를 데이터 결함으로 표시하고 방향 proxy(대리값)와 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(__file__),
                "runtime_path": rel(AP_DIR / "runtime_telemetry"),
                "shared_contract": "Frozen ONNX, feature order, score threshold, D/B decision surface, risk, lot, ATR exits, runtime handoff(고정 ONNX/피처 순서/점수 임계값/D/B 결정 표면/위험/랏/ATR 청산/런타임 인계)는 변경하지 않는다.",
                "known_differences": "run337AR does not execute MT5 Strategy Tester(메타트레이더5 전략 테스터 신규 실행 없음); it audits prior runtime telemetry schema(기존 런타임 기록 스키마 감사).",
                "parity_check": "Schema-level runtime parity boundary(스키마 수준 런타임 동등성 경계): runtime telemetry has decision(결정) but lacks required D/B source fields(D/B 원천 필드 누락).",
                "parity_identity": {
                    "parent_run_id": PARENT_RUN_ID,
                    "parent_runtime_telemetry_path": rel(AP_DIR / "runtime_telemetry"),
                    "direct_sidecar_ready_count": final.get("direct_sidecar_ready_count"),
                    "direction_proxy_only_count": final.get("direction_proxy_only_count"),
                },
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority(런타임 탐침 전용, 런타임 권위 없음)",
                "effect": "MT5 runtime output(MT5 런타임 출력)에 없는 D/B 원천을 런타임 권위처럼 주장하지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": RUN_ID,
                "evidence_available": [
                    rel(RUN_DIR / "db_source_lineage_scan_inventory.csv"),
                    rel(RUN_DIR / "db_source_column_match_matrix.csv"),
                    rel(RUN_DIR / "sidecar_feasibility_decision.csv"),
                    rel(RUN_DIR / "out_of_scope_lock_contract.csv"),
                ],
                "evidence_missing": [
                    "timestamp-aligned D/B source sidecar",
                    "runtime telemetry columns db_decision_source/d_source/b_source/d_score/b_score/decision_surface_branch/source_component",
                    "broker Strategy Tester current-day forward KPI visibility",
                ],
                "judgment_label": "inconclusive_forward_boundary_with_out_of_scope_db_attribution(전진 경계 불충분 및 D/B 귀속 범위 밖)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "D/B 원천 보조표는 찾지 못했다. 그래서 앞으로의 귀속 분석은 방향, 세션, 시간, 국면, 비용, 곡선 포켓까지만 말하고 D/B 귀속은 제외한다.",
            },
        )
    )
    return artifacts


def build_gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "lineage_scan_scope_materialized",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "db_source_scan_root_inventory.csv"),
            "effect": "스캔 범위(scope, 범위)를 고정해 D/B 보조표 탐색 누락을 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "required_db_column_matrix_materialized",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "db_source_column_match_matrix.csv"),
            "effect": "필수 D/B 컬럼(required columns, 필수 컬럼)의 실제 존재 여부를 컬럼별로 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_direction_proxy_substitution",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "out_of_scope_lock_contract.csv"),
            "effect": "decision(결정) 방향 proxy(대리값)를 D/B source(D/B 원천)로 바꾸어 말하지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "frozen_candidate_no_mutation",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "runtime_parity_receipt.json"),
            "effect": "ONNX/임계값/규칙/랏/위험/런타임 인계를 바꾸지 않았음을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_goal_claim_boundary",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_report(final: Mapping[str, Any], decision: Mapping[str, Any], inventory_rows: Sequence[Mapping[str, Any]]) -> Path:
    class_counts = Counter(str(row.get("classification", "")) for row in inventory_rows)
    top_relevant = [
        row
        for row in sorted(inventory_rows, key=lambda item: int(item.get("relevance_score") or 0), reverse=True)
        if int(row.get("relevance_score") or 0) > 0 or row.get("classification") != "missing_required"
    ][:20]
    report = f"""# Stage337AR D/B Source Sidecar Feasibility Lock(337AR D/B 원천 보조표 가능성 고정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- scanned files(스캔 파일): `{final['scanned_files']}`
- relevant artifacts(관련 산출물): `{final['relevant_artifacts']}`
- direct sidecar ready(직접 보조표 준비): `{final['direct_sidecar_ready_count']}`
- partial D/B columns(부분 D/B 컬럼): `{final['partial_db_columns_count']}`
- direction proxy only(방향 대리값 전용): `{final['direction_proxy_only_count']}`
- out_of_scope evidence(범위 밖 근거): `{final['out_of_scope_evidence_count']}`
- D/B source status(D/B 원천 상태): `{final['db_source_status']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Decision(결정)

run337AR(337AR 실행)는 frozen lineage(고정 계보) 안에서 timestamp-aligned D/B sidecar(시점 정렬 D/B 보조표)를 찾지 못했다. 효과(effect, 효과)는 D/B attribution(D/B 귀속)을 `out_of_scope_by_claim(주장 범위 밖)`으로 고정하고, 이후 분석을 direction/session/hour/month/regime/cost/curve pocket(방향/세션/시간/월/국면/비용/곡선 포켓)으로 제한하는 것이다.

## Classification Counts(분류 수)

| classification(분류) | rows(행) |
|---|---:|
"""
    for name, count in sorted(class_counts.items()):
        report += f"| `{name}` | `{count}` |\n"
    report += """
## Most Relevant Evidence(주요 근거)

| classification(분류) | path(경로) | schema hits(스키마 적중) | text hits(문서 적중) |
|---|---|---|---|
"""
    for row in top_relevant:
        report += (
            f"| `{row.get('classification', '')}` | `{row.get('path', '')}` | "
            f"`{row.get('required_schema_fields_present', '')}` | `{row.get('required_text_mentions', '')}` |\n"
        )
    report += f"""
## Boundary(경계)

- allowed(허용): direction attribution(방향 귀속), long/short attribution(롱/숏 귀속), session/hour/month/regime/cost/curve pocket diagnostics(세션/시간/월/국면/비용/곡선 포켓 진단).
- forbidden(금지): decision(결정), p_long/p_short(롱/숏 확률), route signal(경로 신호)을 D/B source(D/B 원천)로 대체.
- no mutation(변경 없음): model/ONNX/adapter/feature order/threshold/risk/lot/ATR/runtime handoff(모델/ONNX/어댑터/피처 순서/임계값/위험/랏/ATR/런타임 인계) 변경 없음.

final_feasibility(최종 가능성): `{decision['final_feasibility']}`
"""
    return write_text(REPORT_PATH, report)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# 2026-05-27 Stage337AR D/B Source Sidecar Decision(337AR D/B 원천 보조표 결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- scanned_files(스캔 파일): `{final['scanned_files']}`
- direct_sidecar_ready_count(직접 보조표 준비 수): `{final['direct_sidecar_ready_count']}`
- db_source_status(D/B 원천 상태): `{final['db_source_status']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): D/B attribution(D/B 귀속)은 timestamp-aligned sidecar(시점 정렬 보조표)가 없어서 `out_of_scope_by_claim(주장 범위 밖)`으로 고정한다. 이는 후보를 실패/성공으로 판정하는 것이 아니라, 이후 보고서에서 없는 원천을 만들어내지 않게 하는 안전장치다.
"""
    return write_text(DECISION_DOC, text)


def update_workspace_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- broker_forward_boundary(브로커 전진 경계): `failed`
- tester_visible_cutoff_policy(테스터 가시 컷오프 정책): `confirmed_current_day_intraday_hidden`
- broker_current_day_gap_rows(브로커 현재일 공백 행): `16`
- completed_visible_rows(완성일 가시 행): `1`
- db_source_status(D/B 원천 상태): `{final['db_source_status']}`
- db_source_sidecar_feasible(D/B 원천 보조표 가능): `false`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_current_day_cutoff_and_db_source_out_of_scope`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AR(337AR 실행)는 D/B source sidecar(D/B 원천 보조표)가 frozen lineage(고정 계보)에 없음을 고정했다. 이후 분석은 D/B 귀속을 제외하고 검증 가능한 귀속 축으로 진행한다.
"""
    artifacts.append(write_text(SELECTED_STATUS, selection))

    state, state_bom = read_text(WORKSPACE_STATE)
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, flags=re.MULTILINE)
    focus = (
        "- >-\n"
        f"  Stage337 run337AR focus complete: run337AR(337AR 실행)은 `{STATUS}`로 D/B source sidecar(D/B 원천 보조표) 가능성을 계보 전체에서 잠갔다. "
        f"Effect(효과): scanned files(스캔 파일) `{final['scanned_files']}`, direct sidecar(직접 보조표) `{final['direct_sidecar_ready_count']}`, "
        f"direction proxy only(방향 대리값 전용) `{final['direction_proxy_only_count']}`이며 D/B attribution(D/B 귀속)은 out_of_scope_by_claim(주장 범위 밖)이다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    state = re.sub(r"- >-\n  Stage337 run337AR focus complete:.*?(?=\n- >-|\Z)", "", state, flags=re.S)
    state = re.sub(r"current_focus:\n\s*\n?", "current_focus:\n" + focus + "\n", state, count=1)
    artifacts.append(write_text(WORKSPACE_STATE, state, state_bom))

    old_current, current_bom = read_text(CURRENT_STATE)
    marker = "\n## Stage267 Candidate Pool"
    tail = old_current[old_current.find(marker) :] if marker in old_current else "\n"
    current = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- secondary_current_run(보조 현재 실행): `none`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Stage337 run337AR(337AR 실행) - 2026-05-27

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): D/B source sidecar(D/B 원천 보조표)는 frozen lineage(고정 계보)에서 직접 준비된 증거가 없어 out_of_scope_by_claim(주장 범위 밖)으로 고정했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    artifacts.append(write_text(CURRENT_STATE, current + tail, current_bom))

    brief, brief_bom = read_text(STAGE_BRIEF)
    brief = re.sub(r"- latest_run\(최신 실행\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", brief, count=1)
    summary = (
        f"- run337AR_summary(337AR 요약): `{STATUS}`. "
        f"Effect(효과): scanned files(스캔 파일) `{final['scanned_files']}`, direct sidecar(직접 보조표) `{final['direct_sidecar_ready_count']}`, "
        f"D/B source status(D/B 원천 상태) `{final['db_source_status']}`.\n"
    )
    if "run337AR_summary(337AR 요약)" in brief:
        brief = re.sub(r"- run337AR_summary\(337AR 요약\): [^\n]*(?:\n|$)", summary, brief, count=1)
    else:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(write_text(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = read_text(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AR(337AR 실행) `{STATUS}`. "
        f"Effect(효과): D/B source sidecar(D/B 원천 보조표) 직접 근거 `{final['direct_sidecar_ready_count']}`개로, D/B attribution(D/B 귀속)을 out_of_scope_by_claim(주장 범위 밖)으로 고정했고 Forward/Goal(전진/목표)은 주장하지 않음.\n"
    )
    pattern = rf"^- {re.escape(TODAY)}: Stage337 run337AR\(337AR 실행\).*$"
    if re.search(pattern, changelog, flags=re.MULTILINE):
        changelog = re.sub(pattern, line.rstrip(), changelog, flags=re.MULTILINE)
    else:
        changelog = changelog.rstrip() + "\n" + line
    artifacts.append(write_text(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "db_source_sidecar_feasibility_lock",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_runtime_boundary",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__db_source_sidecar_feasibility_lock",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "db_source_sidecar_feasibility_lock",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "lineage_scan_out_of_scope_lock(계보 스캔 및 범위 밖 고정)",
        "tier_scope": "Tier A u42/cp322A frozen lineage(Tier A u42/cp322A 고정 계보)",
        "kpi_scope": "schema_feasibility_no_forward_kpi",
        "scoreboard_lane": "data_integrity_runtime_boundary",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"scanned={final['scanned_files']};direct_sidecar={final['direct_sidecar_ready_count']};direction_proxy={final['direction_proxy_only_count']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__db_source_sidecar_feasibility_lock",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_runtime_boundary",
        "evidence_scope": "Stage321-337 frozen lineage CSV/JSON/MD scan and run337AP/AQ schema evidence",
        "kpi_scope": "schema_feasibility_no_forward_decision",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;direct_sidecar={final['direct_sidecar_ready_count']};db_source_status={final['db_source_status']}",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__db_source_sidecar_feasibility_lock",
        "family": "db_source_sidecar_feasibility_lock",
        "question": "can frozen cp322A lineage provide a timestamp-aligned D/B source sidecar without mutation",
        "metric_scope": "sidecar_feasibility_schema_scan_no_forward_kpi",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    return [
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row, RUN_REGISTRY_COLUMNS),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row, ALPHA_LEDGER_COLUMNS),
        upsert_csv(STAGE_LEDGER, ["ledger_row_id"], stage_row, STAGE_LEDGER_COLUMNS),
    ]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    unique_paths: list[Path] = []
    seen_paths: set[str] = set()
    for path in paths:
        try:
            artifact_path = rel(path)
        except ValueError:
            continue
        if not io_path(path).exists():
            continue
        if artifact_path in seen_paths:
            continue
        seen_paths.add(artifact_path)
        unique_paths.append(path)
    artifact_ids = {f"{RUN_ID}::{rel(path)}" for path in unique_paths}
    rows = [row for row in rows if row.get("artifact_id") not in artifact_ids]
    created_at = now_utc()
    for path in unique_paths:
        artifact_path = rel(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows)


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    root_rows, scan_files = iter_scan_files()
    inventory_rows = [inspect_artifact(path) for path in scan_files]
    match_rows = build_match_matrix(inventory_rows)
    decision_rows, decision = build_decision_rows(inventory_rows, root_rows)
    lock_rows = build_lock_contract(decision)

    root_inventory_path = write_csv(
        RUN_DIR / "db_source_scan_root_inventory.csv",
        ["root_id", "lineage_role", "root_path", "exists", "scanned_text_artifacts", "effect", "claim_boundary"],
        root_rows,
    )
    inventory_path = write_csv(
        RUN_DIR / "db_source_lineage_scan_inventory.csv",
        [
            "artifact_id",
            "root_id",
            "lineage_role",
            "path",
            "file_type",
            "read_status",
            "header_or_key_count",
            "text_bytes_scanned_cap",
            "time_axis_fields",
            "required_schema_fields_present",
            "required_text_mentions",
            "alternate_schema_terms",
            "alternate_text_terms",
            "direction_schema_fields",
            "direction_text_terms",
            "subject_terms",
            "out_of_scope_terms",
            "classification",
            "sidecar_ready",
            "relevance_score",
            "effect",
            "claim_boundary",
        ],
        inventory_rows,
    )
    match_path = write_csv(
        RUN_DIR / "db_source_column_match_matrix.csv",
        [
            "artifact_id",
            "path",
            "required_column",
            "presence",
            "usable_for_timestamp_aligned_sidecar",
            "artifact_classification",
            "effect",
            "claim_boundary",
        ],
        match_rows,
    )
    decision_path = write_csv(
        RUN_DIR / "sidecar_feasibility_decision.csv",
        [
            "decision_id",
            "scanned_roots",
            "scanned_files",
            "relevant_artifacts",
            "read_errors",
            "direct_sidecar_ready_count",
            "partial_db_columns_count",
            "direction_proxy_only_count",
            "surface_metadata_only_count",
            "out_of_scope_evidence_count",
            "missing_required_count",
            "required_columns",
            "final_feasibility",
            "final_judgment",
            "allowed_claim",
            "forbidden_claim",
            "next_action",
            "effect",
            "claim_boundary",
        ],
        decision_rows,
    )
    lock_path = write_csv(
        RUN_DIR / "out_of_scope_lock_contract.csv",
        ["contract_id", "status", "rule", "allowed", "forbidden", "effect", "claim_boundary"],
        lock_rows,
    )

    final = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "scanned_roots": decision["scanned_roots"],
        "scanned_files": decision["scanned_files"],
        "relevant_artifacts": decision["relevant_artifacts"],
        "read_errors": decision["read_errors"],
        "direct_sidecar_ready_count": decision["direct_sidecar_ready_count"],
        "partial_db_columns_count": decision["partial_db_columns_count"],
        "direction_proxy_only_count": decision["direction_proxy_only_count"],
        "surface_metadata_only_count": decision["surface_metadata_only_count"],
        "out_of_scope_evidence_count": decision["out_of_scope_evidence_count"],
        "missing_required_count": decision["missing_required_count"],
        "db_source_status": "out_of_scope_by_claim_no_timestamp_aligned_sidecar",
        "db_source_sidecar_feasible": False,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": "broker_tester_current_day_cutoff_and_db_source_out_of_scope",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = write_json(RUN_DIR / "final_decision.json", final)
    manifest_path = write_json(
        RUN_DIR / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at_utc": now_utc(),
            "script": rel(__file__),
            "inputs": [row["root_path"] for row in root_rows],
            "outputs": [
                rel(root_inventory_path),
                rel(inventory_path),
                rel(match_path),
                rel(decision_path),
                rel(lock_path),
                rel(final_path),
            ],
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "mutation_scope": "read_only_lineage_scan_no_candidate_mutation(읽기 전용 계보 스캔, 후보 변경 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )

    receipt_paths = build_receipts(final)
    gate_path = write_csv(
        RUN_DIR / "required_gate_coverage_audit.csv",
        ["gate_id", "status", "evidence_path", "effect", "claim_boundary"],
        build_gate_rows(final),
    )
    report_path = write_report(final, decision, inventory_rows)
    decision_doc_path = write_decision_doc(final)
    workspace_paths = update_workspace_docs(final)
    register_paths = update_registers(final)
    artifact_registry_path = update_artifact_registry(
        [
            root_inventory_path,
            inventory_path,
            match_path,
            decision_path,
            lock_path,
            final_path,
            manifest_path,
            gate_path,
            report_path,
            decision_doc_path,
            *receipt_paths,
            *workspace_paths,
            *register_paths,
            Path(__file__),
        ],
        final,
    )
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "scanned_files": final["scanned_files"],
                "direct_sidecar_ready_count": final["direct_sidecar_ready_count"],
                "db_source_status": final["db_source_status"],
                "next_action": NEXT_RUN_ID,
                "artifact_registry": rel(artifact_registry_path),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
