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


STAGE_ID = "123_adapter_research__v41_density_scale_followup_review"
RUN_ID = "run123A_stage123_v41_density_scale_followup_review_v1"
PACKET_ID = "stage123_v41_density_scale_followup_review_v1"
PARENT_RUN_ID = "run122A_stage122_v41_density_scale_repair_after_dd_guardrail_v1"
SOURCE_STAGE122_ID = "122_adapter_research__v41_density_scale_repair_after_dd_guardrail"
SOURCE_STAGE122_CLOSEOUT_COMMIT = "d7d1d83862e40bc55f61473209d3a1c38b15d525"
SOURCE_STAGE122_LATEST_COMMIT = "fed35f028fac5621453df67889c4a95cbd8bd77a"
SOURCE_STAGE121_LATEST_COMMIT = "ff03a05b4412a6ed55238940ddd09fc07c3cc1d7"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_route_supply_density_repair_in_stage124_due_to_small_gain"
NEXT_STAGE_ID = "124_adapter_research__v41_route_supply_density_repair_after_small_gain"
NEXT_RUN_ID = "run124A_stage124_v41_route_supply_density_repair_after_small_gain_v1"
NEXT_PACKET_ID = "stage124_v41_route_supply_density_repair_after_small_gain_v1"
EXTERNAL_STATUS = "completed_existing_stage122_mt5_runtime_evidence_reviewed"
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
STAGE120_SOURCE = {
    "adapter_id": "s120_v41_h3_cd7_session_margin_risk035_lng53",
    "profit_factor": 1.735513596,
    "net_profit": 1074.35,
    "max_drawdown_percent": 14.75,
    "trade_count": 177,
}
SOURCE_BY_STAGE122 = {
    "s122_v41_h3_cd6_session_margin_risk035_sht54_lng52": STAGE120_SOURCE["adapter_id"],
    "s122_v41_h3_cd5_session_margin_risk035_sht54_lng52": STAGE120_SOURCE["adapter_id"],
    "s122_v41_h3_cd6_session_margin_risk035_sht53_lng50": STAGE120_SOURCE["adapter_id"],
    "s122_v41_h3_cd5_session_margin_risk035_sht53_lng50": STAGE120_SOURCE["adapter_id"],
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

STAGE122_REVIEWS = Path("stages") / SOURCE_STAGE122_ID / "03_reviews"
STAGE122_REPORT = STAGE122_REVIEWS / "stage122_density_scale_repair_report.md"
STAGE122_DECISION = STAGE122_REVIEWS / "stage122_decision.md"
STAGE122_SUMMARY = STAGE122_REVIEWS / "stage122_density_scale_repair_summary.csv"
STAGE122_SEGMENTS = STAGE122_REVIEWS / "stage122_segment_kpi_summary.csv"
STAGE122_RISK_ATR = STAGE122_REVIEWS / "stage122_risk_atr_telemetry.csv"
STAGE122_GATE_FEATURES = STAGE122_REVIEWS / "stage122_gate_feature_summary.csv"

REPORT_PATH = REVIEWS_ROOT / "stage123_density_scale_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage123_stage120_stage122_34d_comparison.csv"
TRADEOFF_PATH = REVIEWS_ROOT / "stage123_density_scale_tradeoff_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage123_decision.md"
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
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def stage122_rows(split: str) -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(STAGE122_SUMMARY)
        if row.get("split") == split
        and row.get("view") == "actual_routed_total"
        and row.get("status") == "completed"
    ]


def segment_row(adapter_id: str, split: str, segment_type: str, segment: str) -> dict[str, str]:
    for row in read_csv(STAGE122_SEGMENTS):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") != split or row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") == segment_type and row.get("segment") == segment:
            return row
    return {}


def risk_row(adapter_id: str, split: str) -> dict[str, str]:
    for row in read_csv(STAGE122_RISK_ATR):
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def blocked_ratio(adapter_id: str, split: str) -> float:
    for row in read_csv(STAGE122_GATE_FEATURES):
        if row.get("variant_id") == adapter_id and row.get("split") == split:
            return num(row, "blocked_ratio")
    return 0.0


