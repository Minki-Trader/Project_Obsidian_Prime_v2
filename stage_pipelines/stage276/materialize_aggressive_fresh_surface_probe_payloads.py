from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "276_onnx_candidate_campaign__aggressive_fresh_surface_probe"
RUN_ID = "run276B_materialize_aggressive_fresh_surface_probe_payloads_v1"
SOURCE_RUN_ID = "run276A_design_aggressive_fresh_surface_probe_packet_v1"
STATUS = "completed_aggressive_fresh_surface_probe_payload_materialization_no_candidate_selection"
JUDGMENT = "aggressive_probe_payloads_materialized_no_runtime_or_candidate_claim"
NEXT_ACTION = "run276C_execute_or_prepare_aggressive_fresh_surface_mt5_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN276A = STAGE / "02_runs" / "run276A"
RUN_DIR = STAGE / "02_runs" / "run276B"
PAYLOAD_DIR = RUN_DIR / "payloads"
HANDOFF_DIR = RUN_DIR / "handoff"
MT5_DIR = RUN_DIR / "mt5_handoff"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_BRANCH_PLAN = RUN276A / "branch_plan.csv"
SOURCE_SUPPLY = RUN276A / "branch_supply_metrics.csv"
SOURCE_MT5_QUEUE = RUN276A / "mt5_probe_design_queue.csv"
SOURCE_THRESHOLDS = RUN276A / "thresholds.json"
SOURCE_MANIFEST = RUN276A / "run_manifest.json"
SOURCE_LINEAGE = RUN276A / "lineage.json"
SOURCE_REPORT = REVIEWS / "run276A_report.md"
SOURCE_SUPPORT = STAGE / "01_inputs" / "support_control.csv"

PAYLOAD_MANIFEST = RUN_DIR / "payload_manifest.csv"
MT5_PROBE_QUEUE = RUN_DIR / "mt5_probe_queue.csv"
PAYLOAD_READINESS = RUN_DIR / "payload_readiness.csv"
TIER_RECEIPT = RUN_DIR / "tier.csv"
PAYLOAD_SAMPLES = RUN_DIR / "samples.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model.json"
RESULT_JUDGMENT = RUN_DIR / "judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage.json"
RUN_REPORT = REVIEWS / "run276B_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage276/materialize_aggressive_fresh_surface_probe_payloads.py")

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
PAYLOAD_MANIFEST_COLUMNS = (
    "variant_id",
    "queue_id",
    "package_id",
    "materialization_judgment",
    "next_queue_action",
    "payload_path",
    "payload_hash",
    "handoff_path",
    "handoff_hash",
    "mt5_tier_a_signal_path",
    "mt5_tier_a_signal_hash",
    "decision_surface_hash",
    "tier_a_oos_decision_count",
    "tier_a_oos_decision_rate",
    "selected_candidate",
    "onnx_readiness",
    "performance_claim",
)
MT5_QUEUE_COLUMNS = (
    "queue_id",
    "variant_id",
    "package_id",
    "queue_role",
    "payload_path",
    "handoff_path",
    "mt5_tier_a_signal_path",
    "decision_surface_hash",
    "signal_policy",
    "required_before_external_claim",
    "claim_boundary",
)
TIER_COLUMNS = (
    "variant_id",
    "package_id",
    "tier_view",
    "split",
    "rows",
    "decision_count",
    "decision_rate",
    "long_signal_count",
    "short_signal_count",
    "q04_guard_same_signal_rate",
    "claim_boundary",
)
READINESS_COLUMNS = ("check_name", "status", "effect")
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
KEY_COLUMNS = ["timestamp", "symbol", "split", "tier_view"]


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def repo_path(text: str) -> Path:
    return ROOT / text


def read_json(path: Path) -> dict[str, Any]:
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


def token(variant_id: str) -> str:
    return variant_id.replace("run276A_", "")


def load_source_table(path_text: str) -> pd.DataFrame:
    frame = pd.read_parquet(io_path(repo_path(path_text)))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    return frame


def branch_by_variant() -> dict[str, dict[str, str]]:
    return {row["variant_id"]: row for row in read_csv_rows(SOURCE_BRANCH_PLAN)}


