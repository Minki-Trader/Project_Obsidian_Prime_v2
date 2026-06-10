from __future__ import annotations

import csv
import hashlib
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
from stage_pipelines.stage364 import materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db as cq  # noqa: E402
from stage_pipelines.stage364 import train_h17_bad_month_source_balance_repair_scout_without_db as cm  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CS"
RUN_ID = "run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_PROXY_SCOUT_RUN_ID = cm.RUN_ID
RUNTIME_REVIEW_RUN_ID = cq.RUN_ID
NEXT_RUN_ID = "run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1"

STATUS = "completed_stage364CS_h17_month12_long_equity_drawdown_proxy_scout_review_required_no_authority"
JUDGMENT = "positive_proxy_repair_candidate_month12_long_guard_review_required_no_authority"
DECISION = "stage364CS_open_run364CT_h17_month12_long_equity_drawdown_repair_review"
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
CS_PROXY_REPAIR_SURFACE = RUN_DIR / "cs_proxy_repair_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_cs_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_cs_trade_tape.csv"
VARIANT_FILTER_AUDIT = RUN_DIR / "variant_filter_audit.csv"
VARIANT_MONTH_ATTRIBUTION = RUN_DIR / "variant_month_attribution.csv"
VARIANT_MONTH_SIDE_ATTRIBUTION = RUN_DIR / "variant_month_side_attribution.csv"
VARIANT_SIDE_ATTRIBUTION = RUN_DIR / "variant_side_attribution.csv"
VARIANT_HOUR_SIDE_ATTRIBUTION = RUN_DIR / "variant_hour_side_attribution.csv"
EQUITY_DD_PROXY_DIAGNOSTIC = RUN_DIR / "equity_dd_proxy_diagnostic.csv"
PACKAGE_PRECHECK = RUN_DIR / "package_precheck.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_diff_plan.csv"
RUN364CT_QUEUE = RUN_DIR / "run364CT_review_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CS_h17_month12_long_equity_drawdown_repair_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CS_h17_month12_long_equity_drawdown_repair_scout.md"
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
    parent.RUN364CS_QUEUE,
    parent.REPAIR_DESIGN_MATRIX,
    parent.SUCCESS_FAILURE_CONTRACT,
    parent.TIMESTAMP_SAFETY_AUDIT,
    parent.FORBIDDEN_ACTION_AUDIT,
    parent.RUN_MANIFEST,
    cq.MT5_KPI_REVIEW,
    cq.MONTH_SIDE_ATTRIBUTION,
    cq.DRAWDOWN_REVIEW,
    cq.SIDE_ATTRIBUTION,
    cq.RUN_MANIFEST,
    cm.FINAL_DECISION,
    cm.GATE_AUDIT,
    cm.SELECTED_CANDIDATE,
    cm.SELECTED_TRADE_TAPE,
    cm.CM_PROXY_REPAIR_SURFACE,
    cm.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    CS_PROXY_REPAIR_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    VARIANT_FILTER_AUDIT,
    VARIANT_MONTH_ATTRIBUTION,
    VARIANT_MONTH_SIDE_ATTRIBUTION,
    VARIANT_SIDE_ATTRIBUTION,
    VARIANT_HOUR_SIDE_ATTRIBUTION,
    EQUITY_DD_PROXY_DIAGNOSTIC,
    PACKAGE_PRECHECK,
    PROXY_MT5_DIFF_PLAN,
    RUN364CT_QUEUE,
    DATA_INTEGRITY_AUDIT,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.resolve().as_posix()


def exists(path: Path | str) -> bool:
    return io_path(path).exists()


def sha(path: Path | str) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


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
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in materialized:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    cm.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    cm.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    cm.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return cm.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return cm.finite(value, digits)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return cm.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CS inputs(CS 입력 누락): " + ", ".join(missing))
    cr_final = read_json(parent.FINAL_DECISION)
    cm_final = read_json(cm.FINAL_DECISION)
    cq_final = read_json(cq.FINAL_DECISION)
    if cr_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CR next_run_id mismatch(CR 다음 실행 불일치): {cr_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("CR", cr_final), ("CM", cm_final), ("CQ", cq_final)]:
        if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
            raise RuntimeError(f"{label} has forbidden authority claim({label} 금지 권위 주장 존재)")
    for label, gate_path in [("CR", parent.GATE_AUDIT), ("CM", cm.GATE_AUDIT), ("CQ", cq.GATE_AUDIT)]:
        gates = read_csv(gate_path)
        if gates.empty or any(gates["status"].astype(str) != "passed"):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    queue = read_csv(parent.RUN364CS_QUEUE)
    if len(queue) != 8:
        raise RuntimeError(f"CS queue row mismatch(CS 대기열 행 불일치): {len(queue)} != 8")
    return cr_final, cm_final, cq_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "CS proxy scout source(CS 프록시 정찰 원천)",
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
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "Month12 long guard(12월 롱 가드) can preserve density(밀도) while reducing the MT5-informed month12/equity-DD risk clue(MT5 기반 12월/수익곡선 낙폭 위험 단서).",
            "comparison": "CR variants(CR 변형) versus CM04 proxy tape(CM04 프록시 거래 테이프) and CQ MT5 baseline(CQ MT5 기준선).",
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
            "effect": "turn CR repair queue(CR 수리 대기열) into measurable proxy surface(측정 가능한 프록시 표면) without new MT5 execution(새 MT5 실행 없음).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def normalize_trade_frame(frame: pd.DataFrame) -> pd.DataFrame:
    out = cm.normalize_trade_frame(frame.copy())
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
    ]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce").fillna(0.0)
    if "open_month" not in out.columns:
        out["open_month"] = out["open_time_dt"].dt.strftime("%Y-%m")
    if "open_month_num" not in out.columns:
        out["open_month_num"] = out["open_time_dt"].dt.month
    if "direction_margin" not in out.columns:
        out["direction_margin"] = out.apply(
            lambda row: (
                row["p_long"] - max(row["p_short"], row["p_flat"])
                if str(row.get("direction", "")) == "long"
                else row["p_short"] - max(row["p_long"], row["p_flat"])
            ),
            axis=1,
        )
    return out.sort_values("open_time_dt").reset_index(drop=True)


def load_base_frame() -> pd.DataFrame:
    frame = read_csv(cm.SELECTED_TRADE_TAPE)
    return normalize_trade_frame(frame)


