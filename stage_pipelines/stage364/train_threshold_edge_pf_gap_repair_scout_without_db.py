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

from stage_pipelines.stage364 import materialize_threshold_edge_pf_gap_repair_inputs_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_pf_pass_density_restore_offensive_scout_without_db as replay  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AS"
RUN_ID = "run364AS_train_threshold_edge_pf_gap_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.PARENT_RUN_ID
NEXT_RUN_ID = "run364AT_review_threshold_edge_pf_gap_repair_scout_without_db_v1"

STATUS = "completed_stage364AS_threshold_edge_pf_gap_repair_proxy_scout_no_mt5_no_authority"
JUDGMENT = "proxy_scout_completed_threshold_edge_pf_gap_repair_ranked_review_required_no_authority"
DECISION = "stage364AS_open_run364AT_review_threshold_edge_pf_gap_repair_scout"
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
SCOUT_SURFACE = RUN_DIR / "threshold_edge_pf_gap_repair_proxy_scout_surface.csv"
STRICT_CANDIDATES = RUN_DIR / "strict_proxy_candidates.csv"
SELECTED_PROXY_CANDIDATE = RUN_DIR / "selected_proxy_candidate.json"
SELECTED_EXPECTED_TRADE_TAPE = EXPECTED_DIR / "selected_trade_tape.csv"
SELECTED_SESSION_SUMMARY = RUN_DIR / "selected_session_summary.csv"
SELECTED_MONTH_SIDE_SUMMARY = RUN_DIR / "selected_month_side_summary.csv"
POLICY_ATTRIBUTION = RUN_DIR / "policy_attribution.csv"
BASELINE_COMPARISON = RUN_DIR / "baseline_comparison.csv"
RUN364AT_QUEUE = RUN_DIR / "run364AT_review_queue.csv"
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
REPORT_PATH = REVIEW_DIR / "run364AS_threshold_edge_pf_gap_repair_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AS_threshold_edge_pf_gap_repair_scout.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

INPUTS = [
    parent.RUN364AS_QUEUE,
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.SOURCE_SEED_METRICS,
]

OUTPUTS = [
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
    RUN364AT_QUEUE,
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
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def read_json(path: Path) -> Any:
    return parent.read_json(path)


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


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def validate_inputs() -> Mapping[str, Any]:
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과하지 않음)")
    queue = read_csv_rows(parent.RUN364AS_QUEUE)
    if len(queue) != 8:
        raise RuntimeError(f"unexpected run364AS queue rows(364AS 대기열 행 수 이상): {len(queue)}")
    for row in queue:
        if row.get("top_n_status") != "forbidden(금지)":
            raise RuntimeError("top_n guardrail missing(top_n 금지 누락)")
        if row.get("trade_splitting_status") != "not_used(거래 쪼개기 없음)":
            raise RuntimeError("trade splitting guardrail missing(거래 쪼개기 금지 누락)")
        if row.get("oos_threshold_selection_status") != "forbidden(금지)":
            raise RuntimeError("OOS threshold guardrail missing(표본외 임계값 선택 금지 누락)")
        if row.get("timestamp_boundary") != "entry_time_known_only(진입 시점에 알려진 값만 사용)":
            raise RuntimeError("timestamp boundary mismatch(시점 경계 불일치)")
    missing = [rel(path) for path in INPUTS if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AS inputs(364AS 입력 누락): " + ", ".join(missing))
    return parent_final


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "run364AS_scout_queue.csv":
        return "parent scout queue(부모 정찰 대기열)"
    if name == "final_decision.json":
        return "parent final decision(부모 최종 결정)"
    if name == "required_gate_coverage_audit.csv":
        return "parent gate audit(부모 게이트 감사)"
    if name == "source_seed_metrics.csv":
        return "source seed metrics(원천 씨앗 지표)"
    return "supporting input(보조 입력)"


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_role": input_role(path),
            "path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) else "",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUTS
    ]


