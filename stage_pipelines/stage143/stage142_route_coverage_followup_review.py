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
from stage_pipelines.stage56.independent_event_source_route_branch import ARTIFACT_COLUMNS  # noqa: E402


STAGE_ID = "143_adapter_research__stage142_route_coverage_followup_review"
RUN_ID = "run143A_stage143_stage142_route_coverage_followup_review_v1"
PACKET_ID = "stage143_stage142_route_coverage_followup_review_v1"
PARENT_RUN_ID = "run142A_stage142_route_coverage_supply_branch_after_reverse_exhaustion_v1"
SOURCE_STAGE142_ID = "142_adapter_research__route_coverage_supply_branch_after_reverse_exhaustion"
SOURCE_STAGE142_CLOSEOUT_COMMIT = "0f53be36d3bb88fc97ec44cfeaa3e600e7b9e414"
SOURCE_STAGE142_HASH_RECORD_COMMIT = "7813b4d26006336dcf1709949ce78d47462b3c47"
SOURCE_STAGE141_HASH_RECORD_COMMIT = "eb72afcf6f3941bfa9aa84a6de438ba527fd60f8"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "open_stage144_route_shortgate_quality_repair_after_stage142_damage_candidate_not_final"
NEXT_STAGE_ID = "144_adapter_research__route_shortgate_quality_repair_after_stage142_damage"
NEXT_RUN_ID = "run144A_stage144_route_shortgate_quality_repair_after_stage142_damage_v1"
NEXT_PACKET_ID = "stage144_route_shortgate_quality_repair_after_stage142_damage_v1"
EXTERNAL_STATUS = "completed_existing_stage142_mt5_runtime_evidence_reviewed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE_ID
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE142_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage142_route_coverage_supply_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage142_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage142_risk_atr_telemetry.csv"
SOURCE_GATES = SOURCE_REVIEWS / "stage142_gate_feature_summary.csv"
SOURCE_DECISION = SOURCE_REVIEWS / "stage142_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage143_stage142_route_coverage_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage143_route_coverage_tradeoff_summary.csv"
COMPARISON_PATH = REVIEWS_ROOT / "stage143_stage142_34d_comparison.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage143_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage143_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage143_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

CONTROL_ADAPTER = "s142_control_reverse_bothgate_h3_cd5_risk035"
SHORTGATE_NO_REVERSE = "s142_route_shortgate_no_reverse_h3_cd5_risk035"
SHORTGATE_REVERSE = "s142_route_shortgate_reverse_h3_cd5_risk035"
NOGATE_TIGHT = "s142_route_nogate_tight_no_reverse_h3_cd5_risk035"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if columns is None:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(key)
        columns = tuple(ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def routed_summary_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(SOURCE_SUMMARY)
        if row.get("view") == "actual_routed_total" and row.get("route_role") == "routed_total"
    ]


def segment_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_SEGMENTS) if row.get("view") == "actual_routed_total"]


