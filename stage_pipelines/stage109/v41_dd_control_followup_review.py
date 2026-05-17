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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


STAGE_ID = "109_adapter_research__v41_dd_control_followup_review"
RUN_ID = "run109A_stage109_v41_dd_control_followup_review_v1"
PACKET_ID = "stage109_v41_dd_control_followup_review_v1"
PARENT_RUN_ID = "run108A_stage108_v41_dd_control_after_net_early_recovery_repair_v1"
SOURCE_STAGE108_ID = "108_adapter_research__v41_dd_control_after_net_early_recovery_repair"
SOURCE_STAGE108_CLOSEOUT_COMMIT = "d5f13807d196abd557faceb007b666950c1bb197"
SOURCE_STAGE108_LATEST_COMMIT = "e94b562ad2c8a3a7fbcf5ca198f7f5799fae3219"
SOURCE_STAGE107_LATEST_COMMIT = "728d4cba5b3361ba5eaf49561ea8b2d2282b6343"
SOURCE_STAGE106_LATEST_COMMIT = "0e34739b13eaf7d8c7d9bfb48bf168396122d17a"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_trade_density_net_scale_after_dd_tradeoff_repair_in_stage110"
NEXT_STAGE_ID = "110_adapter_research__v41_trade_density_net_scale_after_dd_tradeoff_repair"
NEXT_RUN_ID = "run110A_stage110_v41_trade_density_net_scale_after_dd_tradeoff_repair_v1"
NEXT_PACKET_ID = "stage110_v41_trade_density_net_scale_after_dd_tradeoff_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage108_mt5_runtime_evidence_reviewed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

