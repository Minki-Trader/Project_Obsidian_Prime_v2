from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage56 import context_extratrees_agreement_branch as s56
from stage_pipelines.stage258 import short_tight_margin_pf_repair_after_stage256_tradeoff as s258
from stage_pipelines.stage262 import lowrank_lowedge_oos_recovery_repair as s262
from stage_pipelines.stage264 import dual_objective_lowrank_lowedge_repair as s264


STAGE_ID = "267_adapter_research__baseline_candidate_racing_protocol"
RUN_ID = "run267B_stage267_extended_period_ablation_probe_v1"
RUN_NUMBER = "run267B"
PACKET_ID = "stage267_baseline_candidate_racing_protocol_v1"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
HIST_ROOT = RUN_ROOT / "historical_2024"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

SOURCE_VARIANT_ID = "v41_v22_midcov_et40_agree_h2c0_no_b"
SOURCE_SIGNAL_COLUMN = "stage56_context_et_event_signal"
PERIOD_LABEL = "historical_2024_tier_a_train_era_stress"
COMMON_ROOT = "OPV2/s267b/run267B_2024"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_goal_gate"
)

RUN_MANIFEST_PATH = HIST_ROOT / "manifest.json"
FEATURE_MANIFEST_PATH = HIST_ROOT / "features.csv"
GATE_SUMMARY_PATH = HIST_ROOT / "gates.csv"
MONTHLY_GATE_SUMMARY_PATH = HIST_ROOT / "monthly_gates.csv"
ATTEMPT_MANIFEST_PATH = HIST_ROOT / "attempts.csv"
REPORT_PATH = REVIEWS_ROOT / "stage267_historical_2024_probe_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/historical_stress_2024_probe.py")


