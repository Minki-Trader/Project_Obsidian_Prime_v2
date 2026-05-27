from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import materialize_validation_pocket_cost_shape_repair_inputs as dh  # noqa: E402
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
STAGE_ID = dh.STAGE_ID
RUN_NUMBER = "run337DI"
RUN_ID = "run337DI_review_validation_pocket_cost_shape_repair_inputs_without_db_v1"
PARENT_RUN_ID = dh.RUN_ID
NEXT_RUN_ID = "run337DJ_materialize_pair_prediction_tape_and_surface_attribution_without_db_v1"
STATUS = "completed_stage337DI_validation_pocket_inputs_review_surface_isolation_blocks_release"
JUDGMENT = "inputs_usable_but_label_oracle_and_isolated_oos_surface_require_prediction_tape"
DECISION = "stage337DI_open_run337DJ_materialize_pair_prediction_tape_and_surface_attribution"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DI_validation_pocket_input_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dh.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DI_validation_pocket_cost_shape_repair_inputs_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DI_validation_pocket_cost_shape_repair_inputs_review.md"
SELECTED_STATUS = dh.SELECTED_STATUS
STAGE_BRIEF = dh.STAGE_BRIEF
WORKSPACE_STATE = dh.WORKSPACE_STATE
CURRENT_STATE = dh.CURRENT_STATE
CHANGELOG = dh.CHANGELOG
RUN_REGISTRY = dh.RUN_REGISTRY
ALPHA_LEDGER = dh.ALPHA_LEDGER
ARTIFACT_REGISTRY = dh.ARTIFACT_REGISTRY
STAGE_LEDGER = dh.STAGE_LEDGER

DH_FINAL = dh.FINAL_DECISION
DH_GATES = dh.REQUIRED_GATE_AUDIT
DH_FLOOR_FRAME = dh.FLOOR_FRAME
DH_FLOOR_AUDIT = dh.FLOOR_AUDIT
DH_SLICE_FRAME = dh.SLICE_FRAME
DH_SLICE_POCKET_AUDIT = dh.SLICE_POCKET_AUDIT
DH_OOS_QUARANTINE = dh.OOS_QUARANTINE
DH_FORBIDDEN_SELECTION = dh.FORBIDDEN_SELECTION
DH_PAIR_SURFACE = dh.PAIR_SURFACE
DH_ISOLATED_FLAGS = dh.ISOLATED_FLAGS
DH_DI_QUEUE = dh.DI_QUEUE

