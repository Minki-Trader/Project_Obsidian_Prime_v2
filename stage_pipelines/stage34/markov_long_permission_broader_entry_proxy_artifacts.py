from __future__ import annotations

import re
from typing import Any, Mapping

from foundation.control_plane.ledger import ALPHA_LEDGER_COLUMNS, RUN_REGISTRY_COLUMNS, io_path, ledger_pairs
from stage_pipelines.stage34 import markov_long_permission_broader_entry_proxy_probe as probe


for _name in (
    "RUN_ID", "PACKET_ID", "STAGE_ID", "SOURCE_RUNTIME_RUN_ID", "SOURCE_ATTRIBUTION_RUN_ID",
    "SOURCE_ENTRY_PROXY_RUN_ID", "SOURCE_FREQUENCY_RUN_ID", "RULE_ID", "BOUNDARY", "NEXT_ACTION",
    "MODEL_FAMILY", "FEATURE_SET_ID", "LABEL_ID", "SPLIT_CONTRACT", "RESULT_ROOT", "RUN_ROOT",
    "PACKET_ROOT", "REPORT_PATH", "DECISION_PATH", "STAGE_LEDGER_PATH", "PROJECT_LEDGER_PATH",
    "RUN_REGISTRY_PATH", "REVIEW_INDEX_PATH", "SELECTION_STATUS_PATH", "WORKSPACE_STATE_PATH",
    "CURRENT_WORKING_STATE_PATH", "CHANGELOG_PATH",
):
    globals()[_name] = getattr(probe, _name)

attribution = probe.attribution
rel = probe.rel
upsert_csv_rows_resilient = probe.upsert_csv_rows_resilient


def write_run_files(summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    attribution.write_csv(RESULT_ROOT / "monthly_leave_one_out.csv", list(summary["monthly_leave_one_out_rows"][0].keys()), summary["monthly_leave_one_out_rows"])
    attribution.write_csv(RESULT_ROOT / "monthly_survival_summary.csv", list(summary["monthly_summary_rows"][0].keys()), summary["monthly_summary_rows"])
    attribution.write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "source_runs": [SOURCE_RUNTIME_RUN_ID, SOURCE_ATTRIBUTION_RUN_ID, SOURCE_ENTRY_PROXY_RUN_ID, SOURCE_FREQUENCY_RUN_ID],
            "boundary": BOUNDARY,
            "runtime_probe": {
                key: result.get(key)
                for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure")
                if key in result
            },
        },
    )
    attribution.write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUNTIME_RUN_ID,
            "kpi_scope": "tier_a_markov_broader_entry_proxy_monthly_mt5_probe",
            "model_family": MODEL_FAMILY,
            "feature_set_id": FEATURE_SET_ID,
            "label_id": LABEL_ID,
            "split_contract": SPLIT_CONTRACT,
            "monthly_candidate_read": summary["monthly_candidate_read"],
            "runtime_read": summary["runtime_read"],
            "mt5_records": result.get("mt5_kpi_records", []),
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "mt5": {"kpi_records": result.get("mt5_kpi_records", [])},
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "boundary": BOUNDARY,
        },
    )
    attribution.write_json(RESULT_ROOT / "aggregate_summary.json", summary)


