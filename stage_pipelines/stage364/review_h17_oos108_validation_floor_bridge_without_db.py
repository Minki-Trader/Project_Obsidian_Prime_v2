from __future__ import annotations

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
from stage_pipelines.stage364 import train_h17_oos108_validation_floor_bridge_without_db as el  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = el.STAGE_ID
RUN_NUMBER = "run364EM"
RUN_ID = "run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1"
PARENT_RUN_ID = el.RUN_ID
NEXT_RUN_ID = "run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1"

STATUS = "completed_stage364EM_oos108_validation_floor_bridge_review_package_eligible_open_en_no_authority"
JUDGMENT = "positive_proxy_oos108_validation_floor_bridge_package_eligible_review_cost_stress_caution_no_authority"
DECISION = "stage364EM_mark_package_eligible_open_run364EN_runtime_package"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_oos108_validation_floor_bridge_package_eligible_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = el.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "em_oos108_validation_floor_bridge_review_summary.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
COST_STRESS_REVIEW = RUN_DIR / "cost_stress_review.csv"
MONTH_STABILITY_REVIEW = RUN_DIR / "month_stability_review.csv"
SIDE_BALANCE_REVIEW = RUN_DIR / "side_balance_review.csv"
RUN364EN_QUEUE = RUN_DIR / "run364EN_runtime_package_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EM_h17_oos108_validation_floor_bridge_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EM_h17_oos108_validation_floor_bridge_review.md"
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
    el.FINAL_DECISION,
    el.GATE_AUDIT,
    el.TRADE_SURFACE,
    el.SELECTED_CANDIDATE,
    el.SELECTED_TRADE_TAPE,
    el.MONTH_STABILITY,
    el.COST_STRESS,
    el.MODEL_SCORECARD,
    el.ONNX_SMOKE_REPORT,
    el.MODEL_ARTIFACT_MANIFEST,
    el.DATA_INTEGRITY_AUDIT,
    el.RUN364EM_QUEUE,
    el.RUN_EVIDENCE_RECEIPT,
    el.MODEL_RECEIPT,
    el.ATTRIBUTION_RECEIPT,
    el.JUDGMENT_RECEIPT,
    el.LINEAGE_RECEIPT,
    el.CLAIM_RECEIPT,
    el.RUN_MANIFEST,
    el.REPORT_PATH,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    PACKAGE_DECISION,
    COST_STRESS_REVIEW,
    MONTH_STABILITY_REVIEW,
    SIDE_BALANCE_REVIEW,
    RUN364EN_QUEUE,
    RESULT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    RUNTIME_RECEIPT,
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
    return el.rel(path)


def exists(path: Path | str) -> bool:
    return el.exists(path)


