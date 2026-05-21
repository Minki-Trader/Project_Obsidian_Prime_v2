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

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import run267X_true_internal_ablation_score_table_executor as executor


STAGE_ID = executor.STAGE_ID
RUN_ID = "run267Y_stage267_true_internal_ablation_kpi_signature_review_v1"
PARENT_RUN_ID = executor.RUN_ID
CLAIM_BOUNDARY = executor.CLAIM_BOUNDARY
RUN_ROOT = executor.STAGE_ROOT / "02_runs" / "run267Y" / "true_internal_ablation_kpi_signature_review"
REVIEWS_ROOT = executor.REVIEWS_ROOT

KPI_SUMMARY_PATH = executor.KPI_SUMMARY_PATH
FORENSICS_PATH = executor.FORENSICS_PATH
EXECUTION_RESULT_PATH = executor.EXECUTION_RESULT_PATH
SOURCE_VARIANT_MANIFEST_PATH = executor.SOURCE_VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = executor.SOURCE_RUNTIME_CONTRACT_PATH

SIGNATURE_MATRIX_PATH = RUN_ROOT / "true_internal_kpi_signature_matrix.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_kpi_resilience_summary.csv"
TOP_VARIANTS_PATH = RUN_ROOT / "top_variant_kpi_table.csv"
TIER_DUPLICATE_AUDIT_PATH = RUN_ROOT / "tier_duplicate_audit.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267Y_true_internal_ablation_kpi_signature_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267Y_true_internal_ablation_kpi_signature_review.py")

STAGE_LEDGER_PATH = executor.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = executor.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = executor.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = executor.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = executor.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = executor.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = executor.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = executor.REVIEW_INDEX_PATH

STATUS = "run267Y_true_internal_ablation_kpi_signature_review_completed"
JUDGMENT = "diagnostic_kpi_review_completed_routed_total_gap_named_no_candidate_selection"
NEXT_ACTION = "run267Z_balance_timeslice_trade_quality_review_true_internal_ablation_results"

STAGE_LEDGER_COLUMNS = executor.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = executor.ARTIFACT_COLUMNS

METRIC_KEYS = (
    "net_profit",
    "profit_factor",
    "trade_count",
    "expectancy",
    "max_drawdown_percent",
    "recovery_factor",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


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


def as_int(value: Any) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def metric_signature(row: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(str(row.get(key, "")) for key in METRIC_KEYS)


def compact(values: Sequence[Any]) -> str:
    return ";".join(sorted({str(value) for value in values if str(value) != ""}))


def tier_a_rows(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    return [row for row in rows if str(row.get("tier_scope")) == "Tier A"]


def build_signature_matrix(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, ...], list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        buckets[metric_signature(row)].append(row)
    matrix: list[dict[str, Any]] = []
    for index, (signature, members) in enumerate(sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0])), start=1):
        net_profit, profit_factor, trade_count, expectancy, max_dd, recovery = signature
        tier_scopes = {str(row.get("tier_scope", "")) for row in members}
        matrix.append(
            {
                "signature_id": f"sig{index:02d}",
                "member_count": len(members),
                "candidate_count": len({row.get("candidate_alias") for row in members}),
                "test_count": len({row.get("test_id") for row in members}),
                "tier_scope_count": len(tier_scopes),
                "net_profit": net_profit,
                "profit_factor": profit_factor,
                "trade_count": trade_count,
                "expectancy": expectancy,
                "max_drawdown_percent": max_dd,
                "recovery_factor": recovery,
                "candidates": compact([row.get("candidate_alias") for row in members]),
                "tests": compact([row.get("test_id") for row in members]),
                "tier_scopes": compact(tier_scopes),
                "interpretation": (
                    "tier_a_and_tier_ab_duplicate_due_to_fallback_disabled"
                    if tier_scopes == {"Tier A", "Tier A+B"} and len(members) == 2
                    else "distinct_runtime_metric_signature"
                ),
            }
        )
    return matrix


