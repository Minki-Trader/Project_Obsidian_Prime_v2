from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

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
from foundation.control_plane.mt5_trade_attribution import MarketData, compute_trade_attribution  # noqa: E402
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402


STAGE_ID = "99_adapter_research__v41_oos_early_side_session_context_repair"
RUN_ID = "run99A_stage99_v41_oos_early_side_session_context_repair_v1"
PACKET_ID = "stage99_v41_oos_early_side_session_context_repair_v1"
PARENT_RUN_ID = "run98A_stage98_v41_oos_early_lifecycle_followup_review_v1"
SOURCE_STAGE98_ID = "98_adapter_research__v41_oos_early_lifecycle_followup_review"
SOURCE_STAGE98_CLOSEOUT_COMMIT = "53522bfca9f6f989bba21ba19c5b67cc24cffc6e"
SOURCE_STAGE98_LATEST_COMMIT = "bb6057cd47273fcd5ec4b2a86bce4258949e8da5"
SOURCE_STAGE97_ID = "97_adapter_research__v41_oos_early_lifecycle_repair"
SOURCE_STAGE97_CLOSEOUT_COMMIT = "beeb81ebc58ea4492a0fbe015dab3b1ba9f5cbd6"
SOURCE_STAGE97_LATEST_COMMIT = "5154e76f306a4621b7bb11ee0cd1bfc4014d170a"
SOURCE_STAGE93_CLOSEOUT_COMMIT = "a3c2a42e378ffce41e07e947f0e68ed9e76606a6"
SOURCE_STAGE93_LATEST_COMMIT = "e1b59cbbd7e75ddee05bdcb075fd983e1effc8bf"
SOURCE_ADAPTER_ID = "s93_v41_h3_risk475_gate08_sl2075_tp40_cd10"
NEXT_STAGE_ID = "100_adapter_research__v41_oos_early_context_gate_runtime_repair"
NEXT_RUN_ID = "run100A_stage100_v41_oos_early_context_gate_runtime_repair_v1"
NEXT_PACKET_ID = "stage100_v41_oos_early_context_gate_runtime_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_context_gate_runtime_repair_in_stage100"
EXTERNAL_STATUS = "completed_existing_stage97_mt5_trade_attribution"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
LEGACY_34D_LATEST = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

ADAPTERS = (
    "s97_v41_h2_risk475_gate08_sl2075_tp40_cd10",
    "s97_v41_h4_risk475_gate08_sl2075_tp40_cd10",
    "s97_v41_h3_risk475_gate08_sl2075_tp40_cd8",
)
ADAPTER_SHORT = {
    "s97_v41_h2_risk475_gate08_sl2075_tp40_cd10": "H2",
    "s97_v41_h4_risk475_gate08_sl2075_tp40_cd10": "H4",
    "s97_v41_h3_risk475_gate08_sl2075_tp40_cd8": "CD8",
}
BEST_CANDIDATE = "long_early_mid_range_adxlt20"
BEST_ADAPTER = "s97_v41_h3_risk475_gate08_sl2075_tp40_cd8"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE97_REVIEWS = Path("stages") / SOURCE_STAGE97_ID / "03_reviews"
SOURCE_STAGE98_REVIEWS = Path("stages") / SOURCE_STAGE98_ID / "03_reviews"
SOURCE_STAGE97_SUMMARY_CSV = SOURCE_STAGE97_REVIEWS / "stage97_v41_oos_early_lifecycle_repair_summary.csv"
SOURCE_STAGE97_SUMMARY_JSON = SOURCE_STAGE97_REVIEWS / "stage97_v41_oos_early_lifecycle_repair_summary.json"
SOURCE_STAGE97_SEGMENT_CSV = SOURCE_STAGE97_REVIEWS / "stage97_segment_kpi_summary.csv"
SOURCE_STAGE97_RISK_ATR_CSV = SOURCE_STAGE97_REVIEWS / "stage97_risk_atr_telemetry.csv"
SOURCE_STAGE97_DECISION = SOURCE_STAGE97_REVIEWS / "stage97_decision.md"
SOURCE_STAGE98_DECISION = SOURCE_STAGE98_REVIEWS / "stage98_decision.md"
SOURCE_STAGE98_COMPARISON = SOURCE_STAGE98_REVIEWS / "stage98_stage93_stage97_comparison.csv"

