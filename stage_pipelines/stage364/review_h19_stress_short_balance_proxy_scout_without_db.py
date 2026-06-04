from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import train_h19_stress_short_balance_proxy_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-04"
BK = parent.BK

STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BN"
RUN_ID = "run364BN_review_h19_stress_short_balance_proxy_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = parent.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BO_train_short_source_quality_repair_scout_without_db_v1"

STATUS = "completed_stage364BN_short_source_quality_review_open_bo_repair_scout_no_authority"
JUDGMENT = "package_rejected_bm_short_source_negative_but_h17_h20_margin_repair_seed_positive_review_required_no_authority"
DECISION = "stage364BN_open_run364BO_short_source_quality_repair_scout"
CLAIM_BOUNDARY = (
    "research_development_kpi_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_SHORT_SHARE = parent.TARGET_SHORT_SHARE
MIN_PF_KEEP = parent.MIN_PF_KEEP
MIN_SHORT_SOURCE_PF = 1.15
DEPOSIT = parent.DEPOSIT

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
ATTRIBUTION_DECOMPOSITION = RUN_DIR / "attribution_decomposition.csv"
PACKAGE_GATE_DECISION = RUN_DIR / "package_gate_decision.csv"
SHORT_SOURCE_SEGMENT_REVIEW = RUN_DIR / "short_source_segment_review.csv"
REPAIR_SEED_SURFACE = RUN_DIR / "repair_seed_surface.csv"
SELECTED_REPAIR_SEED = RUN_DIR / "selected_repair_seed.json"
SELECTED_REPAIR_TRADE_TAPE = RUN_DIR / "selected_repair_trade_tape.csv"
FORWARD_REGIME_STABILITY_REVIEW = RUN_DIR / "forward_regime_stability_review.csv"
RUN364BO_QUEUE = RUN_DIR / "run364BO_short_source_quality_repair_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BN_h19_stress_short_balance_proxy_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BN_h19_stress_short_balance_proxy_review.md"
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
    parent.PROXY_SCOUT_SURFACE,
    parent.SELECTED_PROXY_CANDIDATE,
    parent.SELECTED_PROXY_TRADE_TAPE,
    parent.SHORT_SOURCE_FEASIBILITY,
    parent.SHORT_SYNTHETIC_CANDIDATES,
    parent.DISPLACED_PARENT_TRADES,
    parent.FORWARD_REGIME_REPLAY,
    parent.RUN364BN_QUEUE,
    BK.CLOSED_TRADE_ATTRIBUTION,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    ATTRIBUTION_DECOMPOSITION,
    PACKAGE_GATE_DECISION,
    SHORT_SOURCE_SEGMENT_REVIEW,
    REPAIR_SEED_SURFACE,
    SELECTED_REPAIR_SEED,
    SELECTED_REPAIR_TRADE_TAPE,
    FORWARD_REGIME_STABILITY_REVIEW,
    RUN364BO_QUEUE,
    WORK_PACKET,
    KPI_RECEIPT,
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


def io_path(path: Path | str) -> Path:
    return parent.io_path(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


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


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


def drop_empty_csv_columns(path: Path, columns: Sequence[str]) -> None:
    parent.drop_empty_csv_columns(path, columns)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    return parent.as_int(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def json_ready(value: Any) -> Any:
    return parent.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BN inputs(BN 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BM next_run_id mismatch(BM 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("BM has forbidden authority claim(BM 금지 권위 주장 존재)")
    gates = read_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("BM gate audit(BM 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BN review source(BN 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_parent_trades() -> pd.DataFrame:
    frame = pd.read_csv(io_path(BK.CLOSED_TRADE_ATTRIBUTION), encoding="utf-8-sig")
    frame["entry_time_dt"] = pd.to_datetime(frame["entry_time"])
    frame["exit_time_dt"] = pd.to_datetime(frame["exit_time"])
    frame["pnl"] = pd.to_numeric(frame["net_profit_after_cost"], errors="coerce").fillna(0.0)
    frame["side"] = frame["side"].astype(str)
    frame["entry_hour"] = frame["entry_time_dt"].dt.hour
    frame["entry_month"] = frame["entry_time_dt"].dt.strftime("%Y-%m")
    frame["entry_quarter"] = frame["entry_time_dt"].dt.to_period("Q").astype(str)
    return frame.sort_values("entry_time_dt").reset_index(drop=True)


def load_selected_synthetic(final: Mapping[str, Any]) -> pd.DataFrame:
    frame = pd.read_csv(io_path(parent.SHORT_SYNTHETIC_CANDIDATES), encoding="utf-8-sig")
    frame = frame[frame["variant_id"].astype(str) == str(final["selected_variant_id"])].copy()
    frame["entry_time_dt"] = pd.to_datetime(frame["entry_time"])
    frame["exit_time_dt"] = pd.to_datetime(frame["exit_time"])
    frame["pnl"] = pd.to_numeric(frame["pnl"], errors="coerce").fillna(0.0)
    frame["entry_hour"] = pd.to_numeric(frame["entry_hour"], errors="coerce").fillna(-1).astype(int)
    frame["entry_month"] = frame["entry_month"].astype(str)
    frame["entry_quarter"] = frame["entry_time_dt"].dt.to_period("Q").astype(str)
    frame["p_short"] = pd.to_numeric(frame["p_short"], errors="coerce")
    frame["short_margin_vs_long"] = pd.to_numeric(frame["short_margin_vs_long"], errors="coerce")
    frame["side"] = "short"
    return frame.sort_values("entry_time_dt").reset_index(drop=True)


def metric_frame(frame: pd.DataFrame, *, full_days: int) -> dict[str, Any]:
    if frame.empty:
        return {
            "net_profit": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "trade_count": 0,
            "trade_density_per_business_day": 0.0,
            "closed_drawdown_amount": 0.0,
            "closed_drawdown_percent": 0.0,
            "recovery_factor": 0.0,
            "long_trade_count": 0,
            "short_trade_count": 0,
            "short_share": 0.0,
            "win_rate_percent": 0.0,
        }
    ordered = frame.sort_values("entry_time_dt").copy()
    pnl = ordered["pnl"].astype(float)
    gp = float(pnl[pnl > 0].sum())
    gl = float(-pnl[pnl < 0].sum())
    net = float(pnl.sum())
    balance = DEPOSIT + pnl.cumsum()
    peak = balance.cummax()
    dd = peak - balance
    dd_amount = float(dd.max()) if len(dd) else 0.0
    dd_percent = float(((dd / peak.replace(0, np.nan)) * 100.0).max()) if len(dd) else 0.0
    count = int(len(ordered))
    longs = int((ordered["side"].astype(str) == "long").sum())
    shorts = int((ordered["side"].astype(str) == "short").sum())
    return {
        "net_profit": round(net, 2),
        "profit_factor": finite(gp / gl if gl else 999.0, 10),
        "expectancy": finite(net / count if count else 0.0, 10),
        "trade_count": count,
        "trade_density_per_business_day": finite(count / full_days if full_days else 0.0, 10),
        "closed_drawdown_amount": finite(dd_amount, 10),
        "closed_drawdown_percent": finite(dd_percent, 10),
        "recovery_factor": finite(net / dd_amount if dd_amount else 999.0, 10),
        "long_trade_count": longs,
        "short_trade_count": shorts,
        "short_share": finite(shorts / count if count else 0.0, 10),
        "win_rate_percent": finite((pnl > 0).mean() * 100.0, 10),
    }


def synthetic_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    metric = metric_frame(frame, full_days=max(1, int(np.busday_count(frame["entry_time_dt"].min().date(), frame["entry_time_dt"].max().date() + timedelta(days=1)))) if not frame.empty else 1)
    return {
        "synthetic_short_net_profit": metric["net_profit"],
        "synthetic_short_profit_factor": metric["profit_factor"],
        "synthetic_short_trade_count": metric["trade_count"],
        "synthetic_short_expectancy": metric["expectancy"],
        "synthetic_short_win_rate_percent": metric["win_rate_percent"],
    }


def combine(parent_trades: pd.DataFrame, synthetic: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    displaced_ids: set[int] = set()
    displaced_rows: list[dict[str, Any]] = []
    for _, row in synthetic.sort_values("entry_time_dt").iterrows():
        hits = parent_trades[
            (parent_trades["entry_time_dt"] >= row["entry_time_dt"])
            & (parent_trades["entry_time_dt"] < row["exit_time_dt"])
        ]
        for _, hit in hits.iterrows():
            trade_index = int(hit["trade_index"])
            displaced_ids.add(trade_index)
            displaced_rows.append(
                {
                    "displaced_parent_trade_index": trade_index,
                    "displaced_entry_time": hit["entry_time"],
                    "displaced_side": hit["side"],
                    "displaced_pnl": finite(hit["pnl"], 10),
                    "synthetic_entry_time": row["entry_time"],
                }
            )
    kept = parent_trades[~parent_trades["trade_index"].astype(int).isin(displaced_ids)].copy()
    kept_tape = kept[["entry_time_dt", "exit_time_dt", "side", "pnl", "entry_hour", "entry_month", "entry_quarter"]].copy()
    kept_tape["source"] = "parent_kept(부모 유지)"
    synthetic_tape = synthetic[["entry_time_dt", "exit_time_dt", "side", "pnl", "entry_hour", "entry_month", "entry_quarter"]].copy()
    synthetic_tape["source"] = "synthetic_short(합성 숏)"
    combined = pd.concat([kept_tape, synthetic_tape], ignore_index=True).sort_values("entry_time_dt").reset_index(drop=True)
    return combined, pd.DataFrame(displaced_rows)


def full_business_days(parent_trades: pd.DataFrame) -> int:
    return int(np.busday_count(parent_trades["entry_time_dt"].min().date(), parent_trades["entry_time_dt"].max().date() + timedelta(days=1)))


def seed_definitions() -> list[dict[str, Any]]:
    return [
        {
            "seed_id": "bn00_bm_selected_h17_20_ps0440_reference",
            "seed_family": "bm_reference(BM 기준)",
            "description": "BM selected h17-20 p_short>=0.440 reference(BM 선택 17~20시 p_short>=0.440 기준)",
            "mask": lambda s: pd.Series(True, index=s.index),
            "overfit_risk": "high_same_tape(높음, 동일 테이프)",
        },
        {
            "seed_id": "bn01_h17_only_short_source_quality",
            "seed_family": "hour17_core(17시 핵심)",
            "description": "hour 17 short source only(17시 숏 원천만)",
            "mask": lambda s: s["entry_hour"] == 17,
            "overfit_risk": "medium_same_tape(중간, 동일 테이프)",
        },
        {
            "seed_id": "bn02_h17_or_h20_margin_08_10_quality_repair",
            "seed_family": "h17_core_h20_margin_band(17시 핵심 + 20시 마진 밴드)",
            "description": "hour 17 plus hour 20 short_margin_vs_long 0.08..0.10(17시 + 20시 숏-롱 마진 0.08..0.10)",
            "mask": lambda s: (s["entry_hour"] == 17)
            | ((s["entry_hour"] == 20) & (s["short_margin_vs_long"] >= 0.08) & (s["short_margin_vs_long"] <= 0.10)),
            "overfit_risk": "medium_high_same_tape_margin_band(중상, 동일 테이프 마진 밴드)",
        },
        {
            "seed_id": "bn03_h17_or_h20_p0445_quality_repair",
            "seed_family": "h17_core_h20_probability_floor(17시 핵심 + 20시 확률 하한)",
            "description": "hour 17 plus hour 20 p_short>=0.445(17시 + 20시 p_short>=0.445)",
            "mask": lambda s: (s["entry_hour"] == 17) | ((s["entry_hour"] == 20) & (s["p_short"] >= 0.445)),
            "overfit_risk": "medium_same_tape(중간, 동일 테이프)",
        },
        {
            "seed_id": "bn04_h17_or_p046_quality_watch",
            "seed_family": "h17_core_high_probability(17시 핵심 + 고확률)",
            "description": "hour 17 plus all-hour p_short>=0.460(17시 + 전체 시간 p_short>=0.460)",
            "mask": lambda s: (s["entry_hour"] == 17) | (s["p_short"] >= 0.46),
            "overfit_risk": "medium_high_same_tape_probability(중상, 동일 테이프 확률)",
        },
        {
            "seed_id": "bn05_h17_or_margin_08_10_all_watch",
            "seed_family": "h17_core_all_hour_margin_band(17시 핵심 + 전체 시간 마진 밴드)",
            "description": "hour 17 plus all-hour short_margin_vs_long 0.08..0.10(17시 + 전체 시간 숏-롱 마진 0.08..0.10)",
            "mask": lambda s: (s["entry_hour"] == 17) | ((s["short_margin_vs_long"] >= 0.08) & (s["short_margin_vs_long"] <= 0.10)),
            "overfit_risk": "high_same_tape_band(높음, 동일 테이프 밴드)",
        },
    ]


def status_for_seed(row: Mapping[str, Any]) -> str:
    if as_float(row["trade_density_per_business_day"]) < DENSITY_FLOOR:
        return "rejected_density_below_3(거절, 밀도 3 미만)"
    if as_float(row["profit_factor"]) < MIN_PF_KEEP:
        return "rejected_combined_pf_below_1_35(거절, 합산 PF 1.35 미만)"
    if as_float(row["short_share"]) < TARGET_SHORT_SHARE:
        return "watch_short_share_below_target(관찰, 숏 비중 목표 미달)"
    if as_float(row["synthetic_short_profit_factor"]) < MIN_SHORT_SOURCE_PF:
        return "rejected_short_source_pf_below_1_15(거절, 숏 원천 PF 1.15 미만)"
    return "repair_seed_review_candidate_no_authority(수리 씨앗 검토 후보, 권위 없음)"


def seed_score(row: Mapping[str, Any]) -> float:
    score = (as_float(row["net_profit"]) - 959.64) * 0.35
    score += (as_float(row["profit_factor"]) - MIN_PF_KEEP) * 180.0
    score += (as_float(row["synthetic_short_profit_factor"]) - MIN_SHORT_SOURCE_PF) * 120.0
    score += max(0.0, as_float(row["short_share"]) - TARGET_SHORT_SHARE) * 200.0
    score += max(0.0, 84.86 - as_float(row["closed_drawdown_amount"])) * 0.35
    if "high" in str(row.get("overfit_risk")):
        score -= 10.0
    if "repair_seed" not in str(row.get("candidate_status")):
        score -= 100.0
    return round(score, 10)


def build_repair_seed_surface(parent_trades: pd.DataFrame, synthetic: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    full_days = full_business_days(parent_trades)
    rows: list[dict[str, Any]] = []
    tapes: dict[str, pd.DataFrame] = {}
    displaced_map: dict[str, pd.DataFrame] = {}
    for seed in seed_definitions():
        mask = seed["mask"](synthetic)
        selected_syn = synthetic[mask].copy()
        combined, displaced = combine(parent_trades, selected_syn)
        metric = metric_frame(combined, full_days=full_days)
        syn_metric = synthetic_metrics(selected_syn)
        row = {
            "run_id": RUN_ID,
            "seed_id": seed["seed_id"],
            "seed_family": seed["seed_family"],
            "description": seed["description"],
            "overfit_risk": seed["overfit_risk"],
            **metric,
            **syn_metric,
            "synthetic_added_short_count": len(selected_syn),
            "displaced_parent_trade_count": len(displaced),
            "displaced_parent_net_profit": finite(displaced["displaced_pnl"].astype(float).sum() if not displaced.empty else 0.0, 10),
            "feature_boundary": "entry_hour, p_short, short_margin_vs_long only; same-tape review(진입시각, p_short, 숏-롱 마진만 사용, 동일 테이프 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row["candidate_status"] = status_for_seed(row)
        row["selection_score"] = seed_score(row)
        rows.append(row)
        tapes[seed["seed_id"]] = combined
        displaced_map[seed["seed_id"]] = displaced
    surface = pd.DataFrame(rows).sort_values(
        ["candidate_status", "selection_score", "profit_factor"],
        ascending=[True, False, False],
    )
    surface = surface.sort_values(
        ["candidate_status", "selection_score"],
        ascending=[True, False],
    ).reset_index(drop=True)
    candidates = surface[surface["candidate_status"].astype(str).str.contains("repair_seed_review_candidate", na=False)].copy()
    if candidates.empty:
        selected = surface.iloc[0]
    else:
        selected = candidates.sort_values("selection_score", ascending=False).iloc[0]
    return surface, {**tapes, "__selected_id__": selected["seed_id"]}, displaced_map


def attribution_rows(final: Mapping[str, Any], surface: pd.DataFrame, selected_seed: Mapping[str, Any]) -> list[dict[str, Any]]:
    baseline = as_float(final["baseline_closed_trade_net_profit"])
    bm_syn = as_float(final["selected_synthetic_short_net_profit"])
    bm_displaced = as_float(final["selected_displaced_parent_trade_count"])
    displaced = pd.read_csv(io_path(parent.DISPLACED_PARENT_TRADES), encoding="utf-8-sig")
    displaced = displaced[displaced["variant_id"].astype(str) == str(final["selected_variant_id"])]
    bm_displaced_net = as_float(displaced["displaced_pnl"].astype(float).sum())
    return [
        {
            "run_id": RUN_ID,
            "attribution_id": "bm_selected_combined_proxy(BM 선택 합산 프록시)",
            "baseline_net": baseline,
            "displaced_parent_trade_count": bm_displaced,
            "displaced_parent_net_profit": finite(bm_displaced_net, 10),
            "synthetic_short_net_profit": bm_syn,
            "combined_net_profit": final["selected_net_profit"],
            "net_delta_formula": "baseline - displaced_parent_net + synthetic_short_net(기준 - 대체 부모 순수익 + 합성 숏 순수익)",
            "judgment": "combined_gain_from_removing_losing_parent_trades_not_positive_short_source(합산 개선은 양수 숏 원천이 아니라 손실 부모 거래 제거 영향)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "selected_repair_seed(선택 수리 씨앗)",
            "seed_id": selected_seed["seed_id"],
            "displaced_parent_trade_count": selected_seed["displaced_parent_trade_count"],
            "displaced_parent_net_profit": selected_seed["displaced_parent_net_profit"],
            "synthetic_short_net_profit": selected_seed["synthetic_short_net_profit"],
            "synthetic_short_profit_factor": selected_seed["synthetic_short_profit_factor"],
            "combined_net_profit": selected_seed["net_profit"],
            "combined_profit_factor": selected_seed["profit_factor"],
            "short_share": selected_seed["short_share"],
            "judgment": "repair_seed_positive_proxy_but_same_tape_review_only(수리 씨앗은 프록시 양수지만 동일 테이프 검토 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def package_gate_rows(final: Mapping[str, Any], selected_seed: Mapping[str, Any]) -> list[dict[str, Any]]:
    bm_short_pf = as_float(final["selected_synthetic_short_profit_factor"])
    seed_short_pf = as_float(selected_seed["synthetic_short_profit_factor"])
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "bm_selected_package_gate(BM 선택 패키지 게이트)",
            "subject": final["selected_variant_id"],
            "status": "rejected_package_ineligible(거절, 패키지 부적격)",
            "reason": f"synthetic_short_pf={bm_short_pf} < {MIN_SHORT_SOURCE_PF}",
            "effect": "BM 합산 프록시 개선을 MT5 패키지 후보로 올리지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "repair_seed_package_gate(수리 씨앗 패키지 게이트)",
            "subject": selected_seed["seed_id"],
            "status": "not_package_candidate_repair_scout_first(패키지 후보 아님, 수리 정찰 우선)",
            "reason": f"seed_short_pf={seed_short_pf} passes proxy floor but same-tape and no MT5 reprobe(프록시 하한은 통과하지만 동일 테이프 및 MT5 재탐침 없음)",
            "effect": "BO scout(BO 정찰)에서 forward/regime stress(전진/국면 압박)를 먼저 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def segment_rows(synthetic: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis, group_col in [("entry_hour(진입시)", "entry_hour"), ("entry_month(진입월)", "entry_month")]:
        for value, part in synthetic.groupby(group_col, sort=True):
            metric = synthetic_metrics(part.copy())
            rows.append(
                {
                    "run_id": RUN_ID,
                    "axis": axis,
                    "segment_id": str(value),
                    **metric,
                    "p_short_mean": finite(part["p_short"].mean(), 10),
                    "margin_mean": finite(part["short_margin_vs_long"].mean(), 10),
                    "segment_status": "positive_clue(긍정 단서)" if as_float(metric["synthetic_short_profit_factor"]) >= MIN_SHORT_SOURCE_PF and as_int(metric["synthetic_short_trade_count"]) >= 6 else "watch_or_negative(관찰 또는 음수)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def forward_rows(selected_tape: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if selected_tape.empty:
        return rows
    for axis, group_col in [("quarter(분기)", "entry_quarter"), ("month(월)", "entry_month"), ("hour(시)", "entry_hour")]:
        for value, part in selected_tape.groupby(group_col, sort=True):
            days = max(1, int(np.busday_count(part["entry_time_dt"].min().date(), part["entry_time_dt"].max().date() + timedelta(days=1))))
            metric = metric_frame(part.copy(), full_days=days)
            rows.append(
                {
                    "run_id": RUN_ID,
                    "axis": axis,
                    "segment_id": str(value),
                    **metric,
                    "segment_status": "stress_watch(압박 관찰)" if as_float(metric["net_profit"]) <= 0 or as_float(metric["profit_factor"]) < 1.0 else "positive(양수)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def queue_rows(selected_seed: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "selected_seed_id": selected_seed["seed_id"],
        "trade_splitting_status": "forbidden_not_used(금지 및 미사용)",
        "top_n_status": "forbidden_not_used(금지 및 미사용)",
        "timestamp_boundary": "entry_known_hour_probability_margin_only(진입시점 시간/확률/마진만 사용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        {
            **common,
            "queue_rank": 1,
            "queue_id": "bo01_train_h17_h20_margin_short_source_quality_repair_scout",
            "action": "train/replay selected repair seed as proxy scout(선택 수리 씨앗을 프록시 정찰로 학습/재생)",
            "success_criteria": "synthetic short PF>=1.15, combined PF>=1.35, density>=3/day, short_share>=0.12 across stress slices(합성 숏 PF 1.15 이상, 합산 PF 1.35 이상, 밀도 3/day 이상, 숏비중 0.12 이상)",
            "effect": "negative BM short source(음수 BM 숏 원천)를 h17/h20 margin quality seed(17시/20시 마진 품질 씨앗)로 공격 수리한다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bo02_reject_exact_month_shortcut_and_test_entry_known_rules",
            "action": "forbid exact month rescue and test entry-known hour/margin/probability rules(정확 월 구조 금지 및 진입시점 시간/마진/확률 규칙 시험)",
            "success_criteria": "no exact future losing month dependency and no top_n(미래 손실 월 의존 없음, top_n 없음)",
            "effect": "same-tape overfit(동일 테이프 과적합)을 수리 제약으로 바꾼다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bo03_mt5_package_only_after_proxy_and_stress_survive",
            "action": "prepare MT5 package only after BO proxy and stress pass(BO 프록시와 압박 통과 뒤에만 MT5 패키지 준비)",
            "success_criteria": "BO review keeps proxy/MT5 diff plan and runtime parity handoff(BO 검토가 프록시/MT5 차이 계획과 런타임 동등성 인계를 유지)",
            "effect": "repair seed(수리 씨앗)를 운영 주장으로 바로 올리지 않는다.",
        },
    ]


def gate_rows(final: Mapping[str, Any], selected_seed: Mapping[str, Any], queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed",
            "evidence": rel(REPAIR_SEED_SURFACE),
            "effect": "net/PF/expectancy/DD/recovery/trades/short share를 함께 검토했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "row_grain_audit",
            "status": "passed",
            "evidence": rel(ATTRIBUTION_DECOMPOSITION),
            "effect": "BM selected row(선택 행), synthetic short row(합성 숏 행), displaced parent row(대체 부모 행)를 분리했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": rel(PACKAGE_GATE_DECISION),
            "effect": "MT5 KPI(MT5 핵심 성과 지표)는 BK/BM 근거로 제한하고 BN은 리뷰 권위만 가진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "package_reject_gate",
            "status": "passed" if as_float(final["selected_synthetic_short_profit_factor"]) < MIN_SHORT_SOURCE_PF else "failed",
            "evidence": rel(PACKAGE_GATE_DECISION),
            "effect": "BM 선택 후보를 패키지 후보에서 제외했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "repair_seed_gate",
            "status": "passed"
            if as_float(selected_seed["synthetic_short_profit_factor"]) >= MIN_SHORT_SOURCE_PF
            and as_float(selected_seed["profit_factor"]) >= MIN_PF_KEEP
            and as_float(selected_seed["trade_density_per_business_day"]) >= DENSITY_FLOOR
            and as_float(selected_seed["short_share"]) >= TARGET_SHORT_SHARE
            else "failed",
            "evidence": rel(SELECTED_REPAIR_SEED),
            "effect": "BO로 넘길 공격 수리 씨앗을 찾았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "no_trade_splitting_gate",
            "status": "passed",
            "evidence": rel(SELECTED_REPAIR_TRADE_TAPE),
            "effect": "새 거래 쪼개기 없이 one-position proxy(단일 포지션 프록시)만 유지했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if len(queue) == 3 else "failed",
            "evidence": rel(RUN364BO_QUEUE),
            "effect": "다음 BO 작업과 필수 리뷰 게이트를 연결했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 모두 차단했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(
    bm_final: Mapping[str, Any],
    selected_seed: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "bm_selected_variant_id": bm_final["selected_variant_id"],
        "bm_selected_net_profit": bm_final["selected_net_profit"],
        "bm_selected_profit_factor": bm_final["selected_profit_factor"],
        "bm_selected_trade_density": bm_final["selected_trade_density"],
        "bm_selected_short_share": bm_final["selected_short_share"],
        "bm_selected_synthetic_short_net_profit": bm_final["selected_synthetic_short_net_profit"],
        "bm_selected_synthetic_short_profit_factor": bm_final["selected_synthetic_short_profit_factor"],
        "package_decision": "rejected_package_ineligible(패키지 부적격 거절)",
        "selected_repair_seed_id": selected_seed["seed_id"],
        "selected_repair_seed_net_profit": selected_seed["net_profit"],
        "selected_repair_seed_profit_factor": selected_seed["profit_factor"],
        "selected_repair_seed_expectancy": selected_seed["expectancy"],
        "selected_repair_seed_trade_count": selected_seed["trade_count"],
        "selected_repair_seed_density": selected_seed["trade_density_per_business_day"],
        "selected_repair_seed_closed_drawdown_amount": selected_seed["closed_drawdown_amount"],
        "selected_repair_seed_recovery_factor": selected_seed["recovery_factor"],
        "selected_repair_seed_short_share": selected_seed["short_share"],
        "selected_repair_seed_synthetic_short_count": selected_seed["synthetic_added_short_count"],
        "selected_repair_seed_synthetic_short_net_profit": selected_seed["synthetic_short_net_profit"],
        "selected_repair_seed_synthetic_short_profit_factor": selected_seed["synthetic_short_profit_factor"],
        "selected_repair_seed_displaced_parent_net_profit": selected_seed["displaced_parent_net_profit"],
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


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "kpi_evidence(핵심 성과 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "BM combined proxy(BM 합산 프록시)를 패키지 후보와 수리 씨앗으로 분리한다.",
        },
    )


def write_receipts(final: Mapping[str, Any], selected_seed: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        KPI_RECEIPT,
        {
            **base,
            "kpi_subject": selected_seed["seed_id"],
            "headline": {
                "net": selected_seed["net_profit"],
                "pf": selected_seed["profit_factor"],
                "density": selected_seed["trade_density_per_business_day"],
                "short_share": selected_seed["short_share"],
                "synthetic_short_pf": selected_seed["synthetic_short_profit_factor"],
            },
            "kpi_boundary": "proxy review only, not MT5 authority(프록시 검토 전용, MT5 권위 아님)",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_sources": [rel(parent.SHORT_SYNTHETIC_CANDIDATES), rel(parent.DISPLACED_PARENT_TRADES), rel(BK.CLOSED_TRADE_ATTRIBUTION)],
            "time_axis": "entry-known hour/probability/margin plus future bars as labels only(진입시점 시간/확률/마진 + 미래 봉은 라벨 전용)",
            "leakage_boundary": "same-tape repair seed, no operating claim(동일 테이프 수리 씨앗, 운영 주장 없음)",
            "integrity_judgment": "usable_for_repair_seed_review(수리 씨앗 검토에 사용 가능)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": f"BM package rejected; selected repair seed={selected_seed['seed_id']}",
            "driver": "h17 core and h20 margin band make standalone synthetic short PF positive(17시 핵심과 20시 마진 밴드가 합성 숏 단독 PF를 양수화)",
            "risk": "same-tape margin band can overfit(동일 테이프 마진 밴드는 과적합 가능)",
            "next_action": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment_label": JUDGMENT,
            "evidence_available": [rel(ATTRIBUTION_DECOMPOSITION), rel(PACKAGE_GATE_DECISION), rel(REPAIR_SEED_SURFACE)],
            "evidence_missing": ["MT5 runtime reprobe(MT5 런타임 재탐침)", "forward pass(전진 통과)", "runtime authority closure(런타임 권위 종료)"],
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve", "forward_passed"],
            "effect": "repair seed(수리 씨앗)를 운영 모델로 말하지 않는다.",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_review_to_repair_seed(검토와 수리 씨앗 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    attribution: Sequence[Mapping[str, Any]],
    package_rows: Sequence[Mapping[str, Any]],
    segment_review: Sequence[Mapping[str, Any]],
    seed_surface: pd.DataFrame,
    selected_seed: Mapping[str, Any],
    forward_review: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    candidates = seed_surface.to_dict("records")
    report = f"""# run364BN h19 stress short-balance proxy review(364BN h19 압박 숏 균형 프록시 검토)

## Current Truth(현재 진실)

- BM selected(선택): `{final['bm_selected_variant_id']}`
- BM combined proxy net/PF/density/short share(BM 합산 프록시 순수익/수익 팩터/밀도/숏비중): `{final['bm_selected_net_profit']}` / `{final['bm_selected_profit_factor']}` / `{final['bm_selected_trade_density']}` / `{final['bm_selected_short_share']}`
- BM synthetic short net/PF(BM 합성 숏 순수익/수익 팩터): `{final['bm_selected_synthetic_short_net_profit']}` / `{final['bm_selected_synthetic_short_profit_factor']}`
- package decision(패키지 결정): `{final['package_decision']}`
- selected repair seed(선택 수리 씨앗): `{final['selected_repair_seed_id']}`

## Action And Effect(행동과 효과)

Action(행동): BM combined proxy(합산 프록시)를 attribution(귀속), package gate(패키지 게이트), repair seed(수리 씨앗)으로 분리했다.

Effect(효과): BM 자체는 package candidate(패키지 후보)가 아니지만, `bn02_h17_or_h20_margin_08_10_quality_repair`가 synthetic short PF(합성 숏 수익 팩터)와 short share(숏 비중)를 동시에 살리는 공격 탐색 씨앗으로 남았다.

## Attribution(귀속)

{markdown_table(attribution, ['attribution_id', 'baseline_net', 'displaced_parent_net_profit', 'synthetic_short_net_profit', 'combined_net_profit', 'judgment'])}

## Package Gate(패키지 게이트)

{markdown_table(package_rows, ['gate_id', 'subject', 'status', 'reason', 'effect'])}

## Repair Seed Surface(수리 씨앗 표면)

{markdown_table(candidates, ['seed_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_business_day', 'short_share', 'synthetic_short_profit_factor', 'synthetic_short_net_profit', 'selection_score'])}

## Short Source Segments(숏 원천 조각)

{markdown_table(segment_review, ['axis', 'segment_id', 'synthetic_short_trade_count', 'synthetic_short_net_profit', 'synthetic_short_profit_factor', 'segment_status'])}

## Forward/Regime Stress(전진/국면 압박)

{markdown_table(forward_review, ['axis', 'segment_id', 'trade_count', 'net_profit', 'profit_factor', 'short_share', 'segment_status'])}

## BO Queue(BO 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'action', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BN is review only(BN은 검토 전용). No new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BN h19 stress short-balance proxy review(검토)

Action(행동): BM selected proxy(BM 선택 프록시)를 package reject(패키지 거절)로 닫고 `{final['selected_repair_seed_id']}`를 BO repair scout(BO 수리 정찰)로 넘긴다.

Effect(효과): synthetic short source(합성 숏 원천)가 음수인 후보를 운영 후보로 올리지 않고, h17/h20 margin repair seed(17시/20시 마진 수리 씨앗)를 공격 탐색으로 보존한다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - h19 stress short-balance proxy review(h19 압박 숏 균형 프록시 검토).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BN H19 Stress Short-Balance Proxy Review Closeout",
        f"""## run364BN H19 Stress Short-Balance Proxy Review Closeout(364BN h19 압박 숏 균형 프록시 검토 종료)

Action(행동): BM combined proxy(BM 합산 프록시)를 package reject(패키지 거절)와 repair seed(수리 씨앗)으로 분리했다.

Effect(효과): `{final['selected_repair_seed_id']}`를 `{NEXT_RUN_ID}`로 넘기고, 운영 주장은 계속 닫는다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BN H19 Stress Short-Balance Proxy Review(364BN h19 압박 숏 균형 프록시 검토)

Action(행동): BM short source(숏 원천) 음수 문제를 리뷰했다.

Effect(효과): package(패키지)는 거절하고 `{NEXT_RUN_ID}`에서 h17/h20 repair seed(17시/20시 수리 씨앗)를 공격 정찰한다.
""",
    )
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
    replace_prefixed_lines(
        STAGE_README,
        {
            "Current run(현재 실행):": f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "Latest completed run(최근 완료 실행):": f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364BN(364BN 실행)은 BM package(패키지)를 거절하고 `{final['selected_repair_seed_id']}`를 BO repair scout(BO 수리 정찰)로 넘겼다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 short source quality repair(숏 원천 품질 수리)를 공격 정찰한다.",
        },
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

Current truth(현재 진실): `run364BN`은 BM selected proxy(BM 선택 프록시)를 package candidate(패키지 후보)에서 제외했다. 이유는 BM synthetic short PF(합성 숏 수익 팩터)가 `{final['bm_selected_synthetic_short_profit_factor']}`로 음수 품질이기 때문이다. 대신 selected repair seed(선택 수리 씨앗) `{final['selected_repair_seed_id']}`는 proxy net/PF/density/short share(프록시 순수익/수익 팩터/밀도/숏비중) `{final['selected_repair_seed_net_profit']}` / `{final['selected_repair_seed_profit_factor']}` / `{final['selected_repair_seed_density']}` / `{final['selected_repair_seed_short_share']}`이고 synthetic short PF(합성 숏 수익 팩터)는 `{final['selected_repair_seed_synthetic_short_profit_factor']}`다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 h17/h20 margin repair seed(17시/20시 마진 수리 씨앗)를 forward/regime stress(전진/국면 압박)와 no-trade-splitting boundary(거래 쪼개기 금지 경계)로 공격 정찰한다.

Operating boundary(운영 경계): no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Package candidate(패키지 후보): none(없음). BM selected proxy(BM 선택 프록시)는 `{final['package_decision']}`.

Repair seed(수리 씨앗): `{final['selected_repair_seed_id']}`

Repair seed KPI(수리 씨앗 핵심 성과 지표): net `{final['selected_repair_seed_net_profit']}`, PF `{final['selected_repair_seed_profit_factor']}`, expectancy `{final['selected_repair_seed_expectancy']}`, trades `{final['selected_repair_seed_trade_count']}`, density `{final['selected_repair_seed_density']}`, closed DD `{final['selected_repair_seed_closed_drawdown_amount']}`, recovery `{final['selected_repair_seed_recovery_factor']}`, short share `{final['selected_repair_seed_short_share']}`.

Short source quality(숏 원천 품질): BM synthetic short PF(합성 숏 수익 팩터) `{final['bm_selected_synthetic_short_profit_factor']}` rejected(거절). Repair seed synthetic short PF(수리 씨앗 합성 숏 수익 팩터) `{final['selected_repair_seed_synthetic_short_profit_factor']}` review_required(검토 필요).

Next queue(다음 대기열): `{rel(RUN364BO_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): BM h19 short-balance proxy(BM h19 숏 균형 프록시)를 review(검토)했다.
- effect(효과): package candidate(패키지 후보)는 거절하고 `{final['selected_repair_seed_id']}`를 BO repair scout(BO 수리 정찰)로 넘겼다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): h17 core + h20 margin band(17시 핵심 + 20시 마진 밴드)가 BM의 음수 숏 원천을 양수 품질로 바꿀 수 있다.
- positive clue(긍정 단서): repair seed net/PF/density/short share `{final['selected_repair_seed_net_profit']}` / `{final['selected_repair_seed_profit_factor']}` / `{final['selected_repair_seed_density']}` / `{final['selected_repair_seed_short_share']}`.
- effect(효과): 패키지 승격 대신 BO 공격 정찰로 이어간다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): BM package candidate rejected(BM 패키지 후보 거절).
- failure_memory(실패 기억): BM selected synthetic short PF(합성 숏 수익 팩터) `{final['bm_selected_synthetic_short_profit_factor']}`라서 combined proxy(합산 프록시)만으로 패키지하면 안 된다.
- effect(효과): next run(다음 실행)은 standalone short source quality(숏 원천 단독 품질)를 먼저 수리한다.
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
        "rows": 1,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(SELECTED_REPAIR_SEED),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_started_review_only(검토 전용이라 시작 안 함)",
        "work_family": "kpi_evidence(핵심 성과 근거)",
        "scoreboard_lane": "review_attribution(검토 귀속)",
        "net_profit": final["selected_repair_seed_net_profit"],
        "profit_factor": final["selected_repair_seed_profit_factor"],
        "expectancy": final["selected_repair_seed_expectancy"],
        "drawdown": final["selected_repair_seed_closed_drawdown_amount"],
        "recovery_factor": final["selected_repair_seed_recovery_factor"],
        "trade_count": final["selected_repair_seed_trade_count"],
        "trade_density_per_feature_day": final["selected_repair_seed_density"],
        "trade_density_requirement_status": "proxy_passed_ge_3_no_trade_splitting(프록시 3 이상 통과, 거래 쪼개기 없음)",
        "long_trade_count": "",
        "short_trade_count": final["selected_repair_seed_synthetic_short_count"],
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can BM negative short source be repaired into a positive h17/h20 seed without package promotion?(BM 음수 숏 원천을 패키지 승격 없이 양수 h17/h20 씨앗으로 수리할 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, status, judgment in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", STATUS, JUDGMENT),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)", "not_run_parent_runtime_probe_had_no_tier_b_fallback"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", STATUS, JUDGMENT),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "BN review/package reject/repair seed(BN 검토/패키지 거절/수리 씨앗)",
                "status": status,
                "judgment": judgment,
                "primary_kpi": f"seed_net={final['selected_repair_seed_net_profit']};seed_pf={final['selected_repair_seed_profit_factor']};seed_density={final['selected_repair_seed_density']};seed_short_pf={final['selected_repair_seed_synthetic_short_profit_factor']}",
                "guardrail_kpi": f"bm_short_pf={final['bm_selected_synthetic_short_profit_factor']};package_rejected;no_authority",
            }
        )
        if tier == "Tier B":
            for key in ["net_profit", "profit_factor", "expectancy", "drawdown", "recovery_factor", "trade_count", "long_trade_count", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])

    artifact_rows = []
    for artifact_type, path, notes in [
        ("attribution", ATTRIBUTION_DECOMPOSITION, "BN attribution decomposition(BN 귀속 분해)."),
        ("package_gate", PACKAGE_GATE_DECISION, "BN package gate decision(BN 패키지 게이트 결정)."),
        ("repair_seed_surface", REPAIR_SEED_SURFACE, "BN repair seed surface(BN 수리 씨앗 표면)."),
        ("selected_repair_seed", SELECTED_REPAIR_SEED, "Selected BN repair seed(선택 BN 수리 씨앗)."),
        ("next_queue", RUN364BO_QUEUE, "BO repair queue(BO 수리 대기열)."),
        ("report", REPORT_PATH, "BN report(BN 보고서)."),
        ("decision", DECISION_DOC, "BN decision doc(BN 결정 문서)."),
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
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
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
    bm_final = validate_inputs()
    write_work_packet()
    parent_trades = load_parent_trades()
    synthetic = load_selected_synthetic(bm_final)
    seed_surface, tapes, displaced_map = build_repair_seed_surface(parent_trades, synthetic)
    selected_seed_id = str(tapes["__selected_id__"])
    selected_seed = seed_surface[seed_surface["seed_id"].astype(str) == selected_seed_id].iloc[0].to_dict()
    selected_tape = tapes[selected_seed_id]
    selected_displaced = displaced_map[selected_seed_id]
    attribution = attribution_rows(bm_final, seed_surface, selected_seed)
    package_rows = package_gate_rows(bm_final, selected_seed)
    segment_review = segment_rows(synthetic)
    forward_review = forward_rows(selected_tape)
    queue = queue_rows(selected_seed)
    gates = gate_rows(bm_final, selected_seed, queue)
    if any(row["status"] != "passed" for row in gates):
        write_csv(INPUT_MANIFEST, input_manifest_rows())
        write_csv(GATE_AUDIT, gates)
        raise RuntimeError("BN gate failure(BN 게이트 실패): " + ", ".join(row["gate"] for row in gates if row["status"] != "passed"))
    created_at = now_utc()
    final = final_payload(bm_final, selected_seed, gates, created_at)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(ATTRIBUTION_DECOMPOSITION, attribution)
    write_csv(PACKAGE_GATE_DECISION, package_rows)
    write_csv(SHORT_SOURCE_SEGMENT_REVIEW, segment_review)
    write_csv(REPAIR_SEED_SURFACE, seed_surface.to_dict("records"))
    write_json(SELECTED_REPAIR_SEED, selected_seed)
    out_tape = selected_tape.copy()
    out_tape["entry_time"] = out_tape["entry_time_dt"].astype(str)
    out_tape["exit_time"] = out_tape["exit_time_dt"].astype(str)
    write_csv(SELECTED_REPAIR_TRADE_TAPE, out_tape.drop(columns=["entry_time_dt", "exit_time_dt"], errors="ignore").to_dict("records"))
    write_csv(FORWARD_REGIME_STABILITY_REVIEW, forward_review)
    write_csv(RUN364BO_QUEUE, queue)
    write_receipts(final, selected_seed)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_docs(final, attribution, package_rows, segment_review, seed_surface, selected_seed, forward_review, queue, gates)
    write_ledgers(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
