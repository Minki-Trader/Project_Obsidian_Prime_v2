from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337V"
RUN_ID = "run337V_cost_buffer_rebuild_and_source_policy_repair_design_v1"
PARENT_RUN_ID = "run337U_source_clean_cost_buffer_rebuild_or_tester_rollover_reprobe_v1"
NEXT_RUN_ID = "run337W_materialize_cost_buffer_source_policy_repair_inputs_v1"
STATUS = "completed_stage337V_cost_buffer_source_policy_repair_design_no_training_no_selection"
JUDGMENT = "cost_buffer_and_source_policy_repair_design_ready_but_no_onnx_or_forward_decision"
DECISION = "stage337V_open_run337W_materialize_cost_buffer_source_policy_repair_inputs_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337V_design_no_model_training_no_threshold_retuning_no_lot_optimization_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
REPORT_PATH = REVIEWS_DIR / "run337V_cost_buffer_source_policy_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337V_cost_buffer_source_policy_repair_design.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

RUN337R_DIR = STAGE_DIR / "02_runs" / "run337R"
RUN337T_DIR = STAGE_DIR / "02_runs" / "run337T"
RUN337U_DIR = STAGE_DIR / "02_runs" / "run337U"

RUN337R_CURVE = RUN337R_DIR / "curve_pocket_report.csv"
RUN337R_COST = RUN337R_DIR / "cost_stress_report.csv"
RUN337R_DB = RUN337R_DIR / "db_attribution_report.csv"
RUN337R_REGIME = RUN337R_DIR / "regime_attribution_report.csv"
RUN337T_COST = RUN337T_DIR / "u42_cost_stress_detail.csv"
RUN337T_SLICES = RUN337T_DIR / "u42_slice_cost_breakpoint.csv"
RUN337T_DECISION = RUN337T_DIR / "final_u42_source_clean_cost_fragility_decision.json"
RUN337U_DECISION = RUN337U_DIR / "final_tester_rollover_reprobe_decision.json"
RUN337U_GAP = RUN337U_DIR / "tester_rollover_feature_last_gap.csv"

FAILURE_DIGEST_CSV = RUN_DIR / "run337V_failure_memory_digest.csv"
SOURCE_POLICY_MATRIX_CSV = RUN_DIR / "source_policy_repair_matrix.csv"
COST_BUFFER_MATRIX_CSV = RUN_DIR / "cost_buffer_rebuild_hypothesis_matrix.csv"
OVERFIT_GATE_CSV = RUN_DIR / "overfit_parity_gate_contract.csv"
ECONOMIC_SOURCE_CSV = RUN_DIR / "economic_regime_source_policy_contract.csv"
RUN337W_QUEUE_CSV = RUN_DIR / "run337W_materialization_queue.csv"
REQUIRED_GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
EXPERIMENT_RECEIPT_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_JSON = RUN_DIR / "model_validation_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_run337V_cost_buffer_source_policy_design_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def safe_float(value: Any, default: float = math.nan) -> float:
    try:
        text = str(value).strip()
        if not text:
            return default
        number = float(text)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def safe_int(value: Any, default: int = 0) -> int:
    number = safe_float(value, math.nan)
    return default if math.isnan(number) else int(number)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def insert_focus(text: str, body: str, token: str) -> str:
    if token in text:
        return text
    return text.replace("current_focus:\n", f"current_focus:\n{body}\n", 1)


