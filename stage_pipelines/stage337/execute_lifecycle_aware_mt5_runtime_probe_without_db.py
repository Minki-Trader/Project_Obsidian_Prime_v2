from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402
from stage_pipelines.stage337 import train_lifecycle_aware_guarded_scouts_without_db as cd  # noqa: E402


aw = cd.aw
bg = cd.bg

TODAY = "2026-05-28"
STAGE_ID = cd.STAGE_ID
RUN_NUMBER = "run337CE"
RUN_ID = "run337CE_execute_lifecycle_aware_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = cd.RUN_ID
NEXT_RUN_ID = "run337CF_review_lifecycle_aware_runtime_probe_and_failure_attribution_without_db_v1"
REPAIR_NEXT_RUN_ID = "run337CF_repair_lifecycle_aware_runtime_probe_handoff_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CE_lifecycle_aware_mt5_runtime_probe_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = cd.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_COPY_DIR = RUN_DIR / "models"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEWS_DIR = cd.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337CE_lifecycle_aware_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CE_lifecycle_aware_mt5_runtime_probe.md"
SELECTED_STATUS = cd.SELECTED_STATUS
STAGE_BRIEF = cd.STAGE_BRIEF
WORKSPACE_STATE = cd.WORKSPACE_STATE
CURRENT_STATE = cd.CURRENT_STATE
CHANGELOG = cd.CHANGELOG
RUN_REGISTRY = cd.RUN_REGISTRY
ALPHA_LEDGER = cd.ALPHA_LEDGER
ARTIFACT_REGISTRY = cd.ARTIFACT_REGISTRY
STAGE_LEDGER = cd.STAGE_LEDGER

PARENT_FINAL = cd.FINAL_DECISION
PARENT_PACKAGE = cd.MT5_RUNTIME_PROBE_PACKAGE
PARENT_PROXY_EXPECTED = cd.PROXY_EXPECTED_FORWARD
PARENT_QUEUE = cd.NEXT_RESEARCH_QUEUE
PARENT_ONNX_PARITY = cd.ONNX_PARITY
PARENT_LIFECYCLE_SCORECARD = cd.LIFECYCLE_SCORECARD

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_lifecycle_aware_mt5_runtime_probe"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
COMMON_SYNC = RUN_DIR / "common_files_sync.csv"
EXECUTION_SUMMARY = RUN_DIR / "lifecycle_aware_mt5_runtime_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
TESTER_SETTINGS_IDENTITY = RUN_DIR / "tester_settings_identity.json"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    COMMON_SYNC,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    RUNTIME_IDENTITY,
    TESTER_SETTINGS_IDENTITY,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

INPUT_FILES = (
    PARENT_FINAL,
    PARENT_PACKAGE,
    PARENT_PROXY_EXPECTED,
    PARENT_QUEUE,
    PARENT_ONNX_PARITY,
    PARENT_LIFECYCLE_SCORECARD,
    bv.EA_SOURCE,
)


def rel(path: Path | str) -> str:
    value = Path(path)
    try:
        return value.resolve().relative_to(ROOT.resolve()).as_posix()
    except (ValueError, RuntimeError):
        return value.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def parse_args() -> argparse.Namespace:
    parser = bv.parse_args()
    parser.description = "Stage337CE lifecycle-aware MT5 runtime probe."
    return parser


