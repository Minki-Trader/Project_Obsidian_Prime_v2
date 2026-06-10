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
from stage_pipelines.stage364 import train_h17_short_source_pf_balance_polish_scout_without_db as dn  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dn.STAGE_ID
RUN_NUMBER = "run364DO"
RUN_ID = "run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1"
PARENT_RUN_ID = dn.RUN_ID
NEXT_RUN_ID = "run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1"

STATUS = "completed_stage364DO_h17_short_source_pf_balance_review_parameter_only_pf_fail_no_package_no_authority"
JUDGMENT = "inconclusive_parameter_only_pf_balance_polish_net_lift_without_pf_pass_no_package_no_authority"
DECISION = "stage364DO_open_run364DP_short_source_model_label_offensive_reseed"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_parameter_polish_failed_strict_pf_contract_"
    "no_new_model_training_no_new_mt5_execution_no_runtime_package_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = dn.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "do_pf_balance_review_summary.csv"
FAILURE_MEMORY = RUN_DIR / "parameter_only_failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364DP_QUEUE = RUN_DIR / "run364DP_model_label_offensive_reseed_queue.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DO_h17_short_source_pf_balance_polish_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DO_h17_short_source_pf_balance_polish_review.md"
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
    dn.FINAL_DECISION,
    dn.GATE_AUDIT,
    dn.PF_BALANCE_SURFACE,
    dn.SELECTED_CANDIDATE,
    dn.PACKAGE_PRECHECK,
    dn.DATA_INTEGRITY_AUDIT,
    dn.PROXY_MT5_CALIBRATION,
    dn.RUN364DO_QUEUE,
    dn.JUDGMENT_RECEIPT,
    dn.ATTRIBUTION_RECEIPT,
    dn.LINEAGE_RECEIPT,
    dn.CLAIM_RECEIPT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_MEMORY,
    PACKAGE_DECISION,
    RUN364DP_QUEUE,
    RESULT_JUDGMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
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
    return dn.rel(path)


def exists(path: Path | str) -> bool:
    return dn.exists(path)


def sha(path: Path | str) -> str:
    return dn.sha(path)


def json_ready(value: Any) -> Any:
    return dn.json_ready(value)


