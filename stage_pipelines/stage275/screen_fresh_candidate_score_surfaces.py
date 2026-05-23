from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure"
RUN_ID = "run275E_screen_fresh_candidate_score_surfaces_v1"
SOURCE_RUN_ID = "run275D_execute_fresh_candidate_scoring_materialization_probe_v1"
STATUS = "completed_fresh_candidate_score_surface_screen_probe_queue_no_candidate_selection"
JUDGMENT = "screened_stage276_probe_seeds_and_failure_memory_no_candidate_selection"
JUDGMENT_CLASS = "inconclusive_probe_seed"
NEXT_ACTION = "run275F_close_stage275_open_stage276_aggressive_fresh_surface_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN275D = STAGE / "02_runs" / "run275D"
RUN_DIR = STAGE / "02_runs" / "run275E"
SCORE_DIR = RUN275D / "s"
HANDOFF_DIR = RUN275D / "h"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_MANIFEST = RUN275D / "run_manifest.json"
SOURCE_SUMMARY = RUN275D / "summary.csv"
SOURCE_SPLIT = RUN275D / "split.csv"
SOURCE_TIER = RUN275D / "tier.csv"
SOURCE_NORMALIZATION = RUN275D / "norm.json"
SOURCE_DATA = RUN275D / "data.json"
SOURCE_MODEL = RUN275D / "model.json"
SOURCE_LINEAGE = RUN275D / "lineage.json"
SOURCE_REPORT = REVIEWS / "run275D_report.md"

SCREENING = RUN_DIR / "screen.csv"
STAGE276_QUEUE = RUN_DIR / "stage276_queue.csv"
FAILURE_MEMORY = RUN_DIR / "failure.csv"
SUPPORT_CONTROL_CARRY = RUN_DIR / "support.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model.json"
RESULT_JUDGMENT = RUN_DIR / "judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage.json"
RUN_REPORT = REVIEWS / "run275E_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage275/screen_fresh_candidate_score_surfaces.py")

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
SCREEN_COLUMNS = (
    "package_id",
    "package_role",
    "fresh_thesis",
    "rows",
    "active_signal_count",
    "active_signal_rate",
    "long_count",
    "short_count",
    "long_share",
    "changed_signal_count",
    "changed_signal_rate",
    "new_active_count",
    "new_active_rate",
    "removed_active_count",
    "direction_changed_count",
    "direction_changed_rate",
    "tier_a_active_rate",
    "tier_b_active_rate",
    "tier_ab_active_rate_delta",
    "train_active_rate",
    "validation_active_rate",
    "oos_active_rate",
    "split_active_rate_spread",
    "mean_risk_delta_vs_control",
    "structural_screen_score",
    "screening_judgment",
    "screening_reason",
    "next_action",
    "reopen_condition",
    "do_not_repeat_note",
    "selected_candidate",
    "onnx_readiness",
    "performance_claim",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "queue_priority",
    "package_id",
    "source_run",
    "queue_role",
    "fresh_thesis",
    "source_score_table",
    "source_handoff_json",
    "support_control",
    "upside_question",
    "failure_mode_to_watch",
    "discard_condition",
    "required_evidence",
    "claim_boundary",
)
FAILURE_COLUMNS = (
    "failure_id",
    "package_id",
    "failed_boundary",
    "why_failed_or_not_ready",
    "salvage_value",
    "reopen_condition",
    "do_not_repeat_note",
    "evidence_path",
    "claim_boundary",
)
SUPPORT_COLUMNS = (
    "package_id",
    "support_role",
    "screening_judgment",
    "carry_condition",
    "source_score_table",
    "source_handoff_json",
    "claim_boundary",
)

