from __future__ import annotations

import csv
import json
import math
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
    attempt_payload,
    copy_to_common,
    parse_ini,
)
from foundation.mt5 import runtime_support as mt5


STAGE_ID = "267_adapter_research__baseline_candidate_racing_protocol"
RUN_NUMBER = "run267T"
RUN_ID = "run267T_stage267_pool_wide_orthogonal_stability_mt5_attempts_v1"
PARENT_RUN_ID = "run267S_stage267_pool_wide_orthogonal_stability_racing_matrix_v1"
STATUS = "run267T_pool_wide_orthogonal_stability_mt5_attempts_built_execution_pending"
NEXT_ACTION = "run267T_execute_pool_wide_orthogonal_stability_mt5_batch"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_stability_mt5_attempts"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

RUN267S_ROOT = STAGE_ROOT / "02_runs" / "run267S" / "pool_wide_orthogonal_stability_racing_matrix"
RUN267S_QUEUE_PATH = RUN267S_ROOT / "materialization_queue.csv"
RUN267S_MATRIX_PATH = RUN267S_ROOT / "orthogonal_stability_matrix.csv"
RUN267S_SCOPE_PATH = RUN267S_ROOT / "candidate_scope_update.csv"
RUN267S_REPORT_PATH = REVIEWS_ROOT / "stage267_run267S_pool_wide_orthogonal_stability_racing_matrix.md"

RUN267N_ROOT = STAGE_ROOT / "02_runs" / "run267N" / "p0_ablation_replacement_materialization"
RUN267N_VARIANT_MANIFEST_PATH = RUN267N_ROOT / "p0_materialized_variant_manifest.csv"
RUN267N_RUNTIME_CONTRACT_PATH = RUN267N_ROOT / "runtime_contract.csv"
RUN267N_ATTEMPTS_PATH = RUN267N_ROOT / "attempts.csv"

VARIANT_MANIFEST_PATH = RUN_ROOT / "orthogonal_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempts.csv"
ATTEMPT_GAP_PATH = RUN_ROOT / "attempt_gap_register.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
GATE_RECEIPT_PATH = RUN_ROOT / "gate_receipt.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
RESULT_PATH = RUN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267T_pool_wide_orthogonal_stability_mt5_attempts.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267T_build_pool_wide_orthogonal_stability_mt5_attempts.py")

PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

COMMON_ROOT = "OPV2/s267t/run267T_orthogonal_stability"
FROM_DATE = "2024.01.02"
TO_DATE = "2025.01.01"
SPLIT_LABEL = "historical_2024_tier_a_train_era_stress"

AXIS_TESTS = {
    "run267S_axis01_pool_wide_variant_distinguishability": (
        "abl_volatility_bandwidth",
        "rep_volatility_atr",
    ),
    "run267S_axis02_non_calendar_weak_slice_resilience": (
        "abl_trend_strength_direction",
        "rep_trend_strength_adx",
    ),
}

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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


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


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def safe_token(value: str, limit: int = 80) -> str:
    token = "".join(ch.lower() if ch.isalnum() else "_" for ch in str(value))
    token = "_".join(part for part in token.split("_") if part)
    return token[:limit] or "item"


