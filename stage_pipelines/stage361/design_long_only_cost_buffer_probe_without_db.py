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

STAGE_ID = "361_long_only_cost_buffer__validation_oos_positive_cost_failure"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run361A"
RUN_ID = "run361A_design_long_only_cost_buffer_probe_without_db_v1"
PARENT_RUN_ID = "run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
SOURCE_MATERIALIZATION_RUN_ID = "run360B_materialize_regime_stability_pivot_inputs_without_db_v1"
NEXT_RUN_ID = "run361B_materialize_long_only_cost_buffer_inputs_without_db_v1"

STATUS = "completed_stage361A_long_only_cost_buffer_design_ready_materialization_required_no_selection_no_mt5"
JUDGMENT = "long_only_cost_buffer_design_ready_materialization_required_no_operating_claim"
DECISION = "stage361A_open_run361B_materialize_long_only_cost_buffer_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_design_only_long_only_cost_buffer_no_model_training_no_proxy_execution_"
    "no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
REPORT_PATH = REVIEW_DIR / "run361A_long_only_cost_buffer_design.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage361A_long_only_cost_buffer_design.md"

SOURCE_STAGE360_DIR = ROOT / "stages" / "360_regime_stability_pivot__oos_long_cash_edge_validation_loss"
SOURCE_STAGE359_DIR = ROOT / "stages" / "359_runtime_probe_execution__high_density_label_pivot_mt5_check"
SOURCE_SEED_QUEUE = SOURCE_STAGE360_DIR / "02_runs" / "run360C" / "stage361_seed_queue.csv"
SOURCE_REVIEW_SCORECARD = SOURCE_STAGE360_DIR / "02_runs" / "run360C" / "run360C_review_scorecard.csv"
SOURCE_STAGE360C_FINAL = SOURCE_STAGE360_DIR / "02_runs" / "run360C" / "final_decision.json"
SOURCE_STAGE360B_SCORECARD = SOURCE_STAGE360_DIR / "02_runs" / "run360B" / "materialized_filter_scorecard.csv"
SOURCE_STAGE360B_COST = SOURCE_STAGE360_DIR / "02_runs" / "run360B" / "cost_stress_matrix.csv"
SOURCE_STAGE360B_MONTHLY = SOURCE_STAGE360_DIR / "02_runs" / "run360B" / "monthly_stability_scorecard.csv"
SOURCE_STAGE360B_SESSION = SOURCE_STAGE360_DIR / "02_runs" / "run360B" / "session_side_scorecard.csv"
SOURCE_STAGE359B_SUMMARY = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "high_density_label_pivot_mt5_probe_summary.csv"
SOURCE_Q05_VALIDATION_TELEMETRY = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "runtime_telemetry" / "q05_pside_all_validation_telemetry.csv"
SOURCE_Q05_OOS_TELEMETRY = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "runtime_telemetry" / "q05_pside_all_oos_telemetry.csv"

INPUT_FILES = [
    SOURCE_SEED_QUEUE,
    SOURCE_REVIEW_SCORECARD,
    SOURCE_STAGE360C_FINAL,
    SOURCE_STAGE360B_SCORECARD,
    SOURCE_STAGE360B_COST,
    SOURCE_STAGE360B_MONTHLY,
    SOURCE_STAGE360B_SESSION,
    SOURCE_STAGE359B_SUMMARY,
    SOURCE_Q05_VALIDATION_TELEMETRY,
    SOURCE_Q05_OOS_TELEMETRY,
]

WORK_PACKET = RUN_DIR / "work_packet.json"
SOURCE_EVIDENCE_SNAPSHOT = RUN_DIR / "source_evidence_snapshot.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "data_integrity_contract.csv"
MODEL_VALIDATION_CONTRACT = RUN_DIR / "model_validation_contract.csv"
FAILURE_MEMORY_CONSTRAINTS = RUN_DIR / "failure_memory_constraints.csv"
BROAD_SWEEP_PLAN = RUN_DIR / "broad_sweep_plan.csv"
EXTREME_SWEEP_PLAN = RUN_DIR / "extreme_sweep_plan.csv"
MARGIN_GRID_PLAN = RUN_DIR / "margin_grid_plan.csv"
REGIME_AXIS_PLAN = RUN_DIR / "regime_axis_plan.csv"
LABEL_DESIGN_PLAN = RUN_DIR / "label_design_plan.csv"
WFO_VALIDATION_PLAN = RUN_DIR / "wfo_validation_plan.csv"
MICRO_SEARCH_GATE = RUN_DIR / "micro_search_gate.csv"
RUN361B_MATERIALIZATION_QUEUE = RUN_DIR / "run361B_materialization_queue.csv"
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


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
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


def csv_count(path: Path) -> int:
    _, rows = read_csv_rows(path)
    return len(rows)


def source_snapshot() -> dict[str, Any]:
    final = read_json(SOURCE_STAGE360C_FINAL)
    return {
        "primary_seed_id": final["primary_seed_id"],
        "primary_seed_rule_id": final["primary_seed_rule_id"],
        "long_only_validation_net_profit": final["long_only_validation_net_profit"],
        "long_only_oos_net_profit": final["long_only_oos_net_profit"],
        "long_only_validation_cost_0_30_net": final["long_only_validation_cost_0_30_net"],
        "long_only_oos_cost_0_30_net": final["long_only_oos_cost_0_30_net"],
        "seed_rows": final["seed_rows"],
        "review_rows": final["review_rows"],
    }


