from __future__ import annotations

import csv
import io
import json
import math
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, export_mt5_feature_matrix_csv, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db as hi  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db as hh  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as basepkg  # noqa: E402
from stage_pipelines.stage364 import train_h17_density_failure_regime_behavior_reseed_without_db as dt  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db as gz  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db as hf  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db as hb  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-08"
STAGE_ID = hh.STAGE_ID
RUN_NUMBER = "run364HJ"
RUN_ID = "run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1"
PARENT_RUN_ID = hi.RUN_ID
SOURCE_CAPABILITY_RUN_ID = hh.RUN_ID
SOURCE_PROXY_RUN_ID = hf.RUN_ID
NEXT_RUN_ID = "run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364HJ_probability_bin_veto_runtime_package_materialized_mt5_probe_required_no_authority"
JUDGMENT = "runtime_package_materialized_probability_bin_veto_mt5_probe_required_no_authority"
DECISION = "stage364HJ_open_run364HK_probability_bin_veto_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "runtime_probe_package_only_probability_bin_veto_dual_source_partial_route_no_mt5_execution_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

PRIMARY_MODEL_ID = "gz_cost_h2_m0p32__gz_joint_frontier_blend__rf9_l20_n176"
FALLBACK_MODEL_ID = "hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192"
PRIMARY_FEATURE_SET_ID = "gz_joint_frontier_blend"
FALLBACK_FEATURE_SET_ID = "hb_oos_profit_density_bridge"
PRIMARY_ATTEMPT = "run364HJ_probability_bin_veto_dual_source_runtime_probe"
OUTPUT_CONTRACT = "p_short_p_flat_p_long_probability_tensor_threshold_margin_probability_bin_veto"
DEFAULT_METAEDITOR = basepkg.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"

STAGE_DIR = hh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
PRIMARY_FEATURE_MATRIX = RUN_DIR / "primary_gz_feature_matrix.csv"
FALLBACK_FEATURE_MATRIX = RUN_DIR / "fallback_hb_feature_matrix.csv"
FEATURE_ORDER_CONTRACT = RUN_DIR / "feature_order_contract.json"
FEATURE_MATRIX_AUDIT = RUN_DIR / "feature_matrix_audit.csv"
MT5_ONNX_DIR = RUN_DIR / "onnx_mt5"
PRIMARY_MT5_ONNX = MT5_ONNX_DIR / f"{PRIMARY_MODEL_ID}_mt5_probability_tensor.onnx"
FALLBACK_MT5_ONNX = MT5_ONNX_DIR / f"{FALLBACK_MODEL_ID}_mt5_probability_tensor.onnx"
MT5_ONNX_AUDIT = RUN_DIR / "mt5_onnx_contract_audit.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
RUNTIME_PACKAGE_MANIFEST = RUN_DIR / "runtime_package_manifest.json"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = MT5_DIR / "compile" / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
RUN364HK_EXECUTION_QUEUE = RUN_DIR / "run364HK_execution_queue.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUNTIME_REPRESENTATION_AUDIT = RUN_DIR / "runtime_representation_audit.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
WORK_PACKET_RECEIPT = RUN_DIR / "work_packet_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ENV_RECEIPT = RUN_DIR / "environment_reproducibility_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HJ_probability_bin_veto_runtime_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HJ_probability_bin_veto_runtime_package.md"
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
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

PRIMARY_SOURCE_ONNX = STAGE_DIR / "02_runs" / "run364GZ" / "onnx" / "gz_cost_h2_m0p32_gz_joint_frontier_blend_rf9_l20_n176.onnx"
PRIMARY_SOURCE_JOBLIB = STAGE_DIR / "02_runs" / "run364GZ" / "models" / "gz_cost_h2_m0p32_gz_joint_frontier_blend_rf9_l20_n176.joblib"
FALLBACK_SOURCE_ONNX = STAGE_DIR / "02_runs" / "run364HB" / "onnx" / "hb_rebalance_h2_m0p26_hb_oos_profit_density_bridge_rf9_l20_n192.onnx"
FALLBACK_SOURCE_JOBLIB = STAGE_DIR / "02_runs" / "run364HB" / "models" / "hb_rebalance_h2_m0p26_hb_oos_profit_density_bridge_rf9_l20_n192.joblib"
SOURCE_EA = basepkg.EA_SOURCE
SOURCE_EA_BINARY = basepkg.EA_BINARY
PORTABLE_EA_EX5 = basepkg.PORTABLE_EA_EX5
MODEL_INPUT_DATASET = dt.dp.MODEL_INPUT_DATASET
MODEL_INPUT_FEATURE_ORDER = dt.dp.MODEL_INPUT_FEATURE_ORDER

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_probability_bin_veto_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    hi.FINAL_DECISION,
    hi.GATE_AUDIT,
    hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT,
    hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON,
    hi.MODULE_HASHES,
    hi.MT5_COMPILE_RESULT,
    hh.FINAL_DECISION,
    hh.GATE_AUDIT,
    hh.SOURCE_MODEL_RUNTIME_MANIFEST,
    hh.VETO_RULE_MANIFEST,
    hh.PROBABILITY_BIN_EDGES,
    hh.EXPECTED_TRADE_TAPE,
    hh.EXPECTED_ROUTE_SUMMARY,
    hh.RUNTIME_PARITY_CONTRACT,
    hf.SELECTED_CANDIDATE,
    hf.SELECTED_TRADE_TAPE,
    hf.MODEL_ARTIFACT_MANIFEST,
    gz.SELECTED_CANDIDATE,
    gz.FEATURE_AUDIT,
    hb.SELECTED_CANDIDATE,
    hb.FEATURE_AUDIT,
    PRIMARY_SOURCE_ONNX,
    PRIMARY_SOURCE_JOBLIB,
    FALLBACK_SOURCE_ONNX,
    FALLBACK_SOURCE_JOBLIB,
    MODEL_INPUT_DATASET,
    MODEL_INPUT_FEATURE_ORDER,
    SOURCE_EA,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    PRIMARY_FEATURE_MATRIX,
    FALLBACK_FEATURE_MATRIX,
    FEATURE_ORDER_CONTRACT,
    FEATURE_MATRIX_AUDIT,
    PRIMARY_MT5_ONNX,
    FALLBACK_MT5_ONNX,
    MT5_ONNX_AUDIT,
    RUNTIME_POLICY_CONFIG,
    RUNTIME_PACKAGE_MANIFEST,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    RUN364HK_EXECUTION_QUEUE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    RUNTIME_REPRESENTATION_AUDIT,
    EXPECTED_KPI_SUMMARY,
    WORK_PACKET_RECEIPT,
    RUNTIME_RECEIPT,
    BACKTEST_RECEIPT,
    ENV_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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
    NEGATIVE_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def rel(path: Path | str) -> str:
    return Path(path).resolve().relative_to(ROOT).as_posix()


def sha(path: Path | str) -> str:
    import hashlib

    digest = hashlib.sha256()
    with io_path(Path(path)).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        writer.writerows([{key: row.get(key, "") for key in fieldnames} for row in rows])


