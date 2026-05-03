from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, upsert_csv_rows
from foundation.models.xgboost_boosting import XgbVariantSpec

from . import xgboost_characteristic_mt5_probe as base


RUN_ID = "run11F_xgb_dart_booster_probe_v1"
RUN_NUMBER = "run11F"
PACKET_ID = "stage17_run11F_xgb_dart_booster_probe_v1"
CLOSEOUT_PACKET_ID = "stage17_model_family_challenge_closeout_v3"
THRESHOLD_QUANTILE = 0.80
BOUNDARY = "xgboost_dart_booster_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_xgboost_dart_booster_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_xgboost_dart_booster_runtime_probe_after_attempt"
JUDGMENT_CLOSED = "closed_inconclusive_xgboost_dart_no_new_internal_booster_characteristic"
RUN11B_AVG_ROUTED_TRADES = 229.5
RUN11D_VALIDATION_LONG_SHARE = 0.8439334637964775
RUN11D_OOS_LONG_SHARE = 0.7446254071661238


def configure_base() -> None:
    root = base.ROOT
    stage_root = root / "stages" / base.STAGE_ID
    base.RUN_ID = RUN_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.PACKET_ID = PACKET_ID
    base.EXPLORATION_LABEL = "stage17_Model__XGBoostDARTBooster"
    base.BOUNDARY = BOUNDARY
    base.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    base.JUDGMENT_BLOCKED = JUDGMENT_BLOCKED
    base.THRESHOLD_QUANTILE = THRESHOLD_QUANTILE
    base.ONNX_PARITY_TOLERANCE = 0.05
    base.RUN_ROOT = stage_root / "02_runs" / RUN_ID
    base.PACKET_ROOT = root / "docs/agent_control/packets" / PACKET_ID
    base.REVIEW_PACKET_PATH = stage_root / "03_reviews/run11F_xgb_dart_booster_probe_packet.md"
    base.DECISION_PATH = root / "docs/decisions/2026-05-03_stage17_xgboost_dart_booster_probe.md"
    base.default_stage17_xgb_variants = dart_variants  # type: ignore[assignment]
    base.build_summary = build_summary  # type: ignore[assignment]
    base.upsert_run_registry = upsert_run_registry  # type: ignore[assignment]


def dart_variants() -> list[XgbVariantSpec]:
    return [
        XgbVariantSpec(
            variant_id="dart_v01_depth3_lowdrop",
            idea_id="dart_lowdrop_regularized_boosting",
            description="DART booster with shallow depth, low dropout, and conservative regularization.",
            n_estimators=80,
            max_depth=3,
            learning_rate=0.040,
            min_child_weight=3.0,
            subsample=0.75,
            colsample_bytree=0.75,
            reg_alpha=0.10,
            reg_lambda=8.0,
            gamma=0.02,
            booster="dart",
            rate_drop=0.05,
            skip_drop=0.60,
            sample_type="uniform",
            normalize_type="tree",
            random_state=1911,
        ),
        XgbVariantSpec(
            variant_id="dart_v02_depth4_middrop",
            idea_id="dart_depth4_mid_dropout",
            description="DART booster with depth four trees and mid dropout pressure.",
            n_estimators=95,
            max_depth=4,
            learning_rate=0.030,
            min_child_weight=3.0,
            subsample=0.72,
            colsample_bytree=0.72,
            reg_alpha=0.15,
            reg_lambda=9.0,
            gamma=0.03,
            booster="dart",
            rate_drop=0.10,
            skip_drop=0.35,
            sample_type="uniform",
            normalize_type="tree",
            random_state=1912,
        ),
        XgbVariantSpec(
            variant_id="dart_v03_depth2_onedrop",
            idea_id="dart_one_drop_shallow",
            description="DART booster with one-drop enabled and shallower trees.",
            n_estimators=110,
            max_depth=2,
            learning_rate=0.035,
            min_child_weight=4.0,
            subsample=0.80,
            colsample_bytree=0.70,
            reg_alpha=0.20,
            reg_lambda=7.0,
            gamma=0.04,
            booster="dart",
            rate_drop=0.08,
            skip_drop=0.40,
            sample_type="uniform",
            normalize_type="forest",
            one_drop=1,
            random_state=1913,
        ),
    ]


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def replace_block(text: str, marker: str, block: str) -> str:
    pattern = rf"{re.escape(marker)}\n(?:  .*\n)+"
    if re.search(pattern, text):
        return re.sub(pattern, block, text, count=1)
    return text.rstrip() + "\n" + block


