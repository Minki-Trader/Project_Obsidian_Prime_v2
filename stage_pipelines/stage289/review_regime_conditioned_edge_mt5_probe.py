from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


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
    write_csv_rows,
)
from stage_pipelines.stage280.validate_directional_mapping_stability import safe_float, trade_frame  # noqa: E402


STAGE289_ID = "289_onnx_candidate_campaign__regime_conditioned_edge_surface_rebuild"
STAGE290_ID = "290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild"
RUN_ID = "run289C_review_regime_conditioned_edge_mt5_probe_v1"
SOURCE_RUN_ID = "run289B_regime_conditioned_edge_mt5_probe_v1"
STATUS = "completed_regime_conditioned_edge_review_no_candidate_stage290_opened"
JUDGMENT = "regime_conditioned_filtering_did_not_create_positive_edge_no_adapter_no_onnx"
NEXT_ACTION = "run290A_design_payoff_weighted_edge_model_rebuild_packet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE289 = ROOT / "stages" / STAGE289_ID
RUN289A = STAGE289 / "02_runs" / "run289A"
RUN289B = STAGE289 / "02_runs" / "run289B"
RUN_DIR = STAGE289 / "02_runs" / "run289C"
REVIEWS289 = STAGE289 / "03_reviews"
SELECTED289 = STAGE289 / "04_selected" / "selection_status.md"
REVIEW_INDEX289 = REVIEWS289 / "review_index.md"
STAGE_LEDGER289 = REVIEWS289 / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN289A / "candidate_payload_manifest.csv"
SOURCE_KPI = RUN289B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN289B / "execution_result.json"
SOURCE_RUN_MANIFEST = RUN289B / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage289/review_regime_conditioned_edge_mt5_probe.py")

SCOREBOARD = RUN_DIR / "regime_conditioned_edge_scoreboard.csv"
MONTHLY = RUN_DIR / "monthly_attribution.csv"
SESSION = RUN_DIR / "session_attribution.csv"
LOCAL_POCKETS = RUN_DIR / "local_curve_pocket_diagnostics.csv"
CURVE = RUN_DIR / "curve_stability_summary.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
STAGE290_QUEUE = RUN_DIR / "stage290_payoff_weighted_edge_seed_queue.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS289 / "run289C_regime_conditioned_edge_review_stage290_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage289_regime_conditioned_edge_review_stage290_open.md"

STAGE290 = ROOT / "stages" / STAGE290_ID
SPEC290 = STAGE290 / "00_spec" / "stage_brief.md"
INPUTS290 = STAGE290 / "01_inputs"
REVIEWS290 = STAGE290 / "03_reviews"
SELECTED290 = STAGE290 / "04_selected" / "selection_status.md"
STAGE_LEDGER290 = REVIEWS290 / "stage_run_ledger.csv"
REVIEW_INDEX290 = REVIEWS290 / "review_index.md"
INPUT_REFS290 = INPUTS290 / "input_refs.md"
QUEUE290 = INPUTS290 / "stage290_payoff_weighted_edge_seed_queue.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "validation_net_profit",
    "validation_pf",
    "validation_trade_count",
    "validation_trades_per_day",
    "validation_dd",
    "validation_recovery",
    "validation_expectancy",
    "validation_positive_month_share",
    "validation_worst_month_net",
    "validation_worst_session_net",
    "validation_worst_rolling_20_net",
    "validation_worst_rolling_50_net",
    "validation_underwater_ratio",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_trades_per_day",
    "oos_dd",
    "oos_recovery",
    "oos_expectancy",
    "oos_positive_month_share",
    "oos_worst_month_net",
    "oos_worst_session_net",
    "oos_worst_rolling_20_net",
    "oos_worst_rolling_50_net",
    "oos_underwater_ratio",
    "density_gate",
    "profit_scale_gate",
    "efficiency_gate",
    "curve_quality_gate",
    "review_label",
    "failure_reasons",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
