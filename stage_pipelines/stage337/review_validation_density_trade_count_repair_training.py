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

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import train_validation_density_trade_count_repair_candidates as ee  # noqa: E402
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
STAGE_ID = ee.STAGE_ID
RUN_NUMBER = "run337EF"
RUN_ID = "run337EF_review_validation_density_trade_count_repair_training_without_db_v1"
PARENT_RUN_ID = ee.RUN_ID
NEXT_RUN_ID = "run337EG_review_proxy_survivor_attribution_package_precheck_without_db_v1"
STATUS = "completed_stage337EF_training_review_proxy_survivors_found_no_selection_no_mt5"
JUDGMENT = "proxy_survivors_found_but_attribution_and_runtime_precheck_required_no_selection"
DECISION = "stage337EF_open_run337EG_review_proxy_survivor_attribution_package_precheck"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EF_validation_density_trade_count_repair_training_review_without_db_"
    "no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ee.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ee.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EF_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EF_training_review.md"
SELECTED_STATUS = ee.SELECTED_STATUS
STAGE_BRIEF = ee.STAGE_BRIEF
WORKSPACE_STATE = ee.WORKSPACE_STATE
CURRENT_STATE = ee.CURRENT_STATE
CHANGELOG = ee.CHANGELOG
RUN_REGISTRY = ee.RUN_REGISTRY
ALPHA_LEDGER = ee.ALPHA_LEDGER
ARTIFACT_REGISTRY = ee.ARTIFACT_REGISTRY
STAGE_LEDGER = ee.STAGE_LEDGER

EE_FINAL = ee.FINAL_DECISION
EE_GATES = ee.REQUIRED_GATE_AUDIT
EE_QUEUE = ee.EF_QUEUE
MODEL_MANIFEST = ee.TRAINED_MODEL_MANIFEST
ONNX_PARITY = ee.ONNX_PARITY
CLASS_SCORECARD = ee.CANDIDATE_CLASSIFICATION_SCORECARD
TRADE_SCORECARD = ee.PROXY_TRADE_SCORECARD
CONTROL_SCORECARD = ee.NEGATIVE_CONTROL_SCORECARD
DENSITY_AUDIT = ee.DENSITY_GUARD_AUDIT
FIREWALL_REVIEW = ee.RUNTIME_FIREWALL_REVIEW
RELEASE_DISPOSITION = ee.RELEASE_DISPOSITION

