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
from stage_pipelines.stage364 import train_h17_short_source_density_pf_bridge_reseed_without_db as dr  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dr.STAGE_ID
RUN_NUMBER = "run364DS"
RUN_ID = "run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1"
PARENT_RUN_ID = dr.RUN_ID
NEXT_RUN_ID = "run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1"

STATUS = "completed_stage364DS_density_pf_bridge_review_package_rejected_open_dt_no_authority"
JUDGMENT = "negative_density_pf_bridge_review_density_recovery_breaks_validation_no_package_no_authority"
DECISION = "stage364DS_reject_package_open_run364DT_regime_behavior_reseed"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_density_pf_bridge_rejected_no_runtime_package_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = dr.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "ds_density_pf_bridge_review_summary.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "density_pf_failure_memory.csv"
RUN364DT_QUEUE = RUN_DIR / "run364DT_regime_behavior_reseed_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DS_h17_short_source_density_pf_bridge_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DS_h17_short_source_density_pf_bridge_review.md"
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
    dr.FINAL_DECISION,
    dr.GATE_AUDIT,
    dr.BRIDGE_SURFACE,
    dr.SELECTED_CANDIDATE,
    dr.SPLIT_SUMMARY,
    dr.COMPONENT_AUDIT,
    dr.DATA_INTEGRITY_AUDIT,
    dr.PACKAGE_PRECHECK,
    dr.RUN364DS_QUEUE,
    dr.RUN_MANIFEST,
    dr.REPORT_PATH,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364DT_QUEUE,
    RESULT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return dr.rel(path)


def exists(path: Path | str) -> bool:
    return dr.exists(path)


def sha(path: Path | str) -> str:
    return dr.sha(path)


