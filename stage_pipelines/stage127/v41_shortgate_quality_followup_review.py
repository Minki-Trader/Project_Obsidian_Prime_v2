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


STAGE_ID = "127_adapter_research__v41_shortgate_quality_followup_review"
RUN_ID = "run127A_stage127_v41_shortgate_quality_followup_review_v1"
PACKET_ID = "stage127_v41_shortgate_quality_followup_review_v1"
PARENT_RUN_ID = "run126A_stage126_v41_shortgate_quality_repair_after_route_supply_damage_v1"
SOURCE_STAGE126_ID = "126_adapter_research__v41_shortgate_quality_repair_after_route_supply_damage"
SOURCE_STAGE126_CLOSEOUT_COMMIT = "d25e503d4a72dc29affbcfa669db715ad85b4590"
SOURCE_STAGE126_LATEST_COMMIT = "e8144bed82184543c079a846193bb4e1c7aae9e0"
SOURCE_STAGE125_LATEST_COMMIT = "45e7b5c85a30f2ded4741b189adfabc876a84328"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_quality_reframe_in_stage128_after_shortgate_repair_failure"
NEXT_STAGE_ID = "128_adapter_research__v41_quality_reframe_after_shortgate_failure"
NEXT_RUN_ID = "run128A_stage128_v41_quality_reframe_after_shortgate_failure_v1"
NEXT_PACKET_ID = "stage128_v41_quality_reframe_after_shortgate_failure_v1"
EXTERNAL_STATUS = "completed_existing_stage126_mt5_runtime_evidence_reviewed"
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
STAGE122_SOURCE = {
    "adapter_id": "s122_v41_h3_cd5_session_margin_risk035_sht54_lng52",
    "profit_factor": 1.75,
    "net_profit": 1102.04,
    "max_drawdown_percent": 14.66,
    "trade_count": 179,
}
STAGE124_SHORTGATE = {
    "adapter_id": "s124_v41_h3_cd5_shortgate_risk035_sht54_lng52",
    "profit_factor": 1.51,
    "net_profit": 889.34,
    "max_drawdown_percent": 20.23,
    "trade_count": 230,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE126_ID / "03_reviews"
SOURCE_REPORT = SOURCE_REVIEWS / "stage126_shortgate_quality_repair_report.md"
SOURCE_DECISION = SOURCE_REVIEWS / "stage126_decision.md"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage126_shortgate_quality_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage126_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage126_risk_atr_telemetry.csv"
SOURCE_GATES = SOURCE_REVIEWS / "stage126_gate_feature_summary.csv"

REPORT_PATH = REVIEWS_ROOT / "stage127_shortgate_quality_followup_review.md"
GAP_SUMMARY_PATH = REVIEWS_ROOT / "stage127_stage126_quality_gap_summary.csv"
SEGMENT_REVIEW_PATH = REVIEWS_ROOT / "stage127_segment_failure_summary.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage127_repair_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage127_decision.md"
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
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def segment_rows(adapter_id: str, split: str) -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(SOURCE_SEGMENTS)
        if row.get("adapter_id") == adapter_id
        and row.get("split") == split
        and row.get("view") == "actual_routed_total"
        and row.get("segment") in {"early", "mid", "late", "actual_routed_total"}
    ]


def risk_row(adapter_id: str, split: str) -> dict[str, str]:
    for row in read_csv(SOURCE_RISK_ATR):
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def gate_row(adapter_id: str, split: str) -> dict[str, str]:
    for row in read_csv(SOURCE_GATES):
        if row.get("variant_id") == adapter_id and row.get("split") == split:
            return row
    return {}


def read_label(row: Mapping[str, Any]) -> str:
    pf = num(row, "oos_profit_factor")
    net = num(row, "oos_net_profit")
    dd = num(row, "oos_max_drawdown_percent")
    trades = num(row, "oos_trade_count")
    if (
        trades >= 200
        and pf >= LEGACY_34D["profit_factor"]
        and net >= LEGACY_34D["net_profit"]
        and dd <= 18.0
    ):
        return "material_repair_toward_34d"
    if (
        trades >= 190
        and pf > STAGE124_SHORTGATE["profit_factor"] + 0.01
        and net > STAGE124_SHORTGATE["net_profit"]
        and dd < STAGE124_SHORTGATE["max_drawdown_percent"]
    ):
        return "small_repair_confirmed"
    if net < STAGE124_SHORTGATE["net_profit"] and pf <= STAGE124_SHORTGATE["profit_factor"] + 0.005:
        return "no_quality_repair"
    if dd > STAGE124_SHORTGATE["max_drawdown_percent"]:
        return "drawdown_damage"
    return "mixed_not_enough"


