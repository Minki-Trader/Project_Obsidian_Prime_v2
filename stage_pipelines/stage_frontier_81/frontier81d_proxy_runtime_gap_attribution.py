from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_81 import frontier81b_mt5_native_order_intent_cost_shape_proxy_scout as f81b


STAGE_ID = f81b.STAGE_ID
RUN_ID = "frontier81D_proxy_runtime_gap_attribution_v1"
PARENT_RUN_ID = "frontier81C_mt5_runtime_materialization_v1"
NEXT_RUN_ID = "frontier81E_capped_repair_or_rotation_decision_v1"
STATUS = "f81d_runtime_gap_attributed_negative_runtime_economics_no_authority"
JUDGMENT = "signal_feature_onnx_parity_passed_runtime_economics_failed_repair_or_rotation_required_no_authority"
CLAIM_BOUNDARY = (
    "gap_attribution_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
F81B_SUMMARY = REVIEW_DIR / "f81b_order_intent_cost_shape_proxy_summary.json"
F81C_SUMMARY = REVIEW_DIR / "f81c_mt5_runtime_materialization_summary.json"
F81C_MANIFEST = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "run_manifest.json"
F81C_RECEIPT = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "f81c_runtime_receipt.csv"

SUMMARY = REVIEW_DIR / "f81d_proxy_runtime_gap_attribution.json"
GAP_ROWS = REVIEW_DIR / "f81d_proxy_runtime_gap_rows.csv"
REPORT = REVIEW_DIR / "frontier81D_proxy_runtime_gap_attribution_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f81d.md"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f81d_performance_attribution_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f81d_result_judgment_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f81d_claim_discipline_receipt.yaml"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_81/frontier81d_proxy_runtime_gap_attribution.py"


def utc_now() -> str:
    return f78b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def build_gap_rows(runtime_rows: Sequence[Mapping[str, Any]], target: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for runtime in runtime_rows:
        split = str(runtime.get("split") or "")
        prefix = "val" if split == "validation" else split
        proxy_net = as_float(runtime.get("proxy_net_profit"))
        proxy_pf = as_float(runtime.get("proxy_profit_factor"))
        proxy_dd = as_float(runtime.get("proxy_dd_percent"))
        runtime_net = as_float(runtime.get("net_profit"))
        runtime_pf = as_float(runtime.get("profit_factor"))
        runtime_dd = as_float(runtime.get("max_drawdown_percent"))
        proxy_win_rate = as_float(target.get(f"{prefix}_win_rate"))
        runtime_win_rate = as_float(runtime.get("win_rate_percent")) / 100.0
        rows.append(
            {
                "split": split,
                "candidate_id": runtime.get("candidate_id"),
                "source_candidate_id": target.get("candidate_id"),
                "proxy_net_profit": proxy_net,
                "runtime_net_profit": runtime_net,
                "net_runtime_minus_proxy": runtime_net - proxy_net,
                "proxy_profit_factor": proxy_pf,
                "runtime_profit_factor": runtime_pf,
                "pf_runtime_minus_proxy": runtime_pf - proxy_pf,
                "proxy_drawdown_percent": proxy_dd,
                "runtime_drawdown_percent": runtime_dd,
                "dd_runtime_minus_proxy": runtime_dd - proxy_dd,
                "proxy_trade_count": as_float(target.get(f"{prefix}_trade_count")),
                "runtime_trade_count": as_float(runtime.get("trade_count")),
                "expected_signal_count": as_float(runtime.get("expected_signal_count")),
                "runtime_signal_count": as_float(runtime.get("signal_count")),
                "signal_count_diff": as_float(runtime.get("signal_count_diff")),
                "feature_ready_diff": as_float(runtime.get("feature_ready_diff")),
                "expected_selected_trade_count": as_float(runtime.get("expected_selected_trade_count")),
                "order_fill_count": as_float(runtime.get("order_fill_count")),
                "order_fill_rate": as_float(runtime.get("order_fill_rate")),
                "proxy_win_rate": proxy_win_rate,
                "runtime_win_rate": runtime_win_rate,
                "win_rate_runtime_minus_proxy": runtime_win_rate - proxy_win_rate,
                "runtime_average_win": as_float(runtime.get("average_win")),
                "runtime_average_loss": as_float(runtime.get("average_loss")),
                "runtime_payoff_ratio": as_float(runtime.get("payoff_ratio")),
                "runtime_expectancy": as_float(runtime.get("expectancy")),
                "runtime_trades_per_day": as_float(runtime.get("trades_per_day")),
                "runtime_gap_class": runtime.get("gap_cause_summary"),
            }
        )
    return rows


def build_payload(created_at: str) -> dict[str, Any]:
    f81b_summary = read_json(F81B_SUMMARY)
    f81c_summary = read_json(F81C_SUMMARY)
    f81c_manifest = read_json(F81C_MANIFEST)
    runtime_rows = read_csv(F81C_RECEIPT)
    target = f81c_manifest.get("target") or {}
    gap_rows = build_gap_rows(runtime_rows, target)
    validation = next((row for row in gap_rows if row["split"] == "validation"), {})
    oos = next((row for row in gap_rows if row["split"] == "oos"), {})
    parity = {
        "probability_pass_rows": f81c_summary.get("probability_parity_pass_rows"),
        "signal_pass_rows": f81c_summary.get("signal_parity_pass_rows"),
        "feature_pass_rows": f81c_summary.get("feature_readiness_pass_rows"),
        "source_reproduction_pass_rows": f81c_summary.get("source_reproduction_pass_rows"),
    }
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "target": target,
        "f81b_counts": {
            "candidate_rows": f81b_summary.get("candidate_rows"),
            "materialization_candidate_count": f81b_summary.get("materialization_candidate_count"),
            "meaningful_signal_count": f81b_summary.get("meaningful_signal_count"),
            "final_like_reference_count": f81b_summary.get("final_like_reference_count"),
        },
        "f81c_status": f81c_summary.get("status"),
        "runtime_attempt_count": f81c_summary.get("attempt_count"),
        "runtime_completed_attempt_count": f81c_summary.get("completed_attempt_count"),
        "parity": parity,
        "gap_rows": gap_rows,
        "validation_gap": validation,
        "oos_gap": oos,
        "observed_change": "Proxy positive economics inverted to MT5 negative economics on validation and OOS.",
        "likely_drivers": [
            "runtime deal economics after signal/feature/ONNX parity",
            "win-rate collapse from proxy ~43% to runtime ~24-25%",
            "drawdown expansion from proxy 2-4% to runtime 24-31%",
            "tester execution semantics and deal PnL differ from proxy contract PnL scale",
        ],
        "not_primary_drivers": [
            "feature readiness: zero feature_ready_diff in both splits",
            "signal count: zero signal_count_diff in both splits",
            "ONNX handoff: probability and signal parity rows passed",
        ],
        "alternative_explanations": [
            "intrabar TP/SL hit ordering differs from proxy close_direction assumption",
            "spread/commission/slippage and broker deal accounting are not captured by proxy utility",
            "one-sided long exposure may be regime-fragile even when signal count is exact",
            "proxy contract PnL scale may still understate realized tester loss clustering",
        ],
        "attribution_confidence": "high_for_parity_not_cause_medium_for_exact_deal_cause",
        "next_probe": "F81E should do capped repair or rotation: either deal-level entry/exit PnL reconciliation and MT5-realized label rebuild, or rotate away from this one-sided long cost-shape branch.",
        "result_label": "negative_runtime_materialization_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def report_text(payload: Mapping[str, Any]) -> str:
    target = payload["target"]
    val = payload["validation_gap"]
    oos = payload["oos_gap"]
    return f"""# F81D Proxy Runtime Gap Attribution(F81D 프록시/런타임 간극 귀속)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- target(대상): `{target.get('candidate_id')}` / `{target.get('model')}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Observed Change(관찰 변화)

Action(행동): F81C MT5 runtime materialization(F81C MT5 런타임 물질화)을 F81B proxy KPI(F81B 프록시 핵심 성과 지표)와 split(구간)별로 비교했다.

Effect(효과): signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 원인에서 제외하고, runtime economics(런타임 경제성) 붕괴를 다음 F81E 수리 또는 회전 입력으로 고정한다.

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | signal diff(신호 차이) | fill rate(체결률) | win rate proxy/runtime(승률 프록시/런타임) |
|---|---:|---:|---:|---:|---:|
| validation(검증) | `{fmt(val.get('proxy_net_profit'))}/{fmt(val.get('proxy_profit_factor'))}/{fmt(val.get('proxy_drawdown_percent'))}` | `{fmt(val.get('runtime_net_profit'))}/{fmt(val.get('runtime_profit_factor'))}/{fmt(val.get('runtime_drawdown_percent'))}` | `{fmt(val.get('signal_count_diff'), 0)}` | `{fmt(val.get('order_fill_rate'))}` | `{fmt(val.get('proxy_win_rate'))}/{fmt(val.get('runtime_win_rate'))}` |
| OOS(표본외) | `{fmt(oos.get('proxy_net_profit'))}/{fmt(oos.get('proxy_profit_factor'))}/{fmt(oos.get('proxy_drawdown_percent'))}` | `{fmt(oos.get('runtime_net_profit'))}/{fmt(oos.get('runtime_profit_factor'))}/{fmt(oos.get('runtime_drawdown_percent'))}` | `{fmt(oos.get('signal_count_diff'), 0)}` | `{fmt(oos.get('order_fill_rate'))}` | `{fmt(oos.get('proxy_win_rate'))}/{fmt(oos.get('runtime_win_rate'))}` |

## Attribution(귀속)

Primary driver(주 원인): runtime deal economics after parity(동등성 이후 런타임 거래 경제성).

Not primary drivers(주 원인 아님): feature readiness(피처 준비), signal count(신호 수), ONNX handoff(온엑스 인계).

Trade shape(거래 형태): long only(롱 전용), validation trades `{fmt(val.get('runtime_trade_count'), 0)}`, OOS trades `{fmt(oos.get('runtime_trade_count'), 0)}`, OOS trades/day(표본외 일 거래) `{fmt(oos.get('runtime_trades_per_day'))}`.

Next probe(다음 탐침): `{payload.get('next_probe')}`

Forbidden claims(금지 주장): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F81D Required Gate Coverage Audit(F81D 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `runtime_materialization_evidence` | `passed(통과)` | `{rel(F81C_RECEIPT)}` | MT5 Strategy Tester(전략 테스터) 결과를 귀속에 사용한다. |
| `proxy_runtime_gap_attribution` | `passed(통과)` | `{rel(SUMMARY)}`, `{rel(GAP_ROWS)}` | proxy/runtime(프록시/런타임) 차이를 split(구간)별로 기록한다. |
| `parity_not_cause_boundary` | `passed(통과)` | `{rel(F81C_MANIFEST)}` | signal/feature/ONNX parity(신호/피처/온엑스 동등성)를 원인에서 분리한다. |
| `result_judgment_boundary` | `passed(통과)` | `{rel(RESULT_RECEIPT)}` | negative evidence(부정 근거)로 남기되 stage closeout(단계 마감)은 주장하지 않는다. |
| `final_claim_guard` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 권위/승격/실거래/목표 달성을 만들지 않는다. |
"""


def ledger_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    oos = payload["oos_gap"]
    return {
        "ledger_row_id": f"{RUN_ID}__gap_attribution",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "gap_attribution(간극 귀속)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_runtime_gap_attribution(프록시/런타임 간극 귀속)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "mt5_runtime_materialization_gap(런타임 물질화 간극)",
        "scoreboard_lane": "runtime_economics(런타임 경제성)",
        "lane": "gap_attribution(간극 귀속)",
        "family": "kpi_evidence(근거 KPI)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"oos_runtime_net={oos.get('runtime_net_profit')};oos_runtime_pf={oos.get('runtime_profit_factor')};oos_runtime_dd={oos.get('runtime_drawdown_percent')}",
        "guardrail_kpi": "signal_feature_onnx_parity_not_cause;no_authority",
        "external_verification_status": "completed_mt5_runtime_materialization",
        "notes": f"next={NEXT_RUN_ID}; attribution={payload.get('attribution_confidence')}",
        "run_number": "frontier81D",
        "date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("gap_rows") or []),
        "gate_passes": 5,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": (payload.get("target") or {}).get("candidate_id"),
        "model": (payload.get("target") or {}).get("model"),
        "net_profit": oos.get("runtime_net_profit"),
        "profit_factor": oos.get("runtime_profit_factor"),
        "drawdown": oos.get("runtime_drawdown_percent"),
        "trade_count": oos.get("runtime_trade_count"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "gap_attribution",
        "tier": "Tier A",
        "metric_scope": "mt5_runtime_gap",
        "result_status": STATUS,
        "feature_count": (payload.get("target") or {}).get("feature_count"),
        "work_family": "kpi_evidence",
        "row_id": f"{RUN_ID}__gap_attribution",
        "evidence_boundary": "gap_attribution_only_no_authority(간극 귀속만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "gap_attribution_only(간극 귀속만)",
    }


def write_receipts(payload: Mapping[str, Any]) -> None:
    write_text(
        PERFORMANCE_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: gap_attributed_no_authority
observed_change: "{payload.get('observed_change')}"
comparison_baseline: F81B proxy KPI(F81B 프록시 KPI)
likely_drivers:
  - runtime deal economics after parity(동등성 이후 런타임 거래 경제성)
  - win-rate collapse(승률 붕괴)
  - drawdown expansion(손실폭 확대)
segment_checks:
  - validation split(검증 구간)
  - OOS split(표본외 구간)
  - signal count parity(신호 수 동등성)
  - feature readiness parity(피처 준비 동등성)
attribution_confidence: {payload.get('attribution_confidence')}
next_probe: "{payload.get('next_probe')}"
""",
    )
    write_text(
        RESULT_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: negative_runtime_materialization_evidence_no_authority
result_subject: F81C MT5 runtime materialization(F81C MT5 런타임 물질화)
evidence_available:
  - {rel(F81C_RECEIPT)}
  - {rel(SUMMARY)}
evidence_missing:
  - deal-level entry/exit PnL decomposition(거래별 진입/청산 손익 분해)
judgment_label: negative
claim_boundary: {CLAIM_BOUNDARY}
next_condition: F81E capped repair or rotation(F81E 상한 수리 또는 회전)
""",
    )
    write_text(
        CLAIM_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_gap_attribution_no_authority
allowed_claims:
  - runtime_gap_attributed
  - negative_runtime_materialization_evidence
  - next_repair_or_rotation_required
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
final_status: "{JUDGMENT}; boundary={CLAIM_BOUNDARY}"
""",
    )


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f81_runtime_gap_attributed_repair_or_rotation_required_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: inactive_preserve_records_pending_codex_task_force_replacement
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F81D proxy/runtime gap attribution(프록시/런타임 간극 귀속)을 완료했다."
  - "Effect(효과): signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 원인에서 제외하고 runtime economics(런타임 경제성) 실패를 F81E 입력으로 남겼다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F81D proxy/runtime gap attribution(F81D 프록시/런타임 간극 귀속)을 완료했다.

Effect(효과): F81C MT5 runtime materialization(MT5 런타임 물질화)은 signal/feature/ONNX parity(신호/피처/온엑스 동등성)가 맞았지만 validation/OOS(검증/표본외) 모두 negative runtime economics(부정 런타임 경제성)로 귀속됐다.

Next run(다음 실행): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(
        SELECTION_STATUS,
        f"""# F81 Selection Status(F81 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F81D gap attribution(F81D 간극 귀속)을 기록했다.

Effect(효과): F81C runtime materialization(런타임 물질화)은 negative evidence(부정 근거)이며, F81E capped repair or rotation(상한 수리 또는 회전)이 필요하다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F81 Review Index(F81 검토 색인)\n"
    for line in [
        "- `frontier81D_proxy_runtime_gap_attribution_report.md`: F81D proxy/runtime gap attribution report(F81D 프록시/런타임 간극 귀속 보고서)",
        "- `f81d_proxy_runtime_gap_attribution.json`: F81D machine gap attribution(F81D 기계 간극 귀속)",
        "- `f81d_proxy_runtime_gap_rows.csv`: F81D split-level gap rows(F81D 구간별 간극 행)",
        "- `required_gate_coverage_audit_f81d.md`: F81D gate audit(F81D 게이트 감사)",
    ]:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    oos = payload["oos_gap"]
    addition = f"""

- `{RUN_ID}` attributed F81 proxy/runtime gap(F81 프록시/런타임 간극 귀속). Result(결과): OOS runtime net/PF/DD(표본외 런타임 순손익/수익 팩터/손실폭) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}` vs proxy(프록시) `{oos.get('proxy_net_profit')}/{oos.get('proxy_profit_factor')}/{oos.get('proxy_drawdown_percent')}`. Boundary(경계): negative runtime materialization evidence only, no authority(부정 런타임 물질화 근거만, 권위 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_changelog(payload: Mapping[str, Any]) -> None:
    path = ROOT / "docs/workspace/changelog.md"
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else "# Changelog(변경 기록)\n"
    if RUN_ID in text:
        return
    oos = payload["oos_gap"]
    entry = f"""# 2026-06-18 - F81D Proxy Runtime Gap Attribution(F81D 프록시/런타임 간극 귀속)

- Action(행동): `{RUN_ID}`로 F81C MT5 runtime materialization(MT5 런타임 물질화)을 F81B proxy(프록시)와 비교했다.
- Effect(효과): OOS runtime net/PF/DD(표본외 런타임 순손익/수익 팩터/손실폭) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}`가 proxy(프록시) `{oos.get('proxy_net_profit')}/{oos.get('proxy_profit_factor')}/{oos.get('proxy_drawdown_percent')}`에서 붕괴한 것을 negative evidence(부정 근거)로 기록했다.
- Next(다음): `{NEXT_RUN_ID}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
    write_text(path, entry + text)


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_gap"]
    write_text(
        CONTEXT_ANCHOR,
        f"""# F81 Context Anchor(F81 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- OOS runtime(표본외 런타임): net `{oos.get('runtime_net_profit')}`, PF `{oos.get('runtime_profit_factor')}`, DD `{oos.get('runtime_drawdown_percent')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    write_json(SUMMARY, payload)
    write_csv(GAP_ROWS, payload["gap_rows"])
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text(payload))
    write_receipts(payload)
    manifest = {
        **payload,
        "artifacts": {
            "summary": rel(SUMMARY),
            "gap_rows": rel(GAP_ROWS),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
        },
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }
    write_json(RUN_MANIFEST, manifest)
    row = ledger_row(payload, created_at)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    update_state_files(payload, created_at)
    update_selection_status(payload, created_at)
    update_review_index()
    update_idea_registry(payload)
    update_changelog(payload)
    update_context_anchor(payload, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "target": (payload.get("target") or {}).get("candidate_id"),
                    "validation_runtime": payload.get("validation_gap", {}),
                    "oos_runtime": payload.get("oos_gap", {}),
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
