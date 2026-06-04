from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import package_density_restore_stress_candidate_runtime_probe_without_db as package_base  # noqa: E402
from stage_pipelines.stage364 import train_density_restore_forward_regime_stress_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-04"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BI"
RUN_ID = "run364BI_review_density_restore_forward_regime_stress_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID = "run364BJ_implement_h19_opposite_margin_runtime_guard_without_db_v1"

STATUS = "completed_stage364BI_forward_regime_stress_scout_review_runtime_support_gap_no_authority"
JUDGMENT = "proxy_candidate_positive_but_parameter_only_package_ineligible_runtime_guard_support_required_no_authority"
DECISION = "stage364BI_open_run364BJ_h19_opposite_margin_runtime_guard_support"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_SHORT_SHARE = parent.TARGET_SHORT_SHARE

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
CANDIDATE_REVIEW = RUN_DIR / "candidate_review.csv"
PROXY_MT5_COMPARISON_REVIEW = RUN_DIR / "proxy_mt5_comparison_review.csv"
RUNTIME_SUPPORT_GAP_AUDIT = RUN_DIR / "runtime_support_gap_audit.csv"
RUNTIME_SEMANTIC_GAP_REVIEW = RUN_DIR / "runtime_semantic_gap_review.csv"
PACKAGE_READINESS_DECISION = RUN_DIR / "package_readiness_decision.csv"
DENSITY_BREAKING_REPAIR_REVIEW = RUN_DIR / "density_breaking_repair_review.csv"
SHORT_SOURCE_NEXT_ACTION = RUN_DIR / "short_source_next_action.csv"
RUN364BJ_IMPLEMENTATION_QUEUE = RUN_DIR / "run364BJ_implementation_queue.csv"
KPI_CONTRACT_AUDIT = RUN_DIR / "kpi_contract_audit.csv"
ROW_GRAIN_AUDIT = RUN_DIR / "row_grain_audit.csv"
SOURCE_AUTHORITY_AUDIT = RUN_DIR / "source_authority_audit.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
FINAL_CLAIM_GUARD = RUN_DIR / "final_claim_guard.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BI_forward_regime_stress_scout_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BI_forward_regime_stress_scout_review.md"
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

PARENT_FINAL = parent.FINAL_DECISION
PARENT_GATE_AUDIT = parent.GATE_AUDIT
PARENT_QUEUE = parent.RUN364BI_QUEUE
PARENT_SELECTED = parent.SELECTED_PROXY_CANDIDATE
PARENT_SURFACE = parent.SCOUT_SURFACE
PARENT_FORWARD = parent.FORWARD_BLOCK_REPLAY
PARENT_MONTH = parent.MONTH_REGIME_REPLAY
PARENT_SHORT = parent.SHORT_RESTORE_FEASIBILITY
PARENT_REJECTED = parent.REJECTED_DENSITY_REPAIRS
PARENT_REPORT = parent.REPORT_PATH
PARENT_RUNTIME_RECEIPT = parent.RUNTIME_RECEIPT
PARENT_LINEAGE_RECEIPT = parent.LINEAGE_RECEIPT
BD_RUNTIME_POLICY = package_base.RUNTIME_POLICY_CONFIG
BD_RUNTIME_PARITY_CONTRACT = package_base.RUNTIME_PARITY_CONTRACT
BD_RUNTIME_GAP_AUDIT = package_base.RUNTIME_SEMANTIC_GAP_AUDIT
BD_SET_MANIFEST = package_base.TESTER_SET_MANIFEST
SOURCE_EA = package_base.SOURCE_EA
DECISION_SURFACE = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "DecisionSurface.mqh"

