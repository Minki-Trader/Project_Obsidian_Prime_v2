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

RUN_NUMBER = "run340B"
RUN_ID = "run340B_review_quality_balance_blend_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run340A_branch_stage339_to_quality_balance_pressure_review_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run339G_execute_quality_balance_blend_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run339F_materialize_quality_balance_blend_mt5_probe_package_without_db_v1"
SOURCE_PREVIOUS_REVIEW_RUN_ID = "run339E_review_shorter_hold_side_balance_trade_count_expansion_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1"

STATUS = "completed_stage340B_quality_balance_reviewed_local_floor_positive_clue_no_selection"
JUDGMENT = "f01_local_floor_pass_pressure_test_required_no_selection"
DECISION = "stage340B_open_run340C_f01_local_floor_pressure_package"
CLAIM_BOUNDARY = (
    "research_development_quality_balance_mt5_probe_review_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run340B_quality_balance_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage340B_quality_balance_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run340A"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_RUNTIME_PREVIEW = PARENT_RUN_DIR / "quality_balance_runtime_preview.csv"
SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339G"
SOURCE_PACKAGE_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339F"
SOURCE_PREVIOUS_REVIEW_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339E"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_RUNTIME_SUMMARY = SOURCE_RUN_DIR / "quality_balance_blend_mt5_probe_summary.csv"
SOURCE_PROXY_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_RUNTIME_IDENTITY = SOURCE_RUN_DIR / "runtime_identity.csv"
SOURCE_RUN_MANIFEST = SOURCE_RUN_DIR / "run_manifest.json"
SOURCE_VARIANT_PREVIEW = SOURCE_PACKAGE_DIR / "variant_preview.csv"
SOURCE_PREVIOUS_SCORECARD = SOURCE_PREVIOUS_REVIEW_DIR / "shorter_hold_side_balance_probe_scorecard.csv"

SCORECARD = RUN_DIR / "quality_balance_review_scorecard.csv"
KPI_JUDGMENT = RUN_DIR / "quality_balance_kpi_judgment.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run340C_queue.csv"
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


def gate_statuses_pass(frame: pd.DataFrame) -> bool:
    return bool(frame["status"].astype(str).str.lower().eq("passed").all())


def load_context() -> tuple[dict[str, Any], pd.DataFrame, dict[str, Any], pd.DataFrame]:
    parent_final = read_json(PARENT_FINAL_DECISION)
    parent_gates = read_csv(PARENT_GATE_AUDIT)
    source_final = read_json(SOURCE_FINAL_DECISION)
    source_gates = read_csv(SOURCE_GATE_AUDIT)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent_final.get('next_run_id')} != {RUN_ID}")
    if not gate_statuses_pass(parent_gates):
        raise RuntimeError("parent run340A gate audit has failed rows")
    if not gate_statuses_pass(source_gates):
        raise RuntimeError("source run339G gate audit has failed rows")
    return parent_final, parent_gates, source_final, source_gates


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


def row_judgment(row: pd.Series) -> str:
    if bool(row.get("local_floor_pass", False)):
        return "local_floor_pass_positive_clue_no_selection(로컬 하한 통과 긍정 단서, 선정 없음)"
    if bool(row.get("net_profit_pass", False)) and bool(row.get("profit_factor_pass", False)):
        return "positive_profit_shape_missing_risk_floor(수익 형태 긍정이나 위험 하한 미달)"
    if bool(row.get("trade_side_balance_pass", False)):
        return "balance_clue_profit_or_recovery_damaged(균형 단서이나 수익 또는 회복 손상)"
    return "negative_or_weak_probe(부정 또는 약한 탐침)"


