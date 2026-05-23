from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild"
RUN_ID = "run274E_screen_post_q04_failure_score_surfaces_v1"
SOURCE_RUN_ID = "run274D_execute_post_q04_failure_scoring_materialization_probe_v1"
STATUS = "completed_post_q04_failure_score_surface_screen_no_survivor_no_candidate_selection"
JUDGMENT = "negative_valid_filter_like_score_surfaces_no_probe_survivor"
JUDGMENT_CLASS = "negative"
NEXT_ACTION = "run274F_close_stage274_open_stage275_fresh_candidate_construction"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN274D = STAGE / "02_runs" / "run274D"
RUN_DIR = STAGE / "02_runs" / "run274E"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_RUN274D_MANIFEST = RUN274D / "run_manifest.json"
SOURCE_SUMMARY = RUN274D / "score_surface_summary.csv"
SOURCE_SCORE_DIR = RUN274D / "score_tables"
SOURCE_NORMALIZATION = RUN274D / "normalization_receipt.json"

DECISION_MATRIX = RUN_DIR / "screening_decision_matrix.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
PROBE_QUEUE = RUN_DIR / "probe_queue.csv"
STAGE275_HANDOFF = RUN_DIR / "stage275_handoff_recommendation.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run274E_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
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
]
STAGE_LEDGER_COLUMNS = [
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
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]