def selected_metric(selected: Mapping[str, Any], split: str, key: str) -> float:
    return safe_float(selected.get("metrics", {}).get(split, {}).get(key))


def selected_long_share(selected: Mapping[str, Any], split: str) -> float:
    signals = selected_metric(selected, split, "signal_count")
    return safe_div(selected_metric(selected, split, "long_count"), signals)


def selected_top_features(selected: Mapping[str, Any], count: int) -> list[str]:
    features = selected.get("feature_importance", {}).get("top_features", [])
    return [str(row.get("feature")) for row in features[:count] if isinstance(row, Mapping)]


def prior_gbtree_q80_score() -> float:
    path = base.STAGE_ROOT / "02_runs/run11C_xgb_q80_direction_asymmetry_probe_v1/summary.json"
    return safe_float(read_json(path).get("selected_variant", {}).get("characteristic_score"))


def prior_feature_top3() -> list[str]:
    path = base.STAGE_ROOT / "02_runs/run11E_xgb_feature_driver_saturation_v1/summary.json"
    rows = read_json(path).get("feature_driver_rows", [])
    if rows and isinstance(rows[0], Mapping):
        return [str(item) for item in rows[0].get("top3_features", [])]
    return []


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    parity = model_artifacts.get("onnx_parity", {})
    return bool(parity.get("tier_a", {}).get("passed")) and bool(parity.get("tier_b", {}).get("passed"))


def dart_read(summary: Mapping[str, Any]) -> dict[str, Any]:
    selected = summary.get("selected_variant", {})
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    completed = summary.get("external_verification_status") == "completed"
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    val_trades = safe_float(validation.get("trade_count"))
    oos_trades = safe_float(oos.get("trade_count"))
    avg_trades = (val_trades + oos_trades) / 2.0 if val_trades or oos_trades else 0.0
    trade_ratio = safe_div(avg_trades, RUN11B_AVG_ROUTED_TRADES)
    val_long_share = selected_long_share(selected, "validation")
    oos_long_share = selected_long_share(selected, "oos")
    score = safe_float(selected.get("characteristic_score"))
    score_delta = abs(score - prior_gbtree_q80_score())
    top3 = selected_top_features(selected, 3)
    prior_top3 = prior_feature_top3()
    top3_changed = bool(top3 and prior_top3 and top3 != prior_top3)
    trade_frequency_changed = bool(avg_trades and (trade_ratio <= 0.75 or trade_ratio >= 1.25))
    direction_skew_changed = abs(val_long_share - RUN11D_VALIDATION_LONG_SHARE) >= 0.15 or abs(oos_long_share - RUN11D_OOS_LONG_SHARE) >= 0.15
    score_changed = score_delta >= 0.10
    new_characteristic = completed and parity_ok and (top3_changed or trade_frequency_changed or direction_skew_changed or score_changed)
    if not completed or not parity_ok:
        recommendation = "blocked_before_stage18_until_dart_runtime_parity_is_resolved"
        closure_judgment = JUDGMENT_BLOCKED
        strength = "dart_runtime_parity_blocked"
    elif new_characteristic:
        recommendation = "keep_stage17_open_for_dart_followup_attribution"
        closure_judgment = JUDGMENT_COMPLETED
        strength = "dart_internal_booster_characteristic_visible"
    else:
        recommendation = "close_stage17_after_dart_no_new_internal_booster_characteristic"
        closure_judgment = JUDGMENT_CLOSED
        strength = "no_new_dart_internal_booster_characteristic"
    return {
        "characteristic_score": score,
        "model_characteristic_strength": strength,
        "stage17_stop_recommendation": recommendation,
        "closure_judgment": closure_judgment,
        "dart_booster_read": {
            "threshold_quantile": THRESHOLD_QUANTILE,
            "selected_variant_id": selected.get("variant_id"),
            "onnx_parity_passed": parity_ok,
            "avg_routed_trades": avg_trades,
            "run11b_avg_routed_trades": RUN11B_AVG_ROUTED_TRADES,
            "trade_ratio_vs_run11B": trade_ratio,
            "validation_long_signal_share": val_long_share,
            "oos_long_signal_share": oos_long_share,
            "run11d_validation_long_signal_share": RUN11D_VALIDATION_LONG_SHARE,
            "run11d_oos_long_signal_share": RUN11D_OOS_LONG_SHARE,
            "score_delta_vs_gbtree_q80": score_delta,
            "top3_features": top3,
            "prior_gbtree_top3_features": prior_top3,
            "top3_changed": top3_changed,
            "trade_frequency_changed": trade_frequency_changed,
            "direction_skew_changed": direction_skew_changed,
            "score_changed": score_changed,
            "new_characteristic_visible": new_characteristic,
        },
    }


