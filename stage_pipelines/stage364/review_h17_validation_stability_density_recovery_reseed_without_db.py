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
from stage_pipelines.stage364 import train_h17_validation_stability_density_recovery_reseed_without_db as dx  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dx.STAGE_ID
RUN_NUMBER = "run364DY"
RUN_ID = "run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1"
PARENT_RUN_ID = dx.RUN_ID
NEXT_RUN_ID = "run364DZ_train_h17_density_pf_balance_reseed_without_db_v1"

STATUS = "completed_stage364DY_density_recovery_review_package_rejected_open_dz_no_authority"
JUDGMENT = "negative_density_recovery_review_oos_pf_net_failure_no_package_no_authority"
DECISION = "stage364DY_reject_package_open_run364DZ_density_pf_balance_reseed"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_density_recovery_reseed_rejected_no_runtime_package_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = dx.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "dy_density_recovery_review_summary.csv"
FAILURE_MEMORY = RUN_DIR / "density_pf_failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364DZ_QUEUE = RUN_DIR / "run364DZ_density_pf_balance_reseed_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DY_h17_validation_stability_density_recovery_reseed_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DY_h17_validation_stability_density_recovery_reseed_review.md"
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
    dx.FINAL_DECISION,
    dx.GATE_AUDIT,
    dx.TRADE_SURFACE,
    dx.SELECTED_CANDIDATE,
    dx.SELECTED_TRADE_TAPE,
    dx.MONTH_STABILITY,
    dx.COST_STRESS,
    dx.MODEL_SCORECARD,
    dx.ONNX_SMOKE_REPORT,
    dx.DATA_INTEGRITY_AUDIT,
    dx.RUN364DY_QUEUE,
    dx.RUN_EVIDENCE_RECEIPT,
    dx.MODEL_RECEIPT,
    dx.ATTRIBUTION_RECEIPT,
    dx.JUDGMENT_RECEIPT,
    dx.LINEAGE_RECEIPT,
    dx.CLAIM_RECEIPT,
    dx.RUN_MANIFEST,
    dx.REPORT_PATH,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_MEMORY,
    PACKAGE_DECISION,
    RUN364DZ_QUEUE,
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
    return dx.rel(path)


def exists(path: Path | str) -> bool:
    return dx.exists(path)


def sha(path: Path | str) -> str:
    return dx.sha(path)


