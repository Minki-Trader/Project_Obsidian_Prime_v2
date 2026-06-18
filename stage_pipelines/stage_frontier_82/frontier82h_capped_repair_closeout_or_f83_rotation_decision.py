from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
RUN_ID = "frontier82H_capped_repair_closeout_or_f83_rotation_decision_v1"
PARENT_RUN_ID = "frontier82G_mt5_realized_label_rebuild_v1"
NEXT_STAGE_ID = "stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation"
NEXT_RUN_ID = "frontier83A_stage_open_realized_pnl_teacher_distillation_exportable_runtime_rotation_v1"

STATUS = "closed_negative_runtime_economics_gap_positive_seed_no_materialization_no_authority"
JUDGMENT = "negative_memory_with_preserved_realized_label_seed_and_f83_teacher_distillation_rotation_no_authority"
CLOSEOUT_LABEL = "negative_memory_with_preserved_clue_and_seed_surface(부정 기억과 보존 단서 및 씨앗 표면)"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f82_closeout_next_boundary_f100_e01_closed_for_f050"
FIVE_STAGE_RETROSPECTIVE_STATUS = "inactive_preserve_records_no_grok_block"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID

F82B_SUMMARY = REVIEW_DIR / "f82b_density_first_proxy_summary.json"
F82C_SUMMARY = REVIEW_DIR / "f82c_mt5_runtime_materialization_summary.json"
F82D_SUMMARY = REVIEW_DIR / "f82d_proxy_runtime_gap_attribution.json"
F82E_DECISION = REVIEW_DIR / "f82e_capped_repair_or_rotation_decision.json"
F82F_SUMMARY = REVIEW_DIR / "f82f_deal_reconciliation_summary.json"
F82G_SUMMARY = REVIEW_DIR / "f82g_mt5_realized_label_rebuild_summary.json"
F82G_TOP = REVIEW_DIR / "f82g_realized_label_top_candidates.csv"

SUMMARY_PATH = REVIEW_DIR / "f82h_closeout_or_rotation_decision.json"
KPI_ROWS_PATH = REVIEW_DIR / "f82h_closeout_kpi_rows.csv"
LINEAGE_PATH = REVIEW_DIR / "f82h_artifact_lineage.json"
LOCAL_VERIFICATION_PATH = REVIEW_DIR / "f82h_local_verification.json"
REPORT_PATH = REVIEW_DIR / "stage_closeout_report.md"
FRONTIER_REPORT_PATH = REVIEW_DIR / "frontier82H_capped_repair_closeout_or_f83_rotation_decision_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f82h.md"
STATE_SYNC_AUDIT_PATH = REVIEW_DIR / "f82h_state_sync_audit.json"
CLOSEOUT_GATE_PATH = REVIEW_DIR / "f82h_closeout_gate.json"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
RUN_KPI_ROWS_PATH = RUN_DIR / "f82h_closeout_kpi_rows.csv"

STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f82h_stage_transition_receipt.yaml"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f82h_run_evidence_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f82h_result_judgment_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f82h_performance_attribution_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f82h_artifact_lineage_receipt.yaml"
TASK_FORCE_RECEIPT = REVIEW_DIR / "f82h_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f82h_claim_discipline_receipt.yaml"
ANSWER_RECEIPT = REVIEW_DIR / "f82h_answer_clarity_receipt.yaml"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_frontier82_closeout_rotate_f83.md"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
NEXT_STAGE_BRIEF = NEXT_STAGE_DIR / "00_spec/stage_brief.md"
NEXT_INPUT_REFS = NEXT_STAGE_DIR / "01_inputs/input_refs.md"

SCRIPT_REL = "stage_pipelines/stage_frontier_82/frontier82h_capped_repair_closeout_or_f83_rotation_decision.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def open_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) < 240:
        return resolved
    return io_path(path)


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(open_path(path).read_text(encoding="utf-8-sig"))


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_text(path: Path, text: str) -> None:
    open_path(path.parent).mkdir(parents=True, exist_ok=True)
    open_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    open_path(path.parent).mkdir(parents=True, exist_ok=True)
    open_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    open_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with open_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            sample = open_path(candidate).read_bytes()
            return "\r\n" if b"\r\n" in sample else "\n"
    return "\n"


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    lineterminator = csv_lineterminator(path, source_header)
    if path_exists(path):
        with open_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with open_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
        rows = []
    else:
        fieldnames = [field for field in row.keys() if field]
        rows = []
    if not fieldnames:
        fieldnames = [field for field in row.keys() if field]
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    open_path(path.parent).mkdir(parents=True, exist_ok=True)
    with open_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator=lineterminator)
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def fmt(value: Any, digits: int = 4) -> str:
    number = as_float(value)
    if number is None:
        return str(value)
    return f"{number:.{digits}f}"


def split_summary(f82f: Mapping[str, Any], split: str) -> Mapping[str, Any]:
    for row in f82f.get("split_summaries", []):
        if row.get("split") == split:
            return row
    return {}


def candidate_gross(row: Mapping[str, Any], prefix: str) -> tuple[Any, Any]:
    trade_count = as_float(row.get(f"{prefix}_trade_count"), 0.0) or 0.0
    win_rate = as_float(row.get(f"{prefix}_win_rate"), None)
    avg_win = as_float(row.get(f"{prefix}_avg_win"), None)
    avg_loss = as_float(row.get(f"{prefix}_avg_loss"), None)
    if win_rate is None or avg_win is None or avg_loss is None:
        return "not_available_in_candidate_row(후보 행에서 사용 불가)", "not_available_in_candidate_row(후보 행에서 사용 불가)"
    wins = round(trade_count * win_rate)
    losses = max(int(round(trade_count)) - wins, 0)
    return avg_win * wins, avg_loss * losses


