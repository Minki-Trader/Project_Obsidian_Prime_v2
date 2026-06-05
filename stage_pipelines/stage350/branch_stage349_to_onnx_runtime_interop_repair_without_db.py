from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

SOURCE_STAGE_ID = "349_onnx_short_carry_runtime__execute_mt5_probe"
NEW_STAGE_ID = "350_onnx_runtime_interop__softmax_output_shape_repair_probe"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run350A"
RUN_ID = "run350A_branch_stage349_to_onnx_runtime_interop_repair_without_db_v1"
PARENT_RUN_ID = "run349E_repair_treeensemble_onnx_operator_or_pivot_model_family_without_db_v1"
NEXT_RUN_ID = "run350B_probe_softmax_output_shape_and_conversion_semantics_without_db_v1"

STATUS = "completed_stage350A_branch_from_stage349_runtime_probe_weight_split_no_selection"
JUDGMENT = "stage_branch_completed_stage349_heavy_runtime_probe_handoff_to_stage350_onnx_runtime_interop_repair_no_operating_claim"
DECISION = "stage350A_open_run350B_probe_softmax_output_shape_and_conversion_semantics"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_onnx_runtime_interop_repair_handoff_only_"
    "no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run350A_stage_branch.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
INPUT_MANIFEST = NEW_STAGE_DIR / "01_inputs" / "stage350_input_manifest.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run349E"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SUMMARY = SOURCE_RUN_DIR / "runtime_compatible_mlp_mt5_probe_summary.csv"
SOURCE_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_EXPECTED_TAPE = SOURCE_RUN_DIR / "expected_tape.csv"
SOURCE_RUN_MANIFEST = SOURCE_RUN_DIR / "run_manifest.json"
SOURCE_LINEAGE = SOURCE_RUN_DIR / "artifact_lineage_receipt.json"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run349E_runtime_compatible_mlp_operator_pivot_probe.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_STAGE_LEDGER = SOURCE_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

SOURCE_D_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run349D"
SOURCE_D_FINAL_DECISION = SOURCE_D_RUN_DIR / "final_decision.json"
SOURCE_D_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run349D_onnx_no_conversion_runtime_parity_diagnostic.md"
SOURCE_E_SCRIPT = ROOT / "stage_pipelines" / "stage349" / "repair_treeensemble_onnx_operator_or_pivot_model_family_without_db.py"
SOURCE_D_SCRIPT = ROOT / "stage_pipelines" / "stage349" / "test_onnx_no_conversion_runtime_parity_diagnostic_without_db.py"

HANDOFF_MANIFEST = RUN_DIR / "stage349E_to_stage350_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage349_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run350B_runtime_interop_repair_queue.csv"
STAGE_TRANSITION_RECEIPT = RUN_DIR / "stage_transition_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage350A_branch_stage349_to_onnx_runtime_interop_repair.md"