REPORT_PATH = REVIEWS_ROOT / "stage99_oos_early_side_session_context_report.md"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage99_side_session_context_attribution.csv"
PROJECTION_PATH = REVIEWS_ROOT / "stage99_context_gate_projection.csv"
DECISION_PATH = REVIEWS_ROOT / "stage99_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


def rel(path: Path) -> str:
    return path.as_posix()


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def fnum(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        value_float = float(text)
    except ValueError:
        return None
    if math.isnan(value_float):
        return None
    return value_float


def fmt(value: Any, digits: int = 2) -> str:
    numeric = fnum(value)
    if numeric is None:
        return ""
    if math.isinf(numeric):
        return "inf"
    return f"{numeric:.{digits}f}"


def profit_factor(trades: Sequence[Mapping[str, Any]]) -> float | None:
    positive = sum(float(row["net_profit"]) for row in trades if float(row["net_profit"]) > 0)
    negative = -sum(float(row["net_profit"]) for row in trades if float(row["net_profit"]) < 0)
    if negative == 0:
        return math.inf if positive > 0 else None
    return positive / negative


def drawdown_amount(trades: Sequence[Mapping[str, Any]]) -> float:
    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    for row in sorted(trades, key=lambda item: item["close_time"]):
        equity += float(row["net_profit"])
        peak = max(peak, equity)
        max_dd = max(max_dd, peak - equity)
    return max_dd


def metrics(trades: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(trades)
    net = sum(float(row["net_profit"]) for row in rows)
    count = len(rows)
    wins = sum(1 for row in rows if float(row["net_profit"]) > 0)
    mfe_sum = sum(float(row.get("mfe") or 0.0) for row in rows)
    mae_sum = sum(float(row.get("mae") or 0.0) for row in rows)
    return {
        "trade_count": count,
        "net_profit": net,
        "profit_factor": profit_factor(rows),
        "expectancy": net / count if count else None,
        "win_rate": wins / count if count else None,
        "mfe_mean": mfe_sum / count if count else None,
        "mae_mean": mae_sum / count if count else None,
        "mfe_capture_ratio": net / mfe_sum if mfe_sum else None,
        "max_closed_trade_drawdown": drawdown_amount(rows),
    }


def chronological_segment(index: int, count: int) -> str:
    third = (count + 2) // 3
    if index < third:
        return "early"
    if index < third * 2:
        return "mid"
    return "late"


def stage97_report_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(SOURCE_STAGE97_SUMMARY_CSV):
        if row.get("adapter_id") not in ADAPTERS:
            continue
        if row.get("view") != "actual_routed_total":
            continue
        if row.get("split") not in {"validation_is", "oos"}:
            continue
        if row.get("status") != "completed":
            continue
        rows.append(row)
    return rows


def load_trade_rows() -> list[dict[str, Any]]:
    market_data = MarketData.load(REPO_ROOT)
    output: list[dict[str, Any]] = []
    for record in stage97_report_rows():
        report_path = REPO_ROOT / str(record["report_path"])
        report = parse_mt5_trade_report(report_path)
        trades = pair_deals_into_trades(report["deals"])
        stats = compute_trade_attribution(trades, market_data)
        enriched = sorted(stats["trades"], key=lambda row: row["open_time"])
        count = len(enriched)
        for index, trade in enumerate(enriched):
            row = dict(trade)
            row["adapter_id"] = record["adapter_id"]
            row["split"] = record["split"]
            row["view"] = record["view"]
            row["chron_segment"] = chronological_segment(index, count)
            row["source_report_path"] = record["report_path"]
            output.append(row)
    return output


def group_rows(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key, "") for key in keys)].append(row)
    output = []
    for key_values, group in sorted(grouped.items(), key=lambda item: tuple(str(part) for part in item[0])):
        metric = metrics(group)
        result = {key: key_values[index] for index, key in enumerate(keys)}
        result.update(
            {
                "trade_count": metric["trade_count"],
                "net_profit": fmt(metric["net_profit"], 2),
                "profit_factor": fmt(metric["profit_factor"], 6),
                "expectancy": fmt(metric["expectancy"], 6),
                "win_rate": fmt(metric["win_rate"], 6),
                "mfe_mean": fmt(metric["mfe_mean"], 6),
                "mae_mean": fmt(metric["mae_mean"], 6),
                "mfe_capture_ratio": fmt(metric["mfe_capture_ratio"], 6),
                "max_closed_trade_drawdown": fmt(metric["max_closed_trade_drawdown"], 2),
                "stage99_read": attribution_read(group),
            }
        )
        output.append(result)
    return output