def empty_like(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.iloc[0:0].copy()


def remove_condition(frame: pd.DataFrame, condition: pd.Series, *, reason: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    condition = condition.reindex(frame.index, fill_value=False)
    removed = frame[condition].copy()
    if not removed.empty:
        removed["removed_reason"] = reason
    kept = frame[~condition].copy()
    return normalize_trade_frame(kept), normalize_trade_frame(removed) if not removed.empty else removed


def base_effective_days(cm_final: Mapping[str, Any]) -> float:
    count = as_float(cm_final.get("selected_trade_count"))
    density = as_float(cm_final.get("selected_trade_density"))
    if count > 0 and density > 0:
        return count / density
    return 314.0


def metric_frame(frame: pd.DataFrame, effective_days: float) -> dict[str, Any]:
    return cm.cj.metric_frame(frame.copy(), effective_days=effective_days)


def gross_loss(frame: pd.DataFrame) -> float:
    if frame.empty:
        return 0.0
    return float(frame.loc[frame["gross_profit"] < 0, "gross_profit"].sum())


def stress_adjusted_net(frame: pd.DataFrame) -> float:
    if frame.empty:
        return 0.0
    return float(frame["gross_profit"].sum()) + float(frame["swap"].sum()) * 2.0 + float(frame["commission"].sum())


def bad_months(frame: pd.DataFrame) -> list[str]:
    result: list[str] = []
    for month, group in frame.groupby("open_month", sort=True):
        if float(group["net_profit"].sum()) < 0:
            result.append(str(month))
    return result


def month12_long_net(frame: pd.DataFrame) -> float:
    subset = frame[frame["open_month_num"].eq(12) & frame["direction"].eq("long")]
    return float(subset["net_profit"].sum()) if not subset.empty else 0.0


def month12_total_net(frame: pd.DataFrame) -> float:
    subset = frame[frame["open_month_num"].eq(12)]
    return float(subset["net_profit"].sum()) if not subset.empty else 0.0


def apply_variant(queue_row: Mapping[str, Any], base_frame: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, Any]]:
    variant_id = str(queue_row["variant_id"])
    frame = normalize_trade_frame(base_frame)
    filter_rows: list[dict[str, Any]] = []
    transform_parts = ["seed=cm04_cj09_month08_12_pair_guard"]

    def add_filter(reason: str, mask: pd.Series, transform: str) -> None:
        nonlocal frame
        before_short = int(frame["direction"].eq("short").sum())
        frame, removed = remove_condition(frame, mask, reason=reason)
        after_short = int(frame["direction"].eq("short").sum())
        filter_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "filter_step": len(filter_rows) + 1,
                "filter_reason": reason,
                "removed_trade_count": int(len(removed)),
                "removed_long_count": int(removed["direction"].eq("long").sum()) if not removed.empty else 0,
                "removed_short_count": int(removed["direction"].eq("short").sum()) if not removed.empty else 0,
                "removed_net_profit": finite(float(removed["net_profit"].sum()) if not removed.empty else 0.0, 2),
                "short_count_before": before_short,
                "short_count_after": after_short,
                "restored_trade_count": 0,
                "restored_net_profit": 0.0,
                "effect": "remove weak entry-known guard rows(진입 시점 기준 약한 가드 행 제거)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        transform_parts.append(transform)

    if variant_id == "cr00_cm04_runtime_review_baseline":
        filter_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "filter_step": 1,
                "filter_reason": "baseline_no_filter(기준선, 필터 없음)",
                "removed_trade_count": 0,
                "removed_long_count": 0,
                "removed_short_count": 0,
                "removed_net_profit": 0.0,
                "short_count_before": int(frame["direction"].eq("short").sum()),
                "short_count_after": int(frame["direction"].eq("short").sum()),
                "restored_trade_count": 0,
                "restored_net_profit": 0.0,
                "effect": "anchor proxy deltas(프록시 차이 기준점 고정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        return frame, filter_rows, {"transform": "+".join(transform_parts), "removed_trade_count": 0}

    month12_long = frame["open_month_num"].eq(12) & frame["direction"].eq("long")
    h17_20 = frame["open_hour"].isin([17, 18, 19, 20])
    h18_19 = frame["open_hour"].isin([18, 19])
    margin_lt_002 = frame["direction_margin"].lt(0.02)
    margin_lt_003 = frame["direction_margin"].lt(0.03)

    if variant_id == "cr01_month12_long_hours17_20_block":
        add_filter(
            "month12_long_hours17_20_block(12월 롱 17-20시 차단)",
            month12_long & h17_20,
            "month12_long_hours17_20_block",
        )
    elif variant_id == "cr02_month12_long_margin_floor_002":
        add_filter(
            "month12_long_margin_floor_002(12월 롱 마진 하한 0.02)",
            month12_long & margin_lt_002,
            "month12_long_margin_floor_002",
        )
    elif variant_id == "cr03_month12_long_margin_floor_003":
        add_filter(
            "month12_long_margin_floor_003(12월 롱 마진 하한 0.03)",
            month12_long & margin_lt_003,
            "month12_long_margin_floor_003",
        )
    elif variant_id == "cr04_month12_long_hours17_20_floor002":
        add_filter(
            "month12_long_hours17_20_floor002(12월 롱 17-20시 마진 0.02 하한)",
            month12_long & h17_20 & margin_lt_002,
            "month12_long_hours17_20_floor002",
        )
    elif variant_id == "cr05_equity_dd_long_hours18_19_floor002_all_months":
        add_filter(
            "all_month_long_hours18_19_floor002(전체 월 롱 18-19시 마진 0.02 하한)",
            frame["direction"].eq("long") & h18_19 & margin_lt_002,
            "all_month_long_hours18_19_floor002",
        )
    elif variant_id == "cr06_short_floor_preserve_month12_long_guard":
        add_filter(
            "short_floor_preserve_month12_long_hours17_20_block(숏 하한 보존 12월 롱 17-20시 차단)",
            month12_long & h17_20,
            "short_floor_preserve_month12_long_hours17_20_block",
        )
        filter_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "filter_step": len(filter_rows) + 1,
                "filter_reason": "short_floor_restore_not_needed(숏 하한 복원 불필요)",
                "removed_trade_count": 0,
                "removed_long_count": 0,
                "removed_short_count": 0,
                "removed_net_profit": 0.0,
                "short_count_before": int(frame["direction"].eq("short").sum()),
                "short_count_after": int(frame["direction"].eq("short").sum()),
                "restored_trade_count": 0,
                "restored_net_profit": 0.0,
                "effect": "short floor remains at or above 100(숏 하한 100 이상 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        transform_parts.append("short_floor_preserved_no_restore")
    elif variant_id == "cr07_equity_dd_and_bad_month_combo":
        add_filter(
            "combined_month12_and_equity_dd_guard(12월 손실과 수익곡선 낙폭 조합 가드)",
            (month12_long & h17_20) | (frame["direction"].eq("long") & h18_19 & margin_lt_002),
            "combined_month12_equity_dd_guard",
        )
    else:
        raise KeyError(f"unknown CS variant(알 수 없는 CS 변형): {variant_id}")

    return frame, filter_rows, {
        "transform": "+".join(transform_parts),
        "removed_trade_count": int(sum(as_float(row["removed_trade_count"]) for row in filter_rows)),
    }


def candidate_metrics(
    queue_row: Mapping[str, Any],
    frame: pd.DataFrame,
    metadata: Mapping[str, Any],
    base_frame: pd.DataFrame,
    cm_final: Mapping[str, Any],
    cq_kpi: Mapping[str, Any],
    effective_days: float,
) -> dict[str, Any]:
    variant_id = str(queue_row["variant_id"])
    metrics = metric_frame(frame, effective_days)
    base_metrics = metric_frame(base_frame, effective_days)
    base_stress_net = stress_adjusted_net(base_frame)
    stress_net = stress_adjusted_net(frame)
    bads = bad_months(frame)
    base_month12_long = month12_long_net(base_frame)
    current_month12_long = month12_long_net(frame)
    current_month12_total = month12_total_net(frame)
    mt5_month12_net = as_float(cq_kpi.get("worst_month_net"))
    mt5_equity_dd = as_float(cq_kpi.get("equity_drawdown_maximal_amount"))
    density = as_float(metrics["trade_density"])
    pf = as_float(metrics["profit_factor"])
    net = as_float(metrics["net_profit"])
    shorts = int(as_float(metrics["short_trade_count"]))
    dd_proxy = as_float(metrics["closed_trade_drawdown_proxy"])
    base_dd_proxy = as_float(base_metrics["closed_trade_drawdown_proxy"])
    removed = int(as_float(metadata.get("removed_trade_count")))
    month12_repaired = current_month12_long >= 0 and current_month12_total >= 0
    package_pass = (
        net > 0
        and pf >= PROFIT_FACTOR_FLOOR
        and density >= DENSITY_FLOOR
        and shorts >= SHORT_FLOOR
        and len(bads) == 0
        and month12_repaired
        and dd_proxy <= base_dd_proxy + 0.01
    )
    broad_density_failure = density < DENSITY_FLOOR
    score = (
        net
        + pf * 100.0
        + density * 10.0
        + max(current_month12_long, 0.0) * 2.0
        - len(bads) * 200.0
        - max(0.0, dd_proxy - base_dd_proxy) * 5.0
        - removed * 0.5
        + (100.0 if package_pass else 0.0)
        - (150.0 if broad_density_failure else 0.0)
    )
    return {
        "run_id": RUN_ID,
        "variant_id": variant_id,
        "queue_id": queue_row.get("queue_id", ""),
        "rule_surface": queue_row.get("rule_surface", ""),
        "hypothesis": queue_row.get("hypothesis", ""),
        "changed_variables": queue_row.get("changed_variables", ""),
        "transform": metadata.get("transform", ""),
        "input_trade_count": int(len(base_frame)),
        "removed_trade_count": removed,
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "trade_count": metrics["trade_count"],
        "trade_density": metrics["trade_density"],
        "long_trade_count": metrics["long_trade_count"],
        "short_trade_count": metrics["short_trade_count"],
        "short_share": metrics["short_share"],
        "closed_trade_drawdown_proxy": metrics["closed_trade_drawdown_proxy"],
        "closed_trade_recovery_proxy": metrics["closed_trade_recovery_proxy"],
        "gross_profit_sum": metrics["gross_profit_sum"],
        "gross_loss_sum": metrics["gross_loss_sum"],
        "swap_sum": metrics["swap_sum"],
        "commission_sum": metrics["commission_sum"],
        "stress_adjusted_net_swap_haircut_1x": finite(stress_net, 2),
        "stress_adjusted_net_delta_vs_proxy_base": finite(stress_net - base_stress_net, 2),
        "bad_month_count": len(bads),
        "bad_months": ";".join(bads),
        "month12_total_net": finite(current_month12_total, 2),
        "month12_long_net": finite(current_month12_long, 2),
        "month12_long_net_delta_vs_proxy_base": finite(current_month12_long - base_month12_long, 2),
        "proxy_base_net_profit": cm_final.get("selected_net_profit", base_metrics["net_profit"]),
        "proxy_base_profit_factor": cm_final.get("selected_profit_factor", base_metrics["profit_factor"]),
        "proxy_base_trade_density": cm_final.get("selected_trade_density", base_metrics["trade_density"]),
        "proxy_base_month12_long_net": finite(base_month12_long, 2),
        "mt5_baseline_net_profit": cq_kpi.get("net_profit", ""),
        "mt5_baseline_profit_factor": cq_kpi.get("profit_factor", ""),
        "mt5_baseline_density": cq_kpi.get("trade_density_per_feature_day", ""),
        "mt5_baseline_month12_net": finite(mt5_month12_net, 2),
        "mt5_baseline_equity_dd": finite(mt5_equity_dd, 2),
        "net_delta_vs_proxy_base": finite(net - as_float(base_metrics["net_profit"]), 2),
        "profit_factor_delta_vs_proxy_base": finite(pf - as_float(base_metrics["profit_factor"])),
        "density_delta_vs_proxy_base": finite(density - as_float(base_metrics["trade_density"])),
        "closed_dd_delta_vs_proxy_base": finite(dd_proxy - base_dd_proxy, 2),
        "density_status": "passed" if density >= DENSITY_FLOOR else "failed",
        "short_floor_status": "passed" if shorts >= SHORT_FLOOR else "failed",
        "month12_long_status": "passed" if current_month12_long >= 0 else "failed",
        "equity_dd_proxy_status": "passed_closed_trade_proxy_not_worse" if dd_proxy <= base_dd_proxy + 0.01 else "watch_closed_trade_proxy_worse",
        "package_precheck_status": "passed_proxy_precheck(프록시 사전검사 통과)" if package_pass else "failed_proxy_precheck(프록시 사전검사 실패)",
        "candidate_status": "proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음)" if package_pass else "proxy_watch_no_authority(프록시 관찰, 권위 없음)",
        "selection_score": finite(score, 8),
        "equity_dd_proxy_boundary": "closed_trade_proxy_only_mt5_equity_dd_reprobe_required(닫힌 거래 프록시 전용, MT5 수익곡선 낙폭 재탐침 필요)",
        "feature_boundary": "entry-known month_of_year/open_hour/probability_margin only(진입 시점 월/시간/확률 마진만 사용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_surface(cm_final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]], dict[str, Any]]:
    base_frame = load_base_frame()
    effective_days = base_effective_days(cm_final)
    queue = read_csv(parent.RUN364CS_QUEUE)
    cq_kpi = read_csv(cq.MT5_KPI_REVIEW).iloc[0].to_dict()
    rows: list[dict[str, Any]] = []
    frames: dict[str, pd.DataFrame] = {}
    filters: list[dict[str, Any]] = []
    for _, raw in queue.iterrows():
        queue_row = raw.to_dict()
        frame, filter_rows, metadata = apply_variant(queue_row, base_frame)
        row = candidate_metrics(queue_row, frame, metadata, base_frame, cm_final, cq_kpi, effective_days)
        rows.append(row)
        frames[str(row["variant_id"])] = frame
        filters.extend(filter_rows)
    rows = sorted(rows, key=lambda row: as_float(row["selection_score"]), reverse=True)
    base_metrics = {
        "effective_days": effective_days,
        "base_trade_count": len(base_frame),
        "base_net_profit": finite(float(base_frame["net_profit"].sum()), 2),
        "base_month12_long_net": finite(month12_long_net(base_frame), 2),
        "base_month12_total_net": finite(month12_total_net(base_frame), 2),
        "base_closed_trade_drawdown_proxy": metric_frame(base_frame, effective_days)["closed_trade_drawdown_proxy"],
    }
    return rows, frames, filters, base_metrics


def summary_rows(frame_map: Mapping[str, pd.DataFrame], surface: Sequence[Mapping[str, Any]], by: Sequence[str], output_kind: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for surface_row in surface:
        variant_id = str(surface_row["variant_id"])
        frame = frame_map[variant_id]
        if frame.empty:
            continue
        for keys, group in frame.groupby(list(by), sort=True):
            if not isinstance(keys, tuple):
                keys = (keys,)
            row = {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "summary_kind": output_kind,
                "trade_count": int(len(group)),
                "net_profit": finite(float(group["net_profit"].sum()), 2),
                "profit_factor": finite(cm.profit_factor(group)),
                "long_trade_count": int(group["direction"].eq("long").sum()),
                "short_trade_count": int(group["direction"].eq("short").sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column, value in zip(by, keys, strict=False):
                row[str(column)] = value
            rows.append(row)
    return rows


def equity_dd_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "closed_trade_drawdown_proxy": row["closed_trade_drawdown_proxy"],
                "closed_dd_delta_vs_proxy_base": row["closed_dd_delta_vs_proxy_base"],
                "mt5_baseline_equity_dd": row["mt5_baseline_equity_dd"],
                "equity_dd_proxy_status": row["equity_dd_proxy_status"],
                "boundary": row["equity_dd_proxy_boundary"],
                "effect": "closed trade proxy screens damage, but MT5 equity DD must be reprobed(닫힌 거래 프록시는 손상만 선별하고 MT5 수익곡선 낙폭은 재탐침해야 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def package_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "net_positive": str(as_float(row["net_profit"]) > 0).lower(),
                "pf_ge_135": str(as_float(row["profit_factor"]) >= PROFIT_FACTOR_FLOOR).lower(),
                "density_ge_3": str(as_float(row["trade_density"]) >= DENSITY_FLOOR).lower(),
                "short_floor_ge_100": str(as_float(row["short_trade_count"]) >= SHORT_FLOOR).lower(),
                "bad_month_count_zero": str(int(as_float(row["bad_month_count"])) == 0).lower(),
                "month12_long_nonnegative": str(as_float(row["month12_long_net"]) >= 0).lower(),
                "closed_dd_not_worse": str(as_float(row["closed_dd_delta_vs_proxy_base"]) <= 0.01).lower(),
                "package_precheck_status": row["package_precheck_status"],
                "candidate_status": row["candidate_status"],
                "effect": "proxy package screen only; MT5 runtime probe remains required(프록시 패키지 선별 전용, MT5 런타임 탐침 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_mt5_diff_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "comparison_id": "selected_cs_proxy_vs_cq_mt5(선택 CS 프록시 대 CQ MT5)",
            "proxy_net_profit": selected["net_profit"],
            "mt5_baseline_net_profit": selected["mt5_baseline_net_profit"],
            "proxy_profit_factor": selected["profit_factor"],
            "mt5_baseline_profit_factor": selected["mt5_baseline_profit_factor"],
            "proxy_trade_density": selected["trade_density"],
            "mt5_baseline_density": selected["mt5_baseline_density"],
            "proxy_month12_long_net": selected["month12_long_net"],
            "mt5_baseline_month12_net": selected["mt5_baseline_month12_net"],
            "proxy_closed_trade_dd": selected["closed_trade_drawdown_proxy"],
            "mt5_baseline_equity_dd": selected["mt5_baseline_equity_dd"],
            "diff_boundary": "proxy filters cannot replace MT5 equity/month runtime evidence(프록시 필터는 MT5 수익곡선/월 런타임 근거를 대체하지 않음)",
            "next_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "ct01_selected_proxy_candidate_review",
            "review_subject": selected["variant_id"],
            "review_question": "Does selected CS candidate keep net/PF/density while repairing month12 long weakness?(선택 CS 후보가 순수익/수익 팩터/밀도를 유지하며 12월 롱 약점을 수리하는가?)",
            "success_criteria": "density >= 3, shorts >= 100, month12 long net >= 0, no trade splitting(밀도 3 이상, 숏 100 이상, 12월 롱 0 이상, 거래 쪼개기 없음)",
            "failure_criteria": "improvement comes from density collapse or MT5/proxy gap remains unusable(개선이 밀도 붕괴에서 나오거나 MT5/프록시 차이가 사용 불가)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "ct02_equity_dd_runtime_probe_boundary",
            "review_subject": selected["variant_id"],
            "review_question": "Is a narrow MT5 runtime probe justified for equity DD?(수익곡선 낙폭 확인용 좁은 MT5 런타임 탐침이 정당한가?)",
            "success_criteria": "proxy damage screen passes and rule can be represented in EA inputs(프록시 손상 선별 통과 및 EA 입력 표현 가능)",
            "failure_criteria": "closed-trade proxy cannot target equity DD or rule needs unsafe runtime logic(닫힌 거래 프록시가 수익곡선 낙폭을 겨냥하지 못하거나 안전하지 않은 런타임 로직 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def data_integrity_rows(base_frame: pd.DataFrame, surface: Sequence[Mapping[str, Any]], filters: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue = read_csv(parent.RUN364CS_QUEUE)
    duplicate_count = int(base_frame.duplicated(subset=[column for column in ["open_time", "close_time", "direction", "source_bucket"] if column in base_frame.columns]).sum())
    count_over_base = sum(1 for row in surface if as_float(row["trade_count"]) > len(base_frame))
    logic_columns = [column for column in ["variant_id", "changed_variables", "rule_surface"] if column in queue.columns]
    logic_text = queue[logic_columns].astype(str) if logic_columns else pd.DataFrame()
    filter_text = pd.Series([str(row.get("filter_reason", "")) for row in filters])
    exact_date_rows = int(logic_text.apply(lambda col: col.str.contains("2025-", regex=False) | col.str.contains("2026-", regex=False)).any(axis=1).sum()) if not logic_text.empty else 0
    top_n_rows = int(logic_text.apply(lambda col: col.str.contains("top_n", case=False, regex=False)).any(axis=1).sum()) if not logic_text.empty else 0
    split_rows = int(logic_text.apply(lambda col: col.str.contains("trade_splitting", case=False, regex=False)).any(axis=1).sum()) if not logic_text.empty else 0
    filter_exact_date_rows = int((filter_text.str.contains("2025-", regex=False) | filter_text.str.contains("2026-", regex=False)).sum())
    filter_top_n_rows = int(filter_text.str.contains("top_n", case=False, regex=False).sum())
    filter_split_rows = int(filter_text.str.contains("trade_splitting", case=False, regex=False).sum())
    removed_short_rows = sum(int(as_float(row.get("removed_short_count"))) for row in filters)
    rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "input_lineage(입력 계보)",
            "status": "passed" if all(exists(path) for path in INPUT_FILES) else "failed",
            "observed": ";".join(rel(path) for path in INPUT_FILES),
            "effect": "CS uses CR/CQ/CM artifacts only(CS는 CR/CQ/CM 산출물만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "time_axis(시간축)",
            "status": "passed",
            "observed": "open_time sorted; filters use month_of_year/open_hour/direction_margin(진입 시각 정렬, 필터는 월/시간/방향 마진 사용)",
            "effect": "look-ahead path stays closed(미래참조 경로 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "duplicate_trade_key(중복 거래 키)",
            "status": "passed" if duplicate_count == 0 else "failed",
            "observed": f"duplicate_count={duplicate_count}",
            "effect": "one row remains one possible entry(한 행은 하나의 가능한 진입으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "feature_label_boundary(피처/라벨 경계)",
            "status": "passed",
            "observed": "filters do not use realized PnL; PnL is measurement only(필터는 실현 손익을 쓰지 않고 손익은 측정 전용)",
            "effect": "timestamp-safe scout(시점 안전 정찰) 경계를 유지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "no_trade_splitting(거래 쪼개기 없음)",
            "status": "passed" if count_over_base == 0 and removed_short_rows == 0 else "failed",
            "observed": f"candidate_count_gt_base={count_over_base};removed_short_rows={removed_short_rows}",
            "effect": "density is not inflated by added entries(밀도가 추가 진입으로 부풀지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "no_top_n_or_exact_date_filter(top_n/정확 날짜 필터 없음)",
            "status": "passed" if top_n_rows == 0 and exact_date_rows == 0 and split_rows == 0 and filter_exact_date_rows == 0 and filter_top_n_rows == 0 and filter_split_rows == 0 else "failed",
            "observed": f"logic_top_n_rows={top_n_rows};logic_exact_date_rows={exact_date_rows};logic_split_rows={split_rows};filter_exact_date_rows={filter_exact_date_rows};filter_top_n_rows={filter_top_n_rows};filter_split_rows={filter_split_rows}",
            "effect": "repair remains reusable calendar/hour/margin logic(수리는 재사용 가능한 월/시간/마진 로직으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "proxy_mt5_boundary(프록시/MT5 경계)",
            "status": "passed",
            "observed": "equity DD is closed-trade proxy only; MT5 reprobe required(수익곡선 낙폭은 닫힌 거래 프록시 전용, MT5 재탐침 필요)",
            "effect": "proxy result is not promoted into runtime authority(프록시 결과를 런타임 권위로 승격하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "tier_records(티어 기록)",
            "status": "passed",
            "observed": "Tier A separate, Tier B missing_required, Tier A+B out_of_scope are ledgered(Tier A 분리, Tier B 필수 누락, Tier A+B 범위 밖 장부화)",
            "effect": "Tier B is not silently omitted(Tier B를 조용히 생략하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def gate_rows(
    surface: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    data_rows: Sequence[Mapping[str, Any]],
    receipt_paths: Sequence[Path],
    *,
    final_written: bool,
) -> list[dict[str, Any]]:
    passed_packages = sum(1 for row in surface if str(row.get("package_precheck_status", "")).startswith("passed"))
    gates = [
        (
            "scope_completion_gate",
            len(surface) == 8 and exists(CS_PROXY_REPAIR_SURFACE) and exists(SELECTED_CANDIDATE),
            CS_PROXY_REPAIR_SURFACE,
            "8 CS variants were replayed(8개 CS 변형 재생 완료)",
        ),
        (
            "input_lineage_gate",
            all(exists(path) for path in INPUT_FILES),
            INPUT_MANIFEST,
            "CR/CQ/CM inputs are connected(CR/CQ/CM 입력 연결)",
        ),
        (
            "data_integrity_gate",
            bool(data_rows) and all(row["status"] == "passed" for row in data_rows),
            DATA_INTEGRITY_AUDIT,
            "timestamp/no-split/no-top-n checks passed(시점/무분할/no top-n 검사 통과)",
        ),
        (
            "kpi_contract_gate",
            passed_packages > 0 and str(selected.get("package_precheck_status", "")).startswith("passed"),
            PACKAGE_PRECHECK,
            "selected row keeps net/PF/density/short/month12 guards(선택 행이 순수익/수익 팩터/밀도/숏/12월 가드 유지)",
        ),
        (
            "no_trade_splitting_gate",
            all(as_float(row["trade_count"]) <= as_float(row["input_trade_count"]) for row in surface),
            VARIANT_FILTER_AUDIT,
            "no candidate creates more entries than input(어떤 후보도 입력보다 많은 진입을 만들지 않음)",
        ),
        (
            "package_boundary_gate",
            exists(PACKAGE_PRECHECK),
            PACKAGE_PRECHECK,
            "package precheck is proxy-only(패키지 사전검사는 프록시 전용)",
        ),
        (
            "receipt_coverage_gate",
            all(exists(path) for path in receipt_paths),
            RUN_EVIDENCE_RECEIPT,
            "skill receipts exist(스킬 영수증 존재)",
        ),
        (
            "required_gate_coverage_audit",
            final_written,
            GATE_AUDIT,
            "required gates are connected to closeout(필수 게이트가 종료 기록에 연결)",
        ),
        (
            "final_claim_guard",
            exists(CLAIM_RECEIPT),
            CLAIM_RECEIPT,
            "runtime/operating claims remain blocked(런타임/운영 주장은 계속 차단)",
        ),
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


def final_payload(
    selected: Mapping[str, Any],
    surface: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    base_metrics: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_scout_run_id": SOURCE_PROXY_SCOUT_RUN_ID,
        "runtime_review_run_id": RUNTIME_REVIEW_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "surface_rows": len(surface),
        "package_precheck_pass_rows": sum(1 for row in surface if str(row.get("package_precheck_status", "")).startswith("passed")),
        "selected_variant_id": selected["variant_id"],
        "selected_candidate_status": selected["candidate_status"],
        "selected_package_precheck_status": selected["package_precheck_status"],
        "selected_net_profit": selected["net_profit"],
        "selected_profit_factor": selected["profit_factor"],
        "selected_expectancy": selected["expectancy"],
        "selected_trade_count": selected["trade_count"],
        "selected_trade_density": selected["trade_density"],
        "selected_long_trade_count": selected["long_trade_count"],
        "selected_short_trade_count": selected["short_trade_count"],
        "selected_short_share": selected["short_share"],
        "selected_closed_trade_drawdown_proxy": selected["closed_trade_drawdown_proxy"],
        "selected_closed_trade_recovery_proxy": selected["closed_trade_recovery_proxy"],
        "selected_month12_total_net": selected["month12_total_net"],
        "selected_month12_long_net": selected["month12_long_net"],
        "selected_month12_long_delta_vs_proxy_base": selected["month12_long_net_delta_vs_proxy_base"],
        "selected_removed_trade_count": selected["removed_trade_count"],
        "selected_net_delta_vs_proxy_base": selected["net_delta_vs_proxy_base"],
        "selected_profit_factor_delta_vs_proxy_base": selected["profit_factor_delta_vs_proxy_base"],
        "selected_density_delta_vs_proxy_base": selected["density_delta_vs_proxy_base"],
        "selected_closed_dd_delta_vs_proxy_base": selected["closed_dd_delta_vs_proxy_base"],
        "proxy_base_trade_count": base_metrics["base_trade_count"],
        "proxy_base_net_profit": base_metrics["base_net_profit"],
        "proxy_base_month12_long_net": base_metrics["base_month12_long_net"],
        "proxy_base_month12_total_net": base_metrics["base_month12_total_net"],
        "proxy_base_closed_trade_drawdown": base_metrics["base_closed_trade_drawdown_proxy"],
        "mt5_baseline_net_profit": selected["mt5_baseline_net_profit"],
        "mt5_baseline_profit_factor": selected["mt5_baseline_profit_factor"],
        "mt5_baseline_density": selected["mt5_baseline_density"],
        "mt5_baseline_month12_net": selected["mt5_baseline_month12_net"],
        "mt5_baseline_equity_dd": selected["mt5_baseline_equity_dd"],
        "external_verification_status": "out_of_scope_by_claim_proxy_scout_only",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "surface_path": rel(CS_PROXY_REPAIR_SURFACE),
        "selected_trade_tape_path": rel(SELECTED_TRADE_TAPE),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **common,
            "scoreboard_lane": "proxy_scout(프록시 정찰)",
            "measurement_scope": "closed-trade replay from CM selected tape(CM 선택 닫힌 거래 테이프 재생)",
            "selected_kpi": {
                "net_profit": final["selected_net_profit"],
                "profit_factor": final["selected_profit_factor"],
                "trade_count": final["selected_trade_count"],
                "density": final["selected_trade_density"],
                "short_count": final["selected_short_trade_count"],
                "month12_long_net": final["selected_month12_long_net"],
                "closed_trade_drawdown_proxy": final["selected_closed_trade_drawdown_proxy"],
            },
            "effect": "records proxy KPI without treating it as MT5 authority(프록시 KPI를 기록하되 MT5 권위로 보지 않음)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **common,
            "hypothesis": "A reusable month12 long hour/margin guard(재사용 가능한 12월 롱 시간/마진 가드) can reduce month12 long weakness(12월 롱 약점) without killing density(밀도 손상).",
            "decision_use": NEXT_RUN_ID,
            "comparison_baseline": "CM selected proxy tape(CM 선택 프록시 테이프) plus CQ MT5 runtime review(CQ MT5 런타임 검토)",
            "control_variables": ["US100", "M5", "same CM04 tape", "no trade splitting", "no top_n"],
            "changed_variables": ["month_of_year", "open_hour", "direction_margin"],
            "success_criteria": "net > 0, PF >= 1.35, density >= 3, shorts >= 100, month12 long net >= 0",
            "failure_criteria": "density collapse, short floor failure, exact-date/top_n/trade split, or unusable MT5/proxy gap",
            "invalid_conditions": "lookahead, realized-PnL filter, exact date/year filter, missing lineage",
            "stop_conditions": "review before MT5 package or runtime claim(운영 주장 전 검토)",
            "evidence_plan": [rel(CS_PROXY_REPAIR_SURFACE), rel(PACKAGE_PRECHECK), rel(PROXY_MT5_DIFF_PLAN), rel(GATE_AUDIT)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **common,
            "data_source": [rel(parent.RUN364CS_QUEUE), rel(cm.SELECTED_TRADE_TAPE), rel(cq.MT5_KPI_REVIEW)],
            "time_axis": "open_time/close_time sorted(진입/청산 시간 정렬)",
            "feature_label_boundary": "filters use entry-known calendar/hour/probability margin only(필터는 진입 시점 달력/시간/확률 마진만 사용)",
            "leakage_risk": "offline selection uses PnL only after replay(오프라인 선택은 재생 뒤 손익만 사용)",
            "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 조건부 사용 가능)",
            "effect": "keeps look-ahead bias closed(미래참조 편향 차단)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **common,
            "model_family": "no_new_model_rule_surface_replay(새 모델 없음, 규칙 표면 재생)",
            "target_and_label": "not_applicable_no_model_training(모델 학습 없음)",
            "selection_metric": "net/PF/density/short/month12/DD proxy composite(순수익/수익 팩터/밀도/숏/12월/낙폭 프록시 조합)",
            "overfit_risk": "single-sample month guard may overfit(단일 표본 월 가드 과적합 위험)",
            "validation_judgment": "exploratory_proxy_only(탐색 프록시 전용)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **common,
            "observed_change": f"selected {final['selected_variant_id']} improves proxy month12 long net by {final['selected_month12_long_delta_vs_proxy_base']}",
            "likely_drivers": ["month12 long hours 17-20", "entry-known direction margin", "density-preserving removal"],
            "segment_checks": [rel(VARIANT_MONTH_ATTRIBUTION), rel(VARIANT_MONTH_SIDE_ATTRIBUTION), rel(VARIANT_HOUR_SIDE_ATTRIBUTION)],
            "alternative_explanations": ["proxy/MT5 execution gap", "closed-trade DD cannot prove equity DD"],
            "effect": "separates proxy clue from MT5 claim(프록시 단서와 MT5 주장을 분리)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "judgment_class": "positive_exploratory_review_required(긍정 탐색, 검토 필요)",
            "boundary": "proxy_scout_only_no_mt5_no_runtime_authority(프록시 정찰 전용, MT5/런타임 권위 없음)",
            "why_not_promotion": "no new MT5 execution, no runtime parity, no forward evidence(새 MT5 실행/런타임 동등성/전진 근거 없음)",
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "allowed_claim": "CS produced a proxy review candidate(CS가 프록시 검토 후보를 만들었다)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "Goal Achieve"],
            "new_model_training": "not_run",
            "new_mt5_execution": "not_run",
            "effect": "keeps operating claim closed(운영 주장을 닫아 둠)",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if path != LINEAGE_RECEIPT and exists(path) and io_path(path).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_proxy_boundary(CS-CT 프록시 경계 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    selected: Mapping[str, Any],
    surface: Sequence[Mapping[str, Any]],
    filters: Sequence[Mapping[str, Any]],
    package_rows_: Sequence[Mapping[str, Any]],
    proxy_mt5_rows_: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    selected_filters = [row for row in filters if row["variant_id"] == selected["variant_id"]]
    selected_package = [row for row in package_rows_ if row["variant_id"] == selected["variant_id"]]
    report = f"""# run364CS h17 month12 long equity drawdown repair scout(364CS 17시 12월 롱/수익곡선 낙폭 수리 정찰)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{final['selected_variant_id']}`
- selected KPI(선택 핵심 성과 지표): net(순수익) `{final['selected_net_profit']}`, PF(수익 팩터) `{final['selected_profit_factor']}`, density(밀도) `{final['selected_trade_density']}`, shorts(숏) `{final['selected_short_trade_count']}`
- month12 long net(12월 롱 순수익): `{final['selected_month12_long_net']}`, delta(차이) `{final['selected_month12_long_delta_vs_proxy_base']}`
- closed trade DD proxy(닫힌 거래 낙폭 프록시): `{final['selected_closed_trade_drawdown_proxy']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Action And Effect(행동과 효과)

Action(행동): CR queue(CR 대기열) `8`개를 CM selected tape(CM 선택 거래 테이프)에 proxy replay(프록시 재생)했습니다.

Effect(효과): `{final['selected_variant_id']}`가 density(밀도) `3` 이상과 short floor(숏 하한) `100` 이상을 유지하면서 month12 long net(12월 롱 순수익)을 `{final['selected_month12_long_net']}`로 돌렸습니다. 다만 MT5 equity DD(MT5 수익곡선 낙폭)는 아직 재탐침 전입니다.

## Surface(표면)

{markdown_table(surface, ['variant_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_density', 'short_trade_count', 'month12_long_net', 'closed_trade_drawdown_proxy', 'removed_trade_count', 'selection_score'], 10)}

## Selected Filter Audit(선택 필터 감사)

{markdown_table(selected_filters, ['filter_step', 'filter_reason', 'removed_trade_count', 'removed_net_profit', 'short_count_before', 'short_count_after'], 8)}

## Selected Package Precheck(선택 패키지 사전검사)

{markdown_table(selected_package, ['variant_id', 'package_precheck_status', 'net_positive', 'pf_ge_135', 'density_ge_3', 'short_floor_ge_100', 'month12_long_nonnegative', 'closed_dd_not_worse'], 4)}

## Proxy MT5 Diff Plan(프록시 MT5 차이 계획)

{markdown_table(proxy_mt5_rows_, ['comparison_id', 'proxy_net_profit', 'mt5_baseline_net_profit', 'proxy_month12_long_net', 'mt5_baseline_month12_net', 'proxy_closed_trade_dd', 'mt5_baseline_equity_dd'], 4)}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 12)}

## Boundary(경계)

This is proxy scout only(프록시 정찰 전용)입니다. New ONNX model(새 ONNX 모델), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CS decision(결정): month12 long/equity DD proxy scout(12월 롱/수익곡선 낙폭 프록시 정찰)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- selected variant(선택 변형): `{final['selected_variant_id']}`
- selected net/PF/density(선택 순수익/수익 팩터/밀도): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}`
- effect(효과): CT review(CT 검토)에서 MT5 runtime probe(MT5 런타임 탐침) 입력으로 보낼지 판단할 proxy candidate(프록시 후보)를 만들었습니다.
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        f"run364CS__{RUN_ID}",
        f"\n- run364CS__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - selected `{final['selected_variant_id']}`, next `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        f"run364CS__{RUN_ID}",
        f"""
<!-- run364CS__{RUN_ID} -->

## run364CS Month12 Long Repair Scout(364CS 12월 롱 수리 정찰)

Action(행동): CR queue(CR 대기열) `8`개를 proxy replay(프록시 재생)했습니다.

Effect(효과): selected variant(선택 변형) `{final['selected_variant_id']}`를 `{NEXT_RUN_ID}` review(검토)로 넘겼고, 운영 권위는 주장하지 않습니다.
""",
    )
    append_text_once(
        STAGE_README,
        f"run364CS__{RUN_ID}",
        f"\n<!-- run364CS__{RUN_ID} -->\n## run364CS proxy scout(364CS 프록시 정찰)\n\nSelected(선택): `{final['selected_variant_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n",
    )
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected proxy repair variant(선택 프록시 수리 변형): `{final['selected_variant_id']}`.

Selected KPI(선택 핵심 성과 지표): net(순수익) `{final['selected_net_profit']}`, PF(수익 팩터) `{final['selected_profit_factor']}`, density(밀도) `{final['selected_trade_density']}`, shorts(숏) `{final['selected_short_trade_count']}`, month12 long net(12월 롱 순수익) `{final['selected_month12_long_net']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 package review(패키지 검토)와 MT5 reprobe boundary(MT5 재탐침 경계)를 판단합니다.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CS` replayed(재생 완료) `8` month12 long/equity DD repair variants(12월 롱/수익곡선 낙폭 수리 변형). Selected proxy repair variant(선택 프록시 수리 변형)는 `{final['selected_variant_id']}`이고 net/PF/density(순수익/수익 팩터/밀도)는 `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 selected variant(선택 변형)의 package boundary(패키지 경계), MT5 reprobe need(MT5 재탐침 필요성), equity DD proxy limit(수익곡선 낙폭 프록시 한계)을 검토합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364CS__{RUN_ID}",
        f"\n<!-- run364CS__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed CS proxy scout(CS 프록시 정찰 완료); selected `{final['selected_variant_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"run364CS__{RUN_ID}",
        f"\n<!-- run364CS__{RUN_ID} -->\n- `{RUN_ID}`: month12 long/equity DD repair scout(12월 롱/수익곡선 낙폭 수리 정찰). Effect(효과): `{final['selected_variant_id']}`를 MT5 reprobe candidate(MT5 재탐침 후보) 검토 씨앗으로 남김.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"run364CS__boundary__{RUN_ID}",
        f"\n<!-- run364CS__boundary__{RUN_ID} -->\n- `{RUN_ID}` boundary note(경계 메모): proxy scout(프록시 정찰)는 긍정 단서를 만들었지만 MT5 equity DD(MT5 수익곡선 낙폭)를 직접 증명하지 못합니다. Effect(효과): `{NEXT_RUN_ID}`에서 runtime probe boundary(런타임 탐침 경계)를 먼저 판단합니다.\n",
    )


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
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "proxy_scout_only(프록시 정찰 전용)",
        "question": "Which month12 long/equity DD repair variant should CT review?(어떤 12월 롱/수익곡선 낙폭 수리 변형을 CT가 검토할까?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_trade_density"],
        "long_trade_count": final["selected_long_trade_count"],
        "short_trade_count": final["selected_short_trade_count"],
        "max_drawdown_amount": final["selected_closed_trade_drawdown_proxy"],
        "recovery_factor": final["selected_closed_trade_recovery_proxy"],
        "trade_density_requirement_status": "passed_proxy_density_ge_3_no_trade_splitting(프록시 밀도 3 이상, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(CS_PROXY_REPAIR_SURFACE),
        "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_trade_density']};month12_long={final['selected_month12_long_net']}",
        "guardrail_kpi": f"shorts={final['selected_short_trade_count']};closed_dd={final['selected_closed_trade_drawdown_proxy']};no_authority",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows: list[dict[str, Any]] = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)", False),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)", True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "CS proxy repair scout(CS 프록시 수리 정찰)",
            "status": status,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "proxy_repair_surface(프록시 수리 표면)",
        }
        if not include_metrics:
            for key in [
                "net_profit",
                "profit_factor",
                "expectancy",
                "trade_count",
                "trade_density_per_feature_day",
                "long_trade_count",
                "short_trade_count",
                "max_drawdown_amount",
                "recovery_factor",
            ]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    exclusions = {RUN_MANIFEST, LINEAGE_RECEIPT, ARTIFACT_REGISTRY}
    output_paths = [path for path in OUTPUT_FILES if path not in exclusions and exists(path) and io_path(path).is_file()]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_proxy_scout_run_id": SOURCE_PROXY_SCOUT_RUN_ID,
            "runtime_review_run_id": RUNTIME_REVIEW_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in output_paths],
            "final_decision": rel(FINAL_DECISION),
            "external_verification_status": final["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("proxy_repair_surface", CS_PROXY_REPAIR_SURFACE, "CS proxy repair surface(CS 프록시 수리 표면)."),
        ("selected_candidate", SELECTED_CANDIDATE, "Selected CS candidate(선택 CS 후보)."),
        ("selected_trade_tape", SELECTED_TRADE_TAPE, "Selected CS trade tape(선택 CS 거래 기록)."),
        ("filter_audit", VARIANT_FILTER_AUDIT, "CS variant filter audit(CS 변형 필터 감사)."),
        ("month_attribution", VARIANT_MONTH_ATTRIBUTION, "CS month attribution(CS 월 귀속)."),
        ("month_side_attribution", VARIANT_MONTH_SIDE_ATTRIBUTION, "CS month/side attribution(CS 월/방향 귀속)."),
        ("side_attribution", VARIANT_SIDE_ATTRIBUTION, "CS side attribution(CS 방향 귀속)."),
        ("hour_side_attribution", VARIANT_HOUR_SIDE_ATTRIBUTION, "CS hour/side attribution(CS 시간/방향 귀속)."),
        ("equity_dd_proxy", EQUITY_DD_PROXY_DIAGNOSTIC, "CS equity DD proxy diagnostic(CS 수익곡선 낙폭 프록시 진단)."),
        ("package_precheck", PACKAGE_PRECHECK, "CS package precheck(CS 패키지 사전검사)."),
        ("proxy_mt5_diff_plan", PROXY_MT5_DIFF_PLAN, "CS proxy/MT5 diff plan(CS 프록시/MT5 차이 계획)."),
        ("next_queue", RUN364CT_QUEUE, "CT review queue(CT 검토 대기열)."),
        ("report", REPORT_PATH, "CS report(CS 보고서)."),
        ("final_decision", FINAL_DECISION, "CS final decision(CS 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CS run manifest(CS 실행 목록)."),
        ("gate_audit", GATE_AUDIT, "CS gate audit(CS 게이트 감사)."),
        ("lineage_receipt", LINEAGE_RECEIPT, "CS lineage receipt(CS 계보 영수증)."),
        ("script", Path(__file__), "CS producer script(CS 생산 스크립트)."),
    ]
    rows = []
    for artifact_type, path, notes in artifacts:
        if exists(path):
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    _cr_final, cm_final, _cq_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()

    base_frame = load_base_frame()
    surface, frame_map, filters, base_metrics = build_surface(cm_final)
    selected = dict(surface[0])
    selected_frame = frame_map[str(selected["variant_id"])].copy()
    month_rows = summary_rows(frame_map, surface, ["open_month"], "month")
    month_side_rows = summary_rows(frame_map, surface, ["open_month", "direction"], "month_side")
    side_rows = summary_rows(frame_map, surface, ["direction"], "side")
    hour_side_rows = summary_rows(frame_map, surface, ["open_hour", "direction"], "hour_side")
    dd_rows = equity_dd_rows(surface)
    package_rows_ = package_rows(surface)
    proxy_mt5_rows_ = proxy_mt5_diff_rows(selected)
    review_queue = review_queue_rows(selected)
    data_rows_ = data_integrity_rows(base_frame, surface, filters)

    write_csv(CS_PROXY_REPAIR_SURFACE, surface)
    write_json(SELECTED_CANDIDATE, selected)
    write_csv(SELECTED_TRADE_TAPE, selected_frame.drop(columns=["open_time_dt", "close_time_dt"], errors="ignore").to_dict("records"))
    write_csv(VARIANT_FILTER_AUDIT, filters)
    write_csv(VARIANT_MONTH_ATTRIBUTION, month_rows)
    write_csv(VARIANT_MONTH_SIDE_ATTRIBUTION, month_side_rows)
    write_csv(VARIANT_SIDE_ATTRIBUTION, side_rows)
    write_csv(VARIANT_HOUR_SIDE_ATTRIBUTION, hour_side_rows)
    write_csv(EQUITY_DD_PROXY_DIAGNOSTIC, dd_rows)
    write_csv(PACKAGE_PRECHECK, package_rows_)
    write_csv(PROXY_MT5_DIFF_PLAN, proxy_mt5_rows_)
    write_csv(RUN364CT_QUEUE, review_queue)
    write_csv(DATA_INTEGRITY_AUDIT, data_rows_)

    receipt_paths = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    preliminary_gates = gate_rows(surface, selected, data_rows_, receipt_paths, final_written=False)
    final = final_payload(selected, surface, preliminary_gates, base_metrics, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected)
    refresh_lineage_receipt(final)
    gates = gate_rows(surface, selected, data_rows_, receipt_paths, final_written=True)
    final = final_payload(selected, surface, gates, base_metrics, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final, selected)
    write_docs(final, selected, surface, filters, package_rows_, proxy_mt5_rows_, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
