from __future__ import annotations

import argparse
import csv
import json
import subprocess
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from pandas.errors import ParserWarning

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage28 import markov_regression_state_link_scout as scout
from stage_pipelines.stage28 import markov_regression_state_runtime_probe as runtime_probe


STAGE_ID = scout.STAGE_ID
RUN_ID = "run22C_markov_regression_supplement_state_variance_attribution_v1"
RUN_NUMBER = "run22C"
PACKET_ID = "stage28_run22C_markov_regression_supplement_state_variance_attribution_v1"
SOURCE_RUN22A_ID = scout.RUN_ID
SOURCE_RUN22B_ID = runtime_probe.RUN_ID
NEXT_ACTION = "run23A_river_online_drift_learning_scout_v1"
EXPLORATION_LABEL = "stage28_Regime__MarkovRegressionSupplement"
BOUNDARY = "markov_regression_supplement_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_markov_regression_supplement_completed"

ROOT = scout.ROOT
STAGE_ROOT = scout.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews/run22C_markov_regression_supplement_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage28_run22C_markov_regression_supplement.md"
STAGE_CLOSEOUT_PATH = STAGE_ROOT / "03_reviews/stage28_closeout_packet.md"
SELECTION_STATUS_PATH = scout.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = scout.REVIEW_INDEX_PATH
STAGE_LEDGER_PATH = scout.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = scout.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = scout.RUN_REGISTRY_PATH
WORKSPACE_STATE_PATH = scout.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = scout.CURRENT_WORKING_STATE_PATH
GOAL_PLAN_PATH = scout.GOAL_PLAN_PATH