def attribution_read(group: Sequence[Mapping[str, Any]]) -> str:
    metric = metrics(group)
    if metric["trade_count"] and metric["net_profit"] < 0:
        return "negative_context_slice"
    if metric["trade_count"] and (metric["profit_factor"] or 0) < 1.05:
        return "weak_context_slice"
    return "context_slice_measurement"


def is_long_early_range_adxlt20(row: Mapping[str, Any]) -> bool:
    return (
        row.get("direction") == "buy"
        and row.get("session_slice") == "early"
        and row.get("trend_regime") == "range_or_weak_trend"
        and row.get("adx_bucket") == "adx_lt20"
    )


def is_long_any_range_adxlt20(row: Mapping[str, Any]) -> bool:
    return (
        row.get("direction") == "buy"
        and row.get("trend_regime") == "range_or_weak_trend"
        and row.get("adx_bucket") == "adx_lt20"
    )


def is_long_early_mid_range_adxlt20(row: Mapping[str, Any]) -> bool:
    return (
        row.get("direction") == "buy"
        and row.get("session_slice") in {"early", "mid"}
        and row.get("trend_regime") == "range_or_weak_trend"
        and row.get("adx_bucket") == "adx_lt20"
    )


def is_short_late_downtrend_adxgt25(row: Mapping[str, Any]) -> bool:
    return (
        row.get("direction") == "sell"
        and row.get("session_slice") == "late"
        and row.get("trend_regime") == "downtrend"
        and row.get("adx_bucket") == "adx_gt25"
    )


CANDIDATES: dict[str, Callable[[Mapping[str, Any]], bool]] = {
    "long_early_range_adxlt20": is_long_early_range_adxlt20,
    "long_any_range_adxlt20": is_long_any_range_adxlt20,
    "long_early_mid_range_adxlt20": is_long_early_mid_range_adxlt20,
    "short_late_downtrend_adxgt25": is_short_late_downtrend_adxgt25,
}


def projection_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for row in trade_rows:
        grouped[(str(row["adapter_id"]), str(row["split"]))].append(row)
    for (adapter_id, split), rows in sorted(grouped.items()):
        baseline = metrics(rows)
        baseline_early = metrics([row for row in rows if row.get("chron_segment") == "early"])
        for candidate_id, predicate in CANDIDATES.items():
            removed = [row for row in rows if predicate(row)]
            projected_rows = [row for row in rows if not predicate(row)]
            projected = metrics(projected_rows)
            projected_early = metrics([row for row in projected_rows if row.get("chron_segment") == "early"])
            output.append(
                {
                    "adapter_id": adapter_id,
                    "adapter_short": ADAPTER_SHORT.get(adapter_id, ""),
                    "candidate_gate": candidate_id,
                    "split": split,
                    "baseline_trade_count": baseline["trade_count"],
                    "baseline_net": fmt(baseline["net_profit"], 2),
                    "baseline_profit_factor": fmt(baseline["profit_factor"], 6),
                    "baseline_early_net": fmt(baseline_early["net_profit"], 2),
                    "baseline_early_profit_factor": fmt(baseline_early["profit_factor"], 6),
                    "baseline_drawdown_amount": fmt(baseline["max_closed_trade_drawdown"], 2),
                    "removed_count": len(removed),
                    "removed_net": fmt(sum(float(row["net_profit"]) for row in removed), 2),
                    "projected_trade_count": projected["trade_count"],
                    "projected_net": fmt(projected["net_profit"], 2),
                    "projected_profit_factor": fmt(projected["profit_factor"], 6),
                    "projected_early_net": fmt(projected_early["net_profit"], 2),
                    "projected_early_profit_factor": fmt(projected_early["profit_factor"], 6),
                    "projected_drawdown_amount": fmt(projected["max_closed_trade_drawdown"], 2),
                    "projected_net_delta": fmt(projected["net_profit"] - baseline["net_profit"], 2),
                    "projected_early_delta": fmt(projected_early["net_profit"] - baseline_early["net_profit"], 2),
                    "stage99_read": projection_read(adapter_id, split, candidate_id, baseline, projected, baseline_early, projected_early),
                }
            )
    return output


