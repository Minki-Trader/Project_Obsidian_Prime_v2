from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage267 import run267T_pool_wide_orthogonal_stability_executor as executor


STAGE_ID = executor.STAGE_ID
RUN_ID = executor.RUN_ID
CLAIM_BOUNDARY = executor.CLAIM_BOUNDARY
RUN_ROOT = executor.RUN_ROOT
REVIEWS_ROOT = executor.REVIEWS_ROOT

KPI_SUMMARY_PATH = executor.KPI_SUMMARY_PATH
FORENSICS_PATH = executor.FORENSICS_PATH
EXECUTION_RESULT_PATH = executor.EXECUTION_RESULT_PATH
SIGNATURE_MATRIX_PATH = RUN_ROOT / "orthogonal_stability_signature_matrix.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "orthogonal_stability_candidate_summary.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "orthogonal_stability_review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267T_pool_wide_orthogonal_stability_mt5_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267T_pool_wide_orthogonal_stability_mt5_review.py")

STAGE_LEDGER_PATH = executor.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = executor.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = executor.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = executor.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = executor.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = executor.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = executor.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = executor.REVIEW_INDEX_PATH

STATUS = "run267T_pool_wide_orthogonal_stability_mt5_review_completed"
NEXT_ACTION = "run267U_design_true_internal_feature_ablation_after_run267T_signature_collapse"
JUDGMENT = "negative_distinguishability_result_reusable_failure_memory"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return math.nan
    return number if math.isfinite(number) else math.nan


def metric_signature(row: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(
        str(row.get(key, ""))
        for key in (
            "net_profit",
            "profit_factor",
            "trade_count",
            "expectancy",
            "max_drawdown_percent",
            "recovery_factor",
        )
    )


def compact(values: Sequence[Any]) -> str:
    return ";".join(sorted({str(value) for value in values if str(value) != ""}))


def build_signature_matrix(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, ...], list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        buckets[metric_signature(row)].append(row)

    matrix: list[dict[str, Any]] = []
    for index, (signature, members) in enumerate(sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0])), start=1):
        net_profit, profit_factor, trade_count, expectancy, max_dd, recovery = signature
        axes = compact([row.get("axis_id") for row in members])
        tests = compact([row.get("test_id") for row in members])
        candidates = compact([row.get("candidate_alias") for row in members])
        tier_scopes = compact([row.get("tier_scope") for row in members])
        matrix.append(
            {
                "signature_id": f"sig{index:02d}",
                "member_count": len(members),
                "candidate_count": len({row.get("candidate_alias") for row in members}),
                "axis_count": len({row.get("axis_id") for row in members}),
                "test_count": len({row.get("test_id") for row in members}),
                "tier_scope_count": len({row.get("tier_scope") for row in members}),
                "net_profit": net_profit,
                "profit_factor": profit_factor,
                "trade_count": trade_count,
                "expectancy": expectancy,
                "max_drawdown_percent": max_dd,
                "recovery_factor": recovery,
                "candidates": candidates,
                "axes": axes,
                "tests": tests,
                "tier_scopes": tier_scopes,
                "interpretation": "signature_collapse_cluster_candidate_distinction_weak",
            }
        )
    return matrix