def next_probe(label: str) -> str:
    if label == "material_repair_toward_34d":
        return "open_equity_segment_package_review"
    if label == "small_repair_confirmed":
        return "continue_targeted_repair_with_quality_guard"
    return "reframe_quality_density_not_threshold_cooldown"


def metric(row: Mapping[str, str], val_by_adapter: Mapping[str, Mapping[str, str]]) -> dict[str, Any]:
    adapter_id = str(row.get("adapter_id", ""))
    val = val_by_adapter.get(adapter_id, {})
    risk = risk_row(adapter_id, "oos")
    gate = gate_row(adapter_id, "oos")
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    trades = num(row, "trade_count")
    output = {
        "run_id": RUN_ID,
        "adapter_id": adapter_id,
        "repair_label": row.get("repair_label", ""),
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
        "stage124_shortgate_profit_factor": STAGE124_SHORTGATE["profit_factor"],
        "stage124_shortgate_net_profit": STAGE124_SHORTGATE["net_profit"],
        "stage124_shortgate_max_drawdown_percent": STAGE124_SHORTGATE["max_drawdown_percent"],
        "stage124_shortgate_trade_count": STAGE124_SHORTGATE["trade_count"],
        "stage122_source_profit_factor": STAGE122_SOURCE["profit_factor"],
        "stage122_source_net_profit": STAGE122_SOURCE["net_profit"],
        "stage122_source_max_drawdown_percent": STAGE122_SOURCE["max_drawdown_percent"],
        "stage122_source_trade_count": STAGE122_SOURCE["trade_count"],
        "pf_delta_vs_stage124_shortgate": pf - STAGE124_SHORTGATE["profit_factor"],
        "net_delta_vs_stage124_shortgate": net - STAGE124_SHORTGATE["net_profit"],
        "dd_delta_vs_stage124_shortgate": dd - STAGE124_SHORTGATE["max_drawdown_percent"],
        "trade_delta_vs_stage124_shortgate": trades - STAGE124_SHORTGATE["trade_count"],
        "pf_delta_vs_stage122_source": pf - STAGE122_SOURCE["profit_factor"],
        "net_delta_vs_stage122_source": net - STAGE122_SOURCE["net_profit"],
        "dd_delta_vs_stage122_source": dd - STAGE122_SOURCE["max_drawdown_percent"],
        "trade_delta_vs_stage122_source": trades - STAGE122_SOURCE["trade_count"],
        "pf_gap_to_34d": pf - LEGACY_34D["profit_factor"],
        "net_gap_to_34d": net - LEGACY_34D["net_profit"],
        "dd_gap_to_34d": dd - LEGACY_34D["max_drawdown_percent"],
        "trade_count_gap_to_34d": trades - LEGACY_34D["trade_count"],
        "risk_floor_applied_count": num(risk, "risk_floor_applied_count"),
        "max_model_risk_pct": num(risk, "max_model_risk_pct"),
        "max_actual_risk_pct_after_floor": num(risk, "max_actual_risk_pct_after_floor"),
        "avg_atr_points": num(risk, "avg_atr_points"),
        "avg_sl_points": num(risk, "avg_sl_points"),
        "avg_tp_points": num(risk, "avg_tp_points"),
        "gate_block_mode": gate.get("block_mode", ""),
        "gate_blocked_rows": num(gate, "blocked_rows"),
        "gate_blocked_ratio": num(gate, "blocked_ratio"),
    }
    label = read_label(output)
    output["stage127_read"] = label
    output["next_probe"] = next_probe(label)
    return output


def build_rows() -> list[dict[str, Any]]:
    val_by_adapter = {row.get("adapter_id", ""): row for row in source_rows("validation_is")}
    rows = [metric(row, val_by_adapter) for row in source_rows("oos")]
    return sorted(
        rows,
        key=lambda row: (
            num(row, "oos_profit_factor"),
            num(row, "oos_net_profit"),
            -num(row, "oos_max_drawdown_percent"),
            num(row, "oos_trade_count"),
        ),
        reverse=True,
    )


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        rows,
        key=lambda row: (
            num(row, "oos_profit_factor"),
            num(row, "oos_net_profit"),
            -num(row, "oos_max_drawdown_percent"),
            num(row, "oos_trade_count"),
        ),
        default={},
    )