def read_json(path: Path) -> Any:
    return dr.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dr.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dr.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row.keys():
                if key not in fieldnames:
                    fieldnames.append(str(key))
        fieldnames = fieldnames or ["empty"]
    with open(str(io_path(path)), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dr.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dr.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dr.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dr.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing DS inputs(DS 입력 누락): " + ", ".join(missing))
    parent = read_json(dr.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DR next_run_id mismatch(DR 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DR forbidden claim(DR 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(dr.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DR gate audit(DR 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": ["obsidian-artifact-lineage(산출물 계보)", "obsidian-claim-discipline(주장 규율)"],
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(path) for path in INPUT_FILES if path != Path(__file__)],
            "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"],
            "judgment_label": JUDGMENT,
            "review_reason": "DR density/PF bridge(DR 밀도/PF 브리지)는 density_both_count(양쪽 밀도 통과 수)가 많지만 density_and_net_count(양쪽 밀도+순수익 통과 수)가 0입니다.",
            "next_condition": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "inherited_selected_variant": parent["selected_variant_id"],
        },
    )


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DS review input(DS 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]
    write_csv(INPUT_MANIFEST, rows)
    return rows


def review_rows(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_variant_id": parent["selected_variant_id"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "strict_candidate_count": parent["strict_candidate_count"],
            "density_both_count": parent["density_both_count"],
            "density_and_net_count": parent["density_and_net_count"],
            "density_net_pf_count": parent["density_net_pf_count"],
            "review_status": "package_rejected_open_dt(패키지 거절, DT 열기)",
            "effect": "밀도만 회복한 후보를 runtime package(런타임 패키지)로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    package = [
        {
            "run_id": RUN_ID,
            "decision": "do_not_open_runtime_package(런타임 패키지 열지 않음)",
            "reason": "strict_candidate_count=0 and density_and_net_count=0(엄격 후보 0개, 양쪽 밀도+순수익 통과 0개)",
            "selected_variant_id": parent["selected_variant_id"],
            "next_run_id": NEXT_RUN_ID,
            "effect": "proxy clue(프록시 단서)를 운영 package(패키지)로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "ds01_density_bridge_density_without_validation_net",
            "observation": f"density_both={parent['density_both_count']};density_and_net={parent['density_and_net_count']};selected validation/OOS density={parent['selected_validation_trade_density']}/{parent['selected_oos_trade_density']}",
            "why_failed": "density recovery destroys validation net/PF before cross-split contract(밀도 회복이 교차 분할 계약 전에 검증 순수익/PF를 무너뜨림)",
            "salvage_value": "selected low-density variant keeps OOS net/PF clue(선택 저밀도 변형은 표본외 순수익/PF 단서를 보존)",
            "reopen_condition": "new feature/label/regime idea changes validation trade quality before density search(새 피처/라벨/국면 아이디어가 밀도 탐색 전 검증 거래 품질을 바꿀 때)",
            "do_not_repeat": "do not keep widening DP score threshold/session bridge alone(DP 점수 임계값/세션 브리지만 계속 넓히지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "dt01_regime_behavior_reseed",
            "seed": "DR shows density bridge fails because validation quality collapses(DR은 밀도 브리지에서 검증 품질 붕괴를 보임)",
            "target_question": "Can regime/market-behavior labels and features create a denser source before threshold search?(국면/시장 현상 라벨과 피처가 임계값 탐색 전에 더 조밀한 원천을 만들 수 있는가?)",
            "must_keep": "train/validation/OOS split(학습/검증/표본외 분할), no trade splitting(거래 쪼개기 금지), no package before review(검토 전 패키지 금지)",
            "avoid": "risk multiplier only(위험 배수만), DP score bridge widening only(DP 점수 브리지 확대만), OOS-only package(OOS 전용 패키지)",
            "candidate_ideas": "regime-conditioned labels(국면 조건 라벨), volatility/impulse source features(변동성/충격 원천 피처), session re-entry shape(세션 재진입 형태), long/short asymmetric source balance(롱/숏 비대칭 원천 균형)",
            "effect": "같은 density blocker(밀도 차단 원인)를 반복하지 않고 새 수익 원천 탐색으로 전환합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(REVIEW_SUMMARY, summary)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364DT_QUEUE, queue)
    return summary, package, failure, queue


def final_payload(parent: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_variant_id": parent["selected_variant_id"],
        "selected_validation_net": parent["selected_validation_net"],
        "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
        "selected_validation_trade_density": parent["selected_validation_trade_density"],
        "selected_oos_net": parent["selected_oos_net"],
        "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
        "selected_oos_trade_density": parent["selected_oos_trade_density"],
        "strict_candidate_count": parent["strict_candidate_count"],
        "density_both_count": parent["density_both_count"],
        "density_and_net_count": parent["density_and_net_count"],
        "density_net_pf_count": parent["density_net_pf_count"],
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


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_RECEIPT,
        {
            **base,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(dr.BRIDGE_SURFACE)],
            "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "밀도는 열렸지만 검증 품질이 무너져 패키지로 올릴 수 없습니다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_review_no_package(검토 연결, 패키지 없음)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "negative review(부정 검토)를 운영 주장으로 바꾸지 않습니다.",
        },
    )


def gate_rows(final: Mapping[str, Any], *, final_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "DR 입력 계보를 연결했습니다."),
        ("parent_gate_inheritance_gate", exists(dr.GATE_AUDIT), dr.GATE_AUDIT, "DR 게이트 통과 상태를 상속했습니다."),
        ("review_summary_gate", exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "DS 검토 요약을 작성했습니다."),
        ("package_rejection_gate", exists(PACKAGE_DECISION) and int(final["strict_candidate_count"]) == 0, PACKAGE_DECISION, "패키지를 열지 않는 결정을 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "밀도/PF 실패 기억을 기록했습니다."),
        ("next_queue_gate", exists(RUN364DT_QUEUE), RUN364DT_QUEUE, "DT 공격 탐색 대기열을 기록했습니다."),
        ("receipt_coverage_gate", exists(RESULT_RECEIPT) and exists(LINEAGE_RECEIPT) and exists(CLAIM_RECEIPT), RESULT_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DS H17 Short-Source Density/PF Bridge Review(숏 원천 밀도/PF 브리지 검토)

Created(생성): {final['created_at_utc']}

## Review(검토)

Action(행동): DR density/PF bridge(DR 밀도/PF 브리지)의 package(패키지) 가능성을 검토했습니다.

Effect(효과): density_both_count(양쪽 밀도 통과 수) `{final['density_both_count']}`에도 density_and_net_count(양쪽 밀도+순수익 통과 수)가 `{final['density_and_net_count']}`라 runtime package(런타임 패키지)를 열지 않습니다.

## Decision(결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`{NEXT_RUN_ID}`에서 regime/market-behavior reseed(국면/시장 현상 재시드)를 엽니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    decision_doc = f"""# Decision(결정): stage364DS density/PF bridge review(밀도/PF 브리지 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): DR bridge(DR 브리지)를 package(패키지) 후보로 검토했습니다.

Effect(효과): 검증/표본외 동시 순수익 통과가 0개라 package(패키지)는 거절하고 새 regime/behavior seed(국면/현상 씨앗)로 이동합니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364DS__{RUN_ID}", f"\n- run364DS__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density/PF bridge review(밀도/PF 브리지 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DS__{RUN_ID}", f"\n<!-- run364DS__{RUN_ID} -->\n\n## run364DS Density/PF Bridge Review(밀도/PF 브리지 검토)\n\nAction(행동): DR bridge(DR 브리지)를 검토하고 package(패키지)를 거절했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 regime/market-behavior reseed(국면/시장 현상 재시드)를 엽니다.\n")
    append_text_once(STAGE_README, f"run364DS__{RUN_ID}", f"\n<!-- run364DS__{RUN_ID} -->\n## run364DS review(검토)\n\nDR bridge(DR 브리지)는 package rejected(패키지 거절)입니다. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364DS` reviewed(검토 완료) DR density/PF bridge(DR 밀도/PF 브리지) and rejected runtime package(런타임 패키지 거절). density_both_count(양쪽 밀도 통과 수)는 `{final['density_both_count']}`였지만 density_and_net_count(양쪽 밀도+순수익 통과 수)는 `{final['density_and_net_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 regime/market-behavior label/feature seed(국면/시장 현상 라벨/피처 씨앗)를 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): DR density/PF bridge(DR 밀도/PF 브리지)는 package rejected(패키지 거절)입니다. density_both_count(양쪽 밀도 통과 수)는 `{final['density_both_count']}`지만 density_and_net_count(양쪽 밀도+순수익 통과 수)는 `{final['density_and_net_count']}`입니다.

Next seed(다음 씨앗): regime/market-behavior reseed(국면/시장 현상 재시드).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DS__{RUN_ID}", f"\n<!-- run364DS__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DR density/PF bridge(밀도/PF 브리지 검토); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DS__{RUN_ID}", f"\n<!-- run364DS__{RUN_ID} -->\n- `{RUN_ID}`: density bridge(밀도 브리지)는 검증 품질을 보존하지 못했습니다. Effect(효과): 다음 탐색은 threshold/session widening(임계값/세션 확대)이 아니라 regime/market-behavior source seed(국면/시장 현상 원천 씨앗)로 전환합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DS__density_bridge_failed__{RUN_ID}", f"\n<!-- run364DS__density_bridge_failed__{RUN_ID} -->\n- `{RUN_ID}`: DR density/PF bridge(DR 밀도/PF 브리지)는 package rejected(패키지 거절)입니다. density_both_count(양쪽 밀도 통과 수) `{final['density_both_count']}` 중 density_and_net_count(양쪽 밀도+순수익 통과 수)는 `{final['density_and_net_count']}`입니다. Effect(효과): DP score bridge(DP 점수 브리지)만 넓히는 반복을 멈춥니다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    gates = read_csv(GATE_AUDIT)
    gate_passes = int((gates["status"].astype(str) == "passed").sum())
    gate_total = int(len(gates))
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Should DR bridge open package work or close as failure memory?(DR 브리지를 패키지로 열지 실패 기억으로 닫을지?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"density_both={final['density_both_count']};density_and_net={final['density_and_net_count']};package=not_opened",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
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
                "kpi_scope": "DS bridge review(DS 브리지 검토)",
                "metric_scope": "proxy_review_no_package(프록시 검토, 패키지 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "source_authority": "proxy_review_no_mt5_no_package(프록시 검토, MT5/패키지 없음)",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "run_family": "kpi_evidence(KPI 근거)",
                "run_type": "proxy_review(프록시 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(REVIEW_SUMMARY),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
        extend_header=True,
    )
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv"),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "DS density/PF bridge review artifact(DS 밀도/PF 브리지 검토 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


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
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_work_packet(parent)
    input_manifest_rows()
    review_rows(parent)
    final = final_payload(parent, now_utc())
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, final_written=exists(FINAL_DECISION))
    write_json(FINAL_DECISION, {**final, "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates)})
    final = read_json(FINAL_DECISION)
    write_docs(final, gates)
    write_ledgers(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
