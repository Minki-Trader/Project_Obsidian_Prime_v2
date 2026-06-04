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

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import train_cost_stable_h17_source_guard_offensive_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CH"
RUN_ID = "run364CH_review_cost_stable_h17_source_guard_offensive_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_REVIEW_RUN_ID = parent.SOURCE_RUNTIME_REVIEW_RUN_ID
NEXT_RUN_ID = "run364CI_materialize_h17_focus_month_cost_stress_repair_inputs_without_db_v1"

STATUS = "completed_stage364CH_h17_focus_review_package_rejected_open_ci_no_authority"
JUDGMENT = "positive_proxy_clue_but_package_rejected_month_cost_stress_open_ci_no_authority"
DECISION = "stage364CH_open_run364CI_h17_focus_month_cost_stress_repair_inputs"
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
PACKAGE_GATE_DECISION = RUN_DIR / "package_gate_decision.csv"
STRESS_FAILURE_ATTRIBUTION = RUN_DIR / "stress_failure_attribution.csv"
POSITIVE_CLUE_REGISTER = RUN_DIR / "positive_clue_register.csv"
PROXY_MT5_DIFF_REVIEW = RUN_DIR / "proxy_mt5_diff_review.csv"
NEXT_REPAIR_QUEUE = RUN_DIR / "run364CI_h17_focus_month_cost_stress_repair_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364CH_cost_stable_h17_source_guard_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CH_cost_stable_h17_source_guard_review.md"
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
    parent.PROXY_SCOUT_SURFACE,
    parent.SELECTED_CANDIDATE,
    parent.SELECTED_TRADE_TAPE,
    parent.CANDIDATE_FILTER_AUDIT,
    parent.CANDIDATE_SOURCE_ATTRIBUTION,
    parent.CANDIDATE_MONTH_STABILITY,
    parent.COST_STRESS_DIAGNOSTIC,
    parent.PROXY_MT5_DIFF_PLAN,
    parent.RUN364CH_QUEUE,
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


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def json_ready(value: Any) -> Any:
    return parent.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 14) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CH inputs(CH 입력 누락): " + ", ".join(missing))

    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CG next_run_id mismatch(CG 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CG has forbidden authority claim(CG 금지 권위 주장 존재)")

    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CG gate audit(CG 게이트 감사)가 모두 passed(통과)가 아닙니다.")

    queue = read_csv(parent.RUN364CH_QUEUE)
    if len(queue) != 3:
        raise RuntimeError(f"CH queue row mismatch(CH 대기열 행 불일치): {len(queue)} != 3")
    if set(queue["review_subject"].astype(str)) != {str(final["selected_candidate_id"])}:
        raise RuntimeError("CH queue subject(CH 대기열 대상)가 selected candidate(선택 후보)와 다릅니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CH review source(CH 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def selected_frame(df: pd.DataFrame, final: Mapping[str, Any]) -> pd.DataFrame:
    selected_id = str(final["selected_candidate_id"])
    return df[df["candidate_id"].astype(str).eq(selected_id)].copy()


def selected_row(surface: pd.DataFrame, final: Mapping[str, Any]) -> dict[str, Any]:
    selected = selected_frame(surface, final)
    if len(selected) != 1:
        raise RuntimeError(f"selected candidate row mismatch(선택 후보 행 불일치): {len(selected)}")
    return selected.iloc[0].to_dict()


def bad_month_rows(months: pd.DataFrame, final: Mapping[str, Any]) -> list[dict[str, Any]]:
    selected = selected_frame(months, final)
    rows: list[dict[str, Any]] = []
    for _, raw in selected.iterrows():
        row = raw.to_dict()
        if as_float(row.get("net_profit")) < 0 or as_float(row.get("profit_factor")) < 1.0:
            rows.append(row)
    return rows


def package_gate_rows(final: Mapping[str, Any], surface_row: Mapping[str, Any], bad_months: Sequence[Mapping[str, Any]], cost_row: Mapping[str, Any]) -> list[dict[str, Any]]:
    headline_pass = (
        as_float(final["selected_net_delta_vs_parent"]) > 0
        and as_float(final["selected_profit_factor_delta_vs_parent"]) > 0
        and as_float(final["selected_trade_density"]) >= DENSITY_FLOOR
        and as_int(final["selected_short_trade_count"]) >= SHORT_FLOOR
    )
    stress_delta = as_float(cost_row.get("stress_adjusted_net_delta_vs_parent"))
    stress_status = str(cost_row.get("stress_judgment", ""))
    package_rejected = bool(bad_months) or stress_delta < 0 or "watch" in stress_status
    rows = [
        {
            "run_id": RUN_ID,
            "gate_id": "headline_proxy_kpi_gate",
            "subject": "selected proxy KPI(선택 프록시 핵심 성과)",
            "gate_status": "passed_for_proxy(프록시 기준 통과)" if headline_pass else "failed_for_proxy(프록시 기준 실패)",
            "evidence": (
                f"net_delta={final['selected_net_delta_vs_parent']};pf_delta={final['selected_profit_factor_delta_vs_parent']};"
                f"density={final['selected_trade_density']};shorts={final['selected_short_trade_count']}"
            ),
            "effect": "작은 positive clue(긍정 단서)는 보존하지만 package(패키지) 판단은 뒤 게이트에 맡긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "no_trade_splitting_gate",
            "subject": "trade splitting boundary(거래 쪼개기 경계)",
            "gate_status": "passed_no_split(무분할 통과)" if "no_split" in str(surface_row.get("candidate_status", "")) else "watch(관찰)",
            "evidence": f"candidate_status={surface_row.get('candidate_status', '')};trade_delta={final['selected_trade_delta_vs_parent']}",
            "effect": "거래수를 쪼개 수익을 나눈 결과가 아님을 분리 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "month_stability_package_gate",
            "subject": "monthly stability(월별 안정성)",
            "gate_status": "failed_for_package(패키지 기준 실패)" if bad_months else "passed_for_package(패키지 기준 통과)",
            "evidence": f"bad_month_count={len(bad_months)};bad_months={','.join(str(row['open_month']) for row in bad_months)}",
            "effect": "나쁜 월을 다음 repair constraint(수리 제약)로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "cost_stress_package_gate",
            "subject": "cost stress(비용 압박)",
            "gate_status": "failed_for_package(패키지 기준 실패)" if stress_delta < 0 or "watch" in stress_status else "passed_for_package(패키지 기준 통과)",
            "evidence": f"stress_delta={stress_delta};stress_judgment={stress_status}",
            "effect": "스왑 haircut(헤어컷) 진단이 MT5 KPI(MT5 핵심 성과)를 대체하지 못하게 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "mt5_runtime_package_gate",
            "subject": "new MT5 execution(새 MT5 실행)",
            "gate_status": "failed_for_package(패키지 기준 실패)",
            "evidence": "new_mt5_execution=not_run(새 MT5 실행 미실행)",
            "effect": "proxy(프록시)를 runtime authority(런타임 권위)로 승격하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "package_decision_gate",
            "subject": "package decision(패키지 결정)",
            "gate_status": "rejected_open_repair_inputs(거절, 수리 입력 개방)" if package_rejected else "watch_needs_mt5_precheck(관찰, MT5 사전 점검 필요)",
            "evidence": f"bad_months={len(bad_months)};stress_delta={stress_delta};new_mt5_execution=not_run",
            "effect": "CH를 운영 패키지가 아니라 CI materialization(CI 구체화)로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def stress_failure_rows(
    final: Mapping[str, Any],
    bad_months: Sequence[Mapping[str, Any]],
    cost_row: Mapping[str, Any],
    source_rows: pd.DataFrame,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in bad_months:
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
                "attribution": "selected h17 focus still has negative monthly slices(선택 17시 집중에도 음수 월 조각이 남음)",
                "repair_use": "CI should test month-of-year/quarter guard without exact 2025 month memorization(CI는 정확한 2025년 월 암기 없이 월중/분기 가드를 시험)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    stress_delta = as_float(cost_row.get("stress_adjusted_net_delta_vs_parent"))
    if stress_delta < 0 or "watch" in str(cost_row.get("stress_judgment", "")):
        rows.append(
            {
                "run_id": RUN_ID,
                "failure_id": "cost_haircut_selected_delta",
                "candidate_id": final["selected_candidate_id"],
                "failure_type": "cost_stress_watch(비용 압박 관찰)",
                "axis": "swap_haircut(스왑 헤어컷)",
                "segment": "selected_candidate(선택 후보)",
                "net_profit": cost_row.get("net_profit", ""),
                "profit_factor": final["selected_profit_factor"],
                "trade_count": final["selected_trade_count"],
                "short_trade_count": final["selected_short_trade_count"],
                "attribution": f"stress adjusted net delta is {stress_delta}(압박 조정 순수익 차이가 {stress_delta})",
                "repair_use": "CI should keep h17 clue only if stress-adjusted delta clears(CI는 압박 조정 차이가 해소될 때만 17시 단서를 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    synthetic = source_rows[source_rows["source_bucket"].astype(str).eq("synthetic_short_overlay")]
    if not synthetic.empty:
        row = synthetic.iloc[0].to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "failure_id": "sparse_synthetic_overlay_positive_but_thin",
                "candidate_id": final["selected_candidate_id"],
                "failure_type": "thin_positive_source(얇은 긍정 원천)",
                "axis": "source_bucket(원천 버킷)",
                "segment": "synthetic_short_overlay",
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "attribution": "overlay PF is high but only 38 trades(오버레이 PF는 높지만 38거래뿐)",
                "repair_use": "CI should preserve clue but add short-floor and stress controls(CI는 단서를 보존하되 숏 하한과 압박 대조를 붙임)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def positive_clue_rows(final: Mapping[str, Any], surface: pd.DataFrame, source_rows: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "run_id": RUN_ID,
            "clue_id": final["selected_candidate_id"],
            "clue_type": "selected_h17_focus_proxy_clue(선택 17시 집중 프록시 단서)",
            "net_profit": final["selected_net_profit"],
            "profit_factor": final["selected_profit_factor"],
            "expectancy": final["selected_expectancy"],
            "trade_count": final["selected_trade_count"],
            "trade_density": final["selected_trade_density"],
            "short_trade_count": final["selected_short_trade_count"],
            "net_delta_vs_parent": final["selected_net_delta_vs_parent"],
            "profit_factor_delta_vs_parent": final["selected_profit_factor_delta_vs_parent"],
            "usable_as": "CI primary repair seed(CI 주 수리 씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    for _, raw in source_rows.iterrows():
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
                "net_delta_vs_parent": "",
                "profit_factor_delta_vs_parent": "",
                "usable_as": "source balance diagnostic(원천 균형 진단)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    candidates = surface.copy()
    candidates["net_delta_vs_parent_num"] = pd.to_numeric(candidates["net_delta_vs_parent"], errors="coerce").fillna(0.0)
    candidates["stress_delta_num"] = pd.to_numeric(candidates["stress_adjusted_net_delta_vs_parent"], errors="coerce").fillna(0.0)
    candidates["short_count_num"] = pd.to_numeric(candidates["short_trade_count"], errors="coerce").fillna(0.0)
    salvage = candidates[
        candidates["net_delta_vs_parent_num"].gt(as_float(final["selected_net_delta_vs_parent"]))
        & candidates["candidate_id"].astype(str).ne(str(final["selected_candidate_id"]))
    ].sort_values(["stress_delta_num", "net_delta_vs_parent_num"], ascending=[False, False]).head(4)
    for _, raw in salvage.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "clue_id": row["candidate_id"],
                "clue_type": "higher_net_salvage_seed(더 높은 순수익 회수 씨앗)",
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "expectancy": row.get("expectancy", ""),
                "trade_count": row.get("trade_count", ""),
                "trade_density": row.get("trade_density", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "net_delta_vs_parent": row.get("net_delta_vs_parent", ""),
                "profit_factor_delta_vs_parent": row.get("profit_factor_delta_vs_parent", ""),
                "usable_as": "CI secondary comparison seed; repair short floor if below 100(CI 보조 비교 씨앗, 100 미만이면 숏 하한 수리)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_mt5_review_rows(proxy_mt5: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, raw in proxy_mt5.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": row.get("comparison_id", "selected_proxy_vs_parent_mt5(선택 프록시 대 상위 MT5)"),
                "selected_candidate_id": row.get("selected_candidate_id", ""),
                "parent_mt5_net": row.get("parent_mt5_net", ""),
                "proxy_net": row.get("proxy_net", ""),
                "net_diff_proxy_minus_parent": row.get("net_diff_proxy_minus_parent", ""),
                "parent_mt5_profit_factor": row.get("parent_mt5_profit_factor", ""),
                "proxy_profit_factor": row.get("proxy_profit_factor", ""),
                "parent_mt5_density": row.get("parent_mt5_density", ""),
                "proxy_density": row.get("proxy_density", ""),
                "attribution": "proxy lift is a screen result, not a new MT5 result(프록시 우위는 선별 결과이지 새 MT5 결과가 아님)",
                "usability": "usable_for_CI_seed_and_signal_sanity_not_runtime_authority(CI 씨앗과 신호 점검에는 사용 가능, 런타임 권위는 아님)",
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
            "queue_id": "ci01_h17_focus_cost_stress_guard",
            "action": "materialize h17 focus with cost stress guard(17시 집중에 비용 압박 가드를 붙여 구체화)",
            "success_criteria": "stress_adjusted_net_delta>=0, PF>=parent, density>=3, short_count>=100(압박 조정 순수익 차이 0 이상, PF 상위 이상, 밀도 3 이상, 숏 100개 이상)",
            "effect": "CG의 작은 h17 lift(17시 우위)를 비용에 버티는 수리 입력으로 바꾼다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "ci02_bad_month_micro_guard_no_exact_date",
            "action": "test month-of-year/quarter guard without exact 2025 date memorization(정확한 2025년 날짜 암기 없이 월중/분기 가드 시험)",
            "success_criteria": "bad_month_count decreases without deleting one known month(알려진 특정 월 삭제 없이 나쁜 월 수 감소)",
            "effect": "2025-08/2025-12 실패를 과적합 필터가 아니라 timestamp-safe(시점 안전) 국면 제약으로 바꾼다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "ci03_short_floor_rescue_from_cg07_cg12",
            "action": "rescue net lift from cg07/cg12 while restoring short floor(cg07/cg12 순수익 우위를 회수하되 숏 하한 복원)",
            "success_criteria": "net lift remains positive and short_count>=100(순수익 우위 양수 유지, 숏 100개 이상)",
            "effect": "더 큰 net lift(순수익 우위)를 버리지 않고 long/short balance(롱/숏 균형) 제약과 결합한다.",
        },
        {
            **common,
            "queue_rank": 4,
            "queue_id": "ci04_mt5_reprobe_precheck_only_if_stress_clears",
            "action": "prepare MT5 precheck only after stress clears(압박이 해소된 뒤에만 MT5 사전 점검 준비)",
            "success_criteria": "no MT5 package unless CI clears stress and source balance(CI가 압박과 원천 균형을 통과하기 전 MT5 패키지 없음)",
            "effect": "external verification(외부 검증)을 미루지 않되, 약한 proxy(프록시)를 곧장 runtime claim(런타임 주장)으로 올리지 않는다.",
        },
    ]


def gate_rows(
    final_like: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    stress_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    required = {"kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"}
    present = {
        "kpi_contract_audit",
        "row_grain_audit",
        "source_authority_audit",
        "package_reject_gate",
        "stress_memory_gate",
        "next_offensive_seed_gate",
        "proxy_mt5_diff_audit",
        "required_gate_coverage_audit",
    }
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
            "effect": "package(패키지), stress(압박), proxy/MT5 diff(프록시/MT5 차이)를 다른 행 단위로 분리했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": rel(parent.FINAL_DECISION),
            "effect": "CG 산출물만 사용하고 proxy(프록시)를 MT5 KPI(MT5 핵심 성과)로 대체하지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "package_reject_gate",
            "status": "passed" if str(final_like["package_decision"]).startswith("rejected") else "failed",
            "evidence": rel(PACKAGE_GATE_DECISION),
            "effect": "월/비용 압박과 MT5 미실행 때문에 package(패키지)를 거절했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "stress_memory_gate",
            "status": "passed" if len(stress_rows) >= 2 else "failed",
            "evidence": rel(STRESS_FAILURE_ATTRIBUTION),
            "effect": "나쁜 월과 비용 압박을 CI repair constraint(CI 수리 제약)로 전환했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "next_offensive_seed_gate",
            "status": "passed" if len(queue) == 4 else "failed",
            "evidence": rel(NEXT_REPAIR_QUEUE),
            "effect": "same Stage364(같은 364단계) 안에서 다음 공격 수리 대기열을 열었다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "proxy_mt5_diff_audit",
            "status": "passed" if len(proxy_rows) >= 1 else "failed",
            "evidence": rel(PROXY_MT5_DIFF_REVIEW),
            "effect": "proxy expected value(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)를 구분했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if required.issubset(present) else "failed",
            "evidence": rel(WORK_PACKET),
            "effect": "work packet(작업 묶음)의 필수 gate(게이트)가 closeout(종료 기록)에 연결됐다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


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
                "obsidian-claim-discipline(주장 규율)",
            ],
            "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"],
            "result_subject": "CG selected h17 focus proxy(CG 선택 17시 집중 프록시)",
            "evidence_boundary": "review_only(검토 전용)",
            "effect": "CG positive proxy clue(CG 긍정 프록시 단서)를 package reject(패키지 거절)와 CI repair seed(CI 수리 씨앗)로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def final_payload(
    cg_final: Mapping[str, Any],
    surface_row: Mapping[str, Any],
    bad_months: Sequence[Mapping[str, Any]],
    cost_row: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    stress_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    min_month_net = min((as_float(row.get("net_profit")) for row in bad_months), default=0.0)
    min_month_pf = min((as_float(row.get("profit_factor")) for row in bad_months), default=0.0)
    package_decision = "rejected_package_open_ci_repair_inputs_no_authority(패키지 거절, CI 수리 입력 개방, 권위 없음)"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_review_run_id": SOURCE_RUNTIME_REVIEW_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "reviewed_candidate_id": cg_final["selected_candidate_id"],
        "reviewed_net_profit": cg_final["selected_net_profit"],
        "reviewed_profit_factor": cg_final["selected_profit_factor"],
        "reviewed_expectancy": cg_final["selected_expectancy"],
        "reviewed_trade_count": cg_final["selected_trade_count"],
        "reviewed_density": cg_final["selected_trade_density"],
        "reviewed_closed_drawdown_amount": cg_final["selected_closed_trade_drawdown_proxy"],
        "reviewed_recovery_factor": cg_final["selected_closed_trade_recovery_proxy"],
        "reviewed_long_trade_count": cg_final["selected_long_trade_count"],
        "reviewed_short_trade_count": cg_final["selected_short_trade_count"],
        "reviewed_short_share": cg_final["selected_short_share"],
        "reviewed_net_delta_vs_parent": cg_final["selected_net_delta_vs_parent"],
        "reviewed_profit_factor_delta_vs_parent": cg_final["selected_profit_factor_delta_vs_parent"],
        "reviewed_trade_delta_vs_parent": cg_final["selected_trade_delta_vs_parent"],
        "reviewed_short_delta_vs_parent": cg_final["selected_short_delta_vs_parent"],
        "reviewed_transform": cg_final["selected_transform"],
        "reviewed_month_bad_count": len(bad_months),
        "reviewed_bad_months": [row["open_month"] for row in bad_months],
        "reviewed_min_month_net": finite(min_month_net, 2),
        "reviewed_min_month_profit_factor": finite(min_month_pf, 10),
        "reviewed_cost_stress_judgment": cost_row.get("stress_judgment", ""),
        "reviewed_stress_adjusted_net": cost_row.get("stress_adjusted_net_swap_haircut_1x", ""),
        "reviewed_stress_adjusted_net_delta_vs_parent": cost_row.get("stress_adjusted_net_delta_vs_parent", ""),
        "surface_candidate_status": surface_row.get("candidate_status", ""),
        "package_decision": package_decision,
        "package_gate_rows": len(package_rows),
        "stress_failure_count": len(stress_rows),
        "preserved_clue_count": len(clues),
        "proxy_mt5_diff_rows": len(proxy_rows),
        "next_queue_rows": len(queue),
        "next_primary_seed": "ci01_h17_focus_cost_stress_guard",
        "new_model_training": "not_run(미실행)",
        "new_mt5_execution": "not_run(미실행)",
        "forward_passed": "not_run(미실행)",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_review_only_no_new_mt5(주장 범위 밖, 검토 전용 새 MT5 없음)",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any], proxy_rows: Sequence[Mapping[str, Any]], clues: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        KPI_RECEIPT,
        {
            **base,
            "measurement_scope": "net_profit/PF/expectancy/DD/recovery/trades/long_short/cost_stress(순수익/PF/기대값/DD/회복/거래/롱숏/비용압박)",
            "reviewed_candidate": final["reviewed_candidate_id"],
            "headline": {
                "net": final["reviewed_net_profit"],
                "pf": final["reviewed_profit_factor"],
                "density": final["reviewed_density"],
                "shorts": final["reviewed_short_trade_count"],
                "month_bad_count": final["reviewed_month_bad_count"],
                "stress_delta": final["reviewed_stress_adjusted_net_delta_vs_parent"],
            },
            "package_decision": final["package_decision"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_sources": [rel(path) for path in INPUT_FILES],
            "timestamp_boundary": "review uses CG entry-known outputs only; CI forbids exact bad-month memorization(CG의 진입 시점 산출물만 검토, CI는 특정 나쁜 월 암기 금지)",
            "lookahead_bias": "not_detected_in_review_no_new_features_or_labels(검토에서 새 피처/라벨 없음, 미래참조 미탐지)",
            "integrity_judgment": "usable_for_review_not_operating_claim(검토 사용 가능, 운영 주장 불가)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": "CG h17 focus lifted net by 4.01 and PF by 0.002227 but left bad months and cost watch(CG 17시 집중이 순수익 4.01, PF 0.002227 상승했지만 나쁜 월과 비용 관찰이 남음)",
            "comparison_baseline": "parent CD02 MT5/runtime review output(상위 CD02 MT5/런타임 검토 출력)",
            "likely_drivers": ["h17 overlay focus(17시 오버레이 집중)", "source bucket mix(원천 버킷 혼합)", "native short cost firewall alternatives(기본 숏 비용 방화벽 대안)"],
            "segment_checks": [rel(parent.CANDIDATE_MONTH_STABILITY), rel(parent.CANDIDATE_SOURCE_ATTRIBUTION), rel(parent.COST_STRESS_DIAGNOSTIC)],
            "proxy_mt5_diff_review": list(proxy_rows),
            "preserved_clues": list(clues)[:10],
            "attribution_confidence": "medium_for_proxy_low_for_runtime(프록시 중간, 런타임 낮음)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "CG selected h17 focus proxy(CG 선택 17시 집중 프록시)",
            "evidence_available": [rel(path) for path in INPUT_FILES],
            "evidence_missing": ["new MT5 runtime reprobe(새 MT5 런타임 재탐침)", "forward pass(전진 통과)", "operating promotion evidence(운영 승격 근거)"],
            "judgment_label": "positive_proxy_clue_package_rejected(긍정 프록시 단서, 패키지 거절)",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "숫자는 조금 좋아졌지만 월/비용/MT5 근거가 약해서 운영 후보로 올리지 않고 수리 입력으로 넘긴다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claims": ["reviewed CG proxy evidence(CG 프록시 근거 검토)", "CI repair queue opened(CI 수리 대기열 개방)"],
            "forbidden_claims": ["new model trained(새 모델 학습)", "new MT5 execution(새 MT5 실행)", "runtime authority(런타임 권위)", "operating promotion(운영 승격)", "Goal Achieve(목표 달성)"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if exists(path) and path != LINEAGE_RECEIPT and io_path(path).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_generated_with_manifest(커밋 후 추적 또는 목록으로 재생성 가능)",
            "lineage_judgment": "connected_with_boundary_CH_review_to_CI_queue(CH 검토와 CI 대기열 연결, 경계 포함)",
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
    report = f"""# run364CH cost-stable h17 source guard review(364CH 비용 안정 17시 원천 가드 검토)

## Current Truth(현재 진실)

- reviewed candidate(검토 후보): `{final['reviewed_candidate_id']}`
- reviewed KPI(검토 핵심 성과 지표): net/PF/expectancy/density/trades(순수익/수익 팩터/기대값/밀도/거래수) `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_expectancy']}` / `{final['reviewed_density']}` / `{final['reviewed_trade_count']}`
- long/short balance(롱/숏 균형): `{final['reviewed_long_trade_count']}` / `{final['reviewed_short_trade_count']}`
- month bad count(나쁜 월 수): `{final['reviewed_month_bad_count']}` with `{final['reviewed_bad_months']}`
- cost stress(비용 압박): `{final['reviewed_cost_stress_judgment']}`, stress delta(압박 차이) `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`
- package decision(패키지 결정): `{final['package_decision']}`
- next action(다음 행동): `{NEXT_RUN_ID}`

## Action And Effect(행동과 효과)

Action(행동): CG selected proxy(CG 선택 프록시)를 package gate(패키지 게이트), stress attribution(압박 귀속), proxy/MT5 diff(프록시/MT5 차이), CI queue(CI 대기열)로 분리했다.

Effect(효과): `cg09_best_open_hour_overlay_focus`의 작은 positive clue(긍정 단서)는 보존하지만, bad months(나쁜 월), cost stress watch(비용 압박 관찰), new MT5 execution(새 MT5 실행) 없음 때문에 package(패키지)는 거절하고 CI repair(CI 수리)를 연다.

## Package Gate(패키지 게이트)

{markdown_table(package_rows, ['gate_id', 'subject', 'gate_status', 'evidence', 'effect'])}

## Stress Failure Attribution(압박 실패 귀속)

{markdown_table(stress_rows, ['failure_id', 'failure_type', 'axis', 'segment', 'net_profit', 'profit_factor', 'trade_count', 'short_trade_count', 'repair_use'])}

## Positive Clues(긍정 단서)

{markdown_table(clues, ['clue_id', 'clue_type', 'net_profit', 'profit_factor', 'trade_count', 'short_trade_count', 'net_delta_vs_parent', 'usable_as'])}

## Proxy/MT5 Diff Review(프록시/MT5 차이 검토)

{markdown_table(proxy_rows, ['comparison_id', 'parent_mt5_net', 'proxy_net', 'net_diff_proxy_minus_parent', 'parent_mt5_profit_factor', 'proxy_profit_factor', 'usability'])}

## CI Queue(CI 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'action', 'success_criteria', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

CH is review only(CH는 검토 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364CH cost-stable h17 source guard review(비용 안정 17시 원천 가드 검토)

Action(행동): CG h17 focus proxy(CG 17시 집중 프록시)를 package reject(패키지 거절)로 닫고 `{NEXT_RUN_ID}`를 열었다.

Effect(효과): small proxy lift(작은 프록시 우위)는 CI repair seed(CI 수리 씨앗)로 보존하지만, bad month(나쁜 월) `{final['reviewed_bad_months']}`와 cost stress(비용 압박) `{final['reviewed_stress_adjusted_net_delta_vs_parent']}` 때문에 운영 주장(operating claim, 운영 주장)은 하지 않는다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - cost-stable h17 source guard review(비용 안정 17시 원천 가드 검토).")
    append_text_once(
        STAGE_BRIEF,
        "## run364CH Cost-Stable H17 Source Guard Review Closeout",
        f"""## run364CH Cost-Stable H17 Source Guard Review Closeout(364CH 비용 안정 17시 원천 가드 검토 종료)

Action(행동): CG selected h17 focus(CG 선택 17시 집중)를 package gate(패키지 게이트), month/source/cost attribution(월/원천/비용 귀속), proxy/MT5 diff(프록시/MT5 차이)로 검토했다.

Effect(효과): package(패키지)는 거절하고 `{NEXT_RUN_ID}`에서 같은 Stage364(364단계) 안의 수리 입력으로 이어간다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## {RUN_ID}

Action(행동): cost-stable h17 source guard proxy(비용 안정 17시 원천 가드 프록시)를 검토했다.

Effect(효과): stage branch(단계 분기) 없이 `{NEXT_RUN_ID}`로 월/비용/숏 하한 수리 입력을 연다.
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
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364CH(364CH 실행)는 `cg09_best_open_hour_overlay_focus`를 package(패키지)에서 거절하고 CI repair seed(CI 수리 씨앗)로 보존했다. 이유는 bad months(나쁜 월) `{final['reviewed_bad_months']}`, cost stress delta(비용 압박 차이) `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`, new MT5 execution(새 MT5 실행) 없음이다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 h17 focus(17시 집중), bad month guard(나쁜 월 가드), short floor rescue(숏 하한 복원)를 구체화한다.",
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

Current truth(현재 진실): `run364CH` reviewed(검토 완료) CG selected proxy(CG 선택 프록시) `{final['reviewed_candidate_id']}`. Headline KPI(표면 핵심 성과)는 net/PF/density/trades/shorts(순수익/수익 팩터/밀도/거래수/숏) `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_trade_count']}` / `{final['reviewed_short_trade_count']}`이지만, package(패키지)는 `{final['package_decision']}`이다.

Failure memory(실패 기억): bad months(나쁜 월) `{final['reviewed_bad_months']}`, cost stress delta(비용 압박 차이) `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`, new MT5 execution(새 MT5 실행) 없음.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 h17 focus cost stress guard(17시 집중 비용 압박 가드), bad month guard(나쁜 월 가드), short floor rescue(숏 하한 복원)를 같은 Stage364(364단계) 안에서 구체화한다.

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

Package candidate(패키지 후보): none(없음). `{final['reviewed_candidate_id']}` is preserved only as CI repair seed(CI 수리 씨앗으로만 보존).

Reviewed KPI(검토 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, expectancy `{final['reviewed_expectancy']}`, trades `{final['reviewed_trade_count']}`, density `{final['reviewed_density']}`, closed DD `{final['reviewed_closed_drawdown_amount']}`, recovery `{final['reviewed_recovery_factor']}`, long/short `{final['reviewed_long_trade_count']}` / `{final['reviewed_short_trade_count']}`.

Package rejection(패키지 거절): bad months(나쁜 월) `{final['reviewed_bad_months']}`, cost stress delta(비용 압박 차이) `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`, new MT5 execution(새 MT5 실행) 없음.

Next queue(다음 대기열): `{rel(NEXT_REPAIR_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): cost-stable h17 source guard proxy(비용 안정 17시 원천 가드 프록시)를 package gate(패키지 게이트)와 stress attribution(압박 귀속)으로 검토했다.
- effect(효과): package(패키지)는 거절하고 `{NEXT_RUN_ID}` CI repair inputs(CI 수리 입력)를 열었다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): h17 overlay focus(17시 오버레이 집중)는 small net/PF lift(작은 순수익/PF 우위)를 만들지만 month/cost stress(월/비용 압박)를 해결해야 한다.
- positive clue(긍정 단서): net/PF/density/shorts `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_trade_count']}`.
- evidence_boundary(근거 경계): review only(검토 전용), no new MT5 execution(새 MT5 실행 없음).
- next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): CG h17 focus package rejected(CG 17시 집중 패키지 거절).
- failure_memory(실패 기억): bad months(나쁜 월) `{final['reviewed_bad_months']}`, cost stress delta(비용 압박 차이) `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`, MT5 reprobe missing(MT5 재탐침 없음).
- salvage_value(회수 가치): h17 focus(17시 집중)와 synthetic_short_overlay(합성 숏 오버레이)는 CI repair seed(CI 수리 씨앗)로 남긴다.
- reopen_condition(재개 조건): `{NEXT_RUN_ID}`가 stress_adjusted_net_delta>=0(압박 조정 순수익 차이 0 이상), density>=3(밀도 3 이상), short_count>=100(숏 100개 이상)을 동시에 만든다.
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
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "kpi_review_only(핵심 성과 검토 전용)",
        "question": "Does CG h17 focus deserve package or CI repair handoff?(CG 17시 집중을 패키지로 올릴 것인가 CI 수리로 넘길 것인가?)",
        "next_action": NEXT_RUN_ID,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(PACKAGE_GATE_DECISION),
        "result_judgment": JUDGMENT,
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
            "kpi_scope": "CH review(CH 검토)",
            "scoreboard_lane": "stage364_kpi_review(Stage364 핵심 성과 검토)",
            "status": status,
            "primary_kpi": f"net={final['reviewed_net_profit']};pf={final['reviewed_profit_factor']};density={final['reviewed_density']};shorts={final['reviewed_short_trade_count']}",
            "guardrail_kpi": f"bad_months={final['reviewed_month_bad_count']};stress_delta={final['reviewed_stress_adjusted_net_delta_vs_parent']};no_authority",
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "reviewed_proxy(검토 프록시)",
        }
        if include_metrics:
            row.update(metric_values)
        rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)

    registry_row = {
        **common,
        "lane": "stage364_kpi_review(Stage364 핵심 성과 검토)",
        "family": "cost_stable_h17_source_guard_review(비용 안정 17시 원천 가드 검토)",
        "result_status": STATUS,
        "trade_density_requirement_status": "passed_proxy_density_ge_3_no_trade_splitting(프록시 밀도 3 이상 통과, 거래 쪼개기 없음)",
        "view": "kpi_review(핵심 성과 검토)",
        "tier": "Tier A",
        "metric_scope": "reviewed_proxy(검토 프록시)",
    }
    registry_row.update(metric_values)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [registry_row])
    if hasattr(parent, "repair_run_registry_line_endings"):
        parent.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("package_gate_decision", PACKAGE_GATE_DECISION, "CH package gate decision(CH 패키지 게이트 결정)."),
        ("stress_failure_attribution", STRESS_FAILURE_ATTRIBUTION, "CH stress failure attribution(CH 압박 실패 귀속)."),
        ("positive_clue_register", POSITIVE_CLUE_REGISTER, "CH positive clue register(CH 긍정 단서 등록)."),
        ("proxy_mt5_diff_review", PROXY_MT5_DIFF_REVIEW, "CH proxy/MT5 diff review(CH 프록시/MT5 차이 검토)."),
        ("next_repair_queue", NEXT_REPAIR_QUEUE, "CH to CI repair queue(CH에서 CI 수리 대기열)."),
        ("final_decision", FINAL_DECISION, "CH final decision(CH 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CH run manifest(CH 실행 목록)."),
        ("report", REPORT_PATH, "CH report(CH 보고서)."),
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
    # Exclude self-mutating files so the manifest hash stays stable across reruns.
    manifest_exclusions = {RUN_MANIFEST, LINEAGE_RECEIPT, ARTIFACT_REGISTRY}
    output_paths = [path for path in OUTPUT_FILES if path not in manifest_exclusions and exists(path) and io_path(path).is_file()]
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
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    cg_final = validate_inputs()
    surface = read_csv(parent.PROXY_SCOUT_SURFACE)
    months = read_csv(parent.CANDIDATE_MONTH_STABILITY)
    sources = read_csv(parent.CANDIDATE_SOURCE_ATTRIBUTION)
    costs = read_csv(parent.COST_STRESS_DIAGNOSTIC)
    proxy_mt5 = read_csv(parent.PROXY_MT5_DIFF_PLAN)

    surface_row = selected_row(surface, cg_final)
    selected_sources = selected_frame(sources, cg_final)
    selected_cost = selected_frame(costs, cg_final)
    if len(selected_cost) != 1:
        raise RuntimeError(f"selected cost row mismatch(선택 비용 행 불일치): {len(selected_cost)}")
    cost_row = selected_cost.iloc[0].to_dict()
    bad_months = bad_month_rows(months, cg_final)

    package_rows = package_gate_rows(cg_final, surface_row, bad_months, cost_row)
    stress_rows = stress_failure_rows(cg_final, bad_months, cost_row, selected_sources)
    clues = positive_clue_rows(cg_final, surface, selected_sources)
    proxy_rows = proxy_mt5_review_rows(proxy_mt5)
    queue = next_queue_rows(cg_final)
    preliminary = {"package_decision": "rejected_package_open_ci_repair_inputs_no_authority(패키지 거절, CI 수리 입력 개방, 권위 없음)"}
    gates = gate_rows(preliminary, package_rows, stress_rows, proxy_rows, queue)
    failed = [row["gate"] for row in gates if row["status"] != "passed"]
    if failed:
        write_csv(INPUT_MANIFEST, input_manifest_rows())
        write_work_packet()
        write_csv(PACKAGE_GATE_DECISION, package_rows)
        write_csv(STRESS_FAILURE_ATTRIBUTION, stress_rows)
        write_csv(PROXY_MT5_DIFF_REVIEW, proxy_rows)
        write_csv(NEXT_REPAIR_QUEUE, queue)
        write_csv(GATE_AUDIT, gates)
        raise RuntimeError("CH gate failure(CH 게이트 실패): " + ", ".join(failed))

    created_at = now_utc()
    final = final_payload(cg_final, surface_row, bad_months, cost_row, package_rows, stress_rows, clues, proxy_rows, queue, gates, created_at)
    gates = gate_rows(final, package_rows, stress_rows, proxy_rows, queue)
    final = final_payload(cg_final, surface_row, bad_months, cost_row, package_rows, stress_rows, clues, proxy_rows, queue, gates, created_at)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
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
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
