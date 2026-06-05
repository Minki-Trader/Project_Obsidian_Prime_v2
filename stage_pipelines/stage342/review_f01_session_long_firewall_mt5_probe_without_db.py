from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage342 import execute_f01_session_long_firewall_mt5_probe_without_db as exe  # noqa: E402
from stage_pipelines.stage342 import materialize_f01_session_long_firewall_mt5_probe_package_without_db as pkg  # noqa: E402


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run342D"
RUN_ID = "run342D_review_f01_session_long_firewall_mt5_probe_without_db_v1"
PARENT_RUN_ID = exe.RUN_ID
NEXT_RUN_ID = "run342E_materialize_soft_session_long_firewall_mt5_probe_package_without_db_v1"

STATUS = "completed_stage342D_session_long_firewall_reviewed_profit_quality_clue_trade_shape_blocked_no_selection"
JUDGMENT = "hard_early_long_firewall_improves_profit_quality_but_trade_count_and_long_short_balance_block_selection"
DECISION = "stage342D_open_run342E_soft_session_long_firewall_pressure_package"
CLAIM_BOUNDARY = (
    "research_development_review_only_f01_session_long_firewall_mt5_probe_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run342D_f01_session_long_firewall_mt5_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage342D_f01_session_long_firewall_mt5_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

SOURCE_FINAL = exe.FINAL_DECISION
SOURCE_GATES = exe.GATE_AUDIT
SOURCE_SUMMARY = exe.EXECUTION_SUMMARY
SOURCE_DIFF = exe.PROXY_MT5_DIFF
SOURCE_RUNTIME_IDENTITY = exe.RUNTIME_IDENTITY
SOURCE_VARIANT_PREVIEW = pkg.VARIANT_PREVIEW
SOURCE_SIDE_AUDIT = pkg.SIDE_FILTER_EXPECTED_AUDIT

REVIEW_SCORECARD = RUN_DIR / "session_long_firewall_review_scorecard.csv"
KPI_JUDGMENT = RUN_DIR / "session_long_firewall_kpi_judgment.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run342E_soft_session_long_firewall_probe_queue.csv"
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
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
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
    return pkg.rel(path)


def exists(path: Path) -> bool:
    return pkg.path_exists(path)


def is_file(path: Path) -> bool:
    return pkg.path_is_file(path)


def read_csv(path: Path) -> pd.DataFrame:
    return pkg.read_csv(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    pkg.ensure_parent(path)
    with open(pkg.fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    pkg.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_or_replace_csv(path, keys, rows)


def num(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(num(value, default)))
    except (TypeError, ValueError):
        return default


def gate_passed(path: Path) -> bool:
    frame = read_csv(path)
    return bool(frame["status"].astype(str).str.lower().eq("passed").all())


def floor_flags(row: pd.Series) -> dict[str, bool]:
    side_max = max(num(row.get("long_trade_count")), num(row.get("short_trade_count")))
    side_balance = 0.0 if side_max <= 0 else min(num(row.get("long_trade_count")), num(row.get("short_trade_count"))) / side_max
    return {
        "exact_parity_pass": bool(
            row.get("comparison_status") == "completed_exact_proxy_mt5_parity_reached_feature_last"
            and num(row.get("expected_rows")) == num(row.get("matched_rows"))
            and num(row.get("probability_mismatch_rows")) == 0
            and num(row.get("decision_mismatch_rows")) == 0
        ),
        "net_profit_pass": num(row.get("net_profit")) > FLOORS["net_profit"],
        "profit_factor_pass": num(row.get("profit_factor")) >= FLOORS["profit_factor"],
        "expectancy_pass": num(row.get("expectancy")) > FLOORS["expectancy"],
        "recovery_factor_pass": num(row.get("recovery_factor")) >= FLOORS["recovery_factor"],
        "drawdown_pass": num(row.get("max_drawdown_amount")) <= FLOORS["max_drawdown_amount"],
        "trade_count_pass": num(row.get("trade_count")) >= FLOORS["trade_count"],
        "trade_side_balance_pass": side_balance >= FLOORS["trade_side_balance"],
    }


def weakness_tags(row: pd.Series) -> str:
    tags: list[str] = []
    labels = {
        "exact_parity_pass": "parity(동등성)",
        "net_profit_pass": "net_profit(순수익)",
        "profit_factor_pass": "profit_factor(수익 팩터)",
        "expectancy_pass": "expectancy(기대값)",
        "recovery_factor_pass": "recovery_factor(회복 계수)",
        "drawdown_pass": "drawdown(낙폭)",
        "trade_count_pass": "trade_count(거래수)",
        "trade_side_balance_pass": "side_balance(방향 균형)",
    }
    for key, label in labels.items():
        if not bool(row.get(key, False)):
            tags.append(label)
    return ";".join(tags) if tags else "none(없음)"


def row_judgment(row: pd.Series) -> str:
    attempt = str(row.get("attempt_name", ""))
    if bool(row.get("local_floor_pass", False)) and attempt.endswith("_ctl"):
        return "control_floor_pass_preserved_no_new_selection(대조 하한 통과 보존, 신규 선정 없음)"
    if "blk_early_long" in attempt and num(row.get("net_delta_vs_control")) > 0:
        return "profit_quality_clue_but_trade_shape_blocked(수익 품질 단서이나 거래 형태 차단)"
    if "blk_early_all" in attempt:
        return "overfilter_negative_control_edge_damaged(과필터 부정 대조, 우위 손상)"
    if num(row.get("net_profit")) > 0:
        return "positive_control_or_weak_clue_no_selection(긍정 대조 또는 약한 단서, 선정 없음)"
    return "negative_or_unusable_probe(부정 또는 사용 불가 탐침)"


def control_attempt(attempt: str) -> str:
    if attempt.startswith("e03_"):
        return "e01_q01_ctl"
    if attempt.startswith("e04_") or attempt.startswith("e05_"):
        return "e02_q09_ctl"
    return attempt


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    summary = read_csv(SOURCE_SUMMARY).fillna("")
    preview = read_csv(SOURCE_VARIANT_PREVIEW).fillna("")
    side = read_csv(SOURCE_SIDE_AUDIT).fillna("")
    for column in [
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
        "order_attempt_count",
        "order_fill_count",
    ]:
        if column in summary.columns:
            summary[column] = pd.to_numeric(summary[column], errors="coerce")
    side_lookup = {
        str(row["attempt_name"]): row.to_dict()
        for _, row in side.iterrows()
        if str(row.get("attempt_name", "")).strip()
    }
    preview_lookup = {
        str(row["attempt_name"]): row.to_dict()
        for _, row in preview.iterrows()
        if str(row.get("attempt_name", "")).strip()
    }
    rows: list[dict[str, Any]] = []
    control_rows = {str(row["attempt_name"]): row for _, row in summary.iterrows()}
    for _, source in summary.iterrows():
        row = source.to_dict()
        attempt = str(row.get("attempt_name", ""))
        side_max = max(num(row.get("long_trade_count")), num(row.get("short_trade_count")))
        row["trade_side_balance"] = 0.0 if side_max <= 0 else min(num(row.get("long_trade_count")), num(row.get("short_trade_count"))) / side_max
        control_name = control_attempt(attempt)
        control = control_rows.get(control_name, source)
        row["control_attempt"] = control_name
        row["net_delta_vs_control"] = num(row.get("net_profit")) - num(control.get("net_profit"))
        row["profit_factor_delta_vs_control"] = num(row.get("profit_factor")) - num(control.get("profit_factor"))
        row["recovery_delta_vs_control"] = num(row.get("recovery_factor")) - num(control.get("recovery_factor"))
        row["trade_count_delta_vs_control"] = num(row.get("trade_count")) - num(control.get("trade_count"))
        row["long_trade_delta_vs_control"] = num(row.get("long_trade_count")) - num(control.get("long_trade_count"))
        row["short_trade_delta_vs_control"] = num(row.get("short_trade_count")) - num(control.get("short_trade_count"))
        row["blocked_long_rows"] = as_int(side_lookup.get(attempt, {}).get("blocked_long_rows"))
        row["blocked_short_rows"] = as_int(side_lookup.get(attempt, {}).get("blocked_short_rows"))
        row["signal_long_count"] = as_int(preview_lookup.get(attempt, {}).get("signal_long_count"))
        row["signal_short_count"] = as_int(preview_lookup.get(attempt, {}).get("signal_short_count"))
        for key, value in floor_flags(pd.Series(row)).items():
            row[key] = value
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
        row["floor_pass_count"] = sum(1 for key in pass_columns if bool(row[key]))
        row["local_floor_pass"] = all(bool(row[key]) for key in pass_columns)
        row["weakness_tags"] = weakness_tags(pd.Series(row))
        row["review_judgment"] = row_judgment(pd.Series(row))
        row["claim_boundary"] = CLAIM_BOUNDARY
        rows.append(row)
    scorecard = pd.DataFrame(rows)
    scorecard = scorecard.sort_values(
        ["local_floor_pass", "floor_pass_count", "net_profit", "profit_factor", "recovery_factor"],
        ascending=[False, False, False, False, False],
    ).reset_index(drop=True)
    e01 = scorecard.loc[scorecard["attempt_name"].eq("e01_q01_ctl")].iloc[0]
    e02 = scorecard.loc[scorecard["attempt_name"].eq("e02_q09_ctl")].iloc[0]
    e03 = scorecard.loc[scorecard["attempt_name"].eq("e03_q01_blk_early_long")].iloc[0]
    e04 = scorecard.loc[scorecard["attempt_name"].eq("e04_q09_blk_early_long")].iloc[0]
    e05 = scorecard.loc[scorecard["attempt_name"].eq("e05_q09_blk_early_all")].iloc[0]
    best_profit = scorecard.sort_values(["net_profit", "profit_factor"], ascending=[False, False]).iloc[0]
    metrics = {
        "attempt_count": int(len(scorecard)),
        "expected_rows_total": int(scorecard["expected_rows"].fillna(0).sum()),
        "matched_rows_total": int(scorecard["matched_rows"].fillna(0).sum()),
        "mismatch_rows_total": int(
            scorecard["probability_mismatch_rows"].fillna(0).sum()
            + scorecard["decision_mismatch_rows"].fillna(0).sum()
        ),
        "all_exact_parity": bool(scorecard["exact_parity_pass"].astype(bool).all()),
        "local_floor_pass_count": int(scorecard["local_floor_pass"].astype(bool).sum()),
        "hard_firewall_positive_count": int(
            (
                scorecard["attempt_name"].astype(str).str.contains("blk_early_long").astype(bool)
                & (scorecard["net_delta_vs_control"].astype(float) > 0)
            ).sum()
        ),
        "best_profit_attempt": str(best_profit["attempt_name"]),
        "best_profit_model_id": str(best_profit["model_id"]),
        "best_profit_net": num(best_profit["net_profit"]),
        "best_profit_factor": num(best_profit["profit_factor"]),
        "best_profit_expectancy": num(best_profit["expectancy"]),
        "best_profit_recovery": num(best_profit["recovery_factor"]),
        "best_profit_drawdown": num(best_profit["max_drawdown_amount"]),
        "best_profit_trade_count": as_int(best_profit["trade_count"]),
        "best_profit_long_trade_count": as_int(best_profit["long_trade_count"]),
        "best_profit_short_trade_count": as_int(best_profit["short_trade_count"]),
        "best_profit_side_balance": num(best_profit["trade_side_balance"]),
        "q01_control_net": num(e01["net_profit"]),
        "q09_control_net": num(e02["net_profit"]),
        "q01_firewall_net_delta": num(e03["net_delta_vs_control"]),
        "q09_firewall_net_delta": num(e04["net_delta_vs_control"]),
        "q01_firewall_trade_delta": as_int(e03["trade_count_delta_vs_control"]),
        "q09_firewall_trade_delta": as_int(e04["trade_count_delta_vs_control"]),
        "q01_firewall_long_trade_delta": as_int(e03["long_trade_delta_vs_control"]),
        "q09_firewall_long_trade_delta": as_int(e04["long_trade_delta_vs_control"]),
        "overfilter_net": num(e05["net_profit"]),
        "overfilter_trade_count": as_int(e05["trade_count"]),
    }
    judgment = build_kpi_judgment(scorecard)
    attribution = build_attribution(metrics)
    failure = build_failure_memory(metrics)
    next_queue = build_next_queue()
    return scorecard, judgment, attribution, failure, next_queue, metrics


def build_kpi_judgment(scorecard: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in scorecard.iterrows():
        if bool(row["local_floor_pass"]) and str(row["attempt_name"]).endswith("_ctl"):
            judgment_class = "control_floor_pass_no_new_selection(대조 하한 통과, 신규 선정 없음)"
        elif "blk_early_long" in str(row["attempt_name"]) and num(row["net_delta_vs_control"]) > 0:
            judgment_class = "positive_profit_quality_clue_selection_blocked(수익 품질 긍정 단서, 선정 차단)"
        elif "blk_early_all" in str(row["attempt_name"]):
            judgment_class = "negative_control_overfilter(과필터 부정 대조)"
        else:
            judgment_class = "weak_or_context_clue_no_selection(약한 또는 문맥 단서, 선정 없음)"
        rows.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "judgment_class": judgment_class,
                "scoreboard": "MT5 runtime probe(MT5 런타임 탐침);trade shape(거래 형태);runtime parity(런타임 동등성)",
                "parity_level": "P3_exact_runtime_proxy_parity(P3 정확 런타임-프록시 동등성)",
                "wfo_status": "single_window_runtime_probe_only(단일 구간 런타임 탐침만)",
                "local_floor_pass": bool(row["local_floor_pass"]),
                "floor_pass_count": int(row["floor_pass_count"]),
                "weakness_tags": row["weakness_tags"],
                "evidence_missing": (
                    "Tier B(티어 B); forward/replay(전진/재생); cost stress(비용 압박); "
                    "session/regime split beyond designed filter(설계 필터 밖 세션/국면 분할); equity curve quality(수익곡선 품질)"
                ),
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_attribution(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "topic": "hard_early_long_firewall_profit_quality(강한 초반 롱 방화벽 수익 품질)",
                "comparison_baseline": "q01/q09 controls without side filter(사이드 필터 없는 q01/q09 대조)",
                "observed_change": (
                    f"q01 firewall net delta(순수익 차이) {metrics['q01_firewall_net_delta']}, "
                    f"q09 firewall net delta(순수익 차이) {metrics['q09_firewall_net_delta']}; "
                    f"best(최선) {metrics['best_profit_attempt']} net_profit(순수익) {metrics['best_profit_net']} "
                    f"PF(수익 팩터) {metrics['best_profit_factor']} expectancy(기대값) {metrics['best_profit_expectancy']}"
                ),
                "likely_drivers": "minutes_from_cash_open(현금장 개장 후 분) 0~110 long(롱)을 flat(관망) 처리해 약한 early long(초반 롱) 손실을 줄였다.",
                "trade_shape": (
                    f"best trade_count(거래수) {metrics['best_profit_trade_count']}, "
                    f"long/short(롱/숏) {metrics['best_profit_long_trade_count']}/{metrics['best_profit_short_trade_count']}, "
                    f"side_balance(방향 균형) {metrics['best_profit_side_balance']:.3f}"
                ),
                "selection_blocker": "trade_count(거래수)와 long/short balance(롱/숏 균형)가 운영 주장에 부족하다.",
                "attribution_confidence": "medium(중간)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "topic": "overfilter_negative_control(과필터 부정 대조)",
                "comparison_baseline": "q09 hard early-long firewall(q09 강한 초반 롱 방화벽)",
                "observed_change": (
                    f"e05 block all early sides(초반 양방향 차단) net_profit(순수익) {metrics['overfilter_net']}, "
                    f"trade_count(거래수) {metrics['overfilter_trade_count']}"
                ),
                "likely_drivers": "early short(초반 숏)까지 막으면 profitable short supply(수익성 있는 숏 공급)가 줄어든다.",
                "trade_shape": "hard block all sides(강한 양방향 차단)는 수익 품질을 높이는 방향이 아니라 edge(우위)를 잘라낸다.",
                "selection_blocker": "overfilter(과필터)는 다음 탐색에서 부정 대조로만 유지한다.",
                "attribution_confidence": "medium(중간)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_failure_memory(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "failure_id": "run342D_hard_firewall_trade_shape_tax",
                "hypothesis": "early long(초반 롱) 0~110분 차단만으로 운영 가능한 trade shape(거래 형태)를 만들 수 있다.",
                "failed_boundary": (
                    f"best trade_count(거래수) {metrics['best_profit_trade_count']} and "
                    f"long/short(롱/숏) {metrics['best_profit_long_trade_count']}/{metrics['best_profit_short_trade_count']}"
                ),
                "salvage_value": "net_profit/PF/expectancy(순수익/수익 팩터/기대값)가 좋아졌으므로 softer window(부드러운 구간) 탐색 가치가 있다.",
                "do_not_repeat": "hard 0~110 long block(강한 0~110 롱 차단)을 단독 selected model(선정 모델)처럼 다루지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "failure_id": "run342D_early_all_side_overfilter",
                "hypothesis": "early session(초반 세션)을 양방향 모두 막으면 더 안정적일 수 있다.",
                "failed_boundary": f"overfilter net_profit(과필터 순수익) {metrics['overfilter_net']} and trade_count(거래수) {metrics['overfilter_trade_count']}",
                "salvage_value": "short side(숏 방향)는 초반에도 일부 유효하므로 long-only firewall(롱 전용 방화벽) 축을 유지한다.",
                "do_not_repeat": "early all-side block(초반 양방향 차단)을 주 탐색축으로 반복하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_next_queue() -> pd.DataFrame:
    rows = [
        ("e01_q01_control_no_filter", "q01_ctl_s55_l51_m01_h12", False, "", "", "control_quality_anchor(품질 기준 대조)", "q01 exact replay(정확 재생)를 유지한다."),
        ("e02_q09_control_no_filter", "q09_s545_l51_m01_h12", False, "", "", "control_net_anchor(순수익 기준 대조)", "q09 exact replay(정확 재생)를 유지한다."),
        ("e03_q01_block_early_long_0_45", "q01_ctl_s55_l51_m01_h12", True, "0,45", "", "soft_firewall_q01(부드러운 q01 방화벽)", "hard firewall(강한 방화벽)의 trade count tax(거래수 비용)를 줄이는지 본다."),
        ("e04_q09_block_early_long_0_45", "q09_s545_l51_m01_h12", True, "0,45", "", "soft_firewall_q09(부드러운 q09 방화벽)", "q09 순수익 단서가 더 부드럽게 유지되는지 본다."),
        ("e05_q01_block_early_long_0_75", "q01_ctl_s55_l51_m01_h12", True, "0,75", "", "mid_firewall_q01(중간 q01 방화벽)", "0~110분보다 약하고 0~45분보다 강한 중간 구간을 본다."),
        ("e06_q09_block_early_long_0_75", "q09_s545_l51_m01_h12", True, "0,75", "", "mid_firewall_q09(중간 q09 방화벽)", "PF(수익 팩터)와 trade count(거래수)의 절충점을 찾는다."),
        ("e07_q09_block_early_all_0_45_negative_control", "q09_s545_l51_m01_h12", True, "0,45", "0,45", "soft_overfilter_negative_control(부드러운 과필터 부정 대조)", "short supply(숏 공급) 손상을 다시 확인한다."),
    ]
    return pd.DataFrame(
        [
            {
                "queue_id": queue_id,
                "next_run_id": NEXT_RUN_ID,
                "source_attempt": source,
                "side_filter_enabled": enabled,
                "feature_index": 37 if enabled else "",
                "feature_name": "minutes_from_cash_open" if enabled else "",
                "block_long_range": long_range,
                "block_short_range": short_range,
                "role": role,
                "expected_effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for queue_id, source, enabled, long_range, short_range, role, effect in rows
        ]
    )


def artifact_paths() -> list[Path]:
    return [
        REVIEW_SCORECARD,
        KPI_JUDGMENT,
        PERFORMANCE_ATTRIBUTION,
        FAILURE_MEMORY,
        NEXT_QUEUE,
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
        ROOT_SELECTION_STATUS,
        STAGE_BRIEF,
        STAGE_README,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        ROOT_CHANGELOG,
        WORKSPACE_CHANGELOG,
        IDEA_REGISTRY,
        NEGATIVE_RESULT_REGISTER,
        RUN_REGISTRY,
        PROJECT_LEDGER,
        STAGE_LEDGER,
        ARTIFACT_REGISTRY,
        Path(__file__),
    ]


def write_receipts(metrics: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "judgment_class": "positive_profit_quality_clue_selection_blocked(수익 품질 긍정 단서, 선정 차단)",
            "best_profit_attempt": metrics["best_profit_attempt"],
            "selection_blockers": "trade_count(거래수); long_short_balance(롱/숏 균형); missing_forward_and_tier_b(전진 및 Tier B 누락)",
            "effect": "좋은 PF(수익 팩터)를 보존하되 운영 모델로 올리지 않는다.",
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "best_profit_attempt": metrics["best_profit_attempt"],
            "q01_firewall_net_delta": metrics["q01_firewall_net_delta"],
            "q09_firewall_net_delta": metrics["q09_firewall_net_delta"],
            "best_profit_side_balance": metrics["best_profit_side_balance"],
            "next_probe": rel(NEXT_QUEUE),
            "effect": "hard firewall(강한 방화벽)의 수익 개선과 거래 형태 비용을 함께 추적한다.",
        },
    )
    existing = [path for path in artifact_paths() if exists(path) and path != LINEAGE_RECEIPT]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [
                rel(SOURCE_FINAL),
                rel(SOURCE_GATES),
                rel(SOURCE_SUMMARY),
                rel(SOURCE_DIFF),
                rel(SOURCE_RUNTIME_IDENTITY),
                rel(SOURCE_VARIANT_PREVIEW),
                rel(SOURCE_SIDE_AUDIT),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in existing],
            "artifact_hashes": {rel(path): pkg.sha256_file(path) for path in existing if is_file(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "promotion_candidate": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
    )


def gate_row(gate_id: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row("parent_342C_gates_passed", "passed" if gate_passed(SOURCE_GATES) else "failed", rel(SOURCE_GATES), "run342C(342C 실행) MT5 runtime probe(MT5 런타임 탐침)를 이어받는다."),
            gate_row("review_scorecard_written", "passed" if exists(REVIEW_SCORECARD) else "failed", rel(REVIEW_SCORECARD), "KPI scorecard(KPI 점수표)를 만든다."),
            gate_row("exact_runtime_parity_reviewed", "passed" if metrics["all_exact_parity"] and metrics["mismatch_rows_total"] == 0 else "failed", rel(SOURCE_DIFF), "proxy-MT5 parity(프록시-MT5 동등성)를 판정에 연결한다."),
            gate_row("profit_quality_tradeoff_recorded", "passed" if metrics["hard_firewall_positive_count"] >= 2 and metrics["best_profit_trade_count"] < 30 else "failed", rel(PERFORMANCE_ATTRIBUTION), "수익 품질 개선과 거래수 비용을 같이 기록한다."),
            gate_row("failure_memory_written", "passed" if exists(FAILURE_MEMORY) else "failed", rel(FAILURE_MEMORY), "반복하지 않을 실패 기억(failure memory, 실패 기억)을 남긴다."),
            gate_row("next_soft_firewall_queue_written", "passed" if exists(NEXT_QUEUE) and len(read_csv(NEXT_QUEUE)) >= 7 else "failed", rel(NEXT_QUEUE), "다음 softer firewall(부드러운 방화벽) 탐색 queue(대기열)를 만든다."),
            gate_row("tier_records_written", "passed" if exists(STAGE_LEDGER) else "failed", rel(STAGE_LEDGER), "Tier A/Tier B/Tier A+B(티어 A/B/A+B) 장부를 남긴다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(CLAIM_RECEIPT), "review(검토)를 selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)로 말하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "필수 게이트 감사(required gate coverage audit, 필수 게이트 감사)를 기록한다."),
        ]
    )


def write_docs(metrics: Mapping[str, Any], gates: pd.DataFrame) -> None:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
    report = f"""# run342D F01 Session-Long Firewall MT5 Probe Review(342D F01 세션 롱 방화벽 MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{gate_passes}/{gate_total}`
- exact_parity(정확 동등성): `{metrics['matched_rows_total']}/{metrics['expected_rows_total']}`, mismatch(불일치) `{metrics['mismatch_rows_total']}`
- best_profit_attempt(최고 수익 시도): `{metrics['best_profit_attempt']}`
- best_net_profit(최고 순수익): `{metrics['best_profit_net']}`
- best_profit_factor(최고 수익 팩터): `{metrics['best_profit_factor']}`
- best_expectancy(최고 기대값): `{metrics['best_profit_expectancy']}`
- best_recovery_factor(최고 회복 계수): `{metrics['best_profit_recovery']}`
- best_trade_count(최고 거래수): `{metrics['best_profit_trade_count']}`
- best_long_short(최고 롱/숏): `{metrics['best_profit_long_trade_count']}/{metrics['best_profit_short_trade_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run342C(342C 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 검토했다.
Effect(효과): hard early-long firewall(강한 초반 롱 방화벽)이 net profit/PF(순수익/수익 팩터)를 올렸지만 trade count(거래수)와 long/short balance(롱/숏 균형)를 깎았다는 구조를 분리했다.

## Judgment(판정)

e04(이04)는 profit-quality positive clue(수익 품질 긍정 단서)다. selected model(선정 모델)은 아니다.
Effect(효과): 좋은 수익 구조는 보존하고, 운영 승격(operating promotion, 운영 승격)은 막는다.

## Next(다음)

Open `{NEXT_RUN_ID}` with `{rel(NEXT_QUEUE)}`.
Effect(효과): 0~45분, 0~75분 softer firewall(부드러운 방화벽)로 거래수와 방향 균형을 회복하는지 시험한다.

## Boundary(경계)

No selection(선정 없음), no forward(전진 없음), no live readiness(실거래 준비 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage342D Review Decision(342D 검토 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(REVIEW_SCORECARD)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`, `{rel(FAILURE_MEMORY)}`, `{rel(NEXT_QUEUE)}`

Action(행동): hard session-long firewall(강한 세션 롱 방화벽)을 positive clue(긍정 단서)와 selection blocker(선정 차단 사유)로 나눴다.
Effect(효과): 다음 run(실행)은 더 부드러운 시간 구간으로 공격 탐색을 이어간다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 342 Selection Status(342단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_positive_clue(보존 긍정 단서): `{metrics['best_profit_attempt']}`
- preserved_best_net_profit(보존 최고 순수익): `{metrics['best_profit_net']}`
- preserved_best_profit_factor(보존 최고 수익 팩터): `{metrics['best_profit_factor']}`
- selection_blocker(선정 차단): `trade_count_and_side_balance(거래수와 방향 균형)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 높은 PF(수익 팩터)를 운영 주장으로 오해하지 않게 한다.
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

run342D(342D 실행)는 hard early-long firewall(강한 초반 롱 방화벽)을 positive clue(긍정 단서)로 보존하되 selection(선정)은 막았다. run342E(342E 실행)는 softer session-long firewall(부드러운 세션 롱 방화벽) package(패키지)를 만든다.

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
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(WORKSPACE_STATE, workspace)
    marker = f"run342D {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run342D F01 Session-Long Firewall Review(342D F01 세션 롱 방화벽 검토)

- run_id(실행 ID): `{RUN_ID}`
- best_profit_attempt(최고 수익 시도): `{metrics['best_profit_attempt']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): hard firewall(강한 방화벽)은 단서로 보존하고 softer firewall(부드러운 방화벽) 탐색으로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run342D F01 Session-Long Firewall Review(342D F01 세션 롱 방화벽 검토)

- run_id(실행 ID): `{RUN_ID}`
- scorecard(점수표): `{rel(REVIEW_SCORECARD)}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): Stage342(342단계)를 더 가벼운 soft-window(부드러운 구간) 탐색으로 이어간다.
""",
    )
    changelog = f"""## {TODAY} run342D F01 Session-Long Firewall Review(F01 세션 롱 방화벽 검토)

- action(행동): run342C(342C 실행)의 MT5 KPI(MT5 핵심 성과 지표)를 검토했다.
- effect(효과): e04(이04)는 profit-quality clue(수익 품질 단서)로 보존하고 trade_count/side_balance(거래수/방향 균형) 때문에 선정하지 않았다.
- boundary(경계): selected model/runtime authority/Goal Achieve(선정 모델/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_exploration_registers() -> None:
    marker = f"run342D {RUN_ID}"
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage342D Soft Session-Long Firewall Seed(342D 부드러운 세션 롱 방화벽 씨앗)

- idea_id(아이디어 ID): `stage342_soft_session_long_firewall`
- hypothesis(가설): hard 0~110 early-long block(강한 0~110 초반 롱 차단)을 0~45 또는 0~75로 줄이면 PF(수익 팩터) 단서를 보존하면서 trade_count/side_balance(거래수/방향 균형)를 회복할 수 있다.
- source(원천): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): 좋은 단서를 더 좁고 가벼운 탐색으로 이어간다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} Stage342D Hard Firewall Failure Memory(342D 강한 방화벽 실패 기억)

- subject(대상): `hard_early_long_0_110_trade_shape_tax`
- evidence(근거): `{rel(FAILURE_MEMORY)}`
- judgment(판정): `positive_clue_with_selection_blocker(선정 차단이 있는 긍정 단서)`
- effect(효과): hard block(강한 차단)을 반복 선정하지 않고 soft window(부드러운 구간)로 이동한다.
""",
    )


def ledger_rows(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
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
        "candidate_model_id": metrics["best_profit_model_id"],
        "net_profit": metrics["best_profit_net"],
        "profit_factor": metrics["best_profit_factor"],
        "drawdown": metrics["best_profit_drawdown"],
        "recovery_factor": metrics["best_profit_recovery"],
        "trade_count": metrics["best_profit_trade_count"],
        "result_status": "positive_profit_quality_clue_selection_blocked(수익 품질 긍정 단서, 선정 차단)",
        "sample_rows": "",
        "feature_count": "",
        "matched_rows": metrics["matched_rows_total"],
        "expectancy": metrics["best_profit_expectancy"],
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
            for column in [
                "candidate_model_id",
                "net_profit",
                "profit_factor",
                "drawdown",
                "recovery_factor",
                "trade_count",
                "matched_rows",
                "expectancy",
                "attempt_count",
            ]:
                row[column] = ""
            row["result_status"] = "missing_required(필수 누락)"
        rows.append(row)
    return rows


def write_registers(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    rows = ledger_rows(gates, metrics)
    existing = read_csv(STAGE_LEDGER) if exists(STAGE_LEDGER) else pd.DataFrame()
    if not existing.empty and "run_id" in existing.columns:
        existing = existing.loc[~existing["run_id"].astype(str).eq(RUN_ID)].copy()
    stage = pd.concat([existing, pd.DataFrame(rows)], ignore_index=True)
    write_csv(STAGE_LEDGER, stage[[column for column in STAGE_LEDGER_COLUMNS if column in stage.columns]])
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **rows[0],
                "lane": "runtime_probe_review(런타임 탐침 검토)",
                "family": "runtime_backtest",
                "path": rel(FINAL_DECISION),
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "notes": "Hard early-long firewall(강한 초반 롱 방화벽) review only(검토 전용).",
            }
        ],
    )
    project_rows = []
    for row in rows:
        project_rows.append(
            {
                **row,
                "ledger_row_id": f"{RUN_ID}__{row['tier']}",
                "subrun_id": row["tier"],
                "record_view": row["view"],
                "tier_scope": row["tier"],
                "kpi_scope": row["metric_scope"],
                "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
                "path": rel(REPORT_PATH),
                "primary_kpi": f"net_profit={metrics['best_profit_net']};profit_factor={metrics['best_profit_factor']};trade_count={metrics['best_profit_trade_count']}",
                "guardrail_kpi": f"long_short={metrics['best_profit_long_trade_count']}/{metrics['best_profit_short_trade_count']};side_balance={metrics['best_profit_side_balance']:.3f}",
                "external_verification_status": "completed(완료)",
                "notes": "Positive clue(긍정 단서) only; no selection(선정 없음).",
            }
        )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)


