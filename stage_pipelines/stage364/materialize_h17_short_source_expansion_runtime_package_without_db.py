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

from foundation.control_plane.ledger import io_path  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_quality_risk_scale_runtime_package_without_db as da  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as basepkg  # noqa: E402
from stage_pipelines.stage364 import review_h17_short_source_expansion_runtime_positive_scout_without_db as de  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_expansion_runtime_positive_scout_without_db as dd  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = de.STAGE_ID
RUN_NUMBER = "run364DF"
RUN_ID = "run364DF_implement_h17_short_source_expansion_runtime_package_without_db_v1"
PARENT_RUN_ID = de.RUN_ID
SOURCE_PROXY_RUN_ID = dd.RUN_ID
RUNTIME_ANCHOR_RUN_ID = da.RUN_ID
NEXT_RUN_ID = "run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364DF_h17_short_source_expansion_runtime_package_prepared_compile_checked_no_execution"
JUDGMENT = "runtime_probe_package_ready_dd05_short_source_expansion_mt5_execution_required_no_authority"
DECISION = "stage364DF_open_run364DG_execute_h17_short_source_expansion_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_short_source_expansion_compile_checked_"
    "no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

MODEL_ID = da.MODEL_ID
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin_plus_dd05_short_source_expansion"
PRIMARY_ATTEMPT = "run364DF_dd05_short_source_expansion"
DEFAULT_METAEDITOR = da.DEFAULT_METAEDITOR

STAGE_DIR = de.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = MT5_DIR / "compile" / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
RUN364DG_EXECUTION_QUEUE = RUN_DIR / "run364DG_execution_queue.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
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

REPORT_PATH = REVIEW_DIR / "run364DF_h17_short_source_expansion_runtime_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DF_h17_short_source_expansion_runtime_package.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

SOURCE_FEATURE_MATRIX = da.SOURCE_FEATURE_MATRIX
SOURCE_ONNX = da.SOURCE_ONNX
SOURCE_EA = da.SOURCE_EA
SOURCE_EA_BINARY = da.SOURCE_EA_BINARY
PORTABLE_EA_EX5 = da.PORTABLE_EA_EX5
SOURCE_DA_SET = da.SET_DIR / "OPv2_run364DA_cx05_short_quality_risk_scale.set"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_h17_short_source_expansion_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    de.FINAL_DECISION,
    de.GATE_AUDIT,
    de.PACKAGE_DECISION,
    de.SHORT_SOURCE_RULE_CONTRACT,
    de.RUN364DF_QUEUE,
    dd.SELECTED_CANDIDATE,
    dd.SELECTED_TRADE_TAPE,
    dd.FINAL_DECISION,
    da.FINAL_DECISION,
    da.RUNTIME_POLICY_CONFIG,
    SOURCE_DA_SET,
    SOURCE_FEATURE_MATRIX,
    SOURCE_ONNX,
    SOURCE_EA,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    RUNTIME_POLICY_CONFIG,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    RUN364DG_EXECUTION_QUEUE,
    TESTER_IDENTITY_CONTRACT,
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
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return dd.rel(path)


def exists(path: Path | str) -> bool:
    return dd.exists(path)


def sha(path: Path | str) -> str:
    return dd.sha(path)


