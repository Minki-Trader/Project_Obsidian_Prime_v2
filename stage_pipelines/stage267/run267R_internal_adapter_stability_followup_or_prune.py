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
    write_csv_rows,
)


STAGE_ID = "267_adapter_research__baseline_candidate_racing_protocol"
RUN_NUMBER = "run267R"
RUN_ID = "run267R_stage267_internal_adapter_stability_followup_or_prune_v1"
SOURCE_RUN_ID = "run267Q_stage267_internal_feature_order_confirmed_adapter_materialization_v1"
STATUS = "run267R_internal_adapter_stability_followup_or_prune_completed"
NEXT_ACTION = "run267S_materialize_pool_wide_orthogonal_stability_racing_matrix"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "internal_adapter_stability_followup_or_prune"
RUN267Q_REVIEW_ROOT = (
    STAGE_ROOT / "02_runs" / "run267Q" / "internal_feature_order_confirmed_adapter_review"
)

SOURCE_CANDIDATE_SUMMARY_PATH = RUN267Q_REVIEW_ROOT / "candidate_summary.csv"
SOURCE_CANDIDATE_TEST_REVIEW_PATH = RUN267Q_REVIEW_ROOT / "candidate_test_review.csv"
SOURCE_NEGATIVE_SLICE_PATH = RUN267Q_REVIEW_ROOT / "negative_slice_summary.csv"
SOURCE_CURVE_DIAGNOSTICS_PATH = RUN267Q_REVIEW_ROOT / "curve_diagnostics.csv"
SOURCE_REPRODUCTION_AUDIT_PATH = RUN267Q_REVIEW_ROOT / "source_reproduction_audit.csv"
SOURCE_REVIEW_RESULT_PATH = RUN267Q_REVIEW_ROOT / "review_result.json"
SOURCE_REPORT_PATH = REVIEWS_ROOT / "stage267_run267Q_internal_feature_order_confirmed_adapter_mt5_review.md"

PRUNE_MATRIX_PATH = RUN_ROOT / "internal_adapter_prune_matrix.csv"
NEXT_QUEUE_PATH = RUN_ROOT / "next_pool_wide_stability_queue.csv"
GATE_RECEIPT_PATH = RUN_ROOT / "gate_receipt.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
RESULT_PATH = RUN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267R_internal_adapter_stability_followup_or_prune.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267R_internal_adapter_stability_followup_or_prune.py")

STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

BASELINE_POOL = (
    "s264_allow_inner_high_quarter",
    "s264_lowrank_control",
    "s262_lowrank_inner_half_filter",
    "s264_allow_inner_all_oos_anchor",
    "s258_short_tight_control",
)