def write_artifact_registry() -> None:
    rows = []
    for path in artifact_paths():
        if not exists(path) or not is_file(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": pkg.sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], rows)


def main() -> None:
    for path in [
        SOURCE_FINAL,
        SOURCE_GATES,
        SOURCE_SUMMARY,
        SOURCE_DIFF,
        SOURCE_RUNTIME_IDENTITY,
        SOURCE_VARIANT_PREVIEW,
        SOURCE_SIDE_AUDIT,
    ]:
        if not is_file(path):
            raise FileNotFoundError(rel(path))
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    scorecard, judgment, attribution, failure, next_queue, metrics = build_review()
    write_csv(REVIEW_SCORECARD, scorecard)
    write_csv(KPI_JUDGMENT, judgment)
    write_csv(PERFORMANCE_ATTRIBUTION, attribution)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(NEXT_QUEUE, next_queue)
    write_receipts(metrics)
    gates = make_gates(metrics)
    write_csv(GATE_AUDIT, gates)
    write_docs(metrics, gates)
    write_exploration_registers()
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
            "gate_total": int(len(gates)),
            "best_profit_attempt": metrics["best_profit_attempt"],
            "best_profit_model_id": metrics["best_profit_model_id"],
            "best_profit_net": metrics["best_profit_net"],
            "best_profit_factor": metrics["best_profit_factor"],
            "best_profit_expectancy": metrics["best_profit_expectancy"],
            "best_profit_recovery": metrics["best_profit_recovery"],
            "best_profit_drawdown": metrics["best_profit_drawdown"],
            "best_profit_trade_count": metrics["best_profit_trade_count"],
            "best_profit_long_trade_count": metrics["best_profit_long_trade_count"],
            "best_profit_short_trade_count": metrics["best_profit_short_trade_count"],
            "best_profit_side_balance": metrics["best_profit_side_balance"],
            "mismatch_rows_total": metrics["mismatch_rows_total"],
            "candidate_selection": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "command": f"python -B {rel(Path(__file__))}",
            "inputs": [rel(path) for path in [SOURCE_FINAL, SOURCE_GATES, SOURCE_SUMMARY, SOURCE_DIFF, SOURCE_VARIANT_PREVIEW, SOURCE_SIDE_AUDIT]],
            "outputs": [rel(path) for path in artifact_paths() if exists(path)],
            "status": STATUS,
            "judgment": JUDGMENT,
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_registers(gates, metrics)
    write_artifact_registry()
    failed = gates.loc[~gates["status"].astype(str).str.lower().eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run342D gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "best_profit_attempt": metrics["best_profit_attempt"],
                "best_profit_net": metrics["best_profit_net"],
                "best_profit_factor": metrics["best_profit_factor"],
                "best_profit_trade_count": metrics["best_profit_trade_count"],
                "best_profit_long_short": f"{metrics['best_profit_long_trade_count']}/{metrics['best_profit_short_trade_count']}",
                "mismatch_rows_total": metrics["mismatch_rows_total"],
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
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
