from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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


STAGE_ID = "277_onnx_candidate_campaign__fresh_thesis_rebuild"
RUN_ID = "run277E_screen_fresh_thesis_score_surfaces_v1"
SOURCE_RUN_ID = "run277D_execute_fresh_thesis_scoring_probe_v1"
STATUS = "completed_fresh_thesis_score_surface_screen_no_candidate_selection"
JUDGMENT = "fresh_thesis_score_surface_probe_queue_ready_no_candidate_selection"
NEXT_ACTION = "run277F_close_stage277_open_stage278_fresh_thesis_mt5_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN277D = STAGE / "02_runs" / "run277D"
RUN_DIR = STAGE / "02_runs" / "run277E"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SOURCE_SCORE_SUMMARY = RUN277D / "score_surface_summary.csv"
SOURCE_TIER_SUMMARY = RUN277D / "tier_score_summary.csv"
SOURCE_HANDOFF = RUN277D / "handoff_index.csv"
SOURCE_DATA = RUN277D / "data_integrity_receipt.csv"
SOURCE_MANIFEST = RUN277D / "run_manifest.json"

SCREEN_MATRIX = RUN_DIR / "screening_decision_matrix.csv"
STAGE278_QUEUE = RUN_DIR / "stage278_probe_queue.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
SUPPORT_CONTROL = RUN_DIR / "support_control.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run277E_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage277/screen_fresh_thesis_score_surfaces.py")

