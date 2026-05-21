from __future__ import annotations

import csv
import json
import math
import re
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import (
    run267BC_materialize_adjacent_period_replacement_frames as period_tools,
)
from stage_pipelines.stage267 import (
    run267BJ_aggressive_pressure_first_tranche_materialization as source_first_tranche,
)
from stage_pipelines.stage267 import (
    run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design as source_design,
)
from stage_pipelines.stage267 import (
    run267K_retrained_soft_context_adapter_materialization as source_retrain,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267BN"
RUN_ID = "run267BN_stage267_aggressive_second_tranche_cross_period_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_FIRST_TRANCHE_RUN_ID = source_first_tranche.RUN_ID
STATUS = "run267BN_aggressive_second_tranche_cross_period_materialized_execution_pending"
JUDGMENT = "aggressive_second_tranche_cross_period_materialized_no_candidate_selection"
NEXT_ACTION = "run267BO_execute_aggressive_second_tranche_cross_period_mt5"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_second_tranche_cross_period_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"

SOURCE_QUEUE_PATH = source_design.SECOND_TRANCHE_QUEUE_PATH
SOURCE_FIRST_TRANCHE_VARIANT_MANIFEST_PATH = source_first_tranche.VARIANT_MANIFEST_PATH
SOURCE_FIRST_TRANCHE_ATTEMPT_MANIFEST_PATH = source_first_tranche.ATTEMPT_MANIFEST_PATH

QUEUE_DECISION_PATH = RUN_ROOT / "second_tranche_queue_decision.csv"
PERIOD_AVAILABILITY_PATH = RUN_ROOT / "adjacent_period_source_availability.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
FAILURE_MEMORY_SEED_PATH = RUN_ROOT / "failure_memory_seed.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BN_aggressive_second_tranche_cross_period_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BN_aggressive_second_tranche_cross_period_materialization.py")

STAGE_LEDGER_PATH = source_design.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_design.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_design.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_design.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_design.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_design.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_design.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_design.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_design.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_design.ARTIFACT_COLUMNS

SHORT_COMMON_ROOT = "OPV2/s267bn"
WATCH_ALIAS = "s264_aih"
TIER_PAIR_BOUNDARY = "Tier_B_and_actual_routed_total_blocked_until_true_fallback_manifest_exists"
MATERIALIZATION_BOUNDARY = "aggressive_second_tranche_cross_period_from_run267BJ_first_tranche_assets"

PERIOD_BY_TARGET = {
    "2023H2": "adjacent_2023_h2_train_pre_2024",
    "2025H1": "adjacent_2025_h1_validation_post_2024",
    "2025H2": "adjacent_2025_h2_oos_followthrough",
}

MATERIALIZABLE_SCOPE_MARKERS = (
    "direct_mt5_attempt_ready",
    "control_mt5_attempt_ready",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def safe_token(value: str, limit: int = 80) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower()
    return token[:limit] or "item"


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}" if math.isfinite(value) else ""
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered or ("status", "notes"))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def parse_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line or line.startswith("["):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run267BN_aggressive_second_tranche_cross_period_materialization"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "mt5_tester_ini",
        "tester": dict(values),
    }


