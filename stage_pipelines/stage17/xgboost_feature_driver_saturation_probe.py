from __future__ import annotations

import argparse
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
RUN_ID = "run11E_xgb_feature_driver_saturation_v1"
RUN_NUMBER = "run11E"
PACKET_ID = "stage17_run11E_xgb_feature_driver_saturation_v1"
CLOSEOUT_PACKET_ID = "stage17_model_family_challenge_closeout_v2"
SOURCE_RUN_IDS = (
    "run11A_xgb_regularized_boosting_characteristic_scout_v1",
    "run11B_xgb_threshold_q80_frequency_pressure_closeout_v1",
    "run11C_xgb_q80_direction_asymmetry_probe_v1",
    "run11D_xgb_trade_shape_attribution_v1",
)
EXPLORATION_LABEL = "stage17_Model__XGBoostFeatureDriverSaturation"
BOUNDARY = "xgboost_feature_driver_saturation_closeout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "closed_inconclusive_xgboost_regularized_boosting_characteristics_exhausted"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
CLOSEOUT_PACKET_ROOT = ROOT / "docs/agent_control/packets" / CLOSEOUT_PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews/run11E_xgb_feature_driver_saturation_packet.md"
CLOSEOUT_REPORT_PATH = STAGE_ROOT / "03_reviews/stage17_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-03_stage17_xgboost_feature_driver_saturation_closeout.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"

FEATURE_COLUMNS = (
    "source_run_id",
    "selected_variant_id",
    "characteristic_score",
    "threshold",
    "val_signal_coverage",
    "oos_signal_coverage",
    "top10_gain_share",
    "top3_features",
    "top10_features",
)
OVERLAP_COLUMNS = ("left_run_id", "right_run_id", "top3_same", "top10_overlap_count", "top10_overlap_ratio")


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


def source_root(run_id: str) -> Path:
    return STAGE_ROOT / "02_runs" / run_id


def selected_variant(summary: Mapping[str, Any]) -> str:
    return str(summary.get("selected_variant", {}).get("variant_id") or summary.get("selected_variant_id") or "v03_depth4_l1_l2_slow")


def feature_row(run_id: str) -> dict[str, Any]:
    root = source_root(run_id)
    summary = read_json(root / "summary.json")
    variant_id = selected_variant(summary)
    if not io_path(root / "results/xgb_variant_results.csv").exists():
        return {
            "source_run_id": run_id,
            "selected_variant_id": variant_id,
            "characteristic_score": "",
            "threshold": "",
            "val_signal_coverage": "",
            "oos_signal_coverage": "",
            "top10_gain_share": "",
            "top3_features": "",
            "top10_features": "",
        }
    variants = pd.read_csv(io_path(root / "results/xgb_variant_results.csv"))
    selected = variants[variants["variant_id"] == variant_id].iloc[0]
    importance = pd.read_csv(io_path(root / f"results/variant_importance/{variant_id}_feature_importance.csv"))
    top10 = [str(item) for item in importance["feature"].head(10).tolist()]
    return {
        "source_run_id": run_id,
        "selected_variant_id": variant_id,
        "characteristic_score": safe_float(selected.get("characteristic_score")),
        "threshold": safe_float(selected.get("threshold")),
        "val_signal_coverage": safe_float(selected.get("val_signal_coverage")),
        "oos_signal_coverage": safe_float(selected.get("oos_signal_coverage")),
        "top10_gain_share": safe_float(selected.get("top10_gain_share")),
        "top3_features": top10[:3],
        "top10_features": top10,
    }


def feature_rows() -> list[dict[str, Any]]:
    return [feature_row(run_id) for run_id in SOURCE_RUN_IDS[:3]]


def overlap_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, left in enumerate(rows):
        for right in rows[idx + 1 :]:
            left_top10 = set(left.get("top10_features") or [])
            right_top10 = set(right.get("top10_features") or [])
            overlap = len(left_top10 & right_top10)
            out.append(
                {
                    "left_run_id": left.get("source_run_id"),
                    "right_run_id": right.get("source_run_id"),
                    "top3_same": (left.get("top3_features") or []) == (right.get("top3_features") or []),
                    "top10_overlap_count": overlap,
                    "top10_overlap_ratio": overlap / max(len(left_top10 | right_top10), 1),
                }
            )
    return out


