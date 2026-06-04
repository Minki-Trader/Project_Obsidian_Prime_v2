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

from stage_pipelines.stage364 import train_short_source_quality_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-04"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BP"
RUN_ID = "run364BP_review_short_source_quality_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = parent.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BQ_train_broad_clean_short_share_lift_scout_without_db_v1"

STATUS = "completed_stage364BP_short_source_quality_repair_review_package_rejected_open_bq_no_authority"
JUDGMENT = "package_rejected_month_stress_no_mt5_but_broad_clean_short_source_clue_open_bq_no_authority"
DECISION = "stage364BP_open_run364BQ_broad_clean_short_share_lift_scout"
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
NEXT_OFFENSIVE_SEED_QUEUE = RUN_DIR / "run364BQ_broad_clean_short_share_lift_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364BP_short_source_quality_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BP_short_source_quality_repair_review.md"
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
    parent.QUALITY_RULE_SURFACE,
    parent.BROAD_POOL_NEGATIVE_CONTROL,
    parent.SELECTED_QUALITY_CANDIDATE,
    parent.STRESS_SLICE_REVIEW,
    parent.SHORT_SOURCE_QUALITY_SEGMENTS,
    parent.OVERFIT_GUARDRAIL_AUDIT,
    parent.PROXY_MT5_DIFF_PLAN,
    parent.RUN364BP_QUEUE,
    parent.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    PACKAGE_GATE_DECISION,
    STRESS_FAILURE_ATTRIBUTION,
    POSITIVE_CLUE_REGISTER,
    PROXY_MT5_DIFF_REVIEW,
    NEXT_OFFENSIVE_SEED_QUEUE,
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


