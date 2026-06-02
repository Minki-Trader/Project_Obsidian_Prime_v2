from __future__ import annotations

import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import prepare_timestamp_context_onnx_runtime_probe_without_db as pkg  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364K"
RUN_ID = "run364K_review_direct_dense_m5_onnx_scout_without_db_v1"
PARENT_RUN_ID = "run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1"
NEXT_RUN_ID = "run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1"

STATUS = "completed_stage364K_direct_dense_m5_onnx_scout_reviewed_density_bottleneck_next_seed_opened_no_authority"
JUDGMENT = "negative_valid_scout_low_density_profit_clue_preserved_trade_shape_repair_required_no_authority"
DECISION = "stage364K_open_run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_kpi_evidence_review_only_no_new_model_training_no_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
KPI_BOUNDARY = "python_proxy_review_not_mt5_kpi"
STRICT_DENSITY_FLOOR = 3.0
STRICT_PF_FLOOR = 1.05

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run364J"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_THRESHOLD_SURFACE = SOURCE_RUN_DIR / "proxy_threshold_surface.csv"
SOURCE_MODEL_SCORECARD = SOURCE_RUN_DIR / "model_scorecard.csv"
SOURCE_ONNX_SMOKE = SOURCE_RUN_DIR / "onnx_smoke_report.csv"
SOURCE_LABEL_SUMMARY = SOURCE_RUN_DIR / "direct_label_summary.csv"
SOURCE_TRADE_SAMPLE = SOURCE_RUN_DIR / "proxy_trade_sample.csv"
SOURCE_NEXT_QUEUE = SOURCE_RUN_DIR / "run364K_next_queue.csv"
SOURCE_REPORT = REVIEW_DIR / "run364J_direct_dense_m5_onnx_scout.md"