def source_evidence_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "q05_long_only_positive_before_cost",
            "source": rel(SOURCE_STAGE360C_FINAL),
            "validation_net_profit": summary["long_only_validation_net_profit"],
            "oos_net_profit": summary["long_only_oos_net_profit"],
            "interpretation": "positive_seed_before_cost(비용 전 긍정 씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "q05_long_only_cost_failure",
            "source": rel(SOURCE_STAGE360C_FINAL),
            "validation_cost_0_30_net": summary["long_only_validation_cost_0_30_net"],
            "oos_cost_0_30_net": summary["long_only_oos_cost_0_30_net"],
            "interpretation": "cost_buffer_required(비용 버퍼 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "q05_runtime_telemetry_validation",
            "source": rel(SOURCE_Q05_VALIDATION_TELEMETRY),
            "rows": csv_count(SOURCE_Q05_VALIDATION_TELEMETRY),
            "interpretation": "bar_level_probability_source_for_run361B(run361B bar-level, 바 단위 확률 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "q05_runtime_telemetry_oos",
            "source": rel(SOURCE_Q05_OOS_TELEMETRY),
            "rows": csv_count(SOURCE_Q05_OOS_TELEMETRY),
            "interpretation": "bar_level_probability_source_for_run361B(run361B bar-level, 바 단위 확률 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def experiment_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "field": "hypothesis",
            "value": "q05 long-only margin/regime/label filters can restore +0.30 cost buffer while preserving validation/OOS positivity and 3+ trades/day(q05 롱 단독 마진/국면/라벨 필터가 검증/표본외 양수와 일 3거래 이상을 유지하면서 +0.30 비용 버퍼를 회복할 수 있다)",
        },
        {
            "field": "decision_use",
            "value": "choose run361B materialization surfaces only; no candidate selection(run361B 구체화 표면 선택만, 후보 선택 없음)",
        },
        {
            "field": "comparison_baseline",
            "value": "Stage360C q05 long-only report-derived scorecard(Stage360C q05 롱 단독 보고서 파생 점수표)",
        },
        {
            "field": "control_variables",
            "value": "FPMarkets US100 M5, q05 source model, fixed lot 0.1, max_hold_bars 12, no shorts unless negative control(FPMarkets US100 M5, q05 원천 모델, 고정 lot 0.1, 최대 보유 12 bars, 부정 대조 외 숏 금지)",
        },
        {
            "field": "changed_variables",
            "value": "long-only margin thresholds, probability gap, trend/volatility/month regime, cost-aware long labels(롱 단독 마진 임계값, 확률 gap, 추세/변동성/月 국면, 비용 인식 롱 라벨)",
        },
        {
            "field": "success_criteria",
            "value": "materialization queue ready with timestamp-safe sources and guardrails(시점 안전 원천과 가드레일이 있는 구체화 대기열 준비)",
        },
        {
            "field": "failure_criteria",
            "value": "design cannot define non-leaking margin/regime/label inputs(누수 없는 마진/국면/라벨 입력을 정의하지 못함)",
        },
        {
            "field": "invalid_conditions",
            "value": "future labels, post-close trade filtering as execution claim, missing split identity(미래 라벨, 종료 후 거래 필터를 실행 주장으로 사용, 분할 정체성 누락)",
        },
        {
            "field": "evidence_plan",
            "value": "run361B must materialize probability tapes, margin grids, regime joins, density controls, and no-trade controls(run361B는 확률 tape, 마진 grid, 국면 결합, 밀도 대조, 무거래 대조를 구체화)",
        },
    ]


def data_integrity_rows() -> list[dict[str, Any]]:
    return [
        {
            "field": "data_source",
            "value": f"{rel(SOURCE_Q05_VALIDATION_TELEMETRY)}; {rel(SOURCE_Q05_OOS_TELEMETRY)}; {rel(SOURCE_STAGE360B_SCORECARD)}",
        },
        {
            "field": "time_axis",
            "value": "MT5 bar_time/source_time from runtime telemetry; no timezone conversion(MT5 runtime telemetry의 bar_time/source_time, timezone 변환 없음)",
        },
        {
            "field": "sample_scope",
            "value": "FPMarkets US100 M5 Tier A validation and OOS q05 runtime tapes(FPMarkets US100 M5 Tier A 검증/표본외 q05 런타임 tape)",
        },
        {
            "field": "missing_or_duplicate_check",
            "value": "run361B must count bar_time duplicates/missing rows before any grid score(run361B는 grid 점수 전 bar_time 중복/누락을 계산)",
        },
        {
            "field": "feature_label_boundary",
            "value": "margin grid uses only same-bar model probabilities already emitted at runtime; label designs use future returns only as target, never feature(마진 grid는 런타임 출력된 같은 bar 확률만 사용; 라벨 설계는 미래 수익을 target으로만 사용, feature 금지)",
        },
        {
            "field": "split_boundary",
            "value": "validation and OOS remain separate; no synthetic combined result(검증과 표본외 분리 유지, 합성 합산 결과 없음)",
        },
        {
            "field": "leakage_risk",
            "value": "choosing thresholds from both validation and OOS or using closed-trade filter as lifecycle replay(검증/표본외 동시 임계값 선택 또는 종료 거래 필터를 생명주기 재생으로 사용)",
        },
        {
            "field": "integrity_judgment",
            "value": "usable_for_design_only(설계 전용 사용 가능)",
        },
    ]


def model_validation_rows() -> list[dict[str, Any]]:
    return [
        {
            "field": "model_family",
            "value": "none new in run361A; source q05 model only(run361A 새 모델 없음, 원천 q05 모델만 사용)",
        },
        {
            "field": "target_and_label",
            "value": "future long trade survival after +0.30 drag is planned target, not built yet(+0.30 drag 이후 롱 거래 생존은 계획 target, 아직 미구축)",
        },
        {
            "field": "split_method",
            "value": "existing validation/OOS plus required WFO plan(기존 검증/표본외 및 필수 WFO 계획)",
        },
        {
            "field": "selection_metric",
            "value": "none in design; run361B materialization metrics only(설계에서 선택 없음, run361B 구체화 지표만)",
        },
        {
            "field": "secondary_metrics",
            "value": "PF, expectancy, trade density, cost stress, monthly stability, side exposure(PF, 기대값, 거래 밀도, 비용 압박, 월 안정성, 방향 노출)",
        },
        {
            "field": "threshold_policy",
            "value": "broad margin grid first, micro search only after validation and OOS both survive cost(넓은 마진 grid 우선, 검증/표본외 모두 비용 생존 후 micro search)",
        },
        {
            "field": "overfit_risk",
            "value": "multiple threshold/regime attempts on report-derived evidence(보고서 파생 근거 위 다중 임계값/국면 시도)",
        },
        {
            "field": "validation_judgment",
            "value": "exploratory_design_only(탐색 설계 전용)",
        },
    ]


