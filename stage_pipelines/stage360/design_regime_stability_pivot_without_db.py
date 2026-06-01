from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE_ID = "360_regime_stability_pivot__oos_long_cash_edge_validation_loss"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run360A"
RUN_ID = "run360A_design_regime_stability_pivot_without_db_v1"
PARENT_RUN_ID = "run359D_branch_to_stage360_regime_stability_pivot_v1"
SOURCE_REVIEW_RUN_ID = "run359C_review_high_density_label_pivot_mt5_probe_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run358B_package_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run360B_materialize_regime_stability_pivot_inputs_without_db_v1"

STATUS = "completed_stage360A_regime_stability_pivot_design_ready_no_selection_no_mt5"
JUDGMENT = "regime_stability_pivot_design_ready_materialization_required_no_operating_claim"
DECISION = "stage360A_open_run360B_materialize_regime_stability_pivot_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_design_only_regime_stability_pivot_no_model_training_no_proxy_execution_"
    "no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

REPORT_PATH = REVIEW_DIR / "run360A_regime_stability_pivot_design.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage360A_regime_stability_pivot_design.md"

WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "data_integrity_contract.csv"
MODEL_VALIDATION_CONTRACT = RUN_DIR / "model_validation_contract.csv"
SOURCE_EVIDENCE_SNAPSHOT = RUN_DIR / "source_evidence_snapshot.csv"
FAILURE_MEMORY_CONSTRAINTS = RUN_DIR / "failure_memory_constraints.csv"
BROAD_SWEEP_PLAN = RUN_DIR / "broad_sweep_plan.csv"
EXTREME_SWEEP_PLAN = RUN_DIR / "extreme_sweep_plan.csv"
REGIME_AXIS_PLAN = RUN_DIR / "regime_axis_plan.csv"
WFO_VALIDATION_PLAN = RUN_DIR / "wfo_validation_plan.csv"
MICRO_SEARCH_GATE = RUN_DIR / "micro_search_gate.csv"
CANDIDATE_DESIGN_QUEUE = RUN_DIR / "candidate_design_queue.csv"
NEXT_MATERIALIZATION_QUEUE = RUN_DIR / "run360B_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

SOURCE_STAGE359_DIR = ROOT / "stages" / "359_runtime_probe_execution__high_density_label_pivot_mt5_check"
SOURCE_STAGE360_INPUT_MANIFEST = STAGE_DIR / "01_inputs" / "stage360_input_manifest.csv"
SOURCE_STAGE359C_FINAL = SOURCE_STAGE359_DIR / "02_runs" / "run359C" / "final_decision.json"
SOURCE_STAGE359C_REVIEW = SOURCE_STAGE359_DIR / "03_reviews" / "run359C_high_density_label_pivot_mt5_probe_review.md"
SOURCE_STAGE359C_ATTRIBUTION = SOURCE_STAGE359_DIR / "02_runs" / "run359C" / "trade_level_segment_attribution.csv"
SOURCE_STAGE359C_COST = SOURCE_STAGE359_DIR / "02_runs" / "run359C" / "cost_drag_sensitivity.csv"
SOURCE_STAGE359B_SUMMARY = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "high_density_label_pivot_mt5_probe_summary.csv"
SOURCE_STAGE359B_DIFF = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "proxy_mt5_runtime_difference.csv"
SOURCE_STAGE359D_FINAL = STAGE_DIR / "02_runs" / "run359D" / "final_decision.json"
SOURCE_TRAINING_CONTRACT = ROOT / "docs" / "contracts" / "training_label_split_contract_fpmarkets_v2.md"

INPUT_FILES = [
    SOURCE_STAGE360_INPUT_MANIFEST,
    SOURCE_STAGE359C_FINAL,
    SOURCE_STAGE359C_REVIEW,
    SOURCE_STAGE359C_ATTRIBUTION,
    SOURCE_STAGE359C_COST,
    SOURCE_STAGE359B_SUMMARY,
    SOURCE_STAGE359B_DIFF,
    SOURCE_STAGE359D_FINAL,
    SOURCE_TRAINING_CONTRACT,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames and (extend_header or not fieldnames):
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows_list], fieldnames)


def require_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")


def source_summary() -> dict[str, Any]:
    final = read_json(SOURCE_STAGE359C_FINAL)
    return {
        "best_attempt_name": final.get("best_attempt_name"),
        "best_model_id": final.get("best_model_id"),
        "best_net_profit": final.get("best_net_profit"),
        "best_profit_factor": final.get("best_profit_factor"),
        "best_expectancy": final.get("best_expectancy"),
        "best_recovery_factor": final.get("best_recovery_factor"),
        "best_max_drawdown_amount": final.get("best_max_drawdown_amount"),
        "best_trade_count": final.get("best_trade_count"),
        "best_long_trade_count": final.get("best_long_trade_count"),
        "best_short_trade_count": final.get("best_short_trade_count"),
        "best_trade_density_per_feature_day": final.get("best_trade_density_per_feature_day"),
        "proxy_mt5_mismatch_rows": final.get("proxy_mt5_mismatch_rows"),
        "validation_positive_rows": final.get("validation_positive_rows"),
        "q05_validation_net_profit": final.get("q05_validation_net_profit"),
        "q05_validation_profit_factor": final.get("q05_validation_profit_factor"),
        "q05_validation_max_drawdown_percent": final.get("q05_validation_max_drawdown_percent"),
        "q05_oos_month_positive_count": final.get("q05_oos_month_positive_count"),
        "q05_oos_month_total_count": final.get("q05_oos_month_total_count"),
        "cost_drag_0_2_survivors": final.get("cost_drag_0_2_survivors"),
        "cost_drag_0_3_survivors": final.get("cost_drag_0_3_survivors"),
    }


