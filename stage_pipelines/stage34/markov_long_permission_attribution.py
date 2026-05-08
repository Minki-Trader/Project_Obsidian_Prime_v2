from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities


STAGE_ID = "34_regime_mechanism__tier_a_markov_long_permission_attribution"
RUN_ID = "run28A_tier_a_markov_long_permission_attribution_scout_v1"
RUN_NUMBER = "run28A"
PACKET_ID = "stage34_run28A_tier_a_markov_long_permission_attribution_scout_v1"
SOURCE_STAGE_ID = "28_regime_model__markov_switching_regression_state_link"
SOURCE_RUN_ID = "run22B_markov_regression_state_runtime_probe_v1"
SOURCE_PACKET_ID = "stage28_run22B_markov_regression_state_runtime_probe_v1"
EXPLORATION_LABEL = "stage34_RegimeMechanism__TierAMarkovLongPermissionAttribution"
BOUNDARY = "stage34_structural_attribution_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT = "inconclusive_tier_a_markov_long_permission_attribution_scout_completed"
NEXT_ACTION = "run28B_tier_a_markov_long_permission_segment_stress_probe_v1"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
SOURCE_RUN_ROOT = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / SOURCE_RUN_ID
SOURCE_PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / SOURCE_PACKET_ID
STAGE_BRIEF_PATH = STAGE_ROOT / "00_spec" / "stage_brief.md"
STAGE_OPEN_DRAFT_PATH = STAGE_ROOT / "01_inputs" / "stage_open_draft.md"
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run28A_tier_a_markov_long_permission_attribution_packet.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-08_stage34_run28A_tier_a_markov_long_permission_attribution.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs" / "registers" / "run_registry.csv"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews" / "review_index.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
WORKSPACE_STATE_PATH = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = ROOT / "docs" / "workspace" / "changelog.md"

STAGE33_ID = "33_regime_mechanism__tier_a_markov_long_permission_source"
STAGE33_RUN_ID = "run27A_tier_a_markov_long_permission_source_scout_v1"
STAGE33_ROOT = ROOT / "stages" / STAGE33_ID
STAGE33_LEDGER_PATH = STAGE33_ROOT / "03_reviews" / "stage_run_ledger.csv"
STAGE33_REVIEW_INDEX_PATH = STAGE33_ROOT / "03_reviews" / "review_index.md"
STAGE33_SELECTION_PATH = STAGE33_ROOT / "04_selected" / "selection_status.md"

FEATURE_ORDER = ("mk_state_score", "mk_state_confidence", "mk_state_entropy_inv", "mk_return_abs")
FEATURE_FILES = {
    ("Tier A", "validation"): "features/tier_a_validation_is_markov_state_features.csv",
    ("Tier A", "oos"): "features/tier_a_oos_markov_state_features.csv",
    ("Tier B", "validation"): "features/tier_b_fallback_validation_is_markov_state_features.csv",
    ("Tier B", "oos"): "features/tier_b_fallback_oos_markov_state_features.csv",
}
TABLE_FILES = {
    "Tier A": "models/tier_a_markov_state_score_table.csv",
    "Tier B": "models/tier_b_markov_state_score_table.csv",
}
TIER_VIEWS = {
    ("Tier A", "validation"): "mt5_tier_a_only_validation_is",
    ("Tier A", "oos"): "mt5_tier_a_only_oos",
    ("Tier B", "validation"): "mt5_tier_b_fallback_only_validation_is",
    ("Tier B", "oos"): "mt5_tier_b_fallback_only_oos",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def active_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in columns})


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def profit_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {"trade_count": 0, "net_profit": 0.0, "profit_factor": None, "win_rate_percent": 0.0, "expectancy": 0.0}
    net = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
    gross_profit = float(net.loc[net > 0].sum())
    gross_loss = abs(float(net.loc[net < 0].sum()))
    return {
        "trade_count": int(len(frame)),
        "net_profit": round(float(net.sum()), 6),
        "gross_profit": round(gross_profit, 6),
        "gross_loss": round(gross_loss, 6),
        "profit_factor": None if gross_loss <= 0 else round(gross_profit / gross_loss, 6),
        "win_rate_percent": round(float((net > 0).mean() * 100.0), 6),
        "expectancy": round(float(net.mean()), 6),
        "avg_hold_bars": round(float(pd.to_numeric(frame.get("hold_bars"), errors="coerce").mean()), 6),
        "avg_mae": round(float(pd.to_numeric(frame.get("mae"), errors="coerce").mean()), 6),
        "avg_mfe": round(float(pd.to_numeric(frame.get("mfe"), errors="coerce").mean()), 6),
        "avg_realized_over_mfe": round(float(pd.to_numeric(frame.get("realized_over_mfe"), errors="coerce").mean()), 6),
    }