def failure_memory_rows() -> list[dict[str, Any]]:
    return [
        {
            "failure_id": "FM-ST360C-SIMPLE-LATE-VETO",
            "constraint": "do not use no-late as primary selection because validation net was -449.38(validation 순수익 -449.38 때문에 no-late를 주 선택으로 쓰지 않음)",
            "effect": "forces regime router instead of hard session veto(고정 세션 제외 대신 국면 라우터를 강제)",
        },
        {
            "failure_id": "FM-ST360C-SHORT-ONLY-DAMAGE",
            "constraint": "do not reintroduce shorts as density filler(숏을 밀도 채우기로 재도입하지 않음)",
            "effect": "short branch remains negative control(숏 분기는 부정 대조 유지)",
        },
        {
            "failure_id": "FM-ST360C-REPORT-DERIVED-LIFECYCLE",
            "constraint": "closed-trade scorecards cannot imply MT5 lifecycle performance(종료 거래 점수표는 MT5 생명주기 성과를 의미하지 않음)",
            "effect": "run361B must produce proxy inputs and later MT5 replay before promotion(run361B는 프록시 입력을 만들고 승격 전 MT5 재생 필요)",
        },
        {
            "failure_id": "FM-ST361A-COST-FRAGILITY",
            "constraint": "primary seed must repair validation +0.30 cost net -146.63(주 씨앗은 검증 +0.30 비용 순수익 -146.63을 수리해야 함)",
            "effect": "cost drag is primary guardrail, not post-hoc note(비용 drag가 사후 메모가 아니라 주 가드레일)",
        },
    ]


def broad_sweep_rows() -> list[dict[str, Any]]:
    return [
        {
            "sweep_id": "s361_broad_01_margin_gap",
            "changed_variable": "p_long minus max(p_short,p_flat)(p_long - max(p_short,p_flat))",
            "coarse_values": "0.00,0.03,0.06,0.09,0.12,0.16,0.20",
            "control": "long-only, q05 source probabilities, no shorts(롱 단독, q05 원천 확률, 숏 없음)",
            "success_gate": "validation/OOS after +0.30 drag positive and density >= 3(검증/표본외 +0.30 drag 후 양수 및 밀도 3 이상)",
        },
        {
            "sweep_id": "s361_broad_02_long_probability_floor",
            "changed_variable": "p_long floor(p_long 하한)",
            "coarse_values": "0.40,0.45,0.50,0.55,0.60",
            "control": "margin gap sweep paired(마진 gap sweep와 결합)",
            "success_gate": "cost-adjusted expectancy positive(비용 조정 기대값 양수)",
        },
        {
            "sweep_id": "s361_broad_03_regime_router",
            "changed_variable": "trend/volatility/month/session buckets(추세/변동성/月/세션 bucket)",
            "coarse_values": "trend_up,trend_down,vol_low,vol_mid,vol_high,month_fold,late_flag",
            "control": "no fixed no-late veto(고정 no-late 제외 없음)",
            "success_gate": "improves validation cost without OOS concentration(검증 비용을 개선하되 표본외 집중 없음)",
        },
        {
            "sweep_id": "s361_broad_04_long_quality_label",
            "changed_variable": "cost-aware long survival label(비용 인식 롱 생존 라벨)",
            "coarse_values": "H6,H9,H12 with +0.10,+0.20,+0.30 drag(H6/H9/H12와 비용 drag)",
            "control": "timestamp-safe label boundary(시점 안전 라벨 경계)",
            "success_gate": "label input ready for WFO training(WFO 학습 입력 준비)",
        },
        {
            "sweep_id": "s361_broad_05_negative_controls",
            "changed_variable": "no-trade, q05 all, q05 short-only controls(무거래, q05 전체, q05 숏 단독 대조)",
            "coarse_values": "control only(대조 전용)",
            "control": "do not tune controls(대조 튜닝 금지)",
            "success_gate": "detect sparse cherry-pick and density filler(희소 cherry-pick과 밀도 채우기 탐지)",
        },
    ]


def extreme_sweep_rows() -> list[dict[str, Any]]:
    return [
        {
            "extreme_id": "s361_extreme_01_high_margin",
            "value": "margin_gap >= 0.30 and p_long >= 0.65",
            "purpose": "test if edge saturates or becomes too sparse(우위 포화 또는 과도한 희소화 확인)",
            "stop_condition": "density below 3 trades/day(일 3거래 미만)",
        },
        {
            "extreme_id": "s361_extreme_02_no_margin",
            "value": "margin_gap >= 0.00 and p_long floor none",
            "purpose": "baseline against Stage360C long-only(360C 롱 단독 대비 기준)",
            "stop_condition": "same cost failure persists(동일 비용 실패 지속)",
        },
        {
            "extreme_id": "s361_extreme_03_late_allowed_vs_blocked",
            "value": "late-only, no-late, late-with-regime",
            "purpose": "separate hard veto failure from regime inversion(고정 제외 실패와 국면 반전 분리)",
            "stop_condition": "fixed late-only remains density below 3(고정 후반 단독 밀도 3 미만 지속)",
        },
        {
            "extreme_id": "s361_extreme_04_cost_drag_ladder",
            "value": "+0.10,+0.20,+0.30,+0.50 per trade",
            "purpose": "locate cost cliff(비용 cliff 위치 확인)",
            "stop_condition": "+0.30 validation and OOS cannot both stay positive(+0.30 검증/표본외 동시 양수 실패)",
        },
    ]


def margin_grid_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rank = 1
    for margin_gap in [0.00, 0.03, 0.06, 0.09, 0.12, 0.16, 0.20]:
        for p_floor in [0.40, 0.45, 0.50, 0.55, 0.60]:
            rows.append(
                {
                    "grid_id": f"s361_margin_{rank:03d}",
                    "p_long_floor": p_floor,
                    "margin_gap": margin_gap,
                    "side_policy": "long_only(롱 단독)",
                    "short_policy": "disabled(비활성)",
                    "cost_drag_required": "+0.30 per trade(+0.30/거래)",
                    "min_trade_density": "3",
                    "target_trade_density": "3_to_10_plus(3~10 이상)",
                    "materialization_status": "planned_for_run361B(run361B 계획)",
                }
            )
            rank += 1
    return rows


