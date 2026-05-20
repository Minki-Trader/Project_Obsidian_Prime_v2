from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage267 import run267C_p0_mt5_full_batch_review as p0_review
from stage_pipelines.stage267 import run267C_p1_soft_axis_followup_executor as executor
from stage_pipelines.stage267 import run267C_p1_soft_axis_followup_materialization as p1


STAGE_ID = p1.STAGE_ID
RUN_ID = p1.RUN_ID
CLAIM_BOUNDARY = p1.CLAIM_BOUNDARY
P1_ROOT = p1.P1_ROOT
REVIEWS_ROOT = p1.REVIEWS_ROOT
BASE_KPI_PATH = p1.RUN267B_HIST_ROOT / "mt5_kpi_summary.csv"
P1_KPI_PATH = executor.KPI_SUMMARY_PATH
P0_SUMMARY_PATH = p0_review.SUMMARY_PATH
P1_FEATURE_MANIFEST_PATH = p1.FEATURE_VARIANT_MANIFEST_PATH
DETAIL_PATH = P1_ROOT / "p1_soft_axis_delta_review.csv"
SUMMARY_PATH = P1_ROOT / "p1_soft_axis_candidate_variant_summary.csv"
AXIS_PATH = P1_ROOT / "p1_soft_axis_axis_summary.csv"
RESULT_PATH = P1_ROOT / "p1_soft_axis_followup_review.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267C_p1_soft_axis_followup_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267C_p1_soft_axis_followup_review.py")

STATUS = "run267C_p1_soft_axis_followup_review_completed"
NEXT_ACTION = "run267C_select_p1_axes_for_adapter_prototype_or_p2_replacement"

