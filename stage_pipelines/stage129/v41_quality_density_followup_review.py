from __future__ import annotations

import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


STAGE_ID = "129_adapter_research__v41_quality_density_followup_review"
RUN_ID = "run129A_stage129_v41_quality_density_followup_review_v1"
PACKET_ID = "stage129_v41_quality_density_followup_review_v1"
PARENT_RUN_ID = "run128A_stage128_v41_quality_reframe_after_shortgate_failure_v1"
SOURCE_STAGE128_ID = "128_adapter_research__v41_quality_reframe_after_shortgate_failure"
SOURCE_STAGE128_CLOSEOUT_COMMIT = "5279689f46abfd215aae08864999d6983a9d25af"
SOURCE_STAGE128_LATEST_COMMIT = "4d8ba3ab61aa63ca83eb4badba0ba9c524a8eee4"
SOURCE_STAGE127_LATEST_COMMIT = "30a94995ff3feccedf9815f683bdd71a72c9cc2c"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "open_new_v2_model_branch_in_stage130_after_v41_quality_density_tradeoff_failure"
NEXT_STAGE_ID = "130_adapter_research__new_v2_model_branch_after_v41_tradeoff_failure"
NEXT_RUN_ID = "run130A_stage130_new_v2_model_branch_after_v41_tradeoff_failure_v1"
NEXT_PACKET_ID = "stage130_new_v2_model_branch_after_v41_tradeoff_failure_v1"
EXTERNAL_STATUS = "completed_existing_stage128_mt5_runtime_evidence_reviewed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE122_QUALITY = {
    "adapter_id": "s122_v41_h3_cd5_session_margin_risk035_sht54_lng52",
    "profit_factor": 1.75,
    "net_profit": 1102.04,
    "max_drawdown_percent": 14.66,
    "trade_count": 179,
}
STAGE126_BEST = {
    "adapter_id": "s126_v41_h3_cd6_shortgate_risk035_sht54_lng52",
    "profit_factor": 1.510119726,
    "net_profit": 882.40,
    "max_drawdown_percent": 20.12,
    "trade_count": 229,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE128_ID / "03_reviews"
SOURCE_REPORT = SOURCE_REVIEWS / "stage128_quality_reframe_report.md"
SOURCE_DECISION = SOURCE_REVIEWS / "stage128_decision.md"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage128_quality_reframe_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage128_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage128_risk_atr_telemetry.csv"
SOURCE_GATES = SOURCE_REVIEWS / "stage128_gate_feature_summary.csv"

REPORT_PATH = REVIEWS_ROOT / "stage129_quality_density_followup_review.md"
GAP_SUMMARY_PATH = REVIEWS_ROOT / "stage129_stage128_34d_gap_summary.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage129_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage129_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def num(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        return default
    try:
        return float(str(value))
    except ValueError:
        return default


def fmt(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def source_rows(split: str) -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(SOURCE_SUMMARY)
        if row.get("split") == split
        and row.get("view") == "actual_routed_total"
        and row.get("status") == "completed"
    ]


def risk_row(adapter_id: str) -> dict[str, str]:
    for row in read_csv(SOURCE_RISK_ATR):
        if row.get("adapter_id") == adapter_id and row.get("split") == "oos" and row.get("view") == "actual_routed_total":
            return row
    return {}


def gate_row(adapter_id: str) -> dict[str, str]:
    for row in read_csv(SOURCE_GATES):
        if row.get("variant_id") == adapter_id and row.get("split") == "oos":
            return row
    return {}


def read_label(row: Mapping[str, Any]) -> str:
    pf = num(row, "oos_profit_factor")
    net = num(row, "oos_net_profit")
    dd = num(row, "oos_max_drawdown_percent")
    trades = num(row, "oos_trade_count")
    if dd <= LEGACY_34D["max_drawdown_percent"] and net < STAGE126_BEST["net_profit"] and trades < STAGE122_QUALITY["trade_count"]:
        return "dd_repaired_but_density_and_net_collapsed"
    if trades >= 220 and (pf < LEGACY_34D["profit_factor"] or net < LEGACY_34D["net_profit"]):
        return "density_preserved_quality_failed"
    if pf < LEGACY_34D["profit_factor"] and net < LEGACY_34D["net_profit"]:
        return "quality_density_tradeoff_failed"
    return "mixed_not_final"


def metric(row: Mapping[str, str], val_by_adapter: Mapping[str, Mapping[str, str]]) -> dict[str, Any]:
    adapter_id = str(row.get("adapter_id", ""))
    val = val_by_adapter.get(adapter_id, {})
    risk = risk_row(adapter_id)
    gate = gate_row(adapter_id)
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    trades = num(row, "trade_count")
    out = {
        "run_id": RUN_ID,
        "adapter_id": adapter_id,
        "validation_profit_factor": num(val, "profit_factor"),
        "validation_net_profit": num(val, "net_profit"),
        "validation_max_drawdown_percent": num(val, "max_drawdown_percent"),
        "validation_trade_count": num(val, "trade_count"),
        "oos_profit_factor": pf,
        "oos_net_profit": net,
        "oos_max_drawdown_percent": dd,
        "oos_trade_count": trades,
        "oos_cost_stressed_expectancy": num(row, "cost_stressed_expectancy"),
        "same_move_reentry_ratio": num(row, "same_move_reentry_ratio"),
        "mfe_capture_ratio": num(row, "mfe_capture_ratio"),
        "pf_gap_to_34d": pf - LEGACY_34D["profit_factor"],
        "net_gap_to_34d": net - LEGACY_34D["net_profit"],
        "dd_gap_to_34d": dd - LEGACY_34D["max_drawdown_percent"],
        "trade_count_gap_to_34d": trades - LEGACY_34D["trade_count"],
        "pf_delta_vs_stage126_best": pf - STAGE126_BEST["profit_factor"],
        "net_delta_vs_stage126_best": net - STAGE126_BEST["net_profit"],
        "dd_delta_vs_stage126_best": dd - STAGE126_BEST["max_drawdown_percent"],
        "trade_delta_vs_stage126_best": trades - STAGE126_BEST["trade_count"],
        "risk_floor_applied_count": num(risk, "risk_floor_applied_count"),
        "max_model_risk_pct": num(risk, "max_model_risk_pct"),
        "max_actual_risk_pct_after_floor": num(risk, "max_actual_risk_pct_after_floor"),
        "gate_block_mode": gate.get("block_mode", ""),
        "stage129_read": "",
        "next_probe": "open_new_v2_model_branch",
    }
    out["stage129_read"] = read_label(out)
    return out


def build_rows() -> list[dict[str, Any]]:
    val_by_adapter = {row.get("adapter_id", ""): row for row in source_rows("validation_is")}
    rows = [metric(row, val_by_adapter) for row in source_rows("oos")]
    return sorted(
        rows,
        key=lambda row: (
            num(row, "oos_net_profit"),
            num(row, "oos_profit_factor"),
            -num(row, "oos_max_drawdown_percent"),
            num(row, "oos_trade_count"),
        ),
        reverse=True,
    )


def best_net(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: (num(row, "oos_net_profit"), num(row, "oos_profit_factor")), default={})


def best_dd(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return min(rows, key=lambda row: (num(row, "oos_max_drawdown_percent", 99.0), -num(row, "oos_net_profit")), default={})


def gap_columns() -> list[str]:
    return [
        "run_id",
        "adapter_id",
        "validation_profit_factor",
        "validation_net_profit",
        "validation_max_drawdown_percent",
        "validation_trade_count",
        "oos_profit_factor",
        "oos_net_profit",
        "oos_max_drawdown_percent",
        "oos_trade_count",
        "oos_cost_stressed_expectancy",
        "same_move_reentry_ratio",
        "mfe_capture_ratio",
        "pf_gap_to_34d",
        "net_gap_to_34d",
        "dd_gap_to_34d",
        "trade_count_gap_to_34d",
        "pf_delta_vs_stage126_best",
        "net_delta_vs_stage126_best",
        "dd_delta_vs_stage126_best",
        "trade_delta_vs_stage126_best",
        "risk_floor_applied_count",
        "max_model_risk_pct",
        "max_actual_risk_pct_after_floor",
        "gate_block_mode",
        "stage129_read",
        "next_probe",
    ]


def formatted_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    int_cols = {"validation_trade_count", "oos_trade_count", "trade_count_gap_to_34d", "trade_delta_vs_stage126_best", "risk_floor_applied_count"}
    money_cols = {"validation_net_profit", "oos_net_profit", "net_gap_to_34d", "net_delta_vs_stage126_best"}
    out_rows = []
    for row in rows:
        out: dict[str, Any] = {}
        for col in gap_columns():
            value = row.get(col, "")
            if isinstance(value, float):
                out[col] = fmt(value, 0) if col in int_cols else fmt(value, 2) if col in money_cols else fmt(value)
            else:
                out[col] = value
        out_rows.append(out)
    return out_rows


def route_decision_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    net = best_net(rows)
    dd = best_dd(rows)
    return [
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "best_net_adapter": net.get("adapter_id", ""),
            "best_net": fmt(num(net, "oos_net_profit"), 2),
            "best_net_pf": fmt(num(net, "oos_profit_factor")),
            "best_net_dd": fmt(num(net, "oos_max_drawdown_percent")),
            "best_net_trades": fmt(num(net, "oos_trade_count"), 0),
            "best_dd_adapter": dd.get("adapter_id", ""),
            "best_dd": fmt(num(dd, "oos_max_drawdown_percent")),
            "best_dd_net": fmt(num(dd, "oos_net_profit"), 2),
            "route": "open_new_v2_model_branch",
            "reason": "v41_surface_repair_now_shows_safe_but_too_small_or_dense_but_weak",
            "overall_goal_complete": "false",
        }
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | gate(게이트) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter} | {gate} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {read} |".format(
                adapter=row.get("adapter_id", ""),
                gate=row.get("gate_block_mode", ""),
                pf=num(row, "oos_profit_factor"),
                net=num(row, "oos_net_profit"),
                dd=num(row, "oos_max_drawdown_percent"),
                trades=num(row, "oos_trade_count"),
                read=row.get("stage129_read", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]]) -> str:
    net = best_net(rows)
    dd = best_dd(rows)
    return f"""# Stage129 Quality-Density Follow-up Review(129단계 품질-밀도 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE128_ID}`
- source_stage128_closeout_commit(원천 128단계 종료 커밋): `{SOURCE_STAGE128_CLOSEOUT_COMMIT}`
- source_stage128_latest_commit(원천 128단계 최신 커밋): `{SOURCE_STAGE128_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage128(128단계)의 max_hold/ATR bracket(최대 보유/ATR 괄호) 재구성이 34D KPI(34D 핵심 성과 지표) 격차를 실제로 줄였는가, 아니면 다음 bounded repair(경계 수리), demotion(강등), 또는 new branch(새 분기)가 필요한가?

Effect(효과): Stage129(129단계)는 새 실험을 하지 않고 Stage128 evidence(128단계 근거)를 읽어 다음 경계를 정한다.

## KPI Read(핵심 성과 지표 판독)

{markdown_table(rows)}

## Plain Read(쉬운 판독)

- best_net(최대 순손익): `{net.get('adapter_id', '')}` net `{num(net, 'oos_net_profit'):.2f}`, PF `{num(net, 'oos_profit_factor'):.2f}`, DD `{num(net, 'oos_max_drawdown_percent'):.2f}`, trades `{num(net, 'oos_trade_count'):.0f}`.
- best_dd(최저 손실률): `{dd.get('adapter_id', '')}` DD `{num(dd, 'oos_max_drawdown_percent'):.2f}`, net `{num(dd, 'oos_net_profit'):.2f}`, trades `{num(dd, 'oos_trade_count'):.0f}`.
- meaning(의미): v41 surface(브이41 표면)는 안전하게 만들면 너무 작아지고, 거래 수를 살리면 품질이 무너진다.

## Judgment(판정)

- result_subject(판정 대상): Stage128 quality-density reframe(128단계 품질-밀도 재구성).
- judgment_label(판정 라벨): `v41_surface_tradeoff_failed_open_new_branch`.
- next_condition(다음 조건): Stage130(130단계)은 legacy 34D(레거시 34D)를 답습하지 않고 새 v2-native model branch(브이투 고유 모델 분기)를 연다.
- claim_boundary(주장 경계): `{BOUNDARY}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown() -> str:
    return f"""# Stage129 Decision(129단계 판정)

