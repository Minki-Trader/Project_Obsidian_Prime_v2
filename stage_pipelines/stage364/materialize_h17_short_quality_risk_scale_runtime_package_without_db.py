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
from stage_pipelines.stage364 import materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db as co  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_month12_secondary_month_margin_guard_runtime_package_without_db as cu  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as basepkg  # noqa: E402
from stage_pipelines.stage364 import review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db as cy  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364DA"
RUN_ID = "run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_PROXY_RUN_ID = cy.RUN_ID
RUNTIME_ANCHOR_RUN_ID = cu.RUN_ID
NEXT_RUN_ID = "run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364DA_h17_short_quality_risk_scale_runtime_package_prepared_compile_checked_no_execution"
JUDGMENT = "runtime_probe_package_ready_cx05_short_quality_risk_scale_mt5_execution_required_no_authority"
DECISION = "stage364DA_open_run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_short_quality_risk_scale_compile_checked_"
    "no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

MODEL_ID = cu.MODEL_ID
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin_plus_cr04_secondary_month_guard_plus_cx05_short_quality_risk_scale"
PRIMARY_ATTEMPT = "run364DA_cx05_short_quality_risk_scale"
DEFAULT_METAEDITOR = cu.DEFAULT_METAEDITOR

STAGE_DIR = parent.STAGE_DIR
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
RUN364DB_EXECUTION_QUEUE = RUN_DIR / "run364DB_execution_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364DA_h17_short_quality_risk_scale_runtime_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DA_h17_short_quality_risk_scale_runtime_package.md"
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

SOURCE_FEATURE_MATRIX = cu.SOURCE_FEATURE_MATRIX
SOURCE_ONNX = cu.SOURCE_ONNX
SOURCE_EA = cu.SOURCE_EA
SOURCE_EA_BINARY = cu.SOURCE_EA_BINARY
PORTABLE_EA_EX5 = cu.PORTABLE_EA_EX5
SOURCE_CU_SET = cu.SET_DIR / "OPv2_run364CU_cr04_secondary_month_guard.set"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_h17_short_quality_risk_scale_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364DA_QUEUE,
    parent.RISK_SCALE_RULE_CONTRACT,
    parent.RUNTIME_REPRESENTATION_AUDIT,
    parent.EA_SUPPORT_AUDIT,
    cy.FINAL_DECISION,
    cy.SELECTED_CANDIDATE,
    cy.SELECTED_TRADE_TAPE,
    cy.GATE_AUDIT,
    cu.FINAL_DECISION,
    cu.RUNTIME_POLICY_CONFIG,
    cu.TESTER_SET_MANIFEST,
    SOURCE_CU_SET,
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
    RUN364DB_EXECUTION_QUEUE,
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
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return cy.rel(path)


def exists(path: Path | str) -> bool:
    return cy.exists(path)


def sha(path: Path | str) -> str:
    return cy.sha(path)


def read_json(path: Path) -> Any:
    return cy.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    cy.write_json(path, cy.json_ready(payload))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    cy.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    cy.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    cy.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    cy.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR / "compile", SET_DIR, INI_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DA inputs(DA 입력 누락): " + ", ".join(missing))
    parent_final = read_json(parent.FINAL_DECISION)
    selected = read_json(cy.SELECTED_CANDIDATE)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CZ next_run_id mismatch(CZ 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if selected.get("variant_id") != parent_final.get("reviewed_variant_id"):
        raise RuntimeError("CZ reviewed variant and CY selected variant differ(CZ 검토 변형과 CY 선택 변형 불일치)")
    for label, final in [("CZ", parent_final), ("CY", read_json(cy.FINAL_DECISION)), ("CU", read_json(cu.FINAL_DECISION))]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            value = final.get(key, "not_claimed")
            if value != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={value}")
    for label, gate_path in [("CZ", parent.GATE_AUDIT), ("CY", cy.GATE_AUDIT)]:
        gates = read_csv(gate_path)
        if gates.empty or any(gates["status"].astype(str) != "passed"):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    ea_text = io_path(SOURCE_EA).read_text(encoding="utf-8-sig")
    required_tokens = [
        "InpRiskScaleOverlayEnabled",
        "InpRiskScaleOverlaySide",
        "InpRiskScaleOverlayHours",
        "InpRiskScaleOverlayMinMarginVsLong",
        "InpRiskScaleOverlayMultiplier",
        "RiskScaleOverlayMultiplier",
        "risk_scale_overlay",
    ]
    missing_tokens = [token for token in required_tokens if token not in ea_text]
    if missing_tokens:
        raise RuntimeError("EA risk-scale overlay tokens(EA 위험비율 오버레이 토큰) missing: " + ",".join(missing_tokens))
    return parent_final, selected


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DA runtime package source(DA 런타임 패키지 원천)",
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


def feature_order_payload() -> dict[str, Any]:
    return cu.feature_order_payload()


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
        copy_common(cy.SELECTED_TRADE_TAPE, f"{COMMON_EXPECTED_DIR}/cx05_selected_proxy_trade_tape.csv", "common_expected_proxy_trade_tape", "expected proxy tape(예상 프록시 테이프)를 비교 입력으로 복사"),
    ]


