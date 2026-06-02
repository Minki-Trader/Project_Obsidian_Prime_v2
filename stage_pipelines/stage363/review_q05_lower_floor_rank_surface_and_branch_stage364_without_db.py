from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

SOURCE_STAGE_ID = "363_lower_floor_rank_surface__q05_long_density_recovery"
NEXT_STAGE_ID = "364_source_regime_label_pivot__dense_cost_recovery"

RUN_NUMBER = "run363C"
RUN_ID = "run363C_review_q05_lower_floor_rank_surface_without_db_v1"
PARENT_RUN_ID = "run363B_materialize_q05_lower_floor_rank_surface_without_db_v1"
NEXT_RUN_NUMBER = "run364A"
NEXT_RUN_ID = "run364A_branch_stage363_to_source_regime_label_pivot_without_db_v1"
NEXT_STAGE_RUN_ID = "run364B_materialize_timestamp_context_cost_surface_without_db_v1"

STATUS = "completed_stage363C_q05_lower_floor_rank_surface_reviewed_no_selection_stage364_branch"
JUDGMENT = "negative_lower_floor_rank_density_cost_tradeoff_preserved_timestamp_context_pivot_no_operating_claim"
DECISION = "stage363C_close_no_selection_open_stage364_source_regime_label_pivot"
CLAIM_BOUNDARY = (
    "research_development_review_only_q05_lower_floor_rank_negative_memory_and_stage364_handoff_"
    "no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

BRANCH_STATUS = "completed_stage364A_source_regime_label_pivot_opened_no_selection"
BRANCH_JUDGMENT = "stage364_source_regime_label_pivot_opened_from_stage363_density_cost_tradeoff_no_operating_claim"
BRANCH_DECISION = "stage364A_open_run364B_materialize_timestamp_context_cost_surface_without_db_v1"
BRANCH_CLAIM_BOUNDARY = (
    "state_sync_stage_branch_source_regime_label_pivot_handoff_only_no_new_model_training_"
    "no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_open_close_time_joined_to_runtime_bar_time_no_timezone_conversion"

STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
STAGE_SPEC_DIR = STAGE_DIR / "00_spec"
STAGE_REVIEW_DIR = STAGE_DIR / "03_reviews"
STAGE_SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run363B"
SOURCE_CROSS_SPLIT = SOURCE_RUN_DIR / "lower_floor_rank_cross_split.csv"
SOURCE_SCORECARD = SOURCE_RUN_DIR / "lower_floor_rank_scorecard.csv"
SOURCE_FAILURE_ATTRIBUTION = SOURCE_RUN_DIR / "lower_floor_rank_failure_attribution.csv"
SOURCE_REVIEW_QUEUE = SOURCE_RUN_DIR / "run363C_review_queue.csv"
SOURCE_FINAL = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_REPORT = STAGE_REVIEW_DIR / "run363B_q05_lower_floor_rank_surface_materialization.md"
SOURCE_SCRIPT = ROOT / "stage_pipelines" / "stage363" / "materialize_q05_lower_floor_rank_surface_without_db.py"

INPUT_FILES = [
    SOURCE_CROSS_SPLIT,
    SOURCE_SCORECARD,
    SOURCE_FAILURE_ATTRIBUTION,
    SOURCE_REVIEW_QUEUE,
    SOURCE_FINAL,
    SOURCE_GATE_AUDIT,
    SOURCE_REPORT,
    SOURCE_SCRIPT,
]

REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
BRANCH_DECISION_TABLE = RUN_DIR / "stage364_branch_decision.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_DESIGN_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"

REPORT_PATH = STAGE_REVIEW_DIR / "run363C_q05_lower_floor_rank_surface_review.md"
STAGE_BRIEF = STAGE_SPEC_DIR / "stage_brief.md"
REVIEW_INDEX = STAGE_REVIEW_DIR / "review_index.md"
STAGE_LEDGER = STAGE_REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = STAGE_SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_RUN_DIR = NEXT_STAGE_DIR / "02_runs" / NEXT_RUN_NUMBER
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUT_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_REVIEW_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"

NEXT_STAGE_BRIEF = NEXT_SPEC_DIR / "stage_brief.md"
NEXT_INPUT_REFS = NEXT_INPUT_DIR / "input_refs.md"
NEXT_INPUT_MANIFEST = NEXT_INPUT_DIR / "stage364_input_manifest.csv"
NEXT_REPORT_PATH = NEXT_REVIEW_DIR / "run364A_stage_branch.md"
NEXT_REVIEW_INDEX = NEXT_REVIEW_DIR / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_REVIEW_DIR / "stage_run_ledger.csv"
NEXT_SELECTION_STATUS = NEXT_SELECTED_DIR / "selection_status.md"
NEXT_STAGE_README = NEXT_STAGE_DIR / "README.md"
NEXT_BRANCH_HANDOFF = NEXT_RUN_DIR / "stage364_branch_handoff.csv"
NEXT_DESIGN_QUEUE = NEXT_RUN_DIR / "run364B_design_queue.csv"
NEXT_FINAL_DECISION = NEXT_RUN_DIR / "final_decision.json"
NEXT_GATE_AUDIT = NEXT_RUN_DIR / "required_gate_coverage_audit.csv"
NEXT_RUN_MANIFEST = NEXT_RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage363C_lower_floor_rank_review_and_stage364_branch.md"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ensure_parent(path)
    encoding = "utf-8-sig" if bom and path.suffix.lower() in {".md", ".txt"} else "utf-8"
    with open(fs_path(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        with open(fs_path(temp_path), "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            for row in rows_list:
                writer.writerow({key: row.get(key, "") for key in fieldnames})
        os.replace(fs_path(temp_path), fs_path(path))
    finally:
        if exists(temp_path):
            os.remove(fs_path(temp_path))


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    elif extend_header:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    replacements = {tuple(str(row.get(key, "")) for key in key_fields): dict(row) for row in rows}
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for row in existing:
        key = tuple(str(row.get(field, "")) for field in key_fields)
        if key in replacements:
            output.append(replacements[key])
            seen.add(key)
        else:
            output.append(row)
    for key, row in replacements.items():
        if key not in seen:
            output.append(row)
    write_csv(path, output, fieldnames)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, default)))


def find_row(rows: Sequence[Mapping[str, Any]], variant_id: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("variant_id") == variant_id:
            return row
    raise KeyError(variant_id)


def cost_positive(row: Mapping[str, Any]) -> bool:
    return as_float(row.get("validation_cost_0_30_net")) > 0 and as_float(row.get("oos_cost_0_30_net")) > 0


def density_pass(row: Mapping[str, Any]) -> bool:
    return as_float(row.get("validation_density")) >= 3.0 and as_float(row.get("oos_density")) >= 3.0


def candidate_eligible(row: Mapping[str, Any]) -> bool:
    return str(row.get("candidate_eligible", "")).lower() == "true"


def stage363_summary(cross_rows: Sequence[Mapping[str, Any]], final: Mapping[str, Any]) -> dict[str, Any]:
    eligible_rows = [row for row in cross_rows if candidate_eligible(row)]
    both_cost_rows = [row for row in eligible_rows if cost_positive(row)]
    both_cost_density_fail = [row for row in both_cost_rows if not density_pass(row)]
    best_validation = find_row(cross_rows, str(final["best_validation_variant_id"]))
    best_oos = find_row(cross_rows, str(final["best_oos_variant_id"]))
    dense = find_row(cross_rows, "s363_r01_all_long_control")
    hour_rows = [row for row in cross_rows if str(row.get("variant_id", "")).startswith("s363_r07_hour_")]
    hour_positive_rows = [row for row in hour_rows if cost_positive(row)]
    best_hour = max(hour_rows, key=lambda row: as_float(row.get("validation_cost_0_30_net")) + as_float(row.get("oos_cost_0_30_net")))
    closest_density_cost_positive = max(
        both_cost_rows,
        key=lambda row: min(as_float(row.get("validation_density")), as_float(row.get("oos_density"))),
    )
    return {
        "total_rows": len(cross_rows),
        "eligible_rows": len(eligible_rows),
        "passing_rows": sum(1 for row in eligible_rows if cost_positive(row) and density_pass(row)),
        "both_cost_positive_density_fail_rows": len(both_cost_density_fail),
        "best_validation": best_validation,
        "best_oos": best_oos,
        "dense": dense,
        "hour_rows": hour_rows,
        "hour_positive_rows": hour_positive_rows,
        "best_hour": best_hour,
        "closest_density_cost_positive": closest_density_cost_positive,
    }


def build_findings(cross_rows: Sequence[Mapping[str, Any]], final: Mapping[str, Any]) -> list[dict[str, Any]]:
    summary = stage363_summary(cross_rows, final)
    best_validation = summary["best_validation"]
    best_oos = summary["best_oos"]
    dense = summary["dense"]
    best_hour = summary["best_hour"]
    closest = summary["closest_density_cost_positive"]
    return [
        {
            "finding_id": "stage363B_zero_pass_review",
            "description": "lower-floor/rank surface(낮은 하한/순위 표면)는 교차 분할 통과 행을 만들지 못했다",
            "validation_cost_0_30_net": "",
            "validation_density": "",
            "oos_cost_0_30_net": "",
            "oos_density": "",
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "review_judgment": "negative_no_selection(부정, 선택 없음)",
            "primary_evidence": f"passing_cross_split_rows={summary['passing_rows']};both_cost_positive_density_fail_rows={summary['both_cost_positive_density_fail_rows']}",
            "next_use": "close_stage363_and_branch_stage364(363단계 종료 및 364단계 분기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "best_validation_not_selectable",
            "description": "best validation(최선 검증) 변형은 비용 양수지만 밀도 3 미만이다",
            "variant_id": best_validation.get("variant_id", ""),
            "validation_cost_0_30_net": best_validation.get("validation_cost_0_30_net", ""),
            "validation_density": best_validation.get("validation_density", ""),
            "oos_cost_0_30_net": best_validation.get("oos_cost_0_30_net", ""),
            "oos_density": best_validation.get("oos_density", ""),
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "review_judgment": "negative_density_fail(부정, 밀도 실패)",
            "primary_evidence": best_validation.get("filter_expression", ""),
            "next_use": "do_not_micro_tune_lower_floor_margin(낮은 하한 마진 미세조정 반복 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "best_oos_not_selectable",
            "description": "best OOS(최선 표본외) 변형은 표본외 수익이 좋지만 검증/표본외 밀도가 모두 낮다",
            "variant_id": best_oos.get("variant_id", ""),
            "validation_cost_0_30_net": best_oos.get("validation_cost_0_30_net", ""),
            "validation_density": best_oos.get("validation_density", ""),
            "oos_cost_0_30_net": best_oos.get("oos_cost_0_30_net", ""),
            "oos_density": best_oos.get("oos_density", ""),
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "review_judgment": "negative_density_fail(부정, 밀도 실패)",
            "primary_evidence": best_oos.get("filter_expression", ""),
            "next_use": "preserve_cost_positive_sparse_clue_only(희소 비용 양수 단서만 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "dense_control_cost_negative",
            "description": "dense all-long control(고밀도 전체 롱 대조)는 밀도를 지키지만 검증 비용이 음수다",
            "variant_id": dense.get("variant_id", ""),
            "validation_cost_0_30_net": dense.get("validation_cost_0_30_net", ""),
            "validation_density": dense.get("validation_density", ""),
            "oos_cost_0_30_net": dense.get("oos_cost_0_30_net", ""),
            "oos_density": dense.get("oos_density", ""),
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "review_judgment": "negative_cost_fail(부정, 비용 실패)",
            "primary_evidence": "density_passes_but_validation_cost_negative(밀도는 통과하지만 검증 비용 음수)",
            "next_use": "needs_context_not_probability_floor_only(확률 하한만 아니라 문맥 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "open_hour_clue_not_standalone",
            "description": "open-hour attribution(진입 시간 귀속)은 일부 시간대에서 비용 양수를 보이나 단독 밀도는 부족하다",
            "variant_id": best_hour.get("variant_id", ""),
            "validation_cost_0_30_net": best_hour.get("validation_cost_0_30_net", ""),
            "validation_density": best_hour.get("validation_density", ""),
            "oos_cost_0_30_net": best_hour.get("oos_cost_0_30_net", ""),
            "oos_density": best_hour.get("oos_density", ""),
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "review_judgment": "positive_clue_not_candidate(긍정 단서, 후보 아님)",
            "primary_evidence": f"hour_positive_rows={len(summary['hour_positive_rows'])}",
            "next_use": "seed_stage364_timestamp_context_surface(364단계 시점 문맥 표면 씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "closest_density_cost_positive_still_low",
            "description": "비용 양수 중 가장 밀도에 가까운 변형도 3/day(일 3회)에 못 미친다",
            "variant_id": closest.get("variant_id", ""),
            "validation_cost_0_30_net": closest.get("validation_cost_0_30_net", ""),
            "validation_density": closest.get("validation_density", ""),
            "oos_cost_0_30_net": closest.get("oos_cost_0_30_net", ""),
            "oos_density": closest.get("oos_density", ""),
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "review_judgment": "negative_density_gap(부정, 밀도 간격)",
            "primary_evidence": closest.get("filter_expression", ""),
            "next_use": "pivot_to_timestamp_context_or_new_label_source(시점 문맥 또는 새 라벨 원천 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF",
            "hypothesis": "lower p_long floor and validation-derived rank surface(낮은 p_long 하한 및 검증 파생 순위 표면)가 비용과 밀도를 동시에 회복한다",
            "variants_tried": "90 cross-split rows across absolute floor, margin rank, long-short rank, target density, hour attribution, sparse upper bound(90개 교차 분할 행)",
            "failed_boundary": "validation/OOS +0.30 cost positive and density >= 3(검증/표본외 +0.30 비용 양수 및 밀도 3 이상)",
            "why_failed": "21 rows kept both splits cost positive but all stayed below trade density minimum(21행이 양쪽 비용 양수였지만 모두 최소 거래 밀도 미만)",
            "salvage_value": "sparse cost-positive surfaces and open-hour clue(희소 비용 양수 표면 및 진입 시간 단서)",
            "reopen_condition": "timestamp-safe context/regime/label source(시점 안전 문맥/국면/라벨 원천)가 density >= 3 with cost positive를 동시에 만든다",
            "do_not_repeat": "do not repeat lower-floor/rank threshold micro-tuning as candidate selection(낮은 하한/순위 임계값 미세조정을 후보 선택처럼 반복하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_stage364_design_queue() -> list[dict[str, Any]]:
    common = {
        "source_run_id": RUN_ID,
        "source_stage_id": SOURCE_STAGE_ID,
        "time_axis": TIME_AXIS,
        "tier_scope": "Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)",
        "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
        "claim_boundary": BRANCH_CLAIM_BOUNDARY,
    }
    rows = [
        {
            "queue_id": "s364_r01_open_hour_context_stack",
            "priority": 1,
            "idea_family": "timestamp_context_surface(시점 문맥 표면)",
            "hypothesis": "open_time hour/session(진입 시간/세션)을 margin/p_long(마진/p_long)과 결합하면 비용 음수 시간대를 줄이면서 밀도를 보존한다",
            "materialization_plan": "validation-only hour/session allow/deny groups plus q05 dense control(검증 전용 시간/세션 허용/차단 그룹 + q05 고밀도 대조)",
            "success_gate": "validation/OOS cost_0_30_net > 0 and density >= 3 without split trade-count slicing(검증/표본외 비용 양수 및 밀도 3 이상, 거래수 쪼개기 없음)",
            "failure_memory_used": "FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF",
        },
        {
            "queue_id": "s364_r02_day_hour_joint_context",
            "priority": 2,
            "idea_family": "calendar_context_surface(달력 문맥 표면)",
            "hypothesis": "day-of-week/hour(요일/시간) 조합은 q05 dense control(고밀도 대조)의 손실 구간을 설명할 수 있다",
            "materialization_plan": "derive validation-only safe calendar groups from open_time known at entry(진입 시점에 알려진 open_time에서 검증 전용 안전 달력 그룹 파생)",
            "success_gate": "cost-positive validation/OOS with density >= 3 and no OOS-derived thresholds(비용 양수, 밀도 3 이상, 표본외 파생 임계값 금지)",
            "failure_memory_used": "FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF",
        },
        {
            "queue_id": "s364_r03_closed_bar_regime_context",
            "priority": 3,
            "idea_family": "closed_bar_regime_surface(닫힌 봉 국면 표면)",
            "hypothesis": "closed M5 bar volatility/trend state(닫힌 M5 봉 변동성/추세 상태)가 probability threshold(확률 임계값)보다 비용 압박을 잘 설명한다",
            "materialization_plan": "prepare report-derived queue first; later attach existing closed-bar features if materialization shows a clue(먼저 보고서 파생 대기열, 단서가 있으면 기존 닫힌 봉 피처 결합)",
            "success_gate": "no look-ahead, validation-only thresholds, density >= 3(미래참조 없음, 검증 전용 임계값, 밀도 3 이상)",
            "failure_memory_used": "FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF",
        },
        {
            "queue_id": "s364_r04_label_source_pivot_probe",
            "priority": 4,
            "idea_family": "label_source_pivot(라벨 원천 전환)",
            "hypothesis": "q05 long-only label source(q05 롱 단독 라벨 원천)가 dense but noisy(고밀도지만 잡음 큼)라면 label horizon/action source(라벨 기간/행동 원천)를 바꿔야 한다",
            "materialization_plan": "no training in run364B; only design feature/label candidate packet from Stage363 failure memory(run364B에서는 학습 없음, 설계 후보 묶음만)",
            "success_gate": "review produces concrete training packet without operating claim(운영 주장 없이 구체 학습 묶음 생성)",
            "failure_memory_used": "FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF",
        },
        {
            "queue_id": "s364_r05_cost_positive_sparse_expansion",
            "priority": 5,
            "idea_family": "sparse_clue_expansion(희소 단서 확장)",
            "hypothesis": "sparse cost-positive variants(희소 비용 양수 변형)을 같은 신호 반복이 아니라 context expansion(문맥 확장)으로 밀도를 회복할 수 있다",
            "materialization_plan": "expand around best_validation/best_oos with timestamp context, not lower-floor micro tuning(최선 검증/표본외 주변을 시점 문맥으로 확장, 하한 미세조정 아님)",
            "success_gate": "density improves toward 3 while cost stays positive(비용 양수를 유지하며 밀도가 3에 접근)",
            "failure_memory_used": "FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF",
        },
        {
            "queue_id": "s364_r06_dense_control_negative_control",
            "priority": 6,
            "idea_family": "negative_control(부정 대조)",
            "hypothesis": "if all derived context variants cannot beat q05 dense control, the source label is exhausted(문맥 변형이 q05 고밀도 대조를 넘지 못하면 원천 라벨 소진)",
            "materialization_plan": "keep all-long dense control and no-context probability control as guardrails(전체 롱 고밀도 대조와 무문맥 확률 대조 유지)",
            "success_gate": "context variants must beat dense control on validation cost and preserve OOS direction(문맥 변형이 검증 비용에서 고밀도 대조를 넘고 표본외 방향 보존)",
            "failure_memory_used": "FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF",
        },
    ]
    return [{**common, **row} for row in rows]


def source_gate_passed() -> bool:
    _, gate_rows = read_csv_rows(SOURCE_GATE_AUDIT)
    return bool(gate_rows) and all(row.get("status") == "passed" for row in gate_rows)


def gate_rows() -> list[dict[str, Any]]:
    final = read_json(SOURCE_FINAL)
    gates = [
        ("input_cross_split_present", exists(SOURCE_CROSS_SPLIT), SOURCE_CROSS_SPLIT, "Stage363B cross split(363B 교차 분할) 확인"),
        ("input_final_decision_zero_pass", as_int(final.get("passing_cross_split_rows")) == 0, SOURCE_FINAL, "passing_cross_split_rows(교차 분할 통과 행) 0 확인"),
        ("source_gate_audit_passed", source_gate_passed(), SOURCE_GATE_AUDIT, "Stage363B gate audit(363B 게이트 감사) 통과 확인"),
        ("review_findings_written", exists(REVIEW_FINDINGS), REVIEW_FINDINGS, "review findings(검토 결과) 기록"),
        ("failure_memory_written", exists(FAILURE_MEMORY), FAILURE_MEMORY, "failure memory(실패 기억) 기록"),
        ("stage364_design_queue_written", exists(NEXT_DESIGN_QUEUE), NEXT_DESIGN_QUEUE, "Stage364 design queue(364단계 설계 대기열) 기록"),
        ("stage364_structure_created", exists(NEXT_STAGE_BRIEF) and exists(NEXT_SELECTION_STATUS), NEXT_STAGE_BRIEF, "Stage364 structure(364단계 구조) 생성"),
        ("state_sync_audit", exists(WORKSPACE_STATE) and NEXT_STAGE_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "current truth(현재 진실) Stage364 동기화"),
        ("artifact_lineage_connected", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "artifact lineage receipt(산출물 계보 영수증) 기록"),
        ("required_gate_coverage_audit", exists(GATE_AUDIT), GATE_AUDIT, "required gate coverage audit(필수 게이트 커버리지 감사) 기록"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 주장 없음"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "path": rel(path),
            "notes": notes,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, notes in gates
    ]


def branch_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("stage364_structure_created", exists(NEXT_STAGE_DIR), NEXT_STAGE_DIR, "Stage364 structure(364단계 구조) 생성"),
        ("stage364_design_queue_created", exists(NEXT_DESIGN_QUEUE), NEXT_DESIGN_QUEUE, "Stage364 design queue(364단계 설계 대기열) 생성"),
        ("stage364_selection_status_sync", exists(NEXT_SELECTION_STATUS), NEXT_SELECTION_STATUS, "Stage364 selection status(선택 상태) 동기화"),
        ("stage364_ledger_sync", exists(NEXT_STAGE_LEDGER), NEXT_STAGE_LEDGER, "Stage364 ledger(장부) 동기화"),
        ("state_sync_audit", exists(WORKSPACE_STATE) and NEXT_STAGE_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("final_claim_guard", True, NEXT_FINAL_DECISION, "운영 주장 없음"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "path": rel(path),
            "notes": notes,
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, notes in gates
    ]


def write_run_artifacts(findings: Sequence[Mapping[str, Any]], failure_memory: Sequence[Mapping[str, Any]], design_queue: Sequence[Mapping[str, Any]]) -> None:
    write_csv(REVIEW_FINDINGS, findings)
    write_csv(FAILURE_MEMORY, failure_memory)
    write_csv(BRANCH_DECISION_TABLE, [{
        "run_id": RUN_ID,
        "decision": DECISION,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_materialization_run_id": NEXT_STAGE_RUN_ID,
        "reason": "Stage363B lower-floor/rank surface(363B 낮은 하한/순위 표면)가 비용-밀도 동시 통과를 만들지 못함",
        "claim_boundary": CLAIM_BOUNDARY,
    }])
    write_csv(NEXT_BRANCH_HANDOFF, [{
        "source_run_id": RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "design_queue": rel(NEXT_DESIGN_QUEUE),
        "claim_boundary": BRANCH_CLAIM_BOUNDARY,
    }])
    write_csv(NEXT_DESIGN_QUEUE, design_queue)
    write_csv(NEXT_INPUT_MANIFEST, [
        {"input_path": rel(path), "sha256": sha256_file(path), "required": "true", "claim_boundary": BRANCH_CLAIM_BOUNDARY}
        for path in INPUT_FILES
    ])

    write_json(WORK_PACKET, {
        "run_id": RUN_ID,
        "primary_family": "experiment_execution(실험 실행)",
        "primary_skill": "obsidian-result-judgment(결과 판정)",
        "support_skills": [
            "obsidian-reentry-read(재진입 읽기)",
            "obsidian-exploration-mandate(탐색 규율)",
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-artifact-lineage(산출물 계보)",
        ],
        "required_gates": [
            "input_cross_split_present",
            "input_final_decision_zero_pass",
            "source_gate_audit_passed",
            "review_findings_written",
            "failure_memory_written",
            "stage364_design_queue_written",
            "stage364_structure_created",
            "state_sync_audit",
            "artifact_lineage_connected",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(DATA_INTEGRITY_RECEIPT, {
        "data_source": [rel(SOURCE_CROSS_SPLIT), rel(SOURCE_SCORECARD), rel(SOURCE_FAILURE_ATTRIBUTION), rel(SOURCE_FINAL)],
        "time_axis": TIME_AXIS,
        "sample_scope": "US100 M5 q05 long-only MT5 report-derived validation/OOS surface review(US100 M5 q05 롱 단독 MT5 보고서 파생 검증/표본외 표면 검토)",
        "missing_or_duplicate_check": "run363C reviews Stage363B derived rows only; no new bar joins(run363C는 Stage363B 파생 행만 검토, 새 봉 결합 없음)",
        "feature_label_boundary": "no new features, labels, proxy, model, or MT5 execution; next queue uses open_time known at entry(새 피처/라벨/프록시/모델/MT5 없음, 다음 대기열은 진입 시점 open_time 사용)",
        "split_boundary": "validation and OOS remain separate; Stage364 must derive thresholds from validation only(검증/표본외 분리 유지, Stage364 임계값은 검증에서만 파생)",
        "leakage_risk": "OOS-derived session selection or outcome-derived label reuse would be invalid(표본외 파생 세션 선택 또는 결과 파생 라벨 재사용은 무효)",
        "data_hash_or_identity": {
            rel(SOURCE_CROSS_SPLIT): sha256_file(SOURCE_CROSS_SPLIT),
            rel(SOURCE_FINAL): sha256_file(SOURCE_FINAL),
        },
        "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
    })
    write_json(EXPERIMENT_DESIGN_RECEIPT, {
        "idea_id": "IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY",
        "hypothesis": "timestamp-safe context/regime/label source pivot(시점 안전 문맥/국면/라벨 원천 전환)이 q05 dense trade density(q05 고밀도 거래 밀도)를 보존하며 비용을 회복한다",
        "legacy_relation": "none(없음)",
        "tier_scope": "Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)",
        "broad_sweep": "open hour, day/hour, closed-bar regime, label source, sparse clue expansion(진입 시간, 요일/시간, 닫힌 봉 국면, 라벨 원천, 희소 단서 확장)",
        "extreme_sweep": "dense all-long control and no-context probability control(고밀도 전체 롱 대조 및 무문맥 확률 대조)",
        "micro_search_gate": "validation/OOS cost_0_30_net > 0 and density >= 3(검증/표본외 비용 양수 및 밀도 3 이상)",
        "wfo_plan": "WFO after Stage364 produces a positive scout only(Stage364가 긍정 스카우트를 만들 때만 WFO)",
        "failure_memory": rel(FAILURE_MEMORY),
        "evidence_boundary": "stage_branch_only(단계 분기 전용)",
    })
    write_json(LINEAGE_RECEIPT, {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path("stage_pipelines/stage363/review_q05_lower_floor_rank_surface_and_branch_stage364_without_db.py")),
        "consumer": [rel(REPORT_PATH), rel(NEXT_DESIGN_QUEUE), rel(NEXT_STAGE_BRIEF), rel(NEXT_STAGE_RUN_ID)],
        "artifact_paths": [rel(REVIEW_FINDINGS), rel(FAILURE_MEMORY), rel(NEXT_DESIGN_QUEUE), rel(REPORT_PATH), rel(NEXT_REPORT_PATH)],
        "artifact_hashes": {
            rel(SOURCE_CROSS_SPLIT): sha256_file(SOURCE_CROSS_SPLIT),
            rel(SOURCE_FINAL): sha256_file(SOURCE_FINAL),
            rel(SOURCE_GATE_AUDIT): sha256_file(SOURCE_GATE_AUDIT),
        },
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(NEXT_STAGE_LEDGER)],
        "availability": "tracked_docs_with_ignored_run_artifacts(추적 문서와 무시된 실행 산출물)",
        "lineage_judgment": "connected_with_boundary(경계 내 연결됨)",
    })
    write_json(JUDGMENT_RECEIPT, {
        "result_subject": RUN_ID,
        "evidence_available": [rel(SOURCE_FINAL), rel(REVIEW_FINDINGS), rel(FAILURE_MEMORY), rel(NEXT_DESIGN_QUEUE)],
        "evidence_missing": "no new MT5 execution, no candidate selection, no Tier B source(새 MT5 실행 없음, 후보 선택 없음, Tier B 원천 없음)",
        "judgment_label": "negative(부정)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_STAGE_RUN_ID,
        "user_explanation_hook": "lower-floor/rank thresholds found sparse cost-positive clues but not enough daily density(낮은 하한/순위 임계값은 희소 비용 양수 단서를 찾았지만 일 밀도는 부족)",
    })
    write_json(CLAIM_RECEIPT, {
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    })

    final = {
        "stage_id": SOURCE_STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_materialization_run_id": NEXT_STAGE_RUN_ID,
        "review_findings_rows": len(findings),
        "failure_memory_rows": len(failure_memory),
        "stage364_design_queue_rows": len(design_queue),
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {
        "run_id": RUN_ID,
        "created_at_utc": now_utc(),
        "command": "python stage_pipelines/stage363/review_q05_lower_floor_rank_surface_and_branch_stage364_without_db.py",
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(REVIEW_FINDINGS), rel(FAILURE_MEMORY), rel(NEXT_DESIGN_QUEUE), rel(REPORT_PATH), rel(NEXT_REPORT_PATH)],
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(NEXT_FINAL_DECISION, {
        "stage_id": NEXT_STAGE_ID,
        "run_number": NEXT_RUN_NUMBER,
        "run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "status": BRANCH_STATUS,
        "judgment": BRANCH_JUDGMENT,
        "decision": BRANCH_DECISION,
        "next_run_id": NEXT_STAGE_RUN_ID,
        "design_queue_rows": len(design_queue),
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BRANCH_CLAIM_BOUNDARY,
    })
    write_json(NEXT_RUN_MANIFEST, {
        "run_id": NEXT_RUN_ID,
        "created_at_utc": now_utc(),
        "producer": rel(Path("stage_pipelines/stage363/review_q05_lower_floor_rank_surface_and_branch_stage364_without_db.py")),
        "inputs": [rel(FINAL_DECISION), rel(REVIEW_FINDINGS), rel(FAILURE_MEMORY)],
        "outputs": [rel(NEXT_DESIGN_QUEUE), rel(NEXT_BRANCH_HANDOFF), rel(NEXT_REPORT_PATH)],
        "claim_boundary": BRANCH_CLAIM_BOUNDARY,
    })


def best_finding(findings: Sequence[Mapping[str, Any]], key: str) -> Mapping[str, Any]:
    rows = [row for row in findings if row.get(key, "") not in ("", None)]
    return max(rows, key=lambda row: as_float(row[key]))


def write_reports(findings: Sequence[Mapping[str, Any]], design_queue: Sequence[Mapping[str, Any]]) -> None:
    best_validation = best_finding(findings, "validation_cost_0_30_net")
    best_oos = best_finding(findings, "oos_cost_0_30_net")
    zero = next(row for row in findings if row["finding_id"] == "stage363B_zero_pass_review")
    gates = gate_rows()
    branch_gates = branch_gate_rows()

    write_text(REPORT_PATH, f"""# run363C Q05 Lower-Floor Rank Surface Review(run363C q05 낮은 하한 순위 표면 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_stage_id(다음 단계 ID): `{NEXT_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): Stage363B(363B 실행)의 lower-floor/rank surface(낮은 하한/순위 표면)를 검토하고 Stage364(364단계) source/regime/label pivot(원천/국면/라벨 전환)을 열었다.

Effect(효과): lower-floor threshold micro-tuning(낮은 하한 임계값 미세조정)을 더 끌지 않고, timestamp-safe context(시점 안전 문맥)로 밀도와 비용을 다시 찾는다.

## Review Result(검토 결과)

- review_findings_rows(검토 결과 행): `{len(findings)}`
- failure_summary(실패 요약): `{zero["primary_evidence"]}`
- best_validation_finding(최선 검증 항목): `{best_validation["finding_id"]}`
- best_validation_variant_id(최선 검증 변형 ID): `{best_validation.get("variant_id", "")}`
- best_validation_cost_0_30_net(최선 검증 +0.30 비용 순수익): `{best_validation["validation_cost_0_30_net"]}`
- best_validation_density(최선 검증 밀도): `{best_validation["validation_density"]}`
- best_oos_finding(최선 표본외 항목): `{best_oos["finding_id"]}`
- best_oos_variant_id(최선 표본외 변형 ID): `{best_oos.get("variant_id", "")}`
- best_oos_cost_0_30_net(최선 표본외 +0.30 비용 순수익): `{best_oos["oos_cost_0_30_net"]}`
- best_oos_density(최선 표본외 밀도): `{best_oos["oos_density"]}`
- stage364_design_queue_rows(364단계 설계 대기열 행): `{len(design_queue)}`

## Judgment Boundary(판정 경계)

Action(행동): Stage363(363단계)을 no-selection negative memory(선택 없음 부정 기억)로 닫았다.

Effect(효과): 이 closeout(종료)은 promotion_candidate(승격 후보), MT5 execution(MT5 실행), operating promotion(운영 승격), runtime authority(런타임 권위)가 아니다.

## Artifacts(산출물)

- review_findings(검토 결과): `{rel(REVIEW_FINDINGS)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- branch_decision(분기 결정): `{rel(BRANCH_DECISION_TABLE)}`
- stage364_design_queue(364단계 설계 대기열): `{rel(NEXT_DESIGN_QUEUE)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(SELECTION_STATUS, f"""# Stage363 Selection Status(363단계 선택 상태)

- selection_status(선택 상태): `closed_no_selection_branched_to_stage364(종료, 선택 없음, 364단계 분기)`
- active_stage_id(활성 단계 ID): `{SOURCE_STAGE_ID}`
- current_run_id(현재 실행 ID): `{RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- next_stage_id(다음 단계 ID): `{NEXT_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run363C Review Closeout(363C 검토 종료 기록)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- stage364_design_queue_rows(364단계 설계 대기열 행): `{len(design_queue)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): lower-floor/rank surface(낮은 하한/순위 표면)를 더 미세조정하지 않고 Stage364(364단계)로 분기했다.

Effect(효과): 다음 탐색은 timestamp-safe context/regime/label source(시점 안전 문맥/국면/라벨 원천)에 집중한다.
""")
    append_text_once(STAGE_BRIEF, "## run363C Review Closeout", f"""## run363C Review Closeout(363C 검토 종료)

Action(행동): lower-floor/rank surface(낮은 하한/순위 표면) 실패를 no-selection negative memory(선택 없음 부정 기억)로 닫았다.

Effect(효과): Stage364(364단계) `{NEXT_STAGE_ID}`를 열어 timestamp-safe context/regime/label source pivot(시점 안전 문맥/국면/라벨 원천 전환)을 다룬다.
""")
    append_text_once(REVIEW_INDEX, "run363C_q05_lower_floor_rank_surface_review", f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - q05 lower-floor/rank surface(q05 낮은 하한/순위 표면) review(검토) and Stage364 branch(364단계 분기).""")
    append_text_once(STAGE_README, "run363C Review Closeout", f"""## run363C Review Closeout(363C 검토 종료)

Action(행동): Stage363(363단계)을 후보 선택 없이 닫고 Stage364(364단계)로 분기했다.

Effect(효과): 같은 lower-floor/rank threshold(낮은 하한/순위 임계값) 반복을 멈추고 timestamp context(시점 문맥) 탐색으로 넘어간다.
""")

    write_text(NEXT_INPUT_REFS, f"""# Stage364 Input References(364단계 입력 참조)

- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{RUN_ID}`
- parent_materialization_run_id(부모 구체화 실행 ID): `{PARENT_RUN_ID}`
- source_cross_split(원천 교차 분할): `{rel(SOURCE_CROSS_SPLIT)}`
- source_failure_attribution(원천 실패 귀속): `{rel(SOURCE_FAILURE_ATTRIBUTION)}`
- source_final_decision(원천 최종 결정): `{rel(SOURCE_FINAL)}`
- stage364_design_queue(364단계 설계 대기열): `{rel(NEXT_DESIGN_QUEUE)}`
- claim_boundary(주장 경계): `{BRANCH_CLAIM_BOUNDARY}`
""")
    write_text(NEXT_STAGE_BRIEF, f"""# Stage364 Brief(364단계 개요): Source Regime Label Pivot(원천 국면 라벨 전환)

- canonical_stage_id(정식 단계 ID): `{NEXT_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_STAGE_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{NEXT_RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{RUN_ID}`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `{BRANCH_CLAIM_BOUNDARY}`

## Question(질문)

Can timestamp-safe source/regime/label context(시점 안전 원천/국면/라벨 문맥) recover q05 dense cost(고밀도 q05 비용 회복) while keeping trade density >= 3/day(거래 밀도 일 3회 이상 유지)를 달성할 수 있는가?

## Source Truth(원천 진실)

- source_failure(원천 실패): Stage363B(363B 실행)는 passing_cross_split_rows(교차 분할 통과 행) `0`.
- preserved_clue(보존 단서): sparse cost-positive variants(희소 비용 양수 변형)와 open-hour clue(진입 시간 단서)는 남았다.
- no_selection_boundary(선택 없음 경계): candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격) 없음.

## Scope(범위)

Action(행동): Stage364(364단계)는 Stage363C(363C 실행)의 design queue(설계 대기열)를 작게 구체화한다.

Effect(효과): 같은 threshold micro-tuning(임계값 미세조정)을 반복하지 않고, 진입 시점에 알려진 context(문맥)와 label/source pivot(라벨/원천 전환)을 분리해 판단한다.

## Exploration Boundary(탐색 경계)

- idea_id(아이디어 ID): `IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY`
- hypothesis(가설): timestamp-safe context/regime/label source pivot(시점 안전 문맥/국면/라벨 원천 전환)이 dense trade count(고밀도 거래수)를 유지하며 cost drag(비용 끌림)를 줄인다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): open hour(진입 시간), day/hour(요일/시간), closed-bar regime(닫힌 봉 국면), label source(라벨 원천), sparse clue expansion(희소 단서 확장)
- extreme_sweep(극단 탐색): dense all-long control(전체 롱 고밀도 대조), no-context probability control(무문맥 확률 대조)
- micro_search_gate(미세 탐색 게이트): validation/OOS +0.30 net positive(검증/표본외 +0.30 순수익 양수) 그리고 density >= 3(밀도 3 이상)
- wfo_plan(WFO 계획): Stage364B(364B 실행)가 positive scout(긍정 탐색)를 만들 때만 WFO(walk-forward optimization, 워크포워드 최적화)로 강화한다.
- failure_memory(실패 기억): Stage363C(363C 실행)는 lower-floor/rank threshold micro-tuning(낮은 하한/순위 임계값 미세조정)을 반복 금지로 기록했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`
""")
    write_text(NEXT_REPORT_PATH, f"""# run364A Stage Branch(364A 단계 분기): Source Regime Label Pivot(원천 국면 라벨 전환)

- run_id(실행 ID): `{NEXT_RUN_ID}`
- parent_run_id(부모 실행 ID): `{RUN_ID}`
- status(상태): `{BRANCH_STATUS}`
- judgment(판정): `{BRANCH_JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_STAGE_RUN_ID}`
- gate_result(게이트 결과): `{sum(1 for row in branch_gates if row["status"] == "passed")}/{len(branch_gates)}`

Action(행동): Stage363C(363C 실행)의 실패 기억에서 Stage364(364단계) source/regime/label pivot(원천/국면/라벨 전환)을 열었다.

Effect(효과): Stage364B(364B 실행)는 `{rel(NEXT_DESIGN_QUEUE)}`를 작게 구체화하며, 운영 주장 없이 새 수익 원천을 탐색한다.
""")
    write_text(NEXT_REVIEW_INDEX, f"""# Stage364 Review Index(364단계 검토 색인)

- `{NEXT_RUN_ID}`: `{rel(NEXT_REPORT_PATH)}` - Stage364 branch(364단계 분기) and design queue handoff(설계 대기열 인계).
""")
    write_text(NEXT_SELECTION_STATUS, f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- active_stage_id(활성 단계 ID): `{NEXT_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_STAGE_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{NEXT_RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): source/regime/label pivot(원천/국면/라벨 전환) stage(단계)를 열었다.

Effect(효과): 다음 실행은 Stage364B(364B 실행)에서 timestamp context surface(시점 문맥 표면)를 구체화한다.
""")
    write_text(NEXT_STAGE_README, f"""# Stage364(364단계): Source Regime Label Pivot(원천 국면 라벨 전환)

Action(행동): Stage363C(363C 실행)의 lower-floor/rank failure(낮은 하한/순위 실패)에서 timestamp-safe context(시점 안전 문맥) 탐색으로 분기했다.

Effect(효과): q05 dense trade count(q05 고밀도 거래수)를 쪼개지 않고 cost drag(비용 끌림)를 줄일 수 있는 새 설명 축을 확인한다.
""")
    write_text(DECISION_DOC, f"""# Decision(결정): Stage363C Review and Stage364 Branch(363C 검토 및 364단계 분기)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_stage_id(다음 단계 ID): `{NEXT_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- next_materialization_run_id(다음 구체화 실행 ID): `{NEXT_STAGE_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage363B(363B 실행)의 lower-floor/rank surface(낮은 하한/순위 표면)를 no-selection negative memory(선택 없음 부정 기억)로 닫고 Stage364(364단계)를 열었다.

Effect(효과): 다음 탐색은 threshold micro-tuning(임계값 미세조정)이 아니라 timestamp-safe source/regime/label context(시점 안전 원천/국면/라벨 문맥)다.
""")


def registry_rows(findings: Sequence[Mapping[str, Any]], design_queue: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    gates = gate_rows()
    branch_gates = branch_gate_rows()
    best_validation = best_finding(findings, "validation_cost_0_30_net")
    best_oos = best_finding(findings, "oos_cost_0_30_net")
    common_review = {
        "stage_id": SOURCE_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "lower_floor_rank_review(낮은 하한 순위 검토)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage363C reviews lower-floor/rank surface and branches Stage364(Stage363C 낮은 하한/순위 표면 검토 및 Stage364 분기).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(findings),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(REVIEW_FINDINGS),
        "result_status": STATUS,
        "sample_rows": len(findings),
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "lane": "lower_floor_rank_review(낮은 하한 순위 검토)",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Should lower-floor rank surface branch to timestamp context pivot?(낮은 하한 순위 표면을 시점 문맥 전환으로 분기해야 하는가?)",
        "metric_scope": "review_only(검토 전용)",
    }
    tier_a = dict(common_review)
    tier_a.update({
        "subrun_id": f"{RUN_ID}__Tier_A",
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "row_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "kpi_scope": "report-derived review(보고서 파생 검토)",
        "primary_kpi": f"best_validation={best_validation.get('variant_id', '')};validation_net={best_validation.get('validation_cost_0_30_net', '')};best_oos={best_oos.get('variant_id', '')};oos_net={best_oos.get('oos_cost_0_30_net', '')}",
        "guardrail_kpi": f"stage364_design_queue_rows={len(design_queue)};candidate_selection=not_run",
    })
    tier_b = dict(tier_a)
    tier_b.update({
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
    })
    combined = dict(tier_a)
    combined.update({
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
    })
    run_review = dict(tier_a)
    branch_row = {
        "stage_id": NEXT_STAGE_ID,
        "run_id": NEXT_RUN_ID,
        "subrun_id": f"{NEXT_RUN_ID}__Tier_AplusB",
        "parent_run_id": RUN_ID,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "status": BRANCH_STATUS,
        "judgment": BRANCH_JUDGMENT,
        "path": rel(NEXT_REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage364 source/regime/label pivot branch(Stage364 원천/국면/라벨 전환 분기).",
        "run_number": NEXT_RUN_NUMBER,
        "date": TODAY,
        "decision": BRANCH_DECISION,
        "next_run_id": NEXT_STAGE_RUN_ID,
        "rows": len(design_queue),
        "gate_passes": sum(1 for row in branch_gates if row["status"] == "passed"),
        "gate_total": len(branch_gates),
        "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        "report_path": rel(NEXT_REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(NEXT_DESIGN_QUEUE),
        "result_status": BRANCH_STATUS,
        "sample_rows": len(design_queue),
        "source_package_run_id": RUN_ID,
        "work_family": "state_sync(상태 동기화)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": BRANCH_JUDGMENT,
        "final_decision_path": rel(NEXT_FINAL_DECISION),
        "created_at": TODAY,
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "primary_report": rel(NEXT_REPORT_PATH),
        "evidence_boundary": BRANCH_CLAIM_BOUNDARY,
        "next_action": NEXT_STAGE_RUN_ID,
        "question": "Can timestamp-safe source/regime/label context recover dense cost?(시점 안전 원천/국면/라벨 문맥이 고밀도 비용을 회복할 수 있는가?)",
        "ledger_row_id": f"{NEXT_RUN_ID}__Tier_AplusB",
        "row_id": f"{NEXT_RUN_ID}__Tier_AplusB",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage_branch_no_new_runtime(단계 분기, 새 런타임 없음)",
        "primary_kpi": f"design_queue_rows={len(design_queue)}",
        "guardrail_kpi": "no_candidate_selection(후보 선택 없음)",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "metric_scope": "out_of_scope_by_claim(주장 범위 밖)",
    }
    return [run_review, branch_row], [tier_a, tier_b, combined, branch_row], [tier_a, tier_b, combined], [branch_row]


def write_registries(findings: Sequence[Mapping[str, Any]], design_queue: Sequence[Mapping[str, Any]]) -> None:
    run_rows, project_rows, stage_rows, next_stage_rows = registry_rows(findings, design_queue)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)
    write_csv(NEXT_STAGE_LEDGER, next_stage_rows)


def write_workspace_and_notes(design_queue: Sequence[Mapping[str, Any]]) -> None:
    write_text(WORKSPACE_STATE, f"""current_stage_id: {NEXT_STAGE_ID}
current_run_id: {NEXT_STAGE_RUN_ID}
latest_completed_run_id: {NEXT_RUN_ID}
current_status: {BRANCH_STATUS}
current_judgment: {BRANCH_JUDGMENT}
current_decision: {BRANCH_DECISION}
next_run_id: {NEXT_STAGE_RUN_ID}
claim_boundary: {BRANCH_CLAIM_BOUNDARY}
updated_at: {TODAY}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{NEXT_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_STAGE_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{NEXT_RUN_ID}`
- current_status(현재 상태): `{BRANCH_STATUS}`
- current_judgment(현재 판정): `{BRANCH_JUDGMENT}`
- current_decision(현재 결정): `{BRANCH_DECISION}`
- claim_boundary(주장 경계): `{BRANCH_CLAIM_BOUNDARY}`

Action(행동): Stage363C(363C 실행)가 lower-floor/rank surface(낮은 하한/순위 표면)를 no-selection negative memory(선택 없음 부정 기억)로 닫고 Stage364(364단계)를 열었다.

Effect(효과): 다음 작업은 `{NEXT_STAGE_RUN_ID}`에서 timestamp-safe context/regime/label source(시점 안전 문맥/국면/라벨 원천) 설계 대기열 `{len(design_queue)}`개를 구체화한다.
""")
    append_text_once(WORKSPACE_CHANGELOG, "run363C_review_q05_lower_floor_rank_surface_without_db_v1", f"""## {TODAY} run363C Lower-Floor Rank Surface Review and Stage364 Branch(363C 낮은 하한 순위 표면 검토 및 364단계 분기)

Action(행동): Stage363B(363B 실행)의 passing_cross_split_rows(교차 분할 통과 행) `0` 결과를 검토하고 Stage364(364단계)를 열었다.

Effect(효과): current truth(현재 진실)는 `{NEXT_STAGE_ID}` / `{NEXT_STAGE_RUN_ID}`로 이동했고, 같은 threshold micro-tuning(임계값 미세조정)은 반복 금지로 기록됐다.
""")
    append_text_once(IDEA_REGISTRY, "IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY", f"""## IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY

- idea(아이디어): timestamp-safe source/regime/label context(시점 안전 원천/국면/라벨 문맥)로 q05 dense cost(q05 고밀도 비용)를 회복한다.
- source_failure_memory(원천 실패 기억): `{rel(FAILURE_MEMORY)}`.
- design_queue(설계 대기열): `{rel(NEXT_DESIGN_QUEUE)}`.
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`.
- claim_boundary(주장 경계): `{BRANCH_CLAIM_BOUNDARY}`.
""")
    append_text_once(NEGATIVE_RESULT_REGISTER, "FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF", f"""## {TODAY} FM-ST363C-LOWER-FLOOR-RANK-DENSITY-COST-TRADEOFF

- source_run(원천 실행): `{RUN_ID}`
- failure(실패): lower-floor/rank surface(낮은 하한/순위 표면)는 cost-positive sparse rows(비용 양수 희소 행)를 만들었지만 density >= 3(밀도 3 이상)을 동시에 만족하지 못했다.
- salvage_value(회수 가치): sparse cost-positive variants(희소 비용 양수 변형), open-hour clue(진입 시간 단서), dense control failure(고밀도 대조 실패).
- do_not_repeat(반복 금지): lower-floor/rank threshold micro-tuning(낮은 하한/순위 임계값 미세조정)을 후보 선택처럼 반복하지 않는다.
- reopen_condition(재개 조건): timestamp-safe context/regime/label source(시점 안전 문맥/국면/라벨 원천)가 density >= 3(밀도 3 이상)과 cost positive(비용 양수)를 같이 만든다.
- evidence(근거): `{rel(REVIEW_FINDINGS)}`.
""")


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage363/review_q05_lower_floor_rank_surface_and_branch_stage364_without_db.py"), "tracked", SOURCE_STAGE_ID, RUN_ID),
        ("review_report", REPORT_PATH, "tracked", SOURCE_STAGE_ID, RUN_ID),
        ("decision_doc", DECISION_DOC, "tracked", SOURCE_STAGE_ID, RUN_ID),
        ("stage364_report", NEXT_REPORT_PATH, "tracked", NEXT_STAGE_ID, NEXT_RUN_ID),
        ("stage364_stage_brief", NEXT_STAGE_BRIEF, "tracked", NEXT_STAGE_ID, NEXT_RUN_ID),
        ("stage364_input_manifest", NEXT_INPUT_MANIFEST, "tracked", NEXT_STAGE_ID, NEXT_RUN_ID),
        ("stage364_selection_status", NEXT_SELECTION_STATUS, "tracked", NEXT_STAGE_ID, NEXT_RUN_ID),
        ("review_findings", REVIEW_FINDINGS, "ignored_with_manifest", SOURCE_STAGE_ID, RUN_ID),
        ("failure_memory", FAILURE_MEMORY, "ignored_with_manifest", SOURCE_STAGE_ID, RUN_ID),
        ("stage364_design_queue", NEXT_DESIGN_QUEUE, "ignored_with_manifest", NEXT_STAGE_ID, NEXT_RUN_ID),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest", SOURCE_STAGE_ID, RUN_ID),
        ("stage364_final_decision", NEXT_FINAL_DECISION, "ignored_with_manifest", NEXT_STAGE_ID, NEXT_RUN_ID),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest", SOURCE_STAGE_ID, RUN_ID),
        ("stage364_gate_audit", NEXT_GATE_AUDIT, "ignored_with_manifest", NEXT_STAGE_ID, NEXT_RUN_ID),
    ]
    rows = []
    for artifact_type, path, availability, stage_id, run_id in artifacts:
        rows.append({
            "stage_id": stage_id,
            "run_id": run_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) and Path(path).is_file() else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": BRANCH_CLAIM_BOUNDARY if stage_id == NEXT_STAGE_ID else CLAIM_BOUNDARY,
            "artifact_id": f"{run_id}__{artifact_type}",
            "notes": f"Stage363C review and Stage364 branch artifact(363C 검토 및 364단계 분기 산출물); availability={availability}",
            "artifact_path": rel(path),
        })
    append_or_replace_csv(
        ARTIFACT_REGISTRY,
        ["stage_id", "run_id", "artifact_type", "path"],
        rows,
        extend_header=False,
    )


def refresh_gates_and_final() -> None:
    write_csv(GATE_AUDIT, gate_rows())
    write_csv(NEXT_GATE_AUDIT, branch_gate_rows())
    gates = gate_rows()
    branch_gates = branch_gate_rows()
    write_csv(GATE_AUDIT, gates)
    write_csv(NEXT_GATE_AUDIT, branch_gates)
    final = read_json(FINAL_DECISION)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    final["required_gate_coverage_audit"] = rel(GATE_AUDIT)
    write_json(FINAL_DECISION, final)
    next_final = read_json(NEXT_FINAL_DECISION)
    next_final["gate_passes"] = sum(1 for row in branch_gates if row["status"] == "passed")
    next_final["gate_total"] = len(branch_gates)
    next_final["required_gate_coverage_audit"] = rel(NEXT_GATE_AUDIT)
    write_json(NEXT_FINAL_DECISION, next_final)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("Missing required Stage363C inputs: " + ", ".join(missing))
    final = read_json(SOURCE_FINAL)
    if as_int(final.get("passing_cross_split_rows")) != 0:
        raise RuntimeError("Stage363C expects Stage363B passing_cross_split_rows == 0")
    if not source_gate_passed():
        raise RuntimeError("Stage363B source gate audit is not fully passed")


def main() -> None:
    validate_inputs()
    _, cross_rows = read_csv_rows(SOURCE_CROSS_SPLIT)
    final = read_json(SOURCE_FINAL)
    findings = build_findings(cross_rows, final)
    failure_memory = build_failure_memory()
    design_queue = build_stage364_design_queue()
    write_run_artifacts(findings, failure_memory, design_queue)
    write_reports(findings, design_queue)
    write_workspace_and_notes(design_queue)
    write_registries(findings, design_queue)
    refresh_gates_and_final()
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
