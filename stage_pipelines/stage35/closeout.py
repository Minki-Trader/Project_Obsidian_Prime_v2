from __future__ import annotations

import argparse
import json
import re
from typing import Any, Mapping, Sequence

from stage_pipelines.stage35 import atlas_config as base
from stage_pipelines.stage35 import common


RUN_ID = "stage35_context_map_closeout_v1"
PACKET_ID = "stage35_context_map_closeout_v1"
REPORT_PATH = base.STAGE_ROOT / "03_reviews" / "stage35_closeout_packet.md"
DECISION_PATH = common.ROOT / "docs" / "decisions" / "2026-05-09_stage35_closeout_no_stage36.md"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
BOUNDARY = "stage35_closeout_no_stage36_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT = "closed_inconclusive_stage35_context_map_exhausted"


SOURCE_PACKETS = (
    "stage35_run29A_unsupervised_market_state_atlas_mt5_probe_v1",
    "stage35_run29B_worthwhile_deep_sweep_mt5_probe_v1",
    "stage35_run29C_candidate_four_deep_dive_mt5_probe_v1",
)


def _load_packet(packet_id: str) -> dict[str, Any]:
    return common.read_json(common.ROOT / "docs" / "agent_control" / "packets" / packet_id / "aggregate_summary.json")


def _sum_kpi(summaries: Sequence[Mapping[str, Any]], key: str) -> int:
    total = 0
    for summary in summaries:
        kpi = summary.get("kpi_management", {})
        if isinstance(kpi, Mapping):
            total += int(kpi.get(key) or 0)
    return total