STAGE_LEDGER_COLUMNS = (
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
)

ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return value


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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_current_action_block(text: str) -> str:
    text = replace_line_prefix(
        text,
        "- next_run(다음 실행):",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    text = replace_line_prefix(
        text,
        "- action(행동):",
        "- action(행동): run267R(267R 실행)는 run267Q(267Q 실행)의 내부 Adapter(어댑터) 재현 결과와 약한 구간을 비교해 이 분기를 가지치기했다.",
    )
    text = replace_line_prefix(
        text,
        "- effect(효과):",
        "- effect(효과): 변형 차이가 접힌 내부 Adapter(어댑터)를 더 미세 수리하지 않고, 다섯 Baseline candidates(기준 후보) 전체의 넓은 안정성 경주로 되돌린다.",
    )
    text = replace_line_prefix(
        text,
        "- next_action(다음 행동):",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    return text


def worst_slice(
    negative_rows: Sequence[Mapping[str, str]],
    candidate_alias: str,
    axis: str,
    bucket: str,
) -> dict[str, str]:
    rows = [
        row
        for row in negative_rows
        if row.get("candidate_alias") == candidate_alias
        and row.get("axis") == axis
        and row.get("bucket") == bucket
    ]
    if not rows:
        return {}
    return min(rows, key=lambda row: as_float(row.get("net_profit")))


def source_shape_key(row: Mapping[str, str]) -> tuple[str, str]:
    return (str(row.get("candidate_alias", "")), str(row.get("test_id", "")))


def build_prune_matrix(
    summary_rows: Sequence[Mapping[str, str]],
    test_rows: Sequence[Mapping[str, str]],
    negative_rows: Sequence[Mapping[str, str]],
    reproduction_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    test_by_candidate: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in test_rows:
        test_by_candidate[str(row.get("candidate_alias"))].append(row)

    reproduction_mismatches = sum(1 for row in reproduction_rows if row.get("reproduction_status") != "matched")
    rows: list[dict[str, Any]] = []
    for summary in summary_rows:
        alias = str(summary.get("candidate_alias", ""))
        tests = test_by_candidate.get(alias, [])
        monday = worst_slice(negative_rows, alias, "weekday", "Monday")
        session = worst_slice(negative_rows, alias, "session_report", "session_07_12_report_time")
        month = min(
            (row for row in negative_rows if row.get("candidate_alias") == alias and row.get("axis") == "month"),
            key=lambda row: as_float(row.get("net_profit")),
            default={},
        )
        variant_collapse = as_int(summary.get("unique_kpi_shapes")) <= 1
        monday_net = as_float(monday.get("net_profit"), 0.0)
        session_net = as_float(session.get("net_profit"), 0.0)
        weak_slice_flag = monday_net < -80.0 or session_net < -80.0
        decision = "prune_internal_adapter_branch_to_salvage_clue"
        if not variant_collapse and not weak_slice_flag and reproduction_mismatches == 0:
            decision = "allow_one_followup_only"
        rows.append(
            {
                "candidate_alias": alias,
                "candidate_id": summary.get("candidate_id"),
                "candidate_role": summary.get("candidate_role"),
                "review_rows": as_int(summary.get("review_rows")),
                "unique_kpi_shapes": as_int(summary.get("unique_kpi_shapes")),
                "all_reproduced_from_source": summary.get("all_reproduced_from_source"),
                "best_net_profit": as_float(summary.get("best_net_profit")),
                "best_profit_factor": as_float(summary.get("best_profit_factor")),
                "worst_dd_percent": as_float(summary.get("worst_dd_percent")),
                "trade_count_min": min((as_int(row.get("trade_count")) for row in tests), default=0),
                "negative_slice_rows": sum(1 for row in negative_rows if row.get("candidate_alias") == alias),
                "worst_month": month.get("bucket", ""),
                "worst_month_net": as_float(month.get("net_profit"), 0.0),
                "monday_net": monday_net,
                "monday_trade_count": as_int(monday.get("trade_count")),
                "session_07_12_net": session_net,
                "session_07_12_trade_count": as_int(session.get("trade_count")),
                "variant_collapse": variant_collapse,
                "weak_slice_recurred": weak_slice_flag,
                "source_reproduction_mismatches": reproduction_mismatches,
                "decision": decision,
                "reason": (
                    "runtime_reproduced_but_ablation_and_replacement_have_same_shape_and_weak_slices_remain"
                    if decision.startswith("prune")
                    else "followup_allowed_but_not_selected_candidate"
                ),
                "salvage_value": "keep_internal_feature_order_materialization_as_runtime_reproduction_seed",
                "do_not_repeat": "do_not_tune_single_monday_or_session_threshold_without_pool_wide_axis",
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return rows


def build_next_queue() -> list[dict[str, Any]]:
    pool = ";".join(BASELINE_POOL)
    common_controls = (
        "US100;M5;historical_2024;fixed_cost_deposit_tester_contract;"
        "same_candidate_pool;same_no_onnx_claim_boundary"
    )
    return [
        {
            "queue_id": "run267S_axis01_pool_wide_variant_distinguishability",
            "priority": "P0",
            "candidate_scope": pool,
            "hypothesis": "좋은 후보라면 feature ablation(피처 제거)과 similar replacement(유사 대체)가 모두 같은 모양으로 접히지 않아야 한다.",
            "decision_use": "내부 Adapter(어댑터) 분기를 살릴지, 후보군 전체에서 새 축으로 갈지 정한다.",
            "comparison_baseline": "run267N(267N 실행) pool-wide P0 surface(후보군 전체 P0 표면)와 run267Q(267Q 실행) internal reproduction(내부 재현)",
            "control_variables": common_controls,
            "changed_variables": "ablation/replacement axis identity(제거/대체 축 정체성), candidate-wide materialization(후보군 전체 물질화)",
            "sample_scope": "Tier A(티어 A) and actual routed total(실제 라우팅 전체) historical 2024 stress(2024 과거 압박)",
            "success_criteria": "각 후보의 변형별 curve/time-slice/trade-quality(곡선/시간구간/거래품질)가 구분되고, 약한 구간이 악화되지 않는다.",
            "failure_criteria": "모든 변형이 같은 KPI(핵심 성과 지표) 모양으로 접히거나 Monday/session(월요일/세션) 손실이 반복된다.",
            "invalid_conditions": "feature order(피처 순서), set/ini identity(설정/초기화 정체성), parser(파서) 불일치가 있으면 무효다.",
            "stop_conditions": "같은 약한 구간을 한 분기에서 두 번 넘게 수리하지 않는다.",
            "evidence_plan": "candidate_test_review;negative_slice_summary;curve_diagnostics;source_reproduction_audit;artifact_registry",
        },
        {
            "queue_id": "run267S_axis02_non_calendar_weak_slice_resilience",
            "priority": "P0",
            "candidate_scope": pool,
            "hypothesis": "약한 요일/세션을 직접 막는 대신, 비달력 구조 feature(피처)가 약한 구간 손실을 덜 흔들리게 해야 한다.",
            "decision_use": "single-slice repair(단일 구간 수리) 병목을 피하고 넓은 안정성 축을 고른다.",
            "comparison_baseline": "run267Q(267Q 실행)의 Monday/session(월요일/세션) 손실",
            "control_variables": common_controls,
            "changed_variables": "volatility regime(변동성 상태), ATR compression(ATR 압축), trend strength(추세 강도) 구조 feature(피처)",
            "sample_scope": "2024 historical stress(2024 과거 압박) with weekday/session/hour/month(요일/세션/시간/월) KPI(핵심 성과 지표)",
            "success_criteria": "전체 net/PF/DD(순수익/수익 팩터/손실폭)를 크게 훼손하지 않고 약한 구간 손실이 줄어든다.",
            "failure_criteria": "특정 요일 또는 특정 시간만 맞추고 trade count(거래 수)가 무너지거나 다른 월이 깊게 파인다.",
            "invalid_conditions": "요일 자체를 학습 target(목표)로 과최적화하면 무효다.",
            "stop_conditions": "Monday/session(월요일/세션) 전용 threshold(문턱값) 반복은 중단한다.",
            "evidence_plan": "time_slice_kpi;trade_records;curve_zoom_review;failure_memory",
        },
        {
            "queue_id": "run267S_axis03_candidate_pool_prune_or_restore",
            "priority": "P1",
            "candidate_scope": pool,
            "hypothesis": "run267Q(267Q 실행)에서 빠진 세 후보도 동일한 안정성 축에서는 다시 비교 가치가 있을 수 있다.",
            "decision_use": "다섯 후보 유지/탈락/회수 조건을 업데이트한다.",
            "comparison_baseline": "Stage267(267단계) initial scoreboard(초기 점수판), run267B(267B 실행), run267O(267O 실행)",
            "control_variables": common_controls,
            "changed_variables": "candidate inclusion(후보 포함), stress/control role(압박/통제 역할)",
            "sample_scope": "all five Baseline candidates(다섯 기준 후보) under same route interpretation(같은 라우팅 해석)",
            "success_criteria": "각 후보가 다음 연구에 왜 남는지 또는 왜 탈락하는지 근거가 생긴다.",
            "failure_criteria": "두 후보만 반복 수리하고 나머지 후보군의 역할 판정이 비어 있다.",
            "invalid_conditions": "서로 다른 기간 또는 서로 다른 tester contract(테스터 계약)를 같은 비교처럼 쓰면 무효다.",
            "stop_conditions": "탈락 근거가 생긴 후보는 감정적으로 유지하지 않는다.",
            "evidence_plan": "pool_candidate_decision;candidate_role_update;negative_result_register_delta",
        },
    ]


def build_gate_receipts() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "experiment_design",
            "gate_status": "passed",
            "evidence": rel(NEXT_QUEUE_PATH),
            "effect": "hypothesis, comparison, controls, stop conditions, evidence plan are explicit",
        },
        {
            "gate_id": "data_integrity",
            "gate_status": "bounded",
            "evidence": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267R uses 2024 MT5 results as review evidence only, not training target",
        },
        {
            "gate_id": "model_validation",
            "gate_status": "bounded",
            "evidence": rel(PRUNE_MATRIX_PATH),
            "effect": "variant collapse prevents model or candidate selection claim",
        },
        {
            "gate_id": "result_judgment",
            "gate_status": "passed",
            "evidence": rel(REPORT_PATH),
            "effect": "selected candidate and ONNX readiness remain not claimed",
        },
        {
            "gate_id": "artifact_lineage",
            "gate_status": "passed",
            "evidence": rel(LINEAGE_PATH),
            "effect": "source review artifacts connect to run267R outputs",
        },
    ]


def build_failure_memory(prune_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in prune_rows:
        rows.append(
            {
                "candidate_alias": row["candidate_alias"],
                "candidate_id": row["candidate_id"],
                "failed_boundary": "internal_adapter_branch_candidate_selection",
                "why_failed": row["reason"],
                "weak_slice_evidence": f"Monday={row['monday_net']};session_07_12={row['session_07_12_net']}",
                "salvage_value": row["salvage_value"],
                "reopen_condition": "only_reopen_if_pool_wide_axis_creates_distinct_stable_shape",
                "do_not_repeat": row["do_not_repeat"],
            }
        )
    return rows


def build_report(result: Mapping[str, Any]) -> str:
    prune_rows = result["prune_matrix"]
    queue_rows = result["next_queue"]
    lines = [
        "# Stage267 Run267R Internal Adapter Stability Follow-up or Prune(267단계 267R 내부 어댑터 안정성 후속 또는 가지치기)",
        "",
        "- action(행동): run267Q(267Q 실행)의 내부 Adapter(어댑터) 재현 결과를 follow-up/prune(후속/가지치기) 기준으로 재판정했다.",
        "- effect(효과): 재현 성공은 보존하지만, 변형 차이 collapse(접힘)와 weak slices(약한 구간) 반복 때문에 이 분기를 후보 선택으로 밀지 않는다.",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- prune_rows(가지치기 행): `{len(prune_rows)}`",
        f"- next_queue_rows(다음 큐 행): `{len(queue_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267Q(267Q 실행)는 나쁜 실행이 아니었다. MT5(MetaTrader 5, 메타트레이더5)에서 run267N(267N 실행)의 표면을 재현했고, parser(파서)와 source reproduction(원천 재현)도 깨지지 않았다.",
        "하지만 좋은 후보가 되려면 비슷한 feature(피처)를 제거하거나 대체했을 때 다른 정보가 드러나야 한다. 이번에는 `abl_volatility_bandwidth`와 `rep_volatility_atr`, 그리고 Tier A(티어 A)와 routed total(라우팅 전체)이 후보별로 같은 모양으로 접혔다.",
        "또 Monday(월요일)과 session_07_12(7-12시 세션) 손실이 반복됐다. 그래서 이 branch(분기)는 salvage clue(회수 단서)로 보존하고, 다음은 다섯 후보 전체의 orthogonal stability racing(직교 안정성 경주)으로 돌린다.",
        "",
        "## Prune Matrix(가지치기 행렬)",
        "",
        "| candidate(후보) | best net(최고 순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | Monday net(월요일 순수익) | session net(세션 순수익) | decision(판정) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in prune_rows:
        lines.append(
            "| `{candidate_alias}` | {best_net_profit:.2f} | {best_profit_factor:.6f} | {worst_dd_percent:.2f} | {trade_count_min} | {monday_net:.2f} | {session_07_12_net:.2f} | `{decision}` |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Next Queue(다음 큐)",
            "",
            "| queue(큐) | priority(우선순위) | hypothesis(가설) | effect(효과) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | {row['hypothesis']} | {row['decision_use']} |"
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_judgment(결과 판정): `exploratory_prune_to_salvage_no_candidate_selection`.",
            "- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.",
            "- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- next_queue(다음 큐): `{rel(NEXT_QUEUE_PATH)}`",
            f"- gate_receipt(게이트 기록): `{rel(GATE_RECEIPT_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- result(결과): `{rel(RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267R_prune_script", "producer_script", PRODUCER_PATH, "Builds run267R internal Adapter follow-up/prune decision."),
        ("stage267_run267R_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Run267R internal Adapter prune/follow-up matrix."),
        ("stage267_run267R_next_queue", "next_queue", NEXT_QUEUE_PATH, "Run267R next pool-wide stability racing queue."),
        ("stage267_run267R_gate_receipt", "gate_receipt", GATE_RECEIPT_PATH, "Run267R required gate receipt."),
        ("stage267_run267R_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267R failure memory for internal Adapter branch."),
        ("stage267_run267R_lineage", "lineage", LINEAGE_PATH, "Run267R artifact lineage."),
        ("stage267_run267R_result", "result", RESULT_PATH, "Run267R result payload."),
        ("stage267_run267R_report", "review_report", REPORT_PATH, "Run267R user-facing report."),
    )
    rows = []
    for artifact_id, artifact_type, path, notes in entries:
        rows.append(
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
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    report = rel(REPORT_PATH)
    primary_kpi = f"prune_rows={len(result['prune_matrix'])};next_queue_rows={len(result['next_queue'])}"
    guardrail = "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed"
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267R_internal_adapter_stability_followup_or_prune",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "internal_adapter_stability_followup_or_prune",
                "tier_scope": "Tier A and actual routed total historical 2024 internal Adapter review",
                "scoreboard": "experiment_design_result_judgment",
                "status": STATUS,
                "judgment": "exploratory_prune_to_salvage_no_candidate_selection",
                "evidence_boundary": "design_and_prune_receipt_only_no_candidate_selection_no_onnx",
                "report_path": report,
                "notes": f"{primary_kpi};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__internal_adapter_stability_followup_or_prune",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "internal_adapter_stability_followup_or_prune",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "internal_adapter_stability_followup_or_prune",
                "tier_scope": "Tier A and actual routed total historical 2024 internal Adapter review",
                "kpi_scope": "prune_matrix_next_stability_queue",
                "scoreboard_lane": "experiment_design_result_judgment",
                "status": STATUS,
                "judgment": "exploratory_prune_to_salvage_no_candidate_selection",
                "path": report,
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "external_verification_status": "not_applicable_design_consumes_completed_mt5_review",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": SOURCE_RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "internal_feature_order_confirmed_adapter_mt5_review",
                "status": "run267Q_internal_feature_order_confirmed_adapter_mt5_review_completed",
                "judgment": "diagnostic_review_completed_no_candidate_selection",
                "path": rel(SOURCE_REPORT_PATH),
                "notes": "Run267Q review completed; selected_candidate=none; onnx_readiness=not_claimed; next_action=run267R_design_internal_adapter_stability_followup_or_prune.",
            },
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "internal_adapter_stability_followup_or_prune",
                "status": STATUS,
                "judgment": "exploratory_prune_to_salvage_no_candidate_selection",
                "path": report,
                "notes": f"Run267R prunes internal Adapter branch to salvage clue; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
            },
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(str(result["created_at_utc"])),
        key="artifact_id",
    )


def update_current_docs() -> None:
    report_path = rel(REPORT_PATH)
    run_line = f"- run267R_internal_adapter_stability_followup_or_prune(267R 내부 어댑터 안정성 후속/가지치기): `{report_path}`"
    latest_line = f"- latest_design(최신 설계): run267R(267R 실행) internal Adapter follow-up/prune(내부 어댑터 후속/가지치기) report(보고서) `{report_path}`."

    text = read_text(CURRENT_WORKING_STATE_PATH)
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `internal_adapter_branch_pruned_to_salvage`")
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    text = append_after_contains(text, "stage267_run267Q_internal_feature_order_confirmed_adapter_mt5_review.md", run_line)
    text = append_after_contains(text, "## Current Next Action", latest_line)
    text = replace_current_action_block(text)
    write_md(CURRENT_WORKING_STATE_PATH, text)

    for path in (SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        doc = read_text(path)
        if path == SELECTION_STATUS_PATH:
            doc = replace_line_prefix(doc, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        else:
            doc = replace_line_prefix(doc, "- status(상태):", f"- status(상태): `{STATUS}`")
        doc = replace_line_prefix(doc, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        doc = replace_line_prefix(doc, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        doc = append_after_contains(doc, "run267Q_internal_feature_order_confirmed_adapter_mt5_review", run_line)
        doc = replace_line_prefix(doc, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        write_md(path, doc)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = workspace.replace(f"current_run_id: {SOURCE_RUN_ID}", f"current_run_id: {RUN_ID}", 1)
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267R(267R 실행) internal Adapter follow-up/prune(내부 어댑터 후속/가지치기) `{STATUS}`. Effect(효과): run267Q(267Q 실행)의 MT5(MetaTrader 5, 메타트레이더5) 재현 성공은 보존하되 변형 차이 collapse(접힘)와 Monday/session(월요일/세션) 약점 때문에 내부 Adapter(어댑터) 단독 분기는 salvage clue(회수 단서)로 가지치기하고 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line + "\n", 1)
    workspace = workspace.replace(
        "  status: run267Q_internal_feature_order_confirmed_adapter_mt5_review_completed",
        f"  status: {STATUS}",
        1,
    )
    workspace = workspace.replace(
        f"  current_run_id: {SOURCE_RUN_ID}",
        f"  current_run_id: {RUN_ID}",
        1,
    )
    workspace = workspace.replace(
        f"  last_completed_run_id: {SOURCE_RUN_ID}",
        f"  last_completed_run_id: {RUN_ID}",
        1,
    )
    workspace = append_after_contains(
        workspace,
        "run267Q_internal_feature_order_confirmed_adapter_mt5_review_path",
        f"  run267R_internal_adapter_stability_followup_or_prune_path: {report_path}",
    )
    workspace_lines = workspace.splitlines()
    for index, line in enumerate(workspace_lines):
        if line.strip().startswith("Next action(다음 행동)는 `run267R_design_internal_adapter_stability_followup_or_prune`"):
            workspace_lines[index] = (
                f"  Next action(다음 행동)는 `{NEXT_ACTION}`이다. "
                "Effect(효과): run267R(267R 실행)의 가지치기 결과를 받아 다섯 Baseline candidates(기준 후보) "
                "전체의 orthogonal stability racing(직교 안정성 경주)을 물질화한다."
            )
            break
    workspace = "\n".join(workspace_lines) + ("\n" if workspace.endswith("\n") else "")
    workspace = workspace.replace(
        "  next_action: run267R_design_internal_adapter_stability_followup_or_prune",
        f"  next_action: {NEXT_ACTION}",
        1,
    )
    workspace = workspace.replace(
        "is active_run267Q_internal_feature_order_confirmed_adapter_mt5_review_completed(267Q 내부 피처 순서 확인 어댑터 MT5 검토 완료, 후속/가지치기 설계 대기 활성).",
        "is active_run267R_internal_adapter_stability_followup_or_prune_completed(267R 내부 어댑터 안정성 후속/가지치기 완료, 후보군 전체 안정성 경주 물질화 대기 활성).",
        1,
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    for source in (
        SOURCE_CANDIDATE_SUMMARY_PATH,
        SOURCE_CANDIDATE_TEST_REVIEW_PATH,
        SOURCE_NEGATIVE_SLICE_PATH,
        SOURCE_CURVE_DIAGNOSTICS_PATH,
        SOURCE_REPRODUCTION_AUDIT_PATH,
        SOURCE_REVIEW_RESULT_PATH,
    ):
        if not path_exists(source):
            raise FileNotFoundError(source)

    summary_rows = read_csv_rows(SOURCE_CANDIDATE_SUMMARY_PATH)
    test_rows = read_csv_rows(SOURCE_CANDIDATE_TEST_REVIEW_PATH)
    negative_rows = read_csv_rows(SOURCE_NEGATIVE_SLICE_PATH)
    reproduction_rows = read_csv_rows(SOURCE_REPRODUCTION_AUDIT_PATH)
    review_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    prune_matrix = build_prune_matrix(summary_rows, test_rows, negative_rows, reproduction_rows)
    next_queue = build_next_queue()
    gate_receipt = build_gate_receipts()
    failure_memory = build_failure_memory(prune_matrix)
    lineage = {
        "producer": rel(PRODUCER_PATH),
        "source_run_id": SOURCE_RUN_ID,
        "source_inputs": [
            rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH),
            rel(SOURCE_NEGATIVE_SLICE_PATH),
            rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
            rel(SOURCE_REPRODUCTION_AUDIT_PATH),
            rel(SOURCE_REVIEW_RESULT_PATH),
            rel(SOURCE_REPORT_PATH),
        ],
        "outputs": {
            "prune_matrix": rel(PRUNE_MATRIX_PATH),
            "next_queue": rel(NEXT_QUEUE_PATH),
            "gate_receipt": rel(GATE_RECEIPT_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "lineage_judgment": "connected_prune_receipt_no_candidate_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return {
        "created_at_utc": utc_now(),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "source_review_status": review_result.get("status"),
        "prune_matrix": prune_matrix,
        "next_queue": next_queue,
        "gate_receipt": gate_receipt,
        "failure_memory": failure_memory,
        "lineage": lineage,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        PRUNE_MATRIX_PATH,
        result["prune_matrix"],
        (
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "review_rows",
            "unique_kpi_shapes",
            "all_reproduced_from_source",
            "best_net_profit",
            "best_profit_factor",
            "worst_dd_percent",
            "trade_count_min",
            "negative_slice_rows",
            "worst_month",
            "worst_month_net",
            "monday_net",
            "monday_trade_count",
            "session_07_12_net",
            "session_07_12_trade_count",
            "variant_collapse",
            "weak_slice_recurred",
            "source_reproduction_mismatches",
            "decision",
            "reason",
            "salvage_value",
            "do_not_repeat",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        NEXT_QUEUE_PATH,
        result["next_queue"],
        (
            "queue_id",
            "priority",
            "candidate_scope",
            "hypothesis",
            "decision_use",
            "comparison_baseline",
            "control_variables",
            "changed_variables",
            "sample_scope",
            "success_criteria",
            "failure_criteria",
            "invalid_conditions",
            "stop_conditions",
            "evidence_plan",
        ),
    )
    write_csv(GATE_RECEIPT_PATH, result["gate_receipt"], ("gate_id", "gate_status", "evidence", "effect"))
    write_csv(
        FAILURE_MEMORY_PATH,
        result["failure_memory"],
        (
            "candidate_alias",
            "candidate_id",
            "failed_boundary",
            "why_failed",
            "weak_slice_evidence",
            "salvage_value",
            "reopen_condition",
            "do_not_repeat",
        ),
    )
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, build_report(result))


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_current_docs()
    print(
        json.dumps(
            {
                "status": STATUS,
                "prune_rows": len(result["prune_matrix"]),
                "next_queue_rows": len(result["next_queue"]),
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
