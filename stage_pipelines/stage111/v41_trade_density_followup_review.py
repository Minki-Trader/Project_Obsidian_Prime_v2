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


STAGE_ID = "111_adapter_research__v41_trade_density_followup_review"
RUN_ID = "run111A_stage111_v41_trade_density_followup_review_v1"
PACKET_ID = "stage111_v41_trade_density_followup_review_v1"
PARENT_RUN_ID = "run110A_stage110_v41_trade_density_net_scale_after_dd_tradeoff_repair_v1"
SOURCE_STAGE110_ID = "110_adapter_research__v41_trade_density_net_scale_after_dd_tradeoff_repair"
SOURCE_STAGE110_CLOSEOUT_COMMIT = "acbdc3236a7b26696eba3a6a9b87c808789e8a24"
SOURCE_STAGE110_LATEST_COMMIT = "c702502f01e2ef0e9a17d2ac9ec86b6108a82d04"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_route_supply_density_repair_in_stage112"
NEXT_STAGE_ID = "112_adapter_research__v41_route_supply_density_repair"
NEXT_RUN_ID = "run112A_stage112_v41_route_supply_density_repair_v1"
NEXT_PACKET_ID = "stage112_v41_route_supply_density_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage110_mt5_runtime_evidence_reviewed"
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

REFERENCE_STAGE106_NET_PF = {
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
}

REFERENCE_STAGE106_DD = {
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
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE110_REVIEWS = Path("stages") / SOURCE_STAGE110_ID / "03_reviews"
SOURCE_STAGE110_SUMMARY = SOURCE_STAGE110_REVIEWS / "stage110_trade_density_net_scale_summary.csv"
SOURCE_STAGE110_SEGMENTS = SOURCE_STAGE110_REVIEWS / "stage110_segment_kpi_summary.csv"
SOURCE_STAGE110_REPORT = SOURCE_STAGE110_REVIEWS / "stage110_trade_density_net_scale_report.md"
SOURCE_STAGE110_DECISION = SOURCE_STAGE110_REVIEWS / "stage110_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage111_trade_density_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage111_stage106_stage110_34d_comparison.csv"
TRADEOFF_PATH = REVIEWS_ROOT / "stage111_trade_density_tradeoff_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage111_decision.md"
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


def stage110_summary_lookup() -> dict[str, dict[str, str]]:
    return {
        row.get("adapter_id", ""): row
        for row in read_csv(SOURCE_STAGE110_SUMMARY)
        if row.get("split") == "oos" and row.get("view") == "actual_routed_total" and row.get("status") == "completed"
    }


def stage110_segment(adapter_id: str, segment_type: str, segment: str) -> dict[str, str]:
    for row in read_csv(SOURCE_STAGE110_SEGMENTS):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") != "oos" or row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") == segment_type and row.get("segment") == segment:
            return row
    return {}


def stage110_source_label(adapter_id: str) -> str:
    if adapter_id == "s110_v41_h3_cd9_lng53_early_adx19":
        return "stage110_long53_cd9_no_density_gain"
    if adapter_id == "s110_v41_h3_cd8_lng53_early_adx19":
        return "stage110_long53_cd8_small_density_gain"
    if adapter_id == "s110_v41_h3_cd8_lng53_early_adx18":
        return "stage110_long53_adx18_small_density_gain_early_damage"
    if adapter_id == "s110_v41_h3_cd9_both53_early_adx19":
        return "stage110_both53_cd9_no_extra_supply"
    return "stage110_candidate"


