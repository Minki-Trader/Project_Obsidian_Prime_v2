from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

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


STAGE278_ID = "278_onnx_candidate_campaign__fresh_thesis_mt5_probe"
RUN_ID = "run278A_design_fresh_thesis_mt5_probe_packet_v1"
SOURCE_RUN_ID = "stage278_fresh_thesis_mt5_probe_open_v1"
SOURCE_TRANSITION_RUN_ID = "run277F_close_stage277_open_stage278_fresh_thesis_mt5_probe_v1"
STATUS = "completed_fresh_thesis_mt5_probe_packet_design_no_candidate_selection"
JUDGMENT = "fresh_thesis_mt5_probe_packet_ready_no_candidate_selection"
NEXT_ACTION = "run278B_materialize_fresh_thesis_mt5_probe_payloads"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE278_ID
RUN_DIR = STAGE / "02_runs" / "run278A"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_QUEUE = STAGE / "01_inputs" / "stage277_probe_queue.csv"
SOURCE_SCREEN = STAGE / "01_inputs" / "stage277_screening_decision_matrix.csv"
SOURCE_FAILURE = STAGE / "01_inputs" / "stage277_failure_memory.csv"
SOURCE_SUPPORT = STAGE / "01_inputs" / "stage277_support_control.csv"
SOURCE_HANDOFF = STAGE / "01_inputs" / "run277D_handoff_index.csv"
SOURCE_BRIEF = STAGE / "00_spec" / "stage_brief.md"
SOURCE_INPUT_REFS = STAGE / "01_inputs" / "input_refs.md"
SOURCE_CLOSEOUT = ROOT / "stages" / "277_onnx_candidate_campaign__fresh_thesis_rebuild" / "03_reviews" / "stage277_closeout_stage278_handoff.md"
SOURCE_RUN277F_MANIFEST = ROOT / "stages" / "277_onnx_candidate_campaign__fresh_thesis_rebuild" / "02_runs" / "run277F" / "run_manifest.json"
SOURCE_RUN277F_LINEAGE = ROOT / "stages" / "277_onnx_candidate_campaign__fresh_thesis_rebuild" / "02_runs" / "run277F" / "artifact_lineage_receipt.json"

BRANCH_PLAN = RUN_DIR / "probe_branch_plan.csv"
BRANCH_METRICS = RUN_DIR / "branch_supply_metrics.csv"
MT5_QUEUE = RUN_DIR / "mt5_probe_design_queue.csv"
PAYLOAD_CONTRACT = RUN_DIR / "payload_contract_plan.csv"
TESTER_PLAN = RUN_DIR / "tester_identity_plan.csv"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_FORENSICS_PLAN = RUN_DIR / "backtest_forensics_plan.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run278A_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage278/design_fresh_thesis_mt5_probe_packet.py")

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
BRANCH_COLUMNS = (
    "branch_id",
    "package_id",
    "variant_role",
    "fresh_thesis",
    "decision_rule",
    "thresholds_json",
    "route_policy",
    "signal_policy",
    "risk_policy",
    "upside_condition",
    "failure_mode",
    "discard_condition",
    "invalid_condition",
    "evidence_plan",
    "materialization_status",
    "selected_candidate",
    "onnx_readiness",
    "claim_boundary",
)
METRIC_COLUMNS = (
    "branch_id",
    "package_id",
    "record_view",
    "split",
    "rows",
    "decision_count",
    "decision_rate",
    "mean_candidate_decision_score",
    "mean_model_risk_pct",
    "mean_atr_stop_multiplier",
    "mean_atr_take_profit_multiplier",
    "mean_max_hold_bars",
    "mean_reentry_cooldown_bars",
    "tier_b_missing_required_feature_count",
    "fallback_count_design_proxy",
    "claim_boundary",
)
MT5_QUEUE_COLUMNS = (
    "queue_id",
    "queue_priority",
    "branch_id",
    "package_id",
    "source_score_tables",
    "source_handoff_json",
    "route_policy",
    "signal_payload_plan",
    "tester_identity_plan",
    "required_records",
    "success_condition",
    "discard_condition",
    "selected_candidate",
    "onnx_readiness",
    "next_action",
)
PAYLOAD_COLUMNS = (
    "branch_id",
    "package_id",
    "payload_kind",
    "required_columns",
    "feature_order_hash",
    "decision_rule_hash",
    "adapter_schema_hash",
    "expected_output_path",
    "claim_boundary",
)
TESTER_COLUMNS = (
    "branch_id",
    "package_id",
    "tester_identity",
    "symbol",
    "timeframe",
    "route_policy",
    "validation_window",
    "oos_window",
    "cost_assumption_status",
    "required_output",
    "claim_boundary",
)
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


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def repo_path(text: str) -> Path:
    return ROOT / text


def digest_mask(mask: pd.Series) -> str:
    return hashlib.sha256(mask.astype("int8").to_numpy().tobytes()).hexdigest()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except Exception:
        return default
    return number if np.isfinite(number) else default


def rounded(value: Any, digits: int = 8) -> float:
    return round(as_float(value), digits)