def read_json(path: Path) -> Any:
    return dn.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dn.write_json(path, payload)


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
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dn.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dn.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dn.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dn.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dn.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DO inputs(DO 입력 누락): " + ", ".join(missing))
    dn_final = read_json(dn.FINAL_DECISION)
    if dn_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DN next_run_id mismatch(DN 다음 실행 ID 불일치): {dn_final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if dn_final.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DN forbidden claim(DN 금지 주장): {key}={dn_final.get(key)}")
    gates = read_csv(dn.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DN gate audit(DN 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return dn_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DN review input(DN 검토 입력)",
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
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "DN parameter-only polish may have produced a runtime package candidate(DN 파라미터 전용 다듬기가 런타임 패키지 후보를 만들었을 수 있음).",
            "decision_use": "Open package only if strict calibrated DB net/PF exceedance holds(엄격 보정 DB 순수익/PF 초과가 맞을 때만 패키지를 엽니다).",
            "claim_boundary": CLAIM_BOUNDARY,
            "required_gates": [
                "input_lineage_gate",
                "dn_gate_inheritance_gate",
                "strict_precheck_review_gate",
                "package_decision_gate",
                "next_queue_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
    )


def best_rows(surface: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    selected = read_json(dn.SELECTED_CANDIDATE)
    net_rows = [row for row in surface if str(row.get("net_pass_pf_fail_status", "")).startswith("net_pass")]
    short_ready_rows = [row for row in surface if as_float(row.get("estimated_mt5_short_trade_count")) >= dn.SHORT_COUNT_FLOOR]
    best_net = max(surface, key=lambda row: as_float(row.get("runtime_calibrated_net_profit")))
    best_pf = max(short_ready_rows or surface, key=lambda row: as_float(row.get("runtime_calibrated_profit_factor")))
    return selected, best_net, best_pf


def build_reviews(dn_final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = read_csv(dn.PF_BALANCE_SURFACE).to_dict("records")
    selected, best_net, best_pf = best_rows(surface)
    strict_pass_count = int(float(dn_final.get("calibrated_pass_count", 0) or 0))
    net_pass_pf_fail_count = int(float(dn_final.get("net_pass_pf_fail_count", 0) or 0))

    summary = [
        {
            "run_id": RUN_ID,
            "selected_variant_id": selected.get("variant_id", ""),
            "selected_calibrated_net": selected.get("runtime_calibrated_net_profit", ""),
            "selected_calibrated_pf": selected.get("runtime_calibrated_profit_factor", ""),
            "selected_net_delta_vs_db": selected.get("calibrated_net_delta_vs_db", ""),
            "selected_pf_delta_vs_db": selected.get("calibrated_pf_delta_vs_db", ""),
            "selected_short_count": selected.get("estimated_mt5_short_trade_count", ""),
            "selected_precheck": selected.get("calibrated_precheck_status", ""),
            "best_net_variant_id": best_net.get("variant_id", ""),
            "best_net_calibrated_net": best_net.get("runtime_calibrated_net_profit", ""),
            "best_net_calibrated_pf": best_net.get("runtime_calibrated_profit_factor", ""),
            "best_pf_variant_id": best_pf.get("variant_id", ""),
            "best_pf_calibrated_net": best_pf.get("runtime_calibrated_net_profit", ""),
            "best_pf_calibrated_pf": best_pf.get("runtime_calibrated_profit_factor", ""),
            "strict_pass_count": strict_pass_count,
            "net_pass_pf_fail_count": net_pass_pf_fail_count,
            "review_status": "failed_strict_package_contract(엄격 패키지 계약 실패)",
            "effect": "순수익 상승 후보와 PF 통과 후보를 분리해 net-only pass(순수익만 통과)를 runtime package(런타임 패키지)로 넘기지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "do01_parameter_only_risk_scale_net_lift_pf_fail",
            "observation": f"{best_net.get('variant_id', '')} lifted calibrated net to {best_net.get('runtime_calibrated_net_profit', '')} but PF stayed {best_net.get('runtime_calibrated_profit_factor', '')}.",
            "korean_read": "위험 배수 강화는 보정 순수익을 DB 위로 올렸지만 PF는 DB 1.41 아래에 남았습니다.",
            "constraint_for_next": "DP는 단순 risk-scale multiplier(위험 배수) 추가를 중심 전략으로 쓰지 않습니다.",
            "effect": "다음 탐색이 같은 순수익만 통과 문제를 반복하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "do02_quality_filter_pf_not_enough",
            "observation": f"{best_pf.get('variant_id', '')} was best PF among short-ready rows with calibrated PF {best_pf.get('runtime_calibrated_profit_factor', '')}.",
            "korean_read": "품질 필터는 PF를 조금 올렸지만 DB PF 1.41을 넘기에는 부족했습니다.",
            "constraint_for_next": "DP는 feature(피처), label(라벨), model family(모델 계열) 쪽 offensive reseed(공격 재시드)를 우선합니다.",
            "effect": "파라미터만 더 좁히는 탐색에 갇히지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "decision": "do_not_open_runtime_package(런타임 패키지 열지 않음)",
            "reason": "strict calibrated precheck count is zero(엄격 보정 사전검사 통과 수 0).",
            "selected_variant_id": selected.get("variant_id", ""),
            "selected_net_pass_pf_fail_status": selected.get("net_pass_pf_fail_status", ""),
            "required_for_package": "runtime-calibrated net > DB 1018.78 and PF > DB 1.41 with shorts >= 125(런타임 보정 순수익/PF DB 초과와 숏 125 이상)",
            "next_run_id": NEXT_RUN_ID,
            "effect": "MT5 package(MT5 패키지) 제작 시간을 PF 미달 후보에 쓰지 않고 새 수익 원천 탐색으로 돌립니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "dp01_model_label_feature_offensive_reseed",
            "seed": "parameter-only polish can lift net but cannot clear PF(파라미터 전용 다듬기는 순수익을 올리지만 PF를 넘기지 못함)",
            "target_question": "Can a new short-source feature/label/model seed lift PF above DB while keeping density and short count?(새 숏 원천 피처/라벨/모델 씨앗이 밀도와 숏 거래수를 유지하면서 PF를 DB 위로 올릴 수 있는가?)",
            "must_keep": "trade density 3-10+(거래 밀도 3-10 이상), short_count >=125(숏 거래수 125 이상), no trade splitting(거래 쪼개기 금지), timestamp safety(시점 안전)",
            "avoid": "risk multiplier only(위험 배수만), density without PF lift(PF 상승 없는 밀도 추가), runtime authority claim(런타임 권위 주장)",
            "candidate_ideas": "short-source regime interaction(숏 원천 국면 상호작용), cost-aware short label(비용 인식 숏 라벨), asymmetric classifier threshold(비대칭 분류 임계값), session volatility quality(세션 변동성 품질)",
            "effect": "DP는 같은 파라미터 표면을 반복하지 않고 새 수익 구조를 공격적으로 엽니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(REVIEW_SUMMARY, summary)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(PACKAGE_DECISION, package)
    write_csv(RUN364DP_QUEUE, queue)
    return summary, failure, package, queue


def final_payload(dn_final: Mapping[str, Any], summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_variant_id": summary["selected_variant_id"],
        "selected_calibrated_net": summary["selected_calibrated_net"],
        "selected_calibrated_pf": summary["selected_calibrated_pf"],
        "selected_net_delta_vs_db": summary["selected_net_delta_vs_db"],
        "selected_pf_delta_vs_db": summary["selected_pf_delta_vs_db"],
        "selected_short_count": summary["selected_short_count"],
        "strict_pass_count": summary["strict_pass_count"],
        "net_pass_pf_fail_count": summary["net_pass_pf_fail_count"],
        "best_net_variant_id": summary["best_net_variant_id"],
        "best_net_calibrated_net": summary["best_net_calibrated_net"],
        "best_net_calibrated_pf": summary["best_net_calibrated_pf"],
        "best_pf_variant_id": summary["best_pf_variant_id"],
        "best_pf_calibrated_net": summary["best_pf_calibrated_net"],
        "best_pf_calibrated_pf": summary["best_pf_calibrated_pf"],
        "dn_gate_passes": dn_final.get("gate_passes", ""),
        "dn_gate_total": dn_final.get("gate_total", ""),
        "runtime_package": "not_opened",
        "new_model_training": "not_run",
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
    dn_gates = read_csv(dn.GATE_AUDIT)
    strict_count = int(float(read_json(dn.FINAL_DECISION).get("calibrated_pass_count", 0) or 0))
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "DN 입력이 모두 연결됐습니다."),
        ("dn_gate_inheritance_gate", not dn_gates.empty and all(dn_gates["status"].astype(str) == "passed"), dn.GATE_AUDIT, "DN 게이트 통과 상태를 상속했습니다."),
        ("strict_precheck_review_gate", strict_count == 0 and exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "엄격 통과 0개를 패키지 실패로 판정했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "런타임 패키지를 열지 않는 결정을 기록했습니다."),
        ("next_queue_gate", exists(RUN364DP_QUEUE), RUN364DP_QUEUE, "DP 공격 재시드 대기열을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in [RESULT_JUDGMENT_RECEIPT, PERFORMANCE_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]), RESULT_JUDGMENT_RECEIPT, "판정/귀속/계보/주장 경계 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    return [
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


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(dn.PF_BALANCE_SURFACE)],
            "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward evidence(전진 근거)"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "effect": "DN의 순수익 단서를 긍정 단서로 보존하되 패키지 후보로 승격하지 않습니다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": f"best net {final['best_net_variant_id']} net {final['best_net_calibrated_net']} PF {final['best_net_calibrated_pf']}; best PF {final['best_pf_variant_id']} PF {final['best_pf_calibrated_pf']}",
            "comparison_baseline": [dn.BASELINE_RUN_ID, dn.RUNTIME_PROBE_RUN_ID],
            "likely_drivers": ["risk-scale multiplier(위험 배수)", "source quality filter(원천 품질 필터)", "hour veto(시간 배제)"],
            "negative_attribution": "PF did not clear DB 1.41(PF가 DB 1.41을 넘지 못함)",
            "next_probe": NEXT_RUN_ID,
            "effect": "성과 변화 원인을 다음 DP 제약으로 넘깁니다.",
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
            "lineage_judgment": "connected_no_package(패키지 없이 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_package": "not_opened",
            "effect": "PF 미달 후보를 운영 주장으로 올리지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return dn.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], summary: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DO h17 short-source PF/net polish review(17시 숏 원천 PF/순수익 다듬기 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_package(런타임 패키지): `not_opened(열지 않음)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): DN parameter-only polish(DN 파라미터 전용 다듬기)를 strict calibrated precheck(엄격 보정 사전검사) 기준으로 검토했습니다.

Effect(효과): net-only pass(순수익만 통과)를 runtime package(런타임 패키지)로 넘기지 않고, 다음 DP를 model/label/feature offensive reseed(모델/라벨/피처 공격 재시드)로 엽니다.

{markdown_table(summary, ['selected_variant_id', 'selected_calibrated_net', 'selected_calibrated_pf', 'selected_net_delta_vs_db', 'selected_pf_delta_vs_db', 'selected_short_count', 'strict_pass_count', 'net_pass_pf_fail_count'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'korean_read', 'constraint_for_next', 'effect'])}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'selected_variant_id', 'next_run_id', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This run(이번 실행)은 review only(검토 전용)입니다. MT5 execution(MT5 실행), runtime package(런타임 패키지), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DO decision(결정): PF/net polish review(PF/순수익 다듬기 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- selected calibrated net/PF(선택 보정 순수익/PF): `{final['selected_calibrated_net']}` / `{final['selected_calibrated_pf']}`
- strict_pass_count(엄격 통과 수): `{final['strict_pass_count']}`
- runtime package(런타임 패키지): `not_opened(열지 않음)`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DP는 파라미터 다듬기 반복이 아니라 새 short-source model/label/feature(숏 원천 모델/라벨/피처) 탐색으로 갑니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DO__{RUN_ID}", f"\n- run364DO__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - PF/net polish review(PF/순수익 다듬기 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DO__{RUN_ID}", f"\n<!-- run364DO__{RUN_ID} -->\n\n## run364DO PF/net Polish Review(PF/순수익 다듬기 검토)\n\nAction(행동): DN의 parameter-only polish(파라미터 전용 다듬기)를 엄격 보정 기준으로 판정했습니다.\n\nEffect(효과): strict pass(엄격 통과)가 0개라 runtime package(런타임 패키지)를 열지 않고 `{NEXT_RUN_ID}`로 model/label/feature offensive reseed(모델/라벨/피처 공격 재시드)를 엽니다.\n")
    append_text_once(STAGE_README, f"run364DO__{RUN_ID}", f"\n<!-- run364DO__{RUN_ID} -->\n## run364DO review(검토)\n\nParameter-only PF/net polish(파라미터 전용 PF/순수익 다듬기)는 strict package contract(엄격 패키지 계약)를 통과하지 못했습니다. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DO` reviewed(검토 완료) DN PF/net polish(DN PF/순수익 다듬기). Selected candidate(선택 후보) `{final['selected_variant_id']}`는 calibrated net/PF(보정 순수익/PF) `{final['selected_calibrated_net']}` / `{final['selected_calibrated_pf']}`였고, strict_pass_count(엄격 통과 수)는 `{final['strict_pass_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 short-source model/label/feature offensive reseed(숏 원천 모델/라벨/피처 공격 재시드)를 시작합니다.

Operating boundary(운영 경계): runtime package(런타임 패키지)는 열지 않았고 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): parameter-only PF/net polish(파라미터 전용 PF/순수익 다듬기)는 strict package contract(엄격 패키지 계약)를 통과하지 못했습니다.

Selected DN variant(선택 DN 변형): `{final['selected_variant_id']}`
Calibrated net/PF(보정 순수익/PF): `{final['selected_calibrated_net']}` / `{final['selected_calibrated_pf']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DO__{RUN_ID}", f"\n<!-- run364DO__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DN PF/net polish(DN PF/순수익 다듬기); strict pass 0; package not opened(패키지 열지 않음); next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364DO__{RUN_ID}", f"\n<!-- run364DO__{RUN_ID} -->\n- `{RUN_ID}`: parameter-only polish(파라미터 전용 다듬기)는 순수익을 올릴 수 있지만 PF 1.41을 넘지 못했습니다. Effect(효과): DP는 model/label/feature offensive reseed(모델/라벨/피처 공격 재시드)로 갑니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DO__parameter_only_pf_fail__{RUN_ID}", f"\n<!-- run364DO__parameter_only_pf_fail__{RUN_ID} -->\n- `{RUN_ID}`: DN parameter-only polish(DN 파라미터 전용 다듬기)는 strict calibrated DB net/PF exceedance(엄격 보정 DB 순수익/PF 초과)를 달성하지 못했습니다. Effect(효과): runtime package(런타임 패키지)를 열지 않고 새 수익 원천 탐색으로 전환합니다.\n")


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
        "scoreboard_lane": "proxy_review(프록시 검토)",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "evidence_boundary": "proxy_review_no_package_no_mt5_execution(프록시 검토, 패키지/MT5 실행 없음)",
        "question": "Should DN parameter-only polish move to runtime package?(DN 파라미터 전용 다듬기를 런타임 패키지로 넘길 것인가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_calibrated_net"],
        "profit_factor": final["selected_calibrated_pf"],
        "short_trade_count": final["selected_short_count"],
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(REVIEW_SUMMARY),
        "primary_kpi": f"strict_pass_count={final['strict_pass_count']};net_pass_pf_fail_count={final['net_pass_pf_fail_count']}",
        "guardrail_kpi": "runtime_package=not_opened;runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_source(필수 누락, Tier B 원천 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": "DO proxy review(DO 프록시 검토)", "status": status, "view": record_view, "tier": tier_scope, "metric_scope": "runtime_calibrated_proxy_review(런타임 보정 프록시 검토)"}
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "short_trade_count"]:
                row[key] = ""
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("review_summary", REVIEW_SUMMARY, "DO PF/net review summary(DO PF/순수익 검토 요약)."),
        ("failure_memory", FAILURE_MEMORY, "Parameter-only failure memory(파라미터 전용 실패 기억)."),
        ("package_decision", PACKAGE_DECISION, "Package decision(패키지 결정)."),
        ("queue", RUN364DP_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DO producer script(DO 생산 스크립트)."),
    ]:
        if exists(path):
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": artifact_type, "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{artifact_type}", "notes": notes})
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
    dn_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    summary, failure, package, _queue = build_reviews(dn_final)
    created_at = now_utc()
    gates = gate_rows(final_written=False)
    final = final_payload(dn_final, summary[0], gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final_written=True)
    final = final_payload(dn_final, summary[0], gates, created_at)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, summary, failure, package, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