REFERENCE_ROWS = (
    {
        "source_stage": "stage106_net_pf_best",
        "source_run_id": "run106A_stage106_v41_oos_net_density_dd_after_early_recovery_repair_v1",
        "adapter_id": "s106_v41_h3_cd9_lng_early_adx19",
        "profit_factor": 1.637076853,
        "net_profit": 644.76,
        "max_drawdown_percent": 18.69,
        "trade_count": 147,
        "expectancy": 4.386122449,
        "early_net_profit": 38.84,
        "early_profit_factor": 1.157011764,
        "early_mfe_capture_ratio": 0.0727640601,
    },
    {
        "source_stage": "stage106_dd_best",
        "source_run_id": "run106A_stage106_v41_oos_net_density_dd_after_early_recovery_repair_v1",
        "adapter_id": "s106_v41_h4_cd8_lng_early_adx19",
        "profit_factor": 1.551824268,
        "net_profit": 615.72,
        "max_drawdown_percent": 16.06,
        "trade_count": 147,
        "expectancy": 4.188571429,
        "early_net_profit": 57.13,
        "early_profit_factor": 1.198058589,
        "early_mfe_capture_ratio": 0.09606341766,
    },
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE108_REVIEWS = Path("stages") / SOURCE_STAGE108_ID / "03_reviews"
SOURCE_STAGE108_SUMMARY = SOURCE_STAGE108_REVIEWS / "stage108_dd_control_after_net_early_recovery_summary.csv"
SOURCE_STAGE108_SEGMENTS = SOURCE_STAGE108_REVIEWS / "stage108_segment_kpi_summary.csv"
SOURCE_STAGE108_REPORT = SOURCE_STAGE108_REVIEWS / "stage108_dd_control_after_net_early_recovery_report.md"
SOURCE_STAGE108_DECISION = SOURCE_STAGE108_REVIEWS / "stage108_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage109_dd_control_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage109_stage106_stage108_34d_comparison.csv"
TRADEOFF_PATH = REVIEWS_ROOT / "stage109_dd_net_tradeoff_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage109_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def num(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        return default
    try:
        return float(str(value))
    except ValueError:
        return default


def fmt(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def summary_lookup() -> dict[str, dict[str, str]]:
    return {
        row.get("adapter_id", ""): row
        for row in read_csv(SOURCE_STAGE108_SUMMARY)
        if row.get("split") == "oos" and row.get("view") == "actual_routed_total" and row.get("status") == "completed"
    }


def segment_row(adapter_id: str, segment_type: str, segment: str) -> dict[str, str]:
    for row in read_csv(SOURCE_STAGE108_SEGMENTS):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") != "oos" or row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") == segment_type and row.get("segment") == segment:
            return row
    return {}


def stage108_metric_rows() -> list[dict[str, Any]]:
    lookup = summary_lookup()
    rows: list[dict[str, Any]] = []
    for adapter_id, summary in lookup.items():
        full = segment_row(adapter_id, "full_split", "actual_routed_total")
        early = segment_row(adapter_id, "chronological_third", "early")
        rows.append(
            {
                "source_stage": "stage108_candidate",
                "source_run_id": PARENT_RUN_ID,
                "adapter_id": adapter_id,
                "profit_factor": num(full, "profit_factor", num(summary, "profit_factor")),
                "net_profit": num(full, "net_profit", num(summary, "net_profit")),
                "max_drawdown_percent": num(summary, "max_drawdown_percent"),
                "trade_count": num(summary, "trade_count"),
                "expectancy": num(full, "expectancy", num(summary, "expectancy")),
                "early_net_profit": num(early, "net_profit"),
                "early_profit_factor": num(early, "profit_factor"),
                "early_mfe_capture_ratio": num(early, "mfe_capture_ratio"),
            }
        )
    return rows


def row_read(row: Mapping[str, Any]) -> str:
    adapter = str(row.get("adapter_id", ""))
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    early_pf = num(row, "early_profit_factor")
    if adapter == "s108_v41_h4_cd9_lng_early_adx19":
        return "dd_preserved_near_stage106_dd_best_but_pf_below_34d_and_net_low"
    if adapter == "s108_v41_h4_cd10_lng_early_adx19":
        return "dd_slightly_better_but_net_and_early_pf_damaged"
    if adapter == "s108_v41_h3_cd10_lng_early_adx19":
        return "net_pf_preserved_but_dd_unchanged"
    if pf >= 1.63 and net >= 640 and dd >= 18.0:
        return "net_pf_reference_but_dd_gap_remains"
    if dd <= 16.1 and early_pf >= 1.19:
        return "dd_reference_but_pf_net_gap_remains"
    return "reference_or_measurement"


def comparison_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in list(REFERENCE_ROWS) + stage108_metric_rows():
        pf = num(source, "profit_factor")
        net = num(source, "net_profit")
        dd = num(source, "max_drawdown_percent")
        trades = num(source, "trade_count")
        early_net = num(source, "early_net_profit")
        early_pf = num(source, "early_profit_factor")
        early_mfe = num(source, "early_mfe_capture_ratio")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_stage": source.get("source_stage", ""),
                "source_run_id": source.get("source_run_id", ""),
                "adapter_id": source.get("adapter_id", ""),
                "split": "oos",
                "profit_factor": fmt(pf),
                "net_profit": fmt(net, 2),
                "max_drawdown_percent": fmt(dd),
                "trade_count": fmt(trades, 0),
                "expectancy": fmt(num(source, "expectancy")),
                "early_net_profit": fmt(early_net, 2),
                "early_profit_factor": fmt(early_pf),
                "early_mfe_capture_ratio": fmt(early_mfe),
                "pf_gap_to_34d_latest": fmt(pf - LEGACY_34D["profit_factor"]),
                "net_gap_to_34d_latest": fmt(net - LEGACY_34D["net_profit"], 2),
                "dd_gap_to_34d_latest": fmt(dd - LEGACY_34D["max_drawdown_percent"]),
                "trade_count_gap_to_34d_latest": fmt(trades - LEGACY_34D["trade_count"], 0),
                "net_gap_to_stage106_net_pf_best": fmt(net - REFERENCE_ROWS[0]["net_profit"], 2),
                "dd_gap_to_stage106_dd_best": fmt(dd - REFERENCE_ROWS[1]["max_drawdown_percent"]),
                "stage109_read": row_read(source),
            }
        )
    return rows


