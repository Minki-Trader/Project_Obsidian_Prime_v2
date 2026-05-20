from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage267 import run267C_p1_soft_axis_followup_materialization as p1
from stage_pipelines.stage267 import run267C_p1_soft_axis_followup_review as p1_review


STAGE_ID = p1.STAGE_ID
RUN_ID = p1.RUN_ID
CLAIM_BOUNDARY = p1.CLAIM_BOUNDARY
P1_ROOT = p1.P1_ROOT
REVIEWS_ROOT = p1.REVIEWS_ROOT
AXIS_SUMMARY_PATH = p1_review.AXIS_PATH
CANDIDATE_VARIANT_SUMMARY_PATH = p1_review.SUMMARY_PATH
SELECTION_MATRIX_PATH = P1_ROOT / "p1_axis_selection_matrix.csv"
CANDIDATE_SHORTLIST_PATH = P1_ROOT / "p1_adapter_p2_candidate_shortlist.csv"
FAILURE_MEMORY_PATH = P1_ROOT / "p1_axis_failure_memory.csv"
RESULT_PATH = P1_ROOT / "p1_axis_selection_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267C_p1_axis_selection_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267C_p1_axis_selection.py")

STATUS = "run267C_p1_axis_selection_completed"
NEXT_ACTION = "run267D_materialize_late21_adapter_prototype_and_p2_replacement_design"
ADAPTER_DECISION = "carry_forward_adapter_prototype_axis"
P2_DECISION = "carry_forward_p2_replacement_axis"
WATCH_DECISION = "defer_composition_watch"
FAIL_DECISION = "close_as_low_impact_failure_memory"


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


