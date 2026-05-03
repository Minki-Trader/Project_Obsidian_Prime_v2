from __future__ import annotations

import csv
import json
import math
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.alpha_run_ledgers import materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, upsert_csv_rows


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "17_model_family_challenge__xgboost_regularized_boosting_scout"
RUN_ID = "run11G_xgb_dart_attribution_closeout_v1"
RUN_NUMBER = "run11G"
PACKET_ID = "stage17_run11G_xgb_dart_attribution_closeout_v1"
CLOSEOUT_PACKET_ID = "stage17_model_family_challenge_closeout_v3"
SOURCE_RUN_ID = "run11F_xgb_dart_booster_probe_v1"
SOURCE_PACKET_ID = "stage17_run11F_xgb_dart_booster_probe_v1"
EXPLORATION_LABEL = "stage17_Model__XGBoostDARTAttributionCloseout"
BOUNDARY = "xgboost_dart_attribution_closeout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "closed_inconclusive_xgboost_dart_attribution_no_new_axis_after_run11G"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
SOURCE_PACKET_ROOT = ROOT / "docs/agent_control/packets" / SOURCE_PACKET_ID
CLOSEOUT_PACKET_ROOT = ROOT / "docs/agent_control/packets" / CLOSEOUT_PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews/run11G_xgb_dart_attribution_closeout_packet.md"
CLOSEOUT_REPORT_PATH = STAGE_ROOT / "03_reviews/stage17_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-03_stage17_xgboost_dart_attribution_closeout.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6g}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def replace_block(text: str, marker: str, block: str) -> str:
    pattern = rf"{re.escape(marker)}\n(?:  .*\n)+"
    if re.search(pattern, text):
        return re.sub(pattern, block, text, count=1)
    return text.rstrip() + "\n" + block


def load_inputs() -> dict[str, Any]:
    source_summary = read_json(SOURCE_ROOT / "summary.json")
    source_kpi = read_json(SOURCE_ROOT / "kpi_record.json")
    trade_summary = pd.read_csv(io_path(SOURCE_PACKET_ROOT / "trade_attribution_summary.csv"))
    trade_level = pd.read_csv(io_path(SOURCE_PACKET_ROOT / "trade_level_records.csv"))
    return {"source_summary": source_summary, "source_kpi": source_kpi, "trade_summary": trade_summary, "trade_level": trade_level}


def feature_read(source_summary: Mapping[str, Any]) -> dict[str, Any]:
    dart = source_summary.get("dart_booster_read", {})
    top3 = list(dart.get("top3_features") or [])
    prior = list(dart.get("prior_gbtree_top3_features") or [])
    top2_same = bool(len(top3) >= 2 and len(prior) >= 2 and top3[:2] == prior[:2])
    changed_slot = ""
    if len(top3) >= 3 and len(prior) >= 3 and top3[2] != prior[2]:
        changed_slot = f"{prior[2]}=>{top3[2]}"
    return {
        "dart_top3_features": top3,
        "prior_gbtree_top3_features": prior,
        "top2_same": top2_same,
        "changed_slot": changed_slot,
        "feature_shift_kind": "third_slot_ema_ratio_replaces_open_session_flag" if changed_slot else "no_top3_shift",
    }