def metric(row: Mapping[str, Any], val_by_adapter: Mapping[str, Mapping[str, str]]) -> dict[str, Any]:
    adapter_id = str(row.get("adapter_id", ""))
    val = val_by_adapter.get(adapter_id, {})
    full = segment_row(adapter_id, "oos", "full_split", "actual_routed_total")
    early = segment_row(adapter_id, "oos", "chronological_third", "early")
    mid = segment_row(adapter_id, "oos", "chronological_third", "mid")
    late = segment_row(adapter_id, "oos", "chronological_third", "late")
    risk = risk_row(adapter_id, "oos")
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    trades = num(row, "trade_count")
    return {
        "run_id": RUN_ID,
        "adapter_id": adapter_id,
        "repair_label": row.get("repair_label", ""),
        "source_adapter_id": SOURCE_BY_STAGE122.get(adapter_id, ""),
        "source_profit_factor": STAGE120_SOURCE["profit_factor"],
        "source_net_profit": STAGE120_SOURCE["net_profit"],
        "source_max_drawdown_percent": STAGE120_SOURCE["max_drawdown_percent"],
        "source_trade_count": STAGE120_SOURCE["trade_count"],
        "validation_profit_factor": num(val, "profit_factor"),
        "validation_net_profit": num(val, "net_profit"),
        "validation_max_drawdown_percent": num(val, "max_drawdown_percent"),
        "validation_trade_count": num(val, "trade_count"),
        "oos_profit_factor": pf,
        "oos_net_profit": net,
        "oos_max_drawdown_percent": dd,
        "oos_trade_count": trades,
        "oos_trades_per_day": num(row, "trades_per_day"),
        "oos_expectancy": num(row, "expectancy"),
        "oos_cost_stressed_expectancy": num(row, "cost_stressed_expectancy"),
        "same_move_reentry_ratio": num(row, "same_move_reentry_ratio"),
        "mfe_capture_ratio": num(full, "mfe_capture_ratio", num(row, "mfe_capture_ratio")),
        "early_net_profit": num(early, "net_profit"),
        "early_profit_factor": num(early, "profit_factor"),
        "early_trade_count": num(early, "trade_count"),
        "mid_net_profit": num(mid, "net_profit"),
        "mid_profit_factor": num(mid, "profit_factor"),
        "mid_trade_count": num(mid, "trade_count"),
        "late_net_profit": num(late, "net_profit"),
        "late_profit_factor": num(late, "profit_factor"),
        "late_trade_count": num(late, "trade_count"),
        "pf_gap_to_34d": pf - LEGACY_34D["profit_factor"],
        "net_gap_to_34d": net - LEGACY_34D["net_profit"],
        "dd_gap_to_34d": dd - LEGACY_34D["max_drawdown_percent"],
        "trade_count_gap_to_34d": trades - LEGACY_34D["trade_count"],
        "density_gain_vs_stage120_source": trades - STAGE120_SOURCE["trade_count"],
        "pf_delta_vs_stage120_source": pf - STAGE120_SOURCE["profit_factor"],
        "net_delta_vs_stage120_source": net - STAGE120_SOURCE["net_profit"],
        "dd_delta_vs_stage120_source": dd - STAGE120_SOURCE["max_drawdown_percent"],
        "risk_floor_applied_count": num(risk, "risk_floor_applied_count"),
        "max_model_risk_pct": num(risk, "max_model_risk_pct"),
        "max_actual_risk_pct_after_floor": num(risk, "max_actual_risk_pct_after_floor"),
        "risk_bucket": risk.get("risk_bucket", ""),
        "oos_gate_blocked_ratio": blocked_ratio(adapter_id, "oos"),
    }


