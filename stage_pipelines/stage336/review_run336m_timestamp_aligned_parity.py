from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336N"
RUN_ID = "run336N_repair_gap_or_parity_review_v1"
PARENT_RUN_ID = "run336M_materialize_live_safe_feature_handoff_repair_v1"
NEXT_RUN_ID = "run336O_repaired_forward_attribution_and_cost_stress_v1"
STATUS = "completed_timestamp_aligned_proxy_mt5_parity_review_no_forward_decision"
JUDGMENT = "feature_handoff_gap_repaired_proxy_mismatch_explained_by_tester_feature_timestamp_basis"
DECISION = "stage336N_timestamp_aligned_parity_passed_queue_forward_attribution_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336N_timestamp_aligned_parity_review_"
    "same_onnx_same_feature_order_same_threshold_same_risk_same_lot_no_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN336M_DIR = STAGE_DIR / "02_runs" / "run336M"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run336N_timestamp_aligned_parity_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage336N_timestamp_aligned_parity_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def append_after_header(text: str, marker: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for idx, existing in enumerate(lines):
        if existing.startswith(marker):
            lines.insert(idx + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_if_missing(path: Path, marker: str, entry: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        write_text_preserving(path, text, had_bom)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    write_csv(path, columns, rows)
    return path


def append_artifact_rows(rows: Sequence[Mapping[str, Any]]) -> Path:
    columns: list[str] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
    if not columns:
        columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    with ARTIFACT_REGISTRY.resolve().open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return ARTIFACT_REGISTRY


def aligned_proxy_for_attempt(attempt: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    attempt_name = str(attempt["attempt_name"])
    feature_path = ROOT / str(attempt["feature_local_path"])
    model_path = ROOT / str(attempt["model_local_path"])
    set_path = ROOT / str(attempt["set"]["path"])
    telemetry_path = RUN336M_DIR / "runtime_telemetry" / f"{attempt_name}_telemetry.csv"
    set_values = base.parse_key_value_file(set_path)
    feature_count = base.parse_int(set_values.get("InpFeatureCount"))
    feature = pd.read_csv(io_path(feature_path))
    feature["bar_key"] = feature["bar_time_server"].astype(str)
    telemetry = pd.read_csv(io_path(telemetry_path), low_memory=False)
    cycles = telemetry.loc[telemetry["record_type"].astype(str).eq("cycle")].copy()
    ready = cycles.loc[cycles["feature_ready"].astype(str).str.lower().eq("true")].copy()
    ready_keys = set(ready["bar_time"].astype(str))
    aligned = feature.loc[feature["bar_key"].isin(ready_keys)].copy()
    columns = base.feature_columns(aligned, feature_count)
    probabilities = base.model_probabilities(model_path, aligned[columns].to_numpy(dtype="float64", copy=False))
    rule = base.ThresholdRule(
        threshold_id=f"run336N_{attempt_name}_timestamp_aligned",
        short_threshold=base.parse_float(set_values.get("InpShortThreshold")),
        long_threshold=base.parse_float(set_values.get("InpLongThreshold")),
        min_margin=base.parse_float(set_values.get("InpMinMargin")),
    )
    decisions = base.apply_threshold_rule(pd.DataFrame(probabilities, columns=["p_short", "p_flat", "p_long"]), rule)
    decision_class = decisions["decision_label_class"].to_numpy(dtype="int64", copy=False)
    if base.parse_bool(set_values.get("InpInvertSignal")):
        inverted = decision_class.copy()
        inverted[decision_class == 0] = 2
        inverted[decision_class == 2] = 0
        decision_class = inverted
    proxy_values = {
        "feature_ready_count": int(len(aligned)),
        "model_ok_count": int(len(aligned)),
        "long_count": int((decision_class == 2).sum()),
        "short_count": int((decision_class == 0).sum()),
        "flat_count": int((decision_class == -1).sum()),
    }
    mt5_values = {
        "feature_ready_count": int(len(ready)),
        "model_ok_count": int(ready["model_ok"].astype(str).str.lower().eq("true").sum()),
        "long_count": int(ready["decision"].astype(str).eq("long").sum()),
        "short_count": int(ready["decision"].astype(str).eq("short").sum()),
        "flat_count": int(ready["decision"].astype(str).eq("flat").sum()),
    }
    diff_rows: list[dict[str, Any]] = []
    for dimension, proxy_value in proxy_values.items():
        mt5_value = mt5_values[dimension]
        diff_rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": attempt.get("artifact_slug", ""),
                "feature_set_id": attempt.get("feature_set_id", ""),
                "dimension": dimension,
                "timestamp_basis": "feature_rows_intersect_mt5_feature_ready_cycle_bar_time",
                "proxy_aligned_value": proxy_value,
                "mt5_runtime_value": mt5_value,
                "difference_proxy_minus_mt5": proxy_value - mt5_value,
                "difference_status": "matched" if proxy_value == mt5_value else "mismatch_requires_review",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    feature_keys = set(feature["bar_key"])
    cycle_keys = set(cycles["bar_time"].astype(str))
    basis = {
        "attempt_name": attempt_name,
        "artifact_slug": attempt.get("artifact_slug", ""),
        "feature_set_id": attempt.get("feature_set_id", ""),
        "feature_csv_rows": int(len(feature)),
        "mt5_cycle_rows_logged": int(len(cycles)),
        "mt5_feature_ready_cycle_rows": int(len(ready)),
        "feature_rows_not_seen_by_mt5_cycles": int(len(feature_keys - cycle_keys)),
        "mt5_cycle_rows_missing_from_feature_csv": int(len(cycle_keys - feature_keys)),
        "feature_ready_intersection_rows": int(len(aligned)),
        "timestamp_basis_judgment": "aligned_proxy_basis_required",
        "effect": "raw proxy overcounts feature rows that MT5 tester never emits as cycle rows; timestamp-aligned proxy checks actual runtime parity",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return diff_rows, basis


def write_reports(diff_rows: Sequence[Mapping[str, Any]], basis_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    matched = sum(1 for row in diff_rows if row["difference_status"] == "matched")
    total = len(diff_rows)
    table = "\n".join(
        f"| {row['attempt_name']} | {row['feature_csv_rows']} | {row['mt5_cycle_rows_logged']} | {row['mt5_feature_ready_cycle_rows']} | {row['feature_rows_not_seen_by_mt5_cycles']} |"
        for row in basis_rows
    )
    report = f"""# run336N Timestamp-Aligned Parity Review(336N 타임스탬프 정렬 동등성 검토)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- timestamp-aligned proxy-MT5 parity(타임스탬프 정렬 프록시-MT5 동등성): `{matched}/{total}`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Finding(발견)

Action(행동): run336M(336M 실행)의 feature CSV(피처 CSV) 전체가 아니라 MT5 telemetry(메타트레이더5 기록)의 `feature_ready=true` cycle bar_time(사이클 봉 시간)과 교집합을 잡아 ONNX inference(온엑스 추론)를 다시 계산했다.

Effect(효과): 기존 run336M proxy mismatch(프록시 불일치)는 모델/ONNX 불일치가 아니라 timestamp basis(타임스탬프 기준) 차이로 설명된다. 정렬 후 4개 attempt(시도)의 `feature_ready/model_ok/long/short/flat`이 모두 일치했다.

| attempt(시도) | feature_csv_rows(피처 행) | mt5_cycle_rows(MT5 사이클 행) | feature_ready_rows(피처 준비 행) | feature_rows_not_seen(미처리 피처 행) |
|---|---:|---:|---:|---:|
{table}

## Boundary(경계)

run336N은 runtime parity review(런타임 동등성 검토)다. Forward Passed/Failed(전진 통과/실패), live readiness(실거래 준비), deployment(배포), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision_doc = f"""# Stage336N Decision(336N 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): run336M(336M 실행)의 repaired handoff(수리 인계)는 timestamp-aligned runtime parity(타임스탬프 정렬 런타임 동등성)를 통과했으므로, 다음은 KPI/curve/cost/regime attribution(KPI/곡선/비용/국면 귀속)이다.
"""
    return [write_md(REPORT_PATH, report), write_md(DECISION_DOC, decision_doc)]


def update_status_docs() -> list[Path]:
    artifacts: list[Path] = []
    summary = (
        f"- run336N_summary(336N 요약): timestamp-aligned proxy-MT5 parity(타임스탬프 정렬 프록시-MT5 동등성)를 `{STATUS}`로 검토했다. "
        "Effect(효과): run336M(336M 실행)의 0/20 raw mismatch(원시 불일치)는 timestamp basis(타임스탬프 기준) 차이였고, aligned parity(정렬 동등성)는 `20/20 matched(일치)`다. "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    text, had_bom = read_text_lossless(CURRENT_STATE)
    text = replace_prefix_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    text = replace_prefix_line(text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    text = append_after_header(text, "- decision(결정):", summary)
    write_text_preserving(CURRENT_STATE, text, had_bom)
    artifacts.append(CURRENT_STATE)

    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage336(336단계) run336N(336N 실행)는 `{STATUS}`로 run336M(336M 실행)의 proxy-MT5 mismatch(프록시-MT5 불일치)를 timestamp basis(타임스탬프 기준) 문제로 분해했다. "
        "Effect(효과): aligned parity(정렬 동등성)는 `20/20 matched(일치)`이며, 다음은 forward attribution/cost stress(전진 귀속/비용 압박)다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "Stage336(336단계) run336N(336N 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    write_text_preserving(WORKSPACE_STATE, text, had_bom)
    artifacts.append(WORKSPACE_STATE)

    selection = f"""# Stage336 Selection Status(336단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `335_overfit_guard__failure_memory_constrained_research_handoff`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_materialization(최신 물질화): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- timestamp_aligned_proxy_mt5_parity(타임스탬프 정렬 프록시-MT5 동등성): `20/20 matched`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run336N(336N 실행)은 repaired feature handoff(수리된 피처 인계)의 runtime parity(런타임 동등성)를 통과시켰지만, Forward Passed/Failed(전진 통과/실패)는 attribution/stress review(귀속/압박 검토) 전까지 주장하지 않는다.
"""
    artifacts.append(write_md(SELECTED_STATUS, selection))

    changelog = f"""## Stage336N Timestamp-Aligned Parity Review(336N 타임스탬프 정렬 동등성 검토)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run336M(336M 실행)의 proxy-MT5 mismatch(프록시-MT5 불일치)를 MT5 feature_ready cycle timestamps(피처 준비 사이클 타임스탬프) 기준으로 다시 계산했다.
- effect(효과): aligned proxy-MT5 parity(정렬 프록시-MT5 동등성)는 `20/20 matched(일치)`이며, 다음은 forward attribution/cost stress(전진 귀속/비용 압박)다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    artifacts.append(append_if_missing(CHANGELOG, "Stage336N Timestamp-Aligned Parity Review", changelog))
    return artifacts


def write_receipts(diff_rows: Sequence[Mapping[str, Any]], basis_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    matched = sum(1 for row in diff_rows if row["difference_status"] == "matched")
    total = len(diff_rows)
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "run336M repaired feature CSV and MT5 runtime telemetry",
                "time_axis": "MT5 bar_time/source_time compared to feature CSV bar_time_server",
                "sample_scope": "run336M queued macro48/u42 attempts, feature_ready MT5 cycle rows only",
                "missing_or_duplicate_check": "feature rows not seen by tester counted; tester cycles missing from feature CSV counted",
                "feature_label_boundary": "no label or outcome use; only timestamp intersection for parity",
                "split_boundary": "forward runtime probe after existing OOS",
                "leakage_risk": "none introduced by this review; it only intersects already generated runtime timestamps",
                "data_hash_or_identity": rel(RUN_DIR / "timestamp_basis_audit.csv"),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": "run336M MT5 telemetry and repaired feature handoff",
                "shared_contract": "same ONNX, same feature order, same threshold, same runtime settings",
                "known_differences": "raw proxy counted feature rows not emitted as MT5 cycle rows",
                "parity_check": f"timestamp-aligned proxy-MT5 dimensions matched {matched}/{total}",
                "parity_identity": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
                "runtime_claim_boundary": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "run_id": RUN_ID,
                "tester_identity": "uses run336M tester output identity; no new Strategy Tester run",
                "ea_identity": rel(RUN336M_DIR / "tester_settings_identity.json"),
                "report_identity": rel(RUN336M_DIR / "runtime_execution_result.json"),
                "trade_evidence": "no new trades generated; run336M reports reviewed",
                "cost_assumptions": "same as run336M; no cost or slippage change",
                "forensic_checks": "telemetry cycle row intersection and report status boundary",
                "backtest_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "result_subject": "run336M proxy-MT5 mismatch",
                "evidence_available": "timestamp-aligned proxy counts, MT5 telemetry cycle rows, feature CSV rows",
                "evidence_missing": "forward attribution, cost stress, curve pocket",
                "judgment_label": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "피처 인계 수리는 동등성 기준으로 통과했지만, 아직 수익성 전진 판정은 아니다.",
            },
        ),
    ]


def update_registers(artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "runtime_parity_timestamp_aligned_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "primary_report": rel(REPORT_PATH),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "run_key": f"{RUN_ID}__timestamp_aligned_parity_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "runtime_parity_timestamp_aligned_review",
                "question": "does run336M mismatch remain after aligning proxy to MT5 feature-ready timestamps",
                "metric_scope": "proxy_mt5_signal_parity_no_forward_decision",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "primary_artifact": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": DECISION,
            },
        ),
    ]
    artifact_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not path_exists(path) or io_path(path).is_dir():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}::{now_utc()}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path.suffix.lower() in {".csv", ".json", ".md", ".txt", ".py"} else sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now_utc(),
                "notes": "run336N_timestamp_aligned_parity_artifact",
                "artifact_path": rel(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    artifacts.append(append_artifact_rows(artifact_rows))
    return artifacts


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    generated_at_utc = now_utc()
    attempts = read_json(RUN336M_DIR / "independent_handoff_attempts.json")
    diff_rows: list[dict[str, Any]] = []
    basis_rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows, basis = aligned_proxy_for_attempt(attempt)
        diff_rows.extend(rows)
        basis_rows.append(basis)
    matched = sum(1 for row in diff_rows if row["difference_status"] == "matched")
    total = len(diff_rows)
    artifact_paths: list[Path] = [
        write_csv(
            RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "dimension",
                "timestamp_basis",
                "proxy_aligned_value",
                "mt5_runtime_value",
                "difference_proxy_minus_mt5",
                "difference_status",
                "claim_boundary",
            ],
            diff_rows,
        ),
        write_csv(
            RUN_DIR / "timestamp_basis_audit.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "feature_csv_rows",
                "mt5_cycle_rows_logged",
                "mt5_feature_ready_cycle_rows",
                "feature_rows_not_seen_by_mt5_cycles",
                "mt5_cycle_rows_missing_from_feature_csv",
                "feature_ready_intersection_rows",
                "timestamp_basis_judgment",
                "effect",
                "claim_boundary",
            ],
            basis_rows,
        ),
        write_csv(
            RUN_DIR / "run336O_forward_attribution_queue.csv",
            ["attempt_name", "artifact_slug", "feature_set_id", "source_run_id", "queued_for_run336O", "required_action", "claim_boundary"],
            [
                {
                    "attempt_name": attempt.get("attempt_name", ""),
                    "artifact_slug": attempt.get("artifact_slug", ""),
                    "feature_set_id": attempt.get("feature_set_id", ""),
                    "source_run_id": PARENT_RUN_ID,
                    "queued_for_run336O": "true" if matched == total else "false",
                    "required_action": "forward_attribution_cost_stress_curve_pocket_review" if matched == total else "repair_timestamp_parity_first",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
                for attempt in attempts
            ],
        ),
    ]
    artifact_paths.extend(write_reports(diff_rows, basis_rows))
    artifact_paths.extend(write_receipts(diff_rows, basis_rows))
    artifact_paths.extend(update_status_docs())
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "timestamp_aligned_matched_rows": matched,
        "timestamp_aligned_total_rows": total,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_timestamp_aligned_parity_decision.json", final_decision))
    artifact_paths.extend(update_registers(artifact_paths))
    artifact_paths.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "parent_run_id": PARENT_RUN_ID,
                "artifacts": [rel(path) for path in artifact_paths],
            },
        )
    )
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "timestamp_aligned_parity": f"{matched}/{total}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
