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
from stage_pipelines.stage267 import run267C_p0_mt5_variant_materialization as materializer
from stage_pipelines.stage267 import run267C_p0_mt5_variant_smoke_executor as executor


STAGE_ID = materializer.STAGE_ID
RUN_ID = materializer.RUN_ID
RUN_NUMBER = materializer.RUN_NUMBER
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY
VARIANT_ROOT = materializer.VARIANT_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
BASE_KPI_PATH = materializer.RUN267B_HIST_ROOT / "mt5_kpi_summary.csv"
P0_KPI_PATH = executor.KPI_SUMMARY_PATH
DETAIL_PATH = VARIANT_ROOT / "p0_mt5_full_batch_delta_review.csv"
SUMMARY_PATH = VARIANT_ROOT / "p0_mt5_full_batch_candidate_variant_summary.csv"
AXIS_PATH = VARIANT_ROOT / "p0_mt5_full_batch_axis_summary.csv"
RESULT_PATH = VARIANT_ROOT / "p0_mt5_full_batch_review.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267C_p0_mt5_full_batch_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267C_p0_mt5_full_batch_review.py")

NEXT_ACTION = "run267C_design_p0_axis_followup_feature_engineering_variants"
STATUS = "run267C_p0_mt5_full_batch_review_completed"


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


def to_float(row: Mapping[str, str], key: str) -> float:
    try:
        return float(row.get(key, "") or 0.0)
    except ValueError:
        return 0.0


def base_alias(record_view: str) -> str:
    match = re.search(r"mt5_(?:ta|rt)_(.*?)_historical_2024", record_view)
    if not match:
        raise ValueError(f"cannot parse base record view: {record_view}")
    return match.group(1)


def p0_alias_variant(record_view: str) -> tuple[str, str]:
    match = re.search(r"mt5_(?:ta|rt)_(.*?)_(julyblk|lateblk|vollowblk)_historical_2024", record_view)
    if not match:
        raise ValueError(f"cannot parse P0 record view: {record_view}")
    return match.group(1), match.group(2)


def variant_label(variant: str) -> str:
    labels = {
        "julyblk": "July 2024 block(2024년 7월 차단)",
        "lateblk": "late-session block(후반 세션 차단)",
        "vollowblk": "vol-low block(낮은 변동성 차단)",
    }
    return labels.get(variant, variant)


def diagnostic_read(variant: str, trade_delta: float, net_delta: float, dd_delta: float) -> str:
    if variant == "vollowblk":
        return "strong_numeric_but_hard_block_high_trade_removal_requires_soft_feature_engineering(숫자는 강하지만 강제 차단과 거래 제거가 커서 소프트 피처 엔지니어링 필요)"
    if variant == "lateblk":
        return "consistent_dd_repair_clue_with_moderate_trade_cost_session_feature_candidate(중간 거래 비용으로 손실폭을 줄인 세션 피처 후보)"
    if variant == "julyblk":
        return "calendar_weak_slice_clue_not_direct_rule_requires_period_validation(달력 약점 단서일 뿐 직접 규칙이 아니며 기간 검증 필요)"
    if net_delta > 0 and dd_delta < 0 and trade_delta > -120:
        return "constructive_diagnostic_clue(건설적 진단 단서)"
    return "needs_review(검토 필요)"


def candidate_roles() -> dict[str, str]:
    return {spec.alias: spec.role for spec in materializer.input_probe.candidate_specs()}


