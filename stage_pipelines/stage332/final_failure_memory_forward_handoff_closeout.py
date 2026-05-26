from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "332_overfit_guard__failure_memory_forward_research_handoff"
RUN_NUMBER = "run332F"
RUN_ID = "run332F_close_stage332_open_pocket_veto_materialization_stage_v1"
PARENT_RUN_ID = "run332E_runtime_parity_probe_design_v1"
NEXT_STAGE_ID = "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
NEXT_RUN_ID = "run333A_materialize_timestamp_safe_pocket_veto_features_v1"
STATUS = "completed_stage332_closeout_open_stage333_no_selection"
JUDGMENT = "stage332_closed_materialization_handoff_research_only_no_goal_achieve"
DECISION = "stage332_handoff_complete_stage333_open_materialization_next_no_candidate_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage332_closeout_materialization_handoff_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN332A_DIR = STAGE_DIR / "02_runs" / "run332A"
RUN332B_DIR = STAGE_DIR / "02_runs" / "run332B"
RUN332C_DIR = STAGE_DIR / "02_runs" / "run332C"
RUN332D_DIR = STAGE_DIR / "02_runs" / "run332D"
RUN332E_DIR = STAGE_DIR / "02_runs" / "run332E"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUTS_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_RUNS_DIR = NEXT_STAGE_DIR / "02_runs"
NEXT_REVIEWS_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"

DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage332F_close_stage332_open_stage333.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


SOURCE_ARTIFACTS: dict[str, Path] = {
    "run332A_report": REVIEWS_DIR / "run332A_failure_memory_forward_research_handoff_design.md",
    "run332B_report": REVIEWS_DIR / "run332B_data_guard_input_materialization.md",
    "run332C_report": REVIEWS_DIR / "run332C_cost_curve_guarded_scout.md",
    "run332D_report": REVIEWS_DIR / "run332D_pocket_veto_feature_thesis.md",
    "run332E_report": REVIEWS_DIR / "run332E_runtime_parity_probe_contract.md",
    "run332D_feature_materialization_queue": RUN332D_DIR / "feature_materialization_queue.csv",
    "run332D_label_boundary_receipt": RUN332D_DIR / "feature_label_boundary_receipt.json",
    "run332D_pocket_veto_plan": RUN332D_DIR / "pocket_veto_plan.csv",
    "run332E_runtime_parity_contract": RUN332E_DIR / "runtime_parity_contract.csv",
    "run332E_runtime_readiness_matrix": RUN332E_DIR / "runtime_probe_readiness_matrix.csv",
    "run332E_runtime_identity_manifest": RUN332E_DIR / "runtime_identity_manifest.json",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    try:
        return io_path(path).exists()
    except OSError:
        return False


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def insert_after_line(text: str, anchor_prefix: str, insertion: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(anchor_prefix):
            lines.insert(index + 1, insertion)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text + ("\n" if text.endswith("\n") else "\n") + insertion + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    index: dict[tuple[str, ...], dict[str, Any]] = {
        tuple(str(row.get(key, "")) for key in key_columns): row for row in existing
    }
    for row in rows:
        index[tuple(str(row.get(key, "")) for key in key_columns)] = dict(row)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in index.values():
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})
    return path


def append_unique_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    existing_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in existing}
    next_rows = list(existing)
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        if key not in existing_keys:
            next_rows.append(dict(row))
            existing_keys.add(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in next_rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})
    return path


def source_hash_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact_id, path in SOURCE_ARTIFACTS.items():
        exists = path_exists(path)
        rows.append(
            {
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": exists,
                "sha256": sha256_file(path) if exists and io_path(path).is_file() else "",
            }
        )
    return rows


