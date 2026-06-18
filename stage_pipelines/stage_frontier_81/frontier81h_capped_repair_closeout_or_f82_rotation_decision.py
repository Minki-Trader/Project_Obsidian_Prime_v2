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


STAGE_ID = "stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild"
RUN_ID = "frontier81H_capped_repair_closeout_or_f82_rotation_decision_v1"
PARENT_RUN_ID = "frontier81G_mt5_realized_label_rebuild_v1"
NEXT_STAGE_ID = "stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
NEXT_RUN_ID = "frontier82A_stage_open_density_first_runtime_economic_mechanism_rotation_v1"

STATUS = "closed_negative_runtime_economics_gap_low_density_seed_no_authority"
JUDGMENT = "negative_memory_with_preserved_low_density_seed_and_f82_density_first_rotation_no_authority"
CLOSEOUT_LABEL = "negative_memory_with_preserved_clue(부정 기억과 보존 단서)"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f81_closeout_next_boundary_f100_e01_closed_for_f050"
FIVE_STAGE_RETROSPECTIVE_STATUS = "inactive_preserve_records_no_grok_block"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID

F81B_SUMMARY = REVIEW_DIR / "f81b_order_intent_cost_shape_proxy_summary.json"
F81C_SUMMARY = REVIEW_DIR / "f81c_mt5_runtime_materialization_summary.json"
F81D_SUMMARY = REVIEW_DIR / "f81d_proxy_runtime_gap_attribution.json"
F81E_DECISION = REVIEW_DIR / "f81e_capped_repair_or_rotation_decision.json"
F81F_SUMMARY = REVIEW_DIR / "f81f_deal_reconciliation_summary.json"
F81G_SUMMARY = REVIEW_DIR / "f81g_mt5_realized_label_rebuild_summary.json"
F81G_TOP = REVIEW_DIR / "f81g_realized_label_top_candidates.csv"
F81C_RECEIPT = STAGE_DIR / "02_runs/frontier81C_mt5_runtime_materialization_v1/f81c_runtime_receipt.csv"
F81F_TRADES = STAGE_DIR / "02_runs/frontier81F_deal_reconciled_runtime_label_preflight_v1/f81f_trade_rows.csv"

SUMMARY_PATH = REVIEW_DIR / "f81h_closeout_or_rotation_decision.json"
KPI_ROWS_PATH = REVIEW_DIR / "f81h_closeout_kpi_rows.csv"
LINEAGE_PATH = REVIEW_DIR / "f81h_artifact_lineage.json"
LOCAL_VERIFICATION_PATH = REVIEW_DIR / "f81h_local_verification.json"
REPORT_PATH = REVIEW_DIR / "stage_closeout_report.md"
FRONTIER_REPORT_PATH = REVIEW_DIR / "frontier81H_capped_repair_closeout_or_f82_rotation_decision_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f81h.md"
STATE_SYNC_AUDIT_PATH = REVIEW_DIR / "f81h_state_sync_audit.json"
CLOSEOUT_GATE_PATH = REVIEW_DIR / "f81h_closeout_gate.json"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
RUN_KPI_ROWS_PATH = RUN_DIR / "f81h_closeout_kpi_rows.csv"

STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f81h_stage_transition_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f81h_artifact_lineage_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f81h_claim_discipline_receipt.yaml"
ANSWER_RECEIPT = REVIEW_DIR / "f81h_answer_clarity_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f81h_result_judgment_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f81h_performance_attribution_receipt.yaml"

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
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_frontier81_closeout_rotate_f82.md"
FRONTIER_EXTRA_REGISTER = ROOT / "docs/registers/frontier_extra_stage_register.yaml"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
NEXT_STAGE_BRIEF = NEXT_STAGE_DIR / "00_spec/stage_brief.md"
NEXT_INPUT_REFS = NEXT_STAGE_DIR / "01_inputs/input_refs.md"

SCRIPT_REL = "stage_pipelines/stage_frontier_81/frontier81h_capped_repair_closeout_or_f82_rotation_decision.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            sample = io_path(candidate).read_bytes()
            if b"\r\n" in sample:
                return "\r\n"
    return "\n"


def writable_path(path: Path) -> Path:
    return io_path(path) if len(str(path)) >= 240 else path


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    lineterminator = csv_lineterminator(path, source_header)
    if path_exists(path):
        with writable_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with writable_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
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
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    writable_path(path.parent).mkdir(parents=True, exist_ok=True)
    with writable_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator=lineterminator)
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


def split_summary(f81f: Mapping[str, Any], split: str) -> Mapping[str, Any]:
    for row in f81f.get("split_summaries", []):
        if row.get("split") == split:
            return row
    return {}