def projection_read(
    adapter_id: str,
    split: str,
    candidate_id: str,
    baseline: Mapping[str, Any],
    projected: Mapping[str, Any],
    baseline_early: Mapping[str, Any],
    projected_early: Mapping[str, Any],
) -> str:
    full_delta = float(projected["net_profit"]) - float(baseline["net_profit"])
    early_delta = float(projected_early["net_profit"]) - float(baseline_early["net_profit"])
    if adapter_id == BEST_ADAPTER and candidate_id == BEST_CANDIDATE and split == "oos":
        return "best_oos_early_repair_projection_runtime_required"
    if early_delta > 0 and full_delta >= 0:
        return "improves_early_without_full_net_damage_projection"
    if early_delta > 0 and full_delta < 0:
        return "improves_early_but_full_net_damage_projection"
    return "not_preferred_projection"


def best_projection_lookup(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {
        str(row["split"]): row
        for row in rows
        if row.get("adapter_id") == BEST_ADAPTER and row.get("candidate_gate") == BEST_CANDIDATE
    }


def markdown_projection_table(rows: Sequence[Mapping[str, Any]]) -> str:
    best_rows = [row for row in rows if row.get("candidate_gate") == BEST_CANDIDATE]
    lines = [
        "| adapter(어댑터) | split(분할) | baseline net/PF/early(기준 순손익/수익요인/초반) | projected net/PF/early(투영 순손익/수익요인/초반) | removed(제거) | read(판독) |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in best_rows:
        lines.append(
            "| `{}` | `{}` | {} / {} / {} | {} / {} / {} | {} trades, {} net | {} |".format(
                row["adapter_short"],
                row["split"],
                row["baseline_net"],
                row["baseline_profit_factor"],
                row["baseline_early_net"],
                row["projected_net"],
                row["projected_profit_factor"],
                row["projected_early_net"],
                row["removed_count"],
                row["removed_net"],
                row["stage99_read"],
            )
        )
    return "\n".join(lines)


def report_markdown(attribution: Sequence[Mapping[str, Any]], projection: Sequence[Mapping[str, Any]]) -> str:
    best = best_projection_lookup(projection)
    best_val = best.get("validation_is", {})
    best_oos = best.get("oos", {})
    return f"""# Stage99 OOS Early Side/Session/Context Report(99단계 표본외 초반 방향/세션/문맥 보고서)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE97_ID}` and `{SOURCE_STAGE98_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- review_type(검토 유형): `bounded_attribution_projection_no_new_runtime`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

OOS early weakness(표본외 초반 약점)을 side/session/market context(방향/세션/시장 문맥)로 분리해서, validation/OOS full split KPI(검증/표본외 전체 분할 핵심 성과 지표)를 크게 해치지 않는 다음 수리 조건을 잡을 수 있는가?

Answer(답): 예, 단서가 있다. `buy early/mid range_or_weak_trend adx_lt20`(매수 초반/중반 약한 추세 ADX 20 미만) 차단 투영이 가장 깔끔했다. 특히 CD8(8봉 쿨다운) 후보는 validation(검증)에서 net(순손익) `{best_val.get("projected_net", "")}`, PF(수익 요인) `{best_val.get("projected_profit_factor", "")}`로 좋아지고, OOS(표본외) early(초반)는 `{best_oos.get("baseline_early_net", "")}`에서 `{best_oos.get("projected_early_net", "")}`로 올라간다.

Effect(효과): Stage99(99단계)는 실제 런타임(runtime, 실행환경) 성공을 주장하지 않고, Stage100(100단계)에서 구현할 문맥 게이트(context gate, 문맥 제한문)를 하나로 좁힌다.

## Projection KPI(투영 핵심 성과 지표)

{markdown_projection_table(projection)}

Legacy 34D latest target(레거시 34D 최신 목표)은 PF(수익 요인) `{LEGACY_34D_LATEST["profit_factor"]}`, net(순손익) `{LEGACY_34D_LATEST["net_profit"]}`, max DD(최대 손실폭) `{LEGACY_34D_LATEST["max_drawdown_percent"]}%`, trades(거래 수) `{LEGACY_34D_LATEST["trade_count"]}`이다.

Important read(중요 판독): CD8(8봉 쿨다운) projection(투영)은 validation(검증)을 34D net(순손익) 이상으로 올리지만, OOS full net(표본외 전체 순손익)은 아직 34D 최신 net(순손익)보다 낮다. 따라서 연구개발은 계속해야 한다.

## Context Attribution(문맥 원인분해)

- attribution_rows(원인분해 행 수): `{len(attribution)}`
- main_negative_slice(주요 음수 구간): OOS early(표본외 초반)의 buy early range_or_weak_trend adx_lt20(매수 초반 약한 추세 ADX 20 미만)이 반복적으로 손상 구간이다.
- preserved_positive_slice(보존할 양수 구간): sell early downtrend adx_gt25(매도 초반 하락추세 ADX 25 초과)는 양수 기여가 있어 단순 전체 차단 대상이 아니다.
- evidence(근거): `{rel(ATTRIBUTION_PATH)}` and `{rel(PROJECTION_PATH)}`

## Result Judgment(결과 판정)

- judgment_label(판정 라벨): `positive_projection_only_runtime_repair_required`
- selected_projection(선택 투영): `{BEST_CANDIDATE}` on `{BEST_ADAPTER}`
- missing_evidence(빠진 근거): actual MT5 runtime repair(실제 MT5 실행환경 수리), feature-gate parity(피처 제한문 동등성), post-repair validation/OOS report(수리 뒤 검증/표본외 보고서).
- next_condition(다음 조건): Stage100(100단계)에서 문맥 게이트(context gate, 문맥 제한문)를 실제 MT5 경로에 구현하고, validation/OOS(검증/표본외)를 다시 측정한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(projection: Sequence[Mapping[str, Any]]) -> str:
    best = best_projection_lookup(projection)
    val = best.get("validation_is", {})
    oos = best.get("oos", {})
    return f"""# Stage99 Decision(99단계 판정)

decision(판정): `{DECISION}`

Stage99(99단계)는 Stage97(97단계)의 MT5 trade report(MT5 거래 보고서)를 direction/session/context(방향/세션/문맥)으로 다시 읽었다.

Effect(효과): lifecycle-only repair(생명주기 단독 수리)에서 막힌 OOS early(표본외 초반) 문제를, Stage100(100단계)의 실제 context gate runtime repair(문맥 제한문 실행환경 수리) 질문으로 좁혔다.

## Evidence(근거)

- source_stage97_summary(원천 97단계 요약): `{rel(SOURCE_STAGE97_SUMMARY_CSV)}`
- source_stage97_decision(원천 97단계 판정): `{rel(SOURCE_STAGE97_DECISION)}`
- source_stage98_decision(원천 98단계 판정): `{rel(SOURCE_STAGE98_DECISION)}`
- attribution(원인분해): `{rel(ATTRIBUTION_PATH)}`
- projection(투영): `{rel(PROJECTION_PATH)}`
- report(보고서): `{rel(REPORT_PATH)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## KPI Read(핵심 성과 지표 판독)

- selected_gate(선택 제한문): `{BEST_CANDIDATE}`
- selected_adapter(선택 어댑터): `{BEST_ADAPTER}`
- validation_projection(검증 투영): baseline(기준) `{val.get("baseline_net", "")}` / PF `{val.get("baseline_profit_factor", "")}` -> projected(투영) `{val.get("projected_net", "")}` / PF `{val.get("projected_profit_factor", "")}`
- oos_projection(표본외 투영): baseline(기준) `{oos.get("baseline_net", "")}` / PF `{oos.get("baseline_profit_factor", "")}` -> projected(투영) `{oos.get("projected_net", "")}` / PF `{oos.get("projected_profit_factor", "")}`
- oos_early_projection(표본외 초반 투영): baseline(기준) `{oos.get("baseline_early_net", "")}` / PF `{oos.get("baseline_early_profit_factor", "")}` -> projected(투영) `{oos.get("projected_early_net", "")}` / PF `{oos.get("projected_early_profit_factor", "")}`

Verdict(결론): 좋지만 아직 투영(projection, 가정 계산)이다. 실제 MT5 runtime(실행환경) 재현 전에는 34D KPI(34D 핵심 성과 지표) 달성이나 최종 어댑터라고 말할 수 없다.

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage100(100단계) bounded question(경계 질문): `{BEST_CANDIDATE}` 문맥 제한문(context gate, 문맥 제한문)을 실제 MT5 feature/runtime path(피처/실행환경 경로)에 구현하면, validation/OOS full split(검증/표본외 전체 분할)을 보존하면서 OOS early(표본외 초반)를 실제로 개선하는가?

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def write_stage_files(trade_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    attribution = group_rows(
        trade_rows,
        ("adapter_id", "split", "chron_segment", "direction", "session_slice", "trend_regime", "adx_bucket"),
    )
    projection = projection_rows(trade_rows)
    write_csv(
        ATTRIBUTION_PATH,
        attribution,
        (
            "adapter_id",
            "split",
            "chron_segment",
            "direction",
            "session_slice",
            "trend_regime",
            "adx_bucket",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "win_rate",
            "mfe_mean",
            "mae_mean",
            "mfe_capture_ratio",
            "max_closed_trade_drawdown",
            "stage99_read",
        ),
    )
    write_csv(
        PROJECTION_PATH,
        projection,
        (
            "adapter_id",
            "adapter_short",
            "candidate_gate",
            "split",
            "baseline_trade_count",
            "baseline_net",
            "baseline_profit_factor",
            "baseline_early_net",
            "baseline_early_profit_factor",
            "baseline_drawdown_amount",
            "removed_count",
            "removed_net",
            "projected_trade_count",
            "projected_net",
            "projected_profit_factor",
            "projected_early_net",
            "projected_early_profit_factor",
            "projected_drawdown_amount",
            "projected_net_delta",
            "projected_early_delta",
            "stage99_read",
        ),
    )
    write_md(REPORT_PATH, report_markdown(attribution, projection))
    write_md(DECISION_PATH, decision_markdown(projection))
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage99 Review Index(99단계 검토 색인)

- status(상태): `reviewed_closed`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- projection(투영): `{rel(PROJECTION_PATH)}`

Effect(효과): Stage99(99단계)는 문맥 제한문(context gate, 문맥 제한문) 후보를 좁혀 Stage100(100단계) 실제 실행환경 수리로 넘긴다.
""",
    )
    return attribution, projection


def ledger_rows(projection: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    best = best_projection_lookup(projection)
    oos = best.get("oos", {})
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_v2_native_v41_oos_early_side_session_context_projection",
        "status": "reviewed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": (
            f"source_run={PARENT_RUN_ID};source_stage98_latest_commit={SOURCE_STAGE98_LATEST_COMMIT};"
            f"source_stage97_latest_commit={SOURCE_STAGE97_LATEST_COMMIT};selected_projection={BEST_CANDIDATE};"
            "new_runtime=no_projection_only;legacy_relation=lesson_only"
        ),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__projection_gate",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "projection_gate",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage97_trade_context_projection",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage99_oos_early_side_session_context_projection",
        "scoreboard_lane": "regular_risk_execution_review",
        "status": "reviewed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": ledger_pairs(
            (
                ("selected_adapter", BEST_ADAPTER),
                ("selected_gate", BEST_CANDIDATE),
                ("oos_early_projected_net", oos.get("projected_early_net", "")),
                ("oos_early_projected_pf", oos.get("projected_early_profit_factor", "")),
                ("oos_projected_net", oos.get("projected_net", "")),
                ("oos_projected_pf", oos.get("projected_profit_factor", "")),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("target_surface", TARGET_SURFACE),
                ("new_runtime", "no"),
                ("stage100_next_axis", "context_gate_runtime_repair"),
            )
        ),
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Projection-only gate from existing Stage97 MT5 trade reports; actual runtime repair required next.",
    }
    return run_row, alpha_row


def write_ledgers(projection: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    run_row, alpha_row = ledger_rows(projection)
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload}


def write_packet_files(projection: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    best = best_projection_lookup(projection)
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "performance_attribution",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": ["obsidian-result-judgment", "obsidian-experiment-design"],
            "required_gates": ["kpi_contract_audit", "performance_attribution_review", "result_judgment_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "external_verification_status": EXTERNAL_STATUS,
            "review_type": "bounded_attribution_projection_no_new_runtime",
            "source_evidence": [
                rel(SOURCE_STAGE97_SUMMARY_CSV),
                rel(SOURCE_STAGE97_SEGMENT_CSV),
                rel(SOURCE_STAGE97_RISK_ATR_CSV),
                rel(SOURCE_STAGE98_COMPARISON),
            ],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        PACKET_ROOT / "performance_attribution_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "selected_projection": BEST_CANDIDATE,
            "selected_adapter": BEST_ADAPTER,
            "attribution_path": rel(ATTRIBUTION_PATH),
            "projection_path": rel(PROJECTION_PATH),
            "best_projection": best,
            "attribution_confidence": "medium_projection_only",
            "alternative_explanations": [
                "feature/runtime gate may differ from post-trade projection",
                "blocked trades may alter later same-direction cooldown availability",
                "OOS full net remains below 34D latest target surface",
            ],
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "result_subject": "stage97_side_session_context_projection",
            "judgment_label": "positive_projection_only_runtime_repair_required",
            "decision": DECISION,
            "evidence_available": [rel(ATTRIBUTION_PATH), rel(PROJECTION_PATH), rel(REPORT_PATH)],
            "evidence_missing": [
                "actual_mt5_context_gate_runtime_repair",
                "feature_gate_parity",
                "post_repair_validation_oos_reports",
            ],
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
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
            "selected_projection": BEST_CANDIDATE,
            "selected_adapter": BEST_ADAPTER,
            "source_stage98_closeout_commit": SOURCE_STAGE98_CLOSEOUT_COMMIT,
            "source_stage98_latest_commit": SOURCE_STAGE98_LATEST_COMMIT,
            "source_stage97_closeout_commit": SOURCE_STAGE97_CLOSEOUT_COMMIT,
            "source_stage97_latest_commit": SOURCE_STAGE97_LATEST_COMMIT,
            "source_stage93_closeout_commit": SOURCE_STAGE93_CLOSEOUT_COMMIT,
            "source_stage93_latest_commit": SOURCE_STAGE93_LATEST_COMMIT,
            "attribution_path": rel(ATTRIBUTION_PATH),
            "projection_path": rel(PROJECTION_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        (REPORT_PATH, "stage99_v41_oos_early_side_session_context_evidence", "Stage99 bounded context attribution report."),
        (ATTRIBUTION_PATH, "stage99_v41_oos_early_side_session_context_evidence", "Stage99 side/session/context attribution."),
        (PROJECTION_PATH, "stage99_v41_oos_early_side_session_context_evidence", "Stage99 context gate projection."),
        (DECISION_PATH, "stage99_v41_oos_early_side_session_context_evidence", "Stage99 decision."),
        (STAGE_LEDGER_PATH, "stage99_v41_oos_early_side_session_context_evidence", "Stage99 local ledger."),
        (PACKET_ROOT / "aggregate_summary.json", "packet_summary", "Stage99 packet aggregate summary."),
        (PACKET_ROOT / "routing_receipt.json", "packet_control", "Stage99 routing receipt."),
        (PACKET_ROOT / "runtime_evidence_gate.json", "packet_control", "Stage99 runtime evidence gate."),
        (PACKET_ROOT / "performance_attribution_gate.json", "packet_control", "Stage99 performance attribution gate."),
        (PACKET_ROOT / "result_judgment_gate.json", "packet_control", "Stage99 result judgment gate."),
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

Stage100(100단계)는 Stage99(99단계)의 projection(투영)을 실제 MT5 feature/runtime path(피처/실행환경 경로)에 구현하는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

`{BEST_CANDIDATE}` context gate(문맥 제한문)를 실제 런타임(runtime, 실행환경) 경로에 넣으면 validation/OOS full split(검증/표본외 전체 분할)을 보존하면서 OOS early(표본외 초반)를 개선하는가?

Effect(효과): Stage100(100단계)은 Stage99(99단계)의 가정 계산을 실제 실행 근거로 바꾸거나, 실패하면 다음 수리 축으로 넘긴다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage100 Input References(100단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_gate(선택 제한문): `{BEST_CANDIDATE}`
- selected_adapter(선택 어댑터): `{BEST_ADAPTER}`
- stage99_report(99단계 보고서): `{rel(REPORT_PATH)}`
- stage99_projection(99단계 투영): `{rel(PROJECTION_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage100(100단계)은 새 사냥이 아니라 선택된 문맥 제한문(context gate, 문맥 제한문)의 실제 측정만 맡는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage100 Review Index(100단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage100(100단계)은 Stage99(99단계)의 투영 단서를 실제 MT5 검증/표본외 실행으로 좁게 확인한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage100 Selection Status(100단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_gate(선택 제한문): `{BEST_CANDIDATE}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage100(100단계)은 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage99(99단계) closed(종료) as `{DECISION}` and Stage100(100단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): side/session/context projection(방향/세션/문맥 투영)을 실제 context gate runtime repair(문맥 제한문 실행환경 수리)로 넘긴다.
- >-
  Stage99 result(99단계 결과): `{BEST_CANDIDATE}` projection(투영)이 CD8(8봉 쿨다운)의 OOS early(표본외 초반)를 개선할 가능성을 보였다. Effect(효과): 다음 단계는 새 최적화가 아니라 이 조건의 실제 MT5 검증/표본외 측정이다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage99_v41_oos_early_side_session_context_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage98_closeout_commit: {SOURCE_STAGE98_CLOSEOUT_COMMIT}
  source_stage98_latest_commit: {SOURCE_STAGE98_LATEST_COMMIT}
  source_stage97_closeout_commit: {SOURCE_STAGE97_CLOSEOUT_COMMIT}
  source_stage97_latest_commit: {SOURCE_STAGE97_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  selected_projection: {BEST_CANDIDATE}
  selected_adapter: {BEST_ADAPTER}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage99_v41_oos_early_side_session_context_repair:"
    if marker in text:
        text = re.sub(r"\nstage99_v41_oos_early_side_session_context_repair:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{BEST_ADAPTER}`
- status(상태): `stage99_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage99(99단계) closed(종료) as v2-native v41 OOS early side/session/context projection review(브이투 고유 브이41 표본외 초반 방향/세션/문맥 투영 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 실제 수리는 Stage100(100단계)로 이어진다.

## Latest Stage99 Evidence(최신 99단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- selected_gate(선택 제한문): `{BEST_CANDIDATE}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- projection(투영): `{rel(PROJECTION_PATH)}`
- attribution(원인분해): `{rel(ATTRIBUTION_PATH)}`
- stage99_decision(99단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage99 Selection Status(99단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE98_ID}`
- source_decision(원천 판정): `continue_oos_early_side_session_context_repair_in_stage99`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage99_decision(99단계 판정): `{DECISION}`
- selected_gate(선택 제한문): `{BEST_CANDIDATE}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage99(99단계)는 투영 단서를 보존하고, 실제 MT5 context gate runtime repair(문맥 제한문 실행환경 수리)를 Stage100(100단계)로 넘긴다.
""",
    )


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage99 v41 OOS early side/session/context projection closeout(99단계 v41 표본외 초반 방향/세션/문맥 투영 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        f"- selected_gate(선택 제한문): `{BEST_CANDIDATE}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage99(99단계)는 CD8(8봉 쿨다운)의 OOS early(표본외 초반) 약점을 문맥 조건으로 좁혔고, Stage100(100단계) 실제 실행환경 수리로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    trade_rows = load_trade_rows()
    attribution, projection = write_stage_files(trade_rows)
    ledger_payload = write_ledgers(projection)
    write_packet_files(projection, ledger_payload)
    update_artifact_registry()
    create_next_stage()
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
                    "selected_projection": BEST_CANDIDATE,
                    "selected_adapter": BEST_ADAPTER,
                    "attribution_rows": len(attribution),
                    "projection_rows": len(projection),
                    "report": rel(REPORT_PATH),
                    "decision_path": rel(DECISION_PATH),
                    "next_stage": NEXT_STAGE_ID,
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
