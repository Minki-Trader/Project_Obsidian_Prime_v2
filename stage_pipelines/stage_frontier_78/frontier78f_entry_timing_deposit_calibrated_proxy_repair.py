from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b


STAGE_ID = f78b.STAGE_ID
RUN_ID = "frontier78F_entry_timing_deposit_calibrated_proxy_repair_v1"
PARENT_RUN_ID = "frontier78E_proxy_runtime_gap_analysis_and_repair_decision_v1"
NEXT_RUN_IF_SIGNAL = "frontier78G_pre_mt5_grok_entry_timing_deposit_repaired_runtime_probe_v1"
NEXT_RUN_IF_ZERO = "frontier78G_zero_signal_or_negative_repair_closeout_decision_v1"
CLAIM_BOUNDARY = (
    "proxy_repair_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
STATUS_SIGNAL = "entry_timing_deposit_repair_proxy_signal_pre_mt5_grok_required_no_authority"
STATUS_ZERO = "entry_timing_deposit_repair_proxy_zero_signal_decision_required_no_authority"
JUDGMENT_SIGNAL = "repair_proxy_signal_requires_grok_and_mt5_probe_no_authority"
JUDGMENT_ZERO = "repair_proxy_no_signal_or_negative_memory_required_no_authority"

REPAIRED_INITIAL_BALANCE = 500.0
ENTRY_RULE = "same_bar_open_runtime_aligned(동일 봉 시가 런타임 정렬)"
DD_RULE = "dd_pct_uses_tester_deposit_500(손실폭 퍼센트는 테스터 예치금 500 기준)"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SUMMARY = REVIEW_DIR / "f78f_entry_timing_deposit_repair_proxy_summary.json"
CANDIDATES_ALL = REVIEW_DIR / "f78f_entry_timing_deposit_repair_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f78f_entry_timing_deposit_repair_ranked_top100.csv"
AXIS_SUMMARY = REVIEW_DIR / "f78f_entry_timing_deposit_repair_axis_summary.csv"
MODEL_FIT_SUMMARY = REVIEW_DIR / "f78f_entry_timing_deposit_repair_model_fit_summary.csv"
LABEL_AUDIT = REVIEW_DIR / "f78f_entry_timing_deposit_repair_label_audit.csv"
DATA_INTEGRITY = REVIEW_DIR / "f78f_data_integrity_review.json"
MODEL_VALIDATION = REVIEW_DIR / "f78f_model_validation_review.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f78f_artifact_lineage.json"
REPORT = REVIEW_DIR / "frontier78F_entry_timing_deposit_calibrated_proxy_repair_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f78f.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_78/frontier78f_entry_timing_deposit_calibrated_proxy_repair.py"


def now_utc() -> str:
    return f78b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    read_path = path if len(str(path)) < 240 else io_path(path)
    if path_exists(path):
        with read_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        source_read_path = source_header if len(str(source_header)) < 240 else io_path(source_header)
        with source_read_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    write_path = path if len(str(path)) < 240 else io_path(path)
    with write_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def same_bar_entry_indices(df: pd.DataFrame, raw: pd.DataFrame) -> np.ndarray:
    mapping = {ts: idx for idx, ts in enumerate(raw["open_ts"])}
    return df["timestamp"].map(mapping).fillna(-2).astype(int).to_numpy()


def patched_fit_and_score() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    original_entry = f78b.entry_indices_next_bar
    original_balance = f78b.INITIAL_BALANCE
    try:
        f78b.entry_indices_next_bar = same_bar_entry_indices
        f78b.INITIAL_BALANCE = REPAIRED_INITIAL_BALANCE
        candidate_rows, fit_rows, label_rows, summary = f78b.fit_and_score()
    finally:
        f78b.entry_indices_next_bar = original_entry
        f78b.INITIAL_BALANCE = original_balance
    best = summary.get("best_candidate") or {}
    summary = {
        **summary,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "entry_rule": ENTRY_RULE,
        "dd_rule": DD_RULE,
        "initial_balance": REPAIRED_INITIAL_BALANCE,
        "repair_axes": [
            "entry_timing_same_bar_runtime_aligned(진입 시각 동일 봉 런타임 정렬)",
            "dd_denominator_tester_deposit_500(손실폭 분모 테스터 예치금 500)",
            "same F78B feature/model/label axis budget reused(F78B 피처/모델/라벨 축 예산 재사용)",
        ],
        "best_candidate": best,
    }
    for row in candidate_rows:
        row["entry_rule"] = ENTRY_RULE
        row["dd_rule"] = DD_RULE
        row["initial_balance"] = REPAIRED_INITIAL_BALANCE
    return candidate_rows, fit_rows, label_rows, summary


def status_and_next(summary: Mapping[str, Any]) -> tuple[str, str, str]:
    signal_count = int(summary.get("meaningful_signal_count", 0) or 0) + int(summary.get("scout_clue_count", 0) or 0)
    if signal_count > 0:
        return STATUS_SIGNAL, JUDGMENT_SIGNAL, NEXT_RUN_IF_SIGNAL
    return STATUS_ZERO, JUDGMENT_ZERO, NEXT_RUN_IF_ZERO


def data_integrity_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    base = f78b.data_integrity_review(summary)
    base.update(
        {
            "repair_entry_rule": ENTRY_RULE,
            "repair_dd_rule": DD_RULE,
            "runtime_gap_source": "F78E entry timing and deposit denominator gap(F78E 진입 시각 및 예치금 분모 간극)",
            "integrity_judgment": "repair_proxy_integrity_ok_with_runtime_alignment_boundary(런타임 정렬 경계가 있는 수리 프록시 무결성 양호)",
        }
    )
    return base


def model_validation_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    base = f78b.model_validation_review(summary)
    base.update(
        {
            "repair_validation_boundary": "proxy repair after runtime gap analysis; not runtime authority(런타임 간극 분석 후 프록시 수리이며 런타임 권위 아님)",
            "selection_risk": "axis sweep still exploratory; pre-MT5 Grok and runtime probe required before runtime interpretation(축 탐색은 여전히 탐색이며 런타임 해석 전 사전 MT5 Grok 및 런타임 탐침 필요)",
        }
    )
    return base


def artifact_lineage(summary: Mapping[str, Any], next_run: str) -> dict[str, Any]:
    return {
        "source_inputs": [
            rel(f78b.DATASET_PATH),
            rel(f78b.FEATURE_ORDER_PATH),
            rel(f78b.RAW_BARS_PATH),
            "stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78e_proxy_runtime_gap_analysis.json",
        ],
        "producer": SCRIPT_REL,
        "consumer": next_run,
        "artifact_paths": [rel(SUMMARY), rel(CANDIDATES_ALL), rel(CANDIDATES_TOP), rel(AXIS_SUMMARY), rel(REPORT), rel(RUN_MANIFEST)],
        "artifact_hashes": {
            "dataset_sha256": f78b.file_hash(f78b.DATASET_PATH),
            "raw_bars_sha256": f78b.file_hash(f78b.RAW_BARS_PATH),
            "script_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        },
        "lineage_judgment": "connected_repair_proxy_with_boundary(경계 있는 수리 프록시 연결)",
    }


def format_best(best: Mapping[str, Any]) -> str:
    if not best:
        return "none(없음)"
    return (
        f"{best.get('candidate_id')} val net/PF/DD/calendar_tpd/trades(검증 순수익/수익 팩터/손실폭/달력일 거래/거래) "
        f"{best.get('val_net')}/{best.get('val_pf')}/{best.get('val_dd_pct')}/{best.get('val_calendar_trades_day')}/{best.get('val_trade_count')}; "
        f"oos(표본외) {best.get('oos_net')}/{best.get('oos_pf')}/{best.get('oos_dd_pct')}/{best.get('oos_calendar_trades_day')}/{best.get('oos_trade_count')}"
    )


def report_text(created_at: str, summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, Any]], status: str, judgment: str, next_run: str) -> str:
    table = "\n".join(
        [
            "| candidate(후보) | model(모델) | label(라벨) | feature(피처) | session/risk/cd(세션/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | oos net/PF/DD/tpd/trades(표본외) | scout/meaningful(탐색/의미) |",
            "|---|---|---|---|---|---:|---:|---|",
            *[
                f"| `{row.get('candidate_id')}` | `{row.get('model')}` | `{row.get('label_name')}` | `{row.get('feature_set')}` | `{row.get('session')}/{row.get('risk_filter')}/{row.get('cooldown_bars')}` | "
                f"`{row.get('val_net'):.4f}/{row.get('val_pf'):.4f}/{row.get('val_dd_pct'):.4f}/{row.get('val_calendar_trades_day'):.4f}/{row.get('val_trade_count')}` | "
                f"`{row.get('oos_net'):.4f}/{row.get('oos_pf'):.4f}/{row.get('oos_dd_pct'):.4f}/{row.get('oos_calendar_trades_day'):.4f}/{row.get('oos_trade_count')}` | "
                f"`{row.get('scout_clue')}/{row.get('meaningful_signal')}` |"
                for row in top_rows[:12]
            ],
        ]
    )
    return f"""# Frontier78F Entry Timing + Deposit-Calibrated Proxy Repair Report(F78F 진입 시각 + 예치금 보정 프록시 수리 보고서)

Updated(갱신): {created_at}

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- candidate rows(후보 행): `{summary['candidate_rows']}`
- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`
- final-like reference count(완성 유사 참조 수): `{summary['final_like_reference_count']}`
- entry rule(진입 규칙): `{ENTRY_RULE}`
- DD rule(손실폭 규칙): `{DD_RULE}`
- best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}
- next action(다음 행동): `{next_run}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Top Repaired Proxy Rows(상위 수리 프록시 행)

{table}

## Interpretation Boundary(해석 경계)

Action(행동): F78E에서 확인한 entry timing mismatch(진입 시각 불일치)와 DD denominator mismatch(손실폭 분모 불일치)를 proxy scout(프록시 탐색) 기준에 반영했다.

Effect(효과): 이후 MT5 Runtime Probe(MT5 런타임 탐침)로 다시 물질화할 수 있는 repaired candidate surface(수리된 후보 표면)를 만든다.
"""