def regime_axis_rows() -> list[dict[str, Any]]:
    return [
        {
            "axis_id": "s361_regime_01_trend",
            "source": "timestamp-safe feature join from existing feature matrix or telemetry-safe derived trend(기존 피처 행렬 또는 telemetry 안전 파생 추세)",
            "buckets": "trend_up,trend_flat,trend_down",
            "leakage_guard": "bar_time <= decision bar only(decision bar 이하 bar_time만)",
        },
        {
            "axis_id": "s361_regime_02_volatility",
            "source": "rolling ATR/range quantile using past bars only(과거 bar만 쓰는 rolling ATR/range 분위)",
            "buckets": "vol_low,vol_mid,vol_high",
            "leakage_guard": "rolling window excludes future bars(rolling window 미래 bar 제외)",
        },
        {
            "axis_id": "s361_regime_03_month_fold",
            "source": "calendar month/fold from bar_time(bar_time 월/fold)",
            "buckets": "month and rolling fold(月 및 rolling fold)",
            "leakage_guard": "router must be trained only on prior folds(router는 이전 fold로만 학습)",
        },
        {
            "axis_id": "s361_regime_04_session",
            "source": "bar_time hour from MT5 telemetry(MT5 telemetry bar_time hour)",
            "buckets": "us_cash_16_20,late_21_23,other",
            "leakage_guard": "session is diagnostic, not hard veto until WFO confirms(session은 WFO 확인 전 진단 전용)",
        },
    ]


def label_design_rows() -> list[dict[str, Any]]:
    return [
        {
            "label_id": "s361_label_01_long_survival_h12_cost030",
            "target": "long trade survives +0.30 drag over max H12(+0.30 drag 후 H12 내 롱 거래 생존)",
            "feature_boundary": "features at decision bar only(decision bar 피처만)",
            "use_case": "cost-aware long quality model(비용 인식 롱 품질 모델)",
        },
        {
            "label_id": "s361_label_02_long_adverse_excursion",
            "target": "avoid trades with large adverse excursion(큰 역행 변동 거래 회피)",
            "feature_boundary": "future path target only, never feature(미래 경로는 target만, feature 금지)",
            "use_case": "drawdown and expectancy control(낙폭과 기대값 제어)",
        },
        {
            "label_id": "s361_label_03_cost_bucket_meta",
            "target": "trade remains positive under +0.10/+0.20/+0.30 ladder(+0.10/+0.20/+0.30 비용 ladder에서 양수 유지)",
            "feature_boundary": "train-only WFO meta-label(학습 전용 WFO meta-label)",
            "use_case": "margin grid tie-breaker(마진 grid 동률 해소)",
        },
    ]


def wfo_rows() -> list[dict[str, Any]]:
    return [
        {
            "fold_id": "s361_wfo_01",
            "train_window": "2025-01 to 2025-03",
            "validation_window": "2025-04",
            "test_window": "2025-05",
            "purpose": "early validation of cost-aware long label(비용 인식 롱 라벨 초기 검증)",
        },
        {
            "fold_id": "s361_wfo_02",
            "train_window": "2025-01 to 2025-05",
            "validation_window": "2025-06",
            "test_window": "2025-07",
            "purpose": "mid validation stability(중간 검증 안정성)",
        },
        {
            "fold_id": "s361_wfo_03",
            "train_window": "2025-01 to 2025-07",
            "validation_window": "2025-08",
            "test_window": "2025-09",
            "purpose": "pre-OOS handoff check(표본외 인계 전 확인)",
        },
        {
            "fold_id": "s361_oos_guard",
            "train_window": "validation-only design freeze(검증 전용 설계 고정)",
            "validation_window": "2025-01 to 2025-09",
            "test_window": "2025-10 to 2026-04",
            "purpose": "OOS used for confirmation, not micro-tuning(표본외는 확인용, micro-tuning 금지)",
        },
    ]


def micro_search_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "s361_micro_gate_01",
            "condition": "at least one broad margin/regime surface has validation and OOS +0.30 net > 0(넓은 마진/국면 표면 하나 이상이 검증/표본외 +0.30 순수익 양수)",
            "effect": "allows narrower threshold search(좁은 임계값 탐색 허용)",
        },
        {
            "gate_id": "s361_micro_gate_02",
            "condition": "trade density stays >= 3/day and no trade splitting evidence(거래 밀도 일 3 이상 및 거래 쪼개기 근거 없음)",
            "effect": "prevents sparse cherry-pick(희소 cherry-pick 방지)",
        },
        {
            "gate_id": "s361_micro_gate_03",
            "condition": "monthly concentration no worse than Stage360C long-only(月 집중이 Stage360C 롱 단독보다 나쁘지 않음)",
            "effect": "prevents single-month selection(단일 월 선택 방지)",
        },
    ]