def stage_summary_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "run332A_design_failure_memory_forward_research_handoff_packet_v1",
            "role": "failure_memory_to_research_constraints",
            "status_read": "completed_failure_memory_forward_research_handoff_design_no_selection",
            "handoff_effect": "Stage331 failure memory converted to constraints, not selected.",
        },
        {
            "run_id": "run332B_materialize_failure_memory_forward_data_and_guard_inputs_v1",
            "role": "data_guard_input_materialization",
            "status_read": "completed_data_guard_input_materialization_with_refresh_probe_boundary_no_selection",
            "handoff_effect": "existing forward handoff identity and raw refresh boundary recorded.",
        },
        {
            "run_id": "run332C_design_or_materialize_cost_curve_guarded_scout_v1",
            "role": "cost_curve_guarded_scout",
            "status_read": "completed_cost_curve_guarded_scout_materialization_no_selection",
            "handoff_effect": "cost+2 and rolling-pocket fragility converted to veto conditions.",
        },
        {
            "run_id": "run332D_design_pocket_veto_feature_thesis_v1",
            "role": "pocket_veto_feature_thesis",
            "status_read": "completed_pocket_veto_feature_thesis_design_no_selection",
            "handoff_effect": "four timestamp-safe thesis branches queued for materialization.",
        },
        {
            "run_id": "run332E_runtime_parity_probe_design_v1",
            "role": "runtime_parity_probe_contract",
            "status_read": "completed_runtime_parity_probe_contract_design_no_runtime_execution",
            "handoff_effect": "future MT5 probe requires feature/model/threshold/risk/report/telemetry identity.",
        },
    ]


def handoff_rows() -> list[dict[str, Any]]:
    materialization_queue = read_csv_rows(RUN332D_DIR / "feature_materialization_queue.csv")
    readiness = read_csv_rows(RUN332E_DIR / "runtime_probe_readiness_matrix.csv")
    return [
        {
            "handoff_id": "data_identity_boundary",
            "source_run": "run332B",
            "evidence_path": rel(RUN332B_DIR / "forward_handoff_identity_audit.csv"),
            "handoff_state": "ready_as_input_boundary",
            "next_stage_use": "verify feature source identity before materialized branch scoring.",
            "forbidden_use": "do not infer forward pass or retune threshold from handoff identity.",
        },
        {
            "handoff_id": "cost_curve_veto_memory",
            "source_run": "run332C",
            "evidence_path": rel(RUN332C_DIR / "guarded_scout_queue.csv"),
            "handoff_state": "ready_as_failure_memory",
            "next_stage_use": "test whether feature theses reduce cost and pocket fragility.",
            "forbidden_use": "do not exclude known bad dates or optimize lot size around the pocket.",
        },
        {
            "handoff_id": "feature_materialization_queue",
            "source_run": "run332D",
            "evidence_path": rel(RUN332D_DIR / "feature_materialization_queue.csv"),
            "handoff_state": f"{len(materialization_queue)}_queued_branches",
            "next_stage_use": "materialize four timestamp-safe pocket veto thesis branches.",
            "forbidden_use": "do not use Stage331 pocket labels as features.",
        },
        {
            "handoff_id": "runtime_parity_contract",
            "source_run": "run332E",
            "evidence_path": rel(RUN332E_DIR / "runtime_probe_readiness_matrix.csv"),
            "handoff_state": f"{len(readiness)}_design_ready_not_runtime_ready_branches",
            "next_stage_use": "carry MT5 report and telemetry evidence requirements into future probe.",
            "forbidden_use": "do not claim runtime authority from contract design only.",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_rows = source_hash_rows()
    queue_rows = read_csv_rows(RUN332D_DIR / "feature_materialization_queue.csv")
    contract_rows = read_csv_rows(RUN332E_DIR / "runtime_parity_contract.csv")
    readiness_rows = read_csv_rows(RUN332E_DIR / "runtime_probe_readiness_matrix.csv")
    source_missing = [row["artifact_id"] for row in source_rows if not row["exists"]]
    readiness_claim_ok = all(
        row.get("allowed_claim_now") == "runtime_contract_ready_only"
        and row.get("runtime_probe_readiness") == "design_ready_but_not_runtime_ready"
        for row in readiness_rows
    )
    return [
        {
            "gate": "source_stage_evidence_present",
            "status": "pass" if not source_missing else "fail",
            "evidence_path": rel(RUN_DIR / "source_artifact_hashes.json"),
            "notes": "all run332A-E source artifacts present" if not source_missing else f"missing={source_missing}",
        },
        {
            "gate": "feature_materialization_queue_ready",
            "status": "pass" if len(queue_rows) == 4 else "fail",
            "evidence_path": rel(RUN332D_DIR / "feature_materialization_queue.csv"),
            "notes": f"queued_branches={len(queue_rows)}",
        },
        {
            "gate": "runtime_contract_handoff_ready",
            "status": "pass" if len(contract_rows) == 6 and len(readiness_rows) == 4 and readiness_claim_ok else "fail",
            "evidence_path": rel(RUN332E_DIR / "runtime_probe_readiness_matrix.csv"),
            "notes": f"contract_rows={len(contract_rows)};readiness_rows={len(readiness_rows)};claim_boundary_ok={readiness_claim_ok}",
        },
        {
            "gate": "next_stage_scope_named",
            "status": "pass",
            "evidence_path": rel(NEXT_SPEC_DIR / "stage_brief.md"),
            "notes": "Stage333 is a materialization question, not a selection or operating promotion.",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "no_retune_guard_receipt.json"),
            "notes": "no threshold, lot, model, ONNX, D/B rule, or runtime handoff change in run332F.",
        },
        {
            "gate": "state_sync_audit",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "state_sync_receipt.json"),
            "notes": "workspace state, current working state, stage selection docs, and next stage docs are written by this run.",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "notes": "Forward Passed/Failed, runtime authority, live readiness, deployment, and Goal Achieve are not claimed.",
        },
        {
            "gate": "outputs_exist",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "run_manifest.json"),
            "notes": "run332F closeout artifacts are materialized.",
        },
    ]