def feature_order_from_runtime_csv(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    if not header or header[0] != "bar_time_server":
        raise RuntimeError(f"unexpected runtime feature header: {rel(path)}")
    return list(header[1:])


def source_feature_path(attempt_name: str) -> Path:
    return (
        source_first_tranche.VARIANT_ROOT
        / WATCH_ALIAS
        / attempt_name
        / "features"
        / f"{attempt_name}_features.csv"
    )


def source_model_path(attempt_name: str) -> Path:
    return (
        source_first_tranche.VARIANT_ROOT
        / WATCH_ALIAS
        / attempt_name
        / "models"
        / f"{attempt_name}_model.csv"
    )


def spec_for_watch_alias() -> Any:
    specs = {spec.alias: spec for spec in input_probe.candidate_specs()}
    return specs[WATCH_ALIAS]


def first_tranche_sources() -> dict[str, dict[str, Any]]:
    variants = read_csv(SOURCE_FIRST_TRANCHE_VARIANT_MANIFEST_PATH)
    attempts = read_csv(SOURCE_FIRST_TRANCHE_ATTEMPT_MANIFEST_PATH)
    attempts_by_name = {str(row["attempt_name"]): row for row in attempts}
    output: dict[str, dict[str, Any]] = {}
    for variant in variants:
        variant_id = str(variant["variant_id"])
        attempt_name = str(variant["attempt_name"])
        attempt = attempts_by_name.get(attempt_name)
        if not attempt:
            raise RuntimeError(f"missing first tranche attempt row for {attempt_name}")
        output[variant_id] = {"variant": variant, "attempt": attempt}
    return output


def is_materializable(row: Mapping[str, str]) -> bool:
    scope = str(row.get("materialization_scope", ""))
    return any(marker in scope for marker in MATERIALIZABLE_SCOPE_MARKERS)


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        scope = str(row.get("materialization_scope", ""))
        if "source_surface_needed_before_mt5" in scope:
            decision = "blocked_source_surface_needed_before_mt5"
            effect = "similar replacement(유사 대체)은 feature surface(피처 표면)를 먼저 만들어야 한다."
        elif "audit_before_more_mt5" in scope:
            decision = "audit_only_not_materialized"
            effect = "explode branch(기회 확장 분기)는 깊은 hole(구멍) 감사를 먼저 한다."
        elif is_materializable(row):
            decision = "materialized_execution_pending"
            effect = "다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 기간 취약성을 확인한다."
        else:
            decision = "not_materialized_unrecognized_scope"
            effect = "scope(범위)가 명확하지 않아 실행 입력으로 만들지 않는다."
        rows.append(
            {
                "queue_id": row.get("queue_id"),
                "priority": row.get("priority"),
                "materialization_scope": scope,
                "candidate_alias": row.get("candidate_alias"),
                "source_variant_id": row.get("source_variant_id"),
                "target_period": row.get("target_period"),
                "target_split": row.get("target_split"),
                "run267BN_decision": decision,
                "effect": effect,
                "claim_boundary": "no_selection_no_onnx_no_goal_achieve",
            }
        )
    return rows


def period_lookup(period_rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row["period_id"]): row for row in period_rows}