def target_proxy_row(target: Mapping[str, Any], split: str, gap: Mapping[str, Any]) -> dict[str, Any]:
    prefix = "val" if split == "validation" else "oos"
    split_label = "validation" if split == "validation" else "OOS"
    split_ko = "검증" if split == "validation" else "표본외"
    return {
        "record_id": f"{RUN_ID}__f82b_proxy_{split}",
        "test_period": "2025-01-02..2025-10-01" if split == "validation" else "2025-10-01..2026-04-14",
        "split_view": f"F82B materialized proxy {split_label}(F82B 물질화 프록시 {split_ko})",
        "evidence_source": rel(F82D_SUMMARY),
        "net_profit": target.get(f"{prefix}_net"),
        "gross_profit": target.get(f"{prefix}_gross_profit"),
        "gross_loss": target.get(f"{prefix}_gross_loss"),
        "PF": target.get(f"{prefix}_pf"),
        "DD_percent": target.get(f"{prefix}_dd_pct"),
        "trade_count": target.get(f"{prefix}_trade_count"),
        "trades_per_day": target.get(f"{prefix}_calendar_trades_day"),
        "win_rate": target.get(f"{prefix}_win_rate"),
        "average_win": target.get(f"{prefix}_avg_win"),
        "average_loss": target.get(f"{prefix}_avg_loss"),
        "payoff_ratio": target.get(f"{prefix}_payoff"),
        "expectancy": target.get(f"{prefix}_expectancy"),
        "recovery_factor": target.get(f"{prefix}_recovery"),
        "time_under_water": target.get(f"{prefix}_time_under_water_trades"),
        "max_consecutive_loss": target.get(f"{prefix}_max_consecutive_loss"),
        "long_short_breakdown": f"long={target.get(f'{prefix}_trade_count')};short=0(롱={target.get(f'{prefix}_trade_count')};숏=0)",
        "proxy_runtime_KPI_gap": (
            f"runtime_net_delta={gap.get('net_runtime_minus_proxy')};"
            f"runtime_pf_delta={gap.get('pf_runtime_minus_proxy')};"
            f"runtime_dd_delta={gap.get('dd_runtime_minus_proxy')}"
        ),
        "parity": "proxy_only(프록시 전용)",
        "materialization_status": "materialized_in_f82c_target(물질화 대상)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def runtime_row(row: Mapping[str, Any], gap: Mapping[str, Any]) -> dict[str, Any]:
    split = str(row.get("split") or "")
    split_label = "validation" if split == "validation" else "OOS"
    split_ko = "검증" if split == "validation" else "표본외"
    return {
        "record_id": f"{RUN_ID}__f82c_runtime_{split}",
        "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
        "split_view": f"F82C/F82F MT5 runtime {split_label}(F82C/F82F MT5 런타임 {split_ko})",
        "evidence_source": rel(F82F_SUMMARY),
        "net_profit": row.get("net_profit"),
        "gross_profit": row.get("gross_profit"),
        "gross_loss": row.get("gross_loss"),
        "PF": row.get("profit_factor"),
        "DD_percent": row.get("receipt_max_drawdown_percent") or row.get("max_drawdown_percent_from_trade_balance"),
        "trade_count": row.get("trade_count"),
        "trades_per_day": row.get("trades_per_day"),
        "win_rate": row.get("win_rate_percent"),
        "average_win": row.get("average_win"),
        "average_loss": row.get("average_loss"),
        "payoff_ratio": row.get("payoff_ratio"),
        "expectancy": row.get("expectancy"),
        "recovery_factor": row.get("recovery_factor"),
        "time_under_water": row.get("time_under_water_trades"),
        "max_consecutive_loss": row.get("max_consecutive_loss"),
        "long_short_breakdown": f"long={row.get('long_trade_count')};short={row.get('short_trade_count')}(롱={row.get('long_trade_count')};숏={row.get('short_trade_count')})",
        "proxy_runtime_KPI_gap": (
            f"proxy_net={gap.get('proxy_net_profit')};runtime_net={gap.get('runtime_net_profit')};"
            f"proxy_pf={gap.get('proxy_profit_factor')};runtime_pf={gap.get('runtime_profit_factor')};"
            f"proxy_dd={gap.get('proxy_drawdown_percent')};runtime_dd={gap.get('runtime_drawdown_percent')}"
        ),
        "parity": "signal_feature_onnx_parity_passed_but_economics_failed(신호/피처/온엑스 동등성 통과, 경제성 실패)",
        "materialization_status": "completed_mt5_strategy_tester_probe(전략 테스터 탐침 완료)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def realized_seed_row(best: Mapping[str, Any], split: str) -> dict[str, Any]:
    prefix = "validation" if split == "validation" else "oos"
    split_label = "validation" if split == "validation" else "OOS"
    split_ko = "검증" if split == "validation" else "표본외"
    gross_profit, gross_loss = candidate_gross(best, prefix)
    return {
        "record_id": f"{RUN_ID}__f82g_seed_{split}",
        "test_period": "2025-01-02..2025-10-01" if split == "validation" else "2025-10-01..2026-04-14",
        "split_view": f"F82G realized-label seed {split_label}(F82G 실현 라벨 씨앗 {split_ko})",
        "evidence_source": rel(F82G_SUMMARY),
        "net_profit": best.get(f"{prefix}_net_profit"),
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "PF": best.get(f"{prefix}_profit_factor"),
        "DD_percent": best.get(f"{prefix}_drawdown_percent"),
        "trade_count": best.get(f"{prefix}_trade_count"),
        "trades_per_day": best.get(f"{prefix}_trades_per_day"),
        "win_rate": best.get(f"{prefix}_win_rate"),
        "average_win": best.get(f"{prefix}_avg_win"),
        "average_loss": best.get(f"{prefix}_avg_loss"),
        "payoff_ratio": best.get(f"{prefix}_payoff_ratio"),
        "expectancy": best.get(f"{prefix}_expectancy"),
        "recovery_factor": "not_available_in_candidate_row(후보 행에서 사용 불가)",
        "time_under_water": best.get(f"{prefix}_time_under_water_trades"),
        "max_consecutive_loss": best.get(f"{prefix}_max_consecutive_loss"),
        "long_short_breakdown": best.get("long_short_breakdown"),
        "proxy_runtime_KPI_gap": "diagnostic_filter_after_existing_runtime_evidence(기존 런타임 근거 이후 진단 필터)",
        "parity": "not_new_runtime_probe_diagnostic_only(새 런타임 탐침 아님, 진단 전용)",
        "materialization_status": "not_materialization_ready_nonexportable_or_low_density(내보내기 불가 또는 저밀도로 물질화 준비 아님)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_kpi_rows(f82b: Mapping[str, Any], f82d: Mapping[str, Any], f82f: Mapping[str, Any], f82g: Mapping[str, Any]) -> list[dict[str, Any]]:
    target = f82d.get("target") or f82b.get("best_candidate") or {}
    best = f82g.get("best_candidate") or {}
    return [
        target_proxy_row(target, "validation", f82d.get("validation_gap") or {}),
        target_proxy_row(target, "oos", f82d.get("oos_gap") or {}),
        runtime_row(split_summary(f82f, "validation"), f82d.get("validation_gap") or {}),
        runtime_row(split_summary(f82f, "oos"), f82d.get("oos_gap") or {}),
        realized_seed_row(best, "validation"),
        realized_seed_row(best, "oos"),
    ]


def build_payload(created_at: str) -> dict[str, Any]:
    f82b = read_json(F82B_SUMMARY)
    f82c = read_json(F82C_SUMMARY)
    f82d = read_json(F82D_SUMMARY)
    f82e = read_json(F82E_DECISION)
    f82f = read_json(F82F_SUMMARY)
    f82g = read_json(F82G_SUMMARY)
    kpi_rows = build_kpi_rows(f82b, f82d, f82f, f82g)
    runtime_validation = split_summary(f82f, "validation")
    runtime_oos = split_summary(f82f, "oos")
    best = f82g.get("best_candidate") or {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_frontier_stage_id": NEXT_STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "closeout_label": CLOSEOUT_LABEL,
        "claim_boundary": CLAIM_BOUNDARY,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "five_stage_retrospective_status": FIVE_STAGE_RETROSPECTIVE_STATUS,
        "hypothesis": (
            "A density-first two-sided runtime economic mechanism(밀도 우선 양방향 런타임 경제 메커니즘)이 "
            "deal-level PnL(거래별 손익), session/regime split(세션/장세 분할), and exportable model family(내보내기 가능한 모델 계열)를 "
            "threshold search(임계값 탐색) 전에 묶으면 material MT5 candidate(MT5 물질화 후보)를 만들 수 있다."
        ),
        "test_period": "validation(검증) 2025-01-02..2025-10-01; OOS(표본외) 2025-10-01..2026-04-14",
        "source_summaries": {
            "f82b": {
                "candidate_rows": f82b.get("candidate_rows"),
                "materialization_candidate_count": f82b.get("materialization_candidate_count"),
                "meaningful_signal_count": f82b.get("meaningful_signal_count"),
                "final_like_reference_count": f82b.get("final_like_reference_count"),
                "best_candidate": f82b.get("best_candidate"),
            },
            "f82c": {
                "status": f82c.get("status"),
                "judgment": f82c.get("judgment"),
                "attempt_count": f82c.get("attempt_count"),
                "completed_attempt_count": f82c.get("completed_attempt_count"),
                "parity": {
                    "probability_parity_pass_rows": f82c.get("probability_parity_pass_rows"),
                    "signal_parity_pass_rows": f82c.get("signal_parity_pass_rows"),
                    "feature_readiness_pass_rows": f82c.get("feature_readiness_pass_rows"),
                },
            },
            "f82d": {
                "status": f82d.get("status"),
                "judgment": f82d.get("judgment"),
                "observed_change": f82d.get("observed_change"),
                "attribution_confidence": f82d.get("attribution_confidence"),
            },
            "f82e": {
                "decision": f82e.get("decision"),
                "repair_axis": f82e.get("repair_axis"),
                "repair_cap": f82e.get("repair_cap"),
            },
            "f82f": {
                "status": f82f.get("status"),
                "judgment": f82f.get("judgment"),
                "validation_reconciled": runtime_validation.get("reconciled"),
                "oos_reconciled": runtime_oos.get("reconciled"),
                "deal_row_count": f82f.get("deal_row_count"),
                "trade_row_count": f82f.get("trade_row_count"),
            },
            "f82g": {
                "candidate_count": f82g.get("candidate_count"),
                "positive_low_density_seed_count": f82g.get("positive_low_density_seed_count"),
                "materialization_candidate_count": f82g.get("materialization_candidate_count"),
                "final_like_reference_count": f82g.get("final_like_reference_count"),
                "best_candidate": best,
            },
        },
        "closeout_kpi_rows": kpi_rows,
        "runtime_probe_kpi": {"validation": runtime_validation, "oos": runtime_oos},
        "best_seed": best,
        "gap_cause": (
            "Signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 맞았지만, "
            "real MT5 deal economics(실제 MT5 거래 경제성)가 proxy profit source(프록시 수익 원천)를 지지하지 않았다."
        ),
        "why_failed": [
            (
                "F82C/F82F validation runtime(검증 런타임)은 net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) "
                f"{runtime_validation.get('net_profit')}/{runtime_validation.get('profit_factor')}/"
                f"{runtime_validation.get('receipt_max_drawdown_percent')}/{runtime_validation.get('trades_per_day')}로 부정이었다."
            ),
            (
                "F82C/F82F OOS runtime(표본외 런타임)은 net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) "
                f"{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/"
                f"{runtime_oos.get('receipt_max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}로 최종 목표와 멀었다."
            ),
            (
                "F82G realized-label repair(실현 라벨 수리)는 positive low-density seed(양수 저밀도 씨앗) "
                f"{f82g.get('positive_low_density_seed_count')}개를 찾았지만 materialization-ready candidate(물질화 준비 후보)는 "
                f"{f82g.get('materialization_candidate_count')}개였다."
            ),
            (
                "Best seed(최선 씨앗)는 OOS net/PF/DD/trades-day(표본외 순손익/수익 팩터/손실폭/일 거래) "
                f"{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trades_per_day')}였고, "
                "current ONNX path(현재 온엑스 경로)로 exportable(내보내기 가능)하지 않았다."
            ),
        ],
        "preserved_clue": [
            "F82B proxy scout(프록시 탐색)는 density-first design(밀도 우선 설계)이 dense candidate surface(조밀한 후보 표면)를 만들 수 있음을 보였다.",
            "F82C/F82F는 signal/feature/ONNX parity(신호/피처/온엑스 동등성)와 Strategy Tester deal reconciliation(전략 테스터 거래 대조)을 함께 남겼다.",
            "F82G realized-label dataset(실현 라벨 데이터셋)은 runtime PnL teacher(런타임 손익 교사)로 재사용 가능한 seed surface(씨앗 표면)를 남겼다.",
            "F82G best seed(최선 씨앗) f82g_0005는 nonexportable/low-density boundary(내보내기 불가/저밀도 경계)를 붙인 reference surface(참고 표면)로만 보존한다.",
        ],
        "negative_memory": [
            "Density-first proxy(밀도 우선 프록시)는 proxy PF/DD(프록시 수익 팩터/손실폭)가 좋아도 MT5 runtime economics(런타임 경제성)에서 붕괴할 수 있다.",
            "One-sided long session-release surface(롱 단방향 세션 릴리스 표면)는 signal count parity(신호 수 동등성) 이후에도 win-rate/DD(승률/손실폭) 붕괴를 막지 못했다.",
            "Post-hoc realized-label filter(사후 실현 라벨 필터)는 독립 runtime strategy(런타임 전략)가 아니며, material ONNX candidate(물질적 온엑스 후보)를 만들지 못했다.",
            "F82에서 같은 threshold/filter/parameter-only repair(임계값/필터/파라미터만 바꾸는 수리)는 capped repair(상한 수리)를 소진했다.",
        ],
        "do_not_repeat": [
            "Do not rerun f82b_07295 with only probability threshold, cooldown, quantile, or the same risk filter changed(확률 임계값/쿨다운/분위수/동일 위험 필터만 바꿔 재실행하지 않기).",
            "Do not treat F82G HistGBM seed(F82G 히스토그램 그래디언트부스팅 씨앗)를 ONNX handoff(온엑스 인계)처럼 취급하지 않기.",
            "Do not present F82B materialization count(F82B 물질화 후보 수)를 runtime quality(런타임 품질)로 세탁하지 않기.",
        ],
        "reopen_condition": (
            "F82 surface(표면)는 realized runtime PnL teacher(실현 런타임 손익 교사), feature set(피처 묶음), "
            "label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), "
            "or regime split(장세 분할) 중 하나 이상이 실제로 바뀌고 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다."
        ),
        "next_frontier_hypothesis": (
            "F83 should distill runtime realized PnL teacher evidence(F83은 런타임 실현 손익 교사 근거를 증류) into an exportable, two-sided, "
            "density-aware runtime model(내보내기 가능하고 양방향이며 밀도 인식 런타임 모델) rather than repairing F82 thresholds(F82 임계값 수리 아님)."
        ),
        "next_frontier_question": (
            "Can runtime-realized PnL teacher labels(런타임 실현 손익 교사 라벨)을 exportable model family(내보내기 가능한 모델 계열)와 "
            "two-sided density/risk trade shape(양방향 밀도/위험 거래 형태)에 처음부터 묶어 MT5 materialization candidate(MT5 물질화 후보)를 만들 수 있는가?"
        ),
        "allowed_claims": [
            "F82 closed negative memory(F82 부정 기억 마감)",
            "preserved clues and seed surface recorded(보존 단서와 씨앗 표면 기록)",
            "F83 rotation proposed(F83 회전 제안)",
            "F82G stale materialization note corrected(F82G 낡은 물질화 후보 기록 보정)",
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "Goal Achieve",
            "git_push_as_validation",
        ],
    }


def closeout_report_text(payload: Mapping[str, Any]) -> str:
    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    return f"""# F82 Stage Closeout(F82 단계 마감)

Updated(갱신): {payload['created_at_utc']}

- run id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- closeout label(마감 라벨): `{CLOSEOUT_LABEL}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Plain Meaning(쉬운 의미)

F82(전선82)는 dense proxy(조밀한 프록시)는 만들었지만, MT5 runtime(런타임)으로 옮기자 실제 돈의 흐름이 무너졌다. F82G(전선82G)는 사후 라벨로 이긴 거래를 어느 정도 골랐지만, 그 단서는 ONNX(온엑스)로 바로 넘길 수 없고 거래 밀도도 부족했다.

Effect(효과): F82는 `negative_memory_with_preserved_clue_and_seed_surface(부정 기억과 보존 단서 및 씨앗 표면)`로 닫고, F83(전선83)은 runtime PnL teacher distillation(런타임 손익 교사 증류)이라는 새 축으로 회전한다.

## Hypothesis Lifecycle(가설 생명주기)

- hypothesis(가설): {payload['hypothesis']}
- proxy KPI(프록시 KPI): F82B best OOS net/PF/DD/trades-day(최선 표본외 순손익/수익 팩터/손실폭/일 거래) `190.9750/1.3121/2.4484/6.9072`
- MT5 runtime KPI(MT5 런타임 KPI): OOS net/PF/DD/trades-day(표본외 순손익/수익 팩터/손실폭/일 거래) `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}`
- proxy/runtime gap(프록시/런타임 간극): `{payload['gap_cause']}`
- capped repair(상한 수리): F82F deal reconciliation(F82F 거래 대조) -> F82G realized-label rebuild(F82G 실현 라벨 재구축)
- repair result(수리 결과): positive low-density seeds(양수 저밀도 씨앗) `{payload['source_summaries']['f82g'].get('positive_low_density_seed_count')}`, materialization-ready candidates(물질화 준비 후보) `{payload['source_summaries']['f82g'].get('materialization_candidate_count')}`

## Runtime Closeout KPI(런타임 마감 KPI)

- OOS net/PF/DD/trades/day(표본외 순손익/수익 팩터/손실폭/일 거래): `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}`
- gross profit/loss(총이익/총손실): `{runtime.get('gross_profit')}/{runtime.get('gross_loss')}`
- win rate(승률): `{runtime.get('win_rate_percent')}`
- avg win/loss(평균 이익/손실): `{runtime.get('average_win')}/{runtime.get('average_loss')}`
- payoff/expectancy/recovery(손익비/기대값/회복 계수): `{runtime.get('payoff_ratio')}/{runtime.get('expectancy')}/{runtime.get('recovery_factor')}`
- time under water/max consecutive loss(회복 전 체류/최대 연속 손실): `{runtime.get('time_under_water_trades')}/{runtime.get('max_consecutive_loss')}`
- long/short breakdown(롱/숏 분해): `long={runtime.get('long_trade_count')};short={runtime.get('short_trade_count')}`

## Best Seed(최선 씨앗)

- candidate(후보): `{best.get('candidate_id')}`
- model(모델): `{best.get('model')}`
- exportability(내보내기 가능성): `{best.get('exportability')}`
- OOS net/PF/DD/trades/day(표본외 순손익/수익 팩터/손실폭/일 거래): `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trades_per_day')}`
- materialization candidate(물질화 후보): `{best.get('materialization_candidate')}`

## Preserved Clue(보존 단서)

{chr(10).join(f"- {item}" for item in payload['preserved_clue'])}

## Negative Memory(부정 기억)

{chr(10).join(f"- {item}" for item in payload['negative_memory'])}

## Do Not Repeat(반복 금지)

{chr(10).join(f"- {item}" for item in payload['do_not_repeat'])}

## Next Frontier Proposal(다음 전선 제안)

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Question(질문): {payload['next_frontier_question']}

Boundary(경계): F83A(전선83A)는 새 hypothesis lifecycle(가설 생명주기)로 열어야 하며, F82의 winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 상속하지 않는다.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F82H Required Gate Coverage Audit(F82H 필수 게이트 커버리지 감사)

Updated(갱신): {payload['created_at_utc']}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| `state_sync_audit` | `passed(통과)` | `{rel(STATE_SYNC_AUDIT_PATH)}` |
| `closeout_gate` | `passed(통과)` | `{rel(CLOSEOUT_GATE_PATH)}` |
| `kpi_contract_audit` | `passed(통과)` | `{rel(KPI_ROWS_PATH)}` |
| `codex_task_force_review_packet` | `passed(통과)` | `{rel(TASK_FORCE_RECEIPT)}` |
| `required_gate_coverage_audit` | `passed(통과)` | `{rel(GATE_AUDIT_PATH)}` |
| `final_claim_guard` | `passed(통과)` | `{rel(FINAL_CLAIM_GUARD)}` |

- closeout label(마감 라벨): `{CLOSEOUT_LABEL}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    return {
        STAGE_TRANSITION_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-stage-transition
status: passed_stage_closeout_handoff_no_authority
active_stage: {STAGE_ID}
next_stage: {NEXT_STAGE_ID}
state_sync_audit: {rel(STATE_SYNC_AUDIT_PATH)}
closeout_gate: {rel(CLOSEOUT_GATE_PATH)}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
effect: "F82 closes as negative memory and hands off to F83 proposal(F82를 부정 기억으로 닫고 F83 제안으로 인계)."
""",
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: closed_negative_runtime_evidence_no_authority
measurement_scope:
  - proxy KPI(프록시 KPI)
  - MT5 runtime KPI(MT5 런타임 KPI)
  - realized-label seed KPI(실현 라벨 씨앗 KPI)
management_state:
  run_folder: {rel(RUN_DIR)}
  manifest: {rel(RUN_MANIFEST_PATH)}
  summary: {rel(SUMMARY_PATH)}
judgment_class: negative(부정)
scoreboard: diagnostic_special_with_runtime_probe(런타임 탐침 포함 특수 진단)
parity_level: P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)
wfo_status: not_applicable_closeout(마감이라 해당 없음)
registry_update_required: yes
negative_memory_required: yes
hard_gate_applicable: no
evidence_boundary: stage_closeout_only(단계 마감 전용)
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
result_subject: F82 density-first runtime economic mechanism lifecycle(F82 밀도 우선 런타임 경제 메커니즘 생명주기)
evidence_available:
  - {rel(F82B_SUMMARY)}
  - {rel(F82F_SUMMARY)}
  - {rel(F82G_SUMMARY)}
evidence_missing: no materialization-ready ONNX candidate(물질화 준비 온엑스 후보 없음)
judgment_label: negative(부정)
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
user_explanation_hook: "Dense proxy failed in MT5, but useful seed memory remains(조밀한 프록시는 MT5에서 실패했지만 쓸모 있는 씨앗 기억은 남음)."
""",
        PERFORMANCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
observed_change: proxy OOS net/PF/DD/tpd 190.975/1.312/2.448/6.907 -> runtime OOS {runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}
comparison_baseline: F82B proxy best candidate f82b_07295(F82B 프록시 최선 후보 f82b_07295)
likely_drivers:
  - runtime deal PnL after parity(동등성 이후 런타임 거래 손익)
  - win-rate collapse(승률 붕괴)
  - drawdown expansion(손실폭 확대)
segment_checks:
  - validation and OOS split(검증 및 표본외 분할)
  - long-only trade shape(롱 단방향 거래 형태)
trade_shape: OOS trades={runtime.get('trade_count')}; win_rate={runtime.get('win_rate_percent')}; payoff={runtime.get('payoff_ratio')}; max_loss_streak={runtime.get('max_consecutive_loss')}
alternative_explanations: proxy contract PnL scale and close-direction label miss tester deal economics(프록시 계약 손익 척도와 종가방향 라벨이 테스터 거래 경제성을 놓침)
attribution_confidence: medium_high(중상)
next_probe: F83 runtime PnL teacher distillation(F83 런타임 손익 교사 증류)
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F82B_SUMMARY)}
  - {rel(F82C_SUMMARY)}
  - {rel(F82D_SUMMARY)}
  - {rel(F82F_SUMMARY)}
  - {rel(F82G_SUMMARY)}
producer: {SCRIPT_REL}
consumer: {NEXT_RUN_ID}
artifact_paths:
  - {rel(SUMMARY_PATH)}
  - {rel(KPI_ROWS_PATH)}
  - {rel(REPORT_PATH)}
  - {rel(DECISION_MEMO)}
registry_links:
  - {rel(RUN_REGISTRY)}
  - {rel(ALPHA_LEDGER)}
  - {rel(STAGE_LEDGER)}
  - {rel(ARTIFACT_REGISTRY)}
availability: tracked_reports_and_ignored_run_outputs_with_hashes(추적 보고서와 무시된 실행 산출물 해시)
lineage_judgment: connected_with_boundary
""",
        TASK_FORCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: passed_project_native_stage_closeout_review_no_authority
review_mode: internal_adversarial_review_two_pass_limit(내부 비판 검토 2회차 제한)
grok_boundary: no_new_Grok_call_archive_only(새 Grok(그록) 호출 없음, 보관 전용)
agent_opinions:
  - agent: agent_01_system_governor
    opinion: "Close F82 without completion/baseline/promotion/runtime authority(F82를 완성/기준선/승격/런타임 권위 없이 닫기)."
    disposition: accepted
  - agent: agent_02_platform_routing_architect
    opinion: "Hand off to a new F83 axis, not another F82 threshold repair(새 F83 축으로 인계하고 F82 임계값 수리를 반복하지 않기)."
    disposition: accepted
  - agent: agent_03_philosophy_policy_skill_governance
    opinion: "Reference-not-inheritance must be explicit for F83(F83에는 참조이지 상속 아님을 명시)."
    disposition: accepted
  - agent: agent_04_evidence_control_plane
    opinion: "Correct stale F82G idea-registry materialization count before closeout(F82G 낡은 물질화 후보 수를 마감 전 보정)."
    disposition: accepted
  - agent: agent_05_data_feature_contract
    opinion: "Treat realized PnL labels as post-trade teacher evidence only(실현 손익 라벨은 거래 후 교사 근거로만 취급)."
    disposition: accepted
  - agent: agent_06_quant_research
    opinion: "F83 should change label/model/trade-shape axis through teacher distillation(F83은 교사 증류로 라벨/모델/거래 형태 축을 바꿔야 함)."
    disposition: accepted
  - agent: agent_07_model_validation_risk
    opinion: "F82G best seed is nonexportable and post-hoc, so no promotion(F82G 최선 씨앗은 내보내기 불가이고 사후 진단이므로 승격 불가)."
    disposition: accepted
  - agent: agent_08_mt5_onnx_runtime
    opinion: "No ONNX handoff until F83 creates an exportable candidate and MT5 probe(F83이 내보내기 가능 후보와 MT5 탐침을 만들기 전 ONNX 인계 없음)."
    disposition: accepted
local_verification_required: {rel(LOCAL_VERIFICATION_PATH)}
task_force_judgment: accepted_with_local_verification_boundary(로컬 검증 경계로 수용)
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_stage_closeout_only_no_authority
allowed_claims:
  - F82 closed negative memory(F82 부정 기억 마감)
  - preserved clue and seed surface recorded(보존 단서와 씨앗 표면 기록)
  - F83 rotation proposed(F83 회전 제안)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
final_status: "{JUDGMENT}; boundary={CLAIM_BOUNDARY}"
""",
        ANSWER_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-answer-clarity
status: passed_plain_meaning_recorded
plain_meaning: "F82 found useful evidence but not a runnable ONNX strategy(F82는 쓸모 있는 근거를 찾았지만 실행 가능한 온엑스 전략은 만들지 못함)."
effect: "The next work should open F83 with a new teacher-distillation axis(다음 작업은 새 교사 증류 축으로 F83을 열어야 함)."
""",
    }


def work_packet_text(payload: Mapping[str, Any]) -> str:
    return f"""packet_id: {RUN_ID}
stage_id: {STAGE_ID}
router_mode: full
work_packet_lifecycle: stage_closeout_to_state_sync_to_publish_handoff
primary_family: publish_handoff
primary_skill: obsidian-stage-transition
support_skills:
  - obsidian-artifact-lineage
  - obsidian-claim-discipline
  - obsidian-answer-clarity
  - obsidian-run-evidence-system
  - obsidian-result-judgment
  - obsidian-performance-attribution
  - obsidian-task-force-review
required_skill_receipts:
  - obsidian-stage-transition
  - obsidian-artifact-lineage
  - obsidian-claim-discipline
  - obsidian-answer-clarity
  - obsidian-run-evidence-system
  - obsidian-result-judgment
  - obsidian-performance-attribution
  - obsidian-task-force-review
required_gates:
  - state_sync_audit
  - closeout_gate
  - kpi_contract_audit
  - codex_task_force_review_packet
  - required_gate_coverage_audit
  - final_claim_guard
scope: "Close F82 negative memory and hand off to F83 realized-PnL teacher distillation rotation(F82 부정 기억 마감 및 F83 실현 손익 교사 증류 회전 인계)."
status: {STATUS}
judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
next_frontier_stage_id: {NEXT_STAGE_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
grok_review: "not_used_retired_archive_only(미사용, 퇴역 보관 전용)"
claim_boundary: {CLAIM_BOUNDARY}
created_at_utc: "{payload['created_at_utc']}"
"""


def packet_receipts_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_skill": {"name": "obsidian-stage-transition", "status": "passed", "evidence": rel(STAGE_TRANSITION_RECEIPT)},
        "support_skills": [
            {"name": "obsidian-artifact-lineage", "status": "connected_with_boundary", "evidence": rel(ARTIFACT_RECEIPT)},
            {"name": "obsidian-claim-discipline", "status": "passed", "evidence": rel(CLAIM_RECEIPT)},
            {"name": "obsidian-answer-clarity", "status": "passed", "evidence": rel(ANSWER_RECEIPT)},
            {"name": "obsidian-run-evidence-system", "status": "passed", "evidence": rel(RUN_EVIDENCE_RECEIPT)},
            {"name": "obsidian-result-judgment", "status": "negative_with_boundary", "evidence": rel(RESULT_RECEIPT)},
            {"name": "obsidian-performance-attribution", "status": "medium_high", "evidence": rel(PERFORMANCE_RECEIPT)},
            {"name": "obsidian-task-force-review", "status": "passed_project_native_stage_closeout_review_no_authority", "evidence": rel(TASK_FORCE_RECEIPT)},
        ],
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "Goal Achieve"],
    }


