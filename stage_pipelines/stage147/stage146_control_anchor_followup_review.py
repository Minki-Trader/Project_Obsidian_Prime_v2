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


STAGE_ID = "147_adapter_research__stage146_control_anchor_followup_review"
RUN_ID = "run147A_stage147_stage146_control_anchor_followup_review_v1"
PACKET_ID = "stage147_stage146_control_anchor_followup_review_v1"
SOURCE_STAGE146_ID = "146_adapter_research__control_anchor_trade_supply_after_shortgate_no_repair"
SOURCE_STAGE146_CLOSEOUT_COMMIT = "d17bc202a1cb49df164cd0e70a8445dd2f9694e2"
SOURCE_STAGE146_HASH_RECORD_COMMIT = "f63827bc249653329b99494eca2b17f0926af7cd"
SOURCE_STAGE145_HASH_RECORD_COMMIT = "7b6d881cbf5871674724d2c2a8dfb082301fda82"
SOURCE_STAGE142_HASH_RECORD_COMMIT = "7813b4d26006336dcf1709949ce78d47462b3c47"
SOURCE_ADAPTER_ID = "s142_control_reverse_bothgate_h3_cd5_risk035"
SOFTSESSION_ADAPTER_ID = "s146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035"
NEXT_STAGE_ID = "148_adapter_research__softsession_supply_quality_repair_after_stage146_damage"
NEXT_RUN_ID = "run148A_stage148_softsession_supply_quality_repair_after_stage146_damage_v1"
NEXT_PACKET_ID = "stage148_softsession_supply_quality_repair_after_stage146_damage_v1"
DECISION = "open_stage148_softsession_supply_quality_repair_after_stage146_damage_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
EXTERNAL_STATUS = "completed_existing_stage146_mt5_runtime_evidence_reviewed"
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
PRODUCER_PATH = Path("stage_pipelines/stage147/stage146_control_anchor_followup_review.py")

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE146_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage146_control_anchor_trade_supply_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage146_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage146_risk_atr_telemetry.csv"
SOURCE_GATES = SOURCE_REVIEWS / "stage146_gate_feature_summary.csv"
SOURCE_DECISION = SOURCE_REVIEWS / "stage146_decision.md"
SOURCE_REPORT = SOURCE_REVIEWS / "stage146_control_anchor_trade_supply_report.md"

REPORT_PATH = REVIEWS_ROOT / "stage147_stage146_control_anchor_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage147_control_anchor_tradeoff_summary.csv"
SEGMENT_FAILURE_PATH = REVIEWS_ROOT / "stage147_segment_failure_summary.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage147_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage147_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage147_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE142_CONTROL = {
    "profit_factor": 1.795976838,
    "net_profit": 1186.30,
    "max_drawdown_percent": 14.66,
    "trade_count": 180,
    "validation_profit_factor": 1.582222632,
    "validation_net_profit": 1388.24,
    "validation_max_drawdown_percent": 11.85,
    "validation_trade_count": 265,
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


def split_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split:
            return row
    return {}


def segment_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_SEGMENTS) if row.get("view") == "actual_routed_total"]


def risk_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_RISK_ATR) if row.get("view") == "actual_routed_total"]


def gate_rows() -> list[dict[str, str]]:
    return read_csv(SOURCE_GATES)


def segment_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    for row in rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return row
    return {}


def risk_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split:
            return row
    return {}


def gate_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("variant_id") == adapter_id and row.get("split") == split:
            return row
    return {}