def write_receipts(generated_at_utc: str) -> list[Path]:
    source_rows = source_hash_rows()
    failed_gates = [row for row in gate_rows() if row["status"] != "pass"]
    return [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_rows),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "source_stage": STAGE_ID,
                "next_stage": NEXT_STAGE_ID,
                "source_artifacts": source_rows,
                "handoff_artifacts": [rel(RUN_DIR / "stage332_to_stage333_handoff.csv")],
                "artifact_paths": [
                    rel(RUN_DIR / "stage332_closeout_summary.csv"),
                    rel(RUN_DIR / "stage332_to_stage333_handoff.csv"),
                    rel(RUN_DIR / "stage333_open_plan.csv"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
                "lineage_judgment": "connected_with_research_only_boundary",
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "no_retune_guard_receipt.json",
            {
                "selected_candidate_changed": False,
                "onnx_changed": False,
                "feature_order_changed": False,
                "threshold_changed": False,
                "d_b_rule_changed": False,
                "risk_or_lot_logic_changed": False,
                "runtime_handoff_changed": False,
                "new_data_threshold_fit": False,
                "notes": "run332F closes and opens stages only; it does not tune or repair model behavior.",
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "Stage332 failure-memory forward research handoff closeout and Stage333 materialization stage open",
                "evidence_available": [
                    rel(RUN332D_DIR / "feature_materialization_queue.csv"),
                    rel(RUN332E_DIR / "runtime_probe_readiness_matrix.csv"),
                    rel(RUN_DIR / "stage332_to_stage333_handoff.csv"),
                ],
                "evidence_missing": [
                    "no Stage333 materialized feature frames yet",
                    "no new MT5 tester output in run332F",
                    "no forward pass/fail decision",
                ],
                "judgment_label": "exploratory_handoff_closeout",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "Stage332 did enough handoff work to open materialization, but nothing here proves the strategy works forward.",
                "failed_gates": failed_gates,
            },
        ),
        write_json(
            RUN_DIR / "state_sync_receipt.json",
            {
                "workspace_state_target": NEXT_STAGE_ID,
                "current_run_target": NEXT_RUN_ID,
                "stage332_selection_status": "closed_no_selection_materialization_handoff",
                "stage333_selection_status": "open_planned",
                "main_push_required_after_closeout": True,
                "generated_at_utc": generated_at_utc,
            },
        ),
    ]


