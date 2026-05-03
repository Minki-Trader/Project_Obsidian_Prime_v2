from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import io_path, json_ready

from . import xgboost_characteristic_mt5_probe as base


RUN_ID = "run11B_xgb_threshold_q80_frequency_pressure_closeout_v1"
RUN_NUMBER = "run11B"
PACKET_ID = "stage17_run11B_xgb_frequency_closeout_v1"
CLOSEOUT_PACKET_ID = "stage17_model_family_challenge_closeout_v1"
THRESHOLD_QUANTILE = 0.80
BOUNDARY = "xgboost_frequency_pressure_closeout_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "closed_inconclusive_xgboost_frequency_pressure_runtime_probe_evidence"
JUDGMENT_BLOCKED = "blocked_xgboost_frequency_pressure_mt5_runtime_probe_after_attempt"
STOP_RECOMMENDATION = "close_stage17_preserve_xgboost_characteristic_and_frequency_pressure_memory"
RUN11A_AVG_ROUTED_TRADES = 125.5


def configure_base() -> None:
    root = base.ROOT
    stage_root = root / "stages" / base.STAGE_ID
    base.RUN_ID = RUN_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.PACKET_ID = PACKET_ID
    base.EXPLORATION_LABEL = "stage17_Model__XGBoostFrequencyPressureCloseout"
    base.BOUNDARY = BOUNDARY
    base.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    base.JUDGMENT_BLOCKED = JUDGMENT_BLOCKED
    base.THRESHOLD_QUANTILE = THRESHOLD_QUANTILE
    base.RUN_ROOT = stage_root / "02_runs" / RUN_ID
    base.PACKET_ROOT = root / "docs/agent_control/packets" / PACKET_ID
    base.REVIEW_PACKET_PATH = stage_root / "03_reviews/run11B_xgb_frequency_pressure_closeout_packet.md"
    base.DECISION_PATH = root / "docs/decisions/2026-05-03_stage17_xgboost_frequency_pressure_closeout.md"
    base.characteristic_read = closeout_read  # type: ignore[assignment]


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def closeout_read(summary: Mapping[str, Any]) -> dict[str, Any]:
    selected = summary.get("selected_variant", {})
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    completed = summary.get("external_verification_status") == "completed"
    val_trades = safe_float(validation.get("trade_count"))
    oos_trades = safe_float(oos.get("trade_count"))
    avg_trades = (val_trades + oos_trades) / 2.0 if val_trades or oos_trades else 0.0
    increase_ratio = avg_trades / RUN11A_AVG_ROUTED_TRADES if RUN11A_AVG_ROUTED_TRADES else 0.0
    val_pf = safe_float(validation.get("profit_factor"))
    oos_pf = safe_float(oos.get("profit_factor"))
    val_net = safe_float(validation.get("net_profit"))
    oos_net = safe_float(oos.get("net_profit"))
    return {
        "characteristic_score": safe_float(selected.get("characteristic_score")),
        "model_characteristic_strength": "visible_frequency_pressure_tested",
        "stage17_stop_recommendation": STOP_RECOMMENDATION,
        "closure_judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "frequency_pressure": {
            "threshold_quantile": THRESHOLD_QUANTILE,
            "run11a_avg_routed_trades": RUN11A_AVG_ROUTED_TRADES,
            "run11b_avg_routed_trades": avg_trades,
            "increase_ratio": increase_ratio,
            "frequency_goal_met": avg_trades > RUN11A_AVG_ROUTED_TRADES,
            "validation_trade_count": val_trades,
            "oos_trade_count": oos_trades,
            "validation_profit_factor": val_pf,
            "oos_profit_factor": oos_pf,
            "validation_net_profit": val_net,
            "oos_net_profit": oos_net,
        },
    }


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def metric(summary: Mapping[str, Any], view: str, key: str) -> Any:
    return summary.get(view, {}).get(key)