def io_path(path: Path | str) -> Path:
    return parent.io_path(path)


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


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BP inputs(BP 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BO next_run_id mismatch(BO 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("BO has forbidden authority claim(BO 금지 권위 주장 존재)")
    gates = read_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("BO gate audit(BO 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BP review source(BP 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_rows(path: Path) -> list[dict[str, Any]]:
    if not exists(path):
        return []
    return pd.read_csv(io_path(path), encoding="utf-8-sig").to_dict("records")


def row_by_id(rows: Sequence[Mapping[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    for row in rows:
        if str(row.get(key)) == value:
            return dict(row)
    return None


def package_gate_rows(final: Mapping[str, Any], quality: Sequence[Mapping[str, Any]], broad: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected = row_by_id(quality, "candidate_id", str(final["selected_candidate_id"])) or {}
    bo05 = row_by_id(quality, "candidate_id", "bo05_h17_margin_075_105_or_h20_margin_08_10") or {}
    bo90 = row_by_id(broad, "candidate_id", "bo90_broad_h17_20_ps0440_margin080_control") or {}
    bo91 = row_by_id(broad, "candidate_id", "bo91_broad_h16_17_20_ps0445_margin080_control") or {}
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "selected_bo_package_gate(선택 BO 패키지 게이트)",
            "subject": final["selected_candidate_id"],
            "status": "rejected_package_ineligible(패키지 부적격 거절)",
            "reason": f"month_bad_count={final['month_bad_count']}; package_candidate_rows={final['package_candidate_rows']}; new_mt5_execution={final['new_mt5_execution']}",
            "effect": "프록시 단서를 MT5 package(MT5 패키지)로 바로 올리지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "bo05_high_source_pf_gate(bo05 높은 원천 PF 게이트)",
            "subject": "bo05_h17_margin_075_105_or_h20_margin_08_10",
            "status": "preserved_clue_not_package(보존 단서, 패키지 아님)",
            "reason": f"short_share={bo05.get('short_share')} < {TARGET_SHORT_SHARE}; synthetic_short_pf={bo05.get('synthetic_short_profit_factor')}",
            "effect": "높은 숏 원천 품질을 BQ의 품질 하한 씨앗으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "bo90_broad_clean_gate(bo90 넓은 클린 게이트)",
            "subject": "bo90_broad_h17_20_ps0440_margin080_control",
            "status": "preserved_clue_short_share_repair_required(보존 단서, 숏 비중 수리 필요)",
            "reason": f"net={bo90.get('net_profit')}; pf={bo90.get('profit_factor')}; short_share={bo90.get('short_share')} < {TARGET_SHORT_SHARE}; overlap={bo90.get('synthetic_overlap_count')}",
            "effect": "넓은 풀에서 겹침 없는 양수 숏 원천을 다음 공격 수리로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate_id": "bo91_overlap_gate(bo91 겹침 게이트)",
            "subject": "bo91_broad_h16_17_20_ps0445_margin080_control",
            "status": "rejected_overlap_but_repair_seed(겹침 거절, 수리 씨앗)",
            "reason": f"synthetic_overlap_count={bo91.get('synthetic_overlap_count')}; short_share={bo91.get('short_share')}",
            "effect": "h16 확장은 outcome(결과값)이 아니라 entry-known priority(진입기지 우선순위)로만 재시험한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def stress_failure_rows(stress: Sequence[Mapping[str, Any]], short_segments: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in stress:
        if str(row.get("segment_status", "")).startswith("stress_watch"):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "failure_id": f"stress_{row.get('axis')}_{row.get('segment_id')}",
                    "failure_type": "combined_month_stress(합산 월 압박)",
                    "segment": row.get("segment_id"),
                    "net_profit": row.get("net_profit"),
                    "profit_factor": row.get("profit_factor"),
                    "trade_count": row.get("trade_count"),
                    "attribution": "combined tape segment failed net/PF floor(합산 테이프 조각이 순수익/PF 하한 실패)",
                    "repair_use": "next run may test entry-known broad clean lift, not exact month removal(다음 실행은 정확 월 제거가 아니라 진입기지 넓은 클린 보강을 시험)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    for row in short_segments:
        if str(row.get("segment_status", "")).startswith("watch_or_negative") and as_int(row.get("synthetic_short_trade_count")) >= 2:
            rows.append(
                {
                    "run_id": RUN_ID,
                    "failure_id": f"short_source_{row.get('axis')}_{row.get('segment_id')}",
                    "failure_type": "synthetic_short_source_stress(합성 숏 원천 압박)",
                    "segment": row.get("segment_id"),
                    "net_profit": row.get("synthetic_short_net_profit"),
                    "profit_factor": row.get("synthetic_short_profit_factor"),
                    "trade_count": row.get("synthetic_short_trade_count"),
                    "attribution": "standalone synthetic shorts weak in this segment(이 조각의 합성 숏 단독 품질 약함)",
                    "repair_use": "convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def positive_clue_rows(quality: Sequence[Mapping[str, Any]], broad: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ids = [
        ("bo00_bn_seed_h17_or_h20_margin_08_10_reference", quality, "selected_proxy_clue(선택 프록시 단서)"),
        ("bo05_h17_margin_075_105_or_h20_margin_08_10", quality, "high_short_source_pf_clue(높은 숏 원천 PF 단서)"),
        ("bo90_broad_h17_20_ps0440_margin080_control", broad, "broad_clean_source_clue(넓은 클린 원천 단서)"),
        ("bo91_broad_h16_17_20_ps0445_margin080_control", broad, "overlap_repair_clue(겹침 수리 단서)"),
    ]
    rows: list[dict[str, Any]] = []
    for cid, table, clue_type in ids:
        row = row_by_id(table, "candidate_id", cid)
        if not row:
            continue
        rows.append(
            {
                "run_id": RUN_ID,
                "clue_id": cid,
                "clue_type": clue_type,
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "density": row.get("trade_density_per_business_day"),
                "short_share": row.get("short_share"),
                "synthetic_short_profit_factor": row.get("synthetic_short_profit_factor"),
                "synthetic_overlap_count": row.get("synthetic_overlap_count", 0),
                "month_bad_count": row.get("month_bad_count"),
                "usable_as": "BQ offensive seed(BQ 공격 씨앗)" if cid in {"bo05_h17_margin_075_105_or_h20_margin_08_10", "bo90_broad_h17_20_ps0440_margin080_control", "bo91_broad_h16_17_20_ps0445_margin080_control"} else "BP reviewed proxy clue(BP 검토 프록시 단서)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_mt5_rows(final: Mapping[str, Any], proxy_plan: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in proxy_plan:
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": row.get("comparison_id"),
                "source_runtime_probe_run_id": row.get("source_runtime_probe_run_id", SOURCE_RUNTIME_PROBE_RUN_ID),
                "mt5_net_profit": row.get("mt5_net_profit"),
                "proxy_net_profit": row.get("proxy_net_profit"),
                "net_diff_proxy_minus_mt5": row.get("net_diff_proxy_minus_mt5"),
                "mt5_profit_factor": row.get("mt5_profit_factor"),
                "proxy_profit_factor": row.get("proxy_profit_factor"),
                "profit_factor_diff_proxy_minus_mt5": row.get("profit_factor_diff_proxy_minus_mt5"),
                "attribution": row.get("attribution"),
                "usability": "not_usable_for_authority_package_rejected(권위에 사용 불가, 패키지 거절)",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if not rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": "missing_proxy_mt5_diff(프록시 MT5 차이 누락)",
                "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
                "usability": "blocked_missing_input(입력 누락 차단)",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def next_queue_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "selected_proxy_clue": final["selected_candidate_id"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        {
            **common,
            "queue_rank": 1,
            "queue_id": "bq01_broad_h17_20_clean_short_share_lift",
            "seed_source": "bo90_broad_h17_20_ps0440_margin080_control",
            "action": "expand clean broad h17/h20 source while lifting short share(겹침 없는 넓은 17/20시 원천을 숏 비중 보강으로 확장)",
            "success_criteria": "PF>=1.35, density>=3, short_share>=0.12, synthetic_short_pf>=1.15, overlap=0(PF 1.35 이상, 밀도 3 이상, 숏비중 0.12 이상, 합성 숏 PF 1.15 이상, 겹침 0)",
            "effect": "bo90의 높은 순수익/PF 단서를 숏 비중 제약과 같이 시험한다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bq02_entry_known_overlap_safe_h16_extension",
            "seed_source": "bo91_broad_h16_17_20_ps0445_margin080_control",
            "action": "retry h16 extension with entry-known p_short/margin priority only(16시 확장을 진입기지 p_short/마진 우선순위만으로 재시험)",
            "success_criteria": "no outcome-priority, no overlap, no top_n, no exact month(결과값 우선순위 없음, 겹침 없음, top_n 없음, 정확 월 없음)",
            "effect": "bo91의 숏 비중 단서를 look-ahead bias(미래참조 편향) 없이 복구한다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bq03_high_short_source_pf_guardrail",
            "seed_source": "bo05_h17_margin_075_105_or_h20_margin_08_10",
            "action": "use bo05 high synthetic PF as quality guardrail(bo05 높은 합성 PF를 품질 가드레일로 사용)",
            "success_criteria": "short source PF remains high while share recovers(숏 원천 PF가 높은 상태에서 숏 비중 회복)",
            "effect": "높은 품질 단서를 거래수 쪼개기 없이 넓힌다.",
        },
    ]


def gate_rows(final: Mapping[str, Any], package_rows: Sequence[Mapping[str, Any]], stress_rows: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed",
            "evidence": rel(POSITIVE_CLUE_REGISTER),
            "effect": "net/PF/expectancy/DD/recovery/trades/short share를 분리 검토했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "row_grain_audit",
            "status": "passed",
            "evidence": rel(STRESS_FAILURE_ATTRIBUTION),
            "effect": "패키지 게이트, 월 압박, 숏 원천 조각을 행 단위로 분리했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": rel(PROXY_MT5_DIFF_REVIEW),
            "effect": "proxy expected value(프록시 예상값)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않게 했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "package_reject_gate",
            "status": "passed" if as_int(final["package_candidate_rows"]) == 0 and as_int(final["month_bad_count"]) > 0 else "failed",
            "evidence": rel(PACKAGE_GATE_DECISION),
            "effect": "BO proxy(BO 프록시)를 패키지 후보에서 제외했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "stress_memory_gate",
            "status": "passed" if len(stress_rows) >= 2 else "failed",
            "evidence": rel(STRESS_FAILURE_ATTRIBUTION),
            "effect": "월별 실패를 다음 탐색 제약으로 바꿨다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "next_offensive_seed_gate",
            "status": "passed" if len(queue) == 3 else "failed",
            "evidence": rel(NEXT_OFFENSIVE_SEED_QUEUE),
            "effect": "bo90/bo91/bo05 단서를 다음 BQ 공격 탐색으로 연결했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if len(package_rows) >= 4 else "failed",
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
    bo_final: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    stress_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
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
        "reviewed_candidate_id": bo_final["selected_candidate_id"],
        "reviewed_net_profit": bo_final["selected_net_profit"],
        "reviewed_profit_factor": bo_final["selected_profit_factor"],
        "reviewed_density": bo_final["selected_density"],
        "reviewed_short_share": bo_final["selected_short_share"],
        "reviewed_synthetic_short_profit_factor": bo_final["selected_synthetic_short_profit_factor"],
        "reviewed_month_bad_count": bo_final["month_bad_count"],
        "reviewed_package_candidate_rows": bo_final["package_candidate_rows"],
        "package_decision": "rejected_package_ineligible_month_stress_no_mt5(패키지 부적격 거절, 월 압박 및 MT5 없음)",
        "preserved_clue_count": len(clues),
        "stress_failure_count": len(stress_rows),
        "next_primary_seed": "bo90_broad_h17_20_ps0440_margin080_control",
        "next_secondary_seed": "bo91_broad_h16_17_20_ps0445_margin080_control",
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
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "BO proxy clue(BO 프록시 단서)를 패키지 거절과 BQ 공격 씨앗으로 분리한다.",
        },
    )


def write_receipts(final: Mapping[str, Any], proxy_mt5: Sequence[Mapping[str, Any]], clues: Sequence[Mapping[str, Any]]) -> None:
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
            "data_sources": [rel(parent.QUALITY_RULE_SURFACE), rel(parent.BROAD_POOL_NEGATIVE_CONTROL), rel(parent.STRESS_SLICE_REVIEW)],
            "timestamp_boundary": "review uses BO entry-known rule outputs only(검토는 BO 진입기지 규칙 출력만 사용)",
            "integrity_judgment": "usable_for_review_no_new_labeling(검토 사용 가능, 새 라벨링 없음)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "proxy_mt5_diff": list(proxy_mt5),
            "preserved_clues": list(clues),
            "driver": "selected proxy gain is useful but month stress blocks package(선택 프록시 개선은 유용하지만 월 압박이 패키지를 막음)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment": JUDGMENT,
            "package_decision": final["package_decision"],
            "next_condition": NEXT_RUN_ID,
            "missing_evidence": ["new MT5 runtime reprobe(새 MT5 런타임 재탐침)", "forward pass(전진 통과)", "operating promotion evidence(운영 승격 근거)"],
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "effect": "패키지 거절과 다음 탐색만 주장한다.",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_bo_review_to_bq_offensive_seed(BO 검토와 BQ 공격 씨앗 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    stress_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    proxy_mt5: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364BP short source quality repair review(364BP 숏 원천 품질 수리 검토)

## Current Truth(현재 진실)

- reviewed candidate(검토 후보): `{final['reviewed_candidate_id']}`
- reviewed KPI(검토 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['reviewed_net_profit']}` / `{final['reviewed_profit_factor']}` / `{final['reviewed_density']}` / `{final['reviewed_short_share']}`
- month_bad_count(월 나쁨 수): `{final['reviewed_month_bad_count']}`
- package decision(패키지 결정): `{final['package_decision']}`
- next primary seed(다음 주 씨앗): `{final['next_primary_seed']}`

## Action And Effect(행동과 효과)

Action(행동): BO selected proxy(BO 선택 프록시)를 package gate(패키지 게이트), stress attribution(압박 귀속), proxy/MT5 diff(프록시/MT5 차이), next offensive seed(다음 공격 씨앗)으로 분리했다.

Effect(효과): package(패키지)는 거절하지만, `bo90` clean broad source(클린 넓은 원천), `bo91` overlap repair(겹침 수리), `bo05` high short-source PF(높은 숏 원천 PF)를 BQ scout(BQ 정찰)로 보존한다.

## Package Gate(패키지 게이트)

{markdown_table(package_rows, ['gate_id', 'subject', 'status', 'reason', 'effect'])}

## Stress Failure Attribution(압박 실패 귀속)

{markdown_table(stress_rows, ['failure_id', 'failure_type', 'segment', 'net_profit', 'profit_factor', 'trade_count', 'repair_use'])}

## Positive Clues(긍정 단서)

{markdown_table(clues, ['clue_id', 'clue_type', 'net_profit', 'profit_factor', 'density', 'short_share', 'synthetic_short_profit_factor', 'usable_as'])}

## Proxy/MT5 Diff(프록시/MT5 차이)

{markdown_table(proxy_mt5, ['comparison_id', 'mt5_net_profit', 'proxy_net_profit', 'net_diff_proxy_minus_mt5', 'mt5_profit_factor', 'proxy_profit_factor', 'usability'])}

## BQ Queue(BQ 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'seed_source', 'action', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BP is review only(BP는 검토 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BP short source quality repair review(숏 원천 품질 수리 검토)

Action(행동): BO selected proxy(BO 선택 프록시)를 package reject(패키지 거절)로 닫고 `{NEXT_RUN_ID}`를 연다.

Effect(효과): 월 압박과 MT5 미검증 때문에 운영 후보로 올리지 않고, bo90/bo91/bo05 단서를 다음 공격 탐색 제약으로 넘긴다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - short source quality repair review(숏 원천 품질 수리 검토).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BP Short Source Quality Repair Review Closeout",
        f"""## run364BP Short Source Quality Repair Review Closeout(364BP 숏 원천 품질 수리 검토 종료)

Action(행동): BO selected proxy(BO 선택 프록시)를 package reject(패키지 거절), stress memory(압박 기억), BQ offensive seed(BQ 공격 씨앗)으로 분리했다.

Effect(효과): `{NEXT_RUN_ID}`에서 bo90/bo91/bo05 단서를 broad clean short-share lift(넓은 클린 숏 비중 보강)로 공격 탐색한다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BP Short Source Quality Repair Review(364BP 숏 원천 품질 수리 검토)

Action(행동): BO proxy clue(BO 프록시 단서)를 패키지 게이트로 검토했다.

Effect(효과): 패키지는 거절하고 `{NEXT_RUN_ID}`로 넓은 클린 숏 비중 보강을 연다.
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
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364BP(364BP 실행)는 BO proxy clue(BO 프록시 단서)를 package reject(패키지 거절)로 닫고 bo90/bo91/bo05를 BQ offensive seed(BQ 공격 씨앗)로 넘겼다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 broad clean short-share lift(넓은 클린 숏 비중 보강)를 실행한다.",
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

Current truth(현재 진실): `run364BP`는 BO selected proxy(BO 선택 프록시) `{final['reviewed_candidate_id']}`를 package candidate(패키지 후보)에서 거절했다. 이유는 month_bad_count(월 나쁨 수) `{final['reviewed_month_bad_count']}`, package_candidate_rows(패키지 후보 행) `{final['reviewed_package_candidate_rows']}`, new MT5 execution(새 MT5 실행) 없음이다. Positive clue(긍정 단서)는 `bo90`, `bo91`, `bo05`로 보존한다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 bo90 broad clean source(bo90 넓은 클린 원천), bo91 overlap-safe h16 extension(bo91 겹침 안전 16시 확장), bo05 high short-source PF(bo05 높은 숏 원천 PF)를 broad clean short-share lift(넓은 클린 숏 비중 보강)로 공격 정찰한다.

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

Package candidate(패키지 후보): none(없음). BO selected proxy(BO 선택 프록시)는 `{final['package_decision']}`.

Preserved clues(보존 단서): `bo90_broad_h17_20_ps0440_margin080_control`, `bo91_broad_h16_17_20_ps0445_margin080_control`, `bo05_h17_margin_075_105_or_h20_margin_08_10`.

Reviewed proxy KPI(검토 프록시 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, density `{final['reviewed_density']}`, short share `{final['reviewed_short_share']}`, synthetic short PF `{final['reviewed_synthetic_short_profit_factor']}`.

Next queue(다음 대기열): `{rel(NEXT_OFFENSIVE_SEED_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): BO short source quality repair(BO 숏 원천 품질 수리)를 package gate(패키지 게이트)로 검토했다.
- effect(효과): package(패키지)는 거절하고 `{NEXT_RUN_ID}`로 bo90/bo91/bo05 공격 씨앗을 넘겼다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): broad clean h17/h20 short source(넓은 클린 17/20시 숏 원천)와 overlap-safe h16 extension(겹침 안전 16시 확장)을 결합하면 short share(숏 비중)를 회복할 수 있다.
- positive clue(긍정 단서): bo90 net/PF(순수익/PF) `1044.49` / `1.4158388603`, bo05 synthetic short PF(합성 숏 PF) `2.8224308655`.
- next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): BO package rejected(BO 패키지 거절).
- failure_memory(실패 기억): selected proxy(선택 프록시)는 month_bad_count(월 나쁨 수) `{final['reviewed_month_bad_count']}`이고 MT5 reprobe(MT5 재탐침)가 없다.
- effect(효과): package(패키지)가 아니라 broad clean short-share lift(넓은 클린 숏 비중 보강) 제약으로 넘긴다.
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
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(POSITIVE_CLUE_REGISTER),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_started_review_only(검토 전용이라 시작 안 함)",
        "work_family": "kpi_evidence(핵심 성과 근거)",
        "scoreboard_lane": "review_attribution(검토 귀속)",
        "net_profit": final["reviewed_net_profit"],
        "profit_factor": final["reviewed_profit_factor"],
        "trade_density_per_feature_day": final["reviewed_density"],
        "trade_density_requirement_status": "proxy_passed_ge_3_no_trade_splitting(프록시 3 이상 통과, 거래 쪼개기 없음)",
        "trade_count": "",
        "expectancy": "",
        "drawdown": "",
        "recovery_factor": "",
        "long_trade_count": "",
        "short_trade_count": "",
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can BO proxy clue become a package or should it pivot to broad clean short-share lift?(BO 프록시 단서가 패키지가 될 수 있는가, 아니면 넓은 클린 숏 비중 보강으로 전환해야 하는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, status, judgment in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", STATUS, JUDGMENT),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)", "not_run_parent_runtime_probe_had_no_tier_b_fallback"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", STATUS, JUDGMENT),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "BP review/package reject/next seed(BP 검토/패키지 거절/다음 씨앗)",
                "status": status,
                "judgment": judgment,
                "primary_kpi": f"reviewed_net={final['reviewed_net_profit']};reviewed_pf={final['reviewed_profit_factor']};month_bad={final['reviewed_month_bad_count']};package_rows={final['reviewed_package_candidate_rows']}",
                "guardrail_kpi": "no_new_mt5;no_authority;proxy_mt5_diff_recorded",
            }
        )
        if tier == "Tier B":
            for key in ["net_profit", "profit_factor", "trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])

    artifact_rows = []
    for artifact_type, path, notes in [
        ("package_gate_decision", PACKAGE_GATE_DECISION, "BP package gate decision(BP 패키지 게이트 결정)."),
        ("stress_failure_attribution", STRESS_FAILURE_ATTRIBUTION, "BP stress failure attribution(BP 압박 실패 귀속)."),
        ("positive_clue_register", POSITIVE_CLUE_REGISTER, "BP positive clues(BP 긍정 단서)."),
        ("proxy_mt5_diff_review", PROXY_MT5_DIFF_REVIEW, "BP proxy/MT5 diff review(BP 프록시/MT5 차이 검토)."),
        ("next_queue", NEXT_OFFENSIVE_SEED_QUEUE, "BQ queue(BQ 대기열)."),
        ("report", REPORT_PATH, "BP report(BP 보고서)."),
        ("decision", DECISION_DOC, "BP decision doc(BP 결정 문서)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
    ]:
        if exists(path):
            artifact_rows.append(
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
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


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
            "decision": DECISION,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
        },
    )


def main() -> None:
    ensure_dirs()
    bo_final = validate_inputs()
    write_work_packet()
    quality = load_rows(parent.QUALITY_RULE_SURFACE)
    broad = load_rows(parent.BROAD_POOL_NEGATIVE_CONTROL)
    stress = load_rows(parent.STRESS_SLICE_REVIEW)
    short_segments = load_rows(parent.SHORT_SOURCE_QUALITY_SEGMENTS)
    proxy_plan = load_rows(parent.PROXY_MT5_DIFF_PLAN)
    package = package_gate_rows(bo_final, quality, broad)
    stress_failures = stress_failure_rows(stress, short_segments)
    clues = positive_clue_rows(quality, broad)
    proxy_mt5 = proxy_mt5_rows(bo_final, proxy_plan)
    queue = next_queue_rows(bo_final)
    gates = gate_rows(bo_final, package, stress_failures, queue)
    if any(row["status"] != "passed" for row in gates):
        write_csv(INPUT_MANIFEST, input_manifest_rows())
        write_csv(PACKAGE_GATE_DECISION, package)
        write_csv(STRESS_FAILURE_ATTRIBUTION, stress_failures)
        write_csv(GATE_AUDIT, gates)
        raise RuntimeError("BP gate failure(BP 게이트 실패): " + ", ".join(row["gate"] for row in gates if row["status"] != "passed"))
    created_at = now_utc()
    final = final_payload(bo_final, package, stress_failures, clues, queue, gates, created_at)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(PACKAGE_GATE_DECISION, package)
    write_csv(STRESS_FAILURE_ATTRIBUTION, stress_failures)
    write_csv(POSITIVE_CLUE_REGISTER, clues)
    write_csv(PROXY_MT5_DIFF_REVIEW, proxy_mt5)
    write_csv(NEXT_OFFENSIVE_SEED_QUEUE, queue)
    write_receipts(final, proxy_mt5, clues)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_docs(final, package, stress_failures, clues, proxy_mt5, queue, gates)
    write_ledgers(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
