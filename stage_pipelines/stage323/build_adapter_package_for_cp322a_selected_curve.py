from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402


STAGE323_ID = "323_onnx_candidate_campaign__selected_curve_adapter_package"
STAGE324_ID = "324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter"
RUN_ID = "run323A_build_adapter_package_for_cp322a_selected_curve_v1"
SOURCE_RUN_ID = "run322C_review_cp321b_curve_stability_pressure_mt5_probe_v1"
SOURCE_MT5_RUN_ID = "run322B_execute_cp321b_curve_stability_pressure_mt5_probe_v1"
STATUS = "completed_selected_curve_adapter_package_stage324_opened"
JUDGMENT = "adapter_package_built_no_onnx_readiness"
SELECTED_CANDIDATE = "cp322A_cp321b_exact_replay_control_surface"
SELECTED_BRANCH = "run322A_cp322A_cp321b_exact_replay_control"
ADAPTER_PACKAGE_ID = "stage323_cp322a_selected_curve_adapter_package_v1"
NEXT_ACTION = "run324A_execute_onnx_go_pressure_for_cp322a_adapter_package"
UPDATED_ON = "2026-05-26"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_onnx_go_pressure_gate"
)

STAGE323 = ROOT / "stages" / STAGE323_ID
RUN_DIR = STAGE323 / "02_runs" / "run323A"
PACKAGE_DIR = RUN_DIR / "adapter_package"
REVIEWS323 = STAGE323 / "03_reviews"
SELECTED323 = STAGE323 / "04_selected" / "selection_status.md"
REVIEW_INDEX323 = REVIEWS323 / "review_index.md"
STAGE_LEDGER323 = REVIEWS323 / "stage_run_ledger.csv"

STAGE322 = ROOT / "stages" / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
RUN322A = STAGE322 / "02_runs" / "run322A"
RUN322B = STAGE322 / "02_runs" / "run322B"
RUN322C = STAGE322 / "02_runs" / "run322C"
SOURCE_MANIFEST = RUN322A / "candidate_payload_manifest.csv"
SOURCE_BRANCH_QUEUE = RUN322A / "branch_design_queue.csv"
SOURCE_MODEL = RUN322A / "models" / f"{SELECTED_BRANCH}_stability_pressure_surface.json"
SOURCE_HANDOFF = RUN322A / "handoff" / f"{SELECTED_BRANCH}_handoff.json"
SOURCE_MT5_KPI = RUN322B / "mt5_kpi_summary.csv"
SOURCE_RUNTIME_PARITY = RUN322B / "runtime_parity_receipt.json"
SOURCE_EXECUTION_RESULT = RUN322B / "execution_result.json"
SOURCE_SCOREBOARD = RUN322C / "cp321b_curve_stability_pressure_review_scoreboard.csv"
SOURCE_SHAPE = RUN322C / "trade_frame_shape_summary.csv"
SOURCE_FAILURE = RUN322C / "failure_memory.csv"
SOURCE_STAGE322_REVIEW = STAGE322 / "03_reviews" / "run322C_review_stage323_open.md"
SOURCE_SELECTED_PACKAGE = STAGE322 / "04_selected" / "stage322_selected_candidate_package.md"
PRODUCER = ROOT / "stage_pipelines" / "stage323" / "build_adapter_package_for_cp322a_selected_curve.py"

FEATURE_ORDER_RUNTIME = PACKAGE_DIR / "feature_order_runtime.csv"
FEATURE_ORDER_SOURCE = PACKAGE_DIR / "feature_order_source.csv"
ADAPTER_SCHEMA = PACKAGE_DIR / "adapter_schema.json"
DECISION_SURFACE = PACKAGE_DIR / "decision_surface.json"
RISK_LOGIC = PACKAGE_DIR / "risk_logic.json"
RUNTIME_HANDOFF = PACKAGE_DIR / "runtime_handoff_manifest.json"
CANDIDATE_EVIDENCE = PACKAGE_DIR / "candidate_evidence_summary.csv"
FAILURE_MEMORY = PACKAGE_DIR / "failure_memory_summary.csv"
PACKAGE_MANIFEST = PACKAGE_DIR / "adapter_package_manifest.json"
PACKAGE_RECEIPT = PACKAGE_DIR / "adapter_package_hash_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS323 / "run323A_adapter_package_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-26_stage323_cp322a_adapter_package_built_stage324_open.md"