def build_candidate_summary(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in tier_a_rows(rows):
        grouped[str(row.get("candidate_alias", ""))].append(row)
    output: list[dict[str, Any]] = []
    for candidate, items in sorted(grouped.items()):
        nets = [as_float(row.get("net_profit")) for row in items]
        dds = [as_float(row.get("max_drawdown_percent")) for row in items]
        pfs = [as_float(row.get("profit_factor")) for row in items]
        trades = [as_int(row.get("trade_count")) for row in items]
        output.append(
            {
                "candidate_alias": candidate,
                "tier_a_attempt_count": len(items),
                "unique_tier_a_signature_count": len({metric_signature(row) for row in items}),
                "net_profit_min": min(nets),
                "net_profit_max": max(nets),
                "net_profit_mean": sum(nets) / len(nets),
                "profit_factor_min": min(pfs),
                "profit_factor_max": max(pfs),
                "max_drawdown_percent_worst": max(dds),
                "max_drawdown_percent_best": min(dds),
                "trade_count_total": sum(trades),
                "trade_count_min": min(trades),
                "trade_count_max": max(trades),
                "resilience_read": "needs_curve_timeslice_review_before_ranking",
                "selection_read": "no_selected_candidate",
            }
        )
    return output


def build_top_variants(rows: Sequence[Mapping[str, str]], limit: int = 12) -> list[dict[str, Any]]:
    ranked = sorted(tier_a_rows(rows), key=lambda row: as_float(row.get("net_profit")), reverse=True)
    output: list[dict[str, Any]] = []
    for rank, row in enumerate(ranked[:limit], start=1):
        output.append(
            {
                "rank_by_net_profit_tier_a": rank,
                "candidate_alias": row.get("candidate_alias"),
                "candidate_id": row.get("candidate_id"),
                "test_id": row.get("test_id"),
                "feature_family": row.get("feature_family"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "max_drawdown_percent": row.get("max_drawdown_percent"),
                "recovery_factor": row.get("recovery_factor"),
                "ranking_boundary": "not_candidate_selection_requires_curve_timeslice_review",
            }
        )
    return output


def build_tier_duplicate_audit(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    by_queue: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        by_queue[str(row.get("queue_id"))].append(row)
    audit: list[dict[str, Any]] = []
    for queue_id, items in sorted(by_queue.items()):
        ta = next((row for row in items if row.get("tier_scope") == "Tier A"), None)
        rt = next((row for row in items if row.get("tier_scope") == "Tier A+B"), None)
        if not ta or not rt:
            status = "missing_tier_pair"
            same = False
        else:
            same = metric_signature(ta) == metric_signature(rt)
            status = "duplicate_due_to_fallback_disabled" if same else "tier_metric_differs"
        audit.append(
            {
                "queue_id": queue_id,
                "candidate_alias": (ta or rt or {}).get("candidate_alias", ""),
                "test_id": (ta or rt or {}).get("test_id", ""),
                "tier_pair_present": bool(ta and rt),
                "metric_signature_same": same,
                "audit_status": status,
                "interpretation": "Tier A+B row is not fallback evidence when fallback is disabled" if same else "inspect routed setup",
            }
        )
    return audit


def upsert_stage_ledger(result: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267Y_true_internal_ablation_kpi_signature_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "true_internal_ablation_kpi_signature_review",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate audit",
                "scoreboard": "kpi_signature_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "kpi_review_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": (
                    f"unique_signatures={result['unique_metric_signatures']};"
                    f"tier_duplicate_pairs={result['tier_duplicate_pairs']};"
                    f"next_action={NEXT_ACTION};selected_candidate=none."
                ),
            }
        ],
        key="row_id",
    )