PACKAGE_META = {
    "cp275A_volatility_pullback_breakout_surface": {
        "short": "cp275A",
        "role": "selectable_fresh_candidate_seed",
        "fresh_thesis": "volatility_pullback_breakout(변동성 되돌림 돌파)",
    },
    "cp275B_cross_asset_divergence_reversal_surface": {
        "short": "cp275B",
        "role": "selectable_fresh_candidate_seed",
        "fresh_thesis": "cross_asset_divergence_reversal(교차자산 괴리 반전)",
    },
    "cp275C_cash_session_impulse_continuation_surface": {
        "short": "cp275C",
        "role": "selectable_fresh_candidate_seed",
        "fresh_thesis": "cash_session_impulse_continuation(현금장 충격 지속)",
    },
    "cp275D_macro_volatility_squeeze_release_surface": {
        "short": "cp275D",
        "role": "selectable_fresh_candidate_seed",
        "fresh_thesis": "macro_volatility_squeeze_release(거시 변동성 압축 해제)",
    },
    "cp275E_q04_stage274_failure_signature_guard": {
        "short": "cp275E",
        "role": "support_control_only",
        "fresh_thesis": "q04_failure_signature_guard(q04 실패 서명 방어)",
    },
}
SUPPORT_CONTROL = "cp275E_q04_stage274_failure_signature_guard"


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def score_path(package_id: str) -> Path:
    return SCORE_DIR / f"{PACKAGE_META[package_id]['short']}.parquet"


def handoff_path(package_id: str) -> Path:
    return HANDOFF_DIR / f"{PACKAGE_META[package_id]['short']}.json"


def load_scores(package_id: str) -> pd.DataFrame:
    columns = ["timestamp", "split", "tier_view", "entry_signal", "model_risk_pct", "candidate_decision_score"]
    return pd.read_parquet(io_path(score_path(package_id)), columns=columns)


def rate(mask: pd.Series) -> float:
    return float(mask.mean()) if len(mask) else 0.0


def rounded(value: float, digits: int = 8) -> float:
    return round(float(value), digits) if np.isfinite(value) else 0.0


def split_rate(frame: pd.DataFrame, split: str) -> float:
    part = frame[frame["split"].astype(str).eq(split)]
    return rate(part["entry_signal"].astype(str).ne("flat")) if len(part) else 0.0


def tier_rate(frame: pd.DataFrame, tier_view: str) -> float:
    part = frame[frame["tier_view"].astype(str).eq(tier_view)]
    return rate(part["entry_signal"].astype(str).ne("flat")) if len(part) else 0.0


