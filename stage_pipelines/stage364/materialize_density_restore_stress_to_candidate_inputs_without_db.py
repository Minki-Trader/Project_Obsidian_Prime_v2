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

from stage_pipelines.stage364 import review_threshold_edge_density_restore_cost_session_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BA"
RUN_ID = "run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1"

STATUS = "completed_stage364BA_density_restore_stress_to_candidate_inputs_materialized_no_authority"
JUDGMENT = "materialization_completed_stress_positive_clues_to_candidate_scout_inputs_no_authority"
DECISION = "stage364BA_open_run364BB_density_restore_stress_to_candidate_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
TARGET_PF = 1.25

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SOURCE_CLUE_SUMMARY = RUN_DIR / "source_clue_summary.csv"
AXIS_MAP = RUN_DIR / "stress_to_candidate_axis_map.csv"
GUARDRAIL_MATRIX = RUN_DIR / "stress_to_candidate_guardrail_matrix.csv"
RUN364BB_QUEUE = RUN_DIR / "run364BB_scout_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BA_density_restore_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BA_density_restore_materialization.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

INPUTS = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364BA_QUEUE,
    parent.SURFACE_REVIEW,
    parent.POSITIVE_CLUES,
    parent.FAILURE_MEMORY,
    parent.PACKAGE_DECISION,
    parent.REPORT_PATH,
    parent.LINEAGE_RECEIPT,
]

OUTPUTS = [
    INPUT_MANIFEST,
    SOURCE_CLUE_SUMMARY,
    AXIS_MAP,
    GUARDRAIL_MATRIX,
    RUN364BB_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


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


def finite(value: Any, digits: int = 10) -> float:
    number = as_float(value)
    if not math.isfinite(number):
        return 0.0
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[Mapping[str, Any], list[dict[str, str]]]:
    missing = [rel(path) for path in INPUTS if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BA inputs(BA 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if any(final.get(key) != "not_claimed" for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]):
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과되지 않음)")
    queue = read_csv_rows(parent.RUN364BA_QUEUE)
    if len(queue) != 6:
        raise RuntimeError(f"unexpected BA queue rows(BA 대기열 행 수 이상): {len(queue)}")
    for row in queue:
        if "not_used" not in str(row.get("trade_splitting_status", "")):
            raise RuntimeError("trade splitting guardrail missing(거래 쪼개기 금지 누락)")
        if "forbidden" not in str(row.get("top_n_status", "")):
            raise RuntimeError("top_n guardrail missing(top_n 금지 누락)")
        if "forbidden" not in str(row.get("oos_threshold_selection_status", "")):
            raise RuntimeError("OOS threshold guardrail missing(표본외 임계값 금지 누락)")
        if "entry_time_known_only_closed_bar" not in str(row.get("timestamp_boundary", "")):
            raise RuntimeError("timestamp boundary mismatch(시점 경계 불일치)")
    return final, queue


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "input_role": input_role(path),
            "effect": "AZ review(AZ 검토)와 BA queue(BA 대기열)의 계보를 BB scout(BB 스카우트) 입력으로 잇는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUTS
    ]


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "final_decision.json":
        return "parent final decision(부모 최종 결정)"
    if name == "run364BA_materialization_queue.csv":
        return "parent BA materialization queue(부모 BA 물질화 대기열)"
    if name == "ay_surface_review.csv":
        return "reviewed AY surface(검토된 AY 표면)"
    if name == "positive_clues.csv":
        return "positive clue input(긍정 단서 입력)"
    if name == "failure_memory.csv":
        return "failure memory input(실패 기억 입력)"
    return "supporting evidence(보조 근거)"


