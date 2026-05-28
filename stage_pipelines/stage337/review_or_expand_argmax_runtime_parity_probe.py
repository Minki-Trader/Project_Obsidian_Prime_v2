from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import materialize_common_files_and_run_argmax_parity_probe as el  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = el.STAGE_ID
RUN_NUMBER = "run337EM"
RUN_ID = "run337EM_review_or_expand_argmax_runtime_parity_probe_without_db_v1"
PARENT_RUN_ID = el.RUN_ID
NEXT_RUN_ID = "run337EN_surface_degeneracy_memory_or_full_survivor_runtime_probe_without_db_v1"
STATUS_EXECUTED = "completed_stage337EM_argmax_runtime_parity_expanded_direction_pocket_probe_no_selection"
STATUS_BLOCKED = "blocked_stage337EM_argmax_runtime_parity_expansion_handoff_or_terminal_issue_no_selection"
JUDGMENT_EXECUTED = "runtime_probe_direction_pocket_parity_executed_but_forward_and_runtime_authority_not_claimed"
JUDGMENT_BLOCKED = "runtime_probe_expansion_not_sufficient_for_parity_judgment_repair_required"
DECISION_EXECUTED = "stage337EM_open_run337EN_surface_degeneracy_memory_or_full_survivor_runtime_probe"
DECISION_BLOCKED = "stage337EM_open_run337EN_repair_argmax_runtime_parity_expansion"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EM_argmax_runtime_parity_expansion_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = el.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REPORT_COPY_DIR = MT5_DIR / "reports"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = el.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EM_argmax_runtime_parity_expansion.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EM_argmax_runtime_parity_expansion.md"
SELECTED_STATUS = el.SELECTED_STATUS
STAGE_BRIEF = el.STAGE_BRIEF
WORKSPACE_STATE = el.WORKSPACE_STATE
CURRENT_STATE = el.CURRENT_STATE
CHANGELOG = el.CHANGELOG
RUN_REGISTRY = el.RUN_REGISTRY
ALPHA_LEDGER = el.ALPHA_LEDGER
ARTIFACT_REGISTRY = el.ARTIFACT_REGISTRY
STAGE_LEDGER = el.STAGE_LEDGER

EL_FINAL = el.FINAL_DECISION
EL_SUMMARY = el.EXECUTION_SUMMARY
EL_DIFF = el.RUNTIME_DIFF

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_argmax_runtime_parity_expansion"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

ATTEMPT_PACKAGE = RUN_DIR / "argmax_runtime_probe_attempt_package.csv"
COMMON_SYNC = RUN_DIR / "common_files_sync.csv"
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
EXECUTION_SUMMARY = RUN_DIR / "argmax_runtime_probe_execution_summary.csv"
RUNTIME_DIFF = RUN_DIR / "runtime_probability_decision_diff.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
TESTER_SETTINGS_IDENTITY = RUN_DIR / "tester_settings_identity.json"
EL_REVIEW = RUN_DIR / "parent_run337EL_review.csv"
EXPECTED_SURFACE_SCAN = RUN_DIR / "expected_surface_scan.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EL_FINAL,
    EL_SUMMARY,
    EL_DIFF,
    el.EK_FINAL,
    el.EK_GATES,
    el.EJ_ADAPTER_PROBE_MANIFEST,
    el.EH_FEATURE_HANDOFF,
    el.EG_PACKAGE_PRECHECK,
    ROOT / mt5.EA_SOURCE_PATH,
)
OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    COMMON_SYNC,
    EXPECTED_TAPE_INDEX,
    EXECUTION_RESULT,
    EXECUTION_SUMMARY,
    RUNTIME_DIFF,
    TERMINAL_PROCESS_AUDIT,
    RUNTIME_IDENTITY,
    TESTER_SETTINGS_IDENTITY,
    EL_REVIEW,
    EXPECTED_SURFACE_SCAN,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

