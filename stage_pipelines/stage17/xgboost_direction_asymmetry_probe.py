from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, upsert_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload, common_run_root, split_dates_from_frame
from foundation.mt5 import runtime_support as mt5

from . import xgboost_characteristic_mt5_probe as base


RUN_ID = "run11C_xgb_q80_direction_asymmetry_probe_v1"
RUN_NUMBER = "run11C"
PACKET_ID = "stage17_run11C_xgb_direction_asymmetry_v1"
THRESHOLD_QUANTILE = 0.80
BOUNDARY = "xgboost_direction_asymmetry_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_xgboost_direction_asymmetry_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_xgboost_direction_asymmetry_mt5_runtime_probe_after_attempt"
RUN11B_AVG_ROUTED_TRADES = 229.5


def configure_base() -> None:
    root = base.ROOT
    stage_root = root / "stages" / base.STAGE_ID
    base.RUN_ID = RUN_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.PACKET_ID = PACKET_ID
    base.EXPLORATION_LABEL = "stage17_Model__XGBoostDirectionAsymmetry"
    base.BOUNDARY = BOUNDARY
    base.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    base.JUDGMENT_BLOCKED = JUDGMENT_BLOCKED
    base.THRESHOLD_QUANTILE = THRESHOLD_QUANTILE
    base.RUN_ROOT = stage_root / "02_runs" / RUN_ID
    base.PACKET_ROOT = root / "docs/agent_control/packets" / PACKET_ID
    base.REVIEW_PACKET_PATH = stage_root / "03_reviews/run11C_xgb_direction_asymmetry_packet.md"
    base.DECISION_PATH = root / "docs/decisions/2026-05-03_stage17_xgboost_direction_asymmetry.md"
    base.make_attempts = make_attempts  # type: ignore[assignment]
    base.build_summary = build_summary  # type: ignore[assignment]
    base.upsert_run_registry = upsert_run_registry  # type: ignore[assignment]


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def make_attempts(context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], thresholds: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(base.STAGE_NUMBER, RUN_ID)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    disabled_threshold = 1.1
    sides = (
        ("long_only", disabled_threshold, float(thresholds["tier_a"]), disabled_threshold, float(thresholds["tier_b"])),
        ("short_only", float(thresholds["tier_a"]), disabled_threshold, float(thresholds["tier_b"]), disabled_threshold),
    )
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": base.RUN_ROOT,
            "run_id": RUN_ID,
            "stage_number": base.STAGE_NUMBER,
            "exploration_label": base.EXPLORATION_LABEL,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": base.MAX_HOLD_BARS,
            "common_root": common,
        }
        for side, a_short, a_long, b_short, b_long in sides:
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_a_{side}_{runtime_split}", tier=mt5.TIER_A, model_path=f"{common}/models/{tier_a_model}", model_id=f"{RUN_ID}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=a_short, long_threshold=a_long, min_margin=base.MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role=f"tier_a_{side}", record_view_prefix=f"mt5_tier_a_{side}"))
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_b_{side}_{runtime_split}", tier=mt5.TIER_B, model_path=f"{common}/models/{tier_b_model}", model_id=f"{RUN_ID}_tier_b", feature_path=f"{common}/features/{tier_b_matrix}", feature_count=len(context["tier_b_feature_order"]), feature_order_hash=context["tier_b_feature_order_hash"], short_threshold=b_short, long_threshold=b_long, min_margin=base.MIN_MARGIN, invert_signal=False, primary_active_tier="tier_b_fallback", attempt_role=f"tier_b_{side}", record_view_prefix=f"mt5_tier_b_{side}"))
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"routed_{side}_{runtime_split}", tier=mt5.TIER_AB, model_path=f"{common}/models/{tier_a_model}", model_id=f"{RUN_ID}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=a_short, long_threshold=a_long, min_margin=base.MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role=f"routed_{side}", record_view_prefix=f"mt5_routed_{side}", fallback_enabled=True, fallback_model_path=f"{common}/models/{tier_b_model}", fallback_model_id=f"{RUN_ID}_tier_b", fallback_feature_path=f"{common}/features/{tier_b_matrix}", fallback_feature_count=len(context["tier_b_feature_order"]), fallback_feature_order_hash=context["tier_b_feature_order_hash"], fallback_short_threshold=b_short, fallback_long_threshold=b_long, fallback_min_margin=base.MIN_MARGIN, fallback_invert_signal=False))
    return attempts


