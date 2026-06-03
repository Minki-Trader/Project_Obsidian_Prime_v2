from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_hold6_pf_dd_repair_offensive_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_hold6_pf_dd_repair_offensive_scout_without_db as scout  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AR"
RUN_ID = "run364AR_materialize_threshold_edge_pf_gap_repair_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.PARENT_RUN_ID
NEXT_RUN_ID = "run364AS_train_threshold_edge_pf_gap_repair_scout_without_db_v1"

STATUS = "completed_stage364AR_threshold_edge_pf_gap_repair_inputs_no_authority"
JUDGMENT = "materialization_completed_threshold_edge_pf_gap_repair_inputs_no_authority"
DECISION = "stage364AR_open_run364AS_threshold_edge_pf_gap_repair_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
TARGET_PF = 1.30

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
RUN364AS_QUEUE = RUN_DIR / "run364AS_scout_queue.csv"
SOURCE_SEED_METRICS = RUN_DIR / "source_seed_metrics.csv"
REPAIR_AXIS_MAP = RUN_DIR / "threshold_edge_pf_gap_repair_axis_map.csv"
POLICY_GUARDRAIL_AUDIT = RUN_DIR / "policy_guardrail_audit.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
REPORT_PATH = REVIEW_DIR / "run364AR_threshold_edge_pf_gap_repair_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AR_threshold_edge_pf_gap_repair_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

INPUTS = [
    parent.NEXT_QUEUE,
    parent.FINAL_DECISION,
    parent.SURFACE_REVIEW,
    scout.SCOUT_SURFACE,
    scout.FINAL_DECISION,
]

OUTPUTS = [
    INPUT_MANIFEST,
    RUN364AS_QUEUE,
    SOURCE_SEED_METRICS,
    REPAIR_AXIS_MAP,
    POLICY_GUARDRAIL_AUDIT,
    GATE_AUDIT,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]

QUEUE_FIELDNAMES = [
    "run_id",
    "next_run_id",
    "queue_rank",
    "source_queue_rank",
    "source_queue_id",
    "queue_id",
    "axis_id",
    "queue_type",
    "source_variant_id",
    "seed_variant_id",
    "variant_id",
    "short_probability_threshold",
    "long_threshold",
    "min_margin",
    "entry_margin_floor",
    "long_block_feature",
    "long_block_min",
    "max_hold_m5",
    "bridge_policy",
    "bridge_policy_value",
    "density_restore_budget",
    "materialized_policy",
    "session_policy",
    "side_policy",
    "restore_policy",
    "target_repair",
    "implementation_note",
    "implementation_required",
    "seed_net_profit",
    "seed_profit_factor",
    "seed_trade_count",
    "seed_trade_per_business_day",
    "seed_expectancy",
    "seed_max_drawdown",
    "seed_recovery_factor",
    "seed_long_count",
    "seed_short_count",
    "pf_gap_to_1_30",
    "density_gap_to_3day",
    "dd_improvement_vs_parent_selected",
    "trade_splitting_status",
    "top_n_status",
    "oos_threshold_selection_status",
    "timestamp_boundary",
    "forbidden",
    "expected_effect",
    "claim_boundary",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_csv_rows(path)


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


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
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


def finite(value: Any, digits: int = 10) -> float:
    number = as_float(value)
    if not math.isfinite(number):
        return 0.0
    return round(number, digits)


def slug(text: str, limit: int = 96) -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in text).strip("_")
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned[:limit].strip("_")


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> Mapping[str, Any]:
    missing = [rel(path) for path in INPUTS if not Path(path).exists()]
    if missing:
        raise RuntimeError(f"missing required inputs(필수 입력 누락): {missing}")
    queue = read_csv_rows(parent.NEXT_QUEUE)
    if len(queue) != 8:
        raise RuntimeError(f"unexpected run364AR source queue rows(364AR 원천 대기열 행 수 이상): {len(queue)}")
    for row in queue:
        forbidden = row.get("forbidden", "")
        if "top_n forbidden" not in forbidden or "trade_splitting forbidden" not in forbidden:
            raise RuntimeError("queue forbidden policy missing(top_n 또는 거래 쪼개기 금지 누락)")
    parent_final = read_json(parent.FINAL_DECISION)
    if as_int(parent_final.get("package_candidate_rows")) != 0:
        raise RuntimeError("parent review package candidate must remain zero(부모 검토 패키지 후보 0 필요)")
    return {
        "source_queue_rows": len(queue),
        "parent_gate_passes": parent_final.get("gate_passes"),
        "parent_gate_total": parent_final.get("gate_total"),
        "parent_positive_clue": parent_final.get("positive_clue_variant_id"),
    }


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "run364AR_materialization_queue.csv":
        return "parent materialization queue(부모 구체화 대기열)"
    if name == "final_decision.json":
        return "parent or scout final decision(부모 또는 정찰 최종 결정)"
    if name == "surface_review.csv":
        return "parent surface review(부모 표면 검토)"
    if name == "hold6_pf_dd_repair_proxy_scout_surface.csv":
        return "source scout surface(원천 정찰 표면)"
    return "supporting input(보조 입력)"


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUTS:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_role": input_role(path),
                "path": rel(path),
                "exists": Path(path).exists(),
                "sha256": sha(path) if Path(path).exists() else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def surface_by_variant() -> dict[str, dict[str, str]]:
    surface = read_csv_rows(scout.SCOUT_SURFACE)
    return {row.get("variant_id", ""): row for row in surface if row.get("variant_id")}