def build_candidate_summary(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("candidate_alias", ""))].append(row)

    output: list[dict[str, Any]] = []
    for candidate, items in sorted(grouped.items()):
        signatures = {metric_signature(row) for row in items}
        net_values = [as_float(row.get("net_profit")) for row in items]
        dd_values = [as_float(row.get("max_drawdown_percent")) for row in items]
        trade_values = [as_float(row.get("trade_count")) for row in items]
        output.append(
            {
                "candidate_alias": candidate,
                "attempt_count": len(items),
                "unique_signature_count": len(signatures),
                "axis_count": len({row.get("axis_id") for row in items}),
                "test_count": len({row.get("test_id") for row in items}),
                "tier_scope_count": len({row.get("tier_scope") for row in items}),
                "net_profit_min": min(net_values),
                "net_profit_max": max(net_values),
                "max_drawdown_percent_worst": max(dd_values),
                "trade_count_total": sum(trade_values),
                "distinguishability_read": "weak_candidate_separation" if len(signatures) <= 2 else "candidate_separation_present",
                "selection_read": "no_selected_candidate",
            }
        )
    return output


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv_rows(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def upsert_stage_ledger() -> None:
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267T_pool_wide_orthogonal_stability_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_orthogonal_stability_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 orthogonal stability attempts",
            "scoreboard": "runtime_review_failure_memory",
            "status": STATUS,
            "judgment": JUDGMENT,
            "evidence_boundary": "mt5_runtime_review_no_candidate_selection_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"signature_matrix={rel(SIGNATURE_MATRIX_PATH)}; next_action={NEXT_ACTION}; selected_candidate=none.",
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


def upsert_run_registers() -> None:
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "pool_wide_orthogonal_stability_mt5_review",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "notes": f"Run267T review found KPI signature collapse; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_stability_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_orthogonal_stability_mt5_review",
            "parent_run_id": RUN_ID,
            "record_view": "pool_wide_orthogonal_stability_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 orthogonal stability attempts",
            "kpi_scope": "signature_collapse_and_candidate_distinguishability",
            "scoreboard_lane": "runtime_review_failure_memory",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": "unique_metric_signatures=2;candidate_selection=none",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
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


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267T_orthogonal_review_script", "producer_script", PRODUCER_PATH, "Reviews run267T MT5 execution for signature collapse and candidate distinguishability."),
        ("stage267_run267T_orthogonal_signature_matrix", "review_matrix", SIGNATURE_MATRIX_PATH, "Metric signature collapse matrix for run267T."),
        ("stage267_run267T_orthogonal_candidate_summary", "review_matrix", CANDIDATE_SUMMARY_PATH, "Candidate-level stability summary for run267T."),
        ("stage267_run267T_orthogonal_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload for run267T."),
        ("stage267_run267T_orthogonal_mt5_review_report", "review_report", REPORT_PATH, "User-facing run267T MT5 review report."),
    )
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows: list[dict[str, Any]] = []
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
    replacement_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement_ids]
    merged.extend(new_rows)
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_status_and_next_action(text: str) -> str:
    tokens = (
        executor.COMPLETED_STATUS,
        executor.PARTIAL_STATUS,
        executor.BLOCKED_STATUS,
        STATUS,
    )
    for token in tokens:
        text = text.replace(token, STATUS)
    for token in (
        executor.NEXT_ACTION_COMPLETED,
        executor.NEXT_ACTION_PARTIAL,
        executor.NEXT_ACTION_BLOCKED,
        NEXT_ACTION,
    ):
        text = text.replace(token, NEXT_ACTION)
    return text