decision(판정): `{DECISION}`

Stage129(129단계)는 Stage128(128단계) quality-density reframe(품질-밀도 재구성)을 review-only(검토 전용)로 판독했다.

Effect(효과): 현재 v41 surface(브이41 표면)는 34D KPI(34D 핵심 성과 지표)에 필요한 순손익, 손실률, 거래 수 균형을 동시에 만들지 못했으므로 Stage130(130단계)에서 새 v2-native model branch(브이투 고유 모델 분기)를 연다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage128_report(원천 128단계 보고서): `{rel(SOURCE_REPORT)}`
- source_stage128_decision(원천 128단계 판정): `{rel(SOURCE_DECISION)}`
- source_stage128_closeout_commit(원천 128단계 종료 커밋): `{SOURCE_STAGE128_CLOSEOUT_COMMIT}`
- source_stage128_latest_commit(원천 128단계 최신 커밋): `{SOURCE_STAGE128_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage129(129단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research/development(브이투 고유 연구개발)는 Stage130(130단계) 새 모델 분기로 이어진다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows = []
    for path in [REPORT_PATH, GAP_SUMMARY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, STAGE_LEDGER_PATH]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage129_quality_density_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage129 v2-native quality-density follow-up review artifact.",
                }
            )
    return rows


def write_ledgers(best: Mapping[str, Any]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_quality_density_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage128_closeout_commit", SOURCE_STAGE128_CLOSEOUT_COMMIT),
                        ("source_stage128_latest_commit", SOURCE_STAGE128_LATEST_COMMIT),
                        ("best_adapter", best.get("adapter_id")),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage129_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage129_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage128_mt5_runtime_evidence_review",
            "tier_scope": "Tier A+B routed review; Tier B disabled evidence preserved",
            "kpi_scope": "stage129_quality_density_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_adapter", best.get("adapter_id")),
                    ("pf", best.get("oos_profit_factor")),
                    ("net", best.get("oos_net_profit")),
                    ("dd", best.get("oos_max_drawdown_percent")),
                    ("trades", best.get("oos_trade_count")),
                )
            ),
            "guardrail_kpi": f"target_surface={TARGET_SURFACE};decision={DECISION};overall_goal_complete=false",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage129 review only; no new MT5 execution; no operational claim.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows(),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(best: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "result_judgment", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"], "required_gates": ["kpi_contract_audit", "result_judgment_gate", "artifact_lineage_gate"], "status": "completed"})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "source_stage128_summary": rel(SOURCE_SUMMARY), "source_stage128_segments": rel(SOURCE_SEGMENTS), "source_stage128_risk_atr": rel(SOURCE_RISK_ATR), "source_stage128_gates": rel(SOURCE_GATES), "gap_summary_path": rel(GAP_SUMMARY_PATH), "status": "passed_review_only"})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": DECISION, "judgment_label": "v41_surface_tradeoff_failed_open_new_branch", "best_adapter": best, "overall_goal_complete": False})
    write_json(PACKET_ROOT / "artifact_lineage_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_GATES)], "producer": rel(Path("stage_pipelines/stage129/v41_quality_density_followup_review.py")), "artifact_paths": [rel(REPORT_PATH), rel(GAP_SUMMARY_PATH), rel(ROUTE_DECISION_PATH), rel(DECISION_PATH), rel(STAGE_LEDGER_PATH)], "availability": "tracked_after_stage_boundary_commit", "lineage_judgment": "connected_with_boundary"})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "source_stage128_closeout_commit": SOURCE_STAGE128_CLOSEOUT_COMMIT, "source_stage128_latest_commit": SOURCE_STAGE128_LATEST_COMMIT, "best_adapter": best.get("adapter_id"), "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "overall_goal_complete": False})


def create_next_stage() -> None:
    write_md(NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage130(130단계)는 Stage129(129단계) 판정대로 current v41 surface(현재 브이41 표면) 수리를 멈추고 새 v2-native model branch(브이투 고유 모델 분기)를 연다.

## Bounded Question(경계 질문)

레거시 34D(legacy 34D, 레거시 34D)를 답습하지 않고, v2-native features/modeling(브이투 고유 피처/모델링)로 34D KPI(34D 핵심 성과 지표)에 접근하거나 넘을 새 후보 앵커를 만들 수 있는가?

Effect(효과): Stage130(130단계)는 실패한 v41 surface(브이41 표면)를 계속 깎지 않고, 실패 기억을 입력으로 삼아 새 모델 분기를 시작한다.

## Boundary(경계)

`{BOUNDARY}`
""")
    write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage130 Input References(130단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage129_report(129단계 보고서): `{rel(REPORT_PATH)}`
- stage129_gap_summary(129단계 차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- stage128_summary(128단계 요약): `{rel(SOURCE_SUMMARY)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""")
    write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage130 Review Index(130단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`
""")
    write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage130 Selection Status(130단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage129(129단계) closed(종료) as `{DECISION}` and Stage130(130단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): current v41 surface(현재 브이41 표면) 수리를 멈추고 새 v2-native model branch(브이투 고유 모델 분기)를 연다.
- >-
  Stage129 result(129단계 결과)는 `{rel(REPORT_PATH)}`와 `{rel(GAP_SUMMARY_PATH)}`에 기록했다. Effect(효과): safe-but-small(안전하지만 작음)과 dense-but-weak(촘촘하지만 약함) 실패를 다음 모델 분기 입력으로 쓴다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage129_v41_quality_density_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage128_closeout_commit: {SOURCE_STAGE128_CLOSEOUT_COMMIT}
  source_stage128_latest_commit: {SOURCE_STAGE128_LATEST_COMMIT}
  source_stage127_latest_commit: {SOURCE_STAGE127_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage129_v41_quality_density_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage129_v41_quality_density_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage129 Selection Status(129단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE128_ID}`
- source_decision(원천 판정): `continue_quality_density_followup_review_in_stage129_due_to_damage_or_no_repair`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage129_decision(129단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEWS_ROOT / "review_index.md", f"""# Stage129 Review Index(129단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
""")
    write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage130_new_v2_model_branch_surface`
- status(상태): `stage129_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage129(129단계) closed(종료) as v2-native v41 quality-density follow-up review(브이투 고유 브이41 품질-밀도 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage130(130단계) new v2 model branch(새 브이투 모델 분기)로 이어진다.

## Latest Stage129 Evidence(최신 129단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage129 v41 quality-density follow-up review closeout(129단계 v41 품질-밀도 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): v41 surface(브이41 표면)가 safe-but-small(안전하지만 작음) 또는 dense-but-weak(촘촘하지만 약함)으로 갈라진 실패를 기록하고 Stage130 새 v2 모델 분기로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = build_rows()
    net = best_net(rows)
    write_csv(GAP_SUMMARY_PATH, formatted_rows(rows), gap_columns())
    write_csv(ROUTE_DECISION_PATH, route_decision_rows(rows), ["run_id", "decision", "best_net_adapter", "best_net", "best_net_pf", "best_net_dd", "best_net_trades", "best_dd_adapter", "best_dd", "best_dd_net", "route", "reason", "overall_goal_complete"])
    write_md(REPORT_PATH, report_markdown(rows))
    write_md(DECISION_PATH, decision_markdown())
    ledger_payload = write_ledgers(net)
    write_packet_files(net, ledger_payload)
    update_current_truth()
    append_changelog()
    print(json.dumps({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "report": rel(REPORT_PATH)}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
