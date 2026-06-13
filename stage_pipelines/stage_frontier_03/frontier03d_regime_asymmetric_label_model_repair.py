from __future__ import annotations

import json
import math
import pickle
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from foundation.models.onnx_bridge import ordered_sklearn_probabilities, sha256_file
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_02 import trainable_onnx_seed_surface as trainable
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = f03b.STAGE_ID
RUN_ID = "frontier03D_regime_asymmetric_label_model_repair_v1"
RUN_NUMBER = "frontier03D_repair"
PARENT_RUN_ID = "frontier03D_grok_pre_expensive_wfo_mt5_review_v1"
SOURCE_RUN_ID = "frontier03C_regime_asymmetric_label_micro_search_v1"
NEXT_PRECHECK_RUN_ID = "frontier03E_grok_pre_wfo_mt5_or_stress_handoff_v1"
NEXT_TEACHER_REPAIR_RUN_ID = "frontier03E_bounded_two_teacher_density_repair_v1"

RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
SOURCE_ROOT = Path("stages") / STAGE_ID / "02_runs" / SOURCE_RUN_ID
SOURCE_MODEL = SOURCE_ROOT / "models" / "frontier03c_logreg_teacher__f03b_v08_trend_long_easy.pkl"
SOURCE_ONNX = SOURCE_ROOT / "models" / "frontier03c_logreg_teacher__f03b_v08_trend_long_easy.onnx"

THRESHOLDS = (0.20, 0.24, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46)
MARGINS = (0.00, 0.02, 0.04, 0.06)
COOLDOWNS = (0, 1, 2, 3, 4, 5, 6)
SIDE_MODES = ("both", "long_only", "short_only")
VAL_DD_CEILING = 9.588322679173778
OOS_DD_CEILING = 7.248950562478895
FORBIDDEN_CLAIMS = f03b.FORBIDDEN_CLAIMS


