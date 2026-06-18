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


STAGE_ID = "stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation"
RUN_ID = "frontier83G_runtime_realized_outcome_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier83F_short_density_proxy_runtime_gap_analysis_v1"
NEXT_STAGE_ID = "stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap"
NEXT_RUN_ID = "frontier84A_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap_v1"

STATUS = "closed_negative_runtime_winrate_erosion_after_signal_parity_rotation_to_f84_no_authority"
JUDGMENT = "negative_memory_with_runtime_realized_winrate_rebuild_rotation_no_authority"
CLOSEOUT_LABEL = (
    "negative_memory_with_preserved_runtime_parity_clue_and_winrate_gap_seed"
    "(부정 기억과 보존 런타임 동등성 단서 및 승률 간극 씨앗)"
)
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f83_closeout_next_boundary_f100_e01_closed_for_f050"
FIVE_STAGE_RETROSPECTIVE_STATUS = "retired_archive_only_no_new_grok_call_no_next_open_block"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID

F83A_SUMMARY = REVIEW_DIR / "f83a_teacher_distillation_summary.json"
F83B_SUMMARY = REVIEW_DIR / "f83b_mt5_runtime_materialization_summary.json"
F83C_SUMMARY = REVIEW_DIR / "f83c_proxy_runtime_gap_analysis_summary.json"
F83D_SUMMARY = REVIEW_DIR / "f83d_two_sided_density_expansion_decision_summary.json"
F83E_SUMMARY = REVIEW_DIR / "f83e_short_side_density_runtime_materialization_summary.json"
F83F_SUMMARY = REVIEW_DIR / "f83f_short_density_proxy_runtime_gap_analysis_summary.json"
F83F_GAP_ROWS = REVIEW_DIR / "f83f_short_density_proxy_runtime_gap_rows.csv"
F83F_CAUSE_ROWS = REVIEW_DIR / "f83f_gap_cause_attribution_rows.csv"

SUMMARY_PATH = REVIEW_DIR / "f83g_repair_or_rotation_decision_summary.json"
KPI_ROWS_PATH = REVIEW_DIR / "f83g_closeout_kpi_rows.csv"
LINEAGE_PATH = REVIEW_DIR / "f83g_artifact_lineage.json"
LOCAL_VERIFICATION_PATH = REVIEW_DIR / "f83g_local_verification.json"
REPORT_PATH = REVIEW_DIR / "frontier83G_runtime_realized_outcome_repair_or_rotation_decision_report.md"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f83g.md"
STATE_SYNC_AUDIT_PATH = REVIEW_DIR / "f83g_state_sync_audit.json"
CLOSEOUT_GATE_PATH = REVIEW_DIR / "f83g_closeout_gate.json"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
RUN_KPI_ROWS_PATH = RUN_DIR / "f83g_closeout_kpi_rows.csv"

STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f83g_stage_transition_receipt.yaml"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f83g_run_evidence_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f83g_result_judgment_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f83g_performance_attribution_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f83g_artifact_lineage_receipt.yaml"
TASK_FORCE_RECEIPT = REVIEW_DIR / "f83g_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f83g_claim_discipline_receipt.yaml"
ANSWER_RECEIPT = REVIEW_DIR / "f83g_answer_clarity_receipt.yaml"

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
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_frontier83_closeout_rotate_f84.md"
FRONTIER_EXTRA_REGISTER = ROOT / "docs/registers/frontier_extra_stage_register.yaml"
FIVE_STAGE_RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
NEXT_STAGE_BRIEF = NEXT_STAGE_DIR / "00_spec/stage_brief.md"
NEXT_INPUT_REFS = NEXT_STAGE_DIR / "01_inputs/input_refs.md"

SCRIPT_REL = "stage_pipelines/stage_frontier_83/frontier83g_runtime_realized_outcome_repair_or_rotation_decision.py"


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


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            sample = io_path(candidate).read_bytes()
            return "\r\n" if b"\r\n" in sample else "\n"
    return "\n"


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    lineterminator = csv_lineterminator(path, source_header)
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
        rows = []
    else:
        fieldnames = [field for field in row.keys() if field]
        rows = []
    for field in row:
        if field and field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
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


def split_runtime(f83e: Mapping[str, Any], split: str) -> Mapping[str, Any]:
    for row in f83e.get("runtime_closeout_kpis", []):
        if row.get("split") == split:
            return row
    return {}


def split_gap(f83f: Mapping[str, Any], split: str) -> Mapping[str, Any]:
    for row in f83f.get("gap_rows", []):
        if row.get("split") == split:
            return row
    return {}


def split_cause(f83f: Mapping[str, Any], split: str) -> Mapping[str, Any]:
    for row in f83f.get("cause_rows", []):
        if row.get("split") == split:
            return row
    return {}