def classify(row: Mapping[str, Any]) -> tuple[str, str, str, str, str]:
    package_id = str(row["package_id"])
    if package_id == SUPPORT_CONTROL:
        return (
            "support_control_carry(보조 대조 유지)",
            "q04 failure signature guard(q04 실패 서명 방어)는 후보가 아니라 비교 기준이다.",
            "carry_as_stage276_support_control(Stage276 보조 대조로 유지)",
            "do_not_promote_support_control(보조 대조 직접 승격 금지)",
            "support control(보조 대조)을 candidate(후보)로 부르지 않는다.",
        )

    fresh = float(row["changed_signal_rate"]) >= 0.20 and (
        float(row["new_active_rate"]) >= 0.04 or float(row["direction_changed_rate"]) >= 0.01
    )
    bounded_supply = 0.08 <= float(row["validation_active_rate"]) <= 0.50 and 0.08 <= float(row["oos_active_rate"]) <= 0.50
    tier_ok = float(row["tier_ab_active_rate_delta"]) <= 0.12
    split_ok = float(row["split_active_rate_spread"]) <= 0.15
    route_ok = 0.25 <= float(row["long_share"]) <= 0.75

    if fresh and bounded_supply and tier_ok and split_ok and route_ok:
        return (
            "stage276_aggressive_probe_seed(276단계 공격형 탐침 씨앗)",
            "q04 guard(q04 방어 기준) 대비 new active signal(새 활성 신호) 또는 direction change(방향 변경)가 있고 공급/티어/경로가 선별 범위 안에 있다.",
            "queue_for_stage276_aggressive_fresh_surface_probe(Stage276 공격형 새 표면 탐침 대기열)",
            "MT5 probe(MT5 탐침)와 stability review(안정성 검토)에서 curve/trade quality(곡선/거래 품질)가 무너지면 폐기한다.",
            "probe seed(탐침 씨앗)를 selected candidate(선택 후보)로 부르지 않는다.",
        )
    if not fresh:
        return (
            "failure_memory_near_duplicate_or_filter_only(실패 기억: 중복 또는 필터형)",
            "q04 guard(q04 방어 기준) 대비 fresh decision surface(새 판단 표면)가 부족하다.",
            "record_failure_memory(실패 기억 기록)",
            "new_active_rate(새 활성률) 또는 direction_changed_rate(방향 변경률)가 실질적으로 생길 때만 재개한다.",
            "같은 q04 removal(q04 제거) 수리 루프를 반복하지 않는다.",
        )
    if not route_ok:
        return (
            "failure_memory_route_bias(실패 기억: 경로 편향)",
            "long/short route mix(매수/매도 경로 혼합)가 한쪽으로 과도하게 기울었다.",
            "record_failure_memory(실패 기억 기록)",
            "route mix(경로 혼합)가 25~75 percent(25~75퍼센트) 안에 들어올 때 재개한다.",
            "방향 편향을 edge(거래 우위)로 착각하지 않는다.",
        )
    if not bounded_supply:
        return (
            "failure_memory_supply_shape_unbounded(실패 기억: 공급 모양 불량)",
            "validation/oos active rate(검증/표본외 활성률)가 탐침 가능한 공급 범위를 벗어났다.",
            "record_failure_memory(실패 기억 기록)",
            "validation/oos active rate(검증/표본외 활성률)가 8~50 percent(8~50퍼센트) 범위로 돌아올 때 재개한다.",
            "공급량 자체를 edge(거래 우위)로 보지 않는다.",
        )
    if not tier_ok:
        return (
            "failure_memory_partial_context_collapse(실패 기억: 부분 문맥 붕괴)",
            "Tier A/B active rate(티어 A/B 활성률) 차이가 커서 partial-context fallback(부분 문맥 대체) 안정성이 약하다.",
            "record_failure_memory(실패 기억 기록)",
            "Tier B adapter(티어 B 어댑터)를 명시하거나 티어 차이를 낮출 때 재개한다.",
            "full-context only(전체 문맥 전용) 표면을 후보로 과장하지 않는다.",
        )
    return (
        "failure_memory_split_instability(실패 기억: 분할 불안정)",
        "train/validation/oos active rate(학습/검증/표본외 활성률) 차이가 커서 구조 안정성이 약하다.",
        "record_failure_memory(실패 기억 기록)",
        "split spread(분할 격차)가 15 percent(15퍼센트) 이하로 줄 때 재개한다.",
        "한 분할 공급만으로 후보를 부르지 않는다.",
    )


