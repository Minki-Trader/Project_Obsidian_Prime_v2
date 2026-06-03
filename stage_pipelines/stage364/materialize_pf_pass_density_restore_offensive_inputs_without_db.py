from __future__ import annotations

import csv
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_session_side_pf_lift_density_repair_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AL"
RUN_ID = "run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364AM_train_pf_pass_density_restore_offensive_scout_without_db_v1"

STATUS = "completed_stage364AL_pf_pass_density_restore_offensive_inputs_materialized_no_training_no_mt5_no_authority"
JUDGMENT = "pf_pass_density_restore_offensive_inputs_ready_no_operating_claim"
DECISION = "stage364AL_open_run364AM_pf_pass_density_restore_offensive_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_PF = parent.TARGET_PF

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
DENSITY_RESTORE_PROFILE = RUN_DIR / "density_restore_profile.csv"
SEED_ATTRIBUTION_MATRIX = RUN_DIR / "seed_attribution_matrix.csv"
POLICY_MATERIALIZATION_MAP = RUN_DIR / "policy_materialization_map.csv"
SPLIT_GUARDRAIL_QUEUE = RUN_DIR / "split_guardrail_queue.csv"
RUN364AM_QUEUE = RUN_DIR / "run364AM_scout_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AL_pf_pass_density_restore_offensive_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AL_pf_pass_density_restore_offensive_inputs.md"
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
    parent.NEXT_QUEUE,
    parent.SURFACE_REVIEW,
    parent.PACKAGE_GATE_AUDIT,
    parent.POLICY_REVIEW,
    parent.POSITIVE_CLUES,
    parent.FAILURE_MEMORY,
    parent.SESSION_SIDE_REVIEW,
    parent.MONTH_SIDE_REVIEW,
    parent.scout.SCOUT_SURFACE,
    parent.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    DENSITY_RESTORE_PROFILE,
    SEED_ATTRIBUTION_MATRIX,
    POLICY_MATERIALIZATION_MAP,
    SPLIT_GUARDRAIL_QUEUE,
    RUN364AM_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    ATTRIBUTION_RECEIPT,
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


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    parent.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_csv_rows(path)


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
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


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


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(path, exist_ok=True)


def slug(text: str) -> str:
    out = "".join(ch if ch.isalnum() else "_" for ch in text)
    return "_".join(part for part in out.split("_") if part)


def validate_inputs() -> dict[str, Any]:
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 gate(게이트)가 모두 통과되지 않음)")
    queue = read_csv_rows(parent.NEXT_QUEUE)
    if len(queue) != 12:
        raise RuntimeError(f"unexpected offensive queue rows(공격 대기열 행 수 이상): {len(queue)}")
    if any("trade_splitting forbidden" not in row.get("forbidden(금지)", "") for row in queue):
        raise RuntimeError("trade splitting guardrail missing(거래 쪼개기 금지 가드레일 누락)")
    if any("top_n forbidden" not in row.get("forbidden(금지)", "") for row in queue):
        raise RuntimeError("top_n guardrail missing(top_n 금지 가드레일 누락)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AL inputs(364AL 입력 누락): " + ", ".join(missing))
    return parent_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "role(역할)": input_role(path),
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "run364AL_offensive_queue.csv":
        return "parent offensive queue(부모 공격 대기열)"
    if name == "surface_review.csv":
        return "parent reviewed surface(부모 검토 표면)"
    if name == "session_side_pf_lift_density_repair_proxy_scout_surface.csv":
        return "seed replay surface(씨앗 재생 표면)"
    if "receipt" in name:
        return "gate receipt(게이트 영수증)"
    return "supporting evidence(보조 근거)"


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): dict(row) for row in rows if row.get(key, "")}


def seed_surface_by_variant() -> dict[str, dict[str, str]]:
    return by_key(read_csv_rows(parent.scout.SCOUT_SURFACE), "variant_id")


