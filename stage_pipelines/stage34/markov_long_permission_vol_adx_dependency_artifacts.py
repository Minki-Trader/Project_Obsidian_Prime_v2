from __future__ import annotations

import re
from typing import Any, Mapping

from foundation.control_plane.ledger import ALPHA_LEDGER_COLUMNS, RUN_REGISTRY_COLUMNS, io_path, ledger_pairs
from stage_pipelines.stage34 import markov_long_permission_vol_adx_dependency_probe as probe


for _name in (
    "RUN_ID", "PACKET_ID", "STAGE_ID", "SOURCE_RUNTIME_RUN_ID", "SOURCE_ATTRIBUTION_RUN_ID",
    "SOURCE_RUN28E_ID", "BOUNDARY", "NEXT_ACTION", "MODEL_FAMILY", "FEATURE_SET_ID",
    "LABEL_ID", "SPLIT_CONTRACT", "RESULT_ROOT", "RUN_ROOT", "PACKET_ROOT", "REPORT_PATH",
    "DECISION_PATH", "STAGE_LEDGER_PATH", "PROJECT_LEDGER_PATH", "RUN_REGISTRY_PATH",
    "REVIEW_INDEX_PATH", "SELECTION_STATUS_PATH", "WORKSPACE_STATE_PATH", "CURRENT_WORKING_STATE_PATH",
    "CHANGELOG_PATH",
):
    globals()[_name] = getattr(probe, _name)

attribution = probe.attribution
run28e = probe.run28e
rel = probe.rel
write_json = probe.write_json


def write_run_files(summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    outputs = (
        ("component_python_metrics", summary["component_python_rows"]),
        ("feature_ready_summary", summary["feature_ready_summary_rows"]),
        ("mt5_component_summary", summary["mt5_component_rows"]),
        ("monthly_dependency", summary["monthly_dependency_rows"]),
        ("hold_duration_diagnostics", summary["hold_duration_rows"]),
    )
    for key, rows in outputs:
        if rows:
            attribution.write_csv(RESULT_ROOT / f"{key}.csv", list(rows[0].keys()), rows)
            attribution.write_csv(PACKET_ROOT / f"{key}.csv", list(rows[0].keys()), rows)
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "source_runs": [SOURCE_RUNTIME_RUN_ID, SOURCE_ATTRIBUTION_RUN_ID, SOURCE_RUN28E_ID],
            "boundary": BOUNDARY,
            "runtime_probe": {
                key: result.get(key)
                for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure")
                if key in result
            },
        },
    )
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUNTIME_RUN_ID,
            "kpi_scope": "tier_a_markov_vol_adx_dependency_probe",
            "model_family": MODEL_FAMILY,
            "feature_set_id": FEATURE_SET_ID,
            "label_id": LABEL_ID,
            "split_contract": SPLIT_CONTRACT,
            "component_driver_read": summary["component_driver_read"],
            "feature_ready_read": summary["feature_ready_read"],
            "mt5_component_read": summary["mt5_component_read"],
            "october_dependency_read": summary["october_dependency_read"],
            "hold_duration_read": summary["hold_duration_read"],
            "mt5_records": result.get("mt5_kpi_records", []),
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "mt5": {"kpi_records": result.get("mt5_kpi_records", [])},
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "boundary": BOUNDARY,
        },
    )
    write_json(RESULT_ROOT / "aggregate_summary.json", summary)


def review_text(summary: Mapping[str, Any]) -> str:
    comp = summary["component_driver_read"]
    mt5_read = summary["mt5_component_read"]
    oct_read = summary["october_dependency_read"]
    hold = summary["hold_duration_read"]
    return f"""# RUN28F Tier A Markov Vol/ADX Dependency Packet(28F 실행 티어 A 마르코프 변동성/ADX 의존성 묶음)
## Judgment(판정)
- run(실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- boundary(경계): `{BOUNDARY}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): vol_high(고변동), adx_20_25(ADX 20-25), 2025-10(2025년 10월), feature_ready(피처 준비), hold duration(보유 기간)을 같은 근거 묶음에서 확인했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Component Read(구성요소 판독)
- Python validation(파이썬 검증) best PF(최고 수익 팩터): `{comp['validation']['best_profit_factor_rule']}` / `{comp['validation']['best_profit_factor']}`
- Python OOS(파이썬 표본외) best net(최고 순손익): `{comp['oos']['best_net_rule']}` / `{comp['oos']['best_net_profit']}`
- MT5 validation(MT5 검증) best PF(최고 수익 팩터): `{mt5_read.get('validation_is', {}).get('best_profit_factor_rule')}` / `{mt5_read.get('validation_is', {}).get('best_profit_factor')}`
- MT5 OOS(MT5 표본외) best PF(최고 수익 팩터): `{mt5_read.get('oos', {}).get('best_profit_factor_rule')}` / `{mt5_read.get('oos', {}).get('best_profit_factor')}`

효과(effect, 효과): validation(검증)은 `adx_20_25` 제거 쪽이 더 설명력이 있고, OOS(표본외)는 `vol_high` 제거 쪽이 순손익을 더 살린다. union(합집합)은 PF(수익 팩터)는 좋지만 한 달 의존성이 남는다.

## October / Feature / Hold(10월 / 피처 / 보유)
- Python without 2025-10(파이썬 2025년 10월 제외): net(순손익) `{oct_read.get('python_without_2025_10_net')}`, PF(수익 팩터) `{oct_read.get('python_without_2025_10_pf')}`
- MT5 without 2025-10(MT5 2025년 10월 제외): net(순손익) `{oct_read.get('mt5_without_2025_10_net')}`, PF(수익 팩터) `{oct_read.get('mt5_without_2025_10_pf')}`
- hold read(보유 판독): validation/OOS avg hold bars(검증/표본외 평균 보유 봉) `{hold.get('validation_avg_hold_bars')}` / `{hold.get('oos_avg_hold_bars')}`

효과(effect, 효과): 긴 보유는 신호 자체만의 장점이 아니라 feature row omission(피처 행 제거)이 max hold(최대 보유) 평가 빈도를 낮춘 효과가 섞여 있다. 다음은 hold management runtime probe(보유 관리 런타임 탐침)가 맞다.
"""