def build_screening_rows() -> list[dict[str, Any]]:
    control = load_scores(SUPPORT_CONTROL).rename(
        columns={
            "entry_signal": "control_entry_signal",
            "model_risk_pct": "control_model_risk_pct",
            "candidate_decision_score": "control_decision_score",
        }
    )
    rows: list[dict[str, Any]] = []
    for package_id, meta in PACKAGE_META.items():
        frame = load_scores(package_id)
        merged = frame.merge(
            control[["timestamp", "split", "tier_view", "control_entry_signal", "control_model_risk_pct"]],
            on=["timestamp", "split", "tier_view"],
            how="inner",
        )
        active = merged["entry_signal"].astype(str).ne("flat")
        control_active = merged["control_entry_signal"].astype(str).ne("flat")
        changed = merged["entry_signal"].astype(str).ne(merged["control_entry_signal"].astype(str))
        new_active = active & ~control_active
        removed_active = ~active & control_active
        direction_changed = active & control_active & changed
        long_count = int(merged["entry_signal"].astype(str).eq("long").sum())
        short_count = int(merged["entry_signal"].astype(str).eq("short").sum())
        active_count = int(active.sum())
        train = split_rate(merged, "train")
        validation = split_rate(merged, "validation")
        oos = split_rate(merged, "oos")
        tier_a = tier_rate(merged, "Tier A separate")
        tier_b = tier_rate(merged, "Tier B separate")
        long_share = long_count / active_count if active_count else 0.0
        changed_rate = rate(changed)
        new_active_rate = rate(new_active)
        direction_changed_rate = rate(direction_changed)
        split_spread = max(train, validation, oos) - min(train, validation, oos)
        tier_delta = abs(tier_a - tier_b)
        route_penalty = abs(long_share - 0.50) * 20.0 if active_count else 10.0
        structural_score = (
            changed_rate * 35.0
            + new_active_rate * 45.0
            + direction_changed_rate * 35.0
            + max(0.0, 0.50 - split_spread) * 8.0
            + max(0.0, 0.12 - tier_delta) * 10.0
            - route_penalty
        )
        row: dict[str, Any] = {
            "package_id": package_id,
            "package_role": meta["role"],
            "fresh_thesis": meta["fresh_thesis"],
            "rows": int(len(merged)),
            "active_signal_count": active_count,
            "active_signal_rate": rounded(rate(active)),
            "long_count": long_count,
            "short_count": short_count,
            "long_share": rounded(long_share),
            "changed_signal_count": int(changed.sum()),
            "changed_signal_rate": rounded(changed_rate),
            "new_active_count": int(new_active.sum()),
            "new_active_rate": rounded(new_active_rate),
            "removed_active_count": int(removed_active.sum()),
            "direction_changed_count": int(direction_changed.sum()),
            "direction_changed_rate": rounded(direction_changed_rate),
            "tier_a_active_rate": rounded(tier_a),
            "tier_b_active_rate": rounded(tier_b),
            "tier_ab_active_rate_delta": rounded(tier_delta),
            "train_active_rate": rounded(train),
            "validation_active_rate": rounded(validation),
            "oos_active_rate": rounded(oos),
            "split_active_rate_spread": rounded(split_spread),
            "mean_risk_delta_vs_control": rounded(
                float((merged["model_risk_pct"] - merged["control_model_risk_pct"]).mean())
            ),
            "structural_screen_score": rounded(structural_score, 6),
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "performance_claim": "none",
            "claim_boundary": BOUNDARY,
        }
        judgment, reason, next_action, reopen, do_not_repeat = classify(row)
        row.update(
            {
                "screening_judgment": judgment,
                "screening_reason": reason,
                "next_action": next_action,
                "reopen_condition": reopen,
                "do_not_repeat_note": do_not_repeat,
            }
        )
        rows.append(row)
    return rows