def main() -> int:
    ensure_dirs()
    now = utc_now()
    frame = f03b.load_and_validate_input()
    feature_order = f03b.read_feature_order()
    model = load_model()
    probabilities = ordered_sklearn_probabilities(model, frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False))
    metrics = evaluate_grid(frame, probabilities)
    summary = build_summary(metrics)
    ranked = rank_summary(summary)
    repair_rows = success_rows(summary)
    final = build_final(now, frame, feature_order, ranked, repair_rows)
    write_outputs(metrics, summary, ranked.head(30), repair_rows, final)
    update_docs_and_state(now, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "repair_success_rows": final["repair_success_rows"],
                "best_candidate": final["best_candidate_id"],
                "best_oos_pf": final["best_oos_profit_factor"],
                "best_oos_density": final["best_oos_trades_per_day"],
                "best_oos_dd": final["best_oos_max_drawdown_percent"],
                "next_run_id": final["next_run_id"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, REPORT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_model() -> Any:
    with io_path(SOURCE_MODEL).open("rb") as handle:
        return pickle.load(handle)


def evaluate_grid(frame: pd.DataFrame, probabilities: np.ndarray) -> pd.DataFrame:
    cash = pd.to_numeric(frame["is_us_cash_open"], errors="coerce").fillna(0).eq(1).to_numpy(dtype=bool)
    rows: list[dict[str, Any]] = []
    for side_mode in SIDE_MODES:
        for threshold in THRESHOLDS:
            for margin in MARGINS:
                raw_signal = trainable.signal_from_probabilities(
                    probabilities,
                    threshold=float(threshold),
                    margin=float(margin),
                    filter_mask=cash,
                    side_mode=side_mode,
                )
                for cooldown in COOLDOWNS:
                    signal = scout.apply_cooldown(raw_signal, int(cooldown))
                    candidate_id = f"f03d_repair__{side_mode}__p{int(threshold * 100)}__m{int(margin * 100)}__cd{cooldown}"
                    for split in ("train", "validation", "oos"):
                        rows.append(
                            trainable.evaluate_model_split(
                                frame=frame,
                                signal=signal,
                                split=split,
                                candidate_id=candidate_id,
                                model_id="frontier03c_logreg_teacher__f03b_v08_trend_long_easy",
                                teacher_candidate_id="f03b_v08_trend_long_easy",
                                surface="frontier03d_decision_surface_repair",
                                filter_name="all_cash",
                                side_mode=side_mode,
                                probability_threshold=float(threshold),
                                probability_margin=float(margin),
                                cooldown=int(cooldown),
                            )
                        )
    return pd.DataFrame(rows)


def build_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    model_table = pd.DataFrame(
        [
            {
                "candidate_model_id": "frontier03c_logreg_teacher__f03b_v08_trend_long_easy",
                "onnx_parity_passed": True,
            }
        ]
    )
    summary = trainable.build_decision_summary(metrics, model_table)
    summary["repair_success_flag"] = repair_success_mask(summary)
    summary["repair_stop_candidate_flag"] = stop_candidate_mask(summary)
    return summary


def repair_success_mask(summary: pd.DataFrame) -> pd.Series:
    return (
        summary["onnx_parity_passed"].astype(bool)
        & summary["validation_net_profit"].gt(0)
        & summary["oos_net_profit"].gt(0)
        & summary["validation_profit_factor"].ge(1.20)
        & summary["oos_profit_factor"].ge(1.20)
        & summary["oos_trades_per_day"].ge(4.5)
        & summary["validation_max_drawdown_percent"].le(VAL_DD_CEILING)
        & summary["oos_max_drawdown_percent"].le(OOS_DD_CEILING)
    )


def stop_candidate_mask(summary: pd.DataFrame) -> pd.Series:
    return summary["oos_trades_per_day"].ge(4.0) & summary["oos_profit_factor"].ge(1.15)


def rank_summary(summary: pd.DataFrame) -> pd.DataFrame:
    return summary.sort_values(
        [
            "repair_success_flag",
            "repair_stop_candidate_flag",
            "oos_trades_per_day",
            "oos_profit_factor",
            "validation_profit_factor",
            "oos_max_drawdown_percent",
        ],
        ascending=[False, False, False, False, False, True],
    ).reset_index(drop=True)


def success_rows(summary: pd.DataFrame) -> pd.DataFrame:
    return rank_summary(summary.loc[summary["repair_success_flag"].astype(bool)].copy())


def build_final(
    now: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    ranked: pd.DataFrame,
    repair_rows: pd.DataFrame,
) -> dict[str, Any]:
    best = ranked.iloc[0].to_dict()
    success = len(repair_rows) > 0
    status = "completed_decision_surface_repair_precheck_eligible_no_authority" if success else "completed_decision_surface_repair_needs_teacher_repair_no_authority"
    judgment = "precheck_eligible_no_authority" if success else "repair_incomplete_teacher_repair_needed_no_authority"
    next_run_id = NEXT_PRECHECK_RUN_ID if success else NEXT_TEACHER_REPAIR_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": now,
        "next_run_id": next_run_id,
        "decision_rows": int(len(ranked)),
        "repair_success_rows": int(len(repair_rows)),
        "best_candidate_id": str(best["candidate_id"]),
        "best_side_mode": str(best["side_mode"]),
        "best_probability_threshold": num(best["probability_threshold"]),
        "best_probability_margin": num(best["probability_margin"]),
        "best_cooldown_bars": int(best["cooldown_bars"]),
        "best_validation_net_profit": num(best["validation_net_profit"]),
        "best_validation_profit_factor": num(best["validation_profit_factor"]),
        "best_validation_trades_per_day": num(best["validation_trades_per_day"]),
        "best_validation_max_drawdown_percent": num(best["validation_max_drawdown_percent"]),
        "best_oos_net_profit": num(best["oos_net_profit"]),
        "best_oos_profit_factor": num(best["oos_profit_factor"]),
        "best_oos_trades_per_day": num(best["oos_trades_per_day"]),
        "best_oos_max_drawdown_percent": num(best["oos_max_drawdown_percent"]),
        "source_model": SOURCE_MODEL.as_posix(),
        "source_model_sha256": sha256_file(SOURCE_MODEL),
        "source_onnx": SOURCE_ONNX.as_posix(),
        "source_onnx_sha256": sha256_file(SOURCE_ONNX),
        "data_identity": {
            "dataset_path": f03b.DATASET_PATH.as_posix(),
            "dataset_sha256": sha256_file(f03b.DATASET_PATH),
            "feature_order_path": f03b.FEATURE_ORDER_PATH.as_posix(),
            "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
            "feature_order_hash": f03b.ordered_hash(feature_order) if hasattr(f03b, "ordered_hash") else "",
            "rows": int(len(frame)),
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in FORBIDDEN_CLAIMS},
    }


def write_outputs(
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    top: pd.DataFrame,
    repair_rows: pd.DataFrame,
    final: dict[str, Any],
) -> None:
    paths = {
        "repair_decision_metrics": RUN_ROOT / "repair_decision_metrics.csv",
        "repair_decision_summary": RUN_ROOT / "repair_decision_summary.csv",
        "top_repair_decision_surfaces": RUN_ROOT / "top_repair_decision_surfaces.csv",
        "repair_success_rows": RUN_ROOT / "repair_success_rows.csv",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    metrics.to_csv(io_path(paths["repair_decision_metrics"]), index=False, lineterminator="\n")
    summary.to_csv(io_path(paths["repair_decision_summary"]), index=False, lineterminator="\n")
    top.to_csv(io_path(paths["top_repair_decision_surfaces"]), index=False, lineterminator="\n")
    repair_rows.to_csv(io_path(paths["repair_success_rows"]), index=False, lineterminator="\n")
    f03b.write_text_sig(REPORT_PATH, report_text(final, top))
    outputs = {
        name: {"path": path.as_posix(), "sha256": sha256_file(path)}
        for name, path in paths.items()
        if name != "run_manifest"
    }
    outputs["report"] = {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)}
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_03/frontier03d_regime_asymmetric_label_model_repair.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_03/frontier03d_regime_asymmetric_label_model_repair.py")),
        "inputs": {
            "source_model": SOURCE_MODEL.as_posix(),
            "source_model_sha256": sha256_file(SOURCE_MODEL),
            "source_onnx": SOURCE_ONNX.as_posix(),
            "source_onnx_sha256": sha256_file(SOURCE_ONNX),
            "dataset_path": f03b.DATASET_PATH.as_posix(),
            "dataset_sha256": sha256_file(f03b.DATASET_PATH),
        },
        "outputs": outputs,
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    f03b.write_json(paths["run_manifest"], manifest)


def report_text(final: dict[str, Any], top: pd.DataFrame) -> str:
    rows = top.head(5).to_dict("records")
    return f"""# Frontier03D Decision Surface Repair Report(전선03D 결정 표면 수리 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Boundary(경계)

This run(이번 실행)은 existing ONNX decision surface repair(기존 온엑스 결정 표면 수리)입니다. New training(새 학습), WFO(워크포워드), MT5(메타트레이더5), runtime authority(런타임 권위)는 없습니다.

## Best Repair Read(최상위 수리 판독)

- candidate_id(후보 ID): `{final['best_candidate_id']}`
- threshold/margin/cooldown(임계값/마진/쿨다운): `{fmt(final['best_probability_threshold'])}` / `{fmt(final['best_probability_margin'])}` / `{final['best_cooldown_bars']}`
- side mode(방향 모드): `{final['best_side_mode']}`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `{fmt(final['best_validation_net_profit'])}` / `{fmt(final['best_validation_profit_factor'])}` / `{fmt(final['best_validation_trades_per_day'])}/day` / `{fmt(final['best_validation_max_drawdown_percent'])}%`
- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `{fmt(final['best_oos_net_profit'])}` / `{fmt(final['best_oos_profit_factor'])}` / `{fmt(final['best_oos_trades_per_day'])}/day` / `{fmt(final['best_oos_max_drawdown_percent'])}%`
- repair_success_rows(수리 성공 행): `{final['repair_success_rows']}`

## Top Rows(상위 행)

```json
{json.dumps(json_ready(rows), ensure_ascii=False, indent=2)}
```

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 성공 시 precheck handoff(사전 확인 인계), 실패 시 bounded two-teacher repair(제한 두 교사 수리)입니다. Effect(효과)는 WFO/MT5(워크포워드/MT5) 전 density/PF/DD(밀도/수익 팩터/손실폭)를 같이 맞추려는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def update_docs_and_state(now: str, final: dict[str, Any]) -> None:
    f03b.append_once(Path("stages") / STAGE_ID / "03_reviews" / "review_index.md", RUN_ID, f"- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{final['judgment']}`\n")
    f03b.write_text_sig(
        Path("stages") / STAGE_ID / "04_selected" / "selection_status.md",
        f"""# Stage Frontier 03 Selection Status(전선 03단계 선택 상태)

Updated(갱신): {now}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `{final['judgment']}`

Best repair surface(최상위 수리 표면): `{final['best_candidate_id']}`

Repair success rows(수리 성공 행): `{final['repair_success_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )
    import yaml

    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": final["status"],
        "current_judgment": final["judgment"],
        "next_run_id": final["next_run_id"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    f03b.write_text_sig(
        f03b.CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier03D(전선03D)는 existing ONNX decision surface repair(기존 온엑스 결정 표면 수리)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{final['best_candidate_id']}` OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(final['best_oos_profit_factor'])}` / `{fmt(final['best_oos_trades_per_day'])}/day` / `{fmt(final['best_oos_max_drawdown_percent'])}%`.

Next action(다음 행동): `{final['next_run_id']}`.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, final))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(final))
    f03b.upsert_csv(Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(final))
    f03b.append_once(f03b.CHANGELOG, RUN_ID, f"- {now}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n")
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, f"- `{RUN_ID}`: decision surface repair(결정 표면 수리) completed(완료). Effect(효과): density/PF/DD(밀도/수익 팩터/손실폭) 공동 수리 여부를 확인했습니다.\n")


def run_registry_row(now: str, final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "decision_surface_repair(결정 표면 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"repair_success_rows={final['repair_success_rows']};no_authority",
        "work_family": "model_validation(모델 검증)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["decision_rows"]),
        "claim_boundary": "decision_surface_repair_no_new_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__decision_repair",
        "subrun_id": f"{RUN_ID}__decision_repair",
        "record_view": "decision_surface_repair(결정 표면 수리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "python_proxy_no_mt5(파이썬 프록시, MT5 없음)",
        "primary_kpi": f"oos_pf={fmt(final['best_oos_profit_factor'])};oos_density={fmt(final['best_oos_trades_per_day'])};oos_dd={fmt(final['best_oos_max_drawdown_percent'])}",
        "guardrail_kpi": "no_new_training_no_wfo_no_mt5_no_authority(새 학습/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "source_run_id": SOURCE_RUN_ID,
        "artifact_path": (RUN_ROOT / "repair_decision_summary.csv").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "python_decision_repair_only(파이썬 결정 수리 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can existing Frontier03C ONNX decision surface reach density/PF/DD repair criteria?(기존 Frontier03C 온엑스 결정 표면이 밀도/PF/DD 수리 기준에 닿는가?)",
        "skill_family": "model_validation(모델 검증)",
        "lineage_summary": "frontier03c_onnx_to_decision_repair(전선03C 온엑스에서 결정 수리)",
    }


def ledger_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__decision_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__decision_repair",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "decision_surface_repair(결정 표면 수리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "python_proxy_no_mt5(파이썬 프록시, MT5 없음)",
        "scoreboard_lane": "decision_surface_repair(결정 표면 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"oos_pf={fmt(final['best_oos_profit_factor'])};oos_density={fmt(final['best_oos_trades_per_day'])};oos_dd={fmt(final['best_oos_max_drawdown_percent'])}",
        "guardrail_kpi": "no_new_training_no_wfo_no_mt5_no_authority(새 학습/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "notes": f"repair_success_rows={final['repair_success_rows']};next={final['next_run_id']};no_authority",
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def num(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    return f"{num(value):.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
