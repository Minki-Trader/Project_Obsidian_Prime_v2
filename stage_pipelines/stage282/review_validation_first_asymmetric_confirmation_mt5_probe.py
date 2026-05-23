from __future__ import annotations

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
from stage_pipelines.stage280.validate_directional_mapping_stability import (  # noqa: E402
    attribution_rows,
    drawdown_stats,
    quality_summary,
    safe_float,
    trade_frame,
)
from stage_pipelines.stage281.review_drawdown_normalized_directional_mt5_probe import resolve_report_path  # noqa: E402


STAGE282_ID = "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild"
STAGE283_ID = "283_onnx_candidate_campaign__adapter_package_for_cp282d_macro_trend_countercheck"
RUN_ID = "run282C_review_validation_first_asymmetric_confirmation_mt5_probe_v1"
SOURCE_RUN_ID = "run282B_validation_first_asymmetric_confirmation_mt5_probe_v1"
STATUS = "completed_validation_first_probe_review_candidate_selected_stage283_opened"
JUDGMENT = "cp282D_selected_for_adapter_package_no_onnx_readiness"
SELECTED_CANDIDATE = "cp282D_macro_trend_countercheck_surface"
SELECTED_BRANCH = "run282A_cp282D_macro_trend_countercheck"
NEXT_ACTION = "run283A_build_adapter_package_for_cp282d_macro_trend_countercheck"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE282 = ROOT / "stages" / STAGE282_ID
RUN282A = STAGE282 / "02_runs" / "run282A"
RUN282B = STAGE282 / "02_runs" / "run282B"
RUN_DIR = STAGE282 / "02_runs" / "run282C"
REVIEWS282 = STAGE282 / "03_reviews"
SELECTED282 = STAGE282 / "04_selected" / "selection_status.md"
REVIEW_INDEX282 = REVIEWS282 / "review_index.md"
STAGE_LEDGER282 = REVIEWS282 / "stage_run_ledger.csv"

SOURCE_BRANCH_QUEUE = RUN282A / "branch_design_queue.csv"
SOURCE_MANIFEST = RUN282A / "candidate_payload_manifest.csv"
SOURCE_EXECUTION = RUN282B / "execution_result.json"
SOURCE_KPI = RUN282B / "mt5_kpi_summary.csv"
SOURCE_RUN_MANIFEST = RUN282B / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage282/review_validation_first_asymmetric_confirmation_mt5_probe.py")

SCOREBOARD = RUN_DIR / "stability_scoreboard.csv"
MONTHLY = RUN_DIR / "monthly_attribution.csv"
SESSION = RUN_DIR / "session_attribution.csv"
TRADE_QUALITY = RUN_DIR / "trade_quality_summary.csv"
CURVE = RUN_DIR / "curve_stability_summary.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
SELECTED_PACKAGE = RUN_DIR / "selected_candidate_package.json"
RECEIPT = RUN_DIR / "candidate_selection_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS282 / "run282C_candidate_selection_stage283_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage282_candidate_selected_stage283_adapter_package_open.md"

STAGE283 = ROOT / "stages" / STAGE283_ID
SPEC283 = STAGE283 / "00_spec" / "stage_brief.md"
INPUTS283 = STAGE283 / "01_inputs"
REVIEWS283 = STAGE283 / "03_reviews"
SELECTED283 = STAGE283 / "04_selected" / "selection_status.md"
STAGE_LEDGER283 = REVIEWS283 / "stage_run_ledger.csv"
REVIEW_INDEX283 = REVIEWS283 / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "validation_net_profit",
    "validation_pf",
    "validation_trade_count",
    "validation_dd",
    "validation_recovery",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_dd",
    "oos_recovery",
    "tier_b_validation_net_profit",
    "tier_b_validation_pf",
    "tier_b_oos_net_profit",
    "validation_positive_month_share",
    "oos_positive_month_share",
    "validation_worst_month_net",
    "oos_worst_month_net",
    "validation_worst_session_net",
    "oos_worst_session_net",
    "validation_max_losing_streak",
    "oos_max_losing_streak",
    "validation_top_10pct_contribution_share",
    "oos_top_10pct_contribution_share",
    "review_label",
    "failure_reasons",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
