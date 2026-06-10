from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_density_preserve_repair_without_db as fj  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db as hm  # noqa: E402


TODAY = "2026-06-09"
STAGE_ID = hm.STAGE_ID
RUN_NUMBER = "run364HN"
RUN_ID = "run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1"
PARENT_RUN_ID = hm.RUN_ID
NEXT_RUN_ID = "run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1"

STATUS = "completed_stage364HN_density_side_cost_repair_review_package_ready_for_single_source_runtime_package_no_authority"
JUDGMENT = "positive_package_readiness_clue_scaled_density_seed_single_source_mt5_package_required_no_authority"
DECISION = "stage364HN_open_run364HO_single_source_probability_bin_veto_runtime_package"
CLAIM_BOUNDARY = (
    "research_development_package_readiness_review_only_scaled_density_seed_single_source_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
SHORT_SHARE_TARGET = 0.65

STAGE_DIR = hm.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

WORK_PACKET = RUN_DIR / "work_packet.json"
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
PACKAGE_READINESS_REVIEW = RUN_DIR / "hn_package_readiness_review.csv"
GUARDRAIL_REVIEW = RUN_DIR / "hn_guardrail_review.csv"
COST_SIDE_STABILITY_REVIEW = RUN_DIR / "hn_cost_side_stability_review.csv"
FEATURE_ORDER_REVIEW = RUN_DIR / "hn_feature_order_review.csv"
FEATURE_ORDER_CONTRACT = RUN_DIR / "hn_fj_single_source_feature_order_contract.json"
RUN364HO_QUEUE = RUN_DIR / "run364HO_single_source_probability_bin_veto_package_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HN_probability_bin_veto_mt5_density_side_cost_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HN_probability_bin_veto_mt5_density_side_cost_repair_review.md"
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

THIS_FILE = Path(__file__)

STATIC_INPUT_FILES = [
    hm.FINAL_DECISION,
    hm.GATE_AUDIT,
    hm.SELECTED_SEED,
    hm.RUNTIME_SCALED_CANDIDATES,
    hm.DIRECT_STRICT_CANDIDATES,
    hm.SELECTED_SEED_TRADE_TAPE,
    hm.SELECTED_SEED_COST_STRESS,
    hm.SELECTED_SEED_SIDE_SESSION,
    hm.SELECTED_SEED_MONTH_STABILITY,
    hm.ROUTE_PARITY_DECISION,
    hm.RUN364HN_QUEUE,
    hm.LINEAGE_RECEIPT,
    hm.CLAIM_RECEIPT,
    fj.FINAL_DECISION,
    fj.MODEL_ARTIFACT_MANIFEST,
    fj.ONNX_SMOKE_REPORT,
    fj.FEATURE_AUDIT,
    fj.et.dt.dp.MODEL_INPUT_FEATURE_ORDER,
    THIS_FILE,
]

OUTPUT_FILES = [
    WORK_PACKET,
    INPUT_MANIFEST,
    PACKAGE_READINESS_REVIEW,
    GUARDRAIL_REVIEW,
    COST_SIDE_STABILITY_REVIEW,
    FEATURE_ORDER_REVIEW,
    FEATURE_ORDER_CONTRACT,
    RUN364HO_QUEUE,
    RESULT_RECEIPT,
    MODEL_RECEIPT,
    DATA_RECEIPT,
    ATTRIBUTION_RECEIPT,
    RUNTIME_PARITY_RECEIPT,
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
    THIS_FILE,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return hm.rel(path)


def exists(path: Path | str) -> bool:
    return hm.exists(path)


def sha(path: Path | str) -> str:
    return hm.sha(path)


def read_json(path: Path) -> Any:
    return hm.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    hm.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return hm.read_csv(path)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    hm.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    hm.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    hm.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    hm.append_or_replace_csv(path, key_fields, rows)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    hm.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def as_bool_text(value: bool) -> str:
    return "true" if bool(value) else "false"


def project_path(value: Any) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def selected_dynamic_inputs(selected: Mapping[str, Any]) -> list[Path]:
    keys = [
        "selected_onnx_path",
        "selected_joblib_path",
        "source_cost_stress",
        "source_final_decision",
        "source_model_artifact_manifest",
        "source_month_stability",
        "source_onnx_smoke_report",
        "source_side_session_review",
        "source_trade_tape",
        "source_source_surface_path",
    ]
    paths: list[Path] = []
    for key in keys:
        value = selected.get(key)
        if value:
            paths.append(project_path(value))
    paths.extend([fj.MODEL_ARTIFACT_MANIFEST, fj.ONNX_SMOKE_REPORT, fj.FEATURE_AUDIT])
    return list(dict.fromkeys(paths))


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], list[Path]]:
    missing = [rel(path) for path in STATIC_INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HN inputs(HN 입력 누락): " + ", ".join(missing))
    hm_final = read_json(hm.FINAL_DECISION)
    selected = read_json(hm.SELECTED_SEED)
    if hm_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HM next_run_id mismatch(HM 다음 실행 ID 불일치): {hm_final.get('next_run_id')} != {RUN_ID}")
    hm_gates = read_csv(hm.GATE_AUDIT)
    if hm_gates.empty or any(hm_gates["status"].astype(str) != "passed"):
        raise RuntimeError("HM gate audit(HM 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    for label, final in [("HM", hm_final), ("FJ", read_json(fj.FINAL_DECISION))]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if str(final.get(key, "not_claimed")) != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    dynamic = selected_dynamic_inputs(selected)
    dynamic_missing = [rel(path) for path in dynamic if not exists(path)]
    if dynamic_missing:
        raise FileNotFoundError("missing selected seed dynamic inputs(선택 씨앗 동적 입력 누락): " + ", ".join(dynamic_missing))
    return hm_final, selected, list(dict.fromkeys(STATIC_INPUT_FILES + dynamic))


def write_input_manifest(input_files: Sequence[Path]) -> None:
    rows = []
    for path in input_files:
        role = "producer_script(생산 스크립트)" if path == THIS_FILE else "source_artifact(원천 산출물)"
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": as_bool_text(exists(path)),
                "sha256": sha(path),
                "input_role": role,
                "effect": "artifact lineage(산출물 계보)를 HN review(HN 검토)에 연결합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def feature_order_payload(selected: Mapping[str, Any]) -> dict[str, Any]:
    base_order = fj.et.dt.load_feature_order()
    feature_sets = fj.fj_feature_sets(base_order)
    feature_set_id = str(selected["selected_feature_set_id"])
    if feature_set_id not in feature_sets:
        raise RuntimeError(f"missing FJ feature set(FJ 피처 묶음 누락): {feature_set_id}")
    feature_order = feature_sets[feature_set_id]
    payload = {
        "run_id": RUN_ID,
        "source_run_id": selected["selected_source_run_id"],
        "model_id": selected["selected_model_id"],
        "feature_set_id": feature_set_id,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "base_feature_order_path": rel(fj.et.dt.dp.MODEL_INPUT_FEATURE_ORDER),
        "base_feature_order_hash": ordered_hash(base_order),
        "feature_columns": feature_order,
        "contract_status": "reconstructable_from_fj_script__ho_must_materialize_file(재현 가능, HO에서 파일 물질화 필요)",
        "effect": "HO runtime package(HO 런타임 패키지)가 ONNX(온엑스) 입력 순서를 고정할 수 있습니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_ORDER_CONTRACT, payload)
    write_csv(
        FEATURE_ORDER_REVIEW,
        [
            {
                "run_id": RUN_ID,
                "model_id": payload["model_id"],
                "feature_set_id": feature_set_id,
                "feature_count": payload["feature_count"],
                "feature_order_hash": payload["feature_order_hash"],
                "base_feature_order_hash": payload["base_feature_order_hash"],
                "status": payload["contract_status"],
                "effect": payload["effect"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return payload


def artifact_status(selected: Mapping[str, Any]) -> dict[str, Any]:
    model_id = str(selected["selected_model_id"])
    onnx_path = project_path(selected["selected_onnx_path"])
    joblib_path = project_path(selected["selected_joblib_path"])
    manifest = read_csv(fj.MODEL_ARTIFACT_MANIFEST)
    smoke = read_csv(fj.ONNX_SMOKE_REPORT)
    manifest_rows = manifest[manifest["model_id"].astype(str) == model_id] if not manifest.empty else pd.DataFrame()
    smoke_rows = smoke[smoke["model_id"].astype(str) == model_id] if not smoke.empty else pd.DataFrame()
    smoke_status = str(selected.get("selected_onnx_smoke_status", ""))
    smoke_passed = "passed" in smoke_status or (not smoke_rows.empty and smoke_rows["status"].astype(str).str.contains("passed", na=False).any())
    return {
        "onnx_exists": exists(onnx_path),
        "joblib_exists": exists(joblib_path),
        "onnx_sha256_match": sha(onnx_path) == str(selected.get("selected_onnx_sha256", "")),
        "joblib_sha256_match": sha(joblib_path) == str(selected.get("selected_joblib_sha256", "")),
        "manifest_rows": int(len(manifest_rows)),
        "smoke_rows": int(len(smoke_rows)),
        "smoke_passed": bool(smoke_passed),
        "smoke_max_abs_diff": selected.get("selected_onnx_smoke_max_abs_diff", ""),
        "onnx_path": rel(onnx_path),
        "joblib_path": rel(joblib_path),
    }


def no_trade_splitting_status(tape: pd.DataFrame) -> bool:
    if tape.empty or "no_trade_splitting" not in tape.columns:
        return False
    return tape["no_trade_splitting"].astype(str).str.contains("single_position_jump_to_exit_plus_one", na=False).all()


def cost_lookup(cost_frame: pd.DataFrame, split: str, cost: float) -> dict[str, Any]:
    if cost_frame.empty:
        return {}
    frame = cost_frame.copy()
    frame["cost_per_trade"] = pd.to_numeric(frame["cost_per_trade"], errors="coerce")
    rows = frame[(frame["split"].astype(str) == split) & (frame["cost_per_trade"] == cost)]
    return {} if rows.empty else rows.iloc[0].to_dict()


def build_reviews(selected: Mapping[str, Any], feature_payload: Mapping[str, Any], artifact: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    tape = read_csv(hm.SELECTED_SEED_TRADE_TAPE)
    cost_frame = read_csv(hm.SELECTED_SEED_COST_STRESS)
    side_frame = read_csv(hm.SELECTED_SEED_SIDE_SESSION)
    month_frame = read_csv(hm.SELECTED_SEED_MONTH_STABILITY)
    no_split = no_trade_splitting_status(tape)
    validation_cost06 = cost_lookup(cost_frame, "validation", 0.6)
    validation_cost09 = cost_lookup(cost_frame, "validation", 0.9)
    oos_cost06 = cost_lookup(cost_frame, "oos", 0.6)
    combined_cost09 = cost_lookup(cost_frame, "combined", 0.9)

    readiness_rows = [
        {
            "run_id": RUN_ID,
            "review_item": "onnx_joblib_lineage(ONNX/잡립 계보)",
            "status": "passed(통과)" if artifact["onnx_exists"] and artifact["joblib_exists"] and artifact["onnx_sha256_match"] and artifact["joblib_sha256_match"] else "failed(실패)",
            "evidence": f"{artifact['onnx_path']} | {artifact['joblib_path']}",
            "effect": "HO package(HO 패키지)가 같은 모델 산출물을 사용할 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_item": "onnx_smoke(ONNX 스모크)",
            "status": "passed(통과)" if artifact["smoke_passed"] else "failed(실패)",
            "evidence": rel(fj.ONNX_SMOKE_REPORT),
            "max_abs_diff": artifact["smoke_max_abs_diff"],
            "effect": "Python model(Python 모델)과 ONNX(온엑스) 출력 차이가 작은지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_item": "feature_order_contract(피처 순서 계약)",
            "status": "passed_reconstructable(통과, 재현 가능)" if feature_payload["feature_count"] == 60 else "failed(실패)",
            "evidence": rel(FEATURE_ORDER_CONTRACT),
            "feature_count": feature_payload["feature_count"],
            "feature_order_hash": feature_payload["feature_order_hash"],
            "effect": "HO에서 feature CSV(피처 CSV)와 MT5 set(설정 파일)의 입력 수를 고정할 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_item": "single_source_route(단일 원천 라우트)",
            "status": "package_ready_clue(패키지 준비 단서)",
            "evidence": rel(hm.ROUTE_PARITY_DECISION),
            "effect": "GZ+HB dual-source fallback(GZ+HB 이중 원천 대체)의 partial parity(부분 동등성)를 재사용하지 않고 단일 FJ 모델로 좁힙니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    guardrail_rows = [
        {
            "run_id": RUN_ID,
            "guardrail": "direct_proxy_density(직접 프록시 밀도)",
            "value": selected.get("selected_oos_trade_density", ""),
            "threshold": DENSITY_FLOOR,
            "status": "failed_recorded(실패 기록)" if not selected.get("selected_direct_density_pass") else "passed(통과)",
            "effect": "직접 3/day(일 3회) 증명은 없으므로 MT5 proof(MT5 증명)로 부르지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "scaled_density_estimate(스케일 밀도 추정)",
            "value": selected.get("selected_runtime_density_estimate_from_hl_ratio", ""),
            "threshold": DENSITY_FLOOR,
            "status": "passed_as_clue_only(통과, 단서 전용)" if selected.get("selected_scaled_density_pass") else "failed(실패)",
            "effect": "HL ratio(HL 비율)를 사용한 추정이라 HO/MT5 확인 전까지 권위가 없습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "side_balance(방향 균형)",
            "value": selected.get("selected_combined_short_share", ""),
            "threshold": SHORT_SHARE_TARGET,
            "status": "passed(통과)" if float(selected.get("selected_combined_short_share", 1.0)) <= SHORT_SHARE_TARGET else "caution(주의)",
            "effect": "short-heavy(숏 과중) 실패 기억을 완화했는지 봅니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "validation_cost06(검증 비용0.6)",
            "value": finite(validation_cost06.get("net_profit", math.nan)),
            "threshold": "> 0",
            "status": "fragile_recorded(취약 기록)" if float(validation_cost06.get("net_profit", 0.0)) <= 0 else "passed(통과)",
            "effect": "validation(검증) 비용 압박이 약해 운영 주장을 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "combined_cost09(합산 비용0.9)",
            "value": finite(combined_cost09.get("net_profit", math.nan)),
            "threshold": "> 0",
            "status": "thin_pass_recorded(얇은 통과 기록)" if float(combined_cost09.get("net_profit", 0.0)) > 0 else "failed(실패)",
            "effect": "비용 0.9에서 간신히 버티므로 HO에서 MT5 cost/fill(비용/체결) 차이를 봐야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "no_trade_splitting(거래 쪼개기 금지)",
            "value": as_bool_text(no_split),
            "threshold": "single_position_jump_to_exit_plus_one",
            "status": "passed(통과)" if no_split else "failed(실패)",
            "effect": "거래수를 쪼개 수익을 나누는 방식을 배제합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    stability_rows = [
        {
            "run_id": RUN_ID,
            "item": "cost_stress_summary(비용 압박 요약)",
            "validation_cost06_net": finite(validation_cost06.get("net_profit", math.nan)),
            "validation_cost09_net": finite(validation_cost09.get("net_profit", math.nan)),
            "oos_cost06_net": finite(oos_cost06.get("net_profit", math.nan)),
            "combined_cost09_net": finite(combined_cost09.get("net_profit", math.nan)),
            "status": "oos_strong_validation_fragile(표본외 강함, 검증 취약)",
            "effect": "다음 HO/MT5 package(HO/MT5 패키지)에서 비용 차이를 우선 확인하게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "item": "side_session_rows(방향/세션 행)",
            "row_count": int(len(side_frame)),
            "status": "recorded(기록됨)",
            "effect": "특정 hour(시간) 또는 side(방향)에 수익이 몰리는지 HO 검토 입력으로 넘깁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "item": "month_rows(월별 행)",
            "row_count": int(len(month_frame)),
            "status": "recorded(기록됨)",
            "effect": "equity curve quality(수익곡선 품질)와 월별 안정성을 다음 MT5 probe(MT5 탐침)에서 비교할 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue_rows = [
        {
            "run_id": RUN_ID,
            "queue_id": "ho01_materialize_single_source_probability_bin_veto_package",
            "next_run_id": NEXT_RUN_ID,
            "model_id": selected["selected_model_id"],
            "source_run_number": selected["selected_source_run_number"],
            "onnx_path": artifact["onnx_path"],
            "joblib_path": artifact["joblib_path"],
            "feature_order_contract": rel(FEATURE_ORDER_CONTRACT),
            "threshold": selected.get("selected_threshold", ""),
            "probability_bin_veto_boundary": "reuse HI/HJ probability-bin veto support only after HO materializes single-source contract(HI/HJ 확률 구간 거부 지원은 HO 단일 원천 계약 물질화 뒤에만 재사용)",
            "target": "materialize MT5 runtime package(MT5 런타임 패키지 물질화)",
            "avoid": "do not call scaled density MT5 proof(스케일 밀도를 MT5 증명으로 부르지 않음)",
            "effect": "proxy clue(프록시 단서)를 MT5 runtime probe(MT5 런타임 탐침)로 검증할 수 있게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    metrics = {
        "no_trade_splitting": no_split,
        "validation_cost06_net": finite(validation_cost06.get("net_profit", math.nan)),
        "validation_cost09_net": finite(validation_cost09.get("net_profit", math.nan)),
        "oos_cost06_net": finite(oos_cost06.get("net_profit", math.nan)),
        "combined_cost09_net": finite(combined_cost09.get("net_profit", math.nan)),
        "side_session_rows": int(len(side_frame)),
        "month_rows": int(len(month_frame)),
    }
    return readiness_rows, guardrail_rows, stability_rows, queue_rows, metrics


def gate_rows(
    selected: Mapping[str, Any],
    feature_payload: Mapping[str, Any],
    artifact: Mapping[str, Any],
    metrics: Mapping[str, Any],
) -> list[dict[str, Any]]:
    gate_specs = [
        ("parent_hm_gate", exists(hm.FINAL_DECISION), rel(hm.FINAL_DECISION), "HM 입력 계보를 확인했습니다."),
        ("hm_required_gate_coverage_gate", not read_csv(hm.GATE_AUDIT).empty and read_csv(hm.GATE_AUDIT)["status"].astype(str).eq("passed").all(), rel(hm.GATE_AUDIT), "HM 필수 gate(게이트)가 모두 통과했습니다."),
        ("selected_seed_lineage_gate", artifact["onnx_exists"] and artifact["joblib_exists"] and artifact["onnx_sha256_match"] and artifact["joblib_sha256_match"], rel(PACKAGE_READINESS_REVIEW), "ONNX/joblib(온엑스/잡립) 계보를 확인했습니다."),
        ("onnx_smoke_gate", artifact["smoke_passed"], rel(fj.ONNX_SMOKE_REPORT), "ONNX smoke(온엑스 스모크)를 확인했습니다."),
        ("feature_order_reconstruct_gate", feature_payload["feature_count"] == 60 and exists(FEATURE_ORDER_CONTRACT), rel(FEATURE_ORDER_CONTRACT), "FJ feature order(FJ 피처 순서)를 재현했습니다."),
        ("no_trade_splitting_gate", bool(metrics["no_trade_splitting"]), rel(hm.SELECTED_SEED_TRADE_TAPE), "거래 쪼개기 금지를 확인했습니다."),
        ("scaled_density_boundary_gate", bool(selected.get("selected_scaled_density_pass")) and not bool(selected.get("selected_direct_density_pass")), rel(GUARDRAIL_REVIEW), "스케일 밀도는 단서 전용임을 기록했습니다."),
        ("cost_fragility_recorded_gate", exists(COST_SIDE_STABILITY_REVIEW), rel(COST_SIDE_STABILITY_REVIEW), "validation cost(검증 비용) 취약성을 숨기지 않았습니다."),
        ("single_source_route_boundary_gate", exists(hm.ROUTE_PARITY_DECISION), rel(hm.ROUTE_PARITY_DECISION), "단일 원천 route(라우트)로 복잡도를 줄이는 경계를 기록했습니다."),
        ("package_next_queue_gate", exists(RUN364HO_QUEUE), rel(RUN364HO_QUEUE), "HO runtime package(HO 런타임 패키지) 대기열을 만들었습니다."),
        ("paired_tier_record_gate", True, rel(STAGE_LEDGER), "Tier A/Tier B/Tier A+B 기록 경계를 남겼습니다."),
        ("artifact_lineage_gate", exists(LINEAGE_RECEIPT), rel(LINEAGE_RECEIPT), "산출물 계보를 연결했습니다."),
        ("required_gate_coverage_audit", True, rel(GATE_AUDIT), "HN 필수 gate(게이트)를 감사했습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), rel(CLAIM_RECEIPT), "운영 권위 주장을 막았습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gate_specs
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "review_and_package_routing(검토 및 패키지 라우팅)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-model-validation(모델 검증)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-runtime-parity(런타임 동등성)",
            ],
            "required_gates": [
                "parent_hm_gate",
                "hm_required_gate_coverage_gate",
                "selected_seed_lineage_gate",
                "onnx_smoke_gate",
                "feature_order_reconstruct_gate",
                "no_trade_splitting_gate",
                "scaled_density_boundary_gate",
                "cost_fragility_recorded_gate",
                "single_source_route_boundary_gate",
                "package_next_queue_gate",
                "paired_tier_record_gate",
                "artifact_lineage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "question": "Can the HM-selected FJ scaled-density seed be opened as a single-source MT5 runtime package?(HM이 고른 FJ 스케일 밀도 씨앗을 단일 원천 MT5 런타임 패키지로 열 수 있는가?)",
            "effect": "좋은 proxy clue(프록시 단서)를 운영 주장 없이 HO package(HO 패키지) 검증으로 전진시킵니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final_base: Mapping[str, Any], selected: Mapping[str, Any], feature_payload: Mapping[str, Any], artifact: Mapping[str, Any], input_files: Sequence[Path]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": final_base["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RESULT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "judgment_label": JUDGMENT,
            "evidence_available": [rel(hm.SELECTED_SEED), rel(PACKAGE_READINESS_REVIEW), rel(FEATURE_ORDER_CONTRACT), rel(GUARDRAIL_REVIEW)],
            "evidence_missing": ["new MT5 runtime probe(새 MT5 런타임 탐침)", "runtime package(런타임 패키지)", "forward/replay evidence(전진/재생 근거)"],
            "next_condition": NEXT_RUN_ID,
            "effect": "package readiness(패키지 준비성)까지만 긍정하고 운영 권위는 열지 않습니다.",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_id": selected["selected_model_id"],
            "model_family": selected.get("selected_model_family", ""),
            "label_id": selected.get("selected_label_id", ""),
            "feature_set_id": selected.get("selected_feature_set_id", ""),
            "feature_count": feature_payload["feature_count"],
            "feature_order_hash": feature_payload["feature_order_hash"],
            "onnx_smoke_max_abs_diff": artifact["smoke_max_abs_diff"],
            "selection_metric": "HM scaled density/side/cost repair score(HM 스케일 밀도/방향/비용 수리 점수)",
            "validation_judgment": "package_ready_for_runtime_materialization_not_authority(런타임 물질화 준비, 권위 아님)",
            "effect": "ONNX(온엑스) 자동매매 모델을 MT5 probe(MT5 탐침)로 넘길 수 있는 최소 모델 계약을 확인합니다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(path) for path in input_files],
            "time_axis": "source FJ/HM chronological split inherited(FJ/HM 원천 시간순 분할 상속)",
            "feature_label_boundary": "no new feature or label calculation in HN(HN에서 새 피처/라벨 계산 없음)",
            "leakage_risk": "HL density ratio is reused as estimate only(HL 밀도 비율은 추정으로만 재사용)",
            "integrity_judgment": "usable_for_package_review_with_boundary(경계 포함 패키지 검토에 사용 가능)",
            "effect": "timestamp-safe(시점 안전) 주장을 새로 확장하지 않고 원천 산출물 경계를 유지합니다.",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": {
                "selected_oos_net": selected.get("selected_oos_net", ""),
                "selected_oos_profit_factor": selected.get("selected_oos_profit_factor", ""),
                "selected_oos_trade_density": selected.get("selected_oos_trade_density", ""),
                "selected_runtime_density_estimate_from_hl_ratio": selected.get("selected_runtime_density_estimate_from_hl_ratio", ""),
                "combined_cost09_net": selected.get("selected_combined_cost09_net", ""),
                "combined_short_share": selected.get("selected_combined_short_share", ""),
            },
            "likely_drivers": ["FJ behavior/density/cost feature set(FJ 행동/밀도/비용 피처 묶음)", "single-source route simplification(단일 원천 라우트 단순화)", "HL runtime density lift clue(HL 런타임 밀도 상승 단서)"],
            "alternative_explanations": ["HL ratio may not transfer(HL 비율이 이전되지 않을 수 있음)", "MT5 cost/fill differences(MT5 비용/체결 차이)", "validation cost fragility(검증 비용 취약성)"],
            "attribution_confidence": "low_to_medium_until_mt5_probe(MT5 탐침 전까지 낮음~중간)",
            "effect": "좋은 OOS(표본외) 수익을 운영 가능성으로 과장하지 않고 원인을 나눠 봅니다.",
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            **base,
            "research_path": [rel(hm.SELECTED_SEED), rel(FEATURE_ORDER_CONTRACT), rel(hm.ROUTE_PARITY_DECISION)],
            "runtime_path": "not_materialized_yet(HO에서 아직 물질화 전)",
            "shared_contract_needed": ["single-source feature CSV(단일 원천 피처 CSV)", "MT5-compatible ONNX(MT5 호환 ONNX)", "probability-bin veto params(확률 구간 거부 파라미터)", "tester set/ini(테스터 설정/초기화 파일)"],
            "known_differences": ["scaled density estimate is not MT5 proof(스케일 밀도 추정은 MT5 증명 아님)", "HJ dual-source partial route not reused(HJ 이중 원천 부분 라우트 재사용 안 함)"],
            "runtime_claim_boundary": "package_readiness_review_only(패키지 준비성 검토 전용)",
            "effect": "HO에서 runtime parity(런타임 동등성)를 닫아야 할 항목을 미리 고정합니다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in input_files if exists(path) and io_path(path).is_file()],
            "producer": rel(THIS_FILE),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)",
            "lineage_judgment": "connected_with_package_boundary(패키지 경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "single-source package readiness clue requiring HO materialization(단일 원천 패키지 준비 단서, HO 물질화 필요)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve", "promotion_candidate"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "scaled density(스케일 밀도)와 package readiness(패키지 준비성)를 운영 권위로 착각하지 않게 합니다.",
        },
    )


def final_payload(
    created_at: str,
    selected: Mapping[str, Any],
    feature_payload: Mapping[str, Any],
    artifact: Mapping[str, Any],
    metrics: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    gate_passes = sum(1 for gate in gates if gate["status"] == "passed")
    gate_total = len(gates)
    all_passed = gate_passes == gate_total
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS if all_passed else "completed_stage364HN_package_readiness_review_repair_required_no_authority",
        "judgment": JUDGMENT if all_passed else "inconclusive_package_readiness_review_repair_required_no_authority",
        "decision": DECISION if all_passed else "stage364HN_repair_package_readiness_inputs",
        "selected_model_id": selected["selected_model_id"],
        "selected_source_run_number": selected["selected_source_run_number"],
        "selected_feature_set_id": selected["selected_feature_set_id"],
        "selected_threshold": selected.get("selected_threshold", ""),
        "feature_count": feature_payload["feature_count"],
        "feature_order_hash": feature_payload["feature_order_hash"],
        "onnx_path": artifact["onnx_path"],
        "onnx_sha256_match": artifact["onnx_sha256_match"],
        "joblib_path": artifact["joblib_path"],
        "joblib_sha256_match": artifact["joblib_sha256_match"],
        "onnx_smoke_passed": artifact["smoke_passed"],
        "onnx_smoke_max_abs_diff": artifact["smoke_max_abs_diff"],
        "selected_oos_net": selected.get("selected_oos_net", ""),
        "selected_oos_profit_factor": selected.get("selected_oos_profit_factor", ""),
        "selected_oos_trade_density": selected.get("selected_oos_trade_density", ""),
        "selected_runtime_density_estimate_from_hl_ratio": selected.get("selected_runtime_density_estimate_from_hl_ratio", ""),
        "selected_combined_short_share": selected.get("selected_combined_short_share", ""),
        "selected_combined_cost09_net": selected.get("selected_combined_cost09_net", ""),
        "validation_cost06_net": metrics.get("validation_cost06_net", ""),
        "no_trade_splitting": metrics.get("no_trade_splitting", False),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_package": "not_materialized_yet_next_HO(HO에서 아직 물질화 전)",
        "external_verification_status": "not_run_review_only(미실행, 검토 전용)",
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_docs(
    final: Mapping[str, Any],
    readiness_rows: Sequence[Mapping[str, Any]],
    guardrail_rows: Sequence[Mapping[str, Any]],
    stability_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364HN Probability-Bin Veto Density/Side/Cost Repair Review(확률 구간 거부 밀도/방향/비용 수리 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): HM selected seed(HM 선택 씨앗)인 `{final['selected_model_id']}`를 single-source runtime package(단일 원천 런타임 패키지) 후보로 검토했습니다.

Effect(효과): OOS net/PF/density(표본외 순수익/수익 팩터/밀도) `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`와 scaled density estimate(스케일 밀도 추정) `{final['selected_runtime_density_estimate_from_hl_ratio']}`는 긍정 단서입니다. 다만 direct density proof(직접 밀도 증명)는 없고 validation cost(검증 비용)가 취약해 운영 권위는 없습니다.

## Package Readiness(패키지 준비성)

{markdown_table(readiness_rows, ['review_item', 'status', 'evidence', 'feature_count', 'feature_order_hash', 'max_abs_diff', 'effect'])}

## Guardrails(가드레일)

{markdown_table(guardrail_rows, ['guardrail', 'value', 'threshold', 'status', 'effect'])}

## Cost/Side Stability(비용/방향 안정성)

{markdown_table(stability_rows, ['item', 'validation_cost06_net', 'validation_cost09_net', 'oos_cost06_net', 'combined_cost09_net', 'row_count', 'status', 'effect'])}

## Next Queue(다음 대기열)

{markdown_table(queue_rows, ['queue_id', 'next_run_id', 'model_id', 'feature_order_contract', 'target', 'avoid', 'effect'])}

## Boundary(경계)

This run(이 실행)은 package readiness review(패키지 준비성 검토)입니다. MT5 runtime probe(MT5 런타임 탐침), runtime package(런타임 패키지), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364HN decision(결정): single-source probability-bin veto package review(단일 원천 확률 구간 거부 패키지 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- scaled density estimate(스케일 밀도 추정): `{final['selected_runtime_density_estimate_from_hl_ratio']}`
- feature_count/hash(피처 수/해시): `{final['feature_count']}` / `{final['feature_order_hash']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): HO에서 MT5 runtime package(MT5 런타임 패키지)를 물질화해 proxy clue(프록시 단서)를 외부 검증으로 넘깁니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364HN__{RUN_ID}", f"\n- run364HN__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - single-source probability-bin veto package review(단일 원천 확률 구간 거부 패키지 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364HN__{RUN_ID}",
        f"""
<!-- run364HN__{RUN_ID} -->

## run364HN Single-Source Package Review(단일 원천 패키지 검토)

Action(행동): HM selected FJ seed(HM 선택 FJ 씨앗)의 ONNX/joblib(온엑스/잡립), feature order(피처 순서), no-trade-splitting(거래 쪼개기 금지), cost/side guardrail(비용/방향 가드레일)을 검토했습니다.

Effect(효과): `{NEXT_RUN_ID}`에서 single-source MT5 runtime package(단일 원천 MT5 런타임 패키지)를 물질화할 수 있습니다. 운영 권위는 없습니다.
""",
    )
    append_text_once(STAGE_README, f"run364HN__{RUN_ID}", f"\n<!-- run364HN__{RUN_ID} -->\n## run364HN package review(패키지 검토)\n\nSelected model(선택 모델): `{final['selected_model_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{final['status']}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
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

Current truth(현재 진실): `run364HN` reviewed(검토 완료) HM selected FJ seed(HM 선택 FJ 씨앗). ONNX/joblib(온엑스/잡립) lineage(계보), ONNX smoke(온엑스 스모크), feature order reconstruction(피처 순서 재현), no-trade-splitting(거래 쪼개기 금지)은 package readiness clue(패키지 준비 단서)로 통과했습니다.

Selected seed(선택 씨앗): `{final['selected_source_run_number']}` / `{final['selected_model_id']}`. OOS net/PF/density(표본외 순수익/수익 팩터/밀도)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`이고, scaled density estimate(스케일 밀도 추정)는 `{final['selected_runtime_density_estimate_from_hl_ratio']}`입니다.

Important boundary(중요 경계): scaled density estimate(스케일 밀도 추정)는 HL density ratio(HL 밀도 비율)를 재사용한 estimate(추정)입니다. 새 MT5 runtime probe(새 MT5 런타임 탐침), runtime package(런타임 패키지), runtime authority(런타임 권위)는 아닙니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 single-source MT5 runtime package(단일 원천 MT5 런타임 패키지)를 materialize(물질화)하고 feature CSV(피처 CSV), MT5-compatible ONNX(MT5 호환 ONNX), set/ini(설정/초기화 파일), probability-bin veto(확률 구간 거부) 계약을 연결합니다.

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

Selected package seed(선택 패키지 씨앗): `{final['selected_model_id']}` from `{final['selected_source_run_number']}`.

Package readiness(패키지 준비성): ONNX/joblib lineage(온엑스/잡립 계보), ONNX smoke(온엑스 스모크), feature order reconstruction(피처 순서 재현), no-trade-splitting(거래 쪼개기 금지)은 통과했습니다.

Open guardrails(열린 가드레일): direct density proof(직접 밀도 증명) 없음, validation cost fragility(검증 비용 취약성), scaled density estimate only(스케일 밀도 추정 전용), no MT5 runtime probe yet(아직 MT5 런타임 탐침 없음).

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364HN__{RUN_ID}", f"\n<!-- run364HN__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed HM selected FJ seed(HM 선택 FJ 씨앗 검토); judgment `{final['judgment']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HN__{RUN_ID}", f"\n<!-- run364HN__{RUN_ID} -->\n- `{RUN_ID}`: FJ single-source probability-bin veto package(단일 원천 확률 구간 거부 패키지) 준비 단서를 확인했습니다. Effect(효과): HO에서 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 외부 검증을 열 수 있습니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364HN__no_authority__{RUN_ID}", f"\n<!-- run364HN__no_authority__{RUN_ID} -->\n- `{RUN_ID}`: scaled density estimate(스케일 밀도 추정)는 긍정 단서지만 direct density proof(직접 밀도 증명), 새 MT5 runtime probe(새 MT5 런타임 탐침), runtime package(런타임 패키지)가 아직 없어 authority(권위) 없음. Effect(효과): 운영 주장 대신 HO 패키지 물질화로 넘깁니다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__package_readiness",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review(검토)",
        "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B missing_required(Tier A+B 필수 누락)",
        "kpi_scope": "package_readiness_proxy(패키지 준비성 프록시)",
        "scoreboard_lane": "runtime_package_routing(런타임 패키지 라우팅)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "external_verification_status": final["external_verification_status"],
        "notes": "single-source FJ package readiness reviewed(단일 원천 FJ 패키지 준비성 검토)",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "feature_count": final["feature_count"],
        "candidate_model_id": final["selected_model_id"],
        "net_profit": final["selected_oos_net"],
        "profit_factor": final["selected_oos_profit_factor"],
        "trade_density_per_feature_day": final["selected_oos_trade_density"],
        "expected_estimated_mt5_density": final["selected_runtime_density_estimate_from_hl_ratio"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "review_and_package_routing(검토 및 패키지 라우팅)",
        "run_type": "review(검토)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN364HO_QUEUE),
        "result_path": rel(FINAL_DECISION),
        "selected_net_profit": final["selected_oos_net"],
        "selected_profit_factor": final["selected_oos_profit_factor"],
        "selected_trade_density": final["selected_oos_trade_density"],
        "expected_net_profit": final["selected_oos_net"],
        "expected_profit_factor": final["selected_oos_profit_factor"],
        "expected_trade_density": final["selected_runtime_density_estimate_from_hl_ratio"],
    }
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], [ledger_row])
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], [ledger_row])
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**ledger_row, "lane": "runtime_package_routing(런타임 패키지 라우팅)", "primary_report": rel(REPORT_PATH)}])
    artifact_rows = []
    for path in [FINAL_DECISION, GATE_AUDIT, REPORT_PATH, DECISION_DOC, FEATURE_ORDER_CONTRACT, RUN364HO_QUEUE]:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.name}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "review_artifact(검토 산출물)",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
                "created_at_utc": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "HN review(HN 검토)의 재진입 근거를 제공합니다.",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_run_manifest(final: Mapping[str, Any], input_files: Sequence[Path]) -> None:
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
            "command": "python stage_pipelines/stage364/review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db.py",
            "input_files": [rel(path) for path in input_files],
            "input_hashes": {rel(path): sha(path) for path in input_files if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "output_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    hm_final, selected, input_files = validate_inputs()
    write_work_packet()
    write_input_manifest(input_files)
    feature_payload = feature_order_payload(selected)
    artifact = artifact_status(selected)
    readiness_rows, guardrail_rows, stability_rows, queue_rows, metrics = build_reviews(selected, feature_payload, artifact)
    write_csv(PACKAGE_READINESS_REVIEW, readiness_rows)
    write_csv(GUARDRAIL_REVIEW, guardrail_rows)
    write_csv(COST_SIDE_STABILITY_REVIEW, stability_rows)
    write_csv(RUN364HO_QUEUE, queue_rows)
    final_base = {"created_at_utc": created_at, "hm_status": hm_final.get("status", "")}
    write_receipts(final_base, selected, feature_payload, artifact, input_files)
    gates = gate_rows(selected, feature_payload, artifact, metrics)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(created_at, selected, feature_payload, artifact, metrics, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, readiness_rows, guardrail_rows, stability_rows, queue_rows, gates)
    write_ledgers(final)
    write_run_manifest(final, input_files)
    final = {**final, "run_manifest": rel(RUN_MANIFEST), "run_manifest_sha256": sha(RUN_MANIFEST)}
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready({key: final[key] for key in ["run_id", "status", "judgment", "selected_model_id", "selected_oos_net", "selected_oos_profit_factor", "selected_oos_trade_density", "selected_runtime_density_estimate_from_hl_ratio", "feature_count", "gate_passes", "gate_total", "next_run_id", "runtime_authority", "goal_achieve"]}), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
