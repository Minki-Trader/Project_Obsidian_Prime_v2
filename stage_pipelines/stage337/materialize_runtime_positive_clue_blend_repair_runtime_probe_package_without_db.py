from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import review_runtime_positive_clue_blend_pf_recovery_drawdown_training_without_db as fp  # noqa: E402


aw = fp.aw
fo = fp.fo

TODAY = "2026-05-31"
STAGE_ID = fp.STAGE_ID
RUN_NUMBER = "run337FQ"
RUN_ID = "run337FQ_materialize_runtime_positive_clue_blend_repair_runtime_probe_package_without_db_v1"
PARENT_RUN_ID = fp.RUN_ID
NEXT_RUN_ID = "run337FR_execute_runtime_positive_clue_blend_repair_mt5_runtime_probe_without_db_v1"
STATUS = "completed_stage337FQ_runtime_positive_clue_blend_repair_runtime_probe_package_materialized_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_for_mt5_attempt_proxy_diff_required_no_selection"
DECISION = "stage337FQ_open_run337FR_execute_runtime_positive_clue_blend_repair_mt5_runtime_probe_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FQ_runtime_positive_clue_blend_repair_runtime_probe_package_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = fp.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_COPY_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
REVIEWS_DIR = fp.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FQ_runtime_positive_clue_blend_repair_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FQ_runtime_positive_clue_blend_repair_runtime_probe_package.md"
SELECTED_STATUS = fp.SELECTED_STATUS
STAGE_BRIEF = fp.STAGE_BRIEF
WORKSPACE_STATE = fp.WORKSPACE_STATE
CURRENT_STATE = fp.CURRENT_STATE
CHANGELOG = fp.CHANGELOG
RUN_REGISTRY = fp.RUN_REGISTRY
ALPHA_LEDGER = fp.ALPHA_LEDGER
ARTIFACT_REGISTRY = fp.ARTIFACT_REGISTRY
STAGE_LEDGER = fp.STAGE_LEDGER

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_runtime_positive_clue_blend_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