ATTRIBUTION_COLUMNS = (
    "materialized_branch_id",
    "seed_role",
    "tier_scope",
    "split",
    "bucket",
    "net_profit",
    "trade_count",
    "win_rate",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "share_of_positive_net",
    "source_report_path",
)
TRADE_QUALITY_COLUMNS = (
    "materialized_branch_id",
    "seed_role",
    "tier_scope",
    "split",
    "trade_count",
    "net_profit",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "win_rate",
    "expectancy",
    "average_win",
    "average_loss",
    "largest_win",
    "largest_loss",
    "max_losing_streak_count",
    "max_losing_streak_loss",
    "top_trade_contribution_share",
    "top_10pct_contribution_share",
    "source_report_path",
)
CURVE_COLUMNS = (
    "materialized_branch_id",
    "seed_role",
    "tier_scope",
    "split",
    "start_balance",
    "end_balance",
    "net_profit",
    "max_drawdown",
    "max_drawdown_percent",
    "recovery_factor",
    "new_high_count",
    "underwater_trade_count",
    "source_report_path",
)
FAILURE_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "failure_type",
    "failure_reasons",
    "salvage_value",
    "reopen_condition",
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


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def sha256_file(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def load_json(path: Path) -> dict[str, Any]:
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


def attempt_role_key(tier_scope: str, attempt_role: str) -> str:
    if tier_scope == "Tier A+B" or attempt_role == "actual_routed_total":
        return "actual_routed"
    if tier_scope == "Tier A":
        return "tier_a"
    if tier_scope == "Tier B":
        return "tier_b"
    return str(tier_scope).lower().replace(" ", "_")


def parse_kpi_records() -> dict[tuple[str, str, str], dict[str, Any]]:
    execution = load_json(SOURCE_EXECUTION)
    attempt_meta = {
        str(item.get("attempt_name", "")): dict(item)
        for item in execution.get("execution_results", [])
        if item.get("attempt_name")
    }
    records: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in read_csv_dicts(SOURCE_KPI):
        report = json.loads(row.get("report") or "{}")
        metrics = json.loads(row.get("metrics") or "{}")
        attempt_name = str(report.get("attempt_name", ""))
        meta = attempt_meta.get(attempt_name, {})
        materialized_id = str(meta.get("materialized_branch_id", attempt_name))
        tier_scope = str(row.get("tier_scope", meta.get("tier", "")))
        split = str(row.get("split", meta.get("split", "")))
        role = attempt_role_key(tier_scope, str(row.get("route_role", meta.get("attempt_role", ""))))
        records[(materialized_id, role, split)] = {
            "tier_scope": tier_scope,
            "route_role": row.get("route_role", meta.get("attempt_role", "")),
            "split": split,
            "metrics": metrics,
            "report_path": resolve_report_path(str(metrics.get("report_path", "")), report),
        }
    return records


def metric(records: Mapping[tuple[str, str, str], Mapping[str, Any]], materialized_id: str, role: str, split: str, key: str) -> float:
    entry = records.get((materialized_id, role, split), {})
    metrics = entry.get("metrics", {}) if isinstance(entry, Mapping) else {}
    return safe_float(metrics.get(key))


def bucket_values(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str) -> list[float]:
    return [
        safe_float(row.get("net_profit"))
        for row in rows
        if row.get("materialized_branch_id") == materialized_id
        and row.get("tier_scope") == tier_scope
        and row.get("split") == split
    ]


def positive_bucket_share(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str) -> float:
    values = bucket_values(rows, materialized_id, tier_scope, split)
    return sum(1 for value in values if value > 0) / len(values) if values else 0.0


def worst_bucket_net(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str) -> float:
    values = bucket_values(rows, materialized_id, tier_scope, split)
    return min(values) if values else 0.0


def quality_value(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str, key: str) -> float:
    for row in rows:
        if row.get("materialized_branch_id") == materialized_id and row.get("tier_scope") == tier_scope and row.get("split") == split:
            return safe_float(row.get(key))
    return 0.0


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    branch_rows = read_csv_dicts(SOURCE_BRANCH_QUEUE)
    branch_by_id = {row["materialized_branch_id"]: row for row in branch_rows}
    records = parse_kpi_records()
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    for branch in branch_rows:
        materialized_id = branch["materialized_branch_id"]
        package_id = branch["package_id"]
        for role, tier_scope in (("actual_routed", "Tier A+B"), ("tier_a", "Tier A"), ("tier_b", "Tier B")):
            for split in ("validation_is", "oos"):
                entry = records.get((materialized_id, role, split))
                if not entry:
                    continue
                report_path = Path(str(entry.get("report_path", "")))
                frame = trade_frame(report_path)
                monthly_rows.extend(
                    attribution_rows(frame, materialized_id=materialized_id, seed_role=package_id, tier_scope=tier_scope, split=split, source_report_path=report_path, bucket_column="month")
                )
                session_rows.extend(
                    attribution_rows(frame, materialized_id=materialized_id, seed_role=package_id, tier_scope=tier_scope, split=split, source_report_path=report_path, bucket_column="session")
                )
                q = quality_summary(frame)
                quality_rows.append({"materialized_branch_id": materialized_id, "seed_role": package_id, "tier_scope": tier_scope, "split": split, **q, "source_report_path": report_path.as_posix()})
                profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
                curve_rows.append({"materialized_branch_id": materialized_id, "seed_role": package_id, "tier_scope": tier_scope, "split": split, **drawdown_stats(profits), "source_report_path": report_path.as_posix()})

    scoreboard_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    selected_row: dict[str, Any] = {}
    for materialized_id, branch in branch_by_id.items():
        package_id = branch["package_id"]
        validation_net = metric(records, materialized_id, "actual_routed", "validation_is", "net_profit")
        validation_pf = metric(records, materialized_id, "actual_routed", "validation_is", "profit_factor")
        validation_trades = int(metric(records, materialized_id, "actual_routed", "validation_is", "trade_count"))
        validation_dd = metric(records, materialized_id, "actual_routed", "validation_is", "max_drawdown_amount")
        validation_recovery = metric(records, materialized_id, "actual_routed", "validation_is", "recovery_factor")
        oos_net = metric(records, materialized_id, "actual_routed", "oos", "net_profit")
        oos_pf = metric(records, materialized_id, "actual_routed", "oos", "profit_factor")
        oos_trades = int(metric(records, materialized_id, "actual_routed", "oos", "trade_count"))
        oos_dd = metric(records, materialized_id, "actual_routed", "oos", "max_drawdown_amount")
        oos_recovery = metric(records, materialized_id, "actual_routed", "oos", "recovery_factor")
        tier_b_validation_net = metric(records, materialized_id, "tier_b", "validation_is", "net_profit")
        tier_b_validation_pf = metric(records, materialized_id, "tier_b", "validation_is", "profit_factor")
        tier_b_oos_net = metric(records, materialized_id, "tier_b", "oos", "net_profit")
        validation_positive_month_share = positive_bucket_share(monthly_rows, materialized_id, "Tier A+B", "validation_is")
        oos_positive_month_share = positive_bucket_share(monthly_rows, materialized_id, "Tier A+B", "oos")
        validation_worst_month = worst_bucket_net(monthly_rows, materialized_id, "Tier A+B", "validation_is")
        oos_worst_month = worst_bucket_net(monthly_rows, materialized_id, "Tier A+B", "oos")
        validation_worst_session = worst_bucket_net(session_rows, materialized_id, "Tier A+B", "validation_is")
        oos_worst_session = worst_bucket_net(session_rows, materialized_id, "Tier A+B", "oos")
        validation_streak = int(quality_value(quality_rows, materialized_id, "Tier A+B", "validation_is", "max_losing_streak_count"))
        oos_streak = int(quality_value(quality_rows, materialized_id, "Tier A+B", "oos", "max_losing_streak_count"))
        validation_top10 = quality_value(quality_rows, materialized_id, "Tier A+B", "validation_is", "top_10pct_contribution_share")
        oos_top10 = quality_value(quality_rows, materialized_id, "Tier A+B", "oos", "top_10pct_contribution_share")
        reasons: list[str] = []
        if validation_net < 50:
            reasons.append("validation_net_below_50")
        if validation_pf < 1.20:
            reasons.append("validation_pf_below_1_20")
        if validation_recovery < 0.45:
            reasons.append("validation_recovery_below_0_45")
        if validation_trades < 70:
            reasons.append("validation_trade_count_below_70")
        if oos_net < 150 or oos_pf < 1.40 or oos_recovery < 1.50 or oos_trades < 70:
            reasons.append("oos_guardrail_below_floor")
        if tier_b_validation_net <= 0 or tier_b_validation_pf < 1.10:
            reasons.append("tier_b_validation_below_floor")
        if validation_positive_month_share < 0.65:
            reasons.append("validation_positive_month_share_below_0_65")
        if validation_worst_month < -100 or validation_worst_session < -80:
            reasons.append("weak_month_or_session_too_deep")
        if validation_streak > 11:
            reasons.append("validation_losing_streak_above_11")
        if validation_top10 > 2.50:
            reasons.append("validation_top10_concentration_above_2_50")
        label = "selected_for_adapter_package_no_onnx_readiness" if not reasons and materialized_id == SELECTED_BRANCH else "failed_or_watch_not_selected"
        selected_candidate = SELECTED_CANDIDATE if label.startswith("selected") else "none"
        row = {
            "materialized_branch_id": materialized_id,
            "package_id": package_id,
            "validation_net_profit": validation_net,
            "validation_pf": validation_pf,
            "validation_trade_count": validation_trades,
            "validation_dd": validation_dd,
            "validation_recovery": validation_recovery,
            "oos_net_profit": oos_net,
            "oos_pf": oos_pf,
            "oos_trade_count": oos_trades,
            "oos_dd": oos_dd,
            "oos_recovery": oos_recovery,
            "tier_b_validation_net_profit": tier_b_validation_net,
            "tier_b_validation_pf": tier_b_validation_pf,
            "tier_b_oos_net_profit": tier_b_oos_net,
            "validation_positive_month_share": validation_positive_month_share,
            "oos_positive_month_share": oos_positive_month_share,
            "validation_worst_month_net": validation_worst_month,
            "oos_worst_month_net": oos_worst_month,
            "validation_worst_session_net": validation_worst_session,
            "oos_worst_session_net": oos_worst_session,
            "validation_max_losing_streak": validation_streak,
            "oos_max_losing_streak": oos_streak,
            "validation_top_10pct_contribution_share": validation_top10,
            "oos_top_10pct_contribution_share": oos_top10,
            "review_label": label,
            "failure_reasons": ";".join(reasons),
            "selected_candidate": selected_candidate,
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        scoreboard_rows.append(row)
        if selected_candidate != "none":
            selected_row = row
        else:
            failure_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "package_id": package_id,
                    "failure_type": label,
                    "failure_reasons": ";".join(reasons),
                    "salvage_value": "failure memory only; do not carry as candidate",
                    "reopen_condition": "Only reopen if a new thesis changes feature/decision/risk surface.",
                    "claim_boundary": BOUNDARY,
                }
            )
    if not selected_row:
        raise RuntimeError("No selected candidate row met the Stage282 criteria.")
    return scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows, selected_row


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