def copy_model_to_variant(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(rel(source))
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def materialize_attempt(
    row: Mapping[str, str],
    source_entry: Mapping[str, Any],
    frames: Mapping[str, pd.DataFrame],
    period_by_id: Mapping[str, Mapping[str, Any]],
    spec: Any,
    *,
    order: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    variant_id = str(row["source_variant_id"])
    target_period = str(row["target_period"])
    period_id = PERIOD_BY_TARGET[target_period]
    period_meta = period_by_id[period_id]
    variant = dict(source_entry["variant"])
    source_attempt = dict(source_entry["attempt"])
    source_attempt_name = str(source_attempt["attempt_name"])
    source_set_path = repo_path(str(source_attempt["set_path"]))
    source_ini_path = repo_path(str(source_attempt["ini_path"]))
    source_feature_local = source_feature_path(source_attempt_name)
    source_model_local = source_model_path(source_attempt_name)

    set_values = parse_key_values(source_set_path)
    ini_values = parse_key_values(source_ini_path)
    feature_order = feature_order_from_runtime_csv(source_feature_local)
    feature_hash = ordered_hash(feature_order)
    if feature_hash != str(set_values.get("InpFeatureOrderHash")):
        raise RuntimeError(f"feature order hash mismatch for {source_attempt_name}")

    variant_token = safe_token(variant_id, 36)
    period_token = safe_token(target_period, 12)
    attempt_name = f"run267bn_{order:02d}_{WATCH_ALIAS}_{variant_token}_{period_token}"
    feature_local = (
        FEATURE_ROOT
        / WATCH_ALIAS
        / period_id
        / variant_token
        / f"{attempt_name}_features.csv"
    )
    model_local = (
        VARIANT_ROOT
        / WATCH_ALIAS
        / attempt_name
        / "models"
        / f"{attempt_name}_model.csv"
    )
    feature_meta, _runtime = period_tools.build_runtime_feature_file(
        frames[period_id],
        spec,
        feature_order,
        feature_local,
    )
    model_meta = copy_model_to_variant(source_model_local, model_local)

    common_root = f"{SHORT_COMMON_ROOT}/{WATCH_ALIAS}/{period_token}/{variant_token}/{attempt_name}"
    common_feature_path = f"{common_root}/features/{feature_local.name}"
    common_model_path = f"{common_root}/models/{model_local.name}"
    common_feature = copy_to_common(feature_local, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_local, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    telemetry = f"{common_root}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{common_root}/telemetry/{attempt_name}_summary.csv"
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
    magic = 26722000 + order

    next_set_values = dict(set_values)
    next_set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": f"stage267_AggressiveCrossPeriod__{variant_token}_{period_token}",
            "InpTierLabel": input_probe.mt5.TIER_A,
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": str(period_meta["period_label"]),
            "InpModelPath": common_model_path,
            "InpModelId": f"{RUN_ID}_{WATCH_ALIAS}_{variant_token}_{period_token}",
            "InpModelBackend": "ebm_table",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": len(feature_order),
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpFeatureOrderHash": feature_hash,
            "InpFallbackEnabled": "false",
            "InpFallbackUseOnPrimaryFlat": "false",
            "InpFallbackUseOnPrimaryLowConfidence": "false",
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpMagic": magic,
        }
    )
    set_payload = write_set(RUN_ROOT / "mt5" / f"{attempt_name}.set", next_set_values)

    next_ini_values = dict(ini_values)
    next_ini_values.update(
        {
            "FromDate": period_meta["tester_from_date"],
            "ToDate": period_meta["tester_to_date"],
            "Report": report_name,
            "ExpertParameters": EA_TESTER_SET_NAME,
            "ReplaceReport": 1,
            "ShutdownTerminal": 1,
        }
    )
    ini_payload = write_ini(RUN_ROOT / "mt5" / f"{attempt_name}.ini", next_ini_values)

    attempt = {
        "attempt_name": attempt_name,
        "queue_id": row["queue_id"],
        "source_queue_id": row.get("source_queue_id"),
        "source_variant_id": variant_id,
        "source_first_tranche_attempt_name": source_attempt_name,
        "source_first_tranche_set_path": rel(source_set_path),
        "source_first_tranche_ini_path": rel(source_ini_path),
        "candidate_id": row.get("candidate_id"),
        "candidate_alias": WATCH_ALIAS,
        "candidate_role": row.get("candidate_role"),
        "variant_id": variant_id,
        "target_period": target_period,
        "period_id": period_id,
        "tier": input_probe.mt5.TIER_A,
        "split": period_meta["period_label"],
        "attempt_role": "tier_only_total",
        "record_view_prefix": f"mt5_ta_{WATCH_ALIAS}_{variant_token}_{period_token}_bn",
        "set": set_payload,
        "ini": ini_payload,
        "common_telemetry_path": telemetry,
        "common_summary_path": summary,
        "common_feature_path": common_feature_path,
        "common_model_path": common_model_path,
        "feature_count": len(feature_order),
        "feature_order_hash": feature_hash,
        "max_hold_bars": next_set_values.get("InpMaxHoldBars"),
        "model_materialization_type": "cloned_run267BJ_aggressive_score_table",
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "execution_status": "not_executed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    feature_row = {
        "queue_id": row["queue_id"],
        "attempt_name": attempt_name,
        "candidate_id": row.get("candidate_id"),
        "candidate_alias": WATCH_ALIAS,
        "candidate_role": row.get("candidate_role"),
        "variant_id": variant_id,
        "target_period": target_period,
        "period_id": period_id,
        "period_role": period_meta["period_role"],
        "runtime_feature_file": feature_meta["feature_file"],
        "runtime_feature_sha256": feature_meta["feature_sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "source_feature_file": rel(source_feature_local),
        "source_model_file": rel(source_model_local),
        "runtime_model_file": model_meta["path"],
        "runtime_model_sha256": model_meta["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "rows": feature_meta["rows"],
        "first_bar_time_server": feature_meta["first_bar_time_server"],
        "last_bar_time_server": feature_meta["last_bar_time_server"],
        "duplicate_bar_time_rows": feature_meta["duplicate_bar_time_rows"],
        "runtime_missing_feature_cells": feature_meta["runtime_missing_feature_cells"],
        "feature_count": feature_meta["feature_count"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "bar_time_order_status": "pass" if feature_meta["duplicate_bar_time_rows"] == 0 else "blocked_duplicate_time",
        "materialization_status": "materialized_execution_pending",
    }
    variant_row = {
        "queue_id": row["queue_id"],
        "attempt_name": attempt_name,
        "candidate_id": row.get("candidate_id"),
        "candidate_alias": WATCH_ALIAS,
        "candidate_role": row.get("candidate_role"),
        "variant_id": variant_id,
        "target_period": target_period,
        "period_id": period_id,
        "source_first_tranche_attempt_name": source_attempt_name,
        "source_feature_common_path": variant.get("feature_common_path"),
        "source_model_common_path": variant.get("model_common_path"),
        "feature_common_path": common_feature_path,
        "model_common_path": common_model_path,
        "model_policy": "copy_run267BJ_aggressive_variant_model",
        "set_policy": f"clone_run267BJ_aggressive_set_update_period_{period_token}",
        "status": "materialized_execution_pending",
    }
    return attempt, feature_row, variant_row


def require_inputs() -> None:
    required = (
        SOURCE_QUEUE_PATH,
        SOURCE_FIRST_TRANCHE_VARIANT_MANIFEST_PATH,
        SOURCE_FIRST_TRANCHE_ATTEMPT_MANIFEST_PATH,
    )
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run267BN inputs: " + "; ".join(missing))


def build_receipts(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    counts = result["counts"]
    experiment = [
        {
            "field": "hypothesis",
            "value": "anti_overconstraint_prune(과제약 제거) is only worth deeper Adapter(어댑터) work if it survives adjacent periods(인접 기간).",
            "effect": "2024년 숫자 하나를 바로 선택하지 않고 2023H2/2025H1/2025H2에서 깨지는지 본다.",
        },
        {
            "field": "decision_use",
            "value": "materialization only(물질화 한정); next run(다음 실행) executes MT5(MetaTrader 5, 메타트레이더5).",
            "effect": "selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비)를 주장하지 않는다.",
        },
        {
            "field": "control_variables",
            "value": "run267BJ model/set shape(모델/설정 형태), US100 M5, no-BOM profile policy(BOM 없는 프로필 정책), Tier A only(Tier A 한정).",
            "effect": "기간만 바꿔서 branch(분기)의 구조적 안정성을 본다.",
        },
        {
            "field": "changed_variables",
            "value": "runtime feature frame period(런타임 피처 프레임 기간) only for materialized rows(물질화 행).",
            "effect": "미세 threshold tuning(문턱값 미세 조정) 루프로 변질되지 않는다.",
        },
    ]
    data = [
        {
            "field": "source_frame",
            "value": "run267K source_frame(원천 프레임) rebuilt from Stage56/Stage267 surface(표면).",
            "effect": "새 피처 프레임은 기존 MT5(MetaTrader 5, 메타트레이더5) 손익을 라벨로 쓰지 않는다.",
        },
        {
            "field": "period_scope",
            "value": f"period_rows={counts['period_rows']};feature_frames={counts['feature_frames']}",
            "effect": "2023H2/2025H1/2025H2 기간 압박을 분리한다.",
        },
        {
            "field": "missing_or_duplicate_check",
            "value": f"duplicates_total={counts['duplicate_timestamp_rows']};missing_feature_cells={counts['missing_feature_cells']}",
            "effect": "feature handoff(피처 인계)가 깨진 상태로 MT5(MetaTrader 5, 메타트레이더5)를 실행하지 않게 한다.",
        },
        {
            "field": "selection_bias_boundary",
            "value": "queue was selected after run267BL review(267BL 검토 후 큐 선택).",
            "effect": "다음 결과는 diagnostic(진단)이지 선택 근거 단독이 아니다.",
        },
    ]
    runtime = [
        {
            "field": "feature_model_handoff",
            "status": "materialized_execution_pending",
            "value": f"attempts={counts['attempts']}",
            "effect": "EA(Expert Advisor, 전문가 자문)가 Common Files(공통 파일)에서 feature/model(피처/모델)을 읽을 수 있다.",
        },
        {
            "field": "profile_encoding_policy",
            "status": "linked_to_terminal_runner_utf8_no_bom",
            "value": "run267BI no-BOM repair(267BI BOM 제거 수리)",
            "effect": "tester profile(테스터 프로필) 인코딩 차단을 줄인다.",
        },
        {
            "field": "tier_boundary",
            "status": "fallback_blocked",
            "value": TIER_PAIR_BOUNDARY,
            "effect": "actual routed total(실제 라우팅 전체)을 합성 결과로 오해하지 않는다.",
        },
        {
            "field": "ONNX parity(ONNX 동등성)",
            "status": "not_claimed",
            "value": "blocked_until_goal_gate(목표 게이트 전 차단)",
            "effect": "물질화만으로 ONNX(ONNX) 검토를 시작하지 않는다.",
        },
    ]
    failures = [
        {
            "subject": "anti_overconstraint_similar_replacement(과제약 제거 유사 대체)",
            "status": "blocked_source_surface_needed_before_mt5",
            "why_recorded": "similar replacement(유사 대체)은 원천 feature surface(피처 표면)가 먼저 필요하다.",
            "next_condition": "build replacement source surface(대체 원천 표면 구축) before MT5(MetaTrader 5, 메타트레이더5).",
        },
        {
            "subject": "explode_opportunity_recall(기회 회수 확장)",
            "status": "audit_only_not_materialized",
            "why_recorded": "run267BL(267BL 실행)에서 deep session/Monday hole(깊은 세션/월요일 구멍)이 있었다.",
            "next_condition": "hole audit(구멍 감사) before more MT5(MetaTrader 5, 메타트레이더5).",
        },
    ]
    gates = [
        {
            "gate": "source_queue_authority",
            "status": "passed",
            "evidence": rel(SOURCE_QUEUE_PATH),
            "effect": "run267BM(267BM 실행) 설계 큐에서만 출발한다.",
        },
        {
            "gate": "first_tranche_asset_reuse",
            "status": "passed",
            "evidence": rel(SOURCE_FIRST_TRANCHE_ATTEMPT_MANIFEST_PATH),
            "effect": "공격형 첫 묶음(tranche, 묶음)의 model/set(모델/설정) 의미를 보존한다.",
        },
        {
            "gate": "feature_order_hash_preserved",
            "status": "passed",
            "evidence": rel(FEATURE_FRAME_MANIFEST_PATH),
            "effect": "기간만 바꾸고 feature order(피처 순서)는 유지한다.",
        },
        {
            "gate": "mt5_execution_not_claimed",
            "status": "passed",
            "evidence": rel(ATTEMPT_MANIFEST_PATH),
            "effect": "아직 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)를 주장하지 않는다.",
        },
        {
            "gate": "selection_and_onnx_closed",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_PATH),
            "effect": "selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]
    return experiment, data, runtime, failures, gates


def result_judgment_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    counts = result["counts"]
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"queue_rows={counts['queue_rows']};attempts={counts['attempts']};feature_frames={counts['feature_frames']}",
            "evidence_missing": "MT5 KPI, trade list, balance/equity curve, time-slice review, similar replacement source surface, Adapter structure, ONNX parity",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "기간을 바꾼 실행 입력을 만들었고, 아직 강한 후보를 고른 것이 아니다.",
        },
        {
            "result_subject": "similar_replacement_and_hole_audit_rows",
            "evidence_available": rel(QUEUE_DECISION_PATH),
            "evidence_missing": "replacement feature surface and hole audit execution",
            "judgment_label": "recorded_not_materialized",
            "claim_boundary": "not failure, not selection",
            "next_condition": "after run267BO, decide whether replacement surface or hole audit is worth the next branch",
            "user_explanation_hook": "모든 큐를 무작정 실행하지 않고, 필요한 준비가 없는 행은 경계로 남긴다.",
        },
    ]


def build_result() -> dict[str, Any]:
    require_inputs()
    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    first_sources = first_tranche_sources()
    source, source_info = source_retrain.source_frame()
    period_rows, frames = period_tools.build_period_availability(source)
    period_by_id = period_lookup(period_rows)
    spec = spec_for_watch_alias()

    attempts: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    variant_rows: list[dict[str, Any]] = []
    materializable = [row for row in queue_rows if is_materializable(row)]
    for order, row in enumerate(materializable, start=1):
        variant_id = str(row["source_variant_id"])
        if variant_id not in first_sources:
            raise RuntimeError(f"missing first tranche source for {variant_id}")
        target_period = str(row["target_period"])
        if target_period not in PERIOD_BY_TARGET:
            raise RuntimeError(f"unsupported target period: {target_period}")
        attempt, feature_row, variant_row = materialize_attempt(
            row,
            first_sources[variant_id],
            frames,
            period_by_id,
            spec,
            order=order,
        )
        attempts.append(attempt)
        feature_rows.append(feature_row)
        variant_rows.append(variant_row)

    queue_decisions = queue_decision_rows(queue_rows)
    counts = {
        "queue_rows": len(queue_rows),
        "materialized_rows": len(materializable),
        "blocked_or_audit_rows": len(queue_rows) - len(materializable),
        "period_rows": len(period_rows),
        "feature_frames": len(feature_rows),
        "attempts": len(attempts),
        "duplicate_timestamp_rows": sum(as_int(row.get("duplicate_timestamp_rows")) for row in period_rows),
        "missing_feature_cells": sum(as_int(row.get("runtime_missing_feature_cells")) for row in feature_rows),
    }
    result: dict[str, Any] = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_first_tranche_run_id": SOURCE_FIRST_TRANCHE_RUN_ID,
        "created_at_utc": created_at,
        "source_info": source_info,
        "queue_decisions": queue_decisions,
        "period_availability": period_rows,
        "feature_frame_manifest": feature_rows,
        "variant_manifest": variant_rows,
        "attempts": attempts,
        "counts": counts,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "sources": {
            "second_tranche_queue": rel(SOURCE_QUEUE_PATH),
            "first_tranche_variant_manifest": rel(SOURCE_FIRST_TRANCHE_VARIANT_MANIFEST_PATH),
            "first_tranche_attempt_manifest": rel(SOURCE_FIRST_TRANCHE_ATTEMPT_MANIFEST_PATH),
            "producer": rel(PRODUCER_PATH),
        },
        "outputs": {
            "queue_decision": rel(QUEUE_DECISION_PATH),
            "period_availability": rel(PERIOD_AVAILABILITY_PATH),
            "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "failure_memory_seed": rel(FAILURE_MEMORY_SEED_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    experiment, data, runtime, failures, gates = build_receipts(result)
    result["experiment_design_receipt"] = experiment
    result["data_integrity_receipt"] = data
    result["runtime_parity_receipt"] = runtime
    result["failure_memory_seed"] = failures
    result["gate_audit"] = gates
    result["result_judgment"] = result_judgment_rows(result)
    return result


def attempt_manifest_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in result.get("attempts", []):
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "queue_id": attempt["queue_id"],
                "source_queue_id": attempt["source_queue_id"],
                "source_variant_id": attempt["source_variant_id"],
                "source_first_tranche_attempt_name": attempt["source_first_tranche_attempt_name"],
                "candidate_id": attempt["candidate_id"],
                "candidate_alias": attempt["candidate_alias"],
                "candidate_role": attempt["candidate_role"],
                "variant_id": attempt["variant_id"],
                "target_period": attempt["target_period"],
                "period_id": attempt["period_id"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "attempt_role": attempt["attempt_role"],
                "record_view_prefix": attempt["record_view_prefix"],
                "set_path": attempt["set"]["path"],
                "set_sha256": attempt["set"]["sha256"],
                "ini_path": attempt["ini"]["path"],
                "ini_sha256": attempt["ini"]["sha256"],
                "feature_common_path": attempt["common_feature_path"],
                "model_common_path": attempt["common_model_path"],
                "execution_status": attempt["execution_status"],
            }
        )
    return rows


def runtime_contract_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in result.get("attempts", []):
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "queue_id": attempt["queue_id"],
                "candidate_alias": attempt["candidate_alias"],
                "variant_id": attempt["variant_id"],
                "target_period": attempt["target_period"],
                "period_id": attempt["period_id"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "set_path": attempt["set"]["path"],
                "ini_path": attempt["ini"]["path"],
                "feature_common_path": attempt["common_feature_path"],
                "model_common_path": attempt["common_model_path"],
                "telemetry_common_path": attempt["common_telemetry_path"],
                "summary_common_path": attempt["common_summary_path"],
                "profile_encoding_policy": "utf-8-no-bom via terminal_runner",
                "execution_status": "pending",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(QUEUE_DECISION_PATH, result["queue_decisions"])
    write_csv(PERIOD_AVAILABILITY_PATH, result["period_availability"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, attempt_manifest_rows(result))
    write_csv(RUNTIME_CONTRACT_PATH, runtime_contract_rows(result))
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(FAILURE_MEMORY_SEED_PATH, result["failure_memory_seed"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(RUN_MANIFEST_PATH, result)
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_first_tranche_run_id": SOURCE_FIRST_TRANCHE_RUN_ID,
            "sources": result["sources"],
            "outputs": result["outputs"],
            "lineage_judgment": "connected_with_boundary_no_selection",
        },
    )
    write_json(
        REVIEW_RESULT_PATH,
        {
            "run_id": RUN_ID,
            "status": result["status"],
            "queue_rows": result["counts"]["queue_rows"],
            "attempt_count": result["counts"]["attempts"],
            "feature_frame_count": result["counts"]["feature_frames"],
            "blocked_or_audit_rows": result["counts"]["blocked_or_audit_rows"],
            "next_action": result["next_action"],
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_md(REPORT_PATH, report_markdown(result))


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 run267BN Aggressive Second Tranche Cross-period Materialization(267단계 267BN 공격형 2차 묶음 확장 기간 물질화)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- source_first_tranche(첫 공격형 묶음 원천): `{SOURCE_FIRST_TRANCHE_RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- queue_rows(큐 행): `{counts['queue_rows']}`",
        f"- materialized_attempts(물질화 시도): `{counts['attempts']}`",
        f"- blocked_or_audit_rows(차단/감사 행): `{counts['blocked_or_audit_rows']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BM(267BM 실행)의 direct/control MT5 attempt ready(직접/대조 MT5 시도 준비) 행 4개를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다.",
        "Effect(효과): run267BO(267BO 실행)에서 anti_overconstraint_prune(과제약 제거)과 state_acceleration_interaction(상태 가속 상호작용)이 2024년 밖에서도 덜 깨지는지 실행할 수 있다.",
        "",
        "이번 실행은 성과 판정이 아니다.",
        "Effect(효과): baseline candidate(기준 후보)를 바로 고르지 않고, 기간을 바꾸면 무너지는지 볼 준비만 끝냈다.",
        "",
        "## Queue Decision(큐 판단)",
        "",
        "| queue(큐) | variant(변형) | period(기간) | decision(판단) |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["queue_decisions"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['source_variant_id']}` | `{row['target_period']}` | `{row['run267BN_decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Period Availability(기간 가용성)",
            "",
            "| period(기간) | role(역할) | rows(행) | first(첫 시각) | last(마지막 시각) | status(상태) |",
            "| --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in result["period_availability"]:
        lines.append(
            f"| `{row['period_id']}` | `{row['period_role']}` | {row['rows']} | `{row['first_time_utc']}` | `{row['last_time_utc']}` | `{row['availability_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Attempt Inputs(시도 입력)",
            "",
            "| attempt(시도) | variant(변형) | period(기간) | rows(행) | feature hash(피처 해시) | status(상태) |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in result["feature_frame_manifest"]:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['variant_id']}` | `{row['target_period']}` | {row['rows']} | `{row['feature_order_hash']}` | `{row['materialization_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- MT5 execution(MT5 실행): `not_executed`, 다음 run267BO(267BO 실행)에서 확인한다.",
            "- similar replacement(유사 대체): `blocked_source_surface_needed_before_mt5`, 원천 feature surface(피처 표면)가 먼저 필요하다.",
            "- explode opportunity(기회 확장): `audit_only_not_materialized`, deep hole(깊은 구멍) 감사 전 추가 실행하지 않는다.",
            "- Tier B fallback(Tier B 대체): `blocked`, true fallback manifest(진짜 대체 목록)가 아직 없다.",
            "- Adapter(어댑터): 보류. cross-period MT5 KPI(확장 기간 MT5 핵심 성과 지표), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선)를 본 뒤 판단한다.",
            "- ONNX parity(ONNX 동등성): 금지. Goal gate(목표 게이트) 전에는 검토하지 않는다.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source queue(원천 큐): `{rel(SOURCE_QUEUE_PATH)}`",
            f"- source first tranche attempt manifest(첫 묶음 시도 목록): `{rel(SOURCE_FIRST_TRANCHE_ATTEMPT_MANIFEST_PATH)}`",
            f"- feature manifest(피처 목록): `{rel(FEATURE_FRAME_MANIFEST_PATH)}`",
            f"- attempt manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- runtime contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        ]
    )
    return "\n".join(lines) + "\n"


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BN_producer", "producer_script", PRODUCER_PATH, "Builds run267BN cross-period materialization."),
        ("stage267_run267BN_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Run267BM second tranche queue."),
        ("stage267_run267BN_source_variant_manifest", "source_variant_manifest", SOURCE_FIRST_TRANCHE_VARIANT_MANIFEST_PATH, "Run267BJ variant manifest."),
        ("stage267_run267BN_source_attempt_manifest", "source_attempt_manifest", SOURCE_FIRST_TRANCHE_ATTEMPT_MANIFEST_PATH, "Run267BJ attempt manifest."),
        ("stage267_run267BN_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Run267BN queue decision."),
        ("stage267_run267BN_period_availability", "period_availability", PERIOD_AVAILABILITY_PATH, "Adjacent period availability."),
        ("stage267_run267BN_feature_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Runtime feature frame manifest."),
        ("stage267_run267BN_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267BN_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 attempt manifest."),
        ("stage267_run267BN_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime handoff contract."),
        ("stage267_run267BN_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267BN_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267BN_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267BN_failure_memory", "failure_memory_seed", FAILURE_MEMORY_SEED_PATH, "Failure memory seed."),
        ("stage267_run267BN_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267BN_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267BN_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267BN_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267BN_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267BN_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]


def update_ledgers(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    stage_row = {
        "row_id": "stage267_run267BN_aggressive_second_tranche_cross_period_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "aggressive_second_tranche_cross_period_materialization",
        "tier_scope": "Tier A first; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "feature_model_set_ini_materialization_no_mt5_kpi",
        "status": result["status"],
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"queue_rows={counts['queue_rows']};attempts={counts['attempts']};next_action={result['next_action']}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "aggressive_second_tranche_cross_period_materialization",
        "status": result["status"],
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"attempts={counts['attempts']};selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__aggressive_second_tranche_cross_period_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggressive_second_tranche_cross_period_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "aggressive_second_tranche_cross_period_materialization",
        "tier_scope": "Tier A first; true fallback blocked",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "aggressive_cross_period_materialization",
        "status": result["status"],
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={counts['queue_rows']};attempts={counts['attempts']};feature_frames={counts['feature_frames']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {result['next_action']}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(str(result["created_at_utc"])), key="artifact_id")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, status: str, run_id: str, next_action: str, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {run_id}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {run_id}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {run_id}")
                continue
            if stripped.startswith("next_action:"):
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {next_action}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = f"- run267BN_aggressive_second_tranche_cross_period_materialization(267BN 공격형 2차 묶음 확장 기간 물질화): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BN(267BN 실행)은 run267BM(267BM 실행)의 aggressive second tranche/cross-period queue(공격형 2차 묶음/확장 기간 큐)를 물질화했다.",
            f"Effect(효과): {counts['attempts']}개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도) 입력을 만들어 run267BO(267BO 실행)에서 2023H2/2025H1/2025H2 기간 압박을 바로 실행할 수 있다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{result['status']}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{result['status']}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{result['next_action']}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{result['next_action']}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `aggressive_second_tranche_cross_period_materialization`",
        )
        text = append_after_contains(text, "stage267_run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design.md", report_line)
        text = append_block_once(text, "Run267BN(267BN 실행)은", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BN(267BN 실행) aggressive second tranche cross-period materialization(공격형 2차 묶음 확장 기간 물질화) `{result['status']}`. "
        f"Effect(효과): run267BM(267BM 실행)의 direct/control MT5 attempt ready(직접/대조 MT5 시도 준비) 행 {counts['attempts']}개를 feature/model/set/ini(피처/모델/설정/초기화)와 Common Files(공통 파일) 인계로 만들었고 selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        status=str(result["status"]),
        run_id=RUN_ID,
        next_action=str(result["next_action"]),
        report_entry=f"  run267BN_aggressive_second_tranche_cross_period_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_docs(result)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "queue_rows": result["counts"]["queue_rows"],
                "attempt_count": result["counts"]["attempts"],
                "feature_frame_count": result["counts"]["feature_frames"],
                "blocked_or_audit_rows": result["counts"]["blocked_or_audit_rows"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
                "selected_candidate": "none",
                "selected_research_baseline": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