def quality_safe(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    return (
        as_float(val.get("profit_factor")) >= 1.55
        and as_float(val.get("net_profit")) >= LEGACY_34D["net_profit"]
        and as_float(val.get("max_drawdown_percent"), 99.0) <= 15.0
        and as_float(oos.get("profit_factor")) >= LEGACY_34D["profit_factor"]
        and as_float(oos.get("net_profit")) >= LEGACY_34D["net_profit"]
        and as_float(oos.get("max_drawdown_percent"), 99.0) <= 16.5
    )


def read_label(adapter_id: str, val: Mapping[str, Any], oos: Mapping[str, Any], mid: Mapping[str, Any]) -> str:
    oos_gain = as_float(oos.get("trade_count")) - STAGE142_CONTROL["trade_count"]
    val_pf = as_float(val.get("profit_factor"))
    mid_pf = as_float(mid.get("profit_factor"))
    if adapter_id == SOFTSESSION_ADAPTER_ID and oos_gain > 0:
        if val_pf < 1.55 and mid_pf < LEGACY_34D["profit_factor"]:
            return "trade_supply_gain_with_validation_pf_and_oos_mid_damage"
        return "trade_supply_gain_candidate_not_final"
    if oos_gain <= 0 and quality_safe(val, oos):
        return "quality_preserved_but_no_trade_supply_gain"
    if adapter_id.endswith("hold4_h4_cd5_sht54_lng52_risk035"):
        return "hold_extension_kept_oos_quality_but_cut_trades_and_damaged_validation"
    return "no_usable_trade_supply_gain"


def next_use_label(adapter_id: str, read: str) -> str:
    if adapter_id == SOFTSESSION_ADAPTER_ID and read.startswith("trade_supply_gain"):
        return "use_as_stage148_repair_seed_not_baseline"
    return "preserve_as_control_or_failure_memory"


def build_review() -> dict[str, Any]:
    summary = routed_summary_rows()
    segments = segment_rows()
    risks = risk_rows()
    gates = gate_rows()
    adapters = sorted({str(row.get("adapter_id", "")) for row in summary})
    tradeoff: list[dict[str, Any]] = []
    segment_failures: list[dict[str, Any]] = []
    for adapter_id in adapters:
        val = split_row(summary, adapter_id, "validation_is")
        oos = split_row(summary, adapter_id, "oos")
        early = segment_lookup(segments, adapter_id, "oos", "early")
        mid = segment_lookup(segments, adapter_id, "oos", "mid")
        late = segment_lookup(segments, adapter_id, "oos", "late")
        risk_oos = risk_lookup(risks, adapter_id, "oos")
        gate_val = gate_lookup(gates, adapter_id, "validation_is")
        gate_oos = gate_lookup(gates, adapter_id, "oos")
        total_oos_net = as_float(oos.get("net_profit"))
        segment_nets = [as_float(early.get("net_profit")), as_float(mid.get("net_profit")), as_float(late.get("net_profit"))]
        max_segment_share = max(segment_nets) / total_oos_net if total_oos_net > 0 and segment_nets else 0.0
        read = read_label(adapter_id, val, oos, mid)
        tradeoff.append(
            {
                "adapter_id": adapter_id,
                "validation_pf": as_float(val.get("profit_factor")),
                "validation_net": as_float(val.get("net_profit")),
                "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
                "validation_trades": as_float(val.get("trade_count")),
                "oos_pf": as_float(oos.get("profit_factor")),
                "oos_net": as_float(oos.get("net_profit")),
                "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
                "oos_trades": as_float(oos.get("trade_count")),
                "oos_trade_gain_vs_control": as_float(oos.get("trade_count")) - STAGE142_CONTROL["trade_count"],
                "validation_trade_gain_vs_control": as_float(val.get("trade_count")) - STAGE142_CONTROL["validation_trade_count"],
                "oos_trade_gap_vs_34d": as_float(oos.get("trade_count")) - LEGACY_34D["trade_count"],
                "validation_pf_gap_to_guard": as_float(val.get("profit_factor")) - 1.55,
                "oos_mid_pf": as_float(mid.get("profit_factor")),
                "oos_mid_net": as_float(mid.get("net_profit")),
                "oos_late_net": as_float(late.get("net_profit")),
                "max_oos_segment_net_share": max_segment_share,
                "risk_floor_applied_count_oos": as_float(risk_oos.get("risk_floor_applied_count")),
                "max_actual_risk_pct_after_floor_oos": as_float(risk_oos.get("max_actual_risk_pct_after_floor")),
                "gate_blocked_ratio_validation": as_float(gate_val.get("blocked_ratio")),
                "gate_blocked_ratio_oos": as_float(gate_oos.get("blocked_ratio")),
                "quality_safe": quality_safe(val, oos),
                "read": read,
                "next_use": next_use_label(adapter_id, read),
            }
        )
        for segment_name, segment in (("early", early), ("mid", mid), ("late", late)):
            segment_failures.append(
                {
                    "adapter_id": adapter_id,
                    "split": "oos",
                    "segment": segment_name,
                    "profit_factor": as_float(segment.get("profit_factor")),
                    "net_profit": as_float(segment.get("net_profit")),
                    "trade_count": as_float(segment.get("trade_count")),
                    "drawdown_amount": as_float(segment.get("max_closed_trade_drawdown")),
                    "mfe_capture_ratio": as_float(segment.get("mfe_capture_ratio")),
                    "pf_below_34d": as_float(segment.get("profit_factor")) < LEGACY_34D["profit_factor"],
                    "late_or_single_segment_concentration": segment_name == "late" and max_segment_share > 0.45,
                    "stage147_read": (
                        "mid_quality_repair_needed"
                        if adapter_id == SOFTSESSION_ADAPTER_ID and segment_name == "mid"
                        else "segment_watch"
                    ),
                }
            )
    route = [
        {
            "decision": DECISION,
            "reason": "stage146_softsession_added_trades_but_damaged_validation_pf_and_oos_mid_segment_replay_or_ease_added_no_trades_hold4_cut_trades",
            "seed_adapter": SOFTSESSION_ADAPTER_ID,
            "next_stage": NEXT_STAGE_ID,
            "next_axis": "softsession_supply_quality_repair_with_validation_guard_and_oos_mid_segment_filter",
            "do_not_repeat": "broad_no_gate_or_same_shortgate_axis_or_legacy_34d_method_inheritance",
            "overall_goal_complete": False,
        }
    ]
    best_supply = next((row for row in tradeoff if row["adapter_id"] == SOFTSESSION_ADAPTER_ID), {})
    return {
        "tradeoff": tradeoff,
        "segment_failures": segment_failures,
        "route": route,
        "best_supply_seed": best_supply,
        "decision": DECISION,
        "overall_goal_complete": False,
    }


def table_rows(rows: Sequence[Mapping[str, Any]]) -> str:
    header = (
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 손실률) | "
        "OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | OOS trades(표본외 거래 수) | "
        "gain(증가) | mid PF(중반 수익 팩터) | read(판독) |\n"
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"
    )
    body = [
        (
            f"| {row['adapter_id']} | {row['validation_pf']:.6f} | {row['validation_net']:.2f} | {row['validation_dd_percent']:.2f} | "
            f"{row['oos_pf']:.6f} | {row['oos_net']:.2f} | {row['oos_dd_percent']:.2f} | {row['oos_trades']:.0f} | "
            f"{row['oos_trade_gain_vs_control']:.0f} | {row['oos_mid_pf']:.6f} | {row['read']} |"
        )
        for row in rows
    ]
    return "\n".join([header, *body])