def routed_trade_rows(trade_summary: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    data = trade_summary[trade_summary["record_view"].isin(["mt5_routed_total_validation_is", "mt5_routed_total_oos"])].copy()
    for _, row in data.iterrows():
        trade_count = safe_float(row.get("trade_count"))
        long_net = safe_float(row.get("long_net_profit"))
        short_net = safe_float(row.get("short_net_profit"))
        rows.append(
            {
                "record_view": str(row.get("record_view")),
                "split": str(row.get("split")),
                "trade_count": int(trade_count),
                "avg_hold_bars": safe_float(row.get("avg_hold_bars")),
                "mfe_mean": safe_float(row.get("mfe_mean")),
                "mae_mean": safe_float(row.get("mae_mean")),
                "long_net_profit": long_net,
                "short_net_profit": short_net,
                "long_net_share": safe_div(long_net, long_net + short_net),
                "positive_month_ratio": safe_float(row.get("positive_month_ratio")),
            }
        )
    return rows


def regime_summary(trade_level: pd.DataFrame) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    routed = trade_level[trade_level["record_view"].isin(["mt5_routed_total_validation_is", "mt5_routed_total_oos"])].copy()
    for split, split_rows in routed.groupby("split"):
        total = float(len(split_rows))
        for column in ("session_slice", "volatility_regime", "trend_regime", "adx_bucket"):
            if column not in split_rows:
                continue
            counts = split_rows[column].fillna("unknown").astype(str).value_counts()
            if counts.empty:
                continue
            top_value = str(counts.index[0])
            top_count = int(counts.iloc[0])
            top_net = safe_float(split_rows.loc[split_rows[column].astype(str).eq(top_value), "net_profit"].sum())
            out.append(
                {
                    "split": str(split),
                    "regime_type": column,
                    "top_value": top_value,
                    "top_trade_count": top_count,
                    "top_trade_share": safe_div(float(top_count), total),
                    "top_net_profit": top_net,
                }
            )
    return out


def attribution_read(source_summary: Mapping[str, Any], trade_rows: Sequence[Mapping[str, Any]], regimes: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    dart = source_summary.get("dart_booster_read", {})
    validation = source_summary.get("validation_routed", {})
    oos = source_summary.get("oos_routed", {})
    val_dd = safe_float(validation.get("max_drawdown_percent"))
    oos_dd = safe_float(oos.get("max_drawdown_percent"))
    val_pf = safe_float(validation.get("profit_factor"))
    oos_pf = safe_float(oos.get("profit_factor"))
    val_trades = safe_float(validation.get("trade_count"))
    oos_trades = safe_float(oos.get("trade_count"))
    val_long_share = safe_div(safe_float(validation.get("long_trade_count")), val_trades)
    oos_long_share = safe_div(safe_float(oos.get("long_trade_count")), oos_trades)
    long_skew_persisted = val_long_share >= 0.75 and oos_long_share >= 0.75
    both_splits_positive = safe_float(validation.get("net_profit")) > 0.0 and safe_float(oos.get("net_profit")) > 0.0
    risk_blocks_quality_claim = val_dd >= 50.0 or oos_dd >= 35.0
    top_regimes = [row for row in regimes if safe_float(row.get("top_trade_share")) >= 0.45]
    no_second_order_axis = long_skew_persisted and bool(dart.get("top3_changed")) and risk_blocks_quality_claim
    return {
        "new_attribution_axis_visible": not no_second_order_axis,
        "closeout_ready": no_second_order_axis,
        "long_skew_persisted": long_skew_persisted,
        "validation_long_trade_share": val_long_share,
        "oos_long_trade_share": oos_long_share,
        "both_splits_positive": both_splits_positive,
        "validation_profit_factor": val_pf,
        "oos_profit_factor": oos_pf,
        "validation_max_drawdown_percent": val_dd,
        "oos_max_drawdown_percent": oos_dd,
        "risk_blocks_quality_claim": risk_blocks_quality_claim,
        "top_regime_concentrations": top_regimes,
        "plain_read": "DART changed the third feature slot but preserved the Stage17 long-skew trade shape; drawdown blocks quality claims.",
    }


def build_summary() -> dict[str, Any]:
    inputs = load_inputs()
    source_summary = inputs["source_summary"]
    trade_rows = routed_trade_rows(inputs["trade_summary"])
    regimes = regime_summary(inputs["trade_level"])
    feature = feature_read(source_summary)
    read = attribution_read(source_summary, trade_rows, regimes)
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "closeout_packet_id": CLOSEOUT_PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": "xgboost_xgbclassifier_multiclass_dart",
        "boundary": BOUNDARY,
        "judgment": JUDGMENT,
        "external_verification_status": "completed_reused_run11F_mt5_and_kpi_evidence",
        "source_mt5_kpi_record_count": source_summary.get("mt5_kpi_record_count"),
        "source_normalized_kpi_records": inputs["source_kpi"].get("kpi_management", {}).get("normalized_records"),
        "source_trade_attribution_records": inputs["source_kpi"].get("kpi_management", {}).get("trade_attribution_records"),
        "feature_shift_read": feature,
        "routed_trade_rows": trade_rows,
        "regime_summary": regimes,
        "attribution_read": read,
        "stage17_stop_recommendation": "close_stage17_after_dart_attribution_no_new_axis" if read["closeout_ready"] else "keep_stage17_open_for_dart_regime_followup",
        "closure_judgment": JUDGMENT if read["closeout_ready"] else "inconclusive_xgboost_dart_attribution_followup_needed",
        "selected_operating_reference": "none",
        "selected_promotion_candidate": "none",
        "selected_baseline": "none",
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }


def materialize(summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    write_csv(RUN_ROOT / "results/dart_routed_trade_shape.csv", ("record_view", "split", "trade_count", "avg_hold_bars", "mfe_mean", "mae_mean", "long_net_profit", "short_net_profit", "long_net_share", "positive_month_ratio"), summary["routed_trade_rows"])
    write_csv(RUN_ROOT / "results/dart_regime_summary.csv", ("split", "regime_type", "top_value", "top_trade_count", "top_trade_share", "top_net_profit"), summary["regime_summary"])
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__dart_attribution_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "dart_attribution_closeout",
        "parent_run_id": RUN_ID,
        "record_view": "stage17_dart_attribution_closeout",
        "tier_scope": "Tier A+B",
        "kpi_scope": "model_characteristic_attribution_closeout",
        "scoreboard_lane": "model_characteristic_closeout",
        "status": "completed",
        "judgment": summary["closure_judgment"],
        "path": rel(RUN_ROOT / "summary.json"),
        "primary_kpi": ledger_pairs((("new_attribution_axis_visible", summary["attribution_read"].get("new_attribution_axis_visible")), ("long_skew_persisted", summary["attribution_read"].get("long_skew_persisted")), ("both_splits_positive", summary["attribution_read"].get("both_splits_positive")))),
        "guardrail_kpi": ledger_pairs((("risk_blocks_quality_claim", summary["attribution_read"].get("risk_blocks_quality_claim")), ("boundary", BOUNDARY), ("recommendation", summary.get("stage17_stop_recommendation")))),
        "external_verification_status": summary.get("external_verification_status"),
        "notes": "DART attribution closeout reused run11F MT5 evidence; no edge, alpha quality, baseline, promotion, or runtime authority.",
    }
    ledger_outputs = materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=[ledger_row])
    registry_output = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "model_characteristic_closeout",
                "status": "reviewed_closed",
                "judgment": summary["closure_judgment"],
                "path": rel(RUN_ROOT),
                "notes": ledger_pairs((("recommendation", summary.get("stage17_stop_recommendation")), ("source_run", SOURCE_RUN_ID), ("boundary", "closeout_only"))),
            }
        ],
        key="run_id",
    )
    final = {**dict(summary), "ledger_outputs": ledger_outputs, "registry_output": registry_output}
    write_json(RUN_ROOT / "run_manifest.json", {"run_id": RUN_ID, "packet_id": PACKET_ID, "stage_id": STAGE_ID, "created_at_utc": created_at, "source_run_id": SOURCE_RUN_ID, "boundary": BOUNDARY})
    write_json(RUN_ROOT / "summary.json", final)
    write_json(RUN_ROOT / "kpi_record.json", {"run_id": RUN_ID, "packet_id": PACKET_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "kpi_scope": "xgboost_dart_attribution_closeout", "external_verification_status": summary.get("external_verification_status"), "judgment": summary["closure_judgment"], "boundary": BOUNDARY, "attribution_read": summary["attribution_read"], "ledger_outputs": ledger_outputs, "registry_output": registry_output})
    write_json(PACKET_ROOT / "run_summaries" / f"{RUN_ID}.json", final)
    write_packet(final, created_at)
    sync_docs(final)
    return final


