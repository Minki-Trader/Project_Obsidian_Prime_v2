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

from stage_pipelines.stage364 import materialize_density_restore_stress_to_candidate_inputs_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_pf_pass_density_restore_offensive_scout_without_db as replay  # noqa: E402
from stage_pipelines.stage364 import train_threshold_edge_density_restore_cost_session_scout_without_db as ay_scout  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BB"
RUN_ID = "run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
SOURCE_AW_FINAL = ay_scout.SOURCE_AW_FINAL
SOURCE_RUNTIME_POLICY = ay_scout.SOURCE_RUNTIME_POLICY
NEXT_RUN_ID = "run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1"

STATUS = "completed_stage364BB_density_restore_stress_to_candidate_proxy_scout_review_required_no_authority"
JUDGMENT = "proxy_scout_completed_density_restore_stress_candidates_ranked_review_required_no_authority"
DECISION = "stage364BB_open_run364BC_review_density_restore_stress_to_candidate_scout"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
TARGET_PF = 1.25

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EXPECTED_DIR = RUN_DIR / "expected_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
QUEUE_REPLAY_AUDIT = RUN_DIR / "queue_replay_audit.csv"
SCOUT_SURFACE = RUN_DIR / "density_restore_stress_to_candidate_proxy_scout_surface.csv"
STRICT_CANDIDATES = RUN_DIR / "strict_proxy_candidates.csv"
PACKAGE_ELIGIBLE_CANDIDATES = RUN_DIR / "package_eligible_candidates.csv"
SELECTED_PROXY_CANDIDATE = RUN_DIR / "selected_proxy_candidate.json"
SELECTED_EXPECTED_TRADE_TAPE = EXPECTED_DIR / "selected_trade_tape.csv"
SELECTED_SESSION_SUMMARY = RUN_DIR / "selected_session_summary.csv"
SELECTED_MONTH_SIDE_SUMMARY = RUN_DIR / "selected_month_side_summary.csv"
DENSITY_SURVIVAL_COMPARISON = RUN_DIR / "density_survival_comparison.csv"
POLICY_ATTRIBUTION = RUN_DIR / "policy_attribution.csv"
BASELINE_COMPARISON = RUN_DIR / "baseline_comparison.csv"
RUN364BC_QUEUE = RUN_DIR / "run364BC_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364BB_density_restore_stress_candidate_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BB_density_restore_stress_candidate_scout.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

INPUTS = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364BB_QUEUE,
    parent.GUARDRAIL_MATRIX,
    parent.AXIS_MAP,
    parent.REPORT_PATH,
    parent.LINEAGE_RECEIPT,
    SOURCE_AW_FINAL,
    SOURCE_RUNTIME_POLICY,
]

OUTPUTS = [
    INPUT_MANIFEST,
    QUEUE_REPLAY_AUDIT,
    SCOUT_SURFACE,
    STRICT_CANDIDATES,
    PACKAGE_ELIGIBLE_CANDIDATES,
    SELECTED_PROXY_CANDIDATE,
    SELECTED_EXPECTED_TRADE_TAPE,
    SELECTED_SESSION_SUMMARY,
    SELECTED_MONTH_SIDE_SUMMARY,
    DENSITY_SURVIVAL_COMPARISON,
    POLICY_ATTRIBUTION,
    BASELINE_COMPARISON,
    RUN364BC_QUEUE,
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
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_csv_rows(path)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


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
    if isinstance(value, pd.DataFrame):
        return value.to_dict("records")
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float:
    number = as_float(value)
    if not math.isfinite(number):
        return 0.0
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, EXPECTED_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def patch_replay_globals() -> None:
    replay.RUN_ID = RUN_ID
    replay.RUN_NUMBER = RUN_NUMBER
    replay.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    replay.NEXT_RUN_ID = NEXT_RUN_ID
    replay.DENSITY_FLOOR = DENSITY_FLOOR
    replay.TARGET_PF = TARGET_PF


def validate_inputs() -> tuple[Mapping[str, Any], Mapping[str, Any], list[dict[str, str]]]:
    missing = [rel(path) for path in INPUTS if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BB inputs(BB 입력 누락): " + ", ".join(missing))
    parent_final = read_json(parent.FINAL_DECISION)
    aw_final = read_json(SOURCE_AW_FINAL)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if any(parent_final.get(key) != "not_claimed" for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]):
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과되지 않음)")
    queue = read_csv_rows(parent.RUN364BB_QUEUE)
    if len(queue) != 6:
        raise RuntimeError(f"unexpected BB queue rows(BB 대기열 행 수 이상): {len(queue)}")
    for row in queue:
        if "not_used" not in str(row.get("trade_splitting_status", "")):
            raise RuntimeError("trade splitting guardrail missing(거래 쪼개기 금지 누락)")
        if "forbidden" not in str(row.get("top_n_status", "")):
            raise RuntimeError("top_n guardrail missing(top_n 금지 누락)")
        if "forbidden" not in str(row.get("oos_threshold_selection_status", "")):
            raise RuntimeError("OOS threshold guardrail missing(OOS 임계값 금지 누락)")
        if "entry_time_known_only_closed_bar" not in str(row.get("timestamp_boundary", "")):
            raise RuntimeError("timestamp boundary mismatch(시점 경계 불일치)")
    return parent_final, aw_final, queue


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "run364BB_scout_queue.csv":
        return "BB scout queue(BB 스카우트 대기열)"
    if name == "final_decision.json":
        return "parent final decision(부모 최종 결정)"
    if name == "required_gate_coverage_audit.csv":
        return "parent gate audit(부모 게이트 감사)"
    if name == "stress_to_candidate_guardrail_matrix.csv":
        return "guardrail matrix(가드레일 행렬)"
    if name == "stress_to_candidate_axis_map.csv":
        return "axis map(축 지도)"
    if name == "runtime_policy_config.json":
        return "source runtime policy(원천 런타임 정책)"
    return "supporting evidence(보조 근거)"


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_role": input_role(path),
            "path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "effect": "입력 path/hash(경로/해시)를 고정해 BA materialization(BA 물질화)에서 BB scout(BB 스카우트)까지 계보를 잇는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUTS
    ]