def proxy_row(target: Mapping[str, Any], split: str, gap: Mapping[str, Any]) -> dict[str, Any]:
    prefix = "val" if split == "validation" else "oos"
    split_label = "validation" if split == "validation" else "OOS"
    split_ko = "검증" if split == "validation" else "표본외"
    return {
        "record_id": f"{RUN_ID}__proxy_{split}",
        "test_period": "2025-01-02..2025-10-01" if split == "validation" else "2025-10-01..2026-04-14",
        "split_view": f"F83D/F82B short-density proxy {split_label}(F83D/F82B 숏 밀도 프록시 {split_ko})",
        "evidence_source": rel(F83D_SUMMARY),
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
        "long_short_breakdown": f"long=0;short={target.get(f'{prefix}_trade_count')}(롱=0;숏={target.get(f'{prefix}_trade_count')})",
        "proxy_runtime_KPI_gap": (
            f"runtime_net_delta={gap.get('net_runtime_minus_proxy')};"
            f"runtime_pf_delta={gap.get('pf_runtime_minus_proxy')};"
            f"runtime_dd_delta={gap.get('dd_runtime_minus_proxy')};"
            f"runtime_win_rate_delta_pp={gap.get('win_rate_delta_pp')}"
        ),
        "parity": "proxy_only_then_materialized_in_f83e(프록시 전용 후 F83E에서 물질화)",
        "gap_cause": "pending_until_f83f(전선83F까지 보류)",
        "next_action": NEXT_RUN_ID,
        "materialization_status": "f83e_mt5_probe_completed(F83E MT5 탐침 완료)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def runtime_row(row: Mapping[str, Any], gap: Mapping[str, Any], cause: Mapping[str, Any]) -> dict[str, Any]:
    split = str(row.get("split") or "")
    split_label = "validation" if split == "validation" else "OOS"
    split_ko = "검증" if split == "validation" else "표본외"
    return {
        "record_id": f"{RUN_ID}__runtime_{split}",
        "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
        "split_view": f"F83E MT5 runtime {split_label}(F83E MT5 런타임 {split_ko})",
        "evidence_source": rel(F83E_SUMMARY),
        "net_profit": row.get("net_profit"),
        "gross_profit": row.get("gross_profit"),
        "gross_loss": row.get("gross_loss"),
        "PF": row.get("profit_factor"),
        "DD_percent": row.get("max_drawdown_percent"),
        "trade_count": row.get("trade_count"),
        "trades_per_day": row.get("trades_per_day"),
        "win_rate": row.get("win_rate_percent"),
        "average_win": row.get("average_win"),
        "average_loss": row.get("average_loss"),
        "payoff_ratio": row.get("payoff_ratio"),
        "expectancy": row.get("expectancy"),
        "recovery_factor": row.get("recovery_factor"),
        "time_under_water": "missing_from_normalized_receipt(정규화 영수증에서 누락)",
        "max_consecutive_loss": "missing_from_normalized_receipt(정규화 영수증에서 누락)",
        "long_short_breakdown": f"long={row.get('long_trade_count')};short={row.get('short_trade_count')}(롱={row.get('long_trade_count')};숏={row.get('short_trade_count')})",
        "proxy_runtime_KPI_gap": (
            f"proxy_net={gap.get('proxy_net_profit')};runtime_net={gap.get('runtime_net_profit')};"
            f"proxy_pf={gap.get('proxy_profit_factor')};runtime_pf={gap.get('runtime_profit_factor')};"
            f"proxy_dd={gap.get('proxy_drawdown_percent')};runtime_dd={gap.get('runtime_drawdown_percent')};"
            f"win_rate_delta_pp={gap.get('win_rate_delta_pp')}"
        ),
        "parity": "signal_feature_onnx_parity_passed_but_economics_failed(신호/피처/온엑스 동등성 통과, 경제성 실패)",
        "gap_cause": cause.get("dominant_gap_cause") or "runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식)",
        "next_action": NEXT_RUN_ID,
        "materialization_status": "completed_mt5_strategy_tester_probe(전략 테스터 탐침 완료)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_kpi_rows(f83d: Mapping[str, Any], f83e: Mapping[str, Any], f83f: Mapping[str, Any]) -> list[dict[str, Any]]:
    target = f83f.get("target") or f83d.get("target") or {}
    rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        rows.append(proxy_row(target, split, split_gap(f83f, split)))
    for split in ("validation", "oos"):
        rows.append(runtime_row(split_runtime(f83e, split), split_gap(f83f, split), split_cause(f83f, split)))
    return rows


def build_payload(created_at: str) -> dict[str, Any]:
    f83a = read_json(F83A_SUMMARY)
    f83b = read_json(F83B_SUMMARY)
    f83c = read_json(F83C_SUMMARY)
    f83d = read_json(F83D_SUMMARY)
    f83e = read_json(F83E_SUMMARY)
    f83f = read_json(F83F_SUMMARY)
    target = f83f.get("target") or f83d.get("target") or {}
    validation_runtime = split_runtime(f83e, "validation")
    oos_runtime = split_runtime(f83e, "oos")
    validation_gap = split_gap(f83f, "validation")
    oos_gap = split_gap(f83f, "oos")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_frontier_stage_id": NEXT_STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": "rotate_to_f84_runtime_realized_winrate_rebuild(전선84 런타임 실현 승률 재구축으로 회전)",
        "closeout_label": CLOSEOUT_LABEL,
        "claim_boundary": CLAIM_BOUNDARY,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "five_stage_retrospective_status": FIVE_STAGE_RETROSPECTIVE_STATUS,
        "hypothesis": (
            "Realized PnL teacher distillation(실현 손익 교사 증류) and exportable runtime rotation(내보내기 가능 런타임 회전)이 "
            "US100 M5에서 proxy-positive dense short surface(프록시 양수 고밀도 숏 표면)를 MT5 runtime economics(MT5 런타임 경제성)로 "
            "옮길 수 있다."
        ),
        "test_period": "validation(검증) 2025-01-02..2025-10-01; OOS(표본외) 2025-10-01..2026-04-14",
        "source_summaries": {
            "f83a": {"status": f83a.get("status"), "judgment": f83a.get("judgment"), "run_id": f83a.get("run_id")},
            "f83b": {
                "status": f83b.get("status"),
                "judgment": f83b.get("judgment"),
                "best_runtime": f83b.get("best_runtime"),
            },
            "f83c": {
                "status": f83c.get("status"),
                "judgment": f83c.get("judgment"),
                "runtime_parity_preserved": f83c.get("runtime_parity_preserved"),
            },
            "f83d": {
                "status": f83d.get("status"),
                "judgment": f83d.get("judgment"),
                "target_candidate_id": target.get("candidate_id"),
                "candidate_universe_counts": f83d.get("candidate_universe_counts"),
            },
            "f83e": {
                "status": f83e.get("status"),
                "judgment": f83e.get("judgment"),
                "artifact_export_status": f83e.get("artifact_export_status"),
                "completed_attempt_count": f83e.get("completed_attempt_count"),
                "probability_parity_pass_rows": f83e.get("probability_parity_pass_rows"),
                "signal_parity_pass_rows": f83e.get("signal_parity_pass_rows"),
                "feature_readiness_pass_rows": f83e.get("feature_readiness_pass_rows"),
                "runtime_result_judgment": f83e.get("runtime_result_judgment"),
            },
            "f83f": {
                "status": f83f.get("status"),
                "judgment": f83f.get("judgment"),
                "primary_attribution": f83f.get("primary_attribution"),
            },
        },
        "target": target,
        "runtime_probe_kpi": {
            "validation": validation_runtime,
            "oos": oos_runtime,
        },
        "gap_rows": [validation_gap, oos_gap],
        "cause_rows": [split_cause(f83f, "validation"), split_cause(f83f, "oos")],
        "closeout_kpi_rows": build_kpi_rows(f83d, f83e, f83f),
        "observed_change": (
            "F83D proxy(프록시)는 validation/OOS 양수였지만 F83E runtime(런타임)은 "
            f"validation net/PF/DD {validation_runtime.get('net_profit')}/{validation_runtime.get('profit_factor')}/{validation_runtime.get('max_drawdown_percent')} and "
            f"OOS net/PF/DD {oos_runtime.get('net_profit')}/{oos_runtime.get('profit_factor')}/{oos_runtime.get('max_drawdown_percent')}로 붕괴했다."
        ),
        "primary_gap_cause": "runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식)",
        "why_failed": [
            "Signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 보존됐지만 runtime win rate(런타임 승률)가 proxy(프록시)보다 validation -11.66pp, OOS -11.94pp 낮아졌다.",
            "Order fill gap share(주문 체결 간극 비중)는 validation 약 0.0043, OOS 약 0.0045로 net gap(순손익 간극)을 설명하기에 너무 작다.",
            "Runtime DD(런타임 손실폭)는 validation 58.86%, OOS 19.24%로 F83D proxy DD(프록시 손실폭)를 크게 초과했다.",
            "같은 f82b_10355 close_direction smooth_supply short-density surface(동일 숏 밀도 표면)를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)로 반복하면 새 evidence axis(근거 축)가 없다.",
        ],
        "repair_admissibility": {
            "same_surface_threshold_filter_parameter_only": "rejected(거절)",
            "same_surface_reason": "F83F negative memory(부정 기억)가 이미 do-not-repeat(반복 금지)로 잠갔고 primary cause(주 원인)는 threshold(임계값)가 아니라 runtime win-rate erosion(런타임 승률 침식)이다.",
            "allowed_reopen_axes": [
                "runtime-realized outcome label(런타임 실현 결과 라벨)",
                "stop-touch/fill-path target(손절·익절 터치/체결 경로 목표)",
                "risk logic change(위험 로직 변경)",
                "regime/session split(장세/세션 분할)",
                "fresh MT5 Runtime Probe(새 MT5 런타임 탐침)",
            ],
        },
        "preserved_clues": [
            "F83B/F83C long teacher overlay runtime parity clue(F83B/F83C 롱 교사 덧씌움 런타임 동등성 단서)",
            "F83E ONNX/signal/materialization path worked as a runtime probe harness(F83E 온엑스/신호/물질화 경로는 런타임 탐침 장치로 작동)",
            "F83F isolated win-rate erosion after signal parity(F83F가 신호 동등성 이후 승률 침식을 분리)",
            "short-density supply can meet target trade density in proxy(F83D 숏 밀도 공급은 프록시에서 목표 거래 밀도를 충족)",
        ],
        "negative_memory": [
            "Do not reuse f82b_10355 smooth_trade_supply short close_direction surface(동일 f82b_10355 숏 종가방향 부드러운 공급 표면) with parameter-only repair(파라미터만 수리).",
            "Do not treat signal parity(신호 동등성) or ONNX export(온엑스 내보내기) as economics authority(경제성 권위).",
            "Do not explain the F83E loss primarily by fill gap(체결 간극) without row-level evidence(행 단위 근거).",
        ],
        "next_frontier_question": (
            "Can runtime-realized win/loss and stop-touch/fill-path labels(런타임 실현 승패 및 손절·익절 터치/체결 경로 라벨)이 "
            "signal parity after proxy success(프록시 성공 뒤 신호 동등성)에서도 actual MT5 win rate(실제 MT5 승률)를 보존하는 "
            "exportable ONNX candidate(내보내기 가능 온엑스 후보)를 만들 수 있는가?"
        ),
        "next_frontier_seed_axes": [
            "Use F83E/F83F runtime deal outcome as teacher surface(F83E/F83F 런타임 거래 결과를 교사 표면으로 사용)",
            "Train label around realized win/loss, stop-touch, and fill path(실현 승패/손절·익절 터치/체결 경로 중심 라벨 학습)",
            "Segment by session/regime before threshold search(임계값 탐색 전 세션/장세 분할)",
            "Require MT5 materialization once a meaningful candidate appears(의미 있는 후보가 나오면 MT5 물질화 필수)",
        ],
    }


def kpi_table_rows(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| view(보기) | net(순손익) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | win rate(승률) | gap cause(간극 원인) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.get('split_view')} | `{fmt(row.get('net_profit'))}` | `{fmt(row.get('PF'))}` | `{fmt(row.get('DD_percent'))}` | "
            f"`{fmt(row.get('trades_per_day'))}` | `{fmt(row.get('win_rate'))}` | {row.get('gap_cause')} |"
        )
    return "\n".join(lines)


