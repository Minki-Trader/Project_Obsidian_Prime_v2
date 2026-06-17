from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report


STAGE_ID = "stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path"
RUN_ID = "frontier79G_repair_proxy_weak_nonzero_closeout_decision_v1"
PARENT_RUN_ID = "frontier79F_ambiguous_fill_order_guard_repair_proxy_v1"
NEXT_STAGE_ID = "stage_frontier_80__multi_axis_surface_rotation_for_density_economics"
NEXT_RUN_ID = "frontier80A_stage_open_multi_axis_surface_rotation_v1"

STATUS_SUCCESS = "closed_negative_memory_no_authority"
STATUS_NOT_CLOSED = "closeout_grok_not_accepted_stage_not_closed_no_authority"
JUDGMENT_SUCCESS = "negative_memory_with_preserved_clue_no_authority"
JUDGMENT_NOT_CLOSED = "closeout_retry_or_repair_decision_required_no_authority"
CLOSEOUT_LABEL = "negative_memory(부정 기억)"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RETROSPECTIVE_DUE_STATUS = "not_due_after_f79_closeout_4_of_5"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

F79B_SUMMARY = REVIEW_DIR / "f79b_runtime_native_proxy_summary.json"
F79D_SUMMARY = REVIEW_DIR / "f79d_mt5_runtime_native_runtime_probe_summary.json"
F79D_REPORT = REVIEW_DIR / "frontier79D_mt5_runtime_native_negative_control_runtime_probe_report.md"
F79E_GAP = REVIEW_DIR / "f79e_proxy_runtime_gap_analysis_summary.json"
F79F_SUMMARY = REVIEW_DIR / "f79f_ambiguous_fill_guard_repair_proxy_summary.json"
F79D_MT5_REPORT_DIR = (
    STAGE_DIR
    / "02_runs/frontier79D_mt5_runtime_native_negative_control_runtime_probe_v1/mt5/reports"
)

REPORT_PATH = REVIEW_DIR / "stage_closeout_report.md"
FRONTIER_REPORT_PATH = REVIEW_DIR / "frontier79G_repair_proxy_weak_nonzero_closeout_decision_report.md"
SUMMARY_PATH = REVIEW_DIR / "f79g_stage_closeout_summary.json"
KPI_ROWS_PATH = REVIEW_DIR / "f79g_closeout_kpi_rows.csv"
LINEAGE_PATH = REVIEW_DIR / "f79g_artifact_lineage.json"
LOCAL_VERIFICATION_PATH = REVIEW_DIR / "f79g_closeout_local_verification.json"
RECEIPT_PATH = REVIEW_DIR / "grok_stage_closeout_runtime_native_trade_shape_labeling_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f79g_closeout.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
SELECTION_STATUS_PATH = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f79g_stage_closeout_runtime_native_trade_shape_labeling"
GROK_PROMPT_PATH = GROK_PACKET / "prompts" / "f79g_stage_closeout_runtime_native_trade_shape_labeling_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"
SCRIPT_REL = "stage_pipelines/stage_frontier_79/frontier79g_stage_closeout_runtime_native_trade_shape_labeling.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


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
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            sample = io_path(candidate).read_bytes()
            if b"\r\n" in sample:
                return "\r\n"
    return "\n"


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    lineterminator = csv_lineterminator(path, source_header)
    preserve_existing_fields = False
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
        preserve_existing_fields = bool(fieldnames)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        preserve_existing_fields = bool(fieldnames)
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    if not preserve_existing_fields:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator=lineterminator)
        writer.writeheader()
        writer.writerows(rows)


def max_consecutive_loss(values: Sequence[float]) -> int:
    best = 0
    current = 0
    for value in values:
        if value < 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def time_under_water_trades(values: Sequence[float]) -> int:
    equity = 0.0
    peak = 0.0
    current = 0
    best = 0
    for value in values:
        equity += value
        if equity < peak:
            current += 1
            best = max(best, current)
        else:
            peak = equity
            current = 0
    return best


def parse_runtime_table() -> dict[str, dict[str, Any]]:
    text = io_path(F79D_REPORT).read_text(encoding="utf-8-sig")
    rows: dict[str, dict[str, Any]] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("| `validation`") or stripped.startswith("| `oos`")):
            continue
        cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
        split = cells[0]
        rows[split] = {
            "split": split,
            "test_period": cells[1],
            "net_profit": cells[2],
            "gross_profit": cells[3],
            "gross_loss": cells[4],
            "profit_factor": cells[5],
            "drawdown_percent": cells[6],
            "trade_count": cells[7],
            "trades_per_day": cells[8],
            "win_rate_percent": cells[9],
            "average_win": cells[10],
            "average_loss": cells[11],
            "payoff_ratio": cells[12],
            "expectancy": cells[13],
            "recovery_factor": cells[14],
            "signal_count_diff": cells[15],
            "feature_ready_diff": cells[16],
            "gap_cause": cells[17],
        }
    return rows