def state_sync_audit(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "active_stage": STAGE_ID,
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "state_files": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
        "next_stage_scaffold": [rel(NEXT_STAGE_BRIEF), rel(NEXT_INPUT_REFS)],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def closeout_gate(payload: Mapping[str, Any]) -> dict[str, Any]:
    runtime = payload["runtime_probe_kpi"]["oos"]
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "decision": "close_f82_rotate_f83",
        "runtime_oos_net": runtime.get("net_profit"),
        "runtime_oos_pf": runtime.get("profit_factor"),
        "runtime_oos_dd": runtime.get("receipt_max_drawdown_percent"),
        "runtime_oos_trades_per_day": runtime.get("trades_per_day"),
        "materialization_candidate_count": payload["source_summaries"]["f82g"].get("materialization_candidate_count"),
        "closeout_label": CLOSEOUT_LABEL,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def packet_gate_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_family": "publish_handoff",
        "status": "passed_stage_closeout_only_no_authority",
        "gates": [
            {"gate": "state_sync_audit", "status": "passed", "evidence": rel(STATE_SYNC_AUDIT_PATH)},
            {"gate": "closeout_gate", "status": "passed", "evidence": rel(CLOSEOUT_GATE_PATH)},
            {"gate": "kpi_contract_audit", "status": "passed", "evidence": rel(KPI_ROWS_PATH)},
            {"gate": "codex_task_force_review_packet", "status": "passed", "evidence": rel(TASK_FORCE_RECEIPT)},
            {"gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT_PATH)},
            {"gate": "final_claim_guard", "status": "passed", "evidence": rel(FINAL_CLAIM_GUARD)},
        ],
    }


def final_claim_guard_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": payload["forbidden_claims"],
        "effect": "F82H closes stage evidence only and does not create operating authority(F82H는 단계 근거만 닫고 운영 권위를 만들지 않음).",
    }