def source_paths(queue_rows: Sequence[Mapping[str, str]]) -> list[Path]:
    paths = [
        SOURCE_QUEUE,
        SOURCE_SCREEN,
        SOURCE_FAILURE,
        SOURCE_SUPPORT,
        SOURCE_HANDOFF,
        SOURCE_BRIEF,
        SOURCE_INPUT_REFS,
        SOURCE_CLOSEOUT,
        SOURCE_RUN277F_MANIFEST,
        SOURCE_RUN277F_LINEAGE,
    ]
    for row in queue_rows:
        for score_path in str(row["score_table_paths"]).split(";"):
            if score_path:
                paths.append(repo_path(score_path))
        if row.get("handoff_json_path"):
            paths.append(repo_path(row["handoff_json_path"]))
    return paths


def load_package_scores(queue_row: Mapping[str, str]) -> pd.DataFrame:
    frames = []
    for score_path in str(queue_row["score_table_paths"]).split(";"):
        if not score_path:
            continue
        frames.append(pd.read_parquet(io_path(repo_path(score_path))))
    if not frames:
        raise ValueError(f"No score tables for {queue_row.get('package_id')}")
    frame = pd.concat(frames, ignore_index=True)
    required = {
        "timestamp",
        "split",
        "tier_scope",
        "package_id",
        "feature_order_hash",
        "decision_rule_hash",
        "adapter_schema_hash",
        "candidate_decision_score",
        "materialized_decision_flag",
        "entry_signal",
        "model_risk_pct",
        "atr_stop_multiplier",
        "atr_take_profit_multiplier",
        "max_hold_bars",
        "reentry_cooldown_bars",
        "missing_required_feature_count",
    }
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"Missing score columns for {queue_row.get('package_id')}: {missing}")
    frame = frame.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["entry_active"] = pd.to_numeric(frame["materialized_decision_flag"], errors="coerce").fillna(0).astype(int).gt(0)
    return frame


def train_thresholds(frame: pd.DataFrame, columns: Sequence[str]) -> dict[str, float]:
    train = frame[(frame["tier_scope"].astype(str).eq("Tier A")) & (frame["split"].astype(str).eq("train"))]
    if train.empty:
        raise ValueError("Tier A train rows(Tier A 학습 행)가 필요하다.")
    thresholds: dict[str, float] = {}
    for column in columns:
        if column in train.columns:
            series = pd.to_numeric(train[column], errors="coerce")
            thresholds[f"{column}_q50"] = float(series.quantile(0.50))
            thresholds[f"{column}_q60"] = float(series.quantile(0.60))
            thresholds[f"{column}_q65"] = float(series.quantile(0.65))
            thresholds[f"{column}_q70"] = float(series.quantile(0.70))
    series = pd.to_numeric(train["candidate_decision_score"], errors="coerce")
    thresholds["candidate_decision_score_q60"] = float(series.quantile(0.60))
    thresholds["candidate_decision_score_q70"] = float(series.quantile(0.70))
    risk = pd.to_numeric(train["model_risk_pct"], errors="coerce")
    thresholds["model_risk_pct_q65"] = float(risk.quantile(0.65))
    thresholds["model_risk_pct_q70"] = float(risk.quantile(0.70))
    return thresholds


