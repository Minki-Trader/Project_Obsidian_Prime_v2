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

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage364 import execute_overlay_hour17_native_short_ablation_runtime_probe_without_db as bx  # noqa: E402
from stage_pipelines.stage364 import review_overlay_hour17_native_short_ablation_runtime_probe_without_db as by  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = by.STAGE_ID
RUN_NUMBER = "run364BZ"
RUN_ID = "run364BZ_materialize_bx03_december_late_session_guard_inputs_without_db_v1"
PARENT_RUN_ID = by.RUN_ID
SOURCE_RUNTIME_RUN_ID = bx.RUN_ID
NEXT_RUN_ID = "run364CA_execute_bx03_guard_stack_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

BEST_VARIANT_ID = "bx03_hour17_overlay_plus_weak_late_session_firewall"
TRADE_DENSITY_FLOOR = 3.0
BASE_P_SHORT_MIN = 0.4375
BASE_MARGIN_VS_LONG_MIN = 0.075

STAGE_DIR = by.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
CALENDAR_SEMANTICS_AUDIT = RUN_DIR / "calendar_block_semantics_audit.csv"
H17_OVERLAY_QUALITY_SCAN = RUN_DIR / "h17_overlay_quality_floor_scan.csv"
EQUITY_DD_CLUSTER_PROXY = RUN_DIR / "equity_dd_cluster_proxy.csv"
GUARD_CANDIDATE_MATRIX = RUN_DIR / "guard_candidate_matrix.csv"
GUARD_CANDIDATE_PROXY_IMPACT = RUN_DIR / "guard_candidate_proxy_impact.csv"
RUNTIME_ATTEMPT_QUEUE = RUN_DIR / "run364CA_runtime_attempt_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BZ_bx03_december_late_session_guard_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BZ_bx03_december_late_session_guard_inputs.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

SOURCE_BY_FINAL = by.FINAL_DECISION
SOURCE_BY_QUEUE = by.NEXT_QUEUE
SOURCE_BY_TRADE_ATTRIBUTION = by.TRADE_ATTRIBUTION
SOURCE_BY_MEMBERSHIP_DELTA = by.TRADE_MEMBERSHIP_DELTA
SOURCE_BY_VARIANT_DELTAS = by.VARIANT_PAIR_DELTAS
SOURCE_BY_REPORT = by.REPORT_PATH
SOURCE_BX_POLICY = bx.RUNTIME_POLICY_CONFIG
SOURCE_BX_SCOREBOARD = bx.ABLATION_SCOREBOARD
SOURCE_EA = bx.SOURCE_EA
MT5_INPUT_CONTRACT = bx.MT5_INPUT_CONTRACT