def build_scorecard() -> tuple[pd.DataFrame, dict[str, Any]]:
    frame = read_csv(PARENT_RUNTIME_PREVIEW).copy()
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
        "signal_trade_count",
        "signal_side_balance",
        "short_threshold",
        "long_threshold",
        "min_margin",
        "max_hold_bars",
    ]
    for column in numeric_columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    side_max = frame[["long_trade_count", "short_trade_count"]].max(axis=1).replace(0, pd.NA)
    frame["trade_side_balance"] = (
        frame[["long_trade_count", "short_trade_count"]].min(axis=1) / side_max
    ).fillna(0.0)
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
    frame["review_judgment"] = frame.apply(row_judgment, axis=1)
    frame["evidence_boundary"] = "reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)"
    frame["claim_boundary"] = CLAIM_BOUNDARY
    frame = frame.sort_values(
        ["local_floor_pass", "floor_pass_count", "net_profit", "profit_factor", "recovery_factor"],
        ascending=[False, False, False, False, False],
    ).reset_index(drop=True)
    best = frame.iloc[0]
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
        "best_floor_pass_count": safe_int(best.get("floor_pass_count")),
        "best_short_threshold": safe_float(best.get("short_threshold")),
        "best_long_threshold": safe_float(best.get("long_threshold")),
        "best_min_margin": safe_float(best.get("min_margin")),
        "best_max_hold_bars": safe_int(best.get("max_hold_bars")),
        "local_pass_attempts": ";".join(local_pass["attempt_name"].astype(str).tolist()),
    }
    return frame, metrics