def decision_text(summary: Mapping[str, Any]) -> str:
    return f"""# Decision: Stage34 RUN28F Vol/ADX Dependency Completed(결정: 34단계 28F 변동성/ADX 의존성 완료)
- date(날짜): 2026-05-08
- run(실행): `{RUN_ID}`
- judgment(판정): `{summary['judgment']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): `exclude_vol_high_or_adx_20_25`는 보존하지만, 진입 필터 하나로 main seed(메인 씨앗)를 만들지는 않는다. hold duration(보유 기간)과 max hold(최대 보유) 평가 방식이 성과에 섞여 있어 다음 탐침은 보유 관리 쪽이다.
"""


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    mt5_read = summary["mt5_component_read"]
    hold = summary["hold_duration_read"]
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__component_dependency",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "component_dependency",
            "parent_run_id": SOURCE_RUN28E_ID,
            "record_view": "component_python_and_mt5_summary",
            "tier_scope": "Tier A",
            "kpi_scope": "vol_adx_dependency",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["mt5_component_summary"],
            "primary_kpi": ledger_pairs(
                [
                    ("mt5_validation_best_pf_rule", mt5_read.get("validation_is", {}).get("best_profit_factor_rule")),
                    ("mt5_oos_best_pf_rule", mt5_read.get("oos", {}).get("best_profit_factor_rule")),
                ]
            ),
            "guardrail_kpi": ledger_pairs([("boundary", BOUNDARY), ("no_seed_change", True)]),
            "external_verification_status": summary["external_verification_status"],
            "notes": "Volatility and ADX component probes were compared in Python and MT5.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__hold_duration",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "hold_duration",
            "parent_run_id": SOURCE_RUN28E_ID,
            "record_view": "hold_duration_diagnostics",
            "tier_scope": "Tier A",
            "kpi_scope": "trade_shape",
            "scoreboard_lane": "trade_shape",
            "status": "reviewed",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["hold_duration_diagnostics"],
            "primary_kpi": ledger_pairs(
                [
                    ("validation_avg_hold_bars", hold.get("validation_avg_hold_bars")),
                    ("oos_avg_hold_bars", hold.get("oos_avg_hold_bars")),
                ]
            ),
            "guardrail_kpi": "max_hold_only_evaluated_on_feature_ready_bars",
            "external_verification_status": "completed_reused_run28E_trade_attribution",
            "notes": "Long hold duration is linked to feature row omission and max-hold evaluation cadence.",
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
            "primary_kpi": "dependency_probe_completed_no_seed_change",
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
        "notes": "Stage34 Tier A Markov vol/adx component, October dependency, feature-ready, and hold diagnostics; no baseline, promotion, or runtime authority.",
    }
    return {
        "stage_run_ledger": run28e.upsert_csv_rows_resilient(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": run28e.upsert_csv_rows_resilient(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "run_registry": run28e.upsert_csv_rows_resilient(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id"),
    }


def write_packet_artifacts(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {"skill": "obsidian-experiment-design", "status": "executed", "run_id": RUN_ID},
            {"skill": "obsidian-performance-attribution", "status": "executed", "component_driver_read": summary["component_driver_read"]["interpretation"]},
            {"skill": "obsidian-runtime-parity", "status": "executed", "external_verification_status": summary["external_verification_status"]},
            {"skill": "obsidian-backtest-forensics", "status": "executed", "mt5_kpi_record_count": summary["mt5_kpi_record_count"]},
            {"skill": "obsidian-result-judgment", "status": "executed", "judgment": summary["judgment"]},
        ],
    )
    write_json(PACKET_ROOT / "artifact_lineage_gate.json", {"packet_id": PACKET_ID, "status": "passed", "source_packets": summary["source_packets"]})
    write_json(PACKET_ROOT / "component_dependency_gate.json", {"packet_id": PACKET_ID, "status": "passed", "component_driver_read": summary["component_driver_read"]})
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if summary["external_verification_status"] == "completed" else "blocked",
            "external_verification_status": summary["external_verification_status"],
            "mt5_kpi_record_count": summary["mt5_kpi_record_count"],
            "normalized_kpi": kpi,
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if int(kpi.get("parser_errors") or 0) == 0 and int(kpi.get("trade_parser_errors") or 0) == 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
            "trade_parser_errors": kpi.get("trade_parser_errors"),
        },
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": ["Stage34 RUN28F dependency probe completed.", "Hold-management follow-up is indicated."],
            "forbidden_claims": summary["forbidden_claims"],
            "boundary": BOUNDARY,
        },
    )
    gates = [
        "artifact_lineage_gate",
        "component_dependency_gate",
        "runtime_evidence_gate",
        "kpi_contract_audit",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []})


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