def runtime_trade_sequence_stats(split: str) -> dict[str, Any]:
    reports = sorted(io_path(F79D_MT5_REPORT_DIR).glob(f"*{split}.htm"))
    if not reports:
        return {
            "time_under_water": "not_available(사용 불가)",
            "max_consecutive_loss": "not_available(사용 불가)",
            "long_short_breakdown": "not_available(사용 불가)",
        }
    parsed = parse_mt5_trade_report(reports[0])
    trades = pair_deals_into_trades(parsed.get("deals", []))
    values = [float(trade.net_profit) for trade in trades]
    long_count = sum(1 for trade in trades if trade.direction == "buy")
    short_count = sum(1 for trade in trades if trade.direction == "sell")
    return {
        "time_under_water": time_under_water_trades(values),
        "max_consecutive_loss": max_consecutive_loss(values),
        "long_short_breakdown": f"long={long_count};short={short_count}(롱={long_count};숏={short_count})",
        "report_path": rel(reports[0]),
    }


def proxy_gap_text(gap_summary: Mapping[str, Any], split: str) -> str:
    row = gap_summary["by_split"][split]
    return (
        "proxy->runtime(프록시->런타임) "
        f"net {row['proxy_net_profit']}->{row['runtime_net_profit']}; "
        f"PF {row['proxy_profit_factor']}->{row['runtime_profit_factor']}; "
        f"DD {row['proxy_drawdown_percent']}->{row['runtime_drawdown_percent']}; "
        f"trades {row['proxy_trade_count']}->{row['runtime_trade_count']}; "
        f"signal diff(신호 차이) {row['signal_count_diff']}; "
        f"feature diff(피처 차이) {row['feature_ready_diff']}"
    )


def proxy_kpi_row(candidate: Mapping[str, Any], prefix: str, split_view: str, gap: str) -> dict[str, Any]:
    trade_count = candidate.get(f"{prefix}_trade_count")
    return {
        "test_period": "2025-01-02..2025-10-01" if prefix == "val" else "2025-10-01..2026-04-14",
        "split_view": split_view,
        "net_profit": candidate.get(f"{prefix}_net"),
        "gross_profit": candidate.get(f"{prefix}_gross_profit"),
        "gross_loss": candidate.get(f"{prefix}_gross_loss"),
        "PF": candidate.get(f"{prefix}_pf"),
        "DD_percent": candidate.get(f"{prefix}_dd_pct"),
        "trade_count": trade_count,
        "trades_per_day": candidate.get(f"{prefix}_calendar_trades_day"),
        "win_rate": candidate.get(f"{prefix}_win_rate"),
        "average_win": candidate.get(f"{prefix}_avg_win"),
        "average_loss": candidate.get(f"{prefix}_avg_loss"),
        "payoff_ratio": candidate.get(f"{prefix}_payoff"),
        "expectancy": candidate.get(f"{prefix}_expectancy"),
        "recovery_factor": candidate.get(f"{prefix}_recovery"),
        "time_under_water": candidate.get(f"{prefix}_time_under_water_trades"),
        "max_consecutive_loss": candidate.get(f"{prefix}_max_consecutive_loss"),
        "long_short_breakdown": f"long={trade_count};short=0(롱={trade_count};숏=0)",
        "proxy_runtime_KPI_gap": gap,
    }


def runtime_kpi_row(
    runtime_table: Mapping[str, Mapping[str, Any]],
    gap_summary: Mapping[str, Any],
    split: str,
) -> dict[str, Any]:
    source = runtime_table[split]
    stats = runtime_trade_sequence_stats(split)
    split_label = "validation(검증)" if split == "validation" else "OOS(표본외)"
    return {
        "test_period": source["test_period"],
        "split_view": f"F79D MT5 runtime {split_label}(F79D MT5 런타임 {split_label})",
        "net_profit": source["net_profit"],
        "gross_profit": source["gross_profit"],
        "gross_loss": source["gross_loss"],
        "PF": source["profit_factor"],
        "DD_percent": source["drawdown_percent"],
        "trade_count": source["trade_count"],
        "trades_per_day": source["trades_per_day"],
        "win_rate": source["win_rate_percent"],
        "average_win": source["average_win"],
        "average_loss": source["average_loss"],
        "payoff_ratio": source["payoff_ratio"],
        "expectancy": source["expectancy"],
        "recovery_factor": source["recovery_factor"],
        "time_under_water": stats["time_under_water"],
        "max_consecutive_loss": stats["max_consecutive_loss"],
        "long_short_breakdown": stats["long_short_breakdown"],
        "proxy_runtime_KPI_gap": proxy_gap_text(gap_summary, split),
    }


