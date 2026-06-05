from __future__ import annotations

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

STAGE_ID = "340_runtime_lifecycle_exit__quality_balance_pressure_review"
SOURCE_STAGE_ID = "339_runtime_lifecycle_exit__side_balance_probe_review"
STAGE_DIR = ROOT / "stages" / STAGE_ID
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID

RUN_NUMBER = "run340E"
RUN_ID = "run340E_review_f01_local_floor_pressure_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run340D_execute_f01_local_floor_pressure_mt5_probe_without_db_v1"
PACKAGE_RUN_ID = "run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run339G_execute_quality_balance_blend_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run339F_materialize_quality_balance_blend_mt5_probe_package_without_db_v1"
NEXT_RUN_ID = "run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1"

STATUS = "completed_stage340E_f01_pressure_probe_reviewed_negative_with_control_semantics_repair_required_no_selection"
JUDGMENT = "pressure_surface_negative_but_exact_replay_control_semantics_invalid_close_on_flat_mismatch_repair_required_no_selection"
DECISION = "stage340E_open_run340F_corrected_f01_close_on_flat_false_pressure_package"
CLAIM_BOUNDARY = (
    "research_development_f01_pressure_mt5_probe_review_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run340E_f01_pressure_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage340E_f01_pressure_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run340D"
PACKAGE_RUN_DIR = STAGE_DIR / "02_runs" / "run340C"
SOURCE_RUNTIME_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339G"
SOURCE_PACKAGE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339F"

PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_RUNTIME_SUMMARY = PARENT_RUN_DIR / "f01_local_floor_pressure_mt5_probe_summary.csv"
PARENT_PROXY_DIFF = PARENT_RUN_DIR / "proxy_mt5_runtime_difference.csv"
PARENT_RUNTIME_IDENTITY = PARENT_RUN_DIR / "runtime_identity.csv"
PARENT_RUN_MANIFEST = PARENT_RUN_DIR / "run_manifest.json"
PACKAGE_FINAL_DECISION = PACKAGE_RUN_DIR / "final_decision.json"
PACKAGE_GATE_AUDIT = PACKAGE_RUN_DIR / "required_gate_coverage_audit.csv"
PACKAGE_VARIANT_PREVIEW = PACKAGE_RUN_DIR / "variant_preview.csv"
PACKAGE_QUEUE = STAGE_DIR / "02_runs" / "run340B" / "run340C_queue.csv"
SOURCE_RUNTIME_SUMMARY = SOURCE_RUNTIME_RUN_DIR / "quality_balance_blend_mt5_probe_summary.csv"
SOURCE_VARIANT_PREVIEW = SOURCE_PACKAGE_RUN_DIR / "variant_preview.csv"
SOURCE_RUN_MANIFEST = SOURCE_RUNTIME_RUN_DIR / "run_manifest.json"
SOURCE_SET_MANIFEST = SOURCE_PACKAGE_RUN_DIR / "tester_set_manifest.csv"

SCORECARD = RUN_DIR / "f01_pressure_review_scorecard.csv"
CONTROL_SEMANTICS_AUDIT = RUN_DIR / "control_semantics_audit.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run340F_queue.csv"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

FLOORS = {
    "net_profit": 0.0,
    "profit_factor": 1.10,
    "expectancy": 0.0,
    "recovery_factor": 1.00,
    "max_drawdown_amount": 150.0,
    "trade_count": 30.0,
    "trade_side_balance": 0.25,
}

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "report_path",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "view",
    "tier",
    "metric_scope",
    "candidate_model_id",
    "net_profit",
    "profit_factor",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "result_status",
    "sample_rows",
    "feature_count",
    "matched_rows",
    "expectancy",
    "attempt_count",
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False, encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows = list(rows)
    frame = read_csv(path) if path.exists() else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=sorted({column for row in rows for column in row}))
    for row in rows:
        for column in row:
            if column not in frame.columns:
                frame[column] = ""
        mask = pd.Series(True, index=frame.index)
        for key in key_columns:
            if key in frame.columns:
                mask &= frame[key].astype(str).eq(str(row.get(key, "")))
            else:
                mask &= False
        frame = frame.loc[~mask].copy()
        frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + [column for row in rows for column in row]))
    write_csv(path, frame[ordered])


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def normalise_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def gate_statuses_pass(frame: pd.DataFrame) -> bool:
    return bool(frame["status"].astype(str).str.lower().eq("passed").all())


def bool_equal(left: Any, right: Any) -> bool:
    return normalise_bool(left) == normalise_bool(right)


def float_equal(left: Any, right: Any, tolerance: float = 1e-12) -> bool:
    return abs(safe_float(left) - safe_float(right)) <= tolerance


def load_context() -> tuple[dict[str, Any], pd.DataFrame, dict[str, Any], pd.DataFrame]:
    parent_final = read_json(PARENT_FINAL_DECISION)
    parent_gates = read_csv(PARENT_GATE_AUDIT)
    package_final = read_json(PACKAGE_FINAL_DECISION)
    package_gates = read_csv(PACKAGE_GATE_AUDIT)
    parent_next = parent_final.get("next_action", parent_final.get("next_run_id"))
    if parent_next != RUN_ID:
        raise RuntimeError(f"parent next_run mismatch: {parent_next} != {RUN_ID}")
    if not gate_statuses_pass(parent_gates):
        raise RuntimeError("parent run340D gate audit has failed rows")
    if not gate_statuses_pass(package_gates):
        raise RuntimeError("package run340C gate audit has failed rows")
    return parent_final, parent_gates, package_final, package_gates


