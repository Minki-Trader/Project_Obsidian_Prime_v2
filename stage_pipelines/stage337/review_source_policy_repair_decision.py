from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337S"
RUN_ID = "run337S_tester_visible_source_policy_repair_or_next_data_boundary_probe_v1"
PARENT_RUN_ID = "run337R_fresh_boundary_repaired_forward_attribution_and_asof_policy_review_v1"
NEXT_RUN_ID = "run337T_source_clean_u42_cost_fragility_or_tester_rollover_probe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337S_source_policy_repair_decision_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
STATUS = "completed_stage337S_source_policy_repair_decision_no_forward_decision"
JUDGMENT = "source_policy_and_tester_boundary_block_forward_decision_u42_source_clean_but_cost_fragile"
DECISION = "stage337S_open_run337T_source_clean_u42_cost_fragility_or_tester_rollover_probe_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Q_DIR = STAGE_DIR / "02_runs" / "run337Q"
RUN337R_DIR = STAGE_DIR / "02_runs" / "run337R"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337S_source_policy_repair_decision.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337S_source_policy_repair_decision.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SOURCE_RUNTIME = RUN337Q_DIR / "fresh_mt5_runtime_probe_result.csv"
SOURCE_GAP = RUN337Q_DIR / "tester_feature_last_gap_reprobe.csv"
SOURCE_ASOF = RUN337Q_DIR / "asof_source_policy_review.csv"
SOURCE_BOUNDARY = RUN337Q_DIR / "tester_date_boundary_log_audit.csv"
SOURCE_API = RUN337Q_DIR / "fresh_us100_api_probe.json"
SOURCE_CURVE = RUN337R_DIR / "curve_pocket_report.csv"
SOURCE_COST = RUN337R_DIR / "cost_stress_report.csv"
SOURCE_DB = RUN337R_DIR / "db_attribution_report.csv"

SOURCE_POLICY_MATRIX = RUN_DIR / "source_policy_repair_matrix.csv"
TESTER_WINDOW_POLICY = RUN_DIR / "tester_visible_window_policy.csv"
CANDIDATE_ROUTE_DECISION = RUN_DIR / "candidate_route_decision.csv"
NEXT_PROBE_QUEUE = RUN_DIR / "next_probe_queue.csv"
FINAL_DECISION = RUN_DIR / "final_source_policy_decision_report.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_json(path: Path) -> Mapping[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig")) if path_exists(path) else {}


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if bom else "utf-8"), bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def feature_set_source_policy(asof_rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, str]]] = {}
    for row in asof_rows:
        grouped.setdefault(str(row.get("feature_set_id", "")), []).append(row)
    policies: dict[str, dict[str, Any]] = {}
    for feature_set, rows in grouped.items():
        blocked = [row for row in rows if str(row.get("usable_for_forward_pass_fail", "")).lower() == "false"]
        policies[feature_set] = {
            "feature_set_id": feature_set,
            "source_policy_rows": len(rows),
            "forward_block_row_count": len(blocked),
            "blocked_symbols": ";".join(sorted({str(row.get("required_symbol", "")) for row in blocked})),
            "source_policy_status": "forward_source_blocked" if blocked else "source_policy_clean",
        }
    policies.setdefault(
        "us100_technical42_no_external",
        {
            "feature_set_id": "us100_technical42_no_external",
            "source_policy_rows": 0,
            "forward_block_row_count": 0,
            "blocked_symbols": "",
            "source_policy_status": "source_policy_clean_no_external_sources",
        },
    )
    return policies


def stress_breakpoint(attempt_name: str, cost_rows: Sequence[Mapping[str, str]]) -> str:
    rows = [row for row in cost_rows if row.get("attempt_name") == attempt_name]
    positive = [row for row in rows if number(row.get("net_profit")) > 0.0 and number(row.get("profit_factor"), math.nan) >= 1.1]
    if not positive:
        return "base_or_low_cost_fragile"
    return max(positive, key=lambda row: number(row.get("extra_round_trip_points"))).get("extra_round_trip_points", "")