ATTRIBUTION_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "split",
    "bucket_type",
    "bucket",
    "trade_count",
    "net_profit",
    "profit_factor",
    "positive_bucket",
    "source_report_path",
)
CURVE_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "split",
    "trade_count",
    "final_net",
    "max_equity_peak",
    "min_equity",
    "underwater_ratio",
    "source_report_path",
)
POCKET_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "split",
    "rolling_window",
    "worst_rolling_net",
    "pocket_threshold",
    "pocket_label",
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
QUEUE_COLUMNS = (
    "seed_id",
    "source_materialized_branch_id",
    "source_package_id",
    "seed_role",
    "fresh_stage290_question",
    "required_change",
    "forbidden_repair_loop",
    "prior_stage_refs",
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    existing = read_csv_dicts(path)
    new_keys = {str(row.get(key, "")).strip() for row in rows}
    merged = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, columns, merged)


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


def parse_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    text = str(value or "").strip()
    if not text:
        return {}
    return dict(ast.literal_eval(text))


def manifest_by_id() -> dict[str, dict[str, str]]:
    return {row["materialized_branch_id"]: row for row in read_csv_dicts(SOURCE_MANIFEST)}


def parse_records() -> dict[tuple[str, str], dict[str, Any]]:
    records: dict[tuple[str, str], dict[str, Any]] = {}
    known_ids = sorted(manifest_by_id(), key=len, reverse=True)
    for row in read_csv_dicts(SOURCE_KPI):
        if row.get("route_role") != "actual_routed_total":
            continue
        metrics = parse_obj(row.get("metrics"))
        report = parse_obj(row.get("report"))
        attempt_name = str(report.get("attempt_name") or row.get("record_view") or "")
        materialized_id = next((item for item in known_ids if item in attempt_name), "")
        if not materialized_id:
            continue
        records[(materialized_id, str(row.get("split", "")))] = {
            "metrics": metrics,
            "report_path": Path(str(metrics.get("report_path", ""))),
        }
    return records


def profit_factor(values: Sequence[float]) -> float:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = sum(value for value in values if value < 0)
    return gross_profit / abs(gross_loss) if gross_loss < 0 else 0.0


def rolling_min(values: Sequence[float], window: int) -> float:
    if len(values) < window:
        return 0.0
    return float(pd.Series([float(value) for value in values]).rolling(window).sum().min())


def split_days(split: str) -> int:
    return 183 if split == "validation_is" else 131


def attribution_rows(frame: pd.DataFrame, materialized_id: str, package_id: str, split: str, bucket_type: str, bucket_column: str, report_path: Path) -> list[dict[str, Any]]:
    if frame.empty or bucket_column not in frame.columns:
        return []
    rows: list[dict[str, Any]] = []
    for bucket, group in frame.groupby(bucket_column, sort=True):
        profits = [float(value) for value in group["net_profit"].tolist()]
        net = sum(profits)
        rows.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "split": split,
                "bucket_type": bucket_type,
                "bucket": str(bucket),
                "trade_count": len(profits),
                "net_profit": net,
                "profit_factor": profit_factor(profits),
                "positive_bucket": "yes" if net > 0 else "no",
                "source_report_path": report_path.as_posix(),
            }
        )
    return rows