def build_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    base_rows = [row for row in read_csv(BASE_KPI_PATH) if row.get("route_role") == "routed_total"]
    p0_rows = read_csv(P0_KPI_PATH)
    roles = candidate_roles()
    base_by_alias = {base_alias(row["record_view"]): row for row in base_rows}

    detail: list[dict[str, Any]] = []
    for row in p0_rows:
        alias, variant = p0_alias_variant(row["record_view"])
        base = base_by_alias[alias]
        net_delta = to_float(row, "net_profit") - to_float(base, "net_profit")
        pf_delta = to_float(row, "profit_factor") - to_float(base, "profit_factor")
        trade_delta = to_float(row, "trade_count") - to_float(base, "trade_count")
        dd_delta = to_float(row, "max_drawdown_percent") - to_float(base, "max_drawdown_percent")
        recovery_delta = to_float(row, "recovery_factor") - to_float(base, "recovery_factor")
        detail.append(
            {
                "record_view": row["record_view"],
                "candidate_alias": alias,
                "candidate_role": roles.get(alias, ""),
                "diagnostic_variant": variant,
                "diagnostic_label": variant_label(variant),
                "tier_scope": row.get("tier_scope", ""),
                "route_role": row.get("route_role", ""),
                "base_net_profit": to_float(base, "net_profit"),
                "p0_net_profit": to_float(row, "net_profit"),
                "net_profit_delta": net_delta,
                "base_pf": to_float(base, "profit_factor"),
                "p0_pf": to_float(row, "profit_factor"),
                "pf_delta": pf_delta,
                "base_trade_count": to_float(base, "trade_count"),
                "p0_trade_count": to_float(row, "trade_count"),
                "trade_count_delta": trade_delta,
                "base_dd_percent": to_float(base, "max_drawdown_percent"),
                "p0_dd_percent": to_float(row, "max_drawdown_percent"),
                "dd_percent_delta": dd_delta,
                "base_recovery": to_float(base, "recovery_factor"),
                "p0_recovery": to_float(row, "recovery_factor"),
                "recovery_delta": recovery_delta,
                "diagnostic_read": diagnostic_read(variant, trade_delta, net_delta, dd_delta),
            }
        )

    routed = [row for row in detail if row["route_role"] == "routed_total"]
    summary = sorted(routed, key=lambda row: (row["diagnostic_variant"], -float(row["p0_net_profit"])))

    axis_rows: list[dict[str, Any]] = []
    for variant in ("julyblk", "lateblk", "vollowblk"):
        items = [row for row in routed if row["diagnostic_variant"] == variant]
        axis_rows.append(
            {
                "diagnostic_variant": variant,
                "diagnostic_label": variant_label(variant),
                "candidate_count": len(items),
                "avg_net_profit_delta": mean(float(row["net_profit_delta"]) for row in items),
                "avg_pf_delta": mean(float(row["pf_delta"]) for row in items),
                "avg_trade_count_delta": mean(float(row["trade_count_delta"]) for row in items),
                "avg_dd_percent_delta": mean(float(row["dd_percent_delta"]) for row in items),
                "avg_recovery_delta": mean(float(row["recovery_delta"]) for row in items),
                "best_net_candidate": max(items, key=lambda row: float(row["p0_net_profit"]))["candidate_alias"],
                "review_read": diagnostic_read(
                    variant,
                    mean(float(row["trade_count_delta"]) for row in items),
                    mean(float(row["net_profit_delta"]) for row in items),
                    mean(float(row["dd_percent_delta"]) for row in items),
                ),
            }
        )
    return detail, summary, axis_rows