SOURCE_INPUTS = [
    (SOURCE_FINAL_DECISION, "run349E final decision(349E 최종 결정)", True),
    (SOURCE_GATE_AUDIT, "run349E gate audit(349E 게이트 감사)", True),
    (SOURCE_SUMMARY, "run349E runtime-compatible MLP summary(349E 런타임 호환 MLP 요약)", True),
    (SOURCE_DIFF, "run349E proxy/MT5 runtime difference(349E 프록시/MT5 런타임 차이)", True),
    (SOURCE_EXPECTED_TAPE, "run349E expected tape(349E 예상 테이프)", True),
    (SOURCE_RUN_MANIFEST, "run349E run manifest(349E 실행 목록)", True),
    (SOURCE_LINEAGE, "run349E artifact lineage(349E 산출물 계보)", True),
    (SOURCE_REPORT, "run349E report(349E 보고서)", True),
    (SOURCE_D_FINAL_DECISION, "run349D no-conversion final decision(349D no-conversion 최종 결정)", True),
    (SOURCE_D_REPORT, "run349D no-conversion report(349D no-conversion 보고서)", True),
    (SOURCE_E_SCRIPT, "run349E producer script(349E 생산 스크립트)", True),
    (SOURCE_D_SCRIPT, "run349D diagnostic script(349D 진단 스크립트)", True),
    (SOURCE_SELECTION_STATUS, "Stage349 selection status(349단계 선택 상태)", True),
    (SOURCE_STAGE_BRIEF, "Stage349 stage brief(349단계 개요)", True),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(50_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    ensure_parent(path)
    temp_path = path.with_name(f"{path.name}.tmp")
    with open(fs_path(temp_path), "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
    os.replace(fs_path(temp_path), fs_path(path))


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames, existing = keys, []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys]
    write_csv(path, [*kept, *rows], fieldnames)


def source_summary() -> dict[str, Any]:
    run349e = read_json(SOURCE_FINAL_DECISION)
    run349d = read_json(SOURCE_D_FINAL_DECISION)
    _headers, summary_rows = read_csv_rows(SOURCE_SUMMARY)
    best_name = str(run349e.get("best_attempt_name", "e01_mlp_teacher_balanced"))
    best_summary = next((row for row in summary_rows if row.get("attempt_name") == best_name), summary_rows[0] if summary_rows else {})
    return {
        "run349e": run349e,
        "run349d": run349d,
        "summary_rows": summary_rows,
        "best_summary": best_summary,
        "attempt_count": str(run349e.get("attempt_rows", len(summary_rows))),
        "runtime_completed_rows": str(run349e.get("runtime_completed_rows", "")),
        "diff_rows": str(run349e.get("diff_rows", "")),
        "best_attempt_name": best_name,
        "best_net_profit": str(run349e.get("best_net_profit", "")),
        "best_profit_factor": str(run349e.get("best_profit_factor", "")),
        "best_trade_count": str(run349e.get("best_trade_count", "")),
        "run349d_input_hash_match_rows": str(run349d.get("input_hash_match_rows", "")),
        "run349d_probability_match_rows": str(run349d.get("probability_match_rows", "")),
        "run349d_max_abs_diff": str(run349d.get("python_expected_mt5_max_abs_diff", "")),
        "run349d_net_profit": str(run349d.get("net_profit", "")),
        "run349d_profit_factor": str(run349d.get("profit_factor", "")),
        "run349d_trade_count": str(run349d.get("trade_count", "")),
    }


def write_input_manifests() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, label, required in SOURCE_INPUTS:
        present = exists(path)
        rows.append(
            {
                "label": label,
                "path": rel(path),
                "exists": str(present).lower(),
                "sha256": sha256_file(path) if present else "",
                "size_bytes": os.path.getsize(fs_path(path)) if present else "",
                "required": str(required).lower(),
                "producer": "Stage349(349단계)",
                "consumer": RUN_ID,
                "availability": "tracked" if present else "missing",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    columns = [
        "label",
        "path",
        "exists",
        "sha256",
        "size_bytes",
        "required",
        "producer",
        "consumer",
        "availability",
        "claim_boundary",
    ]
    write_csv(INPUT_MANIFEST, rows, columns)
    write_csv(HANDOFF_MANIFEST, rows, columns)
    write_csv(SOURCE_INVENTORY, rows, columns)
    return rows


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    write_text(
        STAGE_README,
        f"""# Stage350 ONNX Runtime Interop Repair(350단계 온엑스 런타임 상호운용 수리)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        STAGE_BRIEF,
        f"""# Stage350 ONNX Runtime Interop Repair(350단계 온엑스 런타임 상호운용 수리)

- canonical_stage_id(정식 단계 ID): `{NEW_STAGE_ID}`
- subtitle(부제): `softmax_output_shape_repair_probe`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`

## Question(질문)

MT5 ONNX runtime(MT5 온엑스 런타임)이 probability output(확률 출력)을 Python(파이썬)과 같은 의미로 읽게 만들 수 있는가?

## Source Truth(원천 진실)

- run349D(349D 실행): input_hash(입력 해시)는 `{summary['run349d_input_hash_match_rows']}`행 일치했지만 probability_match(확률 일치)는 `{summary['run349d_probability_match_rows']}`행이었다.
- run349D(349D 실행): MT5 KPI(MT5 핵심 성과 지표)는 net_profit(순수익) `{summary['run349d_net_profit']}`, profit_factor(수익 팩터) `{summary['run349d_profit_factor']}`, trade_count(거래 수) `{summary['run349d_trade_count']}`였다.
- run349E(349E 실행): pure tensor MLP(순수 텐서 다층 퍼셉트론) 후보 `{summary['attempt_count']}`개를 실행했지만 parity_pass_rows(동등성 통과 행)는 `0`이었다.
- run349E(349E 실행): best_attempt(최고 시도)는 `{summary['best_attempt_name']}`, net_profit(순수익) `{summary['best_net_profit']}`, profit_factor(수익 팩터) `{summary['best_profit_factor']}`, trade_count(거래 수) `{summary['best_trade_count']}`였다.

## Scope(범위)

Stage350(350단계)은 ONNX operator/output semantics(온엑스 연산자/출력 의미)만 좁게 다룬다. softmax axis(소프트맥스 축), fixed output shape(고정 출력 모양), explicit softmax graph(명시 소프트맥스 그래프), InpModelNoConversion(입력 모델 변환 없음) 설정을 비교한다.

## Boundary(경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage350 Input Refs(350단계 입력 참조)

- input_manifest(입력 목록): `{rel(INPUT_MANIFEST)}`
- source_run(원천 실행): `run349E_repair_treeensemble_onnx_operator_or_pivot_model_family_without_db_v1`
- diagnostic_memory(진단 기억): `run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1`

Action(행동): Stage349(349단계)의 MT5 runtime probe(런타임 탐침) 실패 기억을 Stage350(350단계)의 입력으로 고정한다.

Effect(효과): 다음 수리 실행에서 같은 ONNX probability mismatch(온엑스 확률 불일치)를 원인 없이 반복하지 않는다.
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# Stage350 Review Index(350단계 검토 색인)

- run350A stage branch(350A 단계 분기): `{rel(REPORT_PATH)}`
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage350 Selection Status(350단계 선택 상태)

- selection_status(선정 상태): `no_selection(선정 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- latest_judgment(최근 판정): `{JUDGMENT}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- trade_density_requirement(거래 밀도 요건): `{TRADE_DENSITY_REQUIREMENT}`
""",
    )


def write_queue_and_receipts(summary: Mapping[str, Any], source_rows: Sequence[Mapping[str, Any]]) -> None:
    queue_rows = [
        {
            "next_run_id": NEXT_RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "parent_run_id": RUN_ID,
            "priority": "P0",
            "hypothesis": "MT5 ONNX runtime(MT5 온엑스 런타임) mismatch(불일치)는 model family(모델 계열)보다 output semantics(출력 의미) 또는 conversion setting(변환 설정) 문제일 수 있다.",
            "changed_variables": "softmax axis(소프트맥스 축);fixed output shape(고정 출력 모양);explicit softmax graph(명시 소프트맥스 그래프);InpModelNoConversion(입력 모델 변환 없음)",
            "controls": "Stage348 runtime_features(런타임 피처);Stage349 MT5 tester identity(MT5 테스터 정체성);trade density rule(거래 밀도 규칙)",
            "success_criteria": "input_hash parity(입력 해시 동등성) 유지 + probability parity(확률 동등성) 통과 + MT5 KPI(MT5 핵심 성과 지표) 기록",
            "failure_criteria": "probability_match_rows(확률 일치 행) 0 또는 saturated one-hot output(포화 원핫 출력) 반복",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(
        NEXT_QUEUE,
        queue_rows,
        [
            "next_run_id",
            "stage_id",
            "parent_run_id",
            "priority",
            "hypothesis",
            "changed_variables",
            "controls",
            "success_criteria",
            "failure_criteria",
            "claim_boundary",
        ],
    )
    experiment = {
        "hypothesis": queue_rows[0]["hypothesis"],
        "decision_use": "Stage350B(350B 실행)가 runtime-compatible ONNX(런타임 호환 온엑스) 형태를 고를 수 있는지 판단한다.",
        "comparison_baseline": "run349D TreeEnsembleClassifier(트리 앙상블 분류기) no-conversion mismatch(불일치)와 run349E pure tensor MLP(순수 텐서 MLP) mismatch(불일치)",
        "control_variables": queue_rows[0]["controls"],
        "changed_variables": queue_rows[0]["changed_variables"],
        "sample_scope": "FPMarkets US100 M5 Tier A(티어 A) MT5 Strategy Tester(전략 테스터) replay/reuse scope from Stage349",
        "success_criteria": queue_rows[0]["success_criteria"],
        "failure_criteria": queue_rows[0]["failure_criteria"],
        "invalid_conditions": "look-ahead bias(미래참조 편향), feature order drift(피처 순서 드리프트), timestamp mismatch(시각 불일치), missing MT5 report(MT5 보고서 누락)",
        "stop_conditions": "runtime parity(런타임 동등성)가 닫히거나, 출력 의미 수리가 반복 실패해서 새 model/runtime path(모델/런타임 경로)로 pivot(전환)할 때",
        "evidence_plan": "expected tape(예상 테이프), MT5 telemetry(MT5 텔레메트리), Strategy Tester report(전략 테스터 보고서), proxy/MT5 diff(프록시/MT5 차이), required gate audit(필수 게이트 감사), ledgers(장부)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(EXPERIMENT_RECEIPT, experiment)
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_stage_id": SOURCE_STAGE_ID,
            "new_stage_id": NEW_STAGE_ID,
            "reason": "User requested stage branch because Stage349 became heavy(사용자가 Stage349가 무거워져 단계 분기를 요청함).",
            "latest_source_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": [row["path"] for row in source_rows],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
                rel(HANDOFF_MANIFEST),
                rel(NEXT_QUEUE),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
            ],
            "artifact_hashes": "recorded_in_artifact_registry_and_input_manifest(산출물 등록부와 입력 목록에 기록)",
            "registry_links": [rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(RUN_REGISTRY), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "state_sync_stage_branch_only(상태 동기화 단계 분기 전용)",
            "forbidden_claims": [
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "live_readiness(실거래 준비)",
                "goal_achieve(목표 달성)",
            ],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_current_truth() -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {NEW_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage349(349단계)가 무거워져 ONNX runtime interop repair(온엑스 런타임 상호운용 수리)를 Stage350(350단계)으로 분기했다.

Effect(효과): Stage349(349단계)는 MT5 runtime probe(런타임 탐침) 실패 기억으로 고정하고, 다음 작업은 output semantics(출력 의미) 수리만 좁게 다룬다.
""",
    )
    write_text(
        ROOT_SELECTION_STATUS,
        f"""# Stage350 Selection Status(350단계 선택 상태)

- selection_status(선정 상태): `no_selection(선정 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- latest_judgment(최근 판정): `{JUDGMENT}`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )


def append_source_stage_notes() -> None:
    block = f"""## Stage350 Branch Handoff(350단계 분기 인계)

- handoff_run(인계 실행): `{RUN_ID}`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage349(349단계)의 run349F(349F 실행) 대기 상태를 Stage350(350단계)의 run350B(350B 실행)로 분기했다.

Effect(효과): Stage349(349단계)는 MT5 ONNX runtime probe(런타임 탐침)와 negative runtime parity memory(부정 런타임 동등성 기억)를 보존하고, output semantics repair(출력 의미 수리)는 새 단계에서 처리한다.
"""
    append_text_once(SOURCE_STAGE_BRIEF, RUN_ID, block)
    append_text_once(SOURCE_SELECTION_STATUS, RUN_ID, block)


def write_report_and_decision(summary: Mapping[str, Any]) -> None:
    report = f"""# run350A Stage Branch(350A 단계 분기)

- run_id(실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Current Truth(현재 진실)

Action(행동): Stage349(349단계)를 더 무겁게 만들지 않고 Stage350(350단계)을 새로 열었다.

Effect(효과): MT5 runtime evidence(MT5 런타임 근거)와 ONNX output repair(온엑스 출력 수리)를 분리해 다음 재진입 비용을 낮춘다.

## Failure Memory(실패 기억)

- run349D(349D 실행): input_hash(입력 해시) `{summary['run349d_input_hash_match_rows']}`행 일치, probability_match(확률 일치) `{summary['run349d_probability_match_rows']}`행, max_abs_diff(최대 절대 차이) `{summary['run349d_max_abs_diff']}`.
- run349E(349E 실행): pure tensor MLP(순수 텐서 MLP) `{summary['attempt_count']}`개 실행, parity_pass_rows(동등성 통과 행) `0`, best_attempt(최고 시도) `{summary['best_attempt_name']}`.
- run349E(349E 실행): best MT5 KPI(MT5 핵심 성과 지표)는 net_profit(순수익) `{summary['best_net_profit']}`, profit_factor(수익 팩터) `{summary['best_profit_factor']}`, trade_count(거래 수) `{summary['best_trade_count']}`.

## Stage350B Plan(350B 계획)

Stage350B(350B 실행)는 softmax axis(소프트맥스 축), fixed output shape(고정 출력 모양), explicit softmax graph(명시 소프트맥스 그래프), InpModelNoConversion(입력 모델 변환 없음)을 비교한다.

## Judgment Boundary(판정 경계)

이 분기는 state sync(상태 동기화)와 artifact lineage(산출물 계보) 작업이다. 운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
"""
    write_text(REPORT_PATH, report)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage350A Branch(350A 단계 분기)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage349(349단계)의 무거운 런타임 탐침 흐름을 Stage350(350단계)으로 분기한다.

Effect(효과): 다음 실행은 ONNX output semantics(온엑스 출력 의미) 수리에 집중하고, Stage349의 negative runtime parity evidence(부정 런타임 동등성 근거)는 보존한다.
""",
    )


def make_gates() -> list[dict[str, Any]]:
    current_text = read_text(CURRENT_WORKING_STATE) if exists(CURRENT_WORKING_STATE) else ""
    workspace_text = read_text(WORKSPACE_STATE) if exists(WORKSPACE_STATE) else ""
    selection_text = read_text(SELECTION_STATUS) if exists(SELECTION_STATUS) else ""
    root_selection_text = read_text(ROOT_SELECTION_STATUS) if exists(ROOT_SELECTION_STATUS) else ""
    all_required_sources = all(exists(path) for path, _label, required in SOURCE_INPUTS if required)
    gates = [
        ("user_requested_stage_branch_recorded", True, rel(REPORT_PATH), "사용자 요청으로 stage branch(단계 분기)를 기록했다."),
        ("source_artifacts_visible", all_required_sources, rel(INPUT_MANIFEST), "Stage349(349단계) 원천 산출물이 보인다."),
        (
            "new_stage_structure_created",
            all(exists(path) for path in [STAGE_BRIEF, INPUT_REFS, REPORT_PATH, REVIEW_INDEX, SELECTION_STATUS]),
            rel(NEW_STAGE_DIR),
            "Stage350(350단계) 필수 폴더와 문서를 만들었다.",
        ),
        ("experiment_design_receipt_written", exists(EXPERIMENT_RECEIPT), rel(EXPERIMENT_RECEIPT), "Stage350B(350B 실행)의 실험 설계를 기록했다."),
        ("artifact_lineage_connected", exists(LINEAGE_RECEIPT) and exists(HANDOFF_MANIFEST), rel(LINEAGE_RECEIPT), "원천과 새 산출물 계보를 연결했다."),
        ("claim_boundary_guard", exists(CLAIM_RECEIPT), rel(CLAIM_RECEIPT), "운영 주장을 막았다."),
        ("no_new_mt5_execution_boundary", CLAIM_BOUNDARY in selection_text, rel(SELECTION_STATUS), "이번 분기가 새 MT5 실행이 아님을 고정했다."),
        ("next_action_queue_opened", exists(NEXT_QUEUE), rel(NEXT_QUEUE), "다음 실행 대기열을 만들었다."),
        (
            "state_sync_audit",
            NEW_STAGE_ID in workspace_text and NEW_STAGE_ID in current_text and NEW_STAGE_ID in selection_text and NEW_STAGE_ID in root_selection_text,
            f"{rel(WORKSPACE_STATE)};{rel(CURRENT_WORKING_STATE)};{rel(SELECTION_STATUS)}",
            "현재 진실이 Stage350(350단계)을 가리킨다.",
        ),
        ("ledger_sync_audit", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER) and exists(RUN_REGISTRY), rel(STAGE_LEDGER), "단계/프로젝트 장부와 실행 등록부가 연결됐다."),
        ("required_gate_coverage_audit_written", exists(GATE_AUDIT), rel(GATE_AUDIT), "필수 게이트 커버리지 감사를 기록했다."),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, evidence, effect in gates
    ]
    write_csv(GATE_AUDIT, rows, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"])
    return rows


def stage_ledger_rows(gates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gate_passes = str(sum(1 for row in gates if row.get("status") == "passed"))
    gate_total = str(len(gates))
    base = {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "notes": "User requested a stage branch because Stage349 became heavy(사용자가 349단계가 무거워져 단계 분기를 요청함).",
        "source_package_run_id": PARENT_RUN_ID,
        "attempt_count": "2",
        "candidate_model_id": "none(없음)",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
        "result_judgment": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }
    tier_rows = [
        ("Tier A", "Tier A used(Tier A 사용)", "stage_branch_handoff_run349E_onnx_runtime_interop_failure_memory", "Stage349 Tier A runtime evidence handed off(349단계 Tier A 런타임 근거 인계)."),
        ("Tier B", "Tier B fallback used(Tier B 대체 사용)", "missing_required", "Tier B(티어 B)는 이번 분기에서 새 실행이 없어 missing_required(필수 누락)로 남긴다."),
        ("Tier A+B", "Tier A+B combined(Tier A+B 합산)", "same_as_tier_a_until_tier_b_available", "Tier B(티어 B)가 없으므로 combined(합산)은 Tier A와 같은 인계 경계다."),
    ]
    rows = []
    for tier, view, metric_scope, notes in tier_rows:
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{tier}",
                "subrun_id": tier,
                "view": view,
                "record_view": view,
                "tier": tier,
                "tier_scope": tier,
                "metric_scope": metric_scope,
                "kpi_scope": metric_scope,
                "primary_kpi": "stage_branch_handoff_no_new_mt5_execution",
                "guardrail_kpi": f"{TRADE_DENSITY_REQUIREMENT};runtime_parity_not_claimed",
                "notes": notes,
            }
        )
        rows.append(row)
    return rows


def project_ledger_rows(gates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in stage_ledger_rows(gates):
        project = dict(row)
        project["row_id"] = row["ledger_row_id"]
        project["evidence_boundary"] = CLAIM_BOUNDARY
        project["work_family"] = "state_sync(상태 동기화)"
        project["evidence_scope"] = "stage_branch_handoff(단계 분기 인계)"
        project["run_key"] = RUN_ID
        project["question"] = "Split heavy Stage349 into Stage350 ONNX runtime interop repair(무거운 349단계를 350단계 온엑스 런타임 상호운용 수리로 분기)"
        project["next_action"] = NEXT_RUN_ID
        rows.append(project)
    return rows


def write_ledgers(gates: Sequence[Mapping[str, Any]]) -> None:
    stage_header = read_csv_rows(SOURCE_STAGE_LEDGER)[0] if exists(SOURCE_STAGE_LEDGER) else list(stage_ledger_rows(gates)[0].keys())
    write_csv(STAGE_LEDGER, stage_ledger_rows(gates), stage_header)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_ledger_rows(gates))
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "notes": "Stage branch only; no new MT5 execution(단계 분기 전용, 새 MT5 실행 없음).",
            "family": "state_sync(상태 동기화)",
            "primary_report": rel(REPORT_PATH),
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": str(sum(1 for row in gates if row.get("status") == "passed")),
            "gate_total": str(len(gates)),
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "attempt_count": "2",
            "run_date": TODAY,
            "primary_artifact": rel(FINAL_DECISION),
            "candidate_model_id": "none(없음)",
            "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
            "source_package_run_id": PARENT_RUN_ID,
            "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_judgment": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
            "final_decision_path": rel(FINAL_DECISION),
            "gate_audit_path": rel(GATE_AUDIT),
            "created_at": TODAY,
        }
    ]
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows)


def write_final_decision(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer_script": rel(Path(__file__)),
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "artifacts": {
                "final_decision": rel(FINAL_DECISION),
                "gate_audit": rel(GATE_AUDIT),
                "report": rel(REPORT_PATH),
                "input_manifest": rel(INPUT_MANIFEST),
                "next_queue": rel(NEXT_QUEUE),
            },
        },
    )
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
            "gate_total": len(gates),
            "source_run349e_judgment": summary["run349e"].get("judgment", ""),
            "source_run349e_gate_passes": summary["run349e"].get("gate_passes", ""),
            "source_run349e_gate_total": summary["run349e"].get("gate_total", ""),
            "source_run349d_input_hash_match_rows": summary["run349d_input_hash_match_rows"],
            "source_run349d_probability_match_rows": summary["run349d_probability_match_rows"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_artifact_registry() -> None:
    artifacts = [
        ("final_decision", FINAL_DECISION, "run350A final decision(350A 최종 결정)"),
        ("required_gate_coverage_audit", GATE_AUDIT, "run350A gate audit(350A 게이트 감사)"),
        ("handoff_manifest", HANDOFF_MANIFEST, "Stage349E to Stage350 handoff manifest(349E에서 350단계 인계 목록)"),
        ("source_inventory", SOURCE_INVENTORY, "Stage350 source inventory(350단계 원천 목록)"),
        ("next_queue", NEXT_QUEUE, "run350B queue(350B 대기열)"),
        ("stage_transition_receipt", STAGE_TRANSITION_RECEIPT, "stage transition receipt(단계 전환 영수증)"),
        ("artifact_lineage_receipt", LINEAGE_RECEIPT, "artifact lineage receipt(산출물 계보 영수증)"),
        ("claim_boundary_receipt", CLAIM_RECEIPT, "claim boundary receipt(주장 경계 영수증)"),
        ("experiment_design_receipt", EXPERIMENT_RECEIPT, "experiment design receipt(실험 설계 영수증)"),
        ("stage_branch_report", REPORT_PATH, "run350A branch report(350A 분기 보고서)"),
        ("decision_doc", DECISION_DOC, "run350A decision doc(350A 결정 문서)"),
        ("run_manifest", RUN_MANIFEST, "run350A run manifest(350A 실행 목록)"),
        ("stage_brief", STAGE_BRIEF, "Stage350 stage brief(350단계 개요)"),
        ("selection_status", SELECTION_STATUS, "Stage350 selection status(350단계 선택 상태)"),
        ("pipeline", Path(__file__), "run350A producer script(350A 생산 스크립트)"),
    ]
    rows = []
    for artifact_type, path, notes in artifacts:
        rows.append(
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file(path) if exists(path) else "",
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": now_utc(),
                "notes": notes,
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def append_changelogs() -> None:
    block = f"""## {TODAY} {RUN_ID}

Action(행동): Stage349(349단계)의 run349F(349F 실행) 대기 상태를 Stage350(350단계) `ONNX runtime interop repair(온엑스 런타임 상호운용 수리)`로 분기했다.

Effect(효과): 무거운 MT5 runtime probe(런타임 탐침) 기록은 Stage349에 보존하고, 다음 작업은 output semantics(출력 의미) 수리만 좁게 추적한다.

- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(ROOT_CHANGELOG, RUN_ID, block)
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, block)


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [
        rel(path)
        for path in [
            STAGE_BRIEF,
            INPUT_REFS,
            INPUT_MANIFEST,
            SELECTION_STATUS,
            REVIEW_INDEX,
            REPORT_PATH,
            DECISION_DOC,
            FINAL_DECISION,
            RUN_MANIFEST,
            GATE_AUDIT,
            WORKSPACE_STATE,
            CURRENT_WORKING_STATE,
            HANDOFF_MANIFEST,
            NEXT_QUEUE,
            STAGE_LEDGER,
        ]
        if not exists(path)
    ]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    if failed:
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("run350A required gate audit failed(350A 필수 게이트 감사 실패): " + ", ".join(failed))
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        final = read_json(FINAL_DECISION)
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [
        NEW_STAGE_DIR / "00_spec",
        NEW_STAGE_DIR / "01_inputs",
        RUN_DIR,
        REVIEW_DIR,
        NEW_STAGE_DIR / "04_selected",
        DECISION_DOC.parent,
    ]:
        os.makedirs(fs_path(directory), exist_ok=True)
    summary = source_summary()
    source_rows = write_input_manifests()
    write_stage_docs(summary)
    write_queue_and_receipts(summary, source_rows)
    write_current_truth()
    append_source_stage_notes()
    write_report_and_decision(summary)
    gates = make_gates()
    write_ledgers(gates)
    gates = make_gates()
    write_ledgers(gates)
    write_final_decision(summary, gates)
    write_artifact_registry()
    append_changelogs()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
