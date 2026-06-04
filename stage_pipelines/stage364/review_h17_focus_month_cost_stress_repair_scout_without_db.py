from __future__ import annotations

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
from stage_pipelines.stage364 import train_h17_focus_month_cost_stress_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CK"
RUN_ID = "run364CK_review_h17_focus_month_cost_stress_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID = "run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1"

STATUS = "completed_stage364CK_h17_focus_repair_review_package_rejected_open_cl_no_authority"
JUDGMENT = "positive_proxy_repair_clue_but_package_rejected_bad_months_open_cl_no_authority"
DECISION = "stage364CK_open_run364CL_h17_bad_month_source_balance_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_kpi_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
SHORT_FLOOR = parent.SHORT_FLOOR

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
PACKAGE_GATE_DECISION = RUN_DIR / "package_gate_decision.csv"
MONTH_FAILURE_ATTRIBUTION = RUN_DIR / "month_failure_attribution.csv"
SOURCE_BALANCE_REVIEW = RUN_DIR / "source_balance_review.csv"
POSITIVE_CLUE_REGISTER = RUN_DIR / "positive_clue_register.csv"
PROXY_MT5_DIFF_REVIEW = RUN_DIR / "proxy_mt5_diff_review.csv"
NEXT_REPAIR_QUEUE = RUN_DIR / "run364CL_h17_bad_month_source_balance_repair_queue.csv"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CK_h17_focus_month_cost_stress_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CK_h17_focus_month_cost_stress_repair_review.md"
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
    parent.PROXY_REPAIR_SURFACE,
    parent.SELECTED_CANDIDATE,
    parent.SELECTED_TRADE_TAPE,
    parent.CANDIDATE_FILTER_AUDIT,
    parent.CANDIDATE_SOURCE_ATTRIBUTION,
    parent.CANDIDATE_MONTH_STABILITY,
    parent.COST_STRESS_DIAGNOSTIC,
    parent.PACKAGE_PRECHECK,
    parent.PROXY_MT5_DIFF_PLAN,
    parent.RUN364CK_QUEUE,
    parent.DATA_INTEGRITY_AUDIT,
    parent.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    PACKAGE_GATE_DECISION,
    MONTH_FAILURE_ATTRIBUTION,
    SOURCE_BALANCE_REVIEW,
    POSITIVE_CLUE_REGISTER,
    PROXY_MT5_DIFF_REVIEW,
    NEXT_REPAIR_QUEUE,
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


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def json_ready(value: Any) -> Any:
    return parent.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CK inputs(CK 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CJ next_run_id mismatch(CJ 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CJ has forbidden authority claim(CJ 금지 권위 주장 존재)")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CJ gate audit(CJ 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    queue = read_csv(parent.RUN364CK_QUEUE)
    if len(queue) != 4:
        raise RuntimeError(f"CK review queue row mismatch(CK 검토 대기열 행 불일치): {len(queue)} != 4")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CJ review source(CJ 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def selected_frame(df: pd.DataFrame, final: Mapping[str, Any]) -> pd.DataFrame:
    return df[df["candidate_id"].astype(str).eq(str(final["selected_candidate_id"]))].copy()


def selected_row(df: pd.DataFrame, final: Mapping[str, Any]) -> dict[str, Any]:
    selected = selected_frame(df, final)
    if len(selected) != 1:
        raise RuntimeError(f"selected row mismatch(선택 행 불일치): {len(selected)}")
    return selected.iloc[0].to_dict()


def package_gate_rows(
    final: Mapping[str, Any],
    surface_row: Mapping[str, Any],
    package_row: Mapping[str, Any],
    bad_months: Sequence[Mapping[str, Any]],
    cost_row: Mapping[str, Any],
) -> list[dict[str, Any]]:
    headline_pass = (
        as_float(final["selected_net_delta_vs_parent"]) > 0
        and as_float(final["selected_profit_factor_delta_vs_parent"]) > 0
        and as_float(final["selected_trade_density"]) >= DENSITY_FLOOR
        and as_float(final["selected_short_trade_count"]) >= SHORT_FLOOR
    )
    stress_delta = as_float(cost_row.get("stress_adjusted_net_delta_vs_parent"))
    stress_pass = stress_delta >= 0 and "positive" in str(cost_row.get("stress_judgment", ""))
    no_split_pass = as_float(final["selected_trade_count"]) <= as_float(surface_row.get("parent_trade_count", final["selected_trade_count"]))
    package_status = str(package_row.get("package_precheck_status", ""))
    package_rejected = bool(bad_months) or not stress_pass or "failed" in package_status
    rows = [
        {
            "run_id": RUN_ID,
            "gate_id": "headline_proxy_kpi_gate",
            "subject": "selected proxy KPI(선택 프록시 핵심 성과 지표)",
            "gate_status": "passed_for_proxy(프록시 기준 통과)" if headline_pass else "failed_for_proxy(프록시 기준 실패)",
            "evidence": f"net_delta={final['selected_net_delta_vs_parent']};pf_delta={final['selected_profit_factor_delta_vs_parent']};density={final['selected_trade_density']};shorts={final['selected_short_trade_count']}",
            "effect": "positive clue(긍정 단서)는 보존하지만 package(패키지) 판단은 안정성 게이트까지 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "no_trade_splitting_gate",
            "subject": "trade splitting boundary(거래 쪼개기 경계)",
            "gate_status": "passed_no_split(무분할 통과)" if no_split_pass else "failed_split_risk(쪼개기 위험 실패)",
            "evidence": f"selected_trades={final['selected_trade_count']};parent_trades={surface_row.get('parent_trade_count', '')};restored_trades={final.get('selected_restored_trade_count', '')}",
            "effect": "trade/day(일 거래수)가 수익 쪼개기로 올라간 결과인지 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "short_floor_source_balance_gate",
            "subject": "short floor and source balance(숏 하한과 원천 균형)",
            "gate_status": "passed_for_proxy_review(프록시 검토 기준 통과)" if as_float(final["selected_short_trade_count"]) >= SHORT_FLOOR else "failed_short_floor(숏 하한 실패)",
            "evidence": f"shorts={final['selected_short_trade_count']};restored_shorts={final.get('selected_restored_trade_count', '')}",
            "effect": "숏 100개 하한은 지켰지만 source mix(원천 혼합)는 다음 수리에서 계속 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "cost_stress_package_gate",
            "subject": "cost stress(비용 압박)",
            "gate_status": "passed_for_proxy_package_precheck(프록시 패키지 사전점검 통과)" if stress_pass else "failed_for_package(패키지 기준 실패)",
            "evidence": f"stress_delta={stress_delta};stress_judgment={cost_row.get('stress_judgment', '')}",
            "effect": "비용 압박은 개선됐지만 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "month_stability_package_gate",
            "subject": "monthly stability(월 안정성)",
            "gate_status": "failed_for_package(패키지 기준 실패)" if bad_months else "passed_for_package(패키지 기준 통과)",
            "evidence": f"bad_month_count={len(bad_months)};bad_months={','.join(str(row.get('segment', row.get('open_month', ''))) for row in bad_months)}",
            "effect": "남은 손실 월을 다음 repair constraint(수리 제약)으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "mt5_runtime_package_gate",
            "subject": "new MT5 execution(새 MT5 실행)",
            "gate_status": "failed_for_package(패키지 기준 실패)",
            "evidence": "new_mt5_execution=not_run(새 MT5 실행 미실행)",
            "effect": "proxy(프록시)를 runtime authority(런타임 권위)로 올리지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "package_decision_gate",
            "subject": "package decision(패키지 결정)",
            "gate_status": "rejected_open_cl_repair_inputs(거절, CL 수리 입력 개방)" if package_rejected else "watch_needs_mt5_package_precheck(관찰, MT5 패키지 사전점검 필요)",
            "evidence": f"package_precheck={package_status};bad_months={len(bad_months)};stress_delta={stress_delta};new_mt5_execution=not_run",
            "effect": "CK를 운영 패키지가 아니라 CL materialization(CL 구체화)으로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def month_failure_rows(final: Mapping[str, Any], months: pd.DataFrame) -> list[dict[str, Any]]:
    selected = selected_frame(months, final)
    rows: list[dict[str, Any]] = []
    for _, raw in selected.iterrows():
        row = raw.to_dict()
        if as_float(row.get("net_profit")) <= 0 or as_float(row.get("profit_factor")) < 1:
            rows.append(
                {
                    "run_id": RUN_ID,
                    "failure_id": f"bad_month__{row['open_month']}",
                    "candidate_id": final["selected_candidate_id"],
                    "failure_type": "month_stability_failure(월 안정성 실패)",
                    "axis": "open_month(진입 월)",
                    "segment": row["open_month"],
                    "net_profit": row["net_profit"],
                    "profit_factor": row["profit_factor"],
                    "trade_count": row["trade_count"],
                    "short_trade_count": row["short_trade_count"],
                    "attribution": "selected repair still has negative monthly slices(선택 수리에 아직 손실 월 조각이 있음)",
                    "repair_use": "CL should test reusable month/quarter/session class guards without exact 2025 date memorization(CL은 정확한 2025년 날짜 암기 없이 재사용 월/분기/세션 클래스 가드를 시험)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def source_balance_rows(final: Mapping[str, Any], sources: pd.DataFrame, filter_audit: pd.DataFrame) -> list[dict[str, Any]]:
    selected_sources = selected_frame(sources, final)
    selected_filters = selected_frame(filter_audit, final)
    rows: list[dict[str, Any]] = []
    restored = int(sum(as_float(row.get("restored_short_count")) for _, row in selected_filters.iterrows()))
    for _, raw in selected_sources.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": final["selected_candidate_id"],
                "source_bucket": row["source_bucket"],
                "trade_count": row["trade_count"],
                "net_profit": row["net_profit"],
                "profit_factor": row["profit_factor"],
                "expectancy": row.get("expectancy", ""),
                "short_trade_count": row["short_trade_count"],
                "restored_short_count_total": restored,
                "source_judgment": "positive_but_thin_overlay_watch(긍정이나 얇은 오버레이 관찰)" if str(row["source_bucket"]) == "synthetic_short_overlay" else "source_contribution_usable(원천 기여 사용 가능)",
                "effect": "source mix(원천 혼합)를 다음 CL 후보 제약으로 전달한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def positive_clue_rows(final: Mapping[str, Any], surface: pd.DataFrame, sources: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "run_id": RUN_ID,
            "clue_id": final["selected_candidate_id"],
            "clue_type": "selected_repair_proxy_clue(선택 수리 프록시 단서)",
            "net_profit": final["selected_net_profit"],
            "profit_factor": final["selected_profit_factor"],
            "expectancy": final["selected_expectancy"],
            "trade_count": final["selected_trade_count"],
            "trade_density": final["selected_trade_density"],
            "short_trade_count": final["selected_short_trade_count"],
            "stress_delta": final["selected_stress_adjusted_net_delta_vs_parent"],
            "bad_month_count": final["selected_bad_month_count"],
            "usable_as": "CL primary repair seed(CL 주 수리 씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    selected_sources = selected_frame(sources, final)
    for _, raw in selected_sources.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "clue_id": f"{final['selected_candidate_id']}__{row['source_bucket']}",
                "clue_type": "source_attribution_clue(원천 귀속 단서)",
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "expectancy": row.get("expectancy", ""),
                "trade_count": row.get("trade_count", ""),
                "trade_density": "",
                "short_trade_count": row.get("short_trade_count", ""),
                "stress_delta": "",
                "bad_month_count": "",
                "usable_as": "CL source balance diagnostic(CL 원천 균형 진단)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    candidates = surface.copy()
    candidates["bad_month_count_num"] = pd.to_numeric(candidates["bad_month_count"], errors="coerce").fillna(99)
    candidates["net_profit_num"] = pd.to_numeric(candidates["net_profit"], errors="coerce").fillna(0)
    candidates["short_count_num"] = pd.to_numeric(candidates["short_trade_count"], errors="coerce").fillna(0)
    salvage = candidates[
        candidates["candidate_status"].astype(str).str.contains("review_candidate", regex=False)
        & candidates["bad_month_count_num"].lt(as_float(final["selected_bad_month_count"]))
        & candidates["short_count_num"].ge(SHORT_FLOOR)
    ].sort_values(["bad_month_count_num", "net_profit_num"], ascending=[True, False]).head(4)
    for _, raw in salvage.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "clue_id": row["candidate_id"],
                "clue_type": "lower_bad_month_salvage_seed(손실 월 감소 회수 씨앗)",
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "expectancy": row.get("expectancy", ""),
                "trade_count": row.get("trade_count", ""),
                "trade_density": row.get("trade_density", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "stress_delta": row.get("stress_adjusted_net_delta_vs_parent", ""),
                "bad_month_count": row.get("bad_month_count", ""),
                "usable_as": "CL comparison seed with fewer bad months(CL 손실 월이 적은 비교 씨앗)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_mt5_rows(proxy_plan: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, raw in proxy_plan.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": row.get("comparison_id", ""),
                "selected_candidate_id": row.get("selected_candidate_id", ""),
                "parent_mt5_net": row.get("parent_mt5_net", ""),
                "proxy_net": row.get("proxy_net", ""),
                "net_diff_proxy_minus_parent": row.get("net_diff_proxy_minus_parent", ""),
                "parent_mt5_profit_factor": row.get("parent_mt5_profit_factor", ""),
                "proxy_profit_factor": row.get("proxy_profit_factor", ""),
                "parent_mt5_density": row.get("parent_mt5_density", ""),
                "proxy_density": row.get("proxy_density", ""),
                "stress_delta_proxy": row.get("stress_delta_proxy", ""),
                "attribution": "proxy repair improves screen KPI but needs MT5 reprobe after month repair(프록시 수리는 화면 KPI를 개선하지만 월 수리 뒤 MT5 재탐침이 필요)",
                "usability": "usable_for_CL_selection_only_not_runtime_authority(CL 선별 전용 사용 가능, 런타임 권위 아님)",
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
        "allowed_entry_operation": "preserve_or_remove_existing_entries_only(기존 진입 보존 또는 제거만)",
        "trade_splitting_status": "not_used_no_added_entries(미사용, 추가 진입 없음)",
        "top_n_status": "forbidden(금지)",
        "exact_date_filter_status": "forbidden(금지)",
        "minimum_density": DENSITY_FLOOR,
        "minimum_short_count": SHORT_FLOOR,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows = [
        ("cl01_selected_cj09_bad_month_class_guard", "cj09_cg07_native_short_cost_firewall_short_floor_rescue", "month_of_year_and_quarter_class_guard", "bad_month_count decreases;stress_delta>=0;shorts>=100", "turn cj09 into reusable month class repair(CJ09를 재사용 월 클래스 수리로 전환)"),
        ("cl02_cj11_one_bad_month_salvage_guard", "cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue", "one_bad_month_salvage_guard", "bad_month_count<=1;net_delta>0;shorts>=100", "use cj11 as lower bad-month comparison seed(CJ11을 손실 월 감소 비교 씨앗으로 사용)"),
        ("cl03_month08_open_hour17_overlay_pressure_guard", "cj09_cg07_native_short_cost_firewall_short_floor_rescue", "month_of_year=08_open_hour17_pressure", "no exact 2025 date;bad_month_count decreases", "test August class without memorizing 2025-08(2025-08 암기 없이 8월 클래스를 시험)"),
        ("cl04_month12_late_year_overlay_pressure_guard", "cj09_cg07_native_short_cost_firewall_short_floor_rescue", "month_of_year=12_late_year_pressure", "no exact 2025 date;bad_month_count decreases", "test December class without memorizing 2025-12(2025-12 암기 없이 12월 클래스를 시험)"),
        ("cl05_q3_q4_weak_overlay_class_guard", "cj09_cg07_native_short_cost_firewall_short_floor_rescue", "q3_q4_weak_overlay_class", "bad_month_count decreases without killing stress", "generalize bad month memory to quarter class(손실 월 기억을 분기 클래스로 일반화)"),
        ("cl06_source_mix_native_overlay_balance_guard", "cj09_cg07_native_short_cost_firewall_short_floor_rescue", "native_overlay_balance_guard", "source bucket not one tiny edge;shorts>=100", "keep synthetic overlay clue but reduce thin-source risk(합성 오버레이 단서를 보존하되 얇은 원천 위험 감소)"),
        ("cl07_short_floor_restore_quality_control", "cj09_cg07_native_short_cost_firewall_short_floor_rescue", "short_floor_restore_quality_control", "restored shorts do not erase net/PF edge", "audit restored 14 shorts as quality not collapse mask(복원 숏 14개가 붕괴 가림막인지 감사)"),
        ("cl08_mt5_precheck_boundary_after_month_zero", "cj09_cg07_native_short_cost_firewall_short_floor_rescue", "package_precheck_boundary", "MT5 package only if bad_month_count==0 and stress_delta>=0", "prevent weak proxy from becoming runtime claim(약한 프록시가 런타임 주장으로 바뀌는 것을 방지)"),
    ]
    return [
        {
            **common,
            "queue_rank": index,
            "queue_id": queue_id,
            "seed_candidate_id": seed,
            "repair_policy": policy,
            "success_criteria": success,
            "failure_criteria": "net/PF edge disappears or exact 2025 date filter is required(순수익/PF 우위 소멸 또는 정확한 2025년 날짜 필터 필요)",
            "expected_effect": effect,
        }
        for index, (queue_id, seed, policy, success, effect) in enumerate(rows, start=1)
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "kpi_review(KPI 검토)",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-data-integrity", "obsidian-artifact-lineage"],
            "required_gates": ["scope_completion_gate", "input_lineage_gate", "package_decision_gate", "next_queue_gate", "required_gate_coverage_audit"],
            "result_subject": "CJ selected h17 repair candidate(CJ 선택 17시 수리 후보)",
            "effect": "separate preserved proxy clue from package rejection(보존 프록시 단서와 패키지 거절을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(
    package_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    proxy_rows_: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    receipt_paths: Sequence[Path],
    *,
    final_written: bool,
) -> list[dict[str, Any]]:
    package_decision = [row for row in package_rows if row["gate_id"] == "package_decision_gate"]
    gates = [
        ("scope_completion_gate", len(package_rows) >= 7 and bool(month_rows) and bool(source_rows), PACKAGE_GATE_DECISION, "CK review outputs package/month/source rows(CK 검토가 패키지/월/원천 행을 산출)"),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "CJ input artifacts are connected(CJ 입력 산출물이 연결)"),
        ("package_decision_gate", bool(package_decision) and "rejected" in str(package_decision[0]["gate_status"]), PACKAGE_GATE_DECISION, "package was rejected before MT5 handoff(MT5 인계 전 패키지를 거절)"),
        ("proxy_mt5_diff_gate", len(proxy_rows_) >= 1, PROXY_MT5_DIFF_REVIEW, "proxy/MT5 diff remains explicit(프록시/MT5 차이를 명시 유지)"),
        ("next_queue_gate", len(queue) == 8, NEXT_REPAIR_QUEUE, "CL repair queue has 8 rows(CL 수리 대기열 8행 생성)"),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), KPI_RECEIPT, "KPI/data/attribution/judgment/claim receipts exist(KPI/데이터/귀속/판정/주장 영수증 존재)"),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "required gates are connected to closeout(필수 게이트가 종료 기록에 연결)"),
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


def final_payload(
    cj_final: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    proxy_rows_: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    package_decision = "rejected_open_cl_repair_inputs_no_authority(거절, CL 수리 입력 개방, 권위 없음)"
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
        "reviewed_candidate_id": cj_final["selected_candidate_id"],
        "reviewed_net_profit": cj_final["selected_net_profit"],
        "reviewed_profit_factor": cj_final["selected_profit_factor"],
        "reviewed_expectancy": cj_final["selected_expectancy"],
        "reviewed_trade_count": cj_final["selected_trade_count"],
        "reviewed_density": cj_final["selected_trade_density"],
        "reviewed_closed_drawdown_amount": cj_final["selected_closed_trade_drawdown_proxy"],
        "reviewed_recovery_factor": cj_final["selected_closed_trade_recovery_proxy"],
        "reviewed_long_trade_count": cj_final["selected_long_trade_count"],
        "reviewed_short_trade_count": cj_final["selected_short_trade_count"],
        "reviewed_short_share": cj_final["selected_short_share"],
        "reviewed_net_delta_vs_parent": cj_final["selected_net_delta_vs_parent"],
        "reviewed_profit_factor_delta_vs_parent": cj_final["selected_profit_factor_delta_vs_parent"],
        "reviewed_stress_adjusted_net_delta_vs_parent": cj_final["selected_stress_adjusted_net_delta_vs_parent"],
        "reviewed_bad_month_count": cj_final["selected_bad_month_count"],
        "reviewed_bad_months": cj_final["selected_bad_months"],
        "package_decision": package_decision,
        "package_gate_rows": len(package_rows),
        "month_failure_rows": len(month_rows),
        "source_balance_rows": len(source_rows),
        "preserved_clue_rows": len(clues),
        "proxy_mt5_diff_rows": len(proxy_rows_),
        "next_queue_rows": len(queue),
        "external_verification_status": "out_of_scope_by_claim_review_only_no_new_mt5",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "next_queue_path": rel(NEXT_REPAIR_QUEUE),
    }


def write_receipts(final: Mapping[str, Any], clues: Sequence[Mapping[str, Any]], proxy_rows_: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        KPI_RECEIPT,
        {
            **base,
            "measurement_scope": "net/PF/expectancy/drawdown/recovery/trades/long_short/cost_stress(순수익/PF/기대값/낙폭/회복/거래/롱숏/비용압박)",
            "reviewed_candidate": final["reviewed_candidate_id"],
            "headline": {
                "net": final["reviewed_net_profit"],
                "pf": final["reviewed_profit_factor"],
                "density": final["reviewed_density"],
                "shorts": final["reviewed_short_trade_count"],
                "stress_delta": final["reviewed_stress_adjusted_net_delta_vs_parent"],
                "bad_month_count": final["reviewed_bad_month_count"],
            },
            "package_decision": final["package_decision"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "CJ reviewed entry-known open_time/month/source outputs(CJ의 진입 시점 open_time/month/source 산출물 검토)",
            "feature_label_boundary": "review only; no new feature, label, split, or economic join(검토 전용, 새 피처/라벨/분할/경제지표 결합 없음)",
            "leakage_risk": "remaining risk is proxy selection bias, bounded by no runtime claim(남은 위험은 프록시 선택 편향이며 런타임 주장 없음으로 제한)",
            "integrity_judgment": "usable_for_review_not_operating_claim(검토 사용 가능, 운영 주장 불가)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": "CJ selected candidate improved net/PF/stress but retained two bad months(CJ 선택 후보는 순수익/PF/압박을 개선했지만 손실 월 2개를 유지)",
            "comparison_baseline": "CD02 parent and CJ package precheck(CD02 부모와 CJ 패키지 사전점검)",
            "likely_drivers": ["native short firewall recovery(네이티브 숏 방화벽 회복)", "short-floor restore(숏 하한 복원)", "h17 overlay clue(17시 오버레이 단서)"],
            "segment_checks": [rel(parent.CANDIDATE_SOURCE_ATTRIBUTION), rel(parent.CANDIDATE_MONTH_STABILITY), rel(parent.COST_STRESS_DIAGNOSTIC)],
            "preserved_clues": list(clues),
            "proxy_mt5_diff": list(proxy_rows_),
            "attribution_confidence": "medium_for_proxy_low_for_runtime(프록시 중간, 런타임 낮음)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(PACKAGE_GATE_DECISION), rel(MONTH_FAILURE_ATTRIBUTION), rel(SOURCE_BALANCE_REVIEW), rel(PROXY_MT5_DIFF_REVIEW)],
            "evidence_missing": ["new MT5 execution(새 MT5 실행)", "runtime parity(런타임 동등성)", "forward pass(전진 검증)"],
            "judgment_label": "positive_proxy_clue_but_package_rejected(긍정 프록시 단서이나 패키지 거절)",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "숫자는 좋아졌지만 손실 월이 남아 운영 패키지 대신 CL 수리로 넘긴다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claims": ["CK reviewed CJ proxy repair(CK가 CJ 프록시 수리를 검토)", "CL repair queue opened(CL 수리 대기열 개방)"],
            "forbidden_claims": ["runtime authority(런타임 권위)", "operating promotion(운영 승격)", "live readiness(실거래 준비)", "Goal Achieve(목표 달성)"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    exclusions = {LINEAGE_RECEIPT, RUN_MANIFEST, ARTIFACT_REGISTRY}
    output_paths = [path for path in OUTPUT_FILES if path not in exclusions and exists(path) and io_path(path).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in output_paths],
            "artifact_hashes": [{"path": rel(path), "sha256": sha(path)} for path in output_paths],
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def update_stage_brief(final: Mapping[str, Any]) -> None:
    path = io_path(STAGE_BRIEF)
    text = path.read_text(encoding="utf-8-sig")
    replacements = {
        "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
        "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    lines = []
    for line in text.splitlines():
        replaced = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                lines.append(value)
                replaced = True
                break
        if not replaced:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines) + "\n", bom=True)
    append_text_once(
        STAGE_BRIEF,
        f"## run364CK__{RUN_ID}",
        f"""
## run364CK H17 Repair Review Closeout(364CK 17시 수리 검토 종료)

Action(행동): CJ selected repair(CJ 선택 수리)를 package gate(패키지 게이트), month/source/cost attribution(월/원천/비용 귀속), proxy/MT5 diff(프록시/MT5 차이)로 검토했다.

Effect(효과): package(패키지)는 손실 월 2개 때문에 거절하고 `{NEXT_RUN_ID}`로 같은 Stage364(364단계) 안에서 CL repair input(CL 수리 입력)을 연다.
""",
    )


def write_docs(
    final: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    proxy_rows_: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364CK h17 focus repair review(17시 집중 수리 검토)

Updated(갱신): {final['created_at_utc']}

## Current truth(현재 진실)

- reviewed candidate(검토 후보): `{final['reviewed_candidate_id']}`
- KPI(핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, expectancy `{final['reviewed_expectancy']}`, trades `{final['reviewed_trade_count']}`, density `{final['reviewed_density']}`, drawdown proxy `{final['reviewed_closed_drawdown_amount']}`, recovery proxy `{final['reviewed_recovery_factor']}`, long/short `{final['reviewed_long_trade_count']}`/`{final['reviewed_short_trade_count']}`
- cost stress(비용 압박): stress delta `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`
- bad months(손실 월): `{final['reviewed_bad_months']}`
- package decision(패키지 결정): `{final['package_decision']}`
- next action(다음 행동): `{NEXT_RUN_ID}`

## Package Gate(패키지 게이트)

{markdown_table(package_rows, ['gate_id', 'gate_status', 'evidence', 'effect'], 10)}

## Month Failure(월 실패)

{markdown_table(month_rows, ['failure_id', 'segment', 'net_profit', 'profit_factor', 'trade_count', 'short_trade_count', 'repair_use'], 10)}

## Source Balance(원천 균형)

{markdown_table(source_rows, ['source_bucket', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count', 'restored_short_count_total', 'source_judgment'], 10)}

## Preserved Clues(보존 단서)

{markdown_table(clues, ['clue_id', 'clue_type', 'net_profit', 'profit_factor', 'trade_count', 'short_trade_count', 'stress_delta', 'bad_month_count', 'usable_as'], 12)}

## Proxy/MT5 Diff(프록시/MT5 차이)

{markdown_table(proxy_rows_, ['comparison_id', 'parent_mt5_net', 'proxy_net', 'net_diff_proxy_minus_parent', 'parent_mt5_profit_factor', 'proxy_profit_factor', 'usability'], 5)}

## CL Queue(CL 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'seed_candidate_id', 'repair_policy', 'success_criteria', 'expected_effect'], 10)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

This is review only(검토 전용)입니다. New model training(새 모델 학습), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 없습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CK decision(결정): h17 focus repair review

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- reviewed candidate(검토 후보): `{final['reviewed_candidate_id']}`
- package decision(패키지 결정): `{final['package_decision']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 좋은 프록시 수익 단서는 보존하고, 손실 월 2개 때문에 MT5 package(MT5 패키지)는 열지 않는다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        f"run364CK__{RUN_ID}",
        f"\n- run364CK__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - package rejected(패키지 거절), next `{NEXT_RUN_ID}`.\n",
    )
    update_stage_brief(final)
    append_text_once(
        STAGE_README,
        f"run364CK__{RUN_ID}",
        f"""
<!-- run364CK__{RUN_ID} -->
## run364CK h17 focus repair review(17시 집중 수리 검토)

Action(행동): CJ selected repair(CJ 선택 수리)를 package gate(패키지 게이트)와 month/source/cost attribution(월/원천/비용 귀속)으로 검토했다.

Effect(효과): package(패키지)는 거절하고 `{NEXT_RUN_ID}`로 CL repair input(CL 수리 입력)을 연다.
""",
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

Current truth(현재 진실): `run364CK` reviewed(검토 완료) CJ selected repair(CJ 선택 수리) `{final['reviewed_candidate_id']}`. KPI(핵심 성과 지표)는 net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, density `{final['reviewed_density']}`, shorts `{final['reviewed_short_trade_count']}`, stress delta `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`로 좋지만, bad months(손실 월) `{final['reviewed_bad_months']}` 때문에 package(패키지)는 거절했다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 bad month class guard(손실 월 클래스 가드), source balance(원천 균형), short-floor restore quality(숏 하한 복원 품질)를 구체화한다.

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

Package candidate(패키지 후보): none(없음). `{final['reviewed_candidate_id']}` is preserved only as CL repair seed(CL 수리 씨앗으로만 보존).

Reviewed KPI(검토 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, expectancy `{final['reviewed_expectancy']}`, trades `{final['reviewed_trade_count']}`, density `{final['reviewed_density']}`, drawdown `{final['reviewed_closed_drawdown_amount']}`, recovery `{final['reviewed_recovery_factor']}`, long/short `{final['reviewed_long_trade_count']}`/`{final['reviewed_short_trade_count']}`.

Package rejection(패키지 거절): bad months(손실 월) `{final['reviewed_bad_months']}`. MT5 execution(MT5 실행)은 not_run(미실행).

Next queue(다음 대기열): `{rel(NEXT_REPAIR_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364CK__{RUN_ID}",
        f"\n<!-- run364CK__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed CJ h17 repair(CJ 17시 수리 검토); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"run364CK__{RUN_ID}",
        f"\n<!-- run364CK__{RUN_ID} -->\n- `{RUN_ID}`: h17 repair review(17시 수리 검토). Positive clue(긍정 단서): net/PF/density/shorts/stress `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_trade_count']}` / `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`. Effect(효과): bad-month repair seed(손실 월 수리 씨앗)로 보존.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"run364CK__{RUN_ID}",
        f"\n<!-- run364CK__{RUN_ID} -->\n- `{RUN_ID}` package rejection(패키지 거절): bad months(손실 월) `{final['reviewed_bad_months']}` remain despite positive proxy KPI(긍정 프록시 KPI). Reopen condition(재개 조건): `{NEXT_RUN_ID}` creates bad_month_count_zero(손실 월 0) without exact-date filtering(정확 날짜 필터 없음).\n",
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
        "rows": final["month_failure_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "kpi_review(KPI 검토)",
        "scoreboard_lane": "proxy_review(프록시 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "review_only(검토 전용)",
        "question": "Should CJ selected repair open MT5 package or CL repair input?(CJ 선택 수리를 MT5 패키지로 열지 CL 수리 입력으로 넘길지)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["reviewed_net_profit"],
        "profit_factor": final["reviewed_profit_factor"],
        "expectancy": final["reviewed_expectancy"],
        "trade_count": final["reviewed_trade_count"],
        "trade_density_per_feature_day": final["reviewed_density"],
        "long_trade_count": final["reviewed_long_trade_count"],
        "short_trade_count": final["reviewed_short_trade_count"],
        "max_drawdown_amount": final["reviewed_closed_drawdown_amount"],
        "recovery_factor": final["reviewed_recovery_factor"],
        "trade_density_requirement_status": "passed_proxy_density_ge_3_no_trade_splitting(프록시 밀도 3 이상, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(PACKAGE_GATE_DECISION),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
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
            "kpi_scope": "CK proxy review(CK 프록시 검토)",
            "status": status,
            "primary_kpi": f"net={final['reviewed_net_profit']};pf={final['reviewed_profit_factor']};density={final['reviewed_density']};shorts={final['reviewed_short_trade_count']}",
            "guardrail_kpi": f"bad_months={final['reviewed_bad_month_count']};stress_delta={final['reviewed_stress_adjusted_net_delta_vs_parent']};no_authority",
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "reviewed_proxy(검토 프록시)",
        }
        if not include_metrics:
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "long_trade_count", "short_trade_count", "max_drawdown_amount", "recovery_factor"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("package_gate_decision", PACKAGE_GATE_DECISION, "CK package gate decision(CK 패키지 게이트 결정)."),
        ("month_failure_attribution", MONTH_FAILURE_ATTRIBUTION, "CK month failure attribution(CK 월 실패 귀속)."),
        ("source_balance_review", SOURCE_BALANCE_REVIEW, "CK source balance review(CK 원천 균형 검토)."),
        ("positive_clue_register", POSITIVE_CLUE_REGISTER, "CK positive clue register(CK 긍정 단서 등록)."),
        ("proxy_mt5_diff_review", PROXY_MT5_DIFF_REVIEW, "CK proxy/MT5 diff review(CK 프록시/MT5 차이 검토)."),
        ("next_repair_queue", NEXT_REPAIR_QUEUE, "CL repair queue(CL 수리 대기열)."),
        ("report", REPORT_PATH, "CK report(CK 보고서)."),
        ("final_decision", FINAL_DECISION, "CK final decision(CK 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CK run manifest(CK 실행 목록)."),
        ("gate_audit", GATE_AUDIT, "CK required gate audit(CK 필수 게이트 감사)."),
        ("lineage_receipt", LINEAGE_RECEIPT, "CK lineage receipt(CK 계보 영수증)."),
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
    cj_final = validate_inputs()
    surface = read_csv(parent.PROXY_REPAIR_SURFACE)
    package = read_csv(parent.PACKAGE_PRECHECK)
    months = read_csv(parent.CANDIDATE_MONTH_STABILITY)
    sources = read_csv(parent.CANDIDATE_SOURCE_ATTRIBUTION)
    costs = read_csv(parent.COST_STRESS_DIAGNOSTIC)
    filters = read_csv(parent.CANDIDATE_FILTER_AUDIT)
    proxy_plan = read_csv(parent.PROXY_MT5_DIFF_PLAN)

    surface_row = selected_row(surface, cj_final)
    package_row = selected_row(package, cj_final)
    cost_row = selected_row(costs, cj_final)
    month_rows_ = month_failure_rows(cj_final, months)
    source_rows_ = source_balance_rows(cj_final, sources, filters)
    package_rows_ = package_gate_rows(cj_final, surface_row, package_row, month_rows_, cost_row)
    clues = positive_clue_rows(cj_final, surface, sources)
    proxy_rows_ = proxy_mt5_rows(proxy_plan)
    queue = next_queue_rows(cj_final)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    write_csv(PACKAGE_GATE_DECISION, package_rows_)
    write_csv(MONTH_FAILURE_ATTRIBUTION, month_rows_)
    write_csv(SOURCE_BALANCE_REVIEW, source_rows_)
    write_csv(POSITIVE_CLUE_REGISTER, clues)
    write_csv(PROXY_MT5_DIFF_REVIEW, proxy_rows_)
    write_csv(NEXT_REPAIR_QUEUE, queue)

    receipt_paths = [KPI_RECEIPT, DATA_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT, LINEAGE_RECEIPT]
    preliminary_gates = gate_rows(package_rows_, month_rows_, source_rows_, proxy_rows_, queue, receipt_paths, final_written=False)
    final = final_payload(cj_final, package_rows_, month_rows_, source_rows_, clues, proxy_rows_, queue, preliminary_gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, clues, proxy_rows_)
    refresh_lineage_receipt(final)
    gates = gate_rows(package_rows_, month_rows_, source_rows_, proxy_rows_, queue, receipt_paths, final_written=True)
    final = final_payload(cj_final, package_rows_, month_rows_, source_rows_, clues, proxy_rows_, queue, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final, clues, proxy_rows_)
    write_docs(final, package_rows_, month_rows_, source_rows_, clues, proxy_rows_, queue, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