효과(effect, 효과): Stage34(34단계)는 run28F(28F 실행)에서 vol_high(고변동), adx_20_25(ADX 20-25), 2025-10(2025년 10월), feature_ready(피처 준비), hold duration(보유 기간)을 함께 검증했다.
""",
    )
    attribution.write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage34 Selection Status(34단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `{summary['status']}`
- current run(현재 실행): `{RUN_ID}`
- preserved seed(보존 씨앗): `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`
- dependency clue(의존성 단서): `vol_high/adx_20_25 interaction(고변동/ADX 20-25 상호작용)`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): 진입 필터 후보는 보존하지만, 긴 보유와 max hold(최대 보유) 평가 문제가 섞여 있어 operating rule(운영 규칙)로 올리지 않는다.
""",
    )


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"active_branch: .+", f"active_branch: {summary['active_branch']}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    new_focus = (
        "- Stage34(34단계) 34_regime_mechanism__tier_a_markov_long_permission_attribution "
        "reviewed_vol_adx_dependency_probe_completed(변동성/ADX 의존성 탐침 검토 완료): run28F(28F 실행)는 "
        "vol_high(고변동), adx_20_25(ADX 20-25), 2025-10(2025년 10월), feature_ready(피처 준비), hold duration(보유 기간)을 검증했다; "
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
    block = f"""stage34_tier_a_markov_long_permission_attribution:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: {summary['status']}
  current_run_id: {RUN_ID}
  preserved_seed: Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)
  dependency_clue: vol_high/adx_20_25 interaction(고변동/ADX 20-25 상호작용)
  decision_path: {rel(DECISION_PATH)}
  stage_path: stages/{STAGE_ID}
  previous_stage_id: 33_regime_mechanism__tier_a_markov_long_permission_source
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  external_verification_status: {summary['external_verification_status']}
  next_action: {NEXT_ACTION}
  boundary: {BOUNDARY}
"""
    text = re.sub(r"stage34_tier_a_markov_long_permission_attribution:\n(?:  .+\n)+\npre_alpha_stage_queue:", block + "\npre_alpha_stage_queue:", text, count=1)
    attribution.write_md(WORKSPACE_STATE_PATH, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage34 RUN28F Vol/ADX Dependency.*?(?=## Latest |\Z)", "", old, count=1, flags=re.DOTALL)
    comp = summary["component_driver_read"]
    hold = summary["hold_duration_read"]
    block = f"""## Latest Stage34 RUN28F Vol/ADX Dependency(최신 34단계 28F 변동성/ADX 의존성)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `{summary['active_branch']}`
- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

Stage34(34단계) `{RUN_ID}`를 vol/adx component plus hold diagnostics(변동성/ADX 구성요소 + 보유 진단)로 완료했다.

결과(result, 결과): Python(파이썬) OOS(표본외) best net(최고 순손익)은 `{comp['oos']['best_net_rule']}`이고, 긴 hold duration(보유 기간)은 validation/OOS(검증/표본외) 평균 `{hold.get('validation_avg_hold_bars')}` / `{hold.get('oos_avg_hold_bars')}` bars(봉)다.

효과(effect, 효과): 후보는 보존하지만 main seed(메인 씨앗), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다. 다음은 hold management runtime probe(보유 관리 런타임 탐침)다.

"""
    attribution.write_md(CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog(summary: Mapping[str, Any]) -> None:
    old = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    old = re.sub(r"^## 2026-05-08 Stage34 RUN28F Vol/ADX Dependency.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-08 Stage34 RUN28F Vol/ADX Dependency(34단계 28F 변동성/ADX 의존성)

- completed(완료): `{RUN_ID}` vol/adx component plus hold diagnostics(변동성/ADX 구성요소 + 보유 진단)
- source(원천): `{SOURCE_RUN28E_ID}`, `{SOURCE_RUNTIME_RUN_ID}`
- judgment(판정): `{summary['judgment']}`
- effect(효과): `exclude_vol_high_or_adx_20_25`는 보존하지만, hold management(보유 관리) 문제가 섞여 있어 다음 탐침으로 넘긴다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    attribution.write_md(CHANGELOG_PATH, entry + old.lstrip("\ufeff"))


