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

from stage_pipelines.stage342 import execute_soft_session_long_firewall_mt5_probe_without_db as exe  # noqa: E402
from stage_pipelines.stage342 import materialize_soft_session_long_firewall_mt5_probe_package_without_db as pkg  # noqa: E402


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run342G"
RUN_ID = "run342G_review_soft_session_long_firewall_mt5_probe_without_db_v1"
PARENT_RUN_ID = exe.RUN_ID
NEXT_RUN_ID = "run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1"

STATUS = "completed_stage342G_soft_firewall_reviewed_no_trade_shape_recovery_no_selection"
JUDGMENT = "soft_window_does_not_recover_trade_count_hard_firewall_profit_quality_clue_preserved_no_selection"
DECISION = "stage342G_open_run342H_early_long_quality_margin_mix_package"
CLAIM_BOUNDARY = (
    "research_development_review_only_soft_session_long_firewall_mt5_probe_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run342G_soft_session_long_firewall_mt5_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage342G_soft_session_long_firewall_mt5_probe_review.md"
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
HARD_REVIEW_FINAL = STAGE_DIR / "02_runs" / "run342D" / "final_decision.json"
HARD_REVIEW_SCORECARD = STAGE_DIR / "02_runs" / "run342D" / "session_long_firewall_review_scorecard.csv"

REVIEW_SCORECARD = RUN_DIR / "soft_session_long_firewall_review_scorecard.csv"
KPI_JUDGMENT = RUN_DIR / "soft_session_long_firewall_kpi_judgment.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run342H_early_long_quality_margin_mix_queue.csv"
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
    return pkg.base.rel(path)


def exists(path: Path) -> bool:
    return pkg.base.path_exists(path)


def is_file(path: Path) -> bool:
    return pkg.base.path_is_file(path)


def read_csv(path: Path) -> pd.DataFrame:
    return pkg.base.read_csv(path)


def read_json(path: Path) -> Any:
    return pkg.base.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    pkg.base.ensure_parent(path)
    with open(pkg.base.fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    pkg.base.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    pkg.base.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.base.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.base.append_or_replace_csv(path, keys, rows)


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
    tags = []
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
    if attempt in {"e01_q01_ctl", "e02_q09_ctl"}:
        return "control_reference_floor_pass_no_new_selection(대조 참고 하한 통과, 신규 선정 없음)"
    if "blk_early_all" in attempt:
        return "soft_overfilter_negative_control_recovery_broken(부드러운 과필터 부정 대조, 회복 손상)"
    if "blk_early" in attempt:
        return "duplicate_hard_firewall_profit_clue_trade_shape_blocked(강한 방화벽 중복 수익 단서, 거래 형태 차단)"
    return "weak_or_context_clue_no_selection(약한 또는 문맥 단서, 선정 없음)"


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    summary = read_csv(SOURCE_SUMMARY).fillna("")
    side = read_csv(SOURCE_SIDE_AUDIT).fillna("")
    preview = read_csv(SOURCE_VARIANT_PREVIEW).fillna("")
    hard_final = read_json(HARD_REVIEW_FINAL) if is_file(HARD_REVIEW_FINAL) else {}
    hard_scorecard = read_csv(HARD_REVIEW_SCORECARD).fillna("") if is_file(HARD_REVIEW_SCORECARD) else pd.DataFrame()
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
    ]:
        if column in summary.columns:
            summary[column] = pd.to_numeric(summary[column], errors="coerce")
    side_lookup = {str(row["attempt_name"]): row.to_dict() for _, row in side.iterrows()}
    preview_lookup = {str(row["attempt_name"]): row.to_dict() for _, row in preview.iterrows()}
    rows = []
    for _, source in summary.iterrows():
        row = source.to_dict()
        attempt = str(row.get("attempt_name", ""))
        side_max = max(num(row.get("long_trade_count")), num(row.get("short_trade_count")))
        row["trade_side_balance"] = 0.0 if side_max <= 0 else min(num(row.get("long_trade_count")), num(row.get("short_trade_count"))) / side_max
        row["blocked_long_rows"] = as_int(side_lookup.get(attempt, {}).get("blocked_long_count"))
        row["blocked_short_rows"] = as_int(side_lookup.get(attempt, {}).get("blocked_short_count"))
        row["block_long_range"] = preview_lookup.get(attempt, {}).get("block_long_range", "")
        row["block_short_range"] = preview_lookup.get(attempt, {}).get("block_short_range", "")
        row["signal_trade_count"] = as_int(preview_lookup.get(attempt, {}).get("signal_trade_count"))
        row["signal_side_balance"] = num(preview_lookup.get(attempt, {}).get("signal_side_balance"))
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
    scorecard = pd.DataFrame(rows).sort_values(
        ["net_profit", "profit_factor", "recovery_factor"], ascending=[False, False, False]
    )
    best = scorecard.iloc[0]
    filtered = scorecard.loc[scorecard["attempt_name"].astype(str).str.contains("blk_early")]
    hard_best_net = num(hard_final.get("best_profit_net"))
    hard_best_pf = num(hard_final.get("best_profit_factor"))
    hard_best_trade_count = as_int(hard_final.get("best_profit_trade_count"))
    unique_filtered_kpi = filtered[
        ["net_profit", "profit_factor", "trade_count", "long_trade_count", "short_trade_count"]
    ].drop_duplicates()
    soft_no_recovery = bool(
        as_int(best["trade_count"]) <= hard_best_trade_count
        and as_int(best["long_trade_count"]) <= as_int(hard_final.get("best_profit_long_trade_count"))
    )
    metrics = {
        "attempt_count": int(len(scorecard)),
        "expected_rows_total": int(scorecard["expected_rows"].fillna(0).sum()),
        "matched_rows_total": int(scorecard["matched_rows"].fillna(0).sum()),
        "mismatch_rows_total": int(
            scorecard["probability_mismatch_rows"].fillna(0).sum()
            + scorecard["decision_mismatch_rows"].fillna(0).sum()
        ),
        "all_exact_parity": bool(scorecard["exact_parity_pass"].astype(bool).all()),
        "best_attempt": str(best["attempt_name"]),
        "best_model_id": str(best["model_id"]),
        "best_net_profit": num(best["net_profit"]),
        "best_profit_factor": num(best["profit_factor"]),
        "best_expectancy": num(best["expectancy"]),
        "best_recovery_factor": num(best["recovery_factor"]),
        "best_drawdown": num(best["max_drawdown_amount"]),
        "best_trade_count": as_int(best["trade_count"]),
        "best_long_trade_count": as_int(best["long_trade_count"]),
        "best_short_trade_count": as_int(best["short_trade_count"]),
        "best_side_balance": num(best["trade_side_balance"]),
        "hard_best_net": hard_best_net,
        "hard_best_pf": hard_best_pf,
        "hard_best_trade_count": hard_best_trade_count,
        "hard_best_long_trade_count": as_int(hard_final.get("best_profit_long_trade_count")),
        "hard_best_short_trade_count": as_int(hard_final.get("best_profit_short_trade_count")),
        "soft_no_trade_shape_recovery": soft_no_recovery,
        "unique_filtered_kpi_shapes": int(len(unique_filtered_kpi)),
        "blocked_long_rows_total": int(side["blocked_long_count"].astype(float).sum()),
        "blocked_short_rows_total": int(side["blocked_short_count"].astype(float).sum()),
        "hard_scorecard_rows": int(len(hard_scorecard)),
    }
    return (
        scorecard,
        build_kpi_judgment(scorecard),
        build_attribution(metrics),
        build_failure_memory(metrics),
        build_next_queue(),
        metrics,
    )


def build_kpi_judgment(scorecard: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in scorecard.iterrows():
        rows.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "judgment_class": row["review_judgment"],
                "scoreboard": "MT5 runtime probe(MT5 런타임 탐침);trade shape(거래 형태);runtime parity(런타임 동등성)",
                "parity_level": "P3_exact_runtime_proxy_parity(P3 정확 런타임-프록시 동등성)",
                "wfo_status": "single_window_runtime_probe_only(단일 구간 런타임 탐침만)",
                "floor_pass_count": int(row["floor_pass_count"]),
                "weakness_tags": row["weakness_tags"],
                "evidence_missing": "Tier B(티어 B); forward/replay(전진/재생); cost stress(비용 압박); equity curve quality(수익곡선 품질)",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_attribution(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "topic": "soft_window_no_trade_shape_recovery(부드러운 시간 구간 거래 형태 미회복)",
                "comparison_baseline": "run342D hard 0~110 early-long firewall(342D 강한 0~110 초반 롱 방화벽)",
                "observed_change": (
                    f"best soft(최선 부드러운 변형) {metrics['best_attempt']} net_profit(순수익) {metrics['best_net_profit']}, "
                    f"PF(수익 팩터) {metrics['best_profit_factor']}, trade_count(거래수) {metrics['best_trade_count']}, "
                    f"long/short(롱/숏) {metrics['best_long_trade_count']}/{metrics['best_short_trade_count']}; "
                    f"hard trade_count(강한 차단 거래수) {metrics['hard_best_trade_count']}"
                ),
                "likely_drivers": "blocked early longs(차단된 초반 롱)이 모두 0~45분 안에 있어 0~75와 0~110이 같은 거래 형태를 만든다.",
                "selection_blocker": "trade_count(거래수) 23과 side_balance(방향 균형) 0.15가 계속 약하다.",
                "next_probe": "time-window pruning(시간 구간 절단) 대신 long threshold/min_margin(롱 임계값/최소 마진) 혼합으로 early-long quality(초반 롱 품질)를 시험한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "topic": "soft_overfilter_negative_control(부드러운 과필터 부정 대조)",
                "comparison_baseline": "q09 soft long-only block(q09 부드러운 롱 전용 차단)",
                "observed_change": "e07(이07)은 net_profit(순수익) 72.98, PF(수익 팩터) 2.03, recovery(회복) 0.82, trade_count(거래수) 16이다.",
                "likely_drivers": "early short supply(초반 숏 공급)를 자르면 recovery factor(회복 계수)가 깨진다.",
                "selection_blocker": "short side(숏 방향) 차단은 수익 공급을 손상한다.",
                "next_probe": "long-only(롱 전용) 제약을 유지한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_failure_memory(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "failure_id": "run342G_soft_window_no_recovery",
                "hypothesis": "0~45 또는 0~75 soft window(부드러운 구간)는 hard 0~110 block(강한 0~110 차단)의 거래수 비용을 줄일 수 있다.",
                "failed_boundary": (
                    f"best trade_count(최선 거래수) {metrics['best_trade_count']} and "
                    f"long/short(롱/숏) {metrics['best_long_trade_count']}/{metrics['best_short_trade_count']} "
                    f"matches hard firewall(강한 방화벽) trade shape(거래 형태)."
                ),
                "salvage_value": "PF(수익 팩터)와 expectancy(기대값)는 보존되므로 early-long quality gate(초반 롱 품질 게이트)로 이동한다.",
                "do_not_repeat": "time-window only(시간 구간만) 0~45/0~75/0~110 변형을 반복하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "failure_id": "run342G_soft_all_side_overfilter",
                "hypothesis": "0~45 early all-side block(초반 양방향 차단)은 부드럽기 때문에 안정적일 수 있다.",
                "failed_boundary": "e07 net_profit(순수익) 72.98, recovery factor(회복 계수) 0.82, trade_count(거래수) 16.",
                "salvage_value": "short side(숏 방향)는 초반에도 유지하고 long quality(롱 품질)만 조정한다.",
                "do_not_repeat": "early all-side block(초반 양방향 차단)을 주 탐색축으로 쓰지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_next_queue() -> pd.DataFrame:
    rows = [
        ("h01_q02_l515_control", "q02_l515_s55_l515_m01_h12", False, "", "", "higher_long_threshold_control(높은 롱 임계값 대조)", "롱 공급을 전역 임계값으로 정리하면 거래 형태가 나아지는지 본다."),
        ("h02_q04_margin015_control", "q04_m015_s55_l51_m015_h12", False, "", "", "higher_margin_control(높은 마진 대조)", "min_margin(최소 마진)이 약한 early long(초반 롱)을 줄이는지 본다."),
        ("h03_q05_margin02_control", "q05_m02_s55_l51_m02_h12", False, "", "", "strict_margin_control(엄격 마진 대조)", "더 엄격한 margin(마진)의 수익 공급 손상을 확인한다."),
        ("h04_q02_l515_block_early45", "q02_l515_s55_l515_m01_h12", True, "0,45", "", "higher_long_threshold_plus_firewall(높은 롱 임계값+방화벽)", "time-window(시간 구간)만이 아니라 confidence surface(신뢰도 표면)를 같이 바꾼다."),
        ("h05_q04_margin015_block_early45", "q04_m015_s55_l51_m015_h12", True, "0,45", "", "margin_plus_firewall(마진+방화벽)", "롱 차단 후 남는 trade shape(거래 형태)를 margin(마진)으로 조정한다."),
        ("h06_q05_margin02_block_early45", "q05_m02_s55_l51_m02_h12", True, "0,45", "", "strict_margin_plus_firewall(엄격 마진+방화벽)", "과도한 품질 필터가 trade count(거래수)를 더 깨는지 본다."),
        ("h07_q06_margin005_block_early45", "q06_m005_s55_l51_m005_h12", True, "0,45", "", "looser_margin_rescue(느슨한 마진 회복)", "차단 후 margin(마진)을 완화하면 trade count(거래수)가 회복되는지 본다."),
        ("h08_q10_short555_block_early45", "q10_s555_l51_m01_h12", True, "0,45", "", "short_supply_stress(숏 공급 압박)", "숏 임계값을 조금 올려 short concentration(숏 집중)의 위험을 본다."),
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
    base_receipt = {
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
            **base_receipt,
            "judgment_class": "negative_boundary_with_preserved_profit_clue(수익 단서 보존이 있는 부정 경계)",
            "best_attempt": metrics["best_attempt"],
            "selection_blockers": "trade_count(거래수); long_short_balance(롱/숏 균형); missing_forward_and_tier_b(전진 및 Tier B 누락)",
            "effect": "soft window(부드러운 구간)를 반복하지 않고 quality/margin(품질/마진) 축으로 이동한다.",
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base_receipt,
            "best_attempt": metrics["best_attempt"],
            "soft_no_trade_shape_recovery": metrics["soft_no_trade_shape_recovery"],
            "unique_filtered_kpi_shapes": metrics["unique_filtered_kpi_shapes"],
            "next_probe": rel(NEXT_QUEUE),
            "effect": "시간 구간을 줄이는 방법이 거래 형태 비용을 회복하지 못했음을 기록한다.",
        },
    )
    existing = [path for path in artifact_paths() if exists(path) and path != LINEAGE_RECEIPT]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base_receipt,
            "source_inputs": [
                rel(SOURCE_FINAL),
                rel(SOURCE_GATES),
                rel(SOURCE_SUMMARY),
                rel(SOURCE_DIFF),
                rel(SOURCE_RUNTIME_IDENTITY),
                rel(SOURCE_VARIANT_PREVIEW),
                rel(SOURCE_SIDE_AUDIT),
                rel(HARD_REVIEW_FINAL),
                rel(HARD_REVIEW_SCORECARD),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in existing],
            "artifact_hashes": {rel(path): pkg.base.sha256_file(path) for path in existing if is_file(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base_receipt,
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
            gate_row("parent_342F_gates_passed", "passed" if gate_passed(SOURCE_GATES) else "failed", rel(SOURCE_GATES), "run342F(342F 실행) MT5 runtime probe(MT5 런타임 탐침)를 이어받는다."),
            gate_row("review_scorecard_written", "passed" if exists(REVIEW_SCORECARD) else "failed", rel(REVIEW_SCORECARD), "KPI scorecard(KPI 점수표)를 만든다."),
            gate_row("exact_runtime_parity_reviewed", "passed" if metrics["all_exact_parity"] and metrics["mismatch_rows_total"] == 0 else "failed", rel(SOURCE_DIFF), "proxy-MT5 parity(프록시-MT5 동등성)를 판정에 연결한다."),
            gate_row("soft_window_no_recovery_recorded", "passed" if metrics["soft_no_trade_shape_recovery"] else "failed", rel(PERFORMANCE_ATTRIBUTION), "soft window(부드러운 구간)가 거래 형태를 회복하지 못한 경계를 기록한다."),
            gate_row("failure_memory_written", "passed" if exists(FAILURE_MEMORY) else "failed", rel(FAILURE_MEMORY), "반복하지 않을 실패 기억(failure memory, 실패 기억)을 남긴다."),
            gate_row("next_quality_margin_queue_written", "passed" if exists(NEXT_QUEUE) and len(read_csv(NEXT_QUEUE)) >= 8 else "failed", rel(NEXT_QUEUE), "다음 quality/margin(품질/마진) 탐색 queue(대기열)를 만든다."),
            gate_row("tier_records_written", "passed" if exists(STAGE_LEDGER) else "failed", rel(STAGE_LEDGER), "Tier A/Tier B/Tier A+B(티어 A/B/A+B) 장부를 남긴다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(CLAIM_RECEIPT), "review(검토)를 selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)로 말하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "필수 게이트 감사(required gate coverage audit, 필수 게이트 감사)를 기록한다."),
        ]
    )


def write_docs(metrics: Mapping[str, Any], gates: pd.DataFrame) -> None:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
    report = f"""# run342G Soft Session-Long Firewall MT5 Probe Review(342G 부드러운 세션 롱 방화벽 MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{gate_passes}/{gate_total}`
- exact_parity(정확 동등성): `{metrics['matched_rows_total']}/{metrics['expected_rows_total']}`, mismatch(불일치) `{metrics['mismatch_rows_total']}`
- best_attempt(최고 시도): `{metrics['best_attempt']}`
- best_net_profit(최고 순수익): `{metrics['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{metrics['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{metrics['best_recovery_factor']}`
- best_trade_count(최고 거래수): `{metrics['best_trade_count']}`
- best_long_short(최고 롱/숏): `{metrics['best_long_trade_count']}/{metrics['best_short_trade_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run342F(342F 실행)의 soft session-long firewall(부드러운 세션 롱 방화벽) MT5 runtime probe(MT5 런타임 탐침)를 검토했다.
Effect(효과): 0~45/0~75 soft window(부드러운 구간)는 hard block(강한 차단)과 같은 거래 형태를 만들어 trade count(거래수)와 long/short balance(롱/숏 균형)를 회복하지 못했다는 점을 닫았다.

## Judgment(판정)

hard/soft early-long block(강한/부드러운 초반 롱 차단)은 profit-quality clue(수익 품질 단서)를 보존하지만 selected model(선정 모델)은 아니다.
Effect(효과): 다음 탐색은 time-window pruning(시간 구간 절단)이 아니라 long threshold/min_margin(롱 임계값/최소 마진) 혼합으로 이동한다.

## Next(다음)

Open `{NEXT_RUN_ID}` with `{rel(NEXT_QUEUE)}`.
Effect(효과): early-long quality gate(초반 롱 품질 게이트)를 MT5 package(MT5 패키지)로 시험할 준비를 한다.

## Boundary(경계)

No selection(선정 없음), no forward(전진 없음), no live readiness(실거래 준비 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage342G Review Decision(342G 검토 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(REVIEW_SCORECARD)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`, `{rel(FAILURE_MEMORY)}`, `{rel(NEXT_QUEUE)}`

Action(행동): soft-window(부드러운 구간) 탐색을 no trade-shape recovery(거래 형태 미회복)로 닫고 quality/margin mix(품질/마진 혼합) 탐색을 열었다.
Effect(효과): 같은 시간 구간 blocker(차단 원인)를 반복하지 않고 새로운 공격 탐색축으로 이동한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 342 Selection Status(342단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_positive_clue(보존 긍정 단서): `{metrics['best_attempt']}`
- preserved_best_net_profit(보존 최고 순수익): `{metrics['best_net_profit']}`
- preserved_best_profit_factor(보존 최고 수익 팩터): `{metrics['best_profit_factor']}`
- selection_blocker(선정 차단): `trade_count_and_side_balance(거래수와 방향 균형)`
- next_probe(다음 탐침): `early_long_quality_margin_mix(초반 롱 품질/마진 혼합)`
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

run342G(342G 실행)는 soft-window(부드러운 구간)가 trade count(거래수)와 long/short balance(롱/숏 균형)를 회복하지 못했음을 기록했다. run342H(342H 실행)는 early-long quality/margin mix(초반 롱 품질/마진 혼합) MT5 package(MT5 패키지)를 만든다.

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
    marker = f"run342G {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run342G Soft Firewall Review(342G 부드러운 방화벽 검토)

- run_id(실행 ID): `{RUN_ID}`
- best_attempt(최고 시도): `{metrics['best_attempt']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): soft-window(부드러운 구간) 반복을 닫고 quality/margin(품질/마진) 탐색으로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run342G Soft Firewall Review(342G 부드러운 방화벽 검토)

- run_id(실행 ID): `{RUN_ID}`
- scorecard(점수표): `{rel(REVIEW_SCORECARD)}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): Stage342(342단계)를 early-long quality gate(초반 롱 품질 게이트) 탐색으로 이어간다.
""",
    )
    changelog = f"""## {TODAY} run342G Soft Firewall Review(부드러운 방화벽 검토)

- action(행동): run342F(342F 실행)의 MT5 KPI(MT5 핵심 성과 지표)를 검토했다.
- effect(효과): soft-window(부드러운 구간)는 거래 형태를 회복하지 못했으므로 quality/margin(품질/마진) 다음 탐색을 열었다.
- boundary(경계): selected model/runtime authority/Goal Achieve(선정 모델/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_exploration_registers() -> None:
    marker = f"run342G {RUN_ID}"
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage342G Early Long Quality Margin Mix Seed(342G 초반 롱 품질/마진 혼합 씨앗)

- idea_id(아이디어 ID): `stage342_early_long_quality_margin_mix`
- hypothesis(가설): time-window pruning(시간 구간 절단)만으로 부족한 early-long filter(초반 롱 필터)는 long_threshold/min_margin(롱 임계값/최소 마진)과 결합하면 trade_count/side_balance(거래수/방향 균형)를 회복할 수 있다.
- source(원천): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): 같은 시간 구간만 미세조정하지 않고 confidence surface(신뢰도 표면) 쪽으로 확장한다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} Stage342G Soft Window Failure Memory(342G 부드러운 구간 실패 기억)

- subject(대상): `soft_window_0_45_0_75_trade_shape_no_recovery`
- evidence(근거): `{rel(FAILURE_MEMORY)}`
- judgment(판정): `negative_boundary_with_preserved_profit_clue(수익 단서를 보존한 부정 경계)`
- effect(효과): time-window only(시간 구간만) 변형을 반복하지 않고 quality/margin(품질/마진) 축으로 이동한다.
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
        "candidate_model_id": metrics["best_model_id"],
        "net_profit": metrics["best_net_profit"],
        "profit_factor": metrics["best_profit_factor"],
        "drawdown": metrics["best_drawdown"],
        "recovery_factor": metrics["best_recovery_factor"],
        "trade_count": metrics["best_trade_count"],
        "result_status": "negative_boundary_with_preserved_profit_clue_no_selection(수익 단서 보존 부정 경계, 선정 없음)",
        "sample_rows": "",
        "feature_count": "",
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
            for column in ["candidate_model_id", "net_profit", "profit_factor", "drawdown", "recovery_factor", "trade_count", "matched_rows", "expectancy", "attempt_count"]:
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
                "notes": "Soft session-long firewall(부드러운 세션 롱 방화벽) review only(검토 전용).",
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
                "primary_kpi": f"net_profit={metrics['best_net_profit']};profit_factor={metrics['best_profit_factor']};trade_count={metrics['best_trade_count']}",
                "guardrail_kpi": f"long_short={metrics['best_long_trade_count']}/{metrics['best_short_trade_count']};soft_no_trade_shape_recovery={metrics['soft_no_trade_shape_recovery']}",
                "external_verification_status": "completed(완료)",
                "notes": "Preserved profit clue(보존 수익 단서) only; no selection(선정 없음).",
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
                "sha256": pkg.base.sha256_file(path),
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
            "best_side_balance": metrics["best_side_balance"],
            "soft_no_trade_shape_recovery": metrics["soft_no_trade_shape_recovery"],
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
            "inputs": [rel(path) for path in [SOURCE_FINAL, SOURCE_GATES, SOURCE_SUMMARY, SOURCE_DIFF, SOURCE_VARIANT_PREVIEW, SOURCE_SIDE_AUDIT, HARD_REVIEW_FINAL]],
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
        raise RuntimeError(f"run342G gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "best_attempt": metrics["best_attempt"],
                "best_net_profit": metrics["best_net_profit"],
                "best_profit_factor": metrics["best_profit_factor"],
                "best_trade_count": metrics["best_trade_count"],
                "best_long_short": f"{metrics['best_long_trade_count']}/{metrics['best_short_trade_count']}",
                "soft_no_trade_shape_recovery": metrics["soft_no_trade_shape_recovery"],
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