def branch_templates(package_id: str, thresholds: Mapping[str, float]) -> list[dict[str, Any]]:
    if package_id.startswith("cp277C"):
        return [
            {
                "suffix": "q01_base_signal",
                "role": "base_signal_reference(기준 신호 참조)",
                "fresh_thesis": "directional asymmetry reversal(방향 비대칭 반전)이 MT5 탐침에서 실제 거래 공급을 만든다.",
                "rule": "materialized_decision_flag == 1",
                "thresholds": {},
                "mask": lambda f: f["entry_active"],
                "upside": "base signal(기준 신호)이 validation/OOS(검증/표본외)에서 충분한 trade supply(거래 공급)를 유지한다.",
                "failure": "score screen(점수 선별)은 좋지만 MT5 payload(페이로드)로는 공급이 과하거나 약하다.",
                "discard": "actual routed total(실제 라우팅 전체) OOS(표본외) decision_rate(판단 비율)가 0.10 미만이거나 0.45 초과면 폐기한다.",
            },
            {
                "suffix": "q02_side_reversal_strict",
                "role": "side_reversal_strict_pressure(방향 반전 엄격 압박)",
                "fresh_thesis": "side reversal(방향 반전)과 divergence sign(괴리 부호)이 같이 강할 때 손실 방향을 피한다.",
                "rule": "active and side_reversal_score>=q70 and divergence_sign_score>=q60",
                "thresholds": {
                    "side_reversal_score_min": thresholds["side_reversal_score_q70"],
                    "divergence_sign_score_min": thresholds["divergence_sign_score_q60"],
                },
                "mask": lambda f: f["entry_active"]
                & pd.to_numeric(f["side_reversal_score"], errors="coerce").ge(thresholds["side_reversal_score_q70"])
                & pd.to_numeric(f["divergence_sign_score"], errors="coerce").ge(thresholds["divergence_sign_score_q60"]),
                "upside": "directional filter(방향 필터)가 공급을 죽이지 않고 OOS(표본외) 약한 구간을 줄인다.",
                "failure": "엄격 조건이 공급을 없애거나 Tier B(Tier B)에서만 좋아 보인다.",
                "discard": "validation/OOS(검증/표본외) decision_count(판단 수)가 각각 75 미만이면 폐기한다.",
            },
            {
                "suffix": "q03_session_pressure_cap",
                "role": "session_pressure_cap(세션 압력 상한)",
                "fresh_thesis": "session pressure(세션 압력)를 상한 처리하면 실패 시간대 집중을 줄인다.",
                "rule": "active and session_pressure_score<=q70 and candidate_decision_score>=q60",
                "thresholds": {
                    "session_pressure_score_max": thresholds["session_pressure_score_q70"],
                    "candidate_decision_score_min": thresholds["candidate_decision_score_q60"],
                },
                "mask": lambda f: f["entry_active"]
                & pd.to_numeric(f["session_pressure_score"], errors="coerce").le(thresholds["session_pressure_score_q70"])
                & pd.to_numeric(f["candidate_decision_score"], errors="coerce").ge(thresholds["candidate_decision_score_q60"]),
                "upside": "weak session(약한 세션)을 단순 제거가 아니라 score-conditioned cap(점수 조건 상한)으로 줄인다.",
                "failure": "방어형 필터만 남고 fresh edge(새 거래 우위)가 없다.",
                "discard": "OOS(표본외) decision_rate(판단 비율)가 base 대비 절반 미만이면 폐기한다.",
            },
            {
                "suffix": "q04_side_risk_compressed",
                "role": "side_risk_compressed(방향 위험 압축)",
                "fresh_thesis": "side risk(방향 위험)와 model risk(모델 위험)를 같이 압축하면 손실 꼬리를 줄인다.",
                "rule": "active and side_risk_score<=q65 and model_risk_pct<=q70",
                "thresholds": {
                    "side_risk_score_max": thresholds["side_risk_score_q65"],
                    "model_risk_pct_max": thresholds["model_risk_pct_q70"],
                },
                "mask": lambda f: f["entry_active"]
                & pd.to_numeric(f["side_risk_score"], errors="coerce").le(thresholds["side_risk_score_q65"])
                & pd.to_numeric(f["model_risk_pct"], errors="coerce").le(thresholds["model_risk_pct_q70"]),
                "upside": "risk compression(위험 압축)이 거래 수를 지나치게 줄이지 않고 curve(곡선)를 안정화한다.",
                "failure": "risk cap(위험 상한)이 기대값을 같이 제거한다.",
                "discard": "Tier A/Tier B(Tier A/Tier B) decision_rate(판단 비율) 괴리가 0.12 초과면 폐기한다.",
            },
        ]
    return [
        {
            "suffix": "q01_base_signal",
            "role": "base_signal_reference(기준 신호 참조)",
            "fresh_thesis": "macro squeeze contrast(거시 압축 대비)가 MT5 탐침에서 실제 거래 공급을 만든다.",
            "rule": "materialized_decision_flag == 1",
            "thresholds": {},
            "mask": lambda f: f["entry_active"],
            "upside": "base macro contrast(기준 거시 대비)가 validation/OOS(검증/표본외)에서 충분한 공급을 유지한다.",
            "failure": "macro contrast(거시 대비)가 늦은 구간 손실을 그대로 반복한다.",
            "discard": "actual routed total(실제 라우팅 전체) OOS(표본외) decision_rate(판단 비율)가 0.10 미만이거나 0.45 초과면 폐기한다.",
        },
        {
            "suffix": "q02_contrast_reward_focus",
            "role": "contrast_reward_focus(대비 보상 집중)",
            "fresh_thesis": "contrast reward(대비 보상)가 강하고 cooldown(냉각)이 충분할 때 squeeze(압축) 실패를 피한다.",
            "rule": "active and contrast_reward_score>=q65 and cooldown_score>=q50",
            "thresholds": {
                "contrast_reward_score_min": thresholds["contrast_reward_score_q65"],
                "cooldown_score_min": thresholds["cooldown_score_q50"],
            },
            "mask": lambda f: f["entry_active"]
            & pd.to_numeric(f["contrast_reward_score"], errors="coerce").ge(thresholds["contrast_reward_score_q65"])
            & pd.to_numeric(f["cooldown_score"], errors="coerce").ge(thresholds["cooldown_score_q50"]),
            "upside": "reward focus(보상 집중)가 late loss(후반 손실) 없이 공급을 유지한다.",
            "failure": "contrast(대비)가 단순 고점수 필터에 그친다.",
            "discard": "validation/OOS(검증/표본외) decision_count(판단 수)가 각각 75 미만이면 폐기한다.",
        },
        {
            "suffix": "q03_late_loss_compression_guard",
            "role": "late_loss_compression_guard(후반 손실 압축 보호)",
            "fresh_thesis": "late loss compression(후반 손실 압축)이 충분할 때 후반 OOS(표본외) 손실을 줄인다.",
            "rule": "active and late_loss_compression_score>=q70 and cooldown_score>=q60",
            "thresholds": {
                "late_loss_compression_score_min": thresholds["late_loss_compression_score_q70"],
                "cooldown_score_min": thresholds["cooldown_score_q60"],
            },
            "mask": lambda f: f["entry_active"]
            & pd.to_numeric(f["late_loss_compression_score"], errors="coerce").ge(thresholds["late_loss_compression_score_q70"])
            & pd.to_numeric(f["cooldown_score"], errors="coerce").ge(thresholds["cooldown_score_q60"]),
            "upside": "late OOS(후반 표본외) 방어가 단순 거래 축소가 아니라 보상 비대칭을 만든다.",
            "failure": "후반 구간만 줄이고 전체 기대값을 잃는다.",
            "discard": "OOS(표본외) decision_rate(판단 비율)가 base 대비 절반 미만이면 폐기한다.",
        },
        {
            "suffix": "q04_macro_cooldown_risk_cap",
            "role": "macro_cooldown_risk_cap(거시 냉각 위험 상한)",
            "fresh_thesis": "macro state(거시 상태), cooldown(냉각), model risk(모델 위험)를 함께 제한하면 깊은 손실을 줄인다.",
            "rule": "active and macro_squeeze_state_score>=q60 and cooldown_score>=q70 and model_risk_pct<=q70",
            "thresholds": {
                "macro_squeeze_state_score_min": thresholds["macro_squeeze_state_score_q60"],
                "cooldown_score_min": thresholds["cooldown_score_q70"],
                "model_risk_pct_max": thresholds["model_risk_pct_q70"],
            },
            "mask": lambda f: f["entry_active"]
            & pd.to_numeric(f["macro_squeeze_state_score"], errors="coerce").ge(thresholds["macro_squeeze_state_score_q60"])
            & pd.to_numeric(f["cooldown_score"], errors="coerce").ge(thresholds["cooldown_score_q70"])
            & pd.to_numeric(f["model_risk_pct"], errors="coerce").le(thresholds["model_risk_pct_q70"]),
            "upside": "risk cap(위험 상한)이 drawdown(손실폭) 꼬리를 줄이며 공급을 보존한다.",
            "failure": "cooldown(냉각)이 과해져 active supply(활성 공급)가 사라진다.",
            "discard": "Tier A/Tier B(Tier A/Tier B) decision_rate(판단 비율) 괴리가 0.12 초과면 폐기한다.",
        },
    ]