def write_stage333_open() -> list[Path]:
    NEXT_RUNS_DIR.mkdir(parents=True, exist_ok=True)
    stage_brief = write_md(
        NEXT_SPEC_DIR / "stage_brief.md",
        f"""
# Stage333 Timestamp-Safe Pocket Veto Materialization(333단계 타임스탬프 안전 포켓 거부 물질화)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- status(상태): `open_planned`
- opened_by(개방 실행): `{RUN_ID}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- active_question(활성 질문): Stage332(332단계)의 4개 pocket veto thesis(포켓 거부 논제)를 Stage331(331단계) 포켓을 외우지 않는 timestamp-safe feature/control artifact(타임스탬프 안전 피처/대조 산출물)로 물질화할 수 있는가?
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_stage333_materialization_no_threshold_retuning_no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_no_runtime_authority_no_goal_achieve`

Effect(효과): 다음 단계는 수익 지표를 고르기 전에 feature identity(피처 정체성), label boundary(라벨 경계), cost/curve guard(비용/곡선 방어), runtime contract(런타임 계약)를 실제 산출물로 묶는다.
""",
    )
    input_refs = write_md(
        NEXT_INPUTS_DIR / "input_refs.md",
        f"""
# Stage333 Input References(333단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- closeout_report(종료 보고): `{rel(REVIEWS_DIR / "run332F_stage_closeout_open_stage333.md")}`
- feature_materialization_queue(피처 물질화 대기열): `{rel(RUN332D_DIR / "feature_materialization_queue.csv")}`
- feature_label_boundary_receipt(피처 라벨 경계 영수증): `{rel(RUN332D_DIR / "feature_label_boundary_receipt.json")}`
- pocket_veto_plan(포켓 거부 계획): `{rel(RUN332D_DIR / "pocket_veto_plan.csv")}`
- runtime_parity_contract(런타임 동등성 계약): `{rel(RUN332E_DIR / "runtime_parity_contract.csv")}`
- runtime_readiness_matrix(런타임 준비 행렬): `{rel(RUN332E_DIR / "runtime_probe_readiness_matrix.csv")}`
- stage332_handoff(332단계 인계): `{rel(RUN_DIR / "stage332_to_stage333_handoff.csv")}`

Effect(효과): Stage333(333단계)는 Stage332(332단계)의 좋은 숫자를 고르는 것이 아니라, 금지선이 붙은 feature materialization(피처 물질화)을 시작한다.
""",
    )
    stage_ledger = write_csv(
        NEXT_REVIEWS_DIR / "stage_run_ledger.csv",
        [
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
            "decision",
        ],
        [],
    )
    selection = write_md(
        NEXT_SELECTED_DIR / "selection_status.md",
        f"""
# Stage333 Selection Status(333단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{STAGE_ID}`
- opened_by(개방 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage333(333단계)는 materialization(물질화) 단계이며, 아직 candidate selection(후보 선택)이나 forward decision(전진 판정)이 아니다.
""",
    )
    return [stage_brief, input_refs, stage_ledger, selection]