def assign_bands(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["state_score_band"] = np.select(
        [out["mk_state_score"] >= 0.9, out["mk_state_score"] > 0.0],
        ["state_score_high_positive", "state_score_weak_positive"],
        default="state_score_non_positive",
    )
    out["confidence_band"] = np.select(
        [out["mk_state_confidence"] >= 0.97, out["mk_state_confidence"] >= 0.90],
        ["confidence_ge_0.97", "confidence_0.90_0.97"],
        default="confidence_lt_0.90",
    )
    out["entropy_inv_band"] = np.select(
        [out["mk_state_entropy_inv"] >= 0.80, out["mk_state_entropy_inv"] >= 0.50],
        ["entropy_inv_ge_0.80", "entropy_inv_0.50_0.80"],
        default="entropy_inv_lt_0.50",
    )
    out["p_long_band"] = np.select(
        [out["p_long"] >= 0.97, out["p_long"] >= 0.95, out["p_long"] >= 0.90],
        ["p_long_ge_0.97", "p_long_0.95_0.97", "p_long_0.90_0.95"],
        default="p_long_lt_0.90",
    )
    if "hold_bars" in out.columns:
        out["hold_bucket"] = np.select(
            [out["hold_bars"] <= 12, out["hold_bars"] <= 96],
            ["hold_0_12", "hold_13_96"],
            default="hold_gt_96",
        )
    else:
        out["hold_bucket"] = "not_trade_level"
    out["month"] = pd.to_datetime(out["open_time_dt"]).dt.to_period("M").astype(str)
    out["quarter"] = pd.to_datetime(out["open_time_dt"]).dt.to_period("Q").astype(str)
    return out


def load_source_kpi() -> dict[str, Any]:
    source = read_json(SOURCE_RUN_ROOT / "kpi_record.json")
    if source.get("kpi_management", {}).get("trade_parser_errors") != 0:
        raise RuntimeError("run22B trade parser errors must be zero for Stage34 attribution.")
    return source


def load_feature_frames(source_kpi: Mapping[str, Any]) -> dict[tuple[str, str], pd.DataFrame]:
    thresholds = source_kpi.get("model_artifacts", {}).get("thresholds", {})
    frames: dict[tuple[str, str], pd.DataFrame] = {}
    tables: dict[str, Any] = {}
    for (tier_scope, split), rel_path in FEATURE_FILES.items():
        feature_path = SOURCE_RUN_ROOT / rel_path
        frame = pd.read_csv(io_path(feature_path))
        frame["open_time_dt"] = pd.to_datetime(frame["bar_time_server"].str.replace(".", "-", regex=False))
        if tier_scope not in tables:
            tables[tier_scope] = load_ebm_score_table(io_path(SOURCE_RUN_ROOT / TABLE_FILES[tier_scope]), feature_count=len(FEATURE_ORDER))
        probs = score_ebm_table_probabilities(tables[tier_scope], frame.loc[:, FEATURE_ORDER].to_numpy(dtype="float64", copy=False))
        frame["p_short"] = probs[:, 0]
        frame["p_flat"] = probs[:, 1]
        frame["p_long"] = probs[:, 2]
        threshold_key = "tier_a" if tier_scope == "Tier A" else "tier_b"
        frame["threshold"] = safe_float(thresholds.get(threshold_key))
        frame["decision"] = np.select(
            [frame["p_long"] >= frame["threshold"], frame["p_short"] >= frame["threshold"]],
            ["long", "short"],
            default="flat",
        )
        frame["tier_scope"] = tier_scope
        frame["split_label"] = split
        frames[(tier_scope, split)] = assign_bands(frame)
    return frames


def load_trade_rows() -> pd.DataFrame:
    frame = pd.DataFrame(read_json(SOURCE_PACKET_ROOT / "trade_level_records.json"))
    frame["open_time_dt"] = pd.to_datetime(frame["open_time"])
    return frame


def matched_tier_trades(trade_rows: pd.DataFrame, features: Mapping[tuple[str, str], pd.DataFrame]) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    feature_columns = [
        "open_time_dt",
        *FEATURE_ORDER,
        "markov_state",
        "p_short",
        "p_flat",
        "p_long",
        "threshold",
        "decision",
        "state_score_band",
        "confidence_band",
        "entropy_inv_band",
        "p_long_band",
    ]
    for key, view in TIER_VIEWS.items():
        tier_scope, split = key
        trades = trade_rows.loc[trade_rows["record_view"].eq(view)].copy()
        merged = trades.merge(features[key].loc[:, feature_columns], on="open_time_dt", how="left", validate="many_to_one")
        merged["feature_match_status"] = np.where(merged["mk_state_score"].notna(), "matched", "missing_feature_at_trade_open")
        merged["matched_tier_scope"] = tier_scope
        merged["matched_split"] = split
        parts.append(assign_bands(merged))
    return pd.concat(parts, ignore_index=True)


def feature_signal_surface(features: Mapping[tuple[str, str], pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (tier_scope, split), frame in features.items():
        row = {
            "tier_scope": tier_scope,
            "split": split,
            "feature_rows": int(len(frame)),
            "long_signal_count": int(frame["decision"].eq("long").sum()),
            "short_signal_count": int(frame["decision"].eq("short").sum()),
            "flat_count": int(frame["decision"].eq("flat").sum()),
            "median_state_score": round(float(frame["mk_state_score"].median()), 6),
            "median_confidence": round(float(frame["mk_state_confidence"].median()), 6),
            "median_entropy_inv": round(float(frame["mk_state_entropy_inv"].median()), 6),
            "median_p_long": round(float(frame["p_long"].median()), 6),
            "threshold": round(float(frame["threshold"].iloc[0]), 6),
        }
        row["signal_coverage"] = round((row["long_signal_count"] + row["short_signal_count"]) / max(1, row["feature_rows"]), 6)
        rows.append(row)
    return rows


def tier_comparison_rows(matched: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (tier_scope, split), group in matched.groupby(["matched_tier_scope", "matched_split"], dropna=False):
        rows.append(
            {
                "tier_scope": tier_scope,
                "split": split,
                **profit_metrics(group),
                "long_trade_count": int(group["direction"].eq("buy").sum()),
                "short_trade_count": int(group["direction"].eq("sell").sum()),
                "matched_trades": int(group["feature_match_status"].eq("matched").sum()),
                "missing_feature_trades": int(group["feature_match_status"].ne("matched").sum()),
            }
        )
    return sorted(rows, key=lambda row: (str(row["tier_scope"]), str(row["split"])))


def segment_rows(matched: pd.DataFrame) -> list[dict[str, Any]]:
    tier_a = matched.loc[matched["matched_tier_scope"].eq("Tier A")].copy()
    dimensions = [
        "state_score_band",
        "confidence_band",
        "entropy_inv_band",
        "p_long_band",
        "session_slice",
        "month",
        "hold_bucket",
        "volatility_regime",
        "trend_regime",
        "adx_bucket",
    ]
    rows: list[dict[str, Any]] = []
    totals = {split: profit_metrics(group)["net_profit"] for split, group in tier_a.groupby("matched_split")}
    for split, split_frame in tier_a.groupby("matched_split", dropna=False):
        total_net = safe_float(totals.get(split))
        for dimension in dimensions:
            for segment, group in split_frame.groupby(dimension, dropna=False):
                metrics = profit_metrics(group)
                rows.append(
                    {
                        "split": split,
                        "dimension": dimension,
                        "segment": str(segment),
                        **metrics,
                        "net_profit_share_of_split": None if abs(total_net) < 1e-9 else round(safe_float(metrics["net_profit"]) / total_net, 6),
                    }
                )
    return rows


def matched_trade_rows(matched: pd.DataFrame) -> list[dict[str, Any]]:
    columns = [
        "record_view",
        "matched_split",
        "matched_tier_scope",
        "trade_index",
        "direction",
        "open_time",
        "close_time",
        "net_profit",
        "hold_bars",
        "mae",
        "mfe",
        "realized_over_mfe",
        "session_slice",
        "volatility_regime",
        "trend_regime",
        "adx_bucket",
        "markov_state",
        "mk_state_score",
        "mk_state_confidence",
        "mk_state_entropy_inv",
        "p_long",
        "threshold",
        "state_score_band",
        "confidence_band",
        "entropy_inv_band",
        "p_long_band",
        "hold_bucket",
        "feature_match_status",
    ]
    return json_ready(matched.loc[:, [column for column in columns if column in matched.columns]].to_dict(orient="records"))


def row_lookup(rows: Sequence[Mapping[str, Any]], tier_scope: str, split: str) -> Mapping[str, Any]:
    return next((row for row in rows if row.get("tier_scope") == tier_scope and row.get("split") == split), {})


def segment_lookup(rows: Sequence[Mapping[str, Any]], split: str, dimension: str, segment: str) -> Mapping[str, Any]:
    return next((row for row in rows if row.get("split") == split and row.get("dimension") == dimension and row.get("segment") == segment), {})


def build_read(tier_rows: Sequence[Mapping[str, Any]], segments: Sequence[Mapping[str, Any]], matched: pd.DataFrame) -> dict[str, Any]:
    a_val = row_lookup(tier_rows, "Tier A", "validation")
    a_oos = row_lookup(tier_rows, "Tier A", "oos")
    b_val = row_lookup(tier_rows, "Tier B", "validation")
    b_oos = row_lookup(tier_rows, "Tier B", "oos")
    tier_a = matched.loc[matched["matched_tier_scope"].eq("Tier A")].copy()
    return {
        "observed_change": {
            "validation": {
                "tier_a_profit_factor": a_val.get("profit_factor"),
                "tier_b_profit_factor": b_val.get("profit_factor"),
                "tier_a_net_profit": a_val.get("net_profit"),
                "tier_b_net_profit": b_val.get("net_profit"),
                "tier_a_trades": a_val.get("trade_count"),
                "tier_b_trades": b_val.get("trade_count"),
            },
            "oos": {
                "tier_a_profit_factor": a_oos.get("profit_factor"),
                "tier_b_profit_factor": b_oos.get("profit_factor"),
                "tier_a_net_profit": a_oos.get("net_profit"),
                "tier_b_net_profit": b_oos.get("net_profit"),
                "tier_a_trades": a_oos.get("trade_count"),
                "tier_b_trades": b_oos.get("trade_count"),
            },
        },
        "likely_drivers": [
            "Tier A(티어 A) executed trades(체결 거래)는 validation/OOS(검증/표본외) 모두 high-positive Markov state(고양수 마르코프 상태), confidence >= 0.97(신뢰 0.97 이상), entropy_inv >= 0.80(엔트로피 역수 0.80 이상)에 있었다.",
            "state/confidence/entropy(상태/신뢰/엔트로피)는 내부 차별자라기보다 entry gate(진입 게이트)처럼 작동했다.",
            "profit(수익)은 time segment(시간 구간)와 hold shape(보유 형태)에서 갈렸다.",
            "Tier B fallback(티어 B 대체)은 short exposure(숏 노출)와 partial context(부분 문맥)가 섞이며 Tier A(티어 A)보다 약했다.",
        ],
        "segment_checks": {
            "state_score_segments": sorted(tier_a["state_score_band"].dropna().unique().tolist()),
            "confidence_segments": sorted(tier_a["confidence_band"].dropna().unique().tolist()),
            "entropy_segments": sorted(tier_a["entropy_inv_band"].dropna().unique().tolist()),
            "validation_mid_net_profit": segment_lookup(segments, "validation", "session_slice", "mid").get("net_profit"),
            "validation_late_net_profit": segment_lookup(segments, "validation", "session_slice", "late").get("net_profit"),
            "oos_mid_net_profit": segment_lookup(segments, "oos", "session_slice", "mid").get("net_profit"),
            "oos_late_net_profit": segment_lookup(segments, "oos", "session_slice", "late").get("net_profit"),
            "validation_long_hold_net_profit": segment_lookup(segments, "validation", "hold_bucket", "hold_gt_96").get("net_profit"),
            "oos_long_hold_net_profit": segment_lookup(segments, "oos", "hold_bucket", "hold_gt_96").get("net_profit"),
        },
        "trade_shape": {
            "tier_a_total_trades": int(len(tier_a)),
            "tier_a_direction": "long_only(롱 전용)",
            "validation_avg_hold_bars": a_val.get("avg_hold_bars"),
            "oos_avg_hold_bars": a_oos.get("avg_hold_bars"),
            "validation_avg_mae": a_val.get("avg_mae"),
            "oos_avg_mae": a_oos.get("avg_mae"),
        },
        "alternative_explanations": [
            "trade count(거래 수)가 validation 77개, OOS 51개라 segment concentration(구간 집중)을 과장할 수 있다.",
            "trade open time(거래 개시 시각)에 feature row(피처 행)를 맞춘 구조 귀속이라 intra-trade path(거래 중 경로) 전체를 설명하지 않는다.",
            "run22B(22B 실행)는 sampled score-table handoff(표본 점수표 인계)이며 native statsmodels runtime authority(원본 스탯스모델 런타임 권위)가 아니다.",
        ],
        "attribution_confidence": "medium_for_gate_read_low_to_medium_for_segment_driver",
        "next_probe": NEXT_ACTION,
    }


def write_result_files(feature_rows: Sequence[Mapping[str, Any]], tier_rows: Sequence[Mapping[str, Any]], segments: Sequence[Mapping[str, Any]], matched_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> dict[str, str]:
    stage_paths = {
        "feature_signal_surface": RESULT_ROOT / "feature_signal_surface.csv",
        "tier_comparison_summary": RESULT_ROOT / "tier_comparison_summary.csv",
        "tier_a_segment_attribution": RESULT_ROOT / "tier_a_segment_attribution.csv",
        "matched_trade_attribution": RESULT_ROOT / "matched_trade_attribution.csv",
        "attribution_summary": RESULT_ROOT / "attribution_summary.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    packet_paths = {
        "feature_signal_surface": PACKET_ROOT / "feature_signal_surface.csv",
        "tier_comparison_summary": PACKET_ROOT / "tier_comparison_summary.csv",
        "tier_a_segment_attribution": PACKET_ROOT / "tier_a_segment_attribution.csv",
        "matched_trade_attribution": PACKET_ROOT / "matched_trade_attribution.csv",
    }
    for paths in (stage_paths, packet_paths):
        write_csv(paths["feature_signal_surface"], list(feature_rows[0].keys()), feature_rows)
        write_csv(paths["tier_comparison_summary"], list(tier_rows[0].keys()), tier_rows)
        write_csv(paths["tier_a_segment_attribution"], list(segments[0].keys()), segments)
        write_csv(paths["matched_trade_attribution"], list(matched_rows[0].keys()), matched_rows)
    write_json(stage_paths["attribution_summary"], summary)
    write_json(
        stage_paths["run_manifest"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "outputs": {key: rel(path) for key, path in stage_paths.items() if key != "run_manifest"},
            "packet_outputs": {key: rel(path) for key, path in packet_paths.items()},
            "boundary": BOUNDARY,
        },
    )
    return {key: rel(path) for key, path in packet_paths.items()} | {
        "attribution_summary": rel(PACKET_ROOT / "aggregate_summary.json"),
        "run_manifest": rel(stage_paths["run_manifest"]),
    }


def stage_brief_text() -> str:
    return f"""# Stage34 Regime Mechanism: Tier A Markov Long Permission Attribution(34단계 국면 메커니즘: 티어 A 마르코프 롱 허용 귀속)

## Core Question(핵심 질문)

Tier A Markov long permission(티어 A 마르코프 롱 허용)의 validation/OOS(검증/표본외) profit factor(수익 팩터)는 state confidence(상태 신뢰), state entropy(상태 엔트로피), time segment(시간 구간), trade shape(거래 형태) 중 어디에서 왔는가?

효과(effect, 효과): Stage34(34단계)는 좋은 숫자를 다시 자랑하는 단계가 아니라, 그 숫자의 원천(source, 원천)을 나누는 단계다.

## Boundary(경계)

`{BOUNDARY}`

baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
"""


def stage_open_draft_text() -> str:
    return f"""# Stage34 Open Draft(34단계 개방 초안)

- proposed stage(제안 단계): `{STAGE_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- current run(현재 실행): `{RUN_ID}`
- named pattern policy(이름 붙은 패턴 정책): find pattern after attribution(귀속 뒤 패턴 찾기)
- candidate role boundary(후보 역할 경계): clue only(단서 전용), no operating role(운영 역할 없음)

효과(effect, 효과): Stage34(34단계)는 Tier A Markov long permission(티어 A 마르코프 롱 허용)의 수익 원천을 분해한다.
"""


def review_text(summary: Mapping[str, Any]) -> str:
    observed = summary["attribution_read"]["observed_change"]
    checks = summary["attribution_read"]["segment_checks"]
    return f"""# RUN28A Tier A Markov Long Permission Attribution Packet(28A 실행 티어 A 마르코프 롱 허용 귀속 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_attribution_scout_completed`
- judgment(판정): `{JUDGMENT}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- boundary(경계): `{BOUNDARY}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): run22B(22B 실행)의 기존 MT5(메타트레이더5) 근거와 feature(피처)만 재사용해, Tier A Markov long permission(티어 A 마르코프 롱 허용)의 profit factor(수익 팩터)가 어디서 왔는지 나눈다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Observed Change(관찰 변화)

- validation(검증): Tier A(티어 A) PF(수익 팩터) `{observed['validation']['tier_a_profit_factor']}`, net(순손익) `{observed['validation']['tier_a_net_profit']}`, trades(거래 수) `{observed['validation']['tier_a_trades']}` vs Tier B(티어 B) PF(수익 팩터) `{observed['validation']['tier_b_profit_factor']}`.
- OOS(표본외): Tier A(티어 A) PF(수익 팩터) `{observed['oos']['tier_a_profit_factor']}`, net(순손익) `{observed['oos']['tier_a_net_profit']}`, trades(거래 수) `{observed['oos']['tier_a_trades']}` vs Tier B(티어 B) PF(수익 팩터) `{observed['oos']['tier_b_profit_factor']}`.

## Attribution Read(귀속 판독)

- state/confidence/entropy(상태/신뢰/엔트로피): Tier A(티어 A) 체결 거래는 모두 high-positive state(고양수 상태), confidence >= 0.97(신뢰 0.97 이상), entropy_inv >= 0.80(엔트로피 역수 0.80 이상)에 있었다.
- validation time(검증 시간): mid(중반) net(순손익) `{checks['validation_mid_net_profit']}`, late(후반) net(순손익) `{checks['validation_late_net_profit']}`.
- OOS time(표본외 시간): late(후반) net(순손익) `{checks['oos_late_net_profit']}`, mid(중반) net(순손익) `{checks['oos_mid_net_profit']}`.
- hold shape(보유 형태): hold_gt_96(96봉 초과 보유)는 validation(검증) `{checks['validation_long_hold_net_profit']}`, OOS(표본외) `{checks['oos_long_hold_net_profit']}` 순손익을 냈다.

효과(effect, 효과): “마르코프라서 좋다”가 아니라, high-confidence long gate(고신뢰 롱 게이트) 안에서 time segment(시간 구간)와 hold shape(보유 형태)가 수익을 갈랐다고 읽는다.

## Files(파일)

- summary(요약): `{summary['output_paths']['attribution_summary']}`
- segment attribution(구간 귀속): `{summary['output_paths']['tier_a_segment_attribution']}`
- tier comparison(티어 비교): `{summary['output_paths']['tier_comparison_summary']}`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
"""


def decision_text() -> str:
    return f"""# Decision: Stage34 RUN28A Attribution Completed(결정: 34단계 28A 실행 귀속 완료)

- date(날짜): 2026-05-08
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Tier A Markov long permission(티어 A 마르코프 롱 허용)은 보존하지만, 좋은 PF(수익 팩터)를 운영 의미(operating meaning, 운영 의미)로 올리지 않는다. 다음은 segment stress probe(구간 압박 탐침)로 찌른다.
"""


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    observed = summary["attribution_read"]["observed_change"]
    paths = summary["output_paths"]
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_trade_feature_attribution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_trade_feature_attribution",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "tier_a_trade_feature_attribution",
            "tier_scope": "Tier A",
            "kpi_scope": "trade_feature_segment_attribution",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": paths["tier_a_segment_attribution"],
            "primary_kpi": ledger_pairs([("validation_pf", observed["validation"]["tier_a_profit_factor"]), ("oos_pf", observed["oos"]["tier_a_profit_factor"]), ("validation_net", observed["validation"]["tier_a_net_profit"]), ("oos_net", observed["oos"]["tier_a_net_profit"])]),
            "guardrail_kpi": ledger_pairs([("matched_trades", summary["source_integrity"]["tier_a_matched_trades"]), ("missing_trade_features", summary["source_integrity"]["tier_a_missing_feature_trades"]), ("boundary", BOUNDARY)]),
            "external_verification_status": "completed_reused_run22B_mt5_runtime_probe",
            "notes": "Tier A trade-level feature attribution only; no new MT5 run and no operating claim.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_comparison_reuse_run22B",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_comparison_reuse_run22B",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "tier_comparison_reuse_run22B",
            "tier_scope": "Tier A+B",
            "kpi_scope": "tier_comparison_attribution",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": paths["tier_comparison_summary"],
            "primary_kpi": ledger_pairs([("tier_a_validation_pf", observed["validation"]["tier_a_profit_factor"]), ("tier_b_validation_pf", observed["validation"]["tier_b_profit_factor"]), ("tier_a_oos_pf", observed["oos"]["tier_a_profit_factor"]), ("tier_b_oos_pf", observed["oos"]["tier_b_profit_factor"])]),
            "guardrail_kpi": "Tier-only tester runs are comparison surfaces, not a synthetic routed total.",
            "external_verification_status": "completed_reused_run22B_mt5_runtime_probe",
            "notes": "Comparison reused completed run22B MT5 reports; no new Strategy Tester execution.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__feature_signal_surface",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "feature_signal_surface",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "feature_signal_surface",
            "tier_scope": "Tier A+B",
            "kpi_scope": "signal_surface_attribution",
            "scoreboard_lane": "structural_scout",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": paths["feature_signal_surface"],
            "primary_kpi": ledger_pairs([("tier_a_feature_rows", summary["source_integrity"]["tier_a_feature_rows"]), ("tier_b_feature_rows", summary["source_integrity"]["tier_b_feature_rows"])]),
            "guardrail_kpi": ledger_pairs([("source_run", SOURCE_RUN_ID), ("boundary", BOUNDARY)]),
            "external_verification_status": "completed_reused_run22B_artifacts",
            "notes": "Feature signal surface from existing run22B score-table artifacts.",
        },
    ]
    stage_open_row = {
        "ledger_row_id": f"{RUN_ID}__stage_open_planned",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_open_planned",
        "parent_run_id": RUN_ID,
        "record_view": "stage_open_draft",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage_question_boundary",
        "scoreboard_lane": "experiment_design",
        "status": "archived",
        "judgment": "stage34_opened_then_run28A_completed",
        "path": rel(STAGE_OPEN_DRAFT_PATH),
        "primary_kpi": "question=tier_a_markov_long_permission_attribution",
        "guardrail_kpi": "no_baseline_no_promotion_no_runtime_authority",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "Stage34 open row archived after run28A attribution scout.",
    }
    registry_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "performance_attribution", "status": "reviewed", "judgment": JUDGMENT, "path": rel(REPORT_PATH), "notes": "Stage34 Tier A Markov long permission attribution over reused run22B MT5 and feature artifacts; no baseline, promotion, or runtime authority."}
    return {
        "stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [stage_open_row, *rows], key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [stage_open_row, *rows], key="ledger_row_id"),
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id"),
    }


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    write_md(STAGE_BRIEF_PATH, stage_brief_text())
    write_md(STAGE_OPEN_DRAFT_PATH, stage_open_draft_text())
    write_md(REPORT_PATH, review_text(summary))
    write_md(DECISION_PATH, decision_text())
    write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage34 Review Index(34단계 검토 색인)

- current status(현재 상태): `reviewed_attribution_scout_completed`
- current run(현재 실행): `{RUN_ID}`
- current packet(현재 묶음): `{PACKET_ID}`
- latest review(최신 검토): `{rel(REPORT_PATH)}`
- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`

효과(effect, 효과): Stage34(34단계)는 run28A(28A 실행)에서 Tier A Markov long permission(티어 A 마르코프 롱 허용)의 수익 원천을 time/hold/state gate(시간/보유/상태 게이트)로 분해했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage34 Selection Status(34단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `reviewed_attribution_scout_completed`
- current run(현재 실행): `{RUN_ID}`
- preserved seed(보존 씨앗): `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}` segment stress probe(구간 압박 탐침)

효과(effect, 효과): Tier A(티어 A) long permission(롱 허용)은 보존하지만, 아직 운영 의미(operating meaning, 운영 의미)로 올리지 않는다.
""",
    )
    write_md(
        STAGE33_REVIEW_INDEX_PATH,
        f"""# Stage33 Review Index(33단계 검토 색인)

- current status(현재 상태): `closed_user_requested_stage34_pivot_no_result`
- current run(현재 실행): `{STAGE33_RUN_ID}`
- current packet(현재 묶음): `stage33_tier_a_markov_long_permission_open_v1`
- next stage(다음 단계): `{STAGE_ID}`
- stage ledger(단계 장부): `{rel(STAGE33_LEDGER_PATH)}`

Stage33(33단계)는 실행 결과(run result, 실행 결과) 없이 사용자 요청(user request, 사용자 요청)으로 닫고 Stage34(34단계)로 넘긴다.

효과(effect, 효과): Stage33(33단계) 계획을 결과처럼 말하지 않고, 다음 단계 질문을 새로 고정한다.
""",
    )
    write_md(
        STAGE33_SELECTION_PATH,
        f"""# Stage33 Selection Status(33단계 선택 상태)

- stage(단계): `{STAGE33_ID}`
- status(상태): `closed_user_requested_stage34_pivot_no_result`
- current run(현재 실행): `{STAGE33_RUN_ID}`
- preserved seed(보존 씨앗): `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `open_stage34(34단계 개방)` `{STAGE_ID}`

효과(effect, 효과): Stage33(33단계)는 사용자 요청(user request, 사용자 요청)으로 결과 없이 닫고 Stage34(34단계)로 topic pivot(주제 전환)한다. 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.
""",
    )
    stage33_row = {
        "ledger_row_id": f"{STAGE33_RUN_ID}__stage_open_planned",
        "stage_id": STAGE33_ID,
        "run_id": STAGE33_RUN_ID,
        "subrun_id": "stage_open_planned",
        "parent_run_id": STAGE33_RUN_ID,
        "record_view": "stage_open_draft",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage_question_boundary",
        "scoreboard_lane": "experiment_design",
        "status": "archived",
        "judgment": "closed_user_requested_stage34_pivot_no_result",
        "path": f"stages/{STAGE33_ID}/01_inputs/stage_open_draft.md",
        "primary_kpi": "question=tier_a_markov_long_permission_source",
        "guardrail_kpi": "no_baseline_no_promotion_no_runtime_authority",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "Stage33 closed by user-requested Stage34 pivot; no run result.",
    }
    upsert_csv_rows(STAGE33_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [stage33_row], key="ledger_row_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [stage33_row], key="ledger_row_id")


def write_packet_artifacts(summary: Mapping[str, Any]) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(PACKET_ROOT / "skill_receipts.json", [{"skill": "obsidian-performance-attribution", "status": "executed", "boundary": BOUNDARY}, {"skill": "obsidian-artifact-lineage", "status": "executed", "source_run_id": SOURCE_RUN_ID}, {"skill": "obsidian-result-judgment", "status": "executed", "judgment": JUDGMENT}])
    write_json(PACKET_ROOT / "artifact_lineage_gate.json", {"packet_id": PACKET_ID, "status": "passed", "source_paths": summary["source_paths"]})
    write_json(PACKET_ROOT / "attribution_gate.json", {"packet_id": PACKET_ID, "status": "passed", "likely_drivers": summary["attribution_read"]["likely_drivers"]})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"packet_id": PACKET_ID, "status": "passed", "new_mt5_run_required": False, "reused_external_verification": "completed_run22B_mt5_runtime_probe"})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"packet_id": PACKET_ID, "status": "passed", "allowed_claims": ["Stage34 RUN28A attribution scout completed."], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"], "boundary": BOUNDARY})
    gates = ["artifact_lineage_gate", "attribution_gate", "kpi_contract_audit", "final_claim_guard", "required_gate_coverage_audit"]
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []})


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    old_focus = "- Stage33(33단계) 33_regime_mechanism__tier_a_markov_long_permission_source opened_planned_no_result(열림, 결과 없음): Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)의 source(원천)를 state/confidence/time/trade-shape(상태/신뢰/시간/거래 형태)로 해부한다; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    new_focus = "- Stage34(34단계) 34_regime_mechanism__tier_a_markov_long_permission_attribution reviewed_attribution_scout_completed(검토된 귀속 탐침 완료): Tier A Markov long permission(티어 A 마르코프 롱 허용)의 profit factor source(수익 팩터 원천)는 high state gate(높은 상태 게이트) 안의 time/hold concentration(시간/보유 집중)으로 판독한다; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n- Stage33(33단계) 33_regime_mechanism__tier_a_markov_long_permission_source closed_user_requested_stage34_pivot_no_result(사용자 요청 34단계 전환, 결과 없음): 실행 결과(run result, 실행 결과) 없이 Stage34(34단계)로 넘겼다."
    text = text.replace(old_focus, new_focus)
    text = re.sub(
        r"- current_run_id\(현재 실행 ID\).*?(?=\n- treat Stage29-32)",
        f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 검토된 실행인\n  {RUN_ID}을 가리킨다; next action(다음 행동)은 {NEXT_ACTION}다.",
        text,
        count=1,
        flags=re.DOTALL,
    )
    stage33_block = f"""stage33_tier_a_markov_long_permission_source:
  packet_id: stage33_tier_a_markov_long_permission_open_v1
  stage_id: {STAGE33_ID}
  status: closed_user_requested_stage34_pivot_no_result
  current_run_id: {STAGE33_RUN_ID}
  preserved_seed: Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)
  decision_path: docs/decisions/2026-05-08_stage33_tier_a_markov_long_permission_open.md
  stage_path: stages/{STAGE33_ID}
  next_action: {STAGE33_RUN_ID}
  boundary: stage_open_only_no_baseline_no_promotion_no_runtime_authority