def record_metrics(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    attempt_name = view.removeprefix("mt5_")
    for execution in result.get("execution_results", []):
        if execution.get("attempt_name") == attempt_name:
            metrics = execution.get("strategy_tester_report", {}).get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def direction_read(summary: Mapping[str, Any]) -> dict[str, Any]:
    long_val = summary["direction_routed"].get("long_validation", {})
    long_oos = summary["direction_routed"].get("long_oos", {})
    short_val = summary["direction_routed"].get("short_validation", {})
    short_oos = summary["direction_routed"].get("short_oos", {})
    long_avg_trades = (safe_float(long_val.get("trade_count")) + safe_float(long_oos.get("trade_count"))) / 2.0
    short_avg_trades = (safe_float(short_val.get("trade_count")) + safe_float(short_oos.get("trade_count"))) / 2.0
    long_avg_pf = (safe_float(long_val.get("profit_factor")) + safe_float(long_oos.get("profit_factor"))) / 2.0
    short_avg_pf = (safe_float(short_val.get("profit_factor")) + safe_float(short_oos.get("profit_factor"))) / 2.0
    contrast = abs(long_avg_trades - short_avg_trades) / max(long_avg_trades + short_avg_trades, 1.0)
    pf_contrast = abs(long_avg_pf - short_avg_pf)
    new_characteristic = contrast >= 0.25 or pf_contrast >= 0.25
    recommendation = "keep_stage17_open_for_trade_shape_or_regime_attribution" if new_characteristic else "close_stage17_no_new_direction_characteristic_after_run11C"
    return {
        "characteristic_score": safe_float(summary.get("selected_variant", {}).get("characteristic_score")),
        "model_characteristic_strength": "direction_asymmetry_visible" if new_characteristic else "no_new_direction_characteristic",
        "stage17_stop_recommendation": recommendation,
        "closure_judgment": JUDGMENT_COMPLETED,
        "direction_asymmetry": {
            "threshold_quantile": THRESHOLD_QUANTILE,
            "long_avg_routed_trades": long_avg_trades,
            "short_avg_routed_trades": short_avg_trades,
            "long_avg_profit_factor": long_avg_pf,
            "short_avg_profit_factor": short_avg_pf,
            "trade_count_contrast": contrast,
            "profit_factor_contrast": pf_contrast,
            "new_characteristic_visible": new_characteristic,
            "run11b_avg_routed_trades": RUN11B_AVG_ROUTED_TRADES,
        },
    }


def build_summary(result: Mapping[str, Any], selected: Mapping[str, Any], variant_artifacts: Mapping[str, Any], model_artifacts: Mapping[str, Any], prediction_artifacts: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    direction_routed = {
        "long_validation": record_metrics(result, "mt5_routed_long_only_validation_is"),
        "long_oos": record_metrics(result, "mt5_routed_long_only_oos"),
        "short_validation": record_metrics(result, "mt5_routed_short_only_validation_is"),
        "short_oos": record_metrics(result, "mt5_routed_short_only_oos"),
    }
    summary = {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": base.STAGE_ID,
        "model_family": base.MODEL_FAMILY,
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
        "direction_routed": direction_routed,
        "validation_routed": direction_routed["long_validation"],
        "oos_routed": direction_routed["long_oos"],
    }
    summary.update(direction_read(summary))
    return summary


def upsert_run_registry(result: Mapping[str, Any], read: Mapping[str, Any]) -> dict[str, Any]:
    asym = read.get("direction_asymmetry", {})
    row = {
        "run_id": RUN_ID,
        "stage_id": base.STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": read["closure_judgment"],
        "path": base.rel(base.RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("model_family", base.MODEL_FAMILY),
                ("routing_mode", "tier_a_primary_tier_b_fallback_direction_split"),
                ("selected_variant", result.get("selected_variant_id")),
                ("threshold_quantile", THRESHOLD_QUANTILE),
                ("long_avg_trades", asym.get("long_avg_routed_trades")),
                ("short_avg_trades", asym.get("short_avg_routed_trades")),
                ("new_characteristic_visible", asym.get("new_characteristic_visible")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    return upsert_csv_rows(base.RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def packet_markdown(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    direction = summary.get("direction_routed", {})
    asym = summary.get("direction_asymmetry", {})
    lines = [
        "# Stage17 RUN11C XGBoost Direction Asymmetry Probe(17단계 실행11C XGBoost 방향 비대칭 탐침)",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- threshold quantile(임계값 분위수): `q{THRESHOLD_QUANTILE:.2f}`",
        f"- judgment(판정): `{summary.get('closure_judgment')}`",
        f"- characteristic strength(특성 강도): `{summary.get('model_characteristic_strength')}`",
        f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{summary.get('mt5_kpi_record_count')}`",
        f"- normalized KPI records(정규화 핵심성과지표 기록): `{kpi.get('normalized_records')}`",
        f"- trade attribution records(거래 귀속 기록): `{kpi.get('trade_attribution_records')}`",
        "",
        "| side(방향) | validation trades/net/PF(검증 거래/순수익/수익 팩터) | OOS trades/net/PF(표본외 거래/순수익/수익 팩터) |",
        "|---|---:|---:|",
        f"| long-only(롱 전용) | `{direction.get('long_validation', {}).get('trade_count')} / {direction.get('long_validation', {}).get('net_profit')} / {direction.get('long_validation', {}).get('profit_factor')}` | `{direction.get('long_oos', {}).get('trade_count')} / {direction.get('long_oos', {}).get('net_profit')} / {direction.get('long_oos', {}).get('profit_factor')}` |",
        f"| short-only(숏 전용) | `{direction.get('short_validation', {}).get('trade_count')} / {direction.get('short_validation', {}).get('net_profit')} / {direction.get('short_validation', {}).get('profit_factor')}` | `{direction.get('short_oos', {}).get('trade_count')} / {direction.get('short_oos', {}).get('net_profit')} / {direction.get('short_oos', {}).get('profit_factor')}` |",
        "",
        f"- new characteristic visible(새 특성 보임): `{asym.get('new_characteristic_visible')}`",
        f"- trade count contrast(거래 수 대비): `{asym.get('trade_count_contrast')}`",
        f"- profit factor contrast(수익 팩터 대비): `{asym.get('profit_factor_contrast')}`",
        "",
        "효과(effect, 효과): run11B(실행11B)의 거래빈도 확대가 어느 방향에서 생기는지 분리한다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
    ]
    return "\n".join(lines)


def write_packet(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    write_md(base.REVIEW_PACKET_PATH, packet_markdown(summary, kpi))
    runtime_ok = summary.get("external_verification_status") == "completed" and summary.get("attempt_count") == 12 and summary.get("mt5_kpi_record_count") == 20
    kpi_ok = kpi.get("normalized_records") == 20 and kpi.get("parser_errors") == 0 and kpi.get("missing_runs") == 0
    payloads = {
        "runtime_evidence_gate": {"audit_name": "runtime_evidence_gate", "status": "pass" if runtime_ok else "blocked", "passed": runtime_ok, "expected_attempts": 12, "expected_kpi_records": 20, "counts": {"attempt_count": summary.get("attempt_count"), "mt5_kpi_record_count": summary.get("mt5_kpi_record_count")}},
        "kpi_contract_audit": {"audit_name": "kpi_contract_audit", "status": "pass" if kpi_ok else "blocked", "passed": kpi_ok, **dict(kpi)},
        "direction_asymmetry_audit": {"audit_name": "direction_asymmetry_audit", "status": "pass" if runtime_ok else "blocked", "passed": runtime_ok, "direction_asymmetry": summary.get("direction_asymmetry", {})},
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass" if runtime_ok and kpi_ok else "blocked", "passed": runtime_ok and kpi_ok, "allowed_claims": [summary.get("closure_judgment"), "runtime_probe"], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority", "stage_closeout_without_no_new_characteristic"]},
        "required_gate_coverage_audit": {"audit_name": "required_gate_coverage_audit", "status": "pass" if runtime_ok and kpi_ok else "blocked", "passed": runtime_ok and kpi_ok, "required_gates": {"runtime_evidence_gate": "pass" if runtime_ok else "blocked", "kpi_contract_audit": "pass" if kpi_ok else "blocked", "direction_asymmetry_audit": "pass" if runtime_ok else "blocked", "final_claim_guard": "pass" if runtime_ok and kpi_ok else "blocked"}},
    }
    for name, payload in payloads.items():
        write_json(base.PACKET_ROOT / f"{name}.json", payload)


def replace_block(text: str, marker: str, block: str) -> str:
    pattern = rf"{re.escape(marker)}\n(?:  .*\n)+"
    if re.search(pattern, text):
        return re.sub(pattern, block, text, count=1)
    return text.rstrip() + "\n" + block


def sync_docs(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    keep_open = summary.get("stage17_stop_recommendation") != "close_stage17_no_new_direction_characteristic_after_run11C"
    status = "reviewed_run11C_direction_asymmetry_keep_open" if keep_open else "reviewed_closed_no_next_stage_opened"
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
                "- model family(모델 계열): XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅)",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{summary.get('closure_judgment')}`",
                f"- MT5 KPI records(MT5 핵심성과지표 기록): `{summary.get('mt5_kpi_record_count')}`",
                f"- normalized KPI records(정규화 핵심성과지표 기록): `{kpi.get('normalized_records')}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage17(17단계)은 성급한 closeout(마감)을 철회하고, XGBoost 방향 비대칭 특성을 MT5/KPI로 추가 확인했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
            ]
        ),
    )
    write_md(
        base.STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage17 Review Index(17단계 검토 색인)",
                "",
                "- `run11A_xgb_regularized_boosting_characteristic_scout_v1`: XGBoost characteristic MT5 KPI probe(XGBoost 특성 MT5 핵심성과지표 탐침)",
                "- `run11B_xgb_threshold_q80_frequency_pressure_closeout_v1`: frequency pressure probe(거래빈도 압박 탐침), closeout superseded(마감 대체됨)",
                f"- `{RUN_ID}`: direction asymmetry probe(방향 비대칭 탐침)",
                "",
                "효과(effect, 효과): Stage17(17단계)의 모델 특성 탐색을 closeout(마감) 전까지 계속 이어가도록 검토 색인을 고쳤다.",
            ]
        ),
    )
    write_md(
        base.DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-03 Stage17 XGBoost Direction Asymmetry(17단계 XGBoost 방향 비대칭)",
                "",
                "## Decision(결정)",
                "",
                f"`{RUN_ID}`를 q{THRESHOLD_QUANTILE:.2f} long-only/short-only(롱 전용/숏 전용) direction asymmetry probe(방향 비대칭 탐침)로 실행했다.",
                "",
                "효과(effect, 효과): run11B(실행11B)의 성급한 closeout(마감)을 대체하고, 새 특성이 보이면 Stage17(17단계)을 계속 열어둔다.",
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
    state = state.replace("stage17_reviewed_closed_no_next_stage_opened", f"stage17_{status}")
    state = state.replace("current_run_id: run11B_xgb_threshold_q80_frequency_pressure_closeout_v1", f"current_run_id: {RUN_ID}", 1)
    state = state.replace("run11B completed frequency pressure MT5 KPI management and Stage17 is closed with no edge, baseline, promotion, or runtime authority", "run11C completed direction asymmetry MT5 KPI management after correcting premature closeout; no edge, baseline, promotion, or runtime authority")
    state = state.replace("status: reviewed_closed_no_next_stage_opened\n      current_run_id: run11B_xgb_threshold_q80_frequency_pressure_closeout_v1", f"status: {status}\n      current_run_id: {RUN_ID}", 1)
    stage_block = f"""stage17_xgboost_regularized_boosting_scout:
  stage_id: {base.STAGE_ID}
  status: {status}
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {base.MODEL_FAMILY}
  current_run_id: {RUN_ID}
  current_status: reviewed_runtime_probe_completed
  hypothesis: XGBoost regularized boosting shows probability, frequency, and direction-asymmetry behavior under fixed data/runtime contract.
  comparison_baseline: run11A q0.90 characteristic probe and run11B q0.80 frequency pressure probe
  boundary: {BOUNDARY}
  judgment: {summary.get('closure_judgment')}
  selected_variant_id: {summary.get('selected_variant', {}).get('variant_id')}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  normalized_kpi_record_count: {kpi.get('normalized_records')}
  trade_attribution_records: {kpi.get('trade_attribution_records')}
  recommendation: {summary.get('stage17_stop_recommendation')}
  stage_brief_path: {base.rel(base.STAGE_ROOT / '00_spec/stage_brief.md')}
  input_references_path: {base.rel(base.STAGE_ROOT / '01_inputs/input_references.md')}
  selection_status_path: {base.rel(base.STAGE_ROOT / '04_selected/selection_status.md')}
  decision_path: {base.rel(base.DECISION_PATH)}
  next_action: {'trade_shape_or_regime_attribution_if_continuing' if keep_open else 'no_stage18_opened'}
"""
    state = replace_block(state, "stage17_xgboost_regularized_boosting_scout:", stage_block)
    state = state.replace("stage17_model_family_challenge_closeout:\n  packet_id: stage17_model_family_challenge_closeout_v1\n  status: reviewed_closed_no_next_stage_opened", "stage17_model_family_challenge_closeout:\n  packet_id: stage17_model_family_challenge_closeout_v1\n  status: superseded_premature_closeout", 1)
    run_block = f"""stage17_xgboost_run11C_direction_asymmetry:
  packet_id: {PACKET_ID}
  status: reviewed_runtime_probe_completed
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary.get('selected_variant', {}).get('variant_id')}
  threshold_quantile: q{THRESHOLD_QUANTILE:.2f}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  normalized_kpi_record_count: {kpi.get('normalized_records')}
  trade_attribution_records: {kpi.get('trade_attribution_records')}
  recommendation: {summary.get('stage17_stop_recommendation')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {base.rel(base.REVIEW_PACKET_PATH)}
  decision_path: {base.rel(base.DECISION_PATH)}
"""
    state = replace_block(state, "stage17_xgboost_run11C_direction_asymmetry:", run_block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = base.ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "## Latest Stage17 RUN11C Update(최신 17단계 실행11C 업데이트)",
            "",
            f"Stage17(17단계)은 `{RUN_ID}`로 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) direction asymmetry(방향 비대칭)를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심성과지표)까지 확인했다.",
            "",
            f"효과(effect, 효과): run11B(실행11B)의 성급한 closeout(마감)을 교정하고 `{summary.get('stage17_stop_recommendation')}`로 기록했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage17 RUN11C Update" not in current:
        current = current.replace("## 쉬운 설명(Plain Read, 쉬운 설명)", insert + "## 쉬운 설명(Plain Read, 쉬운 설명)", 1)
    current = current.replace("current run(현재 실행): `run11B_xgb_threshold_q80_frequency_pressure_closeout_v1`", f"current run(현재 실행): `{RUN_ID}`")
    current = current.replace("Stage17(17단계)은 `run11B_xgb_threshold_q80_frequency_pressure_closeout_v1`로 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) frequency pressure test(거래빈도 압박 시험)를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심성과지표)까지 완료하고 닫았다.", "Stage17(17단계)은 run11B(실행11B) closeout(마감)을 성급한 판정으로 낮추고 run11C(실행11C) 방향 비대칭 탐침을 완료했다.")
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")
    changelog_path = base.ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage17(17단계) `{RUN_ID}` 방향 비대칭 MT5 KPI 탐침을 완료하고 run11B closeout(마감)을 성급한 판정으로 대체했다. 효과(effect, 효과): MT5 KPI `{summary.get('mt5_kpi_record_count')}`, 정규화 KPI `{kpi.get('normalized_records')}`, 거래 귀속 `{kpi.get('trade_attribution_records')}`을 기록하고 `{summary.get('stage17_stop_recommendation')}`로 판독했다.\n"
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
    attempts = make_attempts(context, model_artifacts, feature_matrices, model_artifacts["thresholds"])
    prepared = {"stage_id": base.STAGE_ID, "stage_number": base.STAGE_NUMBER, "run_id": RUN_ID, "run_number": RUN_NUMBER, "run_root": base.RUN_ROOT, "selected_variant_id": selected.get("variant_id"), "attempts": attempts, "common_copies": copies, "route_coverage": context["tier_b_context_summary"], "model_artifacts": model_artifacts, "feature_matrices": list(feature_matrices.values())}
    result = base.execute_or_block(prepared, args)
    result["selected_variant_id"] = selected.get("variant_id")
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    provisional_kpi = {"normalized_records": 0, "normalized_summary_rows": 0, "missing_runs": 0, "parser_errors": 0, "trade_attribution_records": 0, "trade_level_rows": 0, "trade_parser_errors": 0}
    base.write_run_outputs(context, result, selected, variant_rows, variant_artifacts, model_artifacts, prediction_artifacts, tier_records, provisional_kpi, created_at)
    kpi = base.write_normalized_kpi()
    summary = base.write_run_outputs(context, result, selected, variant_rows, variant_artifacts, model_artifacts, prediction_artifacts, tier_records, kpi, created_at)
    write_packet(summary, kpi)
    write_md(base.RUN_ROOT / "reports/result_summary.md", packet_markdown(summary, kpi))
    sync_docs(summary, kpi)
    print(json.dumps(json_ready({**summary, "kpi_management": kpi}), ensure_ascii=False, indent=2))
    return dict(summary)


def refresh_existing_outputs() -> dict[str, Any]:
    configure_base()
    kpi_record_path = base.RUN_ROOT / "kpi_record.json"
    summary_path = base.RUN_ROOT / "summary.json"
    kpi_record = json.loads(io_path(kpi_record_path).read_text(encoding="utf-8-sig"))
    old_summary = json.loads(io_path(summary_path).read_text(encoding="utf-8-sig"))
    mt5_record = kpi_record.get("mt5", {})
    result = {
        "judgment": kpi_record.get("judgment", JUDGMENT_COMPLETED),
        "external_verification_status": kpi_record.get("external_verification_status", "completed"),
        "execution_results": mt5_record.get("execution_results", []),
        "strategy_tester_reports": mt5_record.get("strategy_tester_reports", []),
        "mt5_kpi_records": mt5_record.get("kpi_records", []),
        "attempts": old_summary.get("attempts", mt5_record.get("execution_results", [])),
        "selected_variant_id": old_summary.get("selected_variant", {}).get("variant_id"),
    }
    summary = build_summary(
        result,
        old_summary.get("selected_variant", {}),
        old_summary.get("variant_artifacts", {}),
        old_summary.get("model_artifacts", {}),
        old_summary.get("prediction_artifacts", {}),
        old_summary.get("python_tier_records", []),
    )
    summary["ledger_outputs"] = old_summary.get("ledger_outputs", {})
    summary["registry_output"] = upsert_run_registry(result, summary)
    kpi_record["judgment"] = summary["closure_judgment"]
    kpi_record["registry_output"] = summary["registry_output"]
    kpi = kpi_record.get("kpi_management", {})
    write_json(summary_path, summary)
    write_json(base.PACKET_ROOT / "run_summaries" / f"{RUN_ID}.json", summary)
    write_json(kpi_record_path, kpi_record)
    write_packet(summary, kpi)
    write_md(base.RUN_ROOT / "reports/result_summary.md", packet_markdown(summary, kpi))
    sync_docs(summary, kpi)
    print(json.dumps(json_ready({**summary, "kpi_management": kpi}), ensure_ascii=False, indent=2))
    return dict(summary)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage17 XGBoost q0.80 direction asymmetry probe.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(base.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(base.METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--refresh-existing", action="store_true")
    args = parser.parse_args(argv)
    if args.refresh_existing:
        refresh_existing_outputs()
    else:
        build_all(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
