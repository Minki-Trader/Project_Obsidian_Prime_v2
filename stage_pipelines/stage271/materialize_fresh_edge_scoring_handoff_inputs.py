from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
RUN_ID = "run271C_materialize_fresh_edge_scoring_handoff_inputs_v1"
SOURCE_RUN_ID = "run271B_materialize_fresh_edge_rebuild_blueprints_v1"
NEXT_ACTION = "run271D_execute_fresh_edge_scoring_probe"
STATUS = "completed_fresh_edge_scoring_handoff_input_materialization_no_candidate_selection"
JUDGMENT = "exploratory_scoring_handoff_inputs_materialized_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
DATASET = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FORBIDDEN_PREFIXES = ("label", "future_")
METADATA_COLUMNS = {
    "timestamp",
    "symbol",
    "split",
    "split_id",
    "label",
    "label_id",
    "label_class",
    "future_timestamp",
    "future_log_return_12",
    "horizon_bars",
    "horizon_minutes",
}

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_ROOT / "02_runs" / "run271C"
HANDOFF_DIR = RUN_DIR / "handoff"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected"
RUN271B_DIR = STAGE_ROOT / "02_runs" / "run271B"
SOURCE_BLUEPRINTS = RUN271B_DIR / "fresh_edge_rebuild_blueprints.json"
SOURCE_SCORING_SURFACES = RUN271B_DIR / "scoring_surface_specs.json"
SOURCE_HANDOFF_SCHEMA = RUN271B_DIR / "adapter_handoff_schema.csv"
SOURCE_IDENTITY = RUN271B_DIR / "package_identity_receipts.csv"
SOURCE_FEATURE_ORDER_PLAN = RUN271B_DIR / "feature_order_plan.csv"
SOURCE_RISK_RECEIPT = RUN271B_DIR / "risk_logic_receipt.csv"
SOURCE_LINEAGE = RUN271B_DIR / "artifact_lineage_receipt.json"
SOURCE_REPORT = REVIEWS / "run271B_report.md"

DATASET_PROFILE = RUN_DIR / "dataset_profile.json"
SCORING_INPUT_SPECS = RUN_DIR / "scoring_input_specs.json"
SCORING_INPUT_SUMMARY = RUN_DIR / "scoring_input_summary.csv"
HANDOFF_INPUT_PLAN = RUN_DIR / "handoff_input_plan.csv"
THRESHOLD_POLICY_RECEIPT = RUN_DIR / "threshold_policy_receipt.csv"
PACKAGE_IDENTITY_RECEIPTS = RUN_DIR / "package_identity_receipts.csv"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
RUN_REPORT = REVIEWS / "run271C_report.md"
SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = Path("stage_pipelines/stage271/materialize_fresh_edge_scoring_handoff_inputs.py")

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
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
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


def json_load(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return dict(json.load(handle))


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def feature_columns(df: pd.DataFrame) -> list[str]:
    return [
        column
        for column in df.columns
        if column not in METADATA_COLUMNS and not any(column.startswith(prefix) for prefix in FORBIDDEN_PREFIXES)
    ]


def profile_dataset() -> dict[str, Any]:
    df = pd.read_parquet(io_path(DATASET))
    features = feature_columns(df)
    observed_hash = sha256_text("\n".join(features))
    if observed_hash != FEATURE_ORDER_HASH:
        raise ValueError(f"Feature order hash mismatch: {observed_hash} != {FEATURE_ORDER_HASH}")
    duplicate_timestamps = int(df["timestamp"].duplicated().sum()) if "timestamp" in df.columns else 0
    return {
        "dataset_path": rel(DATASET),
        "dataset_sha256": sha256_file(DATASET),
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "feature_count": len(features),
        "feature_order_hash": observed_hash,
        "timestamp_min": str(df["timestamp"].min()) if "timestamp" in df.columns else "",
        "timestamp_max": str(df["timestamp"].max()) if "timestamp" in df.columns else "",
        "duplicate_timestamps": duplicate_timestamps,
        "split_counts": {str(k): int(v) for k, v in df["split"].value_counts(dropna=False).to_dict().items()} if "split" in df.columns else {},
        "label_counts": {str(k): int(v) for k, v in df["label"].value_counts(dropna=False).to_dict().items()} if "label" in df.columns else {},
        "feature_columns": features,
        "metadata_columns": [column for column in df.columns if column not in features],
    }


def load_sources() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]], list[dict[str, str]]]:
    blueprints = json_load(SOURCE_BLUEPRINTS)
    scoring = json_load(SOURCE_SCORING_SURFACES)
    handoff = read_csv_rows(SOURCE_HANDOFF_SCHEMA)
    identity = read_csv_rows(SOURCE_IDENTITY)
    return blueprints, scoring, handoff, identity