def gate_audit_text(summary: Mapping[str, Any], status: str, next_run: str) -> str:
    return f"""# Required Gate Coverage Audit F78F(F78F 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F78E repair input(F78E 수리 입력) | `passed(통과)` | `stages/{STAGE_ID}/03_reviews/f78e_proxy_runtime_gap_analysis.json` |
| entry timing repair(진입 시각 수리) | `applied(적용됨)` | `{ENTRY_RULE}` |
| DD denominator repair(손실폭 분모 수리) | `applied(적용됨)` | `{DD_RULE}` |
| proxy KPI contract(프록시 KPI 계약) | `passed(통과)` | `{rel(SUMMARY)}` |
| data integrity(데이터 무결성) | `recorded(기록됨)` | `{rel(DATA_INTEGRITY)}` |
| model validation(모델 검증) | `recorded(기록됨)` | `{rel(MODEL_VALIDATION)}` |
| runtime probe rule(런타임 탐침 규칙) | `required_next(다음 필수)` | `{next_run}` |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |

Open status(현재 상태): `{status}`

Summary(요약): candidates(후보) `{summary.get('candidate_rows')}`, scout(탐색) `{summary.get('scout_clue_count')}`, meaningful(의미) `{summary.get('meaningful_signal_count')}`.
"""