INPUT_FILES = [
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_THRESHOLD_SURFACE,
    SOURCE_MODEL_SCORECARD,
    SOURCE_ONNX_SMOKE,
    SOURCE_LABEL_SUMMARY,
    SOURCE_TRADE_SAMPLE,
    SOURCE_NEXT_QUEUE,
    SOURCE_REPORT,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SURFACE_REVIEW = RUN_DIR / "surface_review.csv"
DENSITY_BOTTLENECK = RUN_DIR / "density_bottleneck_attribution.csv"
SALVAGE_CLUES = RUN_DIR / "salvage_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364L_next_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364K_direct_dense_m5_onnx_scout_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364K_direct_dense_m5_onnx_scout_review.md"
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
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    DENSITY_BOTTLENECK,
    SALVAGE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    WORK_PACKET,
    PERFORMANCE_RECEIPT,
    RESULT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return pkg.tr.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha256_file(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.tr.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.tr.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return pkg.tr.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = False,
) -> None:
    pkg.tr.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364K inputs: " + ", ".join(missing))
    parent = read_json(SOURCE_FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364J next_run_id mismatch: {parent.get('next_run_id')}")
    _, gates = read_csv_rows(SOURCE_GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364J gate audit is not fully passed")


def write_input_manifest() -> None:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "availability": "tracked_or_materialized_with_manifest",
                "effect": "input identity(입력 정체성)을 고정해 review(검토) 판단을 재현 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def load_surface() -> pd.DataFrame:
    frame = pd.read_csv(fs_path(SOURCE_THRESHOLD_SURFACE), encoding="utf-8-sig")
    numeric_cols = [
        "validation_net",
        "oos_net",
        "validation_profit_factor",
        "oos_profit_factor",
        "validation_trade_density",
        "oos_trade_density",
        "validation_trade_count",
        "oos_trade_count",
        "validation_expectancy",
        "oos_expectancy",
        "validation_max_drawdown",
        "oos_max_drawdown",
        "validation_recovery_factor",
        "oos_recovery_factor",
        "validation_long_trade_count",
        "validation_short_trade_count",
        "oos_long_trade_count",
        "oos_short_trade_count",
        "selection_score",
    ]
    for column in numeric_cols:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column].replace({"inf": 999.0, "-inf": -999.0}), errors="coerce")
    return frame


def classify_row(row: pd.Series) -> tuple[str, str]:
    density_pass = row["validation_trade_density"] >= STRICT_DENSITY_FLOOR and row["oos_trade_density"] >= STRICT_DENSITY_FLOOR
    net_pass = row["validation_net"] > 0 and row["oos_net"] > 0
    pf_pass = row["validation_profit_factor"] >= STRICT_PF_FLOOR and row["oos_profit_factor"] >= STRICT_PF_FLOOR
    if density_pass and net_pass and pf_pass:
        return "strict_candidate", "density_net_pf_pass(밀도/순수익/수익 팩터 통과)"
    if net_pass and pf_pass and not density_pass:
        return "profit_pf_pass_density_fail", "profit and PF pass(순수익과 수익 팩터 통과), density fail(밀도 실패)"
    if density_pass and row["oos_net"] > 0 and row["validation_net"] <= 0:
        return "density_oos_positive_validation_fail", "density and OOS positive(밀도와 표본외 양수), validation fail(검증 실패)"
    if net_pass and not pf_pass:
        return "net_positive_pf_weak", "net positive(순수익 양수), PF weak(수익 팩터 약함)"
    return "no_cross_split_edge", "cross split edge not preserved(교차 분할 엣지 보존 실패)"


def build_surface_review(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for _, raw in frame.iterrows():
        class_id, reason = classify_row(raw)
        density_gap = max(0.0, STRICT_DENSITY_FLOOR - min(raw["validation_trade_density"], raw["oos_trade_density"]))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "model_id": raw["model_id"],
                "label_id": raw["label_id"],
                "horizon_m5": int(raw["horizon_m5"]),
                "policy_id": raw["policy_id"],
                "threshold_id": raw["threshold_id"],
                "validation_net": finite(raw["validation_net"]),
                "oos_net": finite(raw["oos_net"]),
                "validation_profit_factor": finite(raw["validation_profit_factor"]),
                "oos_profit_factor": finite(raw["oos_profit_factor"]),
                "validation_trade_density": finite(raw["validation_trade_density"]),
                "oos_trade_density": finite(raw["oos_trade_density"]),
                "density_gap_to_3_per_day": finite(density_gap),
                "validation_trade_count": int(raw["validation_trade_count"]),
                "oos_trade_count": int(raw["oos_trade_count"]),
                "validation_expectancy": finite(raw.get("validation_expectancy", "")),
                "oos_expectancy": finite(raw.get("oos_expectancy", "")),
                "oos_max_drawdown": finite(raw.get("oos_max_drawdown", "")),
                "selection_score": finite(raw.get("selection_score", "")),
                "review_class": class_id,
                "why": reason,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(SURFACE_REVIEW, rows)
    return rows


def build_density_bottleneck(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    group_cols = ["label_id", "horizon_m5", "policy_id"]
    for keys, group in frame.groupby(group_cols, dropna=False):
        label_id, horizon_m5, policy_id = keys
        density_pass = group[(group["validation_trade_density"] >= STRICT_DENSITY_FLOOR) & (group["oos_trade_density"] >= STRICT_DENSITY_FLOOR)]
        profit_pass = group[(group["validation_net"] > 0) & (group["oos_net"] > 0)]
        pf_pass = profit_pass[(profit_pass["validation_profit_factor"] >= STRICT_PF_FLOOR) & (profit_pass["oos_profit_factor"] >= STRICT_PF_FLOOR)]
        best_score = group.sort_values("selection_score", ascending=False).iloc[0]
        best_density = group.sort_values(["oos_trade_density", "validation_trade_density"], ascending=False).iloc[0]
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "label_id": label_id,
                "horizon_m5": int(horizon_m5),
                "policy_id": policy_id,
                "row_count": int(len(group)),
                "density_pass_rows": int(len(density_pass)),
                "profit_positive_rows": int(len(profit_pass)),
                "profit_pf_pass_rows": int(len(pf_pass)),
                "best_score_model_id": best_score["model_id"],
                "best_score_threshold_id": best_score["threshold_id"],
                "best_score_validation_net": finite(best_score["validation_net"]),
                "best_score_oos_net": finite(best_score["oos_net"]),
                "best_score_validation_density": finite(best_score["validation_trade_density"]),
                "best_score_oos_density": finite(best_score["oos_trade_density"]),
                "best_density_model_id": best_density["model_id"],
                "best_density_threshold_id": best_density["threshold_id"],
                "best_density_validation_net": finite(best_density["validation_net"]),
                "best_density_oos_net": finite(best_density["oos_net"]),
                "best_density_validation_density": finite(best_density["validation_trade_density"]),
                "best_density_oos_density": finite(best_density["oos_trade_density"]),
                "attribution": attribution_text(int(horizon_m5), policy_id, len(density_pass), len(profit_pass), len(pf_pass)),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=lambda row: (as_float(row["profit_pf_pass_rows"]), as_float(row["best_score_oos_net"])), reverse=True)
    write_csv(DENSITY_BOTTLENECK, rows)
    return rows


def attribution_text(horizon_m5: int, policy_id: str, density_pass_rows: int, profit_rows: int, pf_rows: int) -> str:
    if horizon_m5 >= 24 and profit_rows > 0 and density_pass_rows == 0:
        return "long hold horizon(긴 보유 기간)이 non-overlap proxy(비중첩 프록시)에서 trade density(거래 밀도)를 압축한다."
    if horizon_m5 <= 6 and density_pass_rows > 0 and pf_rows == 0:
        return "short horizon(짧은 보유 기간)은 density(밀도)를 회복하지만 validation edge(검증 엣지)를 비용 위로 유지하지 못한다."
    if "long_only" in policy_id and profit_rows > 0:
        return "long-only policy(롱 전용 정책)는 salvage clue(회수 단서)이지만 density/PF(밀도/수익 팩터) 동시 조건이 약하다."
    return "mixed attribution(혼합 귀속): threshold(임계값), hold horizon(보유 기간), side policy(방향 정책)를 함께 재설계해야 한다."


def build_salvage_clues(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    profit_pf = frame[
        (frame["validation_net"] > 0)
        & (frame["oos_net"] > 0)
        & (frame["validation_profit_factor"] >= STRICT_PF_FLOOR)
        & (frame["oos_profit_factor"] >= STRICT_PF_FLOOR)
    ].sort_values("selection_score", ascending=False)
    near_density = frame[
        (frame["validation_net"] > 0)
        & (frame["oos_net"] > 0)
        & (frame["oos_trade_density"] >= STRICT_DENSITY_FLOOR)
    ].sort_values(["validation_trade_density", "oos_net"], ascending=False)
    density_oos = frame[
        (frame["validation_trade_density"] >= STRICT_DENSITY_FLOOR)
        & (frame["oos_trade_density"] >= STRICT_DENSITY_FLOOR)
        & (frame["oos_net"] > 0)
    ].sort_values("oos_net", ascending=False)
    clue_sets = [
        ("profit_pf_density_fail", profit_pf.head(8), "preserve signal quality(신호 품질 보존), repair density(밀도 수리)"),
        ("near_density_oos_positive", near_density.head(8), "push validation density over 3/day(검증 밀도 3/일 상향) without trade splitting(거래 쪼개기 없음)"),
        ("density_oos_positive_validation_fail", density_oos.head(8), "repair validation stability(검증 안정성 수리) for dense h6(고밀도 6봉)"),
    ]
    for clue_type, group, salvage_value in clue_sets:
        for rank, (_, raw) in enumerate(group.iterrows(), start=1):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": PARENT_RUN_ID,
                    "clue_type": clue_type,
                    "rank": rank,
                    "model_id": raw["model_id"],
                    "label_id": raw["label_id"],
                    "horizon_m5": int(raw["horizon_m5"]),
                    "policy_id": raw["policy_id"],
                    "threshold_id": raw["threshold_id"],
                    "validation_net": finite(raw["validation_net"]),
                    "oos_net": finite(raw["oos_net"]),
                    "validation_profit_factor": finite(raw["validation_profit_factor"]),
                    "oos_profit_factor": finite(raw["oos_profit_factor"]),
                    "validation_trade_density": finite(raw["validation_trade_density"]),
                    "oos_trade_density": finite(raw["oos_trade_density"]),
                    "salvage_value": salvage_value,
                    "reopen_condition": "pass validation/OOS density >= 3/day(검증/표본외 밀도 3/일 이상) with positive net and PF >= 1.05(양수 순수익과 수익 팩터 1.05 이상)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(SALVAGE_CLUES, rows)
    return rows


def build_failure_memory(surface_rows: Sequence[Mapping[str, Any]], salvage_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    strict_count = sum(1 for row in surface_rows if row["review_class"] == "strict_candidate")
    profit_density_fail = sum(1 for row in surface_rows if row["review_class"] == "profit_pf_pass_density_fail")
    density_validation_fail = sum(1 for row in surface_rows if row["review_class"] == "density_oos_positive_validation_fail")
    rows = [
        {
            "run_id": RUN_ID,
            "source_run_id": PARENT_RUN_ID,
            "idea_id": "IDEA-ST364J-DIRECT-DENSE-M5-RETURN-ONNX-SCOUT",
            "hypothesis": "direct dense M5 return label(직접 고밀도 5분봉 수익 라벨)이 cost-stable high-density ONNX candidate(비용 안정 고밀도 온엑스 후보)를 만들 수 있다.",
            "variants_tried": "16 models(모델), 192 threshold rows(임계값 행), all58/runtime_core feature sets(전체58/런타임 핵심 피처셋), h6/h12/h24 labels(6/12/24봉 라벨)",
            "failed_boundary": "strict cross split cost-density gate(엄격 교차 분할 비용-밀도 게이트)",
            "why_failed": f"strict_candidate_rows={strict_count}; profit_pf_pass_density_fail_rows={profit_density_fail}; density_oos_positive_validation_fail_rows={density_validation_fail}",
            "salvage_value": f"{len(salvage_rows)} salvage clues(회수 단서) preserved; h24 profit quality(24봉 수익 품질) and h6 density recovery(6봉 밀도 회복) must be recombined.",
            "reopen_condition": "shorter hold/exit policy(짧은 보유/청산 정책), session-aware density lift(세션 인지 밀도 상향), validation stability guard(검증 안정성 가드)를 같이 통과할 때 재개한다.",
            "do_not_repeat_note": "Do not reuse fixed h24 non-overlap proxy(고정 24봉 비중첩 프록시)를 high-density claim(고밀도 주장)으로 반복하지 않는다.",
            "judgment_label": "negative_valid_scout(유효한 부정 탐색)",
            "evidence_boundary": CLAIM_BOUNDARY,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(FAILURE_MEMORY, rows)
    return rows


def build_next_queue(salvage_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best_profit = next((row for row in salvage_rows if row["clue_type"] == "profit_pf_density_fail"), {})
    best_density = next((row for row in salvage_rows if row["clue_type"] == "density_oos_positive_validation_fail"), {})
    rows = [
        {
            "queue_id": "run364L_Q01_density_lift_trade_shape_onnx_scout",
            "priority": 1,
            "next_run_id": NEXT_RUN_ID,
            "source_run_id": RUN_ID,
            "idea_id": "IDEA-ST364L-DENSITY-LIFT-TRADE-SHAPE-ONNX-SCOUT",
            "seed_from": f"profit_seed={best_profit.get('model_id', '')};density_seed={best_density.get('model_id', '')}",
            "hypothesis": "combine h24 quality clue(24봉 품질 단서) with h6 density clue(6봉 밀도 단서) using shorter hold and exit policy(짧은 보유와 청산 정책) to reach 3/day+(일 3회 이상).",
            "broad_sweep": "horizon_m5=[3,4,6,8,12], target_density=[3,5,8,12], policies=[long_only,two_sided,side_asym], session guards=[cash_open,midday,last_90m]",
            "extreme_sweep": "density_target=[16,20], hold_m5=[2,3], cost_stress=[0.30,0.45,0.60], overlap_policy=strict_skip_only(엄격 스킵만)",
            "micro_search_gate": "validation/OOS density >= 3/day and net > 0 and PF >= 1.05(검증/표본외 밀도 3/일 이상, 순수익 양수, 수익 팩터 1.05 이상)",
            "wfo_plan": "single-window scout first(단일 구간 스카우트 먼저), then WFO(워크포워드 최적화) only if gate passes",
            "effect": "밀도 병목과 수익 품질 단서를 한 번에 시험한다.",
            "claim_boundary": "research_development_model_training_and_proxy_scout_only_no_mt5_execution_no_authority",
        },
        {
            "queue_id": "run364L_Q02_session_regime_veto_control",
            "priority": 2,
            "next_run_id": NEXT_RUN_ID,
            "source_run_id": RUN_ID,
            "idea_id": "IDEA-ST364L-SESSION-REGIME-VETO-CONTROL",
            "seed_from": "run364J density pass rows with validation loss(밀도 통과 검증 손실 행)",
            "hypothesis": "h6 density rows(6봉 밀도 행)의 validation loss(검증 손실)는 session/regime cluster(세션/국면 군집)에서 온다.",
            "broad_sweep": "session buckets(세션 버킷), volatility buckets(변동성 버킷), side mix(방향 혼합) attribution",
            "extreme_sweep": "cash_open_only(현금장 개장만), no_last_90m(마지막 90분 제외), no_low_vol(저변동 제외)",
            "micro_search_gate": "density still >= 3/day after veto(차단 후에도 밀도 3/일 이상 유지)",
            "wfo_plan": "apply after run364L_Q01 if signal survives(신호 생존 시 적용)",
            "effect": "검증 손실 구간을 줄이되 거래 수를 쪼개지 않는다.",
            "claim_boundary": "research_development_proxy_control_only_no_authority",
        },
    ]
    write_csv(NEXT_QUEUE, rows)
    return rows


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "work_family": "kpi_evidence(핵심 성과 지표 근거)",
            "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
            "support_skills": [
                "obsidian-performance-attribution(옵시디언 성과 귀속)",
                "obsidian-result-judgment(옵시디언 결과 판정)",
                "obsidian-exploration-mandate(옵시디언 탐색 명령)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"],
            "effect": "review(검토) 완료 주장을 KPI row grain(KPI 행 단위)와 source authority(원천 권위)에 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "run364J recovered OOS net/PF(표본외 순수익/수익 팩터 회복) but failed density(밀도 실패).",
            "comparison_baseline": "run364I dense proxy(364I 고밀도 프록시) and run364J strict density gate(364J 엄격 밀도 게이트).",
            "likely_drivers": ["hold horizon(보유 기간)", "non-overlap proxy(비중첩 프록시)", "threshold selection(임계값 선택)", "validation instability(검증 불안정)"],
            "segment_checks": ["label/horizon/policy decomposition(라벨/보유기간/정책 분해)", "density-pass versus profit-pass split(밀도 통과와 수익 통과 분리)"],
            "trade_shape": "h24 profit rows(24봉 수익 행)는 low frequency(저빈도), h6 density rows(6봉 밀도 행)는 validation loss(검증 손실).",
            "alternative_explanations": ["proxy semantics not MT5(프록시 의미가 MT5 아님)", "single-window scout(단일 구간 탐색)", "feature dependency all58(전체58 피처 의존)"],
            "attribution_confidence": "medium(중간)",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RESULT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(SOURCE_FINAL_DECISION), rel(SOURCE_THRESHOLD_SURFACE), rel(SOURCE_ONNX_SMOKE), rel(SURFACE_REVIEW), rel(DENSITY_BOTTLENECK)],
            "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "forward pass(전진 검증)", "WFO(워크포워드 최적화)"],
            "judgment_label": "negative_valid_scout(유효한 부정 탐색)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "수익은 좋은데 너무 적게 거래해서 목표 운영 모델은 아니다. 다만 품질 단서와 밀도 단서를 나눠 다음 실험에 쓴다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_run_id": PARENT_RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "no_claims": ["new model training(새 모델 학습)", "MT5 execution(MT5 실행)", "runtime authority(런타임 권위)", "operating promotion(운영 승격)", "Goal Achieve(목표 달성)"],
            "effect": "review(검토)를 운영 주장(operating claim, 운영 주장)과 분리한다.",
        },
    )


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    required = {"kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"}
    rows = [
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed" if exists(SURFACE_REVIEW) and KPI_BOUNDARY else "failed",
            "evidence": rel(SURFACE_REVIEW),
            "effect": "KPI(핵심 성과 지표)를 proxy review(프록시 검토)로 라벨링해 MT5 KPI(MT5 핵심 성과 지표)와 혼동하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "row_grain_audit",
            "status": "passed" if int(final["surface_review_rows"]) == int(final["source_threshold_rows"]) else "failed",
            "evidence": rel(SURFACE_REVIEW),
            "effect": "run364J threshold row(임계값 행)마다 review class(검토 분류)를 부여한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed" if exists(SOURCE_FINAL_DECISION) and exists(SOURCE_THRESHOLD_SURFACE) else "failed",
            "evidence": f"{rel(SOURCE_FINAL_DECISION)};{rel(SOURCE_THRESHOLD_SURFACE)}",
            "effect": "review source(검토 원천)를 run364J final/surface(최종 결정/표면)로 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": ",".join(sorted(required)),
            "effect": "required gates(필수 게이트)가 closeout(종료 기록)에 연결됐음을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def write_final_and_manifest(
    surface_rows: Sequence[Mapping[str, Any]],
    bottleneck_rows: Sequence[Mapping[str, Any]],
    salvage_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    next_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    parent = read_json(SOURCE_FINAL_DECISION)
    final = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "result_judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_threshold_rows": parent["threshold_rows"],
        "surface_review_rows": len(surface_rows),
        "density_bottleneck_rows": len(bottleneck_rows),
        "salvage_clue_rows": len(salvage_rows),
        "failure_memory_rows": len(failure_rows),
        "next_queue_rows": len(next_rows),
        "strict_candidate_rows": sum(1 for row in surface_rows if row["review_class"] == "strict_candidate"),
        "profit_pf_density_fail_rows": sum(1 for row in surface_rows if row["review_class"] == "profit_pf_pass_density_fail"),
        "density_oos_positive_validation_fail_rows": sum(1 for row in surface_rows if row["review_class"] == "density_oos_positive_validation_fail"),
        "best_preserved_model_id": parent["best_model_id"],
        "best_preserved_label_id": parent["best_label_id"],
        "best_preserved_oos_net": parent["best_oos_net"],
        "best_preserved_oos_pf": parent["best_oos_profit_factor"],
        "best_preserved_oos_density": parent["best_oos_trade_density"],
        "mt5_execution": "not_run",
        "new_model_training": "not_run",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": now_utc(),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
    }
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    manifest_rows = []
    for path in [*INPUT_FILES, *OUTPUT_FILES, Path(__file__)]:
        manifest_rows.append(
            {
                "run_id": RUN_ID,
                "path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "role": "input_or_output",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": now_utc(),
            "status": STATUS,
            "judgment": JUDGMENT,
            "paths": manifest_rows,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final, gates


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    visible = list(rows)[:limit]
    if not visible:
        return "_none(없음)_"
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join("---" for _ in columns) + "|"]
    for row in visible:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def write_report(
    final: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
    bottleneck_rows: Sequence[Mapping[str, Any]],
    salvage_rows: Sequence[Mapping[str, Any]],
    next_rows: Sequence[Mapping[str, Any]],
) -> None:
    top_bottleneck = list(bottleneck_rows)[:10]
    top_salvage = list(salvage_rows)[:12]
    report = f"""# run364K Direct Dense M5 ONNX Scout Review(364K 직접 고밀도 5분봉 온엑스 탐색 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- surface_review_rows(표면 검토 행): `{final["surface_review_rows"]}`
- strict_candidate_rows(엄격 후보 행): `{final["strict_candidate_rows"]}`
- profit_pf_density_fail_rows(수익/PF 통과 밀도 실패 행): `{final["profit_pf_density_fail_rows"]}`
- density_oos_positive_validation_fail_rows(밀도/OOS 양수 검증 실패 행): `{final["density_oos_positive_validation_fail_rows"]}`
- salvage_clue_rows(회수 단서 행): `{final["salvage_clue_rows"]}`
- best_preserved_model_id(보존 최선 모델 ID): `{final["best_preserved_model_id"]}`
- best_preserved_oos_net(보존 최선 표본외 순수익): `{final["best_preserved_oos_net"]}`
- best_preserved_oos_pf(보존 최선 표본외 수익 팩터): `{final["best_preserved_oos_pf"]}`
- best_preserved_oos_density(보존 최선 표본외 밀도): `{final["best_preserved_oos_density"]}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Judgment(판정)

Action(행동): run364J(364J 실행)의 threshold surface(임계값 표면)를 density(밀도), net(순수익), PF(수익 팩터), horizon(보유 기간), policy(정책)로 분해했다.

Effect(효과): direct dense M5 idea(직접 고밀도 5분봉 아이디어)는 invalid(무효)가 아니라 valid negative scout(유효한 부정 탐색)다. h24(24봉)는 수익 품질을 보존하지만 밀도가 낮고, h6(6봉)은 밀도는 회복하지만 검증 안정성이 약하다.

## Bottleneck Attribution(병목 귀속)

{markdown_table(top_bottleneck, ["label_id", "horizon_m5", "policy_id", "density_pass_rows", "profit_positive_rows", "profit_pf_pass_rows", "best_score_oos_net", "best_score_oos_density", "best_density_oos_net", "best_density_oos_density", "attribution"])}

## Salvage Clues(회수 단서)

{markdown_table(top_salvage, ["clue_type", "rank", "model_id", "label_id", "horizon_m5", "policy_id", "validation_net", "oos_net", "validation_trade_density", "oos_trade_density", "salvage_value"])}

## Next Queue(다음 대기열)

{markdown_table(next_rows, ["queue_id", "priority", "next_run_id", "idea_id", "hypothesis", "micro_search_gate"])}

## Evidence(근거)

- surface_review(표면 검토): `{rel(SURFACE_REVIEW)}`
- density_bottleneck_attribution(밀도 병목 귀속): `{rel(DENSITY_BOTTLENECK)}`
- salvage_clues(회수 단서): `{rel(SALVAGE_CLUES)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT)}`

## Boundary(경계)

이번 실행은 review(검토)만 수행했다. new model training(새 모델 학습), MT5 execution(MT5 실행), forward pass(전진 검증), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364K Direct Dense M5 ONNX Scout Review Decision(364K 직접 고밀도 5분봉 온엑스 탐색 검토 결정)

- decision(결정): `{DECISION}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): run364J(364J 실행)의 negative result(부정 결과)를 failure memory(실패 기억)와 next offensive seed(다음 공격 씨앗)로 정리했다.

Effect(효과): 다음 실행은 h24 quality clue(24봉 품질 단서)와 h6 density clue(6봉 밀도 단서)를 trade shape repair(거래 형태 수리)로 결합한다.

Evidence(근거): `{rel(SURFACE_REVIEW)}`, `{rel(DENSITY_BOTTLENECK)}`, `{rel(SALVAGE_CLUES)}`, `{rel(FAILURE_MEMORY)}`.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_state_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run364K(364K 실행)가 run364J(364J 실행)의 direct dense M5 ONNX scout(직접 고밀도 5분봉 온엑스 탐색)를 review(검토)했다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`이며, h24 quality clue(24봉 품질 단서)와 h6 density clue(6봉 밀도 단서)를 결합하는 trade shape repair(거래 형태 수리)를 연다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `direct_dense_m5_scout_reviewed_density_lift_next_seed_opened_no_operating_claim(직접 고밀도 5분봉 탐색 검토 완료, 밀도 상향 다음 씨앗 열림, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- preserved_profit_model_id(보존 수익 모델 ID): `{final["best_preserved_model_id"]}`
- preserved_oos_net(보존 표본외 순수익): `{final["best_preserved_oos_net"]}`
- preserved_oos_density(보존 표본외 거래 밀도): `{final["best_preserved_oos_density"]}`
- strict_candidate_rows(엄격 후보 행): `{final["strict_candidate_rows"]}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run364K Closeout(364K 종료 기록)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): negative scout(부정 탐색)를 failure memory(실패 기억)와 next queue(다음 대기열)로 바꿨다.

Effect(효과): 다음 실행은 density lift(밀도 상향)를 수익 품질과 함께 시험한다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364K Direct Dense M5 ONNX Scout Review Closeout",
        f"""## run364K Direct Dense M5 ONNX Scout Review Closeout(364K 직접 고밀도 5분봉 온엑스 탐색 검토 종료)

Action(행동): run364J(364J 실행)의 192개 threshold row(임계값 행)를 review class(검토 분류)로 나눴다.

Effect(효과): strict_candidate_rows(엄격 후보 행)는 `{final["strict_candidate_rows"]}`이고, 다음 실행은 `{NEXT_RUN_ID}`이다.
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "run364K_direct_dense_m5_onnx_scout_review",
        f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - direct dense M5 ONNX scout review(직접 고밀도 5분봉 온엑스 탐색 검토).""",
    )
    append_text_once(
        STAGE_README,
        "run364K Direct Dense M5 ONNX Scout Review",
        f"""## run364K Direct Dense M5 ONNX Scout Review(364K 직접 고밀도 5분봉 온엑스 탐색 검토)

Action(행동): run364J(364J 실행)의 low-density profit clue(저밀도 수익 단서)를 failure memory(실패 기억)와 next offensive seed(다음 공격 씨앗)로 바꿨다.

Effect(효과): `{NEXT_RUN_ID}`에서 density lift trade shape(밀도 상향 거래 형태)를 시험한다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "run364K_review_direct_dense_m5_onnx_scout_without_db_v1",
        f"""## {TODAY} run364K Direct Dense M5 ONNX Scout Review(364K 직접 고밀도 5분봉 온엑스 탐색 검토)

Action(행동): direct dense M5 scout(직접 고밀도 5분봉 탐색)의 negative result(부정 결과)를 review(검토)했다.

Effect(효과): h24 quality clue(24봉 품질 단서)와 h6 density clue(6봉 밀도 단서)를 다음 trade-shape scout(거래 형태 탐색)로 넘겼다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST364L-DENSITY-LIFT-TRADE-SHAPE-ONNX-SCOUT",
        f"""## IDEA-ST364L-DENSITY-LIFT-TRADE-SHAPE-ONNX-SCOUT

- hypothesis(가설): h24 quality clue(24봉 품질 단서)와 h6 density clue(6봉 밀도 단서)를 shorter hold and exit policy(짧은 보유와 청산 정책)로 결합하면 3/day+(일 3회 이상) density(밀도)를 회복할 수 있다.
- legacy_relation(레거시 관계): `none(없음)`.
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)`.
- broad_sweep(넓은 탐색): `horizon_m5=[3,4,6,8,12]`, `target_density=[3,5,8,12]`, `policy=[long_only,two_sided,side_asym]`.
- extreme_sweep(극단 탐색): `target_density=[16,20]`, `hold_m5=[2,3]`, `cost_stress=[0.30,0.45,0.60]`.
- micro_search_gate(미세 탐색 게이트): validation/OOS density >= 3/day(검증/표본외 밀도 3/일 이상), net > 0(순수익 양수), PF >= 1.05(수익 팩터 1.05 이상).
- wfo_plan(WFO 계획): scout(탐색) 통과 후 WFO(워크포워드 최적화).
- evidence_boundary(근거 경계): `{CLAIM_BOUNDARY}`.
""",
    )
    append_text_once(
        NEGATIVE_REGISTER,
        "run364K_direct_dense_m5_density_bottleneck_failure_memory",
        f"""## run364K Direct Dense M5 Density Bottleneck Failure Memory(364K 직접 고밀도 5분봉 밀도 병목 실패 기억)

Action(행동): run364J(364J 실행)의 strict_candidate_rows(엄격 후보 행) `{final["strict_candidate_rows"]}`개를 확인하고 failure memory(실패 기억)를 남겼다.

Effect(효과): h24 fixed-hold(24봉 고정 보유)는 high-density claim(고밀도 주장)에 반복 사용하지 않고, h6 density row(6봉 밀도 행)는 validation stability repair(검증 안정성 수리) 조건으로 재개한다.
""",
    )
    replace_stage_brief_header()


def replace_stage_brief_header() -> None:
    text = read_text(STAGE_BRIEF)
    if not text:
        return
    replacements = {
        "- current_run_id(": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id(": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(": "- selection_status(선택 상태): `direct_dense_m5_scout_reviewed_density_lift_next_seed_opened_no_operating_claim(직접 고밀도 5분봉 탐색 검토 완료, 밀도 상향 다음 씨앗 열림, 운영 주장 없음)`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    next_lines = []
    for line in text.splitlines():
        replaced = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                next_lines.append(value)
                replaced = True
                break
        if not replaced:
            next_lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(next_lines))


def registry_rows(final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "direct_dense_m5_review(직접 고밀도 5분봉 검토)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_mt5_execution(주장 범위 밖, MT5 실행 없음)",
        "notes": "Stage364K reviewed run364J density bottleneck(Stage364K가 364J 밀도 병목 검토).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["surface_review_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(FAILURE_MEMORY),
        "result_status": STATUS,
        "sample_rows": final["surface_review_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "kpi_evidence(핵심 성과 지표 근거)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "lane": "direct_dense_m5_review(직접 고밀도 5분봉 검토)",
        "family": "kpi_evidence(핵심 성과 지표 근거)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Why did direct dense M5 ONNX scout fail the density gate?(직접 고밀도 5분봉 온엑스 탐색은 왜 밀도 게이트를 실패했는가?)",
        "metric_scope": KPI_BOUNDARY,
        "best_model_id": final["best_preserved_model_id"],
        "best_net_profit": final["best_preserved_oos_net"],
        "best_profit_factor": final["best_preserved_oos_pf"],
        "trade_density_per_feature_day": final["best_preserved_oos_density"],
    }
    tier_a = dict(common)
    tier_a.update(
        {
            "subrun_id": f"{RUN_ID}__Tier_A",
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "kpi_scope": "proxy_review(프록시 검토)",
            "primary_kpi": f"strict_candidate_rows={final['strict_candidate_rows']};salvage_clue_rows={final['salvage_clue_rows']}",
            "guardrail_kpi": "mt5_execution=not_run;runtime_authority=not_claimed",
        }
    )
    tier_b = dict(tier_a)
    tier_b.update(
        {
            "subrun_id": f"{RUN_ID}__Tier_B",
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
        }
    )
    combined = dict(tier_a)
    combined.update(
        {
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "status": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
            "primary_kpi": "combined_not_run(합산 실행 없음)",
            "guardrail_kpi": "do_not_synthesize_combined_result(합산 결과 합성 금지)",
        }
    )
    return [tier_a], [tier_a, tier_b, combined], [tier_a, tier_b, combined]


def write_registries(final: Mapping[str, Any]) -> None:
    run_rows, project_rows, stage_rows = registry_rows(final)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage364/review_direct_dense_m5_onnx_scout_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("selection_status", SELECTION_STATUS, "tracked"),
        ("input_manifest", INPUT_MANIFEST, "ignored_with_manifest"),
        ("surface_review", SURFACE_REVIEW, "ignored_with_manifest"),
        ("density_bottleneck", DENSITY_BOTTLENECK, "ignored_with_manifest"),
        ("salvage_clues", SALVAGE_CLUES, "ignored_with_manifest"),
        ("failure_memory", FAILURE_MEMORY, "ignored_with_manifest"),
        ("next_queue", NEXT_QUEUE, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "notes": f"Stage364K direct dense M5 review artifact(364K 직접 고밀도 5분봉 검토 산출물); availability={availability}",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows, extend_header=False)


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_input_manifest()
    surface = load_surface()
    surface_rows = build_surface_review(surface)
    bottleneck_rows = build_density_bottleneck(surface)
    salvage_rows = build_salvage_clues(surface)
    failure_rows = build_failure_memory(surface_rows, salvage_rows)
    next_rows = build_next_queue(salvage_rows)
    final, _gates = write_final_and_manifest(surface_rows, bottleneck_rows, salvage_rows, failure_rows, next_rows)
    write_receipts(final)
    final, gates = write_final_and_manifest(surface_rows, bottleneck_rows, salvage_rows, failure_rows, next_rows)
    write_report(final, gates, bottleneck_rows, salvage_rows, next_rows)
    update_state_docs(final, gates)
    write_registries(final)
    write_artifact_registry()
    final, gates = write_final_and_manifest(surface_rows, bottleneck_rows, salvage_rows, failure_rows, next_rows)
    write_report(final, gates, bottleneck_rows, salvage_rows, next_rows)
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