def review_surface_by_variant() -> dict[str, dict[str, str]]:
    return by_key(read_csv_rows(parent.SURFACE_REVIEW), "variant_id")


def policy_for_queue(queue_id: str) -> dict[str, str]:
    if queue_id.startswith("control_replay_density_anchor"):
        return {
            "materialized_policy": "control_replay_density_anchor(대조 재생 밀도 기준)",
            "session_policy": "all_sessions(전체 세션)",
            "side_policy": "all_sides(전체 방향)",
            "restore_policy": "none(없음)",
            "bridge_policy_override": "",
            "bridge_policy_value_override": "",
        }
    if queue_id.startswith("pfpass_core_short_restore_budget_010"):
        return {
            "materialized_policy": "pf_pass_core_short_density_restore_budget_010(PF 통과 핵심 숏 밀도 복원 0.10)",
            "session_policy": "pfpass_base_plus_core_short_budget(피에프 통과 기준 + 핵심 숏 예산)",
            "side_policy": "long_seed_short_core_budget_010(롱 씨앗 + 핵심 숏 0.10)",
            "restore_policy": "restore_core_short_from_control_budget_010(대조에서 핵심 숏 0.10 복원)",
            "bridge_policy_override": "block_march_long_restore_core_short_budget",
            "bridge_policy_value_override": "0.10",
        }
    if queue_id.startswith("pfpass_core_short_restore_budget_020"):
        return {
            "materialized_policy": "pf_pass_core_short_density_restore_budget_020(PF 통과 핵심 숏 밀도 복원 0.20)",
            "session_policy": "pfpass_base_plus_core_short_budget(피에프 통과 기준 + 핵심 숏 예산)",
            "side_policy": "long_seed_short_core_budget_020(롱 씨앗 + 핵심 숏 0.20)",
            "restore_policy": "restore_core_short_with_margin_budget_020(마진 포함 핵심 숏 0.20 복원)",
            "bridge_policy_override": "block_march_long_restore_core_short_budget",
            "bridge_policy_value_override": "0.20",
        }
    if queue_id.startswith("pfpass_late_long_density_patch"):
        return {
            "materialized_policy": "pf_pass_late_long_density_patch(PF 통과 후반 롱 밀도 패치)",
            "session_policy": "pfpass_base_plus_post_cash_late_long(PF 통과 기준 + 현금장 후반 롱)",
            "side_policy": "long_late_patch_short_seed(후반 롱 패치 + 숏 씨앗)",
            "restore_policy": "restore_sparse_late_long_from_control(대조에서 희소 후반 롱 복원)",
            "bridge_policy_override": "block_march_long_restore_late_long",
            "bridge_policy_value_override": "0.16",
        }
    if queue_id.startswith("pfpass_non_drag_session_restore"):
        return {
            "materialized_policy": "pf_pass_non_drag_session_restore(PF 통과 비끌림 세션 복원)",
            "session_policy": "all_sessions_except_premarket_short(프리마켓 숏 제외 전체)",
            "side_policy": "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)",
            "restore_policy": "restore_non_drag_core_late_from_control(대조에서 비끌림 핵심/후반 복원)",
            "bridge_policy_override": "block_march_long_restore_non_drag_sessions",
            "bridge_policy_value_override": "0.24",
        }
    if queue_id.startswith("density_anchor_pf_floor_012"):
        return {
            "materialized_policy": "density_anchor_margin_floor_012(밀도 기준 마진 하한 0.12)",
            "session_policy": "all_sessions(전체 세션)",
            "side_policy": "all_sides(전체 방향)",
            "restore_policy": "remove_low_margin_from_control(대조에서 낮은 마진 제거)",
            "bridge_policy_override": "restore_march_non_hour16_margin",
            "bridge_policy_value_override": "0.12",
        }
    if queue_id.startswith("density_anchor_hold6_pf_probe"):
        return {
            "materialized_policy": "density_anchor_hold6_pf_probe(밀도 기준 보유 6 PF 탐침)",
            "session_policy": "all_sessions(전체 세션)",
            "side_policy": "all_sides(전체 방향)",
            "restore_policy": "max_hold6_trade_shape_probe(최대 보유 6 거래 형태 탐침)",
            "bridge_policy_override": "",
            "bridge_policy_value_override": "",
        }
    if queue_id.startswith("dd_seed_density_restore_core_late"):
        return {
            "materialized_policy": "dd_seed_core_late_density_restore(낙폭 씨앗 핵심/후반 밀도 복원)",
            "session_policy": "us_cash_core_plus_post_cash_late_long(핵심 + 현금장 후반 롱)",
            "side_policy": "core_both_sides_late_long(핵심 양방향 + 후반 롱)",
            "restore_policy": "restore_core_late_density_from_dd_seed(낙폭 씨앗에서 핵심/후반 밀도 복원)",
            "bridge_policy_override": "block_march_long_restore_core_late",
            "bridge_policy_value_override": "0.29",
        }
    if queue_id.startswith("pfpass_validation_balance_patch"):
        return {
            "materialized_policy": "pf_pass_validation_balance_patch(PF 통과 검증 균형 패치)",
            "session_policy": "all_sessions_with_validation_report(전체 세션, 검증 분리 보고)",
            "side_policy": "all_sides(전체 방향)",
            "restore_policy": "validation_balance_report_only(검증 균형 보고 전용)",
            "bridge_policy_override": "block_march_long_restore_validation_balance",
            "bridge_policy_value_override": "0.18",
        }
    if queue_id.startswith("pfpass_month_pocket_observation"):
        return {
            "materialized_policy": "month_pocket_observation_no_filter(월 포켓 관찰, 필터 아님)",
            "session_policy": "all_sessions(전체 세션)",
            "side_policy": "all_sides(전체 방향)",
            "restore_policy": "month_pockets_report_only_not_filter(월 포켓은 보고 전용, 필터 아님)",
            "bridge_policy_override": "",
            "bridge_policy_value_override": "",
        }
    if queue_id.startswith("density_anchor_short0455_edge"):
        return {
            "materialized_policy": "density_anchor_short0455_edge(밀도 기준 숏 0.455 경계)",
            "session_policy": "all_sessions_except_premarket_short(프리마켓 숏 제외 전체)",
            "side_policy": "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)",
            "restore_policy": "recover_density_edge_0_455(밀도 경계 0.455 복원)",
            "bridge_policy_override": "restore_march_non_hour16_margin",
            "bridge_policy_value_override": "0.10",
        }
    if queue_id.startswith("pfpass_guardrail_no_trade_split"):
        return {
            "materialized_policy": "pf_pass_guardrail_no_trade_split(PF 통과 거래 쪼개기 금지 가드)",
            "session_policy": "guardrail_only_same_as_seed(가드레일 전용, 씨앗 동일)",
            "side_policy": "guardrail_only_same_as_seed(가드레일 전용, 씨앗 동일)",
            "restore_policy": "no_trade_split_no_topn_guardrail(거래 쪼개기와 top_n 금지 가드)",
            "bridge_policy_override": "",
            "bridge_policy_value_override": "",
        }
    return {
        "materialized_policy": "unclassified_materialization(미분류 구체화)",
        "session_policy": "all_sessions(전체 세션)",
        "side_policy": "all_sides(전체 방향)",
        "restore_policy": "none(없음)",
        "bridge_policy_override": "",
        "bridge_policy_value_override": "",
    }