def append_section_once(path: Path, heading_token: str, section: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if heading_token in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + section.strip() + "\n", had_bom)


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def append_artifact_rows(paths: Sequence[Path], generated_at: str) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    existing = {row.get("artifact_id", "") for row in rows}
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_id = f"{RUN_ID}::{rel(path)}"
        if artifact_id in existing:
            rows = [row for row in rows if row.get("artifact_id") != artifact_id]
        suffix = path.suffix.lower().lstrip(".") or "file"
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": suffix,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if suffix in {"csv", "json", "md", "txt", "py"} else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at,
                "notes": STATUS,
                "artifact_path": rel(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def cost_lookup(rows: Sequence[Mapping[str, str]], attempt: str, extra_points: float) -> Mapping[str, str]:
    for row in rows:
        if row.get("attempt_name") == attempt and abs(safe_float(row.get("extra_round_trip_points")) - extra_points) < 1e-9:
            return row
    return {}


def build_failure_digest() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    curve_rows = read_csv(RUN337R_CURVE)
    r_cost_rows = read_csv(RUN337R_COST)
    t_cost_rows = read_csv(RUN337T_COST)
    u_gap_rows = read_csv(RUN337U_GAP)
    t_slices = read_csv(RUN337T_SLICES)
    u_decision = read_json(RUN337U_DECISION)
    t_decision = read_json(RUN337T_DECISION)

    candidate_attempts = ["m48_plain_rf", "c56_plain_rf", "u42_plain_rf"]
    digest: list[dict[str, Any]] = []
    for curve in curve_rows:
        attempt = curve.get("attempt_name", "")
        if attempt not in candidate_attempts:
            continue
        cost_rows = t_cost_rows if attempt == "u42_plain_rf" else r_cost_rows
        base = cost_lookup(cost_rows, attempt, 0)
        cost1 = cost_lookup(cost_rows, attempt, 1)
        cost5 = cost_lookup(cost_rows, attempt, 5)
        gap = next((row for row in u_gap_rows if row.get("attempt_name") == attempt), {}) if attempt == "u42_plain_rf" else {}
        source_policy = "source_clean_no_external" if attempt == "u42_plain_rf" else "source_policy_repair_required"
        repair_priority = "cost_buffer_control_only" if attempt == "u42_plain_rf" else "repair_candidate_source_policy_first"
        if attempt == "m48_plain_rf":
            repair_priority = "highest_profit_clue_but_source_policy_blocked"
        if attempt == "c56_plain_rf":
            repair_priority = "low_trade_count_high_pf_clue_but_source_policy_blocked"
        digest.append(
            {
                "attempt_name": attempt,
                "feature_set_id": curve.get("feature_set_id", ""),
                "source_policy": source_policy,
                "repair_priority": repair_priority,
                "base_net_profit": safe_float(base.get("net_profit", curve.get("net_profit"))),
                "base_profit_factor": safe_float(base.get("profit_factor", curve.get("profit_factor"))),
                "base_trade_count": safe_int(curve.get("trade_count")),
                "cost_plus_1_net_profit": safe_float(cost1.get("net_profit")),
                "cost_plus_1_profit_factor": safe_float(cost1.get("profit_factor")),
                "cost_plus_5_net_profit": safe_float(cost5.get("net_profit")),
                "cost_plus_5_profit_factor": safe_float(cost5.get("profit_factor")),
                "worst_slice_axis": curve.get("worst_slice_axis", ""),
                "worst_slice_bucket": curve.get("worst_slice_bucket", ""),
                "worst_slice_net_profit": safe_float(curve.get("worst_slice_net_profit")),
                "tester_to_feature_last_gap_minutes": safe_float(gap.get("tester_to_feature_last_gap_minutes", curve.get("tester_to_feature_last_gap_minutes"))),
                "asof_forward_policy_blocked": curve.get("asof_forward_policy_blocked", source_policy != "source_clean_no_external"),
                "use_in_next_run": "design_input_only_no_selection",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    weak_slice_statuses = {"base_negative_pocket", "base_pf_thin", "cost_fragile_below_1_point"}
    metrics = {
        "u42_one_point_pf": safe_float(cost_lookup(t_cost_rows, "u42_plain_rf", 1).get("profit_factor")),
        "u42_five_point_net": safe_float(cost_lookup(t_cost_rows, "u42_plain_rf", 5).get("net_profit")),
        "u42_weak_slice_count": sum(1 for row in t_slices if row.get("slice_status") in weak_slice_statuses),
        "tester_reached_feature_last": u_decision.get("tester_reached_feature_last", 0),
        "tester_gap_total": u_decision.get("tester_gap_total", 0),
        "timestamp_aligned_parity": f"{u_decision.get('timestamp_aligned_signal_parity_matched_rows', 0)}/{u_decision.get('timestamp_aligned_signal_parity_total_rows', 0)}",
        "u42_route_decision": t_decision.get("route_decision", ""),
    }
    return digest, metrics


def build_source_policy_matrix() -> list[dict[str, Any]]:
    return [
        {
            "repair_id": "m48_asof_macro_source_policy_repair",
            "target_attempt": "m48_plain_rf",
            "feature_set_id": "macro48_no_equity_breadth_or_top3",
            "hypothesis": "macro48(거시48) 수익 단서는 as-of source policy(시점 기준 원천 정책)를 엄격히 고치면 재평가할 가치가 있다.",
            "changed_variable": "external macro source handoff, source age flags, missing-source skip policy",
            "fixed_variables": "label horizon, score threshold policy, lot/risk, MT5 runtime contract",
            "source_rule": "VIX/USD/rate source timestamp(원천 시각) <= US100 bar close(봉 종가) only; no future fill(미래 채움 금지)",
            "invalid_if": "macro value from after target bar, hidden forward fill, source close after US100 decision bar, proxy-only KPI claim",
            "required_evidence": "source_age_audit.csv; feature_label_boundary_audit.csv; proxy_expected_result.csv; mt5_runtime_probe_result.csv",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "repair_id": "c56_core_source_policy_repair",
            "target_attempt": "c56_plain_rf",
            "feature_set_id": "core56_no_top3_weight_features",
            "hypothesis": "core56(핵심56) 높은 PF(손익비) 단서는 source staleness(원천 지연)와 low trade count(낮은 거래수)를 분리해야 한다.",
            "changed_variable": "equity breadth/top source availability flags and session-aware as-of joins",
            "fixed_variables": "model family candidates not selected; threshold search forbidden before source audit",
            "source_rule": "cash-session equity source(현금장 주식 원천)는 사용 가능 시각과 결측 플래그를 함께 남긴다.",
            "invalid_if": "stale equity source is silently forward-filled, unavailable rows are converted into profitable filters",
            "required_evidence": "equity_source_availability.csv; stale_row_decision.csv; proxy_mt5_difference.csv; trade_density_report.csv",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "repair_id": "u42_source_clean_control_keepout",
            "target_attempt": "u42_plain_rf",
            "feature_set_id": "us100_technical42_no_external",
            "hypothesis": "u42(US100 기술42)는 source-clean control(원천 깨끗한 대조군)로 유용하지만 비용 버퍼가 얇아 ONNX-ready(온엑스 준비) 대상이 아니다.",
            "changed_variable": "none in source policy; use as negative/control read only",
            "fixed_variables": "all frozen u42 inputs and runtime settings",
            "source_rule": "no external source; only broker US100 M5 technical data",
            "invalid_if": "u42 is promoted because source is clean despite cost fragility",
            "required_evidence": "u42 cost stress and slice breakpoint remain attached as failure memory",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_cost_buffer_matrix() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "cost_margin_objective_pretraining",
            "branch_type": "defensive_rebuild",
            "hypothesis": "entry scores need wider cost margin(비용 여유) before threshold(임계값) can be trusted.",
            "forbidden_shortcut": "do not retune threshold on forward data; do not delete bad hours after seeing forward PnL",
            "predeclared_controls": "cost ladder +0,+0.5,+1,+2,+5,+10; PF and net must be reported at every point",
            "success_criteria": "base PF >= 1.20, +1 PF >= 1.10, +2 net > 0, +5 not catastrophic, trade count still useful",
            "failure_criteria": "u42-like +1 PF below 1.10 or +5 net negative with no offsetting curve repair",
            "next_materialization": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "direction_symmetry_rebuild",
            "branch_type": "defensive_plus_offensive",
            "hypothesis": "short-side pocket(숏 방향 포켓) must be fixed structurally rather than filtered after the fact.",
            "forbidden_shortcut": "do not disable shorts post-hoc unless side limitation is predeclared and separately validated",
            "predeclared_controls": "long attribution, short attribution, D source/B source/D+B attribution, side-specific DD",
            "success_criteria": "both long and short are non-catastrophic or a predeclared one-side model passes density and cost gates",
            "failure_criteria": "sell bucket remains negative like u42 sell net -59.08 without a source or label explanation",
            "next_materialization": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "curve_pocket_robustness_rebuild",
            "branch_type": "curve_quality",
            "hypothesis": "pretty curve(좋은 곡선)는 net profit(순익)이 아니라 worst pocket(최악 포켓)과 underwater stretch(수중 구간) 통제로 만들어진다.",
            "forbidden_shortcut": "do not remove Monday/Tuesday/hour pockets as filters after observing forward losses",
            "predeclared_controls": "worst month, weekday, hour, session, ADX, volatility, chronological third, rolling pocket",
            "success_criteria": "no single pocket breaks the curve while headline net is positive; recovery factor improves without density collapse",
            "failure_criteria": "u42-like Monday, Tuesday, sell, ADX 20-25 pockets remain negative",
            "next_materialization": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "aggressive_density_preserving_rebuild",
            "branch_type": "offensive_probe",
            "hypothesis": "higher trade supply(거래 공급)를 유지하면서 cost buffer(비용 버퍼)를 넓히는 architecture(구조)를 탐색한다.",
            "forbidden_shortcut": "do not improve PF by starving trades; density must be measured",
            "predeclared_controls": "trades/day, no_tier rows, signal rate, fill rate, skip reasons, MT5 order attempts/fills",
            "success_criteria": "trade count remains useful and cost/curve gates do not collapse",
            "failure_criteria": "good PF with too few trades or proxy-only signal improvement",
            "next_materialization": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_overfit_gate_contract() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "no_forward_threshold_search",
            "required_check": "threshold, D/B rule, lot, ATR SL/TP must be fixed before forward/runtime probe",
            "evidence_path": "threshold_identity_audit.csv",
            "blocks_claim": "candidate_selection;Forward Passed;runtime_authority",
            "effect": "forward data(전진 데이터)로 다시 맞춘 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_vs_mt5_row_level_difference",
            "required_check": "proxy expected(프록시 예상값) and MT5 runtime probe(런타임 탐침) counts must be compared timestamp-aligned",
            "evidence_path": "timestamp_aligned_proxy_mt5_difference.csv",
            "blocks_claim": "runtime usability;KPI authority",
            "effect": "proxy(프록시)를 KPI 권위로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "source_asof_boundary",
            "required_check": "all external sources must prove source timestamp <= decision bar close",
            "evidence_path": "source_age_and_availability_audit.csv",
            "blocks_claim": "forward pass/fail;model validation",
            "effect": "look-ahead bias(미래참조 편향)를 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "tester_feature_last_reach",
            "required_check": "Strategy Tester(전략 테스터) telemetry must reach feature_last or claim is downgraded",
            "evidence_path": "tester_feature_last_gap_report.csv",
            "blocks_claim": "Forward Passed;Forward Failed",
            "effect": "테스터가 실제 최신 구간을 보지 못한 결과를 전진 판정으로 쓰지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost_curve_direction_joint_gate",
            "required_check": "cost stress, curve pocket, long/short, and regime slices must all be reported",
            "evidence_path": "cost_curve_direction_joint_review.csv",
            "blocks_claim": "ONNX-ready;Goal Achieve",
            "effect": "순익 하나로 깨진 KPI를 덮지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_economic_source_contract() -> list[dict[str, Any]]:
    return [
        {"source_family": "VIX", "feature_role": "volatility regime(변동성 국면)", "asof_rule": "use only published/available value before US100 bar close", "missing_rule": "mark unavailable; do not future-fill", "stress_slice": "vix_regime", "claim_boundary": CLAIM_BOUNDARY},
        {"source_family": "USDX", "feature_role": "USD regime(달러 국면)", "asof_rule": "source timestamp must be <= decision timestamp", "missing_rule": "mark age bucket and skip if over max age", "stress_slice": "usd_regime", "claim_boundary": CLAIM_BOUNDARY},
        {"source_family": "US10YR", "feature_role": "rate regime(금리 국면)", "asof_rule": "rate value must be aligned to latest known point only", "missing_rule": "session-aware missing flag required", "stress_slice": "rate_regime", "claim_boundary": CLAIM_BOUNDARY},
        {"source_family": "mega-cap equities", "feature_role": "equity breadth(주식 폭)", "asof_rule": "cash-session timestamp must be explicit", "missing_rule": "no silent bridge over closed session", "stress_slice": "equity_source_age", "claim_boundary": CLAIM_BOUNDARY},
        {"source_family": "US100 broker M5", "feature_role": "technical42/source-clean control(기술42/원천 깨끗한 대조군)", "asof_rule": "bar close/open convention must match MT5 runtime", "missing_rule": "tester gap must be recorded", "stress_slice": "technical_control", "claim_boundary": CLAIM_BOUNDARY},
    ]


def build_run337w_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337W_01_source_policy_audits",
            "task": "materialize source age, availability, and feature-label boundary audits for m48/c56",
            "required_inputs": f"{rel(SOURCE_POLICY_MATRIX_CSV)};{rel(ECONOMIC_SOURCE_CSV)}",
            "required_outputs": "source_age_and_availability_audit.csv;feature_label_boundary_audit.csv;source_clean_repair_decision.csv",
            "blocked_if_missing": "external source timestamps or broker bar time convention unavailable",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337W_02_cost_buffer_branch_specs",
            "task": "materialize branch specs for cost margin, direction symmetry, curve pocket, and density preserving probes",
            "required_inputs": rel(COST_BUFFER_MATRIX_CSV),
            "required_outputs": "branch_spec_manifest.csv;cost_ladder_contract.csv;direction_curve_gate_template.csv",
            "blocked_if_missing": "predeclared cost/curve/direction criteria absent",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337W_03_proxy_mt5_usability_templates",
            "task": "materialize proxy expected value templates and MT5 runtime difference schema",
            "required_inputs": rel(OVERFIT_GATE_CSV),
            "required_outputs": "proxy_expected_template.csv;timestamp_aligned_proxy_mt5_difference_schema.csv;usability_decision_rule.csv",
            "blocked_if_missing": "row-level timestamp alignment cannot be specified",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337W_04_tester_boundary_repair_plan",
            "task": "materialize tester history repair or wait/reprobe rule after run337U gap remains",
            "required_inputs": rel(RUN337U_DECISION),
            "required_outputs": "tester_boundary_repair_plan.csv;tester_feature_last_reach_gate.csv",
            "blocked_if_missing": "MT5 tester still cannot reach feature_last and no repair/wait policy is recorded",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337W_05_model_validation_firewall",
            "task": "materialize model validation firewall before any new ONNX training is allowed",
            "required_inputs": f"{rel(COST_BUFFER_MATRIX_CSV)};{rel(OVERFIT_GATE_CSV)}",
            "required_outputs": "model_validation_firewall.csv;no_forward_threshold_search_contract.csv;wfo_split_plan.csv",
            "blocked_if_missing": "training starts before no-lookahead and threshold firewall exists",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_audit(rows_by_name: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    checks = [
        ("failure_memory_loaded", RUN337T_COST, rows_by_name["failure"], "u42 비용 취약성, run337R 귀속, run337U 테스터 gap(공백)을 설계 입력으로 연결했다."),
        ("source_policy_repair_predeclared", SOURCE_POLICY_MATRIX_CSV, rows_by_name["source"], "m48/c56 원천 정책 수리와 u42 대조군 사용 경계를 나눴다."),
        ("cost_buffer_branches_predeclared", COST_BUFFER_MATRIX_CSV, rows_by_name["cost"], "비용 버퍼, 방향 대칭, 곡선 포켓, 거래 밀도 축을 사전 선언했다."),
        ("overfit_parity_firewall_predeclared", OVERFIT_GATE_CSV, rows_by_name["overfit"], "forward threshold search(전진 임계값 탐색)와 proxy-only authority(프록시 단독 권위)를 막았다."),
        ("economic_source_policy_predeclared", ECONOMIC_SOURCE_CSV, rows_by_name["economic"], "VIX/USD/rate/equity/US100 원천의 시점 기준 규칙을 분리했다."),
        ("run337W_queue_materialized", RUN337W_QUEUE_CSV, rows_by_name["queue"], "다음 실행이 어떤 산출물을 만들어야 하는지 대기열로 고정했다."),
    ]
    return [
        {
            "gate_name": name,
            "status": "covered" if path_exists(path) and rows else "missing",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, path, rows, effect in checks
    ]


def build_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_RECEIPT_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "A usable ONNX(온엑스)는 cost buffer(비용 버퍼), source policy(원천 정책), proxy-MT5 parity(프록시-MT5 동등성), and curve pocket(곡선 포켓)을 동시에 통과해야 한다.",
                "decision_use": "run337W materialization queue and later training firewall only; no selection",
                "comparison_baseline": "run337R attribution, run337T u42 cost fragility, run337U tester rollover gap",
                "control_variables": "no model training, no forward threshold retune, no lot optimization, no post-hoc pocket filter",
                "changed_variables": "design contracts and materialization queue only",
                "sample_scope": "US100 M5 forward evidence after 2026-04-14, source-clean u42 control plus source-policy-blocked m48/c56 clues",
                "success_criteria": "run337W can materialize source audits, cost branch specs, proxy/MT5 templates, tester boundary plan, and model validation firewall",
                "failure_criteria": "any cost/source/parity/overfit/timestamps gate is absent",
                "invalid_conditions": "lookahead source joins, forward data threshold search, proxy-only KPI authority, tester gap hidden as pass/fail",
                "stop_conditions": "stop training if source or tester boundary cannot be audited",
                "evidence_plan": [rel(FAILURE_DIGEST_CSV), rel(SOURCE_POLICY_MATRIX_CSV), rel(COST_BUFFER_MATRIX_CSV), rel(OVERFIT_GATE_CSV), rel(RUN337W_QUEUE_CSV)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": [rel(RUN337R_CURVE), rel(RUN337T_COST), rel(RUN337U_DECISION)],
                "time_axis": "US100 M5 broker/runtime bar timestamps; external sources must prove source timestamp <= decision bar close",
                "sample_scope": "design only; no new bars, labels, training rows, or forward pass/fail sample created",
                "missing_or_duplicate_check": "deferred to run337W source_age_and_availability_audit.csv",
                "feature_label_boundary": "predeclared no-lookahead and no forward threshold search firewall",
                "split_boundary": "future WFO/OOS/forward boundaries must be materialized before training",
                "leakage_risk": "using run337R/T/U bad pockets as filters instead of constraints",
                "data_hash_or_identity": rel(REQUIRED_GATE_AUDIT_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            MODEL_VALIDATION_JSON,
            {
                "run_id": RUN_ID,
                "model_family": "future ONNX research branches only; no model trained in run337V",
                "target_and_label": "not created in this run; must be re-declared before training",
                "split_method": "future WFO/OOS/forward split plan required",
                "selection_metric": "none in this run; future metric must include cost, DD, curve pocket, density, parity",
                "secondary_metrics": "PF, trades/day, drawdown, recovery, expectancy, long/short, session/hour/month, volatility, ADX, VIX, USD, rate slices",
                "threshold_policy": "forward threshold search forbidden; threshold identity audit required",
                "overfit_risk": "post-hoc repair using observed forward weak pockets",
                "calibration_risk": "scores are ranking/control surface unless calibrated and proven",
                "comparison_baseline": "run337R/T/U failure memory, not a selected candidate",
                "validation_judgment": "exploratory_design",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": "future run337W/MT5 package; no Strategy Tester run in run337V",
                "shared_contract": "proxy expected and MT5 runtime probe must compare row counts and signal counts timestamp-aligned",
                "known_differences": "run337U tester did not reach feature_last; run337V records repair plan requirement",
                "parity_check": "contract only, external verification out_of_scope_by_claim for this design run",
                "runtime_claim_boundary": "research_only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "cost buffer and source policy repair design packet",
                "evidence_available": [rel(FAILURE_DIGEST_CSV), rel(SOURCE_POLICY_MATRIX_CSV), rel(COST_BUFFER_MATRIX_CSV), rel(RUN337W_QUEUE_CSV)],
                "evidence_missing": "no new ONNX, no MT5 run, no Forward Passed/Failed",
                "judgment_label": "exploratory",
                "claim_boundary": "design ready only; no model, no runtime authority, no Goal Achieve",
                "next_condition": "run337W must materialize required audits/templates before any training or MT5 probe claims",
                "user_explanation_hook": "이번 작업은 좋은 숫자를 고르는 게 아니라, 다음 수리가 과적합으로 새는 길을 막는 설계다.",
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [rel(RUN337R_CURVE), rel(RUN337T_COST), rel(RUN337U_DECISION)],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(FAILURE_DIGEST_CSV), rel(SOURCE_POLICY_MATRIX_CSV), rel(COST_BUFFER_MATRIX_CSV), rel(OVERFIT_GATE_CSV), rel(RUN337W_QUEUE_CSV)],
                "artifact_hashes": "registered in artifact_registry.csv",
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked design artifacts; local 02_runs evidence is ignored_with_manifest",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def write_report(metrics: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337V Cost Buffer Source Policy Repair Design(337V 비용 버퍼 원천 정책 수리 설계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Evidence Read(읽은 근거)

- u42 +1 point PF(u42 1포인트 추가 비용 손익비): `{metrics['u42_one_point_pf']}`
- u42 +5 point net(u42 5포인트 추가 비용 순익): `{metrics['u42_five_point_net']}`
- u42 weak slices(u42 약한 구간): `{metrics['u42_weak_slice_count']}`
- tester feature_last reach(테스터 피처 끝 도달): `{metrics['tester_reached_feature_last']}/{metrics['tester_gap_total']}`
- timestamp-aligned parity(시점 맞춤 동등성): `{metrics['timestamp_aligned_parity']}`

## Materialized Outputs(물질화 산출물)

- failure memory digest(실패 기억 요약): `{rel(FAILURE_DIGEST_CSV)}`
- source policy repair matrix(원천 정책 수리 행렬): `{rel(SOURCE_POLICY_MATRIX_CSV)}`
- cost buffer hypothesis matrix(비용 버퍼 가설 행렬): `{rel(COST_BUFFER_MATRIX_CSV)}`
- overfit/parity gate contract(과적합/동등성 게이트 계약): `{rel(OVERFIT_GATE_CSV)}`
- economic source contract(경제 원천 계약): `{rel(ECONOMIC_SOURCE_CSV)}`
- run337W queue(337W 대기열): `{rel(RUN337W_QUEUE_CSV)}`

## Read(판독)

run337V(337V 실행)는 새 ONNX(온엑스)를 만들지 않았다. 효과(effect, 효과)는 m48/c56의 source-policy repair(원천 정책 수리), u42의 source-clean failure memory(원천 깨끗한 실패 기억), tester boundary(테스터 경계), cost/curve/direction gate(비용/곡선/방향 게이트)를 다음 run337W(337W 실행)의 물질화 조건으로 묶는 것이다.

이 설계는 forward data(전진 데이터)로 임계값을 다시 맞추는 수리를 금지한다. 다음 실행은 proxy expected(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)의 차이를 반드시 같이 보고, 활용 가능성(usability, 활용성)을 별도 라벨로 판정해야 한다.
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(metrics: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337V Decision(337V 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337V(337V 실행)는 비용 버퍼(cost buffer, 비용 버퍼)와 원천 정책(source policy, 원천 정책)을 동시에 수리할 다음 물질화 대기열을 만들었다. u42는 비용 취약성 때문에 대조군으로만 남기고, m48/c56은 look-ahead bias(미래참조 편향) 없이 원천 정책을 증명해야 한다.

Smallest next condition(다음 최소 조건): run337W(337W 실행)에서 source age audit(원천 나이 감사), no-forward-threshold firewall(전진 임계값 탐색 방화벽), proxy-MT5 difference schema(프록시-MT5 차이 스키마), tester boundary repair plan(테스터 경계 수리 계획)을 실제 파일로 물질화한다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs() -> list[Path]:
    artifacts: list[Path] = []
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- u42_source_clean_control(원천 깨끗한 대조군): `kept_as_failure_memory_control_not_onnx_ready`
- source_policy_repair_required(원천 정책 수리 필요): `m48_plain_rf;c56_plain_rf`
- cost_buffer_rebuild_required(비용 버퍼 재구성 필요): `true`
- tester_boundary_required(테스터 경계 필요): `tester must reach feature_last before Forward Passed/Failed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337V는 비용 버퍼와 원천 정책을 동시에 수리할 run337W 물질화 대기열을 만들었고, 아직 모델 학습/선택/운영 주장은 없다.
"""
    artifacts.append(write_md(SELECTED_STATUS, selection_text))

    focus_line = (
        "- >-\n"
        f"  Stage337 run337V focus complete: Stage337(337단계) run337V(337V 실행)는 `{STATUS}`로 cost buffer/source policy repair design(비용 버퍼/원천 정책 수리 설계)을 완료했다. "
        "Effect(효과): u42 비용 취약성, run337U tester gap(테스터 공백), m48/c56 source-policy blocker(원천 정책 차단)를 run337W 물질화 게이트로 묶고 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
        text = insert_focus(text, focus_line, "Stage337 run337V focus complete")
        artifacts.append(write_text_lossless(WORKSPACE_STATE, text, had_bom))
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        entry = f"""
## Stage337 run337V(337V 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cost buffer(비용 버퍼), source policy(원천 정책), overfit/parity firewall(과적합/동등성 방화벽), tester boundary(테스터 경계)를 run337W 물질화 대기열로 고정했다.
"""
        if "## Stage337 run337V(337V 실행)" not in text:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        artifacts.append(write_text_lossless(CURRENT_STATE, text, had_bom))
    if path_exists(CHANGELOG):
        text, had_bom = read_text_lossless(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337V(337V 실행) `{STATUS}`. Effect(효과): 비용 버퍼/원천 정책 수리 설계를 만들고 run337W 물질화 대기열을 열었으며 Forward/Goal(전진/목표) 주장은 없음."
        if "Stage337 run337V(337V 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        artifacts.append(write_text_lossless(CHANGELOG, text, had_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], generated_at: str) -> list[Path]:
    paths = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design_model_validation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "family": "cost_buffer_source_policy_repair_design",
                "primary_report": rel(REPORT_PATH),
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "ledger_row_id": f"{RUN_ID}__cost_buffer_source_policy_repair_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_design_model_validation",
                "evidence_scope": "run337R attribution, run337T cost fragility, run337U tester boundary",
                "kpi_scope": "design_contract_no_new_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": DECISION,
                "run_key": f"{RUN_ID}__cost_buffer_source_policy_repair_design",
                "family": "cost_buffer_source_policy_repair_design",
                "question": "how to repair cost buffer and source policy without forward overfitting",
                "metric_scope": "design_only_no_forward_decision",
                "primary_artifact": rel(REPORT_PATH),
            },
        ),
        upsert_csv(
            ALPHA_LEDGER,
            ["ledger_row_id"],
            {
                "ledger_row_id": f"{RUN_ID}__design_packet",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "design_packet",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "cost_buffer_source_policy_design",
                "tier_scope": "out_of_scope_by_claim_design_no_tier_kpi",
                "kpi_scope": "no_new_kpi_design_contract",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": "not_applicable",
                "guardrail_kpi": "no_forward_threshold_search;proxy_mt5_required;source_asof_required",
                "external_verification_status": "out_of_scope_by_claim",
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
    ]
    paths.append(append_artifact_rows(artifact_paths, generated_at))
    return paths


def main() -> int:
    generated_at = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    failure_rows, metrics = build_failure_digest()
    source_rows = build_source_policy_matrix()
    cost_rows = build_cost_buffer_matrix()
    overfit_rows = build_overfit_gate_contract()
    economic_rows = build_economic_source_contract()
    queue_rows = build_run337w_queue()
    gate_rows = build_gate_audit(
        {
            "failure": failure_rows,
            "source": source_rows,
            "cost": cost_rows,
            "overfit": overfit_rows,
            "economic": economic_rows,
            "queue": queue_rows,
        }
    )

    artifact_paths: list[Path] = [
        write_csv(
            FAILURE_DIGEST_CSV,
            ["attempt_name", "feature_set_id", "source_policy", "repair_priority", "base_net_profit", "base_profit_factor", "base_trade_count", "cost_plus_1_net_profit", "cost_plus_1_profit_factor", "cost_plus_5_net_profit", "cost_plus_5_profit_factor", "worst_slice_axis", "worst_slice_bucket", "worst_slice_net_profit", "tester_to_feature_last_gap_minutes", "asof_forward_policy_blocked", "use_in_next_run", "claim_boundary"],
            failure_rows,
        ),
        write_csv(
            SOURCE_POLICY_MATRIX_CSV,
            ["repair_id", "target_attempt", "feature_set_id", "hypothesis", "changed_variable", "fixed_variables", "source_rule", "invalid_if", "required_evidence", "next_run_use", "claim_boundary"],
            source_rows,
        ),
        write_csv(
            COST_BUFFER_MATRIX_CSV,
            ["branch_id", "branch_type", "hypothesis", "forbidden_shortcut", "predeclared_controls", "success_criteria", "failure_criteria", "next_materialization", "claim_boundary"],
            cost_rows,
        ),
        write_csv(
            OVERFIT_GATE_CSV,
            ["gate_id", "required_check", "evidence_path", "blocks_claim", "effect", "claim_boundary"],
            overfit_rows,
        ),
        write_csv(
            ECONOMIC_SOURCE_CSV,
            ["source_family", "feature_role", "asof_rule", "missing_rule", "stress_slice", "claim_boundary"],
            economic_rows,
        ),
        write_csv(
            RUN337W_QUEUE_CSV,
            ["queue_id", "task", "required_inputs", "required_outputs", "blocked_if_missing", "claim_boundary"],
            queue_rows,
        ),
        write_csv(
            REQUIRED_GATE_AUDIT_CSV,
            ["gate_name", "status", "evidence_path", "effect", "claim_boundary"],
            gate_rows,
        ),
    ]
    artifact_paths.extend(build_receipts(metrics))
    artifact_paths.append(write_report(metrics))
    artifact_paths.append(write_decision_doc(metrics))
    artifact_paths.extend(update_status_docs())
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "failure_memory_rows": len(failure_rows),
        "source_policy_repairs": len(source_rows),
        "cost_buffer_branches": len(cost_rows),
        "overfit_parity_gates": len(overfit_rows),
        "run337w_queue_rows": len(queue_rows),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(FINAL_DECISION_JSON, final_decision))
    artifact_paths.extend(update_registers([*artifact_paths, Path(__file__)], generated_at))
    artifact_paths.append(
        write_json(
            RUN_MANIFEST_JSON,
            {
                **final_decision,
                "generated_at_utc": generated_at,
                "producer": rel(Path(__file__)),
                "source_inputs": [rel(RUN337R_CURVE), rel(RUN337T_COST), rel(RUN337U_DECISION)],
                "artifacts": [rel(path) for path in artifact_paths if path_exists(path)],
            },
        )
    )
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