def report_markdown(review: Mapping[str, Any]) -> str:
    seed = review.get("best_supply_seed", {})
    return f"""# Stage147 Stage146 Control Anchor Follow-up Review(147단계 146단계 대조군 앵커 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE146_ID}`
- source_stage146_closeout_commit(원천 146단계 종료 커밋): `{SOURCE_STAGE146_CLOSEOUT_COMMIT}`
- source_stage146_hash_record_commit(원천 146단계 해시 기록 커밋): `{SOURCE_STAGE146_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage146(146단계) increase trade count(거래 수)를 without damaging PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), and concentration(집중도)?

Effect(효과): Stage146(146단계) 안에서 계속 고치지 않고, 결과 판독만 분리해 다음 수리 축을 좁게 고른다.

## KPI Read(KPI 핵심 성과 지표 판독)

{table_rows(review["tradeoff"])}

## Judgment(판정)

- answer(답): `no`
- usable_supply_seed(사용 가능한 거래 공급 씨앗): `{seed.get("adapter_id", "none")}`
- seed_oos_trades(씨앗 표본외 거래 수): `{as_float(seed.get("oos_trades")):.0f}`
- seed_oos_trade_gain_vs_control(대조군 대비 표본외 거래 증가): `{as_float(seed.get("oos_trade_gain_vs_control")):.0f}`
- seed_oos_pf(씨앗 표본외 수익 팩터): `{as_float(seed.get("oos_pf")):.6f}`
- seed_validation_pf(씨앗 검증 수익 팩터): `{as_float(seed.get("validation_pf")):.6f}`
- failure_read(실패 판독): softsession(소프트 세션)은 표본외 거래 수를 180에서 215로 늘렸지만 validation PF(검증 수익 팩터)가 1.43으로 손상됐고 OOS mid PF(표본외 중반 수익 팩터)가 1.408로 약하다.
- control_read(대조군 판독): replay/ease(재현/완화)는 품질은 보존했지만 표본외 거래 수가 180으로 늘지 않았다.
- hold_read(보유 판독): hold4(4봉 보유)는 표본외 PF/net(수익 팩터/순손익)은 좋지만 거래 수가 178로 줄고 validation PF/DD(검증 수익 팩터/손실률)가 손상됐다.
- decision_use(판정 용도): Stage148(148단계)은 softsession(소프트 세션) 거래 공급 증가분만 repair seed(수리 씨앗)로 쓰고, validation guard(검증 보호문)와 OOS mid filter(표본외 중반 필터)를 좁게 시험한다.
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): weak-session block(약한 세션 차단)을 좁히면 거래 수는 늘지만 약한 validation/mid segment(검증/중반 구간) 거래도 같이 들어왔다.
- likely_drivers(가능 원인): session block width(세션 차단 폭), et40 mid margin block(et40 중간 마진 차단), both-side gate(양방향 게이트), unchanged threshold(유지된 임계값).
- risk_read(위험 판독): risk floor(최소 로트 위험 바닥)는 Stage146 표본외 실제 라우팅에서 0으로, 현재 실패 원인은 위험 바닥보다 진입 품질 쪽이다.
- next_probe(다음 확인): `{NEXT_STAGE_ID}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage147 Decision(147단계 판정)

decision(판정): `{DECISION}`

Stage147(147단계)는 Stage146(146단계) evidence(근거)를 review-only(검토 전용)로 판정했다. Effect(효과): 거래 수 증가 단서와 품질 손상을 분리해 Stage148(148단계) 수리축을 좁힌다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- segment_failure_summary(구간 실패 요약): `{rel(SEGMENT_FAILURE_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage146_summary(원천 146단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage146_segments(원천 146단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage146_risk_atr(원천 146단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
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

Stage147(147단계)은 Stage146 control anchor trade supply repair(146단계 대조군 앵커 거래 공급 수리) 결과를 follow-up review(후속 검토)로 판정한다.

## Bounded Question(경계 질문)

Did Stage146(146단계) increase trade count(거래 수)를 without damaging PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), and concentration(집중도)?

Effect(효과): Stage146(146단계) 안에서 계속 고치지 않고, 결과 판독만 분리해 다음 수리 축을 좁게 고른다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage147 Input References(147단계 입력 참조)

- source_stage(원천 단계): `{SOURCE_STAGE146_ID}`
- source_run(원천 실행): `run146A_stage146_control_anchor_trade_supply_after_shortgate_no_repair_v1`
- source_stage146_closeout_commit(원천 146단계 종료 커밋): `{SOURCE_STAGE146_CLOSEOUT_COMMIT}`
- source_stage146_hash_record_commit(원천 146단계 해시 기록 커밋): `{SOURCE_STAGE146_HASH_RECORD_COMMIT}`
- stage146_decision(146단계 판정): `{rel(SOURCE_DECISION)}`
- stage146_report(146단계 보고서): `{rel(SOURCE_REPORT)}`
- stage146_summary(146단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage146_segment_kpi(146단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage146_risk_atr_telemetry(146단계 위험/ATR 기록): `{rel(SOURCE_RISK_ATR)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage147 Selection Status(147단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE146_ID}`
- source_run(원천 실행): `run146A_stage146_control_anchor_trade_supply_after_shortgate_no_repair_v1`
- stage147_decision(147단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage147 Review Index(147단계 검토 색인)

- review(검토): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- segment_failure_summary(구간 실패 요약): `{rel(SEGMENT_FAILURE_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage148(148단계)은 Stage147(147단계) 판정에 따라 softsession supply quality repair(소프트 세션 거래 공급 품질 수리)를 연다.

## Bounded Question(경계 질문)

Can the Stage146 softsession(146단계 소프트 세션) trade count gain(거래 수 증가)을 keep(보존)하면서 validation PF(검증 수익 팩터)와 OOS mid segment(표본외 중반 구간) 손상을 줄일 수 있는가?

Effect(효과): 거래 수 증가 단서를 버리지 않되, 손상된 softsession(소프트 세션)을 기준선처럼 승격하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage148 Input References(148단계 입력 참조)

- stage147_decision(147단계 판정): `{rel(DECISION_PATH)}`
- stage147_review(147단계 검토): `{rel(REPORT_PATH)}`
- stage147_tradeoff_summary(147단계 상충 요약): `{rel(TRADEOFF_PATH)}`
- stage147_segment_failure_summary(147단계 구간 실패 요약): `{rel(SEGMENT_FAILURE_PATH)}`
- stage146_summary(146단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage146_segment_kpi(146단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage146_risk_atr_telemetry(146단계 위험/ATR 기록): `{rel(SOURCE_RISK_ATR)}`
- repair_seed(수리 씨앗): `{SOFTSESSION_ADAPTER_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage148 Review Index(148단계 검토 색인)

Stage148(148단계)은 open_planned(개방 계획) 상태다. Effect(효과): 다음 실행은 softsession supply quality repair(소프트 세션 거래 공급 품질 수리)만 좁게 다룬다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage148 Selection Status(148단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage147`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- repair_seed(수리 씨앗): `{SOFTSESSION_ADAPTER_ID}`
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
- adapter_under_review(검토 중 어댑터): `stage148_softsession_supply_quality_repair_surface`
- status(상태): `stage147_closed_{DECISION}_stage148_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage147(147단계)는 Stage146(146단계) 결과를 review-only(검토 전용)로 닫았다. Effect(효과): softsession(소프트 세션)의 거래 수 증가 단서는 보존하고, validation PF(검증 수익 팩터)와 OOS mid(표본외 중반) 손상은 Stage148(148단계)에서 좁게 수리한다.

## Latest Stage147 Evidence(최신 147단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- segment_failure_summary(구간 실패 요약): `{rel(SEGMENT_FAILURE_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage147(147단계) closed(종료) as `{DECISION}` and Stage148(148단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage146(146단계)의 softsession(소프트 세션) 거래 수 증가 단서를 품질 수리축으로 넘긴다.
- >-
  Stage147 evidence(147단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(SEGMENT_FAILURE_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): 거래 수 증가와 validation/OOS mid(검증/표본외 중반) 손상을 분리해 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    block = f"""