def summarize_metrics(branch_id: str, package_id: str, frame: pd.DataFrame, mask: pd.Series) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record_view, tier_frame in [
        ("Tier A used(Tier A 사용)", frame[frame["tier_scope"].astype(str).eq("Tier A")]),
        ("Tier B fallback stress(Tier B 대체 스트레스)", frame[frame["tier_scope"].astype(str).eq("Tier B")]),
        ("actual routed total design proxy(실제 라우팅 전체 설계 대리)", frame[frame["tier_scope"].astype(str).eq("Tier A")]),
    ]:
        view_mask = mask.loc[tier_frame.index]
        fallback_count = 0 if record_view.startswith("actual routed") else ""
        for split in ["train", "validation", "oos"]:
            part = tier_frame[tier_frame["split"].astype(str).eq(split)]
            part_mask = view_mask.loc[part.index]
            selected = part.loc[part_mask]
            rows.append(
                {
                    "branch_id": branch_id,
                    "package_id": package_id,
                    "record_view": record_view,
                    "split": split,
                    "rows": int(len(part)),
                    "decision_count": int(part_mask.sum()),
                    "decision_rate": rounded(float(part_mask.mean()) if len(part_mask) else 0.0),
                    "mean_candidate_decision_score": rounded(selected["candidate_decision_score"].mean() if len(selected) else 0.0),
                    "mean_model_risk_pct": rounded(selected["model_risk_pct"].mean() if len(selected) else 0.0),
                    "mean_atr_stop_multiplier": rounded(selected["atr_stop_multiplier"].mean() if len(selected) else 0.0),
                    "mean_atr_take_profit_multiplier": rounded(selected["atr_take_profit_multiplier"].mean() if len(selected) else 0.0),
                    "mean_max_hold_bars": rounded(selected["max_hold_bars"].mean() if len(selected) else 0.0),
                    "mean_reentry_cooldown_bars": rounded(selected["reentry_cooldown_bars"].mean() if len(selected) else 0.0),
                    "tier_b_missing_required_feature_count": int(part["missing_required_feature_count"].max()) if len(part) else 0,
                    "fallback_count_design_proxy": fallback_count,
                    "claim_boundary": BOUNDARY,
                }
            )
    return rows


def split_metric(rows: Sequence[Mapping[str, Any]], branch_id: str, record_view_prefix: str, split: str, field: str) -> float:
    for row in rows:
        if row["branch_id"] == branch_id and str(row["record_view"]).startswith(record_view_prefix) and row["split"] == split:
            return as_float(row[field])
    return 0.0


def materialization_status(branch_id: str, metrics: Sequence[Mapping[str, Any]]) -> str:
    val_count = split_metric(metrics, branch_id, "actual routed", "validation", "decision_count")
    oos_count = split_metric(metrics, branch_id, "actual routed", "oos", "decision_count")
    val_rate = split_metric(metrics, branch_id, "actual routed", "validation", "decision_rate")
    oos_rate = split_metric(metrics, branch_id, "actual routed", "oos", "decision_rate")
    if val_count >= 75 and oos_count >= 75 and 0.08 <= val_rate <= 0.45 and 0.08 <= oos_rate <= 0.45:
        return "queue_for_run278B_payload_materialization(run278B 페이로드 물질화 대기)"
    return "hold_insufficient_or_excessive_supply(공급 부족 또는 과다로 보류)"


