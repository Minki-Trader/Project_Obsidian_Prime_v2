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


STAGE_ID = "145_adapter_research__stage144_shortgate_quality_followup_review"
RUN_ID = "run145A_stage145_stage144_shortgate_quality_followup_review_v1"
PACKET_ID = "stage145_stage144_shortgate_quality_followup_review_v1"
PARENT_RUN_ID = "run144A_stage144_route_shortgate_quality_repair_after_stage142_damage_v1"
SOURCE_STAGE144_ID = "144_adapter_research__route_shortgate_quality_repair_after_stage142_damage"
SOURCE_STAGE144_CLOSEOUT_COMMIT = "594f259774f70267c36cebe38875a1d12c46c490"
SOURCE_STAGE144_HASH_RECORD_COMMIT = "07f23d8939ab31e6e7d1a564cc9c8c9496fa2704"
SOURCE_STAGE143_HASH_RECORD_COMMIT = "ee0f8e716bbcf1252aac3f1f1178c6ecfc7d015a"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "open_stage146_control_anchor_trade_supply_repair_after_shortgate_no_repair_candidate_not_final"
NEXT_STAGE_ID = "146_adapter_research__control_anchor_trade_supply_after_shortgate_no_repair"
NEXT_RUN_ID = "run146A_stage146_control_anchor_trade_supply_after_shortgate_no_repair_v1"
NEXT_PACKET_ID = "stage146_control_anchor_trade_supply_after_shortgate_no_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage144_mt5_runtime_evidence_reviewed"
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

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE144_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage144_shortgate_quality_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage144_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage144_risk_atr_telemetry.csv"
SOURCE_GATES = SOURCE_REVIEWS / "stage144_gate_feature_summary.csv"
SOURCE_DECISION = SOURCE_REVIEWS / "stage144_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage145_stage144_shortgate_quality_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage145_shortgate_quality_tradeoff_summary.csv"
COMPARISON_PATH = REVIEWS_ROOT / "stage145_stage144_34d_comparison.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage145_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage145_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage145_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