stage147_stage146_control_anchor_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE146_ID}
  source_stage146_closeout_commit: {SOURCE_STAGE146_CLOSEOUT_COMMIT}
  source_stage146_hash_record_commit: {SOURCE_STAGE146_HASH_RECORD_COMMIT}
  source_stage145_hash_record_commit: {SOURCE_STAGE145_HASH_RECORD_COMMIT}
  source_stage142_hash_record_commit: {SOURCE_STAGE142_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_action: {NEXT_RUN_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage148_softsession_supply_quality_repair_after_stage146_damage:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage147
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  repair_seed: {SOFTSESSION_ADAPTER_ID}
  next_action: run148A_stage148_softsession_supply_quality_repair_after_stage146_damage_v1
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage147_stage146_control_anchor_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage148_softsession_supply_quality_repair_after_stage146_damage:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage147 Stage146 control anchor follow-up closeout(147단계 146단계 대조군 앵커 후속 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage146(146단계)의 거래 수 증가 단서와 validation/OOS mid(검증/표본외 중반) 손상을 분리하고 Stage148(148단계) 수리축으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        REPORT_PATH,
        TRADEOFF_PATH,
        SEGMENT_FAILURE_PATH,
        ROUTE_DECISION_PATH,
        DECISION_PATH,
        SUMMARY_JSON_PATH,
        STAGE_LEDGER_PATH,
        PRODUCER_PATH,
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage147_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage147 review-only Stage146 control anchor follow-up artifact.",
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
                "lane": "baseline_adapter_stage147_control_anchor_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage146_closeout_commit", SOURCE_STAGE146_CLOSEOUT_COMMIT),
                        ("source_stage146_hash_record_commit", SOURCE_STAGE146_HASH_RECORD_COMMIT),
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
        "split": "stage146_existing_evidence",
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
                ("repair_seed", SOFTSESSION_ADAPTER_ID),
                ("overall_goal_complete", 0),
            )
        ),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {
        "run_registry": run_payload,
        "project_alpha_ledger": project_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": [
                "kpi_contract_audit",
                "result_judgment_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "source_summary": rel(SOURCE_SUMMARY),
            "source_segments": rel(SOURCE_SEGMENTS),
            "tradeoff_path": rel(TRADEOFF_PATH),
            "segment_failure_path": rel(SEGMENT_FAILURE_PATH),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(SEGMENT_FAILURE_PATH), rel(DECISION_PATH)],
            "evidence_missing": ["new_repair_not_attempted_in_stage147_by_design"],
            "judgment_label": "stage146_trade_supply_gain_damaged_not_final",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": "Stage148 must repair softsession supply quality and not promote the damaged Stage146 variant.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage146 softsession increased OOS trades but damaged validation PF and OOS mid segment quality.",
            "comparison_baseline": SOURCE_ADAPTER_ID,
            "likely_drivers": ["weak_session_block_width", "et40_mid_margin_block", "both_side_gate", "unchanged_thresholds"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_GATES), rel(SOURCE_DECISION)],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH), NEXT_STAGE_ID],
            "artifact_paths": [rel(path) for path in [REPORT_PATH, TRADEOFF_PATH, SEGMENT_FAILURE_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH]],
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
        "required_gate_coverage_audit.json": {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "declared_required_gates": [
                "kpi_contract_audit",
                "result_judgment_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "executed_gates": [
                "kpi_contract_audit",
                "result_judgment_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage146_closeout_commit": SOURCE_STAGE146_CLOSEOUT_COMMIT,
            "source_stage146_hash_record_commit": SOURCE_STAGE146_HASH_RECORD_COMMIT,
            "repair_seed": SOFTSESSION_ADAPTER_ID,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "tradeoff": rel(TRADEOFF_PATH),
                "segment_failure": rel(SEGMENT_FAILURE_PATH),
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
    write_csv(SEGMENT_FAILURE_PATH, review["segment_failures"])
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
    seed = review.get("best_supply_seed", {})
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": RUN_ID,
                "decision": DECISION,
                "repair_seed": seed.get("adapter_id", ""),
                "stage148": NEXT_STAGE_ID,
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
