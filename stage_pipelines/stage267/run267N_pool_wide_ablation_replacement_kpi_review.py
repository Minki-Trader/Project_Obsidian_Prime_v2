from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage267 import run267N_pool_wide_ablation_replacement_executor as executor
from stage_pipelines.stage267 import run267N_pool_wide_ablation_replacement_materialization as materializer


STAGE_ID = materializer.STAGE_ID
RUN_ID = materializer.RUN_ID
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY
RUN_ROOT = materializer.MATERIALIZATION_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

BASE_KPI_PATH = materializer.STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "mt5_kpi_summary.csv"
P0_KPI_PATH = executor.KPI_SUMMARY_PATH
EXECUTION_RESULT_PATH = executor.EXECUTION_RESULT_PATH
DETAIL_PATH = RUN_ROOT / "kpi_delta_review.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_kpi_delta_summary.csv"
TEST_SUMMARY_PATH = RUN_ROOT / "test_kpi_delta_summary.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "kpi_review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267N_pool_wide_ablation_replacement_kpi_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267N_pool_wide_ablation_replacement_kpi_review.py")

STATUS = "run267N_pool_wide_ablation_replacement_kpi_review_completed"
NEXT_ACTION = "run267O_pool_wide_balance_timeslice_trade_quality_review"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


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
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def alias_from_record_view(record_view: str) -> tuple[str, str]:
    match = re.match(r"mt5_(ta|rt)_(.*?)_historical_2024", record_view)
    if not match:
        raise ValueError(f"cannot parse record_view: {record_view}")
    route_role = "tier_only_total" if match.group(1) == "ta" else "routed_total"
    return match.group(2), route_role


def review_label(row: Mapping[str, Any]) -> str:
    net_delta = as_float(row.get("net_profit_delta"))
    dd_delta = as_float(row.get("dd_percent_delta"))
    trade_delta = as_float(row.get("trade_count_delta"))
    boundary = str(row.get("materialization_boundary"))
    if net_delta > 250 and dd_delta < -10 and trade_delta > -80 and boundary.startswith("direct"):
        return "strong_direct_clue_needs_curve_review(강한 직접 단서, 곡선 검토 필요)"
    if net_delta > 250 and dd_delta < -10:
        return "strong_proxy_clue_not_internal_ablation(강한 대체 단서, 내부 제거 아님)"
    if net_delta > 0 and dd_delta < 0:
        return "constructive_but_not_enough(건설적이나 충분하지 않음)"
    if net_delta < 0 and dd_delta > 0:
        return "destructive_failure_memory(파괴적 실패 기억)"
    return "mixed_or_weak(혼합 또는 약함)"


def base_rows_by_alias_and_role() -> dict[tuple[str, str], Mapping[str, str]]:
    rows: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in read_csv(BASE_KPI_PATH):
        alias, role = alias_from_record_view(row["record_view"])
        rows[(alias, role)] = row
    return rows


def build_detail_rows() -> list[dict[str, Any]]:
    base_rows = base_rows_by_alias_and_role()
    detail: list[dict[str, Any]] = []
    for row in read_csv(P0_KPI_PATH):
        base = base_rows[(row["candidate_alias"], row["route_role"])]
        next_row: dict[str, Any] = {
            "record_view": row.get("record_view"),
            "candidate_id": row.get("candidate_id"),
            "candidate_alias": row.get("candidate_alias"),
            "candidate_role": row.get("candidate_role"),
            "test_id": row.get("test_id"),
            "test_type": row.get("test_type"),
            "materialization_boundary": row.get("materialization_boundary"),
            "route_role": row.get("route_role"),
            "tier_scope": row.get("tier_scope"),
            "status": row.get("status"),
            "base_net_profit": as_float(base.get("net_profit")),
            "p0_net_profit": as_float(row.get("net_profit")),
            "net_profit_delta": as_float(row.get("net_profit")) - as_float(base.get("net_profit")),
            "base_profit_factor": as_float(base.get("profit_factor")),
            "p0_profit_factor": as_float(row.get("profit_factor")),
            "profit_factor_delta": as_float(row.get("profit_factor")) - as_float(base.get("profit_factor")),
            "base_trade_count": as_float(base.get("trade_count")),
            "p0_trade_count": as_float(row.get("trade_count")),
            "trade_count_delta": as_float(row.get("trade_count")) - as_float(base.get("trade_count")),
            "base_dd_percent": as_float(base.get("max_drawdown_percent")),
            "p0_dd_percent": as_float(row.get("max_drawdown_percent")),
            "dd_percent_delta": as_float(row.get("max_drawdown_percent")) - as_float(base.get("max_drawdown_percent")),
            "base_recovery_factor": as_float(base.get("recovery_factor")),
            "p0_recovery_factor": as_float(row.get("recovery_factor")),
            "recovery_factor_delta": as_float(row.get("recovery_factor")) - as_float(base.get("recovery_factor")),
        }
        next_row["review_label"] = review_label(next_row)
        detail.append(next_row)
    return detail


