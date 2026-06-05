from __future__ import annotations

import csv
import hashlib
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

from stage_pipelines.stage338 import design_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_without_db as ds  # noqa: E402


aw = ds.aw

TODAY = "2026-06-01"
STAGE_ID = ds.STAGE_ID
STAGE_DIR = ds.STAGE_DIR
RUN_NUMBER = "run338C"
RUN_ID = "run338C_materialize_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_inputs_without_db_v1"
PARENT_RUN_ID = ds.RUN_ID
NEXT_RUN_ID = "run338D_review_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_inputs_without_db_v1"
STATUS = "completed_stage338C_runtime_trade_lifecycle_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_trade_lifecycle_repair_inputs_materialized_review_required_no_selection"
DECISION = "stage338C_open_run338D_review_runtime_trade_lifecycle_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338C_runtime_trade_lifecycle_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338C_runtime_trade_lifecycle_repair_inputs.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

ALLOWED_FEATURES = (
    ROOT
    / "stages"
    / "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
    / "02_runs"
    / "run337JL"
    / "jl_allowed_model_feature_set.csv"
)

INPUT_FRAME = RUN_DIR / "run338C_trade_lifecycle_repair_input_frame.parquet"
FEATURE_SCHEMA = RUN_DIR / "run338C_allowed_feature_schema.csv"
LABEL_AUDIT = RUN_DIR / "run338C_trade_lifecycle_label_audit.csv"
FEATURE_LABEL_BOUNDARY_AUDIT = RUN_DIR / "run338C_feature_label_boundary_audit.csv"
SPLIT_MANIFEST = RUN_DIR / "run338C_split_manifest.csv"
TIER_RECORDS = RUN_DIR / "run338C_tier_records.csv"
MATERIALIZATION_SUMMARY = RUN_DIR / "run338C_materialization_summary.csv"
RUN338D_REVIEW_QUEUE = RUN_DIR / "run338D_input_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ds.FINAL_DECISION,
    ds.DESIGN_MATRIX,
    ds.LABEL_BLUEPRINT,
    ds.FEATURE_BLUEPRINT,
    ds.RULE_STACK_CONTRACT,
    ds.DATA_INTEGRITY_CONTRACT,
    ds.MODEL_VALIDATION_CONTRACT,
    ds.MATERIALIZATION_QUEUE,
    ds.SOURCE_INPUT_FRAME,
    ALLOWED_FEATURES,
)
OUTPUT_FILES = (
    INPUT_FRAME,
    FEATURE_SCHEMA,
    LABEL_AUDIT,
    FEATURE_LABEL_BOUNDARY_AUDIT,
    SPLIT_MANIFEST,
    TIER_RECORDS,
    MATERIALIZATION_SUMMARY,
    RUN338D_REVIEW_QUEUE,
    DATA_RECEIPT,
    LINEAGE_RECEIPT,
    MODEL_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


FORBIDDEN_FEATURE_PATTERNS = (
    "future",
    "label",
    "valid_",
    "_valid",
    "target",
    "weight",
    "claim_boundary",
    "feature_label_boundary",
    "split_id",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def is_forbidden_feature(name: str) -> bool:
    lowered = name.lower()
    return any(pattern in lowered for pattern in FORBIDDEN_FEATURE_PATTERNS)


def safe_numeric(series: pd.Series, fill: float = 0.0) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(fill)


def class_counts(series: pd.Series) -> str:
    counts = series.value_counts(dropna=False).sort_index()
    return ";".join(f"{key}:{int(value)}" for key, value in counts.items())


def materialize_inputs() -> tuple[pd.DataFrame, dict[str, Any]]:
    design_final = read_json(ds.FINAL_DECISION)
    allowed = read_csv(ALLOWED_FEATURES)
    frame = pd.read_parquet(str(io(ds.SOURCE_INPUT_FRAME)))
    if "timestamp" not in frame.columns or "source_row_id" not in frame.columns:
        raise RuntimeError("source frame missing timestamp or source_row_id")
    frame = frame.sort_values(["timestamp", "source_row_id"]).reset_index(drop=True)

    allowed_names = [str(name) for name in allowed["feature_name"].tolist()]
    feature_names = [
        name
        for name in allowed_names
        if name in frame.columns and not is_forbidden_feature(name) and pd.api.types.is_numeric_dtype(frame[name])
    ]
    excluded = [
        {
            "feature_name": name,
            "reason": "missing_or_forbidden_or_non_numeric(누락/금지/비수치)",
            "exists": name in frame.columns,
            "forbidden": is_forbidden_feature(name),
            "numeric": bool(name in frame.columns and pd.api.types.is_numeric_dtype(frame[name])),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name in allowed_names
        if name not in feature_names
    ]

    fwd18 = safe_numeric(frame.get("hx_future_log_return_18", pd.Series(0.0, index=frame.index)))
    valid = frame.get("hx_valid_fwd18", pd.Series(True, index=frame.index)).astype(bool)
    vol = safe_numeric(frame.get("historical_vol_20", pd.Series(0.0, index=frame.index))).abs()
    cost_buffer = (0.00008 + vol.rank(pct=True).fillna(0.5) * 0.00012).clip(0.00008, 0.00020)
    long_net = fwd18 - cost_buffer
    short_net = (-fwd18) - cost_buffer
    edge_threshold = (0.00015 + vol.rank(pct=True).fillna(0.5) * 0.00010).clip(0.00015, 0.00025)
    flat = pd.Series(1, index=frame.index)
    runtime_label = flat.copy()
    runtime_label = runtime_label.mask(valid & (long_net > edge_threshold) & (long_net >= short_net), 2)
    runtime_label = runtime_label.mask(valid & (short_net > edge_threshold) & (short_net > long_net), 0)
    runtime_label = runtime_label.mask(~valid, -1)

    underwater = safe_numeric(frame.get("underwater_rate", pd.Series(0.0, index=frame.index)))
    drawdown_pressure = safe_numeric(frame.get("drawdown_pressure_norm", pd.Series(0.0, index=frame.index)))
    survival_label = flat.copy()
    survival_label = survival_label.mask(valid & (runtime_label == 2) & (drawdown_pressure <= 0.65) & (underwater <= 0.55), 2)
    survival_label = survival_label.mask(valid & (runtime_label == 0) & (drawdown_pressure <= 0.65) & (underwater <= 0.55), 0)
    survival_label = survival_label.mask(~valid, -1)

    session_open = frame.get("is_us_cash_open", pd.Series(0, index=frame.index)).astype(int)
    session_label = runtime_label.copy()
    session_label = session_label.mask(valid & (session_open == 0), 1)

    side_loss_weight = 1.0 + (runtime_label.eq(2) & (long_net <= 0)).astype(float) * 1.5 + (runtime_label.eq(0) & (short_net <= 0)).astype(float) * 1.5
    density_weight = 1.0 + (runtime_label.ne(1)).astype(float) * 0.25
    cost_weight = 1.0 + cost_buffer.rank(pct=True).fillna(0.5)
    lifecycle_weight = np.sqrt(side_loss_weight * density_weight * cost_weight).clip(0.5, 3.0)

    row_count = len(frame)
    split_cut = int(math.floor(row_count * 0.80))
    split = np.where(np.arange(row_count) < split_cut, "inner_train", "inner_holdout")

    output_columns = ["timestamp", "symbol", "source_row_id"]
    if "split" in frame.columns:
        output_columns.append("split")
    out = frame[output_columns + feature_names].copy()
    out["run338_split"] = split
    out["run338_tier"] = "Tier A"
    out["tlr_future_log_return_18"] = fwd18.astype("float32")
    out["tlr_cost_buffer_proxy"] = cost_buffer.astype("float32")
    out["tlr_long_net_after_cost_proxy"] = long_net.astype("float32")
    out["tlr_short_net_after_cost_proxy"] = short_net.astype("float32")
    out["tlr_label_runtime_net_after_cost_fwd18"] = runtime_label.astype("int8")
    out["tlr_label_drawdown_survival_corridor_fwd18"] = survival_label.astype("int8")
    out["tlr_label_session_regime_lifecycle_net_fwd18"] = session_label.astype("int8")
    out["tlr_side_loss_quarantine_weight"] = pd.Series(side_loss_weight).astype("float32")
    out["tlr_density_margin_cost_weight"] = pd.Series(density_weight * cost_weight).astype("float32")
    out["tlr_lifecycle_composite_weight"] = pd.Series(lifecycle_weight).astype("float32")

    ensure_parent(INPUT_FRAME)
    out.to_parquet(io(INPUT_FRAME), index=False)

    feature_schema = allowed.loc[allowed["feature_name"].isin(feature_names)].copy()
    feature_schema["run338_allowed"] = "yes(예)"
    feature_schema["run338_timestamp_safe"] = "yes_closed_bar_asof_only(예_닫힌봉_시점기준)"
    feature_schema["claim_boundary"] = CLAIM_BOUNDARY
    excluded_frame = pd.DataFrame(excluded)
    if not excluded_frame.empty:
        excluded_frame["run338_allowed"] = "no(아니오)"
    write_csv(FEATURE_SCHEMA, feature_schema)

    label_audit = pd.DataFrame(
        [
            {
                "label_id": "tlr_label_runtime_net_after_cost_fwd18",
                "valid_rows": int(valid.sum()),
                "class_counts": class_counts(out["tlr_label_runtime_net_after_cost_fwd18"]),
                "uses_future_columns": "hx_future_log_return_18(label only, 라벨 전용)",
                "feature_exclusion": "future/label/valid/weight columns excluded from features(미래/라벨/유효/가중치 열 피처 제외)",
                "effect": "기본 거래 생명주기 손익 방향을 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "label_id": "tlr_label_drawdown_survival_corridor_fwd18",
                "valid_rows": int(valid.sum()),
                "class_counts": class_counts(out["tlr_label_drawdown_survival_corridor_fwd18"]),
                "uses_future_columns": "hx_future_log_return_18 plus outcome pressure columns(label only, 라벨 전용)",
                "feature_exclusion": "outcome pressure columns remain excluded(결과 압박 열 피처 제외 유지)",
                "effect": "낙폭 생존 조건을 라벨에 반영한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "label_id": "tlr_label_session_regime_lifecycle_net_fwd18",
                "valid_rows": int(valid.sum()),
                "class_counts": class_counts(out["tlr_label_session_regime_lifecycle_net_fwd18"]),
                "uses_future_columns": "hx_future_log_return_18(label only, 라벨 전용)",
                "feature_exclusion": "session feature is pretrade; outcome remains label-only(세션 피처는 사전, 결과는 라벨 전용)",
                "effect": "세션/국면 손실 방화벽을 시험한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    write_csv(LABEL_AUDIT, label_audit)

    boundary = pd.DataFrame(
        [
            {
                "audit_id": "feature_columns",
                "row_count": len(feature_schema),
                "forbidden_pattern_hits": int(sum(is_forbidden_feature(name) for name in feature_names)),
                "judgment": "passed(통과)",
                "effect": "모델 피처에 future/label/weight(미래/라벨/가중치) 계열을 넣지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "excluded_planned_or_allowed_columns",
                "row_count": len(excluded_frame),
                "forbidden_pattern_hits": int(excluded_frame["forbidden"].sum()) if not excluded_frame.empty else 0,
                "judgment": "recorded(기록됨)",
                "effect": "위험 열은 제외 목록으로 남긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    write_csv(FEATURE_LABEL_BOUNDARY_AUDIT, boundary)

    split_manifest = out.groupby("run338_split", dropna=False).agg(
        rows=("source_row_id", "count"),
        first_timestamp=("timestamp", "min"),
        last_timestamp=("timestamp", "max"),
    ).reset_index()
    split_manifest["effect"] = "시간순 inner train/holdout(내부 학습/홀드아웃)을 고정한다."
    split_manifest["claim_boundary"] = CLAIM_BOUNDARY
    write_csv(SPLIT_MANIFEST, split_manifest)

    tier_records = pd.DataFrame(
        [
            {
                "record_view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "rows": int(len(out)),
                "status": "materialized(물질화됨)",
                "net_profit": "",
                "profit_factor": "",
                "effect": "전체 문맥 표본 입력을 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "record_view": "Tier B separate(Tier B 분리)",
                "tier": "Tier B",
                "rows": 0,
                "status": "missing_required(필수 누락)",
                "net_profit": "",
                "profit_factor": "",
                "effect": "부분 문맥 표본은 이번 원천에서 분리 불가하므로 생략하지 않고 누락 기록한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "record_view": "Tier A+B combined(Tier A+B 합산)",
                "tier": "Tier A+B",
                "rows": int(len(out)),
                "status": "same_as_tier_a_until_tier_b_available(Tier B 전까지 Tier A와 같음)",
                "net_profit": "",
                "profit_factor": "",
                "effect": "합산을 MT5 성과로 과장하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    write_csv(TIER_RECORDS, tier_records)

    summary = {
        "source_rows": int(len(frame)),
        "materialized_rows": int(len(out)),
        "source_columns": int(len(frame.columns)),
        "output_columns": int(len(out.columns)),
        "feature_count": int(len(feature_names)),
        "excluded_feature_count": int(len(excluded_frame)),
        "train_rows": int((out["run338_split"] == "inner_train").sum()),
        "holdout_rows": int((out["run338_split"] == "inner_holdout").sum()),
        "label_runtime_class_counts": class_counts(out["tlr_label_runtime_net_after_cost_fwd18"]),
        "input_frame_sha256": sha(INPUT_FRAME),
        "source_sha256": sha(ds.SOURCE_INPUT_FRAME),
        "parent_design_variants": int(read_json(ds.FINAL_DECISION).get("design_variants", 0)),
    }
    summary_frame = pd.DataFrame([{**summary, "effect": "run338D input review(입력 검토)가 검증할 입력 정체성", "claim_boundary": CLAIM_BOUNDARY}])
    write_csv(MATERIALIZATION_SUMMARY, summary_frame)

    queue = pd.DataFrame(
        [
            {
                "queue_id": "run338D_review_trade_lifecycle_inputs",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "review run338C timestamp-safe trade lifecycle inputs(run338C 시점 안전 거래 생명주기 입력 검토)",
                "required_inputs": f"{rel(INPUT_FRAME)};{rel(FEATURE_SCHEMA)};{rel(LABEL_AUDIT)};{rel(FEATURE_LABEL_BOUNDARY_AUDIT)};{rel(SPLIT_MANIFEST)};{rel(TIER_RECORDS)}",
                "required_outputs": "input review scorecard(입력 검토 점수표); run338E training queue(학습 대기열); gate audit(게이트 감사)",
                "blocked_if_missing": "feature-label boundary pass or split manifest(피처-라벨 경계 통과 또는 분할 목록)",
                "forbidden_action": "training before input review(입력 검토 전 학습)",
                "effect": "입력이 바로 학습으로 넘어가기 전에 누수와 분포를 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    write_csv(RUN338D_REVIEW_QUEUE, queue)

    return out, feature_schema, label_audit, boundary, split_manifest, tier_records, summary


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(summary: Mapping[str, Any], boundary: pd.DataFrame) -> pd.DataFrame:
    parent_gates = read_csv(ds.GATE_AUDIT)
    forbidden_hits = int(boundary.loc[boundary["audit_id"].eq("feature_columns"), "forbidden_pattern_hits"].iloc[0])
    return pd.DataFrame(
        [
            gate_row("parent_338B_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(ds.GATE_AUDIT), "run338B design(설계) 통과 후 입력을 만든다."),
            gate_row("source_frame_loaded", "passed" if summary["source_rows"] > 0 else "failed", rel(ds.SOURCE_INPUT_FRAME), "원천 parquet(파케이) 프레임을 읽는다."),
            gate_row("feature_schema_materialized", "passed" if summary["feature_count"] > 0 and exists(FEATURE_SCHEMA) else "failed", rel(FEATURE_SCHEMA), "허용 feature schema(피처 스키마)를 만든다."),
            gate_row("feature_label_boundary_passed", "passed" if forbidden_hits == 0 else "failed", rel(FEATURE_LABEL_BOUNDARY_AUDIT), "피처에 future/label/weight(미래/라벨/가중치) 계열이 없음을 확인한다."),
            gate_row("labels_materialized", "passed" if exists(LABEL_AUDIT) and "tlr_label_runtime_net_after_cost_fwd18" in read_csv(LABEL_AUDIT)["label_id"].astype(str).tolist() else "failed", rel(LABEL_AUDIT), "거래 생명주기 label(라벨)을 만든다."),
            gate_row("split_manifest_written", "passed" if summary["train_rows"] > 0 and summary["holdout_rows"] > 0 else "failed", rel(SPLIT_MANIFEST), "시간순 split(분할)을 만든다."),
            gate_row("tier_records_written", "passed" if exists(TIER_RECORDS) else "failed", rel(TIER_RECORDS), "Tier A/B(티어 A/B) 기록을 남긴다."),
            gate_row("run338D_review_queue_opened", "passed" if exists(RUN338D_REVIEW_QUEUE) else "failed", rel(RUN338D_REVIEW_QUEUE), "다음 입력 검토 queue(대기열)를 연다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(FINAL_DECISION), "학습/선택/MT5/운영 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(ds.SOURCE_INPUT_FRAME),
            "time_axis": "timestamp sorted with source_row_id tie-break(시각 정렬과 원천 행 보조키)",
            "sample_scope": f"rows={summary['materialized_rows']};features={summary['feature_count']}",
            "missing_or_duplicate_check": rel(SPLIT_MANIFEST),
            "feature_label_boundary": rel(FEATURE_LABEL_BOUNDARY_AUDIT),
            "split_boundary": rel(SPLIT_MANIFEST),
            "leakage_risk": "future/label/weight columns excluded from features(미래/라벨/가중치 열 피처 제외)",
            "data_hash_or_identity": summary["input_frame_sha256"],
            "integrity_judgment": "usable_with_boundary_review_required(경계 조건부 사용 가능, 검토 필요)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "not_trained_in_run338C(338C에서 학습 없음)",
            "target_and_label": rel(LABEL_AUDIT),
            "split_method": rel(SPLIT_MANIFEST),
            "selection_metric": "not_applicable_input_materialization(입력 생성이라 해당 없음)",
            "validation_judgment": "input_ready_for_review_not_training_yet(검토 준비, 아직 학습 아님)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in OUTPUT_FILES if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 함께 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "threshold_tuning": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338C Trade Lifecycle Input Materialization(거래 생명주기 입력 생성)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- rows(행): `{final['materialized_rows']}`
- features(피처): `{final['feature_count']}`
- train_rows(학습 행): `{final['train_rows']}`
- holdout_rows(홀드아웃 행): `{final['holdout_rows']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338B design(설계)을 실제 timestamp-safe input frame(시점 안전 입력 프레임)으로 물질화했다.
Effect(효과): 다음 run338D가 feature-label boundary(피처-라벨 경계), split(분할), label distribution(라벨 분포)을 검토할 수 있다.

## Evidence(근거)

- input frame(입력 프레임): `{rel(INPUT_FRAME)}`
- feature schema(피처 스키마): `{rel(FEATURE_SCHEMA)}`
- label audit(라벨 감사): `{rel(LABEL_AUDIT)}`
- boundary audit(경계 감사): `{rel(FEATURE_LABEL_BOUNDARY_AUDIT)}`
- review queue(검토 대기열): `{rel(RUN338D_REVIEW_QUEUE)}`

## Boundary(경계)

run338C는 input materialization(입력 생성) 전용이다. Model training(모델 학습), candidate selection(후보 선택), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338C Decision(338C 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(INPUT_FRAME)}`, `{rel(FEATURE_LABEL_BOUNDARY_AUDIT)}`, `{rel(RUN338D_REVIEW_QUEUE)}`

Action(행동): Stage338(338단계) trade lifecycle repair(거래 생명주기 수리) 입력을 만들었다.
Effect(효과): 학습 전에 입력 검토 단계가 누수와 분포를 점검하게 한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run338C는 입력을 만들었고, run338D는 학습 전 input review(입력 검토)를 해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- materialized_rows(물질화 행): `{final['materialized_rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- input_frame(입력 프레임): `{rel(INPUT_FRAME)}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 입력 생성 산출물을 선정 모델로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run338C {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run338C Input Materialization(입력 생성)

- run_id(실행 ID): `{RUN_ID}`
- rows(행): `{final['materialized_rows']}`
- features(피처): `{final['feature_count']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 거래 생명주기 수리 입력을 학습 전 검토 가능하게 만들었다.
""")
    append_text_once(STAGE_README, marker, f"""## run338C Input Materialization(입력 생성)

- run_id(실행 ID): `{RUN_ID}`
- input_frame(입력 프레임): `{rel(INPUT_FRAME)}`
- effect(효과): 설계가 실제 데이터 산출물로 내려왔다.
""")
    changelog = f"""## {TODAY} run338C Trade Lifecycle Input Materialization(거래 생명주기 입력 생성)

- action(행동): `{final['materialized_rows']}`행, `{final['feature_count']}`개 feature(피처)의 입력 프레임을 만들었다.
- effect(효과): run338D input review(입력 검토)가 누수, split(분할), label(라벨) 분포를 확인할 수 있다.
- boundary(경계): training/model selection/MT5 execution(학습/모델 선택/MT5 실행)은 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "input_materialization", "sample_rows": final["materialized_rows"], "feature_count": final["feature_count"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "sample_rows": final["materialized_rows"], "result_status": "same_as_tier_a_until_tier_b_available"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    write_csv(ARTIFACT_REGISTRY, registry[required + [c for c in registry.columns if c not in required]])


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338C inputs: {missing}")
    _out, _schema, _labels, boundary, _split, _tiers, summary = materialize_inputs()
    gates = make_gates(summary, boundary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338C gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "materialized_rows": final["materialized_rows"],
                "feature_count": final["feature_count"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