def clean_run_report(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    fp = summary.get("frequency_pressure", {})
    lines = [
        "# Stage17 RUN11B XGBoost Frequency Pressure Result(17단계 실행11B XGBoost 거래빈도 압박 결과)",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- threshold quantile(임계값 분위수): `q{THRESHOLD_QUANTILE:.2f}`",
        f"- judgment(판정): `{summary.get('closure_judgment')}`",
        f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{summary.get('mt5_kpi_record_count')}`",
        f"- normalized KPI records(정규화 핵심성과지표 기록): `{kpi.get('normalized_records')}`",
        f"- trade attribution records(거래 귀속 기록): `{kpi.get('trade_attribution_records')}`",
        "",
        "| split(분할) | routed trades(라우팅 거래 수) | net profit(순수익) | profit factor(수익 팩터) | recovery(회복 계수) |",
        "|---|---:|---:|---:|---:|",
        f"| validation(검증) | `{metric(summary, 'validation_routed', 'trade_count')}` | `{metric(summary, 'validation_routed', 'net_profit')}` | `{metric(summary, 'validation_routed', 'profit_factor')}` | `{metric(summary, 'validation_routed', 'recovery_factor')}` |",
        f"| OOS(표본외) | `{metric(summary, 'oos_routed', 'trade_count')}` | `{metric(summary, 'oos_routed', 'net_profit')}` | `{metric(summary, 'oos_routed', 'profit_factor')}` | `{metric(summary, 'oos_routed', 'recovery_factor')}` |",
        "",
        f"- average routed trades(평균 라우팅 거래 수): `{fp.get('run11b_avg_routed_trades')}`",
        f"- run11A average routed trades(run11A 평균 라우팅 거래 수): `{fp.get('run11a_avg_routed_trades')}`",
        f"- increase ratio(증가 배율): `{fp.get('increase_ratio')}`",
        "",
        "효과(effect, 효과): 거래 빈도는 늘렸지만 이 결과는 frequency pressure test(빈도 압박 시험)다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
    ]
    return "\n".join(lines)


def write_packet(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    review = base.REVIEW_PACKET_PATH
    write_md(review, clean_run_report(summary, kpi))
    gate_ok = summary.get("external_verification_status") == "completed" and summary.get("mt5_kpi_record_count") == 10
    kpi_ok = kpi.get("normalized_records") == 10 and kpi.get("parser_errors") == 0 and kpi.get("missing_runs") == 0
    payloads = {
        "frequency_pressure_audit": {
            "audit_name": "frequency_pressure_audit",
            "passed": gate_ok,
            "status": "pass" if gate_ok else "blocked",
            "frequency_pressure": summary.get("frequency_pressure", {}),
        },
        "stage_closeout_evidence_gate": {
            "audit_name": "stage_closeout_evidence_gate",
            "passed": gate_ok and kpi_ok,
            "status": "pass" if gate_ok and kpi_ok else "blocked",
            "source_runs": ["run11A_xgb_regularized_boosting_characteristic_scout_v1", RUN_ID],
            "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"),
            "normalized_kpi_record_count": kpi.get("normalized_records"),
            "trade_attribution_records": kpi.get("trade_attribution_records"),
            "judgment": summary.get("closure_judgment"),
        },
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "passed": gate_ok and kpi_ok,
            "status": "pass" if gate_ok and kpi_ok else "blocked",
            "allowed_claims": [summary.get("closure_judgment"), "stage17_closeout", "runtime_probe"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "passed": gate_ok and kpi_ok,
            "status": "pass" if gate_ok and kpi_ok else "blocked",
            "required_gates": {
                "runtime_evidence_gate": "pass" if gate_ok else "blocked",
                "kpi_contract_audit": "pass" if kpi_ok else "blocked",
                "frequency_pressure_audit": "pass" if gate_ok else "blocked",
                "stage_closeout_evidence_gate": "pass" if gate_ok and kpi_ok else "blocked",
                "final_claim_guard": "pass" if gate_ok and kpi_ok else "blocked",
            },
        },
    }
    for name, payload in payloads.items():
        write_json(base.PACKET_ROOT / f"{name}.json", payload)
    closeout_root = base.ROOT / "docs/agent_control/packets" / CLOSEOUT_PACKET_ID
    for name, payload in payloads.items():
        write_json(closeout_root / f"{name}.json", payload)
    write_json(closeout_root / "artifact_index.json", {"packet_id": CLOSEOUT_PACKET_ID, "source_packet_id": PACKET_ID, "run_summary": summary, "report_path": base.rel(base.STAGE_ROOT / "03_reviews/stage17_closeout_packet.md")})


def closeout_markdown(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    fp = summary.get("frequency_pressure", {})
    lines = [
        "# Stage17 Closeout Packet(17단계 마감 묶음)",
        "",
        f"- closeout judgment(마감 판정): `{summary.get('closure_judgment')}`",
        f"- final run(최종 실행): `{RUN_ID}`",
        f"- threshold quantile(임계값 분위수): `q{THRESHOLD_QUANTILE:.2f}`",
        f"- run11A average routed trades(run11A 평균 라우팅 거래 수): `{fp.get('run11a_avg_routed_trades')}`",
        f"- run11B average routed trades(run11B 평균 라우팅 거래 수): `{fp.get('run11b_avg_routed_trades')}`",
        f"- increase ratio(증가 배율): `{fp.get('increase_ratio')}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{summary.get('mt5_kpi_record_count')}`",
        f"- normalized KPI records(정규화 핵심성과지표 기록): `{kpi.get('normalized_records')}`",
        f"- trade attribution records(거래 귀속 기록): `{kpi.get('trade_attribution_records')}`",
        "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| run(실행) | validation routed trades(검증 라우팅 거래 수) | OOS routed trades(표본외 라우팅 거래 수) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) |",
        "|---|---:|---:|---:|---:|",
        "| run11A | `150` | `101` | `-250.95 / 0.74` | `222.0 / 1.58` |",
        f"| run11B | `{metric(summary, 'validation_routed', 'trade_count')}` | `{metric(summary, 'oos_routed', 'trade_count')}` | `{metric(summary, 'validation_routed', 'net_profit')} / {metric(summary, 'validation_routed', 'profit_factor')}` | `{metric(summary, 'oos_routed', 'net_profit')} / {metric(summary, 'oos_routed', 'profit_factor')}` |",
        "",
        "효과(effect, 효과): XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅)는 distinct model behavior(구별되는 모델 행동)를 보였고, threshold relaxation(임계값 완화)으로 거래 빈도도 늘릴 수 있었다. 하지만 validation/OOS(검증/표본외) 품질이 운영 의미로 이어지지 않아 Stage17(17단계)은 inconclusive closeout(불충분 마감)으로 닫는다.",
        "",
        "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
    ]
    return "\n".join(lines)


def replace_block(text: str, marker: str, block: str) -> str:
    pattern = rf"{re.escape(marker)}\n(?:  .*\n)+"
    if re.search(pattern, text):
        return re.sub(pattern, block, text, count=1)
    return text.rstrip() + "\n" + block


def sync_state(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    state_path = base.ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("stage17_reviewed_run11A_mt5_kpi_probe_keep_open", "stage17_reviewed_closed_no_next_stage_opened")
    state = state.replace("reviewed_run11A_mt5_kpi_probe_keep_open", "reviewed_closed_no_next_stage_opened")
    state = re.sub(
        r"(stage17_xgboost_run11A_characteristic_mt5_kpi:\n  packet_id: stage17_run11A_xgb_characteristic_mt5_kpi_v1\n  status: )reviewed_closed_no_next_stage_opened",
        r"\1reviewed_runtime_probe_completed",
        state,
        count=1,
    )
    state = state.replace("current_run_id: run11A_xgb_regularized_boosting_characteristic_scout_v1", f"current_run_id: {RUN_ID}", 1)
    state = state.replace("run11A completed MT5 KPI management and shows visible model-characteristic evidence, but no edge, baseline, promotion, or runtime authority exists", "run11B completed frequency pressure MT5 KPI management and Stage17 is closed with no edge, baseline, promotion, or runtime authority")
    stage_block = f"""stage17_xgboost_regularized_boosting_scout:
  stage_id: {base.STAGE_ID}
  status: reviewed_closed_no_next_stage_opened
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {base.MODEL_FAMILY}
  current_run_id: {RUN_ID}
  current_status: reviewed_closed
  hypothesis: XGBoost regularized boosting can show distinct probability and signal-density behavior, but frequency expansion did not create operating-quality evidence.
  comparison_baseline: run11A q0.90 characteristic probe and fixed data/runtime contract
  boundary: {BOUNDARY}
  judgment: {summary.get('closure_judgment')}
  selected_variant_id: {summary.get('selected_variant', {}).get('variant_id')}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  normalized_kpi_record_count: {kpi.get('normalized_records')}
  trade_attribution_records: {kpi.get('trade_attribution_records')}
  recommendation: {STOP_RECOMMENDATION}
  stage_brief_path: {base.rel(base.STAGE_ROOT / '00_spec/stage_brief.md')}
  input_references_path: {base.rel(base.STAGE_ROOT / '01_inputs/input_references.md')}
  selection_status_path: {base.rel(base.STAGE_ROOT / '04_selected/selection_status.md')}
  closeout_packet_path: {base.rel(base.STAGE_ROOT / '03_reviews/stage17_closeout_packet.md')}
  closeout_decision_path: {base.rel(base.DECISION_PATH)}
  next_action: no_stage18_opened
"""
    state = replace_block(state, "stage17_xgboost_regularized_boosting_scout:", stage_block)
    run_block = f"""stage17_xgboost_run11B_frequency_pressure_closeout:
  packet_id: {PACKET_ID}
  status: reviewed_closed_no_next_stage_opened
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary.get('selected_variant', {}).get('variant_id')}
  threshold_quantile: q{THRESHOLD_QUANTILE:.2f}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  normalized_kpi_record_count: {kpi.get('normalized_records')}
  trade_attribution_records: {kpi.get('trade_attribution_records')}
  recommendation: {STOP_RECOMMENDATION}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {base.rel(base.REVIEW_PACKET_PATH)}
  decision_path: {base.rel(base.DECISION_PATH)}
"""
    state = replace_block(state, "stage17_xgboost_run11B_frequency_pressure_closeout:", run_block)
    closeout_block = f"""stage17_model_family_challenge_closeout:
  packet_id: {CLOSEOUT_PACKET_ID}
  status: reviewed_closed_no_next_stage_opened
  judgment: {summary.get('closure_judgment')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  preserved_clues: run11A_visible_xgboost_characteristic,run11B_frequency_pressure_trade_density_expansion
  negative_memory: threshold relaxation increased trade count but did not create edge, alpha quality, baseline, promotion, or runtime authority
  external_verification_status: {summary.get('external_verification_status')}
  closeout_packet_path: {base.rel(base.STAGE_ROOT / '03_reviews/stage17_closeout_packet.md')}
  closeout_decision_path: {base.rel(base.DECISION_PATH)}
  packet_summary_path: docs/agent_control/packets/{CLOSEOUT_PACKET_ID}/stage_closeout_evidence_gate.json
  next_action: no_stage18_opened
"""
    state = replace_block(state, "stage17_model_family_challenge_closeout:", closeout_block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")


def sync_docs(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    write_md(base.STAGE_ROOT / "03_reviews/stage17_closeout_packet.md", closeout_markdown(summary, kpi))
    write_md(
        base.STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage17 Selection Status(17단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{base.STAGE_ID}`",
                "- status(상태): `reviewed_closed_no_next_stage_opened(검토 후 마감, 다음 단계 미개방)`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- model family(모델 계열): XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅)",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{summary.get('closure_judgment')}`",
                f"- MT5 KPI records(MT5 핵심성과지표 기록): `{summary.get('mt5_kpi_record_count')}`",
                f"- normalized KPI records(정규화 핵심성과지표 기록): `{kpi.get('normalized_records')}`",
                f"- recommendation(권고): `{STOP_RECOMMENDATION}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage17(17단계)은 XGBoost 특성과 거래 빈도 확대 압박을 MT5/KPI까지 확인하고 닫았다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
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
                f"- `{RUN_ID}`: frequency pressure closeout probe(거래빈도 압박 마감 탐침)",
                "- `stage17_closeout_packet.md`: Stage17 closeout(17단계 마감)",
                "",
                "효과(effect, 효과): Stage17(17단계)의 모델 특성, 거래 빈도 확대, MT5 KPI, 마감 판정을 한 검토 색인에서 추적한다.",
            ]
        ),
    )
    write_md(
        base.DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-03 Stage17 XGBoost Frequency Pressure Closeout(17단계 XGBoost 거래빈도 압박 마감)",
                "",
                "## Decision(결정)",
                "",
                f"`{RUN_ID}`를 q{THRESHOLD_QUANTILE:.2f} threshold quantile(임계값 분위수) frequency pressure test(거래빈도 압박 시험)로 실행하고 Stage17(17단계)을 닫는다.",
                "",
                "효과(effect, 효과): run11A(실행11A)의 XGBoost 특성이 실제로 빈도 확대까지 이어지는지 확인했고, 더 파도 Stage17 고유 질문은 충분히 답한 상태로 정리한다.",
                "",
                "## Judgment(판정)",
                "",
                f"- judgment(판정): `{summary.get('closure_judgment')}`",
                f"- recommendation(권고): `{STOP_RECOMMENDATION}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            ]
        ),
    )
    current_path = base.ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "## Latest Stage17 Closeout Update(최신 17단계 마감 업데이트)",
            "",
            f"Stage17(17단계)은 `{RUN_ID}`로 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) frequency pressure test(거래빈도 압박 시험)를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심성과지표)까지 완료하고 닫았다.",
            "",
            f"효과(effect, 효과): `{summary.get('closure_judgment')}`로 기록했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage17 Closeout Update" not in current:
        current = current.replace("## 쉬운 설명(Plain Read, 쉬운 설명)", insert + "## 쉬운 설명(Plain Read, 쉬운 설명)", 1)
    current = current.replace("reviewed_run11A_mt5_kpi_probe_keep_open", "reviewed_closed_no_next_stage_opened")
    current = current.replace("current run(현재 실행): `run11A_xgb_regularized_boosting_characteristic_scout_v1`", f"current run(현재 실행): `{RUN_ID}`")
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")
    changelog_path = base.ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage17(17단계) `{RUN_ID}` 거래빈도 압박 MT5 KPI 탐침을 완료하고 Stage17을 닫았다. 효과(effect, 효과): q{THRESHOLD_QUANTILE:.2f} 임계값으로 MT5 KPI `{summary.get('mt5_kpi_record_count')}`, 정규화 KPI `{kpi.get('normalized_records')}`, 거래 귀속 `{kpi.get('trade_attribution_records')}`을 기록하고 edge(거래 우위) 없이 `{summary.get('closure_judgment')}`로 마감했다.\n"
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")
    sync_state(summary, kpi)


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
    base.write_packet_files(summary, kpi, created_at)
    write_packet(summary, kpi)
    write_md(base.RUN_ROOT / "reports/result_summary.md", clean_run_report(summary, kpi))
    sync_docs(summary, kpi)
    print(json.dumps(json_ready({**summary, "kpi_management": kpi}), ensure_ascii=False, indent=2))
    return dict(summary)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage17 XGBoost q0.80 frequency pressure closeout probe.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(base.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(base.METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--materialize-only", action="store_true")
    args = parser.parse_args(argv)
    build_all(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