def build_matrix() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    runtime = {row["attempt_name"]: row for row in read_csv(SOURCE_RUNTIME)}
    gap = {row["attempt_name"]: row for row in read_csv(SOURCE_GAP)}
    asof_rows = read_csv(SOURCE_ASOF)
    curve_rows = read_csv(SOURCE_CURVE)
    cost_rows = read_csv(SOURCE_COST)
    source_policy = feature_set_source_policy(asof_rows)
    matrix: list[dict[str, Any]] = []
    for curve in curve_rows:
        attempt = curve["attempt_name"]
        feature_set = curve["feature_set_id"]
        policy = source_policy.get(feature_set, {"source_policy_status": "source_policy_unknown", "forward_block_row_count": "", "blocked_symbols": ""})
        tester_gap_minutes = number(gap.get(attempt, {}).get("tester_to_feature_last_gap_minutes"))
        net = number(curve.get("net_profit"))
        pf = number(curve.get("profit_factor"), math.nan)
        cost_survives_to = stress_breakpoint(attempt, cost_rows)
        if tester_gap_minutes > 0:
            tester_status = "tester_current_day_gap_blocks_forward"
        else:
            tester_status = "tester_reaches_feature_last"
        if policy.get("source_policy_status", "").startswith("source_policy_clean") and net > 0 and math.isfinite(pf) and pf > 1.0:
            route = "source_clean_runtime_probe_only"
        elif policy.get("source_policy_status", "").startswith("forward_source_blocked"):
            route = "source_policy_repair_required"
        else:
            route = "runtime_or_source_repair_required"
        if attempt == "u42_plain_rf":
            route = "source_clean_cost_fragility_control"
        matrix.append(
            {
                "attempt_name": attempt,
                "feature_set_id": feature_set,
                "net_profit": curve.get("net_profit", ""),
                "profit_factor": curve.get("profit_factor", ""),
                "trade_count": curve.get("trade_count", ""),
                "max_closed_drawdown": curve.get("max_closed_drawdown", ""),
                "source_policy_status": policy.get("source_policy_status", ""),
                "source_block_row_count": policy.get("forward_block_row_count", ""),
                "blocked_symbols": policy.get("blocked_symbols", ""),
                "tester_status": tester_status,
                "tester_to_feature_last_gap_minutes": tester_gap_minutes,
                "cost_survives_to_extra_points_pf_ge_1_1": cost_survives_to,
                "route_decision": route,
                "forward_pass_fail_usable": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    tester_rows = [
        {
            "attempt_name": row.get("attempt_name", ""),
            "feature_set_id": row.get("feature_set_id", ""),
            "api_latest_us100_close_utc": row.get("api_latest_us100_close_utc", ""),
            "feature_last_timestamp": row.get("feature_last_timestamp", ""),
            "tester_last_observed_bar_time": row.get("tester_last_observed_bar_time", ""),
            "tester_to_feature_last_gap_minutes": row.get("tester_to_feature_last_gap_minutes", ""),
            "tester_to_api_latest_gap_minutes": row.get("tester_to_api_latest_gap_minutes", ""),
            "policy": "use_for_runtime_attribution_only_until_tester_reaches_feature_last",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in read_csv(SOURCE_GAP)
    ]
    route_rows = sorted(matrix, key=lambda row: (row["route_decision"], -number(row["net_profit"])))
    queue = [
        {
            "queue_id": "run337T_source_clean_u42_cost_fragility_control",
            "input_attempt": "u42_plain_rf",
            "task": "Use u42 as source-clean no-external control and test whether cost fragility alone invalidates the surface.",
            "forbidden": "do not retune threshold, lot, risk, or ONNX",
            "success_condition": "cost/curve remains acceptable under fixed settings and tester reaches feature last",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337T_m48_macro_asof_policy_repair",
            "input_attempt": "m48_plain_rf",
            "task": "Repair or explicitly bound macro as-of source policy before any forward pass/fail use.",
            "forbidden": "do not use macro lagged source rows as forward authority",
            "success_condition": "macro source policy rows become forward-usable or the attempt remains blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337T_tester_rollover_reprobe",
            "input_attempt": "all",
            "task": "Reprobe Strategy Tester after broker tester history can include the current feature tail.",
            "forbidden": "do not declare missing data solved from Python API alone",
            "success_condition": "tester_last_observed_bar_time reaches feature_last_timestamp",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return matrix, tester_rows, route_rows, queue


def gate_rows(matrix: Sequence[Mapping[str, Any]], tester_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source_clean = sum(1 for row in matrix if str(row.get("source_policy_status", "")).startswith("source_policy_clean"))
    source_blocked = len(matrix) - source_clean
    tester_blocked = sum(1 for row in tester_rows if number(row.get("tester_to_feature_last_gap_minutes")) > 0)
    return [
        {
            "gate_name": "source_policy_partition",
            "status": "covered",
            "evidence_path": rel(SOURCE_POLICY_MATRIX),
            "effect": f"source-clean rows(원천 깨끗한 행)={source_clean}, source-blocked rows(원천 차단 행)={source_blocked}로 분리했다.",
        },
        {
            "gate_name": "tester_visible_window_policy",
            "status": "covered_blocked",
            "evidence_path": rel(TESTER_WINDOW_POLICY),
            "effect": f"tester gap(테스터 공백)이 {tester_blocked}개라 전진 통과/실패 판정은 막아둔다.",
        },
        {
            "gate_name": "route_decision_no_selection",
            "status": "covered",
            "evidence_path": rel(CANDIDATE_ROUTE_DECISION),
            "effect": "u42는 source-clean control(원천 깨끗한 대조군), m48/core56은 source-policy repair(원천 정책 수리) 대상으로 분리했다.",
        },
        {
            "gate_name": "no_goal_achieve_claim",
            "status": "covered",
            "evidence_path": rel(DECISION_DOC),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def report_text(matrix: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage337S Source Policy Repair Decision(337S 원천 정책 수리 결정)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- decision(결정): `{DECISION}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- Forward Blocked(전진 차단): `current_run_boundary`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "| attempt(시도) | source policy(원천 정책) | tester(테스터) | cost survives(비용 생존) | route(경로) |",
        "|---|---|---|---:|---|",
    ]
    for row in matrix:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['source_policy_status']}` | `{row['tester_status']}` | `{row['cost_survives_to_extra_points_pf_ge_1_1']}` | `{row['route_decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Read(판독)",
            "",
            "m48_plain_rf(거시48 일반 RF)는 가장 좋은 runtime probe(런타임 탐침)지만 macro as-of policy(거시 시점 기준 정책)가 forward authority(전진 권위)를 막는다.",
            "u42_plain_rf(US100 기술42 일반 RF)는 외부 원천이 없어 source-clean control(원천 깨끗한 대조군)로 쓸 수 있지만, 비용 압박에서 PF(손익비)가 얇아진다.",
            "효과: 다음 run337T(337T 실행)는 새 후보 개발이 아니라 source-clean control(원천 깨끗한 대조군)과 tester rollover(테스터 이월) 조건을 분리해서 확인한다.",
        ]
    )
    return "\n".join(lines)


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def append_artifacts(paths: Sequence[Path]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    columns = list(rows[0].keys()) if rows else ["artifact_id", "artifact_type", "path", "artifact_path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"]
    generated = now_utc()
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def update_docs() -> list[Path]:
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_clean_control(원천 깨끗한 대조군): `u42_plain_rf`
- source_policy_repair_required(원천 정책 수리 필요): `m48_plain_rf;c56_plain_rf`
- tester_boundary_required(테스터 경계 필요): `tester must reach feature_last`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): source policy(원천 정책), tester boundary(테스터 경계), cost fragility(비용 취약성)를 분리했고 선택 후보는 만들지 않는다.
"""
    write_text(SELECTED_STATUS, selection, True)
    changed = [SELECTED_STATUS]
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
        focus = (
            "- >-\n"
            f"  Stage337 run337S focus complete: Stage337(337단계) run337S(337S 실행)는 `{STATUS}`로 source policy repair decision(원천 정책 수리 결정)을 완료했다. "
            "Effect(효과): u42는 source-clean control(원천 깨끗한 대조군), m48/core56은 source-policy repair(원천 정책 수리), 전체는 tester boundary(테스터 경계) 필요로 분리했다."
        )
        if "Stage337 run337S focus complete" not in text:
            text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
        write_text(WORKSPACE_STATE, text, bom)
        changed.append(WORKSPACE_STATE)
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        block = f"""## Stage337 run337S(337S 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): u42 source-clean control(원천 깨끗한 대조군), m48/core56 source-policy repair(원천 정책 수리), tester rollover(테스터 이월) 조건을 분리했다. Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        if "## Stage337 run337S(337S 실행)" not in text:
            text = text.rstrip() + "\n\n" + block
        write_text(CURRENT_STATE, text, bom)
        changed.append(CURRENT_STATE)
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337S(337S 실행) `{STATUS}`. Effect(효과): source policy/tester boundary/cost fragility(원천 정책/테스터 경계/비용 취약성)를 분리했고 Forward/Goal(전진/목표) 주장은 없음."
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
        write_text(CHANGELOG, text, bom)
        changed.append(CHANGELOG)
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    matrix, tester_rows, route_rows, queue_rows = build_matrix()
    gates = gate_rows(matrix, tester_rows)
    artifacts = [
        write_csv(SOURCE_POLICY_MATRIX, list(matrix[0].keys()) if matrix else ["attempt_name"], matrix),
        write_csv(TESTER_WINDOW_POLICY, list(tester_rows[0].keys()) if tester_rows else ["attempt_name"], tester_rows),
        write_csv(CANDIDATE_ROUTE_DECISION, list(route_rows[0].keys()) if route_rows else ["attempt_name"], route_rows),
        write_csv(NEXT_PROBE_QUEUE, list(queue_rows[0].keys()), queue_rows),
        write_csv(GATE_AUDIT, ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(
            FINAL_DECISION,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_clean_control": "u42_plain_rf",
                "source_policy_repair_required": ["m48_plain_rf", "c56_plain_rf"],
                "tester_boundary_required": "tester_last_observed_bar_time must reach feature_last_timestamp",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "forward_blocked": "current_run_boundary",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "artifacts": [], "claim_boundary": CLAIM_BOUNDARY}),
        write_text(REPORT_PATH, report_text(matrix), True),
        write_text(
            DECISION_DOC,
            f"""# Stage337S Decision(337S 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): u42_plain_rf는 source-clean control(원천 깨끗한 대조군)로, m48_plain_rf/c56_plain_rf는 source-policy repair(원천 정책 수리) 대상으로, 전체는 tester boundary(테스터 경계) 재확인 대상으로 분리했다.
""",
            True,
        ),
    ]
    artifacts.extend(update_docs())
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "source_policy_repair_decision", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT_PATH), "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed."},
    )
    upsert_csv(
        STAGE_LEDGER,
        ["run_key"],
        {
            "run_key": f"{RUN_ID}__source_policy_repair_decision",
            "ledger_row_id": f"{RUN_ID}__source_policy_repair_decision",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "source_policy_repair_decision",
            "work_family": "data_integrity_runtime_parity_decision",
            "question": "which tester-visible attempts are source-clean controls versus source-policy repair targets",
            "metric_scope": "source_policy_tester_boundary_cost_fragility_no_forward_decision",
            "evidence_scope": "run337Q/run337R reports",
            "kpi_scope": "diagnostic_blocked_forward",
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "primary_artifact": rel(REPORT_PATH),
            "path": rel(REPORT_PATH),
            "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "decision": DECISION,
        },
    )
    artifacts.extend([RUN_REGISTRY, STAGE_LEDGER])
    artifacts.append(append_artifacts(artifacts))
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "artifacts": [rel(path) for path in artifacts], "claim_boundary": CLAIM_BOUNDARY})
    print(json.dumps({"status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "matrix_rows": len(matrix), "next_action": NEXT_RUN_ID, "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