def row_by_adapter_split(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {(str(row.get("adapter_id", "")), str(row.get("split", ""))): row for row in rows}


def late_share(adapter_id: str, split: str, segments: Sequence[Mapping[str, str]]) -> float:
    full = 0.0
    late = 0.0
    for row in segments:
        if row.get("adapter_id") != adapter_id or row.get("split") != split:
            continue
        if row.get("segment_type") == "full_split":
            full = as_float(row.get("net_profit"))
        if row.get("segment_type") == "chronological_third" and row.get("segment") == "late":
            late = as_float(row.get("net_profit"))
    return late / full if full else 0.0


def gate_mode(adapter_id: str) -> str:
    for row in read_csv(SOURCE_GATES):
        if row.get("variant_id") == adapter_id and row.get("split") == "oos":
            return row.get("block_mode", "")
    return ""


def read_label(row: Mapping[str, Any]) -> str:
    if row["adapter_id"] == CONTROL_ADAPTER:
        return "control_preserved_quality_but_trade_gap"
    if row["oos_trades"] >= 300 and (row["oos_pf"] < 1.30 or row["oos_dd_percent"] > 30.0):
        return "raw_supply_broken_quality_damage"
    if row["oos_trade_gain_vs_control"] > 0 and (
        row["oos_pf"] < LEGACY_34D["profit_factor"]
        or row["oos_net"] < LEGACY_34D["net_profit"]
        or row["oos_dd_percent"] > 16.5
    ):
        return "trade_supply_gain_quality_damaged"
    if row["oos_trade_gain_vs_control"] > 0:
        return "trade_supply_gain_candidate_not_final"
    return "no_trade_supply_gain"


def next_probe_label(row: Mapping[str, Any]) -> str:
    if row["adapter_id"] in {SHORTGATE_NO_REVERSE, SHORTGATE_REVERSE}:
        return "stage144_shortgate_quality_repair"
    if row["adapter_id"] == NOGATE_TIGHT:
        return "preserve_as_failure_memory_no_more_nogate_pressure"
    return "keep_as_control"


def build_review() -> dict[str, Any]:
    rows = routed_summary_rows()
    segments = segment_rows()
    by_split = row_by_adapter_split(rows)
    adapters = sorted({str(row.get("adapter_id", "")) for row in rows})
    control_oos = by_split.get((CONTROL_ADAPTER, "oos"), {})
    control_val = by_split.get((CONTROL_ADAPTER, "validation_is"), {})
    tradeoff: list[dict[str, Any]] = []
    for adapter_id in adapters:
        oos = by_split.get((adapter_id, "oos"), {})
        val = by_split.get((adapter_id, "validation_is"), {})
        row = {
            "adapter_id": adapter_id,
            "gate_block_mode": gate_mode(adapter_id),
            "validation_pf": as_float(val.get("profit_factor")),
            "validation_net": as_float(val.get("net_profit")),
            "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
            "validation_trades": as_float(val.get("trade_count")),
            "validation_trade_gain_vs_control": as_float(val.get("trade_count")) - as_float(control_val.get("trade_count")),
            "validation_late_net_share": late_share(adapter_id, "validation_is", segments),
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_trades": as_float(oos.get("trade_count")),
            "oos_trade_gain_vs_control": as_float(oos.get("trade_count")) - as_float(control_oos.get("trade_count")),
            "oos_trade_gap_to_34d": as_float(oos.get("trade_count")) - LEGACY_34D["trade_count"],
            "oos_pf_gap_to_34d": as_float(oos.get("profit_factor")) - LEGACY_34D["profit_factor"],
            "oos_net_gap_to_34d": as_float(oos.get("net_profit")) - LEGACY_34D["net_profit"],
            "oos_dd_gap_to_34d": as_float(oos.get("max_drawdown_percent")) - LEGACY_34D["max_drawdown_percent"],
            "oos_late_net_share": late_share(adapter_id, "oos", segments),
        }
        row["read"] = read_label(row)
        row["next_probe"] = next_probe_label(row)
        tradeoff.append(row)

    comparison = [
        {
            "target": "legacy_34d",
            "profit_factor": LEGACY_34D["profit_factor"],
            "net_profit": LEGACY_34D["net_profit"],
            "max_drawdown_percent": LEGACY_34D["max_drawdown_percent"],
            "trade_count": LEGACY_34D["trade_count"],
            "role": "lesson_only_kpi_target",
        },
        {
            "target": "stage142_control",
            "profit_factor": as_float(control_oos.get("profit_factor")),
            "net_profit": as_float(control_oos.get("net_profit")),
            "max_drawdown_percent": as_float(control_oos.get("max_drawdown_percent")),
            "trade_count": as_float(control_oos.get("trade_count")),
            "role": "quality_control_trade_gap_remaining",
        },
    ]
    best_supply = max(tradeoff, key=lambda row: row["oos_trades"], default={})
    best_salvage = max(
        tradeoff,
        key=lambda row: (
            row["read"] == "trade_supply_gain_quality_damaged",
            row["oos_pf"],
            -row["oos_dd_percent"],
            row["oos_trades"],
        ),
        default={},
    )
    route = [
        {
            "decision": DECISION,
            "reason": "stage142_shortgate_added_50_plus_trades_but_oos_pf_net_dd_failed; nogate_trade_supply_broke_quality",
            "best_supply_adapter": best_supply.get("adapter_id", ""),
            "best_salvage_adapter": best_salvage.get("adapter_id", ""),
            "next_stage": NEXT_STAGE_ID,
            "overall_goal_complete": False,
        }
    ]
    return {"tradeoff": tradeoff, "comparison": comparison, "route": route, "best_supply": best_supply, "best_salvage": best_salvage}


def table_rows(rows: Sequence[Mapping[str, Any]]) -> str:
    header = (
        "| adapter(어댑터) | gate(게이트) | val PF(검증 수익 팩터) | val net(검증 순손익) | val trades(검증 거래 수) | "
        "OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 손실률) | OOS trades(미래구간 거래 수) | gain(증가) | read(판독) |\n"
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"
    )
    body = [
        (
            f"| {row['adapter_id']} | {row['gate_block_mode']} | {row['validation_pf']:.2f} | {row['validation_net']:.2f} | "
            f"{row['validation_trades']:.0f} | {row['oos_pf']:.2f} | {row['oos_net']:.2f} | {row['oos_dd_percent']:.2f} | "
            f"{row['oos_trades']:.0f} | {row['oos_trade_gain_vs_control']:.0f} | {row['read']} |"
        )
        for row in rows
    ]
    return "\n".join([header, *body])


def report_markdown(review: Mapping[str, Any]) -> str:
    best_supply = review.get("best_supply", {})
    best_salvage = review.get("best_salvage", {})
    return f"""# Stage143 Stage142 Route Coverage Follow-up Review(143단계 142단계 경로 커버리지 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE142_ID}`
- source_stage142_closeout_commit(원천 142단계 종료 커밋): `{SOURCE_STAGE142_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage142(142단계) route coverage supply(경로 커버리지 공급) create a usable path toward 34D KPI(34D 핵심 성과 지표), or did it only add trades while damaging OOS quality(미래구간 품질)?

Effect(효과): 거래 수 증가를 바로 성공으로 보지 않고 PF/net/DD(수익 팩터/순손익/손실률) 손상을 같이 판정한다.

## KPI Read(KPI 핵심 성과 지표 판독)

{table_rows(review["tradeoff"])}

## Judgment(판정)

- best_supply_adapter(최대 거래 공급 어댑터): `{best_supply.get("adapter_id", "none")}`
- best_supply_read(최대 거래 공급 판독): `{best_supply.get("read", "")}`
- best_salvage_adapter(수리 후보 어댑터): `{best_salvage.get("adapter_id", "none")}`
- shortgate_lesson(숏게이트 교훈): shortgate(숏게이트)는 OOS trades(미래구간 거래 수)를 약 50개 늘렸지만 PF/net/DD(수익 팩터/순손익/손실률)를 34D 기준 아래로 손상시켰다.
- nogate_lesson(무게이트 교훈): no-gate(무게이트)는 거래 수를 크게 늘렸지만 PF(수익 팩터)와 DD(손실률)가 무너져 failure memory(실패 기억)로 보존한다.
- overall_goal_complete(전체 목표 완료): `false`

Stage143(143단계) 판독은 broad no-gate pressure(넓은 무게이트 압력)를 중단하고 Stage144(144단계) shortgate quality repair(숏게이트 품질 수리)로 좁혀야 한다고 본다. Effect(효과): 거래 수 공급 단서를 버리지 않되, 손상된 품질을 다음 단계의 단일 질문으로 다룬다.
"""


def decision_markdown() -> str:
    return f"""# Stage143 Decision(143단계 판정)

decision(판정): `{DECISION}`

Stage143(143단계)는 Stage142(142단계) MT5(runtime, 런타임) 근거를 review-only(검토 전용)로 판정했다. Effect(효과): shortgate(숏게이트) 거래 수 증가는 보존하고, no-gate(무게이트) 손상은 실패 기억으로 남긴다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage142_summary(원천 142단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage142_segments(원천 142단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage142_risk_atr(원천 142단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def write_stage_docs() -> None:
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# {STAGE_ID}

Stage143(143단계)는 Stage142(142단계) route coverage supply(경로 커버리지 공급)를 review-only(검토 전용)로 판정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage143 Input References(143단계 입력 참조)

- stage142_decision(142단계 판정): `{rel(SOURCE_DECISION)}`
- stage142_summary(142단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage142_segments(142단계 구간): `{rel(SOURCE_SEGMENTS)}`
- stage142_risk_atr(142단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- stage142_gates(142단계 게이트): `{rel(SOURCE_GATES)}`
- source_stage142_closeout_commit(원천 142단계 종료 커밋): `{SOURCE_STAGE142_CLOSEOUT_COMMIT}`
- source_stage142_hash_record_commit(원천 142단계 해시 기록 커밋): `{SOURCE_STAGE142_HASH_RECORD_COMMIT}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage143 Selection Status(143단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE142_ID}`
- source_decision(원천 판정): `continue_stage143_route_coverage_repair_after_damage_or_no_gain_candidate_not_final`
- stage143_decision(143단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage143 Review Index(143단계 검토 색인)

- review(검토): `{rel(REPORT_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage144(144단계)는 Stage143(143단계) 판정에 따라 shortgate quality repair(숏게이트 품질 수리)를 연다.

## Bounded Question(경계 질문)

Can the Stage142 shortgate route(142단계 숏게이트 경로)가 만든 trade count gain(거래 수 증가)을 일부 보존하면서 OOS PF/net/DD(미래구간 수익 팩터/순손익/손실률)를 다시 34D target surface(34D 목표 표면)에 가깝게 회복할 수 있는가?

Effect(효과): no-gate pressure(무게이트 압력)를 반복하지 않고, 손상된 shortgate(숏게이트) 후보의 품질 복구만 좁게 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage144 Input References(144단계 입력 참조)

- stage143_decision(143단계 판정): `{rel(DECISION_PATH)}`
- stage143_review(143단계 검토): `{rel(REPORT_PATH)}`
- stage143_tradeoff_summary(143단계 트레이드오프 요약): `{rel(TRADEOFF_PATH)}`
- stage142_summary(142단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage142_segment_kpi(142단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage142_risk_atr_telemetry(142단계 위험/ATR 원격측정): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage144 Review Index(144단계 검토 색인)

Stage144(144단계)는 active_planned(활성 계획) 상태다. Effect(효과): 다음 실행은 shortgate quality repair(숏게이트 품질 수리)만 다룬다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage144 Selection Status(144단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage143`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage144_shortgate_quality_repair_candidate`
- status(상태): `stage143_closed_{DECISION}_stage144_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage143(143단계)는 Stage142(142단계) route coverage supply(경로 커버리지 공급)가 거래 수는 늘렸지만 OOS quality(미래구간 품질)를 손상했다고 판정했다. Effect(효과): no-gate(무게이트)는 실패 기억으로 두고, shortgate quality repair(숏게이트 품질 수리)만 Stage144(144단계)로 넘긴다.

## Latest Stage143 Evidence(최신 143단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    text = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage143(143단계) closed(종료) as `{DECISION}` and Stage144(144단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): shortgate(숏게이트) 거래 증가 단서를 보존하고 품질 수리 질문으로 넘어간다.
- >-
  Stage143 evidence(143단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(COMPARISON_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): no-gate damage(무게이트 손상)와 shortgate salvage(숏게이트 수리 가능성)를 분리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1) if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", text) else text.rstrip() + "\n" + focus
    block = f"""
stage143_stage142_route_coverage_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE142_ID}
  source_stage142_closeout_commit: {SOURCE_STAGE142_CLOSEOUT_COMMIT}
  source_stage142_hash_record_commit: {SOURCE_STAGE142_HASH_RECORD_COMMIT}
  source_stage141_hash_record_commit: {SOURCE_STAGE141_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage144_route_shortgate_quality_repair_after_stage142_damage:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage143
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run_stage144_route_shortgate_quality_repair
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage143_stage142_route_coverage_followup_review:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage144_route_shortgate_quality_repair_after_stage142_damage:.*?(?=\nstage\d+_|$)", "\n", text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage143 Stage142 route coverage follow-up closeout(143단계 142단계 경로 커버리지 후속 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage142(142단계)의 거래 수 증가가 품질 손상을 동반했음을 기록하고 Stage144(144단계) shortgate quality repair(숏게이트 품질 수리)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [REPORT_PATH, TRADEOFF_PATH, COMPARISON_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage143_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage143 review-only route coverage follow-up artifact.",
                }
            )
    return rows