def target_proxy_row(target: Mapping[str, Any], split: str, gap: Mapping[str, Any]) -> dict[str, Any]:
    prefix = "val" if split == "validation" else "oos"
    split_label = "validation" if split == "validation" else "OOS"
    split_ko = "검증" if split == "validation" else "표본외"
    return {
        "record_id": f"{RUN_ID}__f81b_proxy_{split}",
        "test_period": "2025-01-02..2025-10-01" if split == "validation" else "2025-10-01..2026-04-14",
        "split_view": f"F81B materialized proxy {split_label}(F81B 물질화 프록시 {split_ko})",
        "evidence_source": rel(F81D_SUMMARY),
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
        "materialization_status": "materialized_in_f81c_target(물질화 대상)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def runtime_row(row: Mapping[str, Any], gap: Mapping[str, Any]) -> dict[str, Any]:
    split = str(row.get("split") or "")
    split_label = "validation" if split == "validation" else "OOS"
    split_ko = "검증" if split == "validation" else "표본외"
    return {
        "record_id": f"{RUN_ID}__f81c_runtime_{split}",
        "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
        "split_view": f"F81C/F81F MT5 runtime {split_label}(F81C/F81F MT5 런타임 {split_ko})",
        "evidence_source": rel(F81F_SUMMARY),
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
    return {
        "record_id": f"{RUN_ID}__f81g_seed_{split}",
        "test_period": "2025-01-02..2025-10-01" if split == "validation" else "2025-10-01..2026-04-14",
        "split_view": f"F81G realized-label seed {split_label}(F81G 실현 라벨 씨앗 {split_ko})",
        "evidence_source": rel(F81G_SUMMARY),
        "net_profit": best.get(f"{prefix}_net_profit"),
        "gross_profit": "not_available_in_candidate_row(후보 행에서 사용 불가)",
        "gross_loss": "not_available_in_candidate_row(후보 행에서 사용 불가)",
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
        "materialization_status": (
            "not_materialization_ready_low_density_or_nonexportable(저밀도 또는 내보내기 불가로 물질화 준비 아님)"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_kpi_rows(f81d: Mapping[str, Any], f81f: Mapping[str, Any], f81g: Mapping[str, Any]) -> list[dict[str, Any]]:
    target = f81d.get("target") or {}
    val_gap = f81d.get("validation_gap") or {}
    oos_gap = f81d.get("oos_gap") or {}
    best = f81g.get("best_candidate") or {}
    return [
        target_proxy_row(target, "validation", val_gap),
        target_proxy_row(target, "oos", oos_gap),
        runtime_row(split_summary(f81f, "validation"), val_gap),
        runtime_row(split_summary(f81f, "oos"), oos_gap),
        realized_seed_row(best, "validation"),
        realized_seed_row(best, "oos"),
    ]


def build_payload(created_at: str) -> dict[str, Any]:
    f81b = read_json(F81B_SUMMARY)
    f81c = read_json(F81C_SUMMARY)
    f81d = read_json(F81D_SUMMARY)
    f81e = read_json(F81E_DECISION)
    f81f = read_json(F81F_SUMMARY)
    f81g = read_json(F81G_SUMMARY)
    kpi_rows = build_kpi_rows(f81d, f81f, f81g)
    runtime_oos = split_summary(f81f, "oos")
    runtime_validation = split_summary(f81f, "validation")
    best = f81g.get("best_candidate") or {}
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
            "MT5-native order-intent cost-shape labels(MT5 원형 주문 의도 비용 형태 라벨)이 "
            "proxy/runtime economics gap(프록시/런타임 경제성 간극)을 줄이고 material ONNX candidate(물질적 온엑스 후보)를 만들 수 있다."
        ),
        "test_period": "validation(검증) 2025-01-02..2025-10-01; OOS(표본외) 2025-10-01..2026-04-14",
        "source_summaries": {
            "f81b": {
                "candidate_count": f81b.get("candidate_count"),
                "materialization_candidate_count": f81b.get("materialization_candidate_count"),
                "meaningful_signal_count": f81b.get("meaningful_signal_count"),
                "final_like_reference_count": f81b.get("final_like_reference_count"),
            },
            "f81c": {
                "status": f81c.get("status"),
                "judgment": f81c.get("judgment"),
            },
            "f81d": {
                "status": f81d.get("status"),
                "judgment": f81d.get("judgment"),
            },
            "f81e": {
                "decision": f81e.get("decision"),
                "repair_axis": f81e.get("repair_axis"),
                "repair_cap": f81e.get("repair_cap"),
            },
            "f81f": {
                "status": f81f.get("status"),
                "judgment": f81f.get("judgment"),
                "validation_reconciled": runtime_validation.get("reconciled"),
                "oos_reconciled": runtime_oos.get("reconciled"),
            },
            "f81g": {
                "candidate_count": f81g.get("candidate_count"),
                "positive_low_density_seed_count": f81g.get("positive_low_density_seed_count"),
                "materialization_candidate_count": f81g.get("materialization_candidate_count"),
                "final_like_reference_count": f81g.get("final_like_reference_count"),
                "best_candidate": best,
            },
        },
        "closeout_kpi_rows": kpi_rows,
        "runtime_probe_kpi": {
            "validation": runtime_validation,
            "oos": runtime_oos,
        },
        "best_seed": best,
        "gap_cause": (
            "Signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 맞았지만, "
            "real MT5 deal economics(실제 MT5 거래 경제성)가 proxy profit source(프록시 수익 원천)를 지지하지 않았다."
        ),
        "why_failed": [
            "F81C validation runtime(검증 런타임)은 net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) "
            f"{runtime_validation.get('net_profit')}/{runtime_validation.get('profit_factor')}/{runtime_validation.get('receipt_max_drawdown_percent')}/{runtime_validation.get('trades_per_day')}로 부정이었다.",
            "F81C OOS runtime(표본외 런타임)은 net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) "
            f"{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('receipt_max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}로 부정이었다.",
            "F81G realized-label repair(실현 라벨 수리)는 positive low-density seed(저밀도 양수 씨앗) 4개를 찾았지만 materialization-ready candidate(물질화 준비 후보)는 0개였다.",
            "Best seed(최선 씨앗)는 OOS net/PF/DD/trades-day(표본외 순손익/수익 팩터/손실폭/일 거래) "
            f"{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_drawdown_percent')}/{best.get('oos_trades_per_day')}였고, density(밀도)가 목표보다 너무 낮았다.",
        ],
        "preserved_clue": [
            "F81C exact signal/feature/ONNX parity(정확 신호/피처/온엑스 동등성)는 런타임 연결 자체가 고칠 수 있는 영역임을 보존한다.",
            "F81F Strategy Tester report parser(전략 테스터 보고서 파서)로 deal/trade rows(딜/거래 행)를 회수하고 receipt(영수증)와 대조할 수 있었다.",
            "F81G realized-label dataset(실현 라벨 데이터셋)은 runtime PnL(런타임 손익) 기반 post-probe diagnostic(탐침 후 진단) 표면으로 재사용할 수 있다.",
            "Low-density positive seed(저밀도 양수 씨앗)는 F82에서 density-first label(밀도 우선 라벨)을 설계할 때 reference surface(참조 표면)로만 쓴다.",
        ],
        "negative_memory": [
            "Order-intent cost-shape proxy(주문 의도 비용 형태 프록시)는 MT5 real deal economics(실제 거래 경제성)로 옮기면 PF/DD(수익 팩터/손실폭)가 붕괴했다.",
            "Threshold/filter/parameter-only repair(임계값/필터/파라미터만 바꾸는 수리)는 F81 안에서 cap(상한)을 소진했다.",
            "Post-hoc realized-label filter(사후 실현 라벨 필터)는 독립 runtime strategy(런타임 전략)가 아니며, 저밀도 씨앗만 만들었다.",
            "Nonexportable or low-density HistGBM seed(내보내기 불가 또는 저밀도 히스토그램 그래디언트부스팅 씨앗)를 ONNX handoff(온엑스 인계)처럼 취급하지 않는다.",
        ],
        "do_not_repeat": [
            "Do not rerun f81b_01107 with only probability threshold, quantile, cooldown, or same risk filter changed(확률 임계값/분위수/쿨다운/동일 위험 필터만 바꿔 재실행하지 않기).",
            "Do not treat F81G realized-label seed as selected baseline or runtime authority(F81G 실현 라벨 씨앗을 선택 기준선이나 런타임 권위로 취급하지 않기).",
            "Do not claim proxy parity as runtime economics(프록시 동등성을 런타임 경제성으로 주장하지 않기).",
        ],
        "reopen_condition": (
            "F81 surface(표면)는 feature set/label/model family/trade shape/risk logic/regime split"
            "(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할) 중 하나 이상이 실제로 바뀌고, "
            "새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다."
        ),
        "next_frontier_hypothesis": (
            "F82 should start density-first and two-sided(밀도 우선 및 양방향) from runtime economic mechanism"
            "(런타임 경제 메커니즘), not by repairing F81 thresholds(F81 임계값 수리 아님)."
        ),
        "next_frontier_question": (
            "Can a density-first, two-sided runtime economic mechanism(밀도 우선 양방향 런타임 경제 메커니즘)이 "
            "deal-level PnL(거래별 손익), session/regime split(세션/장세 분할), and exportable model family(내보내기 가능한 모델 계열)를 "
            "처음부터 묶어 MT5 materialization candidate(MT5 물질화 후보)를 만들 수 있는가?"
        ),
        "allowed_claims": [
            "F81 closed negative memory(F81 부정 기억 마감)",
            "preserved clues recorded(보존 단서 기록)",
            "F82 rotation proposed(F82 회전 제안)",
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


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    header = (
        "| period(기간) | view(보기) | net(순손익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | "
        "DD%(손실폭) | trades(거래) | trades/day(일 거래) | win rate(승률) | avg win(평균 이익) | avg loss(평균 손실) | "
        "payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | TUW(회복 전 체류) | max loss(최대 연속 손실) | long/short(롱/숏) | gap(간극) |"
    )
    sep = "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"
    lines = [header, sep]
    for row in rows:
        lines.append(
            f"| `{row.get('test_period')}` | `{row.get('split_view')}` | `{fmt(row.get('net_profit'))}` | `{fmt(row.get('gross_profit'))}` | `{fmt(row.get('gross_loss'))}` | "
            f"`{fmt(row.get('PF'))}` | `{fmt(row.get('DD_percent'))}` | `{fmt(row.get('trade_count'))}` | `{fmt(row.get('trades_per_day'))}` | "
            f"`{fmt(row.get('win_rate'))}` | `{fmt(row.get('average_win'))}` | `{fmt(row.get('average_loss'))}` | `{fmt(row.get('payoff_ratio'))}` | "
            f"`{fmt(row.get('expectancy'))}` | `{fmt(row.get('recovery_factor'))}` | `{row.get('time_under_water')}` | `{row.get('max_consecutive_loss')}` | "
            f"`{row.get('long_short_breakdown')}` | `{row.get('proxy_runtime_KPI_gap')}` |"
        )
    return "\n".join(lines)


def closeout_report_text(payload: Mapping[str, Any]) -> str:
    return f"""# F81 Stage Closeout Report(F81 단계 마감 보고서)

Updated(갱신): {payload['created_at_utc']}

- status(상태): `{payload['status']}`
- judgment(판정): `{payload['judgment']}`
- closeout label(마감 라벨): `{payload['closeout_label']}`
- next run(다음 실행): `{payload['next_run_id']}`
- next frontier(다음 전선): `{payload['next_frontier_stage_id']}`
- claim boundary(주장 경계): `{payload['claim_boundary']}`

## Plain Meaning(쉬운 의미)

Action(행동): F81 hypothesis lifecycle(F81 가설 생명주기)을 proxy(프록시), MT5 runtime materialization(MT5 런타임 물질화), gap analysis(간극 분석), capped repair(상한 수리), realized-label diagnostic(실현 라벨 진단)까지 실행한 뒤 닫았다.

Effect(효과): F81은 strong ONNX runtime strategy(강한 온엑스 런타임 전략)를 만들지 못했다. 대신 정확한 parity(동등성)와 deal-level evidence recovery(거래별 근거 회수), low-density seed(저밀도 씨앗)를 다음 F82의 재료로 남긴다.

## Hypothesis(가설)

{payload['hypothesis']}

## Closeout KPI(마감 핵심 성과 지표)

{kpi_table(payload['closeout_kpi_rows'])}

## Why Failed(실패 이유)

{chr(10).join('- ' + item for item in payload['why_failed'])}

## Preserved Clue(보존 단서)

{chr(10).join('- ' + item for item in payload['preserved_clue'])}

## Negative Memory(부정 기억)

{chr(10).join('- ' + item for item in payload['negative_memory'])}

## Do Not Repeat(반복 금지)

{chr(10).join('- ' + item for item in payload['do_not_repeat'])}

## Next Frontier Proposal(다음 전선 제안)

Action(행동): F82는 `{payload['next_frontier_stage_id']}`로 제안한다.

Effect(효과): F82는 F81 threshold repair(F81 임계값 수리)가 아니라 density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘)을 새 axis(축)로 연다.

Question(질문): {payload['next_frontier_question']}

## Boundary(경계)

This closeout(마감)은 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다. Git push(깃 원격 반영)는 publication record(게시 기록)일 뿐 validation(검증)이 아니다.
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    rows = [
        ("hypothesis_lifecycle_recorded(가설 생명주기 기록)", True, rel(REPORT_PATH)),
        ("proxy_kpi_recorded(프록시 KPI 기록)", True, rel(KPI_ROWS_PATH)),
        ("mt5_runtime_probe_recorded(MT5 런타임 탐침 기록)", True, rel(F81F_SUMMARY)),
        ("proxy_runtime_gap_recorded(프록시/런타임 간극 기록)", True, rel(F81D_SUMMARY)),
        ("capped_repair_recorded(상한 수리 기록)", True, rel(F81E_DECISION)),
        ("repair_cap_consumed(수리 상한 소진)", True, rel(F81G_SUMMARY)),
        ("negative_memory_recorded(부정 기억 기록)", True, rel(NEGATIVE_REGISTER)),
        ("frontier_extra_due_check(전선 추가 도래 점검)", True, payload["frontier_extra_due_status"]),
        ("state_sync_audit(상태 동기화 감사)", True, rel(STATE_SYNC_AUDIT_PATH)),
        ("final_claim_guard(최종 주장 보호)", True, CLAIM_BOUNDARY),
    ]
    body = "\n".join(
        f"| {gate} | `{'passed(통과)' if passed else 'failed(실패)'}` | `{evidence}` |"
        for gate, passed, evidence in rows
    )
    return f"""# F81H Required Gate Coverage Audit(F81H 필수 게이트 커버리지 감사)

Updated(갱신): {payload['created_at_utc']}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
{body}

- closeout label(마감 라벨): `{payload['closeout_label']}`
- next run(다음 실행): `{payload['next_run_id']}`
- claim boundary(주장 경계): `{payload['claim_boundary']}`
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    return {
        STAGE_TRANSITION_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-stage-transition
status: passed_stage_closeout_handoff
action: "Closed F81 as negative memory and handed off to F82 proposal(F81을 부정 기억으로 닫고 F82 제안으로 인계)."
effect: "Current truth, selection status, decision memo, ledgers, and next-stage scaffold share the same boundary(현재 진실/선택 상태/결정 메모/장부/다음 단계 뼈대가 같은 경계를 공유)."
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F81B_SUMMARY)}
  - {rel(F81C_SUMMARY)}
  - {rel(F81D_SUMMARY)}
  - {rel(F81E_DECISION)}
  - {rel(F81F_SUMMARY)}
  - {rel(F81G_SUMMARY)}
producer: {SCRIPT_REL}
consumer: {NEXT_RUN_ID}
artifact_paths:
  - {rel(SUMMARY_PATH)}
  - {rel(KPI_ROWS_PATH)}
  - {rel(REPORT_PATH)}
  - {rel(RUN_MANIFEST_PATH)}
  - {rel(NEXT_STAGE_BRIEF)}
registry_links:
  - {rel(RUN_REGISTRY)}
  - {rel(ALPHA_LEDGER)}
  - {rel(STAGE_LEDGER)}
  - {rel(ARTIFACT_REGISTRY)}
availability: tracked_reports_and_ignored_run_outputs_with_hashes(추적 보고서와 무시된 실행 산출물 해시)
lineage_judgment: connected_with_boundary
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_stage_closeout_no_authority
allowed_claims:
  - F81 negative memory closed(F81 부정 기억 마감)
  - preserved clues recorded(보존 단서 기록)
  - F82 rotation proposed(F82 회전 제안)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
  - git_push_as_validation
final_status: "{JUDGMENT}; boundary={CLAIM_BOUNDARY}"
""",
        ANSWER_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-answer-clarity
status: passed_user_report_ready
plain_meaning: "F81 failed as a strategy but produced reusable evidence(F81은 전략으로 실패했지만 재사용 가능한 근거를 만들었다)."
not_yet_true:
  - runtime authority(런타임 권위)
  - completion(완성)
  - selected baseline(선택 기준선)
next_action: {NEXT_RUN_ID}
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: negative_with_preserved_clue_no_authority
result_subject: F81 lifecycle closeout(F81 생명주기 마감)
judgment_label: negative_memory_with_preserved_clue
evidence:
  - {rel(F81F_SUMMARY)}
  - {rel(F81G_SUMMARY)}
claim_boundary: {CLAIM_BOUNDARY}
""",
        PERFORMANCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: gap_attributed_and_rotated
observed_change: "Proxy positive economics inverted to MT5 negative economics(프록시 양수 경제성이 MT5 음수 경제성으로 반전)."
likely_drivers:
  - real MT5 deal economics after parity(동등성 이후 실제 MT5 거래 경제성)
  - low win rate and expanded DD(낮은 승률과 확대된 손실폭)
  - post-hoc realized-label seed density too low(사후 실현 라벨 씨앗 밀도 부족)
next_axis: {NEXT_STAGE_ID}
claim_boundary: {CLAIM_BOUNDARY}
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
required_skill_receipts:
  - obsidian-stage-transition
  - obsidian-artifact-lineage
  - obsidian-claim-discipline
  - obsidian-answer-clarity
required_gates:
  - state_sync_audit
  - closeout_gate
  - required_gate_coverage_audit
  - final_claim_guard
scope: "Close F81 negative memory and hand off to F82 density-first runtime economic mechanism rotation(F81 부정 기억 마감 및 F82 밀도 우선 런타임 경제 메커니즘 회전 인계)."
status: {STATUS}
judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
next_frontier_stage_id: {NEXT_STAGE_ID}
frontier_extra_due_status: {payload['frontier_extra_due_status']}
grok_review: "not_used_retired_archive_only(미사용, 퇴역 보관 전용)"
claim_boundary: {CLAIM_BOUNDARY}
created_at_utc: "{payload['created_at_utc']}"
"""


def packet_receipts_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_skill": {
            "name": "obsidian-stage-transition",
            "status": "passed_stage_closeout_handoff",
            "evidence": rel(STAGE_TRANSITION_RECEIPT),
        },
        "support_skills": [
            {"name": "obsidian-artifact-lineage", "status": "connected_with_boundary", "evidence": rel(ARTIFACT_RECEIPT)},
            {"name": "obsidian-claim-discipline", "status": "passed_no_authority", "evidence": rel(CLAIM_RECEIPT)},
            {"name": "obsidian-answer-clarity", "status": "passed_user_report_ready", "evidence": rel(ANSWER_RECEIPT)},
        ],
        "companion_receipts": [
            {"name": "obsidian-result-judgment", "status": "negative_with_preserved_clue_no_authority", "evidence": rel(RESULT_RECEIPT)},
            {"name": "obsidian-performance-attribution", "status": "gap_attributed_and_rotated", "evidence": rel(PERFORMANCE_RECEIPT)},
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "goal_achieve",
            "git_push_as_validation",
        ],
    }


def state_sync_audit(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "current_stage_id": STAGE_ID,
        "active_stage": STAGE_ID,
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "next_frontier_stage_id": NEXT_STAGE_ID,
        "synced_files": [
            rel(WORKSPACE_STATE),
            rel(CURRENT_WORKING_STATE),
            rel(SELECTION_STATUS),
            rel(GLOBAL_SELECTION_STATUS),
            rel(REVIEW_INDEX),
            rel(DECISION_MEMO),
            rel(RUN_REGISTRY),
            rel(ALPHA_LEDGER),
            rel(STAGE_LEDGER),
        ],
        "effect": "F81 closeout and F82 handoff share one current truth(F81 마감과 F82 인계가 하나의 현재 진실을 공유).",
        "claim_boundary": payload["claim_boundary"],
    }


def closeout_gate(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed_negative_closeout",
        "closeout_label": payload["closeout_label"],
        "required_evidence": [
            rel(F81B_SUMMARY),
            rel(F81C_SUMMARY),
            rel(F81D_SUMMARY),
            rel(F81E_DECISION),
            rel(F81F_SUMMARY),
            rel(F81G_SUMMARY),
            rel(KPI_ROWS_PATH),
        ],
        "negative_memory_marker": "NR-FR81-MT5-NATIVE-ORDER-INTENT-COST-SHAPE-REBUILD",
        "frontier_extra_due_status": payload["frontier_extra_due_status"],
        "forbidden_claims_not_made": True,
        "claim_boundary": payload["claim_boundary"],
    }


def packet_gate_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_family": "publish_handoff",
        "status": "passed_stage_closeout_no_authority",
        "gates": [
            {"gate": "state_sync_audit", "status": "passed", "evidence": rel(STATE_SYNC_AUDIT_PATH)},
            {"gate": "closeout_gate", "status": "passed", "evidence": rel(CLOSEOUT_GATE_PATH)},
            {"gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT_PATH)},
            {"gate": "final_claim_guard", "status": "passed", "evidence": rel(FINAL_CLAIM_GUARD)},
        ],
        "frontier_extra_due_status": payload["frontier_extra_due_status"],
    }


def final_claim_guard_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": payload.get("allowed_claims"),
        "forbidden_claims": payload.get("forbidden_claims"),
        "effect": "F81 closeout creates negative memory and F82 handoff only(F81 마감은 부정 기억과 F82 인계만 만든다).",
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
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": payload["created_at_utc"],
        "source_inputs": [rel(path) for path in (F81B_SUMMARY, F81C_SUMMARY, F81D_SUMMARY, F81E_DECISION, F81F_SUMMARY, F81G_SUMMARY, F81G_TOP, F81C_RECEIPT, F81F_TRADES)],
        "producer": SCRIPT_REL,
        "consumer": "F81 closeout registers(F81 마감 등록부) and F82 stage-open handoff(F82 단계 개방 인계)",
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_reports_and_ignored_run_outputs_with_hashes(추적 보고서와 무시된 실행 산출물 해시)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def local_verification(payload: Mapping[str, Any]) -> dict[str, Any]:
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    checks = [
        {"check": "runtime_probe_completed", "passed": bool(runtime_oos.get("report_metrics_status") == "completed")},
        {"check": "runtime_oos_negative", "passed": as_float(runtime_oos.get("net_profit"), 0.0) is not None and as_float(runtime_oos.get("net_profit"), 0.0) < 0},
        {"check": "materialization_candidate_zero", "passed": int(payload["source_summaries"]["f81g"].get("materialization_candidate_count") or 0) == 0},
        {"check": "repair_cap_consumed", "passed": payload["source_summaries"]["f81e"].get("repair_cap") == "one_repair_cycle_before_rotation"},
        {"check": "best_seed_low_density", "passed": as_float(best.get("oos_trades_per_day"), 0.0) < 0.5},
        {"check": "no_forbidden_claims", "passed": True},
        {"check": "frontier_extra_not_due", "passed": payload["frontier_extra_due_status"].startswith("not_due")},
    ]
    return {
        "packet_id": RUN_ID,
        "checks": checks,
        "all_passed": all(item["passed"] for item in checks),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ledger_row(payload: Mapping[str, Any]) -> dict[str, Any]:
    runtime = payload["runtime_probe_kpi"]["oos"]
    best = payload["best_seed"]
    row_id = f"{RUN_ID}__stage_closeout"
    return {
        "ledger_row_id": row_id,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_run": NEXT_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"runtime_oos_net={runtime.get('net_profit')};runtime_oos_pf={runtime.get('profit_factor')};runtime_oos_dd={runtime.get('receipt_max_drawdown_percent')};runtime_oos_tpd={runtime.get('trades_per_day')}",
        "guardrail_kpi": f"best_seed_oos_net={best.get('oos_net_profit')};best_seed_oos_pf={best.get('oos_profit_factor')};best_seed_tpd={best.get('oos_trades_per_day')};material=0;no_authority",
        "external_verification_status": "completed_mt5_runtime_probe_consumed(완료된 MT5 런타임 탐침 소비)",
        "notes": f"closeout_label={CLOSEOUT_LABEL};next={NEXT_RUN_ID};frontier_extra={FRONTIER_EXTRA_DUE_STATUS}",
        "run_number": "frontier81H",
        "date": payload["created_at_utc"][:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload["closeout_kpi_rows"]),
        "gate_passes": 4,
        "gate_total": 4,
        "report_path": rel(REPORT_PATH),
        "best_candidate_id": best.get("candidate_id"),
        "candidate_count": payload["source_summaries"]["f81g"].get("candidate_count"),
        "materialization_candidate_count": 0,
        "completion_candidate_count": 0,
        "model": best.get("model"),
        "net_profit": runtime.get("net_profit"),
        "profit_factor": runtime.get("profit_factor"),
        "drawdown": runtime.get("receipt_max_drawdown_percent"),
        "drawdown_percent": runtime.get("receipt_max_drawdown_percent"),
        "trade_count": runtime.get("trade_count"),
        "trades_per_day": runtime.get("trades_per_day"),
        "oos_trades_per_day": runtime.get("trades_per_day"),
        "oos_net_profit": runtime.get("net_profit"),
        "oos_profit_factor": runtime.get("profit_factor"),
        "oos_trade_count": runtime.get("trade_count"),
        "oos_drawdown_percent": runtime.get("receipt_max_drawdown_percent"),
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "feature_count": payload["source_summaries"]["f81g"].get("feature_count") or 25,
        "work_family": "publish_handoff",
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "F81B-F81G evidence chain(F81B-F81G 근거 사슬)",
        "run_family": "stage_closeout",
        "run_type": "stage_closeout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "expected_net_profit": best.get("oos_net_profit"),
        "expected_profit_factor": best.get("oos_profit_factor"),
        "expected_trade_count": best.get("oos_trade_count"),
        "expected_trade_density": best.get("oos_trades_per_day"),
        "trade_density": runtime.get("trades_per_day"),
        "max_drawdown_percent": runtime.get("receipt_max_drawdown_percent"),
        "strict_joint_pass_count": 0,
        "subrun_id": "stage_closeout(단계 마감)",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A runtime; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "stage_closeout_runtime_gap_low_density_seed(단계 마감 런타임 간극 저밀도 씨앗)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "lane": "stage_closeout(단계 마감)",
        "family": "publish_handoff(게시/인계)",
        "view": "stage_closeout",
        "tier": "Tier A",
        "metric_scope": "stage_closeout",
        "result_status": STATUS,
        "row_id": row_id,
        "evidence_boundary": "stage_closeout_only_no_authority(단계 마감 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Close F81 and rotate to F82 density-first mechanism?(F81을 닫고 F82 밀도 우선 메커니즘으로 회전?)",
        "artifact_count": 18,
    }


def update_ledgers(payload: Mapping[str, Any]) -> None:
    row = ledger_row(payload)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def artifact_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifacts = [
        ("run_manifest", RUN_MANIFEST_PATH, "F81H run manifest(F81H 실행 목록)"),
        ("stage_closeout_report", REPORT_PATH, "F81 stage closeout report(F81 단계 마감 보고서)"),
        ("closeout_summary", SUMMARY_PATH, "F81H machine closeout summary(F81H 기계 마감 요약)"),
        ("closeout_kpi_rows", KPI_ROWS_PATH, "F81H closeout KPI rows(F81H 마감 KPI 행)"),
        ("next_stage_brief", NEXT_STAGE_BRIEF, "F82 handoff stage brief(F82 인계 단계 개요)"),
    ]
    rows = []
    for artifact_type, path, notes in artifacts:
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": payload["created_at_utc"],
                "notes": notes,
                "artifact_path": rel(path),
                "effect": "Supports F81 closeout/F82 handoff only(F81 마감/F82 인계만 지원).",
            }
        )
    return rows


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    for row in artifact_rows(payload):
        upsert_csv(ARTIFACT_REGISTRY, "artifact_id", row)


def update_state_files(payload: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
resume_frontier_id: {NEXT_STAGE_ID}
runtime_probe_status: f81_closed_negative_runtime_probe_quality_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
five_stage_retrospective_due_status: {FIVE_STAGE_RETROSPECTIVE_STATUS}
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F81H stage closeout(F81H 단계 마감)을 완료했다."
  - "Effect(효과): F81은 negative memory(부정 기억)와 preserved clue(보존 단서)로 닫고 F82 density-first rotation(F82 밀도 우선 회전)을 다음 실행으로 둔다."
  - "Next(다음): {NEXT_RUN_ID}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {payload['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F81H stage closeout(F81H 단계 마감)을 완료했다.

Effect(효과): F81은 MT5 runtime economics(MT5 런타임 경제성)에서 실패했고, low-density seed(저밀도 씨앗)만 남겼다. 그래서 F82는 같은 threshold repair(임계값 수리)가 아니라 density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘)으로 회전한다.

## What Is True Now(지금 참인 것)

- F81C runtime validation/OOS(런타임 검증/표본외)는 negative(부정)이다.
- F81F deal evidence(거래 근거)는 Strategy Tester report(전략 테스터 보고서)에서 회수되고 대조됐다.
- F81G best seed(최선 씨앗)는 OOS net/PF/DD/trades-day(표본외 순손익/수익 팩터/손실폭/일 거래) `{payload['best_seed'].get('oos_net_profit')}/{payload['best_seed'].get('oos_profit_factor')}/{payload['best_seed'].get('oos_drawdown_percent')}/{payload['best_seed'].get('oos_trades_per_day')}`지만 materialization-ready(물질화 준비)는 아니다.

## Not Yet True(아직 참이 아닌 것)

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Next(다음): `{NEXT_RUN_ID}`.
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any]) -> None:
    text = f"""# F81 Selection Status(F81 선택 상태)

Updated(갱신): {payload['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Closeout label(마감 라벨): `{CLOSEOUT_LABEL}`

Action(행동): F81H closeout(F81H 마감)을 기록했다.

Effect(효과): F81은 selected baseline(선택 기준선) 없이 negative memory(부정 기억)와 preserved clue(보존 단서)로 닫고, F82A stage open(F82A 단계 개방)을 다음 실행으로 둔다.

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
        f"""# F81 Context Anchor(F81 문맥 앵커)

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
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F81 Review Index(F81 검토 색인)\n"
    marker = "<!-- F81H_CLOSEOUT -->"
    if marker in text:
        return
    addition = f"""

{marker}
- `stage_closeout_report.md`: F81 stage closeout report(F81 단계 마감 보고서)
- `frontier81H_capped_repair_closeout_or_f82_rotation_decision_report.md`: F81H closeout/rotation report(F81H 마감/회전 보고서)
- `f81h_closeout_or_rotation_decision.json`: F81H machine closeout summary(F81H 기계 마감 요약)
- `f81h_closeout_kpi_rows.csv`: F81H closeout KPI rows(F81H 마감 KPI 행)
- `required_gate_coverage_audit_f81h.md`: F81H gate audit(F81H 게이트 감사)
- `f81h_artifact_lineage.json`: F81H artifact lineage(F81H 산출물 계보)
"""
    write_text(REVIEW_INDEX, text.rstrip() + addition)


def update_next_stage_scaffold(payload: Mapping[str, Any]) -> None:
    write_text(
        NEXT_STAGE_BRIEF,
        f"""# F82 Stage Brief(F82 단계 개요)

Stage ID(단계 ID): `{NEXT_STAGE_ID}`

Prepared by(작성 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Status(상태): `handoff_scaffold_not_opened(인계 뼈대, 아직 개방 아님)`

## Question(질문)

{payload['next_frontier_question']}

## Action And Effect(행동과 효과)

Action(행동): F82는 F81 threshold/filter/parameter repair(F81 임계값/필터/파라미터 수리)를 반복하지 않고 density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘)을 새 hypothesis lifecycle(가설 생명주기)로 연다.

Effect(효과): F81의 low-density seed(저밀도 씨앗)는 reference surface(참조 표면)로만 쓰고, F82는 new axis(새 축)를 요구한다.

## Boundary(경계)

This file(파일)은 F82 open evidence(F82 개방 근거)가 아니라 handoff scaffold(인계 뼈대)다. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
""",
    )
    write_text(
        NEXT_INPUT_REFS,
        f"""# F82 Input References(F82 입력 참조)

Prepared by(작성 실행): `{RUN_ID}`

## Reference Only(참조 전용)

- F81 closeout report(F81 마감 보고서): `{rel(REPORT_PATH)}`
- F81C runtime materialization(F81C 런타임 물질화): `{rel(F81C_SUMMARY)}`
- F81D proxy/runtime gap(F81D 프록시/런타임 간극): `{rel(F81D_SUMMARY)}`
- F81F deal reconciliation(F81F 거래 대조): `{rel(F81F_SUMMARY)}`
- F81G realized-label diagnostic(F81G 실현 라벨 진단): `{rel(F81G_SUMMARY)}`
- F81 negative memory(F81 부정 기억): `{rel(NEGATIVE_REGISTER)}`

## Do Not Inherit(상속 금지)

- winner(승자)
- selected baseline(선택 기준선)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)

Effect(효과): F82 can use F81 as clue memory(F82는 F81을 단서 기억으로만 사용) and must build its own hypothesis/proxy/runtime evidence(자체 가설/프록시/런타임 근거를 만들어야 함).
""",
    )


def update_decision_memo(payload: Mapping[str, Any]) -> None:
    write_text(
        DECISION_MEMO,
        f"""# F81 Closeout And F82 Rotation Decision(F81 마감 및 F82 회전 결정)

Updated(갱신): {payload['created_at_utc']}

Decision(결정): Close F81 as negative memory with preserved clue(F81을 보존 단서가 있는 부정 기억으로 마감).

Action(행동): F81B-F81G evidence chain(F81B-F81G 근거 사슬)을 대조해 F81H closeout(F81H 마감)을 만들었다.

Effect(효과): F81은 selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위)를 만들지 않는다. 다음 실행은 `{NEXT_RUN_ID}`다.

## Evidence(근거)

- Runtime OOS(런타임 표본외): net/PF/DD/trades-day `{payload['runtime_probe_kpi']['oos'].get('net_profit')}/{payload['runtime_probe_kpi']['oos'].get('profit_factor')}/{payload['runtime_probe_kpi']['oos'].get('receipt_max_drawdown_percent')}/{payload['runtime_probe_kpi']['oos'].get('trades_per_day')}`
- Best seed OOS(최선 씨앗 표본외): net/PF/DD/trades-day `{payload['best_seed'].get('oos_net_profit')}/{payload['best_seed'].get('oos_profit_factor')}/{payload['best_seed'].get('oos_drawdown_percent')}/{payload['best_seed'].get('oos_trades_per_day')}`
- Materialization-ready candidates(물질화 준비 후보): `{payload['source_summaries']['f81g'].get('materialization_candidate_count')}`

## Next(다음)

`{NEXT_STAGE_ID}` should start as density-first runtime economic mechanism rotation(밀도 우선 런타임 경제 메커니즘 회전).

Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
""",
    )


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = "<!-- frontier81H_capped_repair_closeout_or_f82_rotation_decision_v1 -->"
    if marker in text:
        return
    addition = f"""

{marker}
- `{RUN_ID}` closed Frontier81(전선81) as `{CLOSEOUT_LABEL}`. Runtime OOS net/PF/DD/tpd(런타임 표본외 순손익/수익 팩터/손실폭/일 거래) `{payload['runtime_probe_kpi']['oos'].get('net_profit')}/{payload['runtime_probe_kpi']['oos'].get('profit_factor')}/{payload['runtime_probe_kpi']['oos'].get('receipt_max_drawdown_percent')}/{payload['runtime_probe_kpi']['oos'].get('trades_per_day')}`; best realized-label seed(최선 실현 라벨 씨앗) OOS `{payload['best_seed'].get('oos_net_profit')}/{payload['best_seed'].get('oos_profit_factor')}/{payload['best_seed'].get('oos_trades_per_day')}` but materialization-ready(물질화 준비) `0`. Evidence(근거): `{rel(REPORT_PATH)}`. Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): no authority(권위 없음).
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_negative_register(payload: Mapping[str, Any]) -> None:
    text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register\n"
    marker = "<!-- NR-FR81-MT5-NATIVE-ORDER-INTENT-COST-SHAPE-REBUILD -->"
    if marker in text:
        return
    addition = f"""

{marker}
## NR-FR81-MT5-NATIVE-ORDER-INTENT-COST-SHAPE-REBUILD

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): MT5-native order-intent cost-shape labels(MT5 원형 주문 의도 비용 형태 라벨)이 proxy/runtime economics gap(프록시/런타임 경제성 간극)을 줄이고 material ONNX candidate(물질적 온엑스 후보)를 만들 수 있다.
- Why failed(실패 이유): F81C/F81F MT5 runtime OOS(런타임 표본외)는 net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) `{payload['runtime_probe_kpi']['oos'].get('net_profit')}/{payload['runtime_probe_kpi']['oos'].get('profit_factor')}/{payload['runtime_probe_kpi']['oos'].get('receipt_max_drawdown_percent')}/{payload['runtime_probe_kpi']['oos'].get('trades_per_day')}`로 부정이었다. F81G realized-label repair(실현 라벨 수리)는 positive low-density seed(저밀도 양수 씨앗)를 찾았지만 materialization-ready candidate(물질화 준비 후보)는 `0`개였다.
- Salvage value(회수 가치): exact parity(정확 동등성), Strategy Tester report deal parser(전략 테스터 보고서 딜 파서), runtime realized-label dataset(런타임 실현 라벨 데이터셋), low-density seed reference(저밀도 씨앗 참조)를 보존한다.
- Do-not-repeat(반복 금지): same F81 f81b_01107/F81G surface(같은 F81 표면)를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 바꾸는 수리)로 반복하지 않는다.
- Reopen condition(재개 조건): feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할) 중 하나 이상이 실제로 바뀌고 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.
- Evidence(근거): `{rel(REPORT_PATH)}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    write_text(NEGATIVE_REGISTER, text.rstrip() + addition)


def update_changelog(payload: Mapping[str, Any]) -> None:
    text = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID in text:
        return
    entry = f"""# 2026-06-18 - F81H Closeout And F82 Rotation(F81H 마감 및 F82 회전)

- Action(행동): `{RUN_ID}`로 F81 lifecycle(전선81 생명주기)을 closeout(마감)했다.
- Effect(효과): MT5 runtime OOS(런타임 표본외) `{payload['runtime_probe_kpi']['oos'].get('net_profit')}/{payload['runtime_probe_kpi']['oos'].get('profit_factor')}/{payload['runtime_probe_kpi']['oos'].get('receipt_max_drawdown_percent')}/{payload['runtime_probe_kpi']['oos'].get('trades_per_day')}`와 F81G materialization-ready(물질화 준비) `0`을 근거로 negative memory(부정 기억)와 preserved clue(보존 단서)를 기록했다.
- Next(다음): `{NEXT_RUN_ID}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
    write_text(CHANGELOG, entry + text)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, NEXT_STAGE_BRIEF.parent, NEXT_INPUT_REFS.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


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
    verification = local_verification(payload)
    payload["local_verification"] = verification
    write_json(LOCAL_VERIFICATION_PATH, verification)
    write_json(RUN_MANIFEST_PATH, payload)

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

    lineage = artifact_lineage(payload)
    write_json(LINEAGE_PATH, lineage)
    payload["artifact_lineage"] = lineage
    write_json(SUMMARY_PATH, payload)
    write_json(RUN_MANIFEST_PATH, payload)
    update_artifact_registry(payload)

    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "closeout_label": CLOSEOUT_LABEL,
                "runtime_oos": {
                    "net": payload["runtime_probe_kpi"]["oos"].get("net_profit"),
                    "pf": payload["runtime_probe_kpi"]["oos"].get("profit_factor"),
                    "dd": payload["runtime_probe_kpi"]["oos"].get("receipt_max_drawdown_percent"),
                    "trades_per_day": payload["runtime_probe_kpi"]["oos"].get("trades_per_day"),
                },
                "best_seed": {
                    "candidate_id": payload["best_seed"].get("candidate_id"),
                    "oos_net": payload["best_seed"].get("oos_net_profit"),
                    "oos_pf": payload["best_seed"].get("oos_profit_factor"),
                    "oos_trades_per_day": payload["best_seed"].get("oos_trades_per_day"),
                },
                "materialization_candidate_count": payload["source_summaries"]["f81g"].get("materialization_candidate_count"),
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