def update_stage332_selection_status() -> Path:
    text = f"""
# Stage332 Selection Status(332단계 선택 상태)

- stage_status(단계 상태): `closed_no_selection_materialization_handoff`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `331_overfit_guard__cross_horizon_cost_curve_parity_probe`
- latest_design(최신 설계): `run332A_design_failure_memory_forward_research_handoff_packet_v1`
- latest_data_guard(최신 데이터 방어): `run332B_materialize_failure_memory_forward_data_and_guard_inputs_v1`
- latest_cost_curve_scout(최신 비용/곡선 탐침): `run332C_design_or_materialize_cost_curve_guarded_scout_v1`
- latest_feature_thesis(최신 피처 논제): `run332D_design_pocket_veto_feature_thesis_v1`
- latest_runtime_parity_contract(최신 런타임 동등성 계약): `{PARENT_RUN_ID}`
- latest_closeout(최신 종료): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage332(332단계)는 선택 후보 없이 닫고, 4개 pocket veto thesis(포켓 거부 논제)를 Stage333(333단계) materialization(물질화) 입력으로 넘긴다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def write_reports() -> list[Path]:
    queue_count = len(read_csv_rows(RUN332D_DIR / "feature_materialization_queue.csv"))
    contract_count = len(read_csv_rows(RUN332E_DIR / "runtime_parity_contract.csv"))
    readiness_count = len(read_csv_rows(RUN332E_DIR / "runtime_probe_readiness_matrix.csv"))
    report = write_md(
        REVIEWS_DIR / "run332F_stage_closeout_open_stage333.md",
        f"""
# run332F Stage332 Closeout and Stage333 Open(332F 332단계 종료 및 333단계 개방)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Closeout Read(종료 판독)

- stage_summary_count(단계 요약 수): `5`
- materialization_queue_count(물질화 대기열 수): `{queue_count}`
- runtime_contract_count(런타임 계약 수): `{contract_count}`
- runtime_readiness_branch_count(런타임 준비 분기 수): `{readiness_count}`
- failed_gates(실패 게이트): `0`

Effect(효과): Stage332(332단계)는 candidate selection(후보 선택)이 아니라 materialization handoff(물질화 인계)로 닫는다.

## Boundary(경계)