def stage283_spec_markdown(selected_row: Mapping[str, Any]) -> str:
    return f"""# Stage283 Brief(283단계 개요): Adapter Package for cp282D(cp282D 어댑터 패키지)

- canonical_stage_id(정식 단계 ID): `{STAGE283_ID}`
- single_question(단일 질문): `{SELECTED_CANDIDATE}`를 Adapter package(어댑터 패키지)로 추적 가능하게 묶을 수 있는가?
- source_stage(원천 단계): `{STAGE282_ID}`
- source_run(원천 실행): `{RUN_ID}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- Adapter package(어댑터 패키지): `pending`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Candidate Evidence(후보 근거)

- validation_net_profit(검증 순수익): `{safe_float(selected_row['validation_net_profit']):.2f}`
- validation_pf(검증 수익 팩터): `{safe_float(selected_row['validation_pf']):.2f}`
- validation_recovery(검증 회복): `{safe_float(selected_row['validation_recovery']):.2f}`
- oos_net_profit(표본외 순수익): `{safe_float(selected_row['oos_net_profit']):.2f}`
- oos_pf(표본외 수익 팩터): `{safe_float(selected_row['oos_pf']):.2f}`
- oos_recovery(표본외 회복): `{safe_float(selected_row['oos_recovery']):.2f}`

Effect(효과): Stage283(283단계)는 운영 승격이 아니라 feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), runtime handoff(런타임 인계)를 Adapter package(어댑터 패키지)로 고정한다.

`{BOUNDARY}`
"""


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], selected_row: Mapping[str, Any]) -> str:
    lines = [
        "# run282C Report(282C 보고서): Candidate Selection for Adapter Package(어댑터 패키지용 후보 선택)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`",
        "- Adapter package(어댑터 패키지): `pending`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Scoreboard(점수판)",
        "",
        "| branch(분기) | val net(검증 순수익) | val PF(검증 수익 팩터) | val recovery(검증 회복) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | label(라벨) |",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {branch} | {vnet:.2f} | {vpf:.2f} | {vrec:.2f} | {onet:.2f} | {opf:.2f} | {label} |".format(
                branch=row["materialized_branch_id"],
                vnet=safe_float(row["validation_net_profit"]),
                vpf=safe_float(row["validation_pf"]),
                vrec=safe_float(row["validation_recovery"]),
                onet=safe_float(row["oos_net_profit"]),
                opf=safe_float(row["oos_pf"]),
                label=row["review_label"],
            )
        )
    lines.extend(
        [
            "",
            "## Meaning(의미)",
            "",
            f"`{SELECTED_CANDIDATE}`는 선택 후보로 올라갔지만 Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 아직 아니다.",
            "Effect(효과): 다음 단계는 ONNX(온엑스) export(내보내기)가 아니라 Adapter package(어댑터 패키지) 추적성 고정이다.",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def write_stage283_inputs(selected_row: Mapping[str, Any]) -> None:
    for path in (SPEC283.parent, INPUTS283, REVIEWS283, SELECTED283.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_md(SPEC283, stage283_spec_markdown(selected_row))
    write_csv(INPUTS283 / "stage282_selection_scoreboard.csv", SCOREBOARD_COLUMNS, read_csv_dicts(SCOREBOARD))
    write_json(INPUTS283 / "selected_candidate_package.json", json.loads(io_path(SELECTED_PACKAGE).read_text(encoding="utf-8-sig")))
    write_md(
        INPUTS283 / "input_refs.md",
        f"""# Stage283 Input References(283단계 입력 참조)

- source_report(원천 보고서): `{rel(REPORT)}`
- source_scoreboard(원천 점수판): `{rel(SCOREBOARD)}`
- selected_candidate_package(선택 후보 패키지): `{rel(INPUTS283 / 'selected_candidate_package.json')}`
- source_payload_manifest(원천 페이로드 목록): `{rel(SOURCE_MANIFEST)}`

Effect(효과): Stage283(283단계)는 선택 후보를 Adapter package(어댑터 패키지)로 묶는 데 필요한 원천과 해시를 추적한다.
""",
    )
    write_md(
        SELECTED283,
        f"""# Stage283 Selection Status(283단계 선택 상태)

- stage_status(단계 상태): `opened_adapter_package_for_selected_candidate`
- current_packet(현재 작업 묶음): `stage283_adapter_package_for_cp282d_macro_trend_countercheck_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE282_ID}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `pending`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUTS283 / 'input_refs.md')}`
""",
    )
    write_md(
        REVIEW_INDEX283,
        f"""# Stage283 Review Index(283단계 검토 색인)

- stage_brief(단계 개요): `{rel(SPEC283)}`
- input_refs(입력 참조): `{rel(INPUTS283 / 'input_refs.md')}`
""",
    )
    write_csv(
        STAGE_LEDGER283,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage283_open",
                "stage_id": STAGE283_ID,
                "run_id": RUN_ID,
                "view": "stage283_open_adapter_package",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stage_open",
                "status": "opened_adapter_package_pending",
                "judgment": JUDGMENT,
                "evidence_boundary": "selected_candidate_no_adapter_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"selected_candidate={SELECTED_CANDIDATE};next_action={NEXT_ACTION}.",
            }
        ],
    )


def write_outputs(
    scoreboard_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    quality_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    selected_row: Mapping[str, Any],
    created_at: str,
) -> list[Path]:
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(TRADE_QUALITY, TRADE_QUALITY_COLUMNS, quality_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    selected_package = {
        "selected_candidate": SELECTED_CANDIDATE,
        "selected_branch": SELECTED_BRANCH,
        "stage_id": STAGE282_ID,
        "run_id": RUN_ID,
        "feature_surface": ["route_signal_value"],
        "model_or_scoring_surface": "single discrete route signal table for runtime probe",
        "decision_surface": "q03 can replace q02 only when local trend and macro countercheck agree.",
        "risk_logic": "OOS upside is preserved only if validation-like pressure is reduced first.",
        "adapter_path": "Stage283 must package feature order, route diagnostics, decision/risk receipts, and runtime handoff.",
        "runtime_handoff": "MT5 replay completed for Tier A used, Tier B fallback stress, and actual routed total.",
        "scoreboard_row": dict(selected_row),
        "adapter_package": "pending",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }
    write_json(SELECTED_PACKAGE, selected_package)
    write_json(
        RECEIPT,
        {
            "run_id": RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "selected_candidate": SELECTED_CANDIDATE,
            "selected_branch": SELECTED_BRANCH,
            "branch_count": len(scoreboard_rows),
            "failure_rows": len(failure_rows),
            "monthly_rows": len(monthly_rows),
            "session_rows": len(session_rows),
            "trade_quality_rows": len(quality_rows),
            "curve_rows": len(curve_rows),
            "adapter_package": "pending",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "judgment": JUDGMENT,
            "next_action": NEXT_ACTION,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"selected_candidate={SELECTED_CANDIDATE};branches={len(scoreboard_rows)};monthly_rows={len(monthly_rows)};session_rows={len(session_rows)};trade_quality_rows={len(quality_rows)}",
                "evidence_missing": "Adapter package;ONNX parity;MT5 ONNX runtime reproduction",
                "judgment_label": JUDGMENT,
                "judgment_class": "selected_candidate_for_adapter_package",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "후보는 선택됐지만 어댑터와 온엑스 준비는 아직 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "candidate_package_identity(후보 패키지 정체성)",
                "status": "passed",
                "evidence_path": rel(SELECTED_PACKAGE),
                "effect": "후보명, 피처 표면, 판단 표면, 위험 로직, 런타임 인계를 함께 묶는다.",
            },
            {
                "gate_name": "stability_review_passed_for_adapter(어댑터 전 안정성 검토 통과)",
                "status": "passed",
                "evidence_path": rel(SCOREBOARD),
                "effect": "검증과 표본외가 모두 어댑터 패키지로 넘길 만큼 버텼는지 확인한다.",
            },
            {
                "gate_name": "no_onnx_claim(온엑스 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "어댑터 패키지 전에는 온엑스 준비를 주장하지 않는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, selected_row))
    write_md(
        DECISION,
        f"""# Decision(결정): Stage282 Candidate Selected and Stage283 Open(282단계 후보 선택과 283단계 개방)

- date(날짜): `{UPDATED_ON}`
- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`
- decision(결정): Stage282(282단계)는 `{SELECTED_CANDIDATE}`를 Adapter package(어댑터 패키지) 대상으로 선택하고 Stage283(283단계)를 연다.
- effect(효과): ONNX(온엑스)로 바로 가지 않고 feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), runtime handoff(런타임 인계)를 패키지로 고정한다.
- source(원천): `{rel(REPORT)}`
- Adapter package(어댑터 패키지): `pending`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_stage283_inputs(selected_row)
    artifacts = [
        SCOREBOARD,
        MONTHLY,
        SESSION,
        TRADE_QUALITY,
        CURVE,
        FAILURE_MEMORY,
        SELECTED_PACKAGE,
        RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
        SPEC283,
        INPUTS283 / "stage282_selection_scoreboard.csv",
        INPUTS283 / "selected_candidate_package.json",
        INPUTS283 / "input_refs.md",
        SELECTED283,
        STAGE_LEDGER283,
        REVIEW_INDEX283,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE282_ID,
            "target_stage_id": STAGE283_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": created_at,
            "selected_candidate": SELECTED_CANDIDATE,
            "adapter_package": "pending",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
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
            "source_inputs": [rel(SOURCE_BRANCH_QUEUE), rel(SOURCE_MANIFEST), rel(SOURCE_EXECUTION), rel(SOURCE_KPI), rel(SOURCE_RUN_MANIFEST), rel(ROOT / PRODUCER)],
            "source_hashes": {
                rel(path): sha256_file(path)
                for path in [SOURCE_BRANCH_QUEUE, SOURCE_MANIFEST, SOURCE_EXECUTION, SOURCE_KPI, SOURCE_RUN_MANIFEST, ROOT / PRODUCER]
                if path_exists(path)
            },
            "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
            "lineage_judgment": "connected_with_boundary_selected_candidate_no_adapter_no_onnx",
        },
    )
    artifacts.append(LINEAGE)
    return artifacts


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE282_ID,
                "lane": "candidate_selection_for_adapter_package",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"selected_candidate={SELECTED_CANDIDATE};target_stage={STAGE283_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__candidate_selection",
                "stage_id": STAGE282_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage282_candidate_selection_stage283_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "stage282_candidate_selection(282단계 후보 선택)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "monthly_session_curve_trade_quality_selected_candidate_no_onnx",
                "scoreboard_lane": "candidate_selection",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"selected_candidate={SELECTED_CANDIDATE};failure_rows={len(failure_rows)}",
                "guardrail_kpi": "adapter_package=pending;onnx_readiness=not_claimed",
                "external_verification_status": "mt5_trade_reports_parsed",
                "notes": f"target_stage={STAGE283_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    write_csv(
        STAGE_LEDGER282,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage282_closeout",
                "stage_id": STAGE282_ID,
                "run_id": RUN_ID,
                "view": "stage282_candidate_selection_stage283_open",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stability_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "selected_candidate_no_adapter_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"selected_candidate={SELECTED_CANDIDATE};target_stage={STAGE283_ID}.",
            }
        ],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage282_candidate_selection_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE282_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run282C candidate selection(282C 후보 선택)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED282).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- selected_candidate(선택 후보):", f"- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`")
    selected = replace_line_prefix(selected, "- Adapter package(어댑터 패키지):", "- Adapter package(어댑터 패키지): `pending`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run282C_report", f"- run282C_report(282C 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage283_open", f"- stage283_open(283단계 개방): `{STAGE283_ID}`")
    write_md(SELECTED282, selected)

    review_index = io_path(REVIEW_INDEX282).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX282) else "# Stage282 Review Index(282단계 검토 색인)\n"
    review_index = append_once(review_index, "run282C_report", f"- run282C_report(282C 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX282, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage283_adapter_package_for_cp282d_macro_trend_countercheck_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE283_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE282_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `adapter_package_for_cp282d_macro_trend_countercheck`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", f"- adapter_under_review(검토 중 어댑터): `{SELECTED_CANDIDATE}`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_adapter_package_for_selected_candidate`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run282C_summary",
        f"- run282C_summary(282C 요약): `{SELECTED_CANDIDATE}`를 Adapter package(어댑터 패키지) 대상으로 선택하고 Stage283(283단계)를 열었다. Effect(효과): 후보는 생겼지만 Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 아직 없다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE283_ID}")
    focus = (
        f"- >-\n"
        f"  Stage283(283단계) Adapter package(어댑터 패키지) opened for selected candidate(선택 후보) `{SELECTED_CANDIDATE}` by `{RUN_ID}`. "
        f"Effect(효과): ONNX(온엑스) 전에 feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), runtime handoff(런타임 인계)를 고정한다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run282C Candidate selection(282C 후보 선택)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): `{SELECTED_CANDIDATE}`를 Adapter package(어댑터 패키지) 대상으로 선택하고 Stage283(283단계)를 열었다.\n- boundary(경계): Adapter package(어댑터 패키지)는 `pending`, ONNX readiness(온엑스 준비)와 Goal Achieve(목표 달성)는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST283-ADAPTER-PACKAGE-CP282D",
        f"| `IDEA-ST283-ADAPTER-PACKAGE-CP282D` | `{STAGE283_ID}` | Adapter package(어댑터 패키지) for `{SELECTED_CANDIDATE}` | `Tier A used + Tier B fallback stress + actual routed total` | `opened_adapter_package_pending` | 선택 후보를 온엑스 전 추적 가능 패키지로 고정한다. |",
    )
    write_md(IDEA_REGISTER, idea)


def main() -> None:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS282).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows, selected_row = build_outputs()
    artifacts = write_outputs(scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows, selected_row, created_at)
    update_registers_and_docs(created_at, artifacts, scoreboard_rows, failure_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "selected_candidate": SELECTED_CANDIDATE,
                "adapter_package": "pending",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "branch_count": len(scoreboard_rows),
                "failure_memory_count": len(failure_rows),
                "monthly_rows": len(monthly_rows),
                "session_rows": len(session_rows),
                "trade_quality_rows": len(quality_rows),
                "curve_rows": len(curve_rows),
                "target_stage": STAGE283_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
