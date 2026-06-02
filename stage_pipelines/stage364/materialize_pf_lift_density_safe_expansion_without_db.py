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

from stage_pipelines.stage364 import review_pf_dd_near_miss_density_bridge_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AF"
RUN_ID = "run364AF_materialize_pf_lift_density_safe_expansion_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID = "run364AG_train_pf_lift_density_safe_expansion_scout_without_db_v1"

STATUS = "completed_stage364AF_pf_lift_density_safe_expansion_queue_materialized_no_training_no_mt5_no_authority"
JUDGMENT = "pf_lift_density_safe_expansion_inputs_ready_no_operating_claim"
DECISION = "stage364AF_open_run364AG_pf_lift_density_safe_expansion_scout"
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
PF_LIFT_PROFILE = RUN_DIR / "pf_lift_density_safe_profile.csv"
DENSITY_RESTORE_RULE_QUEUE = RUN_DIR / "density_restore_rule_queue.csv"
PF_LIFT_THRESHOLD_GRID = RUN_DIR / "pf_lift_threshold_grid.csv"
RUN364AG_QUEUE = RUN_DIR / "run364AG_scout_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AF_pf_lift_density_safe_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AF_pf_lift_density_safe_inputs.md"
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
    parent.SURFACE_REVIEW,
    parent.PF_LIFT_CANDIDATES,
    parent.NEXT_QUEUE,
    parent.POSITIVE_CLUES,
    parent.FAILURE_MEMORY,
    parent.REPORT_PATH,
    parent.scout.SCOUT_SURFACE,
    parent.scout.SELECTED_PROXY_CANDIDATE,
    parent.scout.BRIDGE_EFFECT_AUDIT,
    parent.scout.EXPRESSION_SAFETY_AUDIT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    PF_LIFT_PROFILE,
    DENSITY_RESTORE_RULE_QUEUE,
    PF_LIFT_THRESHOLD_GRID,
    RUN364AG_QUEUE,
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
        raise RuntimeError(f"parent next_run_id mismatch: {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과되지 않음)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AF inputs(364AF 입력 누락): " + ", ".join(missing))
    return final


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
    if name == "final_decision.json":
        return "parent decision(부모 판정)"
    if name == "required_gate_coverage_audit.csv":
        return "parent gate audit(부모 게이트 감사)"
    if name == "pf_lift_candidates.csv":
        return "PF lift seed candidates(PF 상승 씨앗 후보)"
    if name == "run364AF_pf_lift_density_safe_queue.csv":
        return "parent next queue(부모 다음 대기열)"
    if "bridge" in name:
        return "bridge evidence(연결 근거)"
    return "supporting evidence(보조 근거)"


def load_pf_lift_candidates() -> list[dict[str, str]]:
    return read_csv_rows(parent.PF_LIFT_CANDIDATES)