CANDIDATE_TRAINING_REVIEW = RUN_DIR / "candidate_training_review.csv"
CANDIDATE_PASS_MATRIX = RUN_DIR / "candidate_pass_matrix.csv"
DENSITY_CONTROL_REVIEW = RUN_DIR / "density_control_review.csv"
RELEASE_LOCK_REVIEW = RUN_DIR / "release_lock_review.csv"
FAILURE_MEMORY_UPDATE = RUN_DIR / "failure_memory_update.csv"
EG_QUEUE = RUN_DIR / "run337EG_attribution_precheck_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EE_FINAL,
    EE_GATES,
    EE_QUEUE,
    MODEL_MANIFEST,
    ONNX_PARITY,
    CLASS_SCORECARD,
    TRADE_SCORECARD,
    CONTROL_SCORECARD,
    DENSITY_AUDIT,
    FIREWALL_REVIEW,
    RELEASE_DISPOSITION,
)
OUTPUT_FILES = (
    CANDIDATE_TRAINING_REVIEW,
    CANDIDATE_PASS_MATRIX,
    DENSITY_CONTROL_REVIEW,
    RELEASE_LOCK_REVIEW,
    FAILURE_MEMORY_UPDATE,
    EG_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    RUNTIME_RECEIPT,
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

REVIEW_COLUMNS = (
    "model_id",
    "task_id",
    "validation_pf",
    "validation_trade_count",
    "oos_pf",
    "oos_trade_count",
    "validation_balanced_accuracy",
    "control_block_rows",
    "density_pressure_rows",
    "joint_proxy_pass",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
PASS_COLUMNS = (
    "model_id",
    "validation_pf_pass",
    "validation_trade_count_pass",
    "density_pass",
    "control_pass",
    "oos_thin_quarantine",
    "joint_proxy_pass",
    "proxy_survivor_rank",
    "claim_boundary",
)
DENSITY_CONTROL_COLUMNS = (
    "review_id",
    "rows",
    "blocking_rows",
    "review_status",
    "effect",
    "claim_boundary",
)
LOCK_COLUMNS = (
    "review_id",
    "models",
    "proxy_survivor_rows",
    "release_candidate_rows",
    "auto_mt5_release_rows",
    "release_status",
    "release_blockers",
    "next_condition",
    "effect",
    "claim_boundary",
)
FAILURE_COLUMNS = ("memory_id", "observed", "interpretation", "next_repair_hint", "claim_boundary")
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


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def review_candidates() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    release = pd.read_csv(io_path(RELEASE_DISPOSITION))
    rows: list[dict[str, Any]] = []
    pass_rows: list[dict[str, Any]] = []
    survivors = []
    for item in release.to_dict("records"):
        validation_pf = float(item.get("validation_pf") or 0)
        validation_trades = int(float(item.get("validation_trade_count") or 0))
        oos_pf = float(item.get("oos_pf") or 0)
        oos_trades = int(float(item.get("oos_trade_count") or 0))
        control_blocks = int(float(item.get("control_block_rows") or 0))
        density_blocks = int(float(item.get("density_pressure_rows") or 0))
        pf_pass = validation_pf >= 1.05
        trade_pass = validation_trades >= 500
        density_pass = density_blocks == 0
        control_pass = control_blocks == 0
        oos_thin = oos_pf > 1.5 and oos_trades < 100
        joint = pf_pass and trade_pass and density_pass and control_pass and not oos_thin
        if joint:
            survivors.append((validation_pf, validation_trades, item.get("model_id", "")))
        status_bits = []
        if not pf_pass:
            status_bits.append("validation_pf_block")
        if not trade_pass:
            status_bits.append("validation_trade_count_block")
        if not density_pass:
            status_bits.append("density_pressure_block")
        if not control_pass:
            status_bits.append("control_block")
        if oos_thin:
            status_bits.append("thin_oos_quarantine")
        if joint:
            status_bits.append("proxy_survivor_review_required")
        rows.append(
            {
                "model_id": item.get("model_id", ""),
                "task_id": item.get("task_id", ""),
                "validation_pf": validation_pf,
                "validation_trade_count": validation_trades,
                "oos_pf": oos_pf,
                "oos_trade_count": oos_trades,
                "validation_balanced_accuracy": item.get("validation_balanced_accuracy", 0),
                "control_block_rows": control_blocks,
                "density_pressure_rows": density_blocks,
                "joint_proxy_pass": "true" if joint else "false",
                "review_status": ";".join(status_bits),
                "allowed_use": "proxy survivor attribution review only(프록시 생존 후보 귀속 검토 전용)" if joint else "failure memory and diagnostics(실패 기억과 진단)",
                "forbidden_use": "selection, MT5, Forward, live readiness(선택/MT5/전진/라이브 준비)",
                "effect": "학습 결과를 선택 전에 검토 가능한 행으로 분해한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        pass_rows.append(
            {
                "model_id": item.get("model_id", ""),
                "validation_pf_pass": str(pf_pass).lower(),
                "validation_trade_count_pass": str(trade_pass).lower(),
                "density_pass": str(density_pass).lower(),
                "control_pass": str(control_pass).lower(),
                "oos_thin_quarantine": str(oos_thin).lower(),
                "joint_proxy_pass": str(joint).lower(),
                "proxy_survivor_rank": "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    survivors_sorted = sorted(survivors, key=lambda item: (item[0], item[1]), reverse=True)
    rank_by_model = {model_id: rank for rank, (_, _, model_id) in enumerate(survivors_sorted, start=1)}
    for row in pass_rows:
        if row["model_id"] in rank_by_model:
            row["proxy_survivor_rank"] = rank_by_model[row["model_id"]]
    frame = pd.DataFrame(rows)
    summary = {
        "candidate_rows": len(rows),
        "validation_pf_pass_rows": int((frame["validation_pf"].astype(float) >= 1.05).sum()),
        "validation_trade_count_pass_rows": int((frame["validation_trade_count"].astype(int) >= 500).sum()),
        "validation_both_pass_rows": int(((frame["validation_pf"].astype(float) >= 1.05) & (frame["validation_trade_count"].astype(int) >= 500)).sum()),
        "proxy_survivor_rows": int((frame["joint_proxy_pass"] == "true").sum()),
        "control_block_models": int((frame["control_block_rows"].astype(int) > 0).sum()),
        "density_pressure_models": int((frame["density_pressure_rows"].astype(int) > 0).sum()),
        "best_validation_model_id": frame.sort_values(["validation_pf", "validation_trade_count"], ascending=[False, False]).iloc[0]["model_id"],
        "best_validation_pf": float(frame["validation_pf"].max()),
        "best_validation_trade_count": int(frame.sort_values(["validation_pf", "validation_trade_count"], ascending=[False, False]).iloc[0]["validation_trade_count"]),
        "best_proxy_survivor_model_id": survivors_sorted[0][2] if survivors_sorted else "",
        "best_proxy_survivor_pf": float(survivors_sorted[0][0]) if survivors_sorted else 0.0,
        "best_proxy_survivor_trade_count": int(survivors_sorted[0][1]) if survivors_sorted else 0,
    }
    return rows, pass_rows, summary


def review_density_controls() -> tuple[list[dict[str, Any]], dict[str, int]]:
    density = read_csv(DENSITY_AUDIT)
    controls = read_csv(CONTROL_SCORECARD)
    onnx = read_csv(ONNX_PARITY)
    density_blocks = sum(1 for row in density if row.get("split") == "validation" and row.get("density_pressure_flag") == "true")
    control_blocks = sum(1 for row in controls if row.get("split") == "validation" and row.get("blocks_training_review") == "true")
    onnx_failed = sum(1 for row in onnx if row.get("passed") != "true")
    rows = [
        {
            "review_id": "onnx_parity_review",
            "rows": len(onnx),
            "blocking_rows": onnx_failed,
            "review_status": "passed_onnx_parity" if onnx_failed == 0 else "blocked_onnx_parity",
            "effect": "Python/ONNX 확률 동등성을 EF에서 다시 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "density_pressure_review",
            "rows": len(density),
            "blocking_rows": density_blocks,
            "review_status": "passed_density_guard" if density_blocks == 0 else "blocked_density_pressure",
            "effect": "train 대비 검증 밀도 점프를 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "negative_control_review",
            "rows": len(controls),
            "blocking_rows": control_blocks,
            "review_status": "passed_for_survivor_filter" if control_blocks >= 0 else "blocked_control_parse",
            "effect": "대조 차단 후보를 proxy survivor(프록시 생존 후보)에서 제외한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows, {"density_blocks": density_blocks, "control_blocks": control_blocks, "onnx_failed": onnx_failed}


def build_release_lock(summary: Mapping[str, Any], guard: Mapping[str, int]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    blockers = ["no_auto_release_from_proxy_training", "mt5_not_run", "forward_not_run"]
    if summary["proxy_survivor_rows"] == 0:
        blockers.append("no_proxy_survivor")
    if guard["onnx_failed"] > 0:
        blockers.append("onnx_parity_failed")
    release_status = "proxy_survivors_need_attribution_precheck_no_selection" if summary["proxy_survivor_rows"] > 0 and guard["onnx_failed"] == 0 else "blocked_repair_needed"
    rows = [
        {
            "review_id": "ef_release_lock",
            "models": summary["candidate_rows"],
            "proxy_survivor_rows": summary["proxy_survivor_rows"],
            "release_candidate_rows": 0,
            "auto_mt5_release_rows": 0,
            "release_status": release_status,
            "release_blockers": ";".join(blockers),
            "next_condition": NEXT_RUN_ID,
            "effect": "프록시 생존 후보가 있어도 선택/MT5/Forward 주장을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return rows, {"release_status": release_status, "release_blockers": blockers}


def build_failure_memory(summary: Mapping[str, Any], guard: Mapping[str, int]) -> list[dict[str, str]]:
    return [
        {
            "memory_id": "pf_trade_joint_survivors_found",
            "observed": f"proxy_survivor_rows={summary['proxy_survivor_rows']};best_survivor_pf={summary['best_proxy_survivor_pf']};trades={summary['best_proxy_survivor_trade_count']}",
            "interpretation": "PF와 거래수 공동 하한을 통과한 프록시 후보가 생겼다.",
            "next_repair_hint": "attribution/package precheck before any selection or MT5(선택/MT5 전 귀속/패키지 사전검토).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "top_pf_trade_count_still_thin",
            "observed": f"best_validation_pf={summary['best_validation_pf']};best_validation_trade_count={summary['best_validation_trade_count']}",
            "interpretation": "최고 PF 모델은 여전히 거래수 500 미만이라 단독 우승 근거가 아니다.",
            "next_repair_hint": "rank survivors by joint criteria, not PF alone(PF 단독이 아니라 공동 기준으로 순위화).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "control_blocks_exist_but_survivor_filter_handles_them",
            "observed": f"control_block_models={summary['control_block_models']};control_block_rows={guard['control_blocks']}",
            "interpretation": "대조 차단 후보가 일부 남아 있으므로 생존 후보 필터에서 제외해야 한다.",
            "next_repair_hint": "carry control filter into EG attribution precheck(EG 귀속 사전검토에 대조 필터 이월).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_eg_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337EG_proxy_survivor_attribution",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review proxy survivor attribution(프록시 생존 후보 귀속 검토).",
            "required_inputs": f"{rel(CANDIDATE_TRAINING_REVIEW)};{rel(CANDIDATE_PASS_MATRIX)};{rel(TRADE_SCORECARD)}",
            "required_outputs": "proxy_survivor_attribution.csv;survivor_curve_pocket_review.csv",
            "blocked_if_missing": "candidate review/pass matrix/scorecards(후보 검토/통과 행렬/점수표).",
            "forbidden_action": "no selection or MT5 from proxy survivor list(프록시 생존 목록만으로 선택/MT5 금지).",
            "effect": "생존 후보의 수익 원천과 곡선 포켓을 분해한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EG_package_precheck",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "precheck ONNX/package lineage for proxy survivors(프록시 생존 후보 ONNX/패키지 계보 사전검토).",
            "required_inputs": f"{rel(MODEL_MANIFEST)};{rel(ONNX_PARITY)};{rel(RELEASE_LOCK_REVIEW)}",
            "required_outputs": "survivor_package_precheck.csv",
            "blocked_if_missing": "model manifest or ONNX parity(모델 목록 또는 ONNX 동등성).",
            "forbidden_action": "no deployment/live readiness(배포/라이브 준비 금지).",
            "effect": "런타임 검토 전 계보와 피처 정체성을 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "필수 EE 입력이 있어야 EF 검토가 닫힌다."),
        ("parent_ee_gates_passed", final["ee_failed_gate_rows"] == 0, str(final["ee_failed_gate_rows"]), "0", "부모 EE 학습 게이트가 통과해야 한다."),
        ("parent_next_action_matches", final["ee_next_action"] == RUN_ID, str(final["ee_next_action"]), RUN_ID, "라우팅이 EF로 정확히 이어졌는지 본다."),
        ("onnx_parity_clear", final["onnx_failed_rows"] == 0, str(final["onnx_failed_rows"]), "0", "ONNX 동등성 실패가 없어야 한다."),
        ("proxy_survivors_found", final["proxy_survivor_rows"] > 0, str(final["proxy_survivor_rows"]), ">0", "공동 기준 통과 프록시 후보가 있어야 다음 귀속 검토로 간다."),
        ("density_guard_clear", final["density_pressure_models"] == 0, str(final["density_pressure_models"]), "0", "검증 밀도 압력이 없어야 한다."),
        ("release_locked", final["release_candidate_rows"] == 0 and final["auto_mt5_release_rows"] == 0, f"release={final['release_candidate_rows']};mt5={final['auto_mt5_release_rows']}", "0/0", "EF는 선택/MT5를 자동으로 열지 않는다."),
        ("eg_queue_materialized", final["eg_queue_rows"] == 2, str(final["eg_queue_rows"]), "2", "EG 귀속/패키지 사전검토 큐를 연다."),
        (
            "no_forbidden_claim",
            final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "주장 경계를 보존한다.",
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
    data = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "sample_scope": f"candidates={final['candidate_rows']};proxy_survivors={final['proxy_survivor_rows']}",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_proxy_survivor_attribution(프록시 생존 후보 귀속에 사용 가능).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "onnx_parity": f"{final['onnx_passed_rows']}/{final['onnx_rows']}",
        "selection_metric": "none; proxy survivor filter only(없음, 프록시 생존 필터만).",
        "threshold_policy": "fixed_no_tuning(고정, 조정 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "validation_pf_pass_rows": final["validation_pf_pass_rows"],
        "validation_trade_count_pass_rows": final["validation_trade_count_pass_rows"],
        "validation_both_pass_rows": final["validation_both_pass_rows"],
        "proxy_survivor_rows": final["proxy_survivor_rows"],
        "best_proxy_survivor_pf": final["best_proxy_survivor_pf"],
        "best_proxy_survivor_trade_count": final["best_proxy_survivor_trade_count"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "runtime_claim": "not_run_no_MT5(미실행, MT5 없음)",
        "package_status": "precheck_required(사전검토 필요)",
        "runtime_authority": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_available": "candidate pass matrix, density/control review, release lock(후보 통과 행렬/밀도-대조 검토/해제 잠금).",
        "evidence_missing": "EG attribution, MT5, forward, operating review(EG 귀속/MT5/전진/운영 검토).",
        "next_condition": NEXT_RUN_ID,
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 안에서 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EF Training Review(337EF 학습 검토)

## Conclusion(결론)

run337EF(337EF 실행)는 EE 학습 결과 81개를 검토했다. validation PF(검증 PF)와 validation trade count(검증 거래수)를 동시에 통과하고 density/control(밀도/대조)도 통과한 proxy survivor(프록시 생존 후보)는 `{final["proxy_survivor_rows"]}`개다.

Action(행동): 후보 선택(candidate selection, 후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)은 실행하지 않았다.

Effect(효과): 다음 run337EG(337EG 실행)에서 생존 후보의 attribution/package precheck(귀속/패키지 사전검토)를 한다. 운영 주장이나 live readiness(라이브 준비)는 아직 없다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- candidate_rows(후보 행): `{final["candidate_rows"]}`
- validation_pf_pass_rows(검증 PF 통과 행): `{final["validation_pf_pass_rows"]}`
- validation_trade_count_pass_rows(검증 거래수 통과 행): `{final["validation_trade_count_pass_rows"]}`
- validation_both_pass_rows(검증 PF+거래수 통과 행): `{final["validation_both_pass_rows"]}`
- proxy_survivor_rows(프록시 생존 후보 행): `{final["proxy_survivor_rows"]}`
- best_proxy_survivor_pf(최고 생존 후보 PF): `{final["best_proxy_survivor_pf"]}`
- best_proxy_survivor_trade_count(최고 생존 후보 거래수): `{final["best_proxy_survivor_trade_count"]}`
- release_candidate_rows(해제 후보 행): `{final["release_candidate_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EF

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 공동 기준 통과 프록시 생존 후보가 있어 EG 귀속/패키지 사전검토로 넘긴다. 선택/MT5/Forward(전진)는 금지한다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(CANDIDATE_PASS_MATRIX)}`, `{rel(RELEASE_LOCK_REVIEW)}`
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
        f"  Stage337 run337EF focus complete: training review(학습 검토)에서 proxy survivor(프록시 생존 후보) `{final['proxy_survivor_rows']}`개를 찾았다. "
        "Effect(효과): 다음 run337EG에서 귀속/패키지 사전검토를 한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EF focus complete")
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
## Stage337 run337EF(337EF 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 프록시 생존 후보 `{final['proxy_survivor_rows']}`개를 찾았지만 선택/MT5/Forward/Goal(선택/MT5/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EE("
    if "## Stage337 run337EF(337EF 실행)" not in current_text:
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
- proxy_survivor_rows(프록시 생존 후보 행): `{final["proxy_survivor_rows"]}`
- actual_mt5_execution(실제 MT5 실행): `not_run_ef_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): proxy survivor attribution/package precheck(프록시 생존 후보 귀속/패키지 사전검토)로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EF(337EF 실행) reviewed EE training(EE 학습 검토) and found `{final['proxy_survivor_rows']}` proxy survivors. "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EF(337EF 실행) reviewed EE training"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EF reviewed EE training and opened `{NEXT_RUN_ID}` with proxy survivors={final['proxy_survivor_rows']}."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EF reviewed EE training"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_density_trade_count_repair_training_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"proxy_survivors={final['proxy_survivor_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "training_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "proxy_training_review",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"proxy_survivors={final['proxy_survivor_rows']};best_survivor_pf={final['best_proxy_survivor_pf']}",
        "guardrail_kpi": "release_locked;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment",
        "evidence_scope": "EE training reviewed",
        "kpi_scope": "proxy_survivor_training_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__training_review",
        "family": "model_validation_performance_attribution_result_judgment",
        "question": "do EE repair candidates produce proxy survivors without selection",
        "metric_scope": "validation_pf_trade_count_density_controls_onnx",
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
    candidate_rows, pass_rows, candidate_summary = review_candidates()
    density_control_rows, guard_summary = review_density_controls()
    release_rows, release_summary = build_release_lock(candidate_summary, guard_summary)
    failure_rows = build_failure_memory(candidate_summary, guard_summary)
    queue_rows = build_eg_queue()
    artifacts: list[Path] = [
        write_csv(CANDIDATE_TRAINING_REVIEW, REVIEW_COLUMNS, candidate_rows),
        write_csv(CANDIDATE_PASS_MATRIX, PASS_COLUMNS, pass_rows),
        write_csv(DENSITY_CONTROL_REVIEW, DENSITY_CONTROL_COLUMNS, density_control_rows),
        write_csv(RELEASE_LOCK_REVIEW, LOCK_COLUMNS, release_rows),
        write_csv(FAILURE_MEMORY_UPDATE, FAILURE_COLUMNS, failure_rows),
        write_csv(EG_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    ee_final = read_json(EE_FINAL)
    onnx_rows = read_csv(ONNX_PARITY)
    onnx_passed = sum(1 for row in onnx_rows if row.get("passed") == "true")
    onnx_failed = len(onnx_rows) - onnx_passed
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "ee_next_action": ee_final.get("next_action", ""),
        "ee_failed_gate_rows": sum(1 for row in read_csv(EE_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "candidate_rows": candidate_summary["candidate_rows"],
        "onnx_rows": len(onnx_rows),
        "onnx_passed_rows": onnx_passed,
        "onnx_failed_rows": onnx_failed,
        "validation_pf_pass_rows": candidate_summary["validation_pf_pass_rows"],
        "validation_trade_count_pass_rows": candidate_summary["validation_trade_count_pass_rows"],
        "validation_both_pass_rows": candidate_summary["validation_both_pass_rows"],
        "proxy_survivor_rows": candidate_summary["proxy_survivor_rows"],
        "control_block_models": candidate_summary["control_block_models"],
        "density_pressure_models": candidate_summary["density_pressure_models"],
        "best_validation_model_id": candidate_summary["best_validation_model_id"],
        "best_validation_pf": candidate_summary["best_validation_pf"],
        "best_validation_trade_count": candidate_summary["best_validation_trade_count"],
        "best_proxy_survivor_model_id": candidate_summary["best_proxy_survivor_model_id"],
        "best_proxy_survivor_pf": candidate_summary["best_proxy_survivor_pf"],
        "best_proxy_survivor_trade_count": candidate_summary["best_proxy_survivor_trade_count"],
        "release_candidate_rows": 0,
        "auto_mt5_release_rows": 0,
        "release_status": release_summary["release_status"],
        "release_blockers": release_summary["release_blockers"],
        "eg_queue_rows": len(queue_rows),
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
    artifacts.extend([write_report(final), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))

    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "proxy_survivor_rows": final["proxy_survivor_rows"],
                "best_proxy_survivor_pf": final["best_proxy_survivor_pf"],
                "best_proxy_survivor_trade_count": final["best_proxy_survivor_trade_count"],
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