def build_queue_rows(screening_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    seeds = [
        row for row in screening_rows if str(row["screening_judgment"]).startswith("stage276_aggressive_probe_seed")
    ]
    seeds = sorted(seeds, key=lambda row: float(row["structural_screen_score"]), reverse=True)
    queue: list[dict[str, Any]] = []
    for index, row in enumerate(seeds, start=1):
        package_id = str(row["package_id"])
        queue.append(
            {
                "queue_id": f"stage276_seed_{PACKAGE_META[package_id]['short']}",
                "queue_priority": index,
                "package_id": package_id,
                "source_run": RUN_ID,
                "queue_role": "aggressive_fresh_surface_probe_seed(공격형 새 표면 탐침 씨앗)",
                "fresh_thesis": row["fresh_thesis"],
                "source_score_table": rel(score_path(package_id)),
                "source_handoff_json": rel(handoff_path(package_id)),
                "support_control": SUPPORT_CONTROL,
                "upside_question": (
                    "Can this fresh decision surface(새 판단 표면)가 q04 guard(q04 방어 기준)와 다른 active/direction supply(활성/방향 공급)를 "
                    "MT5 probe(MT5 탐침)에서 보상 비대칭으로 바꿀 수 있는가?"
                ),
                "failure_mode_to_watch": (
                    "curve damage(곡선 손상), trade quality collapse(거래 품질 붕괴), weak month/session concentration(약한 월/세션 집중), "
                    "Tier B partial-context drift(티어 B 부분 문맥 표류)."
                ),
                "discard_condition": (
                    "MT5 runtime probe(MT5 런타임 탐침) 또는 stability review(안정성 검토)에서 PF/DD/recovery/expectancy"
                    "(수익 팩터/손실폭/회복/기대값)가 함께 무너지면 폐기한다."
                ),
                "required_evidence": "score_table;handoff_json;screening_receipt;future_mt5_probe;future_curve_trade_quality_review",
                "claim_boundary": BOUNDARY,
            }
        )
    return queue


def build_failure_rows(screening_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in screening_rows:
        judgment = str(row["screening_judgment"])
        package_id = str(row["package_id"])
        if package_id == SUPPORT_CONTROL or judgment.startswith("stage276_aggressive_probe_seed"):
            continue
        rows.append(
            {
                "failure_id": f"NEG-ST275-RUN275E-{PACKAGE_META[package_id]['short']}",
                "package_id": package_id,
                "failed_boundary": judgment,
                "why_failed_or_not_ready": row["screening_reason"],
                "salvage_value": "rebuild_decision_surface_or_route_balance(판단 표면 또는 경로 균형 재구성)",
                "reopen_condition": row["reopen_condition"],
                "do_not_repeat_note": row["do_not_repeat_note"],
                "evidence_path": rel(SCREENING),
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_support_rows(screening_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "support_role": "stage276_q04_failure_signature_guard(276단계 q04 실패 서명 방어)",
            "screening_judgment": row["screening_judgment"],
            "carry_condition": row["next_action"],
            "source_score_table": rel(score_path(str(row["package_id"]))),
            "source_handoff_json": rel(handoff_path(str(row["package_id"]))),
            "claim_boundary": BOUNDARY,
        }
        for row in screening_rows
        if row["package_id"] == SUPPORT_CONTROL
    ]


def write_receipts(
    screening_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    support_rows: Sequence[Mapping[str, Any]],
) -> None:
    write_csv(SCREENING, SCREEN_COLUMNS, screening_rows)
    write_csv(STAGE276_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(SUPPORT_CONTROL_CARRY, SUPPORT_COLUMNS, support_rows)
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "hypothesis": (
                "run275D score surfaces(275D 점수 표면) 중 일부는 q04 guard(q04 방어 기준)와 다른 fresh signal(새 신호)을 만들며, "
                "Stage276 aggressive probe(276단계 공격형 탐침)에 보낼 가치가 있을 수 있다."
            ),
            "decision_use": "candidate selection(후보 선택)이 아니라 Stage276 probe queue(276단계 탐침 대기열)와 failure memory(실패 기억)를 만든다.",
            "comparison_baseline": "cp275E q04_stage274_failure_signature_guard(q04 Stage274 실패 서명 방어)",
            "control_variables": "run275D score table hashes(점수표 해시), handoff identity(인계 정체성), Tier A/B paired scope(티어 A/B 쌍 범위)",
            "changed_variables": "freshness metrics(새로움 지표), route balance(경로 균형), split supply spread(분할 공급 격차), Tier A/B active delta(티어 A/B 활성 차이)",
            "success_criteria": "at least one probe seed(탐침 씨앗 1개 이상) with fresh active/direction supply(새 활성/방향 공급)",
            "failure_criteria": "all selectable packages(모든 선택 가능 패키지)가 duplicate/filter/route-bias(중복/필터/경로 편향)로 끝난다.",
            "invalid_conditions": "screen result(선별 결과)를 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)로 주장한다.",
            "stop_conditions": "Stage276(276단계)에서 MT5/curve/trade-quality(MT5/곡선/거래 품질) 압박을 통과하지 못하면 폐기한다.",
            "screened_packages": len(screening_rows),
            "queue_rows": len(queue_rows),
            "failure_rows": len(failure_rows),
            "support_rows": len(support_rows),
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "data_source": [rel(SOURCE_MANIFEST), rel(SOURCE_SUMMARY), rel(SOURCE_SPLIT), rel(SOURCE_TIER), rel(SCORE_DIR)],
            "time_axis": "run275E(275E 실행)는 새 bar(봉)를 만들지 않고 timestamp/split/tier_view(시각/분할/티어 보기)를 그대로 비교한다.",
            "sample_scope": "Tier A separate, Tier B separate, Tier A+B combined(티어 A 분리, 티어 B 분리, 티어 A+B 합산) score tables(점수표)",
            "missing_or_duplicate_check": "each package(각 패키지)는 support control(보조 대조)과 timestamp/split/tier_view(시각/분할/티어 보기)로 inner join(내부 결합)했다.",
            "feature_label_boundary": "label/profit columns(라벨/수익 열)을 읽지 않고 signal structure(신호 구조)만 비교했다.",
            "split_boundary": "train/validation/oos(학습/검증/표본외) active supply(활성 공급)를 기록하지만 성과 지표로 쓰지 않는다.",
            "leakage_risk": "screening rule(선별 규칙)은 구조 선별이며 trading KPI(거래 핵심 성과 지표)나 후보 선택으로 쓰지 않는다.",
            "source_hashes": source_hashes(source_inputs()),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "model_family": "deterministic score surface screen(결정론 점수 표면 선별), no trained model(학습 모델 없음)",
            "target_and_label": "no model target(모델 목표 없음), no trading label read(거래 라벨 읽지 않음)",
            "selection_metric": "freshness and structure screen(새로움/구조 선별), not selected candidate(선택 후보 아님)",
            "secondary_metrics": "route balance(경로 균형), split supply spread(분할 공급 격차), Tier A/B delta(티어 A/B 차이)",
            "threshold_policy": "fixed screening thresholds(고정 선별 임계값)",
            "overfit_risk": "q04 failure memory(q04 실패 기억)에 맞춘 구조일 수 있어 Stage276 MT5 pressure(276단계 MT5 압박)가 필요하다.",
            "calibration_risk": "score(점수)는 probability(확률)가 아니며 screen rank(선별 순위)일 뿐이다.",
            "allowed_claims": ["probe_seed_queue(탐침 씨앗 대기열)", "failure_memory(실패 기억)"],
            "forbidden_claims": ["selected_candidate(선택 후보)", "ONNX readiness(ONNX 준비)", "Goal Achieve(목표 달성)"],
            "validation_judgment": JUDGMENT,
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows(queue_rows, failure_rows))
    write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows(queue_rows, failure_rows))


def result_rows(queue_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "screen(선별), stage276_queue(276단계 대기열), failure_memory(실패 기억), support_control(보조 대조), receipts(영수증)",
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), Adapter package(어댑터 패키지), ONNX export/parity(ONNX 내보내기/동등성)",
            "judgment_label": JUDGMENT,
            "judgment_class": JUDGMENT_CLASS,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": f"probe seed(탐침 씨앗) {len(queue_rows)}개와 failure memory(실패 기억) {len(failure_rows)}개를 만들었지만 후보 선택은 아니다.",
        }
    ]