def build_design(queue_rows: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, pd.DataFrame]]:
    branch_rows: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []
    threshold_payload: dict[str, Any] = {"run_id": RUN_ID, "threshold_source": "Tier A train(Tier A 학습)", "packages": {}}
    frames: dict[str, pd.DataFrame] = {}
    for row in queue_rows:
        package_id = row["package_id"]
        frame = load_package_scores(row)
        frames[package_id] = frame
        score_columns = [c for c in frame.columns if c.endswith("_score") and c != "candidate_decision_score"]
        thresholds = train_thresholds(frame, score_columns)
        threshold_payload["packages"][package_id] = thresholds
        masks: dict[str, str] = {}
        for template in branch_templates(package_id, thresholds):
            branch_id = f"run278A_{package_id}_{template['suffix']}"
            mask = template["mask"](frame).fillna(False)
            masks[branch_id] = digest_mask(mask)
            branch_metrics = summarize_metrics(branch_id, package_id, frame, mask)
            metric_rows.extend(branch_metrics)
            status = materialization_status(branch_id, branch_metrics)
            branch_rows.append(
                {
                    "branch_id": branch_id,
                    "package_id": package_id,
                    "variant_role": template["role"],
                    "fresh_thesis": template["fresh_thesis"],
                    "decision_rule": template["rule"],
                    "thresholds_json": json.dumps(json_ready(template["thresholds"]), ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                    "route_policy": "Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체); fallback_count expected 0 if Tier A coverage is complete(티어 A 전체 커버 시 대체 수 0 예상)",
                    "signal_policy": "active=1, flat=0(활성 1, 관망 0); direction neutral until MT5 payload mapping(방향은 MT5 페이로드 매핑 전까지 중립)",
                    "risk_policy": "carry score-table risk fields(점수표 위험 필드 이월): model_risk_pct, ATR stop/take-profit, max hold, cooldown",
                    "upside_condition": template["upside"],
                    "failure_mode": template["failure"],
                    "discard_condition": template["discard"],
                    "invalid_condition": "missing score table(점수표 누락), missing handoff JSON(인계 JSON 누락), or claiming selected candidate(선택 후보 주장)",
                    "evidence_plan": "payload contract(페이로드 계약); tester identity(테스터 정체성); MT5 output(MT5 출력); balance/equity curve(잔액/평가금 곡선); trade quality(거래 품질)",
                    "materialization_status": status,
                    "selected_candidate": "none",
                    "onnx_readiness": "not_claimed",
                    "claim_boundary": BOUNDARY,
                }
            )
        threshold_payload["packages"][package_id]["decision_mask_hashes"] = masks
    return branch_rows, metric_rows, threshold_payload, frames


def build_mt5_queue(branch_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    source_by_package = {row["package_id"]: row for row in queue_rows}
    selected = [row for row in branch_rows if str(row["materialization_status"]).startswith("queue_for_run278B")]
    selected = sorted(selected, key=lambda row: (row["package_id"], row["branch_id"]))
    rows: list[dict[str, Any]] = []
    for index, branch in enumerate(selected, start=1):
        source = source_by_package[str(branch["package_id"])]
        rows.append(
            {
                "queue_id": f"run278B_{index:02d}_{branch['branch_id']}",
                "queue_priority": index,
                "branch_id": branch["branch_id"],
                "package_id": branch["package_id"],
                "source_score_tables": source["score_table_paths"],
                "source_handoff_json": source["handoff_json_path"],
                "route_policy": branch["route_policy"],
                "signal_payload_plan": "create validation/OOS signal CSV and payload parquet(검증/표본외 신호 CSV와 페이로드 파케이 생성)",
                "tester_identity_plan": rel(TESTER_PLAN),
                "required_records": "Tier A used(Tier A 사용);Tier B fallback stress(Tier B 대체 스트레스);actual routed total(실제 라우팅 전체);MT5 tester output(MT5 테스터 출력)",
                "success_condition": "MT5 runtime probe(MT5 런타임 탐침)가 trade count/PF/DD/recovery/expectancy(거래 수/수익 팩터/손실폭/회복/기대값)를 함께 납득시킬 때 survivor watch(생존 관찰)로만 올린다.",
                "discard_condition": branch["discard_condition"],
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "next_action": NEXT_ACTION,
            }
        )
    return rows


def first_value(frame: pd.DataFrame, column: str) -> str:
    return str(frame[column].dropna().iloc[0]) if column in frame.columns and not frame[column].dropna().empty else "unknown"


def split_window(frames: Mapping[str, pd.DataFrame], split: str) -> str:
    timestamps = []
    for frame in frames.values():
        part = frame[frame["split"].astype(str).eq(split)]
        if not part.empty:
            timestamps.extend([part["timestamp"].min(), part["timestamp"].max()])
    if not timestamps:
        return "missing_required(필수 누락)"
    return f"{min(timestamps).date()}..{max(timestamps).date()}"


def build_payload_contract(branch_rows: Sequence[Mapping[str, Any]], frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in branch_rows:
        frame = frames[str(branch["package_id"])]
        rows.append(
            {
                "branch_id": branch["branch_id"],
                "package_id": branch["package_id"],
                "payload_kind": "MT5 signal handoff(MT5 신호 인계)",
                "required_columns": "timestamp,symbol,split,tier_scope,route_policy,signal_active,model_risk_pct,atr_stop_multiplier,atr_take_profit_multiplier,max_hold_bars,reentry_cooldown_bars",
                "feature_order_hash": first_value(frame, "feature_order_hash"),
                "decision_rule_hash": first_value(frame, "decision_rule_hash"),
                "adapter_schema_hash": first_value(frame, "adapter_schema_hash"),
                "expected_output_path": f"stages/{STAGE278_ID}/02_runs/run278B/payloads/{branch['branch_id']}_payload.parquet",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_tester_plan(mt5_rows: Sequence[Mapping[str, Any]], frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    validation_window = split_window(frames, "validation")
    oos_window = split_window(frames, "oos")
    rows: list[dict[str, Any]] = []
    for row in mt5_rows:
        rows.append(
            {
                "branch_id": row["branch_id"],
                "package_id": row["package_id"],
                "tester_identity": "to_be_materialized_in_run278B(run278B에서 물질화 예정)",
                "symbol": "FPMarkets US100(FPMarkets US100)",
                "timeframe": "M5(5분봉)",
                "route_policy": row["route_policy"],
                "validation_window": validation_window,
                "oos_window": oos_window,
                "cost_assumption_status": "must_capture_in_MT5_report(MT5 보고서에서 반드시 캡처)",
                "required_output": "tester report(테스터 보고서);trade list(거래 목록);balance/equity curve(잔액/평가금 곡선);runtime handoff file(런타임 인계 파일)",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def write_receipts(
    queue_rows: Sequence[Mapping[str, str]],
    branch_rows: Sequence[Mapping[str, Any]],
    metrics: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    payload_rows: Sequence[Mapping[str, Any]],
    tester_rows: Sequence[Mapping[str, Any]],
    threshold_payload: Mapping[str, Any],
    frames: Mapping[str, pd.DataFrame],
) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "Fresh thesis score surfaces(새 논제 점수 표면)가 MT5 payload(페이로드)로 변환돼도 구조적 공급과 위험 필드를 유지할 수 있다.",
            "comparison": "base branch(기준 분기) versus strict/focused/risk-capped branches(엄격/집중/위험상한 분기)",
            "controls": "same score tables(같은 점수표), same handoff hashes(같은 인계 해시), same route policy(같은 경로 정책)",
            "changed_variables": "branch decision rule(분기 판단 규칙) and threshold(임계값)",
            "branch_rows": len(branch_rows),
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
            "source_inputs": [rel(path) for path in source_paths(queue_rows)],
            "source_hashes": output_hashes(source_paths(queue_rows)),
            "split_windows": {
                "train": split_window(frames, "train"),
                "validation": split_window(frames, "validation"),
                "oos": split_window(frames, "oos"),
            },
            "tier_policy": "Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체); Tier B missing features(Tier B 누락 피처)는 support boundary(보조 경계)로 기록",
            "label_boundary": "score tables(점수표) only; no future/label profit columns(미래/라벨 수익 열 없음)",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "research_path": rel(PRODUCER_PATH),
            "runtime_path": "planned_run278B_payload_and_MT5_signal_files(run278B 페이로드와 MT5 신호 파일 예정)",
            "shared_contract": "feature_order_hash(피처 순서 해시), decision_rule_hash(판단 규칙 해시), adapter_schema_hash(어댑터 스키마 해시), risk fields(위험 필드)",
            "known_differences": "Python score table(파이썬 점수표)는 runtime authority(런타임 권위)가 아니며 MT5 tester output(MT5 테스터 출력)이 아직 없다.",
            "parity_check": "planned_payload_identity_check(페이로드 정체성 점검 예정)",
            "parity_identity": {"payload_contract_rows": len(payload_rows), "tester_plan_rows": len(tester_rows), "thresholds": threshold_payload},
            "runtime_claim_boundary": "runtime_probe_preparation_only(런타임 탐침 준비만 해당)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        BACKTEST_FORENSICS_PLAN,
        {
            "tester_identity": "to_capture_in_run278B_or_run278C(run278B 또는 run278C에서 캡처)",
            "ea_identity": "no_EA_entrypoint_change_in_run278A(run278A에서 EA 진입점 변경 없음)",
            "report_identity": "missing_until_MT5_execution(MT5 실행 전까지 누락)",
            "trade_evidence": "missing_until_MT5_execution(MT5 실행 전까지 누락)",
            "cost_assumptions": "must_capture_spread_commission_slippage_swap(스프레드/커미션/슬리피지/스왑 캡처 필요)",
            "forensic_checks": "planned_report_path_and_trade_list_check(보고서 경로와 거래 목록 점검 예정)",
            "backtest_judgment": "not_applicable_design_only(설계 전용으로 해당 없음)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run278A fresh thesis MT5 probe packet design(278A 새 논제 MT5 탐침 묶음 설계)",
                "evidence_available": "branch plan(분기 계획), supply metrics(공급 지표), payload contract(페이로드 계약), tester plan(테스터 계획), runtime parity receipt(런타임 동등성 영수증)",
                "evidence_missing": "MT5 runtime output(MT5 런타임 출력), tester report(테스터 보고서), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "design_ready_no_candidate_selection(설계 준비, 후보 선택 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": f"MT5 probe design queue(MT5 탐침 설계 대기열) {len(mt5_rows)}개가 준비됐지만 selected candidate(선택 후보)는 없다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "runtime_evidence_gate(런타임 근거 게이트)",
                "status": "passed_as_design_only_runtime_output_missing(설계 전용, 런타임 출력 없음으로 통과)",
                "evidence_path": rel(RUNTIME_PARITY_RECEIPT),
                "effect": "Python score table(파이썬 점수표)을 runtime authority(런타임 권위)로 바꾸지 않는다.",
            },
            {
                "gate_name": "backtest_forensics_plan_gate(백테스트 포렌식 계획 게이트)",
                "status": "passed_plan_created(계획 생성으로 통과)",
                "evidence_path": rel(BACKTEST_FORENSICS_PLAN),
                "effect": "tester identity(테스터 정체성)와 cost assumptions(비용 가정)을 다음 실행에서 캡처하도록 고정한다.",
            },
            {
                "gate_name": "paired_tier_gate(티어 쌍 게이트)",
                "status": "passed_tier_a_tier_b_routed_design_rows(티어 A/B/라우팅 설계 행으로 통과)",
                "evidence_path": rel(BRANCH_METRICS),
                "effect": "Tier A used(Tier A 사용), Tier B fallback stress(Tier B 대체 스트레스), actual routed total(실제 라우팅 전체)을 분리한다.",
            },
            {
                "gate_name": "payload_contract_gate(페이로드 계약 게이트)",
                "status": "passed_payload_contract_ready(페이로드 계약 준비로 통과)",
                "evidence_path": rel(PAYLOAD_CONTRACT),
                "effect": "run278B(278B 실행)가 신호 파일과 payload parquet(페이로드 파케이)를 만들 수 있다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/온엑스 없음/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            },
        ],
    )


def write_report(branch_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> None:
    queued = "\n".join(
        f"- `{row['branch_id']}` package(패키지) `{row['package_id']}` priority(우선순위) `{row['queue_priority']}`"
        for row in mt5_rows
    ) or "- none(없음)"
    held = "\n".join(
        f"- `{row['branch_id']}`: `{row['materialization_status']}`"
        for row in branch_rows
        if not str(row["materialization_status"]).startswith("queue_for_run278B")
    ) or "- none(없음)"
    write_md(
        RUN_REPORT,
        f"""# run278A Report(278A 보고서): Fresh Thesis MT5 Probe Packet Design(새 논제 MT5 탐침 묶음 설계)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE278_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_rows(분기 행): `{len(branch_rows)}`
- mt5_probe_design_queue_rows(MT5 탐침 설계 대기열 행): `{len(mt5_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## MT5 Probe Queue(MT5 탐침 대기열)

{queued}

## Held Branches(보류 분기)

{held}

## Meaning(의미)

run278A(278A 실행)는 `cp277C/cp277D` score surface(점수 표면)를 MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드)로 만들기 위한 branch plan(분기 계획)을 고정했다.
Effect(효과): 다음 run278B(278B 실행)는 payload parquet(페이로드 파케이), signal CSV(신호 CSV), handoff identity(인계 정체성)를 만들 수 있지만, 아직 selected candidate(선택 후보)나 ONNX readiness(온엑스 준비)는 없다.

## Evidence Paths(근거 경로)

- branch_plan(분기 계획): `{rel(BRANCH_PLAN)}`
- branch_metrics(분기 지표): `{rel(BRANCH_METRICS)}`
- mt5_queue(MT5 대기열): `{rel(MT5_QUEUE)}`
- payload_contract(페이로드 계약): `{rel(PAYLOAD_CONTRACT)}`
- tester_plan(테스터 계획): `{rel(TESTER_PLAN)}`
- runtime_parity_receipt(런타임 동등성 영수증): `{rel(RUNTIME_PARITY_RECEIPT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def manifest_payload(created_at: str, outputs: Sequence[Path], source_input_paths: Sequence[Path], branch_count: int, queue_count: int) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "stage_id": STAGE278_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_transition_run_id": SOURCE_TRANSITION_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in source_input_paths],
        "source_hashes": output_hashes(source_input_paths),
        "output_artifacts": [rel(path) for path in outputs],
        "output_hashes": output_hashes(outputs),
        "branch_rows": branch_count,
        "mt5_probe_design_queue_rows": queue_count,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_design_only",
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "runtime_claim_boundary": "runtime_probe_design_only(런타임 탐침 설계만 해당)",
        "claim_boundary": BOUNDARY,
    }


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


def update_registers(created_at: str, branch_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]], outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE278_ID,
                "lane": "runtime_probe_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"branch_rows={len(branch_rows)};mt5_queue_rows={len(mt5_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_used_design",
            "stage_id": STAGE278_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_used_design",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A used design(Tier A 사용 설계)",
            "tier_scope": "Tier A used",
            "kpi_scope": "runtime_probe_design_no_trading_kpi",
            "scoreboard_lane": "runtime_probe_preparation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(BRANCH_METRICS),
            "primary_kpi": f"branch_rows={len(branch_rows)};mt5_queue_rows={len(mt5_rows)}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Tier A primary route design(Tier A 우선 경로 설계).",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_fallback_design",
            "stage_id": STAGE278_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_fallback_design",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier B fallback stress design(Tier B 대체 스트레스 설계)",
            "tier_scope": "Tier B fallback stress",
            "kpi_scope": "partial_context_runtime_probe_design",
            "scoreboard_lane": "runtime_probe_preparation",
            "status": STATUS,
            "judgment": "partial_context_design_completed_no_runtime_authority(부분 문맥 설계 완료, 런타임 권위 없음)",
            "path": rel(BRANCH_METRICS),
            "primary_kpi": "Tier B rows measured as stress support(Tier B 행은 스트레스 보조로 측정)",
            "guardrail_kpi": "no_fallback_authority_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Tier B missing features(Tier B 누락 피처)는 support boundary(보조 경계)다.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__actual_routed_total_design",
            "stage_id": STAGE278_ID,
            "run_id": RUN_ID,
            "subrun_id": "actual_routed_total_design",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "actual routed total design proxy(실제 라우팅 전체 설계 대리)",
            "tier_scope": "actual routed total",
            "kpi_scope": "runtime_probe_design_no_pnl_claim",
            "scoreboard_lane": "runtime_probe_preparation",
            "status": STATUS,
            "judgment": "routed_design_ready_no_runtime_output(라우팅 설계 준비, 런타임 출력 없음)",
            "path": rel(MT5_QUEUE),
            "primary_kpi": f"mt5_probe_design_queue_rows={len(mt5_rows)}",
            "guardrail_kpi": "performance_claim=none;runtime_authority=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Actual routed total(실제 라우팅 전체)은 설계 대리이며 tester PnL(테스터 손익)이 아니다.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__runtime_probe_design",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_mt5_probe_packet_design",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "runtime_probe_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_runtime_result_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"branch_rows={len(branch_rows)};mt5_queue_rows={len(mt5_rows)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "run278A_mt5_probe_design_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE278_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run278A fresh thesis MT5 probe design artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(branch_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = replace_line_prefix(
        selected,
        "Effect(효과): run278A(",
        "Effect(효과): run278B(278B 실행)에서 payload(페이로드)를 물질화하고 tester identity(테스터 정체성)를 캡처하기 전까지 runtime result(런타임 결과)를 주장하지 않는다.",
    )
    selected = append_once(selected, "run278A_report", f"- run278A_report(278A 보고서): `{rel(RUN_REPORT)}`")
    selected = append_once(selected, "run278A_mt5_queue", f"- run278A_mt5_queue(278A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run278A_report",
        "\n".join(
            [
                f"- run278A_report(278A 보고서): `{rel(RUN_REPORT)}`",
                f"- run278A_branch_plan(278A 분기 계획): `{rel(BRANCH_PLAN)}`",
                f"- run278A_mt5_queue(278A MT5 대기열): `{rel(MT5_QUEUE)}`",
                f"- run278A_payload_contract(278A 페이로드 계약): `{rel(PAYLOAD_CONTRACT)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_mt5_probe_packet_design`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run278A_summary",
        (
            f"- run278A_summary(278A 요약): fresh thesis MT5 probe packet(새 논제 MT5 탐침 묶음)을 branch(분기) `{len(branch_rows)}`개와 "
            f"MT5 probe design queue(MT5 탐침 설계 대기열) `{len(mt5_rows)}`개로 설계했다. Effect(효과): run278B(278B 실행)가 payload(페이로드)를 만들 수 있지만 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE278_ID}")
    focus = (
        "- >-\n"
        f"  Stage278(278단계) run278A(278A 실행) fresh thesis MT5 probe packet design(새 논제 MT5 탐침 묶음 설계) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(branch_rows)}`개와 MT5 probe design queue(MT5 탐침 설계 대기열) `{len(mt5_rows)}`개를 만들었고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage278(278단계) run278A(278A 실행)")
    write_text(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run278A Fresh thesis MT5 probe packet design(새 논제 MT5 탐침 묶음 설계)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): branch(분기) `{len(branch_rows)}`개와 MT5 probe design queue(MT5 탐침 설계 대기열) `{len(mt5_rows)}`개를 만들었다.\n"
            "- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278A",
        f"| `IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278A` | `{STAGE278_ID}` | `cp277C/cp277D` score surface(점수 표면)를 MT5(`MetaTrader 5`, 메타트레이더5) payload(페이로드)용 branch(분기) `{len(branch_rows)}`개로 설계한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `design_ready_no_candidate` | MT5 probe design queue(MT5 탐침 설계 대기열) `{len(mt5_rows)}`개; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def run() -> dict[str, Any]:
    queue_rows = read_csv_rows(SOURCE_QUEUE)
    if not queue_rows:
        raise RuntimeError("Stage278 probe queue is empty.")
    inputs = source_paths(queue_rows)
    must_exist(inputs)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    branch_rows, metrics, threshold_payload, frames = build_design(queue_rows)
    mt5_rows = build_mt5_queue(branch_rows, queue_rows)
    payload_rows = build_payload_contract(branch_rows, frames)
    tester_rows = build_tester_plan(mt5_rows, frames)

    write_csv(BRANCH_PLAN, BRANCH_COLUMNS, branch_rows)
    write_csv(BRANCH_METRICS, METRIC_COLUMNS, metrics)
    write_csv(MT5_QUEUE, MT5_QUEUE_COLUMNS, mt5_rows)
    write_csv(PAYLOAD_CONTRACT, PAYLOAD_COLUMNS, payload_rows)
    write_csv(TESTER_PLAN, TESTER_COLUMNS, tester_rows)
    write_receipts(queue_rows, branch_rows, metrics, mt5_rows, payload_rows, tester_rows, threshold_payload, frames)
    write_report(branch_rows, mt5_rows)

    outputs = [
        BRANCH_PLAN,
        BRANCH_METRICS,
        MT5_QUEUE,
        PAYLOAD_CONTRACT,
        TESTER_PLAN,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_FORENSICS_PLAN,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    manifest = manifest_payload(created_at, outputs, inputs, len(branch_rows), len(mt5_rows))
    write_json(RUN_MANIFEST, manifest)
    outputs.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, outputs, inputs, len(branch_rows), len(mt5_rows))
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    outputs.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, outputs, inputs, len(branch_rows), len(mt5_rows))
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, branch_rows, mt5_rows, outputs)
    update_state_docs(branch_rows, mt5_rows)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE278_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "branch_rows": len(branch_rows),
        "mt5_probe_design_queue_rows": len(mt5_rows),
        "selected_candidate": "none",
        "adapter_package": "none",
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
