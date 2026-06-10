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
from stage_pipelines.stage364 import train_h17_validation_stability_regime_source_reseed_without_db as dv  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dv.STAGE_ID
RUN_NUMBER = "run364DW"
RUN_ID = "run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1"
PARENT_RUN_ID = dv.RUN_ID
NEXT_RUN_ID = "run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1"

STATUS = "completed_stage364DW_validation_stability_review_package_rejected_open_dx_no_authority"
JUDGMENT = "negative_validation_stability_review_density_below_trade_objective_no_package_no_authority"
DECISION = "stage364DW_reject_package_open_run364DX_density_recovery_reseed"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_validation_stability_reseed_rejected_no_runtime_package_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = dv.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "dw_validation_stability_review_summary.csv"
DENSITY_FAILURE = RUN_DIR / "density_failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364DX_QUEUE = RUN_DIR / "run364DX_density_recovery_reseed_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DW_h17_validation_stability_regime_source_reseed_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DW_h17_validation_stability_regime_source_reseed_review.md"
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
    dv.FINAL_DECISION,
    dv.GATE_AUDIT,
    dv.TRADE_SURFACE,
    dv.SELECTED_CANDIDATE,
    dv.SELECTED_TRADE_TAPE,
    dv.MONTH_STABILITY,
    dv.COST_STRESS,
    dv.MODEL_SCORECARD,
    dv.ONNX_SMOKE_REPORT,
    dv.DATA_INTEGRITY_AUDIT,
    dv.RUN364DW_QUEUE,
    dv.RUN_EVIDENCE_RECEIPT,
    dv.MODEL_RECEIPT,
    dv.ATTRIBUTION_RECEIPT,
    dv.JUDGMENT_RECEIPT,
    dv.LINEAGE_RECEIPT,
    dv.CLAIM_RECEIPT,
    dv.RUN_MANIFEST,
    dv.REPORT_PATH,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    DENSITY_FAILURE,
    PACKAGE_DECISION,
    RUN364DX_QUEUE,
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
    return dv.rel(path)


def exists(path: Path | str) -> bool:
    return dv.exists(path)


def sha(path: Path | str) -> str:
    return dv.sha(path)