def copy_file(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {
        "source": rel(source),
        "path": rel(destination),
        "sha256": sha256_file_lf_normalized(destination),
    }


def require_inputs() -> None:
    required = (
        RUN267S_QUEUE_PATH,
        RUN267S_MATRIX_PATH,
        RUN267S_SCOPE_PATH,
        RUN267N_VARIANT_MANIFEST_PATH,
        RUN267N_RUNTIME_CONTRACT_PATH,
        RUN267N_ATTEMPTS_PATH,
    )
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run267T inputs: " + ";".join(missing))


def key_by(rows: Sequence[Mapping[str, str]], *columns: str) -> dict[tuple[str, ...], Mapping[str, str]]:
    keyed: dict[tuple[str, ...], Mapping[str, str]] = {}
    for row in rows:
        key = tuple(str(row.get(column, "")).strip() for column in columns)
        if all(key):
            keyed[key] = row
    return keyed


def source_attempt(
    attempts_by_queue_role: Mapping[tuple[str, str], Mapping[str, str]],
    queue_id: str,
    attempt_role: str,
) -> Mapping[str, str]:
    row = attempts_by_queue_role.get((queue_id, attempt_role))
    if not row:
        raise RuntimeError(f"missing source attempt for {queue_id} {attempt_role}")
    return row


def from_to_dates(attempt_row: Mapping[str, str]) -> tuple[str, str]:
    ini_path = Path(str(attempt_row.get("ini_path", "")))
    if path_exists(ini_path):
        parsed = parse_ini(ini_path)
        return parsed.get("FromDate", FROM_DATE), parsed.get("ToDate", TO_DATE)
    return FROM_DATE, TO_DATE


def source_variants_for_axis() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    queue_rows = read_csv_rows(RUN267S_QUEUE_PATH)
    variant_rows = read_csv_rows(RUN267N_VARIANT_MANIFEST_PATH)
    contract_rows = read_csv_rows(RUN267N_RUNTIME_CONTRACT_PATH)
    source_attempt_rows = read_csv_rows(RUN267N_ATTEMPTS_PATH)
    variants_by_candidate_test = key_by(variant_rows, "candidate_alias", "test_id")
    contracts_by_queue = key_by(contract_rows, "queue_id")
    attempts_by_queue_role = key_by(source_attempt_rows, "queue_id", "attempt_role")

    materialized: list[dict[str, Any]] = []
    runtime_contract: list[dict[str, Any]] = []
    gap_rows: list[dict[str, Any]] = []
    variant_order = 0
    for queue in queue_rows:
        axis_id = queue["axis_id"]
        alias = queue["candidate_alias"]
        candidate_id = queue["candidate_id"]
        candidate_role = queue["candidate_role"]
        tests = AXIS_TESTS.get(axis_id)
        if tests is None:
            gap_rows.append(
                {
                    "gap_id": f"{RUN_NUMBER}_{alias}_{safe_token(axis_id, 48)}",
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": candidate_role,
                    "axis_id": axis_id,
                    "test_id": "not_applicable",
                    "gap_status": "out_of_scope_by_claim",
                    "reason": "candidate_pool_prune_or_restore(후보군 가지치기/복귀)는 MT5 시도가 아니라 판정 장부 축이다.",
                    "required_repair": "use_candidate_scope_and_failure_memory_in_review",
                }
            )
            continue
        for test_id in tests:
            source_variant = variants_by_candidate_test.get((alias, test_id))
            if not source_variant:
                gap_rows.append(
                    {
                        "gap_id": f"{RUN_NUMBER}_{alias}_{safe_token(axis_id, 32)}_{test_id}",
                        "candidate_id": candidate_id,
                        "candidate_alias": alias,
                        "candidate_role": candidate_role,
                        "axis_id": axis_id,
                        "test_id": test_id,
                        "gap_status": "missing_required",
                        "reason": "run267N(267N 실행) source variant(원천 변형)이 없어 새 MT5 시도를 만들지 않았다.",
                        "required_repair": "design_source_variant_before_execution_or_mark_axis_incomplete",
                    }
                )
                continue
            variant_order += 1
            source_queue_id = source_variant["queue_id"]
            contract = contracts_by_queue.get((source_queue_id,), {})
            queue_token = f"run267t_{variant_order:02d}_{alias}_{safe_token(test_id, 44)}"
            local_feature = VARIANT_ROOT / alias / queue_token / "features" / Path(source_variant["feature_file"]).name
            local_model = VARIANT_ROOT / alias / queue_token / "models" / Path(source_variant["model_file"]).name
            feature_copy = copy_file(Path(source_variant["feature_file"]), local_feature)
            model_copy = copy_file(Path(source_variant["model_file"]), local_model)
            common_root = f"{COMMON_ROOT}/{alias}/{queue_token}"
            common_feature_path = f"{common_root}/features/{local_feature.name}"
            common_model_path = f"{common_root}/models/{local_model.name}"
            common_feature = copy_to_common(local_feature, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
            common_model = copy_to_common(local_model, common_model_path, COMMON_FILES_ROOT_DEFAULT)
            materialized.append(
                {
                    "variant_order": variant_order,
                    "variant_id": queue_token,
                    "source_run_id": "run267N_stage267_pool_wide_ablation_replacement_materialization_v1",
                    "source_queue_id": source_queue_id,
                    "run267S_queue_id": queue["queue_id"],
                    "axis_id": axis_id,
                    "axis_class": queue["axis_class"],
                    "priority": queue["priority"],
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": candidate_role,
                    "test_id": test_id,
                    "test_type": source_variant.get("test_type", ""),
                    "feature_family": source_variant.get("feature_family", ""),
                    "materialization_boundary": source_variant.get("materialization_boundary", ""),
                    "source_feature_file": source_variant["feature_file"],
                    "feature_file": feature_copy["path"],
                    "feature_sha256": feature_copy["sha256"],
                    "source_model_file": source_variant["model_file"],
                    "model_file": model_copy["path"],
                    "model_sha256": model_copy["sha256"],
                    "common_feature_path": common_feature["common_path"],
                    "common_feature_sha256": common_feature["sha256"],
                    "common_model_path": common_model["common_path"],
                    "common_model_sha256": common_model["sha256"],
                    "feature_count": as_int(source_variant.get("feature_count")),
                    "feature_order_hash": source_variant.get("feature_order_hash", ""),
                    "feature_order": source_variant.get("feature_order", ""),
                    "rows": as_int(source_variant.get("rows")),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            runtime_contract.append(
                {
                    "variant_id": queue_token,
                    "source_queue_id": source_queue_id,
                    "axis_id": axis_id,
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "test_id": test_id,
                    "shared_contract": "US100 M5;2024 historical stress window;MT5 RuntimeProbeEA;score_table_csv;attempt set/ini identity",
                    "feature_count": as_int(source_variant.get("feature_count")),
                    "feature_order_hash": source_variant.get("feature_order_hash", ""),
                    "model_backend": contract.get("model_backend", "ebm_table"),
                    "model_materialization_type": source_variant.get("model_materialization_type", ""),
                    "materialization_boundary": source_variant.get("materialization_boundary", ""),
                    "short_threshold": as_float(contract.get("short_threshold"), 0.54),
                    "long_threshold": as_float(contract.get("long_threshold"), 0.52),
                    "min_margin": as_float(contract.get("min_margin"), 0.0),
                    "max_hold_bars": as_int(contract.get("max_hold_bars"), 3),
                    "close_on_flat_signal": contract.get("close_on_flat_signal", "false"),
                    "reverse_on_opposite_signal": contract.get("reverse_on_opposite_signal", "true"),
                    "close_only_on_opposite_signal": contract.get("close_only_on_opposite_signal", "false"),
                    "known_difference": "copied_from_run267N_source_variant_no_new_model_logic",
                    "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
                }
            )
    return materialized, runtime_contract, gap_rows


def build_attempts(
    variants: Sequence[Mapping[str, Any]],
    runtime_contract_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    contract_by_variant = {str(row["variant_id"]): row for row in runtime_contract_rows}
    source_attempt_rows = read_csv_rows(RUN267N_ATTEMPTS_PATH)
    attempts_by_queue_role = key_by(source_attempt_rows, "queue_id", "attempt_role")
    attempts: list[dict[str, Any]] = []
    for variant in variants:
        contract = contract_by_variant[str(variant["variant_id"])]
        for attempt_role, tier, suffix, record_prefix in (
            ("tier_only_total", mt5.TIER_A, "ta", "mt5_ta"),
            ("routed_total", mt5.TIER_AB, "rt", "mt5_rt"),
        ):
            source_row = source_attempt(attempts_by_queue_role, str(variant["source_queue_id"]), attempt_role)
            from_date, to_date = from_to_dates(source_row)
            attempt_name = f"{variant['variant_id']}_{suffix}_2024"
            payload = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=267,
                exploration_label=f"stage267_OrthogonalStability__{safe_token(str(variant['axis_id']), 40)}",
                attempt_name=attempt_name,
                tier=tier,
                split=SPLIT_LABEL,
                model_path=str(variant["common_model_path"]),
                model_id=f"{RUN_ID}_{variant['candidate_alias']}_{variant['test_id']}",
                model_backend=str(contract.get("model_backend", "ebm_table")),
                feature_path=str(variant["common_feature_path"]),
                feature_count=as_int(variant.get("feature_count")),
                feature_order_hash=str(variant.get("feature_order_hash", "")),
                short_threshold=as_float(contract.get("short_threshold"), 0.54),
                long_threshold=as_float(contract.get("long_threshold"), 0.52),
                min_margin=as_float(contract.get("min_margin"), 0.0),
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role=attempt_role,
                record_view_prefix=f"{record_prefix}_{variant['candidate_alias']}_{variant['test_id']}_run267t",
                max_hold_bars=as_int(contract.get("max_hold_bars"), 3),
                common_root=f"{COMMON_ROOT}/{variant['candidate_alias']}/{variant['variant_id']}",
                fallback_enabled=False,
                close_on_flat_signal=str(contract.get("close_on_flat_signal", "false")).lower() == "true",
                reverse_on_opposite_signal=str(contract.get("reverse_on_opposite_signal", "true")).lower() == "true",
                close_only_on_opposite_signal=str(contract.get("close_only_on_opposite_signal", "false")).lower() == "true",
            )
            attempts.append(
                {
                    "queue_id": variant["variant_id"],
                    "source_queue_id": variant["source_queue_id"],
                    "axis_id": variant["axis_id"],
                    "candidate_id": variant["candidate_id"],
                    "candidate_alias": variant["candidate_alias"],
                    "candidate_role": variant["candidate_role"],
                    "test_id": variant["test_id"],
                    "priority": variant["priority"],
                    "attempt_name": attempt_name,
                    "tier": tier,
                    "split": SPLIT_LABEL,
                    "attempt_role": attempt_role,
                    "record_view_prefix": payload["record_view_prefix"],
                    "set_path": rel(Path(payload["set"]["path"])),
                    "set_sha256": payload["set"]["sha256"],
                    "ini_path": rel(Path(payload["ini"]["path"])),
                    "ini_sha256": payload["ini"]["sha256"],
                    "common_telemetry_path": payload["common_telemetry_path"],
                    "common_summary_path": payload["common_summary_path"],
                    "fallback_enabled": "false",
                    "execution_status": "not_executed",
                }
            )
    return attempts


def build_gate_receipt() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "experiment_design",
            "gate_status": "passed",
            "evidence": rel(RUN267S_MATRIX_PATH),
            "effect": "run267S(267S 실행)의 가설, 비교, 중단 조건을 MT5 시도 목록에 연결했다.",
        },
        {
            "gate_id": "runtime_parity",
            "gate_status": "bounded",
            "evidence": rel(RUNTIME_CONTRACT_PATH),
            "effect": "Python(파이썬) 원천 변형과 MT5(MetaTrader 5, 메타트레이더5) set/ini(설정/초기화) 정체성을 기록했다.",
        },
        {
            "gate_id": "artifact_lineage",
            "gate_status": "passed",
            "evidence": rel(LINEAGE_PATH),
            "effect": "run267S/N(267S/N 실행) 입력, 복사 산출물, Common Files(Common Files, 공통 파일) 인계를 연결했다.",
        },
        {
            "gate_id": "result_judgment",
            "gate_status": "passed",
            "evidence": rel(REPORT_PATH),
            "effect": "materialization only(물질화만) 경계라 후보 선택과 ONNX 준비를 주장하지 않는다.",
        },
        {
            "gate_id": "required_gap_record",
            "gate_status": "passed",
            "evidence": rel(ATTEMPT_GAP_PATH),
            "effect": "없는 source variant(원천 변형)와 decision-only axis(판정 전용 축)를 숨기지 않았다.",
        },
        {
            "gate_id": "required_gate_coverage_audit",
            "gate_status": "passed",
            "evidence": rel(GATE_RECEIPT_PATH),
            "effect": "필수 gate(게이트)를 closeout(종료 기록) 산출물에 연결했다.",
        },
    ]


def build_lineage(
    variants: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "producer": rel(PRODUCER_PATH),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": [
            rel(RUN267S_QUEUE_PATH),
            rel(RUN267S_MATRIX_PATH),
            rel(RUN267S_SCOPE_PATH),
            rel(RUN267N_VARIANT_MANIFEST_PATH),
            rel(RUN267N_RUNTIME_CONTRACT_PATH),
            rel(RUN267N_ATTEMPTS_PATH),
        ],
        "outputs": {
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "attempt_gap_register": rel(ATTEMPT_GAP_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "gate_receipt": rel(GATE_RECEIPT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "common_root": COMMON_ROOT,
        "common_files_root": COMMON_FILES_ROOT_DEFAULT.as_posix(),
        "variant_count": len(variants),
        "attempt_count": len(attempts),
        "lineage_judgment": "connected_with_boundary",
        "availability": "tracked_manifests_and_common_files_handoff",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_result() -> dict[str, Any]:
    require_inputs()
    variants, runtime_contract, gap_rows = source_variants_for_axis()
    attempts = build_attempts(variants, runtime_contract)
    gate_receipt = build_gate_receipt()
    lineage = build_lineage(variants, attempts)
    return {
        "created_at_utc": utc_now(),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "variant_count": len(variants),
        "attempt_count": len(attempts),
        "gap_count": len(gap_rows),
        "axis_attempts": {
            axis_id: sum(1 for row in attempts if row["axis_id"] == axis_id)
            for axis_id in sorted({str(row["axis_id"]) for row in variants})
        },
        "variant_manifest": variants,
        "runtime_contract": runtime_contract,
        "attempts": attempts,
        "attempt_gaps": gap_rows,
        "gate_receipt": gate_receipt,
        "lineage": lineage,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        VARIANT_MANIFEST_PATH,
        result["variant_manifest"],
        (
            "variant_order",
            "variant_id",
            "source_run_id",
            "source_queue_id",
            "run267S_queue_id",
            "axis_id",
            "axis_class",
            "priority",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "feature_family",
            "materialization_boundary",
            "source_feature_file",
            "feature_file",
            "feature_sha256",
            "source_model_file",
            "model_file",
            "model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_count",
            "feature_order_hash",
            "feature_order",
            "rows",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        result["runtime_contract"],
        (
            "variant_id",
            "source_queue_id",
            "axis_id",
            "candidate_id",
            "candidate_alias",
            "test_id",
            "shared_contract",
            "feature_count",
            "feature_order_hash",
            "model_backend",
            "model_materialization_type",
            "materialization_boundary",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat_signal",
            "reverse_on_opposite_signal",
            "close_only_on_opposite_signal",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        result["attempts"],
        (
            "queue_id",
            "source_queue_id",
            "axis_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "priority",
            "attempt_name",
            "tier",
            "split",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "fallback_enabled",
            "execution_status",
        ),
    )
    write_csv(
        ATTEMPT_GAP_PATH,
        result["attempt_gaps"],
        (
            "gap_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "axis_id",
            "test_id",
            "gap_status",
            "reason",
            "required_repair",
        ),
    )
    write_csv(GATE_RECEIPT_PATH, result["gate_receipt"], ("gate_id", "gate_status", "evidence", "effect"))
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "created_at_utc": result["created_at_utc"],
            "variant_count": result["variant_count"],
            "attempt_count": result["attempt_count"],
            "gap_count": result["gap_count"],
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "attempt_gap_register": rel(ATTEMPT_GAP_PATH),
            "next_action": NEXT_ACTION,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, build_report(result))


def build_report(result: Mapping[str, Any]) -> str:
    axis_attempts = result["axis_attempts"]
    lines = [
        "# Stage267 Run267T Pool-wide Orthogonal Stability MT5 Attempts(267단계 267T 후보군 전체 직교 안정성 MT5 시도)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(부모 실행): `{PARENT_RUN_ID}`",
        f"- variant_count(변형 수): `{result['variant_count']}`",
        f"- attempt_count(시도 수): `{result['attempt_count']}`",
        f"- gap_count(공백 수): `{result['gap_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267S(267S 실행)는 다섯 후보를 세 안정성 축에 올렸다.",
        "run267T(267T 실행)는 그중 MT5(MetaTrader 5, 메타트레이더5)로 바로 시도할 수 있는 축을 `.set/.ini(설정/초기화)`로 만들었다.",
        "Effect(효과): 다음 작업은 아이디어 토론이 아니라 같은 계약으로 tester(테스터)를 돌릴 수 있는 상태가 된다.",
        "",
        "## Built Surface(만든 표면)",
        "",
        "| axis(축) | attempts(시도) | read(판독) |",
        "| --- | ---: | --- |",
    ]
    for axis_id in sorted(axis_attempts):
        lines.append(f"| `{axis_id}` | {axis_attempts[axis_id]} | MT5 execution pending(MT5 실행 대기) |")
    lines.extend(
        [
            "",
            "Axis03(축03)은 후보군 prune/restore(가지치기/복귀) 판정 축이라 MT5 시도로 만들지 않았다.",
            "Effect(효과): 판정 전용 축과 런타임 실행 축을 섞지 않는다.",
            "",
            "## Gap Handling(공백 처리)",
            "",
            f"- missing/out-of-scope rows(필수 누락/범위 밖 행): `{result['gap_count']}`",
            f"- gap register(공백 등록부): `{rel(ATTEMPT_GAP_PATH)}`",
            "- Effect(효과): 없는 source variant(원천 변형)를 있는 것처럼 실행하지 않는다.",
            "",
            "## Runtime Boundary(런타임 경계)",
            "",
            "- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.ex5`, `.set/.ini(설정/초기화)` attempts(시도).",
            "- shared_contract(공유 계약): US100 M5, 2024 historical stress(2024 과거 압박), score-table CSV(점수표 CSV), feature order hash(피처 순서 해시).",
            "- parity_check(동등성 점검): materialization identity only(물질화 정체성만). MT5 tester output(테스터 출력)은 아직 없다.",
            "- runtime_claim_boundary(런타임 주장 경계): `research_only_execution_pending_no_selected_candidate_no_onnx`.",
            "",
            "## Boundary(경계)",
            "",
            "- judgment(판정): `materialized_execution_pending_no_candidate_selection(물질화 완료, 실행 대기, 선택 후보 없음)`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).",
            "",
            "## Artifacts(산출물)",
            "",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
            f"- attempts(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- gate_receipt(게이트 기록): `{rel(GATE_RECEIPT_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- result(결과): `{rel(RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = (
        ("stage267_run267T_script", "producer_script", PRODUCER_PATH, "Builds run267T MT5 attempt materialization."),
        ("stage267_run267T_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267T orthogonal variant manifest."),
        ("stage267_run267T_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267T runtime contract."),
        ("stage267_run267T_attempts", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267T MT5 attempt manifest."),
        ("stage267_run267T_attempt_gap_register", "gap_register", ATTEMPT_GAP_PATH, "Run267T attempt gap register."),
        ("stage267_run267T_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267T run manifest."),
        ("stage267_run267T_gate_receipt", "gate_receipt", GATE_RECEIPT_PATH, "Run267T gate receipt."),
        ("stage267_run267T_lineage", "lineage", LINEAGE_PATH, "Run267T artifact lineage."),
        ("stage267_run267T_result", "result", RESULT_PATH, "Run267T result payload."),
        ("stage267_run267T_report", "review_report", REPORT_PATH, "Run267T user-facing report."),
    )
    rows = []
    for artifact_id, artifact_type, path, notes in artifacts:
        rows.append(
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
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    primary_kpi = f"variants={result['variant_count']};attempts={result['attempt_count']};gaps={result['gap_count']}"
    guardrail = "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed"
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267T_pool_wide_orthogonal_stability_mt5_attempts",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "pool_wide_orthogonal_stability_mt5_attempt_materialization",
                "tier_scope": "Tier A and actual routed total attempts planned",
                "scoreboard": "runtime_contract_attempt_manifest",
                "status": STATUS,
                "judgment": "materialized_execution_pending_no_candidate_selection",
                "evidence_boundary": "feature_model_set_ini_manifest_only_no_mt5_kpi_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"{primary_kpi};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_stability_mt5_attempts",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "pool_wide_orthogonal_stability_mt5_attempts",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "pool_wide_orthogonal_stability_mt5_attempt_materialization",
                "tier_scope": "Tier A and actual routed total attempts planned",
                "kpi_scope": "materialization_identity_no_mt5_kpi",
                "scoreboard_lane": "runtime_contract_attempt_manifest",
                "status": STATUS,
                "judgment": "materialized_execution_pending_no_candidate_selection",
                "path": rel(REPORT_PATH),
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "external_verification_status": "not_started_materialization_only",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "pool_wide_orthogonal_stability_mt5_attempt_materialization",
                "status": STATUS,
                "judgment": "materialized_execution_pending_no_candidate_selection",
                "path": rel(REPORT_PATH),
                "notes": f"Run267T MT5 attempts built; {primary_kpi}; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(str(result["created_at_utc"])),
        key="artifact_id",
    )


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267T_pool_wide_orthogonal_stability_mt5_attempts(267T 후보군 전체 직교 안정성 MT5 시도): "
        f"`{rel(REPORT_PATH)}`"
    )
    status_line = f"`{STATUS}`"
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_stability_mt5_attempts`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): {status_line}")
    current = append_after_contains(current, "run267S_pool_wide_orthogonal_stability_racing_matrix", report_line)
    latest_line = (
        "- latest_materialization(최신 물질화): run267T(267T 실행) pool-wide orthogonal stability MT5 attempts"
        f"(후보군 전체 직교 안정성 MT5 시도) `{rel(REPORT_PATH)}`."
    )
    current = append_after_contains(current, "latest_matrix(최신 행렬): run267S", latest_line)
    current = replace_line_prefix(current, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- action(행동):",
        "- action(행동): run267T(267T 실행)는 run267S(267S 실행) 행렬에서 MT5(MetaTrader 5, 메타트레이더5)로 바로 실행 가능한 변형을 `.set/.ini(설정/초기화)` 시도로 만들었다.",
    )
    current = replace_line_prefix(
        current,
        "- effect(효과):",
        "- effect(효과): 다음 작업은 후보군 전체 직교 안정성 시도를 tester(테스터)에서 실행하고 결과를 거래/곡선/시간구간으로 검토할 수 있다.",
    )
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_block_once(
        current,
        "Run267T(267T 실행)는 run267S",
        (
            "Run267T(267T 실행)는 run267S(267S 실행) 행렬에서 MT5(MetaTrader 5, 메타트레이더5) 시도를 물질화했다.\n"
            f"Effect(효과): `{result['variant_count']}`개 변형과 `{result['attempt_count']}`개 시도를 만들었고, "
            "source variant(원천 변형)가 없는 축은 gap register(공백 등록부)에 남겼다."
        ),
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    for path, status_prefix in (
        (SELECTION_STATUS_PATH, "- stage_status(단계 상태):"),
        (REVIEW_INDEX_PATH, "- status(상태):"),
    ):
        text = read_text(path)
        text = replace_line_prefix(text, status_prefix, f"{status_prefix} {status_line}")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = append_after_contains(text, "run267S_pool_wide_orthogonal_stability_racing_matrix", report_line)
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_block_once(
            text,
            "Run267T(267T 실행)는 후보군 전체 직교 안정성 MT5 시도를 물질화했다.",
            (
                "Run267T(267T 실행)는 후보군 전체 직교 안정성 MT5 시도를 물질화했다.\n"
                "Effect(효과): selected candidate(선택 후보) 없이 실행 대기 상태의 set/ini(설정/초기화), runtime contract(런타임 계약), gap register(공백 등록부)를 남겼다."
            ),
        )
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267T(267T 실행) pool-wide orthogonal stability MT5 attempts"
        f"(후보군 전체 직교 안정성 MT5 시도) `{STATUS}`. Effect(효과): run267S(267S 실행) 행렬에서 "
        f"`{result['variant_count']}`개 변형과 `{result['attempt_count']}`개 set/ini(설정/초기화) 시도를 만들었고 "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267T_build_pool_wide_orthogonal_stability_mt5_attempts`이다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다.",
        1,
    )
    workspace = workspace.replace(
        "run267S(267S 실행) 행렬을 받아 다음 MT5(MetaTrader 5, 메타트레이더5) 물질화 후보를 만든다.",
        "run267T(267T 실행) 시도 목록을 MT5(MetaTrader 5, 메타트레이더5) batch(묶음)로 실행한다.",
        1,
    )
    workspace = workspace.replace(
        "  status: run267S_pool_wide_orthogonal_stability_racing_matrix_materialized",
        f"  status: {STATUS}",
        1,
    )
    workspace = workspace.replace(f"  current_run_id: {PARENT_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {PARENT_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = append_after_contains(
        workspace,
        "run267S_pool_wide_orthogonal_stability_racing_matrix_path",
        f"  run267T_pool_wide_orthogonal_stability_mt5_attempts_path: {rel(REPORT_PATH)}",
    )
    workspace = workspace.replace(
        "  next_action: run267T_build_pool_wide_orthogonal_stability_mt5_attempts",
        f"  next_action: {NEXT_ACTION}",
        1,
    )
    workspace = workspace.replace(
        "active_run267S_pool_wide_orthogonal_stability_racing_matrix_materialized(267S 후보군 전체 직교 안정성 경주 행렬 물질화 완료, 다음 MT5 물질화 대기 활성)",
        "active_run267T_pool_wide_orthogonal_stability_mt5_attempts_built_execution_pending(267T 후보군 전체 직교 안정성 MT5 시도 물질화 완료, 실행 대기 활성)",
        1,
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_current_docs(result)
    print(
        json.dumps(
            {
                "status": STATUS,
                "variant_count": result["variant_count"],
                "attempt_count": result["attempt_count"],
                "gap_count": result["gap_count"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
