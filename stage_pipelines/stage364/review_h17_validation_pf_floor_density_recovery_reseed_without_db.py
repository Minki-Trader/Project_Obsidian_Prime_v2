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
from stage_pipelines.stage364 import train_h17_density_pf_balance_reseed_without_db as dz  # noqa: E402
from stage_pipelines.stage364 import train_h17_validation_pf_floor_density_recovery_reseed_without_db as eb  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = eb.STAGE_ID
RUN_NUMBER = "run364EC"
RUN_ID = "run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1"
PARENT_RUN_ID = eb.RUN_ID
NEXT_RUN_ID = "run364ED_train_h17_dual_pf_floor_bridge_reseed_without_db_v1"

STATUS = "completed_stage364EC_validation_pf_floor_review_package_rejected_open_ed_no_authority"
JUDGMENT = "negative_validation_pf_floor_review_dual_pf_below_floor_no_package_no_authority"
DECISION = "stage364EC_reject_package_open_run364ED_dual_pf_floor_bridge_reseed"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_validation_pf_floor_reseed_rejected_no_runtime_package_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = eb.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "ec_validation_pf_floor_review_summary.csv"
FAILURE_MEMORY = RUN_DIR / "dual_pf_floor_failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364ED_QUEUE = RUN_DIR / "run364ED_dual_pf_floor_bridge_reseed_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EC_h17_validation_pf_floor_density_recovery_reseed_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EC_h17_validation_pf_floor_density_recovery_reseed_review.md"
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
    eb.FINAL_DECISION,
    eb.GATE_AUDIT,
    eb.TRADE_SURFACE,
    eb.SELECTED_CANDIDATE,
    eb.SELECTED_TRADE_TAPE,
    eb.MONTH_STABILITY,
    eb.COST_STRESS,
    eb.MODEL_SCORECARD,
    eb.ONNX_SMOKE_REPORT,
    eb.DATA_INTEGRITY_AUDIT,
    eb.RUN364EC_QUEUE,
    eb.RUN_EVIDENCE_RECEIPT,
    eb.MODEL_RECEIPT,
    eb.ATTRIBUTION_RECEIPT,
    eb.JUDGMENT_RECEIPT,
    eb.LINEAGE_RECEIPT,
    eb.CLAIM_RECEIPT,
    eb.RUN_MANIFEST,
    eb.REPORT_PATH,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_MEMORY,
    PACKAGE_DECISION,
    RUN364ED_QUEUE,
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
    return eb.rel(path)


def exists(path: Path | str) -> bool:
    return eb.exists(path)


def sha(path: Path | str) -> str:
    return eb.sha(path)


