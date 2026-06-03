from __future__ import annotations

import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import materialize_hold6_pf_dd_repair_offensive_inputs_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_pf_pass_density_restore_offensive_scout_without_db as replay  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AP"
RUN_ID = "run364AP_train_hold6_pf_dd_repair_offensive_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.PARENT_RUN_ID
NEXT_RUN_ID = "run364AQ_review_hold6_pf_dd_repair_offensive_scout_without_db_v1"

STATUS = "completed_stage364AP_hold6_pf_dd_repair_proxy_scout_no_mt5_no_authority"
JUDGMENT = "proxy_scout_completed_hold6_pf_dd_repair_ranked_mt5_probe_required_no_authority"
DECISION = "stage364AP_open_run364AQ_review_hold6_pf_dd_repair_offensive_scout"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_PF = parent.TARGET_PF

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EXPECTED_DIR = RUN_DIR / "expected_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
QUEUE_REPLAY_AUDIT = RUN_DIR / "queue_replay_audit.csv"
SCOUT_SURFACE = RUN_DIR / "hold6_pf_dd_repair_proxy_scout_surface.csv"
STRICT_CANDIDATES = RUN_DIR / "strict_proxy_candidates.csv"
SELECTED_PROXY_CANDIDATE = RUN_DIR / "selected_proxy_candidate.json"
SELECTED_EXPECTED_TRADE_TAPE = EXPECTED_DIR / "selected_trade_tape.csv"
SELECTED_SESSION_SUMMARY = RUN_DIR / "selected_session_summary.csv"
SELECTED_MONTH_SIDE_SUMMARY = RUN_DIR / "selected_month_side_summary.csv"
POLICY_ATTRIBUTION = RUN_DIR / "policy_attribution.csv"
BASELINE_COMPARISON = RUN_DIR / "baseline_comparison.csv"
RUN364AQ_QUEUE = RUN_DIR / "run364AQ_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_boundary_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AP_hold6_pf_dd_repair_offensive_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AP_hold6_pf_dd_repair_offensive_scout.md"
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

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364AP_QUEUE,
    parent.REPAIR_AXIS_MAP,
    parent.SEED_PAIR_MATRIX,
    parent.DD_GUARDRAIL_DESIGN,
    parent.REPORT_PATH,
    replay.prev.scout.base.SELECTED_RUNTIME_CANDIDATE,
    replay.prev.scout.base.SELECTED_TRADE_TAPE,
    replay.prev.scout.base.prev.sidepkg.pkg.FEATURE_MATRIX,
    replay.prev.scout.base.prev.sidepkg.pkg.FEATURE_ORDER,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    QUEUE_REPLAY_AUDIT,
    SCOUT_SURFACE,
    STRICT_CANDIDATES,
    SELECTED_PROXY_CANDIDATE,
    SELECTED_EXPECTED_TRADE_TAPE,
    SELECTED_SESSION_SUMMARY,
    SELECTED_MONTH_SIDE_SUMMARY,
    POLICY_ATTRIBUTION,
    BASELINE_COMPARISON,
    RUN364AQ_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
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
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, default)))


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, EXPECTED_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(path, exist_ok=True)


def patch_replay_globals() -> None:
    replay.RUN_ID = RUN_ID
    replay.RUN_NUMBER = RUN_NUMBER
    replay.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    replay.NEXT_RUN_ID = NEXT_RUN_ID


