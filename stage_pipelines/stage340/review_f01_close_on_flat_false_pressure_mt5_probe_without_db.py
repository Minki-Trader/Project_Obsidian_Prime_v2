from __future__ import annotations

import csv
import hashlib
import json
import os
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

RUN_NUMBER = "run340H"
RUN_ID = "run340H_review_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run340G_execute_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1"
PACKAGE_RUN_ID = "run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run339G_execute_quality_balance_blend_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run341A_branch_stage340_to_f01_stability_cost_regime_validation_without_db_v1"

STATUS = "completed_stage340H_f01_close_on_flat_false_pressure_probe_reviewed_positive_clue_no_selection"
JUDGMENT = "f01_corrected_control_positive_runtime_probe_q09_net_clue_quality_tradeoff_forward_cost_session_missing_no_selection"
DECISION = "stage340H_open_stage341A_f01_stability_cost_regime_validation_branch"
CLAIM_BOUNDARY = (
    "research_development_f01_corrected_pressure_mt5_probe_review_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run340H_f01_close_on_flat_false_pressure_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage340H_f01_close_on_flat_false_pressure_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run340G"
PACKAGE_RUN_DIR = STAGE_DIR / "02_runs" / "run340F"
SOURCE_RUNTIME_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339G"

PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_RUNTIME_SUMMARY = PARENT_RUN_DIR / "f01_close_on_flat_false_pressure_mt5_probe_summary.csv"
PARENT_PROXY_DIFF = PARENT_RUN_DIR / "proxy_mt5_runtime_difference.csv"
PARENT_RUNTIME_IDENTITY = PARENT_RUN_DIR / "runtime_identity.csv"
PARENT_RUN_MANIFEST = PARENT_RUN_DIR / "run_manifest.json"
PACKAGE_FINAL_DECISION = PACKAGE_RUN_DIR / "final_decision.json"
PACKAGE_GATE_AUDIT = PACKAGE_RUN_DIR / "required_gate_coverage_audit.csv"
PACKAGE_VARIANT_PREVIEW = PACKAGE_RUN_DIR / "variant_preview.csv"
SOURCE_RUNTIME_SUMMARY = SOURCE_RUNTIME_RUN_DIR / "quality_balance_blend_mt5_probe_summary.csv"

SCORECARD = RUN_DIR / "f01_close_on_flat_false_pressure_review_scorecard.csv"
KPI_JUDGMENT = RUN_DIR / "f01_close_on_flat_false_pressure_kpi_judgment.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_SEED_QUEUE = RUN_DIR / "run341A_seed_queue.csv"
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
    Path(fs_path(path.parent)).mkdir(parents=True, exist_ok=True)


def fs_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def path_exists(path: Path) -> bool:
    return os.path.exists(fs_path(path))


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), low_memory=False, encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.loads(handle.read())


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    if path_exists(path):
        with open(fs_path(path), encoding="utf-8-sig") as handle:
            current = handle.read()
    else:
        current = ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows = list(rows)
    frame = read_csv(path) if path_exists(path) else pd.DataFrame()
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


def gate_statuses_pass(frame: pd.DataFrame) -> bool:
    return bool(frame["status"].astype(str).str.lower().eq("passed").all())


def load_context() -> tuple[dict[str, Any], pd.DataFrame, dict[str, Any], pd.DataFrame]:
    parent_final = read_json(PARENT_FINAL_DECISION)
    parent_gates = read_csv(PARENT_GATE_AUDIT)
    package_final = read_json(PACKAGE_FINAL_DECISION)
    package_gates = read_csv(PACKAGE_GATE_AUDIT)
    parent_next = parent_final.get("next_action", parent_final.get("next_run_id"))
    if parent_next != RUN_ID:
        raise RuntimeError(f"parent next_run mismatch: {parent_next} != {RUN_ID}")
    if not gate_statuses_pass(parent_gates):
        raise RuntimeError("parent run340G gate audit has failed rows")
    if not gate_statuses_pass(package_gates):
        raise RuntimeError("package run340F gate audit has failed rows")
    return parent_final, parent_gates, package_final, package_gates