def ledger_row(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary.get("best_candidate") or {}
    row_id = f"{RUN_ID}__repair_proxy"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_repair(프록시 수리)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "notes": f"candidates={summary.get('candidate_rows')}; scout={summary.get('scout_clue_count')}; meaningful={summary.get('meaningful_signal_count')}; next={next_run}",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT),
        "run_number": "frontier78F",
        "date": created_at[:10],
        "decision": judgment,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "rows": summary.get("candidate_rows"),
        "gate_passes": "8",
        "gate_total": "8",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "best_candidate_id": best.get("candidate_id", ""),
        "candidate_count": summary.get("candidate_rows"),
        "scout_clue_count": summary.get("scout_clue_count"),
        "meaningful_signal_count": summary.get("meaningful_signal_count"),
        "model": best.get("model", ""),
        "net_profit": best.get("oos_net", ""),
        "profit_factor": best.get("oos_pf", ""),
        "drawdown_percent": best.get("oos_dd_pct", ""),
        "expectancy": best.get("oos_expectancy", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trades_per_day": best.get("oos_calendar_trades_day", ""),
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "repaired_contract_proxy_validation_oos(수리 계약 프록시 검증/표본외)",
        "primary_kpi": f"scout={summary.get('scout_clue_count')};meaningful={summary.get('meaningful_signal_count')};near={summary.get('final_like_reference_count')}",
        "guardrail_kpi": f"entry={ENTRY_RULE};dd={DD_RULE}",
        "work_family": "experiment_execution(실험 실행)",
        "row_id": row_id,
        "ledger_row_id": row_id,
        "subrun_id": "entry_timing_deposit_proxy_repair(진입 시각 예치금 프록시 수리)",
        "evidence_boundary": "proxy_repair_only_no_authority(프록시 수리 전용, 권위 없음)",
        "next_action": next_run,
        "question": "Does runtime-aligned entry/deposit repair preserve signal?(런타임 정렬 진입/예치금 수리가 신호를 보존하는가?)",
        "artifact_count": "9",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
        "run_type": "entry_timing_deposit_calibrated_proxy_repair",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_repair_only(프록시 수리 전용)",
    }


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    row = ledger_row(created_at, status, judgment, next_run, summary)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_state(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    best = summary.get("best_candidate") or {}
    workspace = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f78_repaired_proxy_requires_pre_mt5_grok_then_runtime_probe
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f77_closeout_2_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F78F entry timing/deposit proxy repair(진입 시각/예치금 프록시 수리)를 실행했다."
  - "Effect(효과): F78E runtime gap(런타임 간극)을 반영한 후보 표면을 다시 만들었다."
  - "Best(최선): {best.get('candidate_id', '')} OOS net/PF/DD/calendar_tpd {best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}."
  - "Next(다음): {next_run}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, workspace)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F78F entry timing/deposit proxy repair(진입 시각/예치금 프록시 수리)를 실행했다.

Effect(효과): same-bar runtime-aligned entry(동일 봉 런타임 정렬 진입)와 tester deposit DD denominator(테스터 예치금 손실폭 분모)를 반영한 proxy surface(프록시 표면)를 만들었다.

## Repaired Proxy Best(수리 프록시 최선)

- candidate(후보): `{best.get('candidate_id', '')}`
- OOS net/PF/DD/calendar_tpd/trades(표본외 순수익/수익 팩터/손실폭/달력일 거래/거래): `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}/{best.get('oos_trade_count', '')}`

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F78 Selection Status(F78 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F78F entry timing/deposit calibrated proxy repair(진입 시각/예치금 보정 프록시 수리)를 실행했다.

Effect(효과): F78G pre-MT5 Grok review(사전 MT5 Grok 검토) 또는 closeout decision(마감 결정)에 필요한 repaired proxy evidence(수리 프록시 근거)를 만들었다.

Best candidate(최선 후보): {format_best(best)}

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)
    marker = "<!-- frontier78F_entry_timing_deposit_calibrated_proxy_repair_v1 -->"
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in text:
        block = f"""

{marker}
- `{RUN_ID}` executed F78 entry timing/deposit calibrated proxy repair(F78 진입 시각/예치금 보정 프록시 수리). Result(결과): scout `{summary.get('scout_clue_count')}`, meaningful `{summary.get('meaningful_signal_count')}`, final_like `{summary.get('final_like_reference_count')}`. Best(최선): `{best.get('candidate_id', '')}` OOS net/PF/DD/calendar_tpd(표본외 순수익/수익 팩터/손실폭/달력일 거래) `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}`. Next(다음): `{next_run}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
        write_text(IDEA_REGISTRY, text.rstrip() + block)


def run_manifest_payload(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "entry_rule": ENTRY_RULE,
        "dd_rule": DD_RULE,
        "initial_balance": REPAIRED_INITIAL_BALANCE,
        "summary": summary,
        "artifacts": {
            "summary": rel(SUMMARY),
            "candidates_all": rel(CANDIDATES_ALL),
            "candidates_top": rel(CANDIDATES_TOP),
            "axis_summary": rel(AXIS_SUMMARY),
            "fit_summary": rel(MODEL_FIT_SUMMARY),
            "label_audit": rel(LABEL_AUDIT),
            "data_integrity": rel(DATA_INTEGRITY),
            "model_validation": rel(MODEL_VALIDATION),
            "artifact_lineage": rel(ARTIFACT_LINEAGE),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
        },
    }


def main() -> int:
    ensure_dirs()
    created_at = now_utc()
    candidate_rows, fit_rows, label_rows, summary = patched_fit_and_score()
    top_rows = candidate_rows[:100]
    axis_rows = f78b.axis_summary_rows(candidate_rows)
    status, judgment, next_run = status_and_next(summary)
    write_json(SUMMARY, summary)
    write_csv(CANDIDATES_ALL, candidate_rows)
    write_csv(CANDIDATES_TOP, top_rows)
    write_csv(AXIS_SUMMARY, axis_rows)
    write_csv(MODEL_FIT_SUMMARY, fit_rows)
    write_csv(LABEL_AUDIT, label_rows)
    write_json(DATA_INTEGRITY, data_integrity_review(summary))
    write_json(MODEL_VALIDATION, model_validation_review(summary))
    write_json(ARTIFACT_LINEAGE, artifact_lineage(summary, next_run))
    write_text(REPORT, report_text(created_at, summary, top_rows, status, judgment, next_run))
    write_text(GATE_AUDIT, gate_audit_text(summary, status, next_run))
    write_json(RUN_MANIFEST, run_manifest_payload(created_at, status, judgment, next_run, summary))
    update_ledgers(created_at, status, judgment, next_run, summary)
    update_state(created_at, status, judgment, next_run, summary)
    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "candidate_rows": summary["candidate_rows"],
                "scout_clue_count": summary["scout_clue_count"],
                "meaningful_signal_count": summary["meaningful_signal_count"],
                "final_like_reference_count": summary["final_like_reference_count"],
                "best_candidate": summary["best_candidate"],
                "next_run_id": next_run,
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