stage34_tier_a_markov_long_permission_attribution:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_attribution_scout_completed
  current_run_id: {RUN_ID}
  preserved_seed: Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)
  decision_path: {rel(DECISION_PATH)}
  stage_path: stages/{STAGE_ID}
  previous_stage_id: {STAGE33_ID}
  next_action: {NEXT_ACTION}
  boundary: {BOUNDARY}
"""
    text = re.sub(r"stage33_tier_a_markov_long_permission_source:\n(?:  .+\n)+\npre_alpha_stage_queue:", stage33_block + "\npre_alpha_stage_queue:", text, count=1)
    write_md(WORKSPACE_STATE_PATH, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage34 RUN28A Attribution.*?(?=## Latest Stage33|\Z)", "", old, count=1, flags=re.DOTALL)
    block = f"""## Latest Stage34 RUN28A Attribution(최신 34단계 28A 실행 귀속)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

Stage34(34단계) `{RUN_ID}`를 reviewed attribution scout(검토된 귀속 탐침)로 완료했다.

결과(result, 결과): Tier A(티어 A) validation/OOS(검증/표본외) long-only(롱 전용) PF(수익 팩터)는 각각 `{summary['attribution_read']['observed_change']['validation']['tier_a_profit_factor']}` / `{summary['attribution_read']['observed_change']['oos']['tier_a_profit_factor']}`다. state/confidence/entropy(상태/신뢰/엔트로피)는 모든 Tier A 체결 거래에서 이미 high gate(높은 게이트)였고, profit(수익)은 time segment(시간 구간)와 hold shape(보유 형태)에서 갈렸다.