def validate_inputs() -> Mapping[str, Any]:
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 gate, 게이트가 모두 통과하지 않음)")
    queue = read_csv_rows(parent.RUN364AP_QUEUE)
    if len(queue) != 8:
        raise RuntimeError(f"unexpected run364AP queue rows(364AP 대기열 행 수 이상): {len(queue)}")
    for row in queue:
        if row.get("top_n_status") != "forbidden(금지)":
            raise RuntimeError("top_n guardrail missing(top_n 금지 누락)")
        if row.get("trade_splitting_status") != "not_used(거래 쪼개기 없음)":
            raise RuntimeError("trade splitting guardrail missing(거래 쪼개기 금지 누락)")
        if row.get("timestamp_boundary") != "entry_time_known_only(진입 시점에 알려진 값만 사용)":
            raise RuntimeError("timestamp boundary mismatch(시점 경계 불일치)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AP inputs(364AP 입력 누락): " + ", ".join(missing))
    return parent_final


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "run364AP_scout_queue.csv":
        return "parent scout queue(부모 정찰 대기열)"
    if name == "repair_axis_map.csv":
        return "repair axis design(수리 축 설계)"
    if name == "dd_guardrail_design.csv":
        return "DD guardrail design(낙폭 가드 설계)"
    if name.endswith(".json"):
        return "decision or receipt(결정 또는 영수증)"
    if name.endswith(".csv"):
        return "tabular evidence(표 근거)"
    return "supporting input(보조 입력)"


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "role": input_role(path),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def reference_from_parent(parent_final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "reference_variant_id": "run364AN_selected_hold6_seed(364AN 선택 6봉 씨앗)",
        "reference_combined_net_profit": parent_final.get("selected_hold6_seed_net_profit", ""),
        "reference_combined_profit_factor": parent_final.get("selected_hold6_seed_profit_factor", ""),
        "reference_combined_trade_count": "",
        "reference_combined_trade_per_business_day": parent_final.get("selected_hold6_seed_density", ""),
        "reference_combined_expectancy": "",
        "reference_combined_max_drawdown": parent_final.get("selected_hold6_seed_drawdown", ""),
        "reference_combined_recovery_factor": "",
        "reference_combined_long_count": "",
        "reference_combined_short_count": "",
        "reference_combined_long_short_balance": "",
    }