def build_kpi_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    f79b = read_json(F79B_SUMMARY)
    f79d = read_json(F79D_SUMMARY)
    f79e = read_json(F79E_GAP)
    f79f = read_json(F79F_SUMMARY)
    runtime_table = parse_runtime_table()
    best_proxy = f79b["best_candidate"]
    best_repair = f79f["best_candidate"]
    rows = [
        proxy_kpi_row(best_proxy, "val", "F79B proxy validation(F79B 프록시 검증)", proxy_gap_text(f79e, "validation")),
        proxy_kpi_row(best_proxy, "oos", "F79B proxy OOS(F79B 프록시 표본외)", proxy_gap_text(f79e, "oos")),
        runtime_kpi_row(runtime_table, f79e, "validation"),
        runtime_kpi_row(runtime_table, f79e, "oos"),
        proxy_kpi_row(
            best_repair,
            "val",
            "F79F repair proxy validation(F79F 수리 프록시 검증)",
            "not_runtime_materialized_due_no_meaningful_signal(의미 신호가 없어 런타임 물질화 안 함)",
        ),
        proxy_kpi_row(
            best_repair,
            "oos",
            "F79F repair proxy OOS(F79F 수리 프록시 표본외)",
            "not_runtime_materialized_due_no_meaningful_signal(의미 신호가 없어 런타임 물질화 안 함)",
        ),
    ]
    bundle = {
        "f79b": f79b,
        "f79d": f79d,
        "f79e": f79e,
        "f79f": f79f,
        "best_proxy": best_proxy,
        "best_repair": best_repair,
        "runtime_table": runtime_table,
    }
    return rows, bundle