def update_current_truth_docs() -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_status_and_next_action(current)
    current = append_after_contains(
        current,
        "stage267_run267T_pool_wide_orthogonal_stability_mt5_execution.md",
        f"- Stage267(267단계) run267T pool-wide orthogonal stability MT5 review(후보군 전체 직교 안정성 MT5 검토): `{rel(REPORT_PATH)}`",
    )
    current = append_after_contains(
        current,
        "## Current Next Action",
        "- latest_mt5_review(최신 MT5 검토): unique metric signatures(고유 지표 서명) `2`, selected_candidate(선택 후보) `none`, report(보고서) "
        f"`{rel(REPORT_PATH)}`.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_status_and_next_action(selection)
    selection = append_after_contains(
        selection,
        "run267T_pool_wide_orthogonal_stability_mt5_execution",
        f"- run267T_pool_wide_orthogonal_stability_mt5_review(267T 후보군 전체 직교 안정성 MT5 검토): `{rel(REPORT_PATH)}`",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_status_and_next_action(review)
    review = append_after_contains(
        review,
        "run267T_pool_wide_orthogonal_stability_mt5_execution",
        f"- run267T_pool_wide_orthogonal_stability_mt5_review(267T 후보군 전체 직교 안정성 MT5 검토): `{rel(REPORT_PATH)}`",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_status_and_next_action(workspace)
    workspace = append_after_contains(
        workspace,
        "run267T_pool_wide_orthogonal_stability_mt5_execution_report_path",
        f"  run267T_pool_wide_orthogonal_stability_mt5_review_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any]) -> str:
    signature_rows = list(result["signature_matrix"])
    candidate_rows = list(result["candidate_summary"])
    lines = [
        "# Stage267 Run267T Pool-Wide Orthogonal Stability MT5 Review(267단계 267T 후보군 전체 직교 안정성 MT5 검토)",
        "",
        "- action(행동): run267T(267T 실행)의 34개 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)를 signature(서명) 단위로 묶어 검토했다.",
        "- effect(효과): 후보가 실제로 서로 다른 안정성 표면을 만들었는지, 아니면 proxy variant(대체 변형)가 같은 결과로 접혔는지 확인한다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "실행은 성공했다. 하지만 좋은 소식만은 아니다. 34개 결과가 단 2개의 KPI signature(KPI 서명)로 접혔다.",
        "효과는 명확하다. 이번 proxy adapter variant(대체 어댑터 변형)는 후보별 차이를 충분히 드러내지 못했다. 그래서 숫자가 좋아 보이는 행이 있어도 후보 선정이나 ONNX(ONNX) 검토로 갈 수 없다.",
        "다음은 true internal feature ablation(진짜 내부 피처 제거) 또는 더 직접적인 feature path(피처 경로) 재설계가 필요하다.",
        "",
        "## Signature Matrix(서명 행렬)",
        "",
        "| signature(서명) | rows(행) | candidates(후보) | axes(축) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in signature_rows:
        lines.append(
            f"| `{row['signature_id']}` | {row['member_count']} | {row['candidate_count']} | {row['axis_count']} | "
            f"{row['net_profit']} | {row['profit_factor']} | {row['trade_count']} | {row['max_drawdown_percent']} | `{row['interpretation']}` |"
        )
    lines.extend(
        [
            "",
            "## Candidate Summary(후보 요약)",
            "",
            "| candidate(후보) | attempts(시도) | signatures(서명) | net min(순수익 최소) | net max(순수익 최대) | worst DD%(최악 손실폭) | read(판독) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in candidate_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['attempt_count']} | {row['unique_signature_count']} | "
            f"{row['net_profit_min']:.2f} | {row['net_profit_max']:.2f} | {row['max_drawdown_percent_worst']:.2f} | `{row['distinguishability_read']}` |"
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267T_pool_wide_orthogonal_stability_mt5_review`.",
            "- positive_claim(긍정 주장): 없음.",
            "- negative_evidence(부정 근거): KPI signature collapse(KPI 서명 접힘)가 있어 후보 구분성이 약하다.",
            "- reusable_clue(재사용 단서): axis01(1축)은 순수익 `236.31`, PF(수익 팩터) `1.3`, trades(거래 수) `454` 서명으로 접혔고, axis02(2축)는 순수익 `177.49`, PF(수익 팩터) `1.2`, trades(거래 수) `486` 서명으로 접혔다.",
            "- missing_evidence(빠진 근거): true internal feature ablation(진짜 내부 피처 제거), balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 핵심 성과 지표) 재검토.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    if not path_exists(KPI_SUMMARY_PATH):
        raise FileNotFoundError(KPI_SUMMARY_PATH)
    if not path_exists(EXECUTION_RESULT_PATH):
        raise FileNotFoundError(EXECUTION_RESULT_PATH)
    created_at = utc_now()
    kpi_rows = read_csv_rows(KPI_SUMMARY_PATH)
    execution_result = json.loads(io_path(EXECUTION_RESULT_PATH).read_text(encoding="utf-8-sig"))
    signature_matrix = build_signature_matrix(kpi_rows)
    candidate_summary = build_candidate_summary(kpi_rows)
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_execution_result": rel(EXECUTION_RESULT_PATH),
        "source_kpi_summary": rel(KPI_SUMMARY_PATH),
        "source_forensics": rel(FORENSICS_PATH),
        "execution_status": execution_result.get("execution_status"),
        "attempt_count": len(kpi_rows),
        "unique_metric_signatures": len(signature_matrix),
        "signature_matrix": signature_matrix,
        "candidate_summary": candidate_summary,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }
    write_csv(SIGNATURE_MATRIX_PATH, signature_matrix)
    write_csv(CANDIDATE_SUMMARY_PATH, candidate_summary)
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    upsert_stage_ledger()
    upsert_run_registers()
    update_current_truth_docs()
    upsert_artifacts(created_at)
    print(
        json.dumps(
            {
                "status": STATUS,
                "attempt_count": len(kpi_rows),
                "unique_metric_signatures": len(signature_matrix),
                "judgment": JUDGMENT,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