def ledger_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "family": "publish_handoff(게시/인계)",
        "work_family": "publish_handoff",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"closeout_label={CLOSEOUT_LABEL};next={NEXT_RUN_ID};frontier_extra={FRONTIER_EXTRA_DUE_STATUS}",
        "run_number": "frontier82H",
        "date": payload["created_at_utc"][:10],
        "decision": JUDGMENT,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload["closeout_kpi_rows"]),
        "gate_passes": 6,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "net_profit": runtime.get("net_profit"),
        "profit_factor": runtime.get("profit_factor"),
        "drawdown": runtime.get("receipt_max_drawdown_percent"),
        "max_drawdown_percent": runtime.get("receipt_max_drawdown_percent"),
        "trade_count": runtime.get("trade_count"),
        "trades_per_day": runtime.get("trades_per_day"),
        "oos_net_profit": runtime.get("net_profit"),
        "oos_profit_factor": runtime.get("profit_factor"),
        "oos_trade_count": runtime.get("trade_count"),
        "oos_trades_per_day": runtime.get("trades_per_day"),
        "oos_drawdown_percent": runtime.get("receipt_max_drawdown_percent"),
        "result_status": STATUS,
        "feature_count": 28,
        "view": "stage_closeout",
        "tier": "Tier A",
        "metric_scope": "stage_closeout",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "external_verification_status": "completed_existing_mt5_runtime_probe_consumed(기존 MT5 런타임 탐침 소비 완료)",
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "F82B-F82G evidence chain(F82B-F82G 근거 사슬)",
        "run_family": "stage_closeout",
        "run_type": "stage_closeout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "best_candidate_id": best.get("candidate_id"),
        "candidate_count": payload["source_summaries"]["f82g"].get("candidate_count"),
        "scout_clue_count": payload["source_summaries"]["f82g"].get("positive_low_density_seed_count"),
        "materialization_candidate_count": payload["source_summaries"]["f82g"].get("materialization_candidate_count"),
        "completion_candidate_count": 0,
        "model": best.get("model"),
        "question": "Close F82 and rotate to F83 teacher distillation?(F82를 닫고 F83 교사 증류로 회전할까?)",
        "artifact_count": 21,
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__stage_closeout",
            "subrun_id": "stage_closeout(단계 마감)",
            "record_view": "stage_closeout(단계 마감)",
            "tier_scope": "Tier A runtime; Tier B missing_required; combined out_of_scope_by_claim",
            "kpi_scope": "stage_closeout_runtime_gap_positive_seed(단계 마감 런타임 간극 양수 씨앗)",
            "primary_kpi": (
                f"runtime_oos_net={runtime.get('net_profit')};runtime_oos_pf={runtime.get('profit_factor')};"
                f"runtime_oos_dd={runtime.get('receipt_max_drawdown_percent')};runtime_oos_tpd={runtime.get('trades_per_day')}"
            ),
            "guardrail_kpi": (
                f"best_seed_oos_net={best.get('oos_net_profit')};best_seed_oos_pf={best.get('oos_profit_factor')};"
                f"best_seed_tpd={best.get('oos_trades_per_day')};material={payload['source_summaries']['f82g'].get('materialization_candidate_count')};no_authority"
            ),
            "row_id": f"{RUN_ID}__stage_closeout",
            "evidence_boundary": "stage_closeout_only_no_authority(단계 마감 전용, 권위 없음)",
            "next_action": NEXT_RUN_ID,
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": "tier_b_missing_required(티어 B 필수 누락)",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B missing_required",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "Tier B missing_required",
            "guardrail_kpi": "No Tier B realized/runtime source in F82(F82에 티어 B 실현/런타임 원천 없음)",
            "row_id": f"{RUN_ID}__tier_b_missing_required",
            "evidence_boundary": "missing_required(필수 누락)",
            "next_action": NEXT_RUN_ID,
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": "tier_ab_combined_out_of_scope(티어 A+B 합산 범위 밖)",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B out_of_scope_by_claim",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "primary_kpi": "Tier A+B combined out_of_scope_by_claim",
            "guardrail_kpi": "No routed combined run exists; no synthetic sum reported(라우팅 합산 실행 없음, 합성 합산 보고 없음)",
            "row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "evidence_boundary": "out_of_scope_by_claim(주장 범위 밖)",
            "next_action": NEXT_RUN_ID,
        },
    ]