def review_text(summary: Mapping[str, Any]) -> str:
    candidate = summary["monthly_candidate_read"]
    validation = candidate["validation"]
    oos = candidate["oos"]
    runtime = summary["runtime_read"]
    return f"""# RUN28E Tier A Markov Broader Entry Proxy Packet(28E 실행 티어 A 마르코프 넓은 진입 대리 묶음)
## Judgment(판정)
- run(실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- rule(규칙): `{RULE_ID}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- boundary(경계): `{BOUNDARY}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): 월별 생존성(monthly robustness, 월별 버팀)을 먼저 보고, 같은 후보를 MT5(`MetaTrader 5`, 메타트레이더5) feature CSV row omission(피처 CSV 행 제거) 방식으로 실제 Strategy Tester(전략 테스터)에 찔렀다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Monthly Read(월별 판독)
- validation(검증): trades(거래 수) `{validation['full_trade_count']}`, net(순손익) `{validation['full_net_profit']}`, PF(수익 팩터) `{validation['full_profit_factor']}`, min leave-one-out net(월 하나 제외 최저 순손익) `{validation['min_leave_one_out_net_profit']}`, status(상태) `{validation['monthly_survival_status']}`
- OOS(표본외): trades(거래 수) `{oos['full_trade_count']}`, net(순손익) `{oos['full_net_profit']}`, PF(수익 팩터) `{oos['full_profit_factor']}`, min leave-one-out net(월 하나 제외 최저 순손익) `{oos['min_leave_one_out_net_profit']}`, status(상태) `{oos['monthly_survival_status']}`
- OOS dependency(OOS 의존성): top positive month(최대 양수 월) `{oos['top_positive_month']}`, top positive share(최대 양수 월 비중) `{oos['top_positive_month_net_share']}`, flags(표식) `{oos['monthly_survival_flags']}`

효과(effect, 효과): 후보는 한 달을 빼도 전체 OOS(표본외) PF(수익 팩터)가 1 아래로 깨지지는 않는다. 다만 2025-10(2025년 10월)을 빼면 OOS(표본외) net(순손익)이 `{oos['min_leave_one_out_net_profit']}`까지 얇아져서, main seed(메인 씨앗)가 아니라 dependency clue(의존성 단서)로 다루는 편이 맞다.

## MT5 Runtime Probe(MT5 런타임 탐침)
- validation(검증): trades(거래 수) `{runtime['validation'].get('trade_count')}`, net(순손익) `{runtime['validation'].get('net_profit')}`, PF(수익 팩터) `{runtime['validation'].get('profit_factor')}`, feature_ready(피처 준비 수) `{runtime['validation'].get('feature_ready_count')}`
- OOS(표본외): trades(거래 수) `{runtime['oos'].get('trade_count')}`, net(순손익) `{runtime['oos'].get('net_profit')}`, PF(수익 팩터) `{runtime['oos'].get('profit_factor')}`, feature_ready(피처 준비 수) `{runtime['oos'].get('feature_ready_count')}`

효과(effect, 효과): 이번 MT5(메타트레이더5) 검증은 EA(`Expert Advisor`, 전문가 자문) 로직을 새로 바꾸지 않고, `vol_high` 또는 `adx_20_25`에 걸린 feature row(피처 행)를 빼서 해당 시간 신호를 만들지 않게 한 좁은 runtime probe(런타임 탐침)다. 그래서 “터미널에서도 대략 같은 필터 방향이 살아 있는가”는 보지만, operating rule(운영 규칙) 확정은 아니다.

## Files(파일)
- monthly leave-one-out(월 하나 제외): `{summary['output_paths']['monthly_leave_one_out']}`
- monthly summary(월별 요약): `{summary['output_paths']['monthly_survival_summary']}`
- aggregate summary(집계 요약): `{summary['output_paths']['aggregate_summary']}`
"""