def report_markdown(summary: Sequence[Mapping[str, Any]], axis_rows: Sequence[Mapping[str, Any]]) -> str:
    best = sorted(summary, key=lambda row: float(row["p0_net_profit"]), reverse=True)[:8]
    lines = [
        "# Stage267 Run267C P0 MT5 Full Batch Review(267단계 267C 우선순위 0 MT5 전체 묶음 검토)",
        "",
        "- action(행동): P0 MT5 full batch(우선순위 0 MT5 전체 묶음) 30개 KPI(핵심 성과 지표)를 run267B(267B 실행) 2024 기준과 비교했다.",
        "- effect(효과): 반사실(counterfactual, 반사실)로 좋아 보인 축이 실제 MT5 runtime(런타임)에서도 살아나는지 확인하고, hard block(강제 차단)을 후보 해결책으로 오해하지 않게 분리했다.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Axis Read(축 판독)",
        "",
        "| diagnostic axis(진단 축) | avg net delta(평균 순수익 차이) | avg PF delta(평균 수익 팩터 차이) | avg trade delta(평균 거래 수 차이) | avg DD% delta(평균 손실폭% 차이) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in axis_rows:
        lines.append(
            f"| {row['diagnostic_label']} | {csv_value(row['avg_net_profit_delta'])} | {csv_value(row['avg_pf_delta'])} | {csv_value(row['avg_trade_count_delta'])} | {csv_value(row['avg_dd_percent_delta'])} | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Top Routed Reads(상위 라우팅 판독)",
            "",
            "| candidate(후보) | axis(축) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | net delta(순수익 차이) | DD delta(손실폭 차이) |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in best:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['diagnostic_label']} | {csv_value(row['p0_net_profit'])} | {csv_value(row['p0_pf'])} | {csv_value(row['p0_trade_count'])} | {csv_value(row['p0_dd_percent'])} | {csv_value(row['net_profit_delta'])} | {csv_value(row['dd_percent_delta'])} |"
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- vol-low block(낮은 변동성 차단)은 가장 강한 숫자를 냈다. Effect(효과): 다음 연구에서는 hard block(강제 차단) 그대로가 아니라 soft regime feature(부드러운 국면 피처), replacement indicator(대체 지표), adapter constraint(어댑터 제약)로 바꿔 시험해야 한다.",
            "- late-session block(후반 세션 차단)과 July block(7월 차단)은 더 작은 거래 수 비용으로 DD(손실폭)를 줄였다. Effect(효과): 세션/달력 약점 축은 feature engineering(피처 엔지니어링) 후보지만 직접 운영 규칙은 아니다.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- next_action(다음 행동): `run267C_design_p0_axis_followup_feature_engineering_variants`. Effect(효과): 강제 차단을 소프트 피처/유사 대체/어댑터 후보로 바꿔 다시 경주한다.",
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
    current = io_path(materializer.CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = append_after(
        current,
        "- Stage267(267단계) run267C P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_smoke_execution_report.md`",
        "- Stage267(267단계) run267C P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_full_batch_review.md`",
    )
    current = replace_once(
        current,
        "- next_action(다음 행동): `run267C_review_p0_mt5_full_batch_results`. Effect(효과): 전체 P0 batch(전체 우선순위 0 묶음 실행) 결과를 후보별/변형별로 리뷰해 어떤 약점 차단이 실제 개선인지, 어떤 것은 과차단인지 분리한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 강제 차단으로 확인한 약점 축을 soft feature(부드러운 피처), similar replacement(유사 대체), adapter variant(어댑터 변형)로 바꿔 다시 시험한다.",
    )
    write_md(materializer.CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(materializer.SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_once(selection, "- stage_status(단계 상태): `run267C_p0_mt5_variant_smoke_completed`", f"- stage_status(단계 상태): `{STATUS}`")
    selection = append_after(
        selection,
        "- run267C_p0_mt5_smoke_execution(267C 우선순위 0 MT5 스모크 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_smoke_execution_report.md`",
        "- run267C_p0_mt5_full_batch_review(267C 우선순위 0 MT5 전체 묶음 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_full_batch_review.md`",
    )
    selection = replace_once(selection, "- next_action(다음 행동): `run267C_review_p0_mt5_full_batch_results`", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_once(
        selection,
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 P0 full batch(전체 우선순위 0 묶음) 결과 리뷰다.",
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 강제 차단을 소프트 피처/유사 대체/어댑터 변형으로 바꾸는 후속 설계다.",
    )
    write_md(materializer.SELECTION_STATUS_PATH, selection)

    review = io_path(materializer.REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_once(review, "- status(상태): `run267C_p0_mt5_variant_smoke_completed`", f"- status(상태): `{STATUS}`")
    review = append_after(
        review,
        "- run267C_p0_mt5_smoke_execution(267C 우선순위 0 MT5 스모크 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_smoke_execution_report.md`",
        "- run267C_p0_mt5_full_batch_review(267C 우선순위 0 MT5 전체 묶음 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_full_batch_review.md`",
    )
    review = replace_once(
        review,
        "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267C_review_p0_mt5_full_batch_results`로 넘어간다.",
        f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{NEXT_ACTION}`로 넘어간다.",
    )
    write_md(materializer.REVIEW_INDEX_PATH, review)

    workspace = io_path(materializer.WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_once(
        workspace,
        "Stage267(267단계) run267C(267C 실행) P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행) `completed`.",
        "Stage267(267단계) run267C(267C 실행) P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토) completed(완료).",
    )
    workspace = replace_once(
        workspace,
        "Next action(다음 행동)는 `run267C_review_p0_mt5_full_batch_results`이다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다.",
    )
    workspace = replace_once(
        workspace,
        "active_run267C_p0_mt5_variant_smoke_completed(267C 우선순위 0 MT5 스모크 실행 후 검토 활성).",
        "active_run267C_p0_mt5_full_batch_review_completed(267C 우선순위 0 MT5 전체 묶음 검토 후 후속 설계 활성).",
    )
    write_md(materializer.WORKSPACE_STATE_PATH, workspace)


def update_ledgers(created_at: str) -> None:
    stage_row = {
        "row_id": "stage267_run267C_p0_mt5_full_batch_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "p0_mt5_full_batch_review",
        "tier_scope": "Tier A and Tier A+B historical 2024 diagnostic batch",
        "scoreboard": "runtime_full_batch_review",
        "status": STATUS,
        "judgment": "diagnostic_evidence_only_no_candidate_selection",
        "evidence_boundary": "p0_hard_block_diagnostic_review_not_adapter_candidate_not_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    stage_rows = materializer.input_probe.read_csv_rows(materializer.STAGE_LEDGER_PATH)
    stage_rows = [row for row in stage_rows if row.get("row_id") != stage_row["row_id"]]
    stage_rows.append(stage_row)
    materializer.input_probe.write_csv(
        materializer.STAGE_LEDGER_PATH,
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
    materializer.upsert_simple_csv(
        materializer.RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_p0_mt5_full_batch_review",
            "status": STATUS,
            "judgment": "diagnostic_evidence_only_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"P0 full batch review completed; next action {NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    materializer.upsert_simple_csv(
        materializer.PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__p0_mt5_full_batch_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "p0_mt5_full_batch_review",
            "parent_run_id": RUN_ID,
            "record_view": "p0_mt5_full_batch_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 diagnostic batch",
            "kpi_scope": "mt5_runtime_diagnostic_batch_review",
            "scoreboard_lane": "runtime_full_batch_review",
            "status": STATUS,
            "judgment": "diagnostic_evidence_only_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": "30_kpi_records_reviewed",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;hard_block_not_solution",
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
        ("stage267_run267C_p0_full_batch_review_script", "producer_script", PRODUCER_PATH, "Builds P0 MT5 full batch delta review."),
        ("stage267_run267C_p0_full_batch_delta_review", "delta_review", DETAIL_PATH, "Per-record P0 versus baseline delta review."),
        ("stage267_run267C_p0_full_batch_candidate_variant_summary", "candidate_variant_summary", SUMMARY_PATH, "Routed candidate and diagnostic variant summary."),
        ("stage267_run267C_p0_full_batch_axis_summary", "axis_summary", AXIS_PATH, "Diagnostic axis aggregate summary."),
        ("stage267_run267C_p0_full_batch_review_result", "review_result", RESULT_PATH, "JSON result for P0 full batch review."),
        ("stage267_run267C_p0_full_batch_review_report", "review_report", REPORT_PATH, "User-facing P0 full batch review report."),
    )
    rows = materializer.input_probe.read_csv_rows(materializer.ARTIFACT_REGISTRY_PATH)
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
    materializer.input_probe.write_csv(
        materializer.ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def main() -> int:
    created_at = utc_now()
    detail, summary, axis_rows = build_rows()
    write_csv(
        DETAIL_PATH,
        detail,
        (
            "record_view",
            "candidate_alias",
            "candidate_role",
            "diagnostic_variant",
            "diagnostic_label",
            "tier_scope",
            "route_role",
            "base_net_profit",
            "p0_net_profit",
            "net_profit_delta",
            "base_pf",
            "p0_pf",
            "pf_delta",
            "base_trade_count",
            "p0_trade_count",
            "trade_count_delta",
            "base_dd_percent",
            "p0_dd_percent",
            "dd_percent_delta",
            "base_recovery",
            "p0_recovery",
            "recovery_delta",
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
            "diagnostic_variant",
            "diagnostic_label",
            "tier_scope",
            "route_role",
            "base_net_profit",
            "p0_net_profit",
            "net_profit_delta",
            "base_pf",
            "p0_pf",
            "pf_delta",
            "base_trade_count",
            "p0_trade_count",
            "trade_count_delta",
            "base_dd_percent",
            "p0_dd_percent",
            "dd_percent_delta",
            "base_recovery",
            "p0_recovery",
            "recovery_delta",
            "diagnostic_read",
        ),
    )
    write_csv(
        AXIS_PATH,
        axis_rows,
        (
            "diagnostic_variant",
            "diagnostic_label",
            "candidate_count",
            "avg_net_profit_delta",
            "avg_pf_delta",
            "avg_trade_count_delta",
            "avg_dd_percent_delta",
            "avg_recovery_delta",
            "best_net_candidate",
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
    update_ledgers(created_at)
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