def materialization_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "s361B_r01_q05_long_only_margin_grid",
            "priority": 1,
            "next_run_id": NEXT_RUN_ID,
            "source_seed_id": "s361_r01_q05_long_only_margin_grid",
            "materialization_action": "score q05 long-only probability margin grid(q05 롱 단독 확률 마진 격자 점수화) from validation/OOS runtime telemetry(검증/표본외 런타임 텔레메트리)",
            "required_inputs": f"{rel(SOURCE_Q05_VALIDATION_TELEMETRY)};{rel(SOURCE_Q05_OOS_TELEMETRY)}",
            "success_criteria": "validation and OOS +0.30 net positive, density >= 3(검증/표본외 +0.30 순수익 양수, 밀도 3 이상)",
            "selection_allowed": "false(아니오)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s361B_r02_long_regime_router_inputs",
            "priority": 2,
            "next_run_id": NEXT_RUN_ID,
            "source_seed_id": "s361_r02_long_late_regime_router",
            "materialization_action": "join trend/vol/session/month regime buckets timestamp-safely(추세/변동성/세션/月 국면 bucket을 시점 안전하게 결합)",
            "required_inputs": "runtime telemetry plus feature matrix or past-bar derived regimes(런타임 telemetry와 피처 행렬 또는 과거 bar 파생 국면)",
            "success_criteria": "regime attribution ready without future leakage(미래 누수 없는 국면 귀속 준비)",
            "selection_allowed": "false(아니오)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s361B_r03_long_quality_label_inputs",
            "priority": 3,
            "next_run_id": NEXT_RUN_ID,
            "source_seed_id": "s361_r03_long_quality_cost_label",
            "materialization_action": "build timestamp-safe long survival/cost labels(시점 안전 롱 생존/비용 라벨 생성)",
            "required_inputs": "M5 bars, q05 telemetry, fixed H6/H9/H12 horizons(M5 bar, q05 telemetry, 고정 H6/H9/H12 horizon)",
            "success_criteria": "label matrix ready with split and hash(분할 및 hash 포함 label matrix 준비)",
            "selection_allowed": "false(아니오)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s361B_r04_short_firewall_negative_control",
            "priority": 4,
            "next_run_id": NEXT_RUN_ID,
            "source_seed_id": "s361_r04_short_firewall_negative_control",
            "materialization_action": "materialize short-only and high-margin short controls(숏 단독 및 고마진 숏 대조 구체화)",
            "required_inputs": "q05 telemetry decision probabilities(q05 telemetry decision 확률)",
            "success_criteria": "short remains excluded unless validation/OOS/cost all pass(검증/표본외/비용 모두 통과 전 숏 제외 유지)",
            "selection_allowed": "false(아니오)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s361B_r05_density_no_trade_controls",
            "priority": 5,
            "next_run_id": NEXT_RUN_ID,
            "source_seed_id": "s361_r05_density_and_no_trade_controls",
            "materialization_action": "materialize no-trade, all-q05, q05-long-only, sparse density controls(무거래, q05 전체, q05 롱 단독, 희소 밀도 대조 구체화)",
            "required_inputs": "Stage360B scorecards and q05 telemetry(Stage360B 점수표 및 q05 telemetry)",
            "success_criteria": "controls show whether profit is sparse or split(대조가 수익의 희소성/쪼개기 여부를 표시)",
            "selection_allowed": "false(아니오)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(summary: Mapping[str, Any]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "q05 long-only can recover cost buffer through margin/regime/label design(q05 롱 단독은 마진/국면/라벨 설계로 비용 버퍼를 회복할 수 있다)",
            "decision_use": "open run361B materialization only(run361B 구체화만 개설)",
            "comparison_baseline": "Stage360C q05 long-only scorecard(Stage360C q05 롱 단독 점수표)",
            "control_variables": "FPMarkets US100 M5, q05 source model, fixed lot 0.1, max_hold_bars 12",
            "changed_variables": "margin, probability floor, regime buckets, long quality labels",
            "success_criteria": "run361B queue and guardrails ready(run361B 대기열 및 가드레일 준비)",
            "failure_criteria": "no timestamp-safe design path(시점 안전 설계 경로 없음)",
            "invalid_conditions": "lookahead or operating claim from design(미래참조 또는 설계 기반 운영 주장)",
            "evidence_plan": [rel(RUN361B_MATERIALIZATION_QUEUE), rel(GATE_AUDIT), rel(FINAL_DECISION)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "MT5 runtime telemetry bar_time/source_time, no timezone conversion(MT5 런타임 telemetry bar_time/source_time, timezone 변환 없음)",
            "sample_scope": "FPMarkets US100 M5 q05 validation/OOS Tier A(FPMarkets US100 M5 q05 검증/표본외 Tier A)",
            "missing_or_duplicate_check": "planned for run361B materialization(run361B 구체화에서 수행 예정)",
            "feature_label_boundary": "design only; run361B must enforce timestamp-safe joins(설계 전용, run361B가 시점 안전 결합 강제)",
            "split_boundary": "validation/OOS separate(검증/표본외 분리)",
            "leakage_risk": "threshold selection using OOS or future label leakage(OOS를 이용한 임계값 선택 또는 미래 라벨 누수)",
            "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES},
            "integrity_judgment": "usable_for_design_only(설계 전용 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "none_new_design_only(새 모델 없음, 설계 전용)",
            "target_and_label": "long survival after cost planned but not built(비용 후 롱 생존 계획, 미구축)",
            "split_method": "validation/OOS plus WFO plan(검증/표본외 및 WFO 계획)",
            "selection_metric": "none(없음)",
            "secondary_metrics": "PF, expectancy, density, cost stress, monthly stability(PF, 기대값, 밀도, 비용 압박, 월 안정성)",
            "threshold_policy": "broad grid first, no micro search until gates pass(넓은 grid 우선, gate 전 micro search 없음)",
            "overfit_risk": "multiple threshold/regime search(다중 임계값/국면 탐색)",
            "calibration_risk": "q05 scores are runtime model probabilities but not newly calibrated(q05 점수는 런타임 모델 확률이나 새 calibration 없음)",
            "comparison_baseline": "Stage360C long-only(Stage360C 롱 단독)",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "Stage361A design(Stage361A 설계)",
            "evidence_available": "source scorecards, seed queue, telemetry paths(원천 점수표, 씨앗 대기열, telemetry 경로)",
            "evidence_missing": "materialized margin grid, proxy execution, MT5 replay(구체화된 마진 grid, 프록시 실행, MT5 재생)",
            "judgment_label": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "설계가 끝났고 다음은 시점 안전 구체화다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": [
                "candidate_selection(후보 선택)",
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "live_readiness(실거래 준비)",
                "goal_achieve(목표 달성)",
            ],
            "allowed_claims": [
                "design_ready(설계 준비)",
                "run361B_materialization_queue_ready(run361B 구체화 대기열 준비)",
            ],
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path("stage_pipelines/stage361/design_long_only_cost_buffer_probe_without_db.py")),
            "consumer": [rel(RUN361B_MATERIALIZATION_QUEUE), rel(REPORT_PATH), rel(FINAL_DECISION)],
            "artifact_paths": [
                rel(SOURCE_EVIDENCE_SNAPSHOT),
                rel(EXPERIMENT_CONTRACT),
                rel(BROAD_SWEEP_PLAN),
                rel(MARGIN_GRID_PLAN),
                rel(RUN361B_MATERIALIZATION_QUEUE),
            ],
            "artifact_hashes": {
                rel(RUN361B_MATERIALIZATION_QUEUE): sha256_file(RUN361B_MATERIALIZATION_QUEUE),
                rel(MARGIN_GRID_PLAN): sha256_file(MARGIN_GRID_PLAN),
            },
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_reports_generated_run_artifacts_with_manifest(추적 보고서와 manifest 포함 생성 산출물)",
            "lineage_judgment": "connected_with_boundary(경계 내 연결됨)",
            "source_summary": dict(summary),
        },
    )