def queue_type(raw_type: str) -> str:
    if raw_type.startswith("control"):
        return "control(대조)"
    if raw_type.startswith("observation"):
        return "observation(관찰)"
    return "candidate(후보)"


def materialized_queue_rows() -> list[dict[str, Any]]:
    raw_queue = read_csv_rows(parent.NEXT_QUEUE)
    seed_surface = seed_surface_by_variant()
    review_surface = review_surface_by_variant()
    rows: list[dict[str, Any]] = []
    for raw in sorted(raw_queue, key=lambda item: as_float(item.get("queue_rank"), 999.0)):
        seed_id = raw.get("seed_variant_id", "")
        seed = seed_surface.get(seed_id, {})
        review = review_surface.get(seed_id, {})
        policy = policy_for_queue(raw.get("queue_id", ""))
        short_threshold = raw.get("short_probability_threshold") or seed.get("short_probability_threshold", "")
        entry_floor = raw.get("entry_margin_floor") or seed.get("entry_margin_floor", "")
        max_hold = raw.get("max_hold_m5") or seed.get("max_hold_m5", "")
        bridge_policy = policy.get("bridge_policy_override") or seed.get("bridge_policy", "")
        bridge_value = policy.get("bridge_policy_value_override") or seed.get("bridge_policy_value", "")
        variant_id = (
            f"{slug(raw.get('queue_id', 'queue'))}"
            f"__seed_{slug(seed_id)[:80]}"
            f"__ps{str(short_threshold).replace('.', '_')}"
            f"__floor{str(entry_floor).replace('.', '_')}"
            f"__hold{max_hold}"
        )
        density_gap = as_float(raw.get("density_gap_to_3day"))
        restore_budget = as_float(raw.get("density_restore_budget"))
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_id": raw.get("queue_id", ""),
                "axis_id": raw.get("axis_id", ""),
                "queue_type": queue_type(raw.get("queue_type", "")),
                "queue_rank": int(as_float(raw.get("queue_rank"), len(rows) + 1)),
                "seed_variant_id": seed_id,
                "source_queue_id": raw.get("source_queue_id", ""),
                "variant_id": variant_id,
                "short_probability_threshold": short_threshold,
                "long_threshold": seed.get("long_threshold", "0.0"),
                "min_margin": seed.get("min_margin", ""),
                "entry_margin_floor": entry_floor,
                "long_block_feature": seed.get("long_block_feature", "adx_14"),
                "long_block_min": seed.get("long_block_min", "40.0"),
                "max_hold_m5": max_hold,
                "bridge_policy": bridge_policy,
                "bridge_policy_value": bridge_value,
                "materialized_policy": policy["materialized_policy"],
                "session_policy": policy["session_policy"],
                "side_policy": policy["side_policy"],
                "restore_policy": policy["restore_policy"],
                "density_gap_to_3day": finite(density_gap, 10),
                "density_restore_budget": finite(restore_budget, 10),
                "density_restore_status": "needs_restore(복원 필요)" if density_gap > 0 else "density_anchor(밀도 기준)",
                "seed_net_profit": review.get("combined_net_profit", seed.get("combined_net_profit", "")),
                "seed_profit_factor": review.get("combined_profit_factor", seed.get("combined_profit_factor", "")),
                "seed_trade_count": review.get("combined_trade_count", seed.get("combined_trade_count", "")),
                "seed_trade_per_business_day": review.get("combined_trade_per_business_day", seed.get("combined_trade_per_business_day", "")),
                "seed_max_drawdown": review.get("combined_max_drawdown", seed.get("combined_max_drawdown", "")),
                "seed_short_count": review.get("combined_short_count", seed.get("combined_short_count", "")),
                "min_density_requirement": DENSITY_FLOOR,
                "target_profit_factor": TARGET_PF,
                "validation_guardrail": "validation_net_positive_report_separate(검증 순수익 양수 분리 보고)",
                "oos_guardrail": "oos_locked_no_threshold_selection(표본외 잠금, 임계값 선택 없음)",
                "trade_splitting_status": "not_used(거래 쪼개기 없음)",
                "top_n_status": "forbidden(금지)",
                "timestamp_boundary": "entry_time_known_only(진입 시점에 알려진 값만 사용)",
                "forbidden(금지)": raw.get("forbidden(금지)", ""),
                "expected_effect(기대 효과)": raw.get("expected_effect(기대 효과)", ""),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def density_profile_rows(parent_final: Mapping[str, Any], materialized: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    pf_rows = [row for row in materialized if as_float(row.get("seed_profit_factor")) >= TARGET_PF and as_float(row.get("seed_trade_per_business_day")) < DENSITY_FLOOR]
    anchor_rows = [row for row in materialized if str(row.get("density_restore_status")) == "density_anchor(밀도 기준)"]
    return [
        {
            "run_id": RUN_ID,
            "profile_id": "selected_density_anchor(선택 밀도 기준)",
            "source": parent_final.get("parent_selected_variant_id", ""),
            "net_profit": parent_final.get("parent_selected_net_profit", ""),
            "profit_factor": parent_final.get("parent_selected_profit_factor", ""),
            "density": parent_final.get("parent_selected_density", ""),
            "drawdown": parent_final.get("parent_selected_drawdown", ""),
            "effect(효과)": "density(밀도)는 유지되지만 PF(수익 팩터)가 목표 아래라 공격 수리 기준으로 쓴다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "profile_id": "pf_pass_density_fail_seed(PF 통과 밀도 실패 씨앗)",
            "source": "; ".join(row.get("seed_variant_id", "") for row in pf_rows),
            "net_profit": "; ".join(str(row.get("seed_net_profit", "")) for row in pf_rows),
            "profit_factor": "; ".join(str(row.get("seed_profit_factor", "")) for row in pf_rows),
            "density": "; ".join(str(row.get("seed_trade_per_business_day", "")) for row in pf_rows),
            "drawdown": "; ".join(str(row.get("seed_max_drawdown", "")) for row in pf_rows),
            "effect(효과)": "PF(수익 팩터) 통과 씨앗을 density restore(밀도 복원) 대상으로 고정한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "profile_id": "control_and_observation_rows(대조 및 관찰 행)",
            "source": "; ".join(row.get("queue_id", "") for row in anchor_rows),
            "net_profit": "",
            "profit_factor": "",
            "density": "",
            "drawdown": "",
            "effect(효과)": "control(대조)과 observation(관찰)을 후보와 섞어 승격하지 않게 한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]


def attribution_rows(materialized: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in materialized:
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "axis_id": row.get("axis_id", ""),
                "seed_variant_id": row.get("seed_variant_id", ""),
                "seed_profit_factor": row.get("seed_profit_factor", ""),
                "seed_density": row.get("seed_trade_per_business_day", ""),
                "density_gap_to_3day": row.get("density_gap_to_3day", ""),
                "density_restore_budget": row.get("density_restore_budget", ""),
                "session_policy": row.get("session_policy", ""),
                "side_policy": row.get("side_policy", ""),
                "restore_policy": row.get("restore_policy", ""),
                "effect(효과)": "next scout(다음 정찰)에서 KPI(핵심 성과 지표) 변화 원인을 정책별로 나누게 한다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def split_guardrail_rows(materialized: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "guardrail_id": "validation_oos_separate(검증/표본외 분리)",
            "status": "required(필수)",
            "applies_to_rows": len(materialized),
            "forbidden(금지)": "OOS threshold selection(표본외 임계값 선택)",
            "effect(효과)": "OOS(표본외)를 최종 threshold(임계값) 선택에 쓰는 미래참조를 막는다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail_id": "no_trade_splitting(거래 쪼개기 없음)",
            "status": "required(필수)",
            "applies_to_rows": len(materialized),
            "forbidden(금지)": "splitting one signal into partial pseudo-trades(한 신호를 부분 가상 거래로 쪼개기)",
            "effect(효과)": "trade per day(일별 거래수) 3 이상을 거래 쪼개기로 만드는 것을 막는다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail_id": "no_topn_post_entry(top_n 진입 후 순위 없음)",
            "status": "required(필수)",
            "applies_to_rows": len(materialized),
            "forbidden(금지)": "post-entry ranking(진입 후 순위)",
            "effect(효과)": "현재 시점 이후 정보로 좋은 거래만 고르는 bias(편향)를 막는다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": status,
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "queue_materialization_gate",
                "density_requirement_gate",
                "topn_absence_gate",
                "trade_splitting_absence_gate",
                "data_integrity_audit",
                "experiment_design_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final_seed: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final_seed["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "entry timestamp only; no post-entry ranking(진입 시각만 사용, 진입 후 순위 없음)",
            "sample_scope": "US100 M5 Stage364 Tier A materialization only(US100 5분봉 Stage364 티어 A 구체화 전용)",
            "missing_or_duplicate_check": "12 queue rows and parent gate evidence verified(대기열 12행과 부모 게이트 근거 확인)",
            "feature_label_boundary": "no new features or labels; policy rows only(새 피처/라벨 없음, 정책 행 전용)",
            "split_boundary": "validation/OOS separate guardrail written(검증/표본외 분리 가드레일 기록)",
            "leakage_risk": "month pocket observation is not a filter(월 포켓 관찰은 필터가 아님)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-experiment-design(실험 설계)",
            "hypothesis": "PF-pass rows can restore density through session/side rules without trade splitting(PF 통과 행은 세션/방향 규칙으로 거래 쪼개기 없이 밀도를 복원할 수 있음)",
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": "US100 M5, fixed seed surfaces, no top_n, no trade splitting(US100 5분봉, 고정 씨앗 표면, top_n 없음, 거래 쪼개기 없음)",
            "changed_variables": "session policy, side policy, short threshold, margin floor, max hold(세션 정책, 방향 정책, 숏 임계값, 마진 하한, 최대 보유)",
            "success_criteria": "run364AM can test PF>=1.30 and density>=3/day(run364AM이 PF 1.30 이상과 하루 밀도 3 이상을 시험 가능)",
            "failure_criteria": "queue omits controls, uses top_n, permits trade splitting, or uses OOS selection(대조 누락, top_n 사용, 거래 쪼개기 허용, 표본외 선택 사용)",
            "evidence_plan": [rel(RUN364AM_QUEUE), rel(SPLIT_GUARDRAIL_QUEUE), rel(GATE_AUDIT)],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "observed_change": "materialization only; no new KPI generated(구체화 전용, 새 KPI 생성 없음)",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers_to_test": "core short restore, late long patch, non-drag session restore, hold6 shape(핵심 숏 복원, 후반 롱 패치, 비끌림 세션 복원, 보유 6 형태)",
            "segment_checks": [rel(parent.SESSION_SIDE_REVIEW), rel(parent.MONTH_SIDE_REVIEW)],
            "trade_shape": "next run will measure trade count and density(다음 실행이 거래수와 밀도를 측정)",
            "attribution_confidence": "not_applicable_until_replay(재생 전까지 적용 없음)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect(효과)": "materialization(구체화)을 운영 주장으로 승격하지 않는다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AL materialization(구체화)을 완료했다."),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AK 산출물과 queue(대기열)를 확인했다."),
        gate_row("queue_materialization_gate(대기열 구체화 게이트)", RUN364AM_QUEUE, "run364AM scout queue(정찰 대기열)를 만들었다."),
        gate_row("density_requirement_gate(밀도 요구 게이트)", DENSITY_RESTORE_PROFILE, "density floor(밀도 하한) 3/day 기준을 명시했다."),
        gate_row("topn_absence_gate(top_n 부재 게이트)", RUN364AM_QUEUE, "top_n 금지를 모든 행에 기록했다."),
        gate_row("trade_splitting_absence_gate(거래 쪼개기 부재 게이트)", RUN364AM_QUEUE, "거래 쪼개기 없음 상태를 모든 행에 기록했다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "timestamp-safe(시점 안전) 경계를 기록했다."),
        gate_row("experiment_design_gate(실험 설계 게이트)", EXPERIMENT_RECEIPT, "다음 scout(정찰)의 가설과 실패 조건을 기록했다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 hash(해시)를 연결했다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "운영 승격을 주장하지 않았다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 gate(게이트)를 종료 기록에 연결했다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def final_payload(parent_final: Mapping[str, Any], materialized: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    control_rows = sum(1 for row in materialized if row.get("queue_type") == "control(대조)")
    observation_rows = sum(1 for row in materialized if row.get("queue_type") == "observation(관찰)")
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_package_decision": parent_final.get("package_decision"),
        "parent_pf_pass_density_fail_rows": parent_final.get("pf_pass_density_fail_rows"),
        "parent_selected_variant_id": parent_final.get("parent_selected_variant_id"),
        "parent_selected_net_profit": parent_final.get("parent_selected_net_profit"),
        "parent_selected_profit_factor": parent_final.get("parent_selected_profit_factor"),
        "parent_selected_density": parent_final.get("parent_selected_density"),
        "queue_rows": len(materialized),
        "control_rows": control_rows,
        "candidate_rows": len(materialized) - control_rows - observation_rows,
        "observation_rows": observation_rows,
        "top_n_rows": sum(1 for row in materialized if row.get("top_n_status") != "forbidden(금지)"),
        "trade_splitting_rows": sum(1 for row in materialized if row.get("trade_splitting_status") != "not_used(거래 쪼개기 없음)"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def refresh_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = STAGE_BRIEF.read_text(encoding="utf-8-sig")
    lines = []
    for line in text.splitlines():
        if line.startswith("- current_run_id"):
            lines.append(f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`")
        elif line.startswith("- latest_completed_run_id"):
            lines.append(f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`")
        elif line.startswith("- selection_status"):
            lines.append(f"- selection_status(선택 상태): `{STATUS}`")
        elif line.startswith("- claim_boundary"):
            lines.append(f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
        else:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines) + "\n")


def write_docs(final: Mapping[str, Any], materialized: Sequence[Mapping[str, Any]], profile: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AL PF-pass density restore offensive inputs(364AL PF 통과 밀도 복원 공격 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- queue_rows(대기열 행): `{final['queue_rows']}`
- control/candidate/observation(대조/후보/관찰): `{final['control_rows']}` / `{final['candidate_rows']}` / `{final['observation_rows']}`
- top_n_rows(top_n 행): `{final['top_n_rows']}`
- trade_splitting_rows(거래 쪼개기 행): `{final['trade_splitting_rows']}`
- runtime_authority(런타임 권위): `not_claimed`

## Density Profile(밀도 프로필)

{markdown_table(profile, ['profile_id', 'source', 'profit_factor', 'density', 'drawdown', 'effect(효과)'])}

## Materialized Queue(구체화 대기열)

{markdown_table(list(materialized), ['queue_rank', 'queue_id', 'queue_type', 'seed_profit_factor', 'seed_trade_per_business_day', 'density_restore_budget', 'materialized_policy'])}

## Guardrails(가드레일)

- top_n(상위 N개): `forbidden(금지)`
- trade_splitting(거래 쪼개기): `not_used(없음)`
- OOS threshold selection(표본외 임계값 선택): `forbidden(금지)`

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): run364AL은 next scout(다음 정찰) 입력만 만들며 package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- queue_rows(대기열 행): `{final['queue_rows']}`\n- effect(효과): `{NEXT_RUN_ID}` scout queue(정찰 대기열)를 만들었다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AL PF-Pass Density Restore Offensive Inputs Closeout",
        f"\n## run364AL PF-Pass Density Restore Offensive Inputs Closeout(364AL PF 통과 밀도 복원 공격 입력 종료)\n\nAction(행동): run364AK(364AK 실행) offensive queue(공격 대기열) 12개를 run364AM(364AM 실행) scout queue(정찰 대기열)로 구체화했다.\n\nEffect(효과): 거래 쪼개기와 top_n(상위 N개)을 금지한 채 PF-pass density restore(PF 통과 밀도 복원) 탐색을 다음 실행으로 넘긴다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(구체화 전용이라 없음)
- latest_materialization(최근 구체화): `{RUN_ID}`
- next_scout_queue(다음 정찰 대기열): `{rel(RUN364AM_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): run364AL(364AL 실행)은 PF-pass density restore(PF 통과 밀도 복원) offensive queue(공격 대기열) 12개를 next scout(다음 정찰) 입력으로 구체화했다. top_n(상위 N개)과 trade_splitting(거래 쪼개기)은 모두 금지 상태다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 구체화된 queue(대기열)를 proxy replay(프록시 재생)로 검증한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
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
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): PF-pass density restore offensive inputs(PF 통과 밀도 복원 공격 입력)를 구체화했다.\n- effect(효과): `{NEXT_RUN_ID}` scout queue(정찰 대기열)를 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): PF-pass density-fail(PF 통과 밀도 실패) 씨앗을 core short(핵심 숏), late long(후반 롱), non-drag session(비끌림 세션) 복원 축으로 나눈다.\n- effect(효과): PF(수익 팩터) 1.30과 density(밀도) 3/day를 동시에 요구하는 다음 정찰 입력을 만든다.\n",
    )
    append_text_once(
        STAGE_README,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- action(행동): run364AK(364AK 실행) queue(대기열)를 run364AM(364AM 실행) 입력으로 구체화했다.\n- effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 공격 탐색을 이어간다.\n",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "lane": "materialization(구체화)",
        "scoreboard_lane": "materialization(구체화)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"queue_rows={final['queue_rows']}; controls={final['control_rows']}; candidates={final['candidate_rows']}; observations={final['observation_rows']}",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["queue_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(RUN364AM_QUEUE),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_design(실험 설계)",
        "trade_density_requirement_status": "materialized_density_floor_3day_no_trade_split(밀도 하한 하루 3, 거래 쪼개기 없음 구체화)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "evidence_scope": "materialization_no_authority(구체화, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can PF-pass density-fail seeds restore 3/day density without trade splitting?(PF 통과 밀도 실패 씨앗이 거래 쪼개기 없이 하루 3 밀도를 복원할 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "materialized queue(구체화 대기열)"),
        (f"{RUN_ID}__Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "missing_required(필수 누락)"),
        (f"{RUN_ID}__Tier_A_plus_B", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A only plus Tier B missing_required(Tier A만 있고 Tier B 필수 누락)"),
    ]:
        row = dict(common)
        row.update({"ledger_row_id": subrun_id, "subrun_id": subrun_id, "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": kpi_scope})
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("density_restore_profile", DENSITY_RESTORE_PROFILE, "Density restore profile(밀도 복원 프로필)."),
            ("seed_attribution_matrix", SEED_ATTRIBUTION_MATRIX, "Seed attribution matrix(씨앗 귀속 행렬)."),
            ("policy_materialization_map", POLICY_MATERIALIZATION_MAP, "Policy materialization map(정책 구체화 지도)."),
            ("split_guardrail_queue", SPLIT_GUARDRAIL_QUEUE, "Split guardrail queue(분할 가드레일 대기열)."),
            ("next_queue", RUN364AM_QUEUE, "Next scout queue(다음 정찰 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in outputs],
            "artifact_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    materialized = materialized_queue_rows()
    profile = density_profile_rows(parent_final, materialized)
    attribution = attribution_rows(materialized)
    guardrails = split_guardrail_rows(materialized)
    write_csv(DENSITY_RESTORE_PROFILE, profile)
    write_csv(SEED_ATTRIBUTION_MATRIX, attribution)
    write_csv(POLICY_MATERIALIZATION_MAP, materialized)
    write_csv(SPLIT_GUARDRAIL_QUEUE, guardrails)
    write_csv(RUN364AM_QUEUE, materialized)
    write_work_packet()

    created_at = now_utc()
    final_seed = {"created_at_utc": created_at}
    gates = write_receipts(final_seed)
    final = final_payload(parent_final, materialized, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, materialized, profile, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