@dataclass(frozen=True)
class CandidateSpec:
    candidate_id: str
    alias: str
    role: str
    source_stage: str
    module: Any
    variant: Any
    model_path: Path


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        number = float(value)
        if not math.isfinite(number):
            return ""
        return f"{number:.17g}"
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def upsert_csv(path: Path, key: str, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    existing = read_csv_rows(path)
    replacements = {str(row[key]): row for row in rows}
    merged: list[Mapping[str, Any]] = []
    seen: set[str] = set()
    for row in existing:
        row_key = str(row.get(key, ""))
        if row_key in replacements:
            merged.append(replacements[row_key])
            seen.add(row_key)
        else:
            merged.append(row)
    for row_key, row in replacements.items():
        if row_key not in seen:
            merged.append(row)
    write_csv(path, merged, columns)


def variant_for(module: Any, adapter_id: str) -> Any:
    for variant in module.VARIANTS:
        if variant.adapter_id == adapter_id:
            return variant
    raise KeyError(adapter_id)


def candidate_specs() -> tuple[CandidateSpec, ...]:
    return (
        CandidateSpec(
            "s264_allow_inner_high_quarter",
            "s264_aih",
            "challenger_core",
            "264",
            s264,
            variant_for(s264, "s264_allow_inner_high_quarter"),
            Path(
                "stages/264_adapter_research__dual_objective_lowrank_lowedge_repair/"
                "02_runs/run264A/s264_allow_inner_high_quarter/models/"
                "s264_allow_inner_high_quarter_model.csv"
            ),
        ),
        CandidateSpec(
            "s264_lowrank_control",
            "s264_lc",
            "defensive_control",
            "264",
            s264,
            variant_for(s264, "s264_lowrank_control"),
            Path(
                "stages/264_adapter_research__dual_objective_lowrank_lowedge_repair/"
                "02_runs/run264A/s264_lowrank_control/models/s264_lowrank_control_model.csv"
            ),
        ),
        CandidateSpec(
            "s262_lowrank_inner_half_filter",
            "s262_lih",
            "validation_heavy",
            "262",
            s262,
            variant_for(s262, "s262_lowrank_inner_half_filter"),
            Path(
                "stages/262_adapter_research__lowrank_lowedge_oos_recovery_repair/"
                "02_runs/run262A/s262_lowrank_inner_half_filter/models/"
                "s262_lowrank_inner_half_filter_model.csv"
            ),
        ),
        CandidateSpec(
            "s264_allow_inner_all_oos_anchor",
            "s264_aia",
            "oos_anchor",
            "264",
            s264,
            variant_for(s264, "s264_allow_inner_all_oos_anchor"),
            Path(
                "stages/264_adapter_research__dual_objective_lowrank_lowedge_repair/"
                "02_runs/run264A/s264_allow_inner_all_oos_anchor/models/"
                "s264_allow_inner_all_oos_anchor_model.csv"
            ),
        ),
        CandidateSpec(
            "s258_short_tight_control",
            "s258_stc",
            "stress_challenger",
            "258",
            s258,
            variant_for(s258, "s258_short_tight_control"),
            Path(
                "stages/258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff/"
                "02_runs/run258A/s258_short_tight_control/models/s258_short_tight_control_model.csv"
            ),
        ),
    )


def build_2024_source_frame() -> tuple[pd.DataFrame, dict[str, Any]]:
    s56.patch_context()
    common, route_coverage, _ = s56.aw.build_common_table()
    variant = next(item for item in s56.DEFAULT_VARIANTS if item.variant_id == SOURCE_VARIANT_ID)
    frame = s56.build_variant_frame(common, variant)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    tier_a = frame.loc[
        frame["split"].astype(str).eq("train")
        & frame["tier_label"].astype(str).eq(s56.ctx.mt5.TIER_A)
    ].copy()
    tier_a = tier_a.loc[
        tier_a["timestamp"].ge(pd.Timestamp("2024-01-01", tz="UTC"))
        & tier_a["timestamp"].lt(pd.Timestamp("2025-01-01", tz="UTC"))
    ].sort_values("timestamp")
    if tier_a.empty:
        raise RuntimeError("empty 2024 Tier A source frame")
    duplicates = int(tier_a["timestamp"].duplicated().sum())
    missing_signal = int(pd.to_numeric(tier_a[SOURCE_SIGNAL_COLUMN], errors="coerce").isna().sum())
    info = {
        "source_variant_id": SOURCE_VARIANT_ID,
        "source_signal_column": SOURCE_SIGNAL_COLUMN,
        "rows": int(len(tier_a)),
        "first_time_utc": tier_a["timestamp"].min().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_time_utc": tier_a["timestamp"].max().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "split": "train",
        "tier": s56.ctx.mt5.TIER_A,
        "duplicates": duplicates,
        "missing_signal_rows": missing_signal,
        "route_coverage_rows": int(len(route_coverage)) if hasattr(route_coverage, "__len__") else None,
    }
    return tier_a, info


def row_mapping(row: Mapping[str, Any]) -> dict[str, str]:
    timestamp = pd.Timestamp(row["timestamp"])
    return {
        "bar_time_server": timestamp.strftime("%Y.%m.%d %H:%M:%S"),
        "timestamp_utc": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        SOURCE_SIGNAL_COLUMN: csv_value(int(round(float(row[SOURCE_SIGNAL_COLUMN])))),
        "et40_decision_margin": csv_value(float(row.get("et40_decision_margin", 1.0))),
        "minutes_from_cash_open": csv_value(row.get("minutes_from_cash_open")),
    }


def base_extra_set_values(spec: CandidateSpec, magic: int) -> dict[str, Any]:
    values = s264.s250.stage238.s161.base.engine.extra_set_values(spec.variant, magic)
    extra = spec.module.VARIANT_EXTRAS[spec.candidate_id]
    values["InpSideFilterEnabled"] = True
    values["InpSideFilterFeatureIndex"] = 2
    values["InpFallbackSideFilterFeatureIndex"] = 2
    values["InpBlockShortFeatureRange"] = True
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = True
    values["InpBlockLongFeatureMin"] = 1.5
    values["InpBlockLongFeatureMax"] = 2.5
    values["InpModelRiskConfidenceFloor"] = float(extra["risk_confidence_floor"])
    values["InpModelRiskConfidenceCeiling"] = float(extra["risk_confidence_ceiling"])
    values["InpMagic"] = magic
    return values


def summarize_feature_rows(
    spec: CandidateSpec,
    source: pd.DataFrame,
    destination: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    extra = spec.module.VARIANT_EXTRAS[spec.candidate_id]
    branch_mode = str(extra["source_branch_mode"])
    rank_column = str(spec.module.RANK_COLUMN)
    gate_column = f"{spec.module.GATE_COLUMN_PREFIX}_{extra['axis']}"
    fieldnames = ("bar_time_server", SOURCE_SIGNAL_COLUMN, rank_column, gate_column)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)

    totals = {
        "total_rows": 0,
        "signal_rows": 0,
        "long_signal_rows": 0,
        "short_signal_rows": 0,
        "blocked_signal_rows": 0,
        "blocked_long_signal_rows": 0,
        "blocked_short_signal_rows": 0,
        "allowed_signal_rows": 0,
        "context_missing_minutes_rows": 0,
    }
    rank_counts = {name: 0 for name in ("low", "mid", "high", "vhigh")}
    allowed_rank_counts = {name: 0 for name in ("low", "mid", "high", "vhigh")}
    monthly: dict[str, dict[str, Any]] = {}

    with io_path(destination).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for record in source.to_dict("records"):
            mapped = row_mapping(record)
            signal = int(round(spec.module.s250.stage238.parse_float(mapped.get(SOURCE_SIGNAL_COLUMN), 0.0)))
            bucket_value, bucket_label = spec.module.s250.stage238.rank_bucket_for(mapped)
            minutes = spec.module.s250.stage238.s174.s167_minutes_for(mapped)
            if minutes is None:
                totals["context_missing_minutes_rows"] += 1
            gate = spec.module.source_branch_gate_value(mapped, branch_mode)
            month = mapped["timestamp_utc"][:7]
            if month not in monthly:
                monthly[month] = {
                    "candidate_id": spec.candidate_id,
                    "role": spec.role,
                    "source_stage": spec.source_stage,
                    "period_label": PERIOD_LABEL,
                    "month": month,
                    "rows": 0,
                    "signal_rows": 0,
                    "long_signal_rows": 0,
                    "short_signal_rows": 0,
                    "blocked_signal_rows": 0,
                    "allowed_signal_rows": 0,
                }
            totals["total_rows"] += 1
            rank_counts[bucket_label] += 1
            monthly[month]["rows"] += 1
            if signal != 0:
                totals["signal_rows"] += 1
                monthly[month]["signal_rows"] += 1
                if signal > 0:
                    totals["long_signal_rows"] += 1
                    monthly[month]["long_signal_rows"] += 1
                else:
                    totals["short_signal_rows"] += 1
                    monthly[month]["short_signal_rows"] += 1
                if gate >= 0.5:
                    totals["blocked_signal_rows"] += 1
                    monthly[month]["blocked_signal_rows"] += 1
                    if signal > 0:
                        totals["blocked_long_signal_rows"] += 1
                    else:
                        totals["blocked_short_signal_rows"] += 1
                else:
                    totals["allowed_signal_rows"] += 1
                    monthly[month]["allowed_signal_rows"] += 1
                    allowed_rank_counts[bucket_label] += 1
            writer.writerow(
                {
                    "bar_time_server": mapped["bar_time_server"],
                    SOURCE_SIGNAL_COLUMN: csv_value(float(signal)),
                    rank_column: csv_value(float(bucket_value)),
                    gate_column: csv_value(gate),
                }
            )

    signal_rows = max(int(totals["signal_rows"]), 1)
    summary = {
        "candidate_id": spec.candidate_id,
        "role": spec.role,
        "source_stage": spec.source_stage,
        "period_label": PERIOD_LABEL,
        "branch_mode": branch_mode,
        "rank_column": rank_column,
        "gate_column": gate_column,
        **totals,
        "blocked_signal_ratio": totals["blocked_signal_rows"] / signal_rows,
        "allowed_signal_ratio": totals["allowed_signal_rows"] / signal_rows,
        "rank_low_rows": rank_counts["low"],
        "rank_mid_rows": rank_counts["mid"],
        "rank_high_rows": rank_counts["high"],
        "rank_vhigh_rows": rank_counts["vhigh"],
        "allowed_low_signal_rows": allowed_rank_counts["low"],
        "allowed_mid_signal_rows": allowed_rank_counts["mid"],
        "allowed_high_signal_rows": allowed_rank_counts["high"],
        "allowed_vhigh_signal_rows": allowed_rank_counts["vhigh"],
        "gate_description": extra["gate_description"],
    }
    monthly_rows: list[dict[str, Any]] = []
    for row in monthly.values():
        month_signals = max(int(row["signal_rows"]), 1)
        row["blocked_signal_ratio"] = int(row["blocked_signal_rows"]) / month_signals
        row["allowed_signal_ratio"] = int(row["allowed_signal_rows"]) / month_signals
        monthly_rows.append(row)
    return summary, sorted(monthly_rows, key=lambda item: (item["month"], item["candidate_id"]))


def copy_model(spec: CandidateSpec, destination: Path) -> dict[str, Any]:
    if not path_exists(spec.model_path):
        raise FileNotFoundError(spec.model_path)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(spec.model_path), io_path(destination))
    return {
        "source_model": rel(spec.model_path),
        "model_file": rel(destination),
        "model_sha256": sha256_file_lf_normalized(destination),
    }