def read_metric(row: Mapping[str, Any]) -> str:
    pf_ok = num(row, "oos_profit_factor") >= LEGACY_34D["profit_factor"]
    net_ok = num(row, "oos_net_profit") >= LEGACY_34D["net_profit"]
    dd_hits_34d = num(row, "oos_max_drawdown_percent") <= LEGACY_34D["max_drawdown_percent"]
    gain = num(row, "density_gain_vs_stage120_source")
    if gain >= 15 and pf_ok and net_ok and dd_hits_34d:
        return "material_density_gain_and_34d_dd_met"
    if gain >= 15 and pf_ok and net_ok:
        return "material_density_gain_but_dd_above_34d"
    if gain > 0 and pf_ok and net_ok:
        return "small_density_gain_preserved_pf_net_but_not_enough"
    return "density_scale_not_useful_or_damaged"


def comparison_columns() -> list[str]:
    return [
        "run_id",
        "adapter_id",
        "repair_label",
        "source_adapter_id",
        "source_profit_factor",
        "source_net_profit",
        "source_max_drawdown_percent",
        "source_trade_count",
        "validation_profit_factor",
        "validation_net_profit",
        "validation_max_drawdown_percent",
        "validation_trade_count",
        "oos_profit_factor",
        "oos_net_profit",
        "oos_max_drawdown_percent",
        "oos_trade_count",
        "oos_trades_per_day",
        "oos_expectancy",
        "oos_cost_stressed_expectancy",
        "same_move_reentry_ratio",
        "mfe_capture_ratio",
        "early_net_profit",
        "early_profit_factor",
        "early_trade_count",
        "mid_net_profit",
        "mid_profit_factor",
        "mid_trade_count",
        "late_net_profit",
        "late_profit_factor",
        "late_trade_count",
        "pf_gap_to_34d",
        "net_gap_to_34d",
        "dd_gap_to_34d",
        "trade_count_gap_to_34d",
        "density_gain_vs_stage120_source",
        "pf_delta_vs_stage120_source",
        "net_delta_vs_stage120_source",
        "dd_delta_vs_stage120_source",
        "risk_floor_applied_count",
        "max_model_risk_pct",
        "max_actual_risk_pct_after_floor",
        "risk_bucket",
        "oos_gate_blocked_ratio",
        "stage123_read",
    ]


def formatted_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    integer_columns = {
        "source_trade_count",
        "validation_trade_count",
        "oos_trade_count",
        "early_trade_count",
        "mid_trade_count",
        "late_trade_count",
        "trade_count_gap_to_34d",
        "density_gain_vs_stage120_source",
        "risk_floor_applied_count",
    }
    money_columns = {
        "source_net_profit",
        "validation_net_profit",
        "oos_net_profit",
        "early_net_profit",
        "mid_net_profit",
        "late_net_profit",
        "net_gap_to_34d",
        "net_delta_vs_stage120_source",
    }
    output = []
    for row in rows:
        out: dict[str, Any] = {}
        for column in comparison_columns():
            value = row.get(column, "")
            if isinstance(value, float):
                if column in integer_columns:
                    out[column] = fmt(value, 0)
                elif column in money_columns:
                    out[column] = fmt(value, 2)
                else:
                    out[column] = fmt(value, 6)
            else:
                out[column] = value
        output.append(out)
    return output


def build_rows() -> list[dict[str, Any]]:
    val_by_adapter = {row.get("adapter_id", ""): row for row in stage122_rows("validation_is")}
    rows = [metric(row, val_by_adapter) for row in stage122_rows("oos")]
    for row in rows:
        row["stage123_read"] = read_metric(row)
    return rows


def best_density(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        rows,
        key=lambda row: (
            num(row, "oos_trade_count"),
            num(row, "oos_profit_factor"),
            num(row, "oos_net_profit"),
            -num(row, "oos_max_drawdown_percent"),
        ),
        default={},
    )