def tradeoff_rows() -> list[dict[str, Any]]:
    rows = []
    for row in comparison_rows():
        pf = num(row, "profit_factor")
        net = num(row, "net_profit")
        dd = num(row, "max_drawdown_percent")
        early_pf = num(row, "early_profit_factor")
        trades = num(row, "trade_count")
        rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row["adapter_id"],
                "source_stage": row["source_stage"],
                "net_profit": row["net_profit"],
                "profit_factor": row["profit_factor"],
                "max_drawdown_percent": row["max_drawdown_percent"],
                "trade_count": row["trade_count"],
                "early_profit_factor": row["early_profit_factor"],
                "tradeoff_read": tradeoff_read(pf, net, dd, early_pf, trades),
            }
        )
    return rows


def tradeoff_read(pf: float, net: float, dd: float, early_pf: float, trades: float) -> str:
    if dd <= 16.1 and pf < LEGACY_34D["profit_factor"]:
        return "dd_improves_but_pf_fails"
    if dd <= 16.1 and net < REFERENCE_ROWS[0]["net_profit"]:
        return "dd_improves_but_net_scale_fails"
    if pf >= REFERENCE_ROWS[0]["profit_factor"] and net >= REFERENCE_ROWS[0]["net_profit"] and dd > 18.0:
        return "net_pf_ok_but_dd_fails"
    if early_pf < REFERENCE_ROWS[0]["early_profit_factor"]:
        return "early_floor_damaged"
    if trades < 200:
        return "trade_density_gap_remains"
    return "mixed"


def best_net_candidate(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: (num(row, "profit_factor"), num(row, "net_profit"), -num(row, "max_drawdown_percent")))