def upsert_run_registers(result: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "true_internal_ablation_kpi_signature_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": (
                    f"Run267Y KPI signature review; unique_signatures={result['unique_metric_signatures']}; "
                    f"tier_duplicate_pairs={result['tier_duplicate_pairs']}; selected_candidate=none; "
                    f"onnx_readiness=not_claimed; next_action={NEXT_ACTION}."
                ),
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__true_internal_ablation_kpi_signature_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "true_internal_ablation_kpi_signature_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "true_internal_ablation_kpi_signature_review",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate audit",
                "kpi_scope": "kpi_signature_distinguishability_and_routed_gap",
                "scoreboard_lane": "kpi_signature_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"unique_signatures={result['unique_metric_signatures']};top_net={result['top_net_profit']}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267Y_review_script", "producer_script", PRODUCER_PATH, "Reviews run267X KPI signatures and Tier A+B duplicate boundary."),
        ("stage267_run267Y_signature_matrix", "review_matrix", SIGNATURE_MATRIX_PATH, "Run267X true internal KPI signature matrix."),
        ("stage267_run267Y_candidate_summary", "review_matrix", CANDIDATE_SUMMARY_PATH, "Candidate-level true internal KPI summary."),
        ("stage267_run267Y_top_variants", "review_matrix", TOP_VARIANTS_PATH, "Top Tier A net-profit variants with boundary."),
        ("stage267_run267Y_tier_duplicate_audit", "audit_matrix", TIER_DUPLICATE_AUDIT_PATH, "Tier A versus Tier A+B duplicate audit."),
        ("stage267_run267Y_review_result", "review_result", REVIEW_RESULT_PATH, "Run267Y review result payload."),
        ("stage267_run267Y_review_report", "review_report", REPORT_PATH, "User-facing run267Y KPI signature review."),
    )
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
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
    replacement_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement_ids]
    merged.extend(new_rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_markdown_field(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            break
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def update_workspace_state_text(text: str) -> str:
    lines = text.splitlines()
    in_stage267 = False
    inserted_path = False
    inserted_focus = False
    out: list[str] = []
    focus_line = (
        "  Stage267(267단계) run267Y(267Y 실행) true internal ablation KPI signature review"
        "(진짜 내부 제거 KPI 서명 검토) `{status}`. Effect(효과): run267X(267X 실행)의 "
        "48개 KPI(핵심 성과 지표)를 24개 true internal signature(진짜 내부 서명)와 "
        "24개 Tier A+B duplicate pair(Tier A+B 중복 쌍)로 분리했고 selected candidate(선택 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    ).format(status=STATUS)
    for line in lines:
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not inserted_focus:
            out.append(line)
            out.append("- >-")
            out.append(focus_line)
            inserted_focus = True
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            out.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                out.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                out.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                out.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                out.append(f"  next_action: {NEXT_ACTION}")
                continue
            if "run267X_true_internal_ablation_score_table_mt5_execution_report_path" in stripped and not inserted_path:
                out.append(line)
                out.append(f"  run267Y_true_internal_ablation_kpi_signature_review_report_path: {rel(REPORT_PATH)}")
                inserted_path = True
                continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_markdown_field(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_markdown_field(current, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `true_internal_ablation_kpi_signature_review`")
    current = replace_markdown_field(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_markdown_field(current, "- next_run(", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_markdown_field(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(
        current,
        "stage267_run267X_true_internal_ablation_score_table_mt5_execution.md",
        f"- Stage267(267단계) run267Y true internal ablation KPI signature review(진짜 내부 제거 KPI 서명 검토): `{rel(REPORT_PATH)}`",
    )
    current = append_after_contains(
        current,
        "## Current Next Action",
        (
            f"- latest_kpi_review(최신 KPI 검토): unique signatures(고유 서명) `{result['unique_metric_signatures']}`, "
            f"tier duplicate pairs(티어 중복 쌍) `{result['tier_duplicate_pairs']}`, report(보고서) `{rel(REPORT_PATH)}`."
        ),
    )
    current = current.rstrip() + (
        "\n\nRun267Y(267Y 실행)는 run267X(267X 실행)의 KPI signature(KPI 서명)를 검토했다.\n"
        "Effect(효과): true internal feature ablation(진짜 내부 피처 제거)은 proxy collapse(대체 접힘)를 벗어났지만, "
        "Tier A+B(Tier A+B 합산)는 fallback(대체)이 꺼진 중복 행이라 다음 곡선/시간구간 검토에서 경계를 유지한다.\n"
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_markdown_field(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_markdown_field(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_markdown_field(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_markdown_field(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(
        selection,
        "stage267_run267X_true_internal_ablation_score_table_mt5_execution.md",
        f"- run267Y_true_internal_ablation_kpi_signature_review(267Y 진짜 내부 제거 KPI 서명 검토): `{rel(REPORT_PATH)}`",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_markdown_field(review, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    review = append_after_contains(
        review,
        "stage267_run267X_true_internal_ablation_score_table_mt5_execution.md",
        f"- Stage267(267단계) run267Y true internal ablation KPI signature review(진짜 내부 제거 KPI 서명 검토): `{rel(REPORT_PATH)}`",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace))


def report_markdown(result: Mapping[str, Any]) -> str:
    top_rows = result["top_variants"][:8]
    candidate_rows = result["candidate_summary"]
    lines = [
        "# Stage267 Run267Y True Internal Ablation KPI Signature Review(267단계 267Y 진짜 내부 제거 KPI 서명 검토)",
        "",
        f"- action(행동): run267X(267X 실행)의 `48`개 KPI(핵심 성과 지표)를 signature(서명), candidate(후보), Tier pair(티어 쌍)로 나눠 봤다.",
        "- effect(효과): 숫자만 좋아 보이는지, 실제로 변형 차이가 살아났는지, 그리고 Tier A+B(Tier A+B 합산)가 진짜 fallback(대체) 근거인지 분리한다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- unique_metric_signatures(고유 지표 서명): `{result['unique_metric_signatures']}`",
        f"- tier_duplicate_pairs(티어 중복 쌍): `{result['tier_duplicate_pairs']}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267T(267T 실행)에서는 34개 MT5(MetaTrader 5, 메타트레이더5) 결과가 2개 KPI signature(KPI 서명)로 접혔다.",
        "이번 run267X(267X 실행)는 24개 true internal variant(진짜 내부 변형)가 각각 다른 Tier A(Tier A) signature(서명)를 만들었다.",
        "Effect(효과): 이전보다 후보와 제거/대체 축을 구분할 수 있게 됐다.",
        "",
        "하지만 Tier A+B(Tier A+B 합산)는 전부 Tier A(Tier A)와 같은 값이다.",
        "Effect(효과): fallback(대체)이 실제로 빈 구간을 메운 근거가 아니므로, 이 행은 routed robustness(라우팅 견고성) 근거로 쓰면 안 된다.",
        "",
        "숫자상 상위 후보는 보이지만, curve(곡선), weak month(약한 월), session/hour(세션/시간), trade quality(거래 품질)를 아직 보지 않았다.",
        "Effect(효과): selected candidate(선택 후보)나 ONNX(ONNX) 검토는 여전히 금지다.",
        "",
        "## Top Tier A Rows(상위 Tier A 행)",
        "",
        "| rank(순위) | candidate(후보) | test(시험) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | boundary(경계) |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in top_rows:
        lines.append(
            f"| {row['rank_by_net_profit_tier_a']} | `{row['candidate_alias']}` | `{row['test_id']}` | "
            f"{row['net_profit']} | {row['profit_factor']} | {row['trade_count']} | {row['max_drawdown_percent']} | "
            f"`{row['ranking_boundary']}` |"
        )
    lines.extend(
        [
            "",
            "## Candidate Summary(후보 요약)",
            "",
            "| candidate(후보) | rows(행) | net min(순수익 최소) | net max(순수익 최대) | net mean(순수익 평균) | worst DD%(최악 손실폭) | PF min(PF 최소) | trades total(거래 총수) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in candidate_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['tier_a_attempt_count']} | {row['net_profit_min']:.2f} | "
            f"{row['net_profit_max']:.2f} | {row['net_profit_mean']:.2f} | {row['max_drawdown_percent_worst']:.2f} | "
            f"{row['profit_factor_min']:.2f} | {row['trade_count_total']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- result_subject(결과 대상): `run267Y_true_internal_ablation_kpi_signature_review`.",
            "- positive_claim(긍정 주장): `none`.",
            "- useful_evidence(유용 근거): proxy collapse(대체 접힘)는 풀렸고, 24개 Tier A(Tier A) 변형이 서로 다른 KPI signature(KPI 서명)를 만들었다.",
            "- gap_named(이름 붙인 공백): Tier A+B(Tier A+B 합산)는 fallback disabled(대체 비활성)라 Tier A(Tier A) 중복이다.",
            "- missing_required(필수 누락): balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 KPI), trade quality(거래 품질), failure memory(실패 기억) 검토.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    if not path_exists(KPI_SUMMARY_PATH):
        raise FileNotFoundError(KPI_SUMMARY_PATH)
    created_at = utc_now()
    kpi_rows = read_csv_rows(KPI_SUMMARY_PATH)
    signature_matrix = build_signature_matrix(kpi_rows)
    candidate_summary = build_candidate_summary(kpi_rows)
    top_variants = build_top_variants(kpi_rows)
    tier_duplicate_audit = build_tier_duplicate_audit(kpi_rows)
    tier_duplicate_pairs = sum(1 for row in tier_duplicate_audit if row["audit_status"] == "duplicate_due_to_fallback_disabled")
    top_net_profit = top_variants[0]["net_profit"] if top_variants else ""
    result = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_execution_result": rel(EXECUTION_RESULT_PATH),
        "source_kpi_summary": rel(KPI_SUMMARY_PATH),
        "source_forensics": rel(FORENSICS_PATH),
        "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
        "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
        "kpi_rows": len(kpi_rows),
        "unique_metric_signatures": len(signature_matrix),
        "tier_a_unique_signatures": len({metric_signature(row) for row in tier_a_rows(kpi_rows)}),
        "tier_duplicate_pairs": tier_duplicate_pairs,
        "top_net_profit": top_net_profit,
        "signature_matrix": signature_matrix,
        "candidate_summary": candidate_summary,
        "top_variants": top_variants,
        "tier_duplicate_audit": tier_duplicate_audit,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }
    write_csv(SIGNATURE_MATRIX_PATH, signature_matrix)
    write_csv(CANDIDATE_SUMMARY_PATH, candidate_summary)
    write_csv(TOP_VARIANTS_PATH, top_variants)
    write_csv(TIER_DUPLICATE_AUDIT_PATH, tier_duplicate_audit)
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    upsert_stage_ledger(result)
    upsert_run_registers(result)
    update_current_truth_docs(result)
    upsert_artifacts(created_at)
    print(
        json.dumps(
            {
                "status": STATUS,
                "kpi_rows": len(kpi_rows),
                "unique_metric_signatures": len(signature_matrix),
                "tier_a_unique_signatures": result["tier_a_unique_signatures"],
                "tier_duplicate_pairs": tier_duplicate_pairs,
                "top_net_profit": top_net_profit,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
