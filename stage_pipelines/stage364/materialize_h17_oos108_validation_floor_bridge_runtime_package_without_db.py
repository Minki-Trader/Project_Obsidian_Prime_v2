from __future__ import annotations

import csv
import json
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

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, export_mt5_feature_matrix_csv, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as basepkg  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_validation_floor_bridge_without_db as em  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_validation_floor_bridge_without_db as el  # noqa: E402
from stage_pipelines.stage364 import train_h17_validation_stability_regime_source_reseed_without_db as dv  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = el.STAGE_ID
RUN_NUMBER = "run364EN"
RUN_ID = "run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1"
PARENT_RUN_ID = em.RUN_ID
SOURCE_PROXY_RUN_ID = el.RUN_ID
NEXT_RUN_ID = "run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364EN_h17_oos108_validation_floor_bridge_runtime_package_prepared_compile_checked_no_execution"
JUDGMENT = "runtime_probe_package_ready_oos108_validation_floor_bridge_mt5_execution_required_no_authority"
DECISION = "stage364EN_open_run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_oos108_validation_floor_bridge_compile_checked_"
    "csv_feature_handoff_82_features_no_mt5_execution_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MODEL_ID = "oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160"
FEATURE_SET_ID = "source_all82"
LABEL_ID = "oos108_valfloor_dir_h2_m1"
PRIMARY_ATTEMPT = "run364EN_oos108_validation_floor_bridge"
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin_h21_block_gap_guard"
DEFAULT_METAEDITOR = basepkg.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"

STAGE_DIR = el.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_MATRIX = RUN_DIR / "oos108_validation_floor_bridge_feature_matrix.csv"
FEATURE_ORDER = RUN_DIR / "feature_order.json"
FEATURE_MATRIX_AUDIT = RUN_DIR / "feature_matrix_audit.csv"
MT5_ONNX_DIR = RUN_DIR / "onnx_mt5"
MT5_ONNX = MT5_ONNX_DIR / f"{MODEL_ID}_mt5_probability_tensor.onnx"
MT5_ONNX_AUDIT = RUN_DIR / "mt5_onnx_contract_audit.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = MT5_DIR / "compile" / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
RUN364EO_EXECUTION_QUEUE = RUN_DIR / "run364EO_execution_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364EN_h17_oos108_validation_floor_bridge_runtime_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EN_h17_oos108_validation_floor_bridge_runtime_package.md"
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

SOURCE_ONNX = el.ONNX_DIR / f"{MODEL_ID}.onnx"
SOURCE_JOBLIB = el.RUN_DIR / "models" / f"{MODEL_ID}.joblib"
SOURCE_EA = basepkg.EA_SOURCE
SOURCE_EA_BINARY = basepkg.EA_BINARY
PORTABLE_EA_EX5 = basepkg.PORTABLE_EA_EX5

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_oos108_validation_floor_bridge_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    em.FINAL_DECISION,
    em.GATE_AUDIT,
    em.PACKAGE_DECISION,
    em.RUN364EN_QUEUE,
    em.COST_STRESS_REVIEW,
    em.MONTH_STABILITY_REVIEW,
    em.SIDE_BALANCE_REVIEW,
    el.FINAL_DECISION,
    el.GATE_AUDIT,
    el.SELECTED_CANDIDATE,
    el.SELECTED_TRADE_TAPE,
    el.COST_STRESS,
    el.MONTH_STABILITY,
    el.MODEL_ARTIFACT_MANIFEST,
    el.ONNX_SMOKE_REPORT,
    el.DATA_INTEGRITY_AUDIT,
    SOURCE_ONNX,
    SOURCE_JOBLIB,
    SOURCE_EA,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    FEATURE_MATRIX,
    FEATURE_ORDER,
    FEATURE_MATRIX_AUDIT,
    MT5_ONNX,
    MT5_ONNX_AUDIT,
    RUNTIME_POLICY_CONFIG,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    RUN364EO_EXECUTION_QUEUE,
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


def rel(path: Path | str) -> str:
    return el.rel(path)


def exists(path: Path | str) -> bool:
    return el.exists(path)