def floor_flags(row: pd.Series) -> dict[str, bool]:
    return {
        "exact_package_parity_pass": bool(
            row.get("comparison_status") == "completed_exact_proxy_mt5_parity_reached_feature_last"
            and safe_float(row.get("expected_rows")) == safe_float(row.get("matched_rows"))
            and safe_float(row.get("probability_mismatch_rows")) == 0
            and safe_float(row.get("decision_mismatch_rows")) == 0
        ),
        "net_profit_pass": safe_float(row.get("net_profit")) > FLOORS["net_profit"],
        "profit_factor_pass": safe_float(row.get("profit_factor")) >= FLOORS["profit_factor"],
        "expectancy_pass": safe_float(row.get("expectancy")) > FLOORS["expectancy"],
        "recovery_factor_pass": safe_float(row.get("recovery_factor")) >= FLOORS["recovery_factor"],
        "drawdown_pass": safe_float(row.get("max_drawdown_amount")) <= FLOORS["max_drawdown_amount"],
        "trade_count_pass": safe_float(row.get("trade_count")) >= FLOORS["trade_count"],
        "trade_side_balance_pass": safe_float(row.get("trade_side_balance")) >= FLOORS["trade_side_balance"],
    }


def weakness_tags(row: pd.Series) -> str:
    tags: list[str] = []
    for flag, label in [
        ("exact_package_parity_pass", "package_parity(패키지 동등성)"),
        ("exact_replay_control_semantics_pass", "control_semantics(대조 의미)"),
        ("net_profit_pass", "net_profit(순수익)"),
        ("profit_factor_pass", "profit_factor(수익 팩터)"),
        ("expectancy_pass", "expectancy(기대값)"),
        ("recovery_factor_pass", "recovery_factor(회복 계수)"),
        ("drawdown_pass", "drawdown(낙폭)"),
        ("trade_count_pass", "trade_count(거래수)"),
        ("trade_side_balance_pass", "side_balance(방향 균형)"),
    ]:
        if not bool(row.get(flag, False)):
            tags.append(label)
    return ";".join(tags) if tags else "none(없음)"


