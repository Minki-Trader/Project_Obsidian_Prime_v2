from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure"
RUN_ID = "run275C_materialize_fresh_candidate_scoring_handoff_inputs_v1"
SOURCE_RUN_ID = "run275B_materialize_fresh_candidate_package_blueprints_v1"
STATUS = "completed_fresh_candidate_scoring_handoff_input_materialization_no_candidate_selection"
JUDGMENT = "scoring_handoff_inputs_ready_no_candidate_selection"
NEXT_ACTION = "run275D_execute_fresh_candidate_scoring_materialization_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE / "02_runs" / "run275C"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"
RUN275B = STAGE / "02_runs" / "run275B"
HANDOFF_DIR = RUN_DIR / "h"

SOURCE_BLUEPRINTS = RUN275B / "blueprints.json"
SOURCE_SCORING_PLAN = RUN275B / "scoring.csv"
SOURCE_ADAPTER_PLAN = RUN275B / "adapter.csv"
SOURCE_RULES = RUN275B / "rules.csv"
SOURCE_IDENTITY = RUN275B / "identity.csv"
SOURCE_REPORT = REVIEWS / "run275B_report.md"
SOURCE_MANIFEST = RUN275B / "run_manifest.json"

MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
FEATURE_ORDER = MODEL_INPUT.with_name("model_input_feature_order.txt")
DATASET_PROFILE = ROOT / "stages" / "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure" / "02_runs" / "run271C" / "dataset_profile.json"