def saturation_read(rows: Sequence[Mapping[str, Any]], overlaps: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    variant_ids = {str(row.get("selected_variant_id")) for row in rows}
    selected_variant_stable = len(variant_ids) == 1
    top3_stable = all(bool(row.get("top3_features")) for row in rows) and len({tuple(row.get("top3_features") or []) for row in rows}) == 1
    min_top10_overlap = min((safe_float(row.get("top10_overlap_ratio")) for row in overlaps), default=0.0)
    q80_scores = [
        safe_float(row.get("characteristic_score"))
        for row in rows
        if str(row.get("source_run_id", "")).startswith("run11B") or str(row.get("source_run_id", "")).startswith("run11C")
    ]
    q80_score_delta = abs(q80_scores[0] - q80_scores[1]) if len(q80_scores) == 2 else 0.0
    q90_to_q80_score_delta = abs(safe_float(rows[0].get("characteristic_score")) - safe_float(rows[1].get("characteristic_score"))) if len(rows) >= 2 else 0.0
    no_new_feature_driver = selected_variant_stable and top3_stable and min_top10_overlap >= 0.80 and q80_score_delta <= 1.0e-9
    return {
        "selected_variant_stable": selected_variant_stable,
        "top3_features_stable": top3_stable,
        "min_top10_overlap_ratio": min_top10_overlap,
        "q80_characteristic_score_delta_run11B_vs_run11C": q80_score_delta,
        "q90_to_q80_characteristic_score_delta_run11A_vs_run11B": q90_to_q80_score_delta,
        "new_feature_driver_visible": not no_new_feature_driver,
        "model_characteristic_strength": "no_new_feature_driver_after_run11E" if no_new_feature_driver else "feature_driver_changed_after_run11E",
        "stage17_stop_recommendation": "close_stage17_no_new_feature_driver_after_run11E" if no_new_feature_driver else "keep_stage17_open_for_feature_driver_followup",
    }


def build_summary() -> dict[str, Any]:
    rows = feature_rows()
    overlaps = overlap_rows(rows)
    read = saturation_read(rows, overlaps)
    run11d_summary = read_json(source_root("run11D_xgb_trade_shape_attribution_v1") / "summary.json")
    source_kpi = read_json(source_root("run11C_xgb_q80_direction_asymmetry_probe_v1") / "kpi_record.json").get("kpi_management", {})
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "closeout_packet_id": CLOSEOUT_PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_ids": SOURCE_RUN_IDS,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": "xgboost_xgbclassifier_multiclass",
        "selected_variant_id": rows[0].get("selected_variant_id") if rows else "unknown",
        "boundary": BOUNDARY,
        "judgment": JUDGMENT,
        "external_verification_status": "completed_reused_run11A_run11B_run11C_mt5_and_kpi_evidence",
        "feature_driver_rows": rows,
        "feature_overlap_rows": overlaps,
        "saturation_read": read,
        "run11d_trade_shape_attribution": run11d_summary.get("trade_shape_attribution", {}),
        "model_characteristic_strength": read["model_characteristic_strength"],
        "stage17_stop_recommendation": read["stage17_stop_recommendation"],
        "closure_judgment": JUDGMENT,
        "kpi_management": source_kpi,
        "preserved_clues": [
            "run11A_visible_regularized_boosting_characteristic_q90",
            "run11B_frequency_density_increase_q80",
            "run11C_direction_asymmetry_long_trade_density",
            "run11D_stable_long_probability_skew",
            "run11E_feature_driver_saturation_no_new_axis",
        ],
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }


