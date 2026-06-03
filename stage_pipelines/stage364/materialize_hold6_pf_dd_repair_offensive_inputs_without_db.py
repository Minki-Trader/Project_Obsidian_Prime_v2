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

from stage_pipelines.stage364 import review_pf_pass_density_restore_offensive_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AO"
RUN_ID = "run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.PARENT_RUN_ID
NEXT_RUN_ID = "run364AP_train_hold6_pf_dd_repair_offensive_scout_without_db_v1"

STATUS = "completed_stage364AO_hold6_pf_dd_repair_inputs_materialized_no_training_no_mt5_no_authority"
JUDGMENT = "hold6_pf_dd_repair_inputs_ready_with_loss_guard_as_diagnostic_no_authority"
DECISION = "stage364AO_open_run364AP_hold6_pf_dd_repair_offensive_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_PF = parent.TARGET_PF
REFERENCE_DD = -142.323

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
REPAIR_AXIS_MAP = RUN_DIR / "repair_axis_map.csv"
SEED_PAIR_MATRIX = RUN_DIR / "seed_pair_matrix.csv"
DD_GUARDRAIL_DESIGN = RUN_DIR / "dd_guardrail_design.csv"
RUN364AP_QUEUE = RUN_DIR / "run364AP_scout_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AO_hold6_pf_dd_repair_offensive_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AO_hold6_pf_dd_repair_offensive_inputs.md"
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
    parent.POLICY_FAILURE_ATTRIBUTION,
    parent.SESSION_SIDE_REVIEW,
    parent.MONTH_SIDE_REVIEW,
    parent.POSITIVE_CLUES,
    parent.FAILURE_MEMORY,
    parent.REPORT_PATH,
    parent.scout.SCOUT_SURFACE,
    parent.scout.QUEUE_REPLAY_AUDIT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    REPAIR_AXIS_MAP,
    SEED_PAIR_MATRIX,
    DD_GUARDRAIL_DESIGN,
    RUN364AP_QUEUE,
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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def slug(text: str, limit: int = 96) -> str:
    out = "".join(ch if ch.isalnum() else "_" for ch in text)
    return "_".join(part for part in out.split("_") if part)[:limit]


def validate_inputs() -> Mapping[str, Any]:
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 gate, 게이트가 모두 통과하지 않음)")
    queue = read_csv_rows(parent.NEXT_QUEUE)
    if len(queue) != 7:
        raise RuntimeError(f"unexpected run364AO queue rows(364AO 대기열 행 수 이상): {len(queue)}")
    for row in queue:
        forbidden = row.get("forbidden", "") or row.get("forbidden(금지)", "")
        if "top_n forbidden" not in forbidden or "trade_splitting forbidden" not in forbidden:
            raise RuntimeError("queue guardrail missing(top_n 또는 거래 쪼개기 금지 누락)")
        if row.get("timestamp_boundary") != "entry_time_known_only(진입 시점에 알려진 값만 사용)":
            raise RuntimeError("timestamp boundary mismatch(시점 경계 불일치)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AO inputs(364AO 입력 누락): " + ", ".join(missing))
    return parent_final


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "run364AO_materialization_queue.csv":
        return "parent materialization queue(부모 구체화 대기열)"
    if name == "surface_review.csv":
        return "reviewed proxy surface(검토된 프록시 표면)"
    if name == "selected_month_side_review.csv":
        return "loss cluster review input(손실 클러스터 검토 입력)"
    if name == "pf_pass_density_restore_proxy_scout_surface.csv":
        return "parameter source surface(파라미터 원천 표면)"
    if "receipt" in name or name.endswith(".json"):
        return "decision or receipt(결정 또는 영수증)"
    return "supporting evidence(보조 근거)"


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "role": input_role(path),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def by_variant(path: Path) -> dict[str, dict[str, str]]:
    return {row.get("variant_id", ""): dict(row) for row in read_csv_rows(path) if row.get("variant_id")}


def queue_type_label(raw: str) -> str:
    if raw == "control":
        return "control(대조)"
    if raw == "guardrail":
        return "guardrail(가드레일)"
    return "candidate(후보)"