def source_hashes(paths: Sequence[Path]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in paths:
        hashes[rel(path)] = sha256_file(path) if path.suffix == ".parquet" else sha256_file_lf_normalized(path)
    return hashes


def handoff_skeleton(package: Mapping[str, Any], identity: Mapping[str, str], handoff: Mapping[str, str]) -> dict[str, Any]:
    return {
        "package_id": package["package_id"],
        "package_role": package["package_role"],
        "feature_order_hash": FEATURE_ORDER_HASH,
        "blueprint_hash": identity["blueprint_hash"],
        "decision_rule_hash": identity["decision_rule_hash"],
        "risk_rule_hash": identity["risk_rule_hash"],
        "adapter_schema_hash": identity["adapter_schema_hash"],
        "score_columns_hash": identity["score_columns_hash"],
        "runtime_payload_fields": str(handoff["runtime_payload_fields"]).split(";"),
        "score_columns": package["score_columns"],
        "threshold_policy": "train_quantile_materialized_later_no_selection_in_run271C",
        "claim_boundary": BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
    }


def materialize_specs(scoring: Mapping[str, Any], handoff_rows: Sequence[Mapping[str, str]], identity_rows: Sequence[Mapping[str, str]], profile: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    identity_by_id = {row["package_id"]: dict(row) for row in identity_rows}
    handoff_by_id = {row["package_id"]: dict(row) for row in handoff_rows}
    specs = []
    summary_rows = []
    handoff_plan = []
    threshold_rows = []
    for package in scoring["packages"]:
        package_id = package["package_id"]
        identity = identity_by_id[package_id]
        handoff = handoff_by_id[package_id]
        skeleton = handoff_skeleton(package, identity, handoff)
        handoff_path = HANDOFF_DIR / f"{package_id}.json"
        write_json(handoff_path, skeleton)
        score_columns = list(package["score_columns"])
        specs.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "input_dataset": rel(DATASET),
                "row_count": profile["row_count"],
                "feature_order_hash": FEATURE_ORDER_HASH,
                "base_feature_columns": profile["feature_columns"],
                "score_columns": score_columns,
                "score_columns_hash": identity["score_columns_hash"],
                "decision_rule_hash": identity["decision_rule_hash"],
                "risk_rule_hash": identity["risk_rule_hash"],
                "adapter_schema_hash": identity["adapter_schema_hash"],
                "handoff_skeleton": rel(handoff_path),
                "threshold_policy": "derive quantiles on train split only in run271D; validation/oos are read-only evaluation splits",
                "claim_boundary": BOUNDARY,
            }
        )
        summary_rows.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "input_dataset": rel(DATASET),
                "row_count": profile["row_count"],
                "feature_count": profile["feature_count"],
                "score_column_count": len(score_columns),
                "feature_order_hash": FEATURE_ORDER_HASH,
                "score_columns_hash": identity["score_columns_hash"],
                "handoff_skeleton": rel(handoff_path),
                "materialization_status": "scoring_handoff_input_materialized_no_candidate_selection",
            }
        )
        handoff_plan.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "handoff_skeleton": rel(handoff_path),
                "runtime_payload_fields": handoff["runtime_payload_fields"],
                "required_hashes": handoff["required_hashes"],
                "next_consumer": NEXT_ACTION,
                "claim_boundary": BOUNDARY,
            }
        )
        threshold_rows.append(
            {
                "package_id": package_id,
                "threshold_owner": "run271D_execute_fresh_edge_scoring_probe",
                "threshold_policy": "train_split_quantiles_only_no_run271C_selection",
                "planned_thresholds": "p35;p50;p60;p65 depending on package decision rule",
                "validation_boundary": "validation and oos splits are read-only after train quantile materialization",
                "overfit_guard": "do not tune to Stage270 weak buckets without neutral-bucket check",
            }
        )
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "dataset_profile": rel(DATASET_PROFILE),
        "claim_boundary": BOUNDARY,
        "packages": specs,
    }
    return payload, summary_rows, handoff_plan, threshold_rows