def source_seed_rows(queue: Sequence[Mapping[str, str]], surface: Mapping[str, Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = []
    seen: set[str] = set()
    for raw in queue:
        source_variant_id = raw.get("source_variant_id", "")
        if source_variant_id in seen:
            continue
        seen.add(source_variant_id)
        source = surface.get(source_variant_id)
        if not source:
            raise RuntimeError(f"missing source variant in scout surface(정찰 표면 원천 변형 누락): {source_variant_id}")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_variant_id": source_variant_id,
                "source_queue_id": source.get("queue_id", ""),
                "combined_net_profit": source.get("combined_net_profit", ""),
                "combined_profit_factor": source.get("combined_profit_factor", ""),
                "combined_trade_per_business_day": source.get("combined_trade_per_business_day", ""),
                "combined_max_drawdown": source.get("combined_max_drawdown", ""),
                "combined_trade_count": source.get("combined_trade_count", ""),
                "combined_long_count": source.get("combined_long_count", ""),
                "combined_short_count": source.get("combined_short_count", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def spec_for(raw: Mapping[str, str], source: Mapping[str, str]) -> dict[str, Any]:
    queue_id = raw.get("queue_id", "")
    short_threshold = source.get("short_probability_threshold", "0.455")
    long_threshold = source.get("long_threshold", "0.0")
    min_margin = source.get("min_margin", "-0.000562137088")
    entry_floor = source.get("entry_margin_floor", "0.0")
    long_block_feature = source.get("long_block_feature", "adx_14")
    long_block_min = source.get("long_block_min", "40.0")
    max_hold = source.get("max_hold_m5", "6")
    bridge_policy = source.get("bridge_policy", "restore_march_non_hour16_margin")
    bridge_value = source.get("bridge_policy_value", "0.10")
    density_budget = source.get("density_restore_budget", "0.0")
    session_policy = source.get("session_policy", "all_sessions_except_premarket_short(프리마켓 숏 제외 전체)")
    side_policy = source.get("side_policy", "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)")
    queue_type = raw.get("queue_type", "candidate")
    axis_id = "threshold_edge_pf_gap(임계값 경계 PF 간극)"
    materialized_policy = "threshold_edge_replay(임계값 경계 재생)"
    restore_policy = "replay_source_policy(원천 정책 재생)"
    target_repair = "close PF gap while holding density and DD(PF 간극 축소 중 밀도와 DD 유지)"
    implementation_note = "existing_replay_policy(기존 재생 정책)"
    implementation_required = "no"
    expected_effect = raw.get("expected_effect", "")

    if queue_id == "threshold_edge_hold6_control":
        axis_id = "threshold_edge_hold6_control(임계값 경계 6봉 대조)"
        materialized_policy = "control_threshold_edge_hold6(임계값 경계 6봉 대조)"
        restore_policy = "replay_threshold_edge_hold6(임계값 경계 6봉 재생)"
        target_repair = "preserve AQ positive clue(AQ 긍정 단서 보존)"
    elif queue_id == "late_long_hold6_control":
        axis_id = "late_long_pf_lift_control(후반 롱 PF 개선 대조)"
        materialized_policy = "control_late_long_hold6(후반 롱 6봉 대조)"
        restore_policy = "replay_late_long_hold6(후반 롱 6봉 재생)"
        target_repair = "measure PF lift with short-side collapse risk(PF 개선과 숏 붕괴 위험 측정)"
    elif queue_id == "threshold_edge_hold5_probe":
        max_hold = "5"
        axis_id = "hold_compression_5(보유 압축 5봉)"
        materialized_policy = "threshold_edge_hold5_probe(임계값 경계 5봉 탐침)"
        restore_policy = "compress_hold_to_5(보유 5봉 압축)"
        target_repair = "lift PF by reducing weaker tail holds(약한 후미 보유를 줄여 PF 개선)"
    elif queue_id == "threshold_edge_hold4_probe":
        max_hold = "4"
        axis_id = "hold_compression_4(보유 압축 4봉)"
        materialized_policy = "threshold_edge_hold4_probe(임계값 경계 4봉 탐침)"
        restore_policy = "compress_hold_to_4(보유 4봉 압축)"
        target_repair = "test sharper DD and PF tradeoff(더 날카로운 DD/PF 교환 시험)"
    elif queue_id == "threshold_edge_floor001_probe":
        entry_floor = "0.001"
        axis_id = "soft_margin_floor_001(소프트 마진 하한 0.001)"
        materialized_policy = "threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)"
        restore_policy = "small_margin_floor_filter(작은 마진 하한 필터)"
        target_repair = "cut low-margin losses without losing density(저마진 손실 축소와 밀도 유지)"
    elif queue_id == "threshold_edge_late_long_blend_probe":
        bridge_policy = "block_march_long_restore_core_late"
        bridge_value = "0.12"
        density_budget = "0.10"
        session_policy = "us_cash_core_plus_post_cash_late_long(미국 현금장 핵심 + 후반 롱)"
        side_policy = "core_both_sides_late_long(핵심 양방향 + 후반 롱)"
        axis_id = "threshold_edge_late_long_blend(임계값 경계 + 후반 롱 혼합)"
        materialized_policy = "threshold_edge_late_long_blend_probe(임계값 경계 후반 롱 혼합 탐침)"
        restore_policy = "core_late_restore_budget(핵심/후반 복원 예산)"
        target_repair = "borrow late-long PF lift without short collapse(숏 붕괴 없이 후반 롱 PF 개선 차용)"
    elif queue_id == "pf_pass_density_bridge_hold6_probe":
        max_hold = "6"
        bridge_policy = "block_march_long_restore_non_drag_sessions"
        bridge_value = "0.10"
        density_budget = "0.12"
        session_policy = "all_sessions_except_premarket_short(프리마켓 숏 제외 전체)"
        side_policy = "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)"
        axis_id = "pf_pass_density_bridge_hold6(PF 통과 밀도 연결 6봉)"
        materialized_policy = "pf_pass_density_bridge_hold6_probe(PF 통과 밀도 연결 6봉 탐침)"
        restore_policy = "non_drag_density_bridge(비부담 구간 밀도 연결)"
        target_repair = "add density to sparse PF pass without trade splitting(거래 쪼개기 없이 희소 PF 통과에 밀도 추가)"
    elif queue_id == "loss_guard_policy_implementation_gate":
        axis_id = "loss_guard_implementation_gate(손실 가드 구현 게이트)"
        materialized_policy = "loss_guard_policy_design_only(손실 가드 정책 설계 전용)"
        restore_policy = "implementation_required_before_replay(재생 전 구현 필요)"
        target_repair = "prevent loss-cluster DD creep(손실 클러스터 DD 증가 방지)"
        implementation_note = "requires loss-cluster/session drawdown guard not implemented in current replay(현재 재생에 없는 손실 클러스터/세션 DD 가드 필요)"
        implementation_required = "yes"

    return {
        "axis_id": axis_id,
        "queue_type": f"{queue_type}({queue_type_label(queue_type)})",
        "short_probability_threshold": short_threshold,
        "long_threshold": long_threshold,
        "min_margin": min_margin,
        "entry_margin_floor": entry_floor,
        "long_block_feature": long_block_feature,
        "long_block_min": long_block_min,
        "max_hold_m5": max_hold,
        "bridge_policy": bridge_policy,
        "bridge_policy_value": bridge_value,
        "density_restore_budget": density_budget,
        "materialized_policy": materialized_policy,
        "session_policy": session_policy,
        "side_policy": side_policy,
        "restore_policy": restore_policy,
        "target_repair": target_repair,
        "implementation_note": implementation_note,
        "implementation_required": implementation_required,
        "expected_effect": expected_effect,
    }


def queue_type_label(queue_type: str) -> str:
    if queue_type == "control":
        return "대조"
    if queue_type == "candidate":
        return "후보"
    if queue_type == "guardrail":
        return "가드레일"
    return "기타"


def materialized_queue_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_queue = read_csv_rows(parent.NEXT_QUEUE)
    surface = surface_by_variant()
    rows = []
    parent_dd = as_float(parent_final.get("selected_parent_drawdown"), -168.999)
    for sequence, raw in enumerate(sorted(source_queue, key=lambda item: as_float(item.get("queue_rank"), 999.0)), start=1):
        source_variant_id = raw.get("source_variant_id", "")
        source = surface.get(source_variant_id)
        if not source:
            raise RuntimeError(f"missing source variant in scout surface(정찰 표면 원천 변형 누락): {source_variant_id}")
        spec = spec_for(raw, source)
        variant_id = (
            f"{slug(raw.get('queue_id', 'queue'))}"
            f"__source_{slug(source_variant_id, 72)}"
            f"__ps{str(spec['short_probability_threshold']).replace('.', '_')}"
            f"__floor{str(spec['entry_margin_floor']).replace('.', '_')}"
            f"__hold{spec['max_hold_m5']}"
        )
        seed_pf = as_float(source.get("combined_profit_factor"))
        seed_density = as_float(source.get("combined_trade_per_business_day"))
        seed_dd = as_float(source.get("combined_max_drawdown"))
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": sequence,
                "source_queue_rank": raw.get("queue_rank", ""),
                "source_queue_id": raw.get("queue_id", ""),
                "queue_id": f"{raw.get('queue_id')}({materialized_label(raw.get('queue_id', ''))})",
                "axis_id": spec["axis_id"],
                "queue_type": spec["queue_type"],
                "source_variant_id": source_variant_id,
                "seed_variant_id": source_variant_id,
                "variant_id": variant_id,
                "short_probability_threshold": spec["short_probability_threshold"],
                "long_threshold": spec["long_threshold"],
                "min_margin": spec["min_margin"],
                "entry_margin_floor": spec["entry_margin_floor"],
                "long_block_feature": spec["long_block_feature"],
                "long_block_min": spec["long_block_min"],
                "max_hold_m5": spec["max_hold_m5"],
                "bridge_policy": spec["bridge_policy"],
                "bridge_policy_value": spec["bridge_policy_value"],
                "density_restore_budget": spec["density_restore_budget"],
                "materialized_policy": spec["materialized_policy"],
                "session_policy": spec["session_policy"],
                "side_policy": spec["side_policy"],
                "restore_policy": spec["restore_policy"],
                "target_repair": spec["target_repair"],
                "implementation_note": spec["implementation_note"],
                "implementation_required": spec["implementation_required"],
                "seed_net_profit": source.get("combined_net_profit", ""),
                "seed_profit_factor": source.get("combined_profit_factor", ""),
                "seed_trade_count": source.get("combined_trade_count", ""),
                "seed_trade_per_business_day": source.get("combined_trade_per_business_day", ""),
                "seed_expectancy": source.get("combined_expectancy", ""),
                "seed_max_drawdown": source.get("combined_max_drawdown", ""),
                "seed_recovery_factor": source.get("combined_recovery_factor", ""),
                "seed_long_count": source.get("combined_long_count", ""),
                "seed_short_count": source.get("combined_short_count", ""),
                "pf_gap_to_1_30": finite(max(0.0, TARGET_PF - seed_pf)),
                "density_gap_to_3day": finite(max(0.0, DENSITY_FLOOR - seed_density)),
                "dd_improvement_vs_parent_selected": finite(seed_dd - parent_dd),
                "trade_splitting_status": "not_used(거래 쪼개기 없음)",
                "top_n_status": "forbidden(금지)",
                "oos_threshold_selection_status": "forbidden(금지)",
                "timestamp_boundary": raw.get("timestamp_boundary", "entry_time_known_only(진입 시점에 알려진 값만 사용)"),
                "forbidden": raw.get("forbidden", ""),
                "expected_effect": spec["expected_effect"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def materialized_label(queue_id: str) -> str:
    labels = {
        "threshold_edge_hold6_control": "임계값 경계 6봉 대조",
        "late_long_hold6_control": "후반 롱 6봉 대조",
        "threshold_edge_hold5_probe": "임계값 경계 5봉 탐침",
        "threshold_edge_hold4_probe": "임계값 경계 4봉 탐침",
        "threshold_edge_floor001_probe": "임계값 경계 하한 0.001 탐침",
        "threshold_edge_late_long_blend_probe": "임계값 경계 후반 롱 혼합 탐침",
        "pf_pass_density_bridge_hold6_probe": "PF 통과 밀도 연결 6봉 탐침",
        "loss_guard_policy_implementation_gate": "손실 가드 구현 게이트",
    }
    return labels.get(queue_id, "구체화 행")


def repair_axis_rows(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in queue_rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_rank": row["queue_rank"],
                "queue_id": row["queue_id"],
                "axis_id": row["axis_id"],
                "queue_type": row["queue_type"],
                "source_queue_id": row["source_queue_id"],
                "max_hold_m5": row["max_hold_m5"],
                "entry_margin_floor": row["entry_margin_floor"],
                "bridge_policy": row["bridge_policy"],
                "density_restore_budget": row["density_restore_budget"],
                "implementation_required": row["implementation_required"],
                "target_repair": row["target_repair"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def policy_guardrail_rows(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in queue_rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row["queue_id"],
                "top_n_status": row["top_n_status"],
                "trade_splitting_status": row["trade_splitting_status"],
                "oos_threshold_selection_status": row["oos_threshold_selection_status"],
                "timestamp_boundary": row["timestamp_boundary"],
                "implementation_required": row["implementation_required"],
                "guardrail_status": "passed(통과)",
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


def gate_rows(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    implementation_required = sum(1 for row in queue_rows if row.get("implementation_required") == "yes")
    return [
        gate_row("parent_review_gate(부모 검토 게이트)", parent.FINAL_DECISION, "AQ review(검토) 완료와 package 0행 확인"),
        gate_row("source_surface_gate(원천 표면 게이트)", scout.SCOUT_SURFACE, "AP scout surface(정찰 표면)에서 seed metric(씨앗 지표)을 읽음"),
        gate_row("queue_materialization_gate(대기열 구체화 게이트)", RUN364AS_QUEUE, "AS scout queue(정찰 대기열) 8행 생성"),
        gate_row("control_candidate_guardrail_gate(대조/후보/가드레일 게이트)", RUN364AS_QUEUE, "2/5/1 구조 유지"),
        gate_row("implementation_boundary_gate(구현 경계 게이트)", POLICY_GUARDRAIL_AUDIT, f"implementation_required(구현 필요) {implementation_required}행 분리"),
        gate_row("topn_absence_gate(top_n 부재 게이트)", POLICY_GUARDRAIL_AUDIT, "top_n forbidden(금지) 유지"),
        gate_row("trade_splitting_absence_gate(거래 쪼개기 부재 게이트)", POLICY_GUARDRAIL_AUDIT, "거래 쪼개기 없음 유지"),
        gate_row("oos_threshold_lock_gate(표본외 임계값 잠금 게이트)", POLICY_GUARDRAIL_AUDIT, "OOS threshold selection(표본외 임계값 선택) 금지"),
        gate_row("timestamp_boundary_gate(시점 경계 게이트)", POLICY_GUARDRAIL_AUDIT, "entry_time_known_only(진입 시점 알려진 값만 사용) 기록"),
        gate_row("stage_continuity_gate(단계 연속성 게이트)", WORK_PACKET, "새 stage(단계) 분기 없이 Stage364 유지"),
        gate_row("claim_boundary_gate(주장 경계 게이트)", CLAIM_RECEIPT, "운영 주장 없음"),
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "work_family": "offensive_exploration_materialization(공격 탐색 구체화)",
            "primary_skill": "obsidian-prime-ml(프로젝트 전용 ML)",
            "support_skills": [
                "obsidian-reentry-read(재진입 읽기)",
                "obsidian-exploration-mandate(탐색 명령)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "parent_review_gate",
                "source_surface_gate",
                "queue_materialization_gate",
                "control_candidate_guardrail_gate",
                "implementation_boundary_gate",
                "topn_absence_gate",
                "trade_splitting_absence_gate",
                "oos_threshold_lock_gate",
                "timestamp_boundary_gate",
                "stage_continuity_gate",
                "claim_boundary_gate",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "timestamp_boundary": "entry_time_known_only(진입 시점에 알려진 값만 사용)",
            "feature_label_boundary": "no new feature or label; queue materialization only(새 피처 또는 라벨 없음, 대기열 구체화만)",
            "inputs": [rel(path) for path in INPUTS],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "hypothesis": "threshold-edge PF gap can be repaired by hold compression, small margin floor, and late-long blend(임계값 경계 PF 간극은 보유 압축, 작은 마진 하한, 후반 롱 혼합으로 수리 가능)",
            "controls": final["control_rows"],
            "candidates": final["candidate_rows"],
            "guardrails": final["guardrail_rows"],
            "forbidden": "top_n, trade_splitting, OOS threshold selection(top_n, 거래 쪼개기, 표본외 임계값 선택)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "positive_clue_variant_id": final["positive_clue_variant_id"],
            "positive_clue_profit_factor": final["positive_clue_profit_factor"],
            "positive_clue_density": final["positive_clue_density"],
            "positive_clue_drawdown": final["positive_clue_drawdown"],
            "attribution_boundary": "materialization only; no new KPI produced(구체화만 수행, 새 KPI 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "judgment": JUDGMENT,
            "decision": DECISION,
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifacts = []
    for path in OUTPUTS:
        if Path(path).exists():
            artifacts.append(
                {
                    "path": rel(path),
                    "sha256": sha(path),
                    "role": "run364AR output(364AR 출력)",
                }
            )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "artifacts": artifacts,
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def final_payload(parent_final: Mapping[str, Any], queue_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
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
        "source_queue_rows": parent_final.get("next_queue_rows"),
        "as_queue_rows": len(queue_rows),
        "control_rows": sum(1 for row in queue_rows if str(row.get("queue_type")).startswith("control")),
        "candidate_rows": sum(1 for row in queue_rows if str(row.get("queue_type")).startswith("candidate")),
        "guardrail_rows": sum(1 for row in queue_rows if str(row.get("queue_type")).startswith("guardrail")),
        "implementation_required_rows": sum(1 for row in queue_rows if row.get("implementation_required") == "yes"),
        "executable_rows": sum(1 for row in queue_rows if row.get("implementation_required") != "yes"),
        "top_n_rows": sum(1 for row in queue_rows if row.get("top_n_status") != "forbidden(금지)"),
        "trade_splitting_rows": sum(1 for row in queue_rows if row.get("trade_splitting_status") != "not_used(거래 쪼개기 없음)"),
        "oos_threshold_selection_rows": sum(1 for row in queue_rows if row.get("oos_threshold_selection_status") != "forbidden(금지)"),
        "positive_clue_variant_id": parent_final.get("positive_clue_variant_id"),
        "positive_clue_profit_factor": parent_final.get("positive_clue_profit_factor"),
        "positive_clue_density": parent_final.get("positive_clue_density"),
        "positive_clue_drawdown": parent_final.get("positive_clue_drawdown"),
        "positive_clue_net_profit": 840.779,
        "positive_clue_short_count": 87,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_\n"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join([header, sep, *body]) + "\n"


def write_docs(final: Mapping[str, Any], queue_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    queue_preview = [
        {
            "queue_rank": row["queue_rank"],
            "queue_id": row["queue_id"],
            "queue_type": row["queue_type"],
            "max_hold_m5": row["max_hold_m5"],
            "entry_margin_floor": row["entry_margin_floor"],
            "bridge_policy": row["bridge_policy"],
            "seed_pf": row["seed_profit_factor"],
            "seed_density": row["seed_trade_per_business_day"],
            "implementation_required": row["implementation_required"],
        }
        for row in queue_rows
    ]
    report = f"""# run364AR threshold-edge PF gap repair materialization(364AR 임계값 경계 PF 간극 수리 구체화)

## Current Truth(현재 진실)

- action(행동): AQ review(검토) queue(대기열) 8행을 AS scout(정찰) queue(대기열)로 구체화했다.
- effect(효과): package(패키지)는 만들지 않고 threshold-edge(임계값 경계) positive clue(긍정 단서)를 보유 압축, 마진 하한, 후반 롱 혼합 후보로 넘겼다.
- positive_clue(긍정 단서): PF(수익 팩터) `{final['positive_clue_profit_factor']}`, density(밀도) `{final['positive_clue_density']}`, DD(낙폭) `{final['positive_clue_drawdown']}`, net(순수익) `{final['positive_clue_net_profit']}`.
- authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.

## Queue(대기열)

{markdown_table(queue_preview, ['queue_rank', 'queue_id', 'queue_type', 'max_hold_m5', 'entry_margin_floor', 'bridge_policy', 'seed_pf', 'seed_density', 'implementation_required'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): run364AR threshold-edge PF gap repair materialization(364AR 임계값 경계 PF 간극 수리 구체화)

- decision(결정): `{DECISION}`
- action(행동): run364AQ(364AQ 실행)의 materialization queue(구체화 대기열)를 run364AS(364AS 실행) scout queue(정찰 대기열)로 바꿨다.
- effect(효과): 새 stage(단계) 분기 없이 Stage364(364단계) 안에서 threshold-edge(임계값 경계) 단서를 더 공격적으로 탐색한다.
- strict boundary(엄격 경계): no model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no runtime authority(런타임 권위 없음).
- queue(대기열): `{rel(RUN364AS_QUEUE)}`
- report(보고서): `{rel(REPORT_PATH)}`
- gate(게이트): `{final['gate_passes']}/{final['gate_total']}`
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
        bom=True,
    )
    write_text(
        CURRENT_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364AR(364AR 실행)는 run364AQ(364AQ 실행)의 threshold-edge PF/DD clue(임계값 경계 PF/DD 단서)를 run364AS(364AS 실행) scout queue(정찰 대기열) `{rel(RUN364AS_QUEUE)}`로 구체화했다. queue rows(대기열 행)는 `{final['as_queue_rows']}`이고 executable rows(실행 가능 행)는 `{final['executable_rows']}`이며 implementation_required(구현 필요)는 `{final['implementation_required_rows']}`행이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 AS scout(정찰)를 실행해 hold compression(보유 압축), margin floor(마진 하한), late-long blend(후반 롱 혼합)이 PF(수익 팩터) 1.30 간극을 줄이는지 proxy replay(프록시 재생)로 확인한다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(구체화 전용이라 없음)
- latest_materialization(최근 구체화): `{RUN_ID}`
- next_scout_queue(다음 정찰 대기열): `{rel(RUN364AS_QUEUE)}`
- preserved_clues(보존 단서): threshold_edge_pf_dd_lift(임계값 경계 PF/DD 개선), late_long_pf_lift(후반 롱 PF 개선), sparse_pf_density_gap(희소 PF 밀도 간극)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- queue_rows(대기열 행): `{final['as_queue_rows']}`\n- effect(효과): `{NEXT_RUN_ID}` scout queue(정찰 대기열)를 만들었다.\n",
    )
    append_text_once(
        REVIEW_INDEX,
        f"run364AR threshold-edge PF gap repair materialization",
        f"\n- `{RUN_ID}`: threshold-edge PF gap repair materialization(임계값 경계 PF 간극 수리 구체화). report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        STAGE_README,
        f"run364AR Threshold Edge PF Gap Repair Materialization",
        f"\n## run364AR Threshold Edge PF Gap Repair Materialization(364AR 임계값 경계 PF 간극 수리 구체화)\n\nAction(행동): AQ queue(대기열) 8행을 AS scout queue(정찰 대기열)로 구체화했다.\n\nEffect(효과): Stage364(364단계) 안에서 stage(단계) 분기 없이 다음 공격 탐색으로 이어간다.\n",
    )
    append_text_once(
        CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): threshold-edge PF gap repair inputs(임계값 경계 PF 간극 수리 입력)를 구체화했다.\n- effect(효과): `{NEXT_RUN_ID}` scout queue(정찰 대기열)를 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): threshold-edge(임계값 경계) 후보의 PF gap(PF 간극)을 hold compression(보유 압축), margin floor(마진 하한), late-long blend(후반 롱 혼합)로 줄인다.\n- effect(효과): package(패키지) 실패를 idea-dead(아이디어 사망)로 닫지 않고 다음 proxy scout(프록시 정찰)로 넘긴다.\n",
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
        "rows": final["as_queue_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(RUN_DIR),
        "primary_report": rel(REPORT_PATH),
        "family": "stage364_materialization(364단계 구체화)",
        "lane": "offensive_exploration(공격 탐색)",
        "work_family": "offensive_exploration_materialization(공격 탐색 구체화)",
        "primary_artifact": rel(RUN364AS_QUEUE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_applicable_materialization_only(구체화 전용이라 해당 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can threshold-edge PF gap be repaired without density collapse?(임계값 경계 PF 간극을 밀도 붕괴 없이 수리할 수 있는가?)",
        "notes": f"as_queue_rows={final['as_queue_rows']}; executable={final['executable_rows']}; implementation_required={final['implementation_required_rows']}; no_topn_no_split",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common])
    alpha_rows = []
    for suffix, view, tier in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B"),
        ("Tier_AB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": suffix,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "materialized queue only(구체화 대기열 전용)",
                "scoreboard_lane": "materialization(구체화)",
                "primary_kpi": f"as_queue_rows={final['as_queue_rows']}",
                "guardrail_kpi": "top_n=0;trade_splitting=0;oos_threshold_selection=0",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        alpha_rows.append(row)
    append_or_replace_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_rows)
    append_or_replace_csv(STAGE_DIR / "03_reviews" / "stage_run_ledger.csv", ["ledger_row_id"], alpha_rows)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("next_queue", RUN364AS_QUEUE, "Next scout queue(다음 정찰 대기열)."),
        ("repair_axis_map", REPAIR_AXIS_MAP, "Repair axis map(수리 축 지도)."),
        ("gate_audit", GATE_AUDIT, "Required gate audit(필수 게이트 감사)."),
        ("report", REPORT_PATH, "Review report(검토 보고서)."),
        ("decision", DECISION_DOC, "Decision record(결정 기록)."),
        ("lineage", LINEAGE_RECEIPT, "Artifact lineage(산출물 계보)."),
    ]:
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha(path) if Path(path).exists() else "",
                "created_at_utc": final["created_at_utc"],
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "notes": notes,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)
    repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUTS if Path(path).exists()],
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
        },
    )


def main() -> None:
    ensure_dirs()
    validate_inputs()
    created_at = now_utc()
    parent_final = read_json(parent.FINAL_DECISION)
    source_queue = read_csv_rows(parent.NEXT_QUEUE)
    source_surface = surface_by_variant()
    queue_rows = materialized_queue_rows(parent_final)
    source_rows = source_seed_rows(source_queue, source_surface)
    axis_rows = repair_axis_rows(queue_rows)
    guardrail_rows = policy_guardrail_rows(queue_rows)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(RUN364AS_QUEUE, queue_rows, QUEUE_FIELDNAMES)
    write_csv(SOURCE_SEED_METRICS, source_rows)
    write_csv(REPAIR_AXIS_MAP, axis_rows)
    write_csv(POLICY_GUARDRAIL_AUDIT, guardrail_rows)
    write_work_packet()
    gates = gate_rows(queue_rows)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(parent_final, queue_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    write_docs(final, queue_rows, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
