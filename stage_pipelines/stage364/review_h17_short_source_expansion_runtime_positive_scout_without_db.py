import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_quality_risk_scale_runtime_package_without_db as da  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_expansion_runtime_positive_scout_without_db as dd  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dd.STAGE_ID
RUN_NUMBER = "run364DE"
RUN_ID = "run364DE_review_h17_short_source_expansion_runtime_positive_scout_without_db_v1"
PARENT_RUN_ID = dd.RUN_ID
PACKAGE_ANCHOR_RUN_ID = da.RUN_ID
NEXT_RUN_ID = "run364DF_implement_h17_short_source_expansion_runtime_package_without_db_v1"

STATUS = "completed_stage364DE_h17_short_source_expansion_review_runtime_representation_repair_required_no_authority"
JUDGMENT = "positive_proxy_short_source_candidate_runtime_flat_margin_guard_required_no_authority"
DECISION = "stage364DE_open_run364DF_short_source_expansion_runtime_package_repair"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_"
    "runtime_representation_repair_required_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = dd.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
SELECTED_CANDIDATE_REVIEW = RUN_DIR / "selected_candidate_review.csv"
RUNTIME_REPRESENTATION_AUDIT = RUN_DIR / "runtime_representation_audit.csv"
EA_SUPPORT_AUDIT = RUN_DIR / "ea_support_audit.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
SHORT_SOURCE_RULE_CONTRACT = RUN_DIR / "short_source_rule_contract.csv"
PROXY_MT5_BOUNDARY_REVIEW = RUN_DIR / "proxy_mt5_boundary_review.csv"
RUN364DF_QUEUE = RUN_DIR / "run364DF_runtime_package_queue.csv"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DE_h17_short_source_expansion_runtime_positive_scout_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DE_h17_short_source_expansion_runtime_positive_scout_review.md"
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

EA_PATH = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"
DA_SET_PATH = da.SET_DIR / "OPv2_run364DA_cx05_short_quality_risk_scale.set"

