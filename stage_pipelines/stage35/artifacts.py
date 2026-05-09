from __future__ import annotations

import re
from typing import Any, Mapping, Sequence

from stage_pipelines.stage35 import atlas_config as cfg
from stage_pipelines.stage35 import common


def _mt5_rows(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        rows.append(
            {
                "topic_id": record.get("source_topic_id"),
                "record_view": record.get("record_view"),
                "split": record.get("split"),
                "state_direction": record.get("state_direction"),
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


def _mt5_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    read: dict[str, Any] = {"by_topic": {}}
    for topic in cfg.TOPICS:
        topic_rows = [row for row in rows if row["topic_id"] == topic.topic_id]
        read["by_topic"][topic.topic_id] = {
            str(row["split"]): {
                "trade_count": row.get("trade_count"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "status": row.get("status"),
            }
            for row in topic_rows
        }
    return read


def build_summary(
    *,
    created_at: str,
    branch: str,
    atlas: Mapping[str, Any],
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
        "idea_id": cfg.IDEA_ID,
        "created_at_utc": created_at,
        "active_branch": branch,
        "status": "reviewed_unsupervised_atlas_mt5_probe_completed" if completed else "blocked_unsupervised_atlas_mt5_probe_after_attempt",
        "judgment": cfg.JUDGMENT_COMPLETED if completed else cfg.JUDGMENT_BLOCKED,
        "boundary": cfg.BOUNDARY,
        "selected_topics": atlas["selections"],
        "state_summary_row_count": len(atlas["state_rows"]),
        "data_identity": atlas["data_identity"],
        "runtime_inputs": runtime_inputs,
        "external_verification_status": result.get("external_verification_status"),
        "mt5_attempt_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "mt5_rows": mt5_rows,
        "mt5_read": _mt5_read(mt5_rows),
        "known_runtime_difference": runtime_inputs.get("known_runtime_difference"),
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "next_action": "continue_stage35_with_extreme_sweep_or_close_if_user_requests",
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority", "live_readiness"],
        "output_paths": {
            "state_summary": common.rel(cfg.RESULT_ROOT / "atlas_state_summary.csv"),
            "selected_states": common.rel(cfg.RESULT_ROOT / "atlas_selected_states.csv"),
            "mt5_summary": common.rel(cfg.RESULT_ROOT / "mt5_runtime_summary.csv"),
            "aggregate_summary": common.rel(cfg.PACKET_ROOT / "aggregate_summary.json"),
            "run_manifest": common.rel(cfg.RUN_ROOT / "run_manifest.json"),
            "kpi_record": common.rel(cfg.RUN_ROOT / "kpi_record.json"),
            "report": common.rel(cfg.REPORT_PATH),
        },
    }


def write_run_files(summary: Mapping[str, Any], result: Mapping[str, Any], atlas: Mapping[str, Any]) -> None:
    common.write_csv(cfg.RESULT_ROOT / "atlas_state_summary.csv", atlas["state_rows"])
    common.write_csv(cfg.RESULT_ROOT / "atlas_selected_states.csv", atlas["selections"])
    common.write_csv(cfg.RESULT_ROOT / "mt5_runtime_summary.csv", summary["mt5_rows"])
    common.write_json(cfg.RESULT_ROOT / "atlas_model_manifest.json", atlas["model_payloads"])
    common.write_json(cfg.RUN_ROOT / "run_manifest.json", {
        "packet_id": cfg.PACKET_ID,
        "stage_id": cfg.STAGE_ID,
        "run_id": cfg.RUN_ID,
        "run_number": cfg.RUN_NUMBER,
        "boundary": cfg.BOUNDARY,
        "attempts": result.get("attempts", []),
        "runtime_probe": {
            "common_copies": result.get("common_copies", []),
            "compile": result.get("compile", {}),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "failure": result.get("failure"),
        },
    })
    common.write_json(cfg.RUN_ROOT / "kpi_record.json", {
        "run_id": cfg.RUN_ID,
        "stage_id": cfg.STAGE_ID,
        "kpi_scope": "unsupervised_atlas_mt5_runtime_probe",
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
    })
    common.write_json(cfg.RESULT_ROOT / "aggregate_summary.json", summary)
    common.write_json(cfg.PACKET_ROOT / "aggregate_summary.json", summary)
    common.write_json(cfg.PACKET_ROOT / "result_judgment_gate.json", {
        "packet_id": cfg.PACKET_ID,
        "status": "passed_with_boundary" if summary["external_verification_status"] == "completed" else "blocked_after_attempt",
        "judgment": summary["judgment"],
        "allowed_claims": ["Stage35 opened", "run29A atlas probe attempted", "MT5 runtime probe recorded if completed"],
        "forbidden_claims": summary["forbidden_claims"],
    })


def _topic_lines(summary: Mapping[str, Any]) -> str:
    lines = []
    for selection in summary["selected_topics"]:
        lines.append(
            f"- `{selection['topic_id']}`: state(상태) `{selection['selected_state_id']}`, "
            f"direction(방향) `{selection['state_direction']}`, validation rows(검증 행) `{selection['validation_row_count']}`"
        )
    return "\n".join(lines)


def _mt5_table(summary: Mapping[str, Any]) -> str:
    lines = [
        "| topic(주제) | split(분할) | direction(방향) | trades(거래) | net(순손익) | PF(수익 팩터) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary["mt5_rows"]:
        lines.append(
            f"| `{row.get('topic_id')}` | `{row.get('split')}` | `{row.get('state_direction')}` | "
            f"`{row.get('trade_count')}` | `{row.get('net_profit')}` | `{row.get('profit_factor')}` |"
        )
    return "\n".join(lines)


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    common.write_md(
        cfg.STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage35 Context Map: Unsupervised Market State Atlas(35단계 문맥 지도: 비지도 시장 상태 지도)

## Core Question(핵심 질문)

Label(라벨) 없이 market state atlas(시장 상태 지도)를 만들면 US100 M5(나스닥100 5분봉)의 반복 가능한 상태를 나눌 수 있는가?

효과(effect, 효과): Stage34(34단계)의 Markov long permission(마르코프 롱 허용) 꼬리를 잇지 않고, 새 price/context structure(가격/문맥 구조)를 다섯 개 독립 축으로 본다.

## Five Non-Overlapping Topics(겹치지 않는 5개 주제)

{_topic_lines(summary)}

## Boundary(경계)

`{cfg.BOUNDARY}`

baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
""",
    )
    common.write_md(
        cfg.STAGE_ROOT / "01_inputs" / "run29A_input_manifest.md",
        f"""# RUN29A Input Manifest(RUN29A 입력 목록)

- source dataset(원천 데이터셋): `{summary['data_identity']['path']}`
- dataset sha256(데이터셋 해시): `{summary['data_identity']['sha256']}`
- rows(행): `{summary['data_identity']['rows']}`
- timestamp range(시간 범위): `{summary['data_identity']['timestamp_min']}` to `{summary['data_identity']['timestamp_max']}`
- feature order hash(피처 순서 해시): `{summary['data_identity']['feature_order_hash']}`

효과(effect, 효과): Stage35(35단계)의 atlas(지도)가 어떤 입력에서 만들어졌는지 닫힌 계보(lineage, 계보)로 남긴다.
""",
    )
    common.write_md(
        cfg.REPORT_PATH,
        f"""# RUN29A Unsupervised Market State Atlas MT5 Probe(RUN29A 비지도 시장 상태 지도 MT5 탐침)

- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- MT5 attempts(MT5 시도): `{summary['mt5_attempt_count']}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary['mt5_kpi_record_count']}`

## Selected Atlas States(선택된 지도 상태)

{_topic_lines(summary)}

## MT5 Runtime Read(MT5 런타임 판독)

{_mt5_table(summary)}

정규화 KPI(normalized KPI, 정규화 핵심 성과 지표): records(기록) `{summary.get('kpi_management', {}).get('normalized_records')}`, parser errors(파서 오류) `{summary.get('kpi_management', {}).get('parser_errors')}`.

## Runtime Parity Boundary(런타임 동등성 경계)

Python(파이썬)이 cluster state(군집 상태)를 미리 계산했고, MT5(메타트레이더5)는 selected state row(선택 상태 행)만 받은 feature CSV(피처 CSV)를 실행했다.

효과(effect, 효과): 터미널에서 그 시간대만 거래했을 때의 runtime probe(런타임 탐침)는 보지만, native clustering runtime authority(원본 군집 런타임 권위)는 아니다.

## Forbidden Claims(금지 주장)

`edge(거래 우위)`, `alpha_quality(알파 품질)`, `baseline(기준선)`, `promotion(승격)`, `runtime_authority(런타임 권위)`, `live_readiness(실거래 준비)`.
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

효과(effect, 효과): Stage35(35단계)는 열렸고 RUN29A(29A 실행)는 기록됐지만, 아직 선택된 운영 의미는 없다.
""",
    )
    common.write_md(
        cfg.DECISION_PATH,
        f"""# 2026-05-09 Stage35 Open and RUN29A(35단계 개방 및 RUN29A)

## Decision(결정)

Stage35(35단계) `{cfg.STAGE_ID}`를 open(개방)하고 `{cfg.RUN_ID}`를 실행 묶음으로 기록한다.

효과(effect, 효과): Stage34(34단계)를 이어 파지 않고, unsupervised market state atlas(비지도 시장 상태 지도)라는 새 주제(topic pivot, 주제 전환)로 이동한다.

## Result Boundary(결과 경계)

- judgment(판정): `{summary['judgment']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- boundary(경계): `{cfg.BOUNDARY}`

baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
""",
    )


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    run_rows = [{
        "run_id": cfg.RUN_ID,
        "stage_id": cfg.STAGE_ID,
        "lane": "runtime_probe",
        "status": "reviewed" if summary["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["judgment"],
        "path": common.rel(cfg.RUN_ROOT),
        "notes": "Stage35 unsupervised market state atlas five-topic MT5 row-omission runtime probe; no baseline/promotion/runtime authority.",
    }]
    ledger_rows = []
    for row in summary["mt5_rows"]:
        ledger_rows.append({
            "ledger_row_id": f"{cfg.RUN_ID}__{row['record_view']}",
            "stage_id": cfg.STAGE_ID,
            "run_id": cfg.RUN_ID,
            "subrun_id": row["record_view"],
            "parent_run_id": "",
            "record_view": row["record_view"],
            "tier_scope": "Tier A",
            "kpi_scope": "unsupervised_atlas_mt5_runtime_probe",
            "scoreboard_lane": "runtime_probe",
            "status": row.get("status"),
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["mt5_summary"],
            "primary_kpi": common.ledger_pairs([("net_profit", row.get("net_profit")), ("profit_factor", row.get("profit_factor")), ("trade_count", row.get("trade_count"))]),
            "guardrail_kpi": common.ledger_pairs([("topic_id", row.get("topic_id")), ("state_direction", row.get("state_direction")), ("boundary", cfg.BOUNDARY)]),
            "external_verification_status": summary["external_verification_status"],
            "notes": "Actual MT5 tester row for one selected unsupervised atlas state; row omission is a handoff probe.",
        })
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
        f"- Stage35(35단계) {cfg.STAGE_ID} {summary['status']}: RUN29A(29A 실행)는 "
        "label 없이 다섯 개 non-overlapping atlas topics(비중복 지도 주제)를 만들고 MT5 runtime probe(MT5 런타임 탐침)를 기록했다; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n"
    )
    text = re.sub(r"- Stage35\(35단계\).*?\n", "", text)
    text = re.sub(r"current_focus:\n", "current_focus:\n" + focus, text, count=1)
    text = re.sub(
        r"- Stage34\(34단계\) 34_regime_mechanism__tier_a_markov_long_permission_attribution .*?\n",
        "- Stage34(34단계) 34_regime_mechanism__tier_a_markov_long_permission_attribution reviewed_closed(검토 후 닫힘): run28A-run28F(28A-28F 실행)는 Tier A Markov long permission(티어 A 마르코프 롱 허용)의 귀속/구간/월별/MT5(메타트레이더5) 근거를 남겼고, Stage35(35단계)는 별도 topic pivot(주제 전환)으로 열렸다; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n",
        text,
        count=1,
    )
    text = re.sub(
        r"- current_run_id\(현재 실행 ID\).*?\n",
        f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 실행인 `{cfg.RUN_ID}`를 가리킨다. next action(다음 행동)은 `{summary['next_action']}`이다.\n",
        text,
        count=1,
    )
    text = text.replace(
        "- 'next action(다음 행동): open a new stage/topic(새 단계/주제) only when requested; Stage20-32\n  goal(20-32단계 목표)은 complete(완료)'",
        "- 'next action(다음 행동): continue Stage35(35단계) only by explicit user request(명시 사용자 요청); Stage20-32\n  goal(20-32단계 목표)은 complete(완료)'",
        1,
    )
    block = f"""stage35_unsupervised_market_state_atlas:
  packet_id: {cfg.PACKET_ID}
  stage_id: {cfg.STAGE_ID}
  status: {summary['status']}
  current_run_id: {cfg.RUN_ID}
  idea_id: {cfg.IDEA_ID}
  selected_topics: {len(summary['selected_topics'])}
  decision_path: {common.rel(cfg.DECISION_PATH)}
  stage_path: stages/{cfg.STAGE_ID}
  report_path: {common.rel(cfg.REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{cfg.PACKET_ID}/aggregate_summary.json
  external_verification_status: {summary['external_verification_status']}
  next_action: {summary['next_action']}
  boundary: {cfg.BOUNDARY}
"""
    text = re.sub(r"stage35_unsupervised_market_state_atlas:\n(?:  .+\n)+\n", "", text)
    text = text.replace("stage34_tier_a_markov_long_permission_attribution:\n", block + "\nstage34_tier_a_markov_long_permission_attribution:\n", 1)
    common.write_md(path, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = common.io_path(common.CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage35 RUN29A.*?(?=## Latest |\Z)", "", old, count=1, flags=re.DOTALL)
    block = f"""## Latest Stage35 RUN29A Unsupervised Market State Atlas(최신 35단계 RUN29A 비지도 시장 상태 지도)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `{summary['active_branch']}`
- active stage(활성 단계): `{cfg.STAGE_ID}`
- current run(현재 실행): `{cfg.RUN_ID}`
- latest packet(최신 묶음): `{cfg.PACKET_ID}`
- next action(다음 행동): `{summary['next_action']}`

Stage35(35단계)를 unsupervised market state atlas(비지도 시장 상태 지도) 주제로 열고 RUN29A(29A 실행)를 기록했다.

결과(result, 결과): `{len(summary['selected_topics'])}`개 non-overlapping topics(비중복 주제)를 골라 Python(파이썬) atlas state(지도 상태)를 만들고 MT5 runtime probe(MT5 런타임 탐침)를 시도했다. external verification(외부 검증)은 `{summary['external_verification_status']}`다.

효과(effect, 효과): Stage34(34단계) 꼬리를 잇지 않고 새 문맥 지도 주제로 이동했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    common.write_md(common.CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog(summary: Mapping[str, Any]) -> None:
    old = common.io_path(common.CHANGELOG_PATH).read_text(encoding="utf-8-sig") if common.io_path(common.CHANGELOG_PATH).exists() else ""
    old = re.sub(r"^## 2026-05-09 Stage35 RUN29A.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-09 Stage35 RUN29A Unsupervised Market State Atlas(35단계 RUN29A 비지도 시장 상태 지도)

- opened(개방): `{cfg.STAGE_ID}`
- run(실행): `{cfg.RUN_ID}`
- topics(주제): `{len(summary['selected_topics'])}` non-overlapping atlas topics(비중복 지도 주제)
- external verification(외부 검증): `{summary['external_verification_status']}`
- judgment(판정): `{summary['judgment']}`
- effect(효과): 새 context map(문맥 지도) 탐색을 MT5 runtime probe(MT5 런타임 탐침)까지 연결했지만, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    common.write_md(common.CHANGELOG_PATH, entry + old.lstrip("\ufeff"))