def sha(path: Path | str) -> str:
    return el.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return el.as_float(value, default)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    el.write_text(path, text, bom=bom)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    el.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    el.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    el.replace_prefixed_lines(path, replacements, bom=bom)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_ONNX_DIR, MT5_DIR / "compile", SET_DIR, INI_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EN inputs(EN 입력 누락): " + ", ".join(missing))
    em_final = read_json(em.FINAL_DECISION)
    el_final = read_json(el.FINAL_DECISION)
    selected = read_json(el.SELECTED_CANDIDATE)
    if em_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EM next_run_id mismatch(EM 다음 실행 ID 불일치): {em_final.get('next_run_id')} != {RUN_ID}")
    if el_final.get("selected_model_id") != MODEL_ID or selected.get("selected_model_id") != MODEL_ID:
        raise RuntimeError("EL selected model mismatch(EL 선택 모델 불일치)")
    if selected.get("selected_feature_set_id") != FEATURE_SET_ID:
        raise RuntimeError("EL selected feature set mismatch(EL 선택 피처 묶음 불일치)")
    for label, final in [("EM", em_final), ("EL", el_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    for label, gate_path in [("EM", em.GATE_AUDIT), ("EL", el.GATE_AUDIT)]:
        gates = read_csv(gate_path)
        if gates.empty or any(gates["status"].astype(str) != "passed"):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return selected


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EN runtime package source(EN 런타임 패키지 원천)",
            "effect": "input lineage(입력 계보)를 고정해 package(패키지) 재현성을 만듭니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet(selected: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
            "primary_family": "runtime_backtest(런타임 백테스트)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-environment-reproducibility(환경 재현성)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "input_lineage_gate",
                "feature_matrix_gate",
                "onnx_handoff_gate",
                "runtime_representation_gate",
                "compile_gate",
                "runtime_handoff_package_gate",
                "common_files_sync_gate",
                "proxy_mt5_comparison_contract_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "hypothesis": "EL OOS108 validation floor bridge(EL 표본외108 검증 바닥 연결) 후보를 82 feature CSV handoff(82 피처 CSV 인계)로 MT5 probe(MT5 탐침)에 올릴 수 있다.",
            "decision_use": "Prepare MT5 runtime probe package(MT5 런타임 탐침 패키지 준비) only, not authority(권위 아님).",
            "selected_model_id": selected["selected_model_id"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def materialize_feature_matrix(selected: Mapping[str, Any]) -> dict[str, Any]:
    frame, base_feature_order = dv.load_frame()
    feature_sets = el.el_feature_sets(base_feature_order)
    feature_order = list(feature_sets[FEATURE_SET_ID])
    missing = [column for column in feature_order if column not in frame.columns]
    if missing:
        raise RuntimeError("feature columns missing(피처 열 누락): " + ", ".join(missing[:20]))
    if len(feature_order) != 82:
        raise RuntimeError(f"feature count mismatch(피처 수 불일치): {len(feature_order)} != 82")
    probe_frame = frame[frame["split"].astype(str).isin(["validation", "oos"])].copy()
    if probe_frame.empty:
        raise RuntimeError("validation/oos rows missing(검증/표본외 행 누락)")
    export = export_mt5_feature_matrix_csv(
        probe_frame,
        feature_order,
        FEATURE_MATRIX,
        timestamp_column="timestamp",
        metadata_columns=["entry_open", "open", "high", "low", "close", "volume"],
    )
    payload = {
        "run_id": RUN_ID,
        "model_id": selected["selected_model_id"],
        "feature_set_id": FEATURE_SET_ID,
        "feature_count": len(feature_order),
        "feature_columns": feature_order,
        "feature_order_hash": ordered_hash(feature_order),
        "feature_matrix": rel(FEATURE_MATRIX),
        "feature_matrix_sha256": sha(FEATURE_MATRIX),
        "export": export,
        "split_scope": "validation+oos(검증+표본외)",
        "timestamp_semantics": "bar_time_server exported from timestamp(타임스탬프에서 서버 봉 시간 출력)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_ORDER, payload)
    write_csv(
        FEATURE_MATRIX_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "model_id": MODEL_ID,
                "feature_set_id": FEATURE_SET_ID,
                "feature_count": len(feature_order),
                "feature_order_hash": payload["feature_order_hash"],
                "rows": export["rows"],
                "split_scope": "validation+oos(검증+표본외)",
                "matrix_path": rel(FEATURE_MATRIX),
                "matrix_sha256": sha(FEATURE_MATRIX),
                "effect": "feature matrix(피처 행렬)를 MT5 CSV handoff(MT5 CSV 인계)에 맞게 고정했습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
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
    return [
        copy_common(FEATURE_MATRIX, f"{COMMON_FEATURE_DIR}/oos108_validation_floor_bridge_features.csv", "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(MT5_ONNX, f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx", "common_primary_onnx", "MT5-compatible ONNX model(MT5 호환 온엑스 모델)을 Common Files(공용 파일)에 복사합니다."),
        copy_common(FEATURE_ORDER, f"{COMMON_CONFIG_DIR}/feature_order.json", "common_feature_order", "feature order(피처 순서)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(el.SELECTED_TRADE_TAPE, f"{COMMON_EXPECTED_DIR}/selected_el_trade_tape.csv", "common_expected_proxy_trade_tape", "expected proxy tape(예상 프록시 테이프)를 비교 입력으로 복사합니다."),
        copy_common(el.COST_STRESS, f"{COMMON_EXPECTED_DIR}/selected_el_cost_stress.csv", "common_expected_cost_stress", "cost stress(비용 압박) 비교 입력을 복사합니다."),
        copy_common(el.MONTH_STABILITY, f"{COMMON_EXPECTED_DIR}/selected_el_month_stability.csv", "common_expected_month_stability", "month stability(月 안정성) 비교 입력을 복사합니다."),
    ]


def materialize_mt5_compatible_onnx() -> dict[str, Any]:
    import onnx
    from onnx import TensorProto, helper

    model = onnx.load_model_from_string(io_path(SOURCE_ONNX).read_bytes())
    outputs_before = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
        }
        for output in model.graph.output
    ]
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
    io_path(MT5_ONNX.parent).mkdir(parents=True, exist_ok=True)
    io_path(MT5_ONNX).write_bytes(model.SerializeToString())
    outputs_after = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
        }
        for output in model.graph.output
    ]
    payload = {
        "run_id": RUN_ID,
        "source_onnx": rel(SOURCE_ONNX),
        "mt5_onnx": rel(MT5_ONNX),
        "source_sha256": sha(SOURCE_ONNX),
        "mt5_onnx_sha256": sha(MT5_ONNX),
        "zipmap_removed": bool(zipmap_nodes),
        "probability_tensor_name": probability_tensor_name,
        "outputs_before": json.dumps(outputs_before, ensure_ascii=False),
        "outputs_after": json.dumps(outputs_after, ensure_ascii=False),
        "effect": "ZipMap(집맵)을 제거해 MT5가 probability tensor(확률 텐서)를 직접 받게 합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(MT5_ONNX_AUDIT, [payload])
    return payload


def compile_log_ok() -> bool:
    if not exists(COMPILE_LOG):
        return False
    raw = io_path(COMPILE_LOG).read_bytes()
    candidates: list[str] = []
    for encoding in ["utf-8-sig", "utf-16", "utf-16-le"]:
        candidates.append(raw.decode(encoding, errors="replace"))
    return any("Result: 0 errors" in text.replace("\x00", "") for text in candidates)


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
        os.makedirs(str(io_path(PORTABLE_EA_EX5.parent)), exist_ok=True)
        shutil.copy2(io_path(SOURCE_EA_BINARY), io_path(PORTABLE_EA_EX5))
        payload.update({"portable_copied": True, "source_sha256": sha(SOURCE_EA_BINARY), "portable_sha256": sha(PORTABLE_EA_EX5)})
    write_json(COMPILE_RESULT, payload)
    write_json(PORTABLE_EA_SYNC, payload)
    return payload


def materialize_set_and_ini(selected: Mapping[str, Any], feature_payload: Mapping[str, Any]) -> dict[str, Any]:
    common_feature = f"{COMMON_FEATURE_DIR}/oos108_validation_floor_bridge_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_telemetry = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv"
    common_summary = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv"
    threshold = as_float(selected["selected_threshold"])
    margin_vs_flat = as_float(selected["selected_margin_vs_flat"])
    set_values = {
        "InpRunId": f"{RUN_ID}_{PRIMARY_ATTEMPT}",
        "InpExplorationLabel": "stage364EN__OOS108ValidationFloorBridge",
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_oos108_validation_floor_bridge",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": common_feature,
        "InpFeatureCount": int(feature_payload["feature_count"]),
        "InpFeatureCsvUseCommonFiles": True,
        "InpFeatureRequireTimestampMatch": True,
        "InpFeatureAllowLatestFallback": False,
        "InpFeatureStrictHeader": True,
        "InpFeatureCsvDelimiter": ",",
        "InpCsvTimestampIsBarClose": False,
        "InpModelPath": common_model,
        "InpModelId": MODEL_ID,
        "InpModelBackend": "onnx",
        "InpModelUseCommonFiles": True,
        "InpModelUseCpuOnly": True,
        "InpModelNoConversion": False,
        "InpSetOutputShape": True,
        "InpModelUseMatrixTensor": False,
        "InpFeatureOrderHash": feature_payload["feature_order_hash"],
        "InpFallbackEnabled": False,
        "InpShortThreshold": threshold,
        "InpLongThreshold": threshold,
        "InpMinMargin": margin_vs_flat,
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpCalendarBlockEnabled": True,
        "InpCalendarBlockSide": "both",
        "InpCalendarBlockMonth": 0,
        "InpCalendarBlockStartHour": 21,
        "InpCalendarBlockEndHour": 22,
        "InpTimeMarginGuardEnabled": True,
        "InpTimeMarginGuardSide": "both",
        "InpTimeMarginGuardStartHour": 0,
        "InpTimeMarginGuardEndHour": 24,
        "InpTimeMarginGuardBasis": "opposite",
        "InpTimeMarginGuardMinMargin": 0.004,
        "InpEntryMarginFloor": 0.0,
        "InpSyntheticShortSourceEnabled": False,
        "InpSyntheticShortMonthBlockEnabled": False,
        "InpRiskScaleOverlayEnabled": False,
        "InpAllowTrading": True,
        "InpFixedLot": 0.1,
        "InpModelRiskFallbackLot": 0.1,
        "InpModelRiskSizingEnabled": False,
        "InpMagic": 36450001,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": 2,
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpTelemetryEnabled": True,
        "InpTelemetryUseCommonFiles": True,
        "InpTelemetryCsvPath": common_telemetry,
        "InpSummaryCsvPath": common_summary,
    }
    set_path = SET_DIR / "OPv2_run364EN_oos108_validation_floor_bridge.set"
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    report_name = "Project_Obsidian_Prime_v2_run364EO_oos108_validation_floor_bridge_probe"
    ini_path = INI_DIR / "OPv2_run364EN_oos108_validation_floor_bridge.ini"
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
    package = {
        "set_path": set_path,
        "ini_path": ini_path,
        "set_sha256": set_payload["sha256"],
        "ini_sha256": ini_payload["sha256"],
        "parameter_count": set_payload["parameter_count"],
        "report_name": report_name,
        "threshold": threshold,
        "margin_vs_flat": margin_vs_flat,
    }
    write_csv(
        TESTER_SET_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "model_id": MODEL_ID,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "feature_count": feature_payload["feature_count"],
                "threshold": threshold,
                "margin_vs_flat": margin_vs_flat,
                "h21_block": "enabled_both_21_22(양방향 21시-22시 차단)",
                "direction_gap_guard": "time_margin_guard_opposite_min_0p004(반대 방향 마진 최소 0.004)",
                "max_hold_bars": 2,
                "output_contract": OUTPUT_CONTRACT,
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
    return package


def write_contracts(selected: Mapping[str, Any], feature_payload: Mapping[str, Any], package: Mapping[str, Any], sync_rows: Sequence[Mapping[str, Any]]) -> None:
    runtime_policy = {
        "run_id": RUN_ID,
        "model_id": MODEL_ID,
        "feature_contract": "csv_feature_handoff_82_features(CSV 피처 인계 82개)",
        "threshold": package["threshold"],
        "margin_vs_flat": package["margin_vs_flat"],
        "h21_block": True,
        "direction_gap_guard": "InpTimeMarginGuardBasis=opposite;min=0.004",
        "max_hold_bars": 2,
        "known_differences": [
            "CSV feature handoff uses 82 features, not default 58 live contract(CSV 피처 인계는 기본 58개 실거래 계약이 아니라 82개입니다).",
            "MT5 fill/spread/position timing may differ from Python open-to-open proxy(MT5 체결/스프레드/포지션 시점은 Python 시가-시가 프록시와 다를 수 있습니다).",
            "MT5 probe output is absent until EO execution(EO 실행 전에는 MT5 탐침 출력이 없습니다).",
        ],
        "effect": "runtime policy(런타임 정책)를 set/ini(설정/초기화)에 같은 의미로 연결합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, runtime_policy)
    write_csv(
        MODEL_HANDOFF_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "model_id": MODEL_ID,
                "source_onnx": rel(SOURCE_ONNX),
                "source_onnx_sha256": sha(SOURCE_ONNX),
                "mt5_compatible_onnx": rel(MT5_ONNX),
                "mt5_compatible_onnx_sha256": sha(MT5_ONNX),
                "source_joblib": rel(SOURCE_JOBLIB),
                "source_joblib_sha256": sha(SOURCE_JOBLIB),
                "feature_order": rel(FEATURE_ORDER),
                "feature_order_hash": feature_payload["feature_order_hash"],
                "feature_matrix": rel(FEATURE_MATRIX),
                "feature_matrix_sha256": sha(FEATURE_MATRIX),
                "output_contract": OUTPUT_CONTRACT,
                "effect": "model handoff(모델 인계)의 파일과 hash(해시)를 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(COMMON_FILES_SYNC, sync_rows)
    write_csv(
        TESTER_IDENTITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "symbol": "US100",
                "timeframe": "M5",
                "broker": "FPMarkets",
                "tester_model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "set_path": rel(package["set_path"]),
                "ini_path": rel(package["ini_path"]),
                "report_name": package["report_name"],
                "effect": "tester identity(테스터 정체성)를 EO 실행 전 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        PROXY_MT5_COMPARISON_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "proxy_run_id": SOURCE_PROXY_RUN_ID,
                "mt5_probe_run_id": NEXT_RUN_ID,
                "expected_proxy_oos_net": selected["selected_oos_net"],
                "expected_proxy_oos_profit_factor": selected["selected_oos_profit_factor"],
                "expected_proxy_oos_trade_count": selected["selected_oos_trade_count"],
                "expected_proxy_oos_long_count": selected["selected_oos_long_trade_count"],
                "expected_proxy_oos_short_count": selected["selected_oos_short_trade_count"],
                "comparison_required": True,
                "effect": "proxy(프록시)를 MT5 KPI(MT5 핵심 성과 지표)와 비교할 의무를 남깁니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "research_signal": "threshold_margin_h21_block_direction_gap_guard",
                "runtime_signal": "InpShortThreshold/InpLongThreshold/InpMinMargin + calendar/time margin guards",
                "parity_status": "package_prepared_mt5_execution_required(패키지 준비, MT5 실행 필요)",
                "known_difference": "; ".join(runtime_policy["known_differences"]),
                "effect": "runtime parity(런타임 동등성)의 확인 범위와 미확인 범위를 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_REPRESENTATION_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "rule": "threshold_margin(임계값+마진)",
                "python_source": "score>=selected_threshold and score-p_flat>=selected_margin_vs_flat",
                "mt5_representation": "InpShortThreshold/InpLongThreshold/InpMinMargin",
                "status": "represented(표현됨)",
                "effect": "주 신호 조건을 MT5 decision surface(MT5 결정면)에 연결합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "rule": "no_h21_all_hours(21시 제외 전체 시간)",
                "python_source": "selected_hours_id=no_h21_all_hours",
                "mt5_representation": "InpCalendarBlockEnabled=True;side=both;hour=21-22",
                "status": "represented(표현됨)",
                "effect": "21시 거래를 runtime(런타임)에서 차단합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "rule": "direction_gap_floor(방향 간극 바닥)",
                "python_source": "abs(p_short-p_long)>=0.004 after no_h21 filter",
                "mt5_representation": "InpTimeMarginGuardBasis=opposite;side=both;min=0.004",
                "status": "represented_for_signal_side(신호 방향 기준 표현됨)",
                "effect": "long/short probability gap(롱/숏 확률 간극)을 runtime guard(런타임 조건)로 둡니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    write_csv(
        EXPECTED_KPI_SUMMARY,
        [
            {
                "run_id": RUN_ID,
                "model_id": MODEL_ID,
                "validation_net": selected["selected_validation_net"],
                "validation_profit_factor": selected["selected_validation_profit_factor"],
                "validation_trade_density": selected["selected_validation_trade_density"],
                "oos_net": selected["selected_oos_net"],
                "oos_profit_factor": selected["selected_oos_profit_factor"],
                "oos_trade_density": selected["selected_oos_trade_density"],
                "oos_trade_count": selected["selected_oos_trade_count"],
                "oos_long_trade_count": selected["selected_oos_long_trade_count"],
                "oos_short_trade_count": selected["selected_oos_short_trade_count"],
                "source": rel(el.SELECTED_CANDIDATE),
                "effect": "MT5 probe(MT5 탐침) 후 비교할 proxy expected value(프록시 예상값)를 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "tester_ini": rel(package["ini_path"]),
                "tester_set": rel(package["set_path"]),
                "feature_common_path": f"{COMMON_FEATURE_DIR}/oos108_validation_floor_bridge_features.csv",
                "model_common_path": f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx",
                "suggested_command": f"\"{basepkg.DEFAULT_TERMINAL.as_posix()}\" /portable /config:\"{package['ini_path'].as_posix()}\"",
                "effect": "EO 실행 명령과 입력 파일을 한 줄로 묶습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364EO_EXECUTION_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "eo01_execute_oos108_validation_floor_bridge_mt5_runtime_probe",
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "tester_ini": rel(package["ini_path"]),
                "tester_set": rel(package["set_path"]),
                "comparison_contract": rel(PROXY_MT5_COMPARISON_CONTRACT),
                "effect": "다음 작업이 MT5 Strategy Tester(MT5 전략 테스터)를 실행하도록 대기열을 만듭니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(package: Mapping[str, Any], compile_payload: Mapping[str, Any], receipt_paths: Sequence[Path], final_written: bool) -> list[dict[str, Any]]:
    common_paths = read_csv(COMMON_FILES_SYNC) if exists(COMMON_FILES_SYNC) else pd.DataFrame()
    common_ok = (not common_paths.empty) and all(Path(path).exists() for path in common_paths.get("common_absolute_path", []))
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), INPUT_MANIFEST, "입력 계보가 연결됐습니다."),
        ("feature_matrix_gate", exists(FEATURE_MATRIX) and exists(FEATURE_ORDER) and exists(FEATURE_MATRIX_AUDIT), FEATURE_MATRIX_AUDIT, "82 feature matrix(82 피처 행렬)가 작성됐습니다."),
        ("onnx_handoff_gate", exists(MODEL_HANDOFF_MANIFEST) and exists(SOURCE_ONNX) and exists(MT5_ONNX) and exists(MT5_ONNX_AUDIT), MODEL_HANDOFF_MANIFEST, "MT5-compatible ONNX handoff(MT5 호환 온엑스 인계)가 기록됐습니다."),
        ("runtime_representation_gate", exists(RUNTIME_REPRESENTATION_AUDIT) and exists(RUNTIME_PARITY_CONTRACT), RUNTIME_REPRESENTATION_AUDIT, "runtime representation(런타임 표현)이 기록됐습니다."),
        ("compile_gate", bool(compile_payload.get("compile_log_zero_errors")) and bool(compile_payload.get("portable_copied")), COMPILE_RESULT, "MetaEditor compile(메타에디터 컴파일) 오류 0과 portable EA(포터블 EA) 복사를 확인했습니다."),
        ("runtime_handoff_package_gate", exists(package["set_path"]) and exists(package["ini_path"]) and exists(RUNTIME_PROBE_ATTEMPT_PACKAGE), RUNTIME_PROBE_ATTEMPT_PACKAGE, "set/ini/attempt package(설정/초기화/시도 패키지)가 작성됐습니다."),
        ("common_files_sync_gate", common_ok, COMMON_FILES_SYNC, "Common Files(공용 파일) 복사가 확인됐습니다."),
        ("proxy_mt5_comparison_contract_gate", exists(PROXY_MT5_COMPARISON_CONTRACT), PROXY_MT5_COMPARISON_CONTRACT, "proxy vs MT5 비교 계약(프록시와 MT5 비교 계약)이 작성됐습니다."),
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


def final_payload(selected: Mapping[str, Any], feature_payload: Mapping[str, Any], package: Mapping[str, Any], compile_payload: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    all_passed = all(row["status"] == "passed" for row in gates)
    status = STATUS if all_passed else "blocked_stage364EN_runtime_package_gate_failure_repair_required_no_authority"
    judgment = JUDGMENT if all_passed else "inconclusive_runtime_package_gate_failure_repair_required_no_authority"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID if all_passed else RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": DECISION if all_passed else "stage364EN_repair_runtime_package_gate_failure",
        "selected_model_id": MODEL_ID,
        "selected_feature_set_id": FEATURE_SET_ID,
        "selected_label_id": LABEL_ID,
        "feature_count": feature_payload["feature_count"],
        "feature_order_hash": feature_payload["feature_order_hash"],
        "feature_matrix_rows": feature_payload["export"]["rows"],
        "mt5_compatible_onnx": rel(MT5_ONNX),
        "mt5_compatible_onnx_sha256": sha(MT5_ONNX) if exists(MT5_ONNX) else "",
        "threshold": package["threshold"],
        "margin_vs_flat": package["margin_vs_flat"],
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "report_name": package["report_name"],
        "compile_log_zero_errors": bool(compile_payload.get("compile_log_zero_errors")),
        "portable_ea_copied": bool(compile_payload.get("portable_copied")),
        "expected_validation_profit_factor": selected["selected_validation_profit_factor"],
        "expected_oos_net": selected["selected_oos_net"],
        "expected_oos_profit_factor": selected["selected_oos_profit_factor"],
        "expected_oos_trade_density": selected["selected_oos_trade_density"],
        "expected_oos_trade_count": selected["selected_oos_trade_count"],
        "expected_oos_long_trade_count": selected["selected_oos_long_trade_count"],
        "expected_oos_short_trade_count": selected["selected_oos_short_trade_count"],
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
            "research_path": rel(el.SELECTED_CANDIDATE),
            "runtime_path": rel(package["set_path"]),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": [
                "82-feature CSV runtime probe handoff(82개 피처 CSV 런타임 탐침 인계)",
                "MT5 tester output not run yet(MT5 테스터 출력은 아직 미실행)",
                "Python proxy fill semantics differ from MT5(Python 프록시 체결 의미는 MT5와 다름)",
            ],
            "parity_check": rel(RUNTIME_REPRESENTATION_AUDIT),
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(BACKTEST_RECEIPT, {**base, "tester_ini": rel(package["ini_path"]), "tester_set": rel(package["set_path"]), "tester_output_status": "not_run", "next_probe": NEXT_RUN_ID, "forensics_status": "identity_prepared_output_absent(정체성 준비, 출력 없음)"})
    write_json(ENV_RECEIPT, {**base, "metaeditor": DEFAULT_METAEDITOR.as_posix(), "terminal": basepkg.DEFAULT_TERMINAL.as_posix(), "common_files": basepkg.DEFAULT_COMMON_FILES.as_posix(), "compile_result": rel(COMPILE_RESULT), "environment_judgment": "usable_for_next_mt5_probe(다음 MT5 탐침에 사용 가능)"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_for_runtime_probe(런타임 탐침용 연결)"})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(FEATURE_MATRIX_AUDIT), rel(COMPILE_RESULT), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)], "evidence_missing": ["MT5 tester output(MT5 테스터 출력)", "forward/replay evidence(전진/재생 근거)", "runtime authority closure(런타임 권위 종결)"], "judgment_label": final["judgment"], "next_condition": final["next_run_id"], "user_explanation_hook": "Package is ready for MT5 probe, not runtime authority(패키지는 MT5 탐침 준비 완료지만 런타임 권위는 아님)."})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "MT5 runtime probe package prepared and compile checked(MT5 런타임 탐침 패키지 준비 및 컴파일 확인)", "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364EN OOS108 Validation Floor Bridge Runtime Package(표본외108 검증 바닥 연결 런타임 패키지)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- model(모델): `{MODEL_ID}`
- feature contract(피처 계약): `82 feature CSV handoff(82개 피처 CSV 인계)`
- ONNX contract(온엑스 계약): `ZipMap removed probability tensor(집맵 제거 확률 텐서)`
- threshold/margin(임계값/마진): `{final['threshold']}` / `{final['margin_vs_flat']}`
- set/ini(설정/초기화): `{final['set_path']}` / `{final['ini_path']}`
- compile zero errors(컴파일 오류 0): `{final['compile_log_zero_errors']}`
- portable EA copied(포터블 EA 복사): `{final['portable_ea_copied']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

## Action/Effect(행동/효과)

Action(행동): EL 후보의 ONNX(온엑스)를 MT5-compatible probability tensor(MT5 호환 확률 텐서)로 고치고, 82개 feature matrix(피처 행렬), MT5 set/ini(MT5 설정/초기화)를 runtime probe package(런타임 탐침 패키지)로 물질화했습니다.

Effect(효과): EO에서 MT5 Strategy Tester(MT5 전략 테스터)를 바로 실행하고 proxy vs MT5(프록시와 MT5) 차이를 비교할 수 있습니다.

## Expected Proxy(예상 프록시)

- validation PF(검증 수익 팩터): `{final['expected_validation_profit_factor']}`
- OOS net/PF/density/trades(표본외 순수익/수익 팩터/밀도/거래수): `{final['expected_oos_net']}` / `{final['expected_oos_profit_factor']}` / `{final['expected_oos_trade_density']}` / `{final['expected_oos_trade_count']}`
- OOS long/short(표본외 롱/숏): `{final['expected_oos_long_trade_count']}` / `{final['expected_oos_short_trade_count']}`

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is package only(패키지 전용)입니다. MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364EN decision(결정): OOS108 validation floor bridge runtime package(표본외108 검증 바닥 연결 런타임 패키지)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- model(모델): `{MODEL_ID}`
- set_path(설정 경로): `{final['set_path']}`
- ini_path(초기화 경로): `{final['ini_path']}`
- next action(다음 행동): `{final['next_run_id']}`
- effect(효과): MT5 Strategy Tester(MT5 전략 테스터) 실행 준비를 완료합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364EN__{RUN_ID}", f"\n- run364EN__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - OOS108 runtime package(OOS108 런타임 패키지), next `{final['next_run_id']}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EN__{RUN_ID}", f"\n<!-- run364EN__{RUN_ID} -->\n\n## run364EN Runtime Package(런타임 패키지)\n\nAction(행동): OOS108 validation floor bridge(표본외108 검증 바닥 연결) set/ini(설정/초기화 파일), feature matrix(피처 행렬), ONNX(온엑스)를 물질화했습니다.\n\nEffect(효과): `{final['next_run_id']}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364EN__{RUN_ID}", f"\n<!-- run364EN__{RUN_ID} -->\n## run364EN runtime package(런타임 패키지)\n\nCandidate(후보): `{MODEL_ID}`. Next(다음): `{final['next_run_id']}`.\n")
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

Current truth(현재 진실): `run364EN` completed(완료) OOS108 validation floor bridge runtime package(표본외108 검증 바닥 연결 런타임 패키지). Selected model(선택 모델)은 `{MODEL_ID}`이고 feature contract(피처 계약)은 82 feature CSV handoff(82개 피처 CSV 인계)입니다. EA compile(EA 컴파일)는 `{final['compile_log_zero_errors']}`이고 set/ini(설정/초기화 파일)는 `{final['set_path']}` / `{final['ini_path']}`입니다.

Caution(주의): validation cost stress(검증 비용 압박)는 cost 0.6에서 약하고, side balance(방향 균형)는 short-heavy(숏 편향)입니다.

Next action(다음 행동): `{final['next_run_id']}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행해 실제 net/PF/DD/side balance(순수익/수익 팩터/낙폭/방향 균형)를 확인합니다.

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

Selected model(선택 모델): `{MODEL_ID}`

Feature contract(피처 계약): `82 feature CSV handoff(82개 피처 CSV 인계)`.

Expected OOS net/PF/trades(예상 표본외 순수익/수익 팩터/거래수): `{final['expected_oos_net']}` / `{final['expected_oos_profit_factor']}` / `{final['expected_oos_trade_count']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364EN__{RUN_ID}", f"\n<!-- run364EN__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed OOS108 runtime package(OOS108 런타임 패키지); next `{final['next_run_id']}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EN__{RUN_ID}", f"\n<!-- run364EN__{RUN_ID} -->\n- `{RUN_ID}`: EL OOS108 validation floor bridge(EL 표본외108 검증 바닥 연결)를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 물질화했습니다. Effect(효과): proxy clue(프록시 단서)를 MT5 KPI(MT5 핵심 성과 지표)로 검증할 수 있습니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EN__no_authority__{RUN_ID}", f"\n<!-- run364EN__no_authority__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님). Package only(패키지 전용); MT5 runtime output(MT5 런타임 출력) 전까지 operating claim(운영 주장) 금지.\n")


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
        "question": "Can the EL OOS108 bridge be packaged for MT5 runtime probe?(EL OOS108 연결 후보를 MT5 런타임 탐침용으로 패키지화할 수 있는가?)",
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
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"], True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_runtime_package(Tier B 런타임 패키지 없음)", False),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_package_tier_a_only(주장 범위 밖, Tier A 패키지 전용)", False),
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
                "metric_scope": "package_expected_proxy(Package 예상 프록시)",
                "status": status,
                "rows": 1 if include else 0,
                "net_profit": final["expected_oos_net"] if include else "",
                "profit_factor": final["expected_oos_profit_factor"] if include else "",
                "trade_count": final["expected_oos_trade_count"] if include else "",
                "long_trade_count": final["expected_oos_long_trade_count"] if include else "",
                "short_trade_count": final["expected_oos_short_trade_count"] if include else "",
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
                    "notes": "EN OOS108 runtime package artifact(EN OOS108 런타임 패키지 산출물)",
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
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    selected = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(selected)
    feature_payload = materialize_feature_matrix(selected)
    materialize_mt5_compatible_onnx()
    sync_rows = common_sync_rows()
    package = materialize_set_and_ini(selected, feature_payload)
    write_contracts(selected, feature_payload, package, sync_rows)
    compile_payload = compile_and_sync_ea()
    receipt_paths = [WORK_PACKET_RECEIPT, RUNTIME_RECEIPT, BACKTEST_RECEIPT, ENV_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(package, compile_payload, receipt_paths, final_written=False)
    created_at = now_utc()
    final = final_payload(selected, feature_payload, package, compile_payload, gates, created_at)
    write_receipts(final, package)
    gates = gate_rows(package, compile_payload, receipt_paths, final_written=True)
    final = final_payload(selected, feature_payload, package, compile_payload, gates, created_at)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final, gates)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