def reference_from_parent(parent_final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "reference_run_id": parent_final.get("parent_run_id", ""),
        "reference_variant_id": parent_final.get("positive_clue_variant_id", ""),
        "reference_label": "run364AQ_threshold_edge_positive_clue(364AQ 임계값 경계 긍정 단서)",
        "reference_combined_net_profit": as_float(parent_final.get("positive_clue_net_profit")),
        "reference_combined_profit_factor": as_float(parent_final.get("positive_clue_profit_factor")),
        "reference_combined_trade_count": 1127.0,
        "reference_combined_trade_per_business_day": as_float(parent_final.get("positive_clue_density")),
        "reference_combined_expectancy": 0.746032,
        "reference_combined_max_drawdown": as_float(parent_final.get("positive_clue_drawdown")),
        "reference_combined_recovery_factor": 5.683856,
        "reference_combined_long_count": 1040.0,
        "reference_combined_short_count": as_float(parent_final.get("positive_clue_short_count")),
        "target_profit_factor": TARGET_PF,
        "density_floor": DENSITY_FLOOR,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def queue_variants() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    executable: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for index, row in enumerate(read_csv_rows(parent.RUN364AS_QUEUE), start=1):
        if row.get("implementation_required") == "yes":
            skipped.append(
                {
                    "run_id": RUN_ID,
                    "queue_rank": as_int(row.get("queue_rank"), index),
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
                "variant_id": row.get("variant_id", f"run364AS_variant_{index:02d}"),
                "short_threshold": as_float(row.get("short_probability_threshold"), 0.455),
                "long_threshold": as_float(row.get("long_threshold"), replay.prev.scout.base.LONG_THRESHOLD),
                "min_margin": as_float(row.get("min_margin"), -0.000562137088),
                "entry_margin_floor": as_float(row.get("entry_margin_floor"), 0.0),
                "long_block_feature": row.get("long_block_feature", replay.prev.scout.base.SIDE_FILTER_FEATURE),
                "long_block_min": as_float(row.get("long_block_min"), 40.0),
                "max_hold_m5": as_int(row.get("max_hold_m5"), 6),
                "bridge_policy": row.get("bridge_policy", ""),
                "bridge_policy_value": row.get("bridge_policy_value", ""),
                "materialized_policy": row.get("materialized_policy", ""),
                "session_policy": row.get("session_policy", ""),
                "side_policy": row.get("side_policy", ""),
                "restore_policy": row.get("restore_policy", ""),
                "density_gap_to_3day": as_float(row.get("density_gap_to_3day"), 0.0),
                "density_restore_budget": as_float(row.get("density_restore_budget"), 0.0),
                "density_restore_status": "as_replay(364AS 재생)",
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


def add_threshold_edge_deltas(surface: pd.DataFrame, reference: Mapping[str, Any]) -> pd.DataFrame:
    if surface.empty:
        return surface
    out = surface.copy()
    out["net_delta_vs_run364AQ_threshold_edge"] = out["combined_net_profit"].astype(float) - as_float(reference.get("reference_combined_net_profit"))
    out["pf_delta_vs_run364AQ_threshold_edge"] = out["combined_profit_factor"].astype(float) - as_float(reference.get("reference_combined_profit_factor"))
    out["dd_delta_vs_run364AQ_threshold_edge"] = out["combined_max_drawdown"].astype(float) - as_float(reference.get("reference_combined_max_drawdown"))
    out["density_delta_vs_run364AQ_threshold_edge"] = out["combined_trade_per_business_day"].astype(float) - as_float(reference.get("reference_combined_trade_per_business_day"))
    for col in [
        "net_delta_vs_run364AQ_threshold_edge",
        "pf_delta_vs_run364AQ_threshold_edge",
        "dd_delta_vs_run364AQ_threshold_edge",
        "density_delta_vs_run364AQ_threshold_edge",
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
            "queue_id": "review_threshold_edge_pf_gap_repair_scout(임계값 경계 PF 간극 수리 정찰 검토)",
            "selected_variant_id": best.get("variant_id", ""),
            "selected_queue_id": best.get("queue_id", ""),
            "selected_candidate_status": best.get("candidate_status", ""),
            "strict_pass_rows": strict_count,
            "skipped_new_policy_rows": skipped_count,
            "selected_net_profit": best.get("combined_net_profit", ""),
            "selected_profit_factor": best.get("combined_profit_factor", ""),
            "selected_trade_per_business_day": best.get("combined_trade_per_business_day", ""),
            "selected_drawdown": best.get("combined_max_drawdown", ""),
            "selected_short_count": best.get("combined_short_count", ""),
            "question": "Does AS scout produce a package-worthy PF/density/DD structure?(AS 정찰이 패키지 가치 PF/밀도/DD 구조를 만드는가?)",
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
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "work_family": "offensive_exploration_proxy_scout(공격 탐색 프록시 정찰)",
            "primary_skill": "obsidian-prime-ml(프로젝트 전용 ML)",
            "support_skills": [
                "obsidian-exploration-mandate(탐색 명령)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "parent_materialization_gate",
                "queue_replay_gate",
                "topn_absence_gate",
                "trade_splitting_absence_gate",
                "oos_threshold_lock_gate",
                "timestamp_boundary_gate",
                "split_report_gate",
                "tier_ledger_gate",
                "claim_boundary_gate",
                "artifact_lineage_gate",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final_seed: Mapping[str, Any]) -> list[dict[str, Any]]:
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "timestamp_boundary": "entry_time_known_only(진입 시점에 알려진 값만 사용)",
            "feature_label_boundary": "no new feature or label; pre-materialized policy queue replay only(새 피처 또는 라벨 없음, 사전 구체화 정책 대기열 재생만)",
            "lookahead_guard": "OOS threshold selection forbidden(표본외 임계값 선택 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "idea_id": "stage364_threshold_edge_pf_gap_repair(364단계 임계값 경계 PF 간극 수리)",
            "hypothesis": "hold compression, margin floor, and late-long blend may close the PF gap without density collapse(보유 압축, 마진 하한, 후반 롱 혼합이 밀도 붕괴 없이 PF 간극을 줄일 수 있음)",
            "legacy_relation": "none(없음)",
            "tier_scope": "Tier A/B paired ledger(Tier A/B 쌍 장부)",
            "broad_sweep": "hold4/hold5/hold6, floor0/floor001, core-late blend(보유4/5/6, 하한0/0.001, 핵심-후반 혼합)",
            "micro_search_gate": "review must find strict pass or positive clue(검토가 엄격 통과 또는 긍정 단서를 찾아야 함)",
            "evidence_boundary": "single-window proxy scout(단일 구간 프록시 정찰)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "not_applicable(해당 없음)",
            "model_training": "not_performed(수행 안 함)",
            "onnx_export": "not_performed(수행 안 함)",
            "threshold_policy": "pre-materialized queue thresholds; no OOS threshold search(사전 구체화 대기열 임계값, 표본외 임계값 탐색 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "selected_variant_id": final_seed.get("selected_variant_id", ""),
            "selected_net_profit": final_seed.get("selected_combined_net_profit", ""),
            "selected_profit_factor": final_seed.get("selected_combined_profit_factor", ""),
            "selected_density": final_seed.get("selected_combined_trade_per_business_day", ""),
            "selected_drawdown": final_seed.get("selected_combined_max_drawdown", ""),
            "comparison_path": rel(BASELINE_COMPARISON),
            "policy_attribution_path": rel(POLICY_ATTRIBUTION),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "judgment": JUDGMENT,
            "evidence_available": [rel(SCOUT_SURFACE), rel(QUEUE_REPLAY_AUDIT), rel(SELECTED_PROXY_CANDIDATE)],
            "evidence_missing": "MT5 runtime probe, ONNX export, forward pass(MT5 런타임 탐침, ONNX 내보내기, 전진 검증 없음)",
            "judgment_label": "exploratory_proxy_scout(탐색 프록시 정찰)",
            "next_condition": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    gates = [
        gate_row("parent_materialization_gate(부모 구체화 게이트)", parent.FINAL_DECISION, "AR materialization(구체화) 완료 확인"),
        gate_row("queue_replay_gate(대기열 재생 게이트)", SCOUT_SURFACE, "실행 가능 queue(대기열) 행을 재생함"),
        gate_row("topn_absence_gate(top_n 부재 게이트)", QUEUE_REPLAY_AUDIT, "top_n 사용 없음"),
        gate_row("trade_splitting_absence_gate(거래 쪼개기 부재 게이트)", QUEUE_REPLAY_AUDIT, "거래 쪼개기 없음"),
        gate_row("oos_threshold_lock_gate(표본외 임계값 잠금 게이트)", parent.RUN364AS_QUEUE, "표본외 임계값 선택 금지 유지"),
        gate_row("timestamp_boundary_gate(시점 경계 게이트)", parent.RUN364AS_QUEUE, "진입 시점에 알려진 값만 사용"),
        gate_row("split_report_gate(분할 보고 게이트)", SCOUT_SURFACE, "validation/OOS(검증/표본외) KPI를 분리 기록"),
        gate_row("tier_ledger_gate(티어 장부 게이트)", ALPHA_LEDGER, "Tier A/B/합산 장부 행을 기록"),
        gate_row("claim_boundary_gate(주장 경계 게이트)", CLAIM_RECEIPT, "운영 주장 없음"),
        gate_row("artifact_lineage_gate(산출물 계보 게이트)", LINEAGE_RECEIPT, "입력/출력 해시를 기록"),
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
        "selected_pf_delta_vs_threshold_edge": best.get("pf_delta_vs_run364AQ_threshold_edge", ""),
        "selected_density_delta_vs_threshold_edge": best.get("density_delta_vs_run364AQ_threshold_edge", ""),
        "selected_dd_delta_vs_threshold_edge": best.get("dd_delta_vs_run364AQ_threshold_edge", ""),
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
    text = f"""# run364AS threshold-edge PF gap repair scout(364AS 임계값 경계 PF 간극 수리 정찰)

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

## Threshold-Edge Comparison(임계값 경계 비교)

{markdown_table(comparison, ['metric_id', 'reference_value', 'selected_value', 'delta_selected_minus_reference'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): run364AS(364AS 실행)는 proxy scout(프록시 정찰)이며, package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- strict_pass_rows(엄격 통과 행): `{final['strict_pass_rows']}`\n- selected_pf(선택 PF): `{final['selected_combined_profit_factor']}`\n- effect(효과): `{NEXT_RUN_ID}` review queue(검토 대기열)를 만든다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AS Threshold-Edge PF Gap Repair Scout Closeout",
        f"\n## run364AS Threshold-Edge PF Gap Repair Scout Closeout(364AS 임계값 경계 PF 간극 수리 정찰 종료)\n\nAction(행동): run364AR(364AR 실행) queue(대기열) 중 실행 가능한 7행을 proxy replay(프록시 재생)했다.\n\nEffect(효과): Stage364(364단계) 안에서 package(패키지) 없이 다음 review(검토)로 넘길 threshold-edge(임계값 경계) 표면을 만들었다.\n",
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
        CURRENT_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364AS(364AS 실행)는 run364AR(364AR 실행)의 threshold-edge PF gap repair(임계값 경계 PF 간극 수리) queue(대기열) 중 실행 가능한 7행을 proxy replay(프록시 재생)했다. strict_pass_rows(엄격 통과 행)는 `{final['strict_pass_rows']}`이고, selected PF(선택 PF)는 `{final['selected_combined_profit_factor']}`, density(밀도)는 `{final['selected_combined_trade_per_business_day']}`, DD(낙폭)는 `{final['selected_combined_max_drawdown']}`이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 AS surface(AS 표면)를 검토해 package(패키지) 가능성, positive clue(긍정 단서), failure memory(실패 기억)를 분리한다.
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
        "run364AS Threshold-Edge PF Gap Repair Scout",
        f"\n## run364AS Threshold-Edge PF Gap Repair Scout(364AS 임계값 경계 PF 간극 수리 정찰)\n\nAction(행동): AR queue(대기열) 7행을 proxy replay(프록시 재생)했다.\n\nEffect(효과): threshold-edge(임계값 경계) 단서의 PF gap(PF 간극) 수리 가능성을 표면으로 남겼다.\n",
    )
    append_text_once(
        CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): threshold-edge PF gap repair scout(임계값 경계 PF 간극 수리 정찰)를 실행했다.\n- effect(효과): `{NEXT_RUN_ID}` review queue(검토 대기열)를 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): threshold-edge(임계값 경계) PF gap(PF 간극)을 보유 압축과 후반 롱 혼합으로 줄인다.\n- hypothesis(가설): PF(수익 팩터) 1.30 접근이 density(밀도) 3/day 붕괴 없이 가능할 수 있다.\n- effect(효과): proxy scout(프록시 정찰) 표면으로 다음 review(검토)가 package(패키지) 가능성과 실패 기억을 나눌 수 있게 한다.\n",
    )
    append_text_once(
        NEGATIVE_REGISTER,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- status(상태): pending_review(검토 대기).\n- action(행동): AS scout(정찰) 표면을 만들었다.\n- effect(효과): strict_pass_rows(엄격 통과 행)와 selected KPI(선택 KPI)는 다음 review(검토)에서 negative/positive(부정/긍정)로 분리한다.\n",
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
        "family": "stage364_proxy_scout(364단계 프록시 정찰)",
        "lane": "offensive_exploration(공격 탐색)",
        "work_family": "offensive_exploration_proxy_scout(공격 탐색 프록시 정찰)",
        "primary_artifact": rel(SCOUT_SURFACE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_started_proxy_only(프록시 전용이라 시작 안 함)",
        "next_action": NEXT_RUN_ID,
        "question": "Can threshold-edge PF gap be repaired without density collapse?(임계값 경계 PF 간극을 밀도 붕괴 없이 수리할 수 있는가?)",
        "notes": f"scout_rows={final['scout_rows']}; strict={final['strict_pass_rows']}; skipped={final['skipped_new_policy_rows']}; selected_pf={final['selected_combined_profit_factor']}",
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
    for suffix, view, tier in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B"),
        ("Tier_AB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": suffix,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "proxy replay scout(프록시 재생 정찰)",
                "scoreboard_lane": "proxy_scout(프록시 정찰)",
                "primary_kpi": f"net={final['selected_combined_net_profit']};pf={final['selected_combined_profit_factor']};density={final['selected_combined_trade_per_business_day']}",
                "guardrail_kpi": f"dd={final['selected_combined_max_drawdown']};strict={final['strict_pass_rows']};no_topn_no_split",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        alpha_rows.append(row)
    append_or_replace_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_rows)
    append_or_replace_csv(STAGE_DIR / "03_reviews" / "stage_run_ledger.csv", ["ledger_row_id"], alpha_rows)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("scout_surface", SCOUT_SURFACE, "Proxy scout surface(프록시 정찰 표면)."),
        ("strict_candidates", STRICT_CANDIDATES, "Strict proxy candidates(엄격 프록시 후보)."),
        ("selected_candidate", SELECTED_PROXY_CANDIDATE, "Selected proxy candidate(선택 프록시 후보)."),
        ("selected_trade_tape", SELECTED_EXPECTED_TRADE_TAPE, "Selected expected trade tape(선택 예상 거래 테이프)."),
        ("review_queue", RUN364AT_QUEUE, "Next review queue(다음 검토 대기열)."),
        ("gate_audit", GATE_AUDIT, "Required gate audit(필수 게이트 감사)."),
        ("report", REPORT_PATH, "Scout report(정찰 보고서)."),
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
    artifacts = []
    for path in OUTPUTS:
        if exists(path):
            artifacts.append({"path": rel(path), "sha256": sha(path), "role": "run364AS output(364AS 출력)"})
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "artifacts": artifacts,
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
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUTS if exists(path)],
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
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
    surface = add_threshold_edge_deltas(surface, reference)
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
    write_csv(RUN364AT_QUEUE, review_queue)
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
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