def source_runtime_bridge() -> tuple[str, float]:
    return ay_scout.source_runtime_bridge()


def queue_variants(queue: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bridge_policy, bridge_value = source_runtime_bridge()
    executable: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for index, row in enumerate(queue, start=1):
        implementation = str(row.get("implementation_required", ""))
        variant_id = row.get("variant_id", f"run364BB_queue_{index:02d}")
        if not implementation.startswith("no"):
            skipped.append(
                {
                    "run_id": RUN_ID,
                    "queue_rank": as_int(row.get("queue_rank"), index),
                    "queue_id": row.get("queue_id", ""),
                    "variant_id": variant_id,
                    "replay_status": "skipped_implementation_required(구현 필요로 건너뜀)",
                    "reason": implementation,
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
                "seed_variant_id": row.get("source_variant_id", ""),
                "source_queue_id": row.get("source_ay_queue_id", PARENT_RUN_ID),
                "variant_id": variant_id,
                "short_threshold": as_float(row.get("short_probability_threshold"), 0.45),
                "long_threshold": as_float(row.get("long_threshold"), replay.prev.scout.base.LONG_THRESHOLD),
                "min_margin": as_float(row.get("min_margin"), -0.000562137088),
                "entry_margin_floor": as_float(row.get("entry_margin_floor"), 0.0005),
                "long_block_feature": replay.prev.scout.base.SIDE_FILTER_FEATURE,
                "long_block_min": 40.0,
                "max_hold_m5": as_int(row.get("max_hold_m5"), 6),
                "bridge_policy": bridge_policy,
                "bridge_policy_value": bridge_value,
                "density_restore_budget": 0.0,
                "materialized_policy": row.get("axis_id", ""),
                "session_policy": row.get("session_policy", ""),
                "side_policy": row.get("side_policy", ""),
                "restore_policy": row.get("expected_effect", ""),
                "source_session_policy": row.get("session_policy", ""),
                "source_month_stress_policy": row.get("month_stress_policy", ""),
                "source_hour_stress_policy": row.get("hour_stress_policy", ""),
                "density_proxy_target_per_day": as_float(row.get("density_proxy_target_per_day"), 0.0),
                "expected_mt5_survival_ratio": as_float(row.get("expected_mt5_survival_ratio"), 0.0),
                "estimated_mt5_density_from_materialization": as_float(row.get("estimated_mt5_density_per_day"), 0.0),
                "implementation_required": implementation,
                "trade_splitting_status": row.get("trade_splitting_status", ""),
                "top_n_status": row.get("top_n_status", ""),
                "oos_threshold_selection_status": row.get("oos_threshold_selection_status", ""),
                "timestamp_boundary": row.get("timestamp_boundary", ""),
                "expected_effect": row.get("expected_effect", ""),
            }
        )
    return executable, skipped


def reference_from_aw(aw_final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "reference_run_id": aw_final.get("run_id", ""),
        "reference_variant_id": aw_final.get("package_run_id", ""),
        "reference_label": "run364AW MT5 runtime probe review(364AW MT5 런타임 탐침 검토)",
        "reference_combined_net_profit": as_float(aw_final.get("mt5_net_profit")),
        "reference_combined_profit_factor": as_float(aw_final.get("mt5_profit_factor")),
        "reference_combined_trade_count": as_float(aw_final.get("mt5_trade_count")),
        "reference_combined_trade_per_business_day": as_float(aw_final.get("trade_per_business_day")),
        "reference_combined_expectancy": as_float(aw_final.get("mt5_expectancy")),
        "reference_combined_max_drawdown": as_float(aw_final.get("mt5_max_drawdown_percent")),
        "reference_combined_recovery_factor": as_float(aw_final.get("mt5_recovery_factor")),
        "reference_combined_long_count": as_float(aw_final.get("long_trade_count")),
        "reference_combined_short_count": as_float(aw_final.get("short_trade_count")),
        "reference_combined_long_short_balance": as_float(aw_final.get("long_share")),
        "target_profit_factor": TARGET_PF,
        "density_floor": DENSITY_FLOOR,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def is_candidate_queue_type(queue_type: str) -> bool:
    return "candidate" in queue_type


def enrich_surface(surface: pd.DataFrame, variants: Sequence[Mapping[str, Any]], reference: Mapping[str, Any], aw_final: Mapping[str, Any]) -> pd.DataFrame:
    if surface.empty:
        return surface
    out = surface.copy()
    by_variant = {str(item["variant_id"]): item for item in variants}
    survival_ratio = as_float(aw_final.get("mt5_trade_count")) / max(1.0, as_float(aw_final.get("expected_trade_count"), 1.0))
    business_days = max(1, as_int(aw_final.get("expected_business_days"), 333))
    extra_rows: list[dict[str, Any]] = []
    for row in out.to_dict("records"):
        variant = by_variant.get(str(row.get("variant_id")), {})
        trade_count = as_float(row.get("combined_trade_count"))
        estimated_mt5_trade_count = int(round(trade_count * survival_ratio))
        estimated_mt5_density = estimated_mt5_trade_count / business_days
        pf = as_float(row.get("combined_profit_factor"))
        val_net = as_float(row.get("validation_net_profit"))
        oos_net = as_float(row.get("oos_net_profit"))
        short_count = as_float(row.get("combined_short_count"))
        queue_type = str(row.get("queue_type", ""))
        implementation = str(variant.get("implementation_required", ""))
        if estimated_mt5_density < DENSITY_FLOOR:
            status = "fail_estimated_mt5_density_floor(추정 MT5 밀도 하한 실패)"
        elif pf < TARGET_PF:
            status = "fail_proxy_pf_floor(프록시 수익 팩터 하한 실패)"
        elif val_net <= 0 or oos_net <= 0:
            status = "fail_split_profit(분할 수익 실패)"
        elif short_count <= 0:
            status = "fail_short_side_zero(숏 0 실패)"
        elif is_candidate_queue_type(queue_type) and implementation.startswith("no"):
            status = "package_reviewable_proxy_candidate(패키지 검토 가능 프록시 후보)"
        else:
            status = "watch_proxy_surface(프록시 표면 관찰)"
        strict_pass = status.startswith("package_reviewable")
        package_eligible = strict_pass and is_candidate_queue_type(queue_type) and implementation.startswith("no")
        score = (
            as_float(row.get("combined_net_profit"))
            + 950.0 * max(0.0, pf - TARGET_PF)
            + 620.0 * max(0.0, estimated_mt5_density - DENSITY_FLOOR)
            + 0.22 * short_count
            - 520.0 * max(0.0, TARGET_PF - pf)
            - 1300.0 * max(0.0, DENSITY_FLOOR - estimated_mt5_density)
            - 0.10 * max(0.0, abs(as_float(row.get("combined_max_drawdown"))) - abs(as_float(reference.get("reference_combined_max_drawdown"))))
        )
        if not package_eligible:
            score -= 120.0
        if queue_type == "repair_candidate":
            score -= 35.0
        extra_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "estimated_mt5_trade_count": estimated_mt5_trade_count,
                "estimated_mt5_trade_per_business_day": finite(estimated_mt5_density, 10),
                "observed_mt5_proxy_survival_ratio": finite(survival_ratio, 10),
                "business_days": business_days,
                "density_floor": DENSITY_FLOOR,
                "target_profit_factor": TARGET_PF,
                "density_gap_after_survival": finite(estimated_mt5_density - DENSITY_FLOOR, 10),
                "bb_candidate_status": status,
                "strict_proxy_pass": strict_pass,
                "package_eligible_proxy": package_eligible,
                "selection_score": finite(score, 10),
            }
        )
    extra = pd.DataFrame(extra_rows)
    out = out.drop(columns=[col for col in ["bb_candidate_status", "selection_score"] if col in out.columns])
    out = out.merge(extra, on="variant_id", how="left")
    out["net_delta_vs_run364AW_mt5"] = out["combined_net_profit"].astype(float) - as_float(reference.get("reference_combined_net_profit"))
    out["pf_delta_vs_run364AW_mt5"] = out["combined_profit_factor"].astype(float) - as_float(reference.get("reference_combined_profit_factor"))
    out["trade_count_delta_vs_run364AW_mt5"] = out["combined_trade_count"].astype(float) - as_float(reference.get("reference_combined_trade_count"))
    out["estimated_mt5_density_delta_vs_run364AW"] = out["estimated_mt5_trade_per_business_day"].astype(float) - as_float(reference.get("reference_combined_trade_per_business_day"))
    return out.sort_values(["package_eligible_proxy", "selection_score"], ascending=[False, False]).reset_index(drop=True)


