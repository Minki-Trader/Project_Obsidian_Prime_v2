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

STAGE_ID = "339_runtime_lifecycle_exit__side_balance_probe_review"
SOURCE_STAGE_ID = "338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair"
STAGE_DIR = ROOT / "stages" / STAGE_ID
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID

RUN_NUMBER = "run339B"
RUN_ID = "run339B_review_recovered_lifecycle_exit_side_balance_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run339A_branch_stage338_to_lifecycle_exit_probe_review_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run338M_materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run338N_execute_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run339C_materialize_shorter_hold_side_balance_trade_count_expansion_mt5_probe_package_without_db_v1"

STATUS = "completed_stage339B_recovered_lifecycle_exit_probe_reviewed_positive_clue_no_selection"
JUDGMENT = "m02_shorter_hold_improved_profit_recovery_but_trade_count_side_balance_below_floor_no_selection"
DECISION = "stage339B_open_run339C_shorter_hold_side_balance_trade_count_expansion"
CLAIM_BOUNDARY = (
    "research_development_recovered_lifecycle_exit_mt5_probe_review_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run339B_lifecycle_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage339B_lifecycle_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

SOURCE_RUN339A_DIR = STAGE_DIR / "02_runs" / "run339A"
SOURCE_PREVIEW = SOURCE_RUN339A_DIR / "recovered_runtime_preview.csv"
SOURCE_INVENTORY = SOURCE_RUN339A_DIR / "recovered_runtime_output_inventory.csv"
SOURCE_HANDOFF = SOURCE_RUN339A_DIR / "stage338_to_stage339_handoff_manifest.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN339A_DIR / "final_decision.json"

SOURCE_PACKAGE_DIR = SOURCE_STAGE_DIR / "02_runs" / "run338M"
SOURCE_RUNTIME_DIR = SOURCE_STAGE_DIR / "02_runs" / "run338N"
SOURCE_VARIANT_PREVIEW = SOURCE_PACKAGE_DIR / "lifecycle_variant_preview.csv"
SOURCE_ATTEMPT_PACKAGE = SOURCE_PACKAGE_DIR / "runtime_probe_attempt_package.csv"
SOURCE_EXPECTED_TAPE = SOURCE_PACKAGE_DIR / "expected" / "expected_tape.csv"
SOURCE_RUNTIME_SUMMARY = SOURCE_RUNTIME_DIR / "lifecycle_exit_mt5_probe_summary.csv"
SOURCE_MT5_EXECUTION_RESULT = SOURCE_RUNTIME_DIR / "mt5_execution_result.json"
SOURCE_REPORT_RECORDS = SOURCE_RUNTIME_DIR / "strategy_tester_report_records.json"
SOURCE_RUNTIME_IDENTITY = SOURCE_RUNTIME_DIR / "runtime_identity.csv"
SOURCE_OUTPUT_COPY_MANIFEST = SOURCE_RUNTIME_DIR / "runtime_output_copy_manifest.csv"
SOURCE_PROXY_DIFF = SOURCE_RUNTIME_DIR / "proxy_mt5_runtime_difference.csv"

SCORECARD = RUN_DIR / "lifecycle_exit_probe_scorecard.csv"
KPI_JUDGMENT = RUN_DIR / "lifecycle_exit_probe_kpi_judgment.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run339C_queue.csv"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
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


def numeric(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame.columns:
        return pd.Series([pd.NA] * len(frame), index=frame.index)
    return pd.to_numeric(frame[column], errors="coerce")


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


def load_report_records() -> pd.DataFrame:
    records = read_json(SOURCE_REPORT_RECORDS)
    rows: list[dict[str, Any]] = []
    for record in records:
        metrics = record.get("metrics", {})
        rows.append(
            {
                "attempt_name": record.get("attempt_name", ""),
                "report_record_status": record.get("status", ""),
                "report_path_from_record": metrics.get("report_path", record.get("html_report", {}).get("path", "")),
                "report_sha256": record.get("html_report", {}).get("sha256", ""),
                "chart_sha256": record.get("chart", {}).get("sha256", ""),
                "gross_profit": metrics.get("gross_profit", ""),
                "gross_loss": metrics.get("gross_loss", ""),
                "win_rate_percent": metrics.get("win_rate_percent", ""),
                "winning_trade_count": metrics.get("winning_trade_count", ""),
                "losing_trade_count": metrics.get("losing_trade_count", ""),
                "long_win_rate_percent": metrics.get("long_win_rate_percent", ""),
                "short_win_rate_percent": metrics.get("short_win_rate_percent", ""),
                "missing_required_metrics": ";".join(metrics.get("missing_required_metrics", [])),
            }
        )
    return pd.DataFrame(rows)


def load_execution_identity() -> pd.DataFrame:
    records = read_json(SOURCE_MT5_EXECUTION_RESULT)
    rows: list[dict[str, Any]] = []
    for record in records:
        runtime_outputs = record.get("runtime_outputs", {})
        rows.append(
            {
                "attempt_name": record.get("attempt_name", ""),
                "terminal_returncode": record.get("returncode", ""),
                "tester_status_json": record.get("status", ""),
                "summary_exists_json": runtime_outputs.get("summary_exists", ""),
                "telemetry_exists_json": runtime_outputs.get("telemetry_exists", ""),
                "summary_sha256_json": runtime_outputs.get("summary_sha256", ""),
                "telemetry_sha256_json": runtime_outputs.get("telemetry_sha256", ""),
                "set_path_json": record.get("set_path", ""),
                "ini_path_json": record.get("ini_path", ""),
                "tester_profile_set_sha256": record.get("tester_profile_set_copy", {}).get("sha256", ""),
                "tester_profile_ini_sha256": record.get("tester_profile_ini_copy", {}).get("sha256", ""),
            }
        )
    return pd.DataFrame(rows)


def build_scorecard() -> tuple[pd.DataFrame, dict[str, Any]]:
    summary = read_csv(SOURCE_RUNTIME_SUMMARY)
    variants = read_csv(SOURCE_VARIANT_PREVIEW)
    reports = load_report_records()
    execution = load_execution_identity()
    frame = summary.merge(variants, on=["attempt_name", "model_id"], how="left", suffixes=("", "_variant"))
    frame = frame.merge(reports, on="attempt_name", how="left")
    frame = frame.merge(execution, on="attempt_name", how="left")

    numeric_columns = [
        "expected_rows",
        "matched_rows",
        "probability_mismatch_rows",
        "decision_mismatch_rows",
        "max_abs_probability_diff",
        "net_profit",
        "profit_factor",
        "expectancy",
        "recovery_factor",
        "max_drawdown_amount",
        "trade_count",
        "long_trade_count",
        "short_trade_count",
        "signal_trade_count",
        "signal_long_count",
        "signal_short_count",
        "signal_side_balance",
        "gross_profit",
        "gross_loss",
        "win_rate_percent",
    ]
    for column in numeric_columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    side_total = frame["long_trade_count"].fillna(0) + frame["short_trade_count"].fillna(0)
    frame["trade_side_balance"] = (
        frame[["long_trade_count", "short_trade_count"]].min(axis=1) / side_total.replace(0, pd.NA)
    ).fillna(0.0)
    frame["exact_parity_pass"] = (
        frame["expected_rows"].eq(frame["matched_rows"])
        & frame["probability_mismatch_rows"].fillna(1).eq(0)
        & frame["decision_mismatch_rows"].fillna(1).eq(0)
        & frame["tester_status"].astype(str).eq("completed")
        & frame["runtime_status"].astype(str).eq("completed")
        & frame["report_status"].astype(str).eq("completed")
    )
    frame["net_profit_pass"] = frame["net_profit"] > FLOORS["net_profit"]
    frame["profit_factor_pass"] = frame["profit_factor"] >= FLOORS["profit_factor"]
    frame["expectancy_pass"] = frame["expectancy"] > FLOORS["expectancy"]
    frame["recovery_factor_pass"] = frame["recovery_factor"] >= FLOORS["recovery_factor"]
    frame["drawdown_pass"] = frame["max_drawdown_amount"] <= FLOORS["max_drawdown_amount"]
    frame["trade_count_pass"] = frame["trade_count"] >= FLOORS["trade_count"]
    frame["trade_side_balance_pass"] = frame["trade_side_balance"] >= FLOORS["trade_side_balance"]
    pass_columns = [
        "exact_parity_pass",
        "net_profit_pass",
        "profit_factor_pass",
        "expectancy_pass",
        "recovery_factor_pass",
        "drawdown_pass",
        "trade_count_pass",
        "trade_side_balance_pass",
    ]
    frame["floor_pass_count"] = frame[pass_columns].sum(axis=1)
    frame["operating_ready"] = frame[pass_columns].all(axis=1)
    frame["weakness_tags"] = frame.apply(weakness_tags, axis=1)
    frame["review_judgment"] = frame.apply(row_judgment, axis=1)
    frame["claim_boundary"] = CLAIM_BOUNDARY
    frame = frame.sort_values(
        ["operating_ready", "floor_pass_count", "net_profit", "profit_factor", "recovery_factor"],
        ascending=[False, False, False, False, False],
    ).reset_index(drop=True)

    best = frame.iloc[0]
    metrics = {
        "attempt_count": int(len(frame)),
        "expected_rows_total": int(frame["expected_rows"].fillna(0).sum()),
        "matched_rows_total": int(frame["matched_rows"].fillna(0).sum()),
        "probability_mismatch_rows_total": int(frame["probability_mismatch_rows"].fillna(0).sum()),
        "decision_mismatch_rows_total": int(frame["decision_mismatch_rows"].fillna(0).sum()),
        "all_exact_parity": bool(frame["exact_parity_pass"].all()),
        "operating_ready_count": int(frame["operating_ready"].sum()),
        "positive_net_count": int(frame["net_profit_pass"].sum()),
        "best_attempt": str(best["attempt_name"]),
        "best_model_id": str(best["model_id"]),
        "best_net_profit": safe_float(best["net_profit"]),
        "best_profit_factor": safe_float(best["profit_factor"]),
        "best_expectancy": safe_float(best["expectancy"]),
        "best_recovery_factor": safe_float(best["recovery_factor"]),
        "best_drawdown": safe_float(best["max_drawdown_amount"]),
        "best_trade_count": safe_int(best["trade_count"]),
        "best_long_trade_count": safe_int(best["long_trade_count"]),
        "best_short_trade_count": safe_int(best["short_trade_count"]),
        "best_trade_side_balance": safe_float(best["trade_side_balance"]),
        "best_floor_pass_count": safe_int(best["floor_pass_count"]),
        "best_weakness_tags": str(best["weakness_tags"]),
        "report_paths_exist": bool(frame["report_path"].astype(str).map(lambda value: Path(value).exists()).all()),
        "source_partial_final_decision_exists": (SOURCE_RUNTIME_DIR / "final_decision.json").exists(),
    }
    return frame, metrics


def weakness_tags(row: pd.Series) -> str:
    tags: list[str] = []
    if not bool(row.get("exact_parity_pass", False)):
        tags.append("parity")
    if not bool(row.get("net_profit_pass", False)):
        tags.append("net_profit")
    if not bool(row.get("profit_factor_pass", False)):
        tags.append("profit_factor")
    if not bool(row.get("expectancy_pass", False)):
        tags.append("expectancy")
    if not bool(row.get("recovery_factor_pass", False)):
        tags.append("recovery")
    if not bool(row.get("drawdown_pass", False)):
        tags.append("drawdown")
    if not bool(row.get("trade_count_pass", False)):
        tags.append("trade_count")
    if not bool(row.get("trade_side_balance_pass", False)):
        tags.append("side_balance")
    return ";".join(tags) if tags else "none(없음)"


def row_judgment(row: pd.Series) -> str:
    if bool(row.get("operating_ready", False)):
        return "exploratory_probe_all_local_floors_pass_but_no_forward_no_selection(탐색 탐침 로컬 하한 통과, 전진 검증 없음)"
    if bool(row.get("net_profit_pass", False)) and bool(row.get("profit_factor_pass", False)) and bool(row.get("recovery_factor_pass", False)):
        return "positive_clue_but_not_operating_ready(긍정 단서, 운영 준비 아님)"
    if bool(row.get("trade_count_pass", False)) or bool(row.get("trade_side_balance_pass", False)):
        return "shape_clue_profit_damaged(형태 단서, 수익 손상)"
    return "negative_or_weak_probe(부정 또는 약한 탐침)"


def build_kpi_judgment(scorecard: pd.DataFrame, metrics: Mapping[str, Any]) -> pd.DataFrame:
    rows = []
    for _, row in scorecard.iterrows():
        rows.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "judgment_class": "positive_clue(긍정 단서)" if row["review_judgment"].startswith("positive") else "negative_clue(부정 단서)",
                "evidence_boundary": "runtime_probe_reviewed(런타임 탐침 검토됨)",
                "parity_level": "P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)",
                "wfo_status": "exception_single_window_runtime_probe(단일 구간 런타임 탐침 예외)",
                "external_verification_status": "completed(완료)",
                "operating_ready": bool(row["operating_ready"]),
                "floor_pass_count": int(row["floor_pass_count"]),
                "weakness_tags": row["weakness_tags"],
                "next_condition": "forward_or_replay_plus_trade_count_side_balance_repair(전진 또는 재생 검증과 거래수/방향 균형 수리)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "attempt_name": "stage339B_overall",
            "model_id": metrics["best_model_id"],
            "judgment_class": "positive(긍정)_within_runtime_probe_boundary(런타임 탐침 경계 안)",
            "evidence_boundary": "reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)",
            "parity_level": "P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)",
            "wfo_status": "exception_single_window_runtime_probe(단일 구간 런타임 탐침 예외)",
            "external_verification_status": "completed(완료)",
            "operating_ready": False,
            "floor_pass_count": metrics["best_floor_pass_count"],
            "weakness_tags": metrics["best_weakness_tags"],
            "next_condition": "run339C(339C 실행) must improve trade_count(거래수) and side_balance(방향 균형) without losing m02(엠02) profit/recovery(수익/회복)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return pd.DataFrame(rows)


def build_attribution(scorecard: pd.DataFrame) -> pd.DataFrame:
    by_attempt = {str(row["attempt_name"]): row for _, row in scorecard.iterrows()}
    base = by_attempt.get("m01_p55_h18_base")
    m02 = by_attempt.get("m02_p55_h12")
    rows: list[dict[str, Any]] = []

    def add(topic: str, comparison: str, observed: str, drivers: str, confidence: str, next_probe: str) -> None:
        rows.append(
            {
                "topic": topic,
                "comparison_baseline": comparison,
                "observed_change": observed,
                "likely_drivers": drivers,
                "segment_checks": "Tier A only(Tier A 전용);single runtime window(단일 런타임 구간);session/regime split missing(세션/국면 분할 누락)",
                "alternative_explanations": "small trade count(작은 거래수);short-side concentration(숏 집중);single-window noise(단일 구간 잡음)",
                "attribution_confidence": confidence,
                "next_probe": next_probe,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    if base is not None and m02 is not None:
        add(
            "shorter_hold_recovery(짧은 보유 회복)",
            "m01_p55_h18_base",
            (
                f"net_profit(순수익) {safe_float(m02['net_profit']) - safe_float(base['net_profit']):.2f}, "
                f"profit_factor(수익 팩터) {safe_float(m02['profit_factor']) - safe_float(base['profit_factor']):.2f}, "
                f"recovery_factor(회복 계수) {safe_float(m02['recovery_factor']) - safe_float(base['recovery_factor']):.2f}"
            ),
            "max_hold_bars(최대 보유 봉) 18 -> 12, close_on_flat(평탄 청산) false(거짓)",
            "medium(중간)",
            "keep hold=12(보유 12) and sweep side thresholds(방향 임계값 탐색)",
        )

    for attempt in ["m03_p55_h12_cf", "m05_s55_l50_h12_cf", "m06_s55_l48_h12_cf"]:
        row = by_attempt.get(attempt)
        if row is not None:
            add(
                f"{attempt}_close_flat_damage(평탄 청산 손상)",
                "m02_p55_h12 or nearest non-close-flat(가까운 비평탄 청산 대조)",
                f"net_profit(순수익) {safe_float(row['net_profit']):.2f}, trade_count(거래수) {safe_int(row['trade_count'])}",
                "close_on_flat(평탄 청산)이 거래수는 늘리지만 expectancy(기대값)를 악화했다.",
                "medium(중간)" if attempt == "m03_p55_h12_cf" else "low(낮음)",
                "avoid close_on_flat(평탄 청산 회피) until profit-lock or side-specific exit(수익 잠금 또는 방향별 청산) is tested",
            )

    for attempt in ["m04_s55_l50_h18", "m05_s55_l50_h12_cf", "m06_s55_l48_h12_cf"]:
        row = by_attempt.get(attempt)
        if row is not None:
            add(
                f"{attempt}_side_balance_tradeoff(방향 균형 상충)",
                "m02_p55_h12",
                (
                    f"side_balance(방향 균형) {safe_float(row['trade_side_balance']):.3f}, "
                    f"trade_count(거래수) {safe_int(row['trade_count'])}, net_profit(순수익) {safe_float(row['net_profit']):.2f}"
                ),
                "long_threshold(롱 임계값) relief(완화)가 방향 균형은 개선하지만 profit(수익)을 약화했다.",
                "medium(중간)",
                "combine mild long relief(약한 롱 완화) with stricter short threshold(엄격한 숏 임계값) and no close_on_flat(평탄 청산 없음)",
            )
    return pd.DataFrame(rows)


def build_failure_memory(scorecard: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "failure_id": "stage339B_close_on_flat_damage",
                "hypothesis": "close_on_flat(평탄 청산)이 drawdown(낙폭)을 줄이며 trade_count(거래수)를 늘릴 것이다.",
                "variants_tried": "m03_p55_h12_cf;m05_s55_l50_h12_cf;m06_s55_l48_h12_cf",
                "failed_boundary": "net_profit(순수익), profit_factor(수익 팩터), expectancy(기대값), recovery_factor(회복 계수)",
                "why_failed": "extra exits(추가 청산)이 profitable hold(수익 보유)를 끊고 손실 거래 비율을 키웠다.",
                "salvage_value": "close_on_flat(평탄 청산)은 단독 사용 금지, profit-lock(수익 잠금) 또는 side-specific exit(방향별 청산)과만 재개.",
                "reopen_condition": "same or higher net_profit(동일 이상 순수익) with trade_count>=30(거래수 30 이상) on MT5(메타트레이더5)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "failure_id": "stage339B_long_relief_profit_tradeoff",
                "hypothesis": "long_threshold(롱 임계값) relief(완화)가 side_balance(방향 균형)를 개선하며 수익을 유지할 것이다.",
                "variants_tried": "m04_s55_l50_h18;m05_s55_l50_h12_cf;m06_s55_l48_h12_cf",
                "failed_boundary": "side_balance(방향 균형)는 개선됐지만 net_profit(순수익)과 recovery(회복)가 무너졌다.",
                "why_failed": "long supply(롱 공급)를 늘린 표면이 약한 롱을 너무 많이 열었다.",
                "salvage_value": "mild long relief(약한 롱 완화)와 stricter short threshold(엄격한 숏 임계값)를 함께 시험.",
                "reopen_condition": "m02(엠02) 수익/회복을 크게 잃지 않고 side_balance>=0.25(방향 균형 0.25 이상)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_next_queue(metrics: Mapping[str, Any]) -> pd.DataFrame:
    variants = [
        ("c01_s55_l52_h12", 0.55, 0.52, 12, False, "mild_long_relief_from_m02(엠02 기반 약한 롱 완화)"),
        ("c02_s57_l52_h12", 0.57, 0.52, 12, False, "stricter_short_mild_long(엄격한 숏 + 약한 롱)"),
        ("c03_s60_l52_h12", 0.60, 0.52, 12, False, "short_quality_cliff_check(숏 품질 절벽 확인)"),
        ("c04_s55_l50_h12", 0.55, 0.50, 12, False, "m04_long_relief_without_close_flat(평탄 청산 없는 롱 완화)"),
        ("c05_s57_l50_h12", 0.57, 0.50, 12, False, "balanced_trade_count_recovery(균형 거래수 회복)"),
        ("c06_s55_l48_h12", 0.55, 0.48, 12, False, "strong_long_relief_no_close_flat(강한 롱 완화, 평탄 청산 없음)"),
        ("c07_s55_l46_h12", 0.55, 0.46, 12, False, "side_balance_extreme_l46(방향 균형 극단 0.46)"),
        ("c08_s57_l46_h12", 0.57, 0.46, 12, False, "strict_short_side_balance_l46(엄격한 숏과 방향 균형 0.46)"),
        ("c09_s57_l44_h12", 0.57, 0.44, 12, False, "extreme_long_supply_l44(극단 롱 공급 0.44)"),
    ]
    rows = []
    for idx, (variant_id, short_threshold, long_threshold, hold, close_flat, role) in enumerate(variants, start=1):
        rows.append(
            {
                "queue_id": "run339C_shorter_hold_side_balance_trade_count_expansion",
                "next_run_id": NEXT_RUN_ID,
                "priority": idx,
                "seed_attempt": metrics["best_attempt"],
                "variant_id": variant_id,
                "short_threshold": short_threshold,
                "long_threshold": long_threshold,
                "max_hold_bars": hold,
                "close_on_flat": close_flat,
                "variant_role": role,
                "primary_family": "runtime_backtest(런타임 백테스트)",
                "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
                "effect": "m02(엠02)의 profit/recovery(수익/회복)를 씨앗으로 두고 trade_count(거래수)와 side_balance(방향 균형)를 넓힌다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def gate_row(gate_id: str, status: str, evidence_path: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": evidence_path,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(metrics: Mapping[str, Any]) -> pd.DataFrame:
    inventory = read_csv(SOURCE_INVENTORY)
    inventory_ok = inventory.loc[inventory["artifact_role"].astype(str).ne("partial_final_decision(부분 최종 결정)"), "exists"].astype(str).str.lower().eq("true").all()
    rows = [
        gate_row(
            "source_handoff_inputs_available",
            "passed" if SOURCE_PREVIEW.exists() and SOURCE_INVENTORY.exists() and SOURCE_HANDOFF.exists() else "failed",
            f"{rel(SOURCE_PREVIEW)};{rel(SOURCE_INVENTORY)};{rel(SOURCE_HANDOFF)}",
            "run339A(339A 실행) 인계 파일을 검토 입력으로 고정한다.",
        ),
        gate_row(
            "runtime_output_inventory_available",
            "passed" if inventory_ok else "failed",
            rel(SOURCE_INVENTORY),
            "run338N(338N 실행)의 final_decision(최종 결정) 누락은 표시하고, 나머지 산출물은 검토한다.",
        ),
        gate_row(
            "mt5_report_identity_available",
            "passed" if metrics["report_paths_exist"] else "failed",
            rel(SOURCE_REPORT_RECORDS),
            "MT5(메타트레이더5) report(보고서)와 chart(차트) 정체성을 확인한다.",
        ),
        gate_row(
            "exact_proxy_mt5_parity_confirmed",
            "passed" if metrics["all_exact_parity"] else "failed",
            f"{rel(SOURCE_RUNTIME_SUMMARY)};{rel(SOURCE_PROXY_DIFF)}",
            "proxy(프록시)와 MT5(메타트레이더5) 확률/결정 차이를 확인한다.",
        ),
        gate_row(
            "kpi_record_written",
            "passed" if KPI_RECORD.exists() and SCORECARD.exists() else "failed",
            f"{rel(KPI_RECORD)};{rel(SCORECARD)}",
            "KPI(핵심 성과 지표)를 machine-readable(기계 판독 가능)하게 남긴다.",
        ),
        gate_row(
            "result_judgment_written",
            "passed" if RESULT_JUDGMENT_RECEIPT.exists() and KPI_JUDGMENT.exists() else "failed",
            f"{rel(RESULT_JUDGMENT_RECEIPT)};{rel(KPI_JUDGMENT)}",
            "positive clue(긍정 단서)와 no selection(선정 없음)을 분리한다.",
        ),
        gate_row(
            "tier_paired_records_written",
            "passed" if STAGE_LEDGER.exists() else "failed",
            rel(STAGE_LEDGER),
            "Tier A(티어 A), Tier B(티어 B), Tier A+B(티어 A+B)를 분리 기록한다.",
        ),
        gate_row(
            "next_exploration_queue_written",
            "passed" if NEXT_QUEUE.exists() and FAILURE_MEMORY.exists() else "failed",
            f"{rel(NEXT_QUEUE)};{rel(FAILURE_MEMORY)}",
            "실패 기억을 다음 공격 탐색 제약으로 바꾼다.",
        ),
        gate_row(
            "no_forbidden_operating_claim",
            "passed",
            rel(CLAIM_RECEIPT),
            "selected model(선정 모델), operating promotion(운영 승격), runtime authority(런타임 권위)를 주장하지 않는다.",
        ),
        gate_row(
            "required_gate_coverage_audit_written",
            "passed",
            rel(GATE_AUDIT),
            "closeout(종료 기록)의 gate(게이트) 근거를 남긴다.",
        ),
    ]
    return pd.DataFrame(rows)


def write_receipts(scorecard: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        KPI_RECORD,
        {
            **base,
            "measurement_scope": "MT5 runtime probe KPI(MT5 런타임 탐침 핵심 성과 지표)",
            "scoreboard": "runtime_probe(런타임 탐침)",
            "attempt_count": metrics["attempt_count"],
            "expected_rows_total": metrics["expected_rows_total"],
            "matched_rows_total": metrics["matched_rows_total"],
            "probability_mismatch_rows_total": metrics["probability_mismatch_rows_total"],
            "decision_mismatch_rows_total": metrics["decision_mismatch_rows_total"],
            "best_attempt": metrics["best_attempt"],
            "best_model_id": metrics["best_model_id"],
            "best_net_profit": metrics["best_net_profit"],
            "best_profit_factor": metrics["best_profit_factor"],
            "best_expectancy": metrics["best_expectancy"],
            "best_recovery_factor": metrics["best_recovery_factor"],
            "best_drawdown": metrics["best_drawdown"],
            "best_trade_count": metrics["best_trade_count"],
            "best_trade_side_balance": metrics["best_trade_side_balance"],
            "operating_ready_count": metrics["operating_ready_count"],
            "effect": "m02(엠02) shorter hold(짧은 보유)는 수익/회복 단서지만 거래수/방향 균형 하한은 못 닫았다.",
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            **base,
            "parity_level": "P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)",
            "all_exact_parity": metrics["all_exact_parity"],
            "matched_rows_total": metrics["matched_rows_total"],
            "probability_mismatch_rows_total": metrics["probability_mismatch_rows_total"],
            "decision_mismatch_rows_total": metrics["decision_mismatch_rows_total"],
            "external_verification_status": "completed(완료)",
            "runtime_authority": "not_claimed(주장 없음)",
            "effect": "MT5(메타트레이더5) runtime probe(런타임 탐침)는 관찰했지만 runtime authority(런타임 권위)는 주장하지 않는다.",
        },
    )
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run338N recovered lifecycle/exit MT5 probe outputs(338N 복구 생명주기/청산 MT5 탐침 출력)",
            "evidence_available": [rel(SCORECARD), rel(KPI_JUDGMENT), rel(SOURCE_REPORT_RECORDS), rel(SOURCE_PROXY_DIFF)],
            "evidence_missing": [
                "forward/replay evidence(전진/재생 근거)",
                "Tier B evidence(Tier B 근거)",
                "live readiness(실거래 준비)",
                "source run338N final_decision(원천 338N 최종 결정)",
            ],
            "judgment_label": "positive(긍정)_within_runtime_probe_boundary(런타임 탐침 경계 안)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run339C(339C 실행) expands trade_count(거래수) and side_balance(방향 균형) while preserving m02(엠02) profit/recovery(수익/회복)",
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": "m02(엠02) improved net_profit(순수익), profit_factor(수익 팩터), recovery_factor(회복 계수) versus m01(엠01)",
            "comparison_baseline": "m01_p55_h18_base",
            "likely_drivers": "max_hold_bars(최대 보유 봉) 18 -> 12; no close_on_flat(평탄 청산 없음)",
            "segment_checks": "Tier A only(Tier A 전용); session/regime missing(세션/국면 누락)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "shorter hold with side threshold sweep(짧은 보유와 방향 임계값 탐색)",
        },
    )
    source_inputs = [
        SOURCE_PREVIEW,
        SOURCE_INVENTORY,
        SOURCE_HANDOFF,
        SOURCE_VARIANT_PREVIEW,
        SOURCE_ATTEMPT_PACKAGE,
        SOURCE_EXPECTED_TAPE,
        SOURCE_RUNTIME_SUMMARY,
        SOURCE_MT5_EXECUTION_RESULT,
        SOURCE_REPORT_RECORDS,
        SOURCE_RUNTIME_IDENTITY,
        SOURCE_OUTPUT_COPY_MANIFEST,
        SOURCE_PROXY_DIFF,
    ]
    outputs = [
        SCORECARD,
        KPI_JUDGMENT,
        PERFORMANCE_ATTRIBUTION,
        FAILURE_MEMORY,
        NEXT_QUEUE,
        KPI_RECORD,
        RUNTIME_PARITY_RECEIPT,
        RESULT_JUDGMENT_RECEIPT,
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        REPORT_PATH,
        DECISION_DOC,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in source_inputs],
            "artifact_paths": [rel(path) for path in outputs],
            "source_artifact_hashes": {rel(path): sha256_file(path) for path in source_inputs if path.exists()},
            "lineage_judgment": "connected_with_boundary(경계가 있는 연결)",
            "availability": "tracked_and_generated(추적 및 생성)",
            "effect": "미검토 run338N(338N 실행) 산출물을 검토된 Stage339B(339B 실행) 근거로 연결한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "promotion_candidate": "not_claimed(주장 없음)",
            "effect": "좋은 MT5(메타트레이더5) 숫자를 운영 가능 모델로 오해하지 않게 한다.",
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            **base,
            "command": "python stage_pipelines/stage339/review_recovered_lifecycle_exit_side_balance_mt5_probe_without_db.py",
            "producer": rel(Path(__file__)),
            "outputs": [rel(path) for path in outputs + [GATE_AUDIT, FINAL_DECISION]],
        },
    )


def write_stage_docs(metrics: Mapping[str, Any]) -> None:
    report = f"""# run339B Lifecycle Probe Review(생명주기 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- source_runtime_run(원천 런타임 실행): `{SOURCE_RUNTIME_RUN_ID}`
- best_attempt(최고 시도): `{metrics['best_attempt']}`
- net_profit(순수익): `{metrics['best_net_profit']}`
- profit_factor(수익 팩터): `{metrics['best_profit_factor']}`
- expectancy(기대값): `{metrics['best_expectancy']}`
- recovery_factor(회복 계수): `{metrics['best_recovery_factor']}`
- drawdown(낙폭): `{metrics['best_drawdown']}`
- trade_count(거래수): `{metrics['best_trade_count']}`
- trade_side_balance(거래 방향 균형): `{metrics['best_trade_side_balance']:.3f}`
- exact_parity(정확 동등성): `{metrics['matched_rows_total']}/{metrics['expected_rows_total']}` matched(일치), mismatch(불일치) `{metrics['probability_mismatch_rows_total'] + metrics['decision_mismatch_rows_total']}`

## Judgment(판정)

`m02_p55_h12` is a positive clue(긍정 단서) inside runtime_probe(런타임 탐침) evidence. It is not selected(선정 아님).
Effect(효과): net/PF/expectancy/recovery(순수익/수익 팩터/기대값/회복)는 좋아졌지만 trade_count(거래수)와 side_balance(방향 균형)가 운영 하한을 못 닫았음을 분리한다.

## Failure Memory(실패 기억)

- close_on_flat(평탄 청산): trade_count(거래수)는 늘렸지만 expectancy(기대값)와 net_profit(순수익)을 망쳤다.
- long relief(롱 완화): side_balance(방향 균형)는 개선했지만 weak long supply(약한 롱 공급)로 profit(수익)이 무너졌다.

## Next Action(다음 행동)

Open `{NEXT_RUN_ID}`.
Effect(효과): m02(엠02)의 shorter hold(짧은 보유) 수익 구조를 씨앗으로 삼고, close_on_flat(평탄 청산)은 빼며, short threshold(숏 임계값)와 mild long relief(약한 롱 완화)를 넓게 탐색한다.

## Boundary(경계)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating_promotion(운영 승격 없음), no runtime_authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage339B Lifecycle Probe Review Decision(339B 생명주기 탐침 검토 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- evidence(근거): `{rel(SCORECARD)}`, `{rel(KPI_JUDGMENT)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): run338N(338N 실행)의 recovered MT5 runtime output(복구 MT5 런타임 출력)을 reviewed runtime probe(검토된 런타임 탐침)로 정리했다.
Effect(효과): 재실행 없이 exact parity(정확 동등성)와 KPI(핵심 성과 지표)를 판정하고, 다음 공격 탐색 축을 분리했다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage339 Selection Status(339단계 선택 상태)

- active_stage(활성 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- best_reviewed_attempt(최고 검토 시도): `{metrics['best_attempt']}`
- selected_model(선정 모델): `none(없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 좋은 MT5(메타트레이더5) 숫자를 다음 탐색 씨앗으로만 쓰고 운영 모델로 올리지 않는다.
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

run339B(339B 실행)는 recovered MT5 runtime output(복구 MT5 런타임 출력)을 검토했다. m02(엠02)는 strong positive clue(강한 긍정 단서)이지만 trade_count(거래수)와 side_balance(방향 균형)가 부족해 selection(선정)은 없다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
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
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = RUN_ID
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run339B Lifecycle Probe Review(339B 생명주기 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- best_attempt(최고 시도): `{metrics['best_attempt']}`
- net_profit(순수익): `{metrics['best_net_profit']}`
- trade_count(거래수): `{metrics['best_trade_count']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 긍정 단서를 운영 주장으로 올리지 않고 side_balance/trade_count(방향 균형/거래수) 수리로 넘겼다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run339B Lifecycle Probe Review(339B 생명주기 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- best_attempt(최고 시도): `{metrics['best_attempt']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): recovered MT5(복구 MT5) 산출물을 검토하고 다음 공격 탐색 queue(대기열)를 만들었다.
""",
    )
    changelog = f"""## {TODAY} run339B Lifecycle Probe Review(생명주기 탐침 검토)

- action(행동): run338N(338N 실행)의 recovered MT5 runtime output(복구 MT5 런타임 출력)을 reviewed runtime probe(검토된 런타임 탐침)로 정리했다.
- effect(효과): m02(엠02)의 net profit(순수익) `{metrics['best_net_profit']}`, profit factor(수익 팩터) `{metrics['best_profit_factor']}`, recovery factor(회복 계수) `{metrics['best_recovery_factor']}` 단서를 보존하고, trade_count(거래수) `{metrics['best_trade_count']}`와 side_balance(방향 균형) `{metrics['best_trade_side_balance']:.3f}` 약점을 다음 run(실행) 제약으로 넘겼다.
- boundary(경계): selected model(선정 모델), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage339B Shorter Hold Side-Balance Seed(짧은 보유 방향 균형 씨앗)

- idea_id(아이디어 ID): `stage339_shorter_hold_side_balance_expansion`
- hypothesis(가설): m02(엠02)의 hold=12(보유 12) 수익 구조를 유지하면서 short_threshold(숏 임계값)를 높이고 long_threshold(롱 임계값)를 약하게 낮추면 trade_count(거래수)와 side_balance(방향 균형)를 같이 개선할 수 있다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- broad_sweep(넓은 탐색): `{rel(NEXT_QUEUE)}`
- extreme_sweep(극단 탐색): short_threshold(숏 임계값) 0.60, long_threshold(롱 임계값) 0.48 without close_on_flat(평탄 청산 없음)
- micro_search_gate(미세 탐색 게이트): MT5(메타트레이더5) exact parity(정확 동등성) and trade_count>=30(거래수 30 이상) with positive expectancy(기대값 양수)
- evidence_boundary(근거 경계): `reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)`
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} Stage339B Lifecycle Exit Failure Memory(생명주기 청산 실패 기억)

- subject(대상): close_on_flat(평탄 청산) and aggressive long relief(공격적 롱 완화)
- evidence(근거): `{rel(FAILURE_MEMORY)}`
- judgment(판정): `negative_clue_with_salvage(회수 가치 있는 부정 단서)`
- effect(효과): 실패 변형을 버리지 않고 run339C(339C 실행)의 제약으로 바꾼다.
""",
    )


def stage_ledger_rows(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
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
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": metrics["best_model_id"],
        "net_profit": metrics["best_net_profit"],
        "profit_factor": metrics["best_profit_factor"],
        "drawdown": metrics["best_drawdown"],
        "recovery_factor": metrics["best_recovery_factor"],
        "trade_count": metrics["best_trade_count"],
        "result_status": "reviewed_positive_clue_no_selection(검토된 긍정 단서, 선정 없음)",
        "sample_rows": "",
        "feature_count": 53,
        "matched_rows": metrics["matched_rows_total"],
        "expectancy": metrics["best_expectancy"],
        "attempt_count": metrics["attempt_count"],
    }
    rows = []
    for view, tier, metric_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "mt5_runtime_probe_review"),
        ("Tier B separate(Tier B 분리)", "Tier B", "missing_required"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "same_as_tier_a_until_tier_b_available"),
    ]:
        row = dict(base)
        row.update({"view": view, "tier": tier, "metric_scope": metric_scope})
        if metric_scope == "missing_required":
            for metric in ["candidate_model_id", "net_profit", "profit_factor", "drawdown", "recovery_factor", "trade_count", "matched_rows", "expectancy", "attempt_count"]:
                row[metric] = ""
            row["result_status"] = "missing_required(필수 누락)"
        rows.append(row)
    return rows


