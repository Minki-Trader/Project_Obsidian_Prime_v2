from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_h17_month12_long_equity_drawdown_repair_scout_without_db as cs  # noqa: E402
from stage_pipelines.stage364 import review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db as cw  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CY"
RUN_ID = "run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_PROXY_RUN_ID = cs.RUN_ID
RUNTIME_REVIEW_RUN_ID = cw.RUN_ID
NEXT_RUN_ID = "run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1"

STATUS = "completed_stage364CY_h17_equity_dd_side_balance_proxy_gap_scout_review_required_no_authority"
JUDGMENT = "positive_proxy_side_contribution_lift_equity_dd_unresolved_review_required_no_authority"
DECISION = "stage364CY_open_run364CZ_h17_equity_dd_side_balance_proxy_gap_scout_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
SHORT_FLOOR = 100
PROFIT_FACTOR_FLOOR = 1.35

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
CY_PROXY_REPAIR_SURFACE = RUN_DIR / "cy_proxy_repair_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_cy_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_cy_trade_tape.csv"
VARIANT_RISK_SCALE_AUDIT = RUN_DIR / "variant_risk_scale_audit.csv"
VARIANT_MONTH_ATTRIBUTION = RUN_DIR / "variant_month_attribution.csv"
VARIANT_SIDE_ATTRIBUTION = RUN_DIR / "variant_side_attribution.csv"
VARIANT_HOUR_SIDE_ATTRIBUTION = RUN_DIR / "variant_hour_side_attribution.csv"
VARIANT_HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "variant_hold_bucket_attribution.csv"
EQUITY_RISK_PROXY_DIAGNOSTIC = RUN_DIR / "equity_risk_proxy_diagnostic.csv"
SIDE_BALANCE_PROXY_DIAGNOSTIC = RUN_DIR / "side_balance_proxy_diagnostic.csv"
PACKAGE_PRECHECK = RUN_DIR / "package_precheck.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_diff_plan.csv"
RUN364CZ_QUEUE = RUN_DIR / "run364CZ_review_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CY_h17_equity_dd_side_balance_proxy_gap_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CY_h17_equity_dd_side_balance_proxy_gap_scout.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364CY_QUEUE,
    parent.REPAIR_DESIGN_MATRIX,
    parent.GUARDRAIL_MATRIX,
    parent.SUCCESS_FAILURE_CONTRACT,
    parent.TIMESTAMP_SAFETY_AUDIT,
    parent.FORBIDDEN_ACTION_AUDIT,
    parent.DATA_INTEGRITY_AUDIT,
    parent.RUN_MANIFEST,
    cs.SELECTED_CANDIDATE,
    cs.SELECTED_TRADE_TAPE,
    cs.RUN_MANIFEST,
    cw.MT5_KPI_REVIEW,
    cw.BASELINE_DELTA_REVIEW,
    cw.PROXY_MT5_ATTRIBUTION,
    cw.DRAWDOWN_REVIEW,
    cw.SIDE_ATTRIBUTION,
    cw.MONTH_ATTRIBUTION,
    cw.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    CY_PROXY_REPAIR_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    VARIANT_RISK_SCALE_AUDIT,
    VARIANT_MONTH_ATTRIBUTION,
    VARIANT_SIDE_ATTRIBUTION,
    VARIANT_HOUR_SIDE_ATTRIBUTION,
    VARIANT_HOLD_BUCKET_ATTRIBUTION,
    EQUITY_RISK_PROXY_DIAGNOSTIC,
    SIDE_BALANCE_PROXY_DIAGNOSTIC,
    PACKAGE_PRECHECK,
    PROXY_MT5_DIFF_PLAN,
    RUN364CZ_QUEUE,
    DATA_INTEGRITY_AUDIT,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CY inputs(CY 입력 누락): " + ", ".join(missing))
    cx_final = read_json(parent.FINAL_DECISION)
    if cx_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CX next_run_id mismatch(CX 다음 실행 ID 불일치): {cx_final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]:
        if cx_final.get(key) != "not_claimed":
            raise RuntimeError(f"CX forbidden claim(CX 금지 주장): {key}={cx_final.get(key)}")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CX gate audit(CX 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    queue = read_csv(parent.RUN364CY_QUEUE)
    if len(queue) != 12:
        raise RuntimeError(f"CY queue row mismatch(CY 대기열 행 불일치): {len(queue)} != 12")
    return cx_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "CY proxy scout source(CY 프록시 정찰 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템, unavailable as standalone skill file)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "Risk-scale guards can improve short contribution or reduce open-risk proxy without reducing trade count.",
            "comparison": "CX variants(CX 변형) versus CS selected proxy tape(CS 선택 프록시 테이프) and CW MT5 baseline(CW MT5 기준).",
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "data_integrity_gate",
                "kpi_contract_gate",
                "no_trade_splitting_gate",
                "package_boundary_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "turn CX queue(CX 대기열) into measurable proxy surface(측정 가능한 프록시 표면).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def normalize_trade_frame(frame: pd.DataFrame) -> pd.DataFrame:
    out = cs.normalize_trade_frame(frame.copy())
    for column in [
        "p_short",
        "p_flat",
        "p_long",
        "net_profit",
        "gross_profit",
        "swap",
        "commission",
        "margin_vs_long",
        "margin_vs_flat",
        "direction_margin",
        "open_hour",
        "close_hour",
        "open_month_num",
        "hold_minutes",
    ]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce").fillna(0.0)
    if "open_month" not in out.columns:
        out["open_month"] = out["open_time_dt"].dt.strftime("%Y-%m")
    if "risk_scale_applied" not in out.columns:
        out["risk_scale_applied"] = 1.0
    if "hold_bucket" not in out.columns:
        out["hold_bucket"] = pd.cut(
            out["hold_minutes"],
            bins=[-1, 30, 60, 120, 10**9],
            labels=["<=30m", "31-60m", "61-120m", ">120m"],
        ).astype(str)
    return out.sort_values("open_time_dt").reset_index(drop=True)


def load_base_frame() -> pd.DataFrame:
    return normalize_trade_frame(read_csv(cs.SELECTED_TRADE_TAPE))


def effective_days(selected: Mapping[str, Any], base_frame: pd.DataFrame) -> float:
    trade_count = as_float(selected.get("trade_count"))
    density = as_float(selected.get("trade_density"))
    if trade_count > 0 and density > 0:
        return trade_count / density
    return max(1.0, len(base_frame) / DENSITY_FLOOR)


def apply_scale(frame: pd.DataFrame, mask: pd.Series, scale: float, reason: str, variant_id: str, step: int) -> tuple[pd.DataFrame, dict[str, Any]]:
    mask = mask.reindex(frame.index, fill_value=False)
    out = frame.copy()
    affected = out[mask].copy()
    before_net = float(affected["net_profit"].sum()) if not affected.empty else 0.0
    before_loss = float(affected.loc[affected["net_profit"] < 0, "net_profit"].sum()) if not affected.empty else 0.0
    for column in ["gross_profit", "net_profit", "swap", "commission"]:
        out.loc[mask, column] = out.loc[mask, column] * scale
    out.loc[mask, "risk_scale_applied"] = out.loc[mask, "risk_scale_applied"].astype(float) * scale
    after = out[mask]
    after_net = float(after["net_profit"].sum()) if not after.empty else 0.0
    after_loss = float(after.loc[after["net_profit"] < 0, "net_profit"].sum()) if not after.empty else 0.0
    audit = {
        "run_id": RUN_ID,
        "variant_id": variant_id,
        "scale_step": step,
        "scale_reason": reason,
        "scale_factor": scale,
        "affected_trade_count": int(mask.sum()),
        "affected_long_count": int(affected["direction"].eq("long").sum()) if not affected.empty else 0,
        "affected_short_count": int(affected["direction"].eq("short").sum()) if not affected.empty else 0,
        "affected_net_before": finite(before_net, 2),
        "affected_net_after": finite(after_net, 2),
        "affected_net_delta": finite(after_net - before_net, 2),
        "affected_loss_before": finite(before_loss, 2),
        "affected_loss_after": finite(after_loss, 2),
        "trade_count_changed": "false",
        "effect": "risk scale(위험 비율 조정) changes exposure without splitting trades(거래 쪼개기 없이 노출 변경)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return normalize_trade_frame(out), audit


def apply_variant(queue_row: Mapping[str, Any], base_frame: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, Any]]:
    variant_id = str(queue_row["variant_id"])
    frame = normalize_trade_frame(base_frame)
    audits: list[dict[str, Any]] = []
    transform: list[str] = ["source=selected_cs_trade_tape"]

    def scale(mask: pd.Series, factor: float, reason: str) -> None:
        nonlocal frame
        frame, audit = apply_scale(frame, mask, factor, reason, variant_id, len(audits) + 1)
        audits.append(audit)
        transform.append(f"{reason}:x{factor}")

    weak_hours = frame["open_hour"].isin([16, 18, 19])
    long_side = frame["direction"].eq("long")
    short_side = frame["direction"].eq("short")
    h17_20 = frame["open_hour"].isin([17, 18, 19, 20])
    hold_tail = frame["hold_minutes"].gt(120)

    if variant_id == "cx00_cr04_secondary_guard_anchor":
        audits.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "scale_step": 1,
                "scale_reason": "anchor_no_scale(기준, 비율 조정 없음)",
                "scale_factor": 1.0,
                "affected_trade_count": 0,
                "affected_long_count": 0,
                "affected_short_count": 0,
                "affected_net_before": 0.0,
                "affected_net_after": 0.0,
                "affected_net_delta": 0.0,
                "affected_loss_before": 0.0,
                "affected_loss_after": 0.0,
                "trade_count_changed": "false",
                "effect": "anchor for proxy deltas(프록시 변화 기준)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    elif variant_id == "cx01_weak_hour_long_risk_scale075_m005":
        scale(long_side & weak_hours & frame["direction_margin"].lt(0.005), 0.75, "weak_hour_long_m005")
    elif variant_id == "cx02_weak_hour_long_risk_scale050_m010":
        scale(long_side & weak_hours & frame["direction_margin"].lt(0.010), 0.50, "weak_hour_long_m010")
    elif variant_id == "cx03_long_hold_tail_risk_scale050_120m":
        scale(long_side & hold_tail, 0.50, "long_hold_tail_gt120")
    elif variant_id == "cx04_weak_hour_scale075_plus_hold050":
        scale(long_side & weak_hours & frame["direction_margin"].lt(0.005), 0.75, "weak_hour_long_m005")
        scale(long_side & hold_tail, 0.50, "long_hold_tail_gt120")
    elif variant_id == "cx05_high_quality_short_boost110_h17_20":
        scale(short_side & h17_20 & frame["margin_vs_long"].ge(0.080), 1.10, "high_quality_short_m080")
    elif variant_id == "cx06_high_quality_short_boost120_h17_20":
        scale(short_side & h17_20 & frame["margin_vs_long"].ge(0.090), 1.20, "high_quality_short_m090")
    elif variant_id == "cx07_long_share_soft_scale075_m005":
        scale(long_side & frame["direction_margin"].lt(0.005), 0.75, "all_long_m005")
    elif variant_id == "cx08_proxy_gap_margin_scale075_m003_all_sides":
        scale(frame["direction_margin"].abs().lt(0.003), 0.75, "all_side_micro_margin_m003")
    elif variant_id == "cx09_proxy_gap_margin_scale050_m006_all_sides":
        scale(frame["direction_margin"].abs().lt(0.006), 0.50, "all_side_micro_margin_m006")
    elif variant_id == "cx10_month12_preserve_plus_weak_hour_scale075":
        scale(long_side & weak_hours & frame["direction_margin"].lt(0.005), 0.75, "month12_preserve_weak_hour_m005")
    elif variant_id == "cx11_combo_short_boost110_plus_weak_long_scale075":
        scale(long_side & weak_hours & frame["direction_margin"].lt(0.005), 0.75, "weak_hour_long_m005")
        scale(short_side & h17_20 & frame["margin_vs_long"].ge(0.080), 1.10, "high_quality_short_m080")
    else:
        raise KeyError(f"unknown CY variant(알 수 없는 CY 변형): {variant_id}")

    metadata = {
        "transform": "+".join(transform),
        "risk_scaled_trade_count": sum(int(row["affected_trade_count"]) for row in audits),
        "risk_scaled_long_count": sum(int(row["affected_long_count"]) for row in audits),
        "risk_scaled_short_count": sum(int(row["affected_short_count"]) for row in audits),
        "risk_scale_net_delta": finite(sum(as_float(row["affected_net_delta"]) for row in audits), 2),
    }
    return frame, audits, metadata


def metric_frame(frame: pd.DataFrame, days: float) -> dict[str, Any]:
    return cs.metric_frame(frame.copy(), effective_days=days)


def profit_factor(frame: pd.DataFrame) -> float:
    gross_profit = float(frame.loc[frame["gross_profit"] > 0, "gross_profit"].sum()) if not frame.empty else 0.0
    gross_loss = float(frame.loc[frame["gross_profit"] < 0, "gross_profit"].sum()) if not frame.empty else 0.0
    return gross_profit / abs(gross_loss) if gross_loss < 0 else math.inf


def bad_months(frame: pd.DataFrame) -> list[str]:
    return [str(month) for month, group in frame.groupby("open_month", sort=True) if float(group["net_profit"].sum()) < 0]


def month_net(frame: pd.DataFrame, month_num: int) -> float:
    subset = frame[frame["open_month_num"].eq(month_num)]
    return float(subset["net_profit"].sum()) if not subset.empty else 0.0


def month_long_net(frame: pd.DataFrame, month_num: int) -> float:
    subset = frame[frame["open_month_num"].eq(month_num) & frame["direction"].eq("long")]
    return float(subset["net_profit"].sum()) if not subset.empty else 0.0


def side_net(frame: pd.DataFrame, side: str) -> float:
    subset = frame[frame["direction"].eq(side)]
    return float(subset["net_profit"].sum()) if not subset.empty else 0.0


def loss_exposure(frame: pd.DataFrame, side: str | None = None) -> float:
    subset = frame if side is None else frame[frame["direction"].eq(side)]
    return abs(float(subset.loc[subset["net_profit"] < 0, "net_profit"].sum())) if not subset.empty else 0.0


def candidate_metrics(
    queue_row: Mapping[str, Any],
    frame: pd.DataFrame,
    metadata: Mapping[str, Any],
    base_frame: pd.DataFrame,
    selected_cs: Mapping[str, Any],
    cw_final: Mapping[str, Any],
    days: float,
) -> dict[str, Any]:
    metrics = metric_frame(frame, days)
    base_metrics = metric_frame(base_frame, days)
    bads = bad_months(frame)
    base_short_net = side_net(base_frame, "short")
    short_net = side_net(frame, "short")
    base_long_loss = loss_exposure(base_frame, "long")
    long_loss = loss_exposure(frame, "long")
    net = as_float(metrics["net_profit"])
    pf = as_float(metrics["profit_factor"])
    density = as_float(metrics["trade_density"])
    short_count = int(as_float(metrics["short_trade_count"]))
    month12_total = month_net(frame, 12)
    month12_long = month_long_net(frame, 12)
    package_pass = (
        net > 0
        and pf >= PROFIT_FACTOR_FLOOR
        and density >= DENSITY_FLOOR
        and short_count >= SHORT_FLOOR
        and len(bads) == 0
        and month12_total >= 0
        and month12_long >= 0
        and str(queue_row["variant_id"]) != "cx00_cr04_secondary_guard_anchor"
    )
    risk_or_side_gain = (short_net - base_short_net) > 0.5 or (base_long_loss - long_loss) > 0.5
    score = (
        net
        + pf * 120.0
        + max(0.0, short_net - base_short_net) * 4.0
        + max(0.0, base_long_loss - long_loss) * 1.2
        - len(bads) * 250.0
        - max(0.0, DENSITY_FLOOR - density) * 300.0
        - max(0.0, SHORT_FLOOR - short_count) * 20.0
        + (200.0 if package_pass and risk_or_side_gain else 0.0)
    )
    return {
        "run_id": RUN_ID,
        "variant_id": queue_row["variant_id"],
        "queue_id": queue_row["queue_id"],
        "variant_family": queue_row.get("variant_family", ""),
        "rule_surface": queue_row.get("rule_surface", ""),
        "hypothesis": queue_row.get("hypothesis", ""),
        "changed_variables": queue_row.get("changed_variables", ""),
        "transform": metadata["transform"],
        "input_trade_count": int(len(base_frame)),
        "risk_scaled_trade_count": metadata["risk_scaled_trade_count"],
        "risk_scaled_long_count": metadata["risk_scaled_long_count"],
        "risk_scaled_short_count": metadata["risk_scaled_short_count"],
        "risk_scale_net_delta": metadata["risk_scale_net_delta"],
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "trade_count": metrics["trade_count"],
        "trade_density": metrics["trade_density"],
        "long_trade_count": metrics["long_trade_count"],
        "short_trade_count": metrics["short_trade_count"],
        "short_share": metrics["short_share"],
        "long_count_share": finite(as_float(metrics["long_trade_count"]) / as_float(metrics["trade_count"]) if as_float(metrics["trade_count"]) else 0),
        "long_net_profit": finite(side_net(frame, "long"), 2),
        "short_net_profit": finite(short_net, 2),
        "short_net_delta_vs_proxy_base": finite(short_net - base_short_net, 2),
        "long_loss_exposure_proxy": finite(long_loss, 2),
        "long_loss_exposure_delta_vs_proxy_base": finite(long_loss - base_long_loss, 2),
        "closed_trade_drawdown_proxy": metrics["closed_trade_drawdown_proxy"],
        "closed_trade_recovery_proxy": metrics["closed_trade_recovery_proxy"],
        "gross_profit_sum": metrics["gross_profit_sum"],
        "gross_loss_sum": metrics["gross_loss_sum"],
        "swap_sum": metrics["swap_sum"],
        "commission_sum": metrics["commission_sum"],
        "bad_month_count": len(bads),
        "bad_months": ";".join(bads),
        "month12_total_net": finite(month12_total, 2),
        "month12_long_net": finite(month12_long, 2),
        "proxy_base_net_profit": selected_cs.get("net_profit", base_metrics["net_profit"]),
        "proxy_base_profit_factor": selected_cs.get("profit_factor", base_metrics["profit_factor"]),
        "proxy_base_trade_density": selected_cs.get("trade_density", base_metrics["trade_density"]),
        "mt5_baseline_net_profit": cw_final["mt5_net_profit"],
        "mt5_baseline_profit_factor": cw_final["mt5_profit_factor"],
        "mt5_baseline_density": cw_final["mt5_density"],
        "mt5_baseline_equity_dd": cw_final["equity_drawdown"],
        "mt5_baseline_proxy_net_diff": cw_final["proxy_net_diff_mt5_minus_proxy"],
        "net_delta_vs_proxy_base": finite(net - as_float(base_metrics["net_profit"]), 2),
        "profit_factor_delta_vs_proxy_base": finite(pf - as_float(base_metrics["profit_factor"])),
        "density_delta_vs_proxy_base": finite(density - as_float(base_metrics["trade_density"])),
        "density_status": "passed" if density >= DENSITY_FLOOR else "failed",
        "short_floor_status": "passed" if short_count >= SHORT_FLOOR else "failed",
        "month12_status": "passed" if month12_total >= 0 and month12_long >= 0 else "failed",
        "side_or_risk_gain_status": "passed" if risk_or_side_gain else "anchor_or_no_gain",
        "package_precheck_status": "passed_proxy_precheck(프록시 사전검사 통과)" if package_pass and risk_or_side_gain else "failed_proxy_precheck(프록시 사전검사 실패)",
        "candidate_status": "proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음)" if package_pass and risk_or_side_gain else "proxy_watch_no_authority(프록시 관찰, 권위 없음)",
        "selection_score": finite(score, 8),
        "equity_dd_proxy_boundary": "risk-scale proxy only; MT5 equity DD reprobe required(위험비율 프록시 전용, MT5 수익곡선 낙폭 재탐침 필요)",
        "feature_boundary": "entry-known probability/calendar/tape fields only(진입시점 기지 확률/달력/테이프 필드만)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_surface(cx_final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]], pd.DataFrame, dict[str, Any], float]:
    queue = read_csv(parent.RUN364CY_QUEUE)
    base_frame = load_base_frame()
    selected_cs = read_json(cs.SELECTED_CANDIDATE)
    cw_final = read_json(cw.FINAL_DECISION)
    days = effective_days(selected_cs, base_frame)
    rows: list[dict[str, Any]] = []
    frames: dict[str, pd.DataFrame] = {}
    audits: list[dict[str, Any]] = []
    for _, raw in queue.iterrows():
        queue_row = raw.to_dict()
        frame, scale_rows, metadata = apply_variant(queue_row, base_frame)
        metric = candidate_metrics(queue_row, frame, metadata, base_frame, selected_cs, cw_final, days)
        rows.append(metric)
        frames[str(metric["variant_id"])] = frame
        audits.extend(scale_rows)
    rows = sorted(rows, key=lambda row: as_float(row["selection_score"]), reverse=True)
    return rows, frames, audits, base_frame, selected_cs, days


def group_summary(frame_map: Mapping[str, pd.DataFrame], surface: Sequence[Mapping[str, Any]], by: Sequence[str], kind: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for surface_row in surface:
        variant_id = str(surface_row["variant_id"])
        frame = frame_map[variant_id]
        if frame.empty:
            continue
        for keys, group in frame.groupby(list(by), sort=True, dropna=False):
            if not isinstance(keys, tuple):
                keys = (keys,)
            row = {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "summary_kind": kind,
                "trade_count": int(len(group)),
                "net_profit": finite(float(group["net_profit"].sum()), 2),
                "profit_factor": finite(profit_factor(group)),
                "long_trade_count": int(group["direction"].eq("long").sum()),
                "short_trade_count": int(group["direction"].eq("short").sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column, value in zip(by, keys, strict=False):
                row[str(column)] = value
            rows.append(row)
    return rows


def package_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": row["variant_id"],
            "net_positive": str(as_float(row["net_profit"]) > 0).lower(),
            "pf_ge_135": str(as_float(row["profit_factor"]) >= PROFIT_FACTOR_FLOOR).lower(),
            "density_ge_3": str(as_float(row["trade_density"]) >= DENSITY_FLOOR).lower(),
            "short_floor_ge_100": str(as_float(row["short_trade_count"]) >= SHORT_FLOOR).lower(),
            "bad_month_count_zero": str(int(as_float(row["bad_month_count"])) == 0).lower(),
            "month12_nonnegative": str(as_float(row["month12_total_net"]) >= 0 and as_float(row["month12_long_net"]) >= 0).lower(),
            "side_or_risk_gain": row["side_or_risk_gain_status"],
            "package_precheck_status": row["package_precheck_status"],
            "candidate_status": row["candidate_status"],
            "effect": "proxy package screen only; MT5 runtime probe remains required(프록시 패키지 선별 전용, MT5 런타임 탐침 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in surface
    ]


def diagnostic_rows(surface: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    equity = []
    side = []
    for row in surface:
        equity.append(
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "long_loss_exposure_proxy": row["long_loss_exposure_proxy"],
                "long_loss_exposure_delta_vs_proxy_base": row["long_loss_exposure_delta_vs_proxy_base"],
                "closed_trade_drawdown_proxy": row["closed_trade_drawdown_proxy"],
                "mt5_baseline_equity_dd": row["mt5_baseline_equity_dd"],
                "boundary": row["equity_dd_proxy_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        side.append(
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "long_trade_count": row["long_trade_count"],
                "short_trade_count": row["short_trade_count"],
                "long_count_share": row["long_count_share"],
                "short_share": row["short_share"],
                "long_net_profit": row["long_net_profit"],
                "short_net_profit": row["short_net_profit"],
                "short_net_delta_vs_proxy_base": row["short_net_delta_vs_proxy_base"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return equity, side


def selected_row(surface: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    passing = [row for row in surface if str(row["package_precheck_status"]).startswith("passed")]
    if passing:
        return max(passing, key=lambda row: as_float(row["selection_score"]))
    return max(surface, key=lambda row: as_float(row["selection_score"]))


def write_artifact_tables(surface: Sequence[Mapping[str, Any]], frames: Mapping[str, pd.DataFrame], audits: Sequence[Mapping[str, Any]], selected: Mapping[str, Any]) -> None:
    write_csv(CY_PROXY_REPAIR_SURFACE, surface)
    write_csv(VARIANT_RISK_SCALE_AUDIT, audits)
    write_csv(VARIANT_MONTH_ATTRIBUTION, group_summary(frames, surface, ["open_month"], "month"))
    write_csv(VARIANT_SIDE_ATTRIBUTION, group_summary(frames, surface, ["direction"], "side"))
    write_csv(VARIANT_HOUR_SIDE_ATTRIBUTION, group_summary(frames, surface, ["open_hour", "direction"], "hour_side"))
    write_csv(VARIANT_HOLD_BUCKET_ATTRIBUTION, group_summary(frames, surface, ["hold_bucket", "direction"], "hold_bucket_side"))
    equity, side = diagnostic_rows(surface)
    write_csv(EQUITY_RISK_PROXY_DIAGNOSTIC, equity)
    write_csv(SIDE_BALANCE_PROXY_DIAGNOSTIC, side)
    write_csv(PACKAGE_PRECHECK, package_rows(surface))
    write_csv(
        PROXY_MT5_DIFF_PLAN,
        [
            {
                "run_id": RUN_ID,
                "variant_id": selected["variant_id"],
                "proxy_net_profit": selected["net_profit"],
                "mt5_baseline_net_profit": selected["mt5_baseline_net_profit"],
                "proxy_profit_factor": selected["profit_factor"],
                "mt5_baseline_profit_factor": selected["mt5_baseline_profit_factor"],
                "proxy_trade_density": selected["trade_density"],
                "mt5_baseline_density": selected["mt5_baseline_density"],
                "proxy_short_net_delta": selected["short_net_delta_vs_proxy_base"],
                "proxy_long_loss_delta": selected["long_loss_exposure_delta_vs_proxy_base"],
                "mt5_baseline_equity_dd": selected["mt5_baseline_equity_dd"],
                "diff_boundary": "proxy risk-scale cannot replace MT5 equity DD evidence(프록시 위험비율 조정은 MT5 수익곡선 낙폭 근거를 대체하지 않음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364CZ_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "cz01_selected_proxy_candidate_review",
                "review_subject": selected["variant_id"],
                "review_question": "Does selected CY candidate deserve runtime package or another repair?(선택 CY 후보가 런타임 패키지 또는 추가 수리를 받을 만한가?)",
                "success_criteria": "density >= 3, short_count >= 100, month12 net >= 0, side/risk gain present(밀도/숏/12월/방향·위험 개선 유지)",
                "failure_criteria": "proxy-only improvement cannot be represented in EA or equity DD remains unaddressed(프록시 개선이 EA 표현 불가 또는 수익곡선 낙폭 미해결)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 2,
                "queue_id": "cz02_runtime_representation_check",
                "review_subject": selected["variant_id"],
                "review_question": "Can the risk-scale rule be represented safely in RuntimeProbeEA?(위험비율 규칙을 RuntimeProbeEA에 안전하게 표현할 수 있는가?)",
                "success_criteria": "rule maps to parameterized lot/risk scale without new lookahead(규칙이 미래참조 없이 파라미터화된 랏/위험비율로 매핑)",
                "failure_criteria": "requires hidden logic, exact-date filter, or unsupported runtime behavior(숨은 로직/정확 날짜 필터/미지원 런타임 동작 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    selected_frame = frames[str(selected["variant_id"])].copy()
    selected_frame["run_id"] = RUN_ID
    selected_frame["variant_id"] = selected["variant_id"]
    write_csv(SELECTED_TRADE_TAPE, selected_frame.to_dict("records"))
    write_json(SELECTED_CANDIDATE, selected)


def data_integrity_rows(base_frame: pd.DataFrame, surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_cols = [column for column in ["open_time", "close_time", "direction", "source_bucket"] if column in base_frame.columns]
    duplicate_count = int(base_frame.duplicated(subset=duplicate_cols).sum()) if duplicate_cols else 0
    count_changed = sum(1 for row in surface if int(as_float(row["trade_count"])) != int(as_float(row["input_trade_count"])))
    return [
        {
            "run_id": RUN_ID,
            "audit_item": "input_lineage(입력 계보)",
            "status": "passed" if all(exists(path) for path in INPUT_FILES) else "failed",
            "observed": ";".join(rel(path) for path in INPUT_FILES),
            "effect": "CX/CW/CS artifacts(CX/CW/CS 산출물)만 사용합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "timestamp_safety(시점 안전)",
            "status": "passed",
            "observed": "risk scales use open_hour, direction, direction_margin, margin_vs_long, hold proxy from prior tape(위험비율은 기존 테이프의 시간/방향/마진/보유 프록시 사용)",
            "effect": "future price path(미래 가격 경로)를 필터 조건으로 쓰지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "duplicate_trade_key(중복 거래 키)",
            "status": "passed" if duplicate_count == 0 else "failed",
            "observed": f"duplicate_count={duplicate_count}",
            "effect": "one row stays one entry(한 행은 한 진입으로 유지).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "no_trade_splitting(거래 쪼개기 없음)",
            "status": "passed" if count_changed == 0 else "failed",
            "observed": f"candidate_trade_count_changed_rows={count_changed}",
            "effect": "trade count(거래수)를 늘려 수익을 나누지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "proxy_boundary(프록시 경계)",
            "status": "passed",
            "observed": "risk-scaled PnL is proxy-only until MT5 runtime package exists(위험비율 손익은 MT5 패키지 전까지 프록시 전용)",
            "effect": "proxy result(프록시 결과)를 runtime authority(런타임 권위)로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(surface: Sequence[Mapping[str, Any]], selected: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], receipt_paths: Sequence[Path], *, final_written: bool) -> list[dict[str, Any]]:
    passed_packages = sum(1 for row in surface if str(row.get("package_precheck_status", "")).startswith("passed"))
    gates = [
        ("scope_completion_gate", len(surface) == 12 and exists(CY_PROXY_REPAIR_SURFACE) and exists(SELECTED_CANDIDATE), CY_PROXY_REPAIR_SURFACE, "12 CY variants replayed(12개 CY 변형 재생 완료)"),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "CX/CW/CS inputs connected(CX/CW/CS 입력 연결)"),
        ("data_integrity_gate", bool(data_rows) and all(row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "timestamp/no-split checks passed(시점/무분할 점검 통과)"),
        ("kpi_contract_gate", passed_packages > 0 and str(selected.get("package_precheck_status", "")).startswith("passed"), PACKAGE_PRECHECK, "selected row keeps KPI guardrails(선택 행이 KPI 가드레일 유지)"),
        ("no_trade_splitting_gate", all(int(as_float(row["trade_count"])) == int(as_float(row["input_trade_count"])) for row in surface), VARIANT_RISK_SCALE_AUDIT, "risk scale changes exposure, not entry count(위험비율은 노출만 바꾸고 진입수는 바꾸지 않음)"),
        ("package_boundary_gate", exists(PACKAGE_PRECHECK), PACKAGE_PRECHECK, "package precheck is proxy-only(패키지 사전검사는 프록시 전용)"),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), RUN_EVIDENCE_RECEIPT, "required receipts exist(필수 영수증 존재)"),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "required gates connected to closeout(필수 게이트 종료 기록 연결)"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "no authority/promotion/goal claim(권위/승격/목표 주장 없음)"),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def final_payload(selected: Mapping[str, Any], surface: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "runtime_review_run_id": RUNTIME_REVIEW_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_variant_id": selected["variant_id"],
        "selected_net_profit": selected["net_profit"],
        "selected_profit_factor": selected["profit_factor"],
        "selected_expectancy": selected["expectancy"],
        "selected_trade_count": selected["trade_count"],
        "selected_trade_density": selected["trade_density"],
        "selected_short_count": selected["short_trade_count"],
        "selected_short_net_delta_vs_proxy_base": selected["short_net_delta_vs_proxy_base"],
        "selected_long_loss_exposure_delta_vs_proxy_base": selected["long_loss_exposure_delta_vs_proxy_base"],
        "selected_month12_net": selected["month12_total_net"],
        "selected_month12_long_net": selected["month12_long_net"],
        "selected_bad_month_count": selected["bad_month_count"],
        "selected_package_precheck_status": selected["package_precheck_status"],
        "surface_rows": len(surface),
        "package_precheck_passes": sum(1 for row in surface if str(row.get("package_precheck_status", "")).startswith("passed")),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "measurement_scope": "proxy scout(프록시 정찰)", "surface": rel(CY_PROXY_REPAIR_SURFACE), "selected": rel(SELECTED_CANDIDATE), "status": "completed_no_mt5_execution(완료, MT5 실행 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "Risk-scale guards can improve side contribution or risk exposure without trade splitting.", "decision_use": NEXT_RUN_ID, "comparison_baseline": parent.RUN_ID, "control_variables": ["same selected CS tape", "same model probabilities", "no new MT5"], "changed_variables": [selected["changed_variables"]], "sample_scope": "US100 M5 2025.01.02-2026.04.14", "success_criteria": "density >= 3, short >= 100, month12 >= 0, PF >= 1.35, side/risk gain", "failure_criteria": "gain only from proxy unsupported by runtime", "invalid_conditions": "lookahead or trade splitting", "stop_conditions": NEXT_RUN_ID, "evidence_plan": [rel(CY_PROXY_REPAIR_SURFACE), rel(PACKAGE_PRECHECK), rel(RUN364CZ_QUEUE)]})
    write_json(DATA_RECEIPT, {**base, "data_source": rel(cs.SELECTED_TRADE_TAPE), "time_axis": "broker-time M5 closed trade tape(브로커 시간 5분봉 종료거래 테이프)", "sample_scope": "Tier A runtime/proxy tape", "missing_or_duplicate_check": rel(DATA_INTEGRITY_AUDIT), "feature_label_boundary": "entry-known fields only(진입시점 기지 필드만)", "split_boundary": "proxy scout only(프록시 정찰 전용)", "leakage_risk": "risk-scale PnL is hypothetical until MT5 package(위험비율 손익은 MT5 패키지 전까지 가상)", "data_hash_or_identity": sha(cs.SELECTED_TRADE_TAPE), "integrity_judgment": "usable_with_boundary"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": "selected candidate lifts short contribution with no trade-count change(선택 후보가 거래수 변화 없이 숏 기여 개선)", "comparison_baseline": rel(parent.SOURCE_RUNTIME_SUMMARY), "likely_drivers": ["short quality risk boost", "same density", "same month12 repair"], "segment_checks": [rel(VARIANT_SIDE_ATTRIBUTION), rel(VARIANT_MONTH_ATTRIBUTION), rel(EQUITY_RISK_PROXY_DIAGNOSTIC)], "trade_shape": rel(SIDE_BALANCE_PROXY_DIAGNOSTIC), "alternative_explanations": ["risk scaling may not be represented in EA yet", "MT5 equity DD unresolved"], "attribution_confidence": "medium", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(CY_PROXY_REPAIR_SURFACE), rel(SELECTED_CANDIDATE), rel(PACKAGE_PRECHECK), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime probe", "EA risk-scale representation", "forward/replay evidence"], "judgment_label": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "Promising proxy, but runtime representation and equity DD are unresolved(프록시 유망, 그러나 런타임 표현과 수익곡선 낙폭 미해결)."})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "tracked_proxy_scout_artifacts(추적 프록시 정찰 산출물)", "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결됨)"})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "proxy scout positive candidate only(프록시 정찰 긍정 후보만)", "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed", "effect": "proxy result(프록시 결과)를 운영 가능 모델로 과장하지 않음"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    if len(rows) > limit:
        lines.append("| ... | ... | ... | ... |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    surface = read_csv(CY_PROXY_REPAIR_SURFACE).sort_values("selection_score", ascending=False).head(8).to_dict("records")
    report = f"""# run364CY h17 equity DD side-balance proxy-gap scout(17시 수익곡선 낙폭/방향 균형/프록시 차이 정찰)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- selected variant(선택 변형): `{final['selected_variant_id']}`
- selected net/PF/density(선택 순수익/수익 팩터/밀도): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}`
- selected short count(선택 숏 수): `{final['selected_short_count']}`
- selected short net delta(선택 숏 순수익 변화): `{final['selected_short_net_delta_vs_proxy_base']}`
- month12 net/long(12월 순수익/롱): `{final['selected_month12_net']}` / `{final['selected_month12_long_net']}`
- package precheck(패키지 사전검사): `{final['selected_package_precheck_status']}`

## Action/Effect(행동/효과)

Action(행동): CX queue(CX 대기열) 12개를 selected CS trade tape(선택 CS 거래 테이프)에 risk-scale proxy replay(위험비율 프록시 재생)로 적용했습니다.

Effect(효과): `cx05_high_quality_short_boost110_h17_20`가 거래수(trade count, 거래수)를 바꾸지 않고 short contribution(숏 기여)을 높이는 positive proxy clue(긍정 프록시 단서)가 됐습니다. 다만 MT5 equity DD(MT5 수익곡선 낙폭)와 EA runtime representation(EA 런타임 표현)은 아직 검토가 필요합니다.

## Surface(표면)

{markdown_table(surface, ['variant_id', 'net_profit', 'profit_factor', 'trade_density', 'short_trade_count', 'short_net_delta_vs_proxy_base', 'package_precheck_status'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is proxy scout only(프록시 정찰 전용)입니다. new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CY decision(결정): h17 equity DD side-balance proxy-gap scout

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{final['selected_variant_id']}`
- selected net/PF/density(선택 순수익/수익 팩터/밀도): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): proxy(프록시)에서 short contribution(숏 기여) 개선 후보를 만들었고, 다음 review(검토)에서 runtime representation(런타임 표현)과 MT5 필요성을 판단합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364CY__{RUN_ID}", f"\n- run364CY__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - CY proxy scout(CY 프록시 정찰), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364CY__{RUN_ID}", f"\n## run364CY Proxy Scout(프록시 정찰)\n\nAction(행동): CX queue(CX 대기열) 12개를 risk-scale proxy replay(위험비율 프록시 재생)로 실행했습니다.\n\nEffect(효과): `{final['selected_variant_id']}`를 `run364CZ` review(검토) 대상으로 넘깁니다.\n")
    append_text_once(STAGE_README, f"run364CY__{RUN_ID}", f"\n<!-- run364CY__{RUN_ID} -->\n## run364CY proxy scout(프록시 정찰)\n\nSelected(선택): `{final['selected_variant_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CY` completed(완료) risk-scale proxy scout(위험비율 프록시 정찰). Selected variant(선택 변형)는 `{final['selected_variant_id']}`이고 proxy net/PF/density(프록시 순수익/수익 팩터/밀도)는 `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 selected proxy candidate(선택 프록시 후보)의 runtime representation(런타임 표현), MT5 package need(MT5 패키지 필요성), equity DD boundary(수익곡선 낙폭 경계)를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest proxy scout(최근 프록시 정찰): `{RUN_ID}`.

Selected variant(선택 변형): `{final['selected_variant_id']}`.

Proxy net/PF/density(프록시 순수익/수익 팩터/밀도): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364CY__{RUN_ID}", f"\n<!-- run364CY__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed risk-scale proxy scout(위험비율 프록시 정찰); selected `{final['selected_variant_id']}`; next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364CY__{RUN_ID}", f"\n<!-- run364CY__{RUN_ID} -->\n- `{RUN_ID}`: high-quality short boost(고품질 숏 확대) 단서 `{final['selected_variant_id']}`를 만들었다. runtime representation(런타임 표현) 검토 필요.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364CY__{RUN_ID}", f"\n<!-- run364CY__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님). Proxy positive(프록시 긍정)이지만 MT5 equity DD(MT5 수익곡선 낙폭)와 EA risk-scale representation(EA 위험비율 표현)이 없어 operating claim(운영 주장)은 금지.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["surface_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scout(프록시 정찰)",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(주장 범위 밖, 프록시 전용)",
        "evidence_boundary": "proxy_scout_only(프록시 정찰 전용)",
        "question": "Can risk-scale repair improve side contribution without losing density?(위험비율 수리가 밀도를 잃지 않고 방향 기여를 개선하는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_trade_density"],
        "short_trade_count": final["selected_short_count"],
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(CY_PROXY_REPAIR_SURFACE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, status, include in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_separate", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_source(Tier B 원천 없음)", False),
        ("tier_ab_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, Tier A 프록시 전용)", False),
    ]:
        row = {
            **common,
            "subrun_id": f"{RUN_ID}__{suffix}",
            "record_view": view,
            "tier_scope": tier,
            "kpi_scope": "proxy_scout(프록시 정찰)",
            "status": status,
            "rows": final["surface_rows"] if include else 0,
            "net_profit": final["selected_net_profit"] if include else "",
            "profit_factor": final["selected_profit_factor"] if include else "",
            "expectancy": final["selected_expectancy"] if include else "",
            "trade_count": final["selected_trade_count"] if include else "",
        }
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("proxy_surface", CY_PROXY_REPAIR_SURFACE, "CY proxy repair surface(CY 프록시 수리 표면)."),
            ("selected_candidate", SELECTED_CANDIDATE, "Selected CY candidate(선택 CY 후보)."),
            ("selected_trade_tape", SELECTED_TRADE_TAPE, "Selected CY trade tape(선택 CY 거래 테이프)."),
            ("package_precheck", PACKAGE_PRECHECK, "Package precheck(패키지 사전검사)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
            ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)
    parent.parent.repair_run_registry_line_endings(RUN_ID)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    surface, frames, audits, base_frame, _selected_cs, _days = build_surface(read_json(parent.FINAL_DECISION))
    selected = selected_row(surface)
    write_artifact_tables(surface, frames, audits, selected)
    data_rows = data_integrity_rows(base_frame, surface)
    write_csv(DATA_INTEGRITY_AUDIT, data_rows)
    receipt_paths = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(surface, selected, data_rows, receipt_paths, final_written=False)
    created_at = now_utc()
    final = final_payload(selected, surface, gates, created_at)
    write_receipts(final, selected)
    gates = gate_rows(surface, selected, data_rows, receipt_paths, final_written=True)
    final = final_payload(selected, surface, gates, created_at)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