def to_float(row: Mapping[str, Any], key: str) -> float:
    try:
        return float(row.get(key, "") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def classify_axis(row: Mapping[str, str]) -> tuple[str, str, str]:
    axis = row["followup_variant_short"]
    net_delta = to_float(row, "avg_net_profit_delta")
    pf_delta = to_float(row, "avg_pf_delta")
    trade_delta = to_float(row, "avg_trade_count_delta")
    dd_delta = to_float(row, "avg_dd_percent_delta")
    p0_net_delta = to_float(row, "avg_p1_vs_p0_net_profit_delta")
    signal_retention = to_float(row, "avg_signal_retention")

    adapter_ready = (
        net_delta >= 80.0
        and pf_delta >= 0.05
        and dd_delta <= -8.0
        and trade_delta >= -50.0
        and p0_net_delta >= -75.0
        and signal_retention >= 0.85
    )
    p2_ready = net_delta >= 100.0 and pf_delta >= 0.05 and trade_delta >= -45.0 and signal_retention >= 0.80
    watch_ready = net_delta >= 50.0 and dd_delta <= -5.0 and trade_delta >= -15.0

    if adapter_ready:
        return (
            ADAPTER_DECISION,
            "retains_p0_repair_with_usable_trade_cost(P0 수리 효과를 유지하면서 거래 비용이 감당 가능)",
            "adapter prototype(어댑터 원형) 설계에서 우선 축으로 쓴다.",
        )
    if p2_ready:
        reason = "strong_net_or_replacement_signal_but_p0_repair_loss_or_trade_cost_remains(순수익 또는 대체 신호는 강하지만 P0 수리 손실이나 거래 비용이 남음)"
        if axis == "atrcomp":
            reason = "strongest_net_replacement_but_signal_retention_cost_is_high(가장 강한 순수익 대체 축이지만 신호 유지 비용이 큼)"
        if axis == "vlowadx":
            reason = "good_trade_retention_replacement_but_dd_repair_is_shallow(거래 유지가 좋은 대체 축이지만 손실폭 수리는 얕음)"
        return (
            P2_DECISION,
            reason,
            "P2 replacement(2차 대체) 설계에서 구조를 더 좁힌다.",
        )
    if watch_ready:
        return (
            WATCH_DECISION,
            "low_trade_cost_but_p0_repair_loss_too_large(거래 비용은 낮지만 P0 수리 효과 손실이 큼)",
            "다른 축과 합성할 때만 다시 본다.",
        )
    return (
        FAIL_DECISION,
        "low_impact_vs_base_and_p0_repair_not_retained(기준 대비 효과가 작고 P0 수리 효과도 유지하지 못함)",
        "반복 금지 실패 기억으로 닫는다.",
    )


def selection_score(row: Mapping[str, str]) -> float:
    net_delta = to_float(row, "avg_net_profit_delta")
    pf_delta = to_float(row, "avg_pf_delta")
    trade_delta = to_float(row, "avg_trade_count_delta")
    dd_delta = to_float(row, "avg_dd_percent_delta")
    p0_net_delta = to_float(row, "avg_p1_vs_p0_net_profit_delta")
    p0_dd_delta = to_float(row, "avg_p1_vs_p0_dd_percent_delta")
    signal_retention = to_float(row, "avg_signal_retention")
    return (
        net_delta * 0.35
        + pf_delta * 500.0
        + (-dd_delta) * 4.0
        + trade_delta * 0.8
        + max(p0_net_delta, -300.0) * 0.12
        + (-p0_dd_delta) * 3.0
        + signal_retention * 40.0
    )


def build_axis_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in read_csv(AXIS_SUMMARY_PATH):
        decision, reason, next_use = classify_axis(source)
        output = {
            **source,
            "axis_selection_score": selection_score(source),
            "axis_decision": decision,
            "decision_reason": reason,
            "next_use": next_use,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append(output)
    decision_rank = {
        ADAPTER_DECISION: 0,
        P2_DECISION: 1,
        WATCH_DECISION: 2,
        FAIL_DECISION: 3,
    }
    return sorted(rows, key=lambda row: (decision_rank[row["axis_decision"]], -float(row["axis_selection_score"])))


def pair_role(row: Mapping[str, str], axis_decision: str) -> str:
    role = row["candidate_role"]
    if axis_decision == ADAPTER_DECISION and role == "challenger_core":
        return "primary_adapter_probe_pair(주 어댑터 탐침 쌍)"
    if axis_decision == ADAPTER_DECISION and role in {"defensive_control", "validation_heavy"}:
        return "adapter_control_pair(어댑터 대조 쌍)"
    if axis_decision == ADAPTER_DECISION:
        return "adapter_stress_or_anchor_pair(어댑터 압박/앵커 쌍)"
    if axis_decision == P2_DECISION:
        return "p2_replacement_pair(2차 대체 쌍)"
    if axis_decision == WATCH_DECISION:
        return "watch_only_pair(관찰 전용 쌍)"
    return "not_carried_forward_pair(이월하지 않는 쌍)"


def build_shortlist(axis_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axis_decisions = {row["followup_variant_short"]: row["axis_decision"] for row in axis_rows}
    rows = []
    for source in read_csv(CANDIDATE_VARIANT_SUMMARY_PATH):
        axis_decision = axis_decisions[source["followup_variant_short"]]
        if axis_decision == FAIL_DECISION:
            continue
        rows.append(
            {
                "candidate_alias": source["candidate_alias"],
                "candidate_role": source["candidate_role"],
                "followup_variant_short": source["followup_variant_short"],
                "followup_variant_id": source["followup_variant_id"],
                "axis_decision": axis_decision,
                "pair_role": pair_role(source, axis_decision),
                "p1_net_profit": source["p1_net_profit"],
                "p1_pf": source["p1_pf"],
                "p1_trade_count": source["p1_trade_count"],
                "p1_dd_percent": source["p1_dd_percent"],
                "net_profit_delta": source["net_profit_delta"],
                "pf_delta": source["pf_delta"],
                "trade_count_delta": source["trade_count_delta"],
                "dd_percent_delta": source["dd_percent_delta"],
                "p1_vs_p0_net_profit_delta": source["p1_vs_p0_net_profit_delta"],
                "p1_vs_p0_trade_count_delta": source["p1_vs_p0_trade_count_delta"],
                "p1_vs_p0_dd_percent_delta": source["p1_vs_p0_dd_percent_delta"],
                "diagnostic_read": source["diagnostic_read"],
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            0 if row["axis_decision"] == ADAPTER_DECISION else 1 if row["axis_decision"] == P2_DECISION else 2,
            -float(row["p1_net_profit"]),
        ),
    )


def build_failure_memory(axis_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in axis_rows:
        if row["axis_decision"] not in {WATCH_DECISION, FAIL_DECISION}:
            continue
        rows.append(
            {
                "result_id": f"stage267_p1_axis_{row['followup_variant_short']}",
                "idea_id": f"STAGE267-P1-{row['followup_variant_short'].upper()}",
                "hypothesis": "P1 soft-axis(1차 부드러운 축)가 P0 hard block(0차 강제 차단)의 수리 효과를 낮은 거래 비용으로 유지할 수 있다.",
                "why_failed": row["decision_reason"],
                "salvage_value": row["next_use"],
                "reopen_condition": "다른 axis(축)와 결합하거나 새 feature family(피처 계열)에서 DD(drawdown, 손실폭) 수리와 signal retention(신호 유지율)이 동시에 개선될 때.",
                "do_not_repeat": "동일 cutoff(절단값)를 단독으로 반복하지 않는다.",
            }
        )
    return rows


def axis_counts(axis_rows: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in axis_rows:
        counts[row["axis_decision"]] = counts.get(row["axis_decision"], 0) + 1
    return counts


def report_markdown(axis_rows: Sequence[Mapping[str, Any]], shortlist: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> str:
    adapter_rows = [row for row in axis_rows if row["axis_decision"] == ADAPTER_DECISION]
    p2_rows = [row for row in axis_rows if row["axis_decision"] == P2_DECISION]
    watch_rows = [row for row in axis_rows if row["axis_decision"] == WATCH_DECISION]
    fail_rows = [row for row in axis_rows if row["axis_decision"] == FAIL_DECISION]
    memory_rows = [row for row in axis_rows if row["axis_decision"] in {WATCH_DECISION, FAIL_DECISION}]
    lines = [
        "# Stage267 Run267C P1 Axis Selection(267단계 267C 실행 1차 축 선택)",
        "",
        "- action(행동): P1 soft-axis(1차 부드러운 축) 결과를 Adapter prototype(어댑터 원형), P2 replacement(2차 대체), watch(관찰), failure memory(실패 기억)로 분리했다.",
        "- effect(효과): 가장 좋아 보이는 숫자만 고르지 않고, P0 repair retention(0차 수리 유지), trade cost(거래 비용), DD(drawdown, 손실폭), signal retention(신호 유지율)을 같이 본다.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Experiment Design Receipt(실험 설계 기록)",
        "",
        "- hypothesis(가설): P1 soft-axis(1차 부드러운 축) 중 일부는 P0 hard block(0차 강제 차단)의 수리 단서를 더 낮은 과차단으로 유지할 수 있다.",
        "- decision_use(결정 사용처): 다음 Adapter prototype(어댑터 원형) 또는 P2 replacement(2차 대체) 물질화 축을 고른다.",
        f"- comparison_baseline(비교 기준): `{rel(p1.RUN267B_HIST_ROOT / 'mt5_kpi_summary.csv')}`와 `{rel(p1_review.P0_SUMMARY_PATH)}`.",
        "- control_variables(고정 변수): Stage267(267단계) 5개 후보군, 2024 historical stress(2024 과거 압박) 기간, MT5 EA(메타트레이더5 전문가 자문), threshold(임계값), trade management(거래 관리)를 유지한다.",
        "- changed_variables(변경 변수): 다음 작업에서 이월할 axis family(축 계열)와 adapter/replacement(어댑터/대체) 역할만 바꾼다.",
        "- sample_scope(표본 범위): Tier A(티어 A)와 Tier A+B(티어 A+B) routed historical 2024(라우팅 과거 2024) MT5 Strategy Tester(전략 테스터) 결과.",
        "- success_criteria(성공 기준): 수익/PF(수익 팩터)가 기준보다 좋아지고, DD(손실폭)가 줄며, 거래 수와 신호 유지율이 과도하게 무너지지 않는 축을 다음 구조 검증으로 넘긴다.",
        "- failure_criteria(실패 기준): 기준 대비 효과가 작거나 P0 repair(0차 수리)를 거의 잃거나, 같은 cutoff(절단값) 반복만 남는 축은 실패 기억으로 닫는다.",
        "- invalid_conditions(무효 조건): MT5 report(보고서), KPI(KPI, 핵심 성과 지표), feature manifest(피처 목록), P0/base comparison(0차/기준 비교)이 누락되면 이 선택은 무효다.",
        "- stop_conditions(중단 조건): next run(다음 실행)이 다시 한 축 미세조정만 반복하면 P2(2차)로 넘기지 않고 실패 기억으로 닫는다.",
        f"- evidence_plan(근거 계획): `{rel(SELECTION_MATRIX_PATH)}`, `{rel(CANDIDATE_SHORTLIST_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`를 장부에 연결한다.",
        "",
        "## Axis Decision(축 결정)",
        "",
        "| axis(축) | decision(결정) | avg net delta(평균 순수익 차이) | avg PF delta(평균 수익 팩터 차이) | avg trade delta(평균 거래 수 차이) | avg DD% delta(평균 손실폭% 차이) | P1 vs P0 net(1차 대 0차 순수익) | signal retention(신호 유지율) | reason(이유) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in axis_rows:
        lines.append(
            f"| `{row['followup_variant_short']}` | `{row['axis_decision']}` | {csv_value(row['avg_net_profit_delta'])} | {csv_value(row['avg_pf_delta'])} | {csv_value(row['avg_trade_count_delta'])} | {csv_value(row['avg_dd_percent_delta'])} | {csv_value(row['avg_p1_vs_p0_net_profit_delta'])} | {csv_value(row['avg_signal_retention'])} | {row['decision_reason']} |"
        )
    lines.extend(
        [
            "",
            "## Carry Forward(다음 이월)",
            "",
            f"- Adapter prototype(어댑터 원형): `{';'.join(row['followup_variant_short'] for row in adapter_rows) or 'none'}`.",
            f"- P2 replacement(2차 대체): `{';'.join(row['followup_variant_short'] for row in p2_rows) or 'none'}`.",
            f"- watch(관찰): `{';'.join(row['followup_variant_short'] for row in watch_rows) or 'none'}`.",
            f"- failure/watch memory(실패/관찰 기억): `{';'.join(row['followup_variant_short'] for row in memory_rows) or 'none'}`.",
            "",
            "## Shortlist Pair Read(후보-축 짝 판독)",
            "",
            "| candidate(후보) | axis(축) | role(역할) | pair_role(짝 역할) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in shortlist[:15]:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['followup_variant_short']}` | `{row['candidate_role']}` | `{row['pair_role']}` | {row['p1_net_profit']} | {row['p1_pf']} | {row['p1_trade_count']} | {row['p1_dd_percent']} |"
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- selected_candidate(선택 후보): `none`.",
            "- selected_research_baseline(선택 연구 기준선): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- result_subject(결과 대상): `run267C_p1_axis_selection`.",
            "- evidence_available(사용 가능 근거): P1 KPI(KPI, 핵심 성과 지표), P0 comparison(0차 비교), run267B base(267B 기준값), feature manifest(피처 목록), MT5 backtest forensics(백테스트 포렌식).",
            "- evidence_missing(빠진 근거): Adapter prototype MT5 run(어댑터 원형 MT5 실행), P2 replacement MT5 run(2차 대체 MT5 실행), zoomed equity curve(확대 평가금 곡선), full time-slice breakdown(전체 시간 구간 분해), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `exploratory_axis_selection(탐색 축 선택)`.",
            f"- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`. Effect(효과): late21(후반 21시)은 Adapter prototype(어댑터 원형)으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 P2 replacement(2차 대체)로 물질화해 다시 MT5(메타트레이더5) 검증한다.",
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
    report_line_current = "- Stage267(267단계) run267C P1 axis selection(P1 축 선택): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_axis_selection_report.md`"
    current = io_path(p1.CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_once(current, "- status(상태): `run267C_p1_soft_axis_followup_review_completed`", f"- status(상태): `{STATUS}`")
    current = append_after(
        current,
        "- Stage267(267단계) run267C P1 soft-axis follow-up review(P1 부드러운 축 후속 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_review.md`",
        report_line_current,
    )
    current = replace_once(
        current,
        "- action(행동): run267C(267C 실행) P1 soft-axis MT5 execution(P1 부드러운 축 MT5 실행)을 `50`개 attempt(시도)로 수행했다.",
        "- action(행동): run267C(267C 실행) P1 axis selection(P1 축 선택)에서 late21(후반 21시)을 Adapter prototype(어댑터 원형) 축으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)를 P2 replacement(2차 대체) 축으로 분리했다.",
    )
    current = replace_once(
        current,
        "- effect(효과): `50`개 KPI(핵심 성과 지표)를 확보했지만, 아직 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        "- effect(효과): 다음 작업은 후보 선택이 아니라 axis family(축 계열)를 Adapter prototype(어댑터 원형)과 P2 replacement(2차 대체)로 물질화하는 것이다.",
    )
    current = replace_once(
        current,
        "- next_action(다음 행동): `run267C_select_p1_axes_for_adapter_prototype_or_p2_replacement`. Effect(효과): P1 축 중 덜 깨진 쪽만 adapter prototype(어댑터 원형)이나 P2 replacement(2차 대체)로 좁히고, 약한 축은 실패 기록으로 남긴다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): late21(후반 21시)은 어댑터 원형으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 2차 대체 설계로 물질화해 다시 MT5(메타트레이더5) 검증한다.",
    )
    write_md(p1.CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(p1.SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_once(selection, "- stage_status(단계 상태): `run267C_p1_soft_axis_followup_review_completed`", f"- stage_status(단계 상태): `{STATUS}`")
    selection = append_after(
        selection,
        "- run267C_p1_soft_axis_followup_review(267C P1 부드러운 축 후속 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_review.md`",
        "- run267C_p1_axis_selection(267C P1 축 선택): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_axis_selection_report.md`",
    )
    selection = replace_once(selection, "- next_action(다음 행동): `run267C_select_p1_axes_for_adapter_prototype_or_p2_replacement`", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_once(
        selection,
        "Run267C(267C 실행)는 P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 P1 결과를 P0 및 run267B 기준과 비교하는 리뷰다.",
        "Run267C(267C 실행)는 P1 axis selection(P1 축 선택)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 late21(후반 21시) Adapter prototype(어댑터 원형)과 atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX) P2 replacement(2차 대체)를 물질화하는 작업이다.",
    )
    write_md(p1.SELECTION_STATUS_PATH, selection)

    review = io_path(p1.REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_once(review, "- status(상태): `run267C_p1_soft_axis_followup_review_completed`", f"- status(상태): `{STATUS}`")
    review = append_after(
        review,
        "- run267C_p1_soft_axis_followup_review(267C P1 부드러운 축 후속 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_review.md`",
        "- run267C_p1_axis_selection(267C P1 축 선택): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_axis_selection_report.md`",
    )
    review = replace_once(
        review,
        "Run267C(267C 실행)는 P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행)을 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267C_select_p1_axes_for_adapter_prototype_or_p2_replacement`로 이어간다.",
        f"Run267C(267C 실행)는 P1 axis selection(P1 축 선택)을 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{NEXT_ACTION}`로 이어간다.",
    )
    write_md(p1.REVIEW_INDEX_PATH, review)

    workspace = io_path(p1.WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_once(workspace, "updated_on: '2026-05-20'", "updated_on: '2026-05-21'")
    workspace = replace_once(
        workspace,
        "Stage267(267단계) run267C(267C 실행) P1 soft-axis follow-up review(P1 부드러운 축 후속 검토) completed(완료). Effect(효과): `50`개 attempt(시도)를 실제 MT5 Strategy Tester(전략 테스터)로 확인했고, `50`개 KPI(핵심 성과 지표)를 확보했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        "Stage267(267단계) run267C(267C 실행) P1 axis selection(P1 축 선택) completed(완료). Effect(효과): late21(후반 21시)은 Adapter prototype(어댑터 원형) 축으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 P2 replacement(2차 대체) 축으로 나눴지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace = replace_once(
        workspace,
        "Next action(다음 행동)는 `run267C_select_p1_axes_for_adapter_prototype_or_p2_replacement`이다. Effect(효과): 2024-style extended period test(2024년식 확장 기간 시험)를 training-era historical stress(학습 기간 과거 압박)로 라벨링(labeling, 라벨링)한 채, vol_low(낮은 변동성), 2024-07(2024년 7월), Monday(월요일), late session(후반 세션) 약점이 feature ablation(피처 제거)과 similar replacement(유사 대체)에서 줄어드는지 보게 한다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): late21(후반 21시)은 Adapter prototype(어댑터 원형)으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 P2 replacement(2차 대체)로 물질화해 balance/equity curve(잔액/평가금 곡선)와 time-slice KPI(시간 구간 핵심 성과 지표)를 다시 본다.",
    )
    workspace = replace_once(
        workspace,
        "active_run267C_p1_soft_axis_followup_review_completed(267C P1 부드러운 축 후속 검토 뒤 어댑터/P2 선택 활성)",
        "active_run267C_p1_axis_selection_completed(267C P1 축 선택 뒤 run267D 물질화 활성)",
    )
    workspace = workspace.replace(
        "status: run267B_historical_2024_balance_time_slice_review_completed_visual_zoom_pending",
        f"status: {STATUS}",
        1,
    )
    workspace = workspace.replace(
        "current_run_id: run267B_stage267_extended_period_ablation_probe_v1",
        f"current_run_id: {RUN_ID}",
        1,
    )
    workspace = workspace.replace(
        "next_action: run267B_2024_visual_zoom_ablation_replacement_design",
        f"next_action: {NEXT_ACTION}",
        1,
    )
    write_md(p1.WORKSPACE_STATE_PATH, workspace)


def update_ledgers(created_at: str, axis_rows: Sequence[Mapping[str, Any]], shortlist: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    counts = axis_counts(axis_rows)
    stage_row = {
        "row_id": "stage267_run267C_p1_axis_selection",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "p1_axis_selection",
        "tier_scope": "Tier A and Tier A+B historical 2024 soft-axis selection",
        "scoreboard": "runtime_full_batch_review",
        "status": STATUS,
        "judgment": "exploratory_axis_selection_no_candidate_selection",
        "evidence_boundary": "p1_axis_selection_not_adapter_runtime_not_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"adapter_axes={counts.get(ADAPTER_DECISION, 0)}; p2_axes={counts.get(P2_DECISION, 0)}; next_action={NEXT_ACTION}.",
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
            "lane": "baseline_candidate_racing_p1_axis_selection",
            "status": STATUS,
            "judgment": "exploratory_axis_selection_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Axis selection completed; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    p1.upsert_simple_csv(
        p1.PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__p1_axis_selection",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "p1_axis_selection",
            "parent_run_id": RUN_ID,
            "record_view": "p1_axis_selection",
            "tier_scope": "Tier A and Tier A+B historical 2024 soft-axis selection",
            "kpi_scope": "mt5_runtime_soft_axis_selection_review",
            "scoreboard_lane": "runtime_full_batch_review",
            "status": STATUS,
            "judgment": "exploratory_axis_selection_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"adapter_axes={counts.get(ADAPTER_DECISION, 0)};p2_axes={counts.get(P2_DECISION, 0)};watch_axes={counts.get(WATCH_DECISION, 0)};failure_axes={counts.get(FAIL_DECISION, 0)}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;adapter_runtime=not_yet",
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
        ("stage267_run267C_p1_axis_selection_script", "producer_script", PRODUCER_PATH, "Builds P1 axis selection evidence."),
        ("stage267_run267C_p1_axis_selection_matrix", "axis_selection_matrix", SELECTION_MATRIX_PATH, "Axis-level P1 carry-forward decision matrix."),
        ("stage267_run267C_p1_adapter_p2_candidate_shortlist", "candidate_shortlist", CANDIDATE_SHORTLIST_PATH, "Candidate-axis shortlist for adapter/P2 design."),
        ("stage267_run267C_p1_axis_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "P1 axis failure/watch memory."),
        ("stage267_run267C_p1_axis_selection_result", "review_result", RESULT_PATH, "JSON result for P1 axis selection."),
        ("stage267_run267C_p1_axis_selection_report", "review_report", REPORT_PATH, "User-facing P1 axis selection report."),
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
    created_at = utc_now()
    axis_rows = build_axis_rows()
    shortlist = build_shortlist(axis_rows)
    failure_rows = build_failure_memory(axis_rows)
    write_csv(
        SELECTION_MATRIX_PATH,
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
            "axis_selection_score",
            "axis_decision",
            "decision_reason",
            "next_use",
            "claim_boundary",
        ),
    )
    write_csv(
        CANDIDATE_SHORTLIST_PATH,
        shortlist,
        (
            "candidate_alias",
            "candidate_role",
            "followup_variant_short",
            "followup_variant_id",
            "axis_decision",
            "pair_role",
            "p1_net_profit",
            "p1_pf",
            "p1_trade_count",
            "p1_dd_percent",
            "net_profit_delta",
            "pf_delta",
            "trade_count_delta",
            "dd_percent_delta",
            "p1_vs_p0_net_profit_delta",
            "p1_vs_p0_trade_count_delta",
            "p1_vs_p0_dd_percent_delta",
            "diagnostic_read",
        ),
    )
    write_csv(
        FAILURE_MEMORY_PATH,
        failure_rows,
        (
            "result_id",
            "idea_id",
            "hypothesis",
            "why_failed",
            "salvage_value",
            "reopen_condition",
            "do_not_repeat",
        ),
    )
    counts = axis_counts(axis_rows)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "axis_rows": len(axis_rows),
        "shortlist_rows": len(shortlist),
        "failure_memory_rows": len(failure_rows),
        "axis_decision_counts": counts,
        "adapter_axes": [row["followup_variant_short"] for row in axis_rows if row["axis_decision"] == ADAPTER_DECISION],
        "p2_replacement_axes": [row["followup_variant_short"] for row in axis_rows if row["axis_decision"] == P2_DECISION],
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "selection_matrix": rel(SELECTION_MATRIX_PATH),
            "candidate_shortlist": rel(CANDIDATE_SHORTLIST_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_json(RESULT_PATH, payload)
    write_md(REPORT_PATH, report_markdown(axis_rows, shortlist, failure_rows))
    update_docs()
    update_ledgers(created_at, axis_rows, shortlist, failure_rows)
    print(
        json.dumps(
            {
                "status": STATUS,
                "axis_rows": len(axis_rows),
                "adapter_axes": payload["adapter_axes"],
                "p2_replacement_axes": payload["p2_replacement_axes"],
                "failure_memory_rows": len(failure_rows),
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