def base_params(seed_id: str, params_by_variant: Mapping[str, Mapping[str, str]]) -> dict[str, Any]:
    source = dict(params_by_variant.get(seed_id, {}))
    return {
        "short_probability_threshold": source.get("short_probability_threshold", "0.45"),
        "long_threshold": source.get("long_threshold", "0.0"),
        "min_margin": source.get("min_margin", "-0.000562137088"),
        "entry_margin_floor": source.get("entry_margin_floor", "0.0"),
        "long_block_feature": source.get("long_block_feature", "adx_14"),
        "long_block_min": source.get("long_block_min", "40.0"),
        "max_hold_m5": source.get("max_hold_m5", "8"),
        "bridge_policy": source.get("bridge_policy", ""),
        "bridge_policy_value": source.get("bridge_policy_value", ""),
        "density_restore_budget": source.get("density_restore_budget", "0.0"),
    }


def plan_specs(raw: Mapping[str, str], seed: Mapping[str, Any]) -> list[dict[str, Any]]:
    queue_id = raw.get("queue_id", "")
    specs: list[dict[str, Any]] = []
    if queue_id == "hold6_density_anchor_control":
        specs.append(
            {
                "queue_id": "hold6_density_anchor_control(6봉 밀도 기준 대조)",
                "axis_id": "hold6_density_anchor(6봉 밀도 기준)",
                "queue_type": "control(대조)",
                "short_probability_threshold": seed["short_probability_threshold"],
                "entry_margin_floor": "0.0",
                "max_hold_m5": "6",
                "bridge_policy": seed["bridge_policy"] or "restore_march_non_hour16_margin",
                "bridge_policy_value": seed["bridge_policy_value"] or "0.10",
                "density_restore_budget": "0.0",
                "session_policy": "all_sessions(전체 세션)",
                "side_policy": "all_sides(전체 방향)",
                "restore_policy": "replay_hold6_density_anchor(6봉 밀도 기준 재생)",
                "repair_axis": "control_density_hold6(밀도 대조 6봉)",
                "target_repair": "preserve density>=3 while measuring PF/DD(PF/DD 측정 중 밀도 3 이상 보존)",
                "implementation_note": "existing_bridge_policy(기존 연결 정책)",
                "implementation_required": "no",
            }
        )
    elif queue_id == "sparse_pf_pass_anchor_control":
        specs.append(
            {
                "queue_id": "sparse_pf_pass_anchor_control(희소 PF 통과 대조)",
                "axis_id": "sparse_pf_anchor(희소 PF 기준)",
                "queue_type": "control(대조)",
                "short_probability_threshold": seed["short_probability_threshold"],
                "entry_margin_floor": "0.0",
                "max_hold_m5": seed["max_hold_m5"],
                "bridge_policy": seed["bridge_policy"] or "block_march_long_restore_core_short_budget",
                "bridge_policy_value": seed["bridge_policy_value"] or "0.10",
                "density_restore_budget": seed["density_restore_budget"] or "0.10",
                "session_policy": "pfpass_base_plus_core_short_budget(PF 통과 기준 + 핵심 숏 예산)",
                "side_policy": "long_seed_short_core_budget(롱 씨앗 + 핵심 숏 예산)",
                "restore_policy": "replay_sparse_pf_anchor(희소 PF 기준 재생)",
                "repair_axis": "control_sparse_pf(희소 PF 대조)",
                "target_repair": "preserve PF>=1.30 while measuring density gap(PF 1.30 이상 보존 중 밀도 간극 측정)",
                "implementation_note": "existing_bridge_policy(기존 연결 정책)",
                "implementation_required": "no",
            }
        )
    elif queue_id == "threshold_edge_hold6_density_repair":
        specs.append(
            {
                "queue_id": "threshold_edge_hold6_density_repair(임계값 경계 6봉 밀도 수리)",
                "axis_id": "threshold_edge_hold6(임계값 경계 6봉)",
                "queue_type": "candidate(후보)",
                "short_probability_threshold": seed["short_probability_threshold"] or "0.455",
                "entry_margin_floor": "0.0",
                "max_hold_m5": "6",
                "bridge_policy": seed["bridge_policy"] or "restore_march_non_hour16_margin",
                "bridge_policy_value": seed["bridge_policy_value"] or "0.10",
                "density_restore_budget": "0.0",
                "session_policy": "all_sessions_except_premarket_short(프리마켓 숏 제외 전체)",
                "side_policy": "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)",
                "restore_policy": "combine_short0455_edge_with_hold6(숏 0.455 경계와 6봉 결합)",
                "repair_axis": "threshold_edge_plus_hold6(임계값 경계 + 6봉)",
                "target_repair": "recover density while keeping DD improvement(낙폭 개선을 유지하며 밀도 회복)",
                "implementation_note": "existing_bridge_policy_hold_changed(기존 연결 정책, 보유 변경)",
                "implementation_required": "no",
            }
        )
    elif queue_id == "late_long_hold6_pf_patch":
        specs.append(
            {
                "queue_id": "late_long_hold6_pf_patch(후반 롱 6봉 PF 패치)",
                "axis_id": "late_long_hold6_patch(후반 롱 6봉 패치)",
                "queue_type": "candidate(후보)",
                "short_probability_threshold": seed["short_probability_threshold"],
                "entry_margin_floor": "0.0",
                "max_hold_m5": "6",
                "bridge_policy": "block_march_long_restore_late_long",
                "bridge_policy_value": "0.16",
                "density_restore_budget": "0.16",
                "session_policy": "pfpass_base_plus_post_cash_late_long(PF 통과 기준 + 현금장 후반 롱)",
                "side_policy": "long_late_patch_short_seed(후반 롱 패치 + 숏 씨앗)",
                "restore_policy": "late_long_patch_with_hold6(후반 롱 패치와 6봉 결합)",
                "repair_axis": "late_long_hold6_pf_patch(후반 롱 6봉 PF 패치)",
                "target_repair": "add density without PF collapse(PF 붕괴 없이 밀도 추가)",
                "implementation_note": "existing_bridge_policy_hold_changed(기존 연결 정책, 보유 변경)",
                "implementation_required": "no",
            }
        )
    elif queue_id == "soft_margin_floor_micro_sweep":
        for floor in ["0.003", "0.006"]:
            specs.append(
                {
                    "queue_id": f"soft_margin_floor_{floor.replace('.', '_')}(소프트 마진 하한 {floor})",
                    "axis_id": "soft_margin_floor_micro_sweep(소프트 마진 하한 미세 탐색)",
                    "queue_type": "candidate(후보)",
                    "short_probability_threshold": seed["short_probability_threshold"],
                    "entry_margin_floor": floor,
                    "max_hold_m5": "6",
                    "bridge_policy": seed["bridge_policy"] or "restore_march_non_hour16_margin",
                    "bridge_policy_value": seed["bridge_policy_value"] or "0.10",
                    "density_restore_budget": "0.0",
                    "session_policy": "all_sessions(전체 세션)",
                    "side_policy": "all_sides(전체 방향)",
                    "restore_policy": "remove_worst_low_margin_hold6(최악 저마진 6봉 거래 제거)",
                    "repair_axis": "pf_dd_micro_floor(PF/DD 미세 하한)",
                    "target_repair": "raise PF and reduce DD without overfilter(PF 상승과 낙폭 축소, 과필터 방지)",
                    "implementation_note": "existing_entry_floor_only(기존 진입 하한만 사용)",
                    "implementation_required": "no",
                }
            )
    elif queue_id == "loss_cluster_session_guard":
        specs.append(
            {
                "queue_id": "loss_cluster_session_guard(손실 클러스터 세션 가드)",
                "axis_id": "loss_cluster_diagnostic_guard(손실 클러스터 진단 가드)",
                "queue_type": "candidate(후보)",
                "short_probability_threshold": seed["short_probability_threshold"],
                "entry_margin_floor": "0.0",
                "max_hold_m5": "6",
                "bridge_policy": "hold6_loss_cluster_session_guard",
                "bridge_policy_value": "diagnostic_only_no_month_hard_filter",
                "density_restore_budget": "0.0",
                "session_policy": "diagnostic_session_guard_no_hard_month_filter(진단 세션 가드, 고정 월 필터 없음)",
                "side_policy": "hold6_long_loss_cluster_watch(6봉 롱 손실 클러스터 관찰)",
                "restore_policy": "diagnostic_dd_guard_before_replay(재생 전 낙폭 진단 가드)",
                "repair_axis": "dd_loss_cluster_guard(낙폭 손실 클러스터 가드)",
                "target_repair": "repair DD without top_n or month-only overfit(top_n 또는 월 단독 과적합 없이 낙폭 수리)",
                "implementation_note": "new_policy_required_but_month_filter_forbidden(새 정책 필요, 월 고정 필터 금지)",
                "implementation_required": "yes",
            }
        )
    elif queue_id == "pf_pass_density_bridge_no_split_guard":
        specs.append(
            {
                "queue_id": "pf_pass_density_bridge_no_split_guard(PF 통과 밀도 연결 무분할 가드)",
                "axis_id": "no_split_guardrail(무분할 가드레일)",
                "queue_type": "guardrail(가드레일)",
                "short_probability_threshold": seed["short_probability_threshold"],
                "entry_margin_floor": seed["entry_margin_floor"],
                "max_hold_m5": seed["max_hold_m5"],
                "bridge_policy": seed["bridge_policy"] or "block_march_long_restore_core_short_budget",
                "bridge_policy_value": seed["bridge_policy_value"] or "0.10",
                "density_restore_budget": seed["density_restore_budget"] or "0.10",
                "session_policy": "guardrail_only_same_as_seed(가드레일 전용, 씨앗 동일)",
                "side_policy": "guardrail_only_same_as_seed(가드레일 전용, 씨앗 동일)",
                "restore_policy": "no_trade_split_no_topn_guardrail(거래 쪼개기 없음, top_n 없음)",
                "repair_axis": "honesty_guardrail(정직성 가드레일)",
                "target_repair": "keep next scout honest(다음 정찰을 정직하게 유지)",
                "implementation_note": "existing_bridge_policy_guardrail(기존 연결 정책 가드레일)",
                "implementation_required": "no",
            }
        )
    return specs


