from __future__ import annotations

import re
from typing import Any, Mapping, Sequence

from stage_pipelines.stage35 import common
from stage_pipelines.stage35 import worthwhile_config as cfg


def _mt5_rows(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        rows.append(
            {
                "variant_id": record.get("source_variant_id"),
                "family": record.get("source_family"),
                "record_view": record.get("record_view"),
                "split": record.get("split"),
                "direction": record.get("state_direction"),
                "trade_count": metrics.get("trade_count"),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "max_drawdown_amount": metrics.get("max_drawdown_amount"),
                "feature_ready_count": metrics.get("feature_ready_count"),
                "model_ok_count": metrics.get("model_ok_count"),
                "order_fill_count": metrics.get("order_fill_count"),
                "status": record.get("status"),
            }
        )
    return rows


def _best_oos_rows(rows: Sequence[Mapping[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    oos_rows = [dict(row) for row in rows if str(row.get("split")) == "oos" and common.numeric(row.get("trade_count"), 0.0) > 0]
    return sorted(
        oos_rows,
        key=lambda row: (
            common.numeric(row.get("profit_factor"), -999.0),
            common.numeric(row.get("net_profit"), -999999.0),
            common.numeric(row.get("trade_count"), 0.0),
        ),
        reverse=True,
    )[:limit]


def _variant_runtime_read(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("variant_id")), {})[str(row.get("split"))] = row
    reads: list[dict[str, Any]] = []
    for variant_id, splits in grouped.items():
        validation = splits.get("validation_is", {})
        oos = splits.get("oos", {})
        validation_positive = common.numeric(validation.get("net_profit"), 0.0) > 0 and common.numeric(validation.get("profit_factor"), 0.0) > 1.0
        oos_positive = common.numeric(oos.get("net_profit"), 0.0) > 0 and common.numeric(oos.get("profit_factor"), 0.0) > 1.0
        if validation_positive and oos_positive:
            read = "both_positive"
        elif oos_positive:
            read = "oos_only"
        elif validation_positive:
            read = "validation_only"
        else:
            read = "weak_or_negative"
        reads.append(
            {
                "variant_id": variant_id,
                "family": (validation or oos).get("family"),
                "direction": (validation or oos).get("direction"),
                "read": read,
                "validation_trades": validation.get("trade_count"),
                "validation_net_profit": validation.get("net_profit"),
                "validation_profit_factor": validation.get("profit_factor"),
                "oos_trades": oos.get("trade_count"),
                "oos_net_profit": oos.get("net_profit"),
                "oos_profit_factor": oos.get("profit_factor"),
            }
        )
    order = {"both_positive": 0, "oos_only": 1, "validation_only": 2, "weak_or_negative": 3}
    return sorted(
        reads,
        key=lambda row: (
            order.get(str(row["read"]), 99),
            -common.numeric(row.get("oos_profit_factor"), -999.0),
            -common.numeric(row.get("oos_net_profit"), -999999.0),
        ),
    )


def build_summary(
    *,
    created_at: str,
    branch: str,
    variants: Sequence[Mapping[str, Any]],
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
        "source_packet_id": cfg.SOURCE_PACKET_ID,
        "source_run_id": cfg.SOURCE_RUN_ID,
        "idea_id": cfg.IDEA_ID,
        "created_at_utc": created_at,
        "active_branch": branch,
        "status": "reviewed_stage35_worthwhile_deep_sweep_mt5_completed" if completed else "blocked_stage35_worthwhile_deep_sweep_mt5_after_attempt",
        "judgment": cfg.JUDGMENT_COMPLETED if completed else cfg.JUDGMENT_BLOCKED,
        "boundary": cfg.BOUNDARY,
        "variant_count": len(variants),
        "variant_rows": list(variants),
        "runtime_inputs": runtime_inputs,
        "external_verification_status": result.get("external_verification_status"),
        "planned_mt5_attempt_count": len(result.get("attempts", [])),
        "mt5_attempt_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "mt5_rows": mt5_rows,
        "skipped_empty_feature_count": len(runtime_inputs.get("skipped_empty_features", [])),
        "skipped_empty_features": runtime_inputs.get("skipped_empty_features", []),
        "best_oos_runtime_clues": _best_oos_rows(mt5_rows),
        "variant_runtime_read": _variant_runtime_read(mt5_rows),
        "tier_records": {
            "tier_a_separate": "completed" if completed else "blocked_after_attempt",
            "tier_b_separate": "out_of_scope_by_claim_stage35_tier_a_runtime_probe_only",
            "tier_a_b_combined": "out_of_scope_by_claim_stage35_tier_a_runtime_probe_only",
        },
        "exploration_design": {
            "idea_id": cfg.IDEA_ID,
            "hypothesis": "Stage35 useful context may be hidden inside session slices and individual atlas states rather than only the five selected RUN29A topics.",
            "legacy_relation": "concept_only",
            "tier_scope": "Tier A runtime probe; Tier B and combined records are out_of_scope_by_claim.",
            "broad_sweep": "7 session timing variants plus all return-volatility and trend-momentum atlas states.",
            "extreme_sweep": "OOS drift stress excludes 2025-10 for one return-volatility state and one trend-momentum state.",
            "micro_search_gate": "Only variants with repeated validation/OOS MT5 strength should move to a separate native-rule or WFO packet.",
            "wfo_plan": "not WFO; this is a single-window runtime probe and cannot make operating claims.",
            "failure_memory": "Weak or split-inconsistent variants remain negative clues, not dead ideas.",
            "evidence_boundary": "runtime_probe",
        },
        "experiment_design": {
            "hypothesis": "A coarser all-worthwhile sweep can tell which Stage35 clues deserve a later narrow packet.",
            "decision_use": "Choose what, if anything, is still worth researching inside Stage35.",
            "comparison_baseline": cfg.SOURCE_RUN_ID,
            "control_variables": [
                "US100 M5 dataset",
                cfg.FEATURE_SET_ID,
                cfg.LABEL_ID,
                cfg.SPLIT_CONTRACT,
                f"feature_order_hash={cfg.FEATURE_ORDER_HASH}",
                "constant EBM score table",
                f"max_hold_bars={cfg.MAX_HOLD_BARS}",
            ],
            "changed_variables": ["variant row masks", "direction chosen from validation proxy", "OOS drift omission for two stress variants"],
            "sample_scope": "Tier A validation_is and OOS Strategy Tester windows.",
            "success_criteria": "MT5 completed with enough trades and a validation/OOS clue that survives boundary wording.",
            "failure_criteria": "No variant shows OOS strength, or the clue depends on one fragile month only.",
            "invalid_conditions": "missing feature files, malformed tester report, feature hash mismatch, or incomplete MT5 handoff.",
            "stop_conditions": "Stop after all planned variants run; no micro tuning inside this packet.",
            "evidence_plan": "run_manifest, kpi_record, normalized KPI packet, stage/project ledgers, report, and strategy tester outputs.",
        },
        "runtime_parity": {
            "research_path": "stage_pipelines/stage35/worthwhile_deep_sweep.py",
            "runtime_path": "foundation.control_plane.mt5_tier_balance_completion routed MT5 tester handoff",
            "shared_contract": "58-feature order, split windows, constant EBM score table, thresholds, max hold, and row-omission masks.",
            "known_differences": runtime_inputs.get("known_runtime_difference"),
            "parity_check": "MT5 Strategy Tester output plus normalized KPI parsing.",
            "runtime_claim_boundary": "runtime_probe",
        },
        "backtest_forensics": {
            "tester_identity": "captured in prepared MT5 attempts and strategy tester reports",
            "ea_identity": "existing thin EA entrypoint and common-file model/feature handoff",
            "report_identity": "strategy_tester_reports in run_manifest.json",
            "trade_evidence": "mt5_runtime_summary.csv and normalized KPI records",
            "cost_assumptions": "broker Strategy Tester defaults in the active terminal profile",
            "forensic_checks": "feature handoff, tester output presence, normalized KPI parser errors, and ledger identity",
            "backtest_judgment": "usable_with_boundary" if completed else "blocked",
        },
        "result_judgment": {
            "result_subject": cfg.RUN_ID,
            "evidence_available": "MT5 KPI records, run manifest, tester reports, normalized KPI packet, and ledgers" if completed else "prepared artifacts and blocked attempt record",
            "evidence_missing": "native MT5 clustering, WFO, Tier B/combined runtime rows, and operating parity closure",
            "judgment_label": "inconclusive_runtime_probe" if completed else "blocked",
            "claim_boundary": cfg.BOUNDARY,
            "next_condition": "Only a separate narrow packet with stronger parity/WFO can upgrade the clue.",
            "user_explanation_hook": "This tells what is still worth looking at, not what is ready to trade.",
        },
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "next_action": "judge_stage35_run29B_clues_then_close_or_open_one_narrow_followup",
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority", "live_readiness"],
        "output_paths": {
            "variant_summary": common.rel(cfg.RESULT_ROOT / "worthwhile_variant_summary.csv"),
            "mt5_summary": common.rel(cfg.RESULT_ROOT / "mt5_runtime_summary.csv"),
            "aggregate_summary": common.rel(cfg.PACKET_ROOT / "aggregate_summary.json"),
            "run_manifest": common.rel(cfg.RUN_ROOT / "run_manifest.json"),
            "kpi_record": common.rel(cfg.RUN_ROOT / "kpi_record.json"),
            "report": common.rel(cfg.REPORT_PATH),
        },
    }


def write_run_files(summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    common.write_csv(cfg.RESULT_ROOT / "worthwhile_variant_summary.csv", summary["variant_rows"])
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
            "variants": summary["variant_rows"],
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
            "backtest_forensics": summary["backtest_forensics"],
        },
    )
    common.write_json(
        cfg.RUN_ROOT / "kpi_record.json",
        {
            "run_id": cfg.RUN_ID,
            "stage_id": cfg.STAGE_ID,
            "kpi_scope": "stage35_worthwhile_deep_sweep_mt5_runtime_probe",
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
            "allowed_claims": ["Stage35 RUN29B completed as runtime_probe", "worthwhile variants were MT5-tested if completed"],
            "forbidden_claims": summary["forbidden_claims"],
            "required_gate_coverage": {
                "exploration_design": "recorded",
                "runtime_parity": "recorded",
                "backtest_forensics": "recorded",
                "result_judgment": "recorded",
                "tier_pairing": summary["tier_records"],
            },
        },
    )


def _variant_table(summary: Mapping[str, Any]) -> str:
    lines = [
        "| variant(변형) | family(계열) | direction(방향) | validation rows(검증 행) | validation PF(검증 수익 팩터) | OOS rows(표본외 행) | OOS PF(표본외 수익 팩터) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["variant_rows"]:
        lines.append(
            f"| `{row.get('variant_id')}` | `{row.get('family')}` | `{row.get('direction')}` | "
            f"`{row.get('validation_row_count')}` | `{row.get('validation_profit_factor_proxy')}` | "
            f"`{row.get('oos_row_count')}` | `{row.get('oos_profit_factor_proxy')}` |"
        )
    return "\n".join(lines)


def _mt5_table(summary: Mapping[str, Any]) -> str:
    lines = [
        "| variant(변형) | split(분할) | direction(방향) | trades(거래) | net(순손익) | PF(수익 팩터) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary["mt5_rows"]:
        lines.append(
            f"| `{row.get('variant_id')}` | `{row.get('split')}` | `{row.get('direction')}` | "
            f"`{row.get('trade_count')}` | `{row.get('net_profit')}` | `{row.get('profit_factor')}` |"
        )
    return "\n".join(lines)


def _best_table(summary: Mapping[str, Any]) -> str:
    if not summary["best_oos_runtime_clues"]:
        return "- 없음(none, 없음)"
    lines = [
        "| rank(순위) | variant(변형) | trades(거래) | net(순손익) | PF(수익 팩터) |",
        "|---:|---|---:|---:|---:|",
    ]
    for index, row in enumerate(summary["best_oos_runtime_clues"], start=1):
        lines.append(
            f"| `{index}` | `{row.get('variant_id')}` | `{row.get('trade_count')}` | "
            f"`{row.get('net_profit')}` | `{row.get('profit_factor')}` |"
        )
    return "\n".join(lines)


def _read_table(summary: Mapping[str, Any]) -> str:
    lines = [
        "| read(판독) | variant(변형) | val net/PF(검증 순손익/수익 팩터) | OOS net/PF(표본외 순손익/수익 팩터) |",
        "|---|---|---:|---:|",
    ]
    for row in summary["variant_runtime_read"]:
        lines.append(
            f"| `{row.get('read')}` | `{row.get('variant_id')}` | "
            f"`{row.get('validation_net_profit')}` / `{row.get('validation_profit_factor')}` | "
            f"`{row.get('oos_net_profit')}` / `{row.get('oos_profit_factor')}` |"
        )
    return "\n".join(lines)


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    common.write_md(
        cfg.REPORT_PATH,
        f"""# RUN29B Worthwhile Deep Sweep MT5 Probe(29B 실행 더 파볼 축 깊은 훑기 MT5 탐침)

- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- variants(변형 수): `{summary['variant_count']}`
- planned MT5 attempts(계획 MT5 시도): `{summary['planned_mt5_attempt_count']}`
- MT5 attempts(MT5 시도): `{summary['mt5_attempt_count']}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary['mt5_kpi_record_count']}`
- skipped empty feature files(빈 피처 파일 제외): `{summary['skipped_empty_feature_count']}`

## Why This Run Exists(이 실행의 이유)

RUN29A(29A 실행)에서 그나마 볼 만한 단서는 session timing(세션 시간), return-volatility state(수익률/변동성 상태), trend-momentum state(추세/모멘텀 상태)였다. RUN29B(29B 실행)는 그 안에서 더 파볼 만한 축을 전부 MT5(`MetaTrader 5`, 메타트레이더5)에 넘겨 확인했다.

효과(effect, 효과): 좋은 단서와 버릴 단서를 한 번에 분리한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Python Proxy Variants(Python 대리 측정 변형)

{_variant_table(summary)}

## MT5 Runtime Read(MT5 런타임 판독)

{_mt5_table(summary)}

## Best OOS Clues(가장 나은 표본외 단서)

{_best_table(summary)}

## Easy Read(쉬운 판독)

{_read_table(summary)}

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `{summary['tier_records']['tier_a_separate']}`
- Tier B separate(Tier B 분리): `{summary['tier_records']['tier_b_separate']}`
- Tier A+B combined(Tier A+B 합산): `{summary['tier_records']['tier_a_b_combined']}`

## Boundary(경계)

`{cfg.BOUNDARY}`

runtime_probe(런타임 탐침)일 뿐이다. edge(거래 우위), alpha_quality(알파 품질), baseline(기준선), promotion(승격), runtime_authority(런타임 권위), live_readiness(실거래 준비)는 금지 주장이다.
""",
    )
    common.write_md(
        cfg.STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage35 Selection Status(35단계 선택 상태)

- stage(단계): `{cfg.STAGE_ID}`
- status(상태): `{summary['status']}`
- current run(현재 실행): `{cfg.RUN_ID}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- latest packet(최신 묶음): `{cfg.PACKET_ID}`
- next action(다음 행동): `{summary['next_action']}`

효과(effect, 효과): RUN29B(29B 실행)는 Stage35(35단계) 안에서 더 파볼 축을 넓게 확인했지만, 선택이나 운영 의미는 만들지 않는다.
""",
    )
    common.write_md(
        cfg.DECISION_PATH,
        f"""# 2026-05-09 Stage35 RUN29B Worthwhile Deep Sweep(35단계 29B 실행 더 파볼 축 깊은 훑기)

## Decision(결정)

Stage35(35단계) 안에서 RUN29A(29A 실행)의 단서 중 더 파볼 만한 축을 모두 RUN29B(29B 실행)로 묶어 MT5(`MetaTrader 5`, 메타트레이더5)에 연결했다.

효과(effect, 효과): Stage35(35단계)를 억지로 이어가지 않고, 실제로 남은 단서가 있는지 한 번에 판독한다.

## Boundary(경계)

`{cfg.BOUNDARY}`

baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
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
            "notes": "Stage35 all-worthwhile session/state/drift MT5 row-omission runtime probe; no baseline/promotion/runtime authority.",
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
                "kpi_scope": "stage35_worthwhile_deep_sweep_mt5_runtime_probe",
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
                        ("family", row.get("family")),
                        ("direction", row.get("direction")),
                        ("boundary", cfg.BOUNDARY),
                    ]
                ),
                "external_verification_status": summary["external_verification_status"],
                "notes": "Actual MT5 tester row for one Stage35 worthwhile variant; row omission is a runtime_probe handoff.",
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
        f"- Stage35(35단계) {cfg.STAGE_ID} {summary['status']}: RUN29B(29B 실행)는 "
        f"`{summary['variant_count']}`개 worthwhile variants(더 파볼 변형)를 MT5 runtime probe(MT5 런타임 탐침)에 연결했다; "
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
  worthwhile_variant_count: {summary['variant_count']}
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
    old = re.sub(r"^## Latest Stage35 RUN29B.*?(?=## Latest |\Z)", "", old, count=1, flags=re.DOTALL)
    block = f"""## Latest Stage35 RUN29B Worthwhile Deep Sweep(최신 35단계 RUN29B 더 파볼 축 깊은 훑기)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `{summary['active_branch']}`
- active stage(활성 단계): `{cfg.STAGE_ID}`
- current run(현재 실행): `{cfg.RUN_ID}`
- latest packet(최신 묶음): `{cfg.PACKET_ID}`
- next action(다음 행동): `{summary['next_action']}`

RUN29B(29B 실행)는 session timing(세션 시간), return-volatility state(수익률/변동성 상태), trend-momentum state(추세/모멘텀 상태), 그리고 2025-10 drift stress(2025년 10월 변화 압박)를 모두 MT5 runtime probe(MT5 런타임 탐침)에 연결했다.

결과(result, 결과): variants(변형) `{summary['variant_count']}`, MT5 attempts(MT5 시도) `{summary['mt5_attempt_count']}`, MT5 KPI records(MT5 핵심 성과 지표 기록) `{summary['mt5_kpi_record_count']}`, external verification(외부 검증) `{summary['external_verification_status']}`.

효과(effect, 효과): Stage35(35단계)에서 남은 단서를 넓게 판독했지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

"""
    common.write_md(common.CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog(summary: Mapping[str, Any]) -> None:
    old_path = common.CHANGELOG_PATH
    old = common.io_path(old_path).read_text(encoding="utf-8-sig") if common.io_path(old_path).exists() else ""
    old = re.sub(r"^## 2026-05-09 Stage35 RUN29B.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-09 Stage35 RUN29B Worthwhile Deep Sweep(35단계 RUN29B 더 파볼 축 깊은 훑기)

- run(실행): `{cfg.RUN_ID}`
- variants(변형): `{summary['variant_count']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- judgment(판정): `{summary['judgment']}`
- effect(효과): 더 파볼 만한 Stage35(35단계) 축을 MT5 runtime probe(MT5 런타임 탐침)로 확인했지만, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

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
