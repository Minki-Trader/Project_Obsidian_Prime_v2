from __future__ import annotations

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
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "277_onnx_candidate_campaign__fresh_thesis_rebuild"
RUN_ID = "run277D_execute_fresh_thesis_scoring_probe_v1"
SOURCE_RUN_ID = "run277C_materialize_fresh_thesis_scoring_handoff_inputs_v1"
STATUS = "completed_fresh_thesis_scoring_probe_no_candidate_selection"
JUDGMENT = "fresh_thesis_score_tables_materialized_no_candidate_selection"
NEXT_ACTION = "run277E_screen_fresh_thesis_score_surfaces"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN277C = STAGE / "02_runs" / "run277C"
RUN_DIR = STAGE / "02_runs" / "run277D"
SCORE_DIR = RUN_DIR / "scores"
HANDOFF_DIR = RUN_DIR / "handoff"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_SPECS = RUN277C / "scoring_input_specs.json"
SOURCE_HANDOFF = RUN277C / "handoff_input_plan.csv"
SOURCE_IDENTITY = RUN277C / "package_identity_receipts.csv"
SOURCE_MANIFEST = RUN277C / "run_manifest.json"

TIER_A_MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
TIER_A_FEATURE_ORDER = TIER_A_MODEL_INPUT.with_name("model_input_feature_order.txt")
TIER_A_SUMMARY = TIER_A_MODEL_INPUT.with_name("model_input_summary.json")
TIER_B_MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v1" / "model_input_dataset.parquet"
TIER_B_FEATURE_ORDER = TIER_B_MODEL_INPUT.with_name("model_input_feature_order.txt")
TIER_B_SUMMARY = TIER_B_MODEL_INPUT.with_name("model_input_summary.json")

SCORE_SUMMARY = RUN_DIR / "score_surface_summary.csv"
TIER_SUMMARY = RUN_DIR / "tier_score_summary.csv"
HANDOFF_INDEX = RUN_DIR / "handoff_index.csv"
DATA_INTEGRITY = RUN_DIR / "data_integrity_receipt.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run277D_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage277/execute_fresh_thesis_scoring_probe.py")

SUMMARY_COLUMNS = (
    "package_id",
    "tier_scope",
    "split",
    "rows",
    "decision_count",
    "decision_rate",
    "mean_candidate_decision_score",
    "q70_candidate_decision_score",
    "q85_candidate_decision_score",
    "q95_candidate_decision_score",
    "mean_model_risk_pct",
    "missing_required_feature_count",
    "missing_required_features",
    "selected_candidate",
    "onnx_readiness",
    "next_use",
)
HANDOFF_COLUMNS = ("package_id", "tier_scope", "score_table_path", "handoff_json_path", "score_rows", "score_sha256", "handoff_sha256", "boundary")
DATA_COLUMNS = ("tier_scope", "dataset_path", "feature_order_path", "feature_order_hash", "rows", "missing_required_feature_count", "missing_required_features", "judgment")
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


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def sha256_text(value: str) -> str:
    import hashlib

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_feature_order(path: Path) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def robust_z(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").astype("float64")
    median = numeric.median(skipna=True)
    mad = (numeric - median).abs().median(skipna=True)
    scale = mad * 1.4826 if mad and np.isfinite(mad) else numeric.std(skipna=True)
    if not scale or not np.isfinite(scale):
        return pd.Series(0.0, index=series.index)
    return ((numeric - median) / scale).replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(-6.0, 6.0)


def sigmoid(value: pd.Series | np.ndarray) -> pd.Series:
    array = np.asarray(value, dtype="float64")
    clipped = np.clip(array, -20.0, 20.0)
    return pd.Series(1.0 / (1.0 + np.exp(-clipped)))


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> pd.Series:
    if name not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[name], errors="coerce").astype("float64").fillna(default)