def data_integrity_payload(profile: Mapping[str, Any], hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "data_source": rel(DATASET),
        "time_axis": "timestamp(타임스탬프)는 UTC closed M5 bar(UTC 닫힌 5분봉) 기준이며 run271C(271C 실행)는 새 라벨을 만들지 않는다",
        "sample_scope": "US100 M5(US100 5분봉), train/validation/oos(학습/검증/표본외), rows 46650",
        "missing_or_duplicate_check": f"duplicate_timestamps={profile['duplicate_timestamps']}",
        "feature_label_boundary": "score inputs use 58 feature columns only; label/future/split metadata are excluded from feature_order_hash",
        "split_boundary": "train split may define thresholds in run271D; validation/oos remain read-only",
        "leakage_risk": "future_log_return_12 and label columns exist for evaluation but are forbidden as score input features",
        "data_hash_or_identity": dict(hashes),
        "integrity_judgment": "usable_with_boundary",
    }


def model_validation_payload(profile: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "fresh rank/scoring surfaces, no trained model yet",
        "target_and_label": "existing label_v1_fwd12 3-class contract is present for evaluation, not for feature input",
        "split_method": f"train/validation/oos counts={profile['split_counts']}",
        "selection_metric": "none_selected; run271D may screen but cannot declare ONNX readiness",
        "secondary_metrics": "weak-slice damage, route counts, trade supply, risk action counts, feature/order hashes",
        "threshold_policy": "train quantile thresholds only; no threshold selected in run271C",
        "overfit_risk": "Stage270 weak-slice informed design; neutral-bucket and Tier A/B checks required",
        "calibration_risk": "scores are rank scores, not probability",
        "comparison_baseline": "run271B q01/q03 difference audit control and Stage270 failure memory",
        "validation_judgment": "exploratory_scoring_input_materialized_no_candidate_selection",
    }


def result_rows() -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "dataset_profile;scoring_input_specs;handoff_skeletons;threshold_policy_receipt;identity_receipts;ledgers",
            "evidence_missing": "actual score table;screening KPI;MT5 runtime output;Adapter package;ONNX export/parity;MT5 runtime reproduction",
            "judgment_label": "exploratory_input_materialization",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "점수/인계 입력은 만들어졌지만 선택 후보(selected candidate, 선택 후보)는 아직 없다.",
        }
    ]