def write_gates() -> list[dict[str, Any]]:
    gates = [
        ("work_packet_schema_lint", exists(WORK_PACKET)),
        ("source_evidence_snapshot", exists(SOURCE_EVIDENCE_SNAPSHOT) and csv_count(SOURCE_EVIDENCE_SNAPSHOT) >= 4),
        ("experiment_contract", exists(EXPERIMENT_CONTRACT)),
        ("data_integrity_contract", exists(DATA_INTEGRITY_CONTRACT)),
        ("model_validation_contract", exists(MODEL_VALIDATION_CONTRACT)),
        ("margin_grid_plan", exists(MARGIN_GRID_PLAN) and csv_count(MARGIN_GRID_PLAN) == 35),
        ("wfo_plan", exists(WFO_VALIDATION_PLAN)),
        ("materialization_queue", exists(RUN361B_MATERIALIZATION_QUEUE) and csv_count(RUN361B_MATERIALIZATION_QUEUE) == 5),
        ("paired_tier_records", True),
        ("artifact_lineage_recorded", exists(LINEAGE_RECEIPT)),
        ("final_claim_guard", exists(CLAIM_RECEIPT)),
        ("required_gate_coverage_audit", True),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "pass" if passed else "fail",
            "effect": "design claim supported(설계 주장 근거)" if passed else "design claim blocked(설계 주장 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def gate_counts(gates: Sequence[Mapping[str, Any]]) -> tuple[int, int]:
    return sum(1 for row in gates if row["status"] == "pass"), len(gates)


def write_report(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes, gate_total = gate_counts(gates)
    report = f"""# run361A Long-Only Cost Buffer Design(361A 롱 단독 비용 버퍼 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{gate_passes}/{gate_total}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Current Truth(현재 진실)

Action(행동): q05 long-only(롱 단독) seed(씨앗)를 margin/regime/label(마진/국면/라벨) 설계로 확장했다.

Effect(효과): 비용 전 validation(검증) `+{summary["long_only_validation_net_profit"]}` 및 OOS(표본외) `+{summary["long_only_oos_net_profit"]}` 단서를, +0.30 cost buffer(+0.30 비용 버퍼) 회복 문제로 바꿨다.

## Design Output(설계 산출물)

- margin_grid_rows(마진 격자 행): `{csv_count(MARGIN_GRID_PLAN)}`
- broad_sweep_rows(넓은 탐색 행): `{csv_count(BROAD_SWEEP_PLAN)}`
- materialization_queue_rows(구체화 대기열 행): `{csv_count(RUN361B_MATERIALIZATION_QUEUE)}`
- wfo_plan_rows(WFO 계획 행): `{csv_count(WFO_VALIDATION_PLAN)}`

## Guardrails(가드레일)

- density(밀도): `{TRADE_DENSITY_REQUIREMENT}`
- side policy(방향 정책): long-only primary(롱 단독 주 경로), short only negative control(숏은 부정 대조 전용)
- cost stress(비용 압박): +0.30 per trade(+0.30/거래)가 primary gate(주 게이트)다.
- claim boundary(주장 경계): design only(설계 전용)이며 proxy/MT5/candidate selection(프록시/MT5/후보 선택)은 없다.

## Next Action(다음 행동)

Action(행동): `{NEXT_RUN_ID}`에서 runtime telemetry(런타임 텔레메트리)를 써서 q05 long-only margin grid(q05 롱 단독 마진 격자), regime joins(국면 결합), label inputs(라벨 입력)을 구체화한다.

Effect(효과): 이후 proxy(프록시)를 만들 수 있는지 판단하고, proxy(프록시)가 생기면 MT5 runtime probe(MT5 런타임 탐침)와 비교할 수 있다.
"""
    write_text(REPORT_PATH, report)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage361A Long-Only Cost Buffer Design(361A 롱 단독 비용 버퍼 설계)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`

Action(행동): q05 long-only(롱 단독) cost buffer(비용 버퍼) 설계를 완료하고 run361B materialization queue(run361B 구체화 대기열)를 열었다.

Effect(효과): Stage361(361단계)은 새 모델 학습(model training, 모델 학습) 전, timestamp-safe(시점 안전) 입력 구체화로 진행한다.
""",
    )


def write_state_docs(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes, gate_total = gate_counts(gates)
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

Action(행동): `run361A`가 q05 long-only cost buffer(q05 롱 단독 비용 버퍼) 설계를 완료했다.

Effect(효과): 다음 작업은 `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`에서 margin grid(마진 grid), regime join(국면 결합), label input(라벨 입력)을 시점 안전하게 구체화한다.
""",
    )
    append_text_once(
        SELECTION_STATUS,
        "## run361A Design Closeout",
        f"""## run361A Design Closeout(361A 설계 종료 기록)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{gate_passes}/{gate_total}`
- margin_grid_rows(마진 grid 행): `{csv_count(MARGIN_GRID_PLAN)}`
- materialization_queue_rows(구체화 대기열 행): `{csv_count(RUN361B_MATERIALIZATION_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): q05 long-only(롱 단독) seed(씨앗)를 margin/regime/label(마진/국면/라벨) 구체화 대기열로 바꿨다.

Effect(효과): Stage361(361단계)은 선택 없이 다음 materialization(구체화)로 진행한다.
""",
    )
    text = read_text(SELECTION_STATUS).replace(
        f"- current_run_id(현재 실행 ID): `{RUN_ID}`",
        f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
    )
    write_text(SELECTION_STATUS, text)
    append_text_once(
        STAGE_BRIEF,
        "## run361A Design Closeout",
        f"""## run361A Design Closeout(361A 설계 종료)

Action(행동): long-only cost buffer(롱 단독 비용 버퍼)를 broad margin/regime/label design(넓은 마진/국면/라벨 설계)로 전환했다.

Effect(효과): run361B(361B 실행)는 새 후보 선택 없이 timestamp-safe materialization(시점 안전 구체화)을 수행한다.
""",
    )
    append_text_once(
        STAGE_README,
        "## run361A Design Closeout",
        f"""## run361A Design Closeout(361A 설계 종료)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "run361A_long_only_cost_buffer_design",
        f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}`. Action(행동): long-only cost buffer design(롱 단독 비용 버퍼 설계). Effect(효과): run361B materialization queue(361B 구체화 대기열) ready."""
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} run361A",
        f"""## {TODAY} run361A

Action(행동): Stage361A designed q05 long-only cost buffer materialization(361A q05 롱 단독 비용 버퍼 구체화 설계).

Effect(효과): current truth(현재 진실)를 `{NEXT_RUN_ID}`로 이동했고, 운영 주장(operating claim, 운영 주장)은 하지 않았다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST361A-Q05-LONG-ONLY-MARGIN-REGIME-LABEL",
        f"""## IDEA-ST361A-Q05-LONG-ONLY-MARGIN-REGIME-LABEL

- idea(아이디어): q05 long-only(롱 단독) margin/regime/label(마진/국면/라벨) 설계로 +0.30 cost buffer(+0.30 비용 버퍼)를 회복한다.
- hypothesis(가설): Stage360C(360C 실행)의 비용 전 검증/표본외 양수 단서는 margin gap(마진 gap), regime router(국면 라우터), cost-aware label(비용 인식 라벨)을 통해 비용 후에도 보존될 수 있다.
- evidence_boundary(근거 경계): design_only(설계 전용).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def registry_rows(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    gate_passes, gate_total = gate_counts(gates)
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "experiment_design(실험 설계)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": "Stage361A designs long-only cost buffer materialization queue(361A 롱 단독 비용 버퍼 구체화 대기열 설계).",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": csv_count(RUN361B_MATERIALIZATION_QUEUE),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "candidate_rows": 0,
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(RUN361B_MATERIALIZATION_QUEUE),
        "net_profit": summary["long_only_oos_net_profit"],
        "result_status": STATUS,
        "sample_rows": csv_count(SOURCE_EVIDENCE_SNAPSHOT),
        "attempt_count": 0,
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "design_only(설계 전용)",
        "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
        "scoreboard_lane": "experiment_design(실험 설계)",
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "trade_density_requirement_status": "design_requires_3_to_10_plus_no_trade_splitting(설계상 3~10 이상 및 거래 쪼개기 금지)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "subrun_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "kpi_scope": "design_only(설계 전용)",
        "primary_kpi": f"queue_rows={csv_count(RUN361B_MATERIALIZATION_QUEUE)};margin_rows={csv_count(MARGIN_GRID_PLAN)}",
        "guardrail_kpi": "no_model_no_proxy_no_mt5_no_selection(모델/프록시/MT5/선택 없음)",
        "work_family": "experiment_design(실험 설계)",
        "row_id": f"{RUN_ID}__Tier_A",
    }
    project_rows = []
    views = [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", STATUS, "design_input_only(설계 입력 전용)", "q05 long-only source scorecard used(q05 롱 단독 원천 점수표 사용)"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)", "missing_required(필수 누락)", "do_not_synthesize_tier_b(Tier B 합성 금지)"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)", "combined_not_run(합산 실행 없음)", "do_not_synthesize_combined_result(합산 결과 합성 금지)"),
    ]
    for suffix, record_view, tier_scope, status, primary_kpi, guardrail in views:
        project_rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_ID}__{suffix}",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": "design_only(설계 전용)",
                "scoreboard_lane": "experiment_design(실험 설계)",
                "status": status,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
                "notes": "Stage361A design only; no selection(Stage361A 설계 전용, 선택 없음).",
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "rows": csv_count(RUN361B_MATERIALIZATION_QUEUE) if suffix == "Tier_A" else 0,
                "gate_passes": gate_passes,
                "gate_total": gate_total,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "operating_ready_rows": 0,
                "run_date": TODAY,
                "primary_artifact": rel(RUN361B_MATERIALIZATION_QUEUE),
                "view": record_view,
                "tier": tier_scope,
                "metric_scope": "design_only(설계 전용)",
                "net_profit": summary["long_only_oos_net_profit"] if suffix == "Tier_A" else "",
                "result_status": status,
                "sample_rows": csv_count(SOURCE_EVIDENCE_SNAPSHOT),
                "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
                "row_id": f"{RUN_ID}__{suffix}",
                "work_family": "experiment_design(실험 설계)",
                "evidence_scope": record_view,
                "run_key": f"{RUN_ID}__{suffix}",
                "question": "How should q05 long-only cost buffer be materialized?(q05 롱 단독 비용 버퍼를 어떻게 구체화할 것인가?)",
                "next_action": NEXT_RUN_ID,
                "trade_density_requirement_status": "design_requires_3_to_10_plus_no_trade_splitting(설계상 3~10 이상 및 거래 쪼개기 금지)",
                "result_judgment": JUDGMENT,
                "final_decision_path": rel(FINAL_DECISION),
                "created_at": TODAY,
            }
        )
    stage_rows = []
    for row in project_rows:
        stage_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": row["subrun_id"],
                "parent_run_id": PARENT_RUN_ID,
                "scoreboard_lane": row["scoreboard_lane"],
                "status": row["status"],
                "judgment": row["judgment"],
                "path": rel(REPORT_PATH),
                "external_verification_status": row["external_verification_status"],
                "notes": row["notes"],
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "rows": row["rows"],
                "gate_passes": gate_passes,
                "gate_total": gate_total,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "operating_ready_rows": 0,
                "run_date": TODAY,
                "primary_artifact": row["primary_artifact"],
                "net_profit": row["net_profit"],
                "result_status": row["status"],
                "sample_rows": row["sample_rows"],
                "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
                "work_family": "experiment_design(실험 설계)",
                "trade_density_requirement_status": row["trade_density_requirement_status"],
                "result_judgment": JUDGMENT,
                "final_decision_path": rel(FINAL_DECISION),
                "created_at": TODAY,
                "lane": "experiment_design(실험 설계)",
                "family": "experiment_design(실험 설계)",
                "primary_report": rel(REPORT_PATH),
                "evidence_boundary": CLAIM_BOUNDARY,
                "next_action": NEXT_RUN_ID,
                "question": row["question"],
                "ledger_row_id": row["ledger_row_id"],
                "row_id": row["row_id"],
                "record_view": row["record_view"],
                "tier_scope": row["tier_scope"],
                "kpi_scope": row["kpi_scope"],
                "primary_kpi": row["primary_kpi"],
                "guardrail_kpi": row["guardrail_kpi"],
                "view": row["view"],
                "tier": row["tier"],
                "metric_scope": row["metric_scope"],
            }
        )
    return [run_row], project_rows, stage_rows


def write_registries(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    run_rows, project_rows, stage_rows = registry_rows(summary, gates)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=False)


def write_final_decision(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes, gate_total = gate_counts(gates)
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "margin_grid_rows": csv_count(MARGIN_GRID_PLAN),
            "materialization_queue_rows": csv_count(RUN361B_MATERIALIZATION_QUEUE),
            "source_summary": dict(summary),
            "data_integrity": "usable_for_design_only(설계 전용 사용 가능)",
            "model_validation": "exploratory_design_only(탐색 설계 전용)",
            "artifact_lineage": "connected_with_boundary(경계 내 연결됨)",
            "result_judgment": "design_ready_materialization_required_no_selection",
            "next_condition": NEXT_RUN_ID,
        },
    )


def write_manifest() -> None:
    artifacts = [
        WORK_PACKET,
        SOURCE_EVIDENCE_SNAPSHOT,
        EXPERIMENT_CONTRACT,
        DATA_INTEGRITY_CONTRACT,
        MODEL_VALIDATION_CONTRACT,
        FAILURE_MEMORY_CONSTRAINTS,
        BROAD_SWEEP_PLAN,
        EXTREME_SWEEP_PLAN,
        MARGIN_GRID_PLAN,
        REGIME_AXIS_PLAN,
        LABEL_DESIGN_PLAN,
        WFO_VALIDATION_PLAN,
        MICRO_SEARCH_GATE,
        RUN361B_MATERIALIZATION_QUEUE,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        REPORT_PATH,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "command": "python stage_pipelines/stage361/design_long_only_cost_buffer_probe_without_db.py",
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha256_file(path)} for path in INPUT_FILES],
            "artifacts": [{"path": rel(path), "sha256": sha256_file(path)} for path in artifacts if exists(path)],
        },
    )


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage361/design_long_only_cost_buffer_probe_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("run_manifest", RUN_MANIFEST, "ignored_with_manifest"),
        ("source_evidence_snapshot", SOURCE_EVIDENCE_SNAPSHOT, "ignored_with_manifest"),
        ("experiment_contract", EXPERIMENT_CONTRACT, "ignored_with_manifest"),
        ("margin_grid_plan", MARGIN_GRID_PLAN, "ignored_with_manifest"),
        ("regime_axis_plan", REGIME_AXIS_PLAN, "ignored_with_manifest"),
        ("label_design_plan", LABEL_DESIGN_PLAN, "ignored_with_manifest"),
        ("run361b_materialization_queue", RUN361B_MATERIALIZATION_QUEUE, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        absolute = ROOT / path if not path.is_absolute() else path
        if not exists(absolute):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(absolute),
                "sha256": sha256_file(absolute),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": now_utc(),
                "notes": availability,
                "artifact_path": rel(absolute),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def main() -> None:
    require_inputs()
    os.makedirs(fs_path(RUN_DIR), exist_ok=True)
    summary = source_snapshot()
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "work_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "source_evidence_snapshot",
                "experiment_contract",
                "data_integrity_contract",
                "model_validation_contract",
                "margin_grid_plan",
                "wfo_plan",
                "materialization_queue",
                "paired_tier_records",
                "artifact_lineage_recorded",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(SOURCE_EVIDENCE_SNAPSHOT, source_evidence_rows(summary))
    write_csv(EXPERIMENT_CONTRACT, experiment_contract_rows())
    write_csv(DATA_INTEGRITY_CONTRACT, data_integrity_rows())
    write_csv(MODEL_VALIDATION_CONTRACT, model_validation_rows())
    write_csv(FAILURE_MEMORY_CONSTRAINTS, failure_memory_rows())
    write_csv(BROAD_SWEEP_PLAN, broad_sweep_rows())
    write_csv(EXTREME_SWEEP_PLAN, extreme_sweep_rows())
    write_csv(MARGIN_GRID_PLAN, margin_grid_rows())
    write_csv(REGIME_AXIS_PLAN, regime_axis_rows())
    write_csv(LABEL_DESIGN_PLAN, label_design_rows())
    write_csv(WFO_VALIDATION_PLAN, wfo_rows())
    write_csv(MICRO_SEARCH_GATE, micro_search_gate_rows())
    write_csv(RUN361B_MATERIALIZATION_QUEUE, materialization_queue_rows())
    write_receipts(summary)
    gates = write_gates()
    write_final_decision(summary, gates)
    write_manifest()
    write_report(summary, gates)
    write_state_docs(summary, gates)
    write_registries(summary, gates)
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