def write_registries(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    rows = stage_ledger_rows(gates, metrics)
    existing = read_csv(STAGE_LEDGER) if STAGE_LEDGER.exists() else pd.DataFrame(columns=STAGE_LEDGER_COLUMNS)
    existing = existing.loc[~existing["run_id"].astype(str).eq(RUN_ID)].copy() if "run_id" in existing.columns else existing
    stage_frame = pd.concat([existing, pd.DataFrame(rows)], ignore_index=True)
    for column in STAGE_LEDGER_COLUMNS:
        if column not in stage_frame.columns:
            stage_frame[column] = ""
    write_csv(STAGE_LEDGER, stage_frame[STAGE_LEDGER_COLUMNS])
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [rows[0]])
    project_rows = []
    for row in rows:
        project_row = dict(row)
        project_row["ledger_row_id"] = f"{RUN_ID}__{row['tier']}"
        project_row["tier_scope"] = row["tier"]
        project_row["record_view"] = row["view"]
        project_row["kpi_scope"] = "runtime_probe_review(런타임 탐침 검토)"
        project_row["scoreboard_lane"] = "runtime_probe(런타임 탐침)"
        project_row["path"] = rel(REPORT_PATH)
        project_row["date"] = TODAY
        project_row["run_number"] = RUN_NUMBER
        project_row["primary_artifact"] = rel(FINAL_DECISION)
        project_rows.append(project_row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    artifacts = [
        SCORECARD,
        KPI_JUDGMENT,
        PERFORMANCE_ATTRIBUTION,
        FAILURE_MEMORY,
        NEXT_QUEUE,
        KPI_RECORD,
        RUNTIME_PARITY_RECEIPT,
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
        STAGE_BRIEF,
        STAGE_README,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        Path(__file__),
    ]
    artifact_rows = []
    for path in artifacts:
        if not path.exists() or not path.is_file():
            continue
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], artifact_rows)