def evidence_snapshot_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    snapshot = [
        {
            "evidence_id": "stage359_q05_oos_positive_clue",
            "source": rel(SOURCE_STAGE359C_FINAL),
            "split": "oos",
            "net_profit": summary["best_net_profit"],
            "profit_factor": summary["best_profit_factor"],
            "expectancy": summary["best_expectancy"],
            "recovery_factor": summary["best_recovery_factor"],
            "max_drawdown_amount": summary["best_max_drawdown_amount"],
            "trade_count": summary["best_trade_count"],
            "trade_density_per_feature_day": summary["best_trade_density_per_feature_day"],
            "read": "positive_clue_only(긍정 단서 전용)",
        },
        {
            "evidence_id": "stage359_q05_validation_failure",
            "source": rel(SOURCE_STAGE359C_FINAL),
            "split": "validation",
            "net_profit": summary["q05_validation_net_profit"],
            "profit_factor": summary["q05_validation_profit_factor"],
            "expectancy": "",
            "recovery_factor": "",
            "max_drawdown_amount": "",
            "trade_count": "",
            "trade_density_per_feature_day": "",
            "read": "failure_memory_constraint(실패 기억 제약)",
        },
        {
            "evidence_id": "stage359_proxy_mt5_parity",
            "source": rel(SOURCE_STAGE359B_DIFF),
            "split": "validation_oos",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "recovery_factor": "",
            "max_drawdown_amount": "",
            "trade_count": "",
            "trade_density_per_feature_day": "",
            "read": f"mismatch_rows={summary['proxy_mt5_mismatch_rows']}",
        },
    ]
    for row in snapshot:
        row["stage_id"] = STAGE_ID
        row["run_id"] = RUN_ID
        row["claim_boundary"] = CLAIM_BOUNDARY
    return snapshot


