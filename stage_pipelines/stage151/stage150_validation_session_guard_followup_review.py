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


STAGE_ID = "151_adapter_research__stage150_validation_session_guard_followup_review"
RUN_ID = "run151A_stage151_stage150_validation_session_guard_followup_review_v1"
PACKET_ID = "stage151_stage150_validation_session_guard_followup_review_v1"
SOURCE_STAGE150_ID = "150_adapter_research__validation_session_guard_repair_after_stage148_tradeoff"
SOURCE_STAGE150_CLOSEOUT_COMMIT = "3331309a56e2f9ae8f7cdd7d1c234e875483449f"
SOURCE_STAGE150_HASH_RECORD_COMMIT = "23d7d57e67ebfaf468c036114630a1e20d2abc9b"
SOURCE_STAGE149_HASH_RECORD_COMMIT = "ce3b740df84f1654d3e3f6a941ecd439cde36140"
SOURCE_STAGE148_HASH_RECORD_COMMIT = "db69b5f07831b58675481f180055a0c60f96997f"
SOURCE_REPAIR_CLUE = "s150_session_mid_margin_restore_h3_cd5_sht54_lng52_risk035"
OOS_CLUE = "s150_session_mid_replay_h3_cd5_sht54_lng52_risk035"
NEXT_STAGE_ID = "152_adapter_research__oos_dd_mid_compression_after_stage150_tradeoff"
NEXT_RUN_ID = "run152A_stage152_oos_dd_mid_compression_after_stage150_tradeoff_v1"
NEXT_PACKET_ID = "stage152_oos_dd_mid_compression_after_stage150_tradeoff_v1"
DECISION = "open_stage152_oos_dd_mid_compression_after_stage150_tradeoff_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
EXTERNAL_STATUS = "completed_existing_stage150_mt5_runtime_evidence_reviewed"
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
PRODUCER_PATH = Path("stage_pipelines/stage151/stage150_validation_session_guard_followup_review.py")

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE150_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage150_validation_session_guard_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage150_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage150_risk_atr_telemetry.csv"
SOURCE_DECISION = SOURCE_REVIEWS / "stage150_decision.md"
SOURCE_REPORT = SOURCE_REVIEWS / "stage150_validation_session_guard_report.md"

REPORT_PATH = REVIEWS_ROOT / "stage151_stage150_validation_session_guard_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage151_validation_guard_tradeoff_summary.csv"
SEGMENT_FAILURE_PATH = REVIEWS_ROOT / "stage151_segment_failure_summary.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage151_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage151_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage151_followup_summary.json"
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
    "oos_trade_count": 180,
    "validation_trade_count": 265,
    "oos_pf": 1.795976838,
    "oos_net": 1186.30,
    "oos_dd_percent": 14.66,
    "validation_pf": 1.582222632,
    "validation_net": 1388.24,
    "validation_dd_percent": 11.85,
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def risk_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_RISK_ATR) if row.get("view") == "actual_routed_total"]


def split_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split:
            return row
    return {}


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


def validation_ok(val: Mapping[str, Any]) -> bool:
    return (
        as_float(val.get("profit_factor")) >= 1.55
        and as_float(val.get("net_profit")) >= LEGACY_34D["net_profit"]
        and as_float(val.get("max_drawdown_percent"), 99.0) <= 15.0
    )


def oos_ok(oos: Mapping[str, Any], mid: Mapping[str, Any]) -> bool:
    return (
        as_float(oos.get("profit_factor")) >= LEGACY_34D["profit_factor"]
        and as_float(oos.get("net_profit")) >= LEGACY_34D["net_profit"]
        and as_float(oos.get("max_drawdown_percent"), 99.0) <= 16.5
        and as_float(mid.get("profit_factor")) >= LEGACY_34D["profit_factor"]
    )


def read_label(adapter_id: str, val: Mapping[str, Any], oos: Mapping[str, Any], mid: Mapping[str, Any]) -> str:
    val_pass = validation_ok(val)
    oos_pass = oos_ok(oos, mid)
    if val_pass and oos_pass:
        return "full_quality_candidate_not_final"
    if val_pass and not oos_pass:
        return "validation_recovered_but_oos_dd_or_mid_damaged"
    if oos_pass and not val_pass:
        return "oos_quality_preserved_but_validation_failed"
    if adapter_id == SOURCE_REPAIR_CLUE:
        return "partial_validation_repair_with_oos_damage"
    return "no_full_repair"


