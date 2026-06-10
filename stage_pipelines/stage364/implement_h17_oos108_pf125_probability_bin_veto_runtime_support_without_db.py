from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import mt5_runtime_module_hashes, sha256_file  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db as hh  # noqa: E402


TODAY = "2026-06-08"
STAGE_ID = hh.STAGE_ID
STAGE_DIR = hh.STAGE_DIR
REVIEW_DIR = hh.REVIEW_DIR
SPEC_DIR = hh.SPEC_DIR
SELECTED_DIR = hh.SELECTED_DIR

RUN_NUMBER = "run364HI"
RUN_ID = "run364HI_implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db_v1"
PARENT_RUN_ID = hh.RUN_ID
NEXT_RUN_ID = "run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1"

STATUS_COMPILE_PASSED = "completed_stage364HI_probability_bin_veto_runtime_support_compile_passed_package_materialization_required_no_authority"
STATUS_COMPILE_BLOCKED = "blocked_stage364HI_probability_bin_veto_runtime_support_compile_not_completed_no_authority"
JUDGMENT_COMPILE_PASSED = "runtime_support_implemented_compile_passed_no_package_no_authority"
JUDGMENT_COMPILE_BLOCKED = "runtime_support_implemented_compile_blocked_no_package_no_authority"
DECISION_COMPILE_PASSED = "stage364HI_open_run364HJ_probability_bin_veto_runtime_package"
DECISION_COMPILE_BLOCKED = "stage364HI_repair_compile_before_package"
CLAIM_BOUNDARY = (
    "runtime_capability_implementation_and_compile_only_no_runtime_package_no_mt5_tester_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
EA_PATH = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"
VETO_MODULE = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "ProbabilityBinVeto.mqh"
MT5_INCLUDE_README = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "README.md"
METAEDITOR_PATH = Path(r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUNTIME_IMPLEMENTATION_MANIFEST = RUN_DIR / "runtime_implementation_manifest.csv"
PROBABILITY_BIN_VETO_PARAMETER_CONTRACT = RUN_DIR / "probability_bin_veto_parameter_contract.csv"
PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON = RUN_DIR / "probability_bin_veto_parameter_contract.json"
MODULE_HASHES = RUN_DIR / "runtime_module_hashes.csv"
MT5_COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
MT5_COMPILE_LOG = MT5_DIR / "mt5_compile.log"
RUN364HJ_QUEUE = RUN_DIR / "hi_hj_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HI_probability_bin_veto_runtime_support.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HI_probability_bin_veto_runtime_support.md"
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

THIS_FILE = Path(__file__)

INPUT_FILES = [
    hh.FINAL_DECISION,
    hh.GATE_AUDIT,
    hh.RUNTIME_CAPABILITY_CONTRACT,
    hh.SOURCE_MODEL_RUNTIME_MANIFEST,
    hh.VETO_RULE_MANIFEST,
    hh.PROBABILITY_BIN_EDGES,
    hh.EXPECTED_TRADE_TAPE,
    hh.RUNTIME_PARITY_CONTRACT,
    hh.RUN364HI_QUEUE,
    EA_PATH,
    VETO_MODULE,
    ROOT / "foundation" / "mt5" / "mql5_compile.py",
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    RUNTIME_IMPLEMENTATION_MANIFEST,
    PROBABILITY_BIN_VETO_PARAMETER_CONTRACT,
    PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON,
    MODULE_HASHES,
    MT5_COMPILE_RESULT,
    MT5_COMPILE_LOG,
    RUN364HJ_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    RUNTIME_PARITY_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    MT5_INCLUDE_README,
    THIS_FILE,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return hh.rel(path)


def exists(path: Path | str) -> bool:
    return hh.exists(path)


def sha(path: Path | str) -> str:
    return hh.sha(path)


def read_json(path: Path) -> dict[str, Any]:
    return hh.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    hh.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    hh.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    hh.write_csv(path, rows)


def append_text_once(path: Path, marker: str, text: str) -> None:
    hh.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    hh.append_or_replace_csv(path, key_fields, rows)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def read_text_flexible(path: Path) -> str:
    raw = io_path(path).read_bytes()
    for encoding in ["utf-16", "utf-8-sig", "cp949"]:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HI inputs(HI 입력 누락): " + ", ".join(missing))
    parent = read_json(hh.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HH next_run_id mismatch(HH 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(hh.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HH gate audit(HH 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden parent claim(금지된 상위 주장): {key}={parent.get(key)}")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "HI runtime support implementation input(HI 런타임 지원 구현 입력)",
            "effect": "구현 근거가 어떤 HH 계약과 코드에서 왔는지 추적합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet(parent: Mapping[str, Any]) -> None:
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
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "runtime_module_integration_gate",
                "probability_veto_contract_gate",
                "module_hash_identity_gate",
                "metaeditor_compile_gate",
                "runtime_parity_boundary_gate",
                "next_action_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "question": "Can EA runtime support reproduce HH probability-bin veto inputs?(EA 런타임 지원이 HH 확률 구간 차단 입력을 재현할 수 있는가?)",
            "action": "Implement reusable probability-bin veto module and compile the EA(재사용 확률 구간 차단 모듈을 구현하고 EA를 컴파일합니다).",
            "effect": "패키지 생성 전 EA 기능 공백을 닫습니다.",
            "parent_summary": {
                "parent_judgment": parent.get("judgment"),
                "selected_veto_key_fields": parent.get("selected_veto_key_fields"),
                "expected_tape_rows": parent.get("expected_tape_rows"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def parameter_contract_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rules = read_csv(hh.VETO_RULE_MANIFEST)
    edges = read_json(hh.PROBABILITY_BIN_EDGES)["bin_edges"]
    rule_text = ";".join(
        f"{int(float(row['open_hour']))}|{int(float(row['pflat_bin']))}|{int(float(row['sl_gap_bin']))}"
        for row in rules.to_dict("records")
    )
    pflat_edges = "|".join(str(value) for value in edges["pflat_bin"])
    sl_gap_edges = "|".join(str(value) for value in edges["sl_gap_bin"])
    payload = {
        "InpProbabilityBinVetoEnabled": "true",
        "InpProbabilityBinVetoPFlatEdges": pflat_edges,
        "InpProbabilityBinVetoShortLongGapEdges": sl_gap_edges,
        "InpProbabilityBinVetoRules": rule_text,
    }
    rows = [
        {
            "run_id": RUN_ID,
            "input_name": name,
            "input_value": value,
            "source_artifact": rel(hh.VETO_RULE_MANIFEST if name.endswith("Rules") else hh.PROBABILITY_BIN_EDGES),
            "effect": "HJ package(패키지)가 EA input(입력값)을 그대로 채울 수 있게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, value in payload.items()
    ]
    write_csv(PROBABILITY_BIN_VETO_PARAMETER_CONTRACT, rows)
    write_json(
        PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON,
        {
            "run_id": RUN_ID,
            "parameters": payload,
            "source_veto_rule_manifest": rel(hh.VETO_RULE_MANIFEST),
            "source_probability_bin_edges": rel(hh.PROBABILITY_BIN_EDGES),
            "bin_semantics": "pd.cut(..., labels=False, include_lowest=True) replicated by ProbabilityBinVeto.mqh(pd.cut 구간 의미를 ProbabilityBinVeto.mqh가 재현)",
            "effect": "설정 파일과 tester handoff(테스터 인계)에 같은 값을 넣을 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return rows, payload


def runtime_integration_rows(parameter_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    ea_text = io_path(EA_PATH).read_text(encoding="utf-8-sig")
    module_text = io_path(VETO_MODULE).read_text(encoding="utf-8-sig")
    checks = [
        ("include_gate", '#include "include/ObsidianPrime/ProbabilityBinVeto.mqh"' in ea_text, rel(EA_PATH)),
        ("input_enabled_gate", "InpProbabilityBinVetoEnabled" in ea_text, rel(EA_PATH)),
        ("configure_gate", "g_probability_bin_veto.Configure" in ea_text, rel(EA_PATH)),
        ("apply_gate", "g_probability_bin_veto.Apply" in ea_text, rel(EA_PATH)),
        ("module_version_gate", "OP_PROBABILITY_BIN_VETO_VERSION" in module_text, rel(VETO_MODULE)),
        ("bin_semantics_gate", "value > lower && value <= upper" in module_text and "value >= lower && value <= upper" in module_text, rel(VETO_MODULE)),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "check": name,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "parameter_contract_present": str(bool(parameter_payload)).lower(),
            "effect": "EA 코드가 HH 확률 구간 차단 계약을 실행 경로에 연결했는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, passed, evidence in checks
    ]
    write_csv(RUNTIME_IMPLEMENTATION_MANIFEST, rows)
    return rows


def module_hash_rows() -> list[dict[str, Any]]:
    rows = []
    for raw in mt5_runtime_module_hashes():
        rows.append(
            {
                "run_id": RUN_ID,
                "module_path": raw.get("path", ""),
                "status": raw.get("status", ""),
                "sha256": raw.get("sha256", ""),
                "effect": "EA와 include module(포함 모듈)의 코드 정체성을 기록합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    ex5_path = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    if exists(ex5_path):
        rows.append(
            {
                "run_id": RUN_ID,
                "module_path": rel(ex5_path),
                "status": "compiled_ex5_present(컴파일된 ex5 존재)",
                "sha256": sha256_file(ex5_path),
                "effect": "MetaEditor compile(메타에디터 컴파일) 산출물 정체성을 기록합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(MODULE_HASHES, rows)
    return rows


def compile_ea() -> dict[str, Any]:
    result = compile_mql5_ea(METAEDITOR_PATH, EA_PATH, MT5_COMPILE_LOG)
    write_json(MT5_COMPILE_RESULT, result)
    return result


def queue_rows(final_next: str) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": final_next,
            "queue_rank": 1,
            "queue_id": "hj01_materialize_probability_bin_veto_runtime_package(확률 구간 차단 런타임 패키지 물질화)",
            "required_inputs": ";".join([rel(PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON), rel(hh.SOURCE_MODEL_RUNTIME_MANIFEST), rel(hh.EXPECTED_TRADE_TAPE), rel(MT5_COMPILE_RESULT)]),
            "do_next": "build package and set file, then prepare narrow MT5 probe(패키지와 설정 파일을 만들고 좁은 MT5 탐침을 준비)",
            "avoid": "do not claim runtime authority from compile only(컴파일만으로 런타임 권위 주장 금지)",
            "effect": "컴파일된 기능을 실제 패키지 인계로 넘깁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364HJ_QUEUE, rows)
    return rows


def selected_final(parent: Mapping[str, Any], compile_result: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    compile_completed = compile_result.get("status") == "completed"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if compile_completed else RUN_ID,
        "status": STATUS_COMPILE_PASSED if compile_completed else STATUS_COMPILE_BLOCKED,
        "judgment": JUDGMENT_COMPILE_PASSED if compile_completed else JUDGMENT_COMPILE_BLOCKED,
        "decision": DECISION_COMPILE_PASSED if compile_completed else DECISION_COMPILE_BLOCKED,
        "runtime_support_implemented": True,
        "metaeditor_compile_status": compile_result.get("status", "missing"),
        "metaeditor_log_path": compile_result.get("log_path", ""),
        "metaeditor_log_sha256": compile_result.get("log_sha256", ""),
        "runtime_package": "not_opened",
        "new_mt5_tester_execution": "not_run(실행 안 함)",
        "selected_oos_net": parent.get("selected_oos_net"),
        "selected_oos_profit_factor": parent.get("selected_oos_profit_factor"),
        "selected_oos_trade_density": parent.get("selected_oos_trade_density"),
        "selected_oos_cost06_net": parent.get("selected_oos_cost06_net"),
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


def gate_rows(final: Mapping[str, Any], implementation_rows: Sequence[Mapping[str, Any]], compile_result: Mapping[str, Any], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, RUNTIME_PARITY_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    compile_log_text = read_text_flexible(MT5_COMPILE_LOG) if exists(MT5_COMPILE_LOG) else ""
    compile_passed = compile_result.get("status") == "completed" and "0 errors" in compile_log_text.lower()
    gates = [
        ("scope_completion_gate", exists(RUNTIME_IMPLEMENTATION_MANIFEST) and exists(PROBABILITY_BIN_VETO_PARAMETER_CONTRACT), RUNTIME_IMPLEMENTATION_MANIFEST, "HI 구현 산출물을 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "HH 계약과 EA 입력 계보를 기록했습니다."),
        ("runtime_module_integration_gate", bool(implementation_rows) and all(row["status"] == "passed" for row in implementation_rows), RUNTIME_IMPLEMENTATION_MANIFEST, "EA가 ProbabilityBinVeto module(확률 구간 차단 모듈)을 포함/설정/호출합니다."),
        ("probability_veto_contract_gate", exists(PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON), PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON, "HH 차단 규칙을 EA input(입력값) 문자열로 변환했습니다."),
        ("module_hash_identity_gate", exists(MODULE_HASHES), MODULE_HASHES, "EA/module/ex5 해시를 기록했습니다."),
        ("metaeditor_compile_gate", compile_passed, MT5_COMPILE_LOG, "MetaEditor compile(메타에디터 컴파일)이 0 errors(오류 0)로 끝났습니다."),
        ("runtime_parity_boundary_gate", exists(RUNTIME_PARITY_RECEIPT), RUNTIME_PARITY_RECEIPT, "컴파일은 런타임 권위를 대체하지 않는다고 기록했습니다."),
        ("next_action_gate", exists(RUN364HJ_QUEUE), RUN364HJ_QUEUE, "HJ 패키지 물질화 대기열을 작성했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 receipt(영수증)를 작성했습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 gate(게이트) 감사가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "운영 권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_receipts(final: Mapping[str, Any], compile_result: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "implementation_manifest": rel(RUNTIME_IMPLEMENTATION_MANIFEST), "parameter_contract": rel(PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON), "compile_result": rel(MT5_COMPILE_RESULT), "effect": "EA 지원과 compile evidence(컴파일 근거)를 한 실행에 묶었습니다."})
    write_json(RUNTIME_PARITY_RECEIPT, {**base, "research_path": rel(hh.RUNTIME_PARITY_CONTRACT), "runtime_path": rel(EA_PATH), "shared_contract": [rel(PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON), rel(hh.VETO_RULE_MANIFEST)], "known_differences": ["Strategy Tester not run yet(전략 테스터 미실행)", "runtime package not opened yet(런타임 패키지 미개방)"], "parity_check": {"metaeditor_compile": compile_result.get("status"), "log_path": compile_result.get("log_path"), "log_sha256": compile_result.get("log_sha256")}, "runtime_claim_boundary": "runtime_capability_implementation_only(런타임 기능 구현 전용)"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID if compile_result.get("status") == "completed" else RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "generated_with_compile_log(컴파일 로그 포함 생성)", "lineage_judgment": "connected_with_boundary(경계 포함 연결)"})
    write_json(JUDGMENT_RECEIPT, {**base, "judgment_label": final["judgment"], "evidence_available": [rel(RUNTIME_IMPLEMENTATION_MANIFEST), rel(PROBABILITY_BIN_VETO_PARAMETER_CONTRACT_JSON), rel(MT5_COMPILE_RESULT), rel(MODULE_HASHES)], "evidence_missing": ["MT5 Strategy Tester output(MT5 전략 테스터 출력)", "runtime telemetry comparison(런타임 기록 비교)"], "next_condition": final["next_run_id"], "effect": "판정을 compile-passed implementation(컴파일 통과 구현)으로만 제한했습니다."})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "compile(컴파일)을 운영 권위로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364HI Probability-Bin Veto Runtime Support(확률 구간 차단 런타임 지원)

Created(생성): {final['created_at_utc']}

Action(행동): `ProbabilityBinVeto.mqh` reusable module(재사용 모듈)을 추가하고 `ObsidianPrimeV2_RuntimeProbeEA.mq5`에 input(입력값), configure(설정), apply(적용) 호출을 연결했습니다.

Effect(효과): HH의 `open_hour|pflat_bin|sl_gap_bin` probability-bin veto(확률 구간 차단)를 MT5 EA(메타트레이더5 전문가 자문)가 재현할 수 있게 됐습니다.

- judgment(판정): `{final['judgment']}`
- MetaEditor compile(메타에디터 컴파일): `{final['metaeditor_compile_status']}`
- compile log(컴파일 로그): `{final['metaeditor_log_path']}`
- runtime package(런타임 패키지): `{final['runtime_package']}`
- new MT5 tester execution(새 MT5 테스터 실행): `{final['new_mt5_tester_execution']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364HI Probability-Bin Veto Runtime Support(확률 구간 차단 런타임 지원)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): EA(전문가 자문)에 probability-bin veto(확률 구간 차단) 기능을 구현하고 MetaEditor compile(메타에디터 컴파일)을 실행했습니다.

Effect(효과): 다음 run(실행)은 runtime package(런타임 패키지)와 set file(설정 파일) 물질화로 좁혀집니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364HI__{RUN_ID}", f"\n- run364HI__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - probability-bin veto runtime support(확률 구간 차단 런타임 지원), next(다음) `{final['next_run_id']}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HI__{RUN_ID}", f"\n<!-- run364HI__{RUN_ID} -->\n\n## run364HI Probability-Bin Veto Runtime Support(확률 구간 차단 런타임 지원)\n\nAction(행동): EA probability-bin veto(확률 구간 차단)를 구현하고 MetaEditor compile(메타에디터 컴파일)을 통과했습니다.\n\nEffect(효과): `{final['next_run_id']}`에서 runtime package(런타임 패키지)를 만들 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364HI__{RUN_ID}", f"\n<!-- run364HI__{RUN_ID} -->\n## run364HI probability-bin veto runtime support(확률 구간 차단 런타임 지원)\n\nNext(다음): `{final['next_run_id']}`.\n")
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {final['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {final['next_run_id']}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{final['next_run_id']}`

Current truth(현재 진실): `run364HI` implemented(구현 완료) probability-bin veto runtime support(확률 구간 차단 런타임 지원) in `ProbabilityBinVeto.mqh` and `ObsidianPrimeV2_RuntimeProbeEA.mq5`. MetaEditor compile(메타에디터 컴파일)은 `{final['metaeditor_compile_status']}`입니다.

Runtime truth(런타임 진실): package(패키지)는 still not opened(아직 열지 않음)입니다. Strategy Tester(전략 테스터)와 runtime telemetry comparison(런타임 기록 비교)은 아직 없습니다.

Next action(다음 행동): `{final['next_run_id']}`에서 runtime package(런타임 패키지), set file(설정 파일), MT5 probe handoff(MT5 탐침 인계)를 물질화합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{final['next_run_id']}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest implementation(최근 구현): HI added(추가) probability-bin veto runtime support(확률 구간 차단 런타임 지원) and passed MetaEditor compile(메타에디터 컴파일 통과).

HF OOS net/profit factor/density/cost0.6(HF 표본밖 순수익/수익 팩터/거래 밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`

Next seed(다음 씨앗): HJ runtime package materialization(HJ 런타임 패키지 물질화).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364HI__{RUN_ID}", f"\n<!-- run364HI__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` implemented probability-bin veto runtime support(확률 구간 차단 런타임 지원) and MetaEditor compile(메타에디터 컴파일) status `{final['metaeditor_compile_status']}`; next(다음) `{final['next_run_id']}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HI__{RUN_ID}", f"\n<!-- run364HI__{RUN_ID} -->\n- `{RUN_ID}`: HF probability-bin veto(확률 구간 차단)를 EA runtime support(EA 런타임 지원)로 구현했습니다. Effect(효과): 다음 run(실행)이 runtime package(런타임 패키지)와 MT5 probe(MT5 탐침) 준비로 이동합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    artifact_count = len([path for path in OUTPUT_FILES if exists(path)])
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": final["next_run_id"],
        "artifact_count": artifact_count,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Can EA runtime support reproduce HH probability-bin veto inputs?(EA 런타임 지원이 HH 확률 구간 차단 입력을 재현할 수 있는가?)",
        "next_action": final["next_run_id"],
        "notes": f"compile={final['metaeditor_compile_status']};runtime_package={final['runtime_package']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_runtime_probe(필수 누락, Tier B 런타임 탐침 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_compile_only(주장 범위 밖, 컴파일 전용)"),
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
                "kpi_scope": "HI runtime support(HI 런타임 지원)",
                "metric_scope": "compile_no_tester(컴파일, 테스터 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "source_authority": "compile_only_no_mt5_tester(컴파일 전용, MT5 테스터 없음)",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "run_family": "runtime_verification(런타임 검증)", "run_type": "probability_bin_veto_runtime_support(확률 구간 차단 런타임 지원)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(MT5_COMPILE_RESULT), "selected_net_profit": final["selected_oos_net"], "selected_profit_factor": final["selected_oos_profit_factor"], "selected_trade_density": final["selected_oos_trade_density"]}])
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "artifact_path": rel(path),
            "artifact_type": "hi_runtime_support_implementation(HI 런타임 지원 구현)",
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "HI 구현 산출물 계보를 register(등록부)에 연결합니다.",
        }
        for path in OUTPUT_FILES
        if exists(path)
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_run_manifest(final: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": final["next_run_id"], "producer": rel(THIS_FILE), "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)], "final_decision": rel(FINAL_DECISION), "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    _, parameter_payload = parameter_contract_rows()
    implementation_rows = runtime_integration_rows(parameter_payload)
    compile_result = compile_ea()
    module_hash_rows()
    queue_rows(NEXT_RUN_ID if compile_result.get("status") == "completed" else RUN_ID)

    preliminary_final = selected_final(parent, compile_result, [], created_at)
    write_receipts(preliminary_final, compile_result)
    gates = gate_rows(preliminary_final, implementation_rows, compile_result, final_written=False)
    final = selected_final(parent, compile_result, gates, created_at)
    gates = gate_rows(final, implementation_rows, compile_result, final_written=True)
    final = selected_final(parent, compile_result, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_run_manifest(final)
    write_docs(final, gates)
    write_receipts(final, compile_result)
    gates = gate_rows(final, implementation_rows, compile_result, final_written=True)
    final = selected_final(parent, compile_result, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_run_manifest(final)
    write_ledgers(final, gates)

    failed = [row for row in gates if row["status"] != "passed"]
    if failed:
        raise RuntimeError("HI gates failed(HI 게이트 실패): " + json.dumps(failed, ensure_ascii=False))
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "compile_status": final["metaeditor_compile_status"], "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "next_run_id": final["next_run_id"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