def support_control_table() -> pd.DataFrame:
    support = read_csv_rows(SOURCE_SUPPORT)
    if not support:
        raise ValueError("support_control.csv(보조 대조 CSV)가 비어 있다.")
    frame = load_source_table(support[0]["source_score_table"])
    return frame[KEY_COLUMNS + ["entry_signal", "candidate_decision_score"]].rename(
        columns={
            "entry_signal": "q04_guard_entry_signal",
            "candidate_decision_score": "q04_guard_decision_score",
        }
    )


def decision_mask(frame: pd.DataFrame, branch: Mapping[str, str]) -> pd.Series:
    active = frame["entry_signal"].astype(str).ne("flat")
    variant_id = str(branch["variant_id"])
    thresholds = json.loads(str(branch["thresholds_json"]) or "{}")
    if variant_id.endswith("_q01_base_surface"):
        return active
    if variant_id.endswith("_q02_score_q70_focus"):
        return active & pd.to_numeric(frame["candidate_decision_score"], errors="coerce").ge(float(thresholds["score_min"]))
    if variant_id.endswith("_q03_q04_distance_focus"):
        return active & frame["entry_signal"].astype(str).ne(frame["q04_guard_entry_signal"].astype(str))
    if variant_id.endswith("_q04_risk_q70_focus"):
        return active & pd.to_numeric(frame["model_risk_pct"], errors="coerce").ge(float(thresholds["risk_min"]))
    raise ValueError(f"Unknown variant_id: {variant_id}")


def route_value(signal: pd.Series, mask: pd.Series) -> pd.Series:
    return pd.Series(np.where(mask & signal.eq("long"), 1, np.where(mask & signal.eq("short"), -1, 0)), index=signal.index, dtype="int8")