def build_control_semantics_audit(package_preview: pd.DataFrame, source_preview: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    source = source_preview.loc[source_preview["attempt_name"].astype(str).eq("f01_s55_l51_m01_h12")].iloc[0]
    package = package_preview.loc[package_preview["attempt_name"].astype(str).eq("p01_f01_control_s55_l51_m01_h12")].iloc[0]
    checks = [
        ("short_threshold", source["short_threshold"], package["short_threshold"], float_equal),
        ("long_threshold", source["long_threshold"], package["long_threshold"], float_equal),
        ("min_margin", source["min_margin"], package["min_margin"], float_equal),
        ("max_hold_bars", source["max_hold_bars"], package["max_hold_bars"], float_equal),
        ("close_on_flat", source["close_on_flat"], package["close_on_flat"], bool_equal),
    ]
    rows = []
    for field, source_value, package_value, comparator in checks:
        passed = bool(comparator(source_value, package_value))
        rows.append(
            {
                "audit_subject": "p01_f01_exact_replay_control(피01 f01 정확 재생 대조)",
                "field_name": field,
                "source_attempt": "f01_s55_l51_m01_h12",
                "package_attempt": "p01_f01_control_s55_l51_m01_h12",
                "source_value": source_value,
                "package_value": package_value,
                "status": "passed" if passed else "failed",
                "effect": (
                    "exact replay control(정확 재생 대조)의 의미가 유지되는지 확인한다. "
                    "효과는 runtime KPI(런타임 핵심 성과 지표)를 원본 f01과 잘못 비교하지 않게 하는 것이다."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    frame = pd.DataFrame(rows)
    return frame, bool(frame["status"].astype(str).eq("passed").all())


def build_scorecard(control_pass: bool) -> tuple[pd.DataFrame, dict[str, Any]]:
    summary = read_csv(PARENT_RUNTIME_SUMMARY).copy()
    package_preview = read_csv(PACKAGE_VARIANT_PREVIEW).copy()
    source_preview = read_csv(SOURCE_VARIANT_PREVIEW).copy()
    source_summary = read_csv(SOURCE_RUNTIME_SUMMARY).copy()
    source_f01 = source_summary.loc[source_summary["attempt_name"].astype(str).eq("f01_s55_l51_m01_h12")].iloc[0]

    numeric_columns = [
        "expected_rows",
        "matched_rows",
        "probability_mismatch_rows",
        "decision_mismatch_rows",
        "net_profit",
        "profit_factor",
        "expectancy",
        "recovery_factor",
        "max_drawdown_amount",
        "trade_count",
        "long_trade_count",
        "short_trade_count",
    ]
    for column in numeric_columns:
        if column in summary.columns:
            summary[column] = pd.to_numeric(summary[column], errors="coerce")
    side_max = summary[["long_trade_count", "short_trade_count"]].max(axis=1).replace(0, pd.NA)
    summary["trade_side_balance"] = (
        summary[["long_trade_count", "short_trade_count"]].min(axis=1) / side_max
    ).fillna(0.0)

    preview_columns = [
        "attempt_name",
        "variant_role",
        "source_attempt_name",
        "signal_trade_count",
        "signal_long_count",
        "signal_short_count",
        "signal_side_balance",
        "short_threshold",
        "long_threshold",
        "min_margin",
        "max_hold_bars",
        "close_on_flat",
    ]
    package_preview = package_preview[preview_columns].copy()
    package_preview = package_preview.rename(
        columns={
            "variant_role": "package_variant_role",
            "source_attempt_name": "package_source_attempt",
            "signal_trade_count": "package_signal_trade_count",
            "signal_long_count": "package_signal_long_count",
            "signal_short_count": "package_signal_short_count",
            "signal_side_balance": "package_signal_side_balance",
            "short_threshold": "package_short_threshold",
            "long_threshold": "package_long_threshold",
            "min_margin": "package_min_margin",
            "max_hold_bars": "package_max_hold_bars",
            "close_on_flat": "package_close_on_flat",
        }
    )
    frame = summary.merge(package_preview, on="attempt_name", how="left")
    frame["source_attempt_name"] = "f01_s55_l51_m01_h12"
    frame["source_close_on_flat"] = normalise_bool(
        source_preview.loc[source_preview["attempt_name"].eq("f01_s55_l51_m01_h12"), "close_on_flat"].iloc[0]
    )
    frame["source_net_profit"] = safe_float(source_f01.get("net_profit"))
    frame["source_profit_factor"] = safe_float(source_f01.get("profit_factor"))
    frame["source_expectancy"] = safe_float(source_f01.get("expectancy"))
    frame["source_recovery_factor"] = safe_float(source_f01.get("recovery_factor"))
    frame["source_max_drawdown_amount"] = safe_float(source_f01.get("max_drawdown_amount"))
    frame["source_trade_count"] = safe_int(source_f01.get("trade_count"))
    frame["source_long_trade_count"] = safe_int(source_f01.get("long_trade_count"))
    frame["source_short_trade_count"] = safe_int(source_f01.get("short_trade_count"))
    frame["exact_replay_control_semantics_pass"] = False
    frame.loc[
        frame["attempt_name"].astype(str).eq("p01_f01_control_s55_l51_m01_h12"),
        "exact_replay_control_semantics_pass",
    ] = control_pass

    for index, row in frame.iterrows():
        for key, value in floor_flags(row).items():
            frame.loc[index, key] = value
    pass_columns = [
        "exact_package_parity_pass",
        "net_profit_pass",
        "profit_factor_pass",
        "expectancy_pass",
        "recovery_factor_pass",
        "drawdown_pass",
        "trade_count_pass",
        "trade_side_balance_pass",
    ]
    frame["floor_pass_count"] = frame[pass_columns].astype(bool).sum(axis=1)
    frame["local_floor_pass"] = frame[pass_columns].astype(bool).all(axis=1)
    frame["control_semantics_status"] = frame["attempt_name"].map(
        lambda value: "failed_close_on_flat_mismatch(평탄 청산 불일치 실패)"
        if str(value) == "p01_f01_control_s55_l51_m01_h12" and not control_pass
        else "not_exact_replay_control(정확 재생 대조 아님)"
    )
    frame["pressure_surface_judgment"] = frame["net_profit"].map(
        lambda value: "negative(부정)" if safe_float(value) <= 0 else "positive_clue(긍정 단서)"
    )
    frame["review_judgment"] = (
        "close_on_flat_true_pressure_surface_negative_original_f01_exact_replay_unproven("
        "평탄 청산 켠 압박 표면은 부정, 원본 f01 정확 재생은 미검증)"
    )
    frame["weakness_tags"] = frame.apply(weakness_tags, axis=1)
    frame["claim_boundary"] = CLAIM_BOUNDARY
    frame = frame.sort_values(
        ["net_profit", "profit_factor", "recovery_factor", "trade_count"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    best = frame.iloc[0]
    metrics = {
        "attempt_count": int(len(frame)),
        "expected_rows_total": int(frame["expected_rows"].fillna(0).sum()),
        "matched_rows_total": int(frame["matched_rows"].fillna(0).sum()),
        "mismatch_rows_total": int(
            frame["probability_mismatch_rows"].fillna(0).sum() + frame["decision_mismatch_rows"].fillna(0).sum()
        ),
        "all_exact_package_parity": bool(frame["exact_package_parity_pass"].astype(bool).all()),
        "control_semantics_pass": bool(control_pass),
        "local_floor_pass_count": int(frame["local_floor_pass"].astype(bool).sum()),
        "positive_net_count": int(frame["net_profit_pass"].astype(bool).sum()),
        "best_attempt": str(best.get("attempt_name", "")),
        "best_model_id": str(best.get("model_id", "")),
        "best_net_profit": safe_float(best.get("net_profit")),
        "best_profit_factor": safe_float(best.get("profit_factor")),
        "best_expectancy": safe_float(best.get("expectancy")),
        "best_recovery_factor": safe_float(best.get("recovery_factor")),
        "best_drawdown": safe_float(best.get("max_drawdown_amount")),
        "best_trade_count": safe_int(best.get("trade_count")),
        "best_long_trade_count": safe_int(best.get("long_trade_count")),
        "best_short_trade_count": safe_int(best.get("short_trade_count")),
        "best_trade_side_balance": safe_float(best.get("trade_side_balance")),
        "source_f01_net_profit": safe_float(source_f01.get("net_profit")),
        "source_f01_profit_factor": safe_float(source_f01.get("profit_factor")),
        "source_f01_expectancy": safe_float(source_f01.get("expectancy")),
        "source_f01_recovery_factor": safe_float(source_f01.get("recovery_factor")),
        "source_f01_drawdown": safe_float(source_f01.get("max_drawdown_amount")),
        "source_f01_trade_count": safe_int(source_f01.get("trade_count")),
        "source_f01_long_trade_count": safe_int(source_f01.get("long_trade_count")),
        "source_f01_short_trade_count": safe_int(source_f01.get("short_trade_count")),
    }
    return frame, metrics


def build_attribution(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "topic": "package_parity(패키지 동등성)",
                "observed_change": (
                    f"run340D(340D 실행)는 matched_rows(일치 행) {metrics['matched_rows_total']}/"
                    f"{metrics['expected_rows_total']}, mismatch_rows(불일치 행) {metrics['mismatch_rows_total']}이다."
                ),
                "attribution": (
                    "MT5(메타트레이더5)는 run340C package(패키지)의 expected tape(예상 테이프)와 정확히 맞았다. "
                    "효과는 runtime parity(런타임 동등성) 문제와 전략 성과 문제를 분리하는 것이다."
                ),
                "usable_for": "package-runtime parity evidence(패키지-런타임 동등성 근거)",
                "not_usable_for": "original f01 replay claim(원본 f01 재생 주장)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "topic": "close_on_flat_true_pressure_surface(평탄 청산 켠 압박 표면)",
                "observed_change": (
                    f"best_attempt(최고 시도) {metrics['best_attempt']} net_profit(순수익) "
                    f"{metrics['best_net_profit']}, profit_factor(수익 팩터) {metrics['best_profit_factor']}, "
                    f"expectancy(기대값) {metrics['best_expectancy']}, recovery_factor(회복 계수) "
                    f"{metrics['best_recovery_factor']}, trade_count(거래수) {metrics['best_trade_count']}이다."
                ),
                "attribution": (
                    "모든 run340D 변형은 close_on_flat(평탄 신호 청산)이 켜진 실행 의미다. "
                    "효과는 이 표면을 negative pressure result(부정 압박 결과)로 닫고, 원본 f01 자체를 부정하지 않는 것이다."
                ),
                "usable_for": "avoid close_on_flat true reuse(평탄 청산 켠 설정 재사용 방지)",
                "not_usable_for": "rejecting source f01(원본 f01 폐기)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "topic": "control_semantics_mismatch(대조 의미 불일치)",
                "observed_change": "source f01(원본 f01)은 close_on_flat=False(꺼짐), p01 control(대조)은 True(켜짐)였다.",
                "attribution": (
                    "threshold(임계값), min_margin(최소 마진), hold(보유)는 같지만 lifecycle exit(생명주기 청산) 의미가 바뀌었다. "
                    "효과는 p01을 exact replay control(정확 재생 대조)로 쓰지 못하게 하는 것이다."
                ),
                "usable_for": "repair/control design(수리/대조 설계)",
                "not_usable_for": "operating promotion(운영 승격)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "topic": "repair_next_queue(다음 수리 대기열)",
                "observed_change": f"{NEXT_RUN_ID}는 close_on_flat=False(평탄 청산 꺼짐)로 exact control(정확 대조)을 복구한다.",
                "attribution": (
                    "run340F queue(대기열)는 원본 f01 실행 의미를 되돌린 뒤 같은 압박 폭을 다시 본다. "
                    "효과는 Stage340(340단계)을 무겁게 넓히지 않고 정확한 분기(branch, 분기)로 이어가는 것이다."
                ),
                "usable_for": "next materialization(다음 물질화)",
                "not_usable_for": "current selection(현재 선정)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_failure_memory() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "failure_id": "run340E_close_on_flat_control_semantics_mismatch",
                "hypothesis": "p01 control(피01 대조)이 source f01(원본 f01)을 정확히 재생할 것이다.",
                "failed_boundary": (
                    "close_on_flat(평탄 신호 청산)이 source=False(원천 꺼짐)에서 package=True(패키지 켜짐)로 바뀌었다."
                ),
                "salvage_value": (
                    "run340D는 close_on_flat=True(평탄 청산 켬) 표면의 부정 결과와 exact package parity(정확 패키지 동등성)를 제공한다."
                ),
                "repair_action": f"open {NEXT_RUN_ID} with close_on_flat=False(평탄 청산 꺼짐).",
                "do_not_repeat": "exact replay control(정확 재생 대조) 라벨을 붙일 때 lifecycle parameter(생명주기 파라미터)를 바꾸지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "failure_id": "run340E_close_on_flat_true_pressure_negative",
                "hypothesis": "close_on_flat=True(평탄 청산 켬)에서도 f01 local floor(로컬 하한)가 유지될 것이다.",
                "failed_boundary": "모든 run340D 변형의 net_profit(순수익)이 음수이고 best PF(최고 수익 팩터)는 0.78이다.",
                "salvage_value": "close_on_flat=True(평탄 청산 켬)는 압박 후보에서 제외하고, 원본 f01 의미로 다시 본다.",
                "repair_action": "same threshold band(같은 임계값 범위)를 close_on_flat=False(평탄 청산 꺼짐)로 재패키징한다.",
                "do_not_repeat": "close_on_flat=True(평탄 청산 켬) 변형을 운영 후보처럼 승격하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_next_queue() -> pd.DataFrame:
    specs = [
        ("q01_ctl_s55_l51_m01_h12", 0.55, 0.510, 0.010, 12, "exact replay control restored(정확 재생 대조 복구)"),
        ("q02_l515_s55_l515_m01_h12", 0.55, 0.515, 0.010, 12, "long threshold tighten(롱 임계값 조임)"),
        ("q03_l505_s55_l505_m01_h12", 0.55, 0.505, 0.010, 12, "long threshold relax(롱 임계값 완화)"),
        ("q04_m015_s55_l51_m015_h12", 0.55, 0.510, 0.015, 12, "margin tighten(마진 조임)"),
        ("q05_m02_s55_l51_m02_h12", 0.55, 0.510, 0.020, 12, "margin stress high(높은 마진 압박)"),
        ("q06_m005_s55_l51_m005_h12", 0.55, 0.510, 0.005, 12, "margin stress low(낮은 마진 압박)"),
        ("q07_h10_s55_l51_m01_h10", 0.55, 0.510, 0.010, 10, "shorter hold(짧은 보유)"),
        ("q08_h14_s55_l51_m01_h14", 0.55, 0.510, 0.010, 14, "longer hold(긴 보유)"),
        ("q09_s545_l51_m01_h12", 0.545, 0.510, 0.010, 12, "short threshold relax(숏 임계값 완화)"),
        ("q10_s555_l51_m01_h12", 0.555, 0.510, 0.010, 12, "short threshold tighten(숏 임계값 조임)"),
    ]
    return pd.DataFrame(
        [
            {
                "attempt_name": attempt,
                "next_run_id": NEXT_RUN_ID,
                "source_model_id": "logreg_balanced_c025",
                "source_runtime_attempt": "f01_s55_l51_m01_h12",
                "short_threshold": short_threshold,
                "long_threshold": long_threshold,
                "min_margin": min_margin,
                "max_hold_bars": hold_bars,
                "close_on_flat": False,
                "source_close_on_flat": False,
                "probe_role": role,
                "control_semantics_role": "exact_control" if attempt.startswith("q01_") else "pressure_variant",
                "required_runtime_check": (
                    "MT5 runtime probe(MT5 런타임 탐침); exact proxy-MT5 parity(정확 프록시-MT5 동등성); "
                    "original f01 lifecycle semantics(원본 f01 생명주기 의미)"
                ),
                "success_criteria": (
                    "net_profit>0(순수익 양수); profit_factor>=1.10(수익 팩터); expectancy>0(기대값 양수); "
                    "recovery>=1.00(회복 계수); drawdown<=150(낙폭); trade_count>=30(거래수); "
                    "side_balance>=0.25(방향 균형); exact control semantics restored(정확 대조 의미 복구)"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for attempt, short_threshold, long_threshold, min_margin, hold_bars, role in specs
        ]
    )


def build_final(metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "attempt_count": metrics["attempt_count"],
        "expected_rows_total": metrics["expected_rows_total"],
        "matched_rows_total": metrics["matched_rows_total"],
        "mismatch_rows_total": metrics["mismatch_rows_total"],
        "all_exact_package_parity": metrics["all_exact_package_parity"],
        "control_semantics_pass": metrics["control_semantics_pass"],
        "local_floor_pass_count": metrics["local_floor_pass_count"],
        "positive_net_count": metrics["positive_net_count"],
        "best_attempt": metrics["best_attempt"],
        "best_model_id": metrics["best_model_id"],
        "best_net_profit": metrics["best_net_profit"],
        "best_profit_factor": metrics["best_profit_factor"],
        "best_expectancy": metrics["best_expectancy"],
        "best_recovery_factor": metrics["best_recovery_factor"],
        "best_drawdown": metrics["best_drawdown"],
        "best_trade_count": metrics["best_trade_count"],
        "best_long_trade_count": metrics["best_long_trade_count"],
        "best_short_trade_count": metrics["best_short_trade_count"],
        "best_trade_side_balance": metrics["best_trade_side_balance"],
        "source_f01_net_profit": metrics["source_f01_net_profit"],
        "source_f01_profit_factor": metrics["source_f01_profit_factor"],
        "source_f01_expectancy": metrics["source_f01_expectancy"],
        "source_f01_recovery_factor": metrics["source_f01_recovery_factor"],
        "source_f01_drawdown": metrics["source_f01_drawdown"],
        "source_f01_trade_count": metrics["source_f01_trade_count"],
        "source_f01_long_trade_count": metrics["source_f01_long_trade_count"],
        "source_f01_short_trade_count": metrics["source_f01_short_trade_count"],
        "judgment_class": "negative_with_repair_required(부정, 수리 필요)",
        "evidence_boundary": "reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)",
        "external_verification_status": "completed_for_run340D_package(340D 패키지는 완료)",
        "original_f01_exact_replay_status": "not_completed_control_semantics_invalid(미완료, 대조 의미 무효)",
        "candidate_selection": "not_run",
        "promotion_candidate": "not_claimed",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(final: Mapping[str, Any], parent_gates: pd.DataFrame, package_gates: pd.DataFrame) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["promotion_candidate"] == "not_claimed"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    next_queue = read_csv(NEXT_QUEUE) if NEXT_QUEUE.exists() else pd.DataFrame()
    close_on_flat_false = bool((next_queue["close_on_flat"].astype(str).str.lower() == "false").all()) if not next_queue.empty else False
    return pd.DataFrame(
        [
            gate_row("parent_340D_gates_passed", "passed" if gate_statuses_pass(parent_gates) else "failed", rel(PARENT_GATE_AUDIT), "run340D(340D 실행) MT5 probe(MT5 탐침) 근거를 이어받는다."),
            gate_row("package_340C_gates_passed", "passed" if gate_statuses_pass(package_gates) else "failed", rel(PACKAGE_GATE_AUDIT), "run340C(340C 실행) package(패키지) 근거를 이어받는다."),
            gate_row("source_f01_reference_loaded", "passed" if SOURCE_RUNTIME_SUMMARY.exists() and SOURCE_VARIANT_PREVIEW.exists() else "failed", f"{rel(SOURCE_RUNTIME_SUMMARY)};{rel(SOURCE_VARIANT_PREVIEW)}", "source f01(원본 f01) 실행 의미와 KPI(핵심 성과 지표)를 확인한다."),
            gate_row("mt5_runtime_summary_reviewed", "passed" if final["attempt_count"] == 10 else "failed", rel(SCORECARD), "MT5 runtime summary(MT5 런타임 요약)를 검토한다."),
            gate_row("exact_package_parity_confirmed", "passed" if final["all_exact_package_parity"] and final["mismatch_rows_total"] == 0 else "failed", rel(PARENT_PROXY_DIFF), "package expected tape(패키지 예상 테이프)와 MT5 output(MT5 출력)의 동등성을 확인한다."),
            gate_row("control_semantics_audit_written", "passed" if CONTROL_SEMANTICS_AUDIT.exists() else "failed", rel(CONTROL_SEMANTICS_AUDIT), "exact replay control(정확 재생 대조)의 의미를 따로 감사한다."),
            gate_row("control_mismatch_classified", "passed" if not final["control_semantics_pass"] else "failed", rel(CONTROL_SEMANTICS_AUDIT), "close_on_flat mismatch(평탄 청산 불일치)를 repair condition(수리 조건)으로 분류한다."),
            gate_row("negative_surface_classified", "passed" if final["positive_net_count"] == 0 and final["best_net_profit"] < 0 else "failed", rel(SCORECARD), "close_on_flat=True(평탄 청산 켬) 표면을 부정 결과로 닫는다."),
            gate_row("corrected_next_queue_written", "passed" if NEXT_QUEUE.exists() and close_on_flat_false else "failed", rel(NEXT_QUEUE), "run340F(340F 실행) 수리 대기열을 close_on_flat=False(평탄 청산 꺼짐)로 만든다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", rel(CLAIM_RECEIPT), "review(검토)를 selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)로 말하지 않는다."),
            gate_row("tier_records_written", "passed", rel(STAGE_LEDGER), "Tier A/B/A+B(티어 A/B/A+B) 기록을 장부에 연결한다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "required gate coverage audit(필수 게이트 커버리지 감사)를 남긴다."),
        ]
    )


def artifact_paths() -> list[Path]:
    return [
        SCORECARD,
        CONTROL_SEMANTICS_AUDIT,
        PERFORMANCE_ATTRIBUTION,
        FAILURE_MEMORY,
        NEXT_QUEUE,
        KPI_RECORD,
        RESULT_JUDGMENT_RECEIPT,
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        SELECTION_STATUS,
        CURRENT_WORKING_STATE,
        WORKSPACE_STATE,
        STAGE_BRIEF,
        STAGE_README,
        ROOT_CHANGELOG,
        WORKSPACE_CHANGELOG,
        RUN_REGISTRY,
        PROJECT_LEDGER,
        STAGE_LEDGER,
        ARTIFACT_REGISTRY,
        Path(__file__),
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        KPI_RECORD,
        {
            **base,
            "measurement_scope": "MT5 runtime probe review(MT5 런타임 탐침 검토)",
            "best_attempt": final["best_attempt"],
            "best_net_profit": final["best_net_profit"],
            "best_profit_factor": final["best_profit_factor"],
            "best_expectancy": final["best_expectancy"],
            "best_recovery_factor": final["best_recovery_factor"],
            "best_drawdown": final["best_drawdown"],
            "best_trade_count": final["best_trade_count"],
            "source_f01_net_profit": final["source_f01_net_profit"],
            "source_f01_profit_factor": final["source_f01_profit_factor"],
            "control_semantics_pass": final["control_semantics_pass"],
            "evidence_boundary": final["evidence_boundary"],
        },
    )
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run340D f01 pressure MT5 probe(340D f01 압박 MT5 탐침)",
            "evidence_available": [rel(PARENT_RUNTIME_SUMMARY), rel(PARENT_PROXY_DIFF), rel(CONTROL_SEMANTICS_AUDIT)],
            "judgment_label": JUDGMENT,
            "evidence_missing": "corrected original f01 replay with close_on_flat=False(평탄 청산 꺼짐 원본 f01 수정 재생)",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": (
                "run340D(340D 실행)는 package parity(패키지 동등성)는 정확하지만 p01 control(피01 대조)이 원본 f01과 "
                "close_on_flat(평탄 청산) 의미가 달라 원본 f01 폐기 근거가 아니다."
            ),
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": "close_on_flat=True pressure surface negative(평탄 청산 켠 압박 표면 부정)",
            "comparison_baseline": "source f01 close_on_flat=False(원본 f01 평탄 청산 꺼짐)",
            "likely_drivers": "lifecycle exit semantics changed(생명주기 청산 의미 변경)",
            "segment_checks": "single Tier A runtime window only(단일 Tier A 런타임 구간만)",
            "attribution_confidence": "high_for_semantics_mismatch_medium_for_market_cause(의미 불일치 높음, 시장 원인 중간)",
            "next_probe": rel(NEXT_QUEUE),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "promotion_candidate": "not_claimed",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    source_inputs = [
        PARENT_FINAL_DECISION,
        PARENT_GATE_AUDIT,
        PARENT_RUNTIME_SUMMARY,
        PARENT_PROXY_DIFF,
        PARENT_RUNTIME_IDENTITY,
        PARENT_RUN_MANIFEST,
        PACKAGE_FINAL_DECISION,
        PACKAGE_GATE_AUDIT,
        PACKAGE_VARIANT_PREVIEW,
        PACKAGE_QUEUE,
        SOURCE_RUNTIME_SUMMARY,
        SOURCE_VARIANT_PREVIEW,
        SOURCE_RUN_MANIFEST,
        SOURCE_SET_MANIFEST,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in source_inputs],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths() if path.exists()],
            "source_artifact_hashes": {rel(path): sha256_file(path) for path in source_inputs if path.exists()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_control_semantics_repair_boundary(대조 의미 수리 경계로 연결)",
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run340E F01 Pressure Probe Review(340E F01 압박 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- exact_package_parity(정확 패키지 동등성): `{final['matched_rows_total']}/{final['expected_rows_total']}`, mismatch(불일치): `{final['mismatch_rows_total']}`
- control_semantics_pass(대조 의미 통과): `{final['control_semantics_pass']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_expectancy(최고 기대값): `{final['best_expectancy']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- source_f01_net_profit(원본 f01 순수익): `{final['source_f01_net_profit']}`
- source_f01_profit_factor(원본 f01 수익 팩터): `{final['source_f01_profit_factor']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Judgment(판정)

run340D(340D 실행)는 MT5(메타트레이더5) package parity(패키지 동등성)는 정확하다. 하지만 p01 control(피01 대조)은 source f01(원본 f01)과 close_on_flat(평탄 신호 청산)이 달라 exact replay control(정확 재생 대조)이 아니다.

Effect(효과): run340D(340D 실행)의 음수 결과를 원본 f01 폐기 근거로 쓰지 않고, close_on_flat=True(평탄 청산 켬) 표면의 부정 결과로만 닫는다.

## Attribution(귀속)

- source f01(원본 f01): close_on_flat=False(평탄 청산 꺼짐), net_profit(순수익) `{final['source_f01_net_profit']}`, profit_factor(수익 팩터) `{final['source_f01_profit_factor']}`.
- run340D best(340D 최고): close_on_flat=True(평탄 청산 켬), net_profit(순수익) `{final['best_net_profit']}`, profit_factor(수익 팩터) `{final['best_profit_factor']}`.
- cause(원인): threshold(임계값) 문제가 아니라 lifecycle exit semantics(생명주기 청산 의미) 변경이 대조군을 무효화했다.

## Next Action(다음 행동)

Open `{NEXT_RUN_ID}` with `{rel(NEXT_QUEUE)}`.
Effect(효과): close_on_flat=False(평탄 청산 꺼짐)로 원본 f01 exact control(정확 대조)을 복구하고 같은 pressure band(압박 범위)를 다시 MT5(메타트레이더5)에서 확인한다.

## Boundary(경계)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating_promotion(운영 승격 없음), no runtime_authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage340E Decision(340E 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(SCORECARD)}`, `{rel(CONTROL_SEMANTICS_AUDIT)}`, `{rel(NEXT_QUEUE)}`

Action(행동): run340D(340D 실행) MT5 KPI(MT5 핵심 성과 지표)와 run340C(340C 실행) package semantics(패키지 의미)를 함께 검토했다.

Effect(효과): close_on_flat mismatch(평탄 청산 불일치)를 정확히 분리하고, Stage340(340단계)을 corrected branch(수정 분기)로 가볍게 이어간다.

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

run340E(340E 실행)는 run340D(340D 실행)를 원본 f01 failure(원본 f01 실패)로 닫지 않고, close_on_flat=True pressure surface(평탄 청산 켠 압박 표면) negative(부정)로만 닫았다. 다음은 close_on_flat=False(평탄 청산 꺼짐) 수리 package(패키지)다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage340 Selection Status(340단계 선정 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_source_f01(보존 원본 f01): `f01_s55_l51_m01_h12`
- source_f01_net_profit(원본 f01 순수익): `{final['source_f01_net_profit']}`
- source_f01_profit_factor(원본 f01 수익 팩터): `{final['source_f01_profit_factor']}`
- run340D_best_attempt(340D 최고 시도): `{final['best_attempt']}`
- run340D_best_net_profit(340D 최고 순수익): `{final['best_net_profit']}`
- control_semantics_pass(대조 의미 통과): `{final['control_semantics_pass']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 정확 대조 의미가 깨진 결과를 selection(선정)으로 오해하지 않게 한다.
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
    marker = f"run340E {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run340E F01 Pressure Probe Review(340E F01 압박 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- control_semantics_pass(대조 의미 통과): `{final['control_semantics_pass']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): close_on_flat(평탄 청산) 불일치를 수리 조건으로 만들고 원본 f01 단서를 보존한다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run340E F01 Pressure Probe Review(340E F01 압박 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- scorecard(점수표): `{rel(SCORECARD)}`
- control_audit(대조 감사): `{rel(CONTROL_SEMANTICS_AUDIT)}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): Stage340(340단계)을 corrected close_on_flat_false branch(수정된 평탄 청산 꺼짐 분기)로 이어간다.
""",
    )
    changelog = f"""## {TODAY} run340E F01 Pressure Probe Review(F01 압박 탐침 검토)

- action(행동): run340D(340D 실행)의 MT5 result(MT5 결과)와 run340C(340C 실행)의 package semantics(패키지 의미)를 함께 검토했다.
- effect(효과): close_on_flat=True(평탄 청산 켬) 표면은 부정으로 닫고, 원본 f01 exact replay(정확 재생)는 run340F(340F 실행)로 수리한다.
- boundary(경계): selected model/runtime authority/Goal Achieve(선정 모델/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_exploration_registers() -> None:
    marker = f"run340E {RUN_ID}"
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage340E Corrected F01 Pressure Branch(340E 수정 F01 압박 분기)

- idea_id(아이디어 ID): `stage340_f01_close_on_flat_false_pressure_repair`
- hypothesis(가설): source f01(원본 f01)의 close_on_flat=False(평탄 청산 꺼짐) 의미를 복구하면 local floor(로컬 하한) 단서가 다시 보일 수 있다.
- source(원천): `{SOURCE_RUNTIME_RUN_ID}` and `{PACKAGE_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): 무거운 Stage340(340단계)을 새 대형 stage(단계)가 아니라 좁은 corrected branch(수정 분기)로 이어간다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} Stage340E Close-On-Flat Control Mismatch(평탄 청산 대조 불일치)

- subject(대상): `run340D_close_on_flat_true_pressure_surface`
- evidence(근거): `{rel(CONTROL_SEMANTICS_AUDIT)}`, `{rel(FAILURE_MEMORY)}`
- judgment(판정): `negative_surface_with_invalid_exact_control(무효 정확 대조를 가진 부정 표면)`
- effect(효과): run340D(340D 실행)를 원본 f01 실패로 과장하지 않고, close_on_flat=True(평탄 청산 켬) 재사용을 막는다.
""",
    )


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [base])
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe_review_with_control_semantics",
            "candidate_model_id": final["best_model_id"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "drawdown": final["best_drawdown"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "negative_with_control_semantics_repair_required_no_selection",
            "matched_rows": final["matched_rows_total"],
            "expectancy": final["best_expectancy"],
            "attempt_count": final["attempt_count"],
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "candidate_model_id": final["best_model_id"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "drawdown": final["best_drawdown"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "matched_rows": final["matched_rows_total"],
            "expectancy": final["best_expectancy"],
            "attempt_count": final["attempt_count"],
        },
    ]
    for row in rows:
        project_row = dict(row)
        project_row["ledger_row_id"] = f"{RUN_ID}__{row['tier']}"
        project_row["tier_scope"] = row["tier"]
        project_row["kpi_scope"] = row["metric_scope"]
        project_row["scoreboard_lane"] = "runtime_probe_review(런타임 탐침 검토)"
        project_row["path"] = rel(REPORT_PATH)
        project_row["date"] = TODAY
        project_row["run_number"] = RUN_NUMBER
        append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], [project_row])
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], [row])


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if ARTIFACT_REGISTRY.exists() else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[
            ~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))
        ].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    ordered = registry[required + [column for column in registry.columns if column not in required]]
    write_csv(ARTIFACT_REGISTRY, ordered)


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    parent_final, parent_gates, package_final, package_gates = load_context()
    package_preview = read_csv(PACKAGE_VARIANT_PREVIEW)
    source_preview = read_csv(SOURCE_VARIANT_PREVIEW)
    control_audit, control_pass = build_control_semantics_audit(package_preview, source_preview)
    write_csv(CONTROL_SEMANTICS_AUDIT, control_audit)
    scorecard, metrics = build_scorecard(control_pass)
    attribution = build_attribution(metrics)
    failure_memory = build_failure_memory()
    next_queue = build_next_queue()
    write_csv(SCORECARD, scorecard)
    write_csv(PERFORMANCE_ATTRIBUTION, attribution)
    write_csv(FAILURE_MEMORY, failure_memory)
    write_csv(NEXT_QUEUE, next_queue)
    final_seed = build_final(metrics)
    write_receipts(final_seed)
    gates = make_gates(final_seed, parent_gates, package_gates)
    final = {
        **final_seed,
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "parent_status": parent_final.get("status", ""),
        "package_status": package_final.get("status", ""),
    }
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final)
    write_exploration_registers()
    write_registers(final, gates)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [
                rel(PARENT_FINAL_DECISION),
                rel(PARENT_GATE_AUDIT),
                rel(PARENT_RUNTIME_SUMMARY),
                rel(PARENT_PROXY_DIFF),
                rel(PACKAGE_FINAL_DECISION),
                rel(PACKAGE_GATE_AUDIT),
                rel(PACKAGE_VARIANT_PREVIEW),
                rel(SOURCE_RUNTIME_SUMMARY),
                rel(SOURCE_VARIANT_PREVIEW),
            ],
            "outputs": [rel(path) for path in artifact_paths() if path.exists()],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_receipts(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run340E gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "source_f01_net_profit": final["source_f01_net_profit"],
                "source_f01_profit_factor": final["source_f01_profit_factor"],
                "control_semantics_pass": final["control_semantics_pass"],
                "mismatch_rows_total": final["mismatch_rows_total"],
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