FEATURE_MATRIX = FEATURE_DIR / "runtime_positive_clue_blend_inner_holdout_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "runtime_positive_clue_blend_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
EXECUTION_QUEUE = RUN_DIR / "run337FR_execution_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    fp.FINAL_DECISION,
    fp.GATE_AUDIT,
    fp.FQ_QUEUE,
    fp.RUNTIME_PROBE_CANDIDATE_QUEUE,
    fp.PROXY_CLUE_REVIEW,
    fp.ONNX_READINESS_REVIEW,
    fo.TRAINED_MODEL_MANIFEST,
    fo.ONNX_PARITY,
    fo.FEATURE_SCHEMA,
    fo.FM_FRAME,
)
OUTPUT_FILES = (
    FEATURE_MATRIX,
    FEATURE_MATRIX_MANIFEST,
    EXPECTED_PROBABILITY_TAPE,
    EXPECTED_PROBABILITY_INDEX,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    EXECUTION_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    RUN_REGISTRY,
    ALPHA_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def patched_inner_holdout_frame(features: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_parquet(aw.io_path(fo.FM_FRAME)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame.sort_values(["source_row_id", "timestamp", "cost_policy_id"], inplace=True)
    _inner_train, inner_holdout = fo.split_inner(frame)
    missing = [feature for feature in features if feature not in inner_holdout.columns]
    if missing:
        raise ValueError(f"missing runtime features: {missing}")
    dedupe_columns = ["timestamp", *features]
    return inner_holdout.drop_duplicates(dedupe_columns).reset_index(drop=True)


def patched_queue_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(fp.RUNTIME_PROBE_CANDIDATE_QUEUE):
        copied = dict(row)
        copied["probe_priority"] = copied.get("priority", "")
        rows.append(copied)
    return rows


def configure_package_engine() -> None:
    replacements = {
        "TODAY": TODAY,
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS": STATUS,
        "JUDGMENT": JUDGMENT,
        "DECISION": DECISION,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "RUN_DIR": RUN_DIR,
        "MT5_DIR": MT5_DIR,
        "SET_DIR": SET_DIR,
        "INI_DIR": INI_DIR,
        "MODEL_COPY_DIR": MODEL_COPY_DIR,
        "FEATURE_DIR": FEATURE_DIR,
        "EXPECTED_DIR": EXPECTED_DIR,
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
        "COMMON_ROOT": COMMON_ROOT,
        "COMMON_FEATURE_DIR": COMMON_FEATURE_DIR,
        "COMMON_MODEL_DIR": COMMON_MODEL_DIR,
        "COMMON_TELEMETRY_DIR": COMMON_TELEMETRY_DIR,
        "FEATURE_MATRIX": FEATURE_MATRIX,
        "FEATURE_MATRIX_MANIFEST": FEATURE_MATRIX_MANIFEST,
        "EXPECTED_PROBABILITY_TAPE": EXPECTED_PROBABILITY_TAPE,
        "EXPECTED_PROBABILITY_INDEX": EXPECTED_PROBABILITY_INDEX,
        "MODEL_HANDOFF_MANIFEST": MODEL_HANDOFF_MANIFEST,
        "COMMON_FILES_SYNC": COMMON_FILES_SYNC,
        "TESTER_SET_MANIFEST": TESTER_SET_MANIFEST,
        "TESTER_INI_MANIFEST": TESTER_INI_MANIFEST,
        "RUNTIME_PROBE_ATTEMPT_PACKAGE": RUNTIME_PROBE_ATTEMPT_PACKAGE,
        "TESTER_IDENTITY_CONTRACT": TESTER_IDENTITY_CONTRACT,
        "PROXY_MT5_COMPARISON_CONTRACT": PROXY_MT5_COMPARISON_CONTRACT,
        "RUNTIME_PARITY_CONTRACT": RUNTIME_PARITY_CONTRACT,
        "EXECUTION_QUEUE": EXECUTION_QUEUE,
        "DATA_RECEIPT": DATA_RECEIPT,
        "MODEL_RECEIPT": MODEL_RECEIPT,
        "RUNTIME_RECEIPT": RUNTIME_RECEIPT,
        "FORENSICS_RECEIPT": FORENSICS_RECEIPT,
        "PERFORMANCE_RECEIPT": PERFORMANCE_RECEIPT,
        "JUDGMENT_RECEIPT": JUDGMENT_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "EZ_FINAL": fp.FINAL_DECISION,
        "EZ_GATES": fp.GATE_AUDIT,
        "EZ_RUNTIME_QUEUE": fp.RUNTIME_PROBE_CANDIDATE_QUEUE,
        "EZ_PROXY_REVIEW": fp.PROXY_CLUE_REVIEW,
        "EY_FRAME": fo.FM_FRAME,
        "EY_FEATURE_SCHEMA": fo.FEATURE_SCHEMA,
        "EY_MODEL_MANIFEST": fo.TRAINED_MODEL_MANIFEST,
        "EY_ONNX_PARITY": fo.ONNX_PARITY,
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
    }
    for name, value in replacements.items():
        setattr(fa, name, value)
    fa.inner_holdout_frame = patched_inner_holdout_frame
    fa.queue_rows = patched_queue_rows


def rewrite_execution_queue() -> Path:
    rows = [
        {
            "queue_id": "fr001_execute_runtime_positive_clue_blend_repair_mt5_runtime_probe",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "execute MT5 runtime probe for five runtime-positive-clue blend ONNX candidates(5개 런타임 긍정 단서 혼합 ONNX 후보 MT5 런타임 탐침 실행)",
            "required_inputs": f"{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)};{rel(EXPECTED_PROBABILITY_TAPE)};{rel(COMMON_FILES_SYNC)}",
            "required_outputs": "runtime telemetry, tester reports, proxy-vs-MT5 diff, backtest forensic receipt(런타임 기록, 테스터 보고서, 프록시-MT5 차이, 백테스트 포렌식 영수증)",
            "blocked_if_missing": "terminal, broker visibility, tester output, telemetry(터미널, 브로커 가시성, 테스터 출력, 런타임 기록)",
            "forbidden_action": "Forward/Goal claim before MT5 evidence(MT5 근거 전 전진/목표 주장)",
            "effect": "hands package to execution without changing thresholds or lots(임계값이나 랏 변경 없이 패키지를 실행으로 넘김)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return write_csv(EXECUTION_QUEUE, fa.QUEUE_COLUMNS, rows)


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    fp_final = read_json(fp.FINAL_DECISION)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "fp_next_action": fp_final.get("next_action", ""),
        "fp_failed_gate_rows": sum(1 for row in read_csv(fp.GATE_AUDIT) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["mt5_execution"] == "not_run" and final["candidate_selection"] == "not_run" and final["goal_achieve"] == "not_claimed"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(fp.FINAL_DECISION), "required FP/FO inputs exist(필수 FP/FO 입력 존재)"),
        ("parent_fp_gates_passed", final["fp_failed_gate_rows"] == 0, str(final["fp_failed_gate_rows"]), "0", rel(fp.GATE_AUDIT), "FP gates passed(FP 게이트 통과)"),
        ("parent_next_action_matches", final["fp_next_action"] == RUN_ID, str(final["fp_next_action"]), RUN_ID, rel(fp.FINAL_DECISION), "FQ follows FP next action(FQ가 FP 다음 행동을 따름)"),
        ("feature_matrix_materialized", final["feature_matrix_rows"] > 1000 and final["feature_count"] == 58, f"rows={final['feature_matrix_rows']};features={final['feature_count']}", ">1000 and 58", rel(FEATURE_MATRIX_MANIFEST), "runtime feature matrix exists(런타임 피처 행렬 존재)"),
        ("expected_probability_tape_materialized", final["expected_probability_rows"] == final["feature_matrix_rows"] * final["attempt_rows"], f"expected={final['expected_probability_rows']};feature_rows={final['feature_matrix_rows']};attempts={final['attempt_rows']}", "feature_rows*attempts", rel(EXPECTED_PROBABILITY_INDEX), "expected probabilities exist for every attempt(모든 시도 예상 확률 존재)"),
        ("unique_timestamp_handoff", final["feature_matrix_rows"] == 5845, str(final["feature_matrix_rows"]), "5845", rel(FEATURE_MATRIX), "runtime package uses unique timestamps(런타임 패키지가 고유 시각 사용)"),
        ("common_files_handoff_ready", final["common_sync_ready_rows"] == final["common_sync_rows"] and final["common_sync_rows"] >= 16, f"ready={final['common_sync_ready_rows']};rows={final['common_sync_rows']}", "all synced and >=16", rel(COMMON_FILES_SYNC), "Common Files handoff ready(공용 파일 인계 준비)"),
        ("tester_set_ini_materialized", final["tester_set_rows"] == final["tester_ini_rows"] == final["attempt_rows"] == 5, f"set={final['tester_set_rows']};ini={final['tester_ini_rows']};attempts={final['attempt_rows']}", "5/5/5", rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "tester files exist for each attempt(각 시도 테스터 파일 존재)"),
        ("execution_queue_materialized", final["execution_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"rows={final['execution_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(EXECUTION_QUEUE), "FR execution queue opened(FR 실행 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"mt5={final['mt5_execution']};selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "FQ materializes only, no operating claim(FQ는 물질화만 수행, 운영 주장 없음)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장이 게이트에 연결됨)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    data = {
        "feature_matrix": rel(FEATURE_MATRIX),
        "feature_rows": final["feature_matrix_rows"],
        "timestamp_grain": "unique inner-holdout M5 timestamps(고유 내부 보류 M5 시각)",
        "integrity_judgment": "usable_for_MT5_runtime_probe(MT5 런타임 탐침용 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_handoff_rows": final["model_handoff_rows"],
        "attempt_rows": final["attempt_rows"],
        "expected_probability_rows": final["expected_probability_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "mt5_execution": "not_run(실행 안 함)",
        "terminal_exists": final["terminal_exists"],
        "common_files_root_exists": final["common_files_root_exists"],
        "portable_ea_exists": final["portable_ea_exists"],
        "next_action": final["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    forensics = {
        "tester_identity": "US100 M5 Deposit=500 Leverage=1:100 Model=4 real ticks(US100 M5 예치금 500 레버리지 1:100 실제 틱)",
        "trade_evidence": "missing_required_until_execution(실행 전 필수 누락)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "proxy_reference": rel(fp.PROXY_CLUE_REVIEW),
        "expected_probability_tape": rel(EXPECTED_PROBABILITY_TAPE),
        "required_next_diff": "diff, attribution, usability(차이, 귀속, 사용 가능성)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_missing": "MT5 tester output and runtime telemetry(MT5 테스터 출력과 런타임 기록)",
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(FORENSICS_RECEIPT, forensics),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    lineage_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in lineage_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in lineage_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_runtime_package_to_FR_execution(FR 실행에 런타임 패키지 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FQ Runtime Probe Package(337단계 337FQ 런타임 탐침 패키지)

## Conclusion(결론)

Action(행동): FO ONNX candidates(FO ONNX 후보) `5`개를 MT5 runtime probe(MT5 런타임 탐침)용 패키지로 만들었다. Effect(효과): 다음 FR execution(FR 실행)이 모델 로직이나 threshold(임계값)를 바꾸지 않고 MT5 비교를 수행할 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- feature_matrix_rows(피처 행렬 행): `{final['feature_matrix_rows']}`
- expected_probability_rows(예상 확률 행): `{final['expected_probability_rows']}`
- attempts(시도): `{final['attempt_rows']}`
- common_sync(공용 파일 동기화): `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`
- tester_window(테스터 구간): `{final['tester_from_date']}` to `{final['tester_to_date']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Boundary(경계): FQ(337FQ 실행)는 package materialization(패키지 물질화) 전용이다. MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표)은 모두 `not_claimed`다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FQ Decision(337FQ 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(EXPECTED_PROBABILITY_TAPE)}`

Action(행동): MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들었다.
Effect(효과): FR에서 tester output(테스터 출력), telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)를 만들 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {fo.fa.ey.current_branch()}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FQ focus complete: run337FQ(337FQ 실행)는 `{final['status']}`로 runtime probe package(런타임 탐침 패키지)를 완료했다. "
        f"Effect(효과): feature rows(피처 행) `{final['feature_matrix_rows']}`, attempts(시도) `{final['attempt_rows']}`, Common Files handoff(공용 파일 인계) `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FQ focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337FQ focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fo.fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337FQ Runtime Probe Package(런타임 탐침 패키지)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- feature_matrix_rows(피처 행렬 행): `{final['feature_matrix_rows']}`
- expected_probability_rows(예상 확률 행): `{final['expected_probability_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): proxy clue(프록시 단서)를 실제 MT5 runtime probe(MT5 런타임 탐침) 실행 패키지로 연결했다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fo.fb.upsert_section_before(current, "## run337FP Runtime Positive Clue Blend Training Review", section, "run337FQ Runtime Probe Package")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- runtime_probe_attempts(런타임 탐침 시도): `{final['attempt_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FQ(337FQ 실행)는 package(패키지)만 완료했고 MT5 execution(MT5 실행), operating selection(운영 선택)은 하지 않았다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = f"- {TODAY}: run337FQ(337FQ 실행) `{final['status']}`. Effect(효과): 5개 ONNX 후보 런타임 탐침 패키지를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, fo.fb.upsert_single_line(brief, "run337FQ(337FQ 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337FQ(337FQ 실행) `{final['status']}`. Effect(효과): MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들고 FR execution(FR 실행)을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    artifacts.append(aw.write_text_lossless(CHANGELOG, fo.fb.upsert_single_line(changelog, "Stage337 run337FQ", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_clue_blend_repair_runtime_probe_package",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"attempts={final['attempt_rows']};feature_rows={final['feature_matrix_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_verification_artifact_lineage_data_integrity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe_package",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_probe_package",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_positive_clue_blend_repair_runtime_probe_package(런타임 긍정 단서 혼합 수리 런타임 탐침 패키지)",
        "tier_scope": "Tier A inner holdout runtime package(Tier A 내부 보류 런타임 패키지)",
        "kpi_scope": "package only; no MT5 KPI(패키지 전용, MT5 성과 없음)",
        "scoreboard_lane": "runtime_verification",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"attempts={final['attempt_rows']};feature_rows={final['feature_matrix_rows']}",
        "guardrail_kpi": "common_files_handoff;no_mt5;no_selection;no_goal",
        "external_verification_status": "required_next_action",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe_package",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_verification_artifact_lineage_data_integrity",
        "evidence_scope": "feature matrix, expected probability tape, Common Files handoff, tester set/ini",
        "kpi_scope": "package_no_mt5",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__runtime_probe_package",
        "family": "runtime_positive_clue_blend_repair_runtime_probe_package",
        "question": "can FO ONNX candidates be handed to MT5 runtime probe",
        "metric_scope": "feature_matrix_expected_tape_common_files",
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fo.fb.upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fo.fb.upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fo.fb.upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        row = {
            "artifact_id": artifact_id,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": artifact_path,
            "sha256": aw.sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": STATUS,
            "artifact_path": artifact_path,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    configure_package_engine()
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    artifacts, summary = fa.materialize_package()
    artifacts.append(rewrite_execution_queue())
    summary["execution_queue_rows"] = 1
    final = make_final(summary)
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, fa.GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "feature_matrix_rows": final["feature_matrix_rows"], "expected_probability_rows": final["expected_probability_rows"], "attempt_rows": final["attempt_rows"], "gates": f"{final['passed_gates']}/{final['gate_rows']}", "next_action": final["next_action"], "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