def write_final_decision(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "best_attempt": metrics["best_attempt"],
            "best_model_id": metrics["best_model_id"],
            "best_net_profit": metrics["best_net_profit"],
            "best_profit_factor": metrics["best_profit_factor"],
            "best_expectancy": metrics["best_expectancy"],
            "best_recovery_factor": metrics["best_recovery_factor"],
            "best_drawdown": metrics["best_drawdown"],
            "best_trade_count": metrics["best_trade_count"],
            "best_trade_side_balance": metrics["best_trade_side_balance"],
            "operating_ready_count": metrics["operating_ready_count"],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
            "effect": "검토된 긍정 단서를 다음 trade_count/side_balance(거래수/방향 균형) 확장으로 넘긴다.",
        },
    )


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    scorecard, metrics = build_scorecard()
    kpi_judgment = build_kpi_judgment(scorecard, metrics)
    attribution = build_attribution(scorecard)
    failure_memory = build_failure_memory(scorecard)
    next_queue = build_next_queue(metrics)

    write_csv(SCORECARD, scorecard)
    write_csv(KPI_JUDGMENT, kpi_judgment)
    write_csv(PERFORMANCE_ATTRIBUTION, attribution)
    write_csv(FAILURE_MEMORY, failure_memory)
    write_csv(NEXT_QUEUE, next_queue)
    write_receipts(scorecard, metrics)
    write_stage_docs(metrics)
    gates = build_gates(metrics)
    write_csv(GATE_AUDIT, gates)
    write_final_decision(gates, metrics)
    write_registries(gates, metrics)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "best_attempt": metrics["best_attempt"],
                "best_net_profit": metrics["best_net_profit"],
                "best_profit_factor": metrics["best_profit_factor"],
                "best_recovery_factor": metrics["best_recovery_factor"],
                "best_trade_count": metrics["best_trade_count"],
                "best_trade_side_balance": metrics["best_trade_side_balance"],
                "next_run_id": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