def summarize_candidates(detail: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    routed = [row for row in detail if row.get("route_role") == "routed_total"]
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in routed:
        grouped[str(row.get("candidate_alias"))].append(row)
    rows: list[dict[str, Any]] = []
    for alias, items in sorted(grouped.items()):
        best_net = max(items, key=lambda row: as_float(row.get("p0_net_profit")))
        worst_net = min(items, key=lambda row: as_float(row.get("p0_net_profit")))
        destructive = [row for row in items if "destructive" in str(row.get("review_label"))]
        strong = [row for row in items if str(row.get("review_label")).startswith("strong")]
        rows.append(
            {
                "candidate_alias": alias,
                "candidate_id": best_net.get("candidate_id"),
                "candidate_role": best_net.get("candidate_role"),
                "test_count": len(items),
                "avg_net_profit_delta": mean(as_float(row.get("net_profit_delta")) for row in items),
                "avg_dd_percent_delta": mean(as_float(row.get("dd_percent_delta")) for row in items),
                "avg_trade_count_delta": mean(as_float(row.get("trade_count_delta")) for row in items),
                "strong_clue_count": len(strong),
                "destructive_failure_count": len(destructive),
                "best_test_id": best_net.get("test_id"),
                "best_net_profit": best_net.get("p0_net_profit"),
                "best_net_delta": best_net.get("net_profit_delta"),
                "best_dd_percent": best_net.get("p0_dd_percent"),
                "worst_test_id": worst_net.get("test_id"),
                "worst_net_profit": worst_net.get("p0_net_profit"),
                "candidate_read": candidate_read(items, strong, destructive),
            }
        )
    return rows


def candidate_read(items: Sequence[Mapping[str, Any]], strong: Sequence[Mapping[str, Any]], destructive: Sequence[Mapping[str, Any]]) -> str:
    aliases = {str(row.get("candidate_alias")) for row in items}
    alias = next(iter(aliases)) if aliases else ""
    if destructive:
        return "contains_destructive_gate_or_rank_failure(파괴적 gate/rank 실패 포함)"
    if alias == "s264_lc" and strong:
        return "strong_direct_gate_variant_clue_but_requires_curve_and_trade_quality_review(강한 직접 gate 단서, 곡선/거래품질 검토 필요)"
    if strong:
        return "strong_proxy_clue_requires_internal_feature_confirmation(강한 대체 단서, 내부 피처 확인 필요)"
    return "constructive_kpi_only_no_selection(건설적 KPI뿐, 선택 아님)"


def summarize_tests(detail: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    routed = [row for row in detail if row.get("route_role") == "routed_total"]
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in routed:
        grouped[str(row.get("test_id"))].append(row)
    rows: list[dict[str, Any]] = []
    for test_id, items in sorted(grouped.items()):
        rows.append(
            {
                "test_id": test_id,
                "test_type": items[0].get("test_type"),
                "materialization_boundary": items[0].get("materialization_boundary"),
                "candidate_count": len(items),
                "avg_net_profit_delta": mean(as_float(row.get("net_profit_delta")) for row in items),
                "avg_dd_percent_delta": mean(as_float(row.get("dd_percent_delta")) for row in items),
                "avg_trade_count_delta": mean(as_float(row.get("trade_count_delta")) for row in items),
                "best_candidate_alias": max(items, key=lambda row: as_float(row.get("p0_net_profit"))).get("candidate_alias"),
                "worst_candidate_alias": min(items, key=lambda row: as_float(row.get("p0_net_profit"))).get("candidate_alias"),
            }
        )
    return rows


def report_markdown(
    detail: Sequence[Mapping[str, Any]],
    candidate_rows: Sequence[Mapping[str, Any]],
    test_rows: Sequence[Mapping[str, Any]],
) -> str:
    routed = [row for row in detail if row.get("route_role") == "routed_total"]
    top = sorted(routed, key=lambda row: as_float(row.get("p0_net_profit")), reverse=True)[:10]
    failures = [row for row in sorted(routed, key=lambda row: as_float(row.get("p0_net_profit"))) if "destructive" in str(row.get("review_label"))]
    lines = [
        "# Stage267 Run267N Pool-Wide P0 KPI Review(267단계 267N 후보군 전체 P0 KPI 검토)",
        "",
        "- action(행동): run267N(267N 실행) MT5(MetaTrader 5, 메타트레이더5) 48개 KPI(핵심 성과 지표)를 run267B(267B 실행) 2024 baseline(기준) KPI와 비교했다.",
        "- effect(효과): 숫자만 큰 후보를 고르지 않고, net profit(순수익), PF(수익 팩터), trade count(거래 수), DD(drawdown, 손실폭), direct/proxy(직접/대체) 경계를 같이 본다.",
        f"- status(상태): `{STATUS}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "가장 큰 숫자는 `s264_lc`의 `abl_gate_variant_rule`에서 나왔다. 하지만 이것은 바로 선택이 아니라, gate variant(게이트 변형) 쪽에 강한 단서가 있다는 뜻이다.",
        "`s264_lc`와 `s262_lih`의 `abl_gate_rank_bucket`은 손실과 DD(drawdown, 손실폭) 악화를 만들었다. 효과는 rank bucket(순위 구간)을 함부로 제거하면 깨진다는 실패 기억으로 남기는 것이다.",
        "proxy adapter(대체 어댑터) 변형 중 volatility/ATR(변동성/ATR) 축은 여러 후보에서 net profit(순수익)과 DD(drawdown, 손실폭)를 동시에 개선했다. 다만 내부 feature ablation(내부 피처 제거)이 아니므로 다음에는 실제 feature/order(피처/순서) 검토가 필요하다.",
        "",
        "## Candidate Read(후보별 판독)",
        "",
        "| candidate(후보) | best test(최고 시험) | best net(최고 순수익) | avg net delta(평균 순수익 차이) | avg DD delta(평균 손실폭 차이) | destructive(파괴 실패) | read(판독) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in candidate_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['best_test_id']}` | {cell(row['best_net_profit'])} | {cell(row['avg_net_profit_delta'])} | {cell(row['avg_dd_percent_delta'])} | {cell(row['destructive_failure_count'])} | {row['candidate_read']} |"
        )
    lines.extend(
        [
            "",
            "## Top KPI Clues(상위 KPI 단서)",
            "",
            "| candidate(후보) | test(시험) | boundary(경계) | net(순수익) | net delta(순수익 차이) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | DD delta(손실폭 차이) |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['test_id']}` | `{row['materialization_boundary']}` | {cell(row['p0_net_profit'])} | {cell(row['net_profit_delta'])} | {cell(row['p0_profit_factor'])} | {cell(row['p0_trade_count'])} | {cell(row['p0_dd_percent'])} | {cell(row['dd_percent_delta'])} |"
        )
    lines.extend(
        [
            "",
            "## Failure Memory(실패 기억)",
            "",
        ]
    )
    if failures:
        for row in failures:
            lines.append(
                f"- `{row['candidate_alias']}` `{row['test_id']}`: net(순수익) {cell(row['p0_net_profit'])}, DD%(손실폭) {cell(row['p0_dd_percent'])}. Effect(효과): rank/gate bucket(순위/게이트 구간) 직접 제거는 현재 후보군에서 취약한 축으로 기록한다."
            )
    else:
        lines.append("- destructive failure(파괴적 실패)는 KPI 기준에서 없다.")
    lines.extend(
        [
            "",
            "## Test Axis Summary(시험 축 요약)",
            "",
            "| test(시험) | boundary(경계) | avg net delta(평균 순수익 차이) | avg DD delta(평균 손실폭 차이) | best candidate(최고 후보) |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in sorted(test_rows, key=lambda item: as_float(item.get("avg_net_profit_delta")), reverse=True):
        lines.append(
            f"| `{row['test_id']}` | `{row['materialization_boundary']}` | {cell(row['avg_net_profit_delta'])} | {cell(row['avg_dd_percent_delta'])} | `{row['best_candidate_alias']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- result_subject(결과 대상): `run267N_pool_wide_ablation_replacement_p0_kpi_review`.",
            "- evidence_available(사용 가능 근거): execution result(실행 결과), KPI summary(KPI 요약), backtest forensics(백테스트 포렌식), KPI delta review(KPI 차이 검토).",
            "- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 확대, trade list(거래 목록) 품질, monthly/session/hour/weekday KPI(월/세션/시간/요일 KPI), internal feature ablation(내부 피처 제거) 확인.",
            "- judgment_label(판정 라벨): `kpi_diagnostic_only_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def upsert_registers(created_at: str, detail_count: int, candidate_count: int) -> None:
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267N_pool_wide_ablation_replacement_kpi_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_ablation_replacement_p0_kpi_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 pool-wide P0 KPI review",
            "scoreboard": "kpi_delta_review",
            "status": STATUS,
            "judgment": "kpi_diagnostic_only_no_candidate_selection",
            "evidence_boundary": "kpi_delta_only_no_curve_timeslice_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"detail_rows={detail_count};candidate_rows={candidate_count};next_action={NEXT_ACTION};selected_candidate=none.",
        },
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
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_pool_wide_p0_kpi_review",
            "status": STATUS,
            "judgment": "kpi_diagnostic_only_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267N pool-wide P0 KPI review; detail_rows={detail_count}; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_ablation_replacement_p0_kpi_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_ablation_replacement_p0_kpi_review",
            "parent_run_id": RUN_ID,
            "record_view": "pool_wide_ablation_replacement_p0_kpi_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 pool-wide P0 KPI review",
            "kpi_scope": "kpi_delta_no_curve_timeslice_yet",
            "scoreboard_lane": "kpi_delta_review",
            "status": STATUS,
            "judgment": "kpi_diagnostic_only_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"detail_rows={detail_count};candidate_rows={candidate_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "completed_mt5_kpi_review_pending_curve_timeslice",
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
    artifact_rows = read_csv(ARTIFACT_REGISTRY_PATH)
    entries = (
        ("stage267_run267N_pool_wide_p0_kpi_review_script", "producer_script", PRODUCER_PATH, "Builds run267N KPI delta review."),
        ("stage267_run267N_pool_wide_p0_kpi_delta_review", "kpi_delta_review", DETAIL_PATH, "Run267N per-attempt KPI delta review."),
        ("stage267_run267N_pool_wide_p0_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267N candidate KPI delta summary."),
        ("stage267_run267N_pool_wide_p0_test_summary", "test_summary", TEST_SUMMARY_PATH, "Run267N test-axis KPI delta summary."),
        ("stage267_run267N_pool_wide_p0_kpi_review_result", "review_result", REVIEW_RESULT_PATH, "Run267N KPI review result payload."),
        ("stage267_run267N_pool_wide_p0_kpi_review_report", "review_report", REPORT_PATH, "User-facing run267N KPI review report."),
    )
    new_rows = [
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
        for artifact_id, artifact_type, path, notes in entries
    ]
    replacement = {row["artifact_id"] for row in new_rows}
    merged = [row for row in artifact_rows if row.get("artifact_id") not in replacement]
    merged.extend(new_rows)
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def replace_status_tokens(text: str) -> str:
    for token in (
        materializer.STATUS,
        executor.COMPLETED_STATUS,
        executor.PARTIAL_STATUS,
        executor.BLOCKED_STATUS,
        STATUS,
    ):
        text = text.replace(token, STATUS)
    for token in (
        materializer.NEXT_ACTION,
        executor.NEXT_ACTION_COMPLETED,
        executor.NEXT_ACTION_PARTIAL,
        executor.NEXT_ACTION_BLOCKED,
        NEXT_ACTION,
    ):
        text = text.replace(token, NEXT_ACTION)
    return text


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def update_docs() -> None:
    current = replace_status_tokens(io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig"))
    current = current.replace(
        "- adapter_under_review(검토 중 어댑터): `pool_wide_ablation_replacement_p0_materialization`",
        "- adapter_under_review(검토 중 어댑터): `pool_wide_ablation_replacement_p0_kpi_review`",
    )
    current = append_after_contains(
        current,
        "stage267_run267N_pool_wide_ablation_replacement_mt5_execution.md",
        f"- Stage267(267단계) run267N pool-wide P0 KPI review(후보군 전체 P0 KPI 검토): `{rel(REPORT_PATH)}`",
    )
    current = current.replace(
        "- action(행동): run267N(267N 실행)는 run267M(267M 실행)의 P0 queue(P0 큐)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.",
        "- action(행동): run267N(267N 실행)는 48개 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)를 baseline(기준) 2024 KPI와 비교했다.",
    )
    current = current.replace(
        "- effect(효과): 다음 작업은 같은 후보군의 P0 변형을 MT5(MetaTrader 5, 메타트레이더5)에서 실행해 누가 덜 깨지는지 확인할 수 있다.",
        "- effect(효과): 다음 작업은 balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), time-slice KPI(시간 구간 핵심 성과 지표)로 KPI 단서를 압박 검토하는 것이다.",
    )
    current = current.replace(
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 물질화된 P0 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) 묶음 실행으로 넘긴다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): KPI 단서를 balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), time-slice KPI(시간 구간 핵심 성과 지표)로 검토한다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    for path in (SELECTION_STATUS_PATH, REVIEW_INDEX_PATH, WORKSPACE_STATE_PATH):
        text = replace_status_tokens(io_path(path).read_text(encoding="utf-8-sig"))
        if path == WORKSPACE_STATE_PATH:
            text = text.replace(
                "Stage267(267단계) run267N(267N 실행) pool-wide P0 materialization(후보군 전체 P0 물질화) `run267N_pool_wide_ablation_replacement_kpi_review_completed`. Effect(효과): run267M(267M 실행)의 P0 queue(P0 큐)를 `24`개 feature/model/set/ini(피처/모델/설정/초기화) 변형과 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)로 고정했으며 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
                "Stage267(267단계) run267N(267N 실행) pool-wide P0 KPI review(후보군 전체 P0 KPI 검토) `run267N_pool_wide_ablation_replacement_kpi_review_completed`. Effect(효과): 48개 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)를 2024 baseline(기준)과 비교했고 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
            )
            text = text.replace(
                "Effect(효과): 물질화된 P0 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) 묶음 실행으로 넘긴다.",
                "Effect(효과): KPI 단서를 balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), time-slice KPI(시간 구간 핵심 성과 지표)로 검토한다.",
            )
            text = text.replace(
                "is active_run267N_pool_wide_ablation_replacement_kpi_review_completed(267N 후보군 전체 제거/대체 물질화 완료, 실행 대기 활성).",
                "is active_run267N_pool_wide_ablation_replacement_kpi_review_completed(267N 후보군 전체 제거/대체 KPI 검토 완료, 곡선/시간구간 검토 대기 활성).",
            )
            text = append_after_contains(
                text,
                "run267N_pool_wide_ablation_replacement_mt5_execution_report_path",
                f"  run267N_pool_wide_ablation_replacement_kpi_review_report_path: {rel(REPORT_PATH)}",
            )
        else:
            text = append_after_contains(
                text,
                "run267N_pool_wide_ablation_replacement_mt5_execution",
                f"- run267N_pool_wide_ablation_replacement_kpi_review(267N 후보군 전체 제거/대체 KPI 검토): `{rel(REPORT_PATH)}`",
            )
        write_md(path, text)


def main() -> int:
    if not path_exists(EXECUTION_RESULT_PATH):
        raise FileNotFoundError(EXECUTION_RESULT_PATH)
    created_at = utc_now()
    detail = build_detail_rows()
    candidate_rows = summarize_candidates(detail)
    test_rows = summarize_tests(detail)
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "detail_rows": len(detail),
        "candidate_rows": len(candidate_rows),
        "test_rows": len(test_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(
        DETAIL_PATH,
        detail,
        (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "materialization_boundary",
            "route_role",
            "tier_scope",
            "status",
            "base_net_profit",
            "p0_net_profit",
            "net_profit_delta",
            "base_profit_factor",
            "p0_profit_factor",
            "profit_factor_delta",
            "base_trade_count",
            "p0_trade_count",
            "trade_count_delta",
            "base_dd_percent",
            "p0_dd_percent",
            "dd_percent_delta",
            "base_recovery_factor",
            "p0_recovery_factor",
            "recovery_factor_delta",
            "review_label",
        ),
    )
    write_csv(CANDIDATE_SUMMARY_PATH, candidate_rows, tuple(candidate_rows[0].keys()))
    write_csv(TEST_SUMMARY_PATH, test_rows, tuple(test_rows[0].keys()))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(detail, candidate_rows, test_rows))
    upsert_registers(created_at, len(detail), len(candidate_rows))
    update_docs()
    print(json.dumps({"status": STATUS, "detail_rows": len(detail), "candidate_rows": len(candidate_rows), "next_action": NEXT_ACTION}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