EL_REVIEW_COLUMNS = (
    "source_run_id",
    "status",
    "attempt_rows",
    "ready_model_rows",
    "matched_rows",
    "probability_mismatch_rows",
    "decision_mismatch_rows",
    "diff_rows",
    "expected_nonflat_rows",
    "runtime_nonflat_rows",
    "finding",
    "effect",
    "claim_boundary",
)
SCAN_COLUMNS = (
    "scan_id",
    "rank",
    "attempt_name",
    "model_id",
    "from_date",
    "to_date",
    "rows",
    "decision_short",
    "decision_long",
    "decision_flat",
    "decision_nonflat",
    "first_nonflat_time",
    "last_nonflat_time",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337EM review or expand argmax runtime parity probe.")
    parser.add_argument("--terminal-path", default=str(el.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(el.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(el.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--attempt-limit", type=int, default=7)
    parser.add_argument("--scan-limit", type=int, default=7)
    parser.add_argument("--latest-from-date", default="2026.04.10")
    parser.add_argument("--latest-to-date", default="2026.04.14")
    parser.add_argument("--from-date", default="2026.04.08")
    parser.add_argument("--to-date", default="2026.04.10")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--wait-timeout-seconds", type=int, default=90)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


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


def write_local_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def configure_el_engine() -> None:
    el.RUN_NUMBER = RUN_NUMBER
    el.RUN_ID = RUN_ID
    el.PARENT_RUN_ID = PARENT_RUN_ID
    el.NEXT_RUN_ID = NEXT_RUN_ID
    el.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    el.RUN_DIR = RUN_DIR
    el.MT5_DIR = MT5_DIR
    el.SET_DIR = SET_DIR
    el.INI_DIR = INI_DIR
    el.REPORT_COPY_DIR = REPORT_COPY_DIR
    el.MODEL_DIR = MODEL_DIR
    el.FEATURE_DIR = FEATURE_DIR
    el.EXPECTED_DIR = EXPECTED_DIR
    el.TELEMETRY_DIR = TELEMETRY_DIR
    el.COMMON_ROOT = COMMON_ROOT
    el.COMMON_MODEL_DIR = COMMON_MODEL_DIR
    el.COMMON_FEATURE_DIR = COMMON_FEATURE_DIR
    el.COMMON_TELEMETRY_DIR = COMMON_TELEMETRY_DIR
    el.ATTEMPT_PACKAGE = ATTEMPT_PACKAGE
    el.COMMON_SYNC = COMMON_SYNC
    el.EXPECTED_TAPE_INDEX = EXPECTED_TAPE_INDEX
    el.EXECUTION_RESULT = EXECUTION_RESULT
    el.EXECUTION_SUMMARY = EXECUTION_SUMMARY
    el.RUNTIME_DIFF = RUNTIME_DIFF
    el.TERMINAL_PROCESS_AUDIT = TERMINAL_PROCESS_AUDIT
    el.RUNTIME_IDENTITY = RUNTIME_IDENTITY
    el.TESTER_SETTINGS_IDENTITY = TESTER_SETTINGS_IDENTITY
    el.REQUIRED_GATE_AUDIT = REQUIRED_GATE_AUDIT
    el.FINAL_DECISION = FINAL_DECISION
    el.RUN_MANIFEST = RUN_MANIFEST


def review_parent_el() -> list[dict[str, Any]]:
    final = read_json(EL_FINAL)
    diff_rows = read_csv(EL_DIFF)
    expected_nonflat = sum(1 for row in diff_rows if row.get("expected_decision") in {"short", "long"})
    runtime_nonflat = sum(1 for row in diff_rows if row.get("mt5_decision") in {"short", "long"})
    row = {
        "source_run_id": final.get("run_id", PARENT_RUN_ID),
        "status": final.get("status", ""),
        "attempt_rows": final.get("attempt_rows", ""),
        "ready_model_rows": final.get("ready_model_rows", ""),
        "matched_rows": final.get("matched_rows", ""),
        "probability_mismatch_rows": final.get("probability_mismatch_rows", ""),
        "decision_mismatch_rows": final.get("decision_mismatch_rows", ""),
        "diff_rows": final.get("diff_rows", ""),
        "expected_nonflat_rows": expected_nonflat,
        "runtime_nonflat_rows": runtime_nonflat,
        "finding": "parent_probe_matched_but_all_ready_rows_flat",
        "effect": "EM expands into a direction-pocket window instead of claiming runtime authority(EM은 런타임 권위를 주장하지 않고 방향 포켓 구간으로 확장)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [row]


def scan_expected_surface(scan_id: str, from_date: str, to_date: str, limit: int) -> list[dict[str, Any]]:
    feature_contracts = el.load_feature_contracts()
    rows: list[dict[str, Any]] = []
    for attempt in el.selected_attempts(limit):
        feature_row = feature_contracts[str(attempt["feature_set_id"])]
        feature_order = json.loads(str(feature_row["included_features_json"]))
        source = ROOT / str(feature_row["source_model_input"])
        frame = el.date_filter(pd.read_parquet(io_path(source)), from_date, to_date)
        if frame.empty:
            rows.append(
                {
                    "scan_id": scan_id,
                    "rank": attempt["proxy_rank"],
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt["model_id"],
                    "from_date": from_date,
                    "to_date": to_date,
                    "rows": 0,
                    "decision_short": 0,
                    "decision_long": 0,
                    "decision_flat": 0,
                    "decision_nonflat": 0,
                    "first_nonflat_time": "",
                    "last_nonflat_time": "",
                    "effect": "no rows in scan window(스캔 구간 행 없음)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        model = joblib.load(io_path(Path(str(attempt["model_path"]))))
        matrix = frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
        probs = el.ordered_probabilities(model, matrix)
        decisions = np.asarray(["short", "flat", "long"], dtype=object)[probs.argmax(axis=1)]
        nonflat = decisions != "flat"
        timestamps = pd.to_datetime(frame["timestamp"], utc=True)
        rows.append(
            {
                "scan_id": scan_id,
                "rank": attempt["proxy_rank"],
                "attempt_name": attempt["attempt_name"],
                "model_id": attempt["model_id"],
                "from_date": from_date,
                "to_date": to_date,
                "rows": int(len(decisions)),
                "decision_short": int((decisions == "short").sum()),
                "decision_long": int((decisions == "long").sum()),
                "decision_flat": int((decisions == "flat").sum()),
                "decision_nonflat": int(nonflat.sum()),
                "first_nonflat_time": timestamps[nonflat].min().strftime("%Y.%m.%d %H:%M:%S") if nonflat.any() else "",
                "last_nonflat_time": timestamps[nonflat].max().strftime("%Y.%m.%d %H:%M:%S") if nonflat.any() else "",
                "effect": "expected decision surface scanned before MT5(예상 결정 표면을 MT5 전에 스캔)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def terminal_process_audit() -> dict[str, Any]:
    return el.terminal_process_audit()


def count_nonflat_diff(diff_rows: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    expected_nonflat = [row for row in diff_rows if row.get("expected_decision") in {"short", "long"}]
    matched_nonflat = [
        row
        for row in expected_nonflat
        if str(row.get("comparison_status")) == "matched" and str(row.get("decision_match")).lower() == "true"
    ]
    return {
        "runtime_expected_nonflat_rows": len(expected_nonflat),
        "runtime_matched_nonflat_rows": len(matched_nonflat),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    parent = read_json(EL_FINAL)
    gates = [
        ("input_presence", final["missing_inputs"] == 0, final["missing_inputs"], "0", "EM 입력이 모두 있어야 한다."),
        (
            "parent_el_next_action_matches",
            parent.get("next_action") == RUN_ID,
            parent.get("next_action", ""),
            RUN_ID,
            "부모 EL이 EM으로 이어져야 한다.",
        ),
        (
            "latest_surface_reviewed",
            final["latest_scan_rows"] > 0,
            final["latest_scan_rows"],
            ">0",
            "최신 표면을 먼저 읽어야 한다.",
        ),
        (
            "latest_surface_flat_named",
            final["latest_scan_nonflat_rows"] == 0,
            final["latest_scan_nonflat_rows"],
            "0",
            "최신 구간의 all-flat(전부 평탄) 현상을 이름 붙인다.",
        ),
        (
            "direction_probe_has_nonflat_expected",
            final["direction_scan_nonflat_rows"] > 0 and final["expected_probe_nonflat_rows"] > 0,
            f"scan={final['direction_scan_nonflat_rows']};probe={final['expected_probe_nonflat_rows']}",
            ">0",
            "확장 MT5 구간에는 방향 분기 행이 있어야 한다.",
        ),
        (
            "common_files_synced",
            final["common_sync_failed_rows"] == 0 and final["common_sync_rows"] >= 2,
            f"failed={final['common_sync_failed_rows']};rows={final['common_sync_rows']}",
            "failed=0;rows>=2",
            "Common Files 인계가 성공해야 한다.",
        ),
        (
            "runtime_probe_attempted",
            final["materialize_only"] == "true" or final["tester_attempt_rows"] >= 1,
            f"materialize_only={final['materialize_only']};tester_attempts={final['tester_attempt_rows']}",
            "materialize_only or attempts>=1",
            "터미널 탐침을 시도해야 한다.",
        ),
        (
            "telemetry_ready_or_blocker_named",
            final["ready_model_rows"] > 0 or final["blocked_attempt_rows"] > 0,
            f"ready={final['ready_model_rows']};blocked={final['blocked_attempt_rows']}",
            "ready>0 or blocked>0",
            "텔레메트리 준비 또는 차단 사유가 있어야 한다.",
        ),
        (
            "runtime_probability_decision_parity_clear_when_ready",
            final["ready_model_rows"] == 0
            or (final["probability_mismatch_rows"] == 0 and final["decision_mismatch_rows"] == 0),
            f"ready={final['ready_model_rows']};prob={final['probability_mismatch_rows']};decision={final['decision_mismatch_rows']}",
            "ready=0 or mismatches=0",
            "준비 행이 있으면 확률/결정 불일치가 없어야 한다.",
        ),
        (
            "nonflat_runtime_rows_matched_when_present",
            final["runtime_expected_nonflat_rows"] == 0
            or final["runtime_expected_nonflat_rows"] == final["runtime_matched_nonflat_rows"],
            f"expected={final['runtime_expected_nonflat_rows']};matched={final['runtime_matched_nonflat_rows']}",
            "all expected nonflat matched",
            "방향 분기 행이 있으면 MT5 결정도 맞아야 한다.",
        ),
        (
            "no_forbidden_claim",
            final["forward_passed"] == "not_claimed" and final["runtime_authority"] == "not_claimed",
            f"forward={final['forward_passed']};authority={final['runtime_authority']}",
            "not_claimed;not_claimed",
            "탐침을 운영 권위로 과장하지 않는다.",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in gates
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EM Argmax Runtime Parity Expansion(확장 런타임 동등성 탐침)

## Conclusion(결론)

run337EM(337EM 실행)는 run337EL(337EL 실행)을 검토한 뒤, 최신 구간 all-flat(전부 평탄) 현상을 따로 기록하고 방향 분기(non-flat, 비평탄)가 있는 2026.04.08~2026.04.10 구간으로 MT5 Strategy Tester(MT5 전략 테스터)를 확장했다.

Action(행동): parent EL(부모 EL) 결과를 검토하고, expected surface scan(예상 표면 스캔), Common Files handoff(공통 파일 인계), MT5 runtime probe(MT5 런타임 탐침), row-level probability/decision diff(행 단위 확률/결정 차이)를 기록했다.

Effect(효과): argmax probe mode(argmax 탐침 모드)의 방향 포켓 동등성은 좁게 검증하지만 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- attempt_rows(시도 행): `{final['attempt_rows']}`
- tester_attempt_rows(테스터 시도 행): `{final['tester_attempt_rows']}`
- ready_model_rows(준비 모델 행): `{final['ready_model_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- probability_mismatch_rows(확률 불일치 행): `{final['probability_mismatch_rows']}`
- decision_mismatch_rows(결정 불일치 행): `{final['decision_mismatch_rows']}`
- latest_scan_nonflat_rows(최신 스캔 비평탄 행): `{final['latest_scan_nonflat_rows']}`
- direction_scan_nonflat_rows(방향 스캔 비평탄 행): `{final['direction_scan_nonflat_rows']}`
- runtime_expected_nonflat_rows(런타임 예상 비평탄 행): `{final['runtime_expected_nonflat_rows']}`
- runtime_matched_nonflat_rows(런타임 일치 비평탄 행): `{final['runtime_matched_nonflat_rows']}`
- blocked_attempt_rows(차단 시도 행): `{final['blocked_attempt_rows']}`
- gates_passed(게이트 통과): `{final['passed_gates']}/{final['gate_rows']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EM

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): 최신 all-flat(전부 평탄) 표면을 차단 신호로 기록하고, 방향 포켓 MT5 parity(동등성)를 좁게 확장했다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(EXPECTED_SURFACE_SCAN)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(RUNTIME_DIFF)}`, `{rel(EXECUTION_RESULT)}`
- next_action(다음 행동): `{final['next_action']}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = workspace_text.replace(f"current_run_id: {RUN_ID}", f"current_run_id: {final['next_action']}", 1)
    workspace_text = workspace_text.replace("current_run_id: run337EM_review_or_expand_argmax_runtime_parity_probe_without_db_v1", f"current_run_id: {final['next_action']}", 1)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337EM focus complete: argmax runtime parity expansion(argmax 런타임 동등성 확장)을 실행했고 "
        f"runtime_expected_nonflat_rows(런타임 예상 비평탄 행) `{final['runtime_expected_nonflat_rows']}`, "
        f"runtime_matched_nonflat_rows(런타임 일치 비평탄 행) `{final['runtime_matched_nonflat_rows']}`를 기록했다. "
        "Effect(효과): 최신 all-flat(전부 평탄) 표면은 별도 실패 기억/확장 탐침으로 넘긴다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EM focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337EM(337EM 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): 최신 구간 all-flat(전부 평탄)을 확인하고 방향 포켓 runtime parity(런타임 동등성)를 확장했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EL("
    if "## Stage337 run337EM(337EM 실행)" not in current_text:
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- latest_surface_nonflat_rows(최신 표면 비평탄 행): `{final['latest_scan_nonflat_rows']}`
- runtime_expected_nonflat_rows(런타임 예상 비평탄 행): `{final['runtime_expected_nonflat_rows']}`
- runtime_matched_nonflat_rows(런타임 일치 비평탄 행): `{final['runtime_matched_nonflat_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): all-flat surface memory(전부 평탄 표면 기억)와 full survivor runtime probe(전체 생존 후보 런타임 탐침) 검토로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EM(337EM 실행) expanded argmax runtime parity probe(argmax 런타임 동등성 탐침). "
        f"Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EM(337EM 실행) expanded argmax"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EM expanded argmax runtime parity into a direction pocket and opened `{final['next_action']}` without Forward/Goal claims."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EM expanded argmax"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "argmax_runtime_parity_expansion_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"ready={final['ready_model_rows']};matched={final['matched_rows']};nonflat={final['runtime_matched_nonflat_rows']}/{final['runtime_expected_nonflat_rows']};next={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_parity_backtest_forensics_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__argmax_runtime_parity_expansion",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "argmax_runtime_parity_expansion",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_parity_probe_no_selection",
        "tier_scope": "tier_a_probe",
        "kpi_scope": "probability_decision_parity_not_profitability",
        "scoreboard_lane": "runtime_parity_result_judgment",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"ready={final['ready_model_rows']};matched={final['matched_rows']};nonflat={final['runtime_matched_nonflat_rows']}/{final['runtime_expected_nonflat_rows']}",
        "guardrail_kpi": "no_selection;no_forward;runtime_authority_not_claimed",
        "external_verification_status": "mt5_strategy_tester_attempted",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__argmax_runtime_parity_expansion",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_backtest_forensics_result_judgment",
        "evidence_scope": "EL review, expected surface scan, Common Files handoff, MT5 tester attempt, telemetry comparison",
        "kpi_scope": "runtime_probability_decision_parity",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__argmax_runtime_parity_expansion",
        "family": "runtime_parity_backtest_forensics_result_judgment",
        "question": "does argmax probe mode reproduce Python meaning when non-flat rows exist",
        "metric_scope": "telemetry_probability_decision_diff",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]

    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
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
                "notes": "Stage337EM argmax runtime parity expansion artifact; no Forward/Goal claims.",
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_local_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    configure_el_engine()
    args = parse_args()
    for directory in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, REPORT_COPY_DIR, MODEL_DIR, FEATURE_DIR, EXPECTED_DIR, TELEMETRY_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    parent_review = review_parent_el()
    latest_scan = scan_expected_surface("latest_surface", args.latest_from_date, args.latest_to_date, args.scan_limit)
    direction_scan = scan_expected_surface("direction_probe_surface", args.from_date, args.to_date, args.scan_limit)
    scan_rows = [*latest_scan, *direction_scan]
    write_local_csv(EL_REVIEW, EL_REVIEW_COLUMNS, parent_review)
    write_local_csv(EXPECTED_SURFACE_SCAN, SCAN_COLUMNS, scan_rows)

    process_audit = terminal_process_audit()
    write_json(TERMINAL_PROCESS_AUDIT, process_audit)
    attempts, sync_rows, expected_index = el.materialize_attempts(args)
    write_local_csv(ATTEMPT_PACKAGE, el.ATTEMPT_COLUMNS, attempts)
    write_local_csv(COMMON_SYNC, el.SYNC_COLUMNS, sync_rows)
    write_local_csv(EXPECTED_TAPE_INDEX, el.EXPECTED_INDEX_COLUMNS, expected_index)
    execution_results, summary_rows, diff_rows = el.run_attempts(args, attempts)
    write_json(EXECUTION_RESULT, {"run_id": RUN_ID, "execution_results": execution_results})
    write_local_csv(EXECUTION_SUMMARY, el.SUMMARY_COLUMNS, summary_rows)
    write_local_csv(RUNTIME_DIFF, el.DIFF_COLUMNS, diff_rows)

    identity = el.identity_rows(
        [
            ("terminal64", "executable", Path(args.terminal_path), "MT5 terminal identity(MT5 터미널 정체성)"),
            ("runtime_ea_source", "mq5", ROOT / mt5.EA_SOURCE_PATH, "EA source(EA 원천)"),
            ("runtime_ea_binary", "ex5", ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5", "EA binary(EA 바이너리)"),
            ("attempt_package", "csv", ATTEMPT_PACKAGE, "attempt package(시도 패키지)"),
            ("execution_summary", "csv", EXECUTION_SUMMARY, "execution summary(실행 요약)"),
        ]
    )
    write_local_csv(RUNTIME_IDENTITY, el.IDENTITY_COLUMNS, identity)
    write_json(
        TESTER_SETTINGS_IDENTITY,
        {
            "run_id": RUN_ID,
            "terminal_path": args.terminal_path,
            "common_files_root": args.common_files_root,
            "tester_profile_root": args.tester_profile_root,
            "latest_from_date": args.latest_from_date,
            "latest_to_date": args.latest_to_date,
            "from_date": args.from_date,
            "to_date": args.to_date,
            "attempt_limit": args.attempt_limit,
            "scan_limit": args.scan_limit,
            "materialize_only": args.materialize_only,
        },
    )

    ready_model_rows = sum(int(row.get("ready_model_rows") or 0) for row in summary_rows)
    matched_rows = sum(int(row.get("matched_rows") or 0) for row in summary_rows)
    probability_mismatch_rows = sum(int(row.get("probability_mismatch_rows") or 0) for row in summary_rows)
    decision_mismatch_rows = sum(int(row.get("decision_mismatch_rows") or 0) for row in summary_rows)
    blocked_attempt_rows = sum(1 for row in summary_rows if str(row.get("runtime_status", "")).startswith("blocked") or str(row.get("comparison_status", "")).startswith("blocked"))
    nonflat_counts = count_nonflat_diff(diff_rows)
    latest_scan_nonflat = sum(int(row["decision_nonflat"]) for row in latest_scan)
    direction_scan_nonflat = sum(int(row["decision_nonflat"]) for row in direction_scan)
    expected_probe_nonflat = sum(int(row["decision_short"]) + int(row["decision_long"]) for row in expected_index)
    status = STATUS_EXECUTED if ready_model_rows > 0 else STATUS_BLOCKED
    judgment = JUDGMENT_EXECUTED if ready_model_rows > 0 else JUDGMENT_BLOCKED
    decision = DECISION_EXECUTED if ready_model_rows > 0 else DECISION_BLOCKED
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(missing),
        "materialize_only": str(args.materialize_only).lower(),
        "terminal_process_status": process_audit["status"],
        "latest_scan_rows": len(latest_scan),
        "latest_scan_nonflat_rows": latest_scan_nonflat,
        "direction_scan_rows": len(direction_scan),
        "direction_scan_nonflat_rows": direction_scan_nonflat,
        "attempt_rows": len(attempts),
        "common_sync_rows": len(sync_rows),
        "common_sync_failed_rows": sum(1 for row in sync_rows if row["status"] != "copied"),
        "expected_probability_tape_rows": sum(int(row["rows"]) for row in expected_index),
        "expected_probe_nonflat_rows": expected_probe_nonflat,
        "tester_attempt_rows": len(execution_results),
        "summary_rows": len(summary_rows),
        "diff_rows": len(diff_rows),
        "ready_model_rows": ready_model_rows,
        "matched_rows": matched_rows,
        "probability_mismatch_rows": probability_mismatch_rows,
        "decision_mismatch_rows": decision_mismatch_rows,
        "blocked_attempt_rows": blocked_attempt_rows,
        **nonflat_counts,
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates)
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY})
    receipts = [
        write_json(DATA_RECEIPT, {"run_id": RUN_ID, "status": "completed", "latest_scan_nonflat_rows": latest_scan_nonflat, "direction_scan_nonflat_rows": direction_scan_nonflat, "claim_boundary": CLAIM_BOUNDARY}),
        write_json(MODEL_RECEIPT, {"run_id": RUN_ID, "model_training": "not_run", "expected_probability_tape_rows": final["expected_probability_tape_rows"], "expected_probe_nonflat_rows": expected_probe_nonflat, "claim_boundary": CLAIM_BOUNDARY}),
        write_json(RUNTIME_RECEIPT, {"run_id": RUN_ID, "runtime_probe_execution": "attempted", "ready_model_rows": ready_model_rows, "runtime_matched_nonflat_rows": final["runtime_matched_nonflat_rows"], "claim_boundary": CLAIM_BOUNDARY}),
        write_json(FORENSICS_RECEIPT, {"run_id": RUN_ID, "tester_settings": rel(TESTER_SETTINGS_IDENTITY), "execution_result": rel(EXECUTION_RESULT), "claim_boundary": CLAIM_BOUNDARY}),
        write_json(JUDGMENT_RECEIPT, {"run_id": RUN_ID, "judgment_label": "runtime_probe" if ready_model_rows > 0 else "blocked", "claim_boundary": CLAIM_BOUNDARY}),
        write_json(LINEAGE_RECEIPT, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    tracked = [write_report(final), write_decision_doc(final)]
    tracked.extend(update_docs(final))
    tracked.extend(update_registers([*OUTPUT_FILES, *receipts, *tracked], final))
    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"], "ready_model_rows": ready_model_rows}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "attempt_rows": len(attempts),
                "ready_model_rows": ready_model_rows,
                "matched_rows": matched_rows,
                "runtime_expected_nonflat_rows": final["runtime_expected_nonflat_rows"],
                "runtime_matched_nonflat_rows": final["runtime_matched_nonflat_rows"],
                "probability_mismatch_rows": probability_mismatch_rows,
                "decision_mismatch_rows": decision_mismatch_rows,
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