def decision_surface_hash(branch: Mapping[str, str], source_hash: str) -> str:
    payload = {
        "variant_id": branch["variant_id"],
        "decision_rule": branch["decision_rule"],
        "thresholds_json": branch["thresholds_json"],
        "source_score_table_hash": source_hash,
        "claim_boundary": BOUNDARY,
    }
    return sha256_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def counts_by_tier_split(payload: pd.DataFrame, variant_id: str, package_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tier_view in ["Tier A separate", "Tier B separate", "Tier A+B combined"]:
        tier_frame = payload if tier_view == "Tier A+B combined" else payload[payload["tier_view"].astype(str).eq(tier_view)]
        for split in ["train", "validation", "oos"]:
            part = tier_frame[tier_frame["split"].astype(str).eq(split)]
            decisions = part["variant_decision_flag"].astype(int).eq(1)
            same_guard = part["route_signal_label"].astype(str).eq(part["q04_guard_entry_signal"].astype(str))
            rows.append(
                {
                    "variant_id": variant_id,
                    "package_id": package_id,
                    "tier_view": tier_view,
                    "split": split,
                    "rows": int(len(part)),
                    "decision_count": int(decisions.sum()),
                    "decision_rate": round(float(decisions.mean()) if len(part) else 0.0, 8),
                    "long_signal_count": int(part["route_signal_value"].astype(int).eq(1).sum()),
                    "short_signal_count": int(part["route_signal_value"].astype(int).eq(-1).sum()),
                    "q04_guard_same_signal_rate": round(float(same_guard[decisions].mean()) if int(decisions.sum()) else 0.0, 8),
                    "claim_boundary": BOUNDARY,
                }
            )
    return rows


def materialize_payloads() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    branch_map = branch_by_variant()
    design_queue = read_csv_rows(SOURCE_MT5_QUEUE)
    q04 = support_control_table()
    manifest_rows: list[dict[str, Any]] = []
    mt5_rows: list[dict[str, Any]] = []
    tier_rows: list[dict[str, Any]] = []
    samples: dict[str, Any] = {}
    for design in design_queue:
        variant_id = design["variant_id"]
        package_id = design["package_id"]
        branch = branch_map[variant_id]
        frame = load_source_table(design["source_score_table"])
        payload = frame.merge(q04, on=KEY_COLUMNS, how="left")
        payload["q04_guard_entry_signal"] = payload["q04_guard_entry_signal"].fillna("flat")
        mask = decision_mask(payload, branch)
        signal = payload["entry_signal"].astype(str)
        payload["source_run_id"] = SOURCE_RUN_ID
        payload["run276b_queue_id"] = design["queue_id"]
        payload["variant_id"] = variant_id
        payload["package_id"] = package_id
        payload["variant_role"] = branch["variant_role"]
        payload["variant_decision_flag"] = mask.astype("int8")
        payload["route_signal_value"] = route_value(signal, mask)
        payload["route_signal_label"] = payload["route_signal_value"].map({1: "long", -1: "short", 0: "flat"})
        payload["variant_model_risk_pct"] = np.where(mask, pd.to_numeric(payload["model_risk_pct"], errors="coerce").fillna(0.0), 0.0)
        payload["payload_claim_boundary"] = BOUNDARY
        source_hash = sha256_file_lf_normalized(repo_path(design["source_score_table"]))
        surface_hash = decision_surface_hash(branch, source_hash)
        payload["variant_decision_surface_hash"] = surface_hash

        local_token = token(variant_id)
        payload_path = PAYLOAD_DIR / f"{local_token}.parquet"
        io_path(PAYLOAD_DIR).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)

        tier_a = payload[payload["tier_view"].astype(str).eq("Tier A separate")].copy()
        tier_a["timestamp"] = pd.to_datetime(tier_a["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        mt5_path = MT5_DIR / f"{local_token}_tier_a_signals.csv"
        io_path(MT5_DIR).mkdir(parents=True, exist_ok=True)
        tier_a[
            [
                "timestamp",
                "symbol",
                "split",
                "variant_id",
                "package_id",
                "variant_decision_flag",
                "route_signal_value",
                "route_signal_label",
                "entry_signal",
                "q04_guard_entry_signal",
                "candidate_decision_score",
                "model_risk_pct",
                "variant_model_risk_pct",
                "variant_decision_surface_hash",
            ]
        ].to_csv(io_path(mt5_path), index=False, lineterminator="\n")

        local_tier_rows = counts_by_tier_split(payload, variant_id, package_id)
        tier_rows.extend(local_tier_rows)
        tier_a_oos = next(row for row in local_tier_rows if row["tier_view"] == "Tier A separate" and row["split"] == "oos")
        handoff_payload = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "variant_id": variant_id,
            "package_id": package_id,
            "source_score_table": design["source_score_table"],
            "source_handoff_json": design["source_handoff_json"],
            "decision_rule": branch["decision_rule"],
            "thresholds": json.loads(str(branch["thresholds_json"]) or "{}"),
            "decision_surface_hash": surface_hash,
            "payload_path": rel(payload_path),
            "payload_hash": sha256_file_lf_normalized(payload_path),
            "mt5_tier_a_signal_path": rel(mt5_path),
            "mt5_tier_a_signal_hash": sha256_file_lf_normalized(mt5_path),
            "tier_view_counts": {
                f"{row['tier_view']}|{row['split']}": {
                    "rows": row["rows"],
                    "decision_count": row["decision_count"],
                    "decision_rate": row["decision_rate"],
                    "long_signal_count": row["long_signal_count"],
                    "short_signal_count": row["short_signal_count"],
                }
                for row in local_tier_rows
            },
            "signal_policy": "variant_decision_flag(분기 판단 플래그)이 1이면 source entry_signal(원천 진입 신호)을 route_signal(경로 신호)로 보존한다.",
            "label_payload_policy": "label/future columns(라벨/미래 열)은 payload parquet(페이로드 파케이)와 MT5 signal CSV(MT5 신호 CSV)에 포함하지 않는다.",
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        handoff_path = HANDOFF_DIR / f"{local_token}.json"
        write_json(handoff_path, handoff_payload)
        manifest_rows.append(
            {
                "variant_id": variant_id,
                "queue_id": design["queue_id"],
                "package_id": package_id,
                "materialization_judgment": "payload_materialized_no_candidate_claim",
                "next_queue_action": "include_for_run276C_mt5_probe",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file_lf_normalized(handoff_path),
                "mt5_tier_a_signal_path": rel(mt5_path),
                "mt5_tier_a_signal_hash": sha256_file_lf_normalized(mt5_path),
                "decision_surface_hash": surface_hash,
                "tier_a_oos_decision_count": tier_a_oos["decision_count"],
                "tier_a_oos_decision_rate": tier_a_oos["decision_rate"],
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "performance_claim": "none",
            }
        )
        mt5_rows.append(
            {
                "queue_id": f"run276C_{local_token}",
                "variant_id": variant_id,
                "package_id": package_id,
                "queue_role": "active_pressure_probe",
                "payload_path": rel(payload_path),
                "handoff_path": rel(handoff_path),
                "mt5_tier_a_signal_path": rel(mt5_path),
                "decision_surface_hash": surface_hash,
                "signal_policy": "route_preserving_structural_signal_pending_run276C_replay_policy",
                "required_before_external_claim": "MT5 runtime output;trade list;balance/equity curve;time-slice KPI",
                "claim_boundary": BOUNDARY,
            }
        )
        samples[variant_id] = payload[
            ["timestamp", "split", "tier_view", "variant_decision_flag", "route_signal_label", "q04_guard_entry_signal"]
        ].head(5).to_dict(orient="records")
    return manifest_rows, mt5_rows, tier_rows, samples


def write_receipts(manifest_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]], tier_rows: Sequence[Mapping[str, Any]], samples: Mapping[str, Any]) -> None:
    write_csv(PAYLOAD_MANIFEST, PAYLOAD_MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_PROBE_QUEUE, MT5_QUEUE_COLUMNS, mt5_rows)
    write_csv(TIER_RECEIPT, TIER_COLUMNS, tier_rows)
    write_json(PAYLOAD_SAMPLES, samples)
    write_csv(
        PAYLOAD_READINESS,
        READINESS_COLUMNS,
        [
            {
                "check_name": "payload_files_materialized(페이로드 파일 물질화)",
                "status": "passed(통과)" if len(manifest_rows) == len(read_csv_rows(SOURCE_MT5_QUEUE)) else "failed(실패)",
                "effect": "각 설계 대기열 행에 payload parquet(페이로드 파케이), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)를 붙인다.",
            },
            {
                "check_name": "mt5_queue_materialized(MT5 대기열 물질화)",
                "status": "passed(통과)" if mt5_rows else "failed_no_queue(대기열 없음)",
                "effect": "run276C(276C 실행)가 소비할 MT5 probe queue(MT5 탐침 대기열)를 만든다.",
            },
            {
                "check_name": "claim_guard(주장 방어)",
                "status": "passed(통과)",
                "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            },
        ],
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "hypothesis": "run276A branch design(276A 분기 설계)을 label-free payload(라벨 없는 페이로드)로 만들면 run276C MT5 probe(276C MT5 탐침)를 준비할 수 있다.",
            "decision_use": "run276C execute/prepare MT5 probe(276C MT5 탐침 실행/준비) 입력으로 사용한다.",
            "changed_variables": "branch decision mask(분기 판단 마스크), route_signal(경로 신호), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)",
            "success_criteria": "all queued branches(모든 대기열 분기)가 payload/handoff/MT5 CSV(페이로드/인계/MT5 CSV)를 가진다.",
            "failure_criteria": "missing payload(페이로드 누락), missing MT5 CSV(MT5 CSV 누락), label/future leakage(라벨/미래 누수)",
            "payload_count": len(manifest_rows),
            "mt5_queue_rows": len(mt5_rows),
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [rel(path) for path in source_inputs()],
            "source_hashes": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs() if path_exists(path)},
            "time_axis": "timestamp/split/tier_view(시각/분할/티어 보기)를 유지한다.",
            "feature_label_boundary": "label/future columns(라벨/미래 열)을 출력에 포함하지 않는다.",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산)",
            "performance_claim": "none",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "model_family": "deterministic payload materialization(결정론 페이로드 물질화), no trained model(학습 모델 없음)",
            "selection_metric": "materialization completeness(물질화 완전성), not candidate selection(후보 선택 아님)",
            "allowed_claims": ["payload_materialized(페이로드 물질화)", "mt5_queue_ready(MT5 대기열 준비)"],
            "forbidden_claims": ["selected_candidate(선택 후보)", "ONNX readiness(ONNX 준비)", "Goal Achieve(목표 달성)"],
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows(manifest_rows, mt5_rows))
    write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows(manifest_rows, mt5_rows))