def gap_columns() -> list[str]:
    return [
        "run_id",
        "adapter_id",
        "repair_label",
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
        "pf_delta_vs_stage124_shortgate",
        "net_delta_vs_stage124_shortgate",
        "dd_delta_vs_stage124_shortgate",
        "trade_delta_vs_stage124_shortgate",
        "pf_delta_vs_stage122_source",
        "net_delta_vs_stage122_source",
        "dd_delta_vs_stage122_source",
        "trade_delta_vs_stage122_source",
        "pf_gap_to_34d",
        "net_gap_to_34d",
        "dd_gap_to_34d",
        "trade_count_gap_to_34d",
        "risk_floor_applied_count",
        "max_model_risk_pct",
        "max_actual_risk_pct_after_floor",
        "avg_atr_points",
        "avg_sl_points",
        "avg_tp_points",
        "gate_block_mode",
        "gate_blocked_rows",
        "gate_blocked_ratio",
        "stage127_read",
        "next_probe",
    ]


def formatted_gap_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    int_cols = {
        "validation_trade_count",
        "oos_trade_count",
        "trade_delta_vs_stage124_shortgate",
        "trade_delta_vs_stage122_source",
        "trade_count_gap_to_34d",
        "risk_floor_applied_count",
        "gate_blocked_rows",
    }
    money_cols = {
        "validation_net_profit",
        "oos_net_profit",
        "net_delta_vs_stage124_shortgate",
        "net_delta_vs_stage122_source",
        "net_gap_to_34d",
    }
    output = []
    for row in rows:
        out: dict[str, Any] = {}
        for col in gap_columns():
            value = row.get(col, "")
            if isinstance(value, float):
                if col in int_cols:
                    out[col] = fmt(value, 0)
                elif col in money_cols:
                    out[col] = fmt(value, 2)
                else:
                    out[col] = fmt(value)
            else:
                out[col] = value
        output.append(out)
    return output


def segment_issue(row: Mapping[str, str]) -> str:
    segment = row.get("segment", "")
    if segment == "actual_routed_total":
        return "total_row"
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    trades = num(row, "trade_count")
    if trades <= 0:
        return "missing_segment_trades"
    if pf < 1.45:
        return "weak_segment_pf"
    if pf < LEGACY_34D["profit_factor"]:
        return "below_34d_pf"
    if net <= 0:
        return "segment_not_profitable"
    return "positive_but_not_final"


def build_segment_review(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    adapter_id = str(best.get("adapter_id", ""))
    output = []
    for row in segment_rows(adapter_id, "oos"):
        output.append(
            {
                "run_id": RUN_ID,
                "adapter_id": adapter_id,
                "segment": row.get("segment", ""),
                "profit_factor": fmt(num(row, "profit_factor")),
                "net_profit": fmt(num(row, "net_profit"), 2),
                "max_drawdown_percent": fmt(num(row, "max_drawdown_percent")),
                "trade_count": fmt(num(row, "trade_count"), 0),
                "issue_label": segment_issue(row),
            }
        )
    return output


def build_route_decision(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "best_adapter": best.get("adapter_id", ""),
            "best_oos_profit_factor": fmt(num(best, "oos_profit_factor")),
            "best_oos_net_profit": fmt(num(best, "oos_net_profit"), 2),
            "best_oos_max_drawdown_percent": fmt(num(best, "oos_max_drawdown_percent")),
            "best_oos_trade_count": fmt(num(best, "oos_trade_count"), 0),
            "stage127_read": best.get("stage127_read", ""),
            "next_stage_or_branch": NEXT_STAGE_ID,
            "repair_focus": "quality_density_reframe_after_shortgate_threshold_cooldown_failure",
            "forbidden_route": "do_not_repeat_no_gate_supply_or_threshold_only_shortgate",
            "overall_goal_complete": "false",
        }
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | vs124 net(124 대비 순손익) | 34D net gap(34D 순손익 차이) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {net_delta:.2f} | {net_gap:.2f} | {read} |".format(
                adapter=row.get("adapter_id", ""),
                pf=num(row, "oos_profit_factor"),
                net=num(row, "oos_net_profit"),
                dd=num(row, "oos_max_drawdown_percent"),
                trades=num(row, "oos_trade_count"),
                net_delta=num(row, "net_delta_vs_stage124_shortgate"),
                net_gap=num(row, "net_gap_to_34d"),
                read=row.get("stage127_read", ""),
            )
        )
    return "\n".join(lines)


