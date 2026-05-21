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
)
from stage_pipelines.stage267 import run267BH_aggressive_candidate_pressure_queue as queue_run
from stage_pipelines.stage267 import run267BI_tester_profile_nobom_handoff_repair as previous


STAGE_ID = previous.STAGE_ID
RUN_NUMBER = "run267BJ"
RUN_ID = "run267BJ_stage267_aggressive_pressure_first_tranche_materialization_v1"
PARENT_RUN_ID = queue_run.RUN_ID
HANDOFF_REPAIR_RUN_ID = previous.RUN_ID
CLAIM_BOUNDARY = previous.CLAIM_BOUNDARY

STAGE_ROOT = previous.STAGE_ROOT
REVIEWS_ROOT = previous.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_pressure_first_tranche_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"

SOURCE_QUEUE_PATH = queue_run.QUEUE_PATH
SOURCE_RUN267W_MANIFEST_PATH = (
    STAGE_ROOT / "02_runs/run267W/true_internal_ablation_score_table_materialization/run_manifest.json"
)
SOURCE_RUN267W_ATTEMPTS_PATH = (
    STAGE_ROOT / "02_runs/run267W/true_internal_ablation_score_table_materialization/attempts.csv"
)
SOURCE_RUN267AW_ROOT = STAGE_ROOT / "02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization"

TRANCHE_QUEUE_PATH = RUN_ROOT / "first_tranche_queue.csv"
SOURCE_AVAILABILITY_AUDIT_PATH = RUN_ROOT / "source_availability_audit.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
MODEL_MUTATION_AUDIT_PATH = RUN_ROOT / "model_mutation_audit.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
FAILURE_MEMORY_SEED_PATH = RUN_ROOT / "failure_memory_seed.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BJ_aggressive_pressure_first_tranche_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BJ_aggressive_pressure_first_tranche_materialization.py")

STAGE_LEDGER_PATH = previous.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = previous.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = previous.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = previous.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = previous.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = previous.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = previous.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = previous.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = previous.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = previous.ARTIFACT_COLUMNS

STATUS = "run267BJ_aggressive_pressure_first_tranche_materialized_execution_pending"
JUDGMENT = "aggressive_first_tranche_materialized_no_candidate_selection"
NEXT_ACTION = "run267BK_execute_aggressive_pressure_first_tranche_with_nobom_profiles"
SHORT_COMMON_ROOT = "OPV2/s267bj"
TIER_PAIR_BOUNDARY = "Tier_B_and_actual_routed_total_blocked_until_true_fallback_manifest_exists"
MATERIALIZATION_BOUNDARY = "aggressive_pressure_first_tranche_from_reproducible_run267W_sources"


TRANCHE_PLAN: tuple[dict[str, Any], ...] = (
    {
        "variant_id": "explode_opportunity_recall",
        "source_test_id": "abl_volatility_bandwidth",
        "source_feature_family": "volatility_bandwidth",
        "source_attempt_role": "tier_only_total",
        "model_policy": "copy_source_score_table",
        "set_policy": "loosen_thresholds_disable_side_and_block_filters",
        "why": "widen permission surface before adding defensive repair.",
    },
    {
        "variant_id": "payoff_convexity_push",
        "source_test_id": "rep_volatility_atr",
        "source_feature_family": "volatility_risk",
        "source_attempt_role": "tier_only_total",
        "model_policy": "copy_source_score_table",
        "set_policy": "expand_atr_payoff_shape_keep_entry_surface",
        "why": "pressure payoff shape without adding a new entry filter.",
    },
    {
        "variant_id": "state_acceleration_interaction",
        "source_test_id": "abl_trend_strength_direction",
        "source_feature_family": "trend_strength_direction",
        "source_attempt_role": "tier_only_total",
        "model_policy": "scale_trend_return_state_scores_as_interaction_proxy",
        "set_policy": "slightly_widen_thresholds_keep_state_surface",
        "why": "test whether trend and return state emphasis survives before a deeper interaction rebuild.",
    },
    {
        "variant_id": "anti_overconstraint_prune",
        "source_test_id": "rep_trend_strength_adx",
        "source_feature_family": "trend_strength",
        "source_attempt_role": "tier_only_total",
        "model_policy": "copy_source_score_table",
        "set_policy": "remove_side_and_block_guard_family_keep_risk_shape",
        "why": "check whether prior defensive guard families were hiding a simpler edge.",
    },
)