VARIANT_META = {
    "lateadx": {
        "followup_variant_id": "p1_late_adx20_25_soft_filter",
        "label": "late-session plus ADX 20-25 soft filter(후반 세션과 ADX 20-25 부드러운 필터)",
        "source_p0_axis": "lateblk",
        "primary_p0_axis": "lateblk",
        "secondary_p0_axis": "",
    },
    "late21": {
        "followup_variant_id": "p1_late_hour21_soft_filter",
        "label": "late-session hour 21 soft filter(후반 세션 21시 부드러운 필터)",
        "source_p0_axis": "lateblk",
        "primary_p0_axis": "lateblk",
        "secondary_p0_axis": "",
    },
    "vlowadx": {
        "followup_variant_id": "p1_vol_low_adx20_25_soft_filter",
        "label": "low-volatility plus ADX 20-25 soft filter(낮은 변동성과 ADX 20-25 부드러운 필터)",
        "source_p0_axis": "vollowblk",
        "primary_p0_axis": "vollowblk",
        "secondary_p0_axis": "",
    },
    "atrcomp": {
        "followup_variant_id": "p1_atr_compression_replacement_filter",
        "label": "ATR compression replacement filter(ATR 압축 대체 필터)",
        "source_p0_axis": "vollowblk",
        "primary_p0_axis": "vollowblk",
        "secondary_p0_axis": "",
    },
    "latevlow": {
        "followup_variant_id": "p1_late_vol_low_intersection_filter",
        "label": "late-session low-volatility intersection filter(후반 세션 낮은 변동성 교차 필터)",
        "source_p0_axis": "lateblk+vollowblk",
        "primary_p0_axis": "vollowblk",
        "secondary_p0_axis": "lateblk",
    },
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def to_float(row: Mapping[str, Any] | None, key: str) -> float:
    if row is None:
        return 0.0
    try:
        return float(row.get(key, "") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def to_int(row: Mapping[str, Any] | None, key: str) -> int:
    if row is None:
        return 0
    try:
        return int(round(float(row.get(key, "") or 0.0)))
    except (TypeError, ValueError):
        return 0


def base_alias(record_view: str) -> str:
    match = re.search(r"mt5_(?:ta|rt)_(.*?)_historical_2024", record_view)
    if not match:
        raise ValueError(f"cannot parse base record view: {record_view}")
    return match.group(1)


def p1_alias_variant(record_view: str) -> tuple[str, str]:
    match = re.search(r"mt5_(?:ta|rt)_(.*?)_(lateadx|late21|vlowadx|atrcomp|latevlow)_historical_2024", record_view)
    if not match:
        raise ValueError(f"cannot parse P1 record view: {record_view}")
    return match.group(1), match.group(2)


def feature_key(row: Mapping[str, str]) -> tuple[str, str]:
    return str(row.get("candidate_alias", "")), str(row.get("followup_variant_id", ""))


def candidate_roles() -> dict[str, str]:
    return {spec.alias: spec.role for spec in p1.input_probe.candidate_specs()}


def p0_by_candidate_axis() -> dict[tuple[str, str], dict[str, str]]:
    rows = [row for row in read_csv(P0_SUMMARY_PATH) if row.get("route_role") == "routed_total"]
    return {(row["candidate_alias"], row["diagnostic_variant"]): row for row in rows}


def diagnostic_read(row: Mapping[str, Any]) -> str:
    net_delta = float(row["net_profit_delta"])
    pf_delta = float(row["pf_delta"])
    trade_delta = float(row["trade_count_delta"])
    dd_delta = float(row["dd_percent_delta"])
    p0_net_delta = float(row["p1_vs_p0_net_profit_delta"])
    p0_trade_delta = float(row["p1_vs_p0_trade_count_delta"])
    p0_dd_delta = float(row["p1_vs_p0_dd_percent_delta"])
    if net_delta > 0 and pf_delta > 0 and dd_delta < 0 and trade_delta >= -60:
        return "constructive_soft_axis_candidate_not_selection(건설적인 부드러운 축 후보이나 선택은 아님)"
    if net_delta > 0 and dd_delta < 0 and trade_delta < -60:
        return "improves_risk_but_trade_cost_still_high(위험은 줄지만 거래 비용이 아직 큼)"
    if p0_net_delta < -150 and p0_dd_delta > 8 and p0_trade_delta > 40:
        return "too_much_p0_repair_lost(0차 수리 효과를 너무 많이 잃음)"
    if net_delta <= 0 or pf_delta <= 0:
        return "weak_against_base(기준값 대비 약함)"
    return "mixed_needs_axis_review(혼합 결과라 축 검토 필요)"


def build_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    base_rows = read_csv(BASE_KPI_PATH)
    p1_rows = read_csv(P1_KPI_PATH)
    features = read_csv(P1_FEATURE_MANIFEST_PATH)
    roles = candidate_roles()
    base_lookup = {(base_alias(row["record_view"]), row.get("route_role", "")): row for row in base_rows}
    p0_lookup = p0_by_candidate_axis()
    feature_lookup = {feature_key(row): row for row in features}

    detail: list[dict[str, Any]] = []
    for row in p1_rows:
        alias, variant_short = p1_alias_variant(row["record_view"])
        variant = VARIANT_META[variant_short]
        base = base_lookup[(alias, row.get("route_role", ""))]
        p0_primary = p0_lookup.get((alias, variant["primary_p0_axis"]))
        p0_secondary = p0_lookup.get((alias, variant["secondary_p0_axis"])) if variant["secondary_p0_axis"] else None
        feature = feature_lookup.get((alias, variant["followup_variant_id"]), {})
        net_delta = to_float(row, "net_profit") - to_float(base, "net_profit")
        pf_delta = to_float(row, "profit_factor") - to_float(base, "profit_factor")
        trade_delta = to_int(row, "trade_count") - to_int(base, "trade_count")
        dd_delta = to_float(row, "max_drawdown_percent") - to_float(base, "max_drawdown_percent")
        recovery_delta = to_float(row, "recovery_factor") - to_float(base, "recovery_factor")
        p0_net_delta = to_float(row, "net_profit") - to_float(p0_primary, "p0_net_profit")
        p0_trade_delta = to_int(row, "trade_count") - to_int(p0_primary, "p0_trade_count")
        p0_dd_delta = to_float(row, "max_drawdown_percent") - to_float(p0_primary, "p0_dd_percent")
        output = {
            "record_view": row["record_view"],
            "candidate_alias": alias,
            "candidate_role": roles.get(alias, ""),
            "followup_variant_short": variant_short,
            "followup_variant_id": variant["followup_variant_id"],
            "followup_label": variant["label"],
            "source_p0_axis": variant["source_p0_axis"],
            "primary_p0_axis": variant["primary_p0_axis"],
            "secondary_p0_axis": variant["secondary_p0_axis"],
            "tier_scope": row.get("tier_scope", ""),
            "route_role": row.get("route_role", ""),
            "base_net_profit": to_float(base, "net_profit"),
            "p1_net_profit": to_float(row, "net_profit"),
            "net_profit_delta": net_delta,
            "base_pf": to_float(base, "profit_factor"),
            "p1_pf": to_float(row, "profit_factor"),
            "pf_delta": pf_delta,
            "base_trade_count": to_int(base, "trade_count"),
            "p1_trade_count": to_int(row, "trade_count"),
            "trade_count_delta": trade_delta,
            "base_dd_percent": to_float(base, "max_drawdown_percent"),
            "p1_dd_percent": to_float(row, "max_drawdown_percent"),
            "dd_percent_delta": dd_delta,
            "base_recovery": to_float(base, "recovery_factor"),
            "p1_recovery": to_float(row, "recovery_factor"),
            "recovery_delta": recovery_delta,
            "p0_primary_net_profit": to_float(p0_primary, "p0_net_profit"),
            "p0_primary_trade_count": to_int(p0_primary, "p0_trade_count"),
            "p0_primary_dd_percent": to_float(p0_primary, "p0_dd_percent"),
            "p1_vs_p0_net_profit_delta": p0_net_delta,
            "p1_vs_p0_trade_count_delta": p0_trade_delta,
            "p1_vs_p0_dd_percent_delta": p0_dd_delta,
            "p0_secondary_net_profit": to_float(p0_secondary, "p0_net_profit") if p0_secondary else "",
            "p0_secondary_dd_percent": to_float(p0_secondary, "p0_dd_percent") if p0_secondary else "",
            "blocked_signal_rows": to_int(feature, "blocked_signal_rows"),
            "kept_signal_rows": to_int(feature, "kept_signal_rows"),
            "signal_retention": to_float(feature, "signal_retention"),
        }
        output["diagnostic_read"] = diagnostic_read(output)
        detail.append(output)

    routed = [row for row in detail if row["route_role"] == "routed_total"]
    summary = sorted(routed, key=lambda row: (row["followup_variant_short"], -float(row["p1_net_profit"])))
    axis_rows: list[dict[str, Any]] = []
    for variant_short in VARIANT_META:
        items = [row for row in routed if row["followup_variant_short"] == variant_short]
        if not items:
            continue
        axis_rows.append(
            {
                "followup_variant_short": variant_short,
                "followup_variant_id": VARIANT_META[variant_short]["followup_variant_id"],
                "followup_label": VARIANT_META[variant_short]["label"],
                "source_p0_axis": VARIANT_META[variant_short]["source_p0_axis"],
                "candidate_count": len(items),
                "avg_net_profit_delta": mean(float(row["net_profit_delta"]) for row in items),
                "avg_pf_delta": mean(float(row["pf_delta"]) for row in items),
                "avg_trade_count_delta": mean(float(row["trade_count_delta"]) for row in items),
                "avg_dd_percent_delta": mean(float(row["dd_percent_delta"]) for row in items),
                "avg_recovery_delta": mean(float(row["recovery_delta"]) for row in items),
                "avg_p1_vs_p0_net_profit_delta": mean(float(row["p1_vs_p0_net_profit_delta"]) for row in items),
                "avg_p1_vs_p0_trade_count_delta": mean(float(row["p1_vs_p0_trade_count_delta"]) for row in items),
                "avg_p1_vs_p0_dd_percent_delta": mean(float(row["p1_vs_p0_dd_percent_delta"]) for row in items),
                "avg_signal_retention": mean(float(row["signal_retention"]) for row in items),
                "best_net_candidate": max(items, key=lambda row: float(row["p1_net_profit"]))["candidate_alias"],
                "best_recovery_candidate": max(items, key=lambda row: float(row["p1_recovery"]))["candidate_alias"],
                "review_read": axis_read(items),
            }
        )
    return detail, summary, axis_rows


def axis_read(items: Sequence[Mapping[str, Any]]) -> str:
    avg_net_delta = mean(float(row["net_profit_delta"]) for row in items)
    avg_trade_delta = mean(float(row["trade_count_delta"]) for row in items)
    avg_dd_delta = mean(float(row["dd_percent_delta"]) for row in items)
    avg_p0_net_delta = mean(float(row["p1_vs_p0_net_profit_delta"]) for row in items)
    if avg_net_delta > 0 and avg_dd_delta < 0 and avg_trade_delta > -60:
        return "best_p1_soft_axis_family_to_consider(검토할 만한 1차 부드러운 축 계열)"
    if avg_net_delta > 0 and avg_dd_delta < 0:
        return "risk_repair_with_trade_cost(거래 비용이 있는 위험 수리)"
    if avg_p0_net_delta < -150:
        return "p0_repair_not_recovered(0차 수리 효과를 회복하지 못함)"
    return "weak_or_mixed_axis(약하거나 혼합된 축)"


def top_rows(summary: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return sorted(
        summary,
        key=lambda row: (
            float(row["p1_net_profit"]),
            float(row["p1_pf"]),
            -float(row["p1_dd_percent"]),
            float(row["p1_recovery"]),
        ),
        reverse=True,
    )[:10]


def report_markdown(summary: Sequence[Mapping[str, Any]], axis_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage267 Run267C P1 Soft-Axis Follow-up Review(267단계 267C 실행 1차 부드러운 축 후속 검토)",
        "",
        "- action(행동): P1 soft-axis MT5 batch(1차 부드러운 축 메타트레이더5 묶음 실행)를 run267B base(267B 기준값)와 P0 hard block(0차 강제 차단) 결과에 같이 맞춰 비교했다.",
        "- effect(효과): 좋아 보이는 숫자만 고르지 않고, 거래 수 비용, DD drawdown(손실폭), P0 repair retention(0차 수리 효과 유지), signal retention(신호 유지율)을 같이 보게 했다.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Axis Read(축 판독)",
        "",
        "| axis(축) | avg net delta(평균 순수익 차이) | avg PF delta(평균 수익 팩터 차이) | avg trade delta(평균 거래 수 차이) | avg DD% delta(평균 손실폭% 차이) | avg signal retention(평균 신호 유지율) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in axis_rows:
        lines.append(
            f"| {row['followup_label']} | {csv_value(row['avg_net_profit_delta'])} | {csv_value(row['avg_pf_delta'])} | {csv_value(row['avg_trade_count_delta'])} | {csv_value(row['avg_dd_percent_delta'])} | {csv_value(row['avg_signal_retention'])} | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Top Routed Reads(상위 라우팅 판독)",
            "",
            "| candidate(후보) | axis(축) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | net delta(순수익 차이) | DD delta(손실폭 차이) | P1 vs P0 net(1차 대 0차 순수익) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in top_rows(summary):
        lines.append(
            f"| `{row['candidate_alias']}` | {row['followup_label']} | {csv_value(row['p1_net_profit'])} | {csv_value(row['p1_pf'])} | {csv_value(row['p1_trade_count'])} | {csv_value(row['p1_dd_percent'])} | {csv_value(row['net_profit_delta'])} | {csv_value(row['dd_percent_delta'])} | {csv_value(row['p1_vs_p0_net_profit_delta'])} | {row['diagnostic_read']} |"
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- result_subject(결과 대상): `run267C_p1_soft_axis_followup_review`.",
            "- evidence_available(사용 가능 근거): P1 KPI(KPI, 핵심 성과 지표), P1 backtest forensics(백테스트 포렌식), feature manifest(피처 목록), P0 comparison(0차 비교), run267B base(267B 기준값).",
            "- evidence_missing(빠진 근거): equity curve(평가금 곡선) 확대 검토, 월별/세션별/요일별 breakdown(분해), adapter prototype(어댑터 원형), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `exploratory(탐색)`.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`. Effect(효과): P1에서 덜 깨진 축만 adapter prototype(어댑터 원형)이나 P2 replacement(2차 대체)로 넘기고, 약한 축은 실패 기억으로 닫는다.",
        ]
    )
    return "\n".join(lines)


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"missing replacement text: {old}")
    return text.replace(old, new, 1)


def append_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def update_docs() -> None:
    status_candidates = [
        "- status(상태): `run267C_p1_soft_axis_followup_mt5_completed`",
        "- status(상태): `run267C_p1_soft_axis_followup_mt5_partial_completed`",
        "- status(상태): `run267C_p1_soft_axis_followup_mt5_partial_mixed`",
    ]
    current = io_path(p1.CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    for old in status_candidates:
        if old in current:
            current = replace_once(current, old, f"- status(상태): `{STATUS}`")
            break
    current = append_after(
        current,
        "- Stage267(267단계) run267C P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_mt5_execution_report.md`",
        "- Stage267(267단계) run267C P1 soft-axis follow-up review(P1 부드러운 축 후속 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_review.md`",
    )
    current = replace_once(
        current,
        "- next_action(다음 행동): `run267C_review_p1_soft_axis_followup_mt5_results`. Effect(효과): P1 결과를 P0 hard block(강제 차단)과 run267B base(기준 실행) 대비로 분해해 다음 adapter(어댑터) 후보를 고를지 판단한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): P1 축 중 덜 깨진 쪽만 adapter prototype(어댑터 원형)이나 P2 replacement(2차 대체)로 좁히고, 약한 축은 실패 기록으로 남긴다.",
    )
    write_md(p1.CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(p1.SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    for old in (
        "- stage_status(단계 상태): `run267C_p1_soft_axis_followup_mt5_completed`",
        "- stage_status(단계 상태): `run267C_p1_soft_axis_followup_mt5_partial_completed`",
        "- stage_status(단계 상태): `run267C_p1_soft_axis_followup_mt5_partial_mixed`",
    ):
        if old in selection:
            selection = replace_once(selection, old, f"- stage_status(단계 상태): `{STATUS}`")
            break
    selection = append_after(
        selection,
        "- run267C_p1_soft_axis_followup_mt5_execution(267C P1 부드러운 축 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_mt5_execution_report.md`",
        "- run267C_p1_soft_axis_followup_review(267C P1 부드러운 축 후속 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_review.md`",
    )
    selection = replace_once(selection, "- next_action(다음 행동): `run267C_review_p1_soft_axis_followup_mt5_results`", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    write_md(p1.SELECTION_STATUS_PATH, selection)

    review = io_path(p1.REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    for old in (
        "- status(상태): `run267C_p1_soft_axis_followup_mt5_completed`",
        "- status(상태): `run267C_p1_soft_axis_followup_mt5_partial_completed`",
        "- status(상태): `run267C_p1_soft_axis_followup_mt5_partial_mixed`",
    ):
        if old in review:
            review = replace_once(review, old, f"- status(상태): `{STATUS}`")
            break
    review = append_after(
        review,
        "- run267C_p1_soft_axis_followup_mt5_execution(267C P1 부드러운 축 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_mt5_execution_report.md`",
        "- run267C_p1_soft_axis_followup_review(267C P1 부드러운 축 후속 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_review.md`",
    )
    review_effect_old = (
        "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), "
        "ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, "
        "`run267C_review_p1_soft_axis_followup_mt5_results`로 이어간다."
    )
    review_effect_old_alt = review_effect_old.replace("이어간다", "넘어간다")
    review_effect_new = (
        "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), "
        "ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, "
        f"`{NEXT_ACTION}`로 이어간다."
    )
    if review_effect_old in review:
        review = replace_once(review, review_effect_old, review_effect_new)
    elif review_effect_old_alt in review:
        review = replace_once(review, review_effect_old_alt, review_effect_new)
    write_md(p1.REVIEW_INDEX_PATH, review)

    workspace = io_path(p1.WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    for old in (
        "Stage267(267단계) run267C(267C 실행) P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행) `completed`.",
        "Stage267(267단계) run267C(267C 실행) P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행) `partial_completed`.",
        "Stage267(267단계) run267C(267C 실행) P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행) `partial_mixed`.",
    ):
        if old in workspace:
            workspace = replace_once(
                workspace,
                old,
                "Stage267(267단계) run267C(267C 실행) P1 soft-axis follow-up review(P1 부드러운 축 후속 검토) completed(완료).",
            )
            break
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267C_review_p1_soft_axis_followup_mt5_results`이다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다.",
        1,
    )
    for old in (
        "active_run267C_p1_soft_axis_followup_mt5_completed(267C P1 부드러운 축 후속 MT5 실행 뒤 리뷰 활성).",
        "active_run267C_p1_soft_axis_followup_mt5_partial_completed(267C P1 부드러운 축 후속 MT5 실행 뒤 리뷰 활성).",
        "active_run267C_p1_soft_axis_followup_mt5_partial_mixed(267C P1 부드러운 축 후속 MT5 실행 뒤 리뷰 활성).",
    ):
        if old in workspace:
            workspace = replace_once(
                workspace,
                old,
                "active_run267C_p1_soft_axis_followup_review_completed(267C P1 부드러운 축 후속 검토 뒤 어댑터/P2 선택 활성).",
            )
            break
    workspace = workspace.replace(
        "active_run267C_p1_soft_axis_followup_mt5_completed(267C P1 부드러운 축 후속 MT5 실행 후 리뷰 활성)",
        "active_run267C_p1_soft_axis_followup_review_completed(267C P1 부드러운 축 후속 검토 뒤 어댑터/P2 선택 활성)",
        1,
    )
    write_md(p1.WORKSPACE_STATE_PATH, workspace)


def update_ledgers(created_at: str, detail_count: int, summary_count: int, axis_count: int) -> None:
    stage_row = {
        "row_id": "stage267_run267C_p1_soft_axis_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "p1_soft_axis_followup_review",
        "tier_scope": "Tier A and Tier A+B historical 2024 soft-axis review",
        "scoreboard": "runtime_full_batch_review",
        "status": STATUS,
        "judgment": "exploratory_diagnostic_evidence_only_no_candidate_selection",
        "evidence_boundary": "p1_soft_axis_review_not_adapter_candidate_not_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"detail_rows={detail_count}; summary_rows={summary_count}; axis_rows={axis_count}; next_action={NEXT_ACTION}.",
    }
    stage_rows = p1.read_csv_rows(p1.STAGE_LEDGER_PATH)
    stage_rows = [row for row in stage_rows if row.get("row_id") != stage_row["row_id"]]
    stage_rows.append(stage_row)
    p1.write_csv(
        p1.STAGE_LEDGER_PATH,
        stage_rows,
        (
            "row_id",
            "stage_id",
            "run_id",
            "view",
            "tier_scope",
            "scoreboard",
            "status",
            "judgment",
            "evidence_boundary",
            "report_path",
            "notes",
        ),
    )
    p1.upsert_simple_csv(
        p1.RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_p1_soft_axis_followup_review",
            "status": STATUS,
            "judgment": "exploratory_diagnostic_evidence_only_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"P1 soft-axis review completed; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    p1.upsert_simple_csv(
        p1.PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__p1_soft_axis_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "p1_soft_axis_followup_review",
            "parent_run_id": RUN_ID,
            "record_view": "p1_soft_axis_followup_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 soft-axis review",
            "kpi_scope": "mt5_runtime_soft_axis_batch_review",
            "scoreboard_lane": "runtime_full_batch_review",
            "status": STATUS,
            "judgment": "exploratory_diagnostic_evidence_only_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"detail_rows={detail_count};summary_rows={summary_count};axis_rows={axis_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;adapter_candidate=not_yet",
            "external_verification_status": "completed",
            "notes": f"Next action: {NEXT_ACTION}.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )

    entries = (
        ("stage267_run267C_p1_soft_axis_followup_review_script", "producer_script", PRODUCER_PATH, "Builds P1 soft-axis follow-up review."),
        ("stage267_run267C_p1_soft_axis_delta_review", "delta_review", DETAIL_PATH, "Per-record P1 versus base and P0 delta review."),
        ("stage267_run267C_p1_soft_axis_candidate_variant_summary", "candidate_variant_summary", SUMMARY_PATH, "Routed P1 candidate and variant summary."),
        ("stage267_run267C_p1_soft_axis_axis_summary", "axis_summary", AXIS_PATH, "P1 soft-axis aggregate summary."),
        ("stage267_run267C_p1_soft_axis_review_result", "review_result", RESULT_PATH, "JSON result for P1 review."),
        ("stage267_run267C_p1_soft_axis_review_report", "review_report", REPORT_PATH, "User-facing P1 soft-axis review report."),
    )
    rows = p1.read_csv_rows(p1.ARTIFACT_REGISTRY_PATH)
    new_rows = []
    for artifact_id, artifact_type, path, notes in entries:
        new_rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    replacement = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(new_rows)
    p1.write_csv(
        p1.ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def main() -> int:
    if not path_exists(P1_KPI_PATH):
        raise FileNotFoundError(P1_KPI_PATH)
    created_at = utc_now()
    detail, summary, axis_rows = build_rows()
    write_csv(
        DETAIL_PATH,
        detail,
        (
            "record_view",
            "candidate_alias",
            "candidate_role",
            "followup_variant_short",
            "followup_variant_id",
            "followup_label",
            "source_p0_axis",
            "primary_p0_axis",
            "secondary_p0_axis",
            "tier_scope",
            "route_role",
            "base_net_profit",
            "p1_net_profit",
            "net_profit_delta",
            "base_pf",
            "p1_pf",
            "pf_delta",
            "base_trade_count",
            "p1_trade_count",
            "trade_count_delta",
            "base_dd_percent",
            "p1_dd_percent",
            "dd_percent_delta",
            "base_recovery",
            "p1_recovery",
            "recovery_delta",
            "p0_primary_net_profit",
            "p0_primary_trade_count",
            "p0_primary_dd_percent",
            "p1_vs_p0_net_profit_delta",
            "p1_vs_p0_trade_count_delta",
            "p1_vs_p0_dd_percent_delta",
            "p0_secondary_net_profit",
            "p0_secondary_dd_percent",
            "blocked_signal_rows",
            "kept_signal_rows",
            "signal_retention",
            "diagnostic_read",
        ),
    )
    write_csv(
        SUMMARY_PATH,
        summary,
        (
            "record_view",
            "candidate_alias",
            "candidate_role",
            "followup_variant_short",
            "followup_variant_id",
            "followup_label",
            "source_p0_axis",
            "primary_p0_axis",
            "secondary_p0_axis",
            "tier_scope",
            "route_role",
            "base_net_profit",
            "p1_net_profit",
            "net_profit_delta",
            "base_pf",
            "p1_pf",
            "pf_delta",
            "base_trade_count",
            "p1_trade_count",
            "trade_count_delta",
            "base_dd_percent",
            "p1_dd_percent",
            "dd_percent_delta",
            "base_recovery",
            "p1_recovery",
            "recovery_delta",
            "p0_primary_net_profit",
            "p0_primary_trade_count",
            "p0_primary_dd_percent",
            "p1_vs_p0_net_profit_delta",
            "p1_vs_p0_trade_count_delta",
            "p1_vs_p0_dd_percent_delta",
            "p0_secondary_net_profit",
            "p0_secondary_dd_percent",
            "blocked_signal_rows",
            "kept_signal_rows",
            "signal_retention",
            "diagnostic_read",
        ),
    )
    write_csv(
        AXIS_PATH,
        axis_rows,
        (
            "followup_variant_short",
            "followup_variant_id",
            "followup_label",
            "source_p0_axis",
            "candidate_count",
            "avg_net_profit_delta",
            "avg_pf_delta",
            "avg_trade_count_delta",
            "avg_dd_percent_delta",
            "avg_recovery_delta",
            "avg_p1_vs_p0_net_profit_delta",
            "avg_p1_vs_p0_trade_count_delta",
            "avg_p1_vs_p0_dd_percent_delta",
            "avg_signal_retention",
            "best_net_candidate",
            "best_recovery_candidate",
            "review_read",
        ),
    )
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "detail_rows": len(detail),
        "summary_rows": len(summary),
        "axis_rows": len(axis_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "detail": rel(DETAIL_PATH),
            "summary": rel(SUMMARY_PATH),
            "axis": rel(AXIS_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_json(RESULT_PATH, payload)
    write_md(REPORT_PATH, report_markdown(summary, axis_rows))
    update_docs()
    update_ledgers(created_at, len(detail), len(summary), len(axis_rows))
    print(
        json.dumps(
            {
                "status": STATUS,
                "detail_rows": len(detail),
                "summary_rows": len(summary),
                "axis_rows": len(axis_rows),
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