def report_markdown(profile: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]]) -> str:
    package_lines = "\n".join(
        f"- `{row['package_id']}`: score columns(점수 열) `{row['score_column_count']}`, handoff skeleton(인계 골격) `{row['handoff_skeleton']}`"
        for row in summary_rows
    )
    return f"""# run271C Fresh Edge Scoring/Handoff Inputs(271C 새 거래 우위 점수/인계 입력)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- dataset_rows(데이터셋 행): `{profile['row_count']}`
- feature_count(피처 수): `{profile['feature_count']}`
- feature_order_hash(피처 순서 해시): `{profile['feature_order_hash']}`
- package_rows(패키지 행): `{len(summary_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Meaning(의미)

run271C(271C 실행)는 run271B(271B 실행)의 blueprint(청사진)를 scoring input spec(점수 입력 규격)과 handoff skeleton(인계 골격)으로 바꿨다.
효과(effect, 효과): 다음 run271D(271D 실행)는 feature order(피처 순서), score columns(점수 열), decision/risk hash(판단/위험 해시)를 잃지 않고 실제 score table(점수표)을 만들 수 있다.

## Packages(패키지)

{package_lines}

## Gate Coverage(게이트 커버리지)

- feature_order_parity(피처 순서 동등성): `{FEATURE_ORDER_HASH}`
- data_integrity_boundary(데이터 무결성 경계): `{rel(DATA_INTEGRITY_RECEIPT)}`
- model_validation_boundary(모델 검증 경계): `{rel(MODEL_VALIDATION_RECEIPT)}`
- artifact_lineage_audit(산출물 계보 감사): `{rel(ARTIFACT_LINEAGE_RECEIPT)}`
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
"""


def manifest_payload(profile: Mapping[str, Any], hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "producer": rel(ROOT / PRODUCER_PATH),
        "entry_command": f"python {PRODUCER_PATH.as_posix()}",
        "created_at_utc": utc_now(),
        "source_hashes": dict(hashes),
        "outputs": {
            "dataset_profile": rel(DATASET_PROFILE),
            "scoring_input_specs": rel(SCORING_INPUT_SPECS),
            "scoring_input_summary": rel(SCORING_INPUT_SUMMARY),
            "handoff_input_plan": rel(HANDOFF_INPUT_PLAN),
            "threshold_policy_receipt": rel(THRESHOLD_POLICY_RECEIPT),
            "package_identity_receipts": rel(PACKAGE_IDENTITY_RECEIPTS),
            "report": rel(RUN_REPORT),
        },
        "dataset_rows": profile["row_count"],
        "feature_count": profile["feature_count"],
        "feature_order_hash": profile["feature_order_hash"],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
        "next_action": NEXT_ACTION,
    }


def lineage_payload(paths: Sequence[Path], hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "source_inputs": dict(hashes),
        "producer": rel(ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)},
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_or_reproducible_from_command",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }


def write_selection_status() -> None:
    text = f"""# Stage271 Selection Status(271단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `stage271_fresh_edge_rebuild_after_nonfilter_failure_v1`
- current_run(현재 실행): `{RUN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- scoring_input_specs(점수 입력 규격): `{rel(SCORING_INPUT_SPECS)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

run271C(271C 실행)는 scoring input specs(점수 입력 규격)와 handoff skeletons(인계 골격)를 만들었다.
효과(effect, 효과): 아직 선택 후보가 아니라 run271D(271D 실행)에서 점수표(score table, 점수표)를 만들 수 있는 입력 정체성이 생긴 것이다.

## Boundary(경계)

`{BOUNDARY}`
"""
    write_md(SELECTION_STATUS, text)