def configure_runtime_helpers() -> None:
    replacements: dict[str, Any] = {
        "bu": cd,
        "aw": cd.aw,
        "bg": cd.bg,
        "__file__": __file__,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "REPAIR_NEXT_RUN_ID": REPAIR_NEXT_RUN_ID,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "STAGE_DIR": STAGE_DIR,
        "RUN_DIR": RUN_DIR,
        "MT5_DIR": MT5_DIR,
        "SET_DIR": SET_DIR,
        "INI_DIR": INI_DIR,
        "MODEL_COPY_DIR": MODEL_COPY_DIR,
        "FEATURE_COPY_DIR": FEATURE_COPY_DIR,
        "TELEMETRY_COPY_DIR": TELEMETRY_COPY_DIR,
        "REPORT_COPY_DIR": REPORT_COPY_DIR,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "SELECTED_STATUS": SELECTED_STATUS,
        "STAGE_BRIEF": STAGE_BRIEF,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CURRENT_STATE": CURRENT_STATE,
        "CHANGELOG": CHANGELOG,
        "RUN_REGISTRY": RUN_REGISTRY,
        "ALPHA_LEDGER": ALPHA_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "STAGE_LEDGER": STAGE_LEDGER,
        "PARENT_FINAL": PARENT_FINAL,
        "PARENT_PACKAGE": PARENT_PACKAGE,
        "PARENT_PROXY_EXPECTED": PARENT_PROXY_EXPECTED,
        "PARENT_QUEUE": PARENT_QUEUE,
        "PARENT_ONNX_PARITY": PARENT_ONNX_PARITY,
        "COMMON_ROOT": COMMON_ROOT,
        "COMMON_MODEL_DIR": COMMON_MODEL_DIR,
        "COMMON_FEATURE_DIR": COMMON_FEATURE_DIR,
        "COMMON_TELEMETRY_DIR": COMMON_TELEMETRY_DIR,
    }
    for name, value in replacements.items():
        setattr(bv, name, value)


def classify(summary_rows: Sequence[Mapping[str, Any]], materialize_only: bool, parent_final: Mapping[str, Any]) -> tuple[str, str, str, str]:
    if materialize_only:
        return (
            "materialized_stage337CE_lifecycle_aware_mt5_runtime_probe_package_no_mt5_execution",
            "materialized_only_actual_mt5_not_executed",
            "stage337CE_keep_runtime_probe_execution_open",
            RUN_ID,
        )
    if not summary_rows:
        return (
            "blocked_stage337CE_no_probe_summary_rows",
            "no_runtime_probe_summary_created",
            "stage337CE_blocked_no_summary_rows",
            REPAIR_NEXT_RUN_ID,
        )
    blocked = [row for row in summary_rows if str(row.get("comparison_status", "")).startswith("blocked")]
    if blocked:
        return (
            "blocked_stage337CE_lifecycle_aware_mt5_runtime_probe_proxy_mismatch_or_no_output",
            "mt5_runtime_probe_missing_or_proxy_mt5_mismatch_requires_repair",
            "stage337CE_open_runtime_probe_handoff_repair",
            REPAIR_NEXT_RUN_ID,
        )
    all_reached = all(str(row.get("feature_last_reached", "")).lower() == "true" for row in summary_rows)
    cost2_note = "cost2_proxy_guard_failed" if int(parent_final.get("cost2_survivors", 0)) == 0 else "cost2_proxy_guard_has_survivor"
    if all_reached:
        return (
            "completed_stage337CE_lifecycle_aware_mt5_runtime_probe_exact_proxy_parity_no_forward_decision",
            f"mt5_runtime_matches_cd_proxy_expected_through_feature_last_{cost2_note}",
            "stage337CE_open_run337CF_runtime_probe_review_and_failure_attribution",
            NEXT_RUN_ID,
        )
    return (
        "completed_stage337CE_lifecycle_aware_mt5_runtime_probe_overlap_parity_tester_gap_remains_no_forward_decision",
        f"mt5_runtime_matches_cd_proxy_expected_on_overlap_but_tester_gap_remains_{cost2_note}",
        "stage337CE_open_run337CF_runtime_probe_gap_and_failure_attribution_review",
        NEXT_RUN_ID,
    )