def stage110_metric_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for adapter_id, summary in stage110_summary_lookup().items():
        full = stage110_segment(adapter_id, "full_split", "actual_routed_total")
        early = stage110_segment(adapter_id, "chronological_third", "early")
        mid = stage110_segment(adapter_id, "chronological_third", "mid")
        late = stage110_segment(adapter_id, "chronological_third", "late")
        rows.append(
            {
                "source_stage": stage110_source_label(adapter_id),
                "source_run_id": PARENT_RUN_ID,
                "adapter_id": adapter_id,
                "profit_factor": num(full, "profit_factor", num(summary, "profit_factor")),
                "net_profit": num(full, "net_profit", num(summary, "net_profit")),
                "max_drawdown_percent": num(summary, "max_drawdown_percent"),
                "trade_count": num(full, "trade_count", num(summary, "trade_count")),
                "expectancy": num(full, "expectancy", num(summary, "expectancy")),
                "cost_stressed_expectancy": num(summary, "cost_stressed_expectancy"),
                "same_move_reentry_ratio": num(summary, "same_move_reentry_ratio"),
                "mfe_capture_ratio": num(full, "mfe_capture_ratio", num(summary, "mfe_capture_ratio")),
                "early_net_profit": num(early, "net_profit"),
                "early_profit_factor": num(early, "profit_factor"),
                "early_mfe_capture_ratio": num(early, "mfe_capture_ratio"),
                "mid_net_profit": num(mid, "net_profit"),
                "mid_profit_factor": num(mid, "profit_factor"),
                "late_net_profit": num(late, "net_profit"),
                "late_profit_factor": num(late, "profit_factor"),
            }
        )
    return rows


def row_read(row: Mapping[str, Any]) -> str:
    source = str(row.get("source_stage", ""))
    trades = num(row, "trade_count")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    early_pf = num(row, "early_profit_factor")
    density_delta = trades - REFERENCE_STAGE106_NET_PF["trade_count"]
    if source == "stage106_net_pf_best":
        return "reference_net_pf_good_but_trade_density_and_dd_gap_remain"
    if source == "stage106_dd_best":
        return "reference_dd_better_but_pf_below_34d_and_net_gap_remain"
    if density_delta <= 0:
        return "threshold_easing_did_not_increase_oos_trade_density"
    if density_delta <= 5 and early_pf < 1.10:
        return "small_density_gain_damaged_oos_early_quality"
    if density_delta <= 5 and net < REFERENCE_STAGE106_NET_PF["net_profit"]:
        return "small_density_gain_not_enough_and_net_lower"
    if dd > 16.5:
        return "density_probe_keeps_drawdown_gap_open"
    return "measurement_supports_further_review"


def comparison_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in [REFERENCE_STAGE106_NET_PF, REFERENCE_STAGE106_DD] + stage110_metric_rows():
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
                "cost_stressed_expectancy": fmt(num(source, "cost_stressed_expectancy")),
                "same_move_reentry_ratio": fmt(num(source, "same_move_reentry_ratio")),
                "mfe_capture_ratio": fmt(num(source, "mfe_capture_ratio")),
                "early_net_profit": fmt(early_net, 2),
                "early_profit_factor": fmt(early_pf),
                "early_mfe_capture_ratio": fmt(early_mfe),
                "mid_net_profit": fmt(num(source, "mid_net_profit"), 2),
                "mid_profit_factor": fmt(num(source, "mid_profit_factor")),
                "late_net_profit": fmt(num(source, "late_net_profit"), 2),
                "late_profit_factor": fmt(num(source, "late_profit_factor")),
                "pf_gap_to_34d_latest": fmt(pf - LEGACY_34D["profit_factor"]),
                "net_gap_to_34d_latest": fmt(net - LEGACY_34D["net_profit"], 2),
                "dd_gap_to_34d_latest": fmt(dd - LEGACY_34D["max_drawdown_percent"]),
                "trade_count_gap_to_34d_latest": fmt(trades - LEGACY_34D["trade_count"], 0),
                "density_delta_vs_stage106_net_pf_best": fmt(trades - REFERENCE_STAGE106_NET_PF["trade_count"], 0),
                "net_delta_vs_stage106_net_pf_best": fmt(net - REFERENCE_STAGE106_NET_PF["net_profit"], 2),
                "dd_delta_vs_stage106_net_pf_best": fmt(dd - REFERENCE_STAGE106_NET_PF["max_drawdown_percent"]),
                "early_pf_delta_vs_stage106_net_pf_best": fmt(early_pf - REFERENCE_STAGE106_NET_PF["early_profit_factor"]),
                "stage111_read": row_read(source),
            }
        )
    return rows


