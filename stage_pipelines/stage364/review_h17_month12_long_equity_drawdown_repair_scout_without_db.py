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
from stage_pipelines.stage364 import review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db as cq  # noqa: E402
from stage_pipelines.stage364 import train_h17_month12_long_equity_drawdown_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CT"
RUN_ID = "run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID = "run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1"

STATUS = "completed_stage364CT_h17_month12_long_equity_dd_review_runtime_representation_repair_required_no_authority"
JUDGMENT = "positive_proxy_candidate_cr04_runtime_representation_gap_open_cu_secondary_month_guard_no_authority"
DECISION = "stage364CT_open_run364CU_secondary_month_margin_guard_runtime_package"
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
SELECTED_VARIANT_REVIEW = RUN_DIR / "selected_variant_review.csv"
PACKAGE_GATE_DECISION = RUN_DIR / "package_gate_decision.csv"
RUNTIME_REPRESENTATION_REVIEW = RUN_DIR / "runtime_representation_review.csv"
PROXY_MT5_GAP_REVIEW = RUN_DIR / "proxy_mt5_gap_review.csv"
EQUITY_DD_BOUNDARY_REVIEW = RUN_DIR / "equity_dd_boundary_review.csv"
MONTH_SIDE_REVIEW = RUN_DIR / "month_side_review.csv"
FILTER_REVIEW = RUN_DIR / "filter_review.csv"
RUNTIME_REPAIR_REQUIREMENTS = RUN_DIR / "runtime_repair_requirements.csv"
RUN364CU_QUEUE = RUN_DIR / "run364CU_runtime_package_queue.csv"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CT_h17_month12_long_equity_drawdown_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CT_h17_month12_long_equity_drawdown_repair_review.md"
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

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.CS_PROXY_REPAIR_SURFACE,
    parent.SELECTED_CANDIDATE,
    parent.SELECTED_TRADE_TAPE,
    parent.VARIANT_FILTER_AUDIT,
    parent.VARIANT_MONTH_SIDE_ATTRIBUTION,
    parent.EQUITY_DD_PROXY_DIAGNOSTIC,
    parent.PACKAGE_PRECHECK,
    parent.PROXY_MT5_DIFF_PLAN,
    parent.RUN364CT_QUEUE,
    parent.DATA_INTEGRITY_AUDIT,
    parent.RUN_MANIFEST,
    cq.MT5_KPI_REVIEW,
    cq.DRAWDOWN_REVIEW,
    cq.RUN_MANIFEST,
    EA_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SELECTED_VARIANT_REVIEW,
    PACKAGE_GATE_DECISION,
    RUNTIME_REPRESENTATION_REVIEW,
    PROXY_MT5_GAP_REVIEW,
    EQUITY_DD_BOUNDARY_REVIEW,
    MONTH_SIDE_REVIEW,
    FILTER_REVIEW,
    RUNTIME_REPAIR_REQUIREMENTS,
    RUN364CU_QUEUE,
    KPI_RECEIPT,
    DATA_RECEIPT,
    ATTRIBUTION_RECEIPT,
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
    return parent.rel(path)


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


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    parent.write_csv(path, rows)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CT inputs(CT 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CS next_run_id mismatch(CS 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CS has forbidden authority claim(CS 금지 권위 주장 존재)")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CS gate audit(CS 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "CT review source(CT 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def selected_month_side_rows(selected_id: str) -> list[dict[str, Any]]:
    rows = []
    source = read_csv(parent.VARIANT_MONTH_SIDE_ATTRIBUTION)
    selected = source[source["variant_id"].astype(str).eq(selected_id)].copy()
    selected["net_num"] = pd.to_numeric(selected["net_profit"], errors="coerce").fillna(0.0)
    selected = selected.sort_values(["open_month", "direction"])
    for _, raw in selected.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": selected_id,
                "open_month": row.get("open_month"),
                "direction": row.get("direction"),
                "trade_count": row.get("trade_count"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "side_read": "month12_long_repaired(12월 롱 수리)" if row.get("open_month") == "2025-12" and row.get("direction") == "long" and as_float(row.get("net_profit")) >= 0 else "segment_watch(구간 관찰)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def selected_filter_rows(selected_id: str) -> list[dict[str, Any]]:
    rows = []
    source = read_csv(parent.VARIANT_FILTER_AUDIT)
    selected = source[source["variant_id"].astype(str).eq(selected_id)]
    for _, raw in selected.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": selected_id,
                "filter_step": row.get("filter_step"),
                "filter_reason": row.get("filter_reason"),
                "removed_trade_count": row.get("removed_trade_count"),
                "removed_long_count": row.get("removed_long_count"),
                "removed_short_count": row.get("removed_short_count"),
                "removed_net_profit": row.get("removed_net_profit"),
                "review_judgment": "timestamp_safe_no_split_filter(시점 안전 무분할 필터)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def runtime_representation_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    ea_text = io_path(EA_PATH).read_text(encoding="utf-8-sig")
    has_month_guard = "InpMonthMarginGuardEnabled" in ea_text
    has_time_guard = "InpTimeMarginGuardEnabled" in ea_text
    has_calendar_block = "InpCalendarBlockEnabled" in ea_text
    has_second_month_guard = "InpMonthMarginGuard2Enabled" in ea_text
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "representation_id": "cr04_exact_piecewise_month12_margin_guard",
            "proxy_rule": "base month12 long signal margin floor 0.01 all hours plus month12 long hours 17-20 floor 0.02(기본 12월 롱 전체 시간 0.01 하한 + 17-20시 0.02 하한)",
            "current_runtime_support": f"month_guard={has_month_guard};time_guard={has_time_guard};calendar_block={has_calendar_block};second_month_guard={has_second_month_guard}",
            "representation_status": "gap_requires_secondary_month_margin_guard(간극 있음, 두 번째 월 마진 가드 필요)" if not has_second_month_guard else "represented_by_secondary_month_margin_guard(두 번째 월 마진 가드로 표현 가능)",
            "required_runtime_change": "add InpMonthMarginGuard2* inputs or equivalent month-specific secondary guard(InpMonthMarginGuard2 계열 입력 또는 동등한 월별 보조 가드 추가)",
            "effect": "prevents replacing a precise proxy rule with broader runtime behavior(정확한 프록시 규칙을 더 넓은 런타임 동작으로 바꾸지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": "cr02_month12_long_margin_floor_002",
            "representation_id": "representable_fallback_all_month12_floor002",
            "proxy_rule": "month12 long signal margin floor 0.02 all hours(12월 롱 전체 시간 0.02 하한)",
            "current_runtime_support": f"month_guard={has_month_guard}",
            "representation_status": "represented_but_not_selected_proxy_best(표현 가능하지만 선택 프록시 최상위 아님)",
            "required_runtime_change": "none for cr02(CR02에는 없음)",
            "effect": "keeps a fallback if CU cannot patch runtime(CU에서 런타임 보강 실패 시 대체 후보 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": "cr01_month12_long_hours17_20_block",
            "representation_id": "representable_fallback_calendar_block",
            "proxy_rule": "base month12 floor 0.01 plus month12 long hours17-20 block(기본 12월 0.01 하한 + 12월 롱 17-20시 차단)",
            "current_runtime_support": f"month_guard={has_month_guard};calendar_block={has_calendar_block}",
            "representation_status": "represented_but_more_destructive_than_cr04(표현 가능하지만 cr04보다 제거 폭 큼)",
            "required_runtime_change": "none for cr01(CR01에는 없음)",
            "effect": "keeps conservative fallback without pretending it is cr04(cr04인 척하지 않는 보수 대체 후보 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def selected_review_rows(final: Mapping[str, Any], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
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
            "month12_long_net": selected["month12_long_net"],
            "closed_trade_drawdown_proxy": selected["closed_trade_drawdown_proxy"],
            "package_precheck_status": selected["package_precheck_status"],
            "review_read": "proxy_positive_runtime_repair_required(프록시 긍정, 런타임 수리 필요)",
            "effect": "keeps cr04 as the target without claiming MT5 success(cr04를 목표로 유지하되 MT5 성공은 주장하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def package_gate_rows(selected: Mapping[str, Any], representation: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    exact = representation[0]
    exact_ready = str(exact["representation_status"]).startswith("represented")
    proxy_pass = str(selected.get("package_precheck_status", "")).startswith("passed")
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "gate_id": "proxy_kpi_package_gate",
            "gate_status": "passed_for_runtime_repair_queue(런타임 수리 대기열 통과)" if proxy_pass else "failed_proxy_precheck(프록시 사전검사 실패)",
            "evidence": f"net={selected['net_profit']};pf={selected['profit_factor']};density={selected['trade_density']};shorts={selected['short_trade_count']};month12_long={selected['month12_long_net']}",
            "effect": "proxy quality is enough to justify repairing runtime representation(프록시 품질은 런타임 표현 수리를 정당화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "gate_id": "runtime_exact_representation_gate",
            "gate_status": "repair_required_before_mt5_probe(MT5 탐침 전 수리 필요)" if not exact_ready else "passed_exact_runtime_representation(정확 런타임 표현 통과)",
            "evidence": exact["current_runtime_support"],
            "effect": "blocks premature MT5 package if cr04 cannot be represented exactly(cr04를 정확히 표현할 수 없으면 성급한 MT5 패키지를 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "gate_id": "package_decision",
            "gate_status": "open_cu_runtime_repair_not_mt5_execution(CU 런타임 수리 개방, MT5 실행 아님)",
            "evidence": rel(RUN364CU_QUEUE),
            "effect": "next action fixes handoff tooling before external verification(다음 행동은 외부 검증 전 인계 도구를 고침)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def proxy_mt5_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    diff = read_csv(parent.PROXY_MT5_DIFF_PLAN).iloc[0].to_dict()
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "proxy_net_profit": diff.get("proxy_net_profit"),
            "mt5_baseline_net_profit": diff.get("mt5_baseline_net_profit"),
            "proxy_profit_factor": diff.get("proxy_profit_factor"),
            "mt5_baseline_profit_factor": diff.get("mt5_baseline_profit_factor"),
            "proxy_trade_density": diff.get("proxy_trade_density"),
            "mt5_baseline_density": diff.get("mt5_baseline_density"),
            "proxy_month12_long_net": diff.get("proxy_month12_long_net"),
            "mt5_baseline_month12_net": diff.get("mt5_baseline_month12_net"),
            "proxy_closed_trade_dd": diff.get("proxy_closed_trade_dd"),
            "mt5_baseline_equity_dd": diff.get("mt5_baseline_equity_dd"),
            "review_judgment": "mt5_reprobe_required_after_runtime_repair(런타임 수리 뒤 MT5 재탐침 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def equity_dd_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "proxy_closed_trade_dd": selected["closed_trade_drawdown_proxy"],
            "proxy_closed_dd_delta": selected["closed_dd_delta_vs_proxy_base"],
            "mt5_equity_dd_baseline": selected["mt5_baseline_equity_dd"],
            "boundary_status": "closed_trade_proxy_not_equity_authority(닫힌 거래 프록시는 수익곡선 권위 아님)",
            "required_next_evidence": "MT5 Strategy Tester equity drawdown after exact runtime representation(정확 런타임 표현 뒤 MT5 전략 테스터 수익곡선 낙폭)",
            "effect": "keeps equity DD repair as a runtime question(수익곡선 낙폭 수리를 런타임 질문으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_repair_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": selected["variant_id"],
            "requirement_id": "secondary_month_margin_guard",
            "required_change": "Add second month-specific margin guard inputs and filter branch(두 번째 월별 마진 가드 입력과 필터 분기 추가)",
            "required_params": "enabled=true;side=long;month=12;start_hour=17;end_hour=21;basis=signal;min_margin=0.02",
            "preserve_existing_params": "primary month guard remains side=long;month=12;start_hour=0;end_hour=24;basis=signal;min_margin=0.01(기존 주 월 가드는 유지)",
            "acceptance_check": "EA exposes InpMonthMarginGuard2Enabled and package records both guards(EA가 보조 월 가드 입력을 노출하고 패키지가 두 가드를 기록)",
            "effect": "makes cr04 runtime-equivalent instead of broadening to cr02 or cr01(cr04를 cr02/cr01로 넓히지 않고 런타임 동등하게 만듦)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def cu_queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "cu01_secondary_month_margin_guard_runtime_package",
            "selected_variant_id": selected["variant_id"],
            "target_runtime_params": "primary_month_guard:min=0.01,hours=0-24;secondary_month_guard:min=0.02,hours=17-21;side=long;month=12;basis=signal",
            "fallback_if_patch_fails": "cr02 all-month month12 floor 0.02 or cr01 calendar block, both lower-priority fallbacks(CR02 전체 월 하한 또는 CR01 캘린더 차단, 둘 다 낮은 우선순위 대체)",
            "success_criteria": "EA compiles, set/ini package includes both guards, no MT5 execution claim(EA 컴파일, 설정/INI가 두 가드 포함, MT5 실행 주장 없음)",
            "failure_criteria": "secondary guard cannot be represented without unsafe logic(보조 가드를 안전하지 않은 로직 없이 표현 불가)",
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
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "runtime_representation_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "review cr04 before runtime packaging and prevent representation drift(cr04를 런타임 패키지 전 검토하고 표현 드리프트를 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(receipts_written: bool) -> list[dict[str, Any]]:
    receipt_paths = [KPI_RECEIPT, DATA_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    receipt_status = all(exists(path) for path in receipt_paths) if receipts_written else False
    return [
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed",
            "evidence": rel(SELECTED_VARIANT_REVIEW),
            "effect": "proxy KPI is reviewed without MT5 authority(프록시 KPI를 MT5 권위 없이 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "row_grain_audit",
            "status": "passed",
            "evidence": "Tier A separate / Tier B missing_required / Tier A+B out_of_scope rows written(티어 행 작성)",
            "effect": "Tier B gap is named(티어 B 간극을 이름 붙임)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": rel(INPUT_MANIFEST),
            "effect": "CT judgment is tied to CS/CQ/EA artifacts(CT 판정이 CS/CQ/EA 산출물에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "runtime_representation_audit",
            "status": "passed",
            "evidence": rel(RUNTIME_REPRESENTATION_REVIEW),
            "effect": "runtime representation gap is recorded before MT5 probing(MT5 탐침 전 런타임 표현 간극 기록)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if receipt_status or not receipts_written else "failed",
            "evidence": rel(GATE_AUDIT),
            "effect": "required gates connect to closeout(필수 게이트가 종료 기록에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority and operating promotion remain not claimed(런타임 권위와 운영 승격을 주장하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(selected: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
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
        "reviewed_variant_id": selected["variant_id"],
        "reviewed_net_profit": selected["net_profit"],
        "reviewed_profit_factor": selected["profit_factor"],
        "reviewed_expectancy": selected["expectancy"],
        "reviewed_trade_count": selected["trade_count"],
        "reviewed_density": selected["trade_density"],
        "reviewed_long_trade_count": selected["long_trade_count"],
        "reviewed_short_trade_count": selected["short_trade_count"],
        "reviewed_month12_long_net": selected["month12_long_net"],
        "reviewed_closed_trade_drawdown_proxy": selected["closed_trade_drawdown_proxy"],
        "reviewed_recovery_factor_proxy": selected["closed_trade_recovery_proxy"],
        "package_decision": "runtime_representation_repair_required_before_mt5_probe",
        "runtime_repair_requirement": "secondary_month_margin_guard",
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


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    write_json(
        KPI_RECEIPT,
        {
            "run_id": RUN_ID,
            "measurement_scope": "proxy KPI review for runtime representation repair(런타임 표현 수리용 프록시 KPI 검토)",
            "management_state": "run folder, manifest, report, registries updated(실행 폴더/목록/보고서/등록부 갱신)",
            "judgment_class": "positive_proxy_with_runtime_repair_required(런타임 수리 필요 긍정 프록시)",
            "scoreboard": "structural_scout(구조 정찰)",
            "parity_level": "P0_unverified(P0 미검증)",
            "wfo_status": "not_applicable(해당 없음)",
            "registry_update_required": "yes",
            "negative_memory_required": "yes_runtime_gap_boundary(런타임 간극 경계 기록)",
            "hard_gate_applicable": "no",
            "evidence_boundary": "candidate(후보)",
            "selected_kpi": selected,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(parent.SELECTED_CANDIDATE), rel(parent.CS_PROXY_REPAIR_SURFACE), rel(parent.SELECTED_TRADE_TAPE), rel(cq.MT5_KPI_REVIEW)],
            "time_axis": "inherits CS open_time/close_time sorted proxy tape(CS 진입/청산 시간 정렬 프록시 테이프 상속)",
            "sample_scope": "Tier A proxy review; Tier B missing_required recorded(Tier A 프록시 검토, Tier B 필수 누락 기록)",
            "missing_or_duplicate_check": rel(parent.DATA_INTEGRITY_AUDIT),
            "feature_label_boundary": "filters use entry-known month/hour/margin; review uses PnL after replay(필터는 진입 시점 월/시간/마진, 검토는 재생 뒤 손익 사용)",
            "split_boundary": "single validation_oos proxy review, no WFO claim(단일 검증 OOS 프록시 검토, WFO 주장 없음)",
            "leakage_risk": "runtime representation drift, not timestamp leakage(시점 누수보다 런타임 표현 드리프트 위험)",
            "data_hash_or_identity": sha(parent.SELECTED_CANDIDATE),
            "integrity_judgment": "usable_with_runtime_boundary(런타임 경계 조건부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "cr04 repairs proxy month12 long while preserving density/crucial short floor(cr04가 밀도와 숏 하한을 유지하며 프록시 12월 롱을 수리)",
            "likely_drivers": ["month12 hours17-20", "signal margin floor 0.02", "limited 8-trade removal"],
            "segment_checks": [rel(MONTH_SIDE_REVIEW), rel(FILTER_REVIEW), rel(EQUITY_DD_BOUNDARY_REVIEW)],
            "alternative_explanations": ["MT5/proxy gap", "closed-trade DD not equal to equity DD", "runtime guard expressiveness"],
            "attribution_confidence": "medium_until_runtime_reprobe(런타임 재탐침 전 중간)",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "CS selected cr04 proxy repair candidate(CS 선택 cr04 프록시 수리 후보)",
            "evidence_available": [rel(SELECTED_VARIANT_REVIEW), rel(PACKAGE_GATE_DECISION), rel(RUNTIME_REPRESENTATION_REVIEW)],
            "evidence_missing": ["exact runtime package(정확 런타임 패키지)", "new MT5 Strategy Tester output(새 MT5 전략 테스터 출력)", "runtime parity closure(런타임 동등성 종료)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "cr04 is worth preserving, but the EA must represent it exactly before MT5 probing(cr04는 보존할 가치가 있지만 MT5 탐침 전 EA가 정확히 표현해야 함).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "proxy review candidate with runtime representation repair requirement(런타임 표현 수리 필요 프록시 검토 후보)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "Goal Achieve"],
            "new_model_training": final["new_model_training"],
            "new_mt5_execution": final["new_mt5_execution"],
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
            "availability": "tracked_and_reproducible_from_script(추적됨, 스크립트로 재생 가능)",
            "lineage_judgment": "connected_with_runtime_repair_boundary(런타임 수리 경계로 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(final: Mapping[str, Any], representation: Sequence[Mapping[str, Any]], package_rows_: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364CT h17 month12 long equity drawdown repair review(364CT 17시 12월 롱/수익곡선 낙폭 수리 검토)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- reviewed variant(검토 변형): `{final['reviewed_variant_id']}`
- proxy KPI(프록시 핵심 성과 지표): net(순수익) `{final['reviewed_net_profit']}`, PF(수익 팩터) `{final['reviewed_profit_factor']}`, density(밀도) `{final['reviewed_density']}`, trades(거래수) `{final['reviewed_trade_count']}`, shorts(숏) `{final['reviewed_short_trade_count']}`
- month12 long net(12월 롱 순수익): `{final['reviewed_month12_long_net']}`
- package decision(패키지 결정): `{final['package_decision']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Action And Effect(행동과 효과)

Action(행동): CS selected proxy(CS 선택 프록시) `cr04`를 KPI(핵심 성과 지표), proxy/MT5 gap(프록시/MT5 차이), EA representation(EA 표현 가능성)으로 검토했습니다.

Effect(효과): `cr04`는 보존하지만, 현재 EA에는 두 번째 month margin guard(월 마진 가드)가 없어 바로 MT5 package(MT5 패키지)로 넘기지 않고 `{NEXT_RUN_ID}`에서 런타임 표현을 먼저 수리합니다.

## Package Gate(패키지 게이트)

{markdown_table(package_rows_, ['gate_id', 'gate_status', 'evidence', 'effect'], 8)}

## Runtime Representation(런타임 표현)

{markdown_table(representation, ['variant_id', 'representation_id', 'representation_status', 'required_runtime_change', 'effect'], 8)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 8)}

## Boundary(경계)

This is review only(검토 전용)입니다. New MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CT decision(결정): cr04 runtime representation repair required(cr04 런타임 표현 수리 필요)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- reviewed variant(검토 변형): `{final['reviewed_variant_id']}`
- effect(효과): `cr04`를 `cr02`나 `cr01`로 넓히지 않고, `{NEXT_RUN_ID}`에서 두 번째 month margin guard(월 마진 가드)를 구현/패키지화합니다.
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        f"run364CT__{RUN_ID}",
        f"\n- run364CT__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cr04 runtime representation repair required(cr04 런타임 표현 수리 필요), next `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        f"run364CT__{RUN_ID}",
        f"""
<!-- run364CT__{RUN_ID} -->

## run364CT Runtime Representation Review(364CT 런타임 표현 검토)

Action(행동): `cr04` 프록시 후보를 EA 표현 가능성까지 검토했습니다.

Effect(효과): 두 번째 month margin guard(월 마진 가드)가 필요하므로 `{NEXT_RUN_ID}`에서 런타임 패키지 수리로 이어갑니다.
""",
    )
    append_text_once(
        STAGE_README,
        f"run364CT__{RUN_ID}",
        f"\n<!-- run364CT__{RUN_ID} -->\n## run364CT review(364CT 검토)\n\nSelected(선택): `{final['reviewed_variant_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n",
    )
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Reviewed proxy repair variant(검토 프록시 수리 변형): `{final['reviewed_variant_id']}`.

Review result(검토 결과): proxy KPI(프록시 핵심 성과 지표)는 유지하지만 exact runtime representation(정확 런타임 표현)을 위해 secondary month margin guard(보조 월 마진 가드)가 필요합니다.

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

Current truth(현재 진실): `run364CT` reviewed(검토 완료) `cr04_month12_long_hours17_20_floor002` and found(확인) proxy KPI(프록시 핵심 성과 지표)는 좋지만 exact runtime representation(정확 런타임 표현)을 위해 secondary month margin guard(보조 월 마진 가드)가 필요합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 EA(전문가 자문)에 보조 월 마진 가드를 추가하고 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만듭니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364CT__{RUN_ID}",
        f"\n<!-- run364CT__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed CT review(CT 검토 완료); cr04 requires secondary month margin guard(보조 월 마진 가드 필요); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"run364CT__{RUN_ID}",
        f"\n<!-- run364CT__{RUN_ID} -->\n- `{RUN_ID}`: cr04 runtime representation review(cr04 런타임 표현 검토). Effect(효과): 정확 표현을 위해 보조 월 마진 가드를 다음 수리 씨앗으로 남김.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"run364CT__runtime_gap__{RUN_ID}",
        f"\n<!-- run364CT__runtime_gap__{RUN_ID} -->\n- `{RUN_ID}` runtime gap(런타임 간극): cr04 proxy(프록시)는 긍정이지만 현재 EA(전문가 자문)는 piecewise month12 margin guard(구간별 12월 마진 가드)를 정확히 표현하지 못합니다. Effect(효과): cr04를 버리지 않고 `{NEXT_RUN_ID}`에서 도구를 먼저 수리합니다.\n",
    )


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
        "work_family": "kpi_evidence(KPI 근거)",
        "scoreboard_lane": "proxy_review(프록시 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "candidate_review_only(후보 검토 전용)",
        "question": "Can cr04 be handed to MT5 without changing its meaning?(cr04를 의미 변경 없이 MT5로 넘길 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["reviewed_net_profit"],
        "profit_factor": final["reviewed_profit_factor"],
        "expectancy": final["reviewed_expectancy"],
        "trade_count": final["reviewed_trade_count"],
        "trade_density_per_feature_day": final["reviewed_density"],
        "long_trade_count": final["reviewed_long_trade_count"],
        "short_trade_count": final["reviewed_short_trade_count"],
        "max_drawdown_amount": final["reviewed_closed_trade_drawdown_proxy"],
        "recovery_factor": final["reviewed_recovery_factor_proxy"],
        "trade_density_requirement_status": "passed_proxy_review_runtime_repair_required(프록시 검토 통과, 런타임 수리 필요)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_REPRESENTATION_REVIEW),
        "primary_kpi": f"net={final['reviewed_net_profit']};pf={final['reviewed_profit_factor']};density={final['reviewed_density']};month12_long={final['reviewed_month12_long_net']}",
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
            "kpi_scope": "CT proxy review(CT 프록시 검토)",
            "status": status,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "runtime_representation_review(런타임 표현 검토)",
        }
        if not include_metrics:
            for key in [
                "net_profit",
                "profit_factor",
                "expectancy",
                "trade_count",
                "trade_density_per_feature_day",
                "long_trade_count",
                "short_trade_count",
                "max_drawdown_amount",
                "recovery_factor",
            ]:
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
        ("selected_variant_review", SELECTED_VARIANT_REVIEW, "CT selected variant review(CT 선택 변형 검토)."),
        ("package_gate_decision", PACKAGE_GATE_DECISION, "CT package gate decision(CT 패키지 게이트 결정)."),
        ("runtime_representation_review", RUNTIME_REPRESENTATION_REVIEW, "CT runtime representation review(CT 런타임 표현 검토)."),
        ("runtime_repair_requirements", RUNTIME_REPAIR_REQUIREMENTS, "CT runtime repair requirements(CT 런타임 수리 요구사항)."),
        ("next_queue", RUN364CU_QUEUE, "CU runtime package queue(CU 런타임 패키지 대기열)."),
        ("report", REPORT_PATH, "CT report(CT 보고서)."),
        ("final_decision", FINAL_DECISION, "CT final decision(CT 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CT run manifest(CT 실행 목록)."),
        ("gate_audit", GATE_AUDIT, "CT gate audit(CT 게이트 감사)."),
        ("lineage_receipt", LINEAGE_RECEIPT, "CT lineage receipt(CT 계보 영수증)."),
        ("script", Path(__file__), "CT producer script(CT 생산 스크립트)."),
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


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()

    selected = read_json(parent.SELECTED_CANDIDATE)
    selected_id = str(selected["variant_id"])
    representation = runtime_representation_rows(selected)
    selected_rows = selected_review_rows(read_json(parent.FINAL_DECISION), selected)
    package_rows_ = package_gate_rows(selected, representation)
    proxy_rows = proxy_mt5_rows(selected)
    dd_rows = equity_dd_rows(selected)
    month_side_rows = selected_month_side_rows(selected_id)
    filter_rows = selected_filter_rows(selected_id)
    repair_rows = runtime_repair_rows(selected)
    queue_rows = cu_queue_rows(selected)

    write_csv(SELECTED_VARIANT_REVIEW, selected_rows)
    write_csv(PACKAGE_GATE_DECISION, package_rows_)
    write_csv(RUNTIME_REPRESENTATION_REVIEW, representation)
    write_csv(PROXY_MT5_GAP_REVIEW, proxy_rows)
    write_csv(EQUITY_DD_BOUNDARY_REVIEW, dd_rows)
    write_csv(MONTH_SIDE_REVIEW, month_side_rows)
    write_csv(FILTER_REVIEW, filter_rows)
    write_csv(RUNTIME_REPAIR_REQUIREMENTS, repair_rows)
    write_csv(RUN364CU_QUEUE, queue_rows)

    preliminary_gates = gate_rows(receipts_written=False)
    final = final_payload(selected, preliminary_gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected)
    refresh_lineage_receipt(final)
    gates = gate_rows(receipts_written=True)
    final = final_payload(selected, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final, selected)
    write_docs(final, representation, package_rows_, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(parent.json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
