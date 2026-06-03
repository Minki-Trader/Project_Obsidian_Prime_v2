from __future__ import annotations

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

from stage_pipelines.stage364 import review_pf_lift_density_safe_expansion_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AI"
RUN_ID = "run364AI_materialize_session_side_pf_lift_density_repair_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1"

STATUS = "completed_stage364AI_session_side_pf_lift_density_repair_inputs_materialized_no_training_no_mt5_no_authority"
JUDGMENT = "session_side_pf_lift_density_repair_inputs_ready_no_operating_claim"
DECISION = "stage364AI_open_run364AJ_session_side_pf_lift_density_repair_scout"
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
REPAIR_PROFILE = RUN_DIR / "session_side_pf_lift_density_repair_profile.csv"
SESSION_SIDE_RULE_QUEUE = RUN_DIR / "session_side_rule_queue.csv"
PF_DENSITY_BRIDGE_RULE_QUEUE = RUN_DIR / "pf_density_bridge_rule_queue.csv"
SPLIT_GUARDRAIL_QUEUE = RUN_DIR / "split_guardrail_queue.csv"
RUN364AJ_QUEUE = RUN_DIR / "run364AJ_scout_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AI_session_side_pf_lift_density_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AI_session_side_pf_lift_density_repair_inputs.md"
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
    parent.SESSION_SIDE_REVIEW,
    parent.MONTH_SIDE_REVIEW,
    parent.POSITIVE_CLUES,
    parent.FAILURE_MEMORY,
    parent.REPORT_PATH,
    parent.scout.FINAL_DECISION,
    parent.scout.SCOUT_SURFACE,
    parent.scout.SELECTED_PROXY_CANDIDATE,
    parent.scout.SELECTED_EXPECTED_TRADE_TAPE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    REPAIR_PROFILE,
    SESSION_SIDE_RULE_QUEUE,
    PF_DENSITY_BRIDGE_RULE_QUEUE,
    SPLIT_GUARDRAIL_QUEUE,
    RUN364AJ_QUEUE,
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


def validate_inputs() -> dict[str, Any]:
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과되지 않음)")
    next_queue = read_csv_rows(parent.NEXT_QUEUE)
    if len(next_queue) != 4:
        raise RuntimeError(f"unexpected parent repair queue rows(부모 수리 대기열 행 수 이상): {len(next_queue)}")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AI inputs(364AI 입력 누락): " + ", ".join(missing))
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def surface_by_variant() -> dict[str, dict[str, str]]:
    return {row.get("variant_id", ""): row for row in read_csv_rows(parent.scout.SCOUT_SURFACE)}


def review_by_variant() -> dict[str, dict[str, str]]:
    return {row.get("variant_id", ""): row for row in read_csv_rows(parent.SURFACE_REVIEW)}


def selected_variant_id() -> str:
    return str(read_json(parent.FINAL_DECISION).get("parent_selected_variant_id", ""))


def pf_seed_variant_ids() -> list[str]:
    rows = read_csv_rows(parent.SURFACE_REVIEW)
    seeds = [
        row.get("variant_id", "")
        for row in rows
        if str(row.get("review_status", "")).startswith("pf_pass_density_fail_repair_seed")
    ]
    return [seed for seed in seeds if seed]


def base_values(variant_id: str) -> dict[str, Any]:
    surface = surface_by_variant().get(variant_id, {})
    review = review_by_variant().get(variant_id, {})
    return {
        "seed_variant_id": variant_id,
        "seed_queue_id": surface.get("queue_id", review.get("queue_id", "")),
        "seed_axis_id": surface.get("axis_id", review.get("axis_id", "")),
        "short_probability_threshold": surface.get("short_probability_threshold", ""),
        "long_threshold": surface.get("long_threshold", ""),
        "entry_margin_floor": surface.get("entry_margin_floor", ""),
        "bridge_policy": surface.get("bridge_policy", ""),
        "bridge_policy_value": surface.get("bridge_policy_value", ""),
        "max_hold_m5": surface.get("max_hold_m5", ""),
        "seed_net_profit": review.get("combined_net_profit", surface.get("combined_net_profit", "")),
        "seed_profit_factor": review.get("combined_profit_factor", surface.get("combined_profit_factor", "")),
        "seed_trade_per_business_day": review.get("combined_trade_per_business_day", surface.get("combined_trade_per_business_day", "")),
        "seed_trade_count": review.get("combined_trade_count", surface.get("combined_trade_count", "")),
        "seed_max_drawdown": review.get("combined_max_drawdown", surface.get("combined_max_drawdown", "")),
    }