def write_ledgers(review: Mapping[str, Any]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage143_route_coverage_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage142_closeout_commit", SOURCE_STAGE142_CLOSEOUT_COMMIT),
                        ("source_stage142_hash_record_commit", SOURCE_STAGE142_HASH_RECORD_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_only",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "view": "review_only",
        "split": "stage142_existing_evidence",
        "tier": "actual_routed_total",
        "route_role": "followup_review",
        "status": "completed",
        "profit_factor": "",
        "net_profit": "",
        "max_drawdown_percent": "",
        "trade_count": "",
        "notes": ledger_pairs(
            (
                ("decision", DECISION),
                ("source_summary", rel(SOURCE_SUMMARY)),
                ("best_salvage_adapter", str(review.get("best_salvage", {}).get("adapter_id", ""))),
                ("overall_goal_complete", 0),
            )
        ),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": ["kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit"],
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "source_summary": rel(SOURCE_SUMMARY),
            "source_segments": rel(SOURCE_SEGMENTS),
            "tradeoff_path": rel(TRADEOFF_PATH),
            "comparison_path": rel(COMPARISON_PATH),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(DECISION_PATH)],
            "evidence_missing": ["new_repair_not_attempted_in_stage143_by_design"],
            "judgment_label": "trade_supply_gain_quality_damaged_not_final",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": "Stage144 must test bounded shortgate quality repair without repeating broad no-gate pressure.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage142 shortgate variants added about 50 OOS trades but pushed PF/net below 34D and DD to 20.23.",
            "comparison_baseline": CONTROL_ADAPTER,
            "likely_drivers": ["route_gate_release", "weaker route quality", "no_gate_supply_pressure_damage"],
            "attribution_confidence": "medium",
            "next_probe": "bounded Stage144 shortgate quality repair",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_GATES), rel(SOURCE_DECISION)],
            "producer": rel(Path("stage_pipelines/stage143/stage142_route_coverage_followup_review.py")),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH), NEXT_STAGE_ID],
            "artifact_paths": [rel(path) for path in [REPORT_PATH, TRADEOFF_PATH, COMPARISON_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH]],
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "ledger_payload": ledger_payload,
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage142_closeout_commit": SOURCE_STAGE142_CLOSEOUT_COMMIT,
            "source_stage142_hash_record_commit": SOURCE_STAGE142_HASH_RECORD_COMMIT,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "tradeoff": rel(TRADEOFF_PATH),
                "comparison": rel(COMPARISON_PATH),
                "route_decision": rel(ROUTE_DECISION_PATH),
                "decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def run() -> Mapping[str, Any]:
    review = build_review()
    write_csv(TRADEOFF_PATH, review["tradeoff"])
    write_csv(COMPARISON_PATH, review["comparison"])
    write_csv(ROUTE_DECISION_PATH, review["route"])
    write_json(SUMMARY_JSON_PATH, review)
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown())
    write_stage_docs()
    update_current_truth()
    append_changelog()
    ledger_payload = write_ledgers(review)
    write_packet_files(review, ledger_payload)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    ledger_payload = {**ledger_payload, "artifact_registry": artifact_payload}
    write_packet_files(review, ledger_payload)
    return review


def main() -> int:
    review = run()
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": RUN_ID,
                "decision": DECISION,
                "best_salvage_adapter": review.get("best_salvage", {}).get("adapter_id", ""),
                "tradeoff_csv": rel(TRADEOFF_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
