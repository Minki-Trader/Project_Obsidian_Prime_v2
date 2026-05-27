from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import materialize_pair_prediction_tape_and_surface_attribution as dj  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = dj.STAGE_ID
RUN_NUMBER = "run337DK"
RUN_ID = "run337DK_review_pair_prediction_tape_surface_attribution_without_db_v1"
PARENT_RUN_ID = dj.RUN_ID
NEXT_RUN_ID = "run337DL_design_prediction_surface_validation_edge_repair_without_db_v1"
STATUS = "completed_stage337DK_prediction_tape_review_surface_and_validation_blocks_release"
JUDGMENT = "frozen_replay_valid_but_validation_edge_and_surface_isolation_block_release"
DECISION = "stage337DK_open_run337DL_design_prediction_surface_validation_edge_repair"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DK_pair_prediction_tape_surface_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dj.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dj.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DK_pair_prediction_tape_surface_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DK_pair_prediction_tape_surface_review.md"
SELECTED_STATUS = dj.SELECTED_STATUS
STAGE_BRIEF = dj.STAGE_BRIEF
WORKSPACE_STATE = dj.WORKSPACE_STATE
CURRENT_STATE = dj.CURRENT_STATE
CHANGELOG = dj.CHANGELOG
RUN_REGISTRY = dj.RUN_REGISTRY
ALPHA_LEDGER = dj.ALPHA_LEDGER
ARTIFACT_REGISTRY = dj.ARTIFACT_REGISTRY
STAGE_LEDGER = dj.STAGE_LEDGER

DJ_FINAL = dj.FINAL_DECISION
DJ_GATES = dj.REQUIRED_GATE_AUDIT
DJ_TAPE_MANIFEST = dj.TAPE_MANIFEST
DJ_PAIR_TAPE = dj.PAIR_TAPE
DJ_PAIR_SCORECARD = dj.PAIR_SCORECARD
DJ_REPLAY_PARITY = dj.REPLAY_PARITY
DJ_SLICE_ATTRIBUTION = dj.SLICE_ATTRIBUTION
DJ_CURVE_REVIEW = dj.CURVE_POCKET_REVIEW
DJ_SURFACE_AUDIT = dj.SURFACE_AUDIT
DJ_RELEASE_BLOCKERS = dj.RELEASE_BLOCKERS
DJ_FIREWALL = dj.FIREWALL_AUDIT
DJ_DK_QUEUE = dj.DK_QUEUE

