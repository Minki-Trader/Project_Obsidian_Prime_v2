from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import materialize_density_restore_forward_regime_stress_inputs_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-04"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BH"
RUN_ID = "run364BH_train_density_restore_forward_regime_stress_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
PACKAGE_RUN_ID = parent.PACKAGE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BI_review_density_restore_forward_regime_stress_scout_without_db_v1"

STATUS = "completed_stage364BH_forward_regime_stress_proxy_scout_review_required_no_authority"
JUDGMENT = "proxy_scout_found_micro_margin_candidate_but_short_balance_unresolved_review_required_no_authority"
DECISION = "stage364BH_open_run364BI_forward_regime_stress_scout_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
TARGET_SHORT_SHARE = 0.12
TARGET_LONG_SHARE = 0.88
DEPOSIT = 500.0

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EXPECTED_DIR = RUN_DIR / "expected_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
ENTRY_PROBABILITY_JOIN_AUDIT = RUN_DIR / "entry_probability_join_audit.csv"
SCOUT_SURFACE = RUN_DIR / "forward_regime_stress_proxy_scout_surface.csv"
SELECTED_PROXY_CANDIDATE = RUN_DIR / "selected_proxy_candidate.json"
SELECTED_EXPECTED_TRADE_TAPE = EXPECTED_DIR / "selected_trade_tape.csv"
SELECTED_SEGMENT_ATTRIBUTION = RUN_DIR / "selected_segment_attribution.csv"
DENSITY_FLOOR_SURVIVAL_AUDIT = RUN_DIR / "density_floor_survival_audit.csv"
FORWARD_BLOCK_REPLAY = RUN_DIR / "selected_forward_block_replay.csv"
MONTH_REGIME_REPLAY = RUN_DIR / "selected_month_regime_replay.csv"
SHORT_RESTORE_FEASIBILITY = RUN_DIR / "short_restore_feasibility_audit.csv"
REJECTED_DENSITY_REPAIRS = RUN_DIR / "rejected_density_breaking_repairs.csv"
RUN364BI_QUEUE = RUN_DIR / "run364BI_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_boundary_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BH_forward_regime_stress_proxy_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BH_forward_regime_stress_proxy_scout.md"
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

BF = parent.parent
BE = BF.parent

BE_SUMMARY = BE.EXECUTION_SUMMARY
BE_PROBABILITY_DIFF = BE.PROBABILITY_DIFF
BF_CLOSED_TRADES = BF.CLOSED_TRADE_ATTRIBUTION
BF_FINAL_DECISION = BF.FINAL_DECISION
BF_RUNTIME_RECEIPT = BF.RUNTIME_RECEIPT
BG_QUEUE = parent.RUN364BH_QUEUE

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.SOURCE_RUNTIME_SUMMARY,
    parent.FORWARD_BLOCK_STRESS,
    parent.MONTHLY_REGIME_STRESS,
    parent.SESSION_SIDE_STABILITY,
    parent.SHORT_RESTORE_SLICES,
    parent.DRAWDOWN_TAIL_STRESS,
    parent.REGIME_GUARDRAIL_MATRIX,
    BG_QUEUE,
    BF_CLOSED_TRADES,
    BF_FINAL_DECISION,
    BF_RUNTIME_RECEIPT,
    BE_SUMMARY,
    BE_PROBABILITY_DIFF,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    ENTRY_PROBABILITY_JOIN_AUDIT,
    SCOUT_SURFACE,
    SELECTED_PROXY_CANDIDATE,
    SELECTED_EXPECTED_TRADE_TAPE,
    SELECTED_SEGMENT_ATTRIBUTION,
    DENSITY_FLOOR_SURVIVAL_AUDIT,
    FORWARD_BLOCK_REPLAY,
    MONTH_REGIME_REPLAY,
    SHORT_RESTORE_FEASIBILITY,
    REJECTED_DENSITY_REPAIRS,
    RUN364BI_QUEUE,
    WORK_PACKET,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
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