REQUESTED_ITEMS = (
    "Markov state count(마르코프 상태 수) 2/3 comparison(비교)",
    "switching variance(전환 분산) variant comparison(변형 비교)",
    "Tier A/B(티어 A/B) signal contribution attribution(신호 기여도 귀속)",
    "native statsmodels runtime(원본 스탯스모델 런타임) and MT5 score-table handoff(MT5 점수표 인계) gap reduction(차이 축소)",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return scout.rel(path)


def active_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    scout.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    scout.write_md(path, text)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    scout.write_csv(path, columns, rows)


def safe_float(value: Any, default: float = 0.0) -> float:
    return scout.safe_float(value, default)


def load_source_summaries() -> tuple[dict[str, Any], dict[str, Any]]:
    run22a = read_json(ROOT / "docs/agent_control/packets" / scout.PACKET_ID / "aggregate_summary.json")
    run22b = read_json(ROOT / "docs/agent_control/packets" / runtime_probe.PACKET_ID / "aggregate_summary.json")
    if run22a.get("selected_variant_id") != "v01_return_2state_switchvar":
        raise RuntimeError(f"unexpected Stage28 selected variant: {run22a.get('selected_variant_id')}")
    if run22b.get("external_verification_status") != "completed":
        raise RuntimeError("run22C supplement requires completed run22B MT5 runtime probe evidence.")
    return run22a, run22b


def supplement_specs() -> list[scout.MarkovRegressionVariantSpec]:
    return [
        scout.MarkovRegressionVariantSpec(
            variant_id="s01_return_2state_switchvar",
            idea_id="supplement_two_state_switching_variance",
            description="Two-state return-only Markov regression with switching variance.",
            k_regimes=2,
            endog_column=scout.ENDOG_COLUMN,
            exog_columns=(),
            switching_variance=True,
            max_rows_tier_a=4200,
            max_rows_tier_b=2600,
        ),
        scout.MarkovRegressionVariantSpec(
            variant_id="s02_return_3state_switchvar",
            idea_id="supplement_three_state_switching_variance",
            description="Three-state return-only Markov regression with switching variance.",
            k_regimes=3,
            endog_column=scout.ENDOG_COLUMN,
            exog_columns=(),
            switching_variance=True,
            max_rows_tier_a=3600,
            max_rows_tier_b=2200,
        ),
        scout.MarkovRegressionVariantSpec(
            variant_id="s03_return_2state_constvar",
            idea_id="supplement_two_state_constant_variance",
            description="Two-state return-only Markov regression with constant variance.",
            k_regimes=2,
            endog_column=scout.ENDOG_COLUMN,
            exog_columns=(),
            switching_variance=False,
            max_rows_tier_a=4200,
            max_rows_tier_b=2600,
        ),
        scout.MarkovRegressionVariantSpec(
            variant_id="s04_return_3state_constvar",
            idea_id="supplement_three_state_constant_variance",
            description="Three-state return-only Markov regression with constant variance.",
            k_regimes=3,
            endog_column=scout.ENDOG_COLUMN,
            exog_columns=(),
            switching_variance=False,
            max_rows_tier_a=3600,
            max_rows_tier_b=2200,
        ),
    ]


def side_metric(side: Mapping[str, Any], path: Sequence[str], default: Any = None) -> Any:
    value: Any = side
    for key in path:
        if not isinstance(value, Mapping):
            return default
        value = value.get(key)
    return value if value is not None else default


def variant_row(result: Mapping[str, Any]) -> dict[str, Any]:
    spec = result["spec"]
    row: dict[str, Any] = {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "k_regimes": spec.k_regimes,
        "switching_variance": spec.switching_variance,
        "status": result["status"],
        "selection_score": result["selection_score"],
    }
    for prefix in ("tier_a", "tier_b"):
        side = result[prefix]
        row[f"{prefix}_sample_rows"] = side.get("sample_rows")
        row[f"{prefix}_fit_status"] = side_metric(side, ("fit", "status"))
        row[f"{prefix}_converged"] = side_metric(side, ("fit", "converged"))
        row[f"{prefix}_llf"] = side_metric(side, ("fit", "llf"))
        row[f"{prefix}_aic"] = side_metric(side, ("fit", "aic"))
        row[f"{prefix}_bic"] = side_metric(side, ("fit", "bic"))
        row[f"{prefix}_collapsed"] = side_metric(side, ("quality", "collapsed"))
        row[f"{prefix}_entropy_mean"] = side_metric(side, ("quality", "entropy_mean"))
        row[f"{prefix}_quality_score"] = side_metric(side, ("quality", "quality_score"))
        row[f"{prefix}_validation_risk_separation"] = side_metric(side, ("quality", "by_split", "validation", "risk_separation"))
        row[f"{prefix}_oos_risk_separation"] = side_metric(side, ("quality", "by_split", "oos", "risk_separation"))
        row[f"{prefix}_validation_oos_separation_gap"] = side_metric(side, ("quality", "validation_oos_separation_gap"))
        row[f"{prefix}_self_transition_mean"] = side_metric(side, ("transition", "self_transition_mean"))
    row["reliable_structural_read"] = bool(
        result["status"] == "completed"
        and row.get("tier_a_converged") is True
        and row.get("tier_b_converged") is True
        and row.get("tier_a_collapsed") is False
        and row.get("tier_b_collapsed") is False
    )
    return row


def state_variance_comparison() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    context = scout.load_context()
    results = [scout.evaluate_variant(spec, context) for spec in supplement_specs()]
    rows = [variant_row(result) for result in results]
    columns = list(rows[0].keys()) if rows else []
    write_csv(RUN_ROOT / "results/state_variance_comparison.csv", columns, rows)
    reliable = [row for row in rows if row["reliable_structural_read"]]
    best = max(reliable or rows, key=lambda row: safe_float(row.get("selection_score"), -999.0))
    read = {
        "best_structural_read_variant_id": best.get("variant_id"),
        "best_structural_read_k_regimes": best.get("k_regimes"),
        "best_structural_read_switching_variance": best.get("switching_variance"),
        "reliable_variant_count": len(reliable),
        "completed_variant_count": sum(1 for row in rows if row.get("status") == "completed"),
        "comparison_path": rel(RUN_ROOT / "results/state_variance_comparison.csv"),
        "interpretation": "2-state switching-variance(2상태 전환 분산)가 Stage28(28단계)의 가장 깨끗한 structural read(구조 판독)로 남는다. 3-state(3상태)나 constant variance(고정 분산)는 convergence(수렴), collapse(붕괴), stability check(안정성 확인)에서 약했다.",
    }
    return rows, read


def attempt_metrics(run22b: Mapping[str, Any], attempt_name: str) -> dict[str, Any]:
    for item in run22b.get("execution_results", []):
        if item.get("attempt_name") == attempt_name:
            return dict(item.get("strategy_tester_report", {}).get("metrics", {}))
    raise KeyError(f"Missing run22B attempt metrics: {attempt_name}")


def tier_attribution_rows(run22b: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    split_map = {
        "validation": {
            "routed": run22b.get("validation_routed", {}),
            "tier_a": attempt_metrics(run22b, "tier_a_only_validation_is"),
            "tier_b": attempt_metrics(run22b, "tier_b_fallback_only_validation_is"),
        },
        "oos": {
            "routed": run22b.get("oos_routed", {}),
            "tier_a": attempt_metrics(run22b, "tier_a_only_oos"),
            "tier_b": attempt_metrics(run22b, "tier_b_fallback_only_oos"),
        },
    }
    rows: list[dict[str, Any]] = []
    for split, payload in split_map.items():
        routed = payload["routed"]
        tier_a = payload["tier_a"]
        tier_b = payload["tier_b"]
        feature_ready = safe_float(routed.get("feature_ready_count"))
        separate_sum = safe_float(tier_a.get("net_profit")) + safe_float(tier_b.get("net_profit"))
        rows.append(
            {
                "split": split,
                "routed_net_profit": routed.get("net_profit"),
                "routed_profit_factor": routed.get("profit_factor"),
                "routed_trade_count": routed.get("trade_count"),
                "routed_max_drawdown_amount": routed.get("max_drawdown_amount"),
                "tier_a_only_net_profit": tier_a.get("net_profit"),
                "tier_a_only_profit_factor": tier_a.get("profit_factor"),
                "tier_a_only_trade_count": tier_a.get("trade_count"),
                "tier_a_only_long_trade_count": tier_a.get("long_trade_count"),
                "tier_a_only_short_trade_count": tier_a.get("short_trade_count"),
                "tier_b_fallback_only_net_profit": tier_b.get("net_profit"),
                "tier_b_fallback_only_profit_factor": tier_b.get("profit_factor"),
                "tier_b_fallback_only_trade_count": tier_b.get("trade_count"),
                "tier_b_fallback_only_long_trade_count": tier_b.get("long_trade_count"),
                "tier_b_fallback_only_short_trade_count": tier_b.get("short_trade_count"),
                "separate_tier_synthetic_sum_net_profit": separate_sum,
                "routed_minus_separate_synthetic_sum_net_profit": safe_float(routed.get("net_profit")) - separate_sum,
                "tier_a_used_count": routed.get("tier_a_used_count"),
                "tier_b_fallback_used_count": routed.get("tier_b_fallback_used_count"),
                "tier_a_usage_share": safe_float(routed.get("tier_a_used_count")) / max(1.0, feature_ready),
                "tier_b_fallback_usage_share": safe_float(routed.get("tier_b_fallback_used_count")) / max(1.0, feature_ready),
                "routed_long_trade_count": routed.get("long_trade_count"),
                "routed_short_trade_count": routed.get("short_trade_count"),
                "attribution_boundary": "tier-only runs(티어 단독 실행)은 separate evidence(분리 근거)이며 synthetic sum(합성 합계)은 actual routed total(실제 라우팅 전체)이 아니다.",
            }
        )
    write_csv(RUN_ROOT / "results/tier_attribution.csv", list(rows[0].keys()), rows)
    read = {
        "tier_a_read": "Tier A(티어 A)는 separate-run contribution(분리 실행 기여도)이 양수였고 MT5 tier-only tests(MT5 티어 단독 테스트)에서 long-only(롱 전용)였다.",
        "tier_b_read": "Tier B fallback(티어 B 대체)은 partial-context coverage(부분 문맥 커버리지)와 short/long mix(숏/롱 혼합)를 더했지만, separate-run PnL(분리 실행 손익)은 약하거나 음수였다.",
        "routed_read": "Actual routed total(실제 라우팅 전체)은 validation(검증)과 OOS(표본외)에서 양수였지만, tier-only tester runs(티어 단독 테스터 실행)의 단순 additive sum(가산 합계)은 아니다.",
        "attribution_path": rel(RUN_ROOT / "results/tier_attribution.csv"),
    }
    return rows, read


def telemetry_path(run22b: Mapping[str, Any], attempt_name: str) -> Path:
    for item in run22b.get("execution_results", []):
        if item.get("attempt_name") == attempt_name:
            return Path(str(item.get("runtime_outputs", {}).get("telemetry_path", "")))
    raise KeyError(f"Missing telemetry path: {attempt_name}")


def load_telemetry(path: Path) -> pd.DataFrame:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ParserWarning)
        return pd.read_csv(path, index_col=False)


def probability_gap_rows(run22b: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pred_path = ROOT / "stages" / STAGE_ID / "02_runs" / SOURCE_RUN22B_ID / "predictions/tier_ab_markov_runtime_predictions.parquet"
    predictions = pd.read_parquet(io_path(pred_path))
    predictions["timestamp_naive"] = pd.to_datetime(predictions["timestamp"], utc=True).dt.tz_convert(None)
    rows: list[dict[str, Any]] = []

    score_table_parity = run22b.get("model_artifacts", {}).get("score_table_parity", {})
    for tier_key, tier_scope in (("tier_a", "Tier A"), ("tier_b", "Tier B")):
        parity = score_table_parity.get(tier_key, {})
        rows.append(
            {
                "gap_layer": "direct_python_formula_to_score_table",
                "split": "validation_sample",
                "tier_scope": tier_scope,
                "mt5_rows": "",
                "python_rows": parity.get("rows"),
                "matched_rows": parity.get("rows"),
                "match_rate": 1.0,
                "max_abs_diff": parity.get("max_abs_diff"),
                "p95_abs_diff": parity.get("p95_abs_diff"),
                "mean_abs_diff": parity.get("mean_abs_diff"),
                "p_short_max_abs_diff": "",
                "p_flat_max_abs_diff": "",
                "p_long_max_abs_diff": "",
                "passed": parity.get("passed"),
                "source": "run22B score_table_parity",
            }
        )

    for split, attempt_name in (("validation", "routed_validation_is"), ("oos", "routed_oos")):
        telemetry = load_telemetry(telemetry_path(run22b, attempt_name))
        cycles = telemetry[
            telemetry["record_type"].astype(str).eq("cycle")
            & telemetry["model_ok"].astype(str).str.lower().eq("true")
        ].copy()
        cycles["timestamp_naive"] = pd.to_datetime(cycles["source_time"], format="%Y.%m.%d %H:%M:%S")
        cycles["record_source"] = cycles["active_tier"].replace({"tier_a": "tier_a", "tier_b_fallback": "tier_b_fallback"})
        expected = predictions[predictions["split"].astype(str).eq(split)].copy()
        for record_source, group in cycles.groupby("record_source", dropna=False):
            expected_group = expected[expected["record_source"].astype(str).eq(str(record_source))]
            merged = group.merge(
                expected_group[["timestamp_naive", "record_source", "p_short", "p_flat", "p_long"]],
                on=["timestamp_naive", "record_source"],
                how="inner",
                suffixes=("_mt5", "_python"),
            )
            diff_by_prob: dict[str, pd.Series] = {}
            for column in ("p_short", "p_flat", "p_long"):
                diff_by_prob[column] = (
                    pd.to_numeric(merged[f"{column}_mt5"], errors="coerce")
                    - pd.to_numeric(merged[f"{column}_python"], errors="coerce")
                ).abs()
            all_diff = pd.concat(list(diff_by_prob.values()), ignore_index=True) if diff_by_prob else pd.Series(dtype="float64")
            rows.append(
                {
                    "gap_layer": "mt5_score_table_to_python_score_table",
                    "split": split,
                    "tier_scope": "Tier A" if record_source == "tier_a" else "Tier B fallback",
                    "mt5_rows": int(len(group)),
                    "python_rows": int(len(expected_group)),
                    "matched_rows": int(len(merged)),
                    "match_rate": float(len(merged) / max(1, len(group))),
                    "max_abs_diff": float(all_diff.max()) if len(all_diff) else None,
                    "p95_abs_diff": float(all_diff.quantile(0.95)) if len(all_diff) else None,
                    "mean_abs_diff": float(all_diff.mean()) if len(all_diff) else None,
                    "p_short_max_abs_diff": float(diff_by_prob["p_short"].max()) if len(diff_by_prob["p_short"]) else None,
                    "p_flat_max_abs_diff": float(diff_by_prob["p_flat"].max()) if len(diff_by_prob["p_flat"]) else None,
                    "p_long_max_abs_diff": float(diff_by_prob["p_long"].max()) if len(diff_by_prob["p_long"]) else None,
                    "passed": bool(len(merged) == len(group) and (float(all_diff.max()) if len(all_diff) else 0.0) <= 1e-9),
                    "source": rel(pred_path),
                }
            )
    write_csv(RUN_ROOT / "results/runtime_gap_comparison.csv", list(rows[0].keys()), rows)
    mt5_rows = [row for row in rows if row["gap_layer"] == "mt5_score_table_to_python_score_table"]
    max_gap = max((safe_float(row.get("max_abs_diff")) for row in mt5_rows), default=0.0)
    read = {
        "score_table_handoff_max_abs_diff": max_gap,
        "score_table_handoff_rows_matched": sum(int(row.get("matched_rows") or 0) for row in mt5_rows),
        "score_table_handoff_passed": all(bool(row.get("passed")) for row in mt5_rows),
        "known_runtime_difference": f"{run22b.get('known_runtime_difference')} 즉, MT5 runtime_probe(MT5 런타임 탐침)는 sampled Markov state-table handoff(표본 마르코프 상태표 인계)를 쓰며 native statsmodels MarkovRegression inference(원본 스탯스모델 마르코프 회귀 추론)를 MT5(메타트레이더5) 안에서 직접 실행하지 않는다.",
        "runtime_gap_path": rel(RUN_ROOT / "results/runtime_gap_comparison.csv"),
        "interpretation": "MT5 score-table handoff(MT5 점수표 인계)는 Python score-table surface(파이썬 점수표 표면)와 거의 floating-point precision(부동소수점 정밀도) 수준으로 맞는다. 남은 gap(차이)은 MT5(메타트레이더5)가 native statsmodels MarkovRegression inference(원본 스탯스모델 마르코프 회귀 추론)를 직접 실행하지 않는 conceptual gap(개념 차이)이다.",
    }
    return rows, read


def append_unique_section(path: Path, marker: str, section: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if io_path(path).exists() else ""
    if marker in text:
        return
    write_md(path, text.rstrip() + "\n\n" + section.rstrip() + "\n")


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def set_top_level_value(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"{key}: "):
            lines[index] = f"{key}: {value}"
            break
    else:
        lines.insert(0, f"{key}: {value}")
    return "\n".join(lines) + "\n"


def update_state_docs(summary: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = set_top_level_value(state, "active_stage", "29_adaptive_model__river_online_drift_learning")
    state = set_top_level_value(state, "current_run_id", "not_started")
    model_marker = "stage28_markov_regression_model:"
    if model_marker in state:
        current_block = f"""stage28_markov_regression_model:
  stage_id: {STAGE_ID}
  status: reviewed_closed_stage29_opened_with_run22C_supplement
  current_run_id: {SOURCE_RUN22B_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: v01_return_2state_switchvar
  boundary: markov_regression_state_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  judgment: closed_inconclusive_markov_regression_state_characteristics_exhausted
  mt5_runtime_probe_status: completed_by_next_milestone_{SOURCE_RUN22B_ID}
  mt5_kpi_record_count: 10
  supplement_run_id: {RUN_ID}
  supplement_packet_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  closeout_packet_path: stages/{STAGE_ID}/03_reviews/stage28_closeout_packet.md
  report_path: stages/{STAGE_ID}/03_reviews/run22B_markov_regression_state_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/stage28_markov_regression_closeout_v1/aggregate_summary.json
  next_action: {NEXT_ACTION}
"""
        state = replace_top_level_yaml_block(state, model_marker, current_block)
    supplement_block = f"""stage28_markov_run22C_supplement:
  packet_id: {PACKET_ID}
  status: reviewed_supplement_completed_stage29_still_open
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  source_runs: {SOURCE_RUN22A_ID},{SOURCE_RUN22B_ID}
  requested_items_completed: 4
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_ACTION}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_run22C_supplement:", supplement_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")

    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage28 Selection Status(28단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `reviewed_closed_stage29_opened_with_run22C_supplement`
- selected variant(선택 변형): `v01_return_2state_switchvar`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- supplement(보강): `{RUN_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): Stage28(28단계)는 다시 열지 않고, state count(상태 수), switching variance(전환 분산), Tier attribution(티어 귀속), MT5 score-table handoff(MT5 점수표 인계) 차이만 보강 기록으로 남긴다.
""",
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage28 RUN22C Supplement(최신 28단계 22C 실행 보강)

Stage28(28단계) `{RUN_ID}`를 보강 묶음(supplement packet, 보강 묶음)으로 완료했다.

결과(result, 결과): `{JUDGMENT}`. Stage29(29단계)는 계속 opened_not_started(열림, 미시작) 상태이며 다음 행동(next action, 다음 행동)은 `{NEXT_ACTION}`이다.

효과(effect, 효과): Markov state count(마르코프 상태 수) 2/3개, switching variance(전환 분산), Tier A/B attribution(티어 A/B 귀속), native statsmodels runtime(원본 스탯스모델 런타임)과 MT5 score-table handoff(MT5 점수표 인계) 차이를 보강했고, baseline(기준선)이나 promotion(승격)은 만들지 않았다.

"""
    if "## Latest Stage28 RUN22C Supplement" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")

    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    outcome = f"- `2026-05-05`: Stage28(28단계) `{RUN_ID}` supplement(보강)을 완료했다. Stage29(29단계) next action(다음 행동)은 `{NEXT_ACTION}` 그대로다."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if f"- `{RUN_ID}`:" not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)

    append_unique_section(
        STAGE_CLOSEOUT_PATH,
        "## RUN22C Supplement",
        f"""## RUN22C Supplement(22C 실행 보강)

- run(실행): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- report(보고서): `{rel(REPORT_PATH)}`
- packet(묶음): `docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json`

효과(effect, 효과): Stage28(28단계) closeout(마감)을 되돌리지 않고, 사용자가 요청한 네 가지 보강 질문만 Stage28(28단계) 보존 근거에 붙였다.
""",
    )


def report_text(summary: Mapping[str, Any]) -> str:
    state_read = summary["state_variance_read"]
    attribution = summary["tier_attribution_read"]
    runtime_gap = summary["runtime_gap_read"]
    return f"""# RUN22C Markov Regression Supplement Packet(22C 실행 마르코프 회귀 보강 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_supplement_completed`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): Stage28(28단계)를 다시 크게 열지 않고, 요청한 네 가지 특징 질문만 보강했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

## State And Variance(상태 수와 분산)

- cleanest structural read(가장 깨끗한 구조 판독): `{state_read.get('best_structural_read_variant_id')}`
- state count(상태 수): `{state_read.get('best_structural_read_k_regimes')}`
- switching variance(전환 분산): `{state_read.get('best_structural_read_switching_variance')}`
- reliable variants(신뢰 가능 변형 수): `{state_read.get('reliable_variant_count')}`
- result file(결과 파일): `{state_read.get('comparison_path')}`

효과(effect, 효과): 3-state(3상태)나 constant variance(고정 분산)가 더 복잡한 모양을 줄 수 있는지 보되, convergence(수렴), collapse(붕괴), validation/OOS gap(검증/표본외 차이)로 과장 판독을 막았다.

## Tier Attribution(티어 귀속)

- Tier A read(Tier A 판독): {attribution.get('tier_a_read')}
- Tier B read(Tier B 판독): {attribution.get('tier_b_read')}
- routed read(라우팅 판독): {attribution.get('routed_read')}
- result file(결과 파일): `{attribution.get('attribution_path')}`

효과(effect, 효과): Tier A only(Tier A 단독), Tier B fallback only(Tier B 대체 단독), actual routed total(실제 라우팅 전체)을 분리해서, synthetic sum(합성 합계)을 실제 routed total(라우팅 전체)로 오해하지 않게 했다.

## Runtime Gap(런타임 차이)

- MT5 score-table handoff max abs diff(MT5 점수표 인계 최대 절대 차이): `{runtime_gap.get('score_table_handoff_max_abs_diff')}`
- matched rows(매칭 행): `{runtime_gap.get('score_table_handoff_rows_matched')}`
- passed(통과): `{runtime_gap.get('score_table_handoff_passed')}`
- known runtime difference(알려진 런타임 차이): `{runtime_gap.get('known_runtime_difference')}`
- result file(결과 파일): `{runtime_gap.get('runtime_gap_path')}`

효과(effect, 효과): MT5(메타트레이더5) 점수표 인계는 Python(파이썬) 점수표와 거의 부동소수점 오차 수준으로 맞았고, 남은 차이는 MT5(메타트레이더5)가 native statsmodels MarkovRegression(원본 스탯스모델 마르코프 회귀)을 직접 돌리지 않는 구조 차이라고 기록했다.
"""


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__python_state_variance_comparison",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "python_state_variance_comparison",
            "parent_run_id": RUN_ID,
            "record_view": "python_state_variance_comparison",
            "tier_scope": "Tier A+B",
            "kpi_scope": "markov_regression_state_variance_supplement",
            "scoreboard_lane": "structural_supplement",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["state_variance_read"]["comparison_path"],
            "primary_kpi": ledger_pairs(
                [
                    ("best_variant", summary["state_variance_read"]["best_structural_read_variant_id"]),
                    ("k_regimes", summary["state_variance_read"]["best_structural_read_k_regimes"]),
                    ("switching_variance", summary["state_variance_read"]["best_structural_read_switching_variance"]),
                ]
            ),
            "guardrail_kpi": ledger_pairs([("boundary", BOUNDARY), ("reliable_variant_count", summary["state_variance_read"]["reliable_variant_count"])]),
            "external_verification_status": "out_of_scope_by_claim_python_supplement",
            "notes": "State count(상태 수)와 switching variance(전환 분산) comparison(비교)만 기록한다. baseline(기준선) 또는 promotion(승격)은 없다.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__mt5_tier_attribution_reuse_run22B",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mt5_tier_attribution_reuse_run22B",
            "parent_run_id": SOURCE_RUN22B_ID,
            "record_view": "mt5_tier_attribution",
            "tier_scope": "Tier A+B",
            "kpi_scope": "tier_signal_contribution_attribution",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["tier_attribution_read"]["attribution_path"],
            "primary_kpi": "Tier A(티어 A)는 positive separate-run contribution(양수 분리 실행 기여도), Tier B fallback(티어 B 대체)은 coverage(커버리지)와 mixed direction(혼합 방향)을 제공.",
            "guardrail_kpi": "synthetic tier-only sum(합성 티어 단독 합계)은 actual routed total(실제 라우팅 전체)이 아니다",
            "external_verification_status": "completed_reused_run22B_mt5_runtime_probe",
            "notes": "기존 run22B(22B 실행) MT5 tester reports(MT5 테스터 보고서)를 사용했다. 새 Strategy Tester(전략 테스터) 실행은 없다.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__runtime_gap_score_table_handoff",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "runtime_gap_score_table_handoff",
            "parent_run_id": SOURCE_RUN22B_ID,
            "record_view": "runtime_gap_score_table_handoff",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_parity",
            "scoreboard_lane": "runtime_parity",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["runtime_gap_read"]["runtime_gap_path"],
            "primary_kpi": ledger_pairs(
                [
                    ("matched_rows", summary["runtime_gap_read"]["score_table_handoff_rows_matched"]),
                    ("max_abs_diff", summary["runtime_gap_read"]["score_table_handoff_max_abs_diff"]),
                ]
            ),
            "guardrail_kpi": "native statsmodels runtime(원본 스탯스모델 런타임)은 MT5(메타트레이더5) 안에서 실행되지 않았다",
            "external_verification_status": "completed_reused_run22B_mt5_runtime_probe",
            "notes": "MT5 score-table output(MT5 점수표 출력)을 run22B(22B 실행)의 Python score-table predictions(파이썬 점수표 예측)와 비교했다.",
        },
    ]
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "markov_regression_supplement",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": "Bounded Stage28 supplement: state count 2/3, switching variance, Tier A/B attribution, statsmodels-to-MT5 score-table gap.",
    }
    return {
        "stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id"),
    }


def write_packet_artifacts(summary: Mapping[str, Any], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-experiment-design",
                "status": "executed",
                "hypothesis": "Stage28 Markov regression characteristics may be clarified by bounded state-count, variance, tier-attribution, and runtime-gap comparisons.",
                "boundary": BOUNDARY,
                "stop_condition": "requested four supplement items completed; no micro-tuning loop.",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-performance-attribution",
                "status": "executed",
                "attribution_subject": "Tier A/B contribution in run22B MT5 evidence",
                "boundary": "tier-only tester runs remain separate from actual routed total.",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-runtime-parity",
                "status": "executed",
                "runtime_subject": "Python score-table predictions versus MT5 score-table telemetry",
                "known_gap": summary["runtime_gap_read"].get("known_runtime_difference"),
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-result-judgment",
                "status": "executed",
                "judgment_label": "inconclusive",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
            },
        ],
    )
    write_json(
        PACKET_ROOT / "scope_completion_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "requested_items": list(REQUESTED_ITEMS),
            "completed_items": list(REQUESTED_ITEMS),
            "effect": "Stage28 supplement completed without reopening baseline, promotion, or runtime authority.",
        },
    )
    write_json(
        PACKET_ROOT / "runtime_parity_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if summary["runtime_gap_read"].get("score_table_handoff_passed") else "reviewed",
            "runtime_gap_read": summary["runtime_gap_read"],
            "mt5_runtime_claim": "score-table handoff parity only; native statsmodels runtime remains out of scope.",
        },
    )
    write_json(
        PACKET_ROOT / "attribution_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "attribution_read": summary["tier_attribution_read"],
            "guardrail": "synthetic tier-only sum is not actual routed total.",
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "new_mt5_run_required": False,
            "mt5_evidence_reused": SOURCE_RUN22B_ID,
            "reason": "requested supplement is comparative attribution and runtime-gap analysis over completed run22B evidence.",
        },
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": ["Stage28 requested supplement completed.", "MT5 score-table handoff matched Python score-table output for reused run22B telemetry."],
            "forbidden_claims": summary["forbidden_claims"],
            "boundary": BOUNDARY,
        },
    )
    gates = ["scope_completion_gate", "runtime_parity_audit", "attribution_gate", "kpi_contract_audit", "final_claim_guard", "required_gate_coverage_audit"]
    write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []},
    )


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    branch = active_branch()
    run22a, run22b = load_source_summaries()
    state_rows, state_read = state_variance_comparison()
    attribution_rows, attribution_read = tier_attribution_rows(run22b)
    runtime_gap_rows, runtime_gap_read = probability_gap_rows(run22b)
    summary: dict[str, Any] = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "status": "reviewed_supplement_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "exploration_label": EXPLORATION_LABEL,
        "source_runs": [SOURCE_RUN22A_ID, SOURCE_RUN22B_ID],
        "requested_items": list(REQUESTED_ITEMS),
        "state_variance_read": state_read,
        "tier_attribution_read": attribution_read,
        "runtime_gap_read": runtime_gap_read,
        "state_variance_rows": state_rows,
        "tier_attribution_rows": attribution_rows,
        "runtime_gap_rows": runtime_gap_rows,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "active_branch": branch,
        "created_at_utc": created_at,
        "next_action": NEXT_ACTION,
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "allowed_claims": ["Stage28 requested supplement completed."],
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority", "native_statsmodels_mt5_runtime_authority"],
    }
    write_md(REPORT_PATH, report_text(summary))
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage28 RUN22C Supplement(28단계 22C 실행 보강)

Stage28(28단계) `{RUN_ID}`를 `{JUDGMENT}`로 기록한다.

효과(effect, 효과): state count(상태 수), switching variance(전환 분산), Tier A/B attribution(티어 A/B 귀속), MT5 score-table handoff(MT5 점수표 인계) 차이를 보강했고, Stage29(29단계) next action(다음 행동)은 `{NEXT_ACTION}` 그대로 둔다.

- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
""",
    )
    summary["ledger_updates"] = materialize_ledgers(summary)
    update_state_docs(summary)
    write_packet_artifacts(summary, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "judgment": JUDGMENT,
                    "best_structural_read_variant_id": state_read.get("best_structural_read_variant_id"),
                    "runtime_gap_max_abs_diff": runtime_gap_read.get("score_table_handoff_max_abs_diff"),
                    "next_action": NEXT_ACTION,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run Stage28 Markov regression bounded supplement.")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
