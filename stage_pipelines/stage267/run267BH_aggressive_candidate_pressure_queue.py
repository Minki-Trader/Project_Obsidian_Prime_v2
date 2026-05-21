from __future__ import annotations

import csv
import json
import sys
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
from stage_pipelines.stage267 import run267BG_adjacent_period_replacement_fresh_report_mt5_executor as previous


STAGE_ID = previous.STAGE_ID
RUN_NUMBER = "run267BH"
RUN_ID = "run267BH_stage267_aggressive_candidate_pressure_queue_v1"
PARENT_RUN_ID = previous.RUN_ID
CLAIM_BOUNDARY = previous.CLAIM_BOUNDARY

STAGE_ROOT = previous.STAGE_ROOT
REVIEWS_ROOT = previous.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_candidate_pressure_queue"

QUEUE_PATH = RUN_ROOT / "aggressive_experiment_queue.csv"
DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
FAILURE_MEMORY_SEED_PATH = RUN_ROOT / "failure_memory_seed.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BH_aggressive_candidate_pressure_queue.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BH_aggressive_candidate_pressure_queue.py")

STAGE_LEDGER_PATH = previous.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = previous.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = previous.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = previous.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = previous.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = previous.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = previous.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = previous.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = previous.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = previous.ARTIFACT_COLUMNS

STATUS = "run267BH_aggressive_candidate_pressure_queue_materialized_execution_pending"
NEXT_ACTION = "run267BI_repair_tester_handoff_and_execute_aggressive_pressure_queue_tranche"


CANDIDATES = [
    {
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "role": "core_challenger",
        "aggressive_angle": "push the current challenger into wider opportunity and higher payoff pressure",
    },
    {
        "candidate_id": "s264_lowrank_control",
        "candidate_alias": "s264_lc",
        "role": "defensive_control",
        "aggressive_angle": "stress the control by removing comfort filters and measuring how quickly it breaks",
    },
    {
        "candidate_id": "s262_lowrank_inner_half_filter",
        "candidate_alias": "s262_lih",
        "role": "validation_heavy",
        "aggressive_angle": "force validation-heavy logic into broader OOS pressure without stacking filters",
    },
    {
        "candidate_id": "s264_allow_inner_all_oos_anchor",
        "candidate_alias": "s264_aia",
        "role": "oos_anchor",
        "aggressive_angle": "turn OOS recovery into a higher-conviction expansion branch while exposing validation damage",
    },
    {
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "role": "stress_challenger",
        "aggressive_angle": "test whether strong OOS numbers survive larger payoff/risk pressure instead of defensive trimming",
    },
]

VARIANTS = [
    {
        "variant_id": "explode_opportunity_recall",
        "hypothesis": "A wider permission surface can reveal a stronger raw edge before defensive filters hide it.",
        "changed_variables": "loosen entry permission, reduce micro-filter stacking, keep calendar guards off unless required for invalidity",
        "extreme_sweep": "decision permission widened by coarse bands; trade-count target pushed upward before any fine threshold search",
        "success_criteria": "trade count expands materially while PF, drawdown, and curve holes remain reviewable across 2024 and adjacent OOS periods",
        "failure_criteria": "trade count rises but PF collapses, drawdown expands sharply, or one month/session carries the whole result",
    },
    {
        "variant_id": "payoff_convexity_push",
        "hypothesis": "Some candidates may need asymmetric payoff expansion rather than more entry filtering.",
        "changed_variables": "ATR risk/reward shape, TP/SL stretch, hold window pressure, no extra feature filter",
        "extreme_sweep": "coarse TP stretch and SL compression/expansion corners to expose convexity cliffs",
        "success_criteria": "expectancy and recovery improve without hiding a deep equity valley in weak months",
        "failure_criteria": "net profit improves only through a few outsized trades or DD becomes uncomfortable",
    },
    {
        "variant_id": "state_acceleration_interaction",
        "hypothesis": "Explosive moves may be captured by interaction features rather than single ADX/ATR replacement.",
        "changed_variables": "new volatility shock x trend acceleration and return impulse interaction features",
        "extreme_sweep": "raw interaction, clipped interaction, and rank-bucket interaction surfaces",
        "success_criteria": "similar market meaning survives feature replacement and does not depend on one indicator column",
        "failure_criteria": "performance disappears when the interaction is clipped or replaced with a similar state axis",
    },
    {
        "variant_id": "anti_overconstraint_prune",
        "hypothesis": "Recent branches may be overconstrained by defensive repair habits; pruning filters can expose a better candidate family.",
        "changed_variables": "remove one defensive guard family at a time and keep risk/reporting fixed",
        "extreme_sweep": "no calendar guard, no weak-slice micro repair, and single-state guard only",
        "success_criteria": "curve becomes simpler or trade quality improves without relying on a narrow day/session filter",
        "failure_criteria": "all gains came from the removed guard blocking bad trades and the unfiltered candidate breaks broadly",
    },
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered or ("status", "notes"))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in fieldnames})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    inserted = False
    for line in lines:
        out.append(line)
        if line == "current_focus:" and not inserted:
            out.extend(focus_block.rstrip().splitlines())
            inserted = True
    if not inserted:
        out.extend(["current_focus:", *focus_block.rstrip().splitlines()])
    return "\n".join(out) + "\n"