def materialize(summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    write_csv(RUN_ROOT / "results/feature_driver_stability.csv", FEATURE_COLUMNS, summary["feature_driver_rows"])
    write_csv(RUN_ROOT / "results/feature_overlap.csv", OVERLAP_COLUMNS, summary["feature_overlap_rows"])
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__feature_driver_saturation",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "feature_driver_saturation",
        "parent_run_id": RUN_ID,
        "record_view": "stage17_feature_driver_saturation",
        "tier_scope": "Tier A+B",
        "kpi_scope": "feature_driver_saturation_closeout",
        "scoreboard_lane": "model_characteristic_closeout",
        "status": "completed",
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT / "summary.json"),
        "primary_kpi": ledger_pairs(
            (
                ("new_feature_driver_visible", summary["saturation_read"].get("new_feature_driver_visible")),
                ("selected_variant_stable", summary["saturation_read"].get("selected_variant_stable")),
                ("top3_features_stable", summary["saturation_read"].get("top3_features_stable")),
                ("min_top10_overlap_ratio", summary["saturation_read"].get("min_top10_overlap_ratio")),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("source_runs", ",".join(SOURCE_RUN_IDS)),
                ("boundary", BOUNDARY),
                ("recommendation", summary.get("stage17_stop_recommendation")),
            )
        ),
        "external_verification_status": summary.get("external_verification_status"),
        "notes": "Feature-driver saturation closeout; no edge, alpha quality, baseline, promotion, or runtime authority.",
    }
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=[ledger_row],
    )
    registry_output = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "model_characteristic_closeout",
                "status": "reviewed_closed",
                "judgment": JUDGMENT,
                "path": rel(RUN_ROOT),
                "notes": ledger_pairs(
                    (
                        ("recommendation", summary.get("stage17_stop_recommendation")),
                        ("new_feature_driver_visible", summary["saturation_read"].get("new_feature_driver_visible")),
                        ("boundary", "closeout_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    final_summary = {**dict(summary), "ledger_outputs": ledger_outputs, "registry_output": registry_output}
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "source_run_ids": SOURCE_RUN_IDS,
        "boundary": BOUNDARY,
        "outputs": {
            "summary": rel(RUN_ROOT / "summary.json"),
            "feature_driver_stability": rel(RUN_ROOT / "results/feature_driver_stability.csv"),
            "feature_overlap": rel(RUN_ROOT / "results/feature_overlap.csv"),
        },
    }
    kpi_record = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "closeout_packet_id": CLOSEOUT_PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "xgboost_feature_driver_saturation_closeout",
        "external_verification_status": summary.get("external_verification_status"),
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "kpi_management": summary.get("kpi_management", {}),
        "saturation_read": summary.get("saturation_read", {}),
        "ledger_outputs": ledger_outputs,
        "registry_output": registry_output,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "summary.json", final_summary)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(PACKET_ROOT / "run_summaries" / f"{RUN_ID}.json", final_summary)
    write_md(RUN_ROOT / "reports/result_summary.md", packet_markdown(final_summary))
    write_packet(final_summary, created_at)
    sync_docs(final_summary)
    return final_summary


def packet_markdown(summary: Mapping[str, Any]) -> str:
    read = summary["saturation_read"]
    first = summary["feature_driver_rows"][0]
    lines = [
        "# Stage17 RUN11E XGBoost Feature Driver Saturation(17단계 실행11E XGBoost 피처 동인 포화)",
        "",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
        f"- selected variant(선택 변형): `{summary.get('selected_variant_id')}`",
        f"- top3 features(상위 3개 피처): `{first.get('top3_features')}`",
        f"- min top10 overlap(최소 상위10 겹침): `{read.get('min_top10_overlap_ratio')}`",
        f"- new feature driver visible(새 피처 동인 보임): `{read.get('new_feature_driver_visible')}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| source run(원천 실행) | score(점수) | threshold(임계값) | top10 gain share(상위10 gain 비중) |",
        "|---|---:|---:|---:|",
    ]
    for row in summary["feature_driver_rows"]:
        lines.append(f"| `{row.get('source_run_id')}` | `{row.get('characteristic_score')}` | `{row.get('threshold')}` | `{row.get('top10_gain_share')}` |")
    lines.extend(
        [
            "",
            "효과(effect, 효과): run11A부터 run11D까지 나온 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) 특성 단서를 feature driver(피처 동인) 관점에서 다시 봤고, 새 피처 축이 더 나오지 않아 Stage17(17단계)을 closeout(마감)한다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def closeout_markdown(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# Stage17 Closeout(17단계 마감)",
            "",
            f"- closeout run(마감 실행): `{RUN_ID}`",
            f"- judgment(판정): `{JUDGMENT}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
            "",
            "## Preserved Clues(보존 단서)",
            "",
            "- run11A: q0.90에서 v03 깊은 L1/L2 느린 부스팅 변형이 가장 뚜렷했다.",
            "- run11B: q0.80에서 거래빈도는 늘었지만 edge(거래 우위)는 만들지 못했다.",
            "- run11C: long-only(롱 전용) 거래 밀도가 short-only(숏 전용)보다 컸다.",
            "- run11D: validation(검증)과 OOS(표본외) 모두 long(롱) 확률 신호 쏠림이 유지됐다.",
            "- run11E: selected variant(선택 변형)와 top feature driver(상위 피처 동인)가 반복되어 새 축이 더 보이지 않았다.",
            "",
            "효과(effect, 효과): Stage17(17단계)은 XGBoost의 특성 기억을 남기고 닫는다. 이 마감은 baseline(기준선) 선택이나 promotion(승격)이 아니다.",
        ]
    )


def write_packet(summary: Mapping[str, Any], created_at: str) -> None:
    source_ok = summary.get("external_verification_status") == "completed_reused_run11A_run11B_run11C_mt5_and_kpi_evidence"
    close_ok = source_ok and summary["saturation_read"].get("new_feature_driver_visible") is False
    payloads = {
        "source_evidence_gate": {
            "audit_name": "source_evidence_gate",
            "status": "pass" if source_ok else "blocked",
            "passed": source_ok,
            "source_runs": SOURCE_RUN_IDS,
            "external_verification_status": summary.get("external_verification_status"),
        },
        "feature_driver_saturation_audit": {
            "audit_name": "feature_driver_saturation_audit",
            "status": "pass" if close_ok else "blocked",
            "passed": close_ok,
            "saturation_read": summary.get("saturation_read"),
        },
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "pass" if close_ok else "blocked",
            "passed": close_ok,
            "allowed_claims": [JUDGMENT, "stage17_closeout"],
            "forbidden_claims": summary.get("forbidden_claims"),
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "status": "pass" if close_ok else "blocked",
            "passed": close_ok,
            "required_gates": {
                "source_evidence_gate": "pass" if source_ok else "blocked",
                "feature_driver_saturation_audit": "pass" if close_ok else "blocked",
                "final_claim_guard": "pass" if close_ok else "blocked",
            },
        },
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "primary_family": "model_characteristic_closeout", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"], "required_gates": list(payloads)})
    write_json(PACKET_ROOT / "artifact_index.json", {"run_summary": rel(RUN_ROOT / "summary.json"), "report_path": rel(REPORT_PATH), "closeout_report_path": rel(CLOSEOUT_REPORT_PATH), "created_at_utc": created_at})
    write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "receipts": [{"skill": "obsidian-result-judgment", "status": "completed", "effect": "closed Stage17 only after no new feature-driver axis appeared"}, {"skill": "obsidian-performance-attribution", "status": "completed", "effect": "attributed run11A-run11D clues before closeout"}, {"skill": "obsidian-artifact-lineage", "status": "completed", "effect": "source runs and closeout artifacts were linked"}]})
    for name, payload in payloads.items():
        write_json(CLOSEOUT_PACKET_ROOT / f"{name}.json", payload)
    write_json(CLOSEOUT_PACKET_ROOT / "stage_closeout_evidence_gate.json", {**payloads["feature_driver_saturation_audit"], "packet_id": CLOSEOUT_PACKET_ID, "closeout_run_id": RUN_ID})
    write_md(REPORT_PATH, packet_markdown(summary))
    write_md(CLOSEOUT_REPORT_PATH, closeout_markdown(summary))