def prepare_view(path: Path, feature_order_path: Path, tier_scope: str, expected_features: Sequence[str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    frame = pd.read_parquet(io_path(path)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["tier_scope"] = tier_scope
    feature_order = load_feature_order(feature_order_path)
    feature_order_hash = sha256_text("\n".join(feature_order))
    missing = [feature for feature in expected_features if feature not in frame.columns]
    for feature in missing:
        frame[feature] = 0.0
    frame["missing_required_feature_count"] = len(missing)
    frame["missing_required_features"] = ";".join(missing) if missing else "none"
    receipt = {
        "tier_scope": tier_scope,
        "dataset_path": rel(path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_hash": feature_order_hash,
        "rows": len(frame),
        "missing_required_feature_count": len(missing),
        "missing_required_features": ";".join(missing) if missing else "none",
        "judgment": "usable_with_missing_features_recorded(누락 피처 기록 조건으로 사용 가능)" if missing else "usable_full_feature_context(전체 피처 문맥 사용 가능)",
    }
    return frame, receipt


def base_output(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": frame["timestamp"],
            "symbol": frame.get("symbol", pd.Series("US100", index=frame.index)),
            "split": frame["split"].astype(str),
            "tier_scope": frame["tier_scope"].astype(str),
            "package_id": spec["package_id"],
            "feature_order_hash": spec["feature_order_hash"],
            "feature_contract_hash": spec["feature_contract_hash"],
            "decision_rule_hash": spec["decision_rule_hash"],
            "adapter_schema_hash": spec["adapter_schema_hash"],
            "score_columns_hash": spec["score_columns_hash"],
            "missing_required_feature_count": frame["missing_required_feature_count"],
            "missing_required_features": frame["missing_required_features"],
            "claim_boundary": BOUNDARY,
        }
    )


def finalize_output(frame: pd.DataFrame, output: pd.DataFrame, side_score: pd.Series, decision_score: pd.Series) -> pd.DataFrame:
    decision = (decision_score >= decision_score.quantile(0.70)).astype("int8")
    side = np.where(side_score >= 0.0, 1, -1)
    output["candidate_decision_score"] = decision_score.clip(0.0, 1.0).round(8)
    output["materialized_decision_flag"] = decision
    output["entry_signal"] = decision * side
    output["route_code"] = output["package_id"].astype(str).str.extract(r"^(cp277.)", expand=False).fillna("cp277")
    output["model_risk_pct"] = (0.01 + 0.02 * output["candidate_decision_score"]).round(6)
    output["atr_stop_multiplier"] = (1.6 + 0.6 * (1.0 - output["candidate_decision_score"])).round(6)
    output["atr_take_profit_multiplier"] = (1.8 + 0.8 * output["candidate_decision_score"]).round(6)
    output["max_hold_bars"] = np.where(output["candidate_decision_score"] >= 0.85, 12, 8)
    output["reentry_cooldown_bars"] = np.where(output["candidate_decision_score"] >= 0.85, 4, 8)
    return output


def score_cp277a(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    cash = col(frame, "is_us_cash_open")
    session_loss = sigmoid(0.35 * col(frame, "is_last_30m_before_cash_close") + 0.25 * (1.0 - cash) + 0.20 * robust_z(col(frame, "vix_zscore_20").abs()) + 0.20 * robust_z(col(frame, "historical_vol_5_over_20").abs()))
    retention = sigmoid(0.30 * robust_z(col(frame, "adx_14").abs()) + 0.25 * robust_z(col(frame, "atr_14_over_atr_50").abs()) + 0.25 * robust_z(col(frame, "bb_squeeze").abs()) + 0.20 * cash)
    weak_cut = (1.0 - session_loss).clip(0.0, 1.0)
    risk_multiplier = (1.0 - 0.45 * session_loss + 0.25 * retention).clip(0.0, 1.0)
    decision = (retention * weak_cut * risk_multiplier).clip(0.0, 1.0)
    output = base_output(frame, spec)
    output["session_loss_state_score"] = session_loss.round(8)
    output["entry_retention_score"] = retention.round(8)
    output["weak_session_cut_score"] = weak_cut.round(8)
    output["risk_multiplier_score"] = risk_multiplier.round(8)
    return finalize_output(frame, output, col(frame, "di_spread_14"), decision)


def score_cp277b(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    vol = robust_z(col(frame, "atr_14_over_atr_50").abs())
    validation_margin = sigmoid(0.25 * robust_z(col(frame, "adx_14")) + 0.25 * robust_z(col(frame, "rsi_14_slope_3")) + 0.20 * robust_z(col(frame, "return_zscore_20").abs()) - 0.20 * vol)
    supply = sigmoid(0.25 * robust_z(col(frame, "log_return_1").abs()) + 0.20 * col(frame, "is_us_cash_open") + 0.20 * robust_z(col(frame, "di_spread_14").abs()) + 0.15 * robust_z(col(frame, "atr_14").abs()))
    pf_floor = (0.55 * validation_margin + 0.45 * supply).clip(0.0, 1.0)
    risk_cap = (1.0 - 0.35 * sigmoid(vol)).clip(0.0, 1.0)
    decision = (pf_floor * supply * risk_cap).clip(0.0, 1.0)
    output = base_output(frame, spec)
    output["pf_floor_score"] = pf_floor.round(8)
    output["supply_state_score"] = supply.round(8)
    output["validation_margin_score"] = validation_margin.round(8)
    output["risk_cap_score"] = risk_cap.round(8)
    return finalize_output(frame, output, col(frame, "return_zscore_20"), decision)


def score_cp277c(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    divergence = robust_z(col(frame, "us100_minus_mega8_equal_return_1")) + robust_z(col(frame, "us100_minus_top3_weighted_return_1"))
    sign_score = sigmoid(divergence.abs())
    session_pressure = sigmoid(0.35 * robust_z(col(frame, "mega8_dispersion_5").abs()) + 0.25 * robust_z(col(frame, "minutes_from_cash_open").abs()) + 0.20 * robust_z(col(frame, "di_spread_14").abs()))
    side_reversal = sigmoid(0.45 * sign_score + 0.30 * session_pressure + 0.25 * robust_z(col(frame, "vortex_indicator").abs()))
    side_risk = (1.0 - 0.40 * session_pressure + 0.20 * sign_score).clip(0.0, 1.0)
    decision = (side_reversal * side_risk).clip(0.0, 1.0)
    output = base_output(frame, spec)
    output["side_reversal_score"] = side_reversal.round(8)
    output["divergence_sign_score"] = sign_score.round(8)
    output["session_pressure_score"] = session_pressure.round(8)
    output["side_risk_score"] = side_risk.round(8)
    return finalize_output(frame, output, divergence, decision)


def score_cp277d(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    squeeze = sigmoid(0.45 * robust_z(col(frame, "bb_squeeze").abs()) + 0.25 * robust_z(col(frame, "bollinger_width_20").abs()) + 0.20 * robust_z(col(frame, "historical_vol_5_over_20").abs()))
    macro = sigmoid(0.25 * robust_z(col(frame, "vix_zscore_20").abs()) + 0.20 * robust_z(col(frame, "us10yr_zscore_20").abs()) + 0.20 * robust_z(col(frame, "usdx_zscore_20").abs()) + 0.15 * robust_z(col(frame, "mega8_dispersion_5").abs()))
    late_loss_compression = (1.0 - 0.35 * sigmoid(robust_z(col(frame, "minutes_from_cash_open").abs())) + 0.25 * squeeze).clip(0.0, 1.0)
    cooldown = (1.0 - 0.30 * macro + 0.20 * late_loss_compression).clip(0.0, 1.0)
    contrast = (squeeze * cooldown * late_loss_compression).clip(0.0, 1.0)
    output = base_output(frame, spec)
    output["macro_squeeze_state_score"] = squeeze.round(8)
    output["contrast_reward_score"] = contrast.round(8)
    output["late_loss_compression_score"] = late_loss_compression.round(8)
    output["cooldown_score"] = cooldown.round(8)
    return finalize_output(frame, output, col(frame, "ema20_ema50_diff"), contrast)


SCORERS: dict[str, Callable[[pd.DataFrame, Mapping[str, Any]], pd.DataFrame]] = {
    "cp277A_session_loss_avoidance_surface": score_cp277a,
    "cp277B_validation_pf_floor_rebalanced_entry_surface": score_cp277b,
    "cp277C_directional_asymmetry_reversal_surface": score_cp277c,
    "cp277D_macro_squeeze_failure_contrast_surface": score_cp277d,
}


def summarize_score(output: pd.DataFrame, package_id: str, tier_scope: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, group in output.groupby("split", dropna=False):
        score = pd.to_numeric(group["candidate_decision_score"], errors="coerce")
        rows.append(
            {
                "package_id": package_id,
                "tier_scope": tier_scope,
                "split": split,
                "rows": len(group),
                "decision_count": int(group["materialized_decision_flag"].sum()),
                "decision_rate": float(group["materialized_decision_flag"].mean()),
                "mean_candidate_decision_score": float(score.mean()),
                "q70_candidate_decision_score": float(score.quantile(0.70)),
                "q85_candidate_decision_score": float(score.quantile(0.85)),
                "q95_candidate_decision_score": float(score.quantile(0.95)),
                "mean_model_risk_pct": float(pd.to_numeric(group["model_risk_pct"], errors="coerce").mean()),
                "missing_required_feature_count": int(group["missing_required_feature_count"].max()),
                "missing_required_features": str(group["missing_required_features"].iloc[0]),
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "next_use": "score_surface_screen",
            }
        )
    return rows


def combined_summary(a_rows: pd.DataFrame, b_rows: pd.DataFrame, package_id: str) -> list[dict[str, Any]]:
    combined = pd.concat([a_rows, b_rows], ignore_index=True)
    return summarize_score(combined, package_id, "Tier A+B combined")


def write_outputs(specs: Sequence[Mapping[str, Any]], tier_a: pd.DataFrame, tier_b: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    summary_rows: list[dict[str, Any]] = []
    tier_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for spec in specs:
        package_id = spec["package_id"]
        scorer = SCORERS[package_id]
        tier_outputs: dict[str, pd.DataFrame] = {}
        for tier_scope, frame in [("Tier A", tier_a), ("Tier B", tier_b)]:
            output = scorer(frame, spec)
            score_path = SCORE_DIR / f"{package_id}_{tier_scope.lower().replace(' ', '_')}_scores.parquet"
            io_path(score_path.parent).mkdir(parents=True, exist_ok=True)
            output.to_parquet(io_path(score_path), index=False)
            artifacts.append(score_path)
            tier_outputs[tier_scope] = output
            rows = summarize_score(output, package_id, tier_scope)
            summary_rows.extend(rows)
            tier_rows.extend(rows)
        combined_rows = combined_summary(tier_outputs["Tier A"], tier_outputs["Tier B"], package_id)
        summary_rows.extend(combined_rows)
        tier_rows.extend(combined_rows)
        handoff_path = HANDOFF_DIR / f"{package_id}_handoff.json"
        handoff_payload = {
            "package_id": package_id,
            "run_id": RUN_ID,
            "score_tables": {
                "Tier A": rel(SCORE_DIR / f"{package_id}_tier_a_scores.parquet"),
                "Tier B": rel(SCORE_DIR / f"{package_id}_tier_b_scores.parquet"),
            },
            "feature_order_hash": spec["feature_order_hash"],
            "feature_contract_hash": spec["feature_contract_hash"],
            "decision_rule_hash": spec["decision_rule_hash"],
            "adapter_schema_hash": spec["adapter_schema_hash"],
            "score_columns_hash": spec["score_columns_hash"],
            "claim_boundary": BOUNDARY,
        }
        write_json(handoff_path, handoff_payload)
        artifacts.append(handoff_path)
        handoff_rows.append(
            {
                "package_id": package_id,
                "tier_scope": "Tier A/Tier B",
                "score_table_path": ";".join(handoff_payload["score_tables"].values()),
                "handoff_json_path": rel(handoff_path),
                "score_rows": len(tier_outputs["Tier A"]) + len(tier_outputs["Tier B"]),
                "score_sha256": ";".join(sha256_file_lf_normalized(SCORE_DIR / f"{package_id}_{tier.lower().replace(' ', '_')}_scores.parquet") for tier in ("Tier A", "Tier B")),
                "handoff_sha256": sha256_file_lf_normalized(handoff_path),
                "boundary": BOUNDARY,
            }
        )
    return summary_rows, tier_rows, handoff_rows, artifacts


def write_report(summary_rows: Sequence[Mapping[str, Any]], package_count: int) -> None:
    oos_lines = []
    for row in summary_rows:
        if row["tier_scope"] == "Tier A+B combined" and row["split"] == "oos":
            oos_lines.append(
                f"- `{row['package_id']}` combined OOS(합산 표본외): decision_rate(판단 비율) `{float(row['decision_rate']):.4f}`, mean_score(평균 점수) `{float(row['mean_candidate_decision_score']):.4f}`"
            )
    write_md(
        REPORT,
        f"""# run277D Report(277D 보고서): Fresh Thesis Scoring Probe(새 논제 점수 탐침)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- package_rows(패키지 행): `{package_count}`
- summary_rows(요약 행): `{len(summary_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## OOS Combined Read(표본외 합산 판독)

{chr(10).join(oos_lines)}

## Boundary(경계)

run277D(277D 실행)는 score table(점수표)와 handoff JSON(인계 JSON)을 만들었다.
Effect(효과): 다음 run277E(277E 실행)에서 score surface(점수 표면)를 선별할 수 있지만, selected candidate(선택 후보), MT5 runtime result(MT5 런타임 결과), ONNX readiness(온엑스 준비)는 아직 없다.
""",
    )


def write_receipts(summary_rows: Sequence[Mapping[str, Any]], data_rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run277D fresh thesis scoring probe(277D 새 논제 점수 탐침)",
                "evidence_available": "score tables(점수표), tier score summary(티어 점수 요약), handoff JSON(인계 JSON), data integrity receipt(데이터 무결성 영수증)",
                "evidence_missing": "MT5 runtime result(MT5 런타임 결과), backtest KPI(백테스트 핵심 성과 지표), selected candidate(선택 후보), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "score_materialized_no_selection(점수 물질화, 선택 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "점수표는 만들어졌지만 MT5 결과와 후보 선택은 아직 없다.",
            }
        ],
    )
    tier_b_missing = max(int(row["missing_required_feature_count"]) for row in data_rows if row["tier_scope"] == "Tier B")
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "data_integrity_gate(데이터 무결성 게이트)",
                "status": "passed_with_tier_b_missing_features_recorded(Tier B 누락 피처 기록 조건으로 통과)" if tier_b_missing else "passed(통과)",
                "evidence_path": rel(DATA_INTEGRITY),
                "effect": "Tier B(티어 B)의 부분 문맥 누락을 숨기지 않는다.",
            },
            {
                "gate_name": "paired_tier_scoring_gate(티어 쌍 점수 게이트)",
                "status": "passed_tier_a_tier_b_combined_rows_written(Tier A/Tier B/합산 행 작성으로 통과)",
                "evidence_path": rel(TIER_SUMMARY),
                "effect": "Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산)을 모두 남긴다.",
            },
            {
                "gate_name": "runtime_handoff_gate(런타임 인계 게이트)",
                "status": "passed_handoff_json_written(인계 JSON 작성으로 통과)",
                "evidence_path": rel(HANDOFF_INDEX),
                "effect": "다음 실행이 score table(점수표)과 해시를 소비할 수 있다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/온엑스 없음/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "점수 물질화를 후보 선택이나 MT5 결과로 올려 말하지 않는다.",
            },
        ],
    )


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def manifest_payload(created_at: str, outputs: Sequence[Path], package_count: int) -> dict[str, Any]:
    sources = [SOURCE_SPECS, SOURCE_HANDOFF, SOURCE_IDENTITY, SOURCE_MANIFEST, TIER_A_MODEL_INPUT, TIER_A_FEATURE_ORDER, TIER_A_SUMMARY, TIER_B_MODEL_INPUT, TIER_B_FEATURE_ORDER, TIER_B_SUMMARY]
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "consumer": [STAGE_ID, NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
        "source_inputs": [rel(path) for path in sources],
        "source_hashes": output_hashes(sources),
        "output_artifacts": [rel(path) for path in outputs],
        "output_hashes": output_hashes(outputs),
        "package_count": package_count,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": manifest["consumer"],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def update_registers(created_at: str, package_count: int, outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "scoring_probe",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"package_rows={package_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__scoring_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "scoring_probe",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "run277D scoring probe(277D 점수 탐침)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "score_materialization",
                "scoreboard_lane": "fresh_thesis_rebuild",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"package_rows={package_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_score_materialization",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__scoring_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_scoring_probe",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "score_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "score_materialization_only_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"package_rows={package_count};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "run277D_scoring_probe_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run277D scoring probe artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(package_count: int) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run277D_report", f"- run277D_report(277D 보고서): `{rel(REPORT)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review_index = append_once(
        review_index,
        "run277D_report",
        "\n".join(
            [
                f"- run277D_report(277D 보고서): `{rel(REPORT)}`",
                f"- run277D_score_summary(277D 점수 요약): `{rel(SCORE_SUMMARY)}`",
                f"- run277D_handoff_index(277D 인계 색인): `{rel(HANDOFF_INDEX)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_scoring_probe`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run277D_summary",
        (
            f"- run277D_summary(277D 요약): package(패키지) `{package_count}`개에 대해 Tier A/Tier B(티어 A/티어 B) score table(점수표)와 handoff JSON(인계 JSON)을 만들었다. "
            "Effect(효과): run277E(277E 실행) score surface screen(점수 표면 선별)로 넘기며 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage277(277단계) run277D(277D 실행) fresh thesis scoring probe(새 논제 점수 탐침) `{RUN_ID}`. "
        f"Effect(효과): package(패키지) `{package_count}`개에 대해 Tier A/Tier B(티어 A/티어 B) score table(점수표)을 만들었고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage277(277단계) run277D(277D 실행)")
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run277D Fresh thesis scoring probe(새 논제 점수 탐침)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): score table(점수표)와 handoff JSON(인계 JSON)을 만들고 run277E(277E 실행) score surface screen(점수 표면 선별)로 넘긴다.\n"
            "- boundary(경계): selected candidate(선택 후보), MT5 runtime result(MT5 런타임 결과), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST277-FRESH-THESIS-REBUILD-RUN277D",
        f"| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277D` | `{STAGE_ID}` | run277C(277C 실행) scoring specs(점수 규격)를 Tier A/Tier B(티어 A/티어 B) score table(점수표)로 물질화한다. | `packages={package_count}` | `score_materialized_no_selection` | next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def run() -> dict[str, Any]:
    must_exist([SOURCE_SPECS, SOURCE_HANDOFF, SOURCE_IDENTITY, SOURCE_MANIFEST, TIER_A_MODEL_INPUT, TIER_A_FEATURE_ORDER, TIER_A_SUMMARY, TIER_B_MODEL_INPUT, TIER_B_FEATURE_ORDER, TIER_B_SUMMARY])
    io_path(SCORE_DIR).mkdir(parents=True, exist_ok=True)
    io_path(HANDOFF_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    specs_payload = json.loads(io_path(SOURCE_SPECS).read_text(encoding="utf-8"))
    specs = specs_payload["packages"]
    expected_features = sorted({feature for spec in specs for feature in str(spec["feature_surface"]).replace(",", ";").split(";")})
    blueprint_payload = json.loads(io_path(STAGE / "02_runs" / "run277B" / "package_blueprints.json").read_text(encoding="utf-8"))
    expected_base = sorted({feature for package in blueprint_payload["packages"] for feature in package["feature_contract"]["base_features"]})
    tier_a, tier_a_receipt = prepare_view(TIER_A_MODEL_INPUT, TIER_A_FEATURE_ORDER, "Tier A", expected_base)
    tier_b, tier_b_receipt = prepare_view(TIER_B_MODEL_INPUT, TIER_B_FEATURE_ORDER, "Tier B", expected_base)
    summary_rows, tier_rows, handoff_rows, score_artifacts = write_outputs(specs, tier_a, tier_b)
    data_rows = [tier_a_receipt, tier_b_receipt]
    write_csv(SCORE_SUMMARY, SUMMARY_COLUMNS, summary_rows)
    write_csv(TIER_SUMMARY, SUMMARY_COLUMNS, tier_rows)
    write_csv(HANDOFF_INDEX, HANDOFF_COLUMNS, handoff_rows)
    write_csv(DATA_INTEGRITY, DATA_COLUMNS, data_rows)
    write_report(summary_rows, len(specs))
    write_receipts(summary_rows, data_rows)

    outputs = [SCORE_SUMMARY, TIER_SUMMARY, HANDOFF_INDEX, DATA_INTEGRITY, RESULT_JUDGMENT, GATE_AUDIT, REPORT] + score_artifacts
    manifest = manifest_payload(created_at, outputs, len(specs))
    write_json(RUN_MANIFEST, manifest)
    outputs.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, outputs, len(specs))
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    outputs.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, outputs, len(specs))
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, len(specs), outputs)
    update_state_docs(len(specs))

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "package_rows": len(specs),
        "summary_rows": len(summary_rows),
        "handoff_rows": len(handoff_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