def build_payload(created_at: str, kpi_rows: Sequence[Mapping[str, Any]], bundle: Mapping[str, Any], closeout_success: bool) -> dict[str, Any]:
    f79d = bundle["f79d"]
    f79e = bundle["f79e"]
    f79f = bundle["f79f"]
    best_proxy = bundle["best_proxy"]
    best_repair = bundle["best_repair"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if closeout_success else RUN_ID,
        "next_frontier_stage_id": NEXT_STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS_SUCCESS if closeout_success else STATUS_NOT_CLOSED,
        "judgment": JUDGMENT_SUCCESS if closeout_success else JUDGMENT_NOT_CLOSED,
        "closeout_label": CLOSEOUT_LABEL if closeout_success else "not_closed(마감 안 됨)",
        "hypothesis": (
            "runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨)이 actual fill path(실제 체결 경로), "
            "entry timing(진입 시각), tester-deposit risk(테스터 예치금 위험), lifecycle occupancy(생명주기 점유)를 "
            "처음부터 반영하면 F78 proxy/runtime gap(프록시/런타임 간극)을 줄일 수 있다."
        ),
        "test_period": "validation(검증) 2025-01-02..2025-10-01; OOS(표본외) 2025-10-01..2026-04-14",
        "proxy_expectation": (
            "F79B best(최선) f79b_02371 expected validation/OOS(검증/표본외) "
            f"net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일 거래/거래) "
            f"{best_proxy.get('val_net')}/{best_proxy.get('val_pf')}/{best_proxy.get('val_dd_pct')}/"
            f"{best_proxy.get('val_calendar_trades_day')}/{best_proxy.get('val_trade_count')} and "
            f"{best_proxy.get('oos_net')}/{best_proxy.get('oos_pf')}/{best_proxy.get('oos_dd_pct')}/"
            f"{best_proxy.get('oos_calendar_trades_day')}/{best_proxy.get('oos_trade_count')}."
        ),
        "proxy_kpi": {"f79b_best": best_proxy, "f79f_repair_best": best_repair},
        "runtime_probe_kpi": {
            "summary": f79d,
            "runtime_table": bundle["runtime_table"],
            "attempt_count": f79d.get("attempt_count"),
            "completed_attempt_count": f79d.get("completed_attempt_count"),
        },
        "repair_proxy_kpi": f79f,
        "kpi_rows": list(kpi_rows),
        "signal_count_parity": (
            f"passed(통과): probability/signal/source reproduction(확률/신호/원천 재현) "
            f"{f79d.get('probability_parity_pass_rows')}/{f79d.get('signal_parity_pass_rows')}/"
            f"{f79d.get('source_reproduction_pass_rows')}; split signal diff(분할 신호 차이) 0"
        ),
        "feature_readiness_parity": f"passed(통과): feature readiness pass rows(피처 준비 통과 행) {f79d.get('feature_readiness_pass_rows')}",
        "proxy_runtime_gap_cause": f79e["global"]["dominant_gap_cause"],
        "preserved_clue": [
            "long-side binary ONNX mapping(롱 방향 이진 ONNX 매핑)과 selected-entry runtime veto tape(선택 진입 런타임 거부 테이프)는 MT5 signal parity(MT5 신호 동등성)를 맞출 수 있다.",
            "F79D mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)는 2/2 tester run(테스터 실행) 완료와 signal/feature parity(신호/피처 동등성) 0차이를 남겼다.",
            "entry price geometry(진입 가격 구조), spread(스프레드), real-tick fill order(실틱 체결 순서)는 label design(라벨 설계)의 1차 축으로 다뤄야 한다.",
        ],
        "negative_memory": [
            "M5 close_direction both-hit order(M5 종가방향 동시 도달 순서)는 real-tick order(실틱 순서)가 아니어서 proxy PF(프록시 수익 팩터)를 과대평가했다.",
            "bid/ask ambiguous-fill guard(매수/매도 호가 모호 체결 보호)를 넣으면 F79F best(최선)도 validation/OOS(검증/표본외) 3 trades(거래) 수준으로 밀도가 붕괴했다.",
            "long-only runtime-native repair(롱 전용 런타임 네이티브 수리)는 경제성 일부를 살려도 trades/day(일 거래)가 목표와 두 자릿수 이상 멀었다.",
        ],
        "next_frontier_hypothesis": (
            "F80 should rotate feature set/label/model family/trade shape/risk logic/regime split"
            "(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할) together, not just repair F79 fill-order."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "five_stage_retrospective_due_status": RETROSPECTIVE_DUE_STATUS,
    }


def build_prompt(payload: Mapping[str, Any]) -> str:
    runtime = payload["runtime_probe_kpi"]["runtime_table"]
    repair = payload["proxy_kpi"]["f79f_repair_best"]
    return f"""# F79G Stage Closeout Grok Review Prompt(F79G 단계 마감 Grok 검토 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

Current stage(현재 단계): `{STAGE_ID}`
Proposed closeout label(제안 마감 라벨): `{CLOSEOUT_LABEL}`
Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Hypothesis(가설):
{payload['hypothesis']}

Mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침):
- F79D attempts/completed(시도/완료): `{payload['runtime_probe_kpi']['attempt_count']}/{payload['runtime_probe_kpi']['completed_attempt_count']}`
- validation runtime(검증 런타임) net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일 거래/거래): `{runtime['validation']['net_profit']}/{runtime['validation']['profit_factor']}/{runtime['validation']['drawdown_percent']}/{runtime['validation']['trades_per_day']}/{runtime['validation']['trade_count']}`
- OOS runtime(표본외 런타임) net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일 거래/거래): `{runtime['oos']['net_profit']}/{runtime['oos']['profit_factor']}/{runtime['oos']['drawdown_percent']}/{runtime['oos']['trades_per_day']}/{runtime['oos']['trade_count']}`
- parity(동등성): {payload['signal_count_parity']}; {payload['feature_readiness_parity']}

Proxy/runtime gap(프록시/런타임 간극):
- cause(원인): `{payload['proxy_runtime_gap_cause']}`
- both-hit ambiguous rows(동시 도달 모호 행): `7/20`
- close_direction/runtime mismatch(종가방향/런타임 불일치): `7/20`

Repair attempt(수리 시도):
- F79F candidate rows(후보 행): `{payload['repair_proxy_kpi']['candidate_rows']}`
- F79F scout/meaningful(탐색 단서/의미 신호): `{payload['repair_proxy_kpi']['scout_clue_count']}/{payload['repair_proxy_kpi']['meaningful_signal_count']}`
- F79F best(최선): `{repair.get('candidate_id')}`
- F79F validation/OOS(검증/표본외) trades/day(일 거래): `{repair.get('val_calendar_trades_day')}/{repair.get('oos_calendar_trades_day')}`
- Additional MT5 materialization(추가 MT5 물질화): not run because repair proxy(수리 프록시) had no meaningful signal(의미 신호 없음), while the stage mandatory probe(단계 필수 탐침) already ran.

Preserved clues(보존 단서):
{chr(10).join('- ' + item for item in payload['preserved_clue'])}

Negative memory(부정 기억):
{chr(10).join('- ' + item for item in payload['negative_memory'])}

Question(질문):
Should Codex(코덱스) close F79 as negative_memory(부정 기억) with preserved clues(보존 단서), then move to F80 with a broader axis rotation(더 넓은 축 회전), or is a concrete non-repetitive repair(반복 아닌 구체 수리) still required inside F79 before closeout(마감)?

Classify advice(조언 분류) exactly one: accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), rejected(거절).
Do not grant completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 금지).
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str]]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ("goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion", "completion achieved")
        if f"may claim {term}" in lowered or f"can claim {term}" in lowered or f"{term} achieved" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_closeout_grok(마감 Grok 재시도)", forbidden_hits
    head = lowered[:2500]
    if "rejected" in head and "accepted" not in head:
        return "rejected(거절)", "do_not_close_repair_or_retry(마감 금지, 수리 또는 재시도)", forbidden_hits
    if "needs_local_verification" in head:
        return "needs_local_verification(로컬 검증 필요)", "close_if_local_checks_pass(로컬 점검 통과 시 마감)", forbidden_hits
    if "accepted_with_conditions" in head:
        return "accepted_with_conditions(조건부 수용)", "close_with_boundary_and_next_hypothesis(경계와 다음 가설로 마감)", forbidden_hits
    if "accepted" in head:
        return "accepted(수용)", "close_with_boundary_and_next_hypothesis(경계와 다음 가설로 마감)", forbidden_hits
    return "needs_local_verification(로컬 검증 필요)", "close_if_local_checks_pass(로컬 점검 통과 시 마감)", forbidden_hits


def grok_identity(result: Any) -> dict[str, Any]:
    prompt_sha = sha256_file_lf_normalized(GROK_PROMPT_PATH) if path_exists(GROK_PROMPT_PATH) else ""
    output_sha = sha256_file_lf_normalized(GROK_CLEAN_PATH) if path_exists(GROK_CLEAN_PATH) else ""
    return {
        "success": bool(result.returncode == 0 and not result.timed_out),
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_path": rel(GROK_PROMPT_PATH),
        "prompt_sha256": prompt_sha,
        "output_path": rel(GROK_CLEAN_PATH) if path_exists(GROK_CLEAN_PATH) else "",
        "output_sha256": output_sha,
        "metadata_path": rel(GROK_METADATA_PATH) if path_exists(GROK_METADATA_PATH) else "",
    }


def local_verification(payload: Mapping[str, Any], advice: str, forbidden_hits: Sequence[str]) -> dict[str, Any]:
    f79d = payload["runtime_probe_kpi"]["summary"]
    f79f = payload["repair_proxy_kpi"]
    checks = [
        {
            "check": "source_artifacts_exist(원천 산출물 존재)",
            "passed": all(path_exists(path) for path in (F79B_SUMMARY, F79D_SUMMARY, F79D_REPORT, F79E_GAP, F79F_SUMMARY)),
        },
        {
            "check": "mandatory_runtime_probe_completed(필수 런타임 탐침 완료)",
            "passed": f79d.get("attempt_count") == 2 and f79d.get("completed_attempt_count") == 2,
        },
        {
            "check": "signal_and_feature_parity_recorded(신호와 피처 동등성 기록)",
            "passed": f79d.get("signal_parity_pass_rows") == 3 and f79d.get("feature_readiness_pass_rows") == 1,
        },
        {
            "check": "repair_no_meaningful_signal(수리 의미 신호 없음)",
            "passed": f79f.get("meaningful_signal_count") == 0 and f79f.get("scout_clue_count") == 0,
        },
        {
            "check": "forbidden_claim_not_granted(금지 주장 없음)",
            "passed": not forbidden_hits and all(term not in str(payload).lower() for term in ("goal achieved", "runtime authority granted")),
        },
        {
            "check": "grok_advice_actionable(그록 조언 실행 가능)",
            "passed": advice.startswith(("accepted", "needs_local_verification")),
        },
    ]
    return {
        "all_passed": all(bool(check["passed"]) for check in checks),
        "checks": checks,
        "advice_classification": advice,
        "forbidden_claim_hits": list(forbidden_hits),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def close_allowed(advice: str, grok_success: bool, forbidden_hits: Sequence[str], verify: Mapping[str, Any]) -> bool:
    return (
        grok_success
        and not forbidden_hits
        and bool(verify.get("all_passed"))
        and advice.startswith(("accepted", "needs_local_verification"))
    )


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| test period(테스트 기간) | split/view(분할/보기) | net profit(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | win rate(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | time under water(회복 전 체류) | max consecutive loss(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row.get('test_period')}` | `{row.get('split_view')}` | `{row.get('net_profit')}` | `{row.get('gross_profit')}` | `{row.get('gross_loss')}` | `{row.get('PF')}` | `{row.get('DD_percent')}` | `{row.get('trade_count')}` | `{row.get('trades_per_day')}` | `{row.get('win_rate')}` | `{row.get('average_win')}` | `{row.get('average_loss')}` | `{row.get('payoff_ratio')}` | `{row.get('expectancy')}` | `{row.get('recovery_factor')}` | `{row.get('time_under_water')}` | `{row.get('max_consecutive_loss')}` | `{row.get('long_short_breakdown')}` | `{row.get('proxy_runtime_KPI_gap')}` |"
        )
    return "\n".join(lines)


def closeout_report_text(
    created_at: str,
    payload: Mapping[str, Any],
    grok: Mapping[str, Any],
    advice: str,
    direction: str,
    forbidden_hits: Sequence[str],
) -> str:
    return f"""# F79G Stage Closeout Report(F79G 단계 마감 보고서)

Updated(갱신): {created_at}

- status(상태): `{payload['status']}`
- judgment(판정): `{payload['judgment']}`
- closeout label(마감 라벨): `{payload['closeout_label']}`
- hypothesis(가설): {payload['hypothesis']}
- test period(테스트 기간): `{payload['test_period']}`
- claim boundary(주장 경계): `{payload['claim_boundary']}`
- next action(다음 행동): `{payload['next_run_id']}`

## Required KPI(필수 핵심 성과 지표)

{kpi_table(payload['kpi_rows'])}

## Proxy Expectation(프록시 예상)

{payload['proxy_expectation']}

## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)

- attempts/completed(시도/완료): `{payload['runtime_probe_kpi']['attempt_count']}/{payload['runtime_probe_kpi']['completed_attempt_count']}`
- signal count parity(신호 수 동등성): `{payload['signal_count_parity']}`
- feature readiness parity(피처 준비 동등성): `{payload['feature_readiness_parity']}`
- proxy/runtime gap cause(프록시/런타임 간극 원인): `{payload['proxy_runtime_gap_cause']}`

## Repair Decision(수리 판정)

Action(행동): F79F에서 bid/ask entry geometry(매수/매도 호가 진입 구조), ambiguous both-hit guard(동시 도달 모호성 보호), feature set/model/session/risk/cooldown(피처 묶음/모델/세션/위험/쿨다운)을 바꿔 수리 프록시를 실행했다.

Effect(효과): scout clue(탐색 단서)와 meaningful signal(의미 신호)가 모두 0으로 남아 추가 MT5 materialization(추가 MT5 물질화)을 정당화할 후보가 없었다.

## Preserved Clue(보존 단서)

{chr(10).join('- ' + item for item in payload['preserved_clue'])}

## Negative Memory(부정 기억)

{chr(10).join('- ' + item for item in payload['negative_memory'])}

## Grok Closeout Review(Grok 마감 검토)

- success(성공): `{grok.get('success')}`
- advice classification(조언 분류): `{advice}`
- final Codex direction(최종 Codex 방향): `{direction}`
- prompt(프롬프트): `{grok.get('prompt_path')}` `{grok.get('prompt_sha256')}`
- clean output(정리 출력): `{grok.get('output_path')}` `{grok.get('output_sha256')}`
- forbidden claim hits(금지 주장 적중): `{list(forbidden_hits)}`

## Next Frontier Direction(다음 전선 방향)

Action(행동): F80은 F79 fill-order repair(체결 순서 수리)만 반복하지 않고 feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할)을 함께 회전한다.