MATERIALIZATION_REVIEW = RUN_DIR / "materialization_integrity_review.csv"
FLOOR_ORACLE_REVIEW = RUN_DIR / "floor_label_oracle_review.csv"
SLICE_REVIEW = RUN_DIR / "slice_pocket_review.csv"
SURFACE_REVIEW = RUN_DIR / "oos_quarantine_surface_review.csv"
DJ_QUEUE = RUN_DIR / "run337DJ_repair_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DH_FINAL,
    DH_GATES,
    DH_FLOOR_FRAME,
    DH_FLOOR_AUDIT,
    DH_SLICE_FRAME,
    DH_SLICE_POCKET_AUDIT,
    DH_OOS_QUARANTINE,
    DH_FORBIDDEN_SELECTION,
    DH_PAIR_SURFACE,
    DH_ISOLATED_FLAGS,
    DH_DI_QUEUE,
)
OUTPUT_FILES = (
    MATERIALIZATION_REVIEW,
    FLOOR_ORACLE_REVIEW,
    SLICE_REVIEW,
    SURFACE_REVIEW,
    DJ_QUEUE,
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

REVIEW_COLUMNS = ("review_id", "status", "observed", "expected", "effect", "claim_boundary")
FLOOR_COLUMNS = (
    "split",
    "cost_policy_id",
    "profit_factor",
    "trade_count",
    "net_after_cost",
    "review_status",
    "interpretation",
    "effect",
    "claim_boundary",
)
SLICE_COLUMNS = (
    "pocket_status",
    "rows",
    "review_status",
    "interpretation",
    "effect",
    "claim_boundary",
)
SURFACE_COLUMNS = (
    "review_id",
    "rows",
    "review_status",
    "interpretation",
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
    final = read_json(DH_FINAL)
    gates = read_csv(DH_GATES)
    floor = read_csv(DH_FLOOR_AUDIT)
    slice_audit = read_csv(DH_SLICE_POCKET_AUDIT)
    quarantine = read_csv(DH_OOS_QUARANTINE)
    forbidden = read_csv(DH_FORBIDDEN_SELECTION)
    surface = read_csv(DH_PAIR_SURFACE)
    flags = read_csv(DH_ISOLATED_FLAGS)
    queue = read_csv(DH_DI_QUEUE)
    floor_oracle_rows = sum(1 for row in floor if as_float(row.get("profit_factor")) >= 900.0)
    thin_slice_rows = sum(1 for row in slice_audit if row.get("pocket_status") == "thin_slice_review_required")
    oos_only_slice_rows = sum(
        1
        for row in slice_audit
        if row.get("pocket_status") in {"oos_positive_validation_weak_slice", "validation_negative_oos_positive_slice"}
    )
    quarantined = sum(1 for row in quarantine if row.get("quarantine_status") == "quarantined_oos_positive_validation_thin")
    forbidden_failed = sum(1 for row in forbidden if row.get("status") != "passed")
    surface_watch = sum(1 for row in surface if row.get("surface_status") == "isolated_oos_surface_watch")
    return {
        "final": final,
        "gates": gates,
        "floor": floor,
        "slice_audit": slice_audit,
        "quarantine": quarantine,
        "forbidden": forbidden,
        "surface": surface,
        "flags": flags,
        "queue": queue,
        "dh_failed_gates": [row for row in gates if row.get("status") != "passed"],
        "floor_oracle_rows": floor_oracle_rows,
        "thin_slice_rows": thin_slice_rows,
        "oos_only_slice_rows": oos_only_slice_rows,
        "quarantined_pairs": quarantined,
        "forbidden_failed_rows": forbidden_failed,
        "surface_watch_rows": surface_watch,
        "isolated_flag_rows": len(flags),
    }


def build_materialization_review(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    final = summary["final"]
    rows = [
        ("floor_frame_rows", str(final.get("floor_frame_rows", 0)), ">0", as_int(final.get("floor_frame_rows")) > 0),
        ("duplicate_floor_keys", str(final.get("duplicate_floor_keys", 0)), "0", as_int(final.get("duplicate_floor_keys")) == 0),
        ("slice_frame_rows", str(final.get("slice_frame_rows", 0)), ">0", as_int(final.get("slice_frame_rows")) > 0),
        ("quarantined_pairs", str(summary["quarantined_pairs"]), str(final.get("parent_oos_positive_thin_rows", 0)), summary["quarantined_pairs"] == as_int(final.get("parent_oos_positive_thin_rows"))),
        ("forbidden_selection_audit", str(summary["forbidden_failed_rows"]), "0", summary["forbidden_failed_rows"] == 0),
    ]
    return [
        {
            "review_id": review_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": "checks DH materialization usability(DH 물질화 사용 가능성 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for review_id, observed, expected, passed in rows
    ]


def build_floor_oracle_review(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in summary["floor"]:
        pf = as_float(row.get("profit_factor"))
        status = "label_shape_only_not_kpi" if pf >= 900.0 else "ordinary_floor_summary"
        rows.append(
            {
                "split": row.get("split", ""),
                "cost_policy_id": row.get("cost_policy_id", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "net_after_cost": row.get("net_after_cost", ""),
                "review_status": status,
                "interpretation": "PF comes from label/action frame, not model predictions(PF는 모델 예측이 아니라 라벨/행동 프레임에서 옴)",
                "effect": "prevents label oracle from becoming KPI claim(라벨 오라클이 KPI 주장으로 바뀌지 않게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_slice_review(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    counts: dict[str, int] = {}
    for row in summary["slice_audit"]:
        counts[row.get("pocket_status", "")] = counts.get(row.get("pocket_status", ""), 0) + 1
    rows: list[dict[str, str]] = []
    for status, count in sorted(counts.items()):
        if status == "thin_slice_review_required":
            review_status = "thin_slices_require_review"
            interpretation = "many slices are too small for release evidence(많은 슬라이스가 해제 근거로는 얇음)"
        elif status in {"oos_positive_validation_weak_slice", "validation_negative_oos_positive_slice"}:
            review_status = "oos_only_slice_block"
            interpretation = "slice-level OOS-only pocket blocks release(슬라이스 단위 OOS 전용 포켓이 해제를 막음)"
        else:
            review_status = "slice_no_oos_only_flag"
            interpretation = "no OOS-only flag at this slice status(이 슬라이스 상태에는 OOS 전용 표시 없음)"
        rows.append(
            {
                "pocket_status": status,
                "rows": count,
                "review_status": review_status,
                "interpretation": interpretation,
                "effect": "summarizes slice pocket evidence(슬라이스 포켓 근거 요약)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_surface_review(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "review_id": "oos_quarantine_review",
            "rows": summary["quarantined_pairs"],
            "review_status": "quarantine_passed_blocks_selection",
            "interpretation": "all OOS-positive validation-thin pairs remain quarantined(모든 OOS 양호/검증 얇음 쌍이 격리 유지)",
            "effect": "prevents OOS winner selection(OOS 승자 선택 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "pair_surface_review",
            "rows": summary["surface_watch_rows"],
            "review_status": "surface_isolation_blocks_release" if summary["surface_watch_rows"] else "surface_watch_clear",
            "interpretation": "most surfaces are isolated OOS watches(대부분 표면이 고립 OOS 감시)",
            "effect": "requires prediction-tape attribution before training or MT5(학습/MT5 전 예측 테이프 귀속 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "isolated_pair_flags",
            "rows": summary["isolated_flag_rows"],
            "review_status": "isolated_pair_flags_block_release" if summary["isolated_flag_rows"] else "no_isolated_pair_flags",
            "interpretation": "pair-level OOS pockets remain isolated(쌍 단위 OOS 포켓이 고립 유지)",
            "effect": "moves next work to frozen prediction replay(다음 작업을 고정 예측 리플레이로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DJ_materialize_frozen_pair_prediction_tape",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize row-level prediction tape from frozen DE models(고정 DE 모델에서 행 단위 예측 테이프 물질화)",
            "required_inputs": f"{rel(dh.FLOOR_FRAME)};{rel(dh.DE_PAIR)};{rel(STAGE_DIR / '02_runs' / 'run337DE' / 'trained_model_manifest.csv')}",
            "required_outputs": "pair_prediction_tape.parquet;prediction_tape_manifest.json(쌍 예측 테이프/목록)",
            "blocked_if_missing": "model artifacts or floor frame(모델 산출물 또는 하한 프레임)",
            "forbidden_action": "no new training, no threshold tuning(새 학습/임계값 튜닝 금지)",
            "effect": "replaces label-oracle floor with frozen model replay(라벨 오라클 하한을 고정 모델 리플레이로 대체)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DJ_materialize_prediction_slice_attribution",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "build non-oracle slice attribution from prediction tape(예측 테이프에서 비오라클 슬라이스 귀속 생성)",
            "required_inputs": "pair_prediction_tape.parquet;slice_stability_frame.csv(쌍 예측 테이프/슬라이스 안정성 프레임)",
            "required_outputs": "prediction_slice_attribution.csv;curve_pocket_review.csv(예측 슬라이스 귀속/곡선 포켓 검토)",
            "blocked_if_missing": "row-level model predictions(행 단위 모델 예측)",
            "forbidden_action": "no slice winner selection(슬라이스 승자 선택 금지)",
            "effect": "tests whether OOS pocket survives actual frozen predictions(실제 고정 예측에서 OOS 포켓이 버티는지 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DJ_materialize_surface_deconcentration_audit",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "audit pair/cost/model deconcentration(쌍/비용/모델 탈집중 감사)",
            "required_inputs": f"{rel(dh.PAIR_SURFACE)};{rel(dh.ISOLATED_FLAGS)}",
            "required_outputs": "surface_deconcentration_audit.csv;release_blocker_update.csv(표면 탈집중 감사/해제 차단 갱신)",
            "blocked_if_missing": "isolated pocket flags(고립 포켓 표시)",
            "forbidden_action": "no model-family cherry-pick(모델 계열 골라잡기 금지)",
            "effect": "keeps OOS surface mining visible(OOS 표면 채굴을 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DJ_preserve_no_release_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "carry no-release firewall into prediction replay(예측 리플레이에 해제 금지 방화벽 이월)",
            "required_inputs": f"{rel(dh.FORBIDDEN_SELECTION)};{rel(dh.OOS_QUARANTINE)}",
            "required_outputs": "prediction_replay_firewall_audit.csv(예측 리플레이 방화벽 감사)",
            "blocked_if_missing": "forbidden selection audit(금지 선택 감사)",
            "forbidden_action": "no MT5 package, no Forward/Goal claim(MT5 패키지/전진/목표 주장 금지)",
            "effect": "keeps review from becoming release(검토가 해제로 바뀌지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DH inputs exist(필수 DH 입력 존재)"),
        ("parent_dh_gates_passed", final["dh_failed_gate_rows"] == 0, str(final["dh_failed_gate_rows"]), "0", "DH materialization usable(DH 물질화 사용 가능)"),
        ("parent_next_action_matches", final["dh_next_action"] == RUN_ID, str(final["dh_next_action"]), RUN_ID, "continues declared DH queue(DH 선언 대기열을 이어감)"),
        ("floor_oracle_named", final["floor_oracle_rows"] > 0, str(final["floor_oracle_rows"]), ">0", "label oracle boundary named(라벨 오라클 경계 명명)"),
        ("quarantine_preserved", final["quarantined_pairs"] == final["parent_quarantined_pairs"], str(final["quarantined_pairs"]), str(final["parent_quarantined_pairs"]), "OOS quarantine preserved(OOS 격리 보존)"),
        ("surface_isolation_named", final["surface_watch_rows"] > 0, str(final["surface_watch_rows"]), ">0", "surface isolation named(표면 고립 명명)"),
        ("isolated_flags_named", final["isolated_flag_rows"] > 0, str(final["isolated_flag_rows"]), ">0", "pair flags named(쌍 표시 명명)"),
        ("forbidden_selection_passed", final["forbidden_failed_rows"] == 0, str(final["forbidden_failed_rows"]), "0", "forbidden actions remain blocked(금지 행동 차단 유지)"),
        ("dj_queue_materialized", final["queue_rows"] >= 4, str(final["queue_rows"]), ">=4", "DJ queue exists(DJ 대기열 존재)"),
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
        "time_axis": "inherits DH closed M5 UTC identity(DH 닫힌 M5 UTC 정체성 상속)",
        "sample_scope": "review only, no new rows created(검토 전용, 새 행 생성 없음)",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "floor audit is label-shape only, not model KPI(하한 감사는 라벨 형태 전용, 모델 KPI 아님)",
        "split_boundary": "validation/OOS read-only(검증/OOS 읽기 전용)",
        "leakage_risk": "label oracle KPI interpretation(라벨 오라클 KPI 해석)",
        "data_hash_or_identity": {"dh_final": sha256_file(DH_FINAL), "floor_audit": sha256_file(DH_FLOOR_AUDIT)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "none in DI; next requires frozen DE replay(DI에는 없음, 다음은 고정 DE 리플레이 필요)",
        "target_and_label": "DH labels reviewed as labels only(DH 라벨은 라벨로만 검토)",
        "split_method": "inherited chronological splits(상속 시간순 분할)",
        "selection_metric": "none(없음)",
        "secondary_metrics": "surface isolation, quarantine, thin slices(표면 고립/격리/얇은 슬라이스)",
        "threshold_policy": "unchanged(변경 없음)",
        "overfit_risk": "surface mining and label oracle interpretation(표면 채굴과 라벨 오라클 해석)",
        "calibration_risk": "prediction tape missing(예측 테이프 누락)",
        "comparison_baseline": rel(DH_PAIR_SURFACE),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"surface_watch_rows={final['surface_watch_rows']};isolated_flags={final['isolated_flag_rows']}",
        "comparison_baseline": rel(DH_PAIR_SURFACE),
        "likely_drivers": "OOS surface concentration, label/action oracle audit(OOS 표면 집중/라벨 행동 오라클 감사)",
        "segment_checks": f"thin_slice_rows={final['thin_slice_rows']};oos_only_slice_rows={final['oos_only_slice_rows']}",
        "trade_shape": "label-shape floor only; prediction trade shape missing(라벨 형태 하한 전용, 예측 거래 형태 누락)",
        "alternative_explanations": "model prediction may differ from label oracle(모델 예측은 라벨 오라클과 다를 수 있음)",
        "attribution_confidence": "medium_for_block_low_for_cause(차단은 중간, 원인 확정은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DH inputs, quarantine, surface, slice audits(DH 입력/격리/표면/슬라이스 감사)",
        "evidence_missing": "row-level frozen model prediction tape(행 단위 고정 모델 예측 테이프)",
        "judgment_label": "review_blocks_release",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "입력은 쓸 수 있지만, 라벨 기반 결과를 성과로 보면 안 되고 고정 모델 예측 테이프가 필요합니다.",
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
    text = f"""# Stage337 run337DI Validation Pocket Input Review(검증 포켓 입력 검토)

## Conclusion(결론)

run337DI(337DI 실행)는 DH 입력을 검토했다. 입력 자체는 usable with boundary(경계부 사용 가능)이다.

다만 floor audit(하한 감사)의 PF `999` 계열은 label/action oracle(라벨/행동 오라클)이다. 즉 model KPI(모델 성과 지표)가 아니라 label-shape diagnostic(라벨 형태 진단)이다.

또한 OOS quarantine(OOS 격리)은 `{final["quarantined_pairs"]}`개로 보존됐고, pair surface(쌍 표면)는 `{final["surface_watch_rows"]}`개가 isolated OOS surface watch(고립 OOS 표면 감시)다. 따라서 release(해제), MT5 probe(MT5 탐침), candidate selection(후보 선택)은 계속 차단한다.

Effect(효과): 다음 run337DJ(337DJ 실행)는 frozen DE models(고정 DE 모델)로 row-level prediction tape(행 단위 예측 테이프)를 물질화해, 라벨 오라클이 아닌 실제 고정 예측 기준으로 슬라이스와 표면을 다시 본다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- floor_oracle_rows(하한 오라클 행): `{final["floor_oracle_rows"]}`
- thin_slice_rows(얇은 슬라이스 행): `{final["thin_slice_rows"]}`
- oos_only_slice_rows(OOS 전용 슬라이스 행): `{final["oos_only_slice_rows"]}`
- surface_watch_rows(표면 감시 행): `{final["surface_watch_rows"]}`
- isolated_flag_rows(고립 표시 행): `{final["isolated_flag_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DI

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): DH 입력은 보존하되, 라벨 오라클과 고립 OOS 표면 때문에 고정 예측 테이프 물질화를 연다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(SURFACE_REVIEW)}`
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
        f"  Stage337 run337DI focus complete: validation pocket input review(검증 포켓 입력 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DJ(337DJ 실행)에서 frozen pair prediction tape/surface attribution(고정 쌍 예측 테이프/표면 귀속)을 물질화한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DI focus complete")
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
## Stage337 run337DI(337DI 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DH 입력은 사용 가능하지만 label oracle/surface isolation(라벨 오라클/표면 고립)이 release(해제)를 막아 frozen prediction tape(고정 예측 테이프)을 연다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DH(337DH"
    if "## Stage337 run337DI(337DI 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_di_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 frozen pair prediction tape and surface attribution(고정 쌍 예측 테이프와 표면 귀속) 물질화다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DI(337DI 실행) reviewed validation pocket repair inputs(검증 포켓 수리 입력 검토). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DI(337DI 실행) reviewed validation pocket"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DI reviewed validation pocket repair inputs(검증 포켓 수리 입력 검토) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DI reviewed validation pocket"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_pocket_cost_shape_repair_input_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"floor_oracle={final['floor_oracle_rows']};surface_watch={final['surface_watch_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "floor_oracle_surface_isolation_review",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"surface_watch={final['surface_watch_rows']};isolated_flags={final['isolated_flag_rows']}",
        "guardrail_kpi": "label_oracle_not_kpi;no_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "evidence_scope": "DH repair inputs reviewed",
        "kpi_scope": "label_oracle_surface_isolation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__input_review",
        "family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "question": "are DH inputs usable for repair, or blocked by label oracle/surface isolation",
        "metric_scope": "floor_oracle_oos_quarantine_surface_flags",
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
    materialization_rows = build_materialization_review(summary)
    floor_rows = build_floor_oracle_review(summary)
    slice_rows = build_slice_review(summary)
    surface_rows = build_surface_review(summary)
    queue_rows = build_queue()
    artifacts: list[Path] = [
        write_csv(MATERIALIZATION_REVIEW, REVIEW_COLUMNS, materialization_rows),
        write_csv(FLOOR_ORACLE_REVIEW, FLOOR_COLUMNS, floor_rows),
        write_csv(SLICE_REVIEW, SLICE_COLUMNS, slice_rows),
        write_csv(SURFACE_REVIEW, SURFACE_COLUMNS, surface_rows),
        write_csv(DJ_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    dh_final: Mapping[str, Any] = summary["final"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dh_next_action": dh_final.get("next_action", ""),
        "dh_failed_gate_rows": len(summary["dh_failed_gates"]),
        "missing_inputs": len(missing),
        "floor_oracle_rows": summary["floor_oracle_rows"],
        "thin_slice_rows": summary["thin_slice_rows"],
        "oos_only_slice_rows": summary["oos_only_slice_rows"],
        "quarantined_pairs": summary["quarantined_pairs"],
        "parent_quarantined_pairs": int(dh_final.get("quarantined_pairs", 0)),
        "forbidden_failed_rows": summary["forbidden_failed_rows"],
        "surface_watch_rows": summary["surface_watch_rows"],
        "isolated_flag_rows": summary["isolated_flag_rows"],
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