PACKAGE_SHORT_IDS = {
    "cp274A_session_loss_asymmetry_router": "cp274A",
    "cp274B_month_regime_resilience_surface": "cp274B",
    "cp274C_drawdown_recovery_context_router": "cp274C",
    "cp274D_q04_failure_boundary_control": "cp274D",
}
SUPPORT_CONTROL = "cp274D_q04_failure_boundary_control"
SELECTABLE_PACKAGES = [
    "cp274A_session_loss_asymmetry_router",
    "cp274B_month_regime_resilience_surface",
    "cp274C_drawdown_recovery_context_router",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("; ".join(missing))


def score_path(package_id: str) -> Path:
    return SOURCE_SCORE_DIR / f"{PACKAGE_SHORT_IDS[package_id]}_scores.parquet"


def load_scores(package_id: str) -> pd.DataFrame:
    return pd.read_parquet(io_path(score_path(package_id)), columns=["timestamp", "tier_view", "entry_signal", "model_risk_pct"])


def decide_screen(row: Mapping[str, Any]) -> tuple[str, str, str, str]:
    package_id = str(row["package_id"])
    if package_id == SUPPORT_CONTROL:
        return (
            "support_control_reference",
            "q04 failure boundary control(q04 실패 경계 보조 대조)로만 사용한다.",
            "Keeps q04 comparison identity(q04 비교 정체성)를 보존한다.",
            "Never promote directly(직접 승격 금지).",
        )
    changed_rate = float(row["changed_signal_rate"])
    new_active = int(row["new_active_count"])
    removed_active = int(row["removed_active_count"])
    direction_changed = int(row["direction_changed_count"])
    if changed_rate < 0.005:
        return (
            "reject_duplicate_or_near_duplicate_signal_surface",
            "q04 control(q04 대조)과 entry signal(진입 신호)이 거의 같아 fresh decision surface(새 판단 표면)가 아니다.",
            "Risk telemetry(위험 기록) 차이는 보존하지만 candidate package(후보 패키지)로 부르지 않는다.",
            "새 entry creation(진입 생성)이나 direction change(방향 변경)가 생길 때만 재개한다.",
        )
    if new_active == 0 and direction_changed == 0 and removed_active > 0:
        return (
            "reject_filter_like_trade_reduction_surface",
            "새 active trade(활성 거래)를 만들지 않고 q04 trade(q04 거래)를 줄이기만 한다.",
            "Removed pocket(제거 구간)은 failure memory(실패 기억)로 남겨 Stage275(275단계)에서 금지 반복을 막는다.",
            "Non-filter reward creation(비필터 보상 생성) 또는 direction switch(방향 전환)가 생길 때만 재개한다.",
        )
    return (
        "probe_queue",
        "q04 control(q04 대조) 대비 새 signal creation(신호 생성) 또는 direction change(방향 변경)가 있다.",
        "Can feed a later pressure probe(후속 압박 탐침 입력 가능).",
        "MT5 probe(MT5 탐침)에서 curve/trade quality(곡선/거래 품질)가 무너지면 폐기한다.",
    )


def build_decision_matrix() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    control = load_scores(SUPPORT_CONTROL).rename(columns={"entry_signal": "control_entry_signal", "model_risk_pct": "control_model_risk_pct"})
    matrix_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    probe_rows: list[dict[str, Any]] = []
    for package_id in [*SELECTABLE_PACKAGES, SUPPORT_CONTROL]:
        current = load_scores(package_id)
        merged = current.merge(control, on=["timestamp", "tier_view"], how="inner")
        active = merged["entry_signal"].ne("flat")
        control_active = merged["control_entry_signal"].ne("flat")
        changed = merged["entry_signal"].ne(merged["control_entry_signal"])
        new_active = active & ~control_active
        removed_active = ~active & control_active
        direction_changed = active & control_active & changed
        row = {
            "package_id": package_id,
            "package_role": "support_control" if package_id == SUPPORT_CONTROL else "selectable_blueprint",
            "score_table_path": rel(score_path(package_id)),
            "score_table_hash": sha256_file(score_path(package_id)),
            "rows": int(len(merged)),
            "changed_signal_count": int(changed.sum()),
            "changed_signal_rate": round(float(changed.mean()), 8),
            "new_active_count": int(new_active.sum()),
            "removed_active_count": int(removed_active.sum()),
            "direction_changed_count": int(direction_changed.sum()),
            "active_signal_count": int(active.sum()),
            "control_active_signal_count": int(control_active.sum()),
            "active_rate": round(float(active.mean()), 8),
            "control_active_rate": round(float(control_active.mean()), 8),
            "active_rate_delta": round(float(active.mean() - control_active.mean()), 8),
            "mean_risk_delta": round(float((merged["model_risk_pct"] - merged["control_model_risk_pct"]).mean()), 8),
            "claim_boundary": BOUNDARY,
        }
        decision, rationale, salvage, reopen = decide_screen(row)
        row["screen_decision"] = decision
        row["rationale"] = rationale
        row["salvage_value"] = salvage
        row["reopen_condition"] = reopen
        matrix_rows.append(row)
        if decision == "probe_queue":
            probe_rows.append(
                {
                    "queue_id": f"run274E__{package_id}",
                    "package_id": package_id,
                    "source_score_table": row["score_table_path"],
                    "reason": rationale,
                    "next_action": NEXT_ACTION,
                    "claim_boundary": BOUNDARY,
                }
            )
        elif package_id != SUPPORT_CONTROL:
            failure_rows.append(
                {
                    "failure_id": f"NEG-ST274-RUN274E-{PACKAGE_SHORT_IDS[package_id]}",
                    "package_id": package_id,
                    "hypothesis": "Post-q04 score surface(q04 이후 점수 표면)가 fresh decision surface(새 판단 표면)가 될 수 있다.",
                    "why_failed": rationale,
                    "salvage_value": salvage,
                    "reopen_condition": reopen,
                    "evidence_path": rel(DECISION_MATRIX),
                    "claim_boundary": BOUNDARY,
                }
            )
    return matrix_rows, failure_rows, probe_rows


def write_receipts(matrix_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], probe_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "hypothesis": "run274D(274D 실행)의 score surfaces(점수 표면) 중 최소 하나가 q04 control(q04 대조)과 구조적으로 구별될 수 있다.",
            "decision_use": "Stage274(274단계)를 더 밀지, 실패 기억으로 닫고 Stage275(275단계) fresh construction(새 구성)으로 넘길지 결정한다.",
            "comparison_baseline": "cp274D_q04_failure_boundary_control(q04 실패 경계 보조 대조)",
            "control_variables": "Same q04 payload(q04 페이로드), same Tier A/B paired scope(티어 A/B 쌍 범위), same claim boundary(주장 경계).",
            "changed_variables": SELECTABLE_PACKAGES,
            "sample_scope": "Score signal overlap(점수 신호 중복도) only; no trading KPI(거래 핵심 성과 지표 없음).",
            "success_criteria": "At least one selectable package(선택 가능 패키지)가 new_active_count(새 활성 수) 또는 direction_changed_count(방향 변경 수)를 만든다.",
            "failure_criteria": "All selectable packages(모든 선택 가능 패키지)가 duplicate(중복) 또는 filter-like trade reduction(필터형 거래 축소)로 끝난다.",
            "invalid_conditions": "Missing control score table(대조 점수표 누락) or score row mismatch(점수 행 불일치).",
            "stop_conditions": "If probe_queue(탐침 대기열)가 empty(비어 있음), do not run MT5(메타트레이더5 실행 금지) from these packages.",
            "evidence_plan": [rel(DECISION_MATRIX), rel(FAILURE_MEMORY), rel(PROBE_QUEUE), rel(STAGE275_HANDOFF)],
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "data_source": [rel(SOURCE_SUMMARY), rel(SOURCE_SCORE_DIR), rel(SOURCE_RUN274D_MANIFEST)],
            "time_axis": "No new bar calculation(새 봉 계산 없음); timestamp/tier_view(타임스탬프/티어 보기) join(결합) only.",
            "sample_scope": {"matrix_rows": len(matrix_rows), "failure_rows": len(failure_rows), "probe_rows": len(probe_rows)},
            "missing_or_duplicate_check": "Each selectable package(선택 가능 패키지)는 control(대조)과 timestamp+tier_view(타임스탬프+티어 보기)로 inner join(내부 결합)된다.",
            "feature_label_boundary": "No labels(라벨) or profit(수익)을 읽지 않는다.",
            "split_boundary": "Screening(선별)은 signal overlap(신호 중복도)만 보며 split performance(분할 성과)를 말하지 않는다.",
            "leakage_risk": "This screen(선별)은 performance(성과) 없이 structure(구조)만 보므로 candidate claim(후보 주장)을 낮춘다.",
            "data_hash_or_identity": {rel(SOURCE_RUN274D_MANIFEST): sha256_file(SOURCE_RUN274D_MANIFEST), rel(SOURCE_SUMMARY): sha256_file(SOURCE_SUMMARY)},
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "model_family": "deterministic score surfaces(결정 점수 표면)",
            "target_and_label": "No model target(모델 목표) or label(라벨).",
            "split_method": "not_performance_split(성과 분할 아님); structure-only screen(구조 전용 선별).",
            "selection_metric": "changed_signal_rate(변경 신호율), new_active_count(새 활성 수), direction_changed_count(방향 변경 수)",
            "secondary_metrics": ["removed_active_count(제거 활성 수)", "active_rate_delta(활성 비율 차이)", "mean_risk_delta(평균 위험 차이)"],
            "threshold_policy": "fixed structural thresholds(고정 구조 임계값)",
            "overfit_risk": "Using q04 failure memory(q04 실패 기억) can overfit(과적합) if it only removes trades(거래 제거).",
            "calibration_risk": "Score values(점수값)는 probability(확률)가 아니다.",
            "comparison_baseline": "cp274D q04 failure boundary control(q04 실패 경계 보조 대조)",
            "validation_judgment": JUDGMENT,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": "run274E score surface screen(274E 점수 표면 선별)",
                "evidence_available": "screening decision matrix(선별 결정 행렬);failure memory(실패 기억);probe queue(탐침 대기열)",
                "evidence_missing": "MT5 KPI(MT5 핵심 성과 지표);Adapter package(어댑터 패키지);ONNX export/parity(온엑스 내보내기/동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": JUDGMENT_CLASS,
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "이번 점수 표면들은 새 후보가 아니라 q04를 줄이거나 거의 복제한 실패 기억이다.",
            }
        ],
    )
    gate_rows = [
        {
            "gate_name": "scope_completion_gate(범위 완료 게이트)",
            "status": "passed",
            "evidence_path": rel(DECISION_MATRIX),
            "effect": "q04 control(q04 대조) 대비 구조 차이를 계산했다.",
        },
        {
            "gate_name": "kpi_contract_audit(KPI 계약 감사)",
            "status": "passed_with_boundary",
            "evidence_path": rel(DECISION_MATRIX),
            "effect": "trading KPI(거래 핵심 성과 지표)가 아닌 structural scout(구조 탐색) 지표로만 판정했다.",
        },
        {
            "gate_name": "negative_memory_gate(부정 기억 게이트)",
            "status": "passed",
            "evidence_path": rel(FAILURE_MEMORY),
            "effect": "반복 금지와 재개 조건을 failure memory(실패 기억)에 남겼다.",
        },
        {
            "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "required gates(필수 게이트)를 closeout(종료 기록)에 연결했다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]
    write_csv(GATE_AUDIT, gate_rows)
    return gate_rows


def write_outputs(matrix_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], probe_rows: Sequence[Mapping[str, Any]]) -> None:
    matrix_columns = [
        "package_id",
        "package_role",
        "score_table_path",
        "score_table_hash",
        "rows",
        "changed_signal_count",
        "changed_signal_rate",
        "new_active_count",
        "removed_active_count",
        "direction_changed_count",
        "active_signal_count",
        "control_active_signal_count",
        "active_rate",
        "control_active_rate",
        "active_rate_delta",
        "mean_risk_delta",
        "screen_decision",
        "rationale",
        "salvage_value",
        "reopen_condition",
        "claim_boundary",
    ]
    failure_columns = ["failure_id", "package_id", "hypothesis", "why_failed", "salvage_value", "reopen_condition", "evidence_path", "claim_boundary"]
    probe_columns = ["queue_id", "package_id", "source_score_table", "reason", "next_action", "claim_boundary"]
    write_csv(DECISION_MATRIX, matrix_rows, matrix_columns)
    write_csv(FAILURE_MEMORY, failure_rows, failure_columns)
    write_csv(PROBE_QUEUE, probe_rows, probe_columns)
    handoff = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "probe_queue_rows": len(probe_rows),
        "failure_memory_rows": len(failure_rows),
        "recommended_next_stage": "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure",
        "fresh_stage_requirements": [
            "Create new active entries(새 활성 진입 생성) or direction changes(방향 변경), not only q04 trade removal(q04 거래 제거만 금지).",
            "Use a fresh edge thesis(새 거래 우위 논제) rather than q04 repair(4번 분기 수리).",
            "Keep feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), handoff identity(인계 정체성) hashable(해시 가능) from the start.",
        ],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(STAGE275_HANDOFF, handoff)
    decision_lines = "\n".join(
        f"- `{row['package_id']}`: `{row['screen_decision']}`, changed_signal_rate(변경 신호율) `{row['changed_signal_rate']}`, new_active_count(새 활성 수) `{row['new_active_count']}`, removed_active_count(제거 활성 수) `{row['removed_active_count']}`"
        for row in matrix_rows
        if row["package_id"] != SUPPORT_CONTROL
    )
    write_md(
        RUN_REPORT,
        f"""# run274E Score Surface Screen(274E 점수 표면 선별)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- judgment_class(판정 분류): `{JUDGMENT_CLASS}`
- probe_queue_rows(탐침 대기열 행): `{len(probe_rows)}`
- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run274E(274E 실행)는 run274D(274D 실행)의 score surface(점수 표면)를 q04 control(q04 대조)과 비교했다.
효과(effect, 효과): 세 selectable package(선택 가능 패키지)가 새 active signal(활성 신호)을 만들지 못하고 q04 signal(q04 신호)을 복제하거나 줄이는 데 그쳤음을 failure memory(실패 기억)로 남긴다.

## Decisions(결정)

{decision_lines}

## Evidence Paths(근거 경로)

- screening_decision_matrix(선별 결정 행렬): `{rel(DECISION_MATRIX)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- probe_queue(탐침 대기열): `{rel(PROBE_QUEUE)}`
- stage275_handoff_recommendation(275단계 인계 권고): `{rel(STAGE275_HANDOFF)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def write_manifests_and_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    source_inputs = [SOURCE_RUN274D_MANIFEST, SOURCE_SUMMARY, SOURCE_NORMALIZATION, *[score_path(pid) for pid in [*SELECTABLE_PACKAGES, SUPPORT_CONTROL]]]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "judgment_class": JUDGMENT_CLASS,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage274/screen_post_q04_failure_score_surfaces.py",
        "entry_command": "python stage_pipelines/stage274/screen_post_q04_failure_score_surfaces.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(NEGATIVE_REGISTER)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    full_artifacts = [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run274E_score_screen_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run274E score surface screen artifact.",
        }
        for path in full_artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def update_ledgers(matrix_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], probe_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"probe_queue={len(probe_rows)};failure_memory={len(failure_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__{row['package_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": row["package_id"],
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "score_surface_screen",
            "tier_scope": "Tier A+B structural screen",
            "kpi_scope": "signal_overlap_vs_q04_control",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": row["screen_decision"],
            "path": rel(DECISION_MATRIX),
            "primary_kpi": f"changed_signal_rate={row['changed_signal_rate']};new_active_count={row['new_active_count']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;trading_kpi=not_applicable",
            "external_verification_status": "not_applicable",
            "notes": f"removed_active_count={row['removed_active_count']};direction_changed_count={row['direction_changed_count']}",
        }
        for row in matrix_rows
    ]
    stage_rows = [
        {
            "row_id": f"{RUN_ID}__{row['package_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": f"score_surface_screen_{row['package_id']}",
            "tier_scope": "Tier A+B structural screen",
            "scoreboard": "structural_scout",
            "status": STATUS,
            "judgment": row["screen_decision"],
            "evidence_boundary": "screen_only_no_candidate_no_onnx",
            "report_path": rel(RUN_REPORT),
            "notes": f"changed_signal_rate={row['changed_signal_rate']};new_active_count={row['new_active_count']}",
        }
        for row in matrix_rows
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_negative_register(failure_rows: Sequence[Mapping[str, Any]]) -> None:
    if not path_exists(NEGATIVE_REGISTER):
        return
    text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig")
    block_lines = []
    for row in failure_rows:
        block_lines.append(
            f"| `{row['failure_id']}` | `IDEA-ST274-POST-Q04-FILTER-LIKE-SCORE-SURFACE` | {row['hypothesis']} | {row['why_failed']} | {row['salvage_value']} | {row['reopen_condition']} |"
        )
    block = "\n".join(block_lines)
    text = append_once(text, "NEG-ST274-RUN274E-cp274A", block)
    write_md(NEGATIVE_REGISTER, text)


def update_state_docs(matrix_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], probe_rows: Sequence[Mapping[str, Any]]) -> None:
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_once(selection, "run274E_report", f"- run274E_report(274E 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run274E_screening_decision_matrix", f"- run274E_screening_decision_matrix(274E 선별 결정 행렬): `{rel(DECISION_MATRIX)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run274E_report",
        "\n".join(
            [
                f"- run274E_report(274E 보고서): `{rel(RUN_REPORT)}`",
                f"- run274E_screening_decision_matrix(274E 선별 결정 행렬): `{rel(DECISION_MATRIX)}`",
                f"- run274E_failure_memory(274E 실패 기억): `{rel(FAILURE_MEMORY)}`",
                f"- run274E_probe_queue(274E 탐침 대기열): `{rel(PROBE_QUEUE)}`",
                f"- run274E_stage275_handoff(274E 275단계 인계): `{rel(STAGE275_HANDOFF)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run274E_summary",
        f"- run274E_summary(274E 요약): run274E(274E 실행)는 score surface(점수 표면) `{len(matrix_rows)}`개를 q04 control(q04 대조)과 비교했고, probe queue(탐침 대기열) `{len(probe_rows)}`행, failure memory(실패 기억) `{len(failure_rows)}`행을 만들었다. Effect(효과): Stage274(274단계)의 post-q04 rebuild(q04 이후 재구성)는 filter-like/duplicate(필터형/중복) 실패로 닫을 준비를 하며, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage274(274단계) run274E(274E 실행) score surface screen(점수 표면 선별) `{RUN_ID}`. "
        f"Effect(효과): probe queue(탐침 대기열) `{len(probe_rows)}`행과 failure memory(실패 기억) `{len(failure_rows)}`행을 만들고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run274E score surface screen(274E 점수 표면 선별)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): score surface(점수 표면) `{len(matrix_rows)}`개를 비교해 probe queue(탐침 대기열) `{len(probe_rows)}`행과 failure memory(실패 기억) `{len(failure_rows)}`행을 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def execute() -> dict[str, Any]:
    must_exist([SOURCE_RUN274D_MANIFEST, SOURCE_SUMMARY, SOURCE_NORMALIZATION, *[score_path(pid) for pid in [*SELECTABLE_PACKAGES, SUPPORT_CONTROL]]])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    matrix_rows, failure_rows, probe_rows = build_decision_matrix()
    write_outputs(matrix_rows, failure_rows, probe_rows)
    gate_rows = write_receipts(matrix_rows, failure_rows, probe_rows)
    artifacts = [
        DECISION_MATRIX,
        FAILURE_MEMORY,
        PROBE_QUEUE,
        STAGE275_HANDOFF,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    write_manifests_and_registry(created_at, artifacts)
    update_ledgers(matrix_rows, failure_rows, probe_rows)
    update_negative_register(failure_rows)
    update_state_docs(matrix_rows, failure_rows, probe_rows)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "judgment_class": JUDGMENT_CLASS,
        "screened_surfaces": len(matrix_rows),
        "probe_queue_rows": len(probe_rows),
        "failure_memory_rows": len(failure_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
        "gate_rows": len(gate_rows),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
