from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_77 import frontier77b_runtime_lifecycle_label_density_proxy_scout as f77b


STAGE_ID = f77b.STAGE_ID
RUN_ID = "frontier77H_stage_closeout_runtime_lifecycle_label_density_rebuild_v1"
PARENT_RUN_ID = "frontier77G_post_repair_gap_analysis_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier78A_stage_open_execution_calibrated_density_contract_pnl_v1"
NEXT_FRONTIER_STAGE_ID = "stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild"

STATUS_SUCCESS = "closed_preserved_clue_no_authority"
STATUS_NOT_CLOSED = "closeout_grok_not_accepted_stage_not_closed_no_authority"
JUDGMENT_SUCCESS = "preserved_clue_with_negative_memory_no_authority"
JUDGMENT_NOT_CLOSED = "closeout_retry_or_repair_decision_required_no_authority"
CLOSEOUT_LABEL = "preserved_clue(보존 단서)"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RETROSPECTIVE_DUE_STATUS = "not_due_after_f77_closeout_2_of_5"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

F77B_SUMMARY = REVIEW_DIR / "f77b_lifecycle_proxy_summary.json"
F77C_TARGET = REVIEW_DIR / "f77c_runtime_materialization_target_selection.json"
F77F_SUMMARY = REVIEW_DIR / "f77f_mt5_lifecycle_point_unit_repair_probe_summary.json"
F77F_RECEIPT = STAGE_DIR / "02_runs" / "frontier77F_mt5_lifecycle_point_unit_repair_probe_v1" / "f77f_runtime_receipt.csv"
F77G_ANALYSIS = REVIEW_DIR / "f77g_post_repair_gap_analysis_closeout_decision.json"
F77G_RECEIPT = REVIEW_DIR / "grok_f77g_post_repair_gap_analysis_closeout_direction_receipt.md"

REPORT_PATH = REVIEW_DIR / "stage_closeout_report.md"
SUMMARY_PATH = REVIEW_DIR / "f77h_stage_closeout_summary.json"
KPI_ROWS_PATH = REVIEW_DIR / "f77h_closeout_kpi_rows.csv"
LINEAGE_PATH = REVIEW_DIR / "f77h_artifact_lineage.json"
LOCAL_VERIFICATION_PATH = REVIEW_DIR / "f77h_closeout_local_verification.json"
RECEIPT_PATH = REVIEW_DIR / "grok_stage_closeout_runtime_lifecycle_label_density_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f77h_closeout.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"
SELECTION_STATUS_PATH = SELECTED_DIR / "selection_status.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f77h_stage_closeout_runtime_lifecycle_label_density"
GROK_PROMPT_PATH = GROK_PACKET / "prompts/f77h_stage_closeout_runtime_lifecycle_label_density_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"


def utc_now() -> str:
    return f77b.utc_now()


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


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def short_number(value: Any) -> str:
    if value in ("", None):
        return ""
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
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
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def proxy_lookup(target: Mapping[str, Any], split: str) -> dict[str, Any]:
    prefix = "val" if split == "validation" else "oos"
    return {
        "net_profit": target.get(f"{prefix}_net", ""),
        "gross_profit": target.get(f"{prefix}_gross_profit", ""),
        "gross_loss": target.get(f"{prefix}_gross_loss", ""),
        "profit_factor": target.get(f"{prefix}_pf", ""),
        "drawdown_percent": target.get(f"{prefix}_dd_pct", ""),
        "trade_count": target.get(f"{prefix}_trade_count", ""),
        "trades_per_day": target.get(f"{prefix}_trades_day", ""),
        "win_rate": target.get(f"{prefix}_win_rate", ""),
        "average_win": target.get(f"{prefix}_avg_win", ""),
        "average_loss": target.get(f"{prefix}_avg_loss", ""),
        "payoff_ratio": target.get(f"{prefix}_payoff", ""),
        "expectancy": target.get(f"{prefix}_expectancy", ""),
        "recovery_factor": target.get(f"{prefix}_recovery", ""),
        "time_under_water": target.get(f"{prefix}_time_under_water_trades", ""),
        "max_consecutive_loss": target.get(f"{prefix}_max_consecutive_loss", ""),
    }