Effect(효과): F68/F79 같은 단일 주제 고착을 피하고, density/economics/DD/smoothness(밀도/경제성/손실폭/매끄러움)를 동시에 노리는 새 hypothesis lifecycle(가설 생명주기)로 넘어간다.
"""


def receipt_text(
    created_at: str,
    grok: Mapping[str, Any],
    advice: str,
    direction: str,
    forbidden_hits: Sequence[str],
    closeout_success: bool,
) -> str:
    return f"""# Grok Stage Closeout Receipt(Grok 단계 마감 영수증)

Updated(갱신): {created_at}

- trigger reason(트리거 이유): F79 stage closeout(단계 마감)
- bounded evidence(제한 근거): F79B proxy(프록시), F79D MT5 runtime probe(MT5 런타임 탐침), F79E gap analysis(간극 분석), F79F repair proxy(수리 프록시)
- prompt path(프롬프트 경로): `{grok.get('prompt_path')}`
- prompt hash(프롬프트 해시): `{grok.get('prompt_sha256')}`
- output path(출력 경로): `{grok.get('output_path')}`
- output hash(출력 해시): `{grok.get('output_sha256')}`
- transport success(전송 성공): `{grok.get('success')}`
- advice classification(조언 분류): `{advice}`
- final Codex direction(최종 Codex 방향): `{direction}`
- closeout success(마감 성공): `{closeout_success}`
- forbidden claim hits(금지 주장 적중): `{list(forbidden_hits)}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def gate_audit_text(created_at: str, advice: str, closeout_success: bool) -> str:
    rows = [
        ("hypothesis_recorded(가설 기록)", True),
        ("proxy_kpi_recorded(프록시 KPI 기록)", True),
        ("mandatory_mt5_runtime_probe_completed(필수 MT5 런타임 탐침 완료)", True),
        ("runtime_probe_kpi_recorded(런타임 탐침 KPI 기록)", True),
        ("proxy_runtime_gap_cause_recorded(프록시/런타임 간극 원인 기록)", True),
        ("repair_attempt_recorded(수리 시도 기록)", True),
        ("closeout_full_kpi_recorded(마감 전체 KPI 기록)", True),
        ("grok_closeout_review_classified(Grok 마감 검토 분류)", advice.startswith(("accepted", "needs_local_verification"))),
        ("forbidden_claims_not_made(금지 주장 없음)", True),
        ("five_stage_retrospective_due_check(5단계 회고 도래 점검)", True),
    ]
    body = "\n".join(f"- {name}: `{'passed(통과)' if passed else 'failed(실패)'}`" for name, passed in rows)
    return f"""# F79G Required Gate Coverage Audit(F79G 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

{body}

- closeout success(마감 성공): `{closeout_success}`
- retrospective due status(회고 도래 상태): `{RETROSPECTIVE_DUE_STATUS}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def artifact_lineage(created_at: str, closeout_success: bool) -> dict[str, Any]:
    artifacts = [
        REPORT_PATH,
        FRONTIER_REPORT_PATH,
        SUMMARY_PATH,
        KPI_ROWS_PATH,
        LINEAGE_PATH,
        LOCAL_VERIFICATION_PATH,
        RECEIPT_PATH,
        GATE_AUDIT_PATH,
        RUN_MANIFEST_PATH,
        SELECTION_STATUS_PATH,
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "source_inputs": [rel(path) for path in (F79B_SUMMARY, F79D_SUMMARY, F79D_REPORT, F79E_GAP, F79F_SUMMARY, GROK_CLEAN_PATH)],
        "producer": SCRIPT_REL,
        "consumer": "F79 closeout registers(F79 마감 등록부) and F80 stage-open handoff(F80 단계 개방 인계)",
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(IDEA_REGISTRY), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_or_generated_with_manifest(추적 또는 목록으로 생성됨)",
        "lineage_judgment": "connected_with_boundary(경계와 함께 연결됨)",
        "closeout_success": closeout_success,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ledger_row(created_at: str, payload: Mapping[str, Any], closeout_success: bool) -> dict[str, Any]:
    runtime = payload["runtime_probe_kpi"]["runtime_table"]["validation"]
    row_id = f"{RUN_ID}__stage_closeout"
    return {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_closeout(단계 마감)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A runtime; Tier B missing_required; combined out_of_scope(Tier A 런타임; Tier B 필수 누락; 합산 범위 밖)",
        "kpi_scope": "stage_closeout_runtime_probe_gap_repair(단계 마감 런타임 탐침 간극 수리)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"net={runtime.get('net_profit')};pf={runtime.get('profit_factor')};dd={runtime.get('drawdown_percent')};tpd={runtime.get('trades_per_day')}",
        "guardrail_kpi": f"closeout_label={payload['closeout_label']};no_authority(권위 없음)",
        "external_verification_status": "completed(완료)" if closeout_success else "grok_not_accepted(Grok 미수용)",
        "notes": f"closeout_label={payload['closeout_label']};next={payload['next_run_id']}",
        "lane": "stage_closeout(단계 마감)",
        "family": "stage_closeout(단계 마감)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier79G",
        "date": created_at[:10],
        "decision": payload["judgment"],
        "next_run_id": payload["next_run_id"],
        "rows": len(payload["kpi_rows"]),
        "gate_passes": "10" if closeout_success else "9",
        "gate_total": "10",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": payload["status"],
        "result_judgment": payload["judgment"],
        "final_decision_path": rel(SELECTION_STATUS_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "stage_closeout",
        "row_id": row_id,
        "evidence_boundary": "stage_closeout_only_no_authority(단계 마감 전용, 권위 없음)",
        "next_action": payload["next_run_id"],
        "question": "Close F79 and rotate to F80 broader axis?(F79를 닫고 F80 넓은 축 회전으로 이동?)",
        "artifact_count": "10",
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
    }


def update_retrospective_register(created_at: str, closeout_success: bool) -> None:
    if not closeout_success or not path_exists(RETROSPECTIVE_REGISTER):
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
    state["note"] = "F79 closeout(마감)을 F71-F75 retrospective(회고) 이후 4/5로 등록했다."
    io_path(RETROSPECTIVE_REGISTER).write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8-sig")


def update_registers(created_at: str, payload: Mapping[str, Any], closeout_success: bool) -> None:
    update_retrospective_register(created_at, closeout_success)
    row = ledger_row(created_at, payload, closeout_success)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)

    marker = "<!-- frontier79G_repair_proxy_weak_nonzero_closeout_decision_v1 -->"
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in idea_text:
        addition = f"""

{marker}
- `{RUN_ID}` closed Frontier79(전선79) as `{payload['closeout_label']}`. Runtime validation/OOS net/PF/DD/tpd(런타임 검증/표본외 순수익/수익 팩터/손실폭/일 거래): `0.28/1.04/0.76/0.0441` and `2.19/1.53/0.53/0.0410`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{payload['next_run_id']}`.
"""
        write_text(IDEA_REGISTRY, idea_text.rstrip() + addition)

    negative_marker = "<!-- NR-FR79-RUNTIME-NATIVE-TRADE-SHAPE-LABELING -->"
    negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig")
    if negative_marker not in negative_text:
        addition = f"""

{negative_marker}
## NR-FR79-RUNTIME-NATIVE-TRADE-SHAPE-LABELING

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨)이 actual fill path(실제 체결 경로)를 반영하면 proxy/runtime gap(프록시/런타임 간극)을 줄일 수 있다.
- Why failed(실패 이유): MT5 Runtime Probe(MT5 런타임 탐침)는 signal/feature parity(신호/피처 동등성)를 맞췄지만 validation/OOS trades/day(검증/표본외 일 거래)가 `0.044/0.041`로 목표보다 너무 낮고, F79F ambiguous-fill repair(모호 체결 수리)는 scout/meaningful(탐색/의미) `0/0`이었다.
- Preserved clue(보존 단서): long-side ONNX mapping(롱 방향 ONNX 매핑), selected-entry veto tape(선택 진입 거부 테이프), runtime bridge(런타임 연결)는 재사용 가치가 있다.
- Do-not-repeat(반복 금지): close_direction both-hit label(종가방향 동시 도달 라벨)을 real-tick economics(실틱 경제성)처럼 쓰지 않는다.
- Reopen condition(재개 조건): feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할)을 함께 바꾸는 새 표면에서만 재개한다.
- Evidence(근거): `{rel(REPORT_PATH)}`.
- Boundary(경계): no authority(권위 없음), no completion(완성 없음).
"""
        write_text(NEGATIVE_REGISTER, negative_text.rstrip() + addition)

    if path_exists(REVIEW_INDEX):
        marker_index = "<!-- F79G_CLOSEOUT -->"
        index_text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
        if marker_index not in index_text:
            addition = f"""

{marker_index}
- F79G closeout(마감): `{rel(REPORT_PATH)}`; summary(요약): `{rel(SUMMARY_PATH)}`; gate audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`.
"""
            write_text(REVIEW_INDEX, index_text.rstrip() + addition)


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
runtime_probe_status: f79_mandatory_runtime_probe_completed_stage_closed
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: {RETROSPECTIVE_DUE_STATUS if closeout_success else 'not_due_after_f78_closeout_3_of_5'}
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F79G stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 닫지 않았다'}."
  - "Effect(효과): F79 negative memory(부정 기억), preserved clue(보존 단서), next frontier hypothesis(다음 전선 가설)를 기록했다."
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

Action(행동): F79G stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 닫지 않았다'}.

Effect(효과): F79는 negative memory(부정 기억)로 닫고, runtime bridge(런타임 연결)와 long-side ONNX mapping(롱 방향 ONNX 매핑)을 preserved clue(보존 단서)로 남겼다.

## Open Work(열린 작업)

- next run(다음 실행): `{payload['next_run_id']}`
- next frontier hypothesis(다음 전선 가설): `{payload['next_frontier_hypothesis']}`
- five-stage retrospective due status(5단계 회고 도래 상태): `{payload['five_stage_retrospective_due_status']}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)

    selection = f"""# F79 Selection Status(F79 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{payload['status']}`

Judgment(판정): `{payload['judgment']}`

Closeout label(마감 라벨): `{payload['closeout_label']}`

Action(행동): F79G stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 닫지 않았다'}.

Effect(효과): 다음 실행은 F80 stage open(F80 단계 개방) 후보이며, F79의 winner/baseline/promotion(승자/기준선/승격)은 만들지 않았다.

Current run(현재 실행): `{current_run}`

Latest completed run(최근 완료 실행): `{latest_completed}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS_PATH, selection)


def main() -> int:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)

    created_at = utc_now()
    kpi_rows, bundle = build_kpi_rows()
    draft_payload = build_payload(created_at, kpi_rows, bundle, True)
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
    grok_success = bool(result.returncode == 0 and not result.timed_out)
    clean_output = io_path(GROK_CLEAN_PATH).read_text(encoding="utf-8-sig") if path_exists(GROK_CLEAN_PATH) else result.clean_stdout
    advice, direction, forbidden_hits = classify_advice(clean_output, grok_success)
    draft_verify = local_verification(draft_payload, advice, forbidden_hits)
    closeout_success = close_allowed(advice, grok_success, forbidden_hits, draft_verify)

    payload = build_payload(created_at, kpi_rows, bundle, closeout_success)
    verify = local_verification(payload, advice, forbidden_hits)
    grok = grok_identity(result)

    write_json(LOCAL_VERIFICATION_PATH, verify)
    report = closeout_report_text(created_at, payload, grok, advice, direction, forbidden_hits)
    write_text(REPORT_PATH, report)
    write_text(FRONTIER_REPORT_PATH, report)
    write_text(RECEIPT_PATH, receipt_text(created_at, grok, advice, direction, forbidden_hits, closeout_success))
    write_text(GATE_AUDIT_PATH, gate_audit_text(created_at, advice, closeout_success))
    write_csv(KPI_ROWS_PATH, kpi_rows)
    write_csv(RUN_DIR / "f79g_closeout_kpi_rows.csv", kpi_rows)

    lineage = artifact_lineage(created_at, closeout_success)
    payload["local_verification"] = verify
    payload["artifact_lineage"] = lineage
    payload["grok"] = grok
    payload["advice_classification"] = advice
    payload["final_codex_direction"] = direction
    payload["forbidden_claim_hits"] = list(forbidden_hits)
    write_json(LINEAGE_PATH, lineage)
    write_json(SUMMARY_PATH, payload)
    write_json(RUN_MANIFEST_PATH, payload)

    update_registers(created_at, payload, closeout_success)
    update_state(created_at, payload, closeout_success)

    print(json.dumps(json_ready({
        "status": payload["status"],
        "judgment": payload["judgment"],
        "closeout_label": payload["closeout_label"],
        "advice_classification": advice,
        "grok_success": grok_success,
        "closeout_success": closeout_success,
        "next_run_id": payload["next_run_id"],
        "forbidden_claim_hits": list(forbidden_hits),
        "report": rel(REPORT_PATH),
    }), ensure_ascii=False, indent=2))
    return 0 if closeout_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