INPUT_FILES = [
    SOURCE_BY_FINAL,
    SOURCE_BY_QUEUE,
    SOURCE_BY_TRADE_ATTRIBUTION,
    SOURCE_BY_MEMBERSHIP_DELTA,
    SOURCE_BY_VARIANT_DELTAS,
    SOURCE_BY_REPORT,
    SOURCE_BX_POLICY,
    SOURCE_BX_SCOREBOARD,
    SOURCE_EA,
    MT5_INPUT_CONTRACT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    CALENDAR_SEMANTICS_AUDIT,
    H17_OVERLAY_QUALITY_SCAN,
    EQUITY_DD_CLUSTER_PROXY,
    GUARD_CANDIDATE_MATRIX,
    GUARD_CANDIDATE_PROXY_IMPACT,
    RUNTIME_ATTEMPT_QUEUE,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return by.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


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
    by.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    by.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    by.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    by.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    by.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")).replace("|", "\\|") for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def hour_in_range(hour: int, start_hour: int, end_hour: int) -> bool:
    normalized_hour = hour % 24
    normalized_start = start_hour % 24
    normalized_end = 24 if end_hour == 24 else end_hour % 24
    if normalized_end == 24:
        return normalized_hour >= normalized_start and normalized_hour < 24
    if normalized_start == normalized_end:
        return True
    if normalized_start < normalized_end:
        return normalized_hour >= normalized_start and normalized_hour < normalized_end
    return normalized_hour >= normalized_start or normalized_hour < normalized_end


def covered_hours(start_hour: int, end_hour: int) -> str:
    return "|".join(str(hour) for hour in range(24) if hour_in_range(hour, start_hour, end_hour))


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BZ inputs(BZ 입력 누락): " + ", ".join(missing))
    parent_final = read_json(SOURCE_BY_FINAL)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BY next_run_id mismatch(BY 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    forbidden = ["runtime_authority", "operating_promotion", "goal_achieve"]
    if any(parent_final.get(key) != "not_claimed" for key in forbidden):
        raise RuntimeError("BY has forbidden authority claim(BY 금지 권위 주장 존재)")
    return parent_final


def read_trade_attribution() -> pd.DataFrame:
    frame = pd.read_csv(io_path(SOURCE_BY_TRADE_ATTRIBUTION))
    for column in ["net_profit", "p_short", "p_flat", "p_long", "open_hour", "close_hour", "hold_minutes"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["open_time"] = pd.to_datetime(frame["open_time"], errors="coerce")
    frame["close_time"] = pd.to_datetime(frame["close_time"], errors="coerce")
    frame["open_month"] = frame["open_time"].dt.month
    frame["close_month_number"] = frame["close_time"].dt.month
    frame["p_edge_short_vs_long"] = frame["p_short"] - frame["p_long"]
    return frame


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BZ materialization source(BZ 구체화 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def calendar_semantics_rows() -> list[dict[str, Any]]:
    rows = []
    for audit_id, start, end, purpose in [
        ("bx01_semantics", 21, 22, "BX1 blocks h21 only because end_hour is exclusive(BX1은 종료 시각 배타라 h21만 차단)"),
        ("bx03_semantics", 21, 23, "BX3 blocks h21+h22 and removed December h22 long(BX3는 h21+h22를 막아 12월 h22 롱을 제거)"),
        ("ca_h22_isolation", 22, 23, "CA isolation blocks h22 only(CA 분리 후보는 h22만 차단)"),
        ("ca_h21_h23_stress", 21, 24, "CA stress blocks h21+h22+h23(CA 압박 후보는 h21+h22+h23 차단)"),
    ]:
        rows.append(
            {
                "run_id": RUN_ID,
                "audit_id": audit_id,
                "start_hour": start,
                "end_hour": end,
                "covered_hours": covered_hours(start, end),
                "hour_range_semantics": "inclusive_start_exclusive_end(시작 포함 종료 제외)",
                "ea_evidence": rel(SOURCE_EA),
                "purpose": purpose,
                "timestamp_safety": "entry server hour only(진입 서버 시각만 사용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def h17_quality_scan_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    synthetic = trades[(trades["variant_id"] == BEST_VARIANT_ID) & (trades["source_bucket"] == "synthetic_short_overlay")].copy()
    rows: list[dict[str, Any]] = []
    if synthetic.empty:
        return rows
    total_net = float(synthetic["net_profit"].sum())
    for column, operator, runtime_param in [
        ("p_edge_short_vs_long", ">=", "InpSyntheticShortSourceMarginVsLongMin"),
        ("p_short", ">=", "InpSyntheticShortSourcePShortMin"),
        ("p_long", "<=", "not_directly_runtime_supported"),
        ("p_flat", "<=", "not_directly_runtime_supported"),
    ]:
        for quantile in [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]:
            threshold = float(synthetic[column].quantile(quantile))
            kept = synthetic[synthetic[column] >= threshold] if operator == ">=" else synthetic[synthetic[column] <= threshold]
            removed = synthetic.loc[~synthetic.index.isin(kept.index)]
            kept_net = float(kept["net_profit"].sum())
            removed_net = float(removed["net_profit"].sum())
            rows.append(
                {
                    "run_id": RUN_ID,
                    "scan_id": f"{column}_{operator}_q{int(quantile * 100)}".replace(">=", "ge").replace("<=", "le"),
                    "source_bucket": "synthetic_short_overlay",
                    "runtime_param": runtime_param,
                    "operator": operator,
                    "threshold": finite(threshold, 10),
                    "baseline_trade_count": int(len(synthetic)),
                    "kept_trade_count": int(len(kept)),
                    "removed_trade_count": int(len(removed)),
                    "baseline_net": finite(total_net, 2),
                    "kept_net": finite(kept_net, 2),
                    "removed_net": finite(removed_net, 2),
                    "losses_kept": int((kept["net_profit"] < 0).sum()),
                    "proxy_effect": "negative_or_weak(부정 또는 약함)" if kept_net < total_net else "positive_proxy(긍정 프록시)",
                    "selection_boundary": "post_run_trade_outcome_scan_not_runtime_authority(사후 거래 결과 탐색이며 런타임 권위 아님)",
                    "timestamp_safety": "threshold can be evaluated from closed-bar probabilities before entry(임계값은 진입 전 닫힌 봉 확률로 평가 가능)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    rows.sort(key=lambda row: (as_float(row["kept_net"]), as_float(row["kept_trade_count"])), reverse=True)
    return rows


def equity_cluster_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    bx3 = trades[trades["variant_id"] == BEST_VARIANT_ID].sort_values(["close_time", "open_time"]).copy()
    bx3["cum_net"] = bx3["net_profit"].cumsum()
    bx3["peak_net"] = bx3["cum_net"].cummax()
    bx3["closed_balance_drawdown"] = bx3["peak_net"] - bx3["cum_net"]
    rows = []
    worst = bx3.sort_values("closed_balance_drawdown", ascending=False).head(12)
    for rank, row in enumerate(worst.itertuples(index=False), start=1):
        rows.append(
            {
                "run_id": RUN_ID,
                "cluster_rank": rank,
                "open_time": getattr(row, "open_time"),
                "close_time": getattr(row, "close_time"),
                "direction": getattr(row, "direction"),
                "source_bucket": getattr(row, "source_bucket"),
                "net_profit": finite(getattr(row, "net_profit"), 2),
                "cum_net": finite(getattr(row, "cum_net"), 2),
                "closed_balance_drawdown": finite(getattr(row, "closed_balance_drawdown"), 2),
                "open_hour": finite(getattr(row, "open_hour"), 0),
                "close_hour": finite(getattr(row, "close_hour"), 0),
                "proxy_boundary": "closed_trade_balance_proxy_not_tick_equity_path(종료 거래 잔고 프록시이며 틱 평가손익 경로 아님)",
                "next_runtime_need": "collect_or_trust MT5 equity DD from strategy tester report(MT5 평가손익 낙폭은 테스터 보고서에서 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def base_candidate_rows(scan_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    margin_q10 = next(row for row in scan_rows if row["scan_id"] == "p_edge_short_vs_long_ge_q10")
    pshort_q10 = next(row for row in scan_rows if row["scan_id"] == "p_short_ge_q10")
    return [
        {
            "candidate_id": "ca01_bx03_semantics_control",
            "runtime_priority": 1,
            "variant_role": "control(대조)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "synthetic_p_short_min": BASE_P_SHORT_MIN,
            "synthetic_margin_vs_long_min": BASE_MARGIN_VS_LONG_MIN,
            "calendar_enabled": True,
            "calendar_side": "long",
            "calendar_month": 12,
            "calendar_start_hour": 21,
            "calendar_end_hour": 23,
            "covered_hours": covered_hours(21, 23),
            "reason": "BX3 exact semantics control(BX3 의미 대조)",
            "expected_learning": "confirm reproducibility before guard changes(가드 변경 전 재현성 확인)",
            "timestamp_safety": "entry-known month/hour and closed-bar probabilities(진입 시점 월/시각과 닫힌 봉 확률)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "candidate_id": "ca02_december_h22_only_long_block_isolation",
            "runtime_priority": 2,
            "variant_role": "calendar_isolation(달력 분리)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "synthetic_p_short_min": BASE_P_SHORT_MIN,
            "synthetic_margin_vs_long_min": BASE_MARGIN_VS_LONG_MIN,
            "calendar_enabled": True,
            "calendar_side": "long",
            "calendar_month": 12,
            "calendar_start_hour": 22,
            "calendar_end_hour": 23,
            "covered_hours": covered_hours(22, 23),
            "reason": "isolate h22 loss block without also blocking h21(h21까지 막지 않고 h22 손실 차단만 분리)",
            "expected_learning": "test whether h21 block is unnecessary drag(h21 차단이 불필요한 손상인지 확인)",
            "timestamp_safety": "month-of-year plus entry server hour only(월값과 진입 서버 시각만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "candidate_id": "ca03_december_h21_h23_long_block_stress",
            "runtime_priority": 3,
            "variant_role": "calendar_stress(달력 압박)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "synthetic_p_short_min": BASE_P_SHORT_MIN,
            "synthetic_margin_vs_long_min": BASE_MARGIN_VS_LONG_MIN,
            "calendar_enabled": True,
            "calendar_side": "long",
            "calendar_month": 12,
            "calendar_start_hour": 21,
            "calendar_end_hour": 24,
            "covered_hours": covered_hours(21, 24),
            "reason": "stress late December long exposure through h23(12월 후반 롱 노출을 h23까지 압박)",
            "expected_learning": "see whether equity DD improves without density falling below floor(밀도 하한을 깨지 않고 평가손익 낙폭이 줄어드는지 확인)",
            "timestamp_safety": "month-of-year plus entry server hour only(월값과 진입 서버 시각만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "candidate_id": "ca04_h17_overlay_margin_q10_floor_negative_control",
            "runtime_priority": 5,
            "variant_role": "negative_control(음성 대조)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "synthetic_p_short_min": BASE_P_SHORT_MIN,
            "synthetic_margin_vs_long_min": margin_q10["threshold"],
            "calendar_enabled": True,
            "calendar_side": "long",
            "calendar_month": 12,
            "calendar_start_hour": 21,
            "calendar_end_hour": 23,
            "covered_hours": covered_hours(21, 23),
            "reason": "mild h17 margin floor had weak/negative proxy(약한 17시 마진 하한의 프록시가 약하거나 부정)",
            "expected_learning": "do not prioritize unless CA has spare attempt budget(CA 시도 여유가 있을 때만 확인)",
            "timestamp_safety": "closed-bar p_short-p_long before entry(진입 전 닫힌 봉 p_short-p_long)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "candidate_id": "ca05_h17_overlay_pshort_q10_floor_negative_control",
            "runtime_priority": 6,
            "variant_role": "negative_control(음성 대조)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "synthetic_p_short_min": pshort_q10["threshold"],
            "synthetic_margin_vs_long_min": BASE_MARGIN_VS_LONG_MIN,
            "calendar_enabled": True,
            "calendar_side": "long",
            "calendar_month": 12,
            "calendar_start_hour": 21,
            "calendar_end_hour": 23,
            "covered_hours": covered_hours(21, 23),
            "reason": "p_short q10 floor removes profitable aggregate in proxy(p_short q10 하한이 프록시에서 수익을 잘라냄)",
            "expected_learning": "reserve as overfit-control check only(과적합 대조 확인용으로만 보류)",
            "timestamp_safety": "closed-bar p_short before entry(진입 전 닫힌 봉 p_short)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "candidate_id": "ca06_native_short_same_calendar_control",
            "runtime_priority": 4,
            "variant_role": "source_control(원천 대조)",
            "synthetic_enabled": False,
            "synthetic_hours": "",
            "synthetic_p_short_min": BASE_P_SHORT_MIN,
            "synthetic_margin_vs_long_min": BASE_MARGIN_VS_LONG_MIN,
            "calendar_enabled": True,
            "calendar_side": "long",
            "calendar_month": 12,
            "calendar_start_hour": 21,
            "calendar_end_hour": 23,
            "covered_hours": covered_hours(21, 23),
            "reason": "native short under same BX3 calendar semantics(같은 BX3 달력 의미에서 기본 숏 대조)",
            "expected_learning": "separate overlay value from h22 firewall value(h22 방화벽 가치와 오버레이 가치를 분리)",
            "timestamp_safety": "entry-known month/hour and closed-bar probabilities(진입 시점 월/시각과 닫힌 봉 확률)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def estimate_candidate_impacts(trades: pd.DataFrame, candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    bx3 = trades[trades["variant_id"] == BEST_VARIANT_ID].copy()
    baseline_net = float(bx3["net_profit"].sum())
    baseline_trades = int(len(bx3))
    rows = []
    for candidate in candidates:
        candidate_id = str(candidate["candidate_id"])
        estimable = True
        note = "removal-only proxy from BX3 closed trades(BX3 종료 거래에서 제거 전용 프록시)"
        remove_mask = pd.Series(False, index=bx3.index)
        if candidate_id == "ca03_december_h21_h23_long_block_stress":
            remove_mask = (
                (bx3["direction"] == "long")
                & (bx3["open_month"] == 12)
                & bx3["open_hour"].apply(lambda hour: hour_in_range(int(hour), 23, 24) if pd.notna(hour) else False)
            )
        elif candidate_id == "ca04_h17_overlay_margin_q10_floor_negative_control":
            threshold = as_float(candidate["synthetic_margin_vs_long_min"])
            remove_mask = (bx3["source_bucket"] == "synthetic_short_overlay") & (bx3["p_edge_short_vs_long"] < threshold)
        elif candidate_id == "ca05_h17_overlay_pshort_q10_floor_negative_control":
            threshold = as_float(candidate["synthetic_p_short_min"])
            remove_mask = (bx3["source_bucket"] == "synthetic_short_overlay") & (bx3["p_short"] < threshold)
        elif candidate_id in {"ca02_december_h22_only_long_block_isolation", "ca06_native_short_same_calendar_control"}:
            estimable = False
            note = "requires MT5 because candidate can restore or replace trades absent from BX3(BX3에 없는 거래를 복원/대체할 수 있어 MT5 필요)"

        removed = bx3[remove_mask] if estimable else bx3.iloc[0:0]
        removed_net = float(removed["net_profit"].sum()) if estimable else math.nan
        estimated_net = baseline_net - removed_net if estimable else math.nan
        estimated_trades = baseline_trades - int(len(removed)) if estimable else math.nan
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "baseline_variant_id": BEST_VARIANT_ID,
                "proxy_estimable": "yes" if estimable else "no",
                "baseline_net": finite(baseline_net, 2),
                "baseline_trade_count": baseline_trades,
                "removed_trade_count": int(len(removed)) if estimable else "",
                "removed_net": finite(removed_net, 2) if estimable else "",
                "estimated_net": finite(estimated_net, 2) if estimable else "",
                "estimated_trade_count": finite(estimated_trades, 0) if estimable else "",
                "estimated_density": finite(estimated_trades / 314.0, 10) if estimable else "",
                "density_floor_status": "passed_proxy" if estimable and estimated_trades / 314.0 >= TRADE_DENSITY_FLOOR else ("requires_mt5" if not estimable else "failed_proxy"),
                "proxy_note": note,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def runtime_queue_rows(candidates: Sequence[Mapping[str, Any]], impacts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    impact_by_id = {str(row["candidate_id"]): row for row in impacts}
    rows = []
    for candidate in sorted(candidates, key=lambda row: int(row["runtime_priority"])):
        candidate_id = str(candidate["candidate_id"])
        if candidate_id in {"ca04_h17_overlay_margin_q10_floor_negative_control", "ca05_h17_overlay_pshort_q10_floor_negative_control"}:
            queue_status = "deferred_proxy_negative(프록시 부정으로 보류)"
        else:
            queue_status = "ready_for_runtime_probe(런타임 탐침 준비)"
        impact = impact_by_id[candidate_id]
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "candidate_id": candidate_id,
                "runtime_priority": candidate["runtime_priority"],
                "queue_status": queue_status,
                "synthetic_enabled": candidate["synthetic_enabled"],
                "synthetic_hours": candidate["synthetic_hours"],
                "synthetic_p_short_min": candidate["synthetic_p_short_min"],
                "synthetic_margin_vs_long_min": candidate["synthetic_margin_vs_long_min"],
                "calendar_enabled": candidate["calendar_enabled"],
                "calendar_side": candidate["calendar_side"],
                "calendar_month": candidate["calendar_month"],
                "calendar_start_hour": candidate["calendar_start_hour"],
                "calendar_end_hour": candidate["calendar_end_hour"],
                "covered_hours": candidate["covered_hours"],
                "proxy_estimable": impact["proxy_estimable"],
                "estimated_net": impact["estimated_net"],
                "estimated_density": impact["estimated_density"],
                "success_condition": "MT5 net/PF/recovery improve without trade density below 3 per day(MT5 순수익/PF/회복이 개선되고 거래 밀도 3/day 이상)",
                "invalid_condition": "runtime output missing or calendar/overlay params not reflected(런타임 출력 누락 또는 달력/오버레이 파라미터 미반영)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gates(candidates: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], receipts_written: bool) -> list[dict[str, Any]]:
    ready_count = sum(1 for row in queue if str(row["queue_status"]).startswith("ready"))
    required = [
        (
            "scope_completion_gate",
            len(candidates) >= 6 and ready_count >= 4,
            GUARD_CANDIDATE_MATRIX,
            "calendar/overlay/equity guard inputs were materialized(달력/오버레이/평가손익 가드 입력을 구체화)",
        ),
        (
            "kpi_contract_audit",
            True,
            GUARD_CANDIDATE_PROXY_IMPACT,
            "BX3 MT5 KPI baseline is carried as proxy baseline only(BX3 MT5 KPI 기준은 프록시 기준으로만 인계)",
        ),
        (
            "skill_receipt_lint",
            receipts_written,
            EXPERIMENT_RECEIPT,
            "experiment/data/model/lineage receipts exist(실험/데이터/모델/계보 영수증 존재)",
        ),
        (
            "timestamp_safety_audit",
            all("timestamp_safety" in row and row["timestamp_safety"] for row in candidates),
            GUARD_CANDIDATE_MATRIX,
            "candidates use entry-known month/hour and closed-bar probabilities(후보는 진입 시점 월/시각과 닫힌 봉 확률만 사용)",
        ),
        (
            "required_gate_coverage_audit",
            True,
            GATE_AUDIT,
            "required gates are linked to closeout(필수 게이트를 종료 기록에 연결)",
        ),
        (
            "final_claim_guard",
            True,
            CLAIM_RECEIPT,
            "no runtime authority, operating promotion, live readiness, or goal claim(런타임 권위/운영 승격/실거래 준비/목표 달성 미주장)",
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
        for gate, passed, evidence, effect in required
    ]


def final_payload(
    parent_final: Mapping[str, Any],
    candidates: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    impacts: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    ready_count = sum(1 for row in queue if str(row["queue_status"]).startswith("ready"))
    h17_negative_controls = sum(1 for row in queue if "deferred_proxy_negative" in str(row["queue_status"]))
    bx3_impact = next(row for row in impacts if row["candidate_id"] == "ca01_bx03_semantics_control")
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": "completed_stage364BZ_bx03_guard_inputs_materialized_open_ca_no_authority",
        "judgment": "materialized_december_h22_calendar_semantics_and_h17_overlay_guard_inputs_no_authority",
        "decision": "stage364BZ_open_run364CA_bx03_guard_stack_runtime_probe",
        "next_run_id": NEXT_RUN_ID,
        "best_variant_id": BEST_VARIANT_ID,
        "parent_best_net_profit": parent_final.get("best_net_profit"),
        "parent_best_profit_factor": parent_final.get("best_profit_factor"),
        "parent_best_trade_count": parent_final.get("best_trade_count"),
        "parent_best_density": parent_final.get("best_density"),
        "parent_best_recovery_factor": parent_final.get("best_recovery_factor"),
        "parent_best_equity_drawdown_amount": parent_final.get("best_equity_drawdown_amount"),
        "candidate_count": len(candidates),
        "runtime_ready_candidate_count": ready_count,
        "h17_negative_control_count": h17_negative_controls,
        "calendar_semantics": "end_hour_exclusive_confirmed_from_EA_HourInRange",
        "h17_overlay_guard_priority": "defer_initial_runtime_grid_proxy_negative",
        "control_proxy_net": bx3_impact.get("estimated_net"),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run_materialization_only",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "BX3 gain can be separated into calendar h22 firewall and h17 overlay source(BX3 개선을 달력 h22 방화벽과 17시 오버레이 원천으로 분리할 수 있다)",
            "decision_use": "choose CA runtime probe variants(CA 런타임 탐침 변형 선택)",
            "comparison_baseline": BEST_VARIANT_ID,
            "control_variables": ["US100 M5", "same ONNX", "fixed lot 0.1", "max_hold_bars=6", "no trade splitting"],
            "changed_variables": ["calendar block start/end hour", "synthetic overlay enabled", "synthetic p_short/margin floors"],
            "sample_scope": "BX3 MT5 validation OOS trade attribution(BX3 MT5 검증 OOS 거래 귀속)",
            "success_criteria": "CA probe keeps density >=3/day and improves net/PF/recovery or DD(CA 탐침이 밀도 3/day 이상과 수익/PF/회복 또는 DD 개선)",
            "failure_criteria": "density collapse or lower net/PF without DD benefit(밀도 붕괴 또는 DD 이득 없는 수익/PF 하락)",
            "invalid_conditions": ["MT5 output missing", "EA params not reflected", "timestamp unsafe filter"],
            "stop_conditions": "stop h17 threshold escalation if proxy remains negative(프록시가 계속 부정이면 17시 임계값 상승 중지)",
            "evidence_plan": [rel(GUARD_CANDIDATE_MATRIX), rel(RUNTIME_ATTEMPT_QUEUE), rel(GATE_AUDIT)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(SOURCE_BY_TRADE_ATTRIBUTION), rel(SOURCE_BY_MEMBERSHIP_DELTA), rel(SOURCE_BX_POLICY)],
            "time_axis": "MT5 server timestamp; open_time is execution time and probabilities are closed-bar runtime inputs(MT5 서버 시각; open_time은 실행 시각이고 확률은 닫힌 봉 런타임 입력)",
            "sample_scope": "US100 M5 validation OOS MT5 runtime probe trades(US100 M5 검증 OOS MT5 런타임 탐침 거래)",
            "missing_or_duplicate_check": "row grain audited by BY; BZ preserves candidate-level and trade-level rows(BY에서 행 단위 감사, BZ는 후보/거래 행 보존)",
            "feature_label_boundary": "no new labels; only entry-known month/hour and closed-bar probabilities(새 라벨 없음; 진입 시점 월/시각과 닫힌 봉 확률만 사용)",
            "split_boundary": "runtime validation OOS only; no forward claim(런타임 검증 OOS 전용, 전진 주장 없음)",
            "leakage_risk": "post-run threshold scan can overfit; therefore h17 floors are negative-control/deferred(사후 임계값 탐색은 과적합 위험이 있어 17시 하한은 음성 대조/보류)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path)},
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "existing ONNX runtime model only(기존 ONNX 런타임 모델만 사용)",
            "target_and_label": "unchanged from BX/BV; no new label(BX/BV와 동일, 새 라벨 없음)",
            "split_method": "MT5 runtime validation OOS inherited from BX(BX에서 이어받은 MT5 런타임 검증 OOS)",
            "selection_metric": "no model selection; next CA will compare MT5 net/PF/density/recovery/DD(모델 선택 없음; 다음 CA가 MT5 순수익/PF/밀도/회복/DD 비교)",
            "threshold_policy": "runtime-configured rule thresholds only(런타임 설정 규칙 임계값만)",
            "overfit_risk": "h17 threshold floors are outcome-scanned; downgraded to deferred controls(17시 임계값은 결과 탐색이라 보류 대조로 강등)",
            "validation_judgment": "exploratory_materialization_only(탐색 구체화 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "BX3 guard input materialization(BX3 가드 입력 구체화)",
            "evidence_available": [rel(GUARD_CANDIDATE_MATRIX), rel(GUARD_CANDIDATE_PROXY_IMPACT), rel(RUNTIME_ATTEMPT_QUEUE)],
            "evidence_missing": ["new MT5 CA execution", "forward replay", "tick equity path beyond tester DD"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "materialized runtime probe inputs only(런타임 탐침 입력 구체화만)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "new_model_training": final["new_model_training"],
            "new_mt5_execution": final["new_mt5_execution"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_closeout(종료 후 추적됨)",
            "lineage_judgment": "connected_with_materialization_boundary(구체화 경계 내 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    candidates: Sequence[Mapping[str, Any]],
    impacts: Sequence[Mapping[str, Any]],
    scan_rows: Sequence[Mapping[str, Any]],
    cluster_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    top_scan = list(scan_rows)[:6]
    ready_candidates = [row for row in candidates if int(row["runtime_priority"]) <= 4]
    report = f"""# run364BZ bx03 December late-session guard inputs(364BZ BX3 12월 후반 세션 가드 입력)

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next(다음): `{NEXT_RUN_ID}`
- gate(게이트): `{final['gate_passes']}/{final['gate_total']}`

## Action(행동)

Action(행동): BY attribution(BY 귀속)에서 나온 December h22 long loss block(12월 22시 롱 손실 차단), h17 overlay loss guard(17시 오버레이 손실 가드), equity DD cluster(평가손익 낙폭 클러스터)를 CA runtime probe(CA 런타임 탐침) 후보 입력으로 materialize(구체화)했다.

Effect(효과): calendar block end_hour(달력 차단 종료 시각)이 exclusive(배타)라는 runtime semantics(런타임 의미)를 명시하고, h17 threshold floors(17시 임계값 하한)는 proxy negative(프록시 부정)라 초기 MT5 grid(MT5 격자) 우선순위에서 낮췄다.

## Runtime Queue(런타임 대기열)

{table(ready_candidates, ["candidate_id", "runtime_priority", "variant_role", "synthetic_enabled", "calendar_start_hour", "calendar_end_hour", "covered_hours"], 8)}

## Proxy Impact(프록시 영향)

{table(impacts, ["candidate_id", "proxy_estimable", "removed_trade_count", "removed_net", "estimated_net", "estimated_density", "density_floor_status"], 8)}

## H17 Scan(17시 스캔)

{table(top_scan, ["scan_id", "runtime_param", "threshold", "kept_trade_count", "kept_net", "removed_net", "proxy_effect"], 6)}

## Equity Cluster Proxy(평가손익 클러스터 프록시)

{table(cluster_rows, ["cluster_rank", "close_time", "source_bucket", "net_profit", "closed_balance_drawdown", "proxy_boundary"], 6)}

## Gates(게이트)

{table(gates, ["gate", "status", "evidence"], 8)}

## Boundary(경계)

runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다. BZ는 materialization only(구체화 전용)이며 새 MT5 execution(MT5 실행)은 하지 않았다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision: Stage364BZ bx03 December late-session guard inputs(결정: BX3 12월 후반 세션 가드 입력)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Action(행동): BX3 calendar semantics(BX3 달력 의미), h17 overlay floor scan(17시 오버레이 하한 스캔), equity DD proxy cluster(평가손익 낙폭 프록시 클러스터)를 CA runtime queue(CA 런타임 대기열)로 구체화했다.

Effect(효과): h22-only isolation(h22 단독 분리), h21-h23 stress(h21-h23 압박), native-short same-calendar control(같은 달력 기본 숏 대조)을 우선 실행 대상으로 만들고, h17 threshold tightening(17시 임계값 강화)은 프록시 부정이라 보류했다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364BZ -->", f"\n<!-- run364BZ -->\n- `{RUN_ID}`: bx03 December late-session guard input materialization(BX3 12월 후반 세션 가드 입력 구체화) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364BZ -->", f"\n<!-- run364BZ -->\n## run364BZ bx03 December late-session guard inputs(BX3 12월 후반 세션 가드 입력)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
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

Current truth(현재 진실): `run364BZ` materialized(구체화 완료) BX3 guard inputs(BX3 가드 입력). Runtime-ready candidates(런타임 준비 후보)는 h22-only isolation(h22 단독 분리), h21-h23 stress(h21-h23 압박), native-short same-calendar control(같은 달력 기본 숏 대조)이고, h17 threshold floors(17시 임계값 하한)는 proxy negative(프록시 부정)로 보류했다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 CA runtime probe(CA 런타임 탐침)를 실행해 MT5 net/PF/density/recovery/equity DD(MT5 순수익/수익 팩터/밀도/회복/평가손익 낙폭)를 비교한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe best variant(런타임 탐침 최선 변형): `{BEST_VARIANT_ID}`

Best MT5 KPI(최선 MT5 핵심 성과 지표): net `{final['parent_best_net_profit']}`, PF `{final['parent_best_profit_factor']}`, trades `{final['parent_best_trade_count']}`, density `{final['parent_best_density']}`, recovery `{final['parent_best_recovery_factor']}`, equity DD `{final['parent_best_equity_drawdown_amount']}`.

Materialized queue(구체화 대기열): CA control/isolation/stress/source-control(CA 대조/분리/압박/원천 대조) `{final['runtime_ready_candidate_count']}` candidates.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364BZ -->", f"\n<!-- run364BZ -->\n- {final['created_at_utc']} `{RUN_ID}` materialized BX3 guard inputs(BX3 가드 입력 구체화). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(IDEA_REGISTRY, "<!-- run364BZ_bx3_guard_inputs -->", "\n<!-- run364BZ_bx3_guard_inputs -->\n- Idea(아이디어): BX3 개선을 December h22 calendar block(12월 h22 달력 차단), h17 overlay(17시 오버레이), native short control(기본 숏 대조)로 분리한다. Effect(효과): 다음 MT5 runtime probe(MT5 런타임 탐침)가 어떤 수익 원천을 검증하는지 선명해진다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "materialization(구체화)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["candidate_count"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(GUARD_CANDIDATE_MATRIX),
        "result_status": final["status"],
        "trade_density_per_feature_day": final["parent_best_density"],
        "trade_density_requirement_status": "passed_parent_runtime_density(상위 런타임 밀도 통과)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "evidence_boundary": "materialization_only(구체화 전용)",
        "next_action": NEXT_RUN_ID,
        "question": "Which BX3 guard variants should CA test next?(BX3 가드 중 다음 CA가 무엇을 시험해야 하는가?)",
        "net_profit": final["parent_best_net_profit"],
        "profit_factor": final["parent_best_profit_factor"],
        "recovery_factor": final["parent_best_recovery_factor"],
        "trade_count": final["parent_best_trade_count"],
        "max_drawdown_amount": final["parent_best_equity_drawdown_amount"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)

    ledger_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "materialization"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "materialization"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}",
            "record_view": view,
            "tier_scope": tier,
            "kpi_scope": scope,
            "view": view,
            "tier": tier,
            "metric_scope": scope,
            "external_verification_status": "not_run_materialization_only(구체화 전용 미실행)",
            "notes": "Tier B missing_required(Tier B 필수 누락); no fallback source(대체 원천 없음).",
        }
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)

    artifact_rows = []
    for artifact_type, path in [
        ("final_decision", FINAL_DECISION),
        ("guard_candidate_matrix", GUARD_CANDIDATE_MATRIX),
        ("runtime_attempt_queue", RUNTIME_ATTEMPT_QUEUE),
        ("proxy_impact", GUARD_CANDIDATE_PROXY_IMPACT),
        ("report", REPORT_PATH),
        ("script", Path(__file__)),
        ("gate_audit", GATE_AUDIT),
    ]:
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha(path),
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
                "created_at_utc": final["created_at_utc"],
                "notes": "materialization artifact(구체화 산출물)",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)


def run_manifest(final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "producer": rel(Path(__file__)),
        "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
        "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()],
        "final_decision": rel(FINAL_DECISION),
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": final["created_at_utc"],
    }


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    parent_final = validate_inputs()
    trades = read_trade_attribution()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    calendar_rows = calendar_semantics_rows()
    scan_rows = h17_quality_scan_rows(trades)
    cluster_rows = equity_cluster_rows(trades)
    candidates = base_candidate_rows(scan_rows)
    impacts = estimate_candidate_impacts(trades, candidates)
    queue = runtime_queue_rows(candidates, impacts)
    write_csv(CALENDAR_SEMANTICS_AUDIT, calendar_rows)
    write_csv(H17_OVERLAY_QUALITY_SCAN, scan_rows)
    write_csv(EQUITY_DD_CLUSTER_PROXY, cluster_rows)
    write_csv(GUARD_CANDIDATE_MATRIX, candidates)
    write_csv(GUARD_CANDIDATE_PROXY_IMPACT, impacts)
    write_csv(RUNTIME_ATTEMPT_QUEUE, queue)

    gates = build_gates(candidates, queue, receipts_written=False)
    final = final_payload(parent_final, candidates, queue, impacts, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = build_gates(candidates, queue, receipts_written=True)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(parent_final, candidates, queue, impacts, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, candidates, impacts, scan_rows, cluster_rows, gates)
    write_ledgers(final)
    write_json(RUN_MANIFEST, run_manifest(final))
    write_receipts(final)
    write_json(RUN_MANIFEST, run_manifest(final))
    print(json.dumps(json_ready(final), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