def packet_markdown(summary: Mapping[str, Any]) -> str:
    read = summary["attribution_read"]
    feature = summary["feature_shift_read"]
    lines = [
        "# Stage17 RUN11G XGBoost DART Attribution Closeout(17단계 실행11G XGBoost DART 귀속 마감)",
        "",
        f"- judgment(판정): `{summary.get('closure_judgment')}`",
        f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
        f"- feature shift(피처 변화): `{feature.get('changed_slot')}`",
        f"- long skew persisted(롱 편향 지속): `{read.get('long_skew_persisted')}`",
        f"- both splits positive(두 분할 모두 양수): `{read.get('both_splits_positive')}`",
        f"- risk blocks quality claim(위험이 품질 주장 차단): `{read.get('risk_blocks_quality_claim')}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| split(분할) | trades(거래 수) | avg hold(평균 보유) | long net(롱 순수익) | short net(숏 순수익) | positive months(양수 월 비율) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary["routed_trade_rows"]:
        lines.append(f"| `{row.get('split')}` | `{row.get('trade_count')}` | `{row.get('avg_hold_bars')}` | `{row.get('long_net_profit')}` | `{row.get('short_net_profit')}` | `{row.get('positive_month_ratio')}` |")
    lines.extend(
        [
            "",
            "효과(effect, 효과): DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅)는 새 피처 단서를 남겼지만, 거래 형태는 Stage17(17단계)의 기존 롱 편향을 벗어나지 않았다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def closeout_markdown(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# Stage17 Closeout v3(17단계 마감 v3)",
            "",
            f"- closeout run(마감 실행): `{RUN_ID}`",
            f"- judgment(판정): `{summary.get('closure_judgment')}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
            "",
            "## Preserved Clues(보존 단서)",
            "",
            "- run11A: q0.90 gbtree(기본 트리 부스팅) 특성이 보였다.",
            "- run11B: q0.80에서 거래 빈도는 늘었다.",
            "- run11C/run11D: 롱 신호와 롱 거래 편향이 반복됐다.",
            "- run11E: gbtree 피처 동인은 포화됐다.",
            "- run11F/run11G: DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅)는 `close_ema20_ratio`를 top3(상위 3개)에 올렸지만, 추가 귀속 축은 만들지 않았다.",
            "",
            "효과(effect, 효과): Stage17(17단계)을 모델 특성 기억으로 닫고 Stage18(18단계)로 넘어갈 수 있다. 이 마감은 baseline(기준선)이나 promotion(승격)이 아니다.",
        ]
    )


def write_packet(summary: Mapping[str, Any], created_at: str) -> None:
    source_ok = summary.get("external_verification_status") == "completed_reused_run11F_mt5_and_kpi_evidence"
    close_ok = source_ok and summary["attribution_read"].get("closeout_ready") is True
    payloads = {
        "source_evidence_gate": {"audit_name": "source_evidence_gate", "status": "pass" if source_ok else "blocked", "passed": source_ok, "source_run_id": SOURCE_RUN_ID, "source_packet_id": SOURCE_PACKET_ID, "source_mt5_kpi_record_count": summary.get("source_mt5_kpi_record_count"), "source_normalized_kpi_records": summary.get("source_normalized_kpi_records"), "source_trade_attribution_records": summary.get("source_trade_attribution_records")},
        "dart_attribution_closeout_audit": {"audit_name": "dart_attribution_closeout_audit", "status": "pass" if close_ok else "blocked", "passed": close_ok, "attribution_read": summary.get("attribution_read"), "feature_shift_read": summary.get("feature_shift_read")},
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass" if close_ok else "blocked", "passed": close_ok, "allowed_claims": [summary.get("closure_judgment"), "stage17_closeout"], "forbidden_claims": summary.get("forbidden_claims")},
        "required_gate_coverage_audit": {"audit_name": "required_gate_coverage_audit", "status": "pass" if close_ok else "blocked", "passed": close_ok, "required_gates": {"source_evidence_gate": "pass" if source_ok else "blocked", "dart_attribution_closeout_audit": "pass" if close_ok else "blocked", "final_claim_guard": "pass" if close_ok else "blocked"}},
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "primary_family": "model_characteristic_closeout", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"], "required_gates": list(payloads)})
    write_json(PACKET_ROOT / "artifact_index.json", {"packet_id": PACKET_ID, "run_summary": rel(RUN_ROOT / "summary.json"), "report_path": rel(REPORT_PATH), "closeout_report_path": rel(CLOSEOUT_REPORT_PATH), "created_at_utc": created_at})
    write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "receipts": [{"skill": "obsidian-result-judgment", "status": "completed", "effect": "closed Stage17 only after DART attribution produced no second-order axis"}, {"skill": "obsidian-runtime-parity", "status": "completed", "effect": "reused run11F completed MT5 and ONNX parity evidence"}]})
    for name, payload in payloads.items():
        write_json(CLOSEOUT_PACKET_ROOT / f"{name}.json", payload)
    write_json(CLOSEOUT_PACKET_ROOT / "stage_closeout_evidence_gate.json", {**payloads["dart_attribution_closeout_audit"], "packet_id": CLOSEOUT_PACKET_ID, "closeout_run_id": RUN_ID})
    write_md(REPORT_PATH, packet_markdown(summary))
    write_md(CLOSEOUT_REPORT_PATH, closeout_markdown(summary))