INPUT_FILES = [
    dd.FINAL_DECISION,
    dd.GATE_AUDIT,
    dd.SELECTED_CANDIDATE,
    dd.SHORT_SOURCE_SURFACE,
    dd.SELECTED_TRADE_TAPE,
    dd.BASELINE_REPLAY_GAP,
    dd.DATA_INTEGRITY_AUDIT,
    dd.RUN364DE_QUEUE,
    dd.RUN_MANIFEST,
    da.FINAL_DECISION,
    da.RUNTIME_POLICY_CONFIG,
    DA_SET_PATH,
    EA_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SELECTED_CANDIDATE_REVIEW,
    RUNTIME_REPRESENTATION_AUDIT,
    EA_SUPPORT_AUDIT,
    PACKAGE_DECISION,
    SHORT_SOURCE_RULE_CONTRACT,
    PROXY_MT5_BOUNDARY_REVIEW,
    RUN364DF_QUEUE,
    RUNTIME_RECEIPT,
    DATA_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
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


def as_float(value: Any, default: float = 0.0) -> float:
    return dd.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return dd.finite(value, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DE inputs(DE 입력 누락): " + ", ".join(missing))
    dd_final = read_json(dd.FINAL_DECISION)
    da_final = read_json(da.FINAL_DECISION)
    if dd_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DD next_run_id mismatch(DD 다음 실행 ID 불일치): {dd_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("DD", dd_final), ("DA", da_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    gates = read_csv(dd.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DD gate audit(DD 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return dd_final, da_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DE runtime representation review source(DE 런타임 표현 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


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
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-result-judgment(옵시디언 결과 판정)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "hypothesis": "DD short-source candidate can be represented as parameterized RuntimeProbeEA package after exact guard review.",
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "selected_candidate_review_gate",
                "runtime_representation_gate",
                "no_trade_splitting_boundary_gate",
                "proxy_mt5_boundary_gate",
                "package_decision_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def set_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def review_runtime_support(selected: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str]:
    ea_text = io_path(EA_PATH).read_text(encoding="utf-8-sig")
    values = set_values(DA_SET_PATH)
    required = {
        "hours": "17|18|19|20|21",
        "p_short_min": 0.4375,
        "margin_vs_long_min": 0.05,
        "margin_vs_flat_min": 0.0,
        "month_block": "month=8;hours=*",
        "risk_scale_hours": "17|18|19|20",
        "risk_scale_margin_vs_long_min": 0.08,
        "max_hold_bars": 6,
    }
    support_checks = [
        ("synthetic_short_enabled_param", "InpSyntheticShortSourceEnabled" in ea_text, "EA has synthetic short enable parameter(EA에 합성 숏 활성 매개변수 있음)"),
        ("synthetic_short_hours_param", "InpSyntheticShortSourceHours" in ea_text, "EA has synthetic short hour list(EA에 합성 숏 시간 목록 있음)"),
        ("synthetic_short_pshort_param", "InpSyntheticShortSourcePShortMin" in ea_text, "EA has p_short minimum guard(EA에 p_short 최소 조건 있음)"),
        ("synthetic_short_margin_long_param", "InpSyntheticShortSourceMarginVsLongMin" in ea_text, "EA has margin_vs_long guard(EA에 margin_vs_long 조건 있음)"),
        ("synthetic_short_month_block_param", "InpSyntheticShortMonthBlockEnabled" in ea_text and "synthetic_short_month_block" in ea_text, "EA has month block for synthetic shorts(EA에 합성 숏 월 차단 있음)"),
        ("synthetic_short_margin_flat_param", "InpSyntheticShortSourceMarginVsFlatMin" in ea_text, "EA has margin_vs_flat guard for p_short dominance(EA에 p_short 우세용 margin_vs_flat 조건 있음)"),
        ("risk_scale_overlay_param", "InpRiskScaleOverlayEnabled" in ea_text and "RiskScaleOverlayMultiplier" in ea_text, "EA has risk-scale overlay(EA에 위험비율 오버레이 있음)"),
    ]
    ea_rows = [
        {
            "run_id": RUN_ID,
            "check_id": check_id,
            "status": "passed" if passed else "missing",
            "evidence": rel(EA_PATH),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for check_id, passed, effect in support_checks
    ]
    set_rows = [
        {
            "run_id": RUN_ID,
            "parameter": key,
            "current_da_value": values.get(key, ""),
            "required_dd_value": required_value,
            "status": "matched" if str(values.get(key, "")) == str(required_value) else "needs_update",
            "effect": "DD package(DD 패키지)에서 set file(설정 파일) 값을 바꿔야 하는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for key, required_value in [
            ("InpSyntheticShortSourceEnabled", "true"),
            ("InpSyntheticShortSourceHours", required["hours"]),
            ("InpSyntheticShortSourcePShortMin", required["p_short_min"]),
            ("InpSyntheticShortSourceMarginVsLongMin", required["margin_vs_long_min"]),
            ("InpSyntheticShortSourceMarginVsFlatMin", required["margin_vs_flat_min"]),
            ("InpSyntheticShortMonthBlockEnabled", "true"),
            ("InpSyntheticShortMonthBlockMonth", "8"),
            ("InpSyntheticShortMonthBlockHours", "*"),
            ("InpRiskScaleOverlayEnabled", "true"),
            ("InpRiskScaleOverlayHours", required["risk_scale_hours"]),
            ("InpRiskScaleOverlayMinMarginVsLong", required["risk_scale_margin_vs_long_min"]),
            ("InpMaxHoldBars", required["max_hold_bars"]),
        ]
    ]
    exact_supported = all(row["status"] == "passed" for row in ea_rows if row["check_id"] != "synthetic_short_margin_flat_param")
    flat_guard_supported = any(row["check_id"] == "synthetic_short_margin_flat_param" and row["status"] == "passed" for row in ea_rows)
    runtime_status = "exact_supported_parameter_only" if exact_supported and flat_guard_supported else "repair_required_add_margin_vs_flat_guard"
    rule_rows = [
        {
            "run_id": RUN_ID,
            "candidate_id": selected["variant_id"],
            "rule_component": "synthetic_short_source(합성 숏 원천)",
            "required_contract": "hours=17|18|19|20|21;p_short>=0.4375;margin_vs_long>=0.05;p_short>p_flat;month8 blocked",
            "runtime_mapping": "InpSyntheticShortSource* plus month block(InpSyntheticShortSource* 및 월 차단)",
            "support_status": runtime_status,
            "effect": "proxy rule(프록시 규칙)을 RuntimeProbeEA(런타임 탐침 EA) 의미로 매핑합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "candidate_id": selected["variant_id"],
            "rule_component": "risk_scale_overlay(위험비율 오버레이)",
            "required_contract": "short hours 17|18|19|20 margin_vs_long>=0.08 multiplier=1.10",
            "runtime_mapping": "InpRiskScaleOverlay*(위험비율 오버레이 매개변수)",
            "support_status": "supported_existing",
            "effect": "DD 후보의 기존 DB risk-scale transfer(DB 위험비율 전달) 의미를 보존합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return ea_rows, set_rows, rule_rows, runtime_status


def build_reviews() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str]:
    selected = read_json(dd.SELECTED_CANDIDATE)
    baseline_gap = read_csv(dd.BASELINE_REPLAY_GAP).iloc[0].to_dict()
    ea_rows, set_rows, rule_rows, runtime_status = review_runtime_support(selected)
    selected_review = [
        {
            "run_id": RUN_ID,
            "candidate_id": selected["variant_id"],
            "selected_estimated_mt5_net_profit": selected["estimated_mt5_net_profit"],
            "selected_estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
            "selected_estimated_mt5_density": selected["estimated_mt5_density"],
            "selected_estimated_mt5_drawdown": selected["estimated_mt5_drawdown"],
            "selected_sim_short_trade_count": selected["sim_short_trade_count"],
            "selected_sim_short_share": selected["sim_short_share"],
            "db_mt5_net_profit": selected["db_mt5_net_profit"],
            "db_mt5_profit_factor": selected["db_mt5_profit_factor"],
            "db_mt5_short_share": selected["db_mt5_short_share"],
            "review_read": "review_candidate_with_runtime_repair_required(런타임 보정 필요 검토 후보)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    boundary_rows = [
        {
            "run_id": RUN_ID,
            "candidate_id": selected["variant_id"],
            "baseline_sim_net": baseline_gap.get("sim_net_profit", ""),
            "baseline_db_mt5_net": baseline_gap.get("db_mt5_net_profit", ""),
            "baseline_gap": baseline_gap.get("net_gap_db_minus_sim", ""),
            "selected_estimated_mt5_net": selected["estimated_mt5_net_profit"],
            "selected_estimated_mt5_pf": selected["estimated_mt5_profit_factor"],
            "boundary": "telemetry replay delta only; MT5 package and tester output required(텔레메트리 재생 변화분 전용, MT5 패키지와 테스터 출력 필요)",
            "effect": "estimated KPI(추정 KPI)를 runtime authority(런타임 권위)로 쓰지 못하게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    package_rows = [
        {
            "run_id": RUN_ID,
            "candidate_id": selected["variant_id"],
            "decision": "open_runtime_package_repair" if runtime_status != "exact_supported_parameter_only" else "open_parameter_only_runtime_package",
            "runtime_status": runtime_status,
            "required_repair": "add InpSyntheticShortSourceMarginVsFlatMin and enforce p_short - p_flat >= min" if runtime_status != "exact_supported_parameter_only" else "none",
            "next_run_id": NEXT_RUN_ID,
            "effect": "MT5 package(MT5 패키지) 이전에 proxy rule(프록시 규칙)을 정확히 표현하게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue_rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "df01_runtime_flat_margin_guard_package",
            "package_subject": selected["variant_id"],
            "required_action": "patch EA flat-margin guard and materialize DD set/ini(EA flat-margin 조건 보정 및 DD set/ini 생성)",
            "success_criteria": "compile zero errors and package has hours 17|18|19|20|21, p_short_min 0.4375, margin_vs_long 0.05, margin_vs_flat 0.0, month8 block",
            "failure_criteria": "cannot represent p_short dominance without hidden logic(p_short 우세를 숨은 로직 없이 표현 불가)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "df02_runtime_probe_preparation",
            "package_subject": selected["variant_id"],
            "required_action": "prepare DB-derived runtime handoff for MT5 tester(DB 기반 런타임 인계를 MT5 테스터용으로 준비)",
            "success_criteria": "feature/model/common files copied and tester profile references new telemetry paths",
            "failure_criteria": "compile/package succeeds but tester handoff is incomplete",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return selected, selected_review, ea_rows, set_rows, rule_rows, boundary_rows, package_rows, queue_rows, runtime_status


def write_artifacts() -> tuple[dict[str, Any], str]:
    selected, selected_review, ea_rows, set_rows, rule_rows, boundary_rows, package_rows, queue_rows, runtime_status = build_reviews()
    write_csv(SELECTED_CANDIDATE_REVIEW, selected_review)
    write_csv(EA_SUPPORT_AUDIT, ea_rows)
    write_csv(RUNTIME_REPRESENTATION_AUDIT, set_rows)
    write_csv(SHORT_SOURCE_RULE_CONTRACT, rule_rows)
    write_csv(PROXY_MT5_BOUNDARY_REVIEW, boundary_rows)
    write_csv(PACKAGE_DECISION, package_rows)
    write_csv(RUN364DF_QUEUE, queue_rows)
    return selected, runtime_status


def gate_rows(runtime_status: str, receipt_paths: Sequence[Path], *, final_written: bool) -> list[dict[str, Any]]:
    ea_rows = read_csv(EA_SUPPORT_AUDIT)
    set_rows = read_csv(RUNTIME_REPRESENTATION_AUDIT)
    package_rows = read_csv(PACKAGE_DECISION)
    gates = [
        ("scope_completion_gate", exists(SELECTED_CANDIDATE_REVIEW) and exists(PACKAGE_DECISION), SELECTED_CANDIDATE_REVIEW, "DE review artifacts written(DE 검토 산출물 작성)"),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "DD/DA/EA inputs linked(DD/DA/EA 입력 연결)"),
        ("selected_candidate_review_gate", exists(SELECTED_CANDIDATE_REVIEW), SELECTED_CANDIDATE_REVIEW, "selected DD candidate reviewed(선택 DD 후보 검토)"),
        ("runtime_representation_gate", not ea_rows.empty and not set_rows.empty and runtime_status in {"repair_required_add_margin_vs_flat_guard", "exact_supported_parameter_only"}, EA_SUPPORT_AUDIT, "runtime support audited and gap named(런타임 지원 감사 및 차이 명명)"),
        ("no_trade_splitting_boundary_gate", exists(dd.DATA_INTEGRITY_AUDIT), dd.DATA_INTEGRITY_AUDIT, "DD no-overlap evidence carried forward(DD 무겹침 근거 이월)"),
        ("proxy_mt5_boundary_gate", exists(PROXY_MT5_BOUNDARY_REVIEW), PROXY_MT5_BOUNDARY_REVIEW, "proxy/MT5 boundary declared(프록시/MT5 경계 명시)"),
        ("package_decision_gate", not package_rows.empty and exists(RUN364DF_QUEUE), PACKAGE_DECISION, "DF package queue opened(DF 패키지 대기열 개방)"),
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


def final_payload(selected: Mapping[str, Any], runtime_status: str, gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_anchor_run_id": PACKAGE_ANCHOR_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_variant_id": selected["variant_id"],
        "runtime_representation_status": runtime_status,
        "required_repair": "InpSyntheticShortSourceMarginVsFlatMin" if runtime_status != "exact_supported_parameter_only" else "none",
        "selected_estimated_mt5_net_profit": selected["estimated_mt5_net_profit"],
        "selected_estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
        "selected_estimated_mt5_density": selected["estimated_mt5_density"],
        "selected_estimated_mt5_drawdown": selected["estimated_mt5_drawdown"],
        "selected_sim_short_trade_count": selected["sim_short_trade_count"],
        "selected_sim_short_share": selected["sim_short_share"],
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
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


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUNTIME_RECEIPT, {**base, "research_path": rel(dd.SHORT_SOURCE_SURFACE), "runtime_path": rel(EA_PATH), "shared_contract": rel(SHORT_SOURCE_RULE_CONTRACT), "known_differences": ["EA currently lacks explicit margin_vs_flat guard for synthetic short source"], "parity_check": rel(EA_SUPPORT_AUDIT), "parity_identity": {"ea_sha256": sha(EA_PATH), "anchor_set_sha256": sha(DA_SET_PATH)}, "runtime_claim_boundary": "research_only_repair_required(연구 전용, 보정 필요)"})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dd.SELECTED_TRADE_TAPE), rel(dd.DATA_INTEGRITY_AUDIT)], "time_axis": "carried from DD telemetry replay(DD 텔레메트리 재생에서 이월)", "sample_scope": "Tier A proxy review(Tier A 프록시 검토)", "missing_or_duplicate_check": rel(dd.DATA_INTEGRITY_AUDIT), "feature_label_boundary": "review only; no new feature calculation(검토 전용, 새 피처 계산 없음)", "split_boundary": "out_of_scope_by_claim_proxy_review_only(주장 범위 밖, 프록시 검토 전용)", "leakage_risk": "runtime package must not add future-path filters(런타임 패키지는 미래 경로 필터를 추가하면 안 됨)", "data_hash_or_identity": sha(dd.SELECTED_TRADE_TAPE), "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)"})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(SELECTED_CANDIDATE_REVIEW), rel(EA_SUPPORT_AUDIT), rel(PACKAGE_DECISION), rel(PROXY_MT5_BOUNDARY_REVIEW)], "evidence_missing": ["new MT5 package", "MetaEditor compile", "MT5 tester output", "forward/replay evidence"], "judgment_label": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "DD candidate is worth packaging, but exact p_short dominance needs EA guard repair(DD 후보는 패키지 가치가 있지만 정확한 p_short 우세는 EA 조건 보정이 필요)."})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "tracked_review_artifacts(추적된 검토 산출물)", "lineage_judgment": "connected_with_repair_boundary(보정 경계로 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "runtime representation review opens repair package(런타임 표현 검토가 보정 패키지를 연다)", "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "review finding(검토 결과)을 operating claim(운영 주장)으로 과장하지 않음"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    ea_rows = read_csv(EA_SUPPORT_AUDIT).to_dict("records")
    package = read_csv(PACKAGE_DECISION).to_dict("records")
    report = f"""# run364DE h17 short-source expansion review(17시 숏 원천 확장 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- selected variant(선택 변형): `{final['selected_variant_id']}`
- judgment(판정): `{final['judgment']}`
- runtime representation status(런타임 표현 상태): `{final['runtime_representation_status']}`
- required repair(필수 보정): `{final['required_repair']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Action/Effect(행동/효과)

Action(행동): DD selected short-source rule(DD 선택 숏 원천 규칙)을 RuntimeProbeEA(런타임 탐침 EA)와 DA set(DA 설정)으로 표현 가능한지 검토했습니다.

Effect(효과): hours/p_short/margin_vs_long/month8 block(시간/p_short/margin_vs_long/8월 차단)은 표현 가능하지만, p_short > p_flat dominance(p_short 우세)를 정확히 닫는 flat-margin guard(flat 마진 조건)가 EA에 없어 `run364DF` 보정 패키지를 열었습니다.

## EA Support(EA 지원)

{markdown_table(ea_rows, ['check_id', 'status', 'effect'])}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'runtime_status', 'required_repair', 'next_run_id'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is review only(검토 전용)입니다. new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DE decision(결정): short-source expansion runtime review(숏 원천 확장 런타임 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{final['selected_variant_id']}`
- runtime representation status(런타임 표현 상태): `{final['runtime_representation_status']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): EA flat-margin guard(EA flat 마진 조건)를 추가한 뒤 DD 패키지를 만들도록 넘깁니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DE__{RUN_ID}", f"\n- run364DE__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - DD short-source runtime review(DD 숏 원천 런타임 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364DE__{RUN_ID}", f"\n## run364DE Runtime Review(런타임 검토)\n\nAction(행동): DD short-source rule(DD 숏 원천 규칙)의 RuntimeProbeEA(런타임 탐침 EA) 표현 가능성을 검토했습니다.\n\nEffect(효과): flat-margin guard(flat 마진 조건) 보정이 필요해 `{NEXT_RUN_ID}`를 열었습니다.\n")
    append_text_once(STAGE_README, f"run364DE__{RUN_ID}", f"\n<!-- run364DE__{RUN_ID} -->\n## run364DE runtime review(런타임 검토)\n\nSelected(선택): `{final['selected_variant_id']}`. Required repair(필수 보정): `{final['required_repair']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DE` completed(완료) DD short-source runtime review(DD 숏 원천 런타임 검토). Selected variant(선택 변형) `{final['selected_variant_id']}`는 package-worthy proxy review candidate(패키지 가치가 있는 프록시 검토 후보)이지만, exact runtime representation(정확한 런타임 표현)을 위해 `{final['required_repair']}` 보정이 필요합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 RuntimeProbeEA(런타임 탐침 EA)에 flat-margin guard(flat 마진 조건)를 추가하고 DD MT5 package(DD MT5 패키지)를 materialize(구체화)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): `{RUN_ID}`.

Selected variant(선택 변형): `{final['selected_variant_id']}`.

Runtime representation(런타임 표현): `{final['runtime_representation_status']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DE__{RUN_ID}", f"\n<!-- run364DE__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed DD runtime representation review(DD 런타임 표현 검토); repair `{final['required_repair']}`; next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364DE__{RUN_ID}", f"\n<!-- run364DE__{RUN_ID} -->\n- `{RUN_ID}`: DD short-source rule(DD 숏 원천 규칙) is package-worthy with runtime repair(런타임 보정 포함 패키지 가치 있음). Required(필수): `{final['required_repair']}`.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364DE__{RUN_ID}", f"\n<!-- run364DE__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님). Existing EA lacked exact flat-margin guard(기존 EA에 정확한 flat 마진 조건 없음); operating claim(운영 주장) 금지 until MT5 probe(MT5 탐침) exists.\n")


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
        "scoreboard_lane": "runtime_review(런타임 검토)",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "evidence_boundary": "runtime_representation_review_only(런타임 표현 검토 전용)",
        "question": "Can DD short-source rule be represented exactly in RuntimeProbeEA?(DD 숏 원천 규칙을 RuntimeProbeEA에 정확히 표현할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_estimated_mt5_net_profit"],
        "profit_factor": final["selected_estimated_mt5_profit_factor"],
        "drawdown": final["selected_estimated_mt5_drawdown"],
        "trade_density_per_feature_day": final["selected_estimated_mt5_density"],
        "short_trade_count": final["selected_sim_short_trade_count"],
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(PACKAGE_DECISION),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, status, include in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_separate", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_runtime_review(Tier B 런타임 검토 없음)", False),
        ("tier_ab_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_review_tier_a_only(주장 범위 밖, Tier A 검토 전용)", False),
    ]:
        ledger_rows.append(
            {
                **common,
                "subrun_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "runtime_representation_review(런타임 표현 검토)",
                "status": status,
                "rows": 1 if include else 0,
                "net_profit": final["selected_estimated_mt5_net_profit"] if include else "",
                "profit_factor": final["selected_estimated_mt5_profit_factor"] if include else "",
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
            ("candidate_review", SELECTED_CANDIDATE_REVIEW, "Selected candidate review(선택 후보 검토)."),
            ("runtime_representation_audit", RUNTIME_REPRESENTATION_AUDIT, "Runtime representation audit(런타임 표현 감사)."),
            ("ea_support_audit", EA_SUPPORT_AUDIT, "EA support audit(EA 지원 감사)."),
            ("package_decision", PACKAGE_DECISION, "Package decision(패키지 결정)."),
            ("rule_contract", SHORT_SOURCE_RULE_CONTRACT, "Short source rule contract(숏 원천 규칙 계약)."),
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
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    selected, runtime_status = write_artifacts()
    receipt_paths = [RUNTIME_RECEIPT, DATA_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(runtime_status, receipt_paths, final_written=False)
    created_at = now_utc()
    final = final_payload(selected, runtime_status, gates, created_at)
    write_receipts(final)
    gates = gate_rows(runtime_status, receipt_paths, final_written=True)
    final = final_payload(selected, runtime_status, gates, created_at)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