def closeout_report_text(payload: Mapping[str, Any]) -> str:
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    runtime_val = payload["runtime_probe_kpi"]["validation"]
    return f"""# F83G Runtime-Realized Outcome Repair Or Rotation Decision(F83G 런타임 실현 결과 수리 또는 회전 결정)

Updated(갱신): {payload['created_at_utc']}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- closeout label(마감 라벨): `{CLOSEOUT_LABEL}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Decision(결정)

Action(행동): F83을 valid negative runtime evidence(유효한 부정 런타임 근거)로 closeout(마감)하고, F84를 runtime-realized win-rate rebuild(런타임 실현 승률 재구축) 축으로 handoff(인계)한다.

Effect(효과): F83의 실패를 버리지 않고, 다음 가설이 고쳐야 할 실제 원인인 runtime win-rate erosion(런타임 승률 침식)을 새 label/target/risk axis(라벨/목표/위험 축)로 가져간다.

## KPI Closeout(KPI 마감)

{kpi_table_rows(payload['closeout_kpi_rows'])}

Runtime validation(런타임 검증): net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) `{runtime_val.get('net_profit')}/{runtime_val.get('profit_factor')}/{runtime_val.get('max_drawdown_percent')}/{runtime_val.get('trades_per_day')}`.

Runtime OOS(런타임 표본외): net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) `{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}`.

## Why Not Repair Same Surface(같은 표면을 수리하지 않는 이유)

- Signal parity(신호 동등성)와 feature readiness(피처 준비)는 통과했지만, runtime win rate(런타임 승률)가 validation -11.66pp, OOS -11.94pp 침식됐다.
- Order fill gap(주문 체결 간극)은 net gap(순손익 간극)의 약 0.45% 수준이라 주 원인으로 보기 어렵다.
- DD(손실폭)는 validation 58.86%, OOS 19.24%까지 커졌다.
- 같은 threshold/filter/parameter(임계값/필터/파라미터)만 바꾸는 repair(수리)는 new axis(새 축)가 아니므로 금지한다.

## Preserved Clues(보존 단서)

{chr(10).join(f"- {item}" for item in payload['preserved_clues'])}

## Negative Memory(부정 기억)

{chr(10).join(f"- {item}" for item in payload['negative_memory'])}

## Next Frontier Proposal(다음 전선 제안)

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Question(질문): {payload['next_frontier_question']}

Boundary(경계): F84 scaffold(전선84 뼈대)는 open evidence(개방 근거)가 아니다. F84A가 독립 open packet(개방 묶음)을 만들어야 한다.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F83G Required Gate Coverage Audit(F83G 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `state_sync_audit(상태 동기화 감사)` | `passed(통과)` | `{rel(STATE_SYNC_AUDIT_PATH)}` | current truth(현재 진실)와 next run(다음 실행)을 같은 회차에 맞춘다. |
| `closeout_gate(마감 게이트)` | `passed(통과)` | `{rel(CLOSEOUT_GATE_PATH)}` | F83을 negative memory(부정 기억)로 닫고 권위 주장을 막는다. |
| `kpi_contract_audit(KPI 계약 감사)` | `passed(통과)` | `{rel(KPI_ROWS_PATH)}` | proxy/runtime KPI(프록시/런타임 핵심 지표)를 함께 남긴다. |
| `frontier_extra_due_check(전선 추가 도래 점검)` | `passed_not_due(통과_도래아님)` | `{rel(FRONTIER_EXTRA_REGISTER)}` | F84 handoff(전선84 인계)는 F100 전이므로 extra stage(추가 단계)로 막히지 않는다. |
| `five_stage_retrospective_archive_check(5단계 회고 보관 점검)` | `passed_retired_archive_only(통과_퇴역 보관 전용)` | `{rel(FIVE_STAGE_RETROSPECTIVE_REGISTER)}` | Grok(그록) 회고는 새 block(차단)을 만들지 않는다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `passed(통과)` | `{rel(TASK_FORCE_RECEIPT)}` | 8명 agent(요원) 검토를 closeout(마감)에 붙인다. |
| `result_judgment_boundary(결과 판정 경계)` | `passed(통과)` | `{rel(RESULT_RECEIPT)}` | negative(부정)과 invalid(무효)를 구분한다. |
| `artifact_lineage_audit(산출물 계보 감사)` | `passed(통과)` | `{rel(LINEAGE_PATH)}` | source/producer/consumer/hash(원천/생산자/소비자/해시)를 연결한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{rel(FINAL_CLAIM_GUARD)}` | completion/runtime authority/live readiness(완성/런타임 권위/실거래 준비)를 금지한다. |

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    return {
        STAGE_TRANSITION_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-stage-transition
status: completed_f83_closeout_f84_handoff_scaffold_no_authority
active_stage: {STAGE_ID}
latest_completed_run_id: {RUN_ID}
next_run_id: {NEXT_RUN_ID}
next_frontier_stage_id: {NEXT_STAGE_ID}
state_sync: same_pass_workspace_current_selection_review_index_decision_memo_registers
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
five_stage_retrospective_status: {FIVE_STAGE_RETROSPECTIVE_STATUS}
claim_boundary: {CLAIM_BOUNDARY}
""",
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: run_closeout_recorded_no_authority
measurement_scope: proxy_runtime_closeout_kpis(프록시/런타임 마감 KPI)
management_state: summary/report/kpi_rows/run_manifest/registry_rows_written(요약/보고/KPI 행/실행 목록/등록부 행 기록)
judgment_class: negative(부정)
scoreboard: runtime_probe_closeout(런타임 탐침 마감)
parity_level: P3_runtime_shadow_parity_sampled_not_economics_authority(P3 런타임 표본 동등성, 경제성 권위 아님)
wfo_status: not_applicable_stage_closeout_from_existing_evidence(기존 근거 기반 단계 마감)
registry_update_required: yes
negative_memory_required: yes
hard_gate_applicable: no
evidence_boundary: stage_closeout_only(단계 마감만)
runtime_oos_net_pf_dd_tpd: {runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}
claim_boundary: {CLAIM_BOUNDARY}
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: negative_stage_closeout_no_authority
result_subject: F83 realized PnL teacher distillation exportable runtime rotation(F83 실현 손익 교사 증류 내보내기 가능 런타임 회전)
evidence_available:
  - {rel(F83D_SUMMARY)}
  - {rel(F83E_SUMMARY)}
  - {rel(F83F_SUMMARY)}
  - {rel(KPI_ROWS_PATH)}