def curve_outputs(report_path: Path, materialized_id: str, package_id: str, split: str) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    frame = trade_frame(report_path)
    profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
    balance = 0.0
    peak = 0.0
    min_equity = 0.0
    underwater = 0
    for profit in profits:
        balance += profit
        peak = max(peak, balance)
        min_equity = min(min_equity, balance)
        if balance < peak:
            underwater += 1
    curve = {
        "materialized_branch_id": materialized_id,
        "package_id": package_id,
        "split": split,
        "trade_count": len(profits),
        "final_net": balance,
        "max_equity_peak": peak,
        "min_equity": min_equity,
        "underwater_ratio": underwater / len(profits) if profits else 0.0,
        "source_report_path": report_path.as_posix(),
    }
    pockets = []
    for window, threshold in ((20, -120.0), (50, -150.0)):
        worst = rolling_min(profits, window)
        pockets.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "split": split,
                "rolling_window": window,
                "worst_rolling_net": worst,
                "pocket_threshold": threshold,
                "pocket_label": "deep_local_pocket" if worst < threshold else "tolerable",
                "source_report_path": report_path.as_posix(),
            }
        )
    monthly = attribution_rows(frame, materialized_id, package_id, split, "month", "month", report_path)
    session = attribution_rows(frame, materialized_id, package_id, split, "session", "session", report_path)
    return curve, pockets, monthly, session


def positive_share(rows: Sequence[Mapping[str, Any]]) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if float(row["net_profit"]) > 0) / len(rows)


def min_net(rows: Sequence[Mapping[str, Any]]) -> float:
    if not rows:
        return 0.0
    return min(float(row["net_profit"]) for row in rows)