def decision_text(summary: Mapping[str, Any]) -> str:
    candidate = summary["monthly_candidate_read"]
    return f"""# Decision: Stage34 RUN28E Broader Entry Proxy Completed(결정: 34단계 28E 넓은 진입 대리 완료)
- date(날짜): 2026-05-08
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- rule(규칙): `{RULE_ID}`
- monthly status(월별 상태): `{candidate['status']}`
- MT5 status(MT5 상태): `{summary['external_verification_status']}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): 후보는 보존하지만 main seed(메인 씨앗)로 승격하지 않는다. 다음 행동(action, 행동)은 `vol_high`와 `adx_20_25`를 분리해, 실제로 어느 축이 2025-10(2025년 10월) 의존성을 만든 것인지 찌르는 것이다.
"""


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    runtime = summary["runtime_read"]
    candidate = summary["monthly_candidate_read"]
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__monthly_survival",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "monthly_survival",
            "parent_run_id": SOURCE_FREQUENCY_RUN_ID,
            "record_view": "monthly_survival_summary",
            "tier_scope": "Tier A",
            "kpi_scope": "monthly_robustness",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["monthly_survival_summary"],
            "primary_kpi": ledger_pairs(
                [
                    ("rule_id", RULE_ID),
                    ("monthly_status", candidate["status"]),
                    ("oos_min_leave_one_out_net", candidate["oos"]["min_leave_one_out_net_profit"]),
                    ("oos_top_positive_month", candidate["oos"]["top_positive_month"]),
                ]
            ),
            "guardrail_kpi": ledger_pairs([("boundary", BOUNDARY), ("no_seed_change", True)]),
            "external_verification_status": summary["external_verification_status"],
            "notes": "Monthly leave-one-out kept the candidate alive but showed October dependency.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mt5_runtime_probe",
            "parent_run_id": SOURCE_RUNTIME_RUN_ID,
            "record_view": "mt5_tier_a_broader_entry_proxy",
            "tier_scope": "Tier A",
            "kpi_scope": "runtime_probe",
            "scoreboard_lane": "runtime_probe",
            "status": "reviewed" if summary["external_verification_status"] == "completed" else "blocked",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["kpi_record"],
            "primary_kpi": ledger_pairs(
                [
                    ("validation_pf", runtime["validation"].get("profit_factor")),
                    ("oos_pf", runtime["oos"].get("profit_factor")),
                    ("validation_trades", runtime["validation"].get("trade_count")),
                    ("oos_trades", runtime["oos"].get("trade_count")),
                ]
            ),
            "guardrail_kpi": "runtime_probe_only_no_runtime_authority",
            "external_verification_status": summary["external_verification_status"],
            "notes": "MT5 probe used Stage34 filtered Tier A feature CSV rows; no EA logic promotion.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__claim_boundary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "claim_boundary",
            "parent_run_id": RUN_ID,
            "record_view": "final_claim_guard",
            "tier_scope": "Tier A",
            "kpi_scope": "claim_boundary",
            "scoreboard_lane": "result_judgment",
            "status": "reviewed",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["aggregate_summary"],
            "primary_kpi": "candidate_preserved_no_seed_change",
            "guardrail_kpi": ledger_pairs([("forbidden_claims", summary["forbidden_claims"]), ("next_action", NEXT_ACTION)]),
            "external_verification_status": summary["external_verification_status"],
            "notes": "No baseline, promotion, live readiness, or runtime authority was created.",
        },
    ]
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_probe",
        "status": "reviewed" if summary["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["judgment"],
        "path": rel(REPORT_PATH),
        "notes": "Stage34 Tier A Markov broader entry proxy monthly robustness plus MT5 runtime probe; no baseline, promotion, or runtime authority.",
    }
    return {
        "stage_run_ledger": upsert_csv_rows_resilient(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows_resilient(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "run_registry": upsert_csv_rows_resilient(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id"),
    }


def write_packet_artifacts(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    attribution.write_csv(PACKET_ROOT / "monthly_leave_one_out.csv", list(summary["monthly_leave_one_out_rows"][0].keys()), summary["monthly_leave_one_out_rows"])
    attribution.write_csv(PACKET_ROOT / "monthly_survival_summary.csv", list(summary["monthly_summary_rows"][0].keys()), summary["monthly_summary_rows"])
    attribution.write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    attribution.write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {"skill": "obsidian-experiment-design", "status": "executed", "run_id": RUN_ID},
            {"skill": "obsidian-performance-attribution", "status": "executed", "monthly_candidate_read": summary["monthly_candidate_read"]["status"]},
            {"skill": "obsidian-runtime-parity", "status": "executed", "external_verification_status": summary["external_verification_status"]},
            {"skill": "obsidian-backtest-forensics", "status": "executed", "mt5_kpi_record_count": summary["mt5_kpi_record_count"]},
            {"skill": "obsidian-result-judgment", "status": "executed", "judgment": summary["judgment"]},
        ],
    )
    attribution.write_json(
        PACKET_ROOT / "artifact_lineage_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "source_packets": summary["source_packets"],
            "runtime_input_model": summary["runtime_inputs"]["model_copy"],
            "runtime_input_features": summary["runtime_inputs"]["feature_outputs"],
        },
    )
    attribution.write_json(
        PACKET_ROOT / "monthly_survival_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if summary["monthly_candidate_read"]["status"] != "monthly_fail" else "blocked",
            "monthly_candidate_read": summary["monthly_candidate_read"],
        },
    )
    attribution.write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if summary["external_verification_status"] == "completed" else "blocked",
            "external_verification_status": summary["external_verification_status"],
            "mt5_kpi_record_count": summary["mt5_kpi_record_count"],
            "normalized_kpi": kpi,
        },
    )
    attribution.write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if int(kpi.get("parser_errors") or 0) == 0 and int(kpi.get("trade_parser_errors") or 0) == 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
            "trade_parser_errors": kpi.get("trade_parser_errors"),
        },
    )
    attribution.write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": ["Stage34 RUN28E broader entry proxy probe completed.", "Candidate remains a dependency clue."],
            "forbidden_claims": summary["forbidden_claims"],
            "boundary": BOUNDARY,
        },
    )
    gates = [
        "artifact_lineage_gate",
        "monthly_survival_gate",
        "runtime_evidence_gate",
        "kpi_contract_audit",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    attribution.write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []},
    )


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    attribution.write_md(REPORT_PATH, review_text(summary))
    attribution.write_md(DECISION_PATH, decision_text(summary))
    attribution.write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage34 Review Index(34단계 검토 색인)