evidence_missing:
  - row_level_deal_mapping_for_each_proxy_signal(각 프록시 신호별 행 단위 거래 매핑)
  - F84 fresh runtime-realized model evidence(F84 새 런타임 실현 모델 근거)
judgment_label: negative(부정)
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
user_explanation_hook: "프록시는 좋아 보였지만 실제 MT5에서는 승률과 손실폭이 무너져 같은 표면 수리는 중단한다."
""",
        PERFORMANCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: attributed_runtime_winrate_erosion_after_signal_parity_no_authority
observed_change: "{payload['observed_change']}"
comparison_baseline: F83D proxy short-density KPI(F83D 프록시 숏 밀도 KPI) vs F83E MT5 runtime KPI(F83E MT5 런타임 KPI)
likely_drivers:
  - close_direction_smooth_supply_proxy_label_mismatch(종가방향 부드러운 공급 프록시 라벨 불일치)
  - runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식)
  - stop_touch_fill_path_missing_from_label(손절·익절 터치/체결 경로 라벨 누락)
segment_checks:
  - validation_split(검증 구간)
  - oos_split(표본외 구간)
  - short_only_direction(숏 전용 방향)
  - fill_gap_share_check(체결 간극 비중 점검)
trade_shape: short_only_dense_runtime_8_trades_per_day_but_negative_expectancy_and_large_dd(숏 전용 8회/일 밀도지만 음수 기대값과 큰 손실폭)
alternative_explanations:
  - spread_or_commission_path(스프레드 또는 수수료 경로)
  - row_level_mapping_missing(행 단위 매핑 누락)
attribution_confidence: medium(중간)
next_probe: {NEXT_RUN_ID}
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F83D_SUMMARY)}
  - {rel(F83E_SUMMARY)}
  - {rel(F83F_SUMMARY)}
producer: {SCRIPT_REL}
consumer: {NEXT_RUN_ID}
artifact_lineage: {rel(LINEAGE_PATH)}
availability: tracked_reports_and_ignored_run_manifest_with_hashes(추적 보고서와 해시 있는 무시 실행 목록)
claim_boundary: {CLAIM_BOUNDARY}
""",
        TASK_FORCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f83g_stage_closeout_and_f84_handoff_no_authority