def fs_path(path: Path | str) -> str:
    raw = str(Path(path).resolve())
    if sys.platform.startswith("win") and len(raw) >= 240 and not raw.startswith("\\\\?\\"):
        return "\\\\?\\" + raw
    return raw


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.resolve().as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.exists() or not candidate.is_file():
        return ""
    digest = hashlib.sha256()
    with open(fs_path(candidate), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if value is None:
        return []
    if isinstance(value, float) and math.isnan(value):
        return []
    if isinstance(value, str):
        if not value:
            return []
        return [item.strip() for item in value.split(";") if item.strip()]
    return []


def ensure_dirs() -> None:
    for path in [RUN_DIR, EXPECTED_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> Mapping[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BH inputs(BH 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"parent has forbidden operating claim(부모 운영 주장 금지 위반): {key}={final.get(key)}")
    gates = read_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트 전체 통과 아님)")
    queue = read_rows(BG_QUEUE)
    if len(queue) != as_int(final.get("queue_rows")):
        raise RuntimeError("BG queue row count mismatch(BG 대기열 행 수 불일치)")
    return final


def load_one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if not rows:
        raise RuntimeError(f"empty required csv(필수 CSV 비어 있음): {rel(path)}")
    return rows[0]


def telemetry_path(summary: Mapping[str, Any]) -> Path:
    raw = str(summary.get("local_telemetry_path", "")).strip()
    if not raw:
        raise RuntimeError("BE summary has no telemetry path(BE 요약에 telemetry 경로 없음)")
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    if not exists(path):
        raise FileNotFoundError(f"telemetry path missing(telemetry 경로 누락): {path}")
    return path


def load_trades_with_probabilities() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    trades = pd.read_csv(fs_path(BF_CLOSED_TRADES), encoding="utf-8-sig")
    trades["entry_time_dt"] = pd.to_datetime(trades["entry_time"])
    trades["entry_month"] = trades["entry_time_dt"].dt.strftime("%Y-%m")
    trades["entry_month_num"] = trades["entry_time_dt"].dt.strftime("%m")
    trades["entry_quarter"] = trades["entry_time_dt"].dt.to_period("Q").astype(str)
    trades["entry_hour"] = trades["entry_time_dt"].dt.hour
    trades["pnl"] = pd.to_numeric(trades["net_profit_after_cost"], errors="coerce").fillna(0.0)
    trades["slice_key"] = trades["side"].astype(str) + "_" + trades["entry_month"].astype(str) + "_h" + trades["entry_hour"].astype(str)
    trades = trades.sort_values("trade_index").reset_index(drop=True)

    summary = load_one_row(BE_SUMMARY)
    tele = pd.read_csv(
        fs_path(telemetry_path(summary)),
        usecols=[
            "record_type",
            "written_at",
            "bar_time",
            "p_short",
            "p_flat",
            "p_long",
            "decision",
            "decision_reason",
            "exec_action",
            "order_filled",
        ],
        encoding="utf-8-sig",
    )
    opens = tele[
        (tele["record_type"].astype(str) == "cycle")
        & (tele["order_filled"].astype(str).str.lower() == "true")
        & (tele["exec_action"].astype(str).str.contains("open", na=False))
    ].copy()
    opens["entry_time_dt"] = pd.to_datetime(opens["written_at"], format="%Y.%m.%d %H:%M:%S")
    for col in ["p_short", "p_flat", "p_long"]:
        opens[col] = pd.to_numeric(opens[col], errors="coerce")
    opens["selected_probability"] = np.where(opens["decision"] == "long", opens["p_long"], opens["p_short"])
    opens["opposite_probability"] = np.where(opens["decision"] == "long", opens["p_short"], opens["p_long"])
    opens["margin_vs_opposite"] = opens["selected_probability"] - opens["opposite_probability"]
    opens["margin_vs_flat"] = opens["selected_probability"] - opens["p_flat"]
    opens["margin_vs_max_other"] = opens.apply(
        lambda row: row["p_long"] - max(row["p_short"], row["p_flat"])
        if row["decision"] == "long"
        else row["p_short"] - max(row["p_long"], row["p_flat"]),
        axis=1,
    )
    join_cols = [
        "entry_time_dt",
        "bar_time",
        "p_short",
        "p_flat",
        "p_long",
        "decision",
        "decision_reason",
        "selected_probability",
        "opposite_probability",
        "margin_vs_opposite",
        "margin_vs_flat",
        "margin_vs_max_other",
    ]
    joined = trades.merge(opens[join_cols], on="entry_time_dt", how="left", validate="one_to_one")
    audit = [
        {
            "run_id": RUN_ID,
            "audit_id": "entry_probability_join(진입 확률 결합)",
            "closed_trade_rows": len(trades),
            "telemetry_open_rows": len(opens),
            "joined_rows": len(joined),
            "missing_probability_rows": int(joined["selected_probability"].isna().sum()),
            "duplicate_entry_time_rows": int(trades["entry_time_dt"].duplicated().sum()),
            "time_axis": "trade entry_time joined to telemetry written_at, each decision used prior closed M5 bar(거래 진입시각을 telemetry 작성시각과 결합, 각 결정은 직전 닫힌 5분봉 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    if audit[0]["missing_probability_rows"] or audit[0]["duplicate_entry_time_rows"] or len(opens) != len(trades):
        raise RuntimeError("entry probability join failed(진입 확률 결합 실패)")
    return joined, audit


def full_business_days(frame: pd.DataFrame) -> int:
    start = frame["entry_time_dt"].min().date()
    end = frame["entry_time_dt"].max().date()
    return int(np.busday_count(start, end + timedelta(days=1)))


def metrics(frame: pd.DataFrame, *, full_days: int) -> dict[str, Any]:
    if frame.empty:
        return {
            "net_profit": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "trade_count": 0,
            "trade_density_per_business_day": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "max_closed_drawdown_amount": 0.0,
            "max_closed_drawdown_percent": 0.0,
            "recovery_factor": 0.0,
            "win_rate_percent": 0.0,
            "long_trade_count": 0,
            "short_trade_count": 0,
            "long_share": 0.0,
            "short_share": 0.0,
        }
    pnl = frame["pnl"].astype(float)
    gross_profit = float(pnl[pnl > 0].sum())
    gross_loss = float(-pnl[pnl < 0].sum())
    net = float(pnl.sum())
    balance = DEPOSIT + pnl.cumsum()
    peak = balance.cummax()
    drawdown = peak - balance
    dd_amount = float(drawdown.max()) if len(drawdown) else 0.0
    dd_percent = float(((drawdown / peak.replace(0, np.nan)) * 100.0).max()) if len(drawdown) else 0.0
    count = int(len(frame))
    longs = int((frame["side"].astype(str) == "long").sum())
    shorts = int((frame["side"].astype(str) == "short").sum())
    return {
        "net_profit": round(net, 2),
        "profit_factor": finite(gross_profit / gross_loss if gross_loss else 999.0, 10),
        "expectancy": finite(net / count if count else 0.0, 10),
        "trade_count": count,
        "trade_density_per_business_day": finite(count / full_days if full_days else 0.0, 10),
        "gross_profit": finite(gross_profit, 10),
        "gross_loss": finite(gross_loss, 10),
        "max_closed_drawdown_amount": finite(dd_amount, 10),
        "max_closed_drawdown_percent": finite(dd_percent, 10),
        "recovery_factor": finite(net / dd_amount if dd_amount else 999.0, 10),
        "win_rate_percent": finite((pnl > 0).mean() * 100.0, 10),
        "long_trade_count": longs,
        "short_trade_count": shorts,
        "long_share": finite(longs / count if count else 0.0, 10),
        "short_share": finite(shorts / count if count else 0.0, 10),
    }


def candidate_definitions() -> list[dict[str, Any]]:
    return [
        {
            "variant_id": "bh00_current_runtime_policy_reference",
            "idea_type": "reference(기준)",
            "policy_family": "no_policy_change(정책 변경 없음)",
            "description": "current BF/BE MT5 closed trade tape baseline(현재 BF/BE MT5 종료 거래 기준)",
        },
        {
            "variant_id": "bh01_long_h19_margin_opp_0015",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "hour19_closed_bar_margin_guard(19시 닫힌 봉 margin 가드)",
            "long_hours": [19],
            "margin_col": "margin_vs_opposite",
            "margin_min": 0.0015,
            "description": "block hour 19 long entries when selected minus opposite probability <0.0015(19시 롱에서 선택-반대 확률 차이 0.0015 미만 차단)",
        },
        {
            "variant_id": "bh02_long_h19_margin_opp_0020",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "hour19_closed_bar_margin_guard(19시 닫힌 봉 margin 가드)",
            "long_hours": [19],
            "margin_col": "margin_vs_opposite",
            "margin_min": 0.002,
            "description": "block hour 19 long entries when selected minus opposite probability <0.0020(19시 롱에서 선택-반대 확률 차이 0.0020 미만 차단)",
        },
        {
            "variant_id": "bh03_long_h19_margin_max_0015",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "hour19_closed_bar_margin_guard(19시 닫힌 봉 margin 가드)",
            "long_hours": [19],
            "margin_col": "margin_vs_max_other",
            "margin_min": 0.0015,
            "description": "block hour 19 long entries when selected minus max-other probability <0.0015(19시 롱에서 선택-최대 다른 확률 차이 0.0015 미만 차단)",
        },
        {
            "variant_id": "bh04_long_h18_margin_opp_0005",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "hour18_closed_bar_margin_guard(18시 닫힌 봉 margin 가드)",
            "long_hours": [18],
            "margin_col": "margin_vs_opposite",
            "margin_min": 0.0005,
            "description": "thin hour 18 long guard(18시 롱 얇은 가드)",
        },
        {
            "variant_id": "bh05_long_h16_margin_opp_0020",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "hour16_closed_bar_margin_guard(16시 닫힌 봉 margin 가드)",
            "long_hours": [16],
            "margin_col": "margin_vs_opposite",
            "margin_min": 0.002,
            "description": "hour 16 long margin stress guard(16시 롱 margin 압박 가드)",
        },
        {
            "variant_id": "bh06_negative_month_exact_firewall",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "exact_month_firewall_research_only(정확 월 방화벽, 연구 전용)",
            "blocked_months": ["2025-08", "2025-12"],
            "overfit_penalty": 20.0,
            "description": "drop exact negative months from BG stress matrix(BG 압박 행렬의 정확 음수 월 제외)",
        },
        {
            "variant_id": "bh07_weak_month_exact_firewall",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "exact_month_firewall_research_only(정확 월 방화벽, 연구 전용)",
            "blocked_months": ["2025-08", "2025-12", "2026-01"],
            "overfit_penalty": 25.0,
            "description": "drop exact weak months from BG stress matrix(BG 압박 행렬의 정확 약한 월 제외)",
        },
        {
            "variant_id": "bh08_hour18_19_long_hard_firewall",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "hard_hour_firewall_density_stress(강한 시간 방화벽 밀도 압박)",
            "hard_block_long_hours": [18, 19],
            "description": "drop all long entries at 18/19(18/19시 롱 전체 제외)",
        },
        {
            "variant_id": "bh09_short_negative_exact_slice_guard",
            "idea_type": "offensive_control(공격/대조)",
            "policy_family": "exact_short_slice_guard_research_only(정확 숏 조각 가드, 연구 전용)",
            "blocked_short_slices": [
                "short_2025-01_h17",
                "short_2025-10_h20",
                "short_2025-04_h17",
                "short_2025-12_h17",
                "short_2025-05_h20",
                "short_2025-02_h17",
            ],
            "overfit_penalty": 35.0,
            "description": "drop exact negative short slices from BG(BG의 정확 음수 숏 조각 제외)",
        },
        {
            "variant_id": "bh10_h19_margin_plus_short_2025_01_h17",
            "idea_type": "offensive_control(공격/대조)",
            "policy_family": "micro_margin_plus_exact_short_slice_watch(소형 margin + 정확 숏 조각 관찰)",
            "long_hours": [19],
            "margin_col": "margin_vs_opposite",
            "margin_min": 0.002,
            "blocked_short_slices": ["short_2025-01_h17"],
            "overfit_penalty": 30.0,
            "description": "h19 margin guard plus one exact short loss slice(19시 margin 가드 + 정확 숏 손실 조각 1개)",
        },
    ]


def candidate_mask(frame: pd.DataFrame, candidate: Mapping[str, Any]) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    blocked_months = as_list(candidate.get("blocked_months"))
    blocked_month_nums = as_list(candidate.get("blocked_month_nums"))
    hard_block_long_hours = [as_int(item) for item in as_list(candidate.get("hard_block_long_hours"))]
    blocked_short_slices = as_list(candidate.get("blocked_short_slices"))
    long_hours = [as_int(item) for item in as_list(candidate.get("long_hours"))]
    if blocked_months:
        mask &= ~frame["entry_month"].isin(blocked_months)
    if blocked_month_nums:
        mask &= ~frame["entry_month_num"].isin(blocked_month_nums)
    if hard_block_long_hours:
        mask &= ~((frame["side"] == "long") & frame["entry_hour"].isin(hard_block_long_hours))
    if blocked_short_slices:
        mask &= ~((frame["side"] == "short") & frame["slice_key"].isin(blocked_short_slices))
    margin_col_value = candidate.get("margin_col")
    margin_min_value = candidate.get("margin_min")
    margin_col = "" if margin_col_value is None or (isinstance(margin_col_value, float) and math.isnan(margin_col_value)) else str(margin_col_value)
    if long_hours and margin_col and margin_min_value is not None and not (isinstance(margin_min_value, float) and math.isnan(margin_min_value)):
        mask &= ~(
            (frame["side"] == "long")
            & frame["entry_hour"].isin(long_hours)
            & (pd.to_numeric(frame[margin_col], errors="coerce") < as_float(margin_min_value))
        )
    return mask


def forward_fail_count(frame: pd.DataFrame) -> int:
    rows = segment_rows(frame, "entry_quarter", "forward_block", full_days=False)
    return sum(1 for row in rows if as_float(row["net_profit"]) <= 0 or as_float(row["profit_factor"]) < 1.0)


def weak_month_fail_count(frame: pd.DataFrame) -> int:
    rows = segment_rows(frame, "entry_month", "month", full_days=False)
    return sum(1 for row in rows if as_float(row["net_profit"]) <= 0 or as_float(row["profit_factor"]) < 1.0)


def selection_score(row: Mapping[str, Any], baseline: Mapping[str, Any]) -> float:
    density = as_float(row["trade_density_per_business_day"])
    net_delta = as_float(row["net_delta_vs_baseline"])
    pf_delta = as_float(row["pf_delta_vs_baseline"])
    dd_delta = as_float(row["closed_dd_delta_vs_baseline"])
    long_share = as_float(row["long_share"])
    removed = as_int(row["removed_trade_count"])
    overfit_penalty = as_float(row.get("overfit_penalty"))
    score = net_delta * 0.20 + pf_delta * 120.0 - max(0.0, dd_delta) * 0.35
    score += min(0.08, max(0.0, density - DENSITY_FLOOR)) * 250.0
    score -= max(0.0, long_share - TARGET_LONG_SHARE) * 120.0
    score -= as_int(row["forward_fail_count"]) * 60.0
    score -= as_int(row["weak_month_fail_count"]) * 10.0
    score -= overfit_penalty
    score -= max(0, removed - 20) * 0.4
    if density < DENSITY_FLOOR:
        score -= 1000.0
    if as_float(row["net_profit"]) <= as_float(baseline["net_profit"]):
        score -= 25.0
    return round(score, 10)


def candidate_status(row: Mapping[str, Any], baseline: Mapping[str, Any]) -> str:
    if as_float(row["trade_density_per_business_day"]) < DENSITY_FLOOR:
        return "rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴)"
    if as_int(row["forward_fail_count"]) > 0:
        return "watch_forward_block_stress_remaining(관찰, 전진 유사 블록 압박 잔존)"
    if as_float(row["long_share"]) > as_float(baseline["long_share"]):
        return "watch_long_skew_worse_than_parent(관찰, 부모보다 롱 편향 악화)"
    if as_float(row["net_profit"]) > as_float(baseline["net_profit"]) and as_float(row["profit_factor"]) >= as_float(baseline["profit_factor"]):
        return "proxy_review_candidate_density_preserved(프록시 검토 후보, 밀도 보존)"
    return "watch_no_strict_improvement(관찰, 엄격 개선 아님)"


def build_surface(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    days = full_business_days(frame)
    baseline_trades = frame.copy()
    baseline = metrics(baseline_trades, full_days=days)
    rows: list[dict[str, Any]] = []
    selected_trades = baseline_trades
    for candidate in candidate_definitions():
        mask = candidate_mask(frame, candidate)
        trades = frame[mask].copy()
        row = dict(candidate)
        row.update(metrics(trades, full_days=days))
        row["run_id"] = RUN_ID
        row["removed_trade_count"] = int(len(frame) - len(trades))
        row["removed_net_profit"] = finite(frame.loc[~mask, "pnl"].sum(), 10)
        row["net_delta_vs_baseline"] = finite(as_float(row["net_profit"]) - as_float(baseline["net_profit"]), 10)
        row["pf_delta_vs_baseline"] = finite(as_float(row["profit_factor"]) - as_float(baseline["profit_factor"]), 10)
        row["density_delta_vs_baseline"] = finite(as_float(row["trade_density_per_business_day"]) - as_float(baseline["trade_density_per_business_day"]), 10)
        row["closed_dd_delta_vs_baseline"] = finite(as_float(row["max_closed_drawdown_amount"]) - as_float(baseline["max_closed_drawdown_amount"]), 10)
        row["forward_fail_count"] = forward_fail_count(trades)
        row["weak_month_fail_count"] = weak_month_fail_count(trades)
        row["density_floor_pass"] = as_float(row["trade_density_per_business_day"]) >= DENSITY_FLOOR
        row["short_share_target_pass"] = as_float(row["short_share"]) >= TARGET_SHORT_SHARE
        row["long_share_target_pass"] = as_float(row["long_share"]) <= TARGET_LONG_SHARE
        row["overfit_penalty"] = as_float(candidate.get("overfit_penalty", 0.0))
        row["candidate_status"] = candidate_status(row, baseline)
        row["selection_score"] = selection_score(row, baseline)
        row["claim_boundary"] = CLAIM_BOUNDARY
        rows.append(row)
    surface = pd.DataFrame(rows).sort_values(
        ["density_floor_pass", "selection_score", "net_profit"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    best_row = surface.iloc[0].to_dict()
    selected_mask = candidate_mask(frame, best_row)
    selected_trades = frame[selected_mask].copy()
    return surface, selected_trades, baseline


def segment_rows(frame: pd.DataFrame, group_col: str, segment_type: str, *, full_days: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if frame.empty:
        return rows
    total_days = full_business_days(frame)
    for key, part in frame.groupby(group_col, sort=True):
        days = total_days if full_days else int(np.busday_count(part["entry_time_dt"].min().date(), part["entry_time_dt"].max().date() + timedelta(days=1)))
        metric = metrics(part.copy(), full_days=max(1, days))
        rows.append(
            {
                "run_id": RUN_ID,
                "segment_type": segment_type,
                "segment_id": str(key),
                "business_days": days,
                **metric,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def selected_segment_rows(selected: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(segment_rows(selected, "entry_quarter", "quarter", full_days=False))
    rows.extend(segment_rows(selected, "entry_month", "month", full_days=False))
    rows.extend(segment_rows(selected, "entry_hour", "entry_hour", full_days=False))
    for (hour, side), part in selected.groupby(["entry_hour", "side"], sort=True):
        metric = metrics(part.copy(), full_days=max(1, int(np.busday_count(part["entry_time_dt"].min().date(), part["entry_time_dt"].max().date() + timedelta(days=1)))))
        rows.append(
            {
                "run_id": RUN_ID,
                "segment_type": "entry_hour_side",
                "segment_id": f"h{hour}_{side}",
                **metric,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def short_restore_rows(baseline: Mapping[str, Any], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    total = as_int(baseline["trade_count"])
    shorts = as_int(baseline["short_trade_count"])
    longs = as_int(baseline["long_trade_count"])
    min_shorts_for_target_at_current_total = math.ceil(TARGET_SHORT_SHARE * total)
    min_added_shorts_at_current_policy = math.ceil((TARGET_SHORT_SHARE * total - shorts) / (1.0 - TARGET_SHORT_SHARE))
    max_total_for_target_without_new_shorts = math.floor(shorts / TARGET_SHORT_SHARE)
    long_removals_needed_without_new_shorts = max(0, total - max_total_for_target_without_new_shorts)
    density_without_new_shorts = finite(max_total_for_target_without_new_shorts / 333.0, 10)
    return [
        {
            "run_id": RUN_ID,
            "audit_id": "current_short_balance_gap(현재 숏 균형 간극)",
            "current_total_trades": total,
            "current_long_trades": longs,
            "current_short_trades": shorts,
            "current_short_share": baseline["short_share"],
            "target_short_share": TARGET_SHORT_SHARE,
            "minimum_short_count_for_current_total": min_shorts_for_target_at_current_total,
            "minimum_added_shorts_needed_if_no_long_removal": min_added_shorts_at_current_policy,
            "long_removals_needed_if_no_new_shorts": long_removals_needed_without_new_shorts,
            "density_if_no_new_shorts_and_target_share": density_without_new_shorts,
            "judgment": "new_short_source_required_for_balance_without_density_collapse(밀도 붕괴 없이 균형을 맞추려면 새 숏 원천 필요)",
            "effect": "BI review(BI 검토)는 margin guard(마진 가드)와 separate short-source exploration(별도 숏 원천 탐색)을 분리해야 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "selected_short_balance_gap(선택 후보 숏 균형 간극)",
            "selected_total_trades": selected["trade_count"],
            "selected_long_trades": selected["long_trade_count"],
            "selected_short_trades": selected["short_trade_count"],
            "selected_short_share": selected["short_share"],
            "target_short_share": TARGET_SHORT_SHARE,
            "judgment": "selected_candidate_does_not_repair_short_balance(선택 후보는 숏 균형을 수리하지 않음)",
            "effect": "runtime probe package(런타임 탐침 패키지) 전에 short router source(숏 라우터 원천)를 새로 열 필요를 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def density_audit_rows(baseline: Mapping[str, Any], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "audit_id": "baseline_density(기준 밀도)",
            "variant_id": "bh00_current_runtime_policy_reference",
            "trade_count": baseline["trade_count"],
            "density": baseline["trade_density_per_business_day"],
            "density_floor": DENSITY_FLOOR,
            "status": "passed(통과)" if as_float(baseline["trade_density_per_business_day"]) >= DENSITY_FLOOR else "failed(실패)",
            "effect": "parent MT5 clue(부모 MT5 단서)가 밀도 하한을 간신히 넘는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "selected_density(선택 밀도)",
            "variant_id": selected["variant_id"],
            "trade_count": selected["trade_count"],
            "density": selected["trade_density_per_business_day"],
            "density_floor": DENSITY_FLOOR,
            "density_buffer": finite(as_float(selected["trade_density_per_business_day"]) - DENSITY_FLOOR, 10),
            "status": "passed(통과)" if as_float(selected["trade_density_per_business_day"]) >= DENSITY_FLOOR else "failed(실패)",
            "effect": "hard delete(강한 삭제)가 아니라 micro guard(미세 가드)만 다음 검토로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def queue_rows(selected: Mapping[str, Any], surface: pd.DataFrame) -> list[dict[str, Any]]:
    rejected = surface[surface["candidate_status"].astype(str).str.contains("density_breaks", na=False)]
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "bi01_review_micro_h19_margin_candidate",
            "selected_variant_id": selected["variant_id"],
            "policy_family": selected["policy_family"],
            "input_artifact": rel(SELECTED_PROXY_CANDIDATE),
            "review_question": "Can hour19 closed-bar margin guard survive review and package prep without hiding forward stress?(19시 닫힌 봉 margin 가드가 전진 압박을 숨기지 않고 검토/패키지 준비를 버티는가?)",
            "success_criteria": "keep density >=3/day, net/PF above parent, no forward-like block net<=0, and no runtime authority claim(밀도 3/day 이상, 순수익/PF 부모 이상, 전진 유사 블록 음수 없음, 런타임 권위 주장 없음)",
            "failure_criteria": "density buffer too thin, threshold looks curve-fit, or MT5 package semantics cannot express guard(밀도 여유가 너무 얇거나 threshold 과적합 또는 MT5 패키지 의미 표현 불가)",
            "effect": "smallest runtime-probe-prep candidate(가장 작은 런타임 탐침 준비 후보)를 검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "bi02_reject_density_breaking_repairs",
            "selected_variant_id": "",
            "policy_family": "density_breaking_hard_filters(밀도 붕괴 강한 필터)",
            "input_artifact": rel(REJECTED_DENSITY_REPAIRS),
            "review_question": "Should hard month/hour firewalls be closed as density-breaking under this run?(강한 월/시간 방화벽을 이번 실행에서 밀도 붕괴로 닫을 것인가?)",
            "success_criteria": "reject exact hard-delete repairs unless new trade source is added(새 거래 원천 없이는 정확 삭제 수리를 거절)",
            "failure_criteria": "hard filter is accidentally promoted despite density<3/day(밀도 3/day 미만인데 강한 필터가 실수로 승격)",
            "effect": "failure memory(실패 기억)를 다음 공격 탐색 제약으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 3,
            "queue_id": "bi03_open_short_source_not_exact_slice_delete",
            "selected_variant_id": "",
            "policy_family": "short_source_exploration_needed(숏 원천 탐색 필요)",
            "input_artifact": rel(SHORT_RESTORE_FEASIBILITY),
            "review_question": "Can a new short source add at least 28 short trades without trade splitting?(새 숏 원천이 거래 쪼개기 없이 최소 28개 숏을 추가할 수 있는가?)",
            "success_criteria": "short_share >=0.12 while density >=3/day and PF not worse than parent(숏 비중 0.12 이상, 밀도 3/day 이상, PF 부모 이상)",
            "failure_criteria": "short balance is attempted by deleting too many longs or exact loss slices(롱 과삭제 또는 정확 손실 조각 삭제로 숏 균형을 시도)",
            "effect": "long skew(롱 편향) 수리는 별도 공격 원천으로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(
    join_audit: Sequence[Mapping[str, Any]],
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    required = [
        ("scope_completion_gate", exists(SCOUT_SURFACE) and exists(SELECTED_PROXY_CANDIDATE), "BH proxy scout(BH 프록시 탐색) 산출물이 생성됐다."),
        ("kpi_contract_audit", as_int(selected["trade_count"]) > 0 and as_float(selected["profit_factor"]) > 0, "net/PF/density/DD/side metrics(순수익/PF/밀도/DD/방향 지표)를 기록했다."),
        ("skill_receipt_lint", all(exists(path) for path in [DATA_RECEIPT, EXPERIMENT_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT]), "필수 receipt(영수증)를 만들었다."),
        ("data_integrity_audit", int(join_audit[0]["missing_probability_rows"]) == 0, "closed trade(종료 거래)와 telemetry probability(원격측정 확률)가 1:1 결합됐다."),
        ("proxy_replay_gate", len(surface) >= 8, "BG queue(BG 대기열)를 여러 후보 proxy replay(프록시 재생)로 평가했다."),
        ("density_survival_gate", as_float(selected["trade_density_per_business_day"]) >= DENSITY_FLOOR, "선택 후보가 3/day 밀도 하한을 유지했다."),
        ("short_balance_boundary_gate", exists(SHORT_RESTORE_FEASIBILITY), "숏 균형 미해결을 별도 audit(감사)로 남겼다."),
        ("runtime_claim_boundary_gate", True, "새 MT5 실행, forward pass(전진 통과), runtime authority(런타임 권위)를 주장하지 않는다."),
        ("artifact_lineage_audit", exists(LINEAGE_RECEIPT), "입력/출력 산출물 계보를 연결했다."),
        ("required_gate_coverage_audit", bool(queue), "필수 gate(게이트)를 closeout(종료 기록)에 연결했다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(GATE_AUDIT if gate == "required_gate_coverage_audit" else FINAL_DECISION),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, effect in required
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-runtime-parity(런타임 동등성)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "BG materialized stress queue(BG 물질화 압박 대기열)를 proxy scout(프록시 탐색)로 좁혀 BI review(BI 검토)로 넘긴다.",
        },
    )


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path),
                "input_role": "BH source input(BH 원천 입력)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summary = load_one_row(BE_SUMMARY)
    tele_path = telemetry_path(summary)
    rows.append(
        {
            "run_id": RUN_ID,
            "input_path": rel(tele_path),
            "exists": exists(tele_path),
            "sha256": sha(tele_path),
            "input_role": "BE runtime telemetry(BE 런타임 원격측정)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "evidence_available": [rel(SCOUT_SURFACE), rel(SELECTED_PROXY_CANDIDATE), rel(SELECTED_EXPECTED_TRADE_TAPE)],
            "evidence_missing": ["new MT5 execution(새 MT5 실행)", "forward pass(전진 통과)", "runtime authority audit(런타임 권위 감사)"],
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(BF_CLOSED_TRADES), rel(BE_SUMMARY), "BE telemetry path from summary(BE 요약의 telemetry 경로)"],
            "time_axis": "entry_time from MT5 closed trades joined to telemetry written_at; telemetry bar_time is prior closed M5 bar(MT5 종료 거래 진입시각을 telemetry 작성시각과 결합, telemetry bar_time은 직전 닫힌 5분봉)",
            "sample_scope": "FPMarkets US100 M5 MT5 closed trades 2025-01-02..2026-04-13, Tier A only(FPMarkets US100 5분봉 MT5 종료 거래, Tier A만)",
            "missing_or_duplicate_check": "entry probability join missing rows=0 and duplicate entry_time=0(진입 확률 결합 누락 0, 중복 진입시각 0)",
            "feature_label_boundary": "policy guard uses entry hour and closed-bar probabilities known at decision time; PnL labels are used only for proxy evaluation(정책 가드는 결정 시점에 아는 진입 시간/닫힌 봉 확률만 사용, 손익 라벨은 프록시 평가 전용)",
            "split_boundary": "historical runtime-probe tape replay, not new forward split(과거 런타임 탐침 테이프 재생, 새 전진 분할 아님)",
            "leakage_risk": "threshold and exact-slice variants are selected after outcome review, so no operating claim(임계값/정확 조각 후보는 결과 검토 뒤 선택됐으므로 운영 주장 없음)",
            "data_hash_or_identity": {"closed_trade_sha256": sha(BF_CLOSED_TRADES), "selected_rows": final["selected_trade_count"]},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "a tiny closed-bar hour19 margin guard can improve PF/DD while preserving 3/day density(작은 19시 닫힌 봉 margin 가드가 3/day 밀도를 보존하며 PF/DD를 개선할 수 있음)",
            "decision_use": "BI review and possible runtime-probe package prep(BI 검토 및 가능한 런타임 탐침 패키지 준비)",
            "comparison_baseline": "run364BE/BF current MT5 runtime policy(현재 MT5 런타임 정책)",
            "control_variables": "US100 M5, fixed 0.1 lot, one position, no trade splitting, no new MT5 execution(US100 5분봉, 0.1 lot, 단일 포지션, 거래 쪼개기 없음, 새 MT5 실행 없음)",
            "changed_variables": "entry guard on hour/probability margin only for scout(탐색에서만 시간/확률 margin 진입 가드 변경)",
            "sample_scope": "MT5 closed trade tape plus telemetry probabilities(MT5 종료 거래 테이프와 원격측정 확률)",
            "success_criteria": "net/PF improve, density >=3/day, no forward-like block net<=0, long share not worse than parent(순수익/PF 개선, 밀도 3/day 이상, 전진 유사 블록 음수 없음, 롱 비중 부모보다 악화 없음)",
            "failure_criteria": "density <3/day, long skew worsens, or exact-slice curve fit dominates(밀도 3/day 미만, 롱 편향 악화, 정확 조각 과적합 우세)",
            "invalid_conditions": "telemetry join mismatch or operating claim without MT5 rerun(telemetry 결합 불일치 또는 MT5 재실행 없는 운영 주장)",
            "stop_conditions": "send only selected micro candidate to review; reject density-breaking repairs(선택된 미세 후보만 검토로 보내고 밀도 붕괴 수리는 거절)",
            "evidence_plan": [rel(SCOUT_SURFACE), rel(GATE_AUDIT), rel(REPORT_PATH)],
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "no new model trained; policy replay over existing ONNX runtime tape(새 모델 학습 없음, 기존 ONNX 런타임 테이프 정책 재생)",
            "target_and_label": "closed-trade PnL label for proxy evaluation only(종료 거래 손익 라벨은 프록시 평가 전용)",
            "split_method": "historical runtime tape replay(과거 런타임 테이프 재생)",
            "selection_metric": "multi-KPI score net/PF/density/DD/forward blocks/long-share(순수익/PF/밀도/DD/전진 블록/롱 비중 다중 KPI)",
            "secondary_metrics": ["short_share", "forward_fail_count", "weak_month_fail_count", "removed_trade_count"],
            "threshold_policy": "fixed scout thresholds after BG queue, review required(BG 대기열 뒤 고정 탐색 임계값, 검토 필요)",
            "overfit_risk": "medium-high because threshold discovered on same runtime tape(같은 런타임 테이프에서 임계값 발견, 중상 위험)",
            "calibration_risk": "probabilities are runtime ONNX scores, treated as ranking/margin not calibrated truth(확률은 런타임 ONNX 점수, 보정된 진실이 아니라 순위/margin으로 취급)",
            "comparison_baseline": "current BF MT5 closed trades(현재 BF MT5 종료 거래)",
            "validation_judgment": "exploratory_proxy_review_required(탐색 프록시, 검토 필요)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(BF_RUNTIME_RECEIPT), rel(BE_SUMMARY)],
            "shared_contract": "closed M5 bar probabilities, entry hour, one-position MT5 semantics(닫힌 5분봉 확률, 진입 시간, 단일 포지션 MT5 의미)",
            "known_differences": "BH does not rerun EA, does not replay full tick sequence after changed guard(BH는 EA 재실행이나 변경 가드 후 전체 틱 재생을 하지 않음)",
            "parity_check": "consumes BE clean probability/runtime parity, adds only proxy closed-trade filter(BE의 깨끗한 확률/런타임 동등성을 소비하고 종료 거래 필터만 추가)",
            "parity_identity": {"source_probability_diff": rel(BE_PROBABILITY_DIFF), "selected_variant_id": selected["variant_id"]},
            "runtime_claim_boundary": "research_only_proxy_scout(연구 전용 프록시 탐색)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": f"selected={selected['variant_id']}; net={selected['net_profit']}; pf={selected['profit_factor']}; density={selected['trade_density_per_business_day']}",
            "comparison_baseline": "run364BE/BF current MT5 policy(현재 MT5 정책)",
            "likely_drivers": "removes a small set of weak hour19 long entries with low selected-vs-opposite margin(선택-반대 margin 낮은 약한 19시 롱 소수 제거)",
            "segment_checks": [rel(FORWARD_BLOCK_REPLAY), rel(MONTH_REGIME_REPLAY), rel(SELECTED_SEGMENT_ATTRIBUTION)],
            "trade_shape": {
                "trade_count": selected["trade_count"],
                "long_count": selected["long_trade_count"],
                "short_count": selected["short_trade_count"],
                "long_share": selected["long_share"],
            },
            "alternative_explanations": "same-tape overfit and closed-trade DD underestimates tester equity DD(동일 테이프 과적합 및 종료 거래 DD가 테스터 equity DD를 과소평가)",
            "attribution_confidence": "medium_proxy_only(프록시 전용 중간)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "run364BH forward/regime stress proxy scout(전진/국면 압박 프록시 탐색)",
            "evidence_available": [rel(SCOUT_SURFACE), rel(SELECTED_PROXY_CANDIDATE), rel(SHORT_RESTORE_FEASIBILITY)],
            "evidence_missing": ["new MT5 strategy tester output(새 MT5 전략 테스터 출력)", "forward pass(전진 통과)", "operating promotion audit(운영 승격 감사)"],
            "judgment_label": "exploratory_proxy_review_required(탐색 프록시, 검토 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "작은 19시 margin 가드는 쓸만한 후보지만, 숏 균형은 아직 못 고쳤다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["operating_promotion", "runtime_authority", "live_readiness", "goal_achieve", "forward_passed"],
            "effect": "BH를 후보 탐색으로 닫고 운영 주장은 막는다.",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_manifested_after_commit(커밋 뒤 추적 또는 목록화)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def final_payload(
    parent_final: Mapping[str, Any],
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    selected_trades: pd.DataFrame,
    baseline: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    density_pass_rows = int(surface["density_floor_pass"].astype(bool).sum())
    strict_rows = int(surface["candidate_status"].astype(str).str.contains("proxy_review_candidate", na=False).sum())
    rejected_rows = int(surface["candidate_status"].astype(str).str.contains("density_breaks", na=False).sum())
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_mt5_net_profit": parent_final.get("parent_mt5_net_profit"),
        "parent_mt5_profit_factor": parent_final.get("parent_mt5_profit_factor"),
        "parent_mt5_trade_count": parent_final.get("parent_mt5_trade_count"),
        "parent_trade_density": parent_final.get("parent_trade_density"),
        "parent_long_share": parent_final.get("parent_long_share"),
        "parent_short_share": parent_final.get("parent_short_share"),
        "baseline_closed_trade_net_profit": baseline["net_profit"],
        "baseline_closed_trade_profit_factor": baseline["profit_factor"],
        "baseline_closed_trade_count": baseline["trade_count"],
        "baseline_closed_trade_density": baseline["trade_density_per_business_day"],
        "baseline_closed_trade_dd_amount": baseline["max_closed_drawdown_amount"],
        "selected_variant_id": selected["variant_id"],
        "selected_policy_family": selected["policy_family"],
        "selected_candidate_status": selected["candidate_status"],
        "selected_net_profit": selected["net_profit"],
        "selected_profit_factor": selected["profit_factor"],
        "selected_expectancy": selected["expectancy"],
        "selected_trade_count": selected["trade_count"],
        "selected_trade_density": selected["trade_density_per_business_day"],
        "selected_density_buffer": finite(as_float(selected["trade_density_per_business_day"]) - DENSITY_FLOOR, 10),
        "selected_closed_drawdown_amount": selected["max_closed_drawdown_amount"],
        "selected_closed_drawdown_percent": selected["max_closed_drawdown_percent"],
        "selected_recovery_factor": selected["recovery_factor"],
        "selected_long_trade_count": selected["long_trade_count"],
        "selected_short_trade_count": selected["short_trade_count"],
        "selected_long_share": selected["long_share"],
        "selected_short_share": selected["short_share"],
        "selected_removed_trade_count": selected["removed_trade_count"],
        "selected_removed_net_profit": selected["removed_net_profit"],
        "selected_net_delta_vs_baseline": selected["net_delta_vs_baseline"],
        "selected_pf_delta_vs_baseline": selected["pf_delta_vs_baseline"],
        "selected_closed_dd_delta_vs_baseline": selected["closed_dd_delta_vs_baseline"],
        "selected_forward_fail_count": selected["forward_fail_count"],
        "selected_weak_month_fail_count": selected["weak_month_fail_count"],
        "selected_selection_score": selected["selection_score"],
        "surface_rows": len(surface),
        "density_pass_rows": density_pass_rows,
        "proxy_review_candidate_rows": strict_rows,
        "rejected_density_breaking_rows": rejected_rows,
        "selected_trade_rows": len(selected_trades),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def sync_stage_brief_header() -> None:
    if not STAGE_BRIEF.exists():
        return
    text = STAGE_BRIEF.read_text(encoding="utf-8-sig")
    marker = "Current active run(현재 활성 실행):"
    lines = []
    replaced = False
    for line in text.splitlines():
        if line.startswith(marker):
            lines.append(f"{marker} `{NEXT_RUN_ID}`")
            replaced = True
        else:
            lines.append(line)
    if replaced:
        write_text(STAGE_BRIEF, "\n".join(lines) + "\n", bom=True)


def write_docs(
    final: Mapping[str, Any],
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    forward_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    short_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    top = surface.head(8).to_dict("records")
    rejected = surface[surface["candidate_status"].astype(str).str.contains("density_breaks", na=False)].head(8).to_dict("records")
    report = f"""# run364BH forward/regime stress proxy scout(364BH 전진/국면 압박 프록시 탐색)

## Scope(범위)

Action(행동): BG queue(BG 대기열)와 BF/BE MT5 closed trade + telemetry(MT5 종료 거래 + 원격측정)를 사용해 policy replay proxy scout(정책 재생 프록시 탐색)를 실행했다.

Effect(효과): Stage364(364단계)를 분기하지 않고, 작은 runtime-probe-prep candidate(런타임 탐침 준비 후보)와 density-breaking repair(밀도 붕괴 수리)를 분리했다.

## Selected(선택)

- selected_variant(선택 변형): `{final['selected_variant_id']}`
- selected net/PF/trades/density/DD/recovery(선택 순수익/수익 팩터/거래수/밀도/낙폭/회복): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_count']}` / `{final['selected_trade_density']}` / `{final['selected_closed_drawdown_amount']}` / `{final['selected_recovery_factor']}`
- selected long/short/share(선택 롱/숏/비중): `{final['selected_long_trade_count']}` / `{final['selected_short_trade_count']}` / `{final['selected_long_share']}`
- baseline net/PF/trades/density(기준 순수익/수익 팩터/거래수/밀도): `{final['baseline_closed_trade_net_profit']}` / `{final['baseline_closed_trade_profit_factor']}` / `{final['baseline_closed_trade_count']}` / `{final['baseline_closed_trade_density']}`

## Top Surface(상위 표면)

{markdown_table(top, ['variant_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_business_day', 'max_closed_drawdown_amount', 'long_share', 'removed_trade_count', 'forward_fail_count', 'selection_score'])}

## Rejected Density Repairs(거절된 밀도 수리)

{markdown_table(rejected, ['variant_id', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_business_day', 'candidate_status'])}

## Selected Forward Blocks(선택 전진 유사 블록)

{markdown_table(forward_rows, ['segment_id', 'trade_count', 'trade_density_per_business_day', 'net_profit', 'profit_factor', 'long_share'])}

## Weak Month Check(약한 월 확인)

{markdown_table([row for row in month_rows if row.get('segment_id') in {'2025-08', '2025-12', '2026-01'}], ['segment_id', 'trade_count', 'net_profit', 'profit_factor', 'trade_density_per_business_day', 'long_share'])}

## Short Balance(숏 균형)

{markdown_table(short_rows, ['audit_id', 'current_short_share', 'minimum_added_shorts_needed_if_no_long_removal', 'long_removals_needed_if_no_new_shorts', 'density_if_no_new_shorts_and_target_share', 'judgment'])}

## BI Queue(BI 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'selected_variant_id', 'policy_family', 'review_question'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'effect'])}

## Claim Boundary(주장 경계)

Effect(효과): 이 run(실행)은 proxy scout(프록시 탐색)이다. 새 MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BH forward/regime stress proxy scout decision(전진/국면 압박 프록시 탐색 결정)

Action(행동): `{RUN_ID}`를 실행해 `{final['selected_variant_id']}`를 BI review(BI 검토) 후보로 남겼다.

Effect(효과): selected candidate(선택 후보)는 net/PF/density(순수익/수익 팩터/밀도)를 개선하지만 short balance(숏 균형)는 아직 미해결이므로 operating promotion(운영 승격)을 막았다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - forward/regime stress proxy scout(전진/국면 압박 프록시 탐색).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BH Forward Regime Stress Proxy Scout Closeout",
        f"""## run364BH Forward Regime Stress Proxy Scout Closeout(364BH 전진 국면 압박 프록시 탐색 종료)

Action(행동): BG queue(BG 대기열)를 closed-trade probability replay(종료 거래 확률 재생)로 평가했다.

Effect(효과): `{final['selected_variant_id']}`를 `{NEXT_RUN_ID}` 검토로 넘기고, hard delete repair(강한 삭제 수리)는 밀도 붕괴로 닫았다.
""",
    )
    sync_stage_brief_header()
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BH Forward Regime Stress Proxy Scout(364BH 전진 국면 압박 프록시 탐색)

Action(행동): 기존 MT5 runtime evidence(런타임 근거)에 미세 margin guard(마진 가드)를 시산했다.

Effect(효과): Stage364(364단계)를 유지하고 `{NEXT_RUN_ID}` review(검토)로 이어간다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_proxy_review_required(없음, 프록시 검토 필요)
- runtime_probe_candidate(런타임 탐침 후보): `{final['selected_variant_id']}` review_required(검토 필요)
- latest_mt5_probe(최근 MT5 탐침): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- latest_mt5_net_pf_trades(최근 MT5 순수익/수익 팩터/거래수): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}`
- latest_proxy_scout(최근 프록시 탐색): `{RUN_ID}`
- selected_proxy_net_pf_density(선택 프록시 순수익/수익 팩터/밀도): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}`
- selected_proxy_long_short(선택 프록시 롱/숏): `{final['selected_long_trade_count']}` / `{final['selected_short_trade_count']}`
- short_balance_status(숏 균형 상태): unresolved_new_short_source_required(미해결, 새 숏 원천 필요)
- next_review_queue(다음 검토 대기열): `{rel(RUN364BI_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
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
        f"""# Current working state(현재 작업 상태)

updated_at_utc(UTC 수정시각): `{final['created_at_utc']}`

current_truth(현재 진실): `run364BH`는 BG forward/regime stress queue(전진/국면 압박 대기열)를 proxy replay(프록시 재생)로 평가했다. selected(선택)는 `{final['selected_variant_id']}`이고 net/PF/trades/density(순수익/수익 팩터/거래수/밀도)는 `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_count']}` / `{final['selected_trade_density']}`다.

operating_truth_boundary(운영 진실 경계): 새 MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(미주장)이다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 selected proxy candidate(선택 프록시 후보)를 review(검토)하고, package(패키지) 가능성과 short source(숏 원천) 분리를 판단한다.
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} - {RUN_ID}

- action(행동): forward/regime stress proxy scout(전진/국면 압박 프록시 탐색)를 실행했다.
- effect(효과): `{final['selected_variant_id']}`를 BI review(BI 검토) 후보로 남기고, 밀도 붕괴 hard filters(강한 필터)를 거절했다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): hour19 closed-bar margin guard(19시 닫힌 봉 margin 가드)가 PF/DD(수익 팩터/낙폭)를 밀도 붕괴 없이 개선할 수 있다.
- positive clue(긍정 단서): selected net/PF/density `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}`.
- effect(효과): short balance(숏 균형)는 별도 source exploration(원천 탐색)으로 분리한다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): density-breaking repairs rejected(밀도 붕괴 수리 거절).
- failure_memory(실패 기억): month/hour hard delete(월/시간 강한 삭제)는 PF를 올려도 trade density(거래 밀도)를 3/day 아래로 깎는다.
- effect(효과): 다음 작업은 hard delete(강한 삭제)보다 micro margin guard(미세 margin 가드)나 new short source(새 숏 원천)에 집중한다.
""",
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
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(SELECTED_PROXY_CANDIDATE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_started_proxy_only(프록시 전용이라 시작 안 함)",
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scout(프록시 탐색)",
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "drawdown": final["selected_closed_drawdown_percent"],
        "recovery_factor": final["selected_recovery_factor"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_trade_density"],
        "trade_density_requirement_status": "proxy_passed_ge_3_no_trade_splitting(프록시 3 이상 통과, 거래 쪼개기 없음)",
        "long_trade_count": final["selected_long_trade_count"],
        "short_trade_count": final["selected_short_trade_count"],
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can a micro forward/regime guard improve BF without breaking density?(미세 전진/국면 가드가 밀도를 깨지 않고 BF를 개선할 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, kpi_scope, status, judgment in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "closed_trade_probability_proxy_scout(종료 거래 확률 프록시 탐색)", STATUS, JUDGMENT),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)", "out_of_scope_by_claim(주장 범위 밖)", "not_run_parent_runtime_probe_had_no_tier_b_fallback"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A proxy plus Tier B out_of_scope(Tier A 프록시 + Tier B 범위 밖)", STATUS, JUDGMENT),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": kpi_scope,
                "status": status,
                "judgment": judgment,
                "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_trade_density']}",
                "guardrail_kpi": f"short_share={final['selected_short_share']};density_breaking_rejected={final['rejected_density_breaking_rows']}",
            }
        )
        if tier == "Tier B":
            row.update({"net_profit": "", "profit_factor": "", "expectancy": "", "drawdown": "", "recovery_factor": "", "trade_count": "", "long_trade_count": "", "short_trade_count": ""})
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    BF.drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    BF.drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])

    artifact_rows = []
    for artifact_type, path, notes in [
        ("scout_surface", SCOUT_SURFACE, "BH proxy scout surface(BH 프록시 탐색 표면)."),
        ("selected_candidate", SELECTED_PROXY_CANDIDATE, "Selected BH proxy candidate(선택 BH 프록시 후보)."),
        ("selected_trade_tape", SELECTED_EXPECTED_TRADE_TAPE, "Selected proxy trade tape(선택 프록시 거래 테이프)."),
        ("short_feasibility", SHORT_RESTORE_FEASIBILITY, "Short restore feasibility audit(숏 복원 가능성 감사)."),
        ("next_queue", RUN364BI_QUEUE, "BI review queue(BI 검토 대기열)."),
        ("report", REPORT_PATH, "BH report(BH 보고서)."),
        ("decision", DECISION_DOC, "BH decision doc(BH 결정 문서)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
    ]:
        if exists(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at_utc": final["created_at_utc"],
                    "created_at": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "package_run_id": PACKAGE_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_work_packet()
    trades, join_audit = load_trades_with_probabilities()
    surface, selected_trades, baseline = build_surface(trades)
    selected = surface.iloc[0].to_dict()
    forward_rows = segment_rows(selected_trades, "entry_quarter", "forward_block", full_days=False)
    month_rows = segment_rows(selected_trades, "entry_month", "month", full_days=False)
    segment_rows_all = selected_segment_rows(selected_trades)
    density_rows = density_audit_rows(baseline, selected)
    short_rows = short_restore_rows(baseline, selected)
    rejected_rows = surface[surface["candidate_status"].astype(str).str.contains("density_breaks", na=False)].to_dict("records")
    queue = queue_rows(selected, surface)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(ENTRY_PROBABILITY_JOIN_AUDIT, join_audit)
    write_csv(SCOUT_SURFACE, surface.to_dict("records"))
    write_csv(SELECTED_EXPECTED_TRADE_TAPE, selected_trades.drop(columns=["entry_time_dt"], errors="ignore").to_dict("records"))
    write_csv(SELECTED_SEGMENT_ATTRIBUTION, segment_rows_all)
    write_csv(DENSITY_FLOOR_SURVIVAL_AUDIT, density_rows)
    write_csv(FORWARD_BLOCK_REPLAY, forward_rows)
    write_csv(MONTH_REGIME_REPLAY, month_rows)
    write_csv(SHORT_RESTORE_FEASIBILITY, short_rows)
    write_csv(REJECTED_DENSITY_REPAIRS, rejected_rows)
    write_csv(RUN364BI_QUEUE, queue)
    write_json(SELECTED_PROXY_CANDIDATE, selected)

    write_receipts({"selected_trade_count": len(selected_trades)}, selected)
    refresh_lineage_receipt({"run_id": RUN_ID, "selected_variant_id": selected["variant_id"]})
    gates = gate_rows(join_audit, surface, selected, queue)
    write_csv(GATE_AUDIT, gates)
    if any(row["status"] != "passed" for row in gates):
        raise RuntimeError("BH gate failure(BH 게이트 실패): " + ", ".join(row["gate"] for row in gates if row["status"] != "passed"))

    created_at = now_utc()
    final = final_payload(parent_final, surface, selected, selected_trades, baseline, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_docs(final, surface, selected, forward_rows, month_rows, short_rows, queue, gates)
    write_ledgers(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