STAGE324 = ROOT / "stages" / STAGE324_ID
SPEC324 = STAGE324 / "00_spec" / "stage_brief.md"
INPUTS324 = STAGE324 / "01_inputs"
REVIEWS324 = STAGE324 / "03_reviews"
SELECTED324 = STAGE324 / "04_selected" / "selection_status.md"
STAGE_LEDGER324 = REVIEWS324 / "stage_run_ledger.csv"
REVIEW_INDEX324 = REVIEWS324 / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

FEATURE_ORDER_COLUMNS = ("position", "feature_name", "dtype", "source", "required", "meaning")
EVIDENCE_COLUMNS = ("metric", "value", "scope", "source")
FAILURE_COLUMNS = (
    "failure_id",
    "package_id",
    "failed_boundary",
    "salvage_value",
    "reopen_condition",
    "do_not_repeat",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
STAGE_LEDGER_COLUMNS = (
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
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_text(path: Path, text: str, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_md(path: Path, text: str) -> None:
    write_text(path, text, bom=True)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def sha256_file(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def load_json(path: Path) -> dict[str, Any]:
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


def selected_manifest_row() -> dict[str, str]:
    for row in read_csv_dicts(SOURCE_MANIFEST):
        if row.get("materialized_branch_id") == SELECTED_BRANCH or row.get("package_id") == SELECTED_CANDIDATE:
            return row
    raise RuntimeError(f"selected branch not found: {SELECTED_BRANCH}")


def selected_branch_row() -> dict[str, str]:
    for row in read_csv_dicts(SOURCE_BRANCH_QUEUE):
        if row.get("branch_id") == SELECTED_BRANCH or row.get("package_id") == SELECTED_CANDIDATE:
            return row
    raise RuntimeError(f"selected branch design not found: {SELECTED_BRANCH}")


def selected_scoreboard_row() -> dict[str, str]:
    for row in read_csv_dicts(SOURCE_SCOREBOARD):
        if row.get("package_id") == SELECTED_CANDIDATE:
            return row
    raise RuntimeError(f"selected scoreboard row not found: {SELECTED_CANDIDATE}")


def selected_shape_rows() -> list[dict[str, str]]:
    return [row for row in read_csv_dicts(SOURCE_SHAPE) if row.get("package_id") == SELECTED_CANDIDATE]


def stability_control_scoreboard_row() -> dict[str, str] | None:
    for row in read_csv_dicts(SOURCE_SCOREBOARD):
        if row.get("package_id") == "cp322B_score65_tight_curve_surface":
            return row
    return None


def parse_metrics(row: Mapping[str, str]) -> dict[str, Any]:
    raw = row.get("metrics", "{}")
    parsed = ast.literal_eval(raw) if raw else {}
    return dict(parsed) if isinstance(parsed, Mapping) else {}


def actual_routed_metrics() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv_dicts(SOURCE_MT5_KPI):
        if SELECTED_BRANCH not in row.get("record_view", ""):
            continue
        if row.get("route_role") != "actual_routed_total":
            continue
        metrics = parse_metrics(row)
        rows.append(
            {
                "record_view": row.get("record_view", ""),
                "tier_scope": row.get("tier_scope", ""),
                "split": row.get("split", ""),
                "status": row.get("status", ""),
                "route_role": row.get("route_role", ""),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "expectancy": metrics.get("expectancy"),
                "recovery_factor": metrics.get("recovery_factor"),
                "max_drawdown_percent": metrics.get("max_drawdown_percent"),
                "order_attempt_count": metrics.get("order_attempt_count"),
                "fill_count": metrics.get("fill_count"),
                "reject_count": metrics.get("reject_count"),
                "skip_count": metrics.get("skip_count"),
                "fill_rate": metrics.get("fill_rate"),
                "feature_ready_count": metrics.get("feature_ready_count"),
                "model_ok_count": metrics.get("model_ok_count"),
                "model_fail_count": metrics.get("model_fail_count"),
                "tier_a_used_count": metrics.get("tier_a_used_count"),
                "tier_b_fallback_used_count": metrics.get("tier_b_fallback_used_count"),
                "no_tier_count": metrics.get("no_tier_count"),
                "report_path": metrics.get("report_path"),
            }
        )
    if len(rows) != 2:
        raise RuntimeError(f"expected validation and OOS actual routed metrics, found {len(rows)}")
    return rows


def selected_feature_paths() -> list[Path]:
    features = RUN322B / "features"
    names = [
        f"{SELECTED_BRANCH}_tier_a_val_route_signal.csv",
        f"{SELECTED_BRANCH}_tier_a_oos_route_signal.csv",
        f"{SELECTED_BRANCH}_tier_b_val_route_signal.csv",
        f"{SELECTED_BRANCH}_tier_b_oos_route_signal.csv",
    ]
    return [features / name for name in names if path_exists(features / name)]


def bool_text(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def build_package(created_at: str) -> list[Path]:
    io_path(PACKAGE_DIR).mkdir(parents=True, exist_ok=True)
    manifest_row = selected_manifest_row()
    branch_row = selected_branch_row()
    score_row = selected_scoreboard_row()
    shape_rows = selected_shape_rows()
    control_row = stability_control_scoreboard_row()
    handoff = load_json(SOURCE_HANDOFF)
    model_surface = load_json(SOURCE_MODEL)
    runtime_rows = [
        {
            "position": 0,
            "feature_name": "run322b_route_signal",
            "dtype": "int8",
            "source": "Stage322 MT5 feature CSV(피처 CSV) alias for route_signal_value(경로 신호값)",
            "required": True,
            "meaning": "-1 short(매도), 0 flat(관망), +1 long(매수)",
        }
    ]
    source_rows = [
        {
            "position": 0,
            "feature_name": "route_signal_value",
            "dtype": "int8",
            "source": "Stage322 model/handoff(모델/인계) logical signal(논리 신호)",
            "required": True,
            "meaning": "logical direction signal(논리 방향 신호) mapped into run322b_route_signal",
        },
        {
            "position": 1,
            "feature_name": "candidate_decision_score",
            "dtype": "float32",
            "source": "Stage322 route feature table(경로 피처 표)",
            "required": True,
            "meaning": "decision score(판단 점수) used before frozen signal replay(동결 신호 재생)",
        },
        {
            "position": 2,
            "feature_name": "source_active_mask",
            "dtype": "int8",
            "source": "Stage322 route feature table(경로 피처 표)",
            "required": True,
            "meaning": "active/flat(활성/관망) source mask(원천 마스크)",
        },
        {
            "position": 3,
            "feature_name": "model_risk_pct",
            "dtype": "float32",
            "source": "Stage322 route feature table(경로 피처 표)",
            "required": True,
            "meaning": "risk sizing percentage(위험 크기 비율) used by MT5 risk bridge(위험 연결)",
        },
    ]
    write_csv(FEATURE_ORDER_RUNTIME, FEATURE_ORDER_COLUMNS, runtime_rows)
    write_csv(FEATURE_ORDER_SOURCE, FEATURE_ORDER_COLUMNS, source_rows)
    write_json(
        ADAPTER_SCHEMA,
        {
            "adapter_package_id": ADAPTER_PACKAGE_ID,
            "selected_candidate": SELECTED_CANDIDATE,
            "selected_branch": SELECTED_BRANCH,
            "runtime_input_features": ["run322b_route_signal"],
            "logical_signal_column": "route_signal_value",
            "runtime_feature_aliases": {"run322b_route_signal": "route_signal_value"},
            "runtime_output": {
                "score_short": "1.0 when run322b_route_signal is -1 else 0.0",
                "score_flat": "1.0 when run322b_route_signal is 0 else 0.0",
                "score_long": "1.0 when run322b_route_signal is +1 else 0.0",
            },
            "feature_order_hash": ordered_hash(["run322b_route_signal"]),
            "logical_feature_order_hash": ordered_hash(["route_signal_value"]),
            "source_feature_order_hash": ordered_hash([row["feature_name"] for row in source_rows]),
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DECISION_SURFACE,
        {
            "selected_candidate": SELECTED_CANDIDATE,
            "selected_branch": SELECTED_BRANCH,
            "branch_lane": branch_row.get("branch_lane", ""),
            "rule_name": branch_row.get("rule_name", handoff.get("rule_name", "")),
            "decision_surface_summary": branch_row.get("decision_surface", ""),
            "stage321_seed_package_id": handoff.get("stage321_seed_package_id", ""),
            "source_stage_id": handoff.get("source_stage_id", ""),
            "source_run_id": handoff.get("source_run_id", ""),
            "stage323_action": "package only(패키지만 구성); no decision surface change(판단 표면 변경 없음)",
            "surface_hashes": {
                "direction_surface_hash": manifest_row.get("direction_surface_hash", handoff.get("direction_surface_hash", "")),
                "model_feature_order_hash": manifest_row.get("model_feature_order_hash", ""),
                "runtime_feature_order_hash_logical": handoff.get("runtime_feature_order_hash", ""),
                "adapter_runtime_feature_order_hash": ordered_hash(["run322b_route_signal"]),
            },
            "discard_condition": "Stage324(324단계)에서 minimum trades(최소 거래수), 4-10 trades/day(일 4-10거래), curve pocket(곡선 포켓), package trace(패키지 추적) 중 하나라도 깨지면 ONNX-go(온엑스 진행)로 넘기지 않는다.",
            "claim_boundary": BOUNDARY,
        },
    )
    risk_keys = [
        "max_hold_bars",
        "close_on_flat_signal",
        "same_direction_reentry_cooldown_bars",
        "atr_sltp_enabled",
        "atr_period",
        "atr_stop_multiplier",
        "atr_take_profit_multiplier",
        "atr_min_stop_points",
        "atr_max_stop_points",
        "atr_min_take_profit_points",
        "atr_max_take_profit_points",
        "exit_risk_overlay_enabled",
        "model_risk_sizing_enabled",
        "model_risk_min_pct",
        "model_risk_max_pct",
        "model_risk_confidence_floor",
        "model_risk_confidence_ceiling",
        "model_risk_fallback_lot",
        "fixed_lot",
    ]
    risk_params = {key: manifest_row.get(key, handoff.get("risk_logic", {}).get(key, "")) for key in risk_keys}
    write_json(
        RISK_LOGIC,
        {
            "selected_candidate": SELECTED_CANDIDATE,
            "risk_logic_summary": "model risk sizing(모델 위험 크기) plus fixed lot(고정 랏) as used in Stage322 MT5 runtime probe(런타임 탐침)",
            "parameters": risk_params,
            "boolean_interpretation": {
                "close_on_flat_signal": bool_text(risk_params.get("close_on_flat_signal", "")),
                "atr_sltp_enabled": bool_text(risk_params.get("atr_sltp_enabled", "")),
                "exit_risk_overlay_enabled": bool_text(risk_params.get("exit_risk_overlay_enabled", "")),
                "model_risk_sizing_enabled": bool_text(risk_params.get("model_risk_sizing_enabled", "")),
            },
            "known_tradeoff": "Selected curve(선택 곡선)는 cp322C(322C 후보)보다 net profit(순수익)은 낮지만 OOS zoom pocket(표본외 확대 포켓)을 통과했다.",
            "claim_boundary": BOUNDARY,
        },
    )
    feature_paths = selected_feature_paths()
    runtime_metrics = actual_routed_metrics()
    write_json(
        RUNTIME_HANDOFF,
        {
            "selected_candidate": SELECTED_CANDIDATE,
            "adapter_package_id": ADAPTER_PACKAGE_ID,
            "research_path": rel(PRODUCER),
            "runtime_path": {
                "stage322_mt5_probe": rel(SOURCE_MT5_KPI),
                "stage322_runtime_parity_receipt": rel(SOURCE_RUNTIME_PARITY),
                "stage322_execution_result": rel(SOURCE_EXECUTION_RESULT),
            },
            "shared_contract": "run322b_route_signal(실행 신호)은 route_signal_value(경로 신호값)의 MT5 feature alias(피처 별칭)이며 -1/0/+1 의미를 유지한다.",
            "known_differences": [
                "Stage322 design artifact(설계 산출물)는 logical feature(논리 피처) route_signal_value를 쓴다.",
                "Stage322 MT5 feature CSV(피처 CSV)는 runtime column(런타임 열) run322b_route_signal을 쓴다.",
                "Stage323 Adapter(어댑터)는 이 alias(별칭)를 명시해 ONNX parity(온엑스 동등성)에서 혼동을 막는다.",
            ],
            "parity_check": "Stage322 MT5 runtime probe(런타임 탐침) completed; Stage323 packages handoff only; Stage324 must pressure before ONNX export(내보내기).",
            "parity_identity": {
                "source_model_path": rel(SOURCE_MODEL),
                "source_model_hash": sha256_file(SOURCE_MODEL),
                "source_handoff_path": rel(SOURCE_HANDOFF),
                "source_handoff_hash": sha256_file(SOURCE_HANDOFF),
                "feature_paths": [rel(path) for path in feature_paths],
                "feature_hashes": {rel(path): sha256_file(path) for path in feature_paths},
                "payload_path": manifest_row.get("payload_path", ""),
                "payload_hash": manifest_row.get("payload_hash", ""),
                "mt5_actual_routed_metrics": runtime_metrics,
            },
            "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
            "claim_boundary": BOUNDARY,
        },
    )
    evidence_rows: list[dict[str, Any]] = [
        {"metric": key, "value": value, "scope": "stage322_selected_scoreboard", "source": rel(SOURCE_SCOREBOARD)}
        for key, value in score_row.items()
        if key != "package_id"
    ]
    if control_row:
        evidence_rows.extend(
            {
                "metric": key,
                "value": value,
                "scope": "stage322_stability_control_cp322B",
                "source": rel(SOURCE_SCOREBOARD),
            }
            for key, value in control_row.items()
            if key in {"combined_net_profit", "validation_pf", "oos_pf", "validation_worst_chunk_net", "oos_worst_chunk_net", "stability_gate"}
        )
    for row in shape_rows:
        split = row.get("split", "")
        evidence_rows.extend(
            {
                "metric": key,
                "value": value,
                "scope": f"stage322_trade_frame_shape_{split}",
                "source": rel(SOURCE_SHAPE),
            }
            for key, value in row.items()
            if key not in {"package_id", "split"}
        )
    for row in runtime_metrics:
        split = row.get("split", "")
        evidence_rows.extend(
            {
                "metric": key,
                "value": value,
                "scope": f"stage322_actual_routed_{split}",
                "source": rel(SOURCE_MT5_KPI),
            }
            for key, value in row.items()
            if key not in {"split", "record_view", "tier_scope", "status", "route_role"}
        )
    write_csv(CANDIDATE_EVIDENCE, EVIDENCE_COLUMNS, evidence_rows)
    failure_rows = []
    for row in read_csv_dicts(SOURCE_FAILURE):
        item = dict(row)
        item["claim_boundary"] = BOUNDARY
        failure_rows.append(item)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    package_manifest = {
        "adapter_package_id": ADAPTER_PACKAGE_ID,
        "selected_candidate": SELECTED_CANDIDATE,
        "selected_branch": SELECTED_BRANCH,
        "created_at_utc": created_at,
        "source_stage_id": STAGE322.name,
        "source_run_id": SOURCE_RUN_ID,
        "source_mt5_run_id": SOURCE_MT5_RUN_ID,
        "runtime_feature_order_path": rel(FEATURE_ORDER_RUNTIME),
        "source_feature_order_path": rel(FEATURE_ORDER_SOURCE),
        "adapter_schema_path": rel(ADAPTER_SCHEMA),
        "decision_surface_path": rel(DECISION_SURFACE),
        "risk_logic_path": rel(RISK_LOGIC),
        "runtime_handoff_path": rel(RUNTIME_HANDOFF),
        "candidate_evidence_path": rel(CANDIDATE_EVIDENCE),
        "failure_memory_path": rel(FAILURE_MEMORY),
        "source_model_snapshot": model_surface,
        "source_handoff_snapshot": handoff,
        "adapter_package": ADAPTER_PACKAGE_ID,
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(PACKAGE_MANIFEST, package_manifest)
    package_paths = [
        FEATURE_ORDER_RUNTIME,
        FEATURE_ORDER_SOURCE,
        ADAPTER_SCHEMA,
        DECISION_SURFACE,
        RISK_LOGIC,
        RUNTIME_HANDOFF,
        CANDIDATE_EVIDENCE,
        FAILURE_MEMORY,
        PACKAGE_MANIFEST,
    ]
    package_hashes = {rel(path): sha256_file(path) for path in package_paths if path_exists(path)}
    write_json(
        PACKAGE_RECEIPT,
        {
            "adapter_package_id": ADAPTER_PACKAGE_ID,
            "selected_candidate": SELECTED_CANDIDATE,
            "package_paths": [rel(path) for path in package_paths],
            "package_hashes": package_hashes,
            "package_hash": hashlib.sha256(json.dumps(package_hashes, sort_keys=True).encode("utf-8")).hexdigest(),
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    package_paths.append(PACKAGE_RECEIPT)
    return package_paths


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def report_markdown() -> str:
    return "\n".join(
        [
            "# run323A Adapter Package Report(323A 어댑터 패키지 보고)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`",
            f"- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`",
            "- ONNX readiness(온엑스 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "Effect(효과): Stage322(322단계)에서 통과한 단일 feature(피처) 곡선 후보를 feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), runtime handoff(런타임 인계), failure memory(실패 기억)까지 묶었다.",
            "",
            "Key judgment(핵심 판정): cp322A(322A 후보)는 net profit(순수익)이 cp322C(322C 후보)보다 낮지만, cp322C는 OOS zoom pocket(표본외 확대 포켓) `-5756.29`로 실패했다. 사용자가 요구한 확대 곡선 조건 때문에 cp322A를 ONNX-go pressure(온엑스 진행 압박) 대상으로만 넘긴다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def stage324_spec_markdown() -> str:
    return f"""# Stage324 Brief(324단계 개요)

- stage_id(단계 ID): `{STAGE324_ID}`
- source_stage(원천 단계): `{STAGE323_ID}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- question(질문): Can this Adapter package(어댑터 패키지) survive ONNX-go pressure(온엑스 진행 압박) across trade density(거래 밀도), curve pocket(곡선 포켓), feature order(피처 순서), and runtime handoff(런타임 인계) before export(내보내기)?
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): export(내보내기) 전에 패키지 추적성(traceability, 추적성)과 약한 곡선 구간을 마지막으로 압박한다.

`{BOUNDARY}`
"""


def write_stage324_inputs() -> None:
    for path in (SPEC324.parent, INPUTS324, REVIEWS324, SELECTED324.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_md(SPEC324, stage324_spec_markdown())
    write_json(INPUTS324 / "adapter_package_manifest.json", load_json(PACKAGE_MANIFEST))
    write_json(INPUTS324 / "adapter_package_hash_receipt.json", load_json(PACKAGE_RECEIPT))
    write_md(
        INPUTS324 / "input_refs.md",
        f"""# Stage324 Input References(324단계 입력 참조)

- adapter_package_manifest(어댑터 패키지 목록): `{rel(INPUTS324 / 'adapter_package_manifest.json')}`
- adapter_package_hash_receipt(어댑터 패키지 해시 영수증): `{rel(INPUTS324 / 'adapter_package_hash_receipt.json')}`
- source_report(원천 보고): `{rel(REPORT)}`
- source_stage322_review(322단계 원천 검토): `{rel(SOURCE_STAGE322_REVIEW)}`

Effect(효과): Stage324(324단계)가 같은 패키지를 다시 읽고 ONNX-go pressure(온엑스 진행 압박)를 실행할 수 있게 한다.
""",
    )
    write_md(
        SELECTED324,
        f"""# Stage324 Selection Status(324단계 선택 상태)

- stage_status(단계 상태): `opened_onnx_go_pressure_after_stage323_adapter_package`
- current_packet(현재 작업 묶음): `324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE323_ID}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUTS324 / 'input_refs.md')}`
""",
    )
    write_md(
        REVIEW_INDEX324,
        f"""# Stage324 Review Index(324단계 검토 색인)

- stage_brief(단계 개요): `{rel(SPEC324)}`
- input_refs(입력 참조): `{rel(INPUTS324 / 'input_refs.md')}`
""",
    )
    write_csv(
        STAGE_LEDGER324,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage324_open",
                "stage_id": STAGE324_ID,
                "run_id": RUN_ID,
                "view": "stage324_open_onnx_go_pressure",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "scoreboard": "stage_open",
                "status": "opened_onnx_go_pressure_after_stage323_adapter_package",
                "judgment": JUDGMENT,
                "evidence_boundary": "adapter_package_built_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"adapter_package={ADAPTER_PACKAGE_ID};next_action={NEXT_ACTION}.",
            }
        ],
    )


def write_outputs(package_paths: Sequence[Path], created_at: str) -> list[Path]:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"adapter_package={ADAPTER_PACKAGE_ID};package_paths={len(package_paths)};stage322_mt5=completed",
                "evidence_missing": "Stage324 ONNX-go pressure(온엑스 진행 압박);ONNX export(온엑스 내보내기);Python inference check(파이썬 추론 확인);feature order parity(피처 순서 동등성);MT5 runtime reproduction(MT5 런타임 재현)",
                "judgment_label": JUDGMENT,
                "judgment_class": "adapter_package_built",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "어댑터 패키지는 만들어졌지만 ONNX 준비나 목표 달성은 아직 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "feature_order_traceable(피처 순서 추적 가능)",
                "status": "passed",
                "evidence_path": f"{rel(FEATURE_ORDER_RUNTIME)};{rel(FEATURE_ORDER_SOURCE)}",
                "effect": "run322b_route_signal(실행 신호)과 route_signal_value(경로 신호값)의 alias(별칭)를 분리해 기록했다.",
            },
            {
                "gate_name": "decision_surface_packaged(판단 표면 패키지화)",
                "status": "passed",
                "evidence_path": rel(DECISION_SURFACE),
                "effect": "Stage323(323단계)는 표면을 바꾸지 않고 Stage322(322단계) 선택 표면을 동결했다.",
            },
            {
                "gate_name": "risk_logic_packaged(위험 로직 패키지화)",
                "status": "passed",
                "evidence_path": rel(RISK_LOGIC),
                "effect": "MT5 runtime probe(런타임 탐침)에 쓴 보유/ATR/사이징 파라미터를 분리했다.",
            },
            {
                "gate_name": "runtime_handoff_traceable(런타임 인계 추적 가능)",
                "status": "passed",
                "evidence_path": rel(RUNTIME_HANDOFF),
                "effect": "Stage322 MT5(메타트레이더5) KPI와 feature CSV(피처 CSV)를 패키지에 연결했다.",
            },
            {
                "gate_name": "no_onnx_readiness_claim(온엑스 준비 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "Stage324(324단계) 압박 전에는 ONNX readiness(온엑스 준비)를 주장하지 않는다.",
            },
            {
                "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
                "status": "passed",
                "evidence_path": rel(GATE_AUDIT),
                "effect": "closeout(종료 기록)에 필요한 gate(게이트)를 직접 연결했다.",
            },
        ],
    )
    write_md(REPORT, report_markdown())
    write_md(
        DECISION,
        f"""# Decision(결정): Stage323 Adapter Package Built and Stage324 Opened(323단계 어댑터 패키지 구성과 324단계 개방)

- date(날짜): `{UPDATED_ON}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`
- decision(결정): Adapter package(어댑터 패키지)를 만들고 Stage324(324단계) ONNX-go pressure(온엑스 진행 압박)를 연다.
- effect(효과): ONNX export(온엑스 내보내기) 전에 trade density(거래 밀도), curve pocket(곡선 포켓), feature order parity(피처 순서 동등성), runtime handoff(런타임 인계)를 한 번 더 압박한다.
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_stage324_inputs()
    artifacts = [
        *package_paths,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
        SPEC324,
        INPUTS324 / "adapter_package_manifest.json",
        INPUTS324 / "adapter_package_hash_receipt.json",
        INPUTS324 / "input_refs.md",
        SELECTED324,
        STAGE_LEDGER324,
        REVIEW_INDEX324,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE323_ID,
            "target_stage_id": STAGE324_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_mt5_run_id": SOURCE_MT5_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": SELECTED_CANDIDATE,
            "adapter_package": ADAPTER_PACKAGE_ID,
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "created_at_utc": created_at,
            "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts.append(RUN_MANIFEST)
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source_inputs": [
                rel(SOURCE_MANIFEST),
                rel(SOURCE_BRANCH_QUEUE),
                rel(SOURCE_MODEL),
                rel(SOURCE_HANDOFF),
                rel(SOURCE_MT5_KPI),
                rel(SOURCE_SCOREBOARD),
                rel(SOURCE_SHAPE),
                rel(SOURCE_FAILURE),
                rel(SOURCE_STAGE322_REVIEW),
                rel(SOURCE_SELECTED_PACKAGE),
                rel(PRODUCER),
            ],
            "source_hashes": {
                rel(path): sha256_file(path)
                for path in [
                    SOURCE_MANIFEST,
                    SOURCE_BRANCH_QUEUE,
                    SOURCE_MODEL,
                    SOURCE_HANDOFF,
                    SOURCE_MT5_KPI,
                    SOURCE_SCOREBOARD,
                    SOURCE_SHAPE,
                    SOURCE_FAILURE,
                    SOURCE_STAGE322_REVIEW,
                    SOURCE_SELECTED_PACKAGE,
                    PRODUCER,
                ]
                if path_exists(path)
            },
            "producer": rel(PRODUCER),
            "consumer": f"{STAGE324_ID}:{NEXT_ACTION}",
            "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER323)],
            "availability": "tracked_package_required_force_add_under_ignored_02_runs",
            "lineage_judgment": "connected_with_boundary_adapter_package_built_no_onnx_claim",
        },
    )
    artifacts.append(LINEAGE)
    return artifacts


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE323_ID,
                "lane": "adapter_package_build",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"selected_candidate={SELECTED_CANDIDATE};adapter_package={ADAPTER_PACKAGE_ID};target_stage={STAGE324_ID}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__adapter_package",
                "stage_id": STAGE323_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage323_adapter_package_stage324_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "adapter_package_build(어댑터 패키지 구성)",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "adapter_package_no_onnx_readiness",
                "scoreboard_lane": "adapter_package",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"selected_candidate={SELECTED_CANDIDATE};adapter_package={ADAPTER_PACKAGE_ID}",
                "guardrail_kpi": "onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_adapter_packaging_only",
                "notes": f"target_stage={STAGE324_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    write_csv(
        STAGE_LEDGER323,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage323_closeout",
                "stage_id": STAGE323_ID,
                "run_id": RUN_ID,
                "view": "stage323_adapter_package_stage324_open",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "scoreboard": "adapter_package_manifest",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "adapter_package_built_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"adapter_package={ADAPTER_PACKAGE_ID};target_stage={STAGE324_ID}.",
            }
        ],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage323_adapter_package_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE323_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run323A adapter package(323A 어댑터 패키지)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED323).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- Adapter package(어댑터 패키지):", f"- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`")
    selected = replace_line_prefix(selected, "- ONNX readiness(온엑스 준비):", "- ONNX readiness(온엑스 준비): `not_claimed`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run323A_report", f"- run323A_report(323A 보고): `{rel(REPORT)}`")
    selected = append_once(selected, "stage324_open(324단계 개방)", f"- stage324_open(324단계 개방): `{STAGE324_ID}`")
    write_md(SELECTED323, selected)

    review_index = io_path(REVIEW_INDEX323).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX323) else "# Stage323 Review Index(323단계 검토 색인)\n"
    review_index = append_once(review_index, "run323A_report", f"- run323A_report(323A 보고): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX323, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE324_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE323_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `cp322A_adapter_onnx_go_pressure`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", f"- adapter_under_review(검토 중 어댑터): `{ADAPTER_PACKAGE_ID}`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_onnx_go_pressure_after_stage323_adapter_package`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- claim_boundary(주장 경계):",
        f"- claim_boundary(주장 경계): `{BOUNDARY}`",
    )
    current = append_once(
        current,
        "run323A_summary",
        f"- run323A_summary(323A 요약): `{SELECTED_CANDIDATE}`의 Adapter package(어댑터 패키지) `{ADAPTER_PACKAGE_ID}`를 만들고 Stage324(324단계)를 열었다. Effect(효과): ONNX readiness(온엑스 준비)는 아직 주장하지 않고, feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), runtime handoff(런타임 인계)를 다음 압박 검증으로 넘긴다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE324_ID}")
    focus = (
        f"- >-\n"
        f"  Stage324(324단계) ONNX-go pressure(온엑스 진행 압박) opened for Adapter package(어댑터 패키지) `{ADAPTER_PACKAGE_ID}` by `{RUN_ID}`. "
        f"Effect(효과): ONNX export(온엑스 내보내기) 전 trade density(거래 밀도), curve pocket(곡선 포켓), feature order(피처 순서), runtime handoff(런타임 인계)를 마지막으로 압박한다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace, bom=True)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run323A Adapter package(323A 어댑터 패키지)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): `{ADAPTER_PACKAGE_ID}`를 구성하고 Stage324(324단계)를 열었다.\n- boundary(경계): ONNX readiness(온엑스 준비)와 Goal Achieve(목표 달성)는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    for path in (RUN_DIR, PACKAGE_DIR, REVIEWS323):
        io_path(path).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    package_paths = build_package(created_at)
    artifacts = write_outputs(package_paths, created_at)
    update_registers_and_docs(created_at, artifacts)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "selected_candidate": SELECTED_CANDIDATE,
                "adapter_package": ADAPTER_PACKAGE_ID,
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "target_stage": STAGE324_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