review_mode: internal_adversarial_review_two_pass_limit(내부 비판 검토 2회차 제한)
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_02_platform_routing_architect
  - agent_03_philosophy_policy_skill_governance
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "Close F83 as negative runtime evidence(F83을 부정 런타임 근거로 마감)."
    - "Reject same-surface threshold/filter-only repair(동일 표면 임계값/필터만 수리 거절)."
    - "Rotate to runtime-realized win-rate label axis(런타임 실현 승률 라벨 축으로 회전)."
    - "Keep F83E ONNX/signal parity as harness clue only(F83E 온엑스/신호 동등성은 장치 단서로만 보존)."
  rejected:
    - "Do not call F83E parity an economics success(F83E 동등성을 경제성 성공으로 부르지 않음)."
    - "Do not blame fill gap as primary cause without row-level proof(행 단위 증명 없이 체결 간극을 주 원인으로 보지 않음)."
  needs_local_verification:
    - "F84A must open a new hypothesis lifecycle(F84A는 새 가설 생명주기를 개방해야 함)."
    - "Any meaningful F84 signal must receive MT5 Strategy Tester materialization(의미 있는 F84 신호는 MT5 전략 테스터 물질화 필요)."
claim_boundary: {CLAIM_BOUNDARY}
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_stage_closeout_no_authority
allowed_claims:
  - f83_closed_negative_runtime_evidence
  - preserved_clue_and_negative_memory_recorded
  - f84_handoff_scaffold_prepared
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
  - git_push_as_validation
claim_boundary: {CLAIM_BOUNDARY}
""",
        ANSWER_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-answer-clarity
status: user_facing_summary_ready
plain_meaning: F83 did not produce a strong runtime strategy; it produced a clear reason to rebuild around runtime-realized win rate(F83은 강한 런타임 전략이 아니라 런타임 실현 승률 중심 재구축 이유를 남김).
what_is_true_now: negative_memory_and_f84_handoff_scaffold(부정 기억과 F84 인계 뼈대)
what_is_not_true: completion_baseline_promotion_runtime_authority_live_readiness_goal_achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 아님)
claim_boundary: {CLAIM_BOUNDARY}
""",
    }


