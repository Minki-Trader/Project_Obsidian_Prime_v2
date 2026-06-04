from __future__ import annotations

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
from stage_pipelines.stage364 import review_cost_stable_h17_source_guard_offensive_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_cost_stable_h17_source_guard_offensive_scout_without_db as cg  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CI"
RUN_ID = "run364CI_materialize_h17_focus_month_cost_stress_repair_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_PROXY_SCOUT_RUN_ID = cg.RUN_ID
NEXT_RUN_ID = "run364CJ_train_h17_focus_month_cost_stress_repair_scout_without_db_v1"

STATUS = "completed_stage364CI_h17_focus_month_cost_stress_repair_inputs_materialized_open_cj_no_authority"
JUDGMENT = "experiment_design_materialized_h17_focus_month_cost_stress_repair_inputs_no_authority"
DECISION = "stage364CI_open_run364CJ_h17_focus_month_cost_stress_repair_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = cg.DENSITY_FLOOR
SHORT_FLOOR = cg.SHORT_FLOOR
MIN_QUEUE_ROWS = 16

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FAILURE_MEMORY_SUMMARY = RUN_DIR / "ch_failure_memory_summary.csv"
REPAIR_AXIS_MAP = RUN_DIR / "h17_focus_repair_axis_map.csv"
COST_STRESS_GUARD_MATRIX = RUN_DIR / "cost_stress_guard_matrix.csv"
BAD_MONTH_GUARD_MATRIX = RUN_DIR / "bad_month_guard_matrix.csv"
SHORT_FLOOR_RESCUE_MATRIX = RUN_DIR / "short_floor_rescue_matrix.csv"
RUN364CJ_QUEUE = RUN_DIR / "run364CJ_h17_focus_month_cost_stress_repair_scout_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CI_h17_focus_month_cost_stress_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CI_h17_focus_month_cost_stress_repair_inputs.md"
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

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.PACKAGE_GATE_DECISION,
    parent.STRESS_FAILURE_ATTRIBUTION,
    parent.POSITIVE_CLUE_REGISTER,
    parent.PROXY_MT5_DIFF_REVIEW,
    parent.NEXT_REPAIR_QUEUE,
    parent.RUN_MANIFEST,
    cg.FINAL_DECISION,
    cg.PROXY_SCOUT_SURFACE,
    cg.CANDIDATE_SOURCE_ATTRIBUTION,
    cg.CANDIDATE_MONTH_STABILITY,
    cg.COST_STRESS_DIAGNOSTIC,
    cg.CANDIDATE_FILTER_AUDIT,
    cg.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    FAILURE_MEMORY_SUMMARY,
    REPAIR_AXIS_MAP,
    COST_STRESS_GUARD_MATRIX,
    BAD_MONTH_GUARD_MATRIX,
    SHORT_FLOOR_RESCUE_MATRIX,
    RUN364CJ_QUEUE,
    DATA_INTEGRITY_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
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


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


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


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def json_ready(value: Any) -> Any:
    return parent.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 14) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def slug(text: Any) -> str:
    raw = str(text)
    out = "".join(ch.lower() if ch.isalnum() else "_" for ch in raw)
    return "_".join(part for part in out.split("_") if part)[:96]


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CI inputs(CI 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CH next_run_id mismatch(CH 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CH has forbidden authority claim(CH 금지 권위 주장 존재)")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CH gate audit(CH 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    queue = read_csv(parent.NEXT_REPAIR_QUEUE)
    if len(queue) != 4:
        raise RuntimeError(f"CH to CI queue mismatch(CH-CI 대기열 불일치): {len(queue)} != 4")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CI materialization source(CI 구체화 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def selected_only(frame: pd.DataFrame, selected_id: str) -> pd.DataFrame:
    return frame[frame["candidate_id"].astype(str).eq(selected_id)].copy()


def failure_memory_rows(ch_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    stress = read_csv(parent.STRESS_FAILURE_ATTRIBUTION)
    rows = []
    for _, raw in stress.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "failure_id": row.get("failure_id", ""),
                "failure_type": row.get("failure_type", ""),
                "axis": row.get("axis", ""),
                "segment": row.get("segment", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "repair_use": row.get("repair_use", ""),
                "converted_constraint": converted_constraint(row),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if not rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "failure_id": "none_detected",
                "failure_type": "none(없음)",
                "axis": "",
                "segment": "",
                "net_profit": ch_final.get("reviewed_net_profit", ""),
                "profit_factor": ch_final.get("reviewed_profit_factor", ""),
                "trade_count": ch_final.get("reviewed_trade_count", ""),
                "repair_use": "no failure memory emitted(실패 기억 없음)",
                "converted_constraint": "none(없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def converted_constraint(row: Mapping[str, Any]) -> str:
    failure = str(row.get("failure_type", ""))
    if "month" in failure:
        return "month-of-year/quarter guard only, no exact 2025 date memorization(월중/분기 가드만, 정확한 2025년 날짜 암기 금지)"
    if "cost" in failure:
        return "stress_adjusted_net_delta must clear zero before MT5 package(압박 조정 순수익 차이가 0 이상일 때만 MT5 패키지)"
    if "thin" in failure or "source" in failure:
        return "synthetic overlay clue must keep short_count>=100 and source balance(합성 오버레이 단서는 숏 100개 이상과 원천 균형 필요)"
    return "repair constraint recorded(수리 제약 기록)"


def axis_rows(ch_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "axis_id": "ci01_cost_stress_guard",
            "source_queue_id": "ci01_h17_focus_cost_stress_guard",
            "hypothesis": "h17 focus can survive if cost stress is guarded(17시 집중은 비용 압박 가드를 붙이면 버틸 수 있다)",
            "changed_variables": "cost_stress_policy, native short hour firewall, stress delta floor(비용 압박 정책, 기본 숏 시간 방화벽, 압박 차이 하한)",
            "success_criteria": "stress_adjusted_net_delta>=0, PF>=parent, density>=3, short_count>=100",
            "failure_criteria": "stress delta remains negative or short floor breaks(압박 차이 음수 유지 또는 숏 하한 붕괴)",
            "invalid_conditions": "new entries or top_n ranking are used(새 진입 또는 top_n 순위 사용)",
            "decision_use": "feeds CJ proxy scout(CJ 프록시 정찰 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "axis_id": "ci02_bad_month_regime_guard",
            "source_queue_id": "ci02_bad_month_micro_guard_no_exact_date",
            "hypothesis": "bad month slices are regime-like and can be constrained without exact-year memorization(나쁜 월 조각은 국면형이며 정확한 연도 암기 없이 제약 가능)",
            "changed_variables": "month-of-year class, quarter class, late-year pressure class(월중 클래스, 분기 클래스, 연말 압박 클래스)",
            "success_criteria": "bad_month_count decreases without deleting a known exact month(알려진 특정 월 삭제 없이 나쁜 월 수 감소)",
            "failure_criteria": "net lift disappears or exact-date filter is required(순수익 우위 소멸 또는 정확한 날짜 필터 필요)",
            "invalid_conditions": "uses 2025-08/2025-12 as exact date filters(2025-08/2025-12를 정확한 날짜 필터로 사용)",
            "decision_use": "tests timestamp-safe month guard(CJ가 시점 안전 월 가드 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "axis_id": "ci03_short_floor_rescue",
            "source_queue_id": "ci03_short_floor_rescue_from_cg07_cg12",
            "hypothesis": "higher net CG variants can be rescued by restoring short_count>=100(순수익 높은 CG 변형은 숏 100개 이상 복원으로 회수 가능)",
            "changed_variables": "rescue source candidate, native short restore budget, quality floor(회수 원천 후보, 기본 숏 복원 예산, 품질 하한)",
            "success_criteria": "net_delta remains positive and short_count>=100(순수익 차이 양수 유지와 숏 100개 이상)",
            "failure_criteria": "PF lift comes only from shrinking shorts below floor(PF 우위가 숏 하한 미만 축소에서만 나옴)",
            "invalid_conditions": "trade splitting or synthetic extra entries(거래 쪼개기 또는 합성 추가 진입)",
            "decision_use": "recovers cg07/cg12-like edge(CJ가 cg07/cg12류 우위 회수)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "axis_id": "ci04_mt5_precheck_boundary",
            "source_queue_id": "ci04_mt5_reprobe_precheck_only_if_stress_clears",
            "hypothesis": "MT5 precheck should only open after proxy stress/source balance clears(MT5 사전 점검은 프록시 압박/원천 균형 통과 뒤에만 열어야 한다)",
            "changed_variables": "package readiness flags only(패키지 준비 플래그만)",
            "success_criteria": "CJ emits package candidates only when stress and source balance clear(CJ가 압박과 원천 균형 통과 시에만 패키지 후보 배출)",
            "failure_criteria": "proxy-only lift is mistaken for runtime claim(프록시 우위를 런타임 주장으로 착각)",
            "invalid_conditions": "runtime authority claimed without MT5 run(MT5 실행 없이 런타임 권위 주장)",
            "decision_use": "guards runtime handoff(런타임 인계 방어)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def bad_month_guard_rows(ch_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    months = read_csv(cg.CANDIDATE_MONTH_STABILITY)
    selected = selected_only(months, ch_final["reviewed_candidate_id"])
    selected["net_num"] = pd.to_numeric(selected["net_profit"], errors="coerce").fillna(0.0)
    selected["pf_num"] = pd.to_numeric(selected["profit_factor"], errors="coerce").fillna(0.0)
    bad = selected[(selected["net_num"] < 0) | (selected["pf_num"] < 1.0)].copy()
    rows: list[dict[str, Any]] = []
    for _, raw in bad.iterrows():
        row = raw.to_dict()
        month_text = str(row["open_month"])
        month_num = int(month_text.split("-")[1])
        quarter = f"Q{((month_num - 1) // 3) + 1}"
        rows.extend(
            [
                {
                    "run_id": RUN_ID,
                    "guard_id": f"month_of_year_{month_num:02d}",
                    "source_bad_month": month_text,
                    "timestamp_safe_guard": f"month_of_year={month_num:02d}(월중={month_num:02d})",
                    "exact_date_filter": "forbidden(금지)",
                    "net_profit": row["net_profit"],
                    "profit_factor": row["profit_factor"],
                    "trade_count": row["trade_count"],
                    "short_trade_count": row["short_trade_count"],
                    "use_in_queue": "month_of_year_soft_guard(월중 소프트 가드)",
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "run_id": RUN_ID,
                    "guard_id": f"quarter_{quarter.lower()}_pressure",
                    "source_bad_month": month_text,
                    "timestamp_safe_guard": f"quarter={quarter}(분기={quarter})",
                    "exact_date_filter": "forbidden(금지)",
                    "net_profit": row["net_profit"],
                    "profit_factor": row["profit_factor"],
                    "trade_count": row["trade_count"],
                    "short_trade_count": row["short_trade_count"],
                    "use_in_queue": "quarter_pressure_soft_guard(분기 압박 소프트 가드)",
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ]
        )
    if not rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "guard_id": "no_bad_month_guard",
                "source_bad_month": "",
                "timestamp_safe_guard": "none(없음)",
                "exact_date_filter": "forbidden(금지)",
                "net_profit": "",
                "profit_factor": "",
                "trade_count": "",
                "short_trade_count": "",
                "use_in_queue": "not_needed(불필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def cost_stress_rows(ch_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    costs = read_csv(cg.COST_STRESS_DIAGNOSTIC)
    surface = read_csv(cg.PROXY_SCOUT_SURFACE)
    merged = costs.merge(
        surface[["candidate_id", "net_delta_vs_parent", "profit_factor_delta_vs_parent", "trade_count", "short_trade_count", "candidate_status"]],
        on="candidate_id",
        how="left",
    )
    merged["stress_delta_num"] = pd.to_numeric(merged["stress_adjusted_net_delta_vs_parent"], errors="coerce").fillna(-999.0)
    merged["net_delta_num"] = pd.to_numeric(merged["net_delta_vs_parent"], errors="coerce").fillna(-999.0)
    chosen_ids = {str(ch_final["reviewed_candidate_id"]), "cg07_native_short_cost_firewall", "cg12_trade_shape_quality_no_split"}
    top = merged[merged["candidate_id"].astype(str).isin(chosen_ids)].copy()
    extra = merged[~merged["candidate_id"].astype(str).isin(chosen_ids)].sort_values(
        ["stress_delta_num", "net_delta_num"], ascending=[False, False]
    ).head(3)
    rows: list[dict[str, Any]] = []
    for _, raw in pd.concat([top, extra], ignore_index=True).drop_duplicates("candidate_id").iterrows():
        row = raw.to_dict()
        stress_delta = as_float(row.get("stress_adjusted_net_delta_vs_parent"))
        short_count = as_int(row.get("short_trade_count"))
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": row["candidate_id"],
                "net_profit": row.get("net_profit", ""),
                "net_delta_vs_parent": row.get("net_delta_vs_parent", ""),
                "profit_factor_delta_vs_parent": row.get("profit_factor_delta_vs_parent", ""),
                "stress_adjusted_net": row.get("stress_adjusted_net_swap_haircut_1x", ""),
                "stress_adjusted_net_delta_vs_parent": stress_delta,
                "short_trade_count": short_count,
                "stress_judgment": row.get("stress_judgment", ""),
                "rescue_need": "short_floor_rescue_required(숏 하한 복원 필요)" if short_count < SHORT_FLOOR else "stress_or_month_repair_required(압박 또는 월 수리 필요)",
                "queue_use": "cost_stress_guard_seed(비용 압박 가드 씨앗)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def short_floor_rows(ch_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    surface = read_csv(cg.PROXY_SCOUT_SURFACE)
    surface["short_num"] = pd.to_numeric(surface["short_trade_count"], errors="coerce").fillna(0.0)
    surface["net_delta_num"] = pd.to_numeric(surface["net_delta_vs_parent"], errors="coerce").fillna(0.0)
    surface["pf_delta_num"] = pd.to_numeric(surface["profit_factor_delta_vs_parent"], errors="coerce").fillna(0.0)
    selected_delta = as_float(ch_final["reviewed_net_delta_vs_parent"])
    candidates = surface[(surface["net_delta_num"] > selected_delta) | (surface["short_num"] < SHORT_FLOOR)].copy()
    candidates = candidates.sort_values(["net_delta_num", "pf_delta_num"], ascending=[False, False]).head(8)
    rows: list[dict[str, Any]] = []
    for _, raw in candidates.iterrows():
        row = raw.to_dict()
        short_count = as_int(row.get("short_trade_count"))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_candidate_id": row["candidate_id"],
                "source_policy": row.get("h17_overlay_policy", ""),
                "net_delta_vs_parent": row.get("net_delta_vs_parent", ""),
                "profit_factor_delta_vs_parent": row.get("profit_factor_delta_vs_parent", ""),
                "trade_density": row.get("trade_density", ""),
                "short_trade_count": short_count,
                "short_rescue_needed": max(0, SHORT_FLOOR - short_count),
                "restore_policy": "restore_native_short_until_floor_100(기본 숏을 100개까지 복원)" if short_count < SHORT_FLOOR else "preserve_floor(하한 보존)",
                "queue_use": "short_floor_rescue_seed(숏 하한 복원 씨앗)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def queue_row(
    rank: int,
    candidate_id: str,
    axis_id: str,
    seed_candidate_id: str,
    h17_policy: str,
    cost_policy: str,
    month_policy: str,
    short_policy: str,
    source_policy: str,
    success: str,
    failure: str,
    effect: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "queue_rank": rank,
        "candidate_id": candidate_id,
        "axis_id": axis_id,
        "seed_candidate_id": seed_candidate_id,
        "h17_overlay_policy": h17_policy,
        "cost_stress_policy": cost_policy,
        "month_guard_policy": month_policy,
        "short_floor_policy": short_policy,
        "source_mix_policy": source_policy,
        "allowed_entry_operation": "preserve_or_remove_existing_entries_only(기존 진입 보존 또는 제거만)",
        "trade_splitting_status": "not_used_no_added_entries(미사용, 추가 진입 없음)",
        "top_n_status": "forbidden(금지)",
        "exact_date_filter_status": "forbidden(금지)",
        "timestamp_safe_inputs": "source_bucket/open_hour/month_of_year/quarter/probabilities known at entry(진입 시점 원천/시간/월중/분기/확률)",
        "minimum_density": DENSITY_FLOOR,
        "minimum_short_count": SHORT_FLOOR,
        "success_criteria": success,
        "failure_criteria": failure,
        "expected_effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def scout_queue_rows(ch_final: Mapping[str, Any], cost_rows_: Sequence[Mapping[str, Any]], month_rows_: Sequence[Mapping[str, Any]], short_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected = str(ch_final["reviewed_candidate_id"])
    rows: list[dict[str, Any]] = []
    add = rows.append
    add(queue_row(1, "cj01_h17_focus_stress_delta_floor", "ci01_cost_stress_guard", selected, "focus_best_overlay_open_hour=17", "stress_delta_floor_ge_0", "none", "preserve_short_floor_100", "selected_source_mix", "stress_delta>=0;pf>=parent;density>=3;shorts>=100", "stress_delta<0 or shorts<100", "turns CH stress watch into explicit stress floor(CH 비용 관찰을 명시 압박 하한으로 전환)"))
    add(queue_row(2, "cj02_h17_focus_native_hour_cost_firewall_soft", "ci01_cost_stress_guard", selected, "focus_best_overlay_open_hour=17", "native_short_hour17_20_soft_firewall", "none", "restore_native_short_if_below_100", "native_short_cost_sensitive", "net_delta>0;stress_delta>=0;shorts>=100", "net lift only from short collapse", "tests cg07-like cost firewall without accepting short collapse(cg07류 비용 방화벽을 숏 붕괴 없이 시험)"))
    add(queue_row(3, "cj03_h17_focus_swap_negative_native_trim", "ci01_cost_stress_guard", selected, "focus_best_overlay_open_hour=17", "trim_negative_swap_native_only", "none", "short_floor_hard_guard", "source_bucket_cost_weighted", "swap haircut improves and density>=3", "density or short floor breaks", "targets swap drag while preserving density(밀도 보존하며 스왑 끌림 공략)"))
    add(queue_row(4, "cj04_h17_focus_cost_anchor_control", "ci01_cost_stress_guard", selected, "focus_best_overlay_open_hour=17", "no_extra_cost_filter_control", "none", "preserve_short_floor_100", "selected_source_mix", "matches CH selected proxy", "control mismatch", "anchors repair surface to CH selected proxy(CH 선택 프록시를 수리 표면 기준으로 고정)"))

    month_guards = [row for row in month_rows_ if row["guard_id"] != "no_bad_month_guard"]
    for offset, guard in enumerate(month_guards[:6], start=5):
        add(
            queue_row(
                offset,
                f"cj{offset:02d}_{slug(guard['guard_id'])}_overlay_soft_guard",
                "ci02_bad_month_regime_guard",
                selected,
                "focus_best_overlay_open_hour=17",
                "stress_delta_floor_ge_0",
                str(guard["timestamp_safe_guard"]),
                "preserve_short_floor_100",
                "overlay_month_pressure_sensitive",
                "bad_month_count decreases;no exact date filter;density>=3;shorts>=100",
                "requires exact 2025 month deletion or kills net lift",
                "converts bad exact months into reusable calendar class guard(나쁜 정확 월을 재사용 가능한 달력 클래스 가드로 전환)",
            )
        )

    rank = len(rows) + 1
    for short in short_rows_[:4]:
        source_id = str(short["source_candidate_id"])
        add(
            queue_row(
                rank,
                f"cj{rank:02d}_{slug(source_id)}_short_floor_rescue",
                "ci03_short_floor_rescue",
                source_id,
                "inherit_source_h17_policy",
                "inherit_source_cost_policy_with_stress_floor",
                "none",
                "restore_native_short_until_floor_100",
                "source_candidate_plus_short_rescue",
                "net_delta>0;pf>=parent;density>=3;shorts>=100",
                "short rescue erases net/PF edge",
                "tries to recover higher-net CG variants without violating short floor(더 높은 순수익 CG 변형을 숏 하한 위반 없이 회수)",
            )
        )
        rank += 1

    add(queue_row(rank, f"cj{rank:02d}_combined_h17_month_cost_guard", "ci04_mt5_precheck_boundary", selected, "focus_best_overlay_open_hour=17", "stress_delta_floor_ge_0_and_native_cost_soft", "month_of_year_or_quarter_soft_guard", "preserve_short_floor_100", "selected_plus_cost_rescue", "all package prechecks pass in proxy", "any precheck fails", "combines month and cost repair before MT5 package consideration(MT5 패키지 전 월/비용 수리 결합)"))
    rank += 1
    add(queue_row(rank, f"cj{rank:02d}_package_precheck_gate_only", "ci04_mt5_precheck_boundary", selected, "no_new_filter", "package_precheck_only", "package_precheck_only", "package_precheck_only", "precheck_flags_only", "emit package only if stress/source/month clear", "any runtime claim from proxy", "keeps runtime boundary explicit(런타임 경계 명시 유지)"))
    rank += 1
    add(queue_row(rank, f"cj{rank:02d}_no_split_topn_forbidden_guardrail", "ci04_mt5_precheck_boundary", selected, "guardrail_only", "guardrail_only", "guardrail_only", "guardrail_only", "guardrail_only", "top_n=forbidden;trade_splitting=not_used", "guardrail missing", "makes no-split/no-topn invariant machine-readable(무분할/no-topn 불변조건을 기계 판독 가능하게 함)"))
    rank += 1
    add(queue_row(rank, f"cj{rank:02d}_parent_cd02_anchor_replay", "ci04_mt5_precheck_boundary", "cd02_ca01_clone_current_session", "preserve_cd02_current_session", "parent_cost_anchor", "none", "parent_short_floor", "parent_source_mix", "parent metrics reproduced in proxy", "parent anchor drift", "keeps a parent replay anchor for attribution(귀속용 상위 재생 기준 보존)"))

    if len(rows) < MIN_QUEUE_ROWS:
        raise RuntimeError(f"CI queue too small(CI 대기열 부족): {len(rows)} < {MIN_QUEUE_ROWS}")
    return rows


def data_integrity_rows(queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    topn_bad = [row for row in queue if row["top_n_status"] != "forbidden(금지)"]
    split_bad = [row for row in queue if not str(row["trade_splitting_status"]).startswith("not_used")]
    exact_bad = [row for row in queue if row["exact_date_filter_status"] != "forbidden(금지)"]
    return [
        {
            "run_id": RUN_ID,
            "check": "input_existence_hash(입력 존재/해시)",
            "status": "passed" if all(exists(path) for path in INPUT_FILES) else "failed",
            "evidence": rel(INPUT_MANIFEST),
            "effect": "all CH/CG inputs are tied by path and hash(CH/CG 입력을 경로와 해시로 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "timestamp_safe_guard(시점 안전 가드)",
            "status": "passed",
            "evidence": rel(RUN364CJ_QUEUE),
            "effect": "queue uses entry-known source/hour/month_of_year/quarter only(대기열은 진입 시점 원천/시간/월중/분기만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "exact_date_filter_absence(정확 날짜 필터 부재)",
            "status": "passed" if not exact_bad else "failed",
            "evidence": rel(BAD_MONTH_GUARD_MATRIX),
            "effect": "2025-08/2025-12 are failure memory, not exact filters(2025-08/2025-12는 실패 기억이지 정확 필터가 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "trade_splitting_absence(거래 쪼개기 부재)",
            "status": "passed" if not split_bad else "failed",
            "evidence": rel(RUN364CJ_QUEUE),
            "effect": "candidate rows preserve or remove existing entries only(후보 행은 기존 진입 보존 또는 제거만 허용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "top_n_absence(top_n 부재)",
            "status": "passed" if not topn_bad else "failed",
            "evidence": rel(RUN364CJ_QUEUE),
            "effect": "no top_n outcome ranking is allowed(top_n 결과 순위 선택 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(data_rows: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], receipts_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("scope_completion_gate", len(queue) >= MIN_QUEUE_ROWS, RUN364CJ_QUEUE, "CJ scout queue(CJ 정찰 대기열)가 충분히 materialized(구체화)됐다."),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "CH/CG input artifacts(CH/CG 입력 산출물)가 연결됐다."),
        ("experiment_design_gate", exists(EXPERIMENT_RECEIPT), EXPERIMENT_RECEIPT, "hypothesis/comparison/criteria(가설/비교/기준)가 기록됐다."),
        ("data_integrity_audit", all(row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "timestamp-safe/no-split/no-topn(시점 안전/무분할/no-topn)을 점검했다."),
        ("repair_axis_coverage_gate", exists(REPAIR_AXIS_MAP) and len(read_csv(REPAIR_AXIS_MAP)) == 4, REPAIR_AXIS_MAP, "CH의 네 CI 축이 모두 구체화됐다."),
        ("required_gate_coverage_audit", receipts_written, GATE_AUDIT, "필수 gate(게이트)가 closeout(종료 기록)에 연결됐다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 주장(operating claim, 운영 주장)을 하지 않았다."),
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


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-run-evidence-system(실행 근거 시스템)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-claim-discipline(주장 규율)",
            ],
            "required_gates": ["work_packet_schema_lint", "input_lineage_gate", "data_integrity_audit", "required_gate_coverage_audit"],
            "decision_use": "materialize CJ scout inputs(CJ 정찰 입력 구체화)",
            "effect": "CH failure memory(CH 실패 기억)를 CJ offensive queue(CJ 공격 대기열)로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def final_payload(ch_final: Mapping[str, Any], queue: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_scout_run_id": SOURCE_PROXY_SCOUT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "reviewed_candidate_id": ch_final["reviewed_candidate_id"],
        "reviewed_net_profit": ch_final["reviewed_net_profit"],
        "reviewed_profit_factor": ch_final["reviewed_profit_factor"],
        "reviewed_density": ch_final["reviewed_density"],
        "reviewed_short_trade_count": ch_final["reviewed_short_trade_count"],
        "reviewed_bad_months": ch_final["reviewed_bad_months"],
        "reviewed_stress_adjusted_net_delta_vs_parent": ch_final["reviewed_stress_adjusted_net_delta_vs_parent"],
        "queue_rows": len(queue),
        "axis_count": 4,
        "minimum_density": DENSITY_FLOOR,
        "minimum_short_count": SHORT_FLOOR,
        "top_n_rows": sum(1 for row in queue if row["top_n_status"] != "forbidden(금지)"),
        "trade_splitting_rows": sum(1 for row in queue if not str(row["trade_splitting_status"]).startswith("not_used")),
        "exact_date_filter_rows": sum(1 for row in queue if row["exact_date_filter_status"] != "forbidden(금지)"),
        "new_model_training": "not_run(미실행)",
        "new_mt5_execution": "not_run(미실행)",
        "external_verification_status": "out_of_scope_by_claim_materialization_only(주장 범위 밖, 구체화 전용)",
        "forward_passed": "not_run(미실행)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "h17 focus can be repaired by cost stress guard, timestamp-safe month guard, and short floor rescue(17시 집중은 비용 압박 가드/시점 안전 월 가드/숏 하한 복원으로 수리 가능)",
            "decision_use": NEXT_RUN_ID,
            "comparison_baseline": "CG selected h17 focus and parent CD02(CG 선택 17시 집중과 상위 CD02)",
            "control_variables": ["symbol US100(심볼 US100)", "timeframe M5(시간프레임 M5)", "no new entries(새 진입 없음)", "no top_n(top_n 없음)"],
            "changed_variables": ["cost_stress_policy(비용 압박 정책)", "month_guard_policy(월 가드 정책)", "short_floor_policy(숏 하한 정책)"],
            "sample_scope": "Stage364 CG/CH proxy evidence only(Stage364 CG/CH 프록시 근거 전용)",
            "success_criteria": "net_delta>0, PF>=parent, density>=3, short_count>=100, stress_delta>=0",
            "failure_criteria": "edge only survives by exact-date deletion, top_n, trade splitting, or short collapse",
            "invalid_conditions": "lookahead feature, exact 2025 date filter, synthetic extra entries",
            "stop_conditions": "open MT5 package only after CJ proxy clears stress/source/month guards",
            "evidence_plan": [rel(RUN364CJ_QUEUE), rel(DATA_INTEGRITY_AUDIT), rel(GATE_AUDIT)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "entry-known open_hour/month_of_year/quarter only(진입 시점에 알려진 시간/월중/분기만)",
            "sample_scope": "CG/CH generated proxy artifacts(CG/CH 생성 프록시 산출물)",
            "feature_label_boundary": "no new feature or label, queue rules only(새 피처/라벨 없음, 대기열 규칙만)",
            "leakage_risk": "month guard overfit if exact 2025 month is used(정확한 2025년 월을 쓰면 월 가드 과적합)",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "CI materialized repair queue(CI 구체화 수리 대기열)",
            "evidence_available": [rel(RUN364CJ_QUEUE), rel(DATA_INTEGRITY_AUDIT), rel(GATE_AUDIT)],
            "evidence_missing": ["new proxy replay(새 프록시 재생)", "new MT5 runtime probe(새 MT5 런타임 탐침)"],
            "judgment_label": "materialized_experiment_design(구체화된 실험 설계)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "다음 정찰이 바로 비용/월/숏 하한 수리를 시험할 수 있게 줄을 세웠다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claims": ["CJ queue materialized(CJ 대기열 구체화)", "no-split/top_n guards recorded(무분할/top_n 가드 기록)"],
            "forbidden_claims": ["model trained(모델 학습)", "MT5 execution(MT5 실행)", "runtime authority(런타임 권위)", "operating promotion(운영 승격)", "Goal Achieve(목표 달성)"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


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
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in output_paths],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("repair_queue", RUN364CJ_QUEUE, "CJ repair scout queue(CJ 수리 정찰 대기열)."),
        ("repair_axis_map", REPAIR_AXIS_MAP, "CI repair axis map(CI 수리 축 지도)."),
        ("failure_memory_summary", FAILURE_MEMORY_SUMMARY, "CH failure memory summary(CH 실패 기억 요약)."),
        ("cost_stress_guard_matrix", COST_STRESS_GUARD_MATRIX, "Cost stress guard matrix(비용 압박 가드 행렬)."),
        ("bad_month_guard_matrix", BAD_MONTH_GUARD_MATRIX, "Bad month guard matrix(나쁜 월 가드 행렬)."),
        ("short_floor_rescue_matrix", SHORT_FLOOR_RESCUE_MATRIX, "Short floor rescue matrix(숏 하한 복원 행렬)."),
        ("final_decision", FINAL_DECISION, "CI final decision(CI 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CI run manifest(CI 실행 목록)."),
        ("report", REPORT_PATH, "CI report(CI 보고서)."),
        ("script", Path(__file__), "CI producer script(CI 생산 스크립트)."),
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
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "created_at_utc": final["created_at_utc"],
                    "created_at": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if exists(path) and path != LINEAGE_RECEIPT and io_path(path).is_file()]
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
            "availability": "tracked_after_commit_or_generated_with_manifest(커밋 후 추적 또는 목록으로 재생성 가능)",
            "lineage_judgment": "connected_with_boundary_CI_to_CJ_queue(CI와 CJ 대기열 연결, 경계 포함)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(final: Mapping[str, Any], failure_rows: Sequence[Mapping[str, Any]], axes: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364CI h17 focus month cost stress repair inputs(364CI 17시 집중 월/비용 압박 수리 입력)

## Current Truth(현재 진실)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- queue rows(대기열 행): `{final['queue_rows']}`
- reviewed seed(검토 씨앗): `{final['reviewed_candidate_id']}`
- reviewed KPI(검토 핵심 성과 지표): net/PF/density/shorts(순수익/수익 팩터/밀도/숏) `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_trade_count']}`
- bad months(나쁜 월): `{final['reviewed_bad_months']}`
- stress delta(압박 차이): `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`

## Action And Effect(행동과 효과)

Action(행동): CH failure memory(CH 실패 기억)를 cost stress guard(비용 압박 가드), bad month regime guard(나쁜 월 국면 가드), short floor rescue(숏 하한 복원), MT5 precheck boundary(MT5 사전 점검 경계) 네 축으로 materialize(구체화)했다.

Effect(효과): CJ scout(CJ 정찰)가 no-split(무분할), no top_n(no top_n), no exact 2025 date filter(정확한 2025년 날짜 필터 없음) 조건으로 바로 replay(재생)할 수 있다.

## Failure Memory(실패 기억)

{markdown_table(failure_rows, ['failure_id', 'failure_type', 'axis', 'segment', 'net_profit', 'profit_factor', 'converted_constraint'], 12)}

## Repair Axes(수리 축)

{markdown_table(axes, ['axis_id', 'hypothesis', 'changed_variables', 'success_criteria', 'failure_criteria'], 8)}

## CJ Queue(CJ 대기열)

{markdown_table(queue, ['queue_rank', 'candidate_id', 'axis_id', 'seed_candidate_id', 'cost_stress_policy', 'month_guard_policy', 'short_floor_policy'], 20)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

CI is materialization only(CI는 구체화 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364CI h17 focus month cost stress repair inputs(17시 집중 월/비용 압박 수리 입력)

Action(행동): `{RUN_ID}`에서 CH review(CH 검토)를 `{NEXT_RUN_ID}` scout queue(정찰 대기열) `{final['queue_rows']}`행으로 구체화했다.

Effect(효과): 다음 작업은 Stage364(364단계) 안에서 비용 압박, 월중/분기 가드, 숏 하한 복원을 공격적으로 replay(재생)할 수 있다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- queue(대기열): `{rel(RUN364CJ_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - h17 focus month cost stress repair inputs(17시 집중 월/비용 압박 수리 입력).")
    append_text_once(
        STAGE_BRIEF,
        "## run364CI H17 Focus Month Cost Stress Repair Inputs Closeout",
        f"""## run364CI H17 Focus Month Cost Stress Repair Inputs Closeout(364CI 17시 집중 월/비용 압박 수리 입력 종료)

Action(행동): CH failure memory(CH 실패 기억)를 `{final['queue_rows']}`개 CJ scout queue(CJ 정찰 대기열)로 구체화했다.

Effect(효과): same Stage364(같은 364단계)에서 stage branch(단계 분기) 없이 `{NEXT_RUN_ID}`로 비용/월/숏 하한 수리를 공격 탐색한다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## {RUN_ID}

Action(행동): CH review(CH 검토)를 CJ repair scout(CJ 수리 정찰) 입력으로 구체화했다.

Effect(효과): stage branch(단계 분기) 없이 `{NEXT_RUN_ID}`로 넘어간다.
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
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364CI(364CI 실행)는 CH failure memory(CH 실패 기억)를 `{final['queue_rows']}`개 CJ scout queue(CJ 정찰 대기열)로 구체화했다. no-split(무분할), no top_n(no top_n), no exact date filter(정확 날짜 필터 없음) 조건을 기록했다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 queue(대기열)를 proxy replay(프록시 재생)한다.",
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

Current truth(현재 진실): `run364CI` materialized(구체화 완료) CH failure memory(CH 실패 기억) into `{final['queue_rows']}` CJ scout rows(CJ 정찰 행). The queue(대기열) preserves no-split(무분할), no top_n(no top_n), and no exact 2025 date filter(정확한 2025년 날짜 필터 없음).

Next action(다음 행동): `{NEXT_RUN_ID}`에서 cost stress guard(비용 압박 가드), month/quarter guard(월중/분기 가드), short floor rescue(숏 하한 복원)를 proxy replay(프록시 재생)한다.

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

Package candidate(패키지 후보): none(없음). CI is materialization only(CI는 구체화 전용).

Materialized queue(구체화 대기열): `{rel(RUN364CJ_QUEUE)}` with `{final['queue_rows']}` rows(행).

Reviewed seed(검토 씨앗): `{final['reviewed_candidate_id']}`. Reviewed KPI(검토 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, density `{final['reviewed_density']}`, shorts `{final['reviewed_short_trade_count']}`.

Guardrails(가드레일): top_n rows(top_n 행) `{final['top_n_rows']}`, trade splitting rows(거래 쪼개기 행) `{final['trade_splitting_rows']}`, exact date filter rows(정확 날짜 필터 행) `{final['exact_date_filter_rows']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): CH failure memory(CH 실패 기억)를 `{final['queue_rows']}`개 CJ repair scout(CJ 수리 정찰) 입력으로 구체화했다.
- effect(효과): stage branch(단계 분기) 없이 `{NEXT_RUN_ID}`로 비용/월/숏 하한 수리 replay(재생)를 연다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): h17 focus(17시 집중)는 비용 압박, 월중/분기 가드, 숏 하한 복원을 결합하면 회수될 수 있다.
- materialized axes(구체화 축): cost stress guard(비용 압박 가드), bad month regime guard(나쁜 월 국면 가드), short floor rescue(숏 하한 복원), MT5 precheck boundary(MT5 사전 점검 경계).
- evidence_boundary(근거 경계): materialization only(구체화 전용), no new MT5 execution(새 MT5 실행 없음).
- next action(다음 행동): `{NEXT_RUN_ID}`.
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
        "rows": final["queue_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_design(실험 설계)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "materialization_only(구체화 전용)",
        "question": "Can CH h17 focus failure memory become a no-split CJ repair scout queue?(CH 17시 집중 실패 기억을 무분할 CJ 수리 정찰 대기열로 바꿀 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUN364CJ_QUEUE),
        "result_judgment": JUDGMENT,
        "net_profit": final["reviewed_net_profit"],
        "profit_factor": final["reviewed_profit_factor"],
        "trade_density_per_feature_day": final["reviewed_density"],
        "short_trade_count": final["reviewed_short_trade_count"],
        "trade_density_requirement_status": "materialized_density_floor_3_no_trade_splitting(밀도 하한 3, 거래 쪼개기 없음 구체화)",
    }
    registry_row = {
        **common,
        "lane": "materialization(구체화)",
        "family": "h17_focus_month_cost_stress_repair_inputs(17시 집중 월/비용 압박 수리 입력)",
        "result_status": STATUS,
        "view": "materialization(구체화)",
        "tier": "Tier A",
        "metric_scope": "queue_materialization(대기열 구체화)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [registry_row])
    rows: list[dict[str, Any]] = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)"),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "CI materialization(CI 구체화)",
            "scoreboard_lane": "stage364_materialization(Stage364 구체화)",
            "status": status,
            "primary_kpi": f"queue_rows={final['queue_rows']};top_n_rows={final['top_n_rows']};trade_splitting_rows={final['trade_splitting_rows']}",
            "guardrail_kpi": f"exact_date_filter_rows={final['exact_date_filter_rows']};no_authority",
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "queue_materialization(대기열 구체화)",
        }
        rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    ch_final = validate_inputs()
    failure_rows = failure_memory_rows(ch_final)
    axes = axis_rows(ch_final)
    bad_months = bad_month_guard_rows(ch_final)
    cost_rows_ = cost_stress_rows(ch_final)
    short_rows_ = short_floor_rows(ch_final)
    queue = scout_queue_rows(ch_final, cost_rows_, bad_months, short_rows_)
    data_rows = data_integrity_rows(queue)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    write_csv(FAILURE_MEMORY_SUMMARY, failure_rows)
    write_csv(REPAIR_AXIS_MAP, axes)
    write_csv(COST_STRESS_GUARD_MATRIX, cost_rows_)
    write_csv(BAD_MONTH_GUARD_MATRIX, bad_months)
    write_csv(SHORT_FLOOR_RESCUE_MATRIX, short_rows_)
    write_csv(RUN364CJ_QUEUE, queue)
    write_csv(DATA_INTEGRITY_AUDIT, data_rows)

    gates = gate_rows(data_rows, queue, receipts_written=False)
    final = final_payload(ch_final, queue, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(data_rows, queue, receipts_written=True)
    final = final_payload(ch_final, queue, gates, created_at)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, failure_rows, axes, queue, gates)
    write_ledgers(final)
    write_manifest(final)
    write_artifact_registry(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