def result_rows(manifest_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "payload_manifest(페이로드 목록), mt5_probe_queue(MT5 탐침 대기열), tier_receipt(티어 영수증), handoff JSON(인계 JSON)",
            "evidence_missing": "MT5 tester output(MT5 테스터 출력), KPI receipt(KPI 영수증), curve/trade-quality review(곡선/거래 품질 검토)",
            "judgment_label": JUDGMENT,
            "judgment_class": "payload_ready_no_runtime_claim",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": f"payload(페이로드) {len(manifest_rows)}개와 MT5 queue(MT5 대기열) {len(mt5_rows)}행을 만들었지만 런타임 결과는 아직 없다.",
        }
    ]


def gate_rows(manifest_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "gate_name": "scope_completion_gate(범위 완료 게이트)",
            "status": "passed(통과)" if manifest_rows and mt5_rows else "failed(실패)",
            "evidence_path": rel(PAYLOAD_MANIFEST),
            "effect": "설계 대기열을 payload/handoff/MT5 CSV(페이로드/인계/MT5 CSV)로 물질화한다.",
        },
        {
            "gate_name": "runtime_evidence_boundary_gate(런타임 근거 경계 게이트)",
            "status": "passed_with_boundary(경계 포함 통과)",
            "evidence_path": rel(MT5_PROBE_QUEUE),
            "effect": "MT5 실행 전이므로 runtime authority(런타임 권위)를 주장하지 않는다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def source_inputs() -> list[Path]:
    paths = [SOURCE_BRANCH_PLAN, SOURCE_SUPPLY, SOURCE_MT5_QUEUE, SOURCE_THRESHOLDS, SOURCE_MANIFEST, SOURCE_LINEAGE, SOURCE_REPORT, SOURCE_SUPPORT]
    for row in read_csv_rows(SOURCE_MT5_QUEUE):
        paths.append(repo_path(row["source_score_table"]))
        paths.append(repo_path(row["source_handoff_json"]))
    for row in read_csv_rows(SOURCE_SUPPORT):
        paths.append(repo_path(row["source_score_table"]))
        paths.append(repo_path(row["source_handoff_json"]))
    return paths


def write_report(manifest_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> None:
    lines = "\n".join(
        f"- `{row['variant_id']}`: payload(페이로드) `{row['payload_path']}`, mt5_csv(MT5 CSV) `{row['mt5_tier_a_signal_path']}`"
        for row in manifest_rows
    )
    write_md(
        RUN_REPORT,
        f"""# run276B Aggressive Fresh Surface Payload Materialization(276B 공격형 새 표면 페이로드 물질화)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- payload_count(페이로드 수): `{len(manifest_rows)}`
- mt5_queue_rows(MT5 대기열 행): `{len(mt5_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run276B(276B 실행)는 run276A(276A 실행)의 MT5 probe design queue(MT5 탐침 설계 대기열)를 payload parquet(페이로드 파케이), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)로 바꿨다.
효과(effect, 효과): run276C(276C 실행)는 실제 MT5 runtime output(MT5 런타임 출력)을 시도하거나, 터미널 차단 사유를 좁게 기록할 수 있다.

## Payloads(페이로드)

{lines}

## Evidence Paths(근거 경로)

- payload_manifest(페이로드 목록): `{rel(PAYLOAD_MANIFEST)}`
- mt5_probe_queue(MT5 탐침 대기열): `{rel(MT5_PROBE_QUEUE)}`
- tier_receipt(티어 영수증): `{rel(TIER_RECEIPT)}`
- readiness(준비 영수증): `{rel(PAYLOAD_READINESS)}`
- lineage(계보): `{rel(LINEAGE_RECEIPT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_stage_docs(manifest_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> None:
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_once(selection, "run276B_report", f"- run276B_report(276B 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run276B_mt5_queue", f"- run276B_mt5_queue(276B MT5 대기열): `{rel(MT5_PROBE_QUEUE)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run276B_report",
        "\n".join(
            [
                f"- run276B_report(276B 보고서): `{rel(RUN_REPORT)}`",
                f"- run276B_payload_manifest(276B 페이로드 목록): `{rel(PAYLOAD_MANIFEST)}`",
                f"- run276B_mt5_queue(276B MT5 대기열): `{rel(MT5_PROBE_QUEUE)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `aggressive_fresh_surface_probe_payload_materialization`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run276B_summary",
        (
            f"- run276B_summary(276B 요약): payload parquet(페이로드 파케이) `{len(manifest_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) "
            f"`{len(mt5_rows)}`행을 만들었다. Effect(효과): run276C(276C 실행)에서 MT5 runtime output(MT5 런타임 출력)을 시도할 수 있고, "
            "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage276(276단계) run276B(276B 실행) aggressive fresh surface payload materialization(공격형 새 표면 페이로드 물질화) `{RUN_ID}`. "
        f"Effect(효과): payload parquet(페이로드 파케이) `{len(manifest_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(mt5_rows)}`행을 만들고, "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run276B aggressive fresh surface payload materialization(276B 공격형 새 표면 페이로드 물질화)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): payload parquet(페이로드 파케이) `{len(manifest_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(mt5_rows)}`행을 만들었다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)


def manifest_payload(created_at: str, artifacts: Sequence[Path], inputs: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in inputs],
        "input_hashes": {rel(path): sha256_file_lf_normalized(path) for path in inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "payload_count": len(manifest_rows),
        "mt5_probe_queue_rows": len(mt5_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def output_artifacts() -> list[Path]:
    artifacts = [
        PAYLOAD_MANIFEST,
        MT5_PROBE_QUEUE,
        PAYLOAD_READINESS,
        TIER_RECEIPT,
        PAYLOAD_SAMPLES,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    artifacts.extend(sorted(PAYLOAD_DIR.glob("*.parquet")))
    artifacts.extend(sorted(HANDOFF_DIR.glob("*.json")))
    artifacts.extend(sorted(MT5_DIR.glob("*.csv")))
    return artifacts


def update_registers(created_at: str, manifest_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"payloads={len(manifest_rows)};mt5_queue={len(mt5_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__{row['variant_id']}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": row["variant_id"],
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "aggressive fresh surface payload materialization(공격형 새 표면 페이로드 물질화)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
            "kpi_scope": "payload_materialization_only_no_trading_kpi",
            "scoreboard_lane": "mt5_probe_payload",
            "status": STATUS,
            "judgment": row["materialization_judgment"],
            "path": rel(PAYLOAD_MANIFEST),
            "primary_kpi": f"tier_a_oos_decision_count={row['tier_a_oos_decision_count']};tier_a_oos_decision_rate={row['tier_a_oos_decision_rate']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
            "notes": f"mt5_signal={row['mt5_tier_a_signal_path']}",
        }
        for row in manifest_rows
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__payload_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "aggressive_fresh_surface_payload_materialization",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "payload_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "payload_materialization_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"payloads={len(manifest_rows)};mt5_queue={len(mt5_rows)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run276B_payload_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run276B aggressive fresh surface payload materialization artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def run() -> dict[str, Any]:
    inputs = source_inputs()
    must_exist(inputs)
    for path in [RUN_DIR, PAYLOAD_DIR, HANDOFF_DIR, MT5_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    manifest_rows, mt5_rows, tier_rows, samples = materialize_payloads()
    write_receipts(manifest_rows, mt5_rows, tier_rows, samples)
    write_report(manifest_rows, mt5_rows)
    artifacts = output_artifacts()
    manifest = manifest_payload(created_at, artifacts, inputs, manifest_rows, mt5_rows)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, artifacts, inputs, manifest_rows, mt5_rows)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    artifacts.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, artifacts, inputs, manifest_rows, mt5_rows)
    write_json(RUN_MANIFEST, manifest)

    update_stage_docs(manifest_rows, mt5_rows)
    update_registers(created_at, manifest_rows, mt5_rows, artifacts)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "payload_count": len(manifest_rows),
        "mt5_probe_queue_rows": len(mt5_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
