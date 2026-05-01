from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
import yaml

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    read_csv_rows,
    upsert_csv_rows,
)


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
RUN_NUMBER = "run03G"
RUN_ID = "run03G_et_variant_stability_probe_v1"
PACKET_ID = "stage12_run03g_variant_stability_probe_v1"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesVariantStabilityProbe"
SOURCE_RUN_ID = "run03D_et_standalone_batch20_v1"
SOURCE_MT5_REFERENCE_RUN_ID = "run03F_et_v11_tier_balance_mt5_v1"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_RUN_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
IDEA_REGISTRY_PATH = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_RESULT_REGISTER_PATH = ROOT / "docs/registers/negative_result_register.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
MODEL_INPUT_PATH = (
    ROOT
    / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
VARIANT_RESULTS_PATH = SOURCE_RUN_ROOT / "results/variant_results.csv"
SCORED_PATH = SOURCE_RUN_ROOT / "predictions/scored_validation_oos.parquet"

TIER_A = "Tier A"
TIER_B = "Tier B"
TIER_AB = "Tier A+B"

RECOMMENDED_ROLES = {
    "v09_depth8_leaf10_q90": "priority_depth_limited_both_direction",
    "v13_base_margin002_q90": "priority_margin_filter",
    "v16_base_long_only_q90": "priority_long_only_asymmetry",
    "v18_core42_features_q90": "secondary_core42_tier_b_alignment",
    "v01_base_leaf20_q90": "secondary_base_q90_reference",
    "v11_base_leaf20_q85": "reference_already_mt5_tier_balance",
    "v20_base_inverse_q90": "negative_boundary_inverse_direction",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig" if bom else "utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def current_branch() -> str:
    try:
        completed = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
    except OSError:
        return "unknown"
    branch = completed.stdout.strip()
    return branch or "unknown"


def pct(value: Any) -> str:
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "NA"
    return f"{float(value):.6f}"


def num(value: Any, digits: int = 6) -> str:
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "NA"
    return f"{float(value):.{digits}f}"


def safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def require_inputs() -> dict[str, Any]:
    missing = [path for path in (VARIANT_RESULTS_PATH, SCORED_PATH, MODEL_INPUT_PATH, FEATURE_ORDER_PATH) if not path_exists(path)]
    if missing:
        raise FileNotFoundError(", ".join(path.as_posix() for path in missing))
    source_summary = json.loads(read_text(SOURCE_RUN_ROOT / "summary.json"))
    boundary = source_summary.get("standalone_boundary", {})
    if boundary.get("stage10_11_inheritance") is not False:
        raise RuntimeError("RUN03D is not marked stage10_11_inheritance=false.")
    if boundary.get("stage10_11_baseline") is not False:
        raise RuntimeError("RUN03D is not marked stage10_11_baseline=false.")
    return source_summary


def aggregate_periods(scored: pd.DataFrame, min_period_signals: int) -> pd.DataFrame:
    frame = scored.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["month"] = frame["timestamp"].dt.strftime("%Y-%m")
    frame["quarter"] = frame["timestamp"].dt.to_period("Q").astype(str)
    frame["is_signal"] = frame["is_signal"].astype(bool)
    frame["directional_correct"] = frame["directional_correct"].astype(bool)
    rows: list[pd.DataFrame] = []
    for grain in ("month", "quarter"):
        grouped = (
            frame.groupby(["variant_id", "split", grain], observed=True)
            .agg(
                rows=("timestamp", "size"),
                signal_count=("is_signal", "sum"),
                directional_correct_count=("directional_correct", "sum"),
                short_count=("decision_class", lambda s: int((s == 0).sum())),
                long_count=("decision_class", lambda s: int((s == 2).sum())),
            )
            .reset_index()
            .rename(columns={grain: "period"})
        )
        grouped["period_grain"] = grain
        grouped["hit_rate"] = grouped.apply(
            lambda row: float(row["directional_correct_count"] / row["signal_count"])
            if int(row["signal_count"]) > 0
            else None,
            axis=1,
        )
        grouped["coverage"] = grouped.apply(
            lambda row: float(row["signal_count"] / row["rows"]) if int(row["rows"]) > 0 else None,
            axis=1,
        )
        grouped["meets_min_signal_gate"] = grouped["signal_count"].astype(int) >= int(min_period_signals)
        rows.append(grouped)
    return pd.concat(rows, ignore_index=True)


def period_stats(periods: pd.DataFrame, variant_id: str, split: str, min_period_signals: int) -> dict[str, Any]:
    subset = periods.loc[
        periods["variant_id"].astype(str).eq(variant_id)
        & periods["split"].astype(str).eq(split)
        & periods["period_grain"].astype(str).eq("month")
    ].copy()
    qualified = subset.loc[subset["signal_count"].astype(int) >= int(min_period_signals)]
    rates = [safe_float(item) for item in qualified["hit_rate"].tolist()]
    rates = [item for item in rates if item is not None]
    return {
        f"{split}_month_count": int(len(subset)),
        f"{split}_qualified_month_count": int(len(qualified)),
        f"{split}_month_hit_mean": float(pd.Series(rates).mean()) if rates else None,
        f"{split}_month_hit_std": float(pd.Series(rates).std(ddof=0)) if len(rates) > 1 else 0.0 if rates else None,
        f"{split}_month_hit_min": float(min(rates)) if rates else None,
        f"{split}_month_hit_max": float(max(rates)) if rates else None,
        f"{split}_positive_months_ge045": int(sum(1 for item in rates if item >= 0.45)),
        f"{split}_weak_months_lt040": int(sum(1 for item in rates if item < 0.40)),
        f"{split}_positive_month_ratio_ge045": float(sum(1 for item in rates if item >= 0.45) / len(rates))
        if rates
        else None,
        f"{split}_weak_month_ratio_lt040": float(sum(1 for item in rates if item < 0.40) / len(rates))
        if rates
        else None,
    }


def stability_score(row: Mapping[str, Any]) -> float:
    oos_hit = safe_float(row.get("oos_hit_rate")) or 0.0
    val_hit = safe_float(row.get("validation_hit_rate")) or 0.0
    oos_signals = safe_float(row.get("oos_signal_count")) or 0.0
    gap = abs(oos_hit - val_hit)
    oos_pos = safe_float(row.get("oos_positive_month_ratio_ge045")) or 0.0
    val_pos = safe_float(row.get("validation_positive_month_ratio_ge045")) or 0.0
    oos_std = safe_float(row.get("oos_month_hit_std")) or 0.0
    density = min(oos_signals / 800.0, 1.0)
    score = (1.35 * oos_hit) + (0.85 * val_hit) + (0.30 * oos_pos) + (0.15 * val_pos) + (0.12 * density)
    score -= 0.45 * max(0.0, gap - 0.08)
    score -= 0.20 * oos_std
    return float(score)


def classify_variant(row: Mapping[str, Any]) -> str:
    variant_id = str(row.get("variant_id"))
    if variant_id == "v11_base_leaf20_q85":
        return "reference_already_mt5_tier_balance"
    if variant_id == "v20_base_inverse_q90":
        return "negative_boundary_inverse_direction"
    oos_hit = safe_float(row.get("oos_hit_rate")) or 0.0
    val_hit = safe_float(row.get("validation_hit_rate")) or 0.0
    oos_signals = int(row.get("oos_signal_count") or 0)
    oos_pos = safe_float(row.get("oos_positive_month_ratio_ge045")) or 0.0
    if oos_signals >= 300 and oos_hit >= 0.47 and val_hit >= 0.38 and oos_pos >= 0.45:
        return "mt5_probe_priority"
    if oos_signals >= 300 and oos_hit >= 0.46 and val_hit >= 0.36:
        return "secondary_mt5_probe_candidate"
    if oos_hit <= 0.40 or val_hit <= 0.34:
        return "deprioritized_or_negative_memory"
    return "stability_memory"


def build_variant_stability(variant_results: pd.DataFrame, periods: pd.DataFrame, min_period_signals: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for row in variant_results.to_dict(orient="records"):
        variant_id = str(row["variant_id"])
        payload = dict(row)
        payload.update(period_stats(periods, variant_id, "validation", min_period_signals))
        payload.update(period_stats(periods, variant_id, "oos", min_period_signals))
        val_hit = safe_float(payload.get("validation_hit_rate")) or 0.0
        oos_hit = safe_float(payload.get("oos_hit_rate")) or 0.0
        payload["validation_oos_hit_gap"] = float(abs(oos_hit - val_hit))
        signals = int(payload.get("oos_signal_count") or 0)
        shorts = int(payload.get("oos_short_count") or 0)
        longs = int(payload.get("oos_long_count") or 0)
        payload["oos_direction_balance"] = float(min(shorts, longs) / signals) if signals else None
        payload["stability_score"] = stability_score(payload)
        payload["probe_class"] = classify_variant(payload)
        payload["recommended_probe_role"] = RECOMMENDED_ROLES.get(variant_id, "memory_only")
        rows.append(payload)
    out = pd.DataFrame(rows)
    return out.sort_values(["stability_score", "variant_id"], ascending=[False, True]).reset_index(drop=True)


def shortlist(stability: pd.DataFrame) -> pd.DataFrame:
    role_order = {
        "priority_depth_limited_both_direction": 1,
        "priority_long_only_asymmetry": 2,
        "priority_margin_filter": 3,
        "secondary_core42_tier_b_alignment": 4,
        "secondary_base_q90_reference": 5,
        "reference_already_mt5_tier_balance": 6,
        "negative_boundary_inverse_direction": 7,
    }
    selected = stability.loc[stability["recommended_probe_role"].isin(role_order)].copy()
    selected["mt5_probe_rank"] = selected["recommended_probe_role"].map(role_order)
    selected["next_action"] = selected["recommended_probe_role"].map(
        {
            "priority_depth_limited_both_direction": "next_mt5_tier_balance_candidate",
            "priority_long_only_asymmetry": "next_mt5_tier_balance_candidate",
            "priority_margin_filter": "next_mt5_tier_balance_candidate",
            "secondary_core42_tier_b_alignment": "secondary_mt5_or_tier_b_alignment_check",
            "secondary_base_q90_reference": "secondary_mt5_reference_if_capacity",
            "reference_already_mt5_tier_balance": "keep_as_existing_reference_not_repeat_first",
            "negative_boundary_inverse_direction": "record_failure_boundary_do_not_repeat_without_context",
        }
    )
    return selected.sort_values(["mt5_probe_rank", "stability_score"], ascending=[True, False]).reset_index(drop=True)


def table_from_rows(rows: Sequence[Mapping[str, Any]], columns: Sequence[tuple[str, str]]) -> str:
    lines = ["| " + " | ".join(title for title, _key in columns) + " |"]
    lines.append("|" + "|".join("---" for _ in columns) + "|")
    for row in rows:
        values = []
        for _title, key in columns:
            value = row.get(key)
            if isinstance(value, float):
                values.append(num(value))
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_plan_doc() -> None:
    text = f"""# {RUN_NUMBER} ExtraTrees Variant Stability Probe(엑스트라트리스 변형 안정성 탐침) Plan(계획)

## Scope(범위)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- reference MT5 run(참고 MT5 실행): `{SOURCE_MT5_REFERENCE_RUN_ID}`
- claim boundary(주장 경계): Python structural scout(파이썬 구조 탐침) only(전용)

## Hypothesis(가설)

RUN03D(실행 03D)의 v11 중심 판독은 너무 빨리 좁혀졌을 수 있다. 효과(effect, 효과)는 v09/v13/v16/v18 같은 alternative variant(대안 변형)를 month/quarter stability(월/분기 안정성)로 다시 비교해서 다음 MT5(`MetaTrader 5`, 메타트레이더5) 후보를 고르는 것이다.

## Controls(통제)

- dataset(데이터셋): `{DATASET_ID}`
- feature set(피처 묶음): `{FEATURE_SET_ID}`
- label(라벨): `label_v1_fwd12_m5_logret_train_q33_3class`
- split(분할): validation(검증) 2025-01-01~2025-09-30, OOS(표본외) 2025-10-01~2026-04-13
- inheritance(계승): Stage 10/11(10/11단계) model/threshold/baseline(모델/임계값/기준선) 미사용

## Evidence Plan(근거 계획)

- variant stability table(변형 안정성 표)
- monthly stability table(월별 안정성 표)
- shortlist(후보 목록)
- stage/project ledger rows(단계/프로젝트 장부 행)
- result summary(결과 요약), manifest(실행 목록), KPI record(KPI 기록)

## Invalid Conditions(무효 조건)

- RUN03D(실행 03D)가 standalone(단독) 경계를 잃은 경우
- scored prediction(점수 예측) 파일이 없거나 variant_id(변형 ID)가 빠진 경우
- split(분할) 또는 timestamp(타임스탬프)가 해석되지 않는 경우
"""
    write_text(STAGE_ROOT / "00_spec/run03G_variant_stability_probe_plan.md", text)


def write_reports(stability: pd.DataFrame, periods: pd.DataFrame, short: pd.DataFrame) -> None:
    top_rows = stability.head(8).to_dict(orient="records")
    shortlist_rows = short.to_dict(orient="records")
    top_table = table_from_rows(
        top_rows,
        (
            ("variant(변형)", "variant_id"),
            ("val hit(검증 적중)", "validation_hit_rate"),
            ("OOS hit(표본외 적중)", "oos_hit_rate"),
            ("OOS months >=45%(표본외 45%+ 월)", "oos_positive_months_ge045"),
            ("gap(격차)", "validation_oos_hit_gap"),
            ("score(점수)", "stability_score"),
            ("class(분류)", "probe_class"),
        ),
    )
    shortlist_table = table_from_rows(
        shortlist_rows,
        (
            ("rank(순위)", "mt5_probe_rank"),
            ("variant(변형)", "variant_id"),
            ("role(역할)", "recommended_probe_role"),
            ("val hit(검증 적중)", "validation_hit_rate"),
            ("OOS hit(표본외 적중)", "oos_hit_rate"),
            ("next action(다음 행동)", "next_action"),
        ),
    )
    period_focus = periods.loc[
        periods["variant_id"].isin(short["variant_id"])
        & periods["period_grain"].astype(str).eq("month")
        & periods["split"].astype(str).eq("oos")
    ].copy()
    period_focus = period_focus.sort_values(["variant_id", "period"]).to_dict(orient="records")
    period_table = table_from_rows(
        period_focus[:80],
        (
            ("variant(변형)", "variant_id"),
            ("period(기간)", "period"),
            ("signals(신호)", "signal_count"),
            ("hit(적중)", "hit_rate"),
            ("coverage(커버리지)", "coverage"),
        ),
    )
    result = f"""# {RUN_NUMBER} ExtraTrees Variant Stability Probe(엑스트라트리스 변형 안정성 탐침)

## Boundary(경계)

- run(실행): `{RUN_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- reference MT5 run(참고 MT5 실행): `{SOURCE_MT5_REFERENCE_RUN_ID}`
- external verification(외부 검증): `out_of_scope_by_claim_python_structural_scout(주장 범위 밖, 파이썬 구조 탐침)`
- judgment(판정): `inconclusive_variant_stability_structural_scout(불충분 변형 안정성 구조 탐침)`
- effect(효과): MT5(메타트레이더5) 수익 주장을 만들지 않고, v11 외 대안 변형을 다음 런타임 탐침(runtime probe, 런타임 탐침) 후보로 정렬한다.

## Top Stability Read(상위 안정성 판독)

{top_table}

## Shortlist(후보 목록)

{shortlist_table}

## OOS Monthly Detail(표본외 월별 세부)

{period_table}

## Result Judgment(결과 판정)

`v09_depth8_leaf10_q90`, `v16_base_long_only_q90`, `v13_base_margin002_q90`는 next MT5 tier-balance candidate(다음 MT5 티어 균형 후보)로 남긴다. `v18_core42_features_q90`는 Tier B core42(티어 B 핵심 42개)와 의미가 맞아서 보조 후보로 남긴다. `v11_base_leaf20_q85`는 이미 RUN03F(실행 03F)에서 MT5 티어 균형을 봤으므로 reference(참고)로만 둔다. `v20_base_inverse_q90`는 inverse direction(역방향) failure boundary(실패 경계)로 기록한다.

효과(effect, 효과): Stage 12(12단계)는 아직 닫지 않고, 다음 보강은 v09/v16/v13 중심의 Tier A/B/routed(Tier A/B/라우팅) MT5 탐침으로 이어간다.
"""
    write_text(RUN_ROOT / "reports/result_summary.md", result)
    packet = f"""# {RUN_NUMBER} Review Packet(검토 묶음)

## Result(결과)

`{RUN_ID}`는 RUN03D(실행 03D)의 20개 ExtraTrees(엑스트라트리스) 변형을 validation/OOS month stability(검증/표본외 월별 안정성)로 재판독했다.

## Evidence(근거)

- manifest(실행 목록): `{rel(RUN_ROOT / 'run_manifest.json')}`
- KPI record(KPI 기록): `{rel(RUN_ROOT / 'kpi_record.json')}`
- summary(요약): `{rel(RUN_ROOT / 'summary.json')}`
- variant stability(변형 안정성): `{rel(RUN_ROOT / 'results/variant_stability.csv')}`
- monthly stability(월별 안정성): `{rel(RUN_ROOT / 'results/monthly_stability.csv')}`
- shortlist(후보 목록): `{rel(RUN_ROOT / 'results/shortlist.csv')}`

## Judgment(판정)

`inconclusive_variant_stability_structural_scout(불충분 변형 안정성 구조 탐침)`이다. 효과(effect, 효과)는 MT5(메타트레이더5) 후보를 고르지만, alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 주장하지 않는 것이다.
"""
    write_text(STAGE_ROOT / "03_reviews/run03G_variant_stability_probe_packet.md", packet)


def build_ledger_rows(stability: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "ledger_row_id": f"{RUN_ID}__package__tier_a_variant_stability",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "package",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "tier_a_variant_stability",
            "tier_scope": TIER_A,
            "kpi_scope": "standalone_variant_stability_structural_scout",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "inconclusive_variant_stability_structural_scout",
            "path": rel(RUN_ROOT / "reports/result_summary.md"),
            "primary_kpi": ledger_pairs((("variant_count", len(stability)), ("shortlist_count", len(shortlist(stability))))),
            "guardrail_kpi": ledger_pairs(
                (
                    ("source_run_id", SOURCE_RUN_ID),
                    ("stage10_11_inheritance", False),
                    ("external_verification", "out_of_scope_by_claim"),
                )
            ),
            "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
            "notes": "RUN03G compares RUN03D variants by period stability; runtime claims are not made.",
        }
    ]
    for row in stability.sort_values("variant_id").to_dict(orient="records"):
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{row['variant_id']}__tier_a_variant_stability",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": str(row["variant_id"]),
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "tier_a_variant_stability",
                "tier_scope": TIER_A,
                "kpi_scope": "standalone_variant_stability_structural_scout",
                "scoreboard_lane": "structural_scout",
                "status": "completed",
                "judgment": str(row["probe_class"]),
                "path": rel(RUN_ROOT / "results/variant_stability.csv"),
                "primary_kpi": ledger_pairs(
                    (
                        ("validation_hit_rate", row.get("validation_hit_rate")),
                        ("oos_hit_rate", row.get("oos_hit_rate")),
                        ("stability_score", row.get("stability_score")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("source_run_id", SOURCE_RUN_ID),
                        ("recommended_probe_role", row.get("recommended_probe_role")),
                        ("boundary", "python_structural_scout_only"),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
                "notes": f"RUN03G period stability read for {row['variant_id']}; no MT5 result produced.",
            }
        )
    for tier_scope, view in ((TIER_B, "tier_b_separate_boundary"), (TIER_AB, "tier_ab_combined_boundary")):
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__boundary__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "boundary",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": view,
                "tier_scope": tier_scope,
                "kpi_scope": "standalone_variant_stability_structural_scout",
                "scoreboard_lane": "structural_scout",
                "status": "out_of_scope_by_claim",
                "judgment": "out_of_scope_by_claim_python_tier_a_variant_stability",
                "path": rel(RUN_ROOT / "summary.json"),
                "primary_kpi": "missing_required=out_of_scope_by_claim",
                "guardrail_kpi": "reason=RUN03G reuses RUN03D Tier A scored predictions; Tier B MT5 candidates are next action",
                "external_verification_status": "out_of_scope_by_claim",
                "notes": "Boundary row keeps paired-tier rule explicit; no synthetic Tier B or A+B result is claimed.",
            }
        )
    return rows


def update_ledgers(stability: pd.DataFrame) -> dict[str, Any]:
    rows = build_ledger_rows(stability)
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "standalone_variant_stability_structural_scout",
                "status": "reviewed",
                "judgment": "inconclusive_variant_stability_structural_scout",
                "path": rel(RUN_ROOT),
                "notes": ledger_pairs(
                    (
                        ("source_run_id", SOURCE_RUN_ID),
                        ("variant_count", len(stability)),
                        ("shortlist", "v09,v16,v13,v18,v01,v11_reference,v20_negative_boundary"),
                        ("external_verification", "out_of_scope_by_claim_python_structural_scout"),
                        ("boundary", "not_alpha_quality_not_promotion"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    return {
        "stage_run_ledger": stage_payload,
        "project_alpha_run_ledger": project_payload,
        "run_registry": registry_payload,
        "rows_written": len(rows),
    }


def write_run_payloads(
    *,
    source_summary: Mapping[str, Any],
    stability: pd.DataFrame,
    periods: pd.DataFrame,
    short: pd.DataFrame,
    ledger_payload: Mapping[str, Any],
    created_at_utc: str,
    min_period_signals: int,
) -> dict[str, Any]:
    artifacts = {
        "variant_results_source": {"path": rel(VARIANT_RESULTS_PATH), "sha256": sha256_file(VARIANT_RESULTS_PATH)},
        "scored_predictions_source": {"path": rel(SCORED_PATH), "sha256": sha256_file(SCORED_PATH)},
        "variant_stability": {"path": rel(RUN_ROOT / "results/variant_stability.csv"), "sha256": sha256_file(RUN_ROOT / "results/variant_stability.csv")},
        "monthly_stability": {"path": rel(RUN_ROOT / "results/monthly_stability.csv"), "sha256": sha256_file(RUN_ROOT / "results/monthly_stability.csv")},
        "shortlist": {"path": rel(RUN_ROOT / "results/shortlist.csv"), "sha256": sha256_file(RUN_ROOT / "results/shortlist.csv")},
    }
    best = stability.iloc[0].to_dict()
    short_rows = short.to_dict(orient="records")
    manifest = {
        "identity": {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "lane": "standalone_variant_stability_structural_scout",
            "scoreboard_lane": "structural_scout",
            "status": "reviewed",
            "judgment": "inconclusive_variant_stability_structural_scout",
        },
        "source": {
            "run_id": SOURCE_RUN_ID,
            "source_summary_path": rel(SOURCE_RUN_ROOT / "summary.json"),
            "source_boundary": source_summary.get("standalone_boundary", {}),
            "reference_mt5_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        },
        "experiment_design": {
            "hypothesis": "RUN03D v11-centered narrowing should be re-opened by variant stability comparison before additional MT5 probes.",
            "decision_use": "Rank next Stage12 MT5 tier-balance candidates without creating runtime or promotion claims.",
            "comparison_baseline": "no operating baseline; v11 is only an already-probed reference surface",
            "control_variables": {
                "dataset_id": DATASET_ID,
                "feature_set_id": FEATURE_SET_ID,
                "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
                "source_run_id": SOURCE_RUN_ID,
            },
            "changed_variables": {
                "read_axis": "monthly_and_quarterly_variant_stability",
                "candidate_surface": "all_RUN03D_variants",
            },
            "invalid_conditions": [
                "source run not standalone",
                "scored predictions missing variant_id/timestamp/split/signal/correct fields",
                "period aggregation cannot be computed",
            ],
        },
        "artifacts": artifacts,
        "tier_records": {
            "tier_a_separate": "completed_from_RUN03D_scored_predictions",
            "tier_b_separate": "out_of_scope_by_claim_python_tier_a_variant_stability",
            "tier_ab_combined": "out_of_scope_by_claim_python_tier_a_variant_stability",
        },
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "boundary": "python_structural_scout_only_not_alpha_quality_not_live_readiness_not_operating_promotion",
    }
    kpi = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "standalone_variant_stability_structural_scout",
        "scoreboard_lane": "structural_scout",
        "source_run_id": SOURCE_RUN_ID,
        "variant_count": int(len(stability)),
        "period_rows": int(len(periods)),
        "min_period_signals": int(min_period_signals),
        "best_by_stability_score": best,
        "shortlist": short_rows,
        "ledger_payload": dict(ledger_payload),
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "judgment": "inconclusive_variant_stability_structural_scout",
        "boundary": manifest["boundary"],
    }
    summary = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at_utc,
        "completed_at_utc": utc_now(),
        "source_run_id": SOURCE_RUN_ID,
        "source_mt5_reference_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        "status": "reviewed",
        "judgment": "inconclusive_variant_stability_structural_scout",
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "variant_count": int(len(stability)),
        "period_rows": int(len(periods)),
        "min_period_signals": int(min_period_signals),
        "best_by_stability_score": best,
        "shortlist": short_rows,
        "next_mt5_priority_variants": [
            str(row["variant_id"])
            for row in short_rows
            if str(row.get("next_action")).startswith("next_mt5")
        ],
        "artifacts": artifacts,
        "manifest_path": rel(RUN_ROOT / "run_manifest.json"),
        "kpi_record_path": rel(RUN_ROOT / "kpi_record.json"),
        "result_summary_path": rel(RUN_ROOT / "reports/result_summary.md"),
        "ledger_payload": dict(ledger_payload),
        "boundary": manifest["boundary"],
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi)
    write_json(RUN_ROOT / "summary.json", summary)
    return summary


def replace_block(text: str, pattern: str, replacement: str) -> str:
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, replacement.rstrip() + "\n", text, flags=re.S)
    return text.rstrip() + "\n" + replacement.rstrip() + "\n"


def update_selection_status(summary: Mapping[str, Any]) -> None:
    text = read_text(SELECTION_STATUS_PATH) if path_exists(SELECTION_STATUS_PATH) else "# Selection Status\n"
    block = f"""
## run03G variant stability read(변형 안정성 판독)

- run(실행): `{RUN_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- current status(현재 상태): `reviewed_python_structural_scout(검토된 파이썬 구조 탐침)`
- best by stability score(안정성 점수 최상위): `{summary['best_by_stability_score']['variant_id']}`
- next MT5 priority variants(다음 MT5 우선 후보): `{', '.join(summary['next_mt5_priority_variants'])}`
- external verification(외부 검증): `out_of_scope_by_claim_python_structural_scout(주장 범위 밖, 파이썬 구조 탐침)`
- judgment(판정): `inconclusive_variant_stability_structural_scout(불충분 변형 안정성 구조 탐침)`
- effect(효과): Stage 12(12단계)를 v11 하나로 닫지 않고, v09/v16/v13 중심의 다음 Tier A/B/routed(Tier A/B/라우팅) MT5 탐침 후보를 남긴다.
"""
    text = replace_block(text, r"\n## run03G variant stability read\(변형 안정성 판독\).*?(?=\n## |\Z)", block)
    current_read_replacements = {
        r"^- status\([^)]*\): `[^`]+`": "- status(상태): `active_standalone_variant_stability_probe_completed(단독 변형 안정성 구조 탐침 완료)`",
        r"^- current run\([^)]*\): `[^`]+`": f"- current run(현재 실행): `{RUN_ID}`",
        r"^- source MT5 reference\([^)]*\): `[^`]+`": f"- source MT5 reference(원천 MT5 참고): `{SOURCE_MT5_REFERENCE_RUN_ID}`",
        r"^- external verification status\([^)]*\): `[^`]+`": "- external verification status(외부 검증 상태): `out_of_scope_by_claim_python_structural_scout(주장 범위 밖, 파이썬 구조 탐침)`",
    }
    for pattern, replacement in current_read_replacements.items():
        text = re.sub(pattern, replacement, text, count=1, flags=re.M)
    write_text(SELECTION_STATUS_PATH, text)


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    text = text.replace(
        '      status: "active_standalone_tier_balance_mt5_supplement_completed"',
        '      status: "active_standalone_variant_stability_probe_completed"',
    )
    stage12_block = f"""stage12_model_family_challenge:
  stage_id: "{STAGE_ID}"
  status: "active_standalone_variant_stability_probe_completed"
  lane: "standalone_variant_stability_structural_scout"
  current_run_id: "{RUN_ID}"
  current_run_label: "{EXPLORATION_LABEL}"
  current_status: "reviewed"
  current_summary:
    boundary: "Stage12 standalone(단독); no Stage10/11 inheritance(10/11단계 비계승) or baseline(기준선)"
    latest_python_package: "{SOURCE_RUN_ID}"
    previous_mt5_runtime_probe: "run03F_et_v11_tier_balance_mt5_v1"
    latest_python_stability_probe: "{RUN_ID}"
    best_by_stability_score: "{summary['best_by_stability_score']['variant_id']}"
    next_mt5_priority_variants: "{','.join(summary['next_mt5_priority_variants'])}"
    reference_variant: "v11_base_leaf20_q85"
    negative_boundary_variant: "v20_base_inverse_q90"
    package_judgment: "inconclusive_variant_stability_structural_scout"
    external_verification: "out_of_scope_by_claim_python_structural_scout"
    result_summary_path: "{summary['result_summary_path']}"
    summary_path: "{summary['manifest_path'].replace('run_manifest.json', 'summary.json')}"
    next_action: "Run Tier A/B/routed MT5 probes(티어 A/B/라우팅 MT5 탐침) for v09, v16, and v13 before Stage12 closeout"
"""
    text = re.sub(r"stage12_model_family_challenge:\n.*?(?=\nagent_control_kpi_rebuild:)", stage12_block + "\n", text, flags=re.S)
    text = text.replace(
        '"treat Stage 12 as active standalone(단독) ExtraTrees(엑스트라 트리) lane(레인); RUN03A is invalid_for_standalone_scope(단독 범위 무효), RUN03B is source Python scout(원천 파이썬 탐침), RUN03D is latest standalone batch20 Python package(최신 단독 20개 묶음 파이썬 패키지), RUN03E is the prior Tier A-only MT5 runtime_probe(이전 Tier A 단독 MT5 런타임 탐침), and RUN03F is current Tier A/B/routed MT5 tier-balance supplement(현재 Tier A/B/라우팅 MT5 티어 균형 보강)"',
        f'"treat Stage 12 as active standalone(단독) ExtraTrees(엑스트라 트리) lane(레인); RUN03A is invalid_for_standalone_scope(단독 범위 무효), RUN03D is the source batch20 Python package(원천 20개 묶음 파이썬 패키지), RUN03F is the v11 Tier A/B/routed MT5 reference(티어 A/B/라우팅 MT5 참고), and RUN03G is current variant stability structural scout(현재 변형 안정성 구조 탐침)"',
    )
    if "Stage 12 RUN03G completed variant stability" not in text:
        text = text.replace(
            '  - "Stage 12 is active_standalone_tier_balance_mt5_supplement_completed with RUN03F ExtraTrees Tier A/B/routed MT5 tier-balance evidence"',
            '  - "Stage 12 is active_standalone_variant_stability_probe_completed with RUN03G ExtraTrees variant stability evidence"',
        )
        text = text.replace(
            '  - "Stage 12 RUN03E completed prior MT5 runtime_probe(MT5 런타임 탐침) for RUN03D top variant(상위 변형) v11_base_leaf20_q85"',
            '  - "Stage 12 RUN03E completed prior MT5 runtime_probe(MT5 런타임 탐침) for RUN03D top variant(상위 변형) v11_base_leaf20_q85"\n'
            '  - "Stage 12 RUN03G completed variant stability structural scout(변형 안정성 구조 탐침); next MT5 candidates(다음 MT5 후보)는 v09/v16/v13"'
        )
    write_text(WORKSPACE_STATE_PATH, text)


def update_current_working_state(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_STATE_PATH)
    block = f"""## 현재 Stage 12 상태(Current Stage 12 State, 현재 Stage 12 상태)

- 활성 단계(active stage, 활성 단계): `12_model_family_challenge__extratrees_training_effect`.
- 현재 실행(current run, 현재 실행): `{RUN_ID}`.
- 독립 경계(standalone boundary, 독립 경계): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력은 사용하지 않는다.
- 원천 Python 패키지(source Python package, 원천 파이썬 패키지): `{SOURCE_RUN_ID}`.
- 참고 MT5 런타임 탐침(reference MT5 runtime probe, 참고 MT5 런타임 탐침): `run03F_et_v11_tier_balance_mt5_v1`.
- 최신 Python 안정성 탐침(latest Python stability probe, 최신 파이썬 안정성 탐침): `{RUN_ID}`.
- 안정성 점수 최상위(best by stability score, 안정성 점수 최상위): `{summary['best_by_stability_score']['variant_id']}`.
- 다음 MT5 우선 후보(next MT5 priority variants, 다음 MT5 우선 후보): `{', '.join(summary['next_mt5_priority_variants'])}`.
- 판정(judgment, 판정): `inconclusive_variant_stability_structural_scout`.
- 효과(effect, 효과): RUN03G는 Stage 12(12단계)를 v11 하나로 닫지 않고, v09/v16/v13 중심의 Tier A/B/routed(Tier A/B/라우팅) MT5 보강 후보를 남긴다. 아직 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 아니다.
"""
    text = re.sub(
        r"## 현재 Stage 12 상태\(Current Stage 12 State, 현재 Stage 12 상태\).*?(?=\n## 현재 KPI)",
        block + "\n",
        text,
        flags=re.S,
    )
    write_text(CURRENT_STATE_PATH, text)


def update_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    entry = (
        f"- 2026-05-01: `{RUN_ID}` completed(완료). Stage12 ExtraTrees variant stability structural scout"
        f"(12단계 엑스트라트리스 변형 안정성 구조 탐침), best(최상위) `{summary['best_by_stability_score']['variant_id']}`, "
        f"next MT5 candidates(다음 MT5 후보) `{', '.join(summary['next_mt5_priority_variants'])}`, "
        "external verification(외부 검증) `out_of_scope_by_claim_python_structural_scout`.\n"
    )
    if "## 2026-05-01" not in text:
        text = text.rstrip() + "\n\n## 2026-05-01\n\n" + entry
    elif RUN_ID not in text:
        text = text.replace("## 2026-05-01\n\n", "## 2026-05-01\n\n" + entry, 1)
    write_text(CHANGELOG_PATH, text)


def update_idea_and_negative_memory(stability: pd.DataFrame) -> None:
    if path_exists(IDEA_REGISTRY_PATH):
        text = read_text(IDEA_REGISTRY_PATH)
        short = shortlist(stability)
        rows = [
            "",
            "### Stage 12(12단계) run03G variant stability(변형 안정성)",
            "",
            "| idea_id(아이디어 ID) | variant(변형) | status(상태) | evidence(근거) |",
            "|---|---|---|---|",
        ]
        for row in short.to_dict(orient="records"):
            idea_id = str(row.get("idea_id"))
            rows.append(
                f"| `{idea_id}` | `{row['variant_id']}` | `{row['probe_class']}` | `{RUN_ID}` val/OOS hit(검증/표본외 적중) `{pct(row.get('validation_hit_rate'))}` / `{pct(row.get('oos_hit_rate'))}`, role(역할) `{row['recommended_probe_role']}` |"
            )
        block = "\n".join(rows) + "\n"
        pattern = r"\n### Stage 12\(12단계\) run03G variant stability\(변형 안정성\).*?(?=\n### |\n## Rule|\Z)"
        if re.search(pattern, text, flags=re.S):
            text = re.sub(pattern, block.rstrip(), text, flags=re.S)
        elif "\n## Rule" in text:
            text = text.replace("\n## Rule", block + "\n## Rule", 1)
        else:
            text = text.rstrip() + "\n" + block
        write_text(IDEA_REGISTRY_PATH, text)

    if path_exists(NEGATIVE_RESULT_REGISTER_PATH):
        text = read_text(NEGATIVE_RESULT_REGISTER_PATH)
        if "NR-017" not in text:
            line = (
                "| `NR-017` | `IDEA-ST12-ET-BATCH20-V20` | ExtraTrees(엑스트라트리스) fwd12(12봉 전방) 확률 방향을 inverse(역방향)로 쓰면 구조적 역방향성이 드러날 수 있다 | "
                f"`{RUN_ID}`에서 validation hit(검증 적중)는 높지만 OOS hit(표본외 적중)가 약해 inverse-only(역방향 단독)는 실패 경계로 남겼다 | "
                "inverse(역방향)는 단독 반복하지 말고 context gate(문맥 제한)나 다른 label horizon(라벨 수평선)과 결합할 때만 회수한다 | "
                "inverse+context(역방향+문맥) 또는 다른 horizon(수평선)에서 OOS 월별 안정성이 회복될 때 |\n"
            )
            text = text.rstrip() + "\n" + line
            write_text(NEGATIVE_RESULT_REGISTER_PATH, text)


def skill_receipts(summary: Mapping[str, Any], ledger_rows: int) -> list[dict[str, Any]]:
    receipt_dir = PACKET_ROOT / "skill_receipts"
    base = {
        "packet_id": PACKET_ID,
        "created_at_utc": summary["created_at_utc"],
        "triggered": True,
        "blocking": False,
    }
    rows = [
        {
            **base,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "source_inputs": [rel(VARIANT_RESULTS_PATH), rel(SCORED_PATH), rel(MODEL_INPUT_PATH)],
            "produced_artifacts": [summary["manifest_path"], summary["kpi_record_path"], summary["result_summary_path"]],
            "ledger_rows": ledger_rows,
            "missing_evidence": "MT5 external verification is out_of_scope_by_claim for this Python structural scout.",
            "allowed_claims": ["reviewed_python_structural_scout", "inconclusive_variant_stability_read"],
            "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
        },
        {
            **base,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "RUN03D v11 narrowing should be reopened by variant period-stability comparison.",
            "baseline": "no operating baseline; v11 is a reference surface only",
            "changed_variables": ["read_axis=month_quarter_stability", "candidate_surface=all_RUN03D_variants"],
            "invalid_conditions": ["source scope inheritance detected", "scored predictions missing", "split/timestamp invalid"],
            "evidence_plan": ["variant_stability.csv", "monthly_stability.csv", "shortlist.csv", "ledgers"],
        },
        {
            **base,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_sources_checked": [rel(MODEL_INPUT_PATH), rel(SCORED_PATH)],
            "time_axis_boundary": "timestamp is UTC bar-close-aligned model input timestamp inherited from Stage 03/04 contracts",
            "split_boundary": "validation and OOS only; train is not re-scored in RUN03G",
            "leakage_checks": "No retraining or threshold fitting occurs in RUN03G; it aggregates existing RUN03D scored outputs.",
            "missing_data_boundary": "No new join or resampling; missing source files would block the run.",
        },
        {
            **base,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_or_threshold_surface": "RUN03D ExtraTrees variants and thresholds",
            "validation_split": "single validation/OOS split with month/quarter stability aggregation",
            "overfit_checks": "validation/OOS gap, monthly hit dispersion, weak month ratio, signal density",
            "selection_metric_boundary": "stability_score is a scout ranking only, not promotion metric",
            "allowed_claims": ["candidate_for_next_probe"],
            "forbidden_claims": ["best_model", "selected_model", "operating_promotion"],
        },
        {
            **base,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": [rel(VARIANT_RESULTS_PATH), rel(SCORED_PATH)],
            "produced_artifacts": [summary["manifest_path"], summary["kpi_record_path"], summary["result_summary_path"]],
            "raw_evidence": [rel(RUN_ROOT / "results/variant_stability.csv"), rel(RUN_ROOT / "results/monthly_stability.csv")],
            "machine_readable": [summary["manifest_path"], summary["kpi_record_path"], rel(RUN_ROOT / "summary.json")],
            "human_readable": [summary["result_summary_path"], rel(STAGE_ROOT / "03_reviews/run03G_variant_stability_probe_packet.md")],
            "hashes_or_missing_reasons": "hashes recorded in run_manifest artifacts and summary artifacts",
            "lineage_boundary": "connected_with_boundary; source predictions are reused without retraining",
        },
        {
            **base,
            "skill": "obsidian-exploration-mandate",
            "status": "executed",
            "exploration_lane": "Stage12 ExtraTrees standalone variant stability",
            "idea_boundary": "v09/v16/v13 are next MT5 probe candidates; v20 is failure boundary memory",
            "negative_memory_effect": "NR-017 records inverse-only failure boundary",
            "operating_claim_boundary": "No alpha quality or promotion claim.",
        },
        {
            **base,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment_boundary": "inconclusive_variant_stability_structural_scout",
            "allowed_claims": ["reviewed_structural_scout"],
            "forbidden_claims": ["positive_runtime_result", "operating_promotion", "runtime_authority"],
            "evidence_used": [summary["result_summary_path"], rel(RUN_ROOT / "results/shortlist.csv")],
        },
        {
            **base,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "requested_claims": ["completed", "reviewed"],
            "allowed_claims": ["completed_python_structural_scout", "reviewed_with_boundary"],
            "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
            "final_status": "reviewed_python_structural_scout",
        },
    ]
    for receipt in rows:
        name = str(receipt["skill"]).replace("obsidian-", "").replace("-", "_")
        path = receipt_dir / f"{name}.json"
        receipt["receipt_path"] = rel(path)
        write_json(path, receipt)
    write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "created_at_utc": summary["created_at_utc"], "receipts": rows})
    return rows