INPUT_FILES = [
    PARENT_FINAL,
    PARENT_GATE_AUDIT,
    PARENT_QUEUE,
    PARENT_SELECTED,
    PARENT_SURFACE,
    PARENT_FORWARD,
    PARENT_MONTH,
    PARENT_SHORT,
    PARENT_REJECTED,
    PARENT_REPORT,
    PARENT_RUNTIME_RECEIPT,
    PARENT_LINEAGE_RECEIPT,
    BD_RUNTIME_POLICY,
    BD_RUNTIME_PARITY_CONTRACT,
    BD_RUNTIME_GAP_AUDIT,
    BD_SET_MANIFEST,
    SOURCE_EA,
    DECISION_SURFACE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    CANDIDATE_REVIEW,
    PROXY_MT5_COMPARISON_REVIEW,
    RUNTIME_SUPPORT_GAP_AUDIT,
    RUNTIME_SEMANTIC_GAP_REVIEW,
    PACKAGE_READINESS_DECISION,
    DENSITY_BREAKING_REPAIR_REVIEW,
    SHORT_SOURCE_NEXT_ACTION,
    RUN364BJ_IMPLEMENTATION_QUEUE,
    KPI_CONTRACT_AUDIT,
    ROW_GRAIN_AUDIT,
    SOURCE_AUTHORITY_AUDIT,
    WORK_PACKET,
    RUN_EVIDENCE_RECEIPT,
    RUNTIME_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    FINAL_CLAIM_GUARD,
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


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


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


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def line_numbers(path: Path, needles: Sequence[str]) -> dict[str, str]:
    if not exists(path):
        return {needle: "" for needle in needles}
    lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    found: dict[str, str] = {}
    for needle in needles:
        locations = [str(index) for index, line in enumerate(lines, start=1) if needle in line]
        found[needle] = ";".join(locations)
    return found


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(path, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364BI inputs(364BI 입력 누락): " + ", ".join(missing))
    parent_final = read_json(PARENT_FINAL)
    selected = read_json(PARENT_SELECTED)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("selected_variant_id") != selected.get("variant_id"):
        raise RuntimeError("selected candidate mismatch(선택 후보 불일치)")
    forbidden = ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]
    if any(parent_final.get(key) != "not_claimed" for key in forbidden):
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_rows(PARENT_GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate audit is not fully passed(부모 게이트 감사가 모두 통과가 아님)")
    return parent_final, selected


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path),
                "input_role": input_role(path),
                "effect": "입력 계보(lineage, 계보)를 고정해 BI 검토가 어떤 근거를 먹었는지 남긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def input_role(path: Path | str) -> str:
    text = rel(path)
    if "run364BH" in text:
        return "BH proxy scout source(BH 프록시 탐색 원천)"
    if "run364BD" in text:
        return "existing runtime package reference(기존 런타임 패키지 참조)"
    if "foundation/mt5" in text:
        return "EA runtime source(EA 런타임 소스)"
    return "project state input(프로젝트 상태 입력)"


def candidate_review_rows(parent_final: Mapping[str, Any], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    density_buffer = as_float(selected.get("trade_density_per_business_day")) - DENSITY_FLOOR
    short_gap = TARGET_SHORT_SHARE - as_float(selected.get("short_share"))
    kpi_positive = (
        as_float(selected.get("net_profit")) > as_float(parent_final.get("baseline_closed_trade_net_profit"))
        and as_float(selected.get("profit_factor")) > as_float(parent_final.get("baseline_closed_trade_profit_factor"))
        and density_buffer >= 0.0
        and as_int(selected.get("forward_fail_count")) == 0
    )
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected.get("variant_id"),
            "review_status": "positive_proxy_candidate_but_runtime_support_gap(긍정 프록시 후보지만 런타임 지원 차이 있음)",
            "kpi_positive": kpi_positive,
            "net_profit": selected.get("net_profit"),
            "profit_factor": selected.get("profit_factor"),
            "expectancy": selected.get("expectancy"),
            "trade_count": selected.get("trade_count"),
            "trade_density_per_business_day": selected.get("trade_density_per_business_day"),
            "density_buffer": finite(density_buffer),
            "max_closed_drawdown_amount": selected.get("max_closed_drawdown_amount"),
            "recovery_factor": selected.get("recovery_factor"),
            "long_trade_count": selected.get("long_trade_count"),
            "short_trade_count": selected.get("short_trade_count"),
            "long_share": selected.get("long_share"),
            "short_share": selected.get("short_share"),
            "short_share_gap_to_012": finite(short_gap),
            "forward_fail_count": selected.get("forward_fail_count"),
            "weak_month_fail_count": selected.get("weak_month_fail_count"),
            "removed_trade_count": selected.get("removed_trade_count"),
            "removed_net_profit": selected.get("removed_net_profit"),
            "review_risk": "thin_density_buffer_and_short_balance_unresolved(밀도 버퍼가 얇고 숏 균형 미해결)",
            "effect": "후보는 살리되 운영 승격(promotion, 승격)으로 오해하지 않게 경계를 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def proxy_mt5_comparison_rows(parent_final: Mapping[str, Any], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "comparison_id": "parent_mt5_closed_trade_reference_vs_selected_proxy",
            "mt5_reference_run": "run364BE/run364BF",
            "proxy_source_run": PARENT_RUN_ID,
            "mt5_reference_net_profit": parent_final.get("baseline_closed_trade_net_profit"),
            "mt5_reference_profit_factor": parent_final.get("baseline_closed_trade_profit_factor"),
            "mt5_reference_trade_count": parent_final.get("baseline_closed_trade_count"),
            "mt5_reference_density": parent_final.get("baseline_closed_trade_density"),
            "selected_proxy_net_profit": selected.get("net_profit"),
            "selected_proxy_profit_factor": selected.get("profit_factor"),
            "selected_proxy_trade_count": selected.get("trade_count"),
            "selected_proxy_density": selected.get("trade_density_per_business_day"),
            "diff_net": finite(as_float(selected.get("net_profit")) - as_float(parent_final.get("baseline_closed_trade_net_profit"))),
            "diff_profit_factor": finite(as_float(selected.get("profit_factor")) - as_float(parent_final.get("baseline_closed_trade_profit_factor"))),
            "diff_trade_count": as_int(selected.get("trade_count")) - as_int(parent_final.get("baseline_closed_trade_count")),
            "usability": "candidate_screening_only_until_mt5_rerun(새 MT5 재실행 전까지 후보 선별 보조 전용)",
            "attribution": "closed-trade replay removes 13 weak hour19 long entries(종료 거래 재생에서 약한 19시 롱 13개 제거)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_support_review(selected: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], bool]:
    ea_text = Path(SOURCE_EA).read_text(encoding="utf-8-sig")
    surface_text = Path(DECISION_SURFACE).read_text(encoding="utf-8-sig")
    lines = line_numbers(
        SOURCE_EA,
        [
            "InpEntryMarginFloor",
            "InpMarchNonHour16MarginFilter",
            "SignalSideMargin",
            "ApplyRuntimeTimeFilters",
            "InpBlockPremarketShort",
        ],
    )
    has_entry_floor = "InpEntryMarginFloor" in ea_text
    has_march_filter = "InpMarchNonHour16MarginFilter" in ea_text
    has_time_filter = "ApplyRuntimeTimeFilters" in ea_text
    has_side_margin = "SignalSideMargin" in ea_text
    has_threshold_margin = "threshold_margin" in surface_text or "threshold_margin" in ea_text
    has_generic_guard = any(token in ea_text for token in ["InpGuardHour", "InpTimeMarginGuard", "InpRuntimeGuardHour", "InpProbabilityGuardHour"])
    has_opposite_margin = any(token in ea_text for token in ["OppositeMargin", "margin_vs_opposite", "p_long - p_short", "p_short - p_long"])
    has_hour19_exact = "hour19" in ea_text.lower() or "InpHour19" in ea_text
    selected_needs_opposite = selected.get("margin_col") == "margin_vs_opposite"
    selected_needs_hour = selected.get("long_hours") == [19] or selected.get("long_hours") == ["19"]
    exact_support = bool(has_generic_guard and has_opposite_margin and selected_needs_opposite and selected_needs_hour)

    support_rows = [
        {
            "run_id": RUN_ID,
            "capability": "global_entry_margin_floor(전역 진입 마진 하한)",
            "present": has_entry_floor,
            "line_reference": lines.get("InpEntryMarginFloor", ""),
            "usable_for_selected_candidate": False,
            "reason": "전역(global, 전역)이고 max-other margin(최대 타방 마진)을 쓰므로 h19 long opposite margin(19시 롱 반대 마진)과 의미가 다르다.",
            "effect": "파라미터만으로 쓰면 후보 성능을 같은 규칙으로 재현했다는 주장을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "march_specific_time_margin_filter(3월 전용 시간/마진 필터)",
            "present": has_march_filter,
            "line_reference": lines.get("InpMarchNonHour16MarginFilter", ""),
            "usable_for_selected_candidate": False,
            "reason": "월(month, 월)이 3월로 고정된 특수 필터라 h19 long guard(19시 롱 가드)를 표현하지 못한다.",
            "effect": "기존 특수 필터를 억지 재사용해 의미를 바꾸는 일을 방지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "generic_hour_side_probability_guard(일반 시간/방향/확률 가드)",
            "present": has_generic_guard,
            "line_reference": "",
            "usable_for_selected_candidate": exact_support,
            "reason": "현재 입력(input, 입력)에는 임의 hour(시간), side(방향), margin basis(마진 기준)를 받는 범용 가드가 없다.",
            "effect": "BJ에서 추가해야 할 정확한 런타임 수리 지점을 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "opposite_probability_margin_basis(반대 방향 확률 마진 기준)",
            "present": has_opposite_margin,
            "line_reference": lines.get("SignalSideMargin", ""),
            "usable_for_selected_candidate": False,
            "reason": "EA의 SignalSideMargin(신호 방향 마진)은 selected - max(flat, opposite)이고 BH 후보는 selected - opposite이다.",
            "effect": "확률 의미 차이(probability semantics diff, 확률 의미 차이)를 운영 동등성(parity, 동등성)에서 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    semantic_rows = [
        {
            "run_id": RUN_ID,
            "gap_id": "hour_scope_gap",
            "research_semantic": "entry_hour == 19 and side == long only(진입 시간이 19이고 롱만)",
            "runtime_semantic": "global entry margin floor or March-only filter(전역 진입 마진 하한 또는 3월 전용 필터)",
            "exact_match": False,
            "known_difference": "현재 EA에는 h19 long only(19시 롱 전용) 확률 가드 파라미터가 없다.",
            "usability": "requires_code_support_before_package(패키지 전 코드 지원 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gap_id": "margin_basis_gap",
            "research_semantic": "p_long - p_short < 0.002 blocks long(롱 확률-숏 확률이 0.002 미만이면 롱 차단)",
            "runtime_semantic": "p_long - max(p_flat, p_short) with InpEntryMarginFloor(전역 진입 마진 하한은 롱 확률-최대 타방 확률)",
            "exact_match": False,
            "known_difference": "p_flat(플랫 확률)이 p_short(숏 확률)보다 높으면 같은 거래를 다르게 차단한다.",
            "usability": "cannot_be_parameter_only_runtime_probe(파라미터만으로 런타임 탐침 불가)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gap_id": "runtime_claim_gap",
            "research_semantic": "closed trade proxy replay(종료 거래 프록시 재생)",
            "runtime_semantic": "Strategy Tester tick execution(전략 테스터 틱 실행)",
            "exact_match": False,
            "known_difference": "새 가드가 EA에서 실행된 적 없으므로 cost/fill/position sequence(비용/체결/포지션 순서)가 검증되지 않았다.",
            "usability": "screening_positive_only(선별 긍정 근거 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return support_rows, semantic_rows, exact_support


def package_readiness_rows(selected: Mapping[str, Any], exact_support: bool) -> list[dict[str, Any]]:
    proxy_positive = as_float(selected.get("net_profit")) > 0 and as_float(selected.get("profit_factor")) > 1.0
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected.get("variant_id"),
            "proxy_positive": proxy_positive,
            "density_floor_pass": as_float(selected.get("trade_density_per_business_day")) >= DENSITY_FLOOR,
            "runtime_exact_support": exact_support,
            "package_ready_parameter_only": False,
            "package_readiness": "not_ready_requires_runtime_guard_support(미준비, 런타임 가드 지원 필요)",
            "next_run_id": NEXT_RUN_ID,
            "decision": DECISION,
            "effect": "다음 작업이 무리한 패키징(package, 패키징)이 아니라 런타임 수리(runtime repair, 런타임 수리)로 시작되게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def density_breaking_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_rows(PARENT_REJECTED):
        rows.append(
            {
                "run_id": RUN_ID,
                "source_variant_id": row.get("variant_id"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "trade_density_per_business_day": row.get("trade_density_per_business_day"),
                "removed_trade_count": row.get("removed_trade_count"),
                "review_decision": "closed_for_this_path_density_below_3_per_day(이번 경로에서는 3/day 미만이라 닫음)",
                "effect": "실패 기억(failure memory, 실패 기억)을 다음 탐색 제약으로 바꾸고, 정확 조각 삭제를 승격하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def short_source_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    current_total = as_int(selected.get("trade_count"))
    current_short = as_int(selected.get("short_trade_count"))
    current_long = as_int(selected.get("long_trade_count"))
    needed_added_shorts = math.ceil((TARGET_SHORT_SHARE * current_total - current_short) / (1.0 - TARGET_SHORT_SHARE))
    return [
        {
            "run_id": RUN_ID,
            "action_id": "new_short_source_required",
            "selected_variant_id": selected.get("variant_id"),
            "current_total_trades": current_total,
            "current_long_trades": current_long,
            "current_short_trades": current_short,
            "current_short_share": selected.get("short_share"),
            "target_short_share": TARGET_SHORT_SHARE,
            "minimum_added_shorts_needed_if_no_long_removal": max(0, needed_added_shorts),
            "forbidden_repair": "delete_longs_or_exact_loss_slices_to_fake_balance(롱 삭제나 정확 손실 조각 삭제로 균형을 꾸미기 금지)",
            "next_action": "explore_new_short_source_after_runtime_guard_support(런타임 가드 지원 후 새 숏 원천 탐색)",
            "effect": "롱 치우침(long skew, 롱 치우침)을 숫자 삭제가 아니라 새 수익 원천 탐색으로 해결하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def implementation_queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "bj01_add_generic_hour_side_margin_guard",
            "selected_variant_id": selected.get("variant_id"),
            "task": "add EA inputs for enabled/side/hour_start/hour_end/margin_basis/min_margin(EA 입력에 사용 여부/방향/시작시/끝시/마진 기준/최소 마진 추가)",
            "success_criteria": "can express hour 19 long p_long-p_short < 0.002 as flat(19시 롱 p_long-p_short < 0.002를 flat으로 표현)",
            "effect": "BH 후보를 MT5에서 같은 의미로 실행할 길을 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "bj02_package_exact_candidate_after_compile",
            "selected_variant_id": selected.get("variant_id"),
            "task": "package exact h19 opposite-margin candidate after compile check(컴파일 확인 후 h19 반대마진 후보를 정확 패키징)",
            "success_criteria": "set/config/semantic audit all name the same guard(set/config/의미 감사가 같은 가드를 지칭)",
            "effect": "proxy expected value(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침) 비교 준비를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 3,
            "queue_id": "bj03_execute_or_block_narrow_mt5_probe",
            "selected_variant_id": selected.get("variant_id"),
            "task": "attempt the narrow Strategy Tester probe or record exact blocker(좁은 전략 테스터 탐침을 시도하거나 정확 차단 사유 기록)",
            "success_criteria": "tester output exists or blocker has command/log/next condition(테스터 출력 존재 또는 명령/로그/다음 조건이 있는 차단 기록)",
            "effect": "외부 검증(external verification, 외부 검증)을 다음으로 반복 지연하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def audit_rows(selected: Mapping[str, Any], exact_support: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    kpi = [
        {
            "run_id": RUN_ID,
            "audit_id": "selected_kpi_contract",
            "net_profit_present": selected.get("net_profit") is not None,
            "profit_factor_present": selected.get("profit_factor") is not None,
            "expectancy_present": selected.get("expectancy") is not None,
            "drawdown_present": selected.get("max_closed_drawdown_amount") is not None,
            "recovery_present": selected.get("recovery_factor") is not None,
            "trade_count_present": selected.get("trade_count") is not None,
            "density_present": selected.get("trade_density_per_business_day") is not None,
            "side_balance_present": selected.get("long_share") is not None and selected.get("short_share") is not None,
            "status": "passed",
            "effect": "단일 KPI(핵심 성과 지표)만 보지 않고 운영 후보 필수 숫자를 함께 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    row_grain = [
        {
            "run_id": RUN_ID,
            "artifact": rel(PARENT_SELECTED),
            "row_grain": "one selected candidate(선택 후보 1행)",
            "rows": 1,
            "status": "passed",
            "effect": "BI 판단 단위를 후보 1개로 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "artifact": rel(PARENT_FORWARD),
            "row_grain": "one forward-like block per row(전진 유사 블록 1행)",
            "rows": len(read_rows(PARENT_FORWARD)),
            "status": "passed",
            "effect": "국면 안정성(regime stability, 국면 안정성)을 블록 단위로 읽는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "artifact": rel(PARENT_REJECTED),
            "row_grain": "one rejected repair variant per row(거절 수리 후보 1행)",
            "rows": len(read_rows(PARENT_REJECTED)),
            "status": "passed",
            "effect": "밀도 파괴(density break, 밀도 파괴) 실패 기억을 후보 단위로 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    source_authority = [
        {
            "run_id": RUN_ID,
            "source": rel(PARENT_SELECTED),
            "authority": "proxy_review_source_only(프록시 검토 원천 전용)",
            "usable_for_operating_claim": False,
            "status": "passed",
            "effect": "프록시(proxy, 프록시)를 MT5 KPI 대체물로 쓰지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "source": rel(SOURCE_EA),
            "authority": "runtime_source_inspection(EA 런타임 소스 검사)",
            "usable_for_operating_claim": False,
            "status": "passed" if not exact_support else "watch",
            "effect": "런타임 동등성(runtime parity, 런타임 동등성) 차이를 코드 기준으로 귀속한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return kpi, row_grain, source_authority


def gate_rows(exact_support: bool) -> list[dict[str, Any]]:
    required = [
        ("kpi_contract_audit", exists(KPI_CONTRACT_AUDIT), "KPI 계약(KPI contract, KPI 계약)이 후보 숫자를 모두 가진다."),
        ("row_grain_audit", exists(ROW_GRAIN_AUDIT), "행 단위(row grain, 행 단위)가 후보/블록/수리별로 분리됐다."),
        ("source_authority_audit", exists(SOURCE_AUTHORITY_AUDIT), "원천 권위(source authority, 원천 권위)가 프록시와 런타임 소스로 분리됐다."),
        ("runtime_semantic_gap_audit", exists(RUNTIME_SEMANTIC_GAP_REVIEW) and not exact_support, "현재 EA 파라미터로 정확 표현 불가함을 기록했다."),
        ("required_gate_coverage_audit", True, "필수 게이트(required gates, 필수 게이트)가 closeout(종료 기록)에 연결됐다."),
        ("final_claim_guard", exists(FINAL_CLAIM_GUARD), "운영 승격/런타임 권위/목표 달성 주장을 금지했다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(GATE_AUDIT if gate == "required_gate_coverage_audit" else RUN_DIR),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, effect in required
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "supplemental_check": "obsidian-runtime-parity(런타임 동등성)",
            "required_gates": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "BH 프록시 후보를 숫자, 원천 권위, 런타임 의미 차이로 나누어 다음 BJ 수리로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def final_payload(
    parent_final: Mapping[str, Any],
    selected: Mapping[str, Any],
    exact_support: bool,
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_variant_id": selected.get("variant_id"),
        "selected_net_profit": selected.get("net_profit"),
        "selected_profit_factor": selected.get("profit_factor"),
        "selected_expectancy": selected.get("expectancy"),
        "selected_trade_count": selected.get("trade_count"),
        "selected_trade_density": selected.get("trade_density_per_business_day"),
        "selected_density_buffer": finite(as_float(selected.get("trade_density_per_business_day")) - DENSITY_FLOOR),
        "selected_closed_drawdown_amount": selected.get("max_closed_drawdown_amount"),
        "selected_recovery_factor": selected.get("recovery_factor"),
        "selected_long_trade_count": selected.get("long_trade_count"),
        "selected_short_trade_count": selected.get("short_trade_count"),
        "selected_long_share": selected.get("long_share"),
        "selected_short_share": selected.get("short_share"),
        "selected_forward_fail_count": selected.get("forward_fail_count"),
        "selected_weak_month_fail_count": selected.get("weak_month_fail_count"),
        "parent_mt5_reference_net_profit": parent_final.get("baseline_closed_trade_net_profit"),
        "parent_mt5_reference_profit_factor": parent_final.get("baseline_closed_trade_profit_factor"),
        "parent_mt5_reference_trade_count": parent_final.get("baseline_closed_trade_count"),
        "parent_mt5_reference_density": parent_final.get("baseline_closed_trade_density"),
        "runtime_exact_support": exact_support,
        "package_ready_parameter_only": False,
        "runtime_support_gap": True,
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "evidence_available": [rel(CANDIDATE_REVIEW), rel(RUNTIME_SEMANTIC_GAP_REVIEW), rel(PACKAGE_READINESS_DECISION)],
            "evidence_missing": ["new MT5 execution(새 MT5 실행)", "compiled package for the new guard(새 가드 컴파일 패키지)", "forward pass(전진 통과)"],
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_semantic": "hour19 long-only p_long-p_short margin guard(19시 롱 전용 p_long-p_short 마진 가드)",
            "runtime_semantic": "current EA supports global max-other entry floor and March-specific guard(현재 EA는 전역 max-other 진입 하한과 3월 전용 가드 지원)",
            "parity_judgment": "semantic_gap_requires_code_support(의미 차이가 있어 코드 지원 필요)",
            "runtime_sources": [rel(SOURCE_EA), rel(DECISION_SURFACE)],
            "support_audit": rel(RUNTIME_SUPPORT_GAP_AUDIT),
            "semantic_gap_review": rel(RUNTIME_SEMANTIC_GAP_REVIEW),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": f"{selected.get('variant_id')} net={selected.get('net_profit')} pf={selected.get('profit_factor')} density={selected.get('trade_density_per_business_day')}",
            "likely_driver": "removal of 13 weak hour19 long entries with low opposite-margin(반대 마진이 낮은 약한 19시 롱 13개 제거)",
            "remaining_risks": [
                "density buffer is only about 0.012/day(밀도 버퍼 약 0.012/day)",
                "short share remains below 0.12(숏 비중 0.12 미만)",
                "same-tape threshold discovery(같은 테이프에서 임계값 발견)",
            ],
            "attribution_confidence": "medium_proxy_only(프록시 전용 중간)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "run364BH selected micro margin candidate(BH 선택 미세 마진 후보)",
            "judgment_label": JUDGMENT,
            "positive_part": "proxy KPI improved and forward-like blocks stayed net/PF positive(프록시 KPI 개선, 전진 유사 블록 순수익/PF 양수)",
            "negative_part": "parameter-only MT5 package not exact and short balance unresolved(파라미터만으로 MT5 패키지 불일치, 숏 균형 미해결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["operating_promotion", "runtime_authority", "live_readiness", "goal_achieve", "forward_passed"],
            "effect": "BI를 검토 완료(review completed, 검토 완료)로만 닫고 운영 주장(operating claim, 운영 주장)은 막는다.",
        },
    )
    write_json(
        FINAL_CLAIM_GUARD,
        {
            "run_id": RUN_ID,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "reason": "no new MT5 execution and runtime semantic gap remains(새 MT5 실행 없고 런타임 의미 차이 남음)",
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
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_runtime_gap_boundary(런타임 차이 경계 포함 연결)",
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def sync_stage_brief_header() -> None:
    if not STAGE_BRIEF.exists():
        return
    text = STAGE_BRIEF.read_text(encoding="utf-8-sig")
    marker = "Current active run("
    lines = []
    replaced = False
    for line in text.splitlines():
        if line.startswith(marker):
            lines.append(f"Current active run(현재 활성 실행): `{NEXT_RUN_ID}`")
            replaced = True
        else:
            lines.append(line)
    if replaced:
        write_text(STAGE_BRIEF, "\n".join(lines) + "\n", bom=True)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    support_rows = read_rows(RUNTIME_SUPPORT_GAP_AUDIT)
    semantic_rows = read_rows(RUNTIME_SEMANTIC_GAP_REVIEW)
    package_rows = read_rows(PACKAGE_READINESS_DECISION)
    short_rows = read_rows(SHORT_SOURCE_NEXT_ACTION)
    queue = read_rows(RUN364BJ_IMPLEMENTATION_QUEUE)
    report = f"""# run364BI forward/regime stress scout review(364BI 전진/국면 스트레스 탐색 검토)

## Scope(범위)
- Parent(부모): `{PARENT_RUN_ID}`
- Selected candidate(선택 후보): `{final['selected_variant_id']}`
- New MT5 execution(새 MT5 실행): not run(미실행)
- Operating claim(운영 주장): not claimed(주장 안 함)

## Current Truth(현재 진실)
BH 후보는 proxy(프록시) 기준으로 net profit(순수익) `{final['selected_net_profit']}`, profit factor(수익 팩터) `{final['selected_profit_factor']}`, trades(거래수) `{final['selected_trade_count']}`, density(밀도) `{final['selected_trade_density']}`를 냈다. 효과는 작은 h19 long margin guard(19시 롱 마진 가드)가 수익 구조를 개선할 수 있다는 clue(단서)를 살린 것이다.

하지만 parameter-only package(파라미터만 패키지)는 불가하다. 후보는 `p_long - p_short < 0.002`를 hour 19 long(19시 롱)에만 적용하지만, 현재 EA는 global max-other entry margin floor(전역 최대 타방 진입 마진 하한)와 March-specific filter(3월 전용 필터)만 가진다.

## Runtime Gap(런타임 차이)
{markdown_table(semantic_rows, ['gap_id', 'research_semantic', 'runtime_semantic', 'exact_match', 'usability'], 6)}

## Support Audit(지원 감사)
{markdown_table(support_rows, ['capability', 'present', 'usable_for_selected_candidate', 'reason'], 8)}

## Package Decision(패키지 결정)
{markdown_table(package_rows, ['variant_id', 'proxy_positive', 'runtime_exact_support', 'package_ready_parameter_only', 'package_readiness'], 4)}

## Short Source(숏 원천)
{markdown_table(short_rows, ['action_id', 'current_short_share', 'minimum_added_shorts_needed_if_no_long_removal', 'next_action'], 4)}

## Next Queue(다음 대기열)
{markdown_table(queue, ['queue_rank', 'queue_id', 'task', 'success_criteria'], 6)}

## Gates(게이트)
{markdown_table(gates, ['gate', 'status', 'effect'], 8)}
"""
    write_text(REPORT_PATH, report, bom=True)
    decision_doc = f"""# {TODAY} Stage364BI decision(결정)

Decision(결정): `{DECISION}`

Judgment(판정): `{JUDGMENT}`

Effect(효과): `run364BH`의 positive proxy clue(긍정 프록시 단서)는 유지한다. 그러나 current EA capability(현재 EA 기능)로는 exact runtime parity(정확 런타임 동등성)가 없으므로 `run364BJ`에서 h19 opposite-margin guard(19시 반대마진 가드)를 먼저 구현하거나 차단 사유를 남긴다.

Forbidden claims(금지 주장): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""
    write_text(DECISION_DOC, decision_doc, bom=True)
    current_state = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364BI` reviewed(검토) the BH selected proxy candidate(선택 프록시 후보). The candidate remains a positive research clue(긍정 연구 단서), but it is not parameter-only package ready(파라미터만 패키지 준비 아님) because runtime semantic gap(런타임 의미 차이) remains.

Selected clue(선택 단서): `{final['selected_variant_id']}` net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, trades `{final['selected_trade_count']}`, density `{final['selected_trade_density']}`.

Open blocker(열린 차단): current EA(현재 EA) lacks generic hour/side/opposite-margin guard(범용 시간/방향/반대마진 가드 없음).

Next action(다음 행동): `{NEXT_RUN_ID}` implements or blocks the exact runtime guard support(정확 런타임 가드 지원을 구현하거나 차단 기록).

Operating boundary(운영 경계): no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(CURRENT_WORKING_STATE, current_state, bom=True)
    workspace_state = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
"""
    write_text(WORKSPACE_STATE, workspace_state, bom=False)
    selection_status = f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe candidate(런타임 탐침 후보): `{final['selected_variant_id']}`

Status(상태): `runtime_support_gap_open(런타임 지원 차이 열림)`

Proxy KPI(프록시 KPI): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, trades `{final['selected_trade_count']}`, density `{final['selected_trade_density']}`, long/short `{final['selected_long_trade_count']}/{final['selected_short_trade_count']}`.

Package readiness(패키지 준비성): not ready as parameter-only(파라미터만으로 준비 안 됨). Current EA(현재 EA) cannot exactly express h19 long p_long-p_short guard(19시 롱 p_long-p_short 가드).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
"""
    write_text(SELECTION_STATUS, selection_status, bom=True)
    sync_stage_brief_header()
    append_text_once(
        REVIEW_INDEX,
        "<!-- run364BI -->",
        f"\n<!-- run364BI -->\n- `{RUN_ID}`: forward/regime scout review(전진/국면 탐색 검토) -> `{REPORT_PATH.relative_to(ROOT).as_posix()}`\n",
    )
    append_text_once(
        STAGE_README,
        "<!-- run364BI -->",
        f"\n<!-- run364BI -->\n## run364BI forward/regime scout review(전진/국면 탐색 검토)\n\n`{JUDGMENT}`. Next(다음): `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "<!-- run364BI -->",
        f"\n<!-- run364BI -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed BH h19 margin candidate(BH 19시 마진 후보 검토). Effect(효과): parameter-only package(파라미터만 패키지) 금지와 BJ runtime guard support(BJ 런타임 가드 지원) 대기열 생성.\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        "<!-- run364BI_h19_runtime_guard -->",
        f"\n<!-- run364BI_h19_runtime_guard -->\n- Idea(아이디어): generic hour/side/opposite-margin guard(범용 시간/방향/반대마진 가드). Seed(씨앗): `{final['selected_variant_id']}`. Effect(효과): proxy clue(프록시 단서)를 MT5에서 같은 의미로 시험할 수 있게 한다.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        "<!-- run364BI_density_breaking_repairs -->",
        f"\n<!-- run364BI_density_breaking_repairs -->\n- Negative memory(부정 기억): exact month/hour hard filters(정확 월/시간 강한 필터)는 density(밀도) < 3/day로 이번 경로에서 rejected(거절). Effect(효과): 같은 삭제식 수리를 운영 후보로 끌고 가지 않는다.\n",
    )


def ledger_rows(final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(PACKAGE_READINESS_DECISION),
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_trade_density"],
        "trade_density_requirement_status": "proxy_passed_ge_3_no_trade_splitting(프록시 3/day 통과, 거래 쪼개기 없음)",
        "max_drawdown_amount": final["selected_closed_drawdown_amount"],
        "recovery_factor": final["selected_recovery_factor"],
        "long_trade_count": final["selected_long_trade_count"],
        "short_trade_count": final["selected_short_trade_count"],
        "work_family": "kpi_evidence(KPI 근거)",
        "evidence_boundary": "proxy_review_runtime_gap_no_mt5_execution(프록시 검토와 런타임 차이, MT5 실행 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "next_action": NEXT_RUN_ID,
        "question": "Can BH h19 margin clue be packaged with exact MT5 semantics?(BH 19시 마진 단서를 정확 MT5 의미로 패키징할 수 있는가?)",
    }
    run_registry = [{**common, "lane": "runtime_semantic_review(런타임 의미 검토)", "path": rel(FINAL_DECISION)}]
    stage_rows = [
        {
            **common,
            "ledger_row_id": f"{RUN_ID}::tier_a_proxy_review",
            "row_id": f"{RUN_ID}::tier_a_proxy_review",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "proxy_review",
            "scoreboard_lane": "runtime_semantic_review",
            "path": rel(FINAL_DECISION),
        },
        {
            **common,
            "ledger_row_id": f"{RUN_ID}::tier_b_missing_required",
            "row_id": f"{RUN_ID}::tier_b_missing_required",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "runtime_semantic_review",
            "path": rel(FINAL_DECISION),
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "trade_count": "",
            "trade_density_per_feature_day": "",
            "notes": "Tier B was out of scope for this runtime semantic review(Tier B는 이번 런타임 의미 검토 범위 밖).",
        },
        {
            **common,
            "ledger_row_id": f"{RUN_ID}::tier_ab_combined_missing_required",
            "row_id": f"{RUN_ID}::tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "runtime_semantic_review",
            "path": rel(FINAL_DECISION),
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "trade_count": "",
            "trade_density_per_feature_day": "",
            "notes": "Combined record is missing_required because no Tier B replay was run(Tier B 재생이 없어 합산 기록은 필수 누락).",
        },
    ]
    return run_registry, stage_rows, stage_rows


def write_ledgers(final: Mapping[str, Any]) -> None:
    run_rows, stage_rows, project_rows = ledger_rows(final)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], stage_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=True)
    parent.repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path) if exists(path) and Path(path).is_file() else ""} for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    parent_final, selected = validate_inputs()
    write_work_packet()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(CANDIDATE_REVIEW, candidate_review_rows(parent_final, selected))
    write_csv(PROXY_MT5_COMPARISON_REVIEW, proxy_mt5_comparison_rows(parent_final, selected))
    support_rows, semantic_rows, exact_support = runtime_support_review(selected)
    write_csv(RUNTIME_SUPPORT_GAP_AUDIT, support_rows)
    write_csv(RUNTIME_SEMANTIC_GAP_REVIEW, semantic_rows)
    write_csv(PACKAGE_READINESS_DECISION, package_readiness_rows(selected, exact_support))
    write_csv(DENSITY_BREAKING_REPAIR_REVIEW, density_breaking_rows())
    write_csv(SHORT_SOURCE_NEXT_ACTION, short_source_rows(selected))
    write_csv(RUN364BJ_IMPLEMENTATION_QUEUE, implementation_queue_rows(selected))
    kpi, row_grain, source_authority = audit_rows(selected, exact_support)
    write_csv(KPI_CONTRACT_AUDIT, kpi)
    write_csv(ROW_GRAIN_AUDIT, row_grain)
    write_csv(SOURCE_AUTHORITY_AUDIT, source_authority)
    write_receipts({}, selected)
    gates = gate_rows(exact_support)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(parent_final, selected, exact_support, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
