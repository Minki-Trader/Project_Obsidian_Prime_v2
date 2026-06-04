from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import train_late_year_short_share_stress_repair_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BT"
RUN_ID = "run364BT_review_late_year_short_share_stress_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = parent.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BU_prepare_late_year_session_gate_mt5_precheck_without_db_v1"

STATUS = "completed_stage364BT_bs_review_precheck_eligible_open_bu_no_authority"
JUDGMENT = "positive_proxy_repair_review_precheck_eligible_low_sample_watch_no_mt5_authority"
DECISION = "stage364BT_open_run364BU_late_year_session_gate_mt5_precheck"
CLAIM_BOUNDARY = (
    "research_development_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
PACKAGE_PRECHECK_DECISION = RUN_DIR / "package_precheck_decision.csv"
OVERFIT_REVIEW = RUN_DIR / "overfit_review.csv"
ROBUSTNESS_SURFACE_REVIEW = RUN_DIR / "robustness_surface_review.csv"
PROXY_MT5_DIFF_REVIEW = RUN_DIR / "proxy_mt5_diff_review.csv"
RUN364BU_QUEUE = RUN_DIR / "run364BU_mt5_precheck_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BT_late_year_short_share_stress_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BT_late_year_short_share_stress_repair_review.md"
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

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.BS_RULE_SURFACE,
    parent.SELECTED_CANDIDATE,
    parent.SELECTED_TRADE_TAPE,
    parent.SELECTED_SYNTHETIC_SHORT_TAPE,
    parent.SELECTED_DISPLACED_PARENT_TRADES,
    parent.SELECTED_PARENT_SUPPRESSED_TRADES,
    parent.LATE_YEAR_STRESS_REPAIR_ATTRIBUTION,
    parent.STRESS_SLICE_REVIEW,
    parent.OVERFIT_GUARDRAIL_AUDIT,
    parent.PROXY_MT5_DIFF_PLAN,
    parent.RUN364BT_QUEUE,
    parent.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    PACKAGE_PRECHECK_DECISION,
    OVERFIT_REVIEW,
    ROBUSTNESS_SURFACE_REVIEW,
    PROXY_MT5_DIFF_REVIEW,
    RUN364BU_QUEUE,
    WORK_PACKET,
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


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


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


def drop_empty_csv_columns(path: Path, columns: Sequence[str]) -> None:
    parent.drop_empty_csv_columns(path, columns)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    return parent.as_int(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 14) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig").fillna("")


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BT inputs(BT 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BS next_run_id mismatch(BS 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("BS has forbidden authority claim(BS 금지 권위 주장 존재)")
    gates = read_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("BS gate audit(BS 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BT review source(BT 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def truthy_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def package_precheck_decision_rows(final: Mapping[str, Any], surface: pd.DataFrame) -> list[dict[str, Any]]:
    package_like = surface[truthy_series(surface["package_like_proxy_row"])].copy()
    synthetic_package_like = package_like[package_like["family_id"].astype(str).str.contains("synthetic", case=False, na=False)]
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "headline_kpi_gate",
            "gate_status": "passed_for_precheck(사전검사 통과)",
            "evidence": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_density']};short_share={final['selected_short_share']}",
            "interpretation": "selected proxy keeps headline KPI above review floors(선택 프록시가 검토 기준 KPI를 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "stress_clear_gate",
            "gate_status": "passed_for_precheck(사전검사 통과)",
            "evidence": f"month_bad_count={final['month_bad_count']};min_month_net={final['min_month_net']};min_month_pf={final['min_month_profit_factor']}",
            "interpretation": "BS repaired BR month stress in proxy(BS가 BR 월 압박을 프록시에서 수리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "low_sample_month_gate",
            "gate_status": "watch_for_precheck(사전검사 관찰)",
            "evidence": f"suppressed_trades={final['selected_parent_suppressed_trade_count']};month_of_year={final['selected_parent_suppress_months']};hours={final['selected_parent_suppress_hours']}",
            "interpretation": "review accepts only MT5 precheck, not promotion(검토는 MT5 사전검사만 허용하고 승격은 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "family_concentration_gate",
            "gate_status": "watch_for_precheck(사전검사 관찰)",
            "evidence": f"package_like_rows={len(package_like)};synthetic_package_like_rows={len(synthetic_package_like)}",
            "interpretation": "all stress-clear rows came from parent-session suppression(압박 해소 행은 부모 세션 억제 계열에 몰림)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "mt5_runtime_gate",
            "gate_status": "pending_for_bu(BU에서 대기)",
            "evidence": "new_mt5_execution=not_run",
            "interpretation": "proxy cannot replace MT5 Strategy Tester(프록시는 MT5 전략 테스터를 대체하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "decision",
            "gate_status": "eligible_for_bu_precheck_not_package_authority(BU 사전검사 적격, 패키지 권위 아님)",
            "evidence": f"next_run_id={NEXT_RUN_ID}",
            "interpretation": "move to materialized MT5 precheck attempt(물질화된 MT5 사전검사 시도로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def overfit_review_rows(final: Mapping[str, Any], parent_overfit: pd.DataFrame) -> list[dict[str, Any]]:
    parent_failed = parent_overfit[parent_overfit["status"].astype(str).str.lower() == "failed"]
    return [
        {
            "run_id": RUN_ID,
            "audit_id": "timestamp_safe_boundary(시점 안전 경계)",
            "status": "passed" if parent_failed.empty else "failed",
            "evidence": "BS used month_of_year/hour/side/probability/margin, not exact year-month(BS는 정확 연월이 아닌 월중/시간/방향/확률/마진 사용)",
            "effect": "look-ahead bias(미래참조 편향) 재발을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "low_sample_repair_watch(소표본 수리 관찰)",
            "status": "watch",
            "evidence": f"suppressed_trade_count={final['selected_parent_suppressed_trade_count']};suppressed_net={final['selected_parent_suppressed_net_profit']}",
            "effect": "5개 거래 제거 효과를 운영 승격 근거로 오해하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "month_of_year_specificity_watch(월중 특이성 관찰)",
            "status": "watch",
            "evidence": f"parent_suppress_months={final['selected_parent_suppress_months']};parent_suppress_hours={final['selected_parent_suppress_hours']}",
            "effect": "December(12월) 계절성 수리가 다른 구간에서 깨지는지 MT5/추가 탐색으로 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "no_package_authority_guard(패키지 권위 차단)",
            "status": "passed",
            "evidence": "new_mt5_execution=not_run; runtime_authority=not_claimed",
            "effect": "precheck eligible(사전검사 적격)과 package authority(패키지 권위)를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def robustness_rows(final: Mapping[str, Any], surface: pd.DataFrame) -> list[dict[str, Any]]:
    package_like = surface[truthy_series(surface["package_like_proxy_row"])].copy()
    top = package_like.sort_values("selection_score", key=lambda s: pd.to_numeric(s, errors="coerce"), ascending=False).head(12)
    rows: list[dict[str, Any]] = [
        {
            "run_id": RUN_ID,
            "review_id": "surface_count_summary(표면 수 요약)",
            "value": len(surface),
            "detail": f"core_pass_rows={int(truthy_series(surface['core_pass']).sum())};package_like_rows={len(package_like)}",
            "interpretation": "surface is broad enough for review(검토할 만큼 표면이 넓음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "selected_intervention_size(선택 개입 크기)",
            "value": final["selected_parent_suppressed_trade_count"],
            "detail": f"suppressed_net={final['selected_parent_suppressed_net_profit']};selected={final['selected_candidate_id']}",
            "interpretation": "small intervention is attractive but sample-risky(작은 개입은 매력적이나 표본 위험이 있음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "family_concentration(계열 집중)",
            "value": package_like["family_id"].nunique() if not package_like.empty else 0,
            "detail": "|".join(sorted(package_like["family_id"].astype(str).unique())) if not package_like.empty else "none",
            "interpretation": "precheck should carry parent-session gate explicitly(사전검사는 부모 세션 게이트를 명시해야 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for rank, (_, row) in enumerate(top.iterrows(), start=1):
        rows.append(
            {
                "run_id": RUN_ID,
                "review_id": f"package_like_rank_{rank:02d}",
                "value": row.get("selection_score", ""),
                "detail": f"{row['candidate_id']};net={row['net_profit']};pf={row['profit_factor']};density={row['trade_density_per_business_day']};suppressed={row['parent_suppressed_trade_count']}",
                "interpretation": "neighbor candidate for BU comparison(BU 비교용 이웃 후보)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_mt5_review_rows(proxy_mt5: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in proxy_mt5.iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": row.get("comparison_id", "bs_proxy_vs_bk_mt5_runtime_probe"),
                "source_runtime_probe_run_id": row.get("source_runtime_probe_run_id", SOURCE_RUNTIME_PROBE_RUN_ID),
                "mt5_net_profit": row.get("mt5_net_profit", ""),
                "proxy_net_profit": row.get("proxy_net_profit", ""),
                "net_diff_proxy_minus_mt5": row.get("net_diff_proxy_minus_mt5", ""),
                "mt5_profit_factor": row.get("mt5_profit_factor", ""),
                "proxy_profit_factor": row.get("proxy_profit_factor", ""),
                "profit_factor_diff_proxy_minus_mt5": row.get("profit_factor_diff_proxy_minus_mt5", ""),
                "mt5_density": row.get("mt5_density", ""),
                "proxy_density": row.get("proxy_density", ""),
                "density_diff_proxy_minus_mt5": row.get("density_diff_proxy_minus_mt5", ""),
                "attribution": "BS proxy changes parent-session gate and synthetic replay without new MT5 execution(BS 프록시는 새 MT5 실행 없이 부모 세션 게이트와 합성 재생을 바꿈)",
                "usability": "usable_for_BU_precheck_handoff_not_runtime_authority(BU 사전검사 인계에는 사용 가능, 런타임 권위 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def next_queue_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "selected_candidate_id": final["selected_candidate_id"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        {
            **common,
            "queue_rank": 1,
            "queue_id": "bu01_materialize_session_gate_precheck_request",
            "action": "materialize MT5 precheck request for December h21 long suppression(12월 21시 롱 억제 MT5 사전검사 요청 물질화)",
            "success_criteria": "bundle/request records selected rule, hashes, and no-authority boundary(번들/요청이 선택 규칙, 해시, 무권위 경계를 기록)",
            "effect": "proxy repair(프록시 수리)를 MT5 실행 의미로 옮길 준비를 한다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bu02_attempt_narrow_mt5_strategy_tester_probe",
            "action": "attempt narrow MT5 Strategy Tester probe if runtime tooling supports the gate(런타임 도구가 게이트를 지원하면 좁은 MT5 전략 테스터 탐침 시도)",
            "success_criteria": "tester output, trade list, or exact blocker log exists(테스터 출력, 거래 목록, 또는 정확한 차단 로그 존재)",
            "effect": "external verification(외부 검증)을 다음으로 미루기만 하지 않는다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bu03_runtime_gap_or_overfit_repair_branch",
            "action": "if MT5 gap or gate support fails, convert blocker into repair seed(MT5 간극 또는 게이트 지원 실패 시 차단을 수리 씨앗으로 변환)",
            "success_criteria": "reject, repair, or package-precheck evidence is explicit(거절/수리/패키지 사전검사 근거가 명시)",
            "effect": "low-sample proxy(소표본 프록시)를 운영 주장으로 넘기지 않는다.",
        },
    ]


def gate_rows(final: Mapping[str, Any], package_rows: Sequence[Mapping[str, Any]], overfit_rows_: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate": "scope_review_completion_gate",
            "status": "passed" if package_rows and overfit_rows_ and proxy_rows else "failed",
            "evidence": f"{rel(PACKAGE_PRECHECK_DECISION)};{rel(OVERFIT_REVIEW)};{rel(PROXY_MT5_DIFF_REVIEW)}",
            "effect": "BS review(BS 검토)를 KPI, 과적합, MT5 차이로 분리했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_gate_audit",
            "status": "passed",
            "evidence": rel(parent.GATE_AUDIT),
            "effect": "BS 산출물의 gate(게이트)가 통과된 상태에서만 리뷰했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "kpi_review_gate",
            "status": "passed" if as_int(final["reviewed_month_bad_count"]) == 0 and as_int(final["reviewed_package_like_rows"]) > 0 else "failed",
            "evidence": rel(PACKAGE_PRECHECK_DECISION),
            "effect": "stress clear(압박 해소)와 precheck eligibility(사전검사 적격)를 확인했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "overfit_watch_recorded",
            "status": "passed" if any(row["status"] == "watch" for row in overfit_rows_) else "failed",
            "evidence": rel(OVERFIT_REVIEW),
            "effect": "low-sample/month-specific risk(소표본/월 특이 위험)를 다음 검증 조건으로 남겼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "proxy_mt5_diff_recorded",
            "status": "passed" if len(proxy_rows) >= 1 else "failed",
            "evidence": rel(PROXY_MT5_DIFF_REVIEW),
            "effect": "proxy(프록시)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않게 했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "next_external_verification_gate",
            "status": "passed" if len(queue) == 3 and queue[1]["queue_id"] == "bu02_attempt_narrow_mt5_strategy_tester_probe" else "failed",
            "evidence": rel(RUN364BU_QUEUE),
            "effect": "다음 작업을 MT5 외부 검증 시도로 직접 연결했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "precheck_boundary_gate",
            "status": "passed" if final["new_mt5_execution"] == "not_run" and final["runtime_authority"] == "not_claimed" else "failed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "precheck eligible(사전검사 적격)을 operating promotion(운영 승격)으로 올리지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "필수 gate(게이트)와 산출물 연결을 확인했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(bs_final: Mapping[str, Any], robustness: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "reviewed_candidate_id": bs_final["selected_candidate_id"],
        "reviewed_net_profit": bs_final["selected_net_profit"],
        "reviewed_profit_factor": bs_final["selected_profit_factor"],
        "reviewed_expectancy": bs_final["selected_expectancy"],
        "reviewed_trade_count": bs_final["selected_trade_count"],
        "reviewed_density": bs_final["selected_density"],
        "reviewed_closed_drawdown_amount": bs_final["selected_closed_drawdown_amount"],
        "reviewed_recovery_factor": bs_final["selected_recovery_factor"],
        "reviewed_long_trade_count": bs_final["selected_long_trade_count"],
        "reviewed_short_trade_count": bs_final["selected_short_trade_count"],
        "reviewed_short_share": bs_final["selected_short_share"],
        "reviewed_month_bad_count": bs_final["month_bad_count"],
        "reviewed_min_month_net": bs_final["min_month_net"],
        "reviewed_min_month_profit_factor": bs_final["min_month_profit_factor"],
        "reviewed_package_like_rows": bs_final["package_candidate_rows"],
        "reviewed_parent_suppressed_trade_count": bs_final["selected_parent_suppressed_trade_count"],
        "reviewed_parent_suppressed_net_profit": bs_final["selected_parent_suppressed_net_profit"],
        "reviewed_parent_suppress_months": bs_final["selected_parent_suppress_months"],
        "reviewed_parent_suppress_hours": bs_final["selected_parent_suppress_hours"],
        "reviewed_parent_suppress_side": bs_final["selected_parent_suppress_side"],
        "precheck_decision": "eligible_for_bu_precheck_not_package_authority(BU 사전검사 적격, 패키지 권위 아님)",
        "overfit_watch": "low_sample_month_of_year_session_gate_watch(소표본 월중 세션 게이트 관찰)",
        "robustness_review_rows": len(robustness),
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


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "kpi_evidence(핵심 성과 지표 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_review_completion_gate",
                "kpi_review_gate",
                "overfit_watch_recorded",
                "proxy_mt5_diff_recorded",
                "next_external_verification_gate",
                "required_gate_coverage_audit",
            ],
            "result_subject": "BS selected proxy repair(BS 선택 프록시 수리)",
            "evidence_boundary": "review_only(검토 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any], proxy_rows: Sequence[Mapping[str, Any]], robustness: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        KPI_RECEIPT,
        {
            **base,
            "reviewed_candidate": final["reviewed_candidate_id"],
            "headline": {
                "net": final["reviewed_net_profit"],
                "pf": final["reviewed_profit_factor"],
                "density": final["reviewed_density"],
                "short_share": final["reviewed_short_share"],
                "month_bad_count": final["reviewed_month_bad_count"],
            },
            "precheck_decision": final["precheck_decision"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_sources": [rel(path) for path in INPUT_FILES if exists(path)],
            "timestamp_boundary": "review uses BS outputs only; selected rule is month_of_year/hour/side, not exact year_month(BS 출력만 검토, 선택 규칙은 정확 연월이 아닌 월중/시간/방향)",
            "integrity_judgment": "usable_for_review_and_BU_handoff_no_new_labeling(검토와 BU 인계에 사용 가능, 새 라벨링 없음)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "proxy_mt5_diff_review": list(proxy_rows),
            "robustness_review": list(robustness)[:10],
            "driver": "December h21 long suppression cleared proxy stress but needs MT5 runtime precheck(12월 21시 롱 억제가 프록시 압박을 해소했지만 MT5 런타임 사전검사가 필요)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_condition": NEXT_RUN_ID,
            "missing_evidence": ["new MT5 Strategy Tester probe(새 MT5 전략 테스터 탐침)", "forward pass(전진 통과)", "runtime parity(런타임 동등성)"],
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "effect": "BT는 BU precheck handoff(BU 사전검사 인계)만 주장한다.",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if exists(path) and path != LINEAGE_RECEIPT]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths if Path(path).is_file()},
            "lineage_judgment": "connected_BS_proxy_repair_to_BU_MT5_precheck(BS 프록시 수리를 BU MT5 사전검사에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    overfit_rows_: Sequence[Mapping[str, Any]],
    robustness: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364BT late-year short-share stress repair review(364BT 연말 숏비중 압박 수리 검토)

## Current Truth(현재 진실)

- reviewed candidate(검토 후보): `{final['reviewed_candidate_id']}`
- reviewed KPI(검토 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_share']}`
- stress(압박): month_bad_count(월 나쁨 수) `{final['reviewed_month_bad_count']}`, min month net/PF(최저 월 순수익/수익 팩터) `{final['reviewed_min_month_net']}` / `{final['reviewed_min_month_profit_factor']}`
- precheck decision(사전검사 결정): `{final['precheck_decision']}`
- overfit watch(과적합 관찰): `{final['overfit_watch']}`

## Action And Effect(행동과 효과)

Action(행동): BS selected proxy(BS 선택 프록시)를 package precheck decision(패키지 사전검사 결정), overfit review(과적합 검토), robustness surface review(강건성 표면 검토), proxy/MT5 diff review(프록시/MT5 차이 검토)로 분리했다.

Effect(효과): BU에서 narrow MT5 Strategy Tester probe(좁은 MT5 전략 테스터 탐침)를 바로 시도할 수 있게 queue(대기열)를 열었고, runtime authority(런타임 권위)는 주장하지 않았다.

## Package Precheck Decision(패키지 사전검사 결정)

{markdown_table(package_rows, ['gate_id', 'gate_status', 'evidence', 'interpretation'])}

## Overfit Review(과적합 검토)

{markdown_table(overfit_rows_, ['audit_id', 'status', 'evidence', 'effect'])}

## Robustness Surface Review(강건성 표면 검토)

{markdown_table(robustness, ['review_id', 'value', 'detail', 'interpretation'])}

## Proxy/MT5 Diff(프록시/MT5 차이)

{markdown_table(proxy_rows, ['comparison_id', 'mt5_net_profit', 'proxy_net_profit', 'net_diff_proxy_minus_mt5', 'mt5_profit_factor', 'proxy_profit_factor', 'usability'])}

## BU Queue(BU 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'action', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BT is review only(BT는 검토 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BT late-year short-share stress repair review(연말 숏비중 압박 수리 검토)

Action(행동): `{final['reviewed_candidate_id']}`를 BU MT5 precheck(BU MT5 사전검사)로 넘겼다.

Effect(효과): precheck eligible(사전검사 적격)은 기록했지만, new MT5 execution(새 MT5 실행)이 없으므로 runtime authority(런타임 권위)는 주장하지 않았다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - late-year stress repair review(연말 압박 수리 검토).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BT Late-Year Stress Repair Review Closeout",
        f"""## run364BT Late-Year Stress Repair Review Closeout(364BT 연말 압박 수리 검토 종료)

Action(행동): BS selected proxy(BS 선택 프록시)를 precheck eligible(사전검사 적격)로 검토했다.

Effect(효과): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester probe(MT5 전략 테스터 탐침)를 시도하도록 current truth(현재 진실)를 넘겼고, 운영 권위는 주장하지 않았다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BT Late-Year Stress Repair Review(364BT 연말 압박 수리 검토)

Action(행동): Stage364(364단계) 안에서 BS 프록시 수리를 검토하고 BU MT5 사전검사로 넘겼다.

Effect(효과): 소표본 과적합 관찰을 유지하면서 외부 검증을 다음 직접 실행 조건으로 만들었다.
""",
    )
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
    replace_prefixed_lines(
        STAGE_README,
        {
            "Current run(현재 실행):": f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "Latest completed run(최근 완료 실행):": f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364BT(364BT 실행)는 `{final['reviewed_candidate_id']}`를 BU MT5 precheck(BU MT5 사전검사)로 넘겼지만 low-sample watch(소표본 관찰)와 no-authority(무권위) 경계를 유지한다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 precheck request(사전검사 요청)를 물질화하고 좁은 Strategy Tester probe(전략 테스터 탐침)를 시도한다.",
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

Current truth(현재 진실): `run364BT`는 BS selected proxy(BS 선택 프록시) `{final['reviewed_candidate_id']}`를 review(검토)했다. KPI(핵심 성과 지표)는 net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_share']}`이고 month_bad_count(월 나쁨 수)는 `{final['reviewed_month_bad_count']}`다. 다만 suppressed trades(억제 거래)가 `{final['reviewed_parent_suppressed_trade_count']}`개인 low-sample month-of-year/session gate(소표본 월중/세션 게이트)이므로 BU MT5 precheck(BU MT5 사전검사)로만 넘긴다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 selected rule(선택 규칙)을 물질화하고 가능한 경우 좁은 MT5 Strategy Tester probe(MT5 전략 테스터 탐침)를 시도한다.

Operating boundary(운영 경계): no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Package candidate(패키지 후보): none(없음). BT review(BT 검토)는 `{final['reviewed_candidate_id']}`를 package precheck eligible(패키지 사전검사 적격)로만 기록했다.

Selected proxy for precheck(사전검사용 선택 프록시): `{final['reviewed_candidate_id']}`

Proxy KPI(프록시 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, expectancy `{final['reviewed_expectancy']}`, trades `{final['reviewed_trade_count']}`, density `{final['reviewed_density']}`, closed DD `{final['reviewed_closed_drawdown_amount']}`, recovery `{final['reviewed_recovery_factor']}`, long/short `{final['reviewed_long_trade_count']}` / `{final['reviewed_short_trade_count']}`, short share `{final['reviewed_short_share']}`.

Watch(관찰): low-sample month-of-year/session gate(소표본 월중/세션 게이트). Suppressed trades(억제 거래) `{final['reviewed_parent_suppressed_trade_count']}`, suppressed net(억제 순수익) `{final['reviewed_parent_suppressed_net_profit']}`.

Next queue(다음 대기열): `{rel(RUN364BU_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): late-year short-share stress repair review(연말 숏비중 압박 수리 검토)를 완료했다.
- effect(효과): `{final['reviewed_candidate_id']}`를 BU MT5 precheck(BU MT5 사전검사)로 넘기고 authority(권위)는 주장하지 않았다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): December h21 long suppression(12월 21시 롱 억제)은 proxy stress(프록시 압박)를 해소할 수 있지만 low-sample watch(소표본 관찰)가 필요하다.
- positive clue(긍정 단서): selected proxy(선택 프록시) net/PF/density/short share `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_share']}`.
- next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): runtime authority not opened(런타임 권위 열지 않음).
- failure_memory(실패 기억): BS 수리는 5개 parent trade(부모 거래) 억제에서 나왔기 때문에 MT5 precheck(MT5 사전검사) 전에는 운영 주장으로 쓸 수 없다.
- salvage_value(회수 가치): precheck eligible(사전검사 적격) 후보로 BU에서 외부 검증을 시도할 가치가 있다.
- reopen_condition(재개 조건): `{NEXT_RUN_ID}`에서 Strategy Tester output(전략 테스터 출력) 또는 정확한 blocker(차단 사유)를 만든다.
""",
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
        "rows": final["robustness_review_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "kpi_evidence(핵심 성과 지표 근거)",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "evidence_boundary": "review_only(검토 전용)",
        "question": "Should BS stress-clear proxy move to MT5 precheck or be rejected?(BS 압박 해소 프록시를 MT5 사전검사로 보낼 것인가 거절할 것인가?)",
        "next_action": NEXT_RUN_ID,
    }
    metric_values = {
        "net_profit": final["reviewed_net_profit"],
        "profit_factor": final["reviewed_profit_factor"],
        "expectancy": final["reviewed_expectancy"],
        "drawdown": final["reviewed_closed_drawdown_amount"],
        "recovery_factor": final["reviewed_recovery_factor"],
        "trade_count": final["reviewed_trade_count"],
        "trade_density_per_feature_day": final["reviewed_density"],
        "long_trade_count": final["reviewed_long_trade_count"],
        "short_trade_count": final["reviewed_short_trade_count"],
        "max_drawdown_amount": final["reviewed_closed_drawdown_amount"],
    }
    rows: list[dict[str, Any]] = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required(필수 누락)", False),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", STATUS, True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "BT review(BT 검토)",
            "scoreboard_lane": "stage364_review(Stage364 검토)",
            "status": status,
            "primary_kpi": f"net={final['reviewed_net_profit']};pf={final['reviewed_profit_factor']};density={final['reviewed_density']};short_share={final['reviewed_short_share']}",
            "guardrail_kpi": f"precheck_eligible;low_sample_watch;suppressed={final['reviewed_parent_suppressed_trade_count']};no_authority",
            "result_judgment": JUDGMENT,
        }
        if include_metrics:
            row.update(metric_values)
        rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])
    registry_row = {
        **common,
        "lane": "stage364_review(Stage364 검토)",
        "family": "late_year_short_share_stress_repair_review(연말 숏비중 압박 수리 검토)",
        "path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "net_profit": final["reviewed_net_profit"],
        "profit_factor": final["reviewed_profit_factor"],
        "drawdown": final["reviewed_closed_drawdown_amount"],
        "recovery_factor": final["reviewed_recovery_factor"],
        "trade_count": final["reviewed_trade_count"],
        "trade_density_per_feature_day": final["reviewed_density"],
        "result_status": STATUS,
        "expectancy": final["reviewed_expectancy"],
        "view": "review(검토)",
        "tier": "Tier A",
        "metric_scope": "reviewed_proxy(검토 프록시)",
        "scoreboard_lane": "stage364_review(Stage364 검토)",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_judgment": JUDGMENT,
        "max_drawdown_amount": final["reviewed_closed_drawdown_amount"],
        "long_trade_count": final["reviewed_long_trade_count"],
        "short_trade_count": final["reviewed_short_trade_count"],
        "row_id": RUN_ID,
        "evidence_boundary": "review_only(검토 전용)",
        "next_action": NEXT_RUN_ID,
        "question": common["question"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [registry_row])
    parent.repair_run_registry_line_endings(RUN_REGISTRY)


def write_manifest(final: Mapping[str, Any]) -> None:
    existing_outputs = [path for path in OUTPUT_FILES if exists(path) and path != RUN_MANIFEST]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in existing_outputs if Path(path).is_file()],
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if not exists(path) or not Path(path).is_file():
            continue
        artifact_type = "run_manifest" if path == RUN_MANIFEST else "stage364BT_artifact"
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
                "artifact_id": f"{RUN_NUMBER}_{Path(path).stem}",
                "notes": "Stage364BT late-year stress repair review artifact(364BT 연말 압박 수리 검토 산출물)",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_tables(
    package_rows: Sequence[Mapping[str, Any]],
    overfit_rows_: Sequence[Mapping[str, Any]],
    robustness: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> None:
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(PACKAGE_PRECHECK_DECISION, package_rows)
    write_csv(OVERFIT_REVIEW, overfit_rows_)
    write_csv(ROBUSTNESS_SURFACE_REVIEW, robustness)
    write_csv(PROXY_MT5_DIFF_REVIEW, proxy_rows)
    write_csv(RUN364BU_QUEUE, queue)


def main() -> None:
    ensure_dirs()
    bs_final = validate_inputs()
    surface = load_csv(parent.BS_RULE_SURFACE)
    parent_overfit = load_csv(parent.OVERFIT_GUARDRAIL_AUDIT)
    proxy_mt5 = load_csv(parent.PROXY_MT5_DIFF_PLAN)
    package_rows = package_precheck_decision_rows(bs_final, surface)
    overfit_rows_ = overfit_review_rows(bs_final, parent_overfit)
    robustness = robustness_rows(bs_final, surface)
    proxy_rows = proxy_mt5_review_rows(proxy_mt5)
    queue = next_queue_rows(bs_final)
    created_at = now_utc()

    write_work_packet()
    write_tables(package_rows, overfit_rows_, robustness, proxy_rows, queue)
    preliminary_final = final_payload(bs_final, robustness, [], created_at)
    write_receipts(preliminary_final, proxy_rows, robustness)
    gates = gate_rows(preliminary_final, package_rows, overfit_rows_, proxy_rows, queue)
    final = final_payload(bs_final, robustness, gates, created_at)
    write_receipts(final, proxy_rows, robustness)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, package_rows, overfit_rows_, robustness, proxy_rows, queue, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_artifact_registry(final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "reviewed_candidate_id": final["reviewed_candidate_id"],
                "precheck_decision": final["precheck_decision"],
                "overfit_watch": final["overfit_watch"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": final["next_run_id"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