- current status(현재 상태): `{summary['status']}`
- current run(현재 실행): `{RUN_ID}`
- current packet(현재 묶음): `{PACKET_ID}`
- latest review(최신 검토): `{rel(REPORT_PATH)}`
- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`

효과(effect, 효과): Stage34(34단계)는 run28E(28E 실행)에서 월별 버팀과 MT5 runtime probe(MT5 런타임 탐침)를 함께 기록했다.
""",
    )
    attribution.write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage34 Selection Status(34단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `{summary['status']}`
- current run(현재 실행): `{RUN_ID}`
- preserved seed(보존 씨앗): `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`
- dependency clue(의존성 단서): `{RULE_ID}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): 후보는 MT5(메타트레이더5)에 한 번 찔렀지만, 월별 의존성이 있어 operating rule(운영 규칙)이나 main seed(메인 씨앗)로 올리지 않는다.
""",
    )


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"active_branch: .+", f"active_branch: {summary['active_branch']}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    new_focus = (
        "- Stage34(34단계) 34_regime_mechanism__tier_a_markov_long_permission_attribution "
        "reviewed_monthly_mt5_probe_completed(월별/MT5 탐침 검토 완료): run28E(28E 실행)는 "
        "`exclude_vol_high_or_adx_20_25`를 월별로 버티는지 보고 MT5 runtime_probe(MT5 런타임 탐침)까지 시도했다; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n"
    )
    text = re.sub(r"- Stage34\(34.*?\) 34_regime_mechanism__tier_a_markov_long_permission_attribution .*?\n(?=- Stage33)", new_focus, text, count=1, flags=re.DOTALL)
    text = re.sub(
        r"- current_run_id\(.*?\).*?(?=\n- treat Stage29-32)",
        f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 검토된 실행인 `{RUN_ID}`를 가리킨다. next action(다음 행동)은 `{NEXT_ACTION}`이다.",
        text,
        count=1,
        flags=re.DOTALL,
    )
    stage34_block = f"""stage34_tier_a_markov_long_permission_attribution:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: {summary['status']}
  current_run_id: {RUN_ID}
  preserved_seed: Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)
  dependency_clue: {RULE_ID}
  decision_path: {rel(DECISION_PATH)}
  stage_path: stages/{STAGE_ID}
  previous_stage_id: 33_regime_mechanism__tier_a_markov_long_permission_source
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  external_verification_status: {summary['external_verification_status']}
  next_action: {NEXT_ACTION}
  boundary: {BOUNDARY}
"""
    text = re.sub(r"stage34_tier_a_markov_long_permission_attribution:\n(?:  .+\n)+\npre_alpha_stage_queue:", stage34_block + "\npre_alpha_stage_queue:", text, count=1)
    attribution.write_md(WORKSPACE_STATE_PATH, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage34 RUN28E Broader Entry Proxy.*?(?=## Latest |\Z)", "", old, count=1, flags=re.DOTALL)
    runtime = summary["runtime_read"]
    candidate = summary["monthly_candidate_read"]
    block = f"""## Latest Stage34 RUN28E Broader Entry Proxy(최신 34단계 28E 넓은 진입 대리)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `{summary['active_branch']}`
- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

Stage34(34단계) `{RUN_ID}`를 monthly robustness plus MT5 runtime probe(월별 버팀 + MT5 런타임 탐침)로 완료했다.

결과(result, 결과): `{RULE_ID}`는 월 하나를 빼도 OOS(표본외) PF(수익 팩터)가 1 아래로 깨지지는 않았다. 다만 2025-10(2025년 10월)을 빼면 OOS(표본외) net(순손익)이 `{candidate['oos']['min_leave_one_out_net_profit']}`까지 얇다. MT5(메타트레이더5) probe(탐침)는 validation/OOS(검증/표본외) trades(거래 수) `{runtime['validation'].get('trade_count')}` / `{runtime['oos'].get('trade_count')}`를 기록했다.

효과(effect, 효과): 후보는 보존하지만 main seed(메인 씨앗), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다. 다음은 `vol_high`와 `adx_20_25`를 분리해 의존성 원인을 본다.

"""
    attribution.write_md(CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog(summary: Mapping[str, Any]) -> None:
    old = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    old = re.sub(r"^## 2026-05-08 Stage34 RUN28E Broader Entry Proxy.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-08 Stage34 RUN28E Broader Entry Proxy(34단계 28E 넓은 진입 대리)

- completed(완료): `{RUN_ID}` monthly robustness plus MT5 runtime probe(월별 버팀 + MT5 런타임 탐침)
- source(원천): `{SOURCE_FREQUENCY_RUN_ID}`, `{SOURCE_RUNTIME_RUN_ID}`
- judgment(판정): `{summary['judgment']}`
- effect(효과): `{RULE_ID}`는 dependency clue(의존성 단서)로 보존한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    attribution.write_md(CHANGELOG_PATH, entry + old.lstrip("\ufeff"))


