from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_model_label_offensive_reseed_without_db as dp  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dp.STAGE_ID
RUN_NUMBER = "run364DQ"
RUN_ID = "run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1"
PARENT_RUN_ID = dp.RUN_ID
NEXT_RUN_ID = "run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1"

STATUS = "completed_stage364DQ_h17_short_source_model_label_review_oos_clue_no_package_no_authority"
JUDGMENT = "inconclusive_oos_short_source_model_clue_validation_density_below_min_no_package_no_authority"
DECISION = "stage364DQ_open_run364DR_short_source_density_pf_bridge_reseed"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_short_source_model_label_reseed_"
    "oos_clue_no_runtime_package_no_new_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = dp.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "dq_model_label_reseed_review_summary.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "density_pf_failure_memory.csv"
RUN364DR_QUEUE = RUN_DIR / "run364DR_density_pf_bridge_reseed_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DQ_h17_short_source_model_label_reseed_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DQ_h17_short_source_model_label_reseed_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    dp.FINAL_DECISION,
    dp.GATE_AUDIT,
    dp.SELECTED_MODEL_SUMMARY,
    dp.TRADE_SHAPE_SURFACE,
    dp.MODEL_SCORECARD,
    dp.ONNX_SMOKE_REPORT,
    dp.DATA_INTEGRITY_AUDIT,
    dp.COST_STRESS,
    dp.MONTH_STABILITY,
    dp.RUN364DQ_QUEUE,
    dp.JUDGMENT_RECEIPT,
    dp.MODEL_RECEIPT,
    dp.LINEAGE_RECEIPT,
    dp.CLAIM_RECEIPT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364DR_QUEUE,
    RESULT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return dp.rel(path)


def exists(path: Path | str) -> bool:
    return dp.exists(path)


def sha(path: Path | str) -> str:
    return dp.sha(path)


def json_ready(value: Any) -> Any:
    return dp.json_ready(value)