def best_dd_candidate(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return min(rows, key=lambda row: (num(row, "max_drawdown_percent", 99.0), -num(row, "profit_factor"), -num(row, "net_profit")))


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | early PF(초반 수익 팩터) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['source_stage']} | {row['adapter_id']} | {row['profit_factor']} | {row['net_profit']} | {row['max_drawdown_percent']} | {row['trade_count']} | {row['early_profit_factor']} | {row['stage109_read']} |"
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]], net_best: Mapping[str, Any], dd_best: Mapping[str, Any]) -> str:
    return f"""# Stage109 DD Control Follow-up Review(109단계 손실률 제어 후속 검토)

- run(실행): `{RUN_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- source_stage108_closeout_commit(원천 108단계 종료 커밋): `{SOURCE_STAGE108_CLOSEOUT_COMMIT}`
- source_stage108_latest_commit(원천 108단계 최신 커밋): `{SOURCE_STAGE108_LATEST_COMMIT}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage108(108단계)의 DD control repair(손실률 제어 수리)가 Stage106 net/PF best(106단계 순손익/수익 팩터 최선), Stage106 DD best(106단계 손실률 최선), 34D target surface(34D 목표 표면) 대비 어떤 균형을 만들었는가?

Effect(효과): Stage109(109단계)는 새 실행이 아니라 실제 MT5 runtime(실행환경) 근거를 판독하고, 다음 수리 범위를 줄인다.

## KPI Comparison(KPI 비교)

{kpi_table(rows)}

## Attribution(성과 귀속)

- observed_change(관찰 변화): Stage108(108단계)은 `hold4(보유4)`로 DD(손실률)를 `16.02~16.06`까지 낮출 수 있음을 재확인했지만, PF/net/early(수익 팩터/순손익/초반)를 동시에 만족하지 못했다.
- comparison_baseline(비교 기준): Stage106 net/PF best(106단계 순손익/수익 팩터 최선), Stage106 DD best(106단계 손실률 최선), 34D target(34D 목표).
- likely_drivers(가능 원인): hold/cooldown(보유/쿨다운) 계열은 거래 수를 `144~147` 부근에 묶어 trade density(거래 밀도)와 net scale(순손익 규모)을 키우지 못했다.
- segment_checks(구간 점검): full OOS(전체 표본외), early(초반), DD(손실률), trade count(거래 수), risk/ATR telemetry(위험/ATR 텔레메트리)를 확인했다.
- trade_shape(거래 형태): 34D target(34D 목표) 거래 수 `404` 대비 현재 최선은 `147`로 크게 낮다.
- alternative_explanations(대안 설명): 같은 거래 집합이 재현된 후보가 있어 cooldown(쿨다운) 변화가 실제 진입 기회를 늘리지 못했을 가능성이 높다.
- attribution_confidence(귀속 신뢰도): `medium`.
- next_probe(다음 탐침): Stage110(110단계)은 lifecycle-only(생명주기 전용) 수리를 멈추고 trade density/net scale(거래 밀도/순손익 규모)을 좁게 늘리는 진입 커버리지 수리를 맡는다.

## Best Reads(최선 판독)

- net_pf_best(순손익/수익 팩터 최선): `{net_best.get("adapter_id")}` with PF(수익 팩터) `{net_best.get("profit_factor")}`, net(순손익) `{net_best.get("net_profit")}`, DD(손실률) `{net_best.get("max_drawdown_percent")}`.
- dd_best(손실률 최선): `{dd_best.get("adapter_id")}` with PF(수익 팩터) `{dd_best.get("profit_factor")}`, net(순손익) `{dd_best.get("net_profit")}`, DD(손실률) `{dd_best.get("max_drawdown_percent")}`.

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage108 DD control repair(108단계 손실률 제어 수리).
- evidence_available(있는 근거): Stage108 MT5 runtime reports(실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).
- evidence_missing(빠진 근거): 34D KPI(34D 핵심 성과 지표) 수준의 net/DD/trade density(순손익/손실률/거래 밀도) 동시 충족.
- judgment_label(판정 라벨): `exploratory_repair_continues`.
- claim_boundary(주장 경계): `{BOUNDARY}`.
- next_condition(다음 조건): `{DECISION}`.

## Decision(판정)

decision(판정): `{DECISION}`

Stage109(109단계)는 전체 목표 완료가 아니다. Effect(효과): Stage110(110단계)은 거래 밀도와 순손익 규모를 늘리는 좁은 수리로 이어진다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(net_best: Mapping[str, Any], dd_best: Mapping[str, Any]) -> str:
    return f"""# Stage109 Decision(109단계 판정)

decision(판정): `{DECISION}`

Stage109(109단계)는 Stage108(108단계)의 actual MT5 runtime result(실제 MT5 실행환경 결과)를 후속 검토했다.