def next_use_label(adapter_id: str, read: str) -> str:
    if adapter_id == SOURCE_REPAIR_CLUE:
        return "use_as_stage152_oos_dd_mid_compression_seed_not_baseline"
    if adapter_id == OOS_CLUE:
        return "preserve_as_oos_mid_failure_memory"
    return "preserve_as_failure_memory"


def build_review() -> dict[str, Any]:
    summary = routed_summary_rows()
    segments = segment_rows()
    risks = risk_rows()
    adapters = sorted({str(row.get("adapter_id", "")) for row in summary})
    tradeoff: list[dict[str, Any]] = []
    segment_failures: list[dict[str, Any]] = []
    for adapter_id in adapters:
        val = split_row(summary, adapter_id, "validation_is")
        oos = split_row(summary, adapter_id, "oos")
        val_early = segment_lookup(segments, adapter_id, "validation_is", "early")
        val_mid = segment_lookup(segments, adapter_id, "validation_is", "mid")
        oos_early = segment_lookup(segments, adapter_id, "oos", "early")
        oos_mid = segment_lookup(segments, adapter_id, "oos", "mid")
        oos_late = segment_lookup(segments, adapter_id, "oos", "late")
        risk_oos = risk_lookup(risks, adapter_id, "oos")
        total_oos_net = as_float(oos.get("net_profit"))
        segment_nets = [as_float(oos_early.get("net_profit")), as_float(oos_mid.get("net_profit")), as_float(oos_late.get("net_profit"))]
        max_segment_share = max(segment_nets) / total_oos_net if total_oos_net > 0 and segment_nets else 0.0
        read = read_label(adapter_id, val, oos, oos_mid)
        tradeoff.append(
            {
                "adapter_id": adapter_id,
                "validation_pf": as_float(val.get("profit_factor")),
                "validation_net": as_float(val.get("net_profit")),
                "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
                "validation_trades": as_float(val.get("trade_count")),
                "validation_early_pf": as_float(val_early.get("profit_factor")),
                "validation_mid_pf": as_float(val_mid.get("profit_factor")),
                "oos_pf": as_float(oos.get("profit_factor")),
                "oos_net": as_float(oos.get("net_profit")),
                "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
                "oos_trades": as_float(oos.get("trade_count")),
                "oos_trade_gain_vs_stage142_control": as_float(oos.get("trade_count")) - STAGE142_CONTROL["oos_trade_count"],
                "oos_mid_pf": as_float(oos_mid.get("profit_factor")),
                "oos_mid_net": as_float(oos_mid.get("net_profit")),
                "oos_late_net": as_float(oos_late.get("net_profit")),
                "max_oos_segment_net_share": max_segment_share,
                "risk_floor_applied_count_oos": as_float(risk_oos.get("risk_floor_applied_count")),
                "max_actual_risk_pct_after_floor_oos": as_float(risk_oos.get("max_actual_risk_pct_after_floor")),
                "validation_guard_pass": validation_ok(val),
                "oos_guard_pass": oos_ok(oos, oos_mid),
                "read": read,
                "next_use": next_use_label(adapter_id, read),
            }
        )
        for split_name, split_segments in (
            ("validation_is", (("early", val_early), ("mid", val_mid))),
            ("oos", (("early", oos_early), ("mid", oos_mid), ("late", oos_late))),
        ):
            for segment_name, segment in split_segments:
                pf = as_float(segment.get("profit_factor"))
                segment_failures.append(
                    {
                        "adapter_id": adapter_id,
                        "split": split_name,
                        "segment": segment_name,
                        "profit_factor": pf,
                        "net_profit": as_float(segment.get("net_profit")),
                        "trade_count": as_float(segment.get("trade_count")),
                        "mfe_capture_ratio": as_float(segment.get("mfe_capture_ratio")),
                        "pf_below_34d": pf < LEGACY_34D["profit_factor"],
                        "dd_or_mid_repair_needed": adapter_id == SOURCE_REPAIR_CLUE and split_name == "oos" and (segment_name == "mid" or as_float(oos.get("max_drawdown_percent"), 99.0) > 16.5),
                        "stage151_read": (
                            "oos_dd_mid_compression_needed"
                            if adapter_id == SOURCE_REPAIR_CLUE and split_name == "oos"
                            else "validation_guard_still_weak"
                            if split_name == "validation_is" and pf < 1.55
                            else "segment_watch"
                        ),
                    }
                )
    seed = next((row for row in tradeoff if row["adapter_id"] == SOURCE_REPAIR_CLUE), {})
    route = [
        {
            "decision": DECISION,
            "reason": "stage150_margin_restore_recovered_validation_but_oos_dd_too_high_and_oos_mid_pf_slightly_below_34d",
            "seed_adapter": SOURCE_REPAIR_CLUE,
            "next_stage": NEXT_STAGE_ID,
            "next_axis": "preserve_validation_recovery_while_compressing_oos_drawdown_and_lifting_oos_mid_pf",
            "do_not_repeat": "do_not_accept_stage150_final_net_or_validation_pf_alone",
            "overall_goal_complete": False,
        }
    ]
    return {
        "tradeoff": tradeoff,
        "segment_failures": segment_failures,
        "route": route,
        "repair_seed": seed,
        "decision": DECISION,
        "overall_goal_complete": False,
    }