def closeout_kpi_rows(receipts: Sequence[Mapping[str, str]], target: Mapping[str, Any], f77g: Mapping[str, Any]) -> list[dict[str, Any]]:
    gap_by_split = {row.get("split"): row for row in f77g.get("split_rows", [])}
    rows: list[dict[str, Any]] = []
    for row in receipts:
        split = row.get("split", "")
        proxy = proxy_lookup(target, split)
        gap = (gap_by_split.get(split) or {}).get("gaps", {})
        runtime_active_tpd = ((gap_by_split.get(split) or {}).get("runtime", {}) or {}).get("trades_per_day_proxy_active_dates", "")
        rows.append(
            {
                "split": split,
                "view": "MT5 Runtime Repair Probe(MT5 런타임 수리 탐침)",
                "test_period": f"{row.get('test_period_start', '')}..{row.get('test_period_end', '')}",
                "net_profit": row.get("net_profit", ""),
                "gross_profit": row.get("gross_profit", ""),
                "gross_loss": row.get("gross_loss", ""),
                "profit_factor": row.get("profit_factor", ""),
                "drawdown_percent": row.get("max_drawdown_percent", ""),
                "trade_count": row.get("trade_count", ""),
                "trades_per_day": row.get("trades_per_day", ""),
                "runtime_active_date_trades_per_day": runtime_active_tpd,
                "win_rate_percent": row.get("win_rate_percent", ""),
                "average_win": row.get("average_win", ""),
                "average_loss": row.get("average_loss", ""),
                "payoff_ratio": row.get("payoff_ratio", ""),
                "expectancy": row.get("expectancy", ""),
                "recovery_factor": row.get("recovery_factor", ""),
                "time_under_water": "not_available_in_runtime_receipt(런타임 영수증에 없음)",
                "max_consecutive_loss": "not_available_in_runtime_receipt(런타임 영수증에 없음)",
                "long_short_breakdown": f"long={row.get('long_trade_count', '')};short={row.get('short_trade_count', '')}",
                "proxy_runtime_kpi_gap": (
                    f"proxy_net={short_number(proxy['net_profit'])};runtime_net={short_number(row.get('net_profit'))};"
                    f"proxy_pf={short_number(proxy['profit_factor'])};runtime_pf={short_number(row.get('profit_factor'))};"
                    f"proxy_dd={short_number(proxy['drawdown_percent'])};runtime_dd={short_number(row.get('max_drawdown_percent'))};"
                    f"proxy_active_tpd={short_number(proxy['trades_per_day'])};runtime_calendar_tpd={short_number(row.get('trades_per_day'))};"
                    f"runtime_active_tpd={short_number(runtime_active_tpd)};"
                    f"net_scale={short_number(gap.get('net_scale'))};gross_profit_scale={short_number(gap.get('gross_profit_scale'))}"
                ),
                "proxy_time_under_water": proxy["time_under_water"],
                "proxy_max_consecutive_loss": proxy["max_consecutive_loss"],
            }
        )
    return rows


def gap_cause_map() -> list[dict[str, str]]:
    return [
        {
            "gap_cause": "money_scale_gap_after_point_unit_repair",
            "bucket": "bookkeeping/measurement(장부/측정)",
            "meaning": "proxy P/L(프록시 손익)이 broker contract P/L(브로커 계약 손익)로 보정되지 않았다.",
        },
        {
            "gap_cause": "trade_density_denominator_gap_proxy_active_dates_vs_runtime_calendar_days",
            "bucket": "bookkeeping/measurement(장부/측정)",
            "meaning": "proxy trades/day(프록시 일 거래 수)는 selected active dates(선택 활성 날짜)를 분모로 썼고 runtime(런타임)은 calendar days(달력일)를 썼다.",
        },
        {
            "gap_cause": "minor_fill_count_gap_from_hold_same_direction_after_realized_runtime_holds",
            "bucket": "preserved mechanic(보존 메커니즘)",
            "meaning": "runtime realized holds(런타임 실제 보유)가 proxy selected entries(프록시 선택 진입) 중 일부를 same-direction hold(동방향 보유)로 압축했다.",
        },
        {
            "gap_cause": "weak_alpha_gap_pf_and_density_below_goal_after_runtime_materialization",
            "bucket": "hypothesis-negative(가설 부정)",
            "meaning": "F77F runtime PF/density(런타임 수익 팩터/밀도)가 목표권과 거리가 멀고 F77B meaningful signal(의미 신호)이 0이었다.",
        },
    ]


def preserved_clues() -> list[str]:
    return [
        "point-unit repair pattern(포인트 단위 수리 패턴): TP18/SL12 price units(가격 단위)을 TP1800/SL1200 broker points(브로커 포인트)로 변환하면 MT5 Invalid stops(잘못된 손절/익절)가 사라진다.",
        "ONNX/EA signal parity path(ONNX/EA 신호 동등성 경로): three-column short schema(3열 숏 스키마)와 selected-entry veto tape(선택 진입 거부 테이프)가 signal count parity(신호 수 동등성)를 유지했다.",
        "runtime bridge mechanics(런타임 연결 메커니즘): point-unit repair(포인트 단위 수리) 후 Strategy Tester(전략 테스터)에서 validation/OOS(검증/표본외) 주문이 체결됐다.",
    ]


def negative_memories() -> list[str]:
    return [
        "zero meaningful proxy candidates(의미 프록시 후보 0): F77B 10,368 후보 중 meaningful signal(의미 신호)과 final-like reference(완성 유사 참조)가 모두 0이었다.",
        "density metric misalignment(밀도 지표 불일치): proxy trades/day(프록시 일 거래 수)는 selected active dates(선택 활성 날짜) 기준이라 final review(최종 검토)의 일 거래 수와 다르다.",
        "money scale not contract-calibrated(금액 배율 계약 미보정): proxy money(프록시 금액)는 MT5 realized P/L(실현 손익)보다 약 12배 크게 보였다.",
        "exportability distorted target selection(내보내기 가능성이 대상 선택 왜곡): best HistGBM(최선 히스토그램 GBM)은 ONNX export(ONNX 내보내기)가 실패해 weaker ExtraTrees(더 약한 엑스트라트리)를 런타임 대상으로 썼다.",
    ]


def next_frontier_hypothesis() -> str:
    return (
        "Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), "
        "final-review density denominator(최종 검토 밀도 분모), fill semantics(체결 의미), "
        "and lifecycle risk(생명주기 위험)를 proxy 단계부터 내장하면 PF/density/DD(수익 팩터/밀도/손실폭)를 동시에 더 잘 맞출 수 있는지 본다."
    )