def tradeoff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        if not str(row.get("source_stage", "")).startswith("stage110"):
            continue
        density_delta = num(row, "density_delta_vs_stage106_net_pf_best")
        net_delta = num(row, "net_delta_vs_stage106_net_pf_best")
        early_delta = num(row, "early_pf_delta_vs_stage106_net_pf_best")
        output.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "source_stage": row.get("source_stage", ""),
                "trade_count": row.get("trade_count", ""),
                "density_delta_vs_stage106_net_pf_best": row.get("density_delta_vs_stage106_net_pf_best", ""),
                "net_profit": row.get("net_profit", ""),
                "net_delta_vs_stage106_net_pf_best": row.get("net_delta_vs_stage106_net_pf_best", ""),
                "profit_factor": row.get("profit_factor", ""),
                "max_drawdown_percent": row.get("max_drawdown_percent", ""),
                "early_profit_factor": row.get("early_profit_factor", ""),
                "early_pf_delta_vs_stage106_net_pf_best": row.get("early_pf_delta_vs_stage106_net_pf_best", ""),
                "tradeoff_read": tradeoff_read(density_delta, net_delta, early_delta),
            }
        )
    return output


def tradeoff_read(density_delta: float, net_delta: float, early_delta: float) -> str:
    if density_delta <= 0:
        return "no_density_gain"
    if density_delta <= 5 and net_delta < 0 and early_delta < 0:
        return "tiny_density_gain_with_net_and_early_damage"
    if density_delta <= 5:
        return "tiny_density_gain_not_34d_scale"
    return "density_gain_needs_new_review"


def best_density_candidate(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if str(row.get("source_stage", "")).startswith("stage110")]
    return max(candidates, key=lambda row: (num(row, "trade_count"), num(row, "net_profit")), default={})


def best_balanced_candidate(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if str(row.get("source_stage", "")).startswith("stage110")]
    return max(
        candidates,
        key=lambda row: (
            num(row, "profit_factor") >= LEGACY_34D["profit_factor"],
            num(row, "early_profit_factor"),
            num(row, "net_profit"),
            -num(row, "max_drawdown_percent"),
        ),
        default={},
    )


def report_markdown(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]]) -> str:
    best_density = best_density_candidate(rows)
    best_balanced = best_balanced_candidate(rows)
    stage110_rows = [row for row in rows if str(row.get("source_stage", "")).startswith("stage110")]
    table = "\n".join(
        "| {adapter} | {pf} | {net} | {dd} | {trades} | {density_delta} | {early_pf} | {read} |".format(
            adapter=row.get("adapter_id", ""),
            pf=row.get("profit_factor", ""),
            net=row.get("net_profit", ""),
            dd=row.get("max_drawdown_percent", ""),
            trades=row.get("trade_count", ""),
            density_delta=row.get("density_delta_vs_stage106_net_pf_best", ""),
            early_pf=row.get("early_profit_factor", ""),
            read=row.get("stage111_read", ""),
        )
        for row in stage110_rows
    )
    tradeoff_lines = "\n".join(
        f"- `{row.get('adapter_id', '')}`: {row.get('tradeoff_read', '')}"
        for row in tradeoffs
    )
    return f"""# Stage111 Trade Density Follow-up Review(111단계 거래 밀도 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE110_ID}`
- source_stage110_closeout_commit(원천 110단계 종료 커밋): `{SOURCE_STAGE110_CLOSEOUT_COMMIT}`
- source_stage110_latest_commit(원천 110단계 최신 커밋): `{SOURCE_STAGE110_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage110(110단계)의 threshold/session gate easing(임계값/세션 제한문 완화)이 34D KPI(34D 핵심 성과 지표) 목표 표면 대비 trade density/net scale(거래 밀도/순손익 규모)을 실제로 열었는가?

Effect(효과): 새 최적화가 아니라, 이미 끝난 Stage110 MT5 runtime evidence(110단계 MT5 실행환경 근거)를 판독해 다음 bounded repair(경계 수리)를 정한다.

## Target Surface(목표 표면)

- 34D PF(34D 수익 팩터): `{LEGACY_34D["profit_factor"]:.6f}`
- 34D net(34D 순손익): `{LEGACY_34D["net_profit"]:.2f}`
- 34D DD%(34D 손실률): `{LEGACY_34D["max_drawdown_percent"]:.6f}`
- 34D trades(34D 거래 수): `{LEGACY_34D["trade_count"]}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

## Stage110 Read(110단계 판독)

| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | density delta(거래 수 차이) | early PF(초반 수익 팩터) | read(판독) |
|---|---:|---:|---:|---:|---:|---:|---|
{table}

## Best Reads(최선 판독)

- best_density_candidate(거래 밀도 최선 후보): `{best_density.get("adapter_id", "")}` with trades(거래 수) `{best_density.get("trade_count", "")}` and early PF(초반 수익 팩터) `{best_density.get("early_profit_factor", "")}`.
- best_balanced_candidate(균형 최선 후보): `{best_balanced.get("adapter_id", "")}` with net(순손익) `{best_balanced.get("net_profit", "")}` and PF(수익 팩터) `{best_balanced.get("profit_factor", "")}`.

## Tradeoff(상충)

{tradeoff_lines}

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage110 threshold/session gate easing(110단계 임계값/세션 제한문 완화).
- evidence_available(있는 근거): Stage110 actual MT5 runtime reports(110단계 실제 MT5 실행환경 보고서), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), trade audit(거래 감사).
- evidence_missing(빠진 근거): 34D scale(34D 규모)에 가까운 trade supply(거래 공급)와 DD control(손실률 제어)을 동시에 보여주는 v2-native repair(브이투 고유 수리)는 아직 없다.
- judgment_label(판정 라벨): `threshold_easing_insufficient_trade_supply_repair_needed`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

## Decision(판정)

decision(판정): `{DECISION}`

Stage111(111단계)는 전체 목표 완료가 아니다. Effect(효과): threshold-only(임계값 전용) 완화가 막혔으므로, Stage112(112단계)는 route supply/session-side coverage(경로 공급/세션-방향 커버리지)를 좁게 수리한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown() -> str:
    return f"""# Stage111 Decision(111단계 판정)

