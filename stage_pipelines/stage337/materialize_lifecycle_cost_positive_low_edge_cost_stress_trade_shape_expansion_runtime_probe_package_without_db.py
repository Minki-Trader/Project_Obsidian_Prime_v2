from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    materialize_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_runtime_probe_package_without_db as package_base,
)
from stage_pipelines.stage337 import (  # noqa: E402
    review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_training_without_db as iy,
)


aw = iy.aw

TODAY = "2026-06-01"
STAGE_ID = iy.STAGE_ID
STAGE_DIR = iy.STAGE_DIR
RUN_NUMBER = "run337IZ"
RUN_ID = "run337IZ_materialize_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_runtime_probe_package_without_db_v1"
PARENT_RUN_ID = iy.RUN_ID
NEXT_RUN_ID = "run337JA_execute_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_mt5_runtime_probe_without_db_v1"
STATUS = "completed_stage337IZ_positive_low_edge_expansion_runtime_probe_package_materialized_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_for_proxy_positive_cost_stress_candidate_proxy_mt5_diff_required_no_selection"
DECISION = "stage337IZ_open_run337JA_execute_positive_low_edge_expansion_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_no_mt5_execution_in_IZ_no_candidate_selection_"
    "no_forward_no_runtime_authority_no_operating_or_goal_claim"
)
PACKAGE_KNOWN_DIFFERENCE = (
    "feature common-file filename inherits lifecycle_cost_repair base engine name, but run directory, run_id, "
    "model identity, and set/ini identity are run337IZ positive-low-edge package artifacts."
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_COPY_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IZ_positive_low_edge_expansion_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IZ_positive_low_edge_expansion_runtime_probe_package.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_positive_low_edge_cost_stress_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

FEATURE_MATRIX = FEATURE_DIR / "positive_low_edge_cost_stress_inner_holdout_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "positive_low_edge_cost_stress_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
EXECUTION_QUEUE = RUN_DIR / "run337JA_execution_queue.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    iy.FINAL_DECISION,
    iy.GATE_AUDIT,
    iy.POSITIVE_MATRIX,
    iy.ix.TRAINED_MODEL_MANIFEST,
    iy.ix.FEATURE_SCHEMA,
    iy.ix.ONNX_PARITY,
    iy.ix.iw.iv.IV_INPUT_FRAME,
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
    ROUTING_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def attempt_name(index: int, model_id: str) -> str:
    return f"iz{index:02d}_{model_id}"


def contracts_and_queue() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    tester = pd.DataFrame(
        [
            {
                "contract_id": "tester_identity",
                "subject": "MT5 Strategy Tester(MT5 전략 테스터)",
                "requirement": "US100 M5, fixed lot(고정 랏), fixed argmax(고정 최대확률), no optimization(최적화 없음)",
                "evidence_path": rel(TESTER_INI_MANIFEST),
                "known_difference": "package only(패키지 전용); actual costs(실제 비용)는 tester output(테스터 출력) 후 확인",
                "blocked_if_missing": "tester report/settings/trade list(테스터 보고서/설정/거래 목록)",
                "forbidden_action": "trust KPI(KPI 신뢰) without tester identity(테스터 정체성 없음)",
                "effect": "JA execution(JA 실행)에서 backtest evidence(백테스트 근거)를 감사할 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    proxy = pd.DataFrame(
        [
            {
                "contract_id": "proxy_mt5_diff",
                "subject": "proxy expected value(프록시 예상값) vs MT5 runtime(MT5 런타임)",
                "requirement": "compare probabilities/hash/decision/KPI diff(확률/해시/결정/KPI 차이 비교)",
                "evidence_path": rel(EXPECTED_PROBABILITY_TAPE),
                "known_difference": "proxy(프록시)는 probability tape(확률 테이프), MT5(메타트레이더5)는 broker lifecycle execution(브로커 생명주기 실행)",
                "blocked_if_missing": "runtime telemetry(런타임 기록) or expected tape(예상 테이프)",
                "forbidden_action": "use proxy net(프록시 순수익)을 MT5 profit(MT5 수익)으로 사용",
                "effect": "proxy(프록시)를 comparison baseline(비교 기준선)으로만 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    runtime = pd.DataFrame(
        [
            {
                "contract_id": "runtime_parity_inputs",
                "subject": "feature/model handoff(피처/모델 인계)",
                "requirement": "feature_input_hash(피처 입력 해시) and ONNX probabilities(ONNX 확률) must match on overlap(겹치는 구간에서 일치)",
                "evidence_path": f"{rel(FEATURE_MATRIX)};{rel(MODEL_HANDOFF_MANIFEST)}",
                "known_difference": PACKAGE_KNOWN_DIFFERENCE,
                "blocked_if_missing": "Common Files handoff(공용 파일 인계) or telemetry(기록)",
                "forbidden_action": "runtime authority(런타임 권위) from package only(패키지만으로 주장)",
                "effect": "JA runtime parity(JA 런타임 동등성)를 행 단위로 비교할 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "ja_execute_positive_low_edge_cost_stress_mt5_runtime_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "execute MT5 runtime probe(MT5 런타임 탐침 실행) for proxy-positive cost-stress ONNX candidate(프록시 양성 비용압박 ONNX 후보)",
                "required_inputs": f"{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)};{rel(EXPECTED_PROBABILITY_TAPE)};{rel(COMMON_FILES_SYNC)}",
                "required_outputs": "runtime telemetry/tester reports/proxy-vs-MT5 diff(런타임 기록/테스터 보고서/프록시-MT5 차이)",
                "blocked_if_missing": "terminal/broker visibility/tester output/telemetry(터미널/브로커 가시성/테스터 출력/런타임 기록)",
                "forbidden_action": "Forward/Goal claim(전진/목표 주장) before MT5 evidence(MT5 근거 전)",
                "effect": "threshold/lots(임계값/랏)을 바꾸지 않고 package(패키지)를 실행으로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return tester, proxy, runtime, queue


def configure_package_engine() -> None:
    source = SimpleNamespace(
        aw=aw,
        STAGE_ID=STAGE_ID,
        STAGE_DIR=STAGE_DIR,
        RUN_ID=iy.RUN_ID,
        FINAL_DECISION=iy.FINAL_DECISION,
        GATE_AUDIT=iy.GATE_AUDIT,
        POSITIVE_MATRIX=iy.POSITIVE_MATRIX,
        ip=SimpleNamespace(
            TRAINED_MODEL_MANIFEST=iy.ix.TRAINED_MODEL_MANIFEST,
            FEATURE_SCHEMA=iy.ix.FEATURE_SCHEMA,
            ONNX_PARITY=iy.ix.ONNX_PARITY,
            FEATURE_SET_ID=iy.ix.FEATURE_SET_ID,
            split_inner=iy.ix.train_base.split_inner,
            io_review=SimpleNamespace(
                inr=SimpleNamespace(IN_INPUT_FRAME=iy.ix.iw.iv.IV_INPUT_FRAME)
            ),
        ),
    )
    package_base.__file__ = __file__
    package_base.iq = source
    package_base.aw = aw
    package_base.TODAY = TODAY
    package_base.STAGE_ID = STAGE_ID
    package_base.STAGE_DIR = STAGE_DIR
    package_base.RUN_NUMBER = RUN_NUMBER
    package_base.RUN_ID = RUN_ID
    package_base.PARENT_RUN_ID = PARENT_RUN_ID
    package_base.NEXT_RUN_ID = NEXT_RUN_ID
    package_base.STATUS = STATUS
    package_base.JUDGMENT = JUDGMENT
    package_base.DECISION = DECISION
    package_base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    package_base.RUN_DIR = RUN_DIR
    package_base.MT5_DIR = MT5_DIR
    package_base.SET_DIR = SET_DIR
    package_base.INI_DIR = INI_DIR
    package_base.MODEL_COPY_DIR = MODEL_COPY_DIR
    package_base.FEATURE_DIR = FEATURE_DIR
    package_base.EXPECTED_DIR = EXPECTED_DIR
    package_base.REVIEW_DIR = REVIEW_DIR
    package_base.REPORT_PATH = REPORT_PATH
    package_base.DECISION_DOC = DECISION_DOC
    package_base.COMMON_ROOT = COMMON_ROOT
    package_base.COMMON_FEATURE_DIR = COMMON_FEATURE_DIR
    package_base.COMMON_MODEL_DIR = COMMON_MODEL_DIR
    package_base.COMMON_TELEMETRY_DIR = COMMON_TELEMETRY_DIR
    package_base.FEATURE_MATRIX = FEATURE_MATRIX
    package_base.FEATURE_MATRIX_MANIFEST = FEATURE_MATRIX_MANIFEST
    package_base.EXPECTED_PROBABILITY_TAPE = EXPECTED_PROBABILITY_TAPE
    package_base.EXPECTED_PROBABILITY_INDEX = EXPECTED_PROBABILITY_INDEX
    package_base.MODEL_HANDOFF_MANIFEST = MODEL_HANDOFF_MANIFEST
    package_base.COMMON_FILES_SYNC = COMMON_FILES_SYNC
    package_base.TESTER_SET_MANIFEST = TESTER_SET_MANIFEST
    package_base.TESTER_INI_MANIFEST = TESTER_INI_MANIFEST
    package_base.RUNTIME_PROBE_ATTEMPT_PACKAGE = RUNTIME_PROBE_ATTEMPT_PACKAGE
    package_base.TESTER_IDENTITY_CONTRACT = TESTER_IDENTITY_CONTRACT
    package_base.PROXY_MT5_COMPARISON_CONTRACT = PROXY_MT5_COMPARISON_CONTRACT
    package_base.RUNTIME_PARITY_CONTRACT = RUNTIME_PARITY_CONTRACT
    package_base.EXECUTION_QUEUE = EXECUTION_QUEUE
    package_base.GATE_AUDIT = GATE_AUDIT
    package_base.FINAL_DECISION = FINAL_DECISION
    package_base.RUN_MANIFEST = RUN_MANIFEST
    package_base.INPUT_FILES = INPUT_FILES
    package_base.OUTPUT_FILES = OUTPUT_FILES
    package_base.attempt_name = attempt_name
    package_base.contracts_and_queue = contracts_and_queue


def postprocess_set_identity() -> pd.DataFrame:
    if not exists(TESTER_SET_MANIFEST):
        return pd.DataFrame()
    manifest = read_csv(TESTER_SET_MANIFEST)
    if manifest.empty:
        return manifest
    for index, row in manifest.iterrows():
        set_path = ROOT / str(row["set_path"])
        text = io(set_path).read_text(encoding="utf-8-sig")
        text = text.replace(
            "stage337IR_LifecycleCostRepair__MT5RuntimeProbe",
            "stage337IZ_PositiveLowEdgeCostStress__MT5RuntimeProbe",
        )
        io(set_path).write_text(text, encoding="utf-8-sig", newline="\n")
        manifest.loc[index, "set_sha256"] = sha(set_path)
        manifest.loc[index, "identity_relabel_status"] = "relabelled_to_run337IZ(337IZ로 재라벨링)"
        manifest.loc[index, "effect"] = "set file(설정 파일)의 exploration label(탐색 라벨)을 IZ package(IZ 패키지) 정체성에 맞춘다."
    write_csv(TESTER_SET_MANIFEST, manifest)
    return manifest


def postprocess_attempt_package() -> None:
    if not exists(RUNTIME_PROBE_ATTEMPT_PACKAGE):
        return
    attempts = read_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE)
    if attempts.empty:
        return
    attempts["known_proxy_runtime_difference"] = (
        "proxy(프록시)는 signal sanity check(신호 점검)이고 MT5(메타트레이더5)는 broker lifecycle execution(브로커 생명주기 실행)이다."
    )
    attempts["forbidden_action"] = "package priority(패키지 우선순위)를 selection/promotion(선택/승격)으로 취급하지 않는다."
    attempts["effect"] = "JA runtime probe(JA 런타임 탐침)가 모델 로직 변경 없이 같은 입력을 읽게 한다."
    attempts["claim_boundary"] = CLAIM_BOUNDARY
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempts)


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(iy.GATE_AUDIT)
    parent_passed = passed_status(parent_gates["status"]).all()
    expected_rows_ok = summary["expected_probability_rows"] == summary["feature_matrix_rows"] * summary["attempt_rows"]
    sync_ready = summary["common_sync_rows"] == summary["common_sync_ready_rows"] and summary["common_sync_rows"] >= 3
    set_manifest = read_csv(TESTER_SET_MANIFEST) if exists(TESTER_SET_MANIFEST) else pd.DataFrame()
    set_relabelled = (
        not set_manifest.empty
        and "identity_relabel_status" in set_manifest.columns
        and set_manifest["identity_relabel_status"].astype(str).str.contains("run337IZ").all()
    )
    return pd.DataFrame(
        [
            gate_row("parent_iy_gates_passed", "passed" if parent_passed else "failed", rel(iy.GATE_AUDIT), "IY review(IY 검토) gate(게이트)가 통과한 후보만 package(패키지)로 넘긴다."),
            gate_row("proxy_positive_candidate_loaded", "passed" if summary["attempt_rows"] >= 1 else "failed", rel(iy.POSITIVE_MATRIX), "proxy-positive(프록시 양성) 후보를 MT5(메타트레이더5) 비교 대상으로 불러온다."),
            gate_row("feature_matrix_materialized", "passed" if exists(FEATURE_MATRIX) and summary["feature_matrix_rows"] > 0 else "failed", rel(FEATURE_MATRIX), "MT5(메타트레이더5)가 읽을 feature matrix(피처 행렬)를 만든다."),
            gate_row("expected_probability_tape_materialized", "passed" if exists(EXPECTED_PROBABILITY_TAPE) and expected_rows_ok else "failed", rel(EXPECTED_PROBABILITY_TAPE), "proxy expected value(프록시 예상값)를 MT5 diff(MT5 차이) 기준선으로 만든다."),
            gate_row("model_and_common_files_synced", "passed" if sync_ready else "failed", rel(COMMON_FILES_SYNC), "ONNX(온엑스)와 feature matrix(피처 행렬)를 Common Files(공용 파일)로 복사한다."),
            gate_row("tester_set_ini_materialized", "passed" if summary["tester_set_rows"] == summary["attempt_rows"] and summary["tester_ini_rows"] == summary["attempt_rows"] else "failed", f"{rel(TESTER_SET_MANIFEST)};{rel(TESTER_INI_MANIFEST)}", "MT5 Strategy Tester(MT5 전략 테스터) 실행 파일을 만든다."),
            gate_row("tester_set_identity_relabelled", "passed" if set_relabelled else "failed", rel(TESTER_SET_MANIFEST), "set file(설정 파일)의 exploration label(탐색 라벨)을 IZ 정체성으로 맞춘다."),
            gate_row("runtime_attempt_package_written", "passed" if exists(RUNTIME_PROBE_ATTEMPT_PACKAGE) and summary["attempt_rows"] >= 1 else "failed", rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "JA execution(JA 실행)이 읽을 attempt package(시도 패키지)를 만든다."),
            gate_row("proxy_mt5_contracts_written", "passed" if exists(PROXY_MT5_COMPARISON_CONTRACT) and exists(RUNTIME_PARITY_CONTRACT) else "failed", f"{rel(PROXY_MT5_COMPARISON_CONTRACT)};{rel(RUNTIME_PARITY_CONTRACT)}", "proxy-MT5 comparison(프록시-MT5 비교) 조건을 고정한다."),
            gate_row("execution_queue_opened", "passed" if exists(EXECUTION_QUEUE) else "failed", rel(EXECUTION_QUEUE), "다음 JA runtime probe(JA 런타임 탐침) 실행으로 넘긴다."),
            gate_row("no_mt5_execution_in_iz", "passed", rel(CLAIM_RECEIPT), "IZ는 package(패키지)만 만들고 MT5 execution(MT5 실행)은 하지 않는다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(CLAIM_RECEIPT), "selected model(선택 모델), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": display_path(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(ROUTING_RECEIPT, {**base, "next_run_id": NEXT_RUN_ID, "attempt_rows": summary["attempt_rows"], "effect": "runtime probe package(런타임 탐침 패키지)를 JA execution(JA 실행)으로 넘긴다."})
    write_json(DATA_RECEIPT, {**base, "feature_matrix": rel(FEATURE_MATRIX), "feature_matrix_rows": summary["feature_matrix_rows"], "first_source_time": summary["first_source_time"], "last_source_time": summary["last_source_time"], "timestamp_semantics": "bar close timestamp(봉 마감 시각)", "effect": "MT5 input time(MT5 입력 시각)을 고정한다."})
    write_json(MODEL_RECEIPT, {**base, "candidate_model_ids": summary["candidate_model_ids"], "model_handoff_rows": summary["model_handoff_rows"], "feature_order_hash": summary["feature_order_hash"], "effect": "ONNX handoff(ONNX 인계) hash(해시)를 고정한다."})
    write_json(RUNTIME_RECEIPT, {**base, "research_path": rel(Path(__file__)), "runtime_path": "package_only_no_execution(패키지 전용, 실행 없음)", "shared_contract": rel(RUNTIME_PARITY_CONTRACT), "parity_check": rel(EXPECTED_PROBABILITY_TAPE), "known_difference": PACKAGE_KNOWN_DIFFERENCE, "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)"})
    write_json(FORENSICS_RECEIPT, {**base, "tester_identity": rel(TESTER_IDENTITY_CONTRACT), "ea_identity": summary["ea_module_hashes"], "report_identity": "not_run_in_IZ(IZ에서 미실행)", "trade_evidence": "not_available_until_JA(JA 전에는 없음)", "cost_assumptions": "Strategy Tester output(전략 테스터 출력) required(필요)", "backtest_judgment": "inconclusive_package_only(패키지만으로 불충분)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "observed_change": "runtime probe package materialized(런타임 탐침 패키지 생성)", "comparison_baseline": rel(iy.FINAL_DECISION), "likely_drivers": "cost-stress survival label and short-side net contribution(비용압박 생존 라벨과 숏 방향 순수익 기여)", "next_probe": NEXT_RUN_ID, "attribution_confidence": "not_applicable_until_mt5(MT5 전 해당 없음)"})
    write_json(JUDGMENT_RECEIPT, {**base, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates)), "judgment_label": JUDGMENT})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "mt5_execution": "not_run_in_IZ", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"})
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 해시 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run_in_IZ",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "package_known_difference": PACKAGE_KNOWN_DIFFERENCE,
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337IZ Positive Low-Edge Cost-Stress Runtime Probe Package(run337IZ 양성 저마진 비용압박 런타임 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- candidate_model_ids(후보 모델 ID): `{final['candidate_model_ids']}`
- feature_matrix_rows(피처 행렬 행 수): `{final['feature_matrix_rows']}`
- expected_probability_rows(예상 확률 행 수): `{final['expected_probability_rows']}`
- common_sync(Common Files 공용 파일 동기화): `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`

## Action(행동)

IY review(IY 검토)의 proxy-positive(프록시 양성) cost-stress(비용압박) 후보를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 만들었다.
Effect(효과): 다음 JA run(JA 실행)이 feature matrix(피처 행렬), ONNX(온엑스), expected tape(예상 테이프), tester set/ini(테스터 설정)를 바로 사용할 수 있다.

## Boundary(경계)

No MT5 execution in IZ(IZ에서 MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Known Difference(알려진 차이)

`{PACKAGE_KNOWN_DIFFERENCE}`
Effect(효과): 실행 경로와 hash(해시)는 추적되지만, JA에서 proxy-MT5 diff(프록시-MT5 차이)를 반드시 확인해야 한다.

## Next(다음)

`{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행하고 proxy-MT5 diff(프록시-MT5 차이)를 기록한다.
"""
    decision = f"""# {TODAY} Stage337IZ Decision(337IZ 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(EXPECTED_PROBABILITY_TAPE)}`, `{rel(COMMON_FILES_SYNC)}`

Action(행동): proxy-positive(프록시 양성) cost-stress ONNX(비용압박 ONNX) 후보를 MT5 runtime probe(MT5 런타임 탐침) 입력으로 만들었다.
Effect(효과): proxy expected value(프록시 예상값)를 MT5 runtime evidence(MT5 런타임 근거)와 비교할 수 있게 했다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

IZ package(IZ 패키지)는 MT5 runtime probe(MT5 런타임 탐침)에 필요한 파일을 만들었다.
Effect(효과): JA run(JA 실행)에서 proxy-MT5 diff(프록시-MT5 차이)를 실제 runtime evidence(런타임 근거)로 확인할 수 있다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선택 모델): `none(없음)`
- probe_priority_model(탐침 우선 모델): `{final['candidate_model_ids']}`
- MT5 execution(MT5 실행): `not_run_in_IZ(IZ에서 미실행)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): runtime package(런타임 패키지)를 selection(선택)이나 authority(권위)로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337IZ {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IZ Positive Low-Edge Cost-Stress Runtime Probe Package(양성 저마진 비용압박 런타임 탐침 패키지)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): feature matrix(피처 행렬), ONNX(온엑스), expected tape(예상 테이프), tester files(테스터 파일)를 만들었다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IZ Positive Low-Edge Cost-Stress Runtime Probe Package(양성 저마진 비용압박 런타임 탐침 패키지)

- action(행동): IY proxy-positive(IY 프록시 양성) 후보를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 만들었다.
- effect(효과): `{NEXT_RUN_ID}`에서 proxy-MT5 diff(프록시-MT5 차이)를 실행 근거로 볼 수 있게 했다.
- boundary(경계): MT5 execution(MT5 실행), selected model(선택 모델), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "runtime_probe_package",
            "candidate_model_ids": final["candidate_model_ids"],
            "feature_matrix_rows": final["feature_matrix_rows"],
            "expected_probability_rows": final["expected_probability_rows"],
            "result_status": "runtime_probe_package_ready_no_mt5_execution",
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    configure_package_engine()
    for path in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_COPY_DIR, FEATURE_DIR, EXPECTED_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    summary = package_base.materialize_package()
    postprocess_set_identity()
    postprocess_attempt_package()
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IZ gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "attempt_rows": final["attempt_rows"],
                "candidate_model_ids": final["candidate_model_ids"],
                "feature_matrix_rows": final["feature_matrix_rows"],
                "expected_probability_rows": final["expected_probability_rows"],
                "common_sync": f"{final['common_sync_ready_rows']}/{final['common_sync_rows']}",
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