def materialized_queue_rows() -> list[dict[str, Any]]:
    queue = read_csv_rows(parent.NEXT_QUEUE)
    review_by_variant = by_variant(parent.SURFACE_REVIEW)
    params_by_variant = by_variant(parent.scout.SCOUT_SURFACE)
    rows: list[dict[str, Any]] = []
    sequence = 1
    for raw in sorted(queue, key=lambda item: as_float(item.get("queue_rank"), 999.0)):
        seed_id = raw.get("source_variant_id", "")
        review = review_by_variant.get(seed_id, {})
        seed = base_params(seed_id, params_by_variant)
        for spec in plan_specs(raw, seed):
            variant_id = (
                f"{slug(spec['queue_id'])}"
                f"__source_{slug(seed_id, 70)}"
                f"__ps{str(spec['short_probability_threshold']).replace('.', '_')}"
                f"__floor{str(spec['entry_margin_floor']).replace('.', '_')}"
                f"__hold{spec['max_hold_m5']}"
            )
            density_gap = max(0.0, DENSITY_FLOOR - as_float(review.get("combined_trade_per_business_day")))
            pf_gap = max(0.0, TARGET_PF - as_float(review.get("combined_profit_factor")))
            dd_gap = min(0.0, as_float(review.get("combined_max_drawdown")) - REFERENCE_DD)
            rows.append(
                {
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "queue_rank": sequence,
                    "source_queue_rank": raw.get("queue_rank", ""),
                    "source_queue_id": raw.get("queue_id", ""),
                    "queue_id": spec["queue_id"],
                    "axis_id": spec["axis_id"],
                    "queue_type": spec["queue_type"],
                    "source_variant_id": seed_id,
                    "seed_variant_id": seed_id,
                    "variant_id": variant_id,
                    "short_probability_threshold": spec["short_probability_threshold"],
                    "long_threshold": seed["long_threshold"],
                    "min_margin": seed["min_margin"],
                    "entry_margin_floor": spec["entry_margin_floor"],
                    "long_block_feature": seed["long_block_feature"],
                    "long_block_min": seed["long_block_min"],
                    "max_hold_m5": spec["max_hold_m5"],
                    "bridge_policy": spec["bridge_policy"],
                    "bridge_policy_value": spec["bridge_policy_value"],
                    "density_restore_budget": spec["density_restore_budget"],
                    "materialized_policy": spec["repair_axis"],
                    "session_policy": spec["session_policy"],
                    "side_policy": spec["side_policy"],
                    "restore_policy": spec["restore_policy"],
                    "target_repair": spec["target_repair"],
                    "implementation_note": spec["implementation_note"],
                    "implementation_required": spec["implementation_required"],
                    "seed_net_profit": review.get("combined_net_profit", ""),
                    "seed_profit_factor": review.get("combined_profit_factor", ""),
                    "seed_trade_count": review.get("combined_trade_count", ""),
                    "seed_trade_per_business_day": review.get("combined_trade_per_business_day", ""),
                    "seed_expectancy": review.get("combined_expectancy", ""),
                    "seed_max_drawdown": review.get("combined_max_drawdown", ""),
                    "seed_recovery_factor": review.get("combined_recovery_factor", ""),
                    "seed_long_count": review.get("combined_long_count", ""),
                    "seed_short_count": review.get("combined_short_count", ""),
                    "pf_gap_to_1_30": finite(pf_gap, 10),
                    "density_gap_to_3day": finite(density_gap, 10),
                    "dd_gap_vs_reference": finite(dd_gap, 10),
                    "trade_splitting_status": "not_used(거래 쪼개기 없음)",
                    "top_n_status": "forbidden(금지)",
                    "oos_threshold_selection_status": "forbidden(금지)",
                    "timestamp_boundary": "entry_time_known_only(진입 시점에 알려진 값만 사용)",
                    "forbidden": raw.get("forbidden", ""),
                    "expected_effect": raw.get("expected_effect", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            sequence += 1
    return rows


def repair_axis_rows(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row["queue_id"],
                "axis_id": row["axis_id"],
                "queue_type": row["queue_type"],
                "source_queue_id": row["source_queue_id"],
                "seed_profit_factor": row["seed_profit_factor"],
                "seed_density": row["seed_trade_per_business_day"],
                "seed_drawdown": row["seed_max_drawdown"],
                "pf_gap_to_1_30": row["pf_gap_to_1_30"],
                "density_gap_to_3day": row["density_gap_to_3day"],
                "dd_gap_vs_reference": row["dd_gap_vs_reference"],
                "repair_axis": row["materialized_policy"],
                "target_repair": row["target_repair"],
                "effect": "run364AP replay(364AP 재생)에서 PF/DD/density(수익 팩터/낙폭/밀도) 변화 원인을 축별로 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def seed_pair_rows(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    hold6 = next((row for row in queue_rows if row["source_queue_id"] == "hold6_density_anchor_control"), {})
    sparse = next((row for row in queue_rows if row["source_queue_id"] == "sparse_pf_pass_anchor_control"), {})
    pairs = [
        ("hold6_density_anchor", hold6, "density source(밀도 원천)"),
        ("sparse_pf_pass_anchor", sparse, "PF source(PF 원천)"),
    ]
    rows = []
    for pair_id, row, role in pairs:
        rows.append(
            {
                "run_id": RUN_ID,
                "pair_id": pair_id,
                "role": role,
                "source_variant_id": row.get("source_variant_id", ""),
                "queue_id": row.get("queue_id", ""),
                "net_profit": row.get("seed_net_profit", ""),
                "profit_factor": row.get("seed_profit_factor", ""),
                "density": row.get("seed_trade_per_business_day", ""),
                "drawdown": row.get("seed_max_drawdown", ""),
                "long_count": row.get("seed_long_count", ""),
                "short_count": row.get("seed_short_count", ""),
                "effect": "두 씨앗을 섞되 package(패키지)나 runtime authority(런타임 권위)는 주장하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def dd_guardrail_rows() -> list[dict[str, Any]]:
    month_rows = read_csv_rows(parent.MONTH_SIDE_REVIEW)
    loss_rows = [
        row
        for row in month_rows
        if str(row.get("review_status", "")).startswith("loss_or_pf_drag") and as_float(row.get("segment_net_profit")) < 0
    ]
    loss_rows.sort(key=lambda row: as_float(row.get("segment_net_profit")))
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(loss_rows[:5], start=1):
        rows.append(
            {
                "run_id": RUN_ID,
                "guardrail_rank": index,
                "observed_scope": f"{row.get('entry_month')} {row.get('side')}",
                "segment_trade_count": row.get("segment_trade_count", ""),
                "segment_net_profit": row.get("segment_net_profit", ""),
                "segment_profit_factor": row.get("segment_profit_factor", ""),
                "segment_max_drawdown": row.get("segment_max_drawdown", ""),
                "allowed_use": "diagnostic_only_no_month_hard_filter(진단 전용, 월 고정 필터 금지)",
                "forbidden": "top_n, trade_splitting, hard month-only filtering(top_n, 거래 쪼개기, 월 단독 고정 필터)",
                "effect": "손실 클러스터를 보되 과거 월만 자르는 과적합 수리를 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate": name,
        "status": status,
        "evidence": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
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
                "topn_absence_gate",
                "trade_splitting_absence_gate",
                "timestamp_boundary_gate",
                "dd_guardrail_gate",
                "experiment_design_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
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
            "time_axis": "entry_time_known_only(진입 시점에 알려진 값만 사용)",
            "feature_label_boundary": "no new feature or label; policy queue only(새 피처 또는 라벨 없음, 정책 대기열만 생성)",
            "split_boundary": "validation/oos remain replay targets; no OOS threshold selection(검증/표본외는 재생 대상, 표본외 임계값 선택 없음)",
            "leakage_risk": "loss month observations are diagnostic only(손실 월 관찰은 진단 전용)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-experiment-design(실험 설계)",
            "hypothesis": "hold6 density seed can repair PF/DD when mixed with sparse PF seed(6봉 밀도 씨앗은 희소 PF 씨앗과 섞이면 PF/DD를 수리할 수 있음)",
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": "US100 M5, existing probability tape, no top_n, no trade splitting(US100 5분봉, 기존 확률 테이프, top_n 없음, 거래 쪼개기 없음)",
            "changed_variables": "max_hold, short threshold, margin floor, session/side repair policy(최대 보유, 숏 임계값, 마진 하한, 세션/방향 수리 정책)",
            "success_criteria": "run364AP tests PF>=1.30, density>=3/day, DD no worse than hold6 anchor(364AP가 PF 1.30 이상, 하루 밀도 3 이상, DD가 6봉 기준보다 나쁘지 않음을 시험)",
            "failure_criteria": "PF remains below target, density falls below 3/day, DD worsens, or split profit fails(PF 목표 미달, 밀도 3 미만, 낙폭 악화, 분할 수익 실패)",
            "forbidden": "top_n, trade splitting, OOS threshold selection, hard month-only filtering(top_n, 거래 쪼개기, 표본외 임계값 선택, 월 단독 고정 필터)",
            "evidence_plan": [rel(RUN364AP_QUEUE), rel(REPAIR_AXIS_MAP), rel(DD_GUARDRAIL_DESIGN), rel(GATE_AUDIT)],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "observed_change": "materialization only; no new KPI generated(구체화 전용, 새 KPI 생성 없음)",
            "positive_clues": [rel(parent.POSITIVE_CLUES), rel(SEED_PAIR_MATRIX)],
            "failure_memory": [rel(parent.FAILURE_MEMORY), rel(DD_GUARDRAIL_DESIGN)],
            "likely_drivers_to_test": "hold6 density, sparse PF anchor, threshold edge, soft margin floor, diagnostic DD guard(6봉 밀도, 희소 PF 기준, 임계값 경계, 소프트 마진 하한, 진단 DD 가드)",
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
            "effect": "materialization(구체화)을 운영 주장으로 승격하지 않는다.",
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
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AO materialization(364AO 구체화)을 완료했다."),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AN review(364AN 검토)와 대기열을 확인했다."),
        gate_row("queue_materialization_gate(대기열 구체화 게이트)", RUN364AP_QUEUE, "run364AP scout queue(364AP 정찰 대기열)를 만들었다."),
        gate_row("topn_absence_gate(top_n 부재 게이트)", RUN364AP_QUEUE, "모든 row(행)에 top_n forbidden(금지)을 기록했다."),
        gate_row("trade_splitting_absence_gate(거래 쪼개기 부재 게이트)", RUN364AP_QUEUE, "모든 row(행)에 거래 쪼개기 없음 상태를 기록했다."),
        gate_row("timestamp_boundary_gate(시점 경계 게이트)", DATA_RECEIPT, "진입 시점에 알려진 값만 사용하도록 경계를 기록했다."),
        gate_row("dd_guardrail_gate(낙폭 가드 게이트)", DD_GUARDRAIL_DESIGN, "손실 클러스터를 진단 전용으로 묶었다."),
        gate_row("experiment_design_gate(실험 설계 게이트)", EXPERIMENT_RECEIPT, "가설, 성공/실패 조건, 금지를 기록했다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 hash(해시)를 연결했다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "운영 승격과 런타임 권위를 주장하지 않았다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 gate(게이트)를 종료 기록에 연결했다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def final_payload(
    parent_final: Mapping[str, Any],
    queue_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
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
        "source_queue_rows": parent_final.get("next_queue_rows"),
        "ap_queue_rows": len(queue_rows),
        "control_rows": sum(1 for row in queue_rows if str(row.get("queue_type")).startswith("control")),
        "candidate_rows": sum(1 for row in queue_rows if str(row.get("queue_type")).startswith("candidate")),
        "guardrail_rows": sum(1 for row in queue_rows if str(row.get("queue_type")).startswith("guardrail")),
        "implementation_required_rows": sum(1 for row in queue_rows if row.get("implementation_required") == "yes"),
        "top_n_rows": sum(1 for row in queue_rows if row.get("top_n_status") != "forbidden(금지)"),
        "trade_splitting_rows": sum(1 for row in queue_rows if row.get("trade_splitting_status") != "not_used(거래 쪼개기 없음)"),
        "direct_month_hard_filter_rows": 0,
        "selected_hold6_seed_net_profit": parent_final.get("selected_combined_net_profit"),
        "selected_hold6_seed_profit_factor": parent_final.get("selected_combined_profit_factor"),
        "selected_hold6_seed_density": parent_final.get("selected_combined_trade_per_business_day"),
        "selected_hold6_seed_drawdown": parent_final.get("selected_combined_max_drawdown"),
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


def write_docs(final: Mapping[str, Any], queue_rows: Sequence[Mapping[str, Any]], dd_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AO hold6 PF/DD repair inputs(364AO 6봉 PF/DD 수리 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- AP queue rows(AP 대기열 행): `{final['ap_queue_rows']}`
- control/candidate/guardrail(대조/후보/가드레일): `{final['control_rows']}` / `{final['candidate_rows']}` / `{final['guardrail_rows']}`
- implementation_required_rows(구현 필요 행): `{final['implementation_required_rows']}`
- top_n_rows(top_n 행): `{final['top_n_rows']}`
- trade_splitting_rows(거래 쪼개기 행): `{final['trade_splitting_rows']}`
- runtime_authority(런타임 권위): `not_claimed`

## Queue(대기열)

{markdown_table(queue_rows, ['queue_rank', 'queue_id', 'queue_type', 'seed_profit_factor', 'seed_trade_per_business_day', 'seed_max_drawdown', 'entry_margin_floor', 'max_hold_m5', 'target_repair', 'implementation_required'])}

## DD Guardrail(낙폭 가드)

{markdown_table(dd_rows, ['guardrail_rank', 'observed_scope', 'segment_net_profit', 'segment_profit_factor', 'allowed_use', 'forbidden'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): run364AO(364AO 실행)는 run364AP(364AP 실행) 입력만 만들며, package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- ap_queue_rows(AP 대기열 행): `{final['ap_queue_rows']}`\n- effect(효과): `{NEXT_RUN_ID}` replay(재생) 입력을 만든다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AO Hold6 PF/DD Repair Inputs Closeout",
        f"\n## run364AO Hold6 PF/DD Repair Inputs Closeout(364AO 6봉 PF/DD 수리 입력 종료)\n\nAction(행동): run364AN(364AN 실행) review queue(검토 대기열) 7개를 run364AP(364AP 실행) scout queue(정찰 대기열) 8개로 구체화했다.\n\nEffect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 hold6 density(6봉 밀도)와 sparse PF(희소 수익 팩터) 단서를 이어간다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(구체화 전용이라 없음)
- latest_materialization(최근 구체화): `{RUN_ID}`
- next_scout_queue(다음 정찰 대기열): `{rel(RUN364AP_QUEUE)}`
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

current_truth(현재 진실): run364AO(364AO 실행)는 run364AN(364AN 실행)의 no_package(패키지 없음) 판정을 받아 hold6 density(6봉 밀도)와 sparse PF(희소 수익 팩터)를 run364AP(364AP 실행) replay(재생) 입력 8개로 구체화했다. top_n(상위 N)과 trade_splitting(거래 쪼개기)은 금지 상태다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 PF/DD repair(PF/DD 수리) replay(재생)를 실행한다.

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
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): hold6 PF/DD repair inputs(6봉 PF/DD 수리 입력)를 구체화했다.\n- effect(효과): `{NEXT_RUN_ID}` scout queue(정찰 대기열)를 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): hold6 density(6봉 밀도) 씨앗과 sparse PF(희소 수익 팩터) 씨앗을 PF/DD repair(PF/DD 수리) 축으로 섞는다.\n- effect(효과): PF(수익 팩터) 1.30, density(밀도) 3/day, DD(낙폭) 수리를 동시에 보는 다음 replay(재생) 입력을 만든다.\n",
    )
    append_text_once(
        STAGE_README,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- action(행동): run364AP(364AP 실행) queue(대기열)를 materialize(구체화)했다.\n- effect(효과): Stage364(364단계) 안에서 stage(단계) 분기 없이 다음 공격 탐색으로 이어간다.\n",
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
        "notes": f"ap_queue_rows={final['ap_queue_rows']}; implementation_required={final['implementation_required_rows']}; no_topn_no_split",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["ap_queue_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(RUN364AP_QUEUE),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_design(실험 설계)",
        "trade_density_requirement_status": "materialized_for_density_floor_3day_no_trade_split(하루 밀도 3 하한, 거래 쪼개기 없음 구체화)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "evidence_scope": "materialization_no_authority(구체화, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can hold6 density be repaired toward PF/DD without losing density?(6봉 밀도를 잃지 않고 PF/DD를 수리할 수 있는가?)",
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
            ("repair_axis_map", REPAIR_AXIS_MAP, "Repair axis map(수리 축 지도)."),
            ("seed_pair_matrix", SEED_PAIR_MATRIX, "Hold6 and sparse PF seed pair matrix(6봉과 희소 PF 씨앗 쌍 행렬)."),
            ("dd_guardrail_design", DD_GUARDRAIL_DESIGN, "DD guardrail design(낙폭 가드 설계)."),
            ("next_queue", RUN364AP_QUEUE, "Next scout queue(다음 정찰 대기열)."),
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
    queue_rows = materialized_queue_rows()
    axis_rows = repair_axis_rows(queue_rows)
    pair_rows = seed_pair_rows(queue_rows)
    dd_rows = dd_guardrail_rows()
    write_csv(RUN364AP_QUEUE, queue_rows)
    write_csv(REPAIR_AXIS_MAP, axis_rows)
    write_csv(SEED_PAIR_MATRIX, pair_rows)
    write_csv(DD_GUARDRAIL_DESIGN, dd_rows)
    write_work_packet()
    created_at = now_utc()
    gates = write_receipts({"created_at_utc": created_at})
    final = final_payload(parent_final, queue_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, queue_rows, dd_rows, gates)
    write_ledgers(final, gates)
    parent.repair_run_registry_line_endings(RUN_ID)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
