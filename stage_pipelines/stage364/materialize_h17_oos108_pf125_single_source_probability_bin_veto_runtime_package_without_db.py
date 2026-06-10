from __future__ import annotations

import csv
import json
import math
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
from stage_pipelines.stage364 import implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db as hi  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db as hj  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db as hn  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_density_preserve_repair_without_db as fj  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-09"
STAGE_ID = hn.STAGE_ID
RUN_NUMBER = "run364HO"
RUN_ID = "run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1"
PARENT_RUN_ID = hn.RUN_ID
NEXT_RUN_ID = "run364HP_execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364HO_single_source_probability_bin_veto_runtime_package_materialized_mt5_probe_required_no_authority"
JUDGMENT = "runtime_package_materialized_single_source_probability_bin_veto_mt5_probe_required_no_authority"
DECISION = "stage364HO_open_run364HP_single_source_probability_bin_veto_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "runtime_probe_package_only_single_source_probability_bin_veto_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MODEL_ID = "fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160"
MODEL_FILE_STEM = "fj_sym_h2_m1p75_fj_behavior_density_cost_et8_l18_n160"
FEATURE_SET_ID = "fj_behavior_density_cost"
ATTEMPT_NAME = "run364HO_single_source_probability_bin_veto_runtime_probe"
DEFAULT_METAEDITOR = hj.basepkg.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"

STAGE_DIR = hn.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MT5_ONNX_DIR = RUN_DIR / "onnx_mt5"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_MATRIX = RUN_DIR / "single_fj_feature_matrix.csv"
FEATURE_ORDER_CONTRACT = RUN_DIR / "feature_order_contract.json"
FEATURE_MATRIX_AUDIT = RUN_DIR / "feature_matrix_audit.csv"
MT5_ONNX = MT5_ONNX_DIR / f"{MODEL_ID}_mt5_probability_tensor.onnx"
MT5_ONNX_AUDIT = RUN_DIR / "mt5_onnx_contract_audit.csv"
EXPECTED_TRADE_TAPE = RUN_DIR / "expected_single_source_trade_tape.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
VETO_APPLICABILITY_AUDIT = RUN_DIR / "probability_bin_veto_applicability_audit.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
RUNTIME_PACKAGE_MANIFEST = RUN_DIR / "runtime_package_manifest.json"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = MT5_DIR / "compile" / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUNTIME_REPRESENTATION_AUDIT = RUN_DIR / "runtime_representation_audit.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
RUN364HP_EXECUTION_QUEUE = RUN_DIR / "run364HP_execution_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364HO_single_source_probability_bin_veto_runtime_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HO_single_source_probability_bin_veto_runtime_package.md"
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

SOURCE_ONNX = STAGE_DIR / "02_runs" / "run364FJ" / "onnx" / f"{MODEL_FILE_STEM}.onnx"
SOURCE_JOBLIB = STAGE_DIR / "02_runs" / "run364FJ" / "models" / f"{MODEL_FILE_STEM}.joblib"
SOURCE_EA = hj.basepkg.EA_SOURCE
SOURCE_EA_BINARY = hj.basepkg.EA_BINARY
PORTABLE_EA_EX5 = hj.basepkg.PORTABLE_EA_EX5
MODEL_INPUT_DATASET = fj.et.dt.dp.MODEL_INPUT_DATASET
MODEL_INPUT_FEATURE_ORDER = fj.et.dt.dp.MODEL_INPUT_FEATURE_ORDER

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_single_source_probability_bin_veto_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    hn.FINAL_DECISION,
    hn.GATE_AUDIT,
    hn.FEATURE_ORDER_CONTRACT,
    hn.RUN364HO_QUEUE,
    hn.LINEAGE_RECEIPT,
    hn.CLAIM_RECEIPT,
    hi.FINAL_DECISION,
    hi.GATE_AUDIT,
    hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON,
    hi.MODULE_HASHES,
    fj.FINAL_DECISION,
    fj.SELECTED_CANDIDATE,
    fj.SELECTED_TRADE_TAPE,
    fj.COST_STRESS,
    fj.SIDE_SESSION_REVIEW,
    fj.MONTH_STABILITY,
    fj.MODEL_ARTIFACT_MANIFEST,
    fj.ONNX_SMOKE_REPORT,
    MODEL_INPUT_DATASET,
    MODEL_INPUT_FEATURE_ORDER,
    SOURCE_ONNX,
    SOURCE_JOBLIB,
    SOURCE_EA,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    FEATURE_MATRIX,
    FEATURE_ORDER_CONTRACT,
    FEATURE_MATRIX_AUDIT,
    MT5_ONNX,
    MT5_ONNX_AUDIT,
    EXPECTED_TRADE_TAPE,
    EXPECTED_KPI_SUMMARY,
    VETO_APPLICABILITY_AUDIT,
    RUNTIME_POLICY_CONFIG,
    RUNTIME_PACKAGE_MANIFEST,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    RUNTIME_REPRESENTATION_AUDIT,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    RUN364HP_EXECUTION_QUEUE,
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
    return hn.rel(path)


def exists(path: Path | str) -> bool:
    return hn.exists(path)


def sha(path: Path | str) -> str:
    return hn.sha(path)