CSV_MODEL_COLUMNS = ("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


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
    out: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {run_id}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            out.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                out.append(report_entry)
                inserted_report = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                out.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                out.append(f"  current_run_id: {run_id}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                out.append(f"  last_completed_run_id: {run_id}")
                continue
            if stripped.startswith("next_action:"):
                if not inserted_report:
                    out.append(report_entry)
                    inserted_report = True
                out.append(f"  next_action: {next_action}")
                continue
        out.append(line)
    if in_stage267 and not inserted_report:
        out.append(report_entry)
    return "\n".join(out) + "\n"


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
    lines = ["; generated_by=run267BJ_aggressive_pressure_first_tranche_materialization"]
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


def as_float(values: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(values.get(key, default))
    except (TypeError, ValueError):
        return default


def as_int(values: Mapping[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(round(float(values.get(key, default))))
    except (TypeError, ValueError):
        return default


def common_path(path_text: str) -> Path:
    return COMMON_FILES_ROOT_DEFAULT / Path(path_text)


def copy_common_to_local(common_path_text: str, destination: Path) -> dict[str, Any]:
    source = common_path(common_path_text)
    if not path_exists(source):
        raise FileNotFoundError(source.as_posix())
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {
        "source_common_path": common_path_text,
        "path": rel(destination),
        "sha256": sha256_file_lf_normalized(destination),
    }


def copy_local_to_common(local_path: Path, common_path_text: str) -> dict[str, Any]:
    destination = common_path(common_path_text)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(local_path), io_path(destination))
    return {
        "source": rel(local_path),
        "common_path": common_path_text,
        "absolute_path": destination.as_posix(),
        "sha256": sha256_file_lf_normalized(destination),
    }


def feature_index_map(feature_csv_path: Path) -> dict[str, int]:
    with io_path(feature_csv_path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    return {name: index - 1 for index, name in enumerate(header) if index > 0}


def mutate_model_scores(source: Path, destination: Path, feature_indexes: Mapping[str, int]) -> dict[str, Any]:
    target_names = ("adx_14", "di_spread_14", "log_return_3", "return_zscore_20", "return_1_over_atr_14")
    target_indexes = {feature_indexes[name] for name in target_names if name in feature_indexes}
    changed = 0
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as src, io_path(destination).open(
        "w", encoding="utf-8", newline=""
    ) as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=list(reader.fieldnames or CSV_MODEL_COLUMNS), lineterminator="\n")
        writer.writeheader()
        for row in reader:
            if row.get("record_type") == "score":
                try:
                    feature_index = int(float(row.get("feature_index", "-999")))
                except ValueError:
                    feature_index = -999
                if feature_index in target_indexes:
                    for key, factor in (("score_short", 1.18), ("score_long", 1.18), ("score_flat", 0.86)):
                        if row.get(key) not in {"", None}:
                            row[key] = f"{float(row[key]) * factor:.12g}"
                    changed += 1
            writer.writerow(row)
    return {
        "policy": "scaled trend/return state score rows as an interaction proxy",
        "target_feature_indexes": ";".join(str(index) for index in sorted(target_indexes)),
        "changed_score_rows": changed,
        "sha256": sha256_file_lf_normalized(destination),
    }


def source_availability_rows() -> list[dict[str, Any]]:
    return [
        {
            "source": "run267BH aggressive queue(공격형 큐)",
            "path": rel(SOURCE_QUEUE_PATH),
            "exists": path_exists(SOURCE_QUEUE_PATH),
            "decision_use": "first tranche selection(첫 묶음 선택)",
            "effect": "uses the user-requested aggressive pressure queue(공격형 압박 큐)를 입력으로 쓴다.",
        },
        {
            "source": "run267BI no-BOM handoff repair(BOM 제거 인계 수리)",
            "path": rel(previous.RUN_MANIFEST_PATH),
            "exists": path_exists(previous.RUN_MANIFEST_PATH),
            "decision_use": "tester profile policy(테스터 프로필 정책)",
            "effect": "future MT5(MetaTrader 5, 메타트레이더5) profiles(프로필)를 UTF-8 no BOM(UTF-8 BOM 없음)으로 넘긴다.",
        },
        {
            "source": "run267W true internal ablation materialization(진짜 내부 제거 물질화)",
            "path": rel(SOURCE_RUN267W_MANIFEST_PATH),
            "exists": path_exists(SOURCE_RUN267W_MANIFEST_PATH),
            "decision_use": "reproducible source assets(재현 가능한 원천 산출물)",
            "effect": "현재 checkout(체크아웃)에 실제 feature/model/set/ini(피처/모델/설정/초기화)가 있어 바로 복제할 수 있다.",
        },
        {
            "source": "run267AW second follow-up materialization(2차 후속 물질화)",
            "path": rel(SOURCE_RUN267AW_ROOT),
            "exists": path_exists(SOURCE_RUN267AW_ROOT),
            "decision_use": "not used in this tranche(이번 묶음에서는 사용 안 함)",
            "effect": "첫 공격형 묶음(tranche, 묶음)은 run267W(267W 실행)의 재현 가능한 true internal(진짜 내부) 산출물에 고정해 원천 혼선을 줄인다.",
        },
    ]


def first_tranche_queue() -> list[dict[str, str]]:
    rows = [row for row in read_csv(SOURCE_QUEUE_PATH) if row.get("candidate_alias") == "s264_aih"]
    by_variant = {row.get("variant_id", ""): row for row in rows}
    selected: list[dict[str, str]] = []
    for plan in TRANCHE_PLAN:
        row = dict(by_variant[str(plan["variant_id"])])
        row.update(
            {
                "tranche_id": RUN_NUMBER,
                "tranche_role": "first_core_challenger_pressure",
                "source_test_id": str(plan["source_test_id"]),
                "source_feature_family": str(plan["source_feature_family"]),
                "model_policy": str(plan["model_policy"]),
                "set_policy": str(plan["set_policy"]),
                "materialization_note": str(plan["why"]),
            }
        )
        selected.append(row)
    return selected


def source_attempts_by_test() -> dict[str, dict[str, Any]]:
    manifest = read_json(SOURCE_RUN267W_MANIFEST_PATH)
    attempts = [
        dict(attempt)
        for attempt in manifest.get("attempts", [])
        if attempt.get("candidate_alias") == "s264_aih"
        and attempt.get("tier") == "Tier A"
        and attempt.get("attempt_role") == "tier_only_total"
    ]
    return {str(attempt.get("test_id")): attempt for attempt in attempts}


def apply_aggressive_set_policy(values: dict[str, str], variant_id: str, magic: int) -> dict[str, Any]:
    out: dict[str, Any] = dict(values)
    short_threshold = as_float(values, "InpShortThreshold", 0.54)
    long_threshold = as_float(values, "InpLongThreshold", 0.52)
    hold_bars = as_int(values, "InpMaxHoldBars", 3)
    risk_max = as_float(values, "InpModelRiskMaxPct", 0.0305)

    if variant_id == "explode_opportunity_recall":
        out["InpShortThreshold"] = max(0.44, short_threshold - 0.045)
        out["InpLongThreshold"] = max(0.44, long_threshold - 0.045)
        out["InpSideFilterEnabled"] = "false"
        out["InpBlockShortFeatureRange"] = "false"
        out["InpBlockLongFeatureRange"] = "false"
        out["InpSameDirectionReentryCooldownBars"] = 0
        out["InpMaxHoldBars"] = min(6, hold_bars + 1)
        out["InpModelRiskMaxPct"] = min(0.04, risk_max + 0.004)
    elif variant_id == "payoff_convexity_push":
        out["InpAtrSltpEnabled"] = "true"
        out["InpAtrStopMultiplier"] = 1.55
        out["InpAtrTakeProfitMultiplier"] = 6.1
        out["InpMaxHoldBars"] = min(7, hold_bars + 2)
        out["InpModelRiskMaxPct"] = min(0.04, risk_max + 0.005)
    elif variant_id == "state_acceleration_interaction":
        out["InpShortThreshold"] = max(0.46, short_threshold - 0.02)
        out["InpLongThreshold"] = max(0.46, long_threshold - 0.02)
        out["InpMaxHoldBars"] = min(6, hold_bars + 1)
        out["InpEntryTransitionOnly"] = "false"
    elif variant_id == "anti_overconstraint_prune":
        out["InpSideFilterEnabled"] = "false"
        out["InpBlockShortFeatureRange"] = "false"
        out["InpBlockLongFeatureRange"] = "false"
        out["InpReentryCooldownBars"] = 0
        out["InpSameDirectionReentryCooldownBars"] = 0
    else:
        raise ValueError(f"unknown variant_id: {variant_id}")

    out["InpFallbackEnabled"] = "false"
    out["InpFallbackUseOnPrimaryFlat"] = "false"
    out["InpFallbackUseOnPrimaryLowConfidence"] = "false"
    out["InpMagic"] = magic
    return out


def materialize_variant(
    queue_row: Mapping[str, str],
    source_attempt: Mapping[str, Any],
    *,
    order: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    variant_id = str(queue_row["variant_id"])
    source_test_id = str(queue_row["source_test_id"])
    attempt_name = f"run267bj_{order:02d}_s264_aih_{safe_token(variant_id, 36)}_ta_2024"
    variant_dir = VARIANT_ROOT / "s264_aih" / attempt_name
    feature_local = variant_dir / "features" / f"{attempt_name}_features.csv"
    model_local = variant_dir / "models" / f"{attempt_name}_model.csv"

    source_set_path = REPO_ROOT / str(source_attempt["set"]["path"])
    source_ini_path = REPO_ROOT / str(source_attempt["ini"]["path"])
    set_values = parse_key_values(source_set_path)
    ini_values = parse_key_values(source_ini_path)

    source_feature_common = str(set_values["InpFeatureCsvPath"])
    source_model_common = str(set_values["InpModelPath"])
    feature_copy = copy_common_to_local(source_feature_common, feature_local)
    model_source_local = variant_dir / "models" / f"{attempt_name}_source_model.csv"
    model_source = copy_common_to_local(source_model_common, model_source_local)

    model_mutation: dict[str, Any]
    if variant_id == "state_acceleration_interaction":
        model_mutation = mutate_model_scores(model_source_local, model_local, feature_index_map(feature_local))
    else:
        shutil.copy2(io_path(model_source_local), io_path(model_local))
        model_mutation = {
            "policy": "copied source score table without score mutation",
            "target_feature_indexes": "",
            "changed_score_rows": 0,
            "sha256": sha256_file_lf_normalized(model_local),
        }

    feature_common = f"{SHORT_COMMON_ROOT}/s264_aih/{attempt_name}/features/{feature_local.name}"
    model_common = f"{SHORT_COMMON_ROOT}/s264_aih/{attempt_name}/models/{model_local.name}"
    feature_common_copy = copy_local_to_common(feature_local, feature_common)
    model_common_copy = copy_local_to_common(model_local, model_common)

    telemetry = f"{SHORT_COMMON_ROOT}/s264_aih/{attempt_name}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{SHORT_COMMON_ROOT}/s264_aih/{attempt_name}/telemetry/{attempt_name}_summary.csv"
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
    magic = 26721000 + order

    next_set_values = apply_aggressive_set_policy(set_values, variant_id, magic)
    next_set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": f"stage267_AggressivePressure__{variant_id}",
            "InpModelPath": model_common,
            "InpModelId": f"{RUN_ID}_s264_aih_{variant_id}",
            "InpModelBackend": "ebm_table",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": feature_common,
            "InpFeatureCsvUseCommonFiles": "true",
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
        }
    )
    set_payload = write_set(RUN_ROOT / "mt5" / f"{attempt_name}.set", next_set_values)

    next_ini_values = dict(ini_values)
    next_ini_values.update(
        {
            "Report": report_name,
            "ExpertParameters": EA_TESTER_SET_NAME,
            "ReplaceReport": 1,
            "ShutdownTerminal": 1,
        }
    )
    ini_payload = write_ini(RUN_ROOT / "mt5" / f"{attempt_name}.ini", next_ini_values)

    attempt = {
        "attempt_name": attempt_name,
        "queue_id": queue_row["queue_id"],
        "source_queue_id": source_attempt.get("queue_id"),
        "source_attempt_name": source_attempt.get("attempt_name"),
        "source_test_id": source_test_id,
        "candidate_id": queue_row["candidate_id"],
        "candidate_alias": queue_row["candidate_alias"],
        "candidate_role": queue_row["candidate_role"],
        "variant_id": variant_id,
        "tier": "Tier A",
        "split": source_attempt.get("split", "historical_2024_tier_a_train_era_stress"),
        "attempt_role": "tier_only_total",
        "record_view_prefix": f"mt5_ta_s264_aih_{safe_token(variant_id, 28)}_bj",
        "set": set_payload,
        "ini": ini_payload,
        "common_telemetry_path": telemetry,
        "common_summary_path": summary,
        "common_feature_path": feature_common,
        "common_model_path": model_common,
        "feature_count": set_values.get("InpFeatureCount"),
        "feature_order_hash": set_values.get("InpFeatureOrderHash"),
        "max_hold_bars": next_set_values.get("InpMaxHoldBars"),
        "model_materialization_type": "aggressive_pressure_score_table_clone_or_proxy_v1",
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "execution_status": "not_executed",
    }
    variant = {
        "queue_id": queue_row["queue_id"],
        "attempt_name": attempt_name,
        "candidate_id": queue_row["candidate_id"],
        "candidate_alias": queue_row["candidate_alias"],
        "candidate_role": queue_row["candidate_role"],
        "variant_id": variant_id,
        "source_test_id": source_test_id,
        "source_attempt_name": source_attempt.get("attempt_name"),
        "source_feature_common_path": source_feature_common,
        "source_model_common_path": source_model_common,
        "feature_common_path": feature_common,
        "model_common_path": model_common,
        "model_policy": queue_row["model_policy"],
        "set_policy": queue_row["set_policy"],
        "status": "materialized",
    }
    mutation = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "source_model": model_source["source_common_path"],
        "model_path": rel(model_local),
        "model_common_path": model_common,
        "policy": model_mutation["policy"],
        "target_feature_indexes": model_mutation["target_feature_indexes"],
        "changed_score_rows": model_mutation["changed_score_rows"],
        "model_sha256": model_mutation["sha256"],
        "feature_sha256": feature_copy["sha256"],
        "common_feature_sha256": feature_common_copy["sha256"],
        "common_model_sha256": model_common_copy["sha256"],
    }
    return attempt, variant, mutation


def build_materialization() -> dict[str, Any]:
    source_audit = source_availability_rows()
    if not path_exists(SOURCE_QUEUE_PATH) or not path_exists(SOURCE_RUN267W_MANIFEST_PATH):
        return {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "status": "blocked_missing_required_source",
            "created_at_utc": utc_now(),
            "source_availability": source_audit,
            "tranche_rows": 0,
            "variant_count": 0,
            "attempt_count": 0,
            "next_action": "run267BJ_repair_missing_aggressive_tranche_sources",
        }

    created_at = utc_now()
    queue_rows = first_tranche_queue()
    source_attempts = source_attempts_by_test()
    attempts: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for order, row in enumerate(queue_rows, start=1):
        source_test_id = row["source_test_id"]
        source_attempt = source_attempts.get(source_test_id)
        if source_attempt is None:
            raise RuntimeError(f"missing source attempt for {source_test_id}")
        attempt, variant, mutation = materialize_variant(row, source_attempt, order=order)
        attempts.append(attempt)
        variants.append(variant)
        mutations.append(mutation)

    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "handoff_repair_run_id": HANDOFF_REPAIR_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_availability": source_audit,
        "source_queue": rel(SOURCE_QUEUE_PATH),
        "source_run267w_manifest": rel(SOURCE_RUN267W_MANIFEST_PATH),
        "tranche_rows": len(queue_rows),
        "variant_count": len(variants),
        "attempt_count": len(attempts),
        "attempts": attempts,
        "variants": variants,
        "model_mutations": mutations,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "next_action": NEXT_ACTION,
    }
    return result


def experiment_design_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "field": "hypothesis",
            "value": "The core challenger may need aggressive pressure rather than more defensive filters.",
            "effect": "s264_aih(핵심 도전자)를 넓은 허용/손익 비대칭/상태 강조/과제약 제거 축으로 본다.",
        },
        {
            "field": "comparison",
            "value": "first tranche uses s264_aih four aggressive variants from the run267BH queue.",
            "effect": "한 후보만 확정하지 않고, 첫 묶음의 실행 가능성을 만든 뒤 다음 MT5(MetaTrader 5, 메타트레이더5) 결과로 비교한다.",
        },
        {
            "field": "invalid_conditions",
            "value": "missing tester output, stale profile handoff, feature/model order drift, report missing",
            "effect": "실행 인계 문제를 성능 문제로 오해하지 않게 한다.",
        },
        {
            "field": "decision_use",
            "value": "execution input only; not candidate selection",
            "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def runtime_parity_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "field": "profile_encoding_policy",
            "status": "linked",
            "value": HANDOFF_REPAIR_RUN_ID,
            "effect": "tester profile(테스터 프로필)은 run267BI(267BI 실행) 수리처럼 UTF-8 no BOM(UTF-8 BOM 없음)으로 복사된다.",
        },
        {
            "field": "feature_model_handoff",
            "status": "materialized",
            "value": str(result["attempt_count"]),
            "effect": "Common Files(공통 파일) 경로에 feature/model(피처/모델)을 복사해 EA(Expert Advisor, 전문가 자문)가 읽을 수 있게 한다.",
        },
        {
            "field": "tier_boundary",
            "status": "blocked_for_fallback",
            "value": TIER_PAIR_BOUNDARY,
            "effect": "Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 아직 합성하지 않는다.",
        },
    ]