SCREEN_COLUMNS = (
    "package_id",
    "combined_oos_mean_score",
    "combined_oos_decision_rate",
    "combined_validation_mean_score",
    "combined_validation_decision_rate",
    "score_alignment_delta",
    "decision_rate_delta",
    "tier_b_missing_required_feature_count",
    "screen_score",
    "screen_read",
    "next_use",
    "selected_candidate",
    "onnx_readiness",
)
QUEUE_COLUMNS = (
    "queue_id",
    "package_id",
    "priority",
    "fresh_thesis_read",
    "score_basis",
    "mt5_probe_intent",
    "required_records",
    "handoff_source",
    "discard_condition",
    "selected_candidate",
    "onnx_readiness",
    "next_action",
)
FAILURE_COLUMNS = ("package_id", "failure_label", "why_not_probe", "salvage_value", "reopen_condition", "selected_candidate", "onnx_readiness")
SUPPORT_COLUMNS = ("control_id", "purpose", "source", "expected_use", "boundary")
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
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


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def f(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def by_package_split(rows: Sequence[Mapping[str, str]], tier_scope: str, split: str) -> dict[str, Mapping[str, str]]:
    return {row["package_id"]: row for row in rows if row.get("tier_scope") == tier_scope and row.get("split") == split}


def screen(summary_rows: Sequence[Mapping[str, str]], data_rows: Sequence[Mapping[str, str]], handoff_rows: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    combined_oos = by_package_split(summary_rows, "Tier A+B combined", "oos")
    combined_val = by_package_split(summary_rows, "Tier A+B combined", "validation")
    handoff_by_package = {row["package_id"]: row for row in handoff_rows}
    tier_b_missing = max(int(f(row.get("missing_required_feature_count"))) for row in data_rows if row.get("tier_scope") == "Tier B")
    matrix: list[dict[str, Any]] = []
    queue: list[dict[str, Any]] = []
    failure: list[dict[str, Any]] = []
    for package_id, oos in combined_oos.items():
        val = combined_val.get(package_id, {})
        oos_mean = f(oos.get("mean_candidate_decision_score"))
        val_mean = f(val.get("mean_candidate_decision_score"))
        oos_rate = f(oos.get("decision_rate"))
        val_rate = f(val.get("decision_rate"))
        score_delta = abs(oos_mean - val_mean)
        rate_delta = abs(oos_rate - val_rate)
        density_ok = 0.12 <= oos_rate <= 0.42
        alignment_ok = score_delta <= 0.09 and rate_delta <= 0.14
        score_strength = oos_mean + f(oos.get("q95_candidate_decision_score")) * 0.25
        penalty = 0.04 * tier_b_missing + (0.08 if not density_ok else 0.0) + (0.08 if not alignment_ok else 0.0)
        screen_score = score_strength - penalty
        probe_ready = screen_score >= 0.42 and density_ok
        read = "probe_queue_not_candidate" if probe_ready else "failure_memory_or_watch_only"
        next_use = "stage278_probe_queue" if probe_ready else "failure_memory"
        matrix.append(
            {
                "package_id": package_id,
                "combined_oos_mean_score": oos_mean,
                "combined_oos_decision_rate": oos_rate,
                "combined_validation_mean_score": val_mean,
                "combined_validation_decision_rate": val_rate,
                "score_alignment_delta": score_delta,
                "decision_rate_delta": rate_delta,
                "tier_b_missing_required_feature_count": tier_b_missing,
                "screen_score": screen_score,
                "screen_read": read,
                "next_use": next_use,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
        if probe_ready:
            priority = "P1" if screen_score >= 0.58 else "P2"
            queue.append(
                {
                    "queue_id": f"run277E_{package_id}",
                    "package_id": package_id,
                    "priority": priority,
                    "fresh_thesis_read": read,
                    "score_basis": f"combined_oos_mean={oos_mean:.6f};combined_oos_rate={oos_rate:.6f};screen_score={screen_score:.6f}",
                    "mt5_probe_intent": "materialize MT5 signal payload(메타트레이더5 신호 페이로드 물질화) then pressure probe(압박 탐침)",
                    "required_records": "Tier A separate;Tier B separate;Tier A+B combined",
                    "handoff_source": handoff_by_package.get(package_id, {}).get("handoff_json_path", ""),
                    "discard_condition": "MT5 validation/OOS(검증/표본외) trade quality(거래 품질)가 동시 약하면 폐기",
                    "selected_candidate": "none",
                    "onnx_readiness": "not_claimed",
                    "next_action": NEXT_ACTION,
                }
            )
        else:
            failure.append(
                {
                    "package_id": package_id,
                    "failure_label": "score_screen_not_probe_ready",
                    "why_not_probe": f"density_ok={density_ok};alignment_ok={alignment_ok};screen_score={screen_score:.6f}",
                    "salvage_value": "score shape(점수 모양) 단서로만 보존",
                    "reopen_condition": "new feature/decision/risk surface(새 피처/판단/위험 표면) or stronger score screen(더 강한 점수 선별)",
                    "selected_candidate": "none",
                    "onnx_readiness": "not_claimed",
                }
            )
    queue.sort(key=lambda row: (row["priority"], row["package_id"]))
    support = [
        {
            "control_id": "ctrl277E_tier_b_missing_feature_watch",
            "purpose": "Tier B missing feature watch(Tier B 누락 피처 관찰)",
            "source": rel(SOURCE_DATA),
            "expected_use": "Stage278(278단계) MT5 probe(탐침) 전 Tier B(티어 B) partial context(부분 문맥) 경계를 계속 표시한다.",
            "boundary": "support control only(보조 대조만), selected candidate(선택 후보) 아님",
        }
    ]
    return matrix, queue, failure, support


def write_report(matrix: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]]) -> None:
    queue_lines = "\n".join(f"- `{row['package_id']}` priority(우선순위) `{row['priority']}` score_basis(점수 근거) `{row['score_basis']}`" for row in queue) or "- none(없음)"
    failure_lines = "\n".join(f"- `{row['package_id']}`: `{row['why_not_probe']}`" for row in failure) or "- none(없음)"
    write_md(
        REPORT,
        f"""# run277E Report(277E 보고서): Fresh Thesis Score Surface Screen(새 논제 점수 표면 선별)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- matrix_rows(행렬 행): `{len(matrix)}`
- probe_queue_rows(탐침 대기열 행): `{len(queue)}`
- failure_memory_rows(실패 기억 행): `{len(failure)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Probe Queue(탐침 대기열)

{queue_lines}

## Failure Memory(실패 기억)

{failure_lines}

## Boundary(경계)

run277E(277E 실행)는 score surface(점수 표면)를 MT5 probe(메타트레이더5 탐침) 대기열로 선별했다.
Effect(효과): probe queue(탐침 대기열)는 selected candidate(선택 후보)가 아니며 ONNX readiness(온엑스 준비)도 아니다.
""",
    )


def write_receipts(queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]]) -> None:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run277E fresh thesis score surface screen(277E 새 논제 점수 표면 선별)",
                "evidence_available": "score summary(점수 요약), handoff index(인계 색인), data integrity receipt(데이터 무결성 영수증)",
                "evidence_missing": "MT5 runtime result(MT5 런타임 결과), backtest KPI(백테스트 핵심 성과 지표), selected candidate(선택 후보), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "probe_queue_ready_no_selection(탐침 대기열 준비, 선택 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": f"probe_queue_rows(탐침 대기열 행)={len(queue)}; failure_memory_rows(실패 기억 행)={len(failure)}; 선택 후보는 없다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "score_screen_gate(점수 선별 게이트)",
                "status": "passed_probe_queue_created(탐침 대기열 생성으로 통과)" if queue else "passed_no_probe_queue(탐침 대기열 없음으로 통과)",
                "evidence_path": rel(SCREEN_MATRIX),
                "effect": "score surface(점수 표면)를 MT5(메타트레이더5) 전 단계에서 분리한다.",
            },
            {
                "gate_name": "paired_tier_boundary_gate(티어 쌍 경계 게이트)",
                "status": "passed_tier_b_missing_features_carried(Tier B 누락 피처 이월로 통과)",
                "evidence_path": rel(SUPPORT_CONTROL),
                "effect": "Tier B(티어 B)의 partial context(부분 문맥)를 다음 단계에 숨기지 않는다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/온엑스 없음/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "probe queue(탐침 대기열)를 후보 선택으로 올려 말하지 않는다.",
            },
            {
                "gate_name": "next_stage_gate(다음 단계 게이트)",
                "status": "passed_stage278_mt5_probe_queue(278단계 MT5 탐침 대기열로 통과)" if queue else "passed_close_or_redesign_required(종료 또는 재설계 필요로 통과)",
                "evidence_path": rel(STAGE278_QUEUE),
                "effect": "다음 큰 질문을 MT5 probe(메타트레이더5 탐침)로 분리한다.",
            },
        ],
    )


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def manifest_payload(created_at: str, outputs: Sequence[Path], queue_count: int, failure_count: int) -> dict[str, Any]:
    sources = [SOURCE_SCORE_SUMMARY, SOURCE_TIER_SUMMARY, SOURCE_HANDOFF, SOURCE_DATA, SOURCE_MANIFEST]
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "consumer": [STAGE_ID, NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
        "source_inputs": [rel(path) for path in sources],
        "source_hashes": output_hashes(sources),
        "output_artifacts": [rel(path) for path in outputs],
        "output_hashes": output_hashes(outputs),
        "probe_queue_rows": queue_count,
        "failure_memory_rows": failure_count,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": manifest["consumer"],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def update_registers(created_at: str, queue_count: int, failure_count: int, outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "score_surface_screen",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"probe_queue_rows={queue_count};failure_memory_rows={failure_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__score_surface_screen",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "score_surface_screen",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "run277E score surface screen(277E 점수 표면 선별)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "score_screen",
                "scoreboard_lane": "fresh_thesis_rebuild",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"probe_queue_rows={queue_count};failure_memory_rows={failure_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_score_screen",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__score_surface_screen",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_score_surface_screen",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "score_screen",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "probe_queue_only_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"probe_queue_rows={queue_count};failure_memory_rows={failure_count};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "run277E_score_screen_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run277E score surface screen artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(queue_count: int, failure_count: int) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run277E_report", f"- run277E_report(277E 보고서): `{rel(REPORT)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review_index = append_once(
        review_index,
        "run277E_report",
        "\n".join(
            [
                f"- run277E_report(277E 보고서): `{rel(REPORT)}`",
                f"- run277E_stage278_queue(277E 278단계 대기열): `{rel(STAGE278_QUEUE)}`",
                f"- run277E_failure_memory(277E 실패 기억): `{rel(FAILURE_MEMORY)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_score_surface_screen`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run277E_summary",
        (
            f"- run277E_summary(277E 요약): score surface screen(점수 표면 선별)에서 probe queue(탐침 대기열) `{queue_count}`개와 failure memory(실패 기억) `{failure_count}`개를 만들었다. "
            "Effect(효과): Stage278(278단계) MT5 probe(MT5 탐침)로 넘기되 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage277(277단계) run277E(277E 실행) fresh thesis score surface screen(새 논제 점수 표면 선별) `{RUN_ID}`. "
        f"Effect(효과): Stage278 probe queue(278단계 탐침 대기열) `{queue_count}`개와 failure memory(실패 기억) `{failure_count}`개를 만들었고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage277(277단계) run277E(277E 실행)")
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run277E Fresh thesis score surface screen(새 논제 점수 표면 선별)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): probe queue(탐침 대기열) `{queue_count}`개와 failure memory(실패 기억) `{failure_count}`개를 만들고 Stage278(278단계) MT5 probe(MT5 탐침)로 넘긴다.\n"
            "- boundary(경계): selected candidate(선택 후보), MT5 runtime result(MT5 런타임 결과), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST277-FRESH-THESIS-REBUILD-RUN277E",
        f"| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277E` | `{STAGE_ID}` | run277D(277D 실행) score surface(점수 표면)를 Stage278(278단계) MT5 probe(MT5 탐침) queue(대기열)로 선별한다. | `probe_queue={queue_count};failure_memory={failure_count}` | `probe_queue_ready_no_selection` | next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def run() -> dict[str, Any]:
    must_exist([SOURCE_SCORE_SUMMARY, SOURCE_TIER_SUMMARY, SOURCE_HANDOFF, SOURCE_DATA, SOURCE_MANIFEST])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    matrix, queue, failure, support = screen(read_csv_rows(SOURCE_SCORE_SUMMARY), read_csv_rows(SOURCE_DATA), read_csv_rows(SOURCE_HANDOFF))
    write_csv(SCREEN_MATRIX, SCREEN_COLUMNS, matrix)
    write_csv(STAGE278_QUEUE, QUEUE_COLUMNS, queue)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure)
    write_csv(SUPPORT_CONTROL, SUPPORT_COLUMNS, support)
    write_report(matrix, queue, failure)
    write_receipts(queue, failure)

    outputs = [SCREEN_MATRIX, STAGE278_QUEUE, FAILURE_MEMORY, SUPPORT_CONTROL, RESULT_JUDGMENT, GATE_AUDIT, REPORT]
    manifest = manifest_payload(created_at, outputs, len(queue), len(failure))
    write_json(RUN_MANIFEST, manifest)
    outputs.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, outputs, len(queue), len(failure))
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    outputs.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, outputs, len(queue), len(failure))
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, len(queue), len(failure), outputs)
    update_state_docs(len(queue), len(failure))

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "probe_queue_rows": len(queue),
        "failure_memory_rows": len(failure),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