def read_json(path: Path) -> Any:
    return dx.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dx.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dx.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = [{str(key): value for key, value in row.items()} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields or ["empty"]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dx.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dx.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dx.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dx.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing DY inputs(DY 입력 누락): " + ", ".join(missing))
    parent = read_json(dx.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DX next_run_id mismatch(DX 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DX forbidden claim(DX 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(dx.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DX gate audit(DX 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {"run_id": RUN_ID, "input_path": rel(path), "exists": exists(path), "sha256": sha(path) if exists(path) and io_path(path).is_file() else "", "input_role": "DY review input(DY 검토 입력)", "claim_boundary": CLAIM_BOUNDARY}
        for path in INPUT_FILES
    ]


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(WORK_PACKET, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "primary_family": "kpi_evidence(KPI 근거)", "primary_skill": "obsidian-result-judgment(결과 판정)", "support_skills": ["obsidian-model-validation(모델 검증)", "obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)"], "review_subject": parent["selected_model_id"], "review_question": "Did DX recover density without losing validation/OOS PF and net?(DX가 검증/표본외 PF와 순수익을 잃지 않고 밀도를 회복했는가?)", "claim_boundary": CLAIM_BOUNDARY})


def review_rows(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = read_csv(dx.TRADE_SURFACE)
    density_both = surface[(surface["validation_trade_density"].map(as_float) >= 3.0) & (surface["oos_trade_density"].map(as_float) >= 3.0)]
    density_net = density_both[(density_both["validation_net"].map(as_float) > 0) & (density_both["oos_net"].map(as_float) > 0)]
    density_net_pf = density_net[(density_net["validation_profit_factor"].map(as_float) >= 1.20) & (density_net["oos_profit_factor"].map(as_float) >= 1.20)]
    net_pf = surface[(surface["validation_net"].map(as_float) > 0) & (surface["oos_net"].map(as_float) > 0) & (surface["validation_profit_factor"].map(as_float) >= 1.20) & (surface["oos_profit_factor"].map(as_float) >= 1.20)]
    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": parent["selected_model_id"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "strict_candidate_count": parent["strict_candidate_count"],
            "density_both_count": int(len(density_both)),
            "density_net_count": int(len(density_net)),
            "density_net_pf_count": int(len(density_net_pf)),
            "net_pf_count": int(len(net_pf)),
            "review_status": "package_rejected_open_dz(패키지 거절, DZ 열기)",
            "effect": "density(밀도)는 회복됐지만 OOS net/PF(표본외 순수익/PF)가 깨져 패키지로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {"run_id": RUN_ID, "memory_id": "dy01_density_recovered_oos_pf_net_failed", "observation": f"selected validation/OOS={parent['selected_validation_net']}/{parent['selected_oos_net']}; density={parent['selected_validation_trade_density']}/{parent['selected_oos_trade_density']}; density_net_pf={len(density_net_pf)}", "why_failed": "density recovery broke OOS net/PF(밀도 회복이 표본외 순수익/PF를 깨뜨림)", "salvage_value": "density_both and density_net rows exist(양쪽 밀도 통과와 양쪽 순수익 통과 행은 존재)", "reopen_condition": "balance filter must keep density>=3 and lift OOS PF/net(균형 필터가 밀도 3 이상을 유지하면서 표본외 PF/순수익을 회복해야 함)", "do_not_repeat": "do not choose validation-positive density when OOS is negative(OOS가 음수인데 검증 양수 밀도만 선택하지 않음)", "claim_boundary": CLAIM_BOUNDARY}
    ]
    package = [
        {"run_id": RUN_ID, "decision": "do_not_open_runtime_package(런타임 패키지 열지 않음)", "reason": "selected OOS net/PF are below zero/one and strict_candidate_count=0(선택 표본외 순수익/PF가 음수/1 미만이고 엄격 후보 0개)", "selected_model_id": parent["selected_model_id"], "next_run_id": NEXT_RUN_ID, "effect": "검증 전용 밀도 회복을 운영 후보로 과장하지 않습니다.", "claim_boundary": CLAIM_BOUNDARY}
    ]
    queue = [
        {"run_id": RUN_ID, "next_run_id": NEXT_RUN_ID, "queue_rank": 1, "queue_id": "dz01_density_pf_balance_reseed", "seed": "DX recovered density but OOS net/PF failed(DX는 밀도를 회복했지만 표본외 순수익/PF가 실패함)", "target_question": "Can density/PF balance keep density>=3 while restoring OOS net and PF?(밀도/PF 균형이 밀도 3 이상을 유지하면서 표본외 순수익과 PF를 회복할 수 있는가?)", "must_keep": "density>=3 both splits(양쪽 밀도 3 이상), validation net/PF positive(검증 순수익/PF 양호), no trade splitting(거래 쪼개기 금지), no package before review(검토 전 패키지 금지)", "avoid": "validation-only optimization(검증 전용 최적화), OOS-only rescue(OOS 전용 구조), risk multiplier only(위험 배수만)", "candidate_ideas": "PF floor inside density fill(밀도 보충 안의 PF 하한), OOS-negative month/session guard(표본외 음수 월/세션 가드), side-payoff balance(방향별 손익 균형), high-density score band pruning(고밀도 점수 구간 가지치기), cost-stress-aware threshold(비용 압박 인식 임계값)", "effect": "밀도 회복 단서와 OOS 실패 기억을 동시에 다음 탐색 조건으로 씁니다.", "claim_boundary": CLAIM_BOUNDARY}
    ]
    write_csv(REVIEW_SUMMARY, summary)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(PACKAGE_DECISION, package)
    write_csv(RUN364DZ_QUEUE, queue)
    return summary, failure, package, queue


def final_payload(parent: Mapping[str, Any], summary: Mapping[str, Any], created_at: str, gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "selected_model_id": parent["selected_model_id"], "selected_validation_net": parent["selected_validation_net"], "selected_validation_profit_factor": parent["selected_validation_profit_factor"], "selected_validation_trade_density": parent["selected_validation_trade_density"], "selected_oos_net": parent["selected_oos_net"], "selected_oos_profit_factor": parent["selected_oos_profit_factor"], "selected_oos_trade_density": parent["selected_oos_trade_density"], "strict_candidate_count": parent["strict_candidate_count"], "density_both_count": summary["density_both_count"], "density_net_count": summary["density_net_count"], "density_net_pf_count": summary["density_net_pf_count"], "net_pf_count": summary["net_pf_count"], "runtime_package": "not_opened", "new_mt5_execution": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "created_at_utc": created_at, "claim_boundary": CLAIM_BOUNDARY, "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "report_path": rel(REPORT_PATH), "final_decision": rel(FINAL_DECISION)}


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    dx_gates = read_csv(dx.GATE_AUDIT)
    final = read_json(FINAL_DECISION) if exists(FINAL_DECISION) else {}
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), INPUT_MANIFEST, "DX 입력 산출물을 모두 연결했습니다."),
        ("dx_gate_inheritance_gate", not dx_gates.empty and all(dx_gates["status"].astype(str) == "passed"), dx.GATE_AUDIT, "DX 게이트 통과 상태를 상속했습니다."),
        ("review_summary_gate", exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "밀도와 OOS 실패를 요약했습니다."),
        ("oos_failure_gate", exists(FAILURE_MEMORY) and as_float(final.get("selected_oos_net", 0)) < 0, FAILURE_MEMORY, "OOS 실패를 실패 기억으로 기록했습니다."),
        ("package_rejection_gate", exists(PACKAGE_DECISION) and int(final.get("strict_candidate_count", 0)) == 0, PACKAGE_DECISION, "패키지를 열지 않는 결정을 기록했습니다."),
        ("next_queue_gate", exists(RUN364DZ_QUEUE), RUN364DZ_QUEUE, "DZ 밀도/PF 균형 재시드 대기열을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    return [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(FAILURE_MEMORY), rel(PACKAGE_DECISION), rel(dx.TRADE_SURFACE)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "cross-split density/net/PF pass(교차 분할 밀도/순수익/PF 통과)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "selected_model_id": final["selected_model_id"], "validation_judgment": JUDGMENT, "runtime_package": "not_opened"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"density recovered {final['selected_validation_trade_density']}/{final['selected_oos_trade_density']} but OOS net/PF {final['selected_oos_net']}/{final['selected_oos_profit_factor']}", "likely_drivers": ["shorter-hold density expansion(짧은 보유 밀도 확장)", "OOS payoff decay(표본외 손익 저하)"], "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_review_no_package(검토 연결, 패키지 없음)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "OOS 실패 모델을 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DY H17 Density Recovery Reseed Review(밀도 회복 재시드 검토)

Created(생성): {final['created_at_utc']}

## Decision(결정)

Action(행동): DX density recovery(DX 밀도 회복)를 package(패키지) 후보로 검토했습니다.

Effect(효과): density(밀도)는 회복됐지만 OOS net/PF(표본외 순수익/PF)가 깨져 package(패키지)를 열지 않습니다.

- judgment(판정): `{JUDGMENT}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- density_both_count(양쪽 밀도 통과 수): `{final['density_both_count']}`
- density_net_count(양쪽 밀도+순수익 통과 수): `{final['density_net_count']}`
- density_net_pf_count(양쪽 밀도+순수익+PF 통과 수): `{final['density_net_pf_count']}`

## Next(다음)

`{NEXT_RUN_ID}`에서 density/PF balance(밀도/PF 균형)를 탐색합니다.

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    decision_doc = f"""# Decision(결정): stage364DY density recovery review(밀도 회복 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): DX 결과를 package(패키지) 적격성 기준으로 검토했습니다.

Effect(효과): OOS PF/net failure(표본외 PF/순수익 실패)를 다음 DZ 탐색의 중심 제약으로 전환합니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364DY__{RUN_ID}", f"\n- run364DY__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density recovery review(밀도 회복 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DY__{RUN_ID}", f"\n<!-- run364DY__{RUN_ID} -->\n\n## run364DY Density Recovery Review(밀도 회복 검토)\n\nAction(행동): DX 밀도 회복과 OOS 실패를 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 density/PF balance(밀도/PF 균형)를 탐색합니다.\n")
    append_text_once(STAGE_README, f"run364DY__{RUN_ID}", f"\n<!-- run364DY__{RUN_ID} -->\n## run364DY review(검토)\n\nDX는 density(밀도)를 회복했지만 OOS net/PF(표본외 순수익/PF)가 깨져 package rejected(패키지 거절)입니다. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DY` reviewed(검토 완료) DX density recovery reseed(DX 밀도 회복 재시드). Density(밀도)는 `{final['selected_validation_trade_density']}` / `{final['selected_oos_trade_density']}`로 회복됐지만 OOS net/PF(표본외 순수익/PF)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}`라서 실패입니다. runtime package(런타임 패키지)는 열지 않았습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density/PF balance reseed(밀도/PF 균형 재시드)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): DX density recovery reseed(DX 밀도 회복 재시드)는 validation density(검증 밀도)는 살렸지만 OOS net/PF(표본외 순수익/PF)가 실패해 package rejected(패키지 거절)입니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Next seed(다음 씨앗): density/PF balance reseed(밀도/PF 균형 재시드).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DY__{RUN_ID}", f"\n<!-- run364DY__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DX density recovery(밀도 회복); package rejected(패키지 거절); next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364DY__{RUN_ID}", f"\n<!-- run364DY__{RUN_ID} -->\n- `{RUN_ID}`: DX는 density(밀도)를 회복했지만 OOS net/PF(표본외 순수익/PF)가 실패했습니다. Effect(효과): 다음 탐색은 density/PF balance(밀도/PF 균형)를 직접 겨냥합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DY__oos_pf_net_failed__{RUN_ID}", f"\n<!-- run364DY__oos_pf_net_failed__{RUN_ID} -->\n- `{RUN_ID}`: DX density recovery(DX 밀도 회복)는 OOS net/PF failure(표본외 순수익/PF 실패)로 package rejected(패키지 거절)입니다. Effect(효과): 검증 전용 밀도 회복을 운영 근거로 쓰지 않습니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Did DX recover density without losing validation/OOS PF and net?(DX가 검증/표본외 PF와 순수익을 잃지 않고 밀도를 회복했는가?)", "next_action": NEXT_RUN_ID, "notes": f"density_net={final['density_net_count']};density_net_pf={final['density_net_pf_count']}", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS), ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"), ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)")]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "DY density recovery review(DY 밀도 회복 검토)", "metric_scope": "proxy_review(Python 프록시 검토)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "proxy_review_no_mt5_no_package(프록시 검토, MT5/패키지 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "run_family": "kpi_evidence(KPI 근거)", "run_type": "proxy_review(프록시 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(REVIEW_SUMMARY), "selected_net_profit": final["selected_oos_net"], "selected_profit_factor": final["selected_oos_profit_factor"], "selected_trade_density": final["selected_oos_trade_density"]}], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "DY density recovery review artifact(DY 밀도 회복 검토 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    summary, _failure, _package, _queue = review_rows(parent)
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
