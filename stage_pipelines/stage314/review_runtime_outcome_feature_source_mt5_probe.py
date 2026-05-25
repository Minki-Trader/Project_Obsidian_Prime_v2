from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402
from stage_pipelines.stage310 import review_runtime_positive_fragment_allocation_mt5_probe as r310  # noqa: E402


STAGE_ID = "314_onnx_candidate_campaign__runtime_outcome_feature_source_rebuild"
RUN_ID = "run314C_review_runtime_outcome_feature_source_mt5_probe_v1"
RUN_NUMBER = "run314C"
SOURCE_RUN_ID = "run314B_execute_runtime_outcome_feature_source_mt5_probe_v1"
PARENT_RUN_ID = "run314A_design_runtime_outcome_feature_source_rebuild_packet_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = r310.BOUNDARY

NEXT_REBUILD_STAGE_ID = "315_onnx_candidate_campaign__runtime_outcome_feature_interaction_rebuild"
NEXT_ADAPTER_STAGE_ID = "315_onnx_candidate_campaign__adapter_package_for_runtime_outcome_feature_source"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN314B = STAGE_ROOT / "02_runs" / "run314B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_KPI = RUN314B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = RUN314B / "attempt_summary.csv"
PRODUCER = Path("stage_pipelines/stage314/review_runtime_outcome_feature_source_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "runtime_outcome_feature_source_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
REPORT_SOURCE_RECEIPT = RUN_ROOT / "report_source_path_receipt.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
SELECTED_QUEUE = RUN_ROOT / "selected_candidate_queue.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage315_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run314C_review_stage315_open.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage314_runtime_outcome_feature_source_review_stage315_open.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = r310.RUN_REGISTRY_COLUMNS
STAGE_LEDGER_COLUMNS = r310.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = r310.ARTIFACT_COLUMNS


def configure_base() -> None:
    replacements = {
        "STAGE_ID": STAGE_ID,
        "RUN_ID": RUN_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "UPDATED_ON": UPDATED_ON,
        "NEXT_REBUILD_STAGE_ID": NEXT_REBUILD_STAGE_ID,
        "NEXT_ADAPTER_STAGE_ID": NEXT_ADAPTER_STAGE_ID,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN310B": RUN314B,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS": REVIEWS,
        "SELECTED": SELECTED,
        "REVIEW_INDEX": REVIEW_INDEX,
        "STAGE_LEDGER": STAGE_LEDGER,
        "SOURCE_KPI": SOURCE_KPI,
        "SOURCE_ATTEMPT_SUMMARY": SOURCE_ATTEMPT_SUMMARY,
        "PRODUCER": PRODUCER,
        "SCOREBOARD": SCOREBOARD,
        "TRADE_QUALITY": TRADE_QUALITY,
        "CURVE": CURVE,
        "REPORT_SOURCE_RECEIPT": REPORT_SOURCE_RECEIPT,
        "FAILURE_MEMORY": FAILURE_MEMORY,
        "SELECTED_QUEUE": SELECTED_QUEUE,
        "NEXT_STAGE_QUEUE": NEXT_STAGE_QUEUE,
        "RESULT_JUDGMENT": RESULT_JUDGMENT,
        "GATE_AUDIT": GATE_AUDIT,
        "RUN_MANIFEST": RUN_MANIFEST,
        "LINEAGE": LINEAGE,
        "REPORT": REPORT,
        "DECISION": DECISION,
        "RUN_REGISTRY": RUN_REGISTRY,
        "ALPHA_LEDGER": ALPHA_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "IDEA_REGISTER": IDEA_REGISTER,
        "NEGATIVE_REGISTER": NEGATIVE_REGISTER,
        "CURRENT_STATE": CURRENT_STATE,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CHANGELOG": CHANGELOG,
    }
    for name, value in replacements.items():
        setattr(r310, name, value)


def rel(path: Path | str) -> str:
    return r310.rel(path)


def write_text(path: Path, text: str) -> None:
    ledger.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ledger.io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    r310.write_csv(path, columns, rows)


def read_text(path: Path) -> str:
    return r310.read_text(path)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    r310.safe_upsert(path, columns, rows, key)


def path_exists(path: Path) -> bool:
    return r310.path_exists(path)


def sha256_file(path: Path) -> str:
    return r310.sha256_file(path)


def number(value: Any, default: float = 0.0) -> float:
    return r310.number(value, default)


def next_stage_rows(scoreboard: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    positive = [row for row in scoreboard if number(row.get("combined_net_profit")) > 0.0]
    return [
        {
            "seed_id": "stage314_runtime_outcome_feature_source_review_seed",
            "source_candidates": ";".join(row["package_id"] for row in positive[:3]) or "none",
            "fresh_thesis": "runtime_outcome_feature_interaction_rebuild",
            "use_as": "failure_memory_or_candidate_seed",
            "upside": "runtime outcome feature source(런타임 결과 피처 원천)가 부분 수익 단서를 만들면 feature interaction(피처 상호작용)으로 규모와 곡선을 동시에 압박한다.",
            "failure_mode": "validation/OOS(검증/표본외), density(밀도), efficiency(효율), curve(곡선)가 함께 통과하지 못하면 실패다.",
            "discard_condition": "narrow feature-threshold repair(좁은 피처 임계값 수정 반복)는 버리고 새 feature interaction(피처 상호작용) 논제로 넘긴다.",
            "next_action": "run315A_design_runtime_outcome_feature_interaction_rebuild_packet",
        }
    ]


def scaffold_next_stage(selected_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if selected_rows:
        next_stage_id = NEXT_ADAPTER_STAGE_ID
        question = "selected runtime outcome feature source(선택된 런타임 결과 피처 원천)를 Adapter package(어댑터 패키지)로 정리할 수 있는가?"
        status = "opened_adapter_package_stage_after_stage314_candidate_selection"
        judgment = "candidate_selected_adapter_package_stage_opened_no_onnx_yet"
        next_action = "run315A_build_runtime_outcome_feature_source_adapter_package"
    else:
        next_stage_id = NEXT_REBUILD_STAGE_ID
        question = "Stage314 runtime outcome feature source(314단계 런타임 결과 피처 원천) 실패 기억을 넘어 feature interaction(피처 상호작용)으로 수익 규모와 곡선을 동시에 개선할 수 있는가?"
        status = "opened_runtime_outcome_feature_interaction_after_stage314_no_selection"
        judgment = "no_candidate_selected_runtime_outcome_feature_interaction_stage_opened"
        next_action = "run315A_design_runtime_outcome_feature_interaction_rebuild_packet"
    next_root = ROOT / "stages" / next_stage_id
    write_text(
        next_root / "00_spec" / "stage_brief.md",
        "\n".join(
            [
                "# Stage315 Brief(315단계 개요)",
                "",
                f"- stage_id(단계 ID): `{next_stage_id}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                f"- question(질문): {question}",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): Stage314(314단계)의 결과를 후보 확정이 아니라 다음 연구 질문의 근거로 넘긴다.",
            ]
        ),
    )
    write_text(
        next_root / "04_selected" / "selection_status.md",
        "\n".join(
            [
                "# Stage315 Selection Status(315단계 선택 상태)",
                "",
                f"- stage_status(단계 상태): `{status}`",
                f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`",
                f"- current_run(현재 실행): `{RUN_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- Adapter package(어댑터 패키지): `{'pending_adapter_build' if selected_rows else 'none'}`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                f"- next_action(다음 행동): `{next_action}`",
                f"- stage314_review(314단계 검토): `{rel(REPORT)}`",
            ]
        ),
    )
    write_text(next_root / "03_reviews" / "review_index.md", f"# Stage315 Review Index(315단계 검토 색인)\n\n- stage314_review(314단계 검토): `{rel(REPORT)}`\n")
    write_csv(
        next_root / "03_reviews" / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage315_open",
                "stage_id": next_stage_id,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "handoff",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "research_development_only",
                "report_path": rel(REPORT),
                "notes": f"next_action={next_action}.",
            }
        ],
    )
    return next_stage_id, status, judgment, next_action
def report_markdown(scoreboard: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]], next_stage_id: str, next_action: str) -> str:
    best = scoreboard[0] if scoreboard else {}
    lines = [
        "# run314C Runtime Outcome Feature Source Review(314C 런타임 결과 피처 원천 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
        f"- Adapter package(어댑터 패키지): `{'deferred_to_stage315' if selected_rows else 'none'}`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}`; source_package(원천 패키지): `{best.get('package_id', 'none')}`",
        "",
        "Effect(효과): actual routed total(실제 라우팅 전체)의 trade list(거래 목록)를 읽어 최소 거래 수, 4-10 trades/day(일 4-10거래), 순수익 규모, 효율, curve pocket(곡선 포켓)을 함께 판정했다.",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | combined(합산) | gates(관문) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        gate_text = ",".join(
            name
            for name, value in (
                ("min", row["minimum_trade_gate"]),
                ("density", row["density_4_10_trades_day_gate"]),
                ("scale", row["profit_scale_gate"]),
                ("eff", row["efficiency_gate"]),
                ("curve", row["curve_pocket_gate"]),
                ("parse", row["report_parse_gate"]),
            )
            if value != "passed"
        )
        lines.append(
            "| {pkg} | {vn:.2f} | {vpf:.2f} | {on:.2f} | {opf:.2f} | {td:.2f}/{od:.2f} | {cn:.2f} | {gates} |".format(
                pkg=row["package_id"],
                vn=number(row["validation_net_profit"]),
                vpf=number(row["validation_pf"]),
                on=number(row["oos_net_profit"]),
                opf=number(row["oos_pf"]),
                td=number(row["validation_trades_per_day"]),
                od=number(row["oos_trades_per_day"]),
                cn=number(row["combined_net_profit"]),
                gates=gate_text or "passed",
            )
        )
    lines.extend(
        [
            "",
            "## Decision(결정)",
            "",
            "Stage314(314단계)는 selected candidate(선택 후보) 없이 닫는다." if not selected_rows else "Stage314(314단계)는 Adapter(어댑터) 패키지 단계로 넘긴다.",
            "Effect(효과): ONNX-worthy(온엑스 가치 있음) 관문 통과 전에는 ONNX(온엑스)를 시작하지 않는다.",
            "",
            f"- opened_stage(열린 단계): `{next_stage_id}`",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def update_docs(status: str, judgment: str, next_stage_id: str, next_action: str, selected_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = r310.replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = r310.replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = r310.replace_line(selected, "- selected_candidate(", f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`")
    selected = r310.replace_line(selected, "- Adapter package(", f"- Adapter package(어댑터 패키지): `{'deferred_to_stage315' if selected_rows else 'none'}`")
    selected = r310.replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selected = r310.drop_prefixed_lines(selected, ("- run314C_report(", "- stage315_opened("))
    selected += f"- run314C_report(314C 보고서): `{rel(REPORT)}`\n"
    selected += f"- stage315_opened(315단계 열림): `{next_stage_id}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = r310.drop_prefixed_lines(review_index, ("- run314C_report(", "- run314C_scoreboard(", "- stage315_seed_queue("))
    review_index += f"- run314C_report(314C 보고서): `{rel(REPORT)}`\n"
    review_index += f"- run314C_scoreboard(314C 점수판): `{rel(SCOREBOARD)}`\n"
    review_index += f"- stage315_seed_queue(315단계 씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = r310.replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`")
    current = r310.replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = r310.replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{next_stage_id}`")
    current = r310.replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = r310.replace_line(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = r310.drop_prefixed_lines(current, ("- run314C_summary(",))
    current = current.rstrip() + f"\n- run314C_summary(314C 요약): Stage314(314단계) actual MT5(실제 메타트레이더5) 검토를 완료했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_rows[0]['package_id'] if selected_rows else 'none'}`이고 next_stage(다음 단계)는 `{next_stage_id}`다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = r310.replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = r310.replace_line(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = r310.replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage314(314단계) run314C(314C 실행) runtime outcome feature source review(런타임 결과 피처 원천 검토) `{RUN_ID}` closed Stage314 and opened `{next_stage_id}`. "
        f"Effect(효과): selected candidate(선택 후보)는 `{selected_rows[0]['package_id'] if selected_rows else 'none'}`이고 Adapter package(어댑터 패키지)는 `{'deferred_to_stage315' if selected_rows else 'none'}`, ONNX readiness(온엑스 준비)는 `not_started`다.\n"
    )
    workspace = r310.prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += (
            f"\n## {UPDATED_ON} run314C Runtime outcome feature source review(314C 런타임 결과 피처 원천 검토)\n\n"
            f"- status(상태): `{status}`\n"
            f"- judgment(판정): `{judgment}`\n"
            f"- effect(효과): Stage314(314단계)를 닫고 `{next_stage_id}`를 열었다.\n"
            "- boundary(경계): 운영 승격이나 런타임 권위를 주장하지 않는다.\n"
        )
    write_text(CHANGELOG, changelog)


def update_memory_registers(failures: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} runtime_outcome_feature_source_review(런타임 결과 피처 원천 검토)\n\n"
            "- idea_id(아이디어 ID): `stage314_runtime_outcome_feature_source_review`\n"
            f"- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate={selected_rows[0]['package_id'] if selected_rows else 'none'}.\n"
        )
        write_text(IDEA_REGISTER, idea)
    if failures:
        negative = read_text(NEGATIVE_REGISTER)
        if RUN_ID not in negative:
            negative += (
                f"\n## {RUN_ID} Stage314 runtime outcome feature source failure memory(314단계 런타임 결과 피처 원천 실패 기억)\n\n"
                f"- failed_profiles(실패 프로필): `{len(failures)}`\n"
                "- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5)에서 최소 거래 수, 밀도, 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.\n"
                "- do_not_repeat(반복 금지): 시간-방향 표만 좁게 다시 보정하지 않는다.\n"
                "- reopen_condition(재개 조건): runtime outcome source(런타임 결과 원천) 자체를 바꿀 때만 재사용한다.\n"
            )
            write_text(NEGATIVE_REGISTER, negative)


def update_registers(status: str, judgment: str, next_action: str) -> None:
    safe_upsert(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "runtime_outcome_feature_source_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate_reviewed;next_action={next_action}."}], "run_id")
    safe_upsert(
        ALPHA_LEDGER,
        ledger.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "runtime_outcome_feature_source_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "trade_quality_curve_profit_scale",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": "actual_mt5_review_completed",
                "guardrail_kpi": "ONNX=not_started",
                "external_verification_status": "completed",
                "notes": f"next_action={next_action}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "runtime_outcome_feature_source_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "runtime_outcome_feature_source_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_onnx", "report_path": rel(REPORT), "notes": "Stage315 opened if no selected candidate; ONNX not started."}], "row_id")


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    for path in paths:
        if not path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage314_runtime_outcome_feature_source_review_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": "2026-05-24T23:59:00Z",
                "notes": "Stage314 review and Stage314 open handoff",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    configure_base()
    rows, report_receipts = r310.load_actual_rows()
    scoreboard, failure_rows, selected_rows = r310.build_scoreboard(rows)
    stage314_rows = next_stage_rows(scoreboard)
    next_stage_id, _next_status, _next_judgment, next_action = scaffold_next_stage(selected_rows)
    status = "completed_runtime_outcome_feature_source_review_stage315_opened"
    judgment = "actual_mt5_candidate_gate_passed_adapter_stage_opened" if selected_rows else "actual_mt5_no_onnx_worthy_candidate_runtime_outcome_feature_source_opened"

    write_csv(SCOREBOARD, list(scoreboard[0].keys()) if scoreboard else ["materialized_branch_id"], scoreboard)
    write_csv(TRADE_QUALITY, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(REPORT_SOURCE_RECEIPT, list(report_receipts[0].keys()) if report_receipts else ["attempt_name"], report_receipts)
    write_csv(CURVE, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(FAILURE_MEMORY, list(failure_rows[0].keys()) if failure_rows else ["failure_id"], failure_rows)
    write_csv(SELECTED_QUEUE, list(selected_rows[0].keys()) if selected_rows else ["materialized_branch_id"], selected_rows)
    write_csv(NEXT_STAGE_QUEUE, list(stage314_rows[0].keys()), stage314_rows)
    write_csv(
        RESULT_JUDGMENT,
        ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "next_action", "claim_boundary"),
        [{"run_id": RUN_ID, "status": status, "judgment": judgment, "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none", "adapter_package": "deferred_to_stage315" if selected_rows else "none", "onnx_readiness": "not_started", "next_action": next_action, "claim_boundary": BOUNDARY}],
    )
    gate_rows = [
        {"gate_name": "mt5_runtime_probe(런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "MT5 runtime output(MT5 런타임 출력)을 검토했다."},
        {"gate_name": "report_source_path_curve_parse(보고서 경로 곡선 파싱)", "status": "passed" if all(row["report_status"] == "exists" for row in report_receipts) else "partial", "evidence_path": rel(REPORT_SOURCE_RECEIPT), "effect": "거래 목록 기반 curve pocket(곡선 포켓)을 판정했다."},
        {"gate_name": "minimum_trade_and_density(최소 거래와 밀도)", "status": "passed" if selected_rows else "mixed", "evidence_path": rel(SCOREBOARD), "effect": "minimum trade count(최소 거래 수)와 4-10 trades/day(일 4-10거래)를 후보 gate(관문)로 읽었다."},
        {"gate_name": "profit_scale_efficiency_curve(수익 규모/효율/곡선)", "status": "passed" if selected_rows else "failed", "evidence_path": rel(SCOREBOARD), "effect": "profit scale(수익 규모), PF/recovery/expectancy(수익 팩터/회복/기대값), curve pocket(곡선 포켓)을 함께 판정했다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "prepared_next_stage" if selected_rows else "not_started", "evidence_path": rel(NEXT_STAGE_QUEUE), "effect": "선택 후보가 없으면 Adapter(어댑터)를 시작하지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter package(어댑터 패키지) 전에는 ONNX(온엑스)를 시작하지 않는다."},
    ]
    write_csv(GATE_AUDIT, list(gate_rows[0].keys()), gate_rows)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none",
        "adapter_package": "deferred_to_stage315" if selected_rows else "none",
        "onnx_readiness": "not_started",
        "goal_achieve": "not_claimed",
        "next_stage_id": next_stage_id,
        "next_action": next_action,
        "artifacts": [rel(path) for path in (SCOREBOARD, TRADE_QUALITY, REPORT_SOURCE_RECEIPT, CURVE, FAILURE_MEMORY, SELECTED_QUEUE, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION)],
        "claim_boundary": BOUNDARY,
    }
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(
        LINEAGE,
        json.dumps(
            {
                "run_id": RUN_ID,
                "producer": str(PRODUCER),
                "source_inputs": [rel(SOURCE_KPI), rel(SOURCE_ATTEMPT_SUMMARY)],
                "consumer": next_action,
                "artifact_paths": manifest["artifacts"],
                "availability": "tracked_manifest_plus_runtime_reports",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_text(REPORT, report_markdown(scoreboard, selected_rows, next_stage_id, next_action))
    write_text(
        DECISION,
        "\n".join(
            [
                "# Stage314 Decision(314단계 결정)",
                "",
                f"- decision(결정): `{judgment}`",
                f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- Adapter package(어댑터 패키지): `{'deferred_to_stage315' if selected_rows else 'none'}`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                f"- next_stage(다음 단계): `{next_stage_id}`",
                "",
                "Effect(효과): ONNX-worthy(온엑스 가치 있음) 관문 통과 전에는 Adapter(어댑터)와 ONNX(온엑스)를 시작하지 않는다.",
            ]
        ),
    )
    update_docs(status, judgment, next_stage_id, next_action, selected_rows)
    update_registers(status, judgment, next_action)
    update_memory_registers(failure_rows, selected_rows)
    next_root = ROOT / "stages" / next_stage_id
    update_artifact_registry(
        [
            SCOREBOARD,
            TRADE_QUALITY,
            REPORT_SOURCE_RECEIPT,
            CURVE,
            FAILURE_MEMORY,
            SELECTED_QUEUE,
            NEXT_STAGE_QUEUE,
            RESULT_JUDGMENT,
            GATE_AUDIT,
            RUN_MANIFEST,
            LINEAGE,
            REPORT,
            DECISION,
            next_root / "00_spec" / "stage_brief.md",
            next_root / "04_selected" / "selection_status.md",
            next_root / "03_reviews" / "review_index.md",
            next_root / "03_reviews" / "stage_run_ledger.csv",
        ]
    )
    print(json.dumps({"status": status, "judgment": judgment, "scoreboard_rows": len(scoreboard), "failure_rows": len(failure_rows), "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none", "adapter_package": "deferred_to_stage315" if selected_rows else "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_stage_id": next_stage_id, "next_action": next_action}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