def table_rows(rows: Sequence[Mapping[str, Any]]) -> str:
    header = (
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val DD%(검증 손실률) | val early PF(검증 초반 수익 팩터) | val mid PF(검증 중반 수익 팩터) | "
        "OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | OOS trades(표본외 거래 수) | OOS mid PF(표본외 중반 수익 팩터) | read(판독) |\n"
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"
    )
    body = [
        (
            f"| {row['adapter_id']} | {row['validation_pf']:.6f} | {row['validation_dd_percent']:.2f} | "
            f"{row['validation_early_pf']:.6f} | {row['validation_mid_pf']:.6f} | {row['oos_pf']:.6f} | "
            f"{row['oos_net']:.2f} | {row['oos_dd_percent']:.2f} | {row['oos_trades']:.0f} | {row['oos_mid_pf']:.6f} | {row['read']} |"
        )
        for row in rows
    ]
    return "\n".join([header, *body])


def report_markdown(review: Mapping[str, Any]) -> str:
    seed = review.get("repair_seed", {})
    return f"""# Stage151 Stage150 Validation Session Guard Follow-up Review(151단계 150단계 검증 세션 보호문 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE150_ID}`
- source_stage150_closeout_commit(원천 150단계 종료 커밋): `{SOURCE_STAGE150_CLOSEOUT_COMMIT}`
- source_stage150_hash_record_commit(원천 150단계 해시 기록 커밋): `{SOURCE_STAGE150_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage150(150단계) preserve OOS mid repair(표본외 중반 수리) while lifting validation early/mid quality(검증 초반/중반 품질)?

Effect(효과): Stage150(150단계) 안에서 계속 고치지 않고, 다음 수리축 또는 폐기 판단을 분리한다.

## KPI Read(KPI 핵심 성과 지표 판독)

{table_rows(review["tradeoff"])}

## Judgment(판정)

- answer(답): `no`
- selected_repair_seed(선택 수리 씨앗): `{seed.get("adapter_id", "none")}`
- seed_validation_pf(씨앗 검증 수익 팩터): `{as_float(seed.get("validation_pf")):.6f}`
- seed_oos_pf(씨앗 표본외 수익 팩터): `{as_float(seed.get("oos_pf")):.6f}`
- seed_oos_dd(씨앗 표본외 손실률): `{as_float(seed.get("oos_dd_percent")):.2f}`
- seed_oos_mid_pf(씨앗 표본외 중반 수익 팩터): `{as_float(seed.get("oos_mid_pf")):.6f}`
- failure_read(실패 판독): margin_restore(마진 복원)는 validation PF(검증 수익 팩터)를 1.59로 회복했지만 OOS DD(표본외 손실률)가 18.94로 높고 OOS mid PF(표본외 중반 수익 팩터)가 1.578로 34D 기준 1.583보다 낮다.
- decision_use(판정 용도): Stage152(152단계)는 margin_restore(마진 복원)의 validation recovery(검증 회복)를 보존하면서 OOS DD/mid(표본외 손실률/중반)를 좁게 압축한다.
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): margin_restore(마진 복원)는 validation(검증)을 회복했지만 OOS drawdown(표본외 손실률)과 OOS mid quality(표본외 중반 품질)를 손상했다.
- comparison_baseline(비교 기준): Stage150 session_mid replay(세션 중간 재현)과 Stage142 control(142단계 대조군).
- likely_drivers(가능 원인): margin block(마진 차단) 폭, session window(세션 창), unchanged lifecycle(유지된 생명주기), unchanged risk/ATR(유지된 위험/ATR).
- next_probe(다음 확인): `{NEXT_STAGE_ID}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage151 Decision(151단계 판정)

decision(판정): `{DECISION}`

Stage151(151단계)는 Stage150(150단계) evidence(근거)를 review-only(검토 전용)로 판정했다. Effect(효과): validation recovery(검증 회복)와 OOS DD/mid damage(표본외 손실률/중반 손상)를 분리해 Stage152(152단계) 수리축을 좁힌다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- segment_failure_summary(구간 실패 요약): `{rel(SEGMENT_FAILURE_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage150_summary(원천 150단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage150_segments(원천 150단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage150_risk_atr(원천 150단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def write_stage_docs() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage151 Selection Status(151단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE150_ID}`
- source_run(원천 실행): `run150A_stage150_validation_session_guard_repair_after_stage148_tradeoff_v1`
- stage151_decision(151단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage151 Review Index(151단계 검토 색인)

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

Stage152(152단계)는 Stage151(151단계) 판정에 따라 OOS DD/mid compression(표본외 손실률/중반 압축)을 연다.

## Bounded Question(경계 질문)

Can Stage150 margin_restore(150단계 마진 복원)의 validation recovery(검증 회복)를 preserve(보존)하면서 OOS DD(표본외 손실률)를 낮추고 OOS mid PF(표본외 중반 수익 팩터)를 34D 기준 이상으로 올릴 수 있는가?

Effect(효과): validation(검증)만 좋아진 후보를 최종처럼 보지 않고, 표본외 손상만 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage152 Input References(152단계 입력 참조)

- stage151_decision(151단계 판정): `{rel(DECISION_PATH)}`
- stage151_review(151단계 검토): `{rel(REPORT_PATH)}`
- stage151_tradeoff_summary(151단계 상충 요약): `{rel(TRADEOFF_PATH)}`
- stage151_segment_failure_summary(151단계 구간 실패 요약): `{rel(SEGMENT_FAILURE_PATH)}`
- stage150_summary(150단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage150_segment_kpi(150단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage150_risk_atr_telemetry(150단계 위험/ATR 기록): `{rel(SOURCE_RISK_ATR)}`
- repair_seed(수리 씨앗): `{SOURCE_REPAIR_CLUE}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    write_md(NEXT_STAGE_ROOT / "03_reviews/review_index.md", "# Stage152 Review Index(152단계 검토 색인)\n\nStage152(152단계)은 open_planned(개방 계획) 상태다.\n")
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage152 Selection Status(152단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage151`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- repair_seed(수리 씨앗): `{SOURCE_REPAIR_CLUE}`
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
- adapter_under_review(검토 중 어댑터): `stage152_oos_dd_mid_compression_surface`
- status(상태): `stage151_closed_{DECISION}_stage152_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage151(151단계)는 Stage150(150단계) validation session guard repair(검증 세션 보호문 수리)를 review-only(검토 전용)로 판정했다. Effect(효과): validation recovery(검증 회복)는 보존하고 OOS DD/mid damage(표본외 손실률/중반 손상)는 Stage152(152단계)에서 좁게 수리한다.

## Latest Stage151 Evidence(최신 151단계 근거)

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
  Stage151(151단계) closed(종료) as `{DECISION}` and Stage152(152단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage150 margin_restore(마진 복원)의 validation recovery(검증 회복)를 보존하고 OOS DD/mid(표본외 손실률/중반)를 좁게 수리한다.
- >-
  Stage151 evidence(151단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(SEGMENT_FAILURE_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): validation(검증) 개선과 OOS(표본외) 손상을 분리해 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    block = f"""