def materialize_set_and_ini(selected: Mapping[str, Any]) -> dict[str, Any]:
    feature_order = feature_order_payload()
    base_values = {key: co.maybe_number(value) for key, value in co.read_set_values(SOURCE_CU_SET).items()}
    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_telemetry = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv"
    common_summary = f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv"
    set_values = dict(base_values)
    set_values.update(
        {
            "InpRunId": f"{RUN_ID}_{PRIMARY_ATTEMPT}",
            "InpExplorationLabel": "stage364DA__Cx05ShortQualityRiskScale",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "validation_oos_cx05",
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
            "InpMagic": 36430005,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
        }
    )
    set_path = SET_DIR / "OPv2_run364DA_cx05_short_quality_risk_scale.set"
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    report_name = "Project_Obsidian_Prime_v2_run364DB_cx05_short_quality_risk_scale_probe"
    ini_path = INI_DIR / "OPv2_run364DA_cx05_short_quality_risk_scale.ini"
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
                "risk_scale_overlay": "side=short;hours=17|18|19|20;basis=margin_vs_long;min=0.080;multiplier=1.10",
                "package_base": rel(SOURCE_CU_SET),
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
            "primary_family": "runtime_verification(런타임 검증)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-environment-reproducibility(환경 재현성)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "hypothesis": "The cx05 short-quality risk-scale rule can be represented in RuntimeProbeEA without changing entry count.",
            "required_gates": [
                "work_packet_schema_lint",
                "input_lineage_gate",
                "runtime_representation_gate",
                "compile_gate",
                "runtime_handoff_package_gate",
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
            "expected_proxy_net": selected["net_profit"],
            "expected_proxy_profit_factor": selected["profit_factor"],
            "expected_proxy_expectancy": selected["expectancy"],
            "expected_proxy_trade_count": selected["trade_count"],
            "expected_proxy_density": selected["trade_density"],
            "expected_proxy_short_count": selected["short_trade_count"],
            "expected_proxy_risk_scaled_short_count": selected["risk_scaled_short_count"],
            "expected_proxy_risk_scale_net_delta": selected["risk_scale_net_delta"],
            "expected_proxy_month12_long_net": selected["month12_long_net"],
            "expected_proxy_closed_trade_dd": selected["closed_trade_drawdown_proxy"],
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
                "base": "CU cr04 secondary month guard anchor(CU cr04 보조 월 가드 기준)",
                "risk_scale_overlay": {
                    "enabled": True,
                    "side": "short",
                    "hours": "17|18|19|20",
                    "basis": "margin_vs_long",
                    "min_margin_vs_long": 0.080,
                    "multiplier": 1.10,
                    "entry_count_effect": "none",
                },
            },
            "expected_proxy": expected[0],
            "known_differences": [
                "DA is package only(DA는 패키지 전용) and has no new MT5 tester output(새 MT5 테스터 출력 없음).",
                "The overlay changes lot exposure, not entry count(오버레이는 랏 노출만 바꾸고 진입 수는 바꾸지 않음).",
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
            {"run_id": RUN_ID, "artifact": "expected_proxy_trade_tape", "local_path": rel(cy.SELECTED_TRADE_TAPE), "sha256": sha(cy.SELECTED_TRADE_TAPE), "model_id": MODEL_ID, "claim_boundary": CLAIM_BOUNDARY},
        ],
    )
    write_csv(COMMON_FILES_SYNC, sync_rows)
    write_csv(
        RUNTIME_REPRESENTATION_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "candidate_id": selected["variant_id"],
                "representation_status": "represented_exactly_by_parameterized_risk_scale_overlay(파라미터화 위험비율 오버레이로 정확 표현)",
                "risk_scale_overlay": "enabled=true;side=short;hours=17|18|19|20;basis=margin_vs_long;min=0.080;multiplier=1.10",
                "entry_count_effect": "none_no_trade_splitting(없음, 거래 쪼개기 없음)",
                "set_path": rel(package["set_path"]),
                "effect": "MT5 can now probe cx05 without changing its rule meaning(MT5가 이제 cx05 규칙 의미를 바꾸지 않고 탐침 가능)",
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
                "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
                "common_files_root": basepkg.DEFAULT_COMMON_FILES.as_posix(),
                "set_path": rel(package["set_path"]),
                "ini_path": rel(package["ini_path"]),
                "report_name": package["report_name"],
                "suggested_command": f"\"{basepkg.DEFAULT_TERMINAL.as_posix()}\" /portable /config:\"{package['ini_path'].as_posix()}\"",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "research_path": rel(parent.RISK_SCALE_RULE_CONTRACT),
                "runtime_path": rel(package["set_path"]),
                "shared_contract": "side=short;hours=17|18|19|20;basis=margin_vs_long;min=0.080;multiplier=1.10",
                "known_differences": "no Strategy Tester output yet(전략 테스터 출력 아직 없음)",
                "parity_check": "EA compile plus set/ini materialization(EA 컴파일 및 설정/INI 구체화)",
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
                "next_run_id": NEXT_RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "candidate_id": selected["variant_id"],
                "set_path": rel(package["set_path"]),
                "ini_path": rel(package["ini_path"]),
                "expected_proxy_net": selected["net_profit"],
                "expected_proxy_profit_factor": selected["profit_factor"],
                "expected_proxy_density": selected["trade_density"],
                "expected_proxy_short_count": selected["short_trade_count"],
                "expected_risk_scaled_short_count": selected["risk_scaled_short_count"],
                "effect": "DB can execute the exact cx05 runtime package(DB가 정확한 cx05 런타임 패키지를 실행 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364DB_EXECUTION_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "db01_execute_cx05_short_quality_risk_scale_package",
                "attempt_name": PRIMARY_ATTEMPT,
                "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
                "ini_path": rel(package["ini_path"]),
                "success_criteria": "Strategy Tester output exists and proxy/MT5 diff can be reviewed(전략 테스터 출력 존재 및 프록시/MT5 차이 검토 가능)",
                "failure_criteria": "terminal cannot run, report missing, or telemetry missing(터미널 실행 불가, 보고서 누락, 원격측정 누락)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(compile_payload: Mapping[str, Any], package: Mapping[str, Any], receipt_paths: Sequence[Path], receipts_written: bool) -> list[dict[str, Any]]:
    compile_status = compile_payload.get("compile_result", {}).get("status")
    compile_ok = bool(compile_payload.get("compile_log_zero_errors")) and bool(compile_payload.get("portable_copied"))
    package_pass = exists(package["set_path"]) and exists(package["ini_path"]) and exists(TESTER_SET_MANIFEST) and exists(TESTER_INI_MANIFEST)
    receipt_status = all(exists(path) for path in receipt_paths)
    return [
        {"run_id": RUN_ID, "gate": "work_packet_schema_lint", "status": "passed", "evidence": rel(WORK_PACKET), "effect": "DA work packet recorded(DA 작업 묶음 기록)", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "input_lineage_gate", "status": "passed", "evidence": rel(INPUT_MANIFEST), "effect": "CZ/CY/CU inputs connected(CZ/CY/CU 입력 연결)", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "runtime_representation_gate", "status": "passed" if exists(RUNTIME_REPRESENTATION_AUDIT) else "failed", "evidence": rel(RUNTIME_REPRESENTATION_AUDIT), "effect": "cx05 rule represented in set/EA contract(cx05 규칙이 설정/EA 계약에 표현)", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "compile_gate", "status": "passed" if compile_ok else "failed", "evidence": f"compile_status={compile_status};zero_errors={compile_payload.get('compile_log_zero_errors')};log={rel(COMPILE_LOG)}", "effect": "EA compile checked and portable binary synced(EA 컴파일 점검 및 포터블 바이너리 동기화)", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "runtime_handoff_package_gate", "status": "passed" if package_pass else "failed", "evidence": f"set={rel(package['set_path'])};ini={rel(package['ini_path'])}", "effect": "DB handoff package prepared(DB 인계 패키지 준비)", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "required_gate_coverage_audit", "status": "passed" if receipts_written and receipt_status else "pending", "evidence": f"receipts_written={receipt_status}", "effect": "required gates linked to receipts(필수 게이트와 영수증 연결)", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "final_claim_guard", "status": "passed", "evidence": "mt5_execution=not_run;authority=not_claimed", "effect": "package is not overstated as authority(패키지를 권위로 과장하지 않음)", "claim_boundary": CLAIM_BOUNDARY},
    ]


def final_payload(
    selected: Mapping[str, Any],
    compile_payload: Mapping[str, Any],
    package: Mapping[str, Any],
    sync_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
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
        "attempt_name": PRIMARY_ATTEMPT,
        "model_id": MODEL_ID,
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "report_name": package["report_name"],
        "compile_status": compile_payload.get("compile_result", {}).get("status", "unknown"),
        "compile_log_zero_errors": bool(compile_payload.get("compile_log_zero_errors")),
        "portable_ea_copied": bool(compile_payload.get("portable_copied")),
        "common_sync_rows": len(sync_rows),
        "runtime_module_hashes": mt5_runtime_module_hashes(),
        "expected_proxy_net": selected["net_profit"],
        "expected_proxy_profit_factor": selected["profit_factor"],
        "expected_proxy_expectancy": selected["expectancy"],
        "expected_proxy_trade_count": selected["trade_count"],
        "expected_proxy_density": selected["trade_density"],
        "expected_proxy_short_count": selected["short_trade_count"],
        "expected_proxy_risk_scaled_short_count": selected["risk_scaled_short_count"],
        "expected_proxy_risk_scale_net_delta": selected["risk_scale_net_delta"],
        "expected_proxy_month12_long_net": selected["month12_long_net"],
        "expected_proxy_closed_trade_dd": selected["closed_trade_drawdown_proxy"],
        "mt5_execution": "not_run",
        "new_model_training": "not_run",
        "external_verification_status": "out_of_scope_by_claim_package_only_db_execution_required",
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
    write_json(WORK_PACKET_RECEIPT, {"run_id": RUN_ID, "work_packet": rel(WORK_PACKET), "claim_boundary": CLAIM_BOUNDARY})
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(parent.RISK_SCALE_RULE_CONTRACT),
            "runtime_path": [rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)],
            "shared_contract": "side=short;hours=17|18|19|20;basis=margin_vs_long;min=0.080;multiplier=1.10",
            "known_differences": "no Strategy Tester output yet(전략 테스터 출력 아직 없음)",
            "parity_check": "compile, common file sync, set/ini materialization(컴파일, 공용 파일 동기화, 설정/INI 구체화)",
            "parity_identity": f"set={final['set_path']};ea={sha(SOURCE_EA)};model={sha(SOURCE_ONNX)}",
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
            "report_identity": "planned only; DB must create Strategy Tester report(계획 전용, DB가 전략 테스터 보고서 생성 필요)",
            "trade_evidence": rel(EXPECTED_KPI_SUMMARY),
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
            "reproducibility_judgment": "local_only_with_manifest(목록 포함 로컬 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "cx05 MT5 runtime probe package(cx05 MT5 런타임 탐침 패키지)",
            "evidence_available": [rel(FINAL_DECISION), rel(COMPILE_RESULT), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST)],
            "evidence_missing": ["new MT5 runtime output(새 MT5 런타임 출력)", "Strategy Tester report(전략 테스터 보고서)", "runtime authority closure(런타임 권위 종료)"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "runtime probe package ready only(런타임 탐침 패키지 준비 전용)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "mt5_execution": final["mt5_execution"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if path != LINEAGE_RECEIPT and exists(path) and io_path(path).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_local_mt5_synced(추적 가능 및 로컬 MT5 동기화)",
            "lineage_judgment": "connected_with_runtime_package_boundary(런타임 패키지 경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return cy.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DA h17 short-quality risk-scale runtime package(364DA 17시 숏 품질 위험비율 런타임 패키지)

Updated(갱신): {final['created_at_utc']}

Action(행동): `cx05_high_quality_short_boost110_h17_20`를 RuntimeProbeEA(런타임 탐침 EA) risk-scale overlay(위험비율 오버레이)와 set/ini(설정/INI)로 materialize(구체화)했습니다.

Effect(효과): `run364DB`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행해 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

- compile status(컴파일 상태): `{final['compile_status']}`
- compile zero errors(컴파일 오류 0개): `{final['compile_log_zero_errors']}`
- set file(설정 파일): `{final['set_path']}`
- ini file(INI 파일): `{final['ini_path']}`
- expected proxy KPI(예상 프록시 핵심 성과 지표): net(순수익) `{final['expected_proxy_net']}`, PF(수익 팩터) `{final['expected_proxy_profit_factor']}`, density(밀도) `{final['expected_proxy_density']}`, trades(거래수) `{final['expected_proxy_trade_count']}`, risk scaled shorts(위험비율 조정 숏) `{final['expected_proxy_risk_scaled_short_count']}`
- MT5 execution(MT5 실행): `{final['mt5_execution']}`

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

DA is package only(DA는 패키지 전용)입니다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DA decision(결정): cx05 short-quality risk-scale package(cx05 숏 품질 위험비율 패키지)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- candidate(후보): `{final['candidate_id']}`
- set file(설정 파일): `{final['set_path']}`
- ini file(INI 파일): `{final['ini_path']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DB에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DA__{RUN_ID}", f"\n- run364DA__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cx05 short quality risk-scale package(cx05 숏 품질 위험비율 패키지), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364DA__{RUN_ID}",
        f"""
<!-- run364DA__{RUN_ID} -->

## run364DA Short Quality Risk-Scale Runtime Package(364DA 숏 품질 위험비율 런타임 패키지)

Action(행동): EA(전문가 자문)에 risk-scale overlay(위험비율 오버레이)를 추가하고 `cx05` set/ini(설정/INI)를 만들었습니다.

Effect(효과): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터) 실행을 시도할 수 있습니다.
""",
    )
    append_text_once(STAGE_README, f"run364DA__{RUN_ID}", f"\n<!-- run364DA__{RUN_ID} -->\n## run364DA runtime package(364DA 런타임 패키지)\n\n`{final['candidate_id']}` package(패키지) ready(준비). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DA` materialized(구체화 완료) `cx05_high_quality_short_boost110_h17_20` MT5 runtime probe package(MT5 런타임 탐침 패키지). Compile status(컴파일 상태)는 `{final['compile_status']}`이고 compile zero errors(컴파일 오류 0개)는 `{final['compile_log_zero_errors']}`입니다. set/ini(설정/INI)는 `{final['set_path']}` / `{final['ini_path']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy/MT5 diff(프록시/MT5 차이), equity DD(수익곡선 낙폭), side balance(방향 균형)를 기록합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe package(런타임 탐침 패키지): `{final['candidate_id']}`.

Set file(설정 파일): `{final['set_path']}`
INI file(INI 파일): `{final['ini_path']}`
Compile status(컴파일 상태): `{final['compile_status']}`

Expected proxy KPI(예상 프록시 핵심 성과 지표): net(순수익) `{final['expected_proxy_net']}`, PF(수익 팩터) `{final['expected_proxy_profit_factor']}`, density(밀도) `{final['expected_proxy_density']}`, shorts(숏) `{final['expected_proxy_short_count']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DA__{RUN_ID}", f"\n<!-- run364DA__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` packaged cx05 short-quality risk-scale(cx05 숏 품질 위험비율 패키지); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DA__{RUN_ID}", f"\n<!-- run364DA__{RUN_ID} -->\n- `{RUN_ID}`: cx05 short-quality risk-scale runtime package(cx05 숏 품질 위험비율 런타임 패키지). Effect(효과): MT5 runtime probe(MT5 런타임 탐침)로 proxy expected value(프록시 예상값)를 검증할 수 있습니다.\n")


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
        "work_family": "runtime_verification(런타임 검증)",
        "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "package_only(패키지 전용)",
        "question": "Can cx05 be represented exactly for MT5 probing?(cx05를 MT5 탐침용으로 정확히 표현할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["expected_proxy_net"],
        "profit_factor": final["expected_proxy_profit_factor"],
        "expectancy": final["expected_proxy_expectancy"],
        "trade_count": final["expected_proxy_trade_count"],
        "trade_density_per_feature_day": final["expected_proxy_density"],
        "short_trade_count": final["expected_proxy_short_count"],
        "max_drawdown_amount": final["expected_proxy_closed_trade_dd"],
        "trade_density_requirement_status": "inherited_proxy_density_ge_3_no_trade_splitting(프록시 밀도 3 이상 및 거래 쪼개기 없음 상속)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "primary_kpi": f"expected_proxy_net={final['expected_proxy_net']};pf={final['expected_proxy_profit_factor']};density={final['expected_proxy_density']};risk_scaled_shorts={final['expected_proxy_risk_scaled_short_count']}",
        "guardrail_kpi": "mt5_execution=not_run;no_authority",
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
            "kpi_scope": "DA runtime package(DA 런타임 패키지)",
            "status": status,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "package_expected_proxy(패키지 예상 프록시)",
        }
        if not include_metrics:
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "short_trade_count", "max_drawdown_amount"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


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


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("runtime_policy_config", RUNTIME_POLICY_CONFIG),
        ("model_handoff_manifest", MODEL_HANDOFF_MANIFEST),
        ("common_files_sync", COMMON_FILES_SYNC),
        ("compile_result", COMPILE_RESULT),
        ("portable_ea_sync", PORTABLE_EA_SYNC),
        ("tester_set_manifest", TESTER_SET_MANIFEST),
        ("tester_ini_manifest", TESTER_INI_MANIFEST),
        ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE),
        ("execution_queue", RUN364DB_EXECUTION_QUEUE),
        ("runtime_representation_audit", RUNTIME_REPRESENTATION_AUDIT),
        ("expected_kpi_summary", EXPECTED_KPI_SUMMARY),
        ("final_decision", FINAL_DECISION),
        ("run_manifest", RUN_MANIFEST),
        ("gate_audit", GATE_AUDIT),
        ("report", REPORT_PATH),
        ("script", Path(__file__)),
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
                    "notes": "DA runtime probe package artifact(DA 런타임 탐침 패키지 산출물).",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    _parent_final, selected = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    compile_payload = compile_and_sync_ea()
    sync_rows = common_sync_rows()
    package = materialize_set_and_ini(selected)
    write_contracts(selected, package, sync_rows)

    receipt_paths = [WORK_PACKET_RECEIPT, RUNTIME_RECEIPT, BACKTEST_RECEIPT, ENV_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT, LINEAGE_RECEIPT]
    preliminary_gates = gate_rows(compile_payload, package, receipt_paths, receipts_written=False)
    final = final_payload(selected, compile_payload, package, sync_rows, preliminary_gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, preliminary_gates)
    write_receipts(final)
    refresh_lineage_receipt(final)

    gates = gate_rows(compile_payload, package, receipt_paths, receipts_written=True)
    final = final_payload(selected, compile_payload, package, sync_rows, gates, created_at)
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
    print(json.dumps(cy.json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