def tradeoff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        read = str(row.get("stage123_read", ""))
        if read == "small_density_gain_preserved_pf_net_but_not_enough":
            next_probe = "move_to_route_supply_or_lifecycle_source_not_more_threshold_only"
        elif read == "material_density_gain_but_dd_above_34d":
            next_probe = "repair_dd_before_accepting_density_gain"
        elif read == "material_density_gain_and_34d_dd_met":
            next_probe = "open_full_equity_segment_review"
        else:
            next_probe = "preserve_as_failure_memory"
        output.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "source_adapter_id": row.get("source_adapter_id", ""),
                "oos_profit_factor": fmt(num(row, "oos_profit_factor")),
                "oos_net_profit": fmt(num(row, "oos_net_profit"), 2),
                "oos_max_drawdown_percent": fmt(num(row, "oos_max_drawdown_percent")),
                "oos_trade_count": fmt(num(row, "oos_trade_count"), 0),
                "density_gain_vs_stage120_source": fmt(num(row, "density_gain_vs_stage120_source"), 0),
                "trade_count_gap_to_34d": fmt(num(row, "trade_count_gap_to_34d"), 0),
                "dd_gap_to_34d": fmt(num(row, "dd_gap_to_34d")),
                "read": read,
                "next_probe": next_probe,
            }
        )
    return output


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | gain(증가) | 34D gap(34D 차이) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter} | {pf} | {net} | {dd} | {trades} | {gain} | {gap} | {read} |".format(
                adapter=row.get("adapter_id", ""),
                pf=row.get("oos_profit_factor", ""),
                net=row.get("oos_net_profit", ""),
                dd=row.get("oos_max_drawdown_percent", ""),
                trades=row.get("oos_trade_count", ""),
                gain=row.get("density_gain_vs_stage120_source", ""),
                gap=row.get("trade_count_gap_to_34d", ""),
                read=row.get("stage123_read", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]]) -> str:
    best = best_density(rows)
    tradeoff_text = "\n".join(
        f"- `{row.get('adapter_id')}`: {row.get('read')} -> {row.get('next_probe')}" for row in tradeoffs
    )
    return f"""# Stage123 Density Scale Follow-up Review(123단계 밀도 규모 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE122_ID}`
- source_stage122_closeout_commit(원천 122단계 종료 커밋): `{SOURCE_STAGE122_CLOSEOUT_COMMIT}`
- source_stage122_latest_commit(원천 122단계 최신 커밋): `{SOURCE_STAGE122_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage122(122단계)의 거래 수 증가가 PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 원격측정)를 보존했는가?

Effect(효과): Stage123(123단계)은 새 실험을 추가하지 않고 Stage122 evidence(근거)를 판독해 다음 수리 방향을 정한다.

## Result Table(결과 표)

{markdown_table(rows)}

## Best Read(최선 판독)

- best_density(최선 밀도): `{best.get('adapter_id', '')}` PF `{best.get('oos_profit_factor', '')}`, net `{best.get('oos_net_profit', '')}`, DD `{best.get('oos_max_drawdown_percent', '')}`, trades `{best.get('oos_trade_count', '')}`
- plain_read(쉬운 판독): Stage122는 Stage120 원천 대비 거래 수를 2건 늘렸다. PF/net(수익 팩터/순손익)은 보존됐지만, 34D의 404거래에는 아직 225건 부족하고 DD%(손실률)는 34D보다 약 1.75%p 높다.

## Tradeoff Notes(트레이드오프 메모)

{tradeoff_text}

## Judgment(판정)

- result_subject(판정 대상): Stage122 density scale repair evidence(122단계 밀도 규모 수리 근거).
- evidence_available(있는 근거): Stage122 MT5 runtime summaries(MT5 실행환경 요약), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 원격측정), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): 34D 수준 trade density(거래 밀도), 34D 수준 DD%(손실률), full equity-shape audit(전체 자본 곡선 형태 감사).
- judgment_label(판정 라벨): `small_density_gain_not_sufficient`.
- claim_boundary(주장 경계): `{BOUNDARY}`.
- next_condition(다음 조건): Stage124(124단계)는 단순 threshold/cooldown(임계값/대기시간) 완화가 아니라 route supply/lifecycle source(경로 공급/생애주기 원천)를 수리해야 한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown() -> str:
    return f"""# Stage123 Decision(123단계 판정)

decision(판정): `{DECISION}`

Stage123(123단계)은 Stage122(122단계)의 density scale repair(밀도 규모 수리)를 후속 검토했다.