def read_json(path: Path) -> Any:
    return dp.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dp.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dp.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dp.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if exists(path):
        with open(str(io_path(path)), "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = [dict(row) for row in reader]
    if not fieldnames:
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    elif extend_header:
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)

    def row_key(row: Mapping[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(key, "")) for key in key_fields)

    replacements = {row_key(row): row for row in materialized}
    kept = [row for row in existing_rows if row_key(row) not in replacements]
    write_csv(path, [*kept, *materialized], fieldnames)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dp.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dp.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DQ inputs(DQ 입력 누락): " + ", ".join(missing))
    final = read_json(dp.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DP next_run_id mismatch(DP 다음 실행 ID 불일치): {final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if final.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DP forbidden claim(DP 금지 주장): {key}={final.get(key)}")
    gates = read_csv(dp.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DP gate audit(DP 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DQ review input(DQ 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "result_review(결과 검토)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-model-validation(모델 검증)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "DP may have produced a package-worthy ONNX seed(DP가 패키지 가치 있는 ONNX 씨앗을 만들었을 수 있음).",
            "decision_use": "Open runtime package only if density/PF contract holds(밀도/PF 계약이 맞을 때만 런타임 패키지를 엽니다).",
            "claim_boundary": CLAIM_BOUNDARY,
            "required_gates": [
                "input_lineage_gate",
                "dp_gate_inheritance_gate",
                "model_smoke_review_gate",
                "strict_contract_review_gate",
                "package_decision_gate",
                "next_queue_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
    )


def build_reviews(dp_final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = read_csv(dp.TRADE_SHAPE_SURFACE).to_dict("records")
    best_oos_pf = max(surface, key=lambda row: as_float(row.get("oos_profit_factor")))
    best_validation_density = max(surface, key=lambda row: as_float(row.get("validation_trade_density")))
    smoke = read_csv(dp.ONNX_SMOKE_REPORT)
    smoke_pass = int(smoke["status"].astype(str).str.startswith("passed").sum()) if not smoke.empty else 0
    summary = [
        {
            "run_id": RUN_ID,
            "selected_model_id": dp_final["selected_model_id"],
            "selected_validation_net": dp_final["selected_validation_net"],
            "selected_validation_profit_factor": dp_final["selected_validation_profit_factor"],
            "selected_validation_trade_density": dp_final["selected_validation_trade_density"],
            "selected_oos_net": dp_final["selected_oos_net"],
            "selected_oos_profit_factor": dp_final["selected_oos_profit_factor"],
            "selected_oos_trade_density": dp_final["selected_oos_trade_density"],
            "strict_candidate_count": dp_final["strict_candidate_count"],
            "onnx_smoke_pass_rows": smoke_pass,
            "best_oos_pf_model_id": best_oos_pf.get("model_id", ""),
            "best_oos_pf": best_oos_pf.get("oos_profit_factor", ""),
            "best_oos_pf_density": best_oos_pf.get("oos_trade_density", ""),
            "best_validation_density_model_id": best_validation_density.get("model_id", ""),
            "best_validation_density": best_validation_density.get("validation_trade_density", ""),
            "best_validation_density_net": best_validation_density.get("validation_net", ""),
            "review_status": "oos_clue_no_package(OOS 단서, 패키지 아님)",
            "effect": "ONNX smoke(온엑스 스모크)는 통과했지만 밀도 계약이 깨져 runtime package(런타임 패키지)를 열지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    package = [
        {
            "run_id": RUN_ID,
            "decision": "do_not_open_runtime_package(런타임 패키지 열지 않음)",
            "reason": "strict_candidate_count is zero and selected density is below 3/day(엄격 후보 0개이고 선택 밀도가 일 3회 미만).",
            "selected_model_id": dp_final["selected_model_id"],
            "selected_oos_net": dp_final["selected_oos_net"],
            "selected_oos_profit_factor": dp_final["selected_oos_profit_factor"],
            "selected_oos_trade_density": dp_final["selected_oos_trade_density"],
            "next_run_id": NEXT_RUN_ID,
            "effect": "OOS clue(표본외 단서)를 보존하되 MT5 package(MT5 패키지)로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "dq01_onnx_oos_clue_density_below_min",
            "observation": f"selected OOS net/PF/density {dp_final['selected_oos_net']} / {dp_final['selected_oos_profit_factor']} / {dp_final['selected_oos_trade_density']}",
            "why_failed": "trade density below 3/day and strict candidate count 0(거래 밀도 일 3회 미만, 엄격 후보 0개)",
            "salvage_value": "model score carries OOS short-quality clue(모델 점수는 표본외 숏 품질 단서를 가짐)",
            "reopen_condition": "density/PF bridge must keep validation and OOS density>=3 with positive net(밀도/PF 브리지가 검증과 표본외 밀도 3 이상과 순수익 양수를 동시에 유지해야 함)",
            "do_not_repeat": "do not package OOS-only low-density seed(OOS 전용 저밀도 씨앗을 패키지하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "dr01_density_pf_bridge_reseed",
            "seed": "DP ONNX seed has OOS net/PF clue but density below 3/day(DP ONNX 씨앗은 OOS 순수익/PF 단서가 있으나 밀도 일 3회 미만)",
            "target_question": "Can hybrid model score + native probability/session rule lift density to 3/day without PF collapse?(모델 점수+기존 확률/세션 규칙 조합이 PF 붕괴 없이 밀도를 일 3회로 올릴 수 있는가?)",
            "must_keep": "train/validation/OOS split(학습/검증/표본외 분할), no trade splitting(거래 쪼개기 금지), ONNX smoke boundary(ONNX 스모크 경계)",
            "avoid": "risk multiplier only(위험 배수만), OOS-only package(OOS 전용 패키지), density without PF lift(PF 상승 없는 밀도)",
            "candidate_ideas": "hybrid score with p_short margin(모델 점수와 p_short 마진 결합), adaptive max hold(적응형 최대 보유), session-quality bridge(세션 품질 브리지), density floor search(밀도 하한 탐색)",
            "effect": "DR은 낮은 밀도 단서를 재사용 가능한 밀도/PF 브리지로 시험합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(REVIEW_SUMMARY, summary)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364DR_QUEUE, queue)
    return summary, package, failure, queue


def build_final(dp_final: Mapping[str, Any], summary: Mapping[str, Any], created_at: str, gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_model_id": summary["selected_model_id"],
        "selected_validation_net": summary["selected_validation_net"],
        "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
        "selected_validation_trade_density": summary["selected_validation_trade_density"],
        "selected_oos_net": summary["selected_oos_net"],
        "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
        "selected_oos_trade_density": summary["selected_oos_trade_density"],
        "strict_candidate_count": summary["strict_candidate_count"],
        "onnx_smoke_pass_rows": summary["onnx_smoke_pass_rows"],
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    dp_gates = read_csv(dp.GATE_AUDIT)
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "DP 입력을 모두 연결했습니다."),
        ("dp_gate_inheritance_gate", not dp_gates.empty and all(dp_gates["status"].astype(str) == "passed"), dp.GATE_AUDIT, "DP 게이트 통과 상태를 상속했습니다."),
        ("model_smoke_review_gate", exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "ONNX smoke(온엑스 스모크)와 선택 모델을 검토했습니다."),
        ("strict_contract_review_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "엄격 후보 부재를 실패 기억으로 기록했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "패키지를 열지 않는 결정을 기록했습니다."),
        ("next_queue_gate", exists(RUN364DR_QUEUE), RUN364DR_QUEUE, "DR 밀도/PF 브리지 대기열을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    return [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(dp.ONNX_SMOKE_REPORT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "density>=3/day strict pass(일 3회 이상 엄격 통과)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "model_validation_boundary": "OOS clue but validation/density not enough(OOS 단서이나 검증/밀도 부족)", "runtime_package": "not_opened"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"OOS net/PF {final['selected_oos_net']} / {final['selected_oos_profit_factor']} with density {final['selected_oos_trade_density']}", "likely_drivers": ["short-source model score(숏 원천 모델 점수)", "fixed-hold short-only replay(고정 보유 숏 전용 재생)"], "failure_driver": "density below objective(목표보다 낮은 밀도)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_review_no_package(검토 연결, 패키지 없음)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "OOS clue(표본외 단서)를 운영 주장으로 올리지 않습니다."})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return dp.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], summary: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DQ h17 short-source model/label reseed review(17시 숏 원천 모델/라벨 재시드 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_package(런타임 패키지): `not_opened(열지 않음)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Review Summary(검토 요약)

{markdown_table(summary, ['selected_model_id', 'selected_validation_net', 'selected_validation_profit_factor', 'selected_validation_trade_density', 'selected_oos_net', 'selected_oos_profit_factor', 'selected_oos_trade_density', 'strict_candidate_count', 'review_status'])}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'selected_oos_net', 'selected_oos_profit_factor', 'selected_oos_trade_density', 'next_run_id'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'why_failed', 'salvage_value', 'reopen_condition', 'do_not_repeat'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is review-only(검토 전용)입니다. ONNX smoke(온엑스 스모크)는 model artifact sanity(모델 산출물 점검)일 뿐이고, MT5 execution(MT5 실행), runtime package(런타임 패키지), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DQ decision(결정): short-source model/label reseed review(숏 원천 모델/라벨 재시드 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- selected OOS net/PF/density(선택 표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- runtime package(런타임 패키지): `not_opened(열지 않음)`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DR은 OOS clue(표본외 단서)를 density/PF bridge(밀도/PF 브리지)로 재시험합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DQ__{RUN_ID}", f"\n- run364DQ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - short-source model/label reseed review(숏 원천 모델/라벨 재시드 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DQ__{RUN_ID}", f"\n<!-- run364DQ__{RUN_ID} -->\n\n## run364DQ Short-Source Model/Label Review(숏 원천 모델/라벨 검토)\n\nAction(행동): DP ONNX seed(DP ONNX 씨앗)의 OOS clue(표본외 단서)와 density gap(밀도 차이)을 검토했습니다.\n\nEffect(효과): 패키지는 열지 않고 `{NEXT_RUN_ID}`에서 density/PF bridge(밀도/PF 브리지)를 탐색합니다.\n")
    append_text_once(STAGE_README, f"run364DQ__{RUN_ID}", f"\n<!-- run364DQ__{RUN_ID} -->\n## run364DQ review(검토)\n\nDP ONNX seed(DP ONNX 씨앗)는 OOS clue(표본외 단서)지만 package(패키지)는 아닙니다. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(STAGE_BRIEF, {"- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`", "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`", "- selection_status": f"- selection_status(선택 상태): `{STATUS}`", "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`"}, bom=True)
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364DQ` reviewed(검토 완료) DP short-source model/label reseed(DP 숏 원천 모델/라벨 재시드). Selected model(선택 모델)은 `{final['selected_model_id']}`이고 OOS net/PF/density(표본외 순수익/PF/밀도)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다. strict_candidate_count(엄격 후보 수)는 `{final['strict_candidate_count']}`라 runtime package(런타임 패키지)는 열지 않았습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 hybrid model score + native probability/session rule(모델 점수 + 기존 확률/세션 규칙)로 density/PF bridge(밀도/PF 브리지)를 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): DP ONNX seed(DP ONNX 씨앗)는 OOS clue(표본외 단서)이지만 density below 3/day(일 3회 미만 밀도)라 package(패키지)가 아닙니다.

Selected model(선택 모델): `{final['selected_model_id']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DQ__{RUN_ID}", f"\n<!-- run364DQ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DP ONNX seed(DP ONNX 씨앗); package not opened(패키지 열지 않음); next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364DQ__{RUN_ID}", f"\n<!-- run364DQ__{RUN_ID} -->\n- `{RUN_ID}`: DP selected model(선택 모델) `{final['selected_model_id']}` preserved as OOS clue(표본외 단서). Effect(효과): DR은 density/PF bridge(밀도/PF 브리지)를 탐색합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DQ__density_below_min__{RUN_ID}", f"\n<!-- run364DQ__density_below_min__{RUN_ID} -->\n- `{RUN_ID}`: DP ONNX seed(DP ONNX 씨앗)는 density below 3/day(일 3회 미만 밀도)라 runtime package(런타임 패키지)로 열지 않았습니다. Effect(효과): OOS-only low-density clue(OOS 전용 저밀도 단서)를 운영 후보로 과장하지 않습니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "result_review(결과 검토)",
        "scoreboard_lane": "model_label_reseed_review(모델/라벨 재시드 검토)",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "evidence_boundary": "proxy_review_no_mt5_no_package(프록시 검토, MT5/패키지 없음)",
        "question": "Should DP ONNX seed move to runtime package?(DP ONNX 씨앗을 런타임 패키지로 넘길 것인가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_oos_net"],
        "profit_factor": final["selected_oos_profit_factor"],
        "trade_density_per_feature_day": final["selected_oos_trade_density"],
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(REVIEW_SUMMARY),
        "primary_kpi": f"oos_net={final['selected_oos_net']};oos_pf={final['selected_oos_profit_factor']};oos_density={final['selected_oos_trade_density']}",
        "guardrail_kpi": "package=not_opened;runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": "DQ model reseed review(DQ 모델 재시드 검토)", "status": status, "view": record_view, "tier": tier_scope, "metric_scope": "proxy_review(프록시 검토)"}
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "trade_density_per_feature_day"]:
                row[key] = ""
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("review_summary", REVIEW_SUMMARY, "DQ review summary(DQ 검토 요약)."),
        ("package_decision", PACKAGE_DECISION, "Package decision(패키지 결정)."),
        ("failure_memory", FAILURE_MEMORY, "Failure memory(실패 기억)."),
        ("queue", RUN364DR_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DQ producer script(DQ 생산 스크립트)."),
    ]:
        if exists(path):
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": artifact_type, "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{artifact_type}", "notes": notes})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    dp_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    summary, package, failure, _queue = build_reviews(dp_final)
    created_at = now_utc()
    gates = gate_rows(final_written=False)
    final = build_final(dp_final, summary[0], created_at, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final_written=True)
    final = build_final(dp_final, summary[0], created_at, gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, summary, package, failure, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