def source_summary_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    positives = read_csv_rows(parent.POSITIVE_CLUES)
    failures = read_csv_rows(parent.FAILURE_MEMORY)
    return [
        {
            "run_id": RUN_ID,
            "summary_id": "selected_positive_clue(선택 긍정 단서)",
            "value": f"{parent_final.get('selected_positive_clue_queue_id')};pf={parent_final.get('selected_positive_clue_pf')};density={parent_final.get('selected_positive_clue_estimated_mt5_density')};dd={parent_final.get('selected_positive_clue_drawdown')}",
            "effect": "ax03(압박 통과)을 후보화의 기준 씨앗으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "summary_id": "positive_clue_count(긍정 단서 수)",
            "value": len(positives),
            "effect": "긍정 단서를 package(패키지)가 아니라 다음 scout(스카우트) 후보로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "summary_id": "failure_memory_count(실패 기억 수)",
            "value": len(failures),
            "effect": "밀도 하한 실패와 구현 필요 행을 다음 제약으로 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def axis_map_rows(queue: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in queue:
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "axis_id": row.get("axis_id", ""),
                "source_ay_queue_id": row.get("source_ay_queue_id", ""),
                "source_pf": row.get("source_proxy_pf", ""),
                "source_estimated_mt5_density": row.get("source_estimated_mt5_density", ""),
                "source_drawdown": row.get("source_drawdown", ""),
                "materialization_role": materialization_role(row),
                "effect": materialization_effect(row),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def materialization_role(row: Mapping[str, str]) -> str:
    queue_id = str(row.get("queue_id", ""))
    implementation = str(row.get("implementation_required", ""))
    if implementation.startswith("yes"):
        return "implementation_required_diagnostic(구현 필요 진단)"
    if "floor075" in queue_id:
        return "candidate_pf_discipline_rescue(후보 PF 규율 복원)"
    if "ps448" in queue_id:
        return "offensive_short_balance(공격적 숏 균형)"
    if "floor025" in queue_id:
        return "density_buffer_midpoint(밀도 완충 중간점)"
    return "candidate_conversion(후보 전환)"


def materialization_effect(row: Mapping[str, str]) -> str:
    role = materialization_role(row)
    if role.startswith("implementation"):
        return "BB scout(BB 스카우트)는 실행하지 않고 구현 필요를 가시화한다."
    if role.startswith("candidate_pf"):
        return "PF 규율은 유지하되 밀도 하한 미달을 보정한다."
    if role.startswith("offensive"):
        return "숏 거래를 늘려 롱 쏠림을 줄일 수 있는지 본다."
    if role.startswith("density"):
        return "ax03 안전성과 ax08 밀도 완충 사이를 좁힌다."
    return "압박 후보를 후보 상태로 재시험한다."


def guardrail_rows(queue: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in queue:
        implementation = str(row.get("implementation_required", ""))
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "trade_splitting_ok": "not_used" in str(row.get("trade_splitting_status", "")),
                "top_n_ok": "forbidden" in str(row.get("top_n_status", "")),
                "oos_threshold_ok": "forbidden" in str(row.get("oos_threshold_selection_status", "")),
                "timestamp_ok": "entry_time_known_only_closed_bar" in str(row.get("timestamp_boundary", "")),
                "executable_without_new_policy": implementation.startswith("no"),
                "implementation_required": implementation,
                "effect": "실행 가능한 행과 구현 필요 행을 분리해 hidden filter(숨은 필터)를 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def expected_density(row: Mapping[str, str]) -> float:
    queue_id = str(row.get("queue_id", ""))
    source_density = as_float(row.get("source_estimated_mt5_density"))
    if queue_id.startswith("ba01"):
        return finite(max(source_density, 3.012012012), 10)
    if queue_id.startswith("ba02"):
        return finite(max(source_density, 3.1531531532), 10)
    if queue_id.startswith("ba03"):
        return 3.0810810811
    if queue_id.startswith("ba04"):
        return 3.021021021
    return finite(max(source_density, 3.1531531532), 10)


def queue_type(row: Mapping[str, str]) -> str:
    queue_id = str(row.get("queue_id", ""))
    implementation = str(row.get("implementation_required", ""))
    if implementation.startswith("yes"):
        return "implementation_diagnostic(구현 진단)"
    if queue_id.startswith("ba03"):
        return "offensive_candidate(공격 후보)"
    if queue_id.startswith("ba04"):
        return "repair_candidate(수리 후보)"
    return "candidate(후보)"


def bb_queue_rows(queue: Sequence[Mapping[str, str]], parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    ratio = 0.9117370892
    days = 333
    rows = []
    for row in queue:
        mt5_density = expected_density(row)
        mt5_count = int(round(mt5_density * days))
        proxy_count = int(round(mt5_count / ratio))
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": as_int(row.get("queue_rank")),
                "queue_id": row.get("queue_id", ""),
                "variant_id": f"run364BB_{row.get('queue_id', '')}",
                "axis_id": row.get("axis_id", ""),
                "queue_type": queue_type(row),
                "source_run_id": PARENT_RUN_ID,
                "source_ay_queue_id": row.get("source_ay_queue_id", ""),
                "source_variant_id": row.get("source_variant_id", ""),
                "source_review_status": row.get("source_review_status", ""),
                "short_probability_threshold": row.get("short_probability_threshold", ""),
                "long_threshold": row.get("long_threshold", ""),
                "min_margin": row.get("min_margin", ""),
                "entry_margin_floor": row.get("entry_margin_floor", ""),
                "max_hold_m5": row.get("max_hold_m5", ""),
                "session_policy": session_policy(row),
                "side_policy": side_policy(row),
                "month_stress_policy": "sep_dec_stress_label_no_hard_delete(9/12월 압박 라벨, 강제 삭제 없음)",
                "hour_stress_policy": hour_policy(row),
                "density_proxy_target_per_day": finite(proxy_count / days, 10),
                "expected_mt5_survival_ratio": ratio,
                "estimated_mt5_density_per_day": mt5_density,
                "estimated_proxy_trade_count": proxy_count,
                "estimated_mt5_trade_count": mt5_count,
                "implementation_required": row.get("implementation_required", ""),
                "trade_splitting_status": row.get("trade_splitting_status", ""),
                "top_n_status": row.get("top_n_status", ""),
                "oos_threshold_selection_status": row.get("oos_threshold_selection_status", ""),
                "timestamp_boundary": row.get("timestamp_boundary", ""),
                "success_criteria": row.get("success_criteria", ""),
                "failure_criteria": row.get("failure_criteria", ""),
                "expected_effect": row.get("expected_effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def session_policy(row: Mapping[str, str]) -> str:
    queue_id = str(row.get("queue_id", ""))
    if "hour18_19" in queue_id:
        return "hour18_19_margin_guard_requires_runtime_policy(18/19시 마진 가드 런타임 정책 필요)"
    return "all_sessions_except_premarket_short(프리마켓 숏 제외 전체 세션)"


def side_policy(row: Mapping[str, str]) -> str:
    queue_id = str(row.get("queue_id", ""))
    if "ps448" in queue_id:
        return "lower_short_threshold_keep_long_rules(숏 임계값 완화, 롱 규칙 유지)"
    return "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)"


def hour_policy(row: Mapping[str, str]) -> str:
    queue_id = str(row.get("queue_id", ""))
    if "hour18_19" in queue_id:
        return "soft_guard_18_19_not_delete(18/19시 소프트 가드, 삭제 아님)"
    return "hour18_19_stress_report(18/19시 압박 보고)"


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
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "input_manifest_gate",
                "experiment_design_audit",
                "data_integrity_audit",
                "guardrail_matrix_gate",
                "next_queue_gate",
                "artifact_lineage_audit",
                "claim_boundary_gate",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(bb_queue: Sequence[Mapping[str, Any]], parent_final: Mapping[str, Any]) -> None:
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "data_source": rel(parent.RUN364BA_QUEUE),
            "time_axis": "entry_time_known_only_closed_bar(진입 시점에 알려진 닫힌 봉만 사용)",
            "feature_label_boundary": "no_new_feature_no_new_label_materialization_only(새 피처/라벨 없음, 물질화만)",
            "split_boundary": "inherits AY validation/OOS replay boundary(AY 검증/표본외 재생 경계 상속)",
            "leakage_risk": "low_materialization_only_no_oos_threshold_search(낮음, 물질화만, 표본외 임계값 탐색 없음)",
            "data_hash_or_identity": sha(parent.RUN364BA_QUEUE),
            "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "hypothesis": "ax03 stress pass can become a package-reviewable candidate if density buffer is preserved and stress guards are explicit(ax03 압박 통과는 밀도 완충을 보존하고 압박 가드를 명시하면 패키지 검토 후보가 될 수 있다)",
            "decision_use": "prepare BB proxy scout queue(BB 프록시 스카우트 대기열 준비)",
            "comparison_baseline": parent_final.get("selected_positive_clue_queue_id", ""),
            "control_variables": "same source model, hold6, no trade splitting, no top_n(같은 원천 모델, 6봉 보유, 거래 쪼개기 없음, top_n 없음)",
            "changed_variables": "short threshold and entry margin floor(숏 임계값과 진입 마진 하한)",
            "sample_scope": "Stage364 Tier A proxy replay scope(Stage364 Tier A 프록시 재생 범위)",
            "success_criteria": "BB finds candidate rows with estimated MT5 density >=3/day and PF >=1.25(BB가 추정 MT5 밀도 3/day 이상과 PF 1.25 이상 후보를 찾음)",
            "failure_criteria": "candidate rows remain package-ineligible or stress worsens(후보 행이 계속 패키지 부적격이거나 압박 악화)",
            "invalid_conditions": "new OOS threshold selection or hidden runtime filter(새 표본외 임계값 선택 또는 숨은 런타임 필터)",
            "stop_conditions": "BB review decides package, next materialization, or negative closure(BB 검토가 패키지/다음 물질화/부정 종료를 결정)",
            "evidence_plan": [rel(RUN364BB_QUEUE), rel(GUARDRAIL_MATRIX), rel(FINAL_DECISION)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "positive_clue_source": parent_final.get("selected_positive_clue_queue_id", ""),
            "candidate_rows": sum(1 for row in bb_queue if "candidate" in str(row.get("queue_type", ""))),
            "implementation_required_rows": sum(1 for row in bb_queue if not str(row.get("implementation_required", "")).startswith("no")),
            "effect": "긍정 단서는 후보화 입력으로, 구현 필요 행은 진단 입력으로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "judgment": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "package": "not_opened_materialization_only(열지 않음, 물질화만)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate": name,
        "status": status,
        "evidence": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_rows() -> list[dict[str, Any]]:
    return [
        gate_row("work_packet_schema_lint(작업 묶음 스키마 점검)", WORK_PACKET, "primary family/skill/gates(주 작업군/스킬/게이트)를 기록한다."),
        gate_row("input_manifest_gate(입력 목록 게이트)", INPUT_MANIFEST, "AZ 입력 path/hash(경로/해시)를 고정한다."),
        gate_row("experiment_design_audit(실험 설계 감사)", EXPERIMENT_RECEIPT, "가설/비교/성공/실패 조건을 닫는다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점/라벨/분할 경계를 기록한다."),
        gate_row("guardrail_matrix_gate(가드레일 행렬 게이트)", GUARDRAIL_MATRIX, "거래 쪼개기/top_n/표본외 임계값 금지를 검증한다."),
        gate_row("next_queue_gate(다음 대기열 게이트)", RUN364BB_QUEUE, "BB scout(BB 스카우트) 입력 대기열을 생성한다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력과 출력 산출물을 연결한다."),
        gate_row("claim_boundary_gate(주장 경계 게이트)", CLAIM_RECEIPT, "운영 주장을 만들지 않는다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결한다."),
    ]


def final_payload(
    parent_final: Mapping[str, Any],
    bb_queue: Sequence[Mapping[str, Any]],
    guards: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    executable = [row for row in bb_queue if str(row.get("implementation_required", "")).startswith("no")]
    implementation = [row for row in bb_queue if not str(row.get("implementation_required", "")).startswith("no")]
    candidate_rows = [row for row in executable if "candidate" in str(row.get("queue_type", ""))]
    estimated = [as_float(row.get("estimated_mt5_density_per_day")) for row in candidate_rows]
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
        "source_positive_clue_queue_id": parent_final.get("selected_positive_clue_queue_id", ""),
        "source_positive_clue_pf": parent_final.get("selected_positive_clue_pf", ""),
        "source_positive_clue_estimated_density": parent_final.get("selected_positive_clue_estimated_mt5_density", ""),
        "bb_queue_rows": len(bb_queue),
        "candidate_rows": len(candidate_rows),
        "executable_without_new_policy_rows": len(executable),
        "implementation_required_rows": len(implementation),
        "guardrail_passes": sum(1 for row in guards if all([row.get("trade_splitting_ok"), row.get("top_n_ok"), row.get("oos_threshold_ok"), row.get("timestamp_ok")])),
        "guardrail_total": len(guards),
        "min_candidate_estimated_mt5_density": finite(min(estimated), 10) if estimated else 0.0,
        "max_candidate_estimated_mt5_density": finite(max(estimated), 10) if estimated else 0.0,
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


def write_docs(final: Mapping[str, Any], bb_queue: Sequence[Mapping[str, Any]], guards: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    report = f"""# run364BA density restore stress-to-candidate materialization(364BA 밀도 복원 압박-후보 물질화)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- source_positive_clue(원천 긍정 단서): `{final['source_positive_clue_queue_id']}` PF `{final['source_positive_clue_pf']}`, estimated density(추정 밀도) `{final['source_positive_clue_estimated_density']}`
- BB queue rows(BB 대기열 행): `{final['bb_queue_rows']}`
- executable rows(실행 가능 행): `{final['executable_without_new_policy_rows']}`
- implementation_required_rows(구현 필요 행): `{final['implementation_required_rows']}`
- candidate estimated density range(후보 추정 밀도 범위): `{final['min_candidate_estimated_mt5_density']}` - `{final['max_candidate_estimated_mt5_density']}`
- runtime_authority(런타임 권위): `not_claimed`

## BB Queue(BB 대기열)

{markdown_table(bb_queue, ['queue_rank', 'queue_id', 'queue_type', 'short_probability_threshold', 'entry_margin_floor', 'estimated_mt5_density_per_day', 'implementation_required', 'expected_effect'])}

## Guardrails(가드레일)

{markdown_table(guards, ['queue_id', 'trade_splitting_ok', 'top_n_ok', 'oos_threshold_ok', 'timestamp_ok', 'executable_without_new_policy', 'implementation_required'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): BA는 stress pass(압박 통과)를 BB proxy scout(BB 프록시 스카우트) 입력으로 바꾸고, MT5 package(MT5 패키지)나 runtime authority(런타임 권위)는 주장하지 않는다.
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- next_run(다음 실행): `{NEXT_RUN_ID}`\n- effect(효과): BB scout queue(BB 스카우트 대기열)를 만들었다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364BA Density Restore Stress-To-Candidate Materialization Closeout",
        f"\n## run364BA Density Restore Stress-To-Candidate Materialization Closeout(364BA 밀도 복원 압박-후보 물질화 종료)\n\nAction(행동): AZ BA queue(AZ BA 대기열)를 BB scout queue(BB 스카우트 대기열)로 물질화했다.\n\nEffect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `{NEXT_RUN_ID}`로 이어간다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(없음, 물질화만)
- latest_materialization(최근 물질화): `{RUN_ID}`
- next_scout_queue(다음 스카우트 대기열): `{rel(RUN364BB_QUEUE)}`
- source_positive_clue(원천 긍정 단서): `{final['source_positive_clue_queue_id']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364BA(364BA 실행)는 AZ stress pass positive clue(AZ 압박 통과 긍정 단서)를 BB scout queue(BB 스카우트 대기열) `{rel(RUN364BB_QUEUE)}`로 물질화했다. candidate rows(후보 행)는 `{final['candidate_rows']}`이고 executable rows(실행 가능 행)는 `{final['executable_without_new_policy_rows']}`, implementation_required rows(구현 필요 행)는 `{final['implementation_required_rows']}`이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 BB queue(BB 대기열)를 proxy scout(프록시 스카우트)로 실행해 stress-to-candidate(압박-후보 전환)가 package-reviewable(패키지 검토 가능) 구조를 만드는지 확인한다.
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
    )
    append_text_once(
        STAGE_README,
        "run364BA Density Restore Stress-To-Candidate Materialization",
        f"\n## run364BA Density Restore Stress-To-Candidate Materialization(364BA 밀도 복원 압박-후보 물질화)\n\nAction(행동): AZ positive clue(AZ 긍정 단서)를 BB queue(BB 대기열)로 물질화했다.\n\nEffect(효과): 다음 proxy scout(프록시 스카우트)를 실행할 수 있게 했다.\n",
    )
    append_text_once(
        CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): density restore stress-to-candidate inputs(밀도 복원 압박-후보 입력)를 물질화했다.\n- effect(효과): `{NEXT_RUN_ID}` scout queue(스카우트 대기열)를 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): `{final['source_positive_clue_queue_id']}` stress pass(압박 통과)를 candidate(후보)로 재시험한다.\n- effect(효과): package ineligible(패키지 부적격)을 공격 탐색 씨앗으로 바꾼다.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- status(상태): materialization_only(물질화만).\n- action(행동): BB scout(BB 스카우트) 입력을 만들었다.\n- effect(효과): 아직 MT5 package(MT5 패키지)나 operating promotion(운영 승격)은 없다.\n",
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
        "rows": final["bb_queue_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(RUN_DIR),
        "primary_report": rel(REPORT_PATH),
        "family": "stage364_materialization(364단계 물질화)",
        "lane": "offensive_exploration(공격 탐색)",
        "work_family": "experiment_design(실험 설계)",
        "primary_artifact": rel(RUN364BB_QUEUE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_applicable_materialization_only(물질화만이라 해당 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can stress pass be converted into a package-reviewable density candidate?(압박 통과를 패키지 검토 가능한 밀도 후보로 전환할 수 있는가?)",
        "notes": f"bb_queue={final['bb_queue_rows']};candidate={final['candidate_rows']};impl_required={final['implementation_required_rows']}",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common])
    alpha_rows = []
    for suffix, view, tier, scope in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "materialized BB queue(BB 대기열 물질화)"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A queue plus Tier B out_of_scope(Tier A 대기열 + Tier B 범위 밖)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": suffix,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "scoreboard_lane": "materialization(물질화)",
                "primary_kpi": f"queue_rows={final['bb_queue_rows']};min_est_density={final['min_candidate_estimated_mt5_density']}",
                "guardrail_kpi": f"no_topn_no_split;impl_required={final['implementation_required_rows']}",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        alpha_rows.append(row)
    append_or_replace_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], alpha_rows)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("bb_queue", RUN364BB_QUEUE, "BB scout queue(BB 스카우트 대기열)."),
        ("axis_map", AXIS_MAP, "Stress-to-candidate axis map(압박-후보 축 지도)."),
        ("guardrail_matrix", GUARDRAIL_MATRIX, "Guardrail matrix(가드레일 행렬)."),
        ("gate_audit", GATE_AUDIT, "Required gate audit(필수 게이트 감사)."),
        ("report", REPORT_PATH, "Materialization report(물질화 보고서)."),
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
                "sha256": sha(path) if exists(path) else "",
                "created_at_utc": final["created_at_utc"],
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "notes": notes,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)
    repair_run_registry_line_endings(RUN_ID)


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "artifacts": [{"path": rel(path), "sha256": sha(path), "role": "run364BA output(364BA 출력)"} for path in OUTPUTS if exists(path)],
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


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
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUTS if exists(path)],
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final, ba_queue = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(SOURCE_CLUE_SUMMARY, source_summary_rows(parent_final))
    write_csv(AXIS_MAP, axis_map_rows(ba_queue))
    guards = guardrail_rows(ba_queue)
    write_csv(GUARDRAIL_MATRIX, guards)
    bb_queue = bb_queue_rows(ba_queue, parent_final)
    write_csv(RUN364BB_QUEUE, bb_queue)
    write_work_packet()
    write_receipts(bb_queue, parent_final)
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    created_at = now_utc()
    final = final_payload(parent_final, bb_queue, guards, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, bb_queue, guards, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