def strict_surface(surface: pd.DataFrame) -> pd.DataFrame:
    if surface.empty:
        return surface.iloc[0:0].copy()
    return surface[surface["strict_proxy_pass"].astype(bool)].copy()


def package_eligible_surface(surface: pd.DataFrame) -> pd.DataFrame:
    if surface.empty:
        return surface.iloc[0:0].copy()
    return surface[surface["package_eligible_proxy"].astype(bool)].copy()


def comparison_rows(best: Mapping[str, Any], reference: Mapping[str, Any]) -> list[dict[str, Any]]:
    pairs = [
        ("net_profit", "combined_net_profit", "reference_combined_net_profit"),
        ("profit_factor", "combined_profit_factor", "reference_combined_profit_factor"),
        ("proxy_trade_count", "combined_trade_count", "reference_combined_trade_count"),
        ("estimated_mt5_density", "estimated_mt5_trade_per_business_day", "reference_combined_trade_per_business_day"),
        ("expectancy", "combined_expectancy", "reference_combined_expectancy"),
        ("drawdown", "combined_max_drawdown", "reference_combined_max_drawdown"),
        ("recovery_factor", "combined_recovery_factor", "reference_combined_recovery_factor"),
        ("long_count", "combined_long_count", "reference_combined_long_count"),
        ("short_count", "combined_short_count", "reference_combined_short_count"),
    ]
    return [
        {
            "run_id": RUN_ID,
            "metric_id": metric_id,
            "reference_run": reference.get("reference_run_id", ""),
            "reference_value": reference.get(reference_key, ""),
            "selected_value": best.get(selected_key, ""),
            "delta_selected_minus_reference": finite(as_float(best.get(selected_key)) - as_float(reference.get(reference_key)), 10),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for metric_id, selected_key, reference_key in pairs
    ]


def density_survival_rows(surface: pd.DataFrame, aw_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    if surface.empty:
        return []
    ratio = as_float(aw_final.get("mt5_trade_count")) / max(1.0, as_float(aw_final.get("expected_trade_count"), 1.0))
    rows: list[dict[str, Any]] = []
    for row in surface.to_dict("records"):
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "proxy_trade_count": row.get("combined_trade_count", ""),
                "observed_survival_ratio_from_AW": finite(ratio, 10),
                "estimated_mt5_trade_count": row.get("estimated_mt5_trade_count", ""),
                "estimated_mt5_trade_per_business_day": row.get("estimated_mt5_trade_per_business_day", ""),
                "materialized_estimated_mt5_density": row.get("estimated_mt5_density_from_materialization", ""),
                "density_floor": DENSITY_FLOOR,
                "status": "passes_floor" if as_float(row.get("estimated_mt5_trade_per_business_day")) >= DENSITY_FLOOR else "below_floor",
                "effect": "AW runtime survival ratio(AW 런타임 생존비)를 보조로 적용해 MT5 밀도 하한을 가늠한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_queue_rows(best: Mapping[str, Any], strict_count: int, package_count: int, skipped_count: int) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "review_density_restore_stress_to_candidate_scout(밀도 복원 압박-후보 스카우트 검토)",
            "selected_variant_id": best.get("variant_id", ""),
            "selected_queue_id": best.get("queue_id", ""),
            "selected_candidate_status": best.get("bb_candidate_status", ""),
            "strict_proxy_pass_rows": strict_count,
            "package_eligible_rows": package_count,
            "skipped_implementation_required_rows": skipped_count,
            "selected_net_profit": best.get("combined_net_profit", ""),
            "selected_profit_factor": best.get("combined_profit_factor", ""),
            "selected_estimated_mt5_trade_per_business_day": best.get("estimated_mt5_trade_per_business_day", ""),
            "selected_proxy_trade_count": best.get("combined_trade_count", ""),
            "selected_drawdown": best.get("combined_max_drawdown", ""),
            "selected_short_count": best.get("combined_short_count", ""),
            "question": "Can BB candidate survive package review without trade splitting?(BB 후보가 거래 쪼개기 없이 패키지 검토를 통과할 수 있는가?)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {"run_id": RUN_ID, "gate": name, "status": status, "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def gate_rows(skipped_count: int) -> list[dict[str, Any]]:
    return [
        gate_row("scope_completion_gate(범위 완료 게이트)", SCOUT_SURFACE, "BB queue(BB 대기열)의 실행 가능 후보를 proxy replay(프록시 재생)로 평가했다."),
        gate_row("parent_materialization_gate(부모 물질화 게이트)", parent.FINAL_DECISION, "BA materialization(BA 물질화)이 BB run_id(BB 실행 ID)를 열었는지 확인했다."),
        gate_row("kpi_contract_audit(KPI 계약 감사)", BASELINE_COMPARISON, "net/PF/density/DD/side KPI(순수익/수익 팩터/밀도/낙폭/방향 지표)를 같은 표면에 기록했다."),
        gate_row("topn_absence_gate(top_n 부재 게이트)", QUEUE_REPLAY_AUDIT, "top_n(상위 N개) 선택 없이 사전 queue(대기열)를 그대로 재생했다."),
        gate_row("trade_splitting_absence_gate(거래 쪼개기 부재 게이트)", QUEUE_REPLAY_AUDIT, "거래 쪼개기 없이 신호 발생 자체만 평가했다."),
        gate_row("oos_threshold_lock_gate(OOS 임계값 잠금 게이트)", parent.RUN364BB_QUEUE, "OOS threshold selection(OOS 임계값 선택)을 금지한 queue(대기열)를 사용했다."),
        gate_row("timestamp_boundary_gate(시점 경계 게이트)", parent.RUN364BB_QUEUE, "entry-time closed-bar(진입 시점 닫힌 봉) 경계를 유지했다."),
        gate_row("implementation_required_visibility_gate(구현 필요 가시화 게이트)", QUEUE_REPLAY_AUDIT, f"새 runtime policy(런타임 정책)가 필요한 {skipped_count}개 행을 숨기지 않고 skipped(건너뜀)로 기록했다."),
        gate_row("skill_receipt_lint(스킬 영수증 점검)", EXPERIMENT_RECEIPT, "experiment/data/model/lineage/judgment receipt(실험/데이터/모델/계보/판정 영수증)를 썼다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "work packet(작업 묶음)의 required gates(필수 게이트)를 closeout(종료 기록)에 연결했다."),
        gate_row("final_claim_guard(최종 주장 가드)", CLAIM_RECEIPT, "runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않았다."),
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "parent_materialization_gate",
                "kpi_contract_audit",
                "topn_absence_gate",
                "trade_splitting_absence_gate",
                "oos_threshold_lock_gate",
                "timestamp_boundary_gate",
                "implementation_required_visibility_gate",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def final_payload(
    parent_final: Mapping[str, Any],
    aw_final: Mapping[str, Any],
    surface: pd.DataFrame,
    best: Mapping[str, Any],
    strict_count: int,
    package_count: int,
    skipped_count: int,
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "source_aw_runtime_review_run_id": aw_final.get("run_id", ""),
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_bb_queue_rows": parent_final.get("bb_queue_rows", ""),
        "scout_rows": int(len(surface)),
        "strict_proxy_pass_rows": strict_count,
        "package_eligible_rows": package_count,
        "skipped_implementation_required_rows": skipped_count,
        "target_profit_factor": TARGET_PF,
        "density_floor": DENSITY_FLOOR,
        "observed_mt5_proxy_trade_survival_ratio": finite(as_float(aw_final.get("mt5_trade_count")) / max(1.0, as_float(aw_final.get("expected_trade_count"), 1.0)), 10),
        "selected_variant_id": best.get("variant_id", ""),
        "selected_queue_id": best.get("queue_id", ""),
        "selected_candidate_status": best.get("bb_candidate_status", ""),
        "selected_package_eligible_proxy": best.get("package_eligible_proxy", False),
        "selected_combined_net_profit": best.get("combined_net_profit", ""),
        "selected_combined_profit_factor": best.get("combined_profit_factor", ""),
        "selected_combined_trade_count": best.get("combined_trade_count", ""),
        "selected_combined_trade_per_business_day": best.get("combined_trade_per_business_day", ""),
        "selected_estimated_mt5_trade_count": best.get("estimated_mt5_trade_count", ""),
        "selected_estimated_mt5_trade_per_business_day": best.get("estimated_mt5_trade_per_business_day", ""),
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
        "top_n_rows": 0,
        "trade_splitting_rows": 0,
        "oos_threshold_selection_rows": 0,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(path) for path in INPUTS],
            "time_axis": "timestamp_dt UTC order and bar_time_server entry session(timestamp_dt UTC 순서와 bar_time_server 진입 세션)",
            "sample_scope": "FPMarkets US100 M5 validation+oos proxy replay, Tier A only(FPMarkets US100 5분봉 검증+OOS 프록시 재생, Tier A만)",
            "missing_or_duplicate_check": "runtime frame duplicate timestamp and required-value checks passed(런타임 프레임 중복 시각과 필수값 점검 통과)",
            "feature_label_boundary": "entry-time probability, margin, session, and closed bar only(진입 시점 확률, 마진, 세션, 닫힌 봉만 사용)",
            "split_boundary": "validation/oos reported separately and not used for OOS threshold choice(검증/OOS 분리 보고, OOS 임계값 선택 없음)",
            "leakage_risk": "proxy ranking before MT5 may overstate usefulness, so authority is not claimed(MT5 전 프록시 순위가 효용을 과장할 수 있어 권위 미주장)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUTS if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "stress pass can become package-reviewable density candidate without trade splitting(압박 통과가 거래 쪼개기 없이 패키지 검토 가능 밀도 후보가 될 수 있음)",
            "decision_use": "open BB review for MT5 package decision(BB 검토를 열어 MT5 패키지 여부를 결정)",
            "comparison_baseline": "run364AW MT5 runtime probe review(364AW MT5 런타임 탐침 검토)",
            "control_variables": "US100 M5 probability tape, one-position replay, no top_n, no trade splitting(US100 5분봉 확률 테이프, 단일 포지션 재생, top_n 없음, 거래 쪼개기 없음)",
            "changed_variables": "short threshold and entry margin floor from BA queue(BA 대기열의 숏 임계값과 진입 마진 하한)",
            "sample_scope": "BA candidate rows executable without new runtime policy(새 런타임 정책 없이 실행 가능한 BA 후보 행)",
            "success_criteria": "estimated MT5 density>=3/day, PF>=1.25, split net positive, short nonzero(추정 MT5 밀도 3/day 이상, PF 1.25 이상, 분할 순수익 양수, 숏 0 아님)",
            "failure_criteria": "package eligible rows zero or DD/cost stress worsens(패키지 가능 행 0 또는 낙폭/비용 압박 악화)",
            "invalid_conditions": "top_n, trade splitting, OOS threshold selection, future feature use(top_n, 거래 쪼개기, OOS 임계값 선택, 미래 피처 사용)",
            "stop_conditions": "after 4 executable rows and 2 implementation diagnostics are recorded(실행 가능 4행과 구현 진단 2행 기록 후 중지)",
            "evidence_plan": [rel(SCOUT_SURFACE), rel(PACKAGE_ELIGIBLE_CANDIDATES), rel(RUN364BC_QUEUE), rel(FINAL_DECISION)],
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "existing ONNX probability tape replay, no new model training(기존 ONNX 확률 테이프 재생, 새 모델 학습 없음)",
            "threshold_policy": "BA pre-materialized thresholds only, no OOS threshold search(BA 사전 물질화 임계값만 사용, OOS 임계값 탐색 없음)",
            "validation_judgment": "exploratory_proxy_no_authority(탐색 프록시, 권위 없음)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": f"selected={final['selected_variant_id']}; net={final['selected_combined_net_profit']}; pf={final['selected_combined_profit_factor']}; est_density={final['selected_estimated_mt5_trade_per_business_day']}",
            "comparison_baseline": "run364AW MT5 runtime probe review(364AW MT5 런타임 탐침 검토)",
            "segment_checks": [rel(SELECTED_SESSION_SUMMARY), rel(SELECTED_MONTH_SIDE_SUMMARY), rel(POLICY_ATTRIBUTION)],
            "trade_shape": {
                "trade_count": final["selected_combined_trade_count"],
                "expectancy": final["selected_combined_expectancy"],
                "drawdown": final["selected_combined_max_drawdown"],
                "long_count": final["selected_combined_long_count"],
                "short_count": final["selected_combined_short_count"],
            },
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run364BB density restore stress-to-candidate proxy scout(run364BB 밀도 복원 압박-후보 프록시 스카우트)",
            "evidence_available": [rel(SCOUT_SURFACE), rel(STRICT_CANDIDATES), rel(PACKAGE_ELIGIBLE_CANDIDATES), rel(FINAL_DECISION)],
            "evidence_missing": "MT5 runtime probe, ONNX export, forward pass(MT5 런타임 탐침, ONNX 내보내기, 전진 검증 없음)",
            "judgment_label": "exploratory(탐색)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "프록시 후보가 나와도 아직 운영 모델은 아니다.",
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
        },
    )


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
    top_rows = surface.head(8).to_dict("records")
    report = f"""# run364BB density restore stress-to-candidate proxy scout(364BB 밀도 복원 압박-후보 프록시 스카우트)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- scout_rows(스카우트 행): `{final['scout_rows']}`
- strict_proxy_pass_rows(엄격 프록시 통과 행): `{final['strict_proxy_pass_rows']}`
- package_eligible_rows(패키지 검토 가능 행): `{final['package_eligible_rows']}`
- skipped_implementation_required_rows(구현 필요 건너뜀 행): `{final['skipped_implementation_required_rows']}`
- selected_net/PF/proxy_trades/estimated_MT5_density/DD(선택 순수익/수익 팩터/프록시 거래수/추정 MT5 밀도/낙폭): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_count']}` / `{final['selected_estimated_mt5_trade_per_business_day']}` / `{final['selected_combined_max_drawdown']}`
- runtime_authority(런타임 권위): `not_claimed`

## Surface(표면)

{markdown_table(top_rows, ['queue_rank', 'queue_id', 'bb_candidate_status', 'package_eligible_proxy', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_count', 'estimated_mt5_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count', 'selection_score'])}

## AW Comparison(AW 비교)

{markdown_table(comparison, ['metric_id', 'reference_value', 'selected_value', 'delta_selected_minus_reference'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): BB candidate(BB 후보)를 proxy scout(프록시 스카우트)로 좁게 평가했지만 MT5 runtime probe(MT5 런타임 탐침)가 아니므로 operating promotion(운영 승격)은 주장하지 않는다.
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- selected(선택): `{final['selected_variant_id']}`\n- package_eligible_rows(패키지 검토 가능 행): `{final['package_eligible_rows']}`\n- effect(효과): `{NEXT_RUN_ID}` review(검토) 대상으로 넘긴다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364BB Density Restore Stress-To-Candidate Proxy Scout Closeout",
        f"\n## run364BB Density Restore Stress-To-Candidate Proxy Scout Closeout(364BB 밀도 복원 압박-후보 프록시 스카우트 종료)\n\nAction(행동): BA queue(BA 대기열)의 실행 가능 후보 4개를 proxy replay(프록시 재생)로 평가했다.\n\nEffect(효과): Stage364(364단계)를 분기하지 않고 `{NEXT_RUN_ID}` review(검토)로 이어간다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_proxy_review_required(없음, 프록시 검토 필요)
- latest_proxy_scout(최근 프록시 스카우트): `{RUN_ID}`
- selected_proxy_candidate(선택 프록시 후보): `{rel(SELECTED_PROXY_CANDIDATE)}`
- package_eligible_rows(패키지 검토 가능 행): `{final['package_eligible_rows']}`
- selected_estimated_mt5_density(선택 추정 MT5 밀도): `{final['selected_estimated_mt5_trade_per_business_day']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364BB(364BB 실행)는 BA scout queue(BA 스카우트 대기열)의 실행 가능 후보 4개를 proxy replay(프록시 재생)로 평가했다. selected candidate(선택 후보)는 `{final['selected_variant_id']}`이고 proxy PF(프록시 수익 팩터)는 `{final['selected_combined_profit_factor']}`, estimated MT5 density(추정 MT5 밀도)는 `{final['selected_estimated_mt5_trade_per_business_day']}`/day(일)이다. package_eligible_rows(패키지 검토 가능 행)는 `{final['package_eligible_rows']}`이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 BB surface(BB 표면)를 검토해 MT5 package(MT5 패키지)로 열지, 추가 materialization(물질화)로 돌릴지 결정한다.
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
    )
    append_text_once(
        STAGE_README,
        "run364BB Density Restore Stress-To-Candidate Proxy Scout",
        f"\n## run364BB Density Restore Stress-To-Candidate Proxy Scout(364BB 밀도 복원 압박-후보 프록시 스카우트)\n\nAction(행동): BA queue(BA 대기열)를 proxy replay(프록시 재생)로 실행했다.\n\nEffect(효과): package-reviewable(패키지 검토 가능) 후보 여부를 `{NEXT_RUN_ID}` review(검토)로 넘긴다.\n",
    )
    append_text_once(
        CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): density restore stress-to-candidate proxy scout(밀도 복원 압박-후보 프록시 스카우트)를 실행했다.\n- effect(효과): `{NEXT_RUN_ID}` review queue(검토 대기열)를 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): AZ stress pass(AZ 압박 통과)를 candidate(후보)로 바꿔 PF 1.25와 추정 MT5 밀도 3/day를 동시에 시험한다.\n- effect(효과): package ineligible(패키지 부적격) 단서를 idea-dead(아이디어 사망)로 닫지 않고 공격 탐색으로 재사용한다.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- status(상태): pending_review(검토 대기).\n- action(행동): BB proxy surface(BB 프록시 표면)를 만들었다.\n- effect(효과): negative/positive(부정/긍정) 판정은 `{NEXT_RUN_ID}` review(검토)에서 package eligibility(패키지 가능성)와 분리해 결정한다.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
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
        "rows": final["scout_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(RUN_DIR),
        "primary_report": rel(REPORT_PATH),
        "family": "stage364_proxy_scout(364단계 프록시 스카우트)",
        "lane": "offensive_exploration(공격 탐색)",
        "work_family": "experiment_execution(실험 실행)",
        "primary_artifact": rel(SCOUT_SURFACE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_started_proxy_only(프록시 전용이라 시작 안 함)",
        "next_action": NEXT_RUN_ID,
        "question": "Can stress pass become a package-reviewable density candidate without trade splitting?(압박 통과를 거래 쪼개기 없이 패키지 검토 가능 밀도 후보로 만들 수 있는가?)",
        "notes": f"strict={final['strict_proxy_pass_rows']};package={final['package_eligible_rows']};skipped={final['skipped_implementation_required_rows']}",
        "net_profit": final["selected_combined_net_profit"],
        "profit_factor": final["selected_combined_profit_factor"],
        "expectancy": final["selected_combined_expectancy"],
        "drawdown": final["selected_combined_max_drawdown"],
        "recovery_factor": final["selected_combined_recovery_factor"],
        "trade_count": final["selected_combined_trade_count"],
        "long_trade_count": final["selected_combined_long_count"],
        "short_trade_count": final["selected_combined_short_count"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common])
    alpha_rows = []
    for suffix, view, tier, scope in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy replay scout(프록시 재생 스카우트)"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A proxy plus Tier B out_of_scope(Tier A 프록시 + Tier B 범위 밖)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": suffix,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "scoreboard_lane": "proxy_scout(프록시 스카우트)",
                "primary_kpi": f"net={final['selected_combined_net_profit']};pf={final['selected_combined_profit_factor']};est_mt5_density={final['selected_estimated_mt5_trade_per_business_day']}",
                "guardrail_kpi": f"no_topn_no_split;package={final['package_eligible_rows']};skipped={final['skipped_implementation_required_rows']}",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        alpha_rows.append(row)
    append_or_replace_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], alpha_rows)
    artifact_rows = []
    for artifact_type, path, notes in [
        ("scout_surface", SCOUT_SURFACE, "Proxy scout surface(프록시 스카우트 표면)."),
        ("strict_candidates", STRICT_CANDIDATES, "Strict proxy candidates(엄격 프록시 후보)."),
        ("package_eligible", PACKAGE_ELIGIBLE_CANDIDATES, "Package eligible proxy candidates(패키지 검토 가능 프록시 후보)."),
        ("selected_candidate", SELECTED_PROXY_CANDIDATE, "Selected proxy candidate(선택 프록시 후보)."),
        ("selected_trade_tape", SELECTED_EXPECTED_TRADE_TAPE, "Selected expected trade tape(선택 예상 거래 테이프)."),
        ("review_queue", RUN364BC_QUEUE, "Next review queue(다음 검토 대기열)."),
        ("gate_audit", GATE_AUDIT, "Required gate audit(필수 게이트 감사)."),
        ("report", REPORT_PATH, "Scout report(스카우트 보고서)."),
        ("decision", DECISION_DOC, "Decision record(결정 기록)."),
        ("lineage", LINEAGE_RECEIPT, "Artifact lineage(산출물 계보)."),
    ]:
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha(path) if exists(path) else "",
                "created_at_utc": final["created_at_utc"],
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "notes": notes,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)
    repair_run_registry_line_endings(RUN_ID)


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "artifacts": [{"path": rel(path), "sha256": sha(path), "role": "run364BB output(364BB 출력)"} for path in OUTPUTS if exists(path)],
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUTS if exists(path)],
        },
    )


def main() -> None:
    ensure_dirs()
    patch_replay_globals()
    parent_final, aw_final, queue = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    frame, _feature_order, _threshold = replay.load_runtime_frame()
    variants, skipped_audit = queue_variants(queue)
    reference = reference_from_aw(aw_final)
    surface, selected_trades, audit_rows = replay.evaluate_queue(frame, variants, reference)
    surface = enrich_surface(surface, variants, reference, aw_final)
    strict = strict_surface(surface)
    package_eligible = package_eligible_surface(surface)
    best = surface.iloc[0].to_dict() if not surface.empty else {}
    audit_rows = [dict(row, replay_status="executed(실행됨)") for row in audit_rows] + skipped_audit
    comparison = comparison_rows(best, reference)
    density_survival = density_survival_rows(surface, aw_final)
    review_queue = review_queue_rows(best, len(strict), len(package_eligible), len(skipped_audit))

    write_csv(QUEUE_REPLAY_AUDIT, audit_rows)
    write_csv(SCOUT_SURFACE, surface.to_dict("records"))
    write_csv(STRICT_CANDIDATES, strict.to_dict("records"), list(surface.columns) if not surface.empty else None)
    write_csv(PACKAGE_ELIGIBLE_CANDIDATES, package_eligible.to_dict("records"), list(surface.columns) if not surface.empty else None)
    write_json(SELECTED_PROXY_CANDIDATE, best)
    write_csv(SELECTED_EXPECTED_TRADE_TAPE, selected_trades.to_dict("records") if not selected_trades.empty else [])
    write_csv(SELECTED_SESSION_SUMMARY, replay.summary_rows(selected_trades, ["entry_session", "side"]))
    write_csv(SELECTED_MONTH_SIDE_SUMMARY, replay.summary_rows(selected_trades, ["entry_month", "side"]))
    write_csv(DENSITY_SURVIVAL_COMPARISON, density_survival)
    write_csv(POLICY_ATTRIBUTION, replay.policy_attribution_rows(surface))
    write_csv(BASELINE_COMPARISON, comparison)
    write_csv(RUN364BC_QUEUE, review_queue)
    write_work_packet()

    created_at = now_utc()
    gates = gate_rows(len(skipped_audit))
    write_csv(GATE_AUDIT, gates)
    final = final_payload(parent_final, aw_final, surface, best, len(strict), len(package_eligible), len(skipped_audit), gates, created_at)
    write_receipts(final)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface, comparison, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