def gate_rows(queue_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    queue_status = "passed(통과)" if queue_rows else "failed_no_probe_seed(탐침 씨앗 없음)"
    return [
        {
            "gate_name": "source_artifact_gate(원천 산출물 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(SOURCE_MANIFEST),
            "effect": "run275D 점수표와 인계 JSON을 원천으로 고정한다.",
        },
        {
            "gate_name": "freshness_screen_gate(새로움 선별 게이트)",
            "status": queue_status,
            "evidence_path": rel(SCREENING),
            "effect": "q04 guard(q04 방어 기준)와 다른 active/direction signal(활성/방향 신호)이 있는지 기록한다.",
        },
        {
            "gate_name": "failure_memory_gate(실패 기억 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(FAILURE_MEMORY),
            "effect": f"discard/reopen boundary(폐기/재개 경계)를 {len(failure_rows)}개 남긴다.",
        },
        {
            "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed(통과)",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "실험 설계, 데이터 무결성, 모델 경계, 결과 판정을 산출물과 연결한다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def source_inputs() -> list[Path]:
    score_paths = [score_path(package_id) for package_id in PACKAGE_META]
    handoff_paths = [handoff_path(package_id) for package_id in PACKAGE_META]
    return [
        SOURCE_MANIFEST,
        SOURCE_SUMMARY,
        SOURCE_SPLIT,
        SOURCE_TIER,
        SOURCE_NORMALIZATION,
        SOURCE_DATA,
        SOURCE_MODEL,
        SOURCE_LINEAGE,
        SOURCE_REPORT,
        *score_paths,
        *handoff_paths,
    ]


def source_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def write_report(
    screening_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    support_rows: Sequence[Mapping[str, Any]],
) -> None:
    screen_lines = "\n".join(
        (
            f"- `{row['package_id']}`: judgment(판정) `{row['screening_judgment']}`, "
            f"changed_rate(변경률) `{row['changed_signal_rate']}`, new_active(새 활성) `{row['new_active_count']}`, "
            f"direction_changed(방향 변경) `{row['direction_changed_count']}`, score(점수) `{row['structural_screen_score']}`"
        )
        for row in screening_rows
    )
    queue_line = ", ".join(str(row["package_id"]) for row in queue_rows) if queue_rows else "none(없음)"
    failure_line = ", ".join(str(row["package_id"]) for row in failure_rows) if failure_rows else "none(없음)"
    write_md(
        RUN_REPORT,
        f"""# run275E Fresh Candidate Score Surface Screen(275E 새 후보 점수 표면 선별)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- judgment_class(판정 분류): `{JUDGMENT_CLASS}`
- screened_packages(선별 패키지): `{len(screening_rows)}`
- stage276_queue_rows(276단계 대기열 행): `{len(queue_rows)}`
- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`
- support_control_rows(보조 대조 행): `{len(support_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run275E(275E 실행)는 run275D(275D 실행)의 score table(점수표)을 q04 guard(q04 방어 기준)와 비교했다.
효과(effect, 효과): Stage276 aggressive probe seed(276단계 공격형 탐침 씨앗) `{len(queue_rows)}`개, failure memory(실패 기억) `{len(failure_rows)}`개, support control(보조 대조) `{len(support_rows)}`개를 분리했고 선택 후보는 아직 없다.

## Screening Decisions(선별 결정)

{screen_lines}

## Queue And Failure(대기열과 실패)

- stage276_queue(276단계 대기열): `{queue_line}`
- failure_memory(실패 기억): `{failure_line}`

## Evidence Paths(근거 경로)

- screen(선별): `{rel(SCREENING)}`
- stage276_queue(276단계 대기열): `{rel(STAGE276_QUEUE)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- support_control(보조 대조): `{rel(SUPPORT_CONTROL_CARRY)}`
- lineage(계보): `{rel(LINEAGE_RECEIPT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


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


def replace_or_append(text: str, prefix: str, replacement: str) -> str:
    if any(line.startswith(prefix) for line in text.splitlines()):
        return replace_line_prefix(text, prefix, replacement)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_stage_docs(queue_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_or_append(selection, "- run275E_report", f"- run275E_report(275E 보고서): `{rel(RUN_REPORT)}`")
    selection = replace_or_append(selection, "- run275E_stage276_queue", f"- run275E_stage276_queue(275E 276단계 대기열): `{rel(STAGE276_QUEUE)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = replace_or_append(review, "- run275E_report", f"- run275E_report(275E 보고서): `{rel(RUN_REPORT)}`")
    review = replace_or_append(review, "- run275E_screen", f"- run275E_screen(275E 선별): `{rel(SCREENING)}`")
    review = replace_or_append(review, "- run275E_stage276_queue", f"- run275E_stage276_queue(275E 276단계 대기열): `{rel(STAGE276_QUEUE)}`")
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_candidate_score_surface_screen`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run275E_summary",
        (
            f"- run275E_summary(275E 요약): run275E(275E 실행)는 Stage276 aggressive probe seed(276단계 공격형 탐침 씨앗) "
            f"`{len(queue_rows)}`개와 failure memory(실패 기억) `{len(failure_rows)}`개를 만들었다. Effect(효과): 다음 작업은 "
            "Stage275(275단계)를 닫고 Stage276(276단계)에서 MT5 pressure probe(MT5 압박 탐침)를 설계하는 것이며, "
            "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage275(275단계) run275E(275E 실행) fresh candidate score surface screen(새 후보 점수 표면 선별) `{RUN_ID}`. "
        f"Effect(효과): Stage276 probe seed(276단계 탐침 씨앗) `{len(queue_rows)}`개와 failure memory(실패 기억) `{len(failure_rows)}`개를 만들고, "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run275E fresh candidate score surface screen(275E 새 후보 점수 표면 선별)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): Stage276 probe seed(276단계 탐침 씨앗) `{len(queue_rows)}`개와 failure memory(실패 기억) `{len(failure_rows)}`개를 만들었다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        RUN_ID,
        (
            f"## 2026-05-23 {RUN_ID}\n\n"
            f"- idea(아이디어): Stage276 aggressive fresh surface probe(276단계 공격형 새 표면 탐침) seeds(씨앗) `{len(queue_rows)}`개.\n"
            f"- evidence(근거): `{rel(STAGE276_QUEUE)}`\n"
            "- boundary(경계): probe seed(탐침 씨앗)이며 selected candidate(선택 후보)가 아니다.\n"
        ),
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        RUN_ID,
        (
            f"## 2026-05-23 {RUN_ID}\n\n"
            f"- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`\n"
            f"- evidence(근거): `{rel(FAILURE_MEMORY)}`\n"
            "- effect(효과): route bias(경로 편향)나 filter-like(필터형) 반복을 다음 candidate construction(후보 구성)에서 금지한다.\n"
        ),
    )
    write_md(NEGATIVE_REGISTER, negative)


def update_registers(
    created_at: str,
    screening_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    artifacts: Sequence[Path],
) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "result_judgment",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"screened={len(screening_rows)};queue={len(queue_rows)};failure={len(failure_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__{row['package_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": row["package_id"],
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "fresh candidate score surface screen(새 후보 점수 표면 선별)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
            "kpi_scope": "screening_only_no_trading_kpi",
            "scoreboard_lane": "fresh_candidate_surface_screen",
            "status": STATUS,
            "judgment": row["screening_judgment"],
            "path": rel(SCREENING),
            "primary_kpi": f"changed_signal_rate={row['changed_signal_rate']};new_active_count={row['new_active_count']};structural_screen_score={row['structural_screen_score']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_score_screen_only",
            "notes": row["screening_reason"],
        }
        for row in screening_rows
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__screen",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_candidate_score_surface_screen",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "screening_probe_seed_and_failure_memory",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "screening_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"queue={len(queue_rows)};failure={len(failure_rows)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run275E_score_surface_screen_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run275E fresh candidate score surface screen artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def manifest_payload(created_at: str, artifacts: Sequence[Path], inputs: Sequence[Path], screening_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "judgment_class": JUDGMENT_CLASS,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in inputs],
        "input_hashes": {rel(path): sha256_file_lf_normalized(path) for path in inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "screened_packages": len(screening_rows),
        "stage276_queue_rows": len(queue_rows),
        "failure_memory_rows": len(failure_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_score_screen_only",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTER), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def run() -> dict[str, Any]:
    inputs = source_inputs()
    must_exist(inputs)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()

    screening_rows = build_screening_rows()
    queue_rows = build_queue_rows(screening_rows)
    failure_rows = build_failure_rows(screening_rows)
    support_rows = build_support_rows(screening_rows)
    write_receipts(screening_rows, queue_rows, failure_rows, support_rows)
    write_report(screening_rows, queue_rows, failure_rows, support_rows)

    artifacts = [
        SCREENING,
        STAGE276_QUEUE,
        FAILURE_MEMORY,
        SUPPORT_CONTROL_CARRY,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    manifest = manifest_payload(created_at, artifacts, inputs, screening_rows, queue_rows, failure_rows)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, artifacts, inputs, screening_rows, queue_rows, failure_rows)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    artifacts.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, artifacts, inputs, screening_rows, queue_rows, failure_rows)
    write_json(RUN_MANIFEST, manifest)

    update_stage_docs(queue_rows, failure_rows)
    artifacts.extend([IDEA_REGISTER, NEGATIVE_REGISTER])
    update_registers(created_at, screening_rows, queue_rows, failure_rows, artifacts)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "screened_packages": len(screening_rows),
        "stage276_queue_rows": len(queue_rows),
        "failure_memory_rows": len(failure_rows),
        "support_control_rows": len(support_rows),
        "queued_packages": [row["package_id"] for row in queue_rows],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