def build_summary(
    result: Mapping[str, Any],
    selected: Mapping[str, Any],
    variant_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    validation = base.routed_metrics(result, "mt5_routed_total_validation_is")
    oos = base.routed_metrics(result, "mt5_routed_total_oos")
    summary = {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": base.STAGE_ID,
        "model_family": "xgboost_xgbclassifier_multiclass_dart",
        "boundary": BOUNDARY,
        "judgment": result["judgment"],
        "external_verification_status": result["external_verification_status"],
        "selected_variant": selected,
        "variant_artifacts": variant_artifacts,
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "python_tier_records": list(tier_records),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "attempt_count": len(result.get("attempts", [])),
        "validation_routed": validation,
        "oos_routed": oos,
    }
    summary.update(dart_read(summary))
    return summary


def upsert_run_registry(result: Mapping[str, Any], read: Mapping[str, Any]) -> dict[str, Any]:
    dart = read.get("dart_booster_read", {})
    row = {
        "run_id": RUN_ID,
        "stage_id": base.STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": read["closure_judgment"],
        "path": base.rel(base.RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("model_family", "xgboost_dart"),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("selected_variant", result.get("selected_variant_id")),
                ("threshold_quantile", THRESHOLD_QUANTILE),
                ("avg_routed_trades", dart.get("avg_routed_trades")),
                ("new_characteristic_visible", dart.get("new_characteristic_visible")),
                ("onnx_parity_passed", dart.get("onnx_parity_passed")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    return upsert_csv_rows(base.RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def metric(summary: Mapping[str, Any], view: str, key: str) -> Any:
    return summary.get(view, {}).get(key)


def packet_markdown(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    dart = summary.get("dart_booster_read", {})
    return "\n".join(
        [
            "# Stage17 RUN11F XGBoost DART Booster Probe(17단계 실행11F XGBoost DART 부스터 탐침)",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- judgment(판정): `{summary.get('closure_judgment')}`",
            f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
            f"- selected variant(선택 변형): `{summary.get('selected_variant', {}).get('variant_id')}`",
            f"- ONNX parity(ONNX 동등성): `{dart.get('onnx_parity_passed')}`",
            f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`",
            f"- normalized KPI records(정규화 핵심 성과 지표 기록): `{kpi.get('normalized_records')}`",
            f"- trade attribution records(거래 귀속 기록): `{kpi.get('trade_attribution_records')}`",
            "",
            "| split(분할) | routed trades(라우팅 거래 수) | net profit(순수익) | profit factor(수익 팩터) | recovery(회복 계수) |",
            "|---|---:|---:|---:|---:|",
            f"| validation(검증) | `{metric(summary, 'validation_routed', 'trade_count')}` | `{metric(summary, 'validation_routed', 'net_profit')}` | `{metric(summary, 'validation_routed', 'profit_factor')}` | `{metric(summary, 'validation_routed', 'recovery_factor')}` |",
            f"| OOS(표본 밖) | `{metric(summary, 'oos_routed', 'trade_count')}` | `{metric(summary, 'oos_routed', 'net_profit')}` | `{metric(summary, 'oos_routed', 'profit_factor')}` | `{metric(summary, 'oos_routed', 'recovery_factor')}` |",
            "",
            f"- avg routed trades(평균 라우팅 거래 수): `{dart.get('avg_routed_trades')}`",
            f"- trade ratio vs run11B(run11B 대비 거래 비율): `{dart.get('trade_ratio_vs_run11B')}`",
            f"- validation long signal share(검증 롱 신호 비중): `{dart.get('validation_long_signal_share')}`",
            f"- OOS long signal share(표본 밖 롱 신호 비중): `{dart.get('oos_long_signal_share')}`",
            f"- top3 changed(상위 3개 피처 변화): `{dart.get('top3_changed')}`",
            f"- new characteristic visible(새 특성 보임): `{dart.get('new_characteristic_visible')}`",
            "",
            "효과(effect, 효과): DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅)를 기존 gbtree(기본 트리 부스팅)와 같은 데이터, threshold(임계값), MT5(`MetaTrader 5`, 메타트레이더5) 경로에서 비교했다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )


def closeout_markdown(summary: Mapping[str, Any]) -> str:
    dart = summary.get("dart_booster_read", {})
    return "\n".join(
        [
            "# Stage17 Closeout v3(17단계 마감 v3)",
            "",
            f"- closeout run(마감 실행): `{RUN_ID}`",
            f"- judgment(판정): `{summary.get('closure_judgment')}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
            f"- avg routed trades(평균 라우팅 거래 수): `{dart.get('avg_routed_trades')}`",
            f"- new characteristic visible(새 특성 보임): `{dart.get('new_characteristic_visible')}`",
            "",
            "효과(effect, 효과): run11F(실행11F)까지 확인한 뒤 DART 내부 부스터 축에서도 새로 팔 특성이 없으면 Stage17(17단계)을 닫는다. 이 마감은 baseline(기준선) 선택이나 promotion(승격)이 아니다.",
        ]
    )


def write_packet(summary: Mapping[str, Any], kpi: Mapping[str, Any], created_at: str) -> None:
    runtime_ok = summary.get("external_verification_status") == "completed" and summary.get("attempt_count") == 6 and summary.get("mt5_kpi_record_count") == 10
    kpi_ok = kpi.get("normalized_records") == 10 and kpi.get("parser_errors") == 0 and kpi.get("missing_runs") == 0
    dart = summary.get("dart_booster_read", {})
    parity_ok = bool(dart.get("onnx_parity_passed"))
    source_ok = runtime_ok and kpi_ok and parity_ok
    close_ok = source_ok and dart.get("new_characteristic_visible") is False
    payloads = {
        "runtime_evidence_gate": {"audit_name": "runtime_evidence_gate", "status": "pass" if runtime_ok else "blocked", "passed": runtime_ok, "expected_attempts": 6, "expected_kpi_records": 10, "counts": {"attempt_count": summary.get("attempt_count"), "mt5_kpi_record_count": summary.get("mt5_kpi_record_count")}},
        "kpi_contract_audit": {"audit_name": "kpi_contract_audit", "status": "pass" if kpi_ok else "blocked", "passed": kpi_ok, **dict(kpi)},
        "dart_booster_characteristic_audit": {"audit_name": "dart_booster_characteristic_audit", "status": "pass" if source_ok else "blocked", "passed": source_ok, "dart_booster_read": dart},
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass" if source_ok else "blocked", "passed": source_ok, "allowed_claims": [summary.get("closure_judgment"), "runtime_probe"], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"]},
        "required_gate_coverage_audit": {"audit_name": "required_gate_coverage_audit", "status": "pass" if source_ok else "blocked", "passed": source_ok, "required_gates": {"runtime_evidence_gate": "pass" if runtime_ok else "blocked", "kpi_contract_audit": "pass" if kpi_ok else "blocked", "dart_booster_characteristic_audit": "pass" if source_ok else "blocked", "final_claim_guard": "pass" if source_ok else "blocked"}},
    }
    for name, payload in payloads.items():
        write_json(base.PACKET_ROOT / f"{name}.json", payload)
    write_json(base.PACKET_ROOT / "artifact_index.json", {"packet_id": PACKET_ID, "run_summary": base.rel(base.RUN_ROOT / "summary.json"), "report_path": base.rel(base.REVIEW_PACKET_PATH), "created_at_utc": created_at})
    write_json(base.PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "primary_family": "runtime_backtest", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-experiment-design", "obsidian-result-judgment"], "required_gates": list(payloads)})
    write_json(base.PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "receipts": [{"skill": "obsidian-experiment-design", "status": "completed", "effect": "fixed DART booster as the changed variable"}, {"skill": "obsidian-runtime-parity", "status": "completed" if parity_ok else "blocked", "runtime_claim_boundary": "runtime_probe", "effect": "checked ONNX handoff before reading MT5 result"}, {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": summary.get("closure_judgment"), "claim_boundary": BOUNDARY}]})
    write_md(base.REVIEW_PACKET_PATH, packet_markdown(summary, kpi))
    if close_ok:
        closeout_root = base.ROOT / "docs/agent_control/packets" / CLOSEOUT_PACKET_ID
        for name, payload in payloads.items():
            write_json(closeout_root / f"{name}.json", payload)
        write_json(closeout_root / "stage_closeout_evidence_gate.json", {**payloads["dart_booster_characteristic_audit"], "packet_id": CLOSEOUT_PACKET_ID, "closeout_run_id": RUN_ID, "passed": True, "status": "pass"})
        write_json(closeout_root / "artifact_index.json", {"packet_id": CLOSEOUT_PACKET_ID, "source_packet_id": PACKET_ID, "report_path": base.rel(base.STAGE_ROOT / "03_reviews/stage17_closeout_packet.md"), "created_at_utc": created_at})
        write_md(base.STAGE_ROOT / "03_reviews/stage17_closeout_packet.md", closeout_markdown(summary))


def sync_docs(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    dart = summary.get("dart_booster_read", {})
    keep_open = bool(dart.get("new_characteristic_visible"))
    blocked = summary.get("closure_judgment") == JUDGMENT_BLOCKED
    status = "reviewed_run11F_dart_booster_keep_open" if keep_open or blocked else "reviewed_closed_no_next_stage_opened"
    current_status = "reviewed_runtime_probe_completed" if keep_open else ("blocked_runtime_parity" if blocked else "reviewed_closed")
    write_md(
        base.STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage17 Selection Status(17단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{base.STAGE_ID}`",
                f"- status(상태): `{status}`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- model family(모델 계열): XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅)",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{summary.get('closure_judgment')}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage17(17단계)은 DART 내부 부스터 축까지 확인한 상태로 갱신된다.",
            ]
        ),
    )
    write_md(
        base.STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage17 Review Index(17단계 검토 색인)",
                "",
                "- `run11A_xgb_regularized_boosting_characteristic_scout_v1`: gbtree q0.90 characteristic probe(gbtree q0.90 특성 탐침)",
                "- `run11B_xgb_threshold_q80_frequency_pressure_closeout_v1`: q0.80 frequency pressure probe(q0.80 빈도 압박 탐침), closeout superseded(마감 대체됨)",
                "- `run11C_xgb_q80_direction_asymmetry_probe_v1`: direction asymmetry probe(방향 비대칭 탐침)",
                "- `run11D_xgb_trade_shape_attribution_v1`: trade shape attribution(거래 형태 귀속)",
                "- `run11E_xgb_feature_driver_saturation_v1`: feature driver saturation closeout(피처 동인 포화 마감), superseded by run11F reopen(run11F 재개로 대체됨)",
                f"- `{RUN_ID}`: DART booster probe(DART 부스터 탐침)",
                "",
                "효과(effect, 효과): Stage17(17단계) 탐색 흐름이 실행별로 이어져, premature closeout(성급한 마감)을 최종 마감으로 오해하지 않게 한다.",
            ]
        ),
    )
    write_md(
        base.DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-03 Stage17 XGBoost DART Booster Probe(17단계 XGBoost DART 부스터 탐침)",
                "",
                "## Decision(결정)",
                "",
                f"`{RUN_ID}`를 DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅) 내부 부스터 탐침으로 실행했다.",
                "",
                "효과(effect, 효과): 기존 gbtree(기본 트리 부스팅)에서 반복된 피처 동인과 롱 편향이 DART에서도 같은지 확인한다.",
                "",
                "## Judgment(판정)",
                "",
                f"- judgment(판정): `{summary.get('closure_judgment')}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
            ]
        ),
    )
    state_path = base.ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("stage17_reviewed_closed_no_next_stage_opened", f"stage17_{status}", 1)
    state = state.replace("current_run_id: run11E_xgb_feature_driver_saturation_v1", f"current_run_id: {RUN_ID}", 1)
    state = state.replace(
        "treat Stage 17 as reviewed_closed after run11E feature-driver saturation closeout; preserve XGBoost clues but no edge, baseline, promotion, or runtime authority",
        "treat Stage 17 as reopened for run11F DART booster probe before Stage18; no edge, baseline, promotion, or runtime authority",
    )
    stage_block = f"""stage17_xgboost_regularized_boosting_scout:
  stage_id: {base.STAGE_ID}
  status: {status}
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: xgboost_xgbclassifier_multiclass_dart
  current_run_id: {RUN_ID}
  current_status: {current_status}
  hypothesis: XGBoost DART dropout boosting can reveal a remaining internal booster characteristic after gbtree feature-driver saturation.
  comparison_baseline: run11E gbtree feature-driver saturation closeout and run11D long probability skew
  boundary: {BOUNDARY}
  judgment: {summary.get('closure_judgment')}
  selected_variant_id: {summary.get('selected_variant', {}).get('variant_id')}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  normalized_kpi_record_count: {kpi.get('normalized_records')}
  trade_attribution_records: {kpi.get('trade_attribution_records')}
  recommendation: {summary.get('stage17_stop_recommendation')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  closeout_packet_path: {base.rel(base.STAGE_ROOT / '03_reviews/stage17_closeout_packet.md') if not keep_open and not blocked else 'none'}
  decision_path: {base.rel(base.DECISION_PATH)}
  next_action: {'dart_followup_attribution_before_stage18' if keep_open else ('resolve_dart_runtime_parity_before_stage18' if blocked else 'stage18_ready_after_stage17_closeout')}
"""
    state = replace_block(state, "stage17_xgboost_regularized_boosting_scout:", stage_block)
    state = state.replace("stage17_model_family_challenge_closeout:\n  packet_id: stage17_model_family_challenge_closeout_v2\n  status: reviewed_closed_no_next_stage_opened", "stage17_model_family_challenge_closeout:\n  packet_id: stage17_model_family_challenge_closeout_v2\n  status: superseded_by_run11F_reopen", 1)
    if not keep_open and not blocked:
        closeout_block = f"""stage17_model_family_challenge_closeout:
  packet_id: {CLOSEOUT_PACKET_ID}
  status: reviewed_closed_no_next_stage_opened
  judgment: {summary.get('closure_judgment')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  preserved_clues: run11A_visible_regularized_boosting_characteristic_q90,run11B_frequency_density_increase_q80,run11C_direction_asymmetry_long_trade_density,run11D_stable_long_probability_skew,run11E_feature_driver_saturation_no_new_axis,run11F_dart_no_new_internal_booster_axis
  negative_memory: XGBoost DART did not reveal a new internal booster characteristic after gbtree feature-driver saturation
  external_verification_status: completed_for_recorded_stage17_mt5_runtime_probes
  closeout_packet_path: {base.rel(base.STAGE_ROOT / '03_reviews/stage17_closeout_packet.md')}
  closeout_decision_path: {base.rel(base.DECISION_PATH)}
  packet_summary_path: docs/agent_control/packets/{CLOSEOUT_PACKET_ID}/stage_closeout_evidence_gate.json
  next_action: stage18_ready
"""
        state = replace_block(state, "stage17_model_family_challenge_closeout:", closeout_block)
    run_block = f"""stage17_xgboost_run11F_dart_booster_probe:
  packet_id: {PACKET_ID}
  status: reviewed_runtime_probe_completed
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary.get('selected_variant', {}).get('variant_id')}
  threshold_quantile: q{THRESHOLD_QUANTILE:.2f}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  normalized_kpi_record_count: {kpi.get('normalized_records')}
  trade_attribution_records: {kpi.get('trade_attribution_records')}
  new_characteristic_visible: {str(dart.get('new_characteristic_visible')).lower()}
  onnx_parity_passed: {str(dart.get('onnx_parity_passed')).lower()}
  recommendation: {summary.get('stage17_stop_recommendation')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {base.rel(base.REVIEW_PACKET_PATH)}
  decision_path: {base.rel(base.DECISION_PATH)}
"""
    state = replace_block(state, "stage17_xgboost_run11F_dart_booster_probe:", run_block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = base.ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "## Latest Stage17 RUN11F Update(최신 17단계 실행11F 업데이트)",
            "",
            f"Stage17(17단계)은 `{RUN_ID}`로 DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅) 내부 부스터 축을 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 확인했다.",
            "",
            f"효과(effect, 효과): `{summary.get('stage17_stop_recommendation')}`로 기록했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage17 RUN11F Update" not in current:
        current = insert + current
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")
    changelog_path = base.ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage17(17단계) `{RUN_ID}` DART 부스터 탐침을 실행했다. 효과(effect, 효과): MT5 KPI `{summary.get('mt5_kpi_record_count')}`, 정규화 KPI `{kpi.get('normalized_records')}`, 새 특성 `{dart.get('new_characteristic_visible')}`를 기록했다.\n"
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    configure_base()
    created_at = base.utc_now()
    context = base.load_context()
    variant_specs = base.default_stage17_xgb_variants()
    variant_rows = [base.variant_characteristic(context, spec) for spec in variant_specs]
    selected = base.choose_variant(variant_rows)
    variant_artifacts = base.materialize_variant_results(variant_rows)
    selected_model_artifacts, tier_a_model, tier_b_model, tier_a_prob, tier_b_prob, a_threshold, b_threshold = base.materialize_selected_models(context, base.selected_spec(selected))
    tier_records, prediction_artifacts = base.python_tier_records(tier_a_prob, tier_b_prob, a_threshold, b_threshold)
    onnx_artifacts = base.export_models(context, selected_model_artifacts, tier_a_model, tier_b_model)
    model_artifacts = {**selected_model_artifacts, **onnx_artifacts, "thresholds": {"tier_a": a_threshold, "tier_b": b_threshold}}
    feature_matrices = base.export_feature_matrices(context)
    copies = base.copy_runtime_inputs(model_artifacts, feature_matrices)
    attempts = base.make_attempts(context, model_artifacts, feature_matrices, model_artifacts["thresholds"])
    prepared = {"stage_id": base.STAGE_ID, "stage_number": base.STAGE_NUMBER, "run_id": RUN_ID, "run_number": RUN_NUMBER, "run_root": base.RUN_ROOT, "selected_variant_id": selected.get("variant_id"), "attempts": attempts, "common_copies": copies, "route_coverage": context["tier_b_context_summary"], "model_artifacts": model_artifacts, "feature_matrices": list(feature_matrices.values())}
    result = base.execute_or_block(prepared, args)
    result["selected_variant_id"] = selected.get("variant_id")
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    provisional_kpi = {"normalized_records": 0, "normalized_summary_rows": 0, "missing_runs": 0, "parser_errors": 0, "trade_attribution_records": 0, "trade_level_rows": 0, "trade_parser_errors": 0}
    base.write_run_outputs(context, result, selected, variant_rows, variant_artifacts, model_artifacts, prediction_artifacts, tier_records, provisional_kpi, created_at)
    kpi = base.write_normalized_kpi()
    summary = base.write_run_outputs(context, result, selected, variant_rows, variant_artifacts, model_artifacts, prediction_artifacts, tier_records, kpi, created_at)
    write_packet(summary, kpi, created_at)
    write_md(base.RUN_ROOT / "reports/result_summary.md", packet_markdown(summary, kpi))
    sync_docs(summary, kpi)
    print(json.dumps(json_ready({**summary, "kpi_management": kpi}), ensure_ascii=False, indent=2))
    return dict(summary)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage17 XGBoost DART booster MT5 probe.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(base.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(base.METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--materialize-only", action="store_true")
    args = parser.parse_args(argv)
    build_all(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