Effect(효과): 거래 수는 177에서 179로 늘었지만 34D의 404거래와는 아직 차이가 크므로, 다음 수리는 threshold/cooldown(임계값/대기시간)만 더 푸는 방식이 아니라 route supply/lifecycle source(경로 공급/생애주기 원천)로 넘어간다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`
- source_stage122_report(원천 122단계 보고서): `{rel(STAGE122_REPORT)}`
- source_stage122_decision(원천 122단계 판정): `{rel(STAGE122_DECISION)}`
- source_stage122_closeout_commit(원천 122단계 종료 커밋): `{SOURCE_STAGE122_CLOSEOUT_COMMIT}`
- source_stage122_latest_commit(원천 122단계 최신 커밋): `{SOURCE_STAGE122_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage123(123단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research(브이투 고유 연구)는 Stage124(124단계) 경로 공급 밀도 수리로 이어진다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows = []
    for path in [REPORT_PATH, COMPARISON_PATH, TRADEOFF_PATH, DECISION_PATH, STAGE_LEDGER_PATH]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage123_density_scale_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage123 v2-native density scale follow-up review artifact.",
                }
            )
    return rows


def write_ledgers(rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = best_density(rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_density_scale_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage122_closeout_commit", SOURCE_STAGE122_CLOSEOUT_COMMIT),
                        ("source_stage122_latest_commit", SOURCE_STAGE122_LATEST_COMMIT),
                        ("best_density", best.get("adapter_id")),
                        ("density_gain", best.get("density_gain_vs_stage120_source")),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage123_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage123_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage122_mt5_runtime_evidence_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage123_density_scale_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_density", best.get("adapter_id")),
                    ("pf", best.get("oos_profit_factor")),
                    ("net", best.get("oos_net_profit")),
                    ("dd", best.get("oos_max_drawdown_percent")),
                    ("trades", best.get("oos_trade_count")),
                    ("density_gain", best.get("density_gain_vs_stage120_source")),
                )
            ),
            "guardrail_kpi": f"target_surface={TARGET_SURFACE};decision={DECISION};overall_goal_complete=false",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage123 review only; no new MT5 execution; no operational claim.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    best = best_density(rows)
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": ["kpi_contract_audit", "result_judgment_gate", "artifact_lineage_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "source_stage122_summary": rel(STAGE122_SUMMARY),
            "source_stage122_segments": rel(STAGE122_SEGMENTS),
            "source_stage122_risk_atr": rel(STAGE122_RISK_ATR),
            "comparison_path": rel(COMPARISON_PATH),
            "tradeoff_path": rel(TRADEOFF_PATH),
            "status": "passed_review_only",
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "judgment_label": "small_density_gain_not_sufficient",
            "best_density_candidate": best,
            "overall_goal_complete": False,
            "forbidden_claims": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "operating_reference", "runtime_authority", "legacy_inheritance"],
        },
    )
    write_json(
        PACKET_ROOT / "artifact_lineage_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "source_inputs": [rel(STAGE122_SUMMARY), rel(STAGE122_SEGMENTS), rel(STAGE122_RISK_ATR), rel(STAGE122_GATE_FEATURES)],
            "producer": rel(Path("stage_pipelines/stage123/v41_density_scale_followup_review.py")),
            "artifact_paths": [rel(REPORT_PATH), rel(COMPARISON_PATH), rel(TRADEOFF_PATH), rel(DECISION_PATH), rel(STAGE_LEDGER_PATH)],
            "availability": "tracked_after_stage_boundary_commit",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage122_closeout_commit": SOURCE_STAGE122_CLOSEOUT_COMMIT,
            "source_stage122_latest_commit": SOURCE_STAGE122_LATEST_COMMIT,
            "best_density_candidate": best.get("adapter_id"),
            "density_gain": best.get("density_gain_vs_stage120_source"),
            "trade_count_gap_to_34d": best.get("trade_count_gap_to_34d"),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage124(124단계)는 Stage123(123단계)의 판정대로, threshold/cooldown(임계값/대기시간)만 더 푸는 방식이 아니라 route supply/lifecycle source(경로 공급/생애주기 원천)를 수리한다.

## Bounded Question(경계 질문)

현재 risk035 ATR bracket(위험 3.5% ATR 괄호)을 유지하면서, 새로운 route supply/lifecycle source(경로 공급/생애주기 원천)가 trade count(거래 수)를 의미 있게 늘리고 PF/net/DD(수익 팩터/순손익/손실률)를 보존할 수 있는가?

Effect(효과): Stage124(124단계)는 34D trade density(34D 거래 밀도) 격차를 줄이기 위해 더 큰 공급원만 좁게 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage124 Input References(124단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage123_report(123단계 보고서): `{rel(REPORT_PATH)}`
- stage123_tradeoff(123단계 트레이드오프): `{rel(TRADEOFF_PATH)}`
- stage122_summary(122단계 요약): `{rel(STAGE122_SUMMARY)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage124 Review Index(124단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage124 Selection Status(124단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage123(123단계) closed(종료) as `{DECISION}` and Stage124(124단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): threshold/cooldown(임계값/대기시간)만으로는 밀도 증가가 작아 route supply/lifecycle source(경로 공급/생애주기 원천) 수리로 넘긴다.
- >-
  Stage123 result(123단계 결과)는 `{rel(REPORT_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 기록했다. Effect(효과): Stage122의 +2 trades(거래 2건 증가)는 충분하지 않다는 판정을 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage123_v41_density_scale_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage122_closeout_commit: {SOURCE_STAGE122_CLOSEOUT_COMMIT}
  source_stage122_latest_commit: {SOURCE_STAGE122_LATEST_COMMIT}
  source_stage121_latest_commit: {SOURCE_STAGE121_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage123_v41_density_scale_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage123_v41_density_scale_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")

    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage123 Selection Status(123단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE122_ID}`
- source_decision(원천 판정): `continue_density_scale_followup_review_in_stage123_with_small_gain`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage123_decision(123단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage123 Review Index(123단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
""",
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage124_route_supply_density_repair_surface`
- status(상태): `stage123_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage123(123단계) closed(종료) as v2-native v41 density scale follow-up review(브이투 고유 브이41 밀도 규모 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage124(124단계) route supply density repair(경로 공급 밀도 수리)로 이어진다.

## Latest Stage123 Evidence(최신 123단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(트레이드오프 요약): `{rel(TRADEOFF_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage123 v41 density scale follow-up review closeout(123단계 v41 밀도 규모 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage122(122단계)의 +2 trade(거래 2건 증가)는 충분하지 않다고 판정하고 Stage124(124단계) route supply density repair(경로 공급 밀도 수리)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main(argv: Sequence[str] | None = None) -> int:
    del argv
    rows = build_rows()
    formatted = formatted_rows(rows)
    tradeoffs = tradeoff_rows(rows)
    write_csv(COMPARISON_PATH, formatted, comparison_columns())
    write_csv(
        TRADEOFF_PATH,
        tradeoffs,
        [
            "run_id",
            "adapter_id",
            "source_adapter_id",
            "oos_profit_factor",
            "oos_net_profit",
            "oos_max_drawdown_percent",
            "oos_trade_count",
            "density_gain_vs_stage120_source",
            "trade_count_gap_to_34d",
            "dd_gap_to_34d",
            "read",
            "next_probe",
        ],
    )
    write_md(REPORT_PATH, report_markdown(formatted, tradeoffs))
    write_md(DECISION_PATH, decision_markdown())
    write_csv(STAGE_LEDGER_PATH, [], ALPHA_LEDGER_COLUMNS)
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(rows, artifacts)
    write_packet_files(rows, ledger_payload)
    write_md(REPORT_PATH, report_markdown(formatted, tradeoffs))
    write_md(DECISION_PATH, decision_markdown())
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(rows, artifacts)
    write_packet_files(rows, ledger_payload)
    update_current_truth()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "report": rel(REPORT_PATH),
                    "comparison": rel(COMPARISON_PATH),
                    "tradeoff": rel(TRADEOFF_PATH),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