def segment_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| segment(구간) | PF(수익 팩터) | net(순손익) | trades(거래 수) | issue(이슈) |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {segment} | {pf} | {net} | {trades} | {issue} |".format(
                segment=row.get("segment", ""),
                pf=row.get("profit_factor", ""),
                net=row.get("net_profit", ""),
                trades=row.get("trade_count", ""),
                issue=row.get("issue_label", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], segment_review: Sequence[Mapping[str, Any]]) -> str:
    best = best_row(rows)
    unique_profiles = {
        (
            fmt(num(row, "oos_profit_factor")),
            fmt(num(row, "oos_net_profit"), 2),
            fmt(num(row, "oos_max_drawdown_percent")),
            fmt(num(row, "oos_trade_count"), 0),
        )
        for row in rows
    }
    return f"""# Stage127 Shortgate Quality Follow-up Review(127단계 숏 게이트 품질 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE126_ID}`
- source_stage126_closeout_commit(원천 126단계 종료 커밋): `{SOURCE_STAGE126_CLOSEOUT_COMMIT}`
- source_stage126_latest_commit(원천 126단계 최신 커밋): `{SOURCE_STAGE126_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage126(126단계)의 shortgate quality repair(숏 게이트 품질 수리)가 거래 수 증가를 일부 보존하면서 PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록)를 회복했는가?

Effect(효과): Stage127(127단계)는 새 실험을 하지 않고 Stage126 evidence(126단계 근거)를 판독해 다음 bounded repair(경계 수리)를 정한다.

## KPI Read(핵심 성과 지표 판독)

{markdown_table(rows)}

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `{best.get('adapter_id', '')}`
- OOS PF(표본외 수익 팩터): `{num(best, 'oos_profit_factor'):.6f}`
- OOS net(표본외 순손익): `{num(best, 'oos_net_profit'):.2f}`
- OOS DD%(표본외 손실률): `{num(best, 'oos_max_drawdown_percent'):.2f}`
- trades(거래 수): `{num(best, 'oos_trade_count'):.0f}`
- gap_to_34D(34D 대비 차이): PF `{num(best, 'pf_gap_to_34d'):.6f}`, net `{num(best, 'net_gap_to_34d'):.2f}`, DD `{num(best, 'dd_gap_to_34d'):.2f}`, trades `{num(best, 'trade_count_gap_to_34d'):.0f}`.
- vs_Stage124_shortgate(124단계 숏 게이트 대비): net `{num(best, 'net_delta_vs_stage124_shortgate'):.2f}`, trades `{num(best, 'trade_delta_vs_stage124_shortgate'):.0f}`, DD `{num(best, 'dd_delta_vs_stage124_shortgate'):.2f}`.
- unique_profiles(고유 결과 형태): `{len(unique_profiles)}` of `{len(rows)}` variants(변형). Effect(효과): threshold/cooldown(임계값/대기시간)만 바꾼 수리는 결과 형태를 거의 바꾸지 못했다.

## Segment Read(구간 판독)

{segment_table(segment_review)}

## Judgment(판정)

- result_subject(판정 대상): Stage126 shortgate quality repair(126단계 숏 게이트 품질 수리).
- result_label(결과 라벨): `{best.get('stage127_read', '')}`.
- plain_read(쉬운 판독): 229 trades(거래)로 Stage122 품질 기준보다 거래 수는 늘었지만, PF/net/DD(수익 팩터/순손익/손실률)는 34D target(34D 목표)과 Stage122 source(122단계 원천 품질) 양쪽에 부족하다.
- risk_atr_read(위험/ATR 판독): risk floor(위험 바닥) 손상은 보이지 않지만, ATR/risk(ATR/위험) 존재만으로 품질이 회복되지는 않았다.
- next_condition(다음 조건): Stage128(128단계)은 no-gate supply(무게이트 공급) 반복이나 threshold-only shortgate(임계값 전용 숏 게이트) 반복이 아니라 quality-density reframe(품질-밀도 재구성)을 좁게 다룬다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown() -> str:
    return f"""# Stage127 Decision(127단계 판정)

