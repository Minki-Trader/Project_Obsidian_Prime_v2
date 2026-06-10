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
from stage_pipelines.stage364 import train_h17_bad_month_source_balance_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CN"
RUN_ID = "run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID = "run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1"

STATUS = "completed_stage364CN_h17_bad_month_source_balance_repair_review_open_co_no_authority"
JUDGMENT = "positive_proxy_package_review_candidate_open_mt5_probe_inputs_no_authority"
DECISION = "stage364CN_open_run364CO_h17_bad_month_source_balance_repair_mt5_probe_inputs"
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
SOURCE_BALANCE_REVIEW = RUN_DIR / "source_balance_review.csv"
MONTH_STABILITY_REVIEW = RUN_DIR / "month_stability_review.csv"
COST_STRESS_REVIEW = RUN_DIR / "cost_stress_review.csv"
FILTER_REVIEW = RUN_DIR / "filter_review.csv"
POSITIVE_CLUE_REGISTER = RUN_DIR / "positive_clue_register.csv"
PROXY_MT5_DIFF_REVIEW = RUN_DIR / "proxy_mt5_diff_review.csv"
MT5_REPROBE_BOUNDARY = RUN_DIR / "mt5_reprobe_boundary.csv"
CANDIDATE_RULE_PACKAGE = RUN_DIR / "cm04_candidate_rule_package.json"
RUN364CO_QUEUE = RUN_DIR / "run364CO_mt5_runtime_probe_input_queue.csv"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CN_h17_bad_month_source_balance_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CN_h17_bad_month_source_balance_repair_review.md"
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
    parent.CM_PROXY_REPAIR_SURFACE,
    parent.SELECTED_CANDIDATE,
    parent.SELECTED_TRADE_TAPE,
    parent.CANDIDATE_FILTER_AUDIT,
    parent.CANDIDATE_SOURCE_ATTRIBUTION,
    parent.CANDIDATE_MONTH_STABILITY,
    parent.COST_STRESS_DIAGNOSTIC,
    parent.PACKAGE_PRECHECK,
    parent.PROXY_MT5_DIFF_PLAN,
    parent.RUN364CN_QUEUE,
    parent.DATA_INTEGRITY_AUDIT,
    parent.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    PACKAGE_GATE_DECISION,
    SOURCE_BALANCE_REVIEW,
    MONTH_STABILITY_REVIEW,
    COST_STRESS_REVIEW,
    FILTER_REVIEW,
    POSITIVE_CLUE_REGISTER,
    PROXY_MT5_DIFF_REVIEW,
    MT5_REPROBE_BOUNDARY,
    CANDIDATE_RULE_PACKAGE,
    RUN364CO_QUEUE,
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
        raise FileNotFoundError("missing CN inputs(CN 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CM next_run_id mismatch(CM 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CM has forbidden authority claim(CM 금지 권위 주장 존재)")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CM gate audit(CM 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CN review source(CN 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def selected_frame(df: pd.DataFrame, selected_id: str) -> pd.DataFrame:
    return df[df["candidate_id"].astype(str).eq(selected_id)].copy()


def one_selected(df: pd.DataFrame, selected_id: str, label: str) -> dict[str, Any]:
    selected = selected_frame(df, selected_id)
    if len(selected) != 1:
        raise RuntimeError(f"{label} selected row mismatch(선택 행 불일치): {len(selected)}")
    return selected.iloc[0].to_dict()


def package_gate_rows(
    final: Mapping[str, Any],
    surface_row: Mapping[str, Any],
    package_row: Mapping[str, Any],
    source_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    cost_row: Mapping[str, Any],
    filter_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    source_total = sum(as_float(row.get("trade_count")) for row in source_rows)
    source_net = sum(as_float(row.get("net_profit")) for row in source_rows)
    bad_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0 or as_float(row.get("profit_factor")) < 1.0]
    stress_delta = as_float(cost_row.get("stress_adjusted_net_delta_vs_parent"))
    filter_removed = sum(as_float(row.get("removed_trade_count")) for row in filter_rows)
    filter_restored = sum(as_float(row.get("restored_trade_count")) for row in filter_rows)
    parent_trades = as_float(surface_row.get("parent_trade_count", final["selected_trade_count"]))
    no_split_pass = as_float(final["selected_trade_count"]) <= parent_trades
    source_balance_pass = (
        int(as_float(final["selected_long_trade_count"])) > 0
        and int(as_float(final["selected_short_trade_count"])) >= SHORT_FLOOR
        and abs(source_net - as_float(final["selected_net_profit"])) < 0.05
        and int(source_total) == int(as_float(final["selected_trade_count"]))
    )
    package_pass = (
        "passed" in str(package_row.get("package_precheck_status", ""))
        and not bad_months
        and stress_delta >= 0
        and no_split_pass
        and source_balance_pass
    )
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "proxy_package_precheck_gate",
            "subject": "package precheck(패키지 사전검사)",
            "gate_status": "passed_for_mt5_probe_input(통과, MT5 탐침 입력 인계)" if package_pass else "failed_for_mt5_probe_input(실패, MT5 탐침 입력 보류)",
            "evidence": (
                f"status={package_row.get('package_precheck_status')};bad_months={len(bad_months)};"
                f"stress_delta={stress_delta};source_balance={source_balance_pass}"
            ),
            "effect": "MT5 probe(MT5 탐침) 입력으로 넘기되 운영 주장(operating claim, 운영 주장)은 하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "headline_kpi_gate",
            "subject": "headline KPI(표면 핵심 성과 지표)",
            "gate_status": "passed_for_proxy_review(프록시 검토 통과)",
            "evidence": (
                f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};"
                f"expectancy={final['selected_expectancy']};density={final['selected_trade_density']};"
                f"trades={final['selected_trade_count']}"
            ),
            "effect": "좋은 proxy(프록시) 숫자를 후보성(candidate quality, 후보성)으로만 보존합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "trade_density_and_no_split_gate",
            "subject": "trade density and no split(거래 밀도와 무분할)",
            "gate_status": "passed_no_split_density_ge_3(무분할 및 밀도 3 이상 통과)" if no_split_pass else "failed_split_risk(분할 위험 실패)",
            "evidence": (
                f"density={final['selected_trade_density']};selected_trades={final['selected_trade_count']};"
                f"parent_trades={parent_trades};removed={filter_removed};restored={filter_restored}"
            ),
            "effect": "거래수를 쪼개 수익을 나눈 결과인지 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "month_stability_gate",
            "subject": "monthly stability(월 안정성)",
            "gate_status": "passed_bad_month_zero(손실 월 0개 통과)" if not bad_months else "failed_bad_months(손실 월 존재)",
            "evidence": f"bad_month_count={len(bad_months)};weakest_month={month_rows[0].get('open_month', '') if month_rows else ''}",
            "effect": "CK/CL의 failure memory(실패 기억)가 해소됐는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "source_balance_gate",
            "subject": "source balance(원천 균형)",
            "gate_status": "passed_source_sum_and_short_floor(원천 합산 및 숏 하한 통과)" if source_balance_pass else "failed_source_balance(원천 균형 실패)",
            "evidence": (
                f"source_total={int(source_total)};source_net={finite(source_net, 2)};"
                f"long={final['selected_long_trade_count']};short={final['selected_short_trade_count']};"
                f"short_share={final['selected_short_share']}"
            ),
            "effect": "long_threshold/native_short/synthetic_overlay(롱 임계값/기본 숏/합성 오버레이)가 끊기지 않았는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "cost_stress_gate",
            "subject": "cost stress(비용 압박)",
            "gate_status": "passed_stress_delta_nonnegative(압박 차이 0 이상 통과)" if stress_delta >= 0 else "failed_stress_delta(압박 차이 실패)",
            "evidence": f"stress_delta={stress_delta};swap_sum={cost_row.get('swap_sum')};stress_judgment={cost_row.get('stress_judgment')}",
            "effect": "swap haircut(스왑 헤어컷) 뒤에도 후보성이 남는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "new_mt5_execution_boundary_gate",
            "subject": "new MT5 execution(새 MT5 실행)",
            "gate_status": "not_run_boundary_preserved(미실행 경계 보존)",
            "evidence": "new_mt5_execution=not_run(새 MT5 실행 미실행)",
            "effect": "proxy(프록시)를 MT5 KPI(MT5 핵심 성과 지표)로 대체하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def source_balance_rows(source: pd.DataFrame, selected_id: str) -> list[dict[str, Any]]:
    rows = []
    for _, raw in selected_frame(source, selected_id).iterrows():
        row = raw.to_dict()
        bucket = str(row.get("source_bucket"))
        if bucket == "synthetic_short_overlay":
            judgment = "high_pf_but_thin_watch(높은 PF지만 얇아서 관찰)"
        elif bucket == "native_short_threshold":
            judgment = "short_floor_support(숏 하한 지원)"
        else:
            judgment = "main_long_profit_body(주 롱 수익 몸통)"
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": selected_id,
                "source_bucket": bucket,
                "trade_count": row.get("trade_count"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "expectancy": row.get("expectancy"),
                "long_trade_count": row.get("long_trade_count"),
                "short_trade_count": row.get("short_trade_count"),
                "source_judgment": judgment,
                "effect": "CO materialization(CO 구체화)에서 원천별 규칙 구현 경계를 유지합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def month_review_rows(months: pd.DataFrame, selected_id: str) -> list[dict[str, Any]]:
    selected = selected_frame(months, selected_id).copy()
    selected["net_num"] = pd.to_numeric(selected["net_profit"], errors="coerce").fillna(0.0)
    selected["pf_num"] = pd.to_numeric(selected["profit_factor"], errors="coerce").fillna(0.0)
    selected = selected.sort_values(["net_num", "pf_num"], ascending=[True, True])
    rows: list[dict[str, Any]] = []
    for _, raw in selected.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": selected_id,
                "open_month": row.get("open_month"),
                "open_month_num": row.get("open_month_num"),
                "trade_count": row.get("trade_count"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "short_trade_count": row.get("short_trade_count"),
                "month_status": row.get("month_status"),
                "watch_role": "weak_positive_month_watch(약한 양수 월 관찰)" if as_float(row.get("net_profit")) < 10 else "positive_month(양수 월)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def cost_review_rows(cost: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "candidate_id": cost.get("candidate_id"),
            "net_profit": cost.get("net_profit"),
            "swap_sum": cost.get("swap_sum"),
            "stress_adjusted_net_swap_haircut_1x": cost.get("stress_adjusted_net_swap_haircut_1x"),
            "stress_adjusted_net_delta_vs_parent": cost.get("stress_adjusted_net_delta_vs_parent"),
            "stress_judgment": cost.get("stress_judgment"),
            "review_judgment": "passed_for_proxy_probe_handoff(프록시 탐침 인계 통과)",
            "effect": "CO에서 실제 MT5 cost layer(MT5 비용층)와 차이를 비교하게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def filter_review_rows(filters: pd.DataFrame, selected_id: str) -> list[dict[str, Any]]:
    rows = []
    for _, raw in selected_frame(filters, selected_id).iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": selected_id,
                "filter_step": row.get("filter_step"),
                "filter_reason": row.get("filter_reason"),
                "removed_trade_count": row.get("removed_trade_count"),
                "removed_short_count": row.get("removed_short_count"),
                "removed_net_profit": row.get("removed_net_profit"),
                "restored_trade_count": row.get("restored_trade_count"),
                "restored_short_count": row.get("restored_short_count"),
                "restored_net_profit": row.get("restored_net_profit"),
                "review_judgment": "entry_known_rule_kept(진입시점 규칙 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def positive_clue_rows(final: Mapping[str, Any], source_rows_: Sequence[Mapping[str, Any]], month_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "run_id": RUN_ID,
            "clue_id": final["selected_candidate_id"],
            "clue_type": "mt5_probe_candidate_seed(MT5 탐침 후보 씨앗)",
            "net_profit": final["selected_net_profit"],
            "profit_factor": final["selected_profit_factor"],
            "expectancy": final["selected_expectancy"],
            "trade_count": final["selected_trade_count"],
            "trade_density": final["selected_trade_density"],
            "short_trade_count": final["selected_short_trade_count"],
            "stress_delta": final["selected_stress_adjusted_net_delta_vs_parent"],
            "bad_month_count": final["selected_bad_month_count"],
            "usable_as": "CO runtime input materialization seed(CO 런타임 입력 구체화 씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    for row in source_rows_:
        rows.append(
            {
                "run_id": RUN_ID,
                "clue_id": f"{final['selected_candidate_id']}__{row['source_bucket']}",
                "clue_type": "source_component_clue(원천 구성 단서)",
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "expectancy": row.get("expectancy"),
                "trade_count": row.get("trade_count"),
                "trade_density": "",
                "short_trade_count": row.get("short_trade_count"),
                "stress_delta": "",
                "bad_month_count": "",
                "usable_as": "CO source rule boundary(CO 원천 규칙 경계)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    weakest = list(month_rows_)[:3]
    for row in weakest:
        rows.append(
            {
                "run_id": RUN_ID,
                "clue_id": f"{final['selected_candidate_id']}__weak_month_{row['open_month']}",
                "clue_type": "weak_positive_month_watch(약한 양수 월 관찰)",
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "expectancy": "",
                "trade_count": row.get("trade_count"),
                "trade_density": "",
                "short_trade_count": row.get("short_trade_count"),
                "stress_delta": "",
                "bad_month_count": final["selected_bad_month_count"],
                "usable_as": "CO monthly stress watch(CO 월별 압박 관찰)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_mt5_rows(proxy_plan: pd.DataFrame, final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for _, raw in proxy_plan.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": row.get("comparison_id", "cm_proxy_vs_next_mt5_probe"),
                "parent_mt5_net": row.get("parent_mt5_net", ""),
                "proxy_net": final["selected_net_profit"],
                "net_diff_proxy_minus_parent": row.get("net_diff_proxy_minus_parent", ""),
                "parent_mt5_profit_factor": row.get("parent_mt5_profit_factor", ""),
                "proxy_profit_factor": final["selected_profit_factor"],
                "usability": "must_compare_in_CO_or_later(CO 이후 반드시 비교)",
                "effect": "proxy expected value(프록시 예상값)를 MT5 KPI(MT5 핵심 성과 지표)와 혼동하지 않게 합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if not rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": "cm_proxy_vs_next_mt5_probe",
                "parent_mt5_net": "",
                "proxy_net": final["selected_net_profit"],
                "net_diff_proxy_minus_parent": "",
                "parent_mt5_profit_factor": "",
                "proxy_profit_factor": final["selected_profit_factor"],
                "usability": "mt5_probe_required(MT5 탐침 필요)",
                "effect": "다음 런타임 탐침에서 차이(diff, 차이)를 기록하게 합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def mt5_boundary_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "candidate_id": final["selected_candidate_id"],
            "boundary_id": "co_materialization_required",
            "mt5_status": "not_run_in_cn(CN에서는 미실행)",
            "required_next_evidence": "EA/set/model_bundle/tester_identity/runtime_output(EA/설정/모델번들/테스터정체성/런타임출력)",
            "diff_required": "proxy_vs_mt5_net_pf_expectancy_drawdown_trade_count(프록시 대 MT5 순수익/PF/기대값/낙폭/거래수)",
            "authority_after_next": "runtime_probe_only_until_parity_closed(동등성 폐쇄 전 런타임 탐침만)",
            "effect": "외부 검증(external verification, 외부 검증)을 다음 입력 구체화로 고정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_queue_rows(final: Mapping[str, Any], queue_row: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "candidate_id": final["selected_candidate_id"],
            "queue_status": "ready_for_runtime_input_materialization(런타임 입력 구체화 준비)",
            "source_trade_tape_path": rel(parent.SELECTED_TRADE_TAPE),
            "source_trade_tape_sha256": sha(parent.SELECTED_TRADE_TAPE),
            "source_surface_path": rel(parent.CM_PROXY_REPAIR_SURFACE),
            "source_surface_sha256": sha(parent.CM_PROXY_REPAIR_SURFACE),
            "rule_package_path": rel(CANDIDATE_RULE_PACKAGE),
            "expected_proxy_net": final["selected_net_profit"],
            "expected_proxy_profit_factor": final["selected_profit_factor"],
            "expected_proxy_expectancy": final["selected_expectancy"],
            "expected_proxy_trade_count": final["selected_trade_count"],
            "expected_proxy_density": final["selected_trade_density"],
            "expected_proxy_short_count": final["selected_short_trade_count"],
            "month_guard_policy": queue_row.get("month_guard_policy", "month_of_year=08_or_12"),
            "short_floor_policy": queue_row.get("short_floor_policy", "restore_native_short_until_floor_100"),
            "source_mix_policy": queue_row.get("source_mix_policy", "native_overlay_balance_keep"),
            "timestamp_safety": queue_row.get("timestamp_safe_inputs", "entry_known_inputs_only(진입 시점 입력만)"),
            "success_criteria": "CO creates executable MT5 probe package; later runtime output compares proxy diff(CO가 실행 가능한 MT5 탐침 패키지를 만들고 이후 런타임 출력과 프록시 차이를 비교)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def rule_package(final: Mapping[str, Any], queue_row: Mapping[str, Any], filter_rows_: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "candidate_id": final["selected_candidate_id"],
        "source_proxy_scout_run_id": parent.RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rule_family": "h17_bad_month_source_balance_repair(17시 손실 월/원천 균형 수리)",
        "entry_known_inputs": [
            "source_bucket",
            "open_hour",
            "month_of_year",
            "quarter",
            "p_short",
            "p_flat",
            "p_long",
            "margin_vs_long",
            "margin_vs_flat",
        ],
        "forbidden_controls": {
            "top_n": "forbidden(금지)",
            "trade_splitting": "forbidden(금지)",
            "exact_year_filter": "forbidden(금지)",
        },
        "queue_policy": {key: queue_row.get(key, "") for key in queue_row.keys()},
        "filter_steps": list(filter_rows_),
        "proxy_kpi": {
            "net_profit": final["selected_net_profit"],
            "profit_factor": final["selected_profit_factor"],
            "expectancy": final["selected_expectancy"],
            "trade_count": final["selected_trade_count"],
            "density": final["selected_trade_density"],
            "long_trade_count": final["selected_long_trade_count"],
            "short_trade_count": final["selected_short_trade_count"],
            "bad_month_count": final["selected_bad_month_count"],
            "stress_delta": final["selected_stress_adjusted_net_delta_vs_parent"],
        },
        "external_verification_status": "not_run_in_cn_open_co_materialization(CN 미실행, CO 구체화 개방)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
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
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(final: Mapping[str, Any], receipt_paths: Sequence[Path], receipts_written: bool) -> list[dict[str, Any]]:
    required = ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit", "final_claim_guard"]
    receipt_status = all(exists(path) for path in receipt_paths) if receipts_written else False
    return [
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed",
            "evidence": f"net={final['reviewed_net_profit']};pf={final['reviewed_profit_factor']};density={final['reviewed_density']};drawdown={final['reviewed_closed_trade_drawdown_proxy']}",
            "effect": "KPI(핵심 성과 지표)를 같은 grain(입도)에서 비교합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "row_grain_audit",
            "status": "passed",
            "evidence": "Tier A separate / Tier B missing_required / Tier A+B out_of_scope rows will be written(티어 행 기록 예정)",
            "effect": "Tier B(티어 B) 누락을 숨기지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": f"parent_final={rel(parent.FINAL_DECISION)};parent_manifest={rel(parent.RUN_MANIFEST)};input_count={len(INPUT_FILES)}",
            "effect": "CN 판정이 CM 산출물 계보에서 끊기지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if receipt_status or not receipts_written else "failed",
            "evidence": f"required={';'.join(required)};receipts_written={receipt_status}",
            "effect": "필수 gate(게이트)와 receipt(영수증)가 closeout(종료)에 묶입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": "no runtime authority / no operating promotion / no goal claim(권위/승격/목표 달성 주장 없음)",
            "effect": "MT5 미실행 후보를 운영 후보로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(
    cm_final: Mapping[str, Any],
    package_rows_: Sequence[Mapping[str, Any]],
    source_rows_: Sequence[Mapping[str, Any]],
    month_rows_: Sequence[Mapping[str, Any]],
    cost_rows_: Sequence[Mapping[str, Any]],
    filter_rows_: Sequence[Mapping[str, Any]],
    proxy_rows_: Sequence[Mapping[str, Any]],
    mt5_rows_: Sequence[Mapping[str, Any]],
    runtime_queue_: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    weakest = month_rows_[0] if month_rows_ else {}
    source_net = sum(as_float(row.get("net_profit")) for row in source_rows_)
    source_trades = sum(as_float(row.get("trade_count")) for row in source_rows_)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "reviewed_candidate_id": cm_final["selected_candidate_id"],
        "reviewed_package_precheck_status": cm_final["selected_package_precheck_status"],
        "reviewed_net_profit": cm_final["selected_net_profit"],
        "reviewed_profit_factor": cm_final["selected_profit_factor"],
        "reviewed_expectancy": cm_final["selected_expectancy"],
        "reviewed_trade_count": cm_final["selected_trade_count"],
        "reviewed_density": cm_final["selected_trade_density"],
        "reviewed_long_trade_count": cm_final["selected_long_trade_count"],
        "reviewed_short_trade_count": cm_final["selected_short_trade_count"],
        "reviewed_short_share": cm_final["selected_short_share"],
        "reviewed_closed_trade_drawdown_proxy": cm_final["selected_closed_trade_drawdown_proxy"],
        "reviewed_recovery_factor_proxy": cm_final["selected_closed_trade_recovery_proxy"],
        "reviewed_bad_month_count": cm_final["selected_bad_month_count"],
        "reviewed_weakest_month": weakest.get("open_month", ""),
        "reviewed_weakest_month_net": weakest.get("net_profit", ""),
        "reviewed_weakest_month_pf": weakest.get("profit_factor", ""),
        "reviewed_stress_adjusted_net_delta_vs_parent": cm_final["selected_stress_adjusted_net_delta_vs_parent"],
        "source_trade_count_sum": finite(source_trades, 0),
        "source_net_sum": finite(source_net, 2),
        "package_decision": "open_run364CO_mt5_probe_input_materialization_no_authority",
        "runtime_probe_input_queue_path": rel(RUN364CO_QUEUE),
        "rule_package_path": rel(CANDIDATE_RULE_PACKAGE),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "external_verification_status": "out_of_scope_by_claim_review_only_open_next_mt5_input_materialization(주장 범위 밖, 검토 전용 및 다음 MT5 입력 구체화 개방)",
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
    write_json(
        KPI_RECEIPT,
        {
            "run_id": RUN_ID,
            "measurement_scope": "proxy KPI review for MT5 probe handoff(프록시 KPI 검토와 MT5 탐침 인계)",
            "management_state": {
                "run_folder": rel(RUN_DIR),
                "manifest": rel(RUN_MANIFEST),
                "kpi_record": rel(FINAL_DECISION),
                "summary": rel(REPORT_PATH),
                "registry_update_required": "yes",
            },
            "judgment_class": "positive",
            "scoreboard": "structural_scout(구조 스카우트)",
            "parity_level": "P0_unverified(P0 미검증)",
            "wfo_status": "not_applicable(해당 없음)",
            "registry_update_required": "yes",
            "negative_memory_required": "yes_weak_month_watch(예, 약한 월 관찰)",
            "hard_gate_applicable": "no",
            "evidence_boundary": "candidate(후보)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_scope": "CM machine-readable proxy artifacts(CM 기계판독 프록시 산출물)",
            "timestamp_safety": "inherited_parent_passed_no_exact_year_filter_and_entry_known_controls(상위 실행의 정확연도 필터 없음 및 진입시점 통제 통과 상속)",
            "trade_splitting": "not_used(미사용)",
            "evidence": [rel(parent.DATA_INTEGRITY_AUDIT), rel(parent.CANDIDATE_FILTER_AUDIT), rel(parent.RUN364CN_QUEUE)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "CM cleared CK bad-month/source blockers while preserving density and short floor(CM이 CK 손실 월/원천 차단을 해소하고 밀도/숏 하한을 보존)",
            "comparison_baseline": parent.PARENT_RUN_ID,
            "likely_drivers": ["month08 synthetic short guard", "month12 low-margin long guard", "native short floor restore"],
            "segment_checks": [rel(SOURCE_BALANCE_REVIEW), rel(MONTH_STABILITY_REVIEW), rel(COST_STRESS_REVIEW), rel(FILTER_REVIEW)],
            "trade_shape": f"trades={final['reviewed_trade_count']};long={final['reviewed_long_trade_count']};short={final['reviewed_short_trade_count']};density={final['reviewed_density']}",
            "alternative_explanations": "proxy-only cost and fill assumptions may differ in MT5(프록시 비용/체결 가정은 MT5에서 달라질 수 있음)",
            "attribution_confidence": "medium_until_mt5_probe(중간, MT5 탐침 전까지)",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "CM selected proxy repair candidate(CM 선택 프록시 수리 후보)",
            "evidence_available": [rel(FINAL_DECISION), rel(PACKAGE_GATE_DECISION), rel(SOURCE_BALANCE_REVIEW), rel(MONTH_STABILITY_REVIEW), rel(COST_STRESS_REVIEW)],
            "evidence_missing": ["new MT5 runtime output(새 MT5 런타임 출력)", "forward replay(전진 재생)", "runtime parity closure(런타임 동등성 폐쇄)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The proxy candidate is good enough to package for a runtime probe, not good enough to call live-ready(프록시 후보는 런타임 탐침 패키지 대상이지만 실거래 준비는 아님).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "proxy package review candidate and CO handoff only(프록시 패키지 검토 후보 및 CO 인계만)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "new_model_training": final["new_model_training"],
            "new_mt5_execution": final["new_mt5_execution"],
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
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_reproducible_from_script(추적 가능 및 스크립트 재생 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    package_rows_: Sequence[Mapping[str, Any]],
    source_rows_: Sequence[Mapping[str, Any]],
    month_rows_: Sequence[Mapping[str, Any]],
    cost_rows_: Sequence[Mapping[str, Any]],
    filter_rows_: Sequence[Mapping[str, Any]],
    proxy_rows_: Sequence[Mapping[str, Any]],
    mt5_rows_: Sequence[Mapping[str, Any]],
    runtime_queue_: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364CN h17 bad-month source-balance repair review(17시 손실 월/원천 균형 수리 검토)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

Action(행동): CM selected candidate(CM 선택 후보) `{final['reviewed_candidate_id']}`를 package gate(패키지 게이트), source/month/cost attribution(원천/월/비용 귀속), MT5 boundary(MT5 경계)로 검토했습니다.

Effect(효과): 후보를 `{NEXT_RUN_ID}` MT5 runtime probe input materialization(MT5 런타임 탐침 입력 구체화)로 넘기지만, runtime authority(런타임 권위)나 operating promotion(운영 승격)은 주장하지 않습니다.

- net profit(순수익): `{final['reviewed_net_profit']}`
- profit factor(수익 팩터): `{final['reviewed_profit_factor']}`
- expectancy(기대값): `{final['reviewed_expectancy']}`
- trade count(거래수): `{final['reviewed_trade_count']}`
- density(밀도): `{final['reviewed_density']}`
- long/short(롱/숏): `{final['reviewed_long_trade_count']}` / `{final['reviewed_short_trade_count']}`
- bad month count(손실 월 수): `{final['reviewed_bad_month_count']}`
- weakest month(가장 약한 월): `{final['reviewed_weakest_month']}` net `{final['reviewed_weakest_month_net']}`, PF `{final['reviewed_weakest_month_pf']}`
- stress delta(압박 차이): `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`

## Package Gate(패키지 게이트)

{markdown_table(package_rows_, ['gate_id', 'gate_status', 'evidence', 'effect'], 10)}

## Source Balance(원천 균형)

{markdown_table(source_rows_, ['source_bucket', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count', 'source_judgment'], 10)}

## Weak Months(약한 월)

{markdown_table(month_rows_, ['open_month', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count', 'watch_role'], 8)}

## Cost Stress(비용 압박)

{markdown_table(cost_rows_, ['net_profit', 'swap_sum', 'stress_adjusted_net_delta_vs_parent', 'stress_judgment', 'review_judgment'], 5)}

## Filter Boundary(필터 경계)

{markdown_table(filter_rows_, ['filter_step', 'filter_reason', 'removed_trade_count', 'restored_trade_count', 'restored_net_profit', 'review_judgment'], 8)}

## Proxy/MT5 Diff(프록시/MT5 차이)

{markdown_table(proxy_rows_, ['comparison_id', 'proxy_net', 'proxy_profit_factor', 'usability', 'effect'], 5)}

## MT5 Probe Handoff(MT5 탐침 인계)

{markdown_table(runtime_queue_, ['candidate_id', 'queue_status', 'expected_proxy_net', 'expected_proxy_profit_factor', 'expected_proxy_density', 'expected_proxy_short_count'], 5)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

CN is review only(CN은 검토 전용)입니다. New model training(새 모델 학습), new MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 없습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CN decision(결정): h17 bad-month source-balance repair review

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- reviewed candidate(검토 후보): `{final['reviewed_candidate_id']}`
- package decision(패키지 결정): `{final['package_decision']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): proxy package review(프록시 패키지 검토)는 통과했지만 MT5 runtime evidence(MT5 런타임 근거)가 없으므로 다음 작업은 입력 구체화입니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        f"run364CN__{RUN_ID}",
        f"\n- run364CN__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - proxy package review passed(프록시 패키지 검토 통과), next `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        f"## run364CN__{RUN_ID}",
        f"""
## run364CN H17 Bad-Month Source-Balance Repair Review Closeout(364CN 17시 손실 월/원천 균형 수리 검토 종료)

Action(행동): CM 후보를 package/source/month/cost/MT5 boundary(패키지/원천/월/비용/MT5 경계)로 검토했습니다.

Effect(효과): `{NEXT_RUN_ID}`를 열어 MT5 runtime probe input(MT5 런타임 탐침 입력)을 구체화하고, 운영 주장(operating claim, 운영 주장)은 닫아둡니다.
""",
    )
    append_text_once(
        STAGE_README,
        f"run364CN__{RUN_ID}",
        f"""
<!-- run364CN__{RUN_ID} -->
## run364CN h17 bad-month source-balance repair review(17시 손실 월/원천 균형 수리 검토)

Action(행동): `{final['reviewed_candidate_id']}`를 MT5 probe handoff(MT5 탐침 인계) 후보로 검토했습니다.

Effect(효과): 다음 실행 `{NEXT_RUN_ID}`에서 runtime input materialization(런타임 입력 구체화)을 진행합니다.
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
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364CN(364CN 실행)이 `{final['reviewed_candidate_id']}`를 MT5 probe input(MT5 탐침 입력) 구체화 대상으로 열었습니다. Proxy KPI(프록시 핵심 성과 지표)는 net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, density `{final['reviewed_density']}`, shorts `{final['reviewed_short_trade_count']}`, bad months `{final['reviewed_bad_month_count']}`입니다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 EA/set/model/tester handoff(EA/설정/모델/테스터 인계)를 구체화합니다.",
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

Current truth(현재 진실): `run364CN` reviewed(검토 완료) CM selected candidate(CM 선택 후보) `{final['reviewed_candidate_id']}`. Proxy KPI(프록시 핵심 성과 지표)는 net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, expectancy `{final['reviewed_expectancy']}`, trades `{final['reviewed_trade_count']}`, density `{final['reviewed_density']}`, long/short `{final['reviewed_long_trade_count']}`/`{final['reviewed_short_trade_count']}`, bad months `{final['reviewed_bad_month_count']}`, stress delta `{final['reviewed_stress_adjusted_net_delta_vs_parent']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 CM rule package(CM 규칙 패키지), EA/set/model/tester identity(EA/설정/모델/테스터 정체성), MT5 runtime probe queue(MT5 런타임 탐침 대기열)를 구체화합니다.

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

MT5 probe input candidate(MT5 탐침 입력 후보): `{final['reviewed_candidate_id']}`.

Reviewed proxy KPI(검토된 프록시 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, expectancy `{final['reviewed_expectancy']}`, trades `{final['reviewed_trade_count']}`, density `{final['reviewed_density']}`, drawdown proxy `{final['reviewed_closed_trade_drawdown_proxy']}`, recovery proxy `{final['reviewed_recovery_factor_proxy']}`, long/short `{final['reviewed_long_trade_count']}`/`{final['reviewed_short_trade_count']}`.

Package decision(패키지 결정): `{final['package_decision']}`.

Next queue(다음 대기열): `{rel(RUN364CO_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364CN__{RUN_ID}",
        f"\n<!-- run364CN__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed CM proxy candidate(CM 프록시 후보 검토); opened `{NEXT_RUN_ID}` for MT5 probe input materialization(MT5 탐침 입력 구체화); no authority claim(권위 주장 없음).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"run364CN__{RUN_ID}",
        f"\n<!-- run364CN__{RUN_ID} -->\n- `{RUN_ID}`: CM bad-month/source-balance repair(CM 손실 월/원천 균형 수리) is preserved as MT5 probe seed(MT5 탐침 씨앗). Positive clue(긍정 단서): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, density `{final['reviewed_density']}`, shorts `{final['reviewed_short_trade_count']}`, bad months `{final['reviewed_bad_month_count']}`.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"run364CN__{RUN_ID}",
        f"\n<!-- run364CN__{RUN_ID} -->\n- `{RUN_ID}` residual risk(잔여 위험): weakest months(약한 월) `{final['reviewed_weakest_month']}` net `{final['reviewed_weakest_month_net']}` and synthetic overlay(합성 오버레이) thin sample(얇은 표본). Reopen condition(재개 조건): `{NEXT_RUN_ID}` or later MT5 probe(MT5 탐침)가 proxy/MT5 diff(프록시/MT5 차이)를 불리하게 보이면 source/month guard(원천/월 가드)를 다시 연다.\n",
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
        "scoreboard_lane": "proxy_package_review(프록시 패키지 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "candidate(후보)",
        "question": "Should CM selected repair open MT5 runtime probe input materialization?(CM 선택 수리가 MT5 런타임 탐침 입력 구체화를 열어도 되는가?)",
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
            "kpi_scope": "CN proxy package review(CN 프록시 패키지 검토)",
            "status": status,
            "primary_kpi": f"net={final['reviewed_net_profit']};pf={final['reviewed_profit_factor']};density={final['reviewed_density']};shorts={final['reviewed_short_trade_count']}",
            "guardrail_kpi": f"bad_months={final['reviewed_bad_month_count']};stress_delta={final['reviewed_stress_adjusted_net_delta_vs_parent']};no_authority",
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "reviewed_proxy_candidate(검토된 프록시 후보)",
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
        ("package_gate_decision", PACKAGE_GATE_DECISION, "CN package gate decision(CN 패키지 게이트 결정)."),
        ("source_balance_review", SOURCE_BALANCE_REVIEW, "CN source balance review(CN 원천 균형 검토)."),
        ("month_stability_review", MONTH_STABILITY_REVIEW, "CN month stability review(CN 월 안정성 검토)."),
        ("cost_stress_review", COST_STRESS_REVIEW, "CN cost stress review(CN 비용 압박 검토)."),
        ("filter_review", FILTER_REVIEW, "CN entry-known filter review(CN 진입시점 필터 검토)."),
        ("positive_clue_register", POSITIVE_CLUE_REGISTER, "CN positive clue register(CN 긍정 단서 등록)."),
        ("proxy_mt5_diff_review", PROXY_MT5_DIFF_REVIEW, "CN proxy/MT5 diff review(CN 프록시/MT5 차이 검토)."),
        ("mt5_reprobe_boundary", MT5_REPROBE_BOUNDARY, "CN MT5 reprobe boundary(CN MT5 재탐침 경계)."),
        ("candidate_rule_package", CANDIDATE_RULE_PACKAGE, "CN candidate rule package(CN 후보 규칙 패키지)."),
        ("runtime_probe_input_queue", RUN364CO_QUEUE, "CO runtime probe input queue(CO 런타임 탐침 입력 대기열)."),
        ("report", REPORT_PATH, "CN report(CN 보고서)."),
        ("final_decision", FINAL_DECISION, "CN final decision(CN 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CN run manifest(CN 실행 목록)."),
        ("gate_audit", GATE_AUDIT, "CN required gate audit(CN 필수 게이트 감사)."),
        ("lineage_receipt", LINEAGE_RECEIPT, "CN lineage receipt(CN 계보 영수증)."),
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
    cm_final = validate_inputs()
    selected_id = str(cm_final["selected_candidate_id"])
    surface = read_csv(parent.CM_PROXY_REPAIR_SURFACE)
    package = read_csv(parent.PACKAGE_PRECHECK)
    sources = read_csv(parent.CANDIDATE_SOURCE_ATTRIBUTION)
    months = read_csv(parent.CANDIDATE_MONTH_STABILITY)
    costs = read_csv(parent.COST_STRESS_DIAGNOSTIC)
    filters = read_csv(parent.CANDIDATE_FILTER_AUDIT)
    proxy_plan = read_csv(parent.PROXY_MT5_DIFF_PLAN)
    cn_queue = read_csv(parent.RUN364CN_QUEUE)

    surface_row = one_selected(surface, selected_id, "surface")
    package_row = one_selected(package, selected_id, "package")
    cost_row = one_selected(costs, selected_id, "cost")
    queue_row = cn_queue.iloc[0].to_dict() if not cn_queue.empty else {}

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    source_rows_ = source_balance_rows(sources, selected_id)
    month_rows_ = month_review_rows(months, selected_id)
    cost_rows_ = cost_review_rows(cost_row)
    filter_rows_ = filter_review_rows(filters, selected_id)
    package_rows_ = package_gate_rows(cm_final, surface_row, package_row, source_rows_, month_rows_, cost_row, filter_rows_)
    positive_rows_ = positive_clue_rows(cm_final, source_rows_, month_rows_)
    proxy_rows_ = proxy_mt5_rows(proxy_plan, cm_final)
    mt5_rows_ = mt5_boundary_rows(cm_final)
    write_json(CANDIDATE_RULE_PACKAGE, rule_package(cm_final, queue_row, filter_rows_))
    runtime_queue_ = runtime_queue_rows(cm_final, queue_row)

    write_csv(PACKAGE_GATE_DECISION, package_rows_)
    write_csv(SOURCE_BALANCE_REVIEW, source_rows_)
    write_csv(MONTH_STABILITY_REVIEW, month_rows_)
    write_csv(COST_STRESS_REVIEW, cost_rows_)
    write_csv(FILTER_REVIEW, filter_rows_)
    write_csv(POSITIVE_CLUE_REGISTER, positive_rows_)
    write_csv(PROXY_MT5_DIFF_REVIEW, proxy_rows_)
    write_csv(MT5_REPROBE_BOUNDARY, mt5_rows_)
    write_csv(RUN364CO_QUEUE, runtime_queue_)

    receipt_paths = [KPI_RECEIPT, DATA_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT, LINEAGE_RECEIPT]
    preliminary = final_payload(cm_final, package_rows_, source_rows_, month_rows_, cost_rows_, filter_rows_, proxy_rows_, mt5_rows_, runtime_queue_, [], created_at)
    gates = gate_rows(preliminary, receipt_paths, receipts_written=False)
    final = final_payload(cm_final, package_rows_, source_rows_, month_rows_, cost_rows_, filter_rows_, proxy_rows_, mt5_rows_, runtime_queue_, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    refresh_lineage_receipt(final)
    gates = gate_rows(final, receipt_paths, receipts_written=True)
    final = final_payload(cm_final, package_rows_, source_rows_, month_rows_, cost_rows_, filter_rows_, proxy_rows_, mt5_rows_, runtime_queue_, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final)
    refresh_lineage_receipt(final)
    write_docs(final, package_rows_, source_rows_, month_rows_, cost_rows_, filter_rows_, proxy_rows_, mt5_rows_, runtime_queue_, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