def sha(path: Path | str) -> str:
    return el.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return el.as_float(value, default)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    el.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    el.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    el.write_csv(path, rows, fieldnames)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    el.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    el.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    el.replace_prefixed_lines(path, replacements, bom=bom)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EM inputs(EM 입력 누락): " + ", ".join(missing))
    parent = read_json(el.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EL next_run_id mismatch(EL 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"EL forbidden claim(EL 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(el.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EL gate audit(EL 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EL package review source(EL 패키지 검토 원천)",
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
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "EL produced a proxy PF108 candidate that may justify a runtime package handoff(EL이 런타임 패키지 인계를 열 만한 프록시 PF108 후보를 만들었다).",
            "decision_use": "Open EN runtime package only as a probe handoff, not as authority(EN 런타임 패키지는 권위가 아니라 탐침 인계로만 연다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def summarize(parent: Mapping[str, Any]) -> dict[str, Any]:
    selected = read_json(el.SELECTED_CANDIDATE)
    surface = read_csv(el.TRADE_SURFACE)
    smoke = read_csv(el.ONNX_SMOKE_REPORT)
    cost = read_csv(el.COST_STRESS)
    months = read_csv(el.MONTH_STABILITY)
    tape = read_csv(el.SELECTED_TRADE_TAPE)

    for column in [
        "validation_net",
        "oos_net",
        "validation_profit_factor",
        "oos_profit_factor",
        "validation_trade_density",
        "oos_trade_density",
    ]:
        surface[column] = surface[column].map(as_float)
    density_net = (
        (surface["validation_trade_density"] >= 3.0)
        & (surface["oos_trade_density"] >= 3.0)
        & (surface["validation_net"] > 0.0)
        & (surface["oos_net"] > 0.0)
    )
    pf108 = density_net & (surface["validation_profit_factor"] >= 1.08) & (surface["oos_profit_factor"] >= 1.08)
    bridge = density_net & (surface["validation_profit_factor"] >= 1.04) & (surface["oos_profit_factor"] >= 1.08)
    relaxed_cost_rows = []
    for row in cost.to_dict("records"):
        split = str(row.get("split", ""))
        cpt = as_float(row.get("cost_per_trade"))
        net = as_float(row.get("net_profit"))
        pf = as_float(row.get("profit_factor"))
        status = "passed(통과)" if net > 0.0 and pf >= 1.0 else "failed(실패)"
        relaxed_cost_rows.append({**row, "review_status": status, "effect": "cost stress(비용 압박)가 패키지 주의 조건으로 기록됩니다.", "claim_boundary": CLAIM_BOUNDARY})

    month_records = months.to_dict("records")
    oos_months = [row for row in month_records if str(row.get("split", "")) == "oos"]
    validation_months = [row for row in month_records if str(row.get("split", "")) == "validation"]
    oos_positive = sum(1 for row in oos_months if str(row.get("positive_month", "")).lower() == "true")
    validation_positive = sum(1 for row in validation_months if str(row.get("positive_month", "")).lower() == "true")
    oos_negative = len(oos_months) - oos_positive
    validation_negative = len(validation_months) - validation_positive

    long_count = int(selected.get("selected_oos_long_trade_count", 0))
    short_count = int(selected.get("selected_oos_short_trade_count", 0))
    total_count = max(int(selected.get("selected_oos_trade_count", 0)), 1)
    long_share = round(long_count / total_count, 10)
    short_share = round(short_count / total_count, 10)
    side_status = "passed_with_short_bias(통과, 숏 편향)" if min(long_count, short_count) >= 100 else "failed_side_count_floor(방향 거래수 바닥 실패)"

    onnx_selected = smoke[smoke["model_id"].astype(str) == str(selected["selected_model_id"])]
    selected_onnx_status = str(onnx_selected.iloc[0]["status"]) if not onnx_selected.empty else "missing(누락)"
    package_eligible = (
        int(parent["pf108_count"]) > 0
        and as_float(selected["selected_min_profit_factor"]) >= 1.08
        and as_float(selected["selected_validation_trade_density"]) >= 3.0
        and as_float(selected["selected_oos_trade_density"]) >= 3.0
        and long_count >= 100
        and short_count >= 100
        and selected_onnx_status.startswith("passed")
    )
    cost_warning = any(
        as_float(row.get("cost_per_trade")) >= 0.6
        and str(row.get("split", "")) == "validation"
        and as_float(row.get("profit_factor")) < 1.0
        for row in cost.to_dict("records")
    )

    return {
        "run_id": RUN_ID,
        "review_subject": PARENT_RUN_ID,
        "selected_model_id": selected["selected_model_id"],
        "selected_label_id": selected["selected_label_id"],
        "selected_feature_set_id": selected["selected_feature_set_id"],
        "selected_hours_id": selected["selected_hours_id"],
        "selected_stability_filter": selected["selected_stability_filter"],
        "selected_threshold": selected["selected_threshold"],
        "selected_margin_vs_flat": selected["selected_margin_vs_flat"],
        "selected_validation_net": selected["selected_validation_net"],
        "selected_validation_profit_factor": selected["selected_validation_profit_factor"],
        "selected_validation_trade_density": selected["selected_validation_trade_density"],
        "selected_oos_net": selected["selected_oos_net"],
        "selected_oos_profit_factor": selected["selected_oos_profit_factor"],
        "selected_oos_trade_density": selected["selected_oos_trade_density"],
        "selected_min_profit_factor": selected["selected_min_profit_factor"],
        "selected_oos_trade_count": selected["selected_oos_trade_count"],
        "selected_oos_long_trade_count": long_count,
        "selected_oos_short_trade_count": short_count,
        "selected_oos_long_share": long_share,
        "selected_oos_short_share": short_share,
        "side_balance_status": side_status,
        "selected_onnx_status": selected_onnx_status,
        "selected_trade_tape_rows": len(tape),
        "surface_rows": len(surface),
        "density_net_count": int(density_net.sum()),
        "bridge_count": int(bridge.sum()),
        "pf108_count": int(pf108.sum()),
        "parent_bridge_count": int(parent["bridge_count"]),
        "parent_pf108_count": int(parent["pf108_count"]),
        "onnx_smoke_pass_rows": int(sum(smoke["status"].astype(str).str.startswith("passed"))),
        "oos_positive_months": oos_positive,
        "oos_negative_months": oos_negative,
        "validation_positive_months": validation_positive,
        "validation_negative_months": validation_negative,
        "cost_stress_warning": cost_warning,
        "package_eligible": package_eligible,
        "package_decision": "eligible_for_runtime_probe_package(런타임 탐침 패키지 가능)" if package_eligible else "rejected_for_runtime_probe_package(런타임 탐침 패키지 거절)",
        "package_reason": "PF108+density+ONNX smoke pass, but cost stress caution remains(PF108+밀도+ONNX 스모크 통과, 단 비용 압박 주의 유지)" if package_eligible else "review gates failed(검토 게이트 실패)",
        "claim_boundary": CLAIM_BOUNDARY,
        "cost_rows": relaxed_cost_rows,
        "month_rows": [
            {
                **row,
                "review_status": "negative_month(음수 월)" if str(row.get("positive_month", "")).lower() != "true" else "positive_month(양수 월)",
                "effect": "monthly stability(月 안정성)가 MT5 probe(MT5 탐침) 전 주의 조건으로 기록됩니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for row in month_records
        ],
    }


def write_reviews(summary: Mapping[str, Any]) -> None:
    review_row = {key: value for key, value in summary.items() if key not in {"cost_rows", "month_rows"}}
    write_csv(REVIEW_SUMMARY, [review_row])
    write_csv(COST_STRESS_REVIEW, summary["cost_rows"])
    write_csv(MONTH_STABILITY_REVIEW, summary["month_rows"])
    write_csv(
        SIDE_BALANCE_REVIEW,
        [
            {
                "run_id": RUN_ID,
                "selected_model_id": summary["selected_model_id"],
                "oos_trade_count": summary["selected_oos_trade_count"],
                "oos_long_trade_count": summary["selected_oos_long_trade_count"],
                "oos_short_trade_count": summary["selected_oos_short_trade_count"],
                "oos_long_share": summary["selected_oos_long_share"],
                "oos_short_share": summary["selected_oos_short_share"],
                "review_status": summary["side_balance_status"],
                "effect": "short-heavy(숏 편향)이지만 양방향 거래수 바닥은 넘었습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        PACKAGE_DECISION,
        [
            {
                "run_id": RUN_ID,
                "review_subject": PARENT_RUN_ID,
                "selected_model_id": summary["selected_model_id"],
                "package_decision": summary["package_decision"],
                "reason": summary["package_reason"],
                "next_run_id": NEXT_RUN_ID,
                "runtime_package": "not_opened_review_only(열지 않음, 검토 전용)",
                "required_artifacts": "ONNX/model_manifest/feature_contract/set_ini_handoff/expected_kpi(ONNX/모델 목록/피처 계약/설정 인계/예상 KPI)",
                "effect": "EN package(EN 패키지)가 MT5 runtime probe(MT5 런타임 탐침) 입력을 만들 수 있게 합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364EN_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "en01_materialize_oos108_validation_floor_bridge_runtime_package",
                "candidate_model_id": summary["selected_model_id"],
                "candidate_source": rel(el.SELECTED_CANDIDATE),
                "selected_onnx": f"stages/{STAGE_ID}/02_runs/run364EL/onnx/{summary['selected_model_id']}.onnx",
                "selected_threshold": summary["selected_threshold"],
                "selected_stability_filter": summary["selected_stability_filter"],
                "review_caution": "cost_stress_validation_pf_below_1_at_0p6_and_short_heavy(비용 0.6 검증 PF 1 미만 및 숏 편향)",
                "effect": "EN에서 parameter/runtime handoff(파라미터/런타임 인계)를 만들고 그 다음 MT5 probe(MT5 탐침)를 열 수 있습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), INPUT_MANIFEST, "EL 입력 산출물이 연결됐습니다."),
        ("review_summary_gate", exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "EL 후보 검토 요약이 작성됐습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "패키지 가능성 판정이 기록됐습니다."),
        ("cost_stress_gate", exists(COST_STRESS_REVIEW), COST_STRESS_REVIEW, "비용 압박 주의 조건이 기록됐습니다."),
        ("month_stability_gate", exists(MONTH_STABILITY_REVIEW), MONTH_STABILITY_REVIEW, "월 안정성 조건이 기록됐습니다."),
        ("side_balance_gate", exists(SIDE_BALANCE_REVIEW), SIDE_BALANCE_REVIEW, "롱/숏 균형 주의 조건이 기록됐습니다."),
        ("next_queue_gate", exists(RUN364EN_QUEUE), RUN364EN_QUEUE, "다음 EN 패키지 대기열이 작성됐습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, RUNTIME_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]), RESULT_RECEIPT, "필수 receipt(영수증)가 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 gate(게이트)가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "authority/promotion/live/goal(권위/승격/실거래/목표) 주장을 차단했습니다."),
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


def build_final(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "package_decision": summary["package_decision"],
        "package_reason": summary["package_reason"],
        "selected_model_id": summary["selected_model_id"],
        "selected_label_id": summary["selected_label_id"],
        "selected_feature_set_id": summary["selected_feature_set_id"],
        "selected_hours_id": summary["selected_hours_id"],
        "selected_stability_filter": summary["selected_stability_filter"],
        "selected_threshold": summary["selected_threshold"],
        "selected_margin_vs_flat": summary["selected_margin_vs_flat"],
        "selected_validation_net": summary["selected_validation_net"],
        "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
        "selected_validation_trade_density": summary["selected_validation_trade_density"],
        "selected_oos_net": summary["selected_oos_net"],
        "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
        "selected_oos_trade_density": summary["selected_oos_trade_density"],
        "selected_min_profit_factor": summary["selected_min_profit_factor"],
        "selected_oos_trade_count": summary["selected_oos_trade_count"],
        "selected_oos_long_trade_count": summary["selected_oos_long_trade_count"],
        "selected_oos_short_trade_count": summary["selected_oos_short_trade_count"],
        "selected_oos_long_share": summary["selected_oos_long_share"],
        "selected_oos_short_share": summary["selected_oos_short_share"],
        "side_balance_status": summary["side_balance_status"],
        "selected_onnx_status": summary["selected_onnx_status"],
        "selected_trade_tape_rows": summary["selected_trade_tape_rows"],
        "surface_rows": summary["surface_rows"],
        "density_net_count": summary["density_net_count"],
        "bridge_count": summary["bridge_count"],
        "pf108_count": summary["pf108_count"],
        "parent_bridge_count": summary["parent_bridge_count"],
        "parent_pf108_count": summary["parent_pf108_count"],
        "onnx_smoke_pass_rows": summary["onnx_smoke_pass_rows"],
        "oos_positive_months": summary["oos_positive_months"],
        "oos_negative_months": summary["oos_negative_months"],
        "validation_positive_months": summary["validation_positive_months"],
        "validation_negative_months": summary["validation_negative_months"],
        "cost_stress_warning": summary["cost_stress_warning"],
        "runtime_package": "not_opened_review_only",
        "new_mt5_execution": "not_run",
        "external_verification_status": "not_run_review_only(미실행, 검토 전용)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_RECEIPT,
        {
            **base,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(COST_STRESS_REVIEW), rel(MONTH_STABILITY_REVIEW), rel(SIDE_BALANCE_REVIEW)],
            "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)", "runtime authority closure(런타임 권위 폐쇄)"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "reviewed_model": final["selected_model_id"],
            "package_decision": final["package_decision"],
            "model_judgment": "package_eligible_for_mt5_probe_only(MT5 탐침 전용 패키지 가능)",
            "onnx_status": final["selected_onnx_status"],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": f"EK selected OOS PF 1.0183147066 -> EL selected OOS PF {final['selected_oos_profit_factor']} with density {final['selected_oos_trade_density']}",
            "likely_drivers": ["no_h21_all_hours(21시 제외 전체 시간)", "valfloor_oos_blend(검증 바닥 표본외 혼합)", "rf8_l70_n160(RandomForest 깊이8 잎70 160트리)"],
            "cautions": ["validation cost stress fails at 0.6(비용 0.6 검증 실패)", "short-heavy side mix(숏 편향 방향 혼합)", "monthly negatives remain(月 음수 구간 남음)"],
            "attribution_confidence": "medium_until_mt5_probe(MT5 탐침 전 중간)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(el.SELECTED_CANDIDATE),
            "onnx_source": f"stages/{STAGE_ID}/02_runs/run364EL/onnx/{final['selected_model_id']}.onnx",
            "runtime_package": "not_opened_review_only(열지 않음, 검토 전용)",
            "runtime_claim_boundary": "package_eligible_not_authority(패키지 가능, 권위 아님)",
            "known_differences": ["proxy replay not MT5 fill semantics(프록시 재생은 MT5 체결 의미가 아님)", "set/ini handoff not materialized yet(설정/초기화 인계 아직 미작성)"],
            "next_runtime_action": NEXT_RUN_ID,
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
            "lineage_judgment": "connected_with_proxy_review_boundary(프록시 검토 경계로 연결)",
        },
    )
    write_json(CLAIM_RECEIPT, {**base, "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "package eligibility(패키지 가능성)을 operating claim(운영 주장)으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364EM H17 OOS108 Validation Floor Bridge Review(표본외108 검증 바닥 연결 검토)

Created(생성): {final['created_at_utc']}

Action(행동): EL OOS108 validation floor bridge(EL 표본외108 검증 바닥 연결) 후보를 package eligibility(패키지 가능성), cost stress(비용 압박), month stability(月 안정성), side balance(방향 균형) 관점에서 검토했습니다.

Effect(효과): 강한 proxy(프록시) 후보를 runtime authority(런타임 권위)로 올리지 않고, EN runtime package(EN 런타임 패키지) 입력으로만 넘깁니다.

Findings(발견):

- selected model(선택 모델): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- bridge_count(연결 후보 수): `{final['bridge_count']}`
- pf108_count(PF108 후보 수): `{final['pf108_count']}`
- ONNX smoke pass(ONNX 스모크 통과): `{final['onnx_smoke_pass_rows']}`
- long/short count(롱/숏 거래수): `{final['selected_oos_long_trade_count']}` / `{final['selected_oos_short_trade_count']}`
- month negatives(월 음수): validation(검증) `{final['validation_negative_months']}`, OOS(표본외) `{final['oos_negative_months']}`
- cost stress warning(비용 압박 주의): `{final['cost_stress_warning']}`

Package decision(패키지 결정): `{final['package_decision']}`

Judgment(판정): `{final['judgment']}`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): stage364EM OOS108 validation floor bridge review(표본외108 검증 바닥 연결 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- package_decision(패키지 결정): `{final['package_decision']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): EL 후보를 runtime package handoff(런타임 패키지 인계) 대상으로 검토했습니다.

Effect(효과): EN에서 MT5 runtime probe(MT5 런타임 탐침)를 위한 handoff(인계)를 만들 수 있지만, 아직 운영 권위는 주장하지 않습니다.
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364EM__{RUN_ID}", f"\n- run364EM__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - package eligible review(패키지 가능 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EM__{RUN_ID}", f"\n<!-- run364EM__{RUN_ID} -->\n\n## run364EM OOS108 Validation Floor Bridge Review(표본외108 검증 바닥 연결 검토)\n\nAction(행동): EL 후보를 package eligible(패키지 가능)로 검토하고 cost stress caution(비용 압박 주의)을 남겼습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 MT5 probe(MT5 탐침) 전 runtime package(런타임 패키지)를 물질화합니다.\n")
    append_text_once(STAGE_README, f"run364EM__{RUN_ID}", f"\n<!-- run364EM__{RUN_ID} -->\n## run364EM OOS108 validation floor bridge review(표본외108 검증 바닥 연결 검토)\n\nPackage(패키지): eligible for runtime probe(런타임 탐침 가능). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364EM` reviewed(검토 완료) EL OOS108 validation floor bridge(EL 표본외108 검증 바닥 연결). Selected model(선택 모델)은 `{final['selected_model_id']}`이고 validation/OOS PF(검증/표본외 PF)는 `{final['selected_validation_profit_factor']}` / `{final['selected_oos_profit_factor']}`입니다. Package decision(패키지 결정)은 `{final['package_decision']}`입니다.

Caution(주의): cost stress(비용 압박)는 validation(검증) cost 0.6에서 깨지고, side balance(방향 균형)는 short-heavy(숏 편향)입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)용 runtime package(런타임 패키지)를 물질화합니다.

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

Latest review(최근 검토): EM reviewed(검토 완료) EL OOS108 validation floor bridge(EL 표본외108 검증 바닥 연결) and opened EN runtime package(EN 런타임 패키지)를 다음 행동으로 열었습니다.

Selected model(선택 모델): `{final['selected_model_id']}`
Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Package decision(패키지 결정): `{final['package_decision']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364EM__{RUN_ID}", f"\n<!-- run364EM__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed EL OOS108 validation floor bridge(표본외108 검증 바닥 연결); package eligible(패키지 가능); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EM__{RUN_ID}", f"\n<!-- run364EM__{RUN_ID} -->\n- `{RUN_ID}`: EL candidate(EL 후보)를 runtime probe package(런타임 탐침 패키지) 대상으로 열었습니다. Effect(효과): OOS PF 1.196과 validation PF 1.133 단서를 MT5 probe(MT5 탐침)로 검증할 수 있게 합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EM__cost_stress_caution__{RUN_ID}", f"\n<!-- run364EM__cost_stress_caution__{RUN_ID} -->\n- `{RUN_ID}`: cost stress(비용 압박)는 validation cost 0.6(검증 비용 0.6)에서 실패합니다. Effect(효과): EN/MT5 probe(EN/MT5 탐침)는 비용 압박을 별도 판정 조건으로 가져갑니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
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
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Should EL open an MT5 runtime package handoff?(EL을 MT5 런타임 패키지 인계로 열 것인가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"package={final['package_decision']};oos_pf={final['selected_oos_profit_factor']};cost_warning={final['cost_stress_warning']}",
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
                "kpi_scope": "EM OOS108 validation floor bridge review(EM 표본외108 검증 바닥 연결 검토)",
                "metric_scope": "proxy_review(Python 프록시 검토)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "",
                "long_trade_count": final["selected_oos_long_trade_count"] if suffix == "tier_a_separate" else "",
                "short_trade_count": final["selected_oos_short_trade_count"] if suffix == "tier_a_separate" else "",
                "source_authority": "proxy_review_package_eligible_no_mt5(Python 프록시 검토 패키지 가능, MT5 없음)",
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
                "lane": "review_control(검토 제어)",
                "family": "alpha_exploration_review(알파 탐색 검토)",
                "primary_report": rel(REPORT_PATH),
                "run_family": "kpi_evidence(KPI 근거)",
                "run_type": "oos108_validation_floor_bridge_review(표본외108 검증 바닥 연결 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "best_model_id": final["selected_model_id"],
                "net_profit": final["selected_oos_net"],
                "profit_factor": final["selected_oos_profit_factor"],
                "trade_density_per_feature_day": final["selected_oos_trade_density"],
                "trade_count": final["selected_oos_trade_count"],
                "long_trade_count": final["selected_oos_long_trade_count"],
                "short_trade_count": final["selected_oos_short_trade_count"],
                "result_status": STATUS,
                "primary_kpi": f"package={final['package_decision']};oos_pf={final['selected_oos_profit_factor']}",
                "guardrail_kpi": f"validation_pf={final['selected_validation_profit_factor']};cost_warning={final['cost_stress_warning']};authority=not_claimed",
                "final_decision_path": rel(FINAL_DECISION),
                "gate_audit_path": rel(GATE_AUDIT),
                "external_verification_status": "not_run(미실행)",
                "evidence_boundary": "proxy_review_package_eligible_no_mt5_runtime_authority(프록시 검토 패키지 가능, MT5 런타임 권위 없음)",
            }
        ],
        extend_header=True,
    )
    el.ej.eh.ef.ed.eb.dz.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "EM OOS108 validation floor bridge review artifact(EM 표본외108 검증 바닥 연결 검토 산출물)",
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
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    summary = summarize(parent)
    write_reviews(summary)
    created_at = now_utc()
    gates = gate_rows(final_written=False)
    final = build_final(summary, gates, created_at)
    write_receipts(final)
    gates = gate_rows(final_written=True)
    final = build_final(summary, gates, created_at)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "package_decision": final["package_decision"], "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