def salvage_value(materialized_id: str, scoreboard: Mapping[str, Any]) -> str:
    if materialized_id.endswith("cp289D_trend_macro_all_hold4"):
        return "OOS recovery clue(표본외 회복 단서) but validation edge absent(검증 엣지 부재)"
    if materialized_id.endswith("cp289E_cash_non_extreme_hold6"):
        return "density supply clue(밀도 공급 단서) but profit scale absent(수익 규모 부재)"
    if float(scoreboard["oos_net_profit"]) > 0:
        return "OOS small positive clue(표본외 소폭 양수 단서) only"
    return "failure memory(실패 기억)"


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = manifest_by_id()
    records = parse_records()
    scoreboard_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for materialized_id, manifest_row in manifest.items():
        package_id = manifest_row["package_id"]
        data: dict[str, dict[str, Any]] = {}
        for split in ("validation_is", "oos"):
            entry = records.get((materialized_id, split), {})
            metrics = entry.get("metrics", {})
            report_path = Path(str(entry.get("report_path", "")))
            curve, pockets, monthly, session = curve_outputs(report_path, materialized_id, package_id, split)
            monthly_rows.extend(monthly)
            session_rows.extend(session)
            curve_rows.append(curve)
            pocket_rows.extend(pockets)
            data[split] = {
                "net": safe_float(metrics.get("net_profit")),
                "pf": safe_float(metrics.get("profit_factor")),
                "trades": safe_float(metrics.get("trade_count")),
                "tpd": safe_float(metrics.get("trade_count")) / split_days(split),
                "dd": safe_float(metrics.get("max_drawdown_amount")),
                "recovery": safe_float(metrics.get("recovery_factor")),
                "expectancy": safe_float(metrics.get("expectancy")),
                "positive_month_share": positive_share(monthly),
                "worst_month_net": min_net(monthly),
                "worst_session_net": min_net(session),
                "r20": next(row["worst_rolling_net"] for row in pockets if row["rolling_window"] == 20),
                "r50": next(row["worst_rolling_net"] for row in pockets if row["rolling_window"] == 50),
                "underwater_ratio": curve["underwater_ratio"],
            }
        density_ok = 4.0 <= data["validation_is"]["tpd"] <= 10.0 and 4.0 <= data["oos"]["tpd"] <= 10.0
        profit_ok = data["validation_is"]["net"] > 150.0 and data["oos"]["net"] > 250.0
        efficiency_ok = (
            data["validation_is"]["pf"] >= 1.10
            and data["oos"]["pf"] >= 1.10
            and data["validation_is"]["recovery"] >= 1.0
            and data["oos"]["recovery"] >= 1.0
            and data["validation_is"]["expectancy"] > 0.0
            and data["oos"]["expectancy"] > 0.0
        )
        curve_ok = (
            data["validation_is"]["positive_month_share"] >= 0.60
            and data["oos"]["positive_month_share"] >= 0.60
            and data["validation_is"]["worst_month_net"] >= -90.0
            and data["oos"]["worst_month_net"] >= -90.0
            and data["validation_is"]["worst_session_net"] >= -120.0
            and data["oos"]["worst_session_net"] >= -120.0
            and data["validation_is"]["r20"] >= -120.0
            and data["oos"]["r20"] >= -120.0
            and data["validation_is"]["r50"] >= -150.0
            and data["oos"]["r50"] >= -150.0
            and data["validation_is"]["underwater_ratio"] <= 0.90
            and data["oos"]["underwater_ratio"] <= 0.90
        )
        reasons: list[str] = []
        if not density_ok:
            reasons.append("trade_density_outside_4_10")
        if not profit_ok:
            reasons.append("profit_scale_not_both_splits")
        if not efficiency_ok:
            reasons.append("efficiency_pf_recovery_expectancy_not_jointly_credible")
        if not curve_ok:
            reasons.append("curve_quality_month_session_or_local_pocket_fail")
        label = "adapter_candidate_ready" if not reasons else "regime_conditioned_edge_negative"
        scoreboard = {
            "materialized_branch_id": materialized_id,
            "package_id": package_id,
            "validation_net_profit": data["validation_is"]["net"],
            "validation_pf": data["validation_is"]["pf"],
            "validation_trade_count": data["validation_is"]["trades"],
            "validation_trades_per_day": data["validation_is"]["tpd"],
            "validation_dd": data["validation_is"]["dd"],
            "validation_recovery": data["validation_is"]["recovery"],
            "validation_expectancy": data["validation_is"]["expectancy"],
            "validation_positive_month_share": data["validation_is"]["positive_month_share"],
            "validation_worst_month_net": data["validation_is"]["worst_month_net"],
            "validation_worst_session_net": data["validation_is"]["worst_session_net"],
            "validation_worst_rolling_20_net": data["validation_is"]["r20"],
            "validation_worst_rolling_50_net": data["validation_is"]["r50"],
            "validation_underwater_ratio": data["validation_is"]["underwater_ratio"],
            "oos_net_profit": data["oos"]["net"],
            "oos_pf": data["oos"]["pf"],
            "oos_trade_count": data["oos"]["trades"],
            "oos_trades_per_day": data["oos"]["tpd"],
            "oos_dd": data["oos"]["dd"],
            "oos_recovery": data["oos"]["recovery"],
            "oos_expectancy": data["oos"]["expectancy"],
            "oos_positive_month_share": data["oos"]["positive_month_share"],
            "oos_worst_month_net": data["oos"]["worst_month_net"],
            "oos_worst_session_net": data["oos"]["worst_session_net"],
            "oos_worst_rolling_20_net": data["oos"]["r20"],
            "oos_worst_rolling_50_net": data["oos"]["r50"],
            "oos_underwater_ratio": data["oos"]["underwater_ratio"],
            "density_gate": "passed" if density_ok else "failed",
            "profit_scale_gate": "passed" if profit_ok else "failed",
            "efficiency_gate": "passed" if efficiency_ok else "failed",
            "curve_quality_gate": "passed" if curve_ok else "failed",
            "review_label": label,
            "failure_reasons": "|".join(reasons) if reasons else "none",
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        scoreboard_rows.append(scoreboard)
        if reasons:
            failure_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "package_id": package_id,
                    "failure_type": label,
                    "failure_reasons": "|".join(reasons),
                    "salvage_value": salvage_value(materialized_id, scoreboard),
                    "reopen_condition": "Only reopen through a fresh payoff-aware model surface, not more inherited-signal filtering.",
                    "claim_boundary": BOUNDARY,
                }
            )
    prior_refs = "|".join(
        [
            rel(SCOREBOARD),
            rel(LOCAL_POCKETS),
            rel(FAILURE_MEMORY),
            rel(ROOT / "stages/287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild/02_runs/run287C/density_scale_curve_pocket_scoreboard.csv"),
            rel(ROOT / "stages/288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild/02_runs/run288C/risk_reward_exit_scoreboard.csv"),
        ]
    )
    queue_rows = [
        {
            "seed_id": "stage290_payoff_weighted_new_model_surface",
            "source_materialized_branch_id": "stage289_all_branches",
            "source_package_id": "none",
            "seed_role": "fresh_model_rebuild_not_filter_repair",
            "fresh_stage290_question": "Can a payoff-weighted model surface create positive expectancy while preserving 4-10 trades/day?",
            "required_change": "new label/objective/model scoring surface using raw feature interactions and payoff weighting",
            "forbidden_repair_loop": "Do not keep filtering inherited cp287E route_signal variants.",
            "prior_stage_refs": prior_refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage290_direction_specific_session_model",
            "source_materialized_branch_id": "run289A_cp289D_trend_macro_all_hold4",
            "source_package_id": "cp289D_trend_macro_all_hold4_surface",
            "seed_role": "oos_recovery_clue_validation_absent",
            "fresh_stage290_question": "Can direction-specific session/regime models keep OOS recovery without losing validation?",
            "required_change": "separate long/short decision surfaces and session-aware calibration",
            "forbidden_repair_loop": "Do not only loosen cp289D density thresholds.",
            "prior_stage_refs": prior_refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage290_curve_smoothness_objective",
            "source_materialized_branch_id": "run289A_cp289E_cash_non_extreme_hold6",
            "source_package_id": "cp289E_cash_non_extreme_hold6_surface",
            "seed_role": "density_supply_clue_profit_absent",
            "fresh_stage290_question": "Can curve-smoothness penalty be part of candidate construction instead of post-hoc rejection?",
            "required_change": "score selection must penalize rolling pockets and weak month/session before MT5 packaging",
            "forbidden_repair_loop": "Do not only take the densest cash-session filter.",
            "prior_stage_refs": prior_refs,
            "claim_boundary": BOUNDARY,
        },
    ]
    return scoreboard_rows, monthly_rows, session_rows, curve_rows, pocket_rows, failure_rows, queue_rows


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        (
            f"- `{row['package_id']}`: validation(검증) net `{float(row['validation_net_profit']):.2f}`, "
            f"`{float(row['validation_trades_per_day']):.2f}` trades/day(일 거래), "
            f"OOS(표본외) net `{float(row['oos_net_profit']):.2f}`, `{float(row['oos_trades_per_day']):.2f}` trades/day(일 거래), "
            f"gates(게이트) `{row['density_gate']}/{row['profit_scale_gate']}/{row['efficiency_gate']}/{row['curve_quality_gate']}`."
        )
        for row in scoreboard_rows
    ]
    return f"""# run289C Regime Conditioned Edge Review(289C 국면 조건부 엣지 검토)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- stage290_seed_count(290단계 씨앗 수): `{len(queue_rows)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Scoreboard(점수판)

{chr(10).join(lines)}

## Decision(결정)

Stage289(289단계)는 density(거래 밀도)는 대체로 맞췄지만 validation(검증) net/PF(순수익/수익 팩터)가 후보로 볼 수준이 아니었다. Effect(효과): inherited route signal filtering(계승 신호 필터링)을 멈추고 Stage290(290단계)에서 payoff-weighted edge model(수익 가중 엣지 모델)을 새 논제로 연다.
"""