decision(판정): `{DECISION}`

Stage111(111단계)는 Stage110(110단계)의 actual MT5 runtime result(실제 MT5 실행환경 결과)를 후속 검토했다.

Effect(효과): threshold/session gate easing(임계값/세션 제한문 완화)이 거래 수를 최대 `+5`개만 늘렸고, 34D KPI(34D 핵심 성과 지표)의 net/trade/DD(순손익/거래 수/손실률) 격차를 충분히 줄이지 못했음을 기록한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- source_stage110_report(원천 110단계 보고서): `{rel(SOURCE_STAGE110_REPORT)}`
- source_stage110_decision(원천 110단계 판정): `{rel(SOURCE_STAGE110_DECISION)}`
- source_stage110_closeout_commit(원천 110단계 종료 커밋): `{SOURCE_STAGE110_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def write_ledgers(best_density: Mapping[str, Any], best_balanced: Mapping[str, Any]) -> dict[str, Any]:
    now = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_trade_density_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": "Stage111 reviewed Stage110 trade density repair and routed to Stage112; research only.",
            }
        ],
        key="run_id",
    )
    ledger_notes = ledger_pairs(
        (
            ("target_surface", TARGET_SURFACE),
            ("decision", DECISION),
            ("best_density_adapter", best_density.get("adapter_id", "")),
            ("best_density_trades", best_density.get("trade_count", "")),
            ("best_balanced_adapter", best_balanced.get("adapter_id", "")),
            ("external_verification_status", EXTERNAL_STATUS),
            ("boundary", BOUNDARY),
        )
    )
    project_payload = upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage111_followup_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage111_followup_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "stage_followup_review",
                "tier_scope": "tier_a_only",
                "kpi_scope": "oos",
                "scoreboard_lane": "v2_native_34d_kpi_lesson_target",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "primary_kpi": ledger_pairs(
                    (
                        ("best_density_trades", best_density.get("trade_count", "")),
                        ("best_density_net", best_density.get("net_profit", "")),
                        ("best_balanced_pf", best_balanced.get("profit_factor", "")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("best_density_early_pf", best_density.get("early_profit_factor", "")),
                        ("best_balanced_dd", best_balanced.get("max_drawdown_percent", "")),
                    )
                ),
                "external_verification_status": EXTERNAL_STATUS,
                "notes": ledger_notes,
            }
        ],
        key="ledger_row_id",
    )
    write_csv(
        STAGE_LEDGER_PATH,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage111_followup_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage111_followup_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "stage_followup_review",
                "tier_scope": "tier_a_only",
                "kpi_scope": "oos",
                "scoreboard_lane": "v2_native_34d_kpi_lesson_target",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "primary_kpi": ledger_pairs(
                    (
                        ("best_density_trades", best_density.get("trade_count", "")),
                        ("best_density_net", best_density.get("net_profit", "")),
                        ("best_balanced_pf", best_balanced.get("profit_factor", "")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("best_density_early_pf", best_density.get("early_profit_factor", "")),
                        ("best_balanced_dd", best_balanced.get("max_drawdown_percent", "")),
                    )
                ),
                "external_verification_status": EXTERNAL_STATUS,
                "notes": ledger_notes,
            }
        ],
        ALPHA_LEDGER_COLUMNS,
    )
    stage_payload = {
        "path": rel(STAGE_LEDGER_PATH),
        "sha256": sha256_file_lf_normalized(STAGE_LEDGER_PATH),
        "hash_policy": "lf_normalized_text_register",
        "rows": 1,
        "upserted_rows": 1,
    }
    return {
        "run_registry": run_payload,
        "project_ledger": project_payload,
        "stage_ledger": stage_payload,
        "created_at_utc": now,
    }


def write_packet_files(best_density: Mapping[str, Any], best_balanced: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "primary_family": "adapter_research",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": ["obsidian-result-judgment", "obsidian-artifact-lineage"],
            "required_gates": ["result_judgment_gate", "runtime_evidence_gate"],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "external_verification_status": EXTERNAL_STATUS,
            "source_summary": rel(SOURCE_STAGE110_SUMMARY),
            "source_segments": rel(SOURCE_STAGE110_SEGMENTS),
            "status": "passed_for_followup_review",
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "decision": DECISION,
            "judgment_label": "threshold_easing_insufficient_trade_supply_repair_needed",
            "overall_goal_complete": False,
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
                "legacy_inheritance",
            ],
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage110_closeout_commit": SOURCE_STAGE110_CLOSEOUT_COMMIT,
            "source_stage110_latest_commit": SOURCE_STAGE110_LATEST_COMMIT,
            "best_density_candidate": best_density,
            "best_balanced_candidate": best_balanced,
            "ledger_payload": ledger_payload,
            "overall_goal_complete": False,
            "pushed_commit_hash": "pending_until_push",
        },
    )


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        REPORT_PATH,
        COMPARISON_PATH,
        TRADEOFF_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
        PACKET_ROOT / "routing_receipt.json",
        PACKET_ROOT / "runtime_evidence_gate.json",
        PACKET_ROOT / "result_judgment_gate.json",
        PACKET_ROOT / "aggregate_summary.json",
    ]
    rows = []
    for path in paths:
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.name}",
                "artifact_type": "stage111_trade_density_followup_review_evidence",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "Stage111 trade density follow-up review artifact; research only.",
            }
        )
    return rows


def update_artifact_registry() -> dict[str, Any]:
    return upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows(),
        key="artifact_id",
    )


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage112(112단계)는 Stage111(111단계)의 판정대로 route supply/session-side coverage(경로 공급/세션-방향 커버리지)를 좁게 수리한다.

## Bounded Question(경계 질문)

Threshold-only easing(임계값 전용 완화)이 거래 수를 열지 못한 뒤, v41 adapter(브이41 어댑터)는 side/session/context route supply(방향/세션/문맥 경로 공급)를 좁게 늘려 34D KPI(34D 핵심 성과 지표)의 trade density/net/DD(거래 밀도/순손익/손실률) 격차를 줄일 수 있는가?

Effect(효과): Stage112(112단계)는 새 모델 사냥(model hunting, 모델 탐색)이 아니라, Stage110(110단계) 실패 축을 받아 controlled route coverage repair(통제된 경로 커버리지 수리)만 수행한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage112 Input References(112단계 입력 참조)

- source_stage111_decision(원천 111단계 판정): `{rel(DECISION_PATH)}`
- source_stage111_report(원천 111단계 보고서): `{rel(REPORT_PATH)}`
- source_stage110_summary(원천 110단계 요약): `{rel(SOURCE_STAGE110_SUMMARY)}`
- source_stage110_segments(원천 110단계 구간): `{rel(SOURCE_STAGE110_SEGMENTS)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage112(112단계)는 Stage110/111(110/111단계) 근거에서 출발하고 legacy inheritance(레거시 상속)는 하지 않는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage112 Review Index(112단계 검토 색인)

- status(상태): `open_planned`
- expected_run(예상 실행): `{NEXT_RUN_ID}`
- expected_packet(예상 작업 묶음): `{NEXT_PACKET_ID}`
- boundary(경계): `{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage112 Selection Status(112단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage112(112단계)는 34D KPI(34D 핵심 성과 지표) 격차를 계속 줄이되, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage111(111단계) closed(종료) as `{DECISION}` and Stage112(112단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): threshold/session gate easing(임계값/세션 제한문 완화)이 거래 수를 충분히 열지 못해 route supply/session-side coverage(경로 공급/세션-방향 커버리지) 수리로 넘긴다.
- >-
  Stage111 result(111단계 결과)는 `{rel(COMPARISON_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 기록했다. Effect(효과): 거래 수 증가가 최대 +5개에 그친 사실을 다음 단계 입력으로 고정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage111_v41_trade_density_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage110_closeout_commit: {SOURCE_STAGE110_CLOSEOUT_COMMIT}
  source_stage110_latest_commit: {SOURCE_STAGE110_LATEST_COMMIT}
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
    marker = "stage111_v41_trade_density_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage111_v41_trade_density_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage111 Selection Status(111단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE110_ID}`
- source_decision(원천 판정): `continue_trade_density_repair_review_in_stage111`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage111_decision(111단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage111(111단계)는 Stage110(110단계) 실제 실행 결과를 판독하고, 운영 의미 없이 Stage112(112단계)로 넘긴다.
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
- adapter_under_review(검토 중 어댑터): `stage112_route_supply_density_repair_surface`
- status(상태): `stage111_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage111(111단계) closed(종료) as v2-native v41 trade density follow-up review(브이투 고유 브이41 거래 밀도 후속 검토). Effect(효과): threshold-only easing(임계값 전용 완화)은 34D KPI(34D 핵심 성과 지표) 격차를 충분히 줄이지 못했고, 다음 연구는 Stage112(112단계) route supply density repair(경로 공급 거래 밀도 수리)로 이어진다.

## Latest Stage111 Evidence(최신 111단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage111 v41 trade density follow-up review closeout(111단계 v41 거래 밀도 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage110(110단계) threshold/session gate easing(임계값/세션 제한문 완화)이 거래 수를 최대 +5개만 늘려 34D KPI(34D 핵심 성과 지표) 격차를 충분히 줄이지 못했으므로 Stage112(112단계) route supply density repair(경로 공급 거래 밀도 수리)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = comparison_rows()
    tradeoffs = tradeoff_rows(rows)
    best_density = best_density_candidate(rows)
    best_balanced = best_balanced_candidate(rows)
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
            "cost_stressed_expectancy",
            "same_move_reentry_ratio",
            "mfe_capture_ratio",
            "early_net_profit",
            "early_profit_factor",
            "early_mfe_capture_ratio",
            "mid_net_profit",
            "mid_profit_factor",
            "late_net_profit",
            "late_profit_factor",
            "pf_gap_to_34d_latest",
            "net_gap_to_34d_latest",
            "dd_gap_to_34d_latest",
            "trade_count_gap_to_34d_latest",
            "density_delta_vs_stage106_net_pf_best",
            "net_delta_vs_stage106_net_pf_best",
            "dd_delta_vs_stage106_net_pf_best",
            "early_pf_delta_vs_stage106_net_pf_best",
            "stage111_read",
        ),
    )
    write_csv(
        TRADEOFF_PATH,
        tradeoffs,
        (
            "run_id",
            "adapter_id",
            "source_stage",
            "trade_count",
            "density_delta_vs_stage106_net_pf_best",
            "net_profit",
            "net_delta_vs_stage106_net_pf_best",
            "profit_factor",
            "max_drawdown_percent",
            "early_profit_factor",
            "early_pf_delta_vs_stage106_net_pf_best",
            "tradeoff_read",
        ),
    )
    write_md(REPORT_PATH, report_markdown(rows, tradeoffs))
    write_md(DECISION_PATH, decision_markdown())
    ledger_payload = write_ledgers(best_density, best_balanced)
    write_packet_files(best_density, best_balanced, ledger_payload)
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
                    "best_density_candidate": best_density.get("adapter_id"),
                    "best_balanced_candidate": best_balanced.get("adapter_id"),
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