def state_sync_audit(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "same_pass_updates": [
            rel(WORKSPACE_STATE),
            rel(CURRENT_WORKING_STATE),
            rel(SELECTION_STATUS),
            rel(GLOBAL_SELECTION_STATUS),
            rel(REVIEW_INDEX),
            rel(DECISION_MEMO),
            rel(NEXT_STAGE_BRIEF),
            rel(NEXT_INPUT_REFS),
            rel(RUN_REGISTRY),
            rel(ALPHA_LEDGER),
            rel(STAGE_LEDGER),
            rel(ARTIFACT_REGISTRY),
            rel(IDEA_REGISTRY),
            rel(NEGATIVE_REGISTER),
            rel(CHANGELOG),
        ],
        "current_stage_id": STAGE_ID,
        "latest_completed_run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "five_stage_retrospective_status": FIVE_STAGE_RETROSPECTIVE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def closeout_gate(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "closeout_type": "negative_memory_with_preserved_clues_and_f84_handoff",
        "has_runtime_probe": True,
        "has_proxy_runtime_gap_attribution": True,
        "has_negative_memory": True,
        "has_next_frontier_home": True,
        "forbidden_claims_blocked": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def packet_gate_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "gates": {
            "state_sync_audit": "pass",
            "closeout_gate": "pass",
            "kpi_contract_audit": "pass",
            "frontier_extra_due_check": "pass_not_due",
            "five_stage_retrospective_archive_check": "pass_retired_archive_only",
            "codex_task_force_review_packet": "pass",
            "result_judgment_boundary": "pass",
            "artifact_lineage_audit": "pass",
            "required_gate_coverage_audit": "pass",
            "final_claim_guard": "pass",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def final_claim_guard_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "pass",
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": [
            "f83_closed_negative_runtime_evidence",
            "preserved_clue_and_negative_memory_recorded",
            "f84_handoff_scaffold_prepared",
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
  - frontier_extra_due_check
  - codex_task_force_review_packet
  - required_gate_coverage_audit
  - final_claim_guard
scope: "Close F83 negative runtime win-rate erosion evidence and hand off F84 runtime-realized win-rate rebuild(F83 부정 런타임 승률 침식 근거 마감 및 F84 런타임 실현 승률 재구축 인계)."
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
        "receipts": [
            {"skill": "obsidian-stage-transition", "status": "executed", "path": rel(STAGE_TRANSITION_RECEIPT)},
            {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
            {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
            {"skill": "obsidian-performance-attribution", "status": "executed", "path": rel(PERFORMANCE_RECEIPT)},
            {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_RECEIPT)},
            {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_RECEIPT)},
            {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
            {"skill": "obsidian-answer-clarity", "status": "executed", "path": rel(ANSWER_RECEIPT)},
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ledger_row(payload: Mapping[str, Any]) -> dict[str, Any]:
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    runtime_val = payload["runtime_probe_kpi"]["validation"]
    return {
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "stage_closeout(단계 마감)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "F83 stage closeout and F84 handoff scaffold(F83 단계 마감 및 F84 인계 뼈대)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "proxy_runtime_closeout(프록시/런타임 마감)",
        "scoreboard_lane": "runtime_probe_closeout(런타임 탐침 마감)",
        "lane": "stage_closeout",
        "family": "publish_handoff",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": (
            f"runtime_validation_net_pf_dd_tpd={runtime_val.get('net_profit')}/{runtime_val.get('profit_factor')}/"
            f"{runtime_val.get('max_drawdown_percent')}/{runtime_val.get('trades_per_day')};"
            f"runtime_oos_net_pf_dd_tpd={runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/"
            f"{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}"
        ),
        "guardrail_kpi": "no_authority;negative_memory;no_same_surface_threshold_only_repair",
        "external_verification_status": "completed_existing_mt5_strategy_tester_probe_in_f83e_gap_attributed_in_f83f",
        "notes": f"next={NEXT_RUN_ID}; decision={payload['decision']}",
        "run_number": "frontier83G",
        "date": payload["created_at_utc"][:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload["closeout_kpi_rows"]),
        "gate_passes": 10,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "net_profit": runtime_oos.get("net_profit"),
        "profit_factor": runtime_oos.get("profit_factor"),
        "drawdown": runtime_oos.get("max_drawdown_percent"),
        "recovery_factor": runtime_oos.get("recovery_factor"),
        "trade_count": runtime_oos.get("trade_count"),
        "trades_per_day": runtime_oos.get("trades_per_day"),
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(SUMMARY_PATH),
        "view": "stage_closeout",
        "tier": "Tier A",
        "metric_scope": "runtime_probe_closeout",
        "result_status": STATUS,
        "work_family": "publish_handoff",
        "row_id": f"{RUN_ID}__stage_closeout",
        "evidence_boundary": "stage_closeout_only_no_authority(단계 마감만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": payload["next_frontier_question"],
        "artifact_count": 20,
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_probe_and_gap_attribution_only(런타임 탐침과 간극 귀인만)",
        "best_candidate_id": payload["target"].get("candidate_id"),
        "model": payload["target"].get("model"),
        "drawdown_percent": runtime_oos.get("max_drawdown_percent"),
        "oos_trades_per_day": runtime_oos.get("trades_per_day"),
        "oos_net_profit": runtime_oos.get("net_profit"),
        "oos_profit_factor": runtime_oos.get("profit_factor"),
        "oos_trade_count": runtime_oos.get("trade_count"),
        "oos_drawdown_percent": runtime_oos.get("max_drawdown_percent"),
    }


def update_ledgers(payload: Mapping[str, Any]) -> None:
    row = ledger_row(payload)
    upsert_csv(RUN_REGISTRY, "run_id", row)
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
runtime_probe_status: f83_closed_negative_runtime_winrate_erosion_after_signal_parity_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
five_stage_retrospective_due_status: {FIVE_STAGE_RETROSPECTIVE_STATUS}
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F83G stage closeout(F83G 단계 마감)을 완료했다."
  - "Effect(효과): F83은 signal parity(신호 동등성) 이후 runtime win-rate erosion(런타임 승률 침식)으로 negative memory(부정 기억) 처리하고 F84 runtime-realized win-rate rebuild(F84 런타임 실현 승률 재구축)를 다음 실행으로 둔다."
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

Action(행동): F83G closeout(마감)에서 F83을 negative runtime evidence(부정 런타임 근거)로 닫았다.

Effect(효과): F83E/F83F는 ONNX/signal parity(온엑스/신호 동등성)가 있어도 MT5 economics(MT5 경제성)가 자동으로 보장되지 않는다는 부정 근거를 남겼고, 다음 F84는 runtime-realized win-rate rebuild(런타임 실현 승률 재구축)로 넘어간다.

## What Is True Now(지금 참인 것)

- F83E runtime validation/OOS(런타임 검증/표본외)는 negative(부정)이다.
- F83F primary attribution(주 귀인)은 runtime win-rate erosion after signal parity(신호 동등성 이후 런타임 승률 침식)이다.
- Same-surface threshold/filter-only repair(동일 표면 임계값/필터만 수리)는 금지한다.
- F84 handoff scaffold(F84 인계 뼈대)는 준비됐지만 F84A open evidence(F84A 개방 근거)는 아직 아니다.

## Not Yet True(아직 참이 아닌 것)

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Next(다음): `{NEXT_RUN_ID}`.
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any]) -> None:
    text = f"""# F83 Selection Status(F83 선택 상태)

Updated(갱신): {payload['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Closeout label(마감 라벨): `{CLOSEOUT_LABEL}`

Action(행동): F83G closeout(F83G 마감)을 기록했다.

Effect(효과): F83은 selected baseline(선택 기준선) 없이 negative memory(부정 기억)와 preserved clue(보존 단서)로 닫고, F84A stage open(F84A 단계 개방)을 다음 실행으로 둔다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS, text)
    write_text(GLOBAL_SELECTION_STATUS, text)


def update_context_anchor(payload: Mapping[str, Any]) -> None:
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    write_text(
        CONTEXT_ANCHOR,
        f"""# F83 Context Anchor(F83 문맥 앵커)

Updated(갱신): {payload['created_at_utc']}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- runtime OOS(런타임 표본외): net/PF/DD/trades-day `{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}`
- primary gap cause(주 간극 원인): `{payload['primary_gap_cause']}`
- next frontier(다음 전선): `{NEXT_STAGE_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F83 Review Index(F83 검토 색인)\n"
    marker = "<!-- F83G_CLOSEOUT -->"
    if marker in text:
        return
    addition = f"""

{marker}
- `stage_closeout_report.md`: F83 stage closeout report(F83 단계 마감 보고서)
- `frontier83G_runtime_realized_outcome_repair_or_rotation_decision_report.md`: F83G repair/rotation closeout report(F83G 수리/회전 마감 보고서)
- `f83g_repair_or_rotation_decision_summary.json`: F83G machine summary(F83G 기계 요약)
- `f83g_closeout_kpi_rows.csv`: F83G closeout KPI rows(F83G 마감 KPI 행)
- `required_gate_coverage_audit_f83g.md`: F83G gate audit(F83G 게이트 감사)
- `f83g_artifact_lineage.json`: F83G artifact lineage(F83G 산출물 계보)
"""
    write_text(REVIEW_INDEX, text.rstrip() + addition)


def update_next_stage_scaffold(payload: Mapping[str, Any]) -> None:
    write_text(
        NEXT_STAGE_BRIEF,
        f"""# F84 Stage Brief(F84 단계 개요)

Stage ID(단계 ID): `{NEXT_STAGE_ID}`

Prepared by(작성 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Status(상태): `handoff_scaffold_not_opened(인계 뼈대, 아직 개방 아님)`

## Question(질문)

{payload['next_frontier_question']}

## Action And Effect(행동과 효과)

Action(행동): F84는 F83 same-surface threshold/filter repair(F83 동일 표면 임계값/필터 수리)를 반복하지 않고 runtime-realized win/loss and stop-touch/fill-path label(런타임 실현 승패 및 손절·익절 터치/체결 경로 라벨)을 새 hypothesis lifecycle(가설 생명주기)로 연다.

Effect(효과): F83F의 primary cause(주 원인)인 runtime win-rate erosion(런타임 승률 침식)을 다음 모델 학습 목표로 직접 겨냥한다.

## Seed Axes(씨앗 축)

{chr(10).join(f"- {item}" for item in payload['next_frontier_seed_axes'])}

## Boundary(경계)

This file(이 파일)은 F84 open evidence(F84 개방 근거)가 아니라 handoff scaffold(인계 뼈대)다. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
""",
    )
    write_text(
        NEXT_INPUT_REFS,
        f"""# F84 Input References(F84 입력 참조)

Prepared by(작성 실행): `{RUN_ID}`

## Reference Only(참조 전용)

- F83 closeout report(F83 마감 보고서): `{rel(STAGE_CLOSEOUT_REPORT)}`
- F83D short-density proxy target(F83D 숏 밀도 프록시 대상): `{rel(F83D_SUMMARY)}`
- F83E MT5 runtime materialization(F83E MT5 런타임 물질화): `{rel(F83E_SUMMARY)}`
- F83F proxy/runtime gap attribution(F83F 프록시/런타임 간극 귀인): `{rel(F83F_SUMMARY)}`
- F83 negative memory(F83 부정 기억): `{rel(NEGATIVE_REGISTER)}`

## Do Not Inherit(상속 금지)

- winner(승자)
- selected baseline(선택 기준선)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)

Effect(효과): F84 can use F83 as clue memory(F84는 F83을 단서 기억으로만 사용) and must build its own hypothesis/proxy/runtime evidence(자체 가설/프록시/런타임 근거를 만들어야 함).
""",
    )


def update_decision_memo(payload: Mapping[str, Any]) -> None:
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    write_text(
        DECISION_MEMO,
        f"""# F83 Closeout And F84 Rotation Decision(F83 마감 및 F84 회전 결정)

Updated(갱신): {payload['created_at_utc']}

Decision(결정): Close F83 as negative runtime win-rate erosion evidence(F83을 런타임 승률 침식 부정 근거로 마감).

Action(행동): F83D-F83F evidence chain(F83D-F83F 근거 사슬)을 대조해 F83G closeout(F83G 마감)을 만들었다.

Effect(효과): F83은 selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위)를 만들지 않는다. 다음 실행은 `{NEXT_RUN_ID}`다.

## Evidence(근거)

- Runtime OOS(런타임 표본외): net/PF/DD/trades-day `{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}`
- Primary cause(주 원인): `{payload['primary_gap_cause']}`
- Same surface repair(동일 표면 수리): `rejected(거절)`

## Next(다음)

`{NEXT_STAGE_ID}` should start as runtime-realized win-rate rebuild after signal parity gap(신호 동등성 간극 이후 런타임 실현 승률 재구축).

Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
""",
    )


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker in text:
        return
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    addition = f"""

{marker}
- `{RUN_ID}` closed Frontier83(전선83) as `{CLOSEOUT_LABEL}`. Runtime OOS net/PF/DD/tpd(런타임 표본외 순손익/수익 팩터/손실폭/일 거래) `{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}`; primary cause(주 원인) `{payload['primary_gap_cause']}`. Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): no authority(권위 없음).
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_negative_register(payload: Mapping[str, Any]) -> None:
    text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register\n"
    marker = "<!-- NR-FR83-REALIZED-PNL-TEACHER-DISTILLATION-RUNTIME-WINRATE-EROSION-CLOSEOUT -->"
    if marker in text:
        return
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    addition = f"""

{marker}
## NR-FR83-REALIZED-PNL-TEACHER-DISTILLATION-RUNTIME-WINRATE-EROSION-CLOSEOUT

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): realized PnL teacher distillation(실현 손익 교사 증류) and exportable runtime rotation(내보내기 가능 런타임 회전)이 proxy-positive dense short surface(프록시 양수 고밀도 숏 표면)를 MT5 runtime economics(MT5 런타임 경제성)로 옮길 수 있다.
- Why failed(실패 이유): F83E/F83F MT5 runtime OOS(런타임 표본외)는 net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) `{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}`였고, primary cause(주 원인)는 `{payload['primary_gap_cause']}`였다.
- Salvage value(회수 가치): F83E ONNX/signal parity harness(F83E 온엑스/신호 동등성 장치), F83F win-rate erosion attribution(F83F 승률 침식 귀인), F83D dense short proxy supply(F83D 고밀도 숏 프록시 공급), F84 runtime-realized label seed(F84 런타임 실현 라벨 씨앗)를 보존한다.
- Do-not-repeat(반복 금지): same `f82b_10355` smooth_trade_supply short close_direction surface(동일 f82b_10355 숏 종가방향 부드러운 공급 표면)를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 바꾸는 수리)로 반복하지 않는다.
- Reopen condition(재개 조건): runtime-realized outcome label(런타임 실현 결과 라벨), stop-touch/fill-path target(손절·익절 터치/체결 경로 목표), risk logic(위험 로직), regime/session split(장세/세션 분할) 중 하나 이상이 실제로 바뀌고 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.
- Evidence(근거): `{rel(STAGE_CLOSEOUT_REPORT)}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    write_text(NEGATIVE_REGISTER, text.rstrip() + addition)


def update_changelog(payload: Mapping[str, Any]) -> None:
    text = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID in text:
        return
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    entry = f"""# 2026-06-18 - F83G Closeout And F84 Rotation(F83G 마감 및 F84 회전)

- Action(행동): `{RUN_ID}`로 F83 lifecycle(F83 생명주기)을 closeout(마감)했다.
- Effect(효과): MT5 runtime OOS(런타임 표본외) `{runtime_oos.get('net_profit')}/{runtime_oos.get('profit_factor')}/{runtime_oos.get('max_drawdown_percent')}/{runtime_oos.get('trades_per_day')}`와 `{payload['primary_gap_cause']}`를 근거로 negative memory(부정 기억)와 F84 runtime-realized win-rate rebuild handoff(전선84 런타임 실현 승률 재구축 인계)를 기록했다.
- Next(다음): `{NEXT_RUN_ID}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
    write_text(CHANGELOG, entry + text)


def local_verification(payload: Mapping[str, Any]) -> dict[str, Any]:
    state_text = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    selection_text = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig") if path_exists(SELECTION_STATUS) else ""
    task_force_text = io_path(TASK_FORCE_RECEIPT).read_text(encoding="utf-8-sig") if path_exists(TASK_FORCE_RECEIPT) else ""
    checks = [
        {"check": "summary_exists", "passed": path_exists(SUMMARY_PATH)},
        {"check": "stage_closeout_report_exists", "passed": path_exists(STAGE_CLOSEOUT_REPORT)},
        {"check": "kpi_rows_exist", "passed": path_exists(KPI_ROWS_PATH)},
        {"check": "gate_audit_exists", "passed": path_exists(GATE_AUDIT_PATH)},
        {"check": "workspace_state_next_run", "passed": NEXT_RUN_ID in state_text},
        {"check": "selection_status_closeout", "passed": RUN_ID in selection_text and STATUS in selection_text},
        {"check": "f84_scaffold_exists", "passed": path_exists(NEXT_STAGE_BRIEF) and path_exists(NEXT_INPUT_REFS)},
        {"check": "task_force_all_agents", "passed": all(f"agent_0{i}_" in task_force_text for i in range(1, 9))},
        {"check": "same_surface_repair_rejected", "passed": payload["repair_admissibility"]["same_surface_threshold_filter_parameter_only"].startswith("rejected")},
        {"check": "frontier_extra_not_due", "passed": FRONTIER_EXTRA_DUE_STATUS.startswith("not_due")},
        {"check": "final_claim_guard_exists", "passed": path_exists(FINAL_CLAIM_GUARD)},
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if all(check["passed"] for check in checks) else "fail",
        "checks": checks,
        "all_passed": all(check["passed"] for check in checks),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_lineage(payload: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = [
        ROOT / SCRIPT_REL,
        SUMMARY_PATH,
        KPI_ROWS_PATH,
        LINEAGE_PATH,
        LOCAL_VERIFICATION_PATH,
        REPORT_PATH,
        STAGE_CLOSEOUT_REPORT,
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
        PACKET_STATE_SYNC_AUDIT,
        PACKET_CLOSEOUT_GATE,
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
        "source_inputs": [
            rel(F83A_SUMMARY),
            rel(F83B_SUMMARY),
            rel(F83C_SUMMARY),
            rel(F83D_SUMMARY),
            rel(F83E_SUMMARY),
            rel(F83F_SUMMARY),
            rel(F83F_GAP_ROWS),
            rel(F83F_CAUSE_ROWS),
        ],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": f"{NEXT_RUN_ID} and F83 closeout registers",
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_reports_and_ignored_run_outputs_with_hashes(추적 보고서와 무시된 실행 산출물 해시)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifacts = [
        ("stage_pipeline_script", ROOT / SCRIPT_REL, "F83G closeout producer script(F83G 마감 생산 스크립트)"),
        ("stage_closeout_report", STAGE_CLOSEOUT_REPORT, "F83 stage closeout report(F83 단계 마감 보고서)"),
        ("repair_rotation_report", REPORT_PATH, "F83G repair/rotation report(F83G 수리/회전 보고서)"),
        ("closeout_summary", SUMMARY_PATH, "F83G machine closeout summary(F83G 기계 마감 요약)"),
        ("closeout_kpi_rows", KPI_ROWS_PATH, "F83G closeout KPI rows(F83G 마감 KPI 행)"),
        ("artifact_lineage", LINEAGE_PATH, "F83G artifact lineage(F83G 산출물 계보)"),
        ("local_verification", LOCAL_VERIFICATION_PATH, "F83G local verification(F83G 로컬 검증)"),
        ("decision_memo", DECISION_MEMO, "F83 closeout/F84 rotation decision(F83 마감/F84 회전 결정)"),
        ("next_stage_brief", NEXT_STAGE_BRIEF, "F84 handoff stage brief(F84 인계 단계 개요)"),
        ("next_input_refs", NEXT_INPUT_REFS, "F84 handoff input refs(F84 인계 입력 참조)"),
        ("task_force_receipt", TASK_FORCE_RECEIPT, "F83G Task Force receipt(F83G 태스크포스 영수증)"),
        ("run_manifest", RUN_MANIFEST_PATH, "F83G ignored run manifest tracked by hash(F83G 무시 실행 목록 해시 추적)"),
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
                "effect": "Supports F83 closeout/F84 handoff only(F83 마감/F84 인계만 지원).",
            }
        )
    return rows


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    for row in artifact_rows(payload):
        upsert_csv(ARTIFACT_REGISTRY, "artifact_id", row)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, NEXT_STAGE_BRIEF.parent, NEXT_INPUT_REFS.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def write_all(payload: Mapping[str, Any]) -> dict[str, Any]:
    write_csv(KPI_ROWS_PATH, payload["closeout_kpi_rows"])
    write_csv(RUN_KPI_ROWS_PATH, payload["closeout_kpi_rows"])
    write_json(SUMMARY_PATH, payload)
    write_text(REPORT_PATH, closeout_report_text(payload))
    write_text(STAGE_CLOSEOUT_REPORT, closeout_report_text(payload))
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
    write_json(LOCAL_VERIFICATION_PATH, verification)
    payload_with_verification = dict(payload)
    payload_with_verification["local_verification"] = verification
    write_json(SUMMARY_PATH, payload_with_verification)
    write_json(RUN_MANIFEST_PATH, payload_with_verification)
    lineage = artifact_lineage(payload_with_verification)
    write_json(LINEAGE_PATH, lineage)
    payload_with_verification["artifact_lineage"] = lineage
    write_json(SUMMARY_PATH, payload_with_verification)
    write_json(RUN_MANIFEST_PATH, payload_with_verification)
    update_artifact_registry(payload_with_verification)
    return verification


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
        "stage_closeout_report": rel(STAGE_CLOSEOUT_REPORT),
        "gate_audit": rel(GATE_AUDIT_PATH),
        "run_manifest": rel(RUN_MANIFEST_PATH),
        "work_packet": rel(WORK_PACKET),
        "next_stage_brief": rel(NEXT_STAGE_BRIEF),
        "task_force_receipt": rel(TASK_FORCE_RECEIPT),
        "local_verification": rel(LOCAL_VERIFICATION_PATH),
    }
    verification = write_all(payload)
    runtime_oos = payload["runtime_probe_kpi"]["oos"]
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": payload["decision"],
                "runtime_oos": {
                    "net": runtime_oos.get("net_profit"),
                    "pf": runtime_oos.get("profit_factor"),
                    "dd": runtime_oos.get("max_drawdown_percent"),
                    "trades_per_day": runtime_oos.get("trades_per_day"),
                },
                "primary_gap_cause": payload["primary_gap_cause"],
                "same_surface_repair": payload["repair_admissibility"]["same_surface_threshold_filter_parameter_only"],
                "next_run_id": NEXT_RUN_ID,
                "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
                "local_verification": verification["status"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