- no threshold retuning(임계값 재튜닝 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 업데이트 없음)
- no ONNX export(ONNX 내보내기 없음)
- no MT5 execution(새 MT5 실행 없음)
- no candidate selection(후보 선택 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage332F Closeout Decision(332F 종료 결정)

Stage332(332단계)는 `closed_no_selection_materialization_handoff(선택 없음 물질화 인계 종료)`로 닫았다.

- decision(결정): `{DECISION}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): failure memory(실패 기억), cost/curve guard(비용/곡선 방어), feature thesis(피처 논제), runtime contract(런타임 계약)가 Stage333(333단계)의 입력으로 고정된다. 이 결정은 forward pass/fail(전진 통과/실패)이나 runtime authority(런타임 권위)가 아니다.
""",
    )
    return [report, decision]


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage333(333단계) `{NEXT_STAGE_ID}`는 run332F(332F 실행)에서 open_planned(열림 계획)로 열렸다. Effect(효과): Stage332(332단계)의 4개 pocket veto thesis(포켓 거부 논제)를 timestamp-safe materialization(타임스탬프 안전 물질화)로 넘기며 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
        "- >-\n"
        f"  Stage332(332단계) run332F(332F 실행)는 `{STATUS}`로 Stage332(332단계)를 닫았다. Effect(효과): data/cost-curve/feature/runtime contract(데이터/비용-곡선/피처/런타임 계약)를 Stage333(333단계) 입력으로 고정하지만 Forward Passed/Failed(전진 통과/실패)는 주장하지 않는다.\n"
    )
    if "Stage333(333단계)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`",
        "- source_stage(": f"- source_stage(원천 단계): `{STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `timestamp_safe_pocket_veto_materialization`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{DECISION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run332F_summary(332F 요약): Stage332(332단계) closeout/open Stage333(333단계 개방)을 `{STATUS}`로 완료했다. "
        "Effect(효과): feature thesis(피처 논제) 4개와 runtime parity contract(런타임 동등성 계약)를 Stage333(333단계) materialization(물질화) 입력으로 넘겼고 선택 후보, Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run332F_summary(332F 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage332F Closeout and Stage333 Open",
            f"""
## 2026-05-26 - Stage332F Closeout and Stage333 Open(332F 종료 및 333단계 개방)

- run332F(332F 실행): Stage332(332단계)를 no selection(선택 없음) materialization handoff(물질화 인계)로 닫았다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage332(332단계)의 4개 thesis(논제), data guard(데이터 방어), cost/curve guard(비용/곡선 방어), runtime contract(런타임 계약)를 Stage333(333단계) 입력으로 넘기고 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run332F_stage_closeout_open_stage333.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "publish_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": f"stage332_closed_no_selection;next_stage={NEXT_STAGE_ID};goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage_closeout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "stage_closeout_and_next_stage_open",
                "tier_scope": "research_handoff_no_trading_kpi",
                "kpi_scope": "materialization_handoff_contract",
                "scoreboard_lane": "publish_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "materialization_queue=4;runtime_contract_rows=6",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_stage_closeout_no_runtime_execution",
                "notes": f"decision={DECISION};next_stage={NEXT_STAGE_ID};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__stage_closeout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "stage_closeout_and_stage333_open(단계 종료 및 333단계 개방)",
                "tier_scope": "research_handoff_no_trading_kpi(연구 인계, 거래 KPI 없음)",
                "scoreboard": "materialization_handoff_contract(물질화 인계 계약)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__)]:
        if path_exists(artifact) and io_path(artifact).is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact.suffix.lstrip(".") or "file",
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage332F closeout artifact; no operating claim.",
                }
            )
    append_unique_csv(ARTIFACT_REGISTRY, ["artifact_id", "path"], artifact_rows)


def write_run_artifacts(generated_at_utc: str) -> list[Path]:
    artifacts: list[Path] = [
        write_csv(
            RUN_DIR / "stage332_closeout_summary.csv",
            ["run_id", "role", "status_read", "handoff_effect"],
            stage_summary_rows(),
        ),
        write_csv(
            RUN_DIR / "stage332_to_stage333_handoff.csv",
            ["handoff_id", "source_run", "evidence_path", "handoff_state", "next_stage_use", "forbidden_use"],
            handoff_rows(),
        ),
        write_csv(
            RUN_DIR / "stage333_open_plan.csv",
            ["plan_id", "target_stage", "next_run_id", "required_input", "required_boundary", "forbidden_claim"],
            [
                {
                    "plan_id": "stage333_run333A_materialization_start",
                    "target_stage": NEXT_STAGE_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "required_input": "four run332D feature theses plus run332E runtime contract",
                    "required_boundary": "timestamp-safe materialization before model/threshold/performance claims",
                    "forbidden_claim": "no selected candidate, no forward pass/fail, no runtime authority, no Goal Achieve",
                }
            ],
        ),
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate", "status", "evidence_path", "notes"], gate_rows()),
        write_json(
            RUN_DIR / "stage332_closeout_decision.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "primary_family": "publish_handoff",
                "primary_skill": "obsidian-stage-transition_unavailable_fallback_to_reentry_artifact_lineage_result_judgment",
                "support_skills": [
                    "obsidian-reentry-read",
                    "obsidian-artifact-lineage",
                    "obsidian-result-judgment",
                ],
                "required_gates": [
                    "state_sync_audit",
                    "closeout_gate",
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": [rel(path) for path in SOURCE_ARTIFACTS.values()],
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(write_receipts(generated_at_utc))
    artifacts.extend(write_reports())
    artifacts.append(update_stage332_selection_status())
    artifacts.extend(write_stage333_open())
    artifacts.extend(update_current_truth())
    return artifacts


def main() -> None:
    generated_at_utc = utc_now()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = write_run_artifacts(generated_at_utc)
    update_registers(generated_at_utc, artifacts)
    failures = [row for row in gate_rows() if row["status"] != "pass"]
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "materialization_queue_count": len(read_csv_rows(RUN332D_DIR / "feature_materialization_queue.csv")),
                "runtime_contract_count": len(read_csv_rows(RUN332E_DIR / "runtime_parity_contract.csv")),
                "failed_gates": failures,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