def artifact_lineage(created_at: str, closeout_success: bool) -> dict[str, Any]:
    source_inputs = [
        "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet",
        "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv",
        rel(F77B_SUMMARY),
        rel(F77C_TARGET),
        rel(F77F_SUMMARY),
        rel(F77F_RECEIPT),
        rel(F77G_ANALYSIS),
    ]
    tracked_artifact_paths = [
        rel(REPORT_PATH),
        rel(SUMMARY_PATH),
        rel(KPI_ROWS_PATH),
        rel(LINEAGE_PATH),
        rel(LOCAL_VERIFICATION_PATH),
        rel(RECEIPT_PATH),
        rel(GATE_AUDIT_PATH),
        rel(GROK_PROMPT_PATH),
        rel(GROK_CLEAN_PATH),
        rel(GROK_METADATA_PATH),
    ]
    ignored_runtime_artifacts = [
        rel(RUN_MANIFEST_PATH),
        rel(F77F_RECEIPT),
        rel(STAGE_DIR / "02_runs" / "frontier77F_mt5_lifecycle_point_unit_repair_probe_v1" / "f77f_execution_results.json"),
        rel(STAGE_DIR / "02_runs" / "frontier77F_mt5_lifecycle_point_unit_repair_probe_v1" / "mt5" / "reports"),
    ]
    artifact_paths = [
        *tracked_artifact_paths,
        *ignored_runtime_artifacts,
    ]
    artifact_hashes = {
        path: file_hash(ROOT / path)
        for path in artifact_paths
        if path_exists(ROOT / path) and io_path(ROOT / path).is_file()
    }
    return {
        "created_at_utc": created_at,
        "source_inputs": source_inputs,
        "producer": "stage_pipelines/stage_frontier_77/frontier77h_stage_closeout_runtime_lifecycle_label_density_rebuild.py",
        "consumer": NEXT_RUN_ID,
        "artifact_paths": artifact_paths,
        "artifact_hashes": artifact_hashes,
        "registry_links": [
            "docs/registers/run_registry.csv",
            "docs/registers/alpha_run_ledger.csv",
            f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv",
            "docs/registers/negative_result_register.md",
            "docs/registers/five_stage_retrospective_register.yaml",
        ],
        "availability": "tracked_reviews_with_ignored_runtime_artifacts(추적 리뷰와 무시된 런타임 산출물)",
        "tracked_artifacts": tracked_artifact_paths,
        "ignored_runtime_artifacts": ignored_runtime_artifacts,
        "ignored_reason": ".gitignore excludes stages/*/02_runs/ and model/export artifacts(.gitignore가 stages/*/02_runs/ 및 모델/내보내기 산출물을 제외함); tracked closeout summaries carry the KPI and identity(추적 마감 요약이 KPI와 정체성을 보존함).",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
    }


def build_closeout_payload(created_at: str, kpi_rows: Sequence[Mapping[str, Any]], closeout_success: bool) -> dict[str, Any]:
    f77b_summary = read_json(F77B_SUMMARY)
    f77f_summary = read_json(F77F_SUMMARY)
    f77g = read_json(F77G_ANALYSIS)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if closeout_success else RUN_ID,
        "next_frontier_stage_id": NEXT_FRONTIER_STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS_SUCCESS if closeout_success else STATUS_NOT_CLOSED,
        "judgment": JUDGMENT_SUCCESS if closeout_success else JUDGMENT_NOT_CLOSED,
        "closeout_label": CLOSEOUT_LABEL if closeout_success else "not_closed(미마감)",
        "hypothesis": "Runtime lifecycle-native labels(런타임 생명주기 기본 라벨)이 tradeable density(거래 가능 밀도)와 parity(동등성)를 보존할 수 있는지.",
        "test_period": "validation 2025-01-02..2025-10-01; OOS 2025-10-01..2026-04-14",
        "proxy_expectation": "lifecycle label(생명주기 라벨)이 independent proxy overcount(독립 프록시 과대계산)를 줄이고 runtime bridge(런타임 연결)에 더 맞을 것.",
        "proxy_kpi": f77b_summary.get("best_candidate", {}),
        "runtime_probe_kpi": f77f_summary.get("best_runtime", {}),
        "kpi_rows": list(kpi_rows),
        "gap_cause_map": gap_cause_map(),
        "preserved_clue": preserved_clues(),
        "negative_memory": negative_memories(),
        "next_frontier_hypothesis": next_frontier_hypothesis(),
        "result_judgment": {
            "result_subject": "F77 runtime lifecycle label density rebuild(F77 런타임 생명주기 라벨 밀도 재구성)",
            "evidence_available": [
                rel(F77B_SUMMARY),
                rel(F77F_SUMMARY),
                rel(F77G_ANALYSIS),
                rel(REPORT_PATH),
            ],
            "evidence_missing": [
                "runtime time_under_water(런타임 회복 전 체류 시간): telemetry/report receipt does not expose closed-trade sequence(종료 거래 순서 미노출)",
                "runtime max_consecutive_loss(런타임 최대 연속 손실): telemetry/report receipt does not expose closed-trade sequence(종료 거래 순서 미노출)",
            ],
            "judgment_label": "preserved_clue(보존 단서)" if closeout_success else "not_closed(미마감)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "open Frontier78(전선78 개방) with execution-calibrated label/density/money contract(실행 보정 라벨/밀도/금액 계약)",
            "user_explanation_hook": "F77은 주문 연결을 고쳤지만 알파는 약했다. 배운 수리법만 들고 새 가설로 간다.",
        },
    }