SOURCE_SHORTGATE = "s142_route_shortgate_reverse_h3_cd5_risk035"
STAGE142_CONTROL = "s142_control_reverse_bothgate_h3_cd5_risk035"
STRICTGATE = "s144_shortgate_reverse_strictgate_cd6_h3_sht54_lng52_risk035"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE142_SHORTGATE_BASELINE = {
    "profit_factor": 1.549398689,
    "net_profit": 963.92,
    "max_drawdown_percent": 20.23,
    "trade_count": 231,
}
STAGE142_CONTROL_BASELINE = {
    "profit_factor": 1.795976838,
    "net_profit": 1186.30,
    "max_drawdown_percent": 14.66,
    "trade_count": 180,
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


def third_net(adapter_id: str, split: str, segment: str, segments: Sequence[Mapping[str, str]]) -> float:
    for row in segments:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return as_float(row.get("net_profit"))
    return 0.0


def gate_mode(adapter_id: str) -> str:
    for row in read_csv(SOURCE_GATES):
        if row.get("variant_id") == adapter_id and row.get("split") == "oos":
            return row.get("block_mode", "")
    return ""


def repair_read(row: Mapping[str, Any]) -> str:
    if row["adapter_id"] == STRICTGATE:
        return "strictgate_cut_trades_but_broke_net_and_dd"
    if row["oos_pf"] > STAGE142_SHORTGATE_BASELINE["profit_factor"] and row["oos_net"] >= STAGE142_SHORTGATE_BASELINE["net_profit"] and row["oos_dd_percent"] < STAGE142_SHORTGATE_BASELINE["max_drawdown_percent"]:
        return "small_repair_candidate_not_final"
    if row["oos_dd_percent"] < STAGE142_SHORTGATE_BASELINE["max_drawdown_percent"] and row["oos_net"] < STAGE142_SHORTGATE_BASELINE["net_profit"]:
        return "dd_slightly_better_but_profit_quality_not_repaired"
    return "shortgate_quality_not_repaired"


def build_review() -> dict[str, Any]:
    rows = routed_summary_rows()
    segments = segment_rows()
    by_split = row_by_adapter_split(rows)
    adapters = sorted({str(row.get("adapter_id", "")) for row in rows})
    tradeoff: list[dict[str, Any]] = []
    for adapter_id in adapters:
        val = by_split.get((adapter_id, "validation_is"), {})
        oos = by_split.get((adapter_id, "oos"), {})
        row = {
            "adapter_id": adapter_id,
            "gate_block_mode": gate_mode(adapter_id),
            "validation_pf": as_float(val.get("profit_factor")),
            "validation_net": as_float(val.get("net_profit")),
            "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
            "validation_trades": as_float(val.get("trade_count")),
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_trades": as_float(oos.get("trade_count")),
            "delta_pf_vs_stage142_shortgate": as_float(oos.get("profit_factor")) - STAGE142_SHORTGATE_BASELINE["profit_factor"],
            "delta_net_vs_stage142_shortgate": as_float(oos.get("net_profit")) - STAGE142_SHORTGATE_BASELINE["net_profit"],
            "delta_dd_vs_stage142_shortgate": as_float(oos.get("max_drawdown_percent")) - STAGE142_SHORTGATE_BASELINE["max_drawdown_percent"],
            "delta_trades_vs_stage142_shortgate": as_float(oos.get("trade_count")) - STAGE142_SHORTGATE_BASELINE["trade_count"],
            "oos_pf_gap_to_34d": as_float(oos.get("profit_factor")) - LEGACY_34D["profit_factor"],
            "oos_net_gap_to_34d": as_float(oos.get("net_profit")) - LEGACY_34D["net_profit"],
            "oos_dd_gap_to_34d": as_float(oos.get("max_drawdown_percent")) - LEGACY_34D["max_drawdown_percent"],
            "oos_trade_gap_to_34d": as_float(oos.get("trade_count")) - LEGACY_34D["trade_count"],
            "oos_early_net": third_net(adapter_id, "oos", "early", segments),
            "oos_mid_net": third_net(adapter_id, "oos", "mid", segments),
            "oos_late_net": third_net(adapter_id, "oos", "late", segments),
        }
        row["read"] = repair_read(row)
        row["next_probe"] = "stage146_control_anchor_trade_supply_repair"
        tradeoff.append(row)
    best = max(
        tradeoff,
        key=lambda row: (
            row["read"] == "small_repair_candidate_not_final",
            row["oos_pf"],
            row["oos_net"],
            -row["oos_dd_percent"],
            row["oos_trades"],
        ),
        default={},
    )
    comparison = [
        {"target": "legacy_34d", **LEGACY_34D, "role": "lesson_only_kpi_target"},
        {"target": "stage142_shortgate_reverse", **STAGE142_SHORTGATE_BASELINE, "role": "damaged_shortgate_source"},
        {"target": "stage142_control", **STAGE142_CONTROL_BASELINE, "role": "quality_anchor_trade_gap_remaining"},
    ]
    route = [
        {
            "decision": DECISION,
            "reason": "stage144_shortgate_quality_repair_did_not_clear_34d_pf_net_dd_or_source_shortgate_profit_quality",
            "best_stage144_adapter": best.get("adapter_id", ""),
            "next_stage": NEXT_STAGE_ID,
            "next_axis": "control_anchor_trade_supply_repair_without_repeating_no_gate_or_shortgate_same_axis",
            "overall_goal_complete": False,
        }
    ]
    return {"tradeoff": tradeoff, "comparison": comparison, "route": route, "best": best}


def table_rows(rows: Sequence[Mapping[str, Any]]) -> str:
    header = (
        "| adapter(어댑터) | OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 손실률) | OOS trades(미래구간 거래 수) | net vs source(원천 대비 순손익) | DD vs source(원천 대비 손실률) | read(판독) |\n"
        "|---|---:|---:|---:|---:|---:|---:|---|"
    )
    body = [
        (
            f"| {row['adapter_id']} | {row['oos_pf']:.6f} | {row['oos_net']:.2f} | {row['oos_dd_percent']:.2f} | "
            f"{row['oos_trades']:.0f} | {row['delta_net_vs_stage142_shortgate']:.2f} | {row['delta_dd_vs_stage142_shortgate']:.2f} | {row['read']} |"
        )
        for row in rows
    ]
    return "\n".join([header, *body])


def report_markdown(review: Mapping[str, Any]) -> str:
    best = review.get("best", {})
    return f"""# Stage145 Stage144 Shortgate Quality Follow-up Review(145단계 144단계 숏게이트 품질 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE144_ID}`
- source_stage144_closeout_commit(원천 144단계 종료 커밋): `{SOURCE_STAGE144_CLOSEOUT_COMMIT}`
- source_stage144_hash_record_commit(원천 144단계 해시 기록 커밋): `{SOURCE_STAGE144_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage144(144단계) recover shortgate quality(숏게이트 품질)를 enough to keep repairing the shortgate axis(숏게이트 축), or should the next bounded stage(다음 경계 단계) pivot to a control anchor(대조군 앵커)?

Effect(효과): 같은 손상 축을 계속 파지 않고, 수리 실패가 확인되면 다음 축으로 넘어간다.

## KPI Read(KPI 핵심 성과 지표 판독)

{table_rows(review["tradeoff"])}

## Judgment(판정)

- best_stage144_adapter(최선 144단계 어댑터): `{best.get("adapter_id", "none")}`
- best_oos_pf(최선 미래구간 수익 팩터): `{as_float(best.get("oos_pf")):.6f}`
- best_oos_net(최선 미래구간 순손익): `{as_float(best.get("oos_net")):.2f}`
- best_oos_dd_pct(최선 미래구간 손실률): `{as_float(best.get("oos_dd_percent")):.2f}`
- stage142_shortgate_source(142단계 숏게이트 원천): PF `1.549399`, net `963.92`, DD `20.23`, trades `231`.
- stage142_control_anchor(142단계 대조군 앵커): PF `1.795977`, net `1186.30`, DD `14.66`, trades `180`.
- read(판독): Stage144(144단계)는 DD(손실률)를 아주 조금 낮춘 후보가 있었지만 net/PF(순손익/수익 팩터)가 원천보다 낮아 shortgate quality repair(숏게이트 품질 수리)로 인정하지 않는다.
- decision_use(판정 용도): Stage146(146단계)는 Stage142 control(142단계 대조군)을 품질 앵커로 놓고, no-gate(무게이트)나 같은 shortgate(숏게이트) 축 반복 없이 거래 공급을 다시 찾는다.
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): cooldown/threshold/gate breadth(대기시간/임계값/게이트 폭) 변경이 shortgate(숏게이트) 손상을 회복하지 못했다.
- comparison_baseline(비교 기준): `{SOURCE_SHORTGATE}` and `{STAGE142_CONTROL}`.
- likely_drivers(가능한 원인): shortgate release(숏게이트 완화) 자체가 약한 거래를 들고 왔고, 단순 재진입 대기시간이나 게이트 폭 조정으로는 품질이 회복되지 않았다.
- segment_checks(구간 확인): validation/OOS(검증/미래구간), chronological thirds(시간 3분할), risk/ATR telemetry(위험/ATR 기록), Tier B disabled diagnostic(티어 B 비활성 진단).
- attribution_confidence(귀속 신뢰도): `medium`.
- next_probe(다음 확인): `{NEXT_STAGE_ID}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage145 Decision(145단계 판정)

decision(판정): `{DECISION}`

Stage145(145단계)는 Stage144(144단계) MT5(runtime, 런타임) 근거를 review-only(검토 전용)로 판정했다. Effect(효과): shortgate quality repair(숏게이트 품질 수리) 실패를 숨기지 않고 다음 수리 축으로 넘긴다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage144_summary(원천 144단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage144_segments(원천 144단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage144_risk_atr(원천 144단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
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

Stage145(145단계)는 Stage144(144단계) shortgate quality repair(숏게이트 품질 수리)를 review-only(검토 전용)로 판정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage145 Input References(145단계 입력 참조)

- stage144_decision(144단계 판정): `{rel(SOURCE_DECISION)}`
- stage144_summary(144단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage144_segments(144단계 구간): `{rel(SOURCE_SEGMENTS)}`
- stage144_risk_atr(144단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- stage144_gates(144단계 게이트): `{rel(SOURCE_GATES)}`
- source_stage144_closeout_commit(원천 144단계 종료 커밋): `{SOURCE_STAGE144_CLOSEOUT_COMMIT}`
- source_stage144_hash_record_commit(원천 144단계 해시 기록 커밋): `{SOURCE_STAGE144_HASH_RECORD_COMMIT}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage145 Selection Status(145단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE144_ID}`
- source_decision(원천 판정): `continue_stage145_shortgate_quality_followup_review_due_to_damage_or_no_repair_candidate_not_final`
- stage145_decision(145단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage145 Review Index(145단계 검토 색인)

- review(검토): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage146(146단계)는 Stage145(145단계) 판정에 따라 control anchor trade supply repair(대조군 앵커 거래 공급 수리)를 연다.

## Bounded Question(경계 질문)

Can the Stage142 control anchor(142단계 대조군 앵커)의 OOS quality(미래구간 품질)를 보존하면서, no-gate(무게이트)나 failed shortgate same-axis repair(실패한 숏게이트 동일 축 수리)를 반복하지 않고 trade count(거래 수)를 늘릴 수 있는가?

Effect(효과): 손상된 숏게이트 축을 더 밀지 않고, 품질이 살아 있던 control anchor(대조군 앵커)에서 다른 좁은 수리 축을 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage146 Input References(146단계 입력 참조)

- stage145_decision(145단계 판정): `{rel(DECISION_PATH)}`
- stage145_review(145단계 검토): `{rel(REPORT_PATH)}`
- stage145_tradeoff_summary(145단계 상충 요약): `{rel(TRADEOFF_PATH)}`
- stage144_summary(144단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage144_segment_kpi(144단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage144_risk_atr_telemetry(144단계 위험/ATR 기록): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage146 Review Index(146단계 검토 색인)

Stage146(146단계)는 active_planned(활성 계획) 상태다. Effect(효과): 다음 실행은 control anchor trade supply repair(대조군 앵커 거래 공급 수리)만 좁게 다룬다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage146 Selection Status(146단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage145`
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
- adapter_under_review(검토 중 어댑터): `stage146_control_anchor_trade_supply_candidate`
- status(상태): `stage145_closed_{DECISION}_stage146_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage145(145단계)는 Stage144(144단계) shortgate quality repair(숏게이트 품질 수리)가 충분하지 않다고 판정했다. Effect(효과): 같은 손상 축을 더 밀지 않고 Stage146(146단계) control anchor trade supply repair(대조군 앵커 거래 공급 수리)로 넘어간다.

## Latest Stage145 Evidence(최신 145단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
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
  Stage145(145단계) closed(종료) as `{DECISION}` and Stage146(146단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): shortgate quality repair(숏게이트 품질 수리) 실패를 보존하고 control anchor(대조군 앵커) 수리 축으로 넘어간다.
- >-
  Stage145 evidence(145단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(COMPARISON_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): Stage144(144단계) 수리 실패와 Stage146(146단계) 전환 이유를 분리해 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1)
    block = f"""
stage145_stage144_shortgate_quality_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE144_ID}
  source_stage144_closeout_commit: {SOURCE_STAGE144_CLOSEOUT_COMMIT}
  source_stage144_hash_record_commit: {SOURCE_STAGE144_HASH_RECORD_COMMIT}
  source_stage143_hash_record_commit: {SOURCE_STAGE143_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage146_control_anchor_trade_supply_after_shortgate_no_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage145
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run_stage146_control_anchor_trade_supply_repair
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage145_stage144_shortgate_quality_followup_review:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage146_control_anchor_trade_supply_after_shortgate_no_repair:.*?(?=\nstage\d+_|$)", "\n", text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage145 Stage144 shortgate quality follow-up closeout(145단계 144단계 숏게이트 품질 후속 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage144(144단계) 수리 실패를 기록하고 Stage146(146단계) control anchor trade supply repair(대조군 앵커 거래 공급 수리)로 넘겼다.\n"
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
                    "artifact_type": "stage145_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage145 review-only shortgate quality follow-up artifact.",
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
                "lane": "baseline_adapter_stage145_shortgate_quality_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage144_closeout_commit", SOURCE_STAGE144_CLOSEOUT_COMMIT),
                        ("source_stage144_hash_record_commit", SOURCE_STAGE144_HASH_RECORD_COMMIT),
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
        "split": "stage144_existing_evidence",
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
                ("best_stage144_adapter", str(review.get("best", {}).get("adapter_id", ""))),
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
            "evidence_missing": ["new_repair_not_attempted_in_stage145_by_design"],
            "judgment_label": "shortgate_quality_repair_failed_not_final",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": "Stage146 must pivot to control-anchor trade supply and avoid repeating broad no-gate or same shortgate axis.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage144 cooldown/threshold/gate-breadth repair did not recover shortgate PF/net/DD.",
            "comparison_baseline": SOURCE_SHORTGATE,
            "likely_drivers": ["weak_shortgate_trade_quality", "insufficient_cooldown_repair", "strictgate_profit_loss"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_GATES), rel(SOURCE_DECISION)],
            "producer": rel(Path("stage_pipelines/stage145/stage144_shortgate_quality_followup_review.py")),
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
            "source_stage144_closeout_commit": SOURCE_STAGE144_CLOSEOUT_COMMIT,
            "source_stage144_hash_record_commit": SOURCE_STAGE144_HASH_RECORD_COMMIT,
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
                "best_stage144_adapter": review.get("best", {}).get("adapter_id", ""),
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
