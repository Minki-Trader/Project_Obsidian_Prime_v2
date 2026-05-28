from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from stage_pipelines.stage336 import attempt_fresh_mt5_runtime_probe_or_block as run336k  # noqa: E402
from stage_pipelines.stage337 import materialize_common_files_and_run_argmax_parity_probe as el  # noqa: E402
from stage_pipelines.stage337 import review_or_expand_argmax_runtime_parity_probe as em  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
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
STAGE_ID = el.STAGE_ID
RUN_NUMBER = "run337EN"
RUN_ID = "run337EN_surface_degeneracy_memory_or_full_survivor_runtime_probe_without_db_v1"
PARENT_RUN_ID = em.RUN_ID
NEXT_RUN_ID = "run337EO_refresh_survivor_feature_handoff_and_surface_reprobe_without_db_v1"
STATUS = "completed_stage337EN_latest_raw_available_survivor_feature_handoff_stale_all_flat_memory_no_selection"
JUDGMENT = "forward_raw_data_available_but_survivor_feature_handoff_stale_and_latest_surface_degenerate_no_forward_decision"
DECISION = "stage337EN_open_run337EO_refresh_survivor_feature_handoff_and_surface_reprobe"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EN_surface_degeneracy_memory_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = el.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RAW_REFRESH_DIR = RUN_DIR / "raw_refresh_probe"
REPORT_PATH = el.REVIEWS_DIR / "run337EN_surface_degeneracy_memory.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EN_surface_degeneracy_memory.md"
SELECTED_STATUS = el.SELECTED_STATUS
STAGE_BRIEF = el.STAGE_BRIEF
WORKSPACE_STATE = el.WORKSPACE_STATE
CURRENT_STATE = el.CURRENT_STATE
CHANGELOG = el.CHANGELOG
RUN_REGISTRY = el.RUN_REGISTRY
ALPHA_LEDGER = el.ALPHA_LEDGER
ARTIFACT_REGISTRY = el.ARTIFACT_REGISTRY
STAGE_LEDGER = el.STAGE_LEDGER

RAW_SUMMARY = RUN_DIR / "fresh_forward_data_probe_summary.csv"
RAW_LATEST = RUN_DIR / "fresh_forward_data_probe_latest.json"
FEATURE_STALENESS = RUN_DIR / "survivor_feature_handoff_staleness.csv"
SURFACE_MEMORY = RUN_DIR / "survivor_surface_degeneracy_memory.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"