Effect(효과): Stage108(108단계)은 DD(손실률)를 낮추는 길과 net/PF(순손익/수익 팩터)를 지키는 길이 갈라진다는 점을 확인했지만, 34D KPI(34D 핵심 성과 지표) 수준의 동시 충족은 만들지 못했다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- source_stage108_summary(원천 108단계 요약): `{rel(SOURCE_STAGE108_SUMMARY)}`
- source_stage108_segment_kpi(원천 108단계 구간 KPI): `{rel(SOURCE_STAGE108_SEGMENTS)}`
- net_pf_best(순손익/수익 팩터 최선): `{net_best.get("adapter_id")}`
- dd_best(손실률 최선): `{dd_best.get("adapter_id")}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def write_ledgers(net_best: Mapping[str, Any], dd_best: Mapping[str, Any]) -> Mapping[str, Any]:
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__stage109_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage109_followup_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_gate",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage108_dd_control_followup_review",
        "scoreboard_lane": "runtime_probe",
        "status": "reviewed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": f"net_best={net_best.get('adapter_id')};dd_best={dd_best.get('adapter_id')}",
        "guardrail_kpi": f"target_surface={TARGET_SURFACE};overall_goal_complete=false",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage109 review-only gate. No new MT5 runtime; Stage108 runtime evidence reviewed.",
    }
    project = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [ledger_row], key="ledger_row_id")
    stage = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [ledger_row], key="ledger_row_id")
    registry = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_dd_control_followup_review",
                "status": "reviewed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_run", PARENT_RUN_ID),
                        ("source_stage108_latest_commit", SOURCE_STAGE108_LATEST_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                        ("new_runtime", "no_review_gate_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    return {"stage_ledger": stage, "project_ledger": project, "run_registry": registry}


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        (REPORT_PATH, "stage109_v41_dd_control_followup_review_evidence", "Stage109 bounded review report."),
        (COMPARISON_PATH, "stage109_v41_dd_control_followup_review_evidence", "Stage109 Stage106/108/34D comparison."),
        (TRADEOFF_PATH, "stage109_v41_dd_control_followup_review_evidence", "Stage109 DD/net tradeoff summary."),
        (DECISION_PATH, "stage109_v41_dd_control_followup_review_evidence", "Stage109 decision."),
        (STAGE_LEDGER_PATH, "stage109_v41_dd_control_followup_review_evidence", "Stage109 local ledger."),
        (PACKET_ROOT / "aggregate_summary.json", "packet_summary", "Stage109 packet aggregate summary."),
        (PACKET_ROOT / "routing_receipt.json", "packet_control", "Stage109 routing receipt."),
        (PACKET_ROOT / "runtime_evidence_gate.json", "packet_control", "Stage109 runtime evidence gate."),
        (PACKET_ROOT / "result_judgment_gate.json", "packet_control", "Stage109 result judgment gate."),
    ]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": notes,
        }
        for path, artifact_type, notes in paths
    ]


def write_packet_files(net_best: Mapping[str, Any], dd_best: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation"],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "external_verification_status": EXTERNAL_STATUS,
            "source_runtime_summary": rel(SOURCE_STAGE108_SUMMARY),
            "source_segment_summary": rel(SOURCE_STAGE108_SEGMENTS),
            "claim_boundary": BOUNDARY,
            "new_runtime": False,
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "result_subject": "Stage108 DD control repair",
            "evidence_available": [rel(SOURCE_STAGE108_SUMMARY), rel(SOURCE_STAGE108_SEGMENTS), rel(SOURCE_STAGE108_REPORT)],
            "evidence_missing": "34D-level net/DD/trade density simultaneously",
            "judgment_label": "exploratory_repair_continues",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
            "overall_goal_complete": False,
            "forbidden_claims": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "operating_reference", "runtime_authority", "legacy_inheritance"],
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "net_pf_best": net_best,
            "dd_best": dd_best,
            "source_stage108_closeout_commit": SOURCE_STAGE108_CLOSEOUT_COMMIT,
            "source_stage108_latest_commit": SOURCE_STAGE108_LATEST_COMMIT,
            "comparison_path": rel(COMPARISON_PATH),
            "tradeoff_path": rel(TRADEOFF_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def update_artifact_registry() -> Mapping[str, Any]:
    return upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows(),
        key="artifact_id",
    )


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage110(110단계)는 Stage109(109단계)의 판정대로 trade density/net scale(거래 밀도/순손익 규모)을 좁게 수리한다.

## Bounded Question(경계 질문)

Stage106/108(106/108단계)에서 확인된 net/PF(순손익/수익 팩터) 보존과 DD(손실률) 저감 단서를 해치지 않고, 낮은 trade density(거래 밀도)와 net scale(순손익 규모)을 개선할 수 있는가?

Effect(효과): Stage110(110단계)은 hold/cooldown-only(보유/쿨다운 전용) 반복을 멈추고, entry coverage(진입 커버리지), session/regime(세션/국면), side-specific logic(방향별 로직)을 좁게 본다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage110 Input References(110단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_comparison(원천 비교): `{rel(COMPARISON_PATH)}`
- source_tradeoff(원천 상충): `{rel(TRADEOFF_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage110(110단계)은 34D KPI(34D 핵심 성과 지표) 대비 가장 큰 격차인 거래 수와 순손익 규모를 다음 수리 입력으로 받는다.
""")
    write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage110 Review Index(110단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage110(110단계)은 Stage109(109단계) closeout(종료 기록)을 이어받아 좁은 수리만 수행한다.
""")
    write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage110 Selection Status(110단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage110(110단계)은 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""")


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage109(109단계) closed(종료) as `{DECISION}` and Stage110(110단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): hold/cooldown(보유/쿨다운)만으로는 34D KPI(34D 핵심 성과 지표) 격차가 닫히지 않아 trade density/net scale(거래 밀도/순손익 규모) 수리로 넘긴다.
- >-
  Stage109 result(109단계 결과)는 `{rel(COMPARISON_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 기록된다. Effect(효과): DD(손실률) 개선 후보와 net/PF(순손익/수익 팩터) 보존 후보가 갈라진 원인을 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage109_v41_dd_control_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage108_closeout_commit: {SOURCE_STAGE108_CLOSEOUT_COMMIT}
  source_stage108_latest_commit: {SOURCE_STAGE108_LATEST_COMMIT}
  source_stage107_latest_commit: {SOURCE_STAGE107_LATEST_COMMIT}
  source_stage106_latest_commit: {SOURCE_STAGE106_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage109_v41_dd_control_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage109_v41_dd_control_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage109 Selection Status(109단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE108_ID}`
- source_decision(원천 판정): `continue_dd_control_repair_review_in_stage109`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage109_decision(109단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage109(109단계)는 Stage108(108단계) 실제 실행 결과를 판독하고, 운영 의미 없이 Stage110(110단계)로 넘긴다.
""")
    write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage109_trade_density_net_scale_repair_surface`
- status(상태): `stage109_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage109(109단계) closed(종료) as v2-native v41 DD control follow-up review(브이투 고유 브이41 손실률 제어 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage110(110단계)로 이어진다.

## Latest Stage109 Evidence(최신 109단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage109 v41 DD control follow-up review closeout(109단계 v41 손실률 제어 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage108(108단계)은 손실률 개선과 순손익/수익 팩터 보존이 갈라졌고, 거래 밀도와 순손익 규모 격차가 남아 Stage110(110단계)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = comparison_rows()
    tradeoffs = tradeoff_rows()
    net_best = best_net_candidate(rows)
    dd_best = best_dd_candidate(rows)
    write_csv(
        COMPARISON_PATH,
        rows,
        (
            "run_id",
            "source_stage",
            "source_run_id",
            "adapter_id",
            "split",
            "profit_factor",
            "net_profit",
            "max_drawdown_percent",
            "trade_count",
            "expectancy",
            "early_net_profit",
            "early_profit_factor",
            "early_mfe_capture_ratio",
            "pf_gap_to_34d_latest",
            "net_gap_to_34d_latest",
            "dd_gap_to_34d_latest",
            "trade_count_gap_to_34d_latest",
            "net_gap_to_stage106_net_pf_best",
            "dd_gap_to_stage106_dd_best",
            "stage109_read",
        ),
    )
    write_csv(
        TRADEOFF_PATH,
        tradeoffs,
        (
            "run_id",
            "adapter_id",
            "source_stage",
            "net_profit",
            "profit_factor",
            "max_drawdown_percent",
            "trade_count",
            "early_profit_factor",
            "tradeoff_read",
        ),
    )
    write_md(REPORT_PATH, report_markdown(rows, tradeoffs, net_best, dd_best))
    write_md(DECISION_PATH, decision_markdown(net_best, dd_best))
    ledger_payload = write_ledgers(net_best, dd_best)
    write_packet_files(net_best, dd_best, ledger_payload)
    update_artifact_registry()
    update_current_truth()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "external_verification_status": EXTERNAL_STATUS,
                    "report": rel(REPORT_PATH),
                    "decision_path": rel(DECISION_PATH),
                    "next_stage": NEXT_STAGE_ID,
                    "net_pf_best": net_best.get("adapter_id"),
                    "dd_best": dd_best.get("adapter_id"),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
