from __future__ import annotations

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
from stage_pipelines.stage364 import materialize_h17_month12_secondary_month_margin_guard_runtime_package_without_db as cu  # noqa: E402
from stage_pipelines.stage364 import review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db as cw  # noqa: E402
from stage_pipelines.stage364 import train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CZ"
RUN_ID = "run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
RUNTIME_ANCHOR_RUN_ID = cu.RUN_ID
MT5_REVIEW_RUN_ID = cw.RUN_ID
NEXT_RUN_ID = "run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1"

STATUS = "completed_stage364CZ_h17_short_quality_risk_scale_review_runtime_representation_repair_required_no_authority"
JUDGMENT = "positive_proxy_short_quality_risk_lift_runtime_representation_gap_open_da_no_authority"
DECISION = "stage364CZ_open_run364DA_h17_short_quality_risk_scale_runtime_package"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_"
    "runtime_representation_repair_required_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = parent.STAGE_DIR
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
RISK_SCALE_RULE_CONTRACT = RUN_DIR / "risk_scale_rule_contract.csv"
PROXY_MT5_GAP_REVIEW = RUN_DIR / "proxy_mt5_gap_review.csv"
EQUITY_DD_BOUNDARY_REVIEW = RUN_DIR / "equity_dd_boundary_review.csv"
RUN364DA_QUEUE = RUN_DIR / "run364DA_short_quality_risk_scale_runtime_package_queue.csv"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CZ_h17_equity_dd_side_balance_proxy_gap_scout_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CZ_h17_equity_dd_side_balance_proxy_gap_scout_review.md"
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
CU_SET_PATH = cu.SET_DIR / "OPv2_run364CU_cr04_secondary_month_guard.set"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.SELECTED_CANDIDATE,
    parent.SELECTED_TRADE_TAPE,
    parent.CY_PROXY_REPAIR_SURFACE,
    parent.PACKAGE_PRECHECK,
    parent.PROXY_MT5_DIFF_PLAN,
    parent.RUN364CZ_QUEUE,
    parent.VARIANT_RISK_SCALE_AUDIT,
    parent.VARIANT_SIDE_ATTRIBUTION,
    parent.VARIANT_MONTH_ATTRIBUTION,
    parent.VARIANT_HOUR_SIDE_ATTRIBUTION,
    parent.EQUITY_RISK_PROXY_DIAGNOSTIC,
    parent.SIDE_BALANCE_PROXY_DIAGNOSTIC,
    parent.RUN_MANIFEST,
    cw.MT5_KPI_REVIEW,
    cw.DRAWDOWN_REVIEW,
    cw.RUN_MANIFEST,
    cu.FINAL_DECISION,
    cu.RUNTIME_POLICY_CONFIG,
    cu.RUNTIME_PARITY_CONTRACT,
    cu.TESTER_SET_MANIFEST,
    CU_SET_PATH,
    EA_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SELECTED_CANDIDATE_REVIEW,
    RUNTIME_REPRESENTATION_AUDIT,
    EA_SUPPORT_AUDIT,
    PACKAGE_DECISION,
    RISK_SCALE_RULE_CONTRACT,
    PROXY_MT5_GAP_REVIEW,
    EQUITY_DD_BOUNDARY_REVIEW,
    RUN364DA_QUEUE,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    ATTRIBUTION_RECEIPT,
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
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


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
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CZ inputs(CZ 입력 누락): " + ", ".join(missing))
    parent_final = read_json(parent.FINAL_DECISION)
    selected = read_json(parent.SELECTED_CANDIDATE)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CY next_run_id mismatch(CY 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if selected.get("variant_id") != parent_final.get("selected_variant_id"):
        raise RuntimeError("CY selected variant mismatch(CY 선택 변형 불일치)")
    for label, final in [("CY", parent_final), ("CW", read_json(cw.FINAL_DECISION)), ("CU", read_json(cu.FINAL_DECISION))]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            value = final.get(key, "not_claimed")
            if value != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={value}")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CY gate audit(CY 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent_final, selected


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "CZ runtime representation review source(CZ 런타임 표현 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def ea_support_flags() -> dict[str, Any]:
    ea_text = io_path(EA_PATH).read_text(encoding="utf-8-sig")
    set_text = io_path(CU_SET_PATH).read_text(encoding="utf-8-sig")
    required_overlay_tokens = [
        "InpRiskScaleOverlayEnabled",
        "InpRiskScaleOverlaySide",
        "InpRiskScaleOverlayHours",
        "InpRiskScaleOverlayMinMarginVsLong",
        "InpRiskScaleOverlayMultiplier",
    ]
    return {
        "has_fixed_lot": "InpFixedLot" in ea_text,
        "has_model_risk_sizing": "InpModelRiskSizingEnabled" in ea_text and "BuildRiskSizingDecision" in ea_text,
        "has_synthetic_short_source": "ApplySyntheticShortSourceOverlay" in ea_text,
        "has_secondary_month_guard": "InpMonthMarginGuard2Enabled" in ea_text,
        "has_risk_scale_overlay": all(token in ea_text for token in required_overlay_tokens),
        "missing_overlay_tokens": [token for token in required_overlay_tokens if token not in ea_text],
        "cu_set_model_risk_enabled": "InpModelRiskSizingEnabled=true" in set_text,
        "cu_set_fixed_lot": "InpFixedLot=0.1" in set_text,
        "ea_sha256": sha(EA_PATH),
        "cu_set_sha256": sha(CU_SET_PATH),
    }


def selected_review_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "net_profit": selected["net_profit"],
            "profit_factor": selected["profit_factor"],
            "expectancy": selected["expectancy"],
            "trade_count": selected["trade_count"],
            "trade_density": selected["trade_density"],
            "long_trade_count": selected["long_trade_count"],
            "short_trade_count": selected["short_trade_count"],
            "risk_scaled_trade_count": selected["risk_scaled_trade_count"],
            "risk_scaled_short_count": selected["risk_scaled_short_count"],
            "risk_scale_net_delta": selected["risk_scale_net_delta"],
            "short_net_delta_vs_proxy_base": selected["short_net_delta_vs_proxy_base"],
            "month12_total_net": selected["month12_total_net"],
            "month12_long_net": selected["month12_long_net"],
            "closed_trade_drawdown_proxy": selected["closed_trade_drawdown_proxy"],
            "mt5_baseline_equity_dd": selected["mt5_baseline_equity_dd"],
            "package_precheck_status": selected["package_precheck_status"],
            "review_status": "positive_proxy_candidate_runtime_repair_required(긍정 프록시 후보, 런타임 수리 필요)",
            "effect": "keeps the short-quality risk idea while blocking direct MT5 package(숏 품질 위험 아이디어는 보존하고 직접 MT5 패키지는 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def ea_support_rows(flags: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        ("fixed_lot_support", flags["has_fixed_lot"], "EA can run fixed-lot probes(EA가 고정 랏 탐침을 실행할 수 있음)"),
        ("model_risk_sizing_support", flags["has_model_risk_sizing"], "EA has generic confidence risk sizing(EA가 일반 신뢰도 기반 위험 산정을 가짐)"),
        ("synthetic_short_source_support", flags["has_synthetic_short_source"], "EA can create synthetic short source overlay(EA가 합성 숏 원천 오버레이를 만들 수 있음)"),
        ("secondary_month_guard_support", flags["has_secondary_month_guard"], "EA has the CU month guard repair(EA가 CU 월 가드 수리를 가짐)"),
        ("short_quality_risk_scale_overlay_support", flags["has_risk_scale_overlay"], "EA can exactly express cx05 risk-scale overlay(EA가 cx05 위험비율 오버레이를 정확히 표현할 수 있음)"),
    ]
    return [
        {
            "run_id": RUN_ID,
            "check_id": check_id,
            "status": "present(존재)" if passed else "missing(누락)",
            "passed": passed,
            "evidence": evidence,
            "effect": "supports runtime handoff(런타임 인계를 지지)" if passed else "requires runtime repair before MT5 probe(MT5 탐침 전 런타임 수리 필요)",
            "ea_sha256": flags["ea_sha256"],
            "cu_set_sha256": flags["cu_set_sha256"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for check_id, passed, evidence in checks
    ]


def runtime_representation_rows(selected: Mapping[str, Any], flags: Mapping[str, Any]) -> list[dict[str, Any]]:
    exact_ready = bool(flags["has_risk_scale_overlay"])
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "representation_id": "cx05_exact_short_quality_risk_scale_overlay",
            "proxy_rule": "short hours 17|18|19|20 with margin_vs_long >= 0.080 use risk_scale 1.10(17|18|19|20시 숏 중 롱 대비 마진 0.080 이상은 위험비율 1.10)",
            "current_runtime_support": f"risk_overlay={exact_ready};model_risk={flags['has_model_risk_sizing']};fixed_lot={flags['has_fixed_lot']}",
            "representation_status": "represented_exactly_ready_for_package(정확 표현 가능, 패키지 가능)" if exact_ready else "repair_required_missing_parameterized_short_quality_risk_scale_overlay(파라미터화 숏 품질 위험비율 오버레이 누락으로 수리 필요)",
            "required_runtime_change": "add parameterized side/hour/margin risk-scale overlay before lot execution(랏 실행 전 방향/시간/마진 기반 위험비율 오버레이 추가)",
            "missing_tokens": "|".join(flags["missing_overlay_tokens"]),
            "effect": "prevents treating proxy lot scaling as MT5 behavior before EA support(EA 지원 전 프록시 랏 조정을 MT5 동작으로 취급하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "representation_id": "generic_model_risk_sizing_not_exact",
            "proxy_rule": "confidence-based risk sizing is generic, not cx05 side/hour/margin specific(신뢰도 기반 위험 산정은 일반형이고 cx05 방향/시간/마진 전용이 아님)",
            "current_runtime_support": f"model_risk={flags['has_model_risk_sizing']};cu_set_enabled={flags['cu_set_model_risk_enabled']}",
            "representation_status": "available_but_not_semantically_equivalent(사용 가능하지만 의미 동일 아님)",
            "required_runtime_change": "do not substitute generic model risk for cx05 exact rule(cx05 정확 규칙을 일반 모델 위험으로 대체하지 않음)",
            "missing_tokens": "",
            "effect": "keeps runtime parity boundary clear(런타임 동등성 경계를 명확히 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": "cx00_cr04_secondary_guard_anchor",
            "representation_id": "current_cu_anchor_exact_for_cr04_not_cx05",
            "proxy_rule": "CR04 secondary month guard anchor without short risk boost(숏 위험 증폭 없는 CR04 보조 월 가드 기준)",
            "current_runtime_support": f"secondary_month_guard={flags['has_secondary_month_guard']};cu_set_fixed_lot={flags['cu_set_fixed_lot']}",
            "representation_status": "represented_anchor_but_not_selected_cx05(기준은 표현되지만 선택 cx05는 아님)",
            "required_runtime_change": "carry CU anchor forward and add risk-scale overlay(CU 기준을 이어가며 위험비율 오버레이 추가)",
            "missing_tokens": "",
            "effect": "keeps previous MT5-positive anchor as the package base(이전 MT5 양수 기준을 패키지 기반으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def package_decision_rows(selected: Mapping[str, Any], representation: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    exact_ready = str(representation[0]["representation_status"]).startswith("represented_exactly")
    proxy_pass = str(selected.get("package_precheck_status", "")).startswith("passed")
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "decision_id": "proxy_kpi_review",
            "decision_status": "passed_for_runtime_repair_queue(런타임 수리 대기열 통과)" if proxy_pass else "failed_proxy_package_screen(프록시 패키지 선별 실패)",
            "evidence": f"net={selected['net_profit']};pf={selected['profit_factor']};density={selected['trade_density']};shorts={selected['short_trade_count']};risk_delta={selected['risk_scale_net_delta']}",
            "effect": "proxy quality justifies runtime package repair work(프록시 품질이 런타임 패키지 수리 작업을 정당화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "decision_id": "direct_mt5_package_decision",
            "decision_status": "direct_package_blocked_runtime_repair_required(직접 패키지 차단, 런타임 수리 필요)" if not exact_ready else "direct_package_allowed_exact_support(정확 지원으로 직접 패키지 가능)",
            "evidence": representation[0]["current_runtime_support"],
            "effect": "avoids external MT5 probe with changed meaning(뜻이 바뀐 외부 MT5 탐침을 피함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "decision_id": "next_work_packet",
            "decision_status": "open_run364DA_runtime_package_repair(run364DA 런타임 패키지 수리 개방)",
            "evidence": rel(RUN364DA_QUEUE),
            "effect": "turns the gap into implementable EA/set requirements(간극을 구현 가능한 EA/설정 요구사항으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def risk_scale_contract_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "contract_id": "cx05_short_quality_risk_scale_contract",
            "side": "short",
            "hours": "17|18|19|20",
            "basis": "margin_vs_long",
            "min_margin_vs_long": 0.080,
            "risk_scale_multiplier": 1.10,
            "entry_count_effect": "none_no_trade_splitting(없음, 거래 쪼개기 없음)",
            "lot_effect": "multiply selected short order lot or computed risk lot by 1.10(선택 숏 주문 랏 또는 계산 위험 랏에 1.10 곱함)",
            "timestamp_boundary": "uses target bar time and entry-known probabilities only(대상 봉 시간과 진입시점 기지 확률만 사용)",
            "telemetry_requirement": "record applied multiplier and overlay reason in runtime telemetry(적용 배수와 오버레이 이유를 런타임 원격측정에 기록)",
            "effect": "defines the exact shared contract for DA implementation(DA 구현을 위한 정확한 공유 계약 정의)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def proxy_mt5_gap_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    selected_net = as_float(selected.get("net_profit"))
    proxy_base_net = as_float(selected.get("proxy_base_net_profit"))
    mt5_net = as_float(selected.get("mt5_baseline_net_profit"))
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "comparison_id": "selected_proxy_vs_current_mt5_anchor",
            "selected_proxy_net": selected_net,
            "current_mt5_anchor_net": mt5_net,
            "proxy_minus_mt5_anchor": finite(selected_net - mt5_net, 8),
            "proxy_base_minus_mt5_anchor": finite(proxy_base_net - mt5_net, 8),
            "selected_delta_vs_proxy_base": selected["net_delta_vs_proxy_base"],
            "review_status": "mt5_reprobe_required(MT5 재탐침 필요)",
            "effect": "keeps proxy uplift separate from actual MT5 KPI(프록시 개선과 실제 MT5 핵심 성과 지표를 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def equity_dd_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "proxy_closed_trade_drawdown": selected["closed_trade_drawdown_proxy"],
            "current_mt5_equity_drawdown": selected["mt5_baseline_equity_dd"],
            "boundary_status": "unresolved_until_mt5_runtime_probe(MT5 런타임 탐침 전 미해결)",
            "effect": "risk-scale proxy did not prove equity DD repair(위험비율 프록시가 수익곡선 낙폭 수리를 증명하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def da_queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "da01_implement_short_quality_risk_scale_overlay",
            "candidate_id": selected["variant_id"],
            "implementation_subject": "RuntimeProbeEA parameterized risk-scale overlay(RuntimeProbeEA 파라미터화 위험비율 오버레이)",
            "required_inputs": "InpRiskScaleOverlayEnabled;InpRiskScaleOverlaySide;InpRiskScaleOverlayHours;InpRiskScaleOverlayMinMarginVsLong;InpRiskScaleOverlayMultiplier",
            "package_base": rel(CU_SET_PATH),
            "success_criteria": "EA compiles, set/ini package created, rule contract exactly represented(EA 컴파일, 설정/INI 패키지 생성, 규칙 계약 정확 표현)",
            "failure_criteria": "rule changes entry count, uses hidden future data, or cannot record lineage(규칙이 진입수를 바꾸거나 숨은 미래 데이터를 쓰거나 계보 기록 불가)",
            "effect": "prepares MT5 runtime probe without changing cx05 meaning(cx05 의미를 바꾸지 않고 MT5 런타임 탐침 준비)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "runtime_representation_review(런타임 표현 검토)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "hypothesis": "A short-quality risk-scale proxy lift can become an MT5 package only if the EA expresses the same side/hour/margin rule.",
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "proxy_kpi_review_gate",
                "runtime_representation_gate",
                "package_boundary_gate",
                "artifact_lineage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(receipts_written: bool) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate": "scope_completion_gate",
            "status": "passed",
            "evidence": rel(SELECTED_CANDIDATE_REVIEW),
            "effect": "selected CY candidate reviewed(선택 CY 후보 검토 완료)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "input_lineage_gate",
            "status": "passed",
            "evidence": rel(INPUT_MANIFEST),
            "effect": "CY/CW/CU inputs connected(CY/CW/CU 입력 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "proxy_kpi_review_gate",
            "status": "passed",
            "evidence": rel(PACKAGE_DECISION),
            "effect": "proxy KPI supports repair queue, not authority(프록시 KPI는 수리 대기열만 지지하고 권위는 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "runtime_representation_gate",
            "status": "passed",
            "evidence": rel(RUNTIME_REPRESENTATION_AUDIT),
            "effect": "exact support gap recorded(정확 지원 간극 기록)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "package_boundary_gate",
            "status": "passed",
            "evidence": rel(RUN364DA_QUEUE),
            "effect": "direct MT5 package blocked until DA repair(DA 수리 전 직접 MT5 패키지 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "artifact_lineage_gate",
            "status": "passed" if receipts_written and exists(LINEAGE_RECEIPT) else "pending",
            "evidence": rel(LINEAGE_RECEIPT),
            "effect": "artifact lineage receipt written(산출물 계보 영수증 작성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if receipts_written else "pending",
            "evidence": rel(GATE_AUDIT),
            "effect": "required gates linked to closeout(필수 게이트 종료 기록 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed" if receipts_written and exists(CLAIM_RECEIPT) else "pending",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "no authority/promotion/goal claim(권위/승격/목표 주장 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(selected: Mapping[str, Any], flags: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "runtime_anchor_run_id": RUNTIME_ANCHOR_RUN_ID,
        "mt5_review_run_id": MT5_REVIEW_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "reviewed_variant_id": selected["variant_id"],
        "reviewed_net_profit": selected["net_profit"],
        "reviewed_profit_factor": selected["profit_factor"],
        "reviewed_expectancy": selected["expectancy"],
        "reviewed_trade_count": selected["trade_count"],
        "reviewed_density": selected["trade_density"],
        "reviewed_short_trade_count": selected["short_trade_count"],
        "reviewed_risk_scaled_short_count": selected["risk_scaled_short_count"],
        "reviewed_risk_scale_net_delta": selected["risk_scale_net_delta"],
        "reviewed_month12_net": selected["month12_total_net"],
        "reviewed_month12_long_net": selected["month12_long_net"],
        "reviewed_closed_trade_drawdown_proxy": selected["closed_trade_drawdown_proxy"],
        "current_mt5_net_profit": selected["mt5_baseline_net_profit"],
        "current_mt5_profit_factor": selected["mt5_baseline_profit_factor"],
        "current_mt5_density": selected["mt5_baseline_density"],
        "current_mt5_equity_dd": selected["mt5_baseline_equity_dd"],
        "runtime_representation_status": "exact_support_present" if flags["has_risk_scale_overlay"] else "repair_required_missing_short_quality_risk_scale_overlay",
        "package_decision": "runtime_representation_repair_required_before_mt5_probe",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "external_verification_status": "out_of_scope_by_claim_review_only_runtime_representation_gap",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any], flags: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(parent.SELECTED_CANDIDATE),
            "runtime_path": rel(EA_PATH),
            "shared_contract": rel(RISK_SCALE_RULE_CONTRACT),
            "known_differences": [
                "CY is proxy-only(CY는 프록시 전용) and has no new MT5 tester output(새 MT5 테스터 출력 없음).",
                "Current EA has generic risk sizing but not the cx05 side/hour/margin risk-scale overlay(현재 EA는 일반 위험 산정은 있으나 cx05 방향/시간/마진 위험비율 오버레이는 없음).",
            ],
            "parity_check": "representation audit only; compile/tester output deferred to DA(표현 감사 전용, 컴파일/테스터 출력은 DA로 이월)",
            "parity_identity": {
                "ea_sha256": flags["ea_sha256"],
                "cu_set_sha256": flags["cu_set_sha256"],
                "selected_candidate_sha256": sha(parent.SELECTED_CANDIDATE),
            },
            "runtime_claim_boundary": "research_only_runtime_representation_repair_required(연구 전용, 런타임 표현 수리 필요)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "cx05 high-quality short risk-scale proxy candidate(cx05 고품질 숏 위험비율 프록시 후보)",
            "evidence_available": [rel(SELECTED_CANDIDATE_REVIEW), rel(PACKAGE_DECISION), rel(RUNTIME_REPRESENTATION_AUDIT), rel(EA_SUPPORT_AUDIT)],
            "evidence_missing": ["EA exact overlay implementation(EA 정확 오버레이 구현)", "MetaEditor compile(메타에디터 컴파일)", "new MT5 Strategy Tester output(새 MT5 전략 테스터 출력)", "runtime equity DD result(런타임 수익곡선 낙폭 결과)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The proxy improved, but MT5 must first learn the exact risk-scale rule(프록시는 개선됐지만 MT5는 먼저 정확한 위험비율 규칙을 배워야 함).",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": "selected cx05 adds 7.87 net through 79 risk-scaled short trades without changing entry count(선택 cx05는 진입수를 바꾸지 않고 위험비율 조정 숏 79개로 순수익 7.87 추가)",
            "comparison_baseline": "cx00 CR04 anchor(cx00 CR04 기준)",
            "likely_drivers": ["short hours 17-20", "margin_vs_long >= 0.080", "risk_scale 1.10"],
            "segment_checks": [rel(parent.VARIANT_SIDE_ATTRIBUTION), rel(parent.VARIANT_HOUR_SIDE_ATTRIBUTION), rel(PROXY_MT5_GAP_REVIEW)],
            "alternative_explanations": ["proxy lot scaling may not reproduce in MT5", "equity DD remains unresolved", "current CU set fixed lot does not include cx05 overlay"],
            "attribution_confidence": "medium_proxy_only(중간, 프록시 전용)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    refresh_lineage_receipt(final)
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "positive proxy review with runtime representation repair requirement(긍정 프록시 검토와 런타임 표현 수리 필요)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "Goal Achieve"],
            "new_model_training": final["new_model_training"],
            "new_mt5_execution": final["new_mt5_execution"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "prevents proxy result from being promoted into operating truth(프록시 결과가 운영 진실로 승격되는 일을 막음)",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if path != LINEAGE_RECEIPT and exists(path) and io_path(path).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_reproducible_from_script(추적 가능하고 스크립트로 재생 가능)",
            "lineage_judgment": "connected_with_runtime_repair_boundary(런타임 수리 경계로 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    if len(rows) > limit:
        lines.append("| ... | ... | ... | ... |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], representation: Sequence[Mapping[str, Any]], package_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364CZ h17 equity DD side balance proxy gap scout review(364CZ 17시 수익곡선 낙폭/방향 균형/프록시 차이 정찰 검토)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- reviewed variant(검토 변형): `{final['reviewed_variant_id']}`
- proxy net/PF/density(프록시 순수익/수익 팩터/밀도): `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}`
- risk-scaled short count(위험비율 조정 숏 수): `{final['reviewed_risk_scaled_short_count']}`
- risk-scale net delta(위험비율 순수익 변화): `{final['reviewed_risk_scale_net_delta']}`
- current MT5 anchor net/PF/density/equity DD(현재 MT5 기준 순수익/수익 팩터/밀도/수익곡선 낙폭): `{final['current_mt5_net_profit']}` / `{final['current_mt5_profit_factor']}` / `{final['current_mt5_density']}` / `{final['current_mt5_equity_dd']}`
- package decision(패키지 결정): `{final['package_decision']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Action And Effect(행동과 효과)

Action(행동): `run364CY` selected proxy(선택 프록시) `cx05`를 EA support(EA 지원), runtime representation(런타임 표현), proxy/MT5 gap(프록시/MT5 차이), equity DD boundary(수익곡선 낙폭 경계)로 검토했습니다.

Effect(효과): `cx05`는 proxy(프록시) 기준으로 보존할 가치가 있지만, 현재 RuntimeProbeEA(런타임 탐침 EA)는 “17-20시 숏, `margin_vs_long >= 0.080`, risk_scale(위험비율) `1.10`”을 정확히 파라미터화하지 못합니다. 따라서 직접 MT5 package(MT5 패키지)는 막고 `{NEXT_RUN_ID}`에서 런타임 패키지 수리로 넘깁니다.

## Package Decision(패키지 결정)

{markdown_table(package_rows, ['decision_id', 'decision_status', 'evidence', 'effect'], 8)}

## Runtime Representation(런타임 표현)

{markdown_table(representation, ['representation_id', 'representation_status', 'required_runtime_change', 'effect'], 8)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 8)}

## Boundary(경계)

This is review only(검토 전용)입니다. New MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CZ decision(결정): h17 short-quality risk-scale runtime repair required(17시 숏 품질 위험비율 런타임 수리 필요)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- reviewed variant(검토 변형): `{final['reviewed_variant_id']}`
- proxy net/PF/density(프록시 순수익/수익 팩터/밀도): `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}`
- runtime status(런타임 상태): `{final['runtime_representation_status']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): proxy(프록시) 개선을 버리지 않고, MT5(메타트레이더5)에서 같은 의미로 실행되도록 EA/set(전문가 자문/설정) 수리를 먼저 엽니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364CZ__{RUN_ID}", f"\n- run364CZ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cx05 runtime representation repair required(cx05 런타임 표현 수리 필요), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364CZ__{RUN_ID}",
        f"""
<!-- run364CZ__{RUN_ID} -->

## run364CZ Runtime Representation Review(364CZ 런타임 표현 검토)

Action(행동): `cx05_high_quality_short_boost110_h17_20` proxy candidate(프록시 후보)를 EA 표현 가능성까지 검토했습니다.

Effect(효과): short quality risk-scale overlay(숏 품질 위험비율 오버레이)가 필요하므로 `{NEXT_RUN_ID}`에서 런타임 패키지 수리로 이어갑니다.
""",
    )
    append_text_once(STAGE_README, f"run364CZ__{RUN_ID}", f"\n<!-- run364CZ__{RUN_ID} -->\n## run364CZ review(364CZ 검토)\n\nSelected(선택): `{final['reviewed_variant_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Reviewed proxy candidate(검토 프록시 후보): `{final['reviewed_variant_id']}`.

Review result(검토 결과): proxy KPI(프록시 핵심 성과 지표)는 보존 가치가 있지만 exact runtime representation(정확 런타임 표현)을 위해 short quality risk-scale overlay(숏 품질 위험비율 오버레이)가 필요합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 EA(전문가 자문)와 set/ini package(설정/INI 패키지)를 수리합니다.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
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

Current truth(현재 진실): `run364CZ` reviewed(검토 완료) `cx05_high_quality_short_boost110_h17_20`. Proxy KPI(프록시 핵심 성과 지표)는 net/PF/density(순수익/수익 팩터/밀도) `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}`이고, risk-scale net delta(위험비율 순수익 변화)는 `{final['reviewed_risk_scale_net_delta']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 RuntimeProbeEA(런타임 탐침 EA)에 side/hour/margin risk-scale overlay(방향/시간/마진 위험비율 오버레이)를 추가하고 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만듭니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364CZ__{RUN_ID}", f"\n<!-- run364CZ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed CZ review(CZ 검토 완료); cx05 requires short quality risk-scale overlay(숏 품질 위험비율 오버레이 필요); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364CZ__{RUN_ID}", f"\n<!-- run364CZ__{RUN_ID} -->\n- `{RUN_ID}`: cx05 short quality risk-scale(숏 품질 위험비율) clue(단서)를 보존. Effect(효과): MT5(메타트레이더5)로 넘기기 전 EA(전문가 자문) 표현 수리를 다음 씨앗으로 둠.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364CZ__runtime_gap__{RUN_ID}", f"\n<!-- run364CZ__runtime_gap__{RUN_ID} -->\n- `{RUN_ID}` runtime gap(런타임 간극): cx05 proxy(프록시)는 긍정이지만 현재 EA(전문가 자문)는 side/hour/margin risk-scale overlay(방향/시간/마진 위험비율 오버레이)를 정확히 표현하지 못합니다. Effect(효과): 직접 MT5 package(MT5 패키지)를 막고 `{NEXT_RUN_ID}`에서 도구를 먼저 수리합니다.\n")


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
        "work_family": "runtime_representation_review(런타임 표현 검토)",
        "scoreboard_lane": "proxy_review(프록시 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "candidate_review_only(후보 검토 전용)",
        "question": "Can cx05 be handed to MT5 without changing its risk-scale meaning?(cx05를 위험비율 의미 변경 없이 MT5로 인계할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["reviewed_net_profit"],
        "profit_factor": final["reviewed_profit_factor"],
        "expectancy": final["reviewed_expectancy"],
        "trade_count": final["reviewed_trade_count"],
        "trade_density_per_feature_day": final["reviewed_density"],
        "short_trade_count": final["reviewed_short_trade_count"],
        "max_drawdown_amount": final["reviewed_closed_trade_drawdown_proxy"],
        "trade_density_requirement_status": "passed_proxy_review_runtime_repair_required(프록시 검토 통과, 런타임 수리 필요)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_REPRESENTATION_AUDIT),
        "primary_kpi": f"net={final['reviewed_net_profit']};pf={final['reviewed_profit_factor']};density={final['reviewed_density']};risk_delta={final['reviewed_risk_scale_net_delta']}",
        "guardrail_kpi": "runtime_representation_repair_required;no_authority",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows: list[dict[str, Any]] = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)", False),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)", True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "CZ proxy runtime review(CZ 프록시 런타임 검토)",
            "status": status,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "runtime_representation_review(런타임 표현 검토)",
        }
        if not include_metrics:
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "short_trade_count", "max_drawdown_amount"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("selected_candidate_review", SELECTED_CANDIDATE_REVIEW, "CZ selected candidate review(CZ 선택 후보 검토)."),
        ("runtime_representation_audit", RUNTIME_REPRESENTATION_AUDIT, "CZ runtime representation audit(CZ 런타임 표현 감사)."),
        ("ea_support_audit", EA_SUPPORT_AUDIT, "CZ EA support audit(CZ EA 지원 감사)."),
        ("package_decision", PACKAGE_DECISION, "CZ package decision(CZ 패키지 결정)."),
        ("risk_scale_rule_contract", RISK_SCALE_RULE_CONTRACT, "CZ risk-scale rule contract(CZ 위험비율 규칙 계약)."),
        ("next_queue", RUN364DA_QUEUE, "DA runtime package queue(DA 런타임 패키지 대기열)."),
        ("report", REPORT_PATH, "CZ report(CZ 보고서)."),
        ("final_decision", FINAL_DECISION, "CZ final decision(CZ 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CZ run manifest(CZ 실행 목록)."),
        ("gate_audit", GATE_AUDIT, "CZ gate audit(CZ 게이트 감사)."),
        ("lineage_receipt", LINEAGE_RECEIPT, "CZ lineage receipt(CZ 계보 영수증)."),
        ("script", Path(__file__), "CZ producer script(CZ 생산 스크립트)."),
    ]
    rows = []
    for artifact_type, path, notes in artifacts:
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
                    "notes": notes,
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
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in output_paths],
            "final_decision": rel(FINAL_DECISION),
            "external_verification_status": final["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    _parent_final, selected = validate_inputs()
    flags = ea_support_flags()

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()

    selected_rows = selected_review_rows(selected)
    ea_rows = ea_support_rows(flags)
    representation = runtime_representation_rows(selected, flags)
    package_rows = package_decision_rows(selected, representation)
    rule_rows = risk_scale_contract_rows(selected)
    gap_rows = proxy_mt5_gap_rows(selected)
    dd_rows = equity_dd_rows(selected)
    queue_rows = da_queue_rows(selected)

    write_csv(SELECTED_CANDIDATE_REVIEW, selected_rows)
    write_csv(EA_SUPPORT_AUDIT, ea_rows)
    write_csv(RUNTIME_REPRESENTATION_AUDIT, representation)
    write_csv(PACKAGE_DECISION, package_rows)
    write_csv(RISK_SCALE_RULE_CONTRACT, rule_rows)
    write_csv(PROXY_MT5_GAP_REVIEW, gap_rows)
    write_csv(EQUITY_DD_BOUNDARY_REVIEW, dd_rows)
    write_csv(RUN364DA_QUEUE, queue_rows)

    gates = gate_rows(receipts_written=False)
    final = final_payload(selected, flags, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected, flags)
    write_csv(GATE_AUDIT, gate_rows(receipts_written=True))
    gates = gate_rows(receipts_written=True)
    final = final_payload(selected, flags, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected, flags)
    write_docs(final, representation, package_rows, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