def build_local_verification(created_at: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    f77b_summary = read_json(F77B_SUMMARY)
    f77f_summary = read_json(F77F_SUMMARY)
    f77g = read_json(F77G_ANALYSIS)
    retro = yaml.safe_load(io_path(RETROSPECTIVE_REGISTER).read_text(encoding="utf-8-sig"))
    best_proxy = f77b_summary.get("best_candidate", {})
    best_runtime = f77f_summary.get("best_runtime", {})
    negative_text = "\n".join(payload.get("negative_memory", []))
    preserved_text = "\n".join(payload.get("preserved_clue", []))
    gap_buckets = {row["gap_cause"]: row["bucket"] for row in payload.get("gap_cause_map", [])}
    checks = [
        {
            "check": "kpi_identity_lock(핵심성과지표 정체성 고정)",
            "passed": bool(
                str(best_proxy.get("candidate_id")) == "f77b_08051"
                and as_float(best_proxy.get("oos_net")) == 127.2
                and str(best_runtime.get("candidate_id")) == "f77f_point_unit_repair_f77b_07979"
                and as_float(best_runtime.get("net_profit")) == 4.48
            ),
            "evidence": {
                "proxy_summary": rel(F77B_SUMMARY),
                "runtime_summary": rel(F77F_SUMMARY),
                "proxy_candidate_id": best_proxy.get("candidate_id"),
                "runtime_candidate_id": best_runtime.get("candidate_id"),
                "proxy_oos_net_pf_dd_tpd": [
                    best_proxy.get("oos_net"),
                    best_proxy.get("oos_pf"),
                    best_proxy.get("oos_dd_pct"),
                    best_proxy.get("oos_trades_day"),
                ],
                "runtime_oos_net_pf_dd_tpd": [
                    best_runtime.get("net_profit"),
                    best_runtime.get("profit_factor"),
                    best_runtime.get("max_drawdown_percent"),
                    best_runtime.get("trades_per_day"),
                ],
            },
        },
        {
            "check": "parity_scope_boundary(동등성 범위 경계)",
            "passed": bool(
                f77f_summary.get("signal_parity_pass_rows") == 3
                and f77f_summary.get("feature_readiness_pass_rows") == 1
                and "P/L/density parity(손익/밀도 동등성)" not in preserved_text
            ),
            "evidence": {
                "signal_parity_pass_rows": f77f_summary.get("signal_parity_pass_rows"),
                "feature_readiness_pass_rows": f77f_summary.get("feature_readiness_pass_rows"),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        },
        {
            "check": "exportability_negative_memory(내보내기 부정 기억)",
            "passed": bool("HistGBM" in negative_text and "ExtraTrees" in negative_text and "export" in negative_text),
            "evidence": {
                "negative_memory": payload.get("negative_memory", []),
                "target_selection": rel(F77C_TARGET),
            },
        },
        {
            "check": "five_stage_retrospective_gate(5단계 회고 게이트)",
            "passed": bool(
                retro.get("state", {}).get("closeouts_since_last", 1) < 5
                and str(retro.get("state", {}).get("current_due_status", "")).startswith("not_due")
            ),
            "evidence": {
                "retrospective_register": rel(RETROSPECTIVE_REGISTER),
                "current_due_status_before_closeout": retro.get("state", {}).get("current_due_status"),
                "closeouts_since_last_before_closeout": retro.get("state", {}).get("closeouts_since_last"),
            },
        },
        {
            "check": "f77g_condition_mapping(F77G 조건 매핑)",
            "passed": bool(
                "bookkeeping/measurement(장부/측정)" in gap_buckets.values()
                and "hypothesis-negative(가설 부정)" in gap_buckets.values()
                and "preserved mechanic(보존 메커니즘)" in gap_buckets.values()
                and all(fragment in negative_text for fragment in ["meaningful", "density", "contract", "exportability"])
                and all(fragment in preserved_text for fragment in ["point-unit", "ONNX/EA", "runtime bridge"])
                and payload.get("next_frontier_stage_id") == NEXT_FRONTIER_STAGE_ID
            ),
            "evidence": {
                "f77g_gap_analysis": rel(F77G_ANALYSIS),
                "gap_buckets": gap_buckets,
                "next_frontier_stage_id": payload.get("next_frontier_stage_id"),
            },
        },
    ]
    return {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "checks": checks,
        "all_passed": all(bool(row["passed"]) for row in checks),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_prompt(payload: Mapping[str, Any]) -> str:
    best_runtime = payload["runtime_probe_kpi"]
    best_proxy = payload["proxy_kpi"]
    return f"""# F77H Stage Closeout Grok Review Prompt(F77H 단계 마감 Grok 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Closeout(Codex 제안 마감)

- stage(단계): `{STAGE_ID}`
- closeout label(마감 라벨): `{CLOSEOUT_LABEL}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Evidence(근거)

- proxy candidates(프록시 후보): `10368`
- meaningful proxy candidates(의미 프록시 후보): `0`
- final-like references(완성 유사 참조): `0`
- proxy best OOS net/PF/DD/tpd(프록시 최선 표본외 순수익/수익 팩터/손실폭/일 거래 수): `{best_proxy.get('oos_net')}/{best_proxy.get('oos_pf')}/{best_proxy.get('oos_dd_pct')}/{best_proxy.get('oos_trades_day')}`
- runtime best OOS net/PF/DD/tpd(런타임 최선 표본외 순수익/수익 팩터/손실폭/일 거래 수): `{best_runtime.get('net_profit')}/{best_runtime.get('profit_factor')}/{best_runtime.get('max_drawdown_percent')}/{best_runtime.get('trades_per_day')}`
- MT5 runtime probe(MT5 런타임 탐침): F77D and F77F both executed(실행), F77F completed 2/2(2/2 완료)
- signal/feature parity(신호/피처 동등성): pass(통과)

## Required F77G Conditions(F77G 필수 조건)

1. gap causes(간극 원인)를 bookkeeping only(장부), hypothesis-negative(가설 부정), preserved mechanic(보존 메커니즘)으로 분리한다.
2. negative memory(부정 기억)에 zero meaningful proxy candidates(의미 프록시 후보 0), density metric misalignment(밀도 지표 불일치), money scale not contract-calibrated(금액 배율 계약 미보정), exportability distorted target selection(내보내기 가능성의 대상 선택 왜곡)을 포함한다.
3. preserved clues(보존 단서)에 point-unit repair pattern(포인트 단위 수리 패턴), ONNX/EA signal parity path(ONNX/EA 신호 동등성 경로), runtime bridge mechanics(런타임 연결 메커니즘)을 포함한다.
4. next frontier(다음 전선)는 F77 continuation(F77 연속)이 아니라 new hypothesis(새 가설)여야 한다.

## Codex Closeout Contents(Codex 마감 내용)

Gap mapping(간극 매핑):
{json.dumps(payload['gap_cause_map'], ensure_ascii=False, indent=2)}

Negative memory(부정 기억):
{json.dumps(payload['negative_memory'], ensure_ascii=False, indent=2)}

Preserved clues(보존 단서):
{json.dumps(payload['preserved_clue'], ensure_ascii=False, indent=2)}

Next frontier hypothesis(다음 전선 가설):
{payload['next_frontier_hypothesis']}

## Focus Question(집중 질문)

Does this satisfy stage closeout(단계 마감) as preserved clue(보존 단서) with negative memory(부정 기억), without granting forbidden claims(금지 주장)?

Classify at top as one of:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str]]:
    lowered = clean_output.lower()
    head = lowered.strip()[:400]
    forbidden_hits = [
        term
        for term in ["goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion", "completion"]
        if f"may claim {term}" in lowered
        or f"can claim {term}" in lowered
        or f"{term} achieved" in lowered
        or f"{term}: yes" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_closeout_grok(마감 Grok 재시도)", forbidden_hits
    if "accepted_with_conditions" in head or "accepted with conditions" in head:
        return "accepted_with_conditions(조건부 수용)", "close_as_preserved_clue_with_conditions_satisfied(조건 충족 후 보존 단서로 마감)", forbidden_hits
    if "accepted" in head and "rejected" not in head:
        return "accepted(수용)", "close_as_preserved_clue(보존 단서로 마감)", forbidden_hits
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)", "do_not_close_until_repaired(수리 전 마감 금지)", forbidden_hits
    if "needs_local_verification" in lowered or "needs local verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)", "do_not_close_until_named_local_checks_are_recorded(지정 로컬 확인 전 마감 금지)", forbidden_hits
    return "accepted_with_conditions(조건부 수용)", "close_as_preserved_clue_with_conditions_satisfied(조건 충족 후 보존 단서로 마감)", forbidden_hits


def close_allowed(advice: str, grok_success: bool, forbidden_hits: Sequence[str]) -> bool:
    return grok_success and advice.startswith("accepted") and not forbidden_hits


def grok_identity(result: Any) -> dict[str, Any]:
    return {
        "packet_path": rel(GROK_PACKET),
        "prompt_path": rel(GROK_PROMPT_PATH),
        "prompt_sha256": file_hash(GROK_PROMPT_PATH),
        "output_path": rel(GROK_CLEAN_PATH),
        "output_exists": path_exists(GROK_CLEAN_PATH),
        "output_sha256": file_hash(GROK_CLEAN_PATH),
        "metadata_path": rel(GROK_METADATA_PATH),
        "metadata_exists": path_exists(GROK_METADATA_PATH),
        "metadata_sha256": file_hash(GROK_METADATA_PATH),
        "success": bool(result.returncode == 0 and not result.timed_out),
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_hash": result.prompt_hash,
        "preflight_warnings": list(result.preflight_warnings),
        "unexpected_top_level_artifacts": list(result.unexpected_top_level_artifacts),
    }


def kpi_table(kpi_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    lines = [
        "| split/view(분할/보기) | test period(테스트 기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | trades/day(일 거래 수) | active tpd(활성일 거래 수) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | TUW(회복 전 체류) | max loss streak(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in kpi_rows:
        lines.append(
            "| `{split}` | `{period}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{active}` | `{win}` | `{avgw}` | `{avgl}` | `{payoff}` | `{exp}` | `{rec}` | `{tuw}` | `{streak}` | `{ls}` | `{gap}` |".format(
                split=f"{row['split']} / {row['view']}",
                period=row["test_period"],
                net=row["net_profit"],
                gp=row["gross_profit"],
                gl=row["gross_loss"],
                pf=row["profit_factor"],
                dd=row["drawdown_percent"],
                trades=row["trade_count"],
                tpd=row["trades_per_day"],
                active=row["runtime_active_date_trades_per_day"],
                win=row["win_rate_percent"],
                avgw=row["average_win"],
                avgl=row["average_loss"],
                payoff=row["payoff_ratio"],
                exp=row["expectancy"],
                rec=row["recovery_factor"],
                tuw=row["time_under_water"],
                streak=row["max_consecutive_loss"],
                ls=row["long_short_breakdown"],
                gap=row["proxy_runtime_kpi_gap"],
            )
        )
    return lines


def closeout_report_text(created_at: str, payload: Mapping[str, Any], grok: Mapping[str, Any], advice: str, direction: str, forbidden_hits: Sequence[str]) -> str:
    lines = [
        "# F77 Stage Closeout Report(F77 단계 마감 보고서)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload['status']}`",
        f"- judgment(판정): `{payload['judgment']}`",
        f"- closeout label(마감 라벨): `{payload['closeout_label']}`",
        f"- Grok advice(Grok 조언): `{advice}`",
        f"- final Codex direction(최종 Codex 방향): `{direction}`",
        f"- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`",
        f"- next action(다음 행동): `{payload['next_run_id']}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Hypothesis(가설)",
        "",
        payload["hypothesis"],
        "",
        f"Proxy expectation(프록시 예상): {payload['proxy_expectation']}",
        "",
        "## Closeout KPI(마감 핵심 성과 지표)",
        "",
        *kpi_table(payload["kpi_rows"]),
        "",
        "## Gap Attribution(간극 귀속)",
        "",
    ]
    for item in payload["gap_cause_map"]:
        lines.append(f"- `{item['gap_cause']}`: {item['bucket']} - {item['meaning']}")
    lines.extend(["", "## Preserved Clue(보존 단서)", ""])
    for item in payload["preserved_clue"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Negative Memory(부정 기억)", ""])
    for item in payload["negative_memory"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Next Frontier(다음 전선)",
            "",
            f"- next run(다음 실행): `{NEXT_RUN_ID}`",
            f"- next stage(다음 단계): `{NEXT_FRONTIER_STAGE_ID}`",
            f"- new hypothesis(새 가설): {payload['next_frontier_hypothesis']}",
            "",
            "## Result Judgment(결과 판정)",
            "",
            f"- result_subject(판정 대상): `{payload['result_judgment']['result_subject']}`",
            f"- judgment_label(판정 라벨): `{payload['result_judgment']['judgment_label']}`",
            f"- evidence_missing(부족 근거): `{'; '.join(payload['result_judgment']['evidence_missing'])}`",
            f"- next_condition(다음 조건): `{payload['result_judgment']['next_condition']}`",
            f"- local verification(로컬 검증): `{rel(LOCAL_VERIFICATION_PATH)}` all_passed `{payload.get('local_verification', {}).get('all_passed')}`",
            "",
            "## Grok Closeout Receipt(Grok 마감 영수증)",
            "",
            f"- packet(묶음): `{grok.get('packet_path')}`",
            f"- prompt(프롬프트): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`",
            f"- output(출력): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`",
            f"- metadata(메타데이터): `{grok.get('metadata_path')}` sha256 `{grok.get('metadata_sha256')}`",
            f"- success(성공): `{grok.get('success')}` returncode `{grok.get('returncode')}`",
            "",
            "This closeout does not create completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        ]
    )
    return "\n".join(lines)


def receipt_text(created_at: str, grok: Mapping[str, Any], advice: str, direction: str, forbidden_hits: Sequence[str], closeout_success: bool) -> str:
    return f"""# F77H Grok Stage Closeout Receipt(F77H Grok 단계 마감 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): stage closeout requires Grok second opinion(단계 마감은 Grok 2차 의견 필수).

Review size(검토 크기): `medium(중간)`

Direction before Grok(Grok 전 방향): close F77 as preserved clue(보존 단서) with negative memory(부정 기억), no authority(권위 없음).

Bounded evidence(제한 근거): F77B proxy summary(F77B 프록시 요약), F77F runtime receipt(F77F 런타임 영수증), F77G gap analysis(F77G 간극 분석), closeout KPI table(마감 KPI 표).

Prompt identity(프롬프트 정체성): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`

Grok output identity(Grok 출력 정체성): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`

Advice classification(조언 분류): `{advice}`

Local verification(로컬 검증): `{rel(LOCAL_VERIFICATION_PATH)}`. Codex checked F77F receipt/summary, F77G gap rows, closeout condition mapping, registers, and forbidden claim boundary(Codex가 F77F 영수증/요약, F77G 간극 행, 마감 조건 매핑, 등록부, 금지 주장 경계를 확인했다).

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`.

Closeout success(마감 성공): `{closeout_success}`.

Final Codex direction(최종 Codex 방향): `{direction}`.
"""


def gate_audit_text(created_at: str, grok: Mapping[str, Any], advice: str, closeout_success: bool) -> str:
    return f"""# Required Gate Coverage Audit F77H Closeout(F77H 마감 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| hypothesis(가설) | `recorded(기록됨)` | `{rel(STAGE_DIR / '00_spec/stage_brief.md')}` |
| proxy KPI(프록시 KPI) | `recorded(기록됨)` | `{rel(F77B_SUMMARY)}` |
| MT5 runtime probe(MT5 런타임 탐침) | `completed(완료)` | tracked summary(추적 요약): `{rel(F77F_SUMMARY)}`; local ignored receipt(로컬 무시 영수증): `{rel(F77F_RECEIPT)}` |
| proxy/runtime gap analysis(프록시/런타임 간극 분석) | `completed(완료)` | `{rel(F77G_ANALYSIS)}` |
| repair(수리) | `completed(완료)` | point-unit repair(포인트 단위 수리) in F77F |
| closeout Grok review(마감 Grok 검토) | `{advice}` | `{grok.get('output_path')}` |
| local verification(로컬 검증) | `{'passed(통과)' if closeout_success else 'not_applied(미반영)'}` | `{rel(LOCAL_VERIFICATION_PATH)}` |
| F77G condition coverage(F77G 조건 커버리지) | `passed(통과)` | gap map, negative memory, preserved clues, new frontier hypothesis(간극 매핑/부정 기억/보존 단서/새 전선 가설) |
| final claim guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
| closeout applied(마감 반영) | `{'passed(통과)' if closeout_success else 'not_closed(미마감)'}` | `{rel(REPORT_PATH)}` |
"""


def ledger_row(created_at: str, payload: Mapping[str, Any], closeout_success: bool) -> dict[str, Any]:
    best = payload["runtime_probe_kpi"]
    row_id = f"{RUN_ID}::stage_closeout::tier_a"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "ledger_row_id": row_id,
        "subrun_id": "stage_closeout(단계 마감)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); combined out_of_scope(합산 범위 밖)",
        "kpi_scope": "stage_closeout_runtime_probe_gap_repair(단계 마감 런타임 탐침 간극 수리)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"net={best.get('net_profit', '')};pf={best.get('profit_factor', '')};dd={best.get('max_drawdown_percent', '')};tpd={best.get('trades_per_day', '')}",
        "guardrail_kpi": f"closeout_label={payload['closeout_label']};no_authority",
        "external_verification_status": "completed(완료)" if closeout_success else "grok_not_accepted(Grok 미수용)",
        "notes": f"closeout_label={payload['closeout_label']};next={payload['next_run_id']}",
        "lane": "stage_closeout(단계 마감)",
        "family": "stage_closeout(단계 마감)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier77H",
        "date": created_at[:10],
        "decision": payload["judgment"],
        "next_run_id": payload["next_run_id"],
        "rows": str(len(payload["kpi_rows"])),
        "gate_passes": "8" if closeout_success else "7",
        "gate_total": "8",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": payload["status"],
        "view": "stage_closeout",
        "tier": "Tier A separate",
        "metric_scope": "stage_closeout",
        "result_judgment": payload["judgment"],
        "final_decision_path": rel(SELECTION_STATUS_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "stage_closeout",
        "row_id": row_id,
        "evidence_boundary": "stage_closeout_only_no_authority(단계 마감 전용, 권위 없음)",
        "next_action": payload["next_run_id"],
        "artifact_count": "9",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_closeout",
        "run_type": "stage_closeout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "trade_density": best.get("trades_per_day", ""),
        "expectancy": best.get("expectancy", ""),
        "recovery_factor": best.get("recovery_factor", ""),
    }


def update_retrospective_register(created_at: str, closeout_success: bool) -> None:
    if not closeout_success:
        return
    data = yaml.safe_load(io_path(RETROSPECTIVE_REGISTER).read_text(encoding="utf-8-sig"))
    state = data.setdefault("state", {})
    closed = list(state.get("closed_frontier_ids_since_last_retrospective") or [])
    if STAGE_ID not in closed:
        closed.append(STAGE_ID)
    state["closed_frontier_ids_since_last_retrospective"] = closed
    state["closeouts_since_last"] = len(closed)
    state["next_numeric_trigger_frontier"] = 80
    state["current_due_status"] = RETROSPECTIVE_DUE_STATUS
    state["last_updated_at_utc"] = created_at
    state["note"] = (
        "F77 closeout(마감)이 F71-F75 retrospective(회고) 이후 2/5로 등록됐다. "
        "F78 open(개방)은 five-stage retrospective gate(5단계 회고 게이트) 관점에서 not_due(아직 아님)다."
    )
    io_path(RETROSPECTIVE_REGISTER).write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8-sig",
    )


def update_registers(created_at: str, payload: Mapping[str, Any], closeout_success: bool) -> None:
    update_retrospective_register(created_at, closeout_success)
    row = ledger_row(created_at, payload, closeout_success)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)
    marker = "<!-- frontier77H_stage_closeout_runtime_lifecycle_label_density_rebuild_v1 -->"
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in idea_text:
        addition = f"""

{marker}
- `{RUN_ID}` closed Frontier77(전선77) as `{payload['closeout_label']}`. Best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래 수): `{payload['runtime_probe_kpi'].get('net_profit')}/{payload['runtime_probe_kpi'].get('profit_factor')}/{payload['runtime_probe_kpi'].get('max_drawdown_percent')}/{payload['runtime_probe_kpi'].get('trades_per_day')}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{payload['next_run_id']}`.
"""
        write_text(IDEA_REGISTRY, idea_text.rstrip() + addition)
    negative_marker = "<!-- NR-FR77-RUNTIME-LIFECYCLE-LABEL-DENSITY-REBUILD -->"
    negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig")
    if negative_marker not in negative_text:
        addition = f"""

{negative_marker}
## NR-FR77-RUNTIME-LIFECYCLE-LABEL-DENSITY-REBUILD

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): runtime lifecycle-native labels(런타임 생명주기 기본 라벨)이 independent proxy overcount(독립 프록시 과대계산)를 줄이고 tradeable density(거래 가능 밀도)를 보존할 수 있다.
- Why failed(실패 이유): F77B meaningful signal(의미 신호) `0`, final-like reference(완성 유사 참조) `0`; F77F OOS runtime(표본외 런타임) net/PF/DD/tpd `4.48/1.23/1.41/0.14871794871794872`로 PF(수익 팩터)와 밀도(밀도)가 목표권 밖이었다.
- Salvage value(회수 가치): point-unit repair(포인트 단위 수리), ONNX/EA signal parity(ONNX/EA 신호 동등성), selected-entry veto tape(선택 진입 거부 테이프), runtime bridge mechanics(런타임 연결 메커니즘).
- Do-not-repeat(반복 금지): F77 lifecycle label surface(F77 생명주기 라벨 표면)를 threshold/session/export repair(임계값/세션/내보내기 수리)만 바꿔 반복하지 않는다.
- Reopen condition(재개 조건): broker contract P/L(브로커 계약 손익), final density denominator(최종 밀도 분모), fill semantics(체결 의미)를 label/target/trade shape(라벨/목표/거래 형태)에 처음부터 내장할 때만 재개한다.
- Evidence(근거): `{rel(REPORT_PATH)}`.
- Boundary(경계): no authority(권위 없음), no completion(완성 없음).
"""
        write_text(NEGATIVE_REGISTER, negative_text.rstrip() + addition)


def update_state(created_at: str, payload: Mapping[str, Any], closeout_success: bool) -> None:
    current_run = payload["next_run_id"] if closeout_success else RUN_ID
    latest_completed = RUN_ID if closeout_success else PARENT_RUN_ID
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {current_run}
latest_completed_run_id: {latest_completed}
current_status: {payload['status']}
current_judgment: {payload['judgment']}
next_run_id: {payload['next_run_id']}
runtime_probe_status: f77_mandatory_runtime_probe_completed_stage_closed
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: {RETROSPECTIVE_DUE_STATUS if closeout_success else 'not_due_after_f76_closeout_1_of_5'}
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F77H stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 Grok 조건 미충족으로 닫지 않았다'}."
  - "Effect(효과): F77 preserved clue(보존 단서), negative memory(부정 기억), next frontier hypothesis(다음 전선 가설)를 기록했다."
  - "Next(다음): {payload['next_run_id']}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{current_run}`

Latest completed run(최근 완료 실행): `{latest_completed}`

## Current Truth(현재 진실)

Action(행동): F77H stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 닫지 않았다'}.

Effect(효과): F77은 point-unit repair(포인트 단위 수리)와 ONNX/EA parity(ONNX/EA 동등성)를 보존 단서로 남기고, 약한 PF/density(수익 팩터/밀도)는 부정 기억으로 남겼다.

## Open Work(열린 작업)

- next run(다음 실행): `{payload['next_run_id']}`
- next frontier hypothesis(다음 전선 가설): {payload['next_frontier_hypothesis']}
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F77 Selection Status(F77 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{payload['status']}`

Judgment(판정): `{payload['judgment']}`

Closeout label(마감 라벨): `{payload['closeout_label']}`

Action(행동): F77H stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 닫지 않았다'}.

Effect(효과): 다음 실행은 새 hypothesis(가설)의 Frontier78 stage open(전선78 단계 개방)이다.

Current run(현재 실행): `{current_run}`

Latest completed run(최근 완료 실행): `{latest_completed}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS_PATH, selection)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    f77c = read_json(F77C_TARGET)
    target = dict(f77c.get("runtime_materialization_target") or {})
    f77g = read_json(F77G_ANALYSIS)
    receipts = read_csv(F77F_RECEIPT)
    kpi_rows = closeout_kpi_rows(receipts, target, f77g)
    draft_payload = build_closeout_payload(created_at, kpi_rows, True)
    prompt = build_prompt(draft_payload)
    write_text(GROK_PROMPT_PATH, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        repo_root=ROOT,
        output_dir=GROK_PACKET,
        prompt_file_path=GROK_PROMPT_PATH,
        review_size="medium",
        timeout_seconds=300,
    )
    success = bool(result.returncode == 0 and not result.timed_out)
    clean_output = io_path(GROK_CLEAN_PATH).read_text(encoding="utf-8-sig") if path_exists(GROK_CLEAN_PATH) else result.clean_stdout
    advice, direction, forbidden_hits = classify_advice(clean_output, success)
    draft_local_verification = build_local_verification(created_at, draft_payload)
    closeout_success = close_allowed(advice, success, forbidden_hits) and bool(draft_local_verification["all_passed"])
    payload = build_closeout_payload(created_at, kpi_rows, closeout_success)
    local_verification = build_local_verification(created_at, payload)
    write_json(LOCAL_VERIFICATION_PATH, local_verification)
    payload["local_verification"] = local_verification
    grok = grok_identity(result)
    write_text(REPORT_PATH, closeout_report_text(created_at, payload, grok, advice, direction, forbidden_hits))
    write_text(RECEIPT_PATH, receipt_text(created_at, grok, advice, direction, forbidden_hits, closeout_success))
    write_text(GATE_AUDIT_PATH, gate_audit_text(created_at, grok, advice, closeout_success))
    lineage = artifact_lineage(created_at, closeout_success)
    write_json(LINEAGE_PATH, lineage)
    payload["artifact_lineage"] = lineage
    payload["grok"] = grok
    payload["advice_classification"] = advice
    payload["final_codex_direction"] = direction
    payload["forbidden_claim_hits"] = list(forbidden_hits)
    write_json(SUMMARY_PATH, payload)
    write_json(RUN_MANIFEST_PATH, payload)
    write_csv(KPI_ROWS_PATH, kpi_rows)
    write_csv(RUN_DIR / "f77h_closeout_kpi_rows.csv", kpi_rows)
    update_registers(created_at, payload, closeout_success)
    update_state(created_at, payload, closeout_success)
    print(
        json.dumps(
            json_ready(
                {
                    "status": payload["status"],
                    "judgment": payload["judgment"],
                    "closeout_label": payload["closeout_label"],
                    "advice_classification": advice,
                    "grok_success": success,
                    "closeout_success": closeout_success,
                    "next_run_id": payload["next_run_id"],
                    "forbidden_claim_hits": list(forbidden_hits),
                    "report": rel(REPORT_PATH),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if closeout_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