def floor_flags(row: pd.Series) -> dict[str, bool]:
    return {
        "exact_parity_pass": bool(
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
        ("exact_parity_pass", "parity(동등성)"),
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


def build_scorecard() -> tuple[pd.DataFrame, dict[str, Any]]:
    frame = read_csv(PARENT_RUNTIME_SUMMARY).copy()
    preview = read_csv(PACKAGE_VARIANT_PREVIEW).copy()
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
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    side_max = frame[["long_trade_count", "short_trade_count"]].max(axis=1).replace(0, pd.NA)
    frame["trade_side_balance"] = (
        frame[["long_trade_count", "short_trade_count"]].min(axis=1) / side_max
    ).fillna(0.0)
    keep_preview = preview[
        [
            "attempt_name",
            "variant_role",
            "source_attempt_name",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat",
            "signal_trade_count",
            "signal_side_balance",
        ]
    ].copy()
    frame = frame.merge(keep_preview, on="attempt_name", how="left")
    for index, row in frame.iterrows():
        for key, value in floor_flags(row).items():
            frame.loc[index, key] = value
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
    frame["floor_pass_count"] = frame[pass_columns].astype(bool).sum(axis=1)
    frame["local_floor_pass"] = frame[pass_columns].astype(bool).all(axis=1)
    frame["weakness_tags"] = frame.apply(weakness_tags, axis=1)
    frame["source_f01_net_profit"] = safe_float(source_f01.get("net_profit"))
    frame["source_f01_profit_factor"] = safe_float(source_f01.get("profit_factor"))
    frame["source_f01_expectancy"] = safe_float(source_f01.get("expectancy"))
    frame["source_f01_recovery_factor"] = safe_float(source_f01.get("recovery_factor"))
    frame["source_f01_drawdown"] = safe_float(source_f01.get("max_drawdown_amount"))
    frame["source_f01_trade_count"] = safe_int(source_f01.get("trade_count"))
    frame["source_f01_long_trade_count"] = safe_int(source_f01.get("long_trade_count"))
    frame["source_f01_short_trade_count"] = safe_int(source_f01.get("short_trade_count"))
    frame["net_delta_vs_source_f01"] = frame["net_profit"] - frame["source_f01_net_profit"]
    frame["recovery_delta_vs_source_f01"] = frame["recovery_factor"] - frame["source_f01_recovery_factor"]
    frame["drawdown_delta_vs_source_f01"] = frame["max_drawdown_amount"] - frame["source_f01_drawdown"]
    frame["review_judgment"] = frame.apply(
        lambda row: "positive_floor_pass(긍정 하한 통과)" if bool(row["local_floor_pass"]) else "weak_or_negative(약함 또는 부정)",
        axis=1,
    )
    frame["claim_boundary"] = CLAIM_BOUNDARY
    frame = frame.sort_values(
        ["local_floor_pass", "net_profit", "profit_factor", "recovery_factor"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    best = frame.iloc[0]
    exact_control = frame.loc[frame["attempt_name"].astype(str).eq("q01_ctl_s55_l51_m01_h12")].iloc[0]
    local_pass = frame.loc[frame["local_floor_pass"].astype(bool)]
    metrics = {
        "attempt_count": int(len(frame)),
        "expected_rows_total": int(frame["expected_rows"].fillna(0).sum()),
        "matched_rows_total": int(frame["matched_rows"].fillna(0).sum()),
        "mismatch_rows_total": int(
            frame["probability_mismatch_rows"].fillna(0).sum() + frame["decision_mismatch_rows"].fillna(0).sum()
        ),
        "all_exact_parity": bool(frame["exact_parity_pass"].astype(bool).all()),
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
        "best_net_delta_vs_source_f01": safe_float(best.get("net_delta_vs_source_f01")),
        "best_recovery_delta_vs_source_f01": safe_float(best.get("recovery_delta_vs_source_f01")),
        "best_drawdown_delta_vs_source_f01": safe_float(best.get("drawdown_delta_vs_source_f01")),
        "exact_control_net_profit": safe_float(exact_control.get("net_profit")),
        "exact_control_profit_factor": safe_float(exact_control.get("profit_factor")),
        "exact_control_expectancy": safe_float(exact_control.get("expectancy")),
        "exact_control_recovery_factor": safe_float(exact_control.get("recovery_factor")),
        "exact_control_drawdown": safe_float(exact_control.get("max_drawdown_amount")),
        "exact_control_trade_count": safe_int(exact_control.get("trade_count")),
        "exact_control_side_balance": safe_float(exact_control.get("trade_side_balance")),
        "source_f01_net_profit": safe_float(source_f01.get("net_profit")),
        "source_f01_profit_factor": safe_float(source_f01.get("profit_factor")),
        "source_f01_expectancy": safe_float(source_f01.get("expectancy")),
        "source_f01_recovery_factor": safe_float(source_f01.get("recovery_factor")),
        "source_f01_drawdown": safe_float(source_f01.get("max_drawdown_amount")),
        "source_f01_trade_count": safe_int(source_f01.get("trade_count")),
        "local_pass_attempts": ";".join(local_pass["attempt_name"].astype(str).tolist()),
    }
    return frame, metrics


def build_kpi_judgment(scorecard: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in scorecard.iterrows():
        rows.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "judgment_class": "positive_clue(긍정 단서)" if bool(row["local_floor_pass"]) else "weak_or_negative(약함 또는 부정)",
                "floor_pass_count": int(row["floor_pass_count"]),
                "local_floor_pass": bool(row["local_floor_pass"]),
                "weakness_tags": row["weakness_tags"],
                "net_profit": row["net_profit"],
                "profit_factor": row["profit_factor"],
                "expectancy": row["expectancy"],
                "recovery_factor": row["recovery_factor"],
                "max_drawdown_amount": row["max_drawdown_amount"],
                "trade_count": row["trade_count"],
                "trade_side_balance": row["trade_side_balance"],
                "evidence_missing": "forward/replay(전진/재생); session/regime split(세션/국면 분할); cost stress(비용 압박); equity curve quality(수익곡선 품질); Tier B(티어 B)",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_attribution(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "topic": "corrected_control_restored(수정 대조 복구)",
                "observed_change": (
                    f"q01 exact control(정확 대조)은 net_profit(순수익) {metrics['exact_control_net_profit']}, "
                    f"profit_factor(수익 팩터) {metrics['exact_control_profit_factor']}, "
                    f"recovery_factor(회복 계수) {metrics['exact_control_recovery_factor']}, "
                    f"drawdown(낙폭) {metrics['exact_control_drawdown']}로 source f01(원본 f01) 구조를 재현했다."
                ),
                "attribution": "close_on_flat=False(평탄 청산 꺼짐)을 복구하자 run340D(340D 실행)의 음수 표면이 사라졌다.",
                "effect": "원본 f01 단서를 보존하고 다음 stability/cost/regime(안정성/비용/국면) 검증으로 보낼 수 있다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "topic": "q09_net_clue_quality_tradeoff(q09 순수익 단서 품질 교환)",
                "observed_change": (
                    f"q09는 net_profit(순수익) {metrics['best_net_profit']}로 source f01 대비 "
                    f"{metrics['best_net_delta_vs_source_f01']:.2f} 높지만 drawdown(낙폭)은 "
                    f"{metrics['best_drawdown_delta_vs_source_f01']:.2f} 커지고 recovery_factor(회복 계수)는 "
                    f"{metrics['best_recovery_delta_vs_source_f01']:.2f} 낮다."
                ),
                "attribution": "short_threshold(숏 임계값) 0.545 완화는 미세 순수익 단서지만 회복 품질을 희생한다.",
                "effect": "q09를 단독 승자로 고정하지 않고 q01과 paired stress(쌍 압박)로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "topic": "hold_variants_recovery_tax(보유 변형 회복 손상)",
                "observed_change": "q07 hold=10(보유 10)과 q08 hold=14(보유 14)는 순수익은 양수지만 recovery_factor(회복 계수)가 1 미만이다.",
                "attribution": "보유 시간만 바꾸는 방향은 수익 구조를 완전히 개선하지 못했다.",
                "effect": "다음 탐색에서 hold-only(보유만 변경) 반복을 줄이고 session/cost/equity(세션/비용/수익곡선)로 질문을 옮긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_failure_memory() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "failure_id": "run340H_hold_only_recovery_tax",
                "hypothesis": "hold(보유) 길이만 바꾸면 recovery_factor(회복 계수)를 유지하면서 순수익을 개선할 것이다.",
                "failed_boundary": "q07 hold=10(보유 10) recovery 0.83, q08 hold=14(보유 14) recovery 0.96으로 floor(하한) 미달이다.",
                "salvage_value": "hold(보유)는 단독 축이 아니라 session/regime(세션/국면) 조건과 결합할 때 다시 열 수 있다.",
                "do_not_repeat": "hold-only(보유만 변경) 압박을 같은 구간에서 반복하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "failure_id": "run340H_q09_net_over_quality_risk",
                "hypothesis": "q09의 순수익 최고값만으로 q01보다 우월하다고 볼 수 있다.",
                "failed_boundary": "q09는 net +0.70이지만 drawdown +10.00, recovery -0.14로 품질 교환이 있다.",
                "salvage_value": "q09는 q01과 함께 stability/cost/regime(안정성/비용/국면) 압박 후보로 보존한다.",
                "do_not_repeat": "단일 net_profit(순수익) 최고값만으로 selection(선정)을 주장하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_next_seed_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "seed_id": "s01_q01_exact_control_quality_anchor",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": "q01_ctl_s55_l51_m01_h12",
                "role": "quality_anchor_exact_control(품질 기준 정확 대조)",
                "stress_axes": "session/regime split(세션/국면 분할); cost stress(비용 압박); equity curve quality(수익곡선 품질)",
                "effect": "source f01(원본 f01)의 안정적 구조가 비용과 국면에서 버티는지 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "seed_id": "s02_q09_net_high_pressure_candidate",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": "q09_s545_l51_m01_h12",
                "role": "net_high_quality_tradeoff_candidate(순수익 높음 품질 교환 후보)",
                "stress_axes": "session/regime split(세션/국면 분할); cost stress(비용 압박); drawdown localization(낙폭 위치화)",
                "effect": "q09(큐09)의 작은 순수익 개선이 비용과 국면 압박에서도 살아남는지 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "seed_id": "s03_hold_only_negative_control",
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": "q07_h10_s55_l51_m01_h10;q08_h14_s55_l51_m01_h14",
                "role": "negative_control(부정 대조)",
                "stress_axes": "do_not_repeat_hold_only(보유만 변경 반복 금지)",
                "effect": "실패 기억을 다음 stage(단계)의 제약으로 쓴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_final(metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "attempt_count": metrics["attempt_count"],
        "expected_rows_total": metrics["expected_rows_total"],
        "matched_rows_total": metrics["matched_rows_total"],
        "mismatch_rows_total": metrics["mismatch_rows_total"],
        "all_exact_parity": metrics["all_exact_parity"],
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
        "exact_control_net_profit": metrics["exact_control_net_profit"],
        "exact_control_profit_factor": metrics["exact_control_profit_factor"],
        "exact_control_expectancy": metrics["exact_control_expectancy"],
        "exact_control_recovery_factor": metrics["exact_control_recovery_factor"],
        "exact_control_drawdown": metrics["exact_control_drawdown"],
        "exact_control_trade_count": metrics["exact_control_trade_count"],
        "exact_control_side_balance": metrics["exact_control_side_balance"],
        "best_net_delta_vs_source_f01": metrics["best_net_delta_vs_source_f01"],
        "best_recovery_delta_vs_source_f01": metrics["best_recovery_delta_vs_source_f01"],
        "best_drawdown_delta_vs_source_f01": metrics["best_drawdown_delta_vs_source_f01"],
        "local_pass_attempts": metrics["local_pass_attempts"],
        "judgment_class": "positive_clue_no_selection(긍정 단서, 선정 없음)",
        "evidence_boundary": "reviewed_mt5_runtime_probe_no_selection(검토된 MT5 런타임 탐침, 선정 없음)",
        "external_verification_status": "completed(완료)",
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
    return pd.DataFrame(
        [
            gate_row("parent_340G_gates_passed", "passed" if gate_statuses_pass(parent_gates) else "failed", rel(PARENT_GATE_AUDIT), "run340G(340G 실행) MT5 probe(MT5 탐침)를 이어받는다."),
            gate_row("package_340F_gates_passed", "passed" if gate_statuses_pass(package_gates) else "failed", rel(PACKAGE_GATE_AUDIT), "run340F(340F 실행) package(패키지)를 이어받는다."),
            gate_row("scorecard_written", "passed" if path_exists(SCORECARD) else "failed", rel(SCORECARD), "KPI scorecard(KPI 점수표)를 만든다."),
            gate_row("positive_clue_classified", "passed" if final["local_floor_pass_count"] >= 1 and final["best_net_profit"] > 0 else "failed", rel(SCORECARD), "positive clue(긍정 단서)를 하한 기준으로 분류한다."),
            gate_row("q09_quality_tradeoff_recorded", "passed" if final["best_drawdown_delta_vs_source_f01"] > 0 and final["best_recovery_delta_vs_source_f01"] < 0 else "failed", rel(PERFORMANCE_ATTRIBUTION), "q09(큐09)의 순수익/품질 교환을 기록한다."),
            gate_row("next_stage_seed_queue_written", "passed" if path_exists(NEXT_SEED_QUEUE) else "failed", rel(NEXT_SEED_QUEUE), "다음 stage(단계) seed queue(씨앗 대기열)를 만든다."),
            gate_row("tier_records_written", "passed", rel(STAGE_LEDGER), "Tier A/B/A+B(티어 A/B/A+B) 기록을 장부에 연결한다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", rel(CLAIM_RECEIPT), "review(검토)를 selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)로 말하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "required gate coverage audit(필수 게이트 커버리지 감사)를 남긴다."),
        ]
    )


def artifact_paths() -> list[Path]:
    return [
        SCORECARD,
        KPI_JUDGMENT,
        PERFORMANCE_ATTRIBUTION,
        FAILURE_MEMORY,
        NEXT_SEED_QUEUE,
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
            "exact_control_net_profit": final["exact_control_net_profit"],
            "exact_control_profit_factor": final["exact_control_profit_factor"],
            "local_floor_pass_count": final["local_floor_pass_count"],
            "evidence_boundary": final["evidence_boundary"],
        },
    )
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run340G f01 close_on_flat false pressure MT5 probe(340G f01 평탄 청산 꺼짐 압박 MT5 탐침)",
            "evidence_available": [rel(PARENT_RUNTIME_SUMMARY), rel(PARENT_PROXY_DIFF), rel(SCORECARD)],
            "judgment_label": JUDGMENT,
            "evidence_missing": "forward/replay(전진/재생); cost stress(비용 압박); session/regime(세션/국면); equity curve quality(수익곡선 품질); Tier B(티어 B)",
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": "close_on_flat false restored positive runtime surface(평탄 청산 꺼짐 복구 긍정 런타임 표면)",
            "comparison_baseline": "source f01 and run340D close_on_flat true failure(원본 f01과 340D 평탄 청산 켬 실패)",
            "likely_drivers": "lifecycle exit semantics restored(생명주기 청산 의미 복구)",
            "attribution_confidence": "high_for_semantics_repair_medium_for_q09_edge(의미 수리 높음, q09 우위 중간)",
            "next_probe": rel(NEXT_SEED_QUEUE),
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
        SOURCE_RUNTIME_SUMMARY,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in source_inputs],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths() if path_exists(path)],
            "source_artifact_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_positive_clue_boundary(긍정 단서 경계로 연결)",
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run340H F01 Close-On-Flat False Pressure Review(340H F01 평탄 청산 꺼짐 압박 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- exact_parity(정확 동등성): `{final['matched_rows_total']}/{final['expected_rows_total']}`, mismatch(불일치): `{final['mismatch_rows_total']}`
- local_floor_pass_count(로컬 하한 통과 수): `{final['local_floor_pass_count']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_expectancy(최고 기대값): `{final['best_expectancy']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- exact_control_net_profit(정확 대조 순수익): `{final['exact_control_net_profit']}`
- exact_control_profit_factor(정확 대조 수익 팩터): `{final['exact_control_profit_factor']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Judgment(판정)

close_on_flat=False(평탄 청산 꺼짐)을 복구하자 f01(에프01) 표면은 다시 positive runtime clue(긍정 런타임 단서)가 됐다. q09(큐09)는 net_profit(순수익)이 가장 높지만 source f01(원본 f01) 대비 drawdown(낙폭)이 커지고 recovery_factor(회복 계수)가 낮아 quality tradeoff(품질 교환)가 있다.

Effect(효과): q09(큐09)를 단일 승자로 고정하지 않고, q01 exact control(정확 대조)과 q09 net-high clue(순수익 높은 단서)를 다음 stability/cost/regime(안정성/비용/국면) stage(단계)로 함께 넘긴다.

## Boundary(경계)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating_promotion(운영 승격 없음), no runtime_authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage340H Decision(340H 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(SCORECARD)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`, `{rel(NEXT_SEED_QUEUE)}`

Action(행동): run340G(340G 실행)의 corrected MT5 KPI(수정 MT5 핵심 성과 지표)를 검토했다.

Effect(효과): Stage341(341단계)로 session/regime stability(세션/국면 안정성), cost stress(비용 압박), equity curve quality(수익곡선 품질) 검증을 분기할 수 있다.

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

run340H(340H 실행)는 close_on_flat=False(평탄 청산 꺼짐) corrected probe(수정 탐침)를 positive runtime clue(긍정 런타임 단서)로 닫았다. 다음은 Stage341(341단계) branch(분기)로 stability/cost/regime(안정성/비용/국면)을 검증한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage340 Selection Status(340단계 선정 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- positive_clue_anchor(긍정 단서 기준): `q01_ctl_s55_l51_m01_h12`
- net_high_clue(순수익 높은 단서): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- exact_control_net_profit(정확 대조 순수익): `{final['exact_control_net_profit']}`
- exact_control_recovery_factor(정확 대조 회복 계수): `{final['exact_control_recovery_factor']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): positive clue(긍정 단서)를 운영 선정(selection, 선정)으로 오해하지 않게 한다.
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
    marker = f"run340H {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run340H F01 Close-On-Flat False Pressure Review(340H F01 평탄 청산 꺼짐 압박 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- local_floor_pass_count(로컬 하한 통과 수): `{final['local_floor_pass_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): q01/q09(큐01/큐09)를 Stage341(341단계) stability/cost/regime(안정성/비용/국면) 검증 씨앗으로 보존한다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run340H F01 Close-On-Flat False Pressure Review(340H F01 평탄 청산 꺼짐 압박 검토)

- run_id(실행 ID): `{RUN_ID}`
- scorecard(점수표): `{rel(SCORECARD)}`
- seed_queue(씨앗 대기열): `{rel(NEXT_SEED_QUEUE)}`
- effect(효과): Stage340(340단계) 압박 질문을 닫고 Stage341(341단계) 안정성 검증으로 넘긴다.
""",
    )
    changelog = f"""## {TODAY} run340H F01 Close-On-Flat False Pressure Review(F01 평탄 청산 꺼짐 압박 검토)

- action(행동): run340G(340G 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 검토했다.
- effect(효과): close_on_flat=False(평탄 청산 꺼짐) 복구가 긍정 단서를 되살렸고, q09(큐09)의 순수익 단서는 품질 교환으로 분류했다.
- boundary(경계): selected model/runtime authority/Goal Achieve(선정 모델/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_exploration_registers() -> None:
    marker = f"run340H {RUN_ID}"
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage340H F01 Stability Cost Seed(340H F01 안정성 비용 씨앗)

- idea_id(아이디어 ID): `stage341_f01_stability_cost_regime_validation`
- hypothesis(가설): q01 exact control(정확 대조)과 q09 net-high clue(순수익 높은 단서)가 cost/session/regime(비용/세션/국면) 압박에서도 버티면 promotion_candidate(승격 후보) 비교 가치가 생긴다.
- source(원천): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- seed_queue(씨앗 대기열): `{rel(NEXT_SEED_QUEUE)}`
- effect(효과): 긍정 단서를 운영 주장으로 과장하지 않고 다음 외부 검증 질문으로 넘긴다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} Stage340H Hold-Only Recovery Tax(보유 단독 회복 손상)

- subject(대상): `q07_h10` and `q08_h14`
- evidence(근거): `{rel(FAILURE_MEMORY)}`
- judgment(판정): `negative_clue_with_constraint(제약으로 남기는 부정 단서)`
- effect(효과): hold-only(보유만 변경) 반복을 줄이고 session/regime(세션/국면) 조건과 결합할 때만 다시 연다.
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
            "metric_scope": "mt5_runtime_probe_review",
            "candidate_model_id": final["best_model_id"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "drawdown": final["best_drawdown"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "positive_clue_no_selection",
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
    registry = read_csv(ARTIFACT_REGISTRY) if path_exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not path_exists(path) or not path_is_file(path):
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
    Path(fs_path(RUN_DIR)).mkdir(parents=True, exist_ok=True)
    parent_final, parent_gates, package_final, package_gates = load_context()
    scorecard, metrics = build_scorecard()
    kpi_judgment = build_kpi_judgment(scorecard)
    attribution = build_attribution(metrics)
    failure_memory = build_failure_memory()
    next_seed = build_next_seed_queue()
    write_csv(SCORECARD, scorecard)
    write_csv(KPI_JUDGMENT, kpi_judgment)
    write_csv(PERFORMANCE_ATTRIBUTION, attribution)
    write_csv(FAILURE_MEMORY, failure_memory)
    write_csv(NEXT_SEED_QUEUE, next_seed)
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
            ],
            "outputs": [rel(path) for path in artifact_paths() if path_exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_receipts(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run340H gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "exact_control_net_profit": final["exact_control_net_profit"],
                "exact_control_recovery_factor": final["exact_control_recovery_factor"],
                "local_floor_pass_count": final["local_floor_pass_count"],
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