def write_review_index() -> None:
    text = f"""# Stage271 Review Index(271단계 검토 색인)

## Current State(현재 상태)

Stage271(271단계)는 run271C(271C 실행) fresh edge scoring/handoff input materialization(새 거래 우위 점수/인계 입력 물질화)을 완료했다.
효과(effect, 효과): selected candidate(선택 후보) 없이 run271D(271D 실행) scoring probe(점수 탐침)로 넘어간다.

## Reports(보고)

- run271A report(271A 보고): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271A_report.md`
- run271B report(271B 보고): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271B_report.md`
- run271C report(271C 보고): `{rel(RUN_REPORT)}`
- run271C scoring input specs(271C 점수 입력 규격): `{rel(SCORING_INPUT_SPECS)}`
"""
    write_md(REVIEW_INDEX, text)


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


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_state_docs(profile: Mapping[str, Any]) -> None:
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `fresh_edge_scoring_handoff_inputs`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run271C_summary(271C 요약)",
        f"- run271C_summary(271C 요약): run271C(271C 실행)는 rows(행) `{profile['row_count']}`, feature_count(피처 수) `{profile['feature_count']}`, feature_order_hash(피처 순서 해시) `{profile['feature_order_hash']}`를 확인하고 scoring input specs(점수 입력 규격)와 handoff skeletons(인계 골격)를 만들었다. Effect(효과): run271D(271D 실행)가 점수표(score table, 점수표)를 만들 수 있지만, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage271(271단계) run271C(271C 실행) fresh edge scoring/handoff input materialization(새 거래 우위 점수/인계 입력 물질화) `{RUN_ID}`. "
        f"Effect(효과): dataset rows(데이터셋 행) `{profile['row_count']}`, feature_count(피처 수) `{profile['feature_count']}`, feature_order_hash(피처 순서 해시) `{profile['feature_order_hash']}`를 확인했고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run271C scoring/handoff inputs(271C 점수/인계 입력)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): feature order hash(피처 순서 해시)를 확인하고 scoring input specs(점수 입력 규격)와 handoff skeletons(인계 골격)를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def update_registers(created_at: str, artifacts: Sequence[Path], profile: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]]) -> None:
    package_count = len(summary_rows)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"package_rows={package_count};dataset_rows={profile['row_count']};feature_count={profile['feature_count']};selected_candidate=none;onnx_readiness=not_claimed.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_input",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_input",
            "parent_run_id": "",
            "record_view": "Tier A scoring input(티어 A 점수 입력)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "input_materialization",
            "scoreboard_lane": "fresh_edge_scoring_handoff_inputs",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(SCORING_INPUT_SPECS),
            "primary_kpi": f"dataset_rows={profile['row_count']};feature_count={profile['feature_count']};package_rows={package_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_input_only",
            "notes": "Tier A scoring input materialized; no score table yet.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_input",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_input",
            "parent_run_id": "",
            "record_view": "Tier B scoring input(티어 B 점수 입력)",
            "tier_scope": "Tier B separate",
            "kpi_scope": "input_materialization",
            "scoreboard_lane": "fresh_edge_scoring_handoff_inputs",
            "status": STATUS,
            "judgment": "planned_with_boundary_no_authority",
            "path": rel(DATA_INTEGRITY_RECEIPT),
            "primary_kpi": "tier_b_input=planned",
            "guardrail_kpi": "no_fallback_authority_claimed",
            "external_verification_status": "out_of_scope_by_claim_input_only",
            "notes": "Tier B scoring input remains separate until actual routed record exists.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_input",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_ab_input",
            "parent_run_id": "",
            "record_view": "Tier A+B scoring input(티어 A+B 점수 입력)",
            "tier_scope": "Tier A+B combined",
            "kpi_scope": "input_materialization",
            "scoreboard_lane": "fresh_edge_scoring_handoff_inputs",
            "status": STATUS,
            "judgment": "planned_combined_record_no_performance_claim",
            "path": rel(SCORING_INPUT_SPECS),
            "primary_kpi": "combined_input=planned",
            "guardrail_kpi": "performance_claim=none",
            "external_verification_status": "out_of_scope_by_claim_input_only",
            "notes": "Combined input is a future record requirement, not performance.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_edge_scoring_handoff_input_materialization",
                "tier_scope": "Tier A+B paired input",
                "scoreboard": "input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "input_only_no_score_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"package_rows={package_count};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    if path_exists(ARTIFACT_REGISTRY):
        existing = [row for row in read_csv_rows(ARTIFACT_REGISTRY) if str(row.get("run_id", "")).strip() != RUN_ID]
        write_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, existing)
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run271C_scoring_handoff_input_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run271C fresh edge scoring/handoff input artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def run() -> dict[str, Any]:
    sources = [
        DATASET,
        SOURCE_BLUEPRINTS,
        SOURCE_SCORING_SURFACES,
        SOURCE_HANDOFF_SCHEMA,
        SOURCE_IDENTITY,
        SOURCE_FEATURE_ORDER_PLAN,
        SOURCE_RISK_RECEIPT,
        SOURCE_LINEAGE,
        SOURCE_REPORT,
    ]
    must_exist(sources)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(HANDOFF_DIR).mkdir(parents=True, exist_ok=True)
    profile = profile_dataset()
    blueprints, scoring, handoff_rows, identity_rows = load_sources()
    specs, summary_rows, handoff_plan, threshold_rows = materialize_specs(scoring, handoff_rows, identity_rows, profile)
    hashes = source_hashes(sources)
    identity_out = []
    by_id = {row["package_id"]: row for row in identity_rows}
    for row in summary_rows:
        source = by_id[row["package_id"]]
        handoff_hash = sha256_file_lf_normalized(ROOT / row["handoff_skeleton"])
        identity_out.append({**source, "handoff_skeleton_hash": handoff_hash, "identity_judgment": "scoring_handoff_input_materialized_no_performance_claim"})

    write_json(DATASET_PROFILE, profile)
    write_json(SCORING_INPUT_SPECS, specs)
    write_csv(
        SCORING_INPUT_SUMMARY,
        ("package_id", "package_role", "input_dataset", "row_count", "feature_count", "score_column_count", "feature_order_hash", "score_columns_hash", "handoff_skeleton", "materialization_status"),
        summary_rows,
    )
    write_csv(
        HANDOFF_INPUT_PLAN,
        ("package_id", "package_role", "handoff_skeleton", "runtime_payload_fields", "required_hashes", "next_consumer", "claim_boundary"),
        handoff_plan,
    )
    write_csv(
        THRESHOLD_POLICY_RECEIPT,
        ("package_id", "threshold_owner", "threshold_policy", "planned_thresholds", "validation_boundary", "overfit_guard"),
        threshold_rows,
    )
    write_csv(
        PACKAGE_IDENTITY_RECEIPTS,
        ("package_id", "package_role", "feature_order_hash", "blueprint_hash", "decision_rule_hash", "risk_rule_hash", "adapter_schema_hash", "score_columns_hash", "handoff_skeleton_hash", "identity_judgment"),
        identity_out,
    )
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_payload(profile, hashes))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_payload(profile))
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows())
    write_json(RUN_MANIFEST, manifest_payload(profile, hashes))
    write_md(RUN_REPORT, report_markdown(profile, summary_rows))
    write_selection_status()
    write_review_index()
    artifacts = [
        RUN_MANIFEST,
        DATASET_PROFILE,
        SCORING_INPUT_SPECS,
        SCORING_INPUT_SUMMARY,
        HANDOFF_INPUT_PLAN,
        THRESHOLD_POLICY_RECEIPT,
        PACKAGE_IDENTITY_RECEIPTS,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        *sorted(HANDOFF_DIR.glob("*.json")),
        RUN_REPORT,
        SELECTION_STATUS,
        REVIEW_INDEX,
    ]
    write_json(ARTIFACT_LINEAGE_RECEIPT, lineage_payload([*artifacts, ARTIFACT_LINEAGE_RECEIPT], hashes))
    artifacts.append(ARTIFACT_LINEAGE_RECEIPT)
    created_at = utc_now()
    update_registers(created_at, artifacts, profile, summary_rows)
    update_state_docs(profile)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "dataset_rows": profile["row_count"],
        "feature_count": profile["feature_count"],
        "feature_order_hash": profile["feature_order_hash"],
        "package_rows": len(summary_rows),
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