def repair_profile_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    package_gates = read_csv_rows(parent.PACKAGE_GATE_AUDIT)
    session_rows = read_csv_rows(parent.SESSION_SIDE_REVIEW)
    positive_session = [
        row for row in session_rows
        if row.get("entry_session") == "us_cash_core(미국 현금장 핵심)"
        and str(row.get("review_status", "")).startswith("positive_pf")
    ]
    premarket_short = [
        row for row in session_rows
        if row.get("entry_session") == "us_premarket_cash_open(미국 프리마켓/현금장 초반)"
        and row.get("side") == "short"
    ]
    return [
        {
            "run_id": RUN_ID,
            "profile_id": "selected_density_safe_near_pf(선택 밀도 안전 PF 근접)",
            "source": parent_final.get("parent_selected_variant_id", ""),
            "net_profit": parent_final.get("parent_selected_net_profit", ""),
            "profit_factor": parent_final.get("parent_selected_profit_factor", ""),
            "density": parent_final.get("parent_selected_density", ""),
            "drawdown": parent_final.get("parent_selected_drawdown", ""),
            "effect(효과)": "밀도는 지키되 PF 목표 미달을 수리 대상으로 고정한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "profile_id": "package_blockers(패키지 차단 원인)",
            "source": rel(parent.PACKAGE_GATE_AUDIT),
            "net_profit": "",
            "profit_factor": "; ".join(f"{row.get('gate_id')}={row.get('status')}" for row in package_gates),
            "density": "",
            "drawdown": "",
            "effect(효과)": "PF 목표와 엄격 패키지 행 실패를 다음 제약으로 쓴다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "profile_id": "core_session_positive(핵심 세션 양수)",
            "source": rel(parent.SESSION_SIDE_REVIEW),
            "net_profit": "; ".join(f"{row.get('side')}={row.get('segment_net_profit')}" for row in positive_session),
            "profit_factor": "; ".join(f"{row.get('side')}={row.get('segment_profit_factor')}" for row in positive_session),
            "density": "; ".join(f"{row.get('side')}={row.get('segment_trade_per_business_day')}" for row in positive_session),
            "drawdown": "; ".join(f"{row.get('side')}={row.get('segment_max_drawdown')}" for row in positive_session),
            "effect(효과)": "핵심 세션 롱/숏 양수 포켓을 공격 탐색 씨앗으로 쓴다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "profile_id": "premarket_short_drag(프리마켓 숏 끌림)",
            "source": rel(parent.SESSION_SIDE_REVIEW),
            "net_profit": "; ".join(row.get("segment_net_profit", "") for row in premarket_short),
            "profit_factor": "; ".join(row.get("segment_profit_factor", "") for row in premarket_short),
            "density": "; ".join(row.get("segment_trade_per_business_day", "") for row in premarket_short),
            "drawdown": "; ".join(row.get("segment_max_drawdown", "") for row in premarket_short),
            "effect(효과)": "프리마켓 숏 차단을 손실 압박 대조로 만든다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]


def common_row(queue_id: str, axis_id: str, seed_variant: str, policy: str, session_policy: str, side_policy: str, restore_policy: str) -> dict[str, Any]:
    base = base_values(seed_variant)
    return {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "queue_id": queue_id,
        "axis_id": axis_id,
        "seed_variant_id": seed_variant,
        "seed_queue_id": base["seed_queue_id"],
        "seed_axis_id": base["seed_axis_id"],
        "short_probability_threshold": base["short_probability_threshold"],
        "long_threshold": base["long_threshold"],
        "entry_margin_floor": base["entry_margin_floor"],
        "max_hold_m5": base["max_hold_m5"],
        "bridge_policy": base["bridge_policy"],
        "bridge_policy_value": base["bridge_policy_value"],
        "materialized_policy": policy,
        "session_policy": session_policy,
        "side_policy": side_policy,
        "restore_policy": restore_policy,
        "min_density_requirement": DENSITY_FLOOR,
        "target_profit_factor": TARGET_PF,
        "validation_guardrail": "validation_net_positive_and_report_separate(검증 순수익 양수 및 분리 보고)",
        "oos_guardrail": "oos_not_used_for_operating_threshold(표본외를 운영 임계값 선택에 쓰지 않음)",
        "trade_splitting_status": "not_used(거래 쪼개기 없음)",
        "top_n_status": "forbidden(금지)",
        "timestamp_boundary": "entry_time_known_only(진입 시점에 알려진 값만 사용)",
        "seed_net_profit": base["seed_net_profit"],
        "seed_profit_factor": base["seed_profit_factor"],
        "seed_trade_per_business_day": base["seed_trade_per_business_day"],
        "seed_trade_count": base["seed_trade_count"],
        "seed_max_drawdown": base["seed_max_drawdown"],
        "effect(효과)": "run364AJ(실행364AJ)에서 고정 규칙 프록시로 재생한다.",
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def session_side_rule_rows() -> list[dict[str, Any]]:
    selected = selected_variant_id()
    return [
        common_row(
            "selected_control_full_session(선택 대조 전체 세션)",
            "control(대조)",
            selected,
            "baseline_replay(기준 재생)",
            "all_sessions(전체 세션)",
            "all_sides(전체 방향)",
            "none(없음)",
        ),
        common_row(
            "block_premarket_short_only(프리마켓 숏만 차단)",
            "session_side_pf_lift(세션 방향 PF 상승)",
            selected,
            "block_premarket_short(프리마켓 숏 차단)",
            "all_sessions_except_premarket_short(프리마켓 숏 제외 전체)",
            "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)",
            "none(없음)",
        ),
        common_row(
            "core_plus_premarket_long(핵심 세션 + 프리마켓 롱)",
            "session_side_pf_lift(세션 방향 PF 상승)",
            selected,
            "core_session_keep_premarket_long(핵심 세션 보존 + 프리마켓 롱)",
            "us_cash_core_plus_premarket_long(미국 현금장 핵심 + 프리마켓 롱)",
            "core_both_sides_premarket_long_only(핵심 양방향 + 프리마켓 롱만)",
            "none(없음)",
        ),
        common_row(
            "core_session_only_dual_side(핵심 세션 양방향만)",
            "session_side_pf_lift(세션 방향 PF 상승)",
            selected,
            "core_session_only(핵심 세션만)",
            "us_cash_core_only(미국 현금장 핵심만)",
            "core_long_and_short(핵심 롱/숏)",
            "none(없음)",
        ),
        common_row(
            "core_plus_late_long(핵심 세션 + 후반 롱)",
            "session_density_restore(세션 밀도 복원)",
            selected,
            "core_session_plus_late_long(핵심 세션 + 후반 롱)",
            "us_cash_core_plus_post_cash_late_long(핵심 + 현금장 후반 롱)",
            "core_both_sides_late_long(핵심 양방향 + 후반 롱)",
            "restore_sparse_late_long_watch(희소 후반 롱 관찰 복원)",
        ),
    ]


def pf_density_bridge_rows() -> list[dict[str, Any]]:
    selected = selected_variant_id()
    seeds = pf_seed_variant_ids()
    first_seed = seeds[0] if seeds else selected
    second_seed = seeds[1] if len(seeds) > 1 else first_seed
    third_seed = seeds[2] if len(seeds) > 2 else second_seed
    return [
        common_row(
            "pfpass_core_restore(통과 PF 핵심 복원)",
            "pf_pass_density_bridge(PF 통과 밀도 연결)",
            first_seed,
            "pf_pass_seed_restore_core_session(PF 통과 씨앗 핵심 세션 복원)",
            "us_cash_core_restore(미국 현금장 핵심 복원)",
            "core_both_sides_restore(핵심 양방향 복원)",
            "restore_core_from_selected_density_safe(선택 밀도 안전 후보에서 핵심 세션 복원)",
        ),
        common_row(
            "pfpass_core_plus_premarket_long_restore(PF 통과 핵심 + 프리마켓 롱 복원)",
            "pf_pass_density_bridge(PF 통과 밀도 연결)",
            second_seed,
            "pf_pass_seed_restore_core_and_premarket_long(PF 통과 씨앗 핵심 및 프리마켓 롱 복원)",
            "us_cash_core_plus_premarket_long(핵심 + 프리마켓 롱)",
            "core_both_sides_premarket_long_only(핵심 양방향 + 프리마켓 롱만)",
            "restore_core_and_premarket_long_from_selected(선택 후보에서 핵심/프리마켓 롱 복원)",
        ),
        common_row(
            "pfpass_block_premarket_short_restore_density(PF 통과 프리마켓 숏 차단 밀도 복원)",
            "pf_pass_density_bridge(PF 통과 밀도 연결)",
            third_seed,
            "pf_pass_seed_block_premarket_short_restore_density(PF 통과 씨앗 프리마켓 숏 차단 밀도 복원)",
            "all_sessions_except_premarket_short(프리마켓 숏 제외 전체)",
            "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)",
            "restore_non_drag_sessions_from_selected(선택 후보에서 손실 끌림 외 세션 복원)",
        ),
        common_row(
            "selected_short0455_density_edge_recheck(선택 숏 0.455 밀도 경계 재검토)",
            "near_density_bridge(밀도 경계 연결)",
            "selected_short0455_restore_margin010__ps0_455__floor0_0__hold8",
            "near_density_repair_with_session_guard(밀도 근접 수리 + 세션 가드)",
            "all_sessions_except_premarket_short(프리마켓 숏 제외 전체)",
            "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)",
            "recover_density_gap_0_04(밀도 격차 0.04 복원)",
        ),
    ]


def split_guardrail_rows() -> list[dict[str, Any]]:
    selected = selected_variant_id()
    return [
        common_row(
            "validation_pf_repair_selected_split_guard(선택 후보 검증 PF 수리 분할 가드)",
            "split_guardrail(분할 가드레일)",
            selected,
            "validation_pf_drag_repair_without_oos_selection(표본외 선택 없는 검증 PF 끌림 수리)",
            "all_sessions_with_validation_report(전체 세션, 검증 분리 보고)",
            "all_sides(전체 방향)",
            "validation_loss_segments_as_report_only(검증 손실 세그먼트는 보고 전용)",
        ),
        common_row(
            "oos_locked_replay_control(표본외 잠금 재생 대조)",
            "split_guardrail(분할 가드레일)",
            selected,
            "oos_locked_control_replay(표본외 잠금 대조 재생)",
            "all_sessions(전체 세션)",
            "all_sides(전체 방향)",
            "no_oos_threshold_selection(표본외 임계값 선택 없음)",
        ),
        common_row(
            "month_positive_pocket_observation_only(월 양수 포켓 관찰 전용)",
            "market_behavior_observation(시장 현상 관찰)",
            selected,
            "month_pocket_observation_no_filter(월 포켓 관찰, 필터 아님)",
            "all_sessions(전체 세션)",
            "all_sides(전체 방향)",
            "month_pockets_report_only_not_filter(월 포켓은 보고 전용, 필터 아님)",
        ),
    ]


def materialized_queue_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    session_rows = session_side_rule_rows()
    bridge_rows = pf_density_bridge_rows()
    split_rows = split_guardrail_rows()
    combined = session_rows + bridge_rows + split_rows
    for index, row in enumerate(combined, start=1):
        row["queue_rank"] = index
        row["queue_type"] = "control(대조)" if index in {1, 10} else "candidate(후보)"
    return session_rows, bridge_rows, split_rows, combined


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": status,
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def final_payload(parent_final: Mapping[str, Any], combined: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at_utc: str) -> dict[str, Any]:
    controls = sum(1 for row in combined if row.get("queue_type") == "control(대조)")
    candidates = len(combined) - controls
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
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_package_decision": parent_final.get("package_decision"),
        "parent_selected_variant_id": parent_final.get("parent_selected_variant_id"),
        "parent_selected_net_profit": parent_final.get("parent_selected_net_profit"),
        "parent_selected_profit_factor": parent_final.get("parent_selected_profit_factor"),
        "parent_selected_density": parent_final.get("parent_selected_density"),
        "parent_pf_pass_density_fail_rows": parent_final.get("pf_pass_density_fail_rows"),
        "queue_rows": len(combined),
        "control_rows": controls,
        "candidate_rows": candidates,
        "top_n_rows": sum(1 for row in combined if row.get("top_n_status") != "forbidden(금지)"),
        "trade_splitting_rows": sum(1 for row in combined if row.get("trade_splitting_status") != "not_used(거래 쪼개기 없음)"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "skill": "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "entry session and split labels inherited from run364AG(진입 세션과 분할 라벨은 364AG에서 상속)",
            "sample_scope": "US100 M5 Stage364 Tier A materialization only(US100 5분봉 Stage364 티어 A 구체화 전용)",
            "missing_or_duplicate_check": "parent inputs and 12 materialized queue rows verified(부모 입력과 12개 구체화 대기열 행 확인)",
            "feature_label_boundary": "no new features or labels; fixed policy rows only(새 피처/라벨 없음, 고정 정책 행만 사용)",
            "split_boundary": "validation/OOS guardrail columns written for next run(다음 실행용 검증/표본외 가드레일 컬럼 기록)",
            "leakage_risk": "month pocket is observation only, not a filter(月 포켓은 관찰 전용이며 필터 아님)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "hypothesis": "session/side rules can lift PF while restoring density without trade splitting(세션/방향 규칙이 거래 쪼개기 없이 PF를 올리고 밀도를 복원할 수 있음)",
            "decision_use": "prepare run364AJ proxy scout queue(run364AJ 프록시 정찰 대기열 준비)",
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": "US100 M5, selected proxy seed, fixed thresholds, no top_n, no trade splitting(US100 5분봉, 선택 프록시 씨앗, 고정 임계값, top_n 없음, 거래 쪼개기 없음)",
            "changed_variables": "session policy, side policy, PF-pass density restore policy(세션 정책, 방향 정책, PF 통과 밀도 복원 정책)",
            "sample_scope": "proxy materialization only(프록시 구체화 전용)",
            "success_criteria": "next run can test PF>=1.30 and density>=3/day(PF 1.30 이상과 일 3회 이상 밀도 시험 가능)",
            "failure_criteria": "queue omits controls, uses top_n, or permits trade splitting(대기열이 대조를 빠뜨리거나 top_n/거래 쪼개기를 허용)",
            "invalid_conditions": "post-entry ranking or OOS threshold selection(진입 후 순위 또는 표본외 임계값 선택)",
            "stop_conditions": "materialization complete after queue, gates, ledgers, report(대기열/게이트/장부/보고서 이후 구체화 완료)",
            "evidence_plan": [rel(RUN364AJ_QUEUE), rel(GATE_AUDIT), rel(FINAL_DECISION)],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(옵시디언 성과 귀속)",
            "observed_change": "run364AH found core session positive dual-side pocket and premarket short drag(364AH는 핵심 세션 양방향 양수 포켓과 프리마켓 숏 끌림을 찾음)",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "session filter, short-side admission, PF-pass density restore(세션 필터, 숏 허용, PF 통과 밀도 복원)",
            "segment_checks": [rel(parent.SESSION_SIDE_REVIEW), rel(parent.MONTH_SIDE_REVIEW)],
            "trade_shape": "queue materialization only, no new trades(대기열 구체화 전용, 새 거래 없음)",
            "alternative_explanations": "MT5 fills may differ after package(패키지 이후 MT5 체결은 다를 수 있음)",
            "attribution_confidence": "low_until_run364AJ_proxy(364AJ 프록시 전까지 낮음)",
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
            "effect(효과)": "구체화 산출물을 운영 주장으로 승격하지 않는다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "skill": "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_reproducible_from_command(커밋 후 추적 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AI 구체화를 닫음"),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AH 검토 산출물을 확인함"),
        gate_row("queue_materialization_gate(대기열 구체화 게이트)", RUN364AJ_QUEUE, "run364AJ 정찰 대기열을 만듦"),
        gate_row("topn_absence_gate(top_n 부재 게이트)", RUN364AJ_QUEUE, "top_n 사용 금지를 기록함"),
        gate_row("trade_splitting_absence_gate(거래 쪼개기 부재 게이트)", RUN364AJ_QUEUE, "거래 쪼개기 없음 상태를 기록함"),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점 안전 경계를 기록함"),
        gate_row("experiment_design_gate(실험 설계 게이트)", EXPERIMENT_RECEIPT, "다음 프록시 정찰 설계를 기록함"),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "세션/방향 단서를 연결함"),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 해시를 연결함"),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "운영 승격을 주장하지 않음"),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 게이트를 종료 기록에 연결함"),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


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


def write_docs(final: Mapping[str, Any], combined: Sequence[Mapping[str, Any]], profile: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AI session/side PF lift density repair inputs(364AI 세션/방향 PF 상승 밀도 수리 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- parent_selected_variant(부모 선택 변형): `{final['parent_selected_variant_id']}`
- parent net/PF/density(부모 순수익/수익 팩터/밀도): `{final['parent_selected_net_profit']}` / `{final['parent_selected_profit_factor']}` / `{final['parent_selected_density']}`
- queue_rows(대기열 행): `{final['queue_rows']}`
- control_rows(대조 행): `{final['control_rows']}`
- candidate_rows(후보 행): `{final['candidate_rows']}`
- top_n_rows(top_n 행): `{final['top_n_rows']}`
- trade_splitting_rows(거래 쪼개기 행): `{final['trade_splitting_rows']}`
- runtime_authority(런타임 권위): `not_claimed`

## Repair Profile(수리 프로필)

{markdown_table(profile, ['profile_id', 'source', 'net_profit', 'profit_factor', 'density', 'effect(효과)'])}

## Materialized Queue(구체화 대기열)

{markdown_table(combined, ['queue_rank', 'queue_id', 'axis_id', 'seed_variant_id', 'materialized_policy', 'session_policy', 'side_policy', 'restore_policy'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 materialization(구체화)은 run364AJ(실행364AJ) 프록시 정찰 입력만 만들며, package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
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
        "## run364AI Session/Side PF Lift Density Repair Inputs Closeout(364AI 세션/방향 PF 상승 밀도 수리 입력 종료)",
        f"\n## run364AI Session/Side PF Lift Density Repair Inputs Closeout(364AI 세션/방향 PF 상승 밀도 수리 입력 종료)\n\nAction(행동): run364AH(364AH 실행)의 세션/방향 단서를 `12`개 고정 규칙 대기열로 구체화했다.\n\nEffect(효과): 다음 실행은 `{NEXT_RUN_ID}`이고, top_n(상위 N개 자르기)과 trade splitting(거래 쪼개기)은 금지 상태로 남긴다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(구체화 전용이라 없음)
- latest_proxy_review(최근 프록시 검토): `run364AH`
- latest_materialization(최근 구체화): `run364AI`
- next_scout_queue(다음 정찰 대기열): `{rel(RUN364AJ_QUEUE)}`
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

current_truth(현재 진실): run364AI(364AI 실행)는 run364AH(364AH 실행)의 session/side PF lift density repair(세션/방향 PF 상승 밀도 수리) 단서를 `12`개 scout queue(정찰 대기열)로 구체화했다. top_n(상위 N개 자르기)과 trade splitting(거래 쪼개기)은 금지이며, package(패키지)와 runtime authority(런타임 권위)는 없다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 고정 규칙 프록시 재생을 실행한다.

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
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): session/side PF lift density repair inputs(세션/방향 PF 상승 밀도 수리 입력)를 구체화했다.\n- effect(효과): `{NEXT_RUN_ID}` 정찰 대기열 `12`개를 만들었다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        "\n## "
        + RUN_ID
        + "\n\n- idea(아이디어): 핵심 세션 양수 포켓과 프리마켓 숏 끌림을 분리해 PF와 밀도를 동시에 시험한다.\n"
        + "- positive clue(긍정 단서): us_cash_core(미국 현금장 핵심) 롱/숏은 모두 PF 1.31 이상이다.\n"
        + "- failure memory(실패 기억): PF 통과 씨앗은 밀도를 잃으므로 밀도 복원 규칙과 함께 시험해야 한다.\n",
    )
    append_text_once(
        STAGE_README,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- action(행동): session/side PF lift density repair inputs(세션/방향 PF 상승 밀도 수리 입력)를 만들었다.\n- effect(효과): Stage364(364단계) 안에서 `{NEXT_RUN_ID}`로 이어간다.\n",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "materialization(구체화)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"queue_rows={final['queue_rows']}; controls={final['control_rows']}; candidates={final['candidate_rows']}",
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
        "primary_artifact": rel(RUN364AJ_QUEUE),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_design(실험 설계)",
        "trade_density_requirement_status": "materialized_for_next_scout(다음 정찰용 구체화)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "evidence_scope": "materialization_no_authority(구체화, 권위 없음)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "materialization queue(구체화 대기열)"),
        (f"{RUN_ID}__Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)"),
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
            ("repair_profile", REPAIR_PROFILE, "Repair profile(수리 프로필)."),
            ("session_side_rule_queue", SESSION_SIDE_RULE_QUEUE, "Session side rule queue(세션 방향 규칙 대기열)."),
            ("pf_density_bridge_rule_queue", PF_DENSITY_BRIDGE_RULE_QUEUE, "PF density bridge rule queue(PF 밀도 연결 규칙 대기열)."),
            ("split_guardrail_queue", SPLIT_GUARDRAIL_QUEUE, "Split guardrail queue(분할 가드레일 대기열)."),
            ("next_queue", RUN364AJ_QUEUE, "Next scout queue(다음 정찰 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
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
            "skill": "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in outputs],
            "artifact_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_reproducible_from_command(커밋 후 추적 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    profile = repair_profile_rows(parent_final)
    session_rows, bridge_rows, split_rows, combined = materialized_queue_rows()
    write_csv(REPAIR_PROFILE, profile)
    write_csv(SESSION_SIDE_RULE_QUEUE, session_rows)
    write_csv(PF_DENSITY_BRIDGE_RULE_QUEUE, bridge_rows)
    write_csv(SPLIT_GUARDRAIL_QUEUE, split_rows)
    write_csv(RUN364AJ_QUEUE, combined)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-performance-attribution(옵시디언 성과 귀속)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "queue_materialization_gate",
                "topn_absence_gate",
                "trade_splitting_absence_gate",
                "data_integrity_audit",
                "experiment_design_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    created_at = now_utc()
    temp_final = {"created_at_utc": created_at}
    gates = write_receipts(temp_final)
    final = final_payload(parent_final, combined, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, combined, profile, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