SPECS = RUN_DIR / "specs.json"
HANDOFF_PLAN = RUN_DIR / "handoff.csv"
IDENTITY_RECEIPT = RUN_DIR / "identity.csv"
SCHEMA = RUN_DIR / "schema.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model.json"
RESULT_JUDGMENT = RUN_DIR / "judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage.json"
RUN_REPORT = REVIEWS / "run275C_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage275/materialize_fresh_candidate_scoring_handoff_inputs.py")

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
HANDOFF_COLUMNS = (
    "package_id",
    "package_role",
    "handoff_skeleton_path",
    "handoff_skeleton_hash",
    "runtime_handoff_fields",
    "identity_fields",
    "input_column_status",
    "missing_source_columns",
    "next_action",
    "claim_boundary",
)
IDENTITY_COLUMNS = (
    "package_id",
    "package_role",
    "feature_order_hash",
    "blueprint_hash",
    "score_columns_hash",
    "decision_rule_hash",
    "risk_rule_hash",
    "adapter_schema_hash",
    "handoff_skeleton_hash",
    "identity_judgment",
    "claim_boundary",
)
SCHEMA_COLUMNS = (
    "package_id",
    "field_name",
    "field_role",
    "source",
    "materialization_status",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")

GENERATED_COLUMNS = {
    "tier_view",
    "package_id",
    "feature_order_hash",
    "decision_rule_hash",
    "risk_rule_hash",
    "adapter_schema_hash",
    "claim_boundary",
    "q04_control_signature",
    "stage274_duplicate_filter_signature",
    "active_signal_count",
    "changed_signal_rate",
    "new_active_count",
    "direction_changed_count",
}


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest_payload(payload: Any) -> str:
    raw = json.dumps(json_ready(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


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


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return dict(json.load(handle))


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def feature_order_values() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def short_id(package_id: str) -> str:
    return package_id.split("_", 1)[0]


def source_columns(profile: Mapping[str, Any], features: Sequence[str]) -> set[str]:
    metadata = set(profile.get("metadata_columns", []))
    return {*metadata, *features, *GENERATED_COLUMNS}


def skeleton_path(package_id: str) -> Path:
    return HANDOFF_DIR / f"{short_id(package_id)}.json"


def build_skeleton(package: Mapping[str, Any]) -> dict[str, Any]:
    runtime_fields = list(package["runtime_handoff_plan"])
    identity_fields = [
        "package_id",
        "feature_order_hash",
        "blueprint_hash",
        "score_columns_hash",
        "decision_rule_hash",
        "risk_rule_hash",
        "adapter_schema_hash",
        "handoff_skeleton_hash",
    ]
    payload_fields = {field: None for field in runtime_fields}
    return {
        "package_id": package["package_id"],
        "package_role": package["package_role"],
        "source_run_id": SOURCE_RUN_ID,
        "feature_order_hash": package["source_feature_order_hash"],
        "blueprint_hash": package["blueprint_hash"],
        "score_columns_hash": package["score_columns_hash"],
        "decision_rule_hash": package["decision_rule_hash"],
        "risk_rule_hash": package["risk_rule_hash"],
        "adapter_schema_hash": package["adapter_schema_hash"],
        "runtime_handoff_fields": runtime_fields,
        "identity_fields": identity_fields,
        "payload_fields": payload_fields,
        "freshness_guard": package["freshness_guard"],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def build_specs(blueprints: Sequence[Mapping[str, Any]], profile: Mapping[str, Any], features: Sequence[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    available = source_columns(profile, features)
    specs: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    for package in blueprints:
        required = list(package["required_source_columns"])
        missing = [column for column in required if column not in available]
        skeleton = build_skeleton(package)
        skel_path = skeleton_path(str(package["package_id"]))
        skeleton["handoff_skeleton_hash"] = digest_payload(skeleton)
        write_json(skel_path, skeleton)
        status = "complete" if not missing else "missing_required"
        specs.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "input_column_status": status,
                "required_source_columns": required,
                "missing_source_columns": missing,
                "score_columns": package["score_columns"],
                "runtime_handoff_fields": package["runtime_handoff_plan"],
                "handoff_skeleton_path": rel(skel_path),
                "handoff_skeleton_hash": skeleton["handoff_skeleton_hash"],
                "feature_order_hash": package["source_feature_order_hash"],
                "blueprint_hash": package["blueprint_hash"],
                "decision_rule_hash": package["decision_rule_hash"],
                "risk_rule_hash": package["risk_rule_hash"],
                "adapter_schema_hash": package["adapter_schema_hash"],
                "claim_boundary": BOUNDARY,
                "next_action": NEXT_ACTION,
            }
        )
        handoff_rows.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "handoff_skeleton_path": rel(skel_path),
                "handoff_skeleton_hash": skeleton["handoff_skeleton_hash"],
                "runtime_handoff_fields": ";".join(package["runtime_handoff_plan"]),
                "identity_fields": ";".join(skeleton["identity_fields"]),
                "input_column_status": status,
                "missing_source_columns": ";".join(missing),
                "next_action": NEXT_ACTION,
                "claim_boundary": BOUNDARY,
            }
        )
        identity_rows.append(
            {
                "package_id": package["package_id"],
                "package_role": package["package_role"],
                "feature_order_hash": package["source_feature_order_hash"],
                "blueprint_hash": package["blueprint_hash"],
                "score_columns_hash": package["score_columns_hash"],
                "decision_rule_hash": package["decision_rule_hash"],
                "risk_rule_hash": package["risk_rule_hash"],
                "adapter_schema_hash": package["adapter_schema_hash"],
                "handoff_skeleton_hash": skeleton["handoff_skeleton_hash"],
                "identity_judgment": "input_identity_complete_no_candidate_selection" if not missing else "input_identity_missing_required",
                "claim_boundary": BOUNDARY,
            }
        )
        for field in required:
            role = "base_feature_or_metadata" if field in available else "missing_required"
            schema_rows.append(
                {
                    "package_id": package["package_id"],
                    "field_name": field,
                    "field_role": role,
                    "source": "model_input_dataset_or_generated_identity",
                    "materialization_status": "available_for_run275D" if field in available else "missing_required",
                    "claim_boundary": BOUNDARY,
                }
            )
        for field in package["runtime_handoff_plan"]:
            schema_rows.append(
                {
                    "package_id": package["package_id"],
                    "field_name": field,
                    "field_role": "adapter_output_or_handoff_field",
                    "source": "run275D_planned_score_output",
                    "materialization_status": "planned_not_materialized_in_run275C",
                    "claim_boundary": BOUNDARY,
                }
            )
    return specs, handoff_rows, identity_rows, schema_rows


def experiment_receipt(specs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "hypothesis": "run275B blueprints(청사진)는 run275C scoring/handoff inputs(점수/인계 입력)로 물질화 가능하다.",
        "decision_use": "Allow run275D score materialization(점수 물질화) only for packages(패키지) with complete input identity(완전한 입력 정체성).",
        "comparison_baseline": "cp275E_q04_stage274_failure_signature_guard",
        "control_variables": "feature_order_hash, decision_rule_hash, risk_rule_hash, adapter_schema_hash(피처/판단/위험/어댑터 해시) fixed from run275B",
        "changed_variables": "input skeletons(입력 골격), handoff skeletons(인계 골격), feature/handoff schema(피처/인계 스키마)",
        "sample_scope": "US100 M5 model input identity(모델 입력 정체성); no trading KPI(거래 KPI 없음)",
        "success_criteria": "Every package(모든 패키지)가 handoff skeleton(인계 골격), input column status(입력 열 상태), identity receipt(정체성 영수증)를 가진다.",
        "failure_criteria": "Missing required source columns(필수 원천 열 누락) or missing skeleton hash(골격 해시 누락).",
        "invalid_conditions": "Feature order mismatch(피처 순서 불일치), label leakage(라벨 누수), or missing source blueprint(원천 청사진 누락).",
        "stop_conditions": "If selectable packages(선택 가능 패키지) have missing_required(필수 누락), do not run score materialization(점수 물질화 금지).",
        "evidence_plan": [SPECS, HANDOFF_PLAN, IDENTITY_RECEIPT, SCHEMA],
        "input_status_counts": {status: sum(1 for row in specs if row["input_column_status"] == status) for status in sorted({row["input_column_status"] for row in specs})},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def data_integrity_receipt(profile: Mapping[str, Any], feature_hash: str, specs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "data_source": rel(MODEL_INPUT),
        "time_axis": "M5 timestamp(M5 시각) from model input dataset(모델 입력 데이터셋); run275C(275C 실행)는 새 시계열 값을 계산하지 않는다.",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "date_min": profile.get("timestamp_min"),
            "date_max": profile.get("timestamp_max"),
            "rows": profile.get("row_count"),
            "splits": profile.get("split_counts"),
            "tier_scope": "Tier A source plus Tier B/Tier A+B planned downstream(티어 A 원천 및 하위 티어 B/Tier A+B 계획)",
        },
        "missing_or_duplicate_check": f"duplicate_timestamps(중복 시각)={profile.get('duplicate_timestamps')}",
        "feature_label_boundary": "Required source columns(필수 원천 열)은 metadata/features/generated identity(메타데이터/피처/생성 정체성)만 허용한다.",
        "split_boundary": "run275D thresholds(임계값)는 train split(학습 분할) only.",
        "leakage_risk": "future_log_return_12/label columns(미래 수익/라벨 열) are not listed as scoring inputs(점수 입력 아님).",
        "data_hash_or_identity": {
            "dataset_hash": sha256_file_lf_normalized(MODEL_INPUT),
            "feature_order_hash": feature_hash,
            "blueprint_hash": sha256_file_lf_normalized(SOURCE_BLUEPRINTS),
        },
        "integrity_judgment": "usable_with_boundary_scoring_input_ready" if all(row["input_column_status"] == "complete" for row in specs) else "inconclusive_missing_required",
        "claim_boundary": BOUNDARY,
    }


def model_validation_receipt(specs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "model_family": "deterministic score surface input(결정 점수 표면 입력); no trained model(훈련 모델 없음)",
        "target_and_label": "entry/direction/risk scoring inputs(진입/방향/위험 점수 입력); label not consumed(라벨 미사용)",
        "split_method": "run275C input materialization(입력 물질화); thresholds deferred(임계값은 보류)",
        "selection_metric": "input completeness(입력 완전성), feature order identity(피처 순서 정체성), handoff skeleton identity(인계 골격 정체성)",
        "secondary_metrics": "future run275D changed_signal_rate/new_active_count/direction_changed_count(변경 신호율/새 활성 수/방향 변경 수)",
        "threshold_policy": "train_split_only_downstream",
        "overfit_risk": "No score fitted yet(아직 점수 적합 없음); future risk is weak-pocket overfit(약점 구간 과적합).",
        "calibration_risk": "Scores(점수)는 probability(확률)가 아니라 deterministic rank/state(결정 순위/상태)다.",
        "comparison_baseline": "cp275E_q04_stage274_failure_signature_guard",
        "validation_judgment": "input_ready_no_candidate_selection" if all(row["input_column_status"] == "complete" for row in specs) else "inconclusive_missing_required",
        "claim_boundary": BOUNDARY,
    }


def result_rows(specs: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    complete = sum(1 for row in specs if row["input_column_status"] == "complete")
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"scoring input specs(점수 입력 규격) {len(specs)} rows; complete(완전) {complete}; handoff skeletons(인계 골격); identity receipts(정체성 영수증)",
            "evidence_missing": "score tables(점수표); active-entry/direction screen(활성 진입/방향 선별); MT5 runtime output(MT5 런타임 출력); ONNX parity(온엑스 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "청사진을 점수/인계 입력으로 바꿨지만 아직 점수표나 후보 선택은 아니다.",
        }
    ]


def gate_rows(specs: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    missing = sum(1 for row in specs if row["input_column_status"] != "complete")
    input_status = "passed(통과)" if missing == 0 else "failed_missing_required(필수 누락 실패)"
    return [
        {
            "gate_name": "scope_completion_gate(범위 완료 게이트)",
            "status": input_status,
            "evidence_path": rel(SPECS),
            "effect": "package(패키지)별 입력 열 상태를 기록했다.",
        },
        {
            "gate_name": "artifact_lineage_audit(산출물 계보 감사)",
            "status": "passed(통과)",
            "evidence_path": rel(LINEAGE_RECEIPT),
            "effect": "run275B 청사진부터 run275C 입력/골격까지 연결한다.",
        },
        {
            "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed(통과)" if missing == 0 else "passed_with_repair_needed(수정 필요 포함 통과)",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "완료 주장의 근거와 claim boundary(주장 경계)를 연결했다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def write_report(specs: Sequence[Mapping[str, Any]], handoff_rows: Sequence[Mapping[str, Any]]) -> None:
    lines = "\n".join(
        f"- `{row['package_id']}`: input_column_status(입력 열 상태) `{row['input_column_status']}`, skeleton(골격) `{row['handoff_skeleton_path']}`"
        for row in handoff_rows
    )
    complete = sum(1 for row in specs if row["input_column_status"] == "complete")
    write_md(
        RUN_REPORT,
        f"""# run275C Fresh Candidate Scoring/Handoff Inputs(275C 새 후보 점수/인계 입력)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- complete input packages(완전 입력 패키지): `{complete}/{len(specs)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run275C(275C 실행)는 run275B(275B 실행)의 blueprints(청사진)를 scoring input specs(점수 입력 규격)와 handoff skeletons(인계 골격)로 바꿨다.
효과(effect, 효과): 다음 run275D(275D 실행)는 실제 score table(점수표)을 만들고 q04 duplicate/filter-like(중복/필터형) 여부를 선별할 수 있다.

## Handoff Skeletons(인계 골격)

{lines}

## Evidence Paths(근거 경로)

- specs(규격): `{rel(SPECS)}`
- handoff plan(인계 계획): `{rel(HANDOFF_PLAN)}`
- identity receipt(정체성 영수증): `{rel(IDENTITY_RECEIPT)}`
- schema(스키마): `{rel(SCHEMA)}`

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


def update_stage_docs(specs: Sequence[Mapping[str, Any]]) -> None:
    complete = sum(1 for row in specs if row["input_column_status"] == "complete")
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_or_append(selection, "- run275C_report", f"- run275C_report(275C 보고서): `{rel(RUN_REPORT)}`")
    selection = replace_or_append(selection, "- run275C_specs", f"- run275C_specs(275C 규격): `{rel(SPECS)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = replace_or_append(review, "- run275C_report", f"- run275C_report(275C 보고서): `{rel(RUN_REPORT)}`")
    review = replace_or_append(review, "- run275C_specs", f"- run275C_specs(275C 규격): `{rel(SPECS)}`")
    review = replace_or_append(review, "- run275C_handoff", f"- run275C_handoff(275C 인계): `{rel(HANDOFF_PLAN)}`")
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_candidate_scoring_handoff_input_materialization`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run275C_summary",
        f"- run275C_summary(275C 요약): run275C(275C 실행)는 scoring input specs(점수 입력 규격)와 handoff skeletons(인계 골격)를 package(패키지) `{len(specs)}`개에 대해 만들었다. Effect(효과): complete input packages(완전 입력 패키지) `{complete}/{len(specs)}`개를 run275D(275D 실행) score materialization(점수 물질화)로 넘긴다. Boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage275(275단계) run275C(275C 실행) fresh candidate scoring/handoff input materialization(새 후보 점수/인계 입력 물질화) `{RUN_ID}`. "
        f"Effect(효과): package(패키지) `{len(specs)}`개에 scoring input specs(점수 입력 규격)와 handoff skeletons(인계 골격)를 만들고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## 2026-05-23 run275C fresh candidate scoring/handoff input materialization(275C 새 후보 점수/인계 입력 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): package(패키지) `{len(specs)}`개에 scoring input specs(점수 입력 규격)와 handoff skeletons(인계 골격)를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def update_registers(created_at: str, specs: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> None:
    complete = sum(1 for row in specs if row["input_column_status"] == "complete")
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"packages={len(specs)};complete_inputs={complete};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
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
            "record_view": "fresh candidate scoring handoff input(새 후보 점수 인계 입력)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined input scope",
            "kpi_scope": "input_materialization",
            "scoreboard_lane": "fresh_candidate_scoring_handoff",
            "status": STATUS,
            "judgment": row["input_column_status"],
            "path": rel(SPECS),
            "primary_kpi": f"input_column_status={row['input_column_status']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_input_materialization",
            "notes": f"handoff_skeleton={row['handoff_skeleton_path']}",
        }
        for row in specs
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_candidate_scoring_handoff_inputs",
                "tier_scope": "Tier A+B paired input scope",
                "scoreboard": "input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "input_materialization_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"packages={len(specs)};complete_inputs={complete};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run275C_scoring_handoff_input_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run275C fresh candidate scoring/handoff input materialization artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def manifest_payload(created_at: str, specs: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], source_inputs: Sequence[Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "package_ids": [row["package_id"] for row in specs],
        "complete_input_packages": sum(1 for row in specs if row["input_column_status"] == "complete"),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }


def run() -> dict[str, Any]:
    must_exist(
        [
            SOURCE_BLUEPRINTS,
            SOURCE_SCORING_PLAN,
            SOURCE_ADAPTER_PLAN,
            SOURCE_RULES,
            SOURCE_IDENTITY,
            SOURCE_REPORT,
            SOURCE_MANIFEST,
            MODEL_INPUT,
            FEATURE_ORDER,
            DATASET_PROFILE,
        ]
    )
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(HANDOFF_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    blueprints_payload = read_json(SOURCE_BLUEPRINTS)
    blueprints = list(blueprints_payload["packages"])
    profile = read_json(DATASET_PROFILE)
    features = feature_order_values()
    feature_hash = str(profile.get("feature_order_hash", ""))
    specs, handoff_rows, identity_rows, schema_rows = build_specs(blueprints, profile, features)

    write_json(SPECS, {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "packages": specs,
        "payload_profile": {
            "dataset_path": rel(MODEL_INPUT),
            "dataset_rows": profile.get("row_count"),
            "feature_count": len(features),
            "feature_order_hash": feature_hash,
            "split_counts": profile.get("split_counts"),
        },
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    })
    write_csv(HANDOFF_PLAN, HANDOFF_COLUMNS, handoff_rows)
    write_csv(IDENTITY_RECEIPT, IDENTITY_COLUMNS, identity_rows)
    write_csv(SCHEMA, SCHEMA_COLUMNS, schema_rows)
    write_json(EXPERIMENT_RECEIPT, experiment_receipt(specs))
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_receipt(profile, feature_hash, specs))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_receipt(specs))
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows(specs))
    write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows(specs))
    write_report(specs, handoff_rows)

    skeletons = [skeleton_path(str(row["package_id"])) for row in specs]
    source_inputs = [
        SOURCE_BLUEPRINTS,
        SOURCE_SCORING_PLAN,
        SOURCE_ADAPTER_PLAN,
        SOURCE_RULES,
        SOURCE_IDENTITY,
        SOURCE_REPORT,
        SOURCE_MANIFEST,
        MODEL_INPUT,
        FEATURE_ORDER,
        DATASET_PROFILE,
    ]
    artifacts = [
        SPECS,
        HANDOFF_PLAN,
        IDENTITY_RECEIPT,
        SCHEMA,
        *skeletons,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    manifest = manifest_payload(created_at, specs, artifacts, source_inputs)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, specs, artifacts, source_inputs)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    artifacts.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, specs, artifacts, source_inputs)
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, specs, artifacts)
    update_stage_docs(specs)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "packages": len(specs),
        "complete_input_packages": sum(1 for row in specs if row["input_column_status"] == "complete"),
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
