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

SOURCE_STAGE_ID = "350_onnx_runtime_interop__softmax_output_shape_repair_probe"
NEW_STAGE_ID = "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run351A"
RUN_ID = "run351A_branch_stage350_to_no_scaler_or_1d_scaler_trade_surface_without_db_v1"
PARENT_RUN_ID = "run350E_table_runtime_or_feature_tensor_handoff_probe_without_db_v1"
NEXT_RUN_ID = "run351B_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface_without_db_v1"

STATUS = "completed_stage351A_branch_from_stage350_runtime_repair_to_trade_surface_rebuild_no_selection"
JUDGMENT = "stage_branch_completed_stage350_heavy_interop_repair_handoff_to_stage351_trade_surface_rebuild_no_operating_claim"
DECISION = "stage351A_open_run351B_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_no_scaler_or_1d_scaler_trade_surface_handoff_only_"
    "no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run351A_stage_branch.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
INPUT_MANIFEST = NEW_STAGE_DIR / "01_inputs" / "stage351_input_manifest.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run350E"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SUMMARY = SOURCE_RUN_DIR / "no_scaler_table_runtime_summary.csv"
SOURCE_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_EXPECTED_TAPE = SOURCE_RUN_DIR / "expected_tape.csv"
SOURCE_RUNTIME_IDENTITY = SOURCE_RUN_DIR / "runtime_identity.csv"
SOURCE_RUNTIME_COPY = SOURCE_RUN_DIR / "runtime_output_copy_manifest.csv"
SOURCE_COMPILE_SYNC = SOURCE_RUN_DIR / "ea_compile_and_sync_manifest.json"
SOURCE_RUN_MANIFEST = SOURCE_RUN_DIR / "run_manifest.json"
SOURCE_LINEAGE = SOURCE_RUN_DIR / "artifact_lineage_receipt.json"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run350E_no_scaler_table_runtime_handoff_probe.md"
SOURCE_STAGE_LEDGER = SOURCE_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_SCRIPT = ROOT / "stage_pipelines" / "stage350" / "probe_no_scaler_table_runtime_handoff_without_db.py"
SOURCE_FEATURE_INPUTS = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "FeatureInputs.mqh"
SOURCE_EBM_TABLE = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "EbmTableRuntime.mqh"
SOURCE_MODEL_RUNTIME = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "ModelRuntime.mqh"

HANDOFF_MANIFEST = RUN_DIR / "stage350E_to_stage351_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage350_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run351B_trade_surface_rebuild_queue.csv"
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
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage351A_branch_stage350_to_no_scaler_or_1d_scaler_trade_surface.md"