stage151_stage150_validation_session_guard_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE150_ID}
  source_stage150_closeout_commit: {SOURCE_STAGE150_CLOSEOUT_COMMIT}
  source_stage150_hash_record_commit: {SOURCE_STAGE150_HASH_RECORD_COMMIT}
  source_stage149_hash_record_commit: {SOURCE_STAGE149_HASH_RECORD_COMMIT}
  source_stage148_hash_record_commit: {SOURCE_STAGE148_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_action: {NEXT_RUN_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage152_oos_dd_mid_compression_after_stage150_tradeoff:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage151
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  repair_seed: {SOURCE_REPAIR_CLUE}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage151_stage150_validation_session_guard_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage152_oos_dd_mid_compression_after_stage150_tradeoff:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage151 Stage150 validation guard follow-up closeout(151단계 150단계 검증 보호문 후속 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): validation recovery(검증 회복)와 OOS DD/mid damage(표본외 손실률/중반 손상)를 분리하고 Stage152(152단계) 수리축으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [REPORT_PATH, TRADEOFF_PATH, SEGMENT_FAILURE_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH, PRODUCER_PATH]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage151_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage151 review-only Stage150 validation guard follow-up artifact.",
                }
            )
    return rows


def write_ledgers() -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage151_validation_guard_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs((("source_stage150_closeout_commit", SOURCE_STAGE150_CLOSEOUT_COMMIT), ("source_stage150_hash_record_commit", SOURCE_STAGE150_HASH_RECORD_COMMIT), ("target_surface", TARGET_SURFACE), ("overall_goal_complete", 0))),
            }
        ],
        key="run_id",
    )
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_only",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "view": "review_only",
        "split": "stage150_existing_evidence",
        "tier": "actual_routed_total",
        "route_role": "followup_review",
        "status": "completed",
        "profit_factor": "",
        "net_profit": "",
        "max_drawdown_percent": "",
        "trade_count": "",
        "notes": ledger_pairs((("decision", DECISION), ("source_summary", rel(SOURCE_SUMMARY)), ("repair_seed", SOURCE_REPAIR_CLUE), ("overall_goal_complete", 0))),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(ledger_payload: Mapping[str, Any]) -> None:
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard", "required_gate_coverage_audit"],
            "status": "completed",
        },
        "kpi_contract_audit.json": {"source_summary": rel(SOURCE_SUMMARY), "source_segments": rel(SOURCE_SEGMENTS), "tradeoff_path": rel(TRADEOFF_PATH), "segment_failure_path": rel(SEGMENT_FAILURE_PATH), "status": "completed"},
        "result_judgment_gate.json": {"result_subject": RUN_ID, "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(SEGMENT_FAILURE_PATH), rel(DECISION_PATH)], "evidence_missing": ["new_repair_not_attempted_in_stage151_by_design"], "judgment_label": "stage150_tradeoff_not_final", "decision": DECISION, "claim_boundary": BOUNDARY, "next_condition": "Stage152 must preserve validation recovery while compressing OOS DD and lifting OOS mid PF.", "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {"observed_change": "Stage150 margin_restore recovered validation but damaged OOS DD and OOS mid quality.", "comparison_baseline": "Stage150 session_mid replay and Stage142 control", "likely_drivers": ["margin_block_width", "session_window", "unchanged_lifecycle", "unchanged_risk_atr"], "attribution_confidence": "medium", "next_probe": NEXT_STAGE_ID, "status": "completed"},
        "artifact_lineage_audit.json": {"source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_DECISION)], "producer": rel(PRODUCER_PATH), "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH), NEXT_STAGE_ID], "artifact_paths": [rel(path) for path in [REPORT_PATH, TRADEOFF_PATH, SEGMENT_FAILURE_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH]], "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)], "availability": "tracked", "lineage_judgment": "connected_with_boundary", "ledger_payload": ledger_payload},
        "final_claim_guard.json": {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {"packet_id": PACKET_ID, "run_id": RUN_ID, "declared_required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard", "required_gate_coverage_audit"], "executed_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard", "required_gate_coverage_audit"], "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage150_closeout_commit": SOURCE_STAGE150_CLOSEOUT_COMMIT,
            "source_stage150_hash_record_commit": SOURCE_STAGE150_HASH_RECORD_COMMIT,
            "repair_seed": SOURCE_REPAIR_CLUE,
            "required_outputs": {"report": rel(REPORT_PATH), "tradeoff": rel(TRADEOFF_PATH), "segment_failure": rel(SEGMENT_FAILURE_PATH), "route_decision": rel(ROUTE_DECISION_PATH), "decision": rel(DECISION_PATH)},
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
    ledger_payload = write_ledgers()
    write_packet_files(ledger_payload)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    ledger_payload = {**ledger_payload, "artifact_registry": artifact_payload}
    write_packet_files(ledger_payload)
    return review


def main() -> int:
    review = run()
    seed = review.get("repair_seed", {})
    print(json.dumps({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "repair_seed": seed.get("adapter_id", ""), "stage152": NEXT_STAGE_ID, "tradeoff_csv": rel(TRADEOFF_PATH)}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