def build_queue() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    order = 1
    for candidate in CANDIDATES:
        for variant in VARIANTS:
            rows.append(
                {
                    "queue_order": order,
                    "queue_id": f"run267BH_{order:02d}_{candidate['candidate_alias']}_{variant['variant_id']}",
                    "candidate_id": candidate["candidate_id"],
                    "candidate_alias": candidate["candidate_alias"],
                    "candidate_role": candidate["role"],
                    "variant_id": variant["variant_id"],
                    "experiment_class": "aggressive_pressure_not_filter_stack",
                    "hypothesis": variant["hypothesis"],
                    "decision_use": "decide whether this candidate deserves materialization as an aggressive branch, not selection",
                    "comparison_baseline": "Stage267 baseline candidate pool plus run267N/run267O/run267AP/run267AQ/run267AX/run267AY evidence",
                    "control_variables": "symbol=US100; timeframe=M5; broker=FPMarkets; reporting includes 2024, adjacent OOS, curve, time-slice, trade quality",
                    "changed_variables": variant["changed_variables"],
                    "sample_scope": "Tier A first; Tier B and actual routed total remain blocked until true fallback route manifest exists",
                    "broad_sweep": candidate["aggressive_angle"],
                    "extreme_sweep": variant["extreme_sweep"],
                    "success_criteria": variant["success_criteria"],
                    "failure_criteria": variant["failure_criteria"],
                    "invalid_conditions": "tester start missing, report missing, runtime CSV missing, feature order drift, stale report/profile handoff",
                    "stop_conditions": "stop after one materialization plus one review if the branch only repeats defensive filtering or breaks all weak slices",
                    "evidence_plan": "materialize feature/model/set/ini, run MT5 Strategy Tester, parse report/trades, inspect curve/time-slice/trade quality, record failures",
                    "claim_boundary": "research_queue_only_no_candidate_selection_no_onnx",
                }
            )
            order += 1
    return rows


def build_design_receipt(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "field": "hypothesis",
            "value": "Aggressive pressure can expose a stronger research package than repeated defensive repair.",
            "effect": "방어 필터를 계속 덧붙이는 loop(반복)를 끊고 후보별 강한 방향을 먼저 시험한다.",
        },
        {
            "field": "decision_use",
            "value": "materialization priority only",
            "effect": "좋아 보인다는 이유로 selected candidate(선택 후보)나 ONNX(오닉스) 검토를 주장하지 않는다.",
        },
        {
            "field": "queue_size",
            "value": str(len(queue_rows)),
            "effect": "다섯 후보를 모두 aggressive(공격형) 축에 올려 한 후보 미세 수리 병목을 줄인다.",
        },
        {
            "field": "invalid_conditions",
            "value": "tester/report/runtime/file-order drift",
            "effect": "MT5(MetaTrader 5, 메타트레이더5) 인계 실패를 성능 실패로 오해하지 않는다.",
        },
    ]