INPUT_FILES = (
    em.FINAL_DECISION,
    em.EXPECTED_SURFACE_SCAN,
    em.EXECUTION_SUMMARY,
    em.RUNTIME_DIFF,
    el.EJ_ADAPTER_PROBE_MANIFEST,
    el.EH_FEATURE_HANDOFF,
    el.EG_PACKAGE_PRECHECK,
)
OUTPUT_FILES = (
    RAW_SUMMARY,
    RAW_LATEST,
    FEATURE_STALENESS,
    SURFACE_MEMORY,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

RAW_COLUMNS = (
    "contract_symbol",
    "broker_symbol",
    "status",
    "rows",
    "first_open_utc",
    "last_open_utc",
    "last_close_utc",
    "csv_path",
    "manifest_path",
    "last_error",
)
STALENESS_COLUMNS = (
    "rank",
    "attempt_name",
    "model_id",
    "feature_set_id",
    "source_model_input",
    "feature_rows",
    "feature_first_timestamp",
    "feature_last_timestamp",
    "rows_after_2026_04_14",
    "latest_raw_us100_close_utc",
    "feature_to_latest_raw_gap_minutes",
    "handoff_status",
    "effect",
    "claim_boundary",
)
SURFACE_COLUMNS = (
    "rank",
    "attempt_name",
    "model_id",
    "feature_rows",
    "decision_short_total",
    "decision_long_total",
    "decision_flat_total",
    "decision_nonflat_total",
    "last_nonflat_timestamp",
    "latest_overlap_from",
    "latest_overlap_to",
    "latest_overlap_rows",
    "latest_overlap_nonflat_rows",
    "surface_memory",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337EN surface degeneracy memory and latest raw data probe.")
    parser.add_argument("--terminal-path", default=r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E\terminal64.exe")
    parser.add_argument("--end-utc", default="")
    parser.add_argument("--attempt-limit", type=int, default=7)
    parser.add_argument("--latest-overlap-from", default="2026.04.10")
    parser.add_argument("--latest-overlap-to", default="2026.04.14")
    return parser.parse_args()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def write_local_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


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


def configure_raw_probe() -> None:
    run336k.RAW_REFRESH_DIR = RAW_REFRESH_DIR
    run336k.CLAIM_BOUNDARY = CLAIM_BOUNDARY


def timestamp_text(value: pd.Timestamp) -> str:
    if pd.isna(value):
        return ""
    return value.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")


def build_feature_and_surface_rows(
    latest: Mapping[str, Any],
    *,
    attempt_limit: int,
    latest_overlap_from: str,
    latest_overlap_to: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    latest_close = pd.to_datetime(latest.get("us100_last_close_utc", ""), utc=True, errors="coerce")
    feature_contracts = el.load_feature_contracts()
    staleness_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    forward_start = pd.Timestamp("2026-04-14T00:00:00Z")
    for attempt in el.selected_attempts(attempt_limit):
        feature_row = feature_contracts[str(attempt["feature_set_id"])]
        feature_order = json.loads(str(feature_row["included_features_json"]))
        source = ROOT / str(feature_row["source_model_input"])
        frame = pd.read_parquet(io_path(source))
        timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
        first_ts = timestamps.min()
        last_ts = timestamps.max()
        rows_after_forward = int((timestamps >= forward_start).sum())
        gap_minutes = "" if pd.isna(latest_close) or pd.isna(last_ts) else (latest_close - last_ts).total_seconds() / 60.0
        handoff_status = "stale_before_forward_window" if rows_after_forward == 0 else "has_forward_rows"
        staleness_rows.append(
            {
                "rank": attempt["proxy_rank"],
                "attempt_name": attempt["attempt_name"],
                "model_id": attempt["model_id"],
                "feature_set_id": attempt["feature_set_id"],
                "source_model_input": rel(source),
                "feature_rows": int(len(frame)),
                "feature_first_timestamp": timestamp_text(first_ts),
                "feature_last_timestamp": timestamp_text(last_ts),
                "rows_after_2026_04_14": rows_after_forward,
                "latest_raw_us100_close_utc": latest.get("us100_last_close_utc", ""),
                "feature_to_latest_raw_gap_minutes": gap_minutes,
                "handoff_status": handoff_status,
                "effect": "raw data exists but survivor feature handoff must be refreshed(원천 데이터는 있으나 생존 후보 피처 인계 갱신 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        model = joblib.load(io_path(Path(str(attempt["model_path"]))))
        matrix = frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
        probs = el.ordered_probabilities(model, matrix)
        decisions = np.asarray(["short", "flat", "long"], dtype=object)[probs.argmax(axis=1)]
        nonflat = decisions != "flat"
        latest_overlap = el.date_filter(frame, latest_overlap_from, latest_overlap_to)
        if latest_overlap.empty:
            latest_nonflat = 0
        else:
            latest_probs = el.ordered_probabilities(
                model,
                latest_overlap.loc[:, feature_order].to_numpy(dtype="float64", copy=False),
            )
            latest_decisions = np.asarray(["short", "flat", "long"], dtype=object)[latest_probs.argmax(axis=1)]
            latest_nonflat = int((latest_decisions != "flat").sum())
        surface_rows.append(
            {
                "rank": attempt["proxy_rank"],
                "attempt_name": attempt["attempt_name"],
                "model_id": attempt["model_id"],
                "feature_rows": int(len(frame)),
                "decision_short_total": int((decisions == "short").sum()),
                "decision_long_total": int((decisions == "long").sum()),
                "decision_flat_total": int((decisions == "flat").sum()),
                "decision_nonflat_total": int(nonflat.sum()),
                "last_nonflat_timestamp": timestamp_text(timestamps[nonflat].max()) if nonflat.any() else "",
                "latest_overlap_from": latest_overlap_from,
                "latest_overlap_to": latest_overlap_to,
                "latest_overlap_rows": int(len(latest_overlap)),
                "latest_overlap_nonflat_rows": latest_nonflat,
                "surface_memory": "latest_overlap_all_flat" if latest_nonflat == 0 else "latest_overlap_has_direction",
                "effect": "records surface degeneracy before any retuning(재튜닝 없이 표면 퇴화 기억을 기록)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return staleness_rows, surface_rows


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    parent = read_json(em.FINAL_DECISION)
    gates = [
        ("input_presence", final["missing_inputs"] == 0, final["missing_inputs"], "0", "EN 입력이 모두 있어야 한다."),
        (
            "parent_em_next_action_matches",
            parent.get("next_action") == RUN_ID,
            parent.get("next_action", ""),
            RUN_ID,
            "부모 EM이 EN으로 이어져야 한다.",
        ),
        (
            "latest_raw_probe_completed",
            final["raw_us100_status"] == "completed",
            final["raw_us100_status"],
            "completed",
            "최신 raw US100 탐침이 성공해야 한다.",
        ),
        (
            "forward_raw_rows_present",
            final["raw_us100_rows"] > 0 and final["raw_us100_last_close_after_forward_start"] == "true",
            f"rows={final['raw_us100_rows']};after={final['raw_us100_last_close_after_forward_start']}",
            "rows>0;after=true",
            "2026-04-14 이후 raw 데이터가 있어야 한다.",
        ),
        (
            "survivor_feature_frames_measured",
            final["feature_handoff_rows"] == final["attempt_limit"],
            final["feature_handoff_rows"],
            final["attempt_limit"],
            "생존 후보 피처 프레임을 모두 측정해야 한다.",
        ),
        (
            "feature_handoff_stale_named",
            final["feature_rows_after_forward_total"] == 0,
            final["feature_rows_after_forward_total"],
            "0",
            "현재 생존 후보 피처 인계가 전진 구간을 덮지 못함을 이름 붙인다.",
        ),
        (
            "latest_overlap_all_flat_named",
            final["latest_overlap_nonflat_rows"] == 0,
            final["latest_overlap_nonflat_rows"],
            "0",
            "기존 마지막 겹침 구간의 all-flat(전부 평탄)을 이름 붙인다.",
        ),
        (
            "no_forbidden_claim",
            final["forward_passed"] == "not_claimed" and final["runtime_authority"] == "not_claimed",
            f"forward={final['forward_passed']};authority={final['runtime_authority']}",
            "not_claimed;not_claimed",
            "데이터/표면 기억을 운영 주장으로 과장하지 않는다.",
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
        for gate_id, passed, observed, expected, effect in gates
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EN Surface Degeneracy Memory(표면 퇴화 기억)

## Conclusion(결론)

run337EN(337EN 실행)는 최신 raw broker data(원천 브로커 데이터)가 있는지와 현재 survivor feature handoff(생존 후보 피처 인계)가 그 데이터를 덮는지를 분리했다.

Action(행동): MT5 API(MT5 API)로 2026-04-14 이후 raw M5(원천 5분봉)를 다시 확인하고, 7개 survivor(생존 후보)의 feature frame(피처 프레임) 마지막 시각과 decision surface(결정 표면)를 스캔했다.

Effect(효과): raw US100(원천 US100)은 `{final['raw_us100_last_close_utc']}`까지 있으나, 생존 후보 피처 프레임은 2026-04-13에서 멈춰 forward pass/fail(전진 통과/실패)을 판단할 수 없다. 다음은 피처 인계 갱신과 표면 재탐침이다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- raw_us100_rows(원천 US100 행): `{final['raw_us100_rows']}`
- raw_us100_last_close_utc(원천 US100 마지막 종가 UTC): `{final['raw_us100_last_close_utc']}`
- feature_handoff_rows(피처 인계 행): `{final['feature_handoff_rows']}`
- feature_rows_after_forward_total(전진 이후 피처 행 합): `{final['feature_rows_after_forward_total']}`
- stale_feature_handoff_rows(낡은 피처 인계 행): `{final['stale_feature_handoff_rows']}`
- latest_overlap_nonflat_rows(최신 겹침 비평탄 행): `{final['latest_overlap_nonflat_rows']}`
- gates_passed(게이트 통과): `{final['passed_gates']}/{final['gate_rows']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EN

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): 최신 raw data(원천 데이터)는 있으나 survivor feature handoff(생존 후보 피처 인계)가 낡아 Forward(전진) 판정이 아니라 refresh/reprobe(갱신/재탐침)로 보낸다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(RAW_SUMMARY)}`, `{rel(RAW_LATEST)}`, `{rel(FEATURE_STALENESS)}`, `{rel(SURFACE_MEMORY)}`
- next_action(다음 행동): `{final['next_action']}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = workspace_text.replace(f"current_run_id: {RUN_ID}", f"current_run_id: {final['next_action']}", 1)
    workspace_text = workspace_text.replace("current_run_id: run337EN_surface_degeneracy_memory_or_full_survivor_runtime_probe_without_db_v1", f"current_run_id: {final['next_action']}", 1)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337EN focus complete: latest raw data(최신 원천 데이터)는 `{final['raw_us100_last_close_utc']}`까지 확인했지만 "
        f"survivor feature handoff(생존 후보 피처 인계)는 forward rows(전진 행) `{final['feature_rows_after_forward_total']}`로 멈췄다. "
        "Effect(효과): Forward(전진) 판정 대신 feature refresh/reprobe(피처 갱신/재탐침)를 연다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EN focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337EN(337EN 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): raw forward data(원천 전진 데이터)는 있지만 survivor feature handoff(생존 후보 피처 인계)가 2026-04-13에서 멈춰 refresh/reprobe(갱신/재탐침)를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EM("
    if "## Stage337 run337EN(337EN 실행)" not in current_text:
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- raw_us100_last_close_utc(원천 US100 마지막 종가 UTC): `{final['raw_us100_last_close_utc']}`
- survivor_feature_rows_after_forward_total(생존 후보 전진 피처 행 합): `{final['feature_rows_after_forward_total']}`
- latest_overlap_nonflat_rows(최신 겹침 비평탄 행): `{final['latest_overlap_nonflat_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): feature handoff refresh(피처 인계 갱신)와 surface reprobe(표면 재탐침)으로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EN(337EN 실행) separated raw forward data availability(원천 전진 데이터 가용성) from stale survivor feature handoff(낡은 생존 후보 피처 인계). "
        f"Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EN(337EN 실행) separated raw forward"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EN confirmed latest raw data exists but survivor feature handoff is stale, opening `{final['next_action']}` without Forward/Goal claims."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EN confirmed latest raw"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "surface_degeneracy_memory_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"raw_last={final['raw_us100_last_close_utc']};feature_forward_rows={final['feature_rows_after_forward_total']};next={final['next_action']};goal_achieve_not_claimed.",
        "family": "data_integrity_runtime_parity_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__surface_degeneracy_memory",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "surface_degeneracy_memory",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "data_feature_surface_memory_no_selection",
        "tier_scope": "tier_a_probe",
        "kpi_scope": "data_freshness_and_decision_surface_not_profitability",
        "scoreboard_lane": "data_integrity_result_judgment",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"raw_rows={final['raw_us100_rows']};feature_forward_rows={final['feature_rows_after_forward_total']};latest_nonflat={final['latest_overlap_nonflat_rows']}",
        "guardrail_kpi": "no_selection;no_forward;runtime_authority_not_claimed",
        "external_verification_status": "mt5_api_raw_data_probe_completed",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__surface_degeneracy_memory",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_runtime_parity_result_judgment",
        "evidence_scope": "MT5 API raw data probe, survivor feature staleness, surface memory",
        "kpi_scope": "data_freshness_and_decision_surface",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__surface_degeneracy_memory",
        "family": "data_integrity_runtime_parity_result_judgment",
        "question": "is latest forward data missing or is the survivor feature handoff stale and all-flat",
        "metric_scope": "raw_data_freshness_feature_staleness_surface_degeneracy",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
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
                "sha256": run336k.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": "Stage337EN surface degeneracy and raw data freshness artifact; no Forward/Goal claims.",
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_local_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    configure_raw_probe()
    args = parse_args()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    end_utc = run336k.parse_optional_utc(args.end_utc)
    raw_rows, latest = run336k.probe_latest_raw_data(Path(args.terminal_path), end_utc)
    feature_rows, surface_rows = build_feature_and_surface_rows(
        latest,
        attempt_limit=args.attempt_limit,
        latest_overlap_from=args.latest_overlap_from,
        latest_overlap_to=args.latest_overlap_to,
    )
    write_local_csv(RAW_SUMMARY, RAW_COLUMNS, raw_rows)
    write_json(RAW_LATEST, {**latest, "claim_boundary": CLAIM_BOUNDARY})
    write_local_csv(FEATURE_STALENESS, STALENESS_COLUMNS, feature_rows)
    write_local_csv(SURFACE_MEMORY, SURFACE_COLUMNS, surface_rows)

    us100 = next((row for row in raw_rows if row.get("contract_symbol") == "US100"), {})
    raw_last_close = pd.to_datetime(us100.get("last_close_utc", ""), utc=True, errors="coerce")
    forward_start = pd.Timestamp("2026-04-14T00:00:00Z")
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(missing),
        "attempt_limit": args.attempt_limit,
        "raw_symbol_rows": len(raw_rows),
        "raw_us100_status": us100.get("status", ""),
        "raw_us100_rows": int(us100.get("rows") or 0),
        "raw_us100_last_close_utc": us100.get("last_close_utc", ""),
        "raw_us100_last_close_after_forward_start": str((not pd.isna(raw_last_close)) and raw_last_close >= forward_start).lower(),
        "feature_handoff_rows": len(feature_rows),
        "feature_rows_after_forward_total": sum(int(row.get("rows_after_2026_04_14") or 0) for row in feature_rows),
        "stale_feature_handoff_rows": sum(1 for row in feature_rows if row.get("handoff_status") == "stale_before_forward_window"),
        "latest_overlap_nonflat_rows": sum(int(row.get("latest_overlap_nonflat_rows") or 0) for row in surface_rows),
        "surface_memory_rows": len(surface_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
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
    write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates)
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY})
    receipts = [
        write_json(DATA_RECEIPT, {"run_id": RUN_ID, "raw_us100_rows": final["raw_us100_rows"], "feature_rows_after_forward_total": final["feature_rows_after_forward_total"], "claim_boundary": CLAIM_BOUNDARY}),
        write_json(RUNTIME_RECEIPT, {"run_id": RUN_ID, "runtime_probe_execution": "not_run_in_en", "parent_runtime_parity": rel(em.FINAL_DECISION), "claim_boundary": CLAIM_BOUNDARY}),
        write_json(JUDGMENT_RECEIPT, {"run_id": RUN_ID, "judgment_label": "blocked_forward_feature_handoff_refresh_required", "claim_boundary": CLAIM_BOUNDARY}),
        write_json(LINEAGE_RECEIPT, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    tracked = [write_report(final), write_decision_doc(final)]
    tracked.extend(update_docs(final))
    tracked.extend(update_registers([*OUTPUT_FILES, *receipts, *tracked, *[Path(str(row.get("csv_path", ""))) for row in raw_rows if row.get("csv_path")], *[Path(str(row.get("manifest_path", ""))) for row in raw_rows if row.get("manifest_path")]], final))
    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "raw_us100_rows": final["raw_us100_rows"],
                "raw_us100_last_close_utc": final["raw_us100_last_close_utc"],
                "feature_rows_after_forward_total": final["feature_rows_after_forward_total"],
                "latest_overlap_nonflat_rows": final["latest_overlap_nonflat_rows"],
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