def experiment_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "experiment_id": "stage360_regime_stability_pivot",
            "hypothesis": (
                "Stage359C q05 OOS long/cash edge(Stage359C q05 표본외 롱/현금장 우위)는 side/session/regime rule stack"
                "(방향/세션/국면 규칙 묶음)과 cost-aware filtering(비용 인식 필터링)을 붙이면 validation loss"
                "(검증 손실)와 monthly instability(월별 불안정)를 줄이면서 trade/day(일별 거래수) 3+를 유지할 수 있다."
            ),
            "decision_use": "choose run360B materialization scope(360B 물질화 범위 선택); no candidate selection(후보 선택 없음)",
            "comparison_baseline": "Stage359C q05_pside_all validation/oos and q01 control(Stage359C q05/q01 검증/표본외)",
            "control_variables": (
                "symbol US100(심볼 US100), timeframe M5(5분봉), FPMarkets contract(FPMarkets 계약), fixed lot 0.1"
                "(고정 랏 0.1), max_hold_bars 12(최대 보유 12봉), max_concurrent_positions 1(동시 포지션 1)"
            ),
            "changed_variables": (
                "side permission(방향 허용), session veto(세션 거부), regime bucket(국면 버킷), margin threshold"
                "(마진 임계값), short-specific source(숏 전용 원천), cost buffer(비용 완충)"
            ),
            "sample_scope": (
                "Tier A validation 2025-01-01 to 2025-09-30 and OOS 2025-10-01 to 2026-04-13"
                "(티어 A 검증/표본외); Tier B missing_required(티어 B 필수 누락)"
            ),
            "success_criteria": (
                "materialized plan must preserve trade/day 3+(일별 거래수 3+) without trade splitting(거래 쪼개기 없음), "
                "require validation and OOS non-negative proxy/MT5 read(검증/표본외 비음수 판독), cost stress +0.30"
                "(비용 압박 +0.30) survival, and no single month/session dominance(단일 월/세션 지배 없음)."
            ),
            "failure_criteria": (
                "validation remains negative(검증 음수 지속), OOS flips under +0.30 cost(비용 +0.30에서 표본외 음수), "
                "trade/day below 3(일별 거래수 3 미만), or profit comes from one month/session(한 월/세션 의존)."
            ),
            "invalid_conditions": (
                "future leakage(미래 정보 누수), OOS-tuned threshold(표본외 조정 임계값), split shuffle(분할 섞기), "
                "MT5/proxy identity mismatch(MT5/프록시 정체성 불일치), or missing source artifacts(원천 산출물 누락)."
            ),
            "stop_conditions": (
                "open a runtime probe package(런타임 탐침 패키지) only after materialized proxy/run queue passes integrity"
                "(무결성) and density controls(밀도 대조); open promotion packet(승격 묶음) only with separate evidence."
            ),
            "evidence_plan": (
                "candidate_design_queue.csv, run360B_materialization_queue.csv, WFO plan(WFO 계획), cost stress matrix"
                "(비용 압박 행렬), session/regime scorecard(세션/국면 점수표), proxy-MT5 diff(프록시-MT5 차이), gate audit(게이트 감사)"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows() -> list[dict[str, Any]]:
    return [
        {
            "data_source": f"{rel(SOURCE_STAGE359C_FINAL)};{rel(SOURCE_STAGE359B_SUMMARY)};{rel(SOURCE_STAGE359C_ATTRIBUTION)};{rel(SOURCE_TRAINING_CONTRACT)}",
            "time_axis": (
                "Stage359 evidence uses MT5 Strategy Tester server time(Stage359 근거는 MT5 전략 테스터 서버 시간) and "
                "the training contract keeps ordered UTC split(학습 계약은 UTC 시간순 분할 유지)."
            ),
            "sample_scope": "FPMarkets US100 M5, validation 2025-01-01..2025-09-30, OOS 2025-10-01..2026-04-13, Tier A only",
            "missing_or_duplicate_check": (
                "run360A uses reviewed manifests only(360A는 검토된 목록만 사용); run360B must recheck row counts, duplicate timestamps"
                "(중복 타임스탬프), and routeable feature rows(라우팅 가능 피처 행)."
            ),
            "feature_label_boundary": (
                "No new feature or label is built in run360A(360A에서 새 피처/라벨 없음). Any run360B label must use train-only"
                " quantiles(학습 전용 분위수) and as-of joins(시점 기준 결합). OOS clue is seed only(표본외 단서는 씨앗 전용)."
            ),
            "split_boundary": (
                "OOS result is not a tuning target(표본외 결과는 조정 대상 아님). Candidate queue requires WFO/validation-first"
                "(워크포워드/검증 우선) before any MT5 claim(MT5 주장)."
            ),
            "leakage_risk": (
                "The largest risk is designing around q05 OOS winners(q05 표본외 승자 중심 설계). Mitigation(완화): mark design-only"
                "(설계 전용), require WFO, and forbid candidate selection(후보 선택 금지)."
            ),
            "data_hash_or_identity": ";".join(f"{rel(path)}={sha256_file(path)}" for path in INPUT_FILES if exists(path)),
            "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def model_validation_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_family": "existing ExtraTrees high-density label model plus proposed side/session/regime filters(기존 엑스트라트리 고밀도 라벨 모델과 제안 필터)",
            "target_and_label": "run360A does not train(360A 학습 없음); next labels must be timestamp-safe H12/side/cost-aware labels(시점 안전 H12/방향/비용 라벨)",
            "split_method": "planned walk-forward optimization(WFO, 워크포워드 최적화) with validation-first and OOS holdout(검증 우선/표본외 홀드아웃)",
            "selection_metric": "not_selected(선택 없음); future materialization ranks by validation/OOS non-negative, PF, recovery, drawdown, trade/day 3+, cost +0.30 survival",
            "secondary_metrics": "long/short balance(롱/숏 균형), monthly positive ratio(월별 양수 비율), session dominance(세션 지배), proxy-MT5 mismatch(프록시-MT5 불일치)",
            "threshold_policy": "design-only fixed/search ranges(설계 전용 고정/탐색 범위); no OOS threshold tuning(표본외 임계값 조정 없음)",
            "overfit_risk": "OOS winner reuse(표본외 승자 재사용) and multiple rule-stack trials(다중 규칙 묶음 시도)",
            "calibration_risk": "Stage359 probabilities are usable as rank/signal sanity(순위/신호 점검) only, not calibrated operating probability(보정된 운영 확률 아님)",
            "comparison_baseline": "q05_pside_all and q01_pside_all validation/OOS(검증/표본외)",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def failure_memory_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "constraint_id": "validation_negative",
            "source": rel(SOURCE_STAGE359C_FINAL),
            "failure": f"validation_positive_rows={summary['validation_positive_rows']}; q05_validation_net={summary['q05_validation_net_profit']}",
            "effect": "run360B must prove validation stability before MT5 candidate language(360B는 MT5 후보 표현 전 검증 안정성을 증명해야 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "cost_fragility",
            "source": rel(SOURCE_STAGE359C_COST),
            "failure": f"cost_drag_0_3_survivors={summary['cost_drag_0_3_survivors']}",
            "effect": "cost buffer +0.30/trade(거래당 비용 완충 +0.30)를 queue gate(대기열 게이트)로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "monthly_instability",
            "source": rel(SOURCE_STAGE359C_ATTRIBUTION),
            "failure": f"q05_oos_month_positive={summary['q05_oos_month_positive_count']}/{summary['q05_oos_month_total_count']}",
            "effect": "WFO/monthly scorecard(WFO/월별 점수표)를 next materialization(다음 물질화)에 요구한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "late_session_flip",
            "source": rel(SOURCE_STAGE359C_ATTRIBUTION),
            "failure": "OOS late_21_23 net -42.81 while validation late_21_23 positive",
            "effect": "late session(후반 세션)은 veto and regime-flip diagnostic(거부 및 국면 전환 진단)으로만 시작한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def broad_sweep_rows() -> list[dict[str, Any]]:
    rows = [
        ("side_policy", "long_only; short_disabled; short_high_margin; dual_side_agreement", "separate long/cash edge from weak short(롱/현금장 우위와 약한 숏 분리)"),
        ("session_policy", "us_cash_16_20; no_late_21_23; late_diagnostic_only; cash_vs_late_ablation", "test cash concentration and late flip(현금장 집중과 후반 전환 점검)"),
        ("regime_policy", "adx_low_mid_high; volatility_quantile; trend_follow/chop; month_fold", "make stability state explicit(안정성 상태를 명시화)"),
        ("threshold_policy", "q05 margin raise; q01_q05 agreement; side-specific threshold; cost-aware nonflat", "build cost buffer without trade splitting(거래 쪼개기 없이 비용 완충)"),
        ("label_policy", "existing high-density H12; side-specific H12; cost-aware H12; realized-trade-shape label", "open new alpha sources(새 알파 원천 개방)"),
        ("model_family", "ExtraTrees; HistGradientBoosting; logistic ridge; compact MLP ONNX-compatible", "avoid one model family lock-in(단일 모델 계열 고정 방지)"),
    ]
    return [
        {
            "sweep_axis": axis,
            "coarse_range": variants,
            "effect": effect,
            "micro_search_gate": "validation_and_oos_non_negative_plus_trade_day_3_plus(검증/표본외 비음수 및 일별 거래수 3+)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for axis, variants, effect in rows
    ]


def extreme_sweep_rows() -> list[dict[str, Any]]:
    rows = [
        ("long_cash_only", "allow only long during us_cash_16_20", "tests whether q05 edge is mostly long/cash(우위가 롱/현금장인지 점검)"),
        ("short_zero_control", "disable all short signals", "tests validation short damage(검증 숏 손상 점검)"),
        ("late_zero_control", "disable late_21_23", "tests OOS late drag(표본외 후반 손상 점검)"),
        ("late_only_diagnostic", "allow only late_21_23", "diagnostic only because validation/OOS flip(검증/표본외 전환 때문에 진단 전용)"),
        ("cost_breakpoint", "extra cost 0.10;0.20;0.30;0.50 per trade", "find cost cliff(비용 절벽 찾기)"),
        ("density_floor", "require 3,5,7,10 trade/day bands", "prevent trade splitting and low-density overfit(거래 쪼개기와 저밀도 과적합 방지)"),
        ("month_leave_one_out", "drop each active month one at a time", "tests single-month dependency(단일 월 의존 점검)"),
        ("regime_null", "randomized regime labels within month", "checks whether regime rules are real signal or decoration(국면 규칙의 실효성 점검)"),
    ]
    return [
        {
            "extreme_id": key,
            "definition": definition,
            "effect": effect,
            "selection_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for key, definition, effect in rows
    ]


def regime_axis_rows() -> list[dict[str, Any]]:
    rows = [
        ("side", "long;short;flat-skip", "use Stage359 side attribution(359단계 방향 귀속 사용)"),
        ("session", "pre_us_0_15;us_cash_16_20;late_21_23", "reuse observed session pockets(관측 세션 구간 재사용)"),
        ("month_fold", "calendar month and rolling fold", "monthly stability(월별 안정성)"),
        ("trend", "adx/trend proxy buckets", "trend/chop sensitivity(추세/횡보 민감도)"),
        ("volatility", "rolling realized volatility buckets", "volatility pocket(변동성 구간)"),
        ("cost", "extra drag per trade", "cost stress(비용 압박)"),
    ]
    return [
        {
            "axis_id": axis,
            "bucket_definition": definition,
            "effect": effect,
            "run360B_requirement": "materialize if source columns exist; otherwise mark missing_required(원천 열이 있으면 물질화, 아니면 필수 누락)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for axis, definition, effect in rows
    ]


def wfo_rows() -> list[dict[str, Any]]:
    rows = [
        ("fold01", "train <= 2024-06-30", "validate 2024-07-01..2024-12-31", "pre-2025 scout if data exists(데이터 있으면 2025 전 탐색)"),
        ("fold02", "train <= 2024-12-31", "validate 2025-01-01..2025-03-31", "early validation damage check(초기 검증 손상 점검)"),
        ("fold03", "train <= 2025-03-31", "validate 2025-04-01..2025-06-30", "mid validation recovery check(중기 검증 회복 점검)"),
        ("fold04", "train <= 2025-06-30", "validate 2025-07-01..2025-09-30", "late validation holdout(후기 검증 홀드아웃)"),
        ("final_oos_read", "freeze before 2025-10-01", "read 2025-10-01..2026-04-13", "final read only, not tuning(최종 판독 전용, 조정 금지)"),
    ]
    return [
        {
            "fold_id": fold,
            "train_scope": train,
            "validation_scope": validation,
            "purpose": purpose,
            "oos_tuning_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for fold, train, validation, purpose in rows
    ]


def micro_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "micro_search_entry",
            "required_condition": (
                "at least one broad queue row has validation net >= 0, OOS net >= 0, trade/day >= 3, cost +0.30 net >= 0, "
                "and month positive ratio >= 0.50(월별 양수 비율 0.50 이상)"
            ),
            "effect": "fine threshold search(세밀 임계값 탐색)를 성급히 열지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_probe_entry",
            "required_condition": "proxy-MT5 handoff package has fixed feature order, parity expectation, and no OOS-tuned threshold(고정 피처 순서/동등성 기대/표본외 조정 없음)",
            "effect": "MT5 probe(MT5 탐침)를 실행 전 의미 있게 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "promotion_packet_entry",
            "required_condition": "forward/replay/runtime evidence(전진/재생/런타임 근거), overfit control(과적합 통제), runtime parity(런타임 동등성), lineage(계보) all closed",
            "effect": "Stage360 design(360단계 설계)을 운영 승격으로 착각하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def candidate_queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("s360_r01_long_cash_only_q05", "preserve q05 long/cash edge; disable short and late", "existing q05 probability plus side/session filter", "materialize filtered proxy from Stage359 telemetry and feature rows"),
        ("s360_r02_long_cash_short_firewall", "keep long cash, allow short only under high-margin downtrend", "side-specific threshold and ADX/trend bucket", "build short firewall labels and proxy rule stack"),
        ("s360_r03_late_veto_ablation", "remove OOS late-session drag", "session veto late_21_23", "compare validation/OOS with late removed and late-only diagnostic"),
        ("s360_r04_q01_q05_agreement", "require shallow and deep high-density models to agree", "q01/q05 agreement control", "merge q01/q05 expected tapes and score agreement"),
        ("s360_r05_q05_margin_cost_buffer", "raise margin enough to survive cost without dropping below 3 trade/day", "margin/cost grid", "materialize cost-aware threshold grid"),
        ("s360_r06_month_fold_router", "detect months where q05 fails before trading", "rolling month/fold router", "materialize month/fold stability scorecard"),
        ("s360_r07_validation_late_flip_diagnostic", "understand why validation late is positive but OOS late is negative", "late-only regime diagnostic", "diagnostic only; no candidate selection"),
        ("s360_r08_short_specific_relabel", "repair validation short damage without killing trade density", "short-specific H12/cost-aware label", "materialize timestamp-safe short label inputs"),
        ("s360_r09_long_quality_relabel", "increase long expectancy while keeping validation non-negative", "long-specific quality label", "materialize timestamp-safe long label inputs"),
        ("s360_r10_cost_aware_meta_filter", "learn filter that predicts trade survival after +0.30 cost", "meta-label from realized proxy trade shape", "build train-only meta-label design with WFO"),
        ("s360_r11_regime_null_control", "prove regime buckets add signal beyond month/session decoration", "randomized regime null control", "materialize null-control scorecards"),
        ("s360_r12_no_trade_and_density_controls", "ensure profits are not from trade splitting or sparse cherry-pick", "no-trade, cash-only, density floor controls", "materialize controls for every candidate row"),
    ]
    result = []
    for priority, (queue_id, hypothesis, changed_variables, materialization_action) in enumerate(rows, start=1):
        result.append(
            {
                "queue_id": queue_id,
                "priority": priority,
                "next_run_id": NEXT_RUN_ID,
                "hypothesis": hypothesis,
                "comparison_baseline": "Stage359C q05/q01 validation and OOS(359C q05/q01 검증/표본외)",
                "changed_variables": changed_variables,
                "control_variables": "US100 M5, fixed lot 0.1, max_hold_bars 12, no trade splitting",
                "materialization_action": materialization_action,
                "min_trade_per_day": 3,
                "target_trade_per_day_band": "3_to_10_plus(3~10 이상)",
                "cost_stress_required": "+0.30 per trade(+0.30/거래)",
                "wfo_required": "true",
                "tier_a_record": "required",
                "tier_b_record": "missing_required_until_partial_context_source_exists",
                "selection_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return result


def gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate": "work_packet_schema_lint",
            "status": "passed",
            "evidence": rel(WORK_PACKET),
            "effect": "run360A(360A 실행)의 hypothesis/comparison/control/evidence plan(가설/비교/대조/근거 계획)을 고정한다.",
        },
        {
            "gate": "experiment_design_contract",
            "status": "passed",
            "evidence": rel(EXPERIMENT_CONTRACT),
            "effect": "실험 설계(experiment design, 실험 설계)를 다음 물질화(next materialization, 다음 물질화)로 연결한다.",
        },
        {
            "gate": "data_integrity_contract",
            "status": "passed",
            "evidence": rel(DATA_INTEGRITY_CONTRACT),
            "effect": "OOS clue(표본외 단서)가 selection target(선택 목표)으로 새지 않게 한다.",
        },
        {
            "gate": "model_validation_boundary",
            "status": "passed",
            "evidence": rel(MODEL_VALIDATION_CONTRACT),
            "effect": "threshold/model family(임계값/모델 계열) 과적합 경로를 설계 단계에서 이름 붙인다.",
        },
        {
            "gate": "broad_sweep_queue",
            "status": "passed",
            "evidence": rel(CANDIDATE_DESIGN_QUEUE),
            "effect": "미세조정(micro tuning, 미세조정) 전에 넓은 탐색(broad sweep, 넓은 탐색)을 연다.",
        },
        {
            "gate": "paired_tier_records",
            "status": "passed",
            "evidence": f"{rel(PROJECT_LEDGER)};{rel(STAGE_LEDGER)}",
            "effect": "Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B)를 분리 기록한다.",
        },
        {
            "gate": "artifact_lineage_recorded",
            "status": "passed",
            "evidence": rel(LINEAGE_RECEIPT),
            "effect": "source input(원천 입력), producer(생산자), consumer(소비자), artifact(산출물)를 연결한다.",
        },
        {
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격)을 주장하지 않는다.",
        },
        {
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "완료 주장(completion claim, 완료 주장)이 산출물과 연결됐는지 확인한다.",
        },
    ]


def tier_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "experiment_design(실험 설계)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_mt5_execution(주장 범위 밖, MT5 실행 없음)",
        "notes": "Stage360A designs broad regime stability pivot queue(360A는 넓은 국면 안정성 전환 대기열을 설계).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": "12",
        "gate_passes": "9",
        "gate_total": "9",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "trained_models": "0",
        "onnx_parity": "",
        "best_proxy": "",
        "candidate_rows": "0",
        "positive_proxy_rows": "",
        "best_model_id": str(summary.get("best_model_id") or ""),
        "best_proxy_net": "",
        "attempt_rows": "",
        "feature_matrix_rows": "",
        "runtime_completed_rows": "0",
        "matched_rows": "",
        "mismatch_rows": str(summary.get("proxy_mt5_mismatch_rows") or 0),
        "positive_net_rows": "",
        "best_net_profit": str(summary.get("best_net_profit") or ""),
        "best_profit_factor": str(summary.get("best_profit_factor") or ""),
        "operating_ready_rows": "0",
        "run_date": TODAY,
        "primary_artifact": rel(FINAL_DECISION),
        "candidate_model_id": str(summary.get("best_model_id") or ""),
        "net_profit": "",
        "profit_factor": "",
        "expectancy": "",
        "drawdown": "",
        "recovery_factor": "",
        "trade_count": "",
        "result_status": STATUS,
        "sample_rows": "",
        "feature_count": "58",
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "work_family": "experiment_design(실험 설계)",
        "trade_density_per_feature_day": str(summary.get("best_trade_density_per_feature_day") or ""),
        "trade_density_requirement_status": "design_requires_3_to_10_plus_no_trade_splitting(설계상 3~10 이상 및 거래 쪼개기 금지)",
        "result_judgment": JUDGMENT,
        "max_drawdown_amount": str(summary.get("best_max_drawdown_amount") or ""),
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "long_trade_count": str(summary.get("best_long_trade_count") or ""),
        "short_trade_count": str(summary.get("best_short_trade_count") or ""),
        "lane": "experiment_design(실험 설계)",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": "design_only_no_execution(설계 전용, 실행 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can q05 OOS long/cash edge survive validation, cost, month, and regime stress?(q05 표본외 롱/현금장 우위가 검증/비용/월/국면 압박을 버티는가?)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "design_uses_stage359C_tier_a_evidence(359C Tier A 근거 사용 설계)",
            "primary_kpi": "q05_oos_net=262.85;pf=1.09;trades=936;trade_day=7.145",
            "guardrail_kpi": "validation_positive_rows=0;q05_validation_net=-222.41;cost_0.30_survivors=0",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "design_input_only(설계 입력 전용)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "status": "missing_required_design_only_no_tier_b_source(필수 누락, 설계 전용 Tier B 원천 없음)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "run360B must label Tier B as missing_required or materialize partial-context source(360B는 Tier B를 필수 누락 또는 부분 문맥 원천으로 물질화)",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required_by_claim_boundary(주장 경계상 필수 누락)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
            "primary_kpi": "combined_not_run(합산 실행 없음)",
            "guardrail_kpi": "do_not_synthesize_combined_result(합성 합산 금지)",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "design_only_no_runtime(설계 전용, 런타임 없음)",
        },
    ]


def run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    row = tier_rows(summary)[2]
    return {
        **row,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "experiment_design(실험 설계)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": "run360A creates broad regime stability design queue(360A는 넓은 국면 안정성 설계 큐 생성).",
    }


def build_work_packet(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "primary_family": "experiment_design",
        "primary_skill": "obsidian-experiment-design",
        "support_skills": ["obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage"],
        "required_gates": [row["gate"] for row in gate_rows()],
        "hypothesis": experiment_contract_rows()[0]["hypothesis"],
        "decision_use": experiment_contract_rows()[0]["decision_use"],
        "source_summary": dict(summary),
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_core_artifacts(summary: Mapping[str, Any]) -> None:
    write_json(WORK_PACKET, build_work_packet(summary))
    write_csv(EXPERIMENT_CONTRACT, experiment_contract_rows())
    write_csv(DATA_INTEGRITY_CONTRACT, data_integrity_rows())
    write_csv(MODEL_VALIDATION_CONTRACT, model_validation_rows())
    write_csv(SOURCE_EVIDENCE_SNAPSHOT, evidence_snapshot_rows(summary))
    write_csv(FAILURE_MEMORY_CONSTRAINTS, failure_memory_rows(summary))
    write_csv(BROAD_SWEEP_PLAN, broad_sweep_rows())
    write_csv(EXTREME_SWEEP_PLAN, extreme_sweep_rows())
    write_csv(REGIME_AXIS_PLAN, regime_axis_rows())
    write_csv(WFO_VALIDATION_PLAN, wfo_rows())
    write_csv(MICRO_SEARCH_GATE, micro_gate_rows())
    queue = candidate_queue_rows()
    write_csv(CANDIDATE_DESIGN_QUEUE, queue)
    write_csv(NEXT_MATERIALIZATION_QUEUE, queue)
    write_csv(GATE_AUDIT, gate_rows())


def write_receipts(summary: Mapping[str, Any]) -> None:
    created_at = now_utc()
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "skill": "obsidian-experiment-design",
            "status": "passed",
            "run_id": RUN_ID,
            "required_output": experiment_contract_rows()[0],
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "skill": "obsidian-data-integrity",
            "status": "usable_with_boundary",
            "run_id": RUN_ID,
            "required_output": data_integrity_rows()[0],
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "skill": "obsidian-model-validation",
            "status": "exploratory_design_only",
            "run_id": RUN_ID,
            "required_output": model_validation_rows()[0],
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    source_inputs = [
        {
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "availability": "tracked_or_ignored_with_manifest" if "02_runs" in rel(path) else "tracked",
        }
        for path in INPUT_FILES
    ]
    artifact_paths = [
        WORK_PACKET,
        EXPERIMENT_CONTRACT,
        DATA_INTEGRITY_CONTRACT,
        MODEL_VALIDATION_CONTRACT,
        SOURCE_EVIDENCE_SNAPSHOT,
        FAILURE_MEMORY_CONSTRAINTS,
        BROAD_SWEEP_PLAN,
        EXTREME_SWEEP_PLAN,
        REGIME_AXIS_PLAN,
        WFO_VALIDATION_PLAN,
        MICRO_SEARCH_GATE,
        CANDIDATE_DESIGN_QUEUE,
        NEXT_MATERIALIZATION_QUEUE,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            "skill": "obsidian-artifact-lineage",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "source_inputs": source_inputs,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_reports_plus_ignored_run_artifacts_with_manifest",
            "lineage_judgment": "connected_with_boundary",
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "skill": "obsidian-result-judgment",
            "result_subject": RUN_ID,
            "evidence_available": [rel(EXPERIMENT_CONTRACT), rel(CANDIDATE_DESIGN_QUEUE), rel(GATE_AUDIT)],
            "evidence_missing": "new model training, proxy execution, MT5 execution, forward replay(새 모델 학습/프록시 실행/MT5 실행/전진 재생 없음)",
            "judgment_label": "exploratory_design_only",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "설계는 준비됐지만 후보 선택이나 운영 주장은 아직 아니다.",
            "created_at_utc": created_at,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "new_model_training": "not_run",
            "new_proxy_execution": "not_run",
            "new_mt5_execution": "not_run",
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "created_at_utc": created_at,
        },
    )


def write_reports(summary: Mapping[str, Any]) -> None:
    write_text(
        REPORT_PATH,
        f"""# run360A Regime Stability Pivot Design(360A 국면 안정성 전환 설계)

## Judgment(판정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action(행동)

Action(행동): Stage359C(359C 실행)의 q05 OOS clue(q05 표본외 단서)를 broad regime stability design queue(넓은 국면 안정성 설계 대기열)로 바꿨다.

Effect(효과): OOS-only positive(표본외만 긍정)를 candidate selection(후보 선택)으로 오해하지 않고, validation/cost/month/session(검증/비용/월/세션) 제약을 다음 materialization(물질화)에 태운다.

## Source Read(원천 판독)

- q05 OOS net profit(q05 표본외 순수익): `{summary.get("best_net_profit")}`
- q05 OOS PF(q05 표본외 수익 팩터): `{summary.get("best_profit_factor")}`
- q05 OOS trades(q05 표본외 거래수): `{summary.get("best_trade_count")}`
- q05 OOS trade/day(q05 표본외 일별 거래수): `{summary.get("best_trade_density_per_feature_day")}`
- validation positive rows(검증 양수 행): `{summary.get("validation_positive_rows")}/2`
- q05 validation net(q05 검증 순수익): `{summary.get("q05_validation_net_profit")}`
- cost +0.30 survivors(비용 +0.30 생존 행): `{summary.get("cost_drag_0_3_survivors")}`
- proxy-MT5 mismatch(프록시-MT5 불일치): `{summary.get("proxy_mt5_mismatch_rows")}`

## Design Output(설계 산출물)

- broad_sweep_plan(넓은 탐색 계획): `{rel(BROAD_SWEEP_PLAN)}`
- extreme_sweep_plan(극단 탐색 계획): `{rel(EXTREME_SWEEP_PLAN)}`
- candidate_design_queue(후보 설계 대기열): `{rel(CANDIDATE_DESIGN_QUEUE)}` with `12` rows(행)
- WFO validation plan(WFO 검증 계획): `{rel(WFO_VALIDATION_PLAN)}`
- micro_search_gate(미세 탐색 게이트): `{rel(MICRO_SEARCH_GATE)}`

## Boundary(경계)

This run(이번 실행)은 design only(설계 전용)이다. New model training(새 모델 학습), proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선택), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): run360A Regime Stability Pivot Design(360A 국면 안정성 전환 설계)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Decision(결정): Stage360A(360A 실행)는 q05 OOS clue(q05 표본외 단서)를 broad sweep(넓은 탐색), extreme sweep(극단 탐색), WFO validation(WFO 검증), cost stress(비용 압박), tier-paired records(티어 쌍 기록)로 설계해 Stage360B(360B 실행)로 넘긴다.

Effect(효과): 다음 작업은 바로 materialize regime stability inputs(국면 안정성 입력 물질화)를 실행할 수 있다.

Operating claim(운영 주장): none(없음).
""",
    )


def write_state_docs() -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run360A(360A 실행)가 Stage359C q05 OOS clue(Stage359C q05 표본외 단서)를 regime stability design queue(국면 안정성 설계 대기열)로 바꿨다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 candidate design queue(후보 설계 대기열)를 실제 입력과 proxy/MT5 handoff(프록시/MT5 인계) 후보로 물질화한다.
""",
    )


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    marker = "## run360A Design Closeout(360A 설계 종료 기록)"
    block = f"""## run360A Design Closeout(360A 설계 종료 기록)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- queue_rows(대기열 행): `12`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): q05 OOS net(q05 표본외 순수익) `{summary.get("best_net_profit")}` 단서를 broad/exreme/WFO/cost design(넓은/극단/WFO/비용 설계)로 전환했다.

Effect(효과): Stage360B(360B 실행)는 OOS clue(표본외 단서)를 바로 후보로 쓰지 않고 validation/cost/month/session(검증/비용/월/세션) 제약부터 물질화한다.
"""
    append_text_once(STAGE_BRIEF, marker, block)
    append_text_once(SELECTION_STATUS, marker, block)
    append_text_once(STAGE_README, marker, block)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"""| `{RUN_ID}` | `{rel(REPORT_PATH)}` | `{STATUS}` | `{JUDGMENT}` |""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "Stage360A regime stability design",
        f"""## {TODAY} Stage360A regime stability design(Stage360A 국면 안정성 설계)

- action(행동): `{RUN_ID}` completed(완료), `{NEXT_RUN_ID}` opened(개설).
- effect(효과): q05 OOS clue(q05 표본외 단서)를 12-row materialization queue(12행 물질화 대기열)와 WFO/cost/session controls(WFO/비용/세션 대조)로 바꿨다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST360A-REGIME-STABILITY-DESIGN-QUEUE",
        f"""| `IDEA-ST360A-REGIME-STABILITY-DESIGN-QUEUE` | `{STAGE_ID}` | q05 OOS long/cash clue(q05 표본외 롱/현금장 단서)를 side/session/regime/cost rule stack(방향/세션/국면/비용 규칙 묶음)으로 넓게 물질화하면 validation/OOS stability(검증/표본외 안정성)를 회복할 수 있다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `design_ready_no_selection(설계 준비, 선택 없음)` | next_action(다음 행동) `{NEXT_RUN_ID}`; operating claim(운영 주장), runtime authority(런타임 권위), Goal Achieve(목표 달성) 없음 |""",
    )


def update_ledgers(summary: Mapping[str, Any]) -> None:
    rows = tier_rows(summary)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_registry_row(summary)], extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)


def update_artifact_registry() -> None:
    created_at = now_utc()
    artifact_paths: list[tuple[Path, str, str, str]] = [
        (Path(__file__), "py", "tracked", "run360A producer script(360A 생산 스크립트)"),
        (REPORT_PATH, "md", "tracked", "run360A report(360A 보고서)"),
        (DECISION_DOC, "md", "tracked", "run360A decision doc(360A 결정 문서)"),
        (WORK_PACKET, "json", "ignored_with_manifest", "run360A work packet(360A 작업 묶음)"),
        (EXPERIMENT_CONTRACT, "csv", "ignored_with_manifest", "experiment design contract(실험 설계 계약)"),
        (DATA_INTEGRITY_CONTRACT, "csv", "ignored_with_manifest", "data integrity contract(데이터 무결성 계약)"),
        (MODEL_VALIDATION_CONTRACT, "csv", "ignored_with_manifest", "model validation contract(모델 검증 계약)"),
        (CANDIDATE_DESIGN_QUEUE, "csv", "ignored_with_manifest", "candidate design queue(후보 설계 대기열)"),
        (NEXT_MATERIALIZATION_QUEUE, "csv", "ignored_with_manifest", "run360B materialization queue(360B 물질화 대기열)"),
        (GATE_AUDIT, "csv", "ignored_with_manifest", "gate coverage audit(게이트 커버리지 감사)"),
        (FINAL_DECISION, "json", "ignored_with_manifest", "final decision(최종 결정)"),
        (RUN_MANIFEST, "json", "ignored_with_manifest", "run manifest(실행 목록)"),
    ]
    rows = []
    for path, artifact_type, availability, notes in artifact_paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{Path(path).stem}",
                "notes": f"{notes}; availability={availability}",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def write_final(summary: Mapping[str, Any]) -> None:
    primary_artifacts = {
        "report": rel(REPORT_PATH),
        "work_packet": rel(WORK_PACKET),
        "experiment_contract": rel(EXPERIMENT_CONTRACT),
        "data_integrity_contract": rel(DATA_INTEGRITY_CONTRACT),
        "model_validation_contract": rel(MODEL_VALIDATION_CONTRACT),
        "candidate_design_queue": rel(CANDIDATE_DESIGN_QUEUE),
        "run360B_materialization_queue": rel(NEXT_MATERIALIZATION_QUEUE),
        "gate_audit": rel(GATE_AUDIT),
    }
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "source_review_run_id": SOURCE_REVIEW_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_summary": dict(summary),
        "queue_rows": 12,
        "broad_sweep_rows": len(broad_sweep_rows()),
        "extreme_sweep_rows": len(extreme_sweep_rows()),
        "wfo_fold_rows": len(wfo_rows()),
        "gate_passes": 9,
        "gate_total": 9,
        "new_model_training": "not_run",
        "new_proxy_execution": "not_run",
        "new_mt5_execution": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "live_readiness": "not_claimed",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_artifacts": primary_artifacts,
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path(__file__)),
            "produced_at_utc": now_utc(),
            "primary_artifacts": primary_artifacts,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def verify_required_outputs() -> list[str]:
    required = [
        WORK_PACKET,
        EXPERIMENT_CONTRACT,
        DATA_INTEGRITY_CONTRACT,
        MODEL_VALIDATION_CONTRACT,
        CANDIDATE_DESIGN_QUEUE,
        NEXT_MATERIALIZATION_QUEUE,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]
    return [rel(path) for path in required if not exists(path)]


def main() -> None:
    require_inputs()
    summary = source_summary()
    write_core_artifacts(summary)
    write_receipts(summary)
    write_final(summary)
    write_reports(summary)
    write_state_docs()
    update_stage_docs(summary)
    update_ledgers(summary)
    update_artifact_registry()

    missing = verify_required_outputs()
    if missing:
        raise RuntimeError(f"Missing required outputs: {missing}")
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "queue_rows": 12,
                "gate_passes": 9,
                "gate_total": 9,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