def stage290_brief(queue_rows: Sequence[Mapping[str, Any]]) -> str:
    return f"""# Stage290 Payoff Weighted Edge Model Rebuild(290단계 수익 가중 엣지 모델 재구성)

- canonical_stage_id(정식 단계 ID): `{STAGE290_ID}`
- big_question(큰 질문): inherited signal filtering(계승 신호 필터링)을 버리고 payoff-weighted model surface(수익 가중 모델 표면)로 4-10 trades/day(일 4-10거래), profit scale(수익 규모), PF/recovery/expectancy(수익 팩터/회복/기대값), smooth curve(매끈한 곡선)를 동시에 만들 수 있는가?
- source_stage(원천 단계): `{STAGE289_ID}`
- seed_count(씨앗 수): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): Stage289(289단계)의 신호 필터형 실패를 수리하지 않고, label/objective/model scoring surface(라벨/목적함수/모델 점수 표면)를 새로 만든다.
"""


def write_outputs(
    scoreboard_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    pocket_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    created_at: str,
) -> list[Path]:
    for path in (RUN_DIR, REVIEWS289, INPUTS290, REVIEWS290, SELECTED290.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(LOCAL_POCKETS, POCKET_COLUMNS, pocket_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(STAGE290_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_csv(QUEUE290, QUEUE_COLUMNS, queue_rows)
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"{rel(SCOREBOARD)};{rel(MONTHLY)};{rel(SESSION)};{rel(CURVE)};{rel(LOCAL_POCKETS)};{rel(FAILURE_MEMORY)}",
                "evidence_missing": "selected candidate;Adapter package;ONNX export;ONNX parity;MT5 runtime reproduction for selected package",
                "judgment_label": JUDGMENT,
                "judgment_class": "negative_for_candidate_selection_but_seeded_next_stage(후보 선택은 부정, 다음 단계 씨앗 있음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "거래수는 맞췄지만 수익 엣지가 약해 후보가 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {"gate_name": "density_profit_efficiency_curve_joint_review(밀도/수익/효율/곡선 공동 검토)", "status": "passed", "evidence_path": rel(SCOREBOARD), "effect": "ONNX 후보 조건을 한 번에 판정했다."},
            {"gate_name": "fresh_stage_transition(새 단계 전환)", "status": "passed", "evidence_path": rel(STAGE290_QUEUE), "effect": "계승 신호 필터링 반복을 끊고 새 모델 표면으로 넘긴다."},
            {"gate_name": "no_adapter_no_onnx_claim(어댑터/온엑스 주장 없음)", "status": "passed", "evidence_path": rel(RESULT_JUDGMENT), "effect": "성과 부족 후보를 포장하지 않는다."},
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, queue_rows))
    write_md(SPEC290, stage290_brief(queue_rows))
    write_md(
        INPUT_REFS290,
        f"# Stage290 Input Refs(290단계 입력 참조)\n\n- `{rel(SCOREBOARD)}`\n- `{rel(MONTHLY)}`\n- `{rel(SESSION)}`\n- `{rel(CURVE)}`\n- `{rel(LOCAL_POCKETS)}`\n- `{rel(FAILURE_MEMORY)}`\n- `{rel(STAGE290_QUEUE)}`\n\nEffect(효과): Stage290(290단계)은 Stage289(289단계)의 density-pass/profit-fail(밀도 통과/수익 실패)을 새 payoff-weighted model(수익 가중 모델) 설계 입력으로 쓴다.\n",
    )
    write_csv(STAGE_LEDGER290, STAGE_LEDGER_COLUMNS, [{"row_id": "stage290_opened_from_run289C", "stage_id": STAGE290_ID, "run_id": RUN_ID, "view": "stage_open", "tier_scope": "not_applicable", "scoreboard": "stage290_seed_queue", "status": "opened_payoff_weighted_edge_model_rebuild", "judgment": "stage_opened_no_candidate", "evidence_boundary": "planning_from_stage289_failure_memory", "report_path": rel(REPORT), "notes": f"seed_count={len(queue_rows)};next_action={NEXT_ACTION}"}])
    write_md(REVIEW_INDEX290, f"# Stage290 Review Index(290단계 검토 색인)\n\n- input_refs(입력 참조): `{rel(INPUT_REFS290)}`\n- seed_queue(씨앗 대기열): `{rel(QUEUE290)}`\n")
    write_md(
        SELECTED290,
        f"""# Stage290 Selection Status(290단계 선택 상태)

- stage_status(단계 상태): `opened_payoff_weighted_edge_model_rebuild`
- current_packet(현재 작업 묶음): `stage290_payoff_weighted_edge_model_rebuild_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE289_ID}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUT_REFS290)}`
""",
    )
    write_md(
        DECISION,
        f"# Stage289 Closeout and Stage290 Open(289단계 종료와 290단계 개방)\n\n- decision_date(결정일): `{UPDATED_ON}`\n- source_run(원천 실행): `{RUN_ID}`\n- selected_candidate(선택 후보): `none`\n- reason(이유): regime filtering(국면 필터링)은 4-10 trades/day(일 4-10거래)를 맞췄지만 validation profit/efficiency(검증 수익/효율)를 만들지 못했다.\n- next_stage(다음 단계): `{STAGE290_ID}`\n- next_action(다음 행동): `{NEXT_ACTION}`\n\nEffect(효과): Adapter/ONNX(어댑터/온엑스)로 가지 않고 payoff-weighted model surface(수익 가중 모델 표면) 연구로 이동한다.\n",
    )
    final = [SCOREBOARD, MONTHLY, SESSION, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, STAGE290_QUEUE, QUEUE290, RESULT_JUDGMENT, GATE_AUDIT, REPORT, SPEC290, INPUT_REFS290, STAGE_LEDGER290, REVIEW_INDEX290, SELECTED290, DECISION]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE289_ID, "source_run_id": SOURCE_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "created_at_utc": created_at, "scoreboard_rows": len(scoreboard_rows), "failure_rows": len(failure_rows), "stage290_seed_count": len(queue_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final if path_exists(path)}, "claim_boundary": BOUNDARY})
    final.append(RUN_MANIFEST)
    write_json(LINEAGE, {"run_id": RUN_ID, "producer": PRODUCER.as_posix(), "source_artifacts": [rel(SOURCE_MANIFEST), rel(SOURCE_KPI), rel(SOURCE_EXECUTION), rel(SOURCE_RUN_MANIFEST)], "produced_artifacts": [rel(path) for path in final if path_exists(path)], "claim_boundary": BOUNDARY})
    final.append(LINEAGE)
    return [path for path in final if path_exists(path)]