def build_failure_memory_seed(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        rows.append(
            {
                "queue_id": row["queue_id"],
                "candidate_alias": row["candidate_alias"],
                "variant_id": row["variant_id"],
                "failed_boundary": "not_yet_run",
                "why_failed": "not_applicable_until_mt5_execution",
                "salvage_value": "records an aggressive alternative to defensive filter stacking",
                "reopen_condition": "materialize and run after tester handoff repair; keep if curve/trade quality teaches something even when KPI is weak",
                "do_not_repeat_note": "do not convert this into a narrow one-threshold micro repair without broad-sweep evidence",
            }
        )
    return rows


def build_judgment() -> list[dict[str, Any]]:
    return [
        {"field": "run_status", "value": STATUS, "judgment": "queue_materialized_execution_pending"},
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed"},
        {"field": "next_action", "value": NEXT_ACTION, "judgment": "repair_handoff_then_execute_aggressive_tranche"},
    ]


def build_manifest(created_at: str, queue_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "created_at_utc": created_at,
        "queue_count": len(queue_rows),
        "candidate_count": len(CANDIDATES),
        "variant_count_per_candidate": len(VARIANTS),
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def build_lineage(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "sources": {
            "previous_blocked_runtime_probe": previous.rel(previous.REPORT_PATH),
            "current_working_state": previous.rel(CURRENT_WORKING_STATE_PATH),
            "selection_status": previous.rel(SELECTION_STATUS_PATH),
        },
        "outputs": {
            "queue": rel(QUEUE_PATH),
            "experiment_design_receipt": rel(DESIGN_RECEIPT_PATH),
            "failure_memory_seed": rel(FAILURE_MEMORY_SEED_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "report": rel(REPORT_PATH),
        },
        "run_manifest": manifest,
        "lineage_judgment": "connected_with_boundary",
    }


def report_markdown(queue_rows: Sequence[Mapping[str, Any]], manifest: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 run267BH Aggressive Candidate Pressure Queue(공격형 후보 압박 큐)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- queue_rows(큐 행): `{len(queue_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): 다섯 Baseline candidates(기준 후보)를 aggressive pressure(공격형 압박) 축에 다시 올렸다.",
        "Effect(효과): defensive filter stacking(방어 필터 덧붙이기)만 반복하지 않고, 넓은 permission(허용), payoff convexity(손익 비대칭), interaction feature(상호작용 피처), overconstraint prune(과제약 가지치기)을 실제 다음 실행 큐로 만든다.",
        "",
        "## Queue Shape(큐 구조)",
        "",
        "| variant(변형) | rows(행 수) | intent(의도) |",
        "| --- | ---: | --- |",
    ]
    for variant in VARIANTS:
        count = sum(1 for row in queue_rows if row["variant_id"] == variant["variant_id"])
        lines.append(f"| `{variant['variant_id']}` | {count} | {variant['hypothesis']} |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 큐는 materialization priority(물질화 우선순위)일 뿐 selected candidate(선택 후보)가 아니다.",
            "- MT5(MetaTrader 5, 메타트레이더5) tester handoff(테스터 인계)가 막히면 invalid/blocked(무효/차단)로 기록하고 성능으로 해석하지 않는다.",
            "- true fallback(실제 대체)과 actual routed total(실제 라우팅 전체)은 route manifest(라우트 목록)가 생기기 전까지 차단 상태다.",
            "- 다음 실행은 한 번에 미세조정하지 않고, coarse aggressive tranche(거친 공격형 묶음)부터 본다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- queue(큐): `{rel(QUEUE_PATH)}`",
            f"- design receipt(설계 영수증): `{rel(DESIGN_RECEIPT_PATH)}`",
            f"- failure memory seed(실패 기억 씨앗): `{rel(FAILURE_MEMORY_SEED_PATH)}`",
            f"- manifest(목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- next_action(다음 행동): `{manifest['next_action']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BH_producer", "producer_script", PRODUCER_PATH, "Builds aggressive candidate pressure queue."),
        ("stage267_run267BH_queue", "experiment_queue", QUEUE_PATH, "Aggressive pressure queue."),
        ("stage267_run267BH_design_receipt", "experiment_design_receipt", DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267BH_failure_memory_seed", "failure_memory_seed", FAILURE_MEMORY_SEED_PATH, "Failure memory seed."),
        ("stage267_run267BH_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Judgment boundary."),
        ("stage267_run267BH_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267BH_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267BH_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    return [
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


def update_ledgers(created_at: str, queue_rows: Sequence[Mapping[str, Any]]) -> None:
    stage_row = {
        "row_id": "stage267_run267BH_aggressive_candidate_pressure_queue",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "aggressive_candidate_pressure_queue",
        "tier_scope": "Tier A first; Tier B and actual routed total blocked until route manifest exists",
        "scoreboard": "aggressive_research_queue",
        "status": STATUS,
        "judgment": "execution_pending_no_candidate_selection",
        "evidence_boundary": "research_queue_only_no_onnx_no_operating_claim",
        "report_path": rel(REPORT_PATH),
        "notes": f"queue_rows={len(queue_rows)}; next_action={NEXT_ACTION}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "aggressive_candidate_pressure_queue",
        "status": STATUS,
        "judgment": "execution_pending_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "notes": f"queue_rows={len(queue_rows)}; selected_candidate=none; onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__aggressive_candidate_pressure_queue",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggressive_candidate_pressure_queue",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "aggressive_candidate_pressure_queue",
        "tier_scope": "Tier A first; true fallback blocked",
        "kpi_scope": "design_queue_no_kpi",
        "scoreboard_lane": "aggressive_research_queue",
        "status": STATUS,
        "judgment": "execution_pending_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={len(queue_rows)}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "not_applicable_design_queue",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = artifact_rows(created_at)
    replacement_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement_ids]
    merged.extend(new_rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def update_docs(queue_rows: Sequence[Mapping[str, Any]]) -> None:
    report_line = f"- run267BH_aggressive_candidate_pressure_queue(267BH 공격형 후보 압박 큐): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            f"Run267BH(267BH 실행)는 updated goal(갱신 목표)에 맞춰 aggressive/폭발형 experiment queue(공격형 실험 큐) `{len(queue_rows)}`개를 물질화했다.",
            "Effect(효과): baseline candidate(기준 후보)를 고르는 과정이 defensive filter stacking(방어 필터 덧붙이기)만 되지 않게 하고, 넓은 허용/손익 비대칭/상호작용 피처/과제약 제거 축을 다음 실행 후보로 만든다.",
            f"Next action(다음 행동): `{NEXT_ACTION}`. Effect(효과): MT5(MetaTrader 5, 메타트레이더5) tester handoff(테스터 인계)를 고친 뒤 coarse aggressive tranche(거친 공격형 묶음)를 실행한다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `aggressive_candidate_pressure_queue`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        else:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_after_contains(text, "stage267_run267BG_adjacent_period_replacement_fresh_report_mt5_execution.md", report_line)
        text = append_block_once(text, "Run267BH(267BH 실행)는 updated goal", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BH(267BH 실행) aggressive candidate pressure queue(공격형 후보 압박 큐) `{STATUS}`. "
        f"Effect(효과): defensive filter stacking(방어 필터 덧붙이기)만 반복하지 않도록 다섯 후보 x 네 공격형 변형 = `{len(queue_rows)}`개 큐를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    created_at = utc_now()
    queue_rows = build_queue()
    design_receipt = build_design_receipt(queue_rows)
    failure_memory_seed = build_failure_memory_seed(queue_rows)
    judgment = build_judgment()
    manifest = build_manifest(created_at, queue_rows)
    lineage = build_lineage(manifest)

    write_csv(QUEUE_PATH, queue_rows)
    write_csv(DESIGN_RECEIPT_PATH, design_receipt)
    write_csv(FAILURE_MEMORY_SEED_PATH, failure_memory_seed)
    write_csv(RESULT_JUDGMENT_PATH, judgment)
    write_json(RUN_MANIFEST_PATH, manifest)
    write_json(LINEAGE_PATH, lineage)
    write_md(REPORT_PATH, report_markdown(queue_rows, manifest))
    update_ledgers(created_at, queue_rows)
    update_docs(queue_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "queue_rows": len(queue_rows),
                "report": rel(REPORT_PATH),
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