def read_json(path: Path) -> Any:
    return dv.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dv.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dv.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): value for key, value in row.items()} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in materialized:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields or ["empty"]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dv.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dv.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dv.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dv.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing DW inputs(DW 입력 누락): " + ", ".join(missing))
    parent = read_json(dv.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DV next_run_id mismatch(DV 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DV forbidden claim(DV 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(dv.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DV gate audit(DV 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DW review input(DW 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-model-validation(모델 검증)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "review_subject": parent["selected_model_id"],
            "review_question": "Does DV validation-stability reseed repair validation quality enough for package work?(DV 검증 안정성 재시드가 패키지 작업에 충분할 만큼 검증 품질을 고쳤는가?)",
            "decision_use": "Reject package if density remains below 3/day(밀도가 일 3회 미만이면 패키지를 거절합니다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def review_rows(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = read_csv(dv.TRADE_SURFACE)
    density_both = surface[(surface["validation_trade_density"].map(as_float) >= 3.0) & (surface["oos_trade_density"].map(as_float) >= 3.0)]
    density_net_pf = density_both[
        (density_both["validation_net"].map(as_float) > 0)
        & (density_both["oos_net"].map(as_float) > 0)
        & (density_both["validation_profit_factor"].map(as_float) >= 1.20)
        & (density_both["oos_profit_factor"].map(as_float) >= 1.20)
    ]
    costs = read_csv(dv.COST_STRESS)
    validation_cost09 = costs[(costs["split"].astype(str) == "validation") & (costs["cost_per_trade"].map(as_float) == 0.9)]
    oos_cost09 = costs[(costs["split"].astype(str) == "oos") & (costs["cost_per_trade"].map(as_float) == 0.9)]
    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": parent["selected_model_id"],
            "selected_filter": parent["selected_stability_filter"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_validation_trade_count": parent["selected_validation_trade_count"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "selected_oos_trade_count": parent["selected_oos_trade_count"],
            "strict_candidate_count": parent["strict_candidate_count"],
            "density_both_count": int(len(density_both)),
            "density_net_pf_count": int(len(density_net_pf)),
            "validation_cost_0p9_net": validation_cost09.iloc[0].get("net_profit", "") if not validation_cost09.empty else "",
            "oos_cost_0p9_net": oos_cost09.iloc[0].get("net_profit", "") if not oos_cost09.empty else "",
            "review_status": "package_rejected_open_dx(패키지 거절, DX 열기)",
            "effect": "validation/OOS 수익성은 개선됐지만 trade density(거래 밀도)가 목표보다 낮아 패키지로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "dw01_validation_stability_profit_ok_density_low",
            "observation": f"validation/OOS density={parent['selected_validation_trade_density']}/{parent['selected_oos_trade_density']}; strict={parent['strict_candidate_count']}",
            "why_failed": "profitability recovered but trade density is below 3/day(수익성은 회복됐지만 거래 밀도가 일 3회 미만)",
            "salvage_value": "validation and OOS net/PF are both positive(검증과 표본외 순수익/PF가 모두 양수)",
            "reopen_condition": "density recovery must keep validation/OOS net positive and PF>=1.20 while lifting density>=3(밀도 회복은 검증/표본외 양수 순수익과 PF 1.20 이상을 유지하면서 밀도 3 이상을 만들어야 함)",
            "do_not_repeat": "do not widen density by accepting validation loss(검증 손실을 받아들이며 밀도만 넓히지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    package = [
        {
            "run_id": RUN_ID,
            "decision": "do_not_open_runtime_package(런타임 패키지 열지 않음)",
            "reason": "strict_candidate_count=0 because density is below 3/day(밀도가 일 3회 미만이라 엄격 후보 0개)",
            "selected_model_id": parent["selected_model_id"],
            "next_run_id": NEXT_RUN_ID,
            "effect": "좋은 PF를 거래수 부족 모델로 과대평가하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "dx01_density_recovery_reseed",
            "seed": "DV repaired validation/OOS net and PF but density is far below 3/day(DV는 검증/표본외 순수익과 PF를 고쳤지만 밀도가 일 3회보다 훨씬 낮음)",
            "target_question": "Can density recovery lift trades to 3/day without losing validation/OOS PF and net?(밀도 회복이 검증/표본외 PF와 순수익을 잃지 않고 거래를 일 3회까지 올릴 수 있는가?)",
            "must_keep": "validation/OOS net positive(검증/표본외 순수익 양수), PF>=1.20(PF 1.20 이상), no trade splitting(거래 쪼개기 금지), no package before review(검토 전 패키지 금지)",
            "avoid": "validation loss for density(밀도를 위해 검증 손실 허용), OOS-only density(OOS 전용 밀도), risk multiplier only(위험 배수만)",
            "candidate_ideas": "lower density target with PF floor(PF 하한 포함 낮은 밀도 목표), score band expansion(점수 구간 확장), validation-positive month broadening(검증 양수 월 확장), session-adaptive threshold(세션 적응 임계값), side-balanced density fill(방향 균형 밀도 보충)",
            "effect": "수익성 회복 단서를 다음 밀도 회복 탐색의 보호 조건으로 씁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(REVIEW_SUMMARY, summary)
    write_csv(DENSITY_FAILURE, failure)
    write_csv(PACKAGE_DECISION, package)
    write_csv(RUN364DX_QUEUE, queue)
    return summary, failure, package, queue


def final_payload(parent: Mapping[str, Any], summary: Mapping[str, Any], created_at: str, gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_model_id": parent["selected_model_id"],
        "selected_validation_net": parent["selected_validation_net"],
        "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
        "selected_validation_trade_density": parent["selected_validation_trade_density"],
        "selected_oos_net": parent["selected_oos_net"],
        "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
        "selected_oos_trade_density": parent["selected_oos_trade_density"],
        "strict_candidate_count": parent["strict_candidate_count"],
        "density_both_count": summary["density_both_count"],
        "density_net_pf_count": summary["density_net_pf_count"],
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
    dv_gates = read_csv(dv.GATE_AUDIT)
    final = read_json(FINAL_DECISION) if exists(FINAL_DECISION) else {}
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), INPUT_MANIFEST, "DV 입력 산출물을 모두 연결했습니다."),
        ("dv_gate_inheritance_gate", not dv_gates.empty and all(dv_gates["status"].astype(str) == "passed"), dv.GATE_AUDIT, "DV 게이트 통과 상태를 상속했습니다."),
        ("review_summary_gate", exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "수익성과 밀도 차이를 요약했습니다."),
        ("density_failure_gate", exists(DENSITY_FAILURE) and as_float(final.get("selected_validation_trade_density", 0)) < 3, DENSITY_FAILURE, "밀도 실패를 실패 기억으로 기록했습니다."),
        ("package_rejection_gate", exists(PACKAGE_DECISION) and int(final.get("strict_candidate_count", 0)) == 0, PACKAGE_DECISION, "패키지를 열지 않는 결정을 기록했습니다."),
        ("next_queue_gate", exists(RUN364DX_QUEUE), RUN364DX_QUEUE, "DX 밀도 회복 재시드 대기열을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    return [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(DENSITY_FAILURE), rel(PACKAGE_DECISION), rel(dv.COST_STRESS)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "density>=3/day strict pass(일 3회 이상 엄격 통과)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "selected_model_id": final["selected_model_id"], "model_validation_boundary": "net/PF positive but density below objective(순수익/PF 양수지만 밀도 목표 미달)", "runtime_package": "not_opened"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"validation/OOS net positive {final['selected_validation_net']}/{final['selected_oos_net']} but density {final['selected_validation_trade_density']}/{final['selected_oos_trade_density']}", "likely_drivers": ["validation-stability filter(검증 안정성 필터)", "sparse score selection(희박한 점수 선택)"], "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_review_no_package(검토 연결, 패키지 없음)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "밀도 부족 모델을 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DW H17 Validation-Stability Reseed Review(검증 안정성 재시드 검토)

Created(생성): {final['created_at_utc']}

## Review(검토)

Action(행동): DV validation-stability reseed(DV 검증 안정성 재시드)를 package(패키지) 후보로 검토했습니다.

Effect(효과): validation/OOS net/PF(검증/표본외 순수익/PF)는 살아났지만 density(밀도)가 목표 미달이라 package(패키지)를 열지 않습니다.

## Decision(결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- density_both_count(양쪽 밀도 통과 수): `{final['density_both_count']}`
- density_net_pf_count(양쪽 밀도+순수익+PF 통과 수): `{final['density_net_pf_count']}`

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`{NEXT_RUN_ID}`에서 density recovery(밀도 회복)를 탐색합니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    decision_doc = f"""# Decision(결정): stage364DW validation-stability review(검증 안정성 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): DV 결과를 package(패키지) 적격성 기준으로 검토했습니다.

Effect(효과): density(밀도) 부족을 다음 DX 탐색의 중심 제약으로 전환합니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364DW__{RUN_ID}", f"\n- run364DW__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - validation-stability reseed review(검증 안정성 재시드 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DW__{RUN_ID}", f"\n<!-- run364DW__{RUN_ID} -->\n\n## run364DW Validation-Stability Review(검증 안정성 검토)\n\nAction(행동): DV 수익성 회복과 밀도 실패를 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 density recovery(밀도 회복)를 탐색합니다.\n")
    append_text_once(STAGE_README, f"run364DW__{RUN_ID}", f"\n<!-- run364DW__{RUN_ID} -->\n## run364DW review(검토)\n\nDV는 net/PF(순수익/PF)를 회복했지만 density(밀도)가 낮아 package rejected(패키지 거절)입니다. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DW` reviewed(검토 완료) DV validation-stability reseed(DV 검증 안정성 재시드). Validation/OOS net/PF(검증/표본외 순수익/PF)는 양수지만 density(밀도)는 `{final['selected_validation_trade_density']}` / `{final['selected_oos_trade_density']}`로 일 3회 목표에 못 미칩니다. runtime package(런타임 패키지)는 열지 않았습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density recovery reseed(밀도 회복 재시드)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): DV validation-stability reseed(DV 검증 안정성 재시드)는 validation/OOS net/PF(검증/표본외 순수익/PF)를 회복했지만 density(밀도)가 낮아 package rejected(패키지 거절)입니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Next seed(다음 씨앗): density recovery reseed(밀도 회복 재시드).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DW__{RUN_ID}", f"\n<!-- run364DW__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DV validation-stability reseed(검증 안정성 재시드); package rejected(패키지 거절); next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364DW__{RUN_ID}", f"\n<!-- run364DW__{RUN_ID} -->\n- `{RUN_ID}`: DV model(DV 모델)은 validation/OOS net/PF(검증/표본외 순수익/PF)를 회복했지만 density(밀도)가 낮습니다. Effect(효과): 다음 탐색은 수익성 보호 조건 아래 density recovery(밀도 회복)를 시도합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DW__density_below_objective__{RUN_ID}", f"\n<!-- run364DW__density_below_objective__{RUN_ID} -->\n- `{RUN_ID}`: DV validation-stability model(DV 검증 안정성 모델)은 density below 3/day(일 3회 미만 밀도)로 package rejected(패키지 거절)입니다. Effect(효과): 높은 PF를 낮은 거래수 모델로 과장하지 않습니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Does DV validation-stability reseed repair validation quality enough for package work?(DV 검증 안정성 재시드가 패키지 작업에 충분할 만큼 검증 품질을 고쳤는가?)", "next_action": NEXT_RUN_ID, "notes": f"density={final['selected_validation_trade_density']}/{final['selected_oos_trade_density']};package=not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "DW validation-stability review(DW 검증 안정성 검토)", "metric_scope": "proxy_review(Python 프록시 검토)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "proxy_review_no_mt5_no_package(프록시 검토, MT5/패키지 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "run_family": "kpi_evidence(KPI 근거)", "run_type": "proxy_review(프록시 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(REVIEW_SUMMARY), "selected_net_profit": final["selected_oos_net"], "selected_profit_factor": final["selected_oos_profit_factor"], "selected_trade_density": final["selected_oos_trade_density"]}], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "DW validation-stability review artifact(DW 검증 안정성 검토 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    summary, failure, package, _queue = review_rows(parent)
    created_at = now_utc()
    gates = gate_rows(final_written=False)
    final = final_payload(parent, summary[0], created_at, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final_written=True)
    final = final_payload(parent, summary[0], created_at, gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