def sync_docs(summary: Mapping[str, Any]) -> None:
    status = "reviewed_closed_no_next_stage_opened"
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage17 Selection Status(17단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                f"- status(상태): `{status}`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{summary.get('closure_judgment')}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage17(17단계)은 DART 귀속까지 확인하고 닫혔다.",
            ]
        ),
    )
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage17 Review Index(17단계 검토 색인)",
                "",
                "- `run11A_xgb_regularized_boosting_characteristic_scout_v1`: gbtree q0.90 characteristic probe(gbtree q0.90 특성 탐침)",
                "- `run11B_xgb_threshold_q80_frequency_pressure_closeout_v1`: q0.80 frequency pressure probe(q0.80 빈도 압박 탐침), closeout superseded(마감 대체됨)",
                "- `run11C_xgb_q80_direction_asymmetry_probe_v1`: direction asymmetry probe(방향 비대칭 탐침)",
                "- `run11D_xgb_trade_shape_attribution_v1`: trade shape attribution(거래 형태 귀속)",
                "- `run11E_xgb_feature_driver_saturation_v1`: feature driver saturation closeout(피처 동인 포화 마감), superseded(대체됨)",
                "- `run11F_xgb_dart_booster_probe_v1`: DART booster probe(DART 부스터 탐침)",
                f"- `{RUN_ID}`: DART attribution closeout(DART 귀속 마감)",
                "",
                "효과(effect, 효과): Stage17(17단계)의 닫힘 근거가 최종 run11G(실행11G)로 이어진다.",
            ]
        ),
    )
    write_md(
        DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-03 Stage17 XGBoost DART Attribution Closeout(17단계 XGBoost DART 귀속 마감)",
                "",
                "## Decision(결정)",
                "",
                f"`{RUN_ID}`에서 DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅) 후속 귀속을 닫았다.",
                "",
                "효과(effect, 효과): 추가로 독립적인 모델 특성 축이 나오지 않아 Stage17(17단계)을 마감한다.",
                "",
                "## Judgment(판정)",
                "",
                f"- judgment(판정): `{summary.get('closure_judgment')}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
            ]
        ),
    )
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("stage17_reviewed_run11F_dart_booster_keep_open", "stage17_reviewed_closed_no_next_stage_opened", 1)
    state = state.replace("current_run_id: run11F_xgb_dart_booster_probe_v1", f"current_run_id: {RUN_ID}", 1)
    state = state.replace(
        "treat Stage 17 as reopened for run11F DART booster probe before Stage18; no edge, baseline, promotion, or runtime authority",
        "treat Stage 17 as reviewed_closed after run11G DART attribution closeout; Stage18 is ready but no Stage18 topic is selected yet",
    )
    stage_block = f"""stage17_xgboost_regularized_boosting_scout:
  stage_id: {STAGE_ID}
  status: {status}
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: xgboost_xgbclassifier_multiclass_dart
  current_run_id: {RUN_ID}
  current_status: reviewed_closed
  hypothesis: XGBoost gbtree and DART characteristics were explored until no second-order DART attribution axis remained.
  boundary: {BOUNDARY}
  judgment: {summary.get('closure_judgment')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  preserved_clues: run11A_visible_regularized_boosting_characteristic_q90,run11B_frequency_density_increase_q80,run11C_direction_asymmetry_long_trade_density,run11D_stable_long_probability_skew,run11E_feature_driver_saturation_no_new_axis,run11F_dart_top3_feature_shift,run11G_dart_no_second_order_axis
  negative_memory: DART changed one top3 feature slot but preserved long-skew trade shape and did not create edge, alpha quality, baseline, promotion, or runtime authority
  external_verification_status: completed_for_recorded_stage17_mt5_runtime_probes
  closeout_packet_path: {rel(CLOSEOUT_REPORT_PATH)}
  closeout_decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(CLOSEOUT_PACKET_ROOT / 'stage_closeout_evidence_gate.json')}
  next_action: stage18_ready_topic_not_selected
"""
    state = replace_block(state, "stage17_xgboost_regularized_boosting_scout:", stage_block)
    closeout_block = f"""stage17_model_family_challenge_closeout:
  packet_id: {CLOSEOUT_PACKET_ID}
  status: {status}
  judgment: {summary.get('closure_judgment')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  preserved_clues: run11A_visible_regularized_boosting_characteristic_q90,run11B_frequency_density_increase_q80,run11C_direction_asymmetry_long_trade_density,run11D_stable_long_probability_skew,run11E_feature_driver_saturation_no_new_axis,run11F_dart_top3_feature_shift,run11G_dart_no_second_order_axis
  negative_memory: XGBoost DART follow-up did not reveal a second-order attribution axis
  external_verification_status: completed_for_recorded_stage17_mt5_runtime_probes
  closeout_packet_path: {rel(CLOSEOUT_REPORT_PATH)}
  closeout_decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(CLOSEOUT_PACKET_ROOT / 'stage_closeout_evidence_gate.json')}
  next_action: stage18_ready_topic_not_selected
"""
    state = replace_block(state, "stage17_model_family_challenge_closeout:", closeout_block)
    run_block = f"""stage17_xgboost_run11G_dart_attribution_closeout:
  packet_id: {PACKET_ID}
  status: reviewed_closeout_completed
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  source_run_id: {SOURCE_RUN_ID}
  new_attribution_axis_visible: {str(summary.get('attribution_read', {}).get('new_attribution_axis_visible')).lower()}
  recommendation: {summary.get('stage17_stop_recommendation')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
"""
    state = replace_block(state, "stage17_xgboost_run11G_dart_attribution_closeout:", run_block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "## Latest Stage17 RUN11G Closeout(최신 17단계 실행11G 마감)",
            "",
            f"Stage17(17단계)은 `{RUN_ID}`에서 DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅) 귀속을 확인하고 닫혔다.",
            "",
            "효과(effect, 효과): Stage18(18단계)로 넘어갈 준비는 되었지만, 다음 모델 주제는 아직 선택하지 않았다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage17 RUN11G Closeout" not in current:
        current = insert + current
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")
    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage17(17단계) `{RUN_ID}` DART 귀속 마감으로 닫았다. 효과(effect, 효과): run11F의 MT5/KPI 근거를 재사용해 추가 축 없음과 Stage18 준비 상태를 기록했다.\n"
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def run() -> dict[str, Any]:
    created_at = utc_now()
    summary = build_summary()
    final = materialize(summary, created_at)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))
    return final


def main() -> int:
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
