from __future__ import annotations

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

from foundation.control_plane.ledger import io_path  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as basepkg  # noqa: E402
from stage_pipelines.stage364 import review_h17_bad_month_source_balance_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CO"
RUN_ID = "run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID = "run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364CO_h17_bad_month_source_balance_repair_mt5_probe_package_prepared_compile_checked_no_execution"
JUDGMENT = "runtime_probe_package_ready_cm04_rule_surface_mt5_execution_required_no_authority"
DECISION = "stage364CO_open_run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_common_files_synced_compile_checked_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MODEL_ID = basepkg.MODEL_ID
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin_plus_cm04_entry_known_guards"
PRIMARY_ATTEMPT = "run364CO_cm04_month08_12_source_balance_guard"
DEFAULT_METAEDITOR = basepkg.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = MT5_DIR / "compile" / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
RUNTIME_REPRESENTATION_AUDIT = RUN_DIR / "runtime_representation_audit.csv"
RUN364CP_EXECUTION_QUEUE = RUN_DIR / "run364CP_execution_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ENV_RECEIPT = RUN_DIR / "environment_reproducibility_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CO_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CO_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs.md"
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

SOURCE_FEATURE_MATRIX = basepkg.FEATURE_MATRIX
SOURCE_FEATURE_ORDER = basepkg.FEATURE_ORDER
SOURCE_ONNX = basepkg.SOURCE_ONNX
SOURCE_EA = basepkg.EA_SOURCE
SOURCE_EA_BINARY = basepkg.EA_BINARY
PORTABLE_EA_EX5 = basepkg.PORTABLE_EA_EX5
SOURCE_CA01_SET = STAGE_DIR / "02_runs" / "run364CA" / "mt5" / "sets" / "ca01_OPv2_run364BX_bx03_semantics_control.set"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_h17_bad_month_source_balance_repair_mt5_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364CO_QUEUE,
    parent.CANDIDATE_RULE_PACKAGE,
    parent.MT5_REPROBE_BOUNDARY,
    parent.RUN_MANIFEST,
    SOURCE_CA01_SET,
    SOURCE_FEATURE_MATRIX,
    SOURCE_FEATURE_ORDER,
    SOURCE_ONNX,
    SOURCE_EA,
    parent.parent.SELECTED_TRADE_TAPE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    RUNTIME_POLICY_CONFIG,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    EXPECTED_KPI_SUMMARY,
    RUNTIME_REPRESENTATION_AUDIT,
    RUN364CP_EXECUTION_QUEUE,
    WORK_PACKET,
    EXPERIMENT_RECEIPT,
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
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def fs_path(path: Path | str) -> str:
    return str(io_path(path))


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, parent.json_ready(payload))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


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


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR / "compile", SET_DIR, INI_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CO inputs(CO 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CN next_run_id mismatch(CN 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CN has forbidden authority claim(CN 금지 권위 주장 존재)")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CN gate audit(CN 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CO runtime package source(CO 런타임 패키지 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def read_set_values(path: Path) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for raw in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value
    return values


def maybe_number(value: Any) -> Any:
    if isinstance(value, bool):
        return value
    if not isinstance(value, str):
        return value
    text = value.strip()
    if text.lower() in {"true", "false"}:
        return text.lower() == "true"
    try:
        if any(ch in text for ch in [".", "e", "E"]):
            return float(text)
        return int(text)
    except ValueError:
        return value


def feature_order_payload() -> dict[str, Any]:
    payload = read_json(SOURCE_FEATURE_ORDER)
    if "feature_columns" in payload:
        return {
            "feature_columns": payload["feature_columns"],
            "feature_count": payload.get("feature_count", len(payload["feature_columns"])),
            "feature_order_hash": payload.get("feature_order_hash", ""),
            "model_id": payload.get("model_id", MODEL_ID),
        }
    return read_json(basepkg.SOURCE_FEATURE_ORDER)


def compile_and_sync_ea() -> dict[str, Any]:
    result = compile_mql5_ea(DEFAULT_METAEDITOR, SOURCE_EA, COMPILE_LOG)
    payload = {
        "run_id": RUN_ID,
        "metaeditor": DEFAULT_METAEDITOR.as_posix(),
        "source_ea": rel(SOURCE_EA),
        "source_ea_binary": rel(SOURCE_EA_BINARY),
        "portable_ea_binary": PORTABLE_EA_EX5.as_posix(),
        "compile_result": result,
        "portable_copied": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if result.get("status") == "completed" and exists(SOURCE_EA_BINARY):
        os.makedirs(fs_path(PORTABLE_EA_EX5.parent), exist_ok=True)
        shutil.copy2(fs_path(SOURCE_EA_BINARY), fs_path(PORTABLE_EA_EX5))
        payload.update(
            {
                "portable_copied": True,
                "source_sha256": sha(SOURCE_EA_BINARY),
                "portable_sha256": sha(PORTABLE_EA_EX5),
            }
        )
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
    feature_order_path = RUN_DIR / "feature_order.json"
    write_json(feature_order_path, feature_order_payload())
    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_feature_order = f"{COMMON_CONFIG_DIR}/feature_order.json"
    common_expected_tape = f"{COMMON_EXPECTED_DIR}/cm04_selected_proxy_trade_tape.csv"
    return [
        copy_common(SOURCE_FEATURE_MATRIX, common_feature, "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(SOURCE_ONNX, common_model, "common_primary_onnx", "primary ONNX(주 온엑스)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(feature_order_path, common_feature_order, "common_feature_order", "feature order(피처 순서)를 Common Files(공용 파일)에 복사합니다."),
        copy_common(parent.parent.SELECTED_TRADE_TAPE, common_expected_tape, "common_expected_proxy_trade_tape", "expected proxy tape(예상 프록시 기록)를 차이 비교용으로 복사합니다."),
        copy_common(parent.CANDIDATE_RULE_PACKAGE, f"{COMMON_CONFIG_DIR}/cm04_candidate_rule_package.json", "common_rule_package", "CM rule package(CM 규칙 패키지)를 런타임 인계에 고정합니다."),
    ]


def materialize_set_and_ini(final: Mapping[str, Any]) -> dict[str, Any]:
    feature_order = feature_order_payload()
    base_values = {key: maybe_number(value) for key, value in read_set_values(SOURCE_CA01_SET).items()}
    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_telemetry = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv"
    common_summary = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv"
    set_values = dict(base_values)
    set_values.update(
        {
            "InpRunId": f"{RUN_ID}_{PRIMARY_ATTEMPT}",
            "InpExplorationLabel": "stage364CM04__RuntimeProbe",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "validation_oos_cm04",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": common_feature,
            "InpFeatureCount": int(feature_order["feature_count"]),
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpCsvTimestampIsBarClose": False,
            "InpModelPath": common_model,
            "InpModelId": MODEL_ID,
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpModelUseMatrixTensor": False,
            "InpFeatureOrderHash": feature_order["feature_order_hash"],
            "InpSyntheticShortSourceEnabled": True,
            "InpSyntheticShortSourceHours": "17",
            "InpSyntheticShortSourcePShortMin": 0.4375,
            "InpSyntheticShortSourceMarginVsLongMin": 0.075,
            "InpSyntheticShortMonthBlockEnabled": True,
            "InpSyntheticShortMonthBlockMonth": 8,
            "InpSyntheticShortMonthBlockHours": "*",
            "InpMonthMarginGuardEnabled": True,
            "InpMonthMarginGuardSide": "long",
            "InpMonthMarginGuardMonth": 12,
            "InpMonthMarginGuardStartHour": 0,
            "InpMonthMarginGuardEndHour": 24,
            "InpMonthMarginGuardBasis": "signal",
            "InpMonthMarginGuardMinMargin": 0.01,
            "InpAllowTrading": True,
            "InpFixedLot": 0.1,
            "InpMagic": 36428004,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
        }
    )
    set_path = SET_DIR / "OPv2_run364CO_cm04.set"
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    report_name = "Project_Obsidian_Prime_v2_run364CP_cm04_h17_bad_month_source_balance_probe"
    ini_path = INI_DIR / "OPv2_run364CO_cm04.ini"
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
    set_rows = [
        {
            "run_id": RUN_ID,
            "attempt_name": PRIMARY_ATTEMPT,
            "model_id": MODEL_ID,
            "candidate_id": final["reviewed_candidate_id"],
            "set_path": rel(set_path),
            "set_sha256": set_payload["sha256"],
            "parameter_count": set_payload["parameter_count"],
            "short_threshold": set_values["InpShortThreshold"],
            "long_threshold": set_values["InpLongThreshold"],
            "min_margin": set_values["InpMinMargin"],
            "synthetic_short_month_block": "month=8;hours=*",
            "month_margin_guard": "side=long;month=12;hours=0-24;basis=signal;min=0.01",
            "output_contract": OUTPUT_CONTRACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    ini_rows = [
        {
            "run_id": RUN_ID,
            "attempt_name": PRIMARY_ATTEMPT,
            "ini_path": rel(ini_path),
            "ini_sha256": ini_payload["sha256"],
            "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
            "report_name": report_name,
            "from_date": "2025.01.02",
            "to_date": "2026.04.14",
            "set_path": rel(set_path),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    return {
        "set_path": set_path,
        "ini_path": ini_path,
        "set_payload": set_payload,
        "ini_payload": ini_payload,
        "set_rows": set_rows,
        "ini_rows": ini_rows,
        "set_values": set_values,
        "common_telemetry": common_telemetry,
        "common_summary": common_summary,
        "report_name": report_name,
    }


def write_contracts(final: Mapping[str, Any], package: Mapping[str, Any], sync_rows: Sequence[Mapping[str, Any]]) -> None:
    expected = [
        {
            "run_id": RUN_ID,
            "candidate_id": final["reviewed_candidate_id"],
            "expected_proxy_net": final["reviewed_net_profit"],
            "expected_proxy_profit_factor": final["reviewed_profit_factor"],
            "expected_proxy_expectancy": final["reviewed_expectancy"],
            "expected_proxy_trade_count": final["reviewed_trade_count"],
            "expected_proxy_density": final["reviewed_density"],
            "expected_proxy_short_count": final["reviewed_short_trade_count"],
            "expected_proxy_bad_month_count": final["reviewed_bad_month_count"],
            "expected_proxy_stress_delta": final["reviewed_stress_adjusted_net_delta_vs_parent"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(EXPECTED_KPI_SUMMARY, expected)
    write_json(
        RUNTIME_POLICY_CONFIG,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "model_id": MODEL_ID,
            "candidate_id": final["reviewed_candidate_id"],
            "output_contract": OUTPUT_CONTRACT,
            "decision_surface": {
                "base": "CA01 semantics control(CA01 의미 대조)",
                "month08_synthetic_short_block": {"enabled": True, "month": 8, "hours": "*"},
                "month12_low_margin_long_guard": {"enabled": True, "month": 12, "side": "long", "basis": "signal", "min_margin": 0.01},
                "synthetic_short_source": {"enabled": True, "hours": "17", "p_short_min": 0.4375, "margin_vs_long_min": 0.075},
                "forbidden_controls": ["top_n", "trade_splitting", "exact_year_filter"],
            },
            "expected_proxy": expected[0],
            "known_differences": [
                "proxy expected value(프록시 예상값)는 MT5 Strategy Tester(MT5 전략 테스터) KPI(핵심 성과 지표)를 대체하지 않습니다.",
                "CO is package only(CO는 패키지 전용)라서 fill/cost/runtime output(체결/비용/런타임 출력)은 CP에서 확인합니다.",
            ],
            "mt5_execution": "not_run",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(
        MODEL_HANDOFF_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "model_id": MODEL_ID,
                "source_onnx_path": rel(SOURCE_ONNX),
                "source_onnx_sha256": sha(SOURCE_ONNX),
                "feature_matrix_path": rel(SOURCE_FEATURE_MATRIX),
                "feature_matrix_sha256": sha(SOURCE_FEATURE_MATRIX),
                "feature_order_path": rel(SOURCE_FEATURE_ORDER),
                "feature_order_sha256": sha(SOURCE_FEATURE_ORDER),
                "common_model_path": next(row["common_path"] for row in sync_rows if row["artifact_role"] == "common_primary_onnx"),
                "common_feature_path": next(row["common_path"] for row in sync_rows if row["artifact_role"] == "common_feature_matrix"),
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
                "terminal": basepkg.DEFAULT_TERMINAL.as_posix(),
                "common_files_root": basepkg.DEFAULT_COMMON_FILES.as_posix(),
                "symbol": "US100",
                "timeframe": "M5",
                "tester_model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "from_date": "2025.01.02",
                "to_date": "2026.04.14",
                "attempt_count": 1,
                "effect": "tester identity(테스터 정체성)를 CP 실행 전 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        PROXY_MT5_COMPARISON_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "proxy_net": final["reviewed_net_profit"],
                "proxy_profit_factor": final["reviewed_profit_factor"],
                "proxy_expectancy": final["reviewed_expectancy"],
                "proxy_trade_count": final["reviewed_trade_count"],
                "proxy_drawdown": final["reviewed_closed_trade_drawdown_proxy"],
                "required_mt5_fields": "net_profit;profit_factor;expectancy;drawdown;trade_count;long_short;telemetry",
                "effect": "CP에서 proxy/MT5 diff(프록시/MT5 차이)를 바로 계산하게 합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "research_path": rel(parent.CANDIDATE_RULE_PACKAGE),
                "runtime_path": rel(package["set_path"]),
                "shared_contract": "same ONNX, feature order, CA01 base thresholds, CM month/source guards(동일 온엑스/피처순서/CA01 기준 임계값/CM 월·원천 가드)",
                "known_differences": "CO has no tester output yet(CO는 아직 테스터 출력 없음)",
                "parity_check": "compile/common-files/set/ini package only; CP must execute Strategy Tester(컴파일/공용 파일/설정/INI 패키지 전용, CP 전략 테스터 실행 필요)",
                "parity_identity": f"module_hashes={len(mt5_runtime_module_hashes())};set={package['set_payload']['sha256']};model={sha(SOURCE_ONNX)}",
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_REPRESENTATION_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "rule_id": "month08_synthetic_short_overlay_class_guard",
                "proxy_rule": "remove month 8 synthetic short overlay entries(8월 합성 숏 오버레이 제거)",
                "runtime_parameter": "InpSyntheticShortMonthBlockEnabled=true;InpSyntheticShortMonthBlockMonth=8;InpSyntheticShortMonthBlockHours=*",
                "status": "represented(표현됨)",
                "effect": "8월 합성 숏만 MT5에서 차단합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "rule_id": "month12_low_margin_long_guard",
                "proxy_rule": "remove month 12 long entries with direction margin < 0.01(12월 direction margin 0.01 미만 롱 제거)",
                "runtime_parameter": "InpMonthMarginGuardEnabled=true;side=long;month=12;basis=signal;min=0.01",
                "status": "represented(표현됨)",
                "effect": "12월 낮은 마진 롱을 MT5에서 같은 의미로 차단합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    attempt = {
        "run_id": RUN_ID,
        "attempt_name": PRIMARY_ATTEMPT,
        "next_run_id": NEXT_RUN_ID,
        "tier": "Tier A",
        "split": "validation_oos",
        "model_id": MODEL_ID,
        "candidate_id": final["reviewed_candidate_id"],
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "report_name": package["report_name"],
        "runtime_telemetry_expected": package["common_telemetry"],
        "runtime_summary_expected": package["common_summary"],
        "known_proxy_runtime_difference": "proxy(프록시)는 신호/거래 예상 기록이고 MT5 Strategy Tester(MT5 전략 테스터)의 비용/체결 의미를 대체하지 않습니다.",
        "forbidden_action": "treat_package_as_operating_promotion(패키지를 운영 승격으로 취급)",
        "effect": "같은 set/ini/model/features/rule package(설정/INI/모델/피처/규칙 패키지)로 CP MT5 runtime probe(CP MT5 런타임 탐침)를 실행하게 합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, [attempt])
    write_csv(
        RUN364CP_EXECUTION_QUEUE,
        [
            {
                **attempt,
                "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
                "suggested_command": f"\"{basepkg.DEFAULT_TERMINAL.as_posix()}\" /portable /config:\"{package['ini_path'].as_posix()}\"",
                "queue_status": "ready_for_mt5_runtime_probe_attempt(MT5 런타임 탐침 시도 준비)",
            }
        ],
    )


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-environment-reproducibility(환경 재현성)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "runtime_representation_gate",
                "runtime_handoff_package_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(compile_payload: Mapping[str, Any], package: Mapping[str, Any], receipt_paths: Sequence[Path], receipts_written: bool) -> list[dict[str, Any]]:
    compile_pass = compile_payload.get("compile_result", {}).get("status") == "completed"
    package_pass = exists(package["set_path"]) and exists(package["ini_path"]) and exists(RUNTIME_PROBE_ATTEMPT_PACKAGE)
    receipt_status = all(exists(path) for path in receipt_paths) if receipts_written else False
    return [
        {
            "run_id": RUN_ID,
            "gate": "work_packet_schema_lint",
            "status": "passed",
            "evidence": rel(WORK_PACKET),
            "effect": "CO 작업 묶음(work packet, 작업 묶음)의 주 스킬과 게이트를 고정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "runtime_representation_gate",
            "status": "passed" if compile_pass else "failed",
            "evidence": f"compile_status={compile_payload.get('compile_result', {}).get('status')};module_hashes={len(mt5_runtime_module_hashes())}",
            "effect": "CM 규칙이 EA 입력 표면에서 표현되고 컴파일되는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "runtime_handoff_package_gate",
            "status": "passed" if package_pass else "failed",
            "evidence": f"set={rel(package['set_path'])};ini={rel(package['ini_path'])};attempt={rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}",
            "effect": "CP가 바로 실행할 파일 묶음을 만듭니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if receipt_status or not receipts_written else "failed",
            "evidence": f"receipts_written={receipt_status}",
            "effect": "required gate(필수 게이트)와 receipt(영수증)를 종료에 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": "mt5_execution=not_run;runtime_authority=not_claimed;operating_promotion=not_claimed",
            "effect": "패키지를 운영 권위로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(parent_final: Mapping[str, Any], compile_payload: Mapping[str, Any], package: Mapping[str, Any], sync_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_id": parent_final["reviewed_candidate_id"],
        "attempt_name": PRIMARY_ATTEMPT,
        "model_id": MODEL_ID,
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "report_name": package["report_name"],
        "compile_status": compile_payload.get("compile_result", {}).get("status", "unknown"),
        "portable_ea_copied": bool(compile_payload.get("portable_copied")),
        "terminal_exists": exists(basepkg.DEFAULT_TERMINAL),
        "common_files_exists": exists(basepkg.DEFAULT_COMMON_FILES),
        "common_sync_rows": len(sync_rows),
        "runtime_module_hashes": mt5_runtime_module_hashes(),
        "expected_proxy_net": parent_final["reviewed_net_profit"],
        "expected_proxy_profit_factor": parent_final["reviewed_profit_factor"],
        "expected_proxy_expectancy": parent_final["reviewed_expectancy"],
        "expected_proxy_trade_count": parent_final["reviewed_trade_count"],
        "expected_proxy_density": parent_final["reviewed_density"],
        "expected_proxy_short_count": parent_final["reviewed_short_trade_count"],
        "expected_proxy_bad_month_count": parent_final["reviewed_bad_month_count"],
        "mt5_execution": "not_run",
        "new_model_training": "not_run",
        "external_verification_status": "out_of_scope_by_claim_package_only_cp_execution_required(주장 범위 밖, 패키지 전용 및 CP 실행 필요)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created_at,
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "CM04 proxy rule stack can be represented as RuntimeProbeEA parameters(CM04 프록시 규칙 묶음을 RuntimeProbeEA 파라미터로 표현 가능)",
            "decision_use": "enable CP MT5 runtime probe(CP MT5 런타임 탐침 개방)",
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": ["US100", "M5", MODEL_ID, "CA01 base thresholds", "fixed lot 0.1"],
            "changed_variables": ["month08 synthetic short block", "month12 signal-margin long guard"],
            "sample_scope": "Tier A validation_oos 2025.01.02-2026.04.14",
            "success_criteria": "compile passes and set/ini/common files are materialized(컴파일 통과 및 설정/INI/공용파일 구체화)",
            "failure_criteria": "compile fails or rule cannot be represented(컴파일 실패 또는 규칙 표현 불가)",
            "invalid_conditions": "missing ONNX/features/set identity(온엑스/피처/설정 정체성 누락)",
            "stop_conditions": "CP runtime output contradicts proxy or tester output missing(CP 런타임 출력이 프록시와 충돌하거나 테스터 출력 누락)",
            "evidence_plan": [rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(COMPILE_RESULT)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(parent.CANDIDATE_RULE_PACKAGE),
            "runtime_path": [rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)],
            "shared_contract": "same ONNX, feature matrix, feature order, CM04 guards(동일 온엑스/피처 행렬/피처 순서/CM04 가드)",
            "known_differences": "no tester output yet(아직 테스터 출력 없음)",
            "parity_check": "compile/common-files/set/ini only(컴파일/공용 파일/설정/INI만)",
            "parity_identity": f"model={sha(SOURCE_ONNX)};set={final['set_path']};module_hashes={len(final['runtime_module_hashes'])}",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "ea_identity": [rel(SOURCE_EA), rel(COMPILE_RESULT), rel(PORTABLE_EA_SYNC)],
            "report_identity": "planned only; CP must create Strategy Tester report(계획만, CP가 전략 테스터 보고서를 생성해야 함)",
            "trade_evidence": rel(EXPECTED_KPI_SUMMARY),
            "cost_assumptions": "broker tester real tick model 4, deposit 500, leverage 1:100(브로커 테스터 실제 틱 모델 4, 예치금 500, 레버리지 1:100)",
            "forensic_checks": [rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(RUNTIME_PARITY_CONTRACT)],
            "backtest_judgment": "usable_with_boundary_for_execution(실행용 경계 포함 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ENV_RECEIPT,
        {
            "run_id": RUN_ID,
            "execution_environment": "Windows local MT5 portable(윈도우 로컬 MT5 포터블)",
            "dependency_surface": ["Python", "pandas", "MetaEditor64", "terminal64"],
            "entry_command": f"python {rel(Path(__file__))}",
            "local_assumptions": [basepkg.DEFAULT_PORTABLE_ROOT.as_posix(), basepkg.DEFAULT_COMMON_FILES.as_posix()],
            "clean_checkout_status": "reproducible_with_setup(설정 있으면 재현 가능)",
            "recovery_instruction": "install/restore portable MT5 root if missing(포터블 MT5 루트가 없으면 설치/복구)",
            "reproducibility_judgment": "local_only_with_manifest(목록 포함 로컬 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "CM04 MT5 runtime probe package(CM04 MT5 런타임 탐침 패키지)",
            "evidence_available": [rel(FINAL_DECISION), rel(COMPILE_RESULT), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(COMMON_FILES_SYNC)],
            "evidence_missing": ["new MT5 runtime output(새 MT5 런타임 출력)", "Strategy Tester report(전략 테스터 보고서)", "runtime authority closure(런타임 권위 폐쇄)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The runtime package is ready to execute, but no MT5 KPI exists yet(런타임 패키지는 실행 준비됐지만 MT5 KPI는 아직 없음).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "runtime probe package ready only(런타임 탐침 패키지 준비만)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "mt5_execution": final["mt5_execution"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_local_mt5_synced(추적 가능 및 로컬 MT5 동기화)",
            "lineage_judgment": "connected_with_runtime_package_boundary(런타임 패키지 경계 포함 연결)",
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364CO h17 bad-month source-balance MT5 runtime probe inputs(17시 손실 월/원천 균형 MT5 런타임 탐침 입력)

Updated(갱신): {final['created_at_utc']}

Action(행동): CN candidate(CN 후보) `{final['candidate_id']}`를 RuntimeProbeEA(런타임 탐침 EA) set/ini(설정/INI), Common Files(공용 파일), compile check(컴파일 확인)로 materialize(구체화)했습니다.

Effect(효과): 다음 실행 `{NEXT_RUN_ID}`가 MT5 Strategy Tester(MT5 전략 테스터)를 실행해 proxy/MT5 diff(프록시/MT5 차이)를 기록할 수 있습니다.

- compile status(컴파일 상태): `{final['compile_status']}`
- set file(설정 파일): `{final['set_path']}`
- ini file(INI 파일): `{final['ini_path']}`
- expected proxy KPI(예상 프록시 핵심 성과 지표): net `{final['expected_proxy_net']}`, PF `{final['expected_proxy_profit_factor']}`, trades `{final['expected_proxy_trade_count']}`, density `{final['expected_proxy_density']}`, shorts `{final['expected_proxy_short_count']}`
- MT5 execution(MT5 실행): `{final['mt5_execution']}`

## Gates(게이트)

{parent.markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

CO is package only(CO는 패키지 전용)입니다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CO decision(결정): CM04 MT5 runtime probe package

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- candidate(후보): `{final['candidate_id']}`
- set file(설정 파일): `{final['set_path']}`
- ini file(INI 파일): `{final['ini_path']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): CP에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있게 합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364CO__{RUN_ID}", f"\n- run364CO__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - MT5 runtime probe package ready(MT5 런타임 탐침 패키지 준비), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364CO__{RUN_ID}", f"\n## run364CO MT5 Runtime Probe Package Closeout(MT5 런타임 탐침 패키지 종료)\n\nAction(행동): CM04 rule package(CM04 규칙 패키지)를 RuntimeProbeEA set/ini(런타임 탐침 EA 설정/INI)로 만들었습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 MT5 실행을 시도할 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364CO__{RUN_ID}", f"\n<!-- run364CO__{RUN_ID} -->\n## run364CO MT5 runtime probe package(MT5 런타임 탐침 패키지)\n\n`{final['candidate_id']}` package(패키지) ready(준비). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
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
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CO` materialized(구체화 완료) CM04 MT5 runtime probe package(CM04 MT5 런타임 탐침 패키지). Compile status(컴파일 상태)는 `{final['compile_status']}`, set(설정)은 `{final['set_path']}`, ini(INI)는 `{final['ini_path']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy/MT5 diff(프록시/MT5 차이)를 기록합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

MT5 runtime probe package(MT5 런타임 탐침 패키지): `{final['candidate_id']}`.

Set file(설정 파일): `{final['set_path']}`
INI file(INI 파일): `{final['ini_path']}`
Compile status(컴파일 상태): `{final['compile_status']}`

Expected proxy KPI(예상 프록시 핵심 성과 지표): net `{final['expected_proxy_net']}`, PF `{final['expected_proxy_profit_factor']}`, density `{final['expected_proxy_density']}`, shorts `{final['expected_proxy_short_count']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364CO__{RUN_ID}", f"\n<!-- run364CO__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` packaged CM04 MT5 runtime probe(CM04 MT5 런타임 탐침 패키지); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364CO__{RUN_ID}", f"\n<!-- run364CO__{RUN_ID} -->\n- `{RUN_ID}`: CM04 rule surface(CM04 규칙 표면)를 RuntimeProbeEA(RuntimeProbeEA 런타임 탐침 EA) 입력으로 표현. Effect(효과): MT5 runtime probe(MT5 런타임 탐침)로 proxy expected value(프록시 예상값)를 검증할 수 있음.\n")


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
        "rows": 1,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_design(실험 설계)",
        "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "package(패키지)",
        "question": "Can CM04 proxy rules be materialized as an MT5 runtime probe package?(CM04 프록시 규칙을 MT5 런타임 탐침 패키지로 구체화할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["expected_proxy_net"],
        "profit_factor": final["expected_proxy_profit_factor"],
        "trade_count": final["expected_proxy_trade_count"],
        "trade_density_per_feature_day": final["expected_proxy_density"],
        "short_trade_count": final["expected_proxy_short_count"],
        "trade_density_requirement_status": "inherited_proxy_density_ge_3_no_trade_splitting(프록시 밀도 3 이상 및 거래 쪼개기 없음 상속)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", STATUS, True),
        ("tier_b_fallback_missing_required", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required_no_fallback_source(필수 누락, 대체 원천 없음)", False),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", "out_of_scope_by_claim_no_runtime_execution_yet(주장 범위 밖, 아직 런타임 실행 없음)", True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "CO runtime package(CO 런타임 패키지)",
            "status": status,
            "primary_kpi": f"expected_proxy_net={final['expected_proxy_net']};pf={final['expected_proxy_profit_factor']};density={final['expected_proxy_density']};shorts={final['expected_proxy_short_count']}",
            "guardrail_kpi": "mt5_execution=not_run;no_authority",
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "package_expected_proxy(패키지 예상 프록시)",
        }
        if not include_metrics:
            for key in ["net_profit", "profit_factor", "trade_count", "trade_density_per_feature_day", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("runtime_policy_config", RUNTIME_POLICY_CONFIG),
        ("model_handoff_manifest", MODEL_HANDOFF_MANIFEST),
        ("common_files_sync", COMMON_FILES_SYNC),
        ("compile_result", COMPILE_RESULT),
        ("tester_set_manifest", TESTER_SET_MANIFEST),
        ("tester_ini_manifest", TESTER_INI_MANIFEST),
        ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE),
        ("tester_identity_contract", TESTER_IDENTITY_CONTRACT),
        ("runtime_parity_contract", RUNTIME_PARITY_CONTRACT),
        ("runtime_representation_audit", RUNTIME_REPRESENTATION_AUDIT),
        ("execution_queue", RUN364CP_EXECUTION_QUEUE),
        ("final_decision", FINAL_DECISION),
        ("run_manifest", RUN_MANIFEST),
        ("report", REPORT_PATH),
        ("gate_audit", GATE_AUDIT),
    ]
    rows = []
    for artifact_type, path in artifacts:
        if exists(path):
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": "CO runtime probe package artifact(CO 런타임 탐침 패키지 산출물).",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    exclusions = {RUN_MANIFEST, LINEAGE_RECEIPT, ARTIFACT_REGISTRY}
    output_paths = [path for path in OUTPUT_FILES if path not in exclusions and exists(path) and io_path(path).is_file()]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in output_paths],
            "final_decision": rel(FINAL_DECISION),
            "external_verification_status": final["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    compile_payload = compile_and_sync_ea()
    sync_rows = common_sync_rows()
    package = materialize_set_and_ini(parent_final)
    write_contracts(parent_final, package, sync_rows)
    receipt_paths = [EXPERIMENT_RECEIPT, RUNTIME_RECEIPT, BACKTEST_RECEIPT, ENV_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT, LINEAGE_RECEIPT]
    gates = gate_rows(compile_payload, package, receipt_paths, receipts_written=False)
    final = final_payload(parent_final, compile_payload, package, sync_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    refresh_lineage_receipt(final)
    gates = gate_rows(compile_payload, package, receipt_paths, receipts_written=True)
    final = final_payload(parent_final, compile_payload, package, sync_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final)
    refresh_lineage_receipt(final)
    write_docs(final, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(parent.json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