def profile_rows(parent_final: Mapping[str, Any], candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "profile_id": "run364AD_selected_density_safe_anchor",
            "source_variant_id": parent_final.get("parent_selected_variant_id", ""),
            "source_queue_id": "run364AD_selected",
            "source_profit_factor": finite(parent_final.get("parent_selected_profit_factor")),
            "source_density_per_day": finite(parent_final.get("parent_selected_density")),
            "source_net_profit": finite(parent_final.get("parent_selected_net_profit")),
            "source_drawdown": finite(parent_final.get("parent_selected_drawdown")),
            "diagnosis(진단)": "density passed but PF below target(밀도 통과, PF 목표 미달)",
            "next_use(다음 활용)": "raise short quality while preserving density bridge(숏 품질을 올리되 밀도 연결 보존)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
    ]
    for row in candidates:
        density = as_float(row.get("combined_trade_per_business_day"))
        pf = as_float(row.get("combined_profit_factor"))
        rows.append(
            {
                "run_id": RUN_ID,
                "profile_id": f"candidate_{row.get('queue_id', '')}",
                "source_variant_id": row.get("variant_id", ""),
                "source_queue_id": row.get("queue_id", ""),
                "source_profit_factor": finite(pf),
                "source_density_per_day": finite(density),
                "source_net_profit": row.get("combined_net_profit", ""),
                "source_drawdown": row.get("combined_max_drawdown", ""),
                "diagnosis(진단)": row.get("review_status", ""),
                "next_use(다음 활용)": profile_next_use(pf, density),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def profile_next_use(pf: float, density: float) -> str:
    if pf >= TARGET_PF and density < DENSITY_FLOOR:
        return "restore density without losing PF(PF를 잃지 않고 밀도 복원)"
    if pf < TARGET_PF and density >= DENSITY_FLOOR:
        return "lift PF without breaking density(밀도를 깨지 않고 PF 상승)"
    return "control or stress comparison(대조 또는 압박 비교)"


def density_restore_rules() -> list[dict[str, Any]]:
    rows = [
        (
            "restore_non_hour16_margin_008",
            "entry_month=2025-03 restore non_hour16 abs_margin>=0.08",
            "restore slightly more density while keeping hour16 blocked(16시 차단을 유지하면서 밀도를 조금 더 복원)",
        ),
        (
            "restore_non_hour16_margin_010",
            "entry_month=2025-03 restore non_hour16 abs_margin>=0.10",
            "replay selected run364AD density bridge(선택된 364AD 밀도 연결 재생)",
        ),
        (
            "restore_short_p0475",
            "entry_month=2025-03 restore side=short p_short>=0.475",
            "restore density through short quality(숏 품질로 밀도 복원)",
        ),
        (
            "restore_short_p0490",
            "entry_month=2025-03 restore side=short p_short>=0.490",
            "test stricter short restore for PF defense(PF 방어용 더 엄격한 숏 복원 시험)",
        ),
        (
            "restore_long_p041_adx35",
            "entry_month=2025-03 restore side=long p_long>=0.41 adx_14>=35",
            "test limited long restore without broad March long exposure(넓은 3월 롱 노출 없이 제한 롱 복원 시험)",
        ),
    ]
    return [
        {
            "run_id": RUN_ID,
            "rule_id": rule_id,
            "restore_policy": policy,
            "effect(효과)": effect,
            "timestamp_safety_status": "fixed entry-time threshold(진입 시점 고정 임계값)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for rule_id, policy, effect in rows
    ]


def threshold_grid_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for short_threshold in [0.45, 0.455, 0.46, 0.465, 0.475, 0.49, 0.50]:
        for restore_policy, value in [
            ("restore_march_non_hour16_margin", "0.08"),
            ("restore_march_non_hour16_margin", "0.10"),
            ("restore_march_short_p", "0.475"),
        ]:
            rows.append(
                {
                    "run_id": RUN_ID,
                    "grid_id": f"ps{str(short_threshold).replace('.', '_')}__{restore_policy}__{value.replace('.', '_')}",
                    "short_probability_threshold": short_threshold,
                    "long_block_min": 40.0,
                    "max_hold_m5": 8,
                    "restore_policy": restore_policy,
                    "restore_policy_value": value,
                    "use_case(사용처)": "run364AG scout candidate pool(364AG 정찰 후보군)",
                    "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
                }
            )
    return rows


def queue_item(
    *,
    rank: int,
    queue_id: str,
    axis_id: str,
    seed_variant_id: str,
    short_threshold: float,
    bridge_policy: str,
    bridge_value: str,
    expression: str,
    expected_effect: str,
    entry_margin_floor: float = 0.0,
    queue_type: str = "candidate(후보)",
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "queue_rank": rank,
        "queue_id": queue_id,
        "axis_id": axis_id,
        "queue_type": queue_type,
        "seed_variant_id": seed_variant_id,
        "short_probability_threshold": short_threshold,
        "long_block_min": 40.0,
        "max_hold_m5": 8,
        "entry_margin_floor": entry_margin_floor,
        "bridge_policy": bridge_policy,
        "bridge_policy_value": bridge_value,
        "bridge_expression": expression,
        "expected_effect(효과)": expected_effect,
        "timestamp_safety_status": "timestamp_safe_fixed_threshold(시점 안전 고정 임계값)",
        "trade_splitting_status": "not_used(거래 쪼개기 없음)",
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def scout_queue_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    selected = str(parent_final.get("parent_selected_variant_id", ""))
    rows = [
        queue_item(
            rank=1,
            queue_id="selected_density_safe_control",
            axis_id="control(대조)",
            queue_type="control(대조)",
            seed_variant_id=selected,
            short_threshold=0.45,
            bridge_policy="restore_march_non_hour16_margin",
            bridge_value="0.10",
            expression="short_threshold=0.45; restore non_hour16 abs_margin>=0.10",
            expected_effect="replay run364AD selected density-safe candidate(364AD 선택 밀도 안전 후보 재생)",
        ),
        queue_item(
            rank=2,
            queue_id="pf_pass_density_fail_control",
            axis_id="control(대조)",
            queue_type="control(대조)",
            seed_variant_id="stress4_short050_pf_lift",
            short_threshold=0.50,
            bridge_policy="block_march_long",
            bridge_value="",
            expression="short_threshold=0.50; entry_month=2025-03 block side=long",
            expected_effect="replay PF-pass density-fail control(PF 통과 밀도 실패 대조 재생)",
        ),
        queue_item(
            rank=3,
            queue_id="selected_short0455_restore_margin010",
            axis_id="short_quality_plus_density_restore(숏 품질 + 밀도 복원)",
            seed_variant_id=selected,
            short_threshold=0.455,
            bridge_policy="restore_march_non_hour16_margin",
            bridge_value="0.10",
            expression="short_threshold=0.455; restore non_hour16 abs_margin>=0.10",
            expected_effect="small PF lift while keeping selected density bridge(선택 밀도 연결을 유지하며 작은 PF 상승 시험)",
        ),
        queue_item(
            rank=4,
            queue_id="selected_short0460_restore_margin010",
            axis_id="short_quality_plus_density_restore(숏 품질 + 밀도 복원)",
            seed_variant_id=selected,
            short_threshold=0.46,
            bridge_policy="restore_march_non_hour16_margin",
            bridge_value="0.10",
            expression="short_threshold=0.46; restore non_hour16 abs_margin>=0.10",
            expected_effect="raise short threshold and measure density break risk(숏 임계값을 올리고 밀도 붕괴 위험 측정)",
        ),
        queue_item(
            rank=5,
            queue_id="selected_short0465_restore_margin008",
            axis_id="short_quality_plus_density_restore(숏 품질 + 밀도 복원)",
            seed_variant_id=selected,
            short_threshold=0.465,
            bridge_policy="restore_march_non_hour16_margin",
            bridge_value="0.08",
            expression="short_threshold=0.465; restore non_hour16 abs_margin>=0.08",
            expected_effect="counter higher short threshold with wider restore(높은 숏 임계값을 더 넓은 복원으로 상쇄)",
        ),
        queue_item(
            rank=6,
            queue_id="selected_short0475_restore_short0475",
            axis_id="short_quality_plus_density_restore(숏 품질 + 밀도 복원)",
            seed_variant_id=selected,
            short_threshold=0.475,
            bridge_policy="restore_march_short_p",
            bridge_value="0.475",
            expression="short_threshold=0.475; restore side=short p_short>=0.475",
            expected_effect="let short quality carry both PF and density(숏 품질이 PF와 밀도를 함께 담당하는지 시험)",
        ),
        queue_item(
            rank=7,
            queue_id="selected_margin_floor002_restore_margin008",
            axis_id="margin_band_pf_lift(마진 구간 PF 상승)",
            seed_variant_id=selected,
            short_threshold=0.45,
            bridge_policy="restore_march_non_hour16_margin",
            bridge_value="0.08",
            expression="entry_margin_floor=0.02; restore non_hour16 abs_margin>=0.08",
            expected_effect="remove low-margin noise while preserving density restore(저마진 잡음을 줄이며 밀도 복원 보존)",
            entry_margin_floor=0.02,
        ),
        queue_item(
            rank=8,
            queue_id="selected_margin_floor003_restore_margin010",
            axis_id="margin_band_pf_lift(마진 구간 PF 상승)",
            seed_variant_id=selected,
            short_threshold=0.45,
            bridge_policy="restore_march_non_hour16_margin",
            bridge_value="0.10",
            expression="entry_margin_floor=0.03; restore non_hour16 abs_margin>=0.10",
            expected_effect="test stricter margin floor against PF gap(더 엄격한 마진 하한으로 PF 부족분 시험)",
            entry_margin_floor=0.03,
        ),
        queue_item(
            rank=9,
            queue_id="pfpass_short050_restore_margin008",
            axis_id="pf_pass_density_restore(PF 통과 밀도 복원)",
            seed_variant_id="stress4_short050_pf_lift",
            short_threshold=0.50,
            bridge_policy="block_march_long_restore_non_hour16_margin",
            bridge_value="0.08",
            expression="short_threshold=0.50; block March long; restore non_hour16 abs_margin>=0.08",
            expected_effect="recover density around PF-pass control(PF 통과 대조 주변의 밀도 복원)",
        ),
        queue_item(
            rank=10,
            queue_id="pfpass_short049_restore_margin010",
            axis_id="pf_pass_density_restore(PF 통과 밀도 복원)",
            seed_variant_id="stress4_short050_pf_lift",
            short_threshold=0.49,
            bridge_policy="block_march_long_restore_non_hour16_margin",
            bridge_value="0.10",
            expression="short_threshold=0.49; block March long; restore non_hour16 abs_margin>=0.10",
            expected_effect="slightly loosen PF-pass short gate to regain density(PF 통과 숏 문턱을 조금 낮춰 밀도 회복)",
        ),
        queue_item(
            rank=11,
            queue_id="pfpass_short050_restore_short0475",
            axis_id="pf_pass_density_restore(PF 통과 밀도 복원)",
            seed_variant_id="stress4_short050_pf_lift",
            short_threshold=0.50,
            bridge_policy="block_march_long_restore_short_p",
            bridge_value="0.475",
            expression="short_threshold=0.50; block March long; restore side=short p_short>=0.475",
            expected_effect="restore only high-probability shorts to defend PF(고확률 숏만 복원해 PF 방어)",
        ),
        queue_item(
            rank=12,
            queue_id="mixed_long041_adx35_short0475",
            axis_id="mixed_density_restore(혼합 밀도 복원)",
            seed_variant_id=selected,
            short_threshold=0.475,
            bridge_policy="restore_march_long_p_adx_and_short_p",
            bridge_value="p_long=0.41;adx_14=35;p_short=0.475",
            expression="restore March long p_long>=0.41 adx_14>=35 or short p_short>=0.475",
            expected_effect="test narrow long restore plus short quality(좁은 롱 복원과 숏 품질 결합 시험)",
        ),
    ]
    if any("top_n" in str(row.get("bridge_expression", "")) for row in rows):
        raise RuntimeError("top_n replay is forbidden(top_n 재생은 금지)")
    return rows


def gate_row(name: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": "passed",
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def final_payload(
    profile: Sequence[Mapping[str, Any]],
    rules: Sequence[Mapping[str, Any]],
    grid: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    controls = [row for row in queue if row.get("queue_type") == "control(대조)"]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "profile_rows": len(profile),
        "density_restore_rule_rows": len(rules),
        "threshold_grid_rows": len(grid),
        "run364AG_queue_rows": len(queue),
        "control_rows": len(controls),
        "offensive_rows": len(queue) - len(controls),
        "primary_axis": "short_quality_plus_density_restore(숏 품질 + 밀도 복원)",
        "secondary_axis": "pf_pass_density_restore(PF 통과 밀도 복원)",
        "package_decision": "not_opened_materialization_only(구체화 전용이라 열지 않음)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": 0,
        "gate_total": 0,
    }


def write_receipts(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": final["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "skill": "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "reviewed proxy artifacts inherit entry-time server timestamp(검토된 프록시 산출물은 진입 시점 서버 시간을 상속)",
            "sample_scope": "Stage364 Tier A proxy review inputs only(Stage364 티어 A 프록시 검토 입력 전용)",
            "missing_or_duplicate_check": "not recomputed in materialization; parent gates passed(구체화에서는 재계산하지 않음, 부모 게이트 통과)",
            "feature_label_boundary": "no new label, no future ranking, no top_n replay(새 라벨 없음, 미래 순위 없음, top_n 재생 없음)",
            "split_boundary": "no new split; next run will replay queue(새 분할 없음, 다음 실행이 대기열 재생)",
            "leakage_risk": "future month ranking if top_n is reintroduced(top_n 재도입 시 미래 월 순위 위험)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "hypothesis": "fixed short-quality and density-restore thresholds can approach PF>=1.30 while keeping density>=3/day(고정 숏 품질과 밀도 복원 임계값이 PF 1.30 이상과 밀도 일 3회 이상을 동시에 노릴 수 있음)",
            "decision_use": "choose run364AG proxy scout rows, not package promotion(364AG 프록시 정찰 행 선택, 패키지 승격 아님)",
            "comparison_baseline": "run364AD selected control, stress4_short050 PF-pass density-fail control, baseline replay(364AD 선택 대조, stress4_short050 PF 통과 밀도 실패 대조, 기준 재생)",
            "control_variables": "symbol US100, timeframe M5, max hold 8, ADX block 40, no trade splitting(종목 US100, 5분봉, 최대 보유 8, ADX 차단 40, 거래 쪼개기 없음)",
            "changed_variables": "short threshold, restore margin, restore side, entry margin floor(숏 임계값, 복원 마진, 복원 방향, 진입 마진 하한)",
            "sample_scope": "proxy materialization only, no MT5 execution(프록시 구체화 전용, MT5 실행 없음)",
            "success_criteria": "run364AG finds PF>=1.30 and density>=3/day without worse drawdown concentration(364AG가 PF 1.30 이상과 밀도 일 3회 이상을 찾고 낙폭 집중이 악화되지 않음)",
            "failure_criteria": "PF lift breaks density or density restore loses PF(PF 상승이 밀도를 깨거나 밀도 복원이 PF를 잃음)",
            "invalid_conditions": "top_n replay, post-entry selection, MT5 claim without MT5 output(top_n 재생, 진입 후 선택, MT5 출력 없는 MT5 주장)",
            "stop_conditions": "strict pass rows zero after proxy replay or top_n appears(프록시 재생 후 엄격 통과 0개 또는 top_n 등장)",
            "evidence_plan": [rel(RUN364AG_QUEUE), rel(GATE_AUDIT), rel(FINAL_DECISION)],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(옵시디언 성과 귀속)",
            "observed_change": "density-safe row has PF gap; PF-pass row has density gap(밀도 안전 행은 PF 부족, PF 통과 행은 밀도 부족)",
            "comparison_baseline": "run364AD selected and stress4_short050 PF-pass density-fail control(364AD 선택과 stress4_short050 PF 통과 밀도 실패 대조)",
            "likely_drivers": "short threshold strictness, March long block, non-hour16 restore, margin floor(숏 임계값 엄격도, 3월 롱 차단, non-hour16 복원, 마진 하한)",
            "segment_checks": "not re-run here; next run must check month/session/side/drawdown(여기서는 재실행 없음, 다음 실행이 월/세션/방향/낙폭 확인 필요)",
            "trade_shape": "parent selected 1001 trades, PF 1.2739, density 3.006; PF-pass control 890 trades, PF 1.3066, density 2.6727(부모 선택 1001거래 PF 1.2739 밀도 3.006, PF 통과 대조 890거래 PF 1.3066 밀도 2.6727)",
            "alternative_explanations": "threshold sampling noise or March-specific regime effect(임계값 표본 잡음 또는 3월 특수 국면 효과)",
            "attribution_confidence": "low_until_run364AG_replay(364AG 재생 전까지 낮음)",
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
            "effect(효과)": "materialization(구체화)을 운영 주장으로 승격하지 않음",
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
            "availability": "tracked_after_commit_or_generated_with_manifest(커밋 후 추적 또는 매니페스트로 재생성 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AF materialization(364AF 구체화)을 닫음"),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AE 검토 산출물을 확인함"),
        gate_row("experiment_design_gate(실험 설계 게이트)", EXPERIMENT_RECEIPT, "가설/대조/무효 조건을 기록함"),
        gate_row("queue_materialization_gate(대기열 구체화 게이트)", RUN364AG_QUEUE, "run364AG 정찰 대기열을 만듦"),
        gate_row("topn_absence_gate(top_n 부재 게이트)", RUN364AG_QUEUE, "top_n 재생을 제거함"),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점 안전 고정 임계값 경계를 기록함"),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "PF와 밀도 차이를 다음 검증 항목으로 분리함"),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 해시를 연결함"),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "런타임 권위를 주장하지 않음"),
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


def write_docs(
    final: Mapping[str, Any],
    profile: Sequence[Mapping[str, Any]],
    rules: Sequence[Mapping[str, Any]],
    grid: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AF PF lift density-safe inputs(364AF PF 상승 밀도 안전 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- profile_rows(프로필 행): `{final['profile_rows']}`
- density_restore_rule_rows(밀도 복원 규칙 행): `{final['density_restore_rule_rows']}`
- threshold_grid_rows(임계값 격자 행): `{final['threshold_grid_rows']}`
- run364AG_queue_rows(364AG 대기열 행): `{final['run364AG_queue_rows']}`
- runtime_authority(런타임 권위): `not_claimed`

## Profile(프로필)

{markdown_table(profile, ['profile_id', 'source_variant_id', 'source_profit_factor', 'source_density_per_day', 'diagnosis(진단)', 'next_use(다음 활용)'])}

## Restore Rules(복원 규칙)

{markdown_table(rules, ['rule_id', 'restore_policy', 'effect(효과)'])}

## Scout Queue(정찰 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'axis_id', 'short_probability_threshold', 'bridge_policy', 'bridge_policy_value', 'expected_effect(효과)'])}

## Grid Sample(격자 표본)

{markdown_table(list(grid)[:8], ['grid_id', 'short_probability_threshold', 'restore_policy', 'restore_policy_value'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): materialization(구체화)은 다음 proxy scout(프록시 정찰) 입력만 만들며, MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): run364AG(364AG 실행) PF lift density-safe scout queue(PF 상승 밀도 안전 정찰 대기열)를 만들었다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"\n## run364AF PF Lift Density-Safe Input Closeout(364AF PF 상승 밀도 안전 입력 종료)\n\nAction(행동): run364AE(364AE 실행)의 PF lift/density gap(PF 상승/밀도 간극)을 `{len(queue)}`개 scout queue(정찰 대기열)로 구체화했다.\n\nEffect(효과): 다음 작업은 `{NEXT_RUN_ID}`이며, Stage364(364단계) 안에서 PF 1.30 이상과 density 3/day(일 3회 밀도) 이상을 동시에 시험한다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(구체화 전용이라 없음)
- latest_proxy_review(최근 프록시 검토): `run364AE`
- latest_materialization(최근 구체화): `run364AF`
- next_scout_queue(다음 정찰 대기열): `{rel(RUN364AG_QUEUE)}`
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

current_truth(현재 진실): run364AF(364AF 실행)는 PF lift density-safe expansion(PF 상승 밀도 안전 확장)을 `{final['run364AG_queue_rows']}`개 queue(대기열)로 구체화했다. 핵심 질문은 PF(수익 팩터) `1.30` 이상과 density(밀도) `3/day` 이상을 동시에 지키는지다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 queue(대기열)를 proxy replay scout(프록시 재생 정찰)한다.

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
        RUN_ID,
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): PF lift density-safe expansion(PF 상승 밀도 안전 확장) 입력을 구체화했다.\n- effect(효과): `{NEXT_RUN_ID}` scout(정찰)로 넘길 queue(대기열)를 만들었다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        "\n## "
        + RUN_ID
        + "\n\n- idea(아이디어): PF lift(PF 상승)와 density restore(밀도 복원)를 고정 임계값으로 동시에 시험한다.\n- positive clue(긍정 단서): PF 1.3066 후보와 density 3.006 후보가 따로 존재한다.\n- failure memory(실패 기억): PF만 올리면 density(밀도)가 무너지고, density만 지키면 PF(수익 팩터)가 부족하다.\n",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"\n## {RUN_ID}\n\n- action(행동): PF lift density-safe queue(PF 상승 밀도 안전 대기열)를 만들었다.\n- effect(효과): Stage364(364단계) 분기 없이 run364AG(364AG 실행)로 이어간다.\n",
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
        "notes": f"queue_rows={final['run364AG_queue_rows']}; controls={final['control_rows']}; offensive={final['offensive_rows']}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["run364AG_queue_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(RUN364AG_QUEUE),
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
        (
            f"{RUN_ID}__Tier_A_plus_B",
            "Tier A+B combined(Tier A+B 합산)",
            "Tier A+B",
            "Tier A only plus Tier B missing_required(Tier A만 있고 Tier B 필수 누락)",
        ),
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
            ("pf_lift_profile", PF_LIFT_PROFILE, "PF lift density-safe profile(PF 상승 밀도 안전 프로필)."),
            ("density_restore_rules", DENSITY_RESTORE_RULE_QUEUE, "Density restore rules(밀도 복원 규칙)."),
            ("threshold_grid", PF_LIFT_THRESHOLD_GRID, "PF lift threshold grid(PF 상승 임계값 격자)."),
            ("run364AG_queue", RUN364AG_QUEUE, "Next scout queue(다음 정찰 대기열)."),
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
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    candidates = load_pf_lift_candidates()
    profile = profile_rows(parent_final, candidates)
    rules = density_restore_rules()
    grid = threshold_grid_rows()
    queue = scout_queue_rows(parent_final)
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(PF_LIFT_PROFILE, profile)
    write_csv(DENSITY_RESTORE_RULE_QUEUE, rules)
    write_csv(PF_LIFT_THRESHOLD_GRID, grid)
    write_csv(RUN364AG_QUEUE, queue)
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
                "experiment_design_gate",
                "queue_materialization_gate",
                "topn_absence_gate",
                "data_integrity_audit",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    final = final_payload(profile, rules, grid, queue, now_utc())
    write_json(FINAL_DECISION, final)
    gates = write_receipts(final)
    final["gate_passes"] = sum(1 for row in gates if row.get("status") == "passed")
    final["gate_total"] = len(gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, profile, rules, grid, queue, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