decision(판정): `{DECISION}`

Stage127(127단계)는 Stage126(126단계) shortgate quality repair(숏 게이트 품질 수리)를 review-only(검토 전용)로 판독했다.

Effect(효과): Stage126(126단계)의 threshold/cooldown(임계값/대기시간) 수리는 34D KPI(34D 핵심 성과 지표) 격차를 줄이지 못했으므로, Stage128(128단계)에서 quality-density reframe(품질-밀도 재구성)으로 넘어간다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- segment_failure_summary(구간 실패 요약): `{rel(SEGMENT_REVIEW_PATH)}`
- repair_route_decision(수리 경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage126_report(원천 126단계 보고서): `{rel(SOURCE_REPORT)}`
- source_stage126_decision(원천 126단계 판정): `{rel(SOURCE_DECISION)}`
- source_stage126_closeout_commit(원천 126단계 종료 커밋): `{SOURCE_STAGE126_CLOSEOUT_COMMIT}`
- source_stage126_latest_commit(원천 126단계 최신 커밋): `{SOURCE_STAGE126_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage127(127단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research/development(브이투 고유 연구개발)는 Stage128(128단계)로 이어진다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows = []
    for path in [REPORT_PATH, GAP_SUMMARY_PATH, SEGMENT_REVIEW_PATH, ROUTE_DECISION_PATH, DECISION_PATH, STAGE_LEDGER_PATH]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage127_shortgate_quality_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage127 v2-native shortgate quality follow-up review artifact.",
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
                "lane": "baseline_adapter_v2_native_v41_shortgate_quality_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage126_closeout_commit", SOURCE_STAGE126_CLOSEOUT_COMMIT),
                        ("source_stage126_latest_commit", SOURCE_STAGE126_LATEST_COMMIT),
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
            "ledger_row_id": f"{RUN_ID}__stage127_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage127_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage126_mt5_runtime_evidence_review",
            "tier_scope": "Tier A+B routed review; Tier B disabled evidence preserved",
            "kpi_scope": "stage127_shortgate_quality_followup_review",
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
            "notes": "Stage127 review only; no new MT5 execution; no operational claim.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifacts = artifact_rows()
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifacts,
        key="artifact_id",
    )
    return {
        "run_registry": run_payload,
        "alpha_ledger": alpha_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(best: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": ["kpi_contract_audit", "result_judgment_gate", "artifact_lineage_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "source_stage126_summary": rel(SOURCE_SUMMARY),
            "source_stage126_segments": rel(SOURCE_SEGMENTS),
            "source_stage126_risk_atr": rel(SOURCE_RISK_ATR),
            "source_stage126_gates": rel(SOURCE_GATES),
            "gap_summary_path": rel(GAP_SUMMARY_PATH),
            "segment_review_path": rel(SEGMENT_REVIEW_PATH),
            "status": "passed_review_only",
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "judgment_label": best.get("stage127_read", ""),
            "best_adapter": best,
            "overall_goal_complete": False,
        },
    )
    write_json(
        PACKET_ROOT / "artifact_lineage_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_GATES)],
            "producer": rel(Path("stage_pipelines/stage127/v41_shortgate_quality_followup_review.py")),
            "artifact_paths": [
                rel(REPORT_PATH),
                rel(GAP_SUMMARY_PATH),
                rel(SEGMENT_REVIEW_PATH),
                rel(ROUTE_DECISION_PATH),
                rel(DECISION_PATH),
                rel(STAGE_LEDGER_PATH),
            ],
            "availability": "tracked_after_stage_boundary_commit",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage126_closeout_commit": SOURCE_STAGE126_CLOSEOUT_COMMIT,
            "source_stage126_latest_commit": SOURCE_STAGE126_LATEST_COMMIT,
            "best_adapter": best.get("adapter_id"),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage128(128단계)는 Stage127(127단계) 판정대로 shortgate threshold/cooldown(숏 게이트 임계값/대기시간) 반복을 멈추고 quality-density reframe(품질-밀도 재구성)을 좁게 실행한다.

## Bounded Question(경계 질문)

Stage122 quality anchor(122단계 품질 기준), Stage124 route supply damage(124단계 경로 공급 손상), Stage126 shortgate repair failure(126단계 숏 게이트 수리 실패)를 함께 사용해 34D KPI(34D 핵심 성과 지표)에 가까운 PF/net/DD/trades(수익 팩터/순손익/손실률/거래 수) 균형을 회복할 수 있는가?

Effect(효과): Stage128(128단계)는 legacy method(레거시 방식)를 답습하지 않고, v2-native(브이투 고유) 실패 기억으로 품질과 밀도의 균형을 다시 잡는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage128 Input References(128단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage127_report(127단계 보고서): `{rel(REPORT_PATH)}`
- stage127_gap_summary(127단계 차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- stage127_segment_failure_summary(127단계 구간 실패 요약): `{rel(SEGMENT_REVIEW_PATH)}`
- stage126_summary(126단계 요약): `{rel(SOURCE_SUMMARY)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage128 Review Index(128단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage128 Selection Status(128단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage127(127단계) closed(종료) as `{DECISION}` and Stage128(128단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): shortgate threshold/cooldown(숏 게이트 임계값/대기시간) 반복 대신 quality-density reframe(품질-밀도 재구성)으로 넘어간다.
- >-
  Stage127 result(127단계 결과)는 `{rel(REPORT_PATH)}`, `{rel(GAP_SUMMARY_PATH)}`, `{rel(SEGMENT_REVIEW_PATH)}`에 기록했다. Effect(효과): Stage126(126단계) 수리 실패를 숨기지 않고 다음 수리 경계의 입력으로 쓴다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage127_v41_shortgate_quality_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage126_closeout_commit: {SOURCE_STAGE126_CLOSEOUT_COMMIT}
  source_stage126_latest_commit: {SOURCE_STAGE126_LATEST_COMMIT}
  source_stage125_latest_commit: {SOURCE_STAGE125_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage127_v41_shortgate_quality_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage127_v41_shortgate_quality_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage127 Selection Status(127단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE126_ID}`
- source_decision(원천 판정): `continue_shortgate_quality_followup_review_in_stage127_due_to_damage_or_no_repair`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage127_decision(127단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage127 Review Index(127단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- segment_failure_summary(구간 실패 요약): `{rel(SEGMENT_REVIEW_PATH)}`
- repair_route_decision(수리 경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
""",
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage128_quality_reframe_after_shortgate_failure_surface`
- status(상태): `stage127_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage127(127단계) closed(종료) as v2-native v41 shortgate quality follow-up review(브이투 고유 브이41 숏 게이트 품질 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage128(128단계) quality-density reframe(품질-밀도 재구성)으로 이어진다.

## Latest Stage127 Evidence(최신 127단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- segment_failure_summary(구간 실패 요약): `{rel(SEGMENT_REVIEW_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage127 v41 shortgate quality follow-up review closeout(127단계 v41 숏 게이트 품질 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage126 shortgate repair(126단계 숏 게이트 수리)이 34D KPI(34D 핵심 성과 지표) 격차를 줄이지 못했음을 기록하고 Stage128 quality-density reframe(128단계 품질-밀도 재구성)으로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = build_rows()
    best = best_row(rows)
    segment_review = build_segment_review(best)
    route_decision = build_route_decision(best)
    write_csv(GAP_SUMMARY_PATH, formatted_gap_rows(rows), gap_columns())
    write_csv(SEGMENT_REVIEW_PATH, segment_review, ["run_id", "adapter_id", "segment", "profit_factor", "net_profit", "max_drawdown_percent", "trade_count", "issue_label"])
    write_csv(ROUTE_DECISION_PATH, route_decision, ["run_id", "decision", "best_adapter", "best_oos_profit_factor", "best_oos_net_profit", "best_oos_max_drawdown_percent", "best_oos_trade_count", "stage127_read", "next_stage_or_branch", "repair_focus", "forbidden_route", "overall_goal_complete"])
    write_md(REPORT_PATH, report_markdown(rows, segment_review))
    write_md(DECISION_PATH, decision_markdown())
    ledger_payload = write_ledgers(best)
    write_packet_files(best, ledger_payload)
    update_current_truth()
    append_changelog()
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": RUN_ID,
                "decision": DECISION,
                "best_adapter": best.get("adapter_id", ""),
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