def build_attempts(
    specs: Sequence[CandidateSpec],
    model_exports: Mapping[str, Mapping[str, Any]],
    feature_exports: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, spec in enumerate(specs, start=1):
        candidate_root = HIST_ROOT
        for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
            (
                (mt5.TIER_A, "tier_only_total", f"mt5_ta_{spec.alias}", "ta"),
                (mt5.TIER_AB, "routed_total", f"mt5_rt_{spec.alias}", "rt"),
            ),
            start=1,
        ):
            magic = 26710000 + variant_index * 100 + role_index
            payload = attempt_payload(
                run_root=candidate_root,
                run_id=RUN_ID,
                stage_number=267,
                exploration_label="stage267_BaselineRacing__Historical2024Stress",
                attempt_name=f"{spec.alias}_{attempt_token}_2024",
                tier=tier,
                split=PERIOD_LABEL,
                model_path=str(model_exports[spec.candidate_id]["common_path"]),
                model_id=f"{RUN_ID}_{spec.candidate_id}_entry_adapter_2024",
                model_backend="ebm_table",
                feature_path=str(feature_exports[spec.candidate_id]["common_path"]),
                feature_count=3,
                feature_order_hash=str(feature_exports[spec.candidate_id]["feature_order_hash"]),
                short_threshold=spec.variant.short_threshold,
                long_threshold=spec.variant.long_threshold,
                min_margin=0.0,
                invert_signal=False,
                from_date="2024.01.02",
                to_date="2025.01.01",
                primary_active_tier="tier_a",
                attempt_role=attempt_role,
                record_view_prefix=prefix,
                max_hold_bars=spec.variant.max_hold_bars,
                common_root=f"{COMMON_ROOT}/{spec.alias}",
                fallback_enabled=False,
                close_on_flat_signal=spec.variant.close_on_flat_signal,
                reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                extra_set_values=base_extra_set_values(spec, magic),
            )
            payload["candidate_id"] = spec.candidate_id
            payload["candidate_alias"] = spec.alias
            attempts.append(payload)
    return attempts


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for attempt in attempts:
        rows.append(
            {
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "attempt_name": attempt["attempt_name"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "attempt_role": attempt["attempt_role"],
                "record_view_prefix": attempt["record_view_prefix"],
                "set_path": attempt["set"]["path"],
                "set_sha256": attempt["set"]["sha256"],
                "ini_path": attempt["ini"]["path"],
                "ini_sha256": attempt["ini"]["sha256"],
                "common_telemetry_path": attempt["common_telemetry_path"],
                "common_summary_path": attempt["common_summary_path"],
                "fallback_enabled": attempt.get("fallback_enabled", False),
            }
        )
    return rows


def upsert_stage_ledger() -> None:
    row = {
        "row_id": "stage267_run267B_historical_2024_input_materialized",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "historical_2024_input_materialization",
        "tier_scope": "Tier A train-era historical stress",
        "scoreboard": "structural_scout",
        "status": "completed_input_materialized",
        "judgment": "not_yet_mt5_evaluated",
        "evidence_boundary": "historical_2024_feature_gate_manifest_only_no_mt5_kpi",
        "report_path": rel(REPORT_PATH),
        "notes": (
            "Stage56 v41 Tier A 2024 source frame regenerated and candidate feature/gate inputs "
            "materialized for MT5 execution; no selected candidate, no ONNX readiness, no operating meaning."
        ),
    }
    columns = (
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
    upsert_csv(STAGE_LEDGER_PATH, "row_id", (row,), columns)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267B_historical_2024_script", "producer_script", PRODUCER_PATH, "2024 historical stress input materialization producer."),
        ("stage267_run267B_historical_2024_manifest", "run_manifest", RUN_MANIFEST_PATH, "Historical 2024 materialized attempt manifest."),
        ("stage267_run267B_historical_2024_feature_manifest", "feature_manifest", FEATURE_MANIFEST_PATH, "Candidate 2024 feature/model/common-file manifest."),
        ("stage267_run267B_historical_2024_gate_summary", "gate_summary", GATE_SUMMARY_PATH, "Candidate 2024 gate/rank summary."),
        ("stage267_run267B_historical_2024_monthly_gate_summary", "monthly_gate_summary", MONTHLY_GATE_SUMMARY_PATH, "Candidate 2024 monthly gate/rank summary."),
        ("stage267_run267B_historical_2024_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 set/ini attempt list for 2024 stress."),
        ("stage267_run267B_historical_2024_report", "review_report", REPORT_PATH, "Data integrity boundary and next execution report."),
    )
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in entries:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    return rows


def upsert_artifact_registry(created_at: str) -> None:
    columns = (
        "artifact_id",
        "artifact_type",
        "path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
    )
    upsert_csv(ARTIFACT_REGISTRY_PATH, "artifact_id", artifact_rows(created_at), columns)


def report_markdown(
    source_info: Mapping[str, Any],
    feature_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    attempt_count: int,
) -> str:
    candidates = ", ".join(f"`{row['candidate_id']}`" for row in feature_rows)
    return f"""# Stage267 Historical 2024 Probe Report(267단계 2024 과거 압박 보고)

- action(행동): Stage56 v41(56단계 v41) Tier A(티어 A) 2024 train-era(학습 기간) source signal(원천 신호)을 다시 만들고, 후보별 3-feature(3개 피처) MT5 input(입력)을 생성했다.
- effect(효과): 다섯 후보를 같은 2024 historical stress(2024 과거 압박) 조건에서 실행할 수 있게 되었지만, 아직 MT5 KPI(MT5 성과 지표)는 없다.
- candidates(후보): {candidates}
- attempts(시도): `{attempt_count}` MT5 tester set/ini(테스터 설정/초기화) files(파일)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): Stage56(56단계) `{SOURCE_VARIANT_ID}` regenerated frame(재생성 프레임), plus source model CSV(원천 모델 CSV) copied from Stage258/262/264(258/262/264단계).
- time_axis(시간축): `timestamp` is UTC(UTC), `bar_time_server` is written as `YYYY.MM.DD HH:MM:SS` for MT5(MetaTrader 5, 메타트레이더5) timestamp match(시간 일치).
- sample_scope(표본 범위): US100 M5, Tier A(티어 A), train split(학습 분할), `{source_info['first_time_utc']}` to `{source_info['last_time_utc']}`, rows(행) `{source_info['rows']}`.
- missing_or_duplicate_check(누락/중복 확인): duplicate timestamps(중복 시간) `{source_info['duplicates']}`, missing signal rows(신호 누락 행) `{source_info['missing_signal_rows']}`.
- feature_label_boundary(피처/라벨 경계): this pass(이번 회차)는 label(라벨)을 새로 붙이지 않고 existing source signal/gate(기존 원천 신호/게이트)만 재생성한다.
- split_boundary(분할 경계): 2024 is train-era historical stress(학습 기간 과거 압박) only; it is not OOS(표본외)가 아니다.
- leakage_risk(누수 위험): high(높음) if interpreted as OOS(표본외) or used for promotion(승격); acceptable only as break-resistance probe(깨짐 저항 탐침).
- data_hash_or_identity(데이터 해시/정체성): feature manifest(피처 목록) `{rel(FEATURE_MANIFEST_PATH)}` and gate summary(게이트 요약) `{rel(GATE_SUMMARY_PATH)}`.
- integrity_judgment(무결성 판정): `usable_with_boundary`.

## Gate Read(게이트 판독)

This is not performance attribution(성과 귀속) yet. It only tells how much signal supply(신호 공급)가 each candidate(각 후보) blocks(차단) before MT5 execution(실행).

| candidate(후보) | signal_rows(신호 행) | allowed_signal_rows(허용 신호 행) | blocked_signal_ratio(차단 비율) |
| --- | ---: | ---: | ---: |
{chr(10).join(f"| `{row['candidate_id']}` | {row['signal_rows']} | {row['allowed_signal_rows']} | {float(row['blocked_signal_ratio']):.4f} |" for row in gate_rows)}

## Performance Attribution Boundary(성과 귀속 경계)

- observed_change(관측 변화): none(없음), because MT5 KPI(MT5 성과 지표) has not run.
- comparison_baseline(비교 기준): Stage267(267단계) initial scoreboard(초기 점수판) and existing validation/OOS(검증/표본외) MT5 reports(보고서).
- likely_drivers(가능 동인): unknown(미상) until 2024 tester reports(테스터 보고서), balance/equity curve(잔액/평가금 곡선), trade count(거래 수)가 나온다.
- segment_checks(구간 확인): monthly gate supply(月별 게이트 공급)는 materialized(산출물화)됨; monthly KPI(月별 성과 지표)는 missing_required(필수 누락).
- trade_shape(거래 형태): missing_required(필수 누락), because no tester output(테스터 출력) yet.
- attribution_confidence(귀속 신뢰도): `inconclusive`.
- next_probe(다음 탐침): execute MT5(메타트레이더5 실행) 2024 historical stress(2024 과거 압박) for all attempts(전체 시도), then grade balance/equity full and zoom(전체/확대 평가금 곡선).

## Judgment(판정)

- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- operating meaning(운영 의미): `none`
"""


def materialize(common_files_root: Path) -> dict[str, Any]:
    created_at = utc_now()
    specs = candidate_specs()
    source, source_info = build_2024_source_frame()
    feature_manifest: list[dict[str, Any]] = []
    gate_summary: list[dict[str, Any]] = []
    monthly_gate_summary: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    model_exports: dict[str, dict[str, Any]] = {}
    feature_exports: dict[str, dict[str, Any]] = {}

    for spec in specs:
        feature_path = HIST_ROOT / "features" / f"{spec.alias}.csv"
        model_path = HIST_ROOT / "models" / f"{spec.alias}_model.csv"
        gate_row, monthly_rows = summarize_feature_rows(spec, source, feature_path)
        model_row = copy_model(spec, model_path)
        feature_order = (SOURCE_SIGNAL_COLUMN, gate_row["rank_column"], gate_row["gate_column"])
        feature_hash = ordered_hash(feature_order)
        feature_common_path = f"{COMMON_ROOT}/{spec.alias}/features/{feature_path.name}"
        model_common_path = f"{COMMON_ROOT}/{spec.alias}/models/{model_path.name}"
        feature_copy = copy_to_common(feature_path, feature_common_path, common_files_root)
        model_copy = copy_to_common(model_path, model_common_path, common_files_root)
        common_copies.extend((feature_copy, model_copy))
        model_exports[spec.candidate_id] = {
            **model_row,
            "common_path": model_common_path,
            "common_sha256": model_copy["sha256"],
            "feature_order": list(feature_order),
            "feature_order_hash": feature_hash,
            "feature_count": 3,
        }
        feature_exports[spec.candidate_id] = {
            "feature_file": rel(feature_path),
            "feature_sha256": sha256_file_lf_normalized(feature_path),
            "common_path": feature_common_path,
            "common_sha256": feature_copy["sha256"],
            "feature_order": list(feature_order),
            "feature_order_hash": feature_hash,
            "feature_count": 3,
        }
        feature_manifest.append(
            {
                "candidate_id": spec.candidate_id,
                "candidate_alias": spec.alias,
                "role": spec.role,
                "source_stage": spec.source_stage,
                "period_label": PERIOD_LABEL,
                "feature_file": rel(feature_path),
                "feature_sha256": sha256_file_lf_normalized(feature_path),
                "model_file": rel(model_path),
                "model_sha256": model_row["model_sha256"],
                "common_feature_path": feature_common_path,
                "common_feature_sha256": feature_copy["sha256"],
                "common_model_path": model_common_path,
                "common_model_sha256": model_copy["sha256"],
                "rows": gate_row["total_rows"],
                "first_time_utc": source_info["first_time_utc"],
                "last_time_utc": source_info["last_time_utc"],
                "feature_order": ";".join(feature_order),
                "feature_order_hash": feature_hash,
                "rank_column": gate_row["rank_column"],
                "gate_column": gate_row["gate_column"],
                "branch_mode": gate_row["branch_mode"],
                "readiness_note": "materialized_for_mt5_2024_historical_stress_no_kpi_yet",
            }
        )
        gate_summary.append(gate_row)
        monthly_gate_summary.extend(monthly_rows)

    attempts = build_attempts(specs, model_exports, feature_exports)
    write_csv(FEATURE_MANIFEST_PATH, feature_manifest)
    write_csv(GATE_SUMMARY_PATH, gate_summary)
    write_csv(MONTHLY_GATE_SUMMARY_PATH, monthly_gate_summary)
    write_csv(ATTEMPT_MANIFEST_PATH, attempt_rows(attempts))
    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "period_label": PERIOD_LABEL,
        "created_at_utc": created_at,
        "status": "historical_2024_input_materialized_mt5_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_info": source_info,
        "candidate_pool": [spec.candidate_id for spec in specs],
        "feature_manifest": rel(FEATURE_MANIFEST_PATH),
        "gate_summary": rel(GATE_SUMMARY_PATH),
        "monthly_gate_summary": rel(MONTHLY_GATE_SUMMARY_PATH),
        "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
        "attempts": attempts,
        "common_copies": common_copies,
        "model_exports": model_exports,
        "feature_exports": feature_exports,
        "execution_status": "not_executed_input_materialized_only",
        "forbidden_claims": [
            "deployment",
            "live_readiness",
            "runtime_authority",
            "operating_promotion",
            "operating_reference",
            "production_baseline",
            "overall_goal_complete",
        ],
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    write_md(REPORT_PATH, report_markdown(source_info, feature_manifest, gate_summary, len(attempts)))
    upsert_stage_ledger()
    upsert_artifact_registry(created_at)
    return run_manifest


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--common-files-root", type=Path, default=COMMON_FILES_ROOT_DEFAULT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    manifest = materialize(args.common_files_root)
    print(json.dumps({"status": manifest["status"], "attempts": len(manifest["attempts"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