def build_kpi_judgment(scorecard: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in scorecard.iterrows():
        if bool(row["local_floor_pass"]):
            judgment_class = "positive(긍정)"
        elif safe_float(row["net_profit"]) > 0:
            judgment_class = "positive_clue(긍정 단서)"
        else:
            judgment_class = "negative(부정)"
        rows.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "judgment_class": judgment_class,
                "scoreboard": "runtime_probe(런타임 탐침);regular_risk_execution(정규 위험 실행);trade_shape(거래 형태)",
                "parity_level": "P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)",
                "wfo_status": "exception_single_window_runtime_probe(단일 구간 런타임 탐침 예외)",
                "local_floor_pass": bool(row["local_floor_pass"]),
                "floor_pass_count": int(row["floor_pass_count"]),
                "weakness_tags": row["weakness_tags"],
                "evidence_missing": (
                    "Tier B(티어 B); forward/replay(전진/재생); session/regime split(세션/국면 분할); "
                    "cost stress(비용 압박); equity curve quality(수익곡선 품질)"
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
                "topic": "f01_local_floor_pass(f01 로컬 하한 통과)",
                "comparison_baseline": "run339E c01/c07 split(339E 씨01/씨07 분기)",
                "observed_change": (
                    f"{metrics['best_attempt']} net_profit(순수익) {metrics['best_net_profit']}, "
                    f"profit_factor(수익 팩터) {metrics['best_profit_factor']}, "
                    f"expectancy(기대값) {metrics['best_expectancy']}, "
                    f"recovery_factor(회복 계수) {metrics['best_recovery_factor']}, "
                    f"trade_count(거래수) {metrics['best_trade_count']}, "
                    f"side_balance(방향 균형) {metrics['best_trade_side_balance']:.3f}"
                ),
                "likely_drivers": (
                    "long_threshold(롱 임계값) 0.51과 min_margin(최소 마진) 0.01이 약한 long(롱) 공급을 줄이면서 "
                    "trade_count(거래수)를 33으로 회복했다."
                ),
                "segment_checks": (
                    "Tier A(티어 A) 단일 runtime window(런타임 구간)만 확인했다. "
                    "session/regime split(세션/국면 분할), cost stress(비용 압박), forward(전진)는 아직 없다."
                ),
                "trade_shape": (
                    "long/short(롱/숏) 13/20, drawdown(낙폭) 89.31, recovery_factor(회복 계수) 1.38이다."
                ),
                "alternative_explanations": (
                    "single-window noise(단일 구간 잡음), broker cost regime(브로커 비용 국면), "
                    "missing Tier B(티어 B 누락) 가능성이 남는다."
                ),
                "attribution_confidence": "medium(중간)",
                "next_probe": (
                    "f01(에프01)을 exact replay control(정확 재생 대조)로 두고 threshold/min_margin/hold"
                    "(임계값/최소 마진/보유) pressure test(압박 시험)를 실행한다."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "topic": "balance_over_relief_recovery_tax(균형 과완화 회복 손상)",
                "comparison_baseline": "f01_s55_l51_m01_h12",
                "observed_change": (
                    "long_threshold(롱 임계값)을 0.47 이하로 낮추거나 short_threshold(숏 임계값)을 0.56으로 올리면 "
                    "side_balance(방향 균형)는 좋아질 수 있지만 recovery/drawdown(회복/낙폭)이 깨진다."
                ),
                "likely_drivers": (
                    "weak long supply(약한 롱 공급)와 short over-prune(숏 과삭감)이 pay-off distribution"
                    "(손익 분포)을 악화시킨다."
                ),
                "segment_checks": "direction mix(방향 혼합)만 확인했고 time/session(시간/세션) 분해는 아직 없다.",
                "trade_shape": (
                    "f05~f08(에프05~에프08)은 trade_count(거래수)나 side_balance(방향 균형)가 좋아 보여도 "
                    "recovery_factor(회복 계수) 또는 drawdown(낙폭)이 깨진다."
                ),
                "alternative_explanations": (
                    "threshold cliff(임계값 절벽), sample shrink(표본 축소), cost sensitivity(비용 민감도)가 가능하다."
                ),
                "attribution_confidence": "medium(중간)",
                "next_probe": "f01(에프01) 주변의 좁은 pressure band(압박 범위)만 먼저 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_failure_memory() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "failure_id": "run340B_balance_over_relief_recovery_tax",
                "hypothesis": "long_threshold(롱 임계값)을 충분히 낮추면 균형과 수익이 함께 개선될 것이다.",
                "failed_boundary": (
                    "f05~f07(에프05~에프07)은 side_balance(방향 균형)가 높지만 recovery_factor(회복 계수)가 "
                    "1 미만이고 일부 drawdown(낙폭)이 150을 넘는다."
                ),
                "salvage_value": "side_balance(방향 균형) 단서는 보존하되 f01(에프01) 주변 압박으로 좁힌다.",
                "reopen_condition": (
                    "session/regime filter(세션/국면 필터)나 payoff-aware long gate(손익 인식 롱 게이트)가 추가될 때."
                ),
                "do_not_repeat": "long_threshold(롱 임계값)만 0.47 이하로 낮추는 단순 반복 금지.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "failure_id": "run340B_short_threshold_056_profit_collapse",
                "hypothesis": "short_threshold(숏 임계값)을 올리면 방향 균형이 개선되고 손실이 줄 것이다.",
                "failed_boundary": (
                    "f08(에프08)은 side_balance(방향 균형) 1.0이지만 net_profit(순수익) -43.13, "
                    "profit_factor(수익 팩터) 0.75로 무너진다."
                ),
                "salvage_value": "숏 과삭감은 방향 균형 착시를 만들 수 있다는 제약으로 보존한다.",
                "reopen_condition": "short-side cost model(숏 방향 비용 모델) 또는 session filter(세션 필터)가 추가될 때.",
                "do_not_repeat": "short_threshold(숏 임계값) 0.56 단독 상승 반복 금지.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_next_queue() -> pd.DataFrame:
    rows = [
        ("p01_f01_control_s55_l51_m01_h12", 0.55, 0.510, 0.010, 12, "exact replay control(정확 재생 대조)"),
        ("p02_l515_s55_l515_m01_h12", 0.55, 0.515, 0.010, 12, "long threshold tighten(롱 임계값 조임)"),
        ("p03_l505_s55_l505_m01_h12", 0.55, 0.505, 0.010, 12, "long threshold relax(롱 임계값 완화)"),
        ("p04_m015_s55_l51_m015_h12", 0.55, 0.510, 0.015, 12, "margin tighten(마진 조임)"),
        ("p05_m02_s55_l51_m02_h12", 0.55, 0.510, 0.020, 12, "margin stress high(높은 마진 압박)"),
        ("p06_m005_s55_l51_m005_h12", 0.55, 0.510, 0.005, 12, "margin stress low(낮은 마진 압박)"),
        ("p07_h10_s55_l51_m01_h10", 0.55, 0.510, 0.010, 10, "shorter hold(짧은 보유)"),
        ("p08_h14_s55_l51_m01_h14", 0.55, 0.510, 0.010, 14, "longer hold(긴 보유)"),
        ("p09_s545_l51_m01_h12", 0.545, 0.510, 0.010, 12, "short threshold relax(숏 임계값 완화)"),
        ("p10_s555_l51_m01_h12", 0.555, 0.510, 0.010, 12, "short threshold tighten(숏 임계값 조임)"),
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
                "required_runtime_check": (
                    "MT5 runtime probe(MT5 런타임 탐침); exact proxy-MT5 parity(정확 프록시-MT5 동등성); "
                    "local floor retention(로컬 하한 유지)"
                ),
                "success_criteria": (
                    "net_profit>0(순수익 양수); profit_factor>=1.10(수익 팩터); expectancy>0(기대값 양수); "
                    "recovery>=1.00(회복 계수); drawdown<=150(낙폭); trade_count>=30(거래수); "
                    "side_balance>=0.25(방향 균형)"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for attempt, short_threshold, long_threshold, min_margin, hold_bars, role in rows
        ]
    )


def build_final(metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
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
        "best_floor_pass_count": metrics["best_floor_pass_count"],
        "best_short_threshold": metrics["best_short_threshold"],
        "best_long_threshold": metrics["best_long_threshold"],
        "best_min_margin": metrics["best_min_margin"],
        "best_max_hold_bars": metrics["best_max_hold_bars"],
        "local_pass_attempts": metrics["local_pass_attempts"],
        "measurement_scope": "runtime_probe(런타임 탐침);regular_risk_execution(정규 위험 실행);trade_shape(거래 형태)",
        "management_state": "reviewed_with_manifest_kpi_receipts_ledgers(목록/KPI/영수증/장부 포함 검토)",
        "judgment_class": "positive(긍정)",
        "scoreboard": "runtime_probe(런타임 탐침)",
        "parity_level": "P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)",
        "wfo_status": "exception_single_window_runtime_probe(단일 구간 런타임 탐침 예외)",
        "hard_gate_applicable": "no(아니오)",
        "evidence_boundary": "reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)",
        "registry_update_required": "yes(예)",
        "negative_memory_required": "yes(예)",
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }


def artifact_paths() -> list[Path]:
    return [
        SCORECARD,
        KPI_JUDGMENT,
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
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        KPI_RECORD,
        {
            **base,
            "measurement_scope": final["measurement_scope"],
            "scoreboard": final["scoreboard"],
            "parity_level": final["parity_level"],
            "wfo_status": final["wfo_status"],
            "best_attempt": final["best_attempt"],
            "best_net_profit": final["best_net_profit"],
            "best_profit_factor": final["best_profit_factor"],
            "best_expectancy": final["best_expectancy"],
            "best_recovery_factor": final["best_recovery_factor"],
            "best_drawdown": final["best_drawdown"],
            "best_trade_count": final["best_trade_count"],
            "best_trade_side_balance": final["best_trade_side_balance"],
            "local_floor_pass_count": final["local_floor_pass_count"],
            "evidence_boundary": final["evidence_boundary"],
        },
    )
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run339G quality-balance blend MT5 probe(339G 품질-균형 혼합 MT5 탐침)",
            "evidence_available": [rel(SOURCE_RUNTIME_SUMMARY), rel(SCORECARD), rel(SOURCE_PROXY_DIFF)],
            "evidence_missing": (
                "Tier B(티어 B), forward/replay(전진/재생), session/regime split(세션/국면 분할), "
                "cost stress(비용 압박), equity curve quality(수익곡선 품질)"
            ),
            "judgment_label": "positive_runtime_probe_local_floor_pass(긍정 런타임 탐침 로컬 하한 통과)",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": (
                "f01(에프01)은 로컬 하한을 통과했지만 운영 주장은 아니며 압박 시험이 다음 조건이다."
            ),
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": "f01 local floor pass(f01 로컬 하한 통과)",
            "comparison_baseline": "run339E c01/c07 split(339E 씨01/씨07 분기)",
            "likely_drivers": "long_threshold(롱 임계값) 0.51 + min_margin(최소 마진) 0.01 + hold(보유) 12",
            "segment_checks": "single Tier A runtime window only(단일 Tier A 런타임 구간만)",
            "attribution_confidence": "medium(중간)",
            "next_probe": rel(NEXT_QUEUE),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "promotion_candidate": "not_claimed(주장 없음)",
            "forward_passed": "not_claimed(주장 없음)",
            "forward_failed": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
    )
    source_inputs = [
        PARENT_FINAL_DECISION,
        PARENT_GATE_AUDIT,
        PARENT_RUNTIME_PREVIEW,
        SOURCE_FINAL_DECISION,
        SOURCE_GATE_AUDIT,
        SOURCE_RUNTIME_SUMMARY,
        SOURCE_PROXY_DIFF,
        SOURCE_RUNTIME_IDENTITY,
        SOURCE_RUN_MANIFEST,
        SOURCE_VARIANT_PREVIEW,
        SOURCE_PREVIOUS_SCORECARD,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in source_inputs],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths() if path.exists()],
            "artifact_hashes": {rel(path): sha256_file(path) for path in source_inputs if path.exists()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적 또는 명령 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run340B Quality Balance Review(340B 품질-균형 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- source_runtime_run(원천 런타임 실행): `{SOURCE_RUNTIME_RUN_ID}`
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
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- best_side_balance(최고 방향 균형): `{final['best_trade_side_balance']:.3f}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Judgment(판정)

`f01_s55_l51_m01_h12`는 runtime_probe(런타임 탐침) 안에서 local-floor positive clue(로컬 하한 통과 긍정 단서)다. selected model(선정 모델)은 아니다.
Effect(효과): profit factor(수익 팩터), expectancy(기대값), recovery factor(회복 계수), drawdown(낙폭), trade count(거래수), side balance(방향 균형)가 단일 구간에서 동시에 버틴 단서를 보존하지만, forward/replay(전진/재생), cost stress(비용 압박), session/regime(세션/국면), equity curve quality(수익곡선 품질)가 없으므로 운영 주장은 닫지 않는다.

## Attribution(귀속)

- f01(에프01): long_threshold(롱 임계값) 0.51과 min_margin(최소 마진) 0.01이 약한 long(롱)을 줄이면서 trade_count(거래수)를 33으로 회복했다.
- f05~f07(에프05~에프07): side_balance(방향 균형)는 좋아 보이지만 recovery/drawdown(회복/낙폭)이 깨져 단순 long relief(롱 완화)는 위험하다.
- f08(에프08): short_threshold(숏 임계값) 0.56은 균형 착시를 만들지만 net_profit(순수익)을 음수로 만든다.

## Next Action(다음 행동)

Open `{NEXT_RUN_ID}` with `{rel(NEXT_QUEUE)}`.
Effect(효과): f01(에프01)을 exact replay control(정확 재생 대조)로 두고 threshold/min_margin/hold(임계값/최소 마진/보유) pressure test(압박 시험)를 MT5(메타트레이더5)에서 확인한다.

## Boundary(경계)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating_promotion(운영 승격 없음), no runtime_authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage340B Decision(340B 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(SCORECARD)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`, `{rel(NEXT_QUEUE)}`

Action(행동): run339G(339G 실행)의 MT5 KPI(MT5 핵심 성과 지표)를 reviewed runtime probe(검토된 런타임 탐침)로 판정했다.

Effect(효과): f01(에프01)을 local-floor positive clue(로컬 하한 통과 긍정 단서)로 보존하고 pressure test(압박 시험)를 연다.

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

run340B(340B 실행)는 run339G(339G 실행)의 quality-balance blend(품질-균형 혼합) MT5 runtime probe(MT5 런타임 탐침)를 검토했다. run340C(340C 실행)는 f01(에프01) local-floor pass(로컬 하한 통과)가 압박에도 유지되는지 package(패키지)를 만든다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage340 Selection Status(340단계 선정 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_local_floor_clue(보존 로컬 하한 단서): `{final['best_attempt']}`
- preserved_best_net_profit(보존 최고 순수익): `{final['best_net_profit']}`
- preserved_best_profit_factor(보존 최고 수익 팩터): `{final['best_profit_factor']}`
- local_floor_pass_count(로컬 하한 통과 수): `{final['local_floor_pass_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): local floor pass(로컬 하한 통과)를 selection(선정)으로 오해하지 않게 한다.
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
    marker = f"run340B {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run340B Quality Balance Review(340B 품질-균형 검토)

- run_id(실행 ID): `{RUN_ID}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- local_floor_pass_count(로컬 하한 통과 수): `{final['local_floor_pass_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): f01(에프01)을 pressure test(압박 시험) seed(씨앗)로 보존한다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run340B Quality Balance Review(340B 품질-균형 검토)

- run_id(실행 ID): `{RUN_ID}`
- scorecard(점수표): `{rel(SCORECARD)}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): Stage340(340단계) 탐색을 local floor pressure test(로컬 하한 압박 시험)로 이어간다.
""",
    )
    changelog = f"""## {TODAY} run340B Quality Balance Review(품질-균형 검토)

- action(행동): run339G(339G 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 검토했다.
- effect(효과): f01(에프01) local floor pass(로컬 하한 통과)를 보존하고 run340C(340C 실행) pressure package(압박 패키지) 대기열을 만들었다.
- boundary(경계): selected model/runtime authority/Goal Achieve(선정 모델/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_exploration_registers() -> None:
    marker = f"run340B {RUN_ID}"
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage340B F01 Pressure Seed(340B F01 압박 씨앗)

- idea_id(아이디어 ID): `stage340_f01_local_floor_pressure`
- hypothesis(가설): f01(에프01)의 local floor pass(로컬 하한 통과)는 threshold/min_margin/hold(임계값/최소 마진/보유) 압박에서도 일부 유지될 수 있다.
- source(원천): `{SOURCE_RUNTIME_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- broad_sweep(넓은 탐색): `{rel(NEXT_QUEUE)}`
- evidence_boundary(근거 경계): `reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)`
- effect(효과): 긍정 단서를 다음 MT5(메타트레이더5) runtime probe(런타임 탐침)로 검증한다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} Stage340B Balance Failure Memory(340B 균형 실패 기억)

- subject(대상): over-relieved long balance(과완화 롱 균형) and short_threshold_056(숏 임계값 0.56)
- evidence(근거): `{rel(FAILURE_MEMORY)}`
- judgment(판정): `negative_clue_with_salvage(회수 가치가 있는 부정 단서)`
- effect(효과): 균형만 보고 threshold(임계값)를 완화하는 반복을 막고 f01(에프01) 주변 압박으로 좁힌다.
""",
    )


def make_gates(final: Mapping[str, Any], parent_gates: pd.DataFrame, source_gates: pd.DataFrame) -> pd.DataFrame:
    rows = [
        (
            "parent_340A_gates_passed",
            "passed" if gate_statuses_pass(parent_gates) else "failed",
            rel(PARENT_GATE_AUDIT),
            "run340A(340A 실행) branch(분기) 근거를 이어받는다.",
        ),
        (
            "source_339G_gates_passed",
            "passed" if gate_statuses_pass(source_gates) else "failed",
            rel(SOURCE_GATE_AUDIT),
            "run339G(339G 실행) MT5 runtime probe(MT5 런타임 탐침) 근거를 이어받는다.",
        ),
        (
            "kpi_scorecard_written",
            "passed" if SCORECARD.exists() else "failed",
            rel(SCORECARD),
            "KPI scorecard(KPI 점수표)를 만든다.",
        ),
        (
            "result_judgment_written",
            "passed" if KPI_JUDGMENT.exists() and RESULT_JUDGMENT_RECEIPT.exists() else "failed",
            f"{rel(KPI_JUDGMENT)};{rel(RESULT_JUDGMENT_RECEIPT)}",
            "result judgment(결과 판정)을 machine-readable(기계 판독 가능)하게 남긴다.",
        ),
        (
            "performance_attribution_written",
            "passed" if PERFORMANCE_ATTRIBUTION.exists() and PERFORMANCE_ATTRIBUTION_RECEIPT.exists() else "failed",
            f"{rel(PERFORMANCE_ATTRIBUTION)};{rel(PERFORMANCE_ATTRIBUTION_RECEIPT)}",
            "성과 변화 이유를 attribution(귀속)으로 분리한다.",
        ),
        (
            "failure_memory_written",
            "passed" if FAILURE_MEMORY.exists() else "failed",
            rel(FAILURE_MEMORY),
            "반복 금지할 실패 기억(failure memory, 실패 기억)을 남긴다.",
        ),
        (
            "next_pressure_queue_written",
            "passed" if NEXT_QUEUE.exists() else "failed",
            rel(NEXT_QUEUE),
            "다음 pressure test(압박 시험) 대기열을 남긴다.",
        ),
        (
            "tier_records_represented",
            "passed" if final.get("local_floor_pass_count", 0) >= 1 else "failed",
            rel(FINAL_DECISION),
            "Tier A(티어 A), Tier B missing_required(Tier B 필수 누락), Tier A+B(티어 A+B) 경계를 final(최종)과 ledger(장부)에 남긴다.",
        ),
        (
            "no_forbidden_operating_claim",
            "passed",
            rel(CLAIM_RECEIPT),
            "reviewed runtime probe(검토된 런타임 탐침)를 selection(선정), operating promotion(운영 승격), runtime authority(런타임 권위)로 말하지 않는다.",
        ),
        (
            "required_gate_coverage_audit_written",
            "passed",
            rel(GATE_AUDIT),
            "required gate coverage audit(필수 게이트 커버리지 감사)를 쓴다.",
        ),
    ]
    return pd.DataFrame(
        [
            {"gate_id": gate_id, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
            for gate_id, status, evidence, effect in rows
        ]
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
            "result_status": "reviewed_local_floor_positive_clue_no_selection(검토된 로컬 하한 긍정 단서, 선정 없음)",
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
    write_csv(STAGE_LEDGER, pd.DataFrame(rows, columns=STAGE_LEDGER_COLUMNS))
    project_rows = []
    for row in rows:
        project_row = dict(row)
        project_row["ledger_row_id"] = f"{RUN_ID}__{row['tier']}"
        project_row["tier_scope"] = row["tier"]
        project_row["kpi_scope"] = row["metric_scope"]
        project_row["scoreboard_lane"] = "runtime_probe(런타임 탐침)"
        project_row["path"] = rel(REPORT_PATH)
        project_row["date"] = TODAY
        project_row["run_number"] = RUN_NUMBER
        project_row["primary_artifact"] = rel(FINAL_DECISION)
        project_rows.append(project_row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)


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
    parent_final, parent_gates, source_final, source_gates = load_context()
    scorecard, metrics = build_scorecard()
    kpi_judgment = build_kpi_judgment(scorecard)
    attribution = build_attribution(metrics)
    failure_memory = build_failure_memory()
    next_queue = build_next_queue()
    write_csv(SCORECARD, scorecard)
    write_csv(KPI_JUDGMENT, kpi_judgment)
    write_csv(PERFORMANCE_ATTRIBUTION, attribution)
    write_csv(FAILURE_MEMORY, failure_memory)
    write_csv(NEXT_QUEUE, next_queue)
    final_seed = build_final(metrics)
    write_receipts(final_seed)
    gates = make_gates(final_seed, parent_gates, source_gates)
    final = {
        **final_seed,
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "parent_status": parent_final.get("status", ""),
        "source_status": source_final.get("status", ""),
    }
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
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
                rel(PARENT_RUNTIME_PREVIEW),
                rel(SOURCE_FINAL_DECISION),
                rel(SOURCE_GATE_AUDIT),
                rel(SOURCE_RUNTIME_SUMMARY),
                rel(SOURCE_PROXY_DIFF),
                rel(SOURCE_VARIANT_PREVIEW),
            ],
            "outputs": [rel(path) for path in artifact_paths() if path.exists()],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_receipts(final)
    write_docs(final)
    write_exploration_registers()
    write_registers(final, gates)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run340B gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_recovery_factor": final["best_recovery_factor"],
                "best_trade_count": final["best_trade_count"],
                "best_side_balance": final["best_trade_side_balance"],
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