def _candidate_lines(run29c: Mapping[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in run29c.get("candidate_read", []):
        out.append(
            {
                "variant_id": row.get("variant_id"),
                "read": row.get("read"),
                "validation_h12_net": row.get("validation_h12_net"),
                "validation_h12_pf": row.get("validation_h12_pf"),
                "oos_h12_net": row.get("oos_h12_net"),
                "oos_h12_pf": row.get("oos_h12_pf"),
                "oos_no_oct_net": row.get("oos_no_oct_net"),
                "oos_no_oct_pf": row.get("oos_no_oct_pf"),
                "oos_second_half_net": row.get("oos_second_half_net"),
                "oos_second_half_pf": row.get("oos_second_half_pf"),
            }
        )
    return out


def build_summary() -> dict[str, Any]:
    run29a, run29b, run29c = [_load_packet(packet_id) for packet_id in SOURCE_PACKETS]
    completed = all(summary.get("external_verification_status") == "completed" for summary in (run29a, run29b, run29c))
    attempts = sum(int(summary.get("mt5_attempt_count") or 0) for summary in (run29a, run29b, run29c))
    records = sum(int(summary.get("mt5_kpi_record_count") or 0) for summary in (run29a, run29b, run29c))
    candidates = _candidate_lines(run29c)
    fragile = [row for row in candidates if row["read"] == "base_positive_only"]
    failed = [row for row in candidates if row["read"] == "failed_base_recheck"]
    return {
        "packet_id": PACKET_ID,
        "stage_id": base.STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": common.utc_now(),
        "active_branch": common.active_branch(),
        "status": "reviewed_closed_no_stage36_opened",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "source_packets": list(SOURCE_PACKETS),
        "external_verification_status": "completed" if completed else "blocked_or_incomplete_source",
        "mt5_attempt_count": attempts,
        "mt5_kpi_record_count": records,
        "normalized_records": _sum_kpi((run29a, run29b, run29c), "normalized_records"),
        "trade_level_rows": _sum_kpi((run29a, run29b, run29c), "trade_level_rows"),
        "parser_errors": _sum_kpi((run29a, run29b, run29c), "parser_errors"),
        "trade_parser_errors": _sum_kpi((run29a, run29b, run29c), "trade_parser_errors"),
        "candidate_closeout": candidates,
        "preserved_clues": [
            {
                "variant_id": "return_volatility_shape_state2",
                "label": "fragile_seed_only",
                "reason": "base validation/OOS positive, but no-October and OOS second-half fail.",
            },
            {
                "variant_id": "session_cash_open_0_30",
                "label": "weak_context_clue_only",
                "reason": "base validation/OOS barely positive, but no-October and OOS second-half fail.",
            },
        ],
        "negative_memory": [
            {
                "variant_id": row["variant_id"],
                "reason": "failed RUN29C base recheck or drift stress; do not repeat as a Stage35 follow-up without a new hypothesis.",
            }
            for row in failed
        ],
        "further_probe_decision": {
            "decision": "no_more_stage35_probe",
            "why": "No candidate survived base validation/OOS, no-October OOS, and OOS half-window checks together.",
            "effect": "Close Stage35 without opening Stage36 and without creating a baseline or promotion candidate.",
        },
        "performance_attribution": {
            "observed_change": "RUN29B both-positive candidates weakened under RUN29C hold and time stress.",
            "comparison_baseline": "RUN29B base validation/OOS MT5 rows.",
            "likely_drivers": [
                "2025-10 concentration",
                "OOS first-half concentration",
                "hold-length sensitivity",
                "thin trade count for return_volatility_shape_state2 and session_cash_open_0_30",
            ],
            "segment_checks": "hold 6/12/24, OOS without 2025-10, OOS first half, OOS second half.",
            "trade_shape": "trade-level attribution recorded for RUN29A/RUN29B/RUN29C; RUN29C has 4414 trade rows.",
            "alternative_explanations": "row-omission handoff, single-window OOS, broker tester defaults, and non-native state assignment.",
            "attribution_confidence": "medium_for_stage_closeout_low_for_signal_quality",
            "next_probe": "none inside Stage35; only a future explicitly requested native/WFO packet could reopen one preserved clue.",
        },
        "result_judgment": {
            "result_subject": base.STAGE_ID,
            "evidence_available": "RUN29A/RUN29B/RUN29C MT5 reports, normalized KPI, trade attribution, ledgers, and closeout packet.",
            "evidence_missing": "native MT5 state assignment, WFO, Tier B/combined runtime rows, operating parity closure.",
            "judgment_label": "closed_inconclusive",
            "claim_boundary": BOUNDARY,
            "next_condition": "User must explicitly request a new stage or a narrow native/WFO reopening packet.",
            "user_explanation_hook": "Stage35 taught where the weak clues were, but did not leave a robust candidate worth more Stage35 probing.",
        },
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "stage36_opened": False,
        "next_action": "none_stage35_closed_stage36_not_opened",
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority", "live_readiness"],
        "output_paths": {
            "report": common.rel(REPORT_PATH),
            "decision": common.rel(DECISION_PATH),
            "aggregate_summary": common.rel(PACKET_ROOT / "aggregate_summary.json"),
        },
    }


def _candidate_table(summary: Mapping[str, Any]) -> str:
    lines = [
        "| candidate(후보) | read(판독) | base OOS(기본 표본외) | no Oct(10월 제외) | OOS second half(표본외 후반) |",
        "|---|---|---:|---:|---:|",
    ]
    for row in summary["candidate_closeout"]:
        lines.append(
            f"| `{row['variant_id']}` | `{row['read']}` | "
            f"`{row['oos_h12_net']}` / `{row['oos_h12_pf']}` | "
            f"`{row['oos_no_oct_net']}` / `{row['oos_no_oct_pf']}` | "
            f"`{row['oos_second_half_net']}` / `{row['oos_second_half_pf']}` |"
        )
    return "\n".join(lines)


def write_docs(summary: Mapping[str, Any]) -> None:
    common.write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    common.write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed_with_boundary",
            "judgment": summary["judgment"],
            "required_gate_coverage": {
                "performance_attribution": "recorded",
                "result_judgment": "recorded",
                "runtime_evidence_gate": summary["external_verification_status"],
                "final_claim_guard": "no_baseline_no_promotion_no_runtime_authority_no_stage36",
            },
            "forbidden_claims": summary["forbidden_claims"],
        },
    )
    common.write_md(
        REPORT_PATH,
        f"""# Stage35 Closeout Packet(35단계 마감 묶음)

- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- MT5 attempts(MT5 시도): `{summary['mt5_attempt_count']}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary['mt5_kpi_record_count']}`
- normalized records(정규화 기록): `{summary['normalized_records']}`
- trade rows(거래 행): `{summary['trade_level_rows']}`
- parser errors(파서 오류): `{summary['parser_errors']}`

## Final Candidate Read(최종 후보 판독)

{_candidate_table(summary)}

## Closeout Decision(마감 결정)

더 파볼 Stage35(35단계) 후보는 없다.

효과(effect, 효과): Stage35(35단계)는 reviewed closed(검토 후 닫힘)로 끝나고, Stage36(36단계)은 열지 않는다. `return_volatility_shape_state2`와 `session_cash_open_0_30`은 fragile seed(취약 씨앗)로만 보존한다.

## Boundary(경계)

`{BOUNDARY}`

baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 없다.
""",
    )
    common.write_md(
        DECISION_PATH,
        f"""# 2026-05-09 Stage35 Closeout, No Stage36(35단계 마감, 36단계 미개방)

## Decision(결정)

Stage35(35단계) `{base.STAGE_ID}`를 closeout(마감)한다. Stage36(36단계)은 열지 않는다.

효과(effect, 효과): RUN29A/RUN29B/RUN29C(29A/29B/29C 실행)의 MT5 runtime probe(MT5 런타임 탐침) 근거를 보존하고, 추가 Stage35 탐침을 멈춘다.

## Reason(이유)

RUN29C(29C 실행)에서 남은 4개 후보가 no-October OOS(10월 제외 표본외)와 OOS second half(표본외 후반)를 함께 통과하지 못했다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    common.write_md(
        base.STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage35 Selection Status(35단계 선택 상태)

- stage(단계): `{base.STAGE_ID}`
- status(상태): `{summary['status']}`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- stage36 opened(36단계 개방): `false(아님)`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{summary['next_action']}`

효과(effect, 효과): Stage35(35단계)는 닫혔고, 남은 단서는 운영 후보가 아니라 취약 씨앗으로만 보존된다.
""",
    )


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": base.STAGE_ID,
            "lane": "stage_closeout",
            "status": "reviewed_closed",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["report"],
            "notes": "Stage35 closeout after RUN29A-RUN29C MT5 runtime probes; Stage36 not opened; no baseline/promotion/runtime authority.",
        }
    ]
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage_closeout",
            "stage_id": base.STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage_closeout",
            "parent_run_id": "",
            "record_view": "stage35_closeout",
            "tier_scope": "Tier A; Tier B out_of_scope_by_claim",
            "kpi_scope": "stage_closeout",
            "scoreboard_lane": "stage_closeout",
            "status": "reviewed_closed",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["report"],
            "primary_kpi": common.ledger_pairs(
                [
                    ("mt5_attempts", summary["mt5_attempt_count"]),
                    ("mt5_kpi_records", summary["mt5_kpi_record_count"]),
                    ("stage36_opened", int(bool(summary["stage36_opened"]))),
                ]
            ),
            "guardrail_kpi": common.ledger_pairs(
                [
                    ("candidate_survivors", 0),
                    ("fragile_seed_count", len(summary["preserved_clues"])),
                    ("boundary", BOUNDARY),
                ]
            ),
            "external_verification_status": summary["external_verification_status"],
            "notes": "Closeout row; no operating selection, no promotion candidate, no runtime authority.",
        }
    ]
    outputs = {
        "run_registry": common.upsert_run_rows(run_rows),
        "project_alpha_ledger": common.upsert_alpha_rows(common.PROJECT_ALPHA_LEDGER_PATH, ledger_rows),
        "stage_ledger": common.upsert_alpha_rows(base.STAGE_LEDGER_PATH, ledger_rows),
    }
    common.write_json(PACKET_ROOT / "ledger_materialization.json", outputs)
    return outputs


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    path = common.WORKSPACE_STATE_PATH
    text = common.io_path(path).read_text(encoding="utf-8-sig")
    text = re.sub(r"updated_on: .+", "updated_on: '2026-05-09'", text, count=1)
    text = re.sub(r"active_branch: .+", f"active_branch: {summary['active_branch']}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {base.STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    focus = (
        f"- Stage35(35단계) {base.STAGE_ID} reviewed_closed_no_stage36_opened(검토 후 닫힘, 36단계 미개방): "
        "RUN29A-RUN29C(29A-29C 실행) MT5 runtime probe(MT5 런타임 탐침)를 마감했고, "
        "더 파볼 Stage35 후보는 없다고 판정했다; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n"
    )
    text = re.sub(r"- Stage35\(35단계\).*?\n", "", text, count=1)
    text = re.sub(r"current_focus:\n", "current_focus:\n" + focus, text, count=1)
    text = re.sub(
        r"- current_run_id\(현재 실행 ID\).*?\n",
        f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 마감인 `{RUN_ID}`를 가리킨다. next action(다음 행동)은 `{summary['next_action']}`이다.\n",
        text,
        count=1,
    )
    block = f"""stage35_unsupervised_market_state_atlas:
  packet_id: {PACKET_ID}
  stage_id: {base.STAGE_ID}
  status: reviewed_closed_no_stage36_opened
  current_run_id: {RUN_ID}
  idea_id: IDEA-ST35-UNSUPERVISED-MARKET-STATE-ATLAS
  source_runs: run29A_unsupervised_market_state_atlas_mt5_probe_v1, run29B_stage35_worthwhile_deep_sweep_mt5_probe_v1, run29C_stage35_candidate_four_deep_dive_mt5_probe_v1
  preserved_clues: return_volatility_shape_state2_fragile_seed, session_cash_open_0_30_weak_context_clue
  decision_path: {common.rel(DECISION_PATH)}
  stage_path: stages/{base.STAGE_ID}
  report_path: {common.rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  external_verification_status: {summary['external_verification_status']}
  stage36_opened: false
  next_action: {summary['next_action']}
  boundary: {BOUNDARY}
"""
    text = re.sub(r"stage35_unsupervised_market_state_atlas:\n(?:  .+\n)+\n", block + "\n", text, count=1)
    common.write_md(path, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = common.io_path(common.CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage35 Closeout.*?(?=## Latest |\Z)", "", old, count=1, flags=re.DOTALL)
    block = f"""## Latest Stage35 Closeout(최신 35단계 마감)

- active stage(활성 단계): `{base.STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- status(상태): `reviewed_closed_no_stage36_opened`
- next action(다음 행동): `{summary['next_action']}`

Stage35(35단계)는 RUN29A-RUN29C(29A-29C 실행) MT5 runtime probe(MT5 런타임 탐침)를 끝으로 마감했다.

결과(result, 결과): 남은 4개 후보는 no-October OOS(10월 제외 표본외)와 OOS second half(표본외 후반)를 함께 통과하지 못했다. 더 파볼 Stage35 후보는 없다.

효과(effect, 효과): Stage36(36단계)은 열지 않고, fragile seed(취약 씨앗)만 보존한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    common.write_md(common.CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog(summary: Mapping[str, Any]) -> None:
    old_path = common.CHANGELOG_PATH
    old = common.io_path(old_path).read_text(encoding="utf-8-sig") if common.io_path(old_path).exists() else ""
    old = re.sub(r"^## 2026-05-09 Stage35 Closeout.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-09 Stage35 Closeout(35단계 마감)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed_no_stage36_opened`
- external verification(외부 검증): `{summary['external_verification_status']}`
- judgment(판정): `{summary['judgment']}`
- effect(효과): Stage35(35단계)를 마감하고 Stage36(36단계)은 열지 않았다. 남은 단서는 취약 씨앗으로만 보존하며 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    common.write_md(old_path, entry + old.lstrip("\ufeff"))


def run(args: argparse.Namespace) -> dict[str, Any]:
    summary = build_summary()
    write_docs(summary)
    summary["ledger_materialization"] = materialize_ledgers(summary)
    common.write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    if not args.skip_state_update:
        update_workspace_state(summary)
        prepend_context(summary)
        append_changelog(summary)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Close Stage35 without opening Stage36.")
    parser.add_argument("--skip-state-update", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    summary = run(build_arg_parser().parse_args(argv))
    print(
        json.dumps(
            {
                "status": summary["status"],
                "judgment": summary["judgment"],
                "external_verification_status": summary["external_verification_status"],
                "stage36_opened": summary["stage36_opened"],
                "mt5_attempt_count": summary["mt5_attempt_count"],
                "report": summary["output_paths"]["report"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