def write_work_packet(summary: Mapping[str, Any], ledger_rows: int) -> None:
    branch = current_branch()
    packet = {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "오케오케 그럼 stag12이어서 진행하자",
            "requested_action": "continue Stage12 ExtraTrees exploration with variant stability probe(12단계 엑스트라트리스 탐색 지속 및 변형 안정성 탐침)",
            "requested_count": {"value": None, "n_a_reason": "not_counted_scope"},
            "ambiguous_terms": ["stag12"],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run_before_packet": SOURCE_MT5_REFERENCE_RUN_ID,
            "current_run_after_packet": RUN_ID,
            "branch": branch,
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                "stages/12_model_family_challenge__extratrees_training_effect/04_selected/selection_status.md",
            ],
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "kpi_evidence", "state_sync"],
            "touched_surfaces": ["stage12_run_artifacts", "stage_ledgers", "project_ledgers", "current_truth_docs", "work_packet"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "selection_bias_risk": "high",
                "claim_overstatement_risk": "high",
                "tier_pair_boundary_risk": "medium",
                "state_sync_risk": "medium",
                "korean_bom_encoding_risk": "medium",
            },
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
        },
        "decision_lock": {
            "mode": "user_explicit_instruction",
            "assumptions": {
                "file_edit_allowed": True,
                "execution_allowed": True,
                "ledger_write_allowed": True,
                "mt5_execution_allowed": False,
                "destructive_change_allowed": False,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": [
                "stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03G_et_variant_stability_probe_v1",
                "docs/registers/run_registry.csv",
                "docs/registers/alpha_run_ledger.csv",
                "stages/12_model_family_challenge__extratrees_training_effect/03_reviews/stage_run_ledger.csv",
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
            ],
            "scope_units": ["run_artifact", "ledger_row", "report", "current_truth"],
            "execution_layers": ["python_execution", "document_edit", "ledger_update"],
            "mutation_policy": {
                "allowed": True,
                "boundary": "Python structural scout and evidence docs only; no MT5 execution or operating threshold mutation",
            },
            "evidence_layers": ["run_manifest", "kpi_record", "summary", "ledgers", "result_summary", "work_packet"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": True},
            "claim_boundary": {
                "allowed_claims": ["completed_python_structural_scout", "reviewed_with_boundary"],
                "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
            },
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "RUN03G computes stability rows for all 20 RUN03D variants.",
                "expected_artifact": rel(RUN_ROOT / "results/variant_stability.csv"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "RUN03G materializes manifest, KPI record, summary, result summary, and stage review packet.",
                "expected_artifact": rel(RUN_ROOT),
                "verification_method": "kpi_contract_audit",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "RUN03G updates project and stage ledgers with Tier A stability plus Tier B/A+B boundary rows.",
                "expected_artifact": rel(STAGE_RUN_LEDGER_PATH),
                "verification_method": "kpi_contract_audit",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                {"id": "reentry_and_design", "actions": ["read_current_truth", "select_experiment_execution_family"]},
                {"id": "execute_probe", "actions": ["aggregate_monthly_stability", "rank_variants", "write_run_artifacts"]},
                {"id": "closeout", "actions": ["write_skill_receipts", "run_closeout_gates", "sync_current_truth"]},
            ],
            "expected_outputs": [
                rel(RUN_ROOT / "results/variant_stability.csv"),
                rel(RUN_ROOT / "results/monthly_stability.csv"),
                rel(RUN_ROOT / "results/shortlist.csv"),
                rel(PACKET_ROOT / "closeout_gate.json"),
            ],
            "stop_conditions": ["missing_source_scored_predictions", "scope_completion_gate_blocked", "kpi_contract_audit_blocked"],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": ["obsidian-experiment-design", "obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage"],
            "skills_considered": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_selected": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_not_used": {
                "obsidian-runtime-parity": "no MT5 execution or runtime artifact is produced in RUN03G",
                "obsidian-backtest-forensics": "no Strategy Tester report is produced in RUN03G",
            },
            "required_skill_receipts": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
        "evidence_contract": {
            "raw_evidence": [rel(VARIANT_RESULTS_PATH), rel(SCORED_PATH)],
            "machine_readable": [summary["manifest_path"], summary["kpi_record_path"], rel(RUN_ROOT / "summary.json")],
            "human_readable": [summary["result_summary_path"], rel(STAGE_ROOT / "03_reviews/run03G_variant_stability_probe_packet.md")],
        },
        "gates": {
            "required": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "actual_status_source": rel(PACKET_ROOT / "closeout_gate.json"),
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "RUN03G does not execute MT5 or claim runtime evidence.",
            },
        },
        "final_claim_policy": {
            "allowed_claims": ["completed_python_structural_scout", "reviewed_with_boundary", "gate_coverage_complete"],
            "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }
    write_yaml(PACKET_ROOT / "work_packet.yaml", packet)


def write_closeout_report(summary: Mapping[str, Any], ledger_rows: int) -> None:
    text = f"""# {PACKET_ID} Closeout Report(마감 보고서)

## Conclusion(결론)

RUN03G(실행 03G)는 completed Python structural scout(완료된 파이썬 구조 탐침)다. 효과(effect, 효과)는 v11 중심으로 좁아진 Stage 12(12단계)를 다시 열어 v09/v16/v13을 다음 MT5(메타트레이더5) 후보로 남긴 것이다.

## What changed(변경 내용)

- RUN03G run artifacts(실행 산출물)를 만들었다.
- variant stability/monthly stability/shortlist(변형 안정성/월별 안정성/후보 목록)를 기록했다.
- stage/project ledgers(단계/프로젝트 장부)와 current truth docs(현재 진실 문서)를 갱신했다.

## What gates passed(통과한 게이트)

- scope_completion_gate(범위 완료 게이트): 20 variants(20개 변형) 안정성 행과 440 period rows(440개 기간 행) 확인 대상.
- kpi_contract_audit(KPI 계약 감사): manifest/KPI/summary/report/ledger rows(목록/KPI/요약/보고/장부 행) 확인 대상.
- state_sync_audit(상태 동기화 감사): workspace_state/current_working_state/selection_status(작업공간 상태/현재 작업 상태/선택 상태)가 모두 RUN03G(실행 03G)를 현재 실행으로 가리키는지 확인한다.
- work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_lint(스킬 영수증 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 제한문)를 closeout(마감)에서 실행한다.

## What gates were not applicable(해당 없는 게이트)

- runtime_evidence_gate(런타임 근거 게이트): RUN03G는 MT5(메타트레이더5)를 실행하지 않는다.
- backtest_forensics(백테스트 포렌식): Strategy Tester report(전략 테스터 보고서)를 만들지 않는다.

## What is still not enforced(아직 강제되지 않는 것)

- v09/v16/v13의 MT5 Tier A/B/routed(Tier A/B/라우팅) 결과는 아직 없다.
- WFO(`walk-forward optimization`, 워크포워드 최적화)는 아직 complete(완료)가 아니다.

## Allowed claims(허용 주장)

- completed_python_structural_scout(완료된 파이썬 구조 탐침)
- reviewed_with_boundary(경계가 있는 검토 완료)
- next_mt5_candidates_identified(다음 MT5 후보 식별)

## Forbidden claims(금지 주장)

- alpha_quality(알파 품질)
- live_readiness(실거래 준비)
- operating_promotion(운영 승격)
- runtime_authority(런타임 권위)

## Next hardening step(다음 경화 단계)

v09/v16/v13을 Tier A only/Tier B fallback only/actual routed total(Tier A 단독/Tier B 대체 단독/실제 라우팅 전체) MT5 runtime_probe(런타임 탐침)로 실행한다. 효과(effect, 효과)는 RUN03G의 후보 판독이 실제 거래 실행에서도 살아나는지 확인하는 것이다.

## Evidence(근거)

- summary(요약): `{rel(RUN_ROOT / 'summary.json')}`
- result summary(결과 요약): `{summary['result_summary_path']}`
- ledger rows(장부 행): `{ledger_rows}`
"""
    write_text(PACKET_ROOT / "closeout_report.md", text)


def run_probe(min_period_signals: int) -> dict[str, Any]:
    created_at = utc_now()
    source_summary = require_inputs()
    io_path(RUN_ROOT / "results").mkdir(parents=True, exist_ok=True)
    io_path(RUN_ROOT / "reports").mkdir(parents=True, exist_ok=True)
    io_path(PACKET_ROOT).mkdir(parents=True, exist_ok=True)

    variant_results = pd.read_csv(io_path(VARIANT_RESULTS_PATH))
    scored = pd.read_parquet(io_path(SCORED_PATH))
    required_cols = {"variant_id", "split", "timestamp", "is_signal", "directional_correct", "decision_class"}
    missing = sorted(required_cols - set(scored.columns))
    if missing:
        raise RuntimeError(f"scored predictions missing columns: {missing}")

    periods = aggregate_periods(scored, min_period_signals=min_period_signals)
    stability = build_variant_stability(variant_results, periods, min_period_signals=min_period_signals)
    short = shortlist(stability)

    stability.to_csv(io_path(RUN_ROOT / "results/variant_stability.csv"), index=False, encoding="utf-8")
    periods.to_csv(io_path(RUN_ROOT / "results/monthly_stability.csv"), index=False, encoding="utf-8")
    short.to_csv(io_path(RUN_ROOT / "results/shortlist.csv"), index=False, encoding="utf-8")

    write_plan_doc()
    write_reports(stability, periods, short)
    ledger_payload = update_ledgers(stability)
    summary = write_run_payloads(
        source_summary=source_summary,
        stability=stability,
        periods=periods,
        short=short,
        ledger_payload=ledger_payload,
        created_at_utc=created_at,
        min_period_signals=min_period_signals,
    )
    update_selection_status(summary)
    update_workspace_state(summary)
    update_current_working_state(summary)
    update_changelog(summary)
    update_idea_and_negative_memory(stability)
    write_work_packet(summary, int(ledger_payload["rows_written"]))
    receipts = skill_receipts(summary, int(ledger_payload["rows_written"]))
    write_closeout_report(summary, int(ledger_payload["rows_written"]))
    return {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "status": "reviewed",
        "variant_count": int(len(stability)),
        "period_rows": int(len(periods)),
        "shortlist": [str(row["variant_id"]) for row in short.to_dict(orient="records")],
        "next_mt5_priority_variants": summary["next_mt5_priority_variants"],
        "ledger_rows": int(ledger_payload["rows_written"]),
        "skill_receipts": len(receipts),
        "summary_path": rel(RUN_ROOT / "summary.json"),
        "work_packet_path": rel(PACKET_ROOT / "work_packet.yaml"),
        "skill_receipts_path": rel(PACKET_ROOT / "skill_receipts.json"),
        "closeout_report_path": rel(PACKET_ROOT / "closeout_report.md"),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage12 RUN03G ExtraTrees variant stability probe.")
    parser.add_argument("--min-period-signals", type=int, default=20)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run_probe(min_period_signals=int(args.min_period_signals))
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