def build_gates(
    parent: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    sync_rows: Sequence[Mapping[str, Any]],
    execution: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    def row(gate_id: str, passed: bool, observed: str, expected: str, effect: str) -> dict[str, Any]:
        return {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    compile_ok = execution.get("compile", {}).get("status") == "completed" or execution.get("portable_ea_ex5_exists")
    sync_ok = all(str(item.get("status")) == "copied" for item in sync_rows if str(item.get("sync_id", "")).startswith(("common_", "local_", "ea_binary")))
    tester_attempted = any(str(item.get("status")) != "not_run_materialize_only" for item in execution.get("execution_results", []))
    mismatches = sum(1 for item in diff_rows if item.get("comparison_status") != "matched")
    return [
        row("ce_gate_parent_cd_loaded", parent.get("next_action") == RUN_ID, str(parent.get("next_action")), RUN_ID, "CD 산출물이 CE runtime probe(런타임 탐침)를 열었는지 확인한다."),
        row("ce_gate_attempts_materialized", len(attempts) == 6, f"attempts={len(attempts)}", "6 attempts", "6개 CD ONNX(온엑스)를 모두 MT5 입력으로 만들었는지 확인한다."),
        row("ce_gate_common_files_synced", sync_ok, f"sync_rows={len(sync_rows)}", "Common Files synced", "MT5 terminal(터미널)이 같은 feature/model(피처/모델)을 보게 한다."),
        row("ce_gate_compile_or_existing_ex5", bool(compile_ok), str(execution.get("compile", {}).get("status")), "compile completed or existing EX5", "EA compile(전문가 자문 컴파일) 또는 기존 EX5(실행 파일) 정체성을 확보한다."),
        row("ce_gate_tester_attempted", tester_attempted, f"results={len(execution.get('execution_results', []))}", "tester attempted unless materialize-only", "Strategy Tester(전략 테스터)를 실제로 시도했는지 확인한다."),
        row("ce_gate_runtime_outputs", all(str(item.get("runtime_status")) == "completed" for item in summary_rows), f"completed={sum(str(item.get('runtime_status')) == 'completed' for item in summary_rows)}/{len(summary_rows)}", "runtime outputs completed", "MT5 telemetry(런타임 기록)가 실제로 생성됐는지 확인한다."),
        row("ce_gate_proxy_mt5_no_mismatch", mismatches == 0 and bool(diff_rows), f"mismatches={mismatches};diff_rows={len(diff_rows)}", "zero mismatches", "proxy expected(프록시 예상)와 MT5 runtime(런타임)이 같은 신호인지 확인한다."),
        row("ce_gate_no_forward_or_goal_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim", "런타임 탐침만 닫고 Forward/Goal(전진/목표)은 주장하지 않는다."),
    ]


def build_identity_rows(attempts: Sequence[Mapping[str, Any]], sync_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    columns = bv.IDENTITY_COLUMNS
    rows: list[dict[str, Any]] = []
    static_paths = [
        ("ea_source", bv.EA_SOURCE, "EA source(전문가 자문 원천)"),
        ("ea_binary", bv.EA_BINARY, "EA binary(전문가 자문 실행 파일)"),
        ("parent_package", PARENT_PACKAGE, "CD MT5 probe package(CD MT5 탐침 패키지)"),
        ("parent_proxy_expected", PARENT_PROXY_EXPECTED, "CD proxy expected(CD 프록시 예상)"),
    ]
    for artifact_id, path, role in static_paths:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "exists": path_exists(path),
                "sha256": mt5.sha256_file(path) if path_exists(path) and io_path(path).is_file() else "",
                "role": role,
                "status": "present" if path_exists(path) else "missing",
                "effect": "runtime identity(런타임 정체성)를 고정해 결과 해석이 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for attempt in attempts:
        for artifact_id, key, role in (
            ("feature_copy", "feature_local_path", "feature CSV(피처 CSV)"),
            ("model_copy", "model_local_path", "ONNX model(온엑스 모델)"),
            ("set_file", "set_path", "tester set(테스터 설정)"),
            ("ini_file", "ini_path", "tester ini(테스터 초기화)"),
        ):
            path = ROOT / str(attempt.get(key, ""))
            rows.append(
                {
                    "artifact_id": f"{attempt['attempt_name']}::{artifact_id}",
                    "artifact_type": path.suffix.lstrip(".") or "file",
                    "path": rel(path),
                    "exists": path_exists(path),
                    "sha256": mt5.sha256_file(path) if path_exists(path) and io_path(path).is_file() else "",
                    "role": role,
                    "status": "present" if path_exists(path) else "missing",
                    "effect": "attempt identity(시도 정체성)를 고정한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    for item in sync_rows:
        rows.append({column: item.get(column, "") for column in columns})
    return rows


def lifecycle_rows() -> list[dict[str, str]]:
    with io_path(PARENT_LIFECYCLE_SCORECARD).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_report(final: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]]) -> Path:
    runtime_lines = "\n".join(
        "| `{model}` | `{feature}` | `{status}` | {ready} | {matched} | {diff} | `{last}` | {trades} | {net} |".format(
            model=row.get("model_id", ""),
            feature=row.get("feature_set_id", ""),
            status=row.get("comparison_status", ""),
            ready=row.get("ready_model_rows", ""),
            matched=row.get("matched_rows", ""),
            diff=row.get("max_abs_probability_diff", ""),
            last=row.get("feature_last_reached", ""),
            trades=row.get("trade_count", ""),
            net=row.get("net_profit", ""),
        )
        for row in summary_rows
    )
    life_lines = "\n".join(
        f"| `{row['model_id']}` | {row['closed_trade_events']} | {row['net_log_return_cost1']} | {row['profit_factor_cost1']} | {row['net_log_return_cost2']} | `{row['cost2_guard_status']}` |"
        for row in lifecycle_rows()
    )
    return write_md(
        REPORT_PATH,
        f"""# Stage337 run337CE Lifecycle-Aware MT5 Runtime Probe(생애주기 인식 MT5 런타임 탐침)

## Conclusion(결론)

run337CE(337CE 실행)는 run337CD(337CD 실행)의 cost2-aware ONNX scout(비용2 인식 온엑스 스카우트)를 MT5 RuntimeProbeEA(MT5 런타임 탐침 EA)로 실행하고 proxy expected(프록시 예상)와 MT5 telemetry(MT5 기록)를 비교했다.

Effect(효과): runtime parity(런타임 동등성) 범위와 tester gap(테스터 공백)을 분리한다. 이 결과는 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- feature_last_reached_rows(피처 끝 도달 행): `{final['feature_last_reached_rows']}`
- parent_cost2_survivors(부모 비용2 생존): `{final['parent_cost2_survivors']}`

## Runtime Summary(런타임 요약)

| model(모델) | feature_set(피처 세트) | status(상태) | ready(준비) | matched(일치) | max diff(최대 차이) | feature last(피처 끝) | trades(거래) | net(순익) |
|---|---|---|---:|---:|---:|---|---:|---:|
{runtime_lines}

## CD Lifecycle Proxy(CD 생애주기 프록시)

| model(모델) | closed events(닫힌 이벤트) | net cost1(비용1 순수익) | PF cost1(비용1 수익 팩터) | net cost2(비용2 순수익) | cost2 guard(비용2 가드) |
|---|---:|---:|---:|---:|---|
{life_lines}

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337CE Lifecycle-Aware MT5 Runtime Probe(결정: 생애주기 인식 MT5 런타임 탐침)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): CD proxy expected(CD 프록시 예상)와 MT5 telemetry(MT5 기록)의 동등성은 비교했지만, cost2 proxy guard(비용2 프록시 가드)가 부모 단계에서 실패했기 때문에 다음은 runtime gap/failure attribution(런타임 공백/실패 귀속)이다. 후보 선택이나 운영 가능 주장이 아니다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def build_receipts(final: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(1 for row in summary_rows if str(row.get("runtime_status")) == "completed")
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "hypothesis": "CD cost2-aware ONNX outputs should match MT5 telemetry under fixed feature order and fixed threshold.",
                "controls": "no model training, no threshold tuning, no lot optimization, no candidate selection",
                "stop_condition": "proxy/MT5 mismatch or missing telemetry blocks runtime parity claim",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": "run337BQ feature CSVs and run337CD proxy expected outputs",
                "time_axis": "bar close timestamp exact comparison",
                "rows_compared": final["diff_rows"],
                "integrity_judgment": "usable_with_boundary" if completed else "blocked_or_inconclusive",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_subject": "run337CD lifecycle-aware cost2 ONNX scouts",
                "model_rows": final["attempt_rows"],
                "threshold_policy": "fixed_short040_long040_margin002",
                "selection_metric": "none",
                "validation_judgment": "runtime_probe_input_only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(PARENT_PROXY_EXPECTED),
                "runtime_path": rel(REPORT_PATH),
                "shared_contract": "feature order hash, feature input hash, probabilities, decision label, bar time",
                "known_differences": "MT5 telemetry says flat where Python proxy says no_trade",
                "parity_check": rel(PROXY_MT5_DIFF),
                "parity_identity": rel(RUNTIME_IDENTITY),
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            FORENSICS_RECEIPT,
            {
                "tester_identity": "portable MT5 Strategy Tester(전략 테스터), US100, M5, model 4(real ticks, 실제 틱), deposit 500, leverage 1:100",
                "ea_identity": rel(bv.EA_SOURCE),
                "report_identity": rel(REPORT_COPY_DIR),
                "trade_evidence": "strategy reports and telemetry summary when present",
                "cost_assumptions": "broker tester native spread/slippage, no extra modeled commission",
                "forensic_checks": ["tester returncode", "runtime summary", "strategy report artifact", "proxy/MT5 row diff"],
                "backtest_judgment": final["judgment"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)],
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "run artifacts local/ignored, reports and registers tracked",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(REPORT_PATH), rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF)],
                "evidence_missing": "operating review and Forward Passed/Failed decision remain out of scope",
                "judgment_label": final["judgment"],
                "next_condition": final["next_action"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = bv.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", final["next_action"])
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337CE focus complete: lifecycle-aware MT5 runtime probe(생애주기 인식 MT5 런타임 탐침)를 `{final['status']}`로 닫았다. "
        "Effect(효과): proxy-MT5 parity(프록시-MT5 동등성)와 cost2 failure attribution(비용2 실패 귀속)을 run337CF(337CF 실행)로 연다.\n"
    )
    if "Stage337 run337CE focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(bv.write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = bv.read_text_lossless(CURRENT_STATE)
    current = current_text
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = cd.replace_bullet_value(current, field_name, value)
    entry = f"""
## Stage337 run337CE(337CE 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): CD ONNX(온엑스)를 MT5 runtime probe(MT5 런타임 탐침)로 실행하고 proxy expected(프록시 예상)와 telemetry(기록)를 비교했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CE(337CE 실행)" not in current:
        marker = "## Stage337 run337CD(337CD"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(bv.write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `{final['actual_mt5_execution']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): 다음은 lifecycle-aware runtime probe review/failure attribution(생애주기 인식 런타임 탐침 리뷰/실패 귀속)이다.
"""
    artifacts.append(bv.write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = bv.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CE(337CE 실행) executed lifecycle-aware MT5 runtime probe(생애주기 인식 MT5 런타임 탐침). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(bv.write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = bv.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CE executed lifecycle-aware MT5 runtime probe(생애주기 인식 MT5 런타임 탐침) and opened `{final['next_action']}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(bv.write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "lifecycle_aware_mt5_runtime_probe_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};attempts={final['attempt_rows']};goal_achieve_not_claimed.",
        "family": "runtime_parity_backtest_forensics",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_aware_mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "lifecycle_aware_mt5_runtime_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_mt5_runtime_comparison",
        "tier_scope": "Tier A runtime probe; no operating claim",
        "kpi_scope": "runtime_parity_and_cost2_failure_attribution_input",
        "scoreboard_lane": "lifecycle_aware_runtime_probe",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"matched_rows={final['matched_rows']};cost2_survivors={final['parent_cost2_survivors']}",
        "guardrail_kpi": f"mismatch_rows={final['mismatch_rows']};forward_goal_not_claimed",
        "external_verification_status": final["actual_mt5_execution"],
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_aware_mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_backtest_forensics",
        "evidence_scope": "MT5 telemetry, strategy tester report, proxy-vs-MT5 diff, CD lifecycle scorecard",
        "kpi_scope": "runtime_probe_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"attempts={final['attempt_rows']};mismatch_rows={final['mismatch_rows']};cost2_survivors={final['parent_cost2_survivors']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__lifecycle_aware_mt5_runtime_probe",
        "family": "runtime_parity_backtest_forensics",
        "question": "do CD lifecycle-aware ONNX outputs match MT5 RuntimeProbeEA telemetry",
        "metric_scope": "runtime_parity_and_cost2_failure_attribution_input",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    generated = now_utc()
    new_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": mt5.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    args = parse_args()
    configure_runtime_helpers()
    for directory in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_COPY_DIR, FEATURE_COPY_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    parent, package_rows, proxy = bv.load_parent()
    pre_process = bv.terminal_processes()
    compile_result, ea_sync = bv.compile_and_sync_ea(Path(args.metaeditor_path), Path(args.terminal_data_root))
    attempts, sync_rows, attempt_artifacts = bv.materialize_attempts(package_rows, args)
    sync_rows = list(ea_sync) + sync_rows
    execution = bv.execute_attempts(attempts, args, compile_result)
    copied_runtime = bv.copy_runtime_outputs(Path(args.common_files_root), attempts)
    summary_rows, diff_rows, skip_rows = bv.compare_all(attempts, execution, proxy)
    status, judgment, decision, next_action = classify(summary_rows, bool(args.materialize_only), parent)
    gates = build_gates(parent, attempts, sync_rows, execution, summary_rows, diff_rows)
    mismatch_rows = sum(1 for row in diff_rows if row.get("comparison_status") != "matched")
    actual_mt5_execution = "attempted_strategy_tester" if any(row.get("tester_status") not in {"not_run_materialize_only", ""} for row in summary_rows) else "not_run_materialize_only"
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "attempt_rows": len(attempts),
        "summary_rows": len(summary_rows),
        "diff_rows": len(diff_rows),
        "matched_rows": sum(int(row.get("matched_rows") or 0) for row in summary_rows),
        "mismatch_rows": mismatch_rows,
        "runtime_completed_rows": sum(1 for row in summary_rows if str(row.get("runtime_status")) == "completed"),
        "feature_last_reached_rows": sum(1 for row in summary_rows if str(row.get("feature_last_reached")).lower() == "true"),
        "parent_cost2_survivors": int(parent.get("cost2_survivors", 0)),
        "actual_mt5_execution": actual_mt5_execution,
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }

    attempt_rows = [{column: attempt.get(column, "") for column in bv.ATTEMPT_COLUMNS} for attempt in attempts]
    artifacts: list[Path] = [
        write_csv(ATTEMPT_PACKAGE, bv.ATTEMPT_COLUMNS, attempt_rows),
        write_csv(COMMON_SYNC, bv.SYNC_COLUMNS, sync_rows),
        write_csv(EXECUTION_SUMMARY, bv.SUMMARY_COLUMNS, summary_rows),
        write_csv(PROXY_MT5_DIFF, bv.DIFF_COLUMNS, diff_rows),
        write_csv(TELEMETRY_SKIP_SUMMARY, ["attempt_name", "model_id", "skip_reason", "rows", "effect", "claim_boundary"], skip_rows),
        write_csv(RUNTIME_IDENTITY, bv.IDENTITY_COLUMNS, build_identity_rows(attempts, sync_rows)),
        write_json(
            TESTER_SETTINGS_IDENTITY,
            {
                "terminal_path": str(args.terminal_path),
                "terminal_data_root": str(args.terminal_data_root),
                "common_files_root": str(args.common_files_root),
                "tester_profile_root": str(args.tester_profile_root),
                "model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "from_date": "2026.04.14",
                "to_date": attempts[0].get("to_date", "") if attempts else "",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(TERMINAL_PROCESS_AUDIT, {"pre_run": pre_process, "post_run": bv.terminal_processes(), "claim_boundary": CLAIM_BOUNDARY}),
        write_json(MT5_EXECUTION_RESULT, execution),
        write_csv(REQUIRED_GATE_AUDIT, cd.GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(attempt_artifacts)
    artifacts.extend(copied_runtime)
    artifacts.extend(build_receipts(final, summary_rows))
    artifacts.append(write_report(final, summary_rows))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))

    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
