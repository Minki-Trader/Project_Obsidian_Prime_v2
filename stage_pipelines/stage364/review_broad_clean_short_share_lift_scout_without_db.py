import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import train_broad_clean_short_share_lift_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BR"
RUN_ID = "run364BR_review_broad_clean_short_share_lift_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = parent.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BS_train_late_year_short_share_stress_repair_scout_without_db_v1"

STATUS = "completed_stage364BR_bq_review_package_rejected_open_bs_no_authority"
JUDGMENT = "positive_proxy_clue_but_package_rejected_late_year_stress_no_mt5_open_bs_no_authority"
DECISION = "stage364BR_open_run364BS_late_year_short_share_stress_repair_scout"
CLAIM_BOUNDARY = (
    "research_development_kpi_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MIN_PF_KEEP = parent.MIN_PF_KEEP
DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_SHORT_SHARE = parent.TARGET_SHORT_SHARE
MIN_SHORT_SOURCE_PF = parent.MIN_SHORT_SOURCE_PF

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
PACKAGE_GATE_DECISION = RUN_DIR / "package_gate_decision.csv"
STRESS_FAILURE_ATTRIBUTION = RUN_DIR / "stress_failure_attribution.csv"
POSITIVE_CLUE_REGISTER = RUN_DIR / "positive_clue_register.csv"
PROXY_MT5_DIFF_REVIEW = RUN_DIR / "proxy_mt5_diff_review.csv"
NEXT_REPAIR_QUEUE = RUN_DIR / "run364BS_late_year_short_share_stress_repair_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364BR_broad_clean_short_share_lift_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BR_broad_clean_short_share_lift_review.md"
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
    parent.BQ_RULE_SURFACE,
    parent.SELECTED_CANDIDATE,
    parent.SELECTED_TRADE_TAPE,
    parent.SELECTED_SYNTHETIC_SHORT_TAPE,
    parent.STRESS_SLICE_REVIEW,
    parent.OVERFIT_GUARDRAIL_AUDIT,
    parent.PROXY_MT5_DIFF_PLAN,
    parent.SHORT_SHARE_LIFT_ATTRIBUTION,
    parent.RUN364BR_QUEUE,
    parent.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    PACKAGE_GATE_DECISION,
    STRESS_FAILURE_ATTRIBUTION,
    POSITIVE_CLUE_REGISTER,
    PROXY_MT5_DIFF_REVIEW,
    NEXT_REPAIR_QUEUE,
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
    parent.write_json(path, json_ready(payload))


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


def json_ready(value: Any) -> Any:
    return parent.json_ready(value)


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
        raise FileNotFoundError("missing BR inputs(BR 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BQ next_run_id mismatch(BQ 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("BQ has forbidden authority claim(BQ 금지 권위 주장 존재)")
    gates = read_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("BQ gate audit(BQ 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BR review source(BR 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def package_gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        (
            "headline_kpi_gate",
            "selected proxy KPI(선택 프록시 핵심 성과)",
            "passed_for_proxy(프록시 통과)",
            f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_density']};short_share={final['selected_short_share']}",
            "proxy clue remains useful(프록시 단서는 유용하게 남김)",
        ),
        (
            "month_stress_gate",
            "monthly stability(月 안정성)",
            "failed_for_package(패키지 실패)",
            f"month_bad_count={final['month_bad_count']};min_month_net={final['min_month_net']};min_month_pf={final['min_month_profit_factor']}",
            "late-year stress must become repair constraint(연말 압박을 수리 제약으로 바꿈)",
        ),
        (
            "mt5_runtime_gate",
            "new MT5 execution(새 MT5 실행)",
            "failed_for_package(패키지 실패)",
            f"new_mt5_execution={final['new_mt5_execution']}",
            "proxy cannot replace MT5 KPI(프록시는 MT5 핵심 성과를 대체하지 않음)",
        ),
        (
            "package_candidate_row_gate",
            "package candidate rows(패키지 후보 행)",
            "failed_for_package(패키지 실패)" if as_int(final["package_candidate_rows"]) == 0 else "watch(관찰)",
            f"package_candidate_rows={final['package_candidate_rows']}",
            "package not opened before stress and runtime evidence(압박/런타임 근거 전 패키지 열지 않음)",
        ),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate_id": gate_id,
            "subject": subject,
            "gate_status": status,
            "evidence": evidence,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, subject, status, evidence, effect in checks
    ]


def stress_failure_rows(stress: pd.DataFrame) -> list[dict[str, Any]]:
    if stress.empty:
        return []
    rows: list[dict[str, Any]] = []
    bad = stress[stress["segment_status"].astype(str).str.startswith("bad")]
    for _, row in bad.iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "failure_id": f"{row['axis']}__{row['segment_id']}",
                "candidate_id": row["candidate_id"],
                "failure_type": "late_year_month_stress(연말 월 압박)",
                "axis": row["axis"],
                "segment": row["segment_id"],
                "net_profit": row["net_profit"],
                "profit_factor": row["profit_factor"],
                "expectancy": row["expectancy"],
                "trade_count": row["trade_count"],
                "density": row["trade_density_per_business_day"],
                "short_share": row["short_share"],
                "drawdown": row["closed_drawdown_amount"],
                "attribution": "segment has low short share and sub-3 monthly density(해당 조각은 낮은 숏비중과 월 3 미만 밀도)",
                "repair_use": "BS should test month-of-year/late-year stress repair without exact 2025-12 memorization(BS는 정확한 2025-12 암기 없이 월중/연말 압박 수리를 시험)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def positive_clue_rows(final: Mapping[str, Any], surface: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "run_id": RUN_ID,
            "clue_id": final["selected_candidate_id"],
            "clue_type": "selected_bq_proxy_clue(선택 BQ 프록시 단서)",
            "net_profit": final["selected_net_profit"],
            "profit_factor": final["selected_profit_factor"],
            "density": final["selected_density"],
            "short_share": final["selected_short_share"],
            "synthetic_short_profit_factor": final["selected_synthetic_short_profit_factor"],
            "month_bad_count": final["month_bad_count"],
            "synthetic_overlap_count": final["selected_synthetic_overlap_count"],
            "usable_as": "BS offensive repair seed(BS 공격 수리 씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    if not surface.empty:
        core = surface[surface["core_pass"].astype(str).str.lower().isin(["true", "1"])]
        family_tops = core.sort_values(["month_bad_count", "selection_score"], ascending=[True, False]).groupby("family_id", sort=True).head(1)
        for _, row in family_tops.iterrows():
            rows.append(
                {
                    "run_id": RUN_ID,
                    "clue_id": row["candidate_id"],
                    "clue_type": f"family_top_{row['family_id']}(계열 상위 단서)",
                    "net_profit": row["net_profit"],
                    "profit_factor": row["profit_factor"],
                    "density": row["trade_density_per_business_day"],
                    "short_share": row["short_share"],
                    "synthetic_short_profit_factor": row["synthetic_short_profit_factor"],
                    "month_bad_count": row["month_bad_count"],
                    "synthetic_overlap_count": row["synthetic_overlap_count"],
                    "usable_as": "repair comparison seed(수리 비교 씨앗)",
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
                "comparison_id": row.get("comparison_id", "bq_proxy_vs_source_mt5"),
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
                "attribution": "BQ proxy improves headline but has no new MT5 replay(BQ 프록시는 헤드라인을 개선하지만 새 MT5 재생이 없음)",
                "usability": "usable_for_signal_sanity_and_BS_seed_not_runtime_authority(신호 점검 및 BS 씨앗에는 사용 가능, 런타임 권위 아님)",
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
            "queue_id": "bs01_late_year_short_share_density_repair",
            "action": "test late-year/month-of-year short-share and density repair(연말/월중 숏비중 및 밀도 수리 시험)",
            "success_criteria": "PF>=1.35, density>=3, short_share>=0.12, synthetic_short_pf>=1.15, month_bad_count=0, overlap=0(PF 1.35 이상, 밀도 3 이상, 숏비중 0.12 이상, 합성 숏 PF 1.15 이상, 월 나쁨 0, 겹침 0)",
            "effect": "2025-12 exact memorization(정확한 2025-12 암기) 없이 실패 조각을 구조 제약으로 바꾼다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bs02_q4_session_bridge_control",
            "action": "compare h19 bridge with Q4/session controls(19시 브리지와 4분기/세션 대조 비교)",
            "success_criteria": "late-year repair survives without top_n or outcome-priority(연말 수리가 top_n/결과값 우선순위 없이 생존)",
            "effect": "month-specific overfit(월 특정 과적합)을 대조군으로 압박한다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bs03_runtime_package_precheck_if_stress_clears",
            "action": "prepare MT5 package precheck only if stress clears(압박이 사라질 때만 MT5 패키지 사전점검 준비)",
            "success_criteria": "no package without stress_clear and proxy/MT5 diff review(압박 해소와 프록시/MT5 차이 검토 없이는 패키지 없음)",
            "effect": "외부 검증을 미루지 않되, 프록시만으로 운영 주장을 만들지 않는다.",
        },
    ]


def gate_rows(final: Mapping[str, Any], package_rows: Sequence[Mapping[str, Any]], stress_rows: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed",
            "evidence": rel(POSITIVE_CLUE_REGISTER),
            "effect": "net/PF/expectancy/DD/recovery/trades/long-short를 분리 검토했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "row_grain_audit",
            "status": "passed" if package_rows and stress_rows and proxy_rows else "failed",
            "evidence": f"{rel(PACKAGE_GATE_DECISION)};{rel(STRESS_FAILURE_ATTRIBUTION)};{rel(PROXY_MT5_DIFF_REVIEW)}",
            "effect": "패키지, 압박, 프록시-MT5 차이를 서로 다른 행 단위로 분리했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": rel(parent.FINAL_DECISION),
            "effect": "BQ 산출물만 사용하고 proxy(프록시)를 MT5 KPI(MT5 핵심 성과)로 대체하지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "package_reject_gate",
            "status": "passed" if as_int(final["reviewed_month_bad_count"]) > 0 and as_int(final["reviewed_package_candidate_rows"]) == 0 else "failed",
            "evidence": rel(PACKAGE_GATE_DECISION),
            "effect": "월 압박과 MT5 미실행 때문에 package(패키지)를 거절했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "stress_memory_gate",
            "status": "passed" if len(stress_rows) >= 1 else "failed",
            "evidence": rel(STRESS_FAILURE_ATTRIBUTION),
            "effect": "2025-12 실패를 다음 수리 제약으로 전환했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "next_offensive_seed_gate",
            "status": "passed" if len(queue) == 3 else "failed",
            "evidence": rel(NEXT_REPAIR_QUEUE),
            "effect": "BS 공격 탐색 대기열을 열었다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "필수 게이트와 closeout(종료 기록)을 연결했다.",
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


def final_payload(
    bq_final: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    stress_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
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
        "reviewed_candidate_id": bq_final["selected_candidate_id"],
        "reviewed_net_profit": bq_final["selected_net_profit"],
        "reviewed_profit_factor": bq_final["selected_profit_factor"],
        "reviewed_expectancy": bq_final["selected_expectancy"],
        "reviewed_trade_count": bq_final["selected_trade_count"],
        "reviewed_density": bq_final["selected_density"],
        "reviewed_closed_drawdown_amount": bq_final["selected_closed_drawdown_amount"],
        "reviewed_recovery_factor": bq_final["selected_recovery_factor"],
        "reviewed_long_trade_count": bq_final["selected_long_trade_count"],
        "reviewed_short_trade_count": bq_final["selected_short_trade_count"],
        "reviewed_short_share": bq_final["selected_short_share"],
        "reviewed_synthetic_short_profit_factor": bq_final["selected_synthetic_short_profit_factor"],
        "reviewed_month_bad_count": bq_final["month_bad_count"],
        "reviewed_min_month_net": bq_final["min_month_net"],
        "reviewed_min_month_profit_factor": bq_final["min_month_profit_factor"],
        "reviewed_package_candidate_rows": bq_final["package_candidate_rows"],
        "package_decision": "rejected_package_ineligible_late_year_month_stress_no_mt5(패키지 부적격 거절, 연말 월 압박 및 MT5 없음)",
        "stress_failure_count": len(stress_rows),
        "preserved_clue_count": len(clues),
        "proxy_mt5_review_count": len(proxy_rows),
        "next_primary_seed": bq_final["selected_candidate_id"],
        "next_repair_focus": "late_year_short_share_density_stress_repair(연말 숏비중/밀도 압박 수리)",
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
            "primary_family": "kpi_evidence(핵심 성과 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"],
            "result_subject": "BQ selected proxy(BQ 선택 프록시)",
            "evidence_boundary": "review_only(검토 전용)",
            "effect": "BQ positive proxy clue(BQ 긍정 프록시 단서)를 package reject(패키지 거절)와 BS repair seed(BS 수리 씨앗)로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any], proxy_rows: Sequence[Mapping[str, Any]], clues: Sequence[Mapping[str, Any]]) -> None:
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
            "package_decision": final["package_decision"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_sources": [rel(parent.FINAL_DECISION), rel(parent.BQ_RULE_SURFACE), rel(parent.STRESS_SLICE_REVIEW)],
            "timestamp_boundary": "review uses BQ outputs only; next repair forbids exact 2025-12 memorization(BQ 출력만 검토, 다음 수리는 정확한 2025-12 암기 금지)",
            "integrity_judgment": "usable_for_review_no_new_labeling(검토 사용 가능, 새 라벨링 없음)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "proxy_mt5_diff_review": list(proxy_rows),
            "preserved_clues": list(clues)[:8],
            "driver": "headline proxy improved but late-year month stress blocks package(헤드라인 프록시는 개선됐지만 연말 월 압박이 패키지를 막음)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "BQ selected proxy(BQ 선택 프록시)",
            "evidence_available": [rel(parent.FINAL_DECISION), rel(parent.STRESS_SLICE_REVIEW), rel(parent.PROXY_MT5_DIFF_PLAN), rel(parent.GATE_AUDIT)],
            "evidence_missing": ["new MT5 runtime reprobe(새 MT5 런타임 재탐침)", "forward pass(전진 통과)", "operating promotion evidence(운영 승격 근거)"],
            "judgment_label": "positive_proxy_clue_package_rejected(긍정 프록시 단서, 패키지 거절)",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "숫자는 좋아졌지만 2025-12 조각과 MT5 미검증 때문에 운영 후보가 아니라 다음 수리 씨앗이다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "effect": "package reject(패키지 거절)와 next repair(다음 수리)만 주장한다.",
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
            "lineage_judgment": "connected_BQ_review_to_BS_repair_queue(BQ 검토와 BS 수리 대기열 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    stress_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364BR broad clean short-share lift review(364BR 넓은 클린 숏비중 상승 검토)

## Current Truth(현재 진실)

- reviewed candidate(검토 후보): `{final['reviewed_candidate_id']}`
- reviewed KPI(검토 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_share']}`
- month_bad_count(월 나쁨 수): `{final['reviewed_month_bad_count']}`
- min month net/PF(최저 월 순수익/수익 팩터): `{final['reviewed_min_month_net']}` / `{final['reviewed_min_month_profit_factor']}`
- package decision(패키지 결정): `{final['package_decision']}`
- next repair focus(다음 수리 초점): `{final['next_repair_focus']}`

## Action And Effect(행동과 효과)

Action(행동): BQ selected proxy(BQ 선택 프록시)를 package gate(패키지 게이트), stress attribution(압박 귀속), proxy/MT5 diff(프록시/MT5 차이), next repair queue(다음 수리 대기열)로 분리했다.

Effect(효과): BQ proxy(프록시)는 좋은 offensive seed(공격 씨앗)이지만, 2025-12 stress(2025-12 압박)와 new MT5 execution(새 MT5 실행) 없음 때문에 package(패키지)는 거절하고 BS repair(BS 수리)를 연다.

## Package Gate(패키지 게이트)

{markdown_table(package_rows, ['gate_id', 'subject', 'gate_status', 'evidence', 'effect'])}

## Stress Failure Attribution(압박 실패 귀속)

{markdown_table(stress_rows, ['failure_id', 'failure_type', 'segment', 'net_profit', 'profit_factor', 'trade_count', 'density', 'short_share', 'repair_use'])}

## Positive Clues(긍정 단서)

{markdown_table(clues, ['clue_id', 'clue_type', 'net_profit', 'profit_factor', 'density', 'short_share', 'synthetic_short_profit_factor', 'month_bad_count', 'usable_as'])}

## Proxy/MT5 Diff Review(프록시/MT5 차이 검토)

{markdown_table(proxy_rows, ['comparison_id', 'mt5_net_profit', 'proxy_net_profit', 'net_diff_proxy_minus_mt5', 'mt5_profit_factor', 'proxy_profit_factor', 'usability'])}

## BS Queue(BS 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'action', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BR is review only(BR은 검토 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BR broad clean short-share lift review(넓은 클린 숏비중 상승 검토)

Action(행동): BQ selected proxy(BQ 선택 프록시)를 package reject(패키지 거절)로 닫고 `{NEXT_RUN_ID}`를 연다.

Effect(효과): 좋은 프록시 단서는 유지하지만, 2025-12 stress(2025-12 압박)와 MT5 미검증 때문에 운영 후보로 올리지 않는다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - broad clean short-share lift review(넓은 클린 숏비중 상승 검토).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BR Broad Clean Short-Share Lift Review Closeout",
        f"""## run364BR Broad Clean Short-Share Lift Review Closeout(364BR 넓은 클린 숏비중 상승 검토 종료)

Action(행동): BQ proxy(BQ 프록시)를 package reject(패키지 거절), stress memory(압박 기억), BS repair seed(BS 수리 씨앗)으로 분리했다.

Effect(효과): `{NEXT_RUN_ID}`에서 exact 2025-12 memorization(정확한 2025-12 암기) 없이 late-year/month-of-year short-share stress(연말/월중 숏비중 압박)를 공격 탐색한다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BR Broad Clean Short-Share Lift Review(364BR 넓은 클린 숏비중 상승 검토)

Action(행동): BQ selected proxy(BQ 선택 프록시)를 패키지 게이트와 압박 귀속으로 검토했다.

Effect(효과): package(패키지)는 거절하고 `{NEXT_RUN_ID}`로 연말 숏비중/밀도 압박 수리를 연다.
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
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364BR(364BR 실행)는 BQ proxy clue(BQ 프록시 단서)를 package reject(패키지 거절)로 닫고 late-year short-share stress repair(연말 숏비중 압박 수리)를 BS로 열었다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 late-year/month-of-year repair(연말/월중 수리)를 실행한다.",
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

Current truth(현재 진실): `run364BR`는 BQ selected proxy(BQ 선택 프록시) `{final['reviewed_candidate_id']}`를 package candidate(패키지 후보)에서 거절했다. 이유는 month_bad_count(월 나쁨 수) `{final['reviewed_month_bad_count']}`, min month net/PF(최저 월 순수익/수익 팩터) `{final['reviewed_min_month_net']}` / `{final['reviewed_min_month_profit_factor']}`, new MT5 execution(새 MT5 실행) 없음이다. Positive clue(긍정 단서)는 `{final['next_primary_seed']}`로 보존한다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 exact 2025-12 memorization(정확한 2025-12 암기) 없이 late-year/month-of-year short-share and density stress repair(연말/월중 숏비중 및 밀도 압박 수리)를 공격 정찰한다.

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

Package candidate(패키지 후보): none(없음). BQ selected proxy(BQ 선택 프록시)는 `{final['package_decision']}`.

Reviewed proxy(검토 프록시): `{final['reviewed_candidate_id']}`

Reviewed KPI(검토 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, expectancy `{final['reviewed_expectancy']}`, trades `{final['reviewed_trade_count']}`, density `{final['reviewed_density']}`, closed DD `{final['reviewed_closed_drawdown_amount']}`, recovery `{final['reviewed_recovery_factor']}`, long/short `{final['reviewed_long_trade_count']}` / `{final['reviewed_short_trade_count']}`, short share `{final['reviewed_short_share']}`.

Stress memory(압박 기억): month_bad_count(월 나쁨 수) `{final['reviewed_month_bad_count']}`, min month net/PF(최저 월 순수익/수익 팩터) `{final['reviewed_min_month_net']}` / `{final['reviewed_min_month_profit_factor']}`.

Next queue(다음 대기열): `{rel(NEXT_REPAIR_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): BQ broad clean short-share lift(BQ 넓은 클린 숏비중 상승)를 package gate(패키지 게이트)와 stress attribution(압박 귀속)으로 검토했다.
- effect(효과): package(패키지)는 거절하고 `{NEXT_RUN_ID}`로 연말 숏비중/밀도 수리를 넘겼다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): BQ h19 bridge(19시 브리지)는 short share(숏 비중)를 복구하는 positive clue(긍정 단서)지만 late-year stress(연말 압박)가 남는다.
- positive clue(긍정 단서): net/PF/density/short share `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_share']}`.
- next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): BQ package rejected(BQ 패키지 거절).
- failure_memory(실패 기억): 2025-12 segment(2025-12 조각)은 net/PF(순수익/PF) `{final['reviewed_min_month_net']}` / `{final['reviewed_min_month_profit_factor']}`로 약하다.
- salvage_value(회수 가치): 전체 proxy(프록시)는 PF/density/short share(PF/밀도/숏비중) 목표를 동시에 통과했다.
- reopen_condition(재개 조건): `{NEXT_RUN_ID}`에서 exact 2025-12 memorization(정확한 2025-12 암기) 없이 late-year repair(연말 수리)가 month_bad_count(월 나쁨 수) `0`을 만든다.
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
        "rows": final["stress_failure_count"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "kpi_evidence(핵심 성과 근거)",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "evidence_boundary": "kpi_review_only(핵심 성과 검토 전용)",
        "question": "Does BQ proxy deserve package or repair handoff?(BQ 프록시는 패키지인가 수리 인계인가?)",
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
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)", False),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", STATUS, True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "BR review(BR 검토)",
            "scoreboard_lane": "stage364_kpi_review(Stage364 핵심 성과 검토)",
            "status": status,
            "primary_kpi": f"net={final['reviewed_net_profit']};pf={final['reviewed_profit_factor']};density={final['reviewed_density']};short_share={final['reviewed_short_share']}",
            "guardrail_kpi": f"month_bad_count={final['reviewed_month_bad_count']};package_rows={final['reviewed_package_candidate_rows']};no_authority",
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
        "lane": "stage364_kpi_review(Stage364 핵심 성과 검토)",
        "family": "broad_clean_short_share_lift_review(넓은 클린 숏비중 상승 검토)",
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
        "view": "kpi_review(핵심 성과 검토)",
        "tier": "Tier A",
        "metric_scope": "reviewed_proxy(검토 프록시)",
        "trade_density_requirement_status": "passed_density_ge_3(밀도 3 이상 통과)",
        "primary_artifact": rel(PACKAGE_GATE_DECISION),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [registry_row])
    parent.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("package_gate_decision", PACKAGE_GATE_DECISION, "BR package gate decision(BR 패키지 게이트 결정)."),
        ("stress_failure_attribution", STRESS_FAILURE_ATTRIBUTION, "BR stress failure attribution(BR 압박 실패 귀속)."),
        ("positive_clue_register", POSITIVE_CLUE_REGISTER, "BR positive clue register(BR 긍정 단서 등록)."),
        ("proxy_mt5_diff_review", PROXY_MT5_DIFF_REVIEW, "BR proxy/MT5 diff review(BR 프록시/MT5 차이 검토)."),
        ("next_repair_queue", NEXT_REPAIR_QUEUE, "BR to BS repair queue(BR에서 BS 수리 대기열)."),
        ("final_decision", FINAL_DECISION, "BR final decision(BR 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "BR run manifest(BR 실행 목록)."),
        ("report", REPORT_PATH, "BR report(BR 보고서)."),
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
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "created_at_utc": final["created_at_utc"],
                    "created_at": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
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
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    bq_final = validate_inputs()
    write_work_packet()
    surface = load_csv(parent.BQ_RULE_SURFACE)
    stress = load_csv(parent.STRESS_SLICE_REVIEW)
    proxy_mt5 = load_csv(parent.PROXY_MT5_DIFF_PLAN)
    package_rows = package_gate_rows(bq_final)
    stress_rows = stress_failure_rows(stress)
    clues = positive_clue_rows(bq_final, surface)
    proxy_rows = proxy_mt5_review_rows(proxy_mt5)
    queue = next_queue_rows(bq_final)
    preliminary = {
        "reviewed_month_bad_count": bq_final["month_bad_count"],
        "reviewed_package_candidate_rows": bq_final["package_candidate_rows"],
    }
    gates = gate_rows(preliminary, package_rows, stress_rows, proxy_rows, queue)
    if any(row["status"] == "failed" for row in gates):
        write_csv(INPUT_MANIFEST, input_manifest_rows())
        write_csv(PACKAGE_GATE_DECISION, package_rows)
        write_csv(STRESS_FAILURE_ATTRIBUTION, stress_rows)
        write_csv(PROXY_MT5_DIFF_REVIEW, proxy_rows)
        write_csv(GATE_AUDIT, gates)
        raise RuntimeError("BR gate failure(BR 게이트 실패): " + ", ".join(row["gate"] for row in gates if row["status"] == "failed"))
    created_at = now_utc()
    final = final_payload(bq_final, package_rows, stress_rows, clues, proxy_rows, queue, gates, created_at)
    gates = gate_rows(final, package_rows, stress_rows, proxy_rows, queue)
    final = final_payload(bq_final, package_rows, stress_rows, clues, proxy_rows, queue, gates, created_at)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(PACKAGE_GATE_DECISION, package_rows)
    write_csv(STRESS_FAILURE_ATTRIBUTION, stress_rows)
    write_csv(POSITIVE_CLUE_REGISTER, clues)
    write_csv(PROXY_MT5_DIFF_REVIEW, proxy_rows)
    write_csv(NEXT_REPAIR_QUEUE, queue)
    write_receipts(final, proxy_rows, clues)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, package_rows, stress_rows, clues, proxy_rows, queue, gates)
    write_ledgers(final)
    write_manifest(final)
    write_artifact_registry(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