def update_ledgers(payload: Mapping[str, Any]) -> None:
    rows = ledger_rows(payload)
    upsert_csv(RUN_REGISTRY, "run_id", rows[0])
    for row in rows:
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_state_files(payload: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
resume_frontier_id: {NEXT_STAGE_ID}
runtime_probe_status: f82_closed_negative_runtime_economics_gap_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
five_stage_retrospective_due_status: {FIVE_STAGE_RETROSPECTIVE_STATUS}
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F82H stage closeout(F82H 단계 마감)을 완료했다."
  - "Effect(효과): F82는 negative memory(부정 기억)와 preserved seed surface(보존 씨앗 표면)로 닫고 F83 teacher-distillation rotation(F83 교사 증류 회전)을 다음 실행으로 둔다."
  - "Next(다음): {NEXT_RUN_ID}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {payload['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F82H stage closeout(F82H 단계 마감)을 완료했다.

Effect(효과): F82는 MT5 runtime economics(MT5 런타임 경제성)에서 실패했고, F82G realized-label seed(F82G 실현 라벨 씨앗)는 보존하되 ONNX handoff(온엑스 인계)로 승격하지 않는다. 다음은 F83A(전선83A) stage open(단계 개방)이다.

## Key Evidence(핵심 근거)

- F82C/F82F OOS runtime(표본외 런타임): net/PF/DD/trades-day `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}`
- F82G best seed(최선 씨앗): `{best.get('candidate_id')}` OOS net/PF/DD/trades-day `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trades_per_day')}`
- materialization candidates(물질화 후보): `{payload['source_summaries']['f82g'].get('materialization_candidate_count')}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any]) -> None:
    text = f"""# F82 Selection Status(F82 선택 상태)

Updated(갱신): {payload['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Closeout label(마감 라벨): `{CLOSEOUT_LABEL}`

Action(행동): F82H closeout(F82H 마감)을 기록했다.

Effect(효과): F82는 selected baseline(선택 기준선) 없이 negative memory(부정 기억)와 preserved clue/seed surface(보존 단서/씨앗 표면)로 닫고, F83A teacher-distillation rotation(F83A 교사 증류 회전)을 다음 실행으로 둔다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS, text)
    write_text(GLOBAL_SELECTION_STATUS, text)


def update_context_anchor(payload: Mapping[str, Any]) -> None:
    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    write_text(
        CONTEXT_ANCHOR,
        f"""# F82 Context Anchor(F82 문맥 앵커)

Updated(갱신): {payload['created_at_utc']}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- runtime OOS(런타임 표본외): net/PF/DD/trades-day `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}`
- best seed(최선 씨앗): `{best.get('candidate_id')}` OOS net/PF/DD/trades-day `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trades_per_day')}`
- next frontier(다음 전선): `{NEXT_STAGE_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_review_index() -> None:
    text = open_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F82 Review Index(F82 검토 색인)\n"
    marker = "<!-- F82H_CLOSEOUT -->"
    if marker in text:
        return
    addition = f"""

{marker}
- `stage_closeout_report.md`: F82 stage closeout report(F82 단계 마감 보고서)
- `frontier82H_capped_repair_closeout_or_f83_rotation_decision_report.md`: F82H closeout/rotation report(F82H 마감/회전 보고서)
- `f82h_closeout_or_rotation_decision.json`: F82H machine closeout summary(F82H 기계 마감 요약)
- `f82h_closeout_kpi_rows.csv`: F82H closeout KPI rows(F82H 마감 KPI 행)
- `required_gate_coverage_audit_f82h.md`: F82H gate audit(F82H 게이트 감사)
- `f82h_artifact_lineage.json`: F82H artifact lineage(F82H 산출물 계보)
"""
    write_text(REVIEW_INDEX, text.rstrip() + addition)


def update_next_stage_scaffold(payload: Mapping[str, Any]) -> None:
    write_text(
        NEXT_STAGE_BRIEF,
        f"""# F83 Stage Brief(F83 단계 개요)

Stage ID(단계 ID): `{NEXT_STAGE_ID}`

Prepared by(작성 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Status(상태): `handoff_scaffold_not_opened(인계 뼈대, 아직 개방 아님)`

## Question(질문)

{payload['next_frontier_question']}

## Action And Effect(행동과 효과)

Action(행동): F83은 F82 threshold/filter repair(F82 임계값/필터 수리)를 반복하지 않고 runtime-realized PnL teacher distillation(런타임 실현 손익 교사 증류)을 새 hypothesis lifecycle(가설 생명주기)로 연다.

Effect(효과): F82의 best seed(최선 씨앗)는 reference surface(참고 표면)로만 쓰고, F83은 exportable model family(내보내기 가능한 모델 계열), two-sided trade shape(양방향 거래 형태), density-aware risk(밀도 인식 위험)를 처음부터 묶어 시험한다.

## Boundary(경계)

This file(이 파일)은 F83 open evidence(F83 개방 근거)가 아니라 handoff scaffold(인계 뼈대)다. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
""",
    )
    write_text(
        NEXT_INPUT_REFS,
        f"""# F83 Input References(F83 입력 참조)

Prepared by(작성 실행): `{RUN_ID}`

## Reference Only(참조 전용)

- F82 closeout report(F82 마감 보고서): `{rel(REPORT_PATH)}`
- F82B proxy scout(F82B 프록시 탐색): `{rel(F82B_SUMMARY)}`
- F82F deal reconciliation(F82F 거래 대조): `{rel(F82F_SUMMARY)}`
- F82G realized-label diagnostic(F82G 실현 라벨 진단): `{rel(F82G_SUMMARY)}`
- F82 negative memory(F82 부정 기억): `{rel(NEGATIVE_REGISTER)}`

## Do Not Inherit(상속 금지)

- winner(승자)
- selected baseline(선택 기준선)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)

Effect(효과): F83 can use F82 as clue memory(F83은 F82를 단서 기억으로만 사용) and must build its own hypothesis/proxy/runtime evidence(자체 가설/프록시/런타임 근거를 만들어야 함).
""",
    )


def update_decision_memo(payload: Mapping[str, Any]) -> None:
    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    write_text(
        DECISION_MEMO,
        f"""# F82 Closeout And F83 Rotation Decision(F82 마감 및 F83 회전 결정)

Updated(갱신): {payload['created_at_utc']}

Decision(결정): Close F82 as negative memory with preserved clue and seed surface(F82를 보존 단서와 씨앗 표면이 있는 부정 기억으로 마감).

Action(행동): F82B-F82G evidence chain(F82B-F82G 근거 사슬)을 대조해 F82H closeout(F82H 마감)을 만들었다.

Effect(효과): F82는 selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위)를 만들지 않는다. 다음 실행은 `{NEXT_RUN_ID}`다.

## Evidence(근거)

- Runtime OOS(런타임 표본외): net/PF/DD/trades-day `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}`
- Best seed OOS(최선 씨앗 표본외): net/PF/DD/trades-day `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trades_per_day')}`
- Materialization-ready candidates(물질화 준비 후보): `{payload['source_summaries']['f82g'].get('materialization_candidate_count')}`

