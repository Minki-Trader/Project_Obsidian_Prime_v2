from __future__ import annotations

import re
from typing import Any, Mapping, Sequence

from stage_pipelines.stage35 import common
from stage_pipelines.stage35 import candidate_config as cfg


def _mt5_rows(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        rows.append(
            {
                "variant_id": record.get("source_variant_id"),
                "candidate_rank": record.get("candidate_rank"),
                "family": record.get("source_family"),
                "record_view": record.get("record_view"),
                "stress_id": record.get("stress_id") or record.get("split"),
                "stress": record.get("stress"),
                "direction": record.get("state_direction"),
                "max_hold_bars": record.get("max_hold_bars"),
                "trade_count": metrics.get("trade_count"),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "max_drawdown_amount": metrics.get("max_drawdown_amount"),
                "feature_ready_count": metrics.get("feature_ready_count"),
                "model_ok_count": metrics.get("model_ok_count"),
                "status": record.get("status"),
            }
        )
    return rows


def _positive(row: Mapping[str, Any] | None) -> bool:
    if not row:
        return False
    return common.numeric(row.get("net_profit"), 0.0) > 0 and common.numeric(row.get("profit_factor"), 0.0) > 1.0


def _candidate_read(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_variant: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        by_variant.setdefault(str(row.get("variant_id")), {})[str(row.get("stress_id"))] = row
    out: list[dict[str, Any]] = []
    for rank, candidate_id in enumerate(cfg.CANDIDATE_IDS, start=1):
        records = by_variant.get(candidate_id, {})
        base_validation = records.get("validation_h12")
        base_oos = records.get("oos_h12")
        no_oct = records.get("oos_no_oct2025_h12")
        first_half = records.get("oos_first_half_h12")
        second_half = records.get("oos_second_half_h12")
        if _positive(base_validation) and _positive(base_oos) and _positive(no_oct) and _positive(first_half) and _positive(second_half):
            read = "survives_base_drift_and_halves"
        elif _positive(base_validation) and _positive(base_oos) and _positive(no_oct):
            read = "survives_base_and_no_oct"
        elif _positive(base_validation) and _positive(base_oos):
            read = "base_positive_only"
        else:
            read = "failed_base_recheck"
        out.append(
            {
                "candidate_rank": rank,
                "variant_id": candidate_id,
                "read": read,
                "validation_h12_net": None if base_validation is None else base_validation.get("net_profit"),
                "validation_h12_pf": None if base_validation is None else base_validation.get("profit_factor"),
                "oos_h12_net": None if base_oos is None else base_oos.get("net_profit"),
                "oos_h12_pf": None if base_oos is None else base_oos.get("profit_factor"),
                "oos_no_oct_net": None if no_oct is None else no_oct.get("net_profit"),
                "oos_no_oct_pf": None if no_oct is None else no_oct.get("profit_factor"),
                "oos_first_half_net": None if first_half is None else first_half.get("net_profit"),
                "oos_first_half_pf": None if first_half is None else first_half.get("profit_factor"),
                "oos_second_half_net": None if second_half is None else second_half.get("net_profit"),
                "oos_second_half_pf": None if second_half is None else second_half.get("profit_factor"),
            }
        )
    return out


def build_summary(
    *,
    created_at: str,
    branch: str,
    candidates: Sequence[Mapping[str, Any]],
    runtime_inputs: Mapping[str, Any],
    result: Mapping[str, Any],
) -> dict[str, Any]:
    completed = result.get("external_verification_status") == "completed"
    mt5_rows = _mt5_rows(result.get("mt5_kpi_records", []))
    return {
        "packet_id": cfg.PACKET_ID,
        "stage_id": cfg.STAGE_ID,
        "run_id": cfg.RUN_ID,
        "run_number": cfg.RUN_NUMBER,
        "source_run_id": cfg.SOURCE_RUN_ID,
        "source_packet_id": cfg.SOURCE_PACKET_ID,
        "idea_id": cfg.IDEA_ID,
        "created_at_utc": created_at,
        "active_branch": branch,
        "status": "reviewed_stage35_candidate_four_deep_dive_mt5_completed" if completed else "blocked_stage35_candidate_four_deep_dive_mt5_after_attempt",
        "judgment": cfg.JUDGMENT_COMPLETED if completed else cfg.JUDGMENT_BLOCKED,
        "boundary": cfg.BOUNDARY,
        "candidate_count": len(candidates),
        "candidate_rows": list(candidates),
        "stress_output_count": len(runtime_inputs.get("stress_outputs", [])),
        "runtime_inputs": runtime_inputs,
        "external_verification_status": result.get("external_verification_status"),
        "planned_mt5_attempt_count": len(result.get("attempts", [])),
        "mt5_attempt_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "skipped_empty_feature_count": len(runtime_inputs.get("skipped_empty_features", [])),
        "skipped_empty_features": runtime_inputs.get("skipped_empty_features", []),
        "mt5_rows": mt5_rows,
        "candidate_read": _candidate_read(mt5_rows),
        "exploration_design": {
            "idea_id": cfg.IDEA_ID,
            "hypothesis": "The four RUN29B both-positive clues may differ by hold length and OOS time dependence.",
            "legacy_relation": "concept_only",
            "tier_scope": "Tier A runtime probe; Tier B and combined records are out_of_scope_by_claim.",
            "broad_sweep": "Four selected Stage35 variants from RUN29B.",
            "extreme_sweep": "hold 6/12/24 bars plus OOS without 2025-10 and OOS half-window stress.",
            "micro_search_gate": "Only candidates surviving base, no-October, and half-window checks should get a native or WFO packet.",
            "wfo_plan": "not WFO; this is a candidate stress runtime probe.",
            "failure_memory": "Candidate failure is preserved as a negative clue, not idea death.",
            "evidence_boundary": "runtime_probe",
        },
        "runtime_parity": {
            "research_path": "stage_pipelines/stage35/candidate_deep_dive.py",
            "runtime_path": "foundation.control_plane.mt5_tier_balance_completion routed MT5 tester handoff",
            "shared_contract": "58-feature order, fixed thresholds, constant EBM score table, row-omission masks, split windows, and max-hold parameter.",
            "known_differences": runtime_inputs.get("known_runtime_difference"),
            "parity_check": "MT5 Strategy Tester output plus normalized KPI parsing.",
            "runtime_claim_boundary": "runtime_probe",
        },
        "result_judgment": {
            "result_subject": cfg.RUN_ID,
            "evidence_available": "MT5 KPI records, run manifest, tester reports, normalized KPI packet, and ledgers" if completed else "prepared artifacts and blocked attempt record",
            "evidence_missing": "native MT5 state assignment, WFO, Tier B/combined runtime rows, and runtime authority closure",
            "judgment_label": "inconclusive_runtime_probe" if completed else "blocked",
            "claim_boundary": cfg.BOUNDARY,
            "next_condition": "Only a separate narrow native/WFO packet can upgrade a surviving clue.",
        },
        "tier_records": {
            "tier_a_separate": "completed" if completed else "blocked_after_attempt",
            "tier_b_separate": "out_of_scope_by_claim_stage35_tier_a_runtime_probe_only",
            "tier_a_b_combined": "out_of_scope_by_claim_stage35_tier_a_runtime_probe_only",
        },
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "next_action": "judge_run29C_candidate_survivors_then_close_stage35_or_open_one_native_followup",
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority", "live_readiness"],
        "output_paths": {
            "stress_summary": common.rel(cfg.RESULT_ROOT / "candidate_stress_input_summary.csv"),
            "mt5_summary": common.rel(cfg.RESULT_ROOT / "mt5_runtime_summary.csv"),
            "aggregate_summary": common.rel(cfg.PACKET_ROOT / "aggregate_summary.json"),
            "run_manifest": common.rel(cfg.RUN_ROOT / "run_manifest.json"),
            "kpi_record": common.rel(cfg.RUN_ROOT / "kpi_record.json"),
            "report": common.rel(cfg.REPORT_PATH),
        },
    }


def write_run_files(summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    common.write_csv(cfg.RESULT_ROOT / "candidate_stress_input_summary.csv", summary["runtime_inputs"]["stress_outputs"])
    common.write_csv(cfg.RESULT_ROOT / "mt5_runtime_summary.csv", summary["mt5_rows"])
    common.write_json(
        cfg.RUN_ROOT / "run_manifest.json",
        {
            "packet_id": cfg.PACKET_ID,
            "stage_id": cfg.STAGE_ID,
            "run_id": cfg.RUN_ID,
            "run_number": cfg.RUN_NUMBER,
            "boundary": cfg.BOUNDARY,
            "source_run_id": cfg.SOURCE_RUN_ID,
            "attempts": result.get("attempts", []),
            "candidates": summary["candidate_rows"],
            "runtime_probe": {
                "common_copies": result.get("common_copies", []),
                "compile": result.get("compile", {}),
                "execution_results": result.get("execution_results", []),
                "strategy_tester_reports": result.get("strategy_tester_reports", []),
                "external_verification_status": result.get("external_verification_status"),
                "judgment": result.get("judgment"),
                "failure": result.get("failure"),
            },
            "runtime_parity": summary["runtime_parity"],
        },
    )
    common.write_json(
        cfg.RUN_ROOT / "kpi_record.json",
        {
            "run_id": cfg.RUN_ID,
            "stage_id": cfg.STAGE_ID,
            "kpi_scope": "stage35_candidate_four_deep_dive_mt5_runtime_probe",
            "model_family": cfg.MODEL_FAMILY,
            "feature_set_id": cfg.FEATURE_SET_ID,
            "label_id": cfg.LABEL_ID,
            "split_contract": cfg.SPLIT_CONTRACT,
            "mt5_records": result.get("mt5_kpi_records", []),
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "mt5": {"kpi_records": result.get("mt5_kpi_records", [])},
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "boundary": cfg.BOUNDARY,
        },
    )
    common.write_json(cfg.RESULT_ROOT / "aggregate_summary.json", summary)
    common.write_json(cfg.PACKET_ROOT / "aggregate_summary.json", summary)
    common.write_json(
        cfg.PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": cfg.PACKET_ID,
            "status": "passed_with_boundary" if summary["external_verification_status"] == "completed" else "blocked_after_attempt",
            "judgment": summary["judgment"],
            "required_gate_coverage": {
                "exploration_design": "recorded",
                "runtime_parity": "recorded",
                "result_judgment": "recorded",
                "tier_pairing": summary["tier_records"],
            },
            "forbidden_claims": summary["forbidden_claims"],
        },
    )


def _read_table(summary: Mapping[str, Any]) -> str:
    lines = [
        "| rank(순위) | candidate(후보) | read(판독) | base val(기본 검증) | base OOS(기본 표본외) | no Oct OOS(10월 제외 표본외) | first/second half(전반/후반) |",
        "|---:|---|---|---:|---:|---:|---:|",
    ]
    for row in summary["candidate_read"]:
        lines.append(
            f"| `{row['candidate_rank']}` | `{row['variant_id']}` | `{row['read']}` | "
            f"`{row['validation_h12_net']}` / `{row['validation_h12_pf']}` | "
            f"`{row['oos_h12_net']}` / `{row['oos_h12_pf']}` | "
            f"`{row['oos_no_oct_net']}` / `{row['oos_no_oct_pf']}` | "
            f"`{row['oos_first_half_net']}` / `{row['oos_first_half_pf']}` ; "
            f"`{row['oos_second_half_net']}` / `{row['oos_second_half_pf']}` |"
        )
    return "\n".join(lines)


def _mt5_table(summary: Mapping[str, Any]) -> str:
    lines = [
        "| candidate(후보) | stress(압박) | hold(보유) | trades(거래) | net(순손익) | PF(수익 팩터) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in summary["mt5_rows"]:
        lines.append(
            f"| `{row.get('variant_id')}` | `{row.get('stress_id')}` | `{row.get('max_hold_bars')}` | "
            f"`{row.get('trade_count')}` | `{row.get('net_profit')}` | `{row.get('profit_factor')}` |"
        )
    return "\n".join(lines)


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    common.write_md(
        cfg.REPORT_PATH,
        f"""# RUN29C Candidate Four Deep Dive MT5 Probe(29C 실행 후보 4개 심화 MT5 탐침)

- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- candidates(후보): `{summary['candidate_count']}`
- planned MT5 attempts(계획 MT5 시도): `{summary['planned_mt5_attempt_count']}`
- MT5 attempts(MT5 시도): `{summary['mt5_attempt_count']}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary['mt5_kpi_record_count']}`

## Easy Read(쉬운 판독)

{_read_table(summary)}

## Full MT5 Stress Table(전체 MT5 압박 표)

{_mt5_table(summary)}

## Boundary(경계)

`{cfg.BOUNDARY}`

runtime_probe(런타임 탐침)일 뿐이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
""",
    )
    common.write_md(
        cfg.DECISION_PATH,
        f"""# 2026-05-09 Stage35 RUN29C Candidate Four Deep Dive(35단계 29C 실행 후보 4개 심화)

## Decision(결정)

RUN29B(29B 실행)의 both_positive(양쪽 양호) 후보 4개를 RUN29C(29C 실행)로 분리해 hold stress(보유 기간 압박)와 OOS drift stress(표본외 변화 압박)를 MT5(`MetaTrader 5`, 메타트레이더5)에서 확인했다.

효과(effect, 효과): 남은 후보를 더 좁히되, 운영 의미는 만들지 않는다.

## Boundary(경계)

`{cfg.BOUNDARY}`
""",
    )


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    run_rows = [
        {
            "run_id": cfg.RUN_ID,
            "stage_id": cfg.STAGE_ID,
            "lane": "runtime_probe",
            "status": "reviewed" if summary["external_verification_status"] == "completed" else "blocked",
            "judgment": summary["judgment"],
            "path": common.rel(cfg.RUN_ROOT),
            "notes": "Stage35 four-candidate hold/drift MT5 runtime probe; no baseline/promotion/runtime authority.",
        }
    ]
    ledger_rows = []
    for row in summary["mt5_rows"]:
        ledger_rows.append(
            {
                "ledger_row_id": f"{cfg.RUN_ID}__{row['record_view']}",
                "stage_id": cfg.STAGE_ID,
                "run_id": cfg.RUN_ID,
                "subrun_id": row["record_view"],
                "parent_run_id": "",
                "record_view": row["record_view"],
                "tier_scope": "Tier A",
                "kpi_scope": "stage35_candidate_four_deep_dive_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": row.get("status"),
                "judgment": summary["judgment"],
                "path": summary["output_paths"]["mt5_summary"],
                "primary_kpi": common.ledger_pairs(
                    [
                        ("net_profit", row.get("net_profit")),
                        ("profit_factor", row.get("profit_factor")),
                        ("trade_count", row.get("trade_count")),
                    ]
                ),
                "guardrail_kpi": common.ledger_pairs(
                    [
                        ("variant_id", row.get("variant_id")),
                        ("stress_id", row.get("stress_id")),
                        ("max_hold_bars", row.get("max_hold_bars")),
                        ("boundary", cfg.BOUNDARY),
                    ]
                ),
                "external_verification_status": summary["external_verification_status"],
                "notes": "Actual MT5 tester row for one Stage35 candidate stress view.",
            }
        )
    outputs = {
        "run_registry": common.upsert_run_rows(run_rows),
        "project_alpha_ledger": common.upsert_alpha_rows(common.PROJECT_ALPHA_LEDGER_PATH, ledger_rows),
        "stage_ledger": common.upsert_alpha_rows(cfg.STAGE_LEDGER_PATH, ledger_rows),
    }
    common.write_json(cfg.PACKET_ROOT / "ledger_materialization.json", outputs)
    return outputs


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    path = common.WORKSPACE_STATE_PATH
    text = common.io_path(path).read_text(encoding="utf-8-sig")
    text = re.sub(r"updated_on: .+", "updated_on: '2026-05-09'", text, count=1)
    text = re.sub(r"active_branch: .+", f"active_branch: {summary['active_branch']}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {cfg.STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {cfg.RUN_ID}", text, count=1)
    focus = (
        f"- Stage35(35단계) {cfg.STAGE_ID} {summary['status']}: RUN29C(29C 실행)는 "
        "RUN29B(29B 실행)의 4개 후보를 hold/drift stress(보유/변화 압박)로 MT5 runtime probe(MT5 런타임 탐침)했다; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n"
    )
    text = re.sub(r"- Stage35\(35단계\).*?\n", "", text, count=1)
    text = re.sub(r"current_focus:\n", "current_focus:\n" + focus, text, count=1)
    text = re.sub(
        r"- current_run_id\(현재 실행 ID\).*?\n",
        f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 실행인 `{cfg.RUN_ID}`를 가리킨다. next action(다음 행동)은 `{summary['next_action']}`이다.\n",
        text,
        count=1,
    )
    block = f"""stage35_unsupervised_market_state_atlas:
  packet_id: {cfg.PACKET_ID}
  stage_id: {cfg.STAGE_ID}
  status: {summary['status']}
  current_run_id: {cfg.RUN_ID}
  idea_id: {cfg.IDEA_ID}
  selected_topics: 5
  candidate_deep_dive_count: {summary['candidate_count']}
  decision_path: {common.rel(cfg.DECISION_PATH)}
  stage_path: stages/{cfg.STAGE_ID}
  report_path: {common.rel(cfg.REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{cfg.PACKET_ID}/aggregate_summary.json
  external_verification_status: {summary['external_verification_status']}
  next_action: {summary['next_action']}
  boundary: {cfg.BOUNDARY}
"""
    text = re.sub(r"stage35_unsupervised_market_state_atlas:\n(?:  .+\n)+\n", block + "\n", text, count=1)
    common.write_md(path, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = common.io_path(common.CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage35 RUN29C.*?(?=## Latest |\Z)", "", old, count=1, flags=re.DOTALL)
    block = f"""## Latest Stage35 RUN29C Candidate Four Deep Dive(최신 35단계 RUN29C 후보 4개 심화)

- active stage(활성 단계): `{cfg.STAGE_ID}`
- current run(현재 실행): `{cfg.RUN_ID}`
- latest packet(최신 묶음): `{cfg.PACKET_ID}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- MT5 attempts(MT5 시도): `{summary['mt5_attempt_count']}`

RUN29C(29C 실행)는 RUN29B(29B 실행)의 1/2/3/4 후보를 hold stress(보유 기간 압박)와 OOS drift stress(표본외 변화 압박)로 다시 확인했다.

효과(effect, 효과): Stage35(35단계) 후보를 좁히되 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

"""
    common.write_md(common.CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog(summary: Mapping[str, Any]) -> None:
    old_path = common.CHANGELOG_PATH
    old = common.io_path(old_path).read_text(encoding="utf-8-sig") if common.io_path(old_path).exists() else ""
    old = re.sub(r"^## 2026-05-09 Stage35 RUN29C.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-09 Stage35 RUN29C Candidate Four Deep Dive(35단계 RUN29C 후보 4개 심화)

- run(실행): `{cfg.RUN_ID}`
- candidates(후보): `{summary['candidate_count']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- judgment(판정): `{summary['judgment']}`
- effect(효과): RUN29B(29B 실행)의 4개 후보를 MT5 runtime probe(MT5 런타임 탐침)로 더 좁혔지만, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    common.write_md(old_path, entry + old.lstrip("\ufeff"))


__all__ = [
    "append_changelog",
    "build_summary",
    "materialize_ledgers",
    "prepend_context",
    "update_workspace_state",
    "write_run_files",
    "write_stage_docs",
]