def read_json(path: Path) -> Any:
    return eb.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    eb.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    eb.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = [{str(key): eb.dz.json_ready(value) for key, value in row.items()} for row in rows]
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
    eb.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    eb.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    eb.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return eb.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EC inputs(EC 입력 누락): " + ", ".join(missing))
    parent = read_json(eb.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EB next_run_id mismatch(EB 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"EB forbidden claim(EB 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(eb.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EB gate audit(EB 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EC validation PF floor review input(EC 검증 PF 바닥 검토 입력)",
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
            "review_question": "Did EB lift validation PF floor without losing OOS density?(EB가 표본외 밀도를 잃지 않고 검증 PF 바닥을 올렸는가?)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def numeric_surface() -> pd.DataFrame:
    surface = read_csv(eb.TRADE_SURFACE)
    for column in [
        "validation_net",
        "validation_profit_factor",
        "validation_trade_density",
        "oos_net",
        "oos_profit_factor",
        "oos_trade_density",
        "selection_score",
    ]:
        surface[column] = pd.to_numeric(surface[column], errors="coerce").fillna(0.0)
    surface["min_pf"] = surface[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    surface["min_net"] = surface[["validation_net", "oos_net"]].min(axis=1)
    return surface


def review_tables(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = numeric_surface()
    density_both = surface[(surface["validation_trade_density"] >= 3.0) & (surface["oos_trade_density"] >= 3.0)]
    density_net = density_both[(density_both["validation_net"] > 0) & (density_both["oos_net"] > 0)]
    pf110 = density_net[(density_net["validation_profit_factor"] >= 1.10) & (density_net["oos_profit_factor"] >= 1.10)]
    pf115 = density_net[(density_net["validation_profit_factor"] >= 1.15) & (density_net["oos_profit_factor"] >= 1.15)]
    pf120 = density_net[(density_net["validation_profit_factor"] >= 1.20) & (density_net["oos_profit_factor"] >= 1.20)]
    best_bridge = density_net.sort_values(["min_pf", "min_net"], ascending=False).iloc[0].to_dict() if not density_net.empty else {}
    selected_validation_pf = as_float(parent["selected_validation_profit_factor"])
    selected_oos_pf = as_float(parent["selected_oos_profit_factor"])
    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": parent["selected_model_id"],
            "selected_filter": parent["selected_stability_filter"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "strict_candidate_count": parent["strict_candidate_count"],
            "density_both_count": int(len(density_both)),
            "density_net_count": int(len(density_net)),
            "pf110_count": int(len(pf110)),
            "pf115_count": int(len(pf115)),
            "pf120_count": int(len(pf120)),
            "best_bridge_model_id": best_bridge.get("model_id", ""),
            "best_bridge_min_pf": best_bridge.get("min_pf", ""),
            "best_bridge_validation_pf": best_bridge.get("validation_profit_factor", ""),
            "best_bridge_oos_pf": best_bridge.get("oos_profit_factor", ""),
            "package_decision": "rejected(거절)",
            "package_reason": f"strict=0;validation_pf={selected_validation_pf};oos_pf={selected_oos_pf};pf110_count={len(pf110)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "ec01_density_net_expanded_but_pf_floor_failed",
            "observation": f"density_net_count={len(density_net)}; pf110_count={len(pf110)}; pf120_count={len(pf120)}",
            "why_failed": "EB는 density_net(밀도+순수익) 후보를 늘렸지만 validation/OOS PF(검증/표본외 PF)가 함께 1.10도 넘지 못했습니다.",
            "salvage_value": "no_h21(21시 제거), h2_m1p5 label(h2_m1.5 라벨), density>=3(밀도 3 이상)은 보존할 가치가 있습니다.",
            "reopen_condition": "dual PF floor(양쪽 PF 바닥) 후보가 PF>=1.15 또는 1.20에 접근해야 합니다.",
            "do_not_repeat": "PF만 올리려고 density(밀도)를 3/day 아래로 버리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "ec02_oos_pf_surrender_after_validation_floor",
            "observation": f"DZ OOS PF=1.2357 -> EB OOS PF={parent['selected_oos_profit_factor']}; EB validation PF={parent['selected_validation_profit_factor']}",
            "why_failed": "validation PF floor(검증 PF 바닥)를 올리는 과정에서 OOS PF(표본외 PF)가 약해졌습니다.",
            "salvage_value": "다음 ED는 validation/OOS min_pf(검증/표본외 최소 PF)를 직접 보상해야 합니다.",
            "reopen_condition": "min_pf(최소 PF)가 1.10 이상으로 올라오고 density>=3을 유지해야 합니다.",
            "do_not_repeat": "검증 PF만 좋아지는 저균형 후보를 package(패키지)로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "decision": "reject_runtime_package(런타임 패키지 거절)",
            "reason": "no_strict_candidate_and_dual_pf_floor_failed(엄격 후보 없음 및 양쪽 PF 바닥 실패)",
            "runtime_package": "not_opened",
            "new_mt5_execution": "not_run",
            "effect": "EC review(EC 검토)는 EB 단서를 보존하지만 runtime claim(런타임 주장)은 만들지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "ed01_dual_pf_floor_bridge_reseed",
            "hypothesis": "validation/OOS min_pf(검증/표본외 최소 PF)를 직접 보상하면 no_h21 h2 density_net(21시 제거 h2 밀도+순수익) 단서를 PF 1.15~1.20 경계로 끌어올릴 수 있습니다.",
            "seed_model": best_bridge.get("model_id", parent["selected_model_id"]),
            "seed_filter": best_bridge.get("stability_filter", parent["selected_stability_filter"]),
            "required_floor": "validation/OOS net>0 PF>=1.15 scout, PF>=1.20 strict, density>=3(검증/표본외 순수익 양수, PF 1.15 스카우트, PF 1.20 엄격, 밀도 3 이상)",
            "effect": "ED는 PF 한쪽 회복이 아니라 min_pf(최소 PF) 자체를 공격 탐색합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return summary, failure, package, queue


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(eb.FINAL_DECISION), rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY)], "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)", "runtime package(런타임 패키지)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selection_metric": "validation PF floor density recovery proxy(검증 PF 바닥 밀도 회복 프록시)", "secondary_metrics": ["min PF(최소 PF)", "density_net_count(밀도+순수익 후보 수)", "OOS PF(표본외 PF)"], "validation_judgment": "negative_review_boundary(부정 검토 경계)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "comparison_baseline": PARENT_RUN_ID, "likely_drivers": ["no_h21 density bridge(21시 제거 밀도 연결)", "validation PF weighting(검증 PF 가중)", "OOS PF surrender(표본외 PF 약화)"], "attribution_confidence": "medium_proxy_only(중간, 프록시 전용)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_proxy_review_boundary(프록시 검토 경계 안에서 연결됨)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EC review(EC 검토)는 package(패키지)와 authority(권위)를 열지 않습니다."})


def gate_rows(final: Mapping[str, Any], *, final_written: bool) -> list[dict[str, Any]]:
    receipt_paths = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "EB 입력과 EC 검토 입력 계보가 연결됐습니다."),
        ("eb_gate_inheritance_gate", all(read_csv(eb.GATE_AUDIT)["status"].astype(str) == "passed"), eb.GATE_AUDIT, "EB 게이트 통과 상태를 상속했습니다."),
        ("review_summary_gate", exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "EB 요약과 surface(표면) 집계를 기록했습니다."),
        ("package_rejection_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "runtime package(런타임 패키지) 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "dual PF floor(양쪽 PF 바닥) 실패 기억을 기록했습니다."),
        ("next_queue_gate", exists(RUN364ED_QUEUE), RUN364ED_QUEUE, "ED 다음 탐색 대기열을 만들었습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), RESULT_RECEIPT, "필수 receipt(영수증)가 있습니다."),
        ("required_gate_coverage_audit", final_written and exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", all(final.get(key, "not_claimed") == "not_claimed" for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]), CLAIM_RECEIPT, "authority/promotion/live/goal(권위/승격/실거래/목표) 주장을 차단했습니다."),
    ]
    return [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect} for gate, passed, evidence, effect in gates]


def final_payload(parent: Mapping[str, Any], summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_model_id": parent["selected_model_id"],
        "selected_label_id": parent["selected_label_id"],
        "selected_stability_filter": parent["selected_stability_filter"],
        "selected_validation_net": parent["selected_validation_net"],
        "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
        "selected_validation_trade_density": parent["selected_validation_trade_density"],
        "selected_oos_net": parent["selected_oos_net"],
        "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
        "selected_oos_trade_density": parent["selected_oos_trade_density"],
        "strict_candidate_count": parent["strict_candidate_count"],
        "density_both_count": summary["density_both_count"],
        "density_net_count": summary["density_net_count"],
        "pf110_count": summary["pf110_count"],
        "pf115_count": summary["pf115_count"],
        "pf120_count": summary["pf120_count"],
        "best_bridge_model_id": summary["best_bridge_model_id"],
        "best_bridge_min_pf": summary["best_bridge_min_pf"],
        "package_decision": "rejected",
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364EC H17 Validation PF Floor Review(검증 PF 바닥 검토)

Created(생성): {final['created_at_utc']}

## Decision(결정)

Action(행동): EB validation PF floor density recovery(EB 검증 PF 바닥 밀도 회복)를 package(패키지) 후보로 검토했습니다.

Effect(효과): density_net(밀도+순수익)은 늘었지만 dual PF floor(양쪽 PF 바닥)가 실패해 runtime package(런타임 패키지)는 열지 않습니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- density_net_count(밀도+순수익 후보 수): `{final['density_net_count']}`
- pf110_count(PF 1.10 양쪽 통과 수): `{final['pf110_count']}`
- pf120_count(PF 1.20 양쪽 통과 수): `{final['pf120_count']}`

## Next(다음)

`{NEXT_RUN_ID}`에서 validation/OOS min_pf(검증/표본외 최소 PF)를 직접 보상하는 dual PF floor bridge(양쪽 PF 바닥 연결) 탐색을 실행합니다.

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, f"""# Decision(결정): stage364EC validation PF floor review(검증 PF 바닥 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): EB 결과를 package(패키지)와 next seed(다음 씨앗) 관점에서 검토했습니다.

Effect(효과): dual PF floor failure(양쪽 PF 바닥 실패)를 ED 탐색 제약으로 전환합니다.
""", bom=True)
    append_text_once(REVIEW_INDEX, f"run364EC__{RUN_ID}", f"\n- run364EC__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - validation PF floor review(검증 PF 바닥 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EC__{RUN_ID}", f"\n<!-- run364EC__{RUN_ID} -->\n\n## run364EC Validation PF Floor Review(검증 PF 바닥 검토)\n\nAction(행동): EB proxy/ONNX smoke(EB 프록시/온엑스 스모크) 결과를 검토했습니다.\n\nEffect(효과): package(패키지)는 거절하고 ED dual PF floor bridge(양쪽 PF 바닥 연결) 탐색으로 넘깁니다.\n")
    append_text_once(STAGE_README, f"run364EC__{RUN_ID}", f"\n<!-- run364EC__{RUN_ID} -->\n## run364EC validation PF floor review(검증 PF 바닥 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364EC` reviewed(검토 완료) EB validation PF floor density recovery(EB 검증 PF 바닥 밀도 회복). EB는 density_net_count(밀도+순수익 후보 수)를 `{final['density_net_count']}`까지 늘렸지만 PF 1.10 양쪽 통과 수는 `{final['pf110_count']}`이고, 선택 validation/OOS PF(검증/표본외 PF)는 `{final['selected_validation_profit_factor']}` / `{final['selected_oos_profit_factor']}`라서 package(패키지)를 열지 않습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 dual PF floor bridge(양쪽 PF 바닥 연결)를 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): EC는 EB validation PF floor density recovery(EB 검증 PF 바닥 밀도 회복)를 review(검토)했고, dual PF floor failure(양쪽 PF 바닥 실패) 때문에 package rejected(패키지 거절)로 닫았습니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Next seed(다음 씨앗): dual PF floor bridge reseed(양쪽 PF 바닥 연결 재시드).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364EC__{RUN_ID}", f"\n<!-- run364EC__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed EB validation PF floor(검증 PF 바닥); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EC__{RUN_ID}", f"\n<!-- run364EC__{RUN_ID} -->\n- `{RUN_ID}`: density_net(밀도+순수익) 확대는 preserved clue(보존 단서)로 남기고, min_pf(최소 PF)를 ED에서 직접 탐색합니다. Effect(효과): PF 한쪽만 좋아지는 편향을 줄입니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EC__dual_pf_floor__{RUN_ID}", f"\n<!-- run364EC__dual_pf_floor__{RUN_ID} -->\n- `{RUN_ID}`: EB는 density_net_count(밀도+순수익 후보 수) `{final['density_net_count']}`를 만들었지만 pf110_count(PF 1.10 양쪽 통과 수)는 `{final['pf110_count']}`입니다. Effect(효과): ED는 min_pf(최소 PF)를 직접 보상합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Should EB open package or become ED dual PF seed?(EB를 패키지로 열 것인가, ED 양쪽 PF 씨앗으로 넘길 것인가?)", "next_action": NEXT_RUN_ID, "notes": f"density_net_count={final['density_net_count']};pf110_count={final['pf110_count']};pf120_count={final['pf120_count']}", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "EC validation PF floor review(EC 검증 PF 바닥 검토)", "metric_scope": "proxy_review_only(프록시 검토 전용)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "review_existing_proxy_no_mt5(기존 프록시 검토, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "run_family": "kpi_evidence(KPI 근거)", "run_type": "validation_pf_floor_review(검증 PF 바닥 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(PACKAGE_DECISION), "selected_net_profit": final["selected_oos_net"], "selected_profit_factor": final["selected_oos_profit_factor"], "selected_trade_density": final["selected_oos_trade_density"]}], extend_header=True)
    dz.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "EC validation PF floor review artifact(EC 검증 PF 바닥 검토 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    summary_rows, failure_rows, package_rows, queue_rows = review_tables(parent)
    write_csv(REVIEW_SUMMARY, summary_rows)
    write_csv(FAILURE_MEMORY, failure_rows)
    write_csv(PACKAGE_DECISION, package_rows)
    write_csv(RUN364ED_QUEUE, queue_rows)
    final = final_payload(parent, summary_rows[0], [], created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, final_written=False)
    write_csv(GATE_AUDIT, gates)
    gates = gate_rows(final, final_written=True)
    final = final_payload(parent, summary_rows[0], gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_receipts(final)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "package_decision": "rejected", "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