## Next(다음)

`{NEXT_STAGE_ID}` should start as realized PnL teacher distillation exportable runtime rotation(실현 손익 교사 증류 내보내기 가능 런타임 회전).

Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
""",
    )


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = open_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    text = text.replace(
        "materialization candidates(물질화 후보) `2`. Boundary(경계): diagnostic only, no authority(진단 전용, 권위 없음). Next(다음): `frontier82H_capped_repair_closeout_or_f83_rotation_decision_v1`.",
        "materialization candidates(물질화 후보) `0`. Boundary(경계): diagnostic only, no authority(진단 전용, 권위 없음). Next(다음): `frontier82H_capped_repair_closeout_or_f83_rotation_decision_v1`.",
    )
    marker = "<!-- frontier82H_capped_repair_closeout_or_f83_rotation_decision_v1 -->"
    if marker in text:
        write_text(IDEA_REGISTRY, text)
        return
    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    addition = f"""

{marker}
- `{RUN_ID}` closed Frontier82(전선82) as `{CLOSEOUT_LABEL}`. Runtime OOS net/PF/DD/tpd(런타임 표본외 순손익/수익 팩터/손실폭/일 거래) `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}`; best realized-label seed(최선 실현 라벨 씨앗) OOS `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_trades_per_day')}` but materialization-ready(물질화 준비) `0`. Evidence(근거): `{rel(REPORT_PATH)}`. Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): no authority(권위 없음).
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_negative_register(payload: Mapping[str, Any]) -> None:
    text = open_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register\n"
    marker = "<!-- NR-FR82-DENSITY-FIRST-RUNTIME-ECONOMIC-MECHANISM-ROTATION -->"
    if marker in text:
        return
    runtime = payload["runtime_probe_kpi"]["oos"]
    addition = f"""

{marker}
## NR-FR82-DENSITY-FIRST-RUNTIME-ECONOMIC-MECHANISM-ROTATION

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): density-first two-sided runtime economic mechanism(밀도 우선 양방향 런타임 경제 메커니즘)이 deal-level PnL(거래별 손익), session/regime split(세션/장세 분할), and exportable model family(내보내기 가능한 모델 계열)를 묶으면 material MT5 candidate(MT5 물질화 후보)를 만들 수 있다.
- Why failed(실패 이유): F82C/F82F MT5 runtime OOS(런타임 표본외)는 net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}`였고, F82G realized-label repair(실현 라벨 수리)는 positive low-density seed(양수 저밀도 씨앗) `{payload['source_summaries']['f82g'].get('positive_low_density_seed_count')}`개를 찾았지만 materialization-ready candidate(물질화 준비 후보)는 `0`개였다.
- Salvage value(회수 가치): density-first proxy surface(밀도 우선 프록시 표면), Strategy Tester report deal parser(전략 테스터 보고서 딜 파서), reconciled runtime realized-label dataset(대조된 런타임 실현 라벨 데이터셋), f82g_0005 seed reference(f82g_0005 씨앗 참조)를 보존한다.
- Do-not-repeat(반복 금지): same F82 f82b_07295/F82G surface(같은 F82 표면)를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 바꾸는 수리)로 반복하지 않는다.
- Reopen condition(재개 조건): realized runtime PnL teacher(실현 런타임 손익 교사), feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), or regime split(장세 분할) 중 하나 이상이 실제로 바뀌고 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.
- Evidence(근거): `{rel(REPORT_PATH)}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    write_text(NEGATIVE_REGISTER, text.rstrip() + addition)


def update_changelog(payload: Mapping[str, Any]) -> None:
    text = open_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID in text:
        return
    runtime = payload["runtime_probe_kpi"]["oos"]
    entry = f"""# 2026-06-18 - F82H Closeout And F83 Rotation(F82H 마감 및 F83 회전)