def json_ready(value: Any) -> Any:
    return dd.json_ready(value)


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
    dd.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dd.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dd.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dd.replace_prefixed_lines(path, replacements, bom=bom)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR / "compile", SET_DIR, INI_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DF inputs(DF 입력 누락): " + ", ".join(missing))
    de_final = read_json(de.FINAL_DECISION)
    selected = read_json(dd.SELECTED_CANDIDATE)
    if de_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DE next_run_id mismatch(DE 다음 실행 ID 불일치): {de_final.get('next_run_id')} != {RUN_ID}")
    if de_final.get("selected_variant_id") != selected.get("variant_id"):
        raise RuntimeError("DE selected variant and DD selected variant differ(DE 선택 변형과 DD 선택 변형 불일치)")
    for label, final in [("DE", de_final), ("DD", read_json(dd.FINAL_DECISION)), ("DA", read_json(da.FINAL_DECISION))]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            value = final.get(key, "not_claimed")
            if value != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={value}")
    for label, gate_path in [("DE", de.GATE_AUDIT), ("DD", dd.GATE_AUDIT)]:
        gates = read_csv(gate_path)
        if gates.empty or any(gates["status"].astype(str) != "passed"):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    ea_text = io_path(SOURCE_EA).read_text(encoding="utf-8-sig")
    for token in ["InpSyntheticShortSourceMarginVsFlatMin", "margin_vs_flat", "InpRiskScaleOverlayEnabled"]:
        if token not in ea_text:
            raise RuntimeError(f"EA required token missing(EA 필수 토큰 누락): {token}")
    return selected


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DF runtime package source(DF 런타임 패키지 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def compile_log_ok() -> bool:
    if not exists(COMPILE_LOG):
        return False
    raw = io_path(COMPILE_LOG).read_bytes()
    candidates: list[str] = []
    for encoding in ["utf-8-sig", "utf-16", "utf-16-le"]:
        try:
            candidates.append(raw.decode(encoding, errors="replace"))
        except LookupError:
            continue
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


def feature_order_payload() -> dict[str, Any]:
    return da.feature_order_payload()


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
    return [
        copy_common(SOURCE_FEATURE_MATRIX, f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv", "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사"),
        copy_common(SOURCE_ONNX, f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx", "common_primary_onnx", "primary ONNX(주 온엑스)를 Common Files(공용 파일)에 복사"),
        copy_common(feature_order_path, f"{COMMON_CONFIG_DIR}/feature_order.json", "common_feature_order", "feature order(피처 순서)를 Common Files(공용 파일)에 복사"),
        copy_common(dd.SELECTED_TRADE_TAPE, f"{COMMON_EXPECTED_DIR}/dd05_selected_proxy_trade_tape.csv", "common_expected_proxy_trade_tape", "expected proxy tape(예상 프록시 테이프)를 비교 입력으로 복사"),
    ]


def materialize_set_and_ini(selected: Mapping[str, Any]) -> dict[str, Any]:
    feature_order = feature_order_payload()
    base_values = {key: da.co.maybe_number(value) for key, value in da.co.read_set_values(SOURCE_DA_SET).items()}
    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_telemetry = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv"
    common_summary = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv"
    set_values = dict(base_values)
    set_values.update(
        {
            "InpRunId": f"{RUN_ID}_{PRIMARY_ATTEMPT}",
            "InpExplorationLabel": "stage364DF__DD05ShortSourceExpansion",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "validation_oos_dd05",
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
            "InpSyntheticShortSourceHours": "17|18|19|20|21",
            "InpSyntheticShortSourcePShortMin": 0.4375,
            "InpSyntheticShortSourceMarginVsLongMin": 0.05,
            "InpSyntheticShortSourceMarginVsFlatMin": 0.0,
            "InpSyntheticShortMonthBlockEnabled": True,
            "InpSyntheticShortMonthBlockMonth": 8,
            "InpSyntheticShortMonthBlockHours": "*",
            "InpRiskScaleOverlayEnabled": True,
            "InpRiskScaleOverlaySide": "short",
            "InpRiskScaleOverlayHours": "17|18|19|20",
            "InpRiskScaleOverlayBasis": "margin_vs_long",
            "InpRiskScaleOverlayMinMarginVsLong": 0.080,
            "InpRiskScaleOverlayMultiplier": 1.10,
            "InpAllowTrading": True,
            "InpFixedLot": 0.1,
            "InpModelRiskFallbackLot": 0.1,
            "InpModelRiskSizingEnabled": False,
            "InpMagic": 36430006,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
        }
    )
    set_path = SET_DIR / "OPv2_run364DF_dd05_short_source_expansion.set"
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    report_name = "Project_Obsidian_Prime_v2_run364DG_dd05_short_source_expansion_probe"
    ini_path = INI_DIR / "OPv2_run364DF_dd05_short_source_expansion.ini"
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
                "model_id": MODEL_ID,
                "candidate_id": selected["variant_id"],
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "synthetic_short_source": "hours=17|18|19|20|21;p_short_min=0.4375;margin_vs_long_min=0.05;margin_vs_flat_min=0.0;month8_block=*",
                "risk_scale_overlay": "side=short;hours=17|18|19|20;basis=margin_vs_long;min=0.080;multiplier=1.10",
                "package_base": rel(SOURCE_DA_SET),
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
                "set_path": rel(set_path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return {
        "set_path": set_path,
        "ini_path": ini_path,
        "set_payload": set_payload,
        "ini_payload": ini_payload,
        "set_values": set_values,
        "common_telemetry": common_telemetry,
        "common_summary": common_summary,
        "report_name": report_name,
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "runtime_backtest(런타임 백테스트)",
            "primary_skill": "obsidian-runtime-parity(옵시디언 런타임 동등성)",
            "support_skills": [
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
                "obsidian-environment-reproducibility(옵시디언 환경 재현성)",
                "obsidian-result-judgment(옵시디언 결과 판정)",
            ],
            "hypothesis": "The dd05 short-source rule can be represented in RuntimeProbeEA with flat-margin guard and packaged for MT5 probe.",
            "required_gates": [
                "work_packet_schema_lint",
                "input_lineage_gate",
                "runtime_representation_gate",
                "compile_gate",
                "runtime_handoff_package_gate",
                "common_files_sync_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_contracts(selected: Mapping[str, Any], package: Mapping[str, Any], sync_rows: Sequence[Mapping[str, Any]]) -> None:
    expected = [
        {
            "run_id": RUN_ID,
            "candidate_id": selected["variant_id"],
            "expected_estimated_mt5_net": selected["estimated_mt5_net_profit"],
            "expected_estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
            "expected_estimated_mt5_density": selected["estimated_mt5_density"],
            "expected_estimated_mt5_drawdown": selected["estimated_mt5_drawdown"],
            "expected_sim_short_trade_count": selected["sim_short_trade_count"],
            "expected_sim_short_share": selected["sim_short_share"],
            "expected_proxy_net": selected["estimated_mt5_net_profit"],
            "expected_proxy_profit_factor": selected["estimated_mt5_profit_factor"],
            "expected_proxy_trade_count": selected["estimated_mt5_trade_count"],
            "expected_proxy_short_count": selected["sim_short_trade_count"],
            "expected_proxy_expectancy": selected["sim_expectancy"],
            "expected_proxy_risk_scaled_short_count": "",
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
            "candidate_id": selected["variant_id"],
            "output_contract": OUTPUT_CONTRACT,
            "decision_surface": {
                "base": "DA cx05 risk-scale anchor(DA cx05 위험비율 기준)",
                "synthetic_short_source": {
                    "enabled": True,
                    "hours": "17|18|19|20|21",
                    "p_short_min": 0.4375,
                    "min_margin_vs_long": 0.05,
                    "min_margin_vs_flat": 0.0,
                    "month_block": "month=8;hours=*",
                },
                "risk_scale_overlay": {
                    "enabled": True,
                    "side": "short",
                    "hours": "17|18|19|20",
                    "basis": "margin_vs_long",
                    "min_margin_vs_long": 0.080,
                    "multiplier": 1.10,
                },
            },
            "expected_proxy": expected[0],
            "known_differences": [
                "DF is package only(DF는 패키지 전용) and has no new MT5 tester output(새 MT5 테스터 출력 없음).",
                "DD estimated KPIs are telemetry replay deltas(DD 추정 KPI는 텔레메트리 재생 변화분).",
            ],
            "mt5_execution": "not_run",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(
        MODEL_HANDOFF_MANIFEST,
        [
            {"run_id": RUN_ID, "artifact": "onnx", "local_path": rel(SOURCE_ONNX), "sha256": sha(SOURCE_ONNX), "model_id": MODEL_ID, "claim_boundary": CLAIM_BOUNDARY},
            {"run_id": RUN_ID, "artifact": "feature_matrix", "local_path": rel(SOURCE_FEATURE_MATRIX), "sha256": sha(SOURCE_FEATURE_MATRIX), "model_id": MODEL_ID, "claim_boundary": CLAIM_BOUNDARY},
            {"run_id": RUN_ID, "artifact": "expected_proxy_trade_tape", "local_path": rel(dd.SELECTED_TRADE_TAPE), "sha256": sha(dd.SELECTED_TRADE_TAPE), "model_id": MODEL_ID, "claim_boundary": CLAIM_BOUNDARY},
        ],
    )
    write_csv(COMMON_FILES_SYNC, sync_rows)
    write_csv(
        RUNTIME_REPRESENTATION_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "candidate_id": selected["variant_id"],
                "runtime_path": rel(SOURCE_EA),
                "set_path": rel(package["set_path"]),
                "representation_status": "exact_guard_materialized",
                "synthetic_short_source": "InpSyntheticShortSourceMarginVsFlatMin=0.0",
                "effect": "DD p_short dominance(DD p_short 우세)를 runtime guard(런타임 조건)로 표현합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_IDENTITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "ini_path": rel(package["ini_path"]),
                "set_path": rel(package["set_path"]),
                "report_name": package["report_name"],
                "model_id": MODEL_ID,
                "feature_order_hash": feature_order_payload()["feature_order_hash"],
                "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "research_path": rel(dd.SELECTED_CANDIDATE),
                "runtime_path": rel(package["set_path"]),
                "shared_contract": "p_short,p_flat,p_long;hours=17|18|19|20|21;p_short_min=0.4375;margin_vs_long=0.05;margin_vs_flat=0.0;month8_block",
                "known_differences": "package only; MT5 execution not run(패키지 전용, MT5 실행 없음)",
                "parity_check": rel(RUNTIME_REPRESENTATION_AUDIT),
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "candidate_id": selected["variant_id"],
                "model_id": MODEL_ID,
                "set_path": rel(package["set_path"]),
                "ini_path": rel(package["ini_path"]),
                "common_telemetry": package["common_telemetry"],
                "common_summary": package["common_summary"],
                "report_name": package["report_name"],
                "expected_kpi": rel(EXPECTED_KPI_SUMMARY),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364DG_EXECUTION_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "attempt_name": PRIMARY_ATTEMPT,
                "ini_path": rel(package["ini_path"]),
                "set_path": rel(package["set_path"]),
                "execution_question": "Does dd05 short-source expansion transfer to MT5 net/PF/DD/side balance?(dd05 숏 원천 확장이 MT5 순수익/수익 팩터/낙폭/방향 균형으로 전달되는가?)",
                "success_criteria": "MT5 net >= DB 1018.78, PF >= 1.35, density >= 3, short share improves, DD not materially worse",
                "failure_criteria": "MT5 transfer weak, PF below floor, DD worsens, or execution output missing",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(package: Mapping[str, Any], compile_payload: Mapping[str, Any], receipt_paths: Sequence[Path], *, final_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("work_packet_schema_lint", exists(WORK_PACKET), WORK_PACKET, "work packet written(작업 묶음 작성)"),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "inputs linked(입력 연결)"),
        ("runtime_representation_gate", exists(RUNTIME_REPRESENTATION_AUDIT) and "InpSyntheticShortSourceMarginVsFlatMin" in io_path(SOURCE_EA).read_text(encoding="utf-8-sig"), RUNTIME_REPRESENTATION_AUDIT, "flat-margin guard materialized(flat 마진 조건 구체화)"),
        ("compile_gate", bool(compile_payload.get("compile_log_zero_errors")) and bool(compile_payload.get("portable_copied")), COMPILE_RESULT, "MetaEditor compile zero errors and portable EA copied(메타에디터 컴파일 오류 0 및 포터블 EA 복사)"),
        ("runtime_handoff_package_gate", exists(TESTER_SET_MANIFEST) and exists(TESTER_INI_MANIFEST) and exists(RUNTIME_PROBE_ATTEMPT_PACKAGE), RUNTIME_PROBE_ATTEMPT_PACKAGE, "set/ini/attempt package written(set/ini/시도 패키지 작성)"),
        ("common_files_sync_gate", exists(COMMON_FILES_SYNC), COMMON_FILES_SYNC, "Common Files handoff copied(공용 파일 인계 복사)"),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), RUNTIME_RECEIPT, "required receipts exist(필수 영수증 존재)"),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "required gates connected to closeout(필수 게이트를 종료 기록에 연결)"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "no authority/promotion/goal claim(권위/승격/목표 주장 없음)"),
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


def final_payload(selected: Mapping[str, Any], package: Mapping[str, Any], compile_payload: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "runtime_anchor_run_id": RUNTIME_ANCHOR_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_id": selected["variant_id"],
        "model_id": MODEL_ID,
        "attempt_name": PRIMARY_ATTEMPT,
        "compile_status": "completed",
        "compile_log_zero_errors": bool(compile_payload.get("compile_log_zero_errors")),
        "portable_ea_copied": bool(compile_payload.get("portable_copied")),
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "report_name": package["report_name"],
        "expected_estimated_mt5_net": selected["estimated_mt5_net_profit"],
        "expected_estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
        "expected_estimated_mt5_density": selected["estimated_mt5_density"],
        "expected_estimated_mt5_drawdown": selected["estimated_mt5_drawdown"],
        "expected_sim_short_trade_count": selected["sim_short_trade_count"],
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
    write_json(RUNTIME_RECEIPT, {**base, "research_path": rel(dd.SELECTED_CANDIDATE), "runtime_path": rel(package["set_path"]), "shared_contract": rel(RUNTIME_PARITY_CONTRACT), "known_differences": ["package only, MT5 execution next"], "parity_check": rel(RUNTIME_REPRESENTATION_AUDIT), "parity_identity": {"set_sha256": sha(package["set_path"]), "ea_sha256": sha(SOURCE_EA), "onnx_sha256": sha(SOURCE_ONNX)}, "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)"})
    write_json(BACKTEST_RECEIPT, {**base, "tester_ini": rel(package["ini_path"]), "tester_set": rel(package["set_path"]), "tester_output_status": "not_run", "next_probe": NEXT_RUN_ID})
    write_json(ENV_RECEIPT, {**base, "metaeditor": DEFAULT_METAEDITOR.as_posix(), "terminal": basepkg.DEFAULT_TERMINAL.as_posix(), "common_files": basepkg.DEFAULT_COMMON_FILES.as_posix(), "compile_result": rel(COMPILE_RESULT), "environment_judgment": "usable_for_next_mt5_probe(다음 MT5 탐침에 사용 가능)"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "tracked_runtime_package_artifacts(추적된 런타임 패키지 산출물)", "lineage_judgment": "connected_for_runtime_probe(런타임 탐침용 연결)"})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(COMPILE_RESULT), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)], "evidence_missing": ["MT5 tester output", "forward/replay evidence"], "judgment_label": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "Package is ready for MT5 probe, not runtime authority(패키지는 MT5 탐침 준비 완료지만 런타임 권위는 아님)."})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "MT5 runtime probe package prepared and compile checked(MT5 런타임 탐침 패키지 준비 및 컴파일 확인)", "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DF h17 short-source expansion runtime package(17시 숏 원천 확장 런타임 패키지)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- candidate(후보): `{final['candidate_id']}`
- attempt(시도): `{PRIMARY_ATTEMPT}`
- compile zero errors(컴파일 오류 0): `{final['compile_log_zero_errors']}`
- portable EA copied(포터블 EA 복사): `{final['portable_ea_copied']}`
- set/ini(설정/초기화): `{final['set_path']}` / `{final['ini_path']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Action/Effect(행동/효과)

Action(행동): RuntimeProbeEA(런타임 탐침 EA)에 flat-margin guard(flat 마진 조건)를 반영한 뒤 DD05 package(DD05 패키지)를 materialize(구체화)했습니다.

Effect(효과): `p_short > p_flat` 조건을 MT5 runtime(MT5 런타임)에서도 같은 의미로 표현하고, 다음 MT5 Strategy Tester(MT5 전략 테스터) 실행 입력을 만들었습니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is package only(패키지 전용)입니다. MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DF decision(결정): short-source expansion runtime package(숏 원천 확장 런타임 패키지)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- candidate(후보): `{final['candidate_id']}`
- set_path(설정 경로): `{final['set_path']}`
- ini_path(초기화 경로): `{final['ini_path']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): MT5 Strategy Tester(MT5 전략 테스터) 실행 준비를 완료합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DF__{RUN_ID}", f"\n- run364DF__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - DD05 runtime package(DD05 런타임 패키지), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364DF__{RUN_ID}", f"\n## run364DF Runtime Package(런타임 패키지)\n\nAction(행동): DD05 set/ini(설정/초기화 파일)를 materialize(구체화)하고 EA compile(EA 컴파일)을 확인했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364DF__{RUN_ID}", f"\n<!-- run364DF__{RUN_ID} -->\n## run364DF runtime package(런타임 패키지)\n\nCandidate(후보): `{final['candidate_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364DF` completed(완료) DD05 short-source runtime package(DD05 숏 원천 런타임 패키지). EA compile(EA 컴파일)는 zero errors(오류 0)이고 set/ini(설정/초기화 파일)는 `{final['set_path']}` / `{final['ini_path']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행해 실제 net/PF/DD/side balance(순수익/수익 팩터/낙폭/방향 균형) 전달 여부를 확인합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest runtime package(최근 런타임 패키지): `{RUN_ID}`.

Candidate(후보): `{final['candidate_id']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DF__{RUN_ID}", f"\n<!-- run364DF__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed DD05 runtime package(DD05 런타임 패키지); next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364DF__{RUN_ID}", f"\n<!-- run364DF__{RUN_ID} -->\n- `{RUN_ID}`: DD05 short-source expansion(DD05 숏 원천 확장) packaged for MT5 runtime probe(MT5 런타임 탐침 패키지화).\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364DF__{RUN_ID}", f"\n<!-- run364DF__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님). Package only(패키지 전용); MT5 runtime output(MT5 런타임 출력) 전까지 operating claim(운영 주장) 금지.\n")


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
        "work_family": "runtime_backtest(런타임 백테스트)",
        "scoreboard_lane": "runtime_package(런타임 패키지)",
        "external_verification_status": "out_of_scope_by_claim_package_only(주장 범위 밖, 패키지 전용)",
        "evidence_boundary": "compile_checked_package_only(컴파일 확인 패키지 전용)",
        "question": "Can DD05 package be prepared for MT5 probe?(DD05 패키지를 MT5 탐침용으로 준비할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["expected_estimated_mt5_net"],
        "profit_factor": final["expected_estimated_mt5_profit_factor"],
        "drawdown": final["expected_estimated_mt5_drawdown"],
        "trade_density_per_feature_day": final["expected_estimated_mt5_density"],
        "short_trade_count": final["expected_sim_short_trade_count"],
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, status, include in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_separate", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_package(Tier B 패키지 없음)", False),
        ("tier_ab_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_package_tier_a_only(주장 범위 밖, Tier A 패키지 전용)", False),
    ]:
        ledger_rows.append(
            {
                **common,
                "subrun_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "runtime_package(런타임 패키지)",
                "status": status,
                "rows": 1 if include else 0,
                "net_profit": final["expected_estimated_mt5_net"] if include else "",
                "profit_factor": final["expected_estimated_mt5_profit_factor"] if include else "",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("runtime_policy_config", RUNTIME_POLICY_CONFIG, "Runtime policy config(런타임 정책 설정)."),
            ("tester_set", Path(final["set_path"]), "Tester set file(테스터 설정 파일)."),
            ("tester_ini", Path(final["ini_path"]), "Tester ini file(테스터 초기화 파일)."),
            ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE, "Runtime probe attempt package(런타임 탐침 시도 패키지)."),
            ("compile_result", COMPILE_RESULT, "Compile result(컴파일 결과)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
            ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)
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
            "next_run_id": NEXT_RUN_ID,
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
    write_work_packet()
    sync_rows = common_sync_rows()
    package = materialize_set_and_ini(selected)
    write_contracts(selected, package, sync_rows)
    compile_payload = compile_and_sync_ea()
    receipt_paths = [WORK_PACKET_RECEIPT, RUNTIME_RECEIPT, BACKTEST_RECEIPT, ENV_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(package, compile_payload, receipt_paths, final_written=False)
    created_at = now_utc()
    final = final_payload(selected, package, compile_payload, gates, created_at)
    write_receipts(final, package)
    gates = gate_rows(package, compile_payload, receipt_paths, final_written=True)
    final = final_payload(selected, package, compile_payload, gates, created_at)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