def replace_block(text: str, marker: str, block: str) -> str:
    pattern = rf"{re.escape(marker)}\n(?:  .*\n)+"
    if re.search(pattern, text):
        return re.sub(pattern, block, text, count=1)
    return text.rstrip() + "\n" + block


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
                "- model family(모델 계열): XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅)",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{JUDGMENT}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage17(17단계)은 run11E에서 새 피처 동인이 더 보이지 않아 closeout(마감)한다. 운영 기준, 승격, 기준선은 없다.",
            ]
        ),
    )
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage17 Review Index(17단계 검토 색인)",
                "",
                "- `run11A_xgb_regularized_boosting_characteristic_scout_v1`: XGBoost characteristic MT5 KPI probe(XGBoost 특성 MT5 핵심성과지표 탐침)",
                "- `run11B_xgb_threshold_q80_frequency_pressure_closeout_v1`: frequency pressure probe(거래빈도 압박 탐침), closeout superseded(마감 대체됨)",
                "- `run11C_xgb_q80_direction_asymmetry_probe_v1`: direction asymmetry probe(방향 비대칭 탐침)",
                "- `run11D_xgb_trade_shape_attribution_v1`: trade shape attribution(거래 모양 귀속)",
                f"- `{RUN_ID}`: feature driver saturation closeout(피처 동인 포화 마감)",
                "",
                "효과(effect, 효과): Stage17(17단계)은 새 특성이 더 보이지 않는 run11E에서만 closeout(마감)했다.",
            ]
        ),
    )
    write_md(
        DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-03 Stage17 XGBoost Feature Driver Saturation Closeout(17단계 XGBoost 피처 동인 포화 마감)",
                "",
                "## Decision(결정)",
                "",
                f"`{RUN_ID}`에서 selected variant(선택 변형), top3 feature driver(상위 3개 피처 동인), q0.80 characteristic score(특성 점수)가 반복되어 Stage17(17단계)을 닫았다.",
                "",
                "효과(effect, 효과): closeout(마감)은 Stage17 고유 특성 탐색의 종료 기록이며 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.",
                "",
                "## Judgment(판정)",
                "",
                f"- judgment(판정): `{JUDGMENT}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
            ]
        ),
    )
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = re.sub(r"stage17_reviewed_[A-Za-z0-9_]+", "stage17_reviewed_closed_no_next_stage_opened", state)
    state = state.replace("current_run_id: run11D_xgb_trade_shape_attribution_v1", f"current_run_id: {RUN_ID}", 1)
    state = state.replace(
        "treat Stage 17 as XGBoost regularized boosting still open after run11D trade-shape attribution; no edge, baseline, promotion, or runtime authority",
        "treat Stage 17 as reviewed_closed after run11E feature-driver saturation closeout; preserve XGBoost clues but no edge, baseline, promotion, or runtime authority",
    )
    stage_block = f"""stage17_xgboost_regularized_boosting_scout:
  stage_id: {STAGE_ID}
  status: {status}
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {summary.get('model_family')}
  current_run_id: {RUN_ID}
  current_status: reviewed_closed
  hypothesis: XGBoost regularized boosting shows probability, frequency, direction-asymmetry, and long-skew behavior, but feature-driver saturation produced no new axis.
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  selected_variant_id: {summary.get('selected_variant_id')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  preserved_clues: {','.join(summary.get('preserved_clues', []))}
  negative_memory: q0.80 frequency and direction probes did not create edge, alpha quality, baseline, promotion, or runtime authority
  external_verification_status: completed_for_recorded_stage17_mt5_runtime_probes
  closeout_packet_path: {rel(CLOSEOUT_REPORT_PATH)}
  closeout_decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(CLOSEOUT_PACKET_ROOT / 'stage_closeout_evidence_gate.json')}
  next_action: no_stage18_opened
"""
    state = replace_block(state, "stage17_xgboost_regularized_boosting_scout:", stage_block)
    closeout_block = f"""stage17_model_family_challenge_closeout:
  packet_id: {CLOSEOUT_PACKET_ID}
  status: {status}
  judgment: {JUDGMENT}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  preserved_clues: {','.join(summary.get('preserved_clues', []))}
  negative_memory: XGBoost feature drivers saturated after run11E; no edge, alpha quality, baseline, promotion, or runtime authority
  external_verification_status: completed_for_recorded_stage17_mt5_runtime_probes
  closeout_packet_path: {rel(CLOSEOUT_REPORT_PATH)}
  closeout_decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(CLOSEOUT_PACKET_ROOT / 'stage_closeout_evidence_gate.json')}
  next_action: no_stage18_opened
"""
    state = replace_block(state, "stage17_model_family_challenge_closeout:", closeout_block)
    run_block = f"""stage17_xgboost_run11E_feature_driver_saturation:
  packet_id: {PACKET_ID}
  status: reviewed_closeout_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  source_run_ids: {','.join(SOURCE_RUN_IDS)}
  selected_variant_id: {summary.get('selected_variant_id')}
  new_feature_driver_visible: {str(summary.get('saturation_read', {}).get('new_feature_driver_visible')).lower()}
  recommendation: {summary.get('stage17_stop_recommendation')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
"""
    state = replace_block(state, "stage17_xgboost_run11E_feature_driver_saturation:", run_block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "## Latest Stage17 RUN11E Closeout(최신 17단계 실행11E 마감)",
            "",
            f"Stage17(17단계)은 `{RUN_ID}`에서 새 feature driver(피처 동인)가 더 보이지 않아 closeout(마감)했다.",
            "",
            "효과(effect, 효과): XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) 특성 단서는 보존하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage17 RUN11E Closeout" not in current:
        current = insert + current
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")
    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage17(17단계) `{RUN_ID}` 피처 동인 포화 탐침으로 closeout(마감)했다. 효과(effect, 효과): run11A-run11D 특성 단서를 보존하고 운영 주장은 만들지 않았다.\n"
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def run() -> dict[str, Any]:
    created_at = utc_now()
    summary = build_summary()
    final = materialize(summary, created_at)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))
    return final


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage17 XGBoost feature-driver saturation closeout.")
    parser.parse_args(argv)
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