def failure_memory_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in result.get("variants", []):
        rows.append(
            {
                "queue_id": variant["queue_id"],
                "attempt_name": variant["attempt_name"],
                "variant_id": variant["variant_id"],
                "failed_boundary": "not_yet_run",
                "why_failed": "not_applicable_until_mt5_execution",
                "salvage_value": "aggressive pressure input ready",
                "do_not_repeat_note": "do not turn this into a one-threshold repair before MT5 curve/time-slice review",
            }
        )
    return rows


def result_judgment_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "run_status", "value": result["status"], "judgment": "execution_pending"},
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed"},
        {"field": "next_action", "value": result["next_action"], "judgment": "execute_first_tranche_next"},
    ]


def runtime_contract_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in result.get("attempts", []):
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "queue_id": attempt["queue_id"],
                "candidate_alias": attempt["candidate_alias"],
                "variant_id": attempt["variant_id"],
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
            }
        )
    return rows


def attempt_manifest_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in result.get("attempts", []):
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "queue_id": attempt["queue_id"],
                "source_queue_id": attempt["source_queue_id"],
                "source_attempt_name": attempt["source_attempt_name"],
                "candidate_id": attempt["candidate_id"],
                "candidate_alias": attempt["candidate_alias"],
                "candidate_role": attempt["candidate_role"],
                "variant_id": attempt["variant_id"],
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


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(TRANCHE_QUEUE_PATH, first_tranche_queue())
    write_csv(SOURCE_AVAILABILITY_AUDIT_PATH, result.get("source_availability", []))
    write_csv(VARIANT_MANIFEST_PATH, result.get("variants", []))
    write_csv(ATTEMPT_MANIFEST_PATH, attempt_manifest_rows(result))
    write_csv(MODEL_MUTATION_AUDIT_PATH, result.get("model_mutations", []))
    write_csv(RUNTIME_CONTRACT_PATH, runtime_contract_rows(result))
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, experiment_design_rows(result))
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, runtime_parity_rows(result))
    write_csv(FAILURE_MEMORY_SEED_PATH, failure_memory_rows(result))
    write_csv(RESULT_JUDGMENT_PATH, result_judgment_rows(result))
    write_json(RUN_MANIFEST_PATH, result)
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "sources": {
                "aggressive_queue": rel(SOURCE_QUEUE_PATH),
                "handoff_repair": rel(previous.RUN_MANIFEST_PATH),
                "source_run267w_manifest": rel(SOURCE_RUN267W_MANIFEST_PATH),
            },
            "outputs": {
                "tranche_queue": rel(TRANCHE_QUEUE_PATH),
                "variant_manifest": rel(VARIANT_MANIFEST_PATH),
                "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
                "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
                "report": rel(REPORT_PATH),
            },
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        REVIEW_RESULT_PATH,
        {
            "run_id": RUN_ID,
            "status": result["status"],
            "tranche_rows": result["tranche_rows"],
            "attempt_count": result["attempt_count"],
            "next_action": result["next_action"],
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_md(REPORT_PATH, report_markdown(result))


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 run267BJ Aggressive Pressure First Tranche Materialization(공격형 압박 첫 묶음 물질화)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- handoff_repair(인계 수리): `{HANDOFF_REPAIR_RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- tranche_rows(묶음 행): `{result['tranche_rows']}`",
        f"- attempts(시도): `{result['attempt_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BH(267BH 실행)의 s264_aih(핵심 도전자) 공격형 queue(대기열) 4개를 MT5(MetaTrader 5, 메타트레이더5) feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다.",
        "Effect(효과): baseline candidate(기준 후보)를 고르는 일을 방어 필터 누적만으로 끌지 않고, 넓은 허용/손익 비대칭/상태 강조/과제약 제거를 바로 실행 가능한 형태로 바꾼다.",
        "",
        "## Tranche(묶음)",
        "",
        "| variant(변형) | source(원천) | materialization(물질화) |",
        "| --- | --- | --- |",
    ]
    for variant in result.get("variants", []):
        lines.append(
            f"| `{variant['variant_id']}` | `{variant['source_test_id']}` | `{variant['model_policy']}` / `{variant['set_policy']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 실행은 materialization(물질화)이며 candidate selection(후보 선택)이 아니다.",
            "- Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 생기기 전까지 차단한다.",
            "- ONNX parity(ONNX 동등성)나 ONNX conversion(ONNX 변환)은 시작하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- tranche_queue(묶음 큐): `{rel(TRANCHE_QUEUE_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
            f"- model_mutation_audit(모델 변경 감사): `{rel(MODEL_MUTATION_AUDIT_PATH)}`",
            f"- next_action(다음 행동): `{result['next_action']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BJ_producer", "producer_script", PRODUCER_PATH, "Builds run267BJ first aggressive tranche."),
        ("stage267_run267BJ_tranche_queue", "tranche_queue", TRANCHE_QUEUE_PATH, "Run267BJ first tranche queue."),
        ("stage267_run267BJ_source_availability", "source_audit", SOURCE_AVAILABILITY_AUDIT_PATH, "Source availability audit."),
        ("stage267_run267BJ_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267BJ_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 attempt manifest."),
        ("stage267_run267BJ_model_mutation_audit", "model_mutation_audit", MODEL_MUTATION_AUDIT_PATH, "Model mutation audit."),
        ("stage267_run267BJ_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime handoff contract."),
        ("stage267_run267BJ_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267BJ_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267BJ_failure_memory_seed", "failure_memory_seed", FAILURE_MEMORY_SEED_PATH, "Failure memory seed."),
        ("stage267_run267BJ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267BJ_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267BJ_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267BJ_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267BJ_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    rows = [
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
    for path in sorted(VARIANT_ROOT.glob("**/*")):
        if path.is_file():
            rows.append(
                {
                    "artifact_id": "stage267_run267BJ_" + safe_token(rel(path), 160),
                    "artifact_type": "variant_runtime_artifact",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": "Run267BJ materialized feature/model artifact.",
                }
            )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    stage_row = {
        "row_id": "stage267_run267BJ_aggressive_pressure_first_tranche_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "aggressive_pressure_first_tranche_materialization",
        "tier_scope": "Tier A first; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "feature_model_set_ini_materialization_no_mt5_kpi",
        "status": result["status"],
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"tranche_rows={result['tranche_rows']};attempts={result['attempt_count']};next_action={result['next_action']}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "aggressive_pressure_first_tranche_materialization",
        "status": result["status"],
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"attempts={result['attempt_count']};selected_candidate=none;onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__aggressive_pressure_first_tranche_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggressive_pressure_first_tranche_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "aggressive_pressure_first_tranche_materialization",
        "tier_scope": "Tier A first; true fallback blocked",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "aggressive_materialization",
        "status": result["status"],
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"tranche_rows={result['tranche_rows']};attempts={result['attempt_count']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {result['next_action']}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(str(result["created_at_utc"])), key="artifact_id")


def update_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267BJ_aggressive_pressure_first_tranche_materialization(267BJ 공격형 압박 첫 묶음 물질화): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BJ(267BJ 실행)는 run267BH(267BH 실행)의 s264_aih(핵심 도전자) 공격형 첫 묶음(tranche, 묶음)을 물질화했다.",
            f"Effect(효과): {result['attempt_count']}개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도) 입력을 만들었고, 다음 run267BK(267BK 실행)에서 no-BOM(바이트 순서 표시 없음) profile(프로필)로 실행한다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
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
        text = append_after_contains(text, "stage267_run267BI_tester_profile_nobom_handoff_repair.md", report_line)
        text = append_block_once(text, "Run267BJ(267BJ 실행)는", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BJ(267BJ 실행) aggressive pressure first tranche materialization(공격형 압박 첫 묶음 물질화) `{result['status']}`. "
        f"Effect(효과): run267BH(267BH 실행)의 s264_aih(핵심 도전자) 공격형 queue(대기열) 4개를 feature/model/set/ini(피처/모델/설정/초기화)와 Common Files(공통 파일) 인계로 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        status=str(result["status"]),
        run_id=RUN_ID,
        next_action=str(result["next_action"]),
        report_entry=f"  run267BJ_aggressive_pressure_first_tranche_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_materialization()
    write_outputs(result)
    update_ledgers(result)
    update_docs(result)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "tranche_rows": result["tranche_rows"],
                "attempt_count": result["attempt_count"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
                "selected_candidate": "none",
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