def append_text_once(path: Path, marker: str, text: str, *, bom: bool = True) -> None:
    current = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n" + text.lstrip(), bom=bom)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    current_rows = read_csv_rows(path)
    existing_fieldnames: list[str] = []
    if exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            existing_fieldnames = list(csv.DictReader(handle).fieldnames or [])
    fieldnames = list(existing_fieldnames)
    if extend_header:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    elif not fieldnames and rows:
        fieldnames = list(rows[0].keys())
    incoming = {tuple(str(row.get(key, "")) for key in key_fields): row for row in rows}
    kept = [row for row in current_rows if tuple(str(row.get(key, "")) for key in key_fields) not in incoming]
    merged = kept + list(rows)
    write_csv(path, merged, fieldnames)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    if not exists(path):
        return
    lines = io_path(path).read_text(encoding="utf-8-sig").splitlines()
    updated: list[str] = []
    for line in lines:
        updated.append(next((replacement for prefix, replacement in replacements.items() if line.startswith(prefix)), line))
    write_text(path, "\n".join(updated) + "\n", bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() in {"inf", "infinity"}:
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
    for path in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent, MT5_ONNX_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    hi_final = read_json(hi.FINAL_DECISION)
    if hi_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(상위 다음 실행 불일치): {hi_final.get('next_run_id')} != {RUN_ID}")
    if hi_final.get("runtime_authority") != "not_claimed" or hi_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(상위 실행에 금지된 운영 주장이 있습니다)")
    for gate_path, label in [(hi.GATE_AUDIT, "HI"), (hh.GATE_AUDIT, "HH")]:
        gates = read_csv_rows(gate_path)
        if not gates or any(row.get("status") != "passed" for row in gates):
            raise RuntimeError(f"{label} gates not fully passed({label} 게이트가 모두 통과하지 않았습니다)")
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HJ inputs(HJ 입력 누락): " + ", ".join(missing[:30]))
    return hi_final


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        name = Path(path).name
        role = "source_input(원천 입력)"
        if "onnx" in name:
            role = "source_onnx_model(원천 온엑스 모델)"
        elif "feature" in name:
            role = "feature_contract_or_matrix(피처 계약 또는 행렬)"
        elif "veto" in name:
            role = "probability_bin_veto_contract(확률 구간 거부 계약)"
        elif name.endswith(".json"):
            role = "decision_or_receipt(결정 또는 영수증)"
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and io_path(Path(path)).is_file() else "",
                "role": role,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def load_selected() -> dict[str, Any]:
    hf_final = read_json(hf.SELECTED_CANDIDATE)
    gz_final = read_json(gz.SELECTED_CANDIDATE)
    hb_final = read_json(hb.SELECTED_CANDIDATE)
    veto_params = read_json(hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON)["parameters"]
    source_models = read_csv_rows(hh.SOURCE_MODEL_RUNTIME_MANIFEST)
    return {"hf": hf_final, "gz": gz_final, "hb": hb_final, "veto_params": veto_params, "source_models": source_models}


def materialize_feature_matrices() -> dict[str, Any]:
    base_feature_order = dt.load_feature_order()
    frame = dt.load_dataset(base_feature_order)
    primary_order = gz.gz_feature_sets(base_feature_order)[PRIMARY_FEATURE_SET_ID]
    fallback_order = hb.hb_feature_sets(base_feature_order)[FALLBACK_FEATURE_SET_ID]
    missing_primary = [column for column in primary_order if column not in frame.columns]
    missing_fallback = [column for column in fallback_order if column not in frame.columns]
    if missing_primary or missing_fallback:
        raise RuntimeError("feature columns missing(피처 열 누락): " + ", ".join((missing_primary + missing_fallback)[:30]))
    if len(primary_order) != 60:
        raise RuntimeError(f"primary feature count mismatch(우선 피처 수 불일치): {len(primary_order)} != 60")
    if len(fallback_order) != 56:
        raise RuntimeError(f"fallback feature count mismatch(대체 피처 수 불일치): {len(fallback_order)} != 56")
    probe_frame = frame[frame["split"].astype(str).isin(["validation", "oos"])].copy()
    if probe_frame.empty:
        raise RuntimeError("validation/oos rows missing(검증/표본외 행 누락)")
    metadata = ["entry_open", "open", "high", "low", "close", "volume"]
    primary_export = export_mt5_feature_matrix_csv(probe_frame, primary_order, PRIMARY_FEATURE_MATRIX, timestamp_column="timestamp", metadata_columns=metadata)
    fallback_export = export_mt5_feature_matrix_csv(probe_frame, fallback_order, FALLBACK_FEATURE_MATRIX, timestamp_column="timestamp", metadata_columns=metadata)
    payload = {
        "run_id": RUN_ID,
        "model_input_dataset": rel(MODEL_INPUT_DATASET),
        "model_input_dataset_sha256": sha(MODEL_INPUT_DATASET),
        "base_feature_order": rel(MODEL_INPUT_FEATURE_ORDER),
        "base_feature_order_hash": ordered_hash(base_feature_order),
        "primary": {
            "model_id": PRIMARY_MODEL_ID,
            "feature_set_id": PRIMARY_FEATURE_SET_ID,
            "feature_count": len(primary_order),
            "feature_order_hash": ordered_hash(primary_order),
            "feature_columns": primary_order,
            "matrix": rel(PRIMARY_FEATURE_MATRIX),
            "matrix_sha256": sha(PRIMARY_FEATURE_MATRIX),
            "export": primary_export,
        },
        "fallback": {
            "model_id": FALLBACK_MODEL_ID,
            "feature_set_id": FALLBACK_FEATURE_SET_ID,
            "feature_count": len(fallback_order),
            "feature_order_hash": ordered_hash(fallback_order),
            "feature_columns": fallback_order,
            "matrix": rel(FALLBACK_FEATURE_MATRIX),
            "matrix_sha256": sha(FALLBACK_FEATURE_MATRIX),
            "export": fallback_export,
        },
        "split_scope": "validation+oos(검증+표본외)",
        "timestamp_semantics": "bar_time_server is closed M5 bar close time(닫힌 5분봉 종료 시각)",
        "effect": "primary/fallback feature CSV(우선/대체 피처 CSV)를 각각 ONNX 입력 차원에 맞게 고정합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_ORDER_CONTRACT, payload)
    write_csv(
        FEATURE_MATRIX_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "route_role": "primary_anchor(우선 기준)",
                "model_id": PRIMARY_MODEL_ID,
                "feature_set_id": PRIMARY_FEATURE_SET_ID,
                "feature_count": len(primary_order),
                "feature_order_hash": payload["primary"]["feature_order_hash"],
                "rows": primary_export["rows"],
                "matrix_path": rel(PRIMARY_FEATURE_MATRIX),
                "matrix_sha256": sha(PRIMARY_FEATURE_MATRIX),
                "timestamp_semantics": payload["timestamp_semantics"],
                "effect": "GZ 우선 모델 입력을 MT5 CSV handoff(MT5 CSV 인계)로 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "route_role": "fallback_profit(수익 대체)",
                "model_id": FALLBACK_MODEL_ID,
                "feature_set_id": FALLBACK_FEATURE_SET_ID,
                "feature_count": len(fallback_order),
                "feature_order_hash": payload["fallback"]["feature_order_hash"],
                "rows": fallback_export["rows"],
                "matrix_path": rel(FALLBACK_FEATURE_MATRIX),
                "matrix_sha256": sha(FALLBACK_FEATURE_MATRIX),
                "timestamp_semantics": payload["timestamp_semantics"],
                "effect": "HB 대체 모델 입력을 MT5 CSV handoff(MT5 CSV 인계)로 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    return payload


def materialize_mt5_compatible_onnx(source: Path, output: Path, model_id: str, role: str) -> dict[str, Any]:
    import onnx
    from onnx import TensorProto, helper

    model = onnx.load_model_from_string(io_path(source).read_bytes())
    outputs_before = [{"name": output_value.name, "value_type": output_value.type.WhichOneof("value")} for output_value in model.graph.output]
    zipmap_nodes = [node for node in model.graph.node if node.op_type == "ZipMap"]
    probability_tensor_name = "probabilities"
    if zipmap_nodes:
        probability_tensor_name = zipmap_nodes[0].input[0]
        kept_nodes = [node for node in model.graph.node if node.op_type != "ZipMap"]
        del model.graph.node[:]
        model.graph.node.extend(kept_nodes)
    del model.graph.output[:]
    model.graph.output.extend([helper.make_tensor_value_info(probability_tensor_name, TensorProto.FLOAT, [None, 3])])
    onnx.checker.check_model(model)
    io_path(output.parent).mkdir(parents=True, exist_ok=True)
    io_path(output).write_bytes(model.SerializeToString())
    outputs_after = [{"name": output_value.name, "value_type": output_value.type.WhichOneof("value")} for output_value in model.graph.output]
    return {
        "run_id": RUN_ID,
        "route_role": role,
        "model_id": model_id,
        "source_onnx": rel(source),
        "source_sha256": sha(source),
        "mt5_compatible_onnx": rel(output),
        "mt5_onnx_sha256": sha(output),
        "zipmap_removed": bool(zipmap_nodes),
        "probability_tensor_name": probability_tensor_name,
        "outputs_before": json.dumps(outputs_before, ensure_ascii=False),
        "outputs_after": json.dumps(outputs_after, ensure_ascii=False),
        "effect": "ZipMap(집맵)을 제거해 MT5가 probability tensor(확률 텐서)를 직접 읽게 합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def materialize_onnx_pair() -> list[dict[str, Any]]:
    rows = [
        materialize_mt5_compatible_onnx(PRIMARY_SOURCE_ONNX, PRIMARY_MT5_ONNX, PRIMARY_MODEL_ID, "primary_anchor(우선 기준)"),
        materialize_mt5_compatible_onnx(FALLBACK_SOURCE_ONNX, FALLBACK_MT5_ONNX, FALLBACK_MODEL_ID, "fallback_profit(수익 대체)"),
    ]
    write_csv(MT5_ONNX_AUDIT, rows)
    return rows


def compile_log_ok() -> bool:
    if not exists(COMPILE_LOG):
        return False
    raw = io_path(COMPILE_LOG).read_bytes()
    texts = [raw.decode(encoding, errors="replace") for encoding in ["utf-8-sig", "utf-16", "utf-16-le"]]
    return any("Result: 0 errors" in text.replace("\x00", "") for text in texts)


def compile_and_sync_ea() -> dict[str, Any]:
    result = compile_mql5_ea(DEFAULT_METAEDITOR, SOURCE_EA, COMPILE_LOG)
    ok = compile_log_ok()
    payload = {
        "run_id": RUN_ID,
        "metaeditor": DEFAULT_METAEDITOR.as_posix(),
        "source_ea": rel(SOURCE_EA),
        "source_ea_binary": rel(SOURCE_EA_BINARY),
        "portable_ea_binary": PORTABLE_EA_EX5.as_posix(),
        "compile_result": result,
        "compile_log_zero_errors": ok,
        "portable_copied": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if ok and exists(SOURCE_EA_BINARY):
        io_path(PORTABLE_EA_EX5.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(SOURCE_EA_BINARY), io_path(PORTABLE_EA_EX5))
        payload.update({"portable_copied": True, "source_sha256": sha(SOURCE_EA_BINARY), "portable_sha256": sha(PORTABLE_EA_EX5)})
    write_json(COMPILE_RESULT, payload)
    write_json(PORTABLE_EA_SYNC, payload)
    return payload


def copy_common(local_path: Path, common_path: str, role: str, effect: str) -> dict[str, Any]:
    result = copy_to_common_files(basepkg.DEFAULT_COMMON_FILES, local_path, common_path)
    return {
        "run_id": RUN_ID,
        "artifact_role": role,
        "local_path": rel(local_path),
        "local_sha256": sha(local_path),
        "common_path": result["common_path"],
        "common_absolute_path": result["absolute_path"],
        "common_sha256": result["sha256"],
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def common_sync_rows() -> list[dict[str, Any]]:
    rows = [
        copy_common(PRIMARY_FEATURE_MATRIX, f"{COMMON_FEATURE_DIR}/primary_gz_features.csv", "common_primary_feature_matrix", "GZ primary feature matrix(GZ 우선 피처 행렬)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(FALLBACK_FEATURE_MATRIX, f"{COMMON_FEATURE_DIR}/fallback_hb_features.csv", "common_fallback_feature_matrix", "HB fallback feature matrix(HB 대체 피처 행렬)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(PRIMARY_MT5_ONNX, f"{COMMON_MODEL_DIR}/{PRIMARY_MODEL_ID}.onnx", "common_primary_onnx", "GZ primary ONNX(GZ 우선 온엑스)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(FALLBACK_MT5_ONNX, f"{COMMON_MODEL_DIR}/{FALLBACK_MODEL_ID}.onnx", "common_fallback_onnx", "HB fallback ONNX(HB 대체 온엑스)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(FEATURE_ORDER_CONTRACT, f"{COMMON_CONFIG_DIR}/feature_order_contract.json", "common_feature_order_contract", "feature order contract(피처 순서 계약)을 Common Files(공용 파일)에 복사합니다."),
        copy_common(hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON, f"{COMMON_CONFIG_DIR}/probability_bin_veto_parameter_contract.json", "common_probability_bin_veto_contract", "probability-bin veto contract(확률 구간 거부 계약)을 Common Files(공용 파일)에 복사합니다."),
        copy_common(hh.EXPECTED_TRADE_TAPE, f"{COMMON_EXPECTED_DIR}/expected_trade_tape.csv", "common_expected_trade_tape", "expected proxy tape(예상 프록시 테이프)를 비교 입력으로 복사합니다."),
        copy_common(hh.EXPECTED_ROUTE_SUMMARY, f"{COMMON_EXPECTED_DIR}/expected_route_summary.csv", "common_expected_route_summary", "expected route summary(예상 라우트 요약)를 비교 입력으로 복사합니다."),
    ]
    write_csv(COMMON_FILES_SYNC, rows)
    return rows


def materialize_set_and_ini(selected: Mapping[str, Any], feature_payload: Mapping[str, Any]) -> dict[str, Any]:
    common_primary_feature = f"{COMMON_FEATURE_DIR}/primary_gz_features.csv"
    common_fallback_feature = f"{COMMON_FEATURE_DIR}/fallback_hb_features.csv"
    common_primary_model = f"{COMMON_MODEL_DIR}/{PRIMARY_MODEL_ID}.onnx"
    common_fallback_model = f"{COMMON_MODEL_DIR}/{FALLBACK_MODEL_ID}.onnx"
    common_telemetry = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv"
    common_summary = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv"
    hf_final = selected["hf"]
    gz_final = selected["gz"]
    hb_final = selected["hb"]
    veto_params = selected["veto_params"]
    primary_threshold = as_float(gz_final["selected_threshold"])
    primary_margin = as_float(gz_final["selected_margin_vs_flat"])
    fallback_threshold = 0.476377199026
    fallback_margin = -0.14
    set_values: dict[str, Any] = {
        "InpRunId": f"{RUN_ID}_{PRIMARY_ATTEMPT}",
        "InpExplorationLabel": "stage364HJ__ProbabilityBinVetoRuntimeProbe",
        "InpTierLabel": "Tier A primary + Tier B fallback",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_probability_bin_veto",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": common_primary_feature,
        "InpFeatureCount": int(feature_payload["primary"]["feature_count"]),
        "InpFeatureCsvUseCommonFiles": True,
        "InpFeatureRequireTimestampMatch": True,
        "InpFeatureAllowLatestFallback": False,
        "InpFeatureStrictHeader": True,
        "InpFeatureCsvDelimiter": ",",
        "InpCsvTimestampIsBarClose": True,
        "InpModelPath": common_primary_model,
        "InpModelId": PRIMARY_MODEL_ID,
        "InpModelBackend": "onnx",
        "InpModelUseCommonFiles": True,
        "InpModelUseCpuOnly": True,
        "InpModelNoConversion": False,
        "InpSetOutputShape": True,
        "InpModelUseMatrixTensor": False,
        "InpFeatureOrderHash": feature_payload["primary"]["feature_order_hash"],
        "InpFallbackEnabled": True,
        "InpFallbackTierLabel": "Tier B fallback",
        "InpFallbackFeatureCsvPath": common_fallback_feature,
        "InpFallbackFeatureCount": int(feature_payload["fallback"]["feature_count"]),
        "InpFallbackModelPath": common_fallback_model,
        "InpFallbackModelId": FALLBACK_MODEL_ID,
        "InpFallbackModelBackend": "onnx",
        "InpFallbackFeatureOrderHash": feature_payload["fallback"]["feature_order_hash"],
        "InpFallbackUseOnPrimaryFlat": True,
        "InpFallbackPrimaryFlatRequiresNoPosition": True,
        "InpFallbackUseOnPrimaryLowConfidence": False,
        "InpFallbackPrimaryMaxConfidence": 0.0,
        "InpFallbackLowConfidenceRequiresNoPosition": True,
        "InpShortThreshold": primary_threshold,
        "InpLongThreshold": primary_threshold,
        "InpMinMargin": primary_margin,
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpFallbackShortThreshold": fallback_threshold,
        "InpFallbackLongThreshold": fallback_threshold,
        "InpFallbackMinMargin": fallback_margin,
        "InpFallbackDecisionMode": "threshold_margin",
        "InpFallbackInvertSignal": False,
        "InpEntryMarginFloor": 0.0,
        "InpProbabilityBinVetoEnabled": str(veto_params["InpProbabilityBinVetoEnabled"]).lower() == "true",
        "InpProbabilityBinVetoPFlatEdges": veto_params["InpProbabilityBinVetoPFlatEdges"],
        "InpProbabilityBinVetoShortLongGapEdges": veto_params["InpProbabilityBinVetoShortLongGapEdges"],
        "InpProbabilityBinVetoRules": veto_params["InpProbabilityBinVetoRules"],
        "InpTimeMarginGuardEnabled": False,
        "InpCalendarBlockEnabled": False,
        "InpSyntheticShortSourceEnabled": False,
        "InpSyntheticShortMonthBlockEnabled": False,
        "InpAllowTrading": True,
        "InpFixedLot": 0.1,
        "InpModelRiskFallbackLot": 0.1,
        "InpModelRiskSizingEnabled": False,
        "InpRiskScaleOverlayEnabled": False,
        "InpMagic": 36451001,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": 2,
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpEntryTransitionOnly": False,
        "InpTelemetryEnabled": True,
        "InpTelemetryUseCommonFiles": True,
        "InpTelemetryCsvPath": common_telemetry,
        "InpSummaryCsvPath": common_summary,
    }
    set_path = SET_DIR / "OPv2_run364HJ_probability_bin_veto.set"
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    report_name = "Project_Obsidian_Prime_v2_run364HK_probability_bin_veto_runtime_probe"
    ini_path = INI_DIR / "OPv2_run364HJ_probability_bin_veto.ini"
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            expert="Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5",
            symbol="US100",
            period="M5",
            model=4,
            deposit=500.0,
            leverage="1:100",
            from_date="2025.01.02",
            to_date="2026.04.14",
            report=report_name,
        ),
        ini_path,
        set_file_path=Path(set_path.name),
    )
    write_csv(
        TESTER_SET_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "primary_model_id": PRIMARY_MODEL_ID,
                "fallback_model_id": FALLBACK_MODEL_ID,
                "primary_feature_count": feature_payload["primary"]["feature_count"],
                "fallback_feature_count": feature_payload["fallback"]["feature_count"],
                "primary_threshold": primary_threshold,
                "primary_margin_vs_flat": primary_margin,
                "fallback_threshold": fallback_threshold,
                "fallback_margin_vs_flat": fallback_margin,
                "probability_bin_veto_rules": veto_params["InpProbabilityBinVetoRules"],
                "expected_oos_net": hf_final["selected_oos_net"],
                "expected_oos_profit_factor": hf_final["selected_oos_profit_factor"],
                "expected_oos_trade_density": hf_final["selected_oos_trade_density"],
                "runtime_representation": "partial_route_supported(부분 라우트 지원)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_INI_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
                "report_name": report_name,
                "from_date": "2025.01.02",
                "to_date": "2026.04.14",
                "effect": "Strategy Tester(전략 테스터) 실행 범위와 report(보고서) 이름을 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    oos_split = next(
        (
            row
            for row in read_csv_rows(hh.EXPECTED_ROUTE_SUMMARY)
            if row.get("view", "").startswith("split_total") and row.get("split") == "oos"
        ),
        {},
    )
    return {
        "set_path": set_path,
        "ini_path": ini_path,
        "set_sha256": set_payload["sha256"],
        "ini_sha256": ini_payload["sha256"],
        "parameter_count": set_payload["parameter_count"],
        "report_name": report_name,
        "primary_threshold": primary_threshold,
        "primary_margin_vs_flat": primary_margin,
        "fallback_threshold": fallback_threshold,
        "fallback_margin_vs_flat": fallback_margin,
        "expected_oos_net": hf_final["selected_oos_net"],
        "expected_oos_profit_factor": hf_final["selected_oos_profit_factor"],
        "expected_oos_trade_density": hf_final["selected_oos_trade_density"],
        "expected_oos_trade_count": hf_final["selected_oos_trade_count"],
        "expected_oos_long_trade_count": oos_split.get("long_trade_count", ""),
        "expected_oos_short_trade_count": oos_split.get("short_trade_count", ""),
    }


def write_contracts(selected: Mapping[str, Any], feature_payload: Mapping[str, Any], package: Mapping[str, Any], sync_rows: Sequence[Mapping[str, Any]]) -> None:
    hf_final = selected["hf"]
    runtime_policy = {
        "run_id": RUN_ID,
        "primary_model_id": PRIMARY_MODEL_ID,
        "fallback_model_id": FALLBACK_MODEL_ID,
        "feature_contract": "primary 60 features + fallback 56 features(우선 60개 피처 + 대체 56개 피처)",
        "output_contract": OUTPUT_CONTRACT,
        "probability_bin_veto": selected["veto_params"],
        "expected_proxy_oos": {
            "net_profit": hf_final["selected_oos_net"],
            "profit_factor": hf_final["selected_oos_profit_factor"],
            "trade_count": hf_final["selected_oos_trade_count"],
            "trade_density": hf_final["selected_oos_trade_density"],
        },
        "known_differences": [
            "HF Python router(HF 파이썬 라우터)는 score_plus_0p02(점수 0.02 추가) switch(전환)를 사용하지만 EA(전문가 자문)는 primary flat(우선 flat) 이후 fallback(대체)을 시도합니다.",
            "MT5 fill/spread/position timing(MT5 체결/스프레드/포지션 시점)은 Python open-to-open proxy(Python 시가-시가 프록시)와 다를 수 있습니다.",
            "MT5 Strategy Tester output(MT5 전략 테스터 출력)은 HK 실행 전까지 없습니다.",
            "Expected OOS trade density(예상 표본외 거래 밀도)는 3/day(일 3회) 목표보다 낮아 운영 후보가 아니라 runtime capability probe(런타임 기능 탐침)입니다.",
        ],
        "effect": "runtime policy(런타임 정책)를 set/ini(설정/초기화 파일)와 같은 의미로 연결합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, runtime_policy)
    write_json(
        RUNTIME_PACKAGE_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "tester_set": rel(package["set_path"]),
            "tester_ini": rel(package["ini_path"]),
            "common_files_sync": rel(COMMON_FILES_SYNC),
            "runtime_policy_config": rel(RUNTIME_POLICY_CONFIG),
            "feature_order_contract": rel(FEATURE_ORDER_CONTRACT),
            "primary_mt5_onnx": rel(PRIMARY_MT5_ONNX),
            "fallback_mt5_onnx": rel(FALLBACK_MT5_ONNX),
            "module_hashes": mt5_runtime_module_hashes(),
            "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(
        MODEL_HANDOFF_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "route_role": "primary_anchor(우선 기준)",
                "model_id": PRIMARY_MODEL_ID,
                "source_onnx": rel(PRIMARY_SOURCE_ONNX),
                "source_onnx_sha256": sha(PRIMARY_SOURCE_ONNX),
                "mt5_compatible_onnx": rel(PRIMARY_MT5_ONNX),
                "mt5_onnx_sha256": sha(PRIMARY_MT5_ONNX),
                "joblib_path": rel(PRIMARY_SOURCE_JOBLIB),
                "joblib_sha256": sha(PRIMARY_SOURCE_JOBLIB),
                "feature_count": feature_payload["primary"]["feature_count"],
                "feature_order_hash": feature_payload["primary"]["feature_order_hash"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "route_role": "fallback_profit(수익 대체)",
                "model_id": FALLBACK_MODEL_ID,
                "source_onnx": rel(FALLBACK_SOURCE_ONNX),
                "source_onnx_sha256": sha(FALLBACK_SOURCE_ONNX),
                "mt5_compatible_onnx": rel(FALLBACK_MT5_ONNX),
                "mt5_onnx_sha256": sha(FALLBACK_MT5_ONNX),
                "joblib_path": rel(FALLBACK_SOURCE_JOBLIB),
                "joblib_sha256": sha(FALLBACK_SOURCE_JOBLIB),
                "feature_count": feature_payload["fallback"]["feature_count"],
                "feature_order_hash": feature_payload["fallback"]["feature_order_hash"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    write_csv(
        RUNTIME_REPRESENTATION_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "item": "probability_bin_veto(확률 구간 거부)",
                "source_meaning": "veto open_hour+pflat_bin+sl_gap_bin groups(진입 시간+평탄확률 구간+숏롱차 구간 거부)",
                "runtime_meaning": "ProbabilityBinVeto.mqh applies same pd.cut bin semantics(동일 pd.cut 구간 의미 적용)",
                "status": "represented(표현됨)",
                "known_difference": "",
                "effect": "검증 손실 구간 차단을 MT5에서 관찰할 수 있게 합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "item": "dual_source_route(이중 원천 라우트)",
                "source_meaning": "HF score_plus_0p02 switch router(HF 점수 0.02 추가 전환 라우터)",
                "runtime_meaning": "EA fallback after primary flat only(EA는 우선 flat 뒤 대체만 시도)",
                "status": "partial_represented(부분 표현)",
                "known_difference": "generic score switch not implemented(일반 점수 전환 미구현)",
                "effect": "HK에서 proxy-vs-MT5 차이를 정량화해야 합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "item": "trade_density_goal(거래 밀도 목표)",
                "source_meaning": "current HF expected OOS density is below 3/day(현재 HF 예상 표본외 밀도는 일 3회 미만)",
                "runtime_meaning": "runtime capability package only(런타임 기능 패키지 전용)",
                "status": "not_operating_candidate(운영 후보 아님)",
                "known_difference": "user goal requires 3/day or more(사용자 목표는 일 3회 이상)",
                "effect": "좋은 백테스트 조각을 최종 운영 후보로 오해하지 않습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    write_json(
        RUNTIME_PARITY_CONTRACT,
        {
            "run_id": RUN_ID,
            "research_path": rel(hf.SELECTED_CANDIDATE),
            "runtime_path": rel(package["set_path"]),
            "shared_contract": {
                "symbol": "US100",
                "timeframe": "M5",
                "output_order": ["p_short", "p_flat", "p_long"],
                "primary_feature_count": feature_payload["primary"]["feature_count"],
                "fallback_feature_count": feature_payload["fallback"]["feature_count"],
                "probability_bin_veto": selected["veto_params"],
                "max_hold_bars": 2,
                "fixed_lot": 0.1,
            },
            "known_differences": runtime_policy["known_differences"],
            "parity_check": rel(RUNTIME_REPRESENTATION_AUDIT),
            "parity_identity": {
                "tester_set_sha256": package["set_sha256"],
                "tester_ini_sha256": package["ini_sha256"],
                "primary_mt5_onnx_sha256": sha(PRIMARY_MT5_ONNX),
                "fallback_mt5_onnx_sha256": sha(FALLBACK_MT5_ONNX),
                "runtime_module_hashes": mt5_runtime_module_hashes(),
            },
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_csv(
        PROXY_MT5_COMPARISON_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "comparison_subject": "expected_trade_tape_vs_runtime_telemetry(예상 거래 테이프 대 런타임 기록)",
                "proxy_input": rel(hh.EXPECTED_TRADE_TAPE),
                "mt5_runtime_output": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv",
                "required_next_run": NEXT_RUN_ID,
                "diff_axes": "matched_rows,mismatch_rows,net_profit,profit_factor,trade_count,side_mix,skip_reason(일치 행/불일치 행/순수익/수익 팩터/거래수/방향 비율/스킵 사유)",
                "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하게 합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_IDENTITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "tester_model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "symbol": "US100",
                "period": "M5",
                "set_path": rel(package["set_path"]),
                "ini_path": rel(package["ini_path"]),
                "report_name": package["report_name"],
                "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
                "effect": "Strategy Tester(전략 테스터) 정체성을 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    route_summary = read_csv_rows(hh.EXPECTED_ROUTE_SUMMARY)
    write_csv(
        EXPECTED_KPI_SUMMARY,
        [
            {
                "run_id": RUN_ID,
                "view": row.get("view", ""),
                "split": row.get("split", ""),
                "route_role": row.get("route_role", ""),
                "trade_count": row.get("trade_count", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "expectancy": row.get("expectancy", ""),
                "long_trade_count": row.get("long_trade_count", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "effect": "expected proxy KPI(예상 프록시 핵심 성과 지표)를 HK 비교 기준으로 보존합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for row in route_summary
        ],
    )
    attempt_row = {
        "run_id": RUN_ID,
        "attempt_name": PRIMARY_ATTEMPT,
        "tier": "Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)",
        "split": "validation_oos",
        "tester_set": rel(package["set_path"]),
        "tester_ini": rel(package["ini_path"]),
        "runtime_policy": rel(RUNTIME_POLICY_CONFIG),
        "runtime_parity_contract": rel(RUNTIME_PARITY_CONTRACT),
        "proxy_mt5_comparison_contract": rel(PROXY_MT5_COMPARISON_CONTRACT),
        "common_files_sync": rel(COMMON_FILES_SYNC),
        "expected_trade_tape": rel(hh.EXPECTED_TRADE_TAPE),
        "expected_route_summary": rel(hh.EXPECTED_ROUTE_SUMMARY),
        "status": "ready_for_mt5_probe(MT5 탐침 준비)",
        "effect": "HK 실행이 읽을 tester handoff(테스터 인계)를 한 줄로 고정합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, [attempt_row])
    write_csv(
        RUN364HK_EXECUTION_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "hk01_execute_probability_bin_veto_mt5_runtime_probe",
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "tester_ini": rel(package["ini_path"]),
                "tester_set": rel(package["set_path"]),
                "comparison_contract": rel(PROXY_MT5_COMPARISON_CONTRACT),
                "effect": "다음 작업에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하도록 대기열을 만듭니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(package: Mapping[str, Any], compile_payload: Mapping[str, Any], receipt_paths: Sequence[Path], final_written: bool) -> list[dict[str, Any]]:
    common_paths = read_csv_rows(COMMON_FILES_SYNC)
    common_ok = bool(common_paths) and all(Path(row.get("common_absolute_path", "")).exists() for row in common_paths)
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), INPUT_MANIFEST, "입력 계보가 연결됐습니다."),
        ("feature_matrix_gate", exists(PRIMARY_FEATURE_MATRIX) and exists(FALLBACK_FEATURE_MATRIX) and exists(FEATURE_ORDER_CONTRACT), FEATURE_MATRIX_AUDIT, "primary/fallback feature CSV(우선/대체 피처 CSV)가 작성됐습니다."),
        ("onnx_handoff_gate", exists(PRIMARY_MT5_ONNX) and exists(FALLBACK_MT5_ONNX) and exists(MT5_ONNX_AUDIT), MT5_ONNX_AUDIT, "MT5-compatible ONNX handoff(MT5 호환 온엑스 인계)가 작성됐습니다."),
        ("probability_bin_veto_parameter_gate", exists(hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON), hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON, "probability-bin veto(확률 구간 거부) 파라미터가 연결됐습니다."),
        ("runtime_representation_gate", exists(RUNTIME_REPRESENTATION_AUDIT) and exists(RUNTIME_PARITY_CONTRACT), RUNTIME_REPRESENTATION_AUDIT, "runtime representation(런타임 표현)을 기록했습니다."),
        ("compile_gate", bool(compile_payload.get("compile_log_zero_errors")) and bool(compile_payload.get("portable_copied")), COMPILE_RESULT, "MetaEditor compile(메타에디터 컴파일) 오류 0개와 portable EA(휴대용 전문가 자문) 복사를 확인했습니다."),
        ("runtime_handoff_package_gate", exists(package["set_path"]) and exists(package["ini_path"]) and exists(RUNTIME_PROBE_ATTEMPT_PACKAGE), RUNTIME_PROBE_ATTEMPT_PACKAGE, "set/ini/attempt package(설정/초기화/시도 패키지)가 작성됐습니다."),
        ("common_files_sync_gate", common_ok, COMMON_FILES_SYNC, "Common Files(공용 파일) 복사가 확인됐습니다."),
        ("proxy_mt5_comparison_contract_gate", exists(PROXY_MT5_COMPARISON_CONTRACT), PROXY_MT5_COMPARISON_CONTRACT, "proxy vs MT5 비교 계약(프록시 대 MT5 비교 계약)이 작성됐습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), RUNTIME_RECEIPT, "필수 receipt(영수증)가 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 gate(게이트)가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "권위/승격/목표 주장을 하지 않았습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def final_payload(feature_payload: Mapping[str, Any], package: Mapping[str, Any], compile_payload: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    all_passed = all(row["status"] == "passed" for row in gates)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_capability_run_id": SOURCE_CAPABILITY_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID if all_passed else RUN_ID,
        "status": STATUS if all_passed else "blocked_stage364HJ_runtime_package_gate_failure_repair_required_no_authority",
        "judgment": JUDGMENT if all_passed else "inconclusive_runtime_package_gate_failure_repair_required_no_authority",
        "decision": DECISION if all_passed else "stage364HJ_repair_runtime_package_gate_failure",
        "primary_model_id": PRIMARY_MODEL_ID,
        "fallback_model_id": FALLBACK_MODEL_ID,
        "primary_feature_count": feature_payload["primary"]["feature_count"],
        "fallback_feature_count": feature_payload["fallback"]["feature_count"],
        "primary_feature_order_hash": feature_payload["primary"]["feature_order_hash"],
        "fallback_feature_order_hash": feature_payload["fallback"]["feature_order_hash"],
        "feature_matrix_rows": feature_payload["primary"]["export"]["rows"],
        "primary_mt5_onnx": rel(PRIMARY_MT5_ONNX),
        "primary_mt5_onnx_sha256": sha(PRIMARY_MT5_ONNX) if exists(PRIMARY_MT5_ONNX) else "",
        "fallback_mt5_onnx": rel(FALLBACK_MT5_ONNX),
        "fallback_mt5_onnx_sha256": sha(FALLBACK_MT5_ONNX) if exists(FALLBACK_MT5_ONNX) else "",
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "report_name": package["report_name"],
        "primary_threshold": package["primary_threshold"],
        "primary_margin_vs_flat": package["primary_margin_vs_flat"],
        "fallback_threshold": package["fallback_threshold"],
        "fallback_margin_vs_flat": package["fallback_margin_vs_flat"],
        "expected_oos_net": package["expected_oos_net"],
        "expected_oos_profit_factor": package["expected_oos_profit_factor"],
        "expected_oos_trade_density": package["expected_oos_trade_density"],
        "expected_oos_trade_count": package["expected_oos_trade_count"],
        "expected_oos_long_trade_count": package["expected_oos_long_trade_count"],
        "expected_oos_short_trade_count": package["expected_oos_short_trade_count"],
        "runtime_representation": "partial_route_probability_bin_veto_supported(부분 라우트, 확률 구간 거부 지원)",
        "compile_log_zero_errors": bool(compile_payload.get("compile_log_zero_errors")),
        "portable_ea_copied": bool(compile_payload.get("portable_copied")),
        "runtime_module_hashes": mt5_runtime_module_hashes(),
        "new_model_training": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], package: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(WORK_PACKET_RECEIPT, {**base, "work_packet": rel(WORK_PACKET), "primary_family": "runtime_backtest(런타임 백테스트)", "status": "completed"})
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(hf.SELECTED_CANDIDATE),
            "runtime_path": rel(package["set_path"]),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": [
                "HF score_plus_0p02 switch(HF 점수 0.02 전환) is only partially represented(부분 표현)",
                "MT5 tester output(MT5 테스터 출력)은 아직 없습니다.",
                "Expected OOS density(예상 표본외 밀도)는 3/day(일 3회) 목표보다 낮습니다.",
            ],
            "parity_check": rel(RUNTIME_REPRESENTATION_AUDIT),
            "parity_identity": rel(RUNTIME_PACKAGE_MANIFEST),
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(BACKTEST_RECEIPT, {**base, "tester_ini": rel(package["ini_path"]), "tester_set": rel(package["set_path"]), "tester_output_status": "not_run", "next_probe": NEXT_RUN_ID, "forensics_status": "identity_prepared_output_absent(정체성 준비, 출력 없음)"})
    write_json(ENV_RECEIPT, {**base, "metaeditor": DEFAULT_METAEDITOR.as_posix(), "terminal": basepkg.DEFAULT_TERMINAL.as_posix(), "common_files": basepkg.DEFAULT_COMMON_FILES.as_posix(), "compile_result": rel(COMPILE_RESULT), "environment_judgment": "usable_for_next_mt5_probe(다음 MT5 탐침에 사용 가능)"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(Path(path)).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)", "lineage_judgment": "connected_with_boundary(경계 포함 연결)"})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(FEATURE_MATRIX_AUDIT), rel(COMPILE_RESULT), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)], "evidence_missing": ["MT5 tester output(MT5 테스터 출력)", "forward/replay evidence(전진/재생 근거)", "runtime authority closure(런타임 권위 종료)", "3/day operating density(일 3회 운영 밀도)"], "judgment_label": final["judgment"], "next_condition": final["next_run_id"], "user_explanation_hook": "Package is ready for MT5 probe, not runtime authority(패키지는 MT5 탐침 준비이지 런타임 권위가 아님)."})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "MT5 runtime probe package prepared and compile checked(MT5 런타임 탐침 패키지 준비 및 컴파일 확인)", "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364HJ Probability-Bin Veto Runtime Package(확률 구간 거부 런타임 패키지)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- primary model(우선 모델): `{PRIMARY_MODEL_ID}`
- fallback model(대체 모델): `{FALLBACK_MODEL_ID}`
- feature contract(피처 계약): primary 60 + fallback 56(우선 60 + 대체 56)
- probability-bin veto(확률 구간 거부): `17|4|6;21|5|7`
- set/ini(설정/초기화): `{final['set_path']}` / `{final['ini_path']}`
- compile zero errors(컴파일 오류 0): `{final['compile_log_zero_errors']}`
- portable EA copied(휴대용 전문가 자문 복사): `{final['portable_ea_copied']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

## Action/Effect(행동/효과)

Action(행동): HI에서 구현한 probability-bin veto runtime support(확률 구간 거부 런타임 지원)를 GZ primary + HB fallback(GZ 우선 + HB 대체) ONNX(온엑스) 패키지, feature CSV(피처 CSV), MT5 set/ini(MT5 설정/초기화 파일), Common Files(공용 파일) handoff(인계)로 물질화했습니다.

Effect(효과): HK에서 MT5 Strategy Tester(MT5 전략 테스터)를 바로 실행하고 proxy vs MT5(프록시 대 MT5) 차이를 비교할 수 있습니다.

## Expected Proxy(예상 프록시)

- OOS net/PF/density/trades(표본외 순수익/수익 팩터/밀도/거래수): `{final['expected_oos_net']}` / `{final['expected_oos_profit_factor']}` / `{final['expected_oos_trade_density']}` / `{final['expected_oos_trade_count']}`
- OOS long/short(표본외 롱/숏): `{final['expected_oos_long_trade_count']}` / `{final['expected_oos_short_trade_count']}`

## Runtime Boundary(런타임 경계)

- probability-bin veto(확률 구간 거부)는 represented(표현됨)입니다.
- dual-source route(이중 원천 라우트)는 partial_represented(부분 표현)입니다. HF Python router(HF 파이썬 라우터)의 score_plus_0p02(점수 0.02 추가) switch(전환)를 EA(전문가 자문)가 완전히 재현하지 않습니다.
- expected OOS density(예상 표본외 밀도)는 3/day(일 3회) 목표보다 낮습니다. 이 실행은 runtime capability probe package(런타임 기능 탐침 패키지)이지 operating candidate(운영 후보)가 아닙니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364HJ decision(결정): probability-bin veto runtime package(확률 구간 거부 런타임 패키지)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- set_path(설정 경로): `{final['set_path']}`
- ini_path(초기화 경로): `{final['ini_path']}`
- next action(다음 행동): `{final['next_run_id']}`
- effect(효과): MT5 Strategy Tester(MT5 전략 테스터) 실행 준비를 완료합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364HJ__{RUN_ID}", f"\n- run364HJ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - probability-bin veto runtime package(확률 구간 거부 런타임 패키지), next `{final['next_run_id']}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HJ__{RUN_ID}", f"\n<!-- run364HJ__{RUN_ID} -->\n\n## run364HJ Probability-Bin Veto Runtime Package(확률 구간 거부 런타임 패키지)\n\nAction(행동): GZ primary + HB fallback(GZ 우선 + HB 대체) ONNX(온엑스), feature CSV(피처 CSV), probability-bin veto(확률 구간 거부) set/ini(설정/초기화 파일)를 물질화했습니다.\n\nEffect(효과): `{final['next_run_id']}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다. 운영 권위는 없습니다.\n")
    append_text_once(STAGE_README, f"run364HJ__{RUN_ID}", f"\n<!-- run364HJ__{RUN_ID} -->\n## run364HJ runtime package(런타임 패키지)\n\nCandidate(후보): `{PRIMARY_MODEL_ID}` + `{FALLBACK_MODEL_ID}`. Next(다음): `{final['next_run_id']}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{final['next_run_id']}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{final['status']}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {final['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {final['next_run_id']}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{final['next_run_id']}`

Current truth(현재 진실): `run364HJ` materialized(물질화 완료) probability-bin veto runtime package(확률 구간 거부 런타임 패키지). Primary/fallback(우선/대체) feature contract(피처 계약)은 `60/56`이고 set/ini(설정/초기화 파일)는 `{final['set_path']}` / `{final['ini_path']}`입니다. MetaEditor compile(메타에디터 컴파일)은 `compile_zero_errors={final['compile_log_zero_errors']}`입니다.

Runtime truth(런타임 진실): Strategy Tester(전략 테스터)와 runtime telemetry comparison(런타임 기록 비교)은 아직 없습니다.

Important boundary(중요 경계): HF score_plus_0p02 router(HF 점수 0.02 라우터)는 EA fallback-after-flat(EA flat 이후 대체)로만 부분 표현됩니다. Expected OOS trade density(예상 표본외 거래 밀도) `{final['expected_oos_trade_density']}`는 3/day(일 3회) 목표보다 낮습니다.

Next action(다음 행동): `{final['next_run_id']}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy vs MT5(프록시 대 MT5) diff(차이)를 기록합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{final['next_run_id']}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest runtime package(최근 런타임 패키지): `{RUN_ID}`.

Runtime package(런타임 패키지): probability-bin veto(확률 구간 거부) supported(지원), dual-source route(이중 원천 라우트) partial(부분).

Expected OOS net/PF/density/trades(예상 표본외 순수익/수익 팩터/밀도/거래수): `{final['expected_oos_net']}` / `{final['expected_oos_profit_factor']}` / `{final['expected_oos_trade_density']}` / `{final['expected_oos_trade_count']}`.

Goal density note(목표 밀도 메모): current package(현재 패키지)는 3/day(일 3회) 미만이라 operating candidate(운영 후보)가 아닙니다.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364HJ__{RUN_ID}", f"\n<!-- run364HJ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed probability-bin veto runtime package(확률 구간 거부 런타임 패키지); next `{final['next_run_id']}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HJ__{RUN_ID}", f"\n<!-- run364HJ__{RUN_ID} -->\n- `{RUN_ID}`: probability-bin veto(확률 구간 거부)를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 물질화했습니다. Effect(효과): proxy clue(프록시 단서)를 MT5 KPI(MT5 핵심 성과 지표)로 검증할 수 있습니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364HJ__density_boundary__{RUN_ID}", f"\n<!-- run364HJ__density_boundary__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님). Package only(패키지 전용)이며 expected OOS density(예상 표본외 밀도) `{final['expected_oos_trade_density']}`는 3/day(일 3회) 목표보다 낮아 운영 후보로 주장하지 않습니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": final["next_run_id"],
        "rows": 1,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "work_family": "runtime_backtest(런타임 백테스트)",
        "scoreboard_lane": "runtime_package(런타임 패키지)",
        "external_verification_status": "not_run_package_only(미실행, 패키지 전용)",
        "evidence_boundary": "compile_checked_package_only(컴파일 확인 패키지 전용)",
        "question": "Can the HF probability-bin veto route be packaged for MT5 runtime probe?(HF 확률 구간 거부 라우트를 MT5 런타임 탐침으로 패키지화할 수 있는가?)",
        "next_action": final["next_run_id"],
        "net_profit": final["expected_oos_net"],
        "profit_factor": final["expected_oos_profit_factor"],
        "trade_density_per_feature_day": final["expected_oos_trade_density"],
        "trade_count": final["expected_oos_trade_count"],
        "long_trade_count": final["expected_oos_long_trade_count"],
        "short_trade_count": final["expected_oos_short_trade_count"],
        "result_judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    rows = []
    for suffix, record_view, tier_scope, status, include in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", final["status"], True),
        ("tier_b_fallback_used", "Tier B fallback used(Tier B 대체 사용)", "Tier B", final["status"], True),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", final["status"], True),
    ]:
        rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "view": record_view,
                "tier": tier_scope,
                "kpi_scope": "runtime_package(런타임 패키지)",
                "metric_scope": "package_expected_proxy(패키지 예상 프록시)",
                "status": status,
                "rows": 1 if include else 0,
                "net_profit": final["expected_oos_net"] if suffix == "actual_routed_total" else "",
                "profit_factor": final["expected_oos_profit_factor"] if suffix == "actual_routed_total" else "",
                "trade_count": final["expected_oos_trade_count"] if suffix == "actual_routed_total" else "",
                "long_trade_count": final["expected_oos_long_trade_count"] if suffix == "actual_routed_total" else "",
                "short_trade_count": final["expected_oos_short_trade_count"] if suffix == "actual_routed_total" else "",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    artifact_rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "HJ probability-bin veto runtime package artifact(HJ 확률 구간 거부 런타임 패키지 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": final["next_run_id"],
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    validate_inputs()
    selected = load_selected()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "runtime_backtest(런타임 백테스트)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-environment-reproducibility(환경 재현성)",
            ],
            "required_gates": [
                "input_lineage_gate",
                "feature_matrix_gate",
                "onnx_handoff_gate",
                "probability_bin_veto_parameter_gate",
                "runtime_representation_gate",
                "compile_gate",
                "runtime_handoff_package_gate",
                "common_files_sync_gate",
                "proxy_mt5_comparison_contract_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    feature_payload = materialize_feature_matrices()
    materialize_onnx_pair()
    sync_rows = common_sync_rows()
    package = materialize_set_and_ini(selected, feature_payload)
    write_contracts(selected, feature_payload, package, sync_rows)
    compile_payload = compile_and_sync_ea()
    receipt_paths = [WORK_PACKET_RECEIPT, RUNTIME_RECEIPT, BACKTEST_RECEIPT, ENV_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(package, compile_payload, receipt_paths, final_written=False)
    created_at = now_utc()
    final = final_payload(feature_payload, package, compile_payload, gates, created_at)
    write_receipts(final, package)
    gates = gate_rows(package, compile_payload, receipt_paths, final_written=True)
    final = final_payload(feature_payload, package, compile_payload, gates, created_at)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final, gates)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