REPLAY_REVIEW = RUN_DIR / "replay_identity_review.csv"
CURVE_REVIEW = RUN_DIR / "prediction_curve_release_review.csv"
SLICE_BLOCKERS = RUN_DIR / "prediction_slice_blocker_review.csv"
SURFACE_REVIEW = RUN_DIR / "surface_release_blocker_review.csv"
FAILURE_MEMORY = RUN_DIR / "prediction_surface_failure_memory.csv"
DL_QUEUE = RUN_DIR / "run337DL_design_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DJ_FINAL,
    DJ_GATES,
    DJ_TAPE_MANIFEST,
    DJ_PAIR_TAPE,
    DJ_PAIR_SCORECARD,
    DJ_REPLAY_PARITY,
    DJ_SLICE_ATTRIBUTION,
    DJ_CURVE_REVIEW,
    DJ_SURFACE_AUDIT,
    DJ_RELEASE_BLOCKERS,
    DJ_FIREWALL,
    DJ_DK_QUEUE,
)
OUTPUT_FILES = (
    REPLAY_REVIEW,
    CURVE_REVIEW,
    SLICE_BLOCKERS,
    SURFACE_REVIEW,
    FAILURE_MEMORY,
    DL_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

REPLAY_COLUMNS = ("review_id", "rows", "failed_rows", "max_net_abs_diff", "max_pf_abs_diff", "review_status", "effect", "claim_boundary")
CURVE_COLUMNS = (
    "review_id",
    "rows",
    "validation_pf_below_1p05_rows",
    "oos_positive_validation_thin_rows",
    "release_candidate_rows",
    "best_validation_pf",
    "best_oos_pf",
    "review_status",
    "effect",
    "claim_boundary",
)
SLICE_COLUMNS = (
    "pair_id",
    "slice_axis",
    "slice_value",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_trades",
    "validation_net",
    "validation_pf",
    "validation_concentration",
    "oos_trades",
    "oos_net",
    "oos_pf",
    "oos_concentration",
    "slice_review_status",
    "effect",
    "claim_boundary",
)
SURFACE_COLUMNS = (
    "review_id",
    "rows",
    "surface_watch_rows",
    "surface_clear_rows",
    "max_gap",
    "review_status",
    "effect",
    "claim_boundary",
)
MEMORY_COLUMNS = (
    "memory_id",
    "evidence_source",
    "observed_pattern",
    "interpretation",
    "repair_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def summarize_inputs() -> dict[str, Any]:
    final = read_json(DJ_FINAL)
    gates = read_csv(DJ_GATES)
    parity = read_csv(DJ_REPLAY_PARITY)
    curve = read_csv(DJ_CURVE_REVIEW)
    surface = read_csv(DJ_SURFACE_AUDIT)
    blockers = read_csv(DJ_RELEASE_BLOCKERS)
    firewall = read_csv(DJ_FIREWALL)
    failed_parity = [row for row in parity if row.get("status") != "passed_replay_parity"]
    failed_firewall = [row for row in firewall if row.get("status") != "passed"]
    validation_blocks = sum(1 for row in curve if as_float(row.get("validation_pf")) < 1.05)
    oos_thin = sum(1 for row in curve if row.get("review_status") == "oos_positive_validation_thin_block")
    release_rows = sum(1 for row in curve if row.get("review_status") == "validation_floor_pass_review_required")
    surface_watch = sum(1 for row in surface if row.get("surface_status") == "isolated_oos_surface_watch")
    return {
        "final": final,
        "gates": gates,
        "parity": parity,
        "curve": curve,
        "surface": surface,
        "blockers": blockers,
        "firewall": firewall,
        "dj_failed_gates": [row for row in gates if row.get("status") != "passed"],
        "failed_parity": failed_parity,
        "failed_firewall": failed_firewall,
        "validation_blocks": validation_blocks,
        "oos_thin": oos_thin,
        "release_rows": release_rows,
        "surface_watch": surface_watch,
        "best_validation_pf": max((as_float(row.get("validation_pf")) for row in curve), default=0.0),
        "best_oos_pf": max((as_float(row.get("oos_pf")) for row in curve), default=0.0),
        "max_surface_gap": max((as_float(row.get("oos_minus_validation_gap_max")) for row in surface), default=0.0),
    }


def build_replay_review(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    parity = summary["parity"]
    return [
        {
            "review_id": "prediction_tape_replay_identity",
            "rows": len(parity),
            "failed_rows": len(summary["failed_parity"]),
            "max_net_abs_diff": max((as_float(row.get("net_abs_diff")) for row in parity), default=0.0),
            "max_pf_abs_diff": max((as_float(row.get("pf_abs_diff")) for row in parity), default=0.0),
            "review_status": "passed_replay_identity" if not summary["failed_parity"] else "failed_replay_identity",
            "effect": "proves frozen replay can be interpreted(고정 리플레이 해석 가능성 증명)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_curve_review(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "review_id": "prediction_curve_release_review",
            "rows": len(summary["curve"]),
            "validation_pf_below_1p05_rows": summary["validation_blocks"],
            "oos_positive_validation_thin_rows": summary["oos_thin"],
            "release_candidate_rows": summary["release_rows"],
            "best_validation_pf": summary["best_validation_pf"],
            "best_oos_pf": summary["best_oos_pf"],
            "review_status": "release_blocked_validation_edge" if summary["release_rows"] == 0 else "review_release_candidate_exists",
            "effect": "keeps validation survival separate from OOS pocket(검증 생존과 OOS 포켓을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_slice_review() -> list[dict[str, Any]]:
    frame = pd.read_csv(io_path(DJ_SLICE_ATTRIBUTION))
    by_key: dict[tuple[str, str, str], dict[str, Mapping[str, Any]]] = {}
    for row in frame.to_dict("records"):
        key = (str(row["pair_id"]), str(row["slice_axis"]), str(row["slice_value"]))
        by_key.setdefault(key, {})[str(row["split"])] = row
    rows: list[dict[str, Any]] = []
    for (pair_id, axis, value), splits in sorted(by_key.items()):
        validation = splits.get("validation", {})
        oos = splits.get("oos", {})
        val_pf = as_float(validation.get("profit_factor"))
        oos_pf = as_float(oos.get("profit_factor"))
        val_net = as_float(validation.get("net_after_cost"))
        oos_net = as_float(oos.get("net_after_cost"))
        val_trades = as_int(validation.get("trade_count"))
        oos_trades = as_int(oos.get("trade_count"))
        val_conc = as_float(validation.get("concentration_share"))
        oos_conc = as_float(oos.get("concentration_share"))
        if val_trades < 50 or oos_trades < 50:
            status = "thin_slice_not_release_evidence"
        elif val_pf < 1.0 and oos_pf >= 1.10 and oos_net > 0:
            status = "oos_positive_validation_weak_slice_block"
        elif oos_conc >= 0.35 and oos_pf >= 1.10 and val_pf < 1.05:
            status = "oos_concentrated_validation_thin_slice_block"
        else:
            status = "slice_no_release_flag"
        first = validation or oos
        rows.append(
            {
                "pair_id": pair_id,
                "slice_axis": axis,
                "slice_value": value,
                "cost_policy_id": first.get("cost_policy_id", ""),
                "feature_set_id": first.get("feature_set_id", ""),
                "model_config_id": first.get("model_config_id", ""),
                "validation_trades": val_trades,
                "validation_net": val_net,
                "validation_pf": val_pf,
                "validation_concentration": val_conc,
                "oos_trades": oos_trades,
                "oos_net": oos_net,
                "oos_pf": oos_pf,
                "oos_concentration": oos_conc,
                "slice_review_status": status,
                "effect": "reviews non-oracle prediction slice stability(비오라클 예측 슬라이스 안정성 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_surface_review(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "review_id": "prediction_surface_release_review",
            "rows": len(summary["surface"]),
            "surface_watch_rows": summary["surface_watch"],
            "surface_clear_rows": len(summary["surface"]) - summary["surface_watch"],
            "max_gap": summary["max_surface_gap"],
            "review_status": "surface_isolation_blocks_release" if summary["surface_watch"] else "surface_watch_clear",
            "effect": "prevents surface-mined OOS from becoming selection(표면 채굴 OOS가 선택이 되는 것을 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_failure_memory(summary: Mapping[str, Any], slice_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    slice_blocks = sum(1 for row in slice_rows if str(row.get("slice_review_status", "")).endswith("_block"))
    thin_slices = sum(1 for row in slice_rows if row.get("slice_review_status") == "thin_slice_not_release_evidence")
    return [
        {
            "memory_id": "replay_identity_clear",
            "evidence_source": rel(DJ_REPLAY_PARITY),
            "observed_pattern": f"failed_replay_rows={len(summary['failed_parity'])}",
            "interpretation": "frozen replay is valid evidence(고정 리플레이는 유효 근거)",
            "repair_use": "use replay tape for next design(다음 설계에 리플레이 테이프 사용)",
            "forbidden_use": "do not call replay a release(리플레이를 해제로 부르지 않음)",
            "effect": "separates identity pass from trading pass(정체성 통과와 거래 통과 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "validation_edge_broad_block",
            "evidence_source": rel(DJ_CURVE_REVIEW),
            "observed_pattern": f"validation_pf_below_1p05_rows={summary['validation_blocks']};release_rows={summary['release_rows']};best_validation_pf={summary['best_validation_pf']}",
            "interpretation": "validation edge is broadly insufficient(검증 우위가 넓게 부족)",
            "repair_use": "design validation-edge objective/label repair(검증 우위 목표/라벨 수리 설계)",
            "forbidden_use": "do not choose high OOS pair(OOS 높은 쌍 선택 금지)",
            "effect": "moves from release to repair(해제에서 수리로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "oos_surface_isolation_block",
            "evidence_source": rel(DJ_SURFACE_AUDIT),
            "observed_pattern": f"surface_watch_rows={summary['surface_watch']};max_gap={summary['max_surface_gap']}",
            "interpretation": "OOS edge remains surface-isolated(OOS 우위가 표면 고립으로 남음)",
            "repair_use": "design deconcentration and smoother objective(탈집중과 더 매끄러운 목표 설계)",
            "forbidden_use": "do not cherry-pick cost/model surface(비용/모델 표면 골라잡기 금지)",
            "effect": "blocks overfit surface mining(과적합 표면 채굴 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "slice_evidence_not_release_ready",
            "evidence_source": rel(DJ_SLICE_ATTRIBUTION),
            "observed_pattern": f"slice_blocks={slice_blocks};thin_slices={thin_slices}",
            "interpretation": "slice evidence needs repair review before any MT5(슬라이스 근거는 MT5 전 수리 검토 필요)",
            "repair_use": "materialize defensive/aggressive balanced design(방어/공격 균형 설계 물질화)",
            "forbidden_use": "do not use slice winners as candidates(슬라이스 승자를 후보로 쓰지 않음)",
            "effect": "keeps slice analysis diagnostic(슬라이스 분석을 진단으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DL_design_validation_edge_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design validation-edge objective repair without OOS selection(OOS 선택 없이 검증 우위 목표 수리 설계)",
            "required_inputs": f"{rel(CURVE_REVIEW)};{rel(FAILURE_MEMORY)}",
            "required_outputs": "validation_edge_repair_contract.csv(검증 우위 수리 계약)",
            "blocked_if_missing": "prediction curve review(예측 곡선 검토)",
            "forbidden_action": "no threshold tuning or pair selection(임계값 튜닝/쌍 선택 금지)",
            "effect": "targets broad validation weakness(넓은 검증 약점을 목표화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DL_design_surface_deconcentration_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design surface deconcentration repair across cost/model/feature axes(비용/모델/피처 축 표면 탈집중 수리 설계)",
            "required_inputs": f"{rel(SURFACE_REVIEW)};{rel(DJ_SURFACE_AUDIT)}",
            "required_outputs": "surface_deconcentration_repair_contract.csv(표면 탈집중 수리 계약)",
            "blocked_if_missing": "surface review(표면 검토)",
            "forbidden_action": "no cost/model cherry-pick(비용/모델 골라잡기 금지)",
            "effect": "reduces surface mining risk(표면 채굴 위험 감소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DL_design_balanced_defensive_aggressive_packet",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design balanced defensive/aggressive/repair packet(방어/공격/수리 균형 묶음 설계)",
            "required_inputs": f"{rel(FAILURE_MEMORY)};{rel(SLICE_BLOCKERS)}",
            "required_outputs": "balanced_repair_attack_design_queue.csv(균형 수리/공격 설계 대기열)",
            "blocked_if_missing": "failure memory and slice blockers(실패 기억과 슬라이스 차단)",
            "forbidden_action": "no lookahead, no validation/OOS retune(미래참조/검증·OOS 재튜닝 금지)",
            "effect": "keeps research moving toward strong ONNX without repeating lookahead(미래참조 반복 없이 강한 ONNX로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DL_preserve_runtime_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve no-MT5/no-release firewall(무MT5/무해제 방화벽 보존)",
            "required_inputs": rel(DJ_RELEASE_BLOCKERS),
            "required_outputs": "runtime_firewall_contract.csv(런타임 방화벽 계약)",
            "blocked_if_missing": "release blocker update(해제 차단 갱신)",
            "forbidden_action": "no MT5 package or Forward claim(MT5 패키지/전진 주장 금지)",
            "effect": "keeps runtime authority closed(런타임 권위 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DJ inputs exist(필수 DJ 입력 존재)"),
        ("parent_dj_gates_passed", final["dj_failed_gate_rows"] == 0, str(final["dj_failed_gate_rows"]), "0", "DJ materialization usable(DJ 물질화 사용 가능)"),
        ("parent_next_action_matches", final["dj_next_action"] == RUN_ID, str(final["dj_next_action"]), RUN_ID, "continues DJ queue(DJ 대기열을 이어감)"),
        ("replay_identity_passed", final["replay_failed_rows"] == 0, str(final["replay_failed_rows"]), "0", "replay identity passed(리플레이 정체성 통과)"),
        ("validation_block_named", final["validation_pf_below_1p05_rows"] == 18, str(final["validation_pf_below_1p05_rows"]), "18", "all pairs fail validation PF floor(모든 쌍 검증 PF 하한 실패)"),
        ("release_rows_zero", final["release_candidate_rows"] == 0, str(final["release_candidate_rows"]), "0", "no release candidates(해제 후보 없음)"),
        ("surface_isolation_named", final["surface_watch_rows"] > 0, str(final["surface_watch_rows"]), ">0", "surface isolation named(표면 고립 명명)"),
        ("failure_memory_materialized", final["failure_memory_rows"] >= 4, str(final["failure_memory_rows"]), ">=4", "failure memory exists(실패 기억 존재)"),
        ("dl_queue_materialized", final["queue_rows"] >= 4, str(final["queue_rows"]), ">=4", "DL design queue exists(DL 설계 대기열 존재)"),
        (
            "no_release_claim",
            final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "claim boundary preserved(주장 경계 보존)",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits DJ replay tape timestamps(DJ 리플레이 테이프 시각 상속)",
        "sample_scope": "review only, no new predictions(검토 전용, 새 예측 없음)",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "prediction tape already materialized; review reads only(예측 테이프는 이미 물질화, 검토는 읽기 전용)",
        "split_boundary": "train/validation/OOS read-only(학습/검증/OOS 읽기 전용)",
        "leakage_risk": "using OOS pocket as design winner(OOS 포켓을 설계 승자로 사용)",
        "data_hash_or_identity": {"dj_final": sha256_file(DJ_FINAL), "curve": sha256_file(DJ_CURVE_REVIEW)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "frozen DE prediction replay reviewed(고정 DE 예측 리플레이 검토)",
        "target_and_label": "stage1/stage2 replay, no new labels(1/2단계 리플레이, 새 라벨 없음)",
        "split_method": "inherited chronological split(상속 시간순 분할)",
        "selection_metric": "none(없음)",
        "secondary_metrics": "validation PF floor, OOS quarantine, surface isolation(검증 PF 하한/OOS 격리/표면 고립)",
        "threshold_policy": "unchanged(변경 없음)",
        "overfit_risk": "surface isolated OOS edge(표면 고립 OOS 우위)",
        "calibration_risk": "model scores not calibrated trading probabilities(모델 점수는 보정된 거래 확률 아님)",
        "comparison_baseline": rel(DJ_PAIR_SCORECARD),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"release_rows={final['release_candidate_rows']};surface_watch={final['surface_watch_rows']}",
        "comparison_baseline": rel(DJ_CURVE_REVIEW),
        "likely_drivers": "broad validation weakness and OOS surface isolation(넓은 검증 약점과 OOS 표면 고립)",
        "segment_checks": f"slice_block_rows={final['slice_block_rows']};thin_slice_rows={final['thin_slice_rows']}",
        "trade_shape": "prediction replay trade shape reviewed through DJ artifacts(DJ 산출물로 예측 리플레이 거래 형태 검토)",
        "alternative_explanations": "regime luck, target mismatch, model complexity pocket(국면 운/목표 불일치/모델 복잡도 포켓)",
        "attribution_confidence": "high_for_release_block_medium_for_cause(해제 차단은 높음, 원인 확정은 중간)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "replay parity, curve review, slice blockers, surface blockers(리플레이 동등성/곡선 검토/슬라이스 차단/표면 차단)",
        "evidence_missing": "DL repair design and later materialized repair inputs(DL 수리 설계와 이후 수리 입력)",
        "judgment_label": "review_blocks_release",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "고정 리플레이는 믿을 수 있지만, 검증 성과가 넓게 약해서 해제보다 수리 설계가 맞습니다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifact_paths) + paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_review_outputs_with_tracked_report(무시된 검토 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DK Pair Prediction Tape Surface Review(쌍 예측 테이프 표면 검토)

## Conclusion(결론)

run337DK(337DK 실행)는 DJ prediction tape(예측 테이프)를 review(검토)했다. Replay identity(리플레이 정체성)는 통과했다. 즉 frozen model replay(고정 모델 리플레이)는 해석 가능한 근거다.

하지만 validation PF below 1.05(검증 PF 1.05 미만)가 `{final["validation_pf_below_1p05_rows"]}`개, release candidate(해제 후보)가 `{final["release_candidate_rows"]}`개, surface isolation watch(표면 고립 감시)가 `{final["surface_watch_rows"]}`개다. 따라서 release(해제), MT5 probe(MT5 탐침), candidate selection(후보 선택)은 차단한다.

Effect(효과): 다음 run337DL(337DL 실행)은 validation-edge repair(검증 우위 수리), surface deconcentration(표면 탈집중), defensive/aggressive/repair balance(방어/공격/수리 균형)를 설계한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- replay_failed_rows(리플레이 실패 행): `{final["replay_failed_rows"]}`
- validation_pf_below_1p05_rows(검증 PF 1.05 미만 행): `{final["validation_pf_below_1p05_rows"]}`
- oos_positive_validation_thin_rows(OOS 양호/검증 얇음 행): `{final["oos_positive_validation_thin_rows"]}`
- surface_watch_rows(표면 감시 행): `{final["surface_watch_rows"]}`
- slice_block_rows(슬라이스 차단 행): `{final["slice_block_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DK

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 고정 리플레이는 유효하지만 검증 우위와 표면 고립이 release(해제)를 막아 DL 수리 설계를 연다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(FAILURE_MEMORY)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337DK focus complete: pair prediction tape surface review(쌍 예측 테이프 표면 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DL(337DL 실행)에서 validation-edge/surface deconcentration/balanced repair(검증 우위/표면 탈집중/균형 수리) 설계를 연다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DK focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337DK(337DK 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 고정 리플레이는 유효하지만 validation edge/surface isolation(검증 우위/표면 고립)이 해제를 막아 수리 설계를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DJ(337DJ"
    if "## Stage337 run337DK(337DK 실행)" not in current_text:
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `not_run_dk_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 prediction surface validation-edge repair design(예측 표면 검증 우위 수리 설계)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DK(337DK 실행) reviewed pair prediction tape surface attribution(쌍 예측 테이프 표면 귀속 검토). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DK(337DK 실행) reviewed pair prediction"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DK reviewed pair prediction tape surface attribution(쌍 예측 테이프 표면 귀속 검토) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DK reviewed pair prediction"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "pair_prediction_tape_surface_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"validation_blocks={final['validation_pf_below_1p05_rows']};release_rows={final['release_candidate_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__prediction_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "prediction_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "prediction_replay_curve_surface_review",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"release_rows={final['release_candidate_rows']};surface_watch={final['surface_watch_rows']}",
        "guardrail_kpi": "no_selection;no_mt5;replay_identity",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__prediction_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "evidence_scope": "DJ prediction tape reviewed",
        "kpi_scope": "replay_identity_validation_edge_surface_isolation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__prediction_review",
        "family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "question": "does frozen prediction tape release or require repair design",
        "metric_scope": "replay_curve_surface_slice_failure_memory",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]
    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    summary = summarize_inputs()
    replay_rows = build_replay_review(summary)
    curve_rows = build_curve_review(summary)
    slice_rows = build_slice_review()
    surface_rows = build_surface_review(summary)
    memory_rows = build_failure_memory(summary, slice_rows)
    queue_rows = build_queue()
    artifacts: list[Path] = [
        write_csv(REPLAY_REVIEW, REPLAY_COLUMNS, replay_rows),
        write_csv(CURVE_REVIEW, CURVE_COLUMNS, curve_rows),
        write_csv(SLICE_BLOCKERS, SLICE_COLUMNS, slice_rows),
        write_csv(SURFACE_REVIEW, SURFACE_COLUMNS, surface_rows),
        write_csv(FAILURE_MEMORY, MEMORY_COLUMNS, memory_rows),
        write_csv(DL_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    slice_block_rows = sum(1 for row in slice_rows if str(row.get("slice_review_status", "")).endswith("_block"))
    thin_slice_rows = sum(1 for row in slice_rows if row.get("slice_review_status") == "thin_slice_not_release_evidence")
    dj_final: Mapping[str, Any] = summary["final"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dj_next_action": dj_final.get("next_action", ""),
        "dj_failed_gate_rows": len(summary["dj_failed_gates"]),
        "missing_inputs": len(missing),
        "replay_failed_rows": len(summary["failed_parity"]),
        "validation_pf_below_1p05_rows": summary["validation_blocks"],
        "oos_positive_validation_thin_rows": summary["oos_thin"],
        "release_candidate_rows": summary["release_rows"],
        "best_validation_pf": summary["best_validation_pf"],
        "best_oos_pf": summary["best_oos_pf"],
        "surface_watch_rows": summary["surface_watch"],
        "max_surface_gap": summary["max_surface_gap"],
        "slice_review_rows": len(slice_rows),
        "slice_block_rows": slice_block_rows,
        "thin_slice_rows": thin_slice_rows,
        "failure_memory_rows": len(memory_rows),
        "queue_rows": len(queue_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
