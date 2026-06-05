from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

STAGE_ID = "343_quality_margin_runtime__early_long_mix_mt5_probe"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run343F"
RUN_ID = "run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1"
REFERENCE_REVIEW_RUN_ID = "run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run343G_design_directional_long_supply_quality_surface_without_db_v1"

STATUS = "completed_stage343F_trade_shape_rescue_reviewed_profit_anchor_preserved_trade_shape_unresolved_no_selection"
JUDGMENT = "trade_shape_rescue_failed_to_improve_anchor_profit_quality_preserved_no_selection"
DECISION = "stage343F_open_run343G_directional_long_supply_quality_surface_design"
CLAIM_BOUNDARY = (
    "research_development_review_only_trade_shape_rescue_quality_margin_blend_mt5_probe_"
    "no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run343F_trade_shape_rescue_quality_margin_blend_mt5_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage343F_trade_shape_rescue_quality_margin_blend_mt5_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run343E"
PARENT_FINAL = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATES = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_SUMMARY = PARENT_RUN_DIR / "trade_shape_rescue_quality_margin_blend_mt5_probe_summary.csv"
PARENT_DIFF = PARENT_RUN_DIR / "proxy_mt5_runtime_difference.csv"
PARENT_IDENTITY = PARENT_RUN_DIR / "runtime_identity.csv"
PARENT_LINEAGE = PARENT_RUN_DIR / "artifact_lineage_receipt.json"

SOURCE_PACKAGE_DIR = STAGE_DIR / "02_runs" / "run343D"
SOURCE_VARIANT_PREVIEW = SOURCE_PACKAGE_DIR / "variant_preview.csv"
SOURCE_PACKAGE_FINAL = SOURCE_PACKAGE_DIR / "final_decision.json"
REFERENCE_FINAL = STAGE_DIR / "02_runs" / "run343C" / "final_decision.json"

REVIEW_SCORECARD = RUN_DIR / "trade_shape_rescue_review_scorecard.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run343G_directional_long_supply_quality_surface_queue.csv"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
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


def fs_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(f"missing required review input: {rel(path)}")
    return path


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), encoding="utf-8-sig", low_memory=False).fillna("")


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: list[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def append_or_replace_csv(path: Path, key_fields: list[str], rows: list[Mapping[str, Any]], default_columns: list[str] | None = None) -> None:
    if path_is_file(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = list(default_columns or []), []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, kept + [dict(row) for row in rows], fieldnames)


def append_once(path: Path, marker: str, block: str) -> None:
    current = ""
    if path_is_file(path):
        with open(fs_path(path), encoding="utf-8-sig") as handle:
            current = handle.read()
    if marker in current:
        return
    sep = "" if not current or current.endswith("\n") else "\n"
    write_text(path, f"{current}{sep}{block}")


def as_float(value: Any) -> float:
    try:
        if value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def as_int(value: Any) -> int:
    try:
        if value == "":
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def round6(value: float) -> float:
    return round(float(value), 6)


def side_balance(long_count: int, short_count: int) -> float:
    if long_count <= 0 or short_count <= 0:
        return 0.0
    return min(long_count, short_count) / max(long_count, short_count)


def row_to_dict(row: pd.Series) -> dict[str, Any]:
    return {key: row.get(key, "") for key in row.index}


def numeric_summary() -> pd.DataFrame:
    summary = read_csv(required(PARENT_SUMMARY))
    for column in [
        "expected_rows",
        "matched_rows",
        "expected_missing_rows",
        "hash_mismatch_rows",
        "probability_mismatch_rows",
        "decision_mismatch_rows",
        "net_profit",
        "profit_factor",
        "trade_count",
        "expectancy",
        "recovery_factor",
        "max_drawdown_amount",
        "short_trade_count",
        "long_trade_count",
        "max_abs_probability_diff",
    ]:
        if column in summary.columns:
            summary[column] = pd.to_numeric(summary[column], errors="coerce").fillna(0.0)
    summary["side_balance"] = summary.apply(
        lambda row: side_balance(as_int(row["long_trade_count"]), as_int(row["short_trade_count"])),
        axis=1,
    )
    summary["profit_quality_rank"] = summary["net_profit"].rank(method="min", ascending=False).astype(int)
    summary["trade_shape_score"] = (
        summary["trade_count"].astype(float)
        + 10.0 * summary["side_balance"].astype(float)
        + 0.25 * summary["profit_factor"].astype(float)
        - 0.02 * summary["max_drawdown_amount"].astype(float)
    )
    summary["trade_shape_rank"] = summary["trade_shape_score"].rank(method="min", ascending=False).astype(int)
    return summary


def build_scorecard(summary: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    best = row_to_dict(summary.sort_values(["net_profit", "profit_factor", "expectancy"], ascending=False).iloc[0])
    shape = row_to_dict(summary.sort_values(["trade_shape_score", "trade_count", "side_balance"], ascending=False).iloc[0])
    anchor = summary.loc[summary["attempt_name"].astype(str).eq("d01_h04_anchor45")]
    anchor_row = row_to_dict(anchor.iloc[0]) if not anchor.empty else best
    control = summary.loc[summary["attempt_name"].astype(str).eq("d02_h02_shape_ctl")]
    control_row = row_to_dict(control.iloc[0]) if not control.empty else shape

    rows = []
    for _, row in summary.iterrows():
        rows.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "net_profit": as_float(row["net_profit"]),
                "profit_factor": as_float(row["profit_factor"]),
                "expectancy": as_float(row["expectancy"]),
                "recovery_factor": as_float(row["recovery_factor"]),
                "max_drawdown_amount": as_float(row["max_drawdown_amount"]),
                "trade_count": as_int(row["trade_count"]),
                "long_trade_count": as_int(row["long_trade_count"]),
                "short_trade_count": as_int(row["short_trade_count"]),
                "side_balance": round6(as_float(row["side_balance"])),
                "profit_quality_rank": as_int(row["profit_quality_rank"]),
                "trade_shape_rank": as_int(row["trade_shape_rank"]),
                "net_delta_vs_anchor": round6(as_float(row["net_profit"]) - as_float(anchor_row["net_profit"])),
                "pf_delta_vs_anchor": round6(as_float(row["profit_factor"]) - as_float(anchor_row["profit_factor"])),
                "trade_delta_vs_anchor": as_int(row["trade_count"]) - as_int(anchor_row["trade_count"]),
                "long_delta_vs_anchor": as_int(row["long_trade_count"]) - as_int(anchor_row["long_trade_count"]),
                "drawdown_delta_vs_anchor": round6(as_float(row["max_drawdown_amount"]) - as_float(anchor_row["max_drawdown_amount"])),
                "matched_rows": as_int(row["matched_rows"]),
                "expected_rows": as_int(row["expected_rows"]),
                "comparison_status": row.get("comparison_status", ""),
                "interpretation": interpret_attempt(str(row["attempt_name"]), row, anchor_row, control_row),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    scorecard = pd.DataFrame(rows)
    scorecard.to_csv(fs_path(REVIEW_SCORECARD), index=False, encoding="utf-8-sig", lineterminator="\n")
    return scorecard, {"best": best, "shape": shape, "anchor": anchor_row, "shape_control": control_row}


def interpret_attempt(attempt: str, row: pd.Series, anchor: Mapping[str, Any], shape_control: Mapping[str, Any]) -> str:
    if attempt in {"d01_h04_anchor45", "d04_q02_blk15", "d05_q02_blk30", "d10_q02_blk60"}:
        return "same_profit_anchor_surface(동일 수익 앵커 표면): minute block(분 단위 차단) 범위 변화가 MT5 KPI(MT5 핵심 성과 지표)를 바꾸지 않았다."
    if attempt in {"d06_q04_m015_blk15", "d07_q04_m015_blk30"}:
        return "near_anchor_small_long_rescue(앵커 근처 소폭 롱 복구): trade count(거래수)는 +1이나 net/PF(순수익/수익 팩터)는 소폭 하락했다."
    if attempt in {"d02_h02_shape_ctl", "d03_h03_shape_ctl"}:
        return "shape_control_not_profit_quality(거래 형태 대조지만 수익 품질 부족): long/short balance(롱/숏 균형)는 좋지만 profit quality(수익 품질)가 낮다."
    if attempt in {"d08_q10_s555_ctl", "d09_q10_s555_blk15"}:
        return "short_threshold_cost_stress_failed(숏 임계값 비용 압박 실패): drawdown(낙폭)과 PF(수익 팩터)가 악화했다."
    return "review_required(검토 필요)"


def build_attribution(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = review["best"]
    anchor = review["anchor"]
    shape = review["shape_control"]
    near = review["near_anchor"]
    q10 = review["q10_cost"]
    return [
        {
            "attribution_id": "profit_anchor_preserved",
            "observed_change": "best attempt(최고 시도)가 d01/d04/d05/d10 동일 수익 앵커로 수렴",
            "comparison_baseline": "run343C best h04_q02_l515_blk45 및 run343D anchor",
            "likely_drivers": "same q02 threshold/margin(동일 q02 임계값/마진)과 early long block(초반 롱 차단)",
            "trade_shape": f"trades={as_int(best['trade_count'])}; long_short={as_int(best['long_trade_count'])}/{as_int(best['short_trade_count'])}; side_balance={round6(as_float(best['side_balance']))}",
            "segment_checks": "runtime parity(런타임 동등성) 58270/58270, attempt-level KPI(시도별 KPI) 확인",
            "alternative_explanations": "side filter(사이드 필터) minute range(분 범위)가 실제 차단 행 분포를 더 세분하지 못했을 가능성",
            "attribution_confidence": "high(높음)",
            "next_probe": "minute block(분 차단) 반복 대신 directional long quality surface(방향성 롱 품질 표면) 설계",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "shape_control_profit_tax",
            "observed_change": f"shape control(거래 형태 대조)은 trades {as_int(shape['trade_count'])}, long/short {as_int(shape['long_trade_count'])}/{as_int(shape['short_trade_count'])}이나 net {as_float(shape['net_profit'])}, PF {as_float(shape['profit_factor'])}",
            "comparison_baseline": f"anchor net {as_float(anchor['net_profit'])}, PF {as_float(anchor['profit_factor'])}, trades {as_int(anchor['trade_count'])}",
            "likely_drivers": "long supply(롱 공급) 복구가 weak long(약한 롱)을 같이 되살려 payoff quality(손익 품질)를 낮춤",
            "trade_shape": f"net_delta={round6(as_float(shape['net_profit']) - as_float(anchor['net_profit']))}; pf_delta={round6(as_float(shape['profit_factor']) - as_float(anchor['profit_factor']))}; trade_delta={as_int(shape['trade_count']) - as_int(anchor['trade_count'])}",
            "segment_checks": "direction split(방향 분해)만 있음; session/regime(세션/국면)별 손익 분해는 다음 검토 필요",
            "alternative_explanations": "same ONNX(동일 온엑스) 확률 표면에서 threshold(임계값)만 바꾼 한계",
            "attribution_confidence": "medium(중간)",
            "next_probe": "long entries(롱 진입)를 별도 quality/regime feature(품질/국면 피처)로 재분리",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "near_anchor_not_enough",
            "observed_change": f"d06/d07은 net {as_float(near['net_profit'])}, PF {as_float(near['profit_factor'])}, trades {as_int(near['trade_count'])}",
            "comparison_baseline": "d01 profit anchor(수익 앵커)",
            "likely_drivers": "q04 margin(마진) 표면에서 약간의 long rescue(롱 복구)가 가능하지만 trade shape(거래 형태) 개선 폭이 작음",
            "trade_shape": f"trade_delta={as_int(near['trade_count']) - as_int(anchor['trade_count'])}; long_delta={as_int(near['long_trade_count']) - as_int(anchor['long_trade_count'])}; net_delta={round6(as_float(near['net_profit']) - as_float(anchor['net_profit']))}",
            "segment_checks": "attempt-level(시도 단위)만 확인; trade bucket(거래 묶음) 손익 분해는 다음 작업 필요",
            "alternative_explanations": "수익 차이 2.0은 비용/샘플 잡음일 수 있으나 balance(균형) 개선이 너무 작다",
            "attribution_confidence": "medium(중간)",
            "next_probe": "near-anchor clue(앵커 근처 단서)는 salvage seed(회수 씨앗)로 보존하되 selection(선정)하지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "q10_cost_stress_negative",
            "observed_change": f"q10 cost stress(비용 압박)는 net {as_float(q10['net_profit'])}, PF {as_float(q10['profit_factor'])}, drawdown {as_float(q10['max_drawdown_amount'])}",
            "comparison_baseline": "d01 profit anchor(수익 앵커)",
            "likely_drivers": "short threshold(숏 임계값) 상승이 profitable short supply(수익성 숏 공급)를 과도하게 줄임",
            "trade_shape": f"trades={as_int(q10['trade_count'])}; long_short={as_int(q10['long_trade_count'])}/{as_int(q10['short_trade_count'])}",
            "segment_checks": "cost stress(비용 압박) 변형 2개 확인",
            "alternative_explanations": "short concentration(숏 집중) 완화 자체는 필요하지만 threshold-only(임계값 단독) 접근이 약함",
            "attribution_confidence": "high(높음)",
            "next_probe": "short threshold-only(숏 임계값 단독) 미세조정 반복 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "failure_id": "minute_block_micro_tuning_dead_end",
            "hypothesis": "early long block(초반 롱 차단)을 0~15/30/45/60분으로 나누면 trade count(거래수)와 side balance(방향 균형)가 회복된다.",
            "variants_tried": "d01,d04,d05,d10",
            "failed_boundary": "same MT5 KPI(동일 MT5 핵심 성과 지표)로 수렴",
            "why_failed": "blocked long rows(차단 롱 행)가 같은 위치에 몰려 minute range(분 범위) 세분화가 실제 의사결정을 바꾸지 못했다.",
            "salvage_value": "profit anchor(수익 앵커)는 보존",
            "reopen_condition": "다른 feature(피처)나 regime(국면)으로 롱 허용을 나눌 때만 재개",
            "do_not_repeat": "minutes_from_cash_open(현금장 개장 후 분) 범위만 바꾸는 micro-tuning(미세조정)을 반복하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "shape_control_profit_quality_tax",
            "hypothesis": "h02/h03 shape control(거래 형태 대조)을 복구하면 운영 가능한 균형에 가까워진다.",
            "variants_tried": "d02,d03",
            "failed_boundary": "trade_count(거래수)와 long/short balance(롱/숏 균형)는 개선되지만 net/PF/expectancy(순수익/수익 팩터/기대값)가 낮다.",
            "why_failed": "weak long(약한 롱)까지 같이 복구되어 payoff quality(손익 품질)를 희석했다.",
            "salvage_value": "long supply(롱 공급) 후보와 side-balance(방향 균형) 후보",
            "reopen_condition": "long-only quality filter(롱 전용 품질 필터)나 별도 long surface(롱 표면)가 생길 때",
            "do_not_repeat": "h02/h03 no-filter(무필터)를 그대로 운영 후보처럼 보지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "short_threshold_cost_stress_negative",
            "hypothesis": "short threshold(숏 임계값)를 올리면 short concentration(숏 집중)이 줄고 비용 압박에 강해진다.",
            "variants_tried": "d08,d09",
            "failed_boundary": "net/PF/recovery(순수익/수익 팩터/회복 계수)가 악화",
            "why_failed": "profitable short supply(수익성 숏 공급)를 너무 많이 버렸다.",
            "salvage_value": "short concentration(숏 집중) 위험은 계속 감시",
            "reopen_condition": "threshold(임계값)가 아니라 volatility/regime(변동성/국면) 기반 short filter(숏 필터)를 쓸 때",
            "do_not_repeat": "q10_s555 threshold-only(임계값 단독) 접근 반복 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run343G_directional_long_supply_quality_surface_queue",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "seed": "directional_long_quality_surface(방향성 롱 품질 표면)",
            "source_attempts": "d01_h04_anchor45,d06_q04_m015_blk15,d02_h02_shape_ctl",
            "hypothesis": "profit anchor(수익 앵커)의 short supply(숏 공급)는 보존하고, long entries(롱 진입)는 separate quality/regime surface(별도 품질/국면 표면)로 다시 분리하면 trade shape(거래 형태)를 회복할 수 있다.",
            "required_controls": "d01 anchor unchanged(앵커 무변경), d02 shape control(거래 형태 대조), d06 near-anchor rescue(앵커 근처 복구)",
            "effect": "minute block(분 차단) 미세조정 대신 long quality source(롱 품질 원천)를 새로 찾는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run343G_directional_long_supply_quality_surface_queue",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "seed": "trade_bucket_payoff_attribution(거래 묶음 손익 귀속)",
            "source_attempts": "d01_h04_anchor45,d02_h02_shape_ctl,d06_q04_m015_blk15",
            "hypothesis": "shape control(거래 형태 대조)의 추가 11개 trade(거래) 중 손실 cluster(군집)를 찾으면 long rescue(롱 복구)의 제거 조건을 만들 수 있다.",
            "required_controls": "trade list(거래 목록), direction split(방향 분해), session bucket(세션 묶음), drawdown cluster(낙폭 군집)",
            "effect": "롱 복구가 왜 PF(수익 팩터)를 낮추는지 시장 현상 단위로 분해한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run343G_directional_long_supply_quality_surface_queue",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P2",
            "seed": "exit_lifecycle_shape_repair(청산 생명주기 거래 형태 수리)",
            "source_attempts": "d02_h02_shape_ctl,d06_q04_m015_blk15",
            "hypothesis": "entry(진입)를 더 깎기보다 hold/exit lifecycle(보유/청산 생명주기)을 조정하면 trade count(거래수)를 보존하면서 PF(수익 팩터)를 회복할 수 있다.",
            "required_controls": "same entry surface(동일 진입 표면), max hold/close-on-flat variants(최대 보유/관망 청산 변형), no-entry-change control(진입 무변경 대조)",
            "effect": "entry-only(진입 단독) 실패 기억을 exit-side(청산 측) 공격 탐색으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_review() -> dict[str, Any]:
    parent_final = read_json(required(PARENT_FINAL))
    reference_final = read_json(required(REFERENCE_FINAL))
    source_package_final = read_json(required(SOURCE_PACKAGE_FINAL))
    summary = numeric_summary()
    scorecard, selected = build_scorecard(summary)

    near = summary.loc[summary["attempt_name"].astype(str).isin(["d06_q04_m015_blk15", "d07_q04_m015_blk30"])]
    q10 = summary.loc[summary["attempt_name"].astype(str).isin(["d08_q10_s555_ctl", "d09_q10_s555_blk15"])]
    selected["near_anchor"] = row_to_dict(near.sort_values(["net_profit", "profit_factor"], ascending=False).iloc[0])
    selected["q10_cost"] = row_to_dict(q10.sort_values(["net_profit", "profit_factor"], ascending=False).iloc[0])
    selected["parent_final"] = parent_final
    selected["reference_final"] = reference_final
    selected["source_package_final"] = source_package_final
    selected["scorecard_rows"] = int(len(scorecard))
    selected["parity_all_exact"] = bool(
        int(parent_final.get("matched_rows", 0)) == int(parent_final.get("expected_rows", -1))
        and int(parent_final.get("mismatch_rows", -1)) == 0
        and int(parent_final.get("exact_parity_rows", 0)) == int(parent_final.get("attempt_rows", -1))
    )
    selected["trade_shape_recovered"] = False
    selected["profit_anchor_preserved"] = True
    selected["review_judgment_label"] = "negative(부정)_for_trade_shape_rescue_positive_clue_preserved(수익 단서 보존)"

    attribution = build_attribution(selected)
    failure = build_failure_memory(selected)
    next_queue = build_next_queue()
    write_csv(PERFORMANCE_ATTRIBUTION, attribution)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(NEXT_QUEUE, next_queue)
    selected["attribution_rows"] = len(attribution)
    selected["failure_rows"] = len(failure)
    selected["next_queue_rows"] = len(next_queue)
    return selected


def gate_row(gate: str, status: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def all_gates_pass(path: Path) -> bool:
    gates = read_csv(required(path))
    return bool(gates["status"].astype(str).str.lower().eq("passed").all())


def write_gates(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    parent = review["parent_final"]
    no_forbidden = (
        parent.get("candidate_selection") == "not_run"
        and parent.get("runtime_authority") == "not_claimed"
        and parent.get("operating_promotion") == "not_claimed"
        and parent.get("goal_achieve") == "not_claimed"
    )
    gates = [
        gate_row(
            "parent_343E_gates_passed",
            "passed" if all_gates_pass(PARENT_GATES) else "failed",
            PARENT_GATES,
            "run343E(343E 실행)의 MT5 runtime probe gate(런타임 탐침 게이트)를 이어받는다.",
        ),
        gate_row(
            "runtime_parity_verified",
            "passed" if review["parity_all_exact"] else "failed",
            PARENT_DIFF,
            "expected tape(예상 테이프)와 MT5 telemetry(MT5 기록)가 행 단위로 일치한다.",
        ),
        gate_row(
            "kpi_contract_audit_written",
            "passed" if path_is_file(REVIEW_SCORECARD) and review["scorecard_rows"] == int(parent.get("attempt_rows", -1)) else "failed",
            REVIEW_SCORECARD,
            "attempt-level KPI(시도 단위 핵심 성과 지표)를 같은 grain(입자)로 기록한다.",
        ),
        gate_row(
            "performance_attribution_written",
            "passed" if path_is_file(PERFORMANCE_ATTRIBUTION) and review["attribution_rows"] >= 4 else "failed",
            PERFORMANCE_ATTRIBUTION,
            "profit quality(수익 품질), trade shape(거래 형태), cost stress(비용 압박)의 성과 변화를 분해한다.",
        ),
        gate_row(
            "failure_memory_written",
            "passed" if path_is_file(FAILURE_MEMORY) and review["failure_rows"] >= 3 else "failed",
            FAILURE_MEMORY,
            "반복 금지와 회수 조건을 failure memory(실패 기억)로 남긴다.",
        ),
        gate_row(
            "next_offensive_queue_written",
            "passed" if path_is_file(NEXT_QUEUE) and review["next_queue_rows"] >= 3 else "failed",
            NEXT_QUEUE,
            "다음 offensive exploration seed(공격 탐색 씨앗)를 연다.",
        ),
        gate_row(
            "source_authority_audit",
            "passed" if path_is_file(PARENT_FINAL) and path_is_file(PARENT_SUMMARY) and path_is_file(PARENT_IDENTITY) else "failed",
            PARENT_IDENTITY,
            "KPI(핵심 성과 지표)와 tester identity(테스터 정체성)의 source authority(원천 권위)를 확인한다.",
        ),
        gate_row(
            "no_forbidden_operating_claim",
            "passed" if no_forbidden else "failed",
            PARENT_FINAL,
            "review(검토)를 selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)로 올리지 않는다.",
        ),
        gate_row(
            "required_gate_coverage_audit_written",
            "passed",
            GATE_AUDIT,
            "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다.",
        ),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def write_receipts(review: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run343E trade shape rescue quality margin blend MT5 probe(343E 거래 형태 복구 품질 마진 혼합 MT5 탐침)",
            "evidence_available": [rel(PARENT_FINAL), rel(PARENT_SUMMARY), rel(PARENT_GATES), rel(REVIEW_SCORECARD)],
            "evidence_missing": "forward/live/operating evidence(전진/실거래/운영 근거) 없음; Tier B(티어 B)는 missing_required(필수 누락)",
            "judgment_label": "runtime_probe_review(런타임 탐침 검토); trade_shape_rescue_negative(거래 형태 복구 부정); profit_anchor_preserved(수익 앵커 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run343G directional long quality surface(방향성 롱 품질 표면) 설계/패키지",
            "user_explanation_hook": "수익 앵커는 유지됐지만 거래 형태 복구는 실패했으니, 롱을 시간 차단이 아니라 별도 품질 표면으로 다시 찾아야 한다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "partial block(부분 차단)은 anchor(앵커)와 동일, shape control(거래 형태 대조)은 수익 품질 하락",
            "comparison_baseline": "d01_h04_anchor45 and run343C h04_q02_l515_blk45",
            "likely_drivers": "minute block(분 차단) feature(피처)의 낮은 분해능, weak long(약한 롱) 복구 비용, short threshold(숏 임계값) 과필터",
            "segment_checks": "attempt-level KPI(시도 단위 KPI), direction mix(방향 혼합), parity(동등성) 확인; session/regime bucket(세션/국면 묶음)은 다음 작업",
            "trade_shape": {
                "anchor": {
                    "trade_count": as_int(review["anchor"]["trade_count"]),
                    "long": as_int(review["anchor"]["long_trade_count"]),
                    "short": as_int(review["anchor"]["short_trade_count"]),
                    "side_balance": round6(as_float(review["anchor"]["side_balance"])),
                },
                "shape_control": {
                    "trade_count": as_int(review["shape_control"]["trade_count"]),
                    "long": as_int(review["shape_control"]["long_trade_count"]),
                    "short": as_int(review["shape_control"]["short_trade_count"]),
                    "side_balance": round6(as_float(review["shape_control"]["side_balance"])),
                },
            },
            "alternative_explanations": "single-window runtime scout(단일 구간 런타임 탐색)라 regime stability(국면 안정성)는 미검증",
            "attribution_confidence": "medium_high(중상)",
            "next_probe": rel(NEXT_QUEUE),
        },
    )
    artifact_paths = [
        REVIEW_SCORECARD,
        PERFORMANCE_ATTRIBUTION,
        FAILURE_MEMORY,
        NEXT_QUEUE,
        JUDGMENT_RECEIPT,
        PERFORMANCE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [
                rel(PARENT_FINAL),
                rel(PARENT_GATES),
                rel(PARENT_SUMMARY),
                rel(PARENT_DIFF),
                rel(PARENT_IDENTITY),
                rel(PARENT_LINEAGE),
                rel(SOURCE_VARIANT_PREVIEW),
                rel(SOURCE_PACKAGE_FINAL),
                rel(REFERENCE_FINAL),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths if path_is_file(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths if path_is_file(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적 또는 명령 재현 가능)",
            "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "allowed_claim": "reviewed runtime probe result only(검토된 런타임 탐침 결과만)",
        },
    )


def write_final(review: Mapping[str, Any], gates: list[Mapping[str, Any]]) -> dict[str, Any]:
    gate_passes = sum(1 for gate in gates if gate["status"] == "passed")
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "reference_review_run_id": REFERENCE_REVIEW_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": gate_passes,
        "gate_total": len(gates),
        "best_attempt": review["best"]["attempt_name"],
        "best_model_id": review["best"]["model_id"],
        "best_net_profit": as_float(review["best"]["net_profit"]),
        "best_profit_factor": as_float(review["best"]["profit_factor"]),
        "best_expectancy": as_float(review["best"]["expectancy"]),
        "best_drawdown": as_float(review["best"]["max_drawdown_amount"]),
        "best_recovery_factor": as_float(review["best"]["recovery_factor"]),
        "best_trade_count": as_int(review["best"]["trade_count"]),
        "best_long_trade_count": as_int(review["best"]["long_trade_count"]),
        "best_short_trade_count": as_int(review["best"]["short_trade_count"]),
        "best_side_balance": round6(as_float(review["best"]["side_balance"])),
        "shape_control_attempt": review["shape_control"]["attempt_name"],
        "shape_control_net_profit": as_float(review["shape_control"]["net_profit"]),
        "shape_control_profit_factor": as_float(review["shape_control"]["profit_factor"]),
        "shape_control_trade_count": as_int(review["shape_control"]["trade_count"]),
        "shape_control_long_trade_count": as_int(review["shape_control"]["long_trade_count"]),
        "shape_control_short_trade_count": as_int(review["shape_control"]["short_trade_count"]),
        "shape_control_side_balance": round6(as_float(review["shape_control"]["side_balance"])),
        "near_anchor_attempt": review["near_anchor"]["attempt_name"],
        "near_anchor_net_profit": as_float(review["near_anchor"]["net_profit"]),
        "near_anchor_profit_factor": as_float(review["near_anchor"]["profit_factor"]),
        "near_anchor_trade_count": as_int(review["near_anchor"]["trade_count"]),
        "trade_shape_recovered": False,
        "profit_anchor_preserved": True,
        "candidate_selection": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "command": f"python -B {rel(Path(__file__))}",
            "inputs": [
                rel(PARENT_FINAL),
                rel(PARENT_GATES),
                rel(PARENT_SUMMARY),
                rel(PARENT_DIFF),
                rel(PARENT_IDENTITY),
                rel(SOURCE_VARIANT_PREVIEW),
                rel(SOURCE_PACKAGE_FINAL),
                rel(REFERENCE_FINAL),
            ],
            "outputs": [
                rel(FINAL_DECISION),
                rel(REVIEW_SCORECARD),
                rel(PERFORMANCE_ATTRIBUTION),
                rel(FAILURE_MEMORY),
                rel(NEXT_QUEUE),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
            ],
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(review: Mapping[str, Any], final: Mapping[str, Any]) -> None:
    anchor = review["anchor"]
    shape = review["shape_control"]
    near = review["near_anchor"]
    report = f"""# run343F Trade Shape Rescue Review(343F 거래 형태 복구 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- judgment(판정): `{JUDGMENT}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_expectancy(최고 기대값): `{final['best_expectancy']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- best_long_short(최고 롱/숏): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`
- shape_control(거래 형태 대조): `{final['shape_control_attempt']}`, net(순수익) `{final['shape_control_net_profit']}`, PF(수익 팩터) `{final['shape_control_profit_factor']}`, trades(거래수) `{final['shape_control_trade_count']}`, long/short(롱/숏) `{final['shape_control_long_trade_count']}/{final['shape_control_short_trade_count']}`
- near_anchor(앵커 근처): `{final['near_anchor_attempt']}`, net(순수익) `{final['near_anchor_net_profit']}`, PF(수익 팩터) `{final['near_anchor_profit_factor']}`, trades(거래수) `{final['near_anchor_trade_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Judgment(판정)

run343E(343E 실행)는 valid runtime probe(유효 런타임 탐침)다. MT5 telemetry(MT5 런타임 기록)는 expected tape(예상 테이프)와 58,270/58,270 행 일치했고 mismatch(불일치)는 0이다.

profit anchor(수익 앵커)는 보존됐다. `d01_h04_anchor45`, `d04_q02_blk15`, `d05_q02_blk30`, `d10_q02_blk60`은 모두 net profit(순수익) 152.79, PF(수익 팩터) 3.55, trades(거래수) 22로 같은 표면에 수렴했다.

trade shape rescue(거래 형태 복구)는 실패했다. `d02_h02_shape_ctl`은 trades(거래수) 33과 long/short(롱/숏) 13/20을 만들었지만 net profit(순수익) 122.9, PF(수익 팩터) 1.89로 수익 품질을 크게 잃었다. `d06_q04_m015_blk15`는 trades(거래수)를 23으로 1개 늘렸지만 net profit(순수익)은 150.79, PF(수익 팩터)는 3.43으로 앵커를 넘지 못했다.

## Attribution(성과 귀속)

- minute block micro-tuning(분 차단 미세조정): 0~15/30/45/60분 변형이 같은 결과로 수렴했다. 효과는 이 feature(피처)의 range tuning(범위 조정)을 반복하지 않게 하는 것이다.
- shape control tax(거래 형태 대조 비용): 롱 공급은 늘었지만 weak long(약한 롱)까지 같이 복구되어 expectancy(기대값)와 PF(수익 팩터)가 낮아졌다.
- near-anchor clue(앵커 근처 단서): d06/d07은 수익을 거의 유지하며 long trade(롱 거래)를 1개 늘렸지만 운영 가능한 균형 회복은 아니다.
- q10 cost stress(비용 압박): short threshold(숏 임계값) 단독 상승은 net/PF/recovery(순수익/수익 팩터/회복 계수)를 악화했다.

## Next(다음)

run343G(343G 실행)는 directional long quality surface(방향성 롱 품질 표면)를 설계한다. Action(행동): 시간 구간 차단 대신 long-only quality/regime(롱 전용 품질/국면) 원천을 찾는다. Effect(효과): profit anchor(수익 앵커)의 short supply(숏 공급)를 보존하면서 trade shape(거래 형태)를 다시 공격적으로 복구한다.

## Boundary(경계)

No selection(선정 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    decision_doc = f"""# {TODAY} Stage343F Review Decision(343F 검토 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- evidence(근거): `{rel(REVIEW_SCORECARD)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`, `{rel(FAILURE_MEMORY)}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): run343E(343E 실행)의 trade shape rescue MT5 probe(거래 형태 복구 MT5 탐침)를 reviewed result(검토 결과)로 닫았다.
Effect(효과): 수익 앵커는 preserved clue(보존 단서)로 남기고, minute block micro-tuning(분 차단 미세조정)은 failure memory(실패 기억)로 닫아 다음 탐색이 같은 자리에서 맴돌지 않게 한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 343 Selection Status(343단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_profit_anchor(보존 수익 앵커): `{final['best_attempt']}`
- unresolved_failure(미해결 실패): `trade_shape_rescue_failed(거래 형태 복구 실패)`
- next_probe(다음 탐침): `directional_long_supply_quality_surface(방향성 롱 공급 품질 표면)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): run343F(343F 실행)는 review(검토)이고, 다음은 selection(선정)이 아니라 offensive exploration(공격 탐색)이다.
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

run343F(343F 실행)는 run343E(343E 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 검토했다. profit anchor(수익 앵커)는 유지됐지만 trade shape rescue(거래 형태 복구)는 실패했으므로 run343G(343G 실행)는 directional long quality surface(방향성 롱 품질 표면)를 설계한다.

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
    write_text(DECISION_DOC, decision_doc)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(WORKSPACE_STATE, workspace)
    marker = f"run343F {RUN_ID}"
    append_once(
        STAGE_BRIEF,
        marker,
        f"""## run343F Trade Shape Rescue Review(343F 거래 형태 복구 검토)

- run_id(실행 ID): `{RUN_ID}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 수익 앵커는 보존하고, 거래 형태 복구 실패를 다음 방향성 롱 품질 표면 설계의 제약으로 바꾼다.
""",
    )
    append_once(
        STAGE_README,
        marker,
        f"""## run343F Trade Shape Rescue Review(343F 거래 형태 복구 검토)

- run_id(실행 ID): `{RUN_ID}`
- scorecard(점수표): `{rel(REVIEW_SCORECARD)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): run343G(343G 실행)가 minute block(분 차단)이 아니라 directional long quality surface(방향성 롱 품질 표면)를 탐색한다.
""",
    )
    changelog = f"""## {TODAY} run343F Trade Shape Rescue Review(거래 형태 복구 검토)

- action(행동): run343E MT5 runtime probe(MT5 런타임 탐침)를 검토했다.
- effect(효과): best `{final['best_attempt']}` net `{final['best_net_profit']}`, PF `{final['best_profit_factor']}`, trades `{final['best_trade_count']}`를 preserved clue(보존 단서)로 남기고, trade shape rescue(거래 형태 복구)는 no selection(선정 없음)으로 닫았다.
- next(다음): `{NEXT_RUN_ID}`
- boundary(경계): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 주장하지 않는다.
"""
    append_once(ROOT_CHANGELOG, marker, changelog)
    append_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(review: Mapping[str, Any], final: Mapping[str, Any], gates: list[Mapping[str, Any]]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "lane": "runtime_probe_review(런타임 탐침 검토)",
        "family": "kpi_evidence(KPI/장부/근거)",
        "run_number": RUN_NUMBER,
        "attempt_count": review["parent_final"]["attempt_rows"],
        "matched_rows": review["parent_final"]["matched_rows"],
    }
    rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "mt5_runtime_probe_review",
            "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
            "primary_kpi": f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": f"drawdown={final['best_drawdown']};long_short={final['best_long_trade_count']}/{final['best_short_trade_count']}",
            "external_verification_status": "completed(완료)",
            "notes": "Trade shape rescue(거래 형태 복구)는 실패, profit anchor(수익 앵커)는 보존.",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe_review",
            "candidate_model_id": final["best_attempt"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_drawdown"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "profit_anchor_preserved_trade_shape_rescue_failed_no_selection(수익 앵커 보존, 거래 형태 복구 실패, 선정 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "notes": "Tier B(티어 B)는 이 MT5 probe(MT5 탐침)의 범위 밖이다.",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "candidate_model_id": "missing_required",
            "result_status": "missing_required(필수 누락)",
            "attempt_count": "",
            "matched_rows": "",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
            "primary_kpi": f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": f"drawdown={final['best_drawdown']};long_short={final['best_long_trade_count']}/{final['best_short_trade_count']}",
            "external_verification_status": "completed(완료)",
            "notes": "Tier B(티어 B)가 없어 combined(합산)는 Tier A(티어 A) 경계와 같다.",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "candidate_model_id": final["best_attempt"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_drawdown"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    stage_rows = [{key: row.get(key, "") for key in STAGE_LEDGER_COLUMNS} for row in rows]
    append_or_replace_csv(STAGE_LEDGER, ["stage_id", "run_id", "view"], stage_rows, STAGE_LEDGER_COLUMNS)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "notes": "run343F reviewed run343E MT5 KPI and opened directional long quality surface(343F는 343E MT5 KPI를 검토하고 방향성 롱 품질 표면을 열었다).",
                "candidate_model_id": final["best_attempt"],
                "net_profit": final["best_net_profit"],
                "profit_factor": final["best_profit_factor"],
                "expectancy": final["best_expectancy"],
                "drawdown": final["best_drawdown"],
                "recovery_factor": final["best_recovery_factor"],
                "trade_count": final["best_trade_count"],
                "result_status": "reviewed_no_selection(검토됨, 선정 없음)",
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "mt5_runtime_probe_review",
            }
        ],
    )


def write_artifact_registry() -> None:
    rows = []
    for artifact_type, path, notes in [
        ("final_decision", FINAL_DECISION, "run343F review final decision(343F 검토 최종 결정)"),
        ("review_scorecard", REVIEW_SCORECARD, "run343F KPI scorecard(343F KPI 점수표)"),
        ("performance_attribution", PERFORMANCE_ATTRIBUTION, "run343F performance attribution(343F 성과 귀속)"),
        ("failure_memory", FAILURE_MEMORY, "run343F failure memory(343F 실패 기억)"),
        ("next_queue", NEXT_QUEUE, "run343G next offensive queue(343G 다음 공격 대기열)"),
        ("judgment_receipt", JUDGMENT_RECEIPT, "run343F judgment receipt(343F 판정 영수증)"),
        ("performance_receipt", PERFORMANCE_RECEIPT, "run343F performance receipt(343F 성과 영수증)"),
        ("lineage_receipt", LINEAGE_RECEIPT, "run343F lineage receipt(343F 계보 영수증)"),
        ("claim_receipt", CLAIM_RECEIPT, "run343F claim boundary receipt(343F 주장 경계 영수증)"),
        ("required_gate_coverage_audit", GATE_AUDIT, "run343F required gate audit(343F 필수 게이트 감사)"),
        ("report", REPORT_PATH, "run343F review report(343F 검토 보고서)"),
        ("decision_doc", DECISION_DOC, "run343F durable decision(343F 결정 문서)"),
        ("run_manifest", RUN_MANIFEST, "run343F run manifest(343F 실행 목록)"),
        ("pipeline", Path(__file__), "run343F producer script(343F 생산 스크립트)"),
    ]:
        if not path_is_file(path):
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
                "created_at_utc": now_utc(),
                "notes": notes,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows)


def main() -> None:
    for path in [
        PARENT_FINAL,
        PARENT_GATES,
        PARENT_SUMMARY,
        PARENT_DIFF,
        PARENT_IDENTITY,
        PARENT_LINEAGE,
        SOURCE_VARIANT_PREVIEW,
        SOURCE_PACKAGE_FINAL,
        REFERENCE_FINAL,
    ]:
        required(path)
    os.makedirs(fs_path(RUN_DIR), exist_ok=True)
    review = build_review()
    gates = write_gates(review)
    final = write_final(review, gates)
    write_docs(review, final)
    write_receipts(review)
    write_registers(review, final, gates)
    write_artifact_registry()
    write_receipts(review)
    gates = write_gates(review)
    final = write_final(review, gates)
    write_artifact_registry()
    if any(gate["status"] != "passed" for gate in gates):
        failed = [gate["gate_id"] for gate in gates if gate["status"] != "passed"]
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise SystemExit(f"failed gates: {failed}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_trade_count": final["best_trade_count"],
                "best_long_short": f"{final['best_long_trade_count']}/{final['best_short_trade_count']}",
                "trade_shape_recovered": final["trade_shape_recovered"],
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