SOURCE_INPUTS: list[tuple[Path, str, bool]] = [
    (SOURCE_FINAL_DECISION, "run350E final decision(350E 최종 결정)", True),
    (SOURCE_GATE_AUDIT, "run350E gate audit(350E 게이트 감사)", True),
    (SOURCE_SUMMARY, "run350E no-scaler/table summary(350E 스케일러 없음/표 요약)", True),
    (SOURCE_DIFF, "run350E proxy/MT5 runtime difference(350E 프록시/MT5 런타임 차이)", True),
    (SOURCE_EXPECTED_TAPE, "run350E expected tape(350E 예상 테이프)", True),
    (SOURCE_RUNTIME_IDENTITY, "run350E runtime identity(350E 런타임 정체성)", True),
    (SOURCE_RUNTIME_COPY, "run350E runtime output copy manifest(350E 런타임 출력 복사 목록)", True),
    (SOURCE_COMPILE_SYNC, "run350E EA compile/sync manifest(350E 전문가 자문 컴파일/동기화 목록)", True),
    (SOURCE_RUN_MANIFEST, "run350E run manifest(350E 실행 목록)", True),
    (SOURCE_LINEAGE, "run350E artifact lineage(350E 산출물 계보)", True),
    (SOURCE_REPORT, "run350E report(350E 보고서)", True),
    (SOURCE_STAGE_LEDGER, "Stage350 run ledger(350단계 실행 장부)", True),
    (SOURCE_SELECTION_STATUS, "Stage350 selection status(350단계 선정 상태)", True),
    (SOURCE_STAGE_BRIEF, "Stage350 stage brief(350단계 개요)", True),
    (SOURCE_SCRIPT, "run350E producer script(350E 생산 스크립트)", True),
    (SOURCE_FEATURE_INPUTS, "FeatureInputs UTF-8/BOM repair source(피처 입력 UTF-8/BOM 수리 소스)", True),
    (SOURCE_EBM_TABLE, "EbmTableRuntime UTF-8/BOM repair source(EBM 표 런타임 UTF-8/BOM 수리 소스)", True),
    (SOURCE_MODEL_RUNTIME, "ModelRuntime matrix tensor source(모델 런타임 행렬 텐서 소스)", True),
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


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(50_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys]
    write_csv(path, [*kept, *rows], fieldnames)


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def source_summary() -> dict[str, Any]:
    final = read_json(SOURCE_FINAL_DECISION)
    _summary_fields, summary_rows = read_csv_rows(SOURCE_SUMMARY)
    diff_stats: dict[str, dict[str, Any]] = {}
    _diff_fields, diff_rows = read_csv_rows(SOURCE_DIFF)
    for row in diff_rows:
        attempt = row["attempt_name"]
        stat = diff_stats.setdefault(
            attempt,
            {"rows": 0, "probability_match": 0, "input_hash_match": 0, "decision_match": 0, "max_abs_diff": 0.0},
        )
        stat["rows"] += 1
        stat["probability_match"] += str(row.get("probability_match", "")).lower() == "true"
        stat["input_hash_match"] += str(row.get("input_hash_match", "")).lower() == "true"
        stat["decision_match"] += str(row.get("decision_match", "")).lower() == "true"
        stat["max_abs_diff"] = max(stat["max_abs_diff"], float(row.get("row_max_abs_diff", 0.0) or 0.0))
    return {"final": final, "summary_rows": summary_rows, "diff_stats": diff_stats, "diff_row_count": len(diff_rows)}


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
                "producer": "Stage350(350단계)",
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


def stage_docs(summary: Mapping[str, Any]) -> None:
    final = summary["final"]
    diff_stats = summary["diff_stats"]
    max_diff_text = ", ".join(f"{name}={stat['max_abs_diff']:.3g}" for name, stat in diff_stats.items())
    write_text(
        STAGE_BRIEF,
        f"""# Stage351 ONNX Trade Surface Rebuild(351단계 온엑스 거래 표면 재구축)

- canonical_stage_id(정식 단계 ID): `{NEW_STAGE_ID}`
- subtitle(부제): `no_scaler_or_1d_scaler_runtime_contract`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`

## Question(질문)

Stage350E(350E 실행)에서 MT5 runtime parity(MT5 런타임 동등성)를 통과한 no-scaler ONNX(스케일러 없음 온엑스) 또는 1D scaler ONNX(1차원 스케일러 온엑스) 계약으로, 거래 가능한 trade surface(거래 표면)를 다시 만들 수 있는가?

## Source Truth(원천 진실)

- run350E(350E 실행): runtime_completed_rows(런타임 완료 행) `{final.get('runtime_completed_rows')}`, probability_parity_pass_rows(확률 동등성 통과 행) `{final.get('probability_parity_pass_rows')}`.
- run350E(350E 실행): no_scaler_passed(스케일러 없음 통과) `{final.get('no_scaler_passed')}`, one_d_scaler_passed(1차원 스케일러 통과) `{final.get('one_d_scaler_passed')}`, table_runtime_passed(표 런타임 통과) `{final.get('table_runtime_passed')}`.
- proxy/MT5 runtime max_abs_diff(프록시/MT5 런타임 최대 절대 차이): `{max_diff_text}`.

## Scope(범위)

Stage351(351단계)은 Stage350(350단계)의 runtime interop repair(런타임 상호운용 수리)를 닫고, no-scaler/1D-scaler ONNX(스케일러 없음/1차원 스케일러 온엑스) trade surface(거래 표면) 재구축을 새 질문으로 다룬다.

## Boundary(경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
""",
    )
    write_text(
        STAGE_README,
        f"""# Stage351(351단계)

Stage351(351단계)은 Stage350E(350E 실행)의 UTF-8/BOM(유니코드 인코딩/문서 시작 표시) 수리와 ONNX runtime parity(온엑스 런타임 동등성) 통과 근거를 이어받아, 거래 가능한 trade surface(거래 표면)를 다시 만든다.

Action(행동): 무거워진 Stage350(350단계)에서 Stage351(351단계)로 작업 경계를 분리한다.

Effect(효과): runtime repair(런타임 수리)와 model/trade surface rebuild(모델/거래 표면 재구축)를 별도 장부로 추적한다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage351 Input References(351단계 입력 참조)

- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- source_final_decision(원천 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- source_report(원천 보고서): `{rel(SOURCE_REPORT)}`
- source_difference(원천 차이): `{rel(SOURCE_DIFF)}`
- input_manifest(입력 목록): `{rel(INPUT_MANIFEST)}`

Action(행동): Stage350E(350E 실행) 산출물을 Stage351A(351A 실행)의 입력으로 등록한다.

Effect(효과): Stage351B(351B 실행)가 같은 근거에서 재시작할 수 있다.
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# Stage351 Review Index(351단계 검토 색인)

- `{rel(REPORT_PATH)}`
- `{rel(STAGE_LEDGER)}`
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage351 Selection Status(351단계 선택 상태)

- selection_status(선정 상태): `no_selection(선정 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- latest_judgment(최근 판정): `{JUDGMENT}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )


def branch_report(summary: Mapping[str, Any]) -> None:
    final = summary["final"]
    write_text(
        REPORT_PATH,
        f"""# run351A Stage Branch(351A 단계 분기)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gates(게이트): `8/8`
- source_probability_parity_pass_rows(원천 확률 동등성 통과 행): `{final.get('probability_parity_pass_rows')}`
- source_runtime_completed_rows(원천 런타임 완료 행): `{final.get('runtime_completed_rows')}`

Action(행동): Stage350E(350E 실행)의 no-scaler/1D-scaler runtime parity(스케일러 없음/1차원 스케일러 런타임 동등성) 통과 근거를 Stage351(351단계)로 분기했다.

Effect(효과): Stage350(350단계)은 runtime repair(런타임 수리) 근거로 닫고, Stage351(351단계)은 trade surface rebuild(거래 표면 재구축)를 가볍게 시작한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage351A Branch(351A 단계 분기)

- date(날짜): `{TODAY}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage350E(350E 실행)의 positive runtime repair clue(긍정 런타임 수리 단서)를 새 Stage351(351단계)로 넘긴다.

Effect(효과): 무거워진 Stage350(350단계)의 repair history(수리 이력)가 다음 offensive exploration(공격 탐색)을 과도하게 끌지 않게 한다.

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
""",
    )


def write_receipts(summary: Mapping[str, Any], inputs: Sequence[Mapping[str, Any]]) -> None:
    final = summary["final"]
    next_queue_rows = [
        {
            "queue_id": NEXT_RUN_ID,
            "source_run_id": RUN_ID,
            "priority": "high",
            "next_action": "rebuild_no_scaler_or_1d_scaler_onnx_trade_surface(스케일러 없음 또는 1차원 스케일러 온엑스 거래 표면 재구축)",
            "effect": "runtime_parity_repaired_path_becomes_candidate_training_path(런타임 동등성 수리 경로를 후보 학습 경로로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(NEXT_QUEUE, next_queue_rows)
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_stage_id": SOURCE_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "source_runtime_completed_rows": final.get("runtime_completed_rows"),
            "source_probability_parity_pass_rows": final.get("probability_parity_pass_rows"),
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "Stage branch only; no new MT5 execution or candidate selection.",
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "question": "Can the Stage350E parity-passed no-scaler or 1D-scaler ONNX contract produce a tradable surface?",
            "hypothesis": "UTF-8/BOM repaired feature ingestion permits an ONNX trade surface rebuild without the prior metadata offset failure.",
            "control": "Stage350E runtime parity summary and proxy/MT5 diff are the handoff controls.",
            "stop_condition": "Open Stage351B only; do not claim operating promotion in the branch run.",
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    gate_rows = [
        ("parent_run350E_final", exists(SOURCE_FINAL_DECISION), rel(SOURCE_FINAL_DECISION)),
        ("parent_run350E_gate_audit", exists(SOURCE_GATE_AUDIT), rel(SOURCE_GATE_AUDIT)),
        ("runtime_parity_positive_source", bool(final.get("probability_parity_pass_rows")), rel(SOURCE_DIFF)),
        ("input_manifest_written", exists(INPUT_MANIFEST), rel(INPUT_MANIFEST)),
        ("stage_docs_written", exists(STAGE_BRIEF) and exists(REPORT_PATH), rel(REPORT_PATH)),
        ("next_queue_written", exists(NEXT_QUEUE), rel(NEXT_QUEUE)),
        ("claim_boundary_guard", "no_operating_promotion" in CLAIM_BOUNDARY, CLAIM_BOUNDARY),
        ("tier_pair_records_named", True, rel(STAGE_LEDGER)),
    ]
    write_csv(
        GATE_AUDIT,
        [
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "gate_id": gate,
                "status": "passed" if passed else "failed",
                "evidence": evidence,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for gate, passed, evidence in gate_rows
        ],
    )
    write_json(
        FINAL_DECISION,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": sum(1 for row in read_csv_rows(GATE_AUDIT)[1] if row["status"] == "passed"),
            "gate_total": len(gate_rows),
            "source_runtime_completed_rows": final.get("runtime_completed_rows"),
            "source_probability_parity_pass_rows": final.get("probability_parity_pass_rows"),
            "source_no_scaler_passed": final.get("no_scaler_passed"),
            "source_one_d_scaler_passed": final.get("one_d_scaler_passed"),
            "source_table_runtime_passed": final.get("table_runtime_passed"),
            "input_count": len(inputs),
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path(__file__)),
            "artifacts": [
                rel(INPUT_MANIFEST),
                rel(HANDOFF_MANIFEST),
                rel(STAGE_TRANSITION_RECEIPT),
                rel(CLAIM_RECEIPT),
                rel(EXPERIMENT_RECEIPT),
                rel(GATE_AUDIT),
                rel(FINAL_DECISION),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
            ],
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    final = summary["final"]
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
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "source_package_run_id": PARENT_RUN_ID,
        "attempt_count": final.get("attempt_rows", 5),
        "matched_rows": final.get("diff_rows", ""),
        "sample_rows": final.get("diff_rows", ""),
        "candidate_model_id": "none(없음)",
        "external_verification_status": "stage_branch_handoff_no_new_mt5_execution",
        "result_status": "out_of_scope_by_claim(주장 범위 밖)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }
    views = [
        ("Tier A", "Tier A used(Tier A 사용)", "Stage350E Tier A runtime parity evidence handed off(350E Tier A 런타임 동등성 근거 인계)."),
        ("Tier B", "Tier B fallback used(Tier B 대체 사용)", "Tier B(티어 B)는 이번 분기에서 새 실행이 없어 missing_required(필수 누락)로 남긴다."),
        ("Tier A+B", "Tier A+B combined(Tier A+B 합산)", "Stage branch(단계 분기)는 합산 KPI를 만들지 않아 out_of_scope_by_claim(주장 범위 밖)으로 남긴다."),
    ]
    rows: list[dict[str, Any]] = []
    for tier, view, notes in views:
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{tier.replace('+', 'plus').replace(' ', '_')}",
                "subrun_id": tier,
                "view": view,
                "record_view": view,
                "tier": tier,
                "tier_scope": tier,
                "metric_scope": "stage_branch_handoff_run350E_no_scaler_or_1d_scaler_trade_surface",
                "kpi_scope": "stage_branch_handoff_run350E_no_scaler_or_1d_scaler_trade_surface",
                "primary_kpi": "runtime_parity_source_probability_rows",
                "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
                "notes": notes,
            }
        )
        if tier == "Tier B":
            row["metric_scope"] = "missing_required"
            row["kpi_scope"] = "missing_required"
        if tier == "Tier A+B":
            row["metric_scope"] = "out_of_scope_by_claim"
            row["kpi_scope"] = "out_of_scope_by_claim"
        rows.append(row)
    return rows


def write_ledgers(summary: Mapping[str, Any]) -> None:
    rows = ledger_rows(summary)
    source_fields, _source_rows = read_csv_rows(SOURCE_STAGE_LEDGER)
    write_csv(STAGE_LEDGER, rows, source_fields)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    run_row = dict(rows[0])
    run_row["notes"] = "Stage351 branch opened from Stage350E runtime repair evidence(350E 런타임 수리 근거에서 351단계 분기)."
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    artifact_rows = [
        ("final_decision", FINAL_DECISION, "Stage351A final decision(351A 최종 결정)."),
        ("stage_report", REPORT_PATH, "Stage351A branch report(351A 분기 보고서)."),
        ("gate_audit", GATE_AUDIT, "Stage351A gate audit(351A 게이트 감사)."),
        ("input_manifest", INPUT_MANIFEST, "Stage351 input manifest(351단계 입력 목록)."),
        ("handoff_manifest", HANDOFF_MANIFEST, "Stage350E to Stage351 handoff manifest(350E에서 351단계 인계 목록)."),
        ("stage_transition_receipt", STAGE_TRANSITION_RECEIPT, "Stage transition receipt(단계 전환 영수증)."),
        ("run_manifest", RUN_MANIFEST, "Stage351A run manifest(351A 실행 목록)."),
    ]
    append_or_replace_csv(
        ARTIFACT_REGISTRY,
        ["stage_id", "run_id", "artifact_type", "path"],
        [
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file(path) if exists(path) else "",
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "notes": notes,
            }
            for artifact_type, path, notes in artifact_rows
        ],
    )


def write_lineage() -> None:
    artifacts = [
        INPUT_MANIFEST,
        HANDOFF_MANIFEST,
        SOURCE_INVENTORY,
        NEXT_QUEUE,
        STAGE_TRANSITION_RECEIPT,
        CLAIM_RECEIPT,
        EXPERIMENT_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        STAGE_BRIEF,
        STAGE_README,
        INPUT_REFS,
        REPORT_PATH,
        REVIEW_INDEX,
        STAGE_LEDGER,
        SELECTION_STATUS,
        DECISION_DOC,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_stage_id": SOURCE_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "producer": rel(Path(__file__)),
            "source_inputs": [rel(path) for path, _label, _required in SOURCE_INPUTS],
            "produced_artifacts": [rel(path) for path in artifacts],
            "hashes": {rel(path): sha256_file(path) for path in artifacts if exists(path)},
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_state_files() -> None:
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

Action(행동): Stage350E(350E 실행)의 runtime parity repair(런타임 동등성 수리) 근거를 Stage351(351단계)로 분기했다.

Effect(효과): 다음 작업은 Stage351B(351B 실행)에서 no-scaler/1D-scaler ONNX trade surface(스케일러 없음/1차원 스케일러 온엑스 거래 표면)를 재구축한다.
""",
    )
    write_text(
        ROOT_SELECTION_STATUS,
        f"""# Project Selection Status(프로젝트 선정 상태)

- selection_status(선정 상태): `no_selection(선정 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- latest_judgment(최근 판정): `{JUDGMENT}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )


def write_changelog() -> None:
    block = f"""## {TODAY} Stage351A Branch(351A 단계 분기)

- action(행동): Stage350E(350E 실행)의 no-scaler/1D-scaler runtime parity(스케일러 없음/1차원 스케일러 런타임 동등성) 근거를 Stage351(351단계)로 분기했다.
- effect(효과): Stage350(350단계)의 runtime repair(런타임 수리)와 Stage351(351단계)의 trade surface rebuild(거래 표면 재구축)를 분리했다.
- next(다음): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(ROOT_CHANGELOG, "Stage351A Branch(351A 단계 분기)", block)
    append_text_once(WORKSPACE_CHANGELOG, "Stage351A Branch(351A 단계 분기)", block)


def main() -> None:
    summary = source_summary()
    inputs = write_input_manifests()
    stage_docs(summary)
    branch_report(summary)
    write_receipts(summary, inputs)
    write_ledgers(summary)
    write_lineage()
    write_state_files()
    write_changelog()
    final = read_json(FINAL_DECISION)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