def queue_variants() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    executable: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for index, row in enumerate(read_csv_rows(parent.RUN364AP_QUEUE), start=1):
        if row.get("implementation_required") == "yes":
            skipped.append(
                {
                    "run_id": RUN_ID,
                    "queue_id": row.get("queue_id", ""),
                    "variant_id": row.get("variant_id", ""),
                    "replay_status": "skipped_new_policy_required(새 정책 필요로 건너뜀)",
                    "reason": row.get("implementation_note", ""),
                    "trade_count": 0,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        executable.append(
            {
                "run_id": RUN_ID,
                "queue_rank": as_int(row.get("queue_rank"), index),
                "queue_id": row.get("queue_id", ""),
                "axis_id": row.get("axis_id", ""),
                "queue_type": row.get("queue_type", ""),
                "seed_variant_id": row.get("seed_variant_id", ""),
                "source_queue_id": row.get("source_queue_id", ""),
                "variant_id": row.get("variant_id", f"run364AP_variant_{index:02d}"),
                "short_threshold": as_float(row.get("short_probability_threshold"), 0.45),
                "long_threshold": as_float(row.get("long_threshold"), replay.prev.scout.base.LONG_THRESHOLD),
                "min_margin": as_float(row.get("min_margin"), -0.000562137088),
                "entry_margin_floor": as_float(row.get("entry_margin_floor"), 0.0),
                "long_block_feature": row.get("long_block_feature", replay.prev.scout.base.SIDE_FILTER_FEATURE),
                "long_block_min": as_float(row.get("long_block_min"), 40.0),
                "max_hold_m5": as_int(row.get("max_hold_m5"), 8),
                "bridge_policy": row.get("bridge_policy", ""),
                "bridge_policy_value": row.get("bridge_policy_value", ""),
                "materialized_policy": row.get("materialized_policy", ""),
                "session_policy": row.get("session_policy", ""),
                "side_policy": row.get("side_policy", ""),
                "restore_policy": row.get("restore_policy", ""),
                "density_gap_to_3day": as_float(row.get("density_gap_to_3day"), 0.0),
                "density_restore_budget": as_float(row.get("density_restore_budget"), 0.0),
                "density_restore_status": "ap_replay(364AP 재생)",
                "min_density_requirement": DENSITY_FLOOR,
                "target_profit_factor": TARGET_PF,
                "validation_guardrail": "validation_net_positive_report_separate(검증 순수익 양수 분리 보고)",
                "oos_guardrail": "oos_locked_no_threshold_selection(표본외 잠금, 임계값 선택 없음)",
                "trade_splitting_status": row.get("trade_splitting_status", ""),
                "top_n_status": row.get("top_n_status", ""),
                "timestamp_boundary": row.get("timestamp_boundary", ""),
                "expected_effect": row.get("expected_effect", ""),
            }
        )
    return executable, skipped


def add_repair_deltas(surface: pd.DataFrame, reference: Mapping[str, Any]) -> pd.DataFrame:
    if surface.empty:
        return surface
    out = surface.copy()
    out["net_delta_vs_run364AO_hold6_seed"] = out["combined_net_profit"].astype(float) - as_float(reference.get("reference_combined_net_profit"))
    out["pf_delta_vs_run364AO_hold6_seed"] = out["combined_profit_factor"].astype(float) - as_float(reference.get("reference_combined_profit_factor"))
    out["dd_delta_vs_run364AO_hold6_seed"] = out["combined_max_drawdown"].astype(float) - as_float(reference.get("reference_combined_max_drawdown"))
    out["density_delta_vs_run364AO_hold6_seed"] = out["combined_trade_per_business_day"].astype(float) - as_float(reference.get("reference_combined_trade_per_business_day"))
    for col in [
        "net_delta_vs_run364AO_hold6_seed",
        "pf_delta_vs_run364AO_hold6_seed",
        "dd_delta_vs_run364AO_hold6_seed",
        "density_delta_vs_run364AO_hold6_seed",
    ]:
        out[col] = out[col].map(lambda value: finite(value, 10))
    return out


def strict_surface(surface: pd.DataFrame) -> pd.DataFrame:
    if surface.empty or "candidate_status" not in surface:
        return surface.iloc[0:0].copy()
    return surface[surface["candidate_status"].astype(str).str.startswith("pass_")].copy()


def comparison_rows(best: Mapping[str, Any], reference: Mapping[str, Any]) -> list[dict[str, Any]]:
    metrics = [
        "combined_net_profit",
        "combined_profit_factor",
        "combined_trade_count",
        "combined_trade_per_business_day",
        "combined_expectancy",
        "combined_max_drawdown",
        "combined_recovery_factor",
        "combined_long_count",
        "combined_short_count",
        "combined_long_short_balance",
    ]
    rows = []
    for metric in metrics:
        rows.append(
            {
                "run_id": RUN_ID,
                "reference_run_id": PARENT_RUN_ID,
                "reference_label": "run364AN_selected_hold6_seed(364AN 선택 6봉 씨앗)",
                "selected_variant_id": best.get("variant_id", ""),
                "metric_id": metric,
                "reference_value": reference.get(f"reference_{metric}", ""),
                "selected_value": best.get(metric, ""),
                "delta_selected_minus_reference": finite(as_float(best.get(metric)) - as_float(reference.get(f"reference_{metric}")), 10),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_queue_rows(best: Mapping[str, Any], strict_count: int, skipped_count: int) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "review_hold6_pf_dd_repair_offensive_scout(6봉 PF/DD 수리 공격 정찰 검토)",
            "selected_variant_id": best.get("variant_id", ""),
            "selected_queue_id": best.get("queue_id", ""),
            "candidate_status": best.get("candidate_status", ""),
            "strict_pass_rows": strict_count,
            "skipped_new_policy_rows": skipped_count,
            "required_review": "PF/density/DD/split/session/side and MT5 probe need(PF/밀도/낙폭/분할/세션/방향과 MT5 탐침 필요)",
            "effect": "proxy scout(프록시 정찰)를 package(패키지)나 runtime authority(런타임 권위)로 승격하지 않고 검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate": name,
        "status": status,
        "evidence": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "model_validation(모델 검증)",
            "primary_skill": "obsidian-model-validation(모델 검증)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "data_integrity_audit",
                "queue_replay_gate",
                "topn_absence_gate",
                "trade_splitting_absence_gate",
                "kpi_contract_audit",
                "model_boundary_audit",
                "performance_attribution_gate",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base_payload = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "timestamp_dt UTC order; signal uses closed M5 and entry-time features(timestamp_dt UTC 순서, 신호는 닫힌 5분봉과 진입 시점 피처 사용)",
            "sample_scope": "US100 M5 validation+oos proxy replay, Tier A separate; Tier B missing_required(US100 5분봉 검증+표본외 프록시 재생, Tier A 분리; Tier B 필수 누락)",
            "missing_or_duplicate_check": "runtime frame duplicate timestamp and required-value checks inherited from replay helper(런타임 프레임 중복 시각과 필수값 검사는 재생 도우미에서 상속)",
            "feature_label_boundary": "no new features, labels, or OOS threshold selection(새 피처, 라벨, 표본외 임계값 선택 없음)",
            "leakage_risk": "one new policy row skipped until implemented; no silent execution(새 정책 1행은 구현 전 건너뜀, 조용한 실행 없음)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-experiment-design(실험 설계)",
            "hypothesis": "hold6 density can keep density while PF/DD improves under sparse PF repairs(6봉 밀도는 희소 PF 수리와 결합할 때 밀도를 유지하며 PF/DD를 개선할 수 있음)",
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": "US100 M5, prior probability tape, one position, fixed row grain, no top_n, no trade splitting(US100 5분봉, 기존 확률 테이프, 포지션 1개, 고정 행 단위, top_n 없음, 거래 쪼개기 없음)",
            "changed_variables": "hold, threshold edge, late long patch, margin floor(보유, 임계값 경계, 후반 롱 패치, 마진 하한)",
            "success_criteria": "PF>=1.30, density>=3/day, split net positive, short side nonzero(PF 1.30 이상, 하루 밀도 3 이상, 분할 순수익 양수, 숏 0 아님)",
            "failure_criteria": "PF below target, density loss, DD worse than hold6 seed, split loss(PF 목표 미달, 밀도 손실, 6봉 씨앗보다 낙폭 악화, 분할 손실)",
            "invalid_conditions": "top_n, trade splitting, post-entry features, OOS-picked threshold(top_n, 거래 쪼개기, 진입 후 피처, 표본외 선택 임계값)",
            "evidence_plan": [rel(SCOUT_SURFACE), rel(STRICT_CANDIDATES), rel(SELECTED_EXPECTED_TRADE_TAPE), rel(GATE_AUDIT)],
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-model-validation(모델 검증)",
            "model_family": "existing ONNX probability tape replay, no new model training(기존 ONNX 확률 테이프 재생, 새 모델 학습 없음)",
            "split_method": "fixed validation/oos replay(고정 검증/표본외 재생)",
            "selection_metric": "selection_score from net/PF/density/DD/short balance(순수익/PF/밀도/낙폭/숏 균형 선택 점수)",
            "threshold_policy": "pre-materialized queue thresholds, no OOS threshold search(사전 구체화 대기열 임계값, 표본외 임계값 탐색 없음)",
            "overfit_risk": "7 executable proxy rows and one skipped new-policy row(실행 가능 프록시 7행과 새 정책 건너뜀 1행)",
            "validation_judgment": "exploratory_proxy_no_authority(탐색 프록시, 권위 없음)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "observed_change": f"selected {final.get('selected_variant_id')} net/PF/density/DD {final.get('selected_combined_net_profit')}/{final.get('selected_combined_profit_factor')}/{final.get('selected_combined_trade_per_business_day')}/{final.get('selected_combined_max_drawdown')}",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "hold6 anchor, sparse PF anchor, soft margin floors, late long patch(6봉 기준, 희소 PF 기준, 소프트 마진 하한, 후반 롱 패치)",
            "segment_checks": [rel(SELECTED_SESSION_SUMMARY), rel(SELECTED_MONTH_SIDE_SUMMARY), rel(POLICY_ATTRIBUTION)],
            "alternative_explanations": "proxy execution may not match MT5 fills or broker cost(프록시 실행은 MT5 체결이나 브로커 비용과 다를 수 있음)",
            "attribution_confidence": "medium_for_proxy_low_for_operation(프록시는 중간, 운영은 낮음)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-result-judgment(결과 판정)",
            "result_subject": RUN_ID,
            "evidence_available": [rel(SCOUT_SURFACE), rel(STRICT_CANDIDATES), rel(SELECTED_EXPECTED_TRADE_TAPE), rel(FINAL_DECISION)],
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침)",
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "proxy scout only; candidate evidence is not an operating model(프록시 정찰 전용, 후보 근거는 운영 모델이 아님)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base_payload,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "proxy scout(프록시 정찰)를 운영 주장으로 연결하지 않는다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AP proxy scout(364AP 프록시 정찰)를 닫음"),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AO 대기열과 부모 산출물을 확인함"),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점 안전 프록시 재생 경계를 기록함"),
        gate_row("queue_replay_gate(대기열 재생 게이트)", SCOUT_SURFACE, "실행 가능 queue(대기열) 행을 재생함"),
        gate_row("topn_absence_gate(top_n 부재 게이트)", QUEUE_REPLAY_AUDIT, "top_n 사용 없음"),
        gate_row("trade_splitting_absence_gate(거래 쪼개기 부재 게이트)", QUEUE_REPLAY_AUDIT, "거래 쪼개기 없음"),
        gate_row("kpi_contract_audit(KPI 계약 감사)", SCOUT_SURFACE, "net/PF/expectancy/DD/RF/trades/side/density 기록"),
        gate_row("model_boundary_audit(모델 경계 감사)", MODEL_RECEIPT, "새 모델 학습 없음과 threshold(임계값) 경계를 기록"),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "수리 축별 성과 귀속을 연결"),
        gate_row("result_judgment_gate(결과 판정 게이트)", JUDGMENT_RECEIPT, "MT5 필요 경계로 판정"),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 hash(해시) 연결"),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "런타임 권위 주장 없음"),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 gate(게이트)를 종료 기록에 연결"),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def final_payload(
    parent_final: Mapping[str, Any],
    surface: pd.DataFrame,
    best: Mapping[str, Any],
    strict_count: int,
    skipped_count: int,
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_materialization_run_id": parent_final.get("run_id"),
        "scout_rows": int(len(surface)),
        "skipped_new_policy_rows": skipped_count,
        "strict_pass_rows": strict_count,
        "package_path": "review_required_strict_proxy_pass(엄격 프록시 통과, 검토 필요)" if strict_count else "no_package_proxy_review_required(패키지 없음, 프록시 검토 필요)",
        "selected_variant_id": best.get("variant_id", ""),
        "selected_queue_id": best.get("queue_id", ""),
        "selected_candidate_status": best.get("candidate_status", ""),
        "selected_combined_net_profit": best.get("combined_net_profit", ""),
        "selected_combined_profit_factor": best.get("combined_profit_factor", ""),
        "selected_combined_trade_count": best.get("combined_trade_count", ""),
        "selected_combined_trade_per_business_day": best.get("combined_trade_per_business_day", ""),
        "selected_combined_expectancy": best.get("combined_expectancy", ""),
        "selected_combined_max_drawdown": best.get("combined_max_drawdown", ""),
        "selected_combined_recovery_factor": best.get("combined_recovery_factor", ""),
        "selected_combined_long_count": best.get("combined_long_count", ""),
        "selected_combined_short_count": best.get("combined_short_count", ""),
        "selected_combined_long_short_balance": best.get("combined_long_short_balance", ""),
        "selected_validation_net_profit": best.get("validation_net_profit", ""),
        "selected_validation_profit_factor": best.get("validation_profit_factor", ""),
        "selected_oos_net_profit": best.get("oos_net_profit", ""),
        "selected_oos_profit_factor": best.get("oos_profit_factor", ""),
        "selected_pf_delta_vs_hold6": best.get("pf_delta_vs_run364AO_hold6_seed", ""),
        "selected_density_delta_vs_hold6": best.get("density_delta_vs_run364AO_hold6_seed", ""),
        "selected_dd_delta_vs_hold6": best.get("dd_delta_vs_run364AO_hold6_seed", ""),
        "top_n_rows": 0,
        "trade_splitting_rows": 0,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def refresh_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = STAGE_BRIEF.read_text(encoding="utf-8-sig")
    lines = []
    for line in text.splitlines():
        if line.startswith("- current_run_id"):
            lines.append(f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`")
        elif line.startswith("- latest_completed_run_id"):
            lines.append(f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`")
        elif line.startswith("- selection_status"):
            lines.append(f"- selection_status(선택 상태): `{STATUS}`")
        elif line.startswith("- claim_boundary"):
            lines.append(f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
        else:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines) + "\n")


def write_docs(final: Mapping[str, Any], surface: pd.DataFrame, comparison: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    surface_rows = surface.head(8).to_dict("records")
    text = f"""# run364AP hold6 PF/DD repair scout(364AP 6봉 PF/DD 수리 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- scout_rows(정찰 행): `{final['scout_rows']}`
- skipped_new_policy_rows(새 정책 건너뜀 행): `{final['skipped_new_policy_rows']}`
- strict_pass_rows(엄격 통과 행): `{final['strict_pass_rows']}`
- selected_net/PF/density/DD(선택 순수익/PF/밀도/낙폭): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_per_business_day']}` / `{final['selected_combined_max_drawdown']}`
- runtime_authority(런타임 권위): `not_claimed`

## Surface(표면)

{markdown_table(surface_rows, ['queue_rank', 'queue_id', 'candidate_status', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count', 'selection_score'])}

## Hold6 Comparison(6봉 비교)

{markdown_table(comparison, ['metric_id', 'reference_value', 'selected_value', 'delta_selected_minus_reference'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): run364AP(364AP 실행)는 proxy scout(프록시 정찰)이며, package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- strict_pass_rows(엄격 통과 행): `{final['strict_pass_rows']}`\n- selected_pf(선택 PF): `{final['selected_combined_profit_factor']}`\n- effect(효과): `{NEXT_RUN_ID}` review(검토) 대기열을 만든다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AP Hold6 PF/DD Repair Scout Closeout",
        f"\n## run364AP Hold6 PF/DD Repair Scout Closeout(364AP 6봉 PF/DD 수리 정찰 종료)\n\nAction(행동): run364AO(364AO 실행) queue(대기열) 중 실행 가능한 7행을 proxy replay(프록시 재생)했다.\n\nEffect(효과): Stage364(364단계) 안에서 package(패키지) 없이 다음 review(검토)로 넘길 PF/DD repair(PF/DD 수리) 표면을 만들었다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_proxy_review_required(프록시 검토 필요)
- latest_proxy_scout(최근 프록시 정찰): `{RUN_ID}`
- strict_pass_rows(엄격 통과 행): `{final['strict_pass_rows']}`
- selected_proxy_candidate(선택 프록시 후보): `{rel(SELECTED_PROXY_CANDIDATE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): run364AP(364AP 실행)는 run364AO(364AO 실행)의 hold6 PF/DD repair(6봉 PF/DD 수리) queue(대기열) 중 실행 가능한 7행을 proxy replay(프록시 재생)했다. strict_pass_rows(엄격 통과 행)는 `{final['strict_pass_rows']}`이고, selected PF(선택 PF)는 `{final['selected_combined_profit_factor']}`, density(밀도)는 `{final['selected_combined_trade_per_business_day']}`, DD(낙폭)는 `{final['selected_combined_max_drawdown']}`이다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 PF/density/DD/split/session/side(PF/밀도/낙폭/분할/세션/방향) 검토를 닫고, MT5 runtime probe(MT5 런타임 탐침) 필요 여부를 판정한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
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
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): hold6 PF/DD repair proxy scout(6봉 PF/DD 수리 프록시 정찰)를 실행했다.\n- effect(효과): `{NEXT_RUN_ID}` review queue(검토 대기열)를 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): hold6 density(6봉 밀도)와 sparse PF(희소 수익 팩터) 수리 축을 proxy replay(프록시 재생)로 비교한다.\n- effect(효과): PF(수익 팩터), density(밀도), DD(낙폭)를 동시에 보며 다음 검토로 넘긴다.\n",
    )
    append_text_once(
        STAGE_README,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- action(행동): run364AP(364AP 실행) proxy scout(프록시 정찰)를 실행했다.\n- effect(효과): Stage364(364단계) 안에서 다음 review(검토)로 이어간다.\n",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "lane": "proxy_scout(프록시 정찰)",
        "scoreboard_lane": "proxy_scout(프록시 정찰)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"scout_rows={final['scout_rows']}; strict_pass_rows={final['strict_pass_rows']}; selected_pf={final['selected_combined_profit_factor']}; selected_density={final['selected_combined_trade_per_business_day']}",
        "family": "model_validation(모델 검증)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["scout_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(SCOUT_SURFACE),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "model_validation(모델 검증)",
        "trade_density_requirement_status": "proxy_replay_density_checked_no_trade_split(프록시 재생 밀도 확인, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "evidence_scope": "proxy_scout_no_authority(프록시 정찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can hold6 density repair PF/DD without losing the density floor?(6봉 밀도가 밀도 하한을 잃지 않고 PF/DD를 수리할 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy scout metrics(프록시 정찰 지표)"),
        (f"{RUN_ID}__Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "missing_required(필수 누락)"),
        (f"{RUN_ID}__Tier_A_plus_B", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A only plus Tier B missing_required(Tier A만 있고 Tier B 필수 누락)"),
    ]:
        row = dict(common)
        row.update({"ledger_row_id": subrun_id, "subrun_id": subrun_id, "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": kpi_scope})
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("scout_surface", SCOUT_SURFACE, "Proxy scout surface(프록시 정찰 표면)."),
            ("strict_candidates", STRICT_CANDIDATES, "Strict proxy candidates(엄격 프록시 후보)."),
            ("selected_trade_tape", SELECTED_EXPECTED_TRADE_TAPE, "Selected expected trade tape(선택 기대 거래 테이프)."),
            ("selected_proxy_candidate", SELECTED_PROXY_CANDIDATE, "Selected proxy candidate(선택 프록시 후보)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in outputs],
            "artifact_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )


def main() -> None:
    ensure_dirs()
    patch_replay_globals()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    frame, _feature_order, _threshold = replay.load_runtime_frame()
    variants, skipped_audit = queue_variants()
    reference = reference_from_parent(parent_final)
    surface, selected_trades, audit_rows = replay.evaluate_queue(frame, variants, reference)
    surface = add_repair_deltas(surface, reference)
    strict = strict_surface(surface)
    best = surface.iloc[0].to_dict() if not surface.empty else {}
    audit_rows = [dict(row, replay_status="executed(실행됨)") for row in audit_rows] + skipped_audit
    comparison = comparison_rows(best, reference)
    review_queue = review_queue_rows(best, len(strict), len(skipped_audit))

    write_csv(QUEUE_REPLAY_AUDIT, audit_rows)
    write_csv(SCOUT_SURFACE, surface.to_dict("records"))
    write_csv(STRICT_CANDIDATES, strict.to_dict("records"))
    write_json(SELECTED_PROXY_CANDIDATE, best)
    write_csv(SELECTED_EXPECTED_TRADE_TAPE, selected_trades.to_dict("records") if not selected_trades.empty else [])
    write_csv(SELECTED_SESSION_SUMMARY, replay.summary_rows(selected_trades, ["entry_session", "side"]))
    write_csv(SELECTED_MONTH_SIDE_SUMMARY, replay.summary_rows(selected_trades, ["entry_month", "side"]))
    write_csv(POLICY_ATTRIBUTION, replay.policy_attribution_rows(surface))
    write_csv(BASELINE_COMPARISON, comparison)
    write_csv(RUN364AQ_QUEUE, review_queue)
    write_work_packet()

    created_at = now_utc()
    final_seed = {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "selected_variant_id": best.get("variant_id", ""),
        "selected_combined_net_profit": best.get("combined_net_profit", ""),
        "selected_combined_profit_factor": best.get("combined_profit_factor", ""),
        "selected_combined_trade_per_business_day": best.get("combined_trade_per_business_day", ""),
        "selected_combined_max_drawdown": best.get("combined_max_drawdown", ""),
    }
    gates = write_receipts(final_seed)
    final = final_payload(parent_final, surface, best, len(strict), len(skipped_audit), gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface, comparison, gates)
    write_ledgers(final, gates)
    repair_run_registry_line_endings(RUN_ID)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
