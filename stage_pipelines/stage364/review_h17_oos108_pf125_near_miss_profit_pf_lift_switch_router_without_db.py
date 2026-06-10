from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db as hf  # noqa: E402


TODAY = "2026-06-08"
STAGE_ID = hf.STAGE_ID
STAGE_DIR = hf.STAGE_DIR
REVIEW_DIR = hf.REVIEW_DIR
SPEC_DIR = hf.SPEC_DIR
SELECTED_DIR = hf.SELECTED_DIR

RUN_NUMBER = "run364HG"
RUN_ID = "run364HG_review_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1"
PARENT_RUN_ID = hf.RUN_ID
NEXT_RUN_ID = "run364HH_materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db_v1"

STATUS = "completed_stage364HG_hf_strict_proxy_review_runtime_capability_gap_materialization_required_no_authority"
JUDGMENT = "positive_proxy_no_package_hf_strict_pass_runtime_capability_gap_no_authority"
DECISION = "stage364HG_open_run364HH_materialize_near_miss_profit_pf_lift_runtime_capability_inputs"
CLAIM_BOUNDARY = (
    "review_only_hf_strict_proxy_runtime_capability_gap_no_runtime_package_no_new_mt5_execution_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "hg_review_summary.csv"
VETO_ATTRIBUTION = RUN_DIR / "hg_veto_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "hg_package_decision.csv"
RUNTIME_CAPABILITY_GAP = RUN_DIR / "hg_runtime_capability_gap.csv"
RUN364HH_QUEUE = RUN_DIR / "hg_hh_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HG_near_miss_profit_pf_lift_switch_router_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HG_near_miss_profit_pf_lift_switch_router_review.md"
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

THIS_FILE = Path(__file__)

INPUT_FILES = [
    hf.FINAL_DECISION,
    hf.GATE_AUDIT,
    hf.TRADE_SURFACE,
    hf.SELECTED_CANDIDATE,
    hf.SELECTED_TRADE_TAPE,
    hf.SELECTED_VETO_GROUPS,
    hf.MODEL_ARTIFACT_MANIFEST,
    hf.ONNX_SMOKE_REPORT,
    hf.DATA_INTEGRITY_AUDIT,
    hf.RUN364HG_QUEUE,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    VETO_ATTRIBUTION,
    PACKAGE_DECISION,
    RUNTIME_CAPABILITY_GAP,
    RUN364HH_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    THIS_FILE,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return hf.rel(path)


def exists(path: Path | str) -> bool:
    return hf.exists(path)


def sha(path: Path | str) -> str:
    return hf.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return hf.as_float(value, default)


def read_json(path: Path) -> dict[str, Any]:
    return hf.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    hf.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    hf.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    hf.write_csv(path, rows)


def append_text_once(path: Path, marker: str, text: str) -> None:
    hf.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    hf.append_or_replace_csv(path, key_fields, rows)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HG inputs(HG 입력 누락): " + ", ".join(missing))
    parent = read_json(hf.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HF next_run_id mismatch(HF 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    gates = pd.read_csv(io_path(hf.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HF gate audit(HF 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden HF claim(금지된 HF 주장): {key}={parent.get(key)}")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "HG review input(HG 검토 입력)",
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
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "review_question": "Should HF strict proxy open a runtime package now?(HF 엄격 프록시를 지금 런타임 패키지로 열어야 하는가?)",
            "parent_summary": {
                "run_id": parent.get("run_id"),
                "judgment": parent.get("judgment"),
                "selected_oos_net": parent.get("selected_oos_net"),
                "selected_oos_profit_factor": parent.get("selected_oos_profit_factor"),
                "strict_candidate_count": parent.get("strict_candidate_count"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def review_summary_rows(parent: Mapping[str, Any], surface: pd.DataFrame) -> list[dict[str, Any]]:
    strict_rows = int(surface["hf_strict_switch_pass"].astype(str).str.startswith("passed").sum())
    return [
        {
            "run_id": RUN_ID,
            "review_item": "hf_strict_proxy_result(HF 엄격 프록시 결과)",
            "observed": f"strict_rows={strict_rows};selected_oos_net={parent['selected_oos_net']};selected_oos_pf={parent['selected_oos_profit_factor']};selected_oos_density={parent['selected_oos_trade_density']};selected_combined_density={parent['selected_combined_trade_density']}",
            "judgment": "positive_proxy(긍정 프록시)",
            "effect": "수익/PF 목표는 넘었지만 아직 runtime evidence(런타임 근거)는 없습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_item": "density_and_cost_boundary(밀도와 비용 경계)",
            "observed": f"combined_cost09={parent['selected_combined_cost09_net']};delta_combined_density_vs_hd={parent['delta_combined_density_vs_hd']}",
            "judgment": "preserved_but_tight(보존했지만 빡빡함)",
            "effect": "combined density(합산 밀도)는 1.30 바닥 바로 위라 MT5에서 미끄러지면 깨질 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def veto_attribution_rows(veto_groups: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw in veto_groups.to_dict("records"):
        rows.append(
            {
                "run_id": RUN_ID,
                "veto_policy_label": raw.get("veto_policy_label", ""),
                "veto_key_values": raw.get("veto_key_values", ""),
                "validation_count": raw.get("validation_count", ""),
                "validation_net": raw.get("validation_net", ""),
                "removed_total_count": raw.get("removed_total_count", ""),
                "removed_oos_count": raw.get("removed_oos_count", ""),
                "removed_oos_net": raw.get("removed_oos_net", ""),
                "judgment": "validation_loss_bucket_removed(검증 손실 구간 제거)",
                "effect": "차단은 OOS(표본외) 손실을 직접 찾은 것이 아니라 validation(검증) 손실 구간에서 유래했습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(VETO_ATTRIBUTION, rows)
    return rows


def package_decision_rows(parent: Mapping[str, Any]) -> list[dict[str, Any]]:
    strict_proxy = int(parent["strict_candidate_count"]) > 0
    onnx_smoke = int(parent["source_onnx_smoke_pass_rows"]) >= 2
    runtime_capability_supported = False
    package_eligible = strict_proxy and onnx_smoke and runtime_capability_supported
    rows = [
        {
            "run_id": RUN_ID,
            "decision_item": "strict_proxy_gate(엄격 프록시 게이트)",
            "status": "passed" if strict_proxy else "failed",
            "observed": f"strict_candidate_count={parent['strict_candidate_count']}",
            "effect": "프록시 후보 자체는 계속 검토할 가치가 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "decision_item": "source_onnx_smoke_gate(원천 ONNX 스모크 게이트)",
            "status": "passed" if onnx_smoke else "failed",
            "observed": f"source_onnx_smoke_pass_rows={parent['source_onnx_smoke_pass_rows']}",
            "effect": "GZ/HB 원천 모델은 ONNX(온엑스) 계보가 연결됩니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "decision_item": "runtime_capability_gate(런타임 기능 게이트)",
            "status": "failed",
            "observed": "current EA supports primary/fallback models but not generic probability-bin veto(open_hour+pflat_bin+sl_gap_bin)(현재 EA는 우선/대체 모델은 지원하지만 일반 확률 구간 차단은 미지원)",
            "effect": "바로 패키지하지 않고 런타임 표현 계약을 먼저 구체화합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "decision_item": "package_eligible(패키지 적격)",
            "status": "passed" if package_eligible else "failed",
            "observed": f"package_eligible={package_eligible}",
            "effect": "현 상태에서는 package(패키지)를 열지 않고 HH materialization(HH 구체화)로 넘깁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(PACKAGE_DECISION, rows)
    return rows


def capability_gap_rows(parent: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "capability": "dual_source_onnx_route(이중 원천 ONNX 라우트)",
            "current_status": "partially_supported_by_primary_fallback_inputs(우선/대체 입력으로 부분 지원)",
            "required_for_hf": parent["selected_source_models"],
            "effect": "GZ/HB 두 모델을 함께 불러야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "probability_bin_veto(확률 구간 차단)",
            "current_status": "missing_required(필수 누락)",
            "required_for_hf": parent["selected_veto_key_fields"],
            "effect": "open_hour/p_flat/short_long_gap(진입 시간/평탄 확률/숏롱 차이) 구간 차단을 EA가 재현해야 MT5 probe(MT5 탐침)가 의미 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "expected_tape_handoff(예상 테이프 인계)",
            "current_status": "available_from_hf_selected_tape(HF 선택 테이프에서 가능)",
            "required_for_hf": rel(hf.SELECTED_TRADE_TAPE),
            "effect": "MT5 결과와 proxy(프록시)를 비교할 기준을 만들 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(RUNTIME_CAPABILITY_GAP, rows)
    return rows


def queue_rows(parent: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "hh01_materialize_runtime_capability_inputs(런타임 기능 입력 구체화)",
            "source_candidate": parent["selected_route_variant_id"],
            "required_artifacts": "runtime_capability_contract;expected_tape;primary/fallback model manifest;veto_rule_manifest(런타임 기능 계약;예상 테이프;우선/대체 모델 목록;차단 규칙 목록)",
            "do_next": "materialize package inputs before MT5 execution(MT5 실행 전 패키지 입력 구체화)",
            "avoid": "do not claim runtime readiness from proxy pass(프록시 통과만으로 런타임 준비 주장 금지)",
            "effect": "다음 회차에서 EA 수정이 필요한지, 기존 fallback 기능으로 충분한지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364HH_QUEUE, rows)
    return rows


def selected_final(parent: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "package_eligible": False,
        "positive_clue": True,
        "runtime_capability_gap": True,
        "selected_route_variant_id": parent["selected_route_variant_id"],
        "selected_veto_policy_label": parent["selected_veto_policy_label"],
        "selected_oos_net": parent["selected_oos_net"],
        "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
        "selected_oos_trade_density": parent["selected_oos_trade_density"],
        "selected_oos_cost06_net": parent["selected_oos_cost06_net"],
        "selected_combined_trade_density": parent["selected_combined_trade_density"],
        "selected_combined_cost09_net": parent["selected_combined_cost09_net"],
        "strict_candidate_count": parent["strict_candidate_count"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_rows(final: Mapping[str, Any], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION) and exists(RUN364HH_QUEUE), REVIEW_SUMMARY, "HG review summary/package/queue(HG 검토 요약/패키지/대기열)를 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "HF 입력 계보를 기록했습니다."),
        ("kpi_review_gate", exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "HF KPI(핵심 성과 지표)를 검토했습니다."),
        ("veto_attribution_gate", exists(VETO_ATTRIBUTION), VETO_ATTRIBUTION, "차단 그룹 귀속을 기록했습니다."),
        ("package_boundary_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "패키지 미개방 경계를 기록했습니다."),
        ("runtime_capability_gap_gate", exists(RUNTIME_CAPABILITY_GAP), RUNTIME_CAPABILITY_GAP, "런타임 기능 누락을 기록했습니다."),
        ("next_action_gate", exists(RUN364HH_QUEUE), RUN364HH_QUEUE, "HH 다음 행동을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 receipt(영수증)를 작성했습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트 감사가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "운영 권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "review_summary": rel(REVIEW_SUMMARY), "package_decision": rel(PACKAGE_DECISION), "runtime_capability_gap": rel(RUNTIME_CAPABILITY_GAP), "measurement_boundary": "review of Python proxy only(Python 프록시 검토 전용)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "source_veto": rel(VETO_ATTRIBUTION), "observed": f"OOS net/PF(표본외 순수익/PF) {final['selected_oos_net']}/{final['selected_oos_profit_factor']}", "effect": "veto rule(차단 규칙)이 수익/PF 리프트의 주요 귀속입니다."})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(RUNTIME_CAPABILITY_GAP), rel(RUN364HH_QUEUE)], "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "runtime capability implementation evidence(런타임 기능 구현 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_review_boundary(검토 경계로 연결됨)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364HG Near-Miss Profit/PF Lift Review(근접 실패 수익/PF 리프트 검토)

Created(생성): {final['created_at_utc']}

Action(행동): HF strict proxy(HF 엄격 프록시)를 KPI(핵심 성과 지표), veto attribution(차단 귀속), package boundary(패키지 경계), runtime capability gap(런타임 기능 누락)으로 검토했습니다.

Effect(효과): 수익/PF 개선 단서는 보존하지만, 현재 EA(전문가 자문)가 probability-bin veto(확률 구간 차단)를 그대로 표현하지 못하므로 package(패키지)는 열지 않습니다.

- judgment(판정): `{final['judgment']}`
- package_eligible(패키지 적격): `{final['package_eligible']}`
- runtime_capability_gap(런타임 기능 누락): `{final['runtime_capability_gap']}`
- selected_route_variant_id(선택 라우트 변형 ID): `{final['selected_route_variant_id']}`
- selected_veto_policy(선택 차단 정책): `{final['selected_veto_policy_label']}`
- OOS net/PF/density/cost0.6(표본외 순수익/PF/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
- combined density/cost0.9(합산 밀도/비용0.9): `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364HG Near-Miss Profit/PF Lift Review(근접 실패 수익/PF 리프트 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): HF는 package(패키지)로 바로 열지 않고 HH runtime capability materialization(HH 런타임 기능 구체화)로 넘깁니다.

Effect(효과): MT5(메타트레이더5) 실행 전, 두 ONNX(온엑스) 원천 모델과 probability-bin veto(확률 구간 차단)가 EA(전문가 자문)에서 재현 가능한지 먼저 닫습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364HG__{RUN_ID}", f"\n- run364HG__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - near-miss profit/PF lift review(근접 실패 수익/PF 리프트 검토), next(다음) `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HG__{RUN_ID}", f"\n<!-- run364HG__{RUN_ID} -->\n\n## run364HG Near-Miss Profit/PF Lift Review(근접 실패 수익/PF 리프트 검토)\n\nAction(행동): HF strict proxy(HF 엄격 프록시)를 검토하고 package(패키지)는 열지 않았습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 runtime capability inputs(런타임 기능 입력)를 구체화합니다.\n")
    append_text_once(STAGE_README, f"run364HG__{RUN_ID}", f"\n<!-- run364HG__{RUN_ID} -->\n## run364HG near-miss profit/PF lift review(근접 실패 수익/PF 리프트 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
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

Current truth(현재 진실): `run364HG` reviewed(검토 완료) HF strict proxy(HF 엄격 프록시). HF의 OOS net/PF/density/cost0.6(표본외 순수익/PF/밀도/비용0.6)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`입니다.

Package truth(패키지 진실): package(패키지)는 not opened(열지 않음)입니다. 이유는 현재 EA(전문가 자문)가 HF의 probability-bin veto(확률 구간 차단)를 그대로 표현한다는 근거가 없기 때문입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 runtime capability contract(런타임 기능 계약), expected tape(예상 테이프), primary/fallback model manifest(우선/대체 모델 목록), veto rule manifest(차단 규칙 목록)을 구체화합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): HG marked(표시) HF as positive proxy no package(긍정 프록시, 패키지 없음).

HF OOS net/PF/density/cost0.6(HF 표본외 순수익/PF/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`

Next seed(다음 씨앗): HH runtime capability materialization(HH 런타임 기능 구체화).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364HG__{RUN_ID}", f"\n<!-- run364HG__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed HF strict proxy(HF 엄격 프록시); package(패키지) not opened(열지 않음); next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HG__{RUN_ID}", f"\n<!-- run364HG__{RUN_ID} -->\n- `{RUN_ID}`: HF strict proxy(HF 엄격 프록시)는 긍정 단서지만 probability-bin veto(확률 구간 차단) 런타임 표현 누락 때문에 package(패키지)를 열지 않았습니다. Effect(효과): HH가 런타임 기능 계약을 구체화합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    artifact_count = len([path for path in OUTPUT_FILES if exists(path)])
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": artifact_count,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Should HF strict proxy open package now?(HF 엄격 프록시를 지금 패키지로 열어야 하는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"package_eligible={final['package_eligible']};runtime_capability_gap={final['runtime_capability_gap']};oos_net={final['selected_oos_net']};oos_pf={final['selected_oos_profit_factor']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "view": record_view,
                "tier": tier_scope,
                "kpi_scope": "HG review(HG 검토)",
                "metric_scope": "review_no_mt5(검토, MT5 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "source_authority": "review_no_mt5(검토, MT5 없음)",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "run_family": "kpi_evidence(KPI 근거)",
                "run_type": "near_miss_profit_pf_lift_review(근접 실패 수익/PF 리프트 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(REVIEW_SUMMARY),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
    )
    try:
        hf.hb.et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "HG near-miss profit/PF lift review artifact(HG 근접 실패 수익/PF 리프트 검토 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "command": f"python {rel(THIS_FILE)}",
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    surface = pd.read_csv(io_path(hf.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    veto_groups = pd.read_csv(io_path(hf.SELECTED_VETO_GROUPS), encoding="utf-8-sig").fillna("")
    write_csv(REVIEW_SUMMARY, review_summary_rows(parent, surface))
    veto_attribution_rows(veto_groups)
    package_decision_rows(parent)
    capability_gap_rows(parent)
    queue_rows(parent)
    created_at = now_utc()
    draft = {
        "run_id": RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    gates = gate_rows(draft, final_written=False)
    final = selected_final(parent, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, final_written=True)
    final = selected_final(parent, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "package_eligible": final["package_eligible"], "runtime_capability_gap": final["runtime_capability_gap"], "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