def read_json(path: Path) -> Any:
    return hn.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    hn.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return hn.read_csv(path)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    hn.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    hn.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    hn.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    hn.append_or_replace_csv(path, key_fields, rows)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    hn.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def profit_factor(values: pd.Series) -> float | str:
    profits = values[values > 0].sum()
    losses = -values[values < 0].sum()
    if losses == 0:
        return "inf" if profits > 0 else ""
    return round(float(profits / losses), 10)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MT5_ONNX_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HO inputs(HO 입력 누락): " + ", ".join(missing[:30]))
    hn_final = read_json(hn.FINAL_DECISION)
    hi_final = read_json(hi.FINAL_DECISION)
    selected = read_json(fj.SELECTED_CANDIDATE)
    if hn_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HN next_run_id mismatch(HN 다음 실행 ID 불일치): {hn_final.get('next_run_id')} != {RUN_ID}")
    for gate_path, label in [(hn.GATE_AUDIT, "HN"), (hi.GATE_AUDIT, "HI")]:
        gates = read_csv(gate_path)
        if gates.empty or any(gates["status"].astype(str) != "passed"):
            raise RuntimeError(f"{label} gates not fully passed({label} 게이트가 모두 통과하지 않았습니다)")
    for label, final in [("HN", hn_final), ("HI", hi_final), ("FJ", read_json(fj.FINAL_DECISION))]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if str(final.get(key, "not_claimed")) != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    return hn_final, hi_final, selected


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        name = Path(path).name
        role = "source_input(원천 입력)"
        if "onnx" in name:
            role = "source_onnx_model(원천 온엑스 모델)"
        elif "feature" in name:
            role = "feature_contract_or_matrix(피처 계약 또는 행렬)"
        elif "veto" in name:
            role = "probability_bin_veto_contract(확률 구간 거부 계약)"
        elif path == Path(__file__):
            role = "producer_script(생산 스크립트)"
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
                "role": role,
                "effect": "HO package(HO 패키지)의 artifact lineage(산출물 계보)를 연결합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def materialize_feature_matrix() -> dict[str, Any]:
    base_order = fj.et.dt.load_feature_order()
    frame = fj.et.dt.load_dataset(base_order)
    feature_order = fj.fj_feature_sets(base_order)[FEATURE_SET_ID]
    missing = [column for column in feature_order if column not in frame.columns]
    if missing:
        raise RuntimeError("feature columns missing(피처 열 누락): " + ", ".join(missing[:30]))
    if len(feature_order) != 60:
        raise RuntimeError(f"feature count mismatch(피처 수 불일치): {len(feature_order)} != 60")
    probe_frame = frame[frame["split"].astype(str).isin(["validation", "oos"])].copy()
    if probe_frame.empty:
        raise RuntimeError("validation/oos rows missing(검증/표본외 행 누락)")
    metadata = ["entry_open", "open", "high", "low", "close", "volume"]
    export = export_mt5_feature_matrix_csv(probe_frame, feature_order, FEATURE_MATRIX, timestamp_column="timestamp", metadata_columns=metadata)
    payload = {
        "run_id": RUN_ID,
        "model_id": MODEL_ID,
        "feature_set_id": FEATURE_SET_ID,
        "model_input_dataset": rel(MODEL_INPUT_DATASET),
        "model_input_dataset_sha256": sha(MODEL_INPUT_DATASET),
        "base_feature_order": rel(MODEL_INPUT_FEATURE_ORDER),
        "base_feature_order_hash": ordered_hash(base_order),
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "feature_columns": feature_order,
        "matrix": rel(FEATURE_MATRIX),
        "matrix_sha256": sha(FEATURE_MATRIX),
        "export": export,
        "split_scope": "validation+oos(검증+표본외)",
        "timestamp_semantics": "bar_time_server is closed M5 bar close time(닫힌 M5 봉 종료 시각)",
        "effect": "MT5 EA(MT5 전문가 자문)가 FJ ONNX(FJ 온엑스) 입력을 같은 순서로 읽게 합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_ORDER_CONTRACT, payload)
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
                "matrix_path": rel(FEATURE_MATRIX),
                "matrix_sha256": sha(FEATURE_MATRIX),
                "timestamp_semantics": payload["timestamp_semantics"],
                "effect": "single-source feature CSV(단일 원천 피처 CSV)를 MT5 handoff(MT5 인계)로 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return payload


def materialize_mt5_compatible_onnx() -> dict[str, Any]:
    import onnx
    from onnx import TensorProto, helper

    model = onnx.load_model_from_string(io_path(SOURCE_ONNX).read_bytes())
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
    io_path(MT5_ONNX.parent).mkdir(parents=True, exist_ok=True)
    io_path(MT5_ONNX).write_bytes(model.SerializeToString())
    row = {
        "run_id": RUN_ID,
        "route_role": "single_source_fj(단일 원천 FJ)",
        "model_id": MODEL_ID,
        "source_onnx": rel(SOURCE_ONNX),
        "source_sha256": sha(SOURCE_ONNX),
        "mt5_compatible_onnx": rel(MT5_ONNX),
        "mt5_onnx_sha256": sha(MT5_ONNX),
        "zipmap_removed": bool(zipmap_nodes),
        "probability_tensor_name": probability_tensor_name,
        "outputs_before": json.dumps(outputs_before, ensure_ascii=False),
        "outputs_after": json.dumps([{"name": value.name, "value_type": value.type.WhichOneof("value")} for value in model.graph.output], ensure_ascii=False),
        "effect": "ZipMap(집맵)을 제거해 MT5가 probability tensor(확률 텐서)를 직접 읽게 합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(MT5_ONNX_AUDIT, [row])
    return row


def bin_for_value(value: float, edges: Sequence[float]) -> int:
    if not math.isfinite(value) or len(edges) < 2:
        return -1
    for index in range(len(edges) - 1):
        lower = edges[index]
        upper = edges[index + 1]
        if index == 0 and value >= lower and value <= upper:
            return index
        if index > 0 and value > lower and value <= upper:
            return index
    return -1


def apply_veto_to_expected_tape(params: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    tape = read_csv(fj.SELECTED_TRADE_TAPE)
    pflat_edges = [float(item) for item in str(params["InpProbabilityBinVetoPFlatEdges"]).split("|") if item]
    gap_edges = [float(item) for item in str(params["InpProbabilityBinVetoShortLongGapEdges"]).split("|") if item]
    rules = set()
    for record in str(params["InpProbabilityBinVetoRules"]).split(";"):
        if not record.strip():
            continue
        hour, pflat_bin, gap_bin = record.split("|")[:3]
        rules.add((int(hour), int(pflat_bin), int(gap_bin)))
    tape["pflat_bin"] = tape["p_flat"].astype(float).map(lambda value: bin_for_value(value, pflat_edges))
    tape["short_long_gap"] = tape["p_short"].astype(float) - tape["p_long"].astype(float)
    tape["short_long_gap_bin"] = tape["short_long_gap"].map(lambda value: bin_for_value(float(value), gap_edges))
    tape["probability_bin_vetoed"] = tape.apply(lambda row: (int(float(row["open_hour"])), int(row["pflat_bin"]), int(row["short_long_gap_bin"])) in rules, axis=1)
    tape["ho_run_id"] = RUN_ID
    tape["ho_claim_boundary"] = CLAIM_BOUNDARY
    io_path(EXPECTED_TRADE_TAPE.parent).mkdir(parents=True, exist_ok=True)
    tape.to_csv(io_path(EXPECTED_TRADE_TAPE), index=False, encoding="utf-8-sig")
    audit_rows = []
    for split, part in tape.groupby("split", dropna=False):
        vetoed = int(part["probability_bin_vetoed"].sum())
        audit_rows.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "input_trade_count": int(len(part)),
                "vetoed_trade_count": vetoed,
                "kept_trade_count": int(len(part) - vetoed),
                "vetoed_net_profit": finite(part.loc[part["probability_bin_vetoed"], "net_profit"].astype(float).sum()),
                "status": "no_proxy_trade_vetoed(프록시 거래 거부 없음)" if vetoed == 0 else "proxy_trade_vetoed(프록시 거래 거부 있음)",
                "effect": "FJ selected tape(FJ 선택 거래 목록)에 기존 probability-bin veto(확률 구간 거부)가 미치는 영향을 기록합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(VETO_APPLICABILITY_AUDIT, audit_rows)
    return tape, audit_rows


def expected_kpi_rows(tape: pd.DataFrame, selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    kept = tape[~tape["probability_bin_vetoed"]].copy()
    for split in ["validation", "oos", "combined"]:
        part = kept if split == "combined" else kept[kept["split"].astype(str) == split]
        values = part["net_profit"].astype(float) if not part.empty else pd.Series(dtype=float)
        long_count = int((part["direction"].astype(str) == "long").sum()) if not part.empty else 0
        short_count = int((part["direction"].astype(str) == "short").sum()) if not part.empty else 0
        rows.append(
            {
                "run_id": RUN_ID,
                "view": "split_total(분할 전체)" if split != "combined" else "combined_total(합산 전체)",
                "split": split,
                "route_role": "single_source_fj(단일 원천 FJ)",
                "trade_count": int(len(part)),
                "net_profit": finite(values.sum()),
                "profit_factor": profit_factor(values),
                "expectancy": finite(values.mean() if len(values) else math.nan),
                "long_trade_count": long_count,
                "short_trade_count": short_count,
                "trade_density": selected.get(f"selected_{split}_trade_density", "") if split != "combined" else selected.get("selected_combined_trade_density", ""),
                "probability_bin_vetoed_count": int(tape[tape["split"].astype(str).eq(split)]["probability_bin_vetoed"].sum()) if split != "combined" else int(tape["probability_bin_vetoed"].sum()),
                "effect": "HP에서 MT5 runtime telemetry(MT5 런타임 기록)와 비교할 expected proxy KPI(예상 프록시 핵심 성과 지표)를 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EXPECTED_KPI_SUMMARY, rows)
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
    result = copy_to_common_files(hj.basepkg.DEFAULT_COMMON_FILES, local_path, common_path)
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
        copy_common(FEATURE_MATRIX, f"{COMMON_FEATURE_DIR}/single_fj_features.csv", "common_single_source_feature_matrix", "FJ feature matrix(FJ 피처 행렬)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(MT5_ONNX, f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx", "common_single_source_onnx", "FJ MT5-compatible ONNX(FJ MT5 호환 온엑스)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(FEATURE_ORDER_CONTRACT, f"{COMMON_CONFIG_DIR}/feature_order_contract.json", "common_feature_order_contract", "feature order contract(피처 순서 계약)을 Common Files(공용 파일)에 복사합니다."),
        copy_common(hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON, f"{COMMON_CONFIG_DIR}/probability_bin_veto_parameter_contract.json", "common_probability_bin_veto_contract", "probability-bin veto contract(확률 구간 거부 계약)을 Common Files(공용 파일)에 복사합니다."),
        copy_common(EXPECTED_TRADE_TAPE, f"{COMMON_EXPECTED_DIR}/expected_single_source_trade_tape.csv", "common_expected_trade_tape", "expected trade tape(예상 거래 목록)를 비교 입력으로 복사합니다."),
        copy_common(EXPECTED_KPI_SUMMARY, f"{COMMON_EXPECTED_DIR}/expected_kpi_summary.csv", "common_expected_kpi_summary", "expected KPI(예상 핵심 성과 지표)를 비교 입력으로 복사합니다."),
    ]
    write_csv(COMMON_FILES_SYNC, rows)
    return rows


def materialize_set_and_ini(selected: Mapping[str, Any], feature_payload: Mapping[str, Any], veto_params: Mapping[str, Any]) -> dict[str, Any]:
    common_feature = f"{COMMON_FEATURE_DIR}/single_fj_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_telemetry = f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_telemetry.csv"
    common_summary = f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_summary.csv"
    threshold = float(selected["selected_threshold"])
    margin = float(selected.get("selected_margin_vs_flat", -0.08))
    set_values: dict[str, Any] = {
        "InpRunId": f"{RUN_ID}_{ATTEMPT_NAME}",
        "InpExplorationLabel": "stage364HO__SingleSourceProbabilityBinVetoRuntimeProbe",
        "InpTierLabel": "Tier A single-source",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_single_source_probability_bin_veto",
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
        "InpCsvTimestampIsBarClose": True,
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
        "InpFallbackTierLabel": "Tier B fallback disabled",
        "InpFallbackFeatureCsvPath": "",
        "InpFallbackFeatureCount": 0,
        "InpFallbackModelPath": "",
        "InpFallbackModelId": "",
        "InpFallbackModelBackend": "onnx",
        "InpFallbackFeatureOrderHash": "",
        "InpFallbackUseOnPrimaryFlat": False,
        "InpFallbackPrimaryFlatRequiresNoPosition": True,
        "InpFallbackUseOnPrimaryLowConfidence": False,
        "InpFallbackPrimaryMaxConfidence": 0.0,
        "InpFallbackLowConfidenceRequiresNoPosition": True,
        "InpShortThreshold": threshold,
        "InpLongThreshold": threshold,
        "InpMinMargin": margin,
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpFallbackShortThreshold": threshold,
        "InpFallbackLongThreshold": threshold,
        "InpFallbackMinMargin": margin,
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
        "InpMagic": 36452001,
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
    set_path = SET_DIR / "OPv2_run364HO_single_source_probability_bin_veto.set"
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    report_name = "Project_Obsidian_Prime_v2_run364HP_single_source_probability_bin_veto_runtime_probe"
    ini_path = INI_DIR / "OPv2_run364HO_single_source_probability_bin_veto.ini"
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
                "attempt_name": ATTEMPT_NAME,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "model_id": MODEL_ID,
                "feature_count": feature_payload["feature_count"],
                "threshold": threshold,
                "margin_vs_flat": margin,
                "fallback_enabled": False,
                "probability_bin_veto_rules": veto_params["InpProbabilityBinVetoRules"],
                "expected_oos_net": selected["selected_oos_net"],
                "expected_oos_profit_factor": selected["selected_oos_profit_factor"],
                "expected_oos_trade_density": selected["selected_oos_trade_density"],
                "runtime_representation": "single_source_probability_bin_veto_supported(단일 원천 확률 구간 거부 지원)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_INI_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "terminal_path": hj.basepkg.DEFAULT_TERMINAL.as_posix(),
                "report_name": report_name,
                "from_date": "2025.01.02",
                "to_date": "2026.04.14",
                "effect": "Strategy Tester(전략 테스터) 실행 범위와 report(보고서) 이름을 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return {
        "set_path": set_path,
        "ini_path": ini_path,
        "set_sha256": set_payload["sha256"],
        "ini_sha256": ini_payload["sha256"],
        "parameter_count": set_payload["parameter_count"],
        "report_name": report_name,
        "threshold": threshold,
        "margin_vs_flat": margin,
        "expected_oos_net": selected["selected_oos_net"],
        "expected_oos_profit_factor": selected["selected_oos_profit_factor"],
        "expected_oos_trade_density": selected["selected_oos_trade_density"],
        "expected_oos_trade_count": selected["selected_oos_trade_count"],
        "expected_oos_long_trade_count": selected["selected_oos_long_trade_count"],
        "expected_oos_short_trade_count": selected["selected_oos_short_trade_count"],
    }


def write_contracts(
    selected: Mapping[str, Any],
    feature_payload: Mapping[str, Any],
    package: Mapping[str, Any],
    veto_params: Mapping[str, Any],
) -> None:
    runtime_policy = {
        "run_id": RUN_ID,
        "model_id": MODEL_ID,
        "feature_contract": "single-source 60 features(단일 원천 60개 피처)",
        "output_contract": "p_short_p_flat_p_long_probability_tensor_threshold_margin_probability_bin_veto",
        "probability_bin_veto": dict(veto_params),
        "expected_proxy_oos": {
            "net_profit": selected["selected_oos_net"],
            "profit_factor": selected["selected_oos_profit_factor"],
            "trade_count": selected["selected_oos_trade_count"],
            "trade_density": selected["selected_oos_trade_density"],
            "runtime_density_estimate_from_hl_ratio": read_json(hn.FINAL_DECISION)["selected_runtime_density_estimate_from_hl_ratio"],
        },
        "known_differences": [
            "FJ proxy selected tape(FJ 프록시 선택 거래 목록)는 open-to-open proxy(시가-시가 프록시)이고 MT5 fill/spread/position timing(MT5 체결/스프레드/포지션 시점)과 다를 수 있습니다.",
            "Probability-bin veto(확률 구간 거부)는 FJ selected proxy tape(FJ 선택 프록시 거래 목록)에서 0건을 막지만, MT5 bar-by-bar runtime(MT5 봉별 런타임)에서는 후보 생성 순서 차이가 생길 수 있습니다.",
            "Scaled density estimate(스케일 밀도 추정)는 HL density ratio(HL 밀도 비율)를 재사용한 단서이며 MT5 proof(MT5 증명)가 아닙니다.",
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
            "mt5_onnx": rel(MT5_ONNX),
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
                "route_role": "single_source_fj(단일 원천 FJ)",
                "model_id": MODEL_ID,
                "source_onnx": rel(SOURCE_ONNX),
                "source_onnx_sha256": sha(SOURCE_ONNX),
                "mt5_compatible_onnx": rel(MT5_ONNX),
                "mt5_onnx_sha256": sha(MT5_ONNX),
                "joblib_path": rel(SOURCE_JOBLIB),
                "joblib_sha256": sha(SOURCE_JOBLIB),
                "feature_count": feature_payload["feature_count"],
                "feature_order_hash": feature_payload["feature_order_hash"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_REPRESENTATION_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "item": "single_source_route(단일 원천 라우트)",
                "source_meaning": "FJ selected model emits p_short/p_flat/p_long(FJ 선택 모델이 숏/플랫/롱 확률 출력)",
                "runtime_meaning": "EA uses one ONNX and fallback disabled(EA가 ONNX 하나를 쓰고 대체 라우트 비활성)",
                "status": "represented(표현됨)",
                "known_difference": "MT5 fill/spread/timing can differ(MT5 체결/스프레드/시점은 다를 수 있음)",
                "effect": "HJ dual-source partial route(HJ 이중 원천 부분 라우트) 복잡도를 제거합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "item": "probability_bin_veto(확률 구간 거부)",
                "source_meaning": "same HI p_flat and short-long gap bins(HI와 같은 p_flat 및 숏-롱 차이 구간)",
                "runtime_meaning": "ProbabilityBinVeto.mqh applies same bin semantics(동일 구간 의미 적용)",
                "status": "represented_zero_proxy_veto(표현됨, 프록시 거부 0건)",
                "known_difference": "candidate timing may differ in MT5(MT5에서 후보 시점이 다를 수 있음)",
                "effect": "HP에서 probability-bin veto(확률 구간 거부)가 실제 런타임에 어떤 차이를 내는지 볼 수 있습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "item": "trade_density_goal(거래 밀도 목표)",
                "source_meaning": "direct OOS proxy density below 3/day but scaled estimate above 3/day(직접 표본외 프록시 밀도는 3/day 미만이나 스케일 추정은 3/day 초과)",
                "runtime_meaning": "HP must measure actual MT5 trade density(HP가 실제 MT5 거래 밀도를 측정해야 함)",
                "status": "not_operating_candidate_yet(아직 운영 후보 아님)",
                "known_difference": "scaled estimate is not proof(스케일 추정은 증명 아님)",
                "effect": "운영 주장을 막고 외부 검증으로 넘깁니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    write_json(
        RUNTIME_PARITY_CONTRACT,
        {
            "run_id": RUN_ID,
            "research_path": rel(fj.SELECTED_CANDIDATE),
            "runtime_path": rel(package["set_path"]),
            "shared_contract": {
                "symbol": "US100",
                "timeframe": "M5",
                "output_order": ["p_short", "p_flat", "p_long"],
                "feature_count": feature_payload["feature_count"],
                "feature_order_hash": feature_payload["feature_order_hash"],
                "probability_bin_veto": dict(veto_params),
                "max_hold_bars": 2,
                "fixed_lot": 0.1,
                "fallback_enabled": False,
            },
            "known_differences": runtime_policy["known_differences"],
            "parity_check": rel(RUNTIME_REPRESENTATION_AUDIT),
            "parity_identity": {
                "tester_set_sha256": package["set_sha256"],
                "tester_ini_sha256": package["ini_sha256"],
                "mt5_onnx_sha256": sha(MT5_ONNX),
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
                "comparison_subject": "expected_single_source_trade_tape_vs_runtime_telemetry(예상 단일 원천 거래 목록 대 런타임 기록)",
                "proxy_input": rel(EXPECTED_TRADE_TAPE),
                "mt5_runtime_output": f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_telemetry.csv",
                "required_next_run": NEXT_RUN_ID,
                "diff_axes": "matched_rows,mismatch_rows,net_profit,profit_factor,trade_count,trade_density,side_mix,skip_reason(일치/불일치 행, 순수익, 수익 팩터, 거래수, 거래 밀도, 방향 비율, 스킵 사유)",
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
    write_csv(
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "tier": "Tier A single-source(Tier A 단일 원천)",
                "split": "validation_oos",
                "tester_set": rel(package["set_path"]),
                "tester_ini": rel(package["ini_path"]),
                "runtime_policy": rel(RUNTIME_POLICY_CONFIG),
                "runtime_parity_contract": rel(RUNTIME_PARITY_CONTRACT),
                "proxy_mt5_comparison_contract": rel(PROXY_MT5_COMPARISON_CONTRACT),
                "common_files_sync": rel(COMMON_FILES_SYNC),
                "expected_trade_tape": rel(EXPECTED_TRADE_TAPE),
                "expected_kpi_summary": rel(EXPECTED_KPI_SUMMARY),
                "status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "HP 실행이 읽을 tester handoff(테스터 인계)를 한 줄로 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364HP_EXECUTION_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "hp01_execute_single_source_probability_bin_veto_mt5_runtime_probe",
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "tester_ini": rel(package["ini_path"]),
                "tester_set": rel(package["set_path"]),
                "comparison_contract": rel(PROXY_MT5_COMPARISON_CONTRACT),
                "effect": "다음 작업에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하도록 대기열을 만듭니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(package: Mapping[str, Any], compile_payload: Mapping[str, Any], final_written: bool) -> list[dict[str, Any]]:
    common_paths = read_csv(COMMON_FILES_SYNC)
    common_ok = not common_paths.empty and all(Path(str(row.get("common_absolute_path", ""))).exists() for _, row in common_paths.iterrows())
    receipt_paths = [WORK_PACKET_RECEIPT, RUNTIME_RECEIPT, BACKTEST_RECEIPT, ENV_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), INPUT_MANIFEST, "입력 계보가 연결됐습니다."),
        ("feature_matrix_gate", exists(FEATURE_MATRIX) and exists(FEATURE_ORDER_CONTRACT), FEATURE_MATRIX_AUDIT, "single-source feature CSV(단일 원천 피처 CSV)가 작성됐습니다."),
        ("onnx_handoff_gate", exists(MT5_ONNX) and exists(MT5_ONNX_AUDIT), MT5_ONNX_AUDIT, "MT5-compatible ONNX handoff(MT5 호환 온엑스 인계)가 작성됐습니다."),
        ("probability_bin_veto_parameter_gate", exists(hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON), hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON, "probability-bin veto(확률 구간 거부) 파라미터가 연결됐습니다."),
        ("veto_applicability_gate", exists(VETO_APPLICABILITY_AUDIT), VETO_APPLICABILITY_AUDIT, "FJ 선택 테이프에서 veto(거부) 적용성을 기록했습니다."),
        ("runtime_representation_gate", exists(RUNTIME_REPRESENTATION_AUDIT) and exists(RUNTIME_PARITY_CONTRACT), RUNTIME_REPRESENTATION_AUDIT, "runtime representation(런타임 표현)을 기록했습니다."),
        ("compile_gate", bool(compile_payload.get("compile_log_zero_errors")) and bool(compile_payload.get("portable_copied")), COMPILE_RESULT, "MetaEditor compile(메타에디터 컴파일) 오류 0개와 portable EA(휴대 실행 EA) 복사를 확인했습니다."),
        ("runtime_handoff_package_gate", exists(package["set_path"]) and exists(package["ini_path"]) and exists(RUNTIME_PROBE_ATTEMPT_PACKAGE), RUNTIME_PROBE_ATTEMPT_PACKAGE, "set/ini/attempt package(설정/초기화/시도 패키지)가 작성됐습니다."),
        ("common_files_sync_gate", common_ok, COMMON_FILES_SYNC, "Common Files(공용 파일) 복사가 확인됐습니다."),
        ("proxy_mt5_comparison_contract_gate", exists(PROXY_MT5_COMPARISON_CONTRACT), PROXY_MT5_COMPARISON_CONTRACT, "proxy vs MT5(프록시 대 MT5) 비교 계약이 작성됐습니다."),
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


def final_payload(
    created_at: str,
    selected: Mapping[str, Any],
    feature_payload: Mapping[str, Any],
    package: Mapping[str, Any],
    compile_payload: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    all_passed = all(row["status"] == "passed" for row in gates)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if all_passed else RUN_ID,
        "status": STATUS if all_passed else "blocked_stage364HO_single_source_runtime_package_gate_failure_repair_required_no_authority",
        "judgment": JUDGMENT if all_passed else "inconclusive_single_source_runtime_package_gate_failure_repair_required_no_authority",
        "decision": DECISION if all_passed else "stage364HO_repair_single_source_runtime_package_gate_failure",
        "model_id": MODEL_ID,
        "feature_count": feature_payload["feature_count"],
        "feature_order_hash": feature_payload["feature_order_hash"],
        "feature_matrix_rows": feature_payload["export"]["rows"],
        "mt5_onnx": rel(MT5_ONNX),
        "mt5_onnx_sha256": sha(MT5_ONNX) if exists(MT5_ONNX) else "",
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "report_name": package["report_name"],
        "threshold": package["threshold"],
        "margin_vs_flat": package["margin_vs_flat"],
        "expected_oos_net": package["expected_oos_net"],
        "expected_oos_profit_factor": package["expected_oos_profit_factor"],
        "expected_oos_trade_density": package["expected_oos_trade_density"],
        "expected_oos_trade_count": package["expected_oos_trade_count"],
        "expected_oos_long_trade_count": package["expected_oos_long_trade_count"],
        "expected_oos_short_trade_count": package["expected_oos_short_trade_count"],
        "expected_runtime_density_estimate_from_hl_ratio": read_json(hn.FINAL_DECISION)["selected_runtime_density_estimate_from_hl_ratio"],
        "runtime_representation": "single_source_probability_bin_veto_supported(단일 원천 확률 구간 거부 지원)",
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
    write_json(WORK_PACKET_RECEIPT, {**base, "work_packet": rel(WORK_PACKET), "primary_family": "runtime_package(런타임 패키지)", "status": "completed(완료)"})
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(fj.SELECTED_CANDIDATE),
            "runtime_path": rel(package["set_path"]),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": read_json(RUNTIME_POLICY_CONFIG)["known_differences"],
            "parity_check": rel(RUNTIME_REPRESENTATION_AUDIT),
            "parity_identity": rel(RUNTIME_PACKAGE_MANIFEST),
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(BACKTEST_RECEIPT, {**base, "tester_ini": rel(package["ini_path"]), "tester_set": rel(package["set_path"]), "tester_output_status": "not_run(미실행)", "next_probe": NEXT_RUN_ID, "forensics_status": "identity_prepared_output_absent(정체성 준비, 출력 없음)"})
    write_json(ENV_RECEIPT, {**base, "metaeditor": DEFAULT_METAEDITOR.as_posix(), "terminal": hj.basepkg.DEFAULT_TERMINAL.as_posix(), "common_files": hj.basepkg.DEFAULT_COMMON_FILES.as_posix(), "compile_result": rel(COMPILE_RESULT), "environment_judgment": "usable_for_next_mt5_probe(다음 MT5 탐침에 사용 가능)"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)", "lineage_judgment": "connected_with_boundary(경계 포함 연결)"})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(FEATURE_MATRIX_AUDIT), rel(MT5_ONNX_AUDIT), rel(COMPILE_RESULT), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)], "evidence_missing": ["MT5 tester output(MT5 테스터 출력)", "forward/replay evidence(전진/재생 근거)", "runtime authority closure(런타임 권위 종료)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID, "user_explanation_hook": "Package is ready for MT5 probe, not runtime authority(패키지는 MT5 탐침 준비이지 런타임 권위가 아님)."})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "single-source MT5 runtime probe package prepared and compile checked(단일 원천 MT5 런타임 탐침 패키지 준비 및 컴파일 확인)", "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364HO Single-Source Probability-Bin Veto Runtime Package(단일 원천 확률 구간 거부 런타임 패키지)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- model(모델): `{MODEL_ID}`
- feature contract(피처 계약): `{final['feature_count']}` features(피처), hash(해시) `{final['feature_order_hash']}`
- set/ini(설정/초기화): `{final['set_path']}` / `{final['ini_path']}`
- compile zero errors(컴파일 오류 0): `{final['compile_log_zero_errors']}`
- portable EA copied(휴대 실행 EA 복사): `{final['portable_ea_copied']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

## Action/Effect(행동/효과)

Action(행동): HN이 승인한 FJ single-source seed(FJ 단일 원천 씨앗)를 MT5-compatible ONNX(MT5 호환 온엑스), feature CSV(피처 CSV), probability-bin veto(확률 구간 거부) set/ini(설정/초기화 파일), Common Files(공용 파일) handoff(인계)로 materialize(물질화)했습니다.

Effect(효과): HP에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy vs MT5(프록시 대 MT5) 차이를 기록할 수 있습니다.

## Expected Proxy(예상 프록시)

- OOS net/PF/density/trades(표본외 순수익/수익 팩터/밀도/거래수): `{final['expected_oos_net']}` / `{final['expected_oos_profit_factor']}` / `{final['expected_oos_trade_density']}` / `{final['expected_oos_trade_count']}`
- scaled density estimate(스케일 밀도 추정): `{final['expected_runtime_density_estimate_from_hl_ratio']}`
- OOS long/short(표본외 롱/숏): `{final['expected_oos_long_trade_count']}` / `{final['expected_oos_short_trade_count']}`

## Runtime Boundary(런타임 경계)

- probability-bin veto(확률 구간 거부)는 enabled(활성)입니다.
- FJ selected proxy tape(FJ 선택 프록시 거래 목록)에서 vetoed trades(거부 거래)는 0건입니다.
- scaled density estimate(스케일 밀도 추정)는 MT5 proof(MT5 증명)가 아닙니다.
- 이 run(실행)은 runtime package(런타임 패키지)만 만들었고 MT5 execution(MT5 실행)은 아직 하지 않았습니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364HO decision(결정): single-source probability-bin veto runtime package(단일 원천 확률 구간 거부 런타임 패키지)

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
    append_text_once(REVIEW_INDEX, f"run364HO__{RUN_ID}", f"\n- run364HO__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - single-source probability-bin veto runtime package(단일 원천 확률 구간 거부 런타임 패키지), next `{final['next_run_id']}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HO__{RUN_ID}", f"\n<!-- run364HO__{RUN_ID} -->\n\n## run364HO Single-Source Runtime Package(단일 원천 런타임 패키지)\n\nAction(행동): FJ ONNX(FJ 온엑스), feature CSV(피처 CSV), probability-bin veto(확률 구간 거부) set/ini(설정/초기화 파일)를 물질화했습니다.\n\nEffect(효과): `{final['next_run_id']}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다. 운영 권위는 없습니다.\n")
    append_text_once(STAGE_README, f"run364HO__{RUN_ID}", f"\n<!-- run364HO__{RUN_ID} -->\n## run364HO runtime package(런타임 패키지)\n\nCandidate(후보): `{MODEL_ID}`. Next(다음): `{final['next_run_id']}`.\n")
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

Current truth(현재 진실): `run364HO` materialized(물질화 완료) single-source probability-bin veto runtime package(단일 원천 확률 구간 거부 런타임 패키지). Model(모델)은 `{MODEL_ID}`이고 feature contract(피처 계약)은 `{final['feature_count']}`개입니다. set/ini(설정/초기화 파일)는 `{final['set_path']}` / `{final['ini_path']}`입니다. MetaEditor compile(메타에디터 컴파일)은 `compile_zero_errors={final['compile_log_zero_errors']}`입니다.

Expected proxy(예상 프록시): OOS net/PF/density/trades(표본외 순수익/수익 팩터/밀도/거래수)는 `{final['expected_oos_net']}` / `{final['expected_oos_profit_factor']}` / `{final['expected_oos_trade_density']}` / `{final['expected_oos_trade_count']}`입니다. scaled density estimate(스케일 밀도 추정)는 `{final['expected_runtime_density_estimate_from_hl_ratio']}`입니다.

Important boundary(중요 경계): runtime package(런타임 패키지)는 준비됐지만 MT5 Strategy Tester(MT5 전략 테스터) 출력은 아직 없습니다. scaled density estimate(스케일 밀도 추정)는 MT5 proof(MT5 증명)가 아닙니다.

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

Runtime package(런타임 패키지): single-source FJ(단일 원천 FJ), probability-bin veto(확률 구간 거부) supported(지원).

Expected OOS net/PF/density/trades(예상 표본외 순수익/수익 팩터/밀도/거래수): `{final['expected_oos_net']}` / `{final['expected_oos_profit_factor']}` / `{final['expected_oos_trade_density']}` / `{final['expected_oos_trade_count']}`.

Goal density note(목표 밀도 메모): direct proxy density(직접 프록시 밀도)는 3/day(일 3회) 미만이지만 scaled density estimate(스케일 밀도 추정)는 `{final['expected_runtime_density_estimate_from_hl_ratio']}`입니다. HP MT5 runtime probe(HP MT5 런타임 탐침)가 실제 밀도를 확인해야 합니다.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364HO__{RUN_ID}", f"\n<!-- run364HO__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed single-source probability-bin veto runtime package(단일 원천 확률 구간 거부 런타임 패키지); next `{final['next_run_id']}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HO__{RUN_ID}", f"\n<!-- run364HO__{RUN_ID} -->\n- `{RUN_ID}`: FJ single-source ONNX(FJ 단일 원천 온엑스)를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 물질화했습니다. Effect(효과): proxy clue(프록시 단서)를 MT5 KPI(MT5 핵심 성과 지표)로 검증할 수 있습니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364HO__no_authority__{RUN_ID}", f"\n<!-- run364HO__no_authority__{RUN_ID} -->\n- `{RUN_ID}`: runtime package(런타임 패키지)는 준비됐지만 MT5 execution(MT5 실행)과 tester output(테스터 출력)이 없어 authority(권위) 없음. Effect(효과): 운영 주장 대신 HP 런타임 탐침으로 넘깁니다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
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
        "work_family": "runtime_package(런타임 패키지)",
        "scoreboard_lane": "runtime_package(런타임 패키지)",
        "external_verification_status": "not_run_package_only(미실행, 패키지 전용)",
        "evidence_boundary": "compile_checked_package_only(컴파일 확인 패키지 전용)",
        "question": "Can the FJ single-source probability-bin veto route be packaged for MT5 runtime probe?(FJ 단일 원천 확률 구간 거부 라우트를 MT5 런타임 탐침으로 패키지화할 수 있는가?)",
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
        "candidate_model_id": MODEL_ID,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "runtime_package(런타임 패키지)", "primary_report": rel(REPORT_PATH)}])
    rows = []
    for suffix, record_view, tier_scope, row_status in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", final["status"]),
        ("tier_b_fallback_used", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required(필수 누락)"),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", final["status"]),
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
                "status": row_status,
                "rows": 0 if "missing_required" in row_status else 1,
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
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
                    "effect": "HO single-source runtime package(HO 단일 원천 런타임 패키지) 산출물입니다.",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)
    repair_run_registry_line_endings(RUN_ID)


def write_run_manifest(final: Mapping[str, Any]) -> None:
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
            "command": "python -B stage_pipelines/stage364/materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db.py",
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    validate_inputs()
    selected = read_json(fj.SELECTED_CANDIDATE)
    veto_params = read_json(hi.PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON)["parameters"]
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "runtime_package(런타임 패키지)",
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
                "veto_applicability_gate",
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
    feature_payload = materialize_feature_matrix()
    materialize_mt5_compatible_onnx()
    expected_tape, _ = apply_veto_to_expected_tape(veto_params)
    expected_kpi_rows(expected_tape, selected)
    common_sync_rows()
    package = materialize_set_and_ini(selected, feature_payload, veto_params)
    write_contracts(selected, feature_payload, package, veto_params)
    compile_payload = compile_and_sync_ea()
    write_receipts({"created_at_utc": created_at, "judgment": JUDGMENT}, package)
    gates = gate_rows(package, compile_payload, final_written=False)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(created_at, selected, feature_payload, package, compile_payload, gates)
    write_json(FINAL_DECISION, final)
    gates = gate_rows(package, compile_payload, final_written=True)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(created_at, selected, feature_payload, package, compile_payload, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final)
    write_run_manifest(final)
    final = {**final, "run_manifest": rel(RUN_MANIFEST), "run_manifest_sha256": sha(RUN_MANIFEST)}
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready({key: final[key] for key in ["run_id", "status", "judgment", "model_id", "feature_count", "feature_matrix_rows", "expected_oos_net", "expected_oos_profit_factor", "expected_oos_trade_density", "expected_runtime_density_estimate_from_hl_ratio", "compile_log_zero_errors", "portable_ea_copied", "gate_passes", "gate_total", "next_run_id", "runtime_authority", "goal_achieve"]}), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