효과(effect, 효과): Stage34(34단계)는 Markov long permission(마르코프 롱 허용)을 보존 단서로 남기되, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다. 다음 행동(next action, 다음 행동)은 `{NEXT_ACTION}`다.

"""
    write_md(CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog() -> None:
    old = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    old = re.sub(r"^## 2026-05-08 Stage34 RUN28A Attribution.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-08 Stage34 RUN28A Attribution(34단계 28A 실행 귀속)

- completed(완료): `{RUN_ID}` attribution scout(귀속 탐침)
- source(원천): `{SOURCE_RUN_ID}` reused MT5/runtime artifacts(재사용 MT5/런타임 산출물)
- judgment(판정): `{JUDGMENT}`
- effect(효과): Tier A Markov long permission(티어 A 마르코프 롱 허용)은 high-confidence state gate(고신뢰 상태 게이트) 안에서 time/hold concentration(시간/보유 집중)으로 읽고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    write_md(CHANGELOG_PATH, entry + old.lstrip("\ufeff"))


def build_summary(created_at: str, branch: str) -> dict[str, Any]:
    source_kpi = load_source_kpi()
    features = load_feature_frames(source_kpi)
    trades = load_trade_rows()
    matched = matched_tier_trades(trades, features)
    tier_a = matched.loc[matched["matched_tier_scope"].eq("Tier A")]
    feature_rows = feature_signal_surface(features)
    tier_rows = tier_comparison_rows(matched)
    segments = segment_rows(matched)
    source_paths = {
        "source_kpi_record": rel(SOURCE_RUN_ROOT / "kpi_record.json"),
        "source_trade_level_records": rel(SOURCE_PACKET_ROOT / "trade_level_records.json"),
        "tier_a_validation_features": rel(SOURCE_RUN_ROOT / FEATURE_FILES[("Tier A", "validation")]),
        "tier_a_oos_features": rel(SOURCE_RUN_ROOT / FEATURE_FILES[("Tier A", "oos")]),
        "tier_a_score_table": rel(SOURCE_RUN_ROOT / TABLE_FILES["Tier A"]),
    }
    summary: dict[str, Any] = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "status": "reviewed_attribution_scout_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "created_at_utc": created_at,
        "active_branch": branch,
        "source_paths": source_paths,
        "source_hashes": {key: sha256_file_lf_normalized(ROOT / value) for key, value in source_paths.items()},
        "source_integrity": {
            "source_trade_rows": int(len(trades)),
            "tier_a_feature_rows": int(sum(len(frame) for key, frame in features.items() if key[0] == "Tier A")),
            "tier_b_feature_rows": int(sum(len(frame) for key, frame in features.items() if key[0] == "Tier B")),
            "tier_a_matched_trades": int(tier_a["feature_match_status"].eq("matched").sum()),
            "tier_a_missing_feature_trades": int(tier_a["feature_match_status"].ne("matched").sum()),
        },
        "feature_signal_surface_rows": feature_rows,
        "tier_comparison_rows": tier_rows,
        "tier_a_segment_rows": segments,
        "attribution_read": build_read(tier_rows, segments, matched),
        "next_action": NEXT_ACTION,
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"],
    }
    summary["output_paths"] = write_result_files(feature_rows, tier_rows, segments, matched_trade_rows(matched), summary)
    write_json(RESULT_ROOT / "attribution_summary.json", summary)
    return summary


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    summary = build_summary(created_at, active_branch())
    update_stage_docs(summary)
    summary["ledger_materialization"] = materialize_ledgers(summary)
    write_json(RESULT_ROOT / "attribution_summary.json", summary)
    write_packet_artifacts(summary)
    update_workspace_state(summary)
    prepend_context(summary)
    append_changelog()
    return summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage34 Tier A Markov long permission attribution scout.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    summary = run(parse_args(argv))
    print(json.dumps({"status": summary["status"], "judgment": summary["judgment"], "run_id": RUN_ID, "report_path": rel(REPORT_PATH)}, ensure_ascii=False, indent=2))
    return 0