def update_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE289_ID, "lane": "regime_conditioned_edge_review", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"scoreboard_rows={len(scoreboard_rows)};stage290_seed_count={len(queue_rows)};selected_candidate=none;next_action={NEXT_ACTION}"}], key="run_id")
    upsert_csv(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__review", "stage_id": STAGE289_ID, "run_id": RUN_ID, "subrun_id": "run289C", "parent_run_id": SOURCE_RUN_ID, "record_view": "regime_conditioned_edge_review(국면 조건부 엣지 검토)", "tier_scope": "Tier A used/Tier B fallback stress/actual routed total", "kpi_scope": "candidate_selection_review", "scoreboard_lane": "regime_conditioned_edge", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};stage290_seed_count={len(queue_rows)}", "guardrail_kpi": "selected_candidate=none;adapter=none;onnx=not_claimed", "external_verification_status": "completed_run289B_mt5_probe", "notes": "Stage289 closed with no candidate; Stage290 opened."}], key="ledger_row_id")
    upsert_csv(STAGE_LEDGER289, STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE289_ID, "run_id": RUN_ID, "view": "regime_conditioned_edge_review", "tier_scope": "Tier A used/Tier B fallback stress/actual routed total", "scoreboard": rel(SCOREBOARD), "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "no_candidate_no_adapter_no_onnx", "report_path": rel(REPORT), "notes": f"failure_rows={len(failure_rows)};stage290_seed_count={len(queue_rows)}."}], key="row_id")
    artifact_rows = [{"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage289_regime_conditioned_edge_review_artifact", "path": rel(path), "sha256": sha256_file_lf_normalized(path), "stage_id": STAGE289_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "run289C regime conditioned edge review(289C 국면 조건부 엣지 검토)"} for path in artifacts if path_exists(path)]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED289).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- selected_candidate(선택 후보):", "- selected_candidate(선택 후보): `none`")
    selected = replace_line_prefix(selected, "- Adapter package(어댑터 패키지):", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line_prefix(selected, "- ONNX readiness(온엑스 준비):", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run289C_report", f"- run289C_report(289C 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage290_open", f"- stage290_open(290단계 개방): `{STAGE290_ID}`")
    write_md(SELECTED289, selected)

    review_index = io_path(REVIEW_INDEX289).read_text(encoding="utf-8-sig")
    review_index = append_once(review_index, "run289C_report", f"- run289C_report(289C 보고서): `{rel(REPORT)}`\n- run289C_scoreboard(289C 점수판): `{rel(SCOREBOARD)}`\n- run289C_failure_memory(289C 실패 기억): `{rel(FAILURE_MEMORY)}`")
    write_md(REVIEW_INDEX289, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage290_payoff_weighted_edge_model_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE290_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE289_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run289C_summary", f"- run289C_summary(289C 요약): Stage289(289단계)는 4-10 trades/day(일 4-10거래) 밀도는 대체로 맞췄지만 validation profit/efficiency(검증 수익/효율)가 모두 약해 후보 없이 닫고 Stage290(290단계)을 열었다. Effect(효과): Adapter/ONNX(어댑터/온엑스)는 진행하지 않고 payoff-weighted edge model(수익 가중 엣지 모델)을 새 질문으로 넘긴다.")
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE290_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage289(289단계) run289C(289C 실행) regime-conditioned edge review(국면 조건부 엣지 검토) `{RUN_ID}` closed Stage289 and opened Stage290(290단계). Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 없고 next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(changelog, RUN_ID, f"## {UPDATED_ON} run289C Regime-conditioned edge review(289C 국면 조건부 엣지 검토)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): Stage289(289단계)는 selected candidate(선택 후보) 없이 닫고 Stage290(290단계)을 열었다.\n- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `not_claimed`다.\n")
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(idea, "IDEA-ST290-PAYOFF-WEIGHTED-EDGE-MODEL", f"| `IDEA-ST290-PAYOFF-WEIGHTED-EDGE-MODEL` | `{STAGE290_ID}` | payoff-weighted edge model rebuild(수익 가중 엣지 모델 재구성) | `Tier A used + Tier B fallback stress + actual routed total` | `opened` | Stage289(289단계)의 density-pass/profit-fail(밀도 통과/수익 실패) 이후 inherited signal filtering(계승 신호 필터링)을 버리고 새 label/objective/model surface(라벨/목적함수/모델 표면)를 만든다. |")
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(negative, "NEG-ST289-REGIME-CONDITIONED-EDGE", f"| `NEG-ST289-REGIME-CONDITIONED-EDGE` | `{STAGE289_ID}` | `{RUN_ID}` | regime-conditioned inherited signal filtering failed(국면 조건부 계승 신호 필터링 실패) | validation net/PF/recovery(검증 순수익/수익 팩터/회복)가 후보 기준 미달 | reopen only with payoff-weighted fresh model surface(수익 가중 새 모델 표면으로만 재개) |")
    write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    created_at = utc_now()
    outputs = build_outputs()
    scoreboard_rows, monthly_rows, session_rows, curve_rows, pocket_rows, failure_rows, queue_rows = outputs
    artifacts = write_outputs(scoreboard_rows, monthly_rows, session_rows, curve_rows, pocket_rows, failure_rows, queue_rows, created_at)
    update_docs(created_at, artifacts, scoreboard_rows, failure_rows, queue_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "scoreboard_rows": len(scoreboard_rows),
                "failure_rows": len(failure_rows),
                "stage290_seed_count": len(queue_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