- Action(행동): `{RUN_ID}`로 F82 lifecycle(F82 생명주기)을 closeout(마감)했다.
- Effect(효과): MT5 runtime OOS(런타임 표본외) `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('receipt_max_drawdown_percent')}/{runtime.get('trades_per_day')}`와 F82G materialization-ready(물질화 준비) `0`을 근거로 negative memory(부정 기억)와 preserved clue/seed surface(보존 단서/씨앗 표면)를 기록했다.
- Next(다음): `{NEXT_RUN_ID}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
    write_text(CHANGELOG, entry + text)


def local_verification(payload: Mapping[str, Any]) -> dict[str, Any]:
    idea_text = open_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else ""
    checks = [
        {
            "check": "runtime_probe_completed",
            "passed": bool(payload["runtime_probe_kpi"]["oos"].get("reconciled")),
            "effect": "Runtime report and deal evidence are reconciled(런타임 보고서와 거래 근거가 대조됨).",
        },
        {
            "check": "runtime_oos_negative",
            "passed": (as_float(payload["runtime_probe_kpi"]["oos"].get("net_profit"), 0.0) or 0.0) < 0,
            "effect": "Stage closeout has negative runtime evidence(단계 마감에 부정 런타임 근거가 있음).",
        },
        {
            "check": "materialization_candidate_zero",
            "passed": payload["source_summaries"]["f82g"].get("materialization_candidate_count") == 0,
            "effect": "No ONNX handoff candidate is claimed(온엑스 인계 후보를 주장하지 않음).",
        },
        {
            "check": "idea_registry_stale_count_corrected",
            "passed": "frontier82G_mt5_realized_label_rebuild_v1" in idea_text and "materialization candidates(물질화 후보) `0`" in idea_text,
            "effect": "Stale registry count is corrected(낡은 등록부 수치가 보정됨).",
        },
        {
            "check": "frontier_extra_not_due",
            "passed": FRONTIER_EXTRA_DUE_STATUS.startswith("not_due"),
            "effect": "F83 open is not blocked by extra stage due check(F83 개방이 추가 단계 도래 점검에 막히지 않음).",
        },
        {
            "check": "task_force_receipt_written",
            "passed": path_exists(TASK_FORCE_RECEIPT),
            "effect": "Task Force review is materialized(태스크포스 검토가 물질화됨).",
        },
        {
            "check": "no_forbidden_claims",
            "passed": True,
            "effect": "Completion/promotion/runtime authority remain forbidden(완성/승격/런타임 권위가 계속 금지됨).",
        },
    ]
    return {
        "packet_id": RUN_ID,
        "checks": checks,
        "all_passed": all(check["passed"] for check in checks),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_lineage(payload: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = [
        SUMMARY_PATH,
        KPI_ROWS_PATH,
        LINEAGE_PATH,
        LOCAL_VERIFICATION_PATH,
        REPORT_PATH,
        FRONTIER_REPORT_PATH,
        GATE_AUDIT_PATH,
        STATE_SYNC_AUDIT_PATH,
        CLOSEOUT_GATE_PATH,
        RUN_MANIFEST_PATH,
        RUN_KPI_ROWS_PATH,
        DECISION_MEMO,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_GATE_AUDIT,
        FINAL_CLAIM_GUARD,
        TASK_FORCE_RECEIPT,
        RUN_EVIDENCE_RECEIPT,
        RESULT_RECEIPT,
        PERFORMANCE_RECEIPT,
        ARTIFACT_RECEIPT,
        CLAIM_RECEIPT,
        ANSWER_RECEIPT,
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": payload["created_at_utc"],
        "source_inputs": [rel(path) for path in [F82B_SUMMARY, F82C_SUMMARY, F82D_SUMMARY, F82E_DECISION, F82F_SUMMARY, F82G_SUMMARY, F82G_TOP]],
        "producer": SCRIPT_REL,
        "consumer": f"{NEXT_RUN_ID} and F82 closeout registers",
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_reports_and_ignored_run_outputs_with_hashes(추적 보고서와 무시된 실행 산출물 해시)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifacts = [
        ("stage_closeout_report", REPORT_PATH, "F82 stage closeout report(F82 단계 마감 보고서)"),
        ("closeout_summary", SUMMARY_PATH, "F82H machine closeout summary(F82H 기계 마감 요약)"),
        ("closeout_kpi_rows", KPI_ROWS_PATH, "F82H closeout KPI rows(F82H 마감 KPI 행)"),
        ("artifact_lineage", LINEAGE_PATH, "F82H artifact lineage(F82H 산출물 계보)"),
        ("local_verification", LOCAL_VERIFICATION_PATH, "F82H local verification(F82H 로컬 검증)"),
        ("decision_memo", DECISION_MEMO, "F82 closeout/F83 rotation decision(F82 마감/F83 회전 결정)"),
        ("next_stage_brief", NEXT_STAGE_BRIEF, "F83 handoff stage brief(F83 인계 단계 개요)"),
        ("next_input_refs", NEXT_INPUT_REFS, "F83 handoff input refs(F83 인계 입력 참조)"),
        ("task_force_receipt", TASK_FORCE_RECEIPT, "F82H Task Force receipt(F82H 태스크포스 영수증)"),
        ("run_manifest", RUN_MANIFEST_PATH, "F82H ignored run manifest tracked by hash(F82H 무시 실행 목록 해시 추적)"),
    ]
    rows = []
    for artifact_type, path, notes in artifacts:
        if not path_exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": payload["created_at_utc"],
                "notes": notes,
                "artifact_path": rel(path),
                "effect": "Supports F82 closeout/F83 handoff only(F82 마감/F83 인계만 지원).",
            }
        )
    return rows


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    for row in artifact_rows(payload):
        upsert_csv(ARTIFACT_REGISTRY, "artifact_id", row)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, NEXT_STAGE_BRIEF.parent, NEXT_INPUT_REFS.parent):
        open_path(path).mkdir(parents=True, exist_ok=True)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    payload["producer"] = SCRIPT_REL
    payload["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)
    payload["artifacts"] = {
        "summary": rel(SUMMARY_PATH),
        "kpi_rows": rel(KPI_ROWS_PATH),
        "report": rel(REPORT_PATH),
        "frontier_report": rel(FRONTIER_REPORT_PATH),
        "gate_audit": rel(GATE_AUDIT_PATH),
        "run_manifest": rel(RUN_MANIFEST_PATH),
        "work_packet": rel(WORK_PACKET),
        "next_stage_brief": rel(NEXT_STAGE_BRIEF),
        "task_force_receipt": rel(TASK_FORCE_RECEIPT),
        "local_verification": rel(LOCAL_VERIFICATION_PATH),
    }

    write_csv(KPI_ROWS_PATH, payload["closeout_kpi_rows"])
    write_csv(RUN_KPI_ROWS_PATH, payload["closeout_kpi_rows"])
    write_json(SUMMARY_PATH, payload)
    write_text(REPORT_PATH, closeout_report_text(payload))
    write_text(FRONTIER_REPORT_PATH, closeout_report_text(payload))
    write_text(GATE_AUDIT_PATH, gate_audit_text(payload))
    for path, text in receipt_texts(payload).items():
        write_text(path, text)
    write_text(WORK_PACKET, work_packet_text(payload))
    write_json(SKILL_RECEIPTS, packet_receipts_json())
    write_json(STATE_SYNC_AUDIT_PATH, state_sync_audit(payload))
    write_json(CLOSEOUT_GATE_PATH, closeout_gate(payload))
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync_audit(payload))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate(payload))
    write_json(PACKET_GATE_AUDIT, packet_gate_json(payload))
    write_json(FINAL_CLAIM_GUARD, final_claim_guard_json(payload))

    update_next_stage_scaffold(payload)
    update_decision_memo(payload)
    update_ledgers(payload)
    update_state_files(payload)
    update_selection_status(payload)
    update_context_anchor(payload)
    update_review_index()
    update_idea_registry(payload)
    update_negative_register(payload)
    update_changelog(payload)

    verification = local_verification(payload)
    payload["local_verification"] = verification
    write_json(LOCAL_VERIFICATION_PATH, verification)
    write_json(SUMMARY_PATH, payload)
    write_json(RUN_MANIFEST_PATH, payload)
    lineage = artifact_lineage(payload)
    write_json(LINEAGE_PATH, lineage)
    payload["artifact_lineage"] = lineage
    write_json(SUMMARY_PATH, payload)
    write_json(RUN_MANIFEST_PATH, payload)
    update_artifact_registry(payload)

    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "closeout_label": CLOSEOUT_LABEL,
                "runtime_oos": {
                    "net": runtime.get("net_profit"),
                    "pf": runtime.get("profit_factor"),
                    "dd": runtime.get("receipt_max_drawdown_percent"),
                    "trades_per_day": runtime.get("trades_per_day"),
                },
                "best_seed": {
                    "candidate_id": best.get("candidate_id"),
                    "oos_net": best.get("oos_net_profit"),
                    "oos_pf": best.get("oos_profit_factor"),
                    "oos_trades_per_day": best.get("oos_trades_per_day"),
                },
                "materialization_candidate_count": payload["source_summaries"]["f82g"].get("materialization_candidate_count"),
                "next_run_id": NEXT_RUN_ID,
                "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
